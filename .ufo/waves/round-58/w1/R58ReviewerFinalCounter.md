# Round 58 frozen-counter base/control check

Scope: C1 operability and C2 depth only. Used the committed frozen counters (SHA-256 C1 `65da18bbcb03581ca98354d90049215ed3cab3bfd3e41d483908dc1e1c703d3f`, C2 `dbb859612f9d018296b217baec76a5c6cb744609b7c95372dabae4d6691c8503`), equal to the 9e73a031 versions. Base builder SHA-256 is the frozen pin `1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6`. No live fetch.

## C1 base and controls

Command (fresh work under my seat scratch):
`TMPDIR=/fast/scratch/hyaku/chousa-r58/R58ReviewerFinalCounter-2/c1 python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round58/c1-count.py --builder /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/build-spans.py --work /fast/scratch/hyaku/chousa-r58/R58ReviewerFinalCounter-2/c1/work --controls /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round58/controls`

Observed exact terminal summary:
```
BEFORE_FOREIGN=deleted
CONTROL_REFUSEALL=denied
CONTROL_build-spans-r55=denied
DENIED=2/2
SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=2/2
C1=FAIL
```
Exit 1. Full observed legs: `EMPTY_OK=pass`, `REBUILD_OK=pass`, `FOREIGN=fail(rc=0, orphans deleted: foreign gone=True)`, `SYMLINK_OUT=fail(rc=0, expected refusal)(target-dir-written!)`, `SYMLINK_CACHE=fail(rc=0, expected refusal)`, `FIFO_TXT=fail(rc=1, reason ['NOT_REGULAR', 'FIFO', 'REGTYPE', 'SYMLINK'] absent ...)`, `DEVZERO_TXT=fail(rc=1, reason ['NOT_REGULAR', 'SIZE', 'SYMLINK', 'REGTYPE'] absent ...)`, `FAT_RAW=fail(rc=1, reason ['SIZE'] absent ...)`, `MANY_QUOTES=fail(rc=0, expected refusal)`, `ESCAPE_ENTRY=pass(refused)`, `HELDOUT_OK=pass`.

Agreement with `controls/c1-before.txt` and `controls/c1-controls.txt`: C1 remains FAIL; base destructive leg is still discriminating (`BEFORE_FOREIGN=deleted`); both no-op controls are denied. Main counter failure modes match receipts. The mirror hardcoded by C1 for held-out capture-text/capture exists and its checked capture-text and raw hashes match the pins; mirror `tools/build-spans.py` is absent, so I explicitly supplied the lane base builder as candidate. No drift affecting C1 verdict.

## C2 base and controls

Base command:
`TMPDIR=/fast/scratch/hyaku/chousa-r58/R58ReviewerFinalCounter-2/c2 python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round58/c2-count.py --root /home/vgpnk/Projects/shokunin/chousa-shokunin --work /fast/scratch/hyaku/chousa-r58/R58ReviewerFinalCounter-2/c2/base`

Observed: `ENTRIES=0/1 BOUND=0/1 REF_ID_UNBOUND=1`; `QUOTE_ROWS=0/12 CAPTURE_BOUND=0/12 ENTRY_QUOTES=0/12`; `SUBSTANCE=FAIL ANCHOR_BOUND=0/3 INFERENCE_GROUNDED=no STRAY_IDS=- NEW_GROUND=no REBUILD=FAIL`; errors `ENTRY_MISSING`, `PROVENANCE_TRIO`, `S101_NOT_IN_SOURCE`, `REF_ID_UNBOUND`, `MANIFEST_MISSING`, `BUILDER_REBUILD_MISMATCH`, `CAPTURE_BOUND=0/12`, `ANCHOR_BOUND=0/3`, `ENTRY_QUOTES=0/12`, `NEW_GROUND_FAIL`; `C2=FAIL`, exit 1. This agrees with `controls/c2-before.txt` and frozen-counter receipt `controls/c2-before-frozen.txt` on verdict and missing-entry/quote/binding conditions. Output detail differs from older `c2-before.txt` (frozen receipt additionally records `BUILDER_REBUILD_MISMATCH`); it matches `c2-before-frozen.txt` detail.

Built negative roots in fresh scratch with `controls/build-c2-controls.py --work .../controls/roots`, then ran frozen C2 counter against each root. Both STAGED and REWRITE printed `ENTRIES=1/1 BOUND=0/1 REF_ID_UNBOUND=1`, zero of 12 quotes/captures/entry quotes, `SUBSTANCE=FAIL`, errors including `REF_ID_UNBOUND`, `BUILDER_PIN`, `CAPTURE_TEXT_PIN`, `RAW_PIN`, `QUOTES_MISSING`, `MANIFEST_MISSING`, `NEW_GROUND_FAIL`, and `C2=FAIL` (exit 1). Agreement with `controls/c2-controls.txt` for both controls.

All checks run; scratch removed. No tooling installed. No actionable counter/control drift observed.

VERDICT: the frozen C1 base and no-op controls survive as C1=FAIL; frozen C2 base and STAGED/REWRITE controls survive as C2=FAIL. Before receipts agree on verdict; only the older C2 receipt lacks the later frozen receipt's `BUILDER_REBUILD_MISMATCH` diagnostic.