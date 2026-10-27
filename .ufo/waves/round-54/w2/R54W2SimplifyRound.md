# R54W2SimplifyRound — YAGNI review of round 54's landed bytes

Seat: leaf simplifier, wave 2 (FALSIFY). Read-only on the lane; every deletion was made in a
scratch copy and the affected command rerun there.

Scratch: `/fast/scratch/hyaku/chousa-r54/R54W2SimplifyRound/` (removed before this report).
`S=/fast/scratch/hyaku/chousa-r54/R54W2SimplifyRound`; lane copy `$S/lane` (`cp -a`), `TMPDIR=$S`,
`PYTHONDONTWRITEBYTECODE=1` on every run. Shared tree: `git rev-parse HEAD` at start `178667d`;
the four scripts I read hash the same at the end (`sha256sum … | diff - $S/digests.txt` →
`SHARED DIGESTS UNCHANGED`); the only lane writes are other seats' reports plus this file.

Reviewed surface: `git diff --stat c49ffc6 c49ffc6->447cf7e` = `79 files +5828 -4`; the new files
under `corpus/evidence/round54/` (58 tracked) and `git diff … -- tools/capture-text.py` (+304).

## Reproduced baseline (before any deletion), in `$S/lane`

```
c1-count.py --seed 54 --per-leg 2      -> LEGS=6/6 C1=PASS exit=0   (REGRESS: r52 LEGS=9/9, SUPPLEMENT_LEGS=4/4)
c1-supplement.py --seed 54 --per-leg 2 -> ISOLATED/RESAVE/HELDOUT PASS  SUPPLEMENT_LEGS=3/3 exit=0
c2-count.py                            -> ENTRIES=2/2 BOUND=3/3 QUOTE_ROWS=33/33 CAPTURE_BOUND=33/33
                                          SUBSTANCE=PASS ANCHOR_BOUND=3/3 C2=PASS exit=0
build-spans.py --check                 -> SPANS_ROWS=33 STALE=0 exit=0
considerthese-ledger-check.py --root . -> PROPOSALS=35 ROWS=35 IMPL=24 FMT=9 OPEN=1 OPS=1 BAD=0 exit=0
tracked-deletion-check.py              -> TRACKED_DELETION=PASS exit=0
round53/pointer-anchor-check.py --root . -> ANCHORED=16/16 UNANCHORED=0 BAD=0 exit=0
```

`pdf-crosscheck.py` was NOT run: `python3 -c "import pypdf"` → `ModuleNotFoundError`; the only
install path is `uv run --with pypdf` (network). Nothing below depends on it.

## 1. The one deletion that holds — a dead statement in the forge control

`corpus/evidence/round54/controls/build-c1-forge.py` line 40 of the emitted tool:

```python
    sys.argv = [sys.argv[0]] + sys.argv[1:]; sys.exit(ct.main())
```

The assignment is `sys.argv` rebuilt from itself — an identity. Deleted in scratch (one line, the
only diff), rebuilt and scored:

```
$ diff corpus/evidence/round54/controls/build-c1-forge.py corpus/evidence/round54/controls/build-c1-forge-nop.py
40c40
<     sys.argv = [sys.argv[0]] + sys.argv[1:]; sys.exit(ct.main())
>     sys.exit(ct.main())
$ python3 corpus/evidence/round54/controls/build-c1-forge-nop.py $S/forge-nop
$ python3 corpus/evidence/round54/c1-count.py --tool $S/forge-nop/forge.py --seed 54 --per-leg 2
GEN/NONWORD/ENCRYPTED/MALFORMED/REAL/REGRESS=PASS   LEGS=6/6  C1=PASS  exit=0
```

Baseline forge (`$S/forge-base/forge.py`, sha256 `6fed5af7…`) also scored `LEGS=6/6 C1=PASS exit=0`.
Same 6/6, one statement fewer → deletion admitted. Draft (intended lane path
`corpus/evidence/round54/controls/build-c1-forge.py`, BODY line 40):

```python
-    sys.argv = [sys.argv[0]] + sys.argv[1:]; sys.exit(ct.main())
+    sys.exit(ct.main())
```

Nothing else in the builder or its body is removable: `pyflakes` on the builder and on the
extracted body → no output (no unused import on either side). `vulture --min-confidence 40` over
all round-54 scripts → only `c1-count.py:42: unused import 'os'` (see §6).

## 2. Falsified: "duplicate receipts"

Receipts that no script names (grep of every round-54 `.py` for the file name):
`c1-after-candidate.txt`, `census-start.txt`, `census-end.txt`, `measure-after.txt`,
`controls/{c1-before,c1-controls,c1-forge,c2-before,c2-controls}.txt`. Deleted all nine, reran
every command above: output byte-identical (`diff a.txt b.txt` → `SWEEP OUTPUTS BYTE-IDENTICAL`),
so no counter or check reads them. But each is cited as evidence, so none is dead text:
`c1-after-candidate.txt` by `corpus/lessons/round-54.md:21` and `measure-after.txt` by erratum E1 —
deleting either leaves a dangling citation in a frozen document. `census-*.txt` by
`corpus/lessons/round-54.md:111`. Verdict: retain (provenance, not weight).

The dumps are the opposite case — they look like duplicates of the cache `.raw` but are live check
inputs:

```
$ mv corpus/evidence/round54/S101-text-form.txt $S/S101.bak; python3 corpus/evidence/round53/pointer-anchor-check.py --root .
BAD_ANCHOR corpus/SOURCES.md:111 char11170->char11972 -> corpus/evidence/round54/S101-text-form.txt … occurrences=0   (×6)  exit=1
```
(16/16 → 6 BAD.) Not deletable. `corpus/evidence/round54/__pycache__` is gitignored
(`git check-ignore -v` → `.gitignore:3`), so it is not landed bytes.

## 3. Falsified: "dead code paths in the supplement"

`c1-supplement.py`: `pyflakes` and `vulture` clean; every import (argparse, hashlib,
importlib.util, pathlib, random, re, shutil, subprocess, sys, tempfile) is used; no unreachable
branch found. The one line that looks redundant — the resave-changed guard, which the later
`len(docs) != len(F.REAL)` exit-2 would also catch — is the ONLY discriminator against a
copy-through "resave". Probe with a stub `Ctx.soffice` that copies the pinned bytes into the resave
dir (oracle = the tool's own output, so the stub is circular and only the guard can fire):

```
guard    -> (False, 'r54fe0734.doc resave kept the pinned bytes')
noguard  -> (True,  '5 resaved captures')
```
Deleting it makes RESAVE pass on the very shortcut the supplement exists to close. Retain.
The `judge()` copy of the REAL line/ratio rule is forced: `c1-count.py`'s `leg_real` has no
callable the supplement could import, and the counter is frozen. No deletion.

## 4. Falsified: "the ledger's pass-through columns"

`considerthese-ledger.tsv` is `id status pointer note`. The checker reads `id`, `status` and
`pointer` (IMPL only) and drops `note` (`i, st, ptr, _ = r`), enforcing only arity:

```
drop column 4        -> FAIL COLUMNS ×35 … PROPOSALS=35 ROWS=35 IMPL=0 FMT=0 OPEN=0 OPS=0 BAD=35 exit=1
notes all "-"        -> PROPOSALS=35 ROWS=35 IMPL=24 FMT=9 OPEN=1 OPS=1 BAD=0 exit=0
non-IMPL pointer bogus -> PROPOSALS=35 ROWS=35 IMPL=24 FMT=9 OPEN=1 OPS=1 BAD=0 exit=0
```
So `note`'s content and the 11 non-IMPL `pointer` cells are carried but never read — the
`COLUMNS` arity rule is the only thing holding the column, and dropping it is a check change.
Retain; this is the round's one place where data no check reads is carried deliberately (the notes
are the only record of *why* a proposal is FMT/OPEN).

## 5. Falsified: "the round's copies are duplicate authorities"

- `build-spans.py` vs `corpus/evidence/round52/build-spans.py`: exactly four hunks, all docstring or
  path (`242c242 < …"round52" > …"round54"`). The copy is load-bearing, because the builder it came
  from cannot serve this round: `python3 corpus/evidence/round52/build-spans.py --root $S/lane --check`
  → `SPANS_ROWS=39 STALE=0` (it reads round 52's own `quotes.tsv`; round 54 has 33 rows). The copy
  is also the lane convention — `ls corpus/evidence/round{45,46,47,49,50,51,52,53,54}/build-spans.py`
  all exist. A loader/shim would couple round 54's re-derivation to a file another round may edit.
  Retain.
- `pdf-crosscheck.py` vs round 53's: docstring, one import (`unicodedata`), the `DOCS` map and the
  NFKC fold — a different check, not a copy.

## 6. Dead but frozen (named, not touched)

- `c1-count.py:42 import os` — unused at module level (`pyflakes`; the HOOK string imports its own
  `os`). The counter's digest `633430a4…` is pinned by W1 `R54ReviewC1Counter.md:56`, so an edit
  breaks a committed receipt. Retain.
- `c2-count.py` `ALIASES: dict[str, str] = {HIT: HIT}` — a single-entry identity map used only in
  `theme.update({url_of(k): v for k, v in ALIASES.items()})`. Replaced in scratch by
  `theme[url_of(HIT)] = HIT`: `diff $S/c2-baseline.txt $S/c2-noalias.txt` → `OUTPUT IDENTICAL`
  (`C2=PASS`). Inert, but the counter is frozen. Retain.
- `c2-count.py` `HELD = {HIT: "S101"}` — same shape, but genuinely read (`for url, hid in HELD.items()`).

## 7. The tool's unexercised OLE lines — refusal edges, not dead code

`settrace` over 15 inputs (5 pinned `.raw` incl. the byte twin, both fixtures, 2 GEN, 2 ENCRYPTED,
2 MALFORMED, 2 `.xls`): `OLE_REGION=130-388 MISSING=47`. Every missing line is a `raise Refused`,
a bare `else:`, or one of these substantive branches: the DIFAT chain extension (157–162 — no
capture has >109 FAT sectors or a shift-12 header), `deleted_runs`' `lcb == 0` return (248), the
variable-length sprm path in `marks_deleted` (273–276), the `except struct.error` handler (309), the
Prc-skip loop (318–323 — so the E2 `Prc GrpPrl outside the Clx` bound is reached by no input the
round can produce, extending E2/W1 F2), the CP-decrease and piece-bounds refusals (343–357), and
`0x1E → "-"` (382). Each is promised in the docstring; deleting one buys ≤8 lines and costs a wrong
answer or a crash on real Word files. Retain all.

## 8. Traps for the next seat (not weight)

- `build-c1-forge.py` resolves `LANE = HERE.parents[3]` and bakes it into the tool as
  `LANE_TOOL`. I first copied the builder to `$S/` to edit it; the rebuilt forge then scored
  `LEGS=0/6` with `FileNotFoundError: '/fast/tools/capture-text.py'` — a false negative caused by
  depth, not by the edit. Copy the builder only inside `corpus/evidence/round54/controls/`.
- The forge digest in `controls/c1-forge.txt` (`f73ac5c…`) does not reproduce here: two builds now
  are byte-identical (`cmp` → identical, `6fed5af…`, 6/6) and the builder is unchanged since the
  receipt (`git log --oneline -- controls/build-c1-forge.py` → one commit, `6af11e9`), so only the
  CANNED LibreOffice exports made at build time can differ `[INFERENCE]`. Do not read the forge
  digest as reproducible; read the 6/6.

## Preserved contract

Frozen predicates, targets, counters, controls and the nine anchored corrections untouched: the
sweep in §Reproduced baseline and the after-deletion sweep are identical, `c2-count.py` is
byte-identical, and `c1-count.py`/`c2-count.py`/`controls/` are unchanged on disk
(`SHARED DIGESTS UNCHANGED`). The single admitted deletion changes no counter, check or claim
output and is confined to post-freeze E1 material.

VERDICT — attacked 79 files of round-54 landed bytes for deletable weight (receipts, supplement
paths, forge imports/statement, ledger columns, per-round copies, OLE branches): one 1-line
dead statement in `build-c1-forge.py` is deletable with 6/6 preserved; every other hypothesis was
falsified by deletion + rerun (nine receipts are citation-load-bearing, the S101 dump feeds
`pointer-anchor-check`, the resave guard and the ledger column arity are load-bearing, the
build-spans copy is the lane convention, and the 47 unexercised OLE lines are docstring-promised
refusals) — the round's weight survived.
