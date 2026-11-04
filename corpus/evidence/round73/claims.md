# Round 73 claims (frozen before measurement; fresh-start round after three rejected closures)

Base `f748abbb6bf58388e732facd4ecec5612419c457` (the round-72 verifier spot-check tip — the lane tip at this
freeze). Host: **Linux 7.2.11-arch1-1, 32 cores, omp** — the run-15 host, where the three host reasons the
r70/r71/r72 chain cited are measured absent before this freeze (`controls/probe-r73-sizing.txt`):

- `flock(1)` PRESENT at `/usr/bin/flock` and locking (`flock -n <path> -c true` → rc 0); the gate's manifest
  critical section (lines 3970–3981) runs instead of failing closed.
- `timeout(1)` KILLS (`timeout 1 sleep 5` → rc 124), so the r71 locale-boundary wrap's capability probe passes.
- `python3` EXECUTES (3.14.8, the r70 existence-vs-capability lesson) and `/proc/self/fd` exists (the gate's
  fd probe path), `bash` 5.3.20.
- The case-258 (`claims-locale-boundary`) body reproduced verbatim runs **22.58 s, rc 0, `RESEARCH_GATE: CLEAN`**
  on this host (the r72 quiet-window body was 18.131 s) — the 900 s default budget stays ~40x.
- Pre-freeze preflight sizing with G08 skipped: **`PREFLIGHT=7/7 FAILED=none ENV=none SKIPPED=G08`** in 1.79 s
  (G01–G07 green on this host; the r67 NTFS/freeze-check drift does not exist here).

No fetch this round: every ground is own-work committed bytes opened this round (S180 admitted, S181 rejected;
`corpus/lessons/round-72-verifier-spotcheck.md` §6 and the r72 receipts). Wave: one v1 wave of 11 seats under
`ufo-wave-policy.json` (band 8–16) via the run-15 inline spawn handoff, written to
`.ufo/waves/round-73/w1.ready`; the L1 holds the canonical planner seat (the validator rejects a planner role).

Exactly two claims, causally separable: C1's verdict rests on its own two fresh receipts; C2's on its seven
committed checks. Neither needs the other to have landed.

**Fresh-start check (run-15 rule: "-chousa r70–72 rejected on the Windows host (no flock, sibling load)").** The
last three closures were read this round before declaring: r70 `rejected-honest-stop`, r71 `rejected-honest-stop`,
r72 `rejected-honest-stop`, all three on the same completing predicate (SCORECARD round-70/71/72 verdicts and
`corpus/lessons/round-70/71/72-verifier-spotcheck.md`). The failures those closures name are host reasons this
host does not have; C1 is therefore **re-measured here** (fresh receipts at this host) and never re-declared from
the old receipts. Both claims below are unreachable by a do-nothing round: see each claim's control.

## C1 — operability (the lane's lowest-scored non-retired axis, 3/10)

The completing run re-pursued on this host with the r71 timeout-wrap in force and the tool bytes unchanged
(in-tree `tools/research-gate.sh` sha256 `d5d48128509f77edf161e4d8b10b833e6e00f822906460fa049f27d1244d41e2` =
the r71 landing blob; `before-r73-greps.txt` re-derives it).

The rule, **carried unchanged from the r70/r71/r72 claims files**: **battery completes with its verdict line
(anchored `^RESEARCH_GATE_SELFTEST:` count 1) + preflight completes with `SKIPPED=none` (its G08 line naming its
real result) → improved ON THAT PREDICATE**, with the gate's actual result (PASS or FAIL, and the ok/FAIL/skip
case tallies) disclosed everywhere the predicate is cited and the operability score unmoved; **if the bounded
battery still dies before its verdict line, or the preflight cannot complete within its budget → honest-stop
again**, receipts committed as the defect record and the residual routed. No predicate is edited after
measurement, and no measured FAIL is reported as a pass.

Sizing (measured at this freeze, `controls/probe-r73-sizing.txt`): the case-258 body 22.58 s against the
**900 s `LC_BOUNDARY_BUDGET_S` default left UNSET** (~40x the body); `G08_SELFTEST_BUDGET_S` left UNSET (the
preflight's 7200 s default; G01–G07 measured 1.79 s, leaving the full battery inside the budget). Both env
knobs stay unset in the measured runs.

Method discipline (the r70/r71/r72 lessons applied): **single writer** — the direct battery runs to completion
before the preflight starts; receipts land at `controls/battery-r73.txt` and `controls/preflight-r73.txt`, the
first header line naming the measured revision (`git rev-parse` read-only) and the unset budgets; a receipt
header line never begins with the verdict token; every count line in a receipt is re-run immediately before the
commit that carries it.

**Do-nothing control** (frozen in `controls/before-r73-greps.txt` at the base): the r72 receipt's anchored
verdict-line count is **0** and no r72 preflight receipt exists, so a do-nothing round leaves both counters
unmet. A receipt that merely repeats the r72 bytes cannot reach C1.

Counting commands (re-derived by the closure at the landing tip):

```sh
grep -c '^RESEARCH_GATE_SELFTEST:' corpus/evidence/round73/controls/battery-r73.txt   # expected 1
grep -c 'SKIPPED=none'             corpus/evidence/round73/controls/preflight-r73.txt # expected 1
grep -c '^PREFLIGHT='              corpus/evidence/round73/controls/preflight-r73.txt # expected 1
```

## C2 — calibration (sourced on S180, opened this round)

The two routed defects of the round-72 verifier spot-check (`corpus/lessons/round-72-verifier-spotcheck.md` §6,
opened this round as S180), corrected append-only and status-neutral to the r72 rejected-honest-stop ruling — the
r72 verdicts, predicates and receipt bytes stay undisturbed:

1. **V72-1 (kill-line precision).** The r72 narrative (receipt header, LOG, SCORECARD) says "the unguarded grep
   on the missing file kills the script under `set -euo pipefail`". The grep at
   `tools/research-gate.sh:8426` is `set -e`-exempt inside its `&&` list — it supplies the receipt's visible
   symptom line only; the process exit is the next unguarded sub-run assignment at
   **`tools/research-gate.sh:8435`**, inheriting the flock-less `--pin` child's designed rc=2. Neither line
   number is recorded in any r72 artifact. Landing: an append-only LOG correction entry, an append-only
   correction block in `corpus/lessons/round-72.md`, an append-only SCORECARD correction note, plus the
   empirical survival harness receipt (`controls/v72-killline-harness.txt`) re-derived this round.
2. **V72-2 (measurement-tree context).** `corpus/evidence/round72/controls/after-r72-corrections.txt` heads
   "every count line re-run fresh at the verdicts tree" while its own recorded `git rev-parse HEAD` is
   `7f7ea19a` (the landing tip); its counts re-derive there (SCORECARD "18 healthy" = 2), while at the verdicts
   tree `6dd6c82` the verdict row's own quotation adds a third hit (**three at the verdicts tree `6dd6c82`
   against two recorded**). A count line's tree is part of its re-derivation context. Landing: the same three
   correction records state the tree explicitly, and the round-73 report carries the erratum.

**Frozen counter** (`corpus/evidence/round73/c2-count.py`, committed with this file; its seven-check contract
is in its docstring, and `--selftest` catches one mutation per check: `SELFTEST=PASS mutations=7/7`):

```sh
python3 -B corpus/evidence/round73/c2-count.py --lane . --rev <landing-tip> --base f748abbb6bf58388e732facd4ecec5612419c457
# expected: CHECK C2-1..C2-7 PASS; C2=PASS checks=7/7
```

**Do-nothing control** (`controls/before-r73-greps.txt`, red at the base): the same counter at the base prints
`C2=FAIL checks=2/7` — C2-1..C2-5 fail (no correction record exists; the defect texts stand), C2-6/C2-7 pass
vacuously. The fix is the only delta between the red and green runs; `controls/v72-killline-harness.txt` shows
the exempt/kill distinction empirically, and the counter's own mutations show each check can fail.

## Non-goals (declared, not claimed)

No tool bytes change this round (the r72 crash site is a record-precision defect, not a gate defect this round
fixes); the pin-zone isolation probe the wave runs is evidence about this host, not a claim. `operability` stays
3/10 on its historical narrow observable; a capability row enters only if a claim demonstrates it running, and
this round's C1 is a measurement of an existing instrument, so no capability row is pre-claimed.
