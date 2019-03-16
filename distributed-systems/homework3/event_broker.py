import zmq
import logging
import time
import threading
import json
from kazoo.client import KazooClient


class Topic:
    def __init__(self, topic, leader_id, strength, history):
        self.topic = topic
        self.cur_leader_id = leader_id
        self.ownership_strength_map = {leader_id: strength}
        self.history_map = {leader_id: history}
        self.history = []
        self.dead_leader = False
        self.change_leader = False

        self.start_timeout_routine()

    def add_publisher(self, leader_id, strength, history):
        # Adds publisher for this topic.
        self.ownership_strength_map[leader_id] = strength
        self.history_map[leader_id] = history        
        if strength > self.ownership_strength_map[self.cur_leader_id]:
            self.cur_leader_id = leader_id

    def receive_message(self, cur_id, message_contents, is_heartbeat):
        # Processes message for this topic. Returns True if message should be relayed to subscribers.
        if self.change_leader:
            if cur_id != self.cur_leader_id:
                self.remove_publisher(self.cur_leader_id)
            self.start_timeout_routine()
        if cur_id == self.cur_leader_id:
            self.dead_leader = False
            if not is_heartbeat:
                self.history.append(message_contents)
                while len(self.history) > self.history_map[self.cur_leader_id]:
                    del self.history[0]
                return True
        return False

    def remove_publisher(self, publisher_id):
        # Removes dead publisher from topic.
        del self.ownership_strength_map[publisher_id]
        del self.history_map[publisher_id]
        cur_max_strength = 0
        self.cur_leader_id = -1
        for cur_id in self.ownership_strength_map:
            strength = self.ownership_strength_map[cur_id]
            if strength > cur_max_strength:
                cur_max_strength = strength
                self.cur_leader_id = cur_id

    def timeout_routine(self):
        # Routine to see if publisher has died.
        self.dead_leader = False
        self.change_leader = False
        while not self.dead_leader:
            self.dead_leader = True
            time.sleep(10)
        self.change_leader = True

    def start_timeout_routine(self):
        # Starts timeout routine.
        timeout_thread = threading.Thread(target=self.timeout_routine)
        timeout_thread.daemon = True
        timeout_thread.start()


class EventBroker:

    def __init__(self):
        self.context = zmq.Context()
        logging.basicConfig()
        # maps topic strings to topic class
        self.topic_map = {}
        self.num_messages_processed = 0

        self.is_leader = False
        self.zk = KazooClient(hosts='127.0.0.1:2181')
        self.zk.start()
        print "zookeeper started with state", self.zk.state
        self.zk.ensure_path("/MESSAGES")
        try:
            self.zk.create("/LEADER", b"0", ephemeral=True)
            print "BECAME LEADER INITIALLY"
            self.is_leader = True
        except:
            @self.zk.ChildrenWatch("/MESSAGES")
            def watch_children(children):
                print "CHILDREN", children
                # Receive messages and update state in background so that on failure can pick up where leader left off
                while self.num_messages_processed < len(children):
                    received_string = self.zk.get("/MESSAGES/"+children[self.num_messages_processed])[0]
                    self.num_messages_processed += 1
                    print "Received:", received_string
                    register_code, mjson = received_string.split()
                    msg = json.loads(mjson)
                    if register_code == "registerpub":
                        topic = msg["topic"]
                        sender_id = msg["pId"]
                        history = msg["history"]
                        ownership_strength = msg["ownership_strength"]
                        if topic in self.topic_map:
                            self.topic_map[topic].add_publisher(sender_id, ownership_strength, history)
                        else:
                            self.topic_map[topic] = Topic(topic, sender_id, ownership_strength, history)
                    else:
                        topic = register_code
                        sender_id = msg["pId"]
                        message_contents = msg["val"]
                        is_heartbeat = msg["heartbeat"]
                        if topic in self.topic_map:
                            self.topic_map[topic].receive_message(sender_id, message_contents, is_heartbeat)

            @self.zk.DataWatch("/LEADER")
            def watch_func(data, stat):
                if data is not None:
                    return True
                # If data is none, might be able to get node
                try:
                    self.zk.create("/LEADER", b"0", ephemeral=True)
                    print "BECAME LEADER"
                    self.is_leader = True
                    return False
                except:
                    print "FAILED TO BECOME LEADER, OTHER NODE BEAT THIS ONE"
                    return True

        
        while not self.is_leader:
            time.sleep(1)

        self.start()

    def publish_to_subscribers(self, topic, message_contents, sent_date_time, sender_id=None):
        # Send messages to subscribers
        msg = {"contents": message_contents,
               "sender_id": sender_id,
               "datetime": sent_date_time}
        self.xpub_socket.send_string("%s %s" % (topic, json.dumps(msg, separators=(",", ":"))))

        
    def start(self):
        for topic in self.topic_map:
            # Make sure we don't mark anyone as dead until they have a chance to publish
            self.topic_map[topic].change_leader = False
            if self.topic_map[topic].dead_leader:
                self.topic_map[topic].dead_leader = False
                self.topic_map[topic].start_timeout_routine()

        # bind to publisher socket as SUB
        self.xsub_socket = self.context.socket(zmq.SUB)
        self.xsub_socket.bind("tcp://127.0.0.1:5555")

        # bind to subscriber socket as PUB
        self.xpub_socket = self.context.socket(zmq.PUB)
        self.xpub_socket.bind("tcp://127.0.0.1:5556")

        self.xsub_socket.setsockopt_string(zmq.SUBSCRIBE, "registerpub".decode("ascii"))
        self.xsub_socket.setsockopt_string(zmq.SUBSCRIBE, "registersub".decode("ascii"))
        for topic in self.topic_map:
            self.xsub_socket.setsockopt_string(zmq.SUBSCRIBE, topic.decode("ascii"))
        print "NEW LEADER"
        should_continue = True
        while should_continue:
            received_string = self.xsub_socket.recv()
            print "Received:", received_string
            register_code, mjson = received_string.split()
            msg = json.loads(mjson)
            if register_code == "registerpub":
                # Forward register message to all other brokers
                self.zk.create("/MESSAGES/TEST" + str(len(self.zk.get_children("/MESSAGES"))), received_string)
                # Register a publisher
                topic = msg["topic"]
                sender_id = msg["pId"]
                history = msg["history"]
                ownership_strength = msg["ownership_strength"]
                if topic in self.topic_map:
                    self.topic_map[topic].add_publisher(sender_id, ownership_strength, history)
                else:
                    self.topic_map[topic] = Topic(topic, sender_id, ownership_strength, history)
                    self.xsub_socket.setsockopt_string(zmq.SUBSCRIBE, topic.decode("ascii"))
            elif register_code == "registersub":
                # deal with stuff from subscribers
                topic = msg["topic"]
                sender_id = msg["sId"]
                history = msg["history"]
                if topic in self.topic_map:
                    history_list = self.topic_map[topic].history
                    history = min(history, len(history_list))
                    i = len(history_list) - 1
                    while history > 0:
                        self.publish_to_subscribers(topic, history_list[i], None, sender_id)
                        history -= 1
                        i -= 1
            else:
                # Forward register message to all other brokers
                self.zk.create("/MESSAGES/TEST" + str(len(self.zk.get_children("/MESSAGES"))), received_string)
                topic = register_code
                sender_id = msg["pId"]
                message_contents = msg["val"]
                is_heartbeat = msg["heartbeat"]
                if topic in self.topic_map:
                    if self.topic_map[topic].receive_message(sender_id, message_contents, is_heartbeat):
                        sent_date_time = msg["datetime"]
                        self.publish_to_subscribers(topic, message_contents, sent_date_time)
                else:
                    print("Publishing to unregistered topic")

broker = EventBroker()
