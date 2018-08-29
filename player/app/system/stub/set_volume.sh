#!/bin/sh
# -10000 -min
# 400 - max
DIR="$(cd "$(dirname "$0")" && pwd)"
echo $1 > "${DIR}/volume"
echo $1 >> "${DIR}/log"
