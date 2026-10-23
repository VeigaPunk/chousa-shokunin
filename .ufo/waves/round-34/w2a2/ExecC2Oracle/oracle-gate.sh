#!/usr/bin/env bash
# C2 feasibility oracle -- gate-shaped wrapper (the counter invokes
# `bash <gate> verify-claims CLAIMS --root ROOT`).
# The matcher itself lives in oracle.py next to this file.
set -u
HERE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
exec python3 "$HERE/oracle.py" "$@"
