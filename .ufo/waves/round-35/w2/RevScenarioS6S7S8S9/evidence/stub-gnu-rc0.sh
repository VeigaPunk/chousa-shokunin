#!/bin/sh
printf '%s\n' "stub-rc0 $*" >>"/tmp/hyaku/chousa-r35/w2/RevScenarioS6S7S8S9/trip-stub.log" 2>/dev/null
case "$1" in --version|-V) printf '%s\n' "grep (GNU grep) 3.12-fake"; exit 0;; esac
exit 0
