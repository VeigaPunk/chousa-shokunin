# R57W1CritC3Held — R57-C3 do-nothing controls + strongest local attack

Seat item: build the HELD do-nothing control, the CITER variant, and attack the BOUND>=4 gate with the
strongest counterexample available from committed bytes. Frozen claims/counters untouched; all work in
/fast/scratch/hyaku/chousa-r57/R57W1CritC3Held (clone + fixtures), scratch deleted after the run.
Only lane write: this report. No network fetches; quotes taken from committed capture forms only.

## Axes (godspeed)
- Falsification power: can any do-nothing fixture reach BOUND>=4 under the frozen counter?
- Fidelity: do my scratch-built controls reproduce controls/c3-controls.txt exactly?
- Calibration: are the claim's disclosed pre-freeze statements accurate against the committed store?

## Setup
- `git clone /home/vgpnk/Projects/shokunin/chousa-shokunin` → scratch/lane-clone (HEAD e0e73e0; C2 receipt).
- Fixture builder (critic-authored, mirrors the HELD/CITER shape; quotes selected from committed `.txt`
  forms with the exact-once rule + unique-line fallback) → `$S/HELD`, `$S/CITER`; spans via the lane's own
  `tools/build-spans.py --cache <fixture>/corpus/captures`.
- Quote-uniqueness probe on committed forms: S127 clause quote count=1; S118 title quotes count=2
  (fallback to unique full line); S130 count=1; S990 R1-title quote count=0 (note renders the title with
  spaced CJK) → skipped, leaving 1 S990 quote — matches CITER's expected QUOTE_ROWS=6.

## HELD under the frozen counter
`python3 corpus/evidence/round57/c3-count.py --root $S/HELD` (counter run from the lane, unmodified):
```
ENTRY=yes S127_CITED=yes NEW_GROUND=yes CLAUSE=yes
BOUND=1/7 (min 4) R7:S118
SWEPT=6/6 R1 R2 R3 R4 R5 R6
QUOTE_ROWS=5 IN_SPAN=5 IN_ENTRY=5 IN_LESSON=5 SHORT=5 CONTEXT=5 CAPTURE_BOUND=5
SUBSTANCE=PASS ANCHOR_BOUND=0/0 INFERENCE_GROUNDED=no STRAY_IDS=S130
C3=FAIL
exit=1
```
Matches controls/c3-controls.txt HELD block byte-for-byte.

## CITER under the frozen counter
Same command with `--root $S/CITER`:
```
ENTRY=yes S127_CITED=yes NEW_GROUND=yes CLAUSE=yes
BOUND=1/7 (min 4) R7:S118
SWEPT=6/6 R1 R2 R3 R4 R5 R6
QUOTE_ROWS=6 IN_SPAN=6 IN_ENTRY=6 IN_LESSON=6 SHORT=6 CONTEXT=6 CAPTURE_BOUND=6
SUBSTANCE=PASS ANCHOR_BOUND=0/0 INFERENCE_GROUNDED=no STRAY_IDS=S130,S990
C3=FAIL
exit=1
```
Matches the frozen CITER block byte-for-byte.

## EXCLUDED-by-URL question (seat-required read)
The S127 explanatory note's URL `https://www.ttbz.org.cn/upload/file/20250407/6387963977456239722441041.pdf`
(S128/S990 key de9f5afc3809acbf61f4d5bb) IS in `EXCLUDED_URLS` (c3-count.py:65) → the note row can never be
a binding candidate. Counterfactual tested anyway: copied the counter into the scratch clone (permitted
mutation), deleted line 65, reran on CITER — S990 becomes a candidate but binds nothing:
```
BOUND=1/7 (min 4) R7:S118 ... STRAY_IDS=S130,S990 ... C3=FAIL  exit=1
```
Consistent with the note's own form: it holds all six titles only inside 《》 citations / `[n]` reference
lines (heading rule fails: bad prefix chars / prefix >16) and lacks the R1/R2 tokens entirely
(`〔2019〕80号`, `〔2021〕16号` absent; `2021年版`/`2022年版`/`2024年版` present as citations).

## Strongest local attack — GRAY (register S132/S133 as mined rows on this round's committed captures)
Store-wide heading scan (counter's own `heading_title` + token test over all 60 raws: 56 `.txt` + 4 OLE/zip
through `capture-text.py`) found reference headings ONLY in: S118 (R7), S132/a476f41… (R2+R3),
S133/6f545e… (R3). No R1, R4, R5, R6 headings anywhere in the store. S132/S133 are C2 evidence captures
with NO registry row (not held rows), so the strict do-nothing ceiling stays 1; but a gray do-nothing can
register them `mined`/2026-10-27 on the already-committed bytes (zero new fetches). Fixture GRAY does
exactly that, with rows inserted INSIDE the `## Registry` section:
```
BOUND=3/7 (min 4) R2:S132 R3:S132 R7:S118
SWEPT=4/4 R1 R4 R5 R6
QUOTE_ROWS=8 IN_SPAN=8 IN_ENTRY=8 IN_LESSON=8 SHORT=8 CONTEXT=8 CAPTURE_BOUND=8
SUBSTANCE=PASS ANCHOR_BOUND=1/1 INFERENCE_GROUNDED=no STRAY_IDS=S130,S133
C3=FAIL  exit=1
```
S133 fails only MIN_PER_ID (1 unique quote in its form) and stays stray. Ceiling = 3 distinct refs
{R2,R3,R7} < 4: even the strongest committed-bytes attack cannot reach the gate.

## Calibration findings (reported, not patched — freezes stand)
1. `controls/build-c3-controls.py` appends the CITER S990 row at end-of-file — OUTSIDE the `## Registry`
   section (SOURCES.md: Registry ends line 141, `## Paths` at 142) — so `registry()` never parses it and
   the canonical CITER note row is inert as a candidate. The intended risk is only exercised by my
   un-exclusion counterfactual above (still BOUND=1). Smallest safe correction (if the L1 wants the
   control to mean what the seat text says): insert the S990 row before the `## Paths` heading.
2. claims.md's pre-freeze sentence "on the held captures it finds a heading only in S118 (R7) and S130
   (R3's title, without the 2021年版 token)" is accurate for registry-HELD rows; note for precision that
   evidence captures S132/S133 (no registry row, fetched this round) also carry R2/R3 headings with tokens
   — which is why the gray attack above reaches 3, not 1. Threshold 4 still clears it by one.

## Hygiene
- `git status` in the lane before reporting: my only lane write is this file; all fixtures/clone lived in
  scratch and were removed (`rm -rf /fast/scratch/hyaku/chousa-r57/R57W1CritC3Held` — no trap needed,
  deleted by hand after the report was written; nothing >50MB touched /tmp; TMPDIR/PYTHONDONTWRITEBYTECODE
  exported in every driver run).
- Frozen counters never edited; the only mutated copy (EXCLUDED_URLS minus the note URL) ran inside the
  scratch clone, never against the lane.

VERDICT: Attacked R57-C3's BOUND>=4 gate with the HELD/CITER do-nothing controls (both reproduce the
frozen expected outputs, BOUND=1/7 C3=FAIL) and with the strongest local gray attack (S132/S133 mined on
committed captures → BOUND=3/7 C3=FAIL); no do-nothing reaches 4 — the claim survives; the two calibration
notes above are reported, not patched.
