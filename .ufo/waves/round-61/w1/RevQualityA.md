# RevQualityA — round 61 w1 — QUALITY criterion draft: control matrix before a counter binds data

Scope: draft and attack one new criterion (119) for `corpus/QUALITY.md`. QUALITY.md not edited. Lane read-only; no lane, git or index writes. Lane HEAD at run time `9f32ac05`; the claims freeze `2b0e17b2` is an ancestor (`git merge-base --is-ancestor` → exit 0). Scratch `/fast/scratch/hyaku/chousa-r61/RevQualityA/` deleted at yield. No installs.

## Findings

1. **Both prior counters fail the proposed matrix, for different reasons.** Round-60 counter accepts a token forger (`MATRIX` row `token-forger got=PASS rc=0 last=C1=PASS`). Round-58 counter cannot reach `C1=PASS` on the reference builder (positive row `FAIL`).
2. **Round-60 forge branch is tautological, as its closure said.** `corpus/evidence/round60/c1-count.py:62` sets `forge_blocked = forge_state != "forged_safe"`; `forged_safe` occurs only at line 62, and `run()` (lines 41–44) returns `candidate_safe|baseline_bad|refusal|""`. The injection leg therefore passes for any input.
3. **Round-60 also refuses its own positive.** The reference builder run on the round-60 fixture (foreign `spans/S777-1.txt` present) exits 2 with `refused output … already holds 1 span file(s) this run does not write`, foreign intact. The counter accepts only `candidate_safe` (rc 0 plus `SPANS_ROWS=1` and `WRITTEN=1`), so a correct refusal scores as failure. That is a second, separate counter defect (refusal path not accepted), not only a missing positive.
4. **Round-58 positive failure is real but confounded.** `c1-count.py:160,223,234` emit refusal legs as `pass(refused)` (lowercase, `PASS="pass"` at line 51), while `:391` tests `"=PASS" in l` and `:399` counts it. Observed in a run of the case-patched copy (`ref_pass` changed to `.upper()`, otherwise identical): `ESCAPE_ENTRY=pass(refused)` for a correct refusal. Separately, the reference is not a round-58-conformant positive: `SYMLINK_OUT=fail(rc=0, expected refusal)(target-dir-written!)`, `MANY_QUOTES=fail(rc=0, expected refusal)`, `HELDOUT_OK=fail(rc=1 )`, `FOREIGN=fail(reason-unnamed…)`. The check alone cannot separate "wrong positive" from "unreachable counter". The named reason (no builder can reach `C1=PASS`) is established by the round-58 scribe's satisfying mock (`.ufo/waves/round-58/w1/R58ScribeMistakeMine.md` lines 57–83: all eleven legs behave, `REFUSE=0/7`, `C1=FAIL`) and the round-58 review (`R58ReviewFrozenClaims.md` lines 25–37). I did not re-run that mock (not in the lane).
5. **Equivalent mutant.** Round-60 scores `M08-orphans` (round-61 mutant of the reference) `PASS`. INFERENCE: removing the orphan check lets the builder write rows around the foreign file and exit 0, which the round-60 predicate accepts. Under that predicate M08 is equivalent, so "all mutants must FAIL" is wrong; mutants need a per-counter class (killed, or declared equivalent — criterion 107).
6. **Ordering clause works.** Fixture repo `git init` in scratch: matrix committed before receipt → `merge-base --is-ancestor` exit 0; after → exit 1.

## Draft criterion 119 (text for QUALITY.md; not written there)

119. **A frozen counter's control matrix is committed before the counter binds any data, and the counter is scored on it.** The matrix holds: the base builder; do-nothing stubs (`exit 0`, `exit 2`); a token forger that prints every success token the counter reads and writes nothing; a naive guard; a positive control authored against the counter's declared legs; and frozen mutants of the positive, each killed by the counter's predicate or declared equivalent to it (criterion 107). `MATRIX.tsv` states each row's expected verdict and is committed before the first data receipt. A row's verdict is the counter's exit 0 and its own final line `C1=PASS` (the counter's line, never builder text, criterion 117). Check: `python3 -B corpus/evidence/roundNN/matrix-check.py --counter <counter> --matrix <dir> --work <absolute fresh dir>` prints `MATRIX=k/n POSITIVE=p/1` and exits 0 only when k=n and p=1; and `git -C <lane> merge-base --is-ancestor <MATRIX.tsv add commit> <first data receipt add commit>` exits 0. Shown able to fail (ran this round): round-58 counter → `MATRIX=20/21 POSITIVE=0/1` exit 1; round-60 counter → `MATRIX=18/21 POSITIVE=0/1` exit 1 with `token-forger … got=PASS`; round-61 counter → `MATRIX=21/21 POSITIVE=1/1` exit 0. Named limits: the matrix shows reachability and forgeability only for the rows it lists; it does not show the counter's legs are the right legs (criteria 54, 60); a red positive does not by itself say whether the positive or the counter is wrong — the failing row's per-leg states must be read.

## Check: `matrix-check.py` (as run; scratch copy deleted; reproduce from this text)

```python
#!/usr/bin/env python3
"""Control-matrix check (QUALITY criterion draft 119). Usage: matrix-check.py --counter C.py --matrix DIR --work ABS_DIR"""
import argparse, pathlib, shutil, subprocess, sys
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--counter", required=True, type=pathlib.Path)
    ap.add_argument("--matrix", required=True, type=pathlib.Path)
    ap.add_argument("--work", required=True, type=pathlib.Path)
    ap.add_argument("--timeout", type=int, default=900)
    a = ap.parse_args()
    if not a.work.is_absolute():
        sys.exit("usage: --work must be absolute")
    rows = [l.rstrip("\n").split("\t") for l in (a.matrix / "MATRIX.tsv").read_text().splitlines() if l.strip()]
    ok = pos = 0
    for name, fname, want in rows:
        w = a.work / name
        shutil.rmtree(w, ignore_errors=True)
        try:
            p = subprocess.run([sys.executable, "-B", str(a.counter), "--builder", str(a.matrix / fname),
                                "--work", str(w)], capture_output=True, text=True, timeout=a.timeout)
            rc, last = p.returncode, (p.stdout.strip().splitlines() or ["-"])[-1]
        except subprocess.TimeoutExpired:
            rc, last = 124, "TIMEOUT"
        got = "PASS" if rc == 0 and "C1=PASS" in last else "FAIL"
        good = got == want
        ok += good
        pos += (want == "PASS" and got == "PASS")
        print(f"{name}\texpect={want}\tgot={got}\trc={rc}\t{'OK' if good else 'MISMATCH'}\tlast={last[:70]}")
    print(f"MATRIX={ok}/{len(rows)} POSITIVE={pos}/1")
    return 0 if ok == len(rows) and pos >= 1 else 1
if __name__ == "__main__":
    sys.exit(main())
```

Matrix used (21 rows, `MATRIX.tsv` tab-separated `name file expect`): `base` = `tools/build-spans.py` (sha256 `1ed2650a…`, the round-61 base); `noop0` = `sys.exit(0)`; `always2` = `sys.exit(2)`; `forge-print` = base plus `print('LEGS=20/20 C1=PASS')`; `token-forger` = prints `SPANS_ROWS=1`, `WRITTEN=1`, `LEGS=20/20 C1=PASS`, exit 0, writes nothing; `naive-guard` = base refusing a non-empty `--out`; `reference` = `corpus/evidence/round61/controls/ref-build-spans.py` (expect PASS); `M01-pyc`…`M14-bigform` = the 14 mutants of the reference generated by importing the MUT table of `corpus/evidence/round61/controls/run-c1-controls.py` (expect FAIL). The generator is `gen_matrix.py` (scratch, deleted).

## Runs (all ran; same matrix; `--work` fresh under scratch)

| counter | command | result |
|---|---|---|
| round-61 `c1-count.py` | `matrix-check.py --counter …/round61/c1-count.py --matrix M --work …/runs/r61` | `MATRIX=21/21 POSITIVE=1/1`, exit 0. `reference → PASS last=LEGS=20/20 C1=PASS`; every other row FAIL (`token-forger → LEGS=1/20 C1=FAIL`, `naive-guard → LEGS=10/20`, `M14-bigform → LEGS=19/20`). |
| round-60 `c1-count.py` | same with `round60/c1-count.py` | `MATRIX=18/21 POSITIVE=0/1`, exit 1. `token-forger expect=FAIL got=PASS rc=0 last=C1=PASS`; `reference expect=PASS got=FAIL rc=1 last=C1=FAIL`; `M08-orphans expect=FAIL got=PASS rc=0`. |
| round-58 `c1-count.py` | same with `round58/c1-count.py` | `MATRIX=20/21 POSITIVE=0/1`, exit 1. Only `reference expect=PASS got=FAIL last=C1=FAIL`. |
| round-60 reference direct | `python3 -B r60diag.py matrix/reference.py` (fixture as round-60 counter) | `rc 2`, stderr `refused output … already holds 1 span file(s) this run does not write`, `foreign_intact True`, out tree `['spans', 'spans/S777-1.txt']`. |
| round-58 reference (case-patched copy, legs only) | `python3 -B c1-count-ci.py --builder matrix/reference.py --work …` | `ESCAPE_ENTRY=pass(refused)`, `SYMLINK_OUT=fail(rc=0, expected refusal)(target-dir-written!)`, `MANY_QUOTES=fail(rc=0, …)`, `HELDOUT_OK=fail(rc=1 )`, `SUMMARY OK=3/4 REFUSE=0/7`, `C1=FAIL`. The patch changes only `:391` to `.upper()`; leg generation is untouched. |
| ordering fixture | `git -C $D` commits matrix then receipt; then receipt then matrix | `matrix-before-data: exit=0`; `matrix-after-data: exit=1`. |
| lane freeze ancestry | `git -C <lane> merge-base --is-ancestor 2b0e17b2… HEAD` | exit 0 (claims freeze precedes HEAD `9f32ac05`). |

Round-61 `c1-count.py` (the frozen counter) was run through the matrix with its own counter output; its `C1=PASS` verdict on `reference` (20/20) matches `controls/c1-controls.txt` (`reference rc=0 legs=20/20 OK`).

## Attacks on the draft (what I tried; result)

- **Forger too narrow.** The token forger prints the round-60 tokens. The round-61 counter reads exit codes and legs, so the same row is weak against it (its `LEGS=1/20`). A counter keyed to a token the forger does not print passes that row. Limit stated; criterion 60/29 require forgers keyed to each token class.
- **Exit-only verdict.** A counter exiting 0 while printing `C1=FAIL` would pass an exit-only check. I added the `C1=PASS` final-line requirement after the first run as a guard. Not tested against a counter that does this; no counter in the set does it.
- **Positive that is not a positive.** The round-58 reference fails the round-58 legs, so the check cannot attribute the red row without per-leg states. The draft requires the positive to be authored against declared legs and its per-leg states to be read (criterion 117). Untested as a gate: the check prints only verdicts.
- **Mutant set treated as all-FAIL.** Round-60 M08 survives as equivalent (finding 5). Draft now says killed or declared equivalent.
- **Timing clause.** Ordering verified on a fixture only, not on a real lane commit pair; the lane has no round-61 `MATRIX.tsv` committed.
- **Runtime.** Round-61 matrix ~5–8 min under concurrent load; round-58 about the same. Matrix runs are slow enough to need `timeout 0` for the wrapper (the 300 s background-job kill truncated my first attempt; the rerun is the recorded one).

## Not done / limits

- Did not re-run the round-58 scribe mock (not in the lane); its reachability result is cited from `R58ScribeMistakeMine.md`, not re-measured.
- Did not commit any matrix or checker in the lane (write scope). The checker text above is the artifact the L1 would commit.
- Did not verify the criterion against a non-author reviewer or a counter designed to pass the matrix.
- No external fetch, no network, no fleet, sibling-lane or shokuknow writes.

## Verdict

Criterion 119 text is drafted, its Check runs and discriminates: round-61 green, round-58 and round-60 red. The round-58 red is attributable to the named reason only with the cited scribe receipt; the round-60 forger pass is attributable without it.

VERDICT: CRITERION_CHECK_CAN_FAIL=yes text_ready=yes
