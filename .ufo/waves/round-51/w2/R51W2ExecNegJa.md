# R51W2ExecNegJa — re-running the negative claims of `corpus/knowledge/japanese-search-record-r38.md`

Seat: leaf, wave 2 (falsify). Lane `/home/vgpnk/Projects/shokunin/chousa-shokunin` at `4436e279b91d8d68fd439c9095695035fbeeab74`.
Read only: captures under `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/`, the three lane entries, `corpus/README.md`, `SKILL.md`. Wrote nothing but this report; no scratch dir, no fixture repo, no git/jj call, no network, no install (nothing to install).
Capture identity re-derived first: `sha256(url)[:24]` gives `7194acc65a18f6555e4b8893` (S107) and `62be15a474e866e4bef6c9d5` (S108); both files exist, `sha256sum` = `05c7ee9fe9e55461…` / `960da5cf632dbd27…` (the entry's prefixes), lengths 21,216 / 39,676 characters — the entry's figures exactly.

## 1. The four `#### Unknown` sweeps, verbatim from the lane root

Each command is the entry's own text, copied; S107 = `7194acc…txt`, S108 = `62be15a…txt`, both read as UTF-8.

```text
$ cd /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache && python3 -c "ja=open('7194acc65a18f6555e4b8893.txt',encoding='utf-8').read(); cn=open('62be15a474e866e4bef6c9d5.txt',encoding='utf-8').read(); print([ja.count(w) for w in ['標準','規格','JIS']], [cn.count(w) for w in ['標準','規格','JIS']])"
[0, 0, 0] [0, 0, 0]                                   # entry states the same -> reproduces
$ … [ja.count(w) for w in ['失敗','エラー','未実施','不完全','中断','実行でき']] …
[0, 0, 0, 0, 0, 0] [0, 0, 0, 0, 0, 0]                 # reproduces
$ … [ja.count(w) for w in ['履歴','エクスポート','書き出し','出力','保存']] …
[0, 0, 0, 0, 0] [0, 0, 0, 0, 0]                       # reproduces
$ … [ja.count(w) for w in ['改訂']] …
[0] [0]                                               # reproduces
```

Every number the entry prints for these four sweeps is exact. The sub-counts each bullet rests on also reproduce:

```text
アクセス 5 1            # entry: "5 in S107, 1 in S108" -> reproduces
検索でき 3 0            # entry: "3 in S107, 0 in S108" -> reproduces
ガイドライン ja 4 [12212, 12458, 17377, 18363]   # entry's four offsets, in order -> reproduces
ガイドライン cn 2 [28020, 35671]                 # entry's two offsets -> reproduces
更新版であれば更新した旨を記載する -> 1498       # reproduces
PRISMA-S ja 1 [18441]   PRISMA-S cn 0            # "occurs once … inside PRISMA-ScR" -> reproduces
1 次情報の「収集」 -> 2 [297, 1528]              # "char 297 and one other occurrence" -> reproduces
2026年6月5日 第２版 -> [142, 28260, 35891]       # "recurs at 142, 28260, 35891" -> reproduces
```

`recheck:` line: it is a 365-day schedule ("re-download both and confirm … and re-run the four sweeps"), **not runnable as written** — the re-download is a live fetch, forbidden this wave (L0 `8d77e6c1` open). Its confirmable half was run: `text.find` locates `その日時，使用した検索式を同時に記録しておく` at 10234 and `検索者、検索ワード、検索式は別紙様式 (V) -5に示したことを記載する。` at 4409, each exactly once, in the stated form; the four sweeps above reproduce.

## 2. Every `(char N)` anchor in the entry, re-located

Sixteen backticked quotes carry `(char N)`; one more (`このプロセスに際して，誰が検索を行ったの`, 13721) is anchored in prose. Script: regex the entry for `` `quote` (char N) ``, `text.find` in both captures, require `find == N` and `count == 1`.

```text
10234 S107 ja.find=10234  その日時，使用した検索式を同時に記録しておく        OK
10314 S107 ja.find=10314  研究の透明性を保ち，他者                          OK
10370 S107 ja.find=10370  が同様の検索を再現できるようになる                OK
12666 S107 ja.find=12666  PRISMA は，日本語を含め                          OK
12732 S107 ja.find=12732  言語に翻訳されている                              OK
12807 S107 ja.find=12807  報告すべき内容のチェックリストも付録されてい      OK
17398 S107 ja.find=17398  本健康教育学会誌にもシステマティックレビューの投  OK
 3966 S108 cn.find= 3966  全てのデータベース                                OK
 4192 S108 cn.find= 4192  それぞれの情報源が最後に調べられた                OK
 4124 S108 cn.find= 4124  それぞれのデータベース毎に最後に検索した日の日付を記載する。 OK
 4211 S108 cn.find= 4211  ハンドサーチの有無を記載する。                    OK
 4311 S108 cn.find= 4311  検索戦略                                          OK
 4409 S108 cn.find= 4409  検索者、検索ワード、検索式は別紙様式 (V) -5に示したことを記載する。 OK
36834 S108 cn.find=36834  検索ワードや検索式は実際に使用した、もしくはそれと同等の詳細なものであること。 OK
10234 ??    ja.find=10232 か，その日時，使用した検索式を同時に記録しておく  DIFFERS (observed 10232)
13721 S107 ja.find=13721  このプロセスに際して，誰が検索を行ったの          OK
```

**Differs — one anchor, by two characters.** `#### Observation` bullet 1 writes "continues at the head of the right column `か，その日時，使用した検索式を同時に記録しておく` (char 10234)". That string starts at **10232**, not 10234; 10234 is where the shorter span `その日時，…` starts (which is what the `recheck:` line rightly cites). Independent confirmation, not just my `find`: the committed manifest derives it the same way — `python3 corpus/evidence/round51/build-spans.py --check` → `SPANS_ROWS=61 STALE=0` (exit 0), and row `S107-1` is `offset=10152`, span `spans/S107-1.txt`, so quote char = 10152 + 80 = 10232, while row `S107-2` (`その日時，…`) derives 10234. So the entry contradicts its own span manifest on this one cell; the fix is 10232 for the `か，…` variant (or keep 10234 and quote without `か，`). Also confirmed: `望ましい` begins at 10303 (`ja[10303:10312]` = `望ましい．これによ`), as the entry says.

## 3. Supporting sentences inside the negative bullets

- **Unknown 1, "two more (chars 17377, 18363) are reference-list entries for a PRISMA 2020 Japanese translation" — 18363 mischaracterised.** 17377 is that reference (`2020 声明：システマティック・レビュー報告のための更新版ガイドライン」の解説と日本語訳`, same text as S108's 28017/35668). 18363 is a *different* reference: `報告ガイドライン日本語版：` at char 18361, continuing `PRISMA-ScR. 日本臨床作業療` at char 18441 — the PRISMA-**ScR** Japanese version (友利幸之介 et al.). The bullet's conclusion ("None is a search-record standard") still holds; the characterisation does not.
- **`ground:` "Cochrane occurs as a database name" — true of 3 of 4.** Offsets 7243, 12898, 12916 are Cochrane Library in database lists / a database bullet; `Cochrane handbook for system-` at char 14014 is a handbook citation in the reference list, not a database name. The substantive claim it defends (neither document derives a requirement from Cochrane) holds: no occurrence states one.
- **Unknown 4, "S108's 更新 hits are about an updated review" — 15 of 17.** The two outliers are the cited reference's own title (`更新版ガイドライン」の解説と日本語訳` at 28017 and 35668). The bullet's point (第２版 is not a changelog) is unaffected.
- **`source:` footer paraphrase.** The copy's footer reads `日健教誌   第 32 巻   第2 号` at char 13787 (`第2 号`, no space); the entry's non-backticked paraphrase writes `第 32 巻 第 2 号`. Not a located quote, so not a violation — but it is not the copy's spacing.

## 4. Widened searcher sweeps (five synonyms per capture's language)

The Japanese claim under test is the amendment's ("`検索者` 0, `検索担当` 0"), the Chinese one is r39's ("`检索者` occurs 0 times in each of the three forms"). Base counts first, then five added synonyms.

```text
$ cd …/.qcache && python3 -c "ja=…7194acc….txt…; cn=…62be15a….txt…; s112=…34fcefc159bf2ebbd1e09540.txt…; print([t.count('検索者') for t in (ja,cn,s112)])"
S108 検索者 -> 3   (chars 4409, 5720, 36710)      S107 0   S112 0
$ … ['検索実施者','検索担当者','検索した者','誰が検索','サーチャー'] per capture
S107 [0, 0, 0, 1, 0]      S108 [0, 0, 0, 1, 0]      S112 [0, 0, 0, 0, 0]
```

- **S112 (the amendment's claim): the narrowed wording holds.** All five added synonyms are 0. The one extra token, `実施者`, is 0 in S107/S108 and 2 in S112 — and both are `SR の実施者` / `SR 実施者がデータ抽出や` (chars 9154, 20401), i.e. the reviewers, not the person who ran a search. Nothing in S112 names a searcher field.
- **S107/S108 (r38's own captures): a widened sweep finds the searcher named, in both.** `誰が検索` is 1 in each — S107 at char 13721 (already quoted) and, in S108, a sentence the entry does not quote: **`誰が検索を実施したかを記載することが望`**, S108 `.txt` read as UTF-8, char **31183**, unique (`find == count == 1`), 20 characters; its predicate sits on a later line at char 31384 (`ましい。`) because the two-column extraction splits the sentence. Two more S108 searcher statements exist: `検索者は、原則、#8に記載する。` (char 5720, unique) and the (V)-5 sheet row `検索者、` at char 36710.
- So no "neither copy names the searcher" claim survives unscoped: the pair names the searcher in three places in S108 and once in S107. r38 itself never makes that claim (its item-7 bullet puts `検索者` on (V)-5, correctly); the exposure is only the amendment's `ground:` sentence, whose question ("whether any Japanese source in the lane's captures names the searcher as a field") S108 answers **yes**. Amendment + r38 read together are consistent; the amendment alone must not be read as a lane-wide negative.

```text
$ … [t.count(w) for w in ['检索员','检索人员','检索执行者','检索负责人','检索人']] on S109/S110/S111
S109 [0, 0, 0, 0, 0]   S110 [0, 0, 0, 0, 0]   S111 [0, 0, 0, 0, 0]   (base 检索者 also 0/0/0)
```

The Chinese claim holds under widening: no form or record among S109–S111 uses any of the five added searcher nouns, nor `谁检索` / `实施检索` (checked, 0 in all three). The narrowed wording still stands there.

## 5. What holds, and what I did not run

Holds (re-run, not re-read): all four `Unknown` sweeps and every count they print; all sixteen exact char anchors except the one in §2; the four `ガイドライン` / two `ガイドライン` offsets; the edition-line recurrence; the `PRISMA-S`-inside-`PRISMA-ScR` fact (and S108 has no `PRISMA-S` token at all, so "neither document states a PRISMA-S requirement" is stronger than the entry argues); the `1 次情報の「収集」` frame count; the Inference bullet on `verify-sweeps` — read from the tool itself, `bash tools/research-gate.sh verify-sweeps corpus/fixtures/sweeps-r5.md --root ..` prints `SWEEP id=W1 where=… looked=local hits=0 at=- observed=verified verdict=match`, i.e. no searcher and no expression field, and `SKILL.md:482-489` states the same limit ("re-measures only what a sweep names … not that a non-local sweep was ever run").

Widening the `標準/規格/JIS` sweep on regulator vocabulary returned 0 in both captures for `厚生労働省`, `消費者庁`, `通知`, `省令`, `告示`, `府令`, `内閣府`, so "S108 is an industry body's 留意事, not a regulator's rule" is not merely an artefact of three tokens.

Not run: the `recheck:` re-download (network forbidden); the `.docx`/S125 path and the other two counters (other seats' items). No production file was altered, so nothing in the counters or the manifest changed by me.

VERDICT: attacked the four negative sweeps, every printed count, all seventeen char anchors and two widened searcher sweeps — all four sweeps and all counts reproduce exactly; one anchor differs (`か，その日時，…` is at 10232, not 10234, a 2-char slip the committed span manifest also contradicts), two supporting characterisations are loose (char 18363 is a PRISMA-ScR reference, `Cochrane` at 14014 is a handbook citation), and the S112 searcher-absence claim holds under five added Japanese synonyms while the pair S107/S108 names the searcher three times in S108 (newly located at char 31183) and once in S107 — so the negative survives only when scoped as the entries scope it.
