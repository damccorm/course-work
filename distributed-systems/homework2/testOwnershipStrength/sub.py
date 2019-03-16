import os
import sys
from time import sleep


if __name__ == '__main__':
	if __package__ is None:
		import sys
		from os import path
		sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
		from subscriber import Subscriber
	else:
		from ..subscriber import Subscriber

	existing_broker_ip = sys.argv[1]

	sub = Subscriber(existing_broker_ip)

	sub.register("topic1")
	while True:
    	        sub.notify()
