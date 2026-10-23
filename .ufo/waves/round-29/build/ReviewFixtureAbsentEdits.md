# Review — C1 fixture ABSENT ground truth: absent-fabricated and absent-one-word-edit

Seat: ReviewFixtureAbsentEdits, wave 1. Scope: in `corpus/fixtures/quote-reopen-r29/labels.tsv`
joined to `items.tsv`, the 8 items with label ABSENT and class `absent-fabricated` (4) or
`absent-one-word-edit` (4). Question per item: under the frozen normalization and boundary
rule in `corpus/evidence/round29/claims.md`, is the quote truly not present anywhere on the
live page of its registry row (any element a reader's text includes — sidebars, tables, list
items, footers — plus, contractually excluded, comments/script/style/noscript/template/head)?
The fixture files were only read, never edited.

## Method

1. Opened each item's registry URL with the `read` tool (5 distinct pages, all listed in
   the `source` column of `corpus/SOURCES.md`).
2. Re-verified every absence programmatically. Scratch checker
   `/fast/scratch/hyaku/chousa-r29/w1/ReviewFixtureAbsentEdits/checker.py` loads
   `corpus/evidence/round29/c1-count.py` via importlib and calls its reference functions
   (`_Text`, `norm`, `found`, `registry_url`), so HTML→text and normalization are
   byte-identical to the frozen contract. Fetch bounds mirror the counter: GET, UA
   `chousa-quote-reopen-counter/r29`, 30 s timeout, no credentials, ≤8 MiB read.
3. Absence must hold at three strictness levels: (1) frozen `found()` (boundary rule),
   (2) normalized substring with the boundary rule ignored, (3) casefolded substring
   (case ignored too). A hit at any level would be a label defect.
4. Positive control per page: the page's untouched true sentence must be found VERBATIM;
   otherwise the run is invalid, because a broken fetch would masquerade as absence.
5. Full runs: `scratch/run-fresh.log` (second, identical run; first run in the same
   transcript, exit 0, 1.97 s). Raw HTML cached per page under the scratch dir.

What contains what (extraction coverage): tables, footers, sidebars and list items are
ordinary text nodes and are included; only comments and script/style/noscript/template/head
content are dropped, by the frozen contract itself. The `read`-tool rendering truncates
long pages (e.g. Cochrane chapter 2), so verdicts rest on the full fetched HTML.

## Verdicts — 8/8 LABEL-OK

### absent-fabricated (label ABSENT)

| id | row | URL opened | verdict | page evidence |
|---|---|---|---|---|
| 08dc4035 | S008 | https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-02 | LABEL-OK | "SPIDER", "spider", "frame their questions": 0 hits, case-insensitive, full normalized page (150128 bytes, norm 63895 chars). Closest real text: "The FINER criteria ... These state that questions should be Feasible, Interesting, Novel, Ethical, and Relevant (Cummings et al 2007)." |
| 34a402d7 | S044 | https://docs.python.org/3/library/os.path.html | LABEL-OK | "resolves symbolic link", "before every path comparison": 0 hits, case-insensitive. Nearest real text says functions return False on symlinks, no automatic resolution: "Returns False for broken symbolic links" (exists()), "Return True if path refers to an existing path, including broken symbolic links" (lexists). |
| 72a76f58 | S013 | https://jsonlines.org/ | LABEL-OK | "carriage return", "must always end": 0 hits. Real requirement 3 is the opposite shape: "Including a line terminator after the last JSON value in a file is strongly recommended but not required." |
| db75f030 | S002 | https://ifcncodeofprinciples.poynter.org/the-commitments | LABEL-OK | "funding records", "every week": 0 hits. Sole `homepage` hit is unrelated (badge): "...encouraged to publish a badge on their homepage...". Real criterion: "have a page on their website detailing each source of funding accounting for 5% or more of total revenue for its previous financial year." |

### absent-one-word-edit (label ABSENT; exactly one word differs from the page)

| id | row | URL opened | verdict | page text vs item quote |
|---|---|---|---|---|
| f0de2354 | S044 | os.path.html | LABEL-OK | pathname → "filename". Page: "Return the longest common sub-path of each pathname in the iterable paths." True variant found VERBATIM under the frozen rule; "filename" edit absent at all three strictness levels. |
| 9ac20b6c | S008 | chapter-02 | LABEL-OK | seeks → "hopes". Page: "This is best done by clearly framing the questions the review seeks to answer." "hopes to answer": 0 hits; true variant found. |
| ddb2ed41 | S019 | https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-iv | LABEL-OK | periodically → "annually". Page: "All Cochrane reviews should be assessed periodically to determine whether an update is needed." "annual": 0 case-insensitive hits on the whole normalized page (norm 38514 chars); true variant found. |
| cda4cbb7 | S013 | jsonlines.org | LABEL-OK | removed "NOT". Page: "Like the JSON standard a byte order mark (U+FEFF) must NOT be included." "must be included" without NOT: 0 hits; true variant found. |

Why these cannot be boundary artifacts: the edits are inside words ("pathname"/"filename"),
change a low-frequency word ("hopes", "annually"), or delete a token ("NOT") that breaks
the whole span; a boundary-ignoring and case-insensitive search still finds nothing, and
each page's true sentence is found — so the extraction pipeline demonstrably works, and the
absence is real. D1 note (repair-first): nothing in these classes is the digit-glued-token
shape; that class is here only in truncated-token items outside this slice.

## Fetch receipts (from checker run, exit 0)

| row | status | type | bytes | norm chars | raw sha-256 (16) | control |
|---|---|---|---|---|---|---|
| S002 | 200 | text/html | 19482 | 10689 | 77f8767740eea5e7 | found |
| S008 | 200 | text/html | 150128 | 63895 | 900efef70997da81 | found |
| S013 | 200 | text/html | 4877 | 2303 | 198e1cfe99bd89e7 | found |
| S019 | 200 | text/html | 116560 | 38514 | 6e280a694709fc3f | found |
| S044 | 200 | text/html | 90223 | 21371 | d81f20038a4a15da | found |

## Admission self-check, honesty

- Only quotes copied from pages opened this run: all "page says" strings above, ≤25 words,
  access date 2026-10-23 (lane date).
- Runs: checker twice (identical output both times, exit 0); all commands bounded ≤240 s;
  no background jobs; no subagents; scratch dir
  `/fast/scratch/hyaku/chousa-r29/w1/ReviewFixtureAbsentEdits/` holds checker.py,
  results.json, run-fresh.log and the raw HTML caches.
- Bounds: leaf seat; GET only to the 5 registry URLs; no lane writes outside this report;
  fixture and counter untouched. A first draft of this report contained text I could not
  ground, so it was deleted and rewritten from run-fresh.log and results.json only.
- Incorrectly stylistic earlier: "pathname" vs "filename" — both D1-safe (no digit gluing).

## Residual risk and verification gaps

- Page content could change after 2026-10-23; verdicts are time-stamped to the fetch
  receipts above (raw HTML cached in scratch for audit).
- The frozen contract itself excludes HTML comments from page text; if the lane intended
  quote-provenance comments to count, that is a contract question, not a fixture-label
  defect, and it is not this seat's call.
- No LABEL-WRONG found on these 8 items; sibling slices (spliced, truncated-token,
  cross-attributed) are other seats' scope.

## Tooling directive

No tools were installed or updated this run (none needed: python3 stdlib sufficed).
