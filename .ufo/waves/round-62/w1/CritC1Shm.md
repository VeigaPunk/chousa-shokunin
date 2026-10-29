# CritC1Shm: attack on the H14/H15 memory legs under the v2 counter (round 62, w1)

Counter: `corpus/evidence/round62/c1v2-count.py` (sha256 prefix `b7016fba91b03460`, matches claims.md). Imported read-only
and run with `python3 -B`; never edited. Reference legs: round-61 `c1-count.py`. Nothing under the lane was written.
Host: Linux 7.2.11, util-linux unshare 2.42.4, Python 3.14.8, 31.7 GiB RAM, unprivileged user namespaces available.

## Findings

1. **A detached helper escapes the RSS leg.** The leg reads `ru_maxrss` from `wait4` on the `unshare` pid, which covers
   only the builder and the descendants it reaps. A `setsid` helper that holds 150 MiB and is never reaped leaves the
   leg at rc=2 with rss 14.6 MiB. H14 and H15 PASS in both profiles. Official CLI:
   `LEG H14 BIGTXT pass ... rss_kib=16244`, `LEG H15 BIGRAW pass ... rss_kib=16032` (a2, seed 11). Independent peak of
   the helper (VmHWM, sampler): 156 MiB.
2. **The namespace bounds a helper in time, not in size.** Under v2 every helper died when the builder exited
   (survivors 0 in all v2 runs). Under the round-61 counter the same helpers survived the builder: 1, 3, 8, 1
   survivors in a2, a2b, a2c, a2d; the harness killed them. The 200 MiB AS limit is per process, and nothing bounds the
   count: eight helpers of 150 MiB held 1.26 GiB sustained while the v2 leg read rss 14.6 MiB and PASSed (a2c).
   One helper can hold 156 MiB for 50.3 s, inside the 60 s timeout, and PASS both legs (a2d). The timeout does kill the
   namespace: a5b (builder lingers 75 s) gives rc=-9 at 60.0 s, FAIL, and the helper is gone (survivors 0).
3. **`ru_maxrss` is a max over processes, not a sum.** Three reaped children each hold 70 MiB at the same time (barrier):
   H14 and H15 PASS. CLI: `rss_kib=77628` (H14 neutral), `77556` (H15 neutral), `LEGS=13/20`. Sampler sum: 240 MiB.
   A single reaped 150 MiB child is caught (a7 FAIL, rss 159 MiB), so the gap is sum versus max.
4. **Shared-memory staging is invisible to the leg.** A `memfd` copy of the whole 192 MiB capture, through a 1 MiB user
   buffer (`copy_file_range` into a memfd returns EXDEV on this host), passes H14 and H15 in both profiles (rss
   13-14.6 MiB). `Shmem` in `/proc/meminfo` rises by 186-192 MiB during the leg and returns to 64388 kB (baseline
   64756 kB) at exit. CLI (a8, seed 11): `LEG H14 ... pass`, `LEG H15 ... pass`, `LEGS=3/20`.
5. **Legitimate streaming passes, as it should.** 1 MiB reads that refuse at the end (a0) and 8 MiB `mmap` windows with
   `MADV_DONTNEED` (a9) pass both legs at rss 14.6-18.1 MiB; independent peak 13-19 MiB. A whole-file `mmap` (a10)
   is refused under AS in plain (rc=1) and runs windowed in neutral (rc=2, 17.9 MiB): both pass.
6. **H14/H15 do not separate streaming from stubs.** The legs require only rc != 0, no output and rss < 96 MiB. a11
   (`os.unshare(CLONE_NEWPID)` gives EPERM here, so the builder exits 1 before any helper exists) passes both legs at
   13 MiB. The naive whole-file read (a1) passes plain by an AS-limit MemoryError (rc=1, 14.6 MiB) and fails only in
   neutral, where the random AS slack (200-224 MiB) lets the read succeed (206 MiB rss). The catch therefore comes
   from random AS slack, not from the 96 MiB rule.
7. **What the legs do catch:** a 128 MiB read held in the builder (a1b, rss 140 MiB, FAIL both) and a reaped single
   150 MiB child (a7, FAIL both). A builder that waits out the counter is caught by the 60 s timeout (a5b).

Named-limit check (claims.md, C1 named limits): "a builder that reads a 192 MiB capture in a detached helper under the
address-space limit is bounded, not measured" holds per process only. The measured reach is about 200 MiB per process,
unbounded in count (1.26 GiB in a2c) and up to 59 s in duration (a2d). "A builder that keeps the read in shared memory
below the limit is not measured" holds (finding 4). Finding 3 (max versus sum) is not named in claims.md.

## Attack matrix (v2 H14/H15 per profile; driver with an independent /proc sampler)

Counter rss = max over profiles of `ru_maxrss` (MiB). Indep = sampler peak (sum VmRSS of processes whose cmdline carries
the attack's work path; Shmem delta for memfd). Survivors = processes alive after the leg (v2 / v1).

| attack | what it does | v2 H14 | v2 H15 | counter rss | indep peak | surv v2/v1 | class |
|---|---|---|---|---|---|---|---|
| a0 stream_refuse | 1 MiB reads, refuse | PASS | PASS | 14.6 | 13 | 0/0 | legit streaming |
| a9 mmap_window | 8 MiB windows, DONTNEED | PASS | PASS | 18.1 | 19 | 0/0 | legit streaming |
| a10 mmap_whole | whole-file map | PASS | PASS | 17.9 | 17 | 0/0 | AS-bounded or windowed; not escape |
| a1 naive_read | whole-file read | PASS (plain) / FAIL (neutral) | same | 206 | 197 | 0/0 | control, caught via AS slack |
| a1b in_builder_128 | 128 MiB held in builder | FAIL | FAIL | 141 | 139 | 0/0 | control, caught |
| a7 reaped_single_150 | reaped child holds 150 MiB | FAIL | FAIL | 159 | 167 | 0/0 | control, caught |
| a2 detached_hold_150 | setsid helper, unreaped, builder exits | PASS | PASS | 14.6 | 168 (helper 156) | 0/1 | ESCAPE |
| a2b detached_3x120 | three unreaped helpers | PASS | PASS | 14.6 | 390 | 0/3 | ESCAPE |
| a2c detached_8x150 | eight unreaped helpers | PASS | PASS | 14.6 | 1262 | 0/8 | ESCAPE |
| a2d detached_linger | helper holds 50.3 s, builder exits | PASS | PASS | 9.3-14.6 | 168 for 50 s | 0/1 | ESCAPE (duration) |
| a5b linger_builder | builder lingers 75 s | FAIL (rc -9, 60 s) | FAIL | 14.6 | 168 | 0/1 | timeout caught; helper killed |
| a6 reaped_3x70 | three reaped children, concurrent | PASS (CLI 77.6) | PASS (CLI 77.8) | 77.6 | 240 | 0/0 | ESCAPE (max, not sum) |
| a8 memfd_stage | 192 MiB copy in memfd | PASS | PASS | 14.6 | Shmem +191 | 0/0 | ESCAPE (shmem) |
| a11 nested_pidns | os.unshare CLONE_NEWPID | PASS (rc=1, EPERM) | PASS (rc=1) | 13.7 | 15 | 0/0 | stub pass, not escape |

Escapes: a2, a2b, a2c, a2d, a6, a8 (k=6). Legitimate streaming readers that pass: a0, a9 (and a10 windowed).

## Method and receipts

- Frozen counter modules imported with `importlib` (`sys.dont_write_bytecode`); `leg_h14`/`leg_h15` called per profile as
  `main()` does (plain and neutral), and the round-61 counter's legs called once (single layout) for comparison.
  Scratch driver and attack builders: `/fast/scratch/hyaku/chousa-r62/CritC1Shm/` (deleted before yield).
- Official CLI run (`C1V2_SEED=11 python3 -B corpus/evidence/round62/c1v2-count.py --builder <attack> --work <dir>`) for
  a0, a2, a6 and a8: results quoted in findings 1, 3, 4 and 5.
- Sampler: a 3 ms poll of `/proc` (cmdline matched on the work path; VmRSS, VmHWM, RssShmem, Shmem from `/proc/meminfo`).
  Peaks are lower bounds: a6 H15 neutral sampled 12 MiB while its three children existed (poll granularity).
- Sanity: `Shmem` after a8 returned to baseline; sampler found zero processes left after the full matrix (`DONE leftover_processes= 0`).

## Limits and INFERENCE

- Named-file `/dev/shm` retention was NOT run (it would write outside my scratch). INFERENCE: such a file outlives the
  namespace, because teardown kills processes, not files, and the leg checks only `out/` (`clean_out`). Writes outside the
  fixture are not checked by any v2 leg.
- A helper in a nested pid namespace was NOT reached (`os.unshare` gives EPERM for this unprivileged user), so
  nested-namespace survival is untested.
- AS slack is random only in the neutral profile; plain always uses the 200 MiB limit.
- The sampler is a lower bound (poll-based); the leg rss is `ru_maxrss` of the reaped tree, as the counter uses it.
- Smallest routing (not a rewrite): a limit for the next round's battery. The counter already owns the namespace; it
  could sum VmHWM (or VmRSS plus RssShmem) over every process visible in the namespace at the poll, plus a host
  Shmem delta, and reject any leg over 96 MiB. Not checked here: whether a delegated cgroup `memory.peak` is available.
- Battery (`c1v2-battery.py`) was not run on my attacks; the twelve forgers do not depend on memory (named gap X10).

## Tooling

No installs or upgrades. No git, jj or index writes. No network. No writes under the lane or the fleet.

VERDICT: RSS_ESCAPES_UNDER_V2=6 legitimate_streaming=yes
