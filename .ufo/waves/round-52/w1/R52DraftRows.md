# R52DraftRows — four lane Registry rows for the round-52 search-record documents

Seat: leaf member, no dispatch. Lane HEAD `13bc280`; frozen base `00f8c7f5` (`git show 00f8c7f5:corpus/SOURCES.md | grep -oE '^\| S[0-9]{3}' | sort | tail -3` → `S110 S111 S112`; HEAD tail → `S111 S112`), so S113-S116 are free at both revisions (`grep -cE '^\| S11[3-6] '` → `0` at HEAD and `0` at base). No existing row carries any of the four URLs (`grep -c medsci.cn|chinagp.net|niph.go.jp|lifescience.co.jp corpus/SOURCES.md` → `0`; base → `0`), so each appended row is the single `url_of()` hit the C2 counter needs. Every source is an on-disk capture; no network. Staged ids name other lane documents and are not carried over. `opened` = 2026-10-26 (today, per the C2 predicate).

## 1. Rows — corpus/SOURCES.md

Append at the end of `## Registry`, after S112, in this order (ascending id). Each is one line, 11 cells, no `|` in a cell.

```markdown
| S113 | 系统评价/Meta分析中文献检索报告清单（PRISMA-S）解读（郑卿勇）— 梅斯医学 指南・解读指南, a portal copy of a 中国循证医学杂志 item — https://www.medsci.cn/guideline/show_article.do?id=23e481c0052069d3 | docs | B | a commercial portal's copy of a Chinese item-by-item reading of PRISMA-S and of its limits as a reporting standard; the portal page and its abstract mirror, not the journal's own copy, whose attachment the record prices (paymentAmount=10) | 简要介绍 block, page 发布日期 2026-04-25 (record id 23e481c0052069d3); capture .txt read as UTF-8, 8,804 characters; char 2377 | PRISMA-S is the PRISMA 2020 extension giving the search half a 16-item 专项规范, and this reading tests it item by item for cross-disciplinary generality and its intrinsic limits as a 报告规范, recommending practice for Chinese databases | mined | 2026-10-26 | 180d | corpus/knowledge/chinese-prisma-s-reception-r52.md |
| S114 | 中国全科医学 报告清单 — PRISMA2020条目清单 (a Chinese rendering of the PRISMA 2020 checklist) — 《中国全科医学》编辑部 — https://www.chinagp.net/CN/column/item185.shtml | docs | A | a Chinese journal's own published PRISMA 2020 checklist, including its per-source search-date and complete-strategy items, as the journal states them; not PRISMA's own wording | the 报告清单 table, item 6 信息来源 and item 7 检索策略; page 发布日期 2023-01-31; capture .txt read as UTF-8, 6,179 characters; char 1650 | item 6 requires every source consulted to be named together with the 检索或查询日期 of each, and item 7 the complete search strategy for every database, registry and website including the filters and limits used | mined | 2026-10-26 | 180d | corpus/knowledge/chinese-prisma-s-reception-r52.md |
| S115 | 提出様式（日本語）Reporting_Format_Jap_202404 — 国立保健医療科学院 C2H（Evidence to Decision）— https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx | docs | A | the search-record fields a Japanese national institute's own health-technology-assessment submission form requires, as that institute states them | section 3 追加的有用性, 3.1 システマティックレビューのリサーチクエスチョン, in the .docx text form through tools/capture-text.py (19,682 characters; the cache .txt sidecar is not this document), capture .raw sha256 prefix 16fc8c55ee856fef; char 8996 | the form requires the SR's search period to be stated explicitly, fixes its end at one point between the analysis framework being decided and the analysis being submitted to the manufacturer, and requires hand-searched unpublished data to appear in the PRISMA flow chart | mined | 2026-10-26 | 180d | corpus/knowledge/japanese-search-record-niph-form-r52.md |
| S116 | 「PRISMA 2020 チェックリスト」（日本語訳, JPT ONLINE, ライフサイエンス株式会社）— archived copy — https://web.archive.org/web/2024/https://www.lifescience.co.jp/yk/jpt_online/prisma/list_1.pdf — the original https://www.lifescience.co.jp/yk/jpt_online/prisma/list_1.pdf no longer serves the file | docs | B | the Japanese-language wording of PRISMA 2020's own information-source and search-strategy items, as the official translation renders them, read at a web-archive copy because the publisher's host no longer serves the file | the checklist table's 情報源 (item 6) and 検索戦略 (item 7) rows; archived PDF text (.txt) read as UTF-8, 5,328 characters, capture .raw sha256 prefix ba9bc9c14cd0b89f; char 753 | item 7 requires the complete search strategy for every database, registry and website including the filters and limits used, item 6 each information source with the date it was last searched, and the term 検索者 occurs nowhere in the document | mined | 2026-10-26 | 180d | corpus/knowledge/japanese-prisma-item-wording-r40.md |
```

S116's source cell puts the ARCHIVE URL first (the C2 counter reads the first URL; `url_of` → `web.archive.org/web/2024/https://www.lifescience.co.jp/yk/jpt_online/prisma/list_1.pdf`) and keeps the dead original visible after it, with content (not only the pointer) in the anchor.

## 2. Tier, one line each

- **S113 B** — MedSci is a commercial portal reproducing another journal's item: the record's own JSON carries `guiderFrom=中国循证医学杂志` and `paymentAmount=10`, so it is a secondary host, never the journal of record, for a scope about what the reading says.
- **S114 A** — 《中国全科医学》编辑部's own site publishing its own 报告清单 (`发布日期：2023-01-31`, 冀ICP footer): first-party for "what this journal publishes", not tier A for PRISMA 2020's own wording.
- **S115 A** — 国立保健医療科学院's own form on its own domain (`c2h.niph.go.jp`): the institute is the author of the submission requirement it states.
- **S116 B** — a web-archive copy of a publisher PDF, not the publisher; per the lane's own S084 (RFC 7089 §2.1.1, §7) an archive's veracity is out of the document's scope, so the copy is strong secondary for the translation's wording, and the pointer correction rests on content, not on the redirect.

## 3. Stripped prose (the `recheck` cell carries only the cadence; this is what the lesson Gate records)

| id | `recheck` cell | stripped prose, as run |
|---|---|---|
| S113 | 180d | 180d — re-open the page and confirm the 简要介绍 still names the 16 条目 and the 中文数据库 challenge (ran 2026-10-26; capture .txt, char 2377) |
| S114 | 180d | 180d — re-open the page and confirm item 6 still ends 明确说明每一项来源 的 检索或查询日期 (ran 2026-10-26; capture .txt, char 1650) |
| S115 | 180d | 180d — re-download the .docx and run tools/capture-text.py over it, confirming SRにおける文献検索期間について明記する at char 8996 of a 19,682-character text form (ran 2026-10-26; --locate LOCATED count=1 offset=8996) |
| S116 | 180d | 180d — re-fetch the archived PDF and confirm 項目7 still reads 用いたフィルターや制限も含め， and 試験登録，Web サイトの完全な検索戦略を記載する。 (ran 2026-10-26; .txt chars 641 and 753) |

## 4. Gate quotes (machine lines, exact; two per document so each id can carry its ≥3 span rows)

All ten occur exactly once in the stated form, are ≤25 whitespace words and ≤160 characters, and were copied from the form bytes.

```
QUOTE	S111	https://www.medsci.cn/guideline/show_article.do?id=23e481c0052069d3	为文献检索报告提供了包含16个条目的专项规范。本文旨在对PRISMA-S进行系统性中文解读，基于其原始发布文献，在逐条阐释其内涵与要求的基础上，进一步探讨其跨学科的普适性、作为“报告规范”的内在局限，并针对中文数据库等本土化应用挑战提出实践建议	corpus/knowledge/chinese-prisma-s-reception-r52.md
QUOTE	S111	https://www.medsci.cn/guideline/show_article.do?id=23e481c0052069d3	作为“报告规范”的内在局限，并针对中文数据库等本土化应用挑战提出实践建议	corpus/knowledge/chinese-prisma-s-reception-r52.md
QUOTE	S112	https://www.chinagp.net/CN/column/item185.shtml	详细说明获取文献的所有来源，包括 所有数据库、注册平台、网站 、 机构 、参考列表以及 其他 检索或咨询 途径 。明确说明每一项来源 的 检索或查询日期 。	corpus/knowledge/chinese-prisma-s-reception-r52.md
QUOTE	S112	https://www.chinagp.net/CN/column/item185.shtml	呈现 所有数据库、注册平台和网站的 完整 检索策略，包括 用到的 过滤器和限制条件。	corpus/knowledge/chinese-prisma-s-reception-r52.md
QUOTE	S112	https://www.chinagp.net/CN/column/item185.shtml	发布日期：2023-01-31	corpus/knowledge/chinese-prisma-s-reception-r52.md
QUOTE	S125	https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx	SRにおける文献検索期間について明記する。なお、文献検索終了時点は、分析枠組みが決定された後から製造販売業者による分析提出までの一時点に決める。	corpus/knowledge/japanese-search-record-niph-form-r52.md
QUOTE	S125	https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx	ハンドサーチ等により未公表データを収集した場合は、そのことを上記のフローチャートに含める。	corpus/knowledge/japanese-search-record-niph-form-r52.md
QUOTE	S129	https://web.archive.org/web/2024/https://www.lifescience.co.jp/yk/jpt_online/prisma/list_1.pdf	試験登録，Web サイトの完全な検索戦略を記載する。	corpus/knowledge/japanese-prisma-item-wording-r40.md
QUOTE	S129	https://web.archive.org/web/2024/https://www.lifescience.co.jp/yk/jpt_online/prisma/list_1.pdf	用いたフィルターや制限も含め，	corpus/knowledge/japanese-prisma-item-wording-r40.md
QUOTE	S129	https://web.archive.org/web/2024/https://www.lifescience.co.jp/yk/jpt_online/prisma/list_1.pdf	最後に調べられた日付を記載する。	corpus/knowledge/japanese-prisma-item-wording-r40.md
```

Offsets in the stated form (python `find`; `count` in brackets): S111 2377 [1] and 2463 [1] in the `.txt` read as UTF-8 (8,804 chars); S112 1650 [1], 1785 [1], 5744 [1] in the `.txt` (6,179 chars); S125 8996 [1] and 9428 [1] in the capture-text form of the `.raw` (19,682 chars; the `.txt` sidecar is not this document); S129 753 [1], 641 [1], 601 [1] in the archived PDF `.txt` (5,328 chars). The anchor `char N` is the first quote of each document (S113 2377, S114 1650, S115 8996, S116 753).

NIPH `--locate`, verbatim:

```
$ python3 tools/capture-text.py .../3a8b45977cd111e45e3980a5.raw --locate 'SRにおける文献検索期間について明記する。なお、文献検索終了時点は、分析枠組みが決定された後から製造販売業者による分析提出までの一時点に決める。'
LOCATED count=1 offset=8996
exit=0
```

## 5. Checks run

```
$ python3 tools/capture-text.py .../3a8b45977cd111e45e3980a5.raw | wc -m    # 19682 (1239 lines) — the C2 claim's figure
$ python3 tools/capture-text.py .../3a8b45977cd111e45e3980a5.raw --locate 'SRにおける文献検索期間について明記する'
LOCATED count=1 offset=8996
```
Census, run on a scratch copy (`cp corpus/SOURCES.md $S/census.md`, four rows inserted after S112; scratch only, lane untouched):
```
rows: 116            (head 112 + 4)
malformed: 0
tiers: A=100 B=11 C=5   (head A=98 B=9 C=5 → +2 A, +2 B)
status: mined=92 queued=19 rejected=5
dup ids: (none)
enum violations: (none)
missing used-by paths: the four r52 entry paths (see §6)
```
C2-shaped parse (imported `c2-count.py`'s own `registry`, `url_of` against the scratch copy): S113/S114/S115/S116 → `cells 11`, `firstURL_match True`, `status mined`, `opened 2026-10-26`, `used_ok True`, and `new since base: ['S113','S114','S115','S116']`.

## 6. Integration requirements (else these rows read as unbound)

1. **`quotes.tsv` must carry the offsets the anchors name** — every `char N` in an anchor cell must be a `spans.tsv` offset for that id (`c2-count.py` `ANCHOR_BOUND`). The three quotes per Chinese/archived document in §4 give the span seat ≥3 locatable rows each; if the seat prefers round-51's shorter locators (S111 2463, S112 1707, S129 641) it must carry the §4 first quote as well, or the anchor's `char` must be changed to the offset it does carry (mine: 2377 / 1650 / 8996 / 753).
2. **The staged r40 entry must be renumbered on landing**: `japanese-prisma-item-wording-r40.md` holds `S129` ×4 and `S097` ×1 (`grep -o 'S[0-9]\{3\}'` → `S097 1`, `S129 4`). It must read `source: S116 — https://web.archive.org/web/2024/…` and `S129`→`S116` everywhere, and `S097`→`S108` (the lane row for the jaohfa 機能性表示食品 form), or `REF_ID_UNBOUND` ≥1 and C2 fails. The two new entries must cite only their bound ids (S113/S114 for `chinese-prisma-s-reception-r52.md`, S115 for `japanese-search-record-niph-form-r52.md`).
3. **The three `used-by` paths must exist when the rows land** — they do not at HEAD (`ls corpus/knowledge/{japanese-prisma-item-wording-r40,japanese-search-record-niph-form-r52,chinese-prisma-s-reception-r52}.md` → three `No such file`), so rows and entries integrate in one append; the frozen census's missing-`used-by` check reads the four paths until then.
4. Rows are appended in id order and never edited in place: `status`, `recheck`, `used-by` only (contract rule 2).

## 7. Round-51 routed defects this seat touched

- **Pointer corrections need a content anchor** — S116 anchors the checklist's own row labels (情報源 / 検索戦略) plus `char 753` in the archived text, and keeps both URLs in one cell with the archive first; it does not rest on the redirect alone.
- **The NIPH refusal was a capture-form refusal** — S115's scope and anchor name the form (`tools/capture-text.py`, 19,682 characters) and say the cache `.txt` sidecar is not this document, so a later recheck cannot re-read the garbage sidecar as the source.
- The other routed items (nonce counter, adopter twin-id `held` label and refusal ordering, the SKILL one-shot-counter note) are counters/adopter/SKILL work, not Registry rows; untouched here.

## 8. Known limits

- Tier is judged from capture bytes only (network closed, L0 `8d77e6c1`): S113's `paymentAmount=10` is the portal's own JSON field, an access signal, not a tested paywall; S116's "the original no longer serves the file" is inherited from round 51's gate table (`the row's own URL key f3dbe2fe59a684b1b94cfadc is absent`) and was not re-tested this round.
- The 19,682-character agreement between `capture-text.py` and `build-spans.py` is the freeze's own checked figure; I re-read the tool's output (19,682) and did not re-run the builder.
- No row here decides C2: whether all four documents are bound (4/4) or one is refused is the counter's reading; these rows are drafted so all four can bind, and binding fewer leaves the refusal duty (§6.2 aside) to the lesson's `refused-doc` line.
- Scratch `/fast/scratch/hyaku/chousa-r52/R52DraftRows/` was used for the census copy and the NIPH text form only, and is removed.

VERDICT — built the four lane Registry rows (S113-S116) off the four staged rows and their captures: census-clean (11 cells, 0 malformed, 0 dup, 0 enum violations), C2-parse-clean (single first-URL hit each, `mined`, `opened 2026-10-26`, `used-by` exact, new since `00f8c7f5`), with ten located Gate quotes and the NIPH `LOCATED count=1 offset=8996` receipt; the attack it leaves live is the anchor-`char`/spans coupling in §6.1, which the span seat or L1 must close.
