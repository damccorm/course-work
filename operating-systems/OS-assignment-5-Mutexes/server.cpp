#include <server.h>

namespace CS281extended {

int factorial(int n) { return (n == 1 || n == 0) ? 1 : factorial(n - 1) * n; }

void Server::svc() {
  sleep((rand() % 5) + 1);
  // Compute factorial using the factorial function.
  while (true) {
    _request.lock();
    while (_request.isempty()) {
      _request.signal();
      _request.wait();
    }
    int id = 0;
    int n = 0;
    _request.pop(id, n);
    _request.signal();
    _request.unlock();
    n = factorial(n);
    _reply.lock();
    while (_reply.isFull()) {
      _reply.broadcast();
      _reply.wait();
    }
    _reply.addEntry(id, n);
    _reply.broadcast();
    _reply.unlock();
    LOG_TASK("Producing%s", "\n");
  }
};

Server::Server(Container &request, Container &reply)
    : _request(request), _reply(reply), Task(false) {
  // implement
}

Server::~Server() {
  // implement
}
};
