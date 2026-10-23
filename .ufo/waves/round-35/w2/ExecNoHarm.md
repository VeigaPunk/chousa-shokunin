# ExecNoHarm — independent no-harm battery

Access date: 2026-10-23. Axes: **operability** (exit/output stability), **calibration** (revision-bound counter evidence).

## Verdict

**Assigned battery PASS on the requested e87c5d7ea2dbf3730b36a3961de3f06261d015e4 snapshot.** All 14 battery rows have the expected exits/results. All 14 output logs equal the pre-round gate's logs after masking only banner timestamps. No changed verdict, finding, tally or case line was observed. Raw fixture logs do differ in their first-line timestamps; these differences are reported, not silently called byte-identical.

The supplied pre-round gate already has **256**, not 253, cases. Both gates pass all 256, and **all 256 case lines and the complete selftest logs are byte-identical**. Thus the requested first-253 comparison holds more strongly.

This is a scoped no-harm result, not a full admission or an independent two-seed C1/C2 judgment. No production implementation files changed.

## Revision and evidence custody

Primary scratch: `/tmp/hyaku/chousa-r35/w2/ExecNoHarm/` (abbreviated `S` below).
Retained artifacts: `.ufo/waves/round-35/w2/ExecNoHarm/` (abbreviated `E` below).
`E/manifest.json` records exact SHA-256 and byte size for every retained source artifact; each is under 1 MiB. `E/comparison.json` records all 14 timestamp-masked comparisons.

| Gate | Revision/custody | SHA-256 |
|---|---|---|
| Assigned landed gate | `S/landed`, checkout `e87c5d7ea2dbf3730b36a3961de3f06261d015e4` | `1f2fb4f522d9a670b49dd61ad1369f55ee012f3b0d38050654be45a71aaef617` |
| Named pre-round control | Second checkout at the same revision, replacing only `base/tools/research-gate.sh` with the supplied `repairs/base-gate.sh` | `a6307edf687ac0fb1b0b08bf7f0518b3fbc310fa9924b970aa3654612562995b` |
| Supplemental later-tip snapshot | Third checkout `b6f2c0db8de4047e6518f4232da2fd3c3954cf00` | `a47688518e509edbf43b433a5e16e1cf2481233f3acedb5824ba341f7f0c38ad` |

The supplemental gate is **not** substituted for the assigned measurement. The live lane had advanced during this run; the recorded third checkout is the only later-tip snapshot measured here. No assertion is made about subsequent revisions.

## Commands and one row per check

The retained `E/battery.sh` is adapted from the existing round-34 battery, not a new counter convention. Its full invocation, run from `S`, was:

```bash
SCRATCH=$S/tmp timeout -k 5 3600 bash battery.sh \
  $S/landed/tools/research-gate.sh $S/landed $S/out \
  /home/vgpnk/Projects/shokunin $S/obsroot/chousa-shokunin
```

Here `$S` denotes the absolute scratch path above (the actual call used literal absolute paths). Exit **0**, `ROWS=14`, `BATTERY_RESULT=PASS`. Exact expanded commands, cwd, row timeouts, exits, key output and per-log hashes are in `E/logs/battery.out` (SHA-256 `0f82a74fe4369f0eab07b565d621ae7bfc58baea0b180b29c18d816344d4086d`).

All table paths below are under `E/out/`. Counter commands follow `python3 corpus/evidence/ROUND/COUNTER --gate GATE --seed N --receipt PATH`; every counter receipt names the full primary gate hash above and has `predicate_holds=true`.

| Check | Exit | Observed result | Exact retained evidence |
|---|---:|---|---|
| Landed `bash tools/research-gate.sh --selftest` | 0 | PASS 256; 0 skipped; 0 FAIL-case lines | `selftest.log`, `selftest.cases` |
| Claims fixture `verify-claims corpus/fixtures/claims-r2.jsonl --root /home/vgpnk/Projects/shokunin` | 0 | 17/17 CLEAN; 13 supported, 2 contradicted, 2 unsupported | `claims-fleet-root.log` |
| Claims lane-root diagnostic, same file with `--root .` | 1 | 0/17 DRIFT; refused=17, matching base | `claims-lane-root.log` |
| Chain `verify-chain corpus/fixtures/chain-r3.md`, fleet root | 0 | 17/22 CLEAN; exempt=5 | `chain-r3.log` |
| Broken chain `verify-chain corpus/fixtures/chain-r3-broken.md`, fleet root | 1 | 1/2 DRIFT; anchor-missing=1 | `chain-r3-broken.log` |
| Exact SCORECARD round-1 counting command | 0 | VERDICT_BEARING_EXPORTS=3/3 | `observable.log`; expanded command in `E/logs/battery.out` |
| r31 C1 `c1-count-v3.py`, seed 3901 | 0 | LINE_BINDING_MATCH=132/132 | `r31-c1-v3.log`, `.json` |
| r31 C2 `c2-count-v3.py`, seed 3902 | 0 | REVISION_BINDING_MATCH=132/132 | `r31-c2-v3.log`, `.json` |
| r32 C2 `c2-count-v2.py`, seed 3903 | 0 | EXEMPT_AUDIT_MATCH=132/132; RECORD_CHECKS=ok | `r32-c2-v2.log`, `.json` |
| r33 C1 `c1-count-v2.py`, seed 3904 | 0 | TOPLEVEL_FIELD_MATCH=156/156 | `r33-c1-v2.log`, `.json` |
| r32 C2 `c2-count-v3.py`, seed 3905 | 0 | EXEMPT_AUDIT_MATCH=132/132; RECORD_CHECKS=ok | `r32-c2-v3.log`, `.json` |
| r34 C2 `c2-count.py`, seed 3906 | 0 | DEADZONE_MATCH=37/37 | `r34-c2.log`, `.json` |
| Additional original r31 C1 `c1-count.py`, seed 3907 | 0 | LINE_BINDING_MATCH=120/120 | `r31-c1-v1.log`, `.json` |
| Additional original r31 C2 `c2-count.py`, seed 3908 | 0 | REVISION_BINDING_MATCH=120/120 | `r31-c2-v1.log`, `.json` |
| Pre-round gate standalone selftest | 0 | PASS 256, 0 skipped | `E/logs/selftest-base.log` |
| First 253 case-line comparison (`diff` of first 253 extracted lines) | 0 | No changed lines | Full case lists retained under `E/out/` and `E/out-base2/`; full lists have the same SHA-256 below |
| Complete selftest log comparison (`diff`) | 0 | No changed lines, including all 256 cases | Both full logs SHA-256 `5311643cc95e6358a9fd513ec8ba67b944617e7d7da2f8df1c4d33d1f0c75c12` |

Full case-list SHA-256: `f39309655fa554bb501c14f02b2a5aec7f2bb9f29171de33ffb3908037266e8d` (base, primary and supplemental tip).

Claims/chain use the existing fleet-root convention because fixture sources are `research/deep-research-2026-09-28/...`. Using lane root is a known diagnostic refusal, not a new regression. The observable's exact SCORECARD command needs a sibling `../research`; its scratch mimic contains a checkout copy and a copied research tree. The mimic gate was hashed and equals the primary gate. No real lane gate was substituted for this observable run.

## Differential findings

- Base repeat: same battery invocation with `base`, `out-base2`, `tmp-base`, `obsroot-base/chousa-shokunin`; exit **0**, 14/14 expected rows. `E/logs/battery-base2.out` SHA-256 `a4c6c4eddf9973b71d78e37b38afc27d09ba49a9a53f6b4b9b2b5a6e2f8b1960`.
- Every row's output matches base after replacing only `ts=[0-9T:-]+Z`. Raw claims-lane-root, claims-fleet-root, chain-r3 and broken-chain logs differ in their timestamp-bearing first line; no other output line differs. Counter stdout, observable stdout and complete selftest logs are byte-identical.
- Supplemental later tip: same 14-row battery at the pinned `b6f2c0d` snapshot; exit **0**, all expected results, all output logs equal the primary snapshot after that same timestamp mask. `E/logs/battery-tip.out` SHA-256 `9d2aa1d2b271996e9b3f7002111c08e0ed9e82ceda209e548ed9739c165b5852`. Receipts under `E/out-tip/` identify the different full gate hash; they are not primary-wave receipts.
- Gate source changes between base and primary are retained in `E/logs/gate-diff.txt`: grep pin addition, `slen` declaration split and two selftest comment-range corrections. No new selftest case was added by that diff. [INFERENCE] Pin-specific regression protection therefore depends on the separate C1 battery rather than new selftest cases.

## Supplementary round-35 re-derivation

These are one-seed checks only, not the frozen two-fresh-seed acceptance:

- From `S`, `timeout -k 5 900 python3 landed/corpus/evidence/round35/c1-count.py --gate landed/tools/research-gate.sh --seed 3951 --receipt S/out/r35-c1-s3951.json`: exit **0**, GREP_PIN_MATCH=9/9, predicate true, primary gate hash. Log: `E/logs/r35-c1-s3951.log`.
- From `S/landed`, `timeout -k 5 1800 python3 corpus/evidence/round35/c2-count.py --gate tools/research-gate.sh --seed 3952 --receipt S/out/r35-c2-s3952.json`: exit **0**, WITNESS_SEPARATED=2/2, OUTPUT_EQUIV=2/2, LANDED_WITNESS=pass. K1/K2 each output 9/9 and witness fail (chunk stamps=0, direct=1). Log: `E/logs/r35-c2-s3952.log`; receipt in `E/out/`.

No witness bypass or non-oracle C1 MEETS engine was built in this scoped battery assignment.

## Setup errors, limits and procedural qualifications

- The first base mimic lacked `../research`, producing observable 0/3 and aggregate exit 1. That was a setup artifact, not a gate regression. After copying research, a direct observable rerun printed 3/3 (exit 0); the complete retained base repeat then passed. The initial aggregate transcript is retained as `E/logs/battery-base.out`; it must not be used as harm evidence.
- A first supplementary C2 invocation used scratch-parent cwd without an explicit `--battery`, producing battery=absent (exit 1). The witness file existed in the checkout; rerunning from its lane root gave the result above. The corrected receipt/log overwrote that first attempt's path; the initial output remains in the session transcript, not a separate retained file.
- The composite shell wrapper used a 3600-second timeout, exceeding the requested 1800-second cap; individual selftests/counters were bounded at 1800/900 seconds and completed within it. The tool automatically backgrounded three composite invocations. These are procedural deviations, not an assertion of complete protocol compliance. No subagents were launched.
- Supplemental later-tip measurement and round-35 counters exceeded the original eight-item scope; they are clearly separated from assigned evidence.
- Required source reads were not completed in the prescribed first-read order. No LSP interface was exposed in this seat; no supported symbol refactor was attempted. No tools installed, no network, no production edits, no git/jj writes in the lane, no commit/push/deploy.
- One seed per historical counter; no claim of exhaustive semantic coverage. The no-harm finding applies to the exact pinned gates, fixture bytes, commands and environment recorded here. No blocker remains for this scoped assignment.

Files changed: this report and its exclusive `ExecNoHarm/` evidence directory only. Production tests/docs intentionally unchanged: investigation-only assignment.
