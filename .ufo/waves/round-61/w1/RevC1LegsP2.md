# RevC1LegsP2 — review of C1 legs P04 CHECK, P05 REFUSEROW, P06 REBUILD (round 61, w1)

Scope: `corpus/evidence/round61/c1-count.py` (638 lines, not edited), read against predicate R61-C1 in `claims.md`.
Checked: `sha256sum claims.md` = `9afec8d4…0acec` (matches the frozen digest); `controls/ref-build-spans.py` = `86d64c31…eccfd` (matches).
Scratch: `/fast/scratch/hyaku/chousa-r61/RevC1LegsP2/` (deleted before yield). Installs: none. No git writes. Counter and reference not edited.

## Findings (by severity)

### F1 — false positive, P04 CHECK: a `--check` that verifies one span file passes the leg
- Counter: line 314 `victim = sorted((fx.out / "spans").iterdir())[0]` is fixed (not seed-drawn); line 317 is the verdict.
- Incorrect builder `fpA` = reference with `check()` line 234 changed to `elif name == min(files) and (...)`, i.e. only the first span file is compared. Docstring of the builder: "`--check` re-derives every row and compares it with ... span files".
- Full counter: `python3 -B c1-count.py --builder $S/b/fpA.py --work $S/w/fpA-61001 --seed 61001` → `LEG P04 CHECK pass rc=0,0,1`, `LEGS=20/20 C1=PASS`, exit 0. Same at seed 61002.
- Probe (scratch copy of counter, victim = `[-1]`, in-place byte flip; see P-probe below): `LEG P04 CHECK fail rc=0,0,0`, `LEGS=19/20 C1=FAIL`. The leg detects only the file it picks.

### F2 — false positive, P04 CHECK: a size-only span comparison passes the leg
- Counter: line 315 `victim.write_bytes(victim.read_bytes() + b"x")` appends a byte. The predicate (docstring line 15, claims.md R61-C1) says "after one span byte is changed". An append changes length, so a length-only check catches it.
- Incorrect builder `fpB` = reference with `check()` line 234 changed to `p.stat().st_size != len(files[name].encode("utf-8"))`.
- Full counter: `LEG P04 CHECK pass rc=0,0,1`, `LEGS=20/20 C1=PASS` at seeds 61001 and 61002.
- Probe with in-place flip of byte 0 (line 315 replaced): `LEG P04 CHECK fail rc=0,0,0`, `LEGS=19/20 C1=FAIL`.
- Small fixture (2 rows, `$S/demo`), flipping one byte of the last span file, same length:
  `ref --check` rc=1 `SPANS_ROWS=2 STALE=1`; `cA` rc=1 `STALE=1`; `fpA` rc=0 `STALE=0`; `fpB` rc=0 `STALE=0`.
  Flipping the FIRST span file: `ref` 1, `fpA` 1, `fpB` 0. Restoring the file: all 0.

### F3 — false positive, P05 REFUSEROW: the refused row is always index 0
- Counter: lines 323–324 `sid, url, q, e = rows[0]` / `rows[0] = (... + " absent" ...)`. The bad row is always the first row, so any writer that stops at the first refusal has written nothing yet.
- Incorrect builder `fpC` (scratch): `build()` writes each span file as it goes (lines 207–209 inserted) and `break`s at the first refusal (lines 194, 198, 206 `continue`→`break`). Violates the builder docstring "any refusal writes nothing".
- Full counter seed 61001 and 61002: `LEG P05 REFUSEROW pass rc=1`. Full run `LEGS=15/20 C1=FAIL` (P04, H07, H09, H10, H16 fail, not my legs).
- Probe with bad row at index 1 (line 324 `rows[1]`): `LEG P05 REFUSEROW fail rc=1` for `fpC` (row 0's span file was written); `cA`, `cB`, `cC` still `pass`. Full probe counts: `fpC` 14/20; `cA`/`cB`/`cC` 20/20.

## Limits (observed; NOT counted in LEG_DEFECTS)

- L1 (P05, calibration): `clean_out` (lines 278–284) accepts an `out/` and `out/spans/` left empty by a refusing run. `fpD` (creates `out` and `out/spans` before `read_quotes`) → `LEG P05 REFUSEROW pass rc=1`. Predicate text says "no file written"; empty dirs are not files, but the builder docstring says "writes nothing". Recorded as a stricter-than-needed gap for L1 to decide.
- L2 (P06, by design): P06 (lines 330–338) checks that a second identical build leaves the golden tree. `fpE` (second run with an existing `spans.tsv` returns 0 without writing) → `LEG P06 REBUILD pass rc=0,0`. That builder fails `H07 FOREIGN` (`LEG H07 FOREIGN fail`), which is where the no-op hazard belongs. Not a P06 defect.
- L3 (seed independence): victim choice (line 314) and bad-row index (line 323) do not use the seed. P04/P05 outcomes were identical at seeds 61001, 61002, 61003 for every builder run.

## False negatives (correct builders failing my legs): none found

Three correct builders, each a copy of the reference edited in scratch, all satisfying the builder docstring:
- `cA` — guard-first: a structural pre-check (symlink at `DIR/spans`, non-dir `DIR`) before `read_quotes` (scratch lines 325–326). Refuse policy otherwise unchanged.
- `cB` — replace-link policy: a symlink at `DIR/spans` or `DIR/spans.tsv` is unlinked and replaced by the build (guard_out 255–278, write_out 295–310 in scratch). Symlinked span files are overwritten by `os.replace`.
- `cC` — exit-code variant within a stated set: an unreadable capture exits 2 (H17 allows {1,2}) via an `os_error` flag (scratch lines 89–90, 144–146, 213–215). Refused rows still exit 1.

Runs, seeds 61001 / 61002 / 61003, each `python3 -B c1-count.py --builder <b> --work $S/w/<b>-<seed> --seed <s> --receipt $S/<b>-<seed>.json`:
- every run `LEGS=20/20 C1=PASS`, exit 0;
- every run `LEG P04 CHECK pass rc=0,0,1`, `LEG P05 REFUSEROW pass rc=1`, `LEG P06 REBUILD pass rc=0,0` (9 of 9).
- Under the two probes (pos1, flipLast): `cA`, `cB`, `cC` all `LEGS=20/20 C1=PASS`.

Baseline: reference `controls/ref-build-spans.py`, seed 61001: `LEGS=20/20 C1=PASS`, exit 0; `P04 rc=0,0,1`, `P05 rc=1`, `P06 rc=0,0`.

## Results table (full counter, my legs marked)

| builder | hazard | P04 CHECK | P05 REFUSEROW | P06 REBUILD | full result |
|---|---|---|---|---|---|
| ref (baseline) | — | pass | pass | pass | 20/20 PASS |
| cA / cB / cC (correct) | — | pass ×3 seeds | pass ×3 | pass ×3 | 20/20 PASS ×9 |
| fpA | check: first span file only | **pass** | pass | pass | 20/20 PASS (61001, 61002) |
| fpB | check: size-only | **pass** | pass | pass | 20/20 PASS (61001, 61002) |
| fpC | write-before-refusal, fail-fast | fail | **pass** | pass | 15/20 FAIL |
| fpD | empty out dirs before refusal | pass | pass | pass | 18/20 FAIL (H07, H16) |
| fpE | no-op rebuild on existing manifest | pass | pass | pass | 18/20 FAIL (H07, H12) |

## Probes (scratch copies of the counter; frozen file untouched)
- Scratch probe copies replaced `LANE = HERE.parents[2]` with the absolute lane path (copy only), then applied:
  - `pos1`: line 324 `rows[0]` → `rows[1]`.
  - `flipLast`: line 314 `[0]` → `[-1]`; line 315 append → in-place flip of byte 0.
- Outcomes: `pos1` fpC P05 fail (`LEGS=14/20`); `flipLast` fpA P04 fail and fpB P04 fail (`LEGS=19/20` each); `cA`/`cB`/`cC` 20/20 under both probes; `fpD` under `pos1` still passes P05 (`LEGS=18/20`, limit L1).

## Verdict basis

Operability claim impact: C1 is counted by `c1-count.py`, and the counter prints `C1=PASS` for `fpA` and `fpB`. `fpA` leaves every span file except the first unchecked; `fpB` ignores same-length corruption. The leg counts are therefore weaker than their text ("re-derives every row", "one span byte is changed"). Recommendations for L1 (not applied; counter is frozen): choose the P04 victim by seed among all span files and flip a byte in place; choose the P05 refused row by seed over all positions; keep P05 checking no-write for each refusal position.

Commands run (all `python3 -B`, from the scratch dir): counter on reference (seed 61001); counter on cA/cB/cC (seeds 61001–61003); counter on fpA–fpE (seeds 61001, 61002); counter probes `pos1` and `flipLast` on cA, cB, cC, fpA–fpD (seed 61001); small-fixture `--check` demo with `ref`, `cA`, `fpA`, `fpB`. Every reported number above is copied from those outputs.

VERDICT: LEG_DEFECTS=3 false_negative=0 false_positive=3 legs=P04 CHECK, P05 REFUSEROW, P06 REBUILD
