from ..publisher import Publisher
import time

pub = Publisher()
pub.register("topic1", 0, 3)
pub.publish("topic1","initial")
for i in range(20):
	wait_time = 20-i
	print "Waiting for", wait_time, "more seconds"
	time.sleep(1)
pub.publish("topic1", "final")
time.sleep(5)
