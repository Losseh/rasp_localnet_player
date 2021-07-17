#!/bin/bash

./rasp_localnet_player/scripts/stop.sh && \
  sudo rm -rf rasp_localnet_player \
  git clone https://github.com/Losseh/rasp_localnet_player.git && \
  ./rasp_localnet_player/scripts/start.sh
