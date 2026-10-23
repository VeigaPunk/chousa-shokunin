# CriticClaim33 — C1 verdict and §9 shape

## Scope, axes and result

**Pinned revision:** `0fb300b5c27900ab8bb3abeb5f54776d71e04beb`. Read `corpus/evidence/round33/claims.md` first, including governing Design v2. This is a reasoning-only review of committed evidence, not a canonical judgment, admission or implementation review approval.

**Axes:** operability is the claimed axis; depth, coverage, freshness, calibration and adjacency are the other five axes. Predicate/provenance criticism is a review lens, not a second claimed axis. Canonical definitions: `/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/AXES.md:9-16`. No no-harm verdict on those other axes is inferred from this review.

**Scoped verdict: HOLDS for the bounded §9 shape, with two qualifications.** The numerical predicate, pre-candidate freeze, non-oracle controls and operability fit withstand the attacks below. An individual `predicate_holds=true` does **not** establish the entire P1 v2 sentence; the all-runs kill condition remains an external evidence obligation. Also, the broader malformed-input refusal assertion has a direct **[INFERENCE] static counterexample** outside the frozen counter's generated set. Neither qualification is a measured below-156 run. I do not issue the global C1 verdict.

All paths below are lane-relative unless absolute. Command evidence, exact commands, exit codes and key output: `.ufo/waves/round-33/w2/CriticClaim33/evidence.txt` (commands 1–10, each exit 0). No gate, counter, selftest, mutant, judge or other evaluation runtime was run by this seat; consequently this seat has no C1 scoring receipt to omit.

## 1. Same sentence, condition and label — yes numerically, not self-aggregating

| Attack | Evidence | Finding |
|---|---|---|
| Different prose predicate in plan and counter | `claims.md:120-125`; `c1-count-v2.py:4-8` | Same sentence after Markdown/line-wrap removal: the named v2 counter must print 156/156 on two fresh seeds on the landed revision, with no lower run on that revision during round 33. |
| Different denominator or success condition | `c1-count-v2.py:82-101,384-405,427`; `claims.md:125` | Fixed class sizes sum to 156, asserted in code; per-run success is exactly `holds = matched == TOTAL`, and process success uses that boolean. |
| Different receipt label or provenance | `c1-count-v2.py:410-418`; `measure/integrated/c1v2-s3371.json:3-14`; `c1v2-s3372.json:3-14` | Correct `counter_sha256`, landed gate hash, `label: TOPLEVEL_FIELD_MATCH=156/156`, and `predicate_holds: true`. The frozen counter hash was independently obtained from committed bytes (evidence command 7); landed gate hash likewise (command 8). |
| Treating the boolean as the whole P1 | `c1-count-v2.py:338-343,361-364,405-418` | **Not justified.** An invocation uses one seed and one gate. Its boolean proves neither two fresh seeds nor landed-revision identity nor absence of a lower run. |

**Strongest provenance counterexample already in the committed evidence:** `controls/L1-v2-rescore/CtlC1DupPolicy--strict-oracle-s3341.json:4-14` says true and 156/156 but names gate `930a2075…`, not landed `94a7be5a…`. Promoting that true boolean directly to C1 success would assert false provenance. The oracle is expressly feasibility-only (`claims.md:131-134`).

**Smallest safe correction:** retain the frozen counter/predicate unchanged and accompany the final verdict with an immutable, revision-bound aggregation of every candidate/landed run: receipt and stdout paths, gate/counter digests, seed, role, exit and result. Include failures to write a receipt. The counter permits omission of `--receipt` (`:340`) and prints its score before attempting receipt creation (`:405-425`), so the prose kill rule is a procedural obligation, not a self-enforcing program invariant. A complete run ledger/census, not selection of two true booleans, is needed for the global verdict.

The opened landed receipts have distinct seeds 3371/3372, timestamps 08:46:52Z/08:46:56Z, matching landed gate identity and 156/156 (`measure/integrated/c1v2-s337{1,2}.json:3-14`). That supports the two-run portion. This review does not claim to have enumerated every run, including later wave-2 work or unrecorded executions.

## 2. Was v2 a post-data rescue? Committed chronology says no

| Event | Committed evidence | Time/result |
|---|---|---|
| Freeze v2 | Commit `e3e24ec86449e50b089845fef563b7e15c927b40`, evidence commands 1,3,5 | Committed **08:35:29Z**. The patch appends all v2 contract, counter, P1 and kill-rule text. Its round-33 tree has base/oracle receipts, no candidate receipt. |
| Rescore v1 control gates under v2 | Commit `96be79255f8a3bb7d9252e03dd050a1b8b08ac10`, commands 1,10 | Committed **08:40:56Z**, before candidate measurement. `controls/L1-v2-rescore/rescore.sh:14-22` names the v2 counter and two seeds per retained control gate. |
| Candidate code commit | `eb179ec3844f9dff3f938801f5cf2b798052b69d`, command 1 | Committed **08:41:10Z**. |
| First opened candidate scores | `measure/candidate/c1v2-s3351.json:3-14`, `c1v2-s3352.json:3-14` | **08:41:21Z / 08:41:23Z**, gate `52f07c74…`, 156/156 each; added by `7f6aeb70…` at 08:43:17Z (command 2). |
| Integrated landed scores | `measure/integrated/c1v2-s337{1,2}.json:3-14` | **08:46:52Z / 08:46:56Z**, landed `94a7be5a…`, 156/156 each; added at pinned integration commit (command 2). |

The candidate builder explicitly reports **zero counter invocations**, distinguishing its own probes/selftests from P1 scoring (`w1/ExecC1Build.md:9-15,134-138,162`). Its committed artifact directory has no counter receipt (evidence command 6). No committed edit to either `claims.md` or `c1-count-v2.py` occurs between the freeze and the pinned tip (command 4, empty output).

**Conclusion:** the available committed chronology supports a legitimate pre-candidate redesign, not a retroactive denominator/kill-rule amendment. Base/oracle/control scores do precede the candidate; they are the expressly required design controls, not hidden candidate scores (`claims.md:68-75,93-99,131-134`; prompt §9:352-360). This is not proof that an unrecorded execution never happened.

## 3. Does a control meet 156? Oracles do; disclosed shortcuts do not

`controls/L1-v2-rescore/summary.txt:1-68` records the v2 results. The strongest non-oracle control is differing-values-only duplicate rejection: **142/156 on both seeds** (`:23-24`). Its receipt records the correct v2 counter identity, 142 matched, false, and only 10/24 duplicate cases matched (`CtlC1DupPolicy--c-differ-only-s3341.json:3-19`). Do-nothing is 60/156 (`summary.txt:17-18`); no-reader variants are 111/156, 108/156 and 81/156 (`:47-52`). Thus those controls cannot explain away the landed delta.

**Literal answer to “any control meets 156”: yes**, `strict-oracle` and `oracle-pristine` entries do (`summary.txt:27-28,45-46`). Describing the summary as “no control reached 156” without the non-oracle qualifier is inaccurate. `corpus/knowledge/claim-record-fields-r33.md:59` uses that overbroad wording, immediately followed by the correctly qualified best-non-oracle result at `:59-61`.

These are not work-skipping controls: `controls/L1-design/mk-oracle.py:7-24,29-40` actually parses the object using Python `json.loads`, reads top-level members and rejects repeated read keys. `w1/CtlC1DupPolicy.md:20-34,91-95` identifies the same strict-oracle hash `930a2075…`. Their 156/156 is feasibility evidence, not a shortcut surviving §9's required control attack. **Smallest safe correction:** qualify the knowledge sentence as “No pre-data non-oracle control reached 156”; do not delete the passing oracle receipts or amend P1.

## 4. Axis fit and the “already held rule” attack

**Operability fits the changed surface.** The canonical definition is a runnable command producing its stated outcome (AXES.md:13). The lane's executable checklist invokes `verify-claims` to check artifact/revision pointers (`SKILL.md:64-67`); the change replaces that command's raw-line readers with top-level tables (`tools/research-gate.sh:1115-1130,1259-1277`). It is not merely a numerical source-count increase or a newly named province surface.

Operability is the **only scored axis**, score 3, with an intentionally narrow round-1 scale (`SCORECARD.md:5-13`). Therefore “lowest scored” is accurate but does not mean the other five axes were measured, retired, saturated or improved. This counter is not a reason to inflate that old 3-point archive scale.

The intended unknown-key rule already existed (`corpus/evidence/round31/c1-count-v3.py:43`), but it was **not operationally held** for nested members: the same committed counter explicitly describes that carried gate defect (`:16-22`). Base v2 receipt `controls/L1-design-v2/c1v2-base-s3311.json:3-30` is 60/156; the opened landed receipts are 156/156. Thus C1 changes the implementation's behavior rather than only rerunning an unchanged gate on new inputs. It remains a repair/quality improvement on **operability**, not newly earned coverage or depth under prompt §9:361-365.

D1 is different: repairing the exempt-hop *measurement* is expressly not a claim (`claims.md:9-14`). Keeping it outside C1 avoids double-counting an already-held gate rule as new coverage.

## 5. Universal clauses remain; strongest static counterexample

V2 correctly removes the unenumerated “everything else” no-harm promise from P1 (`claims.md:116-118`) and states the exact counted duplicate variants (`:111-114`). It also explicitly excludes malformed lines from the counter while asking the candidate to fail closed (`:139-140`). Nevertheless, the rule is still described universally in `claims.md:30-38` and the knowledge entry says a line that is not one well-formed object is invalid and malformed lines are refused (`claim-record-fields-r33.md:28-30,65-67`). That broader implementation assertion is not established by 156/156: the generator validates every generated row as JSON (`c1-count-v2.py:331-332`), so malformed rows cannot exercise it.

### Concrete witness, not executed by this seat

```json
{"id":"c","source":"README.md","span":"chousa-shokunin","expect":"supported","x":tru}
```

`tru` is not a JSON value. The scanner-only minimal witness is `{"x":tru}`; the longer line supplies the required claim fields so that missing-field invalidation cannot hide acceptance of the malformed token. `README.md:1` contains the span; it also does at round base (evidence command 9).

**[INFERENCE] Static base/landed behavior:** the base raw field readers ignore the unknown `x`; the landed reader also accepts it, leaving the same top-level fields available and no syntax-invalid finding from this token. With the source rooted at the lane, the record is predicted to read `observed=supported`, not the required syntax-invalid result. These are predictions, **not quoted gate outputs or measured exit codes**.

The landed defect is directly localized:

1. `claim_scan` treats an unquoted scalar as bytes up to a delimiter (`tools/research-gate.sh:1217-1225`).
2. It requires only a nonempty scalar (`:1226`); it never checks `true`, `false`, `null` or the JSON number grammar.
3. Closing the containing object then sets success (`:1243-1252`).
4. The caller's malformed-record rejection runs only when `claim_scan` fails (`:1599-1606`), so it does not reject this malformed scalar.

The nested-value path likewise checks bracket/string balancing rather than nested member/value grammar (`:1190-1216`). Thus balancing is not whole-JSON validity. This is an **uncounted, fixable operability defect** in the broad fail-closed assertion, not a lower run of the frozen counter. It does not authorize claiming a P1 miss that was never printed.

**Smallest safe correction:** validate complete value syntax, including ignored scalar/string/container values, before reporting a successful record scan; preserve raw field-string bodies, duplicate handling and the frozen counter. For the specific witness, enforce the scalar token grammar. Do not substitute documentation-only narrowing for the assignment's fail-closed requirement, and do not increase/redefine P1 after scoring. If universal RFC-validity is still claimed, the canonical judge must not infer it from the finite 156-record result.

Other finite-sampling boundaries are explicit: `marker_default`, escaped keys, unread duplicates and malformed lines are excluded; marker duplicates and conflicting ids are uncounted (`claims.md:80-83,111-114,136-140`). The decoy matrix is enumerated, not every possible nesting/string topology (`:103-109`; counter `:73-101,139-148`). **No surface saturation follows.** The “no lower run” clause is a procedural quantifier over actual runs, not evidence of correctness for all JSON inputs.

## 6. Repairs, sources and knowledge — limited cross-check

- **D1–D5:** the frozen design names them as repairs, not extra claims (`claims.md:9-14`). QUALITY 36 addresses metadata-independent fixtures (`corpus/QUALITY.md:275-284`), 37 receipt-tally commands (`:286-291`), 38 battery revision headers (`:293-298`), and 39 recorded-process-only signalling (`:300-306`). These are separate obligations; they cannot make the C1 predicate true by substitution.
- **D2 does not supply the missing C1 global audit:** `corpus/evidence/round33/d2-census.py:2-17,30-31` is specifically the **round-32 APPEND_SERIALIZED** census. It is not a round-33 TOPLEVEL_FIELD_MATCH run-history verifier. This is a scope distinction, not a claim that its stated D2 repair fails.
- **Source authority is appropriately separated:** `corpus/SOURCES.md:72-73` distinguishes RFC object/duplicate semantics and Python default duplicate handling from the lane's local reader policy. The knowledge entry explicitly says rejecting duplicates is the lane's choice, not something either source mandates (`claim-record-fields-r33.md:36-45`). No false standards authority for local fail-closed policy was found in those passages. I did not reopen either URL and claim no independent live-source verification.
- **Knowledge corrections needed:** qualify “no pre-data control” as above; correct the overbroad malformed-refusal assertion through the implementation, not a passing-counter gloss. The entry itself distinguishes counted/unmeasured families (`:63-73`). I did not independently rerun D1/D2/D3/D5 checks or validate their full implementations.

## Disposition and limits

The committed evidence defeats the proposed attacks that v2 was frozen after the opened candidate scores, that the counter uses a different numerical predicate/label, that do-nothing already meets 156, or that operability is merely a mislabeled count. It does **not** justify the stronger claims “the receipt boolean is the global P1,” “no control of any kind reaches 156,” “every malformed line is refused,” or “the whole JSON-reader surface is saturated.”

**Impacted axes:** operability for the malformed-reader counterexample; calibration/provenance as a review risk if finite/per-run evidence is reported universally. This review awards no second axis move and makes no canonical judgment. Its remaining global-kill-rule uncertainty is explicit, not a fabricated pass/failure.

No production files, lane/fleet Git index or jj state were changed. Only this requested report and its private evidence file were written. No installs, network, subagents, background workloads or process signals. A quick static-counterexample coordination message was sent to the assigned malformed-input peer; no peer result is used as evidence here. No follow-on execution is represented as completed.
