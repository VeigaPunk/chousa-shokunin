# CtlC2NoisyB — design v2 re-score

Axes: coverage and operability. Read `corpus/evidence/round32/claims.md:119-189` and the v2 counter contract before scoring. Re-scored all four distinct controls from the original report; no oracle was built by this seat. Flat-path copies are byte-identical aliases, not additional control payloads.

## Frozen inputs and boundaries

Counter: `corpus/evidence/round32/c2-count-v2.py`, design commit `3d586d3a`, SHA-256 `8ec1a1ed44f1d3971a73eeace677cbedd0187563bea063ec6b680261dbb23c8a`.

Observed matching hashes from these commands (exit 0):

```text
timeout 15s sha256sum /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round32/c2-count-v2.py
timeout 15s git show 3d586d3a:corpus/evidence/round32/c2-count-v2.py | sha256sum
```

`S=/fast/scratch/hyaku/chousa-r32/w1/CtlC2NoisyB`; every gate is `S/gates/<control>/tools/research-gate.sh`. C1_TMP/C2_TMP/TMPDIR were S, outside every gate-derived lane root `S/gates/<control>`. All four mutated gate hashes were checked before scoring and matched their original control hashes; none was pristine BASE (`0bc318b3…`), so rebuilding was unnecessary.

## Results

Two fresh seeds per control. Every invocation: counter exit 1, gate exit 1, no timeout, empty stderr, `RECORD_CHECKS=ok`. Target is 132/132. **Every control MISSES.**

| Control | Gate SHA-256 | Fresh seeds | Counts respectively | Verdict |
|---|---|---|---|---|
| noisy-findings | `147900f09f8e39f02265576955d1622b15d18256ca73b69ebe139df1a35a873f` | 8055364568199844946; 4087561188954041677 | 60/132; 60/132 | MISSES |
| noisy-observed | `0389f0b341be1609da5d9b2457c3b63f012fab7068fb6d44a0a1adc6e0b68f60` | 5220345181289092889; 5923239035305813738 | 60/132; 60/132 | MISSES |
| noisy-duplicate | `4db1cd8cd58bd6cda320a39cea0d1a7b6218a3d28e85c17a92b855d1c8b6444e` | 8080037718891573224; 817765620494969616 | 24/132; 24/132 | MISSES |
| duplicate-only | `30225fadc5974f0f3069ed0a9e871bc1d2957f7a33a5d4eac6d1c49b2c9b0c5d` | 5347280805125668471; 4319852068402012179 | 96/132; 96/132 | MISSES |

The original v1 multiplicity counterexample is caught under v2: both duplicate-bearing controls now match R1/R2/R3 at 0/12 each. Duplicate-only matches every other class, including E11/E12 at 6/6 each, leaving exactly 36 multiplicity misses. Nonduplicate noisy controls match R1–R3, F1 and E5 only; combined noise+duplication matches F1 and E5 only. These are observed per-class outputs, not candidate claims.

## Receipts and commands

All paths below are lane-relative. Prefix `A=.ufo/waves/round-32/w1/CtlC2NoisyB/v2`.

For each table seed, the frozen receipt is `A/<control>-s<seed>.json` and full command/output is `A/<control>-s<seed>.log`. Logs contain actual command line 3, exit line 4, `EXEMPT_AUDIT_MATCH` line 6, `RECORD_CHECKS=ok` line 7, and all 16 class lines at 8-23. `A/runs.json` records exact argv vectors, seeds, hashes, paths and timings for all eight runs.

Representative actual command, lane cwd, environment as above (exit 1):

```text
timeout --signal=TERM --kill-after=10s 700s prlimit --as=2147483648 --nproc=8192 --fsize=1048576 -- python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round32/c2-count-v2.py --gate /fast/scratch/hyaku/chousa-r32/w1/CtlC2NoisyB/gates/duplicate-only/tools/research-gate.sh --seed 5347280805125668471 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32/w1/CtlC2NoisyB/v2/duplicate-only-s5347280805125668471.json
```

Two concurrent foreground scoring workers, all subprocesses awaited; finite 700-second timeout, 2 GiB address-space cap, nproc 8192, 1 MiB file-size cap. `timeout 15s df -h /fast` before scoring: 231G available, 72% used. No failed scoring attempts in this re-score batch.

No counter or gate edits, candidate scoring, network, installations, index/jj writes, or runtime judgment. This supplement changes no prior v1 evidence. No escaping control was observed under v2; no further correction is proposed from this scoped re-score.
