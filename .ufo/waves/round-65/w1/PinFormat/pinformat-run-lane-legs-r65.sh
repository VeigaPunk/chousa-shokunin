#!/bin/sh
# PinFormat lane legs: draft specimens, validate with the prefreeze reference, cite limits.
W=/fast/scratch/hyaku/chousa-r65/PinFormat
export TMPDIR=$W/tmp
LANE=/home/vgpnk/Projects/shokunin/chousa-shokunin
REF=$LANE/corpus/evidence/round65/controls/ref-receipt-pin.py
REV=f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd
TRANSCRIPT=$W/out/pinformat-lane-legs-transcript.txt
: > "$TRANSCRIPT"

run() {
  echo "== $1" >> "$TRANSCRIPT"
  shift
  "$@" >> "$TRANSCRIPT" 2>&1
  echo "invocation-rc=$?" >> "$TRANSCRIPT"
}

# Leg 1: draft positive specimen (measured child exits 0)
run leg1-draft-positive python3 "$W/pinformat-specimen-driver.py" \
  --root "$LANE" --revision "$REV" --path corpus/evidence/round65/claims.md \
  --child-exit 0 --out "$W/out/pinformat-positive.receipt"

# Leg 2: reference validates positive specimen
run leg2-ref-positive python3 "$REF" --receipt "$W/out/pinformat-positive.receipt" \
  --root "$LANE" --revision "$REV"

# Leg 3: draft failing-child specimen (measured child exits 7; receipt reports EXIT=7)
run leg3-draft-exit7 python3 "$W/pinformat-specimen-driver.py" \
  --root "$LANE" --revision "$REV" --path corpus/evidence/round65/claims.md \
  --child-exit 7 --out "$W/out/pinformat-exit7.receipt"

# Leg 4: reference validates the failing-child specimen (consistency, not pass/fail)
run leg4-ref-exit7 python3 "$REF" --receipt "$W/out/pinformat-exit7.receipt" \
  --root "$LANE" --revision "$REV"

# Leg 5: tampered digest (first hex nibble of digest flipped)
python3 - "$W/out/pinformat-positive.receipt" "$W/out/pinformat-digest-tampered.receipt" \
  >> "$TRANSCRIPT" 2>&1 <<'PYEOF'
import sys, pathlib
src, dst = sys.argv[1], sys.argv[2]
t = pathlib.Path(src).read_text()
i = t.index('SHA256=') + len('SHA256=')
flip = '0' if t[i] != '0' else '1'
pathlib.Path(dst).write_text(t[:i] + flip + t[i+1:])
PYEOF
echo "tamper-rc=$?" >> "$TRANSCRIPT"
run leg5-ref-tampered-digest python3 "$REF" --receipt "$W/out/pinformat-digest-tampered.receipt" \
  --root "$LANE" --revision "$REV"

# Leg 6: caller --revision differs from header REVISION
run leg6-ref-wrong-caller-revision python3 "$REF" --receipt "$W/out/pinformat-positive.receipt" \
  --root "$LANE" --revision d6ed8155e9b4735639a2cf0a3e479c62f2056195

# Leg 7: malformed caller --revision (uppercase) -> usage exit
run leg7-ref-uppercase-revision python3 "$REF" --receipt "$W/out/pinformat-positive.receipt" \
  --root "$LANE" --revision F99DE3BDFAAF9B4C4FA85CC55DD37B9DF2EE90FD

# Leg 8: forged body only (header untouched, body replaced with fabricated text)
python3 - "$W/out/pinformat-positive.receipt" "$W/out/pinformat-forged-body.receipt" \
  >> "$TRANSCRIPT" 2>&1 <<'PYEOF'
import sys, pathlib
src, dst = sys.argv[1], sys.argv[2]
t = pathlib.Path(src).read_text()
head, _sep, _body = t.partition('\n\n')
pathlib.Path(dst).write_text(head + '\n\n' + 'fabricated output never produced by any run\n')
PYEOF
echo "forge-rc=$?" >> "$TRANSCRIPT"
run leg8-ref-forged-body python3 "$REF" --receipt "$W/out/pinformat-forged-body.receipt" \
  --root "$LANE" --revision "$REV"

# Leg 9: CRLF copy of the positive specimen
python3 - "$W/out/pinformat-positive.receipt" "$W/out/pinformat-crlf.receipt" \
  >> "$TRANSCRIPT" 2>&1 <<'PYEOF'
import sys, pathlib
src, dst = sys.argv[1], sys.argv[2]
t = pathlib.Path(src).read_bytes().replace(b'\n', b'\r\n')
pathlib.Path(dst).write_bytes(t)
PYEOF
echo "crlf-rc=$?" >> "$TRANSCRIPT"
run leg9-ref-crlf python3 "$REF" --receipt "$W/out/pinformat-crlf.receipt" \
  --root "$LANE" --revision "$REV"

# Leg 10: absent receipt file
run leg10-ref-absent-receipt python3 "$REF" --receipt "$W/out/absent.receipt" \
  --root "$LANE" --revision "$REV"

echo "== transcript-complete" >> "$TRANSCRIPT"
