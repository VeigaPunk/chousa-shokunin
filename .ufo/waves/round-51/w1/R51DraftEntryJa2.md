# R51DraftEntryJa2 — lane entry for the Japanese search-record amendment (round 51 / wave 1)

Leaf scribe, no subagent dispatch. The only lane write is this report; the entry itself is in the fenced block below, labelled with its lane path, for the L1 to land. Scratch was `/dev/shm/chousa-r51-R51DraftEntryJa2/` (removed at the end). Nothing was installed or upgraded: pacman is paused host-wide and no tool was needed.

Lane read at `cfe6c9f` (C3-erratum tip); frozen claims at `d603f6f`, base `9ec1751`. Freshness: the newest capture read is the qcache pair `34fcefc159bf2ebbd1e09540.{txt,raw}` dated 2026-10-23 20:40 — two days old today, and it cannot move while L0 `8d77e6c1` (fetch scope) is open.

## 1. Evidence (commands run here, observed output)

1. Staged entry read in full: `/home/vgpnk/Projects/shokuknow/merge/chousa/knowledge/corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md` (2 `source:` lines, staged ids S125 and S126; body ids S097, S105, S106; Unknown's "remains unread … HTTP 000").
2. The lane entry it amends is **not on disk yet** — `ls corpus/knowledge/ | grep -i japan` prints nothing, `rc=1` (68 `.md` files in `corpus/knowledge/`, none named `japanese-*`), and `read corpus/knowledge/japanese-search-record-r38.md` → "Path … not found". It is referred to by path only, as instructed; its content is not restated.
3. Captures: `python3 -c "import hashlib;…"` over the two URLs gives `3a8b45977cd111e45e3980a5` (NIPH `.docx`) and `34fcefc159bf2ebbd1e09540` (JAHBS `.pdf`); `ls -la` shows for the first `3a8b…raw` 178056 B, `3a8b…txt` 319599 B, for the second `34fc…pdf` and `34fc…raw` 7787275 B, `34fc…txt` 47473 B.
4. Forms: `file` on the NIPH pair → `3a8b….txt: Zip archive data` and `3a8b….raw: Microsoft Word 2007+`; `zipfile.is_zipfile('3a8b….txt')` → `False` (its EOCD tail holds `\x1f\xef\xbf\xbd\x02`, the UTF-8 replacement character, so the `.txt` is a lossy UTF-8 decode of the zip). `z.getinfo('word/document.xml').compress_type` → `8` (DEFLATE), and the Japanese quote's UTF-8 bytes occur `0` times in the raw. So the document text exists only after unzipping `word/document.xml`.
5. Chosen S112 form: every `w:t` text of `word/document.xml` concatenated in document order, decoded UTF-8, **18478 characters**, no paragraph break represented. Its layout quirk, measured: the label cell and the value cell are consecutive runs, so `文献検索期間2015年1月から2018年10月まで` is one contiguous string in this form.
6. Chosen S113 form: `34fcefc159bf2ebbd1e09540.txt` read as UTF-8, **25811 characters**; the PDF's two columns interleave, so `プロバイダー` is split at the gutter (`プロバ` ends the left line, `イダー名` opens the right).
7. Quote locations, one command, all counts `1`: S112 at chars `8417 8441 8581 8724 8799 8809 8816`; S113 at chars `10140 10146 11229 11243 11294 11348 11457`. Longest quote 47 characters; longest by whitespace words 2 — both inside the 160-character / 25-word bar.
8. Negative sweep, run verbatim as printed in the entry: `python3 -c "…print(len(a),a.count('検索者'),len(b),b.count('検索者'))"` → `18478 0 25811 0` (S112 form length, 検索者 count, S113 form length, count).
9. PRISMA-translation sweep: key `f3dbe2fe59a684b1b94cfadc`; `ls -la …/f3dbe2fe59a684b1b94cfadc*` → one file, `f3dbe2fe59a684b1b94cfadc.fail`, `cat` → `rc=28`; no `.txt`, no `.raw`. `grep -rn lifescience corpus/` → 0 hits, so the lane names no lifescience.co.jp source at all (the staged entry's "round-3 copy of the checklist" is therefore not a lane row this entry can rest on, and the entry makes no PRISMA-2020 claim).

## 2. Located quotes

Forms: `S112` = the `.raw`'s `word/document.xml` `w:t` concatenation decoded UTF-8 (18478 chars); `S113` = the `.txt` read as UTF-8 (25811 chars). Each occurs exactly once in its stated form.

```
QUOTE	staged-id	url	quote	entry-path
QUOTE	S125	https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx	SRにおける文献検索期間について明記する	corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md
QUOTE	S125	https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx	文献検索終了時点は、分析枠組みが決定された後から製造販売業者による分析提出までの一時点に決める	corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md
QUOTE	S125	https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx	文献検索期間2015年1月から2018年10月まで	corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md
QUOTE	S125	https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx	声明(http://www.prisma-statement.org/)の原則に従い	corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md
QUOTE	S125	https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx	使用したデータベース	corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md
QUOTE	S125	https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx	使用した検索式	corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md
QUOTE	S125	https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx	ハンドサーチ等により未公表データを収集した場合は	corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md
QUOTE	S126	https://www.jahbs.info/journal/pdf/vol38_1/vol38_1_5.pdf	検索の特徴（検索期間	corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md
QUOTE	S126	https://www.jahbs.info/journal/pdf/vol38_1/vol38_1_5.pdf	検索期間，言語制限	corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md
QUOTE	S126	https://www.jahbs.info/journal/pdf/vol38_1/vol38_1_5.pdf	検索した文献データベース名	corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md
QUOTE	S126	https://www.jahbs.info/journal/pdf/vol38_1/vol38_1_5.pdf	Ovid などのプロバ	corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md
QUOTE	S126	https://www.jahbs.info/journal/pdf/vol38_1/vol38_1_5.pdf	検索の開始日と終了日を記載することで	corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md
QUOTE	S126	https://www.jahbs.info/journal/pdf/vol38_1/vol38_1_5.pdf	最新の結果を反映しているかどうか	corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md
QUOTE	S126	https://www.jahbs.info/journal/pdf/vol38_1/vol38_1_5.pdf	評価がしやすくなる	corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md
```

## 3. Gates run on the draft

- `python3 tools/inference-ground.py --entry <scratch>/entry.md --spans <scratch>/ev/spans.tsv --counts /dev/null --registry corpus/SOURCES.md --root .` → `GROUND entry=entry.md section=1 bullets=5 tokens=7 grounded=7`, `GROUND: PASS`, `rc=0`. The span manifest was built here from the real captures in the `build-spans` shape (7 S113 rows, digest `065b889a…`, span = exact slice `text[off-80:off+len+80]`).
- `python3 corpus/evidence/round51/quote-substance-check.py <scratch>/ev/spans.tsv` → `IDS=1 QUOTES=7 FAILURES=0`, `rc=0`.
- `python3 corpus/evidence/round29/prose-check.py <scratch>/entry.md` → `TOTAL hits=0 files=1`, `rc=0`.
- Id census: `grep -o 'S[0-9]\{3\}' entry.md | sort -u` → `S112 S113` only (no body-only token survives; the staged S097/S105/S106 are described, not numbered).
- `grep` of the seven span quotes against the entry → `7/7` present (C2's `QUOTES_IN_ENTRY` leg); `検索期間` present (C2's own term for this entry).
- `python3 corpus/evidence/round51/c2-count.py` read-only, before any landing → `ENTRIES=0/3 BOUND=0/7 … C2=FAIL rc=1` (the pre-wave state; I did not run c1/c3 and wrote nothing).

## 4. The entry  (label `corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md`)

```markdown
# The Japanese search record carries a stated 検索期間: an assessment form requires it, and a methods journal reports it as a PRISMA-P item

source: S112 — https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx — 国立保健医療科学院「医薬品及び医療機器の費用対効果評価に係る分析結果の記載様式と手引」[第2.0版] 2024年4月, sections 3.1 and 3.2: the window sentence (char 8417), the window-end rule (char 8441), the worked example's cells (char 8581), the PRISMA-principles sentence (char 8724), the database and strategy fields (chars 8799 and 8809) and the hand-search sentence (char 8816); form = every `w:t` text of the `.raw`'s `word/document.xml` concatenated in document order and decoded as UTF-8, 18478 characters, no paragraph break represented
source: S113 — https://www.jahbs.info/journal/pdf/vol38_1/vol38_1_5.pdf — 日本保健医療行動科学会雑誌 38(1), 2023, 60–69, 剱持貴史・岡美智代 "システマティックレビューとメタアナリシスの実施方法": step 6's PRISMA-P item sentence (chars 10140 and 10146) and step 7's database, provider and date sentence (chars 11229, 11243 and 11294) with its currency rationale (chars 11348 and 11457); the `.txt` read as UTF-8, 25811 characters
verified-at: 2026-10-25 — both captures re-opened from the read-only qcache and every quoted phrase re-located at its stated offset in its stated form; no fetch made (L0 `8d77e6c1` open)
recheck: 180d — from the lane root, `python3 corpus/evidence/round51/build-spans.py --check` re-derives the S113 rows and prints `SPANS_ROWS=n STALE=0`; the S112 offsets are re-derived only by unzipping the `.raw` member `word/document.xml` and concatenating its `w:t` texts, a form `build-spans` does not read (see Unknown)
ground: wave-1 queue Q6b — what a Japanese academic search-record standard requires a search record to carry — and Q12 — whether a Japanese source requires the searcher's identity as a field; **this is a dated amendment to `corpus/knowledge/japanese-search-record-r38.md`, which it adds to and does not replace**
adopted: round 51 from the campaign package merge/chousa/ — staged `knowledge/corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md`, its ids re-bound by document to this lane's S112 and S113 and its body-only ids dropped rather than renumbered

#### Observation

- **The institute's form requires the search window to be stated, and fixes where it may end.** Section 3.1's list reads "SRにおける文献検索期間について明記する" (`S112`, char 8417) and, in the next sentence, "文献検索終了時点は、分析枠組みが決定された後から製造販売業者による分析提出までの一時点に決める" (`S112`, char 8441) — the window's end sits between two named points in the assessment process, not at a free date.
- **Its worked example records the window as a table cell.** The research-question table's last two cells read "文献検索期間2015年1月から2018年10月まで" (`S112`, char 8581); the label and the value are adjacent here because the label cell's text run and the value cell's text run are consecutive in the form, so the adjacency is the form's and the paragraph break between them is not represented.
- **The same section names the database and the strategy as fields, and grounds them in PRISMA.** Section 3.2 opens "声明(http://www.prisma-statement.org/)の原則に従い" (`S112`, char 8724) and then lists "使用したデータベース" (char 8799) and "使用した検索式" (char 8809). The document is 国立保健医療科学院's own 記載様式と手引 ([第2.0版], char 33) for 医薬品及び医療機器の費用対効果評価 submissions, so what it requires is what that institute's assessments must carry — as this copy states.
- **The same section requires hand-searched unpublished data to be declared.** "ハンドサーチ等により未公表データを収集した場合は" (`S112`, char 8816) must be shown in the PRISMA flow chart, so the non-database part of the search has a place on the record.
- **A peer-reviewed Japanese methods journal reports 検索期間 as a PRISMA-P item.** Step 6's paragraph says PRISMA-P holds the protocol's minimum elements and names the search's features: "検索の特徴（検索期間" (`S113`, char 10140), "検索期間，言語制限" (`S113`, char 10146), beside unpublished material and abstracts.
- **Step 7 names three fields and gives the reason for keeping them.** "検索した文献データベース名" (`S113`, char 11229), the provider "Ovid などのプロバ" (`S113`, char 11243 — the two-column capture splits プロバイダー at the gutter, `プロバ` ending the left line and `イダー名` opening the right), and "検索の開始日と終了日を記載することで" (`S113`, char 11294). The reason follows in the same sentence: "最新の結果を反映しているかどうか" (char 11348) and "評価がしやすくなる" (char 11457).

#### Inference

- **The window is a named field in both documents, and the lane can now name it.** `検索期間，言語制限` (`S113`) is reported as a PRISMA-P protocol element, and `S112` asks a submitter to state the same window and to place its end between the framework decision and the manufacturer's submission. A lane row can carry a window field with a stated end rule, instead of a single search date.
- **The database and the provider are fields separate from the window.** `S113` names `検索した文献データベース名` and the provider beside `検索の開始日と終了日を記載することで`, and `S112` asks for the databases and the strategy used. A record carrying only a date range is incomplete by both.
- **The stated rationale is currency, and it is the lane's own recheck.** `最新の結果を反映しているかどうか` and `評価がしやすくなる` (`S113`): the record is kept so that a reader can judge whether the results are current and whether the search has been refreshed since. That is why a per-database date and a per-strategy date are one requirement in two literatures.
- **Both documents are scoped, and neither is a national standard.** `S112` is one institute's template, and it grounds its fields in PRISMA's principles; `S113` reports `検索の特徴（検索期間` as PRISMA-P's, in a society journal's methods article. The lane can say these two Japanese documents require the field, and cannot say a Japanese national standard does.
- **On Q12 the searcher is not a field in either document.** `検索した文献データベース名` and the dates are the record's identifying fields in `S113`, and `S112`'s field list holds the databases, the strategy and the window. The sweep over both stated forms counts no occurrence of 検索者 in either (both counts 0; the command and its printed output are in Unknown), so neither document names the searcher.

#### Unknown

- **The official Japanese translation of PRISMA 2020 was not opened in this lane's captures.** Sweep, from the lane root: `python3 -c "import hashlib;print(hashlib.sha256(b'https://www.lifescience.co.jp/yk/jpt_online/prisma/list_1.pdf').hexdigest()[:24])"` prints `f3dbe2fe59a684b1b94cfadc`, and `ls -la /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/f3dbe2fe59a684b1b94cfadc*` lists one file, `f3dbe2fe59a684b1b94cfadc.fail` holding `rc=28`; there is no `.txt` and no `.raw`, and `grep -rn lifescience corpus/` returns nothing, so the lane names no lifescience.co.jp source. This entry therefore makes no claim about PRISMA 2020's item text, and the searcher question is answered from the two documents it holds.
- **The 検索者 sweep, and its output.** From the lane root: `python3 -c "import zipfile,xml.etree.ElementTree as E,hashlib as H,pathlib as P;W='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}';C=P.Path('/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache');k=lambda u:H.sha256(u.encode()).hexdigest()[:24];a=''.join(e.text or '' for e in E.fromstring(zipfile.ZipFile(C/(k('https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx')+'.raw')).read('word/document.xml')).iter(W+'t'));b=(C/(k('https://www.jahbs.info/journal/pdf/vol38_1/vol38_1_5.pdf')+'.txt')).read_text(encoding='utf-8');print(len(a),a.count('検索者'),len(b),b.count('検索者'))"` prints `18478 0 25811 0` — the S112 form's length, its 検索者 count, the S113 form's length and its count.
- **Whether S112's requirement binds anything beyond that institute was not established.** The document is the institute's own 記載様式と手引 for its own assessments, and the passages read cite no statute, regulator or ministry.
- **The docx text form is outside the lane's span pipeline.** `build-spans.py` reads a capture as its `.txt` decoded UTF-8, then its `.raw` decoded UTF-16LE; the S112 phrases occur 0 times in the first form and 0 times in the second, because the `.txt` is a lossy UTF-8 decode of a zip and `word/document.xml` is stored DEFLATE-compressed (compress type 8), so no byte-level form exposes the text. This entry's S112 offsets therefore index the unzipped XML form, and its S112 quotes cannot be span-backed this round; they are re-located by the recheck command, not by the manifest.
- **The staged entry's body-only ids were dropped, not renumbered.** Three staged ids named only in that entry's body — a functional-foods notification form, a Chinese reporting module and a Chinese review's published record — name lane rows of other documents or of a round-3 form; no capture for them was opened here, so the sentences resting on them are gone, and Q12 is answered from the two documents this entry holds.
- **Staged material corrected on adoption.** The staged Unknown gave the translation's absence as a host result, HTTP 000 with zero bytes; that fetch is not reproducible in this lane and is replaced by the cache sweep above. The staged worked-example quote was one string, and the capture holds the label and the window in consecutive cells, so the adjacency is the form's. The staged "a national institute requires" wording is kept as that institute's own form, and the field list is extended to the database and the strategy fields the same section names.
```

## 5. Integration material

**(a) `corpus/evidence/round51/quotes.tsv` rows this entry needs** (header `id url quote entry`; every one occurs exactly once in `34fc…txt`, so `build-spans.py` derives them):

```
id	url	quote	entry
S113	https://www.jahbs.info/journal/pdf/vol38_1/vol38_1_5.pdf	検索の特徴（検索期間	corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md
S113	https://www.jahbs.info/journal/pdf/vol38_1/vol38_1_5.pdf	検索期間，言語制限	corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md
S113	https://www.jahbs.info/journal/pdf/vol38_1/vol38_1_5.pdf	検索した文献データベース名	corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md
S113	https://www.jahbs.info/journal/pdf/vol38_1/vol38_1_5.pdf	Ovid などのプロバ	corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md
S113	https://www.jahbs.info/journal/pdf/vol38_1/vol38_1_5.pdf	検索の開始日と終了日を記載することで	corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md
S113	https://www.jahbs.info/journal/pdf/vol38_1/vol38_1_5.pdf	最新の結果を反映しているかどうか	corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md
S113	https://www.jahbs.info/journal/pdf/vol38_1/vol38_1_5.pdf	評価がしやすくなる	corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md
```

**(b) S113 registry row** (`anchor` cell carries `char N` values that are exactly the offsets above, which is what C2's `ANCHOR_BOUND` leg reads):

`| S113 | 剱持貴史・岡美智代, システマティックレビューとメタアナリシスの実施方法 — https://www.jahbs.info/journal/pdf/vol38_1/vol38_1_5.pdf | paper | A | what this methods article states a systematic-review protocol and search record must carry, in its 14-step procedure | step 6's PRISMA-P item sentence (char 10140, char 10146) and step 7's database, provider and date sentence (char 11229, char 11243, char 11294) with its currency rationale (char 11348, char 11457); 日本保健医療行動科学会雑誌 38(1), 2023, 60–69, `.txt` read as UTF-8 | A review protocol states its search period and language limits, and its search record states the database, the provider and the start and end dates so that currency can be judged | mined | 2026-10-25 | 180d | corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md |`

**(c) S112 registry row — do not land as-is (see Finding F1).** The anchor cell below cannot satisfy `ANCHOR_BOUND`, because it names offsets in a form the frozen counter cannot read: `| S112 | 国立保健医療科学院, 医薬品及び医療機器の費用対効果評価に係る分析結果の記載様式と手引 [第2.0版], 2024年4月 — https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx | docs | A | … | section 3.1's window sentence (char 8417) … | … | mined | 2026-10-25 | 180d | corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md |`

**(d) Design B, if the L1 refuses S125** (the only design that lets the frozen C2 reach `ids_ok == nbound` and `anchors == nbound`): delete the `source: S112` line and the three S112-only Observation bullets (window sentence, worked example, database/strategy/hand-search — keeping the S113 bullets), and add to `corpus/lessons/round-51.md`: `refused-doc https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx — .docx text exists only inside a DEFLATE member; neither build-spans form nor c2-count's form_text reads it (0x/0x), so the document is refused, not quoted`. The entry's own term survives in Design B: `検索期間` comes from S113's `検索期間，言語制限`, so C2's `NEW_GROUND` leg still holds.

## 6. Findings

- **F1 (operability, blocks C2 for this document).** The docx's text is in no form the round reads. `build-spans.py` (`form_texts`, lines 66–77) tries `.txt` UTF-8 then `.raw` UTF-16LE; `c2-count.py`'s `form_text` (lines 107–118) re-derives from the recorded digest and accepts only those two files. Run in a scratch root: `python3 …/build-spans.py --root fake2` with three real S112 quotes → `build-spans: refused S112: quote not exactly once in any form (3a8b….txt:0x, 3a8b….raw:0x)` three times, `rc=1`. So a legitimately bound S112 has 0 quote rows, and `ids_ok == nbound` and `anchors == nbound` both fail — C2 cannot pass with S125 bound. Extending `build-spans` would not fix it, because the frozen `c2-count` re-derives the form from the digest.
- **F2 (shortcut, needs a control before the Gate reads C2).** The same legs ARE satisfiable without reading the document: 21 ASCII runs of 12+ characters occur exactly once in the lossy `.txt` (all zip member names, chars 167617–168323). Run in a scratch root with `word/document.xmlPK`, `word/theme/theme1.xmlPK`, `word/media/image1.pngPK` as S112 "quotes" → `QUOTE S112 char 167739 / 168194 / 168127`, `SPANS_ROWS=3 WRITTEN=3`, `rc=0`, digest `471e5589…` (the `.txt`). `CAPTURE_BOUND`, `QUOTES_IN_SPAN` and `ANCHOR_BOUND` would then pass with the entry pasting three filenames. This is the docx analogue of QUALITY 72's hollow-quote class: the frozen C2 measures "the span is a slice of the recorded form file", not "the document was read". If the L1 keeps S125 bound, that must be disclosed as a named limit and scored as a control; I did not use it in the entry.
- **F3 (staged corrections).** Body ids S097/S105/S106 dropped (their sentences are gone, per the assignment's rule); the staged `文献検索期間2015年1月から2018年10月まで` is exact only in the run-concatenated form — in a paragraph-joined form the label and value are separated, so the entry states the form and why the adjacency exists; the staged HTTP-000 fetch result is replaced by the cache sweep; the staged "national institute requires" is kept as that institute's own form, and "as this copy states" is used where the host is a publisher mirror.
- **F4 (depth gained, beyond the staged text).** The NIPH form also requires `使用したデータベース` and `使用した検索式` and grounds them in PRISMA's principles (`声明(…)の原則に従い`), and the JAHBS article reports `検索期間，言語制限` as a PRISMA-P item — so the 検索期間 requirement is attested by two documents, not one, and the entry can say why the field is required (currency) rather than only that it is.
- **F5 (what was not done).** No lane file other than this report; no counter edit; `c1-count.py` and `c3-count.py` were not run; no fetch; no install; scratch removed.

VERDICT: drafted the amendment entry against both captures (34 lines, `GROUND: PASS`, `QUOTES=7 FAILURES=0`, prose `0 hits`, ids `S112 S113` only) and falsified its S112 half — the docx text is in neither form the round's span pipeline reads (`0x/0x`, `rc=1`), while three zip-member names pass `build-spans` as S112 quotes, so the frozen C2 can bind S125 only degenerately or not at all.
