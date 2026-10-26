# R52W2ExecRealDocxFinal — real-data breadth re-run of the LANDED capture-text (round 52, w2)

Seat target: re-run the w1 real-capture breadth (`R52ExecRealDocx` §2/§4) against the **landed** tool at
`e769c03`/`d1d972c`, name every row that moved, and confirm the two `.docx` text forms are byte-stable
against the supplement's pin. Reads only: `.qcache` under `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1`,
lane `tools/capture-text.py`, `corpus/evidence/round52/{c1-count,c1-supplement,build-spans}.py` (module import,
no write). Writes: this report and `/fast/scratch/hyaku/chousa-r52/R52W2ExecRealDocxFinal/` (removed; receipts
below). No production file, index, jj state, fleet file or sibling lane touched. No install needed (nothing
installed; pacman paused, unused).

## 1. Census (attacked w1's "8 expected / 2588 expected")

```
python3 read 4 bytes of every *.raw under .qcache
raws 2596 · first 4 bytes == b'PK\x03\x04' → 8 · non-PK → 2588
```
Both w1 figures reproduce exactly; the zip population is complete (`PK` hits = the 8 raws, no `.pdf`/`.txt` adds).

## 2. Every `.raw` through the landed tool — rc / characters / REFUSED histogram

Driver: 8 threads, `python3 tools/capture-text.py <raw>` per file, recording rc, stdout code points,
stderr; 2596 files in **10.2 s**.

```
total 2596  pk 8  nonpk 2588
rc0 2 · rc1 0 · rc2 2594
rc=2 n=2587  REFUSED not a zip (an OOXML capture is a zip package)
rc=2 n=3     REFUSED no _rels/.rels in the package
rc=2 n=2     REFUSED main part 'xl/workbook.xml' is not WordprocessingML (root {…spreadsheetml/2006/main}workbook)
rc=2 n=1     REFUSED no officeDocument relationship in _rels/.rels
rc=2 n=1     REFUSED main part 'theme/theme/themeManager.xml' is not WordprocessingML (root {…drawingml/2006/main}themeManager)
rc=0 n=2     (both .docx; max chars over the whole population = 19682)
non-PK and not refused → []            # the w1 hole, gone
```

### The 8 zip captures, w1 → now

| raw (key) | package (w1 §2) | w1 rc/chars | now rc/chars | changed? |
|---|---|---|---|---|
| `3a8b45977cd111e45e3980a5` | WordprocessingML — NIPH form | 0 / 19682 | **0 / 19682** | no |
| `b825f17cafd08636a278e6c1` | WordprocessingML — 编制说明 | 0 / 18841 | **0 / 18841** | no |
| `cb101e95f5f5e98d019eeca1` | SpreadsheetML, 822 shared strings | 0 / **0** | **2 / 0**, root refusal | **YES** |
| `e9761e99ba404f708f97c4eb` | SpreadsheetML, 958 shared strings | 0 / **0** | **2 / 0**, root refusal | **YES** |
| `9990f37099e6b98e68f1ecb0` | OPC zip, NuGet `.nupkg` | 2 / 0, no officeDocument | 2 / 0, same string | no |
| `68a1f5a90ad0edb9e9839840` | APK zip | 2 / 0, no `_rels/.rels` | 2 / 0, same | no |
| `bcaebc1a0c6244100bd90d6c` | APK zip | 2 / 0, no `_rels/.rels` | 2 / 0, same | no |
| `6fef2cd89a58578c656ed44f` | plain zip, 8 members | 2 / 0, no `_rels/.rels` | 2 / 0, same | no |

### Non-zip population, w1 → now

w1: `2588 non-PK → 2587 (2, 'REFUSED not a zip…') · 1 (0, '') ← b539a802…` (the OLE2 `.doc` with an embedded
OPC zip). Now: **2588/2588 refused** — 2587 `not a zip`, and `b539a80218080da56a75b624` at rc 2 /
0 bytes with `REFUSED main part 'theme/theme/themeManager.xml' is not WordprocessingML (root {…drawingml/2006/main}themeManager)`.
That is the third moved row, and it is exactly erratum E2(a). **Three rows moved (two `.xlsx`, one OLE `.doc`);
every other of the 2593 is byte-identical in rc, chars and stderr.** No non-zip is accepted; no `.docx`
output changed. Under the assignment's rule, no defect.

## 3. The two `.docx` against the pins

```
$ T=tools/capture-text.py; QC=…/.qcache
$ python3 $T $QC/3a8b45977cd111e45e3980a5.raw | sha256sum
754aae4266a19af9518a4bb46bcd484078baeb095df048d171cfc8cc2f24b0d9  -      # == c1-supplement.py:47 TEXT_SHA
$ python3 $T $QC/b825f17cafd08636a278e6c1.raw | sha256sum
9ef944621610a1bd05035934cc4b4bac8c19dcf950c68fcdea30a22879c00f32  -
$ sha256sum $QC/3a8b45977cd111e45e3980a5.raw
16fc8c55ee856fefbbfc88b391b08233106b337e43aaf9f7a7bd825adeb09763  …  # == c1-count.py:47 REAL_SHA
$ python3 $T $QC/3a8b45977cd111e45e3980a5.raw --locate 'SRにおける文献検索期間について明記する'
LOCATED count=1 offset=8996        rc=0
$ python3 corpus/evidence/round52/c1-count.py
PARAS=PASS ok … REFUSE=PASS ok                    (9 leg lines, each `<LEG>=PASS ok`; elision marked)
REAL=PASS rc=0 count=1 locate=(0, 1, 8996) chars=19682
LEGS=9/9
C1=PASS                                            rc=0
$ python3 corpus/evidence/round52/c1-supplement.py
PREFIX=PASS ok / RELS_FORM=PASS ok / SYNTAX=PASS ok   (three verbatim lines)
REAL_TEXT=PASS rc=0 chars=19682
SUPPLEMENT_LEGS=4/4 / C1_SUPPLEMENT=PASS            rc=0
```

Read-parity with the **other** reader (frozen `build-spans.py:75 docx_text`, imported, not run as a script):
`3a8b… ref 19682 / tool 19682 equal True`, `b825… ref 18841 / tool 18841 equal True`. Supplement `TEXT_SHA` verified,
not trusted: the digest of the tool's own stdout is that string.

## 4. Attacks on the landed tool with the real bytes (each named with its result)

| attack | result |
|---|---|
| NIPH repacked **stored**, members alphabetically reordered | rc 0, 19682 chars, sha `754aae42…` — **identical** |
| NIPH deflate level 9, members **reversed** | rc 0, 19682, `754aae42…` — identical |
| NIPH document member **renamed** (`word/renamed-xxxxxx.xml`), rels Target updated | identical |
| same, rels Target **percent-encoded** (`word%2Frenamed-…`) | identical — E2(e) exercised on real bytes |
| **External** officeDocument relationship injected **before** the real one | identical (tool skips External) |
| External-first + renamed member | identical |
| `--locate ''` on NIPH | `usage: --locate needs a non-empty quote`, **rc 2** — E2(e) holds |
| `--locate` on the Chinese docx, 3 phrases (7 / 3 / 2 occurrences) | rc **1** each, `LOCATED count=7 offset=13`, `count=3 offset=34`, `count=2 offset=28` — offsets are the first occurrence code-point index, count≠1 → exit 1 as frozen |
| frozen `REFUSE` leg coverage (c1-count.py:299-316) | generates only random bytes / HTML / no-relationship zip / dangling target — **no** workbook or theme part, so E2(a)'s "no frozen leg exercises the new classes" is true |

Disclosed divergence checked, not assumed: `build-spans.py docx_text` on the External-first fixture returns
**None** (it takes the first `/officeDocument` relationship regardless of `TargetMode`, reads the absent External
target, `KeyError`), i.e. E3's wording ("then falls back to the UTF-16LE form") is accurate; the tool answers
19682 on the same bytes. No C2 capture carries an External relationship, so no C2 span is affected.

## 5. Risks / blockers

- The three moved rows are **disclosed** in `claims-erratum.md` E2(a). Note the sharp edge the erratum names but
  the counter cannot see: under the frozen sentence those two `.xlsx` and the OLE `.doc` were **exit 0** inputs
  (they fit none of the three refusal classes), so the landed tool's exit 2 is a *new* refusal class. It moves no
  leg (counter 9/9, supplement 4/4) and no real capture loses text (both affected kinds emit 0 `w:t`), but the
  sentence-vs-tool gap is real and only E2(a) covers it.
- Residual real-data gaps unchanged from w1: `w:delText` 0 in both `.docx`, no `.pptx`, no in-package
  External relationship, no part near `MAX_PART` (largest output 19682). Generated legs cover these.
- Nothing blocked; every command above ran to completion; scratch removed.

VERDICT — attacked the landed `tools/capture-text.py` on all 2,596 `.raw` captures (8 zip, 2,588 other): 2 `.docx`
byte-stable at 19682/18841 with NIPH sha256 = `754aae42…` = supplement `TEXT_SHA` and locate count=1 offset=8996,
the 2 `.xlsx` and the OLE `.doc` now REFUSED exit 2 (the only 3 moved rows, all E2(a)-disclosed), 0 non-zip
accepted, frozen counter 9/9 + supplement 4/4 replay green, and six repack/rename/percent-encode/External
mutations of the real NIPH package reproduce the identical text form — no defect found.
