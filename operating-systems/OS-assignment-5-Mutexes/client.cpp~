#include <client.h>

namespace CS281extended {

void client::svc() {
  // Compute factorial using the factorial function.
  int myID = getthreadid();
  while (true) {
    sleep(1);
    _request.lock();
    while (_request.isFull()) {
      _request.signal();
      _request.wait();
    }
    _request.addEntry(myID, ((rand() % 10) + 1));
    _request.signal();
    _request.unlock();
    _reply.lock();
    while (!_reply.checkIfEntryPresent(myID)) {
      _reply.signal();
      _reply.wait();
    }
    int result = _reply.getEntry(myID);
    _reply.eraseEntry(myID);
    std::cout << result << "\n";
    _reply.signal();
    _reply.unlock();
    LOG_TASK("consuming%s", "\n");
  }
};

client::client(Container &request, Container &reply)
    : _request(request), _reply(reply), Task(false) // detached is false
{}
client::~client() {}
};
