# R59Scout32 — bounded offline data walk

## Result

The prescribed round-59 frozen claims file is missing in the visible lane snapshot, so no round-59-specific claim can be adjudicated from the requested authority. Available artifacts support a bounded predecessor-defect finding: the round-58 C1 aggregate's positive verdict path was already identified as vacuous, and the round-59 `c1-before` receipt records hazardous behavior rather than a positive control.

## Observed evidence

- The required `corpus/evidence/round59/claims.md` read returned “not found.” Lane enumeration shows `corpus/evidence/round59/census-start.txt` and `controls/c1-before.txt`, but no `claims.md`. Round-58 `claims.md` exists; it freezes distinct round-58 C1/C2 assertions and pins its counter, so it is not a substitute for round-59 claim bytes.
- `corpus/evidence/round59/controls/c1-before.txt` records `FOREIGN=fail(rc=0, orphans deleted: foreign gone=True)`, `SYMLINK_OUT=fail(...)(target-dir-written!)`, `SYMLINK_CACHE=fail`, and `MANY_QUOTES=fail(rc=0, expected refusal)`. FIFO/device/raw-size legs report refusals but lack the expected diagnostic tokens. It ends `SUMMARY OK=4/4 REFUSE=0/7 ...`, `C1=FAIL`, `EXIT=1`. This is a captured receipt, not a fresh execution.
- `corpus/lessons/round-58.md` §Mistakes identifies the round-58 counter defect: its success tokens are lowercase `pass`, while refusal aggregation checks uppercase `=PASS`; documented all-legs-positive probe therefore still produced `C1=FAIL`. The lesson expressly disclaims an admitted C2 knowledge entry and current GB3469 legal/status claims because the frozen predicate failed and the fetch-scope question stayed open.
- `corpus/evidence/round58/claims.md` lines 15–19 anchors the predecessor C2 source claim to lane-held S101 (HIT specification capture) and requires quote/digest/offset binding. This establishes a prior local-source trail, not a fresh round-59 source or standards-validity finding.
- `corpus/evidence/round59/census-start.txt` records five W04 duplicate-URL warnings and a successful census exit. It is census context, not a claim predicate or positive-path control.

## Inference and limits

Inference: round-59's available before receipt cannot demonstrate positive-verdict-path calibration: it ends FAIL and records unsafe outcomes. The prior lesson gives a specific mechanism for the analogous round-58 counter, but absent round-59 claim/counter bytes I cannot assert that the same exact counter revision or predicate governs this round. No live fetch or execution was performed. L0 fetch-scope question `8d77e6c1` remains open per assignment; current validity of external standards is unresolved.

## Remaining unknowns

Exact frozen round-59 claims and counter bytes; whether round-59 intended to reuse the round-58 predicate; whether a conforming positive control reaches the declared final verdict under the exact intended artifacts; and any authorized external research window/source for present-day standards claims.

Report trailer: `.ufo/waves/round-59/w1/R59Scout32.md`.
