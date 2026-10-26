# R51W2ReopenRowS111 — non-author re-open of Registry row `S111`

seat: `R51W2ReopenRowS111` (leaf; no subagent dispatch). Lane `/home/vgpnk/Projects/shokunin/chousa-shokunin` at tip `4436e279b91d8d68fd439c9095695035fbeeab74`. No network, no installs, no scratch dir created, no lane write except this report.

## 1. Row & capture identity (observed)

```
$ grep -n '^| S111 ' /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md
121:| S111 | 系统评价/Meta分析中文献检索报告清单（PRISMA-S）解读 — 中国生物医学文献服务系统 (SinoMed) 记录 ui=2026335073 — https://www.sinomed.ac.cn/article.do?ui=2026335073 | docs | B | the bibliographic fields and abstract that a national biomedical index serves for the Chinese PRISMA-S interpretation, as this record page shows them; not the interpretation's item text | 来源出版物 and 关键词 fields and the abstract; capture .txt read as UTF-8, 1675 characters; char 695, char 934, char 1138, char 1078, char 1366 | the record shows 中国循证医学杂志 volume 26 issue 4, five keywords and an abstract calling PRISMA-S a 16-item specialised standard, truncated before the item text; the page serves no full text | mined | 2026-10-25 | 180d | corpus/knowledge/chinese-search-record-r39.md |
```

```
$ python3 -c "import hashlib,pathlib;u='https://www.sinomed.ac.cn/article.do?ui=2026335073';k=hashlib.sha256(u.encode()).hexdigest()[:24];q=pathlib.Path('/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache');t,r=q/f'{k}.txt',q/f'{k}.raw';print(k,t.stat().st_size,len(t.read_text('utf-8')),hashlib.sha256(t.read_bytes()).hexdigest()[:16],r.stat().st_size,len(r.read_text('utf-8')),hashlib.sha256(r.read_bytes()).hexdigest()[:16])"
42bac8830527d6f1bb125c49 2969 1675 4d3bff5067b4cf8e 20142 17523 0d1c08a6ca7ee09a
```

## 2. Located quotes (`.txt` read as UTF-8; each `count=1`, ≤25 words, ≤160 chars)

```
$ python3 -c "import pathlib;t=pathlib.Path('/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/42bac8830527d6f1bb125c49.txt').read_text('utf-8');[print(f'cnt={t.count(q)} find={t.find(q)} w={len(q.split())} c={len(q)} | {q}') for q in ['系统评价/Meta分析中文献检索报告清单(PRISMA-S)解读 - 中国生物医学文献服务系统','来源出版物： 中国循证医学杂志 卷：26 期：4','中国循证医学杂志 卷：26 期：4','包含16个条目的专项规范','作为“报告规范”的内在局限,并针对中文','查看主题词相同的文献','质量控制','请登录后再使用此功能','©2016 中国医学科学院 北京协和医学院医学信息研究所/图书馆 版权所有 京ICP备10218182']]"
cnt=1 find=17 w=3 c=47 | 系统评价/Meta分析中文献检索报告清单(PRISMA-S)解读 - 中国生物医学文献服务系统
cnt=1 find=695 w=4 c=24 | 来源出版物： 中国循证医学杂志 卷：26 期：4
cnt=1 find=702 w=3 c=17 | 中国循证医学杂志 卷：26 期：4
cnt=1 find=934 w=1 c=12 | 包含16个条目的专项规范
cnt=1 find=1010 w=1 c=19 | 作为“报告规范”的内在局限,并针对中文
cnt=1 find=1078 w=1 c=10 | 查看主题词相同的文献
cnt=1 find=1138 w=1 c=4 | 质量控制
cnt=1 find=1366 w=1 c=10 | 请登录后再使用此功能
cnt=1 find=1567 w=5 c=51 | ©2016 中国医学科学院 北京协和医学院医学信息研究所/图书馆 版权所有 京ICP备10218182
```

## 3. Spans & used-by verification

```
$ awk -F'\t' '$1=="S111"' /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round51/spans.tsv
S111	https://www.sinomed.ac.cn/article.do?ui=2026335073	4d3bff5067b4cf8e81980618696fdd28c4457f6e64d361b1164b60625c937671	615	spans/S111-1.txt	来源出版物： 中国循证医学杂志 卷：26 期：4	corpus/knowledge/chinese-search-record-r39.md
S111	https://www.sinomed.ac.cn/article.do?ui=2026335073	4d3bff5067b4cf8e81980618696fdd28c4457f6e64d361b1164b60625c937671	622	spans/S111-2.txt	中国循证医学杂志 卷：26 期：4	corpus/knowledge/chinese-search-record-r39.md
S111	https://www.sinomed.ac.cn/article.do?ui=2026335073	4d3bff5067b4cf8e81980618696fdd28c4457f6e64d361b1164b60625c937671	854	spans/S111-3.txt	包含16个条目的专项规范	corpus/knowledge/chinese-search-record-r39.md
S111	https://www.sinomed.ac.cn/article.do?ui=2026335073	4d3bff5067b4cf8e81980618696fdd28c4457f6e64d361b1164b60625c937671	998	spans/S111-4.txt	查看主题词相同的文献	corpus/knowledge/chinese-search-record-r39.md
S111	https://www.sinomed.ac.cn/article.do?ui=2026335073	4d3bff5067b4cf8e81980618696fdd28c4457f6e64d361b1164b60625c937671	1058	spans/S111-5.txt	质量控制	corpus/knowledge/chinese-search-record-r39.md
S111	https://www.sinomed.ac.cn/article.do?ui=2026335073	4d3bff5067b4cf8e81980618696fdd28c4457f6e64d361b1164b60625c937671	1286	spans/S111-6.txt	请登录后再使用此功能	corpus/knowledge/chinese-search-record-r39.md
$ grep -ln '^source: S111 ' /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/*.md
/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/chinese-search-record-r39.md
```

Each span file `S111-1.txt`..`S111-6.txt` has `offset + span.find(quote) == txt.find(quote)` (`615+80=695`, `622+80=702`, `854+80=934`, `998+80=1078`, `1058+80=1138`, `1286+80=1366`).

## 4. Cell-by-cell audit

| Cell | Verdict | Evidence & residual notes |
|---|---|---|
| `id` | **holds** | `S111` (new since base max `S106`; maps staged `S119 -> S111`). |
| `source` | **holds** (minor punctuation gloss) | URL `https://www.sinomed.ac.cn/article.do?ui=2026335073` matches `sha256(url)[:24] = 42bac8830527d6f1bb125c49`. Title and host match `系统评价/Meta分析中文献检索报告清单(PRISMA-S)解读 - 中国生物医学文献服务系统` (`.txt` char 17); record id matches `<input type="hidden" id="ui" value="2026335073"/>` (`.raw:401`, char 13895) and domain `sinomed.ac.cn` (`.txt` char 1497). Note: the cell uses full-width `（PRISMA-S）` whereas the capture uses ASCII `(PRISMA-S)` (`txt.count('（PRISMA-S）') == 0`). |
| `kind` | **holds** | `docs` (valid `sources-census.sh` enum for a web index record page). |
| `tier` | **holds** | `B`. Properly argued by `scope`: this is a secondary bibliographic index record, not the primary article's own text, and `scope` explicitly bounds it to what the index record page shows ("not the interpretation's item text"). |
| `scope` | **holds** | Bounded to "the bibliographic fields and abstract that a national biomedical index serves for the Chinese PRISMA-S interpretation, as this record page shows them; not the interpretation's item text". Operator is `©2016 中国医学科学院 北京协和医学院医学信息研究所/图书馆 版权所有 京ICP备10218182` (`.txt` char 1567; "national" is an English gloss as `国家` is 0 in `.txt`/`.raw`). |
| `anchor` | **holds** (residual cross-file drift in entry `source:` line) | Names `来源出版物 and 关键词 fields and the abstract; capture .txt read as UTF-8, 1675 characters; char 695, char 934, char 1138, char 1078, char 1366`. Form and length (1675) are exact. All 5 `char N` values equal `txt.find(quote)` for S111 rows in `spans.tsv` (695=S111-1, 934=S111-3, 1138=S111-5, 1078=S111-4, 1366=S111-6). **Residual note**: ` anchor` omits `主题词` as a field label because `<tr>…主题词：…</tr>` is inside HTML comment `<!-- … -->` (`.raw:264-299`, chars 8929–9610) and only the widget `查看主题词相同的文献` (char 1078) and checkbox `质量控制` (char 1138) render in `.txt`. However, `corpus/knowledge/chinese-search-record-r39.md:5` still reads `the 来源出版物 / 关键词 / 主题词 fields` on its `source: S111` header line (and `corpus/README.md:1090` still says "that China has no standard for one yet" + "full text order-only"). |
| `teaches` | **holds** | Every clause is in `.txt`: (1) "shows 中国循证医学杂志 volume 26 issue 4" → `来源出版物： 中国循证医学杂志 卷：26 期：4` (char 695); (2) "five keywords" → `关键词：` followed by `PRISMA-S`, `文献检索`, `系统评价`, `报告规范`, `PRISMA 2020` (`.txt:231-240`, chars 737–791); (3) "an abstract calling PRISMA-S a 16-item specialised standard" → `包含16个条目的专项规范` (char 934); (4) "truncated before the item text" → abstract ends mid-sentence at `作为“报告规范”的内在局限,并针对中文` (char 1010, `.raw:258`); (5) "the page serves no full text" → `全文` count is 0 in `.txt`/`.raw`, and only the login prompt `请登录后再使用此功能` (char 1366) and shop-cart form (`.raw:410`) appear. |
| `status` | **holds** | `mined`. |
| `opened` | **holds** | `2026-10-25` (valid ISO date, matches `OPENED` in `c2-count.py`). |
| `recheck` | **holds** | `180d` (matches `^[0-9]+d$` in `sources-census.sh`). |
| `used-by` | **holds** | `corpus/knowledge/chinese-search-record-r39.md`, the exact single entry returned by `grep -ln '^source: S111 ' corpus/knowledge/*.md`. |

## 5. Survival under a non-author re-open

Row `S111` in `corpus/SOURCES.md` **survives** a non-author re-open: all 11 cells hold against `.qcache/42bac8830527d6f1bb125c49.txt` (1,675 chars, sha256 `4d3bff50…`), `c2-count.py` passes (`ANCHOR_BOUND=6/6`, `CAPTURE_BOUND=61/61`, `C2=PASS`), and `sources-census.sh validate` passes (`ok`). The staged overclaims (`学科分类号` field, "paid ordering service") were stripped from `S111` before landing. Two minor cross-file prose drifts outside `SOURCES.md` are noted for L1 awareness: `chinese-search-record-r39.md:5` still lists `主题词` as a field in its `source: S111` anchor description (whereas `SOURCES.md:121` dropped it because `主题词：` is commented out in `.raw:276`), and `corpus/README.md:1090` retains the staged summary phrase "that China has no standard for one yet" / "full text order-only" that the entry itself narrowed.

VERDICT: attacked `corpus/SOURCES.md` row `S111` against `.qcache/42bac8830527d6f1bb125c49.{txt,raw}` — 11/11 cells hold (all 5 `char N` offsets 695, 934, 1138, 1078, 1366 match `text.find(quote)` in `spans.tsv`, tier B is scoped to the bibliographic index record, every `teaches` clause is in the 1,675-char `.txt`, `used-by` matches the sole citing entry) and the row survives a non-author re-open, with only minor cross-file prose drift in `chinese-search-record-r39.md:5` (`主题词` field label) and `corpus/README.md:1090`.
