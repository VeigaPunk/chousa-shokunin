# CriticAxisFit32b — round 32 attempt 2, wave 1

Scope: adversarial review of C1/C2 axis fit, anti-loop, and round-prompt §9 shape. These are review opinions, not canonical Rust judgments or admission decisions. Paths below are lane-relative unless prefixed `../` or absolute. No candidate implementation was scored, no counter or production file was edited, and no other runtime was invoked.

## Axes and per-claim review opinions

| Claim | Axis-fit opinion | §9 shape opinion |
|---|---|---|
| C1 manifest append lock | **Supported: operability, including the lowest-scored non-retired axis.** It changes the correctness of a runnable command's persistent output under cooperating concurrent writers, not domain breadth. | The finite `APPEND_SERIALIZED=24/24` observable is well named, but it does not establish the entire unrestricted prose contract. Retain the frozen predicate; do not advertise universal preservation or full append-path coverage from this count. |
| C2 exempt-hop audit | **Supported: coverage of a previously unread source-content edge class**, conditional on actually resolving eligible U citations through the existing guards/matcher. It is not merely another score of the resolved-hop rule. | There is a concrete contract/counter gap even within the enumerated fixture: exactly-one finding and DRIFT are stronger than the counter's matcher. Additional universal unread/unchanged guarantees are not enumerated. |

### C1: strongest axis objection does not hold

`../AXES.md:12-15` distinguishes domain surfaces from runnable artifacts. The changed surface is `verify-all … --json PATH`'s last-byte probe plus append (`corpus/evidence/round32/claims.md:16-28`), whose base code probes at `tools/research-gate.sh:3192-3195` and appends separately at `:3199`. That is operational correctness of an existing command.

The strongest apparent objection is that this was already round-24 work and cannot improve a saturated observable. Local evidence defeats that objection: round 24 expressly left the two-operation race unfixed (`corpus/knowledge/json-delimiter-r24.md:66-71`); round 25's next-round plan still calls the flock candidate unlanded (`SCORECARD.md:1371-1376`). The inspected base code still contains that gap. This is not claiming the already-landed single-writer delimiter repair again.

Operability is the **only recorded numeric axis score**, 3/10 (`SCORECARD.md:5-13`), and none is retired (`:32-34`). The scorecard explicitly rejects treating unscored axes as saturated and retains the lowest-axis obligation (`:484-495`). C1 therefore meets the axis-selection rationale without inventing scores for the other five axes. A successful C1 would sit beside the historical 3/3 export observable, not justify increasing its exhausted 3/10 scalar; that distinction is already used in `SCORECARD.md:1603-1608,1752-1755`.

### C2: test the strongest re-scoring counterexample

The lane already holds citation parsing, source boundaries and anchor matching for `resolved` rows (`tools/research-gate.sh:1828-1878`). However, the base exempt arm merely increments a count and formats the `to` cell; it never calls citation parsing, source resolution or the anchor matcher (`:1880-1883`). Rows were always parsed; the new surface is **target-source content for U rows**, not previously unread table rows.

A particularly strong prior-art objection is round 10's existing exempt-item audit. That was an audit of six particular items at an **unchanged gate** (`corpus/knowledge/hardening-r10.md:109-118`); it explicitly says exemption truthfulness remains not mode-checkable and says nothing about other records (`:159-162`). It does not establish the proposed general gate operation.

There is also a concrete historical witness, not merely a newly invented fixture: `corpus/lessons/2026-10-15-chain-hop-resolution.md:118-123` records an `unresolved` hop whose anchor exists at A:52 but still receives `observed=exempt`, `RESOLVED_HOPS=0/1`, CLEAN. The frontier still names that unverified declaration (`corpus/README.md:355-362`). C2 would change this existing input's disposition; simply re-running the held resolved-hop rule on fresh inputs would not. The §9 edge-class criterion (`../.ufo/prompts/chousa-round-32.md:361-365`) therefore supports the coverage label.

Coverage must remain narrow: local resolvability of U = unresolved / blocked-no-fetch / labelled-dead, not exemption truth in general, live URL availability, fidelity, entailment, chain transitivity, or rejected/not-applicable judgments (`claims.md:60-70`; `corpus/knowledge/chain-resolution-r3.md:131-156`). `PROVINCE.md:5-8` places citation chaining and the lane's gates within scope.

## Findings: counterexamples, affected axes, smallest safe corrections

### F1 — C2's count can preserve a contract violation inside the counted set

**Counterexample (static derivation, not an executed gate):** take output that matches all 120 hidden truths, then duplicate each `CHAIN_EXEMPT_RESOLVABLE` finding. The contract requires exactly one such line (`claims.md:64-65`), but the counter accumulates finding IDs in a **set** (`c2-count.py:268-273`) and compares only that set (`:282-286`). Duplicating an identical finding does not change the matched count. This implication follows directly from the opened code; no passing experimental receipt is claimed.

The same matcher accepts gate rc 0 or 1 (`:269`), does not parse the final CLEAN/DRIFT summary, and checks only hop `observed` plus finding-ID sets. `LINE_RE` does not inspect hop verdict, while `FIND_RE` accepts any non-whitespace severity and surface (`:78-79`). Thus `120/120` alone cannot establish the contract's `verdict=mismatch`, `severity=warn|crit`, `surface=chain`, or record-DRIFT clauses (`claims.md:63-65`).

**Affected axes:** operability of the verdict interface; calibration of what the coverage receipt proves. This is a fixable detector/provenance defect, not a reason to rename C2 as quality or a demonstrated candidate regression.

**Smallest safe correction:** report the counter bug without editing the frozen counter. L1 can retain P2 exactly and separately check the promised output contract, recording this detector limit honestly. If it needs the stronger contract to be the counting predicate, only an explicitly new pre-candidate design version under `claims.md:99-103` can add multiplicity, field, verdict and summary checks; do not silently reinterpret a 120/120 v1 receipt. Any known miss under the frozen rule remains a miss. Routed the set/cardinality issue to CriticPredicateGaps32b and ReviewerCounters32b by peer message.

### F2 — both contracts contain preservation universals beyond their enumerated populations

**C1:** `claims.md:27-28` says prior bytes are never rewritten, the inode is preserved, every appended line is a JSON object, and **“Nothing else in verify-all changes.”** The 24 trials do check prefix/inode/object/newline properties for the generated seeds (`c1-count.py:157-195`), but all counted writers consume one generated, single-source claims-JSONL shape (`:89-99,198-204`). This does not enumerate all verify-all sections, manifests, records, failures or filesystem conditions. The named no-harm battery is finite (`claims.md:111-117`), not the full universe in “nothing else.”

A sharper gap is creation when PATH is absent (`claims.md:24`). Every counted trial pre-creates PATH (`c1-count.py:200-204`). The solo reference does target a missing `ref.jsonl`, but checks only rc 0/1 and does not inspect its existence or bytes (`:275-286`). **[INFERENCE]** An implementation that returns the normal rc while failing to create an absent manifest is not rejected by that reference check if its existing-file trials are otherwise correct. No such implementation was built or scored here.

**C2:** `claims.md:65-70` says **every** other U hop remains exempt, rejected/not-applicable stays unread **whatever** its citation, resolved hops are unchanged, and no network read is added. The counter enumerates 14 classes (`c2-count.py:58-73`), only verifiable resolved hops for F1 (`:185-192`) and resolvable local judgment hops for E5 (`:203-205`). It does not enumerate resolved invalid/refused/missing-anchor behavior or instrument source/network reads. Matching output is not proof of “unread.”

A useful omitted semantic boundary is an in-boundary file containing the anchor that would nevertheless be refused as resolved because it is over 8 MiB or multi-linked. Those are existing resolved-path guards (`tools/research-gate.sh:1224-1244`), not permissions to broaden the reader. **[INFERENCE]** A new audit that checks only path containment and anchor bytes would overreach C2 even though the fixed classes do not exercise these guards. Reuse the held resolver and anchor semantics, rather than create a second authority.

**Affected axes:** C1 operability; C2 coverage/operability; calibration for both if finite success is promoted to universal preservation. No actual harmed candidate is established by this static review.

**Smallest safe correction:** keep the frozen numerical targets and kill rules unchanged; explicitly bound the resulting evidence to the enumerated trials/classes and named no-harm battery. Preserve the broader implementation obligations, but substantiate them separately with a narrowly scoped diff/control audit rather than claim the count proves them. If §9 requires changing the formal claim wording or counted population, report that as a pre-data design defect for L1 to resolve under the existing version rule, never narrow it after candidate data. Do not claim full axis saturation or all exemption truth has become held ground.

### F3 — the compound predicates need a complete, revision-bound run universe at closure

P1/P2 require two fresh-seed successes **and no lower run on the landed revision** (`claims.md:36-40,77-81`). The receipt's `predicate_holds` is a per-run `matched == TOTAL` (`c1-count.py:298-316`; `c2-count.py:303-315`), not a reduction of the compound round predicate. The claim file does not specify a complete run index/reducer for the “no run” quantifier.

**Counterexample [INFERENCE]:** two cited true receipts plus an omitted false receipt from the same landed revision would satisfy a selected-pair reading but not the actual frozen claim. This is not an allegation that such a candidate receipt exists.

**Affected axis:** calibration/provenance. **Smallest safe correction:** enumerate and commit the complete raw receipt set for each claim, with gate revision/hash, frozen counter hash and seed, including failures; provide the one closure command that reduces that set. A later counter success cannot erase a same-revision miss. Do not combine controls, feasibility oracles, or superseded revisions with candidate evidence. This supplies evidence plumbing without changing either predicate.

## Anti-loop and repairs

C1 changes manifest output serialization; C2 changes source auditing for the exempt arm of verify-chain. Their declared locations are disjoint from quote re-open and verify-claims (`claims.md:10-12,92-97`). Local previous-round evidence agrees: r29/r30 worked quote-reopen (`SCORECARD.md:1593-1608,1687-1700`); r31 worked verify-claims location/revision binding and explicitly left quote-reopen untouched (`:1740-1757`). Reusing held parsing/matching helpers for a new U edge class is not replaying those claims. A build that instead changes claim binding or quote fetch behavior would need separate attribution and cannot borrow this axis-fit opinion.

R1–R6 remain repair work, not added coverage or operability claims: their routed scope is explicit at `corpus/lessons/round-31-verifier-spotcheck.md:201-234`; frozen exclusions are `claims.md:10-12`. No round-31 repair counter results are supplied by this review.

## Evidence opened and commands actually run

Read first: frozen `corpus/evidence/round32/claims.md`, then both counter docstrings. Opened the named §9 prompt, fleet/canonical axes, scorecard, province, relevant gate branches, historical chain/exemption and manifest notes, round-31 routed defects, and the two existing L1 do-nothing receipts.

Existing receipts, **opened, not rerun**:
- `.ufo/waves/round-32/controls/L1-design/base-s11.json:3-18`: frozen C1 hash, base gate hash, seed 11, `APPEND_SERIALIZED=8/24`, false; L classes 0/4 each.
- `.ufo/waves/round-32/controls/L1-design/c2-base-s21.json:3-29`: frozen C2 hash, base gate hash, seed 21, gate rc 0, `EXEMPT_AUDIT_MATCH=84/120`, false; R1–R3 each 0/12, all other listed classes matched.
These substantiate separation from the disclosed do-nothing control; they do not replace the assigned cheap-control wave or candidate measurements.

Commands executed from the lane root:
1. `timeout 10s mkdir -p /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32/w1/CriticAxisFit32b` — exit 0, no stdout.
2. `timeout 10s sha256sum tools/research-gate.sh corpus/evidence/round32/claims.md corpus/evidence/round32/c1-count.py corpus/evidence/round32/c2-count.py` — exit 0:
   - gate: `0bc318b3e74ac0ad45f4b34154e886d84aebf44673612afab6de5e0b0ff11258`
   - claims: `b6641e862c5d7b89df61f45daea7e67702ad1054eb547a7375534814764dfa26`
   - C1 counter: `9e787e80b215f6522335c639d5e1b2e60d0a5812b83a9760daf8be9f78415885`
   - C2 counter: `b6626b2cb81b2aeaf66a8ff11a06c030612bf4e264dc128f290021c4aa71f54c`

Limits: static assigned review only; no counters, builds, selftests, candidate gates, network requests, canonical judge, installs, git/jj writes, background jobs or subagents. Hypothetical counterexamples are labeled as static derivations or [INFERENCE], not reported as exercised results. This report is written once; no extra experiment artifacts were created.
