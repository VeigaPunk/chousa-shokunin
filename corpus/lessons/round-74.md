# Round 74 — actual-loader controls before successor evidence

Base: 8a28732b3c1591b52449a982849b758cda6f4c45; freeze: 1eaa30ad248bbd3bd7469b2c17295fcda5fc02bb.
Claim C1 operability only, predicate and kill rule in `corpus/evidence/round74/claims.md`. Lowest measured axis remains operability; the historical 3/10 score is not generalized or changed.

## Gate

- Admit S182, own-work B scoped to the routed loader defect: `corpus/lessons/round-73-verifier-spotcheck.md` at 8a28732b3c1591b52449a982849b758cda6f4c45, section 5 item 1. Opened 2026-11-04. Located quote: “Before any successor calibration freeze, exercise a real committed append and a real deletion through `load()`” (18 words). This directs the successor controls; not independent truth of arbitrary correction prose.
- Reject S183, own-work C scoped to helper-only selftest as loader certification: `corpus/evidence/round73/c2-count.py` at the same base, lines 162–179. Opened 2026-11-04. Located quote: `base = check({k: v for k, v in FIXTURE.items()}, {}, set())` (line 163, 13 whitespace tokens). This calls check directly, not load; the loader at lines 125–134 mislabels additions as removals. Flip: actual public CLI over committed append/deletion cases passes independently expected outcomes. Do not erase the rejected historical evidence when the successor meets that flip.
- New registry rows: S182 mined, used-by this lesson; S183 rejected, used-by —. Existing status/recheck/used-by cells unchanged. No external URL opened or fetched: both sources are revision-pinned own-work repo paths.
- Non-author spot-check requested: one admit and one reject above. Dispatched wave seats are still author-lane evidence, not independent admission or promotion reviewers.
- Assimilation: none. No package bytes adopted. Latest `considerthese/2026-10-26.md` was opened; no new proposal implemented independently of this claim. No operator-authored consideration edited.

## Mistakes

| class | evidence | captured-by | fix |
|---|---|---|---|
| helper-only test bypasses a defective input adapter | r73 closure section 5 item 1 (S182); frozen r73 load line 131 and selftest line 163 (S183) | prior selftest omitted loader; Gate standard public-invocation rule | successor reads numstat deletion column 1; nine real-commit CLI cases. Old counter 3/9 exit 1 versus prefreeze positive 9/9 exit 0, `corpus/evidence/round74/before-matrix.txt` and `positive-matrix.txt`; QUALITY 134 records prevention |

## Boundaries

Historical r71/r72/r73 rejection rulings stay unchanged. R73 battery/preflight completion is not repeated as a gain. Correction checks still use substring statements and cannot prove entailment or adversarial unforgeability. Old Windows flock/load questions, external-fetch approval, SHONEN review and non-author entailment review remain unanswered; this round needs none of them. No cross-domain source absorbed; PROVINCE unchanged.

## Wave integration and verdict

WAVE-DONE received from Main for w1; `.ufo/waves/round-74/w1-results.json` holds 10 settled outputs: 3 executor, 1 scribe, 1 scout, 1 connector, 2 reviewer, 1 critic, 1 mutation-tester. Four attack seats (40%); L1 canonical planner; no residual or dead seat reported.

At frozen instrument revision 1eaa30ad248bbd3bd7469b2c17295fcda5fc02bb the L1 measured both conjuncts after settlement: `after-matrix.txt` 9/9 exit 0 and `after-historical.txt` C2=PASS checks=7/7 exit 0. Original on the same historical landing is 6/7 exit 1 (`before-historical.txt`). Successor SHA256 9334721a5e7a4080255b478771bf5443739738fb1936b40c116da28d7fa8ac41 matches its frozen committed blob and the matrix receipt. C1 operability improves narrowly on its unchanged predicate; this is not a C2 calibration claim.

Advisory results integrated:
- R74ExecA/B reproduce both conjuncts and the old failure. R74ExecC independent mixed-file/equal-line probes match 7/7 expected outcomes. R74Mutation reversion scores 3/9, force-zero-deletions 5/9 (both killed). Their sources/receipts land in the wave folder.
- R74Critic constants score 4/9, 4/9 and 1/9, but its invocation-order oracle reaches 9/9 without reading input. This is a real surviving forge, not closed by a digest: a digest identifies which implementation was run; it does not make the matrix discriminate that forge. The actual successor was source-reviewed and its digest bound, but general counter robustness remains false.
- R74ReviewFreeze identifies prefreeze criterion 126 noncompliance: no detection-forger battery was committed before scoring. This is an admission-relevant procedural gap. No post-data test repairs that freeze, and the frozen predicate is not amended. **Round admission withheld / not admitted under the current quality bar**, despite the narrow measured C1 improvement; canonical non-author closure rules.
- Nonnumeric/binary fallback is outside the nine text cases; reviewer demonstrates fail-closed binary handling with an inherited invalid-UTF8 traceback limit. No universal loader or semantic-correctness claim.

| class | evidence | captured-by | fix / disposition |
|---|---|---|---|
| required prefreeze attack battery omitted; deterministic order forge survives | `.ufo/waves/round-74/w1/R74ReviewFreeze.md` finding 1; `R74Critic.md` F4 and `R74Critic/forge-order-oracle.log` | existing QUALITY 120 and 126 | disclose surviving forge and freeze noncompliance; do not certify matrix adversarial robustness or admit this round. A future successor must demonstrate rejection before freeze; this round claims no fix to that defect |

Trends: expansion unchanged (no knowledge or capability added); quality improved narrowly (known numeric-column bug repaired, surviving matrix weakness explicitly marked); discernment improved in the lesson-backed-criterion sense (r73 disagreement becomes QUALITY 134), pending outside admit/reject spot-check. Other axes unchanged; historical score delta 0.
