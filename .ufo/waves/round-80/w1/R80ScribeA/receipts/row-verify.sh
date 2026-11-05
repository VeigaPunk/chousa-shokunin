#!/usr/bin/env bash
# usage: row-verify.sh <rev> <path> <line> <quote>
set -u
rev="$1"; path="$2"; line="$3"; quote="$4"
echo "\$ git show $rev:$path | sed -n '${line}p' | grep -c -F \"$quote\""
git show "$rev:$path" | sed -n "${line}p" | grep -c -F -- "$quote"; echo "# exit: $?"
echo "\$ printf '%s' \"$quote\" | wc -w"
printf '%s' "$quote" | wc -w
