# Round 62 · w1 · SentRoundScratch — disk and process hygiene audit (sentinel)

Scope: disk, file-handle, process and memory cost of one run of the frozen v2 counter
(`corpus/evidence/round62/c1v2-count.py`), and what 64 seats running it at once would cost.
No lane, tools, corpus, claims or SKILL.md file was written. Scratch used:
`/fast/scratch/hyaku/chousa-r62/SentRoundScratch/` (deleted before yield). No installs.

## Findings

1. **One run's on-disk footprint is tiny; its apparent size is not.** The counter creates a
   192 MiB sparse file (`truncate(BIG)`) in the H14 (`.txt`) and H15 (`.raw`) legs, in each of the
   two profiles, so four sparse files exist at once: about 805 MB apparent. XFS allocates no blocks
   for the zero tail. Measured on-disk peak is 2.3 MiB for the whole run.
2. **Peak per run, measured descendant-only (not host-wide):** 16 open fds, 3 processes
   (counter, `unshare`, builder), 6 threads, about 257 MB summed RSS. The RSS peak is the H20
   BIGFORM leg (builder RSS 226–231 MB, under the 200 MiB `RLIMIT_AS` plus shared pages).
3. **Leftovers from killed or kept runs are sparse too.** `du -sh` of `/fast/scratch/hyaku/chousa-r62`
   shows 699M on disk and `du -sh --apparent-size` shows 32G. Those 32G are about 40 leftover runs of
   four sparse files each. Any seat that `cp`, `tar` or `rsync`s a work tree without sparse handling
   turns each run into about 800 MB of real data. `disk-guard.sh` uses `du -xsk` (actual), so its
   accounting is not affected.
4. **Memory is the binding resource, not disk.** `MemAvailable` was 17.8 GB at the time of the run;
   30 GB total, 14 GB used by the fleet. Worst case of 64 seats at the H20 peak is 64 × 257 MB ≈ 16.4 GB,
   which is at or above what is available. This is an OOM-killer risk, not an ENOSPC one.
5. **Host-wide counter load right now:** a sampler matching `c1v2-count|build-spans|unshare|c1v2-battery`
   on all of `/proc` saw 199–239 matching processes, 968–1180 fds, and about 6.2 GB summed RSS
   (RSS double-counts shared pages; treat as an upper-bound snapshot). The wave is already running
   many counters at once.
6. **ENOSPC failure mode (INFERENCE; not triggered).** Disk is far from full: `/fast` 33 % used,
   544 GB free; `/tmp` 21 % used, 102 GB free. A write failure inside the counter raises `OSError`,
   which the leg wrapper catches and records as `FAIL counter exception OSError`. A builder write
   failure exits 2 with `build-spans: write failed`. Legs H07, H09–H12, H16 and H19 accept rc 2, and
   their `clean_out` check would still hold after an atomic temp-file rename fails. So under ENOSPC a
   leg could pass on the write-failure exit code. This only matters if `/fast` or `/tmp` fills, which
   disk-guard prevents at SOFT 70 %.
7. **File handles are not a constraint.** `ulimit -n` 524288; system `file-nr` 25798 allocated;
   `file-max` unlimited; `pid_max` 4194304; `threads-max` 245730; `ulimit -u` 122865; `/fast` inodes 5.1 M
   used of 421 M. 64 seats × 16 fds ≈ 1 k fds, 64 × 3 processes ≈ 192 processes.
8. **Parallelism instructions.** The frozen `run-c1v2-controls.py` defaults to `--jobs 3`, so each controls
   seat runs 3 counters at once (about 0.8 GB peak RSS). The battery runs its counter subjects
   sequentially, each with `timeout=1800`. A seat passing `--jobs N` with N > 3 would add
   N × 257 MB RSS and N × 800 MB apparent sparse per seat. I did not read the other seats' instructions,
   so I cannot say which seat exceeds the limit; that is INFERENCE from the frozen runner's defaults.

## Evidence (commands and observed output)

- `bash scripts/hyaku/disk-guard.sh status` (exit 0): `/tmp 21% 101.4G free`,
  `/var/tmp 38% 555.3G`, `/fast/scratch/hyaku 33% 540.7G`; top consumer `chousa-r62` 625.2M, idle=0.
- `df -h /fast /tmp`: `/fast` 804G size, 261G used, 544G avail; `/tmp` 128G, 27G used, 102G avail.
- `stat -f -c '%T %S' /fast /tmp` → `xfs 4096`, `xfs 4096`.
- `ls /fast/scratch/hyaku/chousa-r62` → 37 entries (seat dirs, `CritC1Timing` among them).
- `unshare -Ufp --kill-child --mount-proc true` → rc 0 (sandbox usable).
- Counter run 1 (`TMPDIR=… python3 -B c1v2-count.py --work …/c1run --receipt …`) → `LEGS=20/20 C1V2=PASS`, wall 13.7 s;
  runs 2 and 3 → `LEGS=20/20 C1V2=PASS`, wall 17.1 s and 10.8 s.
- Sampler on the work dir (actual `du -sk`, apparent `du -sb --apparent-size`), run 2: peak actual 2336 KiB,
  peak apparent 806 970 434 B (4 × 192 MiB sparse plus small files).
- Descendant-only sampler (`tree.py`, run 3): `PEAK {'fds': 16, 'procs': 3, 'threads': 6, 'rss_kib': 257000, 'samples': 50}`.
- Builder and counter RSS per leg: H14 rss 20.5 MB, H15 21.2 MB, H20 231 MB (plain) and 168 MB (neutral).
- `du -sh --apparent-size` vs `du -sh` on chousa-r62: 32G vs 699M (sparse leftovers).
- `cat /proc/sys/fs/file-nr` → `25798 0 9223372036854775807`; `ulimit -n` 524288; `/proc/sys/kernel/pid_max` 4194304.
- `free -g` → total 30, used 14, avail 15; `/proc/meminfo` `MemAvailable: 17795116 kB`.

## Recommendations

- Counter parallelism: at most 16 counter processes host-wide (about 4.1 GB peak RSS, about 23 % of the
  17.8 GB available at the time). At most 3 counters per seat (the runner default). Do not run 64 seats at once.
- Each seat should create a fresh `--work` dir with `mktemp -d` under its own scratch, and wrap the run in
  `trap 'rm -rf -- "$W"' EXIT`. A killed run leaves four sparse 192 MiB files per leg in `leg-*`; the
  counter's `finally` does not run on SIGKILL.
- Never `cp`, `tar` or `rsync` a counter work tree without `--sparse=always` or `-S`; never archive it.
- Measure leftovers with `du -sk` (actual), not `--apparent-size`.
- No counter instruction in this wave changes the disk verdict; the memory cap is the constraint to communicate.

Checks for the main agent: none run by me beyond the sampler runs above; those runs were measurements, not
verification of the claims. Peak numbers are from a single host sample per run (sampling every 50–200 ms).

VERDICT: PEAK_DISK_PER_RUN=2.3MiB safe_parallel=16
