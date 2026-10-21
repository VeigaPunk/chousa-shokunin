# FC2Decimal09Overdue15 — falsify C2 control `decimal09-overdue`

Target: dd72641e574679c4f7882dd43de072b4c8892d6f; gate sha256 ca39d14db907ec3fcf41ff0593658b4d6831fa82452944fe1f58463364992f84 (verified in sandbox).
Sandbox: /tmp/chousa-r27-falsify-FC2Decimal09Overdue15 (git archive of dd72641e). No lane files touched except this report. No installs.

## Verdict

Gate behavior: **HOLDS**. No counterexample was found among 30 nearby inputs of the same kind (decimal cadences with leading zeros).
Control as a guard for the round-27 fix: **FALSIFIED (vacuous)**. `decimal09-overdue` stays green when the C2 leading-zero normalization fix is reverted, both on the true base gate and on a minimal revert mutant. It is still a valid preservation control (a decimal cadence must not be read as octal, and the overdue branch must be strict), but it gives no evidence for the C2 repair. That evidence comes from `leading-128k-zeros` and `allzero-128k`.

## (1) Is the expectation derived from the contract, independent of gate code?

Yes. Row `('decimal09-overdue', '2026-01-01', '09d', '2026-01-11', '2026-01-10')` (regressions.py:106).
- `due` is a hand-written literal. It is not computed by `datetime` despite the comment at :95, but it is correct: `date(2026,1,1)+timedelta(9) == 2026-01-10`.
- `freshness` and the expected exit code are computed in Python with a strict `as-of > due` comparison (:114). This matches the contract's "strict as-of>due overdue semantics".
- Assertions: exit 1; the substring `due=2026-01-10 freshness=overdue`; exactly one `^RESEARCH_GATE: ` line; exactly one `^META entry=` line.

Weakness: the expected exit code 1 is the same code that a `set -e` arithmetic crash produces. Under mutant M4 the gate crashed with rc=1, and the exit-code check alone passed. Only the substring and count checks caught it. This is not a defect today, but the exit-code check is not independently discriminating for overdue cases.

## (2) Mutation: revert or mutate the targeted fix

Harness: `probe.py` in the sandbox replicates the control's exact fixture text, environment (`CHOUSA_STRICT=0`, `LC_ALL=C`, `CHOUSA_*` stripped) and assertions, and checks each case against a Python `datetime` oracle. The probe exited 0 in every run below; PASS means the mutant survived the case.

| gate | change | decimal09-overdue | decimal08 | killed by |
|---|---|---|---|---|
| landed | none | PASS | PASS | n/a |
| B0 = full 64eec5d gate (sha c2c813f1…) | the real pre-fix gate | **PASS** | PASS | (huge-cadence baseline not rerun, per contract) |
| M1 | restore base `digits=${digits##+(0)}` (revert the C2 fix only) | **PASS** | PASS | `leading-128k-zeros`: rc=-11 (SIGSEGV), 0 records |
| M2 | `amount=$((digits))` (drop `10#`) | **PASS** | PASS | none of these (normalization already strips the zero) |
| M3 | drop the regex normalization, keep `10#` | **PASS** | PASS | (10#09 = 9) |
| M4 | drop normalization and `10#` | MISMATCH: rc=1/1, but `line 2368: 09: value too great for base`, gate=0 meta=0 | MISMATCH rc=1/0 | both |
| M5 | `BASH_REMATCH[0]` (keep the zeros) plus no `10#` | MISMATCH, same octal error | MISMATCH | both |
| M6 | `asof_days >= due_days` | **PASS** | MISMATCH (overdue at as-of = due) | decimal08 |
| M7 | due + 1 day | MISMATCH rc=0/1, due=2026-01-11 current | MISMATCH | both |

Conclusions:
- Reverting the round-27 fix (B0 and M1) does not make this control fail. The fix replaced extglob `${digits##+(0)}`, which recurses on long zero runs, with a single ERE capture. A two-character input `09` never exercises that difference. The revert is caught only by the 128 KiB controls. M1 gives rc=-11 on both `0×131072+90d` and `0×131072+09d`, while the landed gate passes both.
- The control fails for the intended reason (octal misparse) only when both defenses are removed (M4, M5). In that case `decimal08` dies identically, so `decimal09-overdue` killed nothing that `decimal08` did not also kill.
- It does not test strictness at the boundary; `decimal08` (as-of = due → current) does (M6).

## (3) Nearby inputs on the landed gate (all matched the Python oracle)

Commands: `timeout 120 python3 probe.py tools/research-gate.sh <cases>`, exit 0, all PASS:
- `09d` at as-of = due (current) and as-of = due−1 (current).
- `010d` (valid octal 8, decimal 10): due 2026-01-11, both current and overdue; no octal misread.
- `07d`, `0d` overdue, `00d` current, `0009d`, `0777d` (due 2028-02-17, not octal 511).
- `09d` from 9999-12-22 gives 9999-12-31; from 9999-12-23 gives unknown. `00003652058d` gives 9999-12-31; `0010000000d` gives unknown.
- `09d` across a leap day (2028-02-21 → 2028-03-01), across a year boundary (2025-12-28 → 2026-01-06), and in year 0001.
- Unicode cadences `٠٩d`, `０９d` and mixed `0٩d` under en_US.UTF-8 and C: recheck=unscheduled, due=unknown, rc 0, no arithmetic error.
- `09d` under en_US.UTF-8 at as-of above and at due: correct.
- `0×131072+09d`: due 2026-01-10 overdue, rc 1.
- Direct runs: CRLF entry, `recheck:09d` with no space, and a tab plus trailing note all give due=2026-01-10 freshness=overdue, rc=1. Plain mode gives recheck=scheduled verdict=clean, rc=0, with no due or freshness fields.

## Smallest safe correction (author-lane advice)

No gate change is needed. If the round-27 evidence counts `decimal09-overdue` toward the C2 repair, relabel it as a preservation control: "octal-invalid leading-zero cadence plus strict overdue, already correct at base". Optionally add `010d` (valid octal), which uniquely kills an octal-reading mutant that still parses 08 and 09 (for example a fallback that uses `$((digits))` when the value is valid octal). Optionally require the `META_RECHECK_OVERDUE` finding, so overdue rows do not depend on rc=1, which a crash also produces.

## Limits

Mutants were hand-picked (7 plus the base gate); this is not an exhaustive mutation analysis. I did not run the full selftest or the full regression script, which belong to L1. Only the locales C, C.utf8 and en_US.utf8 are installed. Impacted axis: freshness (credit for the control's evidence), not gate correctness.
