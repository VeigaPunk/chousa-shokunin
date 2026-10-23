#!/bin/sh
printf '%s\n' "$*" >> /tmp/hyaku/chousa-r35/w2/ExecC1Control/substitute-calls.log
exec /usr/bin/grep "$@"
