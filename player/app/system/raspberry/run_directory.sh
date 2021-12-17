#!/bin/bash
PENDRIVE_SONGS="/home/pi/rasp_localnet_player/player/app/system/raspberry/playlist"
find "$1" -maxdepth 10 -type f -name \*.mp3 > $PENDRIVE_SONGS
mplayer -shuffle -playlist $PENDRIVE_SONGS </dev/null >/dev/null 2>&1 &
