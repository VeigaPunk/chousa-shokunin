# ConnectScope — round 64 attempt 2

Advisory only. Lane: `/home/vgpnk/Projects/shokunin/chousa-shokunin`. Only L1 integrates. No production edits, admission decisions, runtime invocation, or independent closure verdict.

## Axes

Declared axes are **operability** (C1), **calibration** (C2), and **depth** (C3); frozen `corpus/evidence/round64/claims.md:23-26,106-109,184-187`. No numeric score or aggregate is proposed.

## One bounded move: a claim-to-evidence provenance crosswalk

[PROPOSAL] L1 should append one round-local closure table distinguishing **frozen predicate evidence**, **post-freeze supplemental evidence**, and **candidate-only observations**, with an explicit own-corpus gate and scope boundary for each row. Each row carries claim/anchor, instrument path+digest, measured target path+digest and production/candidate status, command/cwd/exit, stdout/stderr receipt pointers, and the precise proposition supported or contradicted. This is an application of existing source-verification rules, not a new generic testing framework or a replacement judgment system.

The non-obvious connection: an honest repaired fixture is a *new source* for the technical proposition, not a new meaning for the old source. Use the lane's existing four support states to prevent a supplemental PASS, candidate probe, or mere file existence from becoming frozen-claim closure. The crosswalk preserves both the failed instrument and useful repaired evidence without forcing either to impersonate the other.

## Evidence and gate mapping

| Claim | Own-corpus surface | Scope and required separation |
|---|---|---|
| C1 | `SKILL.md:154` lane-preflight G02; G01 registry census; G04/G05 evidence pointers. Frozen battery and full preflight remain separate receipts (`claims.md:78-93,102`). | G02 normalization, recursive file-kind/symlink handling and UTF-8 reporting are this lane's own corpus gate. G02 success is not research truth; a battery omitting G08 is not a full eight-gate run. Candidate `controls/ref-preflight-v3.py` is not production `tools/lane-preflight.py`. |
| C2 | `SKILL.md:155` claims-audit plus round64 v2 mutation runner and selftest (`claims.md:116-174`). | Anchors and audit results support calibration of this lane's frozen statements. A ten-case selftest alone is not the twelve-mutant closure. Preserve exact output streams as evidence. Generic mutation-testing craft is contested adjacent scope, not acquired here. |
| C3 | `SKILL.md:69-75,89` claim revision binding, inference grounding, source metadata and quote checking; `claims.md:194-239` named instruments and sourced Gate rows. | Separate relocation behavior from source admission. A source opening or a file existing does not establish the technical proposition. Complete relocated trees are expressly allowed; existence asserts are not containment or filesystem identity proof. |

Admission constraints already exist: `corpus/QUALITY.md:3-7` measured anchors, observation/inference separation, append-only errata and retained rejections; `:17-37` source metadata, scoped tiers, four support states and one home per finding. `SKILL.md:20-23` distinguishes source support from truth. The crosswalk reuses those constraints; no new corpus gate is claimed to enforce semantic entailment.

### Explicit contradictions, not averaged away

1. **Frozen C1 fixture mismatch:** frozen `c1-battery-v3.py:386-394` independently calls `tag()` for the new filename and README target in both E12 and E13. Supplement `c1-battery-supplement.py:386-396` instead binds one `t` per fixture. The assignment reports frozen C1 failure; that failure remains the frozen result, not repaired by a supplemental PASS. This seat did not rerun it. The frozen kill rule still requires the unmodified battery on production at landing three times (`claims.md:89-93`).
2. **Supplement identity versus copied wording:** although separately named, the supplement docstring still says “the round-64 claim” and “the same sentence” (`:2-6`); its opening summary says 28 defects/43 legs (`:20`), while another summary says 29/44 (`:56-59`). These are conflicting textual descriptions, not measured counts from this seat. The crosswalk must identify the supplement by path and digest, not adopt its copied claim label. No frozen or inherited file was edited.
3. **Cached probe narrative contradiction:** `w1/G02Probe09.md:4` calls candidate acceptance a “mismatch” but then explicitly says that same PASS is consistent with the frozen benign target. Its actual fixture/output (`:7-14`) supports only isolated candidate acceptance. Preserve that observation without importing the contradictory characterization or treating it as production acceptance.
4. **C2 stream contradiction:** frozen `claims.md:136` requires the fault leg's `FAULT` on stdout. Cached `w1/Counter04/report.md:5` reports exit 1 with `FAULT` on stderr and no stdout. This is secondary seat evidence, not independently reproduced here; it must remain visible for L1's exact-contract review, not be flattened to “fault leg passed.”

## Province boundaries read

- Chousa `PROVINCE.md:3-15`: owns research method and its own corpus/gates; refuses orchestration, dispatch and lifecycle.
- Tameshi `PROVINCE.md:3-17,44-47`: owns reusable honest-check/mutation craft; each product gate remains its lane's. Its general pattern admission requires evidence from two independent lanes. Thus C1/C2 can improve chousa's instruments, but cannot establish a generic testing-method claim here. Contested generic testing scope stays explicit; no sibling work is absorbed.
- Kumitate `PROVINCE.md:3-6,19-24`: owns orchestration/tooling, task/hub contracts and isolation substrates. Copying a golden fixture or using random paths does not grant chousa ownership of runtime isolation, dispatch or lifecycle policy.
- Souji `PROVINCE.md:3-17,32-46,71-83`: owns receipt-gated hygiene and studies filesystem removal semantics; live work products are refused. G02 symlink classification is not deletion authority, quarantine certification or a sibling cleanup contract.
- Tsukuroi `PROVINCE.md:3-28`: owns OS/package/systemd substrate diagnosis; rollback/filesystem health is detection-only. Permission failure in a G02 fixture does not authorize package transactions, service restarts or host repair.

## Second-order effects and risks

- **Runtime:** documentation-only crosswalk adds no execution, allocations, subprocesses or production latency. It must not trigger duplicate heavy batteries or another dispatch runtime.
- **Contract:** exact frozen predicates, streams and targets stay immutable. Risk: a table labelled generically “C1 PASS” could become a new laundering surface; prohibit claim-status inheritance from supplemental/candidate rows.
- **Substrate:** file-kind rules and root-existence assertions remain narrow observations, not symlink confinement, race safety, workspace containment or cleanup permission. Captured cwd and target digest prevent candidate/production and fleet/lane conflation; they do not themselves prove runtime containment.
- **Verification:** retain raw receipts and failed observations; classify their relationship to the claim separately. Risk: stale paths or copied summaries still need a reader—existing gates check structure and some tokens, not full entailment.

[INFERENCE] Calibration and operability improve through less ambiguous closure evidence; depth is preserved through exact scope/source anchors. No harm to another declared axis is expected **provided** this remains an append-only, round-local interpretation aid, not a changed predicate, new claim, forced sibling adoption or replacement for required measurements. This is a proposed benefit, not an exercised improvement.

## Verification handoff (not run)

L1 can inspect the table against existing receipts: each frozen row names the frozen instrument, production target and exact stream/exit obligations; each supplement/candidate row explicitly cannot satisfy the frozen kill rule. Test the interpretation with E12/E13, G02Probe09 and Counter04: none may silently promote to a frozen production PASS. Keep C3 relocation and sourced admission separate. Run only the original counting commands and gates required by the canonical closure assignment, in authorized scratch, with exact receipts; this proposal requests no new probes or rule changes.

## Work and evidence record

No bounded runtime probe was required by this connector item, and none was run. No tests, builds, linters, checks of this report, installs, updates, network fetches, clone creation, git/jj mutations or sibling edits. Scratch was never created, so no scratch tree or live clone remains to remove.

Read-only command executed from the absolute lane root: `sha256sum` on the following eight absolute paths; exit **0**. Output (paths shortened only by the common `/home/vgpnk/Projects/shokunin/` prefix):

```text
bab186919f4518f3662c31661d1e2060b4f9f3d186b33d184c365a3f82d7cfc0  chousa-shokunin/corpus/evidence/round64/claims.md
4b3f0b658bcd3bb640cd2e6e56a28a91a72d5352f2610887db01e636fc039fe2  chousa-shokunin/corpus/evidence/round64/c1-battery-v3.py
a7057ae33ac958f060a25ea325537bec7bed728e7ea2dad3f3a961e715fc33f1  chousa-shokunin/corpus/evidence/round64/c1-battery-supplement.py
cf7826a43aaab7c00708ab54bb46577217e7a67ab44a43a33e17ee2a58c1bbec  chousa-shokunin/PROVINCE.md
b2875fe21f381d98551d5a4946af4fb547ceb6244ce6bef35885dbdf034c28be  tameshi-shokunin/PROVINCE.md
b20bd05ffd41002806b05bc5e49a53301671d580a87ffd2e15b3c093a2196fdc  kumitate-shokunin/PROVINCE.md
bb443de4c484f53094070366b965fa6ee9e1ce274d9b45293d99109f1e74680e  souji-shokunin/PROVINCE.md
177cd834a0d9a63375979c21fbf143d5fa588987f45cfdac07a44a35a895e1cd  tsukuroi-shokunin/PROVINCE.md
```

Claims freeze revision `bf40d99bda9eefdad3ed6276da077cfb24ba82f1` is assignment-provided; this seat pins the bytes actually read above rather than claiming a separate revision comparison.
