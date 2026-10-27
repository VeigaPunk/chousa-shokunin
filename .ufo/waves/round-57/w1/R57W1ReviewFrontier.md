# R57W1ReviewFrontier — frontier-step conformance (round 57, wave 1)

Seat: reviewer, leaf (no subagent dispatch). Scope: check the round's frontier-step conformance against
/home/vgpnk/Projects/shokunin/CORPUS.md (SOURCES contract v1) and round prompt §2b, items (1)-(4).
All commands run read-only in the lane; scratch `/fast/scratch/hyaku/chousa-r57/R57W1ReviewFrontier` created and
deleted before yield (trap-equivalent: `rm -rf` executed after report write; nothing in it but mkdir residue).

## (1) Census command + round-start output committed — CONFORMANT

`/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round57/census-start.txt` exists, committed at the
R57-C2 freeze commit (round start):

```
$ git -C /home/vgpnk/Projects/shokunin/chousa-shokunin log -1 --format='%H %ci %s' corpus/evidence/round57/census-start.txt
c2f914c53201a8f8ee4fef823b82681051d55592 2026-10-27 02:54:05 -0300 round-57: freeze R57-C2 (freshness re-fetch counter, before receipt, controls, egress table, census start)
```

Full file content (7 lines, `cat -A` verified no hidden bytes):

```
chousa	W04	S051 duplicate url www.w3.org/TR/2017/REC-html52-20171214/syntax.html across scopes
chousa	W04	S053 duplicate url docs.python.org/3/library/socket.html across scopes
chousa	W04	S073 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
chousa	W04	S074 duplicate url docs.python.org/3/library/hashlib.html across scopes
chousa	W04	S075 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
chousa	ok	/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md
exit=0
```

Maintained validator re-run at report time — exit=0, same five pre-existing W04 duplicate-URL warnings:

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa ; echo exit=$?
[identical five W04 lines + "chousa ok ..." as census-start.txt]
exit=0
```

Frozen manual census block from CORPUS.md re-run at report time:

```
rows: 130
malformed: 0
tiers: A=106 B=19 C=5
status: mined=106 queued=19 rejected=5
dup-ids:            (empty)
enum-viol:          (empty)
mined-usedby-missing: (empty)
```

Row count 130 matches the round-56 census-end commit b804147 message ("rows 126 -> 130"); no malformed rows, no
duplicate ids, no enum/tier-inflation violations, every `mined` row's used-by path exists on disk.

## (2) SOURCES row opened this round backing a round claim — GAP AT REPORT TIME

Rows carrying `opened=2026-10-27` are exactly S124-S130, but all seven were committed at base 6656f077
(round-56 work earlier today); none opened in round 57 exists yet:

```
$ git -C /home/vgpnk/Projects/shokunin/chousa-shokunin diff 6656f0770a1460d6ba73d9d2976f698a35311921 HEAD -- corpus/SOURCES.md
(empty)
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {o=$10; gsub(/[[:space:]]/,"",o); if (o=="2026-10-27") print $2}' corpus/SOURCES.md
S124 S125 S126 S127 S128 S129 S130   (all committed at base, verified via git log -- corpus/SOURCES.md: no round-57 commits touch it)
```

C3's new fetch ids exist in the fetch record but have no registry rows at report time. refetch.tsv at HEAD already
carries S131-S133 (committed e0e73e0); the working tree appends S133 (alt URL), S134, S135, S136 (17 appended rows,
no deletions — verified `git diff HEAD` shows only `+` lines):

```
$ awk -F'\t' 'NR>1 && $1 ~ /^S13[1-6]$/ {print $1,$2,$4,$6,$7}' corpus/evidence/round57/refetch.tsv | head -7
S131 https://www.nhc.gov.cn/yaozs/c100097/201904/6bc8f273684845d3ab76fed841eb42d2.shtml 1 22 412
S132 https://www.nhc.gov.cn/yaozs/c100097/202107/d2a45e6ae041423f950b3865e43f5ef6.shtml 1 22 412
S133 http://www.tcmevidence.net/UserFiles/upload/file/20230410/6381676262587201848492833.pdf 1 28 000
S134 https://www.hnysfww.com/article.php?id=3275 1 0 200
S135 https://www.takarabiomed.com.cn/DownLoad/2540A.pdf 1 0 200
S136 https://www.hnysfww.com/data/article/1656481067585283603.pdf 1 28 200
$ grep -nE '^\|[[:space:]]*S13[1-6]' corpus/SOURCES.md
NO S131-S136 ROWS in SOURCES.md
```

The frozen C3 predicate requires each bound reference's row to be "new since BASE_REV (`mined`, opened 2026-10-27)"
— these rows must exist (with used-by naming `corpus/knowledge/normative-reference-chain-china-r57.md`) by round end;
at report time none do. Defect: none-yet (time-qualified gap, wave still running).

## (3) Round-57 lesson — NOT YET EXISTENT (must exist by round end)

```
$ ls corpus/lessons/round-57.md
No such file (find over the lane newer than claims.md, excluding .ufo/waves, finds no draft)
```

The scribe log card tracks the same absence (`R57W1ScribeLogCard.md`: `R9 | ls corpus/lessons/round-57.md |
No such file or directory at snapshot → the C2 flag target and the C3 quote-carrier do not exist yet`).
By round end the lesson MUST carry:
- `## Gate`: for every new SOURCES row (expected S131+), the URL, access date 2026-10-27, and a ≤25-word quote with
  location grounding `teaches` (contract rule 1);
- `## Mistakes`: one row per mistake as class · evidence · captured-by · fix (vocabulary from mistakes.md §5);
  the misroot sweep of capture-fetch.py's first run (recorded in commit f9736a3) and the record-less wrap-up S105
  byte removal (commit e0e73e0) must land here;
- quarantine verdicts for the QuarA/B/C hand-check batches — at report time none of the three quarantine reports is
  filed in .ufo/waves/round-57/w1/ (only R57W1ScoutR1, R57W1ScoutR1Gov, R57W1ScoutR7, R57W1ScribeD1,
  R57W1ScribeLogCard present), so the lesson cannot be checked for them yet.
Defect: none-yet (time-qualified gap).

## (4) SOURCES.md append-only — CONFORMANT AT REPORT TIME

```
$ git diff 6656f0770a1460d6ba73d9d2976f698a35311921 HEAD --stat -- corpus/SOURCES.md corpus/lessons/
(empty)
```

No in-place edits, so no used-by/recheck/status old→new logging is owed. Observation (not a defect): a mid-wave
read of my first count returned 131 rows vs the committed 130; the working tree now diffs empty against base, i.e.
a transient editor state, with no committed anomaly.

## Round state context (for calibration)

C2 counter at report time: `SET=47 VERDICTS=47/47 REPRODUCED=41 DRIFTED=5 UNREACHABLE=1 BYTE_BACKED=46
CONSISTENT=46/46 FLAGGED=0/0 C2=PASS` exit=0 — matches committed after-receipt e0e73e0; the 4 dispatch-pending
retries resolved (S100/S103/S106 REPRODUCED on attempt 2; S105 UNREACHABLE after 3 attempts ≥600s apart).
C3 counter at report time: `QUOTE_ROWS=0 … C3=FAIL` exit=0 — build start, no entry/manifest yet; scouts have filed
R1/R1Gov/R7 URL tables, the entry and spans manifest do not exist yet.

## Defects (all time-qualified gaps, none patchable by this seat)

- D1 (item 2): no SOURCES row opened in round 57 exists at report time; C3's S131-S136 fetches are unregistered.
  Must exist by round end carrying opened 2026-10-27 and used-by to the chain entry.
- D2 (item 3): no round-57 lesson (committed or draft) at report time; ## Gate, ## Mistakes, and quarantine
  verdicts cannot be checked and must exist by round end.
- D3 (item 3): quarantine hand-check reports (QuarA/B/C) not yet filed, so the lesson's quarantine verdicts are
  unverifiable at report time.

Items (1) and (4) are conformant. Frozen counters/claims untouched; no lane writes except this report.

VERDICT: attacked frontier-step conformance (census start, round-opened SOURCES rows, round-57 lesson slots,
SOURCES append-only) — items (1) and (4) survived conformant; items (2) and (3) stand as report-time gaps that must
close by round end (S131+ rows with opened 2026-10-27; lesson with ## Gate/## Mistakes/quarantine verdicts).
