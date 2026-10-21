# FDateMonthEnds — C2 month-end `+Nd` attack (round 26 attempt 1)

Seat `ChousaR26R.FDateMonthEnds` (author-lane advice only; not an outside judge).
Judged axis: freshness (C2). Target: Jan31 / Apr30 / Aug31 `+1d`.

## Verdict

**Not falsified.** On the immutable target, `verify-metadata --as-of` puts the
`due=` for every month-end `+1d` case on the first day of the next month. The
`freshness=` boundary and the `META_RECHECK_OVERDUE` finding both follow the
spec: `current` when as-of equals due, `overdue` when as-of is strictly after
due. All of this agrees with an independent Python `datetime` oracle. Two
month-end mutations, made in sandbox copies only, are detected by the same
harness, so the harness can fail.

## Revisions and inputs observed

- Target `0e9784bd52eca456b24d0bc40921480a47f91a2b` from
  `corpus/evidence/round26-measured-revision.json`. Claim base `ba333325…`.
- Lane `git rev-parse HEAD` = `0e9784bd…` at the time of the run.
- Sandbox `/tmp/chousa-r26-falsify-FDateMonthEnds/tree` =
  `git archive 0e9784bd… | tar -x` (exit 0).
- `sha256 tree/tools/research-gate.sh` =
  `c2c813f1b425bc4e74625a2607eaca1b97addf9898f834e88af8f1fe2143abc6`. This
  equals the manifest digest. The claims-file and QUALITY digests also match
  the manifest (`dcbe2b5f…`, `2428baaf…`).
- Harness `attack.py` sha256 `9c9ceb28b7f225ba89b760f0434b0f6566326aec9998cd2d02bb3009e6654f51`.
  It is sandbox-only.
- Environment: GNU bash 5.3.20 and Python 3.14.8. No tools were installed or
  updated.

## Code under attack (observed)

- `tools/research-gate.sh:2295` `metadata_iso_date` checks the calendar,
  including the 30-day months 4/6/9/11 and the Gregorian leap rule.
- `:2310` `metadata_days_from_civil` and `:2324` `metadata_civil_from_days`
  are the era/doe day-count algorithms. They have no month-length table, so a
  month end rolls over by arithmetic.
- `:2343` `metadata_add_days`: requires a decimal-only token, strips leading
  zeros (extglob is on at `:256`), caps the length at 7 digits, and bounds the
  result at 9999-12-31. Out-of-range input returns 1, which gives `unknown`.
- `:2737-2762`: due/freshness selection, and `asof_days > due_days` decides
  overdue.

## Oracle (independent of the implementation)

The oracle is written from the claims spec v1 plus the spec-v1 correction
(`corpus/evidence/round26-claims.md:58-82,143-148`):

- due = R if R is a valid ISO date.
- Otherwise, if R matches `<N>d` and V is a calendar-valid date, due = V+N via
  `datetime.date + timedelta`. This is also unknown if the result falls outside
  0001-01-01 through 9999-12-31.
- Otherwise due is unknown.
- freshness = `overdue` iff as-of > due, else `current`. An overdue finding
  carries the exact `due=` and `as_of=`.

Expected values for the named cases, from Python: `2026-01-31 +1d = 2026-02-01`,
`2026-04-30 +1d = 2026-05-01`, `2026-08-31 +1d = 2026-09-01`.

## Fixtures (92 entries, sandbox `fx/`)

- The three named cases.
- Every month end for 2026, 2027, 2028 (leap), 2100 (non-leap century) and
  2000 (leap century), each with `+1d`. That is 60 entries, including Dec31
  rolling into the next year.
- Zero-padded cadences `01d`, `0001d` and `0000001d` on the three named dates.
- Cross-month cadences: Jan31 `+28d`, `+29d`, `+30d`; Aug31 `+30d`; Apr30
  `+31d`.
- Day-before controls: Jan30, Apr29, Aug30 with `+1d`.
- Jan31 `+0d`.
- Range edges: 9999-12-30 `+1d`, 9999-12-31 `+1d` (gives unknown), and
  0001-01-31 `+1d`.
- Explicit recheck dates that are not calendar-valid: 04-31, 06-31, 09-31,
  11-31, 2026-02-29, 2028-02-30, 2100-02-29.
- Explicit valid dates: 01-31, 04-30, 08-31, 2000-02-29.
- Month-end `verified-at:` dates that are not calendar-valid, with `1d`:
  04-31, 06-31, 2026-02-29.

## Commands and exits

| Command (cwd `/tmp/chousa-r26-falsify-FDateMonthEnds`) | Exit | Result |
|---|---|---|
| `python3 attack.py` (12 as-of dates × 92 entries; as-of 2026-01-31, -02-01, -02-02, -04-30, -05-01, -05-02, -08-31, -09-01, -09-02, -10-21, 0001-01-01, 9999-12-31) | 0 | `TOTAL_MISMATCHES=0 ENTRIES=92 ASOFS=12` |
| each gate run inside it: `bash tree/tools/research-gate.sh verify-metadata fx --root . --as-of A` | 1 (0 at as-of 0001-01-01) | rc 1 when ≥1 overdue drift exists; rc 0 when nothing is overdue |
| `GATE=mut1/... python3 attack.py 2026-02-01 2026-10-21` | 1 | `TOTAL_MISMATCHES=190` (killed) |
| `GATE=mut2/... python3 attack.py 2026-02-01 2026-10-21` | 1 | `TOTAL_MISMATCHES=2` (killed) |

Raw single-entry runs (timestamp lines omitted):

```
# named-jan31.md, --as-of 2026-02-01 → rc=0
META entry=named-jan31.md source=present verified_at=dated recheck=scheduled due=2026-02-01 freshness=current verdict=clean
# --as-of 2026-02-02 → rc=1
META entry=named-jan31.md source=present verified_at=dated recheck=scheduled due=2026-02-01 freshness=overdue verdict=drift
FINDING META_RECHECK_OVERDUE severity=warn surface=metadata obs=entry=named-jan31.md due=2026-02-01 as_of=2026-02-02
# named-apr30.md, --as-of 2026-05-01 → rc=0 due=2026-05-01 freshness=current; --as-of 2026-05-02 → rc=1 overdue, finding due=2026-05-01 as_of=2026-05-02
# named-aug31.md, --as-of 2026-09-01 → rc=0 due=2026-09-01 freshness=current; --as-of 2026-09-02 → rc=1 overdue, finding due=2026-09-01 as_of=2026-09-02
```

## Independent failing controls (QUALITY 17; sandbox copies only)

- **mut1** (`mut1/tools/research-gate.sh` sha256 `3b297b5e…`). Replaces the
  `metadata_add_days` epoch round-trip with a naive `day + amount` printf.
  The harness reports `('named-jan31', …, expected ('2026-02-01','current'),
  got ('2026-01-32','current','clean'))`, and likewise `2026-04-31` and
  `2026-08-32`. The overdue-finding `due=` also mismatches. Killed for the
  targeted reason, not a parse error.
- **mut2** (`daea4a27…`). Drops `11` from the 30-day-month case in
  `metadata_iso_date`. The harness reports `x-nov31` expected `unknown/unknown`,
  got `2026-11-31 current clean`. Killed.

  Only the explicit-date arm sees this mutation. A `+1d` from 11-30 never
  produces 11-31, because the epoch round-trip doesn't consult the
  month-length table.

The unmutated target, re-run after the mutations, still gives
`TOTAL_MISMATCHES=0` with exit 0.

## Residuals (observed, not falsifications)

- A `verified-at: 2026-04-31 …` entry with `recheck: 1d` prints
  `verified_at=dated … due=unknown freshness=unknown verdict=clean`.
  - The `dated` label is base behavior: the base gate `git show ba333325:tools/research-gate.sh`
    prints the same plain line, rc 0. The plain-output hold requires it to stay
    byte-identical.
  - `due=unknown` is what spec v1 asks for (V must be calendar-valid).
  - So an entry whose verified date is not calendar-valid gets no finding and
    a clean verdict under `--as-of`. Its freshness is unknown, not overdue.
    That is spec-conformant, but it is a silent gap for criterion 6. It
    overlaps peer `ChousaR26R.FDateInvalidVerified`.
- Explicit recheck dates that are not calendar-valid, such as `2026-04-31`,
  also print `due=unknown`. They only raise the base `META_RECHECK_UNSCHEDULED`
  info finding, with no warn. This is spec-conformant.
- Scope: these runs cover month ends, Dec31 rollover, the leap and century
  rules, zero-padded cadences of up to 7 digits, and the 9999-12-31 bound.
  Huge cadences and other modes belong to sibling seats. This seat ran no
  selftest, build, lint, or amplification probe.

## Confidence

High that month-end `+Nd` computation, the as-of==due boundary, and overdue
emission all conform to C2 spec v1 at `0e9784bd`. This rests on 1,104
entry×as-of comparisons with zero mismatches and on both mutation controls
being killed. It is not a claim that the C2 admission passed; L1 owns the
integrated run.
