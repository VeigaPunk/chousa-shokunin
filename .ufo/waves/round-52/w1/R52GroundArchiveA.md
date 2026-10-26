# R52GroundArchiveA — re-ground staged S129 (Japanese PRISMA 2020 checklist, Wayback copy)

Seat R52GroundArchiveA (leaf, no dispatch). Only write: this report. Scratch `/fast/scratch/hyaku/chousa-r52/R52GroundArchiveA` removed before exit. No network (L0 `8d77e6c1` open): every receipt below is a command I ran on an on-disk capture, or a read-only file under `/home/vgpnk/Projects/shokuknow/merge/chousa`.

## Capture, form, provenance

`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/e84bfe97808591d23fe3266f.{raw,pdf,txt}` (read-only).

$ C=/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/e84bfe97808591d23fe3266f
$ printf '%s' 'https://web.archive.org/web/2024/https://www.lifescience.co.jp/yk/jpt_online/prisma/list_1.pdf' | sha256sum | cut -c1-24
e84bfe97808591d23fe3266f                       # key↔URL binding holds
$ sha256sum "$C.raw" "$C.pdf"                  # both ba9bc9c14cd0b89f9de559f20b074398333c67ed86c0b5d6ffd64c0118399732
$ cd "$S" && pdftotext -layout "$C.raw" layout.txt && cmp -s layout.txt "$C.txt" && echo IDENTICAL
IDENTICAL                                      # poppler 26.08.0; plain pdftotext differs (302 lines)
$ python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/capture-text.py "$C.raw" ; echo exit=$?
REFUSED not a zip (an OOXML capture is a zip package)
exit=2                                         # correct: this is a PDF, not OOXML
$ grep -aoi -E 'wayback|web\.archive|archive\.org' "$C.raw" | wc -l
0                                              # no archive marker in the raw bytes
```

**Form named for every offset below: the `.txt` read as UTF-8 — 5328 characters, 101 lines** (a faithful `pdftotext -layout` dump of the 1-page PDF). Extraction completeness: the dump's digit set is exactly `1..27` plus `2020` (2×), so items 1–27 with 10a/10b/13a–f/16a–b/20a–d/23a–d/24a–c are all present.

## Located quotes (each occurs exactly once in the `.txt`; offsets by `text.find`)

| # | offset | len | quote (byte-exact) |
|---|---|---|---|
| q1 | 0 | 19 | `PRISMA 2020 チェックリスト` |
| q2 | 200 | 30 | `PRISMA 2020 抄録チェックリストを参照（表 2）。` |
| q3 | 475 | 56 | `すべてのデータベース，研究登録，Web サイト，組織，文献リスト，研究を特定するために調べたり，助言を求めた情報` |
| q4 | 592 | 25 | `それぞれの情報源が最後に調べられた日付を記載する。` |
| q5 | 641 | 15 | `用いたフィルターや制限も含め，` |
| q6 | 753 | 26 | `試験登録，Web サイトの完全な検索戦略を記載する。` |
| q7 | 824 | 20 | `レビューアの数，独立して作業したかどうか` |
| q8 | 991 | 22 | `各報告からデータを収集したレビュー担当者の数` |

q3+q4 = 項目6 情報源 (list…`調べたり，助言を求めた情報源を記載する。`), q5+q6 = 項目7 検索戦略, q7 = 項目8 screeners, q8 = 項目9 data collectors — the two person-roles the checklist *does* name, the contrast for the searcher sweep. q1 is the only title-like line: no masthead, URL or footer anywhere in the dump.

## The seat's three questions

1. **Searcher named?** No. `検索者=0 誰が=0 検索した=0`. `検索` appears 4× and only as 検索戦略 (619, 769) and 項目16a `検索で特定した記録数…検索と選択プロセス` (3111, 3155). Persons occur only as roles: `レビューア=2` (824, 1838), `レビュー担当者=1` (1004), `レビュー著者=1` (5107). "No searcher" is true; "no person" would be false.
2. **Date-of-search wording.** 項目6 = q4 (592). Verb is **`調べられた=1`**, not `検索された=0`: the Japanese collapses EN "searched or consulted" into *consulted/examined*; `最後に=1` (only here) gives "last". The staged "was last searched" is a gloss over `最後に調べられた`.
3. **Identity.** Title = q1. Publisher, translator, date, version are **absent from the text**: `ライフサイエンス=0 株式会社=0 JPT=0 ONLINE=0 版=0 バージョン=0 訳=0 日本語=0`; the only year in the text is `2020` (2×). No Wayback marker in the text (`Wayback=0 web.archive=0`) nor in the raw bytes (`grep -aoi -E 'wayback|web\.archive|archive\.org' *.raw` → no output). The PDF's own metadata is the only date-ish evidence: `Title: 表1`, `Creator: Adobe Illustrator 24.3 (Macintosh)`, `Producer: Adobe PDF library 15.00`, `CreationDate/ModDate 2023-09-19 14:06+09:00` — an authoring stamp on the artwork, not a version/revision date and not a snapshot time.

## The staged recheck sentence is NOT byte-exact

Staged (entry L6 and the row's recheck cell): `用いたフィルターや制限も含め，すべてのデータベース，試験登録，Webサイトの完全な検索戦略を記載する`.

```
$ T=/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/e84bfe97808591d23fe3266f.txt
$ S='用いたフィルターや制限も含め，すべてのデータベース，試験登録，Webサイトの完全な検索戦略を記載する'
$ python3 - "$T" "$S" <<'PY'
import sys
t = open(sys.argv[1], encoding="utf-8").read(); s = sys.argv[2]
a = t.find("用いたフィルターや制限も含め，"); b = t.find("記載する。", a) + 5
print("count=%d find=%d span=%d..%d collapsed_equal=%s" % (t.count(s), t.find(s), a, b, "".join(t[a:b].split()) == "".join(s.split())))
PY
count=0 find=-1 span=641..779 collapsed_equal=False
$ grep -ao '、' "$T" | wc -l ; grep -ao '，' "$T" | wc -l
0
55
```

Capture span 641..779 = `用いたフィルターや制限も含め，\n<37 spaces>すべてのデータベース，\n<47 spaces>試験登録，Web サイトの完全な検索戦略を記載する。`. Whitespace-collapsed the two forms still differ (capture len 51 vs staged 50; capture tail `。`, staged none). So the failures are layout and one space, not punctuation: **the comma is `，` (fullwidth) in both, and `、` never occurs in the capture (0/55)**; (a) two line breaks with 37- and 47-space indents, the second *before* `試験登録`; (b) an ASCII space inside `Web サイト` (staged `Webサイト`); (c) staged drops the terminal `。`. A `recheck` phrased "confirm 項目7 still reads ⟨that⟩" can never pass a byte-exact check. Remedy: anchor on **q6, offset 753, count 1**.

## Staged entry `corpus/knowledge/japanese-prisma-item-wording-r40.md` (read at the staged path)

| staged | sentence | verdict |
|---|---|---|
| L2 | headline "PRISMA 2020's own Japanese wording names no searcher" | **NARROW** — true of the searcher (sweeps), but these bytes are a translation with no masthead; "PRISMA 2020's own" overstates q1. |
| L4 | `source:` archive URL | **SUPPORTED** as locator (key↔URL, digests); publisher attribution is not in the bytes (`ライフサイエンス=0 JPT=0 ONLINE=0`). |
| L6 | `recheck:` quote + "confirm 項目7 still reads …" | **NARROW — fails as written**; use q6 (753). |
| L11–15 | "reachable through an archive … serves it in full" | **SUPPORTED** on disk (1 page, 5328 chars extracted). The "HTTP 000 three rounds" history is **unverifiable offline**. |
| L16–19 | "Item 6 names the sources and the date … last searched" | **SUPPORTED** (q3+q4); **NARROW** twice: `調べたり，助言を求めた` = "consulted **or sought advice**" (entry drops the advice clause); `最後に調べられた` ≠ "last searched". |
| L20–22 | "Item 7 … complete strategy … filters and limits" | **SUPPORTED** (q5 641, q6 753). |
| L23–24 | "the term 検索者 does not occur anywhere in the extracted text" | **SUPPORTED** — `検索者=0` over all 5328 chars; keep the words "extracted text" (the claim is about the dump). |
| L28–35 | "items name sources, dates, strategy; not the person who searched" | **SUPPORTED** (q3–q6 + sweeps). The S097 comparison is another document. |
| L36–43, L58–59 | "three literatures agree …"; the Chinese half | **OUT OF SCOPE** — S097, the NIPH form, PRISMA-S and the two Chinese pages need their own captures. |
| L52–54 | "The Wayback capture is from 2024" | **NARROW** — no snapshot time in the bytes (`Wayback=0`, years only 2020) and none in the raw; `2024` is the URL's *bucket* (`/web/2024/` = nearest snapshot to 2024), not a measurement. PDF CreationDate is 2023-09-19. |

## Staged row S129 (`SOURCES.append.md:54`, read at the staged path)

- `「PRISMA 2020 チェックリスト」（日本語訳, JPT ONLINE, ライフサイエンス株式会社）`: title **SUPPORTED** (q1); `日本語訳` **NARROW** (`訳=0 日本語=0` — inferred from the row, not the file); `JPT ONLINE` **NARROW** (only the URL path `/yk/jpt_online/`); `ライフサイエンス株式会社` **NARROW** (only the host `lifescience.co.jp`).
- `**original withdrawn**`: **UNVERIFIABLE THIS ROUND** — no fetch permitted (L0 open), so no sweep can produce a count. Neither confirmed nor falsified.
- `archived at …` and the cell `archived PDF text extracted with pdftotext, read 2026-10-23`: **SUPPORTED**, reproduced byte-identically (`cmp` IDENTICAL); capture mtime `Oct 23 21:20` agrees with that read date.
- Cell "names every information source … date each was last searched": **SUPPORTED** (q3, q4) with the two glosses above. Cell "complete search strategy … filters and limits used": **SUPPORTED** (q5, q6).
- Cell "the term 検索者 does not occur anywhere in the document": **SUPPORTED** for the extraction — scope it to the extracted text as the entry does. Cell `confirm 項目7 still reads ⟨sentence⟩`: **NARROW**, byte-exact count 0; use q6.
- Cell "**the official** Japanese translation": **NARROW** — "official" occurs nowhere in the bytes (`訳=0`, no publisher string); it is registry attestation, so it belongs to the row's attribution and not to a quoted observation of the document.

## Ids, and the QUOTE machine lines (entry `corpus/knowledge/japanese-prisma-item-wording-r40.md`)

Registry max is S112 (`grep -oE '^\| S[0-9]{3} ' corpus/SOURCES.md | tail` → S110, S111, S112); S113–S118 have no row. Planned lane id for staged S129 is **S116**; never carry `S129` into the lane. The lines below use the *staged* id as the format requires — substitute `S116` on integration.

```
QUOTE	S129	https://web.archive.org/web/2024/https://www.lifescience.co.jp/yk/jpt_online/prisma/list_1.pdf	PRISMA 2020 チェックリスト	corpus/knowledge/japanese-prisma-item-wording-r40.md
QUOTE	S129	https://web.archive.org/web/2024/https://www.lifescience.co.jp/yk/jpt_online/prisma/list_1.pdf	PRISMA 2020 抄録チェックリストを参照（表 2）。	corpus/knowledge/japanese-prisma-item-wording-r40.md
QUOTE	S129	https://web.archive.org/web/2024/https://www.lifescience.co.jp/yk/jpt_online/prisma/list_1.pdf	すべてのデータベース，研究登録，Web サイト，組織，文献リスト，研究を特定するために調べたり，助言を求めた情報	corpus/knowledge/japanese-prisma-item-wording-r40.md
QUOTE	S129	https://web.archive.org/web/2024/https://www.lifescience.co.jp/yk/jpt_online/prisma/list_1.pdf	それぞれの情報源が最後に調べられた日付を記載する。	corpus/knowledge/japanese-prisma-item-wording-r40.md
QUOTE	S129	https://web.archive.org/web/2024/https://www.lifescience.co.jp/yk/jpt_online/prisma/list_1.pdf	用いたフィルターや制限も含め，	corpus/knowledge/japanese-prisma-item-wording-r40.md
QUOTE	S129	https://web.archive.org/web/2024/https://www.lifescience.co.jp/yk/jpt_online/prisma/list_1.pdf	試験登録，Web サイトの完全な検索戦略を記載する。	corpus/knowledge/japanese-prisma-item-wording-r40.md
QUOTE	S129	https://web.archive.org/web/2024/https://www.lifescience.co.jp/yk/jpt_online/prisma/list_1.pdf	レビューアの数，独立して作業したかどうか	corpus/knowledge/japanese-prisma-item-wording-r40.md
QUOTE	S129	https://web.archive.org/web/2024/https://www.lifescience.co.jp/yk/jpt_online/prisma/list_1.pdf	各報告からデータを収集したレビュー担当者の数	corpus/knowledge/japanese-prisma-item-wording-r40.md
```

## Left for the L1 (drafted here, not written to the lane)

QUALITY 30 asks Gate quotes be re-opened with `tools/quote-reopen.py verify --items`; that tool fetches the registry URL, so it **cannot run this round** (no network). Items file I would hand it, intended path `.ufo/waves/round-52/w1/s129-items.tsv`, header `id<TAB>source_id<TAB>quote` plus `S129q1…S129q8` in q1–q8 order, for the first round that re-fetches. Until then the receipts above are the verification: each quote is byte-exact, single-occurrence and form-named (QUALITY 30, 76).

Named limits: completeness rests on the 1-page PDF's text layer (a vector-outlined glyph would be invisible to it); `original withdrawn` and any snapshot date stay unverified offline; PDF metadata dates the file, not the checklist revision.

VERDICT: re-grounded S129 from the Wayback PDF dump — 8 byte-exact single-occurrence quotes with offsets in a named form; the searcher is absent (`検索者=0`), the date-of-search wording is `最後に調べられた`; the staged recheck sentence is **not** byte-exact (line breaks, the `Web サイト` space, a dropped `。`), and "official", the publisher name, `日本語訳` and "capture is from 2024" are NARROW.
