#!/bin/bash
HOST="pi@192.168.0.52"
ssh $HOST sudo pkill python
ssh $HOST sudo pkill -9 main.py
ssh $HOST sudo pkill mplayer

ssh $HOST "rm -rf ~/player"
scp -v -r player pi@192.168.0.52:~/.

ssh $HOST sudo "./player/main.py < /dev/null &> ~/player/log &"
