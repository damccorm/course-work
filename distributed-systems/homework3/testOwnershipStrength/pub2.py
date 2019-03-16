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

	pub.register("topic1", 2)
	while True:
	    pub.publish("topic1", "PUB2")
    	sleep(1)
