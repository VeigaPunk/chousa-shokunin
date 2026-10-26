# R52W2CritExpansion — attack on C2 coverage and expansion credit

Seat: R52W2CritExpansion (leaf; no subagents). BASE = `00f8c7f5272a1d98b6d34913985fa4537e00aaf9`.
Attacked: the Gate's credit ledger for S113/S116/S114 as `corpus/lessons/round-52.md` `## Gate` states it
("Expansion credit is per document and is three, not four … the 梅斯医学 record (S113) is a second carrier").
Counter `c2-count.py` passes (BOUND=4/4, NEW_GROUND=3/3, C2=PASS exit 0, run below) — the claim measures binding,
not entailment (claims.md:115-116); this report attacks the credit judgment only.

## Evidence: commands run

```text
$ git -C /home/vgpnk/Projects/shokunin/chousa-shokunin grep -l 'それぞれの情報源が最後に調べられた' BASE -- corpus/
  BASE:corpus/evidence/round51/quotes.tsv          # line 22: S108 quote, exact run
  BASE:corpus/evidence/round51/spans/S108-3.txt S108-4.txt S108-5.txt
  BASE:corpus/knowledge/japanese-search-record-r38.md
  BASE:corpus/lessons/round-51.md
$ git -C ... grep -l '完全な検索戦略' BASE -- corpus/        → (empty)
$ git -C ... grep -l '文献検索期間' BASE -- corpus/knowledge/ → (empty; lessons only)
$ git -C ... grep -l '检索报告清单' BASE -- corpus/knowledge/ → (empty; lessons only)
$ git -C ... grep -l '检索或查询日期\|信息来源\|完整 检索策略\|明确说明每一项来源' BASE -- corpus/ → (empty)
$ git -C ... grep -l '并针对中文' BASE -- corpus/  → round51 quotes.tsv, spans S111-4/5, r39.md, round-51.md
$ git -C ... grep -l '本土化应用挑战提出实践建议\|实践建议' BASE -- corpus/ → (empty)
$ git -C ... grep -l '郑卿勇' BASE -- corpus/      → SOURCES.md, round51/spans/S111-6.txt
$ git -C ... grep -l 'Page MJ\|n71' BASE -- corpus/ → (empty)
```

```text
$ python3 -c "
t=open('$Q/62be15a474e866e4bef6c9d5.txt',encoding='utf-8').read()   # S108 JAOHFA form, 39,676 chars
print('日付を記載する:', [i for i in range(len(t)) if t.startswith('日付を記載する',i)])
print(repr(t[4160:4260])); print('run count:', t.count('それぞれの情報源が最後に調べられた'))
print('完全な検索戦略 in S108:', '完全な検索戦略' in t)"
日付を記載する: [4146, 4285, 31429, 31460]
'          sources］           する。それぞれの情報源が最後に調べられた ・ハンドサーチの有無を記載する。…'
run count: 1
完全な検索戦略 in S108: False
# at char 4124: 'それぞれのデータベース毎に最後に検索した日の日付を記載する。'
# at char 4330: '用いたフィルターや制限も含め'
```

```text
$ python3 -c "
t=open('$Q/e84bfe97808591d23fe3266f.txt',encoding='utf-8').read()    # S116 archived Japanese PRISMA 2020 table, 5,328 chars
print(t.count('それぞれの情報源が最後に調べられた日付を記載する'), t.count('それぞれの情報源が最後に調べられた'))"
1 1
# char 592 = 'それぞれの情報源が最後に調べられた日付を記載する。'; char 641 = '用いたフィルターや制限も含め，'
# char 753 = '試験登録，Web サイトの完全な検索戦略を記載する。'
```

```text
$ python3 corpus/evidence/round52/c2-count.py   # from lane root
ENTRIES=3/3  BOUND=4/4 (min 3) REFUSED=0  BOUND_IDS=S113,S114,S115,S116
NEW_GROUND=3/3  QUOTE_ROWS=38 ON_BOUND=38/38  SUBSTANCE=PASS
INFERENCE_GROUNDED=3/3  QUARANTINE_VERDICTS=1/1 (S120)  C2=PASS   exit=0
$ grep -c 'S108\|jaohfa' corpus/knowledge/japanese-prisma-item-wording-r40.md → 0
```

## S113 — credit vs refusal, argued both ways

**Credit direction (supported):** the abstract's last clause `并针对中文数据库等本土化应用挑战提出实践建议。` occurs 0
times anywhere at BASE (`实践建议` not grep); it fills exactly the truncation gap round 51 recorded (`corpus/knowledge/
chinese-search-record-r39.md:18` "breaks off mid-sentence after `并针对中文` … char 1024"). The clause is a verified,
single-occurrence located quote at char 2433 (SOURCES.md:123; lesson "All located quotes"). The 梅斯医学 byline date
(2026-04-25) and empty `originalUrl=`/`linkOutUrl=` fields (char 2034, 3139) are per-record facts absent at BASE.

**Refuse direction (supported):** the document is a second carrier of the same article already bound as S111 (SinoMed,
r39); r39 already made the record-vs-article observation in the same genre ("carries bibliographic fields and a truncated
abstract, not the item text"; "serves no full text here"). The author `郑卿勇` was already in the lane at BASE
(SOURCES.md:121 row S111; span S111-6 "查看相同作者发表的文献 … 郑卿勇"), so "the author's name appears only inside that
file name" is per-record trivia, not new article-level knowledge. C2 needs only 3 of 4 bound — the row is not needed for
the pass, and the same "second carrier" test was not applied to S116 (below).

**Verdict S113:** no document-level credit (agree with the lesson's "three, not four"), but not refuse outright: the last
clause is genuine new ground and the lesson records that novelty while denying credit, so its decision survives both
directions if "second carrier" bars credit.

## S116 — the item-6 date sentence is the same sentence's source

The exact run `それぞれの情報源が最後に調べられた` was quoted at BASE from S108 (round-51 quotes.tsv line 22; spans
S108-3/4/5; r38.md:14). S108 is the JAOHFA form, explicitly PRISMA 2020-derived (`PRISMA 2020声明 システマティックレビュー記載の
留意点(別紙様式 (V) -4 本文)`, round-51 quotes.tsv line 19). S116's date sentence contains that run verbatim plus
`日付を記載する`; both documents require the same ground (item 6: name each source, give its last-searched date — S108
char 4124/4192 vs S116 char 592), and S108 already carries item 7's filters/limits phrasing `用いたフィルターや制限も含め`
(char 4330 vs S116 char 641). S116 is therefore the *source* of the wording the JAOHFA form carried: second carrier of the
item-6/7 thematic ground, not new ground. The entry's `ground:` line cites only the S112 amendment (three different
fields: database/provider/window) and never S108 (grep count 0), so the overlap is not disclosed.

Genuinely new from S116: the term `完全な検索戦略` (0 hits at BASE anywhere — absent even in S108's capture), the phrase
`試験登録，Web サイトの完全な検索戦略を記載する。` (char 753), items 8/9 reviewer counts, and the carrier facts (one-page
table, no publisher/date/edition line; original URL `rc=28` marker; memento unchanged to 2026-04-18).

**Verdict S116:** partial credit only — first carrier of the term-level wording and structural facts; second carrier of
the item-6/7 ground. The lesson's full credit for S116 while denying S113 for second-carrier status is internally
inconsistent.

## S114 — first carrier; credit stands

No Chinese PRISMA 2020 checklist item wording exists at BASE (`检索或查询日期`, `信息来源`, `完整 检索策略`, `明确说明每一项来源`
all 0 hits), and no English original is held (`Page MJ`, `n71` 0 hits). The closest base holdings are S109's
`至少提供一个主要数据库的完整检索策略` (one main database — a different requirement) and S111 (PRISMA-S reading record, not
the checklist). S114 is new ground on a new carrier; the lesson's admission ("strongest on-theme Chinese field evidence
the base reading lacked") stands.

## Smallest safe correction

Apply the same second-carrier test the Gate used for S113 to S116: mark the item-6/7 thematic ground as held since round
51 (via S108/r38) and credit S116 only for the differential term/carrier facts; state this in the Gate. No frozen
predicate, counter or target changes; C2 still passes (BOUND=4/4 unchanged).

VERDICT: attacked the Gate's per-document expansion credit — S113 no-credit stands (last clause is the only new ground,
author already known at base), S116 is itself a second carrier of the item-6/7 ground the lane held at base via S108
(its item-6 date sentence is the same sentence's source, not new ground; partial credit only), S114 credit stands.
