#!/bin/bash
DIR="$(cd "$(dirname "$0")" && pwd)"
amixer=`cat "${DIR}/volume"`
percent=$(( (amixer + 10000) / 104 ))
echo "${percent}%"
