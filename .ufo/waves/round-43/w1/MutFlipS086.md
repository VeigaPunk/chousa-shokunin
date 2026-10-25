# MutFlipS086 — C2 flip probe

Seat: MutFlipS086 (mutation-tester, leaf).
Axes: operability, calibration, depth. This probe scores calibration (R43-C2).
Milestone: Round 43: attack the frozen absent-class split and the one local adoption.
Measured commit named by the wave: `737f40b6aa8f37ffe2269db370fd6d65a720d9a8`.
No lane production file, git index, or sibling tree was written. No network. No install.

## Mutant

Smallest behavior-bearing point: the in-process label swap in `corpus/evidence/round43/c2-count.py` (`--flip`), applied only to id S086. Committed row is `not-carried`; the flip rewrites that one label to `misquote` before grading. The swap is not written back.

Committed row (unchanged):

```
S086	not-carried	4	46	0.086957	2
```

Detector invocation (assigned probe, and only disk-touching command against the table is a read):

```
python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round43/c2-count.py --flip S086
```

The table was not edited. The 1/2 bound was not retuned. A surviving mutant would be a coverage finding, not permission to change R43-SPLIT.

## Expected detector

Frozen kill (`corpus/evidence/round43/claims.md`, C2): `--flip S086` must print `SPLIT_AGREES=14/15` and exit 1.

Committed control `corpus/evidence/round43/controls/c2-control-before.txt` (stdout only, no exit line):

```
SPLIT_AGREES=14/15
VOCAB_OK=15/15
MISMATCHES=1
MISMATCH S086 table=misquote independent=not-carried
C2=FAIL
```

Baseline (no flip) must not already fail, or the mutant result is inconclusive.

## Output

Pristine detector, same command without `--flip`:

```
SPLIT_AGREES=15/15
VOCAB_OK=15/15
MISMATCHES=0
C2=PASS
PRISTINE_EXIT:0
```

Mutated detector (`--flip S086`), verbatim:

```
SPLIT_AGREES=14/15
VOCAB_OK=15/15
MISMATCHES=1
MISMATCH S086 table=misquote independent=not-carried
C2=FAIL
MUTATED_EXIT:1
```

An earlier run of the same flip command, before the hashed sequence, printed the same five stdout lines and exited 1.

Restored detector (no flip, after the probe):

```
SPLIT_AGREES=15/15
VOCAB_OK=15/15
MISMATCHES=0
C2=PASS
RESTORED_EXIT:0
```

## Verdict

**killed.**

Baseline passed (`SPLIT_AGREES=15/15`, exit 0), so the flip failure is not a baseline failure and is not inconclusive. The mutant moved one label off the independent class (`table=misquote`, `independent=not-carried`) and the counter dropped to `SPLIT_AGREES=14/15` with exit 1. That matches the frozen kill and the control file byte-for-byte on stdout. Vocabulary stayed `VOCAB_OK=15/15`; the miss is agreement, not an out-of-vocab label. Contract unchanged.

## Restoration evidence

`--flip` mutates the in-memory row list only. Before and after sha256:

```
bba7d8b6b5165cd4d5b21c9b9c9e9275ecb26839ad8764d8db8b4ffebc001a58  corpus/evidence/round43/absent-split.tsv
5cbfe2f1127b50ae894bc48027ba119ca4eaf67fadc88251299512629bc9ba43  corpus/evidence/round43/c2-count.py
```

Both hashes are identical before and after the probe. Restored detector output equals the pristine output. No scratch copy was left behind. Stop after this probe.

Report: .ufo/waves/round-43/w1/MutFlipS086.md
