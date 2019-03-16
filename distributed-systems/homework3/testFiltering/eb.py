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

	eb = EventBroker()
	eb.start()