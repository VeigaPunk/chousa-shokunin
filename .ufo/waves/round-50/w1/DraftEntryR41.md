# Round 50 w1 — DraftEntryR41 (chousa): citation-matching-semantics-r41 draft + inference-ground falsifier

Seat: leaf scribe, no subagents. Captures opened read-only under
`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/`; no network. Scratch
`/dev/shm/chousa-r50-DraftEntryR41/` (deleted at hand-off). No lane file was written.

## Deliverable — lane path `corpus/knowledge/citation-matching-semantics-r41.md` (32 lines)

```markdown
# CNKI's 引文核对 compares a pasted citation against CNKI's own literature record, part by part

source: S105 — https://gs.sxu.edu.cn/docs/2025-03/9e5cdd215a414bf6b5694912018de4c8.pdf — §6.1 引文核对, under 第 6 章 辅助功能 — char 48 (edition line), char 30738, char 30778, char 30793, char 30880, char 30947, char 31101, char 31218, char 31273
source: S106 — https://rwxy.seu.edu.cn/_upload/article/58/cc/5a2fdc1940cfa2522e82ba8b5d81/fb75a598-a343-48f2-bb42-5c6c411506bc.pdf — §2.6 仅去除第一作者本人文献 — char 83 (title block), char 22511, char 22549
source: S107 — https://bs.bnu.edu.cn/docs/20160407183946745914.pdf — §2.3.2 全文（标明引文）报告单 — char 44 (imprint line), char 7995, char 8033
verified-at: 2026-10-25
recheck: 180d — from any cwd, with `QCACHE=/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache`: `python3 -c "import sys;[print(len(t:=open(a,encoding='utf-8').read()),t.count('匹配'),t.count('引文核对'),t.count('辅助'),t.count('查重')) for a in sys.argv[1:]]" "$QCACHE"/e3ca8f4fdd15420b80096a75.txt "$QCACHE"/28750bcdf5d36cd90a7709fb.txt "$QCACHE"/275c79d45b1e9b0fd32cef93.txt` → `38174 0 4 5 0`, `30937 0 0 0 0`, `9914 0 0 0 0`; `python3 -c "import sys;t=open(sys.argv[1],encoding='utf-8').read();s=t.find('6.1 引文核对',30000);e=t.find('6.2 两两比对',s);x=t[s:e];print(s,e,len(x),[x.count(w) for w in ('排序','权重','相似度','算法','匹配','字段','复制比','去除本人')])" "$QCACHE"/e3ca8f4fdd15420b80096a75.txt` → `30727 31262 535 [0, 0, 0, 0, 0, 0, 0, 0]`; then re-download the three copies and confirm §6.1 still opens 引文核对是指，以“中国知网”的文献资源为核对源内容
ground: PROVINCE.md claim-vs-source verification — what a citation-checking feature compares as the vendor's own manuals state it, and which manual documents it
adopted: round 50 from the campaign package `merge/chousa/`, re-bound by document to S105, S106 and S107 (the staged-to-lane id map is in `corpus/lessons/round-50.md` `## Gate`)

#### Observation

- **What the 管理员 copy says the feature is.** In the copy hosted at gs.sxu.edu.cn (edition line `更新时间：2020 年 7 月`, char 48) §6.1 of the 辅助 module is one definition plus three states: `引文核对是指，以“中国知网”的文献资源为核对源内容` (char 30738) — the comparison source is CNKI's own literature resource. The one documented input step is `把待检测文献的参考文献复制到“引文核对”文本框` (char 30793), and the returned list shows `状态、篇名、作者和文献来源` (char 30880) (S105).
- **The three states grade one returned record.** `第一类是“没找到”，表示经过核对，没有找到与输入的这条引文一一对应` (char 30947) — no record corresponds one-to-one; the orange state is `但是引文中有某一部分的信息与源内容不同` (char 31101), hover naming the differing part; the green state is `各项内容都相同` (char 31218) — each item of the citation equals the source content (S105).
- **The section publishes no method.** The `recheck:` slice sweep prints `30727 31262 535 [0, 0, 0, 0, 0, 0, 0, 0]`: the whole §6.1 slice (chars 30727–31262, 535 characters) carries no ranking, weight, similarity, algorithm, field-selection or ratio word. 匹配 also occurs 0 times in the whole 38,174-character copy, and the section's own verb is 比对 (`以核对引文内容的正确性`, char 30778). 比对 is not one mechanism in this copy: §6.2's is `两两比对是将输入的两篇文献进行比对` (char 31273), a document-to-document comparison. The copy states a comparison source and a verdict granularity, not a matching method (S105).
- **The self-citation option is a folder property of the detection flow.** In the 子账号 copy (title block `产品名称：“中国知网”大学生论文管理系统使用手册`, char 83) §2.6 opens `在创建文件夹页面中第一个选项为“仅去除第一作者本人文献”` (char 22511) and says the folder's documents `该文件夹下的所有检测文献在去除本人文献检测结果中` (char 22549) have first-author self-matches removed, so the two 文字复制比 figures differ (S106). The 管理员 copy carries the same option as §3.7 (`创建文件夹时，设置文件夹的属性中，第一个选项为“仅去除第一作者本人`, char 27587) — still a folder property (S105).
- **Neither 大学生论文管理系统 copy documents 引文核对 or the 辅助 module.** The `recheck:` occurrence sweep prints `38174 0 4 5 0` / `30937 0 0 0 0` / `9914 0 0 0 0` (S105 / S106 / S107): 引文核对 4 / 0 / 0, 辅助 5 / 0 / 0, 匹配 and 查重 0 everywhere — so 查重 is not the manuals' own word either. In the 教师 copy (imprint `CNKI 科研诚信管理系统研究中心`, char 44) 引文 occurs 9 times and every occurrence sits inside 标明引文, the report-sheet name: `教师可查看的报告单包括简洁报告单、全文（标明引文）报告单、去除本人` (char 8033), and `点击论文列表内的“选择报告单”，可以打开该篇论文的报告单查看。` (char 7995) — a report sheet, not a checking feature (S107).
- **The two feature texts do not meet.** §6.1 sits under `第 6 章 辅助功能` (char 30661); its 535-character slice contains 复制比 0 and 去除本人 0; the folder option sits in chapter 3 of the same copy, and neither section refers to the other (S105).

#### Inference

- **Catalogue lookup, then a part-by-part verdict — that much the copy states.** S105 gives the comparison source (`引文核对是指，以“中国知网”的文献资源为核对源内容`) and a verdict that either names a differing part (`但是引文中有某一部分的信息与源内容不同`) or finds every item equal (`各项内容都相同`). That is a lookup against CNKI's own record followed by a comparison of the citation's parts with the record — what this copy states, and nothing more specific.
- **The staged claim that the feature is not an author-year or string-similarity algorithm is narrowed to: undocumented.** S105's §6.1 slice carries 算法 0 and 相似度 0, and the copy's own verb is 比对 (`以核对引文内容的正确性`); no matching method is stated anywhere in it. Absence of a method description cannot establish absence of a similarity step, so what is kept is that this copy documents no matching method — not that CNKI uses none.
- **The self-citation rule is documented as acting on a ratio, and nothing links it to 引文核对.** S106 places the option on the folder page (`在创建文件夹页面中第一个选项为“仅去除第一作者本人文献”`) and ties it to the 去除本人文献检测结果, while S105's §6.1 slice contains 复制比 0 and 去除本人 0. The two are documented as separate features; whether the rule bears on a citation verdict is not settled by either copy, and the silence is not a denial.
- **Which manual documents the feature is a product fact before it is a role fact.** S105 documents the 辅助 module of 知网学位论文学术不端行为检测系统 (`第 6 章 辅助功能`), while S106 and S107 document a different product (`产品名称：“中国知网”大学生论文管理系统使用手册`) and carry 辅助 0 times each. No 管理员 manual for the 大学生论文管理系统 was opened, so these three copies cannot settle whether that product has the feature for any role; the narrow statement is that only the 学位论文检测系统's 管理员 copy documents it.

#### Unknown

- How a pasted citation becomes a query: which fields are searched, whether the whole string is used, how candidates are ordered. §6.1 states the paste step and the grading of a returned record only.
- Whether 大学生论文管理系统 has the feature at all: neither copy carries the 辅助 module, and no 管理员 manual for that product is in this capture set.
- Whether the implementation compares by similarity or by an author-year key. The copies state no method; probing the feature with crafted citations would be a different kind of evidence and would need its own label.
- Whether 仅去除第一作者本人文献 changes a 引文核对 verdict in practice: neither copy links the two, and absence of a link is not a statement about behaviour.
```

## Gates I ran on the draft (observed output)

1. Quote re-open. All 17 backticked CJK spans are capture quotes; each occurs exactly once in its
   own `.txt` (UTF-8) and once nowhere else in the other two captures; max 33 chars / 4 whitespace
   words. Per-id span rows S105 11, S106 3, S107 3; every `char N` in every `source:` anchor cell is
   a located quote offset (S105 9/9, S106 3/3, S107 3/3). Only `S105`,`S106`,`S107` occur as S-tokens.
   The two other backticked spans in the draft sit on the `recheck:` header line and are shell
   commands, not quotes (my extractor refused them by name: not present in any capture).
2. `python3 tools/inference-ground.py --entry draft.md --spans spans.tsv --counts /dev/null --root .`
   → `GROUND entry=draft.md section=1 bullets=4 tokens=0 grounded=0` + 4 × `INF_UNGROUNDED`, rc=1.
3. Same entry, tool patched (below) → `tokens=7 grounded=7`, `GROUND: PASS`, rc=0.
4. `python3 corpus/evidence/round48/precision-count.py --tool <tool>` → `CORRECT_BULLETS_PASS=12/12`
   `PRECISION_GATE=PASS` for BOTH the unpatched and the patched tool: the patch is inert on Latin text.

## Findings — staged entry claims I could not keep, and why

- **F1 (blocks the C2 leg). `inference-ground` cannot ground a Chinese bullet.** `WORD_RE` is
  `[A-Za-z]` (tools/inference-ground.py:77) and `has_two_words` counts only whitespace tokens with an
  ASCII letter (:87–90); a CJK phrase is one token with none, so every grounded Chinese quote reads
  as zero words. Reproduced on the draft: `tokens=0`, four `INF_UNGROUNDED`. Round 49 passed only
  because its Japanese quotes carried Latin runs (`CiNii Researchの…`, `1.DOI（メタデータ項目） をもとに検索`).
  These captures are pure Chinese; their only ASCII-bearing 2-token phrases are
  `https://*.cnki.net/，…ActiveX` (S105 char 27431 / S106 char 22353) and the upload-format list
  (S105 char 11788) — off-argument, so no honest gate-satisfying bullet exists without the patch.
  C2's predicate is frozen; the fix belongs to the tool, not the predicate.
- **F2 (drafting trap).** An English paraphrase in straight double quotes inside `#### Inference` is
  read by `QUOTE_RE` as a token and refused `INF_TOKEN_NOT_IN_SPAN` (observed, bullets 1–2 of my
  first draft). Paraphrase unquoted; reserve `"…"` for verbatim capture text.
- **F3. 查重 is not the manuals' word**: 0 / 0 / 0 (`t.count('查重')`); the copies say 检测 / 创建文件夹, so the draft says "folder property of the detection flow".
- **F4. The 仅去除第一作者本人 option is not 子账号-only**: §2.6 of S106 (char 22511) AND §3.7 of
  S105 (char 27587). The staged entry cited only the 子账号 copy; the "two features never meet"
  claim survives only as "neither section refers to the other".
- **F5. "documented on the administrative side" overreaches**: S105 is 知网学位论文学术不端行为检测
  系统（管理员）, S106/S107 are “中国知网”大学生论文管理系统（子账号/教师） — two products, and
  neither 大学生 copy carries the 辅助 module (辅助 0/0). The absence is a product difference first;
  no 管理员 manual for the 大学生 product was opened, so role cannot be concluded. Draft says "as
  this copy states" for both mirrors.
- **F6. The staged algorithm negative is narrowed**: 匹配 0 and the §6.1 slice's 算法 0 / 相似度 0
  support "no method is documented", not "not an author-year or string-similarity algorithm" —
  absence of a description cannot establish absence of a step.
- Verified as staged: 引文核对 4/0/0; 子账号 30,937 chars with 引文核对 0, 核对 0, 匹配 0; 教师 引文 9/9 inside 标明引文; §6.1 definition and the three states verbatim.

## Proposed tool change — lane path `tools/inference-ground.py` (not applied by me)

```python
CJK_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")

def has_two_words(s: str) -> bool:
    words = [w for w in re.split(r"\s+", s.strip()) if WORD_RE.search(w)]
    if len(words) >= 2:
        return True
    # A Chinese phrase carries no spaces, so a token count reads every grounded
    # Chinese quote as zero words: round 50's draft entry produced tokens=0 and
    # four INF_UNGROUNDED findings on four correctly-grounded bullets. Four CJK
    # characters is the floor for two words. Named limit unchanged: `words()` is
    # Latin-only, so a CJK phrase never trips the polarity check.
    return len(CJK_RE.findall(s)) >= 4
```

Changes no frozen predicate text (the docstring already says "two or more words") and adds no new
hole in kind: presence is all it checks, which is the counter's declared limit. Validate with
`precision-count.py` (12/12 observed on both tools).

## Frozen-counter observation (read-only; not my axis, recorded for the L1)

- `python3 corpus/evidence/round50/c1-count.py` (TMPDIR under /dev/shm) → `SELFTEST_DEFAULT=PASS`,
  `BASELINE=PASS rc=0 findings=26`, `PERTURB_PASS=6/6`, `EXPECTED_BAD=PASS rc=2`,
  `R49_REGRESSION=PASS rc=0`, `LEGS=5/5`, `C1=PASS` rc=0.
- `python3 corpus/evidence/round50/c2-count.py` → `ENTRIES=0/3 … SUBSTANCE=FAIL … C2=FAIL` rc=1, identical to the before block of `controls/c2-before.txt` (the draft is not landed).

Touched: this report only. Not touched: lane entries, `corpus/SOURCES.md`, `tools/`, the git index,
`/home/vgpnk/Projects/shokuknow` (read-only), campaign tools. Nothing installed.

VERDICT — drafted `corpus/knowledge/citation-matching-semantics-r41.md` (17 exactly-once quotes,
3 ids, every anchor `char N` a quote offset) and falsified one frozen leg: `inference-ground`
refuses every pure-CJK quote (`tokens=0`, 4 × INF_UNGROUNDED), so C2's "all three entries exit 0"
cannot hold for this theme until the 3-line `has_two_words` fix lands (patched: PASS; R48 12/12).
