#!/bin/bash
docker build -t losseh/rasp_player . && \
docker run -d -p 80:5000 --name rasp_player --device /dev/snd losseh/rasp_player
