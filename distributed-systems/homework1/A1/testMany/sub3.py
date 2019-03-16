from ..subscriber import Subscriber

sub = Subscriber()
sub.register("topic3")
sub.register("topic1")
while True:
	sub.notify()
