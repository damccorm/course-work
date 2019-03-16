from ..publisher import Publisher
from time import sleep

pub = Publisher()
pub.register("topic1", 1)
pub.register("topic2", 3)
pub.register("topic3", 2)

while True:
    pub.publish("topic1", "PUB2")
    pub.publish("topic2", "PUB2")
    pub.publish("topic3", "PUB2")
    sleep(1)
