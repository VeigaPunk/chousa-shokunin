# FDateMaximum — C2 upper calendar domain (9999-12-30 +1d / +2d)

Seat `ChousaR26R.FDateMaximum`, round 26 attempt 1, falsification wave. Author-lane
advice only; not an outside judge or SHONEN claim.

## Verdict

**C2 was not falsified on this axis: 36 of 36 cases agree with the oracle and 0 disagree.**
At the immutable target, `verify-metadata --as-of` gives:

- `9999-12-30 + 1d` → `due=9999-12-31`;
- `9999-12-30 + 2d`, or any computed date after 9999-12-31 → `due=unknown freshness=unknown`, exit 0, and the process does not stop;
- an `--as-of` value with a year past 9999 → exit 2.

The plain output (no `--as-of`) on all 14 fixtures is byte-identical to the base revision, with the timestamp line dropped and the exit code included in the comparison.

## Revisions observed

| item | value |
|---|---|
| target (from `corpus/evidence/round26-measured-revision.json`) | `0e9784bd52eca456b24d0bc40921480a47f91a2b` (lane `HEAD` at the time of the run was the same commit) |
| target `tools/research-gate.sh` sha256 | `c2c813f1b425bc4e74625a2607eaca1b97addf9898f834e88af8f1fe2143abc6` (matches the manifest) |
| target `round26-claims.md` / `QUALITY.md` sha256 | `dcbe2b5f…f1c` / `2428baaf…ce6` (both match the manifest) |
| base `ba3333254dd337658a4f25e7a9471f9cf4e4567e` `tools/research-gate.sh` sha256 | `985a63200ca4c5712806d8752ba27a8f3448b026f773659079e71ca602e56ef7` |
| sandbox | `/tmp/chousa-r26-falsify-FDateMaximum` (`tree/` = `git archive` of the target; `base/` = `git archive` of the base gate) |
| runtime | GNU bash 5.3.20(1), Python 3.14.8 |
| driver / log sha256 | `drive.py` `45a9996c…3621`, `drive.log` `6282aea8…e674` |

## Spec used for the expected values

The frozen spec is `round26-claims.md` lines 59–75 and 143–148. The rules that matter here:

- When R is `<N>d` and V is present, `due` is V + N days in the proleptic Gregorian calendar.
- Leading zeros are stripped from N before conversion.
- A computed date outside 0001-01-01 through 9999-12-31 gives `due=unknown freshness=unknown` and must not terminate the process.
- `freshness` is `overdue` iff as-of is strictly after due.
- Overdue emits `META_RECHECK_OVERDUE` (warn), which makes the verdict drift and the exit code 1.

The expected values come from a Python `datetime` oracle written independently, not from the gate:

- `date.fromisoformat(V) + timedelta(days=int(N.lstrip('0') or '0'))`, with `OverflowError` mapped to `unknown`.
- A spot check confirmed `(date(9999,12,31) - date(1,1,1)).days == 3652058` and `date(9999,12,30) + 1 day == 9999-12-31`.

Fixture entries are data files read by the gate. No entry text was executed.

## Commands and exits

1. `git archive 0e9784bd… | tar -x -C tree`, then a sha256 check. Exit 0.
2. `python3 drive.py` exited 0 and printed `FDATEMAX_AGREE=36/36`.
   - It ran 12 fixtures × 3 as-of dates (2026-10-21, 9999-12-30, 9999-12-31).
   - Each case invoked `bash tree/tools/research-gate.sh verify-metadata FIX --root root --as-of A`.
   - Environment: `CHOUSA_STRICT=0`, `CHOUSA_ROOT=root`, `CHOUSA_NOW_EPOCH=1792540800`; `CHOUSA_RECORD`, `CHOUSA_CLAIMS` and `CHOUSA_AGGREGATOR_ERE` were unset.
   - A case agrees only if all of these match: the exact `META` line, the exit code, the presence of the exact `FINDING META_RECHECK_OVERDUE … due=D as_of=A`, and the absence of any other overdue finding.
3. `--as-of` with years past 9999 or malformed values. The run used the same CLI with `set +e`; an earlier attempt aborted at the first expected exit 2 because `set -e` was still on in the shell, and was re-run.
4. Plain mode on every fixture, comparing the target against the base gate.

### Cases from the driver (all agree)

| fixture | V | R | oracle due | as-of 2026-10-21 | as-of 9999-12-30 | as-of 9999-12-31 |
|---|---|---|---|---|---|---|
| max-plus1 | 9999-12-30 | `1d` | 9999-12-31 | current, rc0 | current, rc0 | current, rc0 (due == as-of) |
| max-plus2 | 9999-12-30 | `2d` | unknown | unknown, rc0 | unknown, rc0 | unknown, rc0 |
| max-plus0 | 9999-12-30 | `0d` | 9999-12-30 | current, rc0 | current, rc0 (due == as-of) | **overdue, rc1, exact FINDING** |
| last-plus0 | 9999-12-31 | `0d` | 9999-12-31 | current | current | current |
| last-plus1 | 9999-12-31 | `1d` | unknown | unknown | unknown | unknown |
| max-pad7 | 9999-12-30 | `0000001d` | 9999-12-31 | current | current | current |
| max-pad11 | 9999-12-30 | `00000000001d` (11 digits, zero-stripped) | 9999-12-31 | current | current | current |
| max-pad11-2 | 9999-12-30 | `00000000002d` | unknown | unknown | unknown | unknown |
| max-7digit | 9999-12-30 | `9999999d` | unknown | unknown | unknown | unknown |
| min-span | 0001-01-01 | `3652058d` (the full domain span) | 9999-12-31 | current | current | current |
| min-span-over | 0001-01-01 | `3652059d` | unknown | unknown | unknown | unknown |
| explicit-last | 2026-01-02 | `9999-12-31` (an ISO date) | 9999-12-31 | current | current | current |

Example of raw target output for the +2d case:
`META entry=max-plus2.md source=present verified_at=dated recheck=scheduled due=unknown freshness=unknown verdict=clean`

### Inputs with years past 9999 (target)

| input | observed |
|---|---|
| `--as-of 10000-01-01` | rc 2, `research-gate: --as-of must be a valid YYYY-MM-DD date` |
| `--as-of 99999-12-31`, `+9999-12-31`, `9999-12-32`, `0000-12-31` | rc 2, same message |
| `recheck: 10000-01-01` with as-of 9999-12-31 | rc 0, `recheck=unscheduled due=unknown freshness=unknown verdict=clean`, plus the legacy `META_RECHECK_UNSCHEDULED` info finding |
| `verified-at: 10000-01-01`, `recheck: 1d` | rc 1, `verified_at=undated … due=unknown freshness=unknown verdict=drift`. The drift comes only from the legacy `META_VERIFIED_AT_UNDATED` warn, which base plain mode also reports with rc 1. There is no overdue finding, so V is correctly treated as none. |

### Plain mode against base (no `--as-of`)

All 14 fixtures (the 12 above plus `recheck-y10k` and `verified-y10k`) printed `SAME` once the `ts=` line was dropped, including the exit code: 13 with rc 0, and `verified-y10k` with rc 1 in both. As a control, the base gate given `--as-of` exits 2 with `research-gate: unknown flag: --as-of`, which is the expected "before" state.

## Code path checked (target `tools/research-gate.sh`)

- `metadata_add_days` (lines 2343–2359):
  - it rejects non-digit text;
  - it strips leading zeros with `${digits##+(0)}`, which works because `shopt -s extglob` is set at line 256;
  - it caps the digit count at 7;
  - it bounds `amount <= days(9999-12-31) - start` before calling `metadata_civil_from_days`.
- A failed bound leaves the defaults `due=unknown freshness=unknown` at lines 2738 and 2747–2750.
- The arithmetic uses only `10#` decimal conversions of regex-validated digits. No user text is evaluated as an arithmetic expression.

## Inference and gaps

- [INFERENCE] If the bound at line 2357 were removed, `metadata_civil_from_days` would format 9999-12-30 + 2 as `10000-01-01`, so the +2d, `last-plus1`, `max-pad11-2` and `min-span-over` rows would fail against the oracle. I did not run that mutation: my item names CLI cases only, not mutations.
- The overdue branch at the top of the domain was exercised only through `0d` (due 9999-12-30, as-of 9999-12-31). No later as-of exists, because as-of is capped at 9999-12-31.
- Not covered by this seat, as they belong to sibling seats: zero or huge cadences away from the upper bound, a malformed `verified-at`, composed flags, and the lower bound 0001-01-01 minus anything.
- This seat did not run the selftest, the build, the full probe, or the 8 MiB amplification. No other check is claimed as passing.

## Tools

No tools were installed or updated.
