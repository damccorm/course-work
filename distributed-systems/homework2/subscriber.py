import zmq
import json
import time
import datetime
import threading
import sys
from collections import deque


class Connection:

    def __init__(self, broker_ip, first_topic, messages):
        self.context = zmq.Context()
        self.messages = messages
        self.topic_list = []
        self.broker_ip = broker_ip
        self.pub_socket = self.context.socket(zmq.PUB)
        self.pub_socket.connect("tcp://" + broker_ip + ":5555")
        self.sub_socket = self.context.socket(zmq.SUB)
        self.sub_socket.connect("tcp://" + broker_ip + ":5556")
        self.sub_socket.setsockopt_string(zmq.SUBSCRIBE, "HEARTBEAT".decode('ascii'))
        time.sleep(3)

        self.add_topic(first_topic)
        self.all_brokers = []

        self.new_topic_location_map = {}
        self.received_heartbeat = True
        self.is_dead = False

        self.start_background_thread()

    def add_topic(self, topic):
        self.topic_list.append(topic)
        self.sub_socket.setsockopt_string(zmq.SUBSCRIBE, topic.decode("ascii"))

    def remove_topic(self, topic):
        # Removes topic from list, returns True if connection still has topics, false otherwise
        # If no topic remains, closes sockets
        self.topic_list.remove(topic)
        if len(self.topic_list) > 0:
            return True
        else:
            self.pub_socket.close()
            self.sub_socket.close()
            return False

    def get_new_location(self, topic):
        if topic in self.new_topic_location_map:
            return self.new_topic_location_map[topic]
        else:
            return None

    def receive_messages(self):
        while not self.is_dead:
            response_string = self.sub_socket.recv()
            if type(response_string) != type(None):
                response_code, msg_string = response_string.split()
                msg = json.loads(msg_string)
                if response_code == "HEARTBEAT":
                    self.received_heartbeat = True
                    self.all_brokers = msg["ip_list"]
                elif msg["contents"] == "TOPIC_MOVED":
                    self.new_topic_location_map[response_code] = msg["new_ip"]
                    self.topic_list.remove(response_code)
                    print "Topic", response_code, "moved to ip", msg["new_ip"]
                # if this is a standard message
                else:
                    sent_date_time_string = msg["datetime"]
                    sent_date_time = datetime.datetime.strptime(sent_date_time_string, "%Y-%m-%dT%H:%M:%S.%f")
                    time_to_send = datetime.datetime.now() - sent_date_time
                    self.messages.append((response_string, time_to_send))

    def start_background_thread(self):
        # Start thread to receive heartbeats
        receive_heartbeat_thread = threading.Thread(target=self.receive_messages)
        receive_heartbeat_thread.daemon = True
        receive_heartbeat_thread.start()


class Subscriber:
    def __init__(self, broker_ip):

        self.context = zmq.Context()

        self.messages = deque()

        # List of BidirectionalConnection objects
        self.connection_list = []

        # Maps topics to index in connection_list
        self.topic_map = {}

        # Maps ips to index in connection_list
        self.ip_map = {}

        # Maps topics to history and amount of history desired
        self.history_map = {}
        self.history_amount = {}

        # Maps topics to ownership strength
        self.ownership_strength_map = {}

        self.known_brokers = [broker_ip]

        dead_broker_thread = threading.Thread(target=self.check_if_dead)
        dead_broker_thread.daemon = True
        dead_broker_thread.start()

    def check_if_dead(self):
        while True:
            time.sleep(5)
            i = 0
            try:
                while i < len(self.connection_list):
                    connection = self.connection_list[i]
                    if connection is not None:
                        if connection.is_dead:
                            print "Discovered dead connection", connection.broker_ip
                            self.known_brokers.remove(connection.broker_ip)
                            for topic in connection.topic_list:
                                self.register(topic, 0, connection.broker_ip)
                            del self.ip_map[connection.broker_ip]
                            self.connection_list[i] = None
                        else:
                            self.known_brokers = connection.all_brokers
                    i += 1
            except ValueError as e:
                print "Issue with checking if dead if this keeps appearing, not concerning otherwise"

    def register(self, topic, history=0, previous_ip=None, first_ip_to_try=None):
        print "Trying to register"
        # TODO: Break into helper functions - currently 60 lines long
        msg_to_send = {"topic": topic,
                       "history": history,
                       "previous_ip": previous_ip}
        formatted_message = json.dumps(msg_to_send, separators=(",", ":"))
        while len(self.known_brokers) > 0 or first_ip_to_try is not None:
            ip = self.known_brokers[0]
            if first_ip_to_try is not None:
                ip = first_ip_to_try
            temp_pub_socket = self.context.socket(zmq.PUB)
            temp_pub_socket.connect("tcp://" + ip + ":5555")
            temp_sub_socket = self.context.socket(zmq.SUB)
            temp_sub_socket.connect("tcp://" + ip + ":5556")
            temp_sub_socket.setsockopt_string(zmq.SUBSCRIBE, "register_sub_response".decode('ascii'))
            temp_sub_socket.RCVTIMEO = 5
            time.sleep(2)
            temp_pub_socket.send_string("%s %s" % ("register_sub", formatted_message))
            temp_pub_socket.close()
            try:
                while True:
                    return_topic, return_message_string = temp_sub_socket.recv().split()
                    return_message = json.loads(return_message_string)
                    if return_message["topic"] == topic:
                        temp_sub_socket.close()
                        correct_ip = return_message["ip"]
                        if correct_ip in self.ip_map:
                            connection = self.connection_list[self.ip_map[correct_ip]]
                            connection.add_topic(topic)
                            self.topic_map[topic] = self.ip_map[correct_ip]
                        else:
                            connection = Connection(correct_ip, topic, self.messages)
                            self.connection_list.append(connection)
                            self.ip_map[correct_ip] = len(self.connection_list)-1
                            self.topic_map[topic] = len(self.connection_list)-1
                        if correct_ip != ip:
                            msg_to_send["previous_ip"] = None
                            connection.send_message("register_sub", msg_to_send)
                            connection.pub_socket.send_string("%s %s" % ("register_sub", json.dumps(msg_to_send, separators=(",", ":"))))
                        self.history_map[topic] = return_message["history"]
                        self.history_amount[topic] = history
                        print(str(topic) + " history is " + str(return_message["history"]))
                        print "Registered for topic", topic, "at ip", correct_ip
                        return
            except:
                # It didn't get back soon enough, we will move on to the next known broker.
                # This is useful in the case of multiple brokers dying at once.
                if first_ip_to_try is not None:
                    first_ip_to_try = None
                else:
                    del self.known_brokers[0]
        print "Failed to register", topic

    def notify(self):
        while True:
            if self.history_map:
                for history_topic in self.history_map.keys():
                    desired_history = self.history_amount[history_topic]
                    history = self.history_map[history_topic]
                    if desired_history > 0:
                        self.history_amount[history_topic] = 0
                        print(str(history))
                        # if we obtain no history or less than we asked for
                        if not history or desired_history > len(history):
                            print("Insufficient publisher history.")
                        else:
                            length = len(history)
                            has_null_element = False
                            for i in range(desired_history):
                                if not history[length - (i + 1)]:
                                    has_null_element = True
                            if has_null_element:
                                print("Insufficient publisher history.")
                            else:
                                for i in range(desired_history):
                                    print(history_topic + " HISTORY " + str(i + 1) + ": "
                                          + str(history[length - (i + 1)]))
                    del self.history_map[history_topic]
            if len(self.messages) > 0:
                message = self.messages.popleft()
                time_to_send = message[1]
                topic, mjson = message[0].split()
                msg = json.loads(mjson)
                print("%s: %s" % (topic, msg["contents"]))
                print "Time to send:", 1000 * time_to_send.total_seconds(), "milliseconds"

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "ERROR, need to specify an ip of a broker"
    else:
        broker_addr = sys.argv[1]
        sub = Subscriber(broker_addr)
        print "Subscriber created"
        time.sleep(10)
        sub.register("dogs", 3)
        print "Subscriber registered for dogs"
        time.sleep(1)
        sub.notify()
