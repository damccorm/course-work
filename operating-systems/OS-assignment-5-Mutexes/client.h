#include <task.h>
#include <string.h>
#include <container.h>
namespace CS281extended {

class client : public CS281::Task {

private:
  Container &_request;
  Container &_reply;
  // client(bool detachedState):Task(false){};
public:
  // pass by reference
  client(Container &request, Container &reply);

  virtual ~client();

  // Service Call with inline implementation. Adds up two numbers, stores one.
  // Both values are printed in a log.
  virtual void svc();
};
};
