from ..publisher import Publisher
from time import sleep

pub = Publisher()

pub.register("topic1", 2)
while True:
    pub.publish("topic1", "PUB1")
    sleep(1)
