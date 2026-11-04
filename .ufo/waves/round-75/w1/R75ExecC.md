# R75ExecC — mechanism isolation: content cases vs order randomisation in loader-matrix-v2

Seat: R75ExecC (leaf executor, lane chousa round 75). Date: 2026-11-04.
Frozen matrix analysed: `corpus/evidence/round75/loader-matrix-v2.py`
(sha256 `95bdd49363e475316c5f5a9e200f039fcc1611f6fbd52848af8e078be0268ee7` — matches the digest
declared in `corpus/evidence/round75/claims.md`; verified on the scratch copies before divergence).
Battery: `corpus/evidence/round75/matrix-battery.py` (frozen, unmodified; resolves its own
`HERE`-relative positives and forgers, so both variant runs used the frozen seven subjects).

No committed lane file was edited. Both variants exist only in scratch; their diffs are retained
below. No tool was installed or upgraded (python3 3.14.8 and git 2.56.0 were already present;
`/home/vgpnk/.omp/agent/RULES.md` read as instructed — nothing to record).

## Variants (scratch-only)

Scratch root: `/fast/scratch/hyaku/chousa-r75/R75ExecC/s.PFfOi6` (created `mktemp -d` inside the
seat scratch root; removed at end — see guard compliance).

- **Variant A — `matrix-a-no-dup-cases.py`** (sha256 `d518d729da9cdd98ca03386fd87301bae857afbf8cb4f8e6da322967672f5c29`):
  the three dup-heading cases (`dup-log-heading`, `dup-lesson-heading`, `dup-card-heading`) removed
  from `CASES`; the nine remaining cases are exactly the diff-decidable r74 surface (unchanged,
  3 appends, 3 deletes, replace-equal, receipt-change). Shuffle retained.
- **Variant B — `matrix-b-fixed-order.py`** (sha256 `ca1fc14dbe9cb4c87c9c3f4e0f124d0fac75053b9a05e48987daaf422031550a`):
  all twelve cases kept; the single line `random.Random(seed).shuffle(order)` removed, so cases
  execute in declared list order. Nothing else changed.

Diffs (retained, `diff -u` vs the pristine copy; exit 1 = differences found, expected):
`R75ExecC/variant-a-no-dup-cases.diff` (sha256 `106e4d57340c9badf7cd2c44cc948a469431c74de40cd96b24a6b6969a000821`),
`R75ExecC/variant-b-fixed-order.diff` (sha256 `26396000b4c20575047a4d35ca409a1048af458715f502f90230688dc4111664`).

## Exact commands and exits (chronological)

| # | Command (abridged paths) | Exit |
|---|---|---|
| 1 | `mkdir -p /fast/scratch/hyaku/chousa-r75/R75ExecC && ls -ld … && python3 --version && git --version && df -h /fast/scratch` | 0 |
| 2 | `S=$(mktemp -d "$ROOT/s.XXXXXX"); cp loader-matrix-v2.py → matrix-orig/a/b; mkdir -p <outdir>; sha256sum` (copy digests = `95bdd493…` each) | 0 |
| 3 | `python3 -c "import ast; ast.parse(open(f).read())"` for both variants → `syntax-ok` ×2 | 0 |
| 4 | `diff -u matrix-orig.py matrix-a-no-dup-cases.py > outdir/variant-a-no-dup-cases.diff` | 1 (differ) |
| 5 | `diff -u matrix-orig.py matrix-b-fixed-order.py > outdir/variant-b-fixed-order.diff` | 1 (differ) |
| 6 | battery A run 1: `matrix-battery.py --matrix …/matrix-a-no-dup-cases.py --work …/work-a --runs 2` | 1 |
| 7 | battery B run 1: `matrix-battery.py --matrix …/matrix-b-fixed-order.py --work …/work-b --runs 2` | 0 |
| 8 | direct detail runs, attempt 1 (4× `matrix-a/b --counter forge-*.py --work …/detail-*`): **exit 2 ×4** — `MATRIX_SETUP: [Errno 2] No such file or directory …`; cause: the matrix does not mkdir its `--work` (the battery does). Not a scoring event. | 2,2,2,2 |
| 9 | `mkdir -p` the four detail work dirs, then rerun the 4 direct runs (A×diff-only, A×order-oracle, B×diff-only, B×order-oracle) | 0, 1, 1, 1 |
| 10 | battery A run 2 → `battery-variantA-runs2.log` | 1 |
| 11 | battery B run 2 → `battery-variantB-runs2.log` | 0 |
| 12 | `sha256sum` of all retained evidence | 0 |

All runs used `python3 -B`; battery and matrix were invoked by absolute path from cwd
`/fast/scratch/hyaku/chousa-r75/R75ExecC/s.PFfOi6` (own scratch), never the fleet root.

## Results

### Battery over Variant A (nine diff-decidable cases, shuffle retained) — `BATTERY=FAIL forgers_rejected=3/5 positive=2/2`, exit 1

Run 1 and run 2 agree on every verdict (run-2 log retained: `battery-variantA-runs2.log`,
sha256 `2e39767693676893b01a393b0382329fab1577f7f1f1c5d95f4f5ec3af9a825d`).

| Subject | type | run marks (run1 / run2) | verdict |
|---|---|---|---|
| successor-counter | POSITIVE | 9/9, 9/9 | ACCEPTED |
| ref-counter | POSITIVE | 9/9, 9/9 | ACCEPTED |
| constant-pass | FORGER | 4/9, 4/9 | REJECTED |
| constant-fail | FORGER | 4/9, 4/9 | REJECTED |
| order-oracle | FORGER | run1: 0/9, 2/9 · run2: 3/9, 4/9 | REJECTED |
| **diff-only** | FORGER | **9/9, 9/9 (exit 0)** | **ACCEPTED** |
| **naive-grep** | FORGER | **9/9, 9/9 (exit 0)** | **ACCEPTED** |

Accepted forgers in variant A: **diff-only and naive-grep**, both at full marks on both runs.
(Run-1 marks for order-oracle were 0/9 and 2/9; run-2 drew different seeds and got 3/9 and 4/9 —
see "Lucky-permutation observation".)

### Battery over Variant B (all twelve cases, declared order, no shuffle) — `BATTERY=PASS forgers_rejected=5/5 positive=2/2`, exit 0

Run 1 and run 2 agree on every verdict (run-2 log retained: `battery-variantB-runs2.log`,
sha256 `6f98223730c2371fef65476bf0ccd0c218cb62a8cc2c04237bfc80259d39bc4c`).

| Subject | type | run marks (run1 / run2) | verdict |
|---|---|---|---|
| successor-counter | POSITIVE | 12/12, 12/12 | ACCEPTED |
| ref-counter | POSITIVE | 12/12, 12/12 | ACCEPTED |
| constant-pass | FORGER | 4/12, 4/12 | REJECTED |
| constant-fail | FORGER | 4/12, 4/12 | REJECTED |
| order-oracle | FORGER | 9/12, 9/12 | REJECTED |
| diff-only | FORGER | 9/12, 9/12 | REJECTED |
| naive-grep | FORGER | 9/12, 9/12 | REJECTED |

Accepted forgers in variant B: **none**. Note the order-oracle's 9/12 is deterministic (identical
marks in both runs — with the shuffle gone there is no seed effect left in its outcomes).

### The two mechanisms, separately

**Content cases kill the diff-only/naive-grep forgers.** Remove the three dup-heading cases
(variant A) and both content-blind forgers jump from REJECTED to ACCEPTED 9/9 on both runs.
Keep the twelve cases (variant B or frozen v2) and both fail at exactly 9/12. Case-level detail
(`detail-variantB-diff-only.txt`, exit 1): the nine diff-decidable cases all PASS, and all three
failures are `CASE dup-*-heading FAIL expected_rc=1 actual_rc=0 failed=none expected_failed=…` —
the forger sees a pure append with no numstat deletion and no receipt change and answers PASS,
wrong check-id set. `detail-variantA-diff-only.txt` shows the same subject scoring `LOADER_MATRIX=9/9
MATRIX=PASS` (exit 0) once the content cases are gone.

**Order randomisation kills the order oracle.** Remove the shuffle (variant B) and the oracle
scores 9/12 deterministically; case-level detail (`detail-variantB-order-oracle.txt`, exit 1) shows
it answers every one of the nine order-decidable cases correctly — `unchanged`, `append-0/1/2`,
`delete-0/1/2` (scripted `C2-6`), `replace-equal`, `receipt-change` (scripted `C2-7`) — and loses
only the three dup-heading cases, where its `n ≥ len(SCRIPT)` default of PASS is wrong for reasons
unrelated to order. With the shuffle present and the content cases removed (variant A), the same
oracle collapses to 0/9, 2/9 (battery run 1) and 3/9, 4/9 (battery run 2): the invocation-count
mapping breaks on permuted order alone. So the v2 matrix needs **both** mechanisms and each kills
a disjoint forge pair: content cases ⇒ diff-only + naive-grep; shuffle ⇒ order-oracle.
(constant-pass/constant-fail die on the rc-expectation cases in every variant: 4/9 and 4/12 each.)

### Consequence for the battery verdict line

Variant B prints a battery verdict line identical to the frozen v2 control:
`BATTERY=PASS forgers_rejected=5/5 positive=2/2`, exit 0. The two matrices are therefore not
separable by the battery verdict alone — only by per-subject order-oracle marks (B: 9/12/9/12
deterministic; v2 shuffled: 3/12 and 2/12 per battery, 5/12 in the committed case-level receipt
`controls/order-oracle-through-v2.txt`, not re-measured here). A v1-wave check that wants to prove
the shuffle mechanism specifically should assert the order-oracle marks, not just the verdict line.

### Lucky-permutation observation (supports the claims.md recorded limit)

Five independent order-oracle runs against variant A were observed: 0/9, 2/9, 3/9, 4/9, and a
single direct run at **7/9** (`detail-variantA-order-oracle.txt`, exit 1 — one `receipt-change`
case answered with the wrong failed check-id `C2-6` instead of `C2-7`, one `delete-1` likewise).
Order randomisation is probabilistic exactly as recorded in claims.md: a single run can score high,
but battery acceptance needs full marks on **both** runs, and none of the five runs reached 9/9.

## Retained evidence (all under `.ufo/waves/round-75/w1/R75ExecC/`)

| File | sha256 |
|---|---|
| `variant-a-no-dup-cases.diff` | `106e4d57340c9badf7cd2c44cc948a469431c74de40cd96b24a6b6969a000821` |
| `variant-b-fixed-order.diff` | `26396000b4c20575047a4d35ca409a1048af458715f502f90230688dc4111664` |
| `battery-variantA-runs2.log` | `2e39767693676893b01a393b0382329fab1577f7f1f1c5d95f4f5ec3af9a825d` |
| `battery-variantB-runs2.log` | `6f98223730c2371fef65476bf0ccd0c218cb62a8cc2c04237bfc80259d39bc4c` |
| `detail-variantA-diff-only.txt` | `5a2271c92ae6629654ce590eff587e8415137a320fffe47218d0828a12eba42f` |
| `detail-variantA-order-oracle.txt` | `2ba61b48a4b51ae072d89ac802af6cabd94ab38c1961bdbe4f124c8a2c7a6357` |
| `detail-variantB-diff-only.txt` | `4db49b399f0d15f26869ebf739f23e1521ce3bd91390fb72e6fac41eae738d28` |
| `detail-variantB-order-oracle.txt` | `2e227e375a021e5d6a20efd7a25bbe173049886bdf94c66b09c034d784281739` |

Subject sha256 prefixes printed by the battery were identical across both variants and both runs
(successor `9334721a…`, ref `909987ce…`, constant-pass `0dbd573c…`, constant-fail `d5155850…`,
order-oracle `180d1a3d…`, diff-only `6691c74c…`, naive-grep `e5fc4104…`) — the frozen subjects,
not re-derivations.

## Guard compliance

- Writes: only `.ufo/waves/round-75/w1/R75ExecC/*` (this report, two diffs, six logs) and scratch
  `/fast/scratch/hyaku/chousa-r75/R75ExecC/s.PFfOi6` (removed after evidence extraction).
- Frozen instruments untouched; the committed matrix digest re-verified on the pristine copy
  before divergence (`95bdd493…`).
- All fixture git activity happened inside `tempfile.TemporaryDirectory` repos the matrix creates
  under its `--work` in scratch; the matrix's own fixture-root assertion
  (`rev-parse --show-toplevel` == fixture root) held on every scored run (no `MATRIX_SETUP` root
  mismatch ever printed; the only exit-2 events were the four missing-`--work` attempts, row 8).
- No subagents, no network, no lane/fleet git or jj mutation, no commits, no pacman transactions.
- Scratch removal: `rm -rf /fast/scratch/hyaku/chousa-r75/R75ExecC` (exit 0, directory verified
  absent).
