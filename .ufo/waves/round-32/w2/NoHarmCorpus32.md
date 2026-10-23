# NoHarmCorpus32 — corpus verdict stability (base vs landed)

Verdict: **HOLDS**. No Chain-table record flips. Every `verify-chain` summary gains only ` resolvable=0`. `verify` is timestamp-identical. Canonical `verify-all` verdict and counts do not flip; the manifest chain tally gains `"resolvable":0` only.

## Attack

Axes: (1) CLEAN/DRIFT and exit stability, (2) count stability except a new zero `resolvable` field, (3) `CHAIN` / `FINDING` line stability. A flip, a nonzero `resolvable`, or any other line change is harm.

Gates (scratch clones of `5d8a170795dcf48c3746a4f03dee9cfe32812834`; base script replaced from `7a7259f0ad41a68068131bfa422a829db9fd1b55:tools/research-gate.sh`):

- base `basegate/tools/research-gate.sh` SHA-256 `0bc318b3e74ac0ad45f4b34154e886d84aebf44673612afab6de5e0b0ff11258`
- landed `landed/tools/research-gate.sh` SHA-256 `10f2fe12043c6f1565c7d7b9446ee0c4dc11e9649aa3350dcab96f8a2ccb4098`

Scratch root: `/fast/scratch/hyaku/chousa-r32/w2/NoHarmCorpus32/`. Documented root: `cd chousa-shokunin && --root ..` is `/home/vgpnk/Projects/shokunin` (printed `fleet-parent=/home/vgpnk/Projects/shokunin`). Each run: `env -u CHOUSA_ROOT -u CHOUSA_RECORD -u CHOUSA_CLAIMS -u CHOUSA_STRICT -u CHOUSA_AGGREGATOR_ERE -u CHOUSA_NOW_EPOCH TMPDIR=…/tmp timeout 90 bash <gate> <mode> <record> --root /home/vgpnk/Projects/shokunin`, cwd = that gate's clone. Stdout/stderr/rc under `…/out/`. Runner `run-noharm.sh` wall 68.59s, ended `RUN_DONE`. No packages installed.

Inventory: 19 corpus markdown files with a line that strips to `## Chain` (python walk). `git diff --quiet 7a7259f0ad41a68068131bfa422a829db9fd1b55 5d8a170795dcf48c3746a4f03dee9cfe32812834 -- corpus/fixtures corpus/knowledge/archived-export-intake.md` exit 0. Scratch trees: `only-landed 0 only-basegate 0 shared-byte-mismatch 0` excluding the swapped gate. `gate_pin_fixture` bodies identical (`pin-fixture-fn-identical True`, 1685 chars).

## Evidence

19/19 `verify-chain`: after masking `ts=`, landed stdout equals base with ` resolvable=0` inserted before the `RESEARCH_GATE` closing paren. Exit codes match. `CHAIN` lines, `FINDING` lines, and `RESOLVED_HOPS=` match. Landed corpus runs: 117 `CHAIN` lines, `observed=resolvable` count 0, no `CHAIN_EXEMPT_RESOLVABLE`. Stderr empty.

| record | rc | landed summary (base is that line without ` resolvable=0`) |
|---|---|---|
| chain-r3.md | 0 | CLEAN hops=22 verified=17 exempt=5 anchor-missing=0 refused=0 invalid=0 findings=0 drift=0 resolvable=0 |
| chain-r3-broken.md | 1 | DRIFT hops=2 verified=1 exempt=0 anchor-missing=1 findings=1 drift=1 resolvable=0 |
| full-r6.md | 0 | CLEAN hops=3 verified=3 exempt=0 resolvable=0 |
| full-r6-broken.md | 1 | DRIFT hops=3 verified=2 exempt=0 anchor-missing=1 findings=1 drift=1 resolvable=0 |
| full-r6-absent.md | 0 | CLEAN hops=1 verified=1 resolvable=0 |
| integrity-r7.md | 0 | CLEAN hops=4 verified=4 resolvable=0 |
| integrity-r7-broken.md | 0 | CLEAN hops=4 verified=4 resolvable=0 |
| sweeps-r5.md | 0 | CLEAN hops=3 verified=2 exempt=1 resolvable=0 |
| sweeps-r5-broken.md | 0 | CLEAN hops=1 verified=1 resolvable=0 |
| archives-r9/A-r9.md | 0 | CLEAN hops=7 verified=6 exempt=1 resolvable=0 |
| archives-r9/B-r9.md | 0 | CLEAN hops=7 verified=6 exempt=1 resolvable=0 |
| archives-r9/C-r9.md | 0 | CLEAN hops=8 verified=7 exempt=1 resolvable=0 |
| controls/A-r9-anchor-missing.md | 1 | DRIFT hops=7 verified=5 exempt=1 anchor-missing=1 findings=1 drift=1 resolvable=0 |
| controls/A-r9-span-not-found.md | 0 | CLEAN hops=7 verified=6 exempt=1 resolvable=0 |
| controls/B-r9-false-sweep.md | 0 | CLEAN hops=7 verified=6 exempt=1 resolvable=0 |
| controls/B-r9-rejection-missing-flip.md | 0 | CLEAN hops=7 verified=6 exempt=1 resolvable=0 |
| controls/C-r9-dangling-ref.md | 0 | CLEAN hops=8 verified=7 exempt=1 resolvable=0 |
| controls/C-r9-structure-break.md | 0 | CLEAN hops=8 verified=7 exempt=1 resolvable=0 |
| knowledge/archived-export-intake.md | 1 | DRIFT hops=8 verified=0 exempt=4 invalid=4 findings=4 drift=4 resolvable=0 |

Intake DRIFT is on both gates (H1-H3 and H8 `CHAIN_CITATION_INVALID`, obs `resolved hop missing anchor`). Not a flip. H4/H5/H6 stay `observed=exempt`.

19/19 `verify`: stdout identical after the `ts=` mask; exits match (18 times rc 0; `C-r9-structure-break.md` rc 1 on both). Example, both gates: `RESEARCH_GATE: CLEAN (findings=0 drift=0 questions=1 sources=3 chains=22 claims=2 negatives=0 rejections=1 approvals=1)`.

Canonical record: the selftest/pin header names no corpus path. Canonical invocation is `verify-all record.md --claims claims.jsonl --json manifest.jsonl --root .` on the fixture `gate_pin_fixture` writes. Materialized at `…/canon/` (outside both lane roots) and run on both gates; also `--pin` to scratch. Both `verify-all` rc 1, stderr 0, stdout identical after `ts=` mask: chain `RESOLVED_HOPS=1/1` CLEAN, integrity DRIFT `refs=4 resolved=3 unresolved=1`, `VERIFY_ALL … drift-sections=1 findings=1 drift=1`, `RESEARCH_GATE: DRIFT (sections=5 run=5 absent=0 drift-sections=1 findings=1 drift=1)`. JSON `base-canon.jsonl` vs `landed-canon.jsonl`: same verdict DRIFT, same record sha256 `c22a6c3d8acf345a4b2a5b9b8ece388c596648cee84c7f9ba3002a75a95f3f84`; the only tally delta is chain `resolvable` absent to `0`. `--pin` rc 0 both (`GATE_PIN: ok`). Pin bodies differ only in volatile `gate_sha256` / `pinned_ts` and that same chain tally key.

## Limits

Did not run `--selftest` or the C1/C2 counters. Scratch lane roots are device 66309 and the fleet root is device 56; cited `research/…` hops still verified (`at=line:…`), so the split did not refuse those reads. Lane-relative bytes cannot diverge: the two clones match aside from the gate file.
