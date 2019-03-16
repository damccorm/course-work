import os
import sys

if __name__ == '__main__':
	if __package__ is None:
		import sys
		from os import path
		sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
		from event_broker import EventBroker
	else:
		from ..event_broker import EventBroker

	this_broker_ip = sys.argv[1]
	existing_broker_ip = None
	if len(sys.argv) > 2:
		existing_broker_ip = sys.argv[2]

	eb = EventBroker(this_broker_ip, existing_broker_ip)
	eb.start()