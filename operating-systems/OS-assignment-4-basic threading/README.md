# assignment-4 : Building an Object oriented wrapper for threads.
=====================================

The objective of this assignment is to demonstrate an understanding of concurrency and threading APIs. Concurrency refers to the ability to execute multiple computations on a computer simultaneously. When applied to a single problem, concurrency often enables the system to solve the problem faster. Several criteria have to be considered when designing a library that can help break up a problem into smaller problems that can be solved concurrently. Some of the criteria are:

1. Protecting the integrity of data structures across concurrent tasks. This often requires the concurrent tasks to run in separate address spaces, i.e., run as different processes.
2. Preventing race conditions.
3. Preventing deadlocks and livelocks.
4. Providing end of life synchronization.
5. Providing the ability to manage the state of a concurrent task, i.e., start a new task or terminating an existing task.

To demonstrate these concepts, you have to design the interface and provide the implementation of an abstract base class called 'Task'. This class must provide a pure virtual function called svc that will be overridden in derived classes. 

The class must provide interfaces to do the following:

1. Construct a new task. It should be possible to create the new concurrent task as joinable or detached. Recall that joinable threads imply that we can use pthread_join to check their status. Detached threads cannot be joined.
2. Activate the task. The activation function will throw an exception if the task creation fails.
3. Terminate the task.
4. Wait for the task to finish and throw an exception upon failure.
5. Show the execution and correct compilation of the program provided to you (example.cpp.)

*Note:* Please complete the implementation in the files: task.h, task.cpp. Partial implementation of the activate function for tasks within the same address space (i.e. creating threads) is already provided. This requires a static method,  which is used as a thread entry function. We pass the this pointer as the argument to pthread create. The this argument is later resolved to the class object within the thread entry function. 

*Useful man page:* man 7 pthreads

*Bonus Question*: Pay attention to the  private copy constructor and private assignment operators in the task interface (look in task.h). There is a bonus question regarding those.

*Grading Crieria*:
=================

1. *25 points:* Interface definition - document each method 
2. *40 points:* Interface implementation
3. *25 points:* Correct Execution of  Example program
4.  *10 points:* Correct and insightful programming style and indentation.
5.   *10 points Bonus Question:* Why do we need to add a private copy constructor and assignment operator to this class interface?

BONUS: We need a private copy constructor and assignment operator because if we didn't have it and the compiler created it itself, the user would have the ability to copy/assign the data from one task object into another object. This object would then have the same taskID and thus access to the same thread, so any changes made by that task object would affect the thread in the original task object. This is undesirable because it could lead to race conditions or other thread safety issues. By declaring a private copy constructor and assignment operator, we ensure that this can't happen.
