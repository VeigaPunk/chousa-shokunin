# R51GroundJaohfaA — re-ground staged S110 (JAOHFA 別紙様式 (V)-4 items 6–7 and (V)-5)

seat `R51GroundJaohfaA` (chousa r51 w1, leaf). Staged id **S110**, url `https://jaohfa.com/pdf/systematic_review.pdf`, staged entry `knowledge/corpus/knowledge/japanese-search-record-r38.md` (read-only). Planned lane row **S108**; entry path used in the machine lines `corpus/knowledge/japanese-search-record-r38.md` — that lane file does **not** exist at the tip (`ls` → `No such file or directory`), so the path is the intended one, not an existing one.

## Capture identity and the form used

```
$ python3 -c "import hashlib;print(hashlib.sha256(b'https://jaohfa.com/pdf/systematic_review.pdf').hexdigest()[:24])"
62be15a474e866e4bef6c9d5
$ python3  # sizes/digests of the two cache members
txt 61188 bytes sha256 960da5cf632dbd278ea941c54d83e3ed8f13657bcb4bcbbfc8d63c9d834acf4a chars=39676 lines=623
raw 291615 bytes sha256 b4ff9d41fde4432260d4adea247a86efe911a61dd1f63034b31dc8b229270be6 head=b'%PDF-1.6\r%\xe2\xe3\xcf\xd3'
$ pdfinfo 62be15a474e866e4bef6c9d5.raw | head -2
Title:           systematic_review.pdf
Creator:         Excel 用 Acrobat PDFMaker 26
```

**Form used: the `.txt` read as UTF-8 — 39 676 characters.** The `.raw` is the original PDF bytes (identical to the `.pdf`); the quoted strings sit in compressed content streams and return **0 byte hits** in the `.raw` (`それぞれのデータベース毎に`, `検索者、検索ワード、検索式`, `第２版` → 0 each), so the `.txt` is the only form where these spans are locatable. Every offset below is `str.find` on that form; every quote asserted `count == 1`, `len <= 160`, `len(split()) <= 25`.

## Located quotes — what each supports, what it does not

Layout note that governs every quote: `pdftotext -layout` renders this form as two interleaved columns, so the left-hand PRISMA text and the right-hand 留意点 text are spliced through each other. The **item-6 left-column sentence is not recoverable as a contiguous string at all** — `t.count('全てのデータベース、研究登録、Web サイト、組織、文献リスト、研究を特定するために')` is 0 verbatim *and* 0 after `re.sub(r"\s+"," ",t)`; offset 4192 shows why: `それぞれの情報源が最後に調べられた ・ハンドサーチの有無を記載する。…`. Only short single-column spans are locatable, and those are what I quote.

1. **`全てのデータベース、研究登録、Web サイ`** — off **3966**. Supports: the enumeration head of the 情報源 requirement, *all* databases, study registries, Web sites (全ての). Does **not** support: organisations or reference lists (next rendered line), that the list is exhaustive, or any verb requiring them to be listed (that verb is in the right column).
2. **`ト、組織、文献リスト、研究を特定するために`** — off **4022**. Supports: the enumeration tail — organisations (組織), reference lists (文献リスト), purpose = identifying studies. Does **not** support: databases/registries/Web sites, nor "any other route": the capture's broader clause is `調べたり、助言を求めたりした情報源` (sources consulted or from which advice was sought), itself line-interleaved and not quotable as one span.
3. **`・検索したデータベース等の情報を全て記載する。`** — off **4044**. Supports: the operative requirement, all consulted databases must be listed. Does **not** support: the 5-way enumeration (left column), nor any date.
4. **`・それぞれのデータベース毎に最後に検索した日の日付を記載する。`** — off **4123**. Supports **exactly** the staged "date of the last search **for each database**". Does **not** support: a date for non-database sources — the left column widens it to `それぞれの情報源が最後に調べられた日付` (each information source, off 4192, line-split); nor a search *period* (`期間` occurs only at 16674/23921/33145, all 摂取期間; `検索日` → 0 hits).
5. **`・ハンドサーチの有無を記載する。ハンドサーチを実施した場合はその方法を記載する。`** — off **4210**. Supports **exactly** the staged hand-search claim (presence/absence, method if performed). Does **not** support: who records it, nor what a hand search must report — a second, separate rule asks for its results (quote 6).
6. **`・ハンドサーチを実施している場合は、その結果を記載する。`** — off **15058**. Supports: an additional hand-search duty (report the results), in a different table row. Does **not** support the staged entry — it never mentions this rule.
7. **`・検索者、検索ワード、検索式は別紙様式 (V) -5に示したことを記載する。`** — off **4408** (item 7, 検索戦略［Search strategy］). Supports: the three fields are shown on the separate form (V)-5. Does **not** support: that (V)-5 *names* them as a heading, that they are its only content, or any binding of searcher to expression.
8. **`・別紙様式 (V) -4 (#7) に合わせた記載とする。`** — off **36746**. Supports: the (V)-5 item-2 row is tied back to (V)-4 #7 (the search strategy). Does **not** support: that the row is a heading, nor which fields it carries.
9. **`・検索ワードや検索式は実際に使用した、もしくはそれと同等の詳細なものであること。`** — off **36833**. Supports the staged "the ones actually used, **or an equivalent detail**". Does **not** support the entry's Inference "the attachment must hold what was typed, **not a reconstruction of it**" — the capture expressly admits 同等の詳細.
10. **`研究を特定するために用いた情報源 (例：`** — off **31026** (抄録 checklist item 4). Supports: an abstract-level 情報源 requirement exists, example = databases and trial registries. Does **not** support: that the example is closed (`例`), nor per-database dates.
11. **`・最後に検索した日の日付を記載する。`** — off **31450** (抄録 item 4 留意点). Supports: a last-search-date duty at abstract level. Does **not** support: "per database" (quote 4 only).
12. **`機能性表示食品制度の届出資料におけるPRISMA 2020声明 システマティックレビュー記載の留意点(別紙様式 (V) -4 本文)`** — off **809**. Supports: the document's identity and domain (届出資料 for 機能性表示食品), and that the quoted table is the (V)-4 本文 part. Does **not** support the edition line: `2026年6月5日 第２版` occurs **3×** (152, 28260, 35891 — one per part), so it fails the exactly-once rule; `作成：一般社団法人 健康食品産業協議会` likewise 3× (298, 28394, 36016), with 協力 listing **three** bodies on the header lines (日本健康・栄養食品協会, 日本抗加齢協会, 日本通信販売協会) — so "author with three cooperating bodies" **is** carried, at char 298 ff.
13. **`・検索者は、原則、#8に記載する。ただし＃7にも記載してあったとしても差し支えない。`** — off **5719** (item 8, 選択プロセス［Selection process］). Supports: a placement rule for the searcher (#8 by principle, #7 tolerated). Does **not** support the staged account — it places the searcher only on (V)-5.

## Machine lines

```
QUOTE	S110	https://jaohfa.com/pdf/systematic_review.pdf	全てのデータベース、研究登録、Web サイ	corpus/knowledge/japanese-search-record-r38.md
QUOTE	S110	https://jaohfa.com/pdf/systematic_review.pdf	ト、組織、文献リスト、研究を特定するために	corpus/knowledge/japanese-search-record-r38.md
QUOTE	S110	https://jaohfa.com/pdf/systematic_review.pdf	・検索したデータベース等の情報を全て記載する。	corpus/knowledge/japanese-search-record-r38.md
QUOTE	S110	https://jaohfa.com/pdf/systematic_review.pdf	・それぞれのデータベース毎に最後に検索した日の日付を記載する。	corpus/knowledge/japanese-search-record-r38.md
QUOTE	S110	https://jaohfa.com/pdf/systematic_review.pdf	・ハンドサーチの有無を記載する。ハンドサーチを実施した場合はその方法を記載する。	corpus/knowledge/japanese-search-record-r38.md
QUOTE	S110	https://jaohfa.com/pdf/systematic_review.pdf	・ハンドサーチを実施している場合は、その結果を記載する。	corpus/knowledge/japanese-search-record-r38.md
QUOTE	S110	https://jaohfa.com/pdf/systematic_review.pdf	・検索者、検索ワード、検索式は別紙様式 (V) -5に示したことを記載する。	corpus/knowledge/japanese-search-record-r38.md
QUOTE	S110	https://jaohfa.com/pdf/systematic_review.pdf	・別紙様式 (V) -4 (#7) に合わせた記載とする。	corpus/knowledge/japanese-search-record-r38.md
QUOTE	S110	https://jaohfa.com/pdf/systematic_review.pdf	・検索ワードや検索式は実際に使用した、もしくはそれと同等の詳細なものであること。	corpus/knowledge/japanese-search-record-r38.md
QUOTE	S110	https://jaohfa.com/pdf/systematic_review.pdf	研究を特定するために用いた情報源 (例：	corpus/knowledge/japanese-search-record-r38.md
QUOTE	S110	https://jaohfa.com/pdf/systematic_review.pdf	・最後に検索した日の日付を記載する。	corpus/knowledge/japanese-search-record-r38.md
QUOTE	S110	https://jaohfa.com/pdf/systematic_review.pdf	機能性表示食品制度の届出資料におけるPRISMA 2020声明 システマティックレビュー記載の留意点(別紙様式 (V) -4 本文)	corpus/knowledge/japanese-search-record-r38.md
QUOTE	S110	https://jaohfa.com/pdf/systematic_review.pdf	・検索者は、原則、#8に記載する。ただし＃7にも記載してあったとしても差し支えない。	corpus/knowledge/japanese-search-record-r38.md
```

## Staged claims about this document that the capture does not carry

The four named checks **are** carried: the 情報源 enumeration (quotes 1–3), the per-database last-search date (4), the hand-search statement (5), the (V)-5 attachment naming searcher/words/expression (7, 8, 9). Not carried:

- **(a) `Inference` "the attachment must hold what was typed, not a reconstruction of it."** The capture's clause is `実際に使用した、もしくはそれと同等の詳細なもの` (quote 9): an equivalent-detail substitute is explicitly allowed. The entry's "as actually run … from the *operator's* side" is stronger than the document.
- **(b) `Inference` "they bind the searcher to the expression."** Nothing binds them: (V)-5 row 2 groups 検索者、検索ワード、検索式 in one 項目 cell (rendered at 36710, 36795, 36840 — three lines, not one string) and cross-refers to (V)-4 #7 (quote 8); no identity-of-searcher-to-expression rule appears.
- **(c) `Observation` "The form is a revision, and says so."** The capture says `第２版` three times; it nowhere states what was revised, what the previous edition was, or that it supersedes one. "Second edition" is carried; "revision" as content is not.
- **(d) `recheck` line "the (V)-5 heading 検索者、検索ワード、検索式".** Not a heading: those are the 項目 cell of **row 2** of the (V)-5 留意点 table (row 1 is タイトル, `・抄録、本文と同じタイトルとする。` at 36643 ff.), split over three lines. `別紙様式 (V)-5` without the space occurs **0×** — the capture always writes `別紙様式 (V) -5` (5×), so a quote copied from the entry's own spelling would fail a byte-exact lint.
- **(e) `Unknown` "Hand-searching is the one imperfection the form does cover."** The "one" is stated nowhere, and the form carries a second hand-search rule (quote 6, results) in another row that the Observation omits; the searcher-placement rule (quote 13) is omitted too.
- **(f) Whole-part omission (not a false claim):** the 抄録 part's item 4 requires 情報源 + last search date (quotes 10, 11) and *recommends* recording who ran the search — `・誰が検索を実施したかを記載することが望` at off **31182** (continues `ましい。` on a later rendered line, so the full clause is not one span). The entry restricts itself to (V)-4 本文 6–7 and (V)-5 and never mentions the abstract-level requirement.

## Calibration note — the absent-defect register row on this URL

`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md:48` (register id `S105`, url = this URL) quotes `情報源［Informationsources］6 全てのデータベース、研究登録、Webサイト、組織、文献リスト、研究を特定するために` (66 chars). In the `.txt` form that is **0×** verbatim and **0×** under NFKC + `\s+` collapse; `Webサイト` is 0× (capture renders `Web サイ` + newline + `ト、組織`), and its second quote `and not, as a search engine's rendering of the same form has it,` is 0× (the searcher's own note, not PDF text). Cause is the two-column interleave shown at offset 4192, not invention — so round-43's refinement to `misquote` is right and `fabricated` would be wrong; but the row cannot be repaired by whitespace collapse and must be re-quoted from single-column spans (quotes 1–3). This bears on C2's "no bound document whose verdict is `fabricated` or `unverifiable`" leg.

## Provenance / limits

No network, no fetch: only the two `.qcache` members and lane files were opened. The `.txt` is a layout rendering, so a claim about *which column* a string sits in rests on the offsets above, not on a coordinate-aware extraction (not run). I ran no lane counter, made no product edit, wrote only this file, installed nothing (none needed), and used no scratch directory.

VERDICT: attacked the staged S110 claims for the JAOHFA form against the 39 676-char `.txt` of capture `62be15a474e866e4bef6c9d5` — the four named requirements (情報源 enumeration, per-database last-search date, hand-search statement, (V)-5 searcher/words/expression) are carried by 13 located single-occurrence quotes, while five staged statements are not carried (typed-not-reconstructed, searcher bound to expression, "revision" content, a (V)-5 *heading*, "the one" imperfection) and the abstract-level item 4 and the searcher-placement rule are omitted.
