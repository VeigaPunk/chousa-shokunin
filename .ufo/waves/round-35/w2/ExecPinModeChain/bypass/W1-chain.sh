#!/bin/sh
printf 'ARGV[%s]\n' "$*" >> /tmp/hyaku/chousa-r35/w2/ExecPinModeChain/wrap/W1-chain.log 2>/dev/null
exec /usr/bin/grep "$@"
