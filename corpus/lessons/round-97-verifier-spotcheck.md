# chousa round 97 — verifier spot-check (non-author)

author: hyaku closure (non-author integrator, @m_zfl)

Closed 2026-11-09 (UTC). Report `.ufo/reports/round-97/chousa.md` (fleet repo); lane HEAD before
`3368868557c375121c4074a7d560fda1fad88cc1`, after `c523b3de3768014925d50adbe14a512f552acca8`.
Driver digest (copied from mutable `.ufo/watchdog.log`):
`2026-11-08T22:53:28-03:00 launch chousa round=97 pgid=3599611 driver=hyaku-inline attempt=1`;
`2026-11-08T23:40:05-03:00 complete chousa round=97; hyaku-inline attempt=1`.

## Conformance (step 1)

| check | command | observed |
|---|---|---|
| report committed by lane identity | `git log --format='%an %H %ci' -- .ufo/reports/round-97/chousa.md` | `chousa-shokunin bdb1a3f6c5cec679cd9f866dbcfd9e6c2470cb31 2026-11-08 23:39:41 -0300` (before the 23:40:05 completion line) |
| SHONEN heading, one line per box | read report §SHONEN | 4 lines, all `[~]`, each with a pointer; `SHONEN.md` itself shows 4 `[~]` boxes, none `[x]` |
| cited commits exist and are ancestors of `master` | `git merge-base --is-ancestor <h> master` for 9a0ce201, 4de41332, d84f4e1e, 1042eb97, c523b3de, 33688685 | all `anc` |
| lane pushed, no leftovers | `scripts/hyaku/jj-lane.sh state …/chousa-shokunin`; `git status --porcelain \| wc -l` | `ahead=0 behind=0 head=detached tracked=0 untracked=0`; `0`; `ls-remote origin refs/heads/master` = `c523b3de…` |
| lineage | `git log --format='%h %p' -4 9a0ce201` | 9a0ce201 ← 33688685 (r96 closure) ← c8087ac5 (report's "Base"); linear |
| prompt carries the template contract | headings of `.ufo/prompts/chousa-round-97.md` | §1 MISSION/AXES, §2 claims, §2b frontier, §3 L2 floor, §4 report contract, §5 commit/push, §6 hyaku addendum, §7 scratch, §8 pre-file ledger |
| misroot cleanup | `ls R97*` at fleet root | none left (the 16 `R97RevenPrior-*.txt` were moved into the lane, per report) |

Verdict: real report, not a marker → status `ok`. No conformance defect found.

## Pre-file falsification ledger (step 2b)

`python3 scripts/hyaku/prefile-falsification.py --lane chousa --round 97` →
`PREFILE-FALSIFICATION: pass claims=2 rows=16 attack_seats=8 findings=0`, exit 0. Ledger
`.ufo/waves/round-97/claim-falsification.tsv`: 16 rows, both claims covered, 9 `falsifies-wording` rows each naming
`plans/round-97.md` (Amendments A1-A5, B1-B12 present there and the narrowed sentences in
`.ufo/waves/round-97/claims.md` §Amendments). No failing row to adjudicate.

## Claims (step 2)

### C1 `C1-SELFTEST-GRIP-R97` — operability — **evidence-verified** (lane gate; not executed per §Gate standard) plus static re-measurement

- Static case count, my measurement: `git show <rev>:tools/search-rerun.py | grep -oE '…"[a-z][0-9]{2}-[a-z0-9-]+"' | sort -u | wc -l`
  → base `33688685`: **32**, HEAD `c523b3de`: **48** (matches reported 32 → 48).
- Outer guard present at HEAD: `_selftest_cases(case)` wrapped in `try … except Exception` → `("setup", False)`
  (tools/search-rerun.py:578-582); per-case guard in `case()`.
- Revision measured: `after-f2/c1-all.txt` header `# computed_against F2=d84f4e1e…`; my
  `git diff --stat d84f4e1e c523b3de -- tools/search-rerun.py corpus/evidence/round97/selftest-controls-r97.py corpus/evidence/round97/entry-controls-r97.py`
  → empty, so the receipt grades the landed bytes.
- Committed tallies: `after-f2/c1-all.txt` lines 51-52 `SEARCH_RERUN_SELFTEST: PASS cases=48/48`, `exit=0`; lines
  153-155 `POSITIVE=1/1 EXTERNAL_KILLED=34/34 … BASE_KILLED=10/34 CASES=48`, `SELFTEST_CONTROLS_R97=PASS`, `exit=0`.
  `grep -c '^CASE external .* KILLED'` → 34. Before (`before-f2/c1-base.txt`): KILLED 10, SURVIVED 24,
  `SELFTEST_CONTROLS_R97=FAIL`, `exit=1`. Oracle stand-ins (constant-pass, hollow-selftest, always-fail) each
  `battery_rc=1 … ok`.
- Harm: `after-f2/c1-verify-harm-and-c2-separable.txt` — six `SAME` lines (plain and `--strict` on three records);
  `git diff 33688685 c523b3de -- tools/search-rerun.py` removes only the old self-test body/docstring and adds
  `_selftest_cases`; `tools/gate-records.py`, `tools/research-gate.sh` unchanged.
- Named limits (a)(b)(g) are honest: `R97MutantsC1.md:35` "19 uncovered outright", routed in SCORECARD planned r98.

Result: before→after reproduced; claim verifies on its F2 sentence.

### C2 `C2-ENTRY-R97` — depth — **re-measured**

| quantity | command (mine) | observed | reported |
|---|---|---|---|
| entry absent at base | `git cat-file -e 33688685:corpus/knowledge/press-checklist-questions-r97.md` | absent | absent |
| GATE-RECORD lines | `grep -c GATE-RECORD <entry>` | 30 | 30 |
| decision rows | rows under `## Decision table` | 8 | 8 |
| located quotes on one capture line | python: whitespace-collapsed quote ⊂ collapsed capture, per `\| L<n> \| S22x \|` row | 29/29, none missing | 29/29 |
| S225 quotes verbatim in S226 | same, against `80a844fe…txt` | 10/26 | 10/26 |
| S225 quotes after deleting non-alphanumerics | lowercase + `[^a-z0-9]` deleted | 14/26 | 14/26 |
| 7 searches at `c8087ac5` | `git grep -lF/-lE <expr> c8087ac5 -- 'corpus/captures/*.txt' \| wc -l` | orphan lines 0, hits per line 0, spelling errors 0, truncation 3, subject headings 4, proximity operators 3, PICO 12 | 0,0,0,3,4,3,12 |
| registry rows | `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md` at base / HEAD | 223 / 226 | 223 / 226 |
| drift after F3 | `git diff --stat 1042eb97 c523b3de -- corpus/knowledge/ tools/ corpus/captures/ corpus/SOURCES.md` | empty | — |

Gate receipts (evidence-verified, not executed): `after-f3/c2-all.txt` header `computed_against F3=1042eb97…`;
`GATE_RECORDS files=1 records=30 ok=30 fail=0`, `METADATA_COMPLETE=1/1`, `SEARCH_RERUN_SUMMARY searches=7
rev_match=7/7`, `ENTRY_CONTROLS=PASS`, all `exit=0`. Result: claim verifies.

## Per-axis verdicts

| axis | verdict | basis |
|---|---|---|
| operability | improved | 34/34 vs 10/34 non-author mutants killed; 48 vs 32 cases; outer guard (C1) |
| depth | improved | new entry holding PRESS 2015 questions with measured reprint comparison (C2) |
| coverage | unchanged | 3 registry rows, `PROVINCE.md` untouched |
| freshness | unchanged | no re-verification claim |
| calibration | unchanged | narrowing via amendments; no claim |
| adjacency | unchanged | no claim |

SCORECARD diff `33688685..c523b3de` is append-only (Round 97 verdict + planned r98); no axis harmed.

## Discernment spot-check (step 3)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S225 Cochrane checklist for editors | admit, tier B | `curl -sSL -A <browser UA>` the PDF → 200, 137268 B, sha256 `56c4cdd605df…` (= recorded raw `56c4cdd6…`); `pdftotext -layout`: line 71 "Are there any spelling errors?", line 73 "…orphan lines…", line 81 "Derived from:" | agree | bytes identical to the capture; quote present; a methods organisation's reprint "derived from" the statement is correctly tier B, not A |
| S226 Karolinska PRESS 2015 page | admit, tier C, corroboration only | GET → 200, 59140 B (HTML differs from capture — dynamic page); "a structured tool for peer review of electronic literature search strategies." present; "Translation of the research question" present | agree | quote holds; library guide correctly tier C and never sole support (my recount: every S226 row is with S225 rows in the decision table) |
| S227 CADTH Table 9 PDF | reject (route, 403) | GET → 403, 5868 B, `<title>Just a moment...` (Cloudflare challenge) | agree | unreachable from this host; rejection names a flip condition and is not a fabrication ruling |

SOURCES row re-opened: `corpus/SOURCES.md:237` (S225) anchor quotes "See PRESS checklist below" (4 words) and
"PRESS 2015 Guideline Evidence-Based Checklist" (5 words) — both ≤25 words, each found once in the re-fetched PDF text.
Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` → `chousa ok …/SOURCES.md`,
exit 0; warnings W04 ×6 (pre-existing duplicate URLs) and W01 `S226 tierC mined` (disclosed in report).

## Trend verdicts

- expansion: **improved** — 223 → 226 registry rows; one new knowledge entry on README's named gap.
- quality: **improved** — search-rerun gate self-test kills 34/34 named non-author mutants vs 10/34 for the base tool,
  with a summary line on set-up crashes.
- discernment: **improved** — all three sampled gate decisions agree on re-open; reprint-vs-reprint measured (10/26,
  14/26) rather than either taken as the guideline; tier C kept off sole support.

## Routed defects (lane fixes next round)

1. `R97MutantsC1` 19 uncovered survivors (g01-g05 guard/summary, `u03-blob-silent`, p04-p07, `m05` non-ASCII str-sort).
2. C1 limit (g): a self-test printing the expected 48 lines without computing them (hash-of-self) passes the battery.
3. C2 limits: Never cells not instrument-checked; WARRANT_TERMS is a lexical floor; SOLE_SUPPORT checks naming, not
   support.
4. `R97SentinelC1` battery docstring wording (read-only / writes-only-under-work; NO_WRITE blind to ignored paths).
5. Carried D1: `S224` names two documents in `refetch.tsv` — needs a reader rule.

Operator note: SHONEN boxes 2 (LOG end-to-end task) and 3 (instructions executable) look checkable by a non-author from
committed receipts; promotion is operator-owned.
