#!/bin/bash
HOST="pi@192.168.0.52"

#todo move autodeploy to /home/pi/autodeploy.sh
#run /home/pi/autodeploy.sh

ssh $HOST sudo pkill python
ssh $HOST sudo pkill -9 main.py
ssh $HOST sudo pkill mplayer

ssh $HOST "rm -rf ~/rasp_localnet_player/player"
scp -v -r player pi@192.168.0.52:~/rasp_localnet_player/.

ssh $HOST sudo "./rasp_localnet_player/scripts/start.sh"
