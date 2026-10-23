# MutSelftestR2 — round-32 R2 mutation probe

## Verdict: HOLDS for the six assigned defects

**Six mutants KILLED; zero survived; zero inconclusive.** Each caused at least one newly added R2 case to fail. Every isolated pristine and restored run passed; no baseline failure was counted as a kill. This is a scoped detector result, not a judgment of C1/C2's frozen predicates.

Axes: **operability** (the full selftest exits 1 for the injected defects and 0 after restoration) and **coverage** (each named round-31 gap reaches its intended new detector).

## Inputs and isolation

- Candidate: `5d8a170795dcf48c3746a4f03dee9cfe32812834`; pristine gate SHA-256 `10f2fe12043c6f1565c7d7b9446ee0c4dc11e9649aa3350dcab96f8a2ccb4098`.
- Read Design v2 at `corpus/evidence/round32/claims.md:119-189`, W1's `ExecR2Selftest31.md`, and the routed gaps at `corpus/lessons/round-31-verifier-spotcheck.md:209-214` before mutation.
- Read-only command `timeout 10s env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /home/vgpnk/Projects/shokunin/chousa-shokunin show 5d8a170795dcf48c3746a4f03dee9cfe32812834:tools/research-gate.sh` returned 0. Its bytes matched all six copied pristine gates and the backup. Read-only `rev-parse` returned gate blob `19b47434fc80df2eb8b4787c36e498b33b2e4539`.
- Each scratch gate occupied `/fast/scratch/hyaku/chousa-r32/w2/MutSelftestR2/<mutant>/lane/tools/research-gate.sh`; each `TMPDIR`, `C1_TMP`, and `C2_TMP` was the sibling `<mutant>/tmp`, outside that lane root. Copied `PROVINCE.md` for the existing lane-fallback selftest (SHA-256 `cf7826a43aaab7c00708ab54bb46577217e7a67ab44a43a33e17ee2a58c1bbec`).
- Six independent scratch roots ran concurrently, without subagents, detached jobs, or production edits. `timeout 10s df -h /fast` returned 0 and showed 220G available before copying. Final `timeout 10s /usr/bin/du -sh` on only my directories returned 0: scratch 2.4M, evidence 352K before the consolidated summary/report.

## Detector and commands

Unmodified full detector, identically invoked for pristine, mutated, and restored phases:

```text
timeout --signal=TERM --kill-after=5s 600s bash /fast/scratch/hyaku/chousa-r32/w2/MutSelftestR2/<mutant>/lane/tools/research-gate.sh --selftest
```

The evidence harness `MutSelftestR2/detect.py` clears inherited `CHOUSA_*`, Git override, and shell-startup variables; sets the three temp variables; caps each combined output log at 1,000,000 bytes; kills its process groups; and restores the pinned backup in `finally` before the restored detector run. Exact commands, exit codes, per-phase hashes, output hashes, and elapsed times are in each `<mutant>-<phase>.json` and `MutSelftestR2/summary.json`.

Commands actually run, both harness exit codes **0**:

```text
timeout --signal=TERM --kill-after=10s 700s python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32/w2/MutSelftestR2/detect.py pristine sha-nonstring line-nonstring endline span-before-stale trimmed-pin hash-fault
timeout --signal=TERM --kill-after=10s 1300s python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32/w2/MutSelftestR2/detect.py mutated-restored sha-nonstring line-nonstring endline span-before-stale trimmed-pin hash-fault
```

All six pristine and all six restored gates returned **0** and printed `RESEARCH_GATE_SELFTEST: PASS (241 cases, 0 skipped)` at line 243 of their respective logs. All twelve logs have SHA-256 `202702b410343f9442378624c87d3fadd9d8c617af48892f782b0051bb05a465`. The six mutated runs returned **1**. There were exactly 18 detector runs; no other selftest or counter run was made by this seat.

## Mutant → failing case table

Line numbers in the mutation column refer to the pinned gate. All mutation diffs and full mutant hashes are preserved in `MutSelftestR2/mutations.json`; the selftest itself was not edited.

| Mutant / smallest changed behavior | Expected new failing case | All actual failing cases | Actual full-selftest output / evidence | Verdict |
|---|---|---|---|---|
| `sha-nonstring`: line 1471 changes presence detection from `json_has_key` to string-only `json_str`, so non-string pins are absent | `claims-r2-sha-nonstring` | `claims-r2-sha-nonstring` | rc 1; `FAIL (1/241 cases)`; `sha-nonstring-mutated.log:236-250` | KILLED |
| `line-nonstring`: line 1464 similarly makes non-string line values absent | `claims-r2-line-nonstring` | `c1-fail-invalid-line`, `claims-r2-line-nonstring` | rc 1; `FAIL (2/241 cases)`; `line-nonstring-mutated.log:219-247,265-277` | KILLED |
| `endline`: line 1567 drops the start-line comparison and binds by end line alone | `claims-r2-endline` | `claims-r2-endline` | rc 1; `FAIL (1/241 cases)`; `endline-mutated.log:238-248` | KILLED |
| `span-before-stale`: line 1536 checks span presence before the hash block and skips pin validation when the span is present | `claims-r2-span-stale` | `claims-sha-stale`, `claims-r2-span-stale`, `r2-hash-fault-shim` | rc 1; `FAIL (3/241 cases)`; `span-before-stale-mutated.log:225-266` | KILLED |
| `trimmed-pin`: two loops after line 1480 strip leading/trailing whitespace from the decoded pin | `claims-r2-ws-pin` | `claims-r2-ws-pin` | rc 1; `FAIL (1/241 cases)`; `trimmed-pin-mutated.log:240-249` | KILLED |
| `hash-fault`: line 1541 substitutes the claimed pin for an invalid hash-tool result instead of `unreadable` | `r2-hash-fault-shim` | `r2-hash-fault-shim` | rc 1; `FAIL (1/241 cases)`; `hash-fault-mutated.log:241-251` | KILLED |

All log paths in the table are under `MutSelftestR2/` next to this report. The new detectors' pinned definitions are `tools/research-gate.sh:7231-7239,7248-7254,7263-7269,7279-7286,7296-7302,7315-7339`.

Behavioral evidence, not merely a generic failing summary:

- Non-string SHA mutant: SN1–SN4 become supported, `VERDICT_BEARING_CLAIMS=4/4`, CLEAN (`sha-nonstring-mutated.log:238-243`).
- Non-string line mutant: LN1–LN3 become supported, `3/3`, CLEAN (`line-nonstring-mutated.log:267-271`).
- End-line mutant: EL1's lines 2–3 span becomes supported despite the line-3-only binding, `2/2`, CLEAN (`endline-mutated.log:240-243`).
- Span-first mutant: SB1 becomes supported, SB2 mislocated, only SB3 remains stale (`span-before-stale-mutated.log:248-254`).
- Trim mutant: WP1–WP3 become supported, `3/3`, CLEAN (`trimmed-pin-mutated.log:242-246`).
- Hash-fault mutant: both normal and fault-shim runs return 0; under the fault shim HF1 remains supported, `1/1`, CLEAN (`hash-fault-mutated.log:241-249`).

The seventh added case, `claims-r2-nested-string`, remained a passing positive control in all 18 runs. It was not a seventh assigned mutation. This does not test the explicitly deferred nested-object-key contract (`tools/research-gate.sh:7340-7351`).

## Hashes and exact restoration

Shared pristine **and restored** SHA-256, for every scratch gate:

```text
10f2fe12043c6f1565c7d7b9446ee0c4dc11e9649aa3350dcab96f8a2ccb4098
```

Mutant SHA-256 values, unchanged by their detector runs:

```text
sha-nonstring      a3d8f2ea78fdc70bda700e976b14ef2a688a16a397273cdd58eaa1db5d2dc48d
line-nonstring     29ef7dde7430a5c61a2521782e2637af3c8c6fdcd9b2c017f66d9fe205a0093b
endline            8cffa223fcd506223d417bef745e12a021525d7183a648f825993f6aa5bd45d2
span-before-stale  409704c16a494949aedfafd437eb8e7978e712be45156fd0b8b44256ec7e959d
trimmed-pin        d9ff23d6f26aaa2ddcd0a37713fb68390399e55ebe0cbaf032df9e44f9a4eee0
hash-fault         091825c346ad1f9796a413ab91e972a8391e2d976443e4258828f070689b6582
```

Each `MutSelftestR2/<mutant>-restoration.json:3-6` records the mutant hash, full backup/restored hashes, and `exact_bytes_restored: true`. Every `<mutant>-restored.json` additionally records the restored hash both before and after its passing detector. The final cleanup command `timeout 10s ps -eo pid,ppid,pgid,args` returned 0; filtering for this seat's scratch and harness paths found no remaining processes (`summary.json`, `remaining_own_processes: []`).

## Limits

One plausible mutation per listed defect, one pristine/mutated/restored cycle per mutation, on this host. This does not establish completeness against other defects or improve the C1/C2 claims; neither frozen counter was run. No network access, tool installation/update, runtime invocation, Git/jj write, integration, or lane production modification was performed. Only this report and my own evidence directory were written in the lane. Every evidence artifact is below 1 MiB; the largest is the 31,506-byte consolidated summary. Scratch gates are restored, not left as candidates.
