# QuarReg093 — quarantine hand-check (§10), register row `chousa` S093

Seat: L1Chousa47.QuarReg093 (leaf). Round 47 wave 1. No fetch, no dispatch, no install.

## Item
Hand-check every backticked quote in the quote cell of absent-defect-register row
`| chousa | round2 | S093 | payload-absent |` against the capture of its URL
(lane id S090), and give a present/absent/unverifiable verdict plus a unique anchor.

## Inputs (read-only)
- Register: /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md
  sha256 `5afe1810a6c3d62f37987b575a954f5b1197daa23005d4bb2f1d982f64bad833`; row at line 43, lane cell `chousa`.
- Capture: /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/4132ec1b265e60624523251f.txt
  sha256 `2f8047a877c390f819c83ee1079ca8229ab16ce461c5f2f45304b33931224997`; 91084 bytes, 90692 chars.
  The capture filename is the URL key: `printf '%s' https://aclanthology.org/2026.findings-acl.19.pdf | sha256sum | cut -c1-24` → `4132ec1b265e60624523251f`.
  Capture head: "How Grounded is Wikipedia? A Study on Structured Evidential Support and Retrieval", Walden, Ricci et al., Johns Hopkins.
- All offsets below are 0-based Python `str` (Unicode code point) offsets into the capture. They are not byte offsets, because `∼` (U+223C) takes 3 bytes.

## Register row (line 43, verbatim)
```
| `chousa` | round2 | S093 | `payload-absent` | https://aclanthology.org/2026.findings-acl.19.pdf | `∼22% of claims in Wikipedia lead sections are unsupported by the article body; ∼30% of claims in the article body are un` | cited source, companion URLs and local artifacts were all checked; the quote is in none of them |
```
The cell has one backticked quote. It ends mid-word (`un`), so it was cut off at 120 characters.

## Commands and decisive output
1. `grep '| S093 |'` on the register gives three rows (chousa line 43, kagi line 79, revenger line 163). Only line 43 is in scope.
2. Exact substring search of the quote in the capture: `exact -1`. Whitespace-collapsed search: `wsnorm -1`. A mechanical "absent" result is therefore reproducible.
3. Hit positions: `22%` [1527, 5809]; `30%` [1618, 6159]; `article body` [1599, 1686, 2579, 32507].
4. Token alignment, starting at the token `∼22%`@1526 and matching each quote word in order (the last word is matched as a prefix):
```
∼22%@1526 of@1531 claims@1534 in@1541 Wikipedia@1544 lead@1554 sections@1559 are@1576
unsupported@1580 by@1592 the@1595 article@1599 body;@1607 ∼30%@1617 of@1669 claims@1672
in@1679 the@1682 article@1686 body@1694 are@1699 un@1703(=unsupported)
skipped capture tokens: ('(2)',1613) ('Cited',1648) ('source',1654)
```
All 22 of 22 quote words occur in order, with no word changed.

## Capture slices carrying each part (verbatim `repr`)
- [1526:1581] `'∼22% of claims in Wikipedia lead sections\n        are u'`
- [1581:1620] `'nsupported by the article body; (2) ∼30'`
- [1620:1700] `'%                           Cited source\n        of claims in the article body a'`
- [1700:1720] `'re unsupported\n     '`
- Wider context [1400:1800]: `'...We show that:                   support\n        (1) ∼22% of claims in Wikipedia lead sections\n        are unsupported by the article body; (2) ∼30%                           Cited source\n        of claims in the article body are unsupported\n        by their (public) sources; and (3) real-world\n...'`

## Why the mechanical check failed (normalisation applied)
- Column interleave: `support` (just before 1522) and `Cited source` (1648–1660) are labels from the Figure 1 column. The PDF text layer runs them into the abstract lines, which is the same failure mode that rounds 43 and 46 found.
- Line breaks and runs of whitespace (1567–1575, 1660–1668). These are whitespace-only.
- Enumerator `(2)` at 1613: the source has it and the quote leaves it out with no ellipsis (the leading `(1)` at 1522 is outside the quoted span). This is an editorial elision in the quote. It is not a quote word that is missing or changed in the capture. It is recorded here so the lane does not reuse the quote as a contiguous span.
- Trailing `un` is a truncation of `unsupported`@1703.
- No hyphen splits and no `\kappa`-style markup in the quoted span.
- A second, paraphrased statement of the same finding sits at 5700–6300 (`lead claims (∼22%) are unsupported by the\n ... body of the same article`). It is not the quoted wording and is not used for the verdict.

## Verdict
- quarantine: register `S093` (https://aclanthology.org/2026.findings-acl.19.pdf) verdict: `present` — all 22 quote words occur in order in capture 4132ec1b…txt at chars 1526–1705, with only whitespace, the interleaved figure label `Cited source`@1648, the elided enumerator `(2)`@1613 and the truncated last word (`un`→`unsupported`@1703) in between.

## Anchor quote (contiguous, unique, 7 words)
`∼22% of claims in Wikipedia lead sections`, at char 1526, unique (`re.finditer` → [1526]); it sits on one line, so no normalisation is needed.
Other unique contiguous runs: `are unsupported by the article body; (2) ∼30%`@1576 [unique] and
`of claims in the article body are unsupported`@1669 [unique].

## Findings by severity
1. (medium, register) The register's `payload-absent` for chousa S093 is a false mechanical verdict. Its cause is a figure-column interleave plus an unmarked enumerator elision, so it is not a fabrication. Route: §10 quarantine line above. The register is read-only and was not edited.
2. (low, quote hygiene) The register quote leaves out `(2)` without an ellipsis. Any lane entry that cites this passage for S090 should use one of the contiguous anchors above, or mark the elision, so that the char-offset anchor check (C3) resolves.

## Residual risk and verification gaps
- The check covers only the on-disk capture. The live PDF was not read (no fetch allowed), so capture fidelity to the published PDF is assumed.
- `grep merge/chousa` for `22%` found no staged use of this quote, so I did not check whether a staged S098 row depends on it.
- No tools were installed. Scratch dir /tmp/chousa-r47-QuarReg093/ was deleted.
