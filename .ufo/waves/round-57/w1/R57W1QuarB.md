# R57W1QuarB — quarantine hand-check, batch B (register rows S093 S094 S095 S104 S105 S108)

Read-only; the only lane file written is this report. Lane `/home/vgpnk/Projects/shokunin/chousa-shokunin`. Scratch
`/fast/scratch/hyaku/chousa-r57/R57W1QuarB/` (deleted before yield, §5). No network fetch; no frozen counter, control
or recipe edited or mutated. R57-C2/C3 (frozen, `corpus/evidence/round57/claims.md`) read, not touched.
**Recipe.** Key = `sha256(url)[:24]` (`tools/quarantine-check.py:cache_key`). Defined form: an OLE/zip `.raw` through
`tools/capture-text.py` stdout; else the `.txt` (`%PDF-` → `pdftotext -layout`; HTML → `html_to_text`). Eleven named
folds + frozen strict test (NFKC+whitespace, case-sensitive) verbatim from `tools/quarantine-check.py` (`FOLDS` 108-114,
`examine_quote`); longest run delegated to the lane's `tools/absent-split.py` (`longest_run`, `classify`, bound 1/2).

```
$ awk -F'|' '{gsub(/^[ \t]+|[ \t]+$/,"",$2);gsub(/^[ \t]+|[ \t]+$/,"",$3);gsub(/^[ \t]+|[ \t]+$/,"",$4)}
    $2=="`chousa`" && $3 ~ /^round[0-9]+$/ {print $4; n++} END{print "ROWS="n > "/dev/stderr"}' \
  .../shokunnow/.ufo/waves/corpus-expansion-1/absent-defect-register.md
S077 S080 S082 S084 S086 S088 S093 S094 S095 S096 S104 S105 S108 S110 S111 S112 S114 S116 S120 S125 S100 S101 S102 S103
ROWS=24   # 20 payload-absent + 4 prose-class (S100-S103); batch D's count confirmed here
```

## 1. THE HAZARD: register S-ids are NOT lane S-ids

Looking a register id up in `corpus/SOURCES.md` returns a **different document**, and the misresolution is *silent*
because the wrong document's capture exists:

```
$ (lane SOURCES.md row with the SAME id vs the register row's own URL, matched by first URL)
reg   lane row with SAME id   correct lane id (by URL)  naive-correct?
S093  https://arxiv.org/html  ['S090']                   MISMATCH
S104  https://chaxin.las.ac.  ['S107']                   MISMATCH
S108  https://jaohfa.com/pdf  ['S092']                   MISMATCH
(S094→S091, S095→S100, S105→S108 likewise)
register rows: 20; naive-id path mismatches the register URL in 20 rows
```

All **20/20** payload-absent rows mismatch (S095 has no lane row with that id; the lane's S095 is own-work,
`corpus/lessons/round-47-verifier-spotcheck.md`). For S093 the naive path lands on
`https://arxiv.org/html/2012.00614v2` (key `44be8711b50a9daae2865b02`) — a capture that **does** exist, so the error
yields a confident verdict about the wrong document instead of an error. **Batch-B rows bind by URL, not by id.**
Bindings used throughout (URL match): S093→`4132ec1b265e60624523251f`/S090 (aclanthology
2026.findings-acl.19.pdf) · S094→`3749141b52b2dbb2e0e821c3`/S091 (ojs.aaai.org …29825/31432) ·
S095→`b539a80218080da56a75b624`/S100 (zcmu.edu.cn …C3A00.doc?e=.doc) · S104→`7194acc65a18f6555e4b8893`/S107
(jstage …32_320208/_pdf/-char/ja) · S105→`62be15a474e866e4bef6c9d5`/S108 (jaohfa.com/pdf/systematic_review.pdf) ·
S108→`b502d4c6a6ee023bee6f8531`/S092 (arxiv.org/html/1803.05355).

## 2. Verdict table — register quoted spans vs the fresh lane-owned defined form

`final.py` output; per quote fold / strict / offset / run. `r43` = the lane's `absent-split.py` re-run on the fresh
bytes — it reproduces the committed `corpus/evidence/round43/absent-split.tsv` **exactly** (S093 79/120, S094 63/86,
S104 25/88, S105 17/24, S108 69/108), so the round-43 split is **stable across the re-fetch** and the batch-B ABSENT
verdicts are re-confirmations, not new findings. S095's MIXED = the lane's `decide()` class for 0<located<n_quotes; on
the register's binary class it is ABSENT (not PRESENT), since q2 alone does not make the row present.

| reg id | form (provenance) | len | quote (len) | fold | strict | offset | run | r43 class | **VERDICT** |
|---|---|---|---|---|---|---|---|---|---|
| S093 | pdftotext -layout (`.txt`) | 90692 | q1 (120) | none | False | – | 79/120 | misquote .658333 | **ABSENT** |
| S094 | pdftotext -layout (`.txt`) | 66321 | q1 (86) | none | False | – | 63/86 | misquote .732558 | **ABSENT** |
| " | " | " | q2 (115) | none | False | – | 60/115 | " | " |
| " | " | " | q3 (119) | none | False | – | 59/119 | " | " |
| S095 | **capture-text(stdout) of OLE raw** | 842 | q1 (22) | none | False | – | 15/22 | misquote 1.000000 | **MIXED** |
| " | " | " | q2 (47) | **exact** | **True** | **143** | **47/47** | " | " |
| " | " | " | q3 (33) | none | False | – | 12/33 | " | " |
| S104 | pdftotext -layout (`.txt`) | 21216 | q1 (88) | none | False | – | 25/88 | not-carried .284091 | **ABSENT** |
| S105 | pdftotext -layout (`.txt`) | 39676 | q1 (66) | none | False | – | 21/66 | misquote .708333 | **ABSENT** |
| " | " | " | q2 (64) | none | False | – | 6/64 | " | " |
| " | " | " | q3 (24) | none | False | – | 17/24 | " | " |
| S108 | html_to_text (`.txt`) | 69681 | q1 (108) | none | False | – | 69/108 | misquote .638889 | **ABSENT** |

## 3. Forms, and why each ABSENT is ABSENT (offsets + actual document text)

| reg id | what the form actually is | why the quote is not located (offsets into that form) |
|---|---|---|
| S093 | `%PDF-` raw; `.txt` = `pdftotext -layout`; **two-column** | quote concatenates two enumerated items **across a line break and across the sidebar column**; doc at 1526 `…lead sections\n are unsupported by the article body; (2) ∼30% … Cited source\n of claims…`; the PDF's own four fragments are each present (verified), and lane pins S090-4..7 cut at exactly those seams (1446/1496/1589/1643) → **misquote, not fabrication** |
| S094 | `%PDF-` raw; `.txt` = `pdftotext -layout`; **two-column** with an **Evidence** sidebar | sidebar interleaves the abstract's lines (doc at 810: `CFEVER comprises 30,012   2004 looking for business opportunities.)\n manually created claims…`); q2 also hyphenates (`degree of fac-` / `tualness.`), q3 (`claims in the “Sup-\n ports”`) breaks on a wrap **and** the Chinese sidebar; halves present separately (verified), whole span not → **misquote** |
| S095 | **OLE Word 97-2003 `.doc`** raw (magic `d0 cf 11 e0 a1 b1 1a e1`), **not** a JS-driven page: `curl` returned the real binary (attempt 2, 801280 B, `raw_sha256 46d1866ce9afd516…`, byte-identical to the refetch record). `.txt` = UTF-8-with-replacement decoding of the raw bytes (762306 chars of mostly NUL) — no Chinese quote can appear there, which is why round-42 called it `unverifiable`. `tools/capture-text.py` (round-52, commit `804a453`; OLE support `8a7d0f1`) renders it to **842 chars of real Chinese text**, and that is the defined form | q2 **present exactly at offset 143**; q1/q3 misquotes of real text: the doc reads `中国知网他引频次的查询需要使用《中国引文数据库》。` and `成功登录《中国引文数据库》后，可按“题名”、“作者”、“单位”等方式…`, the register drops the 《》 and the quote marks and writes `题名作者单位` → **no longer unverifiable: MIXED** |
| S104 | `%PDF-` raw; `.txt` = `pdftotext -layout`; **two-column**, sentence crosses the column break | reading-order proof below → the sentence **is** carried, one character difference → **not-carried is an artefact** |
| S105 | `%PDF-` raw; `.txt` = `pdftotext -layout`; **four-column table** | q1 (`情報源［Informationsources］6 全てのデータベース…`) is the **concatenation of four separate table cells** (`情報源` \| `［Information sources］` \| `6` \| bullet column) that never appear adjacently; q3 is split across two rendered lines; q2 is §4 → **misquote** |
| S108 | raw starts `<!DOCTYP` (arXiv HTML); `.txt` = campaign `html_to_text` | doc at 2741 `The claims are classified as Supported , Refuted or NotEnoughInfo by annotators achieving 0.6841 in Fleiss κ \kappa .` — HTML→text leaves a **space before the comma** and the **LaTeX macro** `\kappa` where the register wrote `κ.`; diff at char 38: quote `,` (0x2c) vs doc ` ` (0x20). Lane pin S092-4 pins the shorter `0.6841 in Fleiss` (2741) → **misquote** |

### S104 reading-order proof (the decisive row)

```
$ pdftotext -bbox-layout 7194acc65a18f6555e4b8893.raw -   (page 4, two columns)
L y=742.6 '記録する．このプロセスに際して，誰が検索を行ったの'
R y= 84.6 'か，その日時，使用した検索式を同時に記録しておくこ'
R y= 98.6 'とが望ましい．これにより，研究の透明性を保ち，他者'
   (left column read first, running footer 122日健教誌第32巻第2号2024年 dropped)
DOC segment: '…記録しておくことが望ましい．これ'
QUOTE      : '…記録しておくことが望ましい。'
identical? False
  first difference at char 51: quote='。' U+3002  doc='．' U+FF0E
```

Reading order (left column then right column) yields the sentence **contiguously**, differing from the register's quote
by **exactly one character** (`。` U+3002 vs `．` U+FF0E). So round-43's **not-carried (25/88 = 0.284 < 1/2) is an
artefact of the `-layout` rendering's column interleaving, not a property of the document**: the sentence *is* carried
by the PDF, in reading order, with one full-stop variant. The frozen bound and tool are untouched; the *label* is what
is wrong. Reported for routing.

## 4. S105 q2 is not a quote of the PDF at all — it is the lane's own English prose

S105's second span is **`and not, as a search engine's rendering of the same form has it,`** — English, while the cited
source is a Japanese PRISMA form (別紙様式 (V)-4). The phrase is in **no lane capture** (`grep -rl "as a search engine"
corpus/captures/` → empty) and in **no lane corpus file** (`grep -rl "as a search engine's rendering" corpus/` → empty).
The census record shows why: the campaign's quote-lint harvested **quote-shaped fragments out of a lane registry note**,
and `line` gives the source as the note prose, not the PDF:

```
'line': '記載する" and not, as a search engine\'s rendering of the same form has it,\n"それぞれの情報源が最後に調べられた日付を記載する". The row quotes the\nPDF\'s own wording; the recheck command matches a contiguous run.'
```

The `line` for the *other* two S105 quotes shows the note quoted the PDF's own wording and the extractor took the
note's **own connective English clause** as a third quoted span; the register then carried it as a quote of the PDF
(the same row already carried that clause in round-41/48 lane reports). Round-48's hand-check reported it as
`LCS 6/64 … inside the PDF's word 'search'` — the six-char run `earch ` is the substring of an unrelated `search` in
the PDF, not the quote. **S105 q2 is a mis-extraction from a lane note, not a defective quotation of the document**;
its ABSENT verdict is true but vacuous.

## 5. Freshness of the six captures + the lane's own pins (read-only)

* All six captures exist as `<key>.raw`+`<key>.txt` in `corpus/captures/`, and every stored byte matches the **last
  successful attempt** in `corpus/evidence/round57/refetch.tsv` (all attempt 2; S095's attempt 1 was a `curl_rc=28`
  timeout with `-` digests). I recomputed `sha256` of each `.raw`/`.txt` — all six match. `recipe_txt(raw)`
  (`tools/capture-fetch.py`) vs the stored `.txt` is **byte-identical for all six**; for S095 the stored `.txt` is the
  UTF-8-with-replacement decoding of the OLE raw (762306 chars), exactly as the recipe produces
  (`sha256 recipe(raw)==stored.txt → True`, `ce30e73574e7`) — a 41-char length delta I first saw was only a
  `read_text` universal-newline artefact, not a content difference.
* Frozen C2 counter, run read-only: `SET=47 VERDICTS=47/47 REPRODUCED=41 DRIFTED=5 UNREACHABLE=1 BYTE_BACKED=46
  CONSISTENT=46/46 FLAGGED=0/0 C2=PASS` (exit 0). All six batch-B keys are inside the 47 and all six are
  **REPRODUCED** (`CAPTURE S090 4132ec1b265e60624523251f pin=2f8047a877c3 REPRODUCED`; `CAPTURE S100
  b539a80218080da56a75b624 pin=46d1866ce9af REPRODUCED`). The dispatch's "43/47 landed, 4 pending" is now 47/47:
  S100/S103/S106 landed and **S105 is the UNREACHABLE row** (3 failed attempts ≥600 s apart).
* Every committed span row of the six lane rows (S090 S091 S100 S107 S108 S092) verified against the **fresh** bytes —
  quote located in the form whose digest the manifest pins, and the span FILE the exact slice at the recorded offset:

```
$ python3 slices.py slices.json
== S093 -> lane S090 (8 rows)  … quotes located in pinned form 8/8;  exact slices 8/8
== S094 -> lane S091 (5 rows)  … quotes located in pinned form 5/5;  exact slices 5/5
== S095 -> lane S100 (3 rows)  … quotes located in pinned form 3/3;  exact slices 3/3
== S104 -> lane S107 (17 rows) … quotes located in pinned form 17/17; exact slices 17/17
== S105 -> lane S108 (10 rows) … quotes located in pinned form 10/10; exact slices 10/10
== S108 -> lane S092 (7 rows)  … quotes located in pinned form 7/7;  exact slices 7/7
TOTALS: quotes in pinned form 50/50 ; exact slices 50/50
quotes in the C2/C3 defined form: 50/50
```

  Two corroborations: (a) the manifest pin equals the **fresh** `.txt` digest for S090/S091/S107/S108/S092 (e.g.
  `2f8047a877c390f8…` for S090) — the round-57 fetch produced the bytes the round-47/51 manifests pinned; (b) **S100
  pins the `.raw` digest, not the `.txt` digest** (`46d1866ce9afd516…` == fresh raw), because S100 is the OLE row
  whose quotes live in the raw's UTF-16LE decoding (`corpus/evidence/round49/build-spans.py` form order) — its `.txt`
  sidecar cannot hold them. Both are consistent, and my S095 verdict uses the `capture-text` form, which holds all
  three spans.

## 6. Findings to route to the L1 (reported, not patched)

1. **Id-space collision (highest value).** Register `S###` ≠ lane `S###`; the naive same-id lookup mismatches on
   **20/20** payload-absent rows and lands on *existing* captures for 5/6 batch-B rows, so the error is silent. A
   machine-readable binding table (register id → lane id → URL → key) would remove the trap; batch A/D should be told
   the binding is by **URL**.
2. **S104 is mis-classed `not-carried`** (see §3): the sentence **is** carried by the PDF in reading order, differing
   by one character. Bound and tool frozen; the *label* is wrong (`corpus/evidence/round43/absent-split.tsv` line for
   S104 should be revisited — I did not touch it).
3. **S105 q2 is a mis-extraction from a lane note** (§4), not a defective quotation of the PDF.
4. **S095 is no longer unverifiable**: `capture-text.py` renders the OLE raw and q2 is present **exactly** at offset
   143 → **MIXED** (see §3 for q1/q3).
5. **The register truncates quotes at 120 chars and keeps only 3 per row** (`absent-defect-register.py:142`, `q[:120]`,
   `r["quotes"][:3]`): S093's registered span is 120 of 155 chars, S094 q3 is 119 of 166. "The register quotes X" is
   always "the register quotes a **prefix** of X" — compare against the census's full quote too.
6. **The round-43 split is stable across the re-fetch** for all five batch-B rows scored there (§2): identical ratios
   to the committed table. Freshness evidence for C2.

## 7. Files changed, verification, cleanup

* **Exactly one lane file written:** this report, `.ufo/waves/round-57/w1/R57W1QuarB.md`. Nothing else in the lane was
  written; the fleet root, `shokunnow` and sibling lanes were read-only. No git/jj mutation anywhere (the
  `git show`/`git log` calls are read-only reads of lane history). **No external fetch** — every byte read is
  committed lane evidence under `chousa-shokunin/corpus/captures/` or the read-only campaign register/census in
  `shokunnow`; `capture-text.py` ran against the committed `.raw`. **No tool installed or upgraded** (no
  pacman/uv/npm) — the directive needed none: `pdftotext` 26.08.0 and Python 3.14.8 are already present and are the
  versions the frozen recipe names.
* **Verification actually run** (commands + observed output pasted above): the slice awk; the id-collision table over
  all 20 rows; `quarantine-check.py examine` and `verdict` against the lane capture dir; the eleven-fold
  `examine_quote` per quote against each defined form; the lane's `absent-split.py:classify` on the fresh bytes; the
  `capture-text.py` rendering of the OLE raw; `pdftotext -layout/-raw/default` and `pdftotext -bbox-layout`
  reading-order reconstruction for S104/S105; digest recomputation of all six captures against `refetch.tsv`; the
  recipe-vs-stored `.txt` byte check; the span slice check (50/50); and the frozen `c2-count.py` (read-only, exit 0,
  `C2=PASS`).
* **Scratch** `/fast/scratch/hyaku/chousa-r57/R57W1QuarB/` — `mkdir -p`, used as `TMPDIR` with
  `PYTHONDONTWRITEBYTECODE=1`, and **deleted before this report was finalised** (`rm -rf --` on that path). Nothing
  written to `/tmp`.

VERDICT: Batch-B hand-check of the six register rows (S093 S094 S095 S104 S105 S108) against the fresh lane-owned
bytes — **five ABSENT (all misquotes, no fabrications) and S095 MIXED** (q2 present exactly at offset 143, so no
longer unverifiable); the lane's 50 pinned spans all survive the re-fetch 50/50 and the round-43 ratios reproduce
exactly — with two findings the frozen tooling does not catch: the register/lane S-id collision (20/20 rows, silently
wrong) and S104's `not-carried` label, an artefact of `-layout` column interleaving where the sentence is present in
reading order with a single `。`/`．` difference.
