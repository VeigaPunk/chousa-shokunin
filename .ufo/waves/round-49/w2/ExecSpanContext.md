# ExecSpanContext — R49 W2: context attack on all 28 spans

Seat: leaf, chousa lane, R49 W2 (FALSIFY). Claims frozen fe740e7; measured code 4ce61fc. No predicate, target or counter changed; no production file written.
Method: resolve each row to its capture FORM by file digest, re-slice it, print the committed span with the quote marked, read both sides against the entry sentence and the capture's headings.

## 1. Form resolution + exact-slice integrity (all 28 rows)
cmd `python3 integ.py` (hashes `.txt`/`.raw` of `sha256(url)[:24]`, matches `capture_sha256`, re-slices):
- S096(3)/S097(2)/S098(5)/S099(3)/S102(3)/S103(4) = 20 rows resolve to the **.txt** form (digest == txt sha);
- S100(3)/S101(5) = 8 rows resolve to the **.raw** form (digest == raw sha, e.g. S100 `46d1866ce9af` vs txt `ce30e73574e7`);
- all 28: `slice=True uniq=True qpos=True` (`INTEGRITY_BAD= 0`); only these rows are not 80/80:
```
S100-1 pre=0  post=80 EMPTY_SIDE SHORT_SIDE     S101-1 pre=39 post=80 SHORT_SIDE
S100-2 pre=8  post=1  SHORT_SIDE                S101-2 pre=4  post=80 SHORT_SIDE
S100-3 pre=80 post=34 SHORT_SIDE                S101-4 pre=48 post=0  EMPTY_SIDE SHORT_SIDE
                                                S101-5 pre=4  post=80 SHORT_SIDE
```
Every non-80 side is in a `.raw` row; 7 of the 8 raw rows are truncated, 2 to zero.

## 2. Raw-form CR clip: boundary audit
cmd `python3 rawclip.py` (for each raw row: char before span start, char at span end, 40-char shoulders):
```
S100 start=1296 end=1401 before='\r' at_end='6'  L40="中国知网他引频次查询方法说明\r\r"  R40="62791829，18601173042\r\r关于自引的说明：…"
S100 start=1423 end=1471 before='\r' at_end='\r' L40="…18601173042\r\r"                 R40="\r\r他引频次具体查询方法如下：…"
S100 start=2781 end=2909 before='儀' at_end='\r' L40="…䡋䩏䩑࡜征ň漀Ị̃⭪Юᘀ౨㼑䌀ᡊ…"      R40="\r\r图4\r\r   \r\r图5\r\r4.检索作者的论文\r…"
S101 start=11166 end=11310 before='\r' at_end='领' L40="(CLC — Chinese Library Classification)。\r" R40="领导讲话、政策性评论…"
S101 start=11166 end=11263 before='\r' at_end='性' L40="(CLC — Chinese Library Classification)。\r" R40="性技术成果报告(科技)…"
S101 start=12081 end=12252 before='集' at_end='\x0b' L40="…者-出版年制。\r14.2参考文献著录项目a. 主要责任者…" R40="h. 文献起止页码；i. …\r14.3"
S101 start=11945 end=12048 before='\r' at_end='\r' L40="…作为标志。\r14 参考文献(References) \r" R40="\r14.2参考文献著录项目a. 主要责任者…"
S101 start=34370 end=34470 before='\r' at_end='t' L40="15.6文章总篇数，…据此计算载文量。\r" R40="thod）。\r16 电讯地址…"
```
Every clip lands on a Word paragraph mark, and every raw quote is whole at both ends (S100-1/S100-2/S101-2/S101-4/
S101-5 end in `。` or open a paragraph; none is severed mid-sentence). **The named hazard does not materialise.**
What the clip does do — cmd `python3 prewin.py`, pre-repair window vs committed span:
```
S100-1 pre-repair [1216:1401] "中国知网他引频次查询方法说明\r\r中国知网他引频次的查询需要使用《中国引文数据库》。…" ; committed len 105, pre=0
S101-4 pre-repair [11865:12048] "…\r14 参考文献(References) \r14.1参考文献是…之一,本规范推荐…作者-出版年制。" ; committed len 103, post=0
```

## 3. Each span, quote marked (cmd `python3 table.py`; `pre|`=left context, `|post`=right)
```
S096-1 pre 80|ている論文が引用して…時増加していきます。 \n \n\n \n \n ※| «CiNii Researchの「参考文献」は、実際の論文の参考文献と必ずしも一致していません» |。実際の論文の参考文献のうち、CiNii Resea…文での掲載数ではなく| post 80
S096-2 pre 80|の参考文献と必ずしも…理で、同定・統合された参考文献だけが表示されます。 | «参考文献数も、論文での掲載数ではなく同定・統合された分をカウントしています。» | \n\n また、CiNii Researchでは、…定・統合処理を行って| post 80
S096-3 pre 80|chの同定・統合処理…統合された分をカウントしています。 \n\n また、| «CiNii Researchでは、CiNii Articlesとは 文献の収録範囲が異なっており» |、（それに伴って）別の手法で同定・統合処理を行ってい…いません。 \n\n| post 80
S097-1 pre 80|\n \n \n \…引用文献および被引用文献へのリンクが表示されます。 | «J-STAGEが連携している外部サービス に登録されている引用文献および被引用文献には、J-STAGEでの記事公開から数日～2週間後にDOIによるリンクが作成されます» |。 このうち、PubMedやCASに収録されているも…n \n\n \n | post 80
S097-2 pre 80| \n\n \n\n…す。\n \n\n \n\n \n \n ※ \n | «DOIがURLとして使用できるようになるには、J-STAGEでの公開から1日～数日程度かかります。» | \n \n\n \n\n \n \n \n \n\…が公開されると、引用| post 80
S098-1 pre 80|PDF) \n \n…\n \n 記事に登録された引用文献の情報をもとに、| «システムが引用元の所在を特定できた文献にリンクを付与しています» |。\n\n リンクの付与は、以下のタイミングで検索を…リンク削除・問い合わ| post 80
S098-2 pre 80|集の原文問合わせ機能…時にシステムで引用元の所在を検索\n\n \n\n | «引用元の所在確認は、次の順で解析・検索を実施しています» |。\n\n 1.DOI（メタデータ項目） をもとに検…号ページなど\n\n| post 80
S098-3 pre 80|わせ機能\n\n 2…認は、次の順で解析・検索を実施しています。\n\n | «1.DOI（メタデータ項目） をもとに検索　例：10.xxxx» |\n\n 2.書誌情報（メタデータ項目） をもとに検…n 4.引用文献の原| post 80
S098-4 pre 80|\n\n 1.DOI…に検索　項目：著者名、誌名、巻号ページなど\n\n | «3.引用文献の原文情報からDOIを検出して検索» |\n\n 4.引用文献の原文情報を書誌情報に解析して…、カンマ(,)やan| post 80
S098-5 pre 80|：10.xxxx\n…引用文献の原文情報からDOIを検出して検索\n\n | «4.引用文献の原文情報を書誌情報に解析して検索» |\n \n\n \n \n \n 引用文献で複数の著…はどのように記述すれ| post 80
S099-1 pre 80|fessional …tic of "lateral reading": | «leaving an unfamiliar website to search the open Web before investing attention in the site at hand» |. Professional development…en impleme| post 80
S099-2 pre 80|hen implem…ndated government course. | «Using a matched control design, students in treatment classrooms (n = 271) were compared to peers (n = 228) in regular classrooms.» | A multilevel linear mixed…classrooms| post 80
S099-3 pre 80|A multilev…n experimental classrooms | «grew significantly in their ability to judge the credibility of digital content» |. These findings inform ef…ecisions a| post 80
S100-1 pre  0|| «中国知网他引频次的查询需要使用《中国引文数据库》。» |为了配合此轮评估工作，大部分高校已经开通了试用，您可…，咨询电话：010-| post 80
S100-2 pre  8|关于自引的说明：| «对于合作发文的参考文献中，如果引文出现了任一合作者，那么这条引文将被认定为自引» |。| post  1
S100-3 pre 80|J开ň漀Ĩᘚ౨㼑䌀ᡊ…、“出版时间”、“文献来源”等方式进行组合查询，注：| «被引频次为0的文献将不会显示» |。高级检索按钮如图4中的红框所示，在弹出的高级检索页面中如图5所示：| post 34
S101-1 pre 39|11.6为便于文献的…期刊评价，确定文献的检索范围，提高检索结果的适用性，| «每一篇文章或资料应根据其内容性质标识一个文献标志码» |。本规范共设置以下五种：A——基础性理论与应用研究…技术管理性文章(包括| post 80
S101-2 pre  4|11.6| «为便于文献的统计和期刊评价» |，确定文献的检索范围，提高检索结果的适用性，每一篇文…用研究 B——应用| post 80
S101-3 pre 80|主编、学位申报人、专…本项数据中不得出现缩写点。b. 文献题名；c. | «文献类型及载体类型标志» |；d. 其他责任者(译者、校注、校点、校勘者等)；…子文献的可获得地址；| post 80
S101-4 pre 48|14.1参考文献是学…成部分，是对期刊论文进行统计和分析的重要信息源之一,| «本规范推荐采用GB/T 7714中规定的顺序编码制格式著录,也可采用GB/T 7714中规定的作者-出版年制。» || post  0
S101-5 pre  4|15.7| «参考文献格式，参照ISO 690» |，采用1位字母：n——顺序编码制（Numeric r…nd date me| post 80
S102-1 pre 80|ます。\n\n\n\…リスト\n\n検索結果には、「篇名」「作者」「刊名」| «「发表时间」「被引」「下载」» |の他、文献に対して可能な操作が一覧で\n表示されます…とその文献の摘要を確| post 80
S102-2 pre 80|る雑誌の情報を確認す…28\n「发表时间」「被引」\n         | «「下载」はそれぞれ文献の公開時期、被引用回数、ダウンロード回数を示します。» |\n\n\n\n\n「操作」には 4 つのアイコンが…    29\n文| post 80
S102-3 pre 80|起点その広がりをビジ…きます。\n\n\n\n\n6.4 引文网络\n\n| «当該文献を中心に年毎の参考、被引用の関係をビジュアルに提示» |、それぞれの文献にアクセスすることもで\nきます。\…6 相关文献推荐\n| post 80
S103-1 pre 80|于知网全库资源为用户…左侧为问答区，用户输入想要研究的学术问题\n\n后，| «CNKI AI 根据相关文献，生成可信增强回答。» |右侧为溯源文献展示区，展示\n\n文献的标题、摘要、…多的文献信息，包含摘| post 80
S103-2 pre 80|区，用户输入想要研究…\n\n文献的标题、摘要、作者、出版日期、文献来源、| «来源数据库» |、引用量以及下载\n量。点击右侧文献的“更多”可以…来源展示区一页最多展| post 80
S103-3 pre 80|想要研究的学术问题\…的标题、摘要、作者、出版日期、文献来源、来源数据库、| «引用量» |以及下载\n量。点击右侧文献的“更多”可以展示更多…区一页最多展示五篇文| post 80
S103-4 pre 80|维度的检索功能，支持…有文章。用户可\n\n通过输入检索词完成查询，并按照| «相关度、发表时间、被引次数和下载量» |四种排\n\n序方式从高到低进行结果排序。检索结果以…户可通过翻页功能\n| post 80
```

## 4. Substance check
cmd `export TMPDIR=/dev/shm/chousa-r49-ExecSpanContext && python3 corpus/evidence/round49/quote-substance-check.py`
```
IDS=8 QUOTES=28 FAILURES=0
exit=0
```

## 5. Boundary markers inside spans (cmd `python3 markers.py`)
```
S097-2 heads=['2. 引']                      S102-1 pages=['25','26'] heads=['5.6 検','5.6.']
S098-2/3/4/5 heads=['1.D','2.書','3.引','4.引']  S102-2 pages=['28','29']
S097-1 heads=['2. 引']                      S102-3 pages=['41'] heads=['6.4 引','6.5 参','6.6 相']
```

## Findings
- **F1 (finding, context empty on one side).** S100-1 `pre=0` and S101-4 `post=0`. Cause is the 4ce61fc CR repair
  (build-spans.py:122-128) clipping to the nearest paragraph mark; both spans still pass, because the frozen C2
  leg is `len(span) > len(quote)` (c2-count.py:175, printed `SPAN_CONTEXT=n/n` at :226). The counter cannot see a
  zero-width side; quote-substance-check bounds span length only from above (:56). Recorded C2=PASS is therefore
  consistent with a span that shows no context at all on one side.
- **F2 (finding, the clip discards the most relevant context).** S100-1's own heading `中国知网他引频次查询方法说明`
  sits 2 chars before the committed span start and is dropped; S101-4 loses `14 参考文献(References)` and the
  following `14.2参考文献著录项目`. Hidden context is *supportive* of the entry, not contrary to it, so no reading
  is contradicted — but build-spans.py:17's "80 chars of captured context either side" is false for raw forms
  (7 of 8 raw rows truncated, 2 to zero), and the docstring was not updated with the repair.
- **F3 (finding, section attribution falsified by context).** citation-count-semantics-r37.md:5 says S101 covers
  "sections 11 and 14"; S101-5 (char 34374) sits in **15.7** — context R40 `thod）。\r16 电讯地址…`, L40
  `15.6文章总篇数…` — and the entry itself calls it "a later parameter table", which the context shows is a
  numbered parameter item (15.5/15.6/15.7), not a table. Quote verbatim; location line under-scoped.
- **F4 (finding, minor).** citation-count-semantics-r37.md:7 locates S103 as "section 2.1 and the result-ordering
  note"; S103-4 (char 3105) is in **3.1.1 文献检索** (heading at 3071). Not false (the note is left unlocated), but
  the location is recoverable and omitted.
- **F5 (flagged, benign).** Crossings into unrelated text: S097-2 right → next section heading
  `2. 引用・被引用文献リンク機能` + its lead-in; S098-4 and S098-5 right → next FAQ question
  `引用文献で複数の著者名を<person-group>で記述する際に…どのように記述すればよいですか。` (capture 29790-30100);
  S102-3 right → page 41 then headings `6.5 参考文献` / `6.6 相关文献推荐`; S096-1 left → the previous
  sub-item 被引用文献's definition, entered via the `※` marker. In each case the quote's own sentence is complete
  and the crossing is whitespace-heavy page furniture or a neighbouring item, so nothing is misread. S102-1 and
  S102-2 straddle page breaks (25→26, 28→29) inside the quote's own sentence — continuation, i.e. required context.
- **F7 (caveat).** S100-3's 80-char left window is 35 chars of UTF-16LE binary decode (`J开ň漀Ĩᘚ౨㼑䌀ᡊ…`) + 45
  readable chars; the readable part abuts the quote (`…方式进行组合查询，注：`). The raw form's "80 chars" is not
  80 readable chars.
- **F8 (caveat, thin quotes with real context).** S103-3 `引用量` = 3 non-space chars (exactly MIN_CHARS) and
  S103-2 `来源数据库` = 5; both are field names inside a live enumeration
  (`文献的标题、摘要、作者、出版日期、文献来源、来源数据库、引用量以及下载量`), which supports the entry's
  "fields including" claim. Per-id LONG_CHARS passes only via S103-4 (17).
- **Not found:** no span hides context contradicting its entry; all 28 quotes are verbatim, unique, exact slices, and no raw-form quote is severed by the CR clip.
- Scratch `/dev/shm/chousa-r49-ExecSpanContext` deleted after use; no installs (none needed).

VERDICT: span context for all 28 rows of round-49 spans.tsv — partly — every quote is a true, exact-slice, non-severed quote whose context supports its entry, but 7 raw-form spans have a truncated side (S100-1 pre=0, S101-4 post=0, invisible to c2-count's `len(span)>len(quote)` leg), the CR repair dropped two adjacent headings, and the entry's S101 location line omits section 15.7 where S101-5 actually sits.
