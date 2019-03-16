import zmq
import json
import time
import threading
from datetime import datetime
import uuid


class Publisher:

    def __init__(self, ip):
        self.context = zmq.Context()
        self.pub_socket = self.context.socket(zmq.PUB)
        self.pub_socket.connect("tcp://127.0.0.1:5555")

        # set a random ID for self
        self.pId = ip

        self.started_heartbeat = False
        self.topics = set()

        time.sleep(3)
        
    def register(self, topic, ownership_strength=0, history=0):
        msg = {"pId": self.pId,
               "topic": topic,
               "ownership_strength": ownership_strength,
               "history": history}
        formatted_message = json.dumps(msg, separators=(",", ":"))
        self.pub_socket.send_string("%s %s" % ("registerpub", formatted_message))
        time.sleep(2)
        print "registered", formatted_message
        self.topics.add(topic)

        if not self.started_heartbeat:
            timeout_thread = threading.Thread(target=self.heartbeat)
            timeout_thread.daemon = True
            timeout_thread.start()
            self.started_heartbeat = True

    def heartbeat(self):
        while True:
            time.sleep(5)
            for topic in self.topics:
                msg = {"pId": self.pId,
                       "val": "",
                       "heartbeat": True}
                self.pub_socket.send_string("%s %s" % (topic, json.dumps(msg, separators=(",", ":"))))
                print "heartbeating for topic:", topic

    def publish(self, topic, val):
        cur_date_time = str(datetime.now())
        cur_date_time = cur_date_time.replace(" ", "T")
        msg = {"pId": self.pId,
               "val": val,
               "heartbeat": False,
               "datetime": cur_date_time}
        self.pub_socket.send_string("%s %s" % (topic, json.dumps(msg, separators=(",", ":"))))
        print "publishing to topic", topic, "message:", val
