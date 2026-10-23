# RerunC1B — WAVE 2 FALSIFY: re-derive the C1 counting command on the landed revision

**Attack:** re-run the frozen `corpus/evidence/round31/c1-count.py` at lane tip `ee1024fd492144c9c7b315890fac247543c37208` on 5 fresh seeds in a fresh clone, clean environment, receipts bound to counter and gate bytes. Axes: coverage (does the landed C1 hold 120/120 on seeds nobody ran?), operability (does the command reproduce end-to-end with correct `counter_sha256`/`gate_sha256` bindings?).

**Command shape** (cwd = fresh clone at tip, `env -i PATH=/usr/bin:/bin HOME=/home/vgpnk timeout 900`):
`python3 corpus/evidence/round31/c1-count.py --seed <S> --gate /fast/scratch/hyaku/chousa-r31/w2/RerunC1B/lane/tools/research-gate.sh --receipt <falsify dir>/receipt-<S>.json`

**Expected bindings** (`sha256sum` in the clone at `ee1024fd`):
- counter `c3aca35da30ee47edc3402daa559f43320e44a82d3a0143b5ea283ec8c49b427`
- gate `c23d7537e03482f2844c9cbc43fc055d3d08d564857a89529b6f13473403823c` (matches the landed C2 gate `c23d7537…`)

| seed | score | exit | counter_sha256 = expected | gate_sha256 = expected | predicate_holds | misses | receipt (falsify/RerunC1B/) |
|---|---|---|---|---|---|---|---|
| 20261023 | LINE_BINDING_MATCH=120/120 | 0 | yes | yes | true | none | receipt-20261023.json |
| 314159265 | LINE_BINDING_MATCH=120/120 | 0 | yes | yes | true | none | receipt-314159265.json |
| 271828182 | LINE_BINDING_MATCH=120/120 | 0 | yes | yes | true | none | receipt-271828182.json |
| 161803398 | LINE_BINDING_MATCH=120/120 | 0 | yes | yes | true | none | receipt-161803398.json |
| 577215664 | LINE_BINDING_MATCH=120/120 | 0 | yes | yes | true | none | receipt-577215664.json |

All 5 receipts: `schema chousa-r31-c1-receipt/v2`, `matched=120`, `gate_timed_out=false`, `misses=[]`; every per-class line at its full count (B1 12/12, B2 12/12, B3 12/12, B4 6/6, M1 12/12, M2 12/12, M3 12/12, M4 8/8, M5 6/6, M6 8/8, I1 12/12, U1 8/8). Runtime ~2.9 s per run.

**Verdict: C1 holds** — no run below 120/120; nothing to quote (no misses list is non-empty). Operability holds: the committed counter re-derives the landed behavior byte-for-byte bound in a stripped environment.

**Observations (not defects):** `gate_rc: 1` in every receipt — verify-claims exits 1 when drift findings are printed (mislocated fixtures), which the counter's contract treats as a valid gate outcome (exit other than 0/1 would score `none`). Receipts bind the gate path to my scratch clone, as contracted.

**Limits:** 5 seeds of an unbounded seed space (kill rule is per-run; no run missed). No tool installs made. No control or sibling candidate re-scored; C2 outside scope. Artifact clone in `/fast/scratch/hyaku/chousa-r31/w2/RerunC1B/` may be deleted.
