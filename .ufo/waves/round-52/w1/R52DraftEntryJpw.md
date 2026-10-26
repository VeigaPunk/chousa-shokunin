# R52DraftEntryJpw — draft of `corpus/knowledge/japanese-prisma-item-wording-r40.md`

Seat: leaf scribe, round 52 wave 1. Wrote nothing but this report; the entry text below is for the L1 to
place at its lane path. Scratch `/fast/scratch/hyaku/chousa-r52/R52DraftEntryJpw/` (removed at end).

## Behavior

Drafted the lane entry for staged `knowledge/corpus/knowledge/japanese-prisma-item-wording-r40.md`
(staged id S129 → lane S116), bound to the web-archive copy of the Japanese PRISMA 2020 checklist.
The document is BOUND, not refused: the archive URL has a `.txt` and a `.raw`; the original URL has only
a failure marker. The entry keeps the C2 NEW_GROUND term 完全な検索戦略 in a located quote (char 766).
Carried over and corrected: the staged dead-host story, the staged "amends" relation, the staged
campaign-queue ground, the staged body ids (dropped: none survive), and one staged inference that the
lane's own files already contradict (below, Findings 4).

## Evidence (commands as run; output verbatim)

1. Cache key = sha256(url)[:24], both URLs, and the three files' sizes/digests:
```
e84bfe97808591d23fe3266f https://web.archive.org/web/2024/https://www.lifescience.co.jp/yk/jpt_online/prisma/list_1.pdf
f3dbe2fe59a684b1b94cfadc https://www.lifescience.co.jp/yk/jpt_online/prisma/list_1.pdf
e84bfe97808591d23fe3266f.raw 343301 ba9bc9c14cd0b89f9de559f20b074398333c67ed86c0b5d6ffd64c0118399732
e84bfe97808591d23fe3266f.txt 10106 93558b6d4b0e7a6b76d37954f7cfced59847c2f34454dc887677b560730ab155
f3dbe2fe59a684b1b94cfadc.fail 6 2fcf2db4e495e485420923d59960bc81c5ca7fc048cefe40a7f417a04a5e8b6a
b'rc=28\n'
b'%PDF-1.6'
```
   The `.fail` file holds exactly `rc=28` plus a newline (6 bytes) and no body, no HTTP status, no date.
   It is the whole of what the original URL's cache entry contains: there is no `.txt` and no `.raw`.

2. The text form is reproducible from the `.raw` (form statement for every quote below):
```
pdftotext -layout e84bfe97808591d23fe3266f.raw "$TMPDIR/pdftotext.txt" && wc -c "$TMPDIR/pdftotext.txt"
10106 /fast/scratch/hyaku/chousa-r52/R52DraftEntryJpw/pdftotext.txt
identical True lenA 5328 lenB 5328
```
   So the form judged is `.qcache/e84bfe97808591d23fe3266f.txt` read as UTF-8: 5,328 characters, 101 lines,
   reproduced byte for byte by `pdftotext -layout` on the 343,301-byte PDF (0 U+FFFD).

3. The entry's `recheck:` command, run from the lane root, printed:
```
5328 [0, 0, 0, 0] [475, 508, 592, 641, 753, 766, 815, 996]
```
   (length, four searcher-term counts, eight quote offsets — the values the entry states.)

4. The PDF's own metadata (`pdfinfo` on the `.raw`): `Pages: 1`, `Page size: 595.275 x 841.89 pts (A4)`,
   `Title: 表1`, `CreationDate: Tue Sep 19 02:06:00 2023 -03`, no edition string.

5. Spans derived in scratch with the lane's frozen builder (not by hand), 8 rows:
```
QUOTE S116 char 475 spans/S116-1.txt
QUOTE S116 char 508 spans/S116-2.txt
QUOTE S116 char 592 spans/S116-3.txt
QUOTE S116 char 641 spans/S116-4.txt
QUOTE S116 char 753 spans/S116-5.txt
QUOTE S116 char 766 spans/S116-6.txt
QUOTE S116 char 815 spans/S116-7.txt
QUOTE S116 char 996 spans/S116-8.txt
SPANS_ROWS=8 WRITTEN=8
```
   Command: `python3 corpus/evidence/round52/build-spans.py --root "$S/root"` with a scratch
   `corpus/evidence/round52/quotes.tsv` holding the 8 rows in the block below (so the builder, not I,
   fixed the offsets; each equals the `char N` printed above).

6. Entry grounding, via the lane's criterion-66 tool against those derived spans:
```
GROUND entry=draft.md section=1 bullets=3 tokens=7 grounded=7
GROUND: PASS
rc=0
```

7. NEW_GROUND at the frozen base: `git grep -c -e 文献検索期間 / -e 完全な検索戦略 / -e 检索报告清单
   00f8c7f5272a1d98b6f34913985fa4537e00aaf9 -- corpus/knowledge` printed 0 / 0 / 0 file hits, and the
   live tree also holds 0 files with 完全な検索戦略.

8. Each of the 8 quotes: `in_capture 1`, length ≤ 32 characters, ≤ 2 whitespace words, present in the
   entry (`in_entry` 2–6). One token set in the entry: `S116` ×4, no other `S###`.

9. Lane files opened before any of them was cited by path: `corpus/knowledge/`
   `japanese-search-record-r38-amendment-2026-10-23.md` (records S112's 検索期間 / provider / database
   sentence), `japanese-search-record-r38.md` (records the 誰が検索を行ったの recommendation at char 13710),
   `chinese-search-record-r39.md` (SinoMed record and Chinese animal-experiment copy, not this checklist).
   `ls corpus/knowledge | grep -i grey` printed nothing: the staged Unknown's
   `grey-literature-and-chinese-search-record-r40.md` does not exist in this lane. Registry maximum is
   `S112` (row 122), so the planned `S116` is free.

## Draft entry — intended lane path `corpus/knowledge/japanese-prisma-item-wording-r40.md`

```markdown path=corpus/knowledge/japanese-prisma-item-wording-r40.md
# A Japanese PRISMA 2020 checklist copy asks its two search items for the sources, their last-searched dates and the complete strategy, and carries no field for the person who searched

source: S116 — https://web.archive.org/web/2024/https://www.lifescience.co.jp/yk/jpt_online/prisma/list_1.pdf — 項目6 情報源 (char 453) and 項目7 検索戦略 (char 619) of the checklist table; located quotes at char 475, char 508, char 555, char 592, char 641, char 753, char 766, char 815 and char 996; capture `.qcache/e84bfe97808591d23fe3266f.txt` read as UTF-8, 5,328 characters, sha256 `93558b6d4b0e7a6b76d37954f7cfced59847c2f34454dc887677b560730ab155`
verified-at: 2026-10-26 — the archive capture opened read-only from the campaign cache; every quote below re-located with `text.find` at the offset stated; the four-term searcher sweep printed 0 for each term; `pdftotext -layout` on the `.raw` (343,301 bytes, sha256 `ba9bc9c14cd0b89f9de559f20b074398333c67ed86c0b5d6ffd64c0118399732`) reproduced the `.txt` byte for byte (10,106 bytes both); no fetch made (L0 `8d77e6c1` open)
recheck: 180d — from the lane root: `QCACHE=/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache; python3 -c "import sys;t=open(sys.argv[1],encoding='utf-8').read();print(len(t),[t.count(q) for q in ('検索者','検索担当者','司書','誰が')],[t.find(q) for q in ('すべてのデータベース，研究登録，Web サイト，組織，文献リスト','研究を特定するために調べたり，助言を求めた情報','それぞれの情報源が最後に調べられた日付を記載する','用いたフィルターや制限も含め，','試験登録，Web サイトの完全な検索戦略を記載する','完全な検索戦略','スクリーニングしたレビューアの数','データを収集したレビュー担当者の数')])" "$QCACHE"/e84bfe97808591d23fe3266f.txt` prints `5328 [0, 0, 0, 0] [475, 508, 592, 641, 753, 766, 815, 996]` (ran 2026-10-26), then re-fetch the archived PDF and confirm 項目7 still asks for the complete search strategy (完全な検索戦略) with its filters and limits
ground: what a Japanese-language PRISMA 2020 checklist copy asks of a systematic review's two search items — the sources consulted, the date each was last searched, and the complete strategy including its filters and limits — and whether that copy carries a field for the person who ran the search; the wording judged is this copy at its web-archive URL, not a national standard, not a re-runnable strategy, and not the English or the Chinese checklist. The lane's related entry `corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md` records a society-journal methods article's three record fields (database, provider, search window); this entry records the checklist items' own wording instead, and neither amends nor replaces that entry.
adopted: round 52 from the campaign package merge/chousa/ (staged `knowledge/corpus/knowledge/japanese-prisma-item-wording-r40.md`); the staged row id and its campaign queue names are dropped and the document is bound to this lane's S116; the staged amendment relation is restated against the lane file at the path above, which the lane holds; the staged "HTTP 000 on three rounds" is replaced by what the cache's failure marker holds

#### Observation

- **The copy is one page of checklist table.** `pdfinfo` on the `.raw` reports a single A4 page and Title 表1; the text form's title line is `PRISMA 2020 チェックリスト` (char 0), and the 5,328 characters are a three-column table (大項目, 番号, チェックリスト項目) running from item 1 to item 27, with item 2 pointing to `表 2` (char 225) — the abstract checklist, which this one-page copy does not carry. The text form holds no publisher, date, edition or URL line: `出版`, `年`, `版` and `http` occur 0 times each (S116).
- **Item 6 (情報源) names five source classes and the advice taken.** `すべてのデータベース，研究登録，Web サイト，組織，文献リスト` (char 475) runs on into `研究を特定するために調べたり，助言を求めた情報` (char 508) and `源を記載する。` (char 555): every database, trial registry, website, organisation and reference list consulted to identify studies, or from which advice was sought. The next sentence adds the date: `それぞれの情報源が最後に調べられた日付を記載する` (char 592).
- **Item 7 (検索戦略) names the strategy, its filters and limits, over three source classes.** `用いたフィルターや制限も含め，` (char 641), then a second mention of the databases (char 694), then `試験登録，Web サイトの完全な検索戦略を記載する` (char 753): the complete search strategy for every database, trial registry and website, filters and limits included. Organisations and reference lists — two of item 6's five classes — are absent from item 7's list.
- **The copy counts people for two other steps.** Item 8 asks for `スクリーニングしたレビューアの数` (char 815) and whether the reviewers worked independently; item 9 asks for `データを収集したレビュー担当者の数` (char 996) and the same independence question. Both are reviewer counts for a step; neither is a search field.
- **The archive copy is the only readable capture; the original URL holds a failure marker.** The cache key is sha256(url)[:24]: the archive URL maps to `e84bfe97808591d23fe3266f` (a `.txt` and a `.raw`), while the original URL maps to `f3dbe2fe59a684b1b94cfadc`, whose only file is `f3dbe2fe59a684b1b94cfadc.fail`, 6 bytes, holding `rc=28` — no `.txt` and no `.raw`.

#### Inference

- **The two search items ask for sources, their dates and a strategy, not for a searcher.** `S116` gives item 6 as `すべてのデータベース，研究登録，Web サイト，組織，文献リスト` with `それぞれの情報源が最後に調べられた日付を記載する`, and item 7 as the `完全な検索戦略` with `用いたフィルターや制限も含め，`: what was searched, when each source was last searched and how, with no slot for who ran the search.
- **Item 6 is the wider list, so a record keyed to item 7 alone omits two source classes.** Item 6 names five classes (`すべてのデータベース，研究登録，Web サイト，組織，文献リスト`), while item 7's list is `試験登録，Web サイトの完全な検索戦略を記載する` after a second mention of the databases; organisations and reference lists therefore belong under the source list and its dates, not under the strategy list (`S116`).
- **A searcher field cannot be sourced from this copy.** Where the copy does name people it counts reviewers (`スクリーニングしたレビューアの数`), and the sweep for 検索者, 検索担当者, 司書 and 誰が returns 0 in the text form, so a row that records who searched rests on another document, and this copy is evidence only that the field is not one of its items (`S116`).

#### Unknown

- **Whether this archived copy is the current revision.** The text form carries no publisher, date, edition or URL line, and `pdfinfo`'s listing of the `.raw` gives Title 表1 and CreationDate 2023-09-19 with no edition field; the archive URL fixes the year 2024 only, so a later revision of the checklist would not appear here, and the original URL holds a `rc=28` failure marker instead of a body.
- **Whether the Japanese table matches the English PRISMA 2020 checklist item for item.** The English checklist was not opened for this entry; the wording judged is the Japanese table's.
- **Whether a searcher field attaches to the Japanese checklist in any form.** This copy has none; the lane's `corpus/knowledge/japanese-search-record-r38.md` records at char 13710 of its first source capture a Japanese society journal's recommendation to record who conducted the search, so which document a reviewer should cite for that field stays open.
- **The Chinese checklist's wording is not in this entry.** No Chinese PRISMA 2020 checklist was opened here; the lane's `corpus/knowledge/chinese-search-record-r39.md` holds a SinoMed record and a Chinese animal-experiment reporting copy, not this checklist's items.
```

## Integration inputs for the L1

### `corpus/evidence/round52/quotes.tsv` rows to append (header `id url quote entry`)

```tsv path=corpus/evidence/round52/quotes.tsv
S116	https://web.archive.org/web/2024/https://www.lifescience.co.jp/yk/jpt_online/prisma/list_1.pdf	すべてのデータベース，研究登録，Web サイト，組織，文献リスト	corpus/knowledge/japanese-prisma-item-wording-r40.md
S116	https://web.archive.org/web/2024/https://www.lifescience.co.jp/yk/jpt_online/prisma/list_1.pdf	研究を特定するために調べたり，助言を求めた情報	corpus/knowledge/japanese-prisma-item-wording-r40.md
S116	https://web.archive.org/web/2024/https://www.lifescience.co.jp/yk/jpt_online/prisma/list_1.pdf	それぞれの情報源が最後に調べられた日付を記載する	corpus/knowledge/japanese-prisma-item-wording-r40.md
S116	https://web.archive.org/web/2024/https://www.lifescience.co.jp/yk/jpt_online/prisma/list_1.pdf	用いたフィルターや制限も含め，	corpus/knowledge/japanese-prisma-item-wording-r40.md
S116	https://web.archive.org/web/2024/https://www.lifescience.co.jp/yk/jpt_online/prisma/list_1.pdf	試験登録，Web サイトの完全な検索戦略を記載する	corpus/knowledge/japanese-prisma-item-wording-r40.md
S116	https://web.archive.org/web/2024/https://www.lifescience.co.jp/yk/jpt_online/prisma/list_1.pdf	完全な検索戦略	corpus/knowledge/japanese-prisma-item-wording-r40.md
S116	https://web.archive.org/web/2024/https://www.lifescience.co.jp/yk/jpt_online/prisma/list_1.pdf	スクリーニングしたレビューアの数	corpus/knowledge/japanese-prisma-item-wording-r40.md
S116	https://web.archive.org/web/2024/https://www.lifescience.co.jp/yk/jpt_online/prisma/list_1.pdf	データを収集したレビュー担当者の数	corpus/knowledge/japanese-prisma-item-wording-r40.md
```

Then `python3 corpus/evidence/round52/build-spans.py` must print the eight `QUOTE S116 char N` lines in
Evidence 5; every one of the eight quotes also has to appear in `corpus/lessons/round-52.md` (the C2
predicate reads the lesson too).

### Registry row S116 (L1 writes; not written here)

Frozen C2 requires: exactly one row whose FIRST source-cell URL is
`https://web.archive.org/web/2024/https://www.lifescience.co.jp/yk/jpt_online/prisma/list_1.pdf`, the row
new since `00f8c7f5`, status `mined`, opened `2026-10-26`, `used-by` naming exactly this entry, and an
`anchor` cell whose `char N` values are offsets of quotes of S116 — use `475`, `592`, `641`, `753`, `766`,
`815`, `996` (each is a `QUOTE S116 char N` value above). The dead original
`https://www.lifescience.co.jp/yk/jpt_online/prisma/list_1.pdf` belongs in the row text only as the
withdrawn pointer; the entry's `source:` line already carries the archive URL.

## Gates run

- `tools/inference-ground.py`: `GROUND: PASS`, rc 0, 3 Inference bullets, 7/7 tokens grounded.
- `build-spans.py` (scratch root): 8/8 rows written, no refusal, char values as listed.
- Quote discipline: each quote occurs exactly once in the `.txt` form, ≤25 whitespace words, ≤160 chars.
- Id discipline in the entry: only `S116`; no staged id and no other lane id.
- NEW_GROUND: 完全な検索戦略 present in the entry, absent from `corpus/knowledge` at the frozen base.

Not run here (L1's land): the frozen `c2-count.py` / `c1-count.py` (they need the three entry files and the
round-52 lesson), and any write into `corpus/`.

## Findings

1. **The staged "official Japanese translation" label is not supported by this copy.** The text form holds
   no publisher, translator, date, edition or URL line (`出版`, `訳`, `年`, `版`, `ライフサイエンス`,
   `http` each 0); its only identity marks are the title line, the host path, and the PDF's metadata
   `Title: 表1`. The entry therefore says "a Japanese-language PRISMA 2020 checklist copy" and locates it
   by URL and metadata, and the ground line refuses to generalise it to a national standard.
2. **The staged "HTTP 000 with zero bytes on three consecutive rounds" is not reproducible from the cache**
   and is replaced by what the marker holds: `rc=28`, 6 bytes (Evidence 1). The entry states no HTTP status.
3. **The staged item 6 / item 7 flattening is corrected.** Item 6 names five classes (databases, trial
   registries, websites, organisations, reference lists); item 7 names three (databases, trial registries,
   websites). The entry states the asymmetry instead of paraphrasing both items the same way.
4. **The staged inference "the searcher's identity appears in the lane's corpus only in a Japanese industry
   form" is false against this lane.** `corpus/knowledge/japanese-search-record-r38.md` records a Japanese
   society journal's recommendation to record who conducted the search (char 13710 of its first capture).
   The entry asserts only that *this copy* has no searcher field, and the Unknown item points at that entry;
   the "only" claim is dropped, not re-scoped silently.
5. **Two staged pointers are dead and were replaced after opening files.** The staged ground's campaign
   queues (wave-5 Q6b, Q12) are not lane objects; the staged Unknown's
   `grey-literature-and-chinese-search-record-r40.md` does not exist in this lane (Evidence 9). The lane
   files that do exist are cited by path; the Chinese checklist's wording is declared not opened here.
6. **Layout caveat, disclosed for the recheck:** the capture is `pdftotext -layout` output, so a sentence
   can be split by a newline and a run of spaces. Every quote used here sits inside one line; item 6's
   `…助言を求めた情報` ends at char 530 and its continuation `源を記載する。` resumes at char 555 (23 layout
   spaces between them), which is why they are quoted separately rather than as one span.

## Out of scope / untouched

Registry row, spans files, `quotes.tsv`, `corpus/lessons/round-52.md` (L1); the frozen C1/C2 counters were
read, not run; no git/jj mutation, no network fetch, no campaign tool, no install. Only write: this report.

VERDICT: Drafted and self-grounded the Japanese PRISMA 2020 checklist entry at its archive copy — 8 quotes derived by the lane builder, `inference-ground` PASS (7/7 tokens), 完全な検索戦略 at char 766 — and attacked the staged entry's official-translation label, its dead-host story, its five-vs-three item flattening and its "only" inference, all four corrected against the files.
