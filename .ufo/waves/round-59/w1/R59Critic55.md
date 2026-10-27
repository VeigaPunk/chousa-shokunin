# R59Critic55 — falsification of the round-58 frozen C1 counter as a positive-verdict calibrator (round 59)

Supersedes my earlier text at this path (written before any run; it only noted absent claims and cited R58 prose). Everything below was run this seat in scratch `/fast/scratch/hyaku/chousa-r59/R59Critic55` (removed). No lane edit, no fetch, no install, no git/jj write.

## Preconditions
- `corpus/evidence/round59/claims.md` is still absent (round59 dir: census-*, controls/c1-before.txt, quarantine-*, s101-open.txt). No round-59 claim is scored here; the only frozen counter/control is round 58's C1.
- Pins at run time: `c1-count.py` sha256 `65da18bb…3d3`; `tools/build-spans.py` = `controls/build-spans-r55.py` = `1ed2650a…0bf6`; lane tree unchanged afterwards (`git status`: only `?? .ufo/waves/round-59/`).

## Method (what is new vs R59Executor09 and the R58 audit)
Executor09 proved the positive path with an escaping/spoofing builder. Nobody had run an HONEST hardened builder. I wrote a scratch wrapper builder (pre-checks SYMLINK/NOT_REGULAR/SIZE/ROWS/FOREIGN, then delegates to the pinned r55 builder) in four variants, and a scratch counter copy changing only `=PASS`→`=pass` at `:391` and `:399` (sha256 `21dae5d3…eeba`, byte-identical to Executor09's copy, so independently reproduced). Copy placed beside a copy of `controls/build-spans-r55.py` (sha `1ed2650a…`) so P3 does not mask the result.

| variant | sha256 | behaviour |
|---|---|---|
| H honest | `3a9d312a…9c6b92` (b-H) | caps rows 100000, raw 64 MiB, honest refusals with reason tokens, no stray writes |
| T tight | `70779fe1…8910af4` | caps rows **3**, raw **200000 B** |
| V loose | `dff9e19a…6c922` | caps rows 100000, raw **83,886,079 B (~80 MiB)** |
| LH leaker | `8d5e59df…0e347` | honest, but on success with `captures` in `--cache` writes `<out>/../leak.txt` |
| LE leaker | (same template) | leaks when `/cache` in `--cache` (the EMPTY_OK fixture) |

## Results
1. **Positive path exists only after the case repair, and only with the sibling control present.** Frozen counter + H: `FOREIGN…MANY_QUOTES=pass(refused)` ×7, `SUMMARY OK=4/4 REFUSE=0/7`, `C1=FAIL`, EXIT=1. Casefixed + H, no `controls/`: `REFUSE=7/7 BEFORE_FOREIGN=absent C1=FAIL`. Casefixed + H, controls present: `SUMMARY OK=4/4 REFUSE=7/7 BEFORE_FOREIGN=deleted DENIED=0/0`, `C1=PASS`, EXIT=0. Confirms P1+P3 on an honest candidate (this is the first honest-candidate positive control; the repair is necessary, not sufficient).
2. **Containment (claim clause 6, "writes nothing outside --out") is vacuous on HELDOUT_OK.** Casefixed + LH: `HELDOUT_OK=pass … C1=PASS`; `w-cf-LH/leak.txt` existed. Casefixed + LE: `EMPTY_OK=fail(write outside --out)`, `C1=FAIL` — so the check works only where the snapshot precedes the run. Source: HELDOUT's `expect_ok(..., snapshot(work))` evaluates `snapshot(work)` as an argument AFTER `run_builder` (c1-count.py near `:333`), while EMPTY_OK takes `snap = snapshot(work)` BEFORE (`:196`). So `outside_before == outside_after` is trivially true on HELDOUT; REBUILD_OK and all refusal legs have no outside-write check except the broken SYMLINK_OUT one. A builder that leaks on the real capture and nowhere else gets `C1=PASS`. Also `snapshot()` ignores directories/symlinks and covers only `work`, never lane/`$HOME`.
3. **Thresholds in the claim are not measured.** Claim says raw reads bounded at 64 MiB and quotes.tsv at 100,000 rows. T (3 rows / 200 KB) and V (80 MiB raw cap) both reach `C1=PASS`. Reason: the fixtures only probe 3-row/129,024 B-capture (accept side) and 100,001 rows / 80 MiB (refuse side); any cap in rows∈[3,100000], raw∈[129024, 80 MiB) scores identically. Over-refusal (T) and the 16 MiB over-allowance (V vs 64 MiB) are invisible; no boundary-at-cap leg exists.
4. **A missing/failing-first-leg builder crashes the counter instead of scoring.** `--builder nonexistent.py`: `FileNotFoundError … out-empty/spans/S777-1.txt` traceback at `:212`, no leg lines, no `C1=`. Same mechanism as Executor09 §5, but reached with a non-control input, so the counter cannot score "builder absent/broken" as FAIL; consumers keying on `C1=PASS` absence see a crash, not a verdict.

## Counterexample verdict
The proposed chain "repair `=PASS` case → C1=PASS means the builder meets claim 1–6" is falsified at claim clauses 4, 5, 6: T and V satisfy no stated threshold yet pass; LH violates containment yet passes. Honest H passing is the only legitimate positive; it requires the case repair AND the r55 control file beside the counter.

## Impacted axes
Calibration (a PASS would over-credit builders with wrong caps/leaks); operability (crash-as-verdict, control-file dependency). Depth not assessed.

## Smallest safe corrections (do not edit frozen round-58 bytes; new round-60 counter)
- Take the pre-run snapshot before EVERY leg and compare outside-`--out` bytes for all legs, including a stray-file probe in each cache/out parent.
- Add cap-boundary legs: exactly 64 MiB accepted (or cap-1), 64 MiB+1 refused; exactly 100,000 rows accepted, 100,001 refused; and a rows>3 / raw>capture-size accept leg so T fails.
- Per-leg typed result + enum reason; wrap fixture setup so a refusing/missing builder yields `C1=FAIL`, never a traceback; make the r55 control self-contained.
- Freeze these H/T/V/LH variants as must-pass/must-deny controls with their sha256 before dispatch.

## Reproduction note
Seat scripts are not preserved (scratch removed as required); variant behaviour is fully specified by the table and the method paragraph; sha256s above allow byte-check if regenerated.
