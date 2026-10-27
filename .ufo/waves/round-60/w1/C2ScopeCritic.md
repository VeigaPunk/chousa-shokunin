# C2ScopeCritic — frozen C2 scope attack

## Counterexample

The strongest local counterexample is the unchanged-base run reported by the independent current-counter audit: `C2=PASS`, exit 0, although the frozen predicate says the base must fail because no round-60 entry exists. The counter points `ENTRY` to the already-existing `corpus/knowledge/citation-count-semantics-r37.md` (`corpus/evidence/round60/c2-count.py:8,13`), and tests generic metadata and a pre-existing Unknown phrase (`:17-18`). It neither requires a new round-60 correction note nor checks its claimed exact observation, prohibited overreach, or the scorecard disposition. The `--work` argument is parsed but unused (`:13`). This is not merely an untested possibility: `.ufo/waves/round-60/w1/C2CounterAudit.md:5-14` records the actual command, output `RAW_PIN=1/1 FORM_PIN=1/1 QUOTE=1/1 LINE=245 METADATA=1/1 LIMIT=1/1; C2=PASS`, exit 0 on the base state.

A second independent counterexample concerns provenance isolation. Although the CLI accepts `--root`, it builds `raw` and `entry` under the provided root but loads `form` from script-global `ROOT` (`c2-count.py:5-7,13`). Therefore a copied lane root is not a closed input set: the source form can silently come from the script checkout while the raw capture and entry come from the caller's root. Hash matching proves byte identity of that external form, not that the tested copy supplied it. The frozen contract explicitly names a `<lane-copy>` and requires the source digest/quote locations and new entry to be verified there (`round60-claims.md:15-17`).

## Source grounding and bounds

The offline S101 text form supports the narrow source-level observation: it identifies `文献类型及载体类型标志` as an element at line 245, and section 14.3.4 describes carrier notation and examples at lines 260-268 (`.ufo/waves/round-60/s101-open.txt`). The historic S101 raw capture digest is pinned in the counter (`c2-count.py:9-11`); the source registry identifies the HIT-hosted document and capture history (`corpus/SOURCES.md`, S101 row; see also the round-49 S101 hand-check summarized in `corpus/lessons/round-49.md`). This only supports what this captured document says. It does not establish current validity, authenticity at origin, CNKI implementation, or adoption by counted records. The existing entry already records version-in-force and product-application limits (`corpus/knowledge/citation-count-semantics-r37.md:74-86`), but that pre-existing scope caution cannot stand in for the claimed new correction note.

## Frozen-input identity caveat

The assignment-provided immutable claim SHA is `09d8053f5f09a26c07f41286a7a885a2c21bff31b30f71963cceaa35d971a440`; my read-only `sha256sum` observation was `65721569fc1336b159c7637acf476cda6f583bbd4b3a84aaadd239f7d02018d1`. The claims path was untracked in the lane status output. I did not alter it. I cannot determine why these identities differ; treat it as a freeze provenance discrepancy, not permission to edit/redefine the predicate. The text currently present explicitly requires exact observation/no-overreach, citation/metadata, scorecard disposition, and base failure (lines 15-17), which is the standard used in this review.

## Impacted axes / verdict relevance

- **Depth (C2): not established.** The current PASS does not establish a new source-grounded correction or constrain its wording against the capture.
- **Operability / measurement integrity: defect.** Base acceptance violates the declared counter contract; root mixing defeats isolated lane-copy measurement.
- **Calibration/discernment: risk of overclaim.** A PASS labels generic old content as verified round work and may suggest source-based admission that the counter has not tested.

These are counter-predicate defects, not evidence that S101's captured statements are false. They do not establish whether a later C2 artifact or alternate counter revision repairs the gaps; my scope is the frozen claim, current counter/source and prior evidence only.

## Smallest safe correction

Keep the frozen claim unchanged. Bind `ENTRY` to the uniquely identified new round-60 note (or enforce an equivalent base-to-target identity that proves it is newly added); assert its exact observation and explicit no-overreach boundary against located pinned source text, verify citation/metadata and the declared scorecard disposition, and exercise an absent-note base fixture that must exit nonzero. Resolve every input, including the text form, beneath `--root`; otherwise reject a non-self-contained root. Until those controls pass, report C2 unprovable/not admitted. Preserve the narrow offline-source limitation; do not turn it into a claim about current standard status or CNKI behavior.

## Evidence boundary

Read-only review of the frozen claim text and supplied hash, current C2 counter/source rendering, existing S101 knowledge entry/registry context, and local round-60 counter audit plus prior committed S101 admission evidence. No live fetch, counter invocation, source edits, claim edits, or git/jj mutation. Scratch `/fast/scratch/hyaku/chousa-r60/C2ScopeCritic` was created for this assignment and removed before yield.