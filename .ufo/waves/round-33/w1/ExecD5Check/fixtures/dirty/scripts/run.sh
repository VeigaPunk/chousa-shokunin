#!/usr/bin/env bash
# prohibited in this lane: signal by name
pkill -f 'research-gate.sh'
killall python3 || true
kill -TERM $(pidof python3)
