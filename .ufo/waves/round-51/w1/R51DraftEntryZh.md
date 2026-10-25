# R51DraftEntryZh — lane draft of `corpus/knowledge/chinese-search-record-r39.md`

seat: R51DraftEntryZh (leaf; no subagent dispatch). Lane `/home/vgpnk/Projects/shokunin/chousa-shokunin` at tip `cfe6c9fb9b56fa80a3005c1a3aaa522b29966306`; base `9ec1751a24231e899ceea4688e21c8edf6046d35`. Staged package `/home/vgpnk/Projects/shokuknow/merge/chousa` (read-only, never written). Captures `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache` (read-only). Scratch `/dev/shm/chousa-r51-R51DraftEntryZh/` (deleted after this report). No installs, no network, no lane write except this report.

## What I built

The lane version of the staged Chinese entry, re-bound by document to three lane ids and grounded on the three on-disk captures. It keeps the staged observations (three module items; one worked record; a Chinese PRISMA-S interpretation indexed without full text) and narrows the four overclaims below. No predicate, target, counter or control touched; the frozen C1/C2/C3 files were not run except that `c2-count.py` was **not** run at all (lane bound) and `inference-ground.py` / `quote-substance-check.py` were run read-only on a scratch manifest.

## Provenance map (staged -> lane)

| staged | lane | URL | capture key | form | chars |
|---|---|---|---|---|---|
| S116 | S109 | https://www.slarc.org.cn/dwyx/EN/article/downloadArticleFile.do?attachType=PDF&id=5290 | `fd468a36d78ff156b6200946` | `.txt`, UTF-8 | 52208 |
| S117 | S110 | https://www.slarc.org.cn/dwyx/CN/article/downloadArticleFile.do?attachType=PDF&id=5237 | `c7266931a1731db3ff6ae77d` | `.txt`, UTF-8 | 50952 |
| S119 | S111 | https://www.sinomed.ac.cn/article.do?ui=2026335073 | `42bac8830527d6f1bb125c49` | `.txt`, UTF-8 | 1675 |

Dropped, with the check that justifies it:
- staged continuation of `chinese-search-log-r37-amendment-2026-10-23.md` — the lane holds no file under that name (`ls corpus/knowledge | grep chinese` lists none).
- the staged body-only `S097` hand-search reference — lane row S097 is the J-STAGE For Publishers page (`corpus/knowledge/aggregator-vs-source-r36.md:5`), and `grep -rn "検索者\|手工检索\|ハンドサーチ\|hand-search" corpus/knowledge/` returned no file carrying the hand-search claim, so there was no lane file to re-point it at.

## Corrections to the staged text

1. `表3 报告模块表 module 3 文献检索策略` -> the module table is **表1** (`表 1 研究方案主体报告框架内容`, char 14179). The only `表 3` token in the capture (char 33964) is inside a cited example: `原文表 3` of van Rhijn-Brouwer.
2. the staged anchor named `学科分类号` for S119 — that field is absent from the SinoMed copy (`学科分类号` 0 occurrences, `分类号` 0); the copy shows `作者`, `作者地址`, `来源出版物`, `关键词`, `摘要`, `主题词`. Anchor corrected.
3. `China has no standard for one yet` -> field-scoped absence: S109 says `尚无专门针对动物实验 SR 的报告规范` (animal-experiment SR reporting), and S111 shows a Chinese PRISMA-S interpretation exists. Neither copy mentions `国家标准` (0 in all three).
4. `a search record a reader can re-run` -> partial re-run: S110 fixes databases, the 2024-04-01 bound and term families, and carries no boolean operator and no per-database strategy (`布尔` 0, word-boundary `AND` 0, `OR` 0, `检索式` 0 in its form).
5. campaign-internal `Q5b`, `Q12 stays open`, `wave 3` language -> plain statements of what the copies say and do not say; S110 called a published *empirical study* (its title is `GRADE 方法的实证研究`), not a review.

## Checks run

Quote location and uniqueness (form `.txt` read as UTF-8, `str.find`), all 24 quotes `count=1` and present in the draft:

```
S109 count=1 off=14179 表 1 研究方案主体报告框架内容
S109 count=1 off=15140 含动物实验特殊数据库
S109 count=1 off=15240 检索词及逻辑关系（结合 MeSH/Emtree 主题词与自由词）
S109 count=1 off=15310 灰色文献的检索与记录
S109 count=1 off=17709 尚无专门针对动物实验 SR 的报告规范
S109 count=1 off=22932 至少提供一个主要数据库的完整检索策略
S109 count=1 off=23097 AND，OR 等
S109 count=1 off=23180 参考文献追溯
S109 count=1 off=24606 手工查阅期刊
S109 count=1 off=23316 表 2 动物实验系统评价的数据库检索参考
S109 count=1 off=24298 预印本平台
S109 count=1 off=121 DOI:10.12300/j.issn.1674-5817.2025.017
S109 count=1 off=4113 1674-5817（2025）04-0496-12
S109 count=1 off=201 ·比较医学研究与报告规范·
S110 count=1 off=11110 文献特征分析
S110 count=1 off=11211 检索中国知网、万方、中国生物医学文献数据库、
S110 count=1 off=11404 从各数据库建立至 2024 年 4 月 1 日
S110 count=1 off=134 DOI:10.12300/j.issn.1674-5817.2024.109
S110 count=1 off=1633 1674-5817（2025）01-0101-11
S111 count=1 off=695 来源出版物： 中国循证医学杂志 卷：26 期：4
S111 count=1 off=934 包含16个条目的专项规范
S111 count=1 off=1138 质量控制
S111 count=1 off=1078 查看主题词相同的文献
S111 count=1 off=1366 请登录后再使用此功能
```

Lane bar, on a scratch span manifest built exactly as `build-spans.py` builds one (span = `form[off-80:off+len+80]`, 7 columns), then `tools/inference-ground.py`:

```
$ python3 tools/inference-ground.py --entry entry.md --spans spans.tsv --counts /dev/null \
    --registry corpus/SOURCES.md --root /home/vgpnk/Projects/shokunin/chousa-shokunin
GROUND entry=entry.md section=1 bullets=6 tokens=9 grounded=9
GROUND: PASS
rc=0
```

Substance floor on the same manifest:

```
$ python3 corpus/evidence/round51/quote-substance-check.py spans.tsv
IDS=3 QUOTES=24 FAILURES=0
rc=0
```

The `recheck:` line run verbatim from the lane root (this is the observed output the entry's counts rest on):

```
$ QCACHE=/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache; python3 -c "..." "$QCACHE"/fd468a36d78ff156b6200946.txt "$QCACHE"/c7266931a1731db3ff6ae77d.txt "$QCACHE"/42bac8830527d6f1bb125c49.txt
/home/.../fd468a36d78ff156b6200946.txt 52208 [1, 3, 0, 0, 0, 0, 4] [14179, 17709, 22932, -1, -1]
/home/.../c7266931a1731db3ff6ae77d.txt 50952 [0, 0, 0, 0, 0, 0, 0] [-1, -1, -1, 11404, -1]
/home/.../42bac8830527d6f1bb125c49.txt 1675 [0, 0, 0, 0, 0, 0, 0] [-1, -1, -1, -1, 934]
rc=0
```

(the list is `布尔, 灰色文献, 检索者, 检索式, 学科分类号, 国家标准, 全文`; the second list is the offsets of the five anchor quotes). A first form of the line used `QCACHE=... python3 ... "$QCACHE"/...` and failed (`FileNotFoundError: '/fd468a36d78ff156b6200946.txt'`) because the shell expands `$QCACHE` before the assignment applies; the landed line uses `;` and is runnable as one command.

Id discipline:

```
$ python3 -c "import re,pathlib;t=pathlib.Path('entry.md').read_text();print(sorted(set(re.findall(r'\bS\d{3,}\b',t))))"
['S109', 'S110', 'S111']
```

## Registry data L1 needs (not written by me)

Three new rows, all `opened 2026-10-25`, `status mined`, `recheck 365d`, `used-by corpus/knowledge/chinese-search-record-r39.md` (exactly that one entry, or the C2 counter's `used == citing` leg fails):

- **S109** — source cell: `动物实验系统评价与Meta分析报告的规范撰写建议 — 实验动物与比较医学 2025;45(4):496-507 — https://www.slarc.org.cn/dwyx/EN/article/downloadArticleFile.do?attachType=PDF&id=5290`; kind `paper`, tier A; scope: what this copy's 表1 row 3, §2.1.1, §2.4.1 and 表2 state about a search record, not a national standard; anchor: `表 1 研究方案主体报告框架内容 and row 3, §2.1.1, §2.4.1, 表 2; char 14179, char 15310, char 15240, char 17709, char 22932, char 24606, char 24298`.
- **S110** — source cell: `提高动物实验系统评价/Meta 分析的证据确定性：GRADE 方法的实证研究 — 实验动物与比较医学 2025;45(1):101-111 — https://www.slarc.org.cn/dwyx/CN/article/downloadArticleFile.do?attachType=PDF&id=5237`; kind `paper`, tier A; scope: what §3 文献特征分析 states as its own search record; anchor: `§3 文献特征分析, the 检索策略 paragraph; char 11110, char 11211, char 11404`.
- **S111** — source cell: `系统评价/Meta分析中文献检索报告清单(PRISMA-S)解读 — 中国循证医学杂志 26(4), SinoMed record — https://www.sinomed.ac.cn/article.do?ui=2026335073`; kind `docs`, tier B (a bibliographic index record: what its fields and abstract state, not the item text); anchor: `来源出版物 / 关键词 / 主题词 fields and the abstract; char 695, char 934, char 1138, char 1078, char 1366`.

Every `char N` above is a quote offset (see the table) — the C2 counter requires exactly that. `quotes.tsv` for `build-spans.py` can be derived from the 24 rows above with header `id<TAB>url<TAB>quote<TAB>entry`; all 24 quotes must also be placed in `corpus/lessons/round-51.md`, or the counter's `QUOTES_IN_LESSON` leg falls short.

## Entry text — intended lane path `corpus/knowledge/chinese-search-record-r39.md`

```markdown
# A Chinese animal-experiment reporting copy asks a search record for three module items and one full database strategy; a SinoMed record shows a Chinese PRISMA-S interpretation of 16 items without its full text

source: S109 — https://www.slarc.org.cn/dwyx/EN/article/downloadArticleFile.do?attachType=PDF&id=5290 — 表1 (研究方案主体报告框架内容) row 3, §2.1.1, §2.4.1 and 表2 — char 14179, char 15310, char 15240, char 17709, char 22932, char 24606, char 24298
source: S110 — https://www.slarc.org.cn/dwyx/CN/article/downloadArticleFile.do?attachType=PDF&id=5237 — §3 文献特征分析, the 检索策略 paragraph — char 11110, char 11211, char 11404
source: S111 — https://www.sinomed.ac.cn/article.do?ui=2026335073 — the 来源出版物 / 关键词 / 主题词 fields and the abstract — char 695, char 934, char 1138, char 1078, char 1366
verified-at: 2026-10-25 — the three captures opened from the read-only qcache; every offset below re-located in the `.txt` form read as UTF-8 (52,208 / 50,952 / 1,675 characters)
recheck: 365d — from any cwd: `QCACHE=/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache; python3 -c "import sys;[print(a,len(t:=open(a,encoding='utf-8').read()),[t.count(w) for w in ('布尔','灰色文献','检索者','检索式','学科分类号','国家标准','全文')],[t.find(q) for q in ('表 1 研究方案主体报告框架内容','尚无专门针对动物实验 SR 的报告规范','至少提供一个主要数据库的完整检索策略','从各数据库建立至 2024 年 4 月 1 日','包含16个条目的专项规范')]) for a in sys.argv[1:]]" "$QCACHE"/fd468a36d78ff156b6200946.txt "$QCACHE"/c7266931a1731db3ff6ae77d.txt "$QCACHE"/42bac8830527d6f1bb125c49.txt` — then re-download the two PDFs and re-open the SinoMed record, confirming the module row, the 2024-04-01 date bound and the journal / volume / issue are unchanged
ground: PROVINCE.md claim-vs-source verification — what a Chinese animal-experiment reporting-recommendation copy asks a search record to carry, what one published Chinese record in the same journal states, and what a SinoMed index record shows about a Chinese PRISMA-S interpretation; not a national standard, not the interpretation's item text and not a re-runnable strategy for S110
adopted: round 51 from the campaign package `merge/chousa/`, re-bound by document to S109, S110 and S111; the staged entry's continuation of `chinese-search-log-r37-amendment-2026-10-23.md` (a file the lane does not hold) and its body-only Japanese hand-search reference are dropped (the staged-to-lane id map is in `corpus/lessons/round-51.md` `## Gate`)

#### Observation

- **The first copy is a reporting-recommendation paper in one Chinese journal.** 实验动物与比较医学 2025, 45(4):496-507, `DOI:10.12300/j.issn.1674-5817.2025.017`, 文章编号 `1674-5817（2025）04-0496-12`, section label `·比较医学研究与报告规范·`; its title is 动物实验系统评价与Meta分析报告的规范撰写建议, set with inter-character spaces in this text form (S109).
- **The protocol table gives the search module three items.** 表1, `表 1 研究方案主体报告框架内容`, row 3 (文献检索策略) carries: the databases, `含动物实验特殊数据库`; the time range with `检索词及逻辑关系（结合 MeSH/Emtree 主题词与自由词）`; and `灰色文献的检索与记录` (S109). The staged reading called this 表3; in this copy the module table is 表1, and the only 表3 token belongs to a cited example's own table (char 33964).
- **The method section asks for one complete strategy and names supplementary steps.** §2.4.1 requires `至少提供一个主要数据库的完整检索策略`, shows controlled terms plus free words joined by boolean operators (`AND，OR 等`), and asks whether `参考文献追溯`, citation searching or `手工查阅期刊` were used, plus the reference manager and dedup method (S109). 表2, `表 2 动物实验系统评价的数据库检索参考`, lists 通用数据库 / 专业数据库 / 灰色文献 / `预印本平台` dimensions, with OpenGrey, ProQuest Dissertations & Theses, EThOS and CAB Abstracts under grey literature and bioRxiv, medRxiv under preprints (S109).
- **The same copy states the absence for its own field.** §2.1.1 says `尚无专门针对动物实验 SR 的报告规范` and advises using the PRISMA framework to disclose the conduct in detail. The sentence's subject is animal-experiment SR reporting in this copy; it does not speak about a national standard (S109).
- **One published Chinese empirical study in the same journal states its own search.** S110 (an empirical study of GRADE use in animal-experiment SRs/MAs), 实验动物与比较医学 2025, 45(1):101-111, `DOI:10.12300/j.issn.1674-5817.2024.109`, 文章编号 `1674-5817（2025）01-0101-11`, §3 `文献特征分析` records: `检索中国知网、万方、中国生物医学文献数据库、` PubMed、Embase 和 Web of Science; `从各数据库建立至 2024 年 4 月 1 日`; 检索策略 combining 主题词 (MeSH/Emtree) with 关键词; then a Chinese term list (动物实验, 鼠, 兔, 狗, 犬, 蛙, 蟾蜍, 猴, 猿, 猪, 猩猩, 鱼, 果蝇, 系统评价, Meta 分析) and an English one running from animal experimentation to systematic review, interleaved with the facing column by the two-column extraction (S110).
- **The SinoMed record carries bibliographic fields and a truncated abstract, not the item text.** S111 (中国生物医学文献服务系统) shows 作者, 作者地址, `来源出版物： 中国循证医学杂志 卷：26 期：4`, keywords PRISMA-S / 文献检索 / 系统评价 / 报告规范 / PRISMA 2020, subject headings *评价研究 / *研究报告 / Meta分析 / *清单 / `质量控制`, and an abstract that calls PRISMA-S a PRISMA 2020 extension giving `包含16个条目的专项规范`. The abstract ends truncated at 在逐条阐释其内…; the page offers `查看主题词相同的文献` and a login prompt `请登录后再使用此功能` with sales contacts, and serves no full text here (S111).
- **Negative sweeps over the three text forms.** Read as UTF-8, the search strings 检索者, 检索式, 学科分类号 and 国家标准 occur 0 times in all three forms; 灰色文献 3 / 0 / 0; 布尔 1 / 0 / 0; 全文 4 / 0 / 0; in S110's form the word-boundary counts are AND 0 and OR 0. Command in `recheck:`. So no copy names the person who ran a search, S110's record states no boolean string, S111's record page shows no 学科分类号 field and no full-text token, and the only 全文 occurrences are in the two PDFs (S109, S110, S111).

#### Inference

- **The module table is a floor, and the same copy raises the bar above it.** §2.4.1 asks for `至少提供一个主要数据库的完整检索策略`, while 表1's row asks only that the record carry the databases, the time range with terms and their logic, and grey literature (S109). A record can fill the three module items and still carry nothing a reader could run, so this copy asks for both a summary and one complete strategy, and only the method section carries the executable bar (S109).
- **Grey literature is the module item the worked record does not carry.** S109 makes `灰色文献的检索与记录` a module item and puts `预印本平台` among its retrieval dimensions; S110's record names six databases and a date bound and mentions 灰色文献 0 times (S109, S110). In these two copies the requirement and the published practice differ, so a reader cannot infer from S110's record that grey literature was searched.
- **What S110 supports is a partial re-run.** Its record fixes the databases, the bound `从各数据库建立至 2024 年 4 月 1 日`, and the term families, and carries no boolean string (布尔 0, AND 0, OR 0, 检索式 0 in that form) (S110). A reader can repeat the sources and the period and re-assemble the term list, but cannot replay a per-database strategy: the copy states none.
- **The absence in S109 is field-scoped, and the index record shows a general search-reporting interpretation exists.** S109 says `尚无专门针对动物实验 SR 的报告规范`; S111 indexes a Chinese PRISMA-S interpretation with `包含16个条目的专项规范` (S109, S111). The two are compatible — one is a field-specific reporting standard, the other a general search-reporting extension — and neither copy supports a statement that no Chinese standard for search reporting exists.
- **The searcher's identity is unrecorded here rather than refused.** The search string 检索者 occurs 0 times in each of the three forms, and S109's module row names the databases, `检索词及逻辑关系（结合 MeSH/Emtree 主题词与自由词）` and `灰色文献的检索与记录` only (S109, S110, S111). On this evidence the question of who ran a search is unanswered by these copies; none of them states that the field is unwanted.
- **The 16-item text stays unread at item level here.** S111's abstract gives the count and the purpose (`包含16个条目的专项规范`) but truncates, and the page serves no full text (S111). So the Chinese wording of the items, and any departure from PRISMA-S's own items, is not in this copy.

#### Unknown

- Whether the Chinese interpretation's 16 items match PRISMA-S's original items in wording or scope: the item text is not served by this record page, and no other copy of it is in the capture set.
- Whether 实验动物与比较医学 requires the module at submission or only recommends it: the copy is framed as 建议, and whether the journal enforces the row is not stated in its text.
- Whether any Chinese body has issued a national standard for systematic-review search reporting: the search string 国家标准 occurs 0 times in all three forms, and these copies do not reach a standards body; the absence in S109 is about animal-experiment SR reporting.
- Whether other Chinese journals or forms ask for the same three items: one journal's copy is opened here, and the grey-literature requirement was read in one module table.
- Whether S110's authors kept per-database strategies in a supplement: this copy states none and no supplement is in the capture set.
- Whether any Chinese form names the searcher as a field: none of these three copies is a form, and 检索者 is absent from all three.
```

## Out of scope / limits

- I wrote no lane file, registry row, lesson, `quotes.tsv`, `spans.tsv` or span file; L1 integrates. I did not run `c1-count.py`, `c2-count.py` or `c3-count.py`.
- The Chinese PRISMA-S item text was not opened: the SinoMed page serves no full text and no other copy is in the cache; the entry states that limit rather than inferring the items.
- S111 is a bibliographic index record on a mirror; every statement about it is scoped "as this copy states".
- The 24 quotes must also land in `corpus/lessons/round-51.md`; the entry alone does not satisfy the C2 `QUOTES_IN_LESSON` leg.

VERDICT: built and self-checked the lane Chinese entry on three read-only captures — 24/24 quotes unique at their offsets, inference-ground PASS (6 bullets, 9 tokens) on a simulated manifest, substance floor PASS, only S109/S110/S111 tokens; the staged 表3, `学科分类号`, `China has no standard`, re-runnable-strategy and Q12/wave-3 readings were narrowed or dropped.
