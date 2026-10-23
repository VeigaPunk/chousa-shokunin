# CtlC2DoNothingB — design-v2 re-score

**Control verdict: MISSES** on both fresh seeds. This seat built only the do-nothing control, no mutants or oracles. The base hash is intentional; there were no mutated bytes to reconstruct. This supplement does not amend the earlier v1 report or judge/admit a candidate.

- **Axes:** coverage; operability of the control/counter invocation. No C1 measurement.
- Read `corpus/evidence/round32/claims.md:119-189` and `c2-count-v2.py:1-140,260-388`. P2 v2 requires 132/132 (`claims.md:171-175`).
- Gate: `/fast/scratch/hyaku/chousa-r32/w1/CtlC2DoNothingB/do-nothing/tools/research-gate.sh`.
- Gate SHA-256: `0bc318b3e74ac0ad45f4b34154e886d84aebf44673612afab6de5e0b0ff11258` (unmodified base).
- Counter SHA-256: `8ec1a1ed44f1d3971a73eeace677cbedd0187563bea063ec6b680261dbb23c8a`. Current counter hash matched `git show 3d586d3a:corpus/evidence/round32/c2-count-v2.py | sha256sum`; no counter edit.
- Layout: gate lane root is `.../CtlC2DoNothingB/do-nothing`; C1_TMP/C2_TMP/TMPDIR are its sibling `.../CtlC2DoNothingB/tmp-v2`, not inside it.

| Seed | Exact count | Exact record-check line | Counter exit | Gate exit | Timed out | Verdict | Receipt (relative to this report's directory) |
|---|---|---|---:|---:|---|---|---|
| 32023401 | `EXEMPT_AUDIT_MATCH=0/132` | `RECORD_CHECKS=fail:gate-rc=0,drift-summary-lines=0` | 1 | 0 | false | MISSES | `v2/base-s32023401.json` |
| 32023403 | `EXEMPT_AUDIT_MATCH=0/132` | `RECORD_CHECKS=fail:gate-rc=0,drift-summary-lines=0` | 1 | 0 | false | MISSES | `v2/base-s32023403.json` |

Both receipts: lines 3-18 ground record failures, hashes, seed, return status, count, and `predicate_holds=false`; lines 19-36 ground every per-class count. Both commands printed the following identical per-class lines:

```text
  R1_U_fragment_quote 0/12
  R2_U_path_anchor_cols 0/12
  R3_U_declared_id 0/12
  F1_resolved_verifiable 0/12
  E1_U_anchor_absent 0/12
  E2_U_missing_file 0/6
  E3_U_external_url 0/6
  E4_U_no_citation 0/6
  E5_J_resolvable 0/12
  E6_U_undeclared_id 0/6
  E7_U_out_of_corpus 0/6
  E8_U_quote_glued 0/6
  E9_U_heading_as_plain_line 0/6
  E10_U_line_partial 0/6
  E11_U_case_only 0/6
  E12_U_whitespace_only 0/6
```

**Why zero:** v2 requires record exit 1 and exactly one DRIFT summary. The base returned 0 with no DRIFT summary, so `record_ok=false` invalidates every hop (`c2-count-v2.py:312-347`), not just R1-R3. For example, each receipt's lines 38-42 still show a truth-resolvable R1 hop observed exempt. Zero E7 credit here is the global record check, not the earlier flat-gate boundary artifact. No control met the target.

**Smallest safe correction [INFERENCE, not implemented/scored]:** audit U citations with existing resolved semantics and produce the required finding, mismatch, drift verdict, and exit 1 when resolvable; do not merely change exit/summary output. Preserve all remaining exemptions and resolved behavior. The existing base coverage defect remains; this is not candidate evidence.

## Commands and execution limits

Cwd: `/home/vgpnk/Projects/shokunin/chousa-shokunin`. `timeout 30s df -h /fast` exited 0: 804G total, 573G used, 231G available (72%). Preparation and hash commands exited 0:

```sh
timeout 30s mkdir -p /fast/scratch/hyaku/chousa-r32/w1/CtlC2DoNothingB/do-nothing/tools /fast/scratch/hyaku/chousa-r32/w1/CtlC2DoNothingB/tmp-v2 /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32/w1/CtlC2DoNothingB/v2 && timeout 30s cp /fast/scratch/hyaku/chousa-r32/w1/CtlC2DoNothingB/base-gate.sh /fast/scratch/hyaku/chousa-r32/w1/CtlC2DoNothingB/do-nothing/tools/research-gate.sh && timeout 30s sha256sum /fast/scratch/hyaku/chousa-r32/w1/CtlC2DoNothingB/do-nothing/tools/research-gate.sh /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round32/c2-count-v2.py

timeout 30s env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /home/vgpnk/Projects/shokunin/chousa-shokunin show 3d586d3a:corpus/evidence/round32/c2-count-v2.py | sha256sum
```

Successful scoring commands ran concurrently; both exited 1 with the count and record-check output above (tool wall times 5.94 and 5.96 seconds):

```sh
timeout 55s env C1_TMP=/fast/scratch/hyaku/chousa-r32/w1/CtlC2DoNothingB/tmp-v2 C2_TMP=/fast/scratch/hyaku/chousa-r32/w1/CtlC2DoNothingB/tmp-v2 TMPDIR=/fast/scratch/hyaku/chousa-r32/w1/CtlC2DoNothingB/tmp-v2 prlimit --nproc=8192 --as=2147483648 --fsize=1048575 -- python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round32/c2-count-v2.py --gate /fast/scratch/hyaku/chousa-r32/w1/CtlC2DoNothingB/do-nothing/tools/research-gate.sh --seed 32023401 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32/w1/CtlC2DoNothingB/v2/base-s32023401.json

timeout 55s env C1_TMP=/fast/scratch/hyaku/chousa-r32/w1/CtlC2DoNothingB/tmp-v2 C2_TMP=/fast/scratch/hyaku/chousa-r32/w1/CtlC2DoNothingB/tmp-v2 TMPDIR=/fast/scratch/hyaku/chousa-r32/w1/CtlC2DoNothingB/tmp-v2 prlimit --nproc=8192 --as=2147483648 --fsize=1048575 -- python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round32/c2-count-v2.py --gate /fast/scratch/hyaku/chousa-r32/w1/CtlC2DoNothingB/do-nothing/tools/research-gate.sh --seed 32023403 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32/w1/CtlC2DoNothingB/v2/base-s32023403.json
```

Earlier launch attempts used exactly this scoring-command structure with `--nproc=2000`, seeds 32023381/32023389, and receipt names `base-s32023381.json`/`base-s32023389.json`. Both exited 1 with `BlockingIOError: [Errno 11] Resource temporarily unavailable` at counter line 306 while launching the gate. Neither emitted a score or receipt; a targeted glob found no such receipt files. These are failed launches, not semantic control scores. The explicit process ceiling was raised, still bounded at 8192; the memory and file-size bounds remained 2 GiB and 1,048,575 bytes.

Diagnostic commands: `timeout 30s prlimit --nproc` exited 0 and printed inherited limits 122865/122865. `timeout 30s ps -U vgpnk -L --no-headers | wc -l` printed `ps: unsupported option '-L'` and an unusable pipeline count 0; the native-binary replacement `timeout 30s /usr/bin/ps -U vgpnk -L --no-headers | wc -l` exited 0 and counted 1666 threads at that later instant. [INFERENCE] The initial 2000 per-user process ceiling conflicted with transient shared-user process pressure; no counter change was needed.

No candidates, other controls, oracles, canonical judge, background jobs, network actions, installs, production edits, git writes, or jj actions were performed. All foreground invocations completed. Receipts remain only in this seat's `v2/` directory; code experiments remain only in its scratch directory.
