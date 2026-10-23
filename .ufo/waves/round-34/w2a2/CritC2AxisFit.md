# CritC2AxisFit — frozen C2 claim-sizing review

Access date for every located source: **2026-10-23**. Axes: **operability, calibration**. This is a critic's evidence record, not an admission decision or a Rust-judge invocation.

## Scope, pins, and result

Reviewed `707da8184a0fc4d10ab3f17271556cdf364f0af5` in an isolated local clone at `/fast/scratch/hyaku/chousa-r34-a2/w2/CritC2AxisFit/frozen` (abbreviated **F** below). Production-path citations below refer to that revision. **E** means `.ufo/waves/round-34/w2a2/CritC2AxisFit/` in the lane. Read the frozen design, C2 counter, audit tool, and audit set first. No production, lane index, jj state, fleet, or sibling changes; no network, installs, signals, C1 counter runs, or held-control re-scoring.

- Landed gate: `a6307edf687ac0fb1b0b08bf7f0518b3fbc310fa9924b970aa3654612562995b`.
- Before gate, extracted from `bf7c931a:tools/research-gate.sh`: `772a1d8e4d94dbf3a44a64bf850b1324e51546eeb62abcd7b3ec585f0e003e58`.
- Frozen counter: `8c0def4d377cdf1a1e4bd2c9151bb0846216658ff14d725d15ac037c12212173`.
- **Numerical re-derivation:** landed `37/37` on fresh seeds **6701309, 6701321**; before `21/37` on the identical seed 6701309. Audit re-run: **0 mismatches / 0 undispositioned**, 43 enumerated checks.
- **Counterexample:** two legal 32765-byte, boundary-delimited-span cases produce `unsupported` and `mislocated` instead of `supported`. Thus the numerical P2 evidence does not establish the unqualified surface contract in `claims-a2.md:52-59`.

All significant child PIDs, exact argv/cwd, exit codes, and stdout/stderr hashes are in **E/commands.json:1-113**. No test was scored from unpinned working-tree gate bytes.

## 1. Strongest counterexample: an earlier occurrence masks an overlapping valid one

The frozen contract says a delimited dead-zone span is supported, and a named line range binds iff a delimited occurrence occupies it (`corpus/evidence/round34/claims-a2.md:51-59`; also gate header `tools/research-gate.sh:54-62`). The counter's separated-copy fixtures do not enumerate overlapping occurrences (`c2-count.py:197-215,235-253`).

Executed fixture construction:

```python
span = 'a\n' * 16382 + 'a'       # 32765 bytes
source_glued = 'x' + span + '\na\n'
source_two_valid = ' ' + span + '\na\n'
```

Both sources contain the exact span at byte offsets **1 and 3**. Offset 3 starts after a newline and ends before a newline, occupying **lines 2–16384**. In the first source, offset 1 is glued to `x` and invalid; offset 3 is valid. In the second, both occurrences are valid, and the claim explicitly names `"line":"2-16384"`. The independent oracle enumerated both exact offsets and the qualifying line ranges: **E/overlap-oracle.json:1-47**. This uses only ASCII letters/newlines and remains inside C2's window; no C1 input was scored.

Command actually run, with C2_TMP/C1_TMP/TMPDIR set to this seat's scratch directory:

```sh
timeout 180s bash "$F/tools/research-gate.sh" verify-claims \
  /fast/scratch/hyaku/chousa-r34-a2/w2/CritC2AxisFit/overlap-fixture/claims.jsonl \
  --root /fast/scratch/hyaku/chousa-r34-a2/w2/CritC2AxisFit/overlap-fixture
```

Exit **1**, with:

- `OVERLAP_GLUE`: `observed=unsupported`, `CLAIM_SPAN_NOT_FOUND`.
- `OVERLAP_LINE`: `observed=mislocated`, first location `lines:1-16383`, despite the correct second range.
- `VERDICT_BEARING_CLAIMS=0/2` and one DRIFT summary.

Evidence: **E/overlap-landed.stdout.txt:2-7**; gate/command/exit binding **E/commands.json:93-110**. Preserved inputs: **E/witness/**; claims-file SHA-256 `ab4ab4640861bbfe07accef856271d802696fc1827bb8cc80f2115a0cde97b7c`.

Cause visible in the frozen source: whole-byte equality sets `resume=offset+slen` before either token boundary or the requested line range is considered (`tools/research-gate.sh:1635-1640`). The overlapping occurrence is discarded. Boundary filtering happens later in `tok_span_at`/`tok_span_all` (`:1652-1661,1673-1682`); line selection happens later still (`:1888-1904`). This ordering is inherited, not evidence of a new regression from lowering the routing constant.

**Impacted axes:** operability (remaining false negatives / incorrect line binding), calibration (the measured predicate is narrower than the advertised contract). **Smallest safe correction now:** retain the frozen counter, TOTAL, P2, and receipts; explicitly record this unmet contract rather than silently narrow it after scoring. Any later semantic repair must stop discarding overlapping candidates before qualification and be separately authorized/tested across shared callers. This read-only review makes no such repair or C1 judgment. P2's committed-run kill rule is not itself triggered by this separate fixture.

## 2. The do-nothing control is real; its frozen explanation is arithmetically false

`claims-a2.md:99-105` predicts 17 long-supported records and a 4/37 ceiling. The counter actually declares:

| Population | supported | unsupported | mislocated | total |
|---|---:|---:|---:|---:|
| Dead-zone records | 12 | 17 | 4 | 33 |
| Short controls | 2 | 2 | 0 | 4 |

Source: `c2-count.py:71-91`. I independently summed those constants with a bounded `python3 -B -c` invocation using `runpy.run_path(..., run_name="review_constants")`; exit **0** printed `do_nothing_matches=21/37` and `changed_cases=16` (command recorded in this seat's tool transcript). No counter main function ran in that calculation.

A compile failure emits `unsupported`, so all **17 unsupported long records score correct without successful matching**, as do the four short controls. The **12 supported + 4 mislocated** dead-zone records miss. My actual base-gate run reproduces that exact class pattern, exit **1**, with PCRE's large-pattern error in its receipt: **E/c2-before-s6701309.json:5-33**. Landed run on the same seed scores all 37, exit **0**: **E/c2-after-s6701309.json:5-35**.

**Interpretation:** 21/37 is partly a truth-distribution credit, not 21 successfully evaluated dead-zone spans. It is nevertheless below the frozen 37/37 target, so this do-nothing control does **not** invalidate the target. The actual move is 16 changed classifications, not 33 newly searched cases. **Smallest correction:** append an arithmetic erratum explaining 12/17/4 and 21/37; preserve the erroneous pre-data prediction and the frozen rule. Do not change the counter's truth distribution to make the original 4/37 story true.

Calibration cross-check: the audit still prints 0/0 because its check of `claims-a2.md` is existence only (`audit-set.json:119-122`); it has no check of this arithmetic. The 43-check count therefore reproduces but does not certify correctness of the C2 explanation. Evidence: **E/audit-frozen.stdout.txt:1-45**, especially `:44-45`; audit dispatch implementation `self-audit.py:84-87,111-119`.

## 3. Surface, minimality, and predicate/label agreement

- **Real operational surface, not merely new inputs scored against unchanged executable bytes.** `git diff bf7c931a 707da8184a0fc4d10ab3f17271556cdf364f0af5 -- tools/research-gate.sh` (exit **0**) shows one non-selftest behavioral change: `TOK_DIRECT_SPAN_MAX=32767` becomes **32764**, plus comments and three selftest cases. The router and existing chunk confirmation are at `tools/research-gate.sh:1581-1603,1621-1641`. The same-seed before/after outputs establish an execution difference. [INFERENCE] This supports a narrow **operability** move; it is not a new verbatim-verification rule or a coverage/depth claim merely because a new counter was added.
- **Minimal for the identified host routing failure:** changing that constant moves precisely the three lengths onto existing machinery; no second matcher authority was introduced. For lengths outside the window the routing comparison takes the same branch as before. This is static delta evidence, not a universal no-regression test. It does not cure the overlap defect above.
- **Per-run predicate agrees.** Frozen P2 and its explicit code/label statement are `claims-a2.md:87-96`; counter docstring restates them at `c2-count.py:5-9`. `TOTAL==37` is pinned at `:90-91`; `holds = matched == TOTAL`, the printed `DEADZONE_MATCH` label, and `predicate_holds` storage are at `:370-379,389-398`. I found no local condition/receipt-label mismatch.
- **The Boolean is per-run, not the entire quantified P2.** Two fresh seeds and the absence of committed lower runs are additional evidence duties, not conditions encoded in one receipt's Boolean. The six committed C2 receipts in the frozen evidence tree are catalogued in **E/committed-receipts.json:1-74**: two before counts 21; four landed counts 37, with correct counter/gate hashes. Seeds 5033 and 5047 are additional to the before seeds 5011/5023. My fresh landed receipts both have count 37 and `predicate_holds=true` (**E/c2-after-s6701309.json:12-15**, **E/c2-after-s6701321.json:12-15**).
- Searched the frozen `.ufo/` and `corpus/` trees using both the full counter digest and `DEADZONE_MATCH=[0-9]+/37`; only those six receipt measurements appeared. This is a committed-tree sweep, not a claim to recover uncommitted or deleted historical runs.

## 4. What 37/37 does not establish

The prompt's sizing rule disallows universals unless the command enumerates their full set (fleet `.ufo/prompts/chousa-round-34.md:350-372`, especially `:351-354,359-369`). The enumerated set here is **37 generated records**, not all delimited spans or all byte mutations. The concrete overlap witness demonstrates why that distinction matters.

- **Quote anchors:** `verify-chain` quotes call the same matcher (`tools/research-gate.sh:2076-2079`), so their routing changes too. The behavior change is disclosed in `SCORECARD.md:1964-1965` and `corpus/knowledge/dead-zone-pcre-r34.md:43-45`, but the C2 counter never invokes that mode (`c2-count.py:328-330`). [INFERENCE] Shared code makes transfer plausible; the 37/37 receipt is not quote-anchor verification.
- **verify-all, including line binding through it:** composition launches fresh section calls (`tools/research-gate.sh:3425-3429`) and selects `verify-claims` at `:3546-3548`; this is not exercised by the C2 counter. Standalone claims-mode line fixtures do not establish binding, aggregation, or manifest behavior through that CLI. I did not run those modes and report no failure in them.
- **Other content/behaviors:** the generator uses lowercase ASCII vocabulary and space/newline separators (`c2-count.py:94,107-145`), every record declares `expect=supported` (`:279`), and runtime is only bounded (`claims-a2.md:111-112`). Neither arbitrary byte classes, contradiction markers, source-pin handling, nor universal runtime/no-harm behavior follows from this count. Other modes and semantics are explicitly not claimed (`claims-a2.md:111-112`).

**Sizing conclusion for the decision owner:** the measured after-state is cheaply re-derivable and the do-nothing baseline cannot reach it. The constant change is a genuine, minimal operational improvement. Nevertheless, the frozen prose contract and capability wording overstate what the count covers; two within-window counterexamples are attached. Treating 37/37 as proof of the full contract would erase an observed defect, not resolve a harmless tradeoff. This review supplies no admission or saturation verdict.

## Commands, receipts, limits

`timeout 30s df -h /fast` succeeded before cloning; 38 GiB available. Clone/check-out commands used `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE`, local source only, pinned revision above; all setup commands exited **0** after an initial invocation was rejected because its requested cwd did not yet exist (no command executed on that rejection). Gate/counter `sha256sum` checks exited **0** and matched the pins above.

The actual aggregate probe command was:

```sh
timeout 900s python3 /fast/scratch/hyaku/chousa-r34-a2/w2/CritC2AxisFit/probe.py
```

It exited **0** after **122.79 seconds**; each gate/counter/audit invocation had an additional **180-second** timeout. Counter commands are exactly `python3 "$F/corpus/evidence/round34/c2-count.py" --gate GATE --seed SEED --receipt RECEIPT`; audit command is `python3 "$F/corpus/evidence/round34/self-audit.py" --lane "$F"`, with timeout wrappers as recorded in **E/commands.json**. Probe source is preserved as **E/probe.py**, SHA-256 `b7b7ea1fa7a78041156476477c831fce9afb1cf0ecd26ec1fb5060fa76592ddb`.

Original four landed C2 seed receipts were inspected/catalogued, **not independently re-run** here; two new landed seeds and one paired before run were executed instead. No full selftest, no-harm battery, quote-anchor run, verify-all run, held C1 control, or whole-round admission check was performed. Audit reproduction is not a semantic audit of all self-description. Every retained artifact is under this seat's E directory and below 1 MiB; fixture source files are about 33 KiB each. No tool installs or updates.
