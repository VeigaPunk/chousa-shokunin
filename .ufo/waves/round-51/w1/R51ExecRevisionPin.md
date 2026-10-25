# R51ExecRevisionPin — routed defect 1: the round-50 measurement pinned to its landed tip
axes: calibration (QUALITY 58) · operability (re-run recipe). Scratch `/dev/shm/chousa-r51-R51ExecRevisionPin/` (removed). No install, no network, no lane write.
## 1. The named revision, and why a bare export cannot measure it
```
$ git -C /home/vgpnk/Projects/shokunin/chousa-shokunin log -1 --format='%H %s' 1d7aba0948cf62f6158f77e220f64320a5b6c6cc
1d7aba0948cf62f6158f77e220f64320a5b6c6cc round-50: wave-2 narrowing of the three entries, supplementary C1 check, hardened checks, erratum, LOG, SCORECARD, final measurement, W2 seat reports
$ git -C /home/vgpnk/Projects/shokunin/chousa-shokunin archive 1d7aba0948cf62f6158f77e220f64320a5b6c6cc | tar -x -C /dev/shm/chousa-r51-R51ExecRevisionPin/tree
$ cd /dev/shm/chousa-r51-R51ExecRevisionPin/tree && for s in c1-count c2-count c1-supplement stale-count-check; do echo "=== $s"; python3 corpus/evidence/round50/$s.py; echo "exit=$?"; done
=== c1-count
SELFTEST_DEFAULT=PASS
BASELINE=PASS rc=0 findings=26
(elided: P1-P6 all `applied=1 rc=1 -> PASS`, PERTURB_PASS=6/6, EXPECTED_BAD=PASS rc=2 — as in the receipt)
R49_REGRESSION=FAIL rc=2
LEGS=4/5
C1=FAIL
exit=1
=== c2-count
NO_BASE_OR_REGISTER
exit=2
=== c1-supplement   -> SUPPLEMENT_LEGS=5/5, C1_SUPPLEMENT=PASS, exit=0 (all legs as in the receipt)
=== stale-count-check -> STALE_HITS=8 UNRESOLVED=0 RECEIPT_ROWS=31, STALE_COUNT=PASS, exit=0 (all RESOLVED lines as in the receipt)
```
Cause, read from the files: `round50/c1-count.py:45,49,137-138`, `round50/c2-count.py:51,139` and `round49/c1-count.py:46,366` set `LANE = pathlib.Path(__file__).resolve().parents[3]` and run `git -C <LANE>` (`show 3c51da77…:corpus/SOURCES.md`, `archive 414a2ec6… corpus`, `grep … BASE_REV`). An export has no `.git`, so c2 exits 2 `NO_BASE_OR_REGISTER` and c1's `R49_REGRESSION` exits 2. A clone is measurable:
`git clone --no-hardlinks -q <lane> repo && git -C repo checkout -q 1d7aba0…` → `rev-parse HEAD` = `1d7aba0948cf62f6158f77e220f64320a5b6c6cc`, `status --porcelain | wc -l` = `0`, `diff -r --brief tree repo -x .git` silent (`$?`=0), 14678 files each.
## 2. The pinned measurement — draft receipt
```text
intended lane path: corpus/evidence/round51/measure-r50-at-tip.txt  (append-only; this label is not part of the receipt — the receipt starts at the `measured-at:` line)
measured-at: 1d7aba0948cf62f6158f77e220f64320a5b6c6cc
tree: clone of the lane at that revision, clean (`git status --porcelain` empty), byte-identical to `git archive 1d7aba0948cf62f6158f77e220f64320a5b6c6cc | tar -x` (`diff -r --brief` silent; 14678 files each)
tool: tools/assimilate-rows.py sha256=382aca9b7e314180ece70a9e1b34fc8622dbfaedf29f9d3efd51df1a94778cb5 (the round-50 tool; HEAD's is bdaf80f4… after 2a3389d)
limit: an export alone is not measurable — round50/c2-count.py:51,139 and round49/c1-count.py:46,366 run `git -C <parents[3]>`, so in a bare export c2 prints NO_BASE_OR_REGISTER exit 2 and c1's R49_REGRESSION exits 2

$ python3 corpus/evidence/round50/c1-count.py
SELFTEST_DEFAULT=PASS
BASELINE=PASS rc=0 findings=26
PERTURB P1 applied=1 rc=1 -> PASS
PERTURB P2 applied=1 rc=1 -> PASS
PERTURB P3 applied=1 rc=1 -> PASS
PERTURB P4 applied=1 rc=1 -> PASS
PERTURB P5 applied=1 rc=1 -> PASS
PERTURB P6 applied=1 rc=1 -> PASS
PERTURB_PASS=6/6
EXPECTED_BAD=PASS rc=2
R49_REGRESSION=PASS rc=0
LEGS=5/5
C1=PASS
exit=0

$ python3 corpus/evidence/round50/c1-supplement.py
P7_NONCE_EXCLUSIVE=PASS
H1_DUPLICATE_EXPECTED=PASS
H2_NO_ENTRY=PASS
H3_OPTION_CLASH=PASS
H4_ENTRYCITES_DASH=PASS
SUPPLEMENT_LEGS=5/5
C1_SUPPLEMENT=PASS
exit=0

$ python3 corpus/evidence/round50/c2-count.py
ENTRIES=3/3
BOUND=3/4 (min 3) REFUSED=1
BOUND_IDS=S104,S105,S106
REF_ID_UNBOUND=0
NEW_GROUND=3/3
QUOTE_ROWS=67 ON_BOUND=67/67
SPAN_IDS=3/3 (min 3 each)
QUOTES_IN_SPAN=67/67
QUOTES_IN_ENTRY=67/67
QUOTES_IN_LESSON=67/67
QUOTE_SHORT=67/67
SPAN_CONTEXT=67/67
CAPTURE_BOUND=67/67
SUBSTANCE=PASS
ANCHOR_BOUND=3/3
INFERENCE_GROUNDED=3/3
QUARANTINE_VERDICTS=0/0 ()
QUARANTINE_BLOCKED_ADOPTED=0
C2=PASS
exit=0

$ python3 corpus/evidence/round50/stale-count-check.py
RESOLVED corpus/QUALITY.md:746 says 28, receipt 31
RESOLVED corpus/QUALITY.md:786 says 28, receipt 31
RESOLVED corpus/README.md:1074 says 28, receipt 31
RESOLVED corpus/README.md:1083 says 28, receipt 31
RESOLVED LOG.md:1803 says 28, receipt 31
RESOLVED LOG.md:1821 says 28, receipt 31
RESOLVED corpus/lessons/round-49.md:20 says 28, receipt 31
RESOLVED corpus/lessons/round-49.md:220 says 28, receipt 31
STALE_HITS=8 UNRESOLVED=0 RECEIPT_ROWS=31
STALE_COUNT=PASS
exit=0
```
## 3. diff against `corpus/evidence/round50/measure-after.txt` — zero differing lines
```
$ awk '/^\$ python3 corpus\/evidence\/round50\/c1-count\.py$/{f=1} /^\$ python3 corpus\/evidence\/round50\/cjk-ground-check\.py/{f=0} f' measure-after.txt > after-slice.txt   # 82 lines; tip-slice.txt is 82 too (`wc -l`)
$ diff -u after-slice.txt tip-slice.txt ; echo diff_rc=$?
diff_rc=0
```
Compared blocks: `c1-count`, `c1-supplement`, `c2-count`, `c2-count --lane-only` (run too; identical), `stale-count-check`. Per-block `difflib.unified_diff`: `IDENTICAL` for each of the four named commands. Differing lines: **none**. Not compared (outside this item): `cjk-ground-check`, `decode-form-check`, `build-spans --check`, `quote-substance-check`, `round47 c2-count --list`, `sources-census.sh`, `grep -cE rows`. `measure-after.txt:1` itself says "at the working tree before the final commit" — the sentence this receipt closes.
## 4. Falsifier — the same command, a second truth at HEAD
```
$ cd /home/vgpnk/Projects/shokunin/chousa-shokunin && git rev-parse --short HEAD && python3 corpus/evidence/round50/c1-count.py
cfe6c9f
BASELINE=FAIL rc=1 findings=?
(elided: P1-P6 `-> PASS`, PERTURB_PASS=6/6, EXPECTED_BAD=PASS rc=2 — as in the receipt)
R49_REGRESSION=FAIL rc=1
LEGS=3/5
C1=FAIL
exit=1
```
`git diff --stat 1d7aba0..HEAD -- tools/assimilate-rows.py` → `102 insertions(+), 19 deletions(-)`; `sha256sum` `382aca9b…` at the tip vs `bdaf80f4…` at HEAD (changed at `2a3389d`). `c2-count.py` at the same worktree still prints `C2=PASS` exit 0. At the parent `9ec1751` both `c1-count` (`LEGS=5/5`) and `c2-count` (`C2=PASS`) pass — the receipt names bytes; it does not discriminate the last two commits.
## 5. Drafted SKILL.md correction — intended lane path: `SKILL.md`, appended as a standalone line after the gate table (after line 132, before the round-25 historical paragraph now at 134); the quoted substring occurs exactly once (`grep -c …` → `1`)
```text
correction: SKILL.md:132 ("C1 measured at candidate `ec52e632edbad7fe51a6573d29acad5a028a7158`") — the round-50 gate row names the candidate and the freeze tree but no landed revision; the four counters are re-measured at the landed tip `1d7aba0948cf62f6158f77e220f64320a5b6c6cc` in `corpus/evidence/round51/measure-r50-at-tip.txt` (`C1=PASS` `C1_SUPPLEMENT=PASS` `C2=PASS` `STALE_COUNT=PASS`, each exit 0; five blocks line-identical to `corpus/evidence/round50/measure-after.txt`), and the row is one-shot there — at `cfe6c9fb` the same `c1-count.py` prints `BASELINE=FAIL rc=1` … `C1=FAIL` exit 1 after `2a3389d` changed the tool default (`tools/assimilate-rows.py` `382aca9b…` -> `bdaf80f4…`).
```
## Risks / blockers
- Both artifacts are drafts in this report only; the lane is untouched, and the receipt must land before any round-51 report cites the round-50 `measure-after.txt` numbers. Not re-measured here: `build-spans.py`, `quote-substance-check.py`, `cjk-ground-check.py`, `decode-form-check.py`, `sources-census.sh`. No install or upgrade was needed or performed.
- QUALITY 68's recipe (`git archive <rev> | tar -x && cd <tmp> && python3 …`) does not work for these two counters (section 1); a future pin must say "clone/checkout at `<rev>`", or the counters must learn a checkout flag.
VERDICT — attacked the "round-50 numbers were measured at a working tree" defect: exported tip `1d7aba0`, showed a bare export cannot run these counters (c2 `NO_BASE_OR_REGISTER` exit 2, c1 `R49_REGRESSION` exit 2), measured a clean clone at that exact revision (all four counters PASS, exit 0), diffed 82 lines against `measure-after.txt` with zero differing lines, and showed the same C1 command failing (`C1=FAIL` exit 1) at `cfe6c9f`; receipt and SKILL.md correction drafted, lane untouched.
