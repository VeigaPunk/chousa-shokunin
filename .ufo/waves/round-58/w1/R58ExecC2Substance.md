# R58ExecC2Substance — C2 quote-substance evaluation (S101 carrier alphabet)

Seat: C2 substance/depth. Evaluate all 12 frozen quotes in `corpus/evidence/round58/c2/quotes.tsv` against the defined OLE text form and the 12-row threshold in `corpus/evidence/round51/quote-substance-check.py`. Frozen inputs read-only: claims `round58/claims.md`, counter `round58/c2-count.py`, builder pin `1ed2650…c80bf6`, capture-text pin `2c0140…e2573`, raw `6dc68fd6b32ce9c8dfcebce8` (sha `6063a3af…d9fddf3`), freeze `9e73a031ab1ac3bac343de008850d7d87f9e5634`, claim base `b13ca7b5c8bbb40d2d29a37fb443c64ca043f791`. No live fetch; no lane file edited. Scratch: `/fast/scratch/hyaku/chousa-r58/R58ExecC2Substance/`.

## 1. Defined form reproduced

`tools/capture-text.py` (sha verified `2c0140bc…e2573`) on the committed raw gives a 27012-char form; `text_form()` and CLI stdout are byte-identical: `text_form len 27012 cli len 27012 equal True` / `tf has CRLF False cli has CR False`. Raw digest = `6063a3aff7a4081e93a685f2721e2cd6b477ba84a841211e298bcddd6d9fddf3`; `sha256(url)[:24]` = `6dc68fd6b32ce9c8dfcebce8` = the committed capture name, so the builder's cache lookup resolves to the lane-held capture.

## 2. Per-quote support — 12/12 bind uniquely

Every frozen quote occurs **exactly once** in the defined form; `form[occ:occ+len]==quote` for all 12. Offsets are the quote occurrence offsets.

| # | occ | ns | len | anchor | # | occ | ns | len | anchor |
|---|---|---|---|---|---|---|---|---|---|
|1|315|13|14|**yes**|7|797|19|19|no|
|2|330|35|36|**yes**|8|838|31|33|no|
|3|590|13|13|no|9|965|26|27|no|
|4|683|29|29|no|10|993|32|33|**yes**|
|5|734|19|20|no|11|1460|27|27|no|
|6|781|15|15|no|12|11723|20|21|no|

Exactly **3 line-start anchors** (Q1 315, Q2 330, Q10 993) — meets the claim's "≥3 anchors" under the occurrence-offset reading. Byte fidelity: the set preserves the source's mixed punctuation — Q2 `，` U+FF0C / `．` U+FF0E; Q8–Q10 `；` U+FF1B; Q8's `–` U+2013 EN DASH inside `CD–ROM` vs the `—` U+2014 separator; Q11 ASCII `,` `.`; Q12 ASCII `(`/`)`. Each is present exactly once, so the strings are faithful, not normalised.

## 3. The 12-row substance threshold — PASSES

Manifest built from the frozen set with the **pinned** builder, then the existing round-51 checker on the scratch-built manifest:

```
$ python3 -B corpus/evidence/round51/quote-substance-check.py <scratch>/build/spans.tsv
IDS=1 QUOTES=12 FAILURES=0
rc=0
```
Same rc=0 on the occurrence-offset shape. Floors: MIN_CHARS=3 (all rows ≥13); LONG_CHARS=12 (max 35); no OVERWIDE_SPAN (all ≤ quote+160). The checker discriminates: replacing Q3's quote with the 2-char `标识` gives `HOLLOW_QUOTE S101 '标识'` + `OVERWIDE_SPAN … len=173`, `FAILURES=2`, rc=1.

## 4. STRUCTURAL (fatal to C2 as frozen): counter offset semantics contradict the pinned builder

`c2-count.py:100–103` requires the manifest `offset` column to hold the **quote occurrence offset** (`occurrences[0]!=off` → `CAPTURE_BIND`). But the **pinned round-55 builder** writes the **span start** (`build-spans.py`: `start=max(0,off-CONTEXT)`; `lines.append(… str(start) …)`), and C2's REBUILD leg demands byte-equality with that builder's output. The two offsets differ by exactly 80 on every row — one leg must fail. Measured on an otherwise fully conforming candidate:

**E1 — builder-produced manifest (span-start offsets):**
```
QUOTE_ROWS=12/12 CAPTURE_BOUND=0/12 ENTRY_QUOTES=0/12
SUBSTANCE=PASS ANCHOR_BOUND=0/3 … REBUILD=MATCH
ERROR CAPTURE_BIND:S101  (×12)   ERROR CAPTURE_BOUND=0/12   ERROR ANCHOR_BOUND=0/3
C2=FAIL
```
**E2 — occurrence-offset manifest (what CAPTURE_BIND demands):**
```
QUOTE_ROWS=12/12 CAPTURE_BOUND=12/12 ENTRY_QUOTES=12/12
SUBSTANCE=PASS ANCHOR_BOUND=3/3 INFERENCE_GROUNDED=yes STRAY_IDS=- NEW_GROUND=yes REBUILD=FAIL
ERROR BUILDER_REBUILD_MISMATCH
C2=FAIL
```
Mutually exclusive by construction: the column cannot be both. The span *files* are byte-identical between shapes (`span FILES byte-identical … True`); only the `offset` column differs (235 vs 315, 250 vs 330, … 11643 vs 11723).

This is an **outlier vs lane convention**, not a new convention. `round51/c2-count.py:211` and `round55/c2-count.py:264` use `ft[o:o+len(span)]==span` (span-start reading); `round51/c2-count.py:207` recovers the occurrence as `int(offset)+span.find(quote)`; round-51/57 manifests show the quote 80 chars into the span; and round-58's own `c1-count.py:133–137` requires `offset == max(0, form.find(quote)-CONTEXT)` (span-start). So within round 58 the two counters disagree about the same manifest format, and the C2 quote set was selected under the occurrence reading (exactly 3 anchors; under span-start offsets the same quotes yield `builder-start anchors: 0`).

**Consequence:** `C2=PASS` is unreachable for any artifact set. Proposal to the L1 (not applied): reconcile counter-side by accepting the builder's span-start column and recovering the occurrence as `off + span.find(quote)` (as rounds 51/55/57 do), and re-express the anchor leg the same way; the builder-side alternative breaks the C1 pin.

## 5. Quote support and claim breadth

Supported by the located text: the reference-type section (Q1) and its GB3469 single-letter **rule** (Q2); electronic double letters (Q3); the carrier-marking requirement (Q4, scoped in-source by `对于非纸张型载体的电子文献`); carrier codes MT/OL (Q5/Q6); the `[type/carrier]` composition (Q7); the three examples (Q8–Q10); the publication element (Q11); the separate document-code heading (Q12), whose span carries `11中图分类号(CLC number)` and `11.1 具有文献标志码的文章应标注分类号`.

**Unsupported — flag to the entry author (measured against `inference-ground.py`):**
1. **The single-letter alphabet `M C N J D R S P G B O K`.** The table is two OLE columns 68 chars apart (`普通\n图书` at 375, first `M` at 443), not contiguous; Q2's span (form[250:446]) reaches only `…文献类型\n标识\nM` — **M alone**; C–K fall outside every span. Bullet `` `M C N J D R S P G B O K` `` → `INF_TOKEN_NOT_IN_SPAN`, GROUND: FAIL. State only that GB3469 prescribes single letters.
2. **`DB CP EB` as a spaced token** → `INF_TOKEN_NOT_IN_SPAN`. The groundable forms are the contiguous label `电子文献类型标识` (in spans 3 and 4) and the letters as printed.
3. **Universal carrier-marking rule.** The paper-carrier exemption `以纸张为载体的传统文献在引做参考文献时不必注明其载体类型` sits at form 1081 and is **truncated in Q10's span** (only `…不必注明其载`, 25 of 28 chars, cut at the 1106 boundary); it appears in no other span. A bullet asserting the rule universally is not supported by the located text; the clause is groundable only in truncated form.
4. **Present-day standards validity** (e.g. `GB/T 7714-2015`) → `INF_TOKEN_NOT_IN_SPAN token='7714'` / `token='2015'`. The claim text correctly excludes this scope.
5. **Polarity exposure.** `不必` occurs in span 10 only; restating the carrier rule at the opposite polarity to its span is exposed to `INF_POLARITY_FLIP` (Q4/Q10 area).

**NEW_GROUND is vacuous (falsification probe).** The counter's base-side grep uses traditional `載体类型标识` (U+8F09) while the entry-side test requires simplified `载体类型标识` (U+8F7D) — different code points, so the base check does not test the string the entry must contain. On the real base both are absent (`git grep -c '載体类型标识' b13ca7b5… -- corpus/knowledge` rc=1; same for the simplified form), so `NEW_GROUND` is not falsified there. But injecting the **simplified** string into the base commit in a scratch clone still gave `NEW_GROUND=yes` — because the corpus never uses the traditional form (`defined form: 載体类型标识=0, 载体类型标识=4`).

**New-ground overlap / registry.** The base already carries S101 document-code material in `corpus/knowledge/citation-count-semantics-r37.md` (`文献标志码` ×2, `文献类型及载体类型标志` ×1), and `corpus/SOURCES.md:111` records `used-by = corpus/knowledge/citation-count-semantics-r37.md`. The new entry must **append** its path to that cell (counter: `ENTRY_REL in cells[10]`), not replace it — QUALITY rule 100 requires an old→new used-by update. `cells[7]=='mined'` already holds.

## 6. Cross-claim check — C1 and C2 are not independent as claims.md asserts

claims.md says C2 "uses the pinned round-55 builder … so it is independent of C1's tool change." The counters make that false in practice: C2 requires `sha(root/tools/build-spans.py)==1ed2650…c80bf6` (`BUILDER_PIN`), while C1's claim is to change `tools/build-spans.py`. Measured in the scratch clone — appending one comment line to the lane builder flips C2 to `ERROR BUILDER_PIN` / `ERROR BUILDER_REBUILD_MISMATCH` / `C2=FAIL`. Unless C1's change lands in a separate file and `tools/build-spans.py` is left byte-identical, both claims cannot pass. Flag for the L1.

## 7. Other legs checked; scope

`PROVENANCE_TRIO`/`S101_NOT_IN_SOURCE` need the entry's **first three lines** to be `source:`/`verified-at:`/`recheck:` with `S101` in line 1. The lane convention is title-first (75 of 82 entries open with `#`), but 5 are source-first (`capture-path-pin-r41`, `reader-allocation-r26`, `receipt-expectation-digests-r40`, `recheck-due-r26`, `registry-link-r26`) — an established variant. `STRAY_IDS`: cite only `S101`. `INFERENCE_GROUNDED=yes` was reached with five Inference bullets each quoting a span-contained phrase (`tools/inference-ground.py` rc=0). No lane file edited (only this report and my scratch tree); no live fetch; no alteration or reinterpretation of `claims.md`, `c1-count.py`, `c2-count.py`, `quote-substance-check.py`, the controls, or the quote set — findings are reported against them, not fixed. The C1 counter was not run and C1 is not judged. The `controls/c2-controls.txt` STAGED/REWRITE controls fail on missing manifest/capture, so they do not discriminate the §4 offset contradiction.

VERDICT: The C2 quote set and the 12-row substance threshold **survive** — all 12 quotes bind uniquely to the defined OLE text form with faithful punctuation and clear the round-51 threshold (`IDS=1 QUOTES=12 FAILURES=0`, rc=0, and the checker discriminates on a hollow quote). But the frozen C2 predicate is **falsified**: the attack is the concrete measured conflict between `c2-count.py`'s occurrence-offset `CAPTURE_BIND` and its own `REBUILD` leg against the pinned round-55 builder, which writes the span start in that column (`CAPTURE_BOUND=0/12 REBUILD=MATCH` vs `CAPTURE_BOUND=12/12 REBUILD=FAIL`; the round-58 C1 counter and rounds 51/55/57 all use the span-start reading, so `c2-count.py` is the outlier), and `NEW_GROUND`'s base check tests U+8F09 while the entry test requires U+8F7D, so a base already carrying the simplified string still passes. Three claim shapes are **inconclusive/unsupported** by the located text: the single-letter alphabet enumeration, the spaced `DB CP EB` token, and a universal carrier-marking rule.
