# R52DraftEntryNiph — draft `corpus/knowledge/japanese-search-record-niph-form-r52.md`

seat: R52DraftEntryNiph (leaf, no dispatch). Lane repo `/home/vgpnk/Projects/shokunin/chousa-shokunin`,
base `00f8c7f5272a1d98b6d34913985fa4537e00aaf9`; read-only cache
`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache`; no network, no fetch (L0 `8d77e6c1` open).
Scratch `/fast/scratch/hyaku/chousa-r52/R52DraftEntryNiph` (removed at exit). No tool installed.
Writes: this report only — no lane product file, no SOURCES row, no lesson, no counter, no git/jj mutation.

## What I did

Drafted the entry from the NIPH half of the staged package entry
`/home/vgpnk/Projects/shokuknow/merge/chousa/knowledge/corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md`,
bound to lane id S115 (`S125 -> S115`; lane registry maximum at base is S112, verified with
`grep -o '^| S[0-9]*' corpus/SOURCES.md | sort -V | tail -3` → S110, S111, S112).
I opened both lane companions before writing and refer to them by path only.

Capture-form work: the `.raw` is a zip; its text form was produced by the round-52 tool, and the
span offsets were re-derived independently by the builder's own reader — the two agree.

| command (cwd = lane root) | observed |
|---|---|
| `python3 tools/capture-text.py .../3a8b45977cd111e45e3980a5.raw > niph.txt` | exit 0; `wc -m` = `19682`; `\n` 1239, `\t` 49, `\r` 0 |
| builder `raw_form(raw)` vs the tool's stdout | `builder len 19682 tool len 19682 equal True`; raw sha256 `16fc8c55ee856fefbbfc88b391b08233106b337e43aaf9f7a7bd825adeb09763` |
| `python3 tools/capture-text.py RAW --locate '<quote>'` × 7 | `LOCATED count=1 offset=` 1445, 8996, 9020, 9189, 9408, 9419, 9428; rc 0 each |
| sidecar `python3 -c "s=open('...3a8b45977cd111e45e3980a5.txt','rb').read().decode('utf-8','replace');print(len(s),s.count(chr(0xfffd)))"` | `168953 72117` (file 319,599 bytes; `検索` 0, `SRにおける` 0) |
| sweep searcher: tool stdout piped over `('検索者','検索担当','誰が','担当者','実施者','司書')` | `19682 [0, 0, 0, 0, 0, 0]` |
| sweep dates over `('検索日','最終検索','検索した日','データベース毎','各データベース','文献検索期間')` | `19682 [0, 0, 0, 0, 0, 2]` |
| sweep expression over `('検索式','完全な検索式','検索戦略','検索ワード','検索語','プラットフォーム','Ovid','プロバイダ')` | `19682 [1, 0, 0, 0, 0, 0, 0, 0]` |
| sweep PRISMA over `('PRISMA-S','PRISMA')` | `19682 [0, 1]` |
| sweep statute over `('法律','省令','通知','義務','罰則','遵守','中央社会保険医療協議会','分析ガイドライン第4版')` | `19682 [0, 0, 0, 0, 0, 0, 1, 1]` |
| `grep -rl 検索者 corpus/knowledge/` | the two search-record entries, rc 0 (no notification-form entry to point at) |
| `grep -c フローチャート` in both companions | `0`, `0` |
| `git grep -l -e 文献検索期間 -e 完全な検索戦略 -e 检索报告清单 00f8c7f5… -- corpus/knowledge` | nothing, rc 1 (the C2 NEW_GROUND premise holds for this term) |
| source-line regex (`^source:\s*S115\s+—\s*<url>(\s|$)`) against the draft | `SOURCE_LINE_MATCH True` |
| builder in a scratch lane tree (7 rows, `quotes.tsv`) | `QUOTE S115 char 1445 … 9428`; `SPANS_ROWS=7 WRITTEN=7`, rc 0 |
| `tools/inference-ground.py --entry draft --spans scratch/manifest --counts /dev/null --registry corpus/SOURCES.md` | `GROUND entry=entry.md section=1 bullets=5 tokens=8 grounded=8` · `GROUND: PASS`, rc 0 |
| `corpus/evidence/round51/quote-substance-check.py scratch/manifest` | `IDS=1 QUOTES=7 FAILURES=0`, rc 0 |
| per-row re-check (quote in span / in entry / ≤25 words / ≤160 chars / span longer / span == form slice at offset) | `ALL_OK 7 / 7` |

Two drafts failed before the pass and are reported, not hidden: `INF_TOKEN_NOT_IN_SPAN token='19,682'`
(an Inference bullet carried the character count; figure removed) and `INF_UNGROUNDED bullet=4`
that bullet then had no quoted phrase; a span phrase was added.

## The entry (lane path `corpus/knowledge/japanese-search-record-niph-form-r52.md`)

```markdown corpus/knowledge/japanese-search-record-niph-form-r52.md
# The NIPH assessment form requires a stated search window, fixes the window's end, and names the database and the expression used — but no searcher (round 52)

source: S115 — https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx — 3.1システマティックレビューのリサーチクエスチョン (the window sentence and the end-point sentence) and 3.2システマティックレビューの結果 (the PRISMA disclosure list and the hand-search clause) of the 記載様式, with the 記入にあたっての基本的な注意事項 that names the 分析ガイドライン; the capture `.qcache/3a8b45977cd111e45e3980a5.raw` is a zip and its text form is `python3 tools/capture-text.py RAW` — 19,682 characters, 0 U+FFFD, raw sha256 `16fc8c55ee856fefbbfc88b391b08233106b337e43aaf9f7a7bd825adeb09763`; located quotes char 1445, char 8996, char 9020, char 9189, char 9408, char 9419, char 9428
verified-at: 2026-10-26 — the `.raw` re-read from the read-only campaign cache through `tools/capture-text.py`, and each quote below re-located with that tool's `--locate`; no fetch made (L0 `8d77e6c1` open)
recheck: 365d — `python3 tools/capture-text.py /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/3a8b45977cd111e45e3980a5.raw --locate 'SRにおける文献検索期間について明記する。'` must print `LOCATED count=1 offset=8996`, and the same command without `--locate` piped to `wc -m` must print 19682, with the seven quotes below once each
ground: what a Japanese health-technology-assessment submission form requires a search record to carry, and what it leaves out, as this copy states it — **a new entry, not an amendment**: it neither restates nor replaces the two lane entries it cites by path, `corpus/knowledge/japanese-search-record-r38.md` and `corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md`, whose second document is the other half of the staged pair this entry comes from; the round-51 refusal of this form was a refusal of its capture form, not of its source quality
adopted: round 52 from the campaign package merge/chousa/ (staged japanese-search-record-r38-amendment-2026-10-23.md)

#### Observation

- **What this copy is.** The cover reads 医薬品及び医療機器の費用対効果評価に係る分析結果の記載様式と手引, `[第2.0版]`, 国立保健医療科学院, 2024年4月: a template plus guidance for a 費用対効果評価 submission, with 記載様式 sections 0–8. Its 記入にあたっての基本的な注意事項 binds the analysis to the 分析ガイドライン and to the 分析枠組み decided by the 費用対効果評価専門組織.
- **The form requires the search window as one instruction, and fixes only its end.** The last instruction of 3.1 reads `SRにおける文献検索期間について明記する。` (char 8996) and continues `文献検索終了時点は、分析枠組みが決定された後から製造販売業者による分析提出までの一時点に決める。` (char 9020): the reviewer states the period, and the end of it is one point inside a stated stretch of the assessment process — after the analysis framework is decided, before the manufacturer's analysis is submitted.
- **The worked example fills the window as a range.** The 3.1 (例) table's closing row is labelled `文献検索期間` and filled `2015年1月から2018年10月まで` (char 9189): a start month and an end month, so the field is a range and not a single search date.
- **3.2 adds three PRISMA-shaped disclosure items and one hand-search clause.** Following `PRISMA(Preferred Reporting Items for Systematic Reviews and Meta-Analyses)声明`, the copy lists what to show clearly, among them `臨床研究の組み入れ基準や除外基準`, `使用したデータベース` (char 9408) and `使用した検索式` (char 9419); and `ハンドサーチ等により未公表データを収集した場合は、そのことを上記のフローチャートに含める。` (char 9428), with `承認申請に用いたデータは未公表のものでも含めることを推奨する。` as a recommendation beside it.
- **The capture form, and why the offsets here are where they are.** The cache `.txt` sidecar of this `.docx` is the zip bytes decoded with replacement: 319,599 bytes read as 168,953 characters with 72,117 U+FFFD and no 検索 at all, so it is a lossy decode and no quote can be located in it (`python3 -c "s=open('/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/3a8b45977cd111e45e3980a5.txt','rb').read().decode('utf-8','replace');print(len(s),s.count(chr(0xfffd)))"` prints `168953 72117`). The tool's text form of the same `.raw` is 19,682 characters with 0 U+FFFD; every `char N` above and below is an offset into that form (`text.find` in the tool's `--locate`). The round-51 lesson records the window sentence at `char 39411` against "form .raw unzipped → word/document.xml UTF-8": in that member's decoded XML the sentence occurs zero times (the runs split it), it occurs once in the concatenated `w:t` text and once in this form (8996), and 39411 locates it in neither.

#### Inference

- **The form requires a window and constrains only where it stops.** `SRにおける文献検索期間について明記する。` is the requirement, and `文献検索終了時点は、分析枠組みが決定された後から製造販売業者による分析提出までの一時点に決める。` fixes the end inside the assessment process, so a row can carry a start and an end and need not carry a per-search rationale for either (S115).
- **The database and the expression are disclosure items at the PRISMA step, not a strategy document.** 3.2 names `使用したデータベース` and `使用した検索式` among what must be shown clearly, so what this copy asks for is what was searched and what was run, shown on the results page; it asks for no per-database strategy, no platform and no provider (the sweeps in Unknown) (S115).
- **The hand-search clause is the form's only non-database requirement, and it lands in the flow chart.** `ハンドサーチ等により未公表データを収集した場合は、そのことを上記のフローチャートに含める。` requires a hand search that produced unpublished data to be visible in the flow chart, which is a reporting slot rather than a field of the search record; neither companion entry by path carries a flow chart (0 occurrences of フローチャート in both) (S115).
- **No searcher is named, and the absence is measured rather than argued.** The form's search statements are the window sentence and the 3.2 items `使用したデータベース` and `使用した検索式`, and the sweep in Unknown counts no 検索者, no 検索担当 and no party term in the text form, so the fields the two companion entries by path state for other Japanese documents — a last-search date per database and an attachment carrying the searcher, the words and the expression — are not fields of this form (S115).
- **As this copy states it, the basis is a council's guideline and not a statute.** The 注意事項 reads `「中央社会保険医療協議会における費用対効果評価の分析ガイドライン第4版(以下、分析ガイドライン)」及び費用対効果評価専門組織で決定された分析枠組みに基づき対象品目を分析すること。`, and the sweep counts no 法律, 省令, 通知, 義務, 罰則 or 遵守, so what the form adds to a search record is a submission template's instruction under that guideline; a statutory footing is not shown here (S115).

#### Unknown

- **The form names no searcher.** Sweep, from the lane root: `python3 tools/capture-text.py /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/3a8b45977cd111e45e3980a5.raw | python3 -c "import sys;t=sys.stdin.read();print(len(t),[t.count(w) for w in ('検索者','検索担当','誰が','担当者','実施者','司書')])"` prints `19682 [0, 0, 0, 0, 0, 0]`. This is the question the lane's Q12 asked, answered on this form's own text: the searcher is not a field here, and nothing in the copy asks who ran the search.
- **There is no per-source or per-database search date, only one window for the review.** The same command over `('検索日','最終検索','検索した日','データベース毎','各データベース','文献検索期間')` prints `19682 [0, 0, 0, 0, 0, 2]`: the window term occurs twice (the 3.1 instruction and the example's row label) and no per-database or per-source date term occurs at all. A record can satisfy this form with one window while the companion entries by path ask a Japanese record for a last-search date per source.
- **There is no complete strategy, no platform and no provider.** The same command over `('検索式','完全な検索式','検索戦略','検索ワード','検索語','プラットフォーム','Ovid','プロバイダ')` prints `19682 [1, 0, 0, 0, 0, 0, 0, 0]`; the single 検索式 is the `使用した検索式` item. So the expression is required as a thing used and shown, and a strategy document, a database platform and a provider name are not.
- **PRISMA is named once and PRISMA-S never.** The same command over `('PRISMA-S','PRISMA')` prints `19682 [0, 1]`; the one PRISMA adopts the statement's 原則 at 3.2 and borrows no item-level wording. Whether the Japanese PRISMA 2020 item text agrees is a different document, read at its web-archive copy by the round-52 entry `corpus/knowledge/japanese-prisma-item-wording-r40.md`; this entry does not rest on it.
- **No statutory instrument is named.** The same command over `('法律','省令','通知','義務','罰則','遵守','中央社会保険医療協議会','分析ガイドライン第4版')` prints `19682 [0, 0, 0, 0, 0, 0, 1, 1]`. The copy names the council and the fourth edition of its guideline once each and no statute, so whether the council's guideline has a statutory footing, and whether a submission that omits the window is refused, are not shown by this capture.
- **Whether submissions in practice carry the window is untested.** This copy is a template with one worked example; nothing in it records a submitted analysis, so the entry states what the form requires and not what filers do. It also binds one scheme: the 記載様式 is for 費用対効果評価 submissions under the council's 分析ガイドライン, and nothing in it claims to govern Japanese review reporting generally.
- **Staged material corrected on adoption.** The staged pair is split by document: its methods-journal half is the lane entry `corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md`, which is not restated here, and this entry adopts only the form, bound to S115 rather than to a staged id; the staged body ids are dropped, not renumbered, and no staged id is carried over. The staged inference that the searcher's identity is absent from both documents is replaced by the measured sweep above, and the staged pointer to a round-3 notification form that files the searcher on an attachment has no lane file to point at: `grep -rl 検索者 corpus/knowledge/` names only the two search-record entries, so that pointer is dropped rather than followed.
```

## Quotes for `quotes.tsv` / spans / lesson (machine lines, staged id S125)

Seven rows; each occurs exactly once in the capture text form (the `.raw` through `tools/capture-text.py`),
is ≤25 whitespace words and ≤160 characters, and is inside the entry above.

```
QUOTE	S125	https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx	「中央社会保険医療協議会における費用対効果評価の分析ガイドライン第4版(以下、分析ガイドライン)」及び費用対効果評価専門組織で決定された分析枠組みに基づき対象品目を分析すること。	corpus/knowledge/japanese-search-record-niph-form-r52.md
QUOTE	S125	https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx	SRにおける文献検索期間について明記する。	corpus/knowledge/japanese-search-record-niph-form-r52.md
QUOTE	S125	https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx	文献検索終了時点は、分析枠組みが決定された後から製造販売業者による分析提出までの一時点に決める。	corpus/knowledge/japanese-search-record-niph-form-r52.md
QUOTE	S125	https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx	2015年1月から2018年10月まで	corpus/knowledge/japanese-search-record-niph-form-r52.md
QUOTE	S125	https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx	使用したデータベース	corpus/knowledge/japanese-search-record-niph-form-r52.md
QUOTE	S125	https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx	使用した検索式	corpus/knowledge/japanese-search-record-niph-form-r52.md
QUOTE	S125	https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx	ハンドサーチ等により未公表データを収集した場合は、そのことを上記のフローチャートに含める。	corpus/knowledge/japanese-search-record-niph-form-r52.md
```

Builder output for those rows (scratch tree, `--root <scratch> --cache <qcache>`):
`QUOTE S115 char 1445` · `8996` · `9020` · `9189` · `9408` · `9419` · `9428`; `SPANS_ROWS=7 WRITTEN=7`.
These seven numbers are also the only `char N` in the entry's `source:` line, so a Registry `anchor` cell
holding all or any of them satisfies the C2 anchor leg; `char 1445`, `8996`, `9020`, `9189`, `9408`,
`9419`, `9428` are all quote offsets in the tool's form.

## Handoff requirements this draft does not perform (other seats' bytes)

- SOURCES.md row: id S115, ten cells, first source cell `… — https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx`,
  kind `docs`, tier per Gate, `mined`, opened `2026-10-26`, `used-by` exactly
  `corpus/knowledge/japanese-search-record-niph-form-r52.md`.
- `corpus/evidence/round52/quotes.tsv` rows above (header `id url quote entry`), then `build-spans.py`.
- `corpus/lessons/round-52.md`: each of the seven quotes must appear in the lesson (C2 `QUOTES_IN_LESSON`),
  plus the `refused-doc` line for whichever document the round refuses (this one is bound, so no `refused-doc`
  line naming its URL) and the register verdict lines.
- The entry carries no `S###` token except S115 (`sorted(set(...))` → `['S115']`), so `REF_ID_UNBOUND`
  contributes nothing from it.

## Findings / limits

- **Round-51 lesson offset is not a locatable anchor.** `corpus/lessons/round-51.md:89` records
  `SRにおける文献検索期間について明記する。` at `char 39411` with form "`.raw` unzipped → word/document.xml
  UTF-8". Measured on that member: the sentence occurs **0** times in the decoded XML (element runs split it),
  once in the concatenated `w:t` text, once at 8996 in the round-52 text form, and once at 9729 in a
  tag-stripped decode (`len 20592`). 39411 locates it in none of those forms — an instance of the routed
  "content anchor for pointer corrections" defect (round-51 spot-check §6 item 4), reported, not repaired here.
- **This is a capture-form capability read, not a compliance finding.** The entry states what the copy
  requires; the sweeps are Unicode substring counts over one text form of one template and do not test
  any submitted analysis, nor any other institute's or the council's own guidance document.
- **`inference-ground` is lexical** (QUALITY 66/67 limits): the pass shows each bullet's quoted phrases and
  figures occur in the cited spans with no measured polarity flip, not that the inference is entailed.
- The staged id could not be carried over and staged body ids could not be written into the entry at all
  (any `S###` other than a bound id fails C2), so the staged corrections are stated in prose without tokens.

VERDICT — built and self-checked the S115 entry (7 single-occurrence located quotes in the `.docx` text form, three negative sweeps plus a statute sweep, `inference-ground` PASS 8/8 tokens, substance 7/7), and attacked the round-51 lesson's `char 39411` anchor, which locates the sentence in no derived form.
