from ..publisher import Publisher

pub = Publisher()
pub.register("topic1", 0, 3)
pub.register("topic2", 0, 2)
pub.publish("topic1", "test1-1")
pub.publish("topic1", "test1-2")
pub.publish("topic1", "test1-3")
pub.publish("topic2", "test2-1")
pub.publish("topic2", "test2-2")
pub.publish("topic2", "test2-3")
