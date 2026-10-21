# ScoutDateRange — C2 year1/9999 range and leap-boundary expectations

Seat: `ChousaR27.ScoutDateRange` (static read-only). Base: `64eec5d41c7cf7f17f5ce1e968e28b3769952596`.
Scope: derive, independently of the gate implementation, the accepted date range and
leap-boundary outcomes that the C2 repair must preserve; give exact persisted-control
expectations for `corpus/evidence/round27-regressions.py` (or a sibling synthetic suite).

Method: source reading (no edits) plus an independent oracle computed with Python
`datetime` (proleptic Gregorian, years 1–9999) and a Python port of the two source
formulas checked exhaustively against `datetime` over all 3,652,059 accepted days.
No gate mode, selftest, regression run, or differential was executed. One
`bash tools/research-gate.sh --help` invocation occurred while checking whether help text
contains anchored verdict lines (it contains none); no fixture or analysis mode ran.
No tools installed. No fixture files created; no production file touched.

Line numbers are **base-commit** anchors. The lane working tree currently carries the C1
usage-helper patch (uncommitted, `git diff` +27/−1), which shifts the tail by +25 lines
(top-level `--as-of` check 6295→6320). Date helpers (2295–2359) are unchanged.

## Observed source contract (OBSERVED, base `64eec5d`)

- Shape: `metadata_iso_date` matches `^([0-9]{4})-([0-9]{2})-([0-9]{2})$` (`:2296`) and
  requires `year >= 1 && month 1..12 && day >= 1` (`:2299`); day ceiling is `31`, `30` for
  `4|6|9|11`, and February `28/29` by `year % 400 == 0 || (year % 4 == 0 && year % 100 != 0)`
  (`:2300–2307`). Four-digit shape plus the year≥1 test pins the accepted range to
  **0001-01-01 .. 9999-12-31** inclusive; `0000-*` and any 5-digit year are rejected.
- Calendar math is Howard Hinnant `days_from_civil`/`civil_from_days` (`:2310–2336`);
  dates before 1582 are proleptic Gregorian (no Julian cutover).
- Output formatting `printf -v META_DATE_RESULT '%04d-%02d-%02d'` (`:2335`) preserves
  four-digit years, so `due=0001-01-01` is emitted and re-parseable by
  `metadata_days_from_iso` (`:2338–2341`).
- Cadence: `metadata_add_days` (`:2343–2359`) accepts `^[0-9]+$`, strips leading zeros
  (`digits=${digits##+(0)}`, `:2348`), requires ≤7 digits (`:2350`), converts with
  `10#` (`:2351`), and clamps `amount <= 9999-12-31_days - start_days` (`:2355–2357`);
  failure returns 1 → `due=unknown freshness=unknown`.
- Classification: `metadata_iso_date "$recheck_first" || [[ ... ^[0-9]+d$ ... || on-release ]]`
  (`:2720–2722`); valid absolute date → due is that date (`:2739–2740`); cadence → due is
  `verified + amount` (`:2741–2750`).
- Strict freshness: `if ((asof_days > due_days)); then freshness=overdue; fi` (`:2754–2756`).
  Equality is **current**, never overdue.
- Usage path: top-level `--as-of` validation `metadata_iso_date "$AS_OF_ARG" || die_usage
  "--as-of must be a valid YYYY-MM-DD date"` (`:6295–6298`), `die_usage` exits 2
  (`:390`). This call is outside any `local LC_ALL=C` scope — the r26 FDateAsOfUsage root cause.
- `die_usage` prints `research-gate: <message>` then the usage block; the usage text
  contains no `^RESEARCH_GATE: ` line (source grep), so "zero anchored verdict lines" is
  a valid assertion for usage errors.

## Independent oracle (DERIVED, no gate execution)

- Epoch offsets: `0001-01-01 = -719162` days, `9999-12-31 = +2932896` days
  (1970-01-01 = 0).
- **Maximum representable span = 3,652,058 days**; 3,652,059 is out of range from
  0001-01-01. 7 digits are exactly sufficient (`3652058 < 10^7`); every 8-digit amount
  (≥10,000,000) is necessarily out of range, so the ≥8-digit early return is sound.
- Exhaustive check: for every day in the accepted range, the ported
  `days_from_civil` and `civil_from_days` agree with `datetime` (3,652,059 days,
  forward and inverse, 0 mismatches). Leap years in 1..9999: **2,424**.
- Leap set edges: 0001 no, 0004 yes, 0100 no, 0400 yes, 1900 no, 2000 yes, 2024 yes,
  2028 yes, 2100 no, 2400 yes, 9996 yes, 9999 no.
- Month ceilings (non-leap): 31/28/31/30/31/30/31/31/30/31/30/31; leap February 29.
- Consequence: the *date helpers themselves already implement the range and leap rule
  correctly for ASCII input*. C2's two defects are the unpinned top-level locale
  (`:2296` via `:6297`) and the recursive extglob strip (`:2348`); the bounds must not be
  changed by the repair.

## Expectation tables

Canonical synthetic fixture `entry.md` (newly generated; `source: S001`,
`verified-at: <V> checked synthetic fixture`, `recheck: <R>`, `## Claim`), run as
`bash tools/research-gate.sh verify-metadata entry.md --root <tmp> [--as-of <A>]`.
Output line shape: `META entry=entry.md source=present verified_at=dated
recheck=scheduled due=<D> freshness=<F> verdict=<clean|drift>` and
`RESEARCH_GATE: <CLEAN|DRIFT> (entries=1 complete=1 findings=<n> drift=<n>)`.

### A. `--as-of` usage validity (exit 2 ⇔ reject)

Reject: `research-gate: --as-of must be a valid YYYY-MM-DD date`, exit **2**, zero lines
matching `^RESEARCH_GATE: `, no `invalid integer` / `arithmetic syntax` diagnostic.

| value | oracle |
|---|---|
| `0001-01-01`, `0001-12-31` | accept (minimum) |
| `0004-02-29`, `0400-02-29`, `1582-10-10`, `2000-02-29`, `2024-02-29`, `2028-02-29`, `2400-02-29`, `9996-02-29` | accept |
| `9999-12-31` | accept (maximum) |
| `0000-01-01`, `0000-02-29`, `0000-12-31` | reject (year 0) |
| `0001-02-29`, `0100-02-29`, `1900-02-29`, `2100-02-29`, `2026-02-29`, `2027-02-29`, `9999-02-29` | reject (non-leap February) |
| `2026-04-31`, `2026-06-31`, `2026-09-31`, `2026-11-31` | reject (30-day months) |
| `9999-12-32`, `2026-13-01`, `2026-00-10`, `2026-01-00` | reject (calendar field) |
| `2026-1-01`, `10000-01-01`, `20261021` | reject (shape) |

Accept controls are measured with the fixture below (due 2026-04-02): as-of ≤
2026-04-02 → `freshness=current`, exit 0; as-of > 2026-04-02 → `freshness=overdue`,
exit 1 and `FINDING META_RECHECK_OVERDUE severity=warn surface=metadata
obs=entry=entry.md due=2026-04-02 as_of=<A>`. So `0001-01-01`, `0004-02-29`,
`0400-02-29`, `2000-02-29`, `2024-02-29`, `2028-02-29`, `2400-02-29` → rc0;
`9996-02-29`, `9999-12-31` → rc1 (and prove the accept path still emitted a verdict).

### B. Cadence due/freshness (calendar arithmetic + range)

| verified | recheck | as-of | expected |
|---|---|---|---|
| `0001-01-01` | `0d` | `0001-01-01` | due `0001-01-01`, current, rc0 |
| `0001-01-01` | `1d` | `0001-01-01` | due `0001-01-02`, current, rc0 |
| `0001-01-01` | `1d` | `0001-01-02` | due `0001-01-02`, current, rc0 (equality) |
| `0001-01-01` | `1d` | `0001-01-03` | due `0001-01-02`, overdue, rc1 |
| `0001-01-01` | `3652058d` | `9999-12-31` | due `9999-12-31`, current, rc0 (already in r27 suite) |
| `0001-01-01` | `0003652058d` | `9999-12-31` | same (already; zero-strip + 7-digit bound) |
| `0001-01-01` | `3652059d` | `9999-12-31` | unknown/unknown, rc0 (already) |
| `9999-12-30` | `1d` | `9999-12-31` | due `9999-12-31`, current, rc0 (**new: upper clamp inclusive**) |
| `9999-12-30` | `2d` | `9999-12-31` | unknown/unknown, rc0 (**new**) |
| `9999-12-31` | `0d` | `9999-12-31` | due `9999-12-31`, current, rc0 (**new**) |
| `9999-12-31` | `1d` | `9999-12-31` | unknown/unknown, rc0 (already) |
| `0001-02-28` | `1d` | `0001-03-01` | due `0001-03-01`, current, rc0 (**new**) |
| `0004-02-28` | `1d` | `0004-02-29` | due `0004-02-29`, current, rc0 (**new**) |
| `0004-02-29` | `1d` | `0004-03-01` | due `0004-03-01`, current, rc0 (**new**) |
| `0100-02-28` | `1d` | `0100-03-01` | due `0100-03-01`, current, rc0 (**new**) |
| `0400-02-28` | `1d` | `0400-02-29` | due `0400-02-29`, current, rc0 (**new**) |
| `1900-02-28` | `1d` | `1900-03-01` | due `1900-03-01`, current, rc0 (already) |
| `2000-02-28` | `1d` | `2000-02-29` | due `2000-02-29`, current, rc0 (already) |
| `2028-02-28` | `1d` | `2028-02-29` | due `2028-02-29`, current, rc0 (already) |
| `2100-02-28` | `1d` | `2100-03-01` | due `2100-03-01`, current, rc0 (already) |
| `2400-02-28` | `1d` | `2400-02-29` | due `2400-02-29`, current, rc0 (**new**) |
| `9996-02-28` | `1d` | `9996-02-29` | due `9996-02-29`, current, rc0 (**new**) |
| `9999-02-28` | `1d` | `9999-03-01` | due `9999-03-01`, current, rc0 (**new**) |
| `2026-12-31` | `1d` | `2027-01-01` | due `2027-01-01`, current, rc0 (**new; year carry**) |
| `2027-12-31` | `1d` | `2028-01-01` | due `2028-01-01`, current, rc0 (**new**) |
| `2028-12-31` | `1d` | `2029-01-01` | due `2029-01-01`, current, rc0 (**new**) |
| `2028-02-28` | `1d` | `2028-03-01` | due `2028-02-29`, **overdue**, rc1 (**new; strict > at leap due**) |
| `2028-02-29` | `1d` | `2028-03-01` | due `2028-03-01`, current, rc0 (**new; equality**) |

Already-present r27 cases `decimal08` (2026-01-01+8=2026-01-09, current, rc0) and
`decimal09-overdue` (2026-01-01+9=2026-01-10, as-of 2026-01-11, overdue, rc1) are correct.

### C. Absolute `recheck` at the range edges (new)

| recheck | as-of | expected |
|---|---|---|
| `0001-01-01` | `0001-01-01` | due `0001-01-01`, current, rc0 |
| `0001-01-01` | `0001-01-02` | due `0001-01-01`, overdue, rc1, `FINDING META_RECHECK_OVERDUE ... due=0001-01-01 as_of=0001-01-02` |
| `9999-12-31` | `9999-12-31` | due `9999-12-31`, current, rc0 |
| `9999-12-31` | `9999-12-30` | due `9999-12-31`, current, rc0 |
| `0000-01-01` | `0001-01-01` | `recheck=unscheduled`, due/freshness unknown, `FINDING META_RECHECK_UNSCHEDULED severity=info`, verdict clean (STRICT=0), rc0 |

Entry-side range note (OBSERVED): `verified_at` state is shape-only (`:2697–2699`), so
`verified-at: 0000-01-01` reports `verified_at=dated` while the cadence path fails
`metadata_iso_date` → `due=unknown freshness=unknown verdict=clean` (rc0). This is
existing behavior to preserve, not a bug to fix in C2.

## Calibration against the persisted suite

`corpus/evidence/round27-regressions.py` date blocks were read (not run). All 12 declared
date cases agree with the independent oracle: `leading-128k-zeros` (due 2026-04-02,
overdue, rc1), `allzero-128k` (due 2026-01-02, current, rc0), `huge-magnitude`
(unknown, rc0), `max-span` (due 9999-12-31, current, rc0), `overflow-span` (unknown,
rc0), `max-date-overflow` (unknown, rc0), `decimal08` (current, rc0),
`decimal09-overdue` (overdue, rc1), `leap-1900/2000/2028/2100` (due 03-01/02-29/02-29/03-01,
current, rc0). Its freshness computation uses `date`/`timedelta`, so it is independent of
the gate arithmetic. Its tokens are hardcoded, so Python's 4,300-digit `int()` string
limit is not hit; any extension that computes `int(token)` must strip leading zeros first.

Gaps for this seat's item (worth persisting, in priority order):
1. `--as-of` min/max acceptance (`0001-01-01`, `9999-12-31`) and year-0 / 5-digit-year
   rejection under both `LC_ALL=C` and `LC_ALL=en_US.UTF-8`.
2. Leap usage matrix: accept `0004-02-29`, `0400-02-29`, `2400-02-29`, `9996-02-29`;
   reject `0001-02-29`, `0100-02-29`, `9999-02-29` (plus already-covered 1900/2000/2028/2100).
3. Upper clamp adjacency: `9999-12-30 + 1d → 9999-12-31 current` and `+2d → unknown`.
4. Strict `>` at a leap due: `2028-02-28 + 1d` compared at `2028-02-29` (current) and
   `2028-03-01` (overdue).
5. Absolute recheck edges (`0001-01-01`, `9999-12-31`) and invalid-calendar recheck
   (`0000-01-01` → unscheduled/unknown).

## Integration notes for the C2 executor / L1

- Preserve `metadata_iso_date` exactly as to shape, year≥1, month ceilings, leap rule,
  and `%04d` formatting; the exhaustive check says this logic is already correct.
  Make the locale pin **function-local** (`local LC_ALL=C` inside `metadata_iso_date`),
  not a script-global `LC_ALL`, so unrelated locale-sensitive output is untouched.
  Do not replace `[0-9]` with `[[:digit:]]` without a local C pin: glibc treats both
  ranges as locale-dependent (r26 measured `^[0-9]$` matching 1,050 code points under
  `en_US.UTF-8`).
- Keep normalization before both the 7-digit bound and `10#`: the bound is only sound on
  normalized digits, and `10#` on a 128 KiB all-zero token aborts. The replacement must
  be stack-safe (parameter expansion or a single regex), not extglob recursion.
- Keep `amount <= last_day - start` (inclusive): it is the only guard that makes
  `9999-12-30 + 1d` succeed while `+2d` and `9999-12-31 + 0d`-overflow paths behave.
- Plain mode (no `--as-of`) never calls `metadata_add_days`; `metadata_iso_date` there
  only classifies `recheck`. A function-local C pin and a stack-safe strip leave
  plain-mode output byte-identical for all ASCII fixtures.
- `metadata_add_days` is reached only through `verify_metadata` (dynamic `local LC_ALL=C`
  at `:2539`), so its `^[0-9]+$` is currently safe; a local C pin there is still cheap
  defense because no persisted control exercises a cadence token under a UTF-8 locale.

## Unrun checks

No gate invocation in a test/analysis mode, no `--selftest`, no
`round27-regressions.py`, no `round26-date-differential.sh`, no mutants, no fixtures.
Expectations above are derived from source reading plus the independent `datetime`
oracle and the exhaustive formula comparison; they were not observed against the gate in
this lane. No files edited or created other than this report.
