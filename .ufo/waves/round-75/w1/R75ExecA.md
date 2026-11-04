# R75ExecA — C1 both-ways reproduction from committed bytes (lane chousa round 75)

Seat: leaf executor. Repo `chousa-shokunin` HEAD verified at frozen revision before any run; no lane/fleet mutation, no network, no subagents. No tool installs or upgrades were needed or performed (nothing added to the environment; tooling directive recorded as no-op).

## Frozen-bytes verification

- `git rev-parse HEAD` → `43a7a0db52c8aabdf32735f58e09610e05200e79` (equals the frozen revision; exit 0).
- `git rev-parse 43a7a0db52c8aabdf32735f58e09610e05200e79^{commit}` → same hash (object exists; exit 0).
- `git status --porcelain corpus/evidence/round75 corpus/evidence/round74` → empty (working tree clean; exit 0), so working bytes == committed bytes for every instrument, forger, control and claims file used below.
- `git show 43a7a0db…:corpus/evidence/round75/loader-matrix-v2.py | sha256sum` → `95bdd49363e475316c5f5a9e200f039fcc1611f6fbd52848af8e078be0268ee7` (identical to working-tree hash). Same equality held for the r74 matrix (`97963825…2ff8d`) and for `matrix-battery.py`, `ref-counter.py`, `c2-count.py`, `claims.md`.

## sha256 vs claims.md

| File | Measured | claims.md | Match |
|---|---|---|---|
| `corpus/evidence/round75/loader-matrix-v2.py` | `95bdd49363e475316c5f5a9e200f039fcc1611f6fbd52848af8e078be0268ee7` | `95bdd4…8ee7` | yes |
| `corpus/evidence/round74/loader-matrix.py` | `979638251845071cfb2c5e130cd81800251c5a6cb041438deb258d8877e2ff8d` | `979638…ff8d` | yes |

The battery's own `MATRIX_SHA256=` lines printed the same two digests on every invocation.

## Commands run and exits (all exits observed, none assumed)

Scratch root `/fast/scratch/hyaku/chousa-r75/R75ExecA` (battery removes its own `--work` tree in a `finally`; recreated per run).

1. before-run1 / before-run2 (r74 matrix), each exit **1**:
   `python3 -B /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round75/matrix-battery.py --matrix /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round74/loader-matrix.py --work /fast/scratch/hyaku/chousa-r75/R75ExecA/before --runs 2`
   Final lines (both runs identical):
   `forgers_rejected=2/5 positive=2/2`
   `BATTERY=FAIL forgers_rejected=2/5 positive=2/2`
   stderr: empty in both runs.
2. after-run1 / after-run2 (v2 matrix), each exit **0**:
   `python3 -B /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round75/matrix-battery.py --matrix /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round75/loader-matrix-v2.py --work /fast/scratch/hyaku/chousa-r75/R75ExecA/after --runs 2`
   Final lines (both runs identical):
   `forgers_rejected=5/5 positive=2/2`
   `BATTERY=PASS forgers_rejected=5/5 positive=2/2`
   stderr: empty in both runs.
3. Predicate verbatim from claims.md (relative paths, cwd = lane root, read-only there; only `--work` was written, inside my scratch), exit **0**:
   `python3 -B corpus/evidence/round75/matrix-battery.py --matrix corpus/evidence/round75/loader-matrix-v2.py --work /fast/scratch/hyaku/chousa-r75/R75ExecA/predicate`
   printed exactly `BATTERY=PASS forgers_rejected=5/5 positive=2/2`.

All four battery runs and the predicate run completed with **no stderr output at all**.

## Expected vs observed

| Run | Expected | Observed | Verdict |
|---|---|---|---|
| before ×2 | exit 1, `BATTERY=FAIL forgers_rejected=2/5 positive=2/2` | identical, both runs | match |
| after ×2 | exit 0, `BATTERY=PASS forgers_rejected=5/5 positive=2/2` | identical, both runs | match |

## Comparison with committed controls (`corpus/evidence/round75/controls/`)

- `before-battery-r74-matrix.txt`: my before runs are line-for-line identical to the control from `RUN`/`SUBJECT` lines through the `BATTERY=` line (same subject digests `9334721a…`, `909987ce…`, `0dbd573c…`, `d5155850…`, `180d1a3d…`, `6691c74c…`, `e5fc4104…`; same marks 9/9, 4/9; control `EXIT=1` = my exit 1). Header-only differences (`measured-at=`, control's L1 work dir in `command=`).
- `after-battery-v2-matrix.txt`: line-for-line identical except the order-oracle per-run marks. Control: `3/12` and `2/12`. Mine: run1 `6/12` and `3/12`, run2 `4/12` and `3/12`. This variance is explicitly recorded in claims.md ("Order randomisation is probabilistic (one oracle run scored 5/12, the battery's two runs 3/12 and 2/12; a lucky permutation is not excluded)"). Every order-oracle run still exited 1 with fewer than full marks, so rejection held 2/2 runs in both of my invocations; the `BATTERY=` line is byte-identical to the control. No differing verdict line, no accepted forger, no rejected positive.
- `order-oracle-through-v2.txt`: single-run case-level detail (5/12, `LOADER_MATRIX=5/12 MATRIX=FAIL`, `EXIT=1`) — consistent with the probabilistic spread above; my battery runs do not emit case-level detail, so no line comparison was possible beyond the aggregate marks, and none was claimed.

## Conclusion

C1's both-ways predicate reproduces from committed bytes at the frozen revision: r74 matrix FAILs the battery (2/5 forgers rejected, order-oracle accepted 9/9), successor v2 matrix PASSes (5/5, 2/2), exit codes 1/0 as claimed, both matrix digests match claims.md. No kill-rule condition observed.

## Retained evidence (this seat's output dir, complete stdout/stderr/exit per run)

- `before-run1.stdout.txt`, `before-run1.stderr.txt` (empty), `before-run2.stdout.txt`, `before-run2.stderr.txt` (empty)
- `after-run1.stdout.txt`, `after-run1.stderr.txt` (empty), `after-run2.stdout.txt`, `after-run2.stderr.txt` (empty)
- `battery-runs-summary.json` — exact argv, exit code, wall seconds for runs 1–4
- `predicate-v2-lane-root.stdout.txt`, `predicate-v2-lane-root.stderr.txt` (empty), `predicate-v2-lane-root.exit.txt`

## Risks / limits

- Order-oracle rejection through v2 remains probabilistic per claims.md's recorded limits; my four subject runs scored 6/12, 3/12, 4/12, 3/12. A lucky permutation defeating rejection in a future single run is not excluded by this evidence.
- Scratch root `/fast/scratch/hyaku/chousa-r75/R75ExecA` removed at end of seat; no other filesystem writes beyond the seat's own output dir and the lane-root read-only predicate run.
