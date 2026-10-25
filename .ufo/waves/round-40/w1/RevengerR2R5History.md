# RevengerR2R5History — R2–R5 reconstruction and classification (round 40, w1)

- seat: RevengerR2R5History (leaf L2, revenger; no dispatch, no production edits)
- date: 2026-10-24
- lane root: /home/vgpnk/Projects/shokunin/chousa-shokunin (all pointers below resolve from this root unless prefixed `fleet:` = /home/vgpnk/Projects/shokunin)
- assigned attack: reconstruct R2–R5 from the spot-check, r39 lesson, r39 report, SCORECARD, spec, and plan; classify each finding true / fixed / contradicted using resolvable pointers
- scope boundary: R1 (receipt-integrity predicate) is RevengerR1History's seat; not attacked here. C1 receipts were not re-verified here.

## Axes (godspeed)

- operability — every classification is backed by a command anyone can re-run from this report.
- calibration — each of R2–R5 gets a source-checked disposition against committed bytes, not prose labels.
- depth — the R4 contrary numbers are traced to a concrete, independently verified counting mechanism; the R2 "six vs seven" contradiction is tied to receipt digests.

## Method

Read-only reconstruction over committed artifacts: r39 verifier spot-check, r39 lesson, fleet r39 report, SCORECARD, r39 `w1-spec.json`/`w1-plan.json` (plus the r40 and r33 specs for provenance), `corpus/evidence/round39/claims.md`, the round-40 disposition record, and the frozen `c2-count.py`. No file under lane production surfaces was modified; the only write is this report.

### Exact commands and outputs

1. Role/agent mixes (spec vs plan, r39), full mixes derived with `collections.Counter` over `items[].role` / `tasks[].agent`:

   ```
   spec roles:  {'executor': 6, 'reviewer': 6, 'critic': 5, 'scout': 3, 'scribe': 3,
                 'mutation-tester': 3, 'sentinel': 2, 'revenger': 2, 'connector': 1, 'simplifier': 1}
   plan agents: {'executor': 6, 'reviewer': 6, 'critic': 5, 'scout': 3, 'scribe': 3,
                 'mutation-tester': 3, 'sentinel': 2, 'revenger': 2, 'connector': 1, 'simplifier': 1}
   spec items: 32, plan tasks: 32
   ```

2. R2 existence/tracking, R3 counts, committed digests:

   ```
   $ ls corpus/evidence/round39/receipts/*.json | wc -l          → 7
   $ git ls-files --error-unmatch corpus/evidence/round39/receipts/c1-mutenv-s39003.json
     → corpus/evidence/round39/receipts/c1-mutenv-s39003.json  TRACKED
   $ for r in 8c7c867b66e103712ae33e1d076786f50dd3239e 6ac1007e6a5d699d0742801026554fac1d900b5d; do
       printf '%s ' "$r"; git ls-tree -r --name-only "$r" -- corpus/knowledge | awk '/\.md$/ {n++} END {print n+0}'
     done
     → 8c7c867b… 50 ; 6ac1007e6… 52
   $ sha256sum tools/research-gate.sh corpus/evidence/round39/c1-count.py
     → 4253c18738f84df9200cbc93f8e077ba63a418c5ee822c1324e1a8d75a9b07e3  tools/research-gate.sh
     → 91618e91640f748df76282244186088218d5f2b7a65364137fa6add29fea05d5  corpus/evidence/round39/c1-count.py
   ```

3. `w1-spec.json` history (single committed revision):

   ```
   $ git log --format=%h -- .ufo/waves/round-39/w1-spec.json → 6d914e9 (only revision)
     role mix at 6d914e9: reviewer 6 / revenger 2 (mix above), 32 seats
   ```

4. R4 provenance probes:

   ```
   $ python3 corpus/evidence/round40/c2-count.py
     R2_DISPOSITION=ok
     R3_DISPOSITION=ok
     R4_DISPOSITION=ok
     R5_DISPOSITION=ok
     R39_CALIBRATION_DISPOSITIONS=4/4   (exit 0)
   $ round-40 w1-spec.json roles → reviewer 6 / revenger 2, total 33 (history: 6c01a41, d164f88)
   $ round-40 w1-plan.json agents → identical mix, total 33
   $ round-33 w2-spec.json roles → {'executor': 15, 'reviewer': 8, 'mutation-tester': 5,
                                    'sentinel': 1, 'critic': 2, 'scout': 3}, total 34 (no revenger field)
   $ r39 spec seat-name prefixes → Rev*: 8, Review*: 0, Revenger*: 0
   ```

## Per-finding reconstruction

### R2 — committed superseded draft receipt → finding TRUE, now FIXED (`corrected`)

- Origin: `corpus/lessons/round-39-verifier-spotcheck.md:72` — `c1-mutenv-s39003.json` committed although the lesson records it "not committed"; report/LOG say "receipts (6)" while seven files are committed.
- Ground truth (all re-derived): the receipt exists and is git-tracked (command 2); the receipts directory holds **7** JSON files; the r39 lesson's own `## Mistakes` row records it "superseded, not committed" (`corpus/lessons/round-39.md:27`) and the `## Gate` receipts paragraph counts "six committed" (`corpus/lessons/round-39.md:55-66`). The contradiction is real → **TRUE**.
- Digest corroboration: the receipt binds `gate_sha256 89022659…` (= the lesson:28 "EDITED working tree (post-pin)" bytes, which were never committed; the committed gate is `4253c187…`, base control `0447ad14…`), `counter_sha256 1c3b2a9e…` (≠ committed counter `91618e91…`), and `expect_sha256 3abd2dcb…` (the stale R1 digest class). It is a superseded draft binding uncommitted bytes, exactly as dispositioned.
- Fix verified: `corpus/evidence/round39/claims.md:197` erratum (append-only) names it superseded and excludes it from the active set; `corpus/evidence/round40/active-r39-receipts.tsv` has exactly 6 rows and does not list s39003; `SCORECARD.md:2257` records the correction. `LOG.md:1453` retains the historical "receipts (6)" wording — LOG is the append-only journal, the correction of record is the claims erratum + SCORECARD row.
- Classification: **TRUE, FIXED** — disposition `corrected` (`corpus/evidence/round40/routed-defect-dispositions.json` R2) matches the artifacts.

### R3 — knowledge-count misstatement → finding TRUE, now FIXED (`corrected`)

- Origin: `corpus/lessons/round-39-verifier-spotcheck.md:73`; the r39 report states "`ls corpus/knowledge/*.md | wc -l` 29 → 31" (`fleet:.ufo/reports/round-39/chousa.md:132-133`).
- Ground truth: `git ls-tree -r --name-only` over `corpus/knowledge` gives **50** at the r39 base `8c7c867b…` and **52** at the r39 tip `6ac1007e6…` (command 2). The report's absolute counts (29 → 31) are wrong; only the +2 delta is right → **TRUE**.
- Fix verified: `corpus/evidence/round39/claims.md:198` erratum records 50 → 52 with a re-runnable command; `SCORECARD.md:2258` supersedes the report wording; the frozen counter re-derives both counts itself (`c2-count.py` `md_count(BASE39/TIP39) == (50, 52)`; live run: `R3_DISPOSITION=ok`).
- Classification: **TRUE, FIXED** — disposition `corrected` matches.

### R4 — wave role-mix mismatch → finding CONTRADICTED, not reproduced (`not-reproduced`)

- Origin: `corpus/lessons/round-39-verifier-spotcheck.md:74` — "the validated spec (`w1-spec.json`: reviewer 8 / revenger 0; totals 32 both)".
- Ground truth (three independent authorities, all re-derived):
  1. committed `w1-spec.json` `items[].role` → reviewer **6**, revenger **2**, 32 seats (command 1); single committed revision (`6d914e9`, command 3);
  2. generated `w1-plan.json` `tasks[].agent` → identical mix, 32 seats;
  3. the r39 report's own role-mix prose (`fleet:.ufo/reports/round-39/chousa.md:168-170`) → executor 6 / reviewer 6 / critic 5 / scout 3 / scribe 3 / mutation-tester 3 / sentinel 2 / **revenger 2** / connector 1 / simplifier 1.
  The spot-check's reviewer **8** / revenger **0** matches **no** committed revision of any r39 artifact → the finding is **CONTRADICTED**.
- Provenance of the wrong numbers (independently verified mechanism): the r39 spec contains exactly **8 seat names starting with `Rev`** (six reviewer seats + two revenger seats) and **0 names starting with `Revenger`** (command 4). Counting seat-name prefixes instead of the `role` field reproduces "reviewer 8 / revenger 0" while keeping totals 32. That a spot-check author made this slip is [INFERENCE]; the 8/0-by-prefix numbers themselves are verified facts. (Sibling corroboration, not my basis: `.ufo/waves/round-40/w1/CriticR4Disposition.md:60-72` reaches the same mechanism; its full-lane sweep found the only reviewer-8 spec anywhere is `round-33/w2-spec.json` — reviewer 8, 34 seats, no revenger field, wrong round/total — which I re-derived independently, command 4.)
- Excluded alternatives: the round-40 spec (33 seats) carries reviewer 6 / revenger 2 as well, so it is not the source of 8/0 either — the claims erratum's "Round 40's … 33-seat spec is not part of the r39 comparison" (`corpus/evidence/round39/claims.md:199`) is correct scoping. Any pre-commit working-tree state is unreconstructible from committed bytes.
- Disposition check: `not-reproduced` with the conflict preserved, no source rewritten (`corpus/evidence/round40/routed-defect-dispositions.json` R4; `SCORECARD.md:2259`; `corpus/lessons/round-40-verifier-spotcheck.md:28` re-derives it independently). The frozen counter requires exact role-count agreement among spec/plan/report **and** keeps the spot-check's contrary statement cited — all hold live (`R4_DISPOSITION=ok`).
- Classification: **CONTRADICTED, not-reproduced** — the only correct status; changing it to "fixed" would invent a spec correction that no evidence supports.

### R5 — "two independent runners" wording → finding TRUE, now FIXED (`corrected`)

- Origin: `corpus/lessons/round-39-verifier-spotcheck.md:75`; the phrase sits in the r39 operability row at `SCORECARD.md:2234` ("7/8 → 8/8 across two seeds, two independent runners").
- Ground truth: the r39 frozen claims disclose that both cited C1 runs were **the L1's construction runs** on seeds 39001/39011 (C1) and 39101 (C2), preceding the freeze (`corpus/evidence/round39/claims.md:3-5`), and the r39 report records "**0 dispatched** / 0 dead this seat" (`fleet:.ufo/reports/round-39/chousa.md:171`). Two construction seeds are not "two independent runners" → **TRUE**.
- Fix verified, append-only: `SCORECARD.md:2255-2260` adds "## Round 40 — closure corrections to r39 (R2–R5)" superseding the phrase with "two seeds, both L1 construction runs" while the original row at `:2234` is retained unedited; `corpus/evidence/round39/claims.md:200` records the same correction. The frozen counter requires both the historical phrase and the corrected wording to be present (anti-rewrite check) — holds live (`R5_DISPOSITION=ok`).
- Classification: **TRUE, FIXED** — disposition `corrected` matches.

## Verdict

| Finding | Spot-check claim | Committed ground truth | Classification | Disposition status |
|---|---|---|---|---|
| R2 | receipt committed despite "not committed"; 7 files vs "receipts (6)" | confirmed (tracked file, 7 JSONs, digests bind uncommitted bytes) | TRUE → FIXED | `corrected` ✓ |
| R3 | report's `29 → 31` wrong; real 50 → 52 | confirmed (git ls-tree 50/52 at the named commits) | TRUE → FIXED | `corrected` ✓ |
| R4 | spec was reviewer 8 / revenger 0 | spec/plan/report all reviewer 6 / revenger 2; 8/0 matches no committed artifact | CONTRADICTED → NOT-REPRODUCED | `not-reproduced` ✓ |
| R5 | "two independent runners" unsupported | confirmed (freeze discloses L1 construction runs; 0 dispatched) | TRUE → FIXED | `corrected` ✓ |

Frozen counter cross-check: `python3 corpus/evidence/round40/c2-count.py` → `R39_CALIBRATION_DISPOSITIONS=4/4`, exit 0 (output above). The counter re-derives R3's tree counts and R4's role histograms from committed bytes and would refuse a prose-only relabel — consistent with the frozen P2 and the kill rules in `corpus/evidence/round40/claims.md` (C2). Separability held: the C2 counter read no receipts.

Resolvable anchor set: spot-check `corpus/lessons/round-39-verifier-spotcheck.md:72-75`; r39 lesson `corpus/lessons/round-39.md:27-28,55-66`; r39 report `fleet:.ufo/reports/round-39/chousa.md:132-133,168-170`; SCORECARD `SCORECARD.md:2234,2255-2260`; r39 claims `corpus/evidence/round39/claims.md:3-5,195-200`; dispositions `corpus/evidence/round40/routed-defect-dispositions.json`; counter `corpus/evidence/round40/c2-count.py`.

Confidence: high on all four classifications — every load-bearing number above was re-derived from committed bytes this seat, not taken from the disposition record. The only inferential step is the causal claim for how the r39 spot-check arrived at 8/0 (prefix-vs-role counting), marked [INFERENCE]; the mechanism's numbers are verified facts and no committed artifact carries 8/0.

Divergences: none with the disposition record or the r40 closure spot-check. One calibration observation: `LOG.md:1453`'s historical "receipts (6)" stands uncorrected in the journal (by append-only design); the correction of record is `corpus/evidence/round39/claims.md:197` + `SCORECARD.md:2257`.

Tooling record: no tools installed or updated (pacman pause honored; git/coreutils/python3 sufficed).
