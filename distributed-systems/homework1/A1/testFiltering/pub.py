from ..publisher import Publisher

pub = Publisher()

pub.register("topic1")
pub.register("topic2")
for i in range(10):
    t = i % 2
    pub.publish("topic" + str(t + 1), i)
