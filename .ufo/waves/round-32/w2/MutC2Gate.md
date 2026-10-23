# MutC2Gate — round 32 attempt 2, W2 FALSIFY

## Scoped verdict

**HOLDS against the seven assigned C2 mutants:** the frozen v2 counter killed all seven. No mutant survived both detectors. **Selftest-only coverage finding:** case-insensitive and whitespace-collapsing U-hop readers both survived all 241 selftest cases. This is a detector-coverage result, not a claim that those behaviors satisfy the contract or an admission judgment.

Axes: **coverage** (U-hop audit semantics and detector sensitivity); **operability** (bounded, executable counter/selftest runs). No C1 mutation or C1 counter run was assigned or performed.

Read the frozen Design v2 at `corpus/evidence/round32/claims.md:119-189` before experimenting. Gate copied from checked-out revision `5d8a170795dcf48c3746a4f03dee9cfe32812834`; pristine/restored SHA-256:

`10f2fe12043c6f1565c7d7b9446ee0c4dc11e9649aa3350dcab96f8a2ccb4098`

Committed counter was executed unmodified from `corpus/evidence/round32/c2-count-v2.py`, SHA-256 `8ec1a1ed44f1d3971a73eeace677cbedd0187563bea063ec6b680261dbb23c8a` (for example, `MutC2Gate/a-mutated-run.json:4-6`). All evidence links below are relative to this report's directory.

## Mutants, expected detectors, actual results

Each mutant was independent, in `/fast/scratch/hyaku/chousa-r32/w2/MutC2Gate/mutant-<letter>/tools/research-gate.sh`. Each used one seed, unchanged across its pristine/mutated/restored runs. Every mutated counter exited **1**; the count column is its actual `EXEMPT_AUDIT_MATCH` output.

| Mutant | Seed | Count | Selftest verdict | Expected detector; actual killed-by |
|---|---:|---:|---|---|
| (a) Lowercase source and anchor only for U hops before anchor matching | 3232101 | 126/132 | PASS, 241 cases, exit 0 | Counter E11: 0/6; **counter only** |
| (b) Collapse horizontal whitespace in source and anchor only for U hops | 3232102 | 126/132 | PASS, 241 cases, exit 0 | Counter E12: 0/6; **counter only** |
| (c) Bypass the canonical containment refusal for U hops, retaining other source checks | 3232103 | 126/132 | FAIL, 1/241, exit 1 | Counter E7: 0/6; **both**, selftest `chain-exempt-unresolvable` |
| (d) Include rejected/not-applicable in the audited arm | 3232104 | 120/132 | FAIL, 1/241, exit 1 | Counter E5: 0/12; **both**, selftest `chain-exempt-judgment` |
| (e) Emit the resolvable finding twice | 3232105 | 96/132 | FAIL, 2/241, exit 1 | Counter R1–R3: 0/36; **both**, selftest `chain-exempt-resolvable` and `chain-exempt-mixed` |
| (f) Emit CHAIN_EXEMPT_RESOLVABLE without incrementing drift or setting DRIFT | 3232106 | 0/132 | FAIL, 2/241, exit 1 | Counter record checks: gate exit 0, no DRIFT summary; **both**, same two selftest cases |
| (g) Move blocked-no-fetch from the audit arm to the exempt/unread arm | 3232107 | 120/132 | FAIL, 1/241, exit 1 | Counter R1–R3: 8/12 each; **both**, selftest `chain-exempt-resolvable` |

Mutation points on pristine gate bytes: (a,b) `chain_probe:1850`; (c) `claim_source_path:1240-1250`, called by `chain_probe:1841`; (d) `verify_chain:1944`; (e) `verify_chain:1953-1954`; (f) `emit_finding:447`; (g) `verify_chain:1944,1961`. Complete applied diffs and full mutant hashes are in [mutations.json](MutC2Gate/mutations.json), lines 2-42. The matching rules remained unchanged in resolved hops for (a,b), so their passing selftests were not obtained by changing display text or resolved-arm semantics.

Per-mutant actual commands, exit codes, key output, elapsed time and output paths:
[a](MutC2Gate/a-mutated-run.json), [b](MutC2Gate/b-mutated-run.json), [c](MutC2Gate/c-mutated-run.json), [d](MutC2Gate/d-mutated-run.json), [e](MutC2Gate/e-mutated-run.json), [f](MutC2Gate/f-mutated-run.json), [g](MutC2Gate/g-mutated-run.json).

Raw counter receipts with class totals and every missed hop:
[a](MutC2Gate/a-mutated.json), [b](MutC2Gate/b-mutated.json), [c](MutC2Gate/c-mutated.json), [d](MutC2Gate/d-mutated.json), [e](MutC2Gate/e-mutated.json), [f](MutC2Gate/f-mutated.json), [g](MutC2Gate/g-mutated.json).

The corresponding `*-mutated-selftest.txt` files retain complete selftest stdout/stderr, including the failing case outputs. [case-summary.json](MutC2Gate/case-summary.json) aggregates every valid three-phase run without omitting failures.

## Pristine and restored controls — every run disclosed

For **each** row a–g, both its pristine and restored counter printed `EXEMPT_AUDIT_MATCH=132/132`, `RECORD_CHECKS=ok`, exit **0**. Both selftests printed `RESEARCH_GATE_SELFTEST: PASS (241 cases, 0 skipped)`, exit **0**. Receipts:

| Case / seed | Pristine command/output record | Restored command/output record |
|---|---|---|
| a / 3232101 | [a-pristine-run.json](MutC2Gate/a-pristine-run.json) | [a-restored-run.json](MutC2Gate/a-restored-run.json) |
| b / 3232102 | [b-pristine-run.json](MutC2Gate/b-pristine-run.json) | [b-restored-run.json](MutC2Gate/b-restored-run.json) |
| c / 3232103 | [c-pristine-run.json](MutC2Gate/c-pristine-run.json) | [c-restored-run.json](MutC2Gate/c-restored-run.json) |
| d / 3232104 | [d-pristine-run.json](MutC2Gate/d-pristine-run.json) | [d-restored-run.json](MutC2Gate/d-restored-run.json) |
| e / 3232105 | [e-pristine-run.json](MutC2Gate/e-pristine-run.json) | [e-restored-run.json](MutC2Gate/e-restored-run.json) |
| f / 3232106 | [f-pristine-run.json](MutC2Gate/f-pristine-run.json) | [f-restored-run.json](MutC2Gate/f-restored-run.json) |
| g / 3232107 | [g-pristine-run.json](MutC2Gate/g-pristine-run.json) | [g-restored-run.json](MutC2Gate/g-restored-run.json) |

**Additional initial run, not hidden:** seed 3232001 on pristine gate bytes printed 132/132, counter exit 0, but selftest exited **153** during its large-file fixture creation. Evidence: [pristine-run.json](MutC2Gate/pristine-run.json):6-29 and [pristine-selftest.txt](MutC2Gate/pristine-selftest.txt):95-96 (`File size limit exceeded`). My initial harness applied a 1,048,575-byte RLIMIT_FSIZE to all child writes, smaller than the selftest's 8 MiB source fixture. This initial selftest result is **INCONCLUSIVE**, never a killed mutant. I changed only the harness limit to 16 MiB, disabled core dumps, and separately capped retained output below 1 MiB; all seven subsequent pristine/mutated/restored sequences used that same revised harness. Configuration is recorded in [controls.json](MutC2Gate/controls.json); revised runner source is [detector-runner.txt](MutC2Gate/detector-runner.txt).

Total: **22 counter executions** — 15 pristine/restored-byte runs, all 132/132, plus seven explicitly labelled mutant/control runs below target. No unmodified landed-gate-byte run scored below target.

## Commands and containment

For each letter `m` and phase `p` in `pristine`, `mutated`, `restored`, the recorded command shape was:

```sh
timeout --signal=TERM --kill-after=5s 700s python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round32/c2-count-v2.py --gate /fast/scratch/hyaku/chousa-r32/w2/MutC2Gate/mutant-$m/tools/research-gate.sh --seed SEED --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32/w2/MutC2Gate/$m-$p.json
timeout --signal=TERM --kill-after=5s 900s bash /fast/scratch/hyaku/chousa-r32/w2/MutC2Gate/mutant-$m/tools/research-gate.sh --selftest
```

Exact expanded invocations are in each `*-run.json`; these command shapes are explanatory, not additional runs. Cwd was that mutant's scratch lane root. The harness removed all CHOUSA_* variables and GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE, and set C1_TMP/C2_TMP/TMPDIR to `/fast/scratch/hyaku/chousa-r32/w2/MutC2Gate/tmp/<run-label>`, outside every gate lane root. Up to four independent foreground runner calls were joined concurrently; no background jobs or subagents were used. Each detector process group was killed after collection to prevent lingering descendants.

Before copying, `timeout 10s df -h /fast` exited 0 and showed 220G available. Retained output was bounded below 1 MiB per artifact; observed maximum artifact size was 18,133 bytes. Final `timeout 10s ps -eo pid=,ppid=,pgid=,args=` exited 0 with **zero experiment-path processes**; receipt in [controls.json](MutC2Gate/controls.json). No installations, network calls, production gate/corpus changes, lane index writes or lane jj writes were performed by this seat.

## Restoration evidence and limits

Every mutant was restored by whole-file replacement with the exact saved pristine bytes, including if its detector failed. [restoration.json](MutC2Gate/restoration.json):2-42 records, for each letter, the full before/mutant/restored SHA-256 and `exact_bytes: true`; all restored hashes equal the full landed hash above. Restored detector records additionally contain that hash before and after execution.

Limits: seven specified defects, one seed per mutant, finite fixtures; no claim of universal correctness. The real reproducible finding is that **selftest alone misses (a) and (b)**. The frozen C2 v2 counter catches both, so **no assigned mutant is missed by both detectors**. Production repairs, contract changes, integration and admission were outside this probe.
