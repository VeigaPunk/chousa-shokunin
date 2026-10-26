# R51W2ExecNegJa2 — the amendment's negatives re-run, the two searcher claims widened

seat: `R51W2ExecNegJa2` (executor, leaf) · round-51 / w2 (falsify) · 2026-10-25
scope: every command-bearing negative in `corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md`
(`#### Unknown`, `recheck:`, the "does not name" bullet, the `verified-at` offsets), then two searcher-absence
claims widened by five synonyms per capture language. Read-only on the lane and on
`/home/vgpnk/Projects/shokuknow`; this file is the only write. No tool installed (pacman paused; `python3` 3.14.8
sufficed — `build-spans.py`'s `form_texts` imported in-process). Lane HEAD observed `72566c8` (wave-2 spec); the
briefing's tip `4436e27` is its ancestor (`git merge-base --is-ancestor … HEAD` → 0). Forms named below are
the `.txt` read as UTF-8; keys were re-derived from `sha256(url)[:24]`, never copied.

## 1. Re-run table — every printed command and negative

| # | item as printed | run (from lane root) | observed | vs the entry |
|---|---|---|---|---|
| 1 | `recheck:` "prints `SPANS_ROWS=n STALE=0`" | `env -u ASSIMILATE_CITES python3 corpus/evidence/round51/build-spans.py --check` | `SPANS_ROWS=61 STALE=0`, rc 0 | **reproduces** |
| 2 | `recheck:` "re-download the PDF and confirm `検索の開始日と終了日を記載することで` (char 11294)" | (i) re-download; (ii) `text.find` in `34fcefc159bf2ebbd1e09540.txt` | (i) **not runnable**: no network by rule (L0 `8d77e6c1`); (ii) `11294`, `count=1` | offset **reproduces**; download not runnable |
| 3 | Unknown 1 key `f3dbe2fe59a684b1b94cfadc`, "`ls` lists only `.fail`" | `python3 -c "import hashlib;print(hashlib.sha256(b'https://www.lifescience.co.jp/yk/jpt_online/prisma/list_1.pdf').hexdigest()[:24])"` + `ls …/f3dbe2fe59a684b1b94cfadc*` | `f3dbe2fe59a684b1b94cfadc`; `/…/.qcache/f3dbe2fe59a684b1b94cfadc.fail` (one line) | **reproduces** |
| 4 | Unknown 2 sweep "prints `25811 [0, 0, 0, 0]`" | the entry's own `python3 -c "…[t.count(w) for w in ('検索者','検索担当','ハンドサーチ','灰色文献')]"`, unmodified | `25811 [0, 0, 0, 0]` | **reproduces exactly** |
| 5 | Unknown 3 "the round's span pipeline cannot read [the `.docx`] from either capture form" | `form_texts(cache, url)` from `build-spans.py:55-66`, key `3a8b45977cd111e45e3980a5` | see (a) | **reproduces** — by execution |
| 6 | Unknown 3 "text exists only inside a compressed `word/document.xml` member" | `zipfile` member list + `<w:t>` text per part | see (b) | **reproduces** |
| 7 | Unknown 4 "it cites no journal rule or standards body in the sentence read" | `t[11180:11560]` + reference `８）` | see (c) | holds only in the narrow reading |
| 8 | Unknown 5 staged "HTTP 000, zero bytes" | `grep -n HTTP merge/chousa/knowledge/corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md` | `64:… returned HTTP 000 with zero bytes for both the` | **reproduces** |
| 9 | `verified-at` "every quoted phrase re-located at its stated offset" | `text.find` for the seven pinned phrases | see (d) | **reproduces** |

(a) `.txt chars 168952 FFFD 72117 quote_count 0` · `.raw chars 89007 FFFD 2755 quote_count 0` — the `.txt`
sidecar is the ZIP bytes decoded with replacement and the builder reads `.raw` as UTF-16LE only, so the quote
(*SRにおける文献検索期間について明記する。*) occurs 0× in both. (b) 19 members; `word/header1.xml` text `''`,
`word/footer1.xml` `'9'`, `word/footnotes.xml` and `endnotes.xml` `''` — no body text outside `document.xml`.
(c) the sentence closes `…評価がしやすくなる８）。` (marker at `11466`, unique) and reference `８）` reads
`Page MJ, McKenzie JE, Bossuyt PM, …` — the PRISMA 2020 statement. (d) `11294 11229 10140 10146 11243 11348
11457`, each unique. Also holding: 25,811 characters, `17 項目`, `未発表の資料や抄録を含めるか` at 9950-10300.

## 2. Widening A — the amendment's searcher claim (S112, Japanese)

Claim attacked, as printed: *"The searcher is not a field in this article. … the sweep in `#### Unknown` counts
no 検索者 and no 検索担当 in the capture, **so** the article does not name who ran the search."* Five synonyms
the entry does not sweep, plus one phrase probe, counted raw and whitespace-insensitively (S112's PDF text
carries letter-spaced runs, e.g. `検 索 を 行 い つ つ` at 6116, so exact-string counts are form-dependent):

| term | S107 `7194acc6…` | S108 `62be15a4…` | S112 `34fcefc1…` |
|---|---|---|---|
| `検索者` | 0 / 0 | **3 / 3** | 0 / 0 |
| `検索担当` · `検索実施者` · `検索責任者` · `サーチャー` · `情報専門家` | 0 | 0 | 0 |
| `司書` (new) | 0 / 0 | 0 / 0 | **5 / 5** |
| `誰が検索` (phrase) | **1 / 1** @13721 | **1 / 1** @31183 | 0 / 0 |
| `誰が` | 1 | 1 | 1 @15105 |

**S112's claim holds.** The single `誰が` is `誰が行ったかを記載することが求めら` (15105, unique) and its
subject is screening: `文献選択を１人または複数人` (15053, unique) `で行ったか` — PRISMA's *who* for study
selection, not for the search. No `誰が検索` occurs, so the 0 is corroborated by reading, not by the count.
Two qualifications the entry omits: (i) the search step does name a person-role — `司書に相談し，協同して
立案することで` (13314, unique) is step 7's advice and `専門の司書に相談したか」という査読コメント`
(13546) is a reviewer question — so only "no searcher *field*" is defensible, not "no person"; (ii) the
letter-spaced runs mean a reader cannot infer from the token count alone which strings were exempt.

## 3. Widening B — the Chinese entry's searcher claim (S109/S110/S111)

Claim attacked (`corpus/knowledge/chinese-search-record-r39.md:27,37`): *"检索者 occurs 0 times in each of the
three forms"* … *"检索者 is absent from all three"*. Five new synonyms plus `谁`, raw / normalised:

| term | S109 `fd468a36…` | S110 `c7266931…` | S111 `42bac883…` |
|---|---|---|---|
| `检索者` · `检索员` · `检索执行者` · `检索负责人` · `图书馆员` · `信息专家` · `谁` | 0 / 0 | 0 / 0 | 0 / 0 |
| `检索人员` (already W1 `R51ExecNegSweep`'s term) | 0 / 0 | 0 / 0 | 0 / 0 |

**Holds, and the widening strengthens it**: 8 terms × 3 forms × 2 count modes, all 0 — the entry's *"unrecorded here rather than refused"* stands; the five spellings and the normalised recount are new.

## 4. F1 — the count cannot carry that entailment (the one real break)

The amendment joins a token count to a naming conclusion with "so". The lane's own captures falsify that step:
`検索者` = 0 in **S107**, the document `japanese-search-record-r38.md` cites as *requiring* the searcher —
which it names as `誰が検索を行ったの` at 13721 (unique) — and S108 names it as `誰が検索を実施したか` at
31183 (unique). So a `検索者` sweep returns 0 for the very document that carries the field. For S112 the
claim survives on reading, not on the count, and Unknown 2's sentence states an inference the lane's own S107
disproves as a rule. (F2, secondary: the width of `司書` in S112 was reported in W1 `R51GroundJahbsB`; I
re-derived it independently and it is absent from the entry.) The full counts and offsets are in §6's run.

## 5. Suggested wording (entry text only; no predicate, target, counter or control touched; L1 decides)

Unknown 2 / Inference 5: "…counts 0 `検索者` and 0 `検索担当`, and a direct read finds no `誰が検索`; the
article's `誰が` requirement is for 文献選択 (15105), and it names a 司書 as co-planner (13314)". Unknown 4:
"the sentence is cited (`８）` = Page et al., PRISMA 2020 statement) but names no journal rule or standards body".

## 6. Not run / limits, and the widening script

- Re-download clause of `recheck:` — not runnable (no network by rule; L0 `8d77e6c1` open); its offset re-located.
- Register `S120` row (`corpus/lessons/round-51.md:88`) states char **39411** for
  `SRにおける文献検索期間について明記する。` in "form `.raw` unzipped → `word/document.xml` UTF-8". My two
  constructions of that form place it at **8417** (`<w:t>` runs joined, 18,478 chars) and **8936**
  (paragraph-joined, 19,716 chars); 0× in the raw XML string. Peer `R51W2CritEntryJa2` reports a 55,839-char
  form locating it at 39411 — the offset needs a form the row does not define; C2's call, not judged here.

```python
import hashlib, re
Q = '/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/'
U = {'S107': 'https://www.jstage.jst.go.jp/article/kenkokyoiku/32/2/32_320208/_pdf/-char/ja',
     'S108': 'https://jaohfa.com/pdf/systematic_review.pdf',
     'S112': 'https://www.jahbs.info/journal/pdf/vol38_1/vol38_1_5.pdf',
     'S109': 'https://www.slarc.org.cn/dwyx/EN/article/downloadArticleFile.do?attachType=PDF&id=5290',
     'S110': 'https://www.slarc.org.cn/dwyx/CN/article/downloadArticleFile.do?attachType=PDF&id=5237',
     'S111': 'https://www.sinomed.ac.cn/article.do?ui=2026335073'}
JA = ['検索者', '検索担当', '検索実施者', '検索責任者', 'サーチャー', '司書', '情報専門家', '誰が検索']
CN = ['检索者', '检索人员', '检索员', '检索执行者', '检索负责人', '图书馆员', '信息专家', '谁']
for sid, terms in [(s, JA) for s in ('S107', 'S108', 'S112')] + [(s, CN) for s in ('S109', 'S110', 'S111')]:
    t = open(Q + hashlib.sha256(U[sid].encode()).hexdigest()[:24] + '.txt', encoding='utf-8').read()
    n = re.sub(r'\s+', '', t)
    print(sid, len(t), {w: (t.count(w), n.count(w)) for w in terms})
```

```
S107 21216 {'検索者': (0, 0), '検索担当': (0, 0), '検索実施者': (0, 0), '検索責任者': (0, 0), 'サーチャー': (0, 0), '司書': (0, 0), '情報専門家': (0, 0), '誰が検索': (1, 1)}
S108 39676 {'検索者': (3, 3), '検索担当': (0, 0), '検索実施者': (0, 0), '検索責任者': (0, 0), 'サーチャー': (0, 0), '司書': (0, 0), '情報専門家': (0, 0), '誰が検索': (1, 1)}
S112 25811 {'検索者': (0, 0), '検索担当': (0, 0), '検索実施者': (0, 0), '検索責任者': (0, 0), 'サーチャー': (0, 0), '司書': (5, 5), '情報専門家': (0, 0), '誰が検索': (0, 0)}
S109 52208 {'检索者': (0, 0), '检索人员': (0, 0), '检索员': (0, 0), '检索执行者': (0, 0), '检索负责人': (0, 0), '图书馆员': (0, 0), '信息专家': (0, 0), '谁': (0, 0)}
S110 50952 {'检索者': (0, 0), '检索人员': (0, 0), '检索员': (0, 0), '检索执行者': (0, 0), '检索负责人': (0, 0), '图书馆员': (0, 0), '信息专家': (0, 0), '谁': (0, 0)}
S111 1675 {'检索者': (0, 0), '检索人员': (0, 0), '检索员': (0, 0), '检索执行者': (0, 0), '检索负责人': (0, 0), '图书馆员': (0, 0), '信息专家': (0, 0), '谁': (0, 0)}
```

VERDICT: attacked the amendment's four command-bearing negatives, its offsets and its searcher inference, plus the Chinese entry's `检索者` absence — every printed command reproduces (`SPANS_ROWS=61 STALE=0`, `25811 [0, 0, 0, 0]`, the PRISMA `.fail` key, the seven offsets, the staged HTTP 000 line, and the `.docx` refusal re-proved by executing `form_texts`: 0 quotes in both forms), both searcher claims survive five-synonym widening in each language (S112 7 of 8 terms 0, the eighth `司書` 5, the only `誰が` at 15105 being 文献選択; S109-S111 8/8 terms 0), but "counts no 検索者 **so** the article does not name who ran the search" is falsified as an inference by the lane's own S107 (`検索者` 0, `誰が検索を行ったの` at 13721) and S112's search step does name a person-role (`司書` 5×, 13314).
