# RevC3Entries — both adopted entries read against their captures (R46 wave 2)

seat: L1Chousa46.RevC3Entries (leaf, no dispatch) · target: lane commit `d09fc8e7e2972e30e5e0aaa6e404c97aa0b9f95a`
method: read `corpus/evidence/round46/claims.md` first and changed no predicate, counter target or kill rule;
then located every quoted token and every stated figure, char pointers included, in the five on-disk captures. No fetch.

## Verdicts

- `corpus/knowledge/evidence-pool-versioning-r39.md` — **findings listed** (1 medium, 2 low).
- `corpus/knowledge/evidence-pool-versioning-r39-amendment-2026-10-23.md` — **findings listed** (1 high, 2 medium, 3 low). Not clean.
- C3 **as declared** still verifies: both counter modes pass and every declared leg holds. The defects are in the prose layer the predicate does not read.

## Clean legs confirmed (on record, not re-litigated)

- `sha256sum` of all five `.qcache` captures equals the `capture_sha256` column of `spans.tsv` (4146 / 60153 / 5676 / 12775 / 126093 bytes).
- `python3 corpus/evidence/round46/c3-count.py` → `C3=PASS` exit 0: `ENTRIES=2/2 CITES_BOUND=5/5 QUOTE_ROWS=11/11 QUOTES_IN_SPAN=11/11 QUOTES_IN_ENTRY=11/11 CAPTURE_BOUND=11/11 REF_ID_UNBOUND=0 REF_BOUND=2/2`; `--lane-only` → `CAPTURE_BOUND=skipped`, `C3=PASS`.
- All 11 rows re-derived independently (`ct[offset:offset+len(span)] == span`): exact slices, **exactly 80 chars of context on each side**, each quote occurring once in its capture.
- No staged-id remnant in either entry: `grep -oE '\bS[0-9]{3,}\b'` yields only S079, S081, S082, S084, S085–S089. S120/S122/S127/S128 occur only in `claims.md`, where they name the staged package.
- Cross-refs bind by document: `SOURCES.md:89` S079 = RFC 7089, `:91` S081 = NDL E2867 WARP; `:92` S082 and `:94` S084 exist `mined` with the named files in `used-by`.

## Entry 2 — `corpus/knowledge/evidence-pool-versioning-r39-amendment-2026-10-23.md`

**E2-1 HIGH — a stated figure sits in the wrong population, and the entry's own two numbers cannot both hold.** `:26` says "counts 5,959 of 7,572 real-source answers carrying a web.archive.org link and 1,582 giving no archive field at all". The cited record disagrees (`corpus/knowledge/evidence-snapshot-coverage-r40.md:12`): "1,582 answers name a `source_url` and carry no archive field at all, **1,491 of them a real source rather than `Metadata`**". So 1,582 is counted over *all* answers naming a `source_url`; inside 7,572 real-source answers the no-field count is **1,491** and the complement of 5,959 is 1,613. As written 5,959 + 1,582 = 7,541 ≠ 7,572. The correct split (5,959 + 1,491 + 74 other archivers + 48 tail) is exactly 7,572. `:11` gets the same split right ("the rest carry no archive field **or** something that is not an archive link"), so this reads as a transcription slip — but as committed it overstates by 91 and contradicts itself. Fix: 1,491, or restate the 1,582 population.

**E2-2 MEDIUM — an unspanned quote carries a wrong char pointer, off by 21.** `:11` quotes `"all source pages are archived on the internet archive"` at "char 14603 of the S089 capture". The quote is verbatim and occurs once, at **14582**; `c[14603:]` is `'archived on the internet archive. 2 2 …'`. The drift is exactly the length of `"all source pages are "`. This quote is not one of the eleven committed spans, so neither `c3-count.py` mode checks it.

**E2-3 MEDIUM — a staged contradiction was corrected silently, against this claim's own kill rule.** The staged amendment (`/home/vgpnk/Projects/shokuknow/merge/chousa/knowledge/corpus/knowledge/evidence-pool-versioning-r39-amendment-2026-10-23.md`, `## Unknown` first bullet) says the examples show `cached_original_claim_url: null` **for claims that first appeared on the internet**. Landed `:26` asserts the opposite reading (nulls co-occur with a null `original_claim_url`; "the hedge appears to follow whether an original URL exists at all"). `claims.md` R46-C3: "A staged sentence that the captures contradict is corrected in the entry **and recorded as a mistake**". The landed `:29` lists three corrections (ASCII apostrophe, two prose ids re-bound, a staged amendment-id pointer replaced) and not this one. Add it.

**E2-4 LOW — the third null-pairing pointer lands on a different field.** `:26` cites "(chars 4444, 6228, 9920)". In the capture `"original_claim_url": null` sits at 4422/6206/9927 with its `null` value at 4444/6228/9949, so the first two point at the asserted value; **9920 is `"speaker": null`'s value** (that record carries an extra `speaker` field), seven chars before the key the sentence is about. Repair to 9949.

**E2-5 LOW — a claimed blind spot is visible in the capture.** `:26` ends "How often a claim WITH an original URL lacks a capture was not measured from this capture." The capture holds exactly one record with a non-null `original_claim_url`, and it carries a matching capture (`https://web.archive.org/web/20230420110107/…`, char 8330). n=1 is not a rate, but "not measured" is wrong — say "one such record, which carries a capture".

**E2-6 LOW — the four-label anchor points only at the fourth label.** `:14` cites "char 1142"; 1142 is `"Conflicting`. The enumeration starts at 1093 (`"Supported"`) and "four labels" at 1080. Anchor at 1080 or 1093.

Checked and correct (left alone): `Where possible` (3185), the `cached_original_claim_url` / `original_claim_url` dictionary sentences (3157+), `claim_date` (2904), the archive-link sentence (3929), the worked-example live/archived pair (5100–5340), `Unanswerable` with `"source_url": ""` and no archive field (9375), the three-problem/three-mechanism pairing including `two-stage sufficiency check` (2928–3090), `κ = 0.742` (3200), `74.7 %` with the space (3239), and that the restriction is predicated of annotators ("Next, annotators convert … while being restricted to …", 6850–7145). "Every null `cached_original_claim_url` sits on a record whose `original_claim_url` is also null" is true 3/3; the fourth record has both filled.

## Entry 1 — `corpus/knowledge/evidence-pool-versioning-r39.md`

**E1-1 MEDIUM — Observation asserts a qualifier its own Unknown disclaims, and the disclaimer is false.** `:16` states "the comparator is human annotators against the super-annotators' **exhaustive** evidence set"; `:28` states the word "exhaustive" occurs 0 times and "the paper's framing of that comparison was not read closely enough here to state more". Both cannot stand. The capture settles it for `:16` — S086 at 19300: "The purpose of this exercise was to provide as much coverage of evidence as possible. We instructed the super-annotators to search over the whole Wikipedia for **every possible sentence** that could be used as evidence. We compared the regular annotations against this set of evidence" (§3.4.2, in the capture). So the Observation is defensible but unanchored (no span, no offset) while the Unknown understates what was read. Either cite §3.4.2 at the qualifier or drop it — do not carry both sentences. `SOURCES.md:97` (row S086) repeats "against a super-annotator's exhaustive set" with no offset; same repair.

**E1-2 LOW — "label-validation pass" narrows what 91.2% measures.** `:16` and the Inference call it "its own label-validation pass" / "label validation is stated as". The capture's §3.4.3 is a combined check: "we chose 227 examples and annotated them for accuracy of **the labels and the evidence provided**. We found that 91.2% of the examples were annotated correctly." The figure is label *and* evidence correctness; calling it label-only misstates its bearing on the evidence step, which is the entry's actual subject.

**E1-3 LOW — off-by-one on the Zenodo revision pointer.** `:27` cites `"revision": 2` at "char 3667"; the field starts at 3666 (`c[3660:3690] == '954", "revision": 2, "files": '`). The `null`-value convention used at 4444/6228 is fine; 3667 breaks it by one. "Zenodo's deposit revision" is read off the field name, not stated — keep the hedge.

Checked and correct (left alone): "names four fields, none of them a revision" (the capture enumerates exactly id/label/claim/evidence), `grep -c revision` = 0 over the whole S085 capture, "for internal use only" at 2593, the four-position tuple at 2349, 95.42% at 6741, 0.6841 at 1869, 31.75/16.82/12.15 at 5534/5842/5929 mapped to more-than-one-sentence / several sentences / more-than-one-page, `build 385` and `2026-04-02`, `publication_date 2018-04-03`, `conceptdoi` (171), `wiki-pages.zip` (4929).

## Gate coverage note (depth axis; distinct from the wave-1 findings)

The eleven-row manifest covers exactly the eleven committed quotes. The two entries carry about twenty prose char pointers and **`c3-count.py` checks none of them**: `QUOTES_IN_*` iterate only `spans.tsv`, and `REF_BOUND` is a sentence-token check. Of the 20 pointers tested by hand, **4 are wrong** (14603 by 21; 9920 by a field; 1142 by an enumeration; 3667 by one) and one figure (1,582) is misbound. That prose-and-figure layer is where the entries' accuracy lives, and it is outside the frozen predicate — reported as measured shape, not as a proposed rule change.

## Residual risk / verification gaps

- The staged package was read only (no tool run under `shokuknow`); the "recorded as a mistake" finding rests on the landed `:29` list, not on separate rule text.
- "Exhaustive" is my reading of "every possible sentence … over the whole Wikipedia" plus "as much coverage as possible"; a stricter reader may still prefer the entry to quote that instead. Either way `:28`'s "not read closely enough" is wrong.
- Registry cells for S085–S089 were checked only to the level `c3-count.py` asserts (URL, `mined`, `used-by`) plus the `exhaustive` contamination at E1-1.
- `c3-count.py` passing is not evidence that any prose figure is right: it reads `spans.tsv` and entry tokens, never `r40`/`r41`.
