# R76ExecC — answer-key closure isolation (C1 matrix v3)

Seat: R76ExecC (executor, leaf). Lane: chousa round 76, wave w1. Frozen predicate: `corpus/evidence/round76/claims.md` (C1). Frozen instruments read, never edited: `loader-matrix-v3.py` sha256 `b79d6441…913f`, `matrix-battery-v3.py` sha256 `217ae367…4360`. Receipts: `.ufo/waves/round-76/w1/R76ExecC/`.

## Bottom line

- Three mutants, one closure each. Each closure is load-bearing for some forger, but not every closure is load-bearing for the frozen battery verdict.
- (a) subject closure: **load-bearing against an answer key that uses v3 case names**, but **not visible to the frozen battery**: the frozen `forge-subject-map.py` carries v2 names, so it stays rejected under the restored subject. The battery still prints `BATTERY=PASS 11/11 2/2`.
- (b) byte-stable closure (salt + pad dropped together): **load-bearing**. A learned tree-identity memo reaches 12/12, a whole-tree size memo reaches 12/12. The frozen `tree-identity` and `size-map` forgers do not revive (class forgers, no table), so the frozen battery still prints PASS.
- (c) child bound/session dropped: **load-bearing for termination**. The `hang` forger stalls the matrix; the battery records `matrix_exit=timeout`, counts it as MISS, and prints `BATTERY=FAIL forgers_rejected=10/11`.
- Routed defect (for the planner): the frozen battery's 11 forgers do not include a learned-table answer key for the subject, tree or size classes, so removing (a) or (b) does not flip the frozen predicate. The closures are verified only by the scratch memo forgers below. This is a coverage gap in C1's battery, not a failure of the frozen matrix. Frozen bytes not edited.

## Variants (scratch only; each drops exactly one closure)

Base: frozen `loader-matrix-v3.py` copied to `/fast/scratch/hyaku/chousa-r76/R76ExecC/` (sha256 `b79d6441…913f`, verified).

- **(a) `variant-a-subject.py`** (sha256 `8f77cd27…0690`): per-case commit subject = case name (`-qm name`), replacing literal `case`. Also changed the base commit subject `case` → `base` (base is not a case; disclosed deviation). Diff: `variant-diffs.txt`.
- **(b) `variant-b-nosalt.py`** (sha256 `87695570…71f`): `salted()` returns the unsalted FILES dict; `pad_line()` returns `""`. Salt and pad dropped together because they are one byte-stability closure in the spec.
- **(c) `variant-c-notimeout.py`** (sha256 `1a1449f7…7e2`): child runs with no `start_new_session`, `communicate()` has no timeout and no `killpg`.

Scratch battery copy: `matrix-battery-v3.py` copied unchanged except `LANE` pinned to the absolute lane path (`HERE.parents[2]` would resolve inside scratch). POSITIVES still point at read-only lane counters.

## Battery copy over each variant (`--runs 1`)

Command (exit codes from receipts): `python3 -B <scratch>/corpus/evidence/round76/matrix-battery-v3.py --matrix <variant> --work <scratch>/out/bat-* --runs 1 --matrix-timeout 300` (C: `--matrix-timeout 90`).

| matrix | battery exit | BATTERY line | notable subject lines |
|---|---|---|---|
| frozen v3 (control) | 0 | `BATTERY=PASS forgers_rejected=11/11 positive=2/2` | all REJECTED; matches predicate exactly |
| (a) subject restored | 0 | `BATTERY=PASS forgers_rejected=11/11 positive=2/2` | `subject-map` REJECTED (4/12) |
| (b) salt+pad dropped | 0 | `BATTERY=PASS forgers_rejected=11/11 positive=2/2` | `tree-identity` 5/12 REJECTED, `size-map` 5/12 REJECTED |
| (c) no child bound | 1 | `BATTERY=FAIL forgers_rejected=10/11 positive=2/2` | `hang`: `RUN FORGER hang 0 matrix_exit=timeout marks=none` → `SUBJECT FORGER hang … MISS` |

Receipts: `battery-control-frozen-matrix.txt`, `battery-a-subject-restored.txt`, `battery-b-byte-stable.txt`, `battery-c-no-child-bound.txt` (each with `# exit=`).

Scratch note on the earlier `--runs 1` run for (c): an orphaned `forge-hang` child from my own `out/wc` run (pid 3001142) survived the battery's outer kill; I killed it (scratch-path match only). No orphans remain (`pgrep` check).

## Named revival table (direct matrix runs, two seeds each, `LOADER_MATRIX_CHILD_TIMEOUT=3`)

Forgers are scratch answer-key forgers written by me. `forge-tree-memo-b.py` and `forge-size-memo-b.py` answer from a table learned by `learn-counter.py` on the A+B learner matrix (case-name subject, no salt/pad). The tree and size keys are content-only, so the table transfers to variant B. `forge-subject-named.py` embeds the v3 CASES table keyed on the case name. Miss falls back to PASS. Full rows: `revival-matrix.txt`.

| forger (scratch) | frozen v3 | (a) subject restored | (b) byte-stable |
|---|---|---|---|
| subject-named (v3 case-name key) | 4/12 FAIL ×2 | **12/12 PASS ×2** (revives) | 4/12 FAIL ×2 (literal `case` subject) |
| tree-memo (rev^{tree} key) | 4/12 FAIL ×2 | 4/12 FAIL ×2 | **12/12 PASS ×2** (revives) |
| size-memo, 3 paths (frozen key shape) | 4/12 FAIL ×2 | 4/12 FAIL ×2 | 11/12 FAIL ×2 (stays rejected) |
| size-memo, whole tree (`ls-tree -lr`) | 4/12 FAIL ×2 | 4/12 FAIL ×2 | **12/12 PASS ×2** (revives) |

Why the 3-path size memo stays at 11/12: the receipt case (`case-08-receipt-change`) edits a path outside the three sized paths, so its key collides with `case-00-unchanged` (learned table: 11 distinct keys over 12 cases; the whole-tree key gives 12 distinct keys, 0 collisions). The size closure is load-bearing only through full-tree sizes; path coverage, not padding, is what blocks the 3-path variant.

## Hang probe (direct, own session, `killpg` on probe limit)

Receipt: `hang-probe.txt`. Commands are the frozen `forge-hang.py` against each matrix:
- frozen v3: `exited rc=1 elapsed=36s LOADER_MATRIX=0/12 MATRIX=FAIL` — the child bound keeps the matrix finite (12 × 3 s).
- (c) no child bound: `stalled rc=killed-by-probe elapsed=100s marks=none` — the matrix did not finish within 100 s (the forger sleeps 300 s per case).
- (c) sanity, constant-pass forger: `exited rc=1 elapsed=0s LOADER_MATRIX=4/12 MATRIX=FAIL` (the probe label text was hardcoded as "forge-hang"; the row is constant-pass).

## Load-bearing verdicts

- **(a) subject:** load-bearing for an answer key that uses v3 case names (revives 12/12 under restored subject; stays 4/12 under frozen literal `case`). Not load-bearing for the frozen battery verdict (battery still PASS 11/11 under restored subject), because the frozen `subject-map` forger's table is v2-named.
- **(b) byte stability:** load-bearing (tree memo 12/12, whole-tree size memo 12/12 under the byte-stable matrix). Not load-bearing for the frozen battery verdict (battery still PASS 11/11 under byte-stable matrix), because the frozen `tree-identity` and `size-map` forgers are class forgers (any change → FAIL), not learned tables.
- **(c) child bound:** load-bearing for termination and for the battery verdict (`hang` → MISS; `BATTERY=FAIL 10/11`). Not a revival: no forger revives under (c); the failure mode is a stall.
- **Any closure NOT load-bearing?** None of the three closures is unnecessary for the answer-key attacks above. The frozen battery's verdict is insensitive to (a) and (b), which is the gap. The 3-path size memo staying rejected is a path-coverage effect, not a closure effect.

## Defects / routed items

1. C1 battery coverage gap: the frozen battery does not include a learned-table answer key over subject, tree or size. A matrix that leaks names or is byte-stable reaches `BATTERY=PASS 11/11`. Route to the planner for the round's limits section; the frozen predicate is not amended.
2. The frozen `forge-subject-map.py` docstring says it is "the r75 answer key" but its MAP keys are v2 names (`append-0`, …). It cannot act as the v3 answer key. Route as a forger-freshness note.
3. The frozen `forge-tree-identity.py` and `forge-size-map.py` docstrings describe a "memo" class, but the code is a class forger (no table). Route as a naming note.

## Harness fidelity and tooling

- Control: the frozen-matrix battery copy reproduces `BATTERY=PASS forgers_rejected=11/11 positive=2/2` (exit 0), matching the predicate.
- Tooling: no installs. Python 3 (host), git (host) only. No network. No pacman.
- Receipts: all in `.ufo/waves/round-76/w1/R76ExecC/` (battery logs, revival table, hang probe, variant diffs, scratch forgers and learned tables, learner counters). ~60 KB.

## Checks the main agent may run (not run by me)

- `python3 -B corpus/evidence/round76/matrix-battery-v3.py --matrix corpus/evidence/round76/loader-matrix-v3.py --work DIR` → expect `BATTERY=PASS forgers_rejected=11/11 positive=2/2`.
- Re-run the scratch revival matrix with `--runs 2` if you want an exact count in the report.

## Cleanup

Scratch `/fast/scratch/hyaku/chousa-r76/R76ExecC/` removed after receipts were copied (see final step). No fleet-root file, no lane file, no sibling repo, no git mutation, no commit, no push.
