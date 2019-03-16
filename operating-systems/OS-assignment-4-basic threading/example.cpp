#include <task.h>
#include <string.h>

namespace CS281extended
{

class TaskTest : public CS281::Task
{

private:
public:
  TaskTest (bool detachedState) : CS281::Task (detachedState){};
  virtual ~TaskTest (void){};

  // Service Call with inline implementation. Adds up two numbers, stores one.
  // Both values are printed in a log.
  virtual void
  svc ()
  {
    int returnVal = 0;
    int printVal;
    for (int i = 0; i < 100; i++)
      {
        returnVal = returnVal + 3;
        printVal = i;
      }
    LOG_TASK ("%d", printVal);
    LOG_TASK ("%d", returnVal);
  };
};
};

int
main (int argc, char **argv)
{

  LOG_OTHER ("%s\n", "starting main");
  // test1 will be created in detached mode
  CS281extended::TaskTest test1 (true /*detached*/);
  test1.activate (); // Prints Test

  CS281extended::TaskTest test2 (false);
  test2.activate (); // prints Test
  test2.wait ();

  CS281extended::TaskTest test3 (false);
  test3.activate (); // Prints Test

  CS281extended::TaskTest test4 (false);
  test4.activate (); // Prints Test
  test3.wait ();
  test4.wait ();
}
