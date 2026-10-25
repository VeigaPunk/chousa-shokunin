# GroundBnuB — round 50 / wave 1 — second pass on the CNKI 教师 manual (S107)

Seat: scribe-ground, leaf (no dispatch). Read: frozen claims (6a068f2), operator `RULES.md`, the capture below, `corpus/SOURCES.md` header + S103 row, `build-spans.py` docstring, the read-only staged entry `merge/chousa/knowledge/corpus/knowledge/citation-matching-semantics-r41.md`. No other seat's report opened. No network, no fetch, no lane tool executed, no production file written.

## 0. Capture identity and text form (form of every offset below)
```
$ sha256sum .../.qcache/275c79d45b1e9b0fd32cef93.{pdf,raw,txt}
cbeccf3f612eb68824def16c0c07001f24790b222ce03c5e7cc5b9eebfbfddc1  ...93.pdf
cbeccf3f612eb68824def16c0c07001f24790b222ce03c5e7cc5b9eebfbfddc1  ...93.raw  (1,245,606 B)
8d201ed15c15709dd413d1468e45352011f03c1618c668068977bff5a9703031  ...93.txt  (22,648 B)
$ pdftotext -layout -enc UTF-8 ...93.raw o.txt && sha256sum o.txt
8d201ed15c15709dd413d1468e45352011f03c1618c668068977bff5a9703031  o.txt
$ python3 -c 'import hashlib;print(hashlib.sha256("https://bs.bnu.edu.cn/docs/20160407183946745914.pdf".encode()).hexdigest()[:24])'
275c79d45b1e9b0fd32cef93
```
Form: `275c79d45b1e9b0fd32cef93.txt` read as UTF-8 — 9,914 characters, byte-identical to `pdftotext -layout -enc UTF-8` (poppler 26.08.0) of the `.raw`; `.raw` == `.pdf`; `build-spans.py`'s `key(url)` reproduces the stem. `.txt` is the builder's first form and every quote below occurs in it exactly once (`text.count(quote)==1`), so no UTF-16LE `.raw` fallback is involved.

## 1. Title, version, date stamp
```
$ pdfinfo ...93.raw
Title:           “中国知网”大学生论文管理系统     Author: wsy     Creator: WPS Office 个人版
CreationDate:    Mon Mar 10 15:37:30 2014 -03     ModDate: Mon Mar 10 15:37:30 2014 -03
Pages: 17     PDF version: 1.7     Encrypted: no     Custom Metadata: no     Metadata Stream: no
```
`pdfinfo -meta` prints no XMP block. Cover, char 0–70: `“中国知网”\n大学生论文管理系统使用手册\n（教师）`, publisher stamp at char 44 (`CNKI 科研诚信管理系统研究中心`).

- **No in-text version or date stamp.** Occurrence counts over the 9,914-char `.txt`: `年` 0, `月` 0, `更新` 0, `修订` 0, `2016` 0, `版本` 0, `日期` 0 — there is no "更新 20xx 年 x 月" line to cite.
- Two dates on disk disagree: PDF Info `CreationDate = ModDate = 2014-03-10 15:37:30 -03` (single revision, not re-saved) versus the URL basename `20160407183946745914` = 2016-04-07 18:39:46, the host's upload-path stamp, not a document date. The only document date is 2014-03-10; reading the URL stamp as the manual's date overstates its currency by ~25 months.
- Self-name is 大学生论文管理系统 (17 = 16 running headers + cover title); `学术不端` alone is 0 — it names 《学术论文不端行为的界定标准》 5× but never calls itself a 学术不端行为检测系统.

## 2. Host (北京师范大学 mirror)
The text form never names its host: `北京师范大学` 0, `bs.bnu` 0, `http` 0. Host evidence is the URL alone (`https://bs.bnu.edu.cn/docs/…`, 北京师范大学). With the cover stamp, the document is CNKI-authored (CNKI 科研诚信管理系统研究中心) and university-hosted — a mirror copy, not a CNKI-served original; nothing in the manual states a distribution or mirror status.

## 3. What the 教师 account can do (documented)
- 一 教师登录 (p.3): choose school first (by 地区/省市 or by typing the name into 检索, char 1995), then 用户名 + 密码 + 身份（教师） + 验证码 → 登录. Identity is school-scoped.
- 2.1 (p.4): the list holds only 该指导老师下属的各学生提交的最新一篇论文; filter by 篇名/作者, by 届, by 未审阅/已审阅; sort by 检测结果 or 提交次数.
- 2.2.1 (p.5–11): 5-part result page — basics + 检测范围 popup; 文字复制比 family (总/去除引用/去除本人已发表/单篇最大); paragraph and 前部/后部 indicators; 中英文互检 (only where enabled); 7 指标 from 《学术论文不端行为的界定标准》; 重合文字来源列表 with 引证关系; 文献溯源; 逐一对比 / 初始化; 全文标红 with double-click lookup; 5 报告单 forms + download original.
- 2.2.2 (p.12): 两两比对 — full-text comparison of two uploaded documents for overlapping text.
- 2.2.3 + 2.2 审阅意见 (p.12–13): download originals (single/all, packaged) or export Excel; 修改意见 + 审阅意见, saved automatically and returning to the review list. 2.3 (p.14–16): report forms, 保存/打印.
- 三 (p.16): 学生信息 list sortable by 姓名/学号/届/院系/专业/班级; per-student password reset (random new password); export to Excel. 四 (p.17): change own password.

## 4. Does the manual say anything about checking a citation against CNKI's resources?
**No.** Occurrence counts over the 9,914-char `.txt` (`re.finditer`): `核对` 0, `匹配` 0, `引文核对` 0, `数据库` 0, `资源` 0, `会议` 0, `网络` 0, `自建库` 0. `中国知网` 17 = 16 running headers + cover title, zero body mentions (each occurrence verified to start the running-title string). The nearest constructs:

- `引文` 9 — one TOC line plus 8 uses, all inside the compound report-form name 全文（标明引文）/全文标明引文. The manual never defines 标明引文 and never uses 引文 standalone.
- `引证` 2 — 引证关系, an attribute beside each matched source in 重合文字来源列表 (2.2.1 第 4 部分) and in the 简洁报告单 (2.3.1 第 4 部分): the relation between the checked document and a matched source, not a check of a citation against a catalogue.
- `引用` 8 — the manual's own wording for a marked citation is the phrase 文中标明了引用的文献, inside the 去除引用文献复制比 definition (char 2955).

What it does document about "what is compared" is a **scope popup with unnamed contents**: `检测范围` is defined only as 本篇文献的比对范围, opened by clicking 查看 (char 2648). The compared corpus is called 相似文献 (6) / 来源文献 (7) and never enumerated; 期刊 and 学位论文 occur only inside the misconduct definitions. So this manual cannot be cited for *what* CNKI compares against — only for the existence of a comparison scope and for document-to-document comparison (两两比对, 逐一对比).

## 5. QUOTE machine lines (`.txt` form; each occurs exactly once; offsets = `text.find`)
```
QUOTE	S107	https://bs.bnu.edu.cn/docs/20160407183946745914.pdf	CNKI 科研诚信管理系统研究中心	corpus/knowledge/citation-matching-semantics-r41.md
QUOTE	S107	https://bs.bnu.edu.cn/docs/20160407183946745914.pdf	验证码，点击“登录”按钮登录系统。	corpus/knowledge/citation-matching-semantics-r41.md
QUOTE	S107	https://bs.bnu.edu.cn/docs/20160407183946745914.pdf	论文审阅页面主要展示了该指导老师下属的各学生提交的最新一篇论文。	corpus/knowledge/citation-matching-semantics-r41.md
QUOTE	S107	https://bs.bnu.edu.cn/docs/20160407183946745914.pdf	点击排序按钮，可以按照检测结果、提交次数进行排序。	corpus/knowledge/citation-matching-semantics-r41.md
QUOTE	S107	https://bs.bnu.edu.cn/docs/20160407183946745914.pdf	检测范围是指本篇文献的比对范围，点击“查看”可打开弹框。	corpus/knowledge/citation-matching-semantics-r41.md
QUOTE	S107	https://bs.bnu.edu.cn/docs/20160407183946745914.pdf	去除引用文献复制比：指去除了作者在文中标明了引用的文献后，	corpus/knowledge/citation-matching-semantics-r41.md
QUOTE	S107	https://bs.bnu.edu.cn/docs/20160407183946745914.pdf	其文字复制比例和引证关系，点击其篇名可查看检测文献与来源文献之间的比对	corpus/knowledge/citation-matching-semantics-r41.md
QUOTE	S107	https://bs.bnu.edu.cn/docs/20160407183946745914.pdf	教师可以点击“文献溯源”逐条查看检测文献与来源文献的重合情况	corpus/knowledge/citation-matching-semantics-r41.md
QUOTE	S107	https://bs.bnu.edu.cn/docs/20160407183946745914.pdf	教师还可以选择某篇来源文献，点击“逐一对比”	corpus/knowledge/citation-matching-semantics-r41.md
QUOTE	S107	https://bs.bnu.edu.cn/docs/20160407183946745914.pdf	进入学生上传文件后，点击“两两比对”按钮，可以比对两篇文献的全文，	corpus/knowledge/citation-matching-semantics-r41.md
QUOTE	S107	https://bs.bnu.edu.cn/docs/20160407183946745914.pdf	选中某个或者全部的学生信息，点击“导出 Excel”按钮	corpus/knowledge/citation-matching-semantics-r41.md
```
Offsets in the same order (chars, each `count==1`; all ≤35 chars, ≤2 whitespace words, no newline/TAB): 44, 2042, 2186, 2437, 2648, 2955, 6968, 7010, 7072, 7518, 9694. All 11 lie outside the 报告单 section (2.3, roughly char 7,980–9,560); the 引证关系 and 文献溯源 quotes come from 2.2.1's result page, not 2.3.1.

## 6. Conflict with the staged entry (verbatim; for the canonical judge, not for me to resolve)
Staged `citation-matching-semantics-r41.md`, Observation ¶2, verbatim:
> The 大学生论文管理系统 子账号 manual contains no 引文核对 section at all (zero
> occurrences of 引文核对, 核对 and 匹配 across 30,937 extracted characters), and
> neither does the 教师 manual, which instead uses 引文 to mean a thesis's own
> citations listed on a report sheet.

- Core claim holds and widens here: `引文核对` 0, `核对` 0 **and** `匹配` 0 over the 教师 manual's 9,914 characters (the entry claims only 引文核对 = 0 for it; the 30,937-char figure is the 子账号 capture, which I did not open).
- The gloss "uses 引文 to mean a thesis's own citations listed on a report sheet" is not what the text says: 9/9 occurrences are inside the report-form name 全文（标明引文）/全文标明引文 (one a TOC line), the manual never defines 标明引文, and it never uses 引文 standalone. Defensible narrower sentence: 引文 appears only in that report-form name, and its own gloss for a marked citation is 文中标明了引用的文献 (char 2955).
- The entry omits 引证关系 (2 occurrences), the one citation-relation term the manual carries — not a contradiction of its thesis, but a gap a Gate reader can point at.

## 7. Integration notes and limits (no predicate/target/counter/control proposal)
- The staged source line for this URL reads `source: S145 — https://bs.bnu.edu.cn/…`; per the wave spec the lane id is S107 (registry max S103; `grep -n "bnu" corpus/SOURCES.md` → no row, so the row is new).
- The three theme entries are absent from `corpus/knowledge/` at lane HEAD 7754172; they exist only in the read-only staged package. The staged anchor `# 全文（标明引文）报告单` is a heading; C2's "at least one `char N` equal to a quote offset" can be satisfied from the offsets in §5.
- Limits: I did not open the 子账号 or 管理员 captures, so nothing here scores their claims; I did not run `c1-count.py`/`c2-count.py`/`build-spans.py` (a scribe reports, it does not re-run the counters); the 2014-03-10 date is the PDF's own Info dictionary, not checked against any external record (no network); page numbers are the manual's printed footers (`第 3 页` … `第 17 页`).
- Tooling: nothing installed or upgraded (none needed; pacman is host-paused).

VERDICT — Attacked the staged entry's 教师-manual claims against the on-disk capture: the "no 引文核对" claim survives and widens (核对/匹配 = 0), but its 引文 gloss does not match the text (9/9 occurrences sit inside the report-form name, and 引证关系 is unmentioned); the manual carries no in-text version, date stamp or host name, so its only document date is PDF Info 2014-03-10, not the URL's 2016-04-07.
