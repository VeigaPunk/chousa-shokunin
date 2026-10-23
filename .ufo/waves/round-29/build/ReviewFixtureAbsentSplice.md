# Review — fixture ground truth: absent-cross-attributed and absent-spliced

Seat: ReviewFixtureAbsentSplice, round 29 wave 1, lane chousa-shokunin.
Scope: the 8 ABSENT items of classes `absent-cross-attributed` (4) and
`absent-spliced` (4) in `corpus/fixtures/quote-reopen-r29/labels.tsv` joined to
`items.tsv`. Question: is each ABSENT label correct under the frozen v2
normalization and boundary rule in `corpus/evidence/round29/claims.md`, when the
item is re-opened against its own registry row's live page?

Verdict up front: **8 of 8 LABEL-OK. No fixture defect found in these two
classes. Nothing to change.**

## Method

- Fetched each item's own registry-row URL (GET only, UA
  `chousa-quote-reopen/1.0 lane-review`, `--max-time 45`, one fetch each) from
  `corpus/SOURCES.md`. All 8 returned `http=200`, `text/html`:
  S002 5623 bytes; S003 107322; S008 38126; S013 1832; S019 28379; S020 62739;
  S038 51239; S044 14297. No UNREACHABLE path is exercised by these items.
- Opened all 7 distinct own-row pages with the `read` tool as corroboration.
  Note: the S020 reader view came back W3C-API-mediated and metadata-only; the
  S020 text check below rests on the served HTML body fetched by curl (same
  URL, same date, 200).
- Reference check in scratch (`/fast/scratch/hyaku/chousa-r29/w1/ReviewFixtureAbsentSplice/check.py`,
  `check2.py`): html.parser extraction with the frozen block list and dropped
  `script style noscript template head`, NFKC, quote-char mapping, zero-width
  deletion, whitespace collapse, case-sensitive search with the alphanumeric
  boundary rule. `check2.py` re-ports the counter's exact reference-extraction
  semantics (`c1-count.py` `_Text`/`norm`/`found`) and re-derives every
  verdict; both models produce byte-identical normalized text on all 8 pages,
  and verdicts agree. Quotes were read from `items.tsv` bytes, not retyped.
- Ran twice after one key-name fix; final runs: `python3 check.py` exit 0,
  `python3 check2.py` exit 0.

## absent-cross-attributed — own row is deliberately the wrong page

| item | row | own-page result | true page |
|---|---|---|---|
| 4ba93361 | S002 | 0 substring hits, 0 boundary hits | 1 boundary hit on S003 |
| 5d313002 | S019 | 0 substring hits, 0 boundary hits | 1 boundary hit on S008 |
| 886813cd | S038 | 0 substring hits, 0 boundary hits | 1 boundary hit on S044 |
| 13fe59fb | S020 | 0 substring hits, 0 boundary hits | 1 boundary hit on S013 |

Each wrong page lacks even a substring stem (probe without the last word: 0
hits), so no boundary artifact can rescue a match. Each true page holds the
sentence with non-alphanumeric characters on both sides. Located quotes (all
accessed 2026-10-23):

- 4ba93361, true page https://hapgood.us/2019/06/19/sift-the-four-moves/ :
  "Since 2017, we've been teaching students with something called the Four
  Moves. Our solution is to give students and others a short list"
- 5d313002, true page https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-02 :
  "This is best done by clearly framing the questions the review seeks to
  answer. The focus of any Cochrane review should be on questions"
- 886813cd, true page https://docs.python.org/3/library/os.path.html :
  "Unlike a Unix shell, Python does not do any automatic path expansions.
  Functions such as expanduser() and expandvars() can be invoked"
- 13fe59fb, true page https://jsonlines.org/ :
  "Like the JSON standard a byte order mark (U+FEFF) must NOT be included.
  2. Each Line is a Valid JSON Value"

Byte notes: the apostrophe in 4ba93361's quote is ASCII 0x27, and 13fe59fb's
"(U+FEFF)" is literal ASCII text, not the codepoint, so the zero-width
deletion rule never touches it. Both normalize identically either way.

## absent-spliced — own row is the true page; omitted words verified in between

All 4 full quotes have 0 substring hits (so 0 boundary hits) on their own
pages; both fragments of each are boundary-present; the between-text is real
page words, never empty, never only punctuation. Fragment-join reconstruction
matches the TSV quote bytes for all 4.

| item | row | between-text (omitted words) |
|---|---|---|
| 2c526a9f | S044 | " in the iterable paths. " (4 words) |
| b2fa9757 | S013 | " that may be processed one record at a time. " (9 words) |
| b58e8ca4 | S008 | " when developing research questions. " (4 words) |
| 1d797926 | S019 | " are more stable, and some research questions " (7 words) |

Located quotes (accessed 2026-10-23):

- 2c526a9f, https://docs.python.org/3/library/os.path.html :
  "Return the longest common sub-path of each pathname in the iterable paths.
  Raise ValueError if paths contain both absolute and relative pathnames"
- b2fa9757, https://jsonlines.org/ :
  "JSON Lines is a convenient format for storing structured data that may be
  processed one record at a time. It works well with unix-style"
- b58e8ca4, https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-02 :
  "The FINER criteria have been proposed as encapsulating the issues that
  should be addressed when developing research questions. These state that
  questions should be"
- 1d797926, https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-iv :
  "Some areas of research evolve rapidly, whereas others are more stable, and
  some research questions stop being relevant to decision makers."

Word counts of the 8 quotes: 12, 14, 12, 13, 18, 18, 21, 14 — all under the
25-word TOO_LONG threshold, so verdict ordering cannot interfere.

## Fidelity of the check against the frozen reference

`c1-count.py` reference functions read at lines 56-145 (read-only). My first
model suppressed block spaces inside dropped subtrees; the reference emits
them there. That difference can only insert whitespace, which normalization
collapses — and on these 8 pages the two models' normalized texts are
byte-identical (`check2.py` prints `True` per page), so the modeling choice is
immaterial here. All 8 verdicts were re-derived under the reference `found()`
semantics with the same outcome.

## Residual risk and gaps

- Labels are tied to page content as served on the access date; later page
  edits could flip any label. That is inherent to the claim design (claims.md,
  "Not claimed" covers later page change) and is not a label error today.
- S020 absence rests on one curl-fetched served body plus the normalized-text
  search (stem probe also 0); the reader view added no text for this page.
- The checker is review-side scratch code, not the claim's tool; no fixture,
  counter, or claims file was opened for writing, and no lane state was touched.
- One fetch per page per model; no retries were needed (all first fetches 200).
