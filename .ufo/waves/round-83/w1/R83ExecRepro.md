# R83ExecRepro — reproduction of the frozen round-83 claims (leaf seat)

Lane: `chousa-shokunin`. Revisions judged: base/round-82 tip `a46534a5…`, egress table `8fff80ee…`, prefreeze
`1b9b2ff8955190a3e5cd42800009d13d6b8e4e04`, claim freeze `3fbf8d1227a8aa317a036604edad93d7b20a149f`, landing
`81b81173f19d175e2b2a6b409b2a496d09d0b258`, tip `aca2a781ef2db375881c21bf407e153f786ac61f`.
Claims file read first: `corpus/evidence/round83/claims.md` (both claims, all kill rules).
Leaf rules observed: no task/subagent dispatch, no production edits, no git/jj mutation of the lane or fleet (only
`git archive`, `git show`, `git cat-file`, `git rev-parse` reads), no network, no package installs. Scratch
`/fast/scratch/hyaku/chousa-r83/R83ExecRepro` was created with `mkdir -p` and removed on exit (see Cleanup).
All receipts cited below are under `.ufo/waves/round-83/w1/R83ExecRepro/`; the two independent checkers are preserved
there as `indep-c1.py` and `indep-c2.py` (their receipts name the scratch path they were run from).

## (a) Instrument identity — all pins match at all four revisions

Command (per revision):
`for rev in 1b9b2ff8… 3fbf8d12… 81b81173… aca2a781…; do while read -r pin p; do case "$pin" in \#*|"") continue;; esac; git show "$rev:corpus/evidence/round83/$p" | sha256sum; done < corpus/evidence/round83/instrument-pins.txt; done`

Receipt: `pins-repro.txt`. Observed: `PINS rev=… match=8 mismatch=0` at each of the four revisions, for all eight
pinned paths (`depth-r83.py`, `gate-records-r83.py`, `run-controls-r83.sh`, `c2-positives.tsv`, `base-knowledge.txt`,
`controls/stub-accept.py`, `controls/stub-quote-only.py`, `controls/stub-refuse.py`). Exit 0 throughout.
Note: my first pass mis-parsed the file's `#` comment line as a pin (`pin="#"`); that was my loop's bug, not a lane
defect — skipped comment lines produce the 8/8 above.

Additional identity (receipt `revision-identity.txt`): `tools/gate-records.py` = `d38443769fe7c2ba014ec9d7861c4078cec24d0a193eeadb2cd5222d0d392687`
at both the landing and the tip revision, matching `corpus/evidence/round83/after/pins-after.txt`; the C1 entry
`corpus/knowledge/appraisal-judgment-records-r83.md` = `40b5bbe6151dde2dc345f9f9d15a46921977641910356d2481e1aca21d7636cd`
at both revisions; `corpus/lessons/round-83.md` exists only at the tip (`48f3bdf1…`); `corpus/SOURCES.md` changes at
the landing (`b104afbd…` → `296c6a62…`), `corpus/evidence/round57/refetch.tsv` is `9f2136c9…` from the prefreeze
commit on.

## (b) BEFORE / AFTER from archived trees

Trees: `git -C <lane> archive <rev> | tar -x -C /fast/scratch/hyaku/chousa-r83/R83ExecRepro/tree-<rev>`.

### BEFORE — `1b9b2ff8955190a3e5cd42800009d13d6b8e4e04` (receipt `before-instruments.txt`)

`python3 -B <tree>/corpus/evidence/round83/depth-r83.py --root <tree>`
```
DEPTH_R83 entries=0 ok_entries=0 rows=0 located_quotes=0 fresh_sources=0
DEPTH_R83=FAIL
rc=1
```
`python3 -B <tree>/corpus/evidence/round83/gate-records-r83.py --root <tree> --repo <lane> --work /fast/scratch/hyaku/chousa-r83/R83ExecRepro`
```
TOOL=absent POSITIVE=0/15 FORGED_REFUSED=0/198 EXPECTED_CODE=0/198 EMPTY_REFUSED=0/1 RC=0/3
GATE_RECORDS_R83=FAIL
rc=1
```
Both match the frozen before lines and rc exactly. `tools/gate-records.py` is absent at this revision (receipt
`revision-identity.txt`), which is why the counter reports `TOOL=absent`.

### AFTER — landing `81b81173f19d175e2b2a6b409b2a496d09d0b258` (receipt `after-81b81173.txt`)

```
ENTRY appraisal-judgment-records-r83.md ok=yes rows=10 quotes=16/16 fails=-
DEPTH_R83 entries=1 ok_entries=1 rows=10 located_quotes=16 fresh_sources=3
DEPTH_R83=PASS
rc=0
```
```
TOOL=present POSITIVE=15/15 FORGED_REFUSED=198/198 EXPECTED_CODE=198/198 EMPTY_REFUSED=1/1 RC=3/3
GATE_RECORDS_R83=PASS
rc=0
```
Predicate arithmetic against claims.md: `entries=1 ok_entries=1` ✓, `rows=10` ≥ 7 ✓, `located_quotes=16` ≥ 8 ✓,
`fresh_sources=3` ✓; the C2 line is exactly the frozen `TOOL=present … RC=3/3` string ✓, rc 0 ✓.
These lines are byte-identical to the committed `corpus/evidence/round83/after/c1-after.txt` and `c2-after.txt`.

### AFTER repeat — tip `aca2a781ef2db375881c21bf407e153f786ac61f` (receipt `after-tip.txt`)

Both runs print the same `DEPTH_R83 …` / `GATE_RECORDS_R83=PASS` lines with rc 0. The predicates still hold at the
tip, i.e. the round-83 lesson commit did not move either number.

## (c) Committed control driver re-run

Command (exactly as assigned, from the lane root):
`HYAKU_SCRATCH=/fast/scratch/hyaku/chousa-r83/R83ExecRepro bash corpus/evidence/round83/run-controls-r83.sh 1b9b2ff8955190a3e5cd42800009d13d6b8e4e04 .ufo/waves/round-83/w1/R83ExecRepro/controls-rerun`

Receipt: `controls-rerun/summary.tsv` plus the eight per-control receipts, comparison in `controls-rerun-compare.txt`.
Observed: the eight rows and `CONTROLS_AS_EXPECTED=8/8`, driver rc 0. `diff` against the committed
`corpus/evidence/round83/controls/receipts/summary.tsv` (at `3fbf8d12…`) is empty (`SUMMARY_IDENTICAL`), and each
per-control receipt body (all lines except the `#` header, which carries the command paths) hashes equal to the
committed body: `BODY_MATCH` for all eight (`c1-d0-donothing`, `c1-d1-r81-filler`, `c1-d3-r82-entry-relanded`,
`c1-b1-salad-boundary`, `c2-k0-donothing`, `c2-f1-stub-accept`, `c2-f2-stub-refuse`, `c2-f3-stub-quote-only`).
The driver's scratch (`$HYAKU_SCRATCH/chousa-r83/controls`) was removed by its `trap`.

## (d) C2 predicate (b) at the tip

From the archived tip tree (receipt `c2-predicate-b.txt`):
`python3 tools/gate-records.py verify --root . corpus/lessons/round-83.md`
```
GATE_RECORD corpus/lessons/round-83.md:19 S009 OK
GATE_RECORD corpus/lessons/round-83.md:20 S212 OK
GATE_RECORD corpus/lessons/round-83.md:21 S213 OK
GATE_RECORDS files=1 records=3 ok=3 fail=0
rc=0
```
`ok=records=3` with `records=3 ≥ 3`, exit 0 ✓. At the landing tree the same command reports
`GATE_RECORDS_ERROR missing corpus/lessons/round-83.md`, rc 2 — the file does not exist before the tip, consistent
with predicate (b) being tip-scoped (receipt `c2-positives-with-repo.txt`).

## (e) C2 K4 — exit contract

Receipt `c2-k4-exit-contract.txt`, fixtures built from round-83.md line 19 in scratch:

| case | command | observed | rc |
|---|---|---|---|
| file with no in-class record (prose mentions only) | `verify --root . <none.md>` | `GATE_RECORDS files=1 records=0 ok=0 fail=0` | 1 |
| one OK record + one FAIL record (`words=99`) | `verify --root . <mixed.md>` | `… :3 S009 OK`, `… :4 S009 FAIL WORDS`, `records=2 ok=1 fail=1` | 1 |
| missing FILE argument | `verify --root .` | argparse `error: the following arguments are required: files` | 2 |
| nonexistent FILE path (extra) | `verify --root . <nope.md>` | `GATE_RECORDS_ERROR missing <nope.md>` | 2 |

Expected 1, 1, 2 — all observed; K4 does not fire (no exit 0 on no-record input, no exit 0 while printing `FAIL`).

## Independent cross-checks (my own code, claims text only)

1. **C1 numbers recomputed** (`c1-independent.txt`, `indep-c1.py`, tip tree). `source:` names exactly 3 S-ids;
   16 declared quotes; decision table has a `Warrant` column and 10 body rows; the Warrant cells name all 16 declared
   qids and no undefined qid; minimum non-Warrant cell length 7 words; each of S009/S212/S213 has a registry row with
   tier A, status `mined`, used-by naming the entry, capture key `sha256(url)[:24]`, an existing capture whose sha256
   equals the refetch `txt_sha256` of a row with `curl_rc=0`, `http=200`, `fetched_utc ≥ 2026-11-06T20:53:00Z`;
   all 16 quotes occur (whitespace-collapsed, curly quotes folded) in their capture and are 8–25 words; 16 distinct
   quote texts. Result: `rows=10`, `located=16/16`, `fresh_sources=3`, exactly the counter's numbers.
2. **C1 K4 ground** (scan, no receipt file beyond the terminal output quoted here). All 94 entries of
   `corpus/evidence/round83/base-knowledge.txt` (read as `corpus/knowledge/<name>`) were grepped for `\bS009\b|S212|S213`
   and for the three source URLs: `sid_hits=0`, `url_hits=0`. No base entry cites the three sources or their URLs.
3. **C2 independent mutant battery** (`c2-independent-mutants.txt`, `indep-c2.py`): 19 hand-built cases at the tip
   tree — genuine admit and genuine rev records (OK), then one case per docstring code (REGISTRY, TIER,
   CAPTURE_PATH, CAPTURE_KEY, CAPTURE_SHA, REFETCH, WORDS, QUOTE_LEN, QUOTE_ABSENT, PARSE, REV, LINE), plus class
   edges: BOM-prefixed genuine record → OK; ZWSP-prefixed forged record → `QUOTE_ABSENT`; tab after `GATE-RECORD` →
   `PARSE`; bare `GATE-RECORD` → `PARSE`; a prose file with inline-code, list-item, blockquote and HTML-comment
   mentions yields no record at all. `mismatched=0`, tool rc 1. (First run of this battery had one wrong expectation of
   mine — I expected `REGISTRY` for a URL mutation; a changed URL keeps the S-id in the registry, so the tool's
   `CAPTURE_KEY,REFETCH` is correct. My fixture error, corrected in the preserved script; not a lane defect.)
4. **The 15 positives directly** (`c2-positives-with-repo.txt`): the tool, run on lessons 80–82 with `--repo <lane>`,
   prints 15 `OK` and `records=15 ok=15 fail=0`, rc 0 — at both the landing and the tip tree. The positive set is
   exactly the 15 `GATE-RECORD` lines of those three lessons.
5. **Forgery arithmetic** (`c2-battery-count.txt`): positives by form 10 admit, 1 unreach, 4 rev × mutations per form
   17/4/6 = **198** derived forgeries, matching the counter's `FORGED_REFUSED=198/198`.
6. **Determinism and read-only behaviour** (`determinism-readonly.txt`): each counter and the tool produce
   byte-identical stdout on a second run (rc 0 both times); a `find . -printf '%p\t%s\t%T@\n'` manifest of the tip
   tree is identical before and after all instrument/tool runs (`TREE UNCHANGED`), i.e. none of them writes inside
   the tree. The tool's only subprocess is `git -C <repo> cat-file -t/-t/blob` (read-only); its imports are
   `argparse, hashlib, os, re, subprocess, sys, unicodedata` — no network module, no writer.
7. **In-class scan of the whole tip tree** (terminal scan quoted in this report): 92 lines are in-class by the frozen
   definition (first text after leading whitespace/Cf is `GATE-RECORD` + whitespace/EOL). 18 are in
   `corpus/lessons/` (the 15 of rounds 80–82 plus the 3 of round 83); the remaining 74 are wave artifacts, receipt
   fixtures and a script docstring line (`corpus/evidence/round80/gate-grounding-check.py:13`). The tool checks only
   the files named on its command line, so only the lesson records are verified by it.

## Findings

**In class: none.** Every expected value in (a)–(e) was observed as stated; no kill rule fired on the checks this
seat ran (C1 K1; C2 K1 both parts; C2 K4). The claims' counters, fixtures, receipts and instrument bytes are as
frozen, and both counts reproduce from committed bytes at the landing and at the tip.

Residuals (out of class, listed separately — none of them is a kill under the frozen rules):

- **R1 — rev-form records need a GITDIR.** Running the landed tool from an archive without `.git` and without
  `--repo` (`c2-positives-direct.txt`): the four round-80 rev records print `FAIL LINE,REV`
  (`records=15 ok=11 fail=4`, rc 1); with `--repo <lane>` all 15 print `OK` (item 4 above). The default
  `--repo=LANE` is documented in the tool's usage, and the frozen counting command passes `--repo`; predicate (b)
  uses url-form records only. Consequence: an operator who forgets `--repo` on an exported tree gets false failures
  on rev records, not false passes.
- **R2 — records outside lessons are not verified by the tool.** 74 in-class lines live in wave artifacts/fixtures
  (item 7). The C2 claim is about "a lesson's `GATE-RECORD` lines" and the counting command gives the three lesson
  files; the tool verifies exactly the files it is handed. Not a contract breach, but the in-class property alone
  does not make a lane file gate-checked.
- **R3 — my own battery expectation error** (item 3), recorded for honesty: one case's expected code was mine, not
  the tool's contract; the corrected run is the one preserved.

Kill rules deliberately not in this seat's scope: C1 K2 (live re-open of the pages) and K3 (warrant reading) — other
round-83 seats; C2 K2/K3 are judged on the landed tool against lane bytes and the counter's own battery, which I
reproduced rather than re-derived in full.

## Environment / tooling

No tool was installed or upgraded (pacman is paused host-wide anyway); no network was used; no host service or sysctl
was touched. Commands used only `git show/archive/cat-file`, `bash` coreutils, and `python3` (standard library) with
`-B`.

## Cleanup

`/fast/scratch/hyaku/chousa-r83/R83ExecRepro` (three archived trees, manifests, fixtures, the two checkers' run-time
copies) is removed before yielding; the receipts and the two checker scripts are copied into this seat's wave output
folder, which is the only lane path written.

VERDICT: R83ExecRepro C1 held — the depth predicate reproduces exactly from committed bytes (before: entries=0 FAIL rc 1; landing and tip: entries=1 ok_entries=1 rows=10 located_quotes=16 fresh_sources=3 PASS rc 0), the 16 quotes locate in the committed captures under an independent normalizer, and no base entry cites S009/S212/S213 or their URLs.
VERDICT: R83ExecRepro C2 held — the tool predicate reproduces exactly (before: TOOL=absent FAIL rc 1; landing and tip: TOOL=present POSITIVE=15/15 FORGED_REFUSED=198/198 EXPECTED_CODE=198/198 EMPTY_REFUSED=1/1 RC=3/3 PASS rc 0), predicate (b) prints ok=records=3 at the tip with rc 0, and the K4 exit contract is 1/1/2 as frozen.
