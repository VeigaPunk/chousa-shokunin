# OracleC1B — v2 re-score of the three C1 feasibility oracles

Supplement to `OracleC1B.md` (v1 results retained there for reference; v1 is no longer counted).
Design v2 committed at lane `3d586d3ae2818193e51a4b2d9e6190157165c319`; base gate
`tools/research-gate.sh` sha256 `0bc318b3e74ac0ad45f4b34154e886d84aebf44673612afab6de5e0b0ff11258`
(unchanged at v2). Counter `corpus/evidence/round32/c1-count-v2.py` sha256
`e6bf95313ad603ff75e03bb64fbe5a2689a9dfe9bc4c0715a21012383508d891`, used exactly as committed;
every receipt records that hash. No counter edit, no candidate scored, no lane file touched.

## Gate layout and identity

Each gate sits at `<scratch>/<control>/tools/research-gate.sh` so the gate's lane root
(`/fast/scratch/hyaku/chousa-r32/w1/OracleC1B/v2gates/<control>`) cannot contain the counter's temp
dirs (`C1_TMP`/`TMPDIR` = `/fast/scratch/hyaku/chousa-r32/w1/OracleC1B/tmp2`).

| oracle | gate path | sha256 | differs from base |
|---|---|---|---|
| A `exec {fd}>>` + `flock -x "$fd"` across probe+append | `v2gates/A/tools/research-gate.sh` | `777ac24e694e15c3a7e53e4bfee4a195dcbc883be99673c4fa36f64ca3e97483` | yes |
| B `flock -x PATH -c` wrapping probe+append in a child | `v2gates/B/tools/research-gate.sh` | `917c9f41b5f9d7dcb41d8b7e6d5dd8493637c23e409690bebe395d0f67105c6b` | yes |
| C python3 `fcntl.flock(LOCK_EX)` wrapper on the append fd | `v2gates/C/tools/research-gate.sh` | `dfee84804c073cd9f2a404089ff03bf93e1c8869cf8324032294b958b70df7e3` | yes |

The mutated bytes are the v1 oracle bytes (same hashes as `OracleC1B.md`); none of the scratch
gates had been restored to pristine. Diffs: `oracles.patch`.

## Scores (v2 counter, 300 ms delayed writes touching the manifest)

Command form per row (cwd lane root, `timeout 900`):

```
C1_TMP=/fast/scratch/hyaku/chousa-r32/w1/OracleC1B/tmp2 TMPDIR=$C1_TMP \
python3 corpus/evidence/round32/c1-count-v2.py \
  --gate /fast/scratch/hyaku/chousa-r32/w1/OracleC1B/v2gates/A/tools/research-gate.sh \
  --seed 4001 --receipt .ufo/waves/round-32/w1/OracleC1B/v2/A-s4001.json
```

| receipt | oracle | seed | count | per-class | elapsed | exit | verdict |
|---|---|---|---|---|---|---|---|
| `v2/A-s4001.json` | A | 4001 | **24/24** | L_empty 4/4, L_terminated 4/4, L_unterminated 4/4, F_unterminated 12/12 | 100.566 s | 0 | **MEETS-TARGET** |
| `v2/A-s4002.json` | A | 4002 | **24/24** | same | 100.789 s | 0 | **MEETS-TARGET** |
| `v2/B-s4011.json` | B | 4011 | **24/24** | same | 101.592 s | 0 | **MEETS-TARGET** |
| `v2/B-s4012.json` | B | 4012 | **24/24** | same | 108.265 s | 0 | **MEETS-TARGET** |
| `v2/C-s4021.json` | C | 4021 | **24/24** | same | 96.636 s | 0 | **MEETS-TARGET** |
| `v2/C-s4022.json` | C | 4022 | **24/24** | same | 95.264 s | 0 | **MEETS-TARGET** |

All six receipts: `predicate_holds=true`, `ref_rc=0`, `total=24`, `fails=[]` on every trial
(read from the JSON files). Wall (bash `time`): 100.6 / 100.8 / 101.6 / 108.3 / 96.7 / 95.3 s.

## Reading

v2's 300 ms write-delay window is exactly the gap a probe-only lock exposes, and none of the three
oracles moved: each still holds its exclusive lock from before the last-byte probe until after the
delayed write returns, so the next writer cannot probe the same unterminated line. The v2 counter
therefore does not false-negative these three legitimate serializers; the v1 blind spot
(`CtlC1PartialLockB` probe-only lock at 24/24) is closed without disturbing correct lock scope.
Cost rose from 4–13 s (v1) to ~95–108 s (v2): ~288 traced writers × 300 ms plus strace start-up.

Limits as in `OracleC1B.md`: three mechanisms only; shared host (sibling-agent load 25–45 on 32
CPUs); B needs `flock(1)`, C needs `python3`; the v2 counter still cannot see which open file
description carries the lock, so oracle B (lock on a separate read-only open of PATH, child appends
through its own fd) passes 24/24 as before. Oracles are feasibility only, never candidates.
During the re-score the lane working tree gained unrelated tracked edits (`SKILL.md`,
`corpus/README.md`, `corpus/lessons/round-31.md` — not this seat); `tools/research-gate.sh` and
`c1-count-v2.py` re-hashed after the last run still equal `0bc318b3…` and `e6bf9531…`.
