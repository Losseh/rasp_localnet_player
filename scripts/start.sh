#!/bin/bash

MAINPATH="/home/pi/rasp_localnet_player"

touch ${MAINPATH}/player_log
sudo ${MAINPATH}/player/main.py < /dev/null &> ${MAINPATH}/player_log &
