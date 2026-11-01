# Round 70 claims (frozen 2026-11-01 at commit A, against base `1db6babf528692d871a2b97be0b3e519614fa300`)

Host: Windows/11, `python -I` (3.13.15) replaces `python3` throughout. Correction to the r69
claims file's host line ("no `python3` on this host"), measured this round: a `python3` alias
EXISTS at the WindowsApps store-stub path and `command -v python3` succeeds against it, but
executing it prints "Python was not found" and fails — an existence-vs-capability gap the gate's
four `command -v python3` guards (base lines 5550, 6691, 7890, 7921) do not survive; C1's repair
probes capability, not existence. Fetches: none this round — every ground is own-work committed
bytes opened this round (S168–S172), so nothing beyond the lane repository is read; the standing
r40/r65 fetch-scope and L2-floor template L0 questions stay open and are routed around, never
treated as answered. No wave: this host has no batched dispatch surface (round-63 attempt-2
precedent, disclosed every round since); every verdict rests on committed counters, controls and
receipts. One reconnaissance run of the gate selftest executed in a scratch copy (S171: base bytes
modified only by the one-line h1 crash guard; diagnostic only, never a measurement of committed
bytes; its full transcript is committed as the capture the row pins).

Trigger: the round-69 closure spot-check (S172) routed exactly two lane items to this round —
(1) the G08 full-run receipt owed since r66 (the skip chain is four receipts old, S168); and
(2) the semantic counter's filler-author residual, whose non-author entailment review bar has
been carried as prose since r66 with nothing actionable behind it.

## C1 — operability (lowest-scored non-retired axis, 3/10)

The G08 check has never produced a full-run receipt on this host, and the reconnaissance (S171)
shows why no honest full run was possible: the battery cannot even finish. Four measured defect
classes, all host-dependence, none a verdict-path bug: (D1) the preflight's frozen 1500 s budget
is un-meetable here (`controls/before-g08-budget.txt`: >1650 s elapsed at case 59 with no verdict
line); (D2) on a flock-less host the manifest-append critical section fails closed BY DESIGN
(S169) and every case that needs a manifest write or a pin/drift capture therefore fails — 2
manifest cases plus the whole pin/drift capture zone (~20 case sites across the r35–r39 sections);
(D3) the guarded `python3` sites trust existence, and this host's python3 is a non-running stub;
(D4) three bare statements manipulating capture products kill the whole battery under `set -euo
pipefail` instead of failing their own case (the h1 assignment, base line 5560, measured by the
recon at case 60; the drift-vol-list sed, base line 5977; the r36 sed -i, base line 8375, found
by the repair-scope scan). This round lands the smallest repair that makes the battery COMPLETE
and TRUTHFUL on this host — it finishes, prints its verdict line with every remaining failure
named and every unrunnable-subject case skipped by name with a reason — then runs the preflight
full (no `--skip`) and commits that receipt too:

  a. `tools/lane-preflight.py` — the g08 budget becomes overridable via `G08_SELFTEST_BUDGET_S`
     (default 7200 s); no other gate, line or behavior changes; every edit sits below the G05
     parser guard the r69 note cites, so line 233 stays byte-identical (verifiable: the landing
     diff has no hunks above the g08 function);
  b. `tools/research-gate.sh` — inside `run_selftest` only (every hunk at line >= 4378): the
     three crash guards (D4); a one-time host-capability probe (`HAVE_FLOCK`, `PY3` — executes
     python3 once); flock-conditional skip-case wiring for exactly the cases whose SUBJECT is the
     manifest append itself (verify-all-manifest-append, verify-all-manifest-two-appends,
     json-unterminated-manifest, json-nul-terminated-manifest, c1lk-second-append,
     all-manifest-hash-shim) reusing the battery's own skip pattern (S170) so the designed
     fail-closed contract (S169) is preserved and honestly skipped, never faked; the four
     `command -v python3` guards become the capability probe; `SKIPPED` moves to the top of
     run_selftest (the r14 block kept resetting it, losing skips counted before cases 103+); the
     pin/drift capture cases are NOT skipped — they run and name their failure (the capture is
     flock-blocked), because a host flock(1) install — the operator decision this round files to
     the L0 queue — would make them pass for real; no existing case's input, expected rc, or
     expected token changes (the two `tall ... r6-manifest.jsonl` case lines keep their literals
     inside the new conditional, re-indentation disclosed);
  c. after-predicates, measured at the landing tip:
     `controls/after-battery-completes-r70.txt` — the repaired battery's own run completes and
     prints its verdict line (`RESEARCH_GATE_SELFTEST: FAIL (k/N cases, K skipped)`, rc=1 by
     immediate `rc=$?`), with the manifest-case skips printed by name and every pin/drift and
     manifest failure a named FAIL-case — a completing truth-telling battery, where the base
     battery died silently (rc=2, no verdict, S171);
     `.ufo/waves/round-70/preflight-final.txt` (copied to `controls/after-full-preflight-r70.txt`)
     — the preflight run with NO `--skip`: the G08 line names its real result, the summary carries
     `SKIPPED=none`, and `EXIT=` is read by immediate `rc=$?`; the receipts pin both tools' sha256
     and the pins re-derive via `tools/digest-in-tree.py` at HEAD.

  Verdict rule, frozen before measurement: battery completes with verdict line + preflight
  completes with `SKIPPED=none` → C1 improved on the frozen predicate (the skip chain ends: a
  full-run receipt exists and the battery's own verdict line replaces a silent crash), with the
  G08 gate's red state disclosed everywhere it is cited — the gate itself is NOT claimed improved;
  if the repaired battery still dies before its verdict line, or the preflight cannot complete,
  C1 lands honest-stop with the red receipts committed as the defect record and the residual
  routed; no predicate is edited after measurement.

  Counting commands (paste-able; receipts name the revision measured):
  `grep -c "RESEARCH_GATE_SELFTEST:" corpus/evidence/round70/controls/before-g08-selftest-partial.txt` → 0
  and the recon capture (S171) shows the case-60 death with rc=2 and no verdict line;
  `grep -c "RESEARCH_GATE_SELFTEST: FAIL" corpus/evidence/round70/controls/after-battery-completes-r70.txt` → 1;
  `grep -rl "GATE G08 gate-selftest PASS" .ufo/waves/ | wc -l` → 0 at the base
  (`controls/before-g08-skip-chain.txt`: four receipts carry `SKIPPED=G08`);
  `grep -c "SKIPPED=none" corpus/evidence/round70/controls/after-full-preflight-r70.txt` → 1.

  Routed with the claim, not hidden: the gate's G08 red is the honest standing state until the
  host gains flock(1) — filed to the L0 queue this round (operator-owned host change; on install,
  the ~20 capture-zone cases flip to real runs with zero skips) — or until a later round lands
  the full skip-surgery with its coverage cost spelled out. The budget default (7200 s) is a
  disclosed host constant.

## C2 — calibration (sourced on S172, opened this round)

The residual has been carried since r66 as "a non-author entailment review remains the real bar"
with nothing actionable behind the bar: at the base, `git grep -c "entailment-review"` over the
registry and records hits 0 files (`controls/before-entailment-packet-greps.txt`). This round
lands the author-side half of the closure:
`corpus/evidence/round70/entailment-review/` — `PROTOCOL.md` (who reviews: a fresh non-author
session not dispatched by the lane author, operator-scheduled, per the r69 spot-check item 5
SHONEN precedent; the 12-claim scope over the four counter-passed entries; the per-claim
procedure bound to QUALITY 8's support states; the closure rule), `review-record.template.md`,
`claims-scope.tsv`, `record-format-check.py` (format only; its docstring states it cannot check
verdict correctness), two fixtures, and a committed battery (`controls/format-battery.txt`) shown
able to fail: valid fixture `RECORD_FORMAT=2/2 REVIEW_FORMAT=PASS` exit 0; broken fixture
`RECORD_FORMAT=0/3 REVIEW_FORMAT=FAIL` exit 1 naming seven defects; absent record ERROR exit 2.
The non-author review itself is requested on record (round report + lesson `## Gate`) as an
operator-scheduled act.

  Limits, frozen with the claim: the packet does NOT close the residual — a passing format check
  says nothing about verdict correctness; the residual stays open until a committed non-author
  review record exists, and the counter's filler-author class stays disclosed everywhere it is
  relied on.

  Counting commands: `ls corpus/evidence/round70/entailment-review | wc -l` → 6 (before: the
  path is absent at the base); `python -I corpus/evidence/round70/entailment-review/record-format-check.py
  --record …fixtures/record-valid.md --scope …claims-scope.tsv --root .` → exit 0; the broken
  fixture → exit 1 (before both: exit 2, path absent — `controls/before-entailment-packet-greps.txt`).
