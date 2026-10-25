# W2 hand-check — chousa register row S120 (round5)

## Verdict: PRESENT — `payload-absent` verdict is falsified

All three quoted strings occur verbatim in the rendered text of the cited
capture. The register row's claim ("the quote is in none of them") is wrong:
this row is a false `payload-absent`, i.e. a fabricated-absence.

## Row under check

- Frozen slice line 19: `S120   payload-absent`
  (`…/assimilation/quarantine-slice`, sha context: file is 788 B).
- Register: `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md:55`
  `chousa | round5 | S120 | payload-absent | https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx`
  with three `<br>`-separated Japanese quotes.
- Lane row: `lanes/chousa/round5/SOURCES-PROPOSED.md` binds the same URL to lane
  id **S125** (registry ids differ from lane ids; ID-REMAP round5 shifts +3, so
  lane S125 → registry S128 — register/renumbering inconsistency noted, but the
  URL+quotes match the register row exactly, so this is the right row).

## Local byte evidence (no fetch)

Capture pair (qcache, keyed by staged-map handle `3a8b45977cd111e45e3980a5`):

- `.qcache/3a8b45977cd111e45e3980a5.raw` — 178,056 B, sha256
  `16fc8c55ee856fefbbfc88b391b08233106b337e43aaf9f7a7bd825adeb09763`,
  `file` → "Microsoft Word 2007+", `unzip -t` → no errors (21 members).
  `docProps/core.xml` author 由美 林, dated 2024-04-11; title text:
  「医薬品及び医療機器の費用対効果評価に係る分析結果の記載様式と手引[第2.0版]
  国立保健医療科学院 2024年4月」— matches the cited artifact.
- `.qcache/3a8b45977cd111e45e3980a5.txt` — 319,599 B, sha256
  `471e558969d4ec3d7f795c4b499be79aa31c6fb1f16f3065563a3d0025ba85ea`.
  NOT text: `file` → "Zip archive data"; bytes show `PK\x03\x04` with UTF-8
  replacement chars (EF BF BD) — a mojibake-corrupted copy of the zip.

## Commands run and observed output

```
unzip -p .../3a8b45977cd111e45e3980a5.raw word/document.xml > document.xml
wc -c document.xml                  -> 1464476
python3 (re.sub '<[^>]+>' -> text)  -> stripped chars: 20591
text.find(each quote):
  'SRにおける文献検索期間について明記する。'                                    -> 9728
  '文献検索終了時点は、分析枠組みが決定された後から製造販売業者による分析提出までの一時点に決める。' -> 9752
  'ハンドサーチ等により未公表データを収集した場合は、そのことを上記のフローチャートに含める。'     -> 10127
  (worked-example cell '文献検索期間2015年1月から2018年10月まで'               -> 9892)
xml.find(each quote) in raw document.xml -> -1 for all three
```

Context around char 9728 of the tag-stripped text:

```
…相互に矛盾する結果となった場合、どのように解釈をするのか記載する。
SRにおける文献検索期間について明記する。なお、文献検索終了時点は、分析枠組み
が決定された後から製造販売業者による分析提出までの一時点に決める。･…
```

## Why the absent verdict happened (inferred mechanism)

The quotes are split across `<w:t>` runs inside `word/document.xml`, so they do
not appear as contiguous substrings in the member bytes (`xml.find` → −1). A
byte-level or tag-naive check of the member reports them absent even though the
rendered text contains them verbatim. Round-42's own verdicts.tsv:20 records
the same capture as `unverifiable` ("OOXML zip decoded as bytes and never
rendered to text") — the extraction required by that verdict now resolves it,
and it resolves to PRESENT, not absent. The `.qcache .txt` companion being a
corrupted zip (not the promised 167,642-char extraction) corroborates that no
usable rendered text was ever checked.

## Disposition for the C1 claim

S120 must be struck from the `payload-absent` counter set: it is a confirmed
fabricated-absence (verdict claims checked-and-absent; local byte evidence
shows present). Scratch under /tmp/chousa-r48-QuarantineS120 deleted on finish.
