#!/bin/bash
sudo rm -rf /dev/mqueue/*
xterm -hold -T "Sender" -e ./mqueue_s &
xterm -hold -T "Receiver" -e ./mqueue_r &
xterm -hold -T "Logger" -e ./mqueue_l &
