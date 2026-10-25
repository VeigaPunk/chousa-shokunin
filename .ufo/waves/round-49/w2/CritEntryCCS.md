# CritEntryCCS — round 49 wave 2 (FALSIFY): `citation-count-semantics-r37.md` claim by claim

Item attacked: every Observation/Inference/Unknown claim of
`corpus/knowledge/citation-count-semantics-r37.md` against its four captures
(S100 `b539a80218080da56a75b624.raw` OLE as UTF-16LE, S101 `6dc68fd6b32ce9c8dfcebce8.raw` OLE as
UTF-16LE, S102 `7809d5114330a60527436b07.txt`, S103 `02aefcf570a7108e699d0990.txt`) plus S096
`09fc63de41f293d43d631c46.txt`. Entry bytes: `sha256 19c27ccb62276b0814db82ba2ee2fe0ee6e349c4cfb58568434e40dd8bd69d4f`,
landed `1254ab2`, unchanged at tip `87e9335` (`git log --oneline -1 -- <entry>` = `1254ab2`; `git status` clean for it).
No frozen predicate, target or counter was touched. Scratch `/dev/shm/chousa-r49-CritEntryCCS`, deleted at end.

## Commands run (with observed output)

1. Decode, both OLE captures:
   `raw.decode('utf-16le', errors='replace')` → `b539a80218080da56a75b624 801280 bytes -> 400543 chars`;
   `6dc68fd6b32ce9c8dfcebce8 129024 bytes -> 64512 chars`.
2. Quote-by-quote membership: every `"…"`/`` `…` `` fragment in the entry, whitespace-stripped, tested against the
   four captures. **16/16 source quotes OK, 0 misses** (5 S100/S101 groups, S102 ×3, S103 ×2, plus the S101 fragments
   `为便于文献的统计和期刊评价`, `文献类型及载体类型标志`, `GB/T 7714`, `参考文献格式，参照ISO 690`). The one
   non-matching quote is the CiNii one, verified separately: `s096.find('CiNii Researchの「参考文献」は、…') = 3599`.
   No fabricated quotation exists in this entry.
3. Registry anchor offsets vs actual quote starts: **15/15 are exact** —
   S100 `1296/1431/2861` OK; S101 `11170/11205/11993/12161/34374` OK (document order: 11170=`为便于…`, 11205=`每一篇…`,
   11993=`本规范推荐…`, 12161=`文献类型及载体类型标志`, 34374=15.7 row); S102 `13260/13514/16123` OK;
   S103 `892/953/959/3175` OK. (I first paired S101 quotes in the entry's order and saw a permutation; the registry
   cell is in document order, so this is a false alarm — no anchor defect.)
4. Disputed-sentence reads: S101 `11993` (14.1), `13249` (14.4), `34383` (15.7); S100 `2861` with its lead-in
   `…方式进行组合查询，注：被引频次为0的文献将不会显示。高级检索按钮如图4中的红框所示…`; S102 `13260` vs `13514`
   (gap `+254` chars, page markers between); S103 `892/953/959/3175`.
5. Download coverage in S102: `re.finditer('下载')` → **only 2 hits, `13271` and `13515`**.

## Overclaims found (entry sentence → capture evidence → smallest narrowing)

1. **`entry:31` — the S102 gloss is spliced across two lines.** Entry: *"The KNS8.0 guide glosses the result-list
   columns `「发表时间」「被引」「下载」` as `「下载」はそれぞれ文献の公開時期、被引用回数、ダウンロード回数を示します。`"*.
   The two quoted strings are 254 chars apart and from different lines: `13260` is the 5.6.1 column enumeration
   (`検索結果には、「篇名」「作者」「刊名」「发表时间」「被引」「下载」の他…`); `13514` is the page-28 gloss, whose
   subject as captured is `「下载」` alone, the subject having been split by a line break (`spans/S102-2.txt` shows
   `「发表时间」「被引」\n         「下载」はそれぞれ…`). The intended sentence is certainly the three columns
   (`それぞれ` + three values in column order), but the entry states a gloss relation that its own quoted fragment does
   not literally carry. **Narrowing:** quote the line as captured with the break and mark it —
   *"the gloss line, split after 「被引」: `「发表时间」「被引」` / `「下载」はそれぞれ文献の公開時期、被引用回数、
   ダウンロード回数を示します。` — i.e. the three columns in that order"*.
2. **`entry:47` — "inbound number" mislabels CiNii's outbound count.** Entry: *"Two indexes give two different reasons
   why an inbound number is not the paper's own number"*. The CNKI half is inbound (`他引频次`, S100 `1296/1431`); the
   CiNii half is not: S096 `3599`–`3707` says the paper's *reference list* shows only `同定・統合された参考文献` and
   `参考文献数も、論文での掲載数ではなく同定・統合された分をカウントしています` — references the paper makes, not
   citations it receives. **Narrowing:** either *"a number the index displays is not the paper's own number"*, or use
   the inbound statement that is in the same capture: `3831` `CiNii Articlesの「参考文献」「被引用文献」の結果とも
   必ずしも一致していません`. (Sibling `aggregator-vs-source-r36.md:48` uses the same quote for reference lists — the
   citation entry is the inconsistent one.)
3. **`entry:28` — "recommends, rather than defers to" ignores 14.4.** Entry: *"(it recommends, rather than defers to,
   the GB/T 7714 formats; a later parameter table reads `参考文献格式，参照ISO 690`)"*. S101 `11993` (14.1) indeed says
   `本规范推荐采用GB/T 7714中规定的顺序编码制格式著录,也可采用GB/T 7714中规定的作者-出版年制。`, and `34383` (15.7)
   says `参照ISO 690`. But the spec also refers to ISO 690 **inside its own format section**: `13249` (14.4)
   `参照ISO 690及ISO 690-2，每一参考文献条目的末尾均以“.”结束。`. So the spec neither defers wholesale to GB/T 7714 nor
   is self-contained: it names two external standards, one in 14.1, one in 14.4/15.7. **Narrowing:** *"it recommends the
   GB/T 7714 顺序编码制 or 作者-出版年制 (14.1) while prescribing its own 编排格式 (14.4) that itself refers to ISO 690
   and ISO 690-2, and codes 参考文献格式 as 参照ISO 690 (15.7) — two external standards, not one"*.
4. **`entry:50` — the zero-row rule is per-product, not "an index query".** Entry: *"A displayed zero, or a missing row,
   in an index query is a display-conditioned result"*. S100 `2861` is scoped: it is a `注` inside the **高级检索** step of
   `中国引文数据库` (`…“学科”、“篇名”、“作者”、“单位”、“出版时间”、“文献来源”等方式进行组合查询，注：被引频次为0的
   文献将不会显示。高级检索按钮如图4…`). The entry's own S102 evidence describes a different product where the column
   exists (`被引` at `13267`) and says nothing about hiding zeros. **Narrowing:** *"in 中国引文数据库's 高级检索, records
   with 被引频次 0 are not displayed (S100); the KNS result list instead exposes a 被引 column (S102 5.6.1) whose zero
   display S102 does not describe — read the display condition from that product's guide"*.
5. **`entry:58` — "a download count carries no claim of dependence" rests on silence.** S102 mentions `下载` exactly
   twice (`13271` column list, `13515` gloss = `ダウンロード回数`) and states no relation to citations. The claim is
   sound as a caution but is asserted beside a sourced gloss as if sourced. **Narrowing:** *"S102 assigns 下载 only
   `ダウンロード回数` and states no relation to citations, so on this third-party copy a download figure supports no
   dependence claim"*.
6. **`entry:19` — the self-citation gloss drops the source's precondition.** Entry: *"a citation in which any co-author
   appears is counted as a self-citation"*. S100 `1431`: `对于合作发文的参考文献中，如果引文出现了任一合作者，那么这条
   引文将被认定为自引。` — the rule is stated **for co-authored works** (`合作发文的参考文献`), and the trigger is any one
   collaborator of the cited work appearing in the citing reference. The entry's `any co-author` leaves both the
   precondition and whose collaborator ambiguous. **Narrowing:** *"for a co-authored work, a reference in which any one of
   its collaborators appears is counted as a self-citation"*.

## Claims that hold

- **Every quoted string is verbatim** in its capture (test 2); S102's `当該文献を中心に年毎の参考、被引用の関係を
  ビジュアルに提示` at `16123` and S103's `CNKI AI 根据相关文献，生成可信增强回答。` at `892` with `来源数据库`
  (`953`) beside `引用量` (`959`) are exact; S103 `引用量` occurs once in the capture and is never defined, which the
  entry correctly does not gloss.
- **The Unknown erratum is exactly right**: `14.1` carries GB/T 7714 (`11993`), the parameter table carries ISO 690
  (`34383`), and the staged reading that put GB/T 7714 in the parameter sentence is absent as written. It is, however,
  incomplete: ISO 690 is also in 14.4 (`13249`), not only "a later parameter table".
- **No false provenance in the adoption note**: the lane's GNU sed row is `S076` (`corpus/SOURCES.md:86`) and S096 is the
  CiNii row (`corpus/SOURCES.md:106`), so "re-pointed by document" is checkable and true.
- **No kengaku-owned metric claim**: the only 评价 token is S101's own purpose clause `为便于文献的统计和期刊评价`
  (`11170`), quoted as the spec's stated purpose; the entry makes no claim about journal evaluation, impact factors or
  ranking, and leaves 15.6's `载文量` (`34329`) unused. Nothing here belongs to the evaluation lane.
- **Source-line precision is short, not wrong**: `entry:5` says "sections 11 and 14" while the entry also quotes 15.7
  (`34374`); `entry:7` says "section 2.1 and the result-ordering note" while the ordering note is 3.1.1 文献检索
  (`3175`). Smallest fix: name 15.7 and 3.1.1.

## Unknown gap (not an overclaim, but the entry should carry it)

S100 never states the arithmetic — that `他引频次` is `被引` minus self-citations under this rule. The entry relies on the
rule "beside each count" without claiming the subtraction, so it is not an overclaim, but a lane record keyed on the rule
should list *"whether 他引频次 is computed as 被引 − 自引, and at what level (record vs citation)"* as Unknown.

## Strongest counterexample

`entry:31` + `entry:50` together: both are display-conditioned provenance claims whose quoted support is a different
line than the sentence asserts (S102's subject split 254 chars earlier; S100's note scoped to one database's advanced
search). Neither is fatal — the reconstructions are almost certainly correct — but both are stated as quotation when they
are reconstruction, and both are fixed by quoting the break and naming the product.

VERDICT: citation-count-semantics-r37 claim by claim — partly — all 16 quoted strings are verbatim, all 15 anchors are exact and the Unknown self-critique is correct, but six glosses overreach their captures (the S102 gloss splices two lines 254 chars apart, "inbound" mislabels CiNii's outbound reference count, "recommends rather than defers" omits 14.4's `参照ISO 690及ISO 690-2`, the zero-row rule is scoped to 中国引文数据库's 高级检索, "download carries no claim of dependence" rests on S102's silence, and the self-citation gloss drops `合作发文`), each fixable by the narrowings above without touching the frozen predicate.
