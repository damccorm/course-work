#ifndef CS281_TASK_HPP
#define CS281_TASK_HPP
#include <pthread.h>
#include <sys/wait.h>
#include <exception>
#include <unistd.h>
#include <thread>
#include <iostream>
#include <string>
// Add more headers as required

namespace CS281
{

class Task
{

private:
  // Add data members as required
  pthread_t taskID;
  bool detachedState;
  /// This is a function that you can pass to pthread_create.
  /// It should turn around and invoke svc on the object
  /// that created the thread.
  static void *thread_entry_func (void *);

public:
  // constructor
  Task (bool detachedState);
  // dtor
  virtual ~Task (void);
  // Activates the task i.e. creates the task
  // the new thread should be in detached state if detached is true
  void activate ();
  // Waits the task
  int wait ();
  // Kills the task.
  void terminate ();
  virtual void svc (void) = 0;
  // print log.
  void printlog (const std::string &data);
  // pthread id
  long getthreadid ();
  // get linux tid - this is static because even the main thread can get its
  // linux tid.
  static long getlinuxtid ();

private:
  Task (const Task &){};
  Task &operator=(const Task &){};
};
};

#define LOG_TASK(fmt, ...)                                                    \
  {                                                                           \
    char buffer[256];                                                         \
    snprintf (buffer, 256, "%ld:%ld:" fmt, CS281::Task::getlinuxtid (),       \
              this->getthreadid (), __VA_ARGS__);                             \
    write (STDOUT_FILENO, buffer, strlen (buffer));                           \
  }

#define LOG_OTHER(fmt, ...)                                                   \
  {                                                                           \
    char buffer[256];                                                         \
    snprintf (buffer, 256, "%ld:" fmt, CS281::Task::getlinuxtid (),           \
              __VA_ARGS__);                                                   \
    write (STDOUT_FILENO, buffer, strlen (buffer));                           \
  }

#endif
