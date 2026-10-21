# FC2 falsify — C2 control `max-date-overflow` @ dd72641e

Agent: `ChousaR27.FC2MaxDateOverflow13-11`. Sandbox: `/tmp/chousa-r27-falsify-FC2MaxDateOverflow13` (git archive of `dd72641e574679c4f7882dd43de072b4c8892d6f`; lane gate sha256 `ca39d14db907ec3fcf41ff0593658b4d6831fa82452944fe1f58463364992f84` verified before extraction). No installs. No full `--selftest` and no whole regression script was run; every probe below is a single `verify-metadata` gate command against a temporary fixture, run sequentially. Bash 5.3.20, Python 3.14.8.

## Verdict

- **Landed gate behavior for this input class: HOLDS.** No counterexample to the contract was found on the landed gate; every nearby boundary probe matches a Python `datetime` oracle.
- **Control as evidence for the C2 repair: FALSIFIED.** `max-date-overflow` already passes on base `64eec5d` with the identical production code; it passes with the round-27 `metadata_add_days` change reverted; and it passes for a mutant that refuses *every* cadence date in year 9999, which violates the C2 clause "Preserve year1–9999". It is a legitimate negative guard for a pre-existing range check, but it has no discriminating power over the round-27 repair and no paired positive boundary case.

## (1) Is the expectation derived from the contract, independent of gate code?

Yes, with one provenance nit.

The row is `('max-date-overflow', '9999-12-31', '1d', '9999-12-31', None)` in `corpus/evidence/round27-regressions.py:104`. `observe()` then requires exit `0` (`int(freshness == 'overdue')` with `freshness='unknown'`), the literal substring `due=unknown freshness=unknown`, one `^RESEARCH_GATE: ` and one `^META entry=` line. Nothing in this row reads the gate text; the regression script reads `text` only to extract the C1 usage helpers. The expectation follows from the C2 contract line "out-of-range values remain unknown" and "Preserve year1–9999".

Independent oracle (Python `datetime`, run in the sandbox):

```
date.max        = 9999-12-31
min+3652058     = 9999-12-31
min+3652059     -> OverflowError date value out of range
max+1           -> OverflowError date value out of range
max+0           = 9999-12-31
```

So the expected `unknown` is the contract's out-of-range result, not an encoding of the gate's implementation. The only gate-dependent element is the output *format* (`due=… freshness=…`), which is unavoidable for a black-box assertion.

Nit: the script comment "Calendar expectations derive from Python datetime" is not literally true for this row — `None` is a hand-written literal (it is correct per the oracle above, and the `leap-*` rows do call `datetime`). Same wording issue the sibling FC2 reports note; not a defect in the expectation.

## (2) Mutation evidence: which production change does it target?

**It targets no round-27 change.** Base `64eec5d` already contains the entire range guard:

```
metadata_add_days() {                       # base 64eec5d, identical in landed
  ...
  metadata_days_from_civil 9999 12 31
  last_day=$META_DAYS
  ((amount <= last_day - start)) || return 1
  metadata_civil_from_days "$((start + amount))"
}
```

The round-27 diff of `metadata_add_days` is only: `local LC_ALL=C`, ASCII digit class `[0123456789]`, and the leading-zero normalizer `[[ $digits =~ ^0*([123456789][0123456789]*)?$ ]]` replacing extglob `digits##+(0)`. The max-date fixture (`recheck: 1d`) touches none of those.

Consequences, each measured:

| # | mutant | max-date-overflow result |
|---|---|---|
| base `64eec5d` | — | **PASS**: `due=unknown freshness=unknown verdict=clean`, rc 0 |
| `mutR` | landed with the base `metadata_add_days` body restored (round-27 fix reverted) | **PASS**: rc 0, exact expected string |
| `mutA` | pre-existing range guard removed | FAIL, rc 1 — but by gate crash, not assertion |
| `mutA2` | overflow clamps to `last_day` instead of unknown | FAIL, clean semantic mismatch |
| `mutB` | `last_day` off by one (`9999 12 30`) | **PASS** (max-span fails instead) |
| `mutD` | blanket refusal of year-9999 cadence dates (see §3) | **PASS** |

Commands (representative):

```
bash tools/research-gate.sh verify-metadata corpus/knowledge/entry.md --root . --as-of 9999-12-31
# landed:    META ... due=unknown freshness=unknown verdict=clean ; RC=0
# base:      META ... due=unknown freshness=unknown verdict=clean ; RC=0
# mutR:      META ... due=unknown freshness=unknown verdict=clean ; RC=0
```

`mutA` (guard deleted) output, verbatim:

```
../mut/mutA-guard-removed.sh: line 2356: 10#: invalid integer constant (error token is "10#")
RC=1
```

The gate computes `due=10000-01-01` from `metadata_civil_from_days`, then `metadata_days_from_iso "$due_date"` (line 2356, `month=${1:5:2}` = `-0`) aborts under `set -euo pipefail` before any `META` line. The control therefore fails on exit code and missing string, and the failure *cause* is the removed overflow guard, but the intended assertion (`due=unknown freshness=unknown`) never evaluates — the failure mode is a crash. This is also an observation about defense in depth: line 2780's freshness comparison is not robust to an out-of-grammar due date; the landed guard is the only thing making that path unreachable. No reachable landed path producing an out-of-grammar due was found.

`mutA2` clamps instead of rejecting (`if ((amount > last_day - start)); then metadata_civil_from_days "$last_day"; return 0; fi`). The control then fails cleanly at rc 0 with `due=9999-12-31 freshness=current` — the assertion itself distinguishes closest-valid-day from unknown.

`mutB` (`last_day` = 9999-12-30) shows the control alone cannot monitor the boundary *value*: the control still passes because 9999-12-31's start is greater than the mutated last day, so it returns unknown for the "wrong" reason; `max-span` (`0001-01-01 + 3652058d`) is the row that kills this mutant. Conversely `mutD` survives both.

**Interpretation.** Reverting the actual C2 fix leaves the control green, so the control supplies no before/after evidence for the repair; the claimed baseline failures were `FDateAsOfUsage` and `FDateHugeCadence`, not overflow. It still adds contract-preservation value for the pre-existing bound, but "Independently persisted controls include … overflow" must not be read as evidence that the overflow path was repaired in round 27.

## (3) Nearby same-class inputs

**Landed gate — all correct** (each a single gate command, fixture `verified-at: <v> …`, `recheck: <r>`, `--as-of <a>`; expectations cross-checked with the Python oracle):

| verified | recheck | as-of | landed result | rc |
|---|---|---|---|---|
| 9999-12-30 | `1d` | 9999-12-31 | `due=9999-12-31 freshness=current` | 0 |
| 9999-12-31 | `0d` | 9999-12-31 | `due=9999-12-31 freshness=current` | 0 |
| 9999-12-30 | `2d` | 9999-12-31 | `due=unknown freshness=unknown` | 0 |
| 9999-12-31 | 131072×`0` + `d` | 9999-12-31 | `due=9999-12-31 freshness=current` | 0 |
| 9999-12-31 | 131072×`0` + `1d` | 9999-12-31 | `due=unknown freshness=unknown` | 0 |
| 9999-12-31 | date-form `9999-12-31` | 9999-12-31 | `due=9999-12-31 freshness=current` | 0 |
| 9999-12-31 | date-form `0001-01-01` | 0001-01-02 | `due=0001-01-01 freshness=overdue` | 1 |
| 0001-01-01 | `0d` | 0001-01-01 | `due=0001-01-01 freshness=current` | 0 |
| 0001-01-01 | `0000000003652058d` | 9999-12-31 | `due=9999-12-31 freshness=current` | 0 |
| 0001-01-01 | `0000000003652059d` | 9999-12-31 | `due=unknown freshness=unknown` | 0 |

No landed wrongness in this class was found.

**Control vacuity — minimal counterexample.** Mutant `mutD` inserts into `metadata_add_days`, after the character checks:

```
if (( 10#$year == 9999 )); then return 1; fi
```

This gate is wrong: `verified-at: 9999-12-30` + `recheck: 1d` is representable and must yield `due=9999-12-31` (Python: `date(9999,12,30)+timedelta(days=1) = 9999-12-31`), yet it emits `due=unknown freshness=unknown verdict=clean`, rc 0. The exact control invocation against `mutD` (absolute entry/root, `cwd=root`, CHOUSA_* stripped, `LC_ALL=C`, `CHOUSA_STRICT=0`, timeout 30) produces precisely the expected observation:

```
META entry=entry.md source=present verified_at=dated recheck=scheduled due=unknown freshness=unknown verdict=clean
METADATA_COMPLETE=1/1
RESEARCH_GATE: CLEAN (entries=1 complete=1 findings=0 drift=0)
RC=0
```

and all 14 C2 `date_cases` (including `max-span`, `overflow-span`, `max-date-overflow`, `decimal08/09`, the four leap rows) pass under `mutD` in my scoped probe. Only my two extra rows (`9999-12-30`+`1d`, `9999-12-31`+`0d`) expose it. The suite has no positive row whose `verified-at` is in year 9999: `max-span` starts at `0001-01-01`, so year 9999 is only exercised as an *output* of `metadata_civil_from_days`, never as an accepted input date. The gate's own selftest has the same blind spot: its only year-9999 fixture is `meta-asof/date-overflow.md` (`verified-at: 9999-12-31`, `recheck: 1d`), which also expects `unknown` (`tools/research-gate.sh:6160-6172`).

Consequently `max-date-overflow` observes `due=unknown` but cannot distinguish "overflow correctly rejected" from "year-9999 input dates mishandled" — the negative half of the boundary is tested and the positive half is not.

For completeness, `mutC` (reject year 9999 inside `metadata_iso_date`) also fails this control, but only because the same function validates `--as-of 9999-12-31` and returns rc 2 (`--as-of must be a valid YYYY-MM-DD date`). That is a usage error, not a demonstration of vacuity; `mutD` is the cleaner counterexample because it leaves `--as-of` parsing intact.

## Smallest safe correction (author-lane advice)

1. Add one paired positive row of the same class, e.g.
   `('max-date-representable', '9999-12-30', '1d', '9999-12-31', '9999-12-31')`
   and/or `('max-date-zero', '9999-12-31', '0d', '9999-12-31', '9999-12-31')`
   (expected `due=9999-12-31 freshness=current`, rc 0). Either row kills `mutD` and `mutB` and turns the boundary into a two-sided test.
2. Keep `max-date-overflow`, but reclassify it in the claims/report: it was already green at base `64eec5d`, so it is a preservation guard for the pre-existing `metadata_add_days` bound, not evidence that round 27 repaired overflow behavior. C2 repair evidence stands on the locale and long-leading-zero controls, which do change base→landed behavior.

Axes impacted: calibration (negative-only boundary assertion, base-green control presented among repair controls) and freshness (strength of the after-evidence). Operability: no impact; no production defect found. This is a fixable control-design defect, not a tradeoff.

## Limits

- Mutants are hand-picked, not exhaustive; only `metadata_add_days`, `metadata_iso_date` and the caller's recheck regex were mutated.
- One gate command at a time from a shared temporary fixture directory; no full selftest and no whole regression script (L1 owns those), so suite-level kill claims are limited to the 14 C2 date rows I reproduced verbatim from the control file.
- The base gate was extracted read-only via `git show 64eec5d:tools/research-gate.sh`; the lane was not modified. No installs were needed.
- Not re-tested here: 128 KiB leading-zero cadence on base/mutR (`FDateHugeCadence` baseline failure, already an accepted receipt and explicitly out of bounds).
- Sandbox artifacts and sha256: `probe-c2-dates.sh` `514c4fe3…`, `mut/base-64eec5d.sh` `c2c813f1…`, `mut/mutA-guard-removed.sh` `a9214dd0…`, `mut/mutA2-clamp-overflow.sh` `01d22c30…`, `mut/mutB-lastday-offbyone.sh` `adf2b83d…`, `mut/mutC-year9999-rejected.sh` `4e32ff70…`, `mut/mutD-refuse-9999-date.sh` `f2528f40…`, `mut/mutR-revert-round27-add-days.sh` `e52b806b…`.

Correction (appended): the selftest date-overflow fixture reference in §3 is `tools/research-gate.sh:6165-6173` (cat block at 6165, assertion at 6172-6173), not 6160-6172; the substance is unchanged.
