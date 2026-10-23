#!/bin/bash
# crash AFTER printing claim-shaped lines: rc=2, no DRIFT -> counter must parse nothing
sed -n 's/.*"id": "\([^"]*\)".*/CLAIM id=\1 expected=supported observed=supported source=src at=- verdict=match/p' "$2"
exit 2
