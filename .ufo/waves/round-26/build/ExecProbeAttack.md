# Round 26 — counting-probe attack (ExecProbeAttack-3)

- Scope: RUNS / calibration; no live-lane code changes. Preregistration read first: `corpus/evidence/round26-claims.md` §C1–C3 (lines 26–115).
- Private clone base observed: `f361d12e44687841e30ec35710ddb366c6f795e0`; frozen probe population base: `ba3333254dd337658a4f25e7a9471f9cf4e4567e`.
- C1 runs used a scratch copy of the probe with `n=1,000,000` bytes (four shapes, each <1 MiB); no 8,388,000-byte memory run was made. Probe basis: `corpus/evidence/round26-measure.sh` lines 51–83.

## Results

1. **C1, old line-materializing gate:** `R26_BASE_REPO=<clone> bash <clone>/round26-measure-small.sh <clone> c1` → `C1_AMPLIFIED=4/4`; shape RSS 270420/137968/138876/138204 KiB vs control 11880 KiB. Frozen hold was `rc=1`, SHA `3f83ba4844cac8d2057b47661be225f84a5945fc7c1db739ec2070b6aa2a4a37` (same as preregistration prefix). The reduced shapes still trip the counter.
2. **C1, bounded-but-skip-header mutant:** replaced only the header line-array fill with `lines=()` in the private gate, ran same command → `C1_AMPLIFIED=0/4` (the predicted after-value), but `C1_FROZEN_SHA=bbb0752a876928e0449f2eb9dc42fc6a0cb212110695521d84557128574b81c9`, `METADATA_COMPLETE=0/29`, `findings=87 drift=87`. This wrong gate passes the C1 amplification metric; the hash hold distinguishes it. Original reader block is at gate lines 2383–2387.
3. **C1 vacuous parse-failure mutant:** gate that always prints usage and exits 2 → `C1_AMPLIFIED=0/4`, all four shape rc=2, frozen rc=2 / empty-output SHA; the probe itself exits 1 because its final summary grep finds nothing. Thus the count alone can look like the predicted after-value, though the overall command fails.
4. **C2 off-by-one cadence mutant** (test-only adapter): probe output `FRESHNESS_CLASSIFIED=29/29`, `C2_ORACLE_AGREE=25/29`, `C2_CONTROLS_CAUGHT=3/6`. Classified count alone gives the after-value; the independent oracle and controls reject it.
5. **C2 current-for-overdue mutant** (test-only adapter): `29/29`, `29/29`, `4/6`. The frozen population has no overdue items (`C2_ORACLE_DIST`: unknown 24, current 4, event 1), so the population measures alone score after; overdue/date-past controls catch the error.
6. **C2 fields emitted even without `--as-of`** (test-only adapter): with `--as-of`, all registered values scored after: `29/29`, `29/29`, `6/6`. A direct no-flag call still printed `due=2027-01-17 freshness=current`. Probe C2 only invokes `--as-of` (`round26-measure.sh` lines 89–95, 164–171); this is a real probe blind spot against the specified no-flag byte-identity hold (preregistration lines 59–63, 107).
7. **C3 never emits `META_SOURCE_USEDBY_MISSING`** (test-only adapter): `C3_CONTROLS_CAUGHT=4/5`, `C3_POSITIVE_CLEAN=1/1`, `C3_POP_R24PLUS_CLEAN=5/5`.
8. **C3 treats queued as mined** (test-only adapter): same movement: `4/5`, `1/1`, `5/5`. Each mutant misses its targeted control; positive and population counts remain unchanged in these adapters. Control logic is `round26-measure.sh` lines 189–223.

## Vacuous-zero check and limits

- Base gate rejects unsupported `--as-of`/`--registry`: C2 printed `rc=2`, `FRESHNESS_CLASSIFIED=0/29`, `C2_ORACLE_AGREE=0/29`, `C2_CONTROLS_CAUGHT=0/6`, yet `c2_probe_rc=0`; C3 printed `0/5`, `0/1`, `0/5`, yet `c3_probe_rc=0`. The rc is visible, but the overall probe exits successfully with zeros (`round26-measure.sh` lines 89–95, 201–222).
- Missing gate is not a zero: `no gate at .../no-gate/tools/research-gate.sh`, `probe_rc=2` (probe line 16).
- C2/C3 mutation runs used explicitly synthetic test adapters delegating to the f361 base gate and adding/removing only targeted output; they are probe-sensitivity experiments, not mutations of a completed candidate implementation. No sibling candidate code was available in this clone when run.
- Bash LSP unavailable: `command -v bash-language-server` → `bash-language-server unavailable`.

## Retained artifacts

- Clone: `/tmp/chousa-r26-ExecProbeAttack-3`. Test files: `round26-measure-small.sh` SHA256 `26dabeb61fdc5020ccc3f6918eaa49a4ca223876112bfd8302f98c46a7a8fcce`; `c2-mutant.py` `c402e9a644b6f9b7e61e0d22a87efdc22f542456de80216fc9b4e48013f447fe`; `c3-mutant.py` `a0db937b1be92257e186247779109e523879c47d59503e7218df24f354400b36`.
- Gate wrappers: `synthetic-c2/tools/research-gate.sh` SHA256 `746f173db880e4d5261a425a5e74e12681a89b6f9c5666d3dd6d89bee62830a3`; `synthetic-c3/tools/research-gate.sh` `c45eb6a5c7af70126ca6baf0b9d9fe3721be72d8a7aabadbc8b73a319231a7f0`; parse-failure wrapper `synthetic-fail/tools/research-gate.sh` `9bfc9507af63b0799922f2e573400d7c32519bbdcde6ff397cfd89d93e1df5cc`.
- Tracked diff against observed base is empty; patch retained at `/tmp/chousa-r26-ExecProbeAttack-3/r26-ExecProbeAttack-3.patch` (0 bytes, SHA256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`). The transient skip-header edit was reversed. Live-lane write: this report only.
- Installs: none.

VERDICT: C2/C3 targeted controls detect the tested semantic mutants, but the C2 no-`--as-of` compatibility blind spot can let an incorrect gate score the full after-vector; failed option parsing also produces success-status zero counters. C1's hash hold catches skip-header output drift, but its amplification value alone can false-pass.