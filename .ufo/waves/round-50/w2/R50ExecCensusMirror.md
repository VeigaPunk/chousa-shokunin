# R50ExecCensusMirror — census of the landed registry, two ways, plus the section-10 collision replay

Seat R50ExecCensusMirror (wave 2, falsify). Item: census the landed registry with `scripts/sources-census.sh` and with the manual CORPUS.md commands, compare with the round-50 lesson and `assimilation/validate/census.txt`, then replay the section-10 collision pipeline against the landed bytes with the unchanged staged ids.
Landed tip `c5b8dca85f759c7a772225fe036e7bb9a809b91c`; base `3c51da77b3696ed884c943548ec4b4006e3ca528` (`git merge-base --is-ancestor` → yes). Pins: `corpus/SOURCES.md` `69d92f33b26119bf…615bf1fa`; base registry `277ef4d50af6280c…a9e23945`; `renumber.tsv` `2a421d9daf492197…d6cd430`; `append.md` `4a116d6ad911e1ed…cacc061c`. Only this report was written.

## 1. Path 1 — fleet tool, from the lane root

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa
chousa	W04	S051 duplicate url www.w3.org/TR/2017/REC-html52-20171214/syntax.html across scopes
chousa	W04	S053 duplicate url docs.python.org/3/library/socket.html across scopes
chousa	W04	S073 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
chousa	W04	S074 duplicate url docs.python.org/3/library/hashlib.html across scopes
chousa	W04	S075 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
chousa	ok	/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md
EXIT=0
$ bash …/sources-census.sh census --root /home/vgpnk/Projects/shokunin chousa
chousa	rows	106
chousa	tier.A	93
chousa	tier.B	8
chousa	tier.C	5
chousa	status.mined	82
chousa	status.queued	19
chousa	status.rejected	5
FLEET	rows	106
FLEET	tier.invalid	0
FLEET	status.invalid	0
FLEET	missing	0
EXIT=0
```
No E-code fired. `FLEET`'s tier/status lines repeat the `chousa` values above because the invocation names one lane, so they are single-lane totals, not fleet-wide — a reading note, not a finding.

## 2. Path 2 — the manual census commands of CORPUS.md, from the lane root

```
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md        -> 106
$ awk -F'|' '/^\|…S[0-9]{3,}…/ && NF!=13 {n++} END{print n+0}' corpus/SOURCES.md -> 0
$ awk … tier histogram                                                        -> A=93 B=8 C=5
$ awk … status histogram                                                      -> mined=82 queued=19 rejected=5
$ awk … duplicate ids | sort | uniq -d                                        -> (empty)
$ awk … enum violations + tier inflation                                      -> (empty)
$ awk … mined used-by paths | while read p; do [ -e "$p" ] || echo missing; done -> (empty)
```
Both paths agree on every number. The appended cells are the ones the lesson claims (`corpus/SOURCES.md:114-116`): S104 `docs|A`, S105 `docs|B`, S106 `docs|B`, all `mined`, `opened 2026-10-25`, recheck `90d/180d/180d` (E08/E09 clean). S105's `used-by` is exactly the two citing entries (`citation-matching-semantics-r41.md, cnki-citation-check-r40.md`); S104 and S106 one each.

## 3. Base (103) and the committed census.txt

Base registry `grep -c` → 103; `tier A=92 B=6 C=5`, `status mined=79 queued=19 rejected=5`. Landed − base = `A+1, B+2, mined+3`, exactly the three appended rows. Base validate on a scratch mirror whose registry parent symlinks the lane's `corpus/knowledge`, `corpus/lessons`, `tools` (a bare copy floods E11 because `used-by` resolves against the registry's parent, `sources-census.sh:567`):
```
$ sources-census.sh validate --file /dev/shm/chousa-r50-R50ExecCensusMirror/baseroot/corpus/SOURCES.md
file	W04	S051 … ; W04 S053 … ; W04 S073 … ; W04 S074 … ; W04 S075 …   (one line each, same text)
file	ok	/dev/shm/…/baseroot/corpus/SOURCES.md
EXIT=0
```
The append introduced **zero** new E/W findings; the five W04 are the pre-existing ones. `assimilation/validate/census.txt` prints the same five W04 and `ok`, `exit=0`; my `validate --file corpus/SOURCES.md` on the landed registry prints the same five lines, differing only in the path line. Comparison: agree.
Lesson: `round-50.md:152` records the round start as "exit 0, `ok`, five W04 (S051 S053 S073 S074 S075), 103 rows" — reproduced exactly — and leaves "Round end: (filled at the report)". The 106 end is verified by my runs but recorded in no committed artifact (`census.txt` is a `validate` run, no row count). Calibration note.

## 4. Section-10 collision pipeline, replayed on the landed registry

```
$ grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort > reg-ids
$ grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' /home/vgpnk/Projects/shokuknow/merge/chousa/SOURCES.append.md \
  | grep -oE 'S[0-9]+' | sort > staged-ids ; comm -12 reg-ids staged-ids
reg-ids: 106 lines, first=S001, last=S106 ; staged-ids: 114 lines, first=S082, last=S195
collisions: 25 lines (S082..S106)
$ sha256sum …/merge/chousa/SOURCES.append.md
a6dec4a0086d3cf767d638d7e52fdda08f78d22b0b376049b0ad14ff0f8aa696   (round-49 pin, unchanged)
$ grep -cE '^ {1,3}\|' corpus/SOURCES.md   -> 0   (guarded and column-zero patterns agree today)
```
**25 collisions remain**, three more than the Gate's 22 (`assimilation/collisions`, `reg-ids` 103 lines). Classified by the URL in each source cell (landed vs staged): `S082–S099` and `S104–S106` differ → **21 hard**; `S100–S103` carry the same URL in both files → **4 re-staged**.
The three new ones are hard, and their staged rows are different documents: staged S104 is 提高护理论文的报告质量 (循证护理论文报告规范, Fudan nursing); staged S105 is `own-work` for `corpus/knowledge/chain-resolution-r3.md`, staged S106 `own-work` for `corpus/knowledge/citation-chain-fidelity-r24.md` (both exist: `ls -l` 15772 / 8931 bytes). None of staged S104/S105/S106 appears in `renumber.tsv`, which maps only ids cited by adopted entries, so their disposition is unrecorded and a future adoption must renumber them again.
The lesson's 22 is correct for its pre-append 103-row snapshot; read from the committed artifacts now it understates the landed state by 3.

## 5. Findings

**F1 — defect (evidence artifact contradicts the lesson and the landed state).** `corpus/lessons/round-50.md:39` says "staged S145 (CNKI 教师 manual) refused, no lane id" and attributes that content to `assimilation/renumber.tsv`. The committed, `git ls-files`-tracked file says otherwise:
```
$ grep -n S145 .ufo/waves/round-50/assimilation/renumber.tsv
6:S145	S107	append	bs.bnu.edu.cn/docs/20160407183946745914.pdf
$ grep -cE '^\|[[:space:]]*S107[[:space:]]*\|' corpus/SOURCES.md  -> 0
$ grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' .ufo/waves/round-50/assimilation/append.md -> 3
```
The refusal is what landed (106 rows, no S107, three appended rows), so the decision is right and the artifact is stale: the map still instructs `append S107` for the refused 教师 manual, and the lesson misdescribes the artifact it cites as its proof.
Residual risk: a later adopter run from `renumber.tsv` appends a row the Gate refused. The fix is one line in that map (or a regenerated one) plus the lesson sentence — neither is mine to write.

**F2 — calibration (adjacent, verified): `corpus/README.md:1079` calls the round-50 lesson "seven refused or deferred staged entries".** The lesson's Decisions table has 8 rows: 3 admit, 4 `refuse`, 1 `admit-later` (5 refused or deferred); "seven" occurs nowhere in the lesson (`grep -n "seven\|Seven" corpus/lessons/round-50.md` → no output), and only 5 staged entries name a theme URL (`grep -lE 'chaxin\.las\.ac\.cn|gs\.sxu\.edu\.cn|rwxy\.seu\.edu\.cn|bs\.bnu\.edu\.cn' merge/chousa/knowledge/corpus/knowledge/*.md` → r48, r41, r47, r40, r39). "Seven" has no reproducing command.

**F3 — method note (not a lane defect).** Validating a registry copy from a scratch directory reports E11 on every mined row (`used-by` resolves against the registry's parent, `sources-census.sh:567`); a bare-copy base run exits 1 with ~100 E11 lines. The clean mirror in §3 is the only valid base comparison and exits 0.

## 6. Owned elsewhere

`spans.tsv` / `c2-count.py` legs, the entries' prose and quote offsets are other seats' items. A peer lead that S105 span offsets were shifted was retracted by its author (the column is the span-block start, `CONTEXT=80`, not the quote position); I did not re-verify it and claim nothing.

## Tooling

No install, no upgrade, no fetch (L0 `8d77e6c1` open), no pacman transaction. Scratch `/dev/shm/chousa-r50-R50ExecCensusMirror/` deleted after the run.

VERDICT: attacked the landed registry's census — both paths (106 rows, 0 malformed, A93/B8/C5, mined82/queued19/rejected5, no duplicate ids, no enum violations, no missing used-by, exit 0, five pre-existing W04, identical to base+3 and to census.txt) — survived; and the section-10 collision pipeline — 25 collisions remain vs the Gate's 22 (21 hard, 4 re-staged; the 3 new ones hard and unmapped in `renumber.tsv`) — numbers hold, but defect found in the collision remedy's evidence: `renumber.tsv:6` still records `S145 → S107 append` for the document `round-50.md:39` calls refused and the landed registry does not carry.
