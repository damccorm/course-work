# Assignment-6
Makeup Assignment (Due April 21)

This is a make up assignment. It is optional. If you attempt this assignment, the best 5 assignment grades will be used to compute your grade average.

For the assignment, please take a look at the message queue example from the class in the course info repository. Copy the source files to your assignment repository. To build the sender and receiver, execute build.sh.

This assignment has three parts. 

Part I - Undertand the timed API for message queues
================================

You should look at the man page of mq_timedsend and mq_timed receive and understand the api and write example programs with them. There is no required submission for this step


Part II - Using the timed API
=================

Modify the copied source code so that the sender waits for  up to 5 seconds for receiver to consume the messages. If receiver does not arrive in given time, the sender should quit. If the receiver is executed first, then it should also wait for up to 5 seconds. 
You should use mq_timedsend and mq_timedreceive as we discussed in the class. Please look at the slides for the API. 

Part III 
==============
Extend the code. The sender should send an integer and not a character buffer to the receiver. The receiver should check if it is prime or not and send the number to a third process called logger if the number is prime. Note that you will have to create a new queue between receiver and logger process (mqueue_l.cpp). When you are done you will have three programs.

Hint: use something like this
```
mq_send(mq, &i, sizeof(i), priority) . The priority can be same i or some other number.
```

The receiver can receive the integer like this
```
int data=0;
int prio=0
mq_receive(mq,&data,sizeof(data),&prio);
```

Submission Procedure:
----------------------
Create two folders part2 and part3 within the repository. Commit your solutions separately for part 2 and part 3. Make sure to copy
the build.sh and test scripts to both sub folders. You will have to edit the build.sh in part 3 to compile the logger process as well.

Running test script:
------------------------
In order to run the different test scripts please do the following first:

(a) sudo mkdir /dev/mqueue
(b) sudo mount -t mqueue none /dev/mqueue

Then, for the first part of the assignment please run the following three scripts - run_part1_normal.sh, run_part1_send_delay.sh, 
run_part1_recv_delay.sh.

For the second part of the assignment please run the following script - run_part2_normal.sh. 

Grading Criteria
--------------------
1. 10 points for correct formatting and indentation
2. 10 points for proper documentation in the code.
3. 40 points for part I
4. 40 points for part II


