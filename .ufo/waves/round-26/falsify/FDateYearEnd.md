# FDateYearEnd — C2 year-end boundary attack (round 26, attempt 1)

Target claim: **C2 freshness** (`verify-metadata --as-of` computed due dates).
Target revision (immutable): `0e9784bd52eca456b24d0bc40921480a47f91a2b`
Working copy: `git archive 0e9784bd… | tar -x -C /tmp/chousa-r26-falsify-FDateYearEnd`
Gate digest check: `sha256sum tools/research-gate.sh` =
`c2c813f1b425bc4e74625a2607eaca1b97addf9898f834e88af8f1fe2143abc6` — matches
`corpus/evidence/round26-measured-revision.json` (QUALITY 15).

## Attack

Year-end carry for cadence arithmetic: `verified-at: 2026-12-31` with
`recheck: 1d` and `recheck: 365d`, each evaluated at due-boundary and
due-plus-one as-of values.

## Independent oracle (Python datetime, spec `due = V + N days`, overdue iff as-of > due)

- `date(2026,12,31) + timedelta(1)`  → **2027-01-01**
- `date(2026,12,31) + timedelta(365)` → **2027-12-31** (day-count, not calendar-year)
- freshness: as-of == due → `current`; as-of > due → `overdue` + `META_RECHECK_OVERDUE`

## Runs (sandbox tree; fixtures in `work/yearend/`)

Fixture shape (both files):
```
source: S001 fixture
verified-at: 2026-12-31 checked fixture
recheck: {1d|365d}

## Body
```

Command per row: `bash tools/research-gate.sh verify-metadata work/yearend/<f> --root work/yearend --as-of <A>`.

| fixture | as-of | expected due / freshness | observed | rc |
|---|---|---|---|---|
| yearend-1d.md | 2027-01-01 | due=2027-01-01 current | `due=2027-01-01 freshness=current verdict=clean` | 0 |
| yearend-1d.md | 2027-01-02 | due=2027-01-01 overdue + finding | `due=2027-01-01 freshness=overdue verdict=drift` + `FINDING META_RECHECK_OVERDUE … due=2027-01-01 as_of=2027-01-02` | 1 |
| yearend-365d.md | 2027-12-31 | due=2027-12-31 current | `due=2027-12-31 freshness=current verdict=clean` | 0 |
| yearend-365d.md | 2028-01-01 | due=2027-12-31 overdue + finding | `due=2027-12-31 freshness=overdue verdict=drift` + `FINDING META_RECHECK_OVERDUE … due=2027-12-31 as_of=2028-01-01` | 1 |

4/4 observed == oracle.

## Why the boundary holds (inspection, not a finding)

`metadata_add_days` (tools/research-gate.sh:2343-2359) converts to days-since-epoch
via `metadata_days_from_civil` (Hinnant algorithm, lines 2310-2321) and converts
back via `metadata_civil_from_days` (2324-2336); year rollover is a property of
the conversion, not month-table arithmetic. Cadence text is decimal-normalized
(`10#`, leading-zero strip, ≤7-digit bound at 2350) and range-checked against
`9999-12-31` before arithmetic — consistent with the spec-v1 correction.

## Verdict

**No defect found on this axis — C2 survives.** `2026-12-31 +1d` correctly
crosses to `2027-01-01`; `+365d` yields `2027-12-31` (exact day count);
the strictly-after overdue rule holds on both sides of the year boundary,
including the `as_of` echo in the drift finding.

## Residual risk / gaps

- Only `1d`/`365d` at one year-end probed; other cadences at other boundaries
  (leap Feb-29 +1d, month-end cadence>month-length) covered by sibling seats.
- Findings asserted by output inspection; rc semantics (0 clean / 1 drift)
  observed, not exhaustively enumerated.
- Tooling: none installed; stock `bash`, `git`, `python3`, `sha256sum` used.
