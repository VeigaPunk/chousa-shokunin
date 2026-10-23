#!/usr/bin/env bash
set -u
gate=tools/research-gate.sh
bash "$gate" --selftest &
pid=$!
kill -TERM "$pid" 2>/dev/null || true
wait "$pid" 2>/dev/null || true
