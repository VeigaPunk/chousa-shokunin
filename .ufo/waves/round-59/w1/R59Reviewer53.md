# R59Reviewer53 — calibration review

## Findings

### Blocker — round 59 has no frozen predicates; positive calibration is not attributable to this round

The required `corpus/evidence/round59/claims.md` is absent (direct read returned “Path not found”; `glob` of `corpus/evidence/round59/` shows evidence/receipts but no claims file). Yet the persisted wave contract explicitly requires that file before work (`.ufo/waves/round-59/w1-spec.json:10,429-434`), and the ready markers exist (`.ufo/waves/round-59/w1.ready`, `w1.ready.dispatched`). The round-59 lesson independently states “claims: none validly frozen” and no round-59 axis claim or score delta (`corpus/lessons/round-59.md:4,10-12`). That is a sound stop on post-hoc claim invention, but it means the milestone's positive verdict-path calibration cannot be evidence of a round-59 frozen claim or score improvement. This is a control/claim design gap, not proof the source research is wrong.

**Falsifier:** an immutable pre-dispatch claim artifact with its freeze identity/digest and a dispatch binding that proves this is the input used. A later-created file cannot establish pre-dispatch freeze; absent that evidence, keep round-59 claims unscored.

### High — available positive-path probes demonstrate the inherited C1 oracle is unsound, not merely unreachable

Round-59 has no C1 after receipt or own counter (`corpus/evidence/round59/` listing); available dynamic probes concern the explicitly inherited round-58 C1 counter. The precise observations are strong but must remain attributed to that counter: `R59MutationTester64.md:30-38` reports that a pristine builder passes all 11 per-leg checks and a foreign-deletion mutant differs on the FOREIGN leg, yet both receive `C1=FAIL` because the aggregate checks uppercase `=PASS` while emitters use lowercase `pass`. More importantly, `R59Executor09.md:86-98,215-260` corrects the too-broad “unreachable for every builder” claim: arbitrary candidate stderr is interpolated into failure-leg text and substring-matched, allowing a builder that fails every refusal check (including writing through symlinked output) to obtain `C1=PASS`, exit 0. The same report shows a scratch-only case-fixed oracle credits a symlink-escaping builder (`:130-161`), and a denial control can crash before scoring (`:194-213`). Therefore a positive output token alone is not a valid calibration criterion; inspect typed per-leg outcomes, containment side effects, and process/control errors. Do not apply these counter-specific results as a finding against an absent round-59 counter or claim.

**Falsifier:** for the actual round-59 frozen counter, show a digest-bound receipt from an independent compliant candidate yielding the exact frozen positive predicate and from targeted mutants/forgeries being rejected; oracle must derive verdict from structured results not candidate-controlled prose and must treat side effects/crashes as explicit failures. No such round-59 package is present, so it cannot presently falsify the finding that round-59 calibration is unproven.

## Residual risk and verification gaps

Source-grounding/scope judgment is limited: `corpus/lessons/round-59.md:10,17-18` records an offline reopen of S101, no live fetch due to unresolved L0 question `8d77e6c1`, no admitted source row, and the full live-source check remaining partial/unverifiable. I did not infer current-origin facts from the local capture. No external fetch, source/counter mutation, controls run, or installation was performed. Read-only review only; tooling rules were read. No positive round-59 predicate/receipt exists to test. The prior report's claims about an exhaustive absence from all lane artifacts were too broad; this assessment relies on current directory listings and the round-59 lesson, and distinguishes inherited round-58 probe results from round-59 evidence.

Report: .ufo/waves/round-59/w1/R59Reviewer53.md
