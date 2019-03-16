import json
import sys
import threading
import time
import uuid
import sys
import zmq
from datetime import datetime


class BidirectionalConnection:

    def __init__(self, broker_ip, own_ip_address, first_topic):
        self.context = zmq.Context()
        self.topic_list = []
        self.broker_ip = broker_ip
        self.own_ip_address = own_ip_address
        self.pub_socket = self.context.socket(zmq.PUB)
        self.pub_socket.connect("tcp://" + broker_ip + ":5555")
        self.sub_socket = self.context.socket(zmq.SUB)
        self.sub_socket.connect("tcp://" + broker_ip + ":5556")
        self.sub_socket.setsockopt_string(zmq.SUBSCRIBE, "HEARTBEAT".decode('ascii'))
        time.sleep(3)

        self.add_topic(first_topic)
        self.all_brokers = []

        self.new_topic_location_map = {}
        # Start thread to send heartbeats
        self.received_heartbeat = True
        self.is_dead = False
        self.start_background_threads()

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

    def send_message(self, topic, msg):
        if topic in self.topic_list:
            self.pub_socket.send_string("%s %s" % (topic, json.dumps(msg, separators=(",", ":"))))
            return True
        else:
            # topic needs to be re-registered elsewhere
            return False

    def get_new_location(self, topic):
        if topic in self.new_topic_location_map:
            return self.new_topic_location_map[topic]
        else:
            return None

    def receive_messages(self):
        try:
            while not self.is_dead:
                response_string = self.sub_socket.recv()
                if type(response_string) != type(None):
                    response_code, msg_string = response_string.split()
                    msg = json.loads(msg_string)
                    if response_code == "HEARTBEAT":
                        self.received_heartbeat = True
                        self.all_brokers = msg["ip_list"]
                    else:
                        if msg["contents"] == "TOPIC_MOVED":
                            self.new_topic_location_map[response_code] = msg["new_ip"]
                            self.topic_list.remove(response_code)
                            print "Topic", response_code, "moved to ip", msg["new_ip"]
        except:
            # Ignore errors here, they sometimes pop up when closing thread
            return

    def heartbeat(self):
        try:
            timeout = 10
            while self.received_heartbeat:
                self.received_heartbeat = False
                time.sleep(timeout/2)
                for topic in self.topic_list:
                    msg = {"ip": self.own_ip_address,
                           "val": "",
                           "heartbeat": True}
                    self.send_message(topic, msg)
                time.sleep(timeout/2)
                for topic in self.topic_list:
                    msg = {"ip": self.own_ip_address,
                           "val": "",
                           "heartbeat": True}
                    self.send_message(topic, msg)
            self.is_dead = True
        except:
            # Ignore errors here, sometimes pop up at end when cleaning up threads
            return

    def start_background_threads(self):
        timeout_thread = threading.Thread(target=self.heartbeat)
        timeout_thread.daemon = True
        timeout_thread.start()
        # Start thread to receive heartbeats
        receive_heartbeat_thread = threading.Thread(target=self.receive_messages)
        receive_heartbeat_thread.daemon = True
        receive_heartbeat_thread.start()


class Publisher:

    def __init__(self, own_ip_address, broker_ip):
        self.context = zmq.Context()

        self.own_ip_address = own_ip_address

        # List of BidirectionalConnection objects
        self.connection_list = []

        # Maps topics to index in connection_list
        self.topic_map = {}

        # Maps ips to index in connection_list
        self.ip_map = {}

        # Maps topics to history
        self.history_map = {}

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
                                self.register(topic, self.ownership_strength_map[topic], None, connection.broker_ip)
                            del self.ip_map[connection.broker_ip]
                            self.connection_list[i] = None
                        else:
                            self.known_brokers = connection.all_brokers
                    i += 1
            except ValueError as e:
                print "Issue with checking if dead if this keeps appearing, not concerning otherwise"
                
    def register(self, topic, ownership_strength=0, history=0, previous_ip = None, first_ip_to_try = None):
        print "Trying to register"
        # TODO: Break into helper functions - currently 60 lines long
        msg_to_send = {"topic": topic,
               "ip": self.own_ip_address,
               "ownership_strength": ownership_strength,
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
            temp_sub_socket.setsockopt_string(zmq.SUBSCRIBE, "register_pub_response".decode('ascii'))
            temp_sub_socket.RCVTIMEO = 5
            time.sleep(2)
            temp_pub_socket.send_string("%s %s" % ("register_pub", formatted_message))
            temp_pub_socket.close()
            try:
                while True:
                    return_topic, return_message_string = temp_sub_socket.recv().split()
                    return_message = json.loads(return_message_string)
                    if return_message["topic"] == topic:
                        temp_sub_socket.close()
                        correct_ip = return_message["ip"]
                        connection = None
                        if correct_ip in self.ip_map:
                            connection = self.connection_list[self.ip_map[correct_ip]]
                            connection.add_topic(topic)
                            self.topic_map[topic] = self.ip_map[correct_ip]
                        else:
                            connection = BidirectionalConnection(correct_ip, self.own_ip_address, topic)
                            self.connection_list.append(connection)
                            self.ip_map[correct_ip] = len(self.connection_list)-1
                            self.topic_map[topic] = len(self.connection_list)-1
                        if correct_ip != ip:
                            msg_to_send["previous_ip"] = None
                            connection.send_message("register_pub", msg_to_send)
                            connection.pub_socket.send_string("%s %s" % ("register_pub", json.dumps(msg_to_send, separators=(",", ":"))))
                        history_list = []
                        if history is not None:
                            for i in range(history):
                                history_list.append(None)
                        self.history_map[topic] = history_list
                        self.ownership_strength_map[topic] = ownership_strength
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

    def publish(self, topic, val):
        cur_date_time = str(datetime.now())
        cur_date_time = cur_date_time.replace(" ", "T")
        cur_history = self.history_map[topic]
        msg = {"ip": self.own_ip_address,
               "val": val,
               "heartbeat": False,
               "datetime": cur_date_time,
               "history": cur_history}
        connection_index = self.topic_map[topic]
        if self.connection_list[connection_index] is None:
            # If that publisher has died, re-register
            print "Failed to publish, switching address"
            self.register(topic, self.ownership_strength_map[topic], None, None)
            self.publish(topic, val)
        elif self.connection_list[connection_index].send_message(topic, msg):
            # If sending was successful
            cur_history.append(val)
            del cur_history[0]
            self.history_map[topic] = cur_history
            print "Publishing to topic", topic, "message:", val
        else:
            print "Failed to publish, switching address"
            # If sending was unsuccessful, need to reregister/resend
            self.new_location = None
            self.new_location = self.connection_list[connection_index].get_new_location(topic)
            first_ip_to_try = None
            if self.new_location is not None:
                first_ip_to_try = self.new_location
            self.register(topic, self.ownership_strength_map[topic], None, None)
            self.publish(topic, val)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "ERROR, need to specify 2 arguments - ip of this node, and an ip of a broker"
    else:
        own_ip_address = sys.argv[1]
        broker_ip = sys.argv[2]
        pub = Publisher(own_ip_address, broker_ip)
        print "Publisher created"
        time.sleep(1)
        pub.register("dogs", 3, 3)
        pub.register("cats", 3, 3)
        time.sleep(1)
        while True:
            pub.publish("dogs", "cool")
            pub.publish("cats", "uncool")
            time.sleep(5)
