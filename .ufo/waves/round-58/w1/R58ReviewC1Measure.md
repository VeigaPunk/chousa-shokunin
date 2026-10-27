# R58ReviewC1Measure — C1 operability

## Scope and inputs
- Read frozen claims and counter at freeze `9e73a031ab1ac3bac343de008850d7d87f9e5634`; claims C1 predicate: `corpus/evidence/round58/claims.md`.
- Claim-base `tools/build-spans.py` extracted from `b13ca7b5c8bbb40d2d29a37fb443c64ca043f791`; SHA-256 `1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6`, identical to the frozen round-55 pin and `controls/build-spans-r55.py`.
- Counter SHA-256 `65da18bbcb03581ca98354d90049215ed3cab3bfd3e41d483908dc1e1c703d3f`; scratch copy matched. `capture-text.py` SHA-256 matched pin `2c0140bc04029c8faedc6c89a65bd657430d8b85f433406946567b70303e2573`.
- `claims.md`, `c1-count.py`, and `controls/c1-before.txt` have no diff between freeze commit and control-results commit `718e8d20779427dc011ab211d69093160e2367cc`.

## Reproduction
Scratch: `/fast/scratch/hyaku/chousa-r58/R58ReviewC1Measure/`. Builder and `capture-text.py` were placed together under scratch `tools/`, matching the base builder's `__file__`-relative import. This corrected an initial scratch-layout-only run that lacked the sibling module; that run is not evidence for the result.

Command (no controls; lane-equivalent layout):
`cd /fast/scratch/hyaku/chousa-r58/R58ReviewC1Measure && export TMPDIR=/fast/scratch/hyaku/chousa-r58/R58ReviewC1Measure && python3 c1-count.py --builder /fast/scratch/hyaku/chousa-r58/R58ReviewC1Measure/tools/build-spans.py --work /fast/scratch/hyaku/chousa-r58/R58ReviewC1Measure/run-before`
Observed exact output (matches `controls/c1-before.txt` body):
```
EMPTY_OK=pass
REBUILD_OK=pass
FOREIGN=fail(rc=0, orphans deleted: foreign gone=True)
SYMLINK_OUT=fail(rc=0, expected refusal)(target-dir-written!)
SYMLINK_CACHE=fail(rc=0, expected refusal)
FIFO_TXT=fail(rc=1, reason ['NOT_REGULAR', 'FIFO', 'REGTYPE', 'SYMLINK'] absent in 'build-spans: refused S571: no defined text form for f4088c6d6da1f4763182a51d (raw neither OLE nor zip, no .txt)\n')
DEVZERO_TXT=fail(rc=1, reason ['NOT_REGULAR', 'SIZE', 'SYMLINK', 'REGTYPE'] absent in 'build-spans: refused S581: no defined text form for a172f04219497476db868414 (raw neither OLE nor zip, no .txt)\n')
FAT_RAW=fail(rc=1, reason ['SIZE'] absent in 'build-spans: refused S551: capture-text refused f96cbd6d82dbae8a8e2c6223.raw: ole-malformed: sector shift 0, mini shift 0\n')
MANY_QUOTES=fail(rc=0, expected refusal)
ESCAPE_ENTRY=pass(refused)
HELDOUT_OK=pass
BEFORE_FOREIGN=deleted
DENIED=0/0
SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=0/0
C1=FAIL
EXIT=1
```

Control command used the same base bytes and `--controls .../controls`; observed `CONTROL_REFUSEALL=denied`, `CONTROL_build-spans-r55=denied`, `DENIED=2/2`, `C1=FAIL`, matching `c1-controls.txt`.

Independent FOREIGN probe: seeded `out/spans/S777-1.txt`, `spans.tsv`, and two valid quote rows, then ran the pinned r55 builder. Exact result: `RC=0`; output spans contained only `S501-1.txt` and `S502-1.txt`; `FOREIGN FILE DELETED BY R55 BUILDER`. The counter's own `BEFORE_FOREIGN=deleted` also passed. Thus the FOREIGN leg genuinely distinguishes the pinned r55 behavior, and both frozen receipts are truthful for the observed run. The base battery's per-leg evidence is consistent: safe legs pass; FOREIGN deletes the foreign span; SYMLINK_OUT writes into `realdir` (observed `spans.tsv` and `spans/`); SYMLINK_CACHE produced `out-9/spans/S591-1.txt`; FIFO/device refuse only with generic “no defined text form” (not the required named class); FAT_RAW refuses malformed OLE (not SIZE); MANY_QUOTES accepted the input and created 100,001 span files; ESCAPE_ENTRY refuses before writing `spans.tsv`; HELDOUT_OK passes its pinned form/digest/offset/span checks.

## Findings against the frozen measurement
1. **C1 counter does not establish “without partial writes” for most refusal legs.** `c1-count.py` calls `expect_refuse(..., forbidden_touch=[])` for `SYMLINK_CACHE`, `FIFO_TXT`, `DEVZERO_TXT`, `FAT_RAW`, and `MANY_QUOTES`; the helper only checks nonzero exit and reason text, and checks existence of explicitly listed paths. It neither snapshots those output trees nor checks that existing files remain byte-identical. The claims and counter docstring state refusal without partial writes / “touch nothing”; these legs can report PASS after a builder has written or altered output before refusing. No such candidate pass is asserted here; this is a predicate coverage gap.
2. **`FAT_RAW`'s SIZE reason does not prove bounded raw reads.** The frozen leg creates an 80 MiB sparse malformed OLE and only requires refusal text containing `SIZE`. Base source `tools/build-spans.py` does `b = raw.read_bytes()` at `Forms.get` before invoking `capture-text.text_form`; observed base refusal is `ole-malformed`, not SIZE. A candidate that reads the whole 80 MiB first and then emits SIZE would satisfy the reason-only check while violating the claimed 64 MiB read bound. The current base run proves the leg fails on this baseline, not that a passing implementation actually bounds reads.

Residual risk: safe-leg `snapshot()` records regular-file bytes only (it omits symlinks and directory metadata), so its “outside --out changed” comparison is not a complete filesystem-write audit. No candidate hardening implementation was assessed in this seat.

Checks not run: no live fetch; no builder patch; no full-suite/build/lint verification.

VERDICT: Base C1 attack battery survives as a negative control; the FOREIGN discriminator and frozen receipt are truthful. C1's frozen predicate is inconclusive for partial-write refusal and the actual 64 MiB read bound because those observations are not enforced by the counter.