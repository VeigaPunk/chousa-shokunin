# C1 truncation controls — CtlC1Truncate

Access date: 2026-10-23. Axis: **operability** only. This is a bounded adversarial-control probe, not a candidate implementation, admission judgment, or production change.

**Result: all four controls MISSES on completed runs; none reached 30/30. Three controls have both requested seeds. Suffix8192's second seed and the representative restored-byte behavioral rerun were started but cancelled to honor the binding 40-minute seat limit. That acceptance coverage is incomplete, not a passing or failing fabricated receipt. Exact scratch-byte restoration is complete.**

## Frozen inputs and smallest mutation

Read `corpus/evidence/round34/claims.md` first, then the counter docstring and implementation. Located quote, accessed 2026-10-23: “Short spans (64..4096 bytes) keep their verdicts.” (`corpus/evidence/round34/claims.md:43`). Frozen design revision: `70feb5eacc959eb98071461fe89f0b892c0810d8`.

- Base gate SHA-256: `43a1af35ca668fe535fcef1e68b0c64bbba3eada59c7a23181f591901fca4346`.
- Frozen counter SHA-256, before and after: `5ef347874960b52561a1cfa517f3f3fc0d1763830e3580c44b993f8394c0a565`.
- Scratch: `/fast/scratch/hyaku/chousa-r34/w1/CtlC1Truncate/`.
- Artifacts below: `A=.ufo/waves/round-34/w1/CtlC1Truncate/`, relative to the lane root. Every retained artifact is below 1 MiB; largest observed was 357659 bytes (`timeout 15s wc -c .../CtlC1Truncate/*`, exit 0).

Each scratch control began as a copy of the verified base. Only two statements were inserted: immediately after local span initialization in `tok_span_at` and `tok_span_all`, at mutant lines 1559 and 1590. Existing matcher, token-boundary checks and line accounting then consume the shortened local span. This explicitly derives line binding from the truncated occurrence. Short fixture spans are unchanged.

| Control | Inserted statement, in both functions | Scored mutant SHA-256 |
|---|---|---|
| prefix32767 | `if [[ ${#span} -gt 32767 ]]; then span=${span:0:32767}; fi` | `403d592f84e7966fca04a77dcbdb0e5e5784daf586e4fd33c4c2cbde06590a11` |
| prefix8192 | `if [[ ${#span} -gt 8192 ]]; then span=${span:0:8192}; fi` | `92a462636b422e7f3cc1f8805f6808e09165f8e5f5c492b2083ce801068003de` |
| suffix32767 | `if [[ ${#span} -gt 32767 ]]; then span=${span: -32767}; fi` | `692c0dc4872bf906bcadeb105fe914abacd30ec3114b5a740c3c0f059013da7e` |
| suffix8192 | `if [[ ${#span} -gt 8192 ]]; then span=${span: -8192}; fi` | `f85d2f25a00e12df81f2b6854d884ab616aabd43f45b062d709a0ef064f1b799` |

Archived scored gates: `A/prefix32767.sh`, `A/prefix8192.sh`, `A/suffix32767.sh`, `A/suffix8192.sh`; pristine archive: `A/base-gate.sh`. Construction and hashes: `A/construction.json`. Base functions and their line accounting were opened at `tools/research-gate.sh:1553-1607`; callers at `:1803-1876`. No ExecC1Build candidate was scored.

## Actual commands and detector

All runs used the frozen counter, cwd `/home/vgpnk/Projects/shokunin/chousa-shokunin`, with `C1_TMP` and `TMPDIR` set to the scratch directory. Maximum simultaneous counter runs in this seat: four. Fresh seeds chosen: 349101 and 349102; neither is in the excluded 3401–3409 range.

The pristine command, exit **1**, was:

```sh
timeout 1700s prlimit --as=2147483648 --nproc=4096 --fsize=16777216 env C1_TMP=/fast/scratch/hyaku/chousa-r34/w1/CtlC1Truncate TMPDIR=/fast/scratch/hyaku/chousa-r34/w1/CtlC1Truncate python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round34/c1-count.py --gate /fast/scratch/hyaku/chousa-r34/w1/CtlC1Truncate/base-gate.sh --seed 349101 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-34/w1/CtlC1Truncate/pristine-s349101.json
```

Each mutation was invoked as the following exact command shape, substituting a row's control and seed:

```sh
timeout 1790s python3 .ufo/waves/round-34/w1/CtlC1Truncate/run-control.py CONTROL SEED /fast/scratch/hyaku/chousa-r34/w1/CtlC1Truncate/CONTROL.sh
```

`run-control.py` launches `timeout 1700s prlimit --as=2147483648 --nproc=4096 --fsize=16777216 python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round34/c1-count.py --gate GATE --seed SEED --receipt RECEIPT`, under the stated environment. Completed runs' exact argument arrays, PID/PGID, exit codes and full counter stdout are retained in `A/CONTROL-sSEED.run.json`. Frozen receipts are `A/CONTROL-sSEED.json`. Pristine provenance and PID/PGID are in `A/pristine-command.json`.

Expected detector: reject every truncation shortcut below the frozen 30/30 target. The counter's record rule is at `corpus/evidence/round34/c1-count.py:280-305`; target and receipt formation at `:316-338`. Its gate timeout remained 1500 seconds, unchanged.

## Measurements and per-control verdicts

Every completed counter exited **1**, with gate exit **1**, `gate_timed_out=false`, and `predicate_holds=false`. The counter only scores records when the required DRIFT line is present (`c1-count.py:281-283`); all completed runs have nonzero matched counts.

| Control | Seed 349101 | Seed 349102 | Target verdict |
|---|---:|---:|---|
| pristine base | 19/30 (945.989 s) | not assigned | baseline failure |
| prefix32767 | 19/30 (939.616 s) | 19/30 (1154.420 s) | **MISSES** |
| prefix8192 | 18/30 (795.027 s) | 23/30 (1063.770 s) | **MISSES** |
| suffix32767 | 19/30 (963.997 s) | 19/30 (1170.521 s) | **MISSES** |
| suffix8192 | 19/30 (1062.050 s) | cancelled; no count/receipt | **MISSES** on measured seed; second-seed coverage incomplete |

Per-class output, transcribed from frozen receipts; the paired 32767 columns apply identically to **both** completed seeds:

| Counter class | Pristine 349101 | Prefix32767, both | Prefix8192 349101 | Prefix8192 349102 | Suffix32767, both | Suffix8192 349101 |
|---|---|---|---|---|---|---|
| long-verbatim-ml | 0/3 | 0/3 | 0/3 | 1/3 | 0/3 | 0/3 |
| long-verbatim-1l | 0/2 | 0/2 | 0/2 | 2/2 | 0/2 | 1/2 |
| long-edge | 0/2 | 0/2 | 0/2 | 0/2 | 0/2 | 0/2 |
| long-mut-head | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 |
| long-mut-tail | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 |
| long-mut-mid | 3/3 | 3/3 | 2/3 | 3/3 | 3/3 | 3/3 |
| long-split | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 1/2 |
| long-glued-left | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 |
| long-glued-right | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 |
| long-line-bound | 0/2 | 0/2 | 0/2 | 0/2 | 0/2 | 0/2 |
| long-line-wrong | 0/2 | 0/2 | 0/2 | 1/2 | 0/2 | 0/2 |
| short-verbatim | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| short-mut | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |

Evidence locations: each completed frozen receipt's `:12-30` gives count and all per-class results. Full stdout with the literal `LONGSPAN_MATCH=` and per-class lines is in the associated `.run.json:27` (pristine stdout is also in the tool transcript). No per-class output exists for either cancelled run, so none is invented.

### What the controls exposed

- Both 32767-byte controls remove the kernel argv-length failure but still print `grep: regular expression is too large` (their receipts `:11`, both seeds). They report every long positive and every long line-bound/mislocated case incorrectly; their 19/30 is the same class profile as the base. This is **not** a working long-span search.
- Prefix8192, seed 349101, falsely accepts a changed middle byte: id `c27911bf0e3`, truth unsupported, observed supported (`A/prefix8192-s349101.json:98-103`). Seed 349102 reaches 23/30 but still misses both long-edge and both long-line-bound records (`A/prefix8192-s349102.json:16-29`).
- Suffix8192, seed 349101, falsely accepts separated halves: id `cd0bbbacb74`, truth unsupported, observed supported (`A/suffix8192-s349101.json:86-91`). Its only positive long single-line match does not rescue its other long-positive and line-binding failures.
- All completed runs preserve the six short-span verdicts. None reaches 30/30; there is no surviving 30/30 shortcut to explain. [INFERENCE] The contrast between 32767's regex-size errors and 8192's false positives demonstrates why simply shortening the search pattern is not a full-span fix.

## Mutation-test status, cancellation and restoration

**Formal mutation verdict: INCONCLUSIVE, not KILLED.** The pristine frozen counter already fails 19/30, so a target-rejected control cannot establish a passing-baseline mutation kill. Mechanical control verdicts above remain MISSES; they do not change the frozen contract.

The second suffix8192 run and restored-byte rerun were launched with the same frozen counter and original bounds, then cancelled at `2026-10-23T11:39:14Z` to return within the seat limit. Both outer processes exited **-2**, emitted only their `RUN_PID`/`RUN_PGID` line on stdout, and ended with `KeyboardInterrupt` on stderr; neither emitted `LONGSPAN_MATCH` or a frozen receipt. The restored run used seed 349101 and `--gate /fast/scratch/hyaku/chousa-r34/w1/CtlC1Truncate/restored-gate.sh`.

Cancellation evidence, exact own PIDs/groups and key output: `A/deadline-and-restoration.json`. Only recorded own groups were signalled: suffix8192 outer 4079899 / inner 4081953; restored outer 891723 / inner 894124. Wrapper exception handling kills/waits its own inner group. Cleanup command:

```sh
timeout 15s /usr/bin/ps --sid 4081953,894124,4079899,891723 -o pid,ppid,pgid,stat,args --cols 300
```

It returned **1**, printing the header and **no process rows**. Every completed wrapper had already reaped its child; all remaining manual subprocess futures were collected and their thread pool shut down. No process-name/pattern signalling was used.

Representative restoration first copied the prefix8192 mutant to `restored-gate.sh` (hash `92a462...003de`) and then overwrote it with exact base bytes (full original hash above); commands/output are in `A/restoration-setup.json`. After **all** own scoring/cancelled processes exited, four separately bounded `cp` commands restored the original base over each scored scratch path. Final `timeout 15s sha256sum /fast/scratch/hyaku/chousa-r34/w1/CtlC1Truncate/*.sh .../corpus/evidence/round34/c1-count.py`, exit **0**, returned the original base hash for **all six scratch gates** (base, four controls, representative restored gate) and the unchanged frozen counter hash. Full names and hashes are in `A/deadline-and-restoration.json`. Archived mutant copies retain their scored hashes and were not overwritten. Exact-byte restoration is proven; the interrupted restored behavioral rerun is explicitly inconclusive.

## Bounds and limits

- `timeout 20s df -h /fast`, exit 0: 88G available before fixture work.
- Individual completed counters took 795–1171 seconds. Their observed durations, plus the four-run seat ceiling, prevented completing suffix8192's second seed and the restored behavioral rerun inside 40 minutes. Seven mutant receipts and one pristine receipt were completed; no missing receipt is represented as a score.
- The shared bash background-job ceiling rejected one suffix8192 launch before execution. Subsequent own bounded runs used Python subprocess handles, recorded PIDs and the same harness. The rejected launch was not counted as a run.
- Initial `ps -C ...` identity lookup exited 1 with an unsupported-option error; `/usr/bin/ps -C ...` succeeded and recorded the pristine PID/PGID (`A/pristine-command.json`).
- No installations, network access, subagent dispatch, candidate scoring, production-file edits, git/jj writes, sibling edits, builds, linters or unrelated checks. Only the explicitly assigned frozen behavioral detector and own-process cleanup were exercised.
