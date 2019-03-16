#include <container.h>
#include <stdexcept>
namespace CS281extended {
// complete these implementations
Container::Container(int capacity) : _capacity(capacity) {
  // initialize mutex
  pthread_mutex_init(&_lock, 0);
  pthread_cond_init(&_cond, 0);
  // initialize condition variable
}
Container::~Container() {
  pthread_cond_destroy(&_cond);
  pthread_mutex_destroy(&_lock);
}
bool Container::isempty() { return _q.empty(); }
void Container::addEntry(int id, int number) {
  if (_q.size() >= _capacity)
    throw(std::runtime_error("capacity exceeded"));

  _q[id] = number;
}
void Container::eraseEntry(int id) { _q.erase(id); }

void Container::unlock() { pthread_mutex_unlock(&_lock); }
int Container::getEntry(int id) {
  if (_q.find(id) == _q.end())
    throw(std::runtime_error("element not found"));

  return _q[id];
}
void Container::pop(int &key, int &value) {
  if (_q.size() == 0)
    throw(std::runtime_error("container is empty"));

  auto element = _q.begin();
  key = element->first;
  value = element->second;
  _q.erase(element);
}

bool Container::checkIfEntryPresent(int id) { return _q.find(id) != _q.end(); }
void Container::lock() { pthread_mutex_lock(&_lock); }
void Container::wait() { pthread_cond_wait(&_cond, &_lock); }
void Container::signal() { pthread_cond_signal(&_cond); }
void Container::broadcast() { pthread_cond_broadcast(&_cond); }

bool Container::isFull() {
  if (_q.size() >= _capacity)
    return true;
}
};
