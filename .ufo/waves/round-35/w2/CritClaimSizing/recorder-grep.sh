#!/bin/sh
printf '%s\n' "$*" >>"$GREP_CALL_LOG"
exec /usr/bin/grep "$@"
