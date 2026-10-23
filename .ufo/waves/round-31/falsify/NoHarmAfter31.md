# Round 31 no-harm: base vs tip

Axes: coverage, operability. Tip: clone at `ee1024fd492144c9c7b315890fac247543c37208`; same fleet root `/home/vgpnk/Projects/shokunin`; base evidence: `.ufo/waves/round-31/build/ExecNoHarmBase/summary.tsv` and its `.stdout`/`.stderr` captures. Commands follow `ExecNoHarmBase.md`; selftest used `timeout 1200`, other commands `timeout 600`. Compared stdout/stderr byte-for-byte after normalizing only `ts=` and `gate_sha256=` values.

| Check | Base rc / output | Tip rc / output | Result |
|---|---|---|---|
| selftest | 0; PASS (215 cases, 0 skipped) | 0; PASS (228 cases, 0 skipped) | Only difference: 13 appended C1/C2 cases 216–228 and total; previous cases unchanged. Expected added coverage, no harm. |
| claims-r2 / claims-r9 | 0; 17/17 CLEAN / 0; 10/10 CLEAN | 0; 17/17 CLEAN / 0; 10/10 CLEAN | stdout/stderr identical after normalization. |
| chain-r3 / chain-r3-broken | 0; 17/22 CLEAN / 1; 1/2 DRIFT | 0; 17/22 CLEAN / 1; 1/2 DRIFT | stdout/stderr identical after normalization. |
| sweeps-r5 / integrity-r7 | 0; 1/2 sweeps, 3/3 rejections CLEAN / 0; refs 16, resolved 15 CLEAN | Same | stdout/stderr identical after normalization. |
| verify-all r7 | 0; 5/5 sections run, CLEAN | Same | stdout/stderr identical after normalization. |
| `--drift` r12 / r8 | 0; `GATE_DRIFT: none` / 1; `GATE_DRIFT: GATE record_sha256` | Same | stdout/stderr identical after normalization. |
| Round-1 observable | 0; `VERDICT_BEARING_EXPORTS=3/3` | Same | All three row results and stdout/stderr identical after normalization. |

Verdict: no harm observed on the specified battery; no unexplained differences. Limits: this is the requested battery only. No tools installed or updated.