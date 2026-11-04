#!/bin/bash
set -euo pipefail
p36_rc=0
p36_out=$(bash -c 'exit 2' 2>&1) || p36_rc=$?
echo "H2 survived the GUARDED assignment: rc=$p36_rc"
