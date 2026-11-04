# R76ExecB — independent derivation of the twelve loader-matrix case expectations

Written **before** opening `corpus/evidence/round76/loader-matrix-v3.py` (or any other matrix
source: `matrix-battery-v3.py`, `round75/loader-matrix-v2.py`, `round74/loader-matrix.py`,
`round76/forgers/`, `round76/controls/`). Sole inputs: the docstring and `check()` of
`corpus/evidence/round74/correction-count.py` (sha256 `9334721a5e7a4080255b478771bf5443739738fb1936b40c116da28d7fa8ac41`)
plus the C1 claim sentence in `round76/claims.md` (which names only the count — twelve — and the
r75 oracle failures, not any per-case content).

## Contract model (from the round74 counter)

The counter is a pure scorer over committed bytes:

- `check(files, deleted, changed)` returns exactly **7** results, ids `C2-1` … `C2-7`
  (`[("C2-1", ok, detail), …]`), one per documented check.
- `deleted` = removed-line counts per protected path from `git diff --numstat <base> <rev>`
  (non-digit numstat → `1`), `changed` = receipt paths differing base→rev (name-only).
- CLI contract: rc **0** + `C2=PASS checks=7/7` iff all checks pass; rc **1** + `C2=FAIL` iff any
  fails; rc **2** usage (`--rev`/`--base` required). `--selftest` is in-memory, never reads a lane.

So a loader-matrix case is one committed fixture state fed through the real public CLI over
`base→rev`; the natural expectations to compare are, per case, `expected_rc` ∈ {0,1} and
`expected_failed` = number of checks the contract forces to FAIL (0 for a compliant fixture, 1 for
a single-fault mutation; k if a mutation touches k checks).

The seven requirements each check enforces (from `check()`):

| id | requirement over the fixture bytes |
|----|------------------------------------|
| C2-1 | `LOG.md` contains **exactly one** line equal (after rstrip) to `## Round 72 correction entry` |
| C2-2 | that (last) LOG entry section contains `8426`, `8435`, `exempt` |
| C2-3 | lesson contains exactly one anchored `## Correction — round-72 spot-check` AND its section contains `V72-1`, `V72-2`, `8426`, `8435`, `7f7ea19a`, `6dd6c82` |
| C2-4 | `SCORECARD.md` exactly one anchored `## Round 72 correction note`, section contains `V72-1`, `V72-2` |
| C2-5 | lesson section contains all three tree phrases (`measured at the landing tip 7f7ea19a`, `three at the verdicts tree 6dd6c82`, `two recorded`) |
| C2-6 | numstat removes **0** lines from each of `LOG.md`, `corpus/lessons/round-72.md`, `SCORECARD.md` |
| C2-7 | neither r72 receipt path changed base→rev |

## Independent case enumeration (12)

One compliant positive plus eleven single-fault mutations — one per distinct violation shape the
contract distinguishes. Each mutation flips exactly one check, so each expects `rc=1, failed=1`.

| # | case (my name) | mutation of the compliant fixture | check flipped | expected rc | expected failed |
|---|----------------|-----------------------------------|---------------|-------------|-----------------|
| 1 | compliant | none (the counter's own FIXTURE) | — | 0 | 0 |
| 2 | anchor-absent | LOG heading line renamed/removed (0 anchors) | C2-1 | 1 | 1 |
| 3 | anchor-duplicated | LOG heading line appears twice (2 anchors) | C2-1 | 1 | 1 |
| 4 | log-token-broken | `8435` replaced (e.g. `:8436`) in LOG entry | C2-2 | 1 | 1 |
| 5 | lesson-name-missing | lesson block drops `V72-2` | C2-3 | 1 | 1 |
| 6 | lesson-anchor-duplicated | lesson heading twice | C2-3 | 1 | 1 |
| 7 | card-heading-renamed | SCORECARD note heading renamed (0 anchors) | C2-4 | 1 | 1 |
| 8 | tree-phrase-broken | `three at the verdicts tree` replaced | C2-5 | 1 | 1 |
| 9 | one-line-removal | delete one LOG.md line base→rev (numstat −1) | C2-6 | 1 | 1 |
| 10 | whole-file-removal | a protected path fully removed (numstat deletion; non-digit → 1) | C2-6 | 1 | 1 |
| 11 | receipt-modified | receipt bytes differ base→rev | C2-7 | 1 | 1 |
| 12 | receipt-deleted | receipt removed (name-only still lists it) | C2-7 | 1 | 1 |

Predictions: case 1 → `expected_rc=0, expected_failed=0`; cases 2–12 → `expected_rc=1,
expected_failed=1` each. A case is mis-derived if the matrix scores a shape my table has no row
for (extra case class) or assigns an expectation contradicting `check()` (e.g. expecting rc 0 or
`failed=0` for a state where a documented check must fail, or rc 1 for the compliant fixture).

Derived but *not* scored cases (protocol, not fixture states): missing `--rev`/`--base` → rc 2;
`--selftest` → `SELFTEST=PASS mutations=7/7`, never touches the lane.

## Comparison protocol

After this file is written I will read the matrix source, run it once against
`round74/correction-count.py` with `LOADER_MATRIX_CHILD_TIMEOUT=10`, and tabulate each printed
`expected_rc=`/`expected_failed=` against the table above. Report `EXPECTATIONS=12/12` or every
mismatch with both sides. Salt/order mechanism witness: instrumented scratch copy printing the
base fixture tree id per run; two runs must differ in tree ids and case order.
