# Round 96 — non-author verifier spot-check (chousa)

author: hyaku closure (non-author integrator, @m_zfl)

Lane-round: chousa r96 (attempt 1, L1 `ChousaR96`). Base `bbf64970b6c73ca64bcc5f6de2f33b0550459813`, landing
`c8087ac529003e667505bcc624f9a7bde0cffbce`. Report `.ufo/reports/round-96/chousa.md` (fleet repo, commit
`ab9abec87fbc58041ce4b8a3563412493b01d2ae`). Closed 2026-11-09 (UTC). Every measurement below was run by this
reviewer over committed bytes (`git show <hash>:<path>`, `git grep <hash>`), never over the live worktree; the
lane's gates were not executed (PROTOCOL §Gate standard, Closure consequence) — their committed evidence was read.

Driver digest (copied from `.ufo/watchdog.log`, mutable):

```
2026-11-08T21:34:16-03:00 launch chousa round=96 pgid=263490 driver=hyaku-inline attempt=1
2026-11-08T22:49:21-03:00 complete chousa round=96; hyaku-inline attempt=1
```

## 1. Step-1 conformance

| check | command | observed | result |
|---|---|---|---|
| report attribution | `git log --format='%an %H %ci' -- .ufo/reports/round-96/chousa.md` (fleet) | `chousa-shokunin ab9abec8…`, committed 22:48:47 -0300; ancestor of fleet `origin/main` (exit 0) | ok |
| lands last | lane `git log -1 --format=%ci c8087ac5` | `22:48:20 -0300` < report commit `22:48:47` | ok |
| SHONEN heading | `grep -c '^## SHONEN'` report; lane `grep -c '^- \[' SHONEN.md` | 1; 4 lines for 4 boxes, all `[~]` | ok |
| cited hashes | `git -C <lane> merge-base --is-ancestor <h> master` for bbf64970, 2db151c5, e91f82fe, 31810b4e, c8087ac5 | all `commit`, all exit 0 | ok |
| pushed, clean | `jj-lane.sh state <lane>`; `git status --porcelain`; `git ls-remote origin refs/heads/master` | `ahead=0 behind=0 tracked=0 untracked=0`; porcelain empty; remote = `c8087ac5…` | ok |
| prompt contract | grep of `.ufo/prompts/chousa-round-96.md` | §1 MISSION/AXES binding, §2 1–3 claims, §2b frontier step, §3 L2 floor, §4 report contract incl. SHONEN, §5 commit scope, §6 hyaku addendum, §8 pre-file ledger | ok |
| wave settled | `.ufo/waves/round-96/w1-results.json` | 12 results; 12 seat reports under `w1/` | ok |

## 2. Claims — re-check

### C1 `C1-SELFTEST-R96` — operability

Re-measured (plain counts over committed bytes):

```
$ git show bbf64970:SKILL.md | grep -c '^| `search-rerun` (r96 re-registration'      → 0
$ git show c8087ac5:SKILL.md | grep -c '^| `search-rerun` (r96 re-registration'      → 1   (SKILL.md:180, kind cell `gate`)
$ git show bbf64970:tools/search-rerun.py | grep -c -- '--selftest'                 → 0
$ git show c8087ac5:tools/search-rerun.py | grep -c -- '--selftest'                 → 6   (def selftest at :420)
$ git diff --quiet e91f82fe c8087ac5 -- tools/search-rerun.py corpus/evidence/round96/selftest-controls-r96.py → exit 0 (F2 == landing)
$ git show c8087ac5:tools/search-rerun.py | grep -n 'm08-env-scrub'                 → asserts GIT_DIR absent and GIT_NO_LAZY_FETCH=1 only
```

Evidence-verified (committed receipts, revision named in each header):
`corpus/evidence/round96/after-f2/c1-selftest.txt` (`computed_against F2=e91f82fe…`): 32 `SELFTEST … ok` lines,
0 not-ok; split by id prefix p=14, m=8, j=10 (matches the amended sentence); `SEARCH_RERUN_SELFTEST: PASS
cases=32/32`, exit 0. `after-f2/c1-controls.txt`: 23 `CASE mutant … KILLED` lines (0 not killed), 3 oracle cases,
no-write, two r95 regression legs, `SELFTEST_CONTROLS=PASS`, exit 0. `before/c1-base.txt`: argparse exit 2.
The amended (A1-A7) sentence is narrower than the F text in exactly the places the wave falsified it: the 23-site
caveat, NO_WRITE's scope, and m08's guard coverage (confirmed at source above). **Verifies on the narrowed sentence.**

### C2 `C2-ENTRY-R96` — depth

Re-measured over `git show c8087ac5:corpus/knowledge/search-peer-review-dedup-r96.md`:

```
Located quotes (rows | Lnn | Sxxx |)                                     → 32
each quote grep -F in its own capture (S224 → 1a8c36c4…txt, S223 → e94691f5…txt) → ok=32 miss=0
quote multiset of Located-quotes == quote multiset of GATE-RECORD lines   → True (32 = 32)
GATE-RECORD lines / decisions                                             → 33 / admit 32, reject 1
capture_sha256 prefixes vs sha256 of the committed captures               → 86f1aacd… ×18, ce72c920… ×14, both equal
Decision-table rows / Lane cells filled                                   → 8 / 8
Searches Q1-Q8 re-run with `git grep -l` at bbf64970 over corpus/captures/*.txt:
  Q1 2/2  Q2 2/2  Q3 3/3  Q4 4/4 (sha256 of LC_ALL=C-sorted path list = 075e0264… = recorded digest)
  Q5 1/1  Q6 0/0  Q7 3/3  Q8 0/0  — every recorded set equal                → 8/8
$ git cat-file -e bbf64970:corpus/knowledge/search-peer-review-dedup-r96.md → absent at base
$ git diff --quiet bbf64970 c8087ac5 -- tools/research-gate.sh tools/gate-records.py → both unchanged
$ git diff --quiet 31810b4e c8087ac5 -- <entry> <entry battery> tools/       → exit 0 (F3 == landing)
```

Evidence-verified: `after-f3/c2-all.txt` (`computed_against F3=31810b4e…`): `GATE_RECORDS files=1 records=33 ok=33
fail=0` exit 0; `METADATA_COMPLETE=1/1` exit 0; `SEARCH_RERUN_SUMMARY searches=8 rev_match=8/8` `SEARCH_RERUN: CLEAN`
exit 0; `ENTRY_CONTROLS=PASS` with the predicate's tallies, exit 0. Base gap `corpus/README.md:1445` at bbf64970
reads "Left open: PRISMA-S item 14 (search peer review) and item 16 (deduplication) …" — the entry holds both.
**Verifies.**

### Pre-file falsification ledger (addendum §8)

```
$ python3 scripts/hyaku/prefile-falsification.py --lane chousa --round 96
PREFILE-FALSIFICATION: pass claims=2 rows=16 attack_seats=7 findings=0      exit=0
```

8 `falsifies-wording` rows (C1: ReviewerC1, CriticClaims, SentinelC1; C2: ReviewerC2, CriticClaims,
ConnectorSiblings, ExecWrap, ScoutSources), each naming `plans/round-96.md` § Amendments; the claims are filed on
the amended sentences in `claims.md` § Amendments, and the SentinelC1 F1 narrowing matches the tool source. No
unreconciled row.

### No-harm

`git diff bbf64970 c8087ac5 -- SCORECARD.md` is append-only (r96 verdict + planned r97). `SHONEN.md` and
`PROVINCE.md` unchanged; `SKILL.md` +5 lines, `QUALITY.md` +28, `LOG.md` +67, all appends; the two other gates
the entry depends on are byte-identical to base.

| axis | verdict | basis |
|---|---|---|
| operability | **improved** | re-measured: gate row 0→1, `--selftest` absent→present with 32 cases (14/8/10); evidence-verified: self-test PASS, battery 23/23 mutants killed, 3/3 oracles rejected |
| depth | **improved** | re-measured: 32/32 quotes located in their captures, 8 rows, 33 records, 8/8 searches reproduce count and set at base |
| coverage | unchanged | registry 221 → 223 (`grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}'`); PROVINCE untouched |
| freshness | unchanged | no re-verification claim; S224 bytes equal S222's capture |
| calibration | unchanged | no calibration claim; narrowing is conformance, not an axis move |
| adjacency | unchanged | no adjacency claim |

## 3. Discernment spot-check (`corpus/lessons/round-96.md` `## Gate`)

Re-opened 2026-11-09T01:51Z with `curl -sSL` (browser UA) into scratch, PDFs converted with `pdftotext -layout`.

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S223 JCHLA PRESS 2015 abstract | admit, tier B | `https://journals.library.ualberta.ca/jchla/index.php/jchla/article/download/28195/20695/73210` → 200, raw sha256 `0bcdbf0e…`, txt sha256 `ce72c920…` (both equal the record) | agree | quote "that peer review should occur after the MEDLINE search" at txt line 167; tier B is right — a lightning-talk abstract by the guideline authors, not the statement |
| S224 PRISMA-S publisher PDF (second scope) | admit, tier A | `https://jmla.pitt.edu/ojs/jmla/article/download/962/1274` → 200, raw `07036f03…`, txt `86f1aacd…` (equal) | agree | "Describe any search peer review process." at lines 303 and 849; item 16 "Deduplication" at 313; standard's own checklist, by its authors |
| CADTH PRESS E&E PDF | reject (route unreachable) | `https://www.cda-amc.ca/sites/default/files/pdf/CP0015_PRESS_Update_Report_2016.pdf` → 403 (HTML body) | agree | still 403; a route rejection, not a source judgement, correctly recorded with a flip condition |
| J Clin Epidemiol guideline statement | reject (route unreachable, no GATE-RECORD) | `https://www.jclinepi.com/article/S0895-4356(16)00058-5/pdf` → 403 | agree | still 403; but see routed defect D1 on its refetch id |

SOURCES row re-opened: `corpus/SOURCES.md:235` (S223). The row has no quote cell (lane format: id, source, kind,
tier, scope, anchor, teaches, status, opened, recheck, used-by); its quote lives in the lesson GATE-RECORD
(`words=9`, ≤25) and was located above. The `teaches` cell ("kept six review elements, left translation into
other databases to the search developer, review after the MEDLINE search") matches txt lines 159 ("Six existing
PRESS elements were retained"), 171-173 (translation element; "translations be peer reviewed at the discretion
of the …") and 167. Agree.

```
$ scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa   → exit 0, `chousa ok`
  W04 ×6: S051, S053, S073, S074, S075 (pre-existing) and S224 (shares S222's URL across scopes, by design)
```

## 4. Trend verdicts

- **expansion: improved** — one new knowledge entry on the gap `corpus/README.md:1445` named at base; two
  registry rows (221 → 223), both re-opened above.
- **quality: unchanged** — no existing entry re-verified, deepened or superseded (diff shows only appends).
- **discernment: improved** — four of four sampled gate decisions agreed on re-open (2 admits, 2 route rejects);
  tier B chosen over A for an abstract; a second scope opened instead of stretching S222's.

## 5. Routed defects (lane fixes next round)

- **D1 refetch id collision.** `corpus/evidence/round57/refetch.tsv` carries the J Clin Epidemiol 403 attempt
  (`2026-11-09T00:36:09Z`) under id `S224`, which the registry gives to the PRISMA-S re-open. Self-disclosed in
  `## Mistakes` row 3 but not corrected in the TSV: append a correction row (append-only) so the id names one
  document.
- **D2 self-test blind spots (already planned r97).** `R96SentinelC1` F1 (dropping `GIT_NO_REPLACE_OBJECTS`
  yields a false CLEAN past both batteries) and F7 (full `GIT_*` scrub unasserted); `R96MutantsC1` Class B/C
  survivors; NO_WRITE baseline after POSITIVE. The C1 sentence is honestly narrowed around them; they stay debt.
- **D3 four gate-kind tools without `--selftest`** (`R96RevenPrior` Q3) — carried in SCORECARD planned r97 item 3.

Note for the operator: SHONEN boxes 1 (SKILL.md decision tables/checklists with cited sources), 2 (end-to-end
task logged in LOG.md) and 4 (PROVINCE.md accurate, untouched) look checkable by a non-author from committed
bytes; promotion is operator-owned and was not touched here.
