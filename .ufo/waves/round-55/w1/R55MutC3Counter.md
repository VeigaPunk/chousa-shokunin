# R55MutC3Counter — mutation test of the frozen C3 counter

Seat: R55MutC3Counter · lane chousa · round 55 wave 1 · BASE_REV `dba605deb5cd5ed4874e0e3c39ba24737409cd80`
Target under test: `corpus/evidence/round55/c3-count.py` (frozen; never edited — every run of the
"frozen" column executed the lane's own file, sha256 `c829e1c2d1c47d02b420247d8832823cb72fcadeb1479dc8b4f3355e6b0ad281`).
Mutants lived only in the fixture clone `fix/` (parents[3] of the mutant path resolves to a clone
holding BASE_REV, so `git_show`/`git archive` work); scratch `$S=/fast/scratch/hyaku/chousa-r55/R55MutC3Counter`.

Detector per run: `python3 <counter> --root $S/rootN --work <fresh empty dir> --skip-slow`.
`--skip-slow` on every run (mutant AND frozen): no mutant exercises E11 (observation None → the
counter's own doc: skip "can never print C3=PASS"). Discriminator = per-item verdict + ERRATA line.
Every root omits the E11 line entirely → E11 is `MISSING` in both columns everywhere; a mutant
"passes" = ERRATA=10/11 MISSING=1 with the crafted defect judged OK.

## Harness evidence

Observations were taken from the counter's own `observe(work, False)` (frozen module loaded
importlib, work=$S/obswork, slow=False — no soffice anywhere in this seat):
E01 `该标准暂无全文，请等待更新 count=1 char=1712` · E02 `…char=569` ·
E03 `附录 S121=0 S122=0; 文献类型 S121=0 S122=0` · E04 `国家标准委 S121=2 S122=2` ·
E05 `located=11972,12007,12795,12963,14049,25123 drift=+802,+802,+802,+802,+802,-9251` ·
E06 `C0=18451 C0_excl_tab_lf=18431 C0_excl_tab_lf_cr=18242` · E07 `form_C0=469 form_LF=469` ·
E08 `ANCHORED=7/16 UNANCHORED=9 BAD=9` · E09 `ctypes_system_under_hook rc=0 marker=SPAWNED` ·
E10 `SHELL LEGS=1/6` · E11 `None`.
Anchors = each item's key phrase verbatim; asserted `ttext.count(anchor)==1` in the BASE target
(builder `build_roots.py` also re-parses every root with the frozen `errata()` before runs).

Baseline (frozen on root0, all 10 lines correct): `E01..E10 OK, E11 MISSING`,
`ERRATA=10/11 MISSING=1 ANCHOR=0 WRONG=0`, `C3=FAIL` rc=1 — errata craft is valid; only E11 absent.

## Mutant table (check removed → shortcut in rootN → frozen / mutant)

| # | check removed (frozen line) | mutant sha256 | shortcut | frozen verdict | mutant verdict |
|---|------------------------------|---------------|----------|----------------|----------------|
| M1 | `keyp not in anchor` (l.249) | `b41a622a73410e3a` | root1: E01 anchor = `the document-type taxonomy the standard prescribes` (unique in r36, lacks key phrase) | `E01 ANCHOR` → `ERRATA=9/11 MISSING=1 ANCHOR=1` rc=1 | `E01 OK` → `ERRATA=10/11 MISSING=1` rc=1 |
| M2 | `ttext.count(anchor) != 1` (l.249) | `3b0cda8187014d1d` | root2: r36 copy appended `count 1 each, on one line` → E04 anchor occurs 2× | `E04 ANCHOR` → `ERRATA=9/11 MISSING=1 ANCHOR=1` rc=1 | `E04 OK` → `ERRATA=10/11 MISSING=1` rc=1 |
| M3 | `tgt != target` (l.249) | `91636897131830a4` | root3: E05 line names `corpus/lessons/round-54.md`; anchor `12,963 / 12,795` still unique in QUALITY.md, observed correct | `E05 ANCHOR` → `ERRATA=9/11 MISSING=1 ANCHOR=1` rc=1 | `E05 OK` → `ERRATA=10/11 MISSING=1` rc=1 |
| M4 | scoping `if inside` (l.215) | `995bac6e8cfa67b4` | root4: correct E08 line parked under decoy `## Wave 55 minutes (decoy)` before the real section | `E08 MISSING` → `ERRATA=9/11 MISSING=2` rc=1 | `E08 OK` → `ERRATA=10/11 MISSING=1` rc=1 |
| M5 | last-wins → `if m.group(1) not in out` first-wins (l.217) | `eedc1f5b75312c79` | root5: two E10 lines — correct, then `observed: "SHELL LEGS=decoy"` (last must govern) | `E10 WRONG` → `ERRATA=9/11 MISSING=1 WRONG=1` rc=1 | `E10 OK` → `ERRATA=10/11 MISSING=1` rc=1 |

All five mutants KILLED: each passes its crafted defect where the frozen counter fails it
(item-level flip, identical observed/anchor bytes otherwise).

## Incidental finding (no coverage gap)

M3's first shortcut — anchor planted in the *named* file instead of the canonical target — failed
BOTH columns (`E05 ANCHOR` under the mutant too), because the count check reads `root / target`,
never `root / tgt`. The exploitable wrong-target defect is therefore a *mislabeled `tgt` field*
(the anchor still unique in the correct file); the frozen `tgt != target` check kills exactly that.
Also noted: BASE SCORECARD l.1434 contains `Packaging erratum: …` — does not match
`^erratum: (E\d\d) `, so it parses in neither column; M4's unscoped match was verified clean on it.

## Restoration / integrity evidence

`sha256sum`: pristine copy `c829e1c2d1c47d02` = lane file `c829e1c2d1c47d02`; after all mutants the
fixture file was restored via `cp` → `c829e1c2d1c47d02` (three equal hashes observed).
Restored-bytes rerun on root0 reproduced the lane-frozen baseline verbatim
(`ERRATA=10/11 MISSING=1`, rc=1). `git -C lane status --porcelain -- corpus/evidence/round55/c3-count.py` → empty.
Lane file, shokuknow, fleet root: read-only ops only (clone, archive, show, status; no fetch/commit/push).
Fixture rev-parse asserted `$S/fix` before any worktree touch. No tooling installed or upgraded.

VERDICT: attacked the frozen C3 counter's five checks via five single-line mutants on a fixture
clone — all KILLED (each mutant's crafted defect flips the target item to OK where frozen fails it);
no coverage finding; frozen counter semantics hold (canonical-target counting, last-line-wins,
section scoping, key-phrase and uniqueness checks all load-bearing).
