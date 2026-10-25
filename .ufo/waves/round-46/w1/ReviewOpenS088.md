# ReviewOpenS088 — lane source S088 (AVeriTeC dataset page) opened, quotes located

item: open S088 this round and locate the quotes that ground its Registry row.
source doc: `https://fever.ai/dataset/averitec.html` (AVeriTeC dataset page, static export)
capture: `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/b73f7e8dd5b0ace740e48046.txt`
capture sha256: `603f9b42ccbafcb8885679e905b2aed5946fb211c29bba0423e27558cc87528b`
length: **12775 bytes = 12775 chars** (0 non-ASCII code points → char offset == byte offset for every span below)
capture name ↔ URL: `sha256("https://fever.ai/dataset/averitec.html")[:24]` = `b73f7e8dd5b0ace740e48046` — **matches the file name exactly** (`…averitec.html/` → `c15519cf…`, `http://…` → `9525c517…`, so the no-slash https form is the bound one).

## Verdicts

| # | Quote | Offset | Occurrences | Verdict | Field |
|---|---|---|---|---|---|
| Q1 | `An archive.org link for the source url` | 3929 | 1 | **located** | evidence answer (`cached_source_url`) |
| Q2 | `Our best estimate for the date the claim first appeared` | 2904 | 1 | **located** | claim (`claim_date`) |
| Q3 | `The Claims in AVeriTeC are classified into four labels: "Supported", "Refuted", "Not\n Enough Evidence", "Conflicting Evidence/Cherry-picking".` | 1037 (len 142, ends 1178) | 1 | **located** | claim (`label`) — value set, not a field description |
| Q4 | `Where possible, an archive.org link to the original claim url` (asked: does the claim-level archive carry a qualifier) | 3185 | 1 | **located** | claim (`cached_original_claim_url`) |

`"Conflicting Evidence"` alone occurs 3× at 1142, 9466, 9672; only 1142 is inside the four-label
sentence (1037–1178). The other two are the worked-example heading and its `"label"` value.

## Anchors (≤25 words, verbatim, with ±120 char context)

**Q1 @3929** — anchor `An archive.org link for the source url` (7 words, slice sha256 `dd7324c4a21ba4d5fbbc14787e7e0a5246b92c10418804091603e57d727faaf0`).
```
-120: s abstractive, extractive, boolean, or unanswerable. \n\n source_url : The answer to the question. \n\n cached_source_url : 
+120: . \n\n source_medium : The medium the answer appeared in, e.g. web text, a pdf, or an image. \n\n \n \n\n \n \n\n \n Below are four
```
**Q2 @2904** — anchor `Our best estimate for the date the claim first appeared` (10 words, slice sha256 `8454397355aa63c419bc4ec852cfb187e7552e026e332e863c59a73068bedc15`).
```
-120: cation : A textual justification explaining how the verdict was reached from the question-answer pairs. \n\n claim_date : 
+120: . \n\n speaker : The person or organization that made the claim, e.g. Barrack Obama, The Onion. \n\n original_claim_url : If
```
**Q3 @1037** — full sentence (16 words, slice sha256 `9b2e76fdbc91931d9a855318c78d00280756ce5c926824ee1b8265201e70a6a8`); it contains a newline after `"Not`.
```
-120: vidence available online, as well as textual justifications explaining how the evidence combines to\n produce a verdict. 
+120: The dataset also contains several fields of\n metadata such as the speaker of the claim, the publisher of the claim, the
```
Single-line sub-anchors, for a row that cannot carry the newline: `four labels: "Supported", "Refuted", "Not` @1080 (5 words); `Enough Evidence", "Conflicting Evidence/Cherry-picking".` @1123 (4 words); `Conflicting Evidence/Cherry-picking` @1142 (2 words).

**Q4 @3185** — anchor `Where possible, an archive.org link to the original claim url` (10 words, slice sha256 `15e6fd1d12d16abac3f51cb1c793bd1dce97f53bd5fa9d3b65fc893f2d00c968`).
```
-120: claim_url : If the claim first appeared on the internet, a url to the original location. \n\n cached_original_claim_url : 
+120: . \n\n fact_checking_article : The fact-checking article we extracted the claim from. \n\n reporting_source : The website or
```

## Qualifier answer

**Yes, at the claim level only.** `cached_original_claim_url : Where possible, an archive.org link to the
original claim url.` (3185) carries the hedge `Where possible`; the evidence-level twin
`cached_source_url : An archive.org link for the source url.` (3929) carries **none**. A Registry row that
says "the archive fields are best-effort" is wrong on the evidence level — this is the same split the lane
already mined in S082 (`corpus/SOURCES.md:92`), so S088's row must restate it, not blur it.

Two further capture facts a row may rely on: `AVeriTeC (Automated Verification of Textual Claims)` is "a dataset of 4568 real-world claims covering fact-checks by 50 different organizations" (775, 823); and the word `revision` occurs **0** times in the whole capture — the page's binding is an archive copy, never a revision id.

## Which staged sentences S088 actually supports

Staged files: `…/merge/chousa/knowledge/corpus/knowledge/evidence-pool-versioning-r39.md` (BASE) and
`…-amendment-2026-10-23.md` (AMEND). S088 is **the same document as staged S127** (same URL, same digest) —
so every `S127` citation in AMEND is S088 re-bound **by document**, not by id arithmetic.

Supported by S088:
- AMEND Obs 1 — "every evidence answer carries a `source_url` **and** a `cached_source_url`, described as
  'An archive.org link for the source url'" — **the field description is supported (Q1)**, the universal is
  contradicted (below).
- AMEND Obs 1 — "the claim's own location is paired the same way through `cached_original_claim_url`, 'Where possible, an archive.org link to the original claim url'" — **supported (Q4)**; the word "location" is wrong for a *url* field, an imprecision to fix while editing.
- AMEND Obs 2 — `claim_date` = "Our best estimate for the date the claim first appeared" — **supported (Q2)**.
- AMEND Obs 3 — "classified into four labels: 'Supported', 'Refuted', 'Not Enough Evidence', and 'Conflicting Evidence/Cherry-picking'" — **supported in substance (Q3), misquoted in form**: the capture has no `and` before the fourth label.
- AMEND Obs 1's worked example (live Wikipedia URL beside the `web.archive.org/web/20230323135844/…` capture)
  — **supported**; both strings are in the Supported example.

Not supported by S088 (belongs to S128/S089): the "temporally constrained evidence annotation" sentence, the
κ=0.742 / 74.7 % figures, and the "text-and-image claims" Unknown bullet. BASE's observations are all
S120/S121/S122 material; S088 supports **none** of them, and BASE's Unknown ("the newer FEVER-family
releases … were not opened, and whether any of them adds a revision binding is unknown", BASE:86) is not
contradicted — it is **superseded**: S088 is that AVERITEC 2024 page and it carries a snapshot binding with
no revision field (`revision` count 0).

## Staged sentences S088 CONTRADICTS (both sides)

1. **Universal over the evidence field.** AMEND (Obs 1): "In AVeriTeC every evidence answer carries a
   `source_url` **and** a `cached_source_url`". Capture, Not Enough Evidence example, char 9375:
   `{ "answer": "No answer could be found.", "answer_type": "Unanswerable", "source_url": "", "source_medium": "" }`
   — the object has **no** `cached_source_url`. Corpus-wide in this capture: 8 `"answer_type"` objects, 7
   `"cached_source_url"`. The lane's own S084 row (`SOURCES.md:94`) says 1,491 of 7,572 answers carry no
   archive field. Correction: "each evidence answer that names a source carries a `source_url` and, per
   field description, a `cached_source_url`".
2. **Which claims lack a claim-level snapshot.** AMEND (Unknown): "the examples show
   `cached_original_claim_url: null` for claims that first appeared on the internet". Capture contradicts
   both directions: the one claim that *did* first appear on the internet (Not Enough Evidence, 8237) has
   `original_claim_url: "https://www.youtube.com/watch?v=xb0LoEBc6_o…"` and a **non-null**
   `cached_original_claim_url: "https://web.archive.org/web/20230420110107/https://www.youtube.com/…"`;
   the nulls (4422, 6206, 9927) sit on claims with `original_claim_url: null` (a convention speech, media
   outlets). Correction: the examples show the nulls on claims with no claim URL, and the single internet
   claim is cached — the "where possible" hedge is the only supported statement.
3. **Qualifier scope.** AMEND (Unknown) heading "The archive captures are 'where possible'" overgeneralizes:
   the hedge is on `cached_original_claim_url` only; `cached_source_url`'s description is unconditional
   (Q1 vs Q4 above). Correction: name the claim-level field.
4. **Label spelling.** AMEND writes `Conflicting Evidence/Cherry-picking`; that is the header sentence's
   spelling (1163), but the page's own example records `"label": "Conflicting Evidence/Cherrypicking"`
   (9672) and its heading likewise (9487). A row quoting the label must say which spelling it pins.
5. **Q3 quotation form.** AMEND inserts `and` inside the quotation (`…"Not Enough Evidence", and
   "Conflicting Evidence/Cherry-picking"`). The capture is `…"Not\n Enough Evidence", "Conflicting
   Evidence/Cherry-picking".` Remove the insertion; a quoted label list must be verbatim.

## Span-manifest hazards (for the builder of `corpus/evidence/round46/spans.tsv`)

`c3-count.py` requires each row's quote to be `in` the span file **and** `in` the entry text, and the span
file to equal `capture[offset:offset+len(span)]` exactly. Consequences measured here:

- Only **Q1** is a contiguous substring of the staged AMEND today. Q2 is broken by the entry's reflow
  (`"Our best\n  estimate …"`, AMEND:20–21); Q4 is broken (`"Where\n  possible …"`, AMEND:15–16); Q3 is both
  reflowed and carries the inserted `and` (AMEND:23–25). Using them as-is gives `QUOTES_IN_ENTRY` failures;
  reflow-only anchors that survive both sides already exist — `estimate for the date the claim first
  appeared` @2913 (in AMEND), `archive.org link to the original claim url` @3204 (in AMEND), but both start
  mid-phrase and are poor anchors. Preferred fix: reflow the entry quotes and drop the `and`, then anchor on
  the full phrase.
- The manifest's `cap_sha` column is the **whole-capture** digest, so the S088 rows must carry
  `603f9b42ccbafcb8885679e905b2aed5946fb211c29bba0423e27558cc87528b`; the slice digests above are only
  cross-checks.
- `c3-count.py` `ALLOWED_IDS` is `S079–S089` and `ID_RE` catches every `S###`. Staged AMEND carries 11
  unbound tokens (`S127`×5, `S128`×4, `S071`×1, `S095`×1); BASE carries 11 (`S120`×4, `S121`×5, `S122`×2).
  Every one must be re-bound by document before the counter can print `REF_ID_UNBOUND=0`: `S127`→`S088`
  (same URL/digest, proven above), `S128`→`S089`; `S071`/`S095`/`S120`–`S122` as the prose ids the entry
  cites, each resolved to the document it names (RFC 7089 for `S071`, `S082` for the AVeriTeC README).

## Verification gaps

- Q3's sentence-boundary choice is mine (starts at `The Claims in AVeriTeC`); a different start would shift
  the offset by a few chars, so the row must use 1037 (or the sub-anchor offsets) verbatim.
- I did not open S085–S087/S089; no claim here is made about them.
- The page's worked examples are the only data I can inspect; whether the release files match these field
  descriptions is S084's question, not this seat's. No fetch performed (L0 `8d77e6c1` open); no tool
  installed; no file written outside this report; no lane production file, git or jj state touched.

## Commands run (verbatim, trimmed)
```
sha256sum …/b73f7e8dd5b0ace740e48046.txt
603f9b42ccbafcb8885679e905b2aed5946fb211c29bba0423e27558cc87528b
wc -c -m -l → 12775 12775 501
python3: hashlib.sha256("https://fever.ai/dataset/averitec.html")[:24] → b73f7e8dd5b0ace740e48046
python3 str.find: Q1 3929 (count 1) · Q2 2904 (1) · Q3 1037 len 142 (1) · Q4 3185 (1)
python3: capture.count("revision") → 0 ; capture.count('"answer_type"') → 8 ; capture.count('"cached_source_url"') → 7
grep -n "estimate|claim_date" AMEND → 20,21 (quote split across lines)
grep -n "Where possible|four labels" AMEND → 16, 24 (both split / amended)
```
