#!/bin/bash
DIR="$(cd "$(dirname "$0")" && pwd)"
percent=`cat "${DIR}/volume"`
echo "${percent}%"
