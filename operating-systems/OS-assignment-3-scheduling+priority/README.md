[![Build Status](https://travis-ci.com/CS3281-2016/assignment-3-dannymccormick3.svg?token=pyUEeBLkG7FqiYPhyfxp&branch=master)](https://travis-ci.com/CS3281-2016/assignment-3-dannymccormick3)


*Note* : 
==============
*The  signal handler registration function that I had described in the readme below has one problem. Once a signal for which the handler has been register is received, the signal handling mechanism resets back to default - which for SIGCHLD is SIG_IGN. Now, you can register the handler. However, in that case, it is possible  that you will miss some instances o SIGCHLD*. 

*Precisely, for this reason there is an (alternative) advanced API for signal management is available. It is called sigaction (http://pubs.opengroup.org/onlinepubs/009695399/functions/sigaction.html). I have reimplemented the sighld example with sigaction - https://github.com/CS3281-2016/course-info/tree/master/examples/processManagement/sigchld-sigaction.  You will also notice that in this version I am not using printf or cout or cerr inside a signal handler. Ideally we should limit ourselves to functions that do not use buffered IO in signal handlers. Therefore, I am using the write function, which is the unbuffered version and has been deemed as async signal safe by POSIX standard. You will also note a convoluted function to convert integers to string to avoid using the buffered implementation that are available in the C library. Let me know if you have questions.*


Assignment 3 :Extending the Basic Shell Interpreter: Due Date Friday March 4, 6 AM.
=============

In this assignment you will extend the basic shell interpreter with the following features. The code that you have to implement is restricted to utilites.cpp and app.cpp. Look at @Task markers - as they give you an idea of where and what you have to implement. The features that you will add are the following:

###  Execute command in background. That is, if the input is the following
```
vbash>>command1 &
```

The shell should launch that command in the background and return the control back to the user. You should immediately see the prompt
```
vbash>>
```

Note that if you have background tasks, then you will have to use an asynchronous pattern to wait for the status of children. See example https://github.com/CS3281-2016/course-info/tree/master/examples/processManagement/sigchld. In this example, a SIGCHLD handler is used. if a handler for the SIGCHLD is register, then the kernel sends the parent process SIGCHLD signal upon termination of any child process (also see https://docs.oracle.com/cd/E19455-01/806-4750/signals-7/index.html). Inside the handler we wait with WNOHANG till no other child process whose status is changed can befound. Recall that signals are asynchronous. It is okay to mix the SIGCHLD handler and regular waitpid after a fork and exec like you did in previous assignment.


It is possible to enter a race condition wherein - while 

###  Execute more than one command in parallel. That is, if I give the the input

```
vbash>>command1||command2||command3
```

The shell should launch all three commands in parallel and then wait for all of them to finish. I should be able to mix the background mode as following.
```
vbash>>command1 &||command2||command3
```

Immediately blocks to check if command 2 and command 3 are finished, but does not wait for command 1 to finish. That is there should be an immediate waitpid call for command 2 and command 3. But the other command should be handled by the SIGCHLD handler.

###  Enable Builtins

The shell should support the following built in commands. A built in is a command that changes the properties of the parent shell itself and does not create a new process.

#### cd 

```
vbash>>cd dir_name
```
Note that the dir_name should be a directory that does not contain spaces. 

#### set_memlimit
```
vbash>>set_memlimit 200
```

This will set the RLIMIT_AS on all future child processes as 200 bytes (review the setrlimit API on man page: http://linux.die.net/man/2/getrlimit). 

```C
struct rlimit {
               rlim_t rlim_cur;  /* Soft limit */
               rlim_t rlim_max;  /* Hard limit (ceiling for rlim_cur) */
           };
```

*Note*: There are soft and hard resources limits (). These resource limits are set using the struct relimit (see above). to set the limit you should set both rlim_cur (soft) and rlim_max (hard) to the value provided to you in the command. 


#### set_policy
```
vbash>>set_policy fifo
```
This will set the scheduling policy to SCHED_FIFO for all children. And set the priority by default to 0. Or,
See the following example for reference: https://github.com/CS3281-2016/course-info/blob/master/examples/scheduling/cpu-loader.cpp
and the sched_set param and sched_set scheduler API for more information.
```
vbash>>set_policy rr
```
This will set the scheduling policy to SCHED_RR for all children. And set the priority by default to 0. Or,
```
vbash>>set_policy other
```
This will set the scheduling policy to SCHED_OTHER for all children. This will set the niceness value to 0. Or,


#### set_priority 
```
vbash>>set_priority 99
```
If the current policy for children is FIFO or RR, the value should be between 0 and 99. Otherwise, the value should be between -20 and +19, the niceness values.

