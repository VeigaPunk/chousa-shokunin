# ExecC1FreshB — C1 fresh-seed result

**Axes:** C1 operability; evidence integrity / fixture validity.

## Verdict

**C1 seed 36311: PASS.** The counter reported `ENGINE_SWAP_CANARY=14/14`; receipt `predicate_holds=true`, seed `36311`, gate SHA-256 `a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8`. S1–S14 all passed. Compared with committed `c1-after-s36001.json`, the per-scenario `scenario`→`pass` map is **identical** (all 14 true); no scenario verdict differs. This is the second-seed result only, not by itself the overall two-seed P1 finding.

## Commands and deciding evidence

1. `timeout 30s mkdir -p /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecC1FreshB /tmp/hyaku/chousa-r36/w1/ExecC1FreshB && timeout 30s sha256sum /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh` — exit 0. Gate hash output: `a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8`. The C1_TMP directory was created before the counter run.
2. `cd /home/vgpnk/Projects/shokunin/chousa-shokunin && C1_TMP=/tmp/hyaku/chousa-r36/w1/ExecC1FreshB timeout 1800 python3 corpus/evidence/round36/c1-count.py --gate tools/research-gate.sh --seed 36311 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecC1FreshB/c1-after-s36311.json` — exit 0. Deciding stdout: `ENGINE_SWAP_CANARY=14/14`; the S1–S14 lines each say `PASS`. Receipt fields: `label=ENGINE_SWAP_CANARY=14/14`, `predicate_holds=true`, and the gate SHA above.
3. `timeout 30s sha256sum /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecC1FreshB/c1-after-s36311.json && timeout 30s wc -c /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecC1FreshB/c1-after-s36311.json` — exit 0. Receipt SHA-256: `4c28a86937e0f4db0de05a0e968792aad28377f52e88df84cf7a197e41a8d6f1`; size `7139` bytes.

## Files and artifacts

Opened on 2026-10-23: `skill://godspeed` (`/home/vgpnk/.agents/skills/godspeed/SKILL.md`); `.ufo/waves/round-36/w1-briefs/ExecC1FreshB.md`; `corpus/evidence/round36/claims.md`; `corpus/evidence/round36/c1-count.py` (requested range 1–220); `corpus/evidence/round36/c2-count.py` (1–180); `tools/argv-witness.py` (1–200); `tools/mechanism-witness.py` (1–180); `.ufo/waves/round-36/measure/c1-after-s36001.json`; and the fresh receipt `.ufo/waves/round-36/w1/ExecC1FreshB/c1-after-s36311.json`. `tools/research-gate.sh` was SHA-256 checked as recorded above.

Created artifact under `.ufo/waves/round-36/w1/ExecC1FreshB/`:
- `c1-after-s36311.json` — SHA-256 `4c28a86937e0f4db0de05a0e968792aad28377f52e88df84cf7a197e41a8d6f1`, 7139 bytes.

No production files were modified. No blocker. Scope caveat from the frozen C1 limits: attribution shows the pinned matcher received each record's query; it does not establish that the matcher result was used. The fresh run is pinned to the landed gate hash above.
