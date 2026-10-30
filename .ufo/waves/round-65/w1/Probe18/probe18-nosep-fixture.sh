#!/usr/bin/env bash
# Probe18 isolated fixture: receipt-pin no-separator surface.
# Lane freeze: f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd
# Reference: corpus/evidence/round65/controls/ref-receipt-pin.py (production tools/receipt-pin.py absent at freeze)
set -u
ROOT=/fast/scratch/hyaku/chousa-r65/Probe18
CLONE=$ROOT/lane
REV=f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd
REF=/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round65/controls/ref-receipt-pin.py
TARGET=corpus/evidence/round65/claims.md
export TMPDIR=$ROOT/tmp
LOG=$ROOT/probe18-nosep-run.log
: > "$LOG"

DIGEST=$(git -C "$CLONE" cat-file blob "$REV:$TARGET" | sha256sum | cut -d' ' -f1)

# v0: valid control WITH empty separator (harness sanity: digest/path/revision all correct)
printf 'REVISION=%s\nEXIT=0\nSHA256=%s %s\n\nfirst output line\nsecond output line\n' "$REV" "$DIGEST" "$TARGET" > "$ROOT/v0-valid-separator.receipt"

# v1: NO separator, 2 body lines (isolates the separator rule; len(lines)>=5)
printf 'REVISION=%s\nEXIT=0\nSHA256=%s %s\nfirst output line\nsecond output line\n' "$REV" "$DIGEST" "$TARGET" > "$ROOT/v1-nosep-2body.receipt"

# v2: NO separator, 1 body line (len(lines)==4 <5, same defect class)
printf 'REVISION=%s\nEXIT=0\nSHA256=%s %s\nfirst output line\n' "$REV" "$DIGEST" "$TARGET" > "$ROOT/v2-nosep-1body.receipt"

run_case() {
  name=$1
  {
    echo "=== $name ==="
    echo "receipt-bytes:"; cat -A "$ROOT/$name.receipt"
    echo "argv: python3 $REF --receipt $ROOT/$name.receipt --root $CLONE --revision $REV"
  } >> "$LOG"
  python3 "$REF" --receipt "$ROOT/$name.receipt" --root "$CLONE" --revision "$REV" > "$ROOT/$name.stdout" 2> "$ROOT/$name.stderr"
  rc=$?
  {
    echo "exit=$rc"
    echo "stdout: $(cat "$ROOT/$name.stdout")"
    echo "stderr: $(cat "$ROOT/$name.stderr")"
  } >> "$LOG"
}

run_case v0-valid-separator
run_case v1-nosep-2body
run_case v2-nosep-1body
cat "$LOG"
