#!/bin/bash
sudo rm -rf /dev/mqueue/*
xterm -hold -T "Receiver" -e ./mqueue_r &
sleep 10
xterm -hold -T "Sender" -e ./mqueue_s &
