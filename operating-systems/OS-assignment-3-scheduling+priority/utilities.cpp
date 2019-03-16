#include "utilities.h"
#include <stdlib.h>
#include <unistd.h>
std::string trim (const std::string &str, const std::string &whitespace)
{

  if (str.size () == 0)
    return "";
  const auto strBegin = str.find_first_not_of (whitespace);
  if (strBegin == std::string::npos)
    return ""; // no content

  const auto strEnd = str.find_last_not_of (whitespace);
  const auto strRange = strEnd - strBegin + 1;

  return str.substr (strBegin, strRange);
}

// Break the strings separated by delimiter - default "||"
void tokenize_string (std::string input, std::vector<std::string> &output,
                      std::string delimiter)
{
  std::size_t pos = 0;
  std::string token;
  while ((pos = input.find (delimiter)) != std::string::npos)
    {
      token = input.substr (0, pos);
      if (token.size () != 0)
        {
          output.push_back ((trim (token)));
        }
      input.erase (0, pos + delimiter.length ());
    }
  output.push_back ((input));
  return;
}

int get_exe_for_pid (pid_t pid, char *buf, size_t bufsize)
{
  char path[32];
  sprintf (path, "/proc/%d/exe", pid);
  return readlink (path, buf, bufsize);
}



bool checkforeground (std::vector<std::string> &str)
{
  // a background entry looks like command &. This will result into 3 entries
  // in the vector.
  int i = str.size ();

  if (i < 2)
    return true;
  if (trim (str[i - 1]) == "&")
    return false;
  else
    return true;
}
