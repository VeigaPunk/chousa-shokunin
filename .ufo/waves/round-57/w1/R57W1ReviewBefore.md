# R57W1ReviewBefore — re-derivation of R57 before receipts and controls in scratch

Seat: leaf reviewer (no subagent dispatch). Scope: re-derive the R57-C2 / R57-C3 before receipts and
controls receipts from the frozen counter bytes at their freeze commits; diff against the committed
receipts. No lane writes; scratch only (deleted before yield — `rm -rf /fast/scratch/hyaku/chousa-r57/R57W1ReviewBefore`).

Tooling: none installed (no upgrade needed). Used system `git`, `python3` 3.x, `pdftotext 26.08.0` (already present).

## Method

```
S=/fast/scratch/hyaku/chousa-r57/R57W1ReviewBefore; mkdir -p "$S"; cd "$S"
export TMPDIR="$S" PYTHONDONTWRITEBYTECODE=1
git clone --shared /home/vgpnk/Projects/shokunin/chousa-shokunin "$S/lane"   # master tip e0e73e0f
git -C "$S/lane" checkout -q c2f914c53201a8f8ee4fef823b82681051d55592      # R57-C2 freeze
python3 "$S/lane/corpus/evidence/round57/c2-count.py"; echo "EXIT=$?"
git -C "$S/lane" checkout -q fd95724d56a33ad150cd263f8add2ce1f3425e6c      # R57-C3 freeze (see D1)
python3 "$S/lane/corpus/evidence/round57/c3-count.py"; echo "EXIT=$?"
git -C "$S/lane" checkout -q master
python3 "$S/lane/corpus/evidence/round57/controls/build-c2-controls.py" "$S/fix2"
python3 "$S/lane/corpus/evidence/round57/controls/build-c3-controls.py" "$S/fix3"
# then c2-count --root / c3-count --root on each fixture
```

## Findings

### C2 before receipt — SURVIVES

Run at freeze commit c2f914c53201a8f8ee4fef823b82681051d55592:

```
SET=47 VERDICTS=0/47 REPRODUCED=0 DRIFTED=0 UNREACHABLE=0 BYTE_BACKED=0 CONSISTENT=0/0 FLAGGED=0/0 C2=FAIL
EXIT=1
```

`diff` of this output against the blob
`c2f914c:corpus/evidence/round57/controls/c2-before.txt` differs only by the receipt's own annotation
lines (`# R57-C2 before: …` header, `exit=1` trailer); the counter line is byte-identical. Matches the
claims.md before profile `SET=47 VERDICTS=0/47 REPRODUCED=0 … C2=FAIL`, exit 1.

### C3 before receipt — SURVIVES

Run at freeze commit fd95724d56a33ad150cd263f8add2ce1f3425e6c:

```
ENTRY=no S127_CITED=no NEW_GROUND=no CLAUSE=no
BOUND=0/7 (min 4) -
SWEPT=0/7 -
QUOTE_ROWS=0 IN_SPAN=0 IN_ENTRY=0 IN_LESSON=0 SHORT=0 CONTEXT=0 CAPTURE_BOUND=0
SUBSTANCE=FAIL ANCHOR_BOUND=0/0 INFERENCE_GROUNDED=no STRAY_IDS=-
C3=FAIL
EXIT=1
```

`diff` against `fd95724:corpus/evidence/round57/controls/c3-before.txt` (after stripping `# ` header and
`exit=1` trailer) = clean. Matches the claims.md before profile `ENTRY=no … BOUND=0/7 … C3=FAIL`, exit 1.

### C2 controls — SURVIVE

Rebuilt EMPTY/JUNK/ALLFAIL fixtures with the frozen builder at master tip (pdftotext 26.08.0 present) and
ran `c2-count.py --root` on each; all three lines match the committed `c2-controls.txt` byte-for-byte,
each exit=1:

```
EMPTY:   SET=47 VERDICTS=0/47 REPRODUCED=0 DRIFTED=0 UNREACHABLE=0 BYTE_BACKED=0 CONSISTENT=0/0 FLAGGED=0/0 C2=FAIL
JUNK:    SET=47 VERDICTS=47/47 REPRODUCED=0 DRIFTED=47 UNREACHABLE=0 BYTE_BACKED=47 CONSISTENT=47/47 FLAGGED=0/47 C2=FAIL
ALLFAIL: SET=47 VERDICTS=47/47 REPRODUCED=0 DRIFTED=0 UNREACHABLE=47 BYTE_BACKED=0 CONSISTENT=0/0 FLAGGED=0/0 C2=FAIL
```

No control meets the target, as claimed.

### C3 controls — SURVIVE

Rebuilt HELD/CITER fixtures (builder rc 0 both) and ran `c3-count.py --root`; both match the committed
`c3-controls.txt` byte-for-byte, each exit=1:

```
HELD:  ENTRY=yes … CLAUSE=yes / BOUND=1/7 (min 4) R7:S118 / SWEPT=6/6 R1 R2 R3 R4 R5 R6 /
       QUOTE_ROWS=5 (all 5s) / SUBSTANCE=PASS ANCHOR_BOUND=0/0 INFERENCE_GROUNDED=no STRAY_IDS=S130 / C3=FAIL
CITER: same, QUOTE_ROWS=6, STRAY_IDS=S130,S990 / C3=FAIL
```

## Notes (not defects in the frozen artifacts)

- At fd95724, `corpus/evidence/round57/refetch.tsv` and all of `corpus/captures/` are absent from git
  (they land in f9736a3, the L1 pass-1 commit). The c3-controls fixtures are built from lane working-tree
  capture bytes, so the committed c3-controls receipt necessarily reflects the then-working-tree bytes;
  re-derivation at master reproduces it exactly, so the receipt is consistent with the frozen counter.
- Live lane master = e0e73e0f (C2 after-receipt commit: 41 REPRODUCED / 5 DRIFTED / 1 UNREACHABLE S105,
  C2=PASS), ahead of the dispatch tip f9736a39; working tree shows in-flight refetch.tsv edits and peer
  wave reports, as expected mid-wave.

## D1 (reported, not patched — seat text vs lane): freeze-hash transcription

My seat text names the R57-C3 freeze commit `fd95724d56a33a150cd2638fadd2ce1f3425e6c`; no such object
exists (`git cat-file -t` → fatal). The actual R57-C3 freeze commit is
`fd95724d56a33ad150cd263f8add2ce1f3425e6c` (`round-57: freeze R57-C3 …`). The R57-C2 hash
`c2f914c53201a8f8ee4fef823b82681051d55592` checks out verbatim. The lane's claims.md does not itself
print either freeze hash, so this is a dispatch/seat-text transcription slip only; the lane's frozen
bytes, receipts and controls are internally consistent.

## VERDICT

Attacked the R57 before/controls receipts by re-deriving them from the frozen counters at the freeze
commits (c2-before, c3-before, C2 EMPTY/JUNK/ALLFAIL, C3 HELD/CITER): all six receipts SURVIVE
byte-identical reproduction; one seat-text hash transcription error reported (D1, not a lane defect).
