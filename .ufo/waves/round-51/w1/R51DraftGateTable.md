# R51DraftGateTable — assimilation Gate table draft (round 51, wave 1)

Seat `R51DraftGateTable`. Drafts `corpus/lessons/round-51.md` `## Gate` → `### Decisions`.
No production edit: the L1 integrates. Columns are the assignment's seven; the lane's
round-49 and round-50 Gate used five (`entry | decision | reason | flip | evidence`), so the last
five drop into that shape and the first two become the round's re-opened-sources table. Axes
named (godspeed): operability (does each decision rest on a command?), depth (every unadopted
neighbour covered, not only the three), calibration (are the province calls and the keys exact?).

## What I read (read-only)

- package `/home/vgpnk/Projects/shokuknow/merge/chousa/`: `MERGE-REPORT.md`, `SOURCES.append.md`
  (114 rows), `knowledge/corpus/knowledge/*.md` (55 files) plus `amendments/corpus/knowledge/*.md`
  (3 files) = the 58 entries the report counts.
- lane `/home/vgpnk/Projects/shokunin/chousa-shokunin/`: `PROVINCE.md`, `corpus/QUALITY.md`,
  `corpus/README.md`, `corpus/SOURCES.md` (106 rows), `corpus/lessons/round-49.md`,
  `corpus/lessons/round-50.md:34-151` (the Gate shape this table follows), and the frozen
  `corpus/evidence/round51/claims.md` (C2's three-entry set and C1's body-only rule bind here).
- captures `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache` (6,871 files;
  key = `sha256(url)[:24]`, `.txt` text form, `.raw` original bytes).

## Facts the table rests on

**F1 — the id spaces collide.** Staged ids S082–S195 (114 rows); lane registry S001–S106
(`grep -cE '^\| S[0-9]{3} ' corpus/SOURCES.md` → `106`) → 25 ids collide, S082–S106 (the 25
staged ids at or below 106). Renumbering starts at S107, the mapping the assignment already fixes.
**F2 — four staged rows are documents the lane holds.** Staged S100, S101, S102, S103 carry the
same URLs as lane rows S100–S103 (`S102` = the 東方書店 CNKI KNS8.0 PDF, `S103` = the CNKI AI guide,
identical strings); round 50's `### Collision check` records the same four as re-staged.
**F3 — body ids name other documents in the append namespace.** `S071` = GNU `env(1)` manual,
`S072` = Bash Reference Manual, `S079` = RFC 7089, `S097` = FEVER, `S105`/`S106` = lane own-work
rows (`chain-resolution-r3.md`, `citation-chain-fidelity-r24.md`). Every body id in a staged entry
must be dropped or re-described by document — the class round 49's adopted line records.
**F4 — the PRISMA-S text is on no capture.** A scan of all 2,549 `.txt` files (`ls -1 *.txt | wc -l`)
finds the checklist string `copied and pasted exactly as run` 0 times; the S082 capture is 267
characters of Cloudflare interstitial (`Client Challenge`).
**F5 — two entries' rows point at a capture that does not hold their document.** S090's row URL
(`_article/-char/ja`, key `02b3b0e8…`, 3,542 characters) has 参照 0 times; the article PDF is a
separate capture (`_pdf/-char/ja`, key `58b1b564…`, 6,242 characters, quote at 3785). S129's row
URL (the dead original, key `f3dbe2fe…`) has no capture at all; the archived PDF does
(`e84bfe97…`).
**F6 — one document, two staged rows.** S133 and S111 both hash to `453d492becd9a2f4632cb8dd`.
**F7 — the theme terms are new.** `git grep -nE '検索式|検索期間|检索策略' 9ec1751a -- corpus/knowledge/`
→ no hits, 0 files (C2's `NEW_GROUND` leg, re-derived at BASE_REV).
**F8 — the three admitted entries already carry their own theme term:** 検索式 ×2 (r38),
检索策略 ×2 (r39), 検索期間 ×3 (amendment).

## The Gate table (draft, for `corpus/lessons/round-51.md` §Gate)

```
| staged entry | documents (S-ids) | capture on disk (yes/no, key) | province fit | decision | reason | flip |
|---|---|---|---|---|---|---|
| `japanese-search-record-r38.md` | S109→S107, S110→S108 | yes: `7194acc65a18f6555e4b8893` (.txt, 21,216 chars), `62be15a474e866e4bef6c9d5` (.txt, 39,676) | in: what a search record must carry (search-strategy taxonomy) | **admit** (C2) | both quotes located (chars 10234, 4409); the entry states its own limit (neither source is a national standard); body id S105 is the lane's own-work row and must be stripped | the round's C2 entry set re-freezes, or a capture shows a Japanese national standard for a search record |
| `chinese-search-record-r39.md` | S116→S109, S117→S110, S119→S111 | yes: `fd468a36d78ff156b6200946` (.txt, 52,208), `c7266931a1731db3ff6ae77d` (.txt, 50,952), `42bac8830527d6f1bb125c49` (.txt, 2,065) | in: same | **admit** (C2) | 3/3 quotes located (chars 15310, 11404, 695); body id S097 is FEVER in this namespace and must be stripped; its `ground:` names `corpus/knowledge/chinese-search-log-r37-amendment-2026-10-23.md`, a path the lane holds only if row 7 lands | same re-freeze, plus row 7 admitted or that pointer rewritten to the package path |
| `japanese-search-record-r38-amendment-2026-10-23.md` | S125→S112, S126→S113 | yes: `3a8b45977cd111e45e3980a5` (.raw = .docx; quote only in `word/document.xml` with tags stripped, char 9729), `34fcefc159bf2ebbd1e09540` (.txt, 25,811, char 11294) | in: same | **admit** (C2) | 2/2 located; body ids S097, S105, S106 must be stripped; it amends row 1, so it appends after it | same re-freeze |
| `search-log-fields-r36.md` | S082, S083, S090 | **no for the tier-A leg**: `01f657b3d0ab045c494b3f92` (.txt, 267 chars = "Client Challenge"); `14aaa168a5cb4d833ca78b0b` (.txt, 210,708, char 112450); S090 row URL `02b3b0e8…` holds the landing page (参照 0) while the PDF is `58b1b564…` (char 3785) | in: it is the field list itself | **refuse** | its central authority is not on disk: the PRISMA-S string it quotes occurs 0 times in every `.txt` in the cache, and 2 of its 3 legs cannot be re-opened from the row as written | a PRISMA-S full-text capture (item-8 string present) plus S090's cell re-pointed to `_pdf/-char/ja`; then admit with the Cochrane leg unchanged |
| `search-tracking-record-r40.md` | S134 | yes: `0ae65ac01b93119d3c2f3fed` (.txt, 27,659, char 1334) | in: a tracking record's columns | **admit-later** | tier A; capture and quote pass; off this round's theme (the western reading) and a fourth entry sits outside the frozen three; body ids S069, S094, S114, S130 name other documents here | next round's entry set or a C2 re-freeze; no capture work left |
| `chinese-search-log-r37.md` | S102, S103, S104 | yes: `7809d5114330a60527436b07` (.txt, 17,317, 专业检索 3764), `02aefcf570a7108e699d0990` (.txt, 8,590, 溯源 780), `3d7b23e68f13add5cfae634b` (.txt, 68,091) | in | **refuse** | superseded: its lead finding (no Chinese-language search-log specification was found) is contradicted by S111/S112, which this round does admit; 2 of its 3 documents are held rows (F2); body ids S071/S072/S079 name the GNU env manual, the Bash manual and RFC 7089 | if the lane wants the superseded reading as a dated appendix: heading marked superseded, the two held-document rows de-duplicated, all body ids stripped |
| `chinese-search-log-r37-amendment-2026-10-23.md` | S111, S112 | yes: `453d492becd9a2f4632cb8dd` (.txt, 8,804, char 2463), `cacddf3bbf780a4c7582bb17` (.txt, 6,179, char 1707) | in | **admit-later** | carries the strongest on-theme field evidence the three do not (the per-source search date in Chinese), but it amends the file row 6 refuses and it is a fourth entry | either row 6 lands as a labelled superseded reading, or this entry's `ground:` cites S111/S112 directly and drops the base pointer; then next round |
| `japanese-prisma-item-wording-r40.md` | S129 | yes, at the archive: `e84bfe97808591d23fe3266f` (.txt, 5,328, char 641); the row's own URL key `f3dbe2fe59a684b1b94cfadc` is absent | in: PRISMA's own Japanese wording | **admit-later** | the document is on disk and its negative is verified (検索者 0 times), but the row's `source` cell names the dead original and its recheck says "confirm 項目7", a string that occurs 0 times in the capture (the row is labelled 検索戦略 with number 7) | row URL re-pointed at the archive with the dead original kept visible, recheck naming the 検索戦略 row; then next round |
| `grey-literature-and-chinese-search-record-r40.md` | S130, S131, S133 | yes: `bdff491a75c6abeda1d9c01d` (.raw, OLE .doc, UTF-16LE decode, char 57497), `27d4865f201e99c1fed9f79b` (.txt, 1,858, char 780), `453d492becd9a2f4632cb8dd` (= S111's document) | **out of province for its spine** (a regulator instrument's currency); in province only for the field sentence | **refuse** | the entry leaves the guideline's currency unresolved and that question is NMPA/legal ground (PROVINCE: out of province, report, never absorb); S133 and S111 hash to one key, so the package would append two rows for one page; the field claim is already carried by the admitted row 2 (S116 module 3, 灰色文献的检索与记录 at char 15310) | the owning lane settles the guideline's status and S133 merges into S111; then the field sentence returns as a dated addendum to row 2 |
| `grey-literature-and-chinese-search-record-r41.md` | S142 | yes: `be6963bbc94761282fea066e` (.txt, 19,352, char 7176) | in (methodological practice), but a conduct claim, not a record field | **refuse** | as staged it carries no located quote (1 backtick span and 0 double-quoted spans in 2,253 characters; every claim is paraphrase), it rests on one tier-B mirror of a 协和医学杂志 paper, and its own Unknown calls it "an argument for the practice, not a requirement" | a primary publisher copy in the cache and the entry rewritten with at least one located quote per claim (the definition sentence sits at char 7176) |
```

## Notes the table compresses

- **The seven C2 documents all have a capture with a located quote (7/7).** The `BOUND>=5` and
  `BOUND+REFUSED=7` legs are satisfiable on the capture side alone; the row-append and `used-by`
  legs are the L1's, and no `refused-doc` line is needed for any of the seven. Rows 4, 6, 9, 10 are
  refused, so their quote lines below are capture evidence for the flip conditions, not span
  candidates for this round.
- **Two quote forms are not `.txt`.** S125 exists only as the `.docx` body (`word/document.xml`,
  tags stripped: the run is split across `<w:t>` elements, so a byte search on the raw XML fails);
  S130 exists only as a UTF-16LE decode of the OLE `.raw` (its `.txt` is those OLE bytes read as
  UTF-8, where 灰色文献 is 0 times). `build-spans.py` must generate both forms or those span legs
  fail — a concrete integration constraint for C2.
- **Row 2's `ground:` pointer and rows 6/7's `amends` chain are one problem**: the staged amendments
  form a linked list whose predecessor the round does not adopt. A middle link cannot land while its
  predecessor is refused without either rewriting the pointer or leaving a lane path that never exists.

## Located quotes (machine lines; each occurs exactly once in the stated form)

Forms: all `.txt` read as UTF-8 except S125 (tag-stripped `word/document.xml` of the `.docx`) and
S130 (UTF-16LE decode of the OLE `.raw`); S090's and S129's URLs are the re-pointed ones.

```
QUOTE	staged-id	url	quote	entry-path
QUOTE	S109	https://www.jstage.jst.go.jp/article/kenkokyoiku/32/2/32_320208/_pdf/-char/ja	その日時，使用した検索式を同時に記録しておく	corpus/knowledge/japanese-search-record-r38.md
QUOTE	S110	https://jaohfa.com/pdf/systematic_review.pdf	検索者、検索ワード、検索式	corpus/knowledge/japanese-search-record-r38.md
QUOTE	S116	https://www.slarc.org.cn/dwyx/EN/article/downloadArticleFile.do?attachType=PDF&id=5290	灰色文献的检索与记录	corpus/knowledge/chinese-search-record-r39.md
QUOTE	S117	https://www.slarc.org.cn/dwyx/CN/article/downloadArticleFile.do?attachType=PDF&id=5237	从各数据库建立至 2024 年 4 月 1 日	corpus/knowledge/chinese-search-record-r39.md
QUOTE	S119	https://www.sinomed.ac.cn/article.do?ui=2026335073	来源出版物： 中国循证医学杂志 卷：26 期：4	corpus/knowledge/chinese-search-record-r39.md
QUOTE	S125	https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx	SRにおける文献検索期間について明記する。	corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md
QUOTE	S126	https://www.jahbs.info/journal/pdf/vol38_1/vol38_1_5.pdf	検索の開始日と終了日を記載することで	corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md
QUOTE	S083	https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-04	Document the search process in enough detail to ensure that it can be reported correctly in the review	corpus/knowledge/search-log-fields-r36.md
QUOTE	S090	https://www.jstage.jst.go.jp/article/jjsme/105/2/105_17/_pdf/-char/ja	著者名（出版年）．文献名．URL（参照日）	corpus/knowledge/search-log-fields-r36.md
QUOTE	S134	https://jmla.pitt.edu/ojs/jmla/article/download/1449/2061	number of records identified from each information source	corpus/knowledge/search-tracking-record-r40.md
QUOTE	S102	https://www.toho-shoten.co.jp/export/sites/default/cnki/help/cnki-kns80.pdf	专业检索	corpus/knowledge/chinese-search-log-r37.md
QUOTE	S103	https://library.um.edu.mo/upload/databases/c1b0fa89e2809581b12c79b9c60ea1af.pdf	溯源	corpus/knowledge/chinese-search-log-r37.md
QUOTE	S111	https://www.medsci.cn/guideline/show_article.do?id=23e481c0052069d3	作为“报告规范”的内在局限	corpus/knowledge/chinese-search-log-r37-amendment-2026-10-23.md
QUOTE	S112	https://www.chinagp.net/CN/column/item185.shtml	明确说明每一项来源 的 检索或查询日期	corpus/knowledge/chinese-search-log-r37-amendment-2026-10-23.md
QUOTE	S129	https://web.archive.org/web/2024/https://www.lifescience.co.jp/yk/jpt_online/prisma/list_1.pdf	用いたフィルターや制限も含め，	corpus/knowledge/japanese-prisma-item-wording-r40.md
QUOTE	S130	http://www.gcpunion.org/upload/cmsfile/1703404975484107.doc	是否检索灰色文献等关键问题	corpus/knowledge/grey-literature-and-chinese-search-record-r40.md
QUOTE	S131	http://m.cnpharm.com/201906/18/c280684.html	指导原则分为概述、方法学要点、报告撰写规范、指导原则所依据的参考文献和附录五个方面	corpus/knowledge/grey-literature-and-chinese-search-record-r40.md
QUOTE	S142	https://www.medsci.cn/article/show_article.do?id=c92c8431e130	灰色文献是指未在同行期刊上公开发表的文献	corpus/knowledge/grey-literature-and-chinese-search-record-r41.md
```

## Limits of this draft

- I ran no frozen counter: `c1-count.py`, `c2-count.py`, `c3-count.py` are the wave's, and the
  assignment forbids running them. Every number here comes from my own read-only probes.
- Province calls are mine. `PROVINCE.md` states the regulator/legal boundary only as "out of
  province → report, never absorb"; the NMPA/legal attribution is the assignment's, not a line I
  read in a lane file. I decided only the ten entries in this neighbourhood; the other 48 staged
  entries were not assessed.
- I did not re-verify the quoted CJK runs against the original PDFs, only against the cache
  captures, and I did not test whether any capture is a stale revision of its document. Nothing
  was installed or upgraded (no tool was needed; no `pacman` call was made).

VERDICT: drafted the round-51 Gate table for all ten search-record entries — 3 admit, 3 admit-later, 4 refuse with firing flips — grounded each capture by cache key and char offset, and found the refusal grounds in the captures themselves: the PRISMA-S checklist is on no capture (0 occurrences of its item-8 string, S082's capture a 267-character challenge page), two entries' rows point at captures that do not hold their document (S090, S129), and one document is staged twice (S133 and S111 share key `453d492b…`).
