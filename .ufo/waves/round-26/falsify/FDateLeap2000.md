# FDateLeap2000 — C2 leap-2000 falsification (round 26, attempt 1)

Seat `ChousaR26R.FDateLeap2000`, scout, author-lane advice only (no outside
judge/SHONEN claim). Target: C2 `--as-of` calendar arithmetic around
2000-02-28 +1d / +2d and the divisible-by-400 leap exception.

## Verdict

**Not falsified.** All 12 cadence cases, 5 `--as-of` validation cases and 4
literal/invalid-date cases agree with Python `datetime` and with spec v1
(`corpus/evidence/round26-claims.md:56-77,143-148`). Two isolated mutations of
the 400-year rule are each killed by these cases. Scope: this verdict covers
only the cases listed below, not C2 as a whole.

## Revision and inputs

- Measured revision: `0e9784bd52eca456b24d0bc40921480a47f91a2b`, from
  `corpus/evidence/round26-measured-revision.json`. Claim base
  `ba3333254dd337658a4f25e7a9471f9cf4e4567e` was not executed.
- Sandbox: `git archive 0e9784bd… | tar -x -C /tmp/chousa-r26-falsify-FDateLeap2000/tree`
  (exit 0). No lane working tree was graded.
- Digests of the archived files match the measured-revision JSON:
  `tools/research-gate.sh` c2c813f1…abc6,
  `corpus/evidence/round26-date-differential.sh` bb8f7f44…f5e7,
  `corpus/evidence/round26-measure.sh` b51c96f6…fb53,
  `corpus/QUALITY.md` 2428baaf…e6, `corpus/evidence/round26-claims.md` dcbe2b5f…f1c.
- Oracle: Python 3.14.8 `datetime.date` + `timedelta`. Expected values were
  derived before any run, from `cases.tsv` into `expected.tsv`.
- Tools installed or updated: none.

## Code under attack (observed)

- `metadata_iso_date` validates leap years with
  `year % 400 == 0 || (year % 4 == 0 && year % 100 != 0)`
  (`tools/research-gate.sh:2304`). This rule governs `--as-of`, the literal
  recheck date and the `verified-at:` V.
- `metadata_days_from_civil` / `metadata_civil_from_days`
  (`tools/research-gate.sh:2310-2336`) use the era/doe algorithm. The
  `- doe / 146096` term (`:2328`) exists only for doe=146096, which is
  2000-02-29, the final day of the 400-year era (0000-03-01 through 2000-02-29).
- `metadata_add_days` (`:2343-2359`) strips leading zeros under `shopt -s extglob`
  (`:256`) and uses `10#` decimal conversion.

## Case set A: cadence arithmetic

Fixture shape: `source: S001 fixture` / `verified-at: V checked fixture` /
`recheck: R` / blank / `## Body`. Command per case:
`bash tree/tools/research-gate.sh verify-metadata work/leap/<n>.md --root $D/work --as-of <A>`.

| case | V | R | as-of | expected due/freshness | rc | result |
|---|---|---|---|---|---|---|
| p1 | 2000-02-28 | 1d | 2000-02-29 | 2000-02-29 current | 0 | AGREE |
| p2 | 2000-02-28 | 2d | 2000-02-29 | 2000-03-01 current | 0 | AGREE |
| z1 | 2000-02-28 | 0001d | 2000-02-29 | 2000-02-29 current | 0 | AGREE |
| z2 | 2000-02-28 | 002d | 2000-03-01 | 2000-03-01 current (due==as-of) | 0 | AGREE |
| e1 | 2000-02-28 | 1d | 2000-03-01 | 2000-02-29 overdue | 1 | AGREE |
| e2 | 2000-02-28 | 2d | 2000-03-02 | 2000-03-01 overdue | 1 | AGREE |
| f1 | 2000-02-29 | 1d | 2000-03-01 | 2000-03-01 current | 0 | AGREE |
| y1 | 2000-02-29 | 365d | 2001-02-28 | 2001-02-28 current | 0 | AGREE |
| y2 | 2000-02-29 | 366d | 2001-03-01 | 2001-03-01 current | 0 | AGREE |
| x1 | 1999-02-28 | 366d | 2000-03-01 | 2000-02-29 overdue | 1 | AGREE |
| c1 | 2100-02-28 | 1d | 2100-03-01 | 2100-03-01 current | 0 | AGREE |
| c2 | 1900-02-28 | 1d | 1900-03-01 | 1900-03-01 current | 0 | AGREE |

Agreement means the full `META` line matched exactly, including
`verdict=drift` for overdue and `verdict=clean` otherwise, and the count of
`META_RECHECK_OVERDUE` findings matched (1 if overdue, else 0). Driver result:
`ALL_FAIL=0`. Rows c1 and c2 are contrast controls for non-leap centuries.
Peer `FDateCentury1900` owns 1900. The overdue finding line is fully formed,
observed from a p1 rerun with as-of 2000-03-01, rc=1:
`FINDING META_RECHECK_OVERDUE severity=warn surface=metadata obs=entry=p1.md due=2000-02-29 as_of=2000-03-01`.

## Case set B: `--as-of` validation and date literals

| input | Python | CLI |
|---|---|---|
| `--as-of 2000-02-29` | valid | rc=0, due=2000-02-29 current |
| `--as-of 2000-02-30` | invalid | rc=2 `--as-of must be a valid YYYY-MM-DD date` |
| `--as-of 1900-02-29` | invalid | rc=2, same message |
| `--as-of 2100-02-29` | invalid | rc=2, same message |
| `--as-of 2400-02-29` | valid | rc=1, p1 overdue (accepted) |
| `recheck: 2000-02-29`, as-of 2000-02-29 | valid literal | rc=0 due=2000-02-29 current |
| `recheck: 2000-02-29`, as-of 2000-03-01 | — | rc=1 due=2000-02-29 overdue + finding |
| `recheck: 1900-02-29` | invalid literal | rc=0 `recheck=unscheduled due=unknown freshness=unknown` + `META_RECHECK_UNSCHEDULED` info |
| `verified-at: 2000-02-30 checked`, `1d` | invalid V | rc=0 `due=unknown freshness=unknown` (spec: `<N>d` without V) |

Observation, not a C2 defect: the `badv` case prints `verified_at=dated` for
the calendar-invalid 2000-02-30. That field comes from the legacy
verified-at classifier, not from C2. I did not compare it against the base.

## Mutations (isolated copies in the sandbox; production untouched)

- **M1**, `:2304`: dropped `year % 400 == 0 ||`. **Killed.** p1, p2 and z1 exit 2
  on `--as-of 2000-02-29`. f1, y1 and y2 lose V and emit `due=unknown`. z2, e1,
  e2, x1, c1 and c2 still agree.
- **M2**, `:2328`: dropped `- doe / 146096`. **Killed.** p1 and z1 emit
  `due=2000-03-01` instead of 02-29. e1 and x1 flip from overdue to current,
  with rc 1 changing to 0. 2000-02-28 +1d and +2d collapse onto the same
  date. Every other case agrees, so the term is specific to 2000-02-29.

## Coverage observations (static read only; nothing run)

- The frozen selftest has leap cases only for 2028 and 2027
  (`tools/research-gate.sh:6090-6107`). It has no 2000, 1900 or 2100 fixture,
  so neither M1 nor M2 is expected to be caught by the selftest. [INFERENCE]
  Not run.
- `corpus/evidence/round26-date-differential.sh:32-34,140-170` samples
  2000-02-28 and 2000-02-29 with `DAY_COUNTS = (0, 1, 28, …)` and the boundary
  due dates 2000-02-29 and 2000-03-01. It would plausibly kill both
  mutations. [INFERENCE] Not run (outside the named bounded checks).
  `DAY_COUNTS` has no `2`, so the exact 2000-02-28 +2d pair (p2/e2) is not a
  direct differential case. Its due date, 2000-03-01, is reached from
  2000-02-29 +1d.

## Commands and exits

1. `git cat-file -t 0e9784bd…` → `commit`; `git archive … | tar -x` → 0.
2. Python expected-value derivation → 0.
3. Case set A driver → 0 (case rcs as tabled; `ALL_FAIL=0`).
4. Case set B loops → 0 (case rcs as tabled).
5. Mutation build (Python string replace with `count==1` asserts) plus diffs →
   one line changed per copy; mutation drivers → 0 (rcs as described).

Not run: the full selftest, build, lint, formatter, the 8 MiB probe,
`round26-measure.sh` and `round26-date-differential.sh`.
