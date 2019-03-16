"""
Authors: Daniel McCormick and Andrew Ragan
File Overview: This file works as a middle broker for an anonymous pub-sub connection.
    It can stand alone as an individual broker, but it is meant to be used in a ring
    of brokers.
"""

import zmq
import time
import threading
import sys
import json
from uhashring import HashRing


class Ring:
    def __init__(self, ip_list, own_ip):
        self.ip_list = ip_list
        self.hashRing = HashRing(ip_list)
        self.own_ip = own_ip

    def add_ip_to_hash_ring(self, ip):
        self.hashRing.add_node(ip)
        self.ip_list.append(ip)

    def remove_ip_from_hash_ring(self, ip):
        self.hashRing.remove_node(ip)
        self.ip_list.remove(ip)
        
    def get_correct_server_ip(self, topic):
        return self.hashRing.get_node(topic)

    def broadcast_to_all_nodes(self, topic, message_string):
        context = zmq.Context()
        for ip in self.ip_list:
            if ip != self.own_ip:
                temp_pub_socket = context.socket(zmq.PUB)
                temp_pub_socket.connect("tcp://" + ip + ":5555")
                temp_pub_socket.send_string("%s %s" % (topic, message_string))
                temp_pub_socket.close()


class Topic:
    def __init__(self, topic, leader_id, strength):
        self.topic = topic
        self.cur_leader_id = leader_id
        self.ownership_strength_map = {leader_id: strength}
        self.dead_leader = False
        self.change_leader = False

        self.start_timeout_routine()

    def add_publisher(self, leader_id, strength):
        # Adds publisher for this topic.
        self.ownership_strength_map[leader_id] = strength
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
                return True
        return False

    def remove_publisher(self, publisher_id):
        # Removes dead publisher from topic.
        del self.ownership_strength_map[publisher_id]
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

    def __init__(self, own_ip, broker_ip=None):
        self.own_ip = own_ip

        self.only_node = False
        if broker_ip is None:
            self.only_node = True

        self.context = zmq.Context()
        self.sub_socket = self.context.socket(zmq.SUB)
        self.sub_socket.bind("tcp://" + own_ip + ":5555")
        self.sub_socket.setsockopt_string(zmq.SUBSCRIBE, "register_pub".decode('ascii'))
        self.sub_socket.setsockopt_string(zmq.SUBSCRIBE, "register_sub".decode('ascii'))
        self.sub_socket.setsockopt_string(zmq.SUBSCRIBE, "add_node".decode('ascii'))
        self.sub_socket.setsockopt_string(zmq.SUBSCRIBE, "node_failed".decode('ascii'))
        self.sub_socket.setsockopt_string(zmq.SUBSCRIBE, "join_ring".decode('ascii'))

        self.pub_socket = self.context.socket(zmq.PUB)
        self.pub_socket.bind("tcp://" + own_ip + ":5556")
        time.sleep(3)

        self.ip_list = [own_ip]
        self.hashRing = None
        if self.only_node:
            self.hashRing = Ring([self.own_ip], self.own_ip)
        else:
            self.build_hash_ring(broker_ip)

        self.topic_map = {}

        self.history_map = {}

        # Heartbeat so that anyone trying to publish to this can watch for failure
        timeout_thread = threading.Thread(target=self.heartbeat)
        timeout_thread.daemon = True
        timeout_thread.start()

        while True:
            self.listen()

    def heartbeat(self):
        while True:
            time.sleep(5)
            for topic in self.topic_map:
                msg = {"ip_list": self.hashRing.ip_list, "contents": ""}
                self.pub_socket.send_string("%s %s" % ("HEARTBEAT", json.dumps(msg, separators=(",", ":"))))
                print("Sending heartbeat: " + str(msg))

    def build_hash_ring(self, broker_ip):
        # Builds the initial hash ring
        temp_pub_socket = self.context.socket(zmq.PUB)
        temp_pub_socket.connect("tcp://" + broker_ip + ":5555")
        temp_sub_socket = self.context.socket(zmq.SUB)
        temp_sub_socket.connect("tcp://" + broker_ip + ":5556")
        sub_filter = "join_ring_response" + self.own_ip
        temp_sub_socket.setsockopt_string(zmq.SUBSCRIBE, sub_filter.decode('ascii'))
        time.sleep(3)

        # Get the ips so that we can add them to the ring
        msg = {"ip": self.own_ip}
        temp_pub_socket.send_string("%s %s" % ("join_ring", json.dumps(msg, separators=(",", ":"))))
        temp_pub_socket.close()
        print "Trying to join ring at ip", broker_ip
        response_code, msg_string = temp_sub_socket.recv().split()
        print "Successfully joined"
        temp_sub_socket.close()
        msg = json.loads(msg_string)
        self.ip_list = msg["ips"]
        self.ip_list.append(self.own_ip)
        self.hashRing = Ring(self.ip_list, self.own_ip)

    def respond_to_node_failure(self, ip_address):
        self.hashRing.remove_ip_from_hash_ring(ip_address)
        msg = {"ip": ip_address}
        self.hashRing.broadcast_to_all_nodes("node_failed", json.dumps(msg, separators=(",", ":")))

    def register_pub(self, received_msg):
        topic = received_msg["topic"]
        correct_ip = self.hashRing.get_correct_server_ip(topic)
        msg = {"topic": topic, "ip": correct_ip}
        self.pub_socket.send_string("%s %s" % ("register_pub_response", json.dumps(msg, separators=(",", ":"))))
        if correct_ip == self.own_ip:
            ownership_strength = received_msg["ownership_strength"]
            sender_id = received_msg["ip"]
            if topic in self.topic_map:
                self.topic_map[topic].add_publisher(sender_id, ownership_strength)
            else:
                self.topic_map[topic] = Topic(topic, sender_id, ownership_strength)
                self.sub_socket.setsockopt_string(zmq.SUBSCRIBE, topic.decode("ascii"))

    def register_sub(self, msg):
        topic = msg["topic"]
        correct_ip = self.hashRing.get_correct_server_ip(topic)
        history = None
        if topic in self.history_map:
            history = self.history_map[topic]
        response = {"topic": topic, "ip": correct_ip, "contents": "", "history": history}
        print("Sending response: " + str(response))
        self.pub_socket.send_string("%s %s" % ("register_sub_response", json.dumps(response, separators=(",", ":"))))

    def register_broker(self, msg):
        # Reply with all the ips already in existence
        new_ip = msg["ip"]
        response = {"ips": self.hashRing.ip_list}
        self.pub_socket.send_string("%s %s" % ("join_ring_response" + new_ip, json.dumps(response, separators=(",", ":"))))
        # Tell other nodes to add this broker
        self.hashRing.add_ip_to_hash_ring(new_ip)
        self.hashRing.broadcast_to_all_nodes("add_node", json.dumps(msg, separators=(",", ":")))

    def relay_message(self, topic, msg):
        correct_server_ip = self.hashRing.get_correct_server_ip(topic)
        sender_id = msg["ip"]
        message_contents = msg["val"]
        is_heartbeat = msg["heartbeat"]
        if self.topic_map[topic].receive_message(sender_id, message_contents, is_heartbeat):
            sent_date_time = msg["datetime"]
            history = msg["history"]
            # Update history so it includes this message
            history.append(message_contents)
            del history[0]
            new_msg = {"contents": message_contents, "history": history, "datetime": sent_date_time, "new_ip": None}
            self.history_map[topic] = history
            self.pub_socket.send_string("%s %s" % (topic, json.dumps(new_msg, separators=(",", ":"))))
        if correct_server_ip != self.own_ip:
            new_msg = {"contents": "TOPIC_MOVED", "new_ip": correct_server_ip}
            self.pub_socket.send_string("%s %s" % (topic, json.dumps(new_msg, separators=(",", ":"))))
            del self.topic_map[topic]

    def listen(self):
        response_code, msg_string = self.sub_socket.recv().split()
        print "Received message with code", response_code, "and message", msg_string
        msg = json.loads(msg_string)
        if response_code == "register_pub":
            if msg["previous_ip"] is not None and msg["previous_ip"] in self.hashRing.ip_list:
                # That node must have died
                self.respond_to_node_failure(msg["previous_ip"])
            self.register_pub(msg)
        elif response_code == "register_sub":
            self.register_sub(msg)
        elif response_code == "join_ring":
            self.register_broker(msg)
        elif response_code == "add_node":
            self.hashRing.add_ip_to_hash_ring(msg["ip"])
        elif response_code == "node_failed":
            self.hashRing.remove_ip_from_hash_ring(msg["ip"])
        elif response_code in self.topic_map:
            self.relay_message(response_code, msg)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "ERROR, need to specify the ip of this node"
    else:
        own_ip_address = sys.argv[1]
        broker_ip = None
        if len(sys.argv) > 2:
            broker_ip = sys.argv[2]
        broke = EventBroker(own_ip_address, broker_ip)
