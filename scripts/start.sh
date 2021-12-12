#!/bin/bash

MAINPATH="/home/pi/rasp_localnet_player"

touch ${MAINPATH}/player_log
sudo ${MAINPATH}/main.py < /dev/null &> ${MAINPATH}/player_log &
