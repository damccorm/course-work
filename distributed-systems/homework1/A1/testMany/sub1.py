from ..subscriber import Subscriber

sub = Subscriber()
sub.register("topic1")
sub.register("topic2")
while True:
	sub.notify()
