# Round 34 (attempt 2) — non-author verifier spot-check

author: hyaku closure (non-author integrator, @m_kfc)
date: 2026-10-23
lane HEAD verified: `fc93dc5e0059f00cde10d41d16b9241dc33282b6` (base `b80539005176ac6ce39bc1c7afb846cb1f2f7c75`)
report: `.ufo/reports/round-34/chousa.md` (committed by lane identity `chousa-shokunin <chousa@shokunin.local>`, fleet commit `22b0b7ae`)

## Step-1 conformance

- Report committed by the lane identity: PASS (`git log --format='%an %H' -- .ufo/reports/round-34/chousa.md`).
- `SHONEN` heading with one line per box: PASS (4 boxes, all `[~]` — asserted-by-author, closure's call, see below).
- Cited lane commits exist and are ancestors of `master` (branch ref, not `@{u}` — HEAD is detached): PASS for
  `7c7eb3a6 2592f9da fe0f22e0 0af0844c fce3119c 707da818 bd8c8bd8 fe3db76c b8e782a1 0b0af3ef 50a8c693 60b41dad 53e4aa05 fc93dc5e b8053900 f20aeaa7 bf7c931a` (17/17 `git merge-base --is-ancestor <full> master`).
- Pushed: PASS — `jj-lane.sh state` → `ahead=0 behind=0`, local=remote=`fc93dc5e…`.
- Uncommitted round work: DEFECT — 3 untracked files `.ufo/waves/round-34/w2a2/ExecC2Oracle/{boundary-diff,diff-fuzz,pcre-boundary}.txt`
  (late-arriving seat debris; the seat's report never landed). Named in notes; status-neutral.
- Prompt contract: PASS — `.ufo/prompts/chousa-round-34.md` carries §§1–6 (mission/axes SSOT, claims, frontier, L2 floor, report contract, commit/push scope, hyaku addendum).

## Per-claim re-check (commands run by this verifier, observed output)

### C2 — operability (dead-zone spans 32765..32767 bytes): VERIFIED (re-measured)

- Mechanism: `git diff 3026a4e5 fc93dc5e -- tools/research-gate.sh` → the only functional change is
  `TOK_DIRECT_SPAN_MAX=32767` → `=32764` (comment rewrite + selftest cases DD1–DD7 otherwise). Confirms the report's "sole functional line".
- Committed receipts re-read: `c2-before-s5011/s5023.json` → matched 21/37, `predicate_holds=false`, gate_sha `772a1d8e4d94dbf3` (unfixed);
  `c2-after-s5011/s5023/s5033/s5047.json` + `c2-l1-rerun-s7001/s7013.json` → matched 37/37, `predicate_holds=true`, gate_sha `a6307edf687ac0fb` (landed).
- My own measurement (fresh seeds, receipts in scratch):
  `LC_ALL=C python3 corpus/evidence/round34/c2-count.py --seed 8609 --receipt …` → `DEADZONE_MATCH=37/37`, exit 0, all 17 classes full.
  `--seed 8777` → `DEADZONE_MATCH=37/37`, exit 0, gate_sha `a6307edf…`. Both runs ≈8 s.
- Absence sweep: every committed `measure-a2/c2*.json` — no below-37 run binds gate `a6307edf…`; the only 21/37 rows bind the unfixed gate.
- Gate evidence (not executed by me, per §Gate standard): no-harm battery summary 11 rows PASS on gate sha256 `a6307edf…`
  (`.ufo/waves/round-34/measure-a2/battery/battery-a2-summary.txt`); selftest `PASS (256 cases, 0 skipped)` in `selftest-a2.log` and `battery/selftest.log`.

### C3 — calibration (self-audit acquisition): VERIFIED (re-measured + committed evidence)

- My own measurement: `python3 corpus/evidence/round34/self-audit.py` on the landed tree →
  `SELF_AUDIT_MISMATCHES=1` (the single mismatch `audit-tool-digest` carries an in-set disposition: superseded by `audit-tool-digest-v3`),
  `SELF_AUDIT_UNDISPOSITIONED=0` — byte-consistent with the committed `measure-a2/audit-v3-final.txt` (62 `AUDIT id=` lines; `audit-set.json` holds 62 checks).
- Preliminary receipt re-read: 3 counted (2 real + 1 superseded pin), 1 undispositioned — matches the report's before-state.
- Falsification-and-reshape is committed evidence: `w2a2/CritC3Claim.md` (shallow-set do-nothing reproduces 0/0 under planted drift),
  negative control `measure-a2/audit-negative-control.txt` (2 lies → MISMATCHES=2), `w2a2/MutC3Inject.md` (5/5 lies killed by the deepened set).
- The first counted run `measure-a2/audit-first-run.txt` (43 checks, 0/0) is retained as the falsified-then-superseded record. Honest.

### C1 — inherited (spans ≥32768): UNVERIFIED (required controls held) — carried unchanged

- Not re-opened per the frozen design; exclusion record re-opened at `corpus/evidence/round34/claims.md:167-180`
  (five provider-held seats; L1-keyed/L1-windows/halves controls excluded from evidence; no claim rests on them). SCORECARD row unchanged.
- Honest standing, disclosed in report and SCORECARD. Carried debt, routed below.

## No axis harmed

- `git diff b8053900..fc93dc5e -- SCORECARD.md` → 75 insertions, 0 deletions (append-only round rows + correction entry).
- `git diff b8053900..fc93dc5e -- PROVINCE.md` → empty.
- Committed battery holds every prior observable (selftest 256, claims 17/17, chain 17/22, broken 1/2, observable 3/3, five counters at full match).
- Census: `scripts/sources-census.sh validate --root … chousa` → exit 0 (two standing W04 duplicate-URL warnings), matching the report's receipt.

## Discernment spot-check (LEARNING.md §Discernment is checked from outside)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S065 re-open (attempt 2) | admit | `/usr/share/man/man3/pcre2limits.3.gz` | agree | sha256 `a3ea2c67…74bd6` matches the row; quote "The maximum size of a compiled pattern is approximately 64 thousand code units for the 8-bit and 16-bit libraries" verbatim at decompressed lines 10–11; 19 words ≤ 25; used-by adds the dead-zone knowledge entry |
| S064 (attempt 1, anchor-corrected) | admit | `/usr/share/man/man2/execve.2.gz` | agree | sha256 `4489dfef…c8eab0dc` matches; the 20-word MAX_ARG_STRLEN quote present; URL recorded-not-fetched is disclosed in the row and the standing L0 queue |
| S066 (attempt 1) | admit | `/usr/share/man/man1/grep.1.gz` | agree | sha256 `9b027d02…85ba` matches; the 7-word `-f` quote is the rendered form of roff-split lines 242–244; the binary-provenance hazard (self-reports pi-uu-grep 0.2.0) is named in the row's host note and report, routed to r35 |
| L1-built controls for held seats | reject | `corpus/evidence/round34/claims.md:167-180` (exclusion record) | agree | safety rule: provider-held seats' controls re-authored by the L1 are excluded from evidence; verified no C2/C3 verdict cites an L1-keyed receipt |
| man7.org fetch | reject (not opened) | `.ufo/l0-questions.md` (standing registered-source rows) | agree | unregistered host; installed copies of the same pages opened instead; disclosed, not bypassed |

No disagreement in the sample. Census validation re-run by me: exit 0.

## Trend verdicts (non-author)

- expansion — **improved**: new measured surface (spans 32765–32767), a capabilities row, and the dead-zone knowledge entry on previously undocumented ground; verified present at `corpus/knowledge/dead-zone-pcre-r34.md`.
- quality — **improved**: the chunk matcher gains demonstrated-failing selftest cases (able-to-fail receipt `measure-a2/deadzone-fixture-vs-gates.txt` re-read); S065 pins hold under my re-open; the 4/37 design expectation carries a committed post-data erratum (claims-a2.md §Erratum) rather than a silent wrong number.
- discernment — **improved**: C3 was falsified by a wave critic and reshaped within the round to an instrument whose count demonstrably moves on drift (before 3/1-undispositioned → after 1-dispositioned/0, re-run by me); my outside sample agrees with every gate decision checked; both attempt sections mine mistakes with fixes shown able to fail.

## SHONEN note for the operator (promotion is operator-owned)

All four boxes are `[~]`. As the non-author verifier I confirm the underlying evidence is checkable and consistent:
SKILL.md registry rows cite the exact `PASS (256 cases, 0 skipped)` banner and the correct case ranges (254–256 dead zone);
the committed battery selftest log and `selftest-a2.log` carry the same banner; PROVINCE diff empty; the end-to-end verify-all evidence is logged (r9 re-execution by a wave seat — lane-dispatched, so it does not itself qualify per PROTOCOL). A named outside reviewer can close these boxes next round.

## Routed defects (for the lane's next round)

1. **Uncommitted wave debris (new)**: `.ufo/waves/round-34/w2a2/ExecC2Oracle/{boundary-diff,diff-fuzz,pcre-boundary}.txt` — commit under a wave entry or remove; reconcile the report's "23 of 33 committed" against the 24 `.md` reports on disk and ExecC2Oracle's partial run (files without a report).
2. Selftest-case comment numbering in `tools/research-gate.sh` ("cases 255-257" vs actual 254-256) — already wave-routed to r35 (comment-only churn constraint); re-confirmed.
3. Host grep provenance (`/usr/bin/grep` self-reports pi-uu-grep 0.2.0 vs pacman grep 3.12-2; gate resolves bare `grep` at research-gate.sh:1618/1641/1687) — already wave-routed: r35 pins the binary and verifies provenance.
4. `slen` dynamic-scope coupling at `research-gate.sh:1631` — already wave-routed: r35 `slen=${#2}`.
5. C1 carried debt: spans ≥32768 remain `unverified (required controls held)`; the next C1-touching round must re-open verification with the exclusion intact, or retire the claim honestly.
