# CtlC2NoReaderB — C2 no-reader controls

## Scope, axes, result

Axes: **coverage** (whether P2 rejects citation-unread shortcuts) and **operability** (bounded, executable controls with auditable receipts). This is a control review, not candidate admission or a canonical judgment.

All three controls **MISSES** the frozen target of `EXEMPT_AUDIT_MATCH=120/120`, on both fresh seeds. No tested no-reader control meets the target. No candidate implementation was scored; neither counter was edited. The controls changed only the base gate's exempt-status arm, splitting U from the unchanged `rejected|not-applicable` arm. The existing `resolved` arm was unchanged and still reads its sources; “no-reader” here refers specifically to U hops.

| Control | Seed | Observed count | Counter exit | Gate exit | Verdict | Receipt under `.ufo/waves/round-32/w1/CtlC2NoReaderB/` |
|---|---:|---|---:|---:|---|---|
| A: existing regular file | 589470747567188 | 78/120 | 1 | 1 | MISSES | `a-s589470747567188.json` |
| A: existing regular file | 434132568312209 | 78/120 | 1 | 1 | MISSES | `a-s434132568312209.json` |
| B: A + canonical inside-boundary check | 844554693974308 | 84/120 | 1 | 1 | MISSES | `b-s844554693974308.json` |
| B: A + canonical inside-boundary check | 603402902260668 | 84/120 | 1 | 1 | MISSES | `b-s603402902260668.json` |
| C: nonempty anchor cell + non-URL `to` | 816412648695012 | 60/120 | 1 | 1 | MISSES | `c-s816412648695012.json` |
| C: nonempty anchor cell + non-URL `to` | 329818189604102 | 60/120 | 1 | 1 | MISSES | `c-s329818189604102.json` |

All six receipts report `predicate_holds=false`, `gate_timed_out=false`. All six commands completed normally with exit 1, in 7.59–9.12 seconds of tool wall time. Receipt metadata independently records the gate exit and hashes (first receipts: `a-s589470747567188.json:3-14`, `b-s844554693974308.json:3-14`, `c-s816412648695012.json:3-14`; second receipts were also opened).

## Provenance and construction

Read first: `corpus/evidence/round32/claims.md`; then both counter docstrings. P2 and the no-reader negative controls are frozen in `claims.md:60-90`. Read the godspeed and shokunin skill guidance and `/home/vgpnk/.omp/agent/RULES.md`. No tool installs, network requests, subagents, background jobs, Git/jj writes, or production-file writes were performed.

Base gate SHA-256, observed with `timeout 15s sha256sum tools/research-gate.sh corpus/evidence/round32/c1-count.py corpus/evidence/round32/c2-count.py` (exit 0):

- Gate: `0bc318b3e74ac0ad45f4b34154e886d84aebf44673612afab6de5e0b0ff11258` — matches the declared base.
- C1 counter (not run): `9e787e80b215f6522335c639d5e1b2e60d0a5812b83a9760daf8be9f78415885`.
- C2 counter: `b6626b2cb81b2aeaf66a8ff11a06c030612bf4e264dc128f290021c4aa71f54c`.

Frozen C2 identity was checked read-only with this command (exit 0), which returned the same `b6626b2c…` hash:

```sh
timeout 15s git show 4111607c857bc29ff31883bc095ae00afb527e50:corpus/evidence/round32/c2-count.py | timeout 15s sha256sum
```

Scratch directory: `/fast/scratch/hyaku/chousa-r32/w1/CtlC2NoReaderB/`. Before copying, `timeout 15s df -h /fast` exited 0 and reported 236G available. `timeout 15s mkdir -p /fast/scratch/hyaku/chousa-r32/w1/CtlC2NoReaderB /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32/w1/CtlC2NoReaderB` exited 0. Each scratch gate was copied with `timeout 15s cp /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh <scratch-gate>` (exit 0), then surgically changed only at the original exempt arm, `tools/research-gate.sh:1880-1883`.

| Scratch gate basename | U-hop decision; no anchor-content read | SHA-256 | Bytes |
|---|---|---|---:|
| `control-a-existing-file.sh` | Strip `to#fragment`; resolve a declared source pointer or use a local path; strip pointer file suffix; require non-URL and `-f`. Does not require a valid/nonempty anchor. | `308dab5001553e04f83fe850455e50527bd5da1547697a634b4806c5a66b9b08` | 307633 |
| `control-b-inside-boundary.sh` | A, additionally require canonical `realpath(target)` to start with canonical `realpath(ROOT)/`. | `0cdc8cb738b957f12c2a5b6409930e50b2b48fd48d4ca5ce397665c07356b533` | 307710 |
| `control-c-anchor-cell.sh` | Require nonempty literal `anchor` cell and a non-HTTP(S)-URL `to`. No path existence, source resolution, or fragment parsing. | `afa7bfdeab02ef9815adc76649325d72d63c2c5f04b2264fde2d6d915a1448e9` | 307269 |

Each flagged U hop increments mismatches, prints `observed=resolvable verdict=mismatch`, and emits one `CHAIN_EXEMPT_RESOLVABLE` finding. Other U hops increment exemptions and print `observed=exempt`. The changed scratch branches start at line 1880; A's branch ends at 1904, B's at 1905, C's at 1892. These controls are intentionally defective shortcuts, not feasibility or candidate patches.

`timeout 15s sha256sum` over the three full scratch paths produced the hashes above (exit 0). `timeout 15s stat -c '%s %n'` over all three gates and six receipts produced the sizes above and receipt sizes 5899, 5899, 5205, 5205, 8002, 8002 bytes (exit 0). No large log was written.

Seeds were drawn using `timeout 10s shuf -i 100000000000000-999999999999999 -n 6` (exit 0), in the order shown in the result table. All six scoring calls were dispatched together as independent tool calls, not shell background jobs.

## Executed scoring commands

Working directory for every command: `/home/vgpnk/Projects/shokunin/chousa-shokunin`. Each command sets all temporary directories to this seat's scratch directory, limits address space to 1 GiB and processes to 2000, and has a 45-second timeout plus a 5-second forced-kill grace. Every command below exited 1, not 124 or 137.

```sh
timeout --kill-after=5s 45s prlimit --as=1073741824 --nproc=2000 -- env C1_TMP=/fast/scratch/hyaku/chousa-r32/w1/CtlC2NoReaderB C2_TMP=/fast/scratch/hyaku/chousa-r32/w1/CtlC2NoReaderB TMPDIR=/fast/scratch/hyaku/chousa-r32/w1/CtlC2NoReaderB python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round32/c2-count.py --gate /fast/scratch/hyaku/chousa-r32/w1/CtlC2NoReaderB/control-a-existing-file.sh --seed 589470747567188 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32/w1/CtlC2NoReaderB/a-s589470747567188.json
timeout --kill-after=5s 45s prlimit --as=1073741824 --nproc=2000 -- env C1_TMP=/fast/scratch/hyaku/chousa-r32/w1/CtlC2NoReaderB C2_TMP=/fast/scratch/hyaku/chousa-r32/w1/CtlC2NoReaderB TMPDIR=/fast/scratch/hyaku/chousa-r32/w1/CtlC2NoReaderB python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round32/c2-count.py --gate /fast/scratch/hyaku/chousa-r32/w1/CtlC2NoReaderB/control-a-existing-file.sh --seed 434132568312209 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32/w1/CtlC2NoReaderB/a-s434132568312209.json
timeout --kill-after=5s 45s prlimit --as=1073741824 --nproc=2000 -- env C1_TMP=/fast/scratch/hyaku/chousa-r32/w1/CtlC2NoReaderB C2_TMP=/fast/scratch/hyaku/chousa-r32/w1/CtlC2NoReaderB TMPDIR=/fast/scratch/hyaku/chousa-r32/w1/CtlC2NoReaderB python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round32/c2-count.py --gate /fast/scratch/hyaku/chousa-r32/w1/CtlC2NoReaderB/control-b-inside-boundary.sh --seed 844554693974308 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32/w1/CtlC2NoReaderB/b-s844554693974308.json
timeout --kill-after=5s 45s prlimit --as=1073741824 --nproc=2000 -- env C1_TMP=/fast/scratch/hyaku/chousa-r32/w1/CtlC2NoReaderB C2_TMP=/fast/scratch/hyaku/chousa-r32/w1/CtlC2NoReaderB TMPDIR=/fast/scratch/hyaku/chousa-r32/w1/CtlC2NoReaderB python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round32/c2-count.py --gate /fast/scratch/hyaku/chousa-r32/w1/CtlC2NoReaderB/control-b-inside-boundary.sh --seed 603402902260668 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32/w1/CtlC2NoReaderB/b-s603402902260668.json
timeout --kill-after=5s 45s prlimit --as=1073741824 --nproc=2000 -- env C1_TMP=/fast/scratch/hyaku/chousa-r32/w1/CtlC2NoReaderB C2_TMP=/fast/scratch/hyaku/chousa-r32/w1/CtlC2NoReaderB TMPDIR=/fast/scratch/hyaku/chousa-r32/w1/CtlC2NoReaderB python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round32/c2-count.py --gate /fast/scratch/hyaku/chousa-r32/w1/CtlC2NoReaderB/control-c-anchor-cell.sh --seed 816412648695012 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32/w1/CtlC2NoReaderB/c-s816412648695012.json
timeout --kill-after=5s 45s prlimit --as=1073741824 --nproc=2000 -- env C1_TMP=/fast/scratch/hyaku/chousa-r32/w1/CtlC2NoReaderB C2_TMP=/fast/scratch/hyaku/chousa-r32/w1/CtlC2NoReaderB TMPDIR=/fast/scratch/hyaku/chousa-r32/w1/CtlC2NoReaderB python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round32/c2-count.py --gate /fast/scratch/hyaku/chousa-r32/w1/CtlC2NoReaderB/control-c-anchor-cell.sh --seed 329818189604102 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32/w1/CtlC2NoReaderB/c-s329818189604102.json
```

## Per-class / per-trial output

These are the complete count and per-class values printed by the counter. Columns correspond one-to-one to the six commands above; none are aggregate averages.

| Printed line/class | A / 589470747567188 | A / 434132568312209 | B / 844554693974308 | B / 603402902260668 | C / 816412648695012 | C / 329818189604102 |
|---|---|---|---|---|---|---|
| `EXEMPT_AUDIT_MATCH` | 78/120 | 78/120 | 84/120 | 84/120 | 60/120 | 60/120 |
| `R1_U_fragment_quote` | 12/12 | 12/12 | 12/12 | 12/12 | 0/12 | 0/12 |
| `R2_U_path_anchor_cols` | 12/12 | 12/12 | 12/12 | 12/12 | 12/12 | 12/12 |
| `R3_U_declared_id` | 12/12 | 12/12 | 12/12 | 12/12 | 12/12 | 12/12 |
| `F1_resolved_verifiable` | 12/12 | 12/12 | 12/12 | 12/12 | 12/12 | 12/12 |
| `E1_U_anchor_absent` | 0/12 | 0/12 | 0/12 | 0/12 | 0/12 | 0/12 |
| `E2_U_missing_file` | 6/6 | 6/6 | 6/6 | 6/6 | 0/6 | 0/6 |
| `E3_U_external_url` | 6/6 | 6/6 | 6/6 | 6/6 | 6/6 | 6/6 |
| `E4_U_no_citation` | 0/6 | 0/6 | 0/6 | 0/6 | 6/6 | 6/6 |
| `E5_J_resolvable` | 12/12 | 12/12 | 12/12 | 12/12 | 12/12 | 12/12 |
| `E6_U_undeclared_id` | 6/6 | 6/6 | 6/6 | 6/6 | 0/6 | 0/6 |
| `E7_U_out_of_corpus` | 0/6 | 0/6 | 6/6 | 6/6 | 0/6 | 0/6 |
| `E8_U_quote_glued` | 0/6 | 0/6 | 0/6 | 0/6 | 0/6 | 0/6 |
| `E9_U_heading_as_plain_line` | 0/6 | 0/6 | 0/6 | 0/6 | 0/6 | 0/6 |
| `E10_U_line_partial` | 0/6 | 0/6 | 0/6 | 0/6 | 0/6 | 0/6 |

## Counterexamples and smallest safe correction

1. **An in-boundary regular file is not proof of an anchor.** A's seed 589470747567188 hop `h044bfcc1` has truth `exempt` but is reported `resolvable` (`a-s589470747567188.json:32-37`). B still fails the corresponding class after canonical boundary enforcement: seed 844554693974308 hop `he88e3bb5` is `exempt` → `resolvable` (`b-s844554693974308.json:32-37`). Both controls falsely flag all 12 E1 hops and all 18 E8–E10 semantic near-misses. Generator evidence: `c2-count.py:120-145,193-195,211-219` makes absent anchors, glued quote bytes, plain text rather than a heading, and partial rather than exact lines. Boundary checking fixes E7's six errors, but none of these anchor errors. Coverage is impacted; successful bounded execution does not compensate for false provenance.
2. **Anchor metadata is neither necessary nor sufficient.** C's seed 816412648695012 hop `hb9760842` is truth `resolvable` but observed `exempt` (`c-s816412648695012.json:32-37`): R1 carries its anchor in `to#quote:…`, not the anchor cell (`c2-count.py:174-176`). C also falsely flags missing files, undeclared IDs, out-of-corpus files, and absent/semantically invalid anchors; the per-class output shows every E2, E6, E7 and E8–E10 hop missed. Coverage is impacted in both directions.
3. **The aggregate alone hides a changed error distribution.** B's 84/120 equals the disclosed base count (`claims.md:83-90`), but its R1–R3 are all correct while E1/E4/E8–E10 are all wrong. This is why the per-class evidence must accompany the count. These are fixable implementation defects in the deliberately deficient controls, not acceptable coverage/operability tradeoffs.

Smallest safe correction [INFERENCE, not implemented or scored here]: reuse the existing resolved citation parsing, declared-pointer/path policy, source read and kind-specific `chain_anchor_at` semantics for U hops. Emit the drift finding only when that exact verification succeeds; otherwise keep U exempt without findings. Preserve the judgment-status arm and the existing resolved behavior. Merely adding a boundary check, a nonempty-cell check, or a byte-substring search does not correct the demonstrated failures (`research-gate.sh:1646-1734,1828-1878`). No predicate/counter amendment is warranted by these three results.

## Limits

This assignment exercised three controls on two seeds each, and only the C2 counter. It did not run C1, candidate builds, the gate selftest, round-31 repairs/counters, no-harm suites, external sources, or a canonical judge. Temporary generated fixtures were not retained; receipts retain the per-class results and concrete missed hop IDs, and the unchanged frozen generator supplies the fixture semantics. The results show rejection of these three specified shortcuts, not proof that every no-reader strategy or every output-format defect is rejected. No broader saturation claim is made. All six scoring commands had completed before this report was written; no started background process remains.
