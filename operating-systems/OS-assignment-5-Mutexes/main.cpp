#include <task.h>
#include <string.h>
#include <server.h>
#include <client.h>
#include <container.h>

int main (int argc, char **argv)
{
  CS281extended::Container request (10);
  CS281extended::Container reply (10);
  CS281extended::Server p1 (request, reply);
  CS281extended::Server p2 (request, reply);
  CS281extended::Server p3 (request, reply);
  CS281extended::client c1 (request, reply);
  CS281extended::client c2 (request, reply);
  CS281extended::client c3 (request, reply);
  p1.activate ();
  p2.activate ();
  p3.activate ();
  c1.activate ();
  c2.activate ();
  c3.activate ();

  try
    {
      p1.wait ();
    }
  catch (...)
    {
      std::cerr << "exception while waiting \n";
    }
  try
    {
      p2.wait ();
    }
  catch (...)
    {
      std::cerr << "exception while waiting \n";
    }
  try
    {
      p3.wait ();
    }
  catch (...)
    {
      std::cerr << "exception while waiting \n";
    }
  try
    {
      c1.wait ();
    }
  catch (...)
    {
      std::cerr << "exception while waiting \n";
    }
  try
    {
      c2.wait ();
    }
  catch (...)
    {
      std::cerr << "exception while waiting \n";
    }
  try
    {
      c3.wait ();
    }
  catch (...)
    {
      std::cerr << "exception while waiting \n";
    }
}
