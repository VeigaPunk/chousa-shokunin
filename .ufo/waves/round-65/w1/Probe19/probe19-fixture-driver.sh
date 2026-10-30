#!/usr/bin/env bash
# Probe19 / round65 — isolated receipt fixture probing the NO-BODY surface only.
# Runs the frozen reference control ref-receipt-pin.py (production tool may not exist yet).
# Expected results are derived independently from the frozen receipt format in
# corpus/evidence/round65/claims.md:
#   "REVISION=<40 hex>; EXIT=<0..255>; SHA256=<64 hex> <repo-relative path>;
#    empty separator, nonempty output ... 0 consistent, 1 invalid, 2 usage/environment."
# => a receipt whose output body is absent (or whitespace-only) is malformed/invalid => exit 1.
set -u
export TMPDIR=/fast/scratch/hyaku/chousa-r65/Probe19/tmp
SCRATCH=/fast/scratch/hyaku/chousa-r65/Probe19
CLONE="$SCRATCH/clone"
LANE=/home/vgpnk/Projects/shokunin/chousa-shokunin
REF="$LANE/corpus/evidence/round65/controls/ref-receipt-pin.py"
REV=f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd
RES="$SCRATCH/probe19-results.txt"

log(){ printf '%s\n' "$*"; printf '%s\n' "$*" >> "$RES"; }
: > "$RES"

log "PROBE19 no-body fixture"
log "ref=$REF"
log "freeze=$REV"
log "lane=$LANE"

# --- one live clone maximum, local source only, no network ---
rm -rf "$CLONE"
if ! git clone --quiet "$LANE" "$CLONE"; then log "SETUP-FAIL clone"; exit 2; fi
top="$(git -C "$CLONE" rev-parse --show-toplevel)"
if [ "$top" != "$CLONE" ]; then log "SETUP-FAIL toplevel=$top"; exit 2; fi
log "clone-toplevel=$top"
if ! git -C "$CLONE" cat-file -e "$REV:SKILL.md"; then log "SETUP-FAIL no SKILL.md at $REV"; exit 2; fi
h="$(git -C "$CLONE" cat-file blob "$REV:SKILL.md" | sha256sum | awk '{print $1}')"
log "blob=SKILL.md@$REV sha256=$h"

# --- receipts (exact bytes preserved; \n = LF) ---
printf 'REVISION=%s\nEXIT=0\nSHA256=%s SKILL.md\n\n' "$REV" "$h" > "$SCRATCH/probe19-nobody-receipt.txt"
printf 'REVISION=%s\nEXIT=0\nSHA256=%s SKILL.md\n\n   \n' "$REV" "$h" > "$SCRATCH/probe19-wsbody-receipt.txt"
printf 'REVISION=%s\nEXIT=0\nSHA256=%s SKILL.md\n\nmeasured output\n' "$REV" "$h" > "$SCRATCH/probe19-positive-receipt.txt"

run_case(){
  name=$1; f=$2; erc=$3; etok=$4
  out="$(python3 -B "$REF" --receipt "$f" --root "$CLONE" --revision "$REV" 2> "$SCRATCH/probe19-$name.stderr")"
  rc=$?
  log "---"
  log "CASE $name receipt=$f"
  sed 's/^/  receipt-bytes|/' "$f" >> "$RES"
  log "EXPECT rc=$erc stdout=[$etok]"
  log "GOT    rc=$rc stdout=[$out]"
  if [ "$rc" = "$erc" ] && [ "$out" = "$etok" ]; then
    log "CASE $name MATCH"
  else
    log "CASE $name MISMATCH"; fail=1
  fi
}

fail=0
run_case no-body  "$SCRATCH/probe19-nobody-receipt.txt"   1 "RECEIPT_PIN=FAIL header/body"
run_case ws-body  "$SCRATCH/probe19-wsbody-receipt.txt"   1 "RECEIPT_PIN=FAIL header/body"
run_case positive "$SCRATCH/probe19-positive-receipt.txt" 0 "RECEIPT_PIN=PASS"

log "---"
if [ "$fail" = 0 ]; then log "PROBE19_RESULT=PASS all observed outputs match independent expectations"
else log "PROBE19_RESULT=FAIL"; fi
exit "$fail"
