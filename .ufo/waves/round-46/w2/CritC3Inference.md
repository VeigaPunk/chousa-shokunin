# CritC3Inference — round 46 w2 (falsify), C3 inference audit

seat `L1Chousa46.CritC3Inference-2` · target `d09fc8e7e2972e30e5e0aaa6e404c97aa0b9f95a` · claims frozen `c2f0e9d1`
Scope: both adopted entries' **Inference** sections, bullet by bullet — does each inference follow from the spans it cites, or does the lane's frame replace the source's? No fetch; captures under `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache`.

## Re-runs (verbatim decisive output)
```
$ python3 corpus/evidence/round46/c3-count.py
ENTRIES=2/2 CITES_BOUND=5/5 QUOTE_ROWS=11/11 QUOTES_IN_SPAN=11/11 QUOTES_IN_ENTRY=11/11
CAPTURE_BOUND=11/11 REF_ID_UNBOUND=0 REF_BOUND=2/2 C3=PASS                 (exit 0)
$ python3 corpus/evidence/round46/c3-count.py --lane-only
CAPTURE_BOUND=skipped … C3=PASS                                          (exit 0)
$ # independent re-derivation of all 11 rows (offset, capture sha256, slice, context)
S085-1 qlen=23 prefix=80 suffix=80 capsha_ok=True slice_ok=True    … identical shape for all 11 rows
```
Span mechanics sound. Entry shas at d09fc8e: base `6ffbb8f8…0217b5`, amendment `84197ced…138c8c`, `spans.tsv d9bdd226…225964`.

## (a) "durability comes from freezing the pool, not from stamping each citation"
**F1 — base:20 FAILS as written.** S087 = `7800e2e1e2df3bc124b6b83e.txt`, 5676 B, sha256 `dfc3e0f5…00ed`:
```
'"doi": "10.5281/zenodo.4925954"' at 138      '"conceptdoi": "10.5281/zenodo.4925953"' at 171
'"relations"' at 1439 → {"version":[{"index":0,"is_last":true,"parent":{"pid_type":"recid","pid_value":"4925953"}}]}
'"latest"' 2541   '"versions"' 2669           '2017' 0   'June' 0   'dump' 0
```
(i) **Field inversion.** `doi` …4925954 is the version id; `conceptdoi` …4925953 == `conceptrecid` == `links.parent_doi`, and the record publishes `versions/latest`. `:20` calls the concept DOI "a versioned …", `:21` "the version is the deposit's conceptdoi" — the series pointer presented as the frozen per-version one; a later deposit moves it, so fixity is inverted, not established. (ii) **Identity not in the capture.** S087 never says `wiki-pages.zip` is the June 2017 dump (0 hits for 2017/June/dump); it says only "sentences extracted from Wikipedia". So "the deposit fixes the pool as a file … the state a verdict points into is dated at the corpus" does not follow from S087; the date still comes only from S085/S086.
The **staged original had it right** ("versioned Zenodo concept (doi 10.5281/zenodo.4925954, concept doi 10.5281/zenodo.4925953)"); the adoption broke it unlogged (`:30`). Repeats at `corpus/README.md:1065`. Minor: the dump title is tagged `(S085, S086)` but is 0 in S086 (which has `used the June 2017 Wikipedia dump, processed`, 1 hit).
**Holds:** date provenance (S085 download list, S086 build sentence) and "no per-citation stamp" (four fields at S085 2349; `revision` 0 in S085).

## (b) the amendment's "same instrument the lane already holds"
**F3 — amend:21 FAILS.** The lane's own holdings refuse it: `citation-version-binding-r37.md:17` "The cadence is the operator's own statement, not a Memento header. **The two are not the same mechanism.**"; `-r36.md:16` "The lane's span check against an archived capture checks the capture. It does not check the origin's past output." `cached_source_url` is a third thing — a stored copy the annotator pasted in (`b73f7e8d…46.txt` 3849, 3929 "An archive.org link for the source url") — neither S079's Memento header nor S081's timestamp-in-URL. Nor does the lane hold it *for its own sources*: its capture is `sha256(url)[:24].txt` (`c3-count.py:64`), content-addressed, no archive.org. `:29` cites r36/r37 as two distinct points, then `:21` merges them; base `:23` has the correct weaker form.
**F4 — amend:19 holds narrowed.** "fixed by a timestamped capture" overstates a documented link; the lane already holds S083 ("a filled archive field is a link to open, not proof of a resolving capture") and r40 (551 of 6,511 filled values are not archive links; 8 are 404-ing double archives). Narrow to "the state a verdict points at is *documented* as an archived copy of the cited page (S088; examples carry 14-digit stamps, e.g. 5293); whether it resolves is a separate check."
**F5 — amend:20 holds.** S088 `claim_date` (2824) and S089's annotator restriction (7057, subject "annotators … restricted to using only online evidence published before the claim's date") are kept apart as the captures require.
**F6 — amend:22: first holds, second fails.** Chain mode resolves anchors (r3) and `claim-support-states-r24.md` has only a per-source "states (or contradicts)" polarity — no claim-level conflict state, correct. But S088's `claim_date` is only "Our best estimate for the date the claim first appeared" (2824); nothing makes it "what turns a set of evidence items into a dated comparison" — that rule is S089's, which `:20` itself called a different corpus.

## (c) the unknown that the corpus does not address revision history
**F7 — base:27 FAILS (overstated).** (1) It answers itself: "the pages travel inside it as one `wiki-pages.zip` file — so a page-level revision is not addressable" is a deposit-level Observation; only upstream history beyond the dump stays open. (2) "not addressable" is imprecise: a page's *dated state* is addressable (one per page, June 2017); absent is a revision id or a later state. (3) "**no source opened here** says how a claim whose evidence sentence was edited upstream is handled" is false at this commit — the amendment adopted with it answers that per citation (S088 `cached_source_url`, S089 claim-date constraint), and its `ground` calls itself "a dated continuation of … which this lane now holds". Scope to FEVER or cross-reference the amendment. Nit: `"revision": 2` starts at 3666, not 3667.
**F8 — base:28 holds narrowed, contradicts base:16.** Verified `exhaustive` 0 and `revision` 0 in S086. Yet `:16` says "the super-annotators' **exhaustive** evidence set" — the word this Unknown says is absent. And "the paper's framing … was not read closely enough" is false: the frame is contiguous at S086 41931 — "the measured recall rate of annotators (see Section 3.4.2), who achieved recall of 72.36% of evidence identified by the super-annotators".
**F9 — base:22 FAILS on its premise.** "Retrieval runs at `recall of 72.36%`" assigns an annotator-agreement figure to a system: the capture's subject is annotators in two of three occurrences (41931; 6741 `95.42% precision and 72.36% recall in evidence retrieval`, inside the annotator-agreement paragraph). `:16` gets this right; the Inference reverts to the lane's frame — sharpest substitution in the pair.
**F10 — amend:26 holds narrowed.** "The archive captures are conditional" is true of AVeriTeC's claim-URL field ("Where possible"), but the successor corpus states the opposite for sources — S089 14603 "To ensure long-term accessibility, all source pages are archived on the internet archive." Say "the claim-URL archive is conditional". Denominator: r40 has 1,582 answers naming a `source_url` with no archive field, 1,491 real-source, so inside 7,572 the complement is 1,491.
**F11 — unlogged correction, amend:29.** The staged amendment called the constraint "operational, with web pages returned as evidence 'limited … to those published before the claim's date'"; the capture states it of the annotators (`:15` now does). Only the apostrophe is logged; C3's kill rule requires a capture-contradicted staged sentence to be "corrected in the entry **and recorded as a mistake**". Also `:11` quotes S089 (char 14603) inside a bullet tagged `(S088)`.

## Verdict per bullet
| bullet | line | verdict |
|---|---|---|
| I1 dated pool / no per-citation stamp | base:20 | **fails** (S087 legs); date half holds |
| I2 differs from sha256 pin; "version is the conceptdoi" | base:21 | **fails** on the field; contrast holds with record `doi` |
| I3 "Retrieval runs at 72.36%" | base:22 | **fails** per F9; conclusion survives narrowing |
| I4 RFC 7089 / WARP corroboration | base:23 | **holds** (S079/S081 mined, `SOURCES.md:89,91`; `archive`/`timestamp` 0 in S085) |
| U1 revision history | base:27 | **fails (overstated)** per F7 |
| U2 not a truth / "not read closely" | base:28 | **holds narrowed** per F8 |
| U3 no source on a rejected revision id | base:29 | **holds** |
| U4 staged corrections | base:30 | **holds** except the omitted concept-DOI regression and a garbled em-dash quote |
| A1 archived copy, not revision id | amend:19 | **holds narrowed** per F4 |
| A2 claim date vs successor rule | amend:20 | **holds** |
| A3 "same instrument … for its own sources" | amend:21 | **fails** per F3 |
| A4 fourth label / dated comparison | amend:22 | first **holds**, second **fails** per F6 |
| AU1 captures conditional | amend:26 | **holds narrowed** per F10 |
| AU2 capture = annotator's read; AU3 image-text, no recall figure | amend:27-28 | **both hold** (title at head of `78761b63…ce9`; "image" 148) |
| AU4 staged corrections | amend:29 | **holds**; omits F11 |

## The counter cannot see any of this (mutation on a /tmp copy, deleted)
```
# apply the F1 correction to a copy:   python3 c3-count.py --root /tmp/…/corrected  →  C3=PASS (exit 0)
# append a false sentence to a copy:   python3 c3-count.py --root /tmp/…/false      →  C3=PASS (exit 0)
```
C3 scores presence of the committed quote, not whether the prose follows it — why F1/F3/F9 pass. Not wave 1's reported C1 defect; C3's own unmeasured clause is "the staged prose is corrected where the captures disagree with it".

## Smallest safe corrections (prose only; no predicate, target or kill rule touched)
1. base:20 — S087 clause → "the deposit publishes the pool as one file (`wiki-pages.zip`) in a record whose version DOI is `10.5281/zenodo.4925954`; the `conceptdoi` `…4925953` names the series"; cite S085 alone for the dump title.
2. base:21 + recheck `:7` — "the version" → the record `doi`; the recheck watches `doi`, not `conceptdoi`.
3. base:22 — "The evidence-annotation step recovers 72.36% of the evidence the super-annotators identified (S086, 41931) while label validation puts correctness at 91.2%."
4. base:16 — drop "exhaustive"; base:28 — drop the "not read closely enough" clause.
5. base:27 — "The pool exposes history only at the deposit level: the pages travel as one `wiki-pages.zip`, so a page's state is addressable as of the June 2017 dump and no revision id or later state is; the successor corpus's per-citation answer (S088) is for a different corpus."
6. amend:21 — "a third form in the same family: a stored copy of the cited state, neither S079's Memento header nor S081's timestamp-in-URL (r37), and not the lane's own byte pin (r36)."
7. amend:19 — "documented as an archived copy …; whether it resolves is a separate check (S083, r40)".
8. amend:22 — attribute the dated-comparison rule to S089.
9. amend:26 — "the claim-URL archive is conditional; the successor corpus states all source pages are archived (S089 14603)"; use the 1,491/7,572 denominator.
10. amend:29 — log the staged "operational, web pages returned" → annotator-side correction; tag `:11`'s S089 quote `(S089)`; fix `corpus/README.md:1065` (repeats F1).

## Pointers
- captures: S085 `5a631adb18988a1a2421ce75.txt` · S086 `1c15b611118dee97e4105fcf.txt` · S087 `7800e2e1e2df3bc124b6b83e.txt` · S088 `b73f7e8dd5b0ace740e48046.txt` · S089 `78761b633aee2289e5874ce9.txt`.
- spans: `corpus/evidence/round46/spans.tsv` (`d9bdd226…`); counter `c3-count.py` (CACHE :38, `key()` :64, presence checks :100-108).
- holdings: `corpus/SOURCES.md:89,91,93` · `citation-version-binding-r36.md:16` · `-r37.md:17` · `evidence-snapshot-coverage-r40.md` (Obs 2) · `claim-support-states-r24.md:8-16`.
- staged originals (read-only): `/home/vgpnk/Projects/shokuknow/merge/chousa/knowledge/corpus/knowledge/`.
- scratch `/tmp/chousa-r46w2-CritC3Inference/` removed. No install, no fetch, no lane byte written outside this report.
