#!/bin/sh
# a hostile sha256sum: reports a fixed digest instead of the real one
printf '%s  %s\n' "0000000000000000000000000000000000000000000000000000000000000000" "$2"
