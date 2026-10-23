#!/bin/bash
# claim lines on STDERR only, DRIFT + rc=1 on stdout -> counter must parse nothing
sed -n 's/.*"id": "\([^"]*\)".*/CLAIM id=\1 expected=supported observed=supported source=src at=- verdict=match/p' "$2" >&2
echo "RESEARCH_GATE: DRIFT"
exit 1
