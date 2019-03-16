#include <task.h>
#include <system_error>
#include <iostream>
#include <string.h>
#include <unistd.h>
#include <sys/syscall.h>
#include <stdio.h>

namespace CS281
{

Task::Task (bool detachedState) : detachedState (detachedState), taskID (0) {}
long
Task::getthreadid ()
{
  return taskID;
}
Task::~Task (void)
{
  // make sure that the task is terminated here.
  try
    {
      terminate ();
      if (!detachedState)
        wait ();
    }
  catch (std::exception &e)
    {

      const char *error = e.what ();
      LOG_OTHER ("Exception: %s\n", error);
    }
}

void *
Task::thread_entry_func (void *handle)
{
  // this code is complete
  if (handle == nullptr)
    return nullptr;
  try
    {
      auto obj = reinterpret_cast<Task *> (handle);
      obj->svc ();
    }
  catch (std::system_error &ex)
    {
      const char *error = ex.what ();
      LOG_OTHER ("System Error: %s\n", error);
    }
  catch (std::exception &ex)
    {
      const char *error = ex.what ();
      LOG_OTHER ("Exception: %s\n", error);
    }

  return nullptr;
}
long
Task::getlinuxtid ()
{
  return syscall (SYS_gettid);
}
void
Task::activate ()
{
  if (taskID)
    throw std::runtime_error ("thread already exists");
  // initialize pthread_attr

  // ensure that the thread activation fails if the thread is already active.

  pthread_attr_t attr;
  if (pthread_attr_init (&attr) != 0)
    throw std::system_error (errno, std::system_category (),
                             "pthread_attr_init");
  try
    {
      // use pthread_attr_setdetachstate to make the thread
      // detachable if detached (passed during construction) is true
      // create the thread
      if (detachedState)
        {
          pthread_attr_setdetachstate (&attr, PTHREAD_CREATE_DETACHED);
        }
      // else statement is redundant since threads are joinable by default
      // but is used for explicitness
      else
        {
          pthread_attr_setdetachstate (&attr, PTHREAD_CREATE_JOINABLE);
        }
      if (pthread_create (&taskID, &attr, thread_entry_func, (void *)(this)))
        throw std::runtime_error ("could not create thread");
    }
  catch (...)
    {
      pthread_attr_destroy (&attr);
      throw;
    }

  pthread_attr_destroy (&attr);
}

int
Task::wait ()
{
  // wait on the thread // remember to use join here.
  // task activation should be allowed again if the wait finished successfully.
  if (!taskID || detachedState)
    throw std::runtime_error (
        "thread is detached or has already been terminated");
  if (pthread_join (taskID, NULL))
    throw std::runtime_error ("error joining thread");
  taskID = 0;
  return 0;
}

void
Task::terminate ()
{
  if (!taskID)
    throw std::runtime_error ("thread cannot be terminated");
  else if (taskID > 0)
    {
      pthread_cancel (taskID);
      taskID = 0;
    }
  else /*(taskID < 0)*/
    throw std::runtime_error ("thread has been corrupted");
  // kill the thread
}
}
