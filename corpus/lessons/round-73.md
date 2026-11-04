# Round 73 — completed host measurement; invalid frozen correction counter

Freeze: `a0f094c272dcb09f1bf79e2c9057d7ea20b7ac7b`; base: `f748abbb6bf58388e732facd4ecec5612419c457`.

## Gate

No external fetch. Opened committed local sources on 2026-11-03:

- **Admit S180**, own-work B: `corpus/lessons/round-72-verifier-spotcheck.md`, section 6, V72-1 (line 90 at freeze). Located quote: “The line that actually exits is the next unguarded sub-run assignment”. The source grounds the exact correction, not shell correctness in general. C2 and this lesson cite S180.
- **Reject S181**, own-work C: `corpus/evidence/round72/controls/after-r72-corrections.txt`, header line 1 at freeze. Located quote: “every count line re-run fresh at the verdicts tree, immediately before the verdicts commit”. Its revision line names landing tip `7f7ea19a`, not verdicts tree `6dd6c82`; the SCORECARD count is 2 at the former, 3 at the latter. Reject only the header's tree attribution, not the historical count at its actual revision. Flip: corrected attribution plus re-derivation at the declared revision.

Registry delta: 179→181 rows, B 44→45, C 12→13, A unchanged 123; mined 146→147, rejected 14→15, queued unchanged 19. Command: `sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa`; before/end receipts in `.ufo/waves/round-73/`. No old status/recheck/used-by cell changed. No frontier coverage-map ground advanced.

Assimilation: none. This round uses opened local records for its frozen claims; no package adoption or external fetch approval is inferred. The read-only shokuknow package and considerthese remain operator inputs, not evidence that a source was opened.

## Measurements

C1's direct battery at freeze: `RESEARCH_GATE_SELFTEST: PASS (275 cases, 0 skipped)`, `SELFTEST_RC=0`, 275 ok / 0 FAIL / 0 skip, 80 seconds. Full preflight at the same instrument revision: `PREFLIGHT=8/8 FAILED=none ENV=none SKIPPED=none`, `PREFLIGHT_RC=0`, 92 seconds. Commands and exact revisions/digests are in `corpus/evidence/round73/claims.md` and `controls/{battery-r73,preflight-r73}.txt`. The original Windows-host control carries zero anchored verdict lines and no completing preflight.

C2's factual corrections land append-only across LOG, the round-72 lesson, and SCORECARD. Its frozen counter does **not** certify them: `load()` reads numstat column zero (additions) as removed lines. R73M01's compliant append scores 6/7; a deletion with no additions passes C2-6. The seven in-memory selftests bypass `load()` and therefore did not catch this. Frozen counter is retained unchanged, target 7/7 not met. The `:8435`→`:84350` substring survivor and fabricated C1 receipt acceptance are explicit limits, not repaired predicates.

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| symptom confused with terminating command | S180 V72-1; original r72 receipt header; gate lines 8426/8435 | none required exact termination context | append-only V72-1 correction; QUALITY 132; empirical harness in wave R73E01 |
| measurement-tree prose contradicts revision | S180 V72-2; S181 header and revision line | QUALITY 130 named revision but did not reconcile prose | append-only V72-2 correction; QUALITY 133; base and verdict-tree counts retained separately |
| frozen loader swaps additions/deletions | `c2-count.py:131`; `.ufo/waves/round-73/w1/R73M01/mutations.txt` | QUALITY 119/115: positive control should traverse the real loader | not fixed in frozen predicate; C2 honestly fails. Before a successor freeze, exercise a real committed append and a real deletion through `load()`, not only synthetic pure checks |
| structural tokens accept semantically wrong text | R73M01 `:84350` survivor; R73C01 fabricated receipt probe | QUALITY 131 | no semantic certification inferred; exact line/source review required; fabricated receipt acceptance disclosed |
| seat receipt misrooted into fleet | `ns-arm-r73s02.txt`, named for R73S02; namespace-arm contents match its assigned probe | absolute seat-path rule and pre-report fleet sweep | copied byte-exact to lane's same relative path, `cmp` exit 0, then removed only the fleet copy; unrelated pre-existing `after` left untouched |

The first two record fixes have red-before grounds in `controls/before-r73-greps.txt`; the counter defect is shown able to fail by the committed seat probes. No claim is made that the frozen loader defect was fixed.

## Outside verification and trends

Wave reviewers are author-lane evidence, never independent promotion or outside discernment verification. Fresh non-author closure remains pending. Expansion unchanged; quality improved by two actual completed instrument runs; discernment unchanged pending the outside admit/reject spot-check. C1 improved; C2 honest-stop / counter-invalid; round not admitted. Numeric operability remains historical 3/10 and no capability row is added.

## Wave settlement and integration

Parent delivered `WAVE-DONE chousa r73 w1`: all 11 seats settled; `.ufo/waves/round-73/w1-results.json` records each output, no reported dead seat. One v1 wave: 2 scout, 1 connector, 3 executor, 1 scribe, 1 revenger, 1 reviewer, 1 critic, 1 mutation-tester; attack share 3/11; L1 holds planner. No residual call, no seat replacement.

- R73E01: harness PASS 8/8 twice, byte-identical output. Copied byte-exact into `corpus/evidence/round73/controls/`; missing-file grep survives, unguarded assignment exits 2, guarded forms continue.
- R73E02: pin/drift rc 0/0, second pin rc 0, injected drift rc 1; line 8435 runs successfully here. R73E03: body rc 0 in 21.97 s; forced one-second timeout rc 124; expiry note matches extracted printf.
- R73S01: additional historical fleet-report restatements at round-72 report lines 20/54 (kill attribution) and 21 (measurement tree) require an explicit erratum in the round-73 report. Historical report bytes untouched.
- R73S02: 13 anchored historical skips; all eligible here, consistent with the direct run's measured zero skips. R73S03: no sibling report in its bounded scan claims this chousa battery; Linux-host remeasurement is not retroactive Windows approval. The old flock question remains unanswered for that old host.
- R73R01/R73M01/R73C01: substring/role-inversion and denial-text forgeries; mutable local git attributes can change diff interpretation; the C2 loader defect; C1 fabricated receipt acceptance. These are limitations of structural counters. No counter is amended after scoring and no forge is substituted for an actual run.
- R73R01 F4/F5: the 1.79 s sizing observation exists in the session tool wall-time output but was not captured in the committed probe receipt; withdraw it as receipt-rederivable evidence. The sizing receipt omitted revision/digest at the probe moment. The decisive battery/preflight receipts do include both; the two completed-run epoch differences (80/92 s) are independently derivable there.
- R73R01 F6/F11: S180/S181 and wave artifacts were prospective at freeze, not then committed. They now land as round evidence; freeze wording overstates their already-landed status. F7: C1 predicate is semantically carried, not byte-identical: r73 names actual PASS/FAIL and G08 explicitly. F10: r71 landing is `e5458b35` (full ancestor derivable from the lane history); the original sizing assertion omitted that revision.

Process caveat: the swarm skill and remaining canonical protocol sections were loaded after dispatch rather than in the required order. No installs/updates occurred. Scribe R73S04 disclosed supplemental schema/count checks beyond its prose-only instruction. None is silently upgraded to outside verification.

## Self-evaluation

Accuracy 3/5: real PASS receipts, but invalid frozen C2 loader and withdrawn sizing provenance claim. Completeness 4/5: corrections and evidence delivered, claim admission intentionally fails rather than fabricating success. Clarity 4/5: verdict split and named counter limits. Actionability 4/5: explicit revisions/commands and real-loader red case. Conciseness 3/5: historical long-form artifacts remain. Average 3.6/5. Highest-impact improvement: a successor counter needs a real Git-backed positive and deletion control before freezing; this round does not claim that repair.
