# ExecSpanBuilder — round 47 w1 — span builder for C3

Item: write `build-spans.py` for round 47 in `/tmp/chousa-r47-ExecSpanBuilder/` by
adapting `corpus/evidence/round46/build-spans.py` (input `corpus/evidence/round47/quotes.tsv`,
columns `id url quote entry`; output 7-column `spans.tsv` + `spans/<id>-<n>.txt`; refuse
absent / non-unique quotes, exit 1 naming them; `--check` prints `SPANS_ROWS=n STALE=k`);
test end to end on a /tmp tree with ≥2 located quotes per id; run the frozen
`c3-count.py --root <tmp>`. Nothing written into the lane except this report.

Verdict: DONE. Builder works end to end; on the /tmp tree the frozen C3 counter shows every
span leg full (QUOTE_ROWS=17, SPAN_IDS=6/6, QUOTES_IN_SPAN=17/17, SPAN_CONTEXT=17/17,
CAPTURE_BOUND=17/17). The other legs fail only because the tree has no entries, Registry rows,
tool or lesson.

## Builder

- Source: 173 lines, sha256 `f0eeafe9e2f83f51e2abd789ed0f7daa78aae2b31744c2e4f5362f4fef7bc925`.
  The full text is in this seat's final result (`agent://L1Chousa47.ExecSpanBuilder`). The
  scratch copy is deleted per the seat contract.
- Destination: `corpus/evidence/round47/build-spans.py`. The lane root defaults to
  `parents[3]` (same as `c3-count.py`), and `--root` overrides it. `--cache` defaults to the
  campaign cache.
- Kept from round 46: span = `capture[start:off+len(quote)+80]` with `start=max(0,off-80)`.
  `offset` is the span start, and `capture_sha256` is the sha256 of the capture's bytes.
  Captures are read with `read_text(utf-8, errors=replace)`, the same as c3-count's
  CAPTURE_BOUND.
- New in round 47:
  - The quote list comes from `quotes.tsv` instead of being hardcoded.
  - Every refusal is collected and printed together; nothing is written when any refusal
    occurs. A quote absent from its capture, a quote that occurs more than once, a missing
    capture, or a span that equals its quote (no context) exits 1.
  - Usage and environment errors exit 2: bad header, a row without 4 cells, an id that is not
    `S###`, one id naming two URLs, an absolute or `..` entry path, a missing quotes.tsv, or a
    missing cache.
  - `--check` counts staleness per row: `SPANS_ROW_STALE` (manifest line differs),
    `SPANS_FILE_STALE` (span bytes differ), `SPANS_ROW_EXTRA` (extra committed row),
    `SPANS_FILE_ORPHAN` (`spans/S###-n.txt` not in the manifest), and `SPANS_HEADER_STALE`.
  - Write mode deletes orphan `S###-n.txt` files.
  - Write mode prints `QUOTE <id> char <N>`, where N is the quote's capture offset. This is
    exactly the value c3-count's ANCHOR_BOUND accepts (span offset + `span.find(quote)`), so
    it gives the anchor-cell drafter a value to copy.

## Located quotes (each count=1 in its capture; usable as the lane quotes.tsv seed)

| id | char | quote |
|---|---|---|
| S085 | 1059 | `forming the necessary evidence for their judgment` |
| S085 | 2265 | `Can be one of SUPPORTS\|REFUTES\|NOT ENOUGH INFO` |
| S085 | 2464 | `[Annotation ID, Evidence ID, null, null] tuple if the label is NOT ENOUGH INFO` |
| S090 | 80077 | `A set of sentences S provides supporting evidence for a claim c if, supposing the contents of S` |
| S090 | 80394 | `true, it would give you greater reason to believe that c is false, all else equal.` |
| S090 | 80674 | `evidence, do not select any sentences.` |
| S091 | 810 | `CFEVER comprises 30,012` |
| S091 | 966 | `Each claim in CFEVER is labeled as “Supports”,` |
| S092 | 59726 | `press Skip then select Not enough information` |
| S092 | 59858 | `You must apply common-sense reasoning` |
| S092 | 59925 | `avoid applying your own world-knowledge` |
| S092 | 2800 | `annotators achieving 0.6841 in Fleiss` |
| S093 | 4846 | `We collect 1,535 claims on the Internet` |
| S093 | 5132 | `We call this database of 7,675 annotated claim-evidence pairs the climate-fever dataset` |
| S094 | 21560 | `annotator agreement is 0.792, indicating substantial` |
| S094 | 20650 | `This manner results in total 202` |
| S094 | 20807 | `claims being relabeled.` |

Entry column: S085, S090 and S091 → `corpus/knowledge/claim-support-test-r37.md`; S092, S093
and S094 → `corpus/knowledge/claim-support-test-r37-amendment-2026-10-23.md`.

Capture sha256 values (from the generated manifest):
- S085 `e18eeb26…d1ba92`
- S090 `2f8047a8…224997`
- S091 `0b3518bf…730573`
- S092 `e5b57b48…85ac5`
- S093 `ab3427c3…2b2ba4`
- S094 `d24f2315…78b136`

Pre-check on all six captures: valid UTF-8 with no CR bytes, and each
`sha256(url)[:24]` matches the cache file name.

## Commands and decisive output (tree = /tmp/chousa-r47-ExecSpanBuilder/tree)

- `python3 tree/.../round47/build-spans.py` → 17 `QUOTE` lines,
  `SPANS_ROWS=17 WRITTEN=17`, exit 0.
- `... --check` → `SPANS_ROWS=17 STALE=0`, exit 0. The same result with an explicit `--root`.
- Independent re-slice (my own script: slice equality, digest, uniqueness, ≥80 chars of
  context or the capture edge) → `SLICE_OK=17/17`.
- F1: append one byte to `spans/S091-2.txt`, then `--check` →
  `SPANS_FILE_STALE spans/S091-2.txt`, `STALE=1`, exit 1.
- F2: change the offset 2720→2721 in the manifest →
  `SPANS_ROW_STALE spans/S092-4.txt`, `STALE=1`, exit 1.
- F3: add an orphan `spans/S093-9.txt` and a duplicated last row →
  `SPANS_ROW_EXTRA spans/S094-3.txt`, `SPANS_FILE_ORPHAN spans/S093-9.txt`, `STALE=2`, exit 1.
  A rebuild removes the orphan; `--check` then gives `STALE=0`.
- F4: add `NOT ENOUGH INFO` (S085) and an invented S093 quote →
  `refused S085: quote occurs 3x in 5a631adb18988a1a2421ce75.txt: 'NOT ENOUGH INFO'` and
  `refused S093: quote absent from 44be8711b50a9daae2865b02.txt: 'climate-fever proves every claim'`,
  exit 1, under both build and `--check`. The manifest sha256 is unchanged.
- F5: S085 given a second URL → `line 19: S085 names https://fever.ai/dataset/averitec.html,
  earlier rows name https://fever.ai/dataset/fever.html`, exit 2.
- F6: bad header → exit 2. F7: no quotes.tsv → exit 2. F8: a cache directory that does not
  exist → exit 2.
- `python3 corpus/evidence/round47/c3-count.py --root <tree>`:
  `ENTRIES=0/2 CITES_BOUND=0/6 QUOTE_ROWS=17 (min 12) SPAN_IDS=6/6 QUOTES_IN_SPAN=17/17
  QUOTES_IN_ENTRY=0/17 SPAN_CONTEXT=17/17 CAPTURE_BOUND=17/17 REF_ID_UNBOUND=0
  ANCHOR_BOUND=0/6 INFERENCE_GROUNDED=0/2 QUARANTINE_VERDICTS=0/4
  QUARANTINE_ABSENT_ADOPTED=0 C3=FAIL`, exit 1.
- The same run with `--lane-only` → identical except `CAPTURE_BOUND=skipped`; exit 1.
- `git -C chousa-shokunin status --porcelain -- corpus/evidence/round47` → empty, so the lane
  is untouched.

## Findings for the entry and row drafters

1. **The staged S092 guideline quote needs the capture's exact characters.**
   - The capture holds the guideline twice: at char 15167 (body, "do I have **strong**
     reason to believe the claim is true") and at char 60107 (appendix A.6, "do I have
     **stronger** reason to believe claim is true").
   - The staged wording follows the appendix copy, and the phrase
     `do I have stronger reason to believe claim is true` is unique in the capture.
   - The staged text writes `If I'm` with a straight apostrophe; the capture has `I’m`
     (U+2019). A quote carrying `I'm` will be refused as absent.
2. **A quote cannot cross a line break.** The PDF captures (S090, S091, S094) break
   sentences across lines and interleave columns. The staged S090 Definition 1 sentence
   ("contents of S\nwere true") and the S094 "202 “NOT\n…ENOUGH INFO\" claims" passage are
   therefore not single-line quotes. Use the shorter unique fragments in the table above.
   This is a named limit of the TSV format, not a defect in the builder.
3. **The held S085 anchor's `char 2349` matches no located quote**, consistent with the
   claims.md "Before" note. The candidates are 1059, 2265 and 2464. The S090–S094 anchors
   can take the char values in the table once those rows exist.
4. **QUOTES_IN_ENTRY requires each quote's exact bytes in the citing entry.** The entry
   drafter should quote these strings verbatim, including the curly quotes in S091.

Risks: none observed. The `--root` default resolves `parents[3]`, so the script must sit at
`corpus/evidence/round47/`; it was tested from that placement inside the tree.
No tools were installed or updated, nothing was fetched, and no labrat was spawned. Scratch
`/tmp/chousa-r47-ExecSpanBuilder/` was deleted after this report was written.
