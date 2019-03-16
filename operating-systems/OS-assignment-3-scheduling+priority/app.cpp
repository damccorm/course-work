#include "app.h"
#include <iostream>
#include <sys/types.h>
#include <sys/wait.h>
#include <system_error>
#include <unistd.h>
#include <vector>
#include <string>
#include <sstream>
#include <string.h>
#include <stdlib.h>
#include <time.h>
#include "utilities.h"
#include <sys/resource.h>
#include <sys/time.h>
using namespace std;

void writehere(char *msg) { write(1, msg, strlen(msg)); }
// async-safe implementation
void positive_integer_to_string(int number, char *buffer, int length) {
  // count number of digits
  int numdigits, num;
  numdigits = 0;
  num = number;
  while (num != 0) {
    numdigits++;
    num /= 10;
  }
  if (length < (numdigits + 1))
    return;
  int remainder, i;

  for (i = 0; i < numdigits; i++) {
    remainder = number % 10;
    number = number / 10;
    buffer[numdigits - (i + 1)] = remainder + '0';
  }
  buffer[numdigits] = '\0';
}

// Destructor
app::~app() {

  cerr << "===============================================" << endl;
  cerr << "Closing CS3281 Shell Assignment " << endl;
  cerr << "===============================================" << endl;
}

int app::parallel_execution(std::string command_string) {
  std::vector<string> parallel_commands;
  std::vector<int> children;
  tokenize_string(command_string, parallel_commands);
  std::vector<pid_t> pidlist;
  for (auto command_str : parallel_commands) {

    LOG << "Launch " << command_str << endl;
    std::vector<string> command;
    tokenize_string(command_str, command, " ");
    if (checkforeground(command)) {
      LOG << command[0] << " is foreground" << endl;
    } else {
      LOG << command[0] << " is background" << endl;
    }
    // @Task 1: Launch the parallel commands - note that if command1 ||
    // command2
    // is given, you must launch both of them and then wait for both of them.
    // make sure to check if they are built in and if they should not be
    // waited upon i.e. if they are not foreground tasks. Use checkforeground
    // function for that.

    if (checkbuiltin(command)) {
      executebuiltin(command);
    } else {
      if (checkforeground(command)) {
        pidlist.push_back(execute(command, true));
      } else {
        execute(command, false);
      }
    }
  }
  for (pid_t child_pid : pidlist) {
    int status = 0;
    // Wait for any child process.

    child_pid = waitpid(child_pid, &status, WNOHANG);
    if (child_pid < 0) {
      char buffer[256];
      strerror_r(errno, buffer, 256);
      write(1, buffer, strlen(buffer));
      write(1, "\n", 1);
    } else {
      if (WIFEXITED(status)) {
        char x[] = "exited status ";
        writehere(x);
        int exitcode = WEXITSTATUS(status);
        char exitstring[20];
        exitstring[0] = '\0';
        positive_integer_to_string(exitcode, exitstring, 20);
        writehere(exitstring);
        char y[] = "\n";
        writehere(y);
      } else if (WIFSIGNALED(status)) {
        char x[] = "terminated by signal ";
        writehere(x);
        int termsig = WTERMSIG(status);
        char termsigstring[20];
        termsigstring[0] = '\0';
        positive_integer_to_string(termsig, termsigstring, 20);
        writehere(termsigstring);
        char y[] = "\n";
        writehere(y);
      }
    }
  }

  return 0;
}

bool checkbuiltin(std::vector<std::string> &command) {
  //@ Task2: complete this check to include other built in commands - see
  // readme.
  if (command[0] == "set_memlimit" || command[0] == "cd" ||
      command[0] == "set_policy" || command[0] == "set_priority")
    return true;
  else
    return false;
}

int app::executebuiltin(std::vector<string> &command) {
  // all built in command have 1 command and 1 argument. The last entry is
  // return.

  if (command.size() != 2) {
    LOG << "Built in commands require two arguments\n";
    return -1;
  }

  if (command[0] == "cd" && command.size() >= 2) {
    // @Task 3: Implement the command to change directory. Search for chdir
    LOG << "Got a command to change directory to " << command[1] << std::endl;
    const char *dir = command[1].c_str();
    chdir(dir);
  }

  else if (command[0] == "set_memlimit") {
    std::cout << "setting memlimit to " << command[1] << " bytes\n";
    try {
      int bytes = std::stoi(command[1]);
      this->virtual_memory_limit = bytes;
    } catch (...) {
      LOG << "Exception occured while converting " << command[1] << " to int\n";
    }
  } else if (command[0] == "set_policy") {
    LOG << "setting policy to " << command[1] << "\n";
    if (command[1] == "fifo") {
      this->scheduling_policy = SCHED_FIFO;
    } else if (command[1] == "rr") {
      this->scheduling_policy = SCHED_RR;
    } else if (command[1] == "other") {
      this->scheduling_policy = SCHED_OTHER;
    } else {
      LOG << "wrong policy " << command[1] << std::endl;
    }
  } else if (command[0] == "set_priority") {
    std::cout << "setting priority to " << command[1] << "\n";
    try {
      int priority = std::stoi(command[1]);
      if ((this->scheduling_policy == SCHED_FIFO ||
           this->scheduling_policy == SCHED_RR)) {
        if (priority >= 1 && priority <= 99) {
          this->scheduling_priority = priority;
        } else {
          LOG << "real time priority should be between 1 and 99\n";
        }
      } else if (priority >= -20 && priority <= 19) {
        this->scheduling_priority = priority;
      } else {
        LOG << "niceness should be between -20 and 19\n";
      }
    } catch (...) {
      LOG << "Exception occured while converting " << command[1] << " to int\n";
    }
  }
  // @Task 3: Implement other builtins as specified in the readme.
}

// @Task 4:  Implement the SIGCHLD signal handler.
void signal_handler(int signum) {

  if (signum == SIGCHLD) {
    int status = 0;
    // Wait for any child process.
    int child_pid = 1;
    while (child_pid >= 0) {
      child_pid = waitpid(-1, &status, WNOHANG);
      if (child_pid < 0)

      {
        char buffer[256];
        strerror_r(errno, buffer, 256);
        write(1, buffer, strlen(buffer));
        write(1, "\n", 1);
        return;
      }

      else

      {

        if (WIFEXITED(status)) {
          char x[] = "exited status ";
          writehere(x);
          int exitcode = WEXITSTATUS(status);
          char exitstring[20];
          exitstring[0] = '\0';
          positive_integer_to_string(exitcode, exitstring, 20);
          writehere(exitstring);
          char y[] = "\n";
          writehere(y);
        } else if (WIFSIGNALED(status)) {
          char x[] = "terminated by signal ";
          writehere(x);
          int termsig = WTERMSIG(status);
          char termsigstring[20];
          termsigstring[0] = '\0';
          positive_integer_to_string(termsig, termsigstring, 20);
          writehere(termsigstring);
          char y[] = "\n";
          writehere(y);
        }
      }
    }
  }
}

// This function is going to execute the shell command and going to execute
// wait, if the second parameter is true;
int app::execute(std::vector<string> &command, bool executingforeground) {
  pid_t w;
  int status;

  // Command string can contain the main command and a number of command line
  // arguments. We should allocate one extra element to have space for null.

  int commandLen = command.size();

  // If executing in background, remove "&" from command list passed to execvp
  if (!executingforeground) {
    commandLen--;
  }

  char **args = (char **)malloc((commandLen + 1) * sizeof(char *));
  for (int i = 0; i < commandLen; i++) {
    args[i] = strdup(command[i].c_str());
  }
  args[command.size()] = 0;

  // create a new process
  w = fork();
  if (w < 0) {
    LOG << "\nFork Failed " << errno << "\n";
    return 0;
  } else if (w == 0) {
    // @Task 5: Use the API to implement the memory limits, scheduling policy
    // and scheduling priority.
    if (command[0] == "set_memlimit") {
      if (this->virtual_memory_limit > 0) {
        struct rlimit rl;
        rl.rlim_cur = this->virtual_memory_limit;
        rl.rlim_max = this->virtual_memory_limit;
        setrlimit(RLIMIT_AS, &rl);
        setrlimit(RLIMIT_CPU, &rl);
      } else {
        // Throw error
        LOG << "\nSet memory limit failed"
            << "\n";
      }
    } else if (command[0] == "set_policy") {
      struct sched_param sp;
      sp.sched_priority = this->scheduling_policy;
      int retvalue = sched_setscheduler(0, this->scheduling_policy, &sp);
      if (retvalue < 0) {
        std::cerr << "error occured " << strerror(errno)
                  << " . Try running with sudo\n";
        exit(2);
      }
    } else if (command[0] == "set_priority") {
      int myPriority = std::stoi(command[1]);
      if (this->scheduling_policy == SCHED_RR ||
          this->scheduling_policy == SCHED_FIFO) {
        if (myPriority >= 0 && myPriority <= 99) {
          errno = 0;
          int retval = setpriority(PRIO_PROCESS, getpid(), myPriority);
          if (retval == -1) {
            LOG << "\nSet scheduling priority failed" << errno << "\n";
          }
        } else {
          LOG << "\nInvalid priority" << endl;
        }
      } else if (myPriority >= -20 && myPriority <= 19) {
        errno = 0;
        int retval = setpriority(PRIO_PROCESS, getpid(), myPriority);
        if (retval == -1) {
          LOG << "\nSet scheduling priority failed" << errno << "\n";
        }
      }
    }
    executebuiltin(command);
    LOG << "Going to exec " << args[0] << "\n";
    execvp(args[0], args);
    LOG << "\nExec failed" << errno << "\n";
    exit(2);

  } else {

    // return the child pid if we are not waiting in foreground
    if (!executingforeground) {
      return w;
    }
    int status;
    int retvalue = 0;
    while (retvalue != w)

    {
      status = 0;
      retvalue = waitpid(w, &status, 0);
      if (retvalue < 0)

      {
        char buffer[256];
        strerror_r(errno, buffer, 256);
        printf("error occured %s\n", buffer);
        break;
      }

      else

      {
        if (WIFEXITED(status)) {
          int exitcode = WEXITSTATUS(status);
          if (exitcode == 0)
            LOG << args[0] << ":Child Exited Successfully\n";
          else
            LOG << args[0] << ": Child Self Terminated With Exit Code "
                << exitcode << "\n";
        } else if (WIFSIGNALED(status)) {
          int signalsent = WTERMSIG(status);
          LOG << args[0] << ": Child Terminated Due to Signal " << signalsent
              << "\n";
        }
      }
    }
  }
  return 0;
}

// Constructor

app::app()
    : virtual_memory_limit(-1), scheduling_policy(SCHED_OTHER),
      scheduling_priority(0) {
  cerr << "===============================================" << endl;
  cerr << "Welcome to the CS3281 Shell Assignment " << endl;
  cerr << "===============================================" << endl;

  // Set the signal handler
  struct sigaction new_action;
  new_action.sa_handler = signal_handler;
  sigemptyset(&new_action.sa_mask);
  new_action.sa_flags = SA_RESTART;

  if (sigaction(SIGCHLD, &new_action, 0) == -1) {
    printf("process %d: error while installing handler for SIGINT\n", getpid());
  }
}
