# Attack24 — hand-check of register row S093 (chousa slice, ordinal 3 by source)

Round 48, wave 1. Lane: chousa-shokunin. Scope: absent-defect-register.md (campaign
`corpus-expansion-1`), chousa slice. Row selection: chousa slice = 20 rows (`## By lane`,
register line 238); sorted by cited source (URL), ordinal 3 = **S093**, cited source
`https://aclanthology.org/2026.findings-acl.19.pdf` (sort order: S125, S110, S093, S116,
S108, …). Row text at register line 43.

## Verdict

- **Verifiable: yes.** Capture exists: `.qcache/4132ec1b265e60624523251f.txt` =
  `sha256(url)[:24]` + `.txt` (91,084 bytes; decodes UTF-8 cleanly, 90,692 chars; head =
  "How Grounded is Wikipedia? A Study on Structured Evidential Support and Retrieval").
- **Quote as recorded: absent (verbatim).** Census full quote (census JSON
  `quote-lint-full-v5.json` finding, chousa/S093, verdict ABSENT, fold null):
  `∼22% of claims in Wikipedia lead sections are unsupported by the article body; ∼30% of
  claims in the article body are unsupported by their (public) sources` (register table
  display truncates at `are un`). Not found in capture: verbatim False, whitespace-fold
  False, no-whitespace fold False.
- **Substance: fully grounded — not a fabrication.** Every fragment occurs verbatim:
  `(1) ∼22% of claims in Wikipedia lead sections` @1522, `are unsupported by the article
  body` @1576, `; (2) ∼30%` @1611, `of claims in the article body are unsupported` @1669,
  `by their (public) sources` @1723, `sources; and (3)` @1741.

## Cause of the miss (exact anchors)

Capture around 1500–1760:

```
(1) ∼22% of claims in Wikipedia lead sections
are unsupported by the article body; (2) ∼30%                           Cited source
of claims in the article body are unsupported
by their (public)
sources; and (3) real-world…
```

Three transcription defects, in order of impact:
1. **Elided enumerators:** the source sentence is enumerated `(1) …; (2) …; (3) …`;
   the quote omits `(1) ` (before `∼22%`, char 1522) and `(2) ` (before `∼30%`, char
   1613). Under whitespace/no-whitespace folds the gap `; (2) ` still breaks contiguity.
2. **Interleaved figure label:** extraction places `Cited source` (char 1648) between
   `∼30%` and `of claims`; even with enumerators restored, the raw capture is not
   contiguous there — matches require de-interleaving.
3. **Register display truncation:** table cell ends `are un` (mid-word); source continues
   `unsupported` (@1698).

## Consistency checks

- Round-47 lesson (`corpus/lessons/round-47.md` line 205) records S093 verdict
  `present`, with the same breaks named (`Cited source` @1648, elided `(2)` @1613,
  truncation `un`→`unsupported`). Its `present` is a word-order-modulo-interleavings
  reading; strict verbatim says absent-as-written. Calibration note: the two readings
  differ; this check reports the strict one and the grounded substance.
- Lane's own corrected form already exists: `corpus/SOURCES.md` line 100 (S090 row) and
  `corpus/knowledge/claim-support-test-r37.md` line 18 quote `are unsupported by the
  article body; (2) ∼30%` — i.e. the enumerator-inclusive form matches the capture, and
  span offsets in `corpus/evidence/round47/spans.tsv` (S090 rows: 1526, 1576, 1669,
  1723) agree with this check's anchors.
- Companion URL captures (`.qcache` keys for `…/2026.findings-acl.19/`, bare, `/abstract`)
  do not exist; the PDF capture is the only campaign artifact for this source.

## Commands run (decisive output)

- `python3` sort of 20 chousa rows by URL → ordinal 3 = S093.
- `python3` sha256(url)[:24] → 4132ec1b265e60624523251f; `.qcache` file present.
- Capture decode + fragment locate: `∼22%` @1526; `(1) ∼22% of claims in Wikipedia lead
  sections` @1522; `are unsupported by the article body` @1576; `; (2) ∼30%` @1611;
  `of claims in the article body are unsupported` @1669; `by their (public) sources`
  @1723; `sources; and (3)` @1741.
- Fold check: verbatim False; `re.sub(r"\s+","",…)` False; whitespace-collapse False;
  collapsed capture after `article body;` = `article body; (2) ∼30% Cited source of
  claims …`.

## Residual risk / gaps

- The capture is pdftotext-class extraction; enumerator and label placement are judged
  from this text layer only (no live fetch; L0 `8d77e6c1` open). If `(1)/(2)/(3)` were
  extraction artifacts rather than glyphs, the corrected quote would be contiguous modulo
  the `Cited source` interleave — cannot be ruled out without the original page, but the
  paper's own prose at chars 5986/6158 ("; (2) an even higher … proportion of body claims
  (∼30%)") repeats the numbered pattern, supporting genuine enumerators.
- I did not re-derive the other three quarantined rows (S094/S108/S110); this is S093
  only. No installs; scratch `/tmp/chousa-r48-Attack24` removed.
