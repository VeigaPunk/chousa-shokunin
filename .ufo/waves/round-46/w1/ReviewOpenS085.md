# ReviewOpenS085 — open the FEVER dataset page, locate its quotes, judge the staged sentences

Item: open lane source S085 (`https://fever.ai/dataset/fever.html`) from the on-disk campaign
capture, locate the three assigned quotes, record offsets/occurrences/context and a row anchor,
and state which staged sentences this source supports or contradicts. No fetch. Leaf seat.

## Capture

```
$ sha256sum .../5a631adb18988a1a2421ce75.txt
e18eeb26a5a5902e10f0e0b25a9886d99bbbafcf8adfb85b7846bbd569d1ba92  ...5a631adb18988a1a2421ce75.txt
$ wc -c -m (same file)   ->  4146 4146
```
sha256(url)[:24] = `5a631adb18988a1a2421ce75` = the file stem. 4146 chars / 4146 bytes,
`str.isascii()` True, non-ASCII scan empty ⇒ **char offset == byte offset**. Build stamp char
4063: `Build info: refs/heads/live build 385` / `Last updated: 2026-04-02T10:58:13.945736`,
matching both adopted entries' source lines. Tooling: nothing installed or upgraded; Python
stdlib only.

## Quote location (`str.find`, `str.count`; contexts `\n`-escaped only, else literal)

**Q1 `A list of evidence sets` — located, count 1, offset 2360**
- 120 before: `ted label for the claim. Can be one of SUPPORTS|REFUTES|NOT ENOUGH INFO .\n\n claim : The text of the claim.\n\n evidence : `
- 120 after: ` (lists of [Annotation ID, Evidence ID, Wikipedia URL, sentence ID] tuples) or a [Annotation ID, Evidence ID, null, null`

**Q2 `Pre-processed Wikipedia Pages (June 2017 dump)` — located, count 1, offset 1271**
- 120 before: ` Dataset \n\n Shared Task Development Dataset (Labelled) / (Unlabelled) \n\n Shared Task Blind Test Dataset (Unlabelled) \n\n `
- 120 after: ` \n\n License \n\n \n \n To replicate the results in the NAACL paper use the following files.\n When concatenated, they form th`

**Q3 the sentence naming the evidence tuple fields — located, count 1**
Char 2349, 193 chars to `NOT ENOUGH INFO`; the whole line is `capture[2348:2544]` including the
release's spaced full stop at 2543:
`evidence : A list of evidence sets (lists of [Annotation ID, Evidence ID, Wikipedia URL, sentence ID] tuples) or a [Annotation ID, Evidence ID, null, null] tuple if the label is NOT ENOUGH INFO .`
- 120 before (2229–2348): ` The annotated label for the claim. Can be one of SUPPORTS|REFUTES|NOT ENOUGH INFO .\n\n claim : The text of the claim.\n\n `
- 120 after (2542–2662): ` .\n\n (the Annotation ID and Evidence ID fields are for internal use only and are not used for scoring . They may help de`

## Anchors (≤25 words, exact capture slices)

| quote | anchor | char | words | slice sha256[:16] |
|---|---|---|---|---|
| Q1/Q3 | `A list of evidence sets (lists of [Annotation ID, Evidence ID, Wikipedia URL, sentence ID] tuples)` | 2360 | 16 | 02586710639b459f |
| Q2 | `Pre-processed Wikipedia Pages (June 2017 dump)` | 1271 | 6 | d147b9198b97b1f4 |

Q3 in full is 34 whitespace tokens, so the anchor must be the 16-token field-list slice; the
null-pair alternative is `a [Annotation ID, Evidence ID, null, null] tuple if the label is NOT
ENOUGH INFO` (15 words, char 2447).

## Span binding, re-derived

`python3 corpus/evidence/round46/build-spans.py --check` → `SPANS_ROWS=11 STALE=0`, exit 0.
`spans.tsv` S085 rows: offsets 2360 and 1271, `capture_sha256` = the digest above; span files
23 B / 46 B are exactly `capture[2360:2383]` and `capture[1271:1317]`.

## Staged sentences S085 supports

1. The evidence-field quote (char 2360) — with the caveat that the staged text lowercases the source's `A`.
2. `for internal use only and are not used for scoring` — count 1, char 2593.
3. `Pre-processed Wikipedia Pages (June 2017 dump)` shipped as a Download Links entry — char 1271.
4. "The word 'revision' does not occur in the release's data-format section" — `count('revision') == 0` over the whole file; likewise "no field naming a per-page revision": the format names exactly 4 fields at char 2168 (`id`, `label`, `claim`, `evidence`).
5. The amendment's "FEVER's three" — `The claims are classified as Supported , Refuted or NotEnoughInfo .` char 917.
6. The amendment's "a URL plus a sentence id … no revision anywhere in the format" — tuple positions Annotation ID, Evidence ID, Wikipedia URL, sentence ID (`sentence ID` at 2438), none a revision.
7. Unused but supporting: `185,445 claims` (745); test split drops label and evidence (3869); the FEVEROUS/AVERITEC/AVERITEC 2.0/AVERIMATEC release list (200–264) matches the staged Unknown.

Not carried here, correctly attributed elsewhere: the June-2017-dump sentence and every
95.42/72.36/0.6841/31.75/16.82/12.15 figure are S086; `wiki-pages.zip`, `conceptdoi`, the
Zenodo deposit are S087. **"frozen" appears 0 times** in this capture (staged base uses it 4×);
the page dates the dump, it never calls it frozen.

## Contradiction check

One staged sentence is falsified as written; both sides:
- Staged base: `**The verdict's binding is a URL and a sentence id — and nothing else.**`
- Capture 2360: `A list of evidence sets (lists of [Annotation ID, Evidence ID, Wikipedia URL, sentence ID] tuples)` — four positional fields, so "nothing else" is false at format level (two ids are present and merely unscored, as the staged text says two sentences later).

The adopted entry already dropped the phrase, but its `Staged material corrected on adoption`
bullet records only the S086 contiguity corrections, so this correction is silent. No other
staged sentence is contradicted by S085.

## Findings

**H1 — no Registry rows for S085–S089, so C3's cite leg is 0/5.** `python3 corpus/evidence/round46/c3-count.py` → `ENTRIES=2/2 CITES_BOUND=0/5 QUOTE_ROWS=11/11 QUOTES_IN_SPAN=11/11 QUOTES_IN_ENTRY=11/11 CAPTURE_BOUND=11/11 REF_ID_UNBOUND=2 REF_BOUND=2/2 C3=FAIL` exit 1. `row_for` returns 0 rows for each of S085…S089; the source lines themselves do match the counter regex (`cat -A` shows U+2014 `M-bM-^@M-^T` with spaces). Every quote/span/capture leg is already green. Owner: ScribeRows.

**H2 — `REF_ID_UNBOUND=2` comes from the amendment's own correction bullet.**
`corpus/knowledge/evidence-pool-versioning-r39-amendment-2026-10-23.md`, `Staged material
corrected on adoption`, quotes the staged ids `S071` and `S095` as tokens; both are outside
S079–S089, which R46-C3 forbids. And `S082` in that same bullet means staged PRISMA-S while
lane S082 is the AVeriTeC README — the counter scores it *bound* while it names another
document (calibration blind spot, not a pass). Fix by document: write "round 1's RFC 7089
row", "round 2's NDL E2867 note", "the staged pin-amendment pointer", leaving
S079/S081/S088/S089 as the only tokens there.

**M1 — adopted Observation claims provenance S085 does not state.**
`corpus/knowledge/evidence-pool-versioning-r39.md:16` says "the page the evidence is drawn
from is shipped as … (`S085`)". The capture supports (a) claims were "generated by altering
sentences extracted from Wikipedia" (745) and (b) the dump is a Download Links entry (1271); it
never says the evidence ids index into that shipped dump. That step is inference and belongs
where the entry already puts it ("The release fixes the pages by shipping …").

**M2 — a supported load-bearing fact was dropped.** The staged form kept the unscored ids
(char 2593); the adopted entry has `count('internal use') == 0`, keeping only "the tuples
carrying the Wikipedia URL and the sentence id". For a row scoped to what the format does and
does not carry, the four-position tuple with two unscored ids is what makes "no revision
anywhere in the format" checkable. Reinstate it, or record the deletion.

**M3 — the staged row scope names a row this lane does not hold.** Staged S120 scope says
"**distinct from wave 2's FEVER dataset row**"; the lane registry has no FEVER row at all
(`grep -c -i fever corpus/SOURCES.md` → `0`), and staged S097 is the *same URL*. Bind by
document or drop the clause — the round-45 reject class (staged S071 → lane S079).

**M4 — the "and nothing else" correction is unrecorded** (Contradiction check). R46-C3's kill
rule requires a contradicted staged sentence to be corrected *and* recorded; add it to the same
bullet as M2.

**L1 — pipe hazard.** The capture's label line contains
`Can be one of SUPPORTS|REFUTES|NOT ENOUGH INFO` (2296) — never paste it into a Registry cell
(no pipe in a cell). Both committed quotes and both anchors above are pipe-free.

**L2 — quote case.** Staged wrote `"a list of evidence sets"` where byte 2360 is `A`; the
adopted entry writes `"A list of evidence sets"` and `QUOTES_IN_ENTRY=11/11` confirms it. Noted
only so a copy-back does not reintroduce it.

## Draft row (11 cells, pipe-free)

```
| S085 | FEVER Dataset — the dataset authors' own release page — https://fever.ai/dataset/fever.html | dataset | A | what the FEVER release format binds a support verdict to and what it does not carry: the evidence-tuple shape, the unscored id positions, and the dated pool download | the Data Format evidence field at char 2360, "A list of evidence sets (lists of [Annotation ID, Evidence ID, Wikipedia URL, sentence ID] tuples)", and the Download Links entry at char 1271, "Pre-processed Wikipedia Pages (June 2017 dump)"; capture sha256 e18eeb26a5a5902e10f0e0b25a9886d99bbbafcf8adfb85b7846bbd569d1ba92, build 385, last updated 2026-04-02 | each evidence tuple is [Annotation ID, Evidence ID, Wikipedia URL, sentence ID] or a null-pair for NOT ENOUGH INFO, the two ids are internal and unscored, the release ships a June 2017 Wikipedia dump, and the four-field record names no revision | mined | 2026-10-25 | 365d | corpus/knowledge/evidence-pool-versioning-r39.md |
```

## Verdicts

Q1 located (2360, 1×); Q2 located (1271, 1×); Q3 located (2349..2543, 1×). Six staged
sentences supported, one falsified as written (`and nothing else`), its correction (and the
M2 deletion) unrecorded; nothing else contradicted by S085.

## Residual risk / gaps

- S085 is the page, not the paper: nothing here bears on the dump-provenance step (M1) or the
  Zenodo deposit; those are S086/S087 and outside this seat.
- The `revision` absence is a whole-capture count (0), so the entry's narrower "in the
  data-format section" is weaker than what was measured, never stronger.
- Whether S085's Download Links resolve to the same `wiki-pages.zip` the Zenodo record files is
  not decidable from a text capture with no rendered link targets — S087's job.
- H1/H2 are other seats' edits; only the reads and counter runs quoted above were verified. No
  scratch directory was created for this seat.
