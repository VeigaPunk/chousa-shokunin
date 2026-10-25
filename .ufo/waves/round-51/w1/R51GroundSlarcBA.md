# R51GroundSlarcBA — re-ground staged S117 against its capture

Seat: R51GroundSlarcBA (leaf). Target: staged S117 — 实验动物与比较医学 2025;45(1):101-111, section 3
文献特征分析, the 检索策略 paragraph — in `corpus/knowledge/chinese-search-record-r39.md`.

## Capture identity and form

- `.txt` form: `c7266931a1731db3ff6ae77d.txt`, **50952 characters**, read as UTF-8 (69789 bytes,
  sha256 `03342b7d…fe2dd`). All offsets below are `text.find(quote)` in that form.
- Key check: `sha256(url)[:24]` for the staged URL printed `c7266931a1731db3ff6ae77d` — matches the filename.
- `.raw` form: 1140215 bytes, `PDF document, version 1.4, 11 page(s)`. Cross-extraction with
  `pdftotext 26.08.0 -enc UTF-8` (37190 chars) carries the same paragraph, the same term lists and the
  same wide tracking (`题 词 （MeSH/Emtree） 和 关 键 词`), so the spacing is in the PDF text layer, not one
  extractor's artifact.
- Both files mtime `2026-10-23 20:39:30 -0300`, consistent with the entry's `verified-at: 2026-10-23`.
- Article identity in the capture: `1674-5817（2025）01-0101-11` @1633 (11 pages from 101 → 101-111);
  the running head at @0 begins with `Feb. 2025, 45(1)` (11 occurrences, one per page) and ends its first
  line with the folio 101; the 引用本文 block @48962 gives `实验动物与比较医学, 2025, 45` @49175 with
  `(1): 101-111. DOI: 10.12300/j.issn.1674-5817.2024.109.` (twice — the Chinese and English self-citations);
  PDF is 11 pages. Journal, volume, issue, page range all carried.
- The search paragraph runs @11211–12390 under `3 动物实验 SRs/MAs 中应用 GRADE 方法的` @10990 +
  `文献特征分析` @11110 — the entry's "section 3, the 检索策略 paragraph" locates correctly.
- Extraction hazard: two columns interleave, splitting `Meta 分…析` and `fruit…fly` across breaks, and the
  justified right column carries per-character spaces. `主题词` and `自由词` therefore return **0** hits in
  this form; `检索` returns 5 (11211, 11334, 11428, 21867, 25865).

## Located quotes — what each supports, what it does not

1. `中国知网、万方、中国生物医学文献数据库、` @11213 — supports the first three named databases in that
   order. Does **not** support exhaustiveness, nor that any named database is animal-experiment-specific.
2. `PubMed、Embase 和 Web of Science 数据库，检索时间` @11299 — supports the three non-Chinese databases and
   the spaced form `Web of Science`; falsifies the entry's rendering `WebofScience`. Does **not** support any
   per-database strategy or thesaurus assignment.
3. `从各数据库建立至 2024 年 4 月 1 日` @11404 — supports coverage from each database's establishment to
   2024-04-01. Does **not** support a search execution date, an update date, or per-database inception dates.
4. `（MeSH/Emtree） 和 关 键 词` @11505 — supports subject headings MeSH/Emtree combined with keywords. Does
   **not** support `自由词`/free text (absent), a Boolean operator, or MeSH→PubMed / Emtree→Embase assignment.
5. `“动物实验”“鼠”“兔”“狗”“犬”“蛙”“蟾蜍”“猴”` @11609 — supports the Chinese list's opening 8 of 15 terms
   (list closes `析 ” 等` @11798); 狗 and 犬 both present, 动物模型/小鼠/大鼠 absent. Does **not** support
   completeness.
6. `“animal model”“mice”“rat”“rabbit”“dog”“frog”` @11910, `“toad”“monkey”“ape”“pig”“swine”“paniscus”`
   @12019, `“bonobo”“chimpanzee”“gorilla”“pongo”“fish”“fruit` @12125 — support 21 English terms, including
   five primate taxa and `animal model` with no Chinese counterpart. Do **not** support the lists being
   translations of each other (15 Chinese vs 21 English; 狗/犬 collapse to one `dog`).
7. `“systematic review”“meta-analysis” 等` @12278 — supports that the English list is explicitly truncated by
   等 (etc.). Does **not** support an executable strategy.
8. `共得到 42 篇使用 GRADE 方法的动物实验 SRs/MAs` @12390 — supports that this search fed a bibliometric count
   (39 English / 3 Chinese within t[11780:12800]), i.e. a survey of GRADE use. Does **not** support an SR protocol.
9. `郑卿勇、许建国和李艺羿进行文献检索与数据提取` @25850 — supports that the document names three people who ran
   the search, in the 作者贡献 statement (heading @25567). Does **not** support these being a *field of the
   search record* — they are not.
10. `制定符合动物实验研究特点的 SRs/MAs 报告规范` @1384 — supports that S117's own abstract calls for a
    reporting standard for animal-experiment SRs/MAs. Does **not** support that such a standard exists.

## Staged claims about this document that the capture does not carry

- **"A Chinese review"** — the capture's title @382 is `提高动物实验系统评价/Meta 分析的证据确定性…实证研究`
  and its section label @226 is `比较医学研究与报告规范` / @315 `Guidelines for Comparative Medical Research and
  Reporting`; `综述` count 0. The capture carries a Chinese methodological **empirical study** in a reporting-
  guidelines section, not a review and not a systematic review.
- **"names every database searched"** — six databases are named; the sentence asserts no completeness, and none
  of the six is animal-experiment-specific, so S117 does not exhibit the S116 module's "animal-experiment-
  specific databases" element it is offered as the exemplar of.
- **"a search record a reader can re-run"** — the strongest overclaim. The paragraph has no Boolean operator
  (the only `AND`/`OR` hits, @28043/28246/34082/36227/40605/35749/45611, are reference-list surnames), no field
  tags, no per-database syntax, no execution date, and both term lists end 等. The capture carries a **summary
  of coverage and terms**, not a re-runnable strategy.
- **"controlled terms (MeSH/Emtree) with keywords"** — carried (Q4) only as `结合` (combined) with no operator;
  "free text" is the lane's gloss, not the capture's word.
- **recheck "confirming module 3"** — module 3 is not in this document: `表3`, `表 3` and `模块` all count 0. The
  entry's single recheck sentence spans three items across two documents; for S117 only the 2024-04-01 bound and
  the journal/volume/issue are checkable, and both pass.

## Falsified / to be corrected at integration

- **Falsified:** Unknown bullet "Neither S116's module list nor S117's own record names the person who ran the
  search … Q12 stays open." For S117 this is false — @25850 names 郑卿勇、许建国和李艺羿. Only the narrower
  claim ("the searcher's identity is not a named field of the record") survives; Q12's stated ground must be
  restated, and the Japanese-vs-Chinese contrast softened.
- **Falsified:** "That is a search record a reader can re-run" — see above; the capture contradicts the
  re-runnability the entry builds its `verify-sweeps` argument on.
- **Drift:** `Embase和WebofScience` vs capture `Embase 和 Web of Science 数据库` (@11299); `主题词（MeSH/Emtree）
  和关键词` vs `题 词 （MeSH/Emtree） 和 关 键 词` (@11505). Prose-legal, not byte-exact if quoted.
- **Omission:** S117's own abstract carries the call for a reporting standard (@1384), which the entry attributes
  only to S116's module/absence. Recording it strengthens the entry's inference without changing it.

## Machine lines

```
QUOTE	S117	https://www.slarc.org.cn/dwyx/CN/article/downloadArticleFile.do?attachType=PDF&id=5237	中国知网、万方、中国生物医学文献数据库、	corpus/knowledge/chinese-search-record-r39.md
QUOTE	S117	https://www.slarc.org.cn/dwyx/CN/article/downloadArticleFile.do?attachType=PDF&id=5237	PubMed、Embase 和 Web of Science 数据库，检索时间	corpus/knowledge/chinese-search-record-r39.md
QUOTE	S117	https://www.slarc.org.cn/dwyx/CN/article/downloadArticleFile.do?attachType=PDF&id=5237	从各数据库建立至 2024 年 4 月 1 日	corpus/knowledge/chinese-search-record-r39.md
QUOTE	S117	https://www.slarc.org.cn/dwyx/CN/article/downloadArticleFile.do?attachType=PDF&id=5237	（MeSH/Emtree） 和 关 键 词	corpus/knowledge/chinese-search-record-r39.md
QUOTE	S117	https://www.slarc.org.cn/dwyx/CN/article/downloadArticleFile.do?attachType=PDF&id=5237	“动物实验”“鼠”“兔”“狗”“犬”“蛙”“蟾蜍”“猴”	corpus/knowledge/chinese-search-record-r39.md
QUOTE	S117	https://www.slarc.org.cn/dwyx/CN/article/downloadArticleFile.do?attachType=PDF&id=5237	“animal model”“mice”“rat”“rabbit”“dog”“frog”	corpus/knowledge/chinese-search-record-r39.md
QUOTE	S117	https://www.slarc.org.cn/dwyx/CN/article/downloadArticleFile.do?attachType=PDF&id=5237	“systematic review”“meta-analysis” 等	corpus/knowledge/chinese-search-record-r39.md
QUOTE	S117	https://www.slarc.org.cn/dwyx/CN/article/downloadArticleFile.do?attachType=PDF&id=5237	共得到 42 篇使用 GRADE 方法的动物实验 SRs/MAs	corpus/knowledge/chinese-search-record-r39.md
QUOTE	S117	https://www.slarc.org.cn/dwyx/CN/article/downloadArticleFile.do?attachType=PDF&id=5237	郑卿勇、许建国和李艺羿进行文献检索与数据提取	corpus/knowledge/chinese-search-record-r39.md
QUOTE	S117	https://www.slarc.org.cn/dwyx/CN/article/downloadArticleFile.do?attachType=PDF&id=5237	制定符合动物实验研究特点的 SRs/MAs 报告规范	corpus/knowledge/chinese-search-record-r39.md
```

## Tooling / scope

- No installs or upgrades (pacman transactions paused host-wide; nothing needed). `pdftotext` 26.08.0 from
  /usr/bin used read-only.
- Scratch `/dev/shm/chousa-r51-R51GroundSlarcBA/` (one pdftotext dump) deleted; no lane file written except this
  report; no campaign tool in /home/vgpnk/Projects/shokuknow executed; no counter run.

VERDICT — Re-grounded staged S117 against `c7266931a1731db3ff6ae77d` (50952 chars, UTF-8; PDF cross-checked):
the four record elements (six databases, 建立→2024-04-01, MeSH/Emtree+关键词, both term lists) are carried, but
"every database", "a Chinese review", "a record a reader can re-run" and "S117 does not name the searcher" are
not — the last two falsified by @12278/@1384 and @25850.
