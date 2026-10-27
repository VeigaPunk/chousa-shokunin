# R58CritC1Bounds — C1 counter attack

## Scope / evidence
- Read frozen `claims.md` and full `c1-count.py`; claim (4) is raw reads bounded at 64 MiB, claim (5) is `quotes.tsv` bounded at 100,000 rows. Counter's concrete probes are an 80 MiB sparse OLE-headed `.raw` and 100,001 identical rows (`S900`).
- Frozen counter SHA is not independently asserted here. Lane HEAD is `5da0a6375a554e1229492a8cb0b9695bd8e85456`; candidate `tools/build-spans.py` and pinned before-builder both hash to `1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6`.
- Baseline command (scratch only):
  `python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round58/c1-count.py --builder /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/build-spans.py --work /fast/scratch/hyaku/chousa-r58/R58CritC1Bounds/base`
- Exact relevant output:
  ```
  FAT_RAW=fail(rc=1, reason ['SIZE'] absent in 'build-spans: refused S551: capture-text refused f96cbd6d82dbae8a8e2c6223.raw: ole-malformed: sector shift 0, mini shift 0\n')
  MANY_QUOTES=fail(rc=0, expected refusal)
  C1=FAIL
  ```
  This is the pinned before-builder, not the proposed hardening. No claim that C1 passes.

## Counterexample: duplicate-ID refusal impersonates row-cap refusal
I ran a scratch-only mutant that has **no total-row limit** but rejects repeated IDs with the message `build-spans: ROWS duplicate id`. On the frozen counter:

`python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round58/c1-count.py --builder /fast/scratch/hyaku/chousa-r58/R58CritC1Bounds/mutant.py --work /fast/scratch/hyaku/chousa-r58/R58CritC1Bounds/dup`

Observed: `MANY_QUOTES=pass(refused)` (overall `C1=FAIL` for unrelated hazard legs). `expect_refuse` accepts any error text containing `SIZE`, `ROWS`, or `CAP`; the all-identical fixture makes duplicate rejection sufficient. The 100,001 row probe therefore does not establish the row-count bound against this accepted leg. The mutant is not a full passing C1 builder; the concrete result falsifies the *MANY_QUOTES leg's discrimination*, not a C1=PASS receipt.

A counter-accepted malformed-row dodge is not demonstrated: no candidate implementation from the build wave was available in this seat's evidence, and the checked-in candidate is still the before-builder. Likewise, I did not execute short-read or boundary-sized raw mutants. The frozen FAT_RAW probe only establishes refusal on its specific 80 MiB sparse fixture; it does not observe bytes read before refusal or test 64 MiB / 64 MiB+1 boundaries.

## Impact and smallest safe correction
- **Operability / row cap:** `MANY_QUOTES` currently admits wrong-reason refusal. Make the 100,001-row fixture distinguishable from duplicate-ID refusal (e.g. varied valid IDs/rows where feasible) and require a specific row-limit diagnostic that cannot be satisfied by a duplicate-ID message. Keep this as a finding against the frozen predicate, not an edit.
- **Operability / raw cap:** current one-point sparse-file fixture cannot prove the read itself was bounded, nor the exact threshold. Add a bounded instrumented probe (or a controlled resource/read counter) and boundary fixtures if the predicate is intended to establish those properties. No such behavior was exercised here.
- The `SYMLINK_OUT` post-check also overwrites the `expect_refuse` result with `SYMLINK_OUT=pass(refused)` whenever its target stays empty; observed source lines 221–225 of the frozen counter. It can mask wrong return/reason on that leg, though separate from the assigned byte/row limits.

Scratch mutant and counter worktree were removed. No tools installed; no source-repository files changed.

VERDICT: Frozen C1 row-cap attack **falsifies the MANY_QUOTES leg's specificity** (wrong-reason duplicate-ID mutant reports pass); raw-bound evasions remain inconclusive because the frozen candidate is the pinned before-builder and no hardened candidate was available.