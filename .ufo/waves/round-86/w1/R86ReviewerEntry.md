# R86ReviewerEntry — K3 attack on the two repaired decision-table rows, and C2's `UNENTAILED_TERM` as an instrument

Seat `R86ReviewerEntry`. Lane chousa, round 86, wave 1. Leaf seat: no subagents, no `agent://all`,
no lane or fleet git/jj mutation, no production edits, no network.

- Revision under attack: `667a5d091dc46168ed95eda0ae7f19a9bcf139a2` (landing). Base: `3bfb6885958ad4a674ad1896f70d1e836be609e4`.
  Egress table `e4468752…`, claim freeze `d0b1bd06872cdf0eeb03eccd099ff69ae6704307`.
- Frozen predicate read first: `corpus/evidence/round86/claims.md`; pre-freeze repairs read in `plans/round-86.md`.
- Scratch: `/fast/scratch/hyaku/chousa-r86/R86ReviewerEntry/` (`tree` = `git archive 667a5d09 | tar -x`, `base` =
  same at `3bfb6885`, plus one full copytree per attack). Removed before yield.
- Receipts (written beside this file, all produced from committed bytes):

| receipt | what it shows |
|---|---|
| `R86ReviewerEntry/r86rev-c2-runs.txt` | counter on landing and base trees |
| `R86ReviewerEntry/r86rev-instrument-attacks.txt` | seven mutated trees, one counter run each |
| `R86ReviewerEntry/r86rev-quotes-verbatim.txt` | independent re-derivation of all 20 located quotes |
| `R86ReviewerEntry/r86rev-warrant-cells.txt` | the two repaired rows, their quotes, the capture lines |
| `R86ReviewerEntry/r86rev-term-scope.txt` | frozen term set, scanned scope, term counts |
| `R86ReviewerEntry/r86rev-capture-identity.txt` | whether the S023 capture changed this round |
| `R86ReviewerEntry/r86rev-s024-revert.txt` | S024 row vs its pre-round-85 state |
| `R86ReviewerEntry/r86rev-registry-parse.txt` | registry parse coverage (217/217 rows) |
| `R86ReviewerEntry/r86rev-pins.txt` | `instrument-pins.txt` vs landed bytes |

No tool installed or upgraded; no pacman call; no network request.

---

## 0. The predicate at landing (K1)

```sh
S=/fast/scratch/hyaku/chousa-r86/R86ReviewerEntry
git -C /home/vgpnk/Projects/shokunin/chousa-shokunin archive 667a5d091dc46168ed95eda0ae7f19a9bcf139a2 | tar -x -C "$S/tree"
python3 -B "$S/tree/corpus/evidence/round86/curation-r86.py" --root "$S/tree"
```

Observed (`r86rev-c2-runs.txt`), exit **0**:

```
SUPERSEDED_LIVE=0 UNENTAILED_TERM=0 MODIFIED_DEF_CITED=1 QUOTES_LOCATED=20/20
CURATION_R86=PASS
```

The same counter on the base tree (`--root $S/base`, exit **1**) reproduces the committed control byte-for-byte,
including both routed rows and their term:

```
SUPERSEDED_LIVE=1 UNENTAILED_TERM=2 MODIFIED_DEF_CITED=0 QUOTES_LOCATED=19/19
SUPERSEDED_STILL_LIVE S024 is mined while S031 supersedes it and is queued
UNENTAILED corpus/knowledge/search-transparency-reporting-r84.md row=Recording when a resource changed term=modification
UNENTAILED corpus/knowledge/provenance-recording-r85.md row=Recording when content was last reviewed term=modification
CURATION_R86=FAIL
```

`sha256sum -c` over all seven `instrument-pins.txt` lines passes at landing, and `tools/gate-records.py` is
`fe204539b9b549ef1c6092a3963d73c7772946b027ab07da19c89961817aa287` as `claims.md` states (`r86rev-pins.txt`).
K1 is met; the instrument bytes are the frozen bytes.

---

## 1. K3 on the two repaired rows — both HELD

The repair, exactly as landed (`git diff 3bfb6885 667a5d09`): r84 row "Recording when a resource changed" gains
warrant `Q13 (S023)` and a rewritten Never; r85 row "Recording when content was last reviewed" moves `Q7` from `S024`
to `S031` and rewrites its Never. The **Do cells are unchanged from base in both rows**, so the repaired cells under
K3 are the two Nevers (and the warrant cells).

### 1a. r84 line 48 — "Recording when a resource changed" — warrant Q13 (S023)

Row (`r86rev-warrant-cells.txt`, `grep -n` on the entry):

```
48:| Recording when a resource changed | state the date on which the resource was changed | record that the resource changed without the date on which it changed | Q13 (S023) |
34:| Q13 | S023 | "Date on which the resource was changed." |
```

Quote located by this seat in the committed capture, not taken from the counter:

```sh
grep -n "Date on which the resource was changed" corpus/captures/f5545a194c06ab421875b047.txt
# 8786: Date on which the resource was changed.
```

and in context (`sed -n '8724,8800p' …`, offsets 52/53/62/63/72/73) the capture reads
`Label / Date Modified`, `Definition / Date on which the resource was changed.`,
`Comment / Recommended practice is to describe the date, date/time, or period of time as recommended for the property
Date, of which this is a subproperty.` The quote is the `dcterms:modified` Definition; the Comment is quoted separately
as the entry's Q10.

- **Do** — "state the date on which the resource was changed": the quote's content verbatim, in the imperative the entry
  uses for every definitional warrant (rows 8, 10, 11 of the same table do the same with Q9/Q11/Q12). Nothing in the row
  is absent from the quote's content.
- **Never** — "record that the resource changed without the date on which it changed": the exact negation of the Do. The
  base Never, `record a modification without its date`, imported the noun `modification`, which the S023 capture contains
  **0** times (`r86rev-term-scope.txt`); the repaired Never retains no noun the quote lacks.
- **Same-source contradiction (K3b)** — none. The adjacent Comment recommends the value's *form* per `Date`; it does not
  contradict dating a change. The label `Date Modified` is consistent.

**Verdict: held.** Residual (not a firing, stated so the verdict is not read as a clean bill): the quote is a definition
and the row issues a recording duty from it. That mood is the entry's disclosed convention — the entry's Limits say
"DCMI's terms … define what `source`, `modified`, `valid`, and `available` mean, not when or how often to set them. The
rows keep only the definitions." Firing on mood would fire rows 8/10/11 and every definition-derived row in both entries,
which is a defect of the entry form, not of this repair.

### 1b. r85 line 39 — "Recording when content was last reviewed" — warrant Q7 (S031)

Row:

```
39:| Recording when content was last reviewed | state the date the content was last reviewed for accuracy and completeness | record a review date for content that was not reviewed for accuracy or completeness | Q7 (S031) |
28:| Q7 | S031 | "Date on which the content on this web page was last reviewed for accuracy and/or completeness." |
 3:source: S215, S026, S031
```

Quote located by this seat:

```sh
grep -n "last reviewed for accuracy" corpus/captures/11d6cc56bb24adfc61eea2b4.txt
# 211: Date on which the content on this web page was last reviewed for accuracy and/or completeness.
```

with the page's full definition block read (`sed -n '195,250p'`, non-blank lines): `Canonical URL:
https://schema.org/lastReviewed`, the definition above, `Values expected to be one of these types / Date`,
`Used on these types / WebPage`. The page carries no other normative prose.

- **Never** — "record a review date for content that was not reviewed for accuracy or completeness": the definition's own
  negation (a `lastReviewed` date names a review that occurred; content reviewed for neither accuracy nor completeness has
  no such date), scoped correctly under the source's "and/or" — a review for accuracy alone is *not* excluded, because
  "not … for accuracy or completeness" means neither. No noun absent from the quote. The base Never,
  `pass a record off as reviewed when only its modification date is known`, imported `modification`, which the S031
  capture contains **0** times (`r86rev-term-scope.txt`: `modified` 0, `modification` 0).
- **Same-source contradiction (K3b)** — none.
- **S031 registry row** (`corpus/SOURCES.md:41`): its anchor's quoted sentence is verbatim at capture line 211; its
  `teaches` says "no comparison to other date properties claimed", which the capture's 0 occurrences of
  `modified`/`modification` supports; its capture key is `sha256(url)[:24]` = `11d6cc56bb24adfc61eea2b4`, and the file's
  content sha is `97fe1a6adbd2ded4…` as the Gate record says.

**Verdict: held.** Residuals: (i) the unchanged **Do** tightens the source's "accuracy and/or completeness" to
"accuracy and completeness", excluding an accuracy-only review the quote permits — an under-claim, pre-existing and
byte-identical to the row the round-85 non-author check already held "faithful … drops `and/or` hedge, immaterial"
(`.ufo/waves/round-85/w1/R85ReviewerEntry.md`, row 6), so it is not a repaired-cell K3 firing but it should be aligned;
(ii) the Never generalises the subject from "the content on this web page" to "content" — safe direction for a
prohibition, still an extension.

---

## 2. `UNENTAILED_TERM` attacked as an instrument

The check, from the pinned bytes (`r86rev-term-scope.txt`):

```python
ENTRIES = ["corpus/knowledge/search-transparency-reporting-r84.md",
           "corpus/knowledge/provenance-recording-r85.md"]
DEFECT_TERMS = ("modification", "modified")
...
joined = " ".join(q for _, _, q in entry_located).lower()      # per-entry, not per-row
for term in DEFECT_TERMS:
    if term in (cells[1] + " " + cells[2]).lower() and term not in joined:
        unentailed.append((rel, cells[0], term))
```

It is a two-word, per-entry substring blacklist over the Do and Never cells of two files. Every attack below runs the
frozen counter (sha `84a64ad4…`) on a full copy of the landing tree; outputs are in `r86rev-instrument-attacks.txt`.

### 2.1 It is satisfied by deleting the word without repairing the claim — YES (E3)

Landing row 9 replaced by a statement the warrant does not support at all, carrying no blacklisted substring:

```
| Recording when a resource changed | state the license under which the resource is distributed | record a distributed resource without naming its license | Q13 (S023) |
```

`SUPERSEDED_LIVE=0 UNENTAILED_TERM=0 MODIFIED_DEF_CITED=1 QUOTES_LOCATED=20/20` / `CURATION_R86=PASS`, **exit 0**.

So the check's pass condition is "the offending word is absent", never "the claim is entailed". The landing happens to
have repaired the claim *and* removed the word, but the instrument cannot tell that from E3.

### 2.2 The frozen term set misses the class the round-85 spot-check named — YES, and the counter passes the defect bytes (E4)

The round-85 non-author check fired K3 on r85 rows 1 and 5 for the imported nouns `primary`, `tool`, `version`, `step`
(`.ufo/waves/round-85/w1/R85ReviewerEntry.md`, "Row 1 … the word `primary`", "Row 5 Never, words `tool`, `version`,
`step` … absent from S026's captured page"). Restoring exactly those two Nevers on the landing tree:

```
| Naming what a resource derives from | … | deliver a resource that passes for a primary when it derives from an identified earlier entity | Q1, Q3 (S215) |
| Recording the source behind a resource | … | cite a tool by name alone, without version or step | Q6 (S026) |
```

gives `SUPERSEDED_LIVE=0 UNENTAILED_TERM=0 MODIFIED_DEF_CITED=1 QUOTES_LOCATED=20/20` / `CURATION_R86=PASS`,
**exit 0**. The counter scores the exact routed defect as a pass.

**Consequence for C2's wording.** C2(b) as frozen says "neither routed entry's decision-table cells carry the frozen
defect terms (`modification`, `modified`) without a located quote of that entry carrying them". As written, that is true
at landing and the predicate verifies it. But its parenthetical characterisation — "the round-85 routed defect 1: an
imported distinction the cited source refuses" — names a *class*, and no byte of the instrument measures that class. Read
strictly to its two words, C2 held; read as "the imported-distinction defect is now instrumented", C2 is false, and E4 is
the witness. The class is closed at landing **by inspection of the rewritten rows, not by the counter**: at landing both
entries contain 0 occurrences of `primary`, `tool`, `version`, `step` (`r86rev-term-scope.txt`), which this seat verified
independently. C2's wording should say the closure of the class is reviewed, not counted — or the term set should be
widened and re-frozen, which it cannot be this round.

### 2.3 K2 is satisfiable by deleting the failing quote (E5a → E5b), and the stated `total ≥ 19` floor is not implemented

- E5a: one quote paraphrased so it no longer occurs in its capture →
  `QUOTES_LOCATED=19/20` / `FAIL`, exit 1.
- E5b: the same paraphrase, then the whole Q7 row deleted → `QUOTES_LOCATED=19/19` / `PASS`, **exit 0**.

The denominator is whatever survives parsing, so an unlocatable quote is "repaired" by deleting it. `claims.md` states
the predicate as "`QUOTES_LOCATED` equal to its total **with the total ≥ 19**"; the counter's predicate is
`quotes_total > 0 and quotes_located == quotes_total`. E5c2 (keep only Q13 and Q7) prints `QUOTES_LOCATED=2/2` /
`PASS`, exit 0. The floor is asserted in prose and absent from the instrument; the same hole admits any quote row whose
text contains `|` (`len(cells) != 3` drops it from numerator *and* denominator).

### 2.4 `MODIFIED_DEF_CITED` is presence, not citation (E6)

Re-pointing the repaired row's warrant to `Q10 (S023)` while leaving Q13 in place still prints `MODIFIED_DEF_CITED=1` /
`PASS`, exit 0. C2's sentence says the row "gains the `modified` Definition quote … as its warrant"; the counter checks
only that some located quote of the entry contains `date on which the resource was changed`. The warrant linkage was
verified by this seat by reading row 48, not by the counter.

### 2.5 The term clearance is entry-scoped, so an unrelated quote clears any row (E7b)

Adding a two-word located quote `| Q14 | S023 | "Date Modified" |` (capture line 8776) and putting `modified` into the
validity row's Never — a row warranted by Q11, whose quote has nothing to do with the term — prints
`UNENTAILED_TERM=0` / `PASS`, exit 0. `joined` is the whole entry's located-quote text, so any located quote that
carries the word immunises every row of that entry.

### 2.6 What the counter never reads

`ENTRIES` is two knowledge files. It never inspects a registry `teaches` cell, an `## Inference` / `## Limits` section,
or any other entry. That is not hypothetical: at landing `corpus/SOURCES.md:34` still reads

```
| S024 | … | A last-reviewed date for accuracy is a property separate from publication or modification dates | queued | …
```

— the comparison the S031 source refuses (0 occurrences of `modified`/`modification` in its capture), stated in a live
registry cell and invisible to `UNENTAILED_TERM=0`. It is dormant only because S024 is `queued`; re-mining S024 restores
the defect with the counter still green.

---

## 3. Other cells that still state more than their warrant entails (item 4)

Out of C2 K3's reach (K3 is scoped to "a repaired decision-table row"), reported because they are in the two entries the
claim governs.

| # | cell | finding | severity |
|---|---|---|---|
| 1 | r84 "Reporting the search outcome" Do | `describe the results from records identified to studies included, ideally with a flow diagram`. The warrant Q5 (`S214` capture line 53, 15 words) stops mid-sentence at "…from the number of records identified"; "to studies included" and "flow diagram" are in the **unquoted** tail (`…in the search to the number of studies included in the review, ideally using a flow diagram.`, lines 53–54). The capture supports the row; the warrant cell does not. | medium |
| 2 | r84 "Comparing evidence-based generation approaches" Do and Never | Q8 (`S018` line 76) is a diagnosis: "the field is fragmented due to inconsistent terminology, isolated evaluation practices, and a lack of unified benchmarks." The Do's prescription ("use a shared taxonomy and unified benchmarks rather than isolated evaluation practices") and the Never's "without noting the fragmentation" are not stated or entailed; "shared taxonomy" is not in the quote ("inconsistent terminology" is). | medium |
| 3 | r85 row 1 Never | Q1 is capability — "chains … **can be** formed using the `prov:wasDerivedFrom` property" — the Never makes a derivation link a duty when the entities are known. Same modality residual the round-85 check recorded for the Do. | low |
| 4 | r85 row 3 Never | Q4 "**can be used** to bound the starting and ending moments" → "describe an entity as atemporal" prohibited. Same modality residual; the round-85 check already logged this as wording strength, not a firing. | low |
| 5 | r85 row 4 Never | Q5 says detailed provenance "includes facets **such as** …"; the Never turns an illustrative facet list into "ship data with no record of how it came to be". | low |
| 6 | r85 row 6 Do | the "and/or" → "and" tightening described in §1b. | low |
| 7 | five truncated quotes | r84 Q4 (ends "…criteria of the review", no ellipsis), Q5 (ends "…identified"), Q6 (ends "…verifiability"); r85 Q5 (ends "…conditions"), Q6 (ends "…given credit"). Each is a sentence fragment presented as a quote; the counter's substring test accepts truncation, and #1 is a row that leans on a truncated tail. | low |

---

## 4. A landed record contradicted by its own bytes (found while locating the quotes)

`corpus/lessons/round-86.md:27–28` states:

> The re-fetch of the same URL produced different bytes (txt sha `20dc0c3ab772…`, previously `f5545a19…` stored under the
> same key), so the capture is the newer body and the line number is the one measured on it.

Committed bytes say otherwise (`r86rev-capture-identity.txt`):

- `sha256sum corpus/captures/f5545a194c06ab421875b047.txt` → `20dc0c3ab7724e1f4be59217c190fa796a66c29b7a653e8d707d64f5fac43a79`,
  148784 bytes — **identical at base and at landing** (`git show 3bfb6885:… | sha256sum` gives the same value).
- `git log --oneline 3bfb6885..667a5d09 -- corpus/captures/f5545a194c06ab421875b047.txt` → no output; the round's only
  capture writes are the two new files `52db06f9…` and `b1b13a12…` (`git diff --stat`).
- `f5545a19…` is not a previous content hash: `printf '%s' 'https://www.dublincore.org/specifications/dublin-core/dcmi-terms/' | sha256sum | cut -c1-24`
  → `f5545a194c06ab421875b047`, the capture **key**. `corpus/evidence/round57/refetch.tsv` has separate `key` and
  `txt_sha256` columns, and its three S023 rows (lines 172/174/184, attempts at 02:16:27Z, 03:54:40Z, 06:00:11Z) all
  record `key=f5545a194c06ab421875b047` and `txt_sha256=20dc0c3ab772…`. The lesson compares column 9 against column 3.

So no re-fetch produced different bytes and the capture is not "the newer body" — it is the round-84 body, and the
line number 8786 is measured on bytes that have not moved. The substantive conclusion (Q13 at 8786) is correct; the
record's account of how it got there is false, in the exact class QUALITY lesson 154 ("a located quote is re-opened …
before the row is written") exists to prevent. Severity: **medium** — it is a landed narrative claim whose own bytes
contradict it, and it would mislead the next round that assumes the old capture body is recoverable at a prior key.

Two adjacent registry observations, offered as the item-2 answer rather than defects:

- **S024's revert is exact.** `diff <(git show 3a17f4da:corpus/SOURCES.md | grep '^| S024 ' ) <(git show 667a5d09:… )`
  → exit 0 (`r86rev-s024-revert.txt`). The lesson's "restores the row to its pre-round-85 bytes" is true, including
  `anchor` and `opened`; the round-85 intermediate state is the one at `02df67db`.
- **S031's `opened` cell and its anchor disagree** about when the source was opened (`opened 2026-10-21`, anchor "page
  re-opened 2026-11-08"). `CORPUS.md` defines `opened` as "ISO date the row's author opened the source" and rule 2 freezes
  it, so the round could not bump it; the anchor is the only record of the re-open and the lesson discloses the anchor
  edit. A contract tension, not a fixable defect this round. Note that the round-86 revert of S024 (status/used-by
  restored, plus `anchor`/`opened`) is itself an in-place edit of two cells rule 2 calls immutable; the lesson names round
  85's violation but not its own, and rule 2's "a correction is a new row" would have preserved both rows.

---

## 5. Verified, not assumed

- Counter line and exit code at landing; base control reproduced exactly (§0).
- All seven instrument pins match the landed bytes; subject tool sha matches `claims.md` (`r86rev-pins.txt`).
- All 20 quotes re-derived independently against each row's own registry URL and capture, normalised (curly quotes folded,
  whitespace collapsed) — **20/20 located**, with line numbers: r84 Q1 17, Q2 18, Q3 19, Q4 20, Q5 53, Q6 and Q7 and Q8
  each at 76/120/198/233, Q9 10318/13363, Q10 3256/4164/4720/4902/5084/7698/8796/11527, Q11 11517, Q12 3246, Q13 **8786**; r85 Q1 779, Q2 780,
  Q3 781, Q4 1021, Q5 453, Q6 453, Q7 **211** (`r86rev-quotes-verbatim.txt`).
- Registry parse coverage: 217 row-shaped lines, 217 parsed with 11 cells, none dropped — `SUPERSEDED_LIVE=0` sees every
  row (`r86rev-registry-parse.txt`). All six cited rows have single-URL source cells, so `urls[-1]` is unambiguous here.
- Term counts that decide the two repaired rows: S023 capture `modified` 4 / `modification` 0; S031 capture `modified` 0 /
  `modification` 0; both entries at landing `primary`/`tool`/`version`/`step` 0 (`r86rev-term-scope.txt`).

## 6. Residual risk and verification gaps

1. **C2's closure of the imported-distinction class is not instrumented.** E4 passes the round-85 defect bytes. Any later
   round that trusts `UNENTAILED_TERM=0` as a class result is trusting a two-word substring test. Highest-value residual.
2. **K2 has no denominator floor in code.** E5b/E5c2: deleting the failing quote row, or 18 of 20 quote rows, restores
   `PASS`. The prose floor "total ≥ 19" is unimplemented.
3. **Registry `teaches` cells are outside every check**; S024:34 carries the refused comparison today.
4. **Entailment of the non-repaired rows** (§3 items 1–2) is the class of defect that round 85 routed and round 86 fixed
   only where it was named. Nothing in this round's predicate would find the next one.
5. **Not checked by this seat** (outside a K3 seat's scope and not claimed): C1's battery, the D1/M17 derivation, the
   egress table's completeness, and whether the round's fetches stayed inside it.

VERDICT: R86ReviewerEntry C2 held — both repaired Nevers now state only what their located quotes state (Q13 at S023 capture line 8786, Q7 at S031 capture line 211) and the frozen predicate prints `SUPERSEDED_LIVE=0 UNENTAILED_TERM=0 MODIFIED_DEF_CITED=1 QUOTES_LOCATED=20/20` exit 0, but the counter passes the round-85 defect bytes verbatim (E4), so C2's class-level closure rests on this review, not on the instrument.
VERDICT: R86ReviewerEntry C1 n/a — C1's battery, D1 class and M17 derivation are outside this seat's assignment and were not run or judged.
