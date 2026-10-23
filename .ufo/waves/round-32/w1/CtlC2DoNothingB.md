# CtlC2DoNothingB — C2 do-nothing control

## Scope, axes, result

- **Axes:** coverage (whether locally resolvable exempt hops are audited), operability (the control and frozen counter complete and produce receipts). C1 append serialization was not exercised.
- **Control:** an unmodified scratch copy of the base `tools/research-gate.sh`; no patch, candidate implementation, counter modification, or feasibility oracle.
- **Control verdict: MISSES** on all three newly selected seeds: **84/120**, not the frozen **120/120** target (`corpus/evidence/round32/claims.md:60-79`). This is counter evidence only, not a canonical runtime judgment or admission decision.
- Every invocation returned counter exit **1**, with receipt `gate_rc=0`, `gate_timed_out=false`, `predicate_holds=false`. All 36 positive exempt-hop cases failed; all remaining 84 cases matched.

## Provenance and preparation

Read first: `corpus/evidence/round32/claims.md`, then both frozen counter docstrings. Read the godspeed skill and operator rules. No tool installation or update was needed.

Working directory for commands: `/home/vgpnk/Projects/shokunin/chousa-shokunin` (the disk preflight used the fleet root).

Executed commands, each exit **0**:

```sh
timeout 30s df -h /fast
```

Output: `/dev/nvme1n1p2 804G 568G 236G 71% /fast`.

```sh
timeout 30s mkdir -p /fast/scratch/hyaku/chousa-r32/w1/CtlC2DoNothingB /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32/w1/CtlC2DoNothingB && timeout 30s cp /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh /fast/scratch/hyaku/chousa-r32/w1/CtlC2DoNothingB/base-gate.sh && timeout 30s sha256sum /fast/scratch/hyaku/chousa-r32/w1/CtlC2DoNothingB/base-gate.sh /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round32/c2-count.py

timeout 30s env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /home/vgpnk/Projects/shokunin/chousa-shokunin show 4111607c857bc29ff31883bc095ae00afb527e50:corpus/evidence/round32/c2-count.py | sha256sum
```

Hashes observed:

- Scratch gate and lane gate: `0bc318b3e74ac0ad45f4b34154e886d84aebf44673612afab6de5e0b0ff11258`, identical to the frozen base hash (`claims.md:3-4`). Scratch gate: `/fast/scratch/hyaku/chousa-r32/w1/CtlC2DoNothingB/base-gate.sh`.
- Current counter and counter read from frozen commit `4111607c857bc29ff31883bc095ae00afb527e50`: `b6626b2cb81b2aeaf66a8ff11a06c030612bf4e264dc128f290021c4aa71f54c`.
- Each receipt records both hashes at lines 3-5.

## Counter commands and receipts

The following independent commands ran concurrently, in the lane cwd, with no background jobs. Each exited **1**. Limits: 55-second foreground timeout, 2 GiB address space, 2,000 processes, and a 1,048,575-byte per-file write ceiling. All three temporary-directory variables pointed inside this seat's scratch directory.

```sh
timeout 55s env C1_TMP=/fast/scratch/hyaku/chousa-r32/w1/CtlC2DoNothingB C2_TMP=/fast/scratch/hyaku/chousa-r32/w1/CtlC2DoNothingB TMPDIR=/fast/scratch/hyaku/chousa-r32/w1/CtlC2DoNothingB prlimit --nproc=2000 --as=2147483648 --fsize=1048575 -- python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round32/c2-count.py --gate /fast/scratch/hyaku/chousa-r32/w1/CtlC2DoNothingB/base-gate.sh --seed 32023271 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32/w1/CtlC2DoNothingB/base-s32023271.json --keep /fast/scratch/hyaku/chousa-r32/w1/CtlC2DoNothingB/fixture-s32023271

timeout 55s env C1_TMP=/fast/scratch/hyaku/chousa-r32/w1/CtlC2DoNothingB C2_TMP=/fast/scratch/hyaku/chousa-r32/w1/CtlC2DoNothingB TMPDIR=/fast/scratch/hyaku/chousa-r32/w1/CtlC2DoNothingB prlimit --nproc=2000 --as=2147483648 --fsize=1048575 -- python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round32/c2-count.py --gate /fast/scratch/hyaku/chousa-r32/w1/CtlC2DoNothingB/base-gate.sh --seed 32023273 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32/w1/CtlC2DoNothingB/base-s32023273.json

timeout 55s env C1_TMP=/fast/scratch/hyaku/chousa-r32/w1/CtlC2DoNothingB C2_TMP=/fast/scratch/hyaku/chousa-r32/w1/CtlC2DoNothingB TMPDIR=/fast/scratch/hyaku/chousa-r32/w1/CtlC2DoNothingB prlimit --nproc=2000 --as=2147483648 --fsize=1048575 -- python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round32/c2-count.py --gate /fast/scratch/hyaku/chousa-r32/w1/CtlC2DoNothingB/base-gate.sh --seed 32023279 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32/w1/CtlC2DoNothingB/base-s32023279.json
```

| Seed | Exact count line | Counter exit | Gate exit | Timed out | Control verdict | Receipt (lane-relative) |
|---|---|---:|---:|---|---|---|
| 32023271 | `EXEMPT_AUDIT_MATCH=84/120` | 1 | 0 | false | MISSES | `.ufo/waves/round-32/w1/CtlC2DoNothingB/base-s32023271.json` |
| 32023273 | `EXEMPT_AUDIT_MATCH=84/120` | 1 | 0 | false | MISSES | `.ufo/waves/round-32/w1/CtlC2DoNothingB/base-s32023273.json` |
| 32023279 | `EXEMPT_AUDIT_MATCH=84/120` | 1 | 0 | false | MISSES | `.ufo/waves/round-32/w1/CtlC2DoNothingB/base-s32023279.json` |

Receipt lines 6-14 ground the seed, gate status, count, and predicate; lines 15-30 ground the following per-class output. Each command printed these exact class/count pairs (the counter prefixes class lines with two spaces):

| Class | Seed 32023271 | Seed 32023273 | Seed 32023279 |
|---|---|---|---|
| R1_U_fragment_quote | 0/12 | 0/12 | 0/12 |
| R2_U_path_anchor_cols | 0/12 | 0/12 | 0/12 |
| R3_U_declared_id | 0/12 | 0/12 | 0/12 |
| F1_resolved_verifiable | 12/12 | 12/12 | 12/12 |
| E1_U_anchor_absent | 12/12 | 12/12 | 12/12 |
| E2_U_missing_file | 6/6 | 6/6 | 6/6 |
| E3_U_external_url | 6/6 | 6/6 | 6/6 |
| E4_U_no_citation | 6/6 | 6/6 | 6/6 |
| E5_J_resolvable | 12/12 | 12/12 | 12/12 |
| E6_U_undeclared_id | 6/6 | 6/6 | 6/6 |
| E7_U_out_of_corpus | 6/6 | 6/6 | 6/6 |
| E8_U_quote_glued | 6/6 | 6/6 | 6/6 |
| E9_U_heading_as_plain_line | 6/6 | 6/6 | 6/6 |
| E10_U_line_partial | 6/6 | 6/6 | 6/6 |

C2 has one 120-hop fixture per seed, not C1-style trials (`c2-count.py:9-14,53-74`). The receipt `misses` arrays identify every failed hop.

## Concrete counterexample, cause, smallest safe correction

**Counterexample:** seed 32023271, hop `ha7282b3a`.

- Preserved record `/fast/scratch/hyaku/chousa-r32/w1/CtlC2DoNothingB/fixture-s32023271/root/r01ddf8f9f2.md:74` marks this hop `unresolved`, with citation `f7802dac712.md#quote:zeyobiho zeze`.
- Opened local source `/fast/scratch/hyaku/chousa-r32/w1/CtlC2DoNothingB/fixture-s32023271/root/f7802dac712.md:2` contains `nabihovi yonape zeyobiho zeze turipe bihorida`: the quote is present with word boundaries.
- `base-s32023271.json:32-37` records this hop's truth `resolvable`, but observation `exempt`.
- The base gate's combined exempt arm (`tools/research-gate.sh:1880-1883`) does not parse or read the citation and unconditionally emits `observed=exempt`. The resolved arm parses the citation, resolves the declared source or local path, applies the source boundary, reads it, and matches its anchor (`tools/research-gate.sh:1828-1878`).

**Impacted axis:** coverage. A locally available citation remains falsely labelled unavailable. The three control executions themselves operated successfully, so these runs do not identify a control-harness operability failure or a C1 result.

**Why the counter rejects do-nothing:** R1-R3 contribute 36 expected `resolvable` hops. The counter compares each observation and its finding-id set with truth (`c2-count.py:268-294`) and requires all 120 to match (`c2-count.py:303-324`). Leaving those 36 as `exempt` cannot meet P2 even though the other 84 cases match and the gate exits 0. No do-nothing control met the target; these runs expose no false acceptance of this control.

**Smallest safe correction [INFERENCE, not implemented or scored]:** separate `unresolved|blocked-no-fetch|labelled-dead` from the judgment statuses, and use the existing resolved citation/source-boundary/anchor semantics for a read-only U audit. Only a citation that would verify should emit `observed=resolvable`, mismatch, exactly one `CHAIN_EXEMPT_RESOLVABLE` warning/critical finding, and drift. All other U hops remain exempt without findings; `rejected`, `not-applicable`, and resolved behavior remain unchanged. Do not replace the resolver with an existence check, arbitrary substring grep, or a second independently defined citation authority. This is a fixable coverage defect in the base, not evidence that the do-nothing implementation satisfies the contract.

## Bounds and limits

- Only the base scratch gate was scored. No candidate C1/C2 build, C1 counter, no-harm suite, selftest, canonical judge, or other runtime was invoked. No admission, integration, or production edit was attempted.
- No network action, lane/fleet git write, jj action, or index mutation was performed. The only git operation was the read-only frozen-counter lookup above.
- Three counters completed in the foreground (tool wall times 2.39, 2.40, 2.39 seconds); no background jobs were launched.
- Preserved fixture and experimental gate remain solely in this seat's scratch directory; counter receipts are solely in its artifact directory. The report is at the assigned trailer path.
- `timeout 30s wc -c` on the three receipt paths and scratch gate exited 0: each receipt is 5,181 bytes; scratch gate is 306,617 bytes, all below 1 MiB. Writes during scoring were additionally capped by `prlimit --fsize=1048575`.
- The counter was not altered. Findings are limited to these three seeded do-nothing control runs and the opened code, receipts, and fixture; no claim of candidate feasibility, all-seed correctness, or overall round acceptance is made.
