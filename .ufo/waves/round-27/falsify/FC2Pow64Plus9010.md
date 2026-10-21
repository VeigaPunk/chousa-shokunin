# FC2Pow64Plus9010 — C2 control `pow64-plus-90`

Item attacked: `corpus/evidence/round27-regressions.py:101`
`('pow64-plus-90', '2026-01-02', '18446744073709551706d', '2026-10-21', None)`
(fixture: `verified-at: 2026-01-02 checked synthetic fixture`, `recheck: 18446744073709551706d`, `--as-of 2026-10-21`; expected exit 0, required `due=unknown freshness=unknown`, counts `^META entry=`=1, `^RESEARCH_GATE: `=1).

Target: immutable lane revision `dd72641e574679c4f7882dd43de072b4c8892d6f`.
Gate `tools/research-gate.sh` sha256 `ca39d14db907ec3fcf41ff0593658b4d6831fa82452944fe1f58463364992f84` (matches declared gate sha).
Pre-repair base `64eec5d41c7cf7f17f5ce1e968e28b3769952596`, gate sha256 `c2c813f1b425bc4e74625a2607eaca1b97addf9898f834e88af8f1fe2143abc6`.
Regressions script sha256 `5afea7863f2b052ba54a46cf2faf88f863d76c61d3d2cf45e091f92bc526a5df`.
All work in `/tmp/chousa-r27-falsify-FC2Pow64Plus9010` (lane archive + synthetic fixtures + gate mutants). No lane file edited; no full `--selftest` or full regression script run; no network; no installs (bash 5.3.20, python3 stdlib only).

## Verdict

**FALSIFIED as an r27 C2 regression control; landed behavior itself HOLDS.**
`pow64-plus-90` passes byte-identically on the pre-repair base gate, and reverting the specific r27 normalization fix leaves it passing. It is sensitive only to the pre-existing 7-digit bound (present at base), so it cannot detect regression/reversion of the repair it is filed under. A same-class input inside the gate's own 8 MiB entry cap still costs ~63 s (7 MiB >90 s), which the 128 KiB control size cannot see.

## 1. Is the expectation derived from the declared contract, independent of gate code?

Contract-derived **semantically**, but not derived the way the suite claims, and not independent in discriminating power.

- Claims file (`corpus/evidence/round27-claims.md`, C2) declares: "A long decimal cadence with leading zeros must compute its representable value without termination; out-of-range values remain unknown." 2^64+90 days from 2026-01-02 is out of the representable year 1–9999 range, so `due=unknown freshness=unknown`, CLEAN (unknown is not overdue) follows from the contract without reading gate code. It also matches the pre-existing selftest expectation `metadata-asof-large-cadence` (gate lines 6157–6162: 30-nines cadence → `due=unknown freshness=unknown verdict=clean`).
- However, the suite's comment "Calendar expectations derive from Python datetime, not the gate arithmetic" (line 75) does not hold for this case. `date_cases` hardcodes `due=None` for `pow64-plus-90`, `huge-magnitude`, `one-then-39-zeros`, `overflow-span`, `max-date-overflow`; Python `date + timedelta` cannot represent them, so only the four `leap-*` rows are actually datetime-derived. The `None` rows are hand-authored contract assertions.
- The assertion is ambiguous about *why* `unknown` happened: the landed gate emits the **same** `due=unknown freshness=unknown verdict=clean` for a calendar-invalid `verified-at` (`2026-02-30 checked`, `2026-13-01`, `2026-02-29` in a non-leap year) with a short `recheck: 90d` (measured; also declared by the pre-existing selftest `metadata-asof-invalid-verified-date`, gate lines 6176–6181). So the required strings alone do not prove overflow rejection — they are also the output of any failure of the verified-at/cadence evaluation legs.

## 2. Mutation: revert/mutate the production fix it targets

Harness: 30-line faithful reimplementation of the script's `observe()` for this one case (`/tmp/.../pow64_control.py`), same fixture, same env (`CHOUSA_STRICT=0 LC_ALL=C`), same cwd/root form, timeout 120 s.

| gate | sha256 (16) | control result | META line |
|---|---|---|---|
| landed dd72641 | `ca39d14db907ec3f` | **PASS** (exit 0, both strings, counts 1/1) | `due=unknown freshness=unknown verdict=clean` |
| base 64eec5d | `c2c813f1b425bc4e` | **PASS** (identical) | `due=unknown freshness=unknown verdict=clean` |
| M1: r27 normalization reverted (`^0*([123456789][0123456789]*)?$` + `BASH_REMATCH[1]` → `digits=${digits##+(0)}`, bound kept) | `2229e80ae6ba32c3` | **PASS** (identical) | `due=unknown freshness=unknown verdict=clean` |
| M2: pre-existing `(( ${#digits} <= 7 )) || return 1` removed (normalization kept) | `7651186d06db0859` | **FAIL, intended reason** | `due=2026-04-02 freshness=overdue verdict=drift`, exit 1, missing `due=unknown freshness=unknown` |

- M1 is the reversion of the *r27 C2 repair* (the mechanism probe `round27-mechanisms.py` counts exactly this site as `C2_recursive_zero_strip`). The control still passes → no mutation sensitivity to the repair.
- That M1 is a real degradation is shown by the control that actually targets the fix: 128 KiB leading-zero cadence (`leading-128k-zeros`) segfaults under M1 (exit 139) and under the base gate (exit 139), while landed returns `due=2026-04-02`, exit 1 (measured, both). The recursive-extglob crash is what the r27 fix removed; `pow64-plus-90` never touches it (no leading zeros).
- M2 failure is a clean semantic mismatch, not setup/parse: exit 1 ≠ 0 and the due/freshness pair is the wrapped value. Bash 5.3.20 wraps `$((10#18446744073709551706))` → `90` (measured), so without the pre-existing bound the gate would compute 2026-01-02+90 = 2026-04-02. That bound is already present at base (base lines 2343–2359), so the control tests pre-base code, not the r27 repair.

## 3. Nearby same-class input: landed gate cost inside its own 8 MiB cap

The landed gate accepts metadata entries up to `SOURCE_READ_MAX_BYTES = 8 MiB` (gate line 271, reader lines 2620–2635). A leading-zero cadence in that size class answers correctly but not promptly:

- `recheck: 0{4194304}90d`, verified 2026-01-02, as-of 2026-10-21: exit 1 in **62,601 ms**, correct `due=2026-04-02 freshness=overdue` (4,194,304-zero fixture, 4,194,466-byte entry).
- `recheck: 0{7340032}90d` (7,340,128-byte entry, under the 8 MiB cap): **timeout rc=124 at 90,000 ms**.
- 128 KiB control case itself: **76 ms**; 1 MiB leading-zero cadence: 2,565 ms.
- Attribution: the cost is not the new ERE (isolated `^0*([123456789][0123456789]*)?$` on a prebuilt 4 MiB string: 163 ms; `^([0-9]+)d$`: 257 ms). It is the per-line CR strip in the metadata header loop, `line=${line%$'\r'}` (gate line 2657), which is quadratic on a long line: microbench `line=${line%$'\r'}` on one all-zero line = 2,338 ms (1 MiB), 11,772 ms (2 MiB), 64,448 ms (4 MiB); read-only loop baseline 56 ms. Gate mutants short-circuiting `metadata_add_days` (S1), `ROOT_PARENT_RE` (S2), the token regex (S3) or the state regex (S4) all remain 62.9–67.5 s, confirming the loop, not the cadence path.
- This is **pre-existing** (same `line=${line%$'\r'}` in base at line 2632) and not introduced by r27; it does mean the C2 promise "long decimal cadence … without termination" holds only for crash/termination, not for practical completion: at 7 MiB the gate that advertises an 8 MiB read boundary does not return within 90 s. The control's 128 KiB size sits 64× below the cap and 32× below the first size (4 MiB) where the gate is grossly slow, so the control cannot surface it.
- [INFERENCE] Extrapolating the measured quadratic (≈4–5.5× per doubling), a line near the 8 MiB cap would cost roughly 4 minutes; not measured (exceeds the 120 s per-command bound).

No same-class **semantic** counterexample was found: 0{131072}+`3652058d` from 0001-01-01 → 9999-12-31 (correct), 0{131072}+`3652059d` → unknown/clean (correct), 0{1048576}+`18446744073709551706d` → unknown/clean in 2,549 ms, and early-date freshness boundaries (verified 0001-01-01, 1d; as-of 0001-01-01/02 current, 0001-01-03 overdue) are correct.

## Minimal counterexamples

1. **Control vacuity**: pre-repair gate `c2c813f1…` produces exactly `META entry=entry.md source=present verified_at=dated recheck=scheduled due=unknown freshness=unknown verdict=clean` / `RESEARCH_GATE: CLEAN (entries=1 complete=1 findings=0 drift=0)` / exit 0 for the control's own fixture — the control passes at base and after reverting the r27 fix (M1).
2. **Same-class latency**: 4 MiB leading-zero cadence within the 8 MiB cap → correct answer after 62.6 s; 7 MiB → no answer at 90 s (rc 124). Root cause the pre-existing quadratic `line=${line%$'\r'}`.

## Limits

- Only single gate invocations and one-case harnesses were run; full `--selftest` and the 58-case regression script were not run (L1 owns them), so no claim here about the other 57 controls.
- Gate mutants were confined to `/tmp` copies; lane files, git/jj state, fleet repo and other lanes were not touched (lane `git status` showed only pre-existing peer changes).
- Base comparison is `64eec5d` (claims-declared base); the claim that the 7-digit bound is pre-existing rests on that blob's lines 2343–2359.
- The 7 MiB number is a timeout (rc 124), not a measured completion time; quadratic extrapolation is marked [INFERENCE].
- "Without termination" is read as “without the r26 crash/abort”; the latency finding is an operability observation, not a claim that the landed cadence semantics are wrong.
