# Round 76 — the answer key is salted; the correction counter stops being a presence test

Base: `1af39fed6058ad46fc075b72fddaae838f43273e`; prefreeze instruments and controls
`da9ac7ec684fe9fe9ad5554cab6180057255b76b`; claims freeze `5daa3628389c164f6ee34027be77d26b175c0de7`.
Two claims in `corpus/evidence/round76/claims.md`: C1 operability (lowest scored non-retired axis,
3/10, held) and C2 calibration. The r75 closure was admitted; this round answers
`corpus/lessons/round-75-verifier-spotcheck.md` routed defects 1–5.

## Gate

- Admit S187, own-work B, scoped to the r75 spot-check's routed defect 1 — the surviving metadata
  channels on the candidate-running matrix. `corpus/lessons/round-75-verifier-spotcheck.md` at
  `1af39fed6058ad46fc075b72fddaae838f43273e`, lines 124–128, quote on line 125. Opened
  2026-11-04. Located quote: "commit subject, tree ids and byte sizes are stable metadata channels, and four content-blind" (14 words). Grounds C1's target; it is the closure record, not independent truth of any counter.
- Admit S188, own-work B, scoped to routed defect 2 — the r75 correction counter as a presence
  test. Same revision and file, lines 129–131, quote on line 130. Opened 2026-11-04.
  Located quote: "polarity and magnitude rather than substring presence, require the correction block to be the final section" (16 words). Grounds C2's target.
- Reject S189, own-work C, scoped to this round's frozen claims file as a source row.
  `corpus/evidence/round76/claims.md` at `5daa3628389c164f6ee34027be77d26b175c0de7`, line 27.
  Opened 2026-11-04. Located quote: "`BATTERY=PASS forgers_rejected=11/11 positive=2/2`" (a code
  span, contiguous on that line). REJECTED: the claims file states the lane's
  own predicate; it is not evidence that the predicate holds — the committed receipts are — and a
  row here would let a later round cite its own declaration as a source. Flip: admit scoped to
  the claim text if an admitted knowledge entry ever rests on a declaration as the only record of
  a prediction.
- New registry rows S187/S188 mined, used-by this lesson; S189 rejected, used-by `—`. Existing
  status/recheck/used-by cells unchanged. No URL opened or fetched: all three are revision-pinned
  committed paths.
- Non-author spot-check requested: two admits and one reject above. Dispatched wave seats are
  author-lane evidence, not independent admission or promotion reviewers.
- Assimilation: none — no package bytes adopted, so no id-collision check is run.
  `considerthese/2026-10-26.md` was opened; no proposal was adopted this round (claim cap), which
  is recorded rather than implemented. No operator-authored consideration was edited.

## Mistakes

| class | evidence | captured-by | fix |
|---|---|---|---|
| a digest typed from memory into a frozen claims file | `corpus/evidence/round76/claims.md` as first written carried `ff56a1bf…` for `matrix-battery-v3.py`; the real blob digest is `217ae367c7e6e4ed23d1e6c1412de50370f309ba12d4a1703eaff386b7094360` (the battery prints `MATRIX_SHA256=` at every run and `sha256sum` reproduces it) | QUALITY 125 (a frozen claims file writes each digest as a 16-hex prefix that `sha256sum` reproduces) — applied only after writing, not before | every digest is now computed with `sha256sum` in the same command that writes the sentence; the claims file was corrected before its freeze commit (`5daa3628`), and the C2 counter digest was re-computed after the V3 polarity repair changed its bytes (`6ba8332f…` → `610e5655…`) |
| a piped receipt captured the pipe's exit code as the instrument's | `corpus/evidence/round76/controls/negative-r75-counter-on-v3.txt` first recorded `MATRIX_EXIT=0` for a matrix whose own last line was `LOADER_MATRIX=0/12 MATRIX=FAIL` (the `tail -3` in the pipeline returned 0) | the receipt was read against its own last line before commit, per the r72 "empty result trusted as negative" family | the receipt was re-run with the rc captured before any filter (`MATRIX_EXIT=1`); the corrected bytes are the committed control |

## Instrument limits (seat-discovered and frozen-byte limits; recorded, not amended after scoring)

- **Finite predicates reproduce, not general closure.** `R76Review` reproduces both after predicates and the full-default before controls from committed bytes. Both outer batteries nevertheless accept invocation-count oracles: C1 accepts the first four matrix calls, C2 accepts calls 1 and 8. These source-blind controls were discovered after the freeze, so they cannot repair its control chronology. Their saved sources and stdout are in `R76Review/`; no frozen byte is changed.
- **C1 metadata rationale is too broad.** `R76Sentinel` measures one subject, three orders, 36 distinct tree ids, but only 32 distinct size tuples across 36 observations: unchanged remains `(107,101,43,44,202)` in 3/3 runs. Fixed-width salts change hashes, not baseline sizes. `R76ExecC` restores named subjects or removes salts/padding and the frozen battery still passes; learned-table scratch forgers revive at 12/12 while the frozen tree-identity/size-map subjects stay 5/12. The subject-map only recognises the old r75 spelling. This is not a proof that metadata channels are closed.
- **C1 invocation/summary channels remain.** `R76Critic2` demonstrates a parent-matrix-keyed counter that scores 12/12 inside the matrix but gives constant PASS in deployment, and three contradictory-summary variants also score 12/12. The matrix uses `any()` for the summary and last-wins CHECK parsing. A correct 3.2-second child is rejected under the battery's 3-second bound but passes the default 20-second matrix: timeout rejection is not semantic discrimination.
- **Mutation sensitivity is incomplete.** `R76Mutation` observes `KILLED=6/15` (6/13 matrix mutants, 0/2 battery mutants against the pristine positive). Restoring v3 case-name subjects, dropping salt or padding, accepting child exit2, ignoring failed ids or the C2 summary survive. Its one-run flaky-order survivor is killed by the actual default two-run predicate; that distinction is retained.
- **C2 has nine observed survivor fixtures, not nine independent causes.** `R76Review2` retains 9/9 exit0 for duplicate authored S182 bullets, delete-then-restore history, a comment-hidden body beneath a visible heading, a fenced sample, bold `**161**` magnitude, an unrecognised negation, a base-already-corrected block, and an h1 after the final literal h2. Exact fixtures/check lines are in `counter-forgeries-blinded.txt`. Endpoint diff is not append-only history; prefix matching is not authored-bullet uniqueness. Both constant counters fail the C2 battery; no blanket-refusal gain is claimed.
- **Precision corrections to claims prose.** The frozen claims sentence saying every receipt names the controls revision is false: prefreeze receipts name worktree bytes through digests, not a future commit. `controls/freeze-remeasure-clone.txt` re-runs the committed freeze bytes but does not backdate them. The label-pair receipt is a positive/negative label-conformance pair, not the missing original r75 red-before battery run; r75 routed defect 5 remains carried. The C2 lane leg defaults to moving `master`; reviewer observed no divergence, but a clean detached checkout alone does not pin it. The first local Gate draft also cited the work tip before its verifier file existed and miscounted the quoted spans; `R76Scribe` caught both before this lesson landed.

## Spot-check intake

| r75 routed defect | disposition |
|---|---|
| 1 metadata channels and untested twelve-order oracle | bounded subject-map/oracle improvement; metadata claims narrowed above; adaptive memo and unchanged-size gaps carried to QUALITY138 |
| 2 presence-test correction counter | six frozen bogus fixtures reject; new duplicate-id/rendering/history survivors carried to QUALITY140 |
| 3 controls/freeze chronology | controls commit da9ac7ec precedes claims freeze 5daa3628; post-freeze shortcut findings remain findings, never prefreeze controls |
| 4 receipt precision | prefreeze worktree-plus-digest evidence explicitly labelled above; committed-freeze rerun retained |
| 5 actual parser-slip red-before | carried: label-pair control does not reconstruct the overwritten historical red-before receipt |

## Boundaries

R71–r75 rejection rulings stay unchanged; no historical landing is retroactively admitted. The
historical operability score stays 3/10 and no capability row is pre-claimed. No Windows-host
flock/load question is treated as answered; the r73 Linux battery/preflight completion is not
re-claimed. External-fetch approval, SHONEN promotion and non-author entailment review remain
operator-owned and unanswered; this round needs none of them. No cross-domain source absorbed;
`PROVINCE.md` unchanged.

## Wave integration and verdict

WAVE-DONE from Main received before filing: `.ufo/waves/round-76/w1-results.json` records 12 seats. One v1 wave, 3 executor, scout, scribe, connector, 2 reviewer, 2 critic, mutation-tester and sentinel; six attack roles (50%), L1 canonical planner, no residual call. Eleven seat reports are retained. R76Critic's report is absent; a wake returned 402 “Insufficient account funds”. Results entries contain null output and no per-seat terminal status/id after orchestrator restart, so “all settled” is the orchestrator's attestation, not twelve independently preserved successful results. No seat was replaced or provider route changed.

R76ExecA and R76Review reproduce C1 before9/11 and after11/11 with both positives accepted; R76Review uses the full default before command. R76ExecB independently derives the twelve expected result/check sets and observes differing orders/base trees. R76ExecC isolates the missing sensitivity of subject/salt closures; R76Sentinel measures unchanged-size leakage. R76Review2 retains nine C2 survivor fixtures; R76Critic2 exposes parent-keyed and contradictory-summary survivors. R76Mutation retains the 6/15 kill table and restoration receipts. R76Scout/Connect route remaining channels and sibling precedents; none of those sibling gates was executed. R76Scribe verifies the Gate/census and catches source-anchor/count errors before landing.

Both frozen finite predicates hold at the controls/claims bytes, including a clean-clone L1 remeasurement. This is not certification that metadata or bogus-correction classes are closed. Admission is withheld for independent closure: the outer no-reader controls were absent before freeze and C2's instrument-discrimination improvement does not itself count SCORECARD/SHONEN mismatches. Historical numeric score stays 3/10; no capability added. Expansion unchanged; quality improved narrowly; discernment improved through lesson-backed QUALITY138–140. No outside promotion or admit/reject judgment is self-granted.

## Self-evaluation

Accuracy4/5: frozen measurements reproduce, but broad rationale and receipt prose needed explicit corrections. Completeness3/5: real instruments/controls, curation and wave evidence land, yet one seat's terminal evidence is missing and declared calibration axis-fit remains unresolved. Clarity4/5: finite predicates and admission separated. Actionability4/5: saved probes define successor controls without rewriting this freeze. Conciseness3/5: large duplicated evidence/prose corpus. Overall3.6/5; improve claim-axis fit and prefreeze shortcut discrimination before another declaration.
