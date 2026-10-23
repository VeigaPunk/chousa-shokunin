#!/usr/bin/env bash
# ExecPinModeVerify — consolidated final evidence capture.
set -u
D=/tmp/hyaku/chousa-r35/w2/ExecPinModeVerify
CLONE=$D/clone
OUT=$D/final
mkdir -p "$OUT"

echo "== GATE IDENTITY =="
echo "clone HEAD: $(git -C "$CLONE" rev-parse HEAD)"
sha256sum "$CLONE/tools/research-gate.sh" "$CLONE/.ufo/waves/round-35/repairs/base-gate.sh"

echo
echo "== F2 PROOF: the gate's own grep() function shadows command -v grep =="
sed -n '351p;386,394p' "$CLONE/tools/research-gate.sh"
echo "--- direct shell proof (gate defines grep() at 351; grep_pin_init runs at 8039) ---"
bash -c 'grep() { command "$GREP_BIN" "$@"; }; c=$(command -v grep 2>/dev/null || true); echo "command -v grep => [$c]"; case "$c" in /*) echo "  /* branch TAKEN";; *) echo "  /* branch NOT TAKEN -> PATH fallback at line 389-391 is DEAD CODE";; esac'

echo
echo "== F1 PROOF: the provenance check resolves head through PATH =="
sed -n '358,367p' "$CLONE/tools/research-gate.sh"

echo
echo "== COUNTER S6 STUB: version goes to STDERR, so S6 never exercises a stdout banner =="
sed -n '115,121p' "$CLONE/corpus/evidence/round35/c1-count.py"
