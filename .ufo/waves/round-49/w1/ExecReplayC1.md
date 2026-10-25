# ExecReplayC1 — round 49 w1 C1 replay (seat report)

seat: ExecReplayC1 (leaf executor, godspeed)
date: 2026-10-25
lane: /home/vgpnk/Projects/shokunin/chousa-shokunin
scope: replay C1 receipts from committed bytes; freeze-predicate equality vs counters.
files changed: only this report.

## Tooling
- Read /home/vgpnk/.omp/agent/RULES.md (operator channel order, update-safety gate) and `skill://godspeed` first.
- No install performed or needed: `python3` already present; no pacman transaction attempted (guard respected).

## 1. Extract candidate bytes (commit 65940928cc9332b386bcbca92571451cc4374cbe)
```
$ mkdir -p /tmp/chousa-r49-ExecReplayC1/tree && git -C /home/vgpnk/Projects/shokunin/chousa-shokunin archive 65940928cc9332b386bcbca92571451cc4374cbe | tar -x -C /tmp/chousa-r49-ExecReplayC1/tree
$ find /tmp/chousa-r49-ExecReplayC1/tree/corpus/evidence/round49 -maxdepth 2 -type f | sort
→ /tmp/chousa-r49-ExecReplayC1/tree/corpus/evidence/round49/{build-spans.py,c1-count.py,c2-count.py,claims.md,controls/c1-before.txt,controls/c2-before.txt,controls/copy-tool.py}
```
Archive also contains `tools/assimilate-rows.py` (sha match below).

## 2. Parity archived vs worktree
```
$ for f in c1-count.py c2-count.py claims.md controls/c1-before.txt controls/copy-tool.py; do
  cmp -s "corpus/evidence/round49/$f" "/tmp/chousa-r49-ExecReplayC1/tree/corpus/evidence/round49/$f" && echo "SAME $f" || echo "DIFF $f"; done
→ SAME c1-count.py; SAME c2-count.py; SAME claims.md; SAME controls/c1-before.txt; SAME controls/copy-tool.py
$ sha256sum tools/assimilate-rows.py /tmp/chousa-r49-ExecReplayC1/tree/tools/assimilate-rows.py /tmp/chousa-r49-ExecReplayC1/tree/corpus/evidence/round49/controls/copy-tool.py corpus/evidence/round49/controls/copy-tool.py
→ 3b8a6e7daa45dca66c1d2f84cbb7903d999091a75a4b92ac2cda2c71997b06a6 (adopter, both copies)
→ 55d440df112412f1dad5fd5b384caad8d92bf7939fd6fd60c054c9642d0bc638 (copy-tool, both copies; = c1-before.txt line 9)
$ git rev-parse --short HEAD → 6594092; git status --porcelain -- tools/assimilate-rows.py corpus/evidence/round49/ → (clean)
```
Candidate is committed at HEAD 6594092, byte-identical to the archived adopter.

## 3. Freeze-predicate equality (claims.md @ fe740e7 vs counter docstrings)
```
$ git -C <lane> show fe740e7838b338d17fec9338c909557e6e7fed7d:corpus/evidence/round49/claims.md > /tmp/chousa-r49-ExecReplayC1/claims-fe740e7.md
$ python3 (scratch analysis):
  claims.md frozen==worktree: True
  C1 predicate exact equality: True | norm equality: True
  C2 predicate exact equality: True | norm equality: True
```
- C1 sentence: claims.md lines 21–32 == `c1-count.py` docstring lines 5–16 (exact).
- C2 sentence: claims.md lines 51–69 == `c2-count.py` docstring lines 5–23 (exact).
- claims.md worktree is byte-identical to the freeze commit.

## 4. Replay runs (from committed bytes, tree root)
First attempt inside the plain extracted tree (not a git repo) exits `NO_BASE_REV` exit=2: `LANE = parents[3]` of the script is the extracted tree and `git -C LANE archive/ls-tree BASE_REV` fails. Fixed by making the scratch tree a git repo wired to the lane object store (no network, no commit):
```
$ git init -q /tmp/chousa-r49-ExecReplayC1/tree
$ printf '%s\n' '/home/vgpnk/Projects/shokunin/chousa-shokunin/.git/objects' > /tmp/chousa-r49-ExecReplayC1/tree/.git/objects/info/alternates
$ git -C <tree> cat-file -t 414a2ec6cde05a921dbdd9e02e7ae56b0db647ef → commit
$ git -C <tree> archive 414a2ec6... corpus | tar -t | head -5 → corpus/, corpus/QUALITY.md, ...
```
(a) Control replay (`--tool corpus/evidence/round49/controls/copy-tool.py`):
```
BASE_REV=414a2ec6cde05a921dbdd9e02e7ae56b0db647ef
TOOL=present sha256=55d440df112412f1dad5fd5b384caad8d92bf7939fd6fd60c054c9642d0bc638
BASE_CENSUS=ok
SET_A TOOL_EXIT=0 CITED=9 APPEND=9/9 HELD=0/0 BY_DOC=0/9 EXTRA=0 REWRITE=0/2 SHAPE=9/9 CONTIGUOUS=no URL=0/9 USED_BY=0/9 NORMALIZED=0/9 COLLISIONS=match CENSUS=exit1 E03	S087 duplicate id;E09	S087 recheck=180d — re-open the NII manual and confirm both 注意書き notes under section G are still present (ran 2026-10-23);E03	S088 duplicate id;E09	S088 recheck=90d — re-open the TAB2 publisher page and confirm section 2 still reads "数日～2週間後にDOIによるリンクが作成されます" (ran 2026-10-2 -> FAIL
SET_B TOOL_EXIT=0 CITED=3 APPEND=3/3 HELD=0/0 BY_DOC=0/3 EXTRA=0 REWRITE=0/1 SHAPE=3/3 CONTIGUOUS=no URL=0/3 USED_BY=0/3 NORMALIZED=0/3 COLLISIONS=match CENSUS=exit1 E03	S082 duplicate id;E09	S082 recheck=180d — `aaron papers fetch 10.1186/s13643-020-01542-z` then confirm Table 1 item 8 still reads "copied and pasted exactly as run" (ran 2026-10-23);E03	S083 duplicate id;E09	S083 recheck=90d — re-open the chapter-04 URL and confirm section 4.5 still reads "Docum -> FAIL
SET_C TOOL_EXIT=0 CITED=5 APPEND=5/3 HELD=2/2 BY_DOC=0/5 EXTRA=0 REWRITE=0/1 SHAPE=4/3 CONTIGUOUS=no URL=0/3 USED_BY=0/3 NORMALIZED=0/3 COLLISIONS=match CENSUS=exit1 E01	S097 fields=13;E04	S114 duplicate url arxiv.org/html/2012.00614v2 within scope the per-evidence versus per-claim structure of a support judgement, on real-world claims;E09	S114 recheck=365d — re-open the arXiv HTML and confirm section 1 still reads "7,675 annotated claim-evidence pairs" (ran 202 -> FAIL
GUARD TOOL_EXIT=0 COLLISIONS=[] -> FAIL
PIPE TOOL_EXIT=0 ROWS=1 CELLS=13 RECHECK=- STRIPPED_LOGGED=no CENSUS=exit1 E01	S990 fields=13 -> FAIL
SETS_PASS=0/3
C1=FAIL
exit=1
```
Compare (python3): `replay lines == c1-before.txt copy-control (lines 8-18): True` — all 11 lines reproduce byte-for-byte.

(b) Candidate replay (default tool `tools/assimilate-rows.py`, sha 3b8a6e7…):
```
BASE_REV=414a2ec6cde05a921dbdd9e02e7ae56b0db647ef
TOOL=present sha256=3b8a6e7daa45dca66c1d2f84cbb7903d999091a75a4b92ac2cda2c71997b06a6
BASE_CENSUS=ok
SET_A TOOL_EXIT=0 CITED=9 APPEND=9/9 HELD=0/0 BY_DOC=9/9 EXTRA=0 REWRITE=2/2 SHAPE=9/9 CONTIGUOUS=yes URL=9/9 USED_BY=9/9 NORMALIZED=9/9 COLLISIONS=match CENSUS=ok -> PASS
SET_B TOOL_EXIT=0 CITED=3 APPEND=3/3 HELD=0/0 BY_DOC=3/3 EXTRA=0 REWRITE=1/1 SHAPE=3/3 CONTIGUOUS=yes URL=3/3 USED_BY=3/3 NORMALIZED=3/3 COLLISIONS=match CENSUS=ok -> PASS
SET_C TOOL_EXIT=0 CITED=5 APPEND=3/3 HELD=2/2 BY_DOC=5/5 EXTRA=0 REWRITE=1/1 SHAPE=3/3 CONTIGUOUS=yes URL=3/3 USED_BY=3/3 NORMALIZED=3/3 COLLISIONS=match CENSUS=ok -> PASS
GUARD TOOL_EXIT=0 COLLISIONS=['S002'] -> PASS
PIPE TOOL_EXIT=0 ROWS=1 CELLS=11 RECHECK=90d STRIPPED_LOGGED=yes CENSUS=ok -> PASS
SETS_PASS=3/3
C1=PASS
exit=0
```
This is the first "after" measurement at the candidate commit (c1-before.txt records only the absent-tool and do-nothing-control states); it matches the claim's Target line exactly.

## Findings
- Frozen predicates equal both counter docstrings exactly; claims.md unchanged from freeze fe740e7.
- Copy-control replay reproduces c1-before.txt lines 8–18 byte-for-byte (11/11).
- Candidate adopter passes all three sets + GUARD + PIPE (C1=PASS exit 0) on first replay from committed bytes; no falsifier found in replay.
- `NO_BASE_REV` exit 2 when the counter's `LANE` is not a git repo with BASE_REV reachable — extracted-tree replays need an object-store link; noted for harness calibration.

## Risks / notes
- Replay determinism verified (two runs, identical output; wall ~1.1s each).
- No network used; no production bytes written; scratch /tmp/chousa-r49-ExecReplayC1 removed before finishing.

VERDICT: attacked C1 adopter replay from commit 6594092 — copy-control leg byte-exact vs c1-before.txt (11/11 lines), candidate measures C1=PASS/3/3, and freeze claims.md predicates equal both counter docstrings; all held.
