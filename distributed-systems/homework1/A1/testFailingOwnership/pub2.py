from ..publisher import Publisher
from time import sleep

pub = Publisher()

pub.register("topic1", 1)
while True:
    pub.publish("topic1", "PUB2")
    sleep(1)