# R50CritGateDecisions — attack on the round-50 Decisions table

seat: R50CritGateDecisions (critic, w2 falsify), 2026-10-25. Target: `corpus/lessons/round-50.md:119-130`
(`### Decisions`) — four refusals, one deferral, three narrowing admits.
Read-only throughout; no fetch (L0 `8d77e6c1` open); no scratch written (all work in heredocs).
Decode forms: `.txt` read as UTF-8 at the stated offsets; S105/S106/教师 `.txt` are `pdftotext -layout`;
S149/S160/S175 `.txt` are the pages' HTML text form (`.raw` identical bytes).

## Capture keys — `sha256(url)[:24]` of each entry's `source:` URL

```
$ cd /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache && for u in "<source: URL>"; do k=$(printf '%s' "$u" | sha256sum | cut -c1-24); echo "$k  $u"; done
9c3aca545490cdfad8428e40  https://check.oversea.cnki.net/vip/Role/VIPprivacyPolicyV2.0.html          (S175, r46)
625375f640d6eb3be0990ef2  https://chn.oversea.cnki.net/index/gb/gb-manual.html                      (S149, r42)
dd50f086f911d06fa2bbd5f9  https://check.cnki.net/tmlc/                                              (S160, r43)
e3ca8f4fdd15420b80096a75  https://gs.sxu.edu.cn/docs/2025-03/9e5cdd215a414bf6b5694912018de4c8.pdf  (S105; r47's S180, r48's S187)
28750bcdf5d36cd90a7709fb  https://rwxy.seu.edu.cn/_upload/article/58/cc/5a2fdc1940cfa2522e82ba8b5d81/fb75a598-a343-48f2-bb42-5c6c411506bc.pdf  (S106)
275c79d45b1e9b0fd32cef93  https://bs.bnu.edu.cn/docs/20160407183946745914.pdf                    (refused 教师)
001287c436f0e6b1d166ae8d  https://chaxin.las.ac.cn/service/citation-search                         (S104)
```

## r46 `cnki-comparison-basis-r46` — refuse (lesson:129): reason TRUE, one lost observation
```
$ python3 -c "s=open('9c3aca545490cdfad8428e40.txt',encoding='utf-8').read();print(len(s));[print(t,s.count(t)) for t in ('引文核对','匹配','比对')]"
28114 / 引文核对 0 / 匹配 0 / 比对 25
```
Paragraph split on blank lines: 比对 counts per paragraph `[1,3,1,4,1,5,5,1,3,1]` — **no scope yields ten**; the
查重检测服务 paragraph carries 3. The character half is form-dependent, not invented: tag-stripped readings give
18,922 raw / 13,304 line-stripped / 13,868 whitespace-collapsed, so 13,527 is a visible-text-order figure, while the
declared `.txt` form is 28,114. `比对 25` is form-independent, so the falsifier stands; w1's "no reading yields
13,527" (`w1/DraftGateTable.md:33`) overstates it.
Closing inference falsified by §6.1, as the row says: `引文核对是指，以“中国知网”的文献资源为核对源内容` (char 30738)
and `参考文献复制到“引文核对”文本框，点击“搜索”按钮，` (char 30800). Loss: the policy observation (seven comparison
libraries, `引文核对` 0 on that surface) is absent from the lane (`grep -rn '优先出版文献库\|比对截止日期'
corpus/knowledge` → no match), but it is about the detection product, not the citation-check feature — out of the
frozen theme. **Verdict: agree with the reason.**

## r47 `cnki-citation-check-query-r47` — refuse (lesson:126): reason TRUE, flip vacuous
```
$ git grep -c '引文核对' 3c51da77b3696ed884c943548ec4b4006e3ca528 -- corpus/knowledge ; echo exit=$?
exit=1        (no output: the lane corpus never held the term, so it never made the round-12 claim)
```
Mis-citation reproduces, twice, against the staged registry as delivered: `SOURCES.append.md:95` S170 = 药品临床
综合评价项目真实世界研究质量控制规范, but r47:13 calls S170 "CNKI's own privacy policy for the detection system";
`SOURCES.append.md:44` S119 = a SinoMed PRISMA-S record, but r47:18 calls S119 "the document the corpus has held
since round 5". Substance is carried by the admits: char 30800 (r40:11) and char 30793 (r41:12).
Stronger reason the row lacks: the entry's remaining observation is live-fetch (人事论文评审服务平台 manual, HTTP 200,
1,439,404 bytes), un-re-testable under L0 `8d77e6c1` — the same ground on which r40:30 dropped the `library.hntky.com`
bullet. **Defect (small):** the flip "a round whose question needs the query-formation sentence as its own entry" can
never fire — that sentence is already adopted at r40 char 30800 and r41 char 30793. Smallest correction: flip =
"the manual's §6.1 changes", as in the r40 row. **Verdict: agree with refusal, disagree with the flip.**

## r48 `citation-check-status-vocabulary-r48` — refuse (lesson:127): reason TRUE, not the strongest; one lesson lost
`橙色` 1 / `琥珀` 0 in S105 → "orange is right" holds. The four result-list columns are in r40:12
(`容有状态、篇名、作者和文献来源。`, char 30878) and the 篇名 link at char 31233, so the residue is folded as claimed.
Stronger reasons the row lacks: (a) r48's headline "the residual is also published" contradicts the adopted r41's
narrowed negative — `no matching method is stated anywhere in it`
(`corpus/knowledge/citation-matching-semantics-r41.md:22`) — so admitting both would land two entries in contradiction
on one document; (b) r48:49 repeats the S119 mis-pointer
(staged S119 = SinoMed record). Loss: r48's method lesson ("a search for a feature's name stops at the naming
paragraph; the behaviour is described after it") appears in neither `corpus/lessons/round-50.md` (`grep -n
'naming sentence\|naming paragraph\|S119\|round 5'` → no match) nor QUALITY 73–79. **Verdict: agree with refusal;
disagree that the stated reason is the strongest; the lesson is the one real loss.**

## r42 `cnki-matching-modes-r42` — refuse (lesson:128): reason TRUE but insufficient; the entry is also over-broad
Its own text says it: title "…they govern the search platform, not the 引文核对 feature"; Inference repeats it. The
"not re-grounded" half is stale — I re-grounded it in one pass: `匹配方式` 7×, `引文核对` 0×, and the three field
assignments reproduce verbatim (`相关度匹配…主题、篇名、全文、摘要、参考文献、文献来源` at 17618; `精确匹配…关键词、
作者、第一作者、通讯作者`; `模糊匹配…作者单位、基金、分类号`).
Stronger reason, found now: the same capture carries a **second** `匹配方式` section (h3 at 23030) reading
`除主题只提供相关度匹配外，其他检索项均提供精确、模糊两种匹配方式` (char 23067), with
`篇名、摘要、全文、参考文献的精确匹配，是指检索词作为一个整体` (char 23128) and
`模糊匹配，则是检索词进行分词后在该检索项的匹配结果` (char 23179). That falsifies r42's unqualified Inference
"the `参考文献` field in particular is a relevance-ranked field rather than an exact one" — the same document gives
that field exact and fuzzy modes too, and r42 never mentions the second section. Its Inference also asserts "the
manual publishes no query-formation rule for it", false against S105 char 30793/30800.
**Verdict: agree with refusal; the reason given is weaker than available — refuse for scope *and* for the over-broad
per-field assignment.**

## r43 `cnki-public-surface-r43` — admit-later (lesson:130): disposition right, stated reason stale
Reason "S160 not re-grounded" is not reproducible as written: w1 itself measured the capture
(`w1/DraftGateTable.md:32`: 1,115 chars, 全文比对数据库 1×, 引文核对 0×), and I re-grounded both sentences —
```
chars 1115 · 本系统以《中国学术文献网络出版总库》为全文比对数据库 (char 211) · 本系统限本单位内部使用 (char 283)
引文核对 0 · 匹配 0
```
Stronger reasons: (a) the entry's second surface has no capture at all — over 2,549 `.txt` captures,
`grep -l '诚信档案'` matches only S106 and there as the manual's chapter-8 title, and
`grep -l '科研人事论文诚信档案系统\|科研·人事论文诚信档案系统'` → 0, so "the sibling portal answers the same way"
cannot be re-grounded this round; (b) a fourth entry would sit outside both frozen counters
(`corpus/evidence/round50/c2-count.py:59` `ENTRIES` = the three; :220 loops only `ENTRIES`), i.e. an unmeasured
adoption in a round whose admission rule is "only if its frozen counter meets the target". A narrowed admit (tmlc
only, sibling sentence dropped) was formally available; the freeze makes it unmeasured, so deferral is right for a
reason the row does not give. **Verdict: agree with disposition, disagree with the stated reason.**

## Narrowing admits
| entry | check | result |
|---|---|---|
| r40 (lesson:123) | `橙色` 1 / `琥珀` 0; `诚信档案` 0 in S105; `状态共分为三种类型` 0 vs `态共分为三种类型` 1 | agrees. The staged recheck string was itself un-runnable; the narrowing fixed it. Caveat, not a defect: `诚信档案` is 0 in S105 only — S106 carries the term once (`grep -c 诚信档案` → 1), in its chapter-8 title; the row says "in the capture", so it is accurate but single-document. |
| r41 (lesson:124) | `匹配` 0 in 38,174; slice 30727–31262 = 535 chars, `[排序,权重,相似度,算法,匹配,字段,复制比,去除本人]` = `[0,0,0,0,0,0,0,0]`; 教师 capture `引文核对` 0/`核对` 0/`匹配` 0/`引文` 9, all inside `标明引文` | agrees. Load-bearing nuance: `相似度` is 3× capture-wide (offsets 18007, 18772, 25567 — 跨语言检测 and 表格检测 report prose), so the slice scoping is what makes the negative true; the row states the slice and is correct. The amber→undocumented narrowing is right: absence of a description cannot establish absence of a step. |
| r39 (lesson:125) | `2.针对中国科学院用户` char 684; `可免去` 1; `自引` 1 / `他引` 1 (the price line only, char 549); `中国科学院` 5 / `中国科学技术信息研究所` 0 / `文献情报中心` 3 | narrowing agrees, **but a naming defect**: the entry anonymizes its publisher ("A Chinese national institute's…") although the capture names `中国科学院文献情报中心` 3× and `corpus/SOURCES.md:114` names it; and the Gate prose "the path says istic" is false for the URL (no `istic` in it; capture `ISTIC`/`istic` 0×). The only `istic` in play is the lane **filename**, inherited from staged `istic-citation-verification-r39.md`. Renaming is blocked by the freeze (`c2-count.py:58` hardcodes the path). Smallest safe correction: one disclosure line in the entry naming the publisher and the filename inheritance, plus a lesson Mistakes row (naming/provenance); rename on the flip. |

## Summary
| decision | reason TRUE? | stronger reason exists? | supportable claim lost? | verdict |
|---|---|---|---|---|
| r46 refuse | yes (比对 25; §6.1) | yes — names no counting command, out of theme | yes, the policy observation (out of theme) | agree |
| r47 refuse | yes (base grep exit 1; S170/S119) | yes — live-fetch residue; flip vacuous | no | agree; flip wrong |
| r48 refuse | yes (橙色 1; columns in r40) | yes — contradicts r41's negative; S119 | the method lesson (unrecorded) | agree; one loss |
| r42 refuse | yes (its own text) | yes — second 匹配方式 section falsifies its inference | no in-theme claim | agree; reason insufficient |
| r43 defer | imprecise, not false (stale) | yes — no sibling capture; counters exclude a 4th entry | no (deferral) | agree on disposition, disagree on reason |
| r40/r41 admits | yes | — | — | agree |
| r39 admit | yes | — | publisher name dropped | agree; naming defect |

VERDICT: attacked the six Decisions rows and the three narrowing admits against seven captures — all five dispositions
survive (r46's tally does not reproduce under any scoping; r42's per-field assignment is over-broad; r47's and r48's ids
mis-point at other documents), but **defect found**: r43's stated reason is stale (S160 re-grounds in one command) where
the durable reasons are the missing sibling capture and the counters' three-entry scope, r47's flip cannot fire, r48's
lost method lesson is unrecorded, and r39's entry drops a grounded publisher name while the lesson calls the URL path
"istic" (it is not).
