# R52W2ReopenRowS116 — attack on Registry row S116 (archived Japanese PRISMA 2020 table)

Seat: R52W2ReopenRowS116. Attacked: the `S116` row of `corpus/SOURCES.md:126` — re-opened its
capture from the campaign cache myself (non-author), checked every cell, and cross-checked the citing
entry `corpus/knowledge/japanese-prisma-item-wording-r40.md` and the frozen C2 predicate
(`corpus/evidence/round52/claims.md:69-97`). No frozen predicate, counter, control or target is
proposed for change; no file outside this report was written.

## 1. Capture re-open (independent of the row)

Files (read-only): `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/e84bfe97808591d23fe3266f.txt` (key `e84bfe97808591d23fe3266f` = sha256(url)[:24]), plus `.raw`/`.pdf`.

```
$ sha256sum .../e84bfe97808591d23fe3266f{.txt,.raw}
93558b6d4b0e7a6b76d37954f7cfced59847c2f34454dc887677b560730ab155  ...e84bfe97808591d23fe3266f.txt
ba9bc9c14cd0b89f9de559f20b074398333c67ed86c0b5d6ffd64c0118399732  ...e84bfe97808591d23fe3266f.raw
$ pdftotext -layout .../e84bfe97808591d23fe3266f.raw reextract.txt && cmp reextract.txt .../e84bfe97808591d23fe3266f.txt && echo CMP_IDENTICAL
CMP_IDENTICAL        # both 10,106 bytes; text form = the PDF's own layout text
$ pdfinfo .../e84bfe97808591d23fe3266f.raw | grep -E 'Title|Pages|CreationDate'
Title:           表1
CreationDate:    Tue Sep 19 02:06:00 2023 -03
Pages:           1
$ python3 -c "import pathlib;t=pathlib.Path('.../e84bfe97808591d23fe3266f.txt').read_text('utf-8');print(len(t),t.count('出版'),t.count('年'),t.count('版'),t.count('http'))"
5328 0 0 0 0
```

Original URL `https://www.lifescience.co.jp/yk/jpt_online/prisma/list_1.pdf` → key `f3dbe2fe59a684b1b94cfadc`: only `f3dbe2fe59a684b1b94cfadc.fail`, 6 bytes, content `rc=28` (no `.txt`/`.raw`). Memento key `c280fdf897ab0d488017b63a` (2026-04-18): `.raw` sha == the same `ba9bc9c1…`.

## 2. Cell verdicts (row = SOURCES.md:126)

| cell | verdict | evidence |
|---|---|---|
| source title/URL | HOLDS | Title `PRISMA 2020 チェックリスト` is capture line 1 (char 0, count=1). First source-cell URL is the document (archive copy); `key(archive)==e84bfe…` matches the cache files. `出版`/`年`/`版`/`http` each 0× → "names no publisher, date or edition". Original-URL parenthetical matches the `rc=28` fail marker. |
| kind | HOLDS | One-page checklist table (pdfinfo Pages 1; three-column 大項目/番号/チェックリスト項目 table, items 1–27); `docs` matches the registry's vocabulary for copied documents. |
| tier | HOLDS (argued) | A is only where the page is primary for what the row scopes. The scope is the wording of PRISMA 2020's items *as this archived anonymous copy renders it*: the canonical statement lives elsewhere (S017), this copy names no publisher/date/edition, its original is unreachable — so it is a derivative rendering, correctly B, not primary authority for the checklist items. |
| scope | HOLDS | Labels `情報源` (find 453) and `検索戦略` (find 619) are in the capture; items 6/7 rows render the wording; no publisher/date/edition/URL line (0-counts above). |
| anchor | HOLDS | Every listed `char N` is the offset of a quote of this id that occurs exactly once: 475 = `すべてのデータベース，研究登録，Web サイト，組織，文献リスト` (2 ws words); 592 = `それぞれの情報源が最後に調べられた日付を記載する` (1); 641 = `用いたフィルターや制限も含め，` (1); 753 = `試験登録，Web サイトの完全な検索戦略を記載する` (2) — all ≤25 ws words, count=1 each, `text.find` == char N. "5328 characters" == len(text). Note the spans.tsv offset column is the window start `max(0, find−80)` (build-spans.py:179), so tsv offsets {0,395,428,475,512,561,673,735,916} are 80 short of true quote offsets; the row anchors use the true offsets — consistent, and `build-spans.py --check` passes: `SPANS_ROWS=38 STALE=0` exit 0 (all 9 S116 span files are exact capture slices, `start:off+len(quote)+80`). |
| teaches | HOLDS | Every clause is carried by a located quote: item 6's five classes + advice (475, 508 `研究を特定するために調べたり，助言を求めた情報`, 555 `源を記載する。`); date each was last searched (592); item 7 filters/limits (641) and complete strategy for databases/registries/websites (753; 766 `完全な検索戦略`); reviewer counts for screening (815 `スクリーニングしたレビューアの数`) and data collection (996 `データを収集したレビュー担当者の数`); "no searcher item" — sweep `検索者`/`検索担当者`/`司書`/`誰が` → counts `[0, 0, 0, 0]`. |
| status / opened / recheck | HOLDS | `mined`; opened 2026-10-26; recheck `180d`. Row absent at base `00f8c7f5`, freeze `37468eadd`, candidate `804a4537` (`git show <rev>:corpus/SOURCES.md | grep -cE '^\| S116 '` → 0,0,0), present at landed `e769c037` (→ 1) and HEAD `d1d972cf`. claims.md contains no S11x token; erratum E1–E4 do not touch the row. |
| used-by | HOLDS | `grep -ln '^source: S116 ' corpus/knowledge/*.md` → exactly `corpus/knowledge/japanese-prisma-item-wording-r40.md`; matches the row's used-by cell, and that entry's `source:` line carries the row's first URL. |
| citing entry cross-check | HOLDS | Entry-listed offsets 475, 508, 555, 592, 641, 753, 766, 815, 996 all equal `text.find()`; line 3 sha (93558b6d…)/size (5,328) match; recheck line's sweep and find list reproduce exactly. |

## 3. Residual risk / gaps

- Whether the anonymous table is the *current* revision stays open: the second memento's identity only proves archive stability through 2026-04-18, and the original fetch is a `rc=28` failure marker — already parked in the entry's Unknown, not a row defect.
- The "no searcher item" clause is bounded to the four sweep terms and the table's visible rows (honest limit; the entry states it as such).
- No defect found in any cell; the row survives a non-author re-open. Nothing was installed (no tool changes; `pdftotext`/`pdfinfo` already present).

VERDICT: attacked Registry row S116 by re-opening its capture (key e84bfe…; sha 93558b6d…; byte-identical `pdftotext -layout` re-extraction; `rc=28` original marker; identical memento) and verifying every cell — source title/URL, kind, tier B (argued), scope, anchors 475/592/641/753 (exactly-once quote offsets), teaches (all clauses quoted; searcher sweep 0), status/opened/recheck (new since base, landed at e769c037) and used-by (exactly one entry) — all HOLDS; the row survives a non-author re-open.
