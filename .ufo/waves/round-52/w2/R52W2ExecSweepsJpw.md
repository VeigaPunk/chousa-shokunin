# R52W2ExecSweepsJpw — falsify: the S116 entry's sweeps re-run, and the grounding gate's CJK blind spot

What I attacked: (1) every command and every negative claim in `corpus/knowledge/japanese-prisma-item-wording-r40.md`; (2) the `char N`/span linkage the entry's offsets rest on (`spans.tsv`, `spans/S116-1..9.txt`); (3) `tools/inference-ground.py` against three mutated copies of the entry's Inference section. Lane tip `e769c03` (base `00f8c7f5272a1d98b6d34913985fa4537e00aaf9`). Scratch `/fast/scratch/hyaku/chousa-r52/R52W2ExecSweepsJpw`, `TMPDIR` set there. No tool installed (none needed; pacman untouched). No network, no fetch. No production write; this report is the only lane write. **Labrat: not dispatched** — no `task`/spawn tool is mounted in this seat, recorded rather than faked.

## 1. The `recheck:` command, run verbatim from the lane root — REPRODUCES

```
$ QCACHE=/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache; python3 -c "import sys;t=open(sys.argv[1],encoding='utf-8').read();print(len(t),[t.count(q) for q in ('検索者','検索担当者','司書','誰が')],[t.find(q) for q in ('すべてのデータベース，研究登録，Web サイト，組織，文献リスト','研究を特定するために調べたり，助言を求めた情報','それぞれの情報源が最後に調べられた日付を記載する','用いたフィルターや制限も含め，','試験登録，Web サイトの完全な検索戦略を記載する','完全な検索戦略','スクリーニングしたレビューアの数','データを収集したレビュー担当者の数')])" "$QCACHE"/e84bfe97808591d23fe3266f.txt
5328 [0, 0, 0, 0] [475, 508, 592, 641, 753, 766, 815, 996]
```
Same length, same four zeros, same eight offsets as the entry prints. The recheck's second clause (`then re-fetch the archived PDF and confirm 項目7 still asks …`) is **not runnable as written here**: network is forbidden by my boundary and L0 `8d77e6c1` is open. I re-derived the form on disk instead (§2, §3) and the 完全な検索戦略 requirement still holds in it.

## 2. `verified-at` identity claims — all REPRODUCE

```
$ sha256sum $QCACHE/e84bfe97808591d23fe3266f.txt $QCACHE/e84bfe97808591d23fe3266f.raw
93558b6d4b0e7a6b76d37954f7cfced59847c2f34454dc887677b560730ab155  …/e84bfe97808591d23fe3266f.txt
ba9bc9c14cd0b89f9de559f20b074398333c67ed86c0b5d6ffd64c0118399732  …/e84bfe97808591d23fe3266f.raw
$ wc -c …e84bfe97808591d23fe3266f.txt …e84bfe97808591d23fe3266f.raw
 10106 …e84bfe97808591d23fe3266f.txt
343301 …e84bfe97808591d23fe3266f.raw
$ pdftotext -layout $QCACHE/e84bfe97808591d23fe3266f.raw repro.txt && sha256sum repro.txt && cmp repro.txt $QCACHE/e84bfe97808591d23fe3266f.txt
93558b6d4b0e7a6b76d37954f7cfced59847c2f34454dc887677b560730ab155  repro.txt
BYTE-IDENTICAL
$ pdfinfo $QCACHE/e84bfe97808591d23fe3266f.raw
Title: 表1 · CreationDate: Tue Sep 19 02:06:00 2023 -03 · Pages: 1 · Page size: 595.275 x 841.89 pts (A4)
  · File size: 343301 bytes · (no Edition field printed)
$ cat $QCACHE/f3dbe2fe59a684b1b94cfadc.fail; wc -c …
rc=28
6
$ python3 -c 'import hashlib;[print(k,hashlib.sha256(u.encode()).hexdigest()[:24]) for k,u in …]'
arch24 e84bfe97808591d23fe3266f · orig f3dbe2fe59a684b1b94cfadc · memento c280fdf897ab0d488017b63a
```
So: 5,328 chars / `93558b6d…`; 343,301 bytes / `ba9bc9c1…`; `pdftotext -layout` byte-identical in both directions; one A4 page, Title 表1, CreationDate 2023-09-19, no Edition key; the `sha256(url)[:24]` key rule holds for all three URLs the entry names; the original URL's only file is the 6-byte `rc=28` marker. **Reproduces.**

## 3. Every `char N` in the entry, re-located with `text.find` in the `.txt` form — all REPRODUCE

| stated | phrase (shortened) | `count` | `find` |
|---|---|---|---|
| char 0 | `PRISMA 2020 チェックリスト` | 1 | 0 |
| char 225 | `表 2` | 1 | 225 |
| char 453 | `情報源` (item 6 label; 2nd at 597) | – | 453 |
| char 475 | `すべてのデータベース，研究登録，Web サイト，組織，文献リスト` | 1 | 475 |
| char 508 | `研究を特定するために調べたり，助言を求めた情報` | 1 | 508 |
| char 555 | `源を記載する。` | 1 | 555 |
| char 592 | `それぞれの情報源が最後に調べられた日付を記載する` | 1 | 592 |
| char 619 | `検索戦略` (item 7 label; 2nd at 769) | – | 619 |
| char 641 | `用いたフィルターや制限も含め，` | 1 | 641 |
| char 694 | 2nd `すべてのデータベース` (`データベース` at 698) | – | 694 |
| char 753 | `試験登録，Web サイトの完全な検索戦略を記載する` | 1 | 753 |
| char 766 | `完全な検索戦略` | 1 | 766 |
| char 815 | `スクリーニングしたレビューアの数` | 1 | 815 |
| char 996 | `データを収集したレビュー担当者の数` | 1 | 996 |

The two label offsets (453, 619) point at the row-label occurrence, the two later occurrences being 597 (`それぞれの情報源…` contains `情報源`) and 769 (`Web サイトの完全な検索戦略`); both stated numbers are exact starts. Context checks the rows are what the entry says they are: `t[200:260]` = `PRISMA 2020 抄録チェックリストを参照（表 2）。` (item 2), `t[780:1010]` shows `選択プロセス 8 …スクリーニングしたレビューアの数…` and `データの収集プロセス 9 …データを収集したレビュー担当者…`. One item-number census, attacking "running from item 1 to item 27": parent rows found 1–9, 11, 12, 14, 15, 17, 18, 19, 21, 22, 25, 26, 27 plus sub-lettered 10a/b, 13a–f, 16a/b, 20a–d, 23a–d, 24a–c, i.e. **all 27 present**; item 27 closes the text at `t[-200:]`.

## 4. Every negative statement in Observation — holds

- `出版`, `年`, `版`, `http` → `0, 0, 0, 0` (four-term sweep re-run above and again here); no `\d{4}` in the text except `2020` ×2 (title). "no publisher, date, edition or URL line" holds on the text form; `pdfinfo` likewise prints no Edition field.
- `組織` = 1 and `文献リスト` = 1 in the whole text form, `0` inside item 7's row `t[619:781]` = `検索戦略 … 用いたフィルターや制限も含め，/ すべてのデータベース，/ 試験登録，Web サイトの完全な検索戦略を記載する。`. "Organisations and reference lists … are absent from item 7's list" holds, and item 6's five classes are the five listed.
- "which this one-page copy does not carry" (the abstract checklist): `Pages: 1`; `表 2` occurs once, only as the item-2 cross-reference; `抄録チェックリスト` occurs once, inside that cross-reference; no second table header in the text.
- searcher sweep `検索者 / 検索担当者 / 司書 / 誰が` → `0 / 0 / 0 / 0`.

## 5. The two negatives widened, five synonyms each (capture's language) — both narrowed wordings still hold

- **Searcher field absent.** Added `検索実施者`, `検索の実施者`, `図書館員`, `情報専門家`, `検索協力者` → each `0`; total with the entry's four terms: nine searcher terms, zero hits. The one hit for bare `担当者` (`t.count('担当者')` = 1 at char 1008) is inside `レビュー担当者`, the item-9 data-collection reviewer count the entry already calls a reviewer count, not a searcher. **Holds.**
- **Item 7 omits organisations and reference lists.** Added `団体`, `機関`, `協会`, `学会`, `企業` and `参考文献`, `引用文献`, `文献目録`, `参照文献`, `リファレンス` → every one `0` in item 7's row **and** `0` in the whole 5,328-char form. **Holds**, and the absence is document-wide, not merely out of that row.

## 6. `#### Unknown` — every locatable claim checked

- Same-memento claim: `c280fdf897ab0d488017b63a.raw` sha256 = `ba9bc9c14cd0b89f9de559f20b074398333c67ed86c0b5d6ffd64c0118399732`, 343,301 bytes, identical to this capture's; its `.txt` is also `93558b6d…`. `grep -c c280fdf897ab0d488017b63a corpus/SOURCES.md` → `0`, `grep -c 20260418151432` → `0`, so "that memento is not a lane row" holds.
- `pdfinfo` "no edition field" → confirmed (no `Edition` key in the listing above).
- "records at char 13710 of its first source capture": in `.qcache/7194acc65a18f6555e4b8893.txt` (21,216 chars, sha256 `05c7ee9fe9e55461…`) `このプロセスに際して，誰が検索を行ったの` → `count 1 find 13710`. Holds, and the ground's path `corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md` exists (8,451 bytes).
- English/Chinese "not opened here" bullets: the entry carries exactly one `source:` line (S116), so no other document is claimed by it — consistent, and not falsifiable by command (absence of work). No contrary lane claim found in the entry.

## 7. The gate on the entry — PASS, and the manifest/char linkage is consistent

```
$ python3 tools/inference-ground.py --entry corpus/knowledge/japanese-prisma-item-wording-r40.md \
    --spans corpus/evidence/round52/spans.tsv --counts /dev/null \
    --registry corpus/SOURCES.md --root .
GROUND entry=corpus/knowledge/japanese-prisma-item-wording-r40.md section=1 bullets=3 tokens=7 grounded=7
GROUND: PASS          (EXIT=0)
```
Tokens per bullet, read back through the tool's own `grounding_tokens`: b1 4 CJK phrases, b2 2, b3 1 (`スクリーニングしたレビューアの数`) — b3's four searcher terms are unbackticked prose, so the load-bearing negative carries no grounding token of its own. I also cleared a false alarm I raised: `spans.tsv`'s `offset` is the **span** start, not the quote start, so `395` for a quote at `475` is `475−80` by design (docstring: "`offset` is the span's start"); for all nine S116 rows `form[offset:offset+len(span)] == spans/S116-n.txt` and `offset + span.find(quote)` equals the entry's stated char (475, 508, 555, 592, 641, 753, 815, 996 and 0). Manifest and entry agree.

## 8. Mutation — negating an Inference bullet: the tool does **not** catch it

Three single-line mutations of a scratch copy (`mut/m1..m3.md`, `diff` shown against the lane file), each run with the §7 command:

- **m1** b3 claim flipped: `A searcher field cannot be sourced from this copy.` → `… can be sourced …` → `GROUND: PASS EXIT=0`.
- **m2** b2 claim flipped: `organisations and reference lists therefore belong under the source list and its dates, not under the strategy list` → `… therefore do not belong under the source list and its dates, but under the strategy list` → `PASS`.
- **m3** b1 affirmed quote negated in place: `item 7 as the `完全な検索戦略`` → `item 7 as not the `完全な検索戦略`` → `PASS`.

Mechanism, read out of the code and executed: `WORDS_RE = re.compile(r"[a-z][a-z'\u2019]*")` (line 253) tokenizes Latin only, so
```
words('完全な検索戦略') == []        content(words(...)) == []
phrase_polarity('完全な検索戦略', spans_S116_1..9) == (False, [])
polarity_flips('and item 7 as not the `完全な検索戦略` …', '完全な検索戦略', spans) == []
phrase_polarity('PRISMA 2020', same spans) == (False, ['prisma'])
polarity_flips('the copy is not PRISMA 2020 at all', 'PRISMA 2020', spans) == ['prisma']   # Latin control fires
```
`stem`-set is empty for a CJK phrase, so `polarity_flips` takes its `if not stems: return []` exit: the round-47 `INF_POLARITY_FLIP` leg is **inert on every CJK-only quote**, which is all this entry's quotes and all of round 52's three entries. It is a *disclosed* limit, not a silent one — `has_two_words`' round-50 comment says "words() is Latin-only, so a CJK phrase never trips the polarity check", and criterion 79 repeats it — but the operational consequence is what the mutation shows: a reader who inverts b1, b2 or b3 of this entry passes the gate with exit 0, and no other counter covers a bullet's own semantics. That is a real gap in the gate's reach over this lane's material, not a defect in the entry or in `spans.tsv`.

## 9. Housekeeping

Scratch removed at the end (`rm -rf /fast/scratch/hyaku/chousa-r52/R52W2ExecSweepsJpw`, verified gone); nothing written outside it and this report. No git/jj command run except read-only `git log`/`git log -S` against the lane. Receipts cited above are pasted here; no ephemeral file is relied on.

**VERDICT: I attacked the R40/S116 entry's `recheck:` command, `verified-at` identity, all 14 stated offsets, all four negative statements and the four `Unknown` bullets (every one reproduces or holds; the re-fetch half is not runnable offline; two negatives survive five synonyms each; the manifest/char arithmetic agrees), and `tools/inference-ground.py` against three negated Inference bullets (all three PASS at exit 0 — the polarity leg is Latin-only by regex, so it is inert on this entry's CJK quotes, a disclosed limit with the consequence that bullet-level inversion is unflagged).**
