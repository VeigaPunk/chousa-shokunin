# R55W2ExecC3Rerun — attack on the R55-C3 after-state

Seat: leaf executor. Scratch `$S=/fast/scratch/hyaku/chousa-r56/R55W2ExecC3Rerun` (`TMPDIR` there, `PYTHONDONTWRITEBYTECODE=1`, removed at exit). Lane write: this file only; no production file, no git/jj mutation, no PATH write, no network, no install (pacman paused; soffice 26.8.1.1 present). C3 = the eleven anchored errata E01–E11 (`corpus/evidence/round55/claims.md` § R55-C3); predicates attacked, never edited.

## Counted tree (the commit the seat names)

```
$ git -C chousa-shokunin cat-file -e 29cfb12abd70f688b48c0d17f31e636f2d81104a && echo REV_OK
REV_OK
$ git -C chousa-shokunin archive 29cfb12abd70f688b48c0d17f31e636f2d81104a | tar -x -C $S/lane
$ git show 29cfb12:corpus/evidence/round55/c3-count.py | sha256sum ; sha256sum corpus/evidence/round55/c3-count.py
c829e1c2d1c47d02b420247d8832823cb72fcadeb1479dc8b4f3355e6b0ad281  -
c829e1c2d1c47d02b420247d8832823cb72fcadeb1479dc8b4f3355e6b0ad281  corpus/evidence/round55/c3-count.py
$ git -C chousa-shokunin diff --stat 29cfb12 HEAD -- corpus/evidence/round55/c3-count.py corpus/evidence/round55/controls/build-c3-controls.py corpus/QUALITY.md corpus/lessons/round-54.md corpus/knowledge/source-type-taxonomy-r36.md SCORECARD.md
 SCORECARD.md | 31 +++++++++++++++++++++++++++++++
```

The only hunk is `@@ -2794,3 +2794,34 @@` — appended after the errata block (that section is the last section at 29cfb12, heading `SCORECARD.md:2780`), so HEAD counts the same bytes. `--root $S/lane` keeps the measurement on the frozen after-state, not the live tree.

## A. Full run, E11 included (`--work` empty)

```
$ python3 corpus/evidence/round55/c3-count.py --root $S/lane --work $S/work/full
E01 OK
E02 OK
E03 OK
E04 OK
E05 OK
E06 OK
E07 OK
E08 OK
E09 OK
E10 OK
E11 OK
ERRATA=11/11 MISSING=0 ANCHOR=0 WRONG=0
C3=PASS
exit=0
```

Identical to the round-55 receipt `corpus/evidence/round55/c3-measure-after.txt`. E11 ran the BASE supplement with soffice under a private profile inside the work dir (`$S/work/full/supp/soffice-profile`); afterwards `pgrep -af soffice.bin | grep R55W2ExecC3Rerun` → none, no `soffice.bin` left.

## B. `--skip-slow` (E11 skipped, cannot pass)

```
$ python3 corpus/evidence/round55/c3-count.py --root $S/lane --work $S/work/skip --skip-slow
E01 OK … E10 OK
E11 WRONG (slow item skipped)
ERRATA=10/11 MISSING=0 ANCHOR=0 WRONG=1
C3=FAIL
exit=1
```

As documented: `obs["E11"] = None` (`c3-count.py:189`) prints WRONG with the `(slow item skipped)` suffix (`c3-count.py:253`) — FAIL, not exit 2.

## C. Controls rebuilt and scored against `controls/c3-controls.txt`

```
$ python3 corpus/evidence/round55/controls/build-c3-controls.py $S/c3c
restate paraphrase
$ python3 corpus/evidence/round55/c3-count.py --root $S/c3c/restate --work $S/work/rb-restate
E01 WRONG … E11 WRONG
ERRATA=0/11 MISSING=0 ANCHOR=0 WRONG=11
C3=FAIL
exit=1
$ python3 corpus/evidence/round55/c3-count.py --root $S/c3c/paraphrase --work $S/work/rb-paraphrase
E01 ANCHOR … E11 ANCHOR
ERRATA=0/11 MISSING=0 ANCHOR=11 WRONG=0
C3=FAIL
exit=1
$ diff <(grep -E '^(E[0-9]+ |ERRATA=|C3=|exit=|## )' corpus/evidence/round55/controls/c3-controls.txt) \
       <(grep -E '^(E[0-9]+ |ERRATA=|C3=|exit=|## )' $S/c3-controls-rebuilt.txt) && echo IDENTICAL
IDENTICAL
```

RESTATE (the lane's own claim as observation) is WRONG on all eleven — the observation is derived, not copied from lane prose; PARAPHRASE dies on `ttext.count(anchor) != 1` before comparison.

## D/E. SCORECARD placement: stray outside ignored, in-section last-wins governs

Wrong line `erratum: E05 corpus/QUALITY.md anchor: "11,972 / … / 25,123" observed: "located=1,2,3,4,5,6 drift=+0,+0,+0,+0,+0,+0"` inserted (D) just before `SCORECARD.md:2780`, still inside `## Planned — round 55` (E05 lines then at 2780 and 2790), and (E) at 2789 immediately after the real E05 at 2788.

```
$ python3 corpus/evidence/round55/c3-count.py --root $S/lane-out --work $S/work/out
E01 OK … E05 OK … E11 OK
ERRATA=11/11 MISSING=0 ANCHOR=0 WRONG=0
C3=PASS
exit=0
$ python3 corpus/evidence/round55/c3-count.py --root $S/lane-lastwins --work $S/work/lastwins
E01 OK … E05 WRONG … E11 OK
ERRATA=10/11 MISSING=0 ANCHOR=0 WRONG=1
C3=FAIL
exit=1
```

D: `errata()` accepts lines only while `inside` the heading (`c3-count.py:206-218`). E: last-wins is the dict overwrite `out[m.group(1)] = …` (`c3-count.py:217`).

## F. Two added clause probes — anchor-key and target clauses

```
$ python3 corpus/evidence/round55/c3-count.py --root $S/lane-nokey --work $S/work/nokey
E01 OK … E05 ANCHOR … E11 OK   ERRATA=10/11 ANCHOR=1 WRONG=0   C3=FAIL   exit=1
$ python3 corpus/evidence/round55/c3-count.py --root $S/lane-tgt --work $S/work/tgt
E05 ANCHOR                     ERRATA=10/11 ANCHOR=1           C3=FAIL   exit=1
```

`lane-nokey` swaps E05's anchor for one occurring exactly once in `QUALITY.md` but lacking the key phrase (`it is not the document (the \`.txt\` sidecar holds none of the six phrases`, count 1); `lane-tgt` names `corpus/lessons/round-54.md` as E05's target. Both rejected, so the target and key-phrase clauses hold independently of the observation clause.

## Findings, risks, blockers

- No falsification: after-state `11/11 PASS` at 29cfb12; both committed controls reproduced line-for-line from a fresh build.
- Last-wins (E) is the frozen rule but a silent failure mode: a later good-or-bad `erratum:` line supersedes silently; the section boundary (D) is the only guard and works.
- A WRONG never prints the expected observation (`c3-count.py:253` prints verdicts only), so an operator cannot diagnose one without reading the counter — an operability limit, not a count flaw.
- E11 is host-dependent: without soffice the counter exits 2 (`ENV_CHANGED`), not FAIL (unexercised — soffice present). Every run used a fresh empty `--work`; scratch removed; only this report written. Blockers: none.

VERDICT: attacked the R55-C3 after-state (11/11 PASS at 29cfb12, `--skip-slow` FAIL, controls byte-identical, out-of-section stray ignored, in-section last-wins and the anchor-key/target clauses all behaving) — survived; no defect found.
