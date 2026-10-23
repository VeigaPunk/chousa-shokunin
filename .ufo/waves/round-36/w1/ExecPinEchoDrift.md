# Round 36 wave 1 — ExecPinEchoDrift

Date: 2026-10-23. Axes: operability (pin echo isolation) and calibration (drift-token specificity).

## Gate and verdict

Scored gate: `/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh`, SHA-256 `a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8` (verified before the runs).

**VERDICT: S13 and S14 both hold on the landed gate in the assigned direct probes.** S13: a pin invoked with `CHOUSA_GREP_PIN_ECHO=1` writes a baseline containing no `GATE_GREP:` line, and unchanged drift is clean. S14: an injected `GATE_GREP:` baseline line is reported as `-GATE_GREP`, not `-LINE`.

## Three requested runs

1. **Echoed pin, then drift without echo.**

   Commands (each gate command was bounded by `timeout 900s`):

   ```text
   CHOUSA_GREP_PIN_ECHO=1 timeout 900s bash /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh --pin /tmp/hyaku/chousa-r36/w1/ExecPinEchoDrift/run1.baseline
   env -u CHOUSA_GREP_PIN_ECHO timeout 900s bash /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh --drift /tmp/hyaku/chousa-r36/w1/ExecPinEchoDrift/run1.baseline
   ```

   Pin exit 0; deciding output: `GATE_PIN: ok path=/tmp/hyaku/chousa-r36/w1/ExecPinEchoDrift/run1.baseline gate_sha256=a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8`. The expected echo was printed by the pin process: `GATE_GREP: path=/usr/bin/grep source=default version="grep (GNU grep) 3.12-modified"`. Drift exit 0; deciding line: `GATE_DRIFT: none`. Baseline scan: `BASELINE_HAS_GATE_GREP=0`.

2. **Echo explicitly supplied in the pin command's environment.**

   Command:

   ```text
   env CHOUSA_GREP_PIN_ECHO=1 timeout 900s bash /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh --pin /tmp/hyaku/chousa-r36/w1/ExecPinEchoDrift/run2.baseline
   ```

   Exit 0; output included the `GATE_GREP: path=/usr/bin/grep source=default version="grep (GNU grep) 3.12-modified"` echo and `GATE_PIN: ok path=/tmp/hyaku/chousa-r36/w1/ExecPinEchoDrift/run2.baseline gate_sha256=a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8`. Baseline scan: `BASELINE_HAS_GATE_GREP=0` (deciding scrub result).

3. **Injected token line.** I copied run 2's baseline and inserted `GATE_GREP: path=/usr/bin/grep source=default version="injected"` immediately after `# --- canonical output follows ---` in the copy only. Then ran:

   ```text
   env -u CHOUSA_GREP_PIN_ECHO timeout 900s bash /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh --drift /tmp/hyaku/chousa-r36/w1/ExecPinEchoDrift/run3.injected.baseline
   ```

   Exit 1 (expected drift); deciding line: `GATE_DRIFT: -GATE_GREP`. It did not report `-LINE`.

## Retained artifacts

All retained artifacts are in the assigned artifact directory and under 1 MiB:

- `.ufo/waves/round-36/w1/ExecPinEchoDrift/run1.baseline` — 2,989 bytes; SHA-256 `366f5c87bd7b4d4e5c4648cd54da458f46ba4e7b985dd441087da1b95ed0cd51`.
- `.ufo/waves/round-36/w1/ExecPinEchoDrift/run2.baseline` — 2,989 bytes; SHA-256 `9e011c7851ff87c5cbe5b317bbf2137c406ed9c8e48d3dee0640c4b1d37ed072`.
- `.ufo/waves/round-36/w1/ExecPinEchoDrift/run3.injected.baseline` — 3,053 bytes; SHA-256 `3ee4dcef68789f20d866bac06bad9b390721e6cd4d86b622f2cb8f6a722d2415`.

## Other commands and evidence

- `timeout 60s sha256sum /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh` — exit 0; output matched the gate SHA above.
- `timeout 60s /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh` — exit 2; its own usage output included `usage: research-gate.sh --pin PATH` and `usage: research-gate.sh --drift PATH`, establishing the invoked syntax.
- `timeout 60s mkdir -p /tmp/hyaku/chousa-r36/w1/ExecPinEchoDrift /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecPinEchoDrift` — exit 0.
- `timeout 60s cp /tmp/hyaku/chousa-r36/w1/ExecPinEchoDrift/run2.baseline /tmp/hyaku/chousa-r36/w1/ExecPinEchoDrift/run3.injected.baseline` — exit 0.
- Artifact retention command: `timeout 60s cp /tmp/hyaku/chousa-r36/w1/ExecPinEchoDrift/run1.baseline /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecPinEchoDrift/run1.baseline && timeout 60s cp /tmp/hyaku/chousa-r36/w1/ExecPinEchoDrift/run2.baseline /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecPinEchoDrift/run2.baseline && timeout 60s cp /tmp/hyaku/chousa-r36/w1/ExecPinEchoDrift/run3.injected.baseline /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecPinEchoDrift/run3.injected.baseline && timeout 60s wc -c /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecPinEchoDrift/run1.baseline /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecPinEchoDrift/run2.baseline /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecPinEchoDrift/run3.injected.baseline && timeout 60s sha256sum /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecPinEchoDrift/run1.baseline /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecPinEchoDrift/run2.baseline /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecPinEchoDrift/run3.injected.baseline` — exit 0; sizes and hashes are listed above.

## Changed files, scope, risks, blockers

Changed files are the report and the three retained baseline artifacts listed above. No production file was edited. No install, build, selftest, counter, lint, or formatter was run. This focused work re-derives S13/S14 only; it does not rescore the complete C1/C2 predicates. Blockers: none.

## Files opened (access date 2026-10-23)

- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1-briefs/ExecPinEchoDrift.md`
- `/home/vgpnk/.agents/skills/godspeed/SKILL.md`
- `/home/vgpnk/.omp/agent/RULES.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round36/claims.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round36/c1-count.py`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round36/c2-count.py`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/argv-witness.py`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/mechanism-witness.py`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/measure/c1-after-s36001.json`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/measure/c1-after-s36011.json`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/measure/c1-before-s36001.json`
- `/tmp/hyaku/chousa-r36/w1/ExecPinEchoDrift/run3.injected.baseline`
