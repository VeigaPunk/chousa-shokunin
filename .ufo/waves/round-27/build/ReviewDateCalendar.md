# ReviewDateCalendar — C2 leap1900/2000/2028 + due-equality (round 27 attempt 1)

Seat `ChousaR27.ReviewDateCalendar`, author-lane advice only. Read scope honored: base
`64eec5d41c7cf7f17f5ce1e968e28b3769952596`, r26 reports, round27 claims/regressions oracle.
No gate/selftest executed. Sources: `git show 64eec5d:tools/research-gate.sh` sha256
`c2c813f1b425bc4e74625a2607eaca1b97addf9898f834e88af8f1fe2143abc6` — identical to the
revision r26 falsified (`corpus/evidence/round26-measured-revision.json`), so r26 line
citations remain valid. Lane-tree diff at review time touched only C1 usage-harness lines;
no C2 repair has landed yet.

## Verdict

**C2 calendar math is correct on base; both C2 defects are isolated to two named sites and
are independent of the leap/equality slice.** The acceptance oracle for the leap and
due-equality slice is fully determined and already 100% encoded in
`corpus/evidence/round27-regressions.py` (rows below); the repair rows are the two r26
failures. No assertion in the existing suite needs weakening or deletion.

## Independent math check (my own, not the gate's)

`metadata_iso_date` leap rule (base `tools/research-gate.sh:2304`):
`year%400==0 || (year%4==0 && year%100!=0)` — correct proleptic Gregorian. Grammar pins
exactly 4 digits (`:2296`) and `year>=1` (`:2299`), so `0000-*` is rejected before the leap
test. `metadata_days_from_civil`/`metadata_civil_from_days` (`:2310-2336`) are the standard
Hinnant formulation; I re-derived spot values by hand:

- 1900-02-28 → −25509; 1900-03-01 → −25508 (+1; 1900 not leap: %100=0, %400≠0).
- 2000-02-28 → 11015; 2000-02-29 → 11016 (+1; 2000 leap: %400=0).
- 2028-02-28+1 → 2028-02-29 (%4=0, %100≠0). 2100-02-28+1 → 2100-03-01 (not leap).
- 2026-01-02 (DOY 2) + 90d → DOY 92 = 2026-04-02 (Mar 31 = DOY 90).

Due equality: base `tools/research-gate.sh:2756` is `((asof_days > due_days))` — strict
greater-than, so `as_of == due` stays `freshness=current`, no `META_RECHECK_OVERDUE`, rc 0.
This matches the claims' "strict as-of>due overdue semantics". Equality is shared by the
literal-recheck branch (`:2739-2740`) and the cadence branch (`:2747-2749`); the comparison
site is single.

## Acceptance oracle (concrete)

Runner: `python3 corpus/evidence/round27-regressions.py --gate tools/research-gate.sh`
(exit 0 all-match / 1 mismatch / 2 setup; per-row `observe()` checks exit code, required and
forbidden substrings, and `^RESEARCH_GATE: ` / `^META entry=` counts; 30 s timeout per run).
Entry fixture is regenerated per row from `verified-at`/`recheck` fields; every case uses a
fresh synthetic temp dir; gate runs with `CHOUSA_STRICT=0`, no `CHOUSA_RECORD/CLAIMS`.

### Invariant rows — must pass on base AND after the C2 repair (leap/equality slice)

| row | verified-at | recheck | --as-of | expected (rc, verdict tail) |
|---|---|---|---|---|
| `leap-1900` | 1900-02-28 | `1d` | 1900-03-01 | rc0, `due=1900-03-01 freshness=current`, 1 verdict line |
| `leap-2000` | 2000-02-28 | `1d` | 2000-02-29 | rc0, `due=2000-02-29 freshness=current` |
| `leap-2028` | 2028-02-28 | `1d` | 2028-02-29 | rc0, `due=2028-02-29 freshness=current` |
| `leap-2100` | 2100-02-28 | `1d` | 2100-03-01 | rc0, `due=2100-03-01 freshness=current` (2100 non-leap) |
| `allzero-128k` | 2026-01-02 | `0`×131072 + `d` | 2026-01-02 | rc0, `due=2026-01-02 freshness=current` (0d equality) |
| `max-span` | 0001-01-01 | `0003652058d` | 9999-12-31 | rc0, `due=9999-12-31 freshness=current` (equality at max span) |
| `huge-magnitude` / `overflow-span` / `max-date-overflow` | — | 40 nines / `3652059d` / `1d` past end | — | rc0, `due=unknown freshness=unknown` |
| `decimal08` / `decimal09-overdue` | 2026-01-01 | `08d` / `09d` | 2026-01-09 / 2026-01-11 | rc0 current / rc1 `due=2026-01-10 freshness=overdue` |

All four leap rows double as due-equality rows (`as_of == due` → current, rc 0). A mutant
flipping `:2756` to `>=` is caught by exit code alone on every equality row; a mutant that
emits the overdue finding without setting freshness would only be caught by the hardening
below. Selftest identities that must remain byte-identical:
`metadata-asof-leap-2028`, `metadata-asof-leap-2027`, `metadata-asof-boundary`
(equality), `metadata-asof-date-past` (literal overdue with `FINDING META_RECHECK_OVERDUE`),
`metadata-asof-large-cadence` (unknown).

### Repair rows — must FAIL on base, PASS after the C2 repair

| rows | base behavior (accepted r26 ground truth) | post-fix requirement |
|---|---|---|
| `leading-128k-zeros` (`0`×131072+`90d`, as-of 2026-10-21) | SIGSEGV exit 139, zero output (`${digits##+(0)}` at base `:2348`, `shopt -s extglob` `:256`, recurses on run length; bound at `:2350` runs after the strip) | rc1, exactly `due=2026-04-02 freshness=overdue`, 1 verdict line, within timeout |
| `allzero-128k` | same SIGSEGV | rc0, `due=2026-01-02 freshness=current` |
| `ascii-cli-en_US.UTF-8-{２０２６-10-21, ٢٠٢٦-10-21, 2026-10-2１}` | rc1 with raw Bash `10#` diagnostics (`metadata_iso_date` regex `[0-9]` at base `:2296` admits 1040+ numeric code points under glibc UTF-8; CLI call at `:6297` is outside `verify_metadata`'s `local LC_ALL=C` at `:2539`) | rc2, stdout empty, `--as-of must be a valid YYYY-MM-DD date`, 0 verdict lines, forbidden: `invalid integer`, `arithmetic syntax`, `cannot change locale` |
| `ascii-cli-C-*` (same 3 tokens under `LC_ALL=C`) | already pass | must keep passing |

Fix shape advice (not an edit): make the grammar itself locale-independent inside
`metadata_iso_date` (function-local `LC_ALL=C`, or explicit `[0123456789]` class) so every
caller is covered, and replace the extglob strip with a non-recursive linear normalization
that preserves exact value semantics for `08`/`09`/`0003652058d` and all-zero (r26's
sandbox regexfix mutant passed 24/24, demonstrating feasibility). The 7-digit bound and
out-of-range→unknown must be untouched.

## Gaps — suggested hardening (additive, no assertion weakened)

1. **P2 — overdue finding not pinned in regressions rows.** `decimal09-overdue` (and any
   future overdue row) only requires the `META` token. Add required
   `FINDING META_RECHECK_OVERDUE ... due=2026-01-10 as_of=2026-01-11` and, on all
   equality/current rows, forbidden `META_RECHECK_OVERDUE`. The selftest pins the finding
   only on `metadata-asof-date-past`.
2. **P2 — entry-side ASCII grammar untested.** Claims: "Date grammar is ASCII YYYY-MM-DD
   under any inherited locale." The `ascii-cli` rows cover only the CLI `--as-of` value. Add
   one row: entry `verified-at: ２０２６-01-02 …` under `LC_ALL=en_US.UTF-8` must classify
   `verified_at=undated` (rc per other fields) with forbidden `invalid integer`/`arithmetic
   syntax`. On base this should already pass — `verify_metadata` pins `local LC_ALL=C`
   (`:2539`) and `metadata_add_days`'s only caller is `:2748` inside that scope — but r26
   F1 marked the entry side `[INFERENCE, not run]`; this row converts that inference into an
   observed control.
3. **P3 — LANG-only inherited locale.** `ascii-cli` rows always set `LC_ALL` explicitly; the
   r26 default exposure was `LC_ALL` unset + `LANG=en_US.UTF-8`. One row with `LC_ALL`/`
   LC_CTYPE` popped and `LANG=en_US.UTF-8` pins "under any inherited locale" literally.
4. **P3 — literal-recheck equality.** All regressions equality rows are cadence-based; a
   `recheck: 2026-10-21` literal with `--as-of 2026-10-21` → `current` exercises the literal
   branch through the shared comparison. Low value (comparison site is single) but cheap.

## Residual risk and unrun checks

- I ran nothing against the gate (assignment: no verification); all base-behavior statements
  come from the two r26 falsify reports plus static reads of the base blob. The oracle's
  expected values above are my independent derivations (datetime arithmetic by hand), which
  agree with both `round27-regressions.py` and r26's 24/24 Python differential.
- The lane tree was being edited during review (selftest region grew 6351→6381 lines, C1
  usage controls landing). All lines I cite are outside the edited region and verified
  identical to base; the C2 rows of `round27-regressions.py` were stable across reads.
- Unverified here: whether the entry-side row (Gap 2) actually passes on base; behavior
  under musl/BSD regex or non-glibc UTF-8 locales; interaction of a future C2 fix with the
  still-pending C1/C3 edits (L1 runs the single integrated verification pass).

## Tools installed

None.
