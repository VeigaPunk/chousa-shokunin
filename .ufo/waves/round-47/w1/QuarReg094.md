# QuarReg094 — quarantine hand-check (§10), register `chousa` S094

Item: hand-check the register row `| S094 |` with lane `chousa` in
`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md` against the capture of its URL
(lane id S091). No fetch was made, and nothing was installed.

## Inputs (read-only)
- Register: `absent-defect-register.md:44`, sha256 `5afe1810a6c3d62f37987b575a954f5b1197daa23005d4bb2f1d982f64bad833`.
  Header at `:27` is `| lane | round | id | class | cited source | quote(s) | note |`. The row's cells are: lane `` `chousa` ``, round `round2`, id `S094`,
  class `` `payload-absent` ``, URL `https://ojs.aaai.org/index.php/AAAI/article/download/29825/31432`, and note
  "cited source, companion URLs and local artifacts were all checked; the quote is in none of them".
- Capture: `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/3749141b52b2dbb2e0e821c3.txt`, 66770 bytes,
  sha256 `0b3518bf2d2ba3047212d6f4ccb83dfd1cf01960e51acb324f7b74b6b2730573`. `sha256(url)[:24]` = `3749141b52b2dbb2e0e821c3`
  (computed), so the filename binds to this URL. The capture is a pdftotext layout render of the CFEVER AAAI-24 paper.
  The abstract is laid out in two columns: the left column is the abstract, and the right column is the Table 1 example
  (wiki/尼克·貝爾格 Nick Berg).
- Offsets below are Python **character** offsets (0-based) into the decoded UTF-8 capture. Byte offsets differ after
  the CJK text; the anchor's byte offset is given separately.

## Commands run (decisive output)
1. `grep -n '| S094 |' register` returned `:44` (chousa, the row above) and `:164` (revenger, out of scope).
2. `python3 chk.py`: a raw `cap.find(quote)` returned **-1 for all three quotes**. The loose word scan found "factualness"
   and "sourced" missing because the render splits them as `fac-`+`tualness` and the
   right-column text sits between the parts. This reproduces the mechanical false negative.
3. `python3 strict.py`: a strict matcher. Each quote is a sequence of literal chars. The only allowances are
   (a) whitespace or a line break between words, (b) a right-column tail of 2 or more spaces followed by any text up to
   `\n` (column interleave), and (c) `-` + optional interleave + `\n` inside a word (hyphen split). Output:
   `Q1 matches=1 [(810, 965)]`, `Q2 matches=1 [(966, 1156)]`, `Q3 matches=1 [(1187, 1359)]`.
4. Part, interleave and anchor offsets (python `str.find`/`re.finditer`). `factualness` occurs 0 times as a
   contiguous string in the capture, and `sourced` occurs once.

## Per-quote hand-check

**Q1** `CFEVER comprises 30,012 manually created claims based on content in Chinese Wikipedia.` — **present**
(all 13 words in order, at char 810–965).
- [810,833) `CFEVER comprises 30,012`
- interleave [857) `2004 looking for business opportunities.)` (right column, Table 1 example, excluded)
- [901,952) `manually created claims based on content in Chinese`
- [955,965) `Wikipedia.`

**Q2** `Each claim in CFEVER is labeled as “Supports”, “Refutes”, or “Not Enough Info” to depict its degree of factualness.`
— **present** (all 19 words in order with the same curly quotes, at char 966–1156; `fac-`/`tualness` is a hyphen split).
- [966,1012) `Each claim in CFEVER is labeled as “Supports”,`
- interleave [1031) `Evidence:` (excluded)
- [1043,1103) `“Refutes”, or “Not Enough Info” to depict its degree of fac-`
- interleave [1119) `[wiki/尼克·貝爾格 (Nick Berg)]` (excluded)
- [1147,1156) `tualness.`

**Q3** `claims in the “Supports” and “Refutes” categories are also annotated with corresponding evidence sentences sourced from `
— **present** (all 16 words in order, at char 1187–1359; hyphen splits `Sup-`/`ports”` and `cor-`/`responding`).
The register cell is truncated mid-sentence with a trailing space; the capture continues `single or mul-`/`tiple pages`.
- [1187,1206) `claims in the “Sup-`
- [1209,1269) `ports” and “Refutes” categories are also annotated with cor-`
- interleave [1285) `他在 2004 年 3 月前往伊拉克 尋找通訊生意商機，自` (excluded)
- [1317,1359) `responding evidence sentences sourced from`

## Verdict
- quarantine: register `S094` (https://ojs.aaai.org/index.php/AAAI/article/download/29825/31432) verdict: `present` — all three register quotes occur word-for-word in order in capture 3749141b52b2dbb2e0e821c3.txt at chars 810–965, 966–1156 and 1187–1359, broken only by the two-column interleave of the Table 1 example and by hyphen splits (fac-/tualness, Sup-/ports, cor-/responding), so `payload-absent` is a mechanical false negative.

Anchor quote (contiguous, unique, 8 words): `manually created claims based on content in Chinese`. It is at char 901 (byte 938),
with exactly 1 hit in the capture.

## Findings by severity
1. **Medium (calibration):** the register row's class `payload-absent` and its note "the quote is in none of them"
   are false for this capture. Evidence: the strict-match offsets above. The cause is the same class round 43 and round 46 found
   (a PDF that interleaves columns and splits words with hyphens). A wave that consumes this register must not treat lane S091's
   quotes as the fabrication class.
2. **Low:** the Q3 register cell ends at `sourced from ` (truncated by the register generator), so a check of the whole
   cell cannot cover the sentence end. The checked prefix is present.

## Residual risk and verification gaps
- Only the on-disk capture was read; the PDF itself was not opened (no fetch, by contract). The interleave reading
  relies on the layout render, where the right-column text is the Table 1 example. The three interleaved slices plainly
  belong to that example (Chinese example text and a `[wiki/…]` evidence tag), not to the abstract.
- I did not check whether the staged or lane entry text quoting S091 uses the same strings. That is outside this item.

Scratch `/tmp/chousa-r47-QuarReg094/` was deleted before finishing.
