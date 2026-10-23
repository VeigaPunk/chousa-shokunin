# CtlBaselineJunk — baseline controls (do-nothing / junk / one-value stubs / label-keyed)

Lane: `chousa-shokunin` (claims.md design v1; gate `tools/research-gate.sh` SHA-256 `ac1315ddaa12e79b68069d1a9866b9b1b55e3a43efef3ba0cb5ca5e665835765`, unmodified land copy, exactly the frozen hash).
Counters run: `corpus/evidence/round31/c1-count.py` (SHA-256 `154e09e7f73bebaf0afc2eed4d6c4c4ed8cb47d42518f764560a81fbcd7b555d`) and `c2-count.py` (`20ed105bf93081468934eea4265028cb1274d0115058b35cec72c9cd5694bf72`).
Work: sandbox `/fast/scratch/hyaku/chousa-r31/CtlBaselineJunk/`; all runs from the lane root, each wrapped in `timeout 900`; every gate exited 0 or 1, no timeouts. Seeds fresh: 1001, 2002, 3003.
Installs: none (existing python3/bash; no tooling changes).

Control scripts (byte-identical copies in this seat dir; receipt `gate_sha256` pins each):
`junk.sh` 9392bb79fdfa1ceb00f229b3b7f4361d8c84306a93a04ff0fcf717d8dcf9b35c
`label_keyed.sh` 87956334c87a47879038634cb94ca1ca31bd640e490accb17a5904794f03b817
`stub_supported.sh` 618ad29fdba28aac66817678cf845c2e3cfad6e7013410f71bcf9523a9a7c28e
`stub_mislocated.sh` 2eed158221f799e8616925bf052bde36fbc467a113268931bba76eb2923e4998
`stub_invalid.sh` 4db32ea3ed88ccb34ee22030780313a845d7ae4fd24ce7b068eb970bc0b98a04
`stub_unsupported.sh` d61bb977d57d62f18057c45c67af158bab63b77ee58b26dab9eea2981bb1d4c7
`stub_stale.sh` 92f0c290730e47fb2e4682e0956e3618df91e2c556e73455c3720bce6d3ade2f
`stub_none.sh` f6fbc3cb3eecde55c73051560e7c6897ad1ef0449fcd77e4a634949b002c40af
`driver.sh` — the runner (in seat dir).

## Results (score = matched/120; `predicate_holds=false` for all 54 runs)

| control | c1 1001 | c1 2002 | c1 3003 | c2 1001 | c2 2002 | c2 3003 | receipt prefix |
|---|---|---|---|---|---|---|---|---|
| base (do-nothing, unmodified lane gate) | 50 | 50 | 50 | 50 | 50 | 50 | `_base_seed` |
| junk (uniform over {supported,mislocated,invalid,unsupported,stale}) | 25 | 23 | 24 | 33 | 25 | 23 | `_junk_seed` |
| stub supported | 42 | 42 | 42 | 40 | 40 | 40 | `_s_supported_seed` |
| stub mislocated | 58 | 58 | 58 | 0 | 0 | 0 | `_s_mislocated_seed` |
| stub invalid | 12 | 12 | 12 | 14 | 14 | 14 | `_s_invalid_seed` |
| stub unsupported | 8 | 8 | 8 | 10 | 10 | 10 | `_s_unsupported_seed` |
| stub stale | 0 | 0 | 0 | 56 | 56 | 56 | `_s_stale_seed` |
| stub none (prints nothing) | 0 | 0 | 0 | 0 | 0 | 0 | `_s_none_seed` |
| label-keyed (observed := expect) | 42 | 42 | 42 | 40 | 40 | 40 | `_label_seed` |

Receipts: `c1<counter>_<control>_seed<seed>.json` under this dir, e.g. `c1_base_seed1001.json`, `c2_s_stale_seed3003.json`; all 54 files present.

## Findings
- Do-nothing base gate reproduces the frozen Before exactly on both counters: 50/120 (C1 and C2). Confirms the baseline.
- Every one-value stub scores exactly the size of its matching hidden-truth class: C1 truth = supported 42, mislocated 58, invalid 12, unsupported 8 (stale and none are not C1 truth values → 0); C2 truth = supported 40, unsupported 10, stale 56, invalid 14. This confirms the counter's fixed 12/9-class enumeration and hidden counts.
- Label-keyed ≡ stub_supported, because every fixture claim carries `expect=supported` (the label carries no truth by design).
- Junk (uniform over the 5 real observed values) lands at 23–33/120, consistent with the binomial expectation ~24 (p=1/5, n=120); worst draw 33/120 (C2 seed 1001) is ~2σ, still far from 120.
- Max reached across all 54 runs: 58/120 (C1 stub_mislocated) and 56/120 (C2 stub_stale) — each simply equals its counter's largest truth slice; even the best constant guess leaves >50% of claims wrong. Nothing approaches 120/120.

## Verdict
- C1: **design holds**.
- C2: **design holds**.
