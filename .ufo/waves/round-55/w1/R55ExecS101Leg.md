# R55ExecS101Leg — S101 defined-form build

Seat: round 55 / wave 1. Scope: the four S101 `QUOTE` lines in `R54DraftEntryStb.md:212-215`; no production files changed. Claims remain frozen.

## Build evidence

Candidate: lane commit `6ca924995d48facbf704d2aa22ddaec236059039`; its `tools/build-spans.py` SHA-256 is `1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6`. `tools/capture-text.py` SHA-256 is the frozen `2c0140bc04029c8faedc6c89a65bd657430d8b85f433406946567b70303e2573`. Ran the archived candidate copy from that revision, with the specified read-only campaign cache and outputs under `/fast/scratch/hyaku/chousa-r55/R55ExecS101Leg/`.

Command:
```sh
python3 "$S/lane/tools/build-spans.py" --quotes "$S/quotes-s101.tsv" --out "$S/out-s101" --cache /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache
```
Observed:
```text
QUOTE S101 char 13105 spans/S101-1.txt
QUOTE S101 char 13194 spans/S101-2.txt
QUOTE S101 char 13484 spans/S101-3.txt
QUOTE S101 char 25014 spans/S101-4.txt
SPANS_ROWS=4 WRITTEN=4
EXIT=0
```
`capture-text.py <6dc68fd6b32ce9c8dfcebce8.raw> --locate '<quote>'` independently returned `LOCATED count=1 offset=13105`, `13194`, `13484`, `25014` in quote order. Defined form: 27,012 chars; raw SHA-256 `6063a3aff7a4081e93a685f2721e2cd6b477ba84a841211e298bcddd6d9fddf3`. Every manifest digest matched that raw; each generated span equaled `form[offset:offset+len(span)]`, was longer than its quote, and had the quote once at `offset + span.find(quote)`. All four quotes were unique in the defined form.

| Row | Quote offset (builder `char N`) | span start (`offset` column) | span chars | quote chars / words | whole-raw UTF-16LE quote offset |
|---|---:|---:|---:|---:|---:|
| S101-1 | 13105 | 13025 | 197 | 37 / 3 | 12303 |
| S101-2 | 13194 | 13114 | 186 | 26 / 11 | 12392 |
| S101-3 | 13484 | 13404 | 226 | 66 / 2 | 12682 |
| S101-4 | 25014 | 24934 | 204 | 44 / 2 | 34265 |

All quote lengths meet the 25-word / 160-character limits. Form versus UTF-16LE offsets differ by +802, +802, +802, and -9251 respectively. Whole-raw UTF-16LE decode was 64,512 chars with 263 U+FFFD; `.txt` sidecar was 157,816 bytes with 14,486 U+FFFD, and contained none of the four quotes.

Additional focused checks:
```text
# same quote table, second out directory; diff -r out-s101 out-s101-b
build2 EXIT=0
IDENTICAL
# --check out-s101
SPANS_ROWS=4 STALE=0
check EXIT=0
# raw-only cache
QUOTE S101 char 13105 spans/S101-1.txt
QUOTE S101 char 13194 spans/S101-2.txt
QUOTE S101 char 13484 spans/S101-3.txt
QUOTE S101 char 25014 spans/S101-4.txt
SPANS_ROWS=4 WRITTEN=4
EXIT=0
```
With only the `.txt` sidecar in the cache, each of the four quotes was refused as `quote occurs 0x in 6dc68fd6b32ce9c8dfcebce8.txt`; exit 1, and no output directory/manifest was created. Thus raw-only succeeds and sidecar-only does not supply these OLE quotes. Normal build had **0 refusals**; no substitute wording was needed. The separate intentionally invalid NUL-containing probe also refused with `quote occurs 0x` and exit 1 (not part of the four-row build).

## S101 state / falsifiers

`R54DraftEntryStb.md:212-215` supplies these exact four input rows; builder offsets above are the defined-form offsets. The S101 entry path named by those rows exists at `corpus/knowledge/source-type-taxonomy-r37.md`, but the current file cites only S123 (`:3`) and each of these four exact quotes occurs 0 times in it. Therefore the block below is ready for a later integration, but does **not** establish entry-containment until the L1 lands the S101 content; do not treat the manifest alone as a complete source entry.

The current `corpus/SOURCES.md:111` S101 `used-by` anchor remains the six old `char` positions `11170, 11205, 11993, 12161, 13247, 34374` (round-54 reanchor report `R54DraftS101Reanchor.md:51-56` lists the corresponding defined-form replacements). The draft entry's S101 source line (`R54DraftEntryStb.md:101`) instead cites `char 12392, 12682, 34265`; these are the UTF-16LE locations of quotes 2-4, while their defined-form positions are 13194, 13484, 25014. Independently checked the six S101 rows in `corpus/evidence/round49/spans.tsv:20-25`: all six existing span files are **not** exact slices at their recorded offsets of this defined form, although each row's quote occurs once in the form. This is consistent with the reanchor report; no lane rows/files were edited.

## Ready `quotes.tsv` block

```tsv
id	url	quote	entry
S101	https://jc.hit.edu.cn/_upload/article/files/f7/54/711916924125a0682e3bc3ebb6ed/1f6f2731-8c87-4812-b7e2-9fad0069d508.doc	14.3.1根据 GB 3469规定，以单字母方式标识以下各种参考文献类型	corpus/knowledge/source-type-taxonomy-r37.md
S101	https://jc.hit.edu.cn/_upload/article/files/f7/54/711916924125a0682e3bc3ebb6ed/1f6f2731-8c87-4812-b7e2-9fad0069d508.doc	文献类型标志 M C N J D R S P G K	corpus/knowledge/source-type-taxonomy-r37.md
S101	https://jc.hit.edu.cn/_upload/article/files/f7/54/711916924125a0682e3bc3ebb6ed/1f6f2731-8c87-4812-b7e2-9fad0069d508.doc	磁带(magnetic tape)——MT，磁盘(disk)——DK，光盘(CD-ROM)——CD，联机网络(online)——OL	corpus/knowledge/source-type-taxonomy-r37.md
S101	https://jc.hit.edu.cn/_upload/article/files/f7/54/711916924125a0682e3bc3ebb6ed/1f6f2731-8c87-4812-b7e2-9fad0069d508.doc	15.5文献载体代码，根据GB 3469规定，采用1位字母：P——印刷本，M——缩微制品	corpus/knowledge/source-type-taxonomy-r37.md
```

Scratch was confined to the assigned directory and removed after capturing this report. No LibreOffice process/tool install was used.

VERDICT — built the four round-54 S101 quotes with the round-55 candidate against the OLE-defined form (4/4 unique, no normal-build refusals); raw-only works, sidecar-only refuses, while the intended lane entry currently lacks all four quotes and needs L1 integration before containment can pass.
