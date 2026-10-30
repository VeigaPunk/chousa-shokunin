#!/bin/sh
# PinFormat working-tree-divergence probe: receipt pins the committed blob while the
# fixture working tree is tampered; demonstrates the reference does no working-tree hashing.
W=/fast/scratch/hyaku/chousa-r65/PinFormat
export TMPDIR=$W/tmp
LANE=/home/vgpnk/Projects/shokunin/chousa-shokunin
REF=$LANE/corpus/evidence/round65/controls/ref-receipt-pin.py
F=$W/fixture
TRANSCRIPT=$W/out/pinformat-fixture-leg-transcript.txt
: > "$TRANSCRIPT"

rm -rf "$F"
mkdir -p "$F"
cd "$F" || exit 9
git init -q . || exit 9

TL=$(git rev-parse --show-toplevel)
echo "toplevel=$TL" >> "$TRANSCRIPT"
if [ "$TL" != "$F" ]; then
  echo "TOPLEVEL-MISMATCH-ABORT" >> "$TRANSCRIPT"
  exit 9
fi

printf 'pinned content\n' > target.txt
git add target.txt
git -c user.email=pinformat@seat.local -c user.name=PinFormat commit -qm pin
REV=$(git rev-parse HEAD)
echo "fixture-rev=$REV" >> "$TRANSCRIPT"

printf 'tampered working tree bytes\n' > target.txt
echo "working-sha=$(sha256sum target.txt | cut -d' ' -f1)" >> "$TRANSCRIPT"

echo "== draft receipt pinning committed blob" >> "$TRANSCRIPT"
python3 "$W/pinformat-specimen-driver.py" --root "$F" --revision "$REV" \
  --path target.txt --child-exit 0 --child-text 'fixture measured output' \
  --out "$W/out/pinformat-wt-divergence.receipt" >> "$TRANSCRIPT" 2>&1
echo "driver-rc=$?" >> "$TRANSCRIPT"

echo "== validate against tampered working tree" >> "$TRANSCRIPT"
python3 "$REF" --receipt "$W/out/pinformat-wt-divergence.receipt" --root "$F" --revision "$REV" >> "$TRANSCRIPT" 2>&1
echo "validator-rc=$?" >> "$TRANSCRIPT"
echo "== transcript-complete" >> "$TRANSCRIPT"
