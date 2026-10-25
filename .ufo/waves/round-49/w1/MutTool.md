# MutTool — C1 gate mutation probe (round 49, wave 1)

2026-10-25 · lane `chousa-shokunin` · target `tools/assimilate-rows.py` · detector `corpus/evidence/round49/c1-count.py` (BASE_REV `414a2ec6cde05a921dbdd9e02e7ae56b0db647ef`).
Method: byte-identical copy to `/tmp/chousa-r49-MutTool/pristine.py`; one single-point mutant per class (`m1`–`m8`); detector `python3 corpus/evidence/round49/c1-count.py --tool <mutant>` run on pristine then each mutant; leg lines pasted verbatim. Production file never written; scratch deleted at the end. No installs (pacman paused; none needed).

## Baseline — pristine copy (must pass; a baseline failure would make every verdict inconclusive)

```
$ python3 corpus/evidence/round49/c1-count.py --tool /tmp/chousa-r49-MutTool/pristine.py   # rc=0
BASE_CENSUS=ok
SET_A TOOL_EXIT=0 CITED=9 APPEND=9/9 HELD=0/0 BY_DOC=9/9 EXTRA=0 REWRITE=2/2 SHAPE=9/9 CONTIGUOUS=yes URL=9/9 USED_BY=9/9 NORMALIZED=9/9 COLLISIONS=match CENSUS=ok -> PASS
SET_B TOOL_EXIT=0 CITED=3 APPEND=3/3 HELD=0/0 BY_DOC=3/3 EXTRA=0 REWRITE=1/1 SHAPE=3/3 CONTIGUOUS=yes URL=3/3 USED_BY=3/3 NORMALIZED=3/3 COLLISIONS=match CENSUS=ok -> PASS
SET_C TOOL_EXIT=0 CITED=5 APPEND=3/3 HELD=2/2 BY_DOC=5/5 EXTRA=0 REWRITE=1/1 SHAPE=3/3 CONTIGUOUS=yes URL=3/3 USED_BY=3/3 NORMALIZED=3/3 COLLISIONS=match CENSUS=ok -> PASS
GUARD TOOL_EXIT=0 COLLISIONS=['S002'] -> PASS
PIPE TOOL_EXIT=0 ROWS=1 CELLS=11 RECHECK=90d STRIPPED_LOGGED=yes CENSUS=ok -> PASS
SETS_PASS=3/3
C1=PASS
```

## Kill matrix (before-hash for every mutant: pristine `3b8a6e7daa45dca66c1d2f84cbb7903d999091a75a4b92ac2cda2c71997b06a6`)

| m | class | single-point edit | sha256 after | verdict | killed by |
|---|---|---|---|---|---|
| 1 | column-zero-only collision grep | L52 `GREP_RE` loses the `{0,3}` leading-space allowance | `835ea00efe156b104d89bb1191e4df4f0e6674c3c74f061406d0b66b45b005c3` | KILLED | GUARD `COLLISIONS=[]` (2-space-indented registry row missed) |
| 2 | sequential substitution | L182 `subst` → `str.replace` loop over `cited` | `893c5f60710440337be232cfcb121641764be9d2c3ce4c6aa7348045673bbd09` | KILLED | SET_A `REWRITE=0/2` (chain S092→S100→S101→S102→S103→S104) |
| 3 | used-by left as staged | L206 drop the used-by tuple | `4ba91a5103819eb0b29629c3210a518dad7f12d7e0bca9fd1d59950f86ef839e` | KILLED | SET_A `USED_BY=6/9` + census `E11`×3; PIPE `E11` |
| 4 | no pipe rewrite | L192–195 delete the rewrite block | `ef079866f57715d4c0330e717ea5368f31dce93b09228b2c8ddd8057bcb49be7` | KILLED | PIPE `CELLS=12` + census `E01 fields=12` |
| 5 | recheck kept as prose | L198–205 delete the reduction block | `50a50ec7badcf295ded1f8d6723970f4e06b030b7f1f81702ba7d8e0ac6d75bf` | KILLED | SET_A/B/C `NORMALIZED=0/n` + census `E09`; PIPE prose recheck, `STRIPPED_LOGGED=no` |
| 6 | ids from 1, not base max+1 | L166 `nxt = max(…)+1` → `nxt = 1` | `59485c895eacdedc55cee8bf4cdbf307ea0f4f866ef3d5ccdd35059dc63b3bcb` | KILLED | SET_A/B/C `BY_DOC=0`, census `E03 duplicate id`; PIPE `E03` |
| 7 | held rows appended anyway | L189 drop the `action != "append"` skip | `06ad37f673593a9a94dee3003c23e41ca08366d922c8ad29feaff6058e4a9be1` | KILLED | SET_C `APPEND=5/3 SHAPE=5/3 CONTIGUOUS=no` + census `E03/E04` |
| 8 | status not forced to `mined` | L206 drop the status tuple | `977dc8b805588577e1a388d3256ad418328664d3580c4ac5d35ef3196050385c` | **SURVIVED** | — `C1=PASS` rc=0 |

## Decisive leg lines per mutant (verbatim; non-listed legs printed PASS)

### m1 — sets 3/3 PASS; only GUARD exercises the 0–3-space allowance (pinned package/registry have no indented id rows)
```
GUARD TOOL_EXIT=0 COLLISIONS=[] -> FAIL
SETS_PASS=3/3
C1=FAIL
```

### m2 — SET_B/SET_C PASS (no staged-id→cited-staged-id chains there)
```
SET_A TOOL_EXIT=0 CITED=9 APPEND=9/9 HELD=0/0 BY_DOC=9/9 EXTRA=0 REWRITE=0/2 SHAPE=9/9 CONTIGUOUS=yes URL=9/9 USED_BY=9/9 NORMALIZED=9/9 COLLISIONS=match CENSUS=ok -> FAIL
SETS_PASS=2/3
C1=FAIL
```

### m3 — 6/9 staged used-by cells coincidentally equal the expected lists; S102/S103/S104 kept staged values naming non-lane paths
```
SET_A TOOL_EXIT=0 CITED=9 APPEND=9/9 HELD=0/0 BY_DOC=9/9 EXTRA=0 REWRITE=2/2 SHAPE=9/9 CONTIGUOUS=yes URL=9/9 USED_BY=6/9 NORMALIZED=9/9 COLLISIONS=match CENSUS=exit1 E11	S102 missing used-by corpus/knowledge/source-type-taxonomy-r37.md;E11	S103 missing used-by corpus/knowledge/chinese-search-log-r37.md;E11	S104 missing used-by corpus/knowledge/chinese-search-log-r37.md -> FAIL
PIPE TOOL_EXIT=0 ROWS=1 CELLS=11 RECHECK=90d STRIPPED_LOGGED=yes CENSUS=exit1 E11	S096 missing used-by corpus/knowledge/elsewhere.md -> FAIL
SETS_PASS=2/3
C1=FAIL
```

### m4 — CELLS=12, not 13: m4 keeps the recheck reduction, which still normalises the recheck cell's escaped pipe; only the anchor's survives
```
PIPE TOOL_EXIT=0 ROWS=1 CELLS=12 RECHECK=- STRIPPED_LOGGED=yes CENSUS=exit1 E01	S096 fields=12 -> FAIL
SETS_PASS=3/3
C1=FAIL
```

### m5
```
SET_A TOOL_EXIT=0 CITED=9 APPEND=9/9 HELD=0/0 BY_DOC=9/9 EXTRA=0 REWRITE=2/2 SHAPE=9/9 CONTIGUOUS=yes URL=9/9 USED_BY=9/9 NORMALIZED=0/9 COLLISIONS=match CENSUS=exit1 E09	S096 recheck=180d — re-open the NII manual and confirm both 注意書き notes under section G are still present (ran 2026-10-23);E09	S097 recheck=90d — re-open the TAB2 publisher page and confirm section 2 still reads "数日～2週間後にDOIによるリンクが作成されます" (ran 2026-10-23);E09	S098 recheck=90d — re-open the FAQ pa -> FAIL
SET_B TOOL_EXIT=0 CITED=3 APPEND=3/3 HELD=0/0 BY_DOC=3/3 EXTRA=0 REWRITE=1/1 SHAPE=3/3 CONTIGUOUS=yes URL=3/3 USED_BY=3/3 NORMALIZED=0/3 COLLISIONS=match CENSUS=exit1 E09	S096 recheck=180d — `aaron papers fetch 10.1186/s13643-020-01542-z` then confirm Table 1 item 8 still reads "copied and pasted exactly as run" (ran 2026-10-23);E09	S097 recheck=90d — re-open the chapter-04 URL and confirm section 4.5 still reads "Document the search process in enough detail to e -> FAIL
SET_C TOOL_EXIT=0 CITED=5 APPEND=3/3 HELD=2/2 BY_DOC=5/5 EXTRA=0 REWRITE=1/1 SHAPE=3/3 CONTIGUOUS=yes URL=3/3 USED_BY=3/3 NORMALIZED=0/3 COLLISIONS=match CENSUS=exit1 E09	S096 recheck=180d — re-download the .doc, decode its UTF-16 body, and confirm the CJK run still contains 是否检索灰色文献等关键问题 (ran 2026-10-23);E09	S097 recheck=180d — re-open the page and confirm the body still reads 指导原则分为概述、方法学要点、报告撰写规范、指导原则所依据的参考文献和附录五个方面 (ran 2026-10-23);E09	S098 recheck=180d — re- -> FAIL
PIPE TOOL_EXIT=0 ROWS=1 CELLS=11 RECHECK=90d — re-open the page and confirm a / b STRIPPED_LOGGED=no CENSUS=exit1 E09	S096 recheck=90d — re-open the page and confirm a / b -> FAIL
SETS_PASS=0/3
C1=FAIL
```

### m6 — SET_B/SET_C/PIPE likewise killed on `E03 duplicate id`
```
SET_A TOOL_EXIT=0 CITED=9 APPEND=9/9 HELD=0/0 BY_DOC=0/9 EXTRA=0 REWRITE=0/2 SHAPE=9/9 CONTIGUOUS=no URL=0/9 USED_BY=0/9 NORMALIZED=0/9 COLLISIONS=match CENSUS=exit1 E03	S001 duplicate id;E03	S002 duplicate id;E03	S003 duplicate id;E03	S004 duplicate id;E03	S005 duplicate id;E03	S006 duplicate id;E03	S007 duplicate id;E03	S008 duplicate id;E03	S009 duplicate id -> FAIL
SETS_PASS=0/3
C1=FAIL
```

### m7
```
SET_C TOOL_EXIT=0 CITED=5 APPEND=5/3 HELD=2/2 BY_DOC=5/5 EXTRA=0 REWRITE=1/1 SHAPE=5/3 CONTIGUOUS=no URL=3/3 USED_BY=3/3 NORMALIZED=3/3 COLLISIONS=match CENSUS=exit1 E03	S085 duplicate id;E03	S093 duplicate id;E04	S093 duplicate url arxiv.org/html/2012.00614v2 within scope the per-evidence versus per-claim structure of a support judgement, on real-world claims -> FAIL
SETS_PASS=2/3
C1=FAIL
```

### m8 — SURVIVOR (full leg block, verbatim)
```
SET_A TOOL_EXIT=0 CITED=9 APPEND=9/9 HELD=0/0 BY_DOC=9/9 EXTRA=0 REWRITE=2/2 SHAPE=9/9 CONTIGUOUS=yes URL=9/9 USED_BY=9/9 NORMALIZED=9/9 COLLISIONS=match CENSUS=ok -> PASS
SET_B TOOL_EXIT=0 CITED=3 APPEND=3/3 HELD=0/0 BY_DOC=3/3 EXTRA=0 REWRITE=1/1 SHAPE=3/3 CONTIGUOUS=yes URL=3/3 USED_BY=3/3 NORMALIZED=3/3 COLLISIONS=match CENSUS=ok -> PASS
SET_C TOOL_EXIT=0 CITED=5 APPEND=3/3 HELD=2/2 BY_DOC=5/5 EXTRA=0 REWRITE=1/1 SHAPE=3/3 CONTIGUOUS=yes URL=3/3 USED_BY=3/3 NORMALIZED=3/3 COLLISIONS=match CENSUS=ok -> PASS
GUARD TOOL_EXIT=0 COLLISIONS=['S002'] -> PASS
PIPE TOOL_EXIT=0 ROWS=1 CELLS=11 RECHECK=90d STRIPPED_LOGGED=yes CENSUS=ok -> PASS
SETS_PASS=3/3
C1=PASS
```

**Survivor mechanism (measured).** Status cell of every staged row extracted from the sha256-pinned `SOURCES.append.md`: S082–S169 and S172–S195 are `mined`; only S170,S171 are `queued`. Cited ids per set (TOKEN_RE ∩ staged rows, extracted): A = S087,S088,S089,S091,S092,S100,S101,S102,S103 · B = S082,S083,S090 · C = S097,S114,S130,S131,S133 — none is S170/S171. GUARD and PIPE fixtures also stage `mined`. The counter's NORMALIZED leg checks `cells[7]=="mined"`, which holds without any forcing. So on every fixture the force is a no-op: no leg distinguishes a tool that leaves a non-`mined` staged status in place. Coverage finding, not a contract change — frozen `claims.md` untouched; the kill rule's "status `mined`" leg is currently unexercised (a fixture citing a `queued` staged row, e.g. S170, would close it).

## Restoration / boundaries
- production `tools/assimilate-rows.py` sha256 before == after == `3b8a6e7daa45dca66c1d2f84cbb7903d999091a75a4b92ac2cda2c71997b06a6` (never edited; mutants lived only under `/tmp/chousa-r49-MutTool/`).
- `pristine.py` hash unchanged across all runs; scratch deleted and verified absent at the end.
- Writes: this report and `/tmp` only. No production file, no git index/jj state, no sibling lane, no `/home/vgpnk/Projects/shokuknow` write; no network, no live fetch; no installs; no subagents/background jobs.

VERDICT: probed the frozen C1 gate with 8 single-point mutants of `assimilate-rows.py` — 7/8 KILLED (GUARD/PIPE/set+census legs), 1 SURVIVOR m8 (status-not-forced: every cited staged row already `mined`, so the force is unobservable to every leg) — recorded as a coverage finding; production bytes untouched.
