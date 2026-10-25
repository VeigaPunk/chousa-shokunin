# ScribeGatesR24to27 — draft Gates rows for the round-24..27 instruments

Item: draft SKILL.md `## Gates` rows (8 cells, one row per instrument family) for the ten
unregistered round-24..27 instruments, stating each real entry, exit contract and write scope,
with observed values from one read-only run each.

Lane state for every run: HEAD `c2f0e9d100c0d46633a6277b2fd51d2ac99678eb`,
`tools/research-gate.sh` sha256 `2cb04bddfd5601d7c113a9b532a25895ce475847ff65f5672afc22586f5ffc34`.
No lane file was written by any run; outputs went to `/tmp/chousa-r46-ScribeGatesR24to27/`.
`git status --porcelain` was 8 lines before and 14 after — every added entry is a peer's
(`corpus/evidence/round46/*`, `corpus/knowledge/evidence-pool-versioning-r39*.md`,
`tools/inference-ground.py`); none is mine. No listed script has a receipt option that writes
into the lane, so no bytes needed snapshotting or restoring (`--output` on the two r27 controls
was omitted).

Instrument digests (sha256, first 16): round24-measure `2b0543be90a81c67`,
round25-measure `a878e14faa7e6b66`, round25-ledger-recount `5578919127795145`,
round25-meta-differential `e07761fe81e6ff4c`, round26-measure `b51c96f63a36bfe0`,
round26-date-differential `bb8f7f44871b1ac5`, round26-registry-differential `852a764870f71e72`,
round27-mechanisms `2c2f95710b0e776f`, round27-regressions `5afea7863f2b052b`,
round27-falsify-controls `ab9462e1d6874575`.

## Commands and verbatim results

1. `python3 corpus/evidence/round25-ledger-recount.py` → RC=0
```
rows=71 by-design=38 carried=22 closed=8 finding=0 operator=3 sum=71 queue_committed=24 queue_true=25
```
2. `python3 corpus/evidence/round27-mechanisms.py tools/research-gate.sh` → RC=0
```
"kind": "source-mechanism-probe-not-verdict", "sha256": "2cb04bddfd56...", counts C1_faulty_usage_substring 0,
C2_locale_unpinned_date_validator 0, C2_recursive_zero_strip 0, C3_stale_candidate_columns 0,
C3_consumed_text_rescan 0, C3_pointer_predicate_on_registry_path 0; claim_totals C1/C2/C3 = 0
```
3. `bash corpus/evidence/round25-meta-differential.sh` → RC=0
```
AGREE=54/54 (fixtures=27, modes normal+strict)
```
4. `bash corpus/evidence/round24-measure.sh .` (lane root as tree) → RC=0
```
== tree /home/vgpnk/Projects/shokunin/chousa-shokunin gate 2cb04bdd
MANIFEST_LINES=2 INVALID_JSON_LINES=0
VERDICT_BEARING_EXPORTS=3/3
  corpus/knowledge/claim-support-states-r24.md admitted=1 ids=S006 S007
  corpus/knowledge/citation-chain-fidelity-r24.md admitted=1 ids=S003 S005
  corpus/knowledge/contextual-source-admission-r24.md admitted=1 ids=S002 S003 S004
EXPANSION_ADMITTED=3/3
rows: 84 / malformed: 0 / tiers: A=78 B=1 C=5 / status: mined=60 queued=19 rejected=5
dup-ids: [] / enum/inflation: [] / missing-used-by: [] / sections: 4/4
MISTAKE_CLASSES=14 CAPTURED_BY_CRITERION=14 UNCAPTURED=0 (bar: corpus/QUALITY.md)
```
5. `bash corpus/evidence/round25-measure.sh .` → RC=1
```
verify-metadata rc=1
METADATA_COMPLETE=25/28
RESEARCH_GATE: DRIFT (entries=28 complete=25 findings=33 drift=3)
META_NAMED_DRIFT_ENTRIES=[entry=archives-verified-r9.md entry=audit-r11.md entry=gate-baseline-r8.md]
2a UNINDEXED=0 [] / 2b FRONTIER_MISSING=0 rounds=[] / 2c EVIDENCE_MISFILED_ROWS=0
2d CAP_ROWS_MISSING=0 rounds=[] (LOG Capabilities +1 rounds=[13,...,23]) / STALE_INDEX_ITEMS=0
3a SKILL_OPEN_CLOSED_FINDING=0 / 3b SKILL_LEDGER_TUPLES_STALE=0 of 0 QUEUE_STALE=0 of 0
3c PLACEHOLDER_GSHA_UNRESOLVED=0 (historical raw slots=1) / 3d LEDGER_ADDENDA_MISSING=0 / STALE_RESTATEMENTS=0
RESEARCH_GATE_SELFTEST: PASS (275 cases, 0 skipped)
GATE_DRIFT: +resolvable drift
```
(stops at the drift line: `set -e` aborts before the r1 `VERDICT_BEARING_EXPORTS` echo)
6. `bash corpus/evidence/round26-measure.sh . all` → RC=0
```
tree=... gate_sha256=2cb04bdd... base=ba333325... as_of=2026-10-21
ctl rc=0 maxrss_kb=11892 elapsed_s=0.0
s1-newlines bytes=8388000 rc=1 maxrss_kb=55476 extra_kb=43584 elapsed_s=86.4 bounded
s2-header-body bytes=8388000 rc=0 maxrss_kb=55684 extra_kb=43792 elapsed_s=0.1 bounded
s3-crlf bytes=8388000 rc=1 maxrss_kb=55292 extra_kb=43400 elapsed_s=46.2 bounded
s4-header-noheading bytes=8388000 rc=0 maxrss_kb=56064 extra_kb=44172 elapsed_s=59.7 bounded
C1_AMPLIFIED=0/4
C1_FROZEN_RC=1 C1_FROZEN_SHA=3f83ba4844cac8d2057b47661be225f84a5945fc7c1db739ec2070b6aa2a4a37
C2_ORACLE_AGREE=29/29 / C2_ORACLE_DIST {'unknown': 24, 'current': 4, 'event': 1} / C2_CONTROLS_CAUGHT=6/6
C3_CONTROLS_CAUGHT=5/5 / C3_POSITIVE_CLEAN=1/1 / C3_POP_R24PLUS_CLEAN=5/5
RESEARCH_GATE_SELFTEST: PASS (275 cases, 0 skipped)
LEGACY_CASES_SHA=5eac4a7e2af964f6e81631f66990426e5c8ef58fb41ba6ec6d0054ef819e01cb
GATE_DRIFT: +resolvable drift / drift rc=1 / VERDICT_BEARING_EXPORTS=3/3
```
7. `bash corpus/evidence/round26-date-differential.sh` → RC=0 (55.0 s)
```
DATE_DIFF_AGREE=9024/9024
```
8. `bash corpus/evidence/round26-registry-differential.sh` → RC=0
```
OUT_OF_CONTRACT_ESCAPED_PIPE=excluded (CORPUS contract v1 forbids | inside a cell)
REGISTRY_DIFF_SUITE=r24plus 5/5 / REGISTRY_DIFF_SUITE=pop29 29/29 / REGISTRY_DIFF_SUITE=adversarial 14/14
REGISTRY_DIFF_AGREE=48/48
```
9. `python3 corpus/evidence/round27-regressions.py --gate tools/research-gate.sh` → RC=0
```
"gate_sha256": "2cb04bdd...", "total": 58, "mismatches": 0, claims C1{6,0} C2{21,0} C3{31,0}
```
10. `python3 corpus/evidence/round27-falsify-controls.py --gate tools/research-gate.sh` → RC=1
```
"gate_sha256": "2cb04bdd...", "total": 32, "mismatches": 2, claims C1{5,0} C2{8,0} C3{19,2}
MISMATCH C3 source-scanner-fault--oE ../residual/ResTokenPrefilter missing 'META_SOURCE_SCAN_FAILED'; count '^FINDING META_SOURCE_SCAN_FAILED\b': 0 != 1
MISMATCH C3 source-scanner-fault--xE ../residual/ResTokenPrefilter missing 'META_SOURCE_SCAN_FAILED'; count '^FINDING META_SOURCE_SCAN_FAILED\b': 0 != 1
```

## Finding: the two r27 falsify mismatches are a superseded control, not a gate defect

The control injects a `grep` shim on `PATH` that exits 2 for `-oE`/`-xE`. Since round 35 the
gate resolves one pinned binary (`GATE_GREP`, default `/usr/bin/grep`; `tools/research-gate.sh:416-493`),
so a `PATH` shim is invisible. Lane probes (today, gate `2cb04bdd`):

- queue row + `PATH` shim → `FINDING META_SOURCE_NOT_MINED severity=warn ... registry row is not mined`, RC=1,
  no `META_SOURCE_SCAN_FAILED`; mined row whose `used-by` does not name the entry →
  `FINDING META_SOURCE_USEDBY_MISSING severity=warn`, RC=1.
- the same shim under `RESEARCH_GATE_GREP=` → `FINDING META_SOURCE_SCAN_FAILED severity=crit surface=metadata
  obs=entry=entry.md source-id scanner failed; registry relationship unknown`, RC=1.

So `FINDING META_SOURCE_SCAN_FAILED` still exists (`tools/research-gate.sh:3425`); only the injection
route died. The r27 family is therefore honest at `30/32` on this gate and the control is superseded
as written — a follow-up owner should re-express it via `RESEARCH_GATE_GREP`. Recorded as a finding,
not repaired (out of scope: these are production files).

## Draft rows (verbatim, for insertion into `## Gates`)

```
| `chousa round-24 counting probe` | probe | `bash corpus/evidence/round24-measure.sh <tree-root> [<bar-QUALITY.md>]` | exit `0` every measurement completed (probe — exit `0` is NOT admission; reconcile the printed values against SCORECARD); exit `1` tree root unreadable (`cd "$R"` fails) or an uncaught `set -u` expansion when the argument is absent (`${1:?tree root}`); no exit `2` path | control: the pre-round bar `git archive ab19cff` yields `EXPANSION_ADMITTED=0/3` and `CAPTURED_BY_CRITERION=3/14`, and the pre-fix gate yields `MANIFEST_LINES=1 INVALID_JSON_LINES=1` (SCORECARD round-24 before cells) where the landed tree yields `MANIFEST_LINES=2 INVALID_JSON_LINES=0` | SCORECARD round-24 cells bound to `json-r24-20261019T213117Z-demo.log`; observed at lane `c2f0e9d` gate `2cb04bdd` exit `0`: `MANIFEST_LINES=2 INVALID_JSON_LINES=0`, `VERDICT_BEARING_EXPORTS=3/3`, `EXPANSION_ADMITTED=3/3`, `MISTAKE_CLASSES=14 CAPTURED_BY_CRITERION=14 UNCAPTURED=0`, registry `rows: 84 malformed: 0 tiers: A=78 B=1 C=5 status: mined=60 queued=19 rejected=5`, `sections: 4/4` (the round-24 census read `18 rows`) | read-only; one `mktemp -d` manifest removed on exit; no receipt option; `SHOKUNIN_ROOT` only chooses the r1 archive root | chousa |
| `chousa round-25 counters and differential` | probe | `bash corpus/evidence/round25-measure.sh <tree-root>` · `python3 corpus/evidence/round25-ledger-recount.py` (lane root) · `bash corpus/evidence/round25-meta-differential.sh` (lane root) | measure: exit `0` all measurements completed, exit `1` any `set -e` failure including the closing `--drift` line (observed `GATE_DRIFT: +resolvable drift`), exit `2` missing population member; ledger-recount: exit `0` iff 71 §3 rows parse and it prints `rows=71 …`, exit `1` on its `SystemExit` message (expected 71 parsed N); meta-differential: exit `0` `AGREE=54/54 (fixtures=27, modes normal+strict)`, exit `1` any `DISAGREE` or empty differential, exit `2` setup | the 27-row `corpus/fixtures/metadata-r25/README.md` table plus the independent stdlib oracle `corpus/evidence/round25-meta-oracle.py` are the control (gate and oracle must both equal the hand-derived row); the ledger recount is its own control — deleting one §3 row makes it report a parsed count below 71 and exit `1`; measure's before-cell is `git archive d730ae4` (SCORECARD: absent-mode rc2, 66 stale index items, 15 restatements) | SCORECARD round-25 cells, `corpus/evidence/round25-measured-revision.json` at `c125d8bc…`, receipts `round25-landed-measure.log` and `round25-landed-differential.log`; observed at lane `c2f0e9d` gate `2cb04bdd`: measure exit `1` with `METADATA_COMPLETE=25/28`, `META_NAMED_DRIFT_ENTRIES=[archives-verified-r9.md audit-r11.md gate-baseline-r8.md]`, `STALE_INDEX_ITEMS=0`, `STALE_RESTATEMENTS=0`, `RESEARCH_GATE_SELFTEST: PASS (275 cases, 0 skipped)`, `GATE_DRIFT: +resolvable drift`; recount exit `0` `rows=71 by-design=38 carried=22 closed=8 finding=0 operator=3 sum=71 queue_committed=24 queue_true=25`; differential exit `0` `AGREE=54/54` | read-only: measure and differential write only `mktemp -d` trees, recount reads `corpus/knowledge/hardening-r10.md`; none takes a receipt option | chousa |
| `chousa round-26 probes and differentials` | probe | `bash corpus/evidence/round26-measure.sh <tree> [PART: c1, c2, c3, holds or all]` (needs `git` and base `ba333325…`) · `bash corpus/evidence/round26-date-differential.sh [<gate.sh>]` · `bash corpus/evidence/round26-registry-differential.sh [<gate-tree>]` | measure: exit `0` every part ran (probe — compare values to `corpus/evidence/round26-claims.md`), exit `2` usage, missing gate, incomplete frozen population or unknown part, exit `1` any `set -euo pipefail` failure (its closing `--drift` may supply it); date-differential: exit `0` `DATE_DIFF_AGREE=9024/9024`, exit `1` any mismatch (`DISAGREE …` on stderr) or an empty differential, exit `2` usage or gate-not-found; registry-differential: exit `0` `REGISTRY_DIFF_AGREE=48/48`, exit `1` any `DISAGREE`, duplicate or missing suite, exit `2` non-directory tree, missing gate or unavailable frozen base | expectations are independently derived, never from gate output: date arithmetic from Python `datetime` over `DAY_COUNTS` and years 1900-2100, registry from `corpus/evidence/round26-registry-oracle.py` across three frozen suites (`REGISTRY_DIFF_SUITE=r24plus 5/5`, `pop29 29/29`, `adversarial 14/14`), C1 from the `ctl rc=0 maxrss_kb=11892` baseline against the amplified shapes | SCORECARD round-26 cells at gate `c2c813f1…`: `C1_AMPLIFIED=4/4 → 0/4`, `C2_ORACLE_AGREE=29/29`, controls `6/6`, `C3_CONTROLS_CAUGHT=5/5`, registry `48/48`, date `9024/9024` — C2 and C3 were falsified beyond those frozen controls (`.ufo/waves/round-26/falsify/`), so their frozen agreement is not grammar equivalence; observed at lane `c2f0e9d` gate `2cb04bdd`: measure exit `0` `C1_AMPLIFIED=0/4`, `C1_FROZEN_RC=1`, `C1_FROZEN_SHA=3f83ba48…`, `C2_ORACLE_AGREE=29/29`, `C2_CONTROLS_CAUGHT=6/6`, `C3_CONTROLS_CAUGHT=5/5`, `C3_POSITIVE_CLEAN=1/1`, `C3_POP_R24PLUS_CLEAN=5/5`, `RESEARCH_GATE_SELFTEST: PASS (275 cases, 0 skipped)`, `GATE_DRIFT: +resolvable drift`, `VERDICT_BEARING_EXPORTS=3/3`; date exit `0` `DATE_DIFF_AGREE=9024/9024`; registry exit `0` `REGISTRY_DIFF_AGREE=48/48` | read-only: measure and registry differential use `mktemp -d` (`/tmp/r26m.*`, `/tmp/chousa-r26-registry-diff.*`), date differential a Python `tempfile` dir; no receipt option | chousa |
| `chousa round-27 mechanism probes and contract controls` | check | `python3 corpus/evidence/round27-mechanisms.py <gate.sh>` · `python3 corpus/evidence/round27-regressions.py --gate PATH [--output OUT.json]` · `python3 corpus/evidence/round27-falsify-controls.py --gate PATH [--output OUT.json]` | mechanisms: exit `0` the counts printed under `kind: source-mechanism-probe-not-verdict` (never a verdict), exit `1` `SystemExit('missing production function: <name>')`, no exit `2` path; regressions and falsify: exit `0` `mismatches: 0` across all controls, exit `1` any `MISMATCH` line with summary `mismatches: N`, exit `2` argparse/setup (gate is not a regular file) | expectations come from frozen claims, Python `datetime` and GFM table rules, not gate output; the falsify controls name their reports under `.ufo/waves/round-27/falsify/`; two of them (`source-scanner-fault--oE`, `--xE`) are SUPERSEDED as written by the round-35 grep pin — a `PATH` shim is bypassed, and the same shim under `RESEARCH_GATE_GREP=` restores exactly one `FINDING META_SOURCE_SCAN_FAILED severity=crit` (lane probe 2026-10-25); replacement route: the grep-pin cases of `bash tools/research-gate.sh --selftest` and `corpus/evidence/round35/c1-count.py` | SCORECARD and LOG round-27 at gate `ac1315dd…`: `regressions → 58 controls, 0 mismatches (C1=6, C2=21, C3=31)`, `falsify-controls → 32 controls, 0 mismatches (C1=5, C2=8, C3=19)`, `mechanisms → C1=0 C2=0 C3=0` versus the non-executing base `1/2/5`; observed at lane `c2f0e9d` gate `2cb04bdd`: mechanisms exit `0`, all six counts `0`; regressions exit `0` `total: 58, mismatches: 0`; falsify exit `1` `total: 32, mismatches: 2` (both C3 scanner-fault cells) | a `tempfile.TemporaryDirectory` (`chousa-r27-synthetic-*`) only; `--output` writes a summary JSON wherever it is pointed and was omitted here | chousa |
```

## Notes, limits, out of scope

- Exit codes are the scripts' own; none of these is an admission gate. `round24/25/26-measure`
  self-declare probe semantics, so their `0` is "ran", and `round25-measure`'s `1` today comes from
  a moved r12 drift baseline, not from a failed claim count — the row says so explicitly.
- The round-26 and round-27 pinned values belong to gates `c2c813f1…` and `ac1315dd…`; today's
  readings are at `2cb04bdd…`, so any later edit must keep both columns distinguishable.
- Round-24's registry census is now `84 rows` (round 24 recorded 18): value drift in a read-only
  census, not a failure of the probe.
- Nothing was installed or upgraded; no network egress; no live target read.
- Out of scope (not performed): editing `SKILL.md`, repairing the r27 falsify control,
  re-registering the counters in `corpus/evidence/round46/c2-count.py`.
- Scratch `/tmp/chousa-r46-ScribeGatesR24to27/` removed before finishing.
