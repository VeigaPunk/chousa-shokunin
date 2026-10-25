# ExecToolMoreSets — C1 generalization probe (round 49 w1)

Seat: ExecToolMoreSets (leaf). Scope: generalize `tools/assimilate-rows.py` beyond the C1 counter's frozen sets using three staged package entries NOT in `c1-count.py`'s SETS. Read-only inputs; sole writes: this report and scratch `/tmp/chousa-r49-ExecToolMoreSets` (deleted before finish).

## Environment / tooling
- Lane HEAD = `65940928cc9332b386bcbca92571451cc4374cbe` ("round-49: C1 candidate tools/assimilate-rows.py…") — `git -C chousa-shokunin rev-parse HEAD`.
- Tool `tools/assimilate-rows.py` sha256 `3b8a6e7daa45dca66c1d2f84cbb7903d999091a75a4b92ac2cda2c71997b06a6` (`sha256sum`).
- Staged `SOURCES.append.md` sha256 `a6dec4a0086d3cf767d638d7e52fdda08f78d22b0b376049b0ad14ff0f8aa696` — identical to C1's pinned PINS value; package unchanged vs the counter snapshot.
- Registry used: lane `corpus/SOURCES.md` working copy (max Registry id = S095; collisions list below). `RULES.md` read; no install/upgrade performed or needed; no pacman transaction.

## Method (per set)
`python3 tools/assimilate-rows.py --staged <PKG>/SOURCES.append.md --knowledge <PKG>/knowledge --registry <LANE>/corpus/SOURCES.md --opened 2026-10-25 --out /tmp/chousa-r49-ExecToolMoreSets/<set> --entry corpus/knowledge/<entry>.md`
then a scratch mirror exactly per `c1-count.py`'s `make_mirror`/`insert_rows` (lane corpus/SOURCES.md copied, append.md rows inserted after the last Registry table row = S095, rewritten entry placed at `corpus/knowledge/`), then `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <mirror>/corpus/SOURCES.md`.

## Set 1 — cnki-citation-check-r40.md
- Tool exit: `0`. Observed: `COLLISIONS=14`, `CITED=3 APPEND=3 HELD=0` (cited S109, S111, S124 — the `S109`–`S111` range dash yields no separate S110 token).
- `renumber.tsv` (verbatim):
  - `S109	S096	append	www.jstage.jst.go.jp/article/kenkokyoiku/32/2/32_320208/_pdf/-char/ja`
  - `S111	S097	append	www.medsci.cn/guideline/show_article.do?id=23e481c0052069d3`
  - `S124	S098	append	gs.sxu.edu.cn/docs/2025-03/9e5cdd215a414bf6b5694912018de4c8.pdf`
- Census: exit `0`; final line `file	ok	/tmp/chousa-r49-ExecToolMoreSets/mirror-cnki-citation-check-r40/corpus/SOURCES.md`. Warnings W04 S051/S053/S073/S074/S075 duplicate-url across scopes are pre-existing: identical list on an un-appended base mirror (`census_exit=0`, `file ok`).
- By-document error: token **S076** passes through unchanged; lane S076 = GNU `sed(1)`/`sed.info` manual (SOURCES.md line 86), while the entry means wave 1's J-STAGE citation-matching question. Reader must repair before landing.

## Set 2 — chinese-search-log-r37.md
- Tool exit: `0`. Observed: `COLLISIONS=14`, `CITED=4 APPEND=4 HELD=0`.
- `renumber.tsv` (verbatim): `S101→S096`, `S102→S097`, `S103→S098`, `S104→S099`, all `append`.
- Census: exit `0`; `file ok` for `mirror-chinese-search-log-r37`; same pre-existing W04 list.
- By-document errors: tokens **S071** (lane: GNU coreutils `env(1)` manual; entry intends PRISMA-S), **S072** (lane: GNU Bash Reference Manual; entry intends Cochrane Handbook), **S079** (lane: RFC 7089 Memento; entry intends the Japanese 参照日 rule) all pass through unchanged.

## Set 3 — search-tracking-record-r40.md
- Tool exit: `0`. Observed: `COLLISIONS=14`, `CITED=4 APPEND=2 HELD=2`.
- `renumber.tsv` (verbatim):
  - `S094	S080	held	warp.ndl.go.jp/en/info/qanda` (staged S094's URL == lane S080; NOT lane S094, which is CorFEVER)
  - `S114	S093	held	arxiv.org/html/2012.00614v2` (URL == lane S093)
  - `S130	S096	append	www.gcpunion.org/upload/cmsfile/1703404975484107.doc`
  - `S134	S097	append	jmla.pitt.edu/ojs/jmla/article/download/1449/2061`
- Census: exit `0`; `file ok` for `mirror-search-tracking-record-r40`; same pre-existing W04 list.
- By-document error: token **S069** (lane: GNU `grep(1)` `-o`/`-b` manual; entry intends PRISMA-S per-strategy date) passes through unchanged.

## Findings
1. Tool exit 0 on all three non-counter entries; every append row is an 11-cell census-schema row (status `mined`, opened `2026-10-25`, recheck reduced to cadence, pipes rewritten, used-by = exactly the citing entries — per `stripped.tsv`); all three mirrors pass the census. The C1 counter's frozen semantics generalize to these entries.
2. Held-by-URL works across packages even where staged ids collide with lane ids: staged S094 held to lane S080 and staged S114 to lane S093 by URL, never to the colliding ids S094/S114. The 14 colliding ids (S082..S095) are reported in `collisions` and never assigned.
3. By-document errors found (5): S076 (set 1), S071/S072/S079 (set 2), S069 (set 3). All are non-staged tokens the tool passes through unchanged per its docstring ("checking that they name the right lane document is the reader's job"); each names a different lane document than the entry intends. None is staged, so none was remapped.

## Risks
- A full adoption of the staged package would need the S082..S095 id collisions reviewed (informational today; not part of this probe).
- Held rows' `used-by` is not widened (tool's named limit) — S080/S093 keep their existing used-by.

VERDICT: probed assimilate-rows.py against three non-counter staged entries — tool exit 0 and census `file ok` on all three scratch mirrors (append S096..S099; hold S080/S093); flagged 5 by-document pass-through mismatches (S076, S071, S072, S079, S069) for the reader's repair.
