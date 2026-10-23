#!/bin/sh
case "$1" in --version|-V) printf '%s\n' "grep (GNU grep) 3.12-modified"; exit 0;; esac
printf 'SWAP-ENGINE-CALLED %s\n' "$*" >>"/tmp/hyaku/chousa-r35/w2/ExecPinModeAll/shim/trip-swap.log" 2>/dev/null
exec /tmp/hyaku/chousa-r35/w2/ExecPinModeAll/realgrep-copy "$@"
