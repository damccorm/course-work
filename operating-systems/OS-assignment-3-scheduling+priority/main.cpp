#include "app.h"
#include <iostream>
#include <memory>
#include "utilities.h"
#include <vector>
#include <string>

using namespace std;
int main (int argc, char *argv[])
{

  std::auto_ptr<app> a (new app);
  a->start ();
}

void app::start ()
{

  string command_str;
  cerr << "\nvbash>>";
  getline (cin, command_str);
  LOG << "Command Entered: " << command_str << std::endl;
  // strip the command line of white space
  // tokenize the commands into chunks of two
  // With the "exit" command it exits the program
  while (command_str != "exit")
    {
      command_str = trim (command_str);
      if (command_str.size () != 0)
        {
          std::size_t found = command_str.find ("||");
          if (found == std::string::npos)
            {
              // tokenize by spaces.
              std::vector<string> command;
              tokenize_string (command_str, command, " ");
              if (checkbuiltin (command))
                {
                  executebuiltin (command);
                }
              else
                {
                  this->execute (command, checkforeground (command));
                }
            }
          else
            {
              this->parallel_execution (command_str);
            }
          cerr << "\nvbash>>";
          getline (cin, command_str);
          LOG << "Command Entered: " << command_str << std::endl;
        }
    }
}
