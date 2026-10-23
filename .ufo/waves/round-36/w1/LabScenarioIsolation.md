# Round 36 W1 — LabScenarioIsolation

Date: 2026-10-23. Axis: C1 scenario isolation / verdict stability.

## Hypothesis

**Every C1 scenario is hermetic: its verdict is unchanged when run in a different order or alone.**

## Source inspection

`c1-count.py` offers only `--gate`, `--seed`, and `--receipt`; it has no scenario selector. The counter creates one per-invocation root using `C1_TMP`, else `TMPDIR`, else the system temp directory. Its `scratch` directory and the fixtures are beneath that root. The fourteen scenario bodies execute sequentially.

Resources shared within an invocation:

- `fa` and `claims_a` serve S1–S9. `trip1`, `trip2`, and `trip3` are common tripwires; S1/S2/S6/S9 truncate the relevant file before use. `rec_a` is used in S7 and S9, and its log is truncated before each use. S3 creates `nogrepbin` beneath the common root.
- S10 uses a separate `fx-b`, recorder/log, and patched gate; S11/S13/S14 use `fx-d`; S12 uses separate `fx-c`. S11's manifest, and S13/S14's pin files, are distinct paths.
- One seeded RNG is advanced through recorder names/markers and fixture generation. The result/run lists and reference-A values are shared bookkeeping.
- `run_gate` constructs a fresh child environment from the counter's environment, removes `CHOUSA_*` and `RESEARCH_GATE_*`, then applies the scenario's `PATH` and explicit overrides. Its subprocess changes do not update the counter's environment. The direct S13/S14 drift subprocesses use an environment copy with `CHOUSA_*` removed.

This is source inspection, not a proof for arbitrary reorderings. The shared files and RNG mean that some fixture/path details intentionally vary with execution state, while each counter invocation gets a new root.

## Experiment

The landed gate was pinned before scoring; both counter receipts independently record the same hash. Master tip was also read.

Commands run (verbatim):

```sh
timeout 900s mkdir -p /tmp/hyaku/chousa-r36/w1/LabScenarioIsolation/clean /tmp/hyaku/chousa-r36/w1/LabScenarioIsolation/poison /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/LabScenarioIsolation
```
Exit: 0 (command completed without error).

```sh
timeout 900s sha256sum /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh
```
Exit: 0. Deciding line: `a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8  /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh`.

```sh
timeout 900s git -C /home/vgpnk/Projects/shokunin/chousa-shokunin rev-parse master
```
Exit: 0. Output: `700bd5fcbf9abc118a6a0f078d51a2e7460c2878`.

Launched these two commands concurrently. Both use seed 36351 and the same absolute gate; the second counter process has the perturbed `TMPDIR` value. `C1_TMP` is unset in both, so `TMPDIR` is the counter's selected temp base.

```sh
timeout 1800s env -u C1_TMP TMPDIR=/tmp/hyaku/chousa-r36/w1/LabScenarioIsolation/clean python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round36/c1-count.py --gate /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh --seed 36351 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/LabScenarioIsolation/clean.json > /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/LabScenarioIsolation/clean.stdout 2> /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/LabScenarioIsolation/clean.stderr; printf 'COUNTER_EXIT_CODE=%s\n' "$?"
```
Captured counter exit: `0`.

```sh
timeout 1800s env -u C1_TMP TMPDIR=/tmp/hyaku/chousa-r36/w1/LabScenarioIsolation/poison python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round36/c1-count.py --gate /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh --seed 36351 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/LabScenarioIsolation/poison.json > /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/LabScenarioIsolation/poison.stdout 2> /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/LabScenarioIsolation/poison.stderr; printf 'COUNTER_EXIT_CODE=%s\n' "$?"
```
Captured counter exit: `0`.

Deciding output in each stdout: `ENGINE_SWAP_CANARY=14/14`, followed by PASS for S1 through S14. Each receipt has `predicate_holds: true`, `seed: 36351`, and `gate_sha256: a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8`. Per-scenario receipt verdicts are identical:

| Scenario | Clean TMPDIR | Perturbed TMPDIR |
|---|---:|---:|
| S1-shim-first-path | pass | pass |
| S2-bash-env-function | pass | pass |
| S3-no-grep-on-path | pass | pass |
| S4-override-relative | pass | pass |
| S5-override-missing | pass | pass |
| S6-override-non-gnu | pass | pass |
| S7-override-distinct-path | pass | pass |
| S8-default-echo | pass | pass |
| S9-override-beats-shim | pass | pass |
| S10-semantic-canary | pass | pass |
| S11-manifest-hash-shim | pass | pass |
| S12-locale-c | pass | pass |
| S13-pin-echo-isolation | pass | pass |
| S14-pin-drift-token | pass | pass |

The run-specific absolute paths differ, as expected. In particular, S10's generated patched-gate hash differs between receipts (`91cdb750ca649e45ed57b697d4bc2d16228899cd9ad36d87f77239e28a5a85b1` clean; `5f3e8115150cca209115ceffc8e93c3ef9436d14a0280e1251532df8dcc87140` perturbed), while its verdict remains pass. Both stderr files are 0 bytes.

## Verdict

**Falsified: NO for the tested concurrent `TMPDIR` perturbation.** All fourteen verdicts remained pass in both runs, with the same gate hash and predicate result. **[INFERENCE]** This supports isolation from counter temp-base relocation, but does not establish the full order/alone hypothesis: the counter cannot select one scenario, and this experiment did not permute the scenario order.

Risk/blocker: no direct singleton or reordered run is available through the counter CLI. The shared tripwires, recorder log, fixture A, and RNG are observable order-sensitive resources; their reset/use patterns looked intentional by inspection, but were not tested under a reordered harness.

## Files opened (2026-10-23)

- Validated brief: `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1-briefs/LabScenarioIsolation.md`
- Frozen claims: `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round36/claims.md`
- C1 counter: `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round36/c1-count.py`
- C2 counter: `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round36/c2-count.py`
- New witness: `/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/argv-witness.py`
- Round-35 witness: `/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/mechanism-witness.py`
- Hashed gate (hash only; no content read): `/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh`
- Experiment outputs inspected: `clean.json`, `poison.json`, `clean.stdout`, and `poison.stdout` under the artifact directory below.

## Evidence artifacts and SHA-256

All are under `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/LabScenarioIsolation/` and below 1 MiB:

- `clean.json` — `a3be01d91e5e7ef4bb2de71226dac3789d0ff5d5aff6fd63a6e07259f9c79560`
- `clean.stdout` — `dab9e7c953dc02f71d884eee399443e8f6a46c0648ee2c6bd7bba24381cdb154`
- `clean.stderr` — `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `poison.json` — `e047227c8c936beb1242801d8a338517f7e7442a24643bd24f8cc8426035b4cc`
- `poison.stdout` — `4f907d0d3e0f1a13f7a3285f168e6301b1ecbea12c8351102d47fd652115c190`
- `poison.stderr` — `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`

No production files were changed. No installs, builds, lint, tests, or formatters were run beyond the specifically required C1 counter experiment.
