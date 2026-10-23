# CtlC2WeakReaderB — design v2 re-score

**All five rebuilt controls MISSED 132/132 on both fresh seeds; every mutated run printed `RECORD_CHECKS=ok` and exited 1.** No candidate or oracle was scored by this seat.

Read `corpus/evidence/round32/claims.md:119-189` and the frozen v2 counter. Counter SHA-256 before/after: `8ec1a1ed44f1d3971a73eeace677cbedd0187563bea063ec6b680261dbb23c8a`, identical to the output of `timeout 15s git show 3d586d3a:corpus/evidence/round32/c2-count-v2.py | timeout 15s sha256sum` (exit 0). No counter edit.

Gates were rebuilt at `/fast/scratch/hyaku/chousa-r32/w1/CtlC2WeakReaderB/gates/<control>/tools/research-gate.sh`; each gate lane root excludes C1_TMP/C2_TMP/TMPDIR (`/fast/scratch/hyaku/chousa-r32/w1/CtlC2WeakReaderB`). Each rebuilt SHA-256 was checked against its original weak-control hash and against BASE before any mutated score; all differed from BASE. Exact mutations remain in the parent directory’s `<control>.patch` artifacts.

| Control | Rebuilt gate SHA-256 | Fresh seeds | Counts (seed order) | RECORD_CHECKS | Verdict | Miss signature |
|---|---|---|---|---|---|---|
| grep-anywhere | `7be8f1d2acb8fae1b6e52baae6a22e8c449cb3d88809c476d70b5f20d4ad19f8` | 2569763456, 2027450782 | 114/132, 114/132 | ok, ok | MISSES | E8/E9/E10 each 0/6 |
| skip-boundary | `a4552ca0157098fda889f339e2373a6150aa060fc3a284b7e2e6840dfed2e081` | 2129073524, 1666069063 | 126/132, 126/132 | ok, ok | MISSES | E7 0/6 |
| case-insensitive | `a0eab06c1546516a21ce54003271742d1b20b742bb319f06939c3a35b4700d06` | 2905630532, 2627283770 | 126/132, 126/132 | ok, ok | MISSES | E11 0/6 |
| whitespace-collapse | `32e03f4f5ccae47fa613efad47b75ee167b4aef03bc61e807213428dda8e8c5d` | 2135935691, 881077013 | 126/132, 126/132 | ok, ok | MISSES | E12 0/6 |
| file-only | `6bed45fb8c4f4735eea3c2db7eb67a59788dd7aabdf5a338851115e9e73629b4` | 2415790626, 4073021679 | 120/132, 120/132 | ok, ok | MISSES | R3 0/12 |

All receipts and raw per-class/per-trial output are under `.ufo/waves/round-32/w1/CtlC2WeakReaderB/v2/`: `<control>-mutated-s<seed>.json` and `.txt` for each table entry. The matching `pristine` and `restored` files preserve the same bounded detector on the same two seeds before mutation and after restoration. `probe-ledger.json` records all 30 commands, outputs, exit codes, hashes and artifact hashes (55,375 bytes; SHA-256 `cb5d60238d46f5f611e8c04f86dfd0eeb32000e5037f97a0434b314aba74728e`).

Concrete mutated command (others are recorded verbatim in their `.txt` files):

```sh
C1_TMP=/fast/scratch/hyaku/chousa-r32/w1/CtlC2WeakReaderB C2_TMP=/fast/scratch/hyaku/chousa-r32/w1/CtlC2WeakReaderB TMPDIR=/fast/scratch/hyaku/chousa-r32/w1/CtlC2WeakReaderB \
  timeout --kill-after=5s 660s prlimit --as=1073741824 --nproc=4096 -- python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round32/c2-count-v2.py --gate /fast/scratch/hyaku/chousa-r32/w1/CtlC2WeakReaderB/gates/grep-anywhere/tools/research-gate.sh --seed 2569763456 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32/w1/CtlC2WeakReaderB/v2/grep-anywhere-mutated-s2569763456.json
```

Cwd `/home/vgpnk/Projects/shokunin/chousa-shokunin`; at most two awaited foreground commands concurrently; 660 s timeout, kill-after 5 s, 1 GiB address-space cap, process cap 4096. The cap was raised from the earlier v1 2000 because that shared-host limit produced fork retries in the separately recorded v1 witness runs. No extra witness runs were needed for v2: the frozen counter itself exercises the new E11/E12 negatives.

## Restoration and limits

Every gate was restored in `finally` to exact BASE SHA-256 `0bc318b3e74ac0ad45f4b34154e886d84aebf44673612afab6de5e0b0ff11258`. The same v2 detector then scored all ten restored runs **0/132**, exactly as on the ten pristine runs, with `RECORD_CHECKS=fail:gate-rc=0,drift-summary-lines=0` and counter exit 1. Mutated runs had gate exit 1 and successful record checks; the missed classes are genuine observed control mismatches, not record-check failures.

Strict killed/survived attribution remains **INCONCLUSIVE**, not “killed,” because the pristine baseline itself fails the full predicate. The requested control verdict is independently **MISSES** for every control. The new case-only and whitespace-only classes now expose the two readers that passed v1; no target was re-scaled by this seat.

No installs, network, background jobs, candidate executions, lane production edits, or Git/JJ writes. All started probe subprocesses were awaited/reaped; all artifacts are below 1 MiB. Original v1 report and lower flat-layout receipts remain unchanged at the previously assigned report path and parent evidence directory.
