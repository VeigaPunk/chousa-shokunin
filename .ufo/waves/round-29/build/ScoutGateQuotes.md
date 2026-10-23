# Round 29 wave 1 — held-out quote inventory H for wave 2

Seat: `ChousaR29.ScoutGateQuotes` (leaf scout). Lane: `/home/vgpnk/Projects/shokunin/chousa-shokunin`.
Task: inventory every located quote in the `## Gate` sections of `corpus/lessons/round-24.md`
through `round-28.md` whose source is an http(s) URL registered in `corpus/SOURCES.md`.
No page was fetched; this is a text inventory over committed lane bytes.

## Artifact

`.ufo/waves/round-29/build/ScoutGateQuotes/held-out.tsv`

- 33 items, header `id<TAB>source_id<TAB>quote<TAB>origin`, 4470 bytes,
  sha256 `254c65d9696bfba99f1ad7a6dbc0e2e9260810cfc9f69319a0291f51bca09881`.
- ids `h01`–`h33`, assigned in file order (round 24 → 28, then line order).
- The builder that produced it lives outside the lane, in scratch:
  `/fast/scratch/hyaku/chousa-r29/w1/ScoutGateQuotes/inventory.py`.

Receipt (re-run of the builder against the current lane bytes, `python3` 3.14.8):

```
$ cd /fast/scratch/hyaku/chousa-r29/w1/ScoutGateQuotes && timeout 120 python3 inventory.py
items=33 skipped_no_url=0 bytes=4470
sha256=254c65d9696bfba99f1ad7a6dbc0e2e9260810cfc9f69319a0291f51bca09881
header_ok=True rows_read_back=33
quotes_over_25_words=[]
duplicate_quote_text=['All Cochrane reviews should be assessed periodically to determine whether an update is needed.']
exit=0
```

Input bytes this inventory was read from (sha256):

| file | bytes | sha256 |
|---|---:|---|
| `corpus/lessons/round-24.md` | 12896 | `6738086a98a3a9d8fcd615f220ff4aac9c16a82b449a9669ec982519429abfc6` |
| `corpus/lessons/round-25.md` | 23114 | `de466bbec40fbce2d9360d616e0b6d000c5d18362d854dd624d3cfc534c9f83b` |
| `corpus/lessons/round-26.md` | 20369 | `17b5b097821d1a98e436a0d7f96ba333a5ec11e46a17d63baec898ae27d46964` |
| `corpus/lessons/round-27.md` | 26544 | `13a1dbd1f11dde39a34bc14982c199111e8795f88f7ba2a928378376aec25888` |
| `corpus/lessons/round-28.md` | 8935 | `0cc9a2cb48fff26e2ff54be1a1c79e9398b10d090a4f9b9cdd9a46ff353843f1` |
| `corpus/SOURCES.md` | — | `8bc103823c3a08114e3f787dca96384a6f739931ae3de8c5bdbc64b7225c64b4` |

## Method

1. Pinned the `## Gate` section line ranges from the committed files: `round-24.md` 39–73,
   `round-25.md` 59–108 (including its `### Append-only correction to the round-24 Gate`
   subsection at 92–99), `round-26.md` 34–69, `round-27.md` 50–75 and 235–246 (the second
   heading is `## Gate (post-falsify source row)`), `round-28.md` 44–58.
2. Enumerated **every** line in those ranges containing a quote character (`"`, U+201C, U+201D,
   U+2018, U+2019) to prove coverage. That enumeration returned exactly the lines listed below
   and no others.
3. Took each quote from its own cell: `"…"` for the round-24 table, `“…”` for the round-25,
   round-26 and round-28 tables and for the two prose quotes. Surrounding marks stripped,
   internal characters kept byte-exact, trailing period kept when it is inside the marks.
4. Checked each `source_id` against `corpus/SOURCES.md`: the row must exist and its `source`
   cell must hold an http(s) URL. All 33 items pass; the registry holds 45 rows.
5. Verified each extracted quote is a contiguous substring of its lesson file (item `h32` wraps
   two source lines, so it is checked against the whitespace-normalized span 48–49 of
   `round-26.md`).

Included per file: round-24 17, round-25 11, round-26 4, round-27 0, round-28 1 → **33 items**.

## Skipped — own-work / path sources (9 rows, no http(s) URL)

Each row below is a located quote in a Gate table whose source cell names only a repo path.

| location | row | path source |
|---|---|---|
| `lessons/round-24.md:48` | S001 | `tools/research-gate.sh` |
| `lessons/round-26.md:40` | S034 | `corpus/evidence/round26-measure-before.log:8`; `tools/research-gate.sh` |
| `lessons/round-26.md:41` | S035 | `corpus/evidence/round26-claims.md`; `tools/research-gate.sh` |
| `lessons/round-26.md:42` | S036 | `corpus/evidence/round26-claims.md`; `tools/research-gate.sh` |
| `lessons/round-27.md:57` | S040 | `.ufo/waves/round-26/falsify/FNoTrade.md:126–128` |
| `lessons/round-27.md:58` | S041 | `.ufo/waves/round-26/falsify/FDateHugeCadence.md:42–44` |
| `lessons/round-27.md:59` | S042 | `.ufo/waves/round-26/falsify/FRegistryHeaderless.md:45` |
| `lessons/round-27.md:239` | S043 | `.ufo/waves/round-27/falsify/FC3ValidTable27.md:59` |
| `lessons/round-28.md:51` | S045 | `.ufo/waves/round-27/residual/ResNoHarm.md:66` |

A second, narrower exclusion inside that set: rows S034, S035 and S036 put code fragments in the
quote cell (`C1_AMPLIFIED=4/4`, `while IFS= read -r line`, `freshness=overdue`,
`META_RECHECK_OVERDUE`, `META_SOURCE_ROW_MISSING`) rather than quoted source text. They would be
excluded by the path rule alone; noted because the cell style differs from every other Gate row.

## Excluded — quote marks that are not located quotes (5 places, no row)

| location | what it is |
|---|---|
| `lessons/round-24.md:50`, `:62` | section labels in the location cell (`"Trace claims…" section`, `"Limitations"`) |
| `lessons/round-25.md:82–84` | Garner et al. BMJ `354:i3507` named by URL with no text opened, no quote and no registry row |
| `lessons/round-25.md:98` | "S007's quote still appears verbatim in §2.1" — a claim about the round-24 quote, restating no new text |
| `lessons/round-27.md:68–69` | three scare-quoted propositions the lesson itself rejects; no source URL and no registry row |
| `lessons/round-28.md:53` | two GNU manual requests recorded as timed out before opening; no URL, no quote, no row |

## Quotes over 25 words

None. Longest are 23 words: `h04` (S005), `h09` (S010), `h31` (S039). Every item is inside the
frozen 25-word limit of the tool contract.

## Items wave 2 should read carefully

- `h05` (S006, `round-24.md:53`, flagged `[summary-not-verbatim]`) is the round-24 Gate quote that
  `round-25.md:94–99` records as a summary rather than a verbatim substring at §3.3. Its
  correction is a separate inventory item, `h28` (S006, `round-25.md:97`, flagged
  `[correction-of-r24:53]`). A re-open of `h05` against the live page is expected to return
  ABSENT on the lesson's own record; `h28` is the text that should match. Both are kept because
  both are located quotes in Gate sections from a registered URL.
- `h18` (S019, `round-25.md:68`) and `h32` (S029, `round-26.md:48–49`, flagged
  `[spans-lines-48-49]`) carry the same sentence text, attributed to two registry rows whose
  `source` cells hold the same Cochrane chapter IV URL. They are two Gate records, not two
  independent re-opens.
- `h10` (S011) and `h29` (S037) are flagged `[pdf-source]`: the registered URL ends in `.pdf`, so
  the frozen tool contract's content-type check (`text/html`, `application/xhtml+xml`,
  `text/plain`) makes them `UNREACHABLE` by construction. They are in the inventory because the
  registry row is an http(s) URL; they are not reopenable under the frozen verdict list.
- `h20` (S021) and `h21` (S022) are flagged `[direct-get-challenge]`: the Gate rows record
  "reader via NCBI; direct GET 203 challenge" for those two URLs.
- `h24` (S025) carries the Gate's note "(RFC reader; HTTP resolves to /info/rfc9111/)".
- `h33` (S044) cites the registry URL with the fragment `#os.path.commonpath:`; the registry row
  holds the same URL without the fragment. The tool strips fragments, so this is not a conflict.
- Flag vocabulary used in `origin` after the `path:LINE` token: `[summary-not-verbatim]`,
  `[correction-of-r24:53]`, `[spans-lines-48-49]`, `[pdf-source]`, `[direct-get-challenge]`.
  No quote contains an ellipsis or a square-bracketed insertion, so nothing needed flagging under
  that rule; the parentheses inside `h08`, `h09`, `h24` and `h29` are source text, not editorial
  insertions.

## Verdict

The inventory is complete for the stated selection rule: 33 items, 9 path-source rows skipped,
5 non-quote quote-mark places excluded, 0 items over 25 words, every `source_id` backed by a
registered http(s) URL, every quote byte-exact against the lesson file it came from.

## Limits

- Quotes are copied from committed lesson bytes, not from live pages. No page was opened and no
  fetch was made in this seat, so no item here carries a fresh page-reading date; the opening
  dates recorded in the Gate rows are 2026-10-19 (round 24) and 2026-10-21 (rounds 25 to 28).
- Inclusion follows the lesson's own quote text. Whether that text still appears on the live page
  is exactly what wave 2 measures, and `h05` is the one item the lane already documents as not
  verbatim.
- The selection is bounded by the line ranges in Method step 1. The coverage check in step 2
  covers quote characters; a located quote written without quote marks anywhere in those ranges
  would not be seen, and none was observed.
- This seat read the five lesson files and `corpus/SOURCES.md` only. It did not read the wave-1
  knowledge file, the fixture or the counter.
- Tools installed or updated: none.
