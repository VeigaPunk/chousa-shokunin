# R51W2CritEntryJa2 — attack on `corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md`

Seat `R51W2CritEntryJa2` (round 51, wave 2 — falsify, leaf critic); seat `R51W2CritEntryJa2-2` (duplicate dispatch, same assigned path) appended a §5 to this file and its runs are folded in below. Tip `4436e279b91d8d68fd439c9095695035fbeeab74`, base `9ec1751a24231e899ceea4688e21c8edf6046d35`, freeze `d603f6f00f78d64f123d3aed2dd9f8701547a4ba`. Read `/home/vgpnk/.omp/agent/RULES.md`; pacman untouched; 0 tools installed (none needed). Scratch `/dev/shm/chousa-r51-R51W2CritEntryJa2b/` (lane files COPIED, never symlinked), deleted at the end. No fetch (L0 `8d77e6c1` open).
Decode form for every `char N`: `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/34fcefc159bf2ebbd1e09540.txt` read as UTF-8, 25,811 characters (`len`). Each offset below is `text.find` of the run quoted immediately before it — where a longer run and its substring differ (11172 vs 11175; 5966 vs 5982) both are correct for their own run and neither is an error. Entry line numbers `:N`.

## 1. Commands and observed output

```
$ python3 - … seven stated offsets
'検索の特徴（検索期間' find= 10140 stated= 10140 count= 1 OK
'検索期間，言語制限' find= 10146 stated= 10146 count= 1 OK
'検索した文献データベース名' find= 11229 stated= 11229 count= 1 OK
'Ovid などのプロバ' find= 11243 stated= 11243 count= 1 OK
'検索の開始日と終了日を記載することで' find= 11294 stated= 11294 count= 1 OK
'最新の結果を反映しているかどうか' find= 11348 stated= 11348 count= 1 OK
'評価がしやすくなる' find= 11457 stated= 11457 count= 1 OK
$ env -u ASSIMILATE_CITES python3 corpus/evidence/round51/build-spans.py --check
SPANS_ROWS=61 STALE=0
$ env -u ASSIMILATE_CITES python3 corpus/evidence/round51/c2-count.py | tail -2
QUARANTINE_BLOCKED_ADOPTED=0
C2=PASS
$ python3 tools/inference-ground.py --entry corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md \
    --spans corpus/evidence/round51/spans.tsv --counts corpus/evidence/round51/c2-count.py --registry corpus/SOURCES.md --root .
GROUND entry=… section=1 bullets=5 tokens=8 grounded=8
GROUND: PASS
$ python3 -c "…counts('検索者','検索担当','ハンドサーチ','灰色文献')…"          → 25811 [0, 0, 0, 0]
$ grep -o "S[0-9]\{3\}" <entry> | sort | uniq -c                                → 15 S112
$ python3 - … docx capture forms
.txt: len 168952 fffd 72117 nul 4442 starts 'PK\x03\x04\x14\x00\x06\x00'; 3 staged quotes find=-1
.raw word/document.xml: compress_type 8 file_size 1464476 compress_size 139609
paragraph-joined w:t runs: len 55839, find('SRにおける文献検索期間について明記する')=39411 count=1
$ cat …/.qcache/f3dbe2fe59a684b1b94cfadc.fail                                        → rc=28
$ python3 -c "…sha256('https://web.archive.org/web/2024/https://www.lifescience.co.jp/yk/jpt_online/prisma/list_1.pdf')[:24]…"
e84bfe97808591d23fe3266f
$ python3 -c "t=open('…/e84bfe97808591d23fe3266f.txt',encoding='utf-8').read();print(len(t),repr(t[:20]));print(t.find('検索戦略'),t.find('用いたフィルターや制限も含め，'),t.count('用いたフィルターや制限も含め，'),t.count('検索期間'),t.count('検索者'))"
5328 'PRISMA 2020 チェックリスト\n大項目' 619 641 1 0 0
$ sed -n '68p' corpus/lessons/round-51.md
| `japanese-prisma-item-wording-r40.md` | S129 | yes, at the archive: `e84bfe97808591d23fe3266f` (.txt, 5,328, char 641); the row's own URL key `f3dbe2fe59a684b1b94cfadc` is absent | …
```

## 2. What holds

- All seven stated offsets reproduce exactly and once in the named form; `25,811` characters reproduces. The `spans.tsv` `offset` column is the span START (`quote = offset + 80`; `10060+80=10140` … `11377+80=11457`), so manifest, entry and Registry `anchor` do not disagree.
- Step attribution holds: `７．検索戦略を立案する` is at 10242; the three-field sentence at 11175 is that step's right-hand column, while the left-hand runs beside it are step 6 (`６．レビュープロトコルをレジストリへ登録する`, 11023).
- The refusal holds and nothing rests on it: only `S112` is cited; the refused `.docx` is in no quote and no span row; its `.txt` sidecar is the zip bytes decoded (72,117 U+FFFD, `PK` magic); the member is DEFLATE; the Gate's own location reproduces at 39,411 in the paragraph-joined `w:t` form. "Cannot read from either capture form" is true of the span pipeline's two forms, not of the document.
- `C2=PASS`, `SPANS_ROWS=61 STALE=0`, `GROUND: PASS`. The counters' presence/binding legs are not what I found wanting; the prose is.
- The `.fail` marker is real: content `rc=28` (so `:24`'s second half is right; only its headline is wrong — D9).

## 3. Defects

**D9 (high) — `:24`'s translation-absence is false, and the document it declares absent is on disk.** `:24` "The official Japanese translation of PRISMA 2020 was not opened in this lane's captures", justified by a sweep whose only hit is `f3dbe2fe59a684b1b94cfadc.fail` (`rc=28`). That sweep proves the dead original URL, not the lane's captures: the 2024 Wayback capture of the same document is in the same `.qcache` (`e84bfe97808591d23fe3266f`, `.txt` 5,328 chars, head `PRISMA 2020 チェックリスト`), and the round's own lesson line 68 records it read this round (`yes, at the archive: e84bfe… …, char 641`). Its content also bears on this entry: item 7 `検索戦略` at 619 with `用いたフィルターや制限も含め，` at 641, and `検索期間` **0**, `検索者` **0**.
*Narrowing:* `:24` → "the original URL's capture failed (`f3dbe2…`, `rc=28`); the 2024 Wayback capture of the same checklist is on disk (`e84bfe…`, 5,328 chars) and the round's lesson records it read; it names `検索戦略` (char 619) and requires filters and limits (char 641) but uses neither `検索期間` nor `検索者`". That converts an absence into the corroboration `:20`/`:6` want. A quote inside `#### Inference` needs a new span row first (`QUOTE_ROWS`, `QUOTES_IN_LESSON` move together). The same false absence is in `corpus/README.md:1106` (`R51W2ReviewReadmeScorecard` D3).

**D1 — the requirement status is asserted in three Inference bullets while `:27` says it was not established, and the step's own requirement sentence is skipped.** `:16` "as what the record must state", `:17` "incomplete by this article's list", `:19` "the lane can say this article requires the field" vs `:27` "…was not established". Capture: 11175-11457 is `…を記載することで … 評価がしやすくなる`, no requirement verb; the step's requirement verbs attach elsewhere: `すことが求められている３）。そのため，レビュープ` (11654), `ロトコルには完全な検索式と言語制限や検索期間な` (11730) + `どを，あらかじめ記載する必要がある３）。その他に` (11805), and a post-search list `検索が終了した後は，検索したデータベース名，` (12105) … `で再現性を担保する。` (12329).
*Narrowing:* `:16` "must state" → "is named as what to record"; `:17` "incomplete" → "does not carry the three items the sentence names as the database's information" (the list is scoped by `使用した文献データベースの情報として`, 11175); `:19` "requires the field" → "states the fields with a rationale and requires the protocol to carry the period in advance (char 11805)"; `:27` → the located answer for the protocol, leaving only the post-search list's force open.

**D2 — the currency rationale is upgraded to a purpose, and the step's second rationale is dropped.** `:18` "The stated rationale is currency … the record is kept so that a reader can judge … whether the search has been refreshed since". Capture: `最新の結果を反映しているかどうか，更新がされて` (11348/11365) then the page-64 running header at 11373, then `いるかどうかの評価がしやすくなる８）` (11450) — writing the dates makes an evaluation easier; it does not say why a record is kept. Step 7's other list gives a different rationale, reproducibility (`で再現性を担保する。`, 12329), so currency is the dates' rationale, not the step's only one.
*Narrowing:* `:18` → "Recording the dates makes it easier to judge whether the latest results are reflected and whether an update has been made (chars 11348, 11365, 11450)"; drop "the record is kept so that" and "and it is the lane's own recheck" (the article states no lane practice); `で再現性を担保する。` inside `#### Inference` needs a span row — quote it in Observation/Unknown or accept the manifest change.

**D3 — "the article does not name who ran the search" is not entailed by a four-token sweep, and the capture names the search's professional party five times.** `:20`. Capture: `を相談できる専門の司書がいないなどの検索上の制` (11956) + `約について，率直に記載する必要がある` (12031) — the search constraints, including no librarian, must be recorded; `い司書に相談し，協同して立案することで，適格な` (13313); `専門の司書に相談したか` (13543); `る専門の司書はいなかったため` (13770); `専門の司書がいる場合には` (14488). `司書` is invisible to the sweep (`検索者`/`検索担当`/`ハンドサーチ`/`灰色文献` all 0, above).
*Narrowing:* `:20` → "the three-field record sentence names no searcher and the capture has no 検索者/検索担当 token; but the article names 専門の司書 as the search's co-planner and requires recording the search constraint of having none (char 11956), so no searcher *field* is not no searcher *named*." Do **not** lean on 15105: `文献選択を１人または複数人` (15053) + `誰が行ったかを記載することが求めら` (15105) sit under step 8 (`８．含める研究を選択する`, 12588) and concern study selection, not the search — it shows the article's person-field vocabulary, nothing about the searcher. Also `:6`'s lane question is already answered YES by the entry this amends: `誰が検索を行ったの` (S107 `7194acc65a18f6555e4b8893.txt` 21,216 chars, char 13721) and `検索者、検索ワード、検索式` (S108 `62be15a474e866e4bef6c9d5.txt` 39,676 chars, char 4409). Do not cite S107/S108 here without updating their Registry `used-by` cells — C2 requires exact match, so a bare id insert breaks BOUND.

**D4 — "peer-reviewed" and "methods journal" (`:1`, `:11`) are attributes no capture sentence states.** Capture: `査読` 3× — `PRISMA 声明の準拠を求める査読付き雑誌` (5966; substring `査読付き雑誌` 5982), `査読者から` (13481) and `査読コメント` (13558), both about the authors' earlier submission to an unnamed journal; `peer` (lowercase) 0×, `ピア` 0×, and `Peer` 2× (14036 body, 23989 reference list), both inside the PRESS guideline (`PRESS` at 23983) — the search-strategy appraisal tool, not journal peer review; no sentence applies peer review to this article or journal. The title block at 158 gives 日本保健医療行動科学会雑誌 and a methods article; `:19` itself says "one society journal's methods article".
*Narrowing:* `:1` "a methods journal" → "a Japanese society journal's methods article"; `:11` → "A Japanese methods article"; drop "peer-reviewed" (it survives only from the Registry row's own `teaches` prose, i.e. circularly).

**D5 — the `プロバイダー` split is a line wrap in the right-hand column, not a gutter crossing.** `:12` "splits プロバイダー at the gutter, `プロバ` ending the left line and `イダー名` opening the right". `repr` 11140-11290: `…検索した文献データベース名，Ovid などのプロバ\n` then the next line's right-hand run `イダー名，検索の開始日と…`; `プロバ` ends the RIGHT-hand run of a line whose left-hand run is step 6's registry text.
*Narrowing:* `:12` → "a line wrap in the right-hand column run". The header's general note (`:3`) is nevertheless true and has a real instance: `また，レジストリにレビュープロト` (11321, left column bottom) + `コルを登録することで，事前に指定した` (8938, right column top), 2,383 characters apart on the page whose header is at 8843 — a gutter crossing inside レビュープロトコル. (Not 13313: that is a wrap inside the left column, `検索や情報に詳し` / `い司書`.)

**D6 — the 17-item reading has no located anchor, and its last element is turned from an inclusion decision into a list-mate.** `:11`. `SR のレビュープロトコルに必須かつ最低限の構成` (9930) and `要素と考えられる，17 項目が含まれている` (10016) are never cited; the cited 10140/10146 carry only 検索の特徴/検索期間; the requirement verb is `明記することが` (10200) + `求められている。` (10208). "beside unpublished material and abstracts" drops `含めるか`: `や抄録を含めるかなど` (10188). And "`検索期間` as a PRISMA-P item" aggregates one level: the capture nests 検索期間 inside 検索の特徴, which it gives as an example of what the 17 items require to be specified.
*Narrowing:* cite 10016 and 10208; write "names 検索期間 inside the search's features, which it gives as an example of what PRISMA-P's 17 items require to be specified, and asks whether unpublished material and abstracts are to be included (char 10188)". Keep it in Observation/header prose: a new backticked token inside `#### Inference` needs a span row.

**D7 — `:26` asserts the refused form's content without a capture offset.** "A national institute's submission form … states a search-period requirement" while the same bullet says its text cannot be read; from either capture form all three staged quotes are absent. The sentence is locatable only in the Gate's member form (39,411).
*Narrowing:* cite that form and offset in `:26`, or write "the staged entry attributes a search-period requirement to the form; this round located the sentence only in the Gate's member form (char 39411)". "Nothing in this entry rests on it" otherwise holds.

**D8 — `:5` recheck prints the literal `n`.** Ran it: `SPANS_ROWS=61 STALE=0`. *Narrowing:* write 61.

Overlap: D4 = `R51W2ReviewEntryJa2` D1; D1/D3 confirm its D2/D3 (D1 adds 11654/11805 and the 12105-12329 list, D3 adds `司書` 11956 and the `used-by` consequence); D2, D5, D6, D7, D8, D9 are not in that report.

## 4. What inference-ground refuses, and what it cannot see

It refuses nothing on this entry (`bullets=5 tokens=8 grounded=8`). Three mutations, each on a scratch COPY of the entry:

```
$ … title: "# The Japanese search record carries…" → "# A Japanese national standard carries a stated 検索期間"
GROUND entry=mut-title.md bullets=5 tokens=8 grounded=8   GROUND: PASS  rc=0
$ … ":20 'The searcher is not a field'" → "'is a field'"; ":17 'incomplete'" → "'complete and sufficient'"
GROUND entry=mut-inf.md bullets=5 tokens=8 grounded=8     GROUND: PASS  rc=0
$ … new Inference bullet "The article is the Japanese national standard for search records and its wording binds
    the field list." with the token `検索の特徴（検索期間` (S112), entry otherwise unchanged
GROUND entry=mut-claim.md bullets=6 tokens=9 grounded=9   GROUND: PASS  rc=0
```

Blind by construction: it reads `#### Inference` bullets only — the title, `source:`/`recheck:`/`adopted:`/`ground:` lines, every Observation bullet (D1's item reading, D4, D5, D6) and every Unknown bullet (D7, D9) are unchecked; `words()` is Latin-only, so a CJK token is a presence check and never trips polarity; a figure need only occur somewhere; and a bullet whose cited token grounds none of its claim (the third mutation) passes.

VERDICT: attacked `corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md` against capture `34fcefc159bf2ebbd1e09540.txt` (UTF-8, 25,811 chars) and the archive capture `e84bfe97808591d23fe3266f.txt` — offsets, step attribution, the `.docx` refusal, the `rc=28` marker and all counters hold, but 9 prose defects break (highest: `:24`'s "not opened in this lane's captures" is false against the on-disk Wayback checklist the lesson records reading, which also shows `検索期間`/`検索者` 0; then the requirement-status contradiction with the unquoted `必要がある` at 11805, the currency purpose-shift plus the dropped `再現性` at 12329, the searcher conclusion unentailed against `司書` 5×, unstated "peer-reviewed"/"methods journal", a gutter misdescription at 11243, an unanchored `17 項目` at 10016, an uncited docx content clause, and `SPANS_ROWS=n`), so the entry is admit-with-narrowing and `inference-ground` refuses none of them.
