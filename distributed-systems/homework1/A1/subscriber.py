import zmq
import json
import time
import datetime
import uuid


class Subscriber:

    def __init__(self):
        # connect to socket as a subscriber
        self.context = zmq.Context()
        self.sub_socket = self.context.socket(zmq.SUB)
        self.sub_socket.connect("tcp://127.0.0.1:5556")

        self.pub_socket = self.context.socket(zmq.PUB)
        self.pub_socket.connect("tcp://127.0.0.1:5555")
        time.sleep(3)

        # set a random ID for self
        self.sId = uuid.uuid4()

    def register(self, topic, history=0):
        if isinstance(topic, bytes):
            topic = topic.decode('ascii')
        self.sub_socket.setsockopt_string(zmq.SUBSCRIBE, topic)
        if history > 0:
            msg = {"topic": topic,
                   "sId": self.sId,
                   "history": history}
            self.pub_socket.send_string("%s %s" % ("registersub", json.dumps(msg, separators=(",", ":"))))

    def notify(self):
        string = self.sub_socket.recv()
        topic, mjson = string.split()
        msg = json.loads(mjson)
        if msg["sender_id"] is None:
            # this is a standard message meant for me
            print("%s: %s" % (topic, msg["contents"]))
            sent_date_time_string = msg["datetime"]
            sent_date_time = datetime.datetime.strptime(sent_date_time_string, "%Y-%m-%dT%H:%M:%S.%f")
            time_to_send = datetime.datetime.now() - sent_date_time
            print "Time to send:", time_to_send.total_seconds(), "seconds"
        elif msg["sender_id"] == self.sId:
            # this is a historical message meant for me
            print("%s HISTORY: %s" % (topic, msg["contents"]))
