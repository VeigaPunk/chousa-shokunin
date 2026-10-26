# R51W2ReopenRowS110 — independent re-open of registry row `S110`

Seat: `R51W2ReopenRowS110` (leaf reviewer, `/skill:godspeed`). Date: 2026-10-25. Lane repo: `/home/vgpnk/Projects/shokunin/chousa-shokunin` at tip `4436e279b91d8d68fd439c9095695035fbeeab74` (base `9ec1751a24231e899ceea4688e21c8edf6046d35`, freeze `d603f6f00f78d64f123d3aed2dd9f8701547a4ba`).
Tooling: read `/home/vgpnk/.omp/agent/RULES.md`; pacman guard respected (0 installs/upgrades). Scratch: none created under `/dev/shm`. No network or live fetch (L0 `8d77e6c1` open).
Decode form (QUALITY 76): every `char N` below is `text.find(quote)` in the capture text form `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/c7266931a1731db3ff6ae77d.txt` **read as UTF-8** (50,952 characters, 69,789 bytes, sha256 `03342b7ded4f9d687a5319a739cf357e4fa37d96de20ce66cba6cc7f5adfe2dd`; `.raw` is a 1,140,215-byte 11-page PDF 1.4, sha256 `815bea41f8c249010fa11f1d374e5977db3bac5e50999ba190788bd4fc51fd07`).

## 1. Commands & observed outputs

```
$ grep -n '^| S110 ' /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md
120:| S110 | 提高动物实验系统评价/Meta分析的证据确定性：GRADE方法的实证研究（李腾飞 等）— 实验动物与比较医学 2025;45(1):101-111 — https://www.slarc.org.cn/dwyx/CN/article/downloadArticleFile.do?attachType=PDF&id=5237 | paper | A | what this empirical study states as its own search record, as a working example | section 3 文献特征分析, the 检索策略 paragraph; capture .txt read as UTF-8, 50952 characters; char 11110, char 11211, char 11404 | the record names the databases searched, the date bound from each database's inception to 2024-04-01 and the combination of controlled terms with keywords; it states no boolean string and does not mention grey literature | mined | 2026-10-25 | 365d | corpus/knowledge/chinese-search-record-r39.md |

$ awk -F'\t' '$1=="S110"' /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round51/spans.tsv
S110	https://www.slarc.org.cn/dwyx/CN/article/downloadArticleFile.do?attachType=PDF&id=5237	03342b7ded4f9d687a5319a739cf357e4fa37d96de20ce66cba6cc7f5adfe2dd	54	spans/S110-1.txt	DOI:10.12300/j.issn.1674-5817.2024.109	corpus/knowledge/chinese-search-record-r39.md
S110	https://www.slarc.org.cn/dwyx/CN/article/downloadArticleFile.do?attachType=PDF&id=5237	03342b7ded4f9d687a5319a739cf357e4fa37d96de20ce66cba6cc7f5adfe2dd	1553	spans/S110-2.txt	1674-5817（2025）01-0101-11	corpus/knowledge/chinese-search-record-r39.md
S110	https://www.slarc.org.cn/dwyx/CN/article/downloadArticleFile.do?attachType=PDF&id=5237	03342b7ded4f9d687a5319a739cf357e4fa37d96de20ce66cba6cc7f5adfe2dd	11030	spans/S110-3.txt	文献特征分析	corpus/knowledge/chinese-search-record-r39.md
S110	https://www.slarc.org.cn/dwyx/CN/article/downloadArticleFile.do?attachType=PDF&id=5237	03342b7ded4f9d687a5319a739cf357e4fa37d96de20ce66cba6cc7f5adfe2dd	11131	spans/S110-4.txt	检索中国知网、万方、中国生物医学文献数据库、	corpus/knowledge/chinese-search-record-r39.md
S110	https://www.slarc.org.cn/dwyx/CN/article/downloadArticleFile.do?attachType=PDF&id=5237	03342b7ded4f9d687a5319a739cf357e4fa37d96de20ce66cba6cc7f5adfe2dd	11133	spans/S110-5.txt	中国知网、万方、中国生物医学文献数据库	corpus/knowledge/chinese-search-record-r39.md
S110	https://www.slarc.org.cn/dwyx/CN/article/downloadArticleFile.do?attachType=PDF&id=5237	03342b7ded4f9d687a5319a739cf357e4fa37d96de20ce66cba6cc7f5adfe2dd	11133	spans/S110-6.txt	中国知网、万方、中国生物医学文献数据库、	corpus/knowledge/chinese-search-record-r39.md
S110	https://www.slarc.org.cn/dwyx/CN/article/downloadArticleFile.do?attachType=PDF&id=5237	03342b7ded4f9d687a5319a739cf357e4fa37d96de20ce66cba6cc7f5adfe2dd	11324	spans/S110-7.txt	从各数据库建立至 2024 年 4 月 1 日	corpus/knowledge/chinese-search-record-r39.md

$ grep -ln '^source: S110 ' /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/*.md
/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/chinese-search-record-r39.md

$ env -u ASSIMILATE_CITES python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round51/c2-count.py
ENTRIES=3/3
BOUND=6/7 (min 5) REFUSED=1
BOUND_IDS=S107,S108,S109,S110,S111,S112
REF_ID_UNBOUND=0
NEW_GROUND=3/3
QUOTE_ROWS=61 ON_BOUND=61/61
SPAN_IDS=6/6 (min 3 each)
QUOTES_IN_SPAN=61/61
QUOTES_IN_ENTRY=61/61
QUOTES_IN_LESSON=61/61
QUOTE_SHORT=61/61
SPAN_CONTEXT=61/61
CAPTURE_BOUND=61/61
SUBSTANCE=PASS
ANCHOR_BOUND=6/6
INFERENCE_GROUNDED=3/3
QUARANTINE_VERDICTS=6/6 (S104,S105,S111,S112,S114,S120)
QUARANTINE_BLOCKED_ADOPTED=0
C2=PASS
```

Capture key, character length, span offsets, and negative sweeps verified via Python on `c7266931a1731db3ff6ae77d.txt`:
```
$ python3 -c '
import hashlib, pathlib, re
u = "https://www.slarc.org.cn/dwyx/CN/article/downloadArticleFile.do?attachType=PDF&id=5237"
p = pathlib.Path("/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/c7266931a1731db3ff6ae77d.txt")
t = p.read_text(encoding="utf-8")
print("key:", hashlib.sha256(u.encode()).hexdigest()[:24], "chars:", len(t))
for q in ["提高动物实验系统评价/Meta 分析的证据确定性：", "李 腾 飞 1,2,3, 郑 卿 勇 1,2, 许 建 国 1,2", "据确定性：GRADE 方法的实证研究[J]. 实验动物与比较医学, 2025, 45", "Med, 2025, 45(1): 101-111. DOI: 10.12300/j.issn.1674-5817.2024.109.", "1674-5817（2025）01-0101-11", "DOI:10.12300/j.issn.1674-5817.2024.109", "Improving the Certainty of Evidence in Animal Experiment Systematic", "Review/Meta-Analysis: An Empirical Study of the GRADE Method", "3 动物实验 SRs/MAs 中应用 GRADE 方法的", "文献特征分析", "检索中国知网、万方、中国生物医学文献数据库、", "中国知网、万方、中国生物医学文献数据库", "PubMed、Embase 和 Web of Science 数据库，检索时间", "从各数据库建立至 2024 年 4 月 1 日", "检索策略结合主", "题 词 （MeSH/Emtree） 和 关 键 词"]:
    print(f"count={t.count(q)} char={t.find(q)} words={len(q.split())} len={len(q)} | {q}")
print("sweeps:", {w: t.count(w) for w in ("布尔","灰色文献","gray","grey","检索式","检索者","NOT")}, "word-AND/OR:", len(re.findall(r"\bAND\b", t)), len(re.findall(r"\bOR\b", t)))
'
key: c7266931a1731db3ff6ae77d chars: 50952
count=1 char=382 words=2 len=25 | 提高动物实验系统评价/Meta 分析的证据确定性：
count=1 char=432 words=12 len=33 | 李 腾 飞 1,2,3, 郑 卿 勇 1,2, 许 建 国 1,2
count=1 char=49152 words=5 len=42 | 据确定性：GRADE 方法的实证研究[J]. 实验动物与比较医学, 2025, 45
count=1 char=49791 words=6 len=67 | Med, 2025, 45(1): 101-111. DOI: 10.12300/j.issn.1674-5817.2024.109.
count=1 char=1633 words=1 len=25 | 1674-5817（2025）01-0101-11
count=1 char=134 words=1 len=38 | DOI:10.12300/j.issn.1674-5817.2024.109
count=1 char=1666 words=9 len=67 | Improving the Certainty of Evidence in Animal Experiment Systematic
count=1 char=1739 words=8 len=60 | Review/Meta-Analysis: An Empirical Study of the GRADE Method
count=1 char=10990 words=6 len=28 | 3 动物实验 SRs/MAs 中应用 GRADE 方法的
count=1 char=11110 words=1 len=6 | 文献特征分析
count=1 char=11211 words=1 len=22 | 检索中国知网、万方、中国生物医学文献数据库、
count=1 char=11213 words=1 len=19 | 中国知网、万方、中国生物医学文献数据库
count=1 char=11299 words=6 len=39 | PubMed、Embase 和 Web of Science 数据库，检索时间
count=1 char=11404 words=7 len=23 | 从各数据库建立至 2024 年 4 月 1 日
count=1 char=11428 words=1 len=7 | 检索策略结合主
count=1 char=11501 words=7 len=25 | 题 词 （MeSH/Emtree） 和 关 键 词
sweeps: {'布尔': 0, '灰色文献': 0, 'gray': 0, 'grey': 0, '检索式': 0, '检索者': 0, 'NOT': 0} word-AND/OR: 0 0
```

## 2. Cell-by-cell audit of `corpus/SOURCES.md:120` (`S110`)

Every located quote below is ≤25 whitespace words and ≤160 characters, occurs **exactly once** (`count == 1`) in `c7266931a1731db3ff6ae77d.txt` read as UTF-8, copied byte-exact with its `text.find(quote)` offset:

1. **`id`** (`S110`): **HOLDS**. New row after base `S106`; maps staged `S117 -> S110` in ascending staged-id order (`S109->S107`, `S110->S108`, `S116->S109`, `S117->S110`, `S119->S111`, `S126->S112`).
2. **`source`** (`提高动物实验系统评价/Meta分析的证据确定性：GRADE方法的实证研究（李腾飞 等）— 实验动物与比较医学 2025;45(1):101-111 — https://www.slarc.org.cn/dwyx/CN/article/downloadArticleFile.do?attachType=PDF&id=5237`): **HOLDS**.
   - `sha256(url)[:24]` = `c7266931a1731db3ff6ae77d`.
   - Title, authors, journal, volume/issue/pages and DOI are all carried in the capture: `提高动物实验系统评价/Meta 分析的证据确定性：` (`char 382`, line 9), `李 腾 飞 1,2,3, 郑 卿 勇 1,2, 许 建 国 1,2` (`char 432`, line 11), `据确定性：GRADE 方法的实证研究[J]. 实验动物与比较医学, 2025, 45` (`char 49152`, line 545), `Med, 2025, 45(1): 101-111. DOI: 10.12300/j.issn.1674-5817.2024.109.` (`char 49791`, line 550), `1674-5817（2025）01-0101-11` (`char 1633`, line 31), and `DOI:10.12300/j.issn.1674-5817.2024.109` (`char 134`, line 3). (The cell omits CJK/Latin typesetter spaces inside the title, which is standard registry prose.)
3. **`kind`** (`paper`): **HOLDS**. Peer-reviewed journal article (`[文献标志码] A [文章编号] 1674-5817（2025）01-0101-11` at `char 1621`, `DOI:10.12300/j.issn.1674-5817.2024.109` at `char 134`, 11-page PDF).
4. **`tier`** (`A`): **HOLDS**. Argued by `scope`: the row is scoped strictly to `what this empirical study states as its own search record, as a working example` (as contrasted with `S111`, a SinoMed index record correctly graded `B`). An own-document statement in the journal's published PDF is primary (tier `A`) for what its own search record states (`QUALITY.md` criterion 7).
5. **`scope`** (`what this empirical study states as its own search record, as a working example`): **HOLDS**. The paper is explicitly an empirical study (`Improving the Certainty of Evidence in Animal Experiment Systematic` at `char 1666` and `Review/Meta-Analysis: An Empirical Study of the GRADE Method` at `char 1739`), and the scope narrows the staged overclaim ("a Chinese review's own search record") to what this empirical study itself states.
6. **`anchor`** (`section 3 文献特征分析, the 检索策略 paragraph; capture .txt read as UTF-8, 50952 characters; char 11110, char 11211, char 11404`): **HOLDS**.
   - Section 3 heading is `3 动物实验 SRs/MAs 中应用 GRADE 方法的` (`char 10990`, line 165) followed on the next right-column line by `文献特征分析` (`char 11110`, line 167).
   - Capture `.txt` read as UTF-8 is `50952` characters (`len(t) == 50952`).
   - Every `char N` in `anchor` equals `text.find(quote)` (`== span_offset + span.find(quote)`) for a located quote of `S110` in `spans.tsv`:
     - `char 11110` = `文献特征分析` (`spans/S110-3.txt`, span offset `11030 + 80 = 11110`)
     - `char 11211` = `检索中国知网、万方、中国生物医学文献数据库、` (`spans/S110-4.txt`, span offset `11131 + 80 = 11211`)
     - `char 11404` = `从各数据库建立至 2024 年 4 月 1 日` (`spans/S110-7.txt`, span offset `11324 + 80 = 11404`)
   - The remaining four `S110` rows in `spans.tsv` also resolve (`char 134` `DOI:10.12300/j.issn.1674-5817.2024.109`, `char 1633` `1674-5817（2025）01-0101-11`, and `char 11213` `中国知网、万方、中国生物医学文献数据库` / `中国知网、万方、中国生物医学文献数据库、`).
7. **`teaches`** (`the record names the databases searched, the date bound from each database's inception to 2024-04-01 and the combination of controlled terms with keywords; it states no boolean string and does not mention grey literature`): **HOLDS** — all five clauses are carried by the capture:
   - *Clause 1 (names the databases searched):* `检索中国知网、万方、中国生物医学文献数据库、` (`char 11211`) and `PubMed、Embase 和 Web of Science 数据库，检索时间` (`char 11299`). (Staged `WebofScience` typo was removed.)
   - *Clause 2 (date bound from each database's inception to 2024-04-01):* `从各数据库建立至 2024 年 4 月 1 日` (`char 11404`).
   - *Clause 3 (combination of controlled terms with keywords):* `检索策略结合主` (`char 11428`) continued after the two-column interleave by `题 词 （MeSH/Emtree） 和 关 键 词` (`char 11501`).
   - *Clause 4 (states no boolean string):* verified by negative sweep over `c7266931a1731db3ff6ae77d.txt` — `布尔` count = `0`, `检索式` count = `0`, `NOT` count = `0`, word-boundary `\bAND\b` = `0`, `\bOR\b` = `0` (all 5 raw `AND` and 17 raw `OR` substrings are inside uppercase English author surnames in the reference list, e.g., `SANDERCOCK` at `char 28043`, `ORCID` at `char 2492`).
   - *Clause 5 (does not mention grey literature):* verified by negative sweep — `灰色文献` count = `0`, `gray` count = `0`, `grey` count = `0`.
8. **`status`** (`mined`): **HOLDS**. Actively cited by `corpus/knowledge/chinese-search-record-r39.md`.
9. **`opened`** (`2026-10-25`): **HOLDS**. Matches round-51 re-open date and `BASE_REV` post-base bound check in `c2-count.py:56,171`.
10. **`recheck`** (`365d`): **HOLDS**. Valid cadence token (`QUALITY.md` criterion 6; `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` exits `0` with `ok`).
11. **`used-by`** (`corpus/knowledge/chinese-search-record-r39.md`): **HOLDS**. Matches `grep -ln '^source: S110 ' corpus/knowledge/*.md` (`corpus/knowledge/chinese-search-record-r39.md:4`) exactly.

## 3. Non-row residual note (outside `SOURCES.md:120`)

While `SOURCES.md:120` (`S110`) and `corpus/knowledge/chinese-search-record-r39.md` narrowed all staged overclaims (`empirical study` instead of `review`, partial re-run instead of re-runnable strategy, field-scoped absence), `corpus/README.md:1090` (copied from `R51DraftReadmeRows.md`) still summarizes `chinese-search-record-r39.md` with the staged phrases `"what a Chinese search record carries and that China has no standard for one yet"` and `"a published Chinese review's own search record (every database, inception to 2024-04-01, the term lists)"`. That does not touch `SOURCES.md:120` or any C1/C2/C3 counter, but is noted for L1 awareness.

VERDICT: Attacked `corpus/SOURCES.md:120` (`S110`) against `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/c7266931a1731db3ff6ae77d.txt` (50,952 chars UTF-8), `spans.tsv`, and `corpus/knowledge/*.md` — all 11 cells (`id`, `source`, `kind`, `tier`, `scope`, `anchor`, `teaches`, `status`, `opened`, `recheck`, `used-by`) HOLD with 0 defects (all 3 anchor offsets `char 11110`, `char 11211`, `char 11404` and all 7 `spans.tsv` quotes verified at `count == 1`, all 5 `teaches` clauses verified by located quotes and 0-count sweeps); row `S110` survives a non-author re-open cleanly.
