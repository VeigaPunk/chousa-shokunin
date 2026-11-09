# Round 95 — non-author verifier spot-check (chousa)

author: hyaku closure (non-author integrator, @m_zfl)

Lane-round: chousa r95 (attempt 2, L1 `ChousaR95a2`). Base `7b2373586fb70f0ead6446c671fcc8b546d3e687`, landing
`07e0e3323db692da4f726437bbc388acea4ae5e0`. Report `.ufo/reports/round-95/chousa.md` (fleet repo, commit
`dc9f587af50a923227f7d6b4ff1476930c790504`). Closed 2026-11-09T00:03Z. All measurements below were run by this
reviewer over `git archive` exports of base and landing into scratch (`/tmp/cv95/{base,after}`, not evidence by
itself — the commands are the pointer and re-run against the cited hashes).

Driver digest (copied from `.ufo/watchdog.log`, mutable):

```
2026-11-08T13:38:18-03:00 launch chousa round=95 pgid=3598027 driver=hyaku-inline attempt=1
2026-11-08T13:48:11-03:00 lane-dead-no-report chousa round=95; retry same round (hyaku-inline attempt=1: L1 ended without a landed report: FAIL report_of (missing, unchanged, no SHONEN heading, or < 400B): .ufo/reports/round-95/chousa.md)
2026-11-08T19:48:09-03:00 launch chousa round=95 pgid=52349 driver=hyaku-inline attempt=2
2026-11-08T21:00:43-03:00 complete chousa round=95; hyaku-inline attempt=2
```

## 1. Step-1 conformance

| check | command | observed | result |
|---|---|---|---|
| report attribution | `git log --format='%an %H %ci' -- .ufo/reports/round-95/chousa.md` (fleet) | `chousa-shokunin dc9f587a… 2026-11-08 21:00:06 -0300`; ancestor of fleet `origin/main` (exit 0) | ok |
| lands last | lane `git log -1 --format=%ci 07e0e332` | `20:59:07 -0300` < report `21:00:06` | ok |
| SHONEN heading | report `## SHONEN`; lane `grep -c '^- \[' SHONEN.md` | heading present, 4 lines for 4 boxes, all `[~]` | ok |
| cited hashes | `git -C <lane> merge-base --is-ancestor <h> master` for 7b237358, d6429e02, d27e9891, bc94923b, 86909f02, dbfc602f, 07e0e332 | all exit 0 | ok |
| `8d77e6c1` (L0 fetch-scope) | `git cat-file -t 8d77e6c1` in the fleet repo | `commit` — "round-29: chousa L0 question"; a fleet hash, not a lane hash | ok |
| pushed, clean | `jj-lane.sh state <lane>`; `git status --porcelain`; `git ls-remote origin refs/heads/master` | `ahead=0 behind=0 tracked=0 untracked=0`; porcelain empty; remote = `07e0e332…` | ok |
| prompt contract | grep of `.ufo/prompts/chousa-round-95.md` | MISSION/AXES binding (l.5), 1–3 claims (l.14), frontier step 2b (l.42), ≥8 L2 in one batch (l.82), report path (l.101), SHONEN (l.118), commit-then-push (l.133), push scope (l.135), L0 (l.138), write scope (l.448), lands-last + hash (l.516) | ok |
| append-only lane files | `git diff --numstat 7b237358 07e0e332 -- LOG.md SCORECARD.md SKILL.md corpus/QUALITY.md corpus/README.md corpus/SOURCES.md corpus/evidence/round57/refetch.tsv` | `50 0`, `43 0`, `3 0`, `11 0`, `11 0`, `2 0`, `2 0` — additions only; every other path is `A` | ok |

Attempt 1 left no landed report (driver line 13:48:11); attempt 2 discarded its 19 untracked files unverified
(`.ufo/waves/round-95/inherited-attempt1.txt`, committed in `d6429e02`). Not a defect of the filed round.

## 2. Claims — re-measured vs evidence-verified

### C1 `C1-RERUN-R95` — operability, capability acquisition (`tools/search-rerun.py`)

- Before (re-measured): `ls /tmp/cv95/base/tools/search-rerun.py` → `No such file or directory`. Matches
  `before/c1-base.txt` (exit 2).
- After (re-measured independently, GNU grep 3.12 — the recording engine — not the lane's tool): each of the 8
  `## Searches` rows of `corpus/fixtures/search-rerun-r95.md` re-run as
  `/usr/bin/grep -l -{F|P} -e '<expr>' corpus/captures/*.txt | LC_ALL=C sort` (sha256 of that output for >3 hits):

  | id | recorded | base tree (rev 7b237358) | landing tree |
  |---|---|---|---|
  | Q1 | 7, `sha256:69cfc059…` | 7, `69cfc059…` | 8, `65eaf046…` |
  | Q2 | 2 (c52a…, c9d1…) | same | 3 (+1a8c36c4) |
  | Q3 | 3 | same 3 files | 4 |
  | Q4 | 1 (62be…) | same | same |
  | Q5 | 14, `sha256:df36eb98…` | 14, `df36eb98…` | 14, `df36eb98…` |
  | Q6 | 1 (c52a…) | same | 2 |
  | Q7 | 0 | 0 | 0 |
  | Q8 | 1 (a640…) | same | 2 |

  8/8 count+set match at the recorded revision; 3/8 unchanged over the landing tree (Q4, Q5, Q7). This
  reproduces the reported `rev_match=8/8 tree_same=3/8 findings=0` from outside the tool.
- Evidence-verified (lane-owned instruments, not executed here per §Gate standard): `after-f2/c1-verify.txt`
  (`# computed_against F=86909f02…`, `SEARCH_RERUN: CLEAN`, exit 0), `after-f2/c1-controls.txt`
  (`FORGERY_REFUSED=10/10 … ORACLES_REJECTED=4/4`, `RERUN_CONTROLS=PASS`, exit 0), `after-f2/c1-mutants.txt`
  (`MUTANTS_KILLED=10/10`, ten named mutants each killed with a named failing group). Revision measured: F2
  `86909f02`; `git diff --stat 86909f02 07e0e332 -- tools corpus/fixtures corpus/captures
  corpus/knowledge/search-rerun-record-r95.md corpus/evidence/round95/*-r95.py` is empty, so F2 = landing for
  the measured paths. All three predicate lines of `claims.json` appear verbatim in the receipts.
- Verdict: **verified — operability improved** (capability row in SCORECARD `## Capabilities (round-95 addition)`).

### C2 `C2-ENTRY-R95` — depth (`corpus/knowledge/search-rerun-record-r95.md`)

- Before (re-measured): entry absent at base; `/usr/bin/grep -l -F 'Document the total number of records
  identified' corpus/captures/*.txt` at base → no file, rc 1 (the entry's absence sentence holds); at landing →
  `corpus/captures/1a8c36c4c24444967bd9c3ce.txt` only.
- After (re-measured): capture sha256 `86f1aacd…3871` = every Gate record's `capture_sha256`; 13 `GATE-RECORD`
  lines; each `words=` equals the quote's word count (13/13); each quote located in the capture text 13/13
  (8 byte-exact, 5 after whitespace and curly-quote normalisation — layout text column padding); decision-table
  rows 7. Faithfulness: reading-order `pdftotext` (no `-layout`) of my own re-fetch gives "If a reader tries to
  duplicate a search from a systematic review, one would expect to retrieve nearly the same results when limiting
  to the timeframe in the original review. If instead, the searcher locates a drastically different number of
  results than reported in the original review, this can be indicative of errors in the published search [22] or
  major changes to a database…" — rows 5–6 and named limit 3 state exactly this split (Q7/Q10/Q11, Q13/Q8/Q9).
- Evidence-verified: `after-f2/c2-gate.txt` (`GATE_RECORDS files=1 records=13 ok=13 fail=0`, exit 0),
  `after-f2/c2-metadata.txt` (`METADATA_COMPLETE=1/1`, `RESEARCH_GATE: CLEAN`), `after-f2/c2-controls.txt`
  (`ENTRY_CONTROLS=PASS`, all predicate groups present), all at F2 = landing.
- Verdict: **verified — depth improved**.

### Harm check

`git diff 7b237358 07e0e332 -- SCORECARD.md` is +43/−0 (capability row, verdict, planned r96); `git diff --quiet
… -- tools/research-gate.sh tools/gate-records.py PROVINCE.md` exit 0; no lane file lost a line. No axis harmed.

### Pre-file falsification ledger

`python3 scripts/hyaku/prefile-falsification.py --lane chousa --round 95` →
`PREFILE-FALSIFICATION: pass claims=2 rows=16 attack_seats=7 findings=0`, exit 0. Independent tally
`awk -F'\t' '{c[$3]++} …' .ufo/waves/round-95/claim-falsification.tsv` → `neutral 7`, `falsifies-wording 9`,
matching the report's pasted output. No failing row to adjudicate.

## 3. Per-axis verdicts

| axis | verdict | basis |
|---|---|---|
| operability | improved | C1 re-measured (independent grep, 8/8 at rev) + receipts at F2 = landing |
| depth | improved | C2 re-measured (13/13 located, 7 rows, reading order faithful) + receipts |
| coverage | unchanged | registry 220 → 221 (`grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md`), no claim |
| freshness | unchanged | no re-verification claim |
| calibration | unchanged | no claim; D1–D8 corrections appended in `LOG.md:2767-2785` |
| adjacency | unchanged | no claim; sibling mechanisms routed, not absorbed |

## 4. Discernment spot-check (`corpus/lessons/round-95.md` `## Gate`)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S222 PRISMA-S, JMLA publisher PDF | admit (tier A) | `curl -sSL https://jmla.pitt.edu/ojs/jmla/article/download/962/1274` → http 200, 532659 B, raw sha256 `07036f03…9ec2`; `pdftotext -layout` sha256 `86f1aacd…3871` | agree | both digests equal the Gate/refetch row; the 16-word item-8 quote is present verbatim in reading order; the standard's own text by its authors in the publishing journal is tier A for this scope |
| Europe PMC fullTextXML PMC7839230 | reject (route unreachable) | `curl -sS https://www.ebi.ac.uk/europepmc/webservices/rest/PMC7839230/fullTextXML` → http 500, 150 B | agree | still unreachable at closure; correctly filed as a route rejection, not a source rejection |
| `corpus/SOURCES.md:234` S222 row (new) | — | Gate record quote (≤25 words, CORPUS rule 1): 16 words, location "Table 1, item 8" | agree | quote located in my re-fetch; row is append-only (+1 line). The source cell's "Systematic Reviews 10:39" is not in the capture (it gives only `doi.org/10.1186/s13643-02001542-z`); the lane already says so in the lesson (`R95ScoutSources` F3) |

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` → exit 0, `chousa ok
…/corpus/SOURCES.md`, the same five pre-existing `W04` duplicate-url warnings (S051, S053, S073, S074, S075).

## 5. Trend verdicts

- **expansion: improved** — one admitted knowledge entry on ground the coverage map named as a gap
  (`corpus/README.md:398-399`), `source: S222` (`mined`), plus a SCORECARD capability row.
- **quality: unchanged** — no existing entry was re-verified, deepened or superseded this round, and none was
  found false (LEARNING.md quality observable); the new entry's own strength is credited to expansion/depth, not
  to this trend. Differs from the author's `improved`.
- **discernment: improved** — the outside spot-check agrees with the gate on the admit and the reject; QUALITY
  220–221 each cite a `## Mistakes` row of this round's lesson.

## 6. Routed defects (status-neutral; the lane fixes next round)

- **D1** SKILL.md Gates row for `search-rerun verify` (r95) gives kind `tool`, outside the §Gate standard
  `gate|probe` vocabulary; the script returns a failing verdict against persisted expected values (the record) so
  it is a gate, and `tools/search-rerun.py` has no self-invocation mode (only `verify`). Re-register it as a gate
  naming its self-test (e.g. `rerun-controls-r95.py`) or add a `--selftest`, append-only.
- **D2** `corpus/lessons/round-95.md:23` still says "C2's entry holds nine located quotes"; after Amendment 1 the
  entry holds 13 (`GATE_RECORDS … records=13`). Corrections-sweep miss; append a correction.
- **D3** Report line 95–96 and SCORECARD "No axis harmed" cite `SKILL_TALLY_R94=PASS` / `CURATION_R94=PASS` "on
  the landing tree", but no round-95 receipt carries those runs (`grep -rl` over `corpus/evidence/round95` finds
  none; the only hits are round-94 LOG lines quoted by a seat). Commit the receipt or drop the sentence (the harm
  verdict above rests on this reviewer's own diffs, not on it).
- **D4** S222 source cell carries the unsupported locator "10:39"; the lesson-prose correction does not follow
  CORPUS rule 2 (a correction is a new row whose `teaches` opens `supersedes S222 —`). Decide and record.
- **D5** `corpus/README.md` Round95 row for `tools/search-rerun.py` points at `corpus/evidence/round95/after/`
  (receipts at F); the claimed numbers live in `after-f2/`.

SHONEN: all four boxes are `[~]` with resolvable pointers; box 4 (PROVINCE untouched — `git diff --quiet` exit 0)
and box 2 (8 real searches re-run, reproduced above) look checkable by a non-author. Promotion is operator-owned.
