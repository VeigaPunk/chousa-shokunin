# ReviewS093Ratio

Seat: leaf reviewer. No subagent. No production edit. No network. No tool install.
Axes: operability (one interpreter, the digested capture, no reroute), calibration (published 79/120, bound not retuned), depth (independent longest-run, not the counter's printout).
Milestone: Round 43 absent-class split. Measured commit `737f40b6aa8f37ffe2269db370fd6d65a720d9a8`.
Recommendation only. Not an admission.

## Verdict

Published figure matches. Independent recompute of S093's one register quote against the committed text capture, after NFKC and whitespace collapse, is **79/120**.

Ratio 79/120 = 0.6583333333333333. Integer test `79*2 >= 120` is true (158 >= 120), so the row is `misquote` under frozen rule R43-SPLIT. The bound was not retuned.

## Findings

No actionable finding. The published 79/120 is the longest contiguous common run of the row quote the rule names, on the capture the round-42 digest names. Three algorithms that are not `tools/absent-split.py` agree on the length, the quote offset, and the document offset.

## Identity

`git rev-parse HEAD` printed `737f40b6aa8f37ffe2269db370fd6d65a720d9a8`.
`git log -1 --format='%H %s' 737f40b6aa8f37ffe2269db370fd6d65a720d9a8` printed `737f40b6aa8f37ffe2269db370fd6d65a720d9a8 round-43: split the absent class and adopt one locally re-opened search-log entry`.
`git merge-base --is-ancestor 737f40b6aa8f37ffe2269db370fd6d65a720d9a8 HEAD` exited 0.
`python3 --version` printed `Python 3.14.8`. `sys.executable` printed `/usr/bin/python3`.
`git status --porcelain` on the round-42 verdict, examine receipt, digest, and round-43 split table printed no lines.

Quote taken from the register data row, not from the published fraction. Register line 43, lane cell `` `chousa` ``, round `round2`, id `S093`, URL `https://aclanthology.org/2026.findings-acl.19.pdf`. One quote, 120 characters, ending mid-word at `are un`. Non-ASCII code points in the quote are two U+223C TILDE OPERATOR. NFKC does not change them. The folded quote equals the raw quote, length 120.

`sha256(quote.encode())[:12]` is `f3654f6c02dd`, equal to `corpus/evidence/round42/receipts/examine.txt` line 14. `sha256(url.encode())[:24]` is `4132ec1b265e60624523251f`, the file named on that line and in `corpus/evidence/round42/receipts/digests.txt` line 11. Variants without `.pdf`, with a trailing slash, with uppercase `.PDF`, and with `http://` hash to keys whose `.txt` files do not exist. No same-identity reroute. This is the chousa row, not the kagi or revenger rows that also carry id S093.

Capture bytes: 91084. SHA-256 `2f8047a877c390f819c83ee1079ca8229ab16ce461c5f2f45304b33931224997`, equal to the digest line. Register SHA-256 `5afe1810a6c3d62f37987b575a954f5b1197daa23005d4bb2f1d982f64bad833`, equal to digests line 4. `Path.read_text` yields 90692 characters, the "90692-char capture" in `corpus/evidence/round42/quarantine-verdicts.tsv`. Sibling `.raw` and `.pdf` are each 2171480 bytes and both start `%PDF-1.7`. The `.qcache` path is not a shokuknow git blob (`git ls-files --error-unmatch` exited 1). Identity is the digest, and the digest matches.

Committed split row, `awk -F'\t' '$1=="S093"' corpus/evidence/round43/absent-split.tsv`, exit 0:

```
S093	misquote	79	120	0.658333	1
```

`79/120` printed to 6 decimal places is `0.658333`, the cell in that row.

## Independent recompute

Normalization, as frozen in `corpus/evidence/round43/claims.md` and as implemented by the counters this seat did not call: `re.sub(r"\s+", " ", unicodedata.normalize("NFKC", text)).strip()`. Document length after that fold: 67835. Quote length: 120. The fold does not change the quote.

Longest contiguous common run was not taken from `tools/absent-split.py` or `corpus/evidence/round43/c2-count.py`. Those modules were not imported. Three algorithms:

- binary search on window length, confirmed by `str.find` / `in`
- DP with the document as the outer axis (the lane DP iterates the quote outside)
- `difflib.SequenceMatcher(..., autojunk=False).find_longest_match`

Canonical transcript, verbatim:

```
REG_SHA256 5afe1810a6c3d62f37987b575a954f5b1197daa23005d4bb2f1d982f64bad833
REG_SHA256_EXPECTED 5afe1810a6c3d62f37987b575a954f5b1197daa23005d4bb2f1d982f64bad833
REG_LINE 43
NCELLS 9
CELL0=''
CELL1='`chousa`'
CELL2='round2'
CELL3='S093'
CELL4='`payload-absent`'
CELL5='https://aclanthology.org/2026.findings-acl.19.pdf'
CELL6='`∼22% of claims in Wikipedia lead sections are unsupported by the article body; ∼30% of claims in the article body are un`'
CELL7='cited source, companion URLs and local artifacts were all checked; the quote is in none of them'
CELL8=''
NQUOTES 1
QUOTE ∼22% of claims in Wikipedia lead sections are unsupported by the article body; ∼30% of claims in the article body are un
QUOTE_SHA12 f3654f6c02dd
EXAMINE_SHA12 f3654f6c02dd
URL https://aclanthology.org/2026.findings-acl.19.pdf
CACHE_KEY 4132ec1b265e60624523251f
VARIANT_KEYS
  'https://aclanthology.org/2026.findings-acl.19.pdf' -> 4132ec1b265e60624523251f exists=True
  'https://aclanthology.org/2026.findings-acl.19.pdf' -> 4132ec1b265e60624523251f exists=True
  'https://aclanthology.org/2026.findings-acl.19' -> 7839b6673b3e2254307b27ac exists=False
  'http://aclanthology.org/2026.findings-acl.19.pdf' -> a977c15d77e6870d8cc460d1 exists=False
  'https://aclanthology.org/2026.findings-acl.19.pdf/' -> 918daaab51ff91999286da53 exists=False
  'https://aclanthology.org/2026.findings-acl.19.PDF' -> 9bdc0b5be02f48e5a83856bf exists=False
CAPTURE_BYTES 91084
CAPTURE_SHA256 2f8047a877c390f819c83ee1079ca8229ab16ce461c5f2f45304b33931224997
CAPTURE_SHA256_EXPECTED 2f8047a877c390f819c83ee1079ca8229ab16ce461c5f2f45304b33931224997
RAW_EXISTS True RAW_BYTES 2171480
PDF_EXISTS True PDF_BYTES 2171480
RAW_HEAD b'%PDF-1.7'
PDF_HEAD b'%PDF-1.7'
BODY_CHARS 90692
FOLDED_LEN 120 FOLDED_EQ_RAW True
DOC_NFKC_WS_LEN 67835
MEMBERSHIP 79/120 qstart 0 dstart 946
DP_DOC_OUTER 79/120 qstart 0 dstart 946
DIFFLIB 79/120 qstart 0 dstart 946
SPAN ∼22% of claims in Wikipedia lead sections are unsupported by the article body; 
SPAN_LEN 79
SPAN_EQ_DOC True
SPAN_COUNT 1
QUOTE_AFTER '∼30% of claims i'
DOC_AFTER '(2) ∼30% Cited source of cla'
RATIO 79/120 0.6583333333333333
GE_HALF True
CLASS misquote
```

The 79-character span is the quote prefix through the space after `body;`. It occurs once in the folded capture, at offset 946. The next quote character is U+223C `∼`. The next capture character is U+0028 `(`. The capture continues `(2) ∼30% Cited source of claims`. The run stops because the rendering inserts the enumerator `(2)` and, on the same line, the other column's `Cited source`. That is a property of the committed `pdftotext -layout` text, not of a second quote.

A quote-outer DP run in an earlier pass of this seat also returned 79 at the same offsets. It is not repeated here; the document-outer DP above is the cross-check that does not share the lane loop order.

## Residual risk

The register generator stores `q[:120]` (`absent-defect-register.py` line 142). The census quote in `quote-lint-full-v5.json` and `quote-lint-full-v4.json` is 155 characters, and its first 120 equal the register quote. On that longer string the same capture still has longest run 79 (the same prefix). The next block is 72: ` of claims in the article body are unsupported by their (public) sources`. Full-quote ratio 79/155 = 0.5096774193548387. Integer test `79*2 >= 155` is true by 3 (158 >= 155), so the class would stay `misquote` if the rule had used the census quote. R43-SPLIT names the row's quotes. The row's quote is the 120-character register cell. 79/120 is the figure for that input. The 120 is also the display cap. That coincidence is disclosed here; it does not move the published figure or the bound.

NFKC is not what creates the 79. The only NFKC character changes in this capture are U+00A8 DIAERESIS (1) and U+2026 HORIZONTAL ELLIPSIS (4). Whitespace collapse alone, without NFKC, is also 79/120, and the same span is present. NFKC without whitespace collapse is 41/120, because the layout line breaks remain. The rule requires both folds. ASCII-only whitespace collapse is also 79/120. Deleting whitespace instead of collapsing it is a different operation (66/99) and is not the rule.

A reading-order reconstruction that stripped the other column was not measured. It would not be the committed capture.

## Verification gaps

- This seat did not run `tools/absent-split.py`, `c1-count.py`, `c2-count.py`, or `c3-count.py`. Agreement with the committed S093 row is a comparison of integers, not a replay of the counter.
- The other 14 absent rows were not recomputed here.
- The PDF was not re-rendered. The measurement is the committed `.txt`, which is what the rule requires. `.raw` and `.pdf` were checked for size and magic only, not byte-identical to each other.
- No resume path was exercised. No lane file, git index, jj state, or shokuknow file was written. A failed preflight does not arise; mutation count outside this report is zero.
- No tool was installed. Pacman was not invoked.
