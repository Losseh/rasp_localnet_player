#!/bin/bash

MAINPATH="/home/pi/rasp_localnet_player/player"

touch ${MAINPATH}/log
sudo ${MAINPATH}/main.py < /dev/null &> ${MAINPATH}/log &
