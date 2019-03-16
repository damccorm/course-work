#include <task.h>
#include <system_error>
#include <iostream>
#include <string.h>
#include <unistd.h>
#include <sys/syscall.h>
#include <stdio.h>
namespace CS281 {
//NOTE: Bonus is at bottom of README file

// Constructor, creates a task object with a detached state of detachedState and
// a taskID of 0
Task::Task(bool detachedState) : detachedState(detachedState), taskID(0) {}

// Returns the id of this object
long Task::getthreadid() { return taskID; }

// Destructor - takes care of all the data, delegates work to terminate
Task::~Task(void) {
  // make sure that the task is terminated here.
  try {
    terminate();
  } catch (...) {
  }
}

// Invokes svc on the object that created the thread
void *Task::thread_entry_func(void *handle) {
  // this code is complete
  if (handle == nullptr)
    return nullptr;
  try {
    auto obj = reinterpret_cast<Task *>(handle);
    obj->svc();
  } catch (std::system_error &ex) {
    const char *error = ex.what();
    LOG_OTHER("System Error: %s\n", error);
  } catch (std::exception &ex) {
    const char *error = ex.what();
    LOG_OTHER("Exception: %s\n", error);
  } catch (...) {
    LOG_OTHER("%s\n", "unknown exception");
  }
  return nullptr;
}

// Returns the id of the system
long Task::getlinuxtid() { return syscall(SYS_gettid); }

// Creates a new thread and activates the task. Will be detached or joined
// depending on detachedState
void Task::activate() {
  // initialize pthread_attr

  // ensure that the thread activation fails if the thread is already active.
  if (taskID != 0) {
    throw std::runtime_error("Thread is already active, cannot activate again");
  }

  pthread_attr_t attr;
  if (pthread_attr_init(&attr) != 0)
    throw std::system_error(errno, std::system_category(), "pthread_attr_init");
  try {
    // use pthread_attr_setdetachstate to make the thread
    // detachable if detached (passed during construction) is true
    // create the thread

    if (detachedState) {
      pthread_attr_setdetachstate(&attr, PTHREAD_CREATE_DETACHED);
    } else {
      pthread_attr_setdetachstate(&attr, PTHREAD_CREATE_JOINABLE);
    }

    if (pthread_create(&taskID, &attr, thread_entry_func, (void *)(this))) {
      throw std::runtime_error("could not create thread");
    }
  } catch (...) {
    pthread_attr_destroy(&attr);
    throw;
  }

  pthread_attr_destroy(&attr);
}

// Waits for task to finish. Throws exception if it fails
int Task::wait() {
  // wait on the thread // remember to use join here.
  // do not wait if thread was created with detached option
  // task activation should be allowed again if the wait finished successfully.
  if (detachedState) {
    return -1;
  }
  if (!taskID) {
    return -1;
  }
  int returned;
  returned = pthread_join(taskID, NULL);
  terminate();
  if (returned != 0) {
    throw std::runtime_error("Thread failed");
  }
}

// Terminates the task by killing the thread
void Task::terminate() {
  // kill the thread
  if (taskID == 0) {
    std::cout << getlinuxtid() << ":Exception: thread cannot be terminated\n";
  } else {
    pthread_cancel(taskID);
    taskID = 0;
  }
}
}
