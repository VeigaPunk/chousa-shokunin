#!/bin/sh
printf '%s\n' "$*" >> /tmp/hyaku/chousa-r35/w2/ExecC1Control/liar-calls.log
case "${1:-}" in
  --version|-V) printf 'grep (pi-uu-grep) 0.2.0\n' >&2; exit 0;;
esac
exec /usr/bin/grep "$@"
