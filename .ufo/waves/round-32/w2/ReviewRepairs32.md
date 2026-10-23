# ReviewRepairs32 — falsification of round-32 r31-repairs (R1–R6)

Target: `corpus/evidence/round32/r31-repairs.md` vs `corpus/lessons/round-31-verifier-spotcheck.md:201-234`.
Base `7a7259f0` (gate `0bc318b3…1258`), landed `5d8a170` (gate `10f2fe12…4098`, both hashes
re-computed via `git show <rev>:tools/research-gate.sh | sha256sum`).

## Verdict: HOLDS with two minor defects (one wrong number, one dead evidence pointer)

| Route | Verdict |
|---|---|
| R1 (append-only correction) | HOLDS — all numbers reproduce |
| R2 counter v3 | HOLDS — hashes, 132 totals, landed/mutant receipts all reproduce |
| R2 selftest (7 cases) | HOLDS — cases present in landed gate; my own clone selftest `PASS (241 cases)` rc=0 |
| R3 (no-harm on `0bc318b3`, lane `4111607c`) | HOLDS — every cited number in the receipts |
| R4 (sibling-file edits + gate comment) | HOLDS (one observation below) |
| R5 (oracle `bfc0b02b` provenance) | PARTIALLY FALSE — total "43 files bind it" is wrong: **46** |
| R6 (fleet report wording) | INCONCLUSIVE — cited report does not exist |

## Findings

### F1 [low — false sentence] R5: file count off by 3
`r31-repairs.md` R5: "43 files under `.ufo/waves/round-31/` bind it (21 receipts, 21 output
echoes, 1 manifest)". Actual: `grep -rl 'bfc0b02b' .ufo/waves/round-31/` → **46** files.
Breakdown: 21 receipts (`oracle-s{1..3}.json` + 18 `restored-*.json`), 21 `.output.json` echoes,
`probe-manifest.json`, **plus** `kill-matrix.json`, `controls/MutOracleC1.md`, and
`falsify/CriticChronology31/receipt-inventory.tsv`, which also contain the hash. The receipt/
echo/manifest subset count (43) is correct; the "43 files under … bind it" total is not.
Also note the spotcheck's own "42 receipts" was itself a conflation (21 receipts + 21 echoes) —
the repair correctly decomposes it, then slips on the file total.

### F2 [low — unverifiable evidence] R6: cited report absent
`.ufo/reports/round-32/chousa.md` does not exist in either repo (fleet `/home/vgpnk/Projects/
shokunin/.ufo/reports/round-32/` contains only kake/kotodama/kumitate/mori/tsukuroi; lane has no
`.ufo/reports/round-32/`). The repair itself is correctly scoped (a wording requirement on a
future fleet report — the spotcheck's R6 says "a future report should say which gate each run
used"), but the "Evidence … re-checked by the L1 this round" column points at a file that does
not yet exist, so the claim cannot be verified this round.

### Observation [not a defect] R4 gate-comment range
`research-gate.sh:6910` now reads `cases 216-228`; in the landed gate the sha256 block is
actually cases 220–228, with 216–219 being the r31 C1 line-binding cases (`ok-case 216
c1-pass-bound` … `ok-case 219 c1-pass-no-line`, per my clone selftest log). The comment text
matches the routed defect verbatim ("the cases are 216–228"), the evidence file
(`m2-trim-space.selftest.stdout`) shows all 13 ok-case lines numbered 216–228, and
`base-grep` confirms the comment covers both r31 blocks. Slightly loose labelling, exact
wording satisfied — flagged for the record only.

## Per-route re-verification detail

- **R1**: `jq '{matched,predicate_holds,gate_sha256}'` on the four receipts:
  fail-open `…654/…514.receipt.json` → `120/true/5d52f37c…` ×2; trim-space `seed{1,2}` →
  `118/false/f3d88b23…` ×2. `round-31.md:97-98` unchanged (git diff shows append-only +13 lines
  at :115); appended correction text matches receipts and `MutC2Hash.md:5` "SURVIVED BOTH";
  `m2-trim-space.selftest.stdout` ends `PASS (228 cases, 0 skipped)`. Correction cites
  `spotcheck.md:203-208` — R1 bullet verified at 203-208 exactly.
- **R2 counter**: `sha256sum` → `c1-count-v3.py 0efbd172…b6`, `c2-count-v3.py 654183e1…a8` ✓;
  `TOTAL = 132` (c1-count-v3.py:67, "v2's 120 plus the 12 non-string claims"); diff adds only the
  two v3 files (v2 `c1-count.py`/`c2-count.py` untouched). Receipts: landed `0bc318b3`
  `matched=132/predicate_holds=true` ×2 seeds each counter; `mutC1Grammar` gate `85d85a7b…` →
  `120/false` (I2_nonstring_line_value 0/12); `mutC2Parse` gate `f9da8257…` → `120/false`
  (I2_nonstring_sha_value 0/12). `nested-probe.log` shows `{"meta":{"line":"9"}}` read as
  record's own (CLAIM_LINE_MISMATCH on NK1) — carried defect honestly recorded.
- **R2 selftest**: `ExecR2Selftest31/r2-selftest.log` → `PASS (235 cases)`, cases 229–235 =
  sha-nonstring, line-nonstring, endline, span-stale, ws-pin, hash-fault-shim, nested-string;
  `.md` line 17 records scratch `82470e57…` and 7-case patch `792cc1b8…`. Landed gate contains
  all seven case names (absent in base). My run on a clean clone @`5d8a170`:
  `PASS (241 cases, 0 skipped)` rc=0 — artifact `self-landed-10f2fe12.log` in this dir
  (sha256 `202702b4…`). Caveat: bare `selftest` (no `--`) prints usage exit 2.
- **R3**: `ExecNoHarmBase32/` all-r7 header `gate_sha256=0bc318b3… lane_rev=4111607c857b…`;
  `selftest.cases` sha `a8873064…` and `PASS (228 cases)`; `claims-r2` `17/17 CLEAN`; `chain-r3`
  `17/22 CLEAN` and `chain-r3-broken` `1/2 DRIFT`, both cmd lines show
  `--root /home/vgpnk/Projects/shokunin` (fleet root) ✓; `r1-observable` 3/3; v2 counters
  `r31-c{1,2}-s{32,33}.json` all `120/true` on `0bc318b3` ✓.
- **R4**: diff base→landed: SKILL.md "Historical — Round-25 final registry correction" marker ✓;
  README.md:960-963 now names `23536590`/`25c5bb70` + gate `0bc318b3…1258` (verified:
  `git show 25c5bb70:tools/research-gate.sh|sha256sum` = `0bc318b3…`; same for `23536590`) ✓;
  gate comment hunk `216-224 → 216-228` ✓ (see observation above).
- **R5**: `oracle-c1.sh` sha256 = `bfc0b02b…c617` ✓, 199 lines ✓, committed blob `7fea55f8` at
  base revision ✓; shebang bash + `exec python3 … <<'PY'` (the RevengerR5Oracle32.md memo gets
  this right; the table's "python script" is shorthand). All 21 receipts uniformly
  `matched=120/predicate_holds=true` — "harmless to P1" confirmed. Finding F1 on the count.
- **R6**: see F2.

## Commands (key ones, all exit 0 unless noted)

- `git diff 7a7259f0 5d8a170 -- SKILL.md corpus/README.md corpus/lessons/round-31.md`
  (3 files, +16/−3; SKILL historical marker, README R4 correction, append-only R1 correction)
- `jq` receipt reads quoted above; `grep -rl 'bfc0b02b' .ufo/waves/round-31/ | wc -l` → 46
- `git clone -q <lane> laneclone && git checkout -q 5d8a170…` then
  `TMPDIR=$PWD/tmp C1_TMP=$PWD/tmp C2_TMP=$PWD/tmp timeout 1800 prlimit --nproc=8000 bash
  laneclone/tools/research-gate.sh --selftest` → rc=0, `PASS (241 cases, 0 skipped)` 40.4 s.
  (A prior run on a bare copied gate file reported `FAIL claims-lane-fallback` — a scratch
  artifact: no `PROVINCE.md`/fixtures in a copy-only root; the proper clone passes. Recorded so
  no seat re-reports it.)

## Residual risk / gaps

- The four round-32 measure receipts (`after-c{1,2}-s*.json`) are all on `10f2fe12` with
  `predicate_holds=true` (spot-checked two: 24/24 and 132/132) — C1/C2 surfaces untouched by
  these repairs.
- R6 cannot be judged until the fleet report lands; nothing in the lane diff blocks it.
- No receipts were re-run for mutants/oracles (committed receipts re-opened verbatim); numbers
  above are re-reads, not new runs, except the landed selftest.

Artifacts: `self-landed-10f2fe12.log` (this dir). No installs. Scratch:
`/fast/scratch/hyaku/chousa-r32/w2/ReviewRepairs32/` (gate copy + laneclone); scratch processes
all completed, none left running.
