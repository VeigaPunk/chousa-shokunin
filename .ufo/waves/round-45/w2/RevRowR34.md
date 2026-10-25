# RevRowR34 — falsify SKILL.md Gates row `research-gate round-34 v1/v2 counters`

Measured at commit `5e8c7ad2f7b8254d83358820286e3d12ca4672d1` from an archive tree at
`/tmp/chousa-r45-RevRowR34/tree` (run `git archive 5e8c7ad2… | tar -x`); all counter runs
from the lane root of that tree, `LC_ALL=C`. No lane writes; scratch removed after.

## Row (SKILL.md:103) has exactly 8 cells — HOLDS
Programmatic parse of the row: `N_CELLS= 8`:
`0 research-gate round-34 v1/v2 counters | 1 gate | 2 entry | 3 verdict map | 4 self-test |
5 pinned values | 6 write scope | 7 chousa`.

## Per cell

### 1 name — HOLDS
Cell: `research-gate round-34 v1/v2 counters`. Matches the target row.

### 2 kind — HOLDS
Cell: `gate`. Consistent with sibling rows.

### 3 entry — HOLDS
Cell text: `` `python3 corpus/evidence/round34/c1-count.py` · `python3 corpus/evidence/round34/c1-count-v2.py` (lane root; `--gate PATH`, `--seed N`, `--receipt OUT.json`) ``.
Both files exist at the commit (`corpus/evidence/round34/c1-count.py`, `c1-count-v2.py`,
also `c1-count-v3.py`, `claims.md`); both ran from lane root with default gate
`tools/research-gate.sh` and produced output (below).

### 4 verdict map — HOLDS
Cell text (key parts): `v1 `LONGSPAN_MATCH=30/30` · v2 `LONGSPAN_MATCH=40/40` exit `0`; any other count exit `1`; harness error exit `2`; both superseded before data by `corpus/evidence/round34/c1-count-v3.py` (design v3, TOTAL 42) …`
- Observation (default gate, seeds 7001/7002):
  - `LONGSPAN_MATCH=30/30` … `EXIT=0` (v1, seed 7001, per-class sums to 30)
  - `LONGSPAN_MATCH=40/40` … `EXIT=0` (v2, seed 7002, per-class sums to 40)
- Any other count → exit 1: fake-pass gate (script `exit 0`) → `LONGSPAN_MATCH=0/30`
  `EXIT=1` and `LONGSPAN_MATCH=0/40` `EXIT=1`.
- Harness error → exit 2: `--gate /tmp/…/does-not-exist.sh` → `c1-count: gate not found: …` `EXIT=2` (both counters).
- `c1-count-v3.py` exists at the commit and asserts `TOTAL == 42` (line 140), matching "design v3, TOTAL 42".
- v1/v2 rejection reasons are documented in the contract (claims.md design v2 § "v1 is therefore rejected as the P1 counter before data"; design v3 § CritC1Shapes "gate shapes no v2 class distinguishes").

### 5 self-test — HOLDS (one part not re-runnable)
Cell text: `Observed on the current gate (HEAD `d82cec904`, gate sha256 `2cb04bdd…`): v1 30/30 seed 7001 rc 0; v2 40/40 seed 7002 rc 0 | before on the round-33 gate `43a1af35`: v1 19/30 (seed 3401, `.ufo/waves/round-34/controls/L1-base/`, only committed v1 receipt); v2 base do-nothing never committed (v2 superseded by v3 before those runs); v3 base on the same gate 25/42 (`LC_ALL=C`), 0/42 ×2 by the 1500 s bound (UTF-8)`
- "Observed on the current gate": reproduced identically at the measured commit — v1 30/30 seed 7001 rc 0; v2 40/40 seed 7002 rc 0. The pinned gate sha256 `2cb04bdd…` fully matches in the measured tree: `2cb04bddfd5601d7c113a9b532a25895ce475847ff65f5672afc22586f5ffc34` (gate unchanged since wave-1 HEAD `d82cec904`). HOLDS.
- "round-33 gate `43a1af35`": this is the round-33 gate FILE sha256 prefix, not a git commit (git rev-parse fails on it). Reconstructed at the round-33 lane revision `70feb5eacc959eb98071461fe89f0b892c0810d8` → `tools/research-gate.sh` sha256 `43a1af35ca668fe535fcef1e68b0c64bbba3eada59c7a23181f591901fca4346`, exact match.
- "v1 19/30 (seed 3401, … L1-base/ …)": committed receipt `.ufo/waves/round-34/controls/L1-base/base-s3401.json` reads `label=LONGSPAN_MATCH=19/30 matched=19 total=30 predicate_holds=False seed=3401 gate=tools/research-gate.sh`; live re-run of v1 against the reconstructed round-33 gate with seed 3401 (LC_ALL=C) reproduced `LONGSPAN_MATCH=19/30` `EXIT=1` (~2m40s). HOLDS.
- "v2 base do-nothing never committed": confirmed — L1-base holds only the v1 receipt; claims.md erratum records the v2 do-nothing receipt never existed. HOLDS.
- "v3 base on the same gate 25/42 (LC_ALL=C)": reproduced — v3 (`c1-count-v3.py`) against the reconstructed round-33 gate, seed 3491, LC_ALL=C → `LONGSPAN_MATCH=25/42` `EXIT=1` (~4m16s). HOLDS.
- "0/42 ×2 by the 1500 s bound (UTF-8)": not re-runnable here (two 1500 s runs ≈ 50 min); inherited from the v3 row; left unexercised.

### 6 pinned values — HOLDS
Cell text: `contract `corpus/evidence/round34/claims.md` (design v1/v2; frozen predicates P1/P1 v2, kill rules v1/v2; v1 commit `70feb5ea`, v2 commit `ef16afb1`)`.
- `corpus/evidence/round34/claims.md` exists at the commit.
- Contains P1 (claims.md:55), P1 v2 (:123), Kill rule (:61), Kill rule v2 (:129), v2 supersede / rejection (:96-145).
- Commit pins resolve: `70feb5ea` → `70feb5eacc959eb98071461fe89f0b892c0810d8`; `ef16afb1` → `ef16afb16c05fb9a4e9a6c5b67cba44bdf3acbdb`.

### 7 write scope — HOLDS
Cell text: `temp dirs only (`C1_TMP` or `TMPDIR`); no network; writes a receipt only when `--receipt` is given`.
- Both counters' docstrings state "No network; writes only its temp dir (C1_TMP or TMPDIR), --keep and --receipt."
- With `--receipt /tmp/…/receipt-v1.json`: file created, `label=LONGSPAN_MATCH=30/30 predicate_holds=True seed=7003 total=30`, exit 0. No receipt written in the no-`--receipt` runs.

### 8 owner — HOLDS
Cell: `chousa`, consistent with the table.

## Verdict
Row HOLDS. Every entry command re-ran and matched the verdict map and self-test observed values;
the exit-0/1/2 contract was exercised directly; pinned paths exist at the measured commit; the
row has exactly 8 cells.

## Residual risk / verification gaps
- The UTF-8 1500 s timeout control (0/42 ×2) was not re-run (≈50 min); it is an inherited v3-row claim, not this row's verdict.
- `--receipt` was tested on v1 only; v2 shares the same code path (schema `chousa-r34-c1-receipt/v2`).
- Counter runtimes (10-20 s landed gate; 2m40s / 4m16s on the old gate) match the row's ~30 s note.

## Pointers
- Row: `SKILL.md:103` at `5e8c7ad2f7b8254d83358820286e3d12ca4672d1`.
- Counter `c1-count.py`: `corpus/evidence/round34/c1-count.py` (TOTAL 30, line 91; exit lines 55-57, 316-317).
- Counter `c1-count-v2.py`: `corpus/evidence/round34/c1-count-v2.py` (TOTAL 40, line 116; exit 77-79, 361-362).
- Contract: `corpus/evidence/round34/claims.md:55-63,123-131,142-165,194-212`.
- Committed v1 control receipt: `.ufo/waves/round-34/controls/L1-base/base-s3401.json`.
- Round-33 gate reconstruction: `tools/research-gate.sh` @ `70feb5eacc959eb98071461fe89f0b892c0810d8`, sha256 `43a1af35ca668fe535fcef1e68b0c64bbba3eada59c7a23181f591901fca4346`.
- Gate sha256 at measured commit: `2cb04bddfd5601d7c113a9b532a25895ce475847ff65f5672afc22586f5ffc34`.
