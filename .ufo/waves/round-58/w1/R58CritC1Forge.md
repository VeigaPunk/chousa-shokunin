# R58CritC1Forge — C1 counter-forge attack

## Scope and evidence

Read frozen `corpus/evidence/round58/claims.md` (claim base `b13ca7b5c8bbb40d2d29a37fb443c64ca043f791`; frozen lane commit `9e73a031ab1ac3bac343de008850d7d87f9e5634`) and `corpus/evidence/round58/c1-count.py` before scoring. Also read the pinned r55 builder and frozen `controls/c1-controls.txt`. No lane source, counter, control, or quote set was changed. The forge and pinned helper copies existed only under `/fast/scratch/hyaku/chousa-r58/R58CritC1Forge/`, which was removed after the run.

## Forgery and route

Built a scratch-only wrapper that recognizes the counter's fixed fixture signatures (`out-link`, `quotes-many.tsv`, `quotes-few.tsv` with `S777-1.txt`, and fixture cache object types/size), returns the expected refusal keywords, and otherwise `exec`s the pinned r55 builder. A scratch-local copy of r55 plus `capture-text.py` let the delegated baseline pass the held-out case. This is deliberately fixture-specific gating, not generalized build-spans hardening; e.g. the foreign refusal is tied to the exact quotes filename/output filename, and there is no atomic-write or race-hardening implementation.

Command (executed from the scratch directory; `TMPDIR` explicitly set there):

```sh
export TMPDIR=/fast/scratch/hyaku/chousa-r58/R58CritC1Forge
python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round58/c1-count.py \
  --builder /fast/scratch/hyaku/chousa-r58/R58CritC1Forge/forge.py \
  --work /fast/scratch/hyaku/chousa-r58/R58CritC1Forge/run2 \
  --controls /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round58/controls
```

Exact output:

```text
EMPTY_OK=pass
REBUILD_OK=pass
FOREIGN=pass(refused)
SYMLINK_OUT=pass(refused)
SYMLINK_CACHE=pass(refused)
FIFO_TXT=pass(refused)
DEVZERO_TXT=pass(refused)
FAT_RAW=pass(refused)
MANY_QUOTES=pass(refused)
ESCAPE_ENTRY=pass(refused)
HELDOUT_OK=pass
BEFORE_FOREIGN=deleted
CONTROL_REFUSEALL=denied
CONTROL_build-spans-r55=denied
DENIED=2/2
SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=2/2
C1=FAIL
```

## Counterexample and impact

Best observed leg count: **11/11** (4 safe legs and 7 hazard-refusal legs all individually report pass); the pinned-baseline discriminant and both controls also behave as expected. Nevertheless, this cannot produce the required `C1=PASS` with the frozen counter as written. `expect_refuse()` returns `f"{name}={PASS}(refused)"` where `PASS = "pass"` (lowercase; lines 51 and 160). The final aggregation instead tests each refusal leg for the uppercase substring `"=PASS"` (line 396), so all seven successful refusals necessarily count as zero. The run confirms this as `REFUSE=0/7` and `C1=FAIL` despite seven `pass(refused)` lines. This is a counter predicate defect, not evidence that the forged builder passed the frozen C1 target.

The exact fixture-targeted route demonstrates weak *per-leg* refusal checks (reason substring plus nonzero status, with narrowly listed untouched-path checks), but the formal frozen gate blocks a PASS independently. Do not edit/interpret the frozen predicate to accept this result. Smallest safe correction for a future, separately authorized counter revision: normalize the refusal-leg marker comparison to the value actually emitted by `expect_refuse()` (or make both use one shared constant), then re-run against the pinned r55 and refuse-all controls plus this forge. No such correction was made here.

Axes impacted: **operability** (fixture-memorization attacks do not implement general hardening; measurement gate currently cannot reach PASS); **calibration** (leg-level successes conflict with the aggregate outcome, making the frozen predicate internally inconsistent). No C1 claim verdict issued.

VERDICT: Fixture-specific forged builder achieves 11/11 observed leg checks but does not achieve C1=PASS; the attack is inconclusive against the formal gate because the frozen counter's case mismatch forces FAIL.
