# CriticAxisFit33 — C1 axis fit and §9 shape

Reasoning-only review of frozen design v1 at `3b528b9a926dd53001a1f1da5df6be1c63fca3ca`. This is advisory criticism, not a Rust-judge, admission, or candidate verdict. Lane-relative paths below are under `/home/vgpnk/Projects/shokunin/chousa-shokunin`; `../` denotes the fleet root.

## Assessment

**Operability is the defensible axis, and the lowest scored non-retired axis. A real implementation repair could move it; the finite counter does not establish the entire behavioral contract as written.** The material objection is contract-to-counter overreach, not a necessary trade between axes. No candidate was opened or scored by this seat.

### Axes and score identity

- The six axes are depth, coverage, operability, freshness, calibration, adjacency (`../AXES.md:9-16`). The changed surface is a runnable command's field reader, not the number 144: C1 names `json_str`/`json_has_key` and their `verify_claims` callers (`corpus/evidence/round33/claims.md:18-27`; actual raw-line regexes at `tools/research-gate.sh:1109-1128`, callers at `:1448-1483`). Correct field identity is necessary for that command to produce its stated outcome, the operability definition (`../AXES.md:13`).
- Operability alone has a numeric score, 3; the other five are explicitly unmeasured, not zero (`SCORECARD.md:7-13`). None is retired (`:32-34`). The recorded saturation test fails closed because 3 is below 8 and unscored axes do not count as saturated (`:469-495`). Thus “lowest **scored** non-retired” is justified; neither “all axes saturated” nor “the other axes are higher” is justified.
- Preserve the original score's identity. It counts three archived inputs and can award at most 3 (`SCORECARD.md:11-13,26-30`). Add a separate C1 observable, not a fabricated 3→4 conversion. This is the existing convention in round 25 (`:1343,1410`), round 29 (`:1605-1608`), round 31 (`:1754-1755`), and round 32 (`:1820-1821`). Potential calibration harm would arise from changing that meaning, not from leaving the scalar at 3.

### Real repair versus re-scoring held ground

- The intended top-level rule is already part of held method: round 31 says unknown JSON keys are ignored (`corpus/evidence/round31/claims.md:87,151`). Its revised counter explicitly records the nested-field violation as a carried **gate defect**, not an added class that the landed gate passes (`corpus/evidence/round31/c1-count-v3.py:16-22,43`). The scorecard also discloses it (`SCORECARD.md:1798-1804`), and the outside round-32 check routes it as D4 (`corpus/lessons/round-32-verifier-spotcheck.md:166-167`).
- Consequently this is restoration of executable behavior on an existing rule, not new coverage or depth. That is compatible with an **operability/quality** move: §9 forbids relabeling re-scoring as coverage or depth, not repairing a command that fails its contract (`../.ufo/prompts/chousa-round-33.md:361-365`; quality includes operability at `../AXES.md:20-23`). Merely adding a new counter with no gate behavior change would not establish this move.
- The recorded base run shows a real observable deficit: `TOPLEVEL_FIELD_MATCH=60/144`, including duplicate records observed `supported` instead of `invalid` (`.ufo/waves/round-33/controls/L1-design/c1-base-s3301.json:3-16,33-37`). Thus the proposal is not simply counting an already-passing implementation. This is existing evidence, not a rerun or proof of a candidate improvement.
- D1 is correctly excluded as a fresh claim: it repairs a counter for an already-held exempt-hop rule (`corpus/evidence/round33/claims.md:9-14`; `SCORECARD.md:1818,1844`). Treating that repair itself as new coverage would repeat the round-32 discrimination mistake.

### Anti-loop: preserve surface identity, do not invent a permanent ban

- Rounds 29 and 30 worked `tools/quote-reopen.py`; round 29 says `research-gate.sh` stayed byte-identical, and round 30 says it was untouched (`SCORECARD.md:1593-1608,1687-1700`). Round 31 deliberately rotated to `research-gate.sh verify-claims` (`corpus/evidence/round31/claims.md:60-62`; `SCORECARD.md:1740-1752`).
- Round 32 worked `verify-all --json` appends and `verify-chain` exempt hops and explicitly left `verify-claims` unchanged (`SCORECARD.md:1806-1818`). C1 returns to a surface worked in round 31; it is **not** a newly acquired command, but it is also not three consecutive axis+surface claims. Do not claim a wholly new parser surface simply because the counter label changed.
- The referenced campaign note's concrete trip is three rounds running of the same axis+surface claim **or** routed defect class, with rotation required in the next round (`../.scratch/goal-20261022-hyaku-12h.md:168-173`). [INFERENCE] The disclosed surface sequence does not show that claim trip. If merely carrying the same nested-field defect from round 31 through round 33 is counted under the defect-class branch, that calls for next-round rotation; it is not evidence that any surface once used in round 31 is permanently barred. The canonical assignment/judge, not this campaign-note interpretation, determines admission.

## Counterexample and §9 objections

### F1 — Seven-key duplicate contract, three-key duplicate population

**Static counterexample (not executed):** a top-level parser that rejects duplicates only for `line`, `sha256`, and `source`, while preserving first-value behavior for `id`, `span`, `expect`, and `marker`.

- Required scope: the seven keys are named at `corpus/evidence/round33/claims.md:30-36`; a duplicate read key is invalid even when values agree.
- Enumerated scope: the only duplicate class chooses keys from exactly `("line", "sha256", "source")` (`corpus/evidence/round33/c1-count.py:85`), and its builder has only those three cases (`:233-253`). The other classes do not generate duplicate top-level read keys (`:190-232,254-284`). Fresh seeds shuffle existing classes; they do not add missing key classes (`:293-309`).
- Witness input, with `src/example.md` containing the boundary-delimited span `needle`:

  ```json
  {"id":"same","id":"same","source":"src/example.md","span":"needle","expect":"supported"}
  ```

  The contract requires `invalid`; identical ids avoid ambiguity about the claim identity. [INFERENCE] The three-key duplicate validator can retain an otherwise matching implementation's 144/144 on every generated seed yet accept this record as supported. This is a static discrimination gap, **not** a measured mutant score.
- Impacted axes: operability (the duplicate rule would still fail); calibration (144/144 advertised as proof of the full seven-key rule). This is a fixable specification/measurement defect, not evidence of a necessary axis trade.

### F2 — Universal preservation is not enumerated or fully observed

- “Everything else” and “Records without nesting or duplicates verify exactly as at base” are unbounded clauses (`corpus/evidence/round33/claims.md:39-40`). The counted flat population is six string-confuser variants with right/wrong line bindings plus four plain outcomes, not the full landed behavior (`c1-count.py:86-88,254-284`). All generated records use top-level `expect=supported` (`:172-173`); marker testing is a nested decoy with no top-level marker (`:226-232`).
- More decisively, the scoring path accepts either gate exit 0 or 1 (`c1-count.py:354`), then tests observed outcome and only the two mismatch-finding sets (`:369-376`). It does not compare the gate exit to a base exit or assert its summary/verdict text. [INFERENCE] An otherwise passing implementation changed to return 0 instead of its drift return 1 could keep 144/144 while violating the expressly preserved exit-code contract. No such candidate regression was observed or run here.
- The general top-level/nested/string invariants (`claims.md:30-38`) also range beyond the three container templates and six string confusers (`c1-count.py:58-70,129-138`). They may be implementation requirements, but the **measured after-state** must not imply exhaustive JSON correctness. Section 9 explicitly bars unenumerated universal claim clauses (`../.ufo/prompts/chousa-round-33.md:343-347`).
- Smaller prose mismatch: the counter description says each read field has before/after decoys (`claims.md:43-45`), whereas `marker` has no top-level counterpart and `expect` is only nested-before (`c1-count.py:226-232`). Describe the actual matrix, not a larger Cartesian product.
- Impacted axes: operability and calibration; no actual cross-axis harm is established by this reasoning-only review. A **real** exit-contract regression would be a no-harm failure, not an acceptable trade (`../AXES.md:33-36`).

### F3 — Round-wide predicate needs round-wide evidence

- P1 includes two fresh-seed runs and no lower run on that revision in round 33 (`claims.md:51-55`). The counter code/receipt `predicate_holds` is only `matched == TOTAL` for one invocation (`c1-count.py:390-403`); it cannot alone establish the round-wide conjuncts. The kill-rule wording additionally says “committed run,” while P1 says “no run” (`claims.md:53,57`). An uncommitted low run must not silently disappear from a no-run assertion.
- This is an evidence-binding limitation, not an observed failed run. Receipt provenance contains gate hash but no lane revision or run-role field (`c1-count.py:396-403`). Smallest safe handling within frozen v1 is an explicit external census binding the relevant receipts/run disclosures to the landed gate bytes and retaining every miss. Do not call a single `predicate_holds=true` receipt the whole P1 result.

## Before value and do-nothing discrimination

**Literal answer:** the before value **is** reachable by doing nothing; it is the do-nothing result, 60/144. Section 9 requires the **after target**, 144/144, to be unreachable by a control skipping the claimed work (`../.ufo/prompts/chousa-round-33.md:352-356`).

The opened base receipt records counter hash `ab6b2ae2…e229`, gate hash `f4731885…03f0`, seed 3301, `gate_rc=1`, matched 60, and `predicate_holds=false` (`.ufo/waves/round-33/controls/L1-design/c1-base-s3301.json:3-14`). Thus that observed do-nothing run does not meet the after target. The two opened 144/144 receipts use the disclosed parser oracle, not the base gate (`c1-oracle-s3302.json:3-14`; `c1-oracle-s3303.json:3-14`); they establish recorded feasibility only, not a no-work shortcut or candidate success. Other skip-work control discrimination is not certified by this seat; the frozen plan requires those receipts before candidate scoring (`claims.md:68-75`).

## Smallest safe correction

1. Keep C1 on operability, keep 3→3 on the original scalar, and record a separate measured field-reader repair observable. Keep D1–D3/D5 as repairs, not extra axes/claims (evidence above).
2. Preserve the frozen counter, TOTAL, P1 and receipts. This seat does not patch a counter. Route F1/F2 as pre-candidate design findings: either a newly authorized, separately frozen design must enumerate its intended duplicate-key/missing-case checks before any candidate data, or v1 must retain its numerical result **with the wider contract explicitly unproved**. Do not silently narrow the frozen target or reinterpret a miss after data (`claims.md:57-59,74-75`; round prompt `:351,357-360`).
3. Do not use 144/144 as the no-harm battery. Bind the separate preservation evidence and receipt census to a revision, preserving all failures; the preceding outside check specifically requires future battery revision headers (`corpus/lessons/round-32-verifier-spotcheck.md:163-165`). A stronger implementation remains allowed; stronger prose is not a substitute for evidence.

## Commands, provenance, limits

Only filesystem/source reading and the following bounded, foreground fact commands were run; all exited 0:

```text
timeout 10s mkdir -p /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-33/w1/CriticAxisFit33
# No output.

# cwd: /home/vgpnk/Projects/shokunin/chousa-shokunin
timeout 10s sha256sum corpus/evidence/round33/claims.md corpus/evidence/round33/c1-count.py tools/research-gate.sh
9e1273772aa32ad5d682b3afc44d277ae176a568cc3592bf0e262412eb193f4f  corpus/evidence/round33/claims.md
ab6b2ae24f6b402e66b583fa0021742204f12bdb4f1b056f8598cd63dc43e229  corpus/evidence/round33/c1-count.py
f4731885ac0f83076210be364fd443a4378ac88c3b3ef94b5bf1c9e380f003f0  tools/research-gate.sh

timeout 10s git ls-tree -l 3b528b9a926dd53001a1f1da5df6be1c63fca3ca -- corpus/evidence/round33/claims.md corpus/evidence/round33/c1-count.py .ufo/waves/round-33/controls/L1-design/c1-base-s3301.json .ufo/waves/round-33/controls/L1-design/c1-oracle-s3302.json .ufo/waves/round-33/controls/L1-design/c1-oracle-s3303.json tools/research-gate.sh
100644 blob 813560f3536fe45b8896e0a541ffa9df1fc6fa1b   11295 .ufo/waves/round-33/controls/L1-design/c1-base-s3301.json
100644 blob 72263ec31619fce1fa2c4752a4eb13ad36c357d2    1109 .ufo/waves/round-33/controls/L1-design/c1-oracle-s3302.json
100644 blob d26843b763df52fdbed212c2b2feb696bb8868b2    1109 .ufo/waves/round-33/controls/L1-design/c1-oracle-s3303.json
100755 blob 9bc858d2222d8b78abfe1eac3e9b3d9fc80b4d03   19037 corpus/evidence/round33/c1-count.py
100644 blob 680b414b2eef624ec80c0ecbc2a0431c2a16430f    6417 corpus/evidence/round33/claims.md
100755 blob ad21f5c15b54779c617f30d8a9c19b2b5a9b4b6f  336677 tools/research-gate.sh
```

The tree listing establishes that the opened baseline/oracle receipt paths and frozen design files are committed at the assigned design revision. Existing receipt gate exits are attributed above; no counter process exit was measured by this seat. Static witnesses are marked [INFERENCE]. No counter, gate, selftest, candidate, alternate judge/runtime, network fetch, install, subagent, or background job was invoked. No production file, Git index, or jj state was modified. Only this report was written; the required own-directory is empty.
