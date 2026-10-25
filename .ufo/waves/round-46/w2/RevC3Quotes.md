# RevC3Quotes — round 46 / wave 2

Item: verify the eleven committed C3 quotes are verbatim in their captures at the recorded offsets,
and that each also appears in the citing entry (the `QUOTES_IN_ENTRY` leg); report any entry copy
that differs in whitespace, punctuation or apostrophe form — S089 curly apostrophe, `%` spacing
explicitly. Bytes under review are `d09fc8e7e2972e30e5e0aaa6e404c97aa0b9f95a`; the lane advanced to
`3807537d` (wave-2 corrections) mid-review, so both are checked. Own derivation, not `build-spans.py`.
No fetch, no install, no lane write (this report only); scratch `/tmp/chousa-r46w2-RevC3Quotes/` deleted.

## Verdict

**The `QUOTES_IN_ENTRY` leg holds, and no quoted copy differs in form.** All eleven quotes are
char-exact substrings of the named capture at `offset + 80`, with 80 chars of text-stream context on
each side; all eleven appear byte-identically in their citing entry at *both* `d09fc8e7` and
`3807537d`; each occurrence is followed by the row's own `(S###)` citation; no quote appears in the
other entry. The two named worries are false alarms on the current bytes:

- **S089 curly apostrophe** — quote, capture slice, `d09fc8e7` entry copy and `3807537d` entry copy
  are all `published before the claimU+2019s date`. The only ASCII-apostrophe copy in the amendment
  is `"before the claim's date"` inside the labelled `#### Unknown` correction note, which describes
  the *staged* text; `published before the claim's date` (ASCII) occurs 0 times.
- **`%` spacing** — `74.7 %` (space) is the capture's form (3×) and the entry's (1×, backticked);
  `74.7%` occurs 0×. `72.36%`/`91.2%` (no space) are capture 3×/1× and entry 6×/2×; space variants 0×.

Artifacts (sha256, `d09fc8e7` bytes): `spans.tsv` `d9bdd226bb5a8be658b49582c4379f8e6996febbb4b35426d3565446f0225964`;
`c3-count.py` `234e2272e8e21e82ed92d7565b4b2e48ca9448a1969687fc002c0de49102f3c5`; base entry `7bffb9d2…`;
amendment `9ab42684…`. `c3-count.py` on the `d09fc8e7` tree: `ENTRIES=2/2 CITES_BOUND=5/5 QUOTE_ROWS=11/11
QUOTES_IN_SPAN=11/11 QUOTES_IN_ENTRY=11/11 CAPTURE_BOUND=11/11 REF_ID_UNBOUND=0 REF_BOUND=2/2 C3=PASS`
exit 0; `--lane-only` identical with `CAPTURE_BOUND=skipped`. Same eight lines on the live `3807537d` tree.

## Per-row derivation (`d09fc8e7` bytes)

`cap==slice` = `capture[offset:offset+len(span)] == span` (chars after UTF-8 decode); `q@+80` = quote at
index 80; `d09`/`3807` = quote an exact substring of that entry. Entry line numbers are identical in both.

| row | off | qlen | pre | post | cap==slice | q@+80 | d09 | 3807 | entry lines | non-ASCII |
|---|---|---|---|---|---|---|---|---|---|---|
| S085-1 | 2280 | 23 | 80 | 80 | yes | yes | yes | yes | 12 | – |
| S085-2 | 1191 | 46 | 80 | 80 | yes | yes | yes | yes | 12, 20 | – |
| S086-1 | 15189 | 44 | 80 | 80 | yes | yes | yes | yes | 13, 30 | – |
| S086-2 | 41931 | 16 | 80 | 80 | yes | yes | yes | yes | 16, 22, 30 | – |
| S086-3 | 20767 | 19 | 80 | 80 | yes | yes | yes | yes | 16, 22 | – |
| S087-1 | 91 | 38 | 80 | 80 | yes | yes | yes | yes | 14, 20, 21 | – |
| S087-2 | 4849 | 23 | 80 | 80 | yes | yes | yes | yes | 14, 20 | – |
| S088-1 | 3849 | 38 | 80 | 80 | yes | yes | yes | yes | 11, 19 | – |
| S088-2 | 2824 | 55 | 80 | 80 | yes | yes | yes | yes | 13, 20, 22 | – |
| S089-1 | 2942 | 42 | 80 | 80 | yes | yes | yes | yes | 15 | – |
| S089-2 | 7057 | 33 | 80 | 80 | yes | yes | yes | yes | 15, 20 | U+2019 |

11 rows, 11 distinct quotes/spans/offsets; all five recorded `capture_sha256` values match the files
named `sha256(url)[:24].txt`; no span ends in a newline (slice equality exact); manifest 7 cols × 11 rows.

## Mutations (fresh extraction of `d09fc8e7` to `/tmp`, `--root`-equivalent tree)

Baseline `--lane-only`: `QUOTES_IN_ENTRY=11/11 C3=PASS` exit 0.

| # | mutation | result |
|---|---|---|
| M-A | curly U+2019 → ASCII in both amendment copies | `QUOTES_IN_ENTRY=10/11 C3=FAIL` exit 1 |
| M-B | `recall of 72.36%` → `recall  of 72.36%` (double space) in base | `QUOTES_IN_ENTRY=10/11 C3=FAIL` exit 1 |
| M-C | delete 1 byte inside S085-1's leading context | `--lane-only` PASS; default `CAPTURE_BOUND=10/11 C3=FAIL` |
| M-D | carrying claim rewritten to the **opposite** meaning, quote untouched (amendment, the S089-2 bullet) | `QUOTES_IN_ENTRY=11/11 … C3=PASS` exit 0 |
| M-F | quote kept, its trailing (`S089`) citation deleted | `QUOTES_IN_ENTRY=11/11 … C3=PASS` exit 0 |
| M-E | all 11 spans trimmed to 20/20 context + offsets rewritten consistently | all eight legs at target, `C3=PASS` exit 0 |

M-A/M-B are the useful positive: the leg *does* reject apostrophe and whitespace drift, so committed
copies are load-bearing. M-C confirms the declared `--lane-only` blind spot; M-E confirms
`w2/RevC3Spans.md` F2 (80/80 unguarded) — **duplicate**. `w1/ScribeEntryAmend.md:61` ran the curly
falsifier; M-A corroborates and adds the whitespace case.

## Findings

**F1 — `QUOTES_IN_ENTRY` passes an uncited quote (medium; calibration).** M-F: keeping
`temporally constrained evidence annotation` in the amendment but deleting its `(\`S089\`)` citation
still scores `QUOTES_IN_ENTRY=11/11 C3=PASS` (`c3-count.py:118`, `in_entry += bool(quote and quote in
texts.get(entry, ""))`). The leg tests token presence in the entry file, not that the quote is
attributed. `CITES_BOUND` only reads the `source:` line and Registry row, so no leg ties a quotation to
its lane id. The committed bytes are correct (every occurrence is followed by its citation), so this is
a guard gap, not a present defect. Distinct from `w2/RevC3Spans.md`'s negative (entry redirected to the
span file), which removes the quote entirely rather than the citation.

**F2 — the leg is indifferent to the claim the quote carries (medium; depth).** M-D: the amendment's
S089-2 bullet can assert the opposite of the capture and C3 still prints PASS. The frozen predicate
(`claims.md:93`) asks only that the quote sit in the entry, so the round cannot distinguish quotation
from correct quotation-plus-reading; the reading is exactly what wave-1 `ReviewerC3Spans.md:117-121`
found wrong at `d09fc8e7` ("operational in the pipeline" vs the capture's annotator restriction). This
is the C3 twin of `CritC1Attack`, which covers C1's tool, not C3's counter — cite it as the C3 leg's
own limit. Not a rule change request: rule changes now would re-scale scored targets.

**F3 — the lane moved under the review (low; record integrity).** `git rev-parse HEAD` answered
`d09fc8e7` at the start of this seat and `3807537d` ("round-46: wave-2 corrections …") at the end;
between them the two entries were edited (2+2 and 3+3 lines: the base `Unknown` revision paragraph,
the amendment's S088 observation and its two S089 bullets). Quote copies are unchanged and all eleven
legs pass on both trees, so nothing scored moved — but a reader of the live tree no longer reads the
`d09fc8e7` sentence wave 1 faulted. Reports in this wave that cite line numbers should say which commit.

**F4 — "80 chars either side" is text-stream, not readable, context for the S086 rows (low; depth;
a narrower consequence of the known interleave class, not reported as such).** The ACL capture is a
two-column PDF extraction (`w1/ReviewOpenS086.md:22`, `w1/ScoutQuarantineOverlap.md:100`), so the S086
spans interleave columns. S086-2's trailing 80 chars are
`'\nracy (N O S CORE E V) approximately 10% for both                 of evidence id'` ("racy" is the
tail of the *left* column's "accuracy"); S086-3's are
`'\nspeakers and were trained either directly by the             of the examples we'`. The quotes
themselves are correct and contiguous within their column, and the entries disclose the interleaving
(`evidence-pool-versioning-r39.md:30`). The span files, however, do not give a reader the surrounding
sentence, which is the stated purpose of the context. No leg measures this; no fix proposed here.

## Residual risk / verification gaps

- Offsets are **character** offsets (as `build-spans.py` slices decoded text). A byte-slice reproducer
  drifts on 5/11 rows by `0,0,32,86,44,0,0,0,0,25,29` bytes (S086-1/2/3, S089-1/2). This corroborates
  `w1/ReviewerC3Spans.md` §6 at per-row precision; `spans.tsv`'s `offset` header still carries no unit.
- `CAPTURE_BOUND` depends on a cache outside the lane (`/home/vgpnk/Projects/shokuknow/…/.qcache`); if
  pruned, default mode drops to `0/11`, and `--lane-only` cannot tell that from forgery.
- I did not judge whether the quoted sentences support the entries' inferences (out of seat:
  `CritC3Inference`), C1/C2, or row truth (scope/teaches). Bytes read: `git archive d09fc8e7` + the live tree.

## Commands (verbatim decisive output)

```
d09fc8e7 tree: c3-count.py → ENTRIES=2/2 CITES_BOUND=5/5 QUOTE_ROWS=11/11 QUOTES_IN_SPAN=11/11
  QUOTES_IN_ENTRY=11/11 CAPTURE_BOUND=11/11 REF_ID_UNBOUND=0 REF_BOUND=2/2 C3=PASS  exit 0
  --lane-only → same, CAPTURE_BOUND=skipped, exit 0   |   build-spans.py --check → STALE=0, exit 0
M-D quote verbatim, carrying claim inverted   → QUOTES_IN_ENTRY=11/11 … C3=PASS  exit 0
M-F quote kept, (`S089`) citation deleted     → QUOTES_IN_ENTRY=11/11 … C3=PASS  exit 0
M-A curly→ASCII → QUOTES_IN_ENTRY=10/11 … C3=FAIL exit 1  |  M-B double space in quote → same
S089-2: quote / capture / entry(d09) / entry(now) all `published before the claimU+2019s date`
'74.7 %' cap=3 entry=1 | '74.7%' 0/0 | '72.36%' cap=3 entry=6 | '72.36 %' 0/0 | '91.2%' cap=1 entry=2 | '91.2 %' 0/0
```
