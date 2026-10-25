# MutSelftest — C1 self-test mutation probe (round 50, wave 1)

Attacked: `tools/assimilate-rows.py --selftest` (observe / selftest / fixtures_digest) at lane commit 6a068f2ae4847a1e4aa959f088a39ddc1b167bc0, working tree.
sha256 before = after = `bff32c11d02bc1bdc28ed484d4895d86c7f3537d8a9496ad474c73d4531f5b81` — the lane file was never modified; every mutant lived under `/dev/shm/chousa-r50-MutSelftest/` (deleted after the probe). No tools installed; pacman untouched.

## Method
- `mkdir -p /dev/shm/chousa-r50-MutSelftest && cp tools/assimilate-rows.py /dev/shm/chousa-r50-MutSelftest/pristine.py`
- Detector (identical for pristine, all mutants, restored): `python3 corpus/evidence/round50/c1-count.py --tool <tool>` — counter bounds each tool run at 120 s and the R49 leg at 600 s; observed ~1.9 s per run.
- One mutant per class: a single exact string replacement, applied to a fresh copy of pristine bytes; the harness asserted each old string occurs exactly once before writing.

## Pristine baseline (`--tool pristine.py` — a baseline failure would make every mutant inconclusive)
```
SELFTEST_DEFAULT=PASS (skipped: --tool)
BASELINE=PASS rc=0 findings=26
PERTURB_PASS=6/6
EXPECTED_BAD=PASS rc=2
R49_REGRESSION=PASS rc=0
LEGS=5/5
C1=PASS
```

## Mutation table (pristine.py line | old | new)
```python
("M1-collisions-dropped",        167, 'found.append("COLLISIONS " + (",".join(ids) if ids else "-"))', 'pass  # M1'),
("M2-map-action-dropped",        172, 'found.append(f"MAP {sid}->{lid} {act}")', 'found.append(f"MAP {sid}->{lid}")'),
("M3-stripped-never",            191, 'found.append(f"STRIPPED {lid} {col}")', 'pass  # M3'),
("M4-one-sided-diff",            220, 'miss, extra = sorted(set(want) - set(got)), sorted(set(got) - set(want))', 'miss, extra = sorted(set(want) - set(got)), []'),
("M5-digest-names-only",         200, 'h.update(p.relative_to(fix).as_posix().encode() + b"\\0" + p.read_bytes() + b"\\0")', 'h.update(p.relative_to(fix).as_posix().encode())'),
("M6-exit0-on-fail",             228, 'return 0 if ok else 1', 'return 0'),
("M7-exit0-unreadable-expected", 212, 'print(f"SELFTEST=ERROR expected file {exp}: {exc}")\n        return 2', 'same print\n        return 0'),
("M8-rowusedby-omitted",         180, 'found += [f"ROWSTATUS {lid} {cells[7]}", f"ROWUSEDBY {lid} {cells[10]}",', 'found += [f"ROWSTATUS {lid} {cells[7]}",'),
("M9-entrycites-staged",         183, 'q = out / e', 'q = know / e'),
("M10-toolexit-never",           162, 'found = [f"TOOLEXIT {r.returncode}"]', 'found = []'),
```

## Counter leg lines per mutant
Constant in all 11 runs: `SELFTEST_DEFAULT=PASS (skipped: --tool)`, `R49_REGRESSION=PASS rc=0` (checked `sort -u` across the ten logs); omitted below. Command per block: `python3 corpus/evidence/round50/c1-count.py --tool <M>.py`.
```
-- M1-collisions-dropped
BASELINE=FAIL rc=1 findings=?
PERTURB_PASS=6/6
EXPECTED_BAD=PASS rc=2
LEGS=4/5
C1=FAIL
-- M2-map-action-dropped
BASELINE=FAIL rc=1 findings=?
PERTURB_PASS=6/6
EXPECTED_BAD=PASS rc=2
LEGS=4/5
C1=FAIL
-- M3-stripped-never
BASELINE=FAIL rc=1 findings=?
PERTURB_PASS=6/6
EXPECTED_BAD=PASS rc=2
LEGS=4/5
C1=FAIL
-- M4-one-sided-diff
BASELINE=PASS rc=0 findings=26
PERTURB_PASS=4/6
EXPECTED_BAD=PASS rc=2
LEGS=4/5
C1=FAIL
P-fail: PERTURB P4 applied=1 rc=1 -> FAIL  (rc ok, but `DIFF unexpected TOOLEXIT 1` can no longer be printed)
P-fail: PERTURB P5 applied=1 rc=0 -> FAIL  (only an extra finding -> mutant prints SELFTEST=PASS rc=0, counter needs rc=1)
-- M5-digest-names-only
BASELINE=FAIL rc=0 findings=26
PERTURB_PASS=6/6
EXPECTED_BAD=PASS rc=2
LEGS=4/5
C1=FAIL
-- M6-exit0-on-fail
BASELINE=PASS rc=0 findings=26
PERTURB_PASS=0/6
EXPECTED_BAD=PASS rc=2
LEGS=4/5
C1=FAIL
P-fail: PERTURB P1 applied=1 rc=0 -> FAIL
P-fail: PERTURB P2 applied=1 rc=0 -> FAIL
(P3, P4, P5, P6 identical shape: applied=1 rc=0 -> FAIL)
-- M7-exit0-unreadable-expected
BASELINE=PASS rc=0 findings=26
PERTURB_PASS=6/6
EXPECTED_BAD=FAIL rc=0
LEGS=4/5
C1=FAIL
-- M8-rowusedby-omitted
BASELINE=FAIL rc=1 findings=?
PERTURB_PASS=5/6
EXPECTED_BAD=PASS rc=2
LEGS=3/5
C1=FAIL
P-fail: PERTURB P5 applied=1 rc=1 -> FAIL  (`DIFF unexpected ROWUSEDBY …` can never be emitted)
-- M9-entrycites-staged
BASELINE=FAIL rc=1 findings=?
PERTURB_PASS=6/6
EXPECTED_BAD=PASS rc=2
LEGS=4/5
C1=FAIL
-- M10-toolexit-never
BASELINE=FAIL rc=1 findings=?
PERTURB_PASS=5/6
EXPECTED_BAD=PASS rc=2
LEGS=3/5
C1=FAIL
P-fail: PERTURB P4 applied=1 rc=1 -> FAIL  (`DIFF unexpected TOOLEXIT 1` can never be emitted)
```

## Restoration evidence
- `cmp pristine.py restored.py` → byte-identical (restored.py = fresh copy of the lane tool taken after all runs).
- `sha256sum restored.py tools/assimilate-rows.py` → both `bff32c11d02bc1bdc28ed484d4895d86c7f3537d8a9496ad474c73d4531f5b81`.
- Detector on restored bytes: `LEGS=5/5`, `C1=PASS`.

## Kill matrix
| mutant | perturbation point | killing leg | verdict |
|---|---|---|---|
| M1 | observe: COLLISIONS dropped | BASELINE | killed |
| M2 | observe: MAP action dropped | BASELINE | killed |
| M3 | observe: STRIPPED never emitted | BASELINE | killed |
| M4 | selftest: one-sided set diff | PERTURB P4+P5 (unexpected side) | killed |
| M5 | fixtures_digest: names only | BASELINE (printed digest ≠ pin, rc still 0) | killed |
| M6 | selftest: exit 0 on FAIL | PERTURB 0/6 (all rc=0, counter needs 1) | killed |
| M7 | selftest: exit 0 on unreadable expected | EXPECTED_BAD (rc=0, needs 2) | killed |
| M8 | observe: ROWUSEDBY omitted | BASELINE (+P5 dead) | killed |
| M9 | observe: ENTRYCITES reads staged entry | BASELINE | killed |
| M10 | observe: TOOLEXIT never reported | BASELINE (+P4 dead) | killed |

10/10 killed, 0 SURVIVORS — no missing perturbation leg found on the tool side. The unexpected-side legs (P4/P5) are the only ones that distinguish two-sided from one-sided diffing (M4), and the digest pin catches a bytes-blind digest (M5); both held.

VERDICT: mutation-tested the frozen C1 self-test with 10 tool-side mutants — 10/10 killed, 0 survivors, pristine bytes restored and re-verified C1=PASS; gate coverage intact.
