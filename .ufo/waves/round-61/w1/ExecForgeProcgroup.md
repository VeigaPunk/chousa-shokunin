# ExecForgeProcgroup — A1 parts (2) detached helper and (3) stdout/stderr flood (round 61, w1)

Claims file sha256 9afec8d4…ace0acec, freeze 2b0e17b (A1), first freeze 1661b85. No install made. No lane file touched.

## Findings (first-freeze counter = `git show 1661b85:…/c1-count.py`; amended = lane `c1-count.py`)

1. **First-freeze verdicts CAN be flipped, FAIL to PASS, by a builder that daemonises.**
   `memhog` = reference builder with `try: _hog = path.read_bytes(); del _hog` inserted before the `size > MAX_CAPTURE`
   check (reads the whole 192 MiB capture, then refuses; fails exactly H14, H15). `memhog-launder` = the same with the
   `__main__` tail replaced by: `fork; setsid; fork; grandchild runs main(), writes rc to a pipe; wrapper
   waitpid()s only the first child, reads the pipe, exits with that rc`. The real work runs in a grandchild that nobody
   `wait4`s, so its peak RSS never reaches the counter's `ru_maxrss`.
   | builder | first-freeze | amended |
   |---|---|---|
   | ref | 20/20 PASS | 20/20 PASS |
   | memhog | 18/20 FAIL (H14 rss_kib=216348, H15 216820) | 18/20 FAIL (H14 216012, H15 216356) |
   | memhog-launder | **20/20 PASS** rc=0 | **20/20 PASS** rc=0 |
   The amended counter's `killpg` does not reach the grandchild because it called `setsid()`. Seed 61001, one run each.
   The wrapper's own RSS is about 20 MiB. Observed: the memory leg measures what the builder *process* waited on, not what the builder *does*.
2. **A detached repairer flips a tree leg FAIL to PASS** (`repair-*` = base builder + epilogue; after `main()` it forks a
   daemon that `rmtree`s `tools/__pycache__`). P03 NOPYC reads `pass` in every cell; base alone fails it (`controls/c1-before.txt`).
   | variant | first-freeze | amended |
   |---|---|---|
   | race, same process group (pidfd wait, then rmtree) | P03 pass 4/4 seeds | **P03 fail 4/4** (killpg wins the race) |
   | race, daemon calls `setsid()` | P03 pass 4/4 | **P03 pass 4/4** |
   | stop: builder `SIGSTOP`s the counter, daemon repairs, daemon `SIGCONT`s | P03 pass 4/4 | **P03 pass 4/4** |
   Seeds 61001–61004; whole counter 8/20 (base 7/20) in each passing cell, so one leg flipped, nothing more was built.
   The stop variant reaches its parent as `getattr(os, "get"+"ppid")()`; the A1 sniff sweep
   `grep -nE 'getppid|/proc/|c1-count|round61|leg-|argv\[0\]'` exits 1 (no match) on it and on `memhog-launder` (observed). The sweep is
   a static string match; it did not see either forge.
3. **A daemon that keeps writing after the builder exits flips a correct builder PASS to FAIL.** `late-*` = reference +
   daemon writing `out/late.txt` every 5 ms for 4 s after exit (pidfd wait).
   first-freeze, same group and setsid: 14/20 (P01, P02, P06, H07, H08, H09 fail), 15 and 33 daemons still alive after the counter exited (killed by my driver).
   amended, same group: 15/20 (P01, P06, H07, H08, H09 fail; 0 survivors, but the daemon wrote before `killpg` in five legs);
   amended, setsid: 14/20, 15 survivors after exit. The amended counter's process-group kill covers only the builder's own group.
4. **Flood (3).**
   - first-freeze, 2 GiB *sparse* stderr + stdout (`ftruncate(1|2, 2 GiB)`, zero disk): counter peak RSS **4115 MiB** (2× the flood: `read_text` bytes + str), wall 5.9 s, no OOM
     (RLIMIT_AS 6 GiB set by my driver); **H14 and H15 fail for a correct builder** (`rss_kib=4214720`). Cause (INFERENCE from the identical
     value in both legs and the counter's own peak): the vfork'd child's `ru_maxrss` inherits the parent's heap high-water; the first-freeze
     counter's hiwater stays at 4 GiB for every later leg. Result 18/20 FAIL for the reference.
   - first-freeze, *real* stderr flood, counter run under `RLIMIT_FSIZE` 1 GiB (my cap; so 1 GiB, not 2 GiB, was written): peak RSS 2068 MiB, wall 15.4 s, 18/20 (H14, H15, `rss_kib=2118456`), disk peak 1024 MiB allocated.
     A real 2 GiB was not run: it would exceed the 1 GiB write budget.
   - amended, real 2 GiB stderr (separately, 2 GiB stdout): builder stopped at the 512 MiB `RLIMIT_FSIZE` (it ignored SIGXFSZ, writes returned EFBIG),
     counter peak RSS 232 MiB, **20/20 PASS** both; disk peak 512 MiB for stderr, and 1020 MiB `st_blocks` for the 512 MiB stdout file
     (btrfs delalloc over-count; the byte limit is 512 MiB per file by the rlimit). Sparse 2 GiB in amended: 20/20, the `ftruncate` fails at the rlimit.
   - A first attempt at 2 GiB stderr *and* stdout real on amended hit my 1.1 GiB abort (1152 MiB allocated); the counter was killed by me and that run is void.
   Host harm: none observed (MemAvailable stayed above 10 GiB of baseline in the runs that completed; no stray files; scratch deleted). The first-freeze
   counter's own transient was 4 GiB for a 2 GiB flood; the amended counter's is none.

## Verdicts by amended counter on the same builders
- flood: handled (no flip, bounded RSS and disk).
- detached helper: **not handled** — `setsid` escapes the group kill (cells 1, 2, 3 above), and `SIGSTOP` of the parent is open.
- Fix directions (INFERENCE, not run): counter sets `PR_SET_CHILD_SUBREAPER`, reaps orphans with `wait4(-1)` so their rusage counts, kills the whole
  descendant tree; or run builders in a PID namespace (`unshare --pid --fork --kill-child`) / cgroup so the leg ends when init exits; measure RSS over the descendant tree, not one `wait4`.

## Evidence pointers (scratch, deleted at yield; commands reproducible from the recipe)
Recipe: scratch lane tree `S/{first,amended}/{corpus/evidence/round61/c1-count.py, tools/{capture-text,build-spans}.py}`; builders generated from
`corpus/evidence/round61/controls/ref-build-spans.py` and base `tools/build-spans.py` by string edits above; driver = `python3 -B c1-count.py --builder B --work S/w-TAG --seed 61001`
under RLIMIT_AS 6–10 GiB (FSIZE 1 GiB only for first-freeze real flood), polling disk and MemAvailable every 0.2 s, one run at a time.
Sequential only: a first parallel batch cross-killed siblings and was discarded.
Caveats: seed 61001–61004 only; one run per cell; race cells win 4/4 but timing depends on host load.

VERDICT: FIRST_FREEZE_FLIPPED=yes flood_harm=first-freeze counter 4.1 GiB transient RSS for 2 GiB flood and H14/H15 false FAIL for a correct builder; none on amended amended_ok=no
