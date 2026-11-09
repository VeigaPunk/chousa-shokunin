# R98ScribeLesson — round 98 scribe report (lane chousa, L1 `ChousaR98`)

Scope (seat spec): draft the round-98 lesson's `## Mistakes` section and a LOG.md entry; draft the `## Gate` lines
for S228-S231 from `refetch.tsv` and the captures. Attacked tree: freeze F `aac826848dda5029ba459568b29d9a92176dc2b6`
(scratch clone, `git rev-parse HEAD` verified). Base `98b8177c1e8b39cdf1167928e4f5d609f6fa81b6`. Lane HEAD `aac82684`
at the time of checking; `git diff aac82684 -- tools corpus/evidence/round98 …` empty.

Drafts (not written into the lane's lesson or LOG):
- `.ufo/waves/round-98/w1/R98ScribeLesson-mistakes-draft.md` — `## Mistakes` (one class), `## Gate` lines S228-S231, notes for the L1.
- `.ufo/waves/round-98/w1/R98ScribeLesson-log-draft.md` — LOG.md entry, round 98.

## Mistake class mined (one)

A guard was instrumented only on the path where it fires (an exception raised inside a case) and not on the path that
reports (the recorded verdict, the count, the summary line, the exit code). Round 97 claimed "each [case] inside a
guard…" (`.ufo/waves/round-97/claims.md:10`, `:102`). Its guard mutants were crash-only
(`corpus/evidence/round97/selftest-controls-r97.py:123-135`, `x1`-`x3`, each a `raise`); the verdict-path mutants
`g01`-`g05` survived the round-97 self-test and the round-95 battery (`.ufo/waves/round-97/w1/R97MutantsC1.md:45-59`,
`:141-144`; `corpus/evidence/round95/*.py` contains no `--selftest`, checked by grep). Captured-by: none.

Fix and how it was shown able to fail: `_guard_canary` (`tools/search-rerun.py:676-699`), called first in `selftest()`
(`:715`). Base receipt: `corpus/evidence/round98/before/c1-base.txt:8-12` (`g01`-`g05` each `rc=0 SURVIVED` under the
round-98 battery applied to the round-97 tool) and `:83` (`BASE_KILLED=12/37 required_killed=12/35 … expect<35 ok`).
F receipt: `R98ScribeLesson-battery-F.txt:2-6` (each `rc=1 KILLED failed=g00-guard-canary`) and this seat's own
reproduction `R98ScribeLesson-direct-g.txt` (g01-g05 KILLED by `g00`; `u01`, `u05` SURVIVED, as named).

## Findings

### F1 — the fix does not reach the self-test's own exit path (coverage residual; the mistake class is narrowed, not closed)

`tools/search-rerun.py:723` (`return _summary(results)` in `selftest()`). A one-site mutant `_summary(results)` +
`return 0` there (`R98ScribeLesson-exit-probe.txt`, diff shows one hunk):
- healthy tree: `python3 -B search-rerun.py --selftest | tail -1` → `SEARCH_RERUN_SELFTEST: PASS cases=67/67`, exit 0 — same as F;
- one failing case (driver replaces `_selftest_cases` with one `case("probe-false", lambda: False)`, the guard canary
  unchanged): F `selftest()` returns `1`, the mutant returns `0`, both print `SEARCH_RERUN_SELFTEST: FAIL cases=1/2 failed=probe-false`.
The canary does not call `selftest()`'s return; no lane case fails on a healthy tree; the mutant is not in the 37, the
prior 34, or the 23. The battery's kill rule (exit 1 + FAIL line) therefore cannot score it. This does not falsify
C1's sentence (the sentence states the PASS line, the 67 case lines and the 35/37 kills; it says nothing about the exit
code of a failing run), and it sits under named limit (a). It is the same class as round-97 `g05`, one function up.
Recorded as a round-99 candidate and as an open residual in the Mistakes row.

### F2 — the approval table's preamble says more than its rows (process claim; the lesson's sentence repeats it)

`corpus/evidence/round98/egress-approval.md`, first paragraph: "It was written before any round-98 GET." Its own rows
say otherwise: the PubMed row was "added after the CADTH appendices GET answered 403 … before any GET below"; the NCBI
row was added "at the same time"; the Europe PMC row was "added after both NCBI GETs returned challenge pages".
Timestamps (`corpus/evidence/round57/refetch.tsv`, `stat -c %y`): S228 GET `02:47:35Z` (`23:47:35` local), S229 and
S230 `02:48:10Z`, S231 `02:48:35Z`; the table's mtime is `23:48:34` local (`02:48:34Z`), i.e. after GETs S228-S230 and
one second before S231. Plan line `plans/round-98.md:31` repeats "written before the first GET" and the lesson's header
repeats "written before the first one". Narrowed claim for the L1: "written before the first GET; rows appended after
GETs 1-3, named in the table". No scribe edit.

### F3 — challenge-page bytes stored as captures against the table's rule (wording vs instrument)

`egress-approval.md` (CADTH row / rule text) says "a challenge page is a failed attempt, never a capture", and the
S230 row says "an http 200 that carries a challenge page is a failed attempt, never a capture". Both keys are on disk
as `.raw/.txt` under `corpus/captures/`: `0954149536aaad411000e1fb` (S229, 21 lines, txt sha256 `7070b59c…`, text
"Cookies must be enabled") and `b5b8d050eea0c638e95ba674` (S230, 13 lines, txt sha256 `4f25f0b1…`, text "Checking your
browser before accessing www.ncbi.nlm.nih.gov"). Receipts: `R98ScribeLesson-gate-hashes.txt`. The Gate lines say "bytes
stored, not cited", matching the disk; the rule's wording needs the L1's decision.

### F4 — the "after" receipts the prompt names are not in the freeze

The seat prompt says receipts are in `before/` and `after/` (at F). At F, `corpus/evidence/round98/` has `before/`
(three files: `c1-base.txt`, `c1-verify-harm.txt`, `c2-base.txt`) and four top-level files; there is no `after/`
(`git ls-tree -r --name-only aac82684 -- corpus/evidence/round98`, `R98ScribeLesson-harm-F.txt`; `ls` in the lane:
`No such file or directory`). The claim's own text (`claims.md`, Before paragraph) names only `before/`. So no
committed after-state receipt exists; the after-state here is this seat's own run of the frozen battery
(`R98ScribeLesson-battery-F.txt`), not a lane receipt. Recorded; not fixed.

### Checked and held (reproductions at F, not verdicts)

- Frozen battery at F, `selftest-controls-r98.py` (its sha256 `942b7069…` equals the one `before/c1-base.txt` records):
  `POSITIVE=1/1 KILL_REQUIRED=35/35 DO_NOTHING_REFUSED=1/1 PRIOR_R97_KILLED=34/34 R96_MUTANTS_KILLED=23/23
  EQUIVALENT_SURVIVED=3/3 ORACLES_REJECTED=5/5 NO_WRITE=1/1 REGRESSION_R95=2/2 EXTERNAL_R97_KILLED=35/37
  BASE_KILLED=12/37 CASES=67`, `SELFTEST_CONTROLS_R98=PASS`, exit 0, 688 s (`R98ScribeLesson-battery-F.txt:146-147`).
  Its five oracles each fail it (`:138-142`); the guard-blind oracle drops `KILL_REQUIRED` to 30/35 (`:141`).
- K3 harm leg, four fixtures, plain and `--strict`: base `98b8177c` vs F, all `SAME`
  (`R98ScribeLesson-harm-F.txt`; `CLEAN` rc 0 plain; `DRIFT` rc 1 `--strict` on all four fixtures; every line SAME).
- Gate hashes: refetch rows for S228-S231 match the committed captures (`R98ScribeLesson-gate-hashes.txt`); S231
  `raw` and `txt` sha256 are identical (`4111c45a…`, one JSON line, `hitCount` 1); S231 located quote is verbatim
  in `abstractText` (16 words, python substring check, also raw-JSON substring).
- `plans/round-98.md` P0 (the `g06` site collision): the battery at F prints `setup=0` on the external leg
  (`R98ScribeLesson-battery-F.txt:39`), so no scored mutant applies more than once; the pre-freeze failure itself was not re-run.

## Not done (by seat scope)

- C2 gate commands (`gate-records.py`, `research-gate.sh`, `search-rerun.py verify`, `entry-controls-r98.py`) were not
  run by this seat; the L1 and the verifier own them.
- No network GET by this seat. The S228-S231 quotes and hashes come from the committed captures and `refetch.tsv`.

## Receipts (all in `.ufo/waves/round-98/w1/`)

- `R98ScribeLesson-battery-F.txt` — full frozen battery at F (148 lines, `exit=0`).
- `R98ScribeLesson-direct-g.txt` — g01-g07, u01, u05 applied to F from the committed probe texts; `--selftest` rc and last line.
- `R98ScribeLesson-exit-probe.txt` — F1 one-hunk mutant, failing-case driver output, healthy-tree rc.
- `R98ScribeLesson-base-guard-rows.txt` — copy of `before/c1-base.txt` lines cited (1-2, 8-12, 45, 83).
- `R98ScribeLesson-cited-lines.txt` — base `case()`/summary lines (`98b8177c:tools/search-rerun.py:569-587`), F line numbers, round-97 battery `x1`-`x3` lines, battery sha.
- `R98ScribeLesson-gate-hashes.txt` — refetch rows S228-S231, capture sha256 and line counts, `555c86e9` absence.
- `R98ScribeLesson-harm-F.txt` — K3 harm leg at F and the tree listing for `corpus/evidence/round98`.
- `R98ScribeLesson-mistakes-draft.md`, `R98ScribeLesson-log-draft.md` — the drafts.

Tooling: nothing installed, upgraded or removed. Pacman not used. Scratch
`/fast/scratch/hyaku/chousa-r98/R98ScribeLesson/` (clone at F, mutant copies, battery work dir) deleted before yield.

VERDICT: R98ScribeLesson C1 n/a — drafted the Mistakes row and reproduced the frozen battery and harm leg at F (predicate lines identical to claims.md); the exit-path residual (F1) lies outside the sentence's stated wording, and no C1 verdict is issued by the scribe.
VERDICT: R98ScribeLesson C2 n/a — drafted the S228-S231 Gate lines from refetch.tsv and the committed captures only; C2 gate commands were not run by this seat, so no C2 verdict is issued.
