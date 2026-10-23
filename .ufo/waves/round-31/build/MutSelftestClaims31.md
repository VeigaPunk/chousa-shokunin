# MutSelftestClaims31 — base claims-selftest sensitivity

Date: 2026-10-23. Axes: **coverage, operability**. Scope: four isolated, sequential one-line mutants; no candidate implementation or C1/C2 counter was run.

## Ownership and revision

**No: I never mutated or restored the lane gate**, including at the L1-reported **04:26:45Z** rewrite. Every gate patch targeted only `/fast/scratch/hyaku/chousa-r31/w1/MutSelftestClaims31/repo/tools/research-gate.sh`. Lane writes were confined to this report and its permitted evidence directory. No lane/fleet Git-index or jj write was performed. My earlier approximate scratch-edit time in IRC was retracted; its exact edit timestamp was not captured.

Read `corpus/evidence/round31/claims.md` first and `/home/vgpnk/.omp/agent/RULES.md` before commands. Sandbox creation, exit **0**:

```sh
timeout 30 mkdir -p /fast/scratch/hyaku/chousa-r31/w1/MutSelftestClaims31 /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-31/build/MutSelftestClaims31
timeout 600 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone --no-hardlinks --no-checkout /home/vgpnk/Projects/shokunin/chousa-shokunin /fast/scratch/hyaku/chousa-r31/w1/MutSelftestClaims31/repo
timeout 600 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/chousa-r31/w1/MutSelftestClaims31/repo checkout --detach d78d18893849cecb710f3b691ec986e1321d39ee
```

Observed checkout: `HEAD is now at d78d188 round-31: frozen claims design v1 and counters (C1 line binding, C2 revision binding)`.

## Same bounded behavioral detector

Working directory: the sandbox `repo` above. Every matrix run used exactly:

```sh
timeout --signal=TERM --kill-after=5s 1800s prlimit --as=2147483648 --nproc=16384 -- env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE -u CHOUSA_ROOT -u CHOUSA_RECORD -u CHOUSA_CLAIMS -u CHOUSA_AGGREGATOR_ERE -u CHOUSA_NOW_EPOCH -u CHOUSA_STRICT LC_ALL=C.utf8 TZ=UTC TMPDIR=/fast/scratch/hyaku/chousa-r31/w1/MutSelftestClaims31 bash tools/research-gate.sh --selftest
```

Runs were synchronous and sequential, with a new process group and an outer 1806-second watchdog. Each process group was already absent at cleanup; no background job remains. Limits: 2 GiB address space per process; `RLIMIT_NPROC=16384`. Hash commands were `timeout 30s sha256sum <sandbox-gate>`, exit 0. Evidence below is under **`.ufo/waves/round-31/build/MutSelftestClaims31/`**; each run has complete `.log` output and a `.json` receipt containing command argv, exit, duration, before/after SHA-256 and failed-case ordinals.

## Kill matrix

The detector is the unchanged full selftest, including the shared matcher’s chain callers. Failing rows omit their case number, so ordinals count top-level `ok-case`/`FAIL-case`/`SKIP-case` rows; pristine output explicitly numbers the corresponding cases.

| Mutant | Exact one-line change | Expected detector target | Actual output / exit | Killing case numbers | Verdict |
|---|---|---|---|---|---|
| M1: drop left boundary | L1314: `if tok_right_ok "$after" "$span"; then` | Left-glued substring must not count as supported | `RESEARCH_GATE_SELFTEST: PASS (215 cases, 0 skipped)` / 0 | None | **Survived** |
| M2: drop right boundary | L1314: `if tok_left_ok "$before" "$span"; then` | Boundary-negative claims/chain cases must retain missing-span/anchor findings | `RESEARCH_GATE_SELFTEST: FAIL (2/215 cases)` / 1 | **42, 44** | **Killed** |
| M3: last occurrence | L1320: append `\| sort -z -t: -k1,1nr` to the grep match stream, before `)` | First boundary-delimited occurrence must determine reported location | `RESEARCH_GATE_SELFTEST: PASS (215 cases, 0 skipped)` / 0 | None | **Survived** |
| M4: unsupported becomes supported | L1449: `unsupported) observed=supported ;;` | Absent unsupported claims must remain unsupported; exact counts must remain correct | `RESEARCH_GATE_SELFTEST: FAIL (11/215 cases)` / 1 | **21, 28, 55, 57, 59, 60, 61, 62, 74, 134, 135** | **Killed** |

M3’s complete replacement line was:

```sh
  done < <(printf '%s' "$hay" | grep -a -z -b -o -P -- "$regex" | sort -z -t: -k1,1nr)
```

Case names: 21 `claims-pass`; 28 `claims-fail-counting`; 42 `claims-boundary-fail`; 44 `chain-fail-boundary`; 55/60/61 `all-pass.md`; 57 `all-structure.md`; 59 `claims-pass.jsonl`; 62 `all-meta.md`; 74 `all-dangling.md`; 134 `json-unterminated-manifest`; 135 `json-nul-terminated-manifest`.

Key observed mutant outputs:

- `m2-drop-right.log:42-56`: both negative cases return `exit=0 want=1`; BF1/BF2/BF3 become supported, `VERDICT_BEARING_CLAIMS=3/3`; corresponding chain anchors become verified, `RESOLVED_HOPS=3/3`.
- `m4-unsupported-as-supported.log:25`: `CLAIM id=P3 expected=unsupported observed=supported source=lib/primary.md at=- verdict=mismatch`; L39 similarly changes C3; L46 becomes `VERDICT_BEARING_CLAIMS=2/6` rather than expected `3/6`. Case 28 still has the expected CLI exit 1: its output assertions, not exit alone, kill this mutant.
- `m1-drop-left.log` and `m3-last-occurrence.log`: all 215 cases pass. These are coverage findings, not permission to relax the left-boundary or first-occurrence contracts.

## Pristine and restoration evidence

Let **H0** = `ac1315ddaa12e79b68069d1a9866b9b1b55e3a43efef3ba0cb5ca5e665835765`, matching the frozen claims’ base-gate pin. Every run’s hash was unchanged across its detector execution. Each mutant was reversed before the next run.

| Run evidence stem | Exit | Actual closing line | Gate SHA-256 before = after |
|---|---:|---|---|
| `baseline-utf8` | 0 | `RESEARCH_GATE_SELFTEST: PASS (215 cases, 0 skipped)` | H0 |
| `m1-drop-left` | 0 | `RESEARCH_GATE_SELFTEST: PASS (215 cases, 0 skipped)` | `9733425eba6c0b518f70d117823c62a234cf41f1e9e7cae79ebd1315aa53279c` |
| `restored-after-m1` | 0 | `RESEARCH_GATE_SELFTEST: PASS (215 cases, 0 skipped)` | H0 |
| `m2-drop-right` | 1 | `RESEARCH_GATE_SELFTEST: FAIL (2/215 cases)` | `c8e7bc0a0925676677472e72ce833a01117e4c033bd1ad3a6fdecf620f3683f6` |
| `restored-after-m2` | 0 | `RESEARCH_GATE_SELFTEST: PASS (215 cases, 0 skipped)` | H0 |
| `m3-last-occurrence` | 0 | `RESEARCH_GATE_SELFTEST: PASS (215 cases, 0 skipped)` | `eaa2ee617c23d8d4c0df15ea6ba9cf694c2490cd13cb4500d61606bcb8f45358` |
| `restored-after-m3` | 0 | `RESEARCH_GATE_SELFTEST: PASS (215 cases, 0 skipped)` | H0 |
| `m4-unsupported-as-supported` | 1 | `RESEARCH_GATE_SELFTEST: FAIL (11/215 cases)` | `b962822df5bf56389719f926cc87fb850d9d05473c3b187ceadb6c6a23492862` |
| `restored-after-m4` | 0 | `RESEARCH_GATE_SELFTEST: PASS (215 cases, 0 skipped)` | H0 |

Observed restored-detector launch times (UTC): M1 **04:28:40.959**, M2 **04:29:39.966**, M3 **04:30:46.947**, M4 **04:31:49.171**. All used the sandbox path, not the lane gate. Final restored run took 25.822 seconds. Exact inverse patches returned the gate’s tool snapshot to its original `A96E` and its measured SHA-256 to H0 after every mutation.

## Limits and disclosed preflight failure

An initial pristine run used the same command except **`LC_ALL=C`**. It returned **1**, `RESEARCH_GATE_SELFTEST: FAIL (10/215 cases)`; evidence `baseline.log` / `baseline.json`, gate H0 before and after. Cases: 21, 55, 57, 59, 60, 61, 62, 74, 134, 135. `baseline.log:26` shows the Unicode-arrow claim P4 incorrectly unsupported; `json_unescape` uses Bash `printf '\u…'`, which is locale-sensitive [INFERENCE: cause of these failures]. This baseline was **inconclusive**, not a killed mutant. `timeout 20 locale -a` returned 0 and listed `C`, `C.utf8`, `en_US.utf8`, `POSIX`. The harness was changed to the installed UTF-8 locale **before any mutant ran**, then pristine, all mutants and all restores used that identical command. No source/test/contract was changed to obtain the passing baseline.

The frozen design text says 154 base cases; the pinned gate actually executed **215**, with **0 skipped**. No network, C1/C2 counters, candidate implementation, integration, contract changes, or other runtime/agent dispatch. No tool installation/update. Requested PTY allocation was unavailable for the short clone command; detectors did not depend on PTY behavior.
