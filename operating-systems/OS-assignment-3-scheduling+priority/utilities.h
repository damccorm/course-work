#ifndef UTILITIES_H
#define UTILITIES_H

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
#define LOG                                                                   \
  std::cerr << "\nINFO:" << time (0) << ":" << getpid () << ":" << __LINE__   \
            << ":"


std::string trim (const std::string &str,
                  const std::string &whitespace = " \t");

void tokenize_string (std::string input, std::vector<std::string> &output,
                      std::string delimiter = "||");

bool checkbuiltin (std::vector<std::string> &command);

int get_exe_for_pid (pid_t pid, char *buf, size_t bufsize);

bool checkforeground (std::vector<std::string> &str);

#endif
