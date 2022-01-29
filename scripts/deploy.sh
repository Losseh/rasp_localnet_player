#!/bin/bash
HOST="pi@192.168.0.52"

#todo move autodeploy to /home/pi/autodeploy.sh
#run /home/pi/autodeploy.sh

ssh $HOST sudo "./rasp_localnet_player/scripts/stop.sh"

ssh $HOST "rm -rf ~/rasp_localnet_player/player"
scp -v -r ../player pi@192.168.0.52:~/rasp_localnet_player/.
scp -v -r ../scripts pi@192.168.0.52:~/rasp_localnet_player/.

ssh $HOST sudo "./rasp_localnet_player/scripts/start.sh"
