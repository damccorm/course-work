# homework3

NOTE: A Zookeeper server must be running for this assignment to work. This may become cluttered and we recommend running clean_up.py before each test to ensure there is no overlap from one run to the next.

Benchmarks when run on Ubuntu virtual machine:
Average time to send/receive one message with:

1 publisher/1 subscriber: 0.0010 s
3 publishers/1 subscriber: 0.0015 s
1 publisher/ 3 subscribers: 0.0012 s
3 publishers/3 subscribers: 0.0014 s

Tests included:

#############################################################################

Test name: testFiltering
Test description: Tests whether the subscriber only receives updates on topics they subscribed to.
To run:
1) Start up 5 terminals in the test's folder and run clean_up.py in one of them.
2) In the first, run "python eb.py" and wait a few seconds
3) In the second, run "python eb.py" and wait a few seconds
4) In the third, run "python eb.py" and wait a few seconds
5) In the fourth, run "python sub.py"
6) In the fifth, run "python pub 127.0.0.1"

Expected output (from sub):

topic1: 0  
topic1: 2  
topic1: 4  
topic1: 6  
topic1: 8

#############################################################################

Test name: testHistory
Test description: Tests whether system accurately maintains history of publishers.
To run:
1) Start up 5 terminals in the test's folder and run clean_up.py in one of them.
2) In the first, run "python eb.py" and wait a few seconds
3) In the second, run "python eb.py" and wait a few seconds
4) In the third, run "python eb.py" and wait a few seconds
5) In the fourth, run "python pub1.py 127.0.0.1"
6) Wait until the publisher finishes plus a few seconds to allow the event_broker to process
7) In the fifth, run "python sub1.py"

Expected output (from sub1):

topic1 HISTORY: test1-2  
topic1 HISTORY: test1-3  
topic2 HISTORY: test2-2  
topic2 HISTORY: test2-3  

NOTE: messages may be out of order, that's ok.

#############################################################################

Test name: testOwnershipStrength
Test description: Tests whether nodes with higher ownership strength are given priority and only their messages are received.
To run:
1) Start up 6 terminals in the test's folder and run clean_up.py in one of them.
2) In the first, run "python eb.py" and wait a few seconds
3) In the second, run "python eb.py" and wait a few seconds
4) In the third, run "python eb.py" and wait a few seconds
5) In the fourth, run "python sub.py"
6) In the fifth, run "python pub1.py 127.0.0.1". This starts up your 1st
   publisher, which has weaker ownership strength.
7) In the sixth, run "python pub2.py 127.0.0.2". This starts up your 2nd
   publisher, which has a stronger ownership strength.

Expected output (from sub):

After you have started pub1, but before starting pub2, you should see:  
topic1: PUB1  
topic1: PUB1  
...  
This should repeat until a few seconds after you start pub2,  
after which you should only see the line:  
topic1: PUB2  
posted approximately every 1 second.  

#############################################################################

Test name: testFailingOwnership
Test description: Tests whether nodes with lower priority take over if the leader dies.
To run:
1) Start up 6 terminals in the test's folder and run clean_up.py in one of them.
2) In the first, run "python eb.py" and wait a few seconds  
3) In the second, run "python eb.py" and wait a few seconds
4) In the third, run "python eb.py" and wait a few seconds
5) In the fourth, run "python sub.py"
6) In the fifth, run "python pub1.py 127.0.0.1". This starts up your 1st
   publisher, which has stronger ownership strength.
7) In the sixth, run "python pub2.py 127.0.0.2". This starts up your 2nd
   publisher, which has a weaker ownership strength.

At this point, check the subscriber output. It should be saying  
topic1: PUB1

8) Now, stop the process in the pub1 terminal (ctrl + C, or simply exit out)

After a few more potential publications of topic1:PUB1, the subscriber should now only see:  
topic1: PUB2

Expected output:  
topic1: PUB1

Repeating UNTIL you kill pub1. THEN:  
topic2: PUB2

This should repeat.
#############################################################################

Test name: testMany
Test description: Tests whether the system works with many publishers and subscribers operating with multiple topics at once.
To run:
1) Start up 9 terminals in the test's folder and run clean_up.py in one of them.
2) In the first, run "python eb.py" and wait a few seconds
3) In the second, run "python eb.py" and wait a few seconds
4) In the third, run "python eb.py" and wait a few seconds
5) In the fourth, run "python pub1.py 127.0.0.1" 
6) In the fifth, run "python pub2.py 127.0.0.2".
7) In the sixth, run "python pub3.py 127.0.0.3".
8) Wait until the publishers register, plus a few seconds to allow the broker to process.
9) To make your life a bit easier, you can minimize the previous 4 terminals. 
10) In the seventh, run "python sub1.py".
11) In the eight, run "python sub2.py".
12) In the ninth, run "python sub3.py".

NOTE: EACH SUBSCRIBER SHOULD HAVE DIFFERENT OUTPUT
Expected Output, sub1 AFTER ALL 3 PUBLISHERS HAVE REGISTERED:  
topic 1: PUB1   
topic 2: PUB2  
...  
(should only print these two lines, over and over. Order doesn't matter)

Expected Output, sub1 AFTER ALL 3 PUBLISHERS HAVE REGISTERED:  
topic 2: PUB2  
topic 3: PUB3  
...  
(should only print these two lines, over and over. Order doesn't matter)

Expected Output, sub1 AFTER ALL 3 PUBLISHERS HAVE REGISTERED:  
topic 1: PUB1  
topic 3: PUB3  
...  
(should only print these two lines, over and over. Order doesn't matter)  

#########################################################################

Test name: testBrokerTolerance
Test description: Tests whether the pub-sub works after a broker dies
1) Start up 5 terminals in the test's folder and run clean_up.py in one of them.
2) In the first, run "python eb.py" and wait a few seconds
3) In the second, run "python eb.py" and wait a few seconds
4) In the third, run "python eb.py" and wait a few seconds
5) In the fourth, run "python sub.py"
6) In the fifth, run "python pub.py 127.0.0.1"
7) Kill whichever eb terminal is receiving updates

Expected output(from sub):  
topic1: "TEST"  
topic1: "TEST"  
topic1: "TEST"  
...

(shouldn't change after eb is killed, though may pause for a little)