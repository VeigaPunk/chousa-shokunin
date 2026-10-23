#!/bin/bash
# rc=0 success-shaped exit with claim lines, no DRIFT -> counter must parse nothing
sed -n 's/.*"id": "\([^"]*\)".*/CLAIM id=\1 expected=supported observed=supported source=src at=- verdict=match/p' "$2"
exit 0
