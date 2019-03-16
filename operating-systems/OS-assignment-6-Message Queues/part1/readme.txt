
= Due Date 10/29 =

Please take a look at the message queue example from the class. To build the sender and receiver, execute build.sh.
This assignment has two parts. Part II does not need to use the timed version of API. 

Part 1 - The sender should wait only up to 5 seconds for receiver to arrive. If receiver does not arrive in given time, the sender should quit.
If the receiver is executed first, then it should only wait for up to 5 seconds. 
You should use mq_timedsend and mq_timedreceive as we discussed in the class. Please look at the slides for the API. You can search the web 
also for solution.

Part II - Extend the code. The sender should send an integer and not a character buffer to the receiver. The receiver should check if it is prime or not
and send the number to a third process called logger if the number is prime. Note that you will have to create a new queue between receiver and
logger process (mqueue_l.cpp). When you are done you will have three processes.

Hint: use something like this
mq_send(mq, &i, sizeof(i), priority) . The priority can be same i or some other number.

The receiver can receive the integer like this
int data=0;
int prio=0
mq_receive(mq,&data,sizeof(data),&prio);

Submissione Procedure:
Create two folders part1 and part2 within the assignment 2 folder. Commit your solutions separately for part 1 and part 2. Make sure to copy
the build.sh to both sub folders. You will have to edit the build.sh in part 2 to compile the logger process as well.

Running test script:
In order to run the different test scripts please do the following first:

(a) sudo mkdir /dev/mqueue
(b) sudo mount -t mqueue none /dev/mqueue

Then, for the first part of the assignment please run the following three scripts - run_part1_normal.sh, run_part1_send_delay.sh, 
run_part1_recv_delay.sh.

For the second part of the assignment please run the following script - run_part2_normal.sh. 
