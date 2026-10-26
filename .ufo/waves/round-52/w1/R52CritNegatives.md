# R52CritNegatives — falsification sweeps on inherited negative claims

Seat: R52CritNegatives (leaf critic, round-52 w1). Attacked: the staged negative
claims round 52 may inherit — the two staged titles in
`japanese-prisma-item-wording-r40.md` and
`chinese-search-log-r37-amendment-2026-10-23.md`, and every `does not`/`no`/
`none`/`未` sentence in the staged entries feeding the three C2 documents.
No subagents (leaf bound); no installs needed (pacman not touched; no tool
installed). Only write: this report. Sweeps use the capture text forms:
Archive `e84bfe97808591d23fe3266f.txt` (pdftotext -layout of the archived PDF),
Medsci `453d492becd9a2f4632cb8dd.txt`, Chinagp
`cacddf3bbf780a4c7582bb17.txt`, NIPH = `capture-text.py` output for
`3a8b45977cd111e45e3980a5.raw` (sidecar `.txt` is garbage for the `.docx`).

## NIPH text form (tool) — command and output

```
$ cd /fast/scratch/hyaku/chousa-r52/R52CritNegatives
$ python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/capture-text.py \
    /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/3a8b45977cd111e45e3980a5.raw \
    > niph.txt 2> niph.err; echo "exit=$?"
exit=0
$ wc -m niph.txt
19682 niph.txt
$ python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/capture-text.py \
    /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/3a8b45977cd111e45e3980a5.raw \
    --locate 'SRにおける文献検索期間について明記する'; echo "exit=$?"
LOCATED count=1 offset=8996
exit=0
```

Sweep harness: `sweeps.py` in scratch (counts + context windows per term per
form; it reads the four forms above, `len()` = characters). Key counts:

| Form (chars) | searcher-denoting terms | positive controls |
|---|---|---|
| Archive (5328) | 検索者=0, サーチャー=0, searcher=0, 検索担当/実施/作業/を行/をする/した/する者=0, 誰が/だれが/だれ=0 | 検索=4, 検索戦略=2, 情報源=2, データベース=2, 組織=1, 文献リスト=1, 助言=1, 日付=1 |
| Medsci (8804) | (n/a) | 解读=14, 标准=1, 规范=10, 国家标准=0, 郑卿勇=3, 中国循证医学杂志=2, paymentAmount=1, haveAttachments=1 |
| Chinagp (6179) | (n/a) | 标准=4, 规范=3, 国家标准=0, 国际报告规范=1, 检索或查询日期=1, Page=1, BMJ=1, 2021=1, n71=2, 发布日期：2023-01-31=1 |
| NIPH (19682) | 検索者=0 + variants=0 | 文献検索期間=2 (検索期間 at 9004/9183; the full sentence at 8996), ハンドサーチ=1 (9428), 研究者=1 (19530) |

## Attack 1 — r40 title/inference: "PRISMA 2020's own Japanese wording names no searcher"

Sweep: all searcher-denoting terms above on Archive; plus whole-document role-noun
scan. Result: 0 searcher terms; the only person-roles in the whole extraction are
`レビューア`=2 (item 8 screeners, item 11 risk-of-bias assessors), `レビュー担当者`=1
(item 9 data collectors), `レビュー著者`=1 (item 26 conflicts), `資金提供者/主宰者`
(item 25) — none performs or names the search. Item texts verbatim:
item 6 at offsets 475/555/592: `すべてのデータベース，研究登録，Web サイト，組織，文献リスト，研究を特定するために調べたり，助言を求めた情報源を記載する。それぞれの情報源が最後に調べられた日付を記載する。`; item 7 at 641/753: `用いたフィルターや制限も含め，すべてのデータベース，試験登録，Web サイトの完全な検索戦略を記載する。` Verdict: SUPPORTED for the archived Japanese extraction.

Overreach note: inference L34 says "not a PRISMA field" — that reads a whole-standard conclusion from one translation extract; the English original is not on disk (L0 open). Narrowed wording for the entry: **"items 6–7 of the archived Japanese translation name the sources, the last-searched dates and the strategy, and name no searcher; the only person-role counts near the search phase are item 8's number of screeners (and items 9/11 for extraction/risk-of-bias assessment); whether the English original names a searcher is not checked here."**

## Attack 2 — r40 observation: "The term 検索者 does not occur anywhere in the extracted text"

Sweep as above. 検索者=0 (also spaced/tokened variants, capital variants, `searcher`, `サーチャー`). Verdict: SUPPORTED verbatim on the Archive extraction.

## Attack 3 — r38-amendment unknown (L66): negative "rests on the round-3 copy of the checklist, not on the translation itself"

No longer inherited as a defect: the r40 sweep above now grounds the negative in the primary-translation extraction (検索者=0). Resolution recorded; nothing to carry.

## Attack 4 — grey-literature r40 (L47-56): "PRISMA 2020's items do not carry [non-database disclosure] … the omission is in PRISMA itself"
Sweep on Archive: 灰色文献=0, ハンドサーチ=0, 未公表=0, 未発表=0, 非データベース=0 — but item 6 (offset 475/592) names `組織` and `文献リスト` and "助言を求めた情報源" (organisations, reference lists, other routes consulted). Verdict: FALSIFIED as stated — PRISMA 2020 item 6 does carry a non-database source disclosure. Narrowed sentence: **"PRISMA 2020 item 6 requires naming sources including organisations, reference lists and other routes, but asks no discrete 'was grey literature searched' question and names no unpublished-material categories (conference papers, dissertations, industry/consultancy reports), as the NIPH form and the NMPA guideline do."**

## Attack 5 — NIPH-form negative (r38-amendment L45–53, carried into `japanese-search-record-niph-form-r52.md`): "the searcher's identity appears in neither [form nor journal]"

Sweep on NIPH tool form (19682 chars): 検索者=0 and variants=0; the single `研究者` at 19530 is the advisory-experts clause ("協力を受けた研究者の個人名や所属については原則として公開しない"), not a searcher field; positive controls confirm the form's actual search-record fields — `文献検索期間について明記する` (8996), `使用した検索式` and `ハンドサーチ等により未公表データを収集した場合は、そのことを上記のフローチャートに含める` (9428). Verdict: SUPPORTED for the NIPH form; sweep must use the tool form, not the sidecar. The Chinese-half of the same sentence (S116/S117) is NOT sweepable on my captures (PDFs not provided) — can remain Unknown until reopened.

## Attack 6 — chinese-search-log-r37-amendment title/inference: "The Chinese answer is a reception, not a standard"; "No Chinese national search-reporting standard was found, and none is claimed."

Sweep on Medsci + Chinagp:
- Medsci: self-describes as `解读` (14×); `报告清单`=7; the only `标准` occurrence is "标准孕产护理" (unrelated); `国家标准`=0; meta `中国循证医学杂志` (guiderFrom field in raw; attachment filename `系统评价_Meta分析中文献检索报告清单（PRISMA-S）解读_郑卿勇.pdf`); `paymentAmount=10`, `haveAttachments=1`; body: "PRISMA-S(PRISMA for Searching)作为PRISMA 2020的扩展版本，为文献检索报告提供了包含16个条目的专项规范。本文旨在对PRISMA-S进行系统性中文解读…" (2328/2377/2400).
- Chinagp: nav `国际报告规范` (330); page renders the translated checklist as `清单`/`报告清单` (23, 284); item 6 at 1707 `明确说明每一项来源 的 检索或查询日期 。`, item 7 at 1785 `呈现 所有数据库、注册平台和网站的 完整 检索策略，包括 用到的 过滤器和限制条件。`; footer attribution at 5530 `From: Page MJ, … The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. BMJ 2021;372:n71. doi: 10.1136/bmj.n71`; `发布日期：2023-01-31` (5744); `国家标准`=0; all 4 `标准` are "criteria" inside checklist item text.
Verdict: SUPPORTED for the two pages (one portal-article interpretation, one journal-published translation; neither self-describes as a national standard). Overreach: the title generalizes "the Chinese answer" literature-wide. Narrowed sentence: **"the two Chinese pages the lane reached are a reception — 梅斯医学's PRISMA-S 解读 article (2026-04-25; attachment sold) and 中国全科医学's translated PRISMA 2020 checklist (2023-01-31, attributed to BMJ 2021;372:n71) — not a Chinese national search-reporting standard; the 'none is claimed' half is guaranteed only for the swept pages, and whether any such national standard exists remains open (keep the Unknown)."**

## Attack 7 — r39 title: "China has no standard for one yet"; and L75–78 "one journal's series is not a national standard … whether any Chinese body has issued a national standard for SR reporting is still not established"

Not sweepable on my four captures: the underlying evidence is S116/S117 (实验动物与比较医学 PDFs), not provided to this seat. The on-disk row quote is the module-3 note "no reporting standard yet exists specifically for animal-experiment systematic reviews" — one journal article's statement, not a China-wide finding. Narrowed wording: **"S116 states no reporting standard yet exists specifically for animal-experiment systematic reviews and advises PRISMA; whether any Chinese national standard for SR reporting exists remains open."** The second half (one journal's series ≠ national standard) is fine as a scope statement.

## Attack 8 — Chinese searcher-absence (r39 L67–70; r38-amendment L71–74): "neither S116's module list nor S117's own record names the person who ran the search"

Same out-of-capture constraint (S116/S117 PDFs absent). Must stay Unknown in the r52 entries, not carried as carried fact. Note the Japanese pair (検索者 in S097) is untouched.

## Misc
All `未` strings in the staged entries are quoted capture language (灰色文献是指未在同行期刊上公开发表的文献; 未发表的学位论文), not claims — no action. No tool installed/updated; no repo writes besides this report; scratch removed at end.

## VERDICT
Attacked 8 inherited negatives: 2 supported verbatim (r40 検索者 sweep; NIPH-form searcher absence), 1 falsified as stated (grey-literature "PRISMA 2020's items do not carry non-database disclosure" — item 6 names organisations/reference lists/other routes), 3 need the narrowed sentences above (reception title; "not a PRISMA field"; r39 "China has no standard"), 2 not sweepable on the given captures and must stay Unknown (Chinese searcher absence; Chinese national-standard existence). Narrowed sentences provided for each; recommend L1 adopt them in the three entry drafts and keep the corresponding Unknown blocks.
