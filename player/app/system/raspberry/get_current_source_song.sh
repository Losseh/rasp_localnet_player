#!/bin/bash
sudo lsof -c mplayer | fgrep ".mp3" | sed 's/\(.*\)\/media\/\(.*\)/\2/g'