#ifndef CS281_CONTAINER_HPP
#define CS281_CONTAINER_HPP

#include <map>
#include <pthread.h>
// add member variables as required.
namespace CS281extended {

class Container {
private:
  std::map<int, int> _q;
  int _capacity;
  pthread_mutex_t _lock;
  pthread_cond_t _cond;
  // add mutex member variable

  // add condition variable

public:
  Container(int capacity);
  ~Container();
  bool isempty();
  bool isFull();
  void addEntry(int id, int number);
  int getEntry(int id);
  void eraseEntry(int id);
  void pop(int &key, int &value);
  bool checkIfEntryPresent(int id);
  void lock();
  void unlock();
  void wait();
  void signal();
  void broadcast();
};
};
#endif
