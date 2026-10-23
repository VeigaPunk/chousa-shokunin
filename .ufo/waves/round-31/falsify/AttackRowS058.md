# AttackRowS058 — S058 source row (W3C Subresource Integrity)

Source row: `corpus/SOURCES.md:68`; quote line: `corpus/lessons/round-31.md:54`
(`## Gate`) and `.ufo/waves/round-31/build/ScribeSrcSRI/drafts.md:19` (same text).
Page URL, opened once 2026-10-23: https://www.w3.org/TR/2016/REC-SRI-20160623/

## What I attacked

1. Is the gate quote on the served page verbatim after whitespace folding, and ≤25 words?
2. Is the quote in the section the row and gate line cite (§3.3.5)?
3. Do the row's `scope`, `teaches`, and `anchor` cells say only what the page says?
4. Is tier A justified?
5. What does the lane's own `tools/quote-reopen.py verify` say for an item naming S058?

## Fetch (scratch: /fast/scratch/hyaku/chousa-r31/w2/AttackRowS058)

```
timeout 90 curl --silent --show-error --max-redirs 0 --dump-header sri.headers \
  --output sri.html --write-out 'HTTP_STATUS=%{http_code}\nREDIRECTS=%{num_redirects}\nBYTES=%{size_download}\n' \
  https://www.w3.org/TR/2016/REC-SRI-20160623/
```
Observed: `HTTP_STATUS=200`, `REDIRECTS=0`, `BYTES=89641`, `EXIT=0`.
`sha256sum sri.html` = `947d942a2db9192d4936c9d1fc2f7cad919a107aed126ef5cd2302ec058d2c75`
(the same full hash recorded in `build/ScribeSrcSRI/drafts.md`; lessons abbreviates it `947d942a…2c75`).

## Verbatim check (independent extraction from the served bytes)

Quote under test: “If actualValue is a case-sensitive match for expectedValue, return true.”

- Served-body byte range `[66511, 66634)` (123 bytes, zero-based) is the raw markup:
  `If <var>actualValue</var> is a case-sensitive match for\n                <var>expectedValue</var>, return <code>true</code>.`
  (sri.html lines 1454–1455).
- Tag strip + whitespace fold yields exactly
  `If actualValue is a case-sensitive match for expectedValue, return true.` — equality `True` against the item quote.
- Word count: 10 (`<=25`). `grep -c "case-sensitive match" sri.html` = 1, so the sentence is unique.
  `actualValue` occurs only in §3.3.5 (sri.html lines 1452, 1454), in the document body, not in `head`/`script`.
- Location: inside `<section resource="#does-response-match-metadatalist">`, heading text
  `3.3.5 Does response match metadataList?`, ordered-list step 6.4. That is the section the gate line cites.

## Lane tool verdict

```
timeout 300 python3 tools/quote-reopen.py verify \
  --items .ufo/waves/round-31/falsify/AttackRowS058/items.tsv
```
items.tsv = header `id<TAB>source_id<TAB>quote` plus `id<TAB>S058<TAB>If actualValue is a case-sensitive match for expectedValue, return true.`

Output:
```
QUOTE_REOPEN	id	VERBATIM	matched in normalized page text
QUOTE_REOPEN_SUMMARY verbatim=1 absent=0 too_long=0 no_source=0 unreachable=0
```
`EXIT=0`. Note: this tool has no `--receipt` flag — passing one gives
`error: unrecognized arguments: --receipt …`, exit 2; I ran it without.

## Row-cell review

### anchor

Row: `sections 3.3.1 “Apply algorithm to response” and 3.3.5 “Does response match metadataList”, dated Recommendation 2016-06-23`

- Page headings (extracted): `3.3.1 Apply algorithm to response` and
  `3.3.5 Does response match metadataList?`. Numbers and titles match, except the row's
  3.3.5 title quote drops the page's terminal `?` — minor punctuation, no semantic change.
- Page date: `<time datetime="2016-06-23">23 June 2016</time>`, and the SotD says the document
  “was published by the Web Application Security Working Group as a Recommendation.”
  Row date `2016-06-23` matches. (The `<h2>` element's id string is the stale
  `w3c-recommendation-15-june-2016`; that string is not rendered — a page artifact, not a row error.)

### scope

Row: `Browser Subresource Integrity response-digest validation (tier A: the primary W3C Recommendation for this mechanism); does not establish this lane gate's exact local-file byte contract, claim-schema validation, or read/hash race behavior`

- Abstract: “This specification defines a mechanism by which user agents may verify that a
  fetched resource has been delivered without unexpected manipulation.” §2.1 defines
  `digest`; §3.1 defines integrity metadata as alg + digest (“val”) + options. “Browser … response-digest validation” is supported.
- Exclusions by absence in the served page: `race` 0 occurrences, `schema` 0, `local file` 0,
  `filesystem` 0; the single “file URI” mention is the §3.3.2 note that file-scheme URLs are
  “unlikely to be eligible for integrity checks.” Nothing on the page states a local-file byte
  contract, claim-schema validation, or read/hash race behavior, so the exclusions hold.
- Tier A: the lane's own meaning is `A = primary or authoritative for that scope`
  (`corpus/knowledge/contextual-source-admission-r24.md:56`). A dated W3C Recommendation is
  authoritative for this mechanism; A is justified. The parenthetical “primary” is a tier
  judgement, not a page statement.

### teaches

Row: `Hash the response representation, compare the resulting digest with expected metadata, and return false when no expected value matches`

- “Hash the response representation” — §3.3.1 step 1 applies the algorithm to the
  “representation data without any content-codings applied, except when the user agent intends
  to consume the content with content-encodings applied”. Supported as a summary; the
  content-coding condition is omitted but not contradicted (ScribeSrcSRI's own verdict records
  that condition).
- “compare the resulting digest with expected metadata” — §3.3.5 sets `actualValue` from
  applying the algorithm to the response (which §3.3.1 returns base64-encoded), and §2.1 defines
  `digest` as “the base64-encoded result of executing a cryptographic hash function on an
  arbitrary block of data”; `expectedValue` is the `val` component. Supported.
- “return false when no expected value matches” — §3.3.5 step 7 is `Return false`.
  Edge nuance: the same algorithm returns `true` earlier when `parsedMetadata` is
  `no metadata` (step 2) or the empty set (step 4), and `false` when the response is ineligible
  (step 3). The clause is the loop's failure path, not an unconditional rule; with an empty
  expected set the page returns `true`. Low-severity wording precision, not a false claim.
- Optional minimal correction (reported, not applied — lane production untouched):
  `Hash the response representation, base64-encode the digest, accept a case-sensitive match with the expected value, and return false after the loop; a metadata list that parses to no metadata or an empty set returns true.`

## Verdict

- **Verbatim: YES.** Exact after whitespace folding; 10 words; unique occurrence; in §3.3.5
  (`#does-response-match-metadatalist`), the section the gate line cites.
- **Tool: `VERBATIM`**, `verbatim=1`, exit 0.
- **Row cells: supported.** Scope and teaches follow the page; anchor numbers/titles/date match
  (one missing `?` and the unconditional-false phrasing are precision notes). Tier A justified
  under the lane's own A = primary-or-authoritative-for-scope meaning.
- **No break**; no row text contradicts the served page.

## Limits

- One URL only, per the item. The page's own “Latest published version” link
  (`https://www.w3.org/TR/SRI/`) and the W3C TR index were not opened, so whether this dated
  Recommendation is the newest SRI edition is unmeasured; “primary” rests on the lane's tier
  meaning and on the page self-identifying as a W3C Recommendation [INFERENCE].
- Network: one GET by me to the named URL (curl, 0 redirects) plus the tool's own fetch of the
  same registry URL; no other host contacted.
- No tool installs or updates were performed.
