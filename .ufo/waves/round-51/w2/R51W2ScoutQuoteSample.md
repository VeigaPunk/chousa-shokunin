# R51W2ScoutQuoteSample — 20-row sample of corpus/evidence/round51/spans.tsv

Attacked: spans.tsv (61 data rows; per id S107 16, S108 11, S109 13, S110 7, S111 6, S112 8; `cut -f1 spans.tsv | sort | uniq -c`).
Tools: none installed. Scratch /dev/shm/chousa-r51-R51W2ScoutQuoteSample/ created and deleted (script reproduced below).
Selection (fixed before reading any lesson text, never opened `corpus/lessons/round-51.md`): by span-file number, S107 {2,6,10,15}, S108 {2,6,10}, S109 {1,5,9,13}, S110 {2,4,7}, S111 {1,3,6}, S112 {2,5,8} = 20 rows.

## Part 1 — location check (20/20 pass)
Form: capture `.txt` read as UTF-8, `key = sha256(url)[:24]`. Per row: `txt.count(quote)==1`, `txt.find(quote)==int(offset)+span.find(quote)` (span = `spans/<file>`), sha256 of the .txt equals the row's capture_sha256.
```
cd corpus/evidence/round51; python3 - <<'E'   # (condensed; the full loop was run over the 20 picks)
for r in rows: key=sha256(r['url'])[:24]; txt=open(QCACHE+key+'.txt',encoding='utf-8').read()
  span=open('spans/'+name).read(); assert txt.count(q)==1 and txt.find(q)==int(r['offset'])+span.find(q)
E
```
Observed (every row `count=1`, `find==exp`, `ok=True`, `txt_sha==rowsha`, span.find(quote)=80 in all 20, i.e. offset is the span start and the quote sits 80 chars in):
| row | key | find (=exp) | words/chars |
|---|---|---|---|
| S107-2 | 7194acc65a18 | 10234 | 1/22 |
| S107-6 | 〃 | 10370 | 1/17 |
| S107-10 | 〃 | 12815 | 1/14 |
| S107-15 | 〃 | 17398 | 1/24 |
| S108-2 | 62be15a474e8 | 1498 | 1/17 |
| S108-6 | 〃 | 4211 | 1/15 |
| S108-10 | 〃 | 36844 | 1/7 |
| S109-1 | fd468a36d78f | 121 | 1/38 |
| S109-5 | 〃 | 15240 | 3/32 |
| S109-9 | 〃 | 23097 | 2/8 |
| S109-13 | 〃 | 24606 | 1/6 |
| S110-2 | c7266931a173 | 1633 | 1/25 |
| S110-4 | 〃 | 11211 | 1/22 |
| S110-7 | 〃 | 11404 | 7/23 |
| S111-1 | 42bac8830527 | 695 | 4/24 |
| S111-3 | 〃 | 934 | 1/12 |
| S111-6 | 〃 | 1366 | 1/10 |
| S112-2 | 34fcefc159bf | 10140 | 1/10 |
| S112-5 | 〃 | 11243 | 1/11 |
| S112-8 | 〃 | 11457 | 1/9 |
All ≤25 words and ≤160 chars. Held: location, uniqueness, offset arithmetic, capture hash. Note the manifest `capture_sha256` is the .txt hash, not the `.raw` hash (raw sha differs, e.g. S107 `9315274a…` vs `05c7ee9f…`) — column naming is accurate only if read as "txt form"; the commands for S107 `.raw` would not match it.

## Part 2 — does the quote support the entry sentence as worded
Entry sentences found with `python3` line scan of the quote in each entry file (entry line numbers below); wider context read from the captures at the stated offsets.
Counts: **supports 16 · weaker than the sentence 4 · unrelated 0.**

Supports (16): S107-2 (r38:12,21,22 — the instruction "who, when, expression recorded together" is `その日時，使用した検索式を同時に記録しておく`; r38:6 recheck char 10234 correct) · S107-10 (r38:13: PRISMA checklist appended; the entry itself limits it to "not about what a search record must carry") · S108-6 (r38:14: ハンドサーチの有無 and 最後に検索した日 present) · S109-1 (r39:13 DOI; quote anchors only the DOI element — 巻期页, 文章编号, section label are other rows) · S109-5 (r39:14,27: table row `3 文献检索策略` (1)(2)(3) at 15000-15500, next row `4 纳排标准`, so "row 3" correct; time range and 检索词 sit in one cell across a line break) · S109-9 (r39:15 boolean operators) · S109-13 (r39:15: 引文检索或手工查阅期刊…并提及使用的文献管理软件及去重方法 — reference manager + dedup confirmed in the same sentence, 去重 count 1) · S110-2 (r39:17 文章编号) · S110-4 and S110-7 (r39:17,25: the search statement at 11211 is inside §3 heading `3 动物实验 SRs/MAs 中应用 GRADE 方法的/文献特征分析` (heading at 10924, 文献特征分析 at 11110), so "§3 records" holds) · S111-1 / S111-3 / S111-6 (r39:18,26,28: bibliographic line, the 16-item abstract sentence "PRISMA-S…为文献检索报告提供了包含16个条目的专项规范", login prompt) · S112-2 (amend:11,19: sentence "…17 項目が含まれている。例えば…検索の特徴（検索期間，言語制限，未発表の資料や抄録を含めるか…）を明記することが求められている" — attribution to PRISMA-P holds) · S112-5 (amend:12: 検索した文献データベース名，Ovid などのプロバ/イダー名，検索の開始日と終了日 — the gutter-split remark is accurate) · S112-8 (amend:12,18: full sentence is "…最新の結果を反映しているかどうか，更新がされているかどうかの評価がしやすくなる", so "currency and whether refreshed since" is supported — I checked this at 11180-11560 because I first suspected over-reading; it holds).

Weaker than the sentence (4), with the narrowing:
1. **S107-15 (r38:27)** "the full name appears **in its reference list** across a line break". Capture 17250-17700 (S107 .txt): the left column reads `…利益となる．日⏎本健康教育学会誌にもシステマティックレビューの投⏎稿・掲載数が増えることを期待する．` — that is the article's closing body sentence (期待する), while the interleaved right-column lines at the same lines are the reference list (`の更新版ガイドライン」の解説と日本語訳．薬理と治療．2021；49：831–842`, `10) PRISMA…`). Narrow to: "the full name 日本健康教育学会誌 appears in the closing body paragraph, split across a line break, so the contiguous run is `本健康教育学会誌にもシステマティックレビューの投`". Also the quote does not bear the rest of the sentence (特別報告; footers 日健教誌 第 32 巻 第 2 号) — `日健教誌` occurs 4 times (748, 9285, 13787, 21177), `特別報告` once, but the string `第 32 巻 第 2 号` occurs 0 times in this form (count run on S107 .txt). Needs its own anchor, or "(2024)" etc.
2. **S107-6 (r38:12)** "The **same sentence** gives the purpose". Context at 10300: `…記録しておくことが望ましい．これにより，研究の透明性を保ち，他者が同様の検索を再現できるようになる．` — `．` closes the instruction; the purpose is the **next** sentence (これにより). Narrow to "the next sentence (これにより) gives the purpose". The quote itself (透明性…再現) is exact.
3. **S108-10 (r38:20)** "the attachment must carry the words and expression `実際に使用した` or `同等の詳細なもの` — the rule is about what was typed, **not a reconstruction of it**". Source (36834): `検索ワードや検索式は実際に使用した、もしくはそれと同等の詳細なものであること。` — the rule expressly admits an equivalent-detail alternative, i.e. what the quote `実際に使用した` supports is "as used", and the clause beside it allows a non-verbatim equivalent. "not a reconstruction" overreads. Narrow to "the expression as used, or an equivalently detailed one". r38:23 words this correctly ("or 同等の詳細なもの, which a reader applies by comparison").
4. **S108-2 (r38:30)** "S108's 更新 **hits** are about an updated review". `更新` occurs 17 times in S108 (python find loop: 1498, 1505, 2092, 2183, 2222, 2251, 2519, 2527, 2537, 2605, 11021, 14314, 14321, 28017, 35668, 36933, 36983); the quote covers one. Two (28017, 35668) are inside the reference title `PRISMA 2020声明：…更新版ガイドライン」の解説と日本語訳`, not an updated-review rule. Narrow to "S108's 更新 hits are 15 about an updated review (更新版/更新元) and 2 in a cited reference title" or cite only the instruction. The `['改訂']` → `[0] [0]` claim holds: 改訂 count 0 in both S107 and S108; 第２版 occurs 3× in S108 (0 in S107).

## Part 3 — extra: entry offsets (outside the 61 rows)
Regex over the three entries (a backticked string followed within 70 chars by `char N`), tested against all six captures: two genuine mismatches, both in `japanese-search-record-r38.md:12`:
- `このプロセスに際して，誰が検索を行ったの` is labelled `(char 13721)`; it actually starts at 13710 (`S107 .txt`, count 1). 13721 = the start of `誰が検索を行ったの` (13710+11).
- `か，その日時，使用した検索式を同時に記録しておく` is labelled `(char 10234)`; it starts at 10232 (count 1). 10234 is where `その日時…` begins (and is the correct value on r38:6 and for row S107-2).
Both are label offsets of an inner substring attached to a longer quote; a reader running `t.find(<backticked string>)` gets 13710 / 10232. The seven S112 offsets in the amendment (10140, 10146, 11229, 11243, 11294, 11348, 11457) all match `find` exactly and each count is 1 (run directly). Other regex hits (rows pairing a quote to a sha or a count list) were pattern artefacts, not claims.

Repair text (intended path `corpus/knowledge/japanese-search-record-r38.md`, line 12): change `(char 13721)` → `(char 13710)` and `(char 10234)` → `(char 10232)` on that line only; line 27: replace "in its reference list" by "in the closing paragraph of the body"; line 12: "The same sentence gives the purpose" → "The next sentence gives the purpose"; line 20: "not a reconstruction of it" → "as used, or an equivalently detailed one"; line 30: "S108's 更新 hits are about" → "S108's 更新 hits are (apart from two in a cited reference title) about".

VERDICT: attacked 20 of 61 spans.tsv rows (all six ids) — 20/20 occur once at offset+span.find and match capture hashes; sentence fit 16 supports, 4 weaker (S107-15 "reference list" is body text; S107-6 "same sentence" is the next; S108-10 "not a reconstruction" contradicts 同等の詳細なもの; S108-2 plural "hits" generalises one of 17), 0 unrelated; plus two entry-line offsets (13721, 10234 in r38:12) are inner-substring labels, 13710/10232 for the written string.
