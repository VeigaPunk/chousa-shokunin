# FC2Decimal0814: falsification of C2 control `decimal08`

- Wave: chousa round27 attempt1, falsify. Pin: `dd72641e574679c4f7882dd43de072b4c8892d6f`.
- Gate: `tools/research-gate.sh`, sha256 `ca39d14db907ec3fcf41ff0593658b4d6831fa82452944fe1f58463364992f84` (verified against `git show`).
- Item: `corpus/evidence/round27-regressions.py:105`, `('decimal08', '2026-01-01', '08d', '2026-01-09', '2026-01-09')`, run by the C2 date loop (lines 112-117).
- Sandbox: `/tmp/chousa-r27-falsify-FC2Decimal0814` (git archive of the pin; `base/` = `64eec5d4` gate; `mut/` = mutants). Synthetic fixtures only. Not run: full `--selftest`, the full regression script, any 128 KiB input against base or extglob mutants.

## Verdict: FALSIFIED (control-level, calibration)

The `decimal08` expectation is contract-correct, and the control does fail for the intended reason under a raw-octal reversion (M3). But it is vacuous for the octal-valued leading-zero class. Mutant M4 (one-zero strip, raw arithmetic) passes `decimal08` and `decimal09-overdue`, and the full script catches M4 only through length-cap controls. The landed gate itself held on all 59 landed-gate probes (no counterexample found; this is not a proof).

## 1. Is the expectation derived from the contract? HOLDS

- Contract (round27-claims C2): a long decimal cadence with leading zeros must compute its representable value; overdue is strict `as-of > due`.
- `08d` = 8 days. `2026-01-01` + 8 = `2026-01-09` (Python `date(2026,1,1)+timedelta(days=8)`). `+9` gives `2026-01-10`, matching `decimal09`.
- `expected_rc` and `freshness` are computed in Python from the literal dates (lines 114-115). The literal `due` is hand-typed, and I verified it independently. Gate code is not consulted.
- Boundary: as-of == due gives `current`, rc 0.

## 2. Mutating the targeted fix: partly HOLDS

Target behavior: leading-zero decimal reads as decimal, never octal. Landed `metadata_add_days` lines 2366-2370 (ERE significant-suffix capture, `(( ${#digits} <= 7 ))`, then `amount=$((10#$digits))`). The gate sets `shopt -s extglob` at line 256.

Each mutant is one edit in its own sandbox copy, run as the control's single case (`LC_ALL=C`, `CHOUSA_*` removed, `CHOUSA_STRICT=0`, `verify-metadata <entry> --root <root> --as-of 2026-01-09`):

| variant (gate sha12) | edit | decimal08 | decimal09-overdue | observation |
|---|---|---|---|---|
| landed (`ca39d14db907`) | none | PASS | PASS | `META ... recheck=scheduled due=2026-01-09 freshness=current verdict=clean`, rc 0 |
| base `64eec5d4` (`c2c813f1b425`) | extglob `${digits##+(0)}` | PASS | PASS | decimal08 does not reproduce a base failure |
| M1 (`2229e80ae6ba`) | revert ERE capture to base extglob strip | PASS | PASS | recursion fix is not detected by decimal08 |
| M2 (`488db665123b`) | drop `10#` only | PASS | PASS | equivalent: normalization already removed leading zeros |
| M3 (`6c1710865837`) | drop normalization and `10#` (`digits=$digits`; `amount=$((digits))`) | **FAIL** rc 1 | **FAIL** rc 1 | stderr `line 2369: 08: value too great for base (error token is "08")`; no META or RESEARCH_GATE line. Intended octal misread, not harness or setup error |
| M4 (`e5c3dc55934f`) | `digits=${digits#0}`; `amount=$((digits))` | PASS | PASS | vacuous, see C1 |
| M5 (`407efdc95353`) | class typo `[12345678]` | PASS | FAIL | decimal09 catches it, decimal08 cannot |
| M6 (`42afde7658c9`) | `digits=${BASH_REMATCH[0]}` | PASS | PASS | caught only by long-zero or length controls |

Reading: decimal08 discriminates the raw-octal reversion (M3) for the intended reason. It is blind to reversions of the recursion fix (M1, M6), which is not its target.

## 3. Counterexamples

### C1 (control vacuity): octal-valued leading-zero cadence

- Minimal input: `recheck: 0010d`, `verified-at: 2026-01-01`, `--as-of 2026-01-11`.
- Landed: `due=2026-01-11 freshness=current`, rc 0. Correct (10 days).
- M4 (as-of 2026-01-12, observed): `due=2026-01-09 freshness=overdue`, rc 1. The `0010` is read as octal 8. M4 at as-of 2026-01-11 fails the same way (rc 1, `due` wrong).
- M4 passes `decimal08` and `decimal09-overdue`, because after the one-zero strip the 8/9 has no leading zero.
- Other same-class M4 failures that no control covers:
  - `00100d`, as-of 2026-04-11: landed `due=2026-04-11` current, rc 0; M4 `due=2026-03-06` overdue, rc 1.
  - `000777d`, as-of 2026-12-31 (run by hand): landed `due=2028-02-17 freshness=current verdict=clean`, rc 0; M4 `due=2027-05-27 freshness=current verdict=clean`, rc 0. Silent wrong date.
- Script coverage: no leading-zero token in `round27-regressions.py` has all-0-7 digits with a significant part of two or more digits. So the octal-value class has no direct coverage.
- M4 is caught in the script only by length refusal. `max-span` under M4 gives `due=unknown freshness=unknown` where `9999-12-31` is expected. The 128K-zero family refuses the same way: the variant `'0'*131072+'08d'` under M4 gives `due=unknown`.
- Forward risk, verified on mutant M4b (M4 with the 7-digit cap raised to 9): decimal08 PASS, decimal09 PASS. `max-span` now fails only by octal crash (`line 2369: 003652058: value too great for base`). The leading-128k case fails by length. `0010d` silently gives `due=2026-01-09 freshness=overdue`, rc 1, and nothing in the script explains it.

### C2 (landed gate): no counterexample found, HOLDS (not proof)

All landed results matched Python-derived expectations on:

- Octal-valued and octal-invalid mixes: `08d`, `09d`, `007d`, `0017d`, `008d`, `0010d` (current and overdue edges), `00100d`, `000777d`, `0000d`, `0000000d` at 9999-12-31, and 28 leading zeros then `8d`.
- Calendar: 2026-12-31 +08d rolls to 2027-01-08; 2028-02-28 +08d is 2028-03-07 (leap); 0001-01-01 +0d and +1d (overdue); 9999-12-30 +1d gives 9999-12-31; 9999-12-30 +2d gives unknown; 0001-01-01 +0003652058d gives 9999-12-31; +0003652059d gives unknown.
- 100-zero prefixes: `1000000d` gives `4763-11-29` (Python-checked); `9999999d` gives unknown; `0d` gives the verified date.
- 128 KiB tokens (landed only, about 75 ms each): `'9'*131072+d` unknown; `'1'+'0'*131071+d` unknown; `'0'*65536+'1'*65536+d` unknown; `'0'*131072+'1d'` gives 2026-01-02 current; `'0'*131072+'08d'` gives 2026-01-09 current.
- Non-ASCII and non-cadence: `٠٨d` and `０８d` under `en_US.UTF-8` give `recheck=unscheduled` with no due date. `-08d`, `+08d`, `08D`, `08 d`, `08days` are unscheduled. Verified-at `٢٠٢٦-01-01`, `２０２６-01-01`, or NBSP-prefixed give `verified_at=undated`, rc 1. Verified `2026-02-30` gives unknown.

### Residual, inherited (not a C2 regression)

- Refused or out-of-range long cadences exit 0 with `due=unknown freshness=unknown verdict=clean` and no finding. This follows the contract ("out-of-range remain unknown"), but a regression to unknown is silent at the verdict level. Only exact `due=` controls catch it.
- The date-case `observe()` has no forbidden tokens for bash arithmetic diagnostics, unlike the ASCII CLI cases, which forbid `arithmetic syntax`. A mutant that printed a diagnostic yet emitted correct META lines and exit 0 would pass. I did not construct one.

## Advice to the author lane (not an admission)

1. Add `0010d` (verified 2026-01-01; as-of 2026-01-11 gives current, rc 0; as-of 2026-01-12 gives overdue, rc 1) and `00100d` (as-of 2026-04-11 gives current, rc 0). Both pass the landed gate and fail M4 (observed).
2. Forbid `value too great for base` and `invalid octal` in date-case output.
3. Keep `decimal08` unchanged. Its expectation is correct.

## Tooling and limits

- Installs: none. Used GNU bash 5.3.20, Python 3.14.8, and git read-only (`archive`, `show`, `ls-tree`, `cat-file`). No lane git or index writes. Lane production files untouched. This report is the only lane write.
- Harness: a per-case replica of the control's `run()` and `observe()` (same env filtering, entry text, arguments, and rc, required, and count checks). It is not the control file.
- Volume: 252 single-case gate invocations (59 landed, 33 base, 160 mutant). No full selftest or regression run. No 128 KiB input on base or extglob mutants.
- Scope: only the metadata add-days path (single caller, line 2773) was audited. The rest of the gate was not reviewed.
- Mutants were edited through the edit tool in the sandbox. Diffs are reproducible from `/tmp/chousa-r27-falsify-FC2Decimal0814/mut/*`.

Trailer: report path relative to the lane is `.ufo/waves/round-27/falsify/FC2Decimal0814.md`.
