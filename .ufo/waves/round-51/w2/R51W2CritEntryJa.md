# R51W2CritEntryJa — attack on `corpus/knowledge/japanese-search-record-r38.md` (S107, S108)

Frozen claims `corpus/evidence/round51/claims.md` + erratum E1–E4 are not questioned; no predicate, target, counter or control is proposed for change. Bytes reviewed are the landed ones: `git show HEAD:corpus/knowledge/japanese-search-record-r38.md | sha256sum` = `870ca1a9…bba24` = the working file, `…/corpus/SOURCES.md` = `6cfb1a21…ea3eb2` = the working file, and `git diff --stat 4436e279… HEAD -- corpus/knowledge corpus/SOURCES.md corpus/evidence/round51` printed nothing (HEAD `72566c8`). Scratch `/dev/shm/chousa-r51-R51W2CritEntryJa/` deleted after use.

## Commands (observed output)

```
$ env -u ASSIMILATE_CITES python3 tools/inference-ground.py --entry corpus/knowledge/japanese-search-record-r38.md \
    --spans corpus/evidence/round51/spans.tsv --counts /dev/null --registry corpus/SOURCES.md --root .
GROUND entry=corpus/knowledge/japanese-search-record-r38.md section=1 bullets=4 tokens=10 grounded=10
GROUND: PASS
$ env -u ASSIMILATE_CITES python3 corpus/evidence/round51/c2-count.py | tail -4
INFERENCE_GROUNDED=3/3
QUARANTINE_VERDICTS=6/6 (S104,S105,S111,S112,S114,S120)
QUARANTINE_BLOCKED_ADOPTED=0
C2=PASS
$ python3 -c 'import pathlib;C=pathlib.Path("/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache");ja=(C/"7194acc65a18f6555e4b8893.txt").read_text();cn=(C/"62be15a474e866e4bef6c9d5.txt").read_text();
print(len(ja),len(cn),ja.count("か，その日時，使用した検索式を同時に記録しておく"),ja.find("か，その日時，使用した検索式を同時に記録しておく"),
ja.find("このプロセスに際して，誰が検索を行ったの"),ja.find("誰が検索を行ったの"),ja.find("その日時，使用した検索式を同時に記録しておく"))'
21216 39676 1 10232 13710 13721 10234
```

So `c2-count.py` **PASSes** on this entry (61/61 quotes in span/entry/lesson, ANCHOR_BOUND=6/6, SUBSTANCE=PASS, INFERENCE_GROUNDED=3/3). Every defect below survives that pass, and D2 is the reason why (§ *What the counters cannot see*).

## Defects

**D1 (entailment + negation, worst) — the expression IS asked for in the checklist body; the entry says it is only attached.**
Bullets: Observation 4 (`:15`) "Item 7 **moves** the searcher, the words and the expression onto a separate form"; Inference 1 (`:20`) "the expression is **not restated in the checklist body but attached**"; title (`:1`) "the expression filed as an attachment". The same bullet (`:15`, first clause) already says item 7 "asks for the complete search strategy for every database, registry and website, filters and limits included" — so the entry contradicts itself. The capture, `62be15a474e866e4bef6c9d5.txt` read as UTF-8, item 7's *requirement* cell is line-wrapped by the two-column extraction into three contiguous runs, each occurring exactly once:
`用いたフィルターや制限も含め、全てのデー` @4330 · `タベース、研究登録、Web サイトの完全な検` @4385 · `索戦略を記載する。` @4481
and the 記載のポイント `検索者、検索ワード、検索式は別紙様式 (V) -5に示したことを記載する。` @4409 sits interleaved on the same extracted line as 4385. The body therefore requires the 完全な検索戦略; (V)-5 *adds* the searcher, words and expression as used. A negation ("not restated … but attached") that the capture's own item-7 cell reverses.
Narrowing: "Item 7 asks for the complete strategy in the body and points the searcher, the words and the expression to a second sheet"; "the body requires the complete strategy, and the searcher and the expression as used are additionally carried on (V)-5"; title "…, the expression as run also filed on an attachment".

**D2 (two figures that do not reproduce) — `char 13721` and `char 10234` are another quote's offsets.**
Observation 1 (`:12`) pairs `このプロセスに際して，誰が検索を行ったの` with char 13721 and `か，その日時，使用した検索式を同時に記録しておく` with char 10234; `text.find` in the stated form gives **13710** and **10232**. The numbers printed are the offsets of the shorter overlapping quotes the entry uses elsewhere — `誰が検索を行ったの` @13721 (Inference 2, `:22`, correct) and `その日時，使用した検索式を同時に記録しておく` @10234 (the `recheck:` line, `:5`, correct). The manifest is right and the entry is wrong: `spans/S107-12.txt` offset 13630 (`+80` = 13710), `S107-1.txt` offset 10152 (`+80` = 10232); `corpus/lessons/round-51.md:97,98,108,110` carry the correct pairing. The same wrong pair is duplicated in `corpus/SOURCES.md:117` (`char 13721, char 10234` in the anchor cell). `verified-at` (`:6`) "every quote below re-located with `text.find`" is therefore not true of these two.
Narrowing: use char 13710 and char 10232 for the long quotes (or shorten the quotes to the 13721/10234 forms); correct the same pair in `SOURCES.md:117`.

**D3 (wrong referent) — "two more … for a PRISMA 2020 Japanese translation".**
Unknown 1 (`:27`, tail): "two more (chars 17377, 18363) are reference-list entries for a PRISMA 2020 Japanese translation". 17377 is that reference (`…の更新版ガイドライン」の解説と日本語訳．薬理と治療．49(6)．831-842．2021`); **18363 is the PRISMA-ScR reference** — `ja[18273:18480]` reads `スコーピングレビューのための報告ガイドライン日本語版：PRISMA-ScR. 日本臨床作業療法研究．2020；7：70–76.` (and `PRISMA-S` @18441 sits inside that `PRISMA-ScR`, as the `ground:` line correctly says).
Narrowing: "the PRISMA 2020 Japanese translation (17377) and the PRISMA-ScR Japanese version (18363)"; conclusion "None is a search-record standard" then still holds.

**D4 (instrument generalised) — "a running header **and footer**".**
Observation 5 (`:16`) and the S108 `source:` line (`:3`): the edition line `2026年6月5日 第２版` occurs exactly 3× (142, 28260, 35891 — verified) but all three are page **headers**: 142 precedes the first form feed, and 28260/35891 follow the `\x0c` at 28149/35789 (the document has 9 form feeds). There is no footer occurrence, and 3 of 10 page blocks carry it, so "running" overstates too.
Narrowing: "a page header on three of the ten pages, so it is a name, not a unique span".

**D5 (characterisation) — "S108's 更新 hits are about an updated review".**
Unknown 4 (`:30`). `更新` occurs 17× in `62be15a…`; only the item-1 point `更新版であれば更新した旨を記載する` @1498 (with its extraction duplicate @1505) is about an updated **review**, while 4 label the updated notification in the abstract/flow (`2092, 2183, 2222, 2251`), 2 are the PRISMA reference title (`28017, 35668`), `2605` names `引用する更新元の届出番号`, `36933/36983` are the (V)-5 prior-study rows, and `2519/2527/2537, 11021, 14314/14321` are the notification's 更新版 fields inside review sections. The bullet's conclusion ("not about this document's own second edition") holds; its plural "hits are about an updated review" does not.
Narrowing: "S108's `更新` hits name an updated notification (届出番号, 更新版) and one reference title, none this document's own second edition".

**D6 (characterisation) — `アクセス` is not only "database reachability".**
Unknown 2 (`:28`): "`アクセス` (5 in S107, 1 in S108) names database reachability and one access date in a reference". S107's five are 5326 `オープンアクセスジャーナル`, 6048, 6636, 6778 (database access), 17691 (`月 15 日にアクセス）`, a reference); S108's single is `レビュープロトコールにアクセスできる場所` @25993 (`アクセス` @26004) — a place a protocol can be accessed, not database reachability. Counts reproduce; the gloss does not. (`検索でき` 3/0 does hold: 5903, 6311, 12415 all "a database one can search".)
Narrowing: "names open-access journals, database reachability, one protocol-access location and one reference access date; none is a failure statement".

**D7 (title/claim strength) — "require", and "one requirement stated twice".**
Title (`:1`) and `ground:` (`:7`) say what the documents *require* / *must* carry; S107's sentence is `…ことが望ましい` (advisory) and the entry says so twice. Inference 2 (`:21`) "one requirement stated twice" flattens an advisory recommendation and an industry form's rule for one notification regime; and its "the same content" merges the article's `その日時` (the search's date) with the form's per-database last-search date. The lane's own coverage row is more careful than the entry: `corpus/README.md:1089` says "a health-education society journal **recommending** …".
Narrowing: "what two Japanese documents say a search record must carry"; "two documents state overlapping fields with different force and different dates — an advisory article and a notification form's rule".

**D8 (adjacent, new row, not the entry) — registry page range does not reproduce.**
`corpus/SOURCES.md:117`: `日本健康教育学会誌 32(2):120-121 (2024)`. The capture's own citation line reads `〔日健教誌，2024; 32(2): 118–124〕` (`118–124` @766; page footers `119` @5701, `120 … 日健教誌` @9275, `121` @10178, `122 … 日健教誌` @13780, `123` @19128, `124 … 日健教誌` @21168). `120-121` is inherited verbatim from the staged row (`/home/vgpnk/Projects/shokuknow/merge/chousa/SOURCES.append.md:34`) and was not re-derived while the anchor's page was corrected 121→122. The entry's own page-footer claim is right; the row's title is wrong.
Narrowing: `32(2):118–124 (2024)`.

## What holds (tested, survived)

- **The layout claim is true, though the offsets were not.** The page-122 block runs 10189–13780; its extracted lines interleave left/right column (capture line 183 @10189 = left `よび結果データを含めることが一般的であるが，必ずし` + right `か，その日時，…` @10232; the column's foot @13705 `記録する．このプロセスに際して，誰が検索を行ったの` @13710, then `122    日健教誌   第 32 巻   第2 号   2024 年` @13780). So "foot of the left column → head of the right column" is exact, and the column wrap explains why the continuation has the *smaller* offset. My first counterexample (that a continuation cannot precede its start) is refuted by the extraction order — reported because it is the claim most likely to be wrongly struck.
- **Page-footer correction (122, not 121) holds.** Section heading `7.    1 次情報のまとめ` @13418, sentence @13710, footer 122 @13780; `特別報告` @0, `喜屋武 享` @2524, 21,216 characters, sha256 prefix `05c7ee9fe9e55461…` all exact.
- **All four Unknown sweeps reproduce exactly**, verbatim command included: `[0, 0, 0] [0, 0, 0]`; `[0]×6 [0]×6`; `[0]×5 [0]×5`; `[0] [0]`; `アクセス 5/1`; `検索でき 3/0`; `ガイドライン` 4/2 with 12212 (STROBE), 12458 (the `ガイドラインである．` predicate of the PRISMA sentence, whose subject reads `PRISMA は，介入研究の報告ガイドライン ʻCONSORTʼ や観察研究の…`), 17377, 18363, 28020, 35671 all locating as claimed.
- **Observation 3 and 4's quotation of the form holds**: item 6's requirement cell (runs `全てのデータベース、研究登録、Web サイ` @3966, `ト、組織、文献リスト、研究を特定するために` @4022, `調べたり、助言を求めたりした情報源を記載` @4102), `全てのデータベース` @3966, `それぞれの情報源が最後に調べられた` @4192, `それぞれのデータベース毎に最後に検索した日の日付を記載する。` @4124, `ハンドサーチの有無を記載する。` @4211, `検索戦略` @4311, and the (V)-5 留意点 `検索ワードや検索式は実際に使用した、…` @36834 (row 2 of the 記載上の留意点 table, `2    別紙様式 (V) -5` @36776).
- **The verify-sweeps inference holds on every checkable point.** `tools/research-gate.sh` emits `SWEEP id=… where=… looked=… hits=… at=… observed=… verdict=…` (2915–3010, summary 3018), and `awk 'NR>=2674 && NR<=3030' … | grep -c 'eval '` = 0 (the command is tokenised for path words, never run). Both cited lane files say it: `corpus/README.md:390-391` "the sweep re-run is a glob/existence check over the named locations, never the recorded command"; `SKILL.md:482-489` "re-measures only what a sweep names … not that a non-local sweep was ever run".
- **`chain-resolution-r3.md` supports Inference 4**: `:145-147` "The mode cannot check that an exemption is truthful — it only forces hops that CLAIM `resolved` to carry anchors that exist."
- **Title line, credit block and three 協力 bodies hold** (`809`, `298-…`, each body 3×); `PRISMA-S` 1× inside `PRISMA-ScR` @18441; the edition-line offsets 142/28260/35891 are exact (only D4's "footer" is wrong).

## What `inference-ground.py` refuses, and what it cannot see

It refuses nothing here: `bullets=4 tokens=10 grounded=10`. It reads **only `#### Inference`**, so the five Observation bullets and the five Unknown bullets are entirely outside it — D2, D3, D4, D5, D6 are in those sections. Inside Inference it checks only that a backticked/double-quoted phrase of ≥2 words occurs verbatim in a cited span (or a numeral in `--counts`); with `--counts /dev/null` no figure is checkable at all. Consequently it cannot see: (a) the `char N` values in prose (D2), even when they name another quote's offset; (b) that the *rest* of the capture contradicts the bullet's unquoted clause (D1 — the quoted fragments are all present, and item 7's requirement cell is never a token); (c) lane-file claims cited in prose (`corpus/README.md`, `SKILL.md`), which carry no token; (d) page/section/header placement (D4), figure provenance (D8) and cross-file pairing (registry anchor vs manifest); (e) title and heading claims (D7). `c2-count.py`'s ANCHOR_BOUND is blind for a sharper reason: it builds `offsets[sid]` as *every* quote's start (`offset + span.find(quote)`, :207) and accepts an anchor if it is in that set (:218-222), so 13721 and 10234 pass as valid offsets of the wrong quotes. `corpus/README.md:390-391` and `SKILL.md:482-487` say it in the lane's own words.

## Draft corrections (for the L1; lane paths as labelled)

```text
corpus/knowledge/japanese-search-record-r38.md:1
# What two Japanese documents say a search record must carry: the searcher, the date and the expression as run, the expression as run also filed on an attachment (round 51)

:4  source: S107 — … located quotes char 13710, char 10232, char 10314, char 10370, char 12666, char 12732, char 12807, char 17398
:12 … `このプロセスに際して，誰が検索を行ったの` at the foot of the left column (char 13710) and continues at the head of
    the right column `か，その日時，使用した検索式を同時に記録しておく` (char 10232) `とが望ましい．`
:15 - **Item 7 asks for the complete strategy in the body and points the searcher, the words and the expression to a
    second sheet.** …（rest unchanged）
:20 As this copy states it, item 7's body requires the complete strategy (`用いたフィルターや制限も含め、…`), and the
    searcher, the words and the expression as used are additionally carried on (V)-5 (`実際に使用した` or `同等の詳細なもの`)
:21 …two documents state overlapping fields with different force — an advisory article and a notification form's rule…
:27 …two more (chars 17377, 18363) are reference-list entries: the PRISMA 2020 Japanese translation and the PRISMA-ScR
    Japanese version.
:30 …; S108's `更新` hits name an updated notification and one reference title, not this document's own second edition.
:28 …`アクセス` (5 in S107, 1 in S108) names open-access journals, database reachability, one protocol-access location and
    one reference access date…

corpus/SOURCES.md:117  … 32(2):118–124 (2024) … | … char 13710, char 10232, char 10314, …
```

VERDICT: attacked the S107/S108 entry's three-field sentence, page/section correction, 'pair' inference, verify-sweeps inference and four Unknown sweeps — the layout claim, footer-122 correction, all four sweeps, the item-6/7 quotations and the verify-sweeps limits all reproduce, while seven defects stand: D1 (a negated "not restated in the checklist body" that item 7's own requirement cell reverses — the strongest), D2 (two `char` values that are overlapping shorter quotes' offsets, duplicated in the registry anchor), D3 (PRISMA-ScR mislabelled as the PRISMA 2020 translation), D4 ("header and footer" where all three occurrences are page headers), D5/D6 (blanket glosses of `更新` and `アクセス`), D7 (title "require" / "one requirement twice" against an advisory sentence), plus the adjacent registry page range 120-121 for a copy that says 118–124.
