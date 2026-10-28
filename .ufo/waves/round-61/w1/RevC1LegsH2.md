# RevC1LegsH2 — review of C1 legs H10 SPANSLINK, H11 FILELINK, H12 TSVLINK

Predicate under test: R61-C1 (`corpus/evidence/round61/claims.md`, C1), counter
`corpus/evidence/round61/c1-count.py` (sha256 `f1d8b6fde8dedd88…`, matches the frozen prefix `f1d8b6fd…`).
Reference builder `corpus/evidence/round61/controls/ref-build-spans.py` (sha256 `86d64c312e1640d44f1e…`, frozen `86d64c31…`).
Nothing under the lane was edited or written; `git status --porcelain` on `corpus/evidence/round61 tools corpus SKILL.md` printed nothing.
Scratch `/fast/scratch/hyaku/chousa-r61/RevC1LegsH2/` deleted before this report. Installs: none.

## Findings

**F1 — false positive, three legs (counter defect).** Each of H10, H11 and H12 passes a builder that
writes through the link into the victim and then restores the victim. The leg verdicts are final-state only:
- H10 `c1-count.py:410-414`: `unchanged = snap(v, True) == vb`; verdict `(unchanged and (r["rc"] != 0 or healed))`.
- H11 `c1-count.py:429-431`; H12 `c1-count.py:445-447`: same shape.
A write that is undone before the child exits is invisible to these lines. The predicate text
(`c1-count.py:7-9`, `:22-26`) says "leaves the file tree as each leg states", so this is a final-state blind spot.
It is not in the named limits (claims.md, "Named limits" i–iv). Candidates (all built from the reference, one
leg-specific edit each; full description in "Candidates" below):
- `FP1-rollback-dir` (H10): `spans` is a symlink to the victim dir. Builder writes the golden files through it,
  unlinks the new names, rewrites the saved victim bytes with `os.utime(ns=…)`, exits 2.
- `FP2-rollback-file` (H11): writes the span file through the file-link (`open(…,'wb')`), restores victim bytes and mtime, exits 2.
- `FP3-samebytes-file` (H12): writes `spans.tsv` through the link with identical bytes (victim already equals the
  manifest), restores victim mtime, exits 2.

Evidence (command: `TMPDIR=$S python3 -B c1-count.py --builder $S/b/<name>.py --work $S/w/<name>-<seed> --seed <seed>`):
```
FP1-rollback-dir seed=61001 rc=0 LEGS=20/20 C1=PASS
FP1-rollback-dir seed=61002 rc=0 LEGS=20/20 C1=PASS
FP1-rollback-dir seed=61003 rc=0 LEGS=20/20 C1=PASS
FP2-rollback-file seed=61001 rc=0 LEGS=20/20 C1=PASS      (and 61002, 61003)
FP3-samebytes-file seed=61001 rc=0 LEGS=20/20 C1=PASS     (and 61002, 61003)
```
Leg lines for the three hazard legs, seed 61001: `LEG H10 SPANSLINK pass rc=2 victim_unchanged=True`;
`LEG H11 FILELINK pass rc=2 victim_unchanged=True`; `LEG H12 TSVLINK pass rc=2 victim_unchanged=True`
(same for all three FP builders).

Syscall proof (`strace -f -e trace=openat,rename,renameat2,unlink,utimensat` around a probe that calls the
counter's own `Fx`/`run`/`snap` helpers, imported read-only):
- FP1 H10: `rename("LEG/out/spans/.S343-1.txt.d19383b5d0de.tmp", "LEG/out/spans/S343-1.txt") = 0`, and later
  `unlink("LEG/victim/S343-1.txt") = 0`; the rename target resolves through the `spans` link into `victim/`.
- FP2 H11: `openat("LEG/victim.txt", O_WRONLY|O_CREAT|O_TRUNC) = 3` from the builder pid, then
  `utimensat(... "LEG/victim.txt" ...)` restoring `2000-12-31T22:00:00`.
- FP3 H12: `openat("LEG/out/spans.tsv", O_WRONLY|O_CREAT|O_TRUNC) = 3`, then
  `utimensat("LEG/victim.tsv", …)` restoring mtime.

**F2 — gap: H10–H12 do not check the output tree on refusal.** Verdicts `c1-count.py:414, 431, 447` accept any
non-zero exit without `snap(fx.out)`. Contrast H09 `c1-count.py:390` (`snap(fx.out) == before`) and the reference
docstring contract ("any refusal writes nothing", reference lines 34–40). Probe with FP1 (`H10 rc=2
victim_unchanged=True`, stderr `build-spans: refused output: spans was a symlink; rolled back`) leaves
`out tree: ['spans', 'spans.tsv']` — a manifest with no span files — and the leg passes. The reference on the same
leg leaves `out tree: ['spans']` (only the link). This is the same leg-coverage gap as F1, reached by a different route.

**F3 — no false negative.** Three correct builders (policies the docstring allows) pass all 20 legs at three seeds
(61001, 61002, 61003), including H10–H12:
- `FN1-replace`: a symlinked `spans` or `spans.tsv` or span file is replaced (unlinked before `mkdir`; `os.replace`
  over the link) instead of refused. Leg lines seed 61001: `H10 rc=0 victim_unchanged=True` (healed branch),
  `H11 rc=0`, `H12 rc=0` — healed passes with the exact golden tree. `LEGS=20/20 C1=PASS` ×3.
- `FN2-exit1-order`: link checks moved before the orphan scan, exit 1 for link refusals (within the docstring's
  {0,1,2}); H07/H09/H16/H19 keep their exit 2. `H10 rc=1`, `H11 rc=1`, `H12 rc=1`. `LEGS=20/20 C1=PASS` ×3.
- `FN3-mixed`: a symlinked `spans` dir is refused (exit 2), symlinked `spans.tsv` and span files are replaced.
  `H10 rc=2`, `H11 rc=0`, `H12 rc=0`. `LEGS=20/20 C1=PASS` ×3.

Baseline harness check: `ref-build-spans.py` at seed 61001 gives `LEGS=20/20 C1=PASS` (`Wall time: 2.40 seconds`),
matching `controls/c1-reference.txt`.

**Calibration.** The three FP builders each reach a PASS on the whole counter, not only on their leg. The C1 PASS
verdict therefore does not discriminate transient writes through links. F3 shows the legs are not over-strict for
correct policies. The H10–H12 legs do not discriminate a restored write, nor a refusal that leaves output.
Not run: whether the landed `tools/build-spans.py` shares these patterns (outside this seat's item).

**Out of item scope, not run (INFERENCE).** H13 OUTSIDE (`c1-count.py:462-468`) checks only that the marker is absent
from output; a builder that reads through the cache link and then refuses for an unrelated reason would also pass.
Routed for whichever seat owns H13.

## Candidates (scratch deleted; reproducible from the reference by these edits)
- `FN1-replace`: guard_out drops the sd/m/span-link refusals (keeps `not sd.is_dir()` for real non-dir);
  `differs` excludes links; write_out unlinks `out/spans` when it is a link before `mkdir`.
- `FN2-exit1-order`: m-link check then sd-link check, both `print` + `return 1, None`; span-link refusal returns 1.
- `FN3-mixed`: reference sd refusal kept; m-link and span-link handled as FN1.
- `FP1-rollback-dir`: guard refuses only non-directory sd; write_out saves victim files, writes through, removes new
  names, restores bytes+mtime, returns 2.
- `FP2-rollback-file`: write_out saves link targets, writes through `write_bytes` for linked span files, restores, returns 2.
- `FP3-samebytes-file`: guard accepts a linked m if `is_file()`; write_out writes manifest through the link, restores mtime, returns 2.
Working path deviation: counter runs used `$S/w/<name>-<seed>` (distinct per run) rather than a single `w`.

## Not claimed
No change to the frozen counter, predicate, controls or targets. No fix proposed here; routed to L1 as counter
defects F1 (three legs) and F2 (refusal state not checked on H10–H12). No external fetch, no network.

VERDICT: LEG_DEFECTS=3 false_negative=0 false_positive=3 legs=H10 SPANSLINK, H11 FILELINK, H12 TSVLINK
