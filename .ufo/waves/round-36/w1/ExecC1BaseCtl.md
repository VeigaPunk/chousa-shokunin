# Round 36 wave 1 — C1 base control (ExecC1BaseCtl)

**Axes:** operability (C1 engine-swap canary) and calibration (the counter's fixture/reference sanity). This assignment measures the committed base-control gate only.

## Verdict

**BASE-CONTROL RESULT REPRODUCED:** seed 36321 scored `ENGINE_SWAP_CANARY=10/14`; `predicate_holds=false`. The four and only four failing scenarios are S11, S12, S13, and S14, matching the frozen claims' descriptions one-for-one. This is the expected do-nothing control; it does not establish the landed-gate C1 claim.

## Evidence

- Gate SHA-256: `a47688518e509edbf43b433a5e16e1cf2481233f3acedb5824ba341f7f0c38ad` (matches the expected base-control hash).
- Counter stdout deciding the score: `ENGINE_SWAP_CANARY=10/14`.
- Receipt fields: `gate_sha256` is the expected base hash; `label` is `ENGINE_SWAP_CANARY=10/14`; `matched` is `10`; `predicate_holds` is `false`; `seed` is `36321`; `total` is `14`.
- The four stdout failure lines and their evidence:
  - `S11-manifest-hash-shim FAIL` — `manifest_ok: false`, gate `rc: 0`, and true gate/record hashes are shown. Matches claims.md S11 (hostile `sha256sum` poisons both fields while command exits 0).
  - `S12-locale-c FAIL` — C-locale observation is `unsupported`/`mismatch`; UTF-8 observation is `supported`/`match`. Matches S12.
  - `S13-pin-echo-isolation FAIL` — `baseline_echo: true`; drift output is `GATE_DRIFT: -LINE`; pin `rc: 0`, drift `rc: 1`. Matches S13 (baseline embeds `GATE_GREP:` and drift reports `-LINE`).
  - `S14-pin-drift-token FAIL` — drift output is `GATE_DRIFT: -LINE`; pin `rc: 0`, drift `rc: 1`. Matches S14 (injected `GATE_GREP:` line pairs as `-LINE`).
- All other listed scenarios S1–S10 passed in the counter output.

## Commands run

1. `timeout 60 sha256sum /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/controls/base-gate-r36.sh` — exit 0; output hash matched the expected hash above.
2. `mkdir -p /tmp/hyaku/chousa-r36/w1/ExecC1BaseCtl /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecC1BaseCtl && cd /home/vgpnk/Projects/shokunin/chousa-shokunin && C1_TMP=/tmp/hyaku/chousa-r36/w1/ExecC1BaseCtl timeout 1800 python3 corpus/evidence/round36/c1-count.py --gate .ufo/waves/round-36/controls/base-gate-r36.sh --seed 36321 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecC1BaseCtl/c1-before-s36321.json` — exit 1 (the counter returns nonzero because its base-control predicate is false); decisive output and scenario evidence are quoted above.
3. `timeout 60 sha256sum /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecC1BaseCtl/c1-before-s36321.json` — exit 0; receipt SHA-256: `beec603870b9fe8d58aa2d15793e1d2c4f3cfe4cba82786549dd3ed731f3784b`.

## Artifact

- `.ufo/waves/round-36/w1/ExecC1BaseCtl/c1-before-s36321.json` — SHA-256 `beec603870b9fe8d58aa2d15793e1d2c4f3cfe4cba82786549dd3ed731f3784b`.

## Files opened (access date: 2026-10-23)

- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1-briefs/ExecC1BaseCtl.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round36/claims.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round36/c1-count.py`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round36/c2-count.py`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/argv-witness.py`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/mechanism-witness.py`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecC1BaseCtl/c1-before-s36321.json`
- `skill://godspeed` (`/home/vgpnk/.agents/skills/godspeed/SKILL.md`)

## Risks / blockers

No blocker for this scoped control measurement. The result is only the base-control run requested here; it is not a fresh-seed re-derivation of the landed C1 or C2 claims. No tools were installed.
