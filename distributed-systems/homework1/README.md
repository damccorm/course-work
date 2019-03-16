# homework1

To run tests execute the following from this directory:
python -m A1.[testname].[filename without filetype]

For example, to run pub1 from the testHistory test suite, run:
python -m A1.testHistory.pub1

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
1) Start up 3 terminals
2) In the first, run "python -m A1.testFiltering.eb" and wait a few seconds
3) In the second, run "python -m A1.testFiltering.sub"
4) In the third, run "python -m A1.testFiltering.pub"

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
1) Start up 3 terminals
2) In the first, run "python -m A1.testHistory.eb" and wait a few seconds
3) In the second, run "python -m A1.testHistory.pub1"
4) Wait until the publisher finishes plus a few seconds to allow the event_broker to process
5) In the third, run "python -m A1.testHistory.sub1"

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
1) Start up 4 terminals
2) In the first, run "python -m A1.testOwnershipStrength.eb" and wait a few seconds
3) In the second, run "python -m A1.testOwnershipStrength.sub"
4) In the third, run "python -m A1.testOwnershipStrength.pub1". This starts up your 1st
   publisher, which has weaker ownership strength.
5) In the fourth, run "python -m A1.testOwnershipStrength.pub2". This starts up your 2nd
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
1) Start up 4 terminals
2) In the first, run "python -m A1.testOwnership.eb" and wait a few seconds
3) In the second, run "python -m A1.testOwnership.sub"
4) In the third, run "python -m A1.testOwnership.pub1". This starts up your 1st
   publisher, which has a stronger ownership strength.
5) In the fourth, run "python -m A1.testOwnership.pub2". This starts up your 2nd
   publisher, which has a weaker ownership strength.

At this point, check the subscriber output. It should be saying
topic1: PUB1

6) Now, stop the process in the pub1 terminal (ctrl + C, or simply exit out)

After a few more potential publications of topic1:PUB1, the subscriber should now only see:
topic1: PUB2

Expected output:
topic1: PUB1

Repeating UNTIL you kill pub1. THEN:

topic2: PUB2

This should repeat.
#############################################################################

Test name: testHeartbeat
Test description: Tests whether publisher continues to be recognized even if they don't publish for a while.
To run:
1) Start up 3 terminals
2) In the first, run "python -m A1.testHeartbeat.eb" and wait a few seconds
3) In the second, run "python -m A1.testHeartbeat.sub"
4) In the third, run "python -m A1.testHeartbeat.pub"

Expected output:
Subscriber should initially receive
topic1: initial

Then 20 seconds should pass and the subscriber should receive
topic1: final

#############################################################################

Test name: testMany
Test description: Tests whether the system works with many publishers and subscribers operating with multiple topics at once.
To run:
1) Start up 7 terminals (I'm so sorry)
2) In the first, run "python -m A1.testMany.eb" and wait a few seconds
3) In the second, run "python -m A1.testMany.pub1"
4) In the third, run "python -m A1.testMany.pub2"
5) In the fourth, run "python -m A1.testMany.pub3"
6) Wait until the publishers register, plus a few seconds to allow the broker to process.
7) To make your life a bit easier, you can minimize the previous 4 terminals.
8) In the 5th terminal, run "python -m A1.testMany.sub1"
9) In the 6th terminal, run "python -m A1.testMany.sub2"
10) In the 7th terminal, run "python -m A1.testMany.sub3"

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

