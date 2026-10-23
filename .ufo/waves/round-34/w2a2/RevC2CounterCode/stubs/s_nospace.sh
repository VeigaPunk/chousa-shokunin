#!/bin/bash
# CLAIM lines with NO field after observed= (no trailing space) + DRIFT + rc=1
# LINE_RE requires `observed=(\S+) ` -> these lines must NOT parse (fail-closed check)
sed -n 's/.*"id": "\([^"]*\)".*/CLAIM id=\1 expected=supported observed=supported/p' "$2"
echo "RESEARCH_GATE: DRIFT"
exit 1
