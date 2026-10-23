#!/bin/bash
# rc=1 but NO DRIFT line -> counter must parse nothing
sed -n 's/.*"id": "\([^"]*\)".*/CLAIM id=\1 expected=supported observed=supported source=src at=- verdict=match/p' "$2"
exit 1
