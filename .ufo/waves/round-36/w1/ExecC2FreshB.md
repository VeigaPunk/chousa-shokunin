# C2 fresh-seed re-derivation — ExecC2FreshB

Access date: 2026-10-23.

## Verdict

**C2 seed 36311: predicate holds.** On the landed gate (sha256 `a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8`), the counter exited 0 and printed the deciding line:

```text
WITNESS_PER_RECORD=5/5 OUTPUT_EQUIV=5/5 LANDED_ATTRIB=pass RENAMED=pass
```

Receipt records `seed=36311`, `predicate_holds=true`, landed witness `pass`, `output_full=true` (9/9), no unattributed records, 11 matcher calls, and renamed control `pass`.

## Per-variant result

| Variant | Output | Witness | Attributed records |
|---|---:|---|---:|
| V1-python-exact | 9/9 | fail | 1 |
| V2-env-keyed | 9/9 | fail | 1 |
| V3-witness-forge | 9/9 | fail | 1 |
| V4-one-call-for-show | 9/9 | fail | 2 |
| V5-body-replaced | 9/9 | fail | 1 |
| V6-renamed-matcher | 9/9 | pass | 9 |

**VERDICT_DIFF_vs_measure/c2-after-s36001.json: none.** All six witness verdicts and `output_full` values match the committed seed-36001 table; all variants are output-full, V1–V5 fail, and V6 passes.

## Commands and retained evidence

Each command ran with the displayed exit status. The counter's shell wrapper exit was 0; `COUNTER_EXIT=0` is its underlying Python counter exit.

```text
timeout 900s bash -lc 'sha256sum /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh; git -C /home/vgpnk/Projects/shokunin/chousa-shokunin rev-parse master'
exit 0
output: a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8  /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh
        700bd5fcbf9abc118a6a0f078d51a2e7460c2878

timeout 900s mkdir -p /tmp/hyaku/chousa-r36/w1/ExecC2FreshB /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecC2FreshB
exit 0

env C1_TMP=/tmp/hyaku/chousa-r36/w1/ExecC2FreshB C2_TMP=/tmp/hyaku/chousa-r36/w1/ExecC2FreshB WITNESS_TMP=/tmp/hyaku/chousa-r36/w1/ExecC2FreshB TMPDIR=/tmp/hyaku/chousa-r36/w1/ExecC2FreshB timeout 1800s python3 corpus/evidence/round36/c2-count.py --seed 36311 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecC2FreshB/c2-36311.json; rc=$?; printf 'COUNTER_EXIT=%s\n' "$rc"; exit 0
shell exit 0; COUNTER_EXIT=0
output:
WITNESS_PER_RECORD=5/5 OUTPUT_EQUIV=5/5 LANDED_ATTRIB=pass RENAMED=pass
  V1-python-exact        output=9/9 witness=fail attrib=1
  V2-env-keyed           output=9/9 witness=fail attrib=1
  V3-witness-forge       output=9/9 witness=fail attrib=1
  V4-one-call-for-show   output=9/9 witness=fail attrib=2
  V5-body-replaced       output=9/9 witness=fail attrib=1
  V6-renamed-matcher     output=9/9 witness=pass attrib=9
COUNTER_EXIT=0

timeout 900s sha256sum /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecC2FreshB/c2-36311.json
exit 0
output: b89559ac8ed504f21316072f783dcc1bc3e09a362a7abc6e9eac03fd253b4e13  /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecC2FreshB/c2-36311.json
```

Retained artifact under my directory: `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecC2FreshB/c2-36311.json` — sha256 `b89559ac8ed504f21316072f783dcc1bc3e09a362a7abc6e9eac03fd253b4e13`.

## Files opened

All accessed 2026-10-23:

- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1-briefs/ExecC2FreshB.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round36/claims.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round36/c1-count.py`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round36/c2-count.py`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/argv-witness.py`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/mechanism-witness.py`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/measure/c2-after-s36001.json`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecC2FreshB/c2-36311.json`
- `/home/vgpnk/.agents/skills/godspeed/SKILL.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecC2FreshB.md`

No installs. No build, lint, formatter, or test commands were run.