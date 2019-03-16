from ..publisher import Publisher
from time import sleep

pub = Publisher()
pub.register("topic1", 2)
pub.register("topic2", 1)
pub.register("topic3", 3)

while True:
    pub.publish("topic1", "PUB3")
    pub.publish("topic2", "PUB3")
    pub.publish("topic3", "PUB3")
    sleep(1)

