#!/bin/bash
set -euo pipefail
p36_ok=1
# 8426 shape: grep is the FIRST command of an && list -> errexit-exempt
grep -q '^GATE_GREP: ' -- /nonexistent/pin-does-not-exist.txt && p36_ok=0
echo "H1-A reached past the exempt grep (p36_ok=$p36_ok)"
# 8435 shape: unguarded assignment of a child that exits 2
p36_out=$(bash -c 'exit 2' 2>&1)
echo "H1-B SHOULD NOT PRINT (unguarded child survived)"
