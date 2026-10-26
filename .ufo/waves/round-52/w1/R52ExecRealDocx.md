# R52ExecRealDocx — real-data breadth for the C1 tool (round 52, w1)

Seat: run `tools/capture-text.py` over every real zip capture in the read-only campaign cache, a
non-zip sample and the whole non-zip population. Reads only: cache under
`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache`, tool at
`tools/capture-text.py` (candidate `804a4537`), frozen claims at lane `37468ead`. Writes: this
report and `/fast/scratch/hyaku/chousa-r52/R52ExecRealDocx/` (removed; receipts copied in first);
no production file, index, or sibling lane touched; no install needed.

## 1. The zip population

```
python3: read 4 bytes of each *.raw under .qcache
raws 2596 · startswith b'PK\x03\x04' → 8
whole cache, all extensions: {'.raw': 2596, '.txt': 2549, '.pdf': 256, '.fail': 1470}
PK hits across all extensions = the 8 raws + their 8 .txt sidecars → the 8 is complete (no .pdf is a zip)
```

## 2. Every zip capture through the tool

`python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/capture-text.py <raw>`; main part from
`_rels/.rels`; element counts over that part with `zipfile` + ElementTree; `chars` = stdout code points.

| raw (key) | package kind (evidence) | main part | rc | chars | U+FFFD | w:instrText | mc:Fallback | w:delText | w:txbxContent | stderr |
|---|---|---|---|---|---|---|---|---|---|---|
| `3a8b45977cd111e45e3980a5` | WordprocessingML `.docx` — NIPH form (creator 国立保健医療科学院 保健医療経済評価研究センター, 2024-04-11) | `word/document.xml` | 0 | 19682 | 0 | 50 | 60 | 0 | 42 | — |
| `b825f17cafd08636a278e6c1` | WordprocessingML `.docx` — 《网络安全漏洞分类分级指南》（征求意见稿）编制说明 (creator `emma`, 2018-10-22) | `word/document.xml` | 0 | 18841 | 0 | 35 | 0 | 0 | 0 | — |
| `cb101e95f5f5e98d019eeca1` | SpreadsheetML `.xlsx` — 822 shared strings (医疗器械…指导原则) | `xl/workbook.xml` | 0 | **0** | 0 | 0 | 0 | 0 | 0 | — |
| `e9761e99ba404f708f97c4eb` | SpreadsheetML `.xlsx` — 958 shared strings (序号/文档名称/公文号) | `xl/workbook.xml` | 0 | **0** | 0 | 0 | 0 | 0 | 0 | — |
| `9990f37099e6b98e68f1ecb0` | OPC zip, no officeDocument rel — NuGet `.nupkg` (Newtonsoft.Json; only `…/manifest`, core-properties) | — | 2 | 0 | — | — | — | — | — | `REFUSED no officeDocument relationship in _rels/.rels` |
| `68a1f5a90ad0edb9e9839840` | APK zip (860 members, `classes.dex`) | — | 2 | 0 | — | — | — | — | — | `REFUSED no _rels/.rels in the package` |
| `bcaebc1a0c6244100bd90d6c` | APK zip (869 members, `classes*.dex`) | — | 2 | 0 | — | — | — | — | — | `REFUSED no _rels/.rels in the package` |
| `6fef2cd89a58578c656ed44f` | plain zip (`disclosure-audit-v1.4-frozen/`, 8 members) | — | 2 | 0 | — | — | — | — | — | `REFUSED no _rels/.rels in the package` |

Two `.docx`, two `.xlsx`, one relationship-less OPC zip, three non-OPC zips. **No `.pptx`** (no capture
resolves to `ppt/presentation.xml`). Every refusal is exit 2, empty stdout, a `REFUSED` stderr line.

## 3. Non-Word main parts — what is printed, and the docstring gap

`.xlsx`: the resolved part holds no `w:t`, so the text form is empty at exit 0 (0 bytes) although the workbook carries 822/958 strings:

```
$ python3 tools/capture-text.py …/cb101e95f5f5e98d019eeca1.raw ; echo rc=$?
rc=0                                        # stdout 0 bytes
$ python3 tools/capture-text.py …/cb101e95f5f5e98d019eeca1.raw --locate '医疗器械生物学评价和审查指南'
LOCATED count=0 offset=-1                   rc=1     # e9761e99… likewise count=0
```

A **legacy `.doc`** that is not a zip by signature, but is accepted by the gate:

```
head b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1'  (OLE2 CFB v3, sector 512; UTF-16 'WordDocument' at 799616)
zipfile.is_zipfile → True  (embedded OPC zip: 15×PK\x03\x04, EOCD at 778054)
members ['[Content_Types].xml','_rels/.rels','theme/theme/themeManager.xml', …]; officeDocument target → theme/theme/themeManager.xml
python3 tools/capture-text.py b539a80218080da56a75b624.raw → rc 0, stdout 0 bytes, stderr empty
sidecar b539a802….txt: 762265 chars, 308430 U+FFFD
```

**Defect?** Not a predicate violation: the predicate refuses "not a zip / no officeDocument
relationship / missing target", and a zip whose officeDocument target is a workbook or theme part
is none of those — the rules applied to such a part legitimately emit nothing. The defect is
documentation: `tools/capture-text.py:26-28` lists only the three refusals and never says a
resolved non-WordprocessingML part yields an **empty text form at exit 0**, so a caller cannot
tell "refused" from "resolved, no `w:t`". Draft addition (report-only; intended lane path
`tools/capture-text.py`, after the Exit codes paragraph — the L1 integrates):

```
A package whose officeDocument part is not WordprocessingML — `xl/workbook.xml` in a
`.xlsx`, `ppt/presentation.xml` in a `.pptx`, or a theme part in a legacy OLE2 document
that embeds an OPC zip — is accepted: the rules above emit only `w:t` text, such a part
holds none, so the text form is empty (0 characters) at exit 0. An empty stdout at exit 0
means "no WordprocessingML text in the resolved part", not "refused".
```

Related bound: the gate is `zipfile.is_zipfile` (`tools/capture-text.py:66`), which searches for an
end-of-central-directory record, not a `PK\x03\x04` signature. No REFUSE-leg generated package can
reach that state, so no leg flips; it is a real-data edge on the word "not a zip", disclosed for the
L1's judgement (I do not propose a predicate change).

## 4. Non-zip population (sample of 10 + full)

```
000f224439dccc949aafb53f.raw rc=2 stdout=b'' stderr=REFUSED not a zip (an OOXML capture is a zip package)
001287c436f0e6b1d166ae8d.raw rc=2 stdout=b'' stderr=REFUSED not a zip (an OOXML capture is a zip package)
002f2eceb4b6b8f841d89b00.raw … 012a018a181585d3e317e68f.raw : identical (all 10, rc=2)
# whole population, every .raw through the CLI (78.1 s):
2588 non-PK .raw → 2587 (2, 'REFUSED not a zip (an OOXML capture is a zip package)') · 1 (0, '') ← b539a802… (§3)
```

## 5. Pinned NIPH capture and an independent reference extraction

```
sha256(3a8b45977cd111e45e3980a5.raw) = 16fc8c55ee856fefbbfc88b391b08233106b337e43aaf9f7a7bd825adeb09763  = c1-count.py REAL_SHA (:47)
  178056 bytes on disk, 48936 UTF-8 bytes of stdout; --locate 'SRにおける文献検索期間について明記する' → LOCATED count=1 offset=8996  rc=0
text form 19682 chars, 0 U+FFFD, 1239 newlines (= the claim's 19682)
sidecar 3a8b45977cd111e45e3980a5.txt: 168953 chars, 72117 U+FFFD (= the docstring's round-51 figure)
```

A second extractor I wrote in report scratch (recursive walk: skip `mc:Fallback` subtree, emit `w:t` text, `w:tab|w:br|w:cr` only under `w:r`, newline after every `w:p`) agrees byte for byte:

```
3a8b45977cd111e45e3980a5.raw ref 19682 / tool 19682 equal True
  instrText 50 (payloads ' TOC \o "1-3" \h \z \u ', ' PAGEREF _Toc161934494 \h ', …), visible in text form 0
  mc:Fallback 60, 21 with text; none emitted from the fallback ('試験4' 2×, both from mc:Choice/w:txbxContent); w:delText 0 → REVISIONS unexercised by real data
b825f17cafd08636a278e6c1.raw ref 18841 / tool 18841 equal True
  instrText 35, 7 payloads (' 图 ', ' 表 ') coincide with body text; extractors agree, so not a leak
```

Sidecar garbage for the four zip captures: 72117 / 102999 / 13297 / 18013 / 308430 U+FFFD — the tool's reason to exist, reproduced on real data.

## 6. Risks / blockers

- `b539a802…` acceptance is not a leg failure; the L1 decides whether "not a zip" means signature or `is_zipfile`. Any change belongs in the docstring/gate, never in a frozen predicate.
- Real-data gaps left to generated legs: `w:delText` (0 in both `.docx`), `.pptx` (absent). Nothing blocked; every command above ran; scratch removed.

VERDICT — attacked `tools/capture-text.py` on the cache's 8 zip captures (+2588 non-zip): both `.docx`
reproduce their text forms exactly (NIPH 19682 chars, sha256 = REAL_SHA, locate count=1 offset=8996)
against an independent extractor, 4 zips and 2587/2588 non-zips refuse at exit 2, and the one real
hole is documented, not hidden: 2 `.xlsx` (plus one OLE2 `.doc` embedding an OPC zip) are accepted at
exit 0 with an empty text form — a docstring statement the tool lacks today.
