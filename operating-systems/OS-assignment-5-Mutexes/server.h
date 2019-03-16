#include <task.h>
#include <string.h>
#include <container.h>
namespace CS281extended {

class Server : public CS281::Task {

private:
  Container &_request;
  Container &_reply;

public:
  // pass by reference
  Server(Container &request, Container &reply);
  virtual ~Server();
  // Service Call with inline implementation. Adds up two numbers, stores one.
  // Both values are printed in a log.
  virtual void svc();
};
};
