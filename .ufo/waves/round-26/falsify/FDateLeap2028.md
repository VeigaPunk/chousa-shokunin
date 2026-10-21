# FDateLeap2028 — C2 attack: 2028-02-28 +1d / +2d (round 26, attempt 1)

Seat `ChousaR26R.FDateLeap2028` (scout, author-lane advice; no outside judge).
Judged on freshness. Verdict: **C2 not falsified on this case.** 28/28 dated
cases agree with an independent Python `datetime` oracle. One spec-edge
observation (O1) is left for L1 to dispose of.

## Target and revisions

- Measured revision `0e9784bd52eca456b24d0bc40921480a47f91a2b` (from
  `corpus/evidence/round26-measured-revision.json`); lane HEAD observed equal.
- Sandbox `/tmp/chousa-r26-falsify-FDateLeap2028/tree` via
  `git archive 0e9784bd… | tar -x` (rc=0). The sandbox
  `sha256sum tools/research-gate.sh` gave
  `c2c813f1…43abc6`, equal to the measured-revision record. `corpus/QUALITY.md`
  and `round26-claims.md` hashes also match.
- Base comparison: `git archive ba3333254dd337658a4f25e7a9471f9cf4e4567e
  tools/research-gate.sh` into `/tmp/chousa-r26-falsify-FDateLeap2028/base` (rc=0).
- Runtime: GNU bash 5.3.20(1), Python 3.14.8. Env per selftest convention:
  `env -u CHOUSA_RECORD -u CHOUSA_CLAIMS -u CHOUSA_AGGREGATOR_ERE CHOUSA_STRICT=0 CHOUSA_ROOT=$WORK`.
- No tools installed or updated.

## Code path read (observed)

- `metadata_iso_date` (`tools/research-gate.sh:2295-2308`): Gregorian Feb max
  (`%400 || %4 && !%100`).
- `metadata_days_from_civil` / `metadata_civil_from_days` (`:2310-2336`):
  Hinnant era/doe algorithms.
- `metadata_add_days` (`:2343-2359`): decimal-only, strips leading zeros via
  `${digits##+(0)}` (`shopt -s extglob` at `:256`), ≤7 digits, bounded by
  9999-12-31.
- Due/freshness branch (`:2736-2763`): overdue iff `asof_days > due_days`.
- The existing selftest covers only `2028-02-28 + 0001d` with as-of equal to
  due (`:6090-6098`). `round26-date-differential.sh` has no 2028 case.

## Oracle differential (independent of the implementation)

Expected values come from `datetime.date.fromisoformat(V) + timedelta(days=N)`.
Freshness is `overdue` iff as-of > due, per spec v1. Driver:
`/tmp/chousa-r26-falsify-FDateLeap2028/drive.py`. Each case is one
`verify-metadata FILE --root $WORK --as-of A` invocation, comparing the
exact `META entry=` line and the presence or absence of the
`META_RECHECK_OVERDUE` finding.

Command: `python3 drive.py` → `ORACLE_CASES=28 DISAGREE=0`, exit 0.

| entry (verified-at / recheck) | oracle due | as-of → freshness (rc) |
|---|---|---|
| 2028-02-28 / `1d` | 2028-02-29 | 02-28 current (0), 02-29 current (0), 03-01 overdue (1) |
| 2028-02-28 / `2d` | 2028-03-01 | 02-29 current (0), 03-01 current (0), 03-02 overdue (1) |
| 2028-02-28 / `0001d`, `00000001d` (8 digits) | 2028-02-29 | 02-29 current, 03-01 overdue |
| 2028-02-28 / `002d`, `000000000002d` (12 digits) | 2028-03-01 | 03-01 current, 03-02 overdue |
| 2028-02-28 / `1d bash …` (trailing command) | 2028-02-29 | 02-29 current, 03-01 overdue |
| `2028-02-28T23:59:59Z checked` / `2d` | 2028-03-01 | 03-01 current, 03-02 overdue |
| 2028-02-28 / `0d` | 2028-02-28 | 02-28 current, 02-29 overdue |
| 2027-02-28 / `1d`, `2d` (non-leap contrast) | 2027-03-01, 2027-03-02 | boundary current, +1 overdue |
| 2100-02-28 / `1d` (century non-leap) | 2100-03-01 | boundary current, +1 overdue |
| 2000-02-28 / `1d` (400-year leap) | 2000-02-29 | boundary current, +1 overdue |

The leap-year arithmetic is really exercised: the same `+1d` gives 02-29 in
2028 and 2000, but 03-01 in 2027 and 2100. Every overdue line carried
`FINDING META_RECHECK_OVERDUE severity=warn surface=metadata obs=entry=<f> due=<D> as_of=<A>`
with exact text, and no current line did.

Further single cases at as-of 2028-03-01:

- `recheck: 2028-02-29` (ISO): `due=2028-02-29 freshness=overdue`, rc=1.
- `recheck: 2028-02-30`: `recheck=unscheduled due=unknown freshness=unknown`,
  rc=0. This matches the spec's "anything else" rule.
- `verified-at: 2028-02-29` with `1d`: `due=2028-03-01 current`. The oracle
  also gives 2028-03-01.

## Option-side cases

`--as-of` validity. Python `fromisoformat` independently gives valid for
2028-02-29 and 2000-02-29, and invalid for 2027-02-29, 2100-02-29 and
2028-02-30.

- `2028-02-29` → rc 0. `2000-02-29` → rc 0.
- `2027-02-29`, `2100-02-29`, `2028-02-30`, `2028-2-29`, `20280229`,
  `' 2028-02-29'`, `'2028-02-29 '`, `2028-02-29x`, and `''` → rc 2 with
  `--as-of must be a valid YYYY-MM-DD date`.
- Bare `--as-of` → rc 2 with `--as-of needs YYYY-MM-DD`.
- `--as-of=2028-03-01` → rc 2 with `unknown flag`.

Flag order. `--as-of` before the mode word, or before PATH with `--root`
reordered, gives the same output as the canonical order: rc 0 at
2028-03-01 and rc 1 at 2028-03-02 for the `2d` entry.

Directory mode (`pair/` = the `1d` and `2d` entries, as-of 2028-03-01):
p1 overdue, p2 current, one finding, `RESEARCH_GATE: DRIFT (entries=2
complete=2 findings=1 drift=1)`, rc=1.

Composition with `--registry`, using a sandbox registry where S001 is mined
with used-by `pair/p1.md, pair/p2.md`:

- as-of 02-29 → CLEAN, rc 0.
- as-of 03-01 → 1 overdue, DRIFT, rc 1.
- as-of 03-02 → 2 overdue, DRIFT, rc 1.
- Reversed flag order gives identical output.

Both screens apply. The registry positive adds no findings.

Plain-output hold, without `--as-of`: on all 16 sandbox fixtures plus `pair/`,
the measured tree and base `ba333325` give byte-identical output and the same
rc, with `ts=` normalized via `sed` and runs ≥1.1 s apart →
`PLAIN_IDENTICAL=17/17`.

## O1 — repeated `--as-of`: an invalid earlier value is silently discarded (spec edge, low)

Observed:

- `verify-metadata p1.md --root W --as-of 2027-02-29 --as-of 2028-03-01` →
  rc **1** with `due=2028-02-29 freshness=overdue`.
- The reverse order → rc 2.

The parser keeps the last value (`:6281-6283`) and validates only after the
loop (`:6295-6297`). Spec v1 says "an absent or calendar-invalid value exits
2". Read literally, a supplied calendar-invalid value did not exit 2.
`--root` and `--registry` follow the same last-value-wins convention, and the
help text and `recheck-due-r26.md` say nothing about repeated flags.

[INFERENCE] This is a convention gap, not a date-arithmetic defect. It
affects no frozen control or frozen-29 prediction. L1 should dispose of it
either way: document last-value-wins, or reject duplicate or invalid
occurrences.

## Not run / scope

- Not run: the full selftest, build, lint, measure probe, and any mutation of
  the target. My item named no mutation, so QUALITY 17 kill-power for this arm
  is not shown here. The 2027/2100 contrast shows only that the oracle
  discriminates leap from non-leap years.
- The date results are metadata arithmetic only. They are not citation
  support, truth, or field readiness.
- No entry text was executed. The `1d bash …` recheck command was parsed as
  text only.
