# C2 v2 counter-of-counter — MutCounterC2v2

Axes: **operability** (bounded execution, exact restoration); **coverage** (reject the named defective controls).

**Verdict: HOLDS for the scoped negative-control discrimination.** Reverting findings multiplicity, record-check enforcement, or E11/E12 makes the matching defective controls pass; restoring the counter rejects them again. All three counter mutants are **KILLED by the negative-control-rejection detector**. The layout mutant is **KILLED by a focused refusal detector**, but **SURVIVES the legal-layout oracle detector**. Its effect on an actual invalid-layout gate score is **INCONCLUSIVE**, because the assignment requires all temporary-directory environment variables outside each scratch gate's lane root. No landed-candidate execution or claim-wide verdict is supplied here.

## Probe and expected detector

Read the frozen `corpus/evidence/round32/claims.md:119-189`, particularly its four changes at lines 163–169. Used four separate scratch copies of the committed counter, initially SHA-256 `8ec1a1ed44f1d3971a73eeace677cbedd0187563bea063ec6b680261dbb23c8a`.

Scratch: `/fast/scratch/hyaku/chousa-r32/w2/MutCounterC2v2/`. All evidence links below are relative to `.ufo/waves/round-32/w2/MutCounterC2v2/`.

The detector for counter mutations is **rejection of a known-defective control**, not acceptance of that control as a candidate. Expected: counter exit 1 and `predicate_holds=false` on pristine/restored bytes; an erroneous full score on mutated bytes fails this detector. Thus the pristine rejection is a successful meta-detector baseline, not a failed gate baseline being mislabeled killed. The oracle's separate expected behavior is 132/132 with exit 0.

Two fresh seeds, **32321023 and 32321024**, were identical in result throughout. Ran **42 counter invocations**: seven control/counter pairs × two seeds × pristine/mutated/restored. Also ran three focused layout-refusal invocations. Every score, including every below-target control score, is preserved in `runs.json`; per-run `<mutant>-<control>-<phase>-s<seed>.output.json` contains the exact command, environment, exit code, stdout, stderr, hashes and corresponding receipt path. None of these controls or mutants is a candidate.

All full scores used this actual command shape, at most two foreground invocations concurrently:

```text
C1_TMP=/fast/scratch/hyaku/chousa-r32/w2/MutCounterC2v2/tmp C2_TMP=/fast/scratch/hyaku/chousa-r32/w2/MutCounterC2v2/tmp TMPDIR=/fast/scratch/hyaku/chousa-r32/w2/MutCounterC2v2/tmp timeout --kill-after=5s 660s prlimit --as=1073741824 --nproc=8000 -- python3 /fast/scratch/hyaku/chousa-r32/w2/MutCounterC2v2/counters/<mutant>/c2-count-v2.py --gate /fast/scratch/hyaku/chousa-r32/w2/MutCounterC2v2/gates/<control>/tools/research-gate.sh --seed <seed> --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32/w2/MutCounterC2v2/<mutant>-<control>-<phase>-s<seed>.json
```

## Actual results

Each cell below holds on **both seeds**. Counts are the printed `EXEMPT_AUDIT_MATCH`; parentheses are actual counter exit codes.

| Counter mutation | Matching control | Pristine | Mutated | Restored | Rejection-detector verdict |
|---|---|---|---|---|---|
| `got = sorted(set(named.get(hid, [])))` at original counter line 342 | Frozen duplicate-only gate | 96/132 (1) | 132/132 (0) | 96/132 (1) | KILLED |
| `record_ok = True` at line 337 | CLEAN + exit 0 | 0/132 (1) | 132/132 (0) | 0/132 (1) | KILLED |
| Same isolated record-check mutation | No verdict summary | 0/132 (1) | 132/132 (0) | 0/132 (1) | KILLED |
| Same isolated record-check mutation | Finding on unknown hop | 0/132 (1) | 132/132 (0) | 0/132 (1) | KILLED |
| Remove E11/E12 rows at lines 94–95; restore old `TOTAL = 120` at line 74 | Case-insensitive reader | 126/132 (1) | 120/120 (0) | 126/132 (1) | KILLED |
| Same isolated negative-class mutation | Whitespace-collapsing reader | 126/132 (1) | 120/120 (0) | 126/132 (1) | KILLED |
| Bypass layout guard at line 292 | Feasibility oracle, legal disjoint layout | 132/132 (0) | 132/132 (0) | 132/132 (0) | SURVIVED this detector |

The 120/120 scores are **mutant-counter outputs only**, not P2 v2 successes or an amended target. Findings-set misses on pristine/restored are exactly R1/R2/R3, each 0/12. Case-reader misses are exactly E11 0/6; whitespace-reader misses exactly E12 0/6 (`miss-signatures.json`). Record failures remain reported even when their enforcement is mutated off: CLEAN yields `gate-rc=0,drift-summary-lines=0`; no-verdict yields `drift-summary-lines=0`; stray-unknown yields `stray-finding-hops=1`. Every other table row prints `RECORD_CHECKS=ok`. These outputs establish why each negative control is rejected, rather than relying only on a low aggregate score.

`meta-detector-results.json` records the PASS/FAIL/PASS rejection expectations for all six negative-control pairs, and PASS/PASS/PASS for the legal-layout oracle.

## Control provenance

- Duplicate-only: exact copy of `.ufo/waves/round-32/controls/L1-design-v2/c2-dup-control-gate.sh`, SHA-256 `30225fadc5974f0f3069ed0a9e871bc1d2957f7a33a5d4eac6d1c49b2c9b0c5d`; duplicate emissions are at its lines 1895–1896.
- WeakReader scratch originals had already been restored to base. Rebuilt **only this seat's copies** from `.ufo/waves/round-32/w1/CtlC2WeakReaderB/{case-insensitive,whitespace-collapse}.patch`. Rebuilt hashes exactly match that seat's `v2-rescore.md:13-14`: case `a0eab06c1546516a21ce54003271742d1b20b742bb319f06939c3a35b4700d06`, whitespace `32e03f4f5ccae47fa613efad47b75ee167b4aef03bc61e807213428dda8e8c5d`.
- Record-output controls copied from the paths disclosed in `.ufo/waves/round-32/w1/MutC2CounterB/v2/source-gates.json`. Copied its `emit-control-v2.py` unchanged, relocated only the helper/truth paths in this seat's gate copies, and generated a private truth payload from the unchanged v2 generator for the two fresh seeds. These are explicitly **truth-fed output-parser controls, not citation readers** (`emit-control-v2.py:8-17,33-38`). No sibling payload or source was changed.
- Legal-layout oracle: exact `c2-oracle-gate.sh` copy, hash `1e3d02fef62e3d434a931313a26e7cb5015b672521769bd0fc2e2fe54e1bda26`.

`setup.json` preserves source/target paths and all source, scored and restoration hashes. The exact scored control bytes are retained in `controls/`; the private helper and truth payload are also retained.

## Layout guard: bounded focused detector and limit

The scratch-layout contract precludes actually putting the fixture under a gate's lane root. Instead, `layout-probe.py` supplies a **synthetic path only** to the counter's existing temp-allocation dependency, observes whether fixture generation is reached, and creates no in-lane files. Its expected detector is: exit 2 with the layout-refusal diagnostic **before** generation. Generation is an observation hook that raises `LAYOUT_PROBE_REACHED_GENERATE`, not a gate or scoring oracle.

Actual command for each phase (same paths and arguments):

```text
timeout --kill-after=2s 20s prlimit --as=1073741824 --nproc=8000 -- python3 /fast/scratch/hyaku/chousa-r32/w2/MutCounterC2v2/layout-probe.py /fast/scratch/hyaku/chousa-r32/w2/MutCounterC2v2/counters/layout-off/c2-count-v2.py /fast/scratch/hyaku/chousa-r32/w2/MutCounterC2v2/gates/oracle/tools/research-gate.sh
```

Actual detector exits: **0 / 1 / 0**; `generate_reached`: **false / true / false**. Pristine/restored print the inside-lane refusal; mutant prints the fixture-generation hook exception. Counter-main exit is 2 in all three, so exit code alone would not distinguish them. Evidence: `layout-guard-{pristine,mutated,restored}.output.json`. This establishes load-bearing refusal control flow, **not** an end-to-end wrong gate score under invalid layout. The legal-layout oracle legitimately cannot kill this mutation; its SURVIVED result is not permission to change the contract.

## Exact restoration and scope

All counter mutations were restored in `finally` by replacing the entire file with the original bytes, before restored runs. `mutation-evidence.json` preserves exact diffs and these hashes:

| Counter copy | Mutated SHA-256 |
|---|---|
| findings-set | `da6588d90ff49b9958828844c89be1f5424628e3cfcb3c5882736041a235a25e` |
| record-off | `b6d830ac0e0b9880f76feea222ccb117e21f93795204a9573f20732a7514a944` |
| layout-off | `feceaaddf18363fc85c5dae71498e07ce90ed21fbd3f052d935abd0175302fe0` |
| negatives-off | `ca618b3d1e3f44c82283987c673fea07acfce66022c5a7a99515216745ca0fc5` |

**Before and restored SHA-256 for every counter:** `8ec1a1ed44f1d3971a73eeace677cbedd0187563bea063ec6b680261dbb23c8a`; exact byte comparisons were true for all four. All five gate copies modified for control reconstruction/relocation were likewise restored byte-for-byte to their copied inputs after preserving scored snapshots. Duplicate-only and oracle gate bytes were never edited.

The production counter's start/end hash remained `8ec1a1ed…b23c8a`. The read-only command `timeout 30s sha256sum corpus/evidence/round32/c2-count-v2.py tools/research-gate.sh` exited 0 at both observations; the **production gate changed** from `10f2fe12…b4098` to `d13a76e3…3edd7` during this probe (`lane-hash-observations.json`). [INFERENCE] This was external to this seat: it performed no production writes and never executed the production gate. All experimental gate inputs were isolated control copies, so this does not alter the reported probes.

No installs, network, Git/JJ writes, subagents, persistent jobs, or production edits. Counter process groups were awaited/reaped and then killed if still present; layout detectors spawn no child gate. The private temp directory was empty after completion. The artifact size observation before the final two small JSON records was 101 files, maximum 308,277 bytes; all evidence files remain below 1 MiB. No candidate-wide falsification, repairs, or integration is claimed.
