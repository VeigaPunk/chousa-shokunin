# ReviewFixtureVerbatimB — fixture ground-truth attack, S019/S020/S038/S044 VERBATIM items

Date of work: 2026-10-23 (lane date; host clock reads 2026-10-22). Scope: all items in
`corpus/fixtures/quote-reopen-r29/items.tsv` joined on id with `labels.tsv` whose `source_id`
is S019, S020, S038 or S044 — 18 items; the 7 VERBATIM items are the assigned core.

## Method (only what I ran)

1. Read the frozen contract (`corpus/evidence/round29/claims.md`) and the counter's reference
   constants (`corpus/evidence/round29/c1-count.py`: SKIP, BLOCK, QMAP).
2. Opened each registry row's URL from `corpus/SOURCES.md` with a direct GET (urllib,
   UA `chousa-quote-reopen-counter/r29`, no cookies, 30 s timeout, one retry, URL used once):
   - S019 https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-iv — 200, text/html, 116560 bytes
   - S020 https://www.w3.org/TR/2013/REC-prov-o-20130430/ — 200, text/html, 464179 bytes
   - S038 https://docs.python.org/3/library/datetime.html — 200, text/html, 430114 bytes
   - S044 https://docs.python.org/3/library/os.path.html — 200, text/html, 90223 bytes
   All 2xx, text/html, under 8 MiB: no UNREACHABLE path triggered.
3. Re-implemented the frozen pipeline in scratch only
   (`/fast/scratch/hyaku/chousa-r29/w1/ReviewFixtureVerbatimB/`): html.parser with decoded
   character references, script/style/noscript/template/head dropped, comments dropped, the
   exact v2 block list emitting spaces, then NFKC, curly-to-straight quotes, soft-hyphen and
   zero-width deletion, whitespace collapse; match requires a non-alphanumeric neighbor on
   both sides; verdict order NO_SOURCE → TOO_LONG → UNREACHABLE → VERBATIM/ABSENT.
4. Also opened S019/S038/S044 with the `read` tool (reader view) as an independent second
   extraction path; S020 via `read` returned only W3C-API metadata (text/markdown, no body),
   so S020 rests on the direct GET — the same fetch path the tool uses.

## Verdicts — core VERBATIM items: 7 of 7 LABEL-OK

| id | src | quote located (normalized page text, with offset) | verdict |
|---|---|---|---|
| 6e4f91e5 | S019 | "All Cochrane reviews should be assessed periodically to determine whether an update is needed." — section IV.1, offset 5759 | LABEL-OK |
| 2cbd5af5 | S020 | "The OWL encoding of the PROV Ontology is available here." — offset 1872 | LABEL-OK |
| cee49a8b | S020 | "The namespace for all PROV-O terms is http://www.w3.org/ns/prov#." — offset 1806 | LABEL-OK |
| 076df58d | S038 | "Objects of the date type are always naive." — offset 5077 (the word date sits in a code span; extraction keeps the span contiguous) | LABEL-OK |
| db86a0d4 | S044 | "Return the longest common sub-path of each pathname in the iterable paths." — offset 3060 | LABEL-OK |
| 676c5e8c | S044 | "Unlike a Unix shell, Python does not do any automatic path expansions." — offset 771 (automatic is italic on the page; extraction flattens it, as the fixture class expects) | LABEL-OK |
| 3406c3dc | S044 | "On Unix and Windows, return the argument with an initial component of ~ or ~user replaced by that user's home directory." — offset 5426 (page carries U+2019 in "user's"; frozen normalization maps it to the fixture's straight apostrophe) | LABEL-OK |

Boundary checks exercised, not assumed: for db86a0d4 the match ends at "paths." with " Raise"
after it; for 076df58d the sentence is followed by " An object of type"; for 3406c3dc the
apostrophe span ends before " On Unix".

## Supplementary same-page checks (free riders on the same fetches): 11 of 11 agree

- S019: 5d313002 ABSENT (S008 text not on this page), ddb2ed41 ABSENT (page says periodically, not annually), 1d797926 ABSENT (splice of two fragments), e2e2d1ce TOO_LONG (35 words).
- S020: 13fe59fb ABSENT (JSON Lines text not on this page), f98e78ae ABSENT ("he OWL encoding…" cut at the start; only occurrence is inside "The OWL", preceded by T, so the boundary rule rejects it).
- S038: 886813cd ABSENT (os.path sentence not on the datetime page).
- S044: f0de2354 ABSENT (page says pathname, not filename), 2c526a9f ABSENT (splice drops "in the iterable paths"), ad795e73 ABSENT ("…iterable pat" truncated inside a token; next char is h), 34a402d7 ABSENT (fabricated sentence).

## Located quotes (≤ 25 words each, copied from the opened pages, access date 2026-10-23)

- S019 https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-iv — "All Cochrane reviews should be assessed periodically to determine whether an update is needed."
- S020 https://www.w3.org/TR/2013/REC-prov-o-20130430/ — "The namespace for all PROV-O terms is http://www.w3.org/ns/prov#."
- S038 https://docs.python.org/3/library/datetime.html — "Objects of the date type are always naive."
- S044 https://docs.python.org/3/library/os.path.html — "Unlike a Unix shell, Python does not do any automatic path expansions."

## Verdict

LABEL-OK on every assigned item; no LABEL-WRONG found; the fixture's ground truth for
S019, S020, S038 and S044 holds against the live pages as served on the access date.
No fixture edit proposed (fixture is frozen); nothing in this report changes any contract,
axis, route or judgment.

## Limits

- Labels are true by construction; I tested the committed labels against the pages as served
  now, which is the same exposure the run-time counter has for these rows.
- My checker is a faithful re-implementation of the frozen contract in scratch, not the
  shipped tool; the tool itself was not run (out of my scope).
- Counter-side page-window sampling, run-time variants and the other 4 fixture source rows
  (S002, S003, S008, S013) are outside this item.
- Network use: exactly the 4 registry URLs above, GET only; no installs (tooling directive
  2026-10-19: nothing installed, nothing updated).
