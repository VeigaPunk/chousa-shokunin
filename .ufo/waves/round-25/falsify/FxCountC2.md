# FxCountC2 — independent Claim 2 count reproduction

## Scope and checkpoint
- Used a private clone at corrected full checkpoint `e93ac711f885a10d44fdd80a1734997419595b5a` (observed HEAD); its `tools/research-gate.sh` SHA-256 prefix is `63a39282`. Separately unpacked base `d730ae4c33989ad9c8535764d4cae77b4db869f6` with `git archive` into `/tmp`.
- Per L1 checkpoint corrections: `0fc037e` omitted the gate helper; `d8c8cff` fixed that but omitted `corpus/evidence/README.md`; the complete e93 pin was used for the after-run. No measurements were made against the incomplete intermediate pins.
- Ran the same `corpus/evidence/round25-measure.sh` from the e93 private clone against both tree roots; no production/code edits.

## Reproduction
Base (`d730ae4`; command `bash /tmp/chousa-r25-FxCountC2/corpus/evidence/round25-measure.sh /tmp/chousa-r25-FxCountC2-d730ae4`; `MEASURE_RC=0`):
```text
2a UNINDEXED=2 ['knowledge/audit-r11.md', 'lessons/2026-10-19-hardlink-alias-boundary.md']
2b FRONTIER_MISSING=13 rounds=[11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
2c EVIDENCE_MISFILED_ROWS=43
2d CAP_ROWS_MISSING=8 rounds=[15, 17, 18, 19, 20, 21, 22, 23] (LOG Capabilities +1 rounds=[13, 14, 15, 17, 18, 19, 20, 21, 22, 23])
STALE_INDEX_ITEMS=66
```
Matches committed `round25-measure-before.log:5-10`. Holds: selftest `PASS (136 cases, 0 skipped)`, `GATE_DRIFT: none` (`drift rc=0`), `VERDICT_BEARING_EXPORTS=3/3` (baseline log lines 17-21).

Full e93 checkpoint (`bash /tmp/chousa-r25-FxCountC2/corpus/evidence/round25-measure.sh /tmp/chousa-r25-FxCountC2`; `MEASURE_RC=0`):
```text
2a UNINDEXED=0 []
2b FRONTIER_MISSING=0 rounds=[]
2c EVIDENCE_MISFILED_ROWS=0
2d CAP_ROWS_MISSING=0 rounds=[] (LOG Capabilities +1 rounds=[13, 14, 15, 17, 18, 19, 20, 21, 22, 23])
STALE_INDEX_ITEMS=0
```
Matches committed `round25-measure-after.log:40-45`. Holds: selftest `PASS (154 cases, 0 skipped)`, `GATE_DRIFT: none` (`drift rc=0`), `VERDICT_BEARING_EXPORTS=3/3` (after log lines 52-56).

## Finding
**P2 — C2's evidence/capability populations are self-enumerating, so zero does not establish index completeness.** The pre-registration claims a frozen population and describes 43 misfiled evidence rows plus 8 missing capability rows (`corpus/evidence/round25-claims.md:52-60`), but `round25-measure.sh:34-42` counts only misfiled rows it happens to read, and `:43-54` derives the capability-round population from the current `LOG.md`. Unlike `:27`'s explicit base-file list and `:31-32`'s fixed round range, neither 2c nor 2d pins an expected record/round inventory.

Concrete input-only counterexamples, made in disposable private clones of e93 (code unchanged):
- Empty `corpus/evidence/README.md`: the script reports `2c EVIDENCE_MISFILED_ROWS=0` and `STALE_INDEX_ITEMS=0`, `MUTANT_MEASURE_RC=0`; the 154-case selftest, drift hold, and 3/3 export hold still pass. Yet the real e93 index has receipt rows (e.g. `corpus/evidence/README.md:909-920`).
- Empty `LOG.md`: it reports `2d CAP_ROWS_MISSING=0 rounds=[] (LOG Capabilities +1 rounds=[])` and `STALE_INDEX_ITEMS=0`, `MUTANT_MEASURE_RC=0`; real e93 LOG entries include `Capabilities +1` at `LOG.md:585,607,626`.
- Missing `corpus/evidence/README.md`: the 2c Python block raises `FileNotFoundError`; the shell continues into claim 3 and holds, then exits `MISSING_INPUT_MEASURE_RC=0` without printing `STALE_INDEX_ITEMS`. `round25-measure.sh:8` has `set -u` but not `set -e`; the later commands at `:57-85` mask that failed count block's status.

This is a measurement/spec-population gap, not a falsification of the reproduced e93 counts on the present files: those counts match both committed logs. But the zero total can also describe wholesale loss of the two source populations, so it is not by itself evidence that the indexes/ledgers are complete.

## Residual risk and verification gaps
- `2a` and `2b` are protected against empty inputs by their explicit expected base-file list and fixed rounds; the vacuity observed is specific to 2c/2d's dynamic input sets.
- `lsp` device unavailable: `read xd://lsp` returned “No such tool” and listed mounted devices without LSP. Source inspection and execution above are not semantic LSP evidence.
- No tools installed. No full suite/build run beyond the explicitly assigned measurement script and its included holds.

VERDICT: Base and full-checkpoint Claim 2 counts reproduce exactly; C2's 2c/2d completeness claim remains vulnerable to empty or missing input populations.
