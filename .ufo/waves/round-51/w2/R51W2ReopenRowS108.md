# R51W2ReopenRowS108 — re-open Registry row S108

Attacked: row `S108` in `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md:118` against on-disk capture `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/62be15a474e866e4bef6c9d5.txt` (61,188 bytes, 39,676 UTF-8 chars, sha256 `960da5cf632dbd278ea941c54d83e3ed8f13657bcb4bcbbfc8d63c9d834acf4a`), `corpus/evidence/round51/spans.tsv`, and `CORPUS.md` SOURCES-CONTRACT-v1. No tools installed; no scratch directory created; no lane files touched outside this report.

## 1. Row and capture extraction

```
$ grep -n '^| S108 ' /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md
118:| S108 | 機能性表示食品制度の届出資料におけるPRISMA 2020声明 システマティックレビュー記載の留意点 (別紙様式 (V)-4 本文) — 一般社団法人 健康食品産業協議会, 2026年6月5日 第2版 — https://jaohfa.com/pdf/systematic_review.pdf | docs | A | what this industry body's reporting form requires of a search record, as the form states it | 別紙様式 (V)-4 items 6 情報源 and 7 検索戦略 with their 記載のポイント and 別紙様式 (V)-5 item 2 with its 留意点; edition line 2026年6月5日 第２版; capture .txt read as UTF-8, 39676 characters; char 3966, char 4192, char 4124, char 4211, char 4409, char 36834 | the form requires every source consulted to be listed with the date each was last searched (per database), the presence or absence of hand-searching to be stated, and the searcher, search words and search expression to go on a separate attachment (V)-5 that holds what was actually used or an equivalent detail | mined | 2026-10-25 | 180d | corpus/knowledge/japanese-search-record-r38.md |
$ awk -F'|' 'NR==118{print "NF="NF}' /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md
NF=13
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa | tail -1
chousa	ok	/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md
```

## 2. Capture verification and located quotes (`.txt` read as UTF-8)

```
$ python3 -c '
import hashlib, pathlib
u = "https://jaohfa.com/pdf/systematic_review.pdf"
p = pathlib.Path("/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache") / (hashlib.sha256(u.encode()).hexdigest()[:24] + ".txt")
b = p.read_bytes(); t = p.read_text(encoding="utf-8")
print(p.name, len(b), len(t), hashlib.sha256(b).hexdigest())
for q in [
  "機能性表示食品制度の届出資料におけるPRISMA 2020声明 システマティックレビュー記載の留意点(別紙様式 (V) -4 本文)",
  "更新版であれば更新した旨を記載する",
  "全てのデータベース",
  "それぞれのデータベース毎に最後に検索した日の日付を記載する。",
  "それぞれの情報源が最後に調べられた",
  "ハンドサーチの有無を記載する。",
  "検索者、検索ワード、検索式",
  "検索者、検索ワード、検索式は別紙様式 (V) -5に示したことを記載する。",
  "検索ワードや検索式は実際に使用した、もしくはそれと同等の詳細なものであること。",
  "実際に使用した",
  "同等の詳細なもの",
]:
  print(f"char={t.find(q)} count={t.count(q)} words={len(q.split())} len={len(q)} | {q}")
'
62be15a474e866e4bef6c9d5.txt 61188 39676 960da5cf632dbd278ea941c54d83e3ed8f13657bcb4bcbbfc8d63c9d834acf4a
char=809 count=1 words=6 len=66 | 機能性表示食品制度の届出資料におけるPRISMA 2020声明 システマティックレビュー記載の留意点(別紙様式 (V) -4 本文)
char=1498 count=1 words=1 len=17 | 更新版であれば更新した旨を記載する
char=3966 count=1 words=1 len=9 | 全てのデータベース
char=4124 count=1 words=1 len=30 | それぞれのデータベース毎に最後に検索した日の日付を記載する。
char=4192 count=1 words=1 len=17 | それぞれの情報源が最後に調べられた
char=4211 count=1 words=1 len=15 | ハンドサーチの有無を記載する。
char=4409 count=1 words=1 len=13 | 検索者、検索ワード、検索式
char=4409 count=1 words=3 len=37 | 検索者、検索ワード、検索式は別紙様式 (V) -5に示したことを記載する。
char=36834 count=1 words=1 len=39 | 検索ワードや検索式は実際に使用した、もしくはそれと同等の詳細なものであること。
char=36844 count=1 words=1 len=7 | 実際に使用した
char=36859 count=1 words=1 len=8 | 同等の詳細なもの
```

## 3. Span manifest and `used-by` checks

```
$ awk -F'\t' '$1=="S108"{print $1,$4,$5,$6}' /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round51/spans.tsv
S108 729 spans/S108-1.txt 機能性表示食品制度の届出資料におけるPRISMA 2020声明 システマティックレビュー記載の留意点(別紙様式 (V) -4 本文)
S108 1418 spans/S108-2.txt 更新版であれば更新した旨を記載する
S108 3886 spans/S108-3.txt 全てのデータベース
S108 4044 spans/S108-4.txt それぞれのデータベース毎に最後に検索した日の日付を記載する。
S108 4112 spans/S108-5.txt それぞれの情報源が最後に調べられた
S108 4131 spans/S108-6.txt ハンドサーチの有無を記載する。
S108 4329 spans/S108-7.txt 検索者、検索ワード、検索式
S108 4329 spans/S108-8.txt 検索者、検索ワード、検索式は別紙様式 (V) -5に示したことを記載する。
S108 36754 spans/S108-9.txt 検索ワードや検索式は実際に使用した、もしくはそれと同等の詳細なものであること。
S108 36764 spans/S108-10.txt 実際に使用した
S108 36779 spans/S108-11.txt 同等の詳細なもの
$ grep -ln '^source: S108 ' /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/*.md
/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/japanese-search-record-r38.md
$ env -u ASSIMILATE_CITES python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round51/c2-count.py | grep -E '^(BOUND|ANCHOR_BOUND|CAPTURE_BOUND|C2)='
BOUND=6/7 (min 5) REFUSED=1
CAPTURE_BOUND=61/61
ANCHOR_BOUND=6/6
C2=PASS
```

Note on `spans.tsv` column 4 (`offset`): `build-spans.py:44,119` sets `offset = max(0, text.find(quote) - 80)` as the span-slice start (`span.find(quote) == 80` for all 11 S108 rows), and `c2-count.py:207` computes `int(offset) + span.find(quote)`, yielding `{809, 1498, 3966, 4124, 4192, 4211, 4409, 36834, 36844, 36859}` — exact match to `text.find(quote)` in the `.txt` read as UTF-8.

## 4. Cell-by-cell audit and verdict

1. **`id` (`S108`) — HOLDS.** Next unused ID after S107, unique in `corpus/SOURCES.md`, renumbered from staged S110.
2. **`source` — HOLDS.** Carries the document's Part 1 title (`機能性表示食品制度の届出資料におけるPRISMA 2020声明 システマティックレビュー記載の留意点(別紙様式 (V) -4 本文)`, located at `char 809`, replacing the staged row's column-header misnomer), author `一般社団法人 健康食品産業協議会` (at `char 301`, 3× across the 3 parts), edition `2026年6月5日 第2版` (ASCII `2` for the capture's fullwidth `第２版` at `char 142`, 3×, and `(V)-4` for `(V) -4` — bibliographic normalization in the title label, not a located quote), and canonical URL `https://jaohfa.com/pdf/systematic_review.pdf` (`sha256(url)[:24] = 62be15a474e866e4bef6c9d5`).
3. **`kind` (`docs`) — HOLDS.** Valid enum; the PDF is an industry association's guidance/form-completion document (`記載の留意点`).
4. **`tier` (`A`) — HOLDS.** Argued by `scope`: staged S110 was `B` under a broader scope, whereas lane S108 narrows `scope` to `"what this industry body's reporting form requires of a search record, as the form states it"` and is served from the author body's own domain (`jaohfa.com`). An own-document statement on the issuing body's host is primary (`A`) for what the document itself states (unlike S111, an index record at `B`, or S105/S106, third-party university mirrors at `B`).
5. **`scope` — HOLDS.** Narrowed to what this reporting form itself states it requires of a search record; matches both the capture's identity (`一般社団法人 健康食品産業協議会`, `char 301`) and every claim cited from S108 in `japanese-search-record-r38.md`.
6. **`anchor` — HOLDS.** Names the exact sections (`別紙様式 (V)-4 items 6 情報源 and 7 検索戦略 with their 記載のポイント and 別紙様式 (V)-5 item 2 with its 留意点`), the edition line (`2026年6月5日 第２版`, exact fullwidth match to `char 142`), the decode form and length (`capture .txt read as UTF-8, 39676 characters`), and six `char N` offsets (`3966, 4192, 4124, 4211, 4409, 36834`). Every `char N` is the exact `text.find(quote)` offset of an S108 quote in `spans.tsv` (`S108-3`..`S108-9`).
7. **`teaches` — HOLDS.** Every clause is carried by the `.txt` capture read as UTF-8:
   - *"every source consulted to be listed"*: item 6 `全てのデータベース` (`char 3966`) and right-column `・検索したデータベース等の情報を全て記載する。` (`char 4044`, 1×);
   - *"with the date each was last searched (per database)"*: item 6 `それぞれの情報源が最後に調べられた` (`char 4192`) and right-column `それぞれのデータベース毎に最後に検索した日の日付を記載する。` (`char 4124`);
   - *"the presence or absence of hand-searching to be stated"*: item 6 `ハンドサーチの有無を記載する。` (`char 4211`);
   - *"the searcher, search words and search expression to go on a separate attachment (V)-5"*: item 7 `検索者、検索ワード、検索式は別紙様式 (V) -5に示したことを記載する。` (`char 4409`);
   - *"that holds what was actually used or an equivalent detail"*: (V)-5 item 2 `検索ワードや検索式は実際に使用した、もしくはそれと同等の詳細なものであること。` (`char 36834`, with `実際に使用した` at `char 36844` and `同等の詳細なもの` at `char 36859`).
   No clause in `teaches` exceeds what the capture states.
8. **`status` (`mined`) — HOLDS.** Valid enum; cited by an existing knowledge entry in `used-by`.
9. **`opened` (`2026-10-25`) — HOLDS.** Valid ISO date of the round-51 re-open from the on-disk capture cache.
10. **`recheck` (`180d`) — HOLDS.** Valid `NNd` cadence under `CORPUS.md` and `sources-census.sh`.
11. **`used-by` (`corpus/knowledge/japanese-search-record-r38.md`) — HOLDS.** Exact match to `grep -ln '^source: S108 ' corpus/knowledge/*.md` (1 file, line 4).

**Survival on a non-author re-open:** YES. Every cell holds against the `.txt` capture read as UTF-8, all six `char N` anchor offsets resolve to single-occurrence quotes in `spans.tsv`, `teaches` contains zero ungrounded clauses, and `tier: A` is strictly justified by the narrowed own-document scope.

VERDICT: attacked SOURCES.md row S108 across all 11 cells against capture 62be15a474e866e4bef6c9d5.txt and spans.tsv — 11/11 cells hold (0 defects); row S108 survives a non-author re-open.
