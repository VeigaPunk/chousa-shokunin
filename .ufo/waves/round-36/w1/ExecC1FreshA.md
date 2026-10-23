# ExecC1FreshA — C1 fresh-seed measurement

Access date for all listed reads: 2026-10-23.

## Result

**Verdict: P1 arm measured on fresh seed 36301: PASS, 14/14; this seat's single run does not alone complete the frozen two-seed P1 predicate.** `predicate_holds=true`; the counter exited 0. The stdout deciding line was `ENGINE_SWAP_CANARY=14/14`; all S1–S14 rows were PASS. Counter-reported elapsed time was 4.16 s; shell `time` reported 4.191 s wall time.

The receipt records `gate_sha256=a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8`, label `ENGINE_SWAP_CANARY=14/14`, total 14, and `predicate_holds=true`. Pre- and post-run hashes of `tools/research-gate.sh` both matched the expected landed-gate SHA.

## Commands and deciding evidence

1. `timeout 30 mkdir -p /tmp/hyaku/chousa-r36/w1/ExecC1FreshA /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecC1FreshA` — exit 0, no output. This created the required existing `C1_TMP` directory before scoring.
2. `timeout 30 sha256sum /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh` — exit 0; `a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8`.
3. `cd /home/vgpnk/Projects/shokunin/chousa-shokunin && TIMEFORMAT='ELAPSED_SECONDS=%3R'; time C1_TMP=/tmp/hyaku/chousa-r36/w1/ExecC1FreshA timeout 1800 python3 corpus/evidence/round36/c1-count.py --gate tools/research-gate.sh --seed 36301 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecC1FreshA/c1-after-s36301.json; rc=$?; printf 'EXIT_CODE=%s\\n' "$rc"; exit "$rc"` — exit 0; deciding stdout line `ENGINE_SWAP_CANARY=14/14`.
4. `timeout 30 sha256sum /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecC1FreshA/c1-after-s36301.json /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh` — exit 0; receipt SHA `ca0a95234e36ee55a9900c60f159618601f90d6f6431419ba87d0227ea911af2`; gate SHA `a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8`.

## Retained artifact

- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecC1FreshA/c1-after-s36301.json` — SHA-256 `ca0a95234e36ee55a9900c60f159618601f90d6f6431419ba87d0227ea911af2`.
- No other retained artifact was created in the lane artifact directory. Counter scratch data is under `/tmp/hyaku/chousa-r36/w1/ExecC1FreshA/`.

## Files opened (2026-10-23)

- `/home/vgpnk/.agents/skills/godspeed/SKILL.md`
- `/home/vgpnk/.omp/agent/RULES.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1-briefs/ExecC1FreshA.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round36/claims.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round36/c1-count.py`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round36/c2-count.py`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/argv-witness.py`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/mechanism-witness.py`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh` (hashed before and after run)
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecC1FreshA/c1-after-s36301.json`
- Listed `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/measure/`.

## Risk / blocker

The receipt establishes one fresh-seed arm only. Frozen P1 requires two fresh seeds; this report makes no two-seed verdict. No implementation files were changed and no installation was performed.