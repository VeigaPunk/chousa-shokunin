# FC2MaxSpan11: falsification of C2 control `max-span` at dd72641e574679c4f7882dd43de072b4c8892d6f

Author-lane advice, not an outside admission. Agent `ChousaR27.FC2MaxSpan11-11`, 2026-10-21.

**Verdict: FALSIFIED (narrow).**
- (1) Expectation derivation: HOLDS. The literal `9999-12-31` and the freshness rule are contract-correct and independent of gate code.
- (2) Intended-reason failure: HOLDS for the designed regressions (bound ordering/size, strict edge, last day, civil conversion, non-strict overdue). The control is vacuous by construction to due-echo and 7-digit truncation, and to no-bound and normalization-revert.
- (3) Nearby inputs: FALSIFIED for the control. Two concrete inputs kill faults that `max-span` passes. The landed gate HOLDS on every max-span-class input tried (0/3572 differential mismatches; all single-entry boundary probes correct). The one wrong result found is a pre-existing, base-identical verified-at leniency outside this control.
- Calibration: base also passes this control (7/7), so `max-span` is a preservation check, not repair evidence.

## Scope and setup
- Lane `/home/vgpnk/Projects/shokunin/chousa-shokunin` at dd72641e. Gate `tools/research-gate.sh` sha256 `ca39d14db907ec3fcf41ff0593658b4d6831fa82452944fe1f58463364992f84` (matches the assignment). Base `64eec5d41c7cf7f17f5ce1e968e28b3769952596` gate extracted for comparison only (sha `c2c813f1b425bc4e74625a2607eaca1b97addf9898f834e88af8f1fe2143abc6`).
- Sandbox `/tmp/chousa-r27-falsify-FC2MaxSpan11` via `git archive | tar -x`. No lane file, index, or git state was modified. The only lane write is this report.
- Not run: `--selftest`, the full `round27-regressions.py`, and any 128 KiB control on base or on any mutant (the base recursion on long zero runs is the known unsafe reproduction). L1 owns the full runs.
- Derived harness `work/max-span-subset.py`: lines 1-68 and 95-111 of the control, with the C1 usage block and the C2 locale/plain and C3 sections removed, and the date loop filtered to 7 boundary cases (max-span, overflow-span, max-date-overflow, huge-magnitude, one-then-39-zeros, pow64-plus-90, decimal09-overdue). `observe`, `run`, and the expectation tuples are unchanged.

## 1. Expectation derivation (HOLDS, with caveats)
- Control line 102: `('max-span', '0001-01-01', '0003652058d', '9999-12-31', '9999-12-31')`. Freshness is computed with Python `date` and strict `>` (line 114), never from gate output.
- Python confirms the literal: `(date.max - date.min).days == 3652058`; `date(1,1,1) + timedelta(3652058) == 9999-12-31`; `+3652059` raises OverflowError.
- Caveat (calibration): the due value is a typed literal, not computed from the fixture. As-of equals due by construction, so any gate that echoes as-of as due passes this case.
- Caveat (locale): `run()` defaults to `LC_ALL=C` (line 60) and the date loop never passes a locale. No cadence case runs under a UTF-8 locale.

## 2. Mutation: does the control fail for the intended reason?
Targeted landed fix: the 7-digit bound applied to the significant suffix (landed `:2366-2369`). The bound is unchanged from base (`:2350`). The change is the non-recursive normalization replacing base `:2348`. Ten one-line sandbox mutants; all pass `bash -n`; diffs are 1-3 lines.

| Mutant | Change | max-span | other subset cases | function-level differential (mismatches / cases) |
|---|---|---|---|---|
| M1 | raw-length `<=7` check before zero-strip (inserted before `:2366`) | FAIL: `missing 'due=9999-12-31 freshness=current'` | all pass | 586 / 3572 |
| M2 | bound 7 to 6 (`:2369`) | FAIL, same string | all pass | 492 / 3572 |
| M3 | `<=` to `<` at span edge (`:2376`) | FAIL, same string (rc 0) | all pass | 86 / 3572 |
| M4 | entry due = `$AS_OF_ARG` (`:2774`) | **PASS (vacuous)** | decimal09-overdue FAIL (rc 0, expected 1) | entry level, n/a |
| M5 | truncate significant digits to 7 instead of rejecting (`:2369`) | **PASS (vacuous)** | one-then-39-zeros FAIL, pow64-plus-90 FAIL | 64 / 3572 |
| M6 | bound removed (`:2369` becomes `true`) | **PASS (vacuous)** | huge-magnitude FAIL (rc 1), pow64-plus-90 FAIL (rc 1) | 55 / 3572 (non-date output, e.g. `OK -13818274584066417-08-01`) |
| M7 | revert to base `${digits##+(0)}` (`:2366-2367`) | **PASS (vacuous)** | all pass | 0 / 3336 (inputs of 200 chars or fewer only) |
| M8 | last day 9999-12-30 (`:2374`) | FAIL, same string | all pass | 86 / 3572 |
| M9 | civil conversion minus one day (`:2377`) | FAIL (rc 1 plus string) | decimal09-overdue FAIL | 1517 / 3572 |
| M10 | overdue `>=` instead of `>` (`:2781`) | FAIL (rc 1, expected 0, plus string) | all pass | entry level, n/a |

- Targeted ordering and exactness regressions (M1, M2, M3, M8, M9, M10) fail for the intended reason. No parse or setup error occurred.
- Vacuous to M4, M5, M6, M7. M7 is equivalent on every input of 200 characters or fewer; its failure mode needs long zero runs, which are covered by the 128 KiB controls. I did not run those on M7.
- Base revision passes the 7-case subset (all `errors: []`). This control cannot show the C2 repair; it guards only against regressions introduced by the fix.

## 3. Nearby inputs and counterexamples
Single gate runs on landed (`CHOUSA_STRICT=0 LC_ALL=C`, as-of 9999-12-31 unless noted). Mutant columns come from the same fixtures run against M4 and M5.

| Input (verified-at 0001-01-01 unless noted) | Landed | M4 (due=as-of) | M5 (truncate-7) |
|---|---|---|---|
| `0003652058d` (max span, control case) | due 9999-12-31 current, rc 0 | same | same |
| `3652057d` (max minus one) | due 9999-12-30 overdue, rc 1 | **due 9999-12-31 current, rc 0 (WRONG)** | overdue, rc 1 |
| `36520580d` (8 significant digits, 7-digit prefix in span) | unknown, rc 0 | unknown, rc 0 | **due 9999-12-31 current, rc 0 (WRONG)** |
| `3652059d` | unknown, rc 0 | not run | unknown, rc 0 |
| 131072 leading zeros + `3652058d` / `36520580d` / `3652057d` | current rc 0 / unknown rc 0 / overdue rc 1 | not run | not run |
| verified 0001-01-02 + `3652057d` | 9999-12-31 current, rc 0 | not run | not run |
| CRLF line endings, max span | current, rc 0 | not run | not run |
| as-of 2026-10-21, max span | due 9999-12-31 current, rc 0 | not run | not run |
| cadence `٣٦٥٢٠٥٨d` under en_US.UTF-8; fullwidth `３６５２０５８d` under C | recheck=unscheduled, rc 0 (ASCII-only, correct) | not run | not run |

Function-level differential (extracted `metadata_add_days`, sourced with `shopt -s extglob` as gate `:256`, compared to Python proleptic-Gregorian arithmetic). Inputs cover leap, year-1, and 9999 edges, 128 KiB prefixes, Unicode digits, and 1500 random near-span cases. Totals: 3572 cases, 1517 expected OK, 2055 expected UNK.
- Landed: **0 mismatches**.
- Mutants: see the table in section 2.

Pre-existing counterexample, unchanged by the landed diff and reproduced on base. It counters the claim "Date grammar is ASCII YYYY-MM-DD" for verified-at:
- `verified-at: 2026-01-021` (recheck 90d, as-of 2026-10-21): landed and base both give `verified_at=dated due=2026-04-02 freshness=overdue`, rc 1, no finding. The date is silently truncated to `2026-01-02`.
- `verified-at: 0001-01-01x`: both revisions give dated, `due=9999-12-31 current`.
- Cause: the state check (landed `:2723`) and capture (`:2769`) are prefix-anchored, not end-anchored. [INFERENCE] The non-digit-suffix leniency (for example `T10:00Z`) may be intended. The digit-glued case is the clearest counterexample.

## 4. Commands and exit codes
- `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin archive dd72641e574679c4f7882dd43de072b4c8892d6f | tar -x -C /tmp/chousa-r27-falsify-FC2MaxSpan11`: exit 0; gate sha matches.
- `git archive 64eec5d4… tools/research-gate.sh | tar -x -C …-base`: exit 0.
- `python3 work/max-span-subset.py --gate tools/research-gate.sh`: exit 0 (the harness exits 0 by design; mismatches are in its JSON); 7/7 `errors: []`.
- Same harness on base: 7/7 `errors: []`.
- `bash -n work/mut/M{1..10}/tools/research-gate.sh`: exit 0 each.
- Same harness on each mutant: outputs in section 2.
- `python3 work/diff_check.py <gate> <label>`: exit 0 for each; landed `cases=3572 expect_OK=1517 expect_UNK=2055 harness_rc=0 mismatches=0`.
- `python3 work/e2e_check.py`: exit 0; outputs in section 3.
- Long-prefix probes on landed (131173-byte entries): rc 0 current, rc 0 unknown, rc 1 overdue as listed.

## 5. Limits
- Full selftest and full regression script not run (bounds). L1's counts (210, 58/58) are not re-verified.
- M7 long-zero behavior not reproduced (lane instruction). Its verdict covers inputs of 200 characters or fewer only.
- Differential exercises extracted helper functions, not the gate's main. Entry-level behavior was checked only through single gate invocations.
- Base revision used only on short inputs.
- Pre-existing verified-at finding is confirmed on base but its intent is [INFERENCE].
- No network, no host secrets, no /proc, no strace, no installs.

## 6. Tooling
No installs or updates. Used existing GNU bash 5.3.20(1)-release, Python 3.14.8, and locales C, C.utf8, en_US.utf8, POSIX (`locale -a`). Sandbox artifacts live under `/tmp/chousa-r27-falsify-FC2MaxSpan11/work` and are not persisted.

## 7. Advice to the author lane (not an outside admission)
1. Add `max-minus-one-overdue`: verified `0001-01-01`, recheck `3652057d`, as-of `9999-12-31`, expect due `9999-12-30`, rc 1. Kills M4.
2. Add `max-span-plus-one-8digit`: verified `0001-01-01`, recheck `36520580d`, as-of `9999-12-31`, expect unknown, rc 0. Kills M5.
3. Add a UTF-8-locale cadence case (`٣٦٥٢٠٥٨d` under en_US.UTF-8 expects unscheduled) so the cadence path is locale-pinned.
4. Relabel `max-span` as a preservation check. Repair evidence is the 128 KiB and locale controls.
5. Decide the verified-at grammar. If strict, add a control for `2026-01-021` expecting `META_VERIFIED_AT_UNDATED`. This is pre-existing and outside the round27 repairs.
