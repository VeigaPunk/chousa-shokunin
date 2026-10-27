# R59Executor12 — round-58 frozen C1 counter, positive-verdict path

Seat: R59Executor12 (leaf, id `R59Executor12-3`), axis **operability**, milestone
"Round59 build and falsify controls for positive verdict-path calibration".
Scope: isolated scratch inspection/execution of the exact round-58 frozen counter, its frozen
controls, and verbatim execution of its verdict-path source lines. No lane file was edited; no
git/jj/index write; no external fetch; no install; no pacman.

## Preconditions observed before work

- `corpus/evidence/round59/claims.md` — the dispatch-mandated frozen-claims path — **does not
  exist**. `corpus/evidence/round59/` contained only `census-start.txt` and `controls/c1-before.txt`
  at start. No round-59 frozen claim/predicate was therefore available to test.
- `corpus/evidence/round59/controls/c1-before.txt` sha256
  `2c9bbe5446ae4f733bf17a2836cc1b32e823fc8bc287d3da42801b948cfaebfe` is **byte-identical** to
  `corpus/evidence/round58/controls/c1-before.txt`. The round-59 "before" receipt is a copy, not a
  new measurement.
- Frozen artifacts used (read-only):
  - `corpus/evidence/round58/c1-count.py` — 406 lines, sha256
    `65da18bbcb03581ca98354d90049215ed3cab3bfd3e41d483908dc1e1c703d3f`.
  - `corpus/evidence/round58/controls/REFUSEALL.py` sha256 `e7721cef…72fb`;
    `corpus/evidence/round58/controls/build-spans-r55.py` sha256 `1ed2650a…0bf6`.
  - `tools/build-spans.py` sha256 `1ed2650a…0bf6` — the lane builder **is** the pinned round-55
    unhardened builder, so the frozen "before" leg values are expected on the lane head.
- Scratch: `/fast/scratch/hyaku/chousa-r59/R59Executor12/` only (shared path with peer
  `R59Executor12`; two of my run directories disappeared mid-seat, so the baseline was re-run in a
  uniquely named subdir and every receipt below is inline text, not a scratch path).

## Commands and exact outputs

### R1 — exact frozen counter, lane builder, frozen controls

```
cd /home/vgpnk/Projects/shokunin/chousa-shokunin
python3 corpus/evidence/round58/c1-count.py --builder tools/build-spans.py \
  --work /fast/scratch/hyaku/chousa-r59/R59Executor12/e12-lane-w2 \
  --controls corpus/evidence/round58/controls
```

```
EMPTY_OK=pass
REBUILD_OK=pass
FOREIGN=fail(rc=0, orphans deleted: foreign gone=True)
SYMLINK_OUT=fail(rc=0, expected refusal)(target-dir-written!)
SYMLINK_CACHE=fail(rc=0, expected refusal)
FIFO_TXT=fail(rc=1, reason ['NOT_REGULAR', 'FIFO', 'REGTYPE', 'SYMLINK'] absent in 'build-spans: refused S571: no defined text form for f4088c6d6da1f4763182a51d (raw neither OLE nor zip, no .txt)\n')
DEVZERO_TXT=fail(rc=1, reason ['NOT_REGULAR', 'SIZE', 'SYMLINK', 'REGTYPE'] absent in 'build-spans: refused S581: no defined text form for a172f04219497476db868414 (raw neither OLE nor zip, no .txt)\n')
FAT_RAW=fail(rc=1, reason ['SIZE'] absent in 'build-spans: refused S551: capture-text refused f96cbd6d82dbae8a8e2c6223.raw: ole-malformed: sector shift 0, mini shift 0\n')
MANY_QUOTES=fail(rc=0, expected refusal)
ESCAPE_ENTRY=pass(refused)
HELDOUT_OK=pass
BEFORE_FOREIGN=deleted
CONTROL_REFUSEALL=denied
CONTROL_build-spans-r55=denied
DENIED=2/2
SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=2/2
C1=FAIL
EXIT=1
```

Wall time 8.51 s (first identical run: 64.86 s, same 22 lines and exit 1). This reproduces
`corpus/evidence/round58/controls/c1-controls.txt` line for line.

### R2 — exact frozen counter, frozen REFUSEALL control as candidate

```
python3 corpus/evidence/round58/c1-count.py \
  --builder corpus/evidence/round58/controls/REFUSEALL.py \
  --work /fast/scratch/hyaku/chousa-r59/R59Executor12/e12-refuseall-w2
```

```
Traceback (most recent call last):
  File ".../corpus/evidence/round58/c1-count.py", line 406, in <module>
    sys.exit(main())
  File ".../corpus/evidence/round58/c1-count.py", line 212, in main
    foreign.write_bytes(b"foreign evidence bytes\n")
  ...
FileNotFoundError: [Errno 2] No such file or directory:
'/fast/scratch/hyaku/chousa-r59/R59Executor12/e12-refuseall-w2/out-empty/spans/S777-1.txt'
EXIT=1
```

### R3 — positive-verdict-path probe (no edit to the frozen file)

Scratch script imports the exact frozen module (`importlib`), calls its own `expect_ok` and
`expect_refuse` to obtain the leg strings a fully conforming candidate emits, then `exec`s the
frozen verdict lines **verbatim** from the file (`389–394`, `398–401`). Output:

```
SAFE_LEG_RETURNED: 'EMPTY_OK=pass'
REF_LEG_RETURNED: 'FOREIGN=pass(refused)'
REF_LEG_RETURNED: 'SYMLINK_OUT=pass(refused)'
REF_LEG_RETURNED: 'SYMLINK_CACHE=pass(refused)'
REF_LEG_RETURNED: 'FIFO_TXT=pass(refused)'
REF_LEG_RETURNED: 'DEVZERO_TXT=pass(refused)'
REF_LEG_RETURNED: 'FAT_RAW=pass(refused)'
REF_LEG_RETURNED: 'MANY_QUOTES=pass(refused)'
OK_LEGS: ['EMPTY_OK=pass', 'REBUILD_OK=pass', 'HELDOUT_OK=pass', 'ESCAPE_ENTRY=pass(refused)']
389:     ok_pass = all(l.endswith("(pass)") or l.endswith(")") and f"{FAIL}" not in l and "=pass" in l for l in ok_legs)
390:     ok_pass = all(("=pass" in l) for l in ok_legs)
391:     ref_pass = all(("=PASS" in l) for l in ref_legs)
392:     integrity = any(l == "BEFORE_FOREIGN=deleted" for l in legs)
393:     denied_pass = (denied == total) if total else True
394:     verdict = "PASS" if (ok_pass and ref_pass and integrity and denied_pass) else "FAIL"
398:     print(f"SUMMARY OK={sum('=pass' in l for l in ok_legs)}/{len(ok_legs)} "
399:           f"REFUSE={sum('=PASS' in l for l in ref_legs)}/{len(ref_legs)} "
400:           f"BEFORE_FOREIGN={before} DENIED={denied}/{total}")
401:     print(f"C1={verdict}")
EVALUATED ok_pass: True
EVALUATED ref_pass: False
EVALUATED integrity: True denied_pass: True
EVALUATED verdict: FAIL
EVALUATED summary lines:
SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=2/2
C1=FAIL
NEGATIVE_PROBE_case_sensitive_match: False
COUNTERFACTUAL_line391: ref_pass = all(("=pass" in l) for l in ref_legs)
COUNTERFACTUAL ref_pass: True verdict: PASS
```

### R4 — SYMLINK_OUT leg block executed verbatim (lines 227–236)

Same technique: `exec` the frozen source lines with a stub `run_builder` for three behaviours.
(`raw` = the frozen `expect_refuse` return before the block's override; `final_leg` = what the
counter actually appends.)

```
A_rc0_nowrite: rc=0 write_target=False
  raw_expect_refuse='SYMLINK_OUT=fail(rc=0, expected refusal)'
  final_leg='SYMLINK_OUT=pass(refused)'
B_rc1_wrote_target: rc=1 write_target=True
  raw_expect_refuse='SYMLINK_OUT=pass(refused)'
  final_leg='SYMLINK_OUT=pass(refused)(target-dir-written!)'
C_rc1_correct_reason_nowrite: rc=1 write_target=False
  raw_expect_refuse='SYMLINK_OUT=fail(/fast/.../realdir/spans.tsv was touched/removed)'
  final_leg='SYMLINK_OUT=pass(refused)'
EXIT=0
```

## Findings

**D1 — the positive verdict is unreachable by construction (fatal to the frozen predicate).**
`PASS = "pass"` (line 51); `expect_ok` and `expect_refuse` emit `f"{name}={PASS}…"` (147, 160),
and the hardcoded `ESCAPE_ENTRY` string is lowercase (315). The aggregate tests `"=PASS" in l`
(391) and the summary counts `sum('=PASS' in l …)` (399). R3 supplies the exact helper-produced
strings for a candidate whose 4 safe and 7 refusal legs all pass and gets `ok_pass=True`,
`ref_pass=False`, `REFUSE=0/7`, `C1=FAIL`. No candidate builder can ever produce `C1=PASS` from
these bytes; the frozen claim is unprovable and its target state is unrepresentable. A one-case
correction to line 391 flips the same probe to `verdict: PASS`, isolating the defect to the
token comparison. [Observed in R3; mechanism read from lines 51/147/160/315/391/399.]

**D2 — the SYMLINK_OUT refusal leg passes candidates that never refused.** Lines 232–236 append
`expect_refuse(...)`, then unconditionally replace the leg with `pass(refused)` whenever the real
target directory is empty — regardless of `returncode` or diagnostic text. R4/A: a builder that
exits **0** and writes nothing is recorded `SYMLINK_OUT=pass(refused)`. R4/C: a refusal whose
reason class is wrong is also recorded pass. The leg therefore cannot discriminate refusal from
silence. [Observed in R4.]

**D3 — writing the forbidden target is still scored a pass.** `expect_refuse` fails only when a
`forbidden_touch` path is *absent* (`if not p.exists(): return FAIL("… was touched/removed")`,
lines 158–160): the predicate is inverted. R4/B: refusal text + a written `realdir/spans.tsv`
returns `pass(refused)`; the block then only appends the suffix `(target-dir-written!)`, which the
aggregate ignores (a `=pass` leg remains a pass). The counter's own stated integration hazard
therefore cannot fail its leg. [Observed in R4; line 236 appends rather than downgrades.]

**D4 — the control denominator is optional and vacuous.** `denied_pass = (denied == total) if total
else True` (393). The frozen predicate command in `corpus/evidence/round58/claims.md` is
`… --builder <builder> --work <fresh-absolute-dir>` with **no** `--controls`, and the round-59
before receipt shows `DENIED=0/0`. With line 391 corrected, an unaccompanied run would certify
`C1=PASS` without any deny control, so the claim's "do-nothing controls must not reach `C1=PASS`"
clause is not exercised by the declared invocation. [Observed: claims text, R1/`c1-before`
`DENIED=0/0`, line 393.]

**D5 — a do-nothing control crashes the counter instead of being evaluated.** A candidate that
never writes the safe output makes line 212 fail (`out-empty/spans/S777-1.txt` missing): R2 exits
1 with a traceback and prints no `C1=` line. Inside `--controls`, this is counted as
`CONTROL_REFUSEALL=denied` solely because no `C1=PASS` tail exists (line 377), not because the
counter evaluated and rejected it. Deny evidence is therefore a crash artifact for this control.
[Observed in R1 and R2; denial path read from lines 370–379.]

**Minor.** Line 389 assigns `ok_pass` with a first expression that line 390 immediately overwrites
(dead expression); `expect_ok`'s `want` dict (line 136) is also unused. Neither changes the verdict,
but both show the aggregate path was not exercised.

## Operability implication

The round-59 baseline (`C1=FAIL`, `OK=4/4`, `REFUSE=0/7`) is reproduced exactly and is a correct
falsification of the unhardened lane builder. But the frozen gate cannot certify the repair it
asks for: any positive receipt for these bytes is impossible (D1), and two refusal/side-effect
legs would pass a silent or destructive candidate (D2–D3). The round-58 lesson's "unprovable"
classification is mechanically confirmed rather than merely accepted. No numeric operability score
change is claimed by this seat.

## Prospective calibration targets (not applied; for the freezing seat)

1. Freeze a positive control that reaches the **exact** final `C1=PASS`/exit-0 predicate before wave
   data; keep frozen bytes append-only.
2. Use one token case consistently across emit (147/160/315), aggregate (391) and summary (399).
3. Make a written forbidden path fatal even when refusal text is present; keep refusal-with-no-write
   passing without relying on an "empty dir" override.
4. Create each leg's fixtures independently of candidate success (no `out-empty/spans` assumption),
   so a do-nothing candidate yields leg failures, not a traceback.
5. Require a non-zero control denominator in the frozen command (pass `--controls` or fail on
   `DENIED=0/0`), and require a control to emit leg lines, not merely lack a `C1=PASS` tail.

## Artifacts, cleanup, disclosure

- Writes: scratch `/fast/scratch/hyaku/chousa-r59/R59Executor12/` only (probe scripts, `--work`
  dirs, logs), all removed before yield; this report is the only lane write.
- No install/update was performed (pacman intentionally not run). LSP was not used: the work is
  inspection and verbatim execution of a single dynamic Python script, not symbol resolution.
- Scratch path collision risk observed: peer `R59Executor12` shares the assigned scratch directory
  and my first run directories were removed mid-seat; receipts above are inline, not path-dependent.
- Risks: this report's assigned filename `.ufo/waves/round-59/w1/R59Executor12.md` may also be the
  peer executor's target; if so, the later write wins and both seats' findings should be merged by
  the integrator. Blockers: none for this seat's scope; the missing round-59 `claims.md` prevented
  testing any round-59-specific predicate.
