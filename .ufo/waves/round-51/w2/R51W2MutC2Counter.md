# R51W2MutC2Counter — mutation battery on the frozen C2 counter

Round 51 wave 2 (falsify), 2026-10-25. Attacked: `corpus/evidence/round51/c2-count.py`
(frozen counter of claim R51-C2, `corpus/evidence/round51/claims.md`), on real lane bytes.
Method: scratch copy at `/dev/shm/chousa-r51-R51W2MutC2Counter/root` (real dirs, `cp -r`;
pristine snapshot at `.../pristine`); each mutant applied to the copy only, detector run with
`--root`, bytes restored from the snapshot, restoration hash-compared against the snapshot.
Tooling: no installs (python3 + the frozen counter only); every run `env -u ASSIMILATE_CITES`;
no network, no writes outside this report and `/dev/shm/chousa-r51-R51W2MutC2Counter`.

## Setup and pristine baseline

```
R=/dev/shm/chousa-r51-R51W2MutC2Counter; L=/home/vgpnk/Projects/shokunin/chousa-shokunin
mkdir -p $R/root/corpus/knowledge $R/root/corpus/lessons $R/root/corpus/evidence/round51 $R/root/tools
cp -r $L/corpus/evidence/round51/. $R/root/corpus/evidence/round51/
cp $L/corpus/knowledge/japanese-search-record-r38.md $L/corpus/knowledge/chinese-search-record-r39.md \
   $L/corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md $R/root/corpus/knowledge/
cp $L/corpus/SOURCES.md $R/root/corpus/SOURCES.md
cp $L/corpus/lessons/round-51.md $R/root/corpus/lessons/round-51.md
cp $L/tools/inference-ground.py $R/root/tools/inference-ground.py
cp -r $R/root $R/pristine
```

```
$ env -u ASSIMILATE_CITES python3 $L/corpus/evidence/round51/c2-count.py --root $R/root; echo rc=$?
ENTRIES=3/3
BOUND=6/7 (min 5) REFUSED=1
BOUND_IDS=S107,S108,S109,S110,S111,S112
REF_ID_UNBOUND=0
NEW_GROUND=3/3
QUOTE_ROWS=61 ON_BOUND=61/61
SPAN_IDS=6/6 (min 3 each)
QUOTES_IN_SPAN=61/61
QUOTES_IN_ENTRY=61/61
QUOTES_IN_LESSON=61/61
QUOTE_SHORT=61/61
SPAN_CONTEXT=61/61
CAPTURE_BOUND=61/61
SUBSTANCE=PASS
ANCHOR_BOUND=6/6
INFERENCE_GROUNDED=3/3
QUARANTINE_VERDICTS=6/6 (S104,S105,S111,S112,S114,S120)
QUARANTINE_BLOCKED_ADOPTED=0
C2=PASS
rc=0
```
Detector conclusive on pristine bytes. (First scratch build mis-copied evidence/ one level up and
printed QUOTE_ROWS=0 C2=FAIL; rebuilt and re-ran — harness error, not a counter defect.)

## Battery — mutate → run → restore; sha256 prefixes restored-vs-pristine
**M1 shift one `char N` in a bound row's anchor (SOURCES.md S112: `char 10140`→`char 10141`).**
`ANCHOR_BOUND=5/6` `C2=FAIL` rc=1 — KILLED (char no longer an offset of an S107..S112 quote).
Restored: `6cfb1a21d0c6c566` = pristine `6cfb1a21d0c6c566`.
**M2 change one quote character in an entry (E_JA `か，その日時`→`か、その日時`, manifest row 1).**
`QUOTES_IN_ENTRY=60/61` `SUBSTANCE=PASS` `INFERENCE_GROUNDED=3/3` `C2=FAIL` rc=1 — KILLED by the
entry-containment leg alone (inference-ground did not catch this quote).
Restored: `870ca1a962b3b36c` = pristine `870ca1a962b3b36c`.
**M3 swap two lane ids in `source:` lines (E_JA S107↔S108, URLs left in place).**
`BOUND=4/7 (min 5) REFUSED=1` `BOUND_IDS=S109,S110,S111,S112` `REF_ID_UNBOUND=24` `C2=FAIL` rc=1 —
KILLED (the cites check `source: <bound id> — <url>` fails for both docs; the freed ids become
unbound tokens). Restored: `870ca1a962b3b36c` = pristine `870ca1a962b3b36c`.
**M4 widen a used-by cell (SOURCES.md S109 used-by += `, corpus/knowledge/japanese-search-record-r38.md`).**
`BOUND=5/7 (min 5) REFUSED=1` `BOUND_IDS=S107,S108,S110,S111,S112` `SPAN_IDS=5/5` `ANCHOR_BOUND=5/5`
`C2=FAIL` rc=1 — KILLED, but note how: every printed ratio still reads 5/5; the kill is the
predicate arithmetic `nbound + refused == 7` (5+1=6), i.e. "used-by names EXACTLY the citing
entries", visible only via BOUND_IDS dropping S109. Over-wide used-by cannot pass.
Restored: `6cfb1a21d0c6c566` = pristine `6cfb1a21d0c6c566`.
**M5 delete the refused-doc line (lesson line 56, `refused-doc: https://c2h.niph…docx …`).**
`BOUND=6/7 (min 5) REFUSED=0` `QUOTES_IN_LESSON=61/61` `C2=FAIL` rc=1 — KILLED (6+0≠7). The prose
"Refused document (no lane row)" paragraph on line 54 does not satisfy the leg; only the exact
`refused-doc` + URL line does. Restored: `8969378368d64bcc` = pristine `8969378368d64bcc`.
**M6 change one verdict line to a malformed one (lesson `register S104 (round 3) verdict:` value → `checked`).**
`QUARANTINE_VERDICTS=5/6 (S104,S105,S111,S112,S114,S120)` `C2=FAIL` rc=1 — KILLED (the regex needs
present|absent-as-written|unverifiable|fabricated; the missing count fails
`len(verdicts)==len(reg_ids)`). Restored: `8969378368d64bcc` = pristine `8969378368d64bcc`.
**M7 rename an entry file (`japanese-search-record-r38-amendment-2026-10-23.md` → `.md.mut`).**
`ENTRIES=2/3` `NEW_GROUND=2/3` `INFERENCE_GROUNDED=2/3` `C2=FAIL` rc=1 — KILLED.
Restored (moved back): `37228fad1677ee67` = pristine `37228fad1677ee67`.
**M8 drop one spans.tsv row (deleted row 1: `spans/S107-1.txt`, the か，その日時… quote; S107 16→15).**
`QUOTE_ROWS=60 ON_BOUND=60/60` `SPAN_IDS=6/6 (min 3 each)` `ANCHOR_BOUND=6/6` `C2=PASS` rc=0 —
**SURVIVOR.** Every leg recomputes over the shrunken n; the ≥3-per-id quota still holds, and every
anchor char is contributed by another row (char 10234 = `spans/S107-5.txt` at offset 10234), so the
anchor leg does not miss the deleted offset. Blind spot: the counter never reads `quotes.tsv` or the
lesson's "All located quotes" section, so it cannot detect loss of any individual manifest row while
the quota holds — the 61-row manifest could shrink to exactly 3 per id (18 rows) and still print
C2=PASS. Coverage finding, not a contract change: the frozen predicate says "at least three per id".
**M9 reorder quotes (swapped manifest rows 1 and 2: spans/S107-1.txt ↔ spans/S107-2.txt).**
`SUBSTANCE=PASS` `CAPTURE_BOUND=61/61` `C2=PASS` rc=0 — **SURVIVOR.** The counter is
order-insensitive (per-row checks; offsets accumulated into a set). Row order is not part of the
frozen predicate, so benign — but manifest rows can be shuffled without detection.
**M10 edit a span file by one byte (appended `x` to `spans/S107-1.txt`, 184→185 bytes).**
`QUOTES_IN_SPAN=61/61` `SPAN_CONTEXT=61/61` `CAPTURE_BOUND=60/61` `C2=FAIL` rc=1 — KILLED by the
capture-slice leg only (quote still in span; only `ft[o:o+len(span)] == span` fails).
Supplementary probe: same mutant with `--lane-only` → `CAPTURE_BOUND=skipped` `C2=PASS` rc=0, i.e.
M10 survives lane-only mode. That is a declared weakness (docstring: "invented spans/digests pass
`--lane-only` and fail `CAPTURE_BOUND`"), and the frozen counting command runs without `--lane-only`.
Restored: `bb8d1c11ca01fc30` = pristine `bb8d1c11ca01fc30`.

## Score

8/10 killed (M1 M2 M3 M4 M5 M6 M7 M10), 2 survivors (M8 M9), 0 inconclusive (baseline passed).
Survivors are counter blind spots, not contract defects: (a) no leg cross-checks spans.tsv against
quotes.tsv or the lesson's located-quote section, so row loss above the 3-per-id quota is invisible;
(b) row order is unobserved; (c) M10 additionally survives the declared `--lane-only` mode.

## Restoration and cleanup evidence

After the battery: `diff -r root pristine` → `ROOT==PRISTINE` (empty diff); detector re-run on the
restored root → `C2=PASS` rc=0. Lane tree untouched by this seat: `git -C $L status --porcelain`
shows only pre-existing wave-management entries (`.ufo/waves/round-51/w2*` untracked, w1 seat file
modified by others); no production file, index, or sibling report written. Scratch
`/dev/shm/chousa-r51-R51W2MutC2Counter` deleted after this report was written (verified absent).

VERDICT: attacked the frozen C2 counter with 10 byte-level mutants on a scratch copy — 8 killed with
the exact failing leg identified, 2 survivors named as blind spots (manifest row loss above quota;
row order), lane bytes untouched, all mutants restored hash-exact.
