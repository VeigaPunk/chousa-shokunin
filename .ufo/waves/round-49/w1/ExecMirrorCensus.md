# ExecMirrorCensus — round 49 w1: adoption mirror + sources-census runs

Seat: ExecMirrorCensus (leaf; no subagents/jobs). Tooling: read
`~/.omp/agent/RULES.md`; no install performed (nothing needed). Only write:
this report. Scratch `/tmp/chousa-r49-ExecMirrorCensus` deleted at end.

## 1. Mirror build (commands run, observed)

```
$ mkdir -p /tmp/chousa-r49-ExecMirrorCensus/lane
$ cp -a /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus \
        /tmp/chousa-r49-ExecMirrorCensus/lane/corpus
-> "copied"; find ... -type f | wc -l = 780
```

Used-by-path extraction (python over copied SOURCES.md, 11-cell rows):
80 used-by refs total; exactly one outside `corpus/`:
`S077 -> tools/quarantine-check.py`. Real lane holds
`tools/quarantine-check.py` (16,281 B, exists); mirror got a touched placeholder
per assignment: `touch /tmp/chousa-r49-ExecMirrorCensus/lane/tools/quarantine-check.py`.

Insertion: `edit PUT >105` (after S095 row, the last `## Registry` row, before
the blank line and `## Paths`) — S096..S104 now lines 106–114 of the mirror
SOURCES.md, row text verbatim from `adopt/append.md`.

Knowledge copies:
```
$ cp -a chousa-shokunin/.ufo/waves/round-49/assimilation/adopt/corpus/knowledge/*.md \
        /tmp/chousa-r49-ExecMirrorCensus/lane/corpus/knowledge/
-> aggregator-vs-source-r36.md (6250 B), citation-count-semantics-r37.md (6224 B)
```

## 2. sources-census.sh runs (commands, observed output)

BEFORE (pristine copy + tools placeholder):

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file \
    /tmp/chousa-r49-ExecMirrorCensus/lane/corpus/SOURCES.md
validate_before_exit=0
file	W04	S051 duplicate url www.w3.org/TR/2017/REC-html52-20171214/syntax.html across scopes
file	W04	S053 duplicate url docs.python.org/3/library/socket.html across scopes
file	W04	S073 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
file	W04	S074 duplicate url docs.python.org/3/library/hashlib.html across scopes
file	W04	S075 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
file	ok	/tmp/chousa-r49-ExecMirrorCensus/lane/corpus/SOURCES.md
```

(Without the placeholder, the same validate exited **1** with one extra line:
`file	E11	S077 missing used-by tools/quarantine-check.py`.)

```
$ bash .../sources-census.sh census --file .../SOURCES.md   # same file
census_before_exit=0
file	rows	95 | file	tier.A	89 | file	tier.B	1 | file	tier.C	5
file	status.mined	71 | file	status.queued	19 | file	status.rejected	5
FLEET: rows 95, tier A 89 B 1 C 5 invalid 0, status queued 19 mined 71 rejected 5 invalid 0, missing 0
```

AFTER (9 rows inserted + 2 knowledge files copied):

```
validate_after_exit=0
file	W04	S051 duplicate url ... (identical 5 W04 lines as before)
file	ok	/tmp/chousa-r49-ExecMirrorCensus/lane/corpus/SOURCES.md
census_after_exit=0
file	rows	104 | file	tier.A	92 | file	tier.B	7 | file	tier.C	5
file	status.mined	80 | file	status.queued	19 | file	status.rejected	5
FLEET: rows 104, tier A 92 B 7 C 5 invalid 0, status queued 19 mined 80 rejected 5 invalid 0, missing 0
```

Delta: +9 rows (S096–S104): +3 tier A (S096–098), +6 tier B (S099–104),
+9 mined; queued/rejected unchanged; no E/W line added by the adoption (validate
exit 0 before and after, same 5 pre-existing W04). No E04/E08/E09/E10 or
W01/W02/W03 from any adopted row; all 9 rows have valid opened dates
(2026-10-25), valid NNd recheck cadences, and distinct URLs.

## 3. stripped.tsv — every stripped recheck prose (Gate block)

All 9 rows carry a stripped `recheck` prose (verbatim from `adopt/stripped.tsv`):

- S096: `180d — re-open the NII manual and confirm both 注意書き notes under section G are still present (ran 2026-10-23)`
- S097: `90d — re-open the TAB2 publisher page and confirm section 2 still reads "数日～2週間後にDOIによるリンクが作成されます" (ran 2026-10-23)`
- S098: `90d — re-open the FAQ page and confirm the four-step 引用元の所在確認 list is unchanged (ran 2026-10-23)`
- S099: `180d — re-open https://ncpssd.org/service/help?mainTitle=%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98 and confirm item 7 still limits full-text download to registered users (ran 2026-10-23)`
- S100: `365d — re-open the ERIC record and confirm the abstract still carries the "lateral reading" sentence (ran 2026-10-23)`
- S101: `180d — re-download the document and confirm 关于自引的说明 still reads "如果引文出现了任一合作者，那么这条引文将被认定为自引" (ran 2026-10-23)`
- S102: `180d — re-download the document and confirm section 14.2 still lists nine 著录项目 beginning with 主要责任者 and 文献题名 (ran 2026-10-23)`
- S103: `180d — re-download the PDF and confirm section 5.6.1 still reads "被引用回数" (ran 2026-10-23)`
- S104: `180d — re-download the PDF and confirm section 2.1 still lists 引用量 and 下载量 (ran 2026-10-23)`

Non-recheck strips also present: `opened=2026-10-23` for all 9 (equal to the
rows' opened values, so redundant with the registry), and `used-by`
amplifications — S102 adds `corpus/knowledge/source-type-taxonomy-r37.md`;
S103 and S104 add `corpus/knowledge/chinese-search-log-r37.md` (append.md rows
carry only `corpus/knowledge/citation-count-semantics-r37.md`).

## 4. Calibration observations

- E11 checks mined rows' used-by against the lane root; the single
  outside-corpus ref (`tools/quarantine-check.py`, S077) makes validate exit 1
  without the touched placeholder, 0 with it. Mirror reproduces the real lane's
  file presence.
- The used-by stripping is what keeps the adopted registry census-clean: the
  two stripped-in targets `source-type-taxonomy-r37.md` and
  `chinese-search-log-r37.md` are absent from the lane corpus (present only in
  the staged merge package
  `/home/vgpnk/Projects/shokuknow/merge/chousa/knowledge/corpus/knowledge/`).
  Re-applying the full stripped used-by cells would raise two E11 findings in
  the mirror; as written (append.md verbatim), adoption validates clean.

VERDICT: built the round-49 C2 adoption mirror (corpus copy + used-by
placeholder + append insertion + knowledge copies) and ran sources-census
validate/census before vs after — 95→104 rows, tier A 89→92 / B 1→7, mined
71→80, validate exit 0 both times (pre-existing W04 ×5 only), census exit 0;
listed all 9 stripped recheck prose for the lesson Gate block.
