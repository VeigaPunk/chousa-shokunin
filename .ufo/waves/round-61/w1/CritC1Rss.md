# CritC1Rss — R61-C1 memory leg (H14 BIGTXT, H15 BIGRAW) attack

Frozen inputs read, not edited: `corpus/evidence/round61/claims.md`, `c1-count.py`, `controls/`. Lane `tools/` untouched.

## Method
- Loaded the frozen `c1-count.py` read-only with `importlib` and called its own `leg_h14` / `leg_h15` (`big_leg`: sparse 192 MiB file in the fixture cache, `run()` via `os.wait4`, pass = `rc != 0`, no output tree, `ru_maxrss < 96 MiB`). Seed 61001, `random.Random(61001)`. This is the counter's own check, not a re-implementation.
- Eleven candidate builders (scratch only, now deleted). Each candidate also writes its own `VmHWM` to a side file outside the fixture, as ground truth for comparison. The counter never reads that file.
- Command shape: `python3 -B harness.py <candidate>`; the harness prints the leg tuple from the frozen module.

## Results (counter's H14 / H15 `rss_kib`, verdict; independent peak)

| cand | construction | counter H14 | counter H15 | independent peak | reading |
|---|---|---|---|---|---|
| c1_whole | `read_bytes()`, then refuse | 214644 FAIL | 214888 FAIL | VmHWM 216012 | control, correct |
| c2_stream | 1 MiB `read` chunks, sha256, refuse at EOF | 20068 PASS | 19916 PASS | VmHWM 20068 | legitimate |
| c3_mmap_dontneed | `mmap` in 1 MiB windows, `MADV_DONTNEED` after each, refuse at end | 22036 PASS | 21624 PASS | VmHWM 22036 | legitimate |
| c4_mmap_touch | `mmap`, `sha256(mm)` with no DONTNEED | 213624 FAIL | 212880 FAIL | VmHWM 215064 | counted (file-backed mapped pages reach ru_maxrss) |
| c5_detached | double fork + `setsid`; grandchild `read_bytes()`; parent refuses at once | **18188 PASS** | **17700 PASS** | grandchild VmHWM **208968 kB** / **208972 kB** | **ESCAPE** |
| c6_waited | fork (same group); grandchild `read_bytes()`; parent `waitpid`, then refuses | 208456 FAIL | 207196 FAIL | grandchild VmHWM 208940 / 208956 | counted (waited child folds into the parent's rusage) |
| c7_memfd | 1 MiB chunks written into `memfd_create`, refuse | **20004 PASS** | **19860 PASS** | own VmHWM 20004 / 19860; system Shmem **272264 kB / 269648 kB** while retained | **ESCAPE** |
| c8_late_setsid | detached setsid writer; creates `out/spans.tsv` 2.5 s after the leg returns | 18208 PASS | 18396 PASS | n/a (tree, not RSS) | adjacent tree escape (see Finding 3) |
| c9_orphan_pgid | double fork, no `setsid`; grandchild reads, parent refuses | 18448 PASS | 18996 PASS | no completion marker written | not an escape in this run (see Finding 4) |

Subreaper probe (`PR_SET_CHILD_SUBREAPER` on a wrapper that spawns c5 the way `run()` does, then `wait4(-1)` in a loop): the reparented grandchild reports `ru_maxrss` **208132 kB**; the direct child reports 19336 kB.

## Findings

1. **Escape A — detached helper (c5).** A helper that leaves the process group with `setsid` and does the 192 MiB read is invisible to `wait4` on the direct child. The counter saw 18188 KiB (H14) and 17700 KiB (H15) while the reading process peaked at about 204 MiB. The helper survives the `killpg`, because `setsid` moves it out of the group. Both legs PASS. This is a measurement escape and not legitimate: the capture is held whole, just outside the measured tree.
2. **Escape B — shared-memory staging (c7).** Chunks are copied into an anonymous `memfd` that the process keeps until exit, so the whole capture is retained in shmem, not in process RSS. The counter saw 20004 / 19860 KiB. System `Shmem` read 272264 / 269648 kB while the memfd was alive; the baseline read at the start of the session was 77472 kB. The increase is about 190 MiB, which matches the capture. Not legitimate: the capture is held whole. (The baseline and the peak were taken at different moments; the 190 MiB match is INFERENCE.) A `/dev/shm` file written with `write()` would be the same escape (not run).
3. **Adjacent tree escape (c8, not RSS).** The late writer creates `out/spans.tsv` 2.5 s after the leg returns. The leg's `clean_out` runs when `run()` returns, so it cannot see the write. Confirmed: after the leg returned, `work/c8_late_setsid-leg_h14/.../out/spans.tsv` and `.../out/x/` existed. Route to L1 as a counter limit on the C1 tree check. Survival past `killpg` needs `setsid`, the same condition as Escape A.
4. **Not an escape in this run (c9).** A non-`setsid` orphan stays in the counter's process group, so `killpg` ends it. No completion marker was written and no survivor was left at check time. That the group kill always wins the race is INFERENCE from one run. Do not rely on it.
5. **Counted correctly.** Waited helpers (c6: 208456 / 207196 counter vs 208940 / 208956 helper) and mapped file pages (c4) both reach the counter's `ru_maxrss` (`cmaxrss` and `RssFile`). The counter's metric is sound for those classes.
6. **Frozen predicate limit.** H14 and H15 check `rc != 0`, the output tree and the child's `ru_maxrss` only. c5 and c7 satisfy that literally. A builder that refuses without a size check and reads in the background passes.

## Legitimate streaming (decision)
- **Legitimate:** c2 (1 MiB chunks to EOF, nothing retained) and c3 (windowed mmap with `MADV_DONTNEED`; resident set bounded, no retained copy). The capture is never held whole, and the reads cover the full file (the loops run to EOF, per the code; byte count not logged, so full coverage is read from code, not measured).
- **Escape:** c5 (work moved outside the measured tree) and c7 (whole copy retained outside RSS).
- **Counted, not an escape:** c1, c4, c6.
- **Reference builder:** `controls/ref-build-spans.py` checks size (`_read`, line 140) before reading. It never reads 192 MiB, so neither escape applies to it. The escapes matter for a builder that does read: the frozen H14/H15 legs cannot tell it from a streaming builder.

## Suggested counter-level closure (not applied; frozen)
Set `PR_SET_CHILD_SUBREAPER` on the counter and collect with `wait4(-1)` until `ECHILD` before the `killpg`, summing `ru_maxrss` (the subreaper probe above shows this catches c5 at 208132 kB). The tree check should run after the group is gone, not when `run()` returns (closes c8). Neither change touches the predicate sentence. Whether to amend is L1's decision under the frozen kill rule.

## Limits of this probe
- Seed 61001 only; one run per candidate (two runs for c5, c7, c3, c2 showed stable peaks).
- The harness calls the frozen leg functions, not `main()`. The seeded shuffle and the 20-leg run were not exercised, so `C1=` was not counted.
- Candidates implement only the H14/H15 read path, not the full span build. They are probes of the memory leg, not builders for the other legs.
- Pairing of `VmHWM` pids to legs follows run order (INFERENCE). The values are close enough that the verdict does not depend on it.

## Installs
None.

## Cleanup
Scratch `/fast/scratch/hyaku/chousa-r61/CritC1Rss/` removed (verified: `No such file or directory`). No writes outside this report.

VERDICT: RSS_ESCAPES=2 legitimate_streaming=yes
