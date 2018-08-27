#!/bin/bash
amixer scontents | tail -n 1 | sed 's/.*\[\(.*%\)\].*/\1/g'
