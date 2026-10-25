# ReviewOpenS086 — lane source S086 opened, quotes located, contiguity-tested, landed rows checked

seat: reviewer (leaf, no dispatch). item: open the S086 capture, locate the four assigned quotes,
record offset / count / 120-char flanks / a ≤25-word verbatim anchor, and state which staged
sentences this source supports and which it contradicts. No fetch; no lane write but this file.
Scratch `/tmp/chousa-r46-ReviewOpenS086/` removed. Flanks are `repr`; offsets from `str.find`.

## Identity, size, commands

```
path   /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/1c15b611118dee97e4105fcf.txt
$ sha256sum …
c508913aba177ae4d33b29b7076f305bbac578a1ea11d39e30ddee2d787d563f   …/1c15b611118dee97e4105fcf.txt
$ wc -c -m -l …
  639 60030 60153    (lines=639  chars=60030  bytes=60153; bytes-chars=123 non-ASCII)
len(open(p).read()) = 60030
sha256("https://aclanthology.org/N18-1074.pdf")[:24] = 1c15b611118dee97e4105fcf  (filename == cache key -> S086 by construction)
capture:1   'FEVER: a large-scale dataset for Fact Extraction and VERification' — Thorne, Vlachos,
            Christodoulopoulos, Mittal; capture:4907 'Proceedings of NAACL-HLT 2018, pages 809–819'
```

Two-column PDF extraction: nearly every line is `<left column><runs of spaces><right column>`, so a
contiguous slice carries one column per line. Every quote below was found with `str.find`; every
count with `str.count`.

## Quote 1 — `used the June 2017 Wikipedia dump, processed`

```
offset 15269  count 1  line 157 col 1  len 44
before: 'vels of entity\nfrom information extracted from Wikipedia. We                           similarity and class membership.\n'
after : '                               This process resulted in claims (both extracted\nit with Stanford CoreNLP (Manning et al., 2014),        '
```
Verdict: **located**, contiguous, unique. Anchor (7 words): `used the June 2017 Wikipedia dump, processed`.
Contiguity: `capture:156` ends `…from Wikipedia. We`, then 27 spaces + `diagram to illustrate the
different levels of entity`, then `\n`, then `capture:157` `used the June 2017…`. The subject `We`
sits on the previous line, so `We used the June 2017 Wikipedia dump` is **not** a substring.

## Quote 2 — `recall of 72.36%`

```
offset 42011  count 1 for the exact string ('72.36' occurs 3x: 6762, 20403, 42021)  line 445 col 100
before: 'l rate of annotators\nsentence selection component decreased the accu-                 (see Section 3.4.2), who achieved '
after : '\nracy (N O S CORE E V) approximately 10% for both                 of evidence identified by the super-annotators.\ndecomp'
```
Verdict: **located**, contiguous, unique for the 10-char string. Anchor (7 words): `who achieved recall of 72.36%`.
Content: `capture:442-446` — the pipeline ablation, "the measured recall rate of annotators (see Section 3.4.2), who achieved recall of 72.36% of evidence identified by the super-annotators"; the primary statement is `capture:71-76` "resulting in inter-annotator agreement of 0.6841 in Fleiss κ … and 95.42% precision and 72.36% recall in evi-dence retrieval" — inter-annotator agreement, not a model score.

## Quote 3 — `We found that 91.2%`

```
offset 20847  count 1  line 215 col 62  ('91.2' occurs once)
before: 'them for accuracy of the labels\nfirst task. All annotators were native US English            and the evidence provided. '
after : '\nspeakers and were trained either directly by the             of the examples were annotated correctly. 3% of\nauthors, o'
```
Verdict: **located**, contiguous, unique. Anchor (8 words, one line): `and the evidence provided. We found that 91.2%` (offset 20820).
Contiguity: the continuation `of the examples were annotated correctly.` is the **right** column of
line 215, interrupted by `\n` + left column `speakers and were trained either directly by the`.

## Quote 4 — the 31.75 / 16.82 / 12.15 passage

One left-column paragraph (`capture:61-66`) interrupted line by line by the right-column Rodney King
example. Each number located, unique, contiguous only inside its own line.

```
31.75  off 5534  count 1  line 61 col 15
  before: ' the USA.\nnot the sentence from which original claim was                 [wiki/Los Angeles Riots]\nextracted and thus in '
  after : '% of the claims more                    The 1992 Los Angeles riots,\nthan one sentence was considered appropriate ev-    '
  anchor (7 words): 'thus in 31.75% of the claims more'
16.82  off 5842  count 1  line 64 col 1
  before: 'ms require composition of evidence                     were a series of riots, lootings, ar-\nfrom multiple sentences in '
  after : '% of cases. Fur-                   sons, and civil disturbances that\nthermore, in 12.15% of the claims, this evidence   '
  anchor (7 words): 'from multiple sentences in 16.82% of cases.'
12.15  off 5929  count 1  line 65 col 11
  before: ', ar-\nfrom multiple sentences in 16.82% of cases. Fur-                   sons, and civil disturbances that\nthermore, in '
  after : '% of the claims, this evidence                   occurred in Los Angeles County, Cali-\nwas taken from multiple pages.   '
  anchor (7 words): 'in 12.15% of the claims, this evidence'
```
Verdict: **all three located**; the grammatical passage is contiguous nowhere. The raw interleaved window `s[5500:5975]` (475 chars) contains all three numbers *and* all three anchors (verified `True/True/True` at slice offsets +31, +315, +426) but is not a readable sentence: `spans.tsv` therefore needs one row per number with its per-line anchor, because a single quote string carrying two of the three numbers does not exist in this capture.

## Staged sentences S086 supports (figures re-verified here)

`…/merge/chousa/knowledge/corpus/knowledge/evidence-pool-versioning-r39.md`
- `"We used the June 2017 Wikipedia dump" (S121)` — supported in substance, quote cross-line (Quote 1).
- `0.6841 in Fleiss kappa for claim verification classification` — supported: `capture:1749` "The
  claims are classified as S UPPORTED, R E - FUTED or N OT E NOUGH I NFO by annota- tors achieving
  0.6841 in Fleiss κ." (capture spells `κ`; the same figure recurs at `capture:71`).
- `95.42% precision and 72.36% recall in evidence retrieval` — supported; paper's own wording
  `capture:20403` "the precision/recall was 95.42% and 72.36% respectively" after "We compared the
  regular annotations against this set of evidence". The staged Unknown's "measured against one
  super-annotator's exhaustive set" is exactly right.
- `31.75 % / 16.82 % / 12.15 %` sentence — supported in substance and in every number.
- `Of 227 examples annotated by the authors` — supported: `capture:20637` "we chose 227 exam- ples
  and annotated them for accuracy of the labels and the evidence provided".
- `all except two annotators achieved > 90 % precision and all but 9 achieved recall > 70 %` —
  supported: `capture:21750` "When compared against the super-annotators, all" + `except two
  annotators achieved > 90% precision` + `and all but 9 achieved recall > 70% in evidence retrieval`
  (paper writes `90%`/`70%`, no space).
- Amendment entry: nothing in S086 bears on S127/S128; the amendment's Unknown ("the round-4
  finding — 72.36 % recall on FEVER — has no successor figure here") is consistent, not contradicted.

## Staged sentence S086 CONTRADICTS

One. Staged Inference: "the authors' own validation puts **label correctness** at 91.2 %". Capture
`capture:20637-20850`: "we chose 227 exam-ples and annotated them for accuracy of the **labels and
the evidence provided**. We found that 91.2% of the **examples** were annotated correctly. 3% of the
claims were mistakes in claim generation…". The figure is over *examples*, covering label **and**
evidence correctness, and the next sentence's separate 3 % claim-generation error is omitted by the
staged text. **Resolved in the landed entry** (`corpus/knowledge/evidence-pool-versioning-r39.md:15`):
"its own label-validation pass found that `We found that 91.2%` of the sampled examples were
annotated correctly" — scope now correct.

## Staged quote forms that are NOT substrings (each verified `present=False`)

`We used the June 2017 Wikipedia dump` · `95.42% precision and 72.36% recall in evidence retrieval` (`evi-\ndence`) · `91.2 % of the examples were annotated correctly` · `all except two annotators achieved > 90 % precision` · `31.75 % of claims more than one sentence was considered appropriate evidence` · `16.82 % of claims required evidence composed of multiple sentences` · `12.15 % took evidence from multiple pages` · `Ideally, exhaustive search strategies` — the last is absent from the whole capture (count 0), so the staged Unknown's quoted "paper's own framing" cannot be an S086 span at all. All three the landed entry uses as spans were corrected to the contiguous anchors, recorded at `…-r39.md:29`.

## Landed state, checked after the entry and manifest appeared

```
spans.tsv S086 rows: 15269 / 42011 / 20847  capture_sha256 c5089134…563f  (matches sha256 above)
S086-1..3: capture_bound True | quote in span True | quote in entry True
SOURCES.md: rows S085–S089 now at 96–100 (11-cell check is the counter's job, not re-derived here)
```
Findings on the landed artefacts:
- **Counter state.** `git diff corpus/evidence/round46/c3-count.py` (+8/−2) is hardening only — a span path that is absolute or contains `..` is skipped, and a non-integer offset `continue`s. The three leg expressions are unchanged, so the frozen rule still decides the verdict; the line cites below are the current file's.
- **M1 (medium, lane-wide, claim strength — not a counter failure).** All 11 span files equal their
  quote byte for byte (`span_len == quote_len` for every row: 23, 46, 44, 16, 19, 38, 23, 38, 55, 42,
  33). With `span == quote`, `QUOTES_IN_SPAN` is entailed by `CAPTURE_BOUND` (`c3-count.py:117,127`:
  `quote in span` and `ct[o:o + len(span)] == span`), so that leg tests nothing the capture-bound leg
  does not already test, and no span shows the quote inside a readable passage. The counter still
  passes as frozen; the claim's wording ("each span file is the exact slice") is satisfied, but the
  intent — a quote adjudicated against surrounding captured text — is not exercised. For the next
  round: require `len(span) > len(quote)` (e.g. ±80 chars) or fail the row.
- **M2 (low, same root).** Because a span carries no context, the `capture_sha256` column is the only evidence that the offset was chosen from a reading rather than found by search — not fixable by the counter as frozen, named as a limit.
- **No misattribution found in the landed entry.** `…-r39.md:15` "reports `recall of 72.36%` for evidence retrieval" is exactly the paper's own frame (`capture:71-76`), not a model metric.

## Residual risk / gaps

- Line-final `-` is a real soft hyphen in the extraction: `evi-/dence`, `exam-/ples`, `ret-/rieval`,
  `accu-/racy`, `annota-/tors` can never be quoted whole. Spans for this source must be line-internal.
- 72.36 % appears at 6762, 20403 and 42021/42011; a span row pins one offset, and 42011 is the one
  whose subject (annotator recall) the entry's Unknown relies on.
- The staged amendment's S127/S128 sentences were not checked against their captures by this seat.
- No live read performed or needed; no tool installed or upgraded.
