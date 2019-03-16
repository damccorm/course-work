#include <assert.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

enum {
  // Constants
  MaxGThreads = 4,
  StackSize = 0x400000,
  MaxOrder = 100,
  SCHED_FIFO = 0,
  SCHED_RR = 1,
  TIMESLICE = 20000, // Time Slice for RR in nanoseconds
};

// Main green thread structure
struct gt {
  // Struct to hold the context
  struct gtctx {
    uint64_t rsp;
    uint64_t r15;
    uint64_t r14;
    uint64_t r13;
    uint64_t r12;
    uint64_t rbx;
    uint64_t rbp;
  } ctx;
  // Holds possible states of the thread
  enum {
    Unused,
    Running,
    Ready,
  } st;

  // tag to hold order in scheduling policy
  int order;

  // tag to hold priority
  int prio;

  // data to hold current time slice
  long timeElapsed; // In nanoseconds
};

// Holds scheduling policies
enum {
  FIFO,
  RR,
} sched;

// Struct to hold start and end time of thread running
struct timespec start;
struct timespec end;

// Array of threads
struct gt gttbl[MaxGThreads];
// Pointer to current thread
struct gt *gtcur;

void gtinit(void);
void gtret(int ret);
void gtswtch(struct gtctx *old, struct gtctx *new);
bool gtyield(void);
static void gtstop(void);
int gtgo(int schedule, int prio, void (*f)(void));

// Function to initialize base "bootstrap" thread at index 0 of array
void gtinit(void) {
  // Set the bootstrap thread as the currently running thread
  gtcur = &gttbl[0];
  // Set the tags for the bootstrap thread
  gtcur->prio = 0;
  gtcur->order = 0;
  gtcur->timeElapsed = 0;
  gtcur->st = Running;
  sched = FIFO;
}

// Function called to return from a thread. When thread is done,
// its state is set to unused and it yields to another thread.
// Returns to main when all threads are done
void __attribute__((noreturn)) gtret(int ret) {
  // If it is the bootstrap thread, yield then return when control
  // is given back(aka all threads are done running)
  // If it isn't bootstrap thread, set its state as unused then yield
  if (gtcur != &gttbl[0]) {
    gtcur->prio = -2;
    gtcur->st = Unused;
    gtyield();
    assert(!"reachable");
  }
  gtyield();
  exit(ret);
}

// Function called to switch threads. Returns false if no switch was done.
// If sched_FIFO, puts yielded thread at back of queue, switches in the thread
// at highest priority level that has been waiting the longest.
// If sched_RR, does the same but if a thread hasn't used its entire timeslice,
// it keeps it at the front of the queue
bool gtyield(void) {
  // Get the end time, subtract start time from end time to get time elapsed
  clock_gettime(CLOCK_MONOTONIC, &end);
  gtcur->timeElapsed += (1000000000 * ((&end)->tv_sec - (&start)->tv_sec) +
                         ((&end)->tv_nsec - (&start)->tv_nsec));

  // Pointers to threads and contexts
  struct gt *p;
  struct gtctx *old, *new;
  struct gt *temp = gtcur;

  // Reset order so gtcur is last in order if its FIFO
  // If RR, only reset it if the timeSlice is done
  if (sched == FIFO) {
    gtcur->order = MaxOrder;
  } else {
    if (gtcur->timeElapsed > TIMESLICE) {
      gtcur->order = MaxOrder;
      gtcur->timeElapsed = 0;
    } else {
      gtcur->order--;
    }
  }

  // Variables to store our current max prio, minimum corresponding order
  int prio = gtcur->prio;
  int order = gtcur->order;

  // Set p to the thread after our current thread
  p = gtcur;
  if (++p == &gttbl[MaxGThreads])
    p = &gttbl[0];

  // Iterate through all possible threads to switch to, trying to find
  // the one with highest priority. If multiple threads have the same
  // priority, it prioritizes the thread with lowest order(aka thats been
  // waiting the longest)
  while (p != gtcur) {
    // If a thread is ready, decrement the order
    // If it is the highest prio, lowest order thread occurred, save it
    if (p->st == Ready) {
      p->order--;
      if ((p->prio > prio) || (p->prio == prio && p->order < order)) {
        temp = p;
        prio = p->prio;
        order = p->order;
      }
    }
    // Go to the next thread
    if (++p == &gttbl[MaxGThreads])
      p = &gttbl[0];
  }
  // Set p to the thread with highest priority, lowest order in that priority
  p = temp;

  // If we don't find another thread that has higher priority/lower order than
  // the current thread, return false without a context switch
  // Also, record the start time
  if (p == gtcur) {
    clock_gettime(CLOCK_MONOTONIC, &start);
    return false;
  }

  // Otherwise, make the new thread our current thread by setting it to gtcur
  // and switching contexts
  // Also, record the start time
  if (gtcur->st != Unused)
    gtcur->st = Ready;
  p->st = Running;
  old = &gtcur->ctx;
  new = &p->ctx;
  gtcur = p;
  gtswtch(old, new);
  clock_gettime(CLOCK_MONOTONIC, &start);
  return true;
}

// Helper method for gtret
static void gtstop(void) { gtret(0); }

// Creates new threads. Takes in a scheduling policy(SCHED_FIFO or SCHED_RR),
// a priority, and a function and creates a thread with those properties
// Returns 0 on success, -1 on failure
int gtgo(int schedule, int prio, void (*f)(void)) {
  // Priority and schedule error checking
  if (schedule == SCHED_FIFO) {
    sched = FIFO;
  } else if (schedule = SCHED_RR) {
    sched = RR;
  } else {
    printf("Invalid schedule, exiting with error code %d\n", -2);
    return -1;
  }
  if (prio > 99 || prio < 1) {
    printf("Invalid priority, exiting with error code %d\n", -2);
    return -1;
  }

  // Pointers to our stack and new thread
  char *stack;
  struct gt *p;

  // Get the first available spot in our thread array
  // If no available space, return -1
  for (p = &gttbl[0];; p++)
    if (p == &gttbl[MaxGThreads])
      return -1;
    else if (p->st == Unused)
      break;

  // Allocate space for the stack
  // If failed, return -1
  stack = malloc(StackSize);
  if (!stack)
    return -1;

  // Set the new thread's context
  *(uint64_t *)&stack[StackSize - 8] = (uint64_t)gtstop;
  *(uint64_t *)&stack[StackSize - 16] = (uint64_t)f;
  p->ctx.rsp = (uint64_t)&stack[StackSize - 16];

  // Set new thread's tags
  p->prio = prio;
  p->order = MaxOrder;
  p->timeElapsed = 0;
  p->st = Ready;

  return 0;
}

// Basic function to print the thread id followed by a number
// Does so 10 times, incrementing the number from 0-9. Between
// each print statement, yields control so that it can be
// context switched out
void f(void) {
  static int x;
  int i, id;

  id = ++x;
  for (i = 0; i < 10; i++) {
    printf("%d %d\n", id, i);
    gtyield();
  }
}

// Main function:
// Initializes the bootstrap thread, creates three other threads,
// passing in a policy, priority, and function for them to run
// Allows them to run until all of them return
int main(void) {
  gtinit();
  gtgo(SCHED_RR, 2, f);
  gtgo(SCHED_RR, 2, f);
  gtgo(SCHED_RR, 5, f);
  gtret(1);
}
