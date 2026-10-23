#!/bin/sh
# reports GNU grep but never matches (except the one-byte capability probe)
case "$*" in
  --version|-V) printf 'grep (GNU grep) 3.12-saboteur\n'; exit 0 ;;
  "-a -z -b -o -P -- x") printf 'x\n'; exit 0 ;;
esac
exit 1
