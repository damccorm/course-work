from ..publisher import Publisher
from time import sleep

pub = Publisher()
pub.register("topic1", 3)
pub.register("topic2", 2)
pub.register("topic3", 1)

while True:
    pub.publish("topic1", "PUB1")
    pub.publish("topic2", "PUB1")
    pub.publish("topic3", "PUB1")
    sleep(1)
