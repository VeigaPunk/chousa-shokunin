# ExecToolB — independent N-version of the frozen quote-reopen tool contract

Seat: `ExecToolB` (executor). Wave 1 build of round 29, lane `chousa-shokunin`.
Deliverable: `.ufo/waves/round-29/build/ExecToolB/quote-reopen-b.py`.
Role: a differential oracle for wave 2, **not** the landed tool. The landed tool
is `tools/quote-reopen.py`, landed by the L1 in commit `30c9d24d`.

## What I did

I wrote a second implementation of the frozen contract in
`corpus/evidence/round29/claims.md` ("Tool contract (frozen)") from that prose
alone, without reading any other seat's code. The implementation is deliberately
structured differently from the counter's reference functions in
`corpus/evidence/round29/c1-count.py`, so that a divergence between the two
surfaces a contract ambiguity rather than a shared bug:

| area | counter reference (`c1-count.py`) | this N-version |
|---|---|---|
| registry | fixed column offset `ln.split("|")[2]` | markdown-table parse, `source` column located from the header row |
| HTML to text | one `HTMLParser` subclass with an `out` list | own `HTMLParser` subclass that records chunks and applies block/skip rules during the parse |
| match | manual `str.find` scan with `isalnum()` boundary tests | one compiled regex with look-around assertions for the boundary |
| fetch | module-level `urllib.request.urlopen` | private opener with a scheme-restricting redirect handler, per-URL result cache, one retry |
| character folding | a `str.maketrans` literal | the same table built from code points, so no invisible literal can be lost when the file is copied |

The deliverable is pure ASCII (verified: `grep -n '[^ -~]'` returns nothing), so
the U+200B and U+FEFF entries cannot be silently dropped by an editor or a
transfer. This matters: my first two drafts lost U+200B on write and the tool
died at import with `ValueError: string keys in translatetable must be of length 1`.
Building the table from code points fixed that permanently.

## Files changed

- `.ufo/waves/round-29/build/ExecToolB/quote-reopen-b.py` (new, 14 291 bytes,
  SHA-256 `37dc4ae35983ff5e91124907886b8600b409b3664dd261071f56f339e1562505`).
- `.ufo/waves/round-29/build/ExecToolB/receipt-v3-run{1,2,3,4,5}.json` (counter
  receipts, written by the counter itself).
- `.ufo/waves/round-29/build/ExecToolB.md` (this report).

No lane file outside my own directory was touched. I ran no `git` or `jj` write
command in the lane.

## Counter runs (the recorded line)

The v3 counter has no `--seed` option; each run draws a fresh 64-bit seed. I ran
the counter from a scratch clone at
`/fast/scratch/hyaku/chousa-r29/w1/ExecToolB/clone`, into which I copied the
current lane `c1-count.py` (SHA-256
`cd50965032278c355f780d357c5672f14840fc218bb1b7dc4adaa6993b5c175d`, identical to
the lane's), the current `claims.md`, the current `corpus/SOURCES.md` and the
frozen fixture.

Command, run from the clone root:

```
python3 corpus/evidence/round29/c1-count.py --receipt <clone>/.ufo/waves/round-29/build/ExecToolB/receipt-v3-runN.json \
  -- python3 .ufo/waves/round-29/build/ExecToolB/quote-reopen-b.py verify
```

Every run printed `QUOTE_REOPEN_MATCH=130/130` and the counter exited 0:

| run | seed | counter line | counter exit | tool exit | wall |
|---|---|---|---|---|---|
| 1 | 18138116962243805326 | `QUOTE_REOPEN_MATCH=130/130` | 0 | 1 | 3.10 s |
| 2 | 11482700126727038829 | `QUOTE_REOPEN_MATCH=130/130` | 0 | 1 | 2.86 s |
| 3 | 2131004332346949462 | `QUOTE_REOPEN_MATCH=130/130` | 0 | 1 | 2.90 s |
| 4 | 12205884551787819808 | `QUOTE_REOPEN_MATCH=130/130` | 0 | 1 | 2.82 s |
| 5 | 8244263761270426205 | `QUOTE_REOPEN_MATCH=130/130` | 0 | 1 | 2.91 s |

All 16 per-class lines were full marks in every run. Run 5 in full:
`runtime-page-window 24/24`, `runtime-page-transpose 24/24`,
`runtime-subspan 14/14`, `runtime-transpose 14/14`, `runtime-crossattr 14/14`,
`verbatim-inline-markup 9/9`, `verbatim-plain 3/3`,
`verbatim-typographic-apostrophe 2/2`, `too-long-true-text 3/3`,
`absent-cross-attributed 4/4`, `absent-fabricated 4/4`,
`absent-one-word-edit 4/4`, `absent-spliced 4/4`,
`absent-truncated-token 4/4`, `no-source-own-work-row 2/2`,
`no-source-unregistered-id 1/1`. I record the tool exit of 1 as correct: the
contract says exit 0 only if *every* item is VERBATIM, and the run contains
ABSENT, NO_SOURCE and TOO_LONG items by construction, so exit 1 is the
contract-correct code for a fully correct run. The counter ignores the tool's
exit code for the predicate.

No miss occurred on any run, so there is nothing to report as a shortfall.

## Evidence beyond the counter

Because the counter scores only the aggregate, I also measured the two
implementation surfaces directly against the counter's own reference functions
(reading the counter, not any seat's code), so wave 2 gets a sharper oracle
than the aggregate score:

- **HTML to text.** 419 hand-written and randomly generated HTML documents
  (nested blocks, skip tags, comments, entities, unclosed tags, self-closing
  tags, random tag soups) fed to both `c1-count.py`'s `_Text` and my
  `TextExtractor`: **0 differences** in the extracted text.
- **Match rule.** 6000 random pairs, both sides fed the same normalized text
  and the same normalized quote: **0 differences**. (An earlier run that fed
  raw strings to both sides showed 71 differences in 4000; that run was
  unfair, because the counter's `found()` normalizes its quote argument while
  my `occurs_in()` expects an already-normalized quote. On the contract's
  actual pipeline — normalize page text and quote alike, then match — the two
  agree exactly.)
- **Registry.** All 49 registered ids plus S999 and S046 to S049: **0 URL
  differences** between my `Registry.url_for` and the counter's `registry_url`.
- **Length rule.** The 3 fixture TOO_LONG items measure 34, 35 and 34
  normalized words; no other fixture item exceeds 25 normalized words, so the
  `TOO_LONG` boundary is unambiguous on this corpus.
- **Fetch bounds.** With 12 items over 5 distinct source ids (2 of them
  NO_SOURCE), the tool issued exactly **3 HTTP requests for 3 distinct URLs**,
  at most 1 per URL, and cached the result. Redirects to a non-http(s) scheme
  are refused (verified: an `ftp://` redirect target raises HTTPError 302), and
  an `http` to `https` redirect is followed normally.
- **Error paths.** Missing items file → exit 2; wrong header → exit 2; unknown
  subcommand → argparse usage error, exit 2.

One observation worth passing to wave 2: `normalize()` is **not idempotent**
for 18 of 3000 random inputs (NFKC is not idempotent for some combining
sequences). Both my implementation and the counter's share this property, so
it does not affect the score, but any tool that normalizes twice would drift
from both. The contract's pipeline normalizes once per side, which is what I
implemented.

## Where the contract was ambiguous, and the choice I made

These are the points where the frozen prose left room and I had to decide. A
wave-2 diff between this oracle and the landed tool should look here first.

1. **Which column is the `source` cell.** The contract says "the row's
   `source` cell" but does not fix an offset. I locate the column from the
   header row of the markdown table rather than hardcoding an offset. On the
   current registry this is the same cell the counter's fixed offset 2 selects,
   and it is robust to a column being inserted.
2. **Which rows count as registry rows.** I accept any table row whose first
   cell matches `S` followed by digits, skipping the header and the separator
   row. The counter matches the literal prefix `| Sxxx |`. On this registry
   both select the same 49 rows. If a future row used a different id shape,
   the two would diverge; the contract does not say.
3. **Whether a row with no URL is NO_SOURCE.** The contract lists as NO_SOURCE
   both "the id is not a registry row" and "the row's `source` cell has no
   `http://` or `https://` URL". I read the second case as still being a
   registry row (so it is NO_SOURCE by the cell rule, not by the id rule) and
   report the two cases with different detail text. The verdict is the same
   either way; only the detail differs.
4. **Stripping trailing characters from the URL.** The contract says to strip
   trailing `.,;)` characters. I strip exactly that set, once, at the end of
   the matched URL. A URL that legitimately ends in a period or closing
   parenthesis is altered by this rule; the contract mandates it, so I did not
   try to be clever.
5. **The URL regex is greedy over non-space.** A source cell holding two URLs
   separated by a space yields the first, per "the first URL in the cell". I
   use `https?://\S+`, the same shape as the counter's.
6. **Fragment removal.** The contract says the fragment is removed before the
   request. I strip it at request time, not when parsing the registry, so the
   `source` cell's URL is reported verbatim in the detail field. The registry
   has one such row (S046).
7. **What the `TOO_LONG` count counts.** "the normalized quote has more than
   25 whitespace-separated words". I count words in the normalized quote
   (after NFKC, quote folding, zero-width deletion and whitespace collapse),
   so `>` 25 is TOO_LONG and exactly 25 is not. The counter's own length rule
   is not in the frozen reference functions, so this is my reading alone.
8. **Whether `TOO_LONG` is decided before or after the fetch.** The contract
   lists the verdicts in a fixed order (NO_SOURCE, TOO_LONG, UNREACHABLE, then
   the match), so I check length before fetching. This also means a too-long
   quote never triggers a network request.
9. **Whether the match is on raw or normalized page text.** The contract says
   normalization is "applied to page text and quote alike", so I normalize the
   extracted page text before matching. The counter's reference does the same
   via `norm("".join(p.out))`.
10. **The alphanumeric boundary, precisely.** "the character before it (if
    any) and the character after it (if any) are not alphanumeric
    (`str.isalnum`)". `str.isalnum()` is true for letters, digits and other
    numeric characters, and false for `_`. Python's regex word class is
    alphanumeric *plus* underscore, so I use `[^\W_]`, which I verified equals
    `str.isalnum()` over the entire Unicode range (0 mismatches across
    0x110000 code points). The underscore is therefore a valid boundary, as
    the contract's wording requires.
11. **An empty quote.** An empty normalized quote matches nothing; both
    implementations return False. I made this explicit rather than letting an
    empty pattern match everywhere.
12. **Which statuses earn the retry.** The contract says "one retry" without
    saying what is retried. I retry on transport failures and timeouts, and on
    5xx (a server-side condition that can be transient). I do not retry a 4xx
    or a non-2xx that is not 5xx, because those cannot change on a second
    attempt.
13. **Content type check.** I use the media type with parameters stripped
    (`text/html`, `application/xhtml+xml`, `text/plain`), so
    `text/html; charset=utf-8` is accepted.
14. **Charset.** When the response declares no charset I decode as UTF-8 with
    `errors="replace"`, matching the counter's reference.
15. **Body cap.** I read at most 8 MiB plus one byte and treat "over 8 MiB" as
    UNREACHABLE. The contract does not say whether the cap applies to the
    compressed or the decompressed body; I apply it after decompression, and
    the decompression itself is bounded by the same cap.
16. **Default registry location.** The contract says the default registry is
    `corpus/SOURCES.md` under the tool's lane root, "the parent of `tools/`".
    My file does not live in `tools/`, so I resolve it as: if the script sits
    in a directory named `tools`, use that directory's parent; otherwise
    search upward from the working directory first and then from the script's
    own directory. The counter runs the candidate with the lane root as the
    working directory, so the search finds the lane's `corpus/SOURCES.md`
    either way. This is the one place where my file's location is
    deliberately different from the landed tool's.
17. **Detail text.** The contract fixes the output shape
    `QUOTE_REOPEN<TAB><id><TAB><VERDICT><TAB><detail>` but not the detail
    content. I emit a short, tab-free string: the URL on a match or a
    no-match, the word count for TOO_LONG, the reason for NO_SOURCE and
    UNREACHABLE. Tabs would corrupt the field split, so I keep them out.
18. **Summary line counts.** I count each verdict across all items, including
    NO_SOURCE and TOO_LONG items, and print them in the contract's order:
    `verbatim`, `absent`, `too_long`, `no_source`, `unreachable`.
19. **Exit code 0.** The contract says exit 0 if every item is VERBATIM. Since
    the counter's item set always contains non-VERBATIM items by construction,
    a perfect run exits 1. The counter's own exit is 0. I kept the contract's
    wording literally.
20. **User-Agent.** The contract requires the User-Agent to contain
    `chousa-quote-reopen`. Mine is
    `chousa-quote-reopen/1.0 (quote-reopen-b differential oracle)`.

## Limits and risks

- The counter's page-sampled items depend on the live pages at run time. All
  five of my runs scored 130/130, but a run against a changed or temporarily
  unavailable page would report a miss that is not a tool defect. A miss must
  be reported as a miss, never re-scaled.
- My tool fetches each URL at most once per run, so it sees one snapshot of
  each page; the counter fetches each page twice and requires a window to be
  present in both fetches. A page that changes between the counter's two
  fetches and my fetch can shift a page-window item.
- I did not test against `text/plain` or `application/xhtml+xml` responses in
  the live path, because no registry row serves those types; the code path
  exists but is exercised only by the unit-level checks above.
- The contract does not pin the summary line's whitespace, so a byte-diff of
  the two implementations' stdout may differ there even though the counter
  parses it identically.
- The scratch clone under `/fast/scratch/hyaku/chousa-r29/w1/ExecToolB/` is
  mine and disposable; the receipts were copied into my lane directory.

## Tooling

No package was installed or updated. Everything used was already present:
Python 3.14.8 standard library only (`html.parser`, `urllib`, `re`,
`unicodedata`, `gzip`, `zlib`), plus `git`, `timeout`, `sha256sum` and `diff`.
No network access outside the registry URLs named in `corpus/SOURCES.md`.
