# FDateHugeCadence — C2 40-digit / leading-zero cadence attack (round 26 attempt 1)

Seat `ChousaR26R.FDateHugeCadence`, author-lane advice only (no outside judge).
Judged on: freshness (C2).

**Verdict: C2 FALSIFIED on the spec-v1 correction's "does not terminate the
process" clause.** A cadence with ≥68,000 leading zeros (an 80 KB entry, far
under the 8 MiB reader cap) makes `verify-metadata --as-of` die with SIGSEGV
(exit 139), with **no output**. In a directory scan, one such entry wipes the
output of every other entry. Plain mode (no `--as-of`) and the base
`ba333325` gate handle the same bytes cleanly. The 40-digit, octal-trap,
2^63/2^64 and range-boundary cases all match an independent Python oracle
(24/24), and both isolated mutants are caught.

## Revisions and identities (observed)

- Target: `0e9784bd52eca456b24d0bc40921480a47f91a2b` (from
  `corpus/evidence/round26-measured-revision.json`). The lane HEAD observed at
  report time is the same commit.
- `git show 0e9784bd…:tools/research-gate.sh | sha256sum` =
  `c2c813f1b425bc4e74625a2607eaca1b97addf9898f834e88af8f1fe2143abc6`. This
  equals the revision file's recorded digest and the sandbox archive's digest
  (QUALITY 15).
- Base for the regression comparison: `ba3333254dd337658a4f25e7a9471f9cf4e4567e`
  (`tools/research-gate.sh` and `corpus/knowledge` via `git archive`).
- Sandbox: `/tmp/chousa-r26-falsify-FDateHugeCadence/`, containing `tree/`
  (`git archive 0e9784bd | tar -x`), `base/`, and three mutants. Harness
  sha256 values: `gen.py` b58e7f6a…9420, `run.py` 48d35979…e694,
  `gate_scale.py` 0b948678…57b4, `expected.json` e10b86c3…0d96.
- Runtime: GNU bash 5.3.20(1), Python 3.14.8, `ulimit -s` 8192 (KiB).
- Tools installed: none. `bc` and `/usr/bin/time` are absent, so timing and
  peak RSS were measured in Python (`os.wait4` / `ru_maxrss`).

## Finding F1 (falsifier): extglob leading-zero strip overflows the stack

The site is `tools/research-gate.sh:2348`, in `metadata_add_days`:

```
digits=${digits##+(0)}
```

`shopt -s extglob` is set globally at line 256. Bash's extglob `+(0)`
longest-prefix match recurses in proportion to the run length. It runs before
the 7-digit bound at line 2350, so the bound cannot protect it.

| leading zeros (cadence `0…090d`, verified 2026-01-02, as-of 2026-10-21) | exit | elapsed | peak RSS KiB | output |
|---|---|---|---|---|
| 0 | 1 | 0.01 s | 8740 | due=2026-04-02 overdue (correct) |
| 1,000 | 1 | 0.02 s | 8740 | correct |
| 4,000 | 1 | 0.05 s | 8776 | correct |
| 16,000 | 1 | 0.60 s | 8780 | correct |
| 64,000 | 1 | **8.77 s** | 14988 | correct |
| 68,000 / 72,000 / 76,000 / 80,000 / 96,000 / 128,000 / 192,000 / 256,000 | **SIGSEGV (−11; 139 without `timeout`)** | 0.08–0.24 s | ≈15–17k | **nothing**; the banner is lost too |

Commands: `python3 scale.py` and
`python3 gate_scale.py tree/tools/research-gate.sh asof <sizes>`. Each run is
`timeout 300 env CHOUSA_STRICT=0 bash tree/tools/research-gate.sh verify-metadata scale/zN/e.md --root scale/zN --as-of 2026-10-21`.
Raw output for 256k without `timeout`: `exit=139`, and `asof.out` is empty.

Localization (observed):

- Bare reproduction:
  `bash -c 'shopt -s extglob; d=$(head -c N /dev/zero | tr "\0" 0)90; d=${d##+(0)}'`
  exits 0 at N = 32k, 48k and 64k, and **139** at N = 80k, 96k, 128k,
  160k, 200k and 256k.
- The regex `[[ $r =~ ^([0-9]+)d$ ]]` on a 256,002-character token matches
  fine (exit 0). The recheck classification regex is not the cause.
- Stripping a 256,000-character run of `9`s with the same expansion exits 0.
  Only a leading-zero run triggers the crash.
- The same 256k entry **without `--as-of`** exits 0 with `verdict=clean`, and
  the plain-mode times are 0.02 s at 16k and 0.03 s at 64k. The **base
  `ba333325`** gate also exits 0 on it. So the crash is a regression
  introduced by C2's `--as-of` path, not inherited.

Blast radius (observed): I copied the frozen 29 base entries
(`git archive ba333325 corpus/knowledge`) into `pop/dir` and ran
`verify-metadata pop/dir --root pop/base --as-of 2026-10-21`.

- Control: rc=1, all 29 entries well-formed,
  `RESEARCH_GATE: DRIFT (entries=29 complete=26 findings=33 drift=3)`.
- With one added `zz-crash.md` (80,000 zeros): **rc=139, 0 bytes of
  output.** All 29 legitimate verdicts are lost.
- The same 30-file directory in plain mode: rc=1,
  `RESEARCH_GATE: DRIFT (entries=30 complete=27 findings=33 drift=3)`.

Contract breached: the claims file's "Spec-v1 correction" says a cadence
"whose magnitude exceeds safe computation, yields `due=unknown
freshness=unknown`; it does not terminate the process." The 80k-zero cadence
has value 90, so the oracle expects `due=2026-04-02 freshness=overdue`. Any
result other than termination is acceptable under the spec, but termination
is not. Exit 139 is also outside the gate's 0/1/2 exit contract.

Secondary harm (observed): at 64k zeros, `--as-of` takes 8.77 s versus
0.03 s in plain mode, roughly quadratic growth (×14.6 time for ×4 length
between 16k and 64k). The claims' Harms line says "a slower or less bounded
mode … voids admission", and QUALITY 18 says a byte cap is not a time or
memory budget.

Inference: the crash threshold depends on stack size. A larger `ulimit -s`
raises it toward the 8 MiB file cap at the cost of more quadratic time; any
finite stack leaves an admissible file that crashes. I did not run this.

Candidate fix, sandbox-only (a demonstration, not a production edit; L1
owns integration). In `mut-regexfix/`, I replaced line 2348 with:

```
[[ $digits =~ ^0*([0-9]*)$ ]]; digits=${BASH_REMATCH[1]}
```

Results: all 24 oracle cases pass (`run.py` exit 0), and 16k, 64k and 256k
zeros give exit 1, `due=2026-04-02 freshness=overdue`, in 0.02 s, 0.03 s and
0.19 s (peak 12,872 KiB at 256k). I did not run the selftest or the full
probe on this mutant.

A regression case that would catch this: a ≥128k-zero cadence under
`--as-of` that expects a nonzero due line and an exit in {0, 1}. The
existing `metadata-asof-large-cadence` case (36 nines) and `leap-2028`
(`0001d`) never exercise a long zero run.

## Finding F2 (holds): 40-digit, octal-trap, wrap and range arithmetic

Oracle: `gen.py`, written from the frozen spec independently of the gate.
For each case:

- `due = date.fromisoformat(V) + timedelta(days=int(digits, 10))`.
- Python `OverflowError`/`ValueError` (beyond 9999-12-31 or a huge
  timedelta) maps to `due=unknown freshness=unknown`.
- `overdue` iff as-of > due. Expected rc is 1 when overdue and 0 otherwise,
  and an overdue result must carry a `FINDING META_RECHECK_OVERDUE` line.

Run: `python3 run.py`, which executes
`env -u CHOUSA_RECORD -u CHOUSA_CLAIMS -u CHOUSA_AGGREGATOR_ERE CHOUSA_STRICT=0 bash tree/tools/research-gate.sh verify-metadata cases/N/N.md --root cases/N --as-of A`.
Result: **`MISMATCH 0 of 24`, exit 0**, about 0.01 s per case.

| case | recheck token | V → as-of | due / freshness (gate = oracle) |
|---|---|---|---|
| z40_ninety | 38 zeros + `90d` | 2026-01-02 → 2026-10-21 | 2026-04-02 overdue, rc1 |
| z40_allzero | 40 zeros + `d` | 2026-10-20 | 2026-10-20 overdue, rc1 |
| z40_one_overdue | 39 zeros + `1d` | 2026-10-19 | 2026-10-20 overdue |
| n40_huge | 40 nines | 2026-01-02 | unknown, rc0 |
| n40_onetrail | `1` + 39 zeros | 2026-01-02 | unknown |
| pow63m1 / pow63 / pow64p90 | 9223372036854775807 / …808 / 18446744073709551706 | 2026-01-02 | unknown (no wrap; 2^64+90 is not 90) |
| octal08 / 09 / 010 / 0777 | `08d` `09d` `010d` `0777d` | 2026-10-01 / 2026-01-01 | 10-09, 10-10, 10-11 (decimal, not octal) / 2028-02-17 |
| max_exact / max_exact_z40 / eight_digit_inrange_z | `3652058d`, 33 zeros + `3652058d`, `03652058d` | 0001-01-01 | 9999-12-31 current |
| max_plus1 / max_plus1_z40 | `3652059d`, 33 zeros + `3652059d` | 0001-01-01 | unknown |
| eight_digit / seven_nines | `10000000d` / `9999999d` | 0001-01-01 / 2026-01-02 | unknown |
| end_minus / end_over | `1d` / `2d` | 9999-12-30 → 9999-12-31 | 9999-12-31 current / unknown |
| leap_400 / leap_1900 | `1d` | 2000-02-28 / 1900-02-28 | 2000-02-29 overdue / 1900-03-01 current |
| big_z_overdue | 35 zeros + `00365d` | 2020-01-01 | 2020-12-31 overdue |

Raw per-case output is in `run.log` in the sandbox. The 7-digit length bound
is safe: the largest in-range span is 3,652,058 days (0001-01-01 to
9999-12-31), which has 7 digits.

## Independent failing controls (QUALITY 17)

These are isolated mutants in the sandbox, each run with
`python3 run.py mut-X/tools/research-gate.sh`.

- **nostrip** deletes line 2348. The result is `MISMATCH 6 of 24`, exit 1:
  z40_ninety, z40_allzero, z40_one_overdue, max_exact_z40,
  eight_digit_inrange_z and big_z_overdue go to `unknown` and lose the
  overdue rc and finding. This shows the leading-zero cases detect a missing
  normalization.
- **nobound** deletes the `${#digits} <= 7` line. The result is
  `MISMATCH 3 of 24`, exit 1.
  - n40_huge and pow63 die with rc1 and
    `line 2340: 10#: invalid integer constant (error token is "10#")`, with
    no META line. This is process termination through an arithmetic error.
  - pow64p90 silently **wraps** to `due=2026-04-02 freshness=overdue`.
  - This shows the huge-cadence cases detect a missing bound and integer
    wrap. These are expected negative controls, not regressions in the
    target.
- **regexfix** (the F1 candidate above) gives `MISMATCH 0 of 24`, exit 0.

## Not run

I did not run the full selftest, build, lint, formatter,
`round26-measure.sh`, or the 8 MiB amplification probe. No entry text was
executed. No production file was edited; the only lane write is this report.
