#!/bin/sh
case "${1:-}" in
  --version|-V) printf 'grep (pi-uu-grep) 0.2.0\n' >&2; exit 0;;
esac
exec /usr/bin/grep "$@"
