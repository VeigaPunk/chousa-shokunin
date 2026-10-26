# R51W2ExecNegZh — negative claims and sweeps of `chinese-search-record-r39.md`

Seat: R51W2ExecNegZh (falsify). Target: `corpus/knowledge/chinese-search-record-r39.md` at lane tip `72566c8` (entry landed `4436e27`). All runs from `/home/vgpnk/Projects/shokunin/chousa-shokunin`; captures read-only from the qcache; no network; no install performed. Forms: S109 `.txt` `fd468a36d78ff156b6200946.txt`, S110 `.txt` `c7266931a1731db3ff6ae77d.txt`, S111 `.txt` `42bac8830527d6f1bb125c49.txt`, each read as UTF-8.

## 1. The `recheck:` command (line 7), run verbatim

```console
$ QCACHE=/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache; python3 -c "import sys;[print(a,len(t:=open(a,encoding='utf-8').read()),[t.count(w) for w in ('布尔','灰色文献','检索者','检索式','学科分类号','国家标准','全文')],[t.find(q) for q in ('表 1 研究方案主体报告框架内容','尚无专门针对动物实验 SR 的报告规范','至少提供一个主要数据库的完整检索策略','从各数据库建立至 2024 年 4 月 1 日','包含16个条目的专项规范')]) for a in sys.argv[1:]]" "$QCACHE"/fd468a36d78ff156b6200946.txt "$QCACHE"/c7266931a1731db3ff6ae77d.txt "$QCACHE"/42bac8830527d6f1bb125c49.txt
…/fd468a36d78ff156b6200946.txt 52208 [1, 3, 0, 0, 0, 0, 4] [14179, 17709, 22932, -1, -1]
…/c7266931a1731db3ff6ae77d.txt 50952 [0, 0, 0, 0, 0, 0, 0] [-1, -1, -1, 11404, -1]
…/42bac8830527d6f1bb125c49.txt 1675  [0, 0, 0, 0, 0, 0, 0] [-1, -1, -1, -1, 934]
```

**Reproduces, digit for digit**, against the entry's stated text lengths (52,208 / 50,952 / 1,675, line 6), its claim vector (布尔 1/0/0, 灰色文献 3/0/0, 检索者 0/0/0, 检索式 0/0/0, 学科分类号 0/0/0, 国家标准 0/0/0, 全文 4/0/0) and every listed offset (14179, 17709, 22932, 11404, 934). The command's second clause, `then re-download the two PDFs and re-open the SinoMed record`, is **not runnable as written** under this wave's boundary: it needs network egress and L0 `8d77e6c1` is open. That is a boundary, not an entry defect; the sweep half is self-sufficient and offline.

## 2. Every negative claim in the entry, re-run

| entry line | claim | command | observed | verdict |
|---|---|---|---|---|
| 19 | 检索者 / 检索式 / 学科分类号 / 国家标准 = 0 in all three | `recheck` above | 0/0/0 each | **reproduces** |
| 19 | 灰色文献 3 / 0 / 0; 布尔 1 / 0 / 0 | `recheck` above | 3/0/0; 1/0/0 | **reproduces** |
| 19 | 全文 4 / 0 / 0 | `recheck` above | 4/0/0 | **reproduces** |
| 19 | "the only 全文 occurrences are in **the two PDFs** (S109, S110, S111)" | same vector | S109 4, **S110 0**, S111 0; occurrences at char 20856, 22789, 25488, 30115 — all in S109 | **differs** (see 4a) |
| 19, 25 | "in S110's form the word-boundary counts are AND 0 and OR 0" | `python3 -c "import re;t=open('…/c7266931a1731db3ff6ae77d.txt',encoding='utf-8').read();print(len(re.findall(r'\bAND\b',t)),len(re.findall(r'\bOR\b',t)),t.count('AND'),t.count('OR'))"` | `0 0 5 17` | **reproduces**; the 5/17 plain substrings are all inside names (`ANDREWS` 28043, `SANDERCOCK` 28246, `ORCID` 2492…) — no operator |
| 25 | "carries no boolean string (布尔 0, AND 0, OR 0, 检索式 0)" | widened: `Boolean` 0, `boolean` 0, `逻辑运算符` 0, `检索表达式` 0, `检索语句` 0, `检索串` 0, `search string` 0 in S110 | 0 across the widen set; `检索策略` 2 (the sentence the entry describes, keyword+MeSH combination) | **reproduces** |
| 14 | "the module table is 表1 … the only 表3 token belongs to a cited example's own table (char 33964)" | `t.count('表3'), t.count('表 3'), t.find('表 3')` on S109 | `0 1 33964`, context `（原文表 3）` | **reproduces** (staged `表3` unspaced: 0 occurrences) |
| 13 | title "set with inter-character spaces in this text form" | `s109.find('动物实验系统评价与Meta分析报告的规范撰写建议')` = -1; `s109.find('动 物 实 验 系 统 评 价')` = 1176 | spaced form at 1176 | **reproduces** |
| 16 | "§2.1.1 … does not speak about a national standard" | 国家标准 0; context at 17709 reads `由于目前尚无专门针对动物实验 SR 的报告规范，研究者可参考 PRISMA 框架` | holds | **reproduces** |
| 18 | "The abstract ends truncated at `在逐条阐释其内…`" | `s111.find('在逐条阐释其内')` = 980; next chars `涵与要求的基础上,进一步探`; last abstract chars at 1024 = `并针对中文` | 980 is mid-abstract; the abstract runs on to char 1024 | **differs** (see 4b) |
| 18 | "shows no 学科分类号 field and no full-text token" | `t.find('学科分类号')=-1, t.find('全文')=-1` on S111 | -1 / -1 | **reproduces** |
| 33 | "whether the journal enforces the row is not stated in its text" | S109: 稿约 0, 投稿须知 0; `要求` 2 at 28142 and 30712, both about the PRISMA flow diagram (`强烈建议（通常要求）使用 PRISMA 流程图`) | no enforcement sentence | **reproduces** |
| 36 | "this copy states none and no supplement is in the capture set" | S110: 补充材料 0, 附件 0, 附录 0, 在线补充 0, `Supplementary` 0, `Appendix` 0; `supplement` 2 = `supplementation` inside reference titles (34872, 45101); neither S110's DOI `10.12300/j.issn.1674-5817.2024.109` nor its title string resolves to any second capture (`grep -l` over 2,549 `.txt`) | one capture only, no supplement | **reproduces** |
| 9 | the staged file `chinese-search-log-r37-amendment-2026-10-23.md` is "(a file the lane does not hold)" | `ls corpus/knowledge/` — the lane holds 5 files, that one absent; the staged package holds it (`merge/chousa/knowledge/corpus/knowledge/`) | absent from lane, present staged | **reproduces** |

## 3. Widening the two "neither X names the searcher" claims

Command (all three forms at once, counts only):

```console
$ python3 - <<'PY'
Q="/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/"
F={"S109":"fd468a36d78ff156b6200946.txt","S110":"c7266931a1731db3ff6ae77d.txt","S111":"42bac8830527d6f1bb125c49.txt"}
T={k:open(Q+v,encoding='utf-8').read() for k,v in F.items()}
for w in ['检索者','检索员','检索人员','检索馆员','信息专员','图书馆员','情报人员','检索执行','检索由','检索工作','检索过程','检索人','执行检索','完成检索','searcher','librarian','information specialist','conducted the search','CRediT','author contribution','Acknowledg','致谢','作者贡献','我们检索','笔者','谁检索','无需','不要求','不必','拒绝','不做要求']:
    print(w, *[T[k].count(w) for k in ('S109','S110','S111')])
PY
检索者 0 0 0     检索员 0 0 0     检索人员 0 0 0    检索馆员 0 0 0   信息专员 0 0 0
图书馆员 0 0 0   情报人员 0 0 0   检索执行 0 0 0    检索由 0 0 0     检索工作 0 0 0
检索过程 0 0 0   检索人 0 0 0     执行检索 0 0 0    完成检索 0 0 0   searcher 1 1 0
librarian 0 0 0  information specialist 0 0 0     conducted the search 0 0 0
CRediT 0 0 0     author contribution 0 0 0        Acknowledgements 0 0 0
致谢 0 0 0       作者贡献 1 1 0   我们检索 0 0 0  笔者 0 0 0  谁检索 0 0 0
无需 0 0 0       不要求 0 0 0     不必 0 0 0      拒绝 0 0 0  不做要求 0 0 0
```

Word-boundary re-run of the two `searcher` hits: `re.findall(r'\bsearcher\w*',t)` = 0 in S109/S110/S111; the hits are inside `researcher` (1 each in S109, S110). Chinese side: **14 distinct person-terms, all 0/0/0**; English side after the boundary filter: 0. `作者贡献` occurs once in S109 and once in S110 — I opened both: they head the journal's author-contribution list (作者贡献：郑卿勇…), not a search-role statement. `无需/不要求/不必/拒绝/不做要求` = 0/0/0, so the *refusal half* of line 27 ("none of them states that the field is unwanted") is also clean.

- **Line 27** — "The searcher's identity is unrecorded here rather than refused … the search string 检索者 occurs 0 times in each of the three forms": **narrowed wording still holds.** No synonym in either language names a person who ran a search, no contributor/acknowledgement statement assigns the search, and no copy says the field is not wanted.
- **Line 37** — "Whether any Chinese form names the searcher as a field: none of these three copies is a form, and 检索者 is absent from all three": **the 检索者 half holds under widening**, and the module table is indeed the only field-shaped artefact. One calibration caveat: S109 does carry a 9-row tabular reporting framework (表1, `序号 / 模块 / 具体报告内容`, char 14179) which is form-like in shape; "none of these three copies is a form" is exact only in the sense of a submitted instrument. Its row 3 still names no searcher, so the substance is untouched — this is a wording note, not a break.

The same widening applied to the third count-based negative, line 34 (see 4c), surfaced a real counterexample: `GB/T 35892—2018` at char 50121 and `实验动物管理条例` at char 50074, both in S110.

## 4. What breaks

**4a. Line 19, the 全文 gloss.** Counts are 4 / 0 / 0; the sentence says the occurrences are "in **the two PDFs** (S109, S110, S111)". S110 is a PDF and has zero. Replacement sentence, intended for `corpus/knowledge/chinese-search-record-r39.md` line 19 (the trailing clause only):

```text
So no copy names the person who ran a search, S110's record states no boolean string, S111's record page shows no 学科分类号 field and no full-text token, and the only 全文 occurrences are the four in S109 (char 20856, 22789, 25488, 30115), none in S110 and none in S111 (S109, S110, S111).
```

**4b. Line 18, the truncation point.** `在逐条阐释其内` is at char 980 and is followed by `涵与要求的基础上,进一步探…`; the abstract's last characters are `并针对中文` at char 1024. The abstract is truncated, but not at the stated place. Replacement, intended for line 18:

```text
The abstract ends truncated mid-sentence at `并针对中文` (char 1024; `在逐条阐释其内` at char 980 is mid-abstract, not the cut); the page offers `查看主题词相同的文献` and the login prompt `请登录后再使用此功能`, and serves no full text here (S111).
```

The same phrasing is carried by the registry row S111 in `corpus/SOURCES.md` ("truncated before the item text") — that row's wording survives, since the abstract *is* truncated before any item text; only the entry's specific cut point is wrong.

**4c. Line 34, "these copies do not reach a standards body".** The token count reproduces (国家标准 0/0/0, widened 国标/行业标准/团体标准/标准化委员会/卫生健康委员会 0/0/0), but the gloss is falsified by S110's own journal boilerplate: `本刊是我国实验动物科学与比较医学领域的一本专业学术期刊，严格遵守国家实验动物相关法律、法规和标准`, citing `《实验动物管理条例》` (char 50074) and `《实验动物 福利伦理审查指南》（GB/T 35892—2018）` (char 50121). A GB/T number is a national standard, so the copy does reach one — just not for search reporting. Replacement, intended for line 34:

```text
- Whether any Chinese body has issued a national standard for systematic-review search reporting: the search string 国家标准 occurs 0 times in all three forms, and the only standard any of them names is S110's own ethics boilerplate (《实验动物管理条例》 char 50074, GB/T 35892—2018 char 50121), which is animal-welfare regulation, not search reporting; the absence in S109 is about animal-experiment SR reporting.
```

**4d. Line 32, "no other copy of it is in the capture set" — wording, not substance.** Read "it" as the item text: true. Read "it" as the article: there are **two** captures of the same Chinese PRISMA-S interpretation in the qcache — S111's SinoMed page (`42bac883…`, 1,675 chars, bound as S111) and an unbound MedSci.cn announcement page (`453d492becd9a2f4632cb8dd.txt`, 8,804 chars, `# 系统评价/Meta分析中文献检索报告清单（PRISMA-S）解读 -指南&解读指南-MedSci.cn`). I audited all 8 qcache forms containing `PRISMA-S` for item text (`条目` count, title match): only those two are the Chinese interpretation, and neither carries any item text — both stop at the same abstract clause (`包含16个条目的专项规范` at 934 / 2389 and 3499). Suggested narrowing, intended for line 32:

```text
- … the item text is not served by this record page, and neither capture of the article in the cache (42bac8830527d6f1bb125c49, SinoMed; 453d492becd9a2f4632cb8dd, MedSci.cn, 8,804 characters) carries any item text.
```

## 5. What holds (attacked, not broken)

- The `recheck:` command is executable from the lane root with `env -u ASSIMILATE_CITES` never needed (it reads no environment but `QCACHE`) and prints every number the entry states, including text lengths and offsets — the strongest piece of operability in the entry.
- Three module items in 表1 row 3 (`含动物实验特殊数据库` / `检索词及逻辑关系（结合 MeSH/Emtree 主题词与自由词）` / `灰色文献的检索与记录` at 15310), verified by dumping chars 15100–16100: row 3 carries exactly (1)(2)(3) and row 4 begins 纳排标准. The "only" is exact.
- The 表3→表1 correction (line 14) is right and its supporting offset (33964) is right.
- S110's six databases, the 2024-04-01 bound (char 11404), the Chinese/English term families and the absence of any boolean operator all reproduce; the entry's "six databases" count is exact (`中国知网、万方、中国生物医学文献数据库` + PubMed, Embase, Web of Science).
- S110 grey literature = 0, supplement = 0, per-database strategy = 0 (检索式/检索表达式/检索语句/检索串/search string all 0).
- S111's fields, its five keywords, its `*`-marked major subject headings and the login/sales furniture all reproduce; there is no 学科分类号 and no 全文 token.
- The searcher claims (lines 27, 37) survive a 14-term Chinese and 8-term English widening.
- The adopted-file claim (line 9) is exact: the lane does not hold `chinese-search-log-r37-amendment-2026-10-23.md`.

Two defects (4a, 4b) touch phrasing only; 4c removes a false gloss; 4d narrows an over-broad "no other copy". None of them moves a predicate, target, counter or control: all sit in the entry's Observation/Unknown prose, and the frozen counts they lean on reproduce unchanged.

## 6. Notes for the integrator

- Fix order: 4b and 4a are one-line edits in the entry; 4c and 4d are Unknown-bullet rewrites. 4c also suggests a one-clause note in the registry row S111 only if the row is meant to state the cut point — as written that row is fine.
- The MedSci capture (4d) is unbound to any registry row; I did not propose binding it, since it serves no item text and would add a second row for one article (the lesson already warns of that for S133/S111).
- Scratch `/dev/shm/chousa-r51-R51W2ExecNegZh/` deleted after the last run; no lane file other than this report was written; no tool installed.

VERDICT: attacked every negative claim and this entry's single printable sweep (11 claims re-run, 3 widened) — the `recheck:` command, all seven count vectors, the text lengths, the 表1/表3 correction, the no-boolean, no-supplement, no-学科分类号, no-全文, no-enforcement and no-searcher results all reproduce exactly, while four phrasings break or over-reach: the 全文 gloss (S110 has 0, not "the two PDFs"), the abstract's cut point (char 1024 `并针对中文`, not `在逐条阐释其内` at 980), "these copies do not reach a standards body" (S110 cites GB/T 35892—2018 at 50121), and "no other copy of it is in the capture set" (a second, unbound MedSci capture exists, though neither serves item text).
