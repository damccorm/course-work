import os
import sys
from time import sleep


if __name__ == '__main__':
	if __package__ is None:
		import sys
		from os import path
		sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
		from publisher import Publisher
	else:
		from ..publisher import Publisher

	this_ip = sys.argv[1]

	pub = Publisher(this_ip)

	pub.register("topic1", 0, 3)
	pub.register("topic2", 0, 2)
	pub.publish("topic1", "test1-1")
	pub.publish("topic1", "test1-2")
	pub.publish("topic1", "test1-3")
	pub.publish("topic2", "test2-1")
	pub.publish("topic2", "test2-2")
	pub.publish("topic2", "test2-3")
