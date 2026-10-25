# ReviewerC3Spans — round 46 / wave 1

Item: review the C3 span plan — locate each of the eleven planned quotes in its own capture, report
char offset, occurrence count, contiguity; flag non-contiguous or duplicated quotes with a
≤25-word contiguous+unique replacement; check that `citation-version-binding-r36.md` holds RFC
7089's Memento-Datetime claim and `citation-version-binding-r37.md` holds the WARP timestamp-in-URL
claim, so the amendment can cite S079/S081 by document.

State: `chousa-shokunin` at `c2f0e9d` plus this run's tree. The plan moved twice under me:
`build-spans.py` `d41b1e5a…` (span = quote alone) → `b5c4d83b…` (`CONTEXT = 80`, span = quote ±80)
and `spans.tsv` `224f7062…` → `d9bdd226…`; every number below is the current one. No fetch.

## 1. The eleven planned quotes — offsets, counts, contiguity

Re-derivation: read each capture, re-find the quote, re-slice the committed span.

```
id    span_start quote_off  n span_exact ctx  quote
S085  2280       2360       1 True       160  A list of evidence sets
S085  1191       1271       1 True       160  Pre-processed Wikipedia Pages (June 2017 dump)
S086  15189      15269      1 True       160  used the June 2017 Wikipedia dump, processed
S086  41931      42011      1 True       160  recall of 72.36%
S086  20767      20847      1 True       160  We found that 91.2%
S087  91         171        1 True       160  "conceptdoi": "10.5281/zenodo.4925953"
S087  4849       4929       1 True       160  "key": "wiki-pages.zip"
S088  3849       3929       1 True       160  An archive.org link for the source url
S088  2824       2904       1 True       160  Our best estimate for the date the claim first appeared
S089  2942       3022       1 True       160  temporally constrained evidence annotation
S089  7057       7137       1 True       160  published before the claim’s date
```

`build-spans.py --check` → `SPANS_ROWS=11 STALE=0` exit 0; `c3-count` → `CAPTURE_BOUND=11/11`.
Every quote is contiguous, unique (n=1), sits at `span_start+80`, and each committed span is the
exact slice `t[span_start:span_start+len(span)]` (context exactly 160 all eleven). No quote holds a
tab or newline, so the TSV stays 7 columns. **No replacement is due under the assignment's rule.**

Contiguity caveats — contiguous but truncated at a pdf column boundary, so they cannot be extended
on one line (each carries a number without its referent): S086 quote_off 15269 starts a line, with
`We` ending the previous one and the continuation `it with Stanford CoreNLP…` on the next; S086
20847 ends a line, the referent `of the examples were annotated correctly` at char 20928 (line
216); S086 42011 ends a line, `of evidence identified by the super-annotators` at 42093 (line 446).
Extending any needs a second row, which breaks `N_QUOTES=11`; both entries handle it honestly — the
base entry records the interruption under `#### Unknown` and cites the precision figure by offset.

## 2. Non-unique quotes — in the earlier plan revision, already fixed

The 07:24 revision (`d41b1e5a…`, 4178 bytes) planned the bare forms, both of which abort the
builder (`quote not unique`): `10.5281/zenodo.4925953` **n=3** (doi_url, conceptdoi, links block)
and `wiki-pages.zip` **n=2**. Current forms are unique (`"conceptdoi": "10.5281/zenodo.4925953"`
n=1 @171; `"key": "wiki-pages.zip"` n=1 @4929). Closed — a re-plan reverting to the bare DOI or
file name cannot build.

## 3. C3 passes in both modes; registry rows landed

`python3 corpus/evidence/round46/c3-count.py` (default, current tree):

```
ENTRIES=2/2
CITES_BOUND=5/5
QUOTE_ROWS=11/11
QUOTES_IN_SPAN=11/11
QUOTES_IN_ENTRY=11/11
CAPTURE_BOUND=11/11
REF_ID_UNBOUND=0
REF_BOUND=2/2
C3=PASS          (exit 0)
```

`--lane-only` → `REF_ID_UNBOUND=0 REF_BOUND=2/2 C3=PASS`, exit 0. Rows 96–100 carry S085–S089, each
11 cells, URL in cell 2, `mined` in cell 8, entry path in cell 11, inside `## Registry` (line 7;
`## Paths` now 101). Before the rows landed the same tree read `CITES_BOUND=0/5 C3=FAIL` — the only
leg that ever failed; the four span legs were 11/11 in every run. The counter was patched mid-round
(path-traversal and offset guards, +8/−2 vs `c2f0e9d`, now `234e2272…`); the frozen `c2f0e9d` copy
run with `--root` prints the same nine lines and `C3=PASS`, exit 0 — the verdict holds either way.

Row-level notes (row truth is C3's named limit):

- **S088 (row 99) has one wrong anchor offset:** "the claim-date slice at char 2891: `Our best
  estimate for the date the claim first appeared`". At 2891 the capture reads `claim_date : Our best
  estimate …`; the quoted text starts at **2904**. Fix: 2891 → 2904, or quote the 69-char field
  slice. Exactly the defect class the theme is about.
- The other seven checked anchors are exact and unique: `S085 @2349`, `S086 @6737`, `@6784`,
  `@20847`, `S087 @171`, `S088 @3909`, `S089 @7084` — all `exact=True n=1`.
- ScribeRows' draft scoped the rows "distinct in scope from lane row S097 / S113"; both are *staged*
  ids (`SOURCES.append.md:22`, `:38`) and neither occurs in `corpus/SOURCES.md` (`grep -c` → 0). The
  landed rows correctly drop those clauses — do not resurrect them.
- S085's landed recheck is `365d`; staged S120's row said `180d`, and the entries' "Staged material
  corrected on adoption" records only the quote corrections, not the interval change.

## 4. Two cross-reference bindings — both hold; entries cite by document

- **r36 holds the Memento-Datetime claim.** RFC 7089 capture `…/.qcache/d0c4a09a9de32cb91d5e3797.txt`
  (sha256 `c3c7b7f2…bbe801dc`, ASCII so char==byte), char 14896: `The presence of a
  "Memento-Datetime" header and associated value for a given response constitutes a promise that
  the resource state reflected in the response will no longer change (see Section 4.5.6).` S079 row:
  11 cells, `mined`, used-by `citation-version-binding-r36.md`. ✓
- **r37 holds the WARP timestamp-in-URL claim — by E2867 (S081), not by the WARP FAQ (S080).** E2867
  capture `…/.qcache/0034b800811072de3980e85b.txt` (sha256 `d2a58e70…4848f`): `保存日時を含むURLへの変更`
  n=1 @2508 and `warp.ndl.go.jp/web/20250102112233` n=1 @2604. The WARP FAQ
  `…/.qcache/5f54e82c87a76eefdc9a0d35.txt` (sha256 `a7e46e27…c8dc8`) supports only the cadence
  (`National institution websites are archived once per month` n=1 @6425). So S081 for the URL
  mechanism is right, S080 for it wrong; the entries make that split ("the NDL note on WARP's URL
  renewal (`S081`)") and `REF_BOUND=2/2` confirms the sentence test.
- Two defects in r37 itself (not C3 legs): its `source: S080` line has a placeholder ("the cadence
  answer, byte offset of the committed capture" — no offset), and its `recheck: 180d` disagrees
  with S080's row (`90d`).

## 5. Staged prose the captures falsify — corrected in the entries

| staged string | count | contiguous replacement (n=1) |
|---|---|---|
| `We used the June 2017 Wikipedia dump` | 0 | `used the June 2017 Wikipedia dump, processed` @15269 |
| `95.42% precision and 72.36% recall in evidence retrieval` | 0 (pdftotext hyphenates `evi-`/`dence`) | `95.42% precision and 72.36% recall` @6741 |
| `all except two annotators achieved > 90 % precision and all but 9 achieved recall > 70 % in evidence retrieval` | 0 | `except two annotators achieved > 90% precision` @21810 + `and all but 9 achieved recall > 70% in evidence` (line 226) |
| S089 `limited ... to those published before the claim's date` | 0 (`to those` occurs nowhere; ASCII `'`) | `while being restricted to using only online evidence published before the claim’s date.` @7084 (U+2019) |

The landed entries carry the corrected forms (`QUOTES_IN_ENTRY=11/11`) and the base entry records
the first two under `#### Unknown`. One residual reading drift (medium): the amendment says the
restriction is "operational in the pipeline" / "the constraint the pipeline enforces", while the
capture states it of annotators (`annotators convert the verification rationale … while being
restricted to using only online evidence published before the claim’s date.`); no pipeline filter
is shown. Recommend "annotation-time restriction".

## 6. Calibration notes and hazards

- **`offset` now means two things.** In `spans.tsv` it is the *span start* (`quote_off − 80`); in the
  entries' source lines "char N" is the *quote* offset (S086: entry 15269, manifest 15189). Both are
  true, but an `offset`-only header invites the reader to see an unexplained 80-char gap. Suggest
  `span_start` + `quote_offset`, or the entries citing "span row S086-1".
- **char vs byte.** S086 is 60153 bytes / 60030 chars; S089 126093 / 125537. All offsets are
  characters after UTF-8 decode (both scripts `read_text`); a byte-offset rechecker lands 123 and 556
  chars late.
- **staged→lane id collision.** Staged `S082` ≠ lane `S082` (lane S082 = AVeriTeC README).
  Renumbering the staged "round 2's S082" to lane S082 would pass `REF_ID_UNBOUND` (S082 ∈
  `ALLOWED_IDS`) while binding the wrong document. The entries avoided it; the counter cannot see
  this class — a candidate C3 control next round.
- **S088 capture oddity.** The third null `cached_original_claim_url` (char 9920) lacks its trailing
  comma in the captured JSON. The amendment still holds (three nulls at 4444, 6228, 9920, each
  beside a null `original_claim_url`; the single `Unanswerable` answer at 9375 carries
  `"source_url": ""`). "Neither a source URL nor an archive field" is one step stronger than the
  bytes, which carry an empty `source_url`.

## Residual risk

- Nothing fetched (L0 `8d77e6c1` open); every number is from the on-disk captures. Row *truth*
  (scope/teaches prose) is unmeasured by C3 and by me — I checked row shape, offsets, named anchors.
- Both plan files changed during the review; the table is bound to `b5c4d83b…` and `d9bdd226…`. A
  later rebuild invalidates the numbers, not the contiguity findings (properties of the captures).
- I did not judge C1/C2; the counter-patch note concerns C3 only.
