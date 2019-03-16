from ..subscriber import Subscriber

sub = Subscriber()
sub.register("topic2")
sub.register("topic3")
while True:
	sub.notify()
