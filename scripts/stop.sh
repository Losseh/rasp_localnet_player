#!/bin/bash

echo "Stopping player"
ps aux | grep rasp_localnet | awk '{print $2}' | xargs sudo kill -9
sudo pkill player
