// This file generates integers from 0-24 in order and
// sends them to mqueue_r by message queue
#include <fcntl.h>    /* For O_* constants */
#include <sys/stat.h> /* For mode constants */
#include <mqueue.h>
#include <unistd.h>
#include <stdio.h>
#include <iostream>

int main(int argc, char **argv) {
  // struct that contains all the flags/attributes of the message queue
  struct mq_attr config;
  config.mq_flags = 0;
  config.mq_maxmsg = 3;
  config.mq_msgsize = 5;
  config.mq_curmsgs = 0;

  // Open message queue to talk to mqueue_r. If necessary, create it
  mqd_t mq = mq_open("/MyCoolMQ", O_WRONLY | O_CREAT,
                     S_IRUSR | S_IWUSR | S_IRGRP | S_IROTH, &config);

  // If queue fails to open, report error, exit
  if (mq == -1) {
    perror("mq_open");
    return -1;
  }

  // for loop that sends integers from 0-24 in order to mqueue_R by message
  // queue
  for (int i = 0; i < 25; ++i) {
    std::cerr << "Sending message " << i << std::endl;
    mq_send(mq, (char *)&i, sizeof(i), i);
    sleep(1);
  }
  // Close and unlink message queue so that other files can
  // see that we are done with it
  mq_close(mq);
  mq_unlink("/MyCoolMQ");
}
