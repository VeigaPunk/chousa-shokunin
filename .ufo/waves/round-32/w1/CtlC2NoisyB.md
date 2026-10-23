# CtlC2NoisyB — C2 noisy controls

## Axes and scope

**Coverage:** correct U-hop classifications, findings, and finding multiplicity. **Operability:** non-resolvable U hops must remain exempt without diagnostic noise. This is control evidence, not candidate admission or a canonical judgment.

Read first: `corpus/evidence/round32/claims.md`, then both frozen counter docstrings. No production file, counter, Git index, jj state, or sibling lane was changed. All experiments were scratch BASE-gate copies; no C1/C2 candidate was scored. No network, installs, gate selftest, or unrelated checks.

Path aliases below:
- `S=/fast/scratch/hyaku/chousa-r32/w1/CtlC2NoisyB`
- `A=.ufo/waves/round-32/w1/CtlC2NoisyB` (lane-relative)
- Lane: `/home/vgpnk/Projects/shokunin/chousa-shokunin`

## Strongest counterexample

**The duplicate-only real-reader control prints two findings per resolvable U hop, yet the frozen counter scores 120/120 on two fresh seeds.** It violates the exactly-one condition in `corpus/evidence/round32/claims.md:63-65`.

Receipts:
- `A/bounded-disjoint-duplicate-only-s5239036554333767031.json:3-14` — counter exit 0, gate exit 1, 120/120, predicate_holds=true.
- `A/bounded-disjoint-duplicate-only-s6022806861474399502.json:3-14` — same.

Separate raw audits on the two retained fixtures both exited 1, with no stderr. Each produced 120 CHAIN lines (36 resolvable, 12 verified, 72 exempt) and **72 CHAIN_EXEMPT_RESOLVABLE findings for 36 distinct hops, exactly two per hop**. Audit commands, counts, and SHA-256 values are in `A/duplicate-audit.json`.

Concrete evidence: `A/duplicate-audit-s5239036554333767031.stdout:2,122-123`:

```text
CHAIN hop=h1969d43f status=unresolved observed=resolvable source=f85a4e2300f.md anchor=heading:"semofa perimo" at=line:3 verdict=mismatch
FINDING CHAIN_EXEMPT_RESOLVABLE severity=warn surface=chain obs=hop=h1969d43f status=unresolved citation verifies as resolved
FINDING CHAIN_EXEMPT_RESOLVABLE severity=warn surface=chain obs=hop=h1969d43f status=unresolved citation verifies as resolved
```

Second independent fixture: `A/duplicate-audit-s6022806861474399502.stdout:5,122-123`, hop `h06fde3d0`, status labelled-dead, likewise two identical findings. Both raw outputs end at lines 194-195 with `RESOLVED_HOPS=12/120` and DRIFT, findings=72, drift=72.

**Why it passes:** `corpus/evidence/round32/c2-count.py:273` stores finding IDs in a set. Lines 284-286 compare that set with `{CHAIN_EXEMPT_RESOLVABLE}`. Two identical findings collapse to one ID. CHAIN-line duplication is checked at lines 276-280, but finding multiplicity is not. The docstring's set rule at lines 32-34 is weaker than its exactly-one contract at lines 21-23. No counter was patched.

## Control construction and identity

Base hash command, exit 0:

```text
timeout 15s sha256sum tools/research-gate.sh corpus/evidence/round32/c1-count.py corpus/evidence/round32/c2-count.py
```

Observed hashes:
- BASE gate: `0bc318b3e74ac0ad45f4b34154e886d84aebf44673612afab6de5e0b0ff11258`
- C1 counter: `9e787e80b215f6522335c639d5e1b2e60d0a5812b83a9760daf8be9f78415885`
- C2 counter: `b6626b2cb81b2aeaf66a8ff11a06c030612bf4e264dc128f290021c4aa71f54c`

`timeout 15s git show 4111607c857bc29ff31883bc095ae00afb527e50:corpus/evidence/round32/c2-count.py | sha256sum` also returned the C2 hash above. Read-only Git only.

Each control was copied from BASE. The original resolved evaluator (`tools/research-gate.sh:1829-1878`) remains verbatim inside a one-iteration loop, containing its early `continue` statements. Its dispatch also accepts U statuses; postprocessing applies only to U. Rejected/not-applicable retain the original unread arm. The controls differ only in postprocessing and necessary bookkeeping:

| Control | Behavior | SHA-256 |
|---|---|---|
| noisy-findings | Verified → resolvable + one finding; every other result → exempt, retaining all original resolved-arm findings | `147900f09f8e39f02265576955d1622b15d18256ca73b69ebe139df1a35a873f` |
| noisy-observed | Same reader; failed U outcomes retain anchor-missing/refused/invalid observations and original findings | `0389f0b341be1609da5d9b2457c3b63f012fab7068fb6d44a0a1adc6e0b68f60` |
| noisy-duplicate | noisy-findings plus a second identical resolvability finding | `4db1cd8cd58bd6cda320a39cea0d1a7b6218a3d28e85c17a92b855d1c8b6444e` |
| duplicate-only | Isolates multiplicity: discard resolved-arm failure findings/state for U, keep failed U exempt, emit the resolvability finding twice | `30225fadc5974f0f3069ed0a9e871bc1d2957f7a33a5d4eac6d1c49b2c9b0c5d` |

Final gate paths are `S/gates/<control>/tools/research-gate.sh`; sizes 307429–308277 bytes. Hashes, sizes, exact argv vectors, receipt paths, and timing are in `A/bounded-disjoint-runs.json`. Duplicate calls are at `S/gates/duplicate-only/tools/research-gate.sh:1895-1896`.

## Scored trials — disjoint allowed roots

All scoring used the unchanged committed counter, lane cwd, and C1_TMP/C2_TMP/TMPDIR set to S. Gate-derived LANE_ROOT is `S/gates/<control>`, disjoint from the fixture tree. Two concurrent foreground scoring workers; all children awaited. Limits: timeout 700 seconds, kill-after 10 seconds, address space 2 GiB, nproc 8192, file size 1 MiB. All eight successful scoring invocations had empty stderr, gate_rc=1, gate_timed_out=false.

One exact command (exit 0; environment/cwd recorded above):

```text
timeout --signal=TERM --kill-after=10s 700s prlimit --as=2147483648 --nproc=8192 --fsize=1048576 -- python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round32/c2-count.py --gate /fast/scratch/hyaku/chousa-r32/w1/CtlC2NoisyB/gates/duplicate-only/tools/research-gate.sh --seed 5239036554333767031 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32/w1/CtlC2NoisyB/bounded-disjoint-duplicate-only-s5239036554333767031.json --keep /fast/scratch/hyaku/chousa-r32/w1/CtlC2NoisyB/fixture-bounded-disjoint-duplicate-only-s5239036554333767031
```

For each row below, receipt is `A/bounded-disjoint-<control>-s<seed>.json`; the adjacent `.log` contains the full actual command at line 3, exit at line 4, count at line 6, and every per-class output line at lines 7-20.

| Control | Trial | Fresh seed | Counter exit | Count | Target-count verdict |
|---|---:|---:|---:|---|---|
| noisy-findings | 1 | 2871693562036699951 | 1 | 60/120 | MISSES |
| noisy-findings | 2 | 9154681397938830412 | 1 | 60/120 | MISSES |
| noisy-observed | 1 | 7979547634130007614 | 1 | 60/120 | MISSES |
| noisy-observed | 2 | 4292539536881331703 | 1 | 60/120 | MISSES |
| noisy-duplicate | 1 | 4968697293548520812 | 1 | 60/120 | MISSES |
| noisy-duplicate | 2 | 8742748046569772371 | 1 | 60/120 | MISSES |
| duplicate-only | 1 | 5239036554333767031 | 0 | 120/120 | MEETS-TARGET |
| duplicate-only | 2 | 6022806861474399502 | 0 | 120/120 | MEETS-TARGET |

MEETS-TARGET here describes the frozen counter's target count in the stated control configuration, **not** an assertion that a landed revision satisfies P2, its no-lower-run requirement, or the prose contract.

### Per-class lines

Each entry applies separately to both trials of that control. Exact uncollapsed output is retained in each `.log`; C2 emits per-class lines, not C1-style individual trial lines.

| Class | noisy-findings | noisy-observed | noisy-duplicate | duplicate-only |
|---|---:|---:|---:|---:|
| R1_U_fragment_quote | 12/12 | 12/12 | 12/12 | 12/12 |
| R2_U_path_anchor_cols | 12/12 | 12/12 | 12/12 | 12/12 |
| R3_U_declared_id | 12/12 | 12/12 | 12/12 | 12/12 |
| F1_resolved_verifiable | 12/12 | 12/12 | 12/12 | 12/12 |
| E1_U_anchor_absent | 0/12 | 0/12 | 0/12 | 12/12 |
| E2_U_missing_file | 0/6 | 0/6 | 0/6 | 6/6 |
| E3_U_external_url | 0/6 | 0/6 | 0/6 | 6/6 |
| E4_U_no_citation | 0/6 | 0/6 | 0/6 | 6/6 |
| E5_J_resolvable | 12/12 | 12/12 | 12/12 | 12/12 |
| E6_U_undeclared_id | 0/6 | 0/6 | 0/6 | 6/6 |
| E7_U_out_of_corpus | 0/6 | 0/6 | 0/6 | 6/6 |
| E8_U_quote_glued | 0/6 | 0/6 | 0/6 | 6/6 |
| E9_U_heading_as_plain_line | 0/6 | 0/6 | 0/6 | 6/6 |
| E10_U_line_partial | 0/6 | 0/6 | 0/6 | 6/6 |

Examples explaining the noisy misses:
- `A/bounded-disjoint-noisy-findings-s2871693562036699951.json:32-36`: truth exempt, observed `exempt+findings=CHAIN_ANCHOR_NOT_FOUND`.
- `A/bounded-disjoint-noisy-observed-s7979547634130007614.json:32-36`: truth exempt, observed anchor-missing.
- Combined noisy-duplicate still matches every R1–R3 hop despite doubling its finding; its unrelated noise supplies the 60 failures. The isolated duplicate-only control removes that masking defect.

## Earlier attempts retained, not hidden

### Flat-gate geometry

Initial gates were `S/<control>.sh`, with C2_TMP=S. BASE derives LANE_ROOT from the gate's parent directory (`tools/research-gate.sh:287-291`) and allows both ROOT and LANE_ROOT (`:1186-1222`). That layout made the generated E7 `../outside` files fall inside the relocated LANE_ROOT. The counter generator labels E7 exempt unconditionally (`corpus/evidence/round32/c2-count.py:208-210`). The control's own full resolved evaluator consequently found these six citations resolvable.

All initial receipts/logs remain in A, indexed by `A/runs.json`. Counts:

| Flat control | Seeds | Counts, counter exits |
|---|---|---|
| noisy-findings | 6422185893591383400; 2626605178957809124 | 60/120 each, exit 1 |
| noisy-observed | 6670895969077106734; 7277747829333055323 | 60/120 each, exit 1 |
| noisy-duplicate | 434026363343337342; 6791658236543462606 | 60/120 each, exit 1 |
| duplicate-only | 2900585060432225386; 4221803085486873511 | 114/120 each, exit 1 |

Per-class/per-trial lines are in `A/<control>-s<seed>.log:6-20`. The first three have the same class counts as their disjoint trials. Flat duplicate-only matches all classes except E7 0/6; its receipt `A/duplicate-only-s2900585060432225386.json:31-67` identifies all six as observed=resolvable. This is a boundary-context confound, not a counter fix or a discarded valid P2 candidate miss. Gate contents and hashes were unchanged by relocation; both contexts are disclosed.

### Process-limit failures

Eight disjoint-layout attempts under nproc=2000 exited 1 with no score and no receipt: Python Popen raised `BlockingIOError: [Errno 11] Resource temporarily unavailable` before starting the gate. Commands, seeds, and complete stderr are indexed in `A/disjoint-runs.json`; example `A/disjoint-noisy-findings-s2941157572406731558.log:3-37`. [INFERENCE] The shared-UID fleet load exceeded that low limit. Raising the still-finite nproc cap to 8192 and reducing concurrency to two produced the eight scored trials above. The counter does not catch this OSError as a harness exit 2; it was not patched or interpreted as a scored semantic miss.

The attempted diagnostic `timeout 15s ps -u vgpnk -L --no-headers -o lwp= | wc -l` printed `ps: unsupported option '-L'`; its pipeline printed 0, **not** a valid process count. `timeout 15s df -h /fast` succeeded before fixtures: 236G available, 71% used. Fixtures/logs were bounded; no installs or services were started.

## Impact and smallest safe correction

1. **Noisy failure diagnostics / raw failure observations:** actual coverage and operability defects, caught at 60/120. Keep non-resolvable U hops observed=exempt with no finding naming the hop; do not leak the ordinary resolved-arm failure diagnostics. This is not an acceptable axis tradeoff under the stated contract.
2. **Finding multiplicity:** a fixable counter defect. For a future authorized pre-data design, retain per-hop finding occurrences rather than a set, and require exactly one correctly identified finding for resolvable truth, zero otherwise. Keep the committed counter unchanged in this wave; route this result through the L1's frozen-design/kill-rule process (`claims.md:99-103`), not a silent predicate reinterpretation. A 120/120 receipt alone does not establish the prose exactly-one requirement.
3. **Scratch identity:** keep each gate-derived LANE_ROOT disjoint from C2_TMP/kept fixtures; do not infer identical source boundaries from identical gate hashes after relocation.

Limits: only the scoped controls and two raw duplicate audits were exercised. No claim about candidate behavior, no-harm results, C1, or round-31 repairs. Canonical judgment/admission remains outside this review.
