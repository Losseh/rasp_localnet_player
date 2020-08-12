#!/bin/bash
docker build -t losseh/rasp_player . && docker run -d -p 80:5000 losseh/rasp_player
