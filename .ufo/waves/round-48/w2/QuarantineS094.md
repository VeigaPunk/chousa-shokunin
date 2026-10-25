# QuarantineS094 — hand-check, register `chousa` S094 (lane S091)

Scope: re-verify the `payload-absent` verdict on chousa-register row S094 against the on-disk capture of
`https://ojs.aaai.org/index.php/AAAI/article/download/29825/31432` (CFEVER, AAAI-24). No live fetch. Read-only; leaf member.

## Inputs

- Frozen slice row: `.ufo/waves/round-48/assimilation/quarantine-slice:8` — `S094   `payload-absent``.
- Register row: `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`
  byte offsets 6544–7114 (571 B line, `|` `chousa` `|` round2 `|` S094 `|` `payload-absent` `|`
  `https://ojs.aaai.org/index.php/AAAI/article/download/29825/31432` `|` 3 `<br>`-joined quotes `|`
  "cited source, companion URLs and local artifacts were all checked; the quote is in none of them").
- Lane binding: `corpus/SOURCES.md:101` binds this URL to **lane id S091** (register campaign id ≠ lane id;
  URL is the join key — same convention as QuarantineS108).
- The lane SOURCES-PROPOSED file `lanes/chousa/round2/SOURCES-PROPOSED.md:26` binds id "S094" to a *different*
  URL (`warp.ndl.go.jp/en/info/qanda`, a WARP FAQ); the CFEVER block is its `S099` (lines 89–95). This is a
  same-round renumbering artifact in the expansion wave, not the register's join key; the register row's URL
  resolves to CFEVER/S091.
- Capture: `.ufo/waves/corpus-expansion-1/.qcache/3749141b52b2dbb2e0e821c3.txt` — 66,770 bytes, sha256
  `0b3518bf2d2ba3047212d6f4ccb83dfd1cf01960e51acb324f7b74b6b2730573` (matches `corpus/evidence/round42/receipts/digests.txt:9`).
- Companion payloads `.pdf`/`.raw`: 231,231 bytes each, sha256
  `83a30baf0d47afce01c76ceabc84014f19af773b468566d828279d646a784597`; `file` → PDF 1.5.
  Gate block (`SOURCES-PROPOSED.md:91`) records "HTTP 200, 231,231 bytes; text extracted with pdftotext -layout,
  66,770 bytes" — sizes match the cache exactly.
- Cache-key check: `printf 'https://ojs.aaai.org/index.php/AAAI/article/download/29825/31432' | sha256sum |
  cut -c1-24` → `3749141b52b2dbb2e0e821c3` ✓ (capture filename is the cited URL).

## Commands run (decisive output)

Text begins "The Thirty-Eighth AAAI Conference on Artificial Intelligence / CFEVER: A Chinese Fact Extraction
and VERification Dataset" — correct paper.

`grep -n` raw anchors (lines are pdftotext -layout two-column interleave; right column = worked example):

```
15:  Extraction and VERification. CFEVER comprises 30,012            2004 looking for business opportunities.)
17:  Wikipedia. Each claim in CFEVER is labeled as “Supports”,       Evidence:
18:  “Refutes”, or “Not Enough Info” to depict its degree of fac-    [wiki/尼克·貝爾格 (Nick Berg)]
19:  tualness. Similar to the FEVER dataset, claims in the “Sup-
20:  ports” and “Refutes” categories are also annotated with cor-    他在 2004 年 3 月前往伊拉克 …
21:  responding evidence sentences sourced from single or mul-       2004 年 4 月 9 日失蹤。(…)
22:  tiple pages in Chinese Wikipedia. Our labeled dataset holds     2004 to search for communication…
```

Left-column de-interleave (split at first ≥3-space run followed by right-column text, ~col 58–65) +
line-break dehyphenation reconstructs the abstract; all three register quotes then match **verbatim**:

```
FOUND  Q1 'CFEVER comprises 30,012 manually created claims based on content in Chinese Wikipedia.'
FOUND  Q2 'Each claim in CFEVER is labeled as “Supports”, “Refutes”, or “Not Enough Info” to depict its degree of factualness.'
FOUND  Q3 'claims in the “Supports” and “Refutes” categories are also annotated with corresponding evidence
          sentences sourced from single or multiple pages in Chinese Wikipedia.'
```

Piecewise raw anchors into the capture (char offset → byte offset in .txt):

```
'CFEVER comprises 30,012'                          char 810  byte 847
'manually created claims based on content in Chinese\n  Wikipedia.'  char 901  byte 938
'to depict its degree of fac-'                     char 1075 byte 1124
'claims in the “Sup-'                              char 1187 byte 1247
'ports” and “Refutes” categories are also annotated with cor-'  char 1209 byte 1271
'sourced from single or mul-'                      char 1347 byte 1453
'tiple pages in Chinese Wikipedia.'                char 1438 byte 1556
'Verdict: Supports' (worked-example quote)         char 2490 byte 2670
```

Quote digests vs round-42 receipts (`corpus/evidence/round42/receipts/examine.txt:15-17` records three
quarantined S094 quotes against `3749141b52b2dbb2e0e821c3.txt`, all "absent"):

```
Q1 sha256[:12] 5ac7e7bebfe9  (86 ch)  matches receipt  ✓
Q2 sha256[:12] 56db22ca2d0b (115 ch)  matches receipt  ✓
Q3 register truncation 'claims … sourced from' (119 ch, no trailing space) sha256[:12] bb3802796101
   matches receipt  ✓ — the full sentence in the capture contains this prefix verbatim after fold repair
```

Mechanism of the false negative: the abstract is a single contiguous passage on the page, but
`pdftotext -layout` splits it at ~column 60 and interleaves the right column's worked example, and hyphenates
`fac-/tualness`, `Sup-/ports`, `cor-/responding`, `mul-/tiple` across lines. An exact-substring or whitespace/
hyphen-fold check that does not de-interleave columns and rejoin hyphens cannot match. The round-42 runner's
"eleven folds" (verdict.txt:11) evidently lacked the column-deinterleave + dehyphen fold — same miss class as
the round-47 arXiv `\kappa` artifact, different surface.

## Verdict

- **Q1, Q2, Q3: `present`.** Every register quote reconstructs verbatim (character-for-character) from the
  contiguous abstract span of capture `3749141b52b2dbb2e0e821c3.txt` chars ~810–1560; only pdftotext
  column-interleave and hyphenation stand between raw text and quote.
- Register row S094 (`payload-absent`, "the quote is in none of them") is a **false negative — falsified**.
  The cited-source capture was fetched (231,231-byte PDF in cache, digest-confirmed, cache-key = sha256(URL))
  and contains all three quotes.
- The register row is nonetheless *internally consistent*: url, quotes and lane all belong to one source
  (CFEVER / lane S091). The failure is in the match fold, not the join.

## Residual risk / gaps

- If the acceptance predicate requires byte-exact literal matching with zero normalisation, all three quotes
  read `absent-as-written` (the literal strings never occur); the substance is fully present and the miss is a
  known extraction artifact class (rounds 42/43/46/47 pattern).
- Capture is the campaign cache, not a live read; whether the served bytes changed since 2026-10-23 is
  unchecked by design (no-fetch lane bound).
- The lane PROPOSED file's id collision ("S094" → WARP FAQ) is a naming hazard for future id-bound checks;
  URL-joining is required. Not a defect in the register row itself.

## Tools / hygiene

- No installs or upgrades; no pacman transactions. Scratch dir not needed; nothing under /tmp to delete.
- Single write: this report. No production file, sibling lane, git/jj/index, or fleet repo touched.
