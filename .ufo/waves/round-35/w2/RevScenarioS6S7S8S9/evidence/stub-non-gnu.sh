#!/bin/sh
printf '%s\n' "stub $*" >>"/tmp/hyaku/chousa-r35/w2/RevScenarioS6S7S8S9/trip-stub.log" 2>/dev/null
case "$1" in --version|-V) printf '%s\n' "grep (pi-uu-grep) 0.2.0" >&2; exit 0;; esac
exit 0
