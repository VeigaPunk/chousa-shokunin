# R50MutStaleCount — mutation test: `corpus/evidence/round50/stale-count-check.py` (round 50, w2)

8 single-point mutants vs pristine on lane bytes, in two prose states — after (lane tree, HEAD `c5b8dca85f759c7a772225fe036e7bb9a809b91c`) and before (same minus the 3 correction
lines: `QUALITY.md:786`, `README.md:1083`, `round-49.md:220`) — plus targeted probes where lane bytes mask a mutant. Lane never written; every run on copies under
`/dev/shm/chousa-r50-R50MutStaleCount` via `--root` (deleted at end). No tools installed (none needed; pacman paused host-wide).

## Setup
- Copied into `$S/root/`: `corpus/evidence/round50/stale-count-check.py`, `corpus/QUALITY.md`, `corpus/README.md`, `LOG.md`, `corpus/lessons/round-49.md`, `corpus/evidence/round49/spans.tsv`; `$S/root2` = copy with the 3 correction lines deleted.
- Receipt: `$ awk 'NF' spans.tsv | wc -l` → 32, row 1 = `id⇥url⇥…` header → `RECEIPT_ROWS=31`.
- Pristine digests (sha256sum; identical after all work, see Restoration):
```
4273436ac915ab47a3dc56148bb14827dbde0cd48cbf477bc85ef5331fcbecd9  corpus/evidence/round50/stale-count-check.py
ab1370d62c66bbf69b82a4b5c0ef5cae51754f30a1376f1671394dee78e5c44d  corpus/QUALITY.md
3a4bee523d814f12de9a3f14592e0e5a55b1801ced180bf99f90a2694ada7fad  corpus/README.md
37e0d02cd82c467c70365fd505f459bc785644011008412f4d4b7bbf297734a6  LOG.md
49af6a2afb18d90c35e78518877376a52cbfcf8dec9d8f6fcf95810f930efde2  corpus/lessons/round-49.md
96bc0bebcacf8a880736cdace6dd24d1a74645af7509c4068c21878d41a06472  corpus/evidence/round49/spans.tsv
```

## Pristine baselines
`$ python3 stale-count-check.py --root $S/root` (after) — exit 1:
```
RESOLVED corpus/QUALITY.md:746 says 28, receipt 31
RESOLVED corpus/QUALITY.md:786 says 28, receipt 31
RESOLVED corpus/README.md:1074 says 28, receipt 31
STALE corpus/README.md:1080 says 55, receipt 31
RESOLVED corpus/README.md:1083 says 28, receipt 31
STALE LOG.md:1803 says 28, receipt 31
RESOLVED corpus/lessons/round-49.md:20 says 28, receipt 31
RESOLVED corpus/lessons/round-49.md:220 says 28, receipt 31
STALE_HITS=8 UNRESOLVED=2 RECEIPT_ROWS=31
STALE_COUNT=FAIL
```
`--root $S/root2` (before) — exit 1: `STALE QUALITY.md:746 says 28` / `STALE README.md:1074 says 28` / `STALE README.md:1080 says 55` / `STALE LOG.md:1803 says 28` / `STALE round-49.md:20 says 28` (all "receipt 31") `STALE_HITS=5 UNRESOLVED=5 RECEIPT_ROWS=31` `STALE_COUNT=FAIL`.

**Baseline defects found (beside the probe):**
- **B1** The after-state FAILS on today's bytes: `UNRESOLVED=2`. (a) `README.md:1080` "55-row manifest" describes round-50's manifest, but the check pins one receipt (round-49, 31) → cross-receipt false stale (the criterion's own named limit "one receipt per scan" biting the lane's own README row). (b) `LOG.md:1803 says 28` is genuinely stale (28→31) and LOG.md carries no correction line (`$ grep -c 'correction:.*superseded by' LOG.md` → 0 matches). So QUALITY.md:782-783's "after them `STALE_COUNT=PASS`, exit 0 (`stale-count-after.txt`)" is false on current bytes, and the cited file does not exist: `corpus/evidence/round50/` holds only `stale-count-before.txt` + `stale-count-check.py` (glob), the staged package has none (glob `merge/chousa/**/stale-count*` → none), and `claims.md`/`claims-erratum.md` never mention stale-count (grep → 0).
- **B2** The frozen before-capture no longer matches lane bytes: `stale-count-before.txt` shows 4 STALE, all "says 28"; today's before-state shows 5 STALE including "README.md:1080 says 55" → the README round-50 index row landed after that capture.
The detector itself functions (well-formed STALE/RESOLVED lines, correct exit codes), so the mutant comparisons below are conclusive.

## Mutants (scratch copies)
- **m1** `said()`: `n != m` → `n == m`
- **m2** elif-branch drops `i in named[j]` — correction accepted without naming the stale line
- **m3** resolution also accepted from a correction in ANY file, position ignored (cross-file pool; mutated file written whole to scratch)
- **m4** `PATTERNS` drops `CAPTURE_BOUND=(\d+)/\1`
- **m5** `PROSE` drops `corpus/lessons/round-49.md`
- **m6** elif-branch drops `set(nums[j-1]) <= quoted[j]` — correction may quote a NEW disagreeing value
- **m7** missing-receipt `return 2` → `return 0`
- **m8** `receipt_rows` returns `len(rows)` — header counted

## Kill matrix (exit/UNRESOLVED; IDENTICAL = byte-identical stdout+exit)
| m  | after (root) | before (root2) | targeted probe | verdict |
|----|--------------|----------------|----------------|---------|
| m1 | DIFFERS 1/2→1/2 (hits 8→2: flags the two `QUOTES=31` quotes at QUALITY:786, round-49:220) | DIFFERS 1/5→0/0 PASS | — | KILLED |
| m2 | DIFFERS 1/2→1/1 (README:1080 STALE→RESOLVED via correction naming 1074) | DIFFERS 1/5→1/4 (QUALITY:746 RESOLVED via criterion-74 prose line 780, which matches CORRECTION but names/quotes nothing) | — | KILLED |
| m3 | IDENTICAL | IDENTICAL | fx3b: pristine 1/1 → mut3 0/0 | KILLED (masked on lane) |
| m4 | IDENTICAL (LOG:1803's 28 also matched by "28 located quotes") | IDENTICAL | fx4: pristine 1/1 → mut4 0/0 | KILLED (masked on lane) |
| m5 | DIFFERS hits 8→6 | DIFFERS 5→4 | — | KILLED |
| m6 | IDENTICAL | IDENTICAL | fx6: 1/2 → 1/1 (LOG:1 STALE→RESOLVED; exit 1 both) | KILLED (masked on lane) |
| m7 | IDENTICAL | IDENTICAL | `--receipt absent`: pristine exit 2 → mut7 exit 0 | KILLED (masked on lane) |
| m8 | DIFFERS 1/2→1/6 (receipt 32; `QUOTES=31` quotes become STALE) | DIFFERS (receipt 32) | — | KILLED |

**SURVIVORS: none.** Masked on lane bytes: m3, m4, m6, m7 — today's bytes alone cannot distinguish them (coverage note, not a check defect).

## Probe transcripts
fx3b (cross-file: `QUALITY.md:1`=`QUOTES=54`; `LOG.md:1`=`QUOTES=54`, `:2`=`correction: line 1 (QUOTES=54) superseded by the recount`; receipt 55 rows):
```
pristine: STALE corpus/QUALITY.md:1 says 54, receipt 55 / RESOLVED LOG.md:1… / RESOLVED LOG.md:2… / UNRESOLVED=1 → exit 1
mut3:     RESOLVED corpus/QUALITY.md:1 says 54, receipt 55 / … / UNRESOLVED=0 STALE_COUNT=PASS → exit 0
```
fx4 (`README.md:1`=`CAPTURE_BOUND=30/30`, receipt 31): pristine `STALE corpus/README.md:1 says 30, receipt 31 / UNRESOLVED=1` exit 1; mut4 `STALE_HITS=0 UNRESOLVED=0 RECEIPT_ROWS=31 / STALE_COUNT=PASS` exit 0.
fx6 (`LOG.md:1`=`QUOTES=54`; `:2`=`correction: LOG.md:1 (QUOTES=54) superseded by QUOTES=53`; receipt 55):
```
pristine: STALE LOG.md:1 says 54 / RESOLVED LOG.md:2 says 54 / STALE LOG.md:2 says 53 / UNRESOLVED=2 → exit 1
mut6:     RESOLVED LOG.md:1 says 54 / RESOLVED LOG.md:2 says 54 / STALE LOG.md:2 says 53 / UNRESOLVED=1 → exit 1 (stdout differs)
```
receipt-missing (`--receipt $S/absent.tsv` on root): pristine `RECEIPT_MISSING …` exit 2; mut7 `RECEIPT_MISSING …` exit 0.
Note: fx3 (first attempt) was misbuilt — its correction named LOG's own line 1, which says 55, so quoted[2]=∅ and even pristine flagged it; rebuilt as fx3b above. m1/m8 show the corrections quote the new value in `QUOTES=31` form; pristine tolerates that only because 31 == m.

## Restoration
`$ sha256sum` of all six lane files after every run → the same six digests as Setup, byte for byte; `$ cmp` lane vs `$S/root` copy → "same" ×6. Lane HEAD unchanged (`c5b8dca8…`). Scratch removed: `rm -rf /dev/shm/chousa-r50-R50MutStaleCount`.

## Tooling
No install or upgrade performed (none required).

**VERDICT:** attacked `stale-count-check.py` with 8 mutants — 0 survivors (4 killed on lane bytes, 4 by targeted probes: cross-file resolution, CAPTURE_BOUND-only, new-value-in-correction, missing-receipt); the check survives, but the pristine baseline exposes a defect: QUALITY 74's cited `stale-count-after.txt` does not exist (lane or staged package) and its claimed after-state `STALE_COUNT=PASS` exit 0 is not reproducible — today the check exits 1 with UNRESOLVED=2 (LOG.md:1803's stale 28 has no correction line; README:1080's "55-row manifest" is a cross-receipt false stale), and the frozen before-capture (4 STALE) no longer matches lane bytes (5 STALE).
