# ScoutQuarantineOverlap — round 46 wave 1

item: quarantine check for the five adopted URLs (S085–S089); is any adopted row
quarantined, and is the 24-row slice still 24 rows today.
seat: leaf scout, read-only over both repos. No fetch. No production writes.

## Method (4 independent legs)

1. lane tool: `python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/quarantine-check.py slice`
2. operator recipe (verbatim from `.ufo/waves/round-42/gen-w1-spec.py:43`), then the
   *naive* variant without the round/id guards, to test the recipe itself.
3. the ticket's token greps, case-insensitive, over the whole register.
4. **URL-key equality** — stronger than token grep: extract every `https?://…` from
   every register pipe row, `sha256(url)[:24]`, and intersect with the five capture keys.

## Slice count today = 24

```
$ awk -F'|' -v l='chousa' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' \
    /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md | nl
 1 S077   `payload-absent`     11 S104   `payload-absent`
 2 S080   `payload-absent`     12 S105   `payload-absent`
 3 S082   `payload-absent`     13 S108   `payload-absent`
 4 S084   `payload-absent`     14 S110   `payload-absent`
 5 S086   `payload-absent`     15 S111   `payload-absent`
 6 S088   `payload-absent`     16 S112   `payload-absent`
 7 S093   `payload-absent`     17 S114   `payload-absent`
 8 S094   `payload-absent`     18 S116   `payload-absent`
 9 S095   `payload-absent`     19 S120   `payload-absent`
10 S096   `payload-absent`     20 S125   `payload-absent`
21 S100`  the gate block named no locator, so no quote was checked
22 S101`  idem   23 S102`  idem   24 S103`  idem
COUNT=24
```

`quarantine-check.py slice` prints the same 24 rows (20 class rows + 4 never-checked
gate rows), exit 0. Register digest, today:
`sha256 5afe1810a6c3d62f37987b575a954f5b1197daa23005d4bb2f1d982f64bad833`, 375 lines,
header still `194` rows / `324` quotes.

Recipe caution: the naive `awk 'NR>1 && /^\|\s*`chousa`/'` returns **25** because the
`## By lane` summary row at line 238 (`| `chousa` | 20 |`) matches the lane cell. The
two guards in the operator recipe are what make the count right; pasting the naive one
would over-count by one.

## Token greps (whole register, `-i`)

| token | hits | line / row / lane |
|---|---|---|
| `fever.ai` | 0 | — |
| `aclanthology` | 3 | 43 `S093` chousa/r2 · 50 `S110` chousa/r3 · **54 `S116` chousa/r4** |
| `zenodo` | 0 | — |
| `2505.17978` | 0 | — |
| `2305.13117` | 0 | — |
| `AVeriTeC` | 0 | — |
| `AVeriMaTeC` | 0 | — |
| `FEVER` (extra) | 1 | 44 `S094` chousa/r2 — matched inside `CFEVER`, not the FEVER paper |

Line 54 is the hit that matters:
`| `chousa` | round4 | S116 | `payload-absent` | https://aclanthology.org/N18-1074.pdf | …`
`N18-1074.pdf` **is** the FEVER ACL paper, staged as lane `S086`.

## URL-key sweep over all 375 lines (targets = the five capture keys)

```
5a631adb18988a1a2421ce75  S085 fever.ai/dataset/fever.html        -> none
1c15b611118dee97e4105fcf  S086 aclanthology.org/N18-1074.pdf      -> [(54, 'https://aclanthology.org/N18-1074.pdf')]
7800e2e1e2df3bc124b6b83e  S087 zenodo record 4925954             -> none
b73f7e8dd5b0ace740e48046  S088 fever.ai/dataset/averitec.html     -> none
78761b633aee2289e5874ce9  S089 arxiv.org/html/2505.17978v2        -> none
```

All five captures exist under
`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/`
(4146 / 60153 / 5676 / 12775 / 126093 bytes, filename = key). `capture_kind` on the
S086 capture = `page` (UTF-8 text, real PDF extraction, `FEVER: a large-scale dataset…`).

## Adjudication of register row S116 (the only overlap)

`quarantine-check.py examine` on the slice: `S116 1 absent … S116 2 absent … S116 3
absent`, all against capture `1c15b611118dee97e4105fcf.txt`. That is the frozen rule
working as declared. It is **not** a fabrication finding: all three register quotes are
verbatim in the capture, split by the PDF's two-column extraction.

Word-by-word probe (`D = re.sub(r"\s+"," ",capture)`; find each quote word in order,
print the interposed text between consecutive matches):

* q1 `resulting in inter-annotator agreement of 0.6841 in Fleiss κ (Fleiss, 1971) in
  claim verification classification, and 95.42% precision` — **all 18 words present, in
  order**. Gaps: ` Los Angeles County, officially `, ` the County of Los Angeles, `,
  ` is the most populous county in the USA. ` — i.e. the right-hand column of a figure
  caption, interleaved.
* q2 `We used the June 2017 Wikipedia dump` — **all 7 words present, in order**
  (`used the June 2017 Wikipedia dump` at char **15269**). Gaps are left-column
  fragments of the adjacent paragraph interleaved between `We` and `used`.
* q3 `…appropriate evidence. Claims require composition of evidence` — present except
  for the hyphen split `appropriate ev-` (char 5629) / `idence. Claims require`
  (char 5710); `Claims require composition of evidence` exact at char 5718.

So the class is: two-column PDF interleave + end-of-line hyphenation. The campaign
checker's wrappers catch neither, and `payload-absent` here means "not contiguous in
extraction", not "not in the source".

## Cross-artifact id collision (recorded, not resolved by me)

Register ids are the *campaign's* numbering and reuse the low S-range:
register `S086` = ncpssd.cn (line 41), register `S088` = jmu.edu.cn PDF (line 42) —
different documents from lane `S086` (FEVER ACL paper) and lane `S088` (AVeriTeC
dataset page). Register `S085`, `S087`, `S089` are unoccupied. This is exactly why the
frozen C3 predicate requires re-binding by document; the Registry rows must carry the
lane URL, never the register's.

## Effect on the adopted spans

Lane entry `corpus/knowledge/evidence-pool-versioning-r39.md` already binds S086 to
three single-line slices: char 15269 `used the June 2017 Wikipedia dump, processed`,
char 42011 `recall of 72.36%`, char 20847 `We found that 91.2%`. I re-checked all three
against the capture: each is an exact contiguous slice. None of the register's three
stitched quotes is reused. Residual risk for the span builder: any span that crosses a
hyphenated line break (`ev-/idence`) or a column interleave will fail exact-slice
binding even though the words are there.

## Verdict

* **Is any adopted row quarantined? YES — one of five, and only at URL level.**
  Lane `S086` (FEVER ACL paper, `aclanthology.org/N18-1074.pdf`) is register row
  `chousa round4 S116`, class `payload-absent`, 3 quotes. `S085`, `S087`, `S088`, `S089`
  have zero token hits and zero URL-key collisions.
* **Does that bar adoption? No, on this evidence.** The class is a two-column
  extraction artifact, proved word-by-word above; the document is present, complete and
  `page`-kind, and the entry's actual spans are exact slices. The honest record is that
  S116 is a **false positive of the register**, to be written down as such (with these
  offsets) rather than silently passed — mechanically, `located==0 → absent → refuse`
  would still fire, so a reviewer applying the frozen rule to S116 will refuse it unless
  this adjudication travels with the row.
* **24 rows today? Yes — 24** (20 + 4), register digest `5afe1810…`, unchanged.

confidence: high on counts, keys and the three word-by-word probes (all commands run
here, outputs pasted). Medium on the inference that S116 is a checker false positive
*by design class* rather than a one-off: I verified this row only, not the other 193.
unknowns: whether the campaign owner wants S116 re-classed upstream (outside this lane);
whether any *other* register row is the same two-column/hyphen artifact class — a cheap
follow-up is to re-run the fold chain with a hyphen-join + column-split fold over all
194 rows.

tooling: none installed or upgraded this item.
