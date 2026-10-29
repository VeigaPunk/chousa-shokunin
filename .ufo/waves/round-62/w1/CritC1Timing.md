# CritC1Timing — R62-C1 timing and ordering attack (critic)

Seat CritC1Timing, item critic, claim C1 (operability). Axes: operability (does the counter separate a forger from a
hardened builder), coverage (which timing/ordering channels were exercised), calibration (do same-seed runs agree).
Counter `corpus/evidence/round62/c1v2-count.py` run unmodified (read only). Battery not run (not assigned).

## Findings

1. **A timing-and-mtime forger reaches the counter's full pass: `LEGS=20/20 C1V2=PASS` in 7 of 10 runs.**
   Builder B2 (`timing-forger-b.py`) is the round-61 base builder with two switches that read the counter's own
   fixture state. Each channel was isolated by an ablation at seed 62001:
   - Fixture mtime marker. The counter plants prior-state and victim files with mtime 2001-01-01
     (`OLD_NS = 978307200 * 10**9`, used in `prior_state`, `victim_dir`, and the H11/H12 victims). B2 treats a
     file with that mtime under `--out` or `--cache`, or a non-directory `--out`, as counter state and runs the landing
     builder. Ablation `ablate-b-nomtime.py`: `LEGS=16/20 C1V2=FAIL`, failing H07 H08 H09 H16.
   - Symlink sleep. Any symlink on `--out`, `out/spans`, `out/spans.tsv`, or a `--cache` entry makes B2 sleep 120 s. The
     counter's 60 s timeout SIGKILLs it (rc -9). H10, H11 and H12 accept any `rc != 0` (`c1v2-count.py` lines 512, 529,
     545), and H13 accepts `rc != 0 and not leaked` (line 566), so rc -9 with an untouched victim passes. Ablation
     `ablate-b-nosleep.py` (symlink runs the base builder instead): `LEGS=16/20`, failing H10 H11 H12 H13, with
     `victim_unchanged=False`.
   - Reading: the sleep channel is the "waits out the counter" named limit, now measured. The mtime channel is not in
     the claim's named limits. Both are outside the 12-forger battery. Under the claim's rule (a forger beyond the
     twelve is a counter limit, not a refutation) this routes to the next round's battery. The stated operability aim
     is still unmet for this class: the counter reads a forger as `C1V2=PASS`.

2. **Invocation counting does not help a forger.** B1 (`timing-forger-a.py`) logs each call to a `/dev/shm` ledger keyed
   by the counter's `--work` root and profile. The first call per profile runs the landing builder; later calls run the
   base builder; a later call with a symlink sleeps 120 s. Best `LEGS=15/20`, in 9 of 10 runs (14/20 once). It fails
   H07, H08, H09, H11 and H16 in every run. Only the first call per profile is correct, so every later leg runs base.
   H11 fails on every run for a separate reason: its symlink sits at `out/spans/<id>-1.txt`, which B1's symlink check
   does not look at, so base writes into the victim (`rc=0 victim_unchanged=False`).
   - PID channel: the counter's sandbox makes the builder PID 1. Probe:
     `unshare -Ufp --kill-child --mount-proc python3 -c 'import os;print("pid",os.getpid())'` printed `pid 1`, `rc=0`.
     The PID carries no per-leg information. This matches the frozen NSpid/`getpid()==1` named limit.
   - `/proc/uptime` and fixture timing: neither builder reads them, and I ran no test for them. The counter exposes no
     timing observable except its 60 s timeout (INFERENCE from `c1v2-count.py` `run()`).

3. **Same-seed verdict flips: 4 of 20 builder runs, all on leg H14 BIGTXT, neutral profile only.** The flipping pairs:
   B2 62001 (rep 2: 19/20), B2 62003 (rep 1: 19/20), B2 62005 (rep 2: 19/20), and B1 62003 (rep 2: 14/20). Each flip is
   `LEG H14 BIGTXT fail neutral: FAIL rc=1 rss_kib=215292` (also 215652, 216176, 215556), against `limit=98304`. The
   plain profile on the same runs stays at `rss_kib` 19 to 20 MiB, and the other 16 runs' neutral H14 is about 19 MiB.
   - Mechanism (INFERENCE, not pinned by a run): the neutral profile's address-space limit is `AS_LIMIT` plus a
     `secrets.randbelow(25)` MiB slack (`_env_and_limits`). The base builder's 192 MiB read either fails at allocation
     (RSS about 19 MiB) or touches pages first (RSS about 215 MiB, over the 96 MiB check). The slack is unseeded, so the
     verdict is not a function of `C1V2_SEED` alone.
   - No other leg flipped. All `rc -9` results across the batch were on the sleep legs (H10–H13); none appeared on a
     legitimate leg despite 20 concurrent counters on 32 cores.

## Calibration

- Landing builder, seed 62001, one run: `LEGS=20/20 C1V2=PASS`, exit 0, 4.4 s. H14 neutral `rss_kib=20968`. Not repeated
  (INFERENCE that it is stable at other seeds).
- Per-run table (LEGS, from `LEGS=` lines; rep 1 / rep 2):

| builder | 62001 | 62002 | 62003 | 62004 | 62005 |
|---|---|---|---|---|---|
| B1 timing-forger-a (count + sleep) | 15 / 15 | 15 / 15 | 15 / 14 | 15 / 15 | 15 / 15 |
| B2 timing-forger-b (mtime + sleep) | 20 / 19 | 20 / 20 | 19 / 20 | 20 / 20 | 20 / 19 |
| ablate-b-nomtime (62001 only) | 16 | | | | |
| ablate-b-nosleep (62001 only) | 16 | | | | |

- Best LEGS: 20/20 (B2 at 62001 rep 1, 62002 both reps, 62003 rep 2, 62004 both reps, 62005 rep 1).

## Run record

- Counter command (each run): `C1V2_SEED=<N> python3 -B corpus/evidence/round62/c1v2-count.py --builder <B> --work <scratch>/w-<b>-<seed>-<rep> --receipt <json>`.
  Deviation: `--work` was suffixed per run instead of the literal `.../w`, so 20 runs could go concurrently. The counter
  removes each work dir at exit (no `--keep`). 23 counter runs in total: 20 batch, 1 landing reference, 2 ablations.
- Candidate builders (my directory, `.ufo/waves/round-62/w1/CritC1Timing/`): `timing-forger-a.py`,
  `timing-forger-b.py`, `ablate-b-nomtime.py`, `ablate-b-nosleep.py`. The two ablations are B2 with one branch replaced
  (scripted string replace with an `assert` on each change). Each builder runs the landing or base code in-process with
  `__file__` set to the fixture's tools file, so `capture-text.py` resolves to the fixture copy. Both builders are stdlib
  Python; the scripts were not `py_compile`d into `__pycache__` (`-B`).
- Frozen paths untouched. `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin status --short -- corpus tools SKILL.md`
  printed nothing (read only).
- Cleanup: 20 `/dev/shm/critc1timing-*` ledgers from the batch removed; scratch `/fast/scratch/hyaku/chousa-r62/CritC1Timing`
  removed (verified absent). No tool installed or upgraded; no pacman, no network.

## Routed limits (next round, not applied: the counter is frozen)

- Add a forger class to the battery: "mtime marker plus symlink sleep" (B2 shape, 20/20 on the counter).
- Candidate counter changes for a later round (proposals, not made here): H10–H13 require `rc in (1, 2)` so a timeout
  kill (rc -9) fails; plant victim and prior-state mtimes with a per-run random time so the 2001 marker is not a
  signature; make H14's RSS check independent of address-space slack (for example, a size guard first).

VERDICT: TIMING_FORGE_BEST=20/20 over 5 seeds
