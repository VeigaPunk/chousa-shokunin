# QuarantineS093 — hand-check, register row `chousa` round2 `S093`

Seat: L1Chousa48.QuarantineS093 (leaf). Round 48 wave 2. No fetch, no dispatch, no install.

## Verdict

**`present`** — the row's quoted span is in the cited source's on-disk capture; the `payload-absent` class is a false mechanical verdict, not a fabrication.

## Row under test

- Frozen slice: `.ufo/waves/round-48/assimilation/quarantine-slice` line 7: `S093   \`payload-absent\``.
- Register: `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`, line 43, byte offset 6220; file 83,621 bytes, sha256 `5afe1810a6c3d62f37987b575a954f5b1197daa23005d4bb2f1d982f64bad833`:
  `| \`chousa\` | round2 | S093 | \`payload-absent\` | https://aclanthology.org/2026.findings-acl.19.pdf | \`∼22% of claims in Wikipedia lead sections are unsupported by the article body; ∼30% of claims in the article body are un\` | … |`
  (120-char-truncated tail of the staged quote.)
- `grep ' S093 '` on the register yields 3 rows (chousa:43, kagi:79, revenger:163); only line 43 is in scope.
- Census `quote-lint-full-v5.json`: `chousa round2 S093` binds the ACL URL with `"binding":"id"`; the ABSENT quote is the full staged sentence `…are unsupported by their (public) sources`. The three other S093 quotes (Definitions 1–2, prompt) are `folded/whitespace` — present.

## Identity (register id → lane row)

- Register/round2 `S093` = staged `lanes/chousa/round2/SOURCES-PROPOSED.md` **S098** (Gate — S098, line 81: URL + "Opened 2026-10-23 (HTTP 200, 2,171,480 bytes; pdftotext -layout, 91,084 bytes)"; quote cell line 87 is the full sentence) = merged `corpus/SOURCES.md` line 100 **S090** (claimed offsets: char 1526, 1576, 1669 — all verified below).

## Capture (on-disk only)

- `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/4132ec1b265e60624523251f.txt`
  - `printf '%s' <url> | sha256sum | cut -c1-24` → `4132ec1b265e60624523251f` — filename is the URL key.
  - 91,084 bytes / 90,692 chars; sha256 `2f8047a877c390f819c83ee1079ca8229ab16ce461c5f2f45304b33931224997`.
  - `.raw` ≡ `.pdf` (`cmp` identical; 2,171,480 bytes, sha256 `15673fb43980fa4bfbe3c98811f9a0b09995abb70be6a1b9e663d39ffcbc3ac0`), matching the gate's logged download size.
  - Provenance check: local `pdftotext -layout 4132ec1b….pdf` reproduces the `.txt` **byte-identical** (sha256 `2f8047a8…` again) — the capture is the stored PDF's own text layer. All offsets are 0-based Python `str` code-point offsets.

## Commands and observed output

1. `t.find(quote)` on full staged quote → `-1`; on register truncation → `-1`.
   `re.sub(r'\s+',' ',…)` whitespace-fold → `-1`. → mechanical ABSENT reproduces.
2. `t[1400:1820]`:
   `'…We show that:                   support\n        (1) ∼22% of claims in Wikipedia lead sections\n        are unsupported by the article body; (2) ∼30%                           Cited source\n        of claims in the article body are unsupported\n        by their (public) sources; and (3) real-world\n…'`
3. Token alignment of the full 26-word quote, in order, span chars 1526–1749:
   `∼22%@1526 of@1531 claims@1534 in@1541 Wikipedia@1544 lead@1554 sections@1559 are@1576 unsupported@1580 by@1592 the@1595 article@1599 body;@1607 ∼30%@1617 of@1669 claims@1672 in@1679 the@1682 article@1686 body@1694 are@1699 unsupported@1703 by@1723 their@1726 (public)@1732 sources;@1741`
   Skipped capture tokens only: `('(2)',1613) ('Cited',1648) ('source',1654)` — no quote word missing or altered.
4. Anchors (`re.finditer`, all unique): `∼22% of claims in Wikipedia lead sections`@1526 [1 hit]; `are unsupported by the article body; (2) ∼30%`@1576 [1]; `of claims in the article body are unsupported`@1669 [1]. Lane's three claimed offsets all land exactly.
5. Register sha256 `5afe1810…` and capture sha256 `2f8047a8…` match the round-47 adjudication (`w1/QuarReg093.md`) — same bytes, same verdict, independently re-derived.

## Reason

The PDF text layer interleaves Figure-1 column labels (`support`@~1515, `Cited source`@1648–1660) and keeps the enumerator `(2)`@1613 inside the quoted span, while the staged quote elides `(2)` without an ellipsis. No exact/whitespace/case/punct fold can bridge arbitrary injected tokens, so all eleven folds miss and the row lands in `payload-absent` mechanically. Every quoted word is present, verbatim, in order: **present**, with the caveat that the quote is not a contiguous span (elided `(2)` + interleave) — lane entries should cite the contiguous anchors above or mark the elision. Companion URLs: none staged (`local: null`, gate names only the PDF). A paraphrased restatement at chars ~5750–6300 is a different wording, not the quote.

## Findings by severity

1. (medium, register/slice) False-positive `payload-absent` for chousa S093: quote present; the row is a precision counterexample to any "quarantined = fabricated" reading, consistent with the frozen R48-C1 motivation that whitespace-fold is insufficient (this failure mode needs column-interleave tolerance, not more folds). Register/slice not edited (read-only inputs).
2. (low, quote hygiene) `(2)` elided without ellipsis in the staged quote and its register truncation (`…are un`). Anchors for reuse: @1526, @1576, @1669.

## Residual risk / gaps

- Capture fidelity to the live PDF is assumed (no fetch allowed; L0 `8d77e6c1` open). The capture is internally consistent: raw==pdf, and the staged gate's logged sizes match the cached bytes.
- Round-47 `w1/QuarReg093.md` reached `present`; this check re-derived it from bytes, not from that report.
- Scratch `/tmp/chousa-r48-QuarantineS093/` used for the pdftotext reproduction; deleted after verification.
