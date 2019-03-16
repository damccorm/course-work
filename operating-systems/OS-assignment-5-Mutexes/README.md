# assignment-5 : Synchronization among Multiple Reader-Writers
=====================================
Due: Date - April 15th 2016 at 6 AM

The goal of this programming assignment is to implement a multiple readers-multiple writers program on Linux. We do not worry about priority to readers or writers. Anyone who gets a chance will proceed. This assignment will help you better understand the principle of concurrency, mutual exclusion and the use of condition variables.

*Note*: This assignment builds upon the assignment 4. The folder library contains the solution for the task class you completed in the last assignment.

Note 2: The container class implementation has been provided. But it is just a wrapper. You goal is to implement the client.cpp svc method and server.cpp svc method. Focus on the required synchronization steps. Look in main.cpp for the different entities that have been created.

Program Details
==============================
In this assignment we are going to implement multiple clients and multiple servers, all of them sharing two instances of Container Class: request container and reply container. A Container class wraps a map which contains items keyed by an integer ID (we are going to use the thread ID as the key). The clients and servers are written a derived class of the Task Class you build during the last assignment. 


Assume that the server tasks have the ability to compute factorials of a given number. These threads use the traditional recursive approach to find factorial (the factorial functions has already been implemented in the server.cpp). Moreover, assume that server threads take their own time to compute this value (essentially put a random sleep value between 1 and 5 sec) in the svc methor.


Each client thread operates in a “forever” loop implemented using a while true. It “thinks” for a while (use the sleep function call  combined with a random number between 0-5). Thereafter it should generated a random number that it wants to compute the factorial for. Then it sends that number along with its id to the request container. For that it  grabs the lock associated with the Request container and waits for a condition variable on the “Request Container” to make sure the Container is not full - checked using the condition isFull. If container is not full, it inserts an entry - using the addEntry function <thread ID, requested number> in it. It then sends a broadcast to all servers that there is a new request. It then proceeds to wait for a reply (see description below). The number is generated randomly between 1 and 10. And the threadID is obtained using the helper method getthreadid() or getLinuxtid in the Parent Task Class.

Each server thread also operates in a “forever” loop. They also try to grab the lock and wait on a condition variable to check if some request has showed up in the Request Container. If some request has showed up, that server thread will remove the item, compute the factorial, and insert the reply as a tuple <client thread ID, requested number, answer> into the Reply Container. Note that inserting into the Reply Container will require another set of lock and condition variables in much the same way that one will need for the Request Container. As shown later the signaling operation here must be a broadcast since the server thread doesn’t know which requesting thread from the client it is supposed to talk to.

In the meantime, client threads are waiting for replies. So they are waiting on a condition variable for the Reply Queue (to see if something is available as a reply). Because the server had broadcast the reply, all waiting client threads will wake up all at once. However, the incoming reply may not be for the same client thread that made the request originally ( this can be checked using the checkIfEntryPresent function). If the reply for the client is not there, it will not read the reply but rather go back to waiting.  Only the eligible thread will remove the reply from the container by using the eraseEntry function and print the answer. Once done processing a reply, the thread goes back to its thinking process to make a new request on the server.

Note: You will need to add one lock and one condition variable per Container. The same condition variable can be used with the two different conditions (isEmpty) and (isFull). Note that the isEmpty and isFull conditions can be only be checked if you have the lock on the Container.


Real-world Illustration
==========================
This assignment represents an almost real-life scenario. Client threads are like web users. Server threads are the ones that serve incoming client requests. In real-world, clients are distributed across the network. On the server-side, usually there will be one master thread that reads the incoming data on the network interface card, and hand off the request to one of the worker threads. Worker threads subsequently send a reply to the client over the network. 

Files In the Asssignment
=====

1. container.h  -- this is the header file of the container. In the main.cpp two instances of the container are created. one for request and another for reply. In this assignment, you will edit container.h to add appropriate member variables for condition variables and mutex.
2. container.cpp -- source code for container functions. Implement empty shells. you can add any other function, you deem is required.
3. main.cpp - this is the master function that activates all servers and clients. It instantiates the containers. And waits on them. you should not have to add any code to this file.
4. server.cpp server.h - this is a task implemented using assignment 3 library. The server takes the reference of the two container instances : request and reply. You should see the main function. It shows how these references are being passed. You have to implement the svc method as described in the text above.
5. client.cpp client.h - this is the client task. it also requres the reference to the two instances - request and reply. You have to implement the svc method as described in the text above.
6. library/  - the library folder contains the task header and source file from previous assignment. It contains the full solution. you dont need to change anything in the files in this folder.

Running the complete program
=============================

If built correctly, the output might look like the following. You do not have to match it exactly.

```
vagrant@vagrant:~/cs281/assignment-5-cs281-test$ ./taskexample 
server id 21615 3!=6 sending to client 21617
Client Id 21617 result 6
server id 21616 6!=720 sending to client 21618
server id 21616 2!=2 sending to client 21617
Client Id 21617 result 2
Client Id 21618 result 720
server id 21614 7!=5040 sending to client 21619
Client Id 21619 result 5040
server id 21614 0!=1 sending to client 21618
Client Id 21618 result 1
server id 21615 8!=40320 sending to client 21617
Client Id 21617 result 40320
server id 21614 0!=1 sending to client 21618
Client Id 21618 result 1
server id 21616 2!=2 sending to client 21619
Client Id 21619 result 2
server id 21615 9!=362880 sending to client 21619
Client Id 21619 result 362880
server id 21616 8!=40320 sending to client 21618
Client Id 21618 result 40320
server id 21614 3!=6 sending to client 21617
Client Id 21617 result 6
server id 21615 2!=2 sending to client 21619
Client Id 21619 result 2
server id 21614 1!=1 sending to client 21617
Client Id 21617 result 1
server id 21616 7!=5040 sending to client 21618
Client Id 21618 result 5040
server id 21615 0!=1 sending to client 21618
Client Id 21618 result 1
server id 21614 1!=1 sending to client 21617
server id 21614 4!=24 sending to client 21619
Client Id 21617 result 1
Client Id 21619 result 24
server id 21614 0!=1 sending to client 21618
Client Id 21618 result 1
server id 21614 5!=120 sending to client 21619
Client Id 21619 result 120
server id 21616 7!=5040 sending to client 21618
Client Id 21618 result 5040
server id 21614 6!=720 sending to client 21618
Client Id 21618 result 720
^C
vagrant@vagrant:~/cs281/assignment-5-cs281-test$ 
```

