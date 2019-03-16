from ..subscriber import Subscriber

sub = Subscriber()
sub.register("topic1", 2)
sub.register("topic2", 4)
while True:
	sub.notify()
