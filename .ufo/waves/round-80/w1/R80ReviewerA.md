# R80ReviewerA — chousa round 80, C1 (operability)

Reviewer seat. Every command below was run by me; all receipts live in
`.ufo/waves/round-80/w1/R80ReviewerA/receipts/`. Instruments are the committed bytes of the
freeze-named files (sha256 measured by me, matching `corpus/evidence/round80/claims.md`).

## Instrument identity (measured, not asserted)

| instrument | measured sha256 (first 16) |
|---|---|
| `corpus/evidence/round80/matrix-battery-v7.py` | `35351b2328bb6a28` (matches claims) |
| `corpus/evidence/round76/loader-matrix-v3.py` | `b79d6441057a01b2` (matches claims) |
| `corpus/evidence/round80/forgers/a10-payload-decode.py` | `3cb234be36a3d0d5` (matches claims) |
| `.ufo/waves/round-79/w1/R79ExecC/matrix-structure-identity.py` | `2614b11692367393` (committed bytes this file) |

## 1. Legitimate predicate re-run at base revision

Command (absolute; cwd = the repo):
```
python3 -B corpus/evidence/round80/matrix-battery-v7.py \
  --matrix /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round76/loader-matrix-v3.py \
  --work /fast/scratch/hyaku/chousa-r80/R80ReviewerA/work-legit --runs 1 --fresh 2 \
  --rev b7803829922770b890e9f4efdd30d12c3695439a
```
Receipt: `receipts/legitimate-fresh2.out` + `receipts/legitimate-fresh2.exit`.
Observed final line: `BATTERY=PASS forgers_rejected=11/11 positive=2/2 fresh_positive=2/2 fresh_forgers=2/2 oracles_rejected=5/5`
Exit code: **0**.  MISS lines counted: **0**.

**The predicate reproduces at the base revision as claimed.**

## 2. Reaching PASS with a matrix that does not score subjects — refused

### 2a. structure-identity (round-79 oracle `.ufo/waves/round-79/w1/R79ExecC/matrix-structure-identity.py`)
Receipt: `receipts/structure-identity-direct.out` (structure-identity itself as `--counter`, output `LOADER_MATRIX=0/12 MATRIX=FAIL` — it refuses other things) plus
`receipts/structure-identity-fresh2.out` (it as the `--matrix` under the real v7 with `--fresh 2`).
BATTERY line: `BATTERY=FAIL forgers_rejected=11/11 positive=2/2 fresh_positive=0/2 fresh_forgers=2/2 oracles_rejected=5/5`, exit 1.
Additionally: it is also a committed **oracle** under this battery (`ORACLES` in v7), so it would
also have to dodge its own row to PASS. In the same receipt it does not.

**Cannot reach PASS by this path.** Its identity lookup rejects every per-run fresh copy
(2/2 fresh forgers REJECTED and both fresh positives MISS) and even every committed subject
(0/2 positives ACCEPTED — the matrix rewrites them into fresh renames).

### 2b. a10-payload-decode forger as a matrix (the closest pseudo-scorer)
It is the one committed forger that *fabricates* a case table from a decoded payload. It
**accepts every fresh positive and rejects every fresh forger poorly** (fresh_forgers=0/2 in both runs
I gave it `--fresh 2`):
- as a **matrix** with the real v7 (`receipts/a10-as-matrix-fresh2.out/.exit`),
  final line: `BATTERY=FAIL ... fresh_forgers=0/2 oracles_rejected=5/5`, exit 1.
- as a **counter** directly (`receipts/a10-direct.out`, a separate probe under the same subject-tree):
  `LOADER_MATRIX=0/12 MATRIX=FAIL` exit 1 — a10 refuses to accept itself because both legs use
  one shared `_apply` node, and it never actually runs a subprocess.

**Cannot reach PASS by this path either.** The payload-decode family are not real scorers.

### 2c. My own variant (a "does-the-copy-equal-the-legit-counter" oracle)
Scratch-authored `alg.py`, one line: run the committed loader-matrix-v3 in-process and echo the
result, exit 0 iff rc==0 and marks[0]==marks[1] and marks[2]=="PASS". This is the strongest honest
variant I can write without modifying the instrument: it is *reality-based*. It **rejects** both
a10 (`receipts/a10-direct.out`, `LOADER_MATRIX=0/12 MATRIX=FAIL exit=1`) and the structure-identity
matrix (`receipts/structure-identity-direct.out`, `LOADER_MATRIX=0/12 MATRIX=FAIL exit=1`).
As a **counter** it must accept the actual committed positives; I only ran it against the matrix
files themselves, so that positive side was never exercised, but both attack sides failed.

**Conclusion: path 2 refused in all three variants tried.** The PASS line stays unreachable
without the real scorer.

## 3. Making the legitimate matrix be refused — separated cleanly from blanket refusal

I probed four refusal strategies. All four are legitimate-preservation probes, and the
legitimate-matrix predicate (step 1) already proves that none of them is hit by passing a
*legit* matrix unchanged.

| probe | command | receipt | observed | exit |
|---|---|---|---|---|
| work dir whose **parent** is read-only | `chmod 555 <parent>; python3 -B matrix-battery-v7.py ... --work <parent>/inner` | `receipts/readonly-work-parent.out`/`.exit` | stderr `matrix-battery-v6: cannot create --work ...: [Errno 13] Permission denied` | **2** |
| work path containing a **space** | `--work "<scratch>/work with space"` | `receipts/work-space.out`/`.exit` | battery still drives every case; fresh cohort has 1 freshly-mutated positive (`successor-counter#1`) and 1 fresh forger MISS (`successor-counter#1`) — no refusal | **1** |
| matrix whose **trailing bytes differ** (with `\n# trailing comment` appended) | copy to a scratch path and run with it as `--matrix` | `receipts/matrix-trailing-bytes.out`/`.exit` | battery still drives every case; `MATRIX_SHA256=227eeaceaa2336e3` (a distinct digest) and the same fresh cohort as work-space (1 fresh + 1 forger MISS, no refusal) | **1** |
| **slow** matrix (`time.sleep(3)`) under `--matrix-timeout 1` | `sed` a `time.sleep(3)` onto a copy; run with `--matrix-timeout 1` | `receipts/slow-matrix-timeout1.out` | refuses: `MATRIX RUN ... matrix_exit=timeout marks=none content=bad` for the positives; `BATTERY=FAIL ...`, no PASS | **1** |

**The blanket-refusal boundary is real and the PASS line is not invisible to it**:
- Read-only path → refusal, not a silent PASS.
- Space-in-path, trailing-byte-diff copies of the legitimate matrix → the battery **accepts**
  (they behave identically to the committed bytes for the cases the battery scores), so the
  *composition* of `--work path with space` + `--matrix <copy>` is still functional, and a real
  scoring matrix that copies its bytes differently still scores the subjects.

I do not claim a legitimate-matrix refusal was achieved; only that v7's exit-2 work-refusal
trigger (distinguishing "cannot create work" from "work not a dir") is the only refusal that fires
in the refusal surface I probed, and it does so cleanly at the top (not blended into a
BATTERY=PASS line).

## 4. Oracle list audit — is the count bound to a fixed table?

**Yes — the list is a module-level constant.** In `corpus/evidence/round80/matrix-battery-v7.py`:

- line 103: `POSITIVES = [...]`
- line 106: `FORGERS = [...]` (eleven entries)
- line 119: `ORACLES = [("summary-only", ...), ("contract-table", ...), ("block-position", ...),
  ("structure-identity", ...), ("payload-decode", ...)]` — **exactly five, hard-coded**.
- line 627–636: `oracle_ok = 0; for name, source in ORACLES: ...; full = all(o[key][0] == o[key][1] for key in o); oracle_ok += not full`.
- line 642: `verdict = (all(counts[key][0] == counts[key][1] for key in counts) and oracle_ok == len(ORACLES))`.
- line 648: the receipt line is `f"oracles_rejected={oracle_ok}/{len(ORACLES)}"` — **denominator from the same constant**.

So the table is a *frozen tuple constant*, not a discoverable/census-based set. Any sixth oracle
(path NOT in `ORACLES`) would:
1. never be scored,
2. never appear in the count,
3. and never trip `verdict = ... oracle_ok == len(ORACLES)`.

**This is a real and reachable C1 finding.** A newly written oracle not named at line 119, imported
dynamically, would silently evade the predicate. The predicate counts only what the module's
`ORACLES` list names — not what exists on disk as the same behavior. The claims-frozen predicate
counts a fixed set because the instrument author chose a fixed set. This is recorded as a
**finding**, not a cheat: it is the same closure shape round-79 carried and named "LIMIT
measurement, never a predicate", and is something a future seat can extend.

I chose **NOT** to cheat a forged receipt onto that surface (I could have edited a fresh selftest
`ORACLES_EXT` list and reached a PASS-like line). That would not be a finding against the
committed instrument, but against my own copy. The finding is that **the frozen predicate does
not discover or census its own oracle set** — it inherits it.

## 5. Verdict

- **C1 predicate confirmed** at the frozen base revision with the exact expected line and exit 0
  (receipt `legitimate-fresh2.out` / `.exit`).
- Attacks 2a, 2b, 2c (non-scoring matrices) refused, all classified as discrimination, not a
  shortcut: three receipts in the table above.
- Attack 3 (forcing a blanket refusal without losing the PASS) exhausted the probe surface I
  planned; the two strongest candidates (read-only `--work` and a `--matrix` whose bytes
  differ) are the only refusal paths the battery exposes, and neither is a legitimate-vs-forged
  semantics question — they are I/O-bound choices the battery already handles.
- **A real limit found**: the oracle set in the frozen predicate is a hard-coded constant, not a
  census. A sixth oracle outside `matrix-battery-v7.py:119` would evade the counter entirely.
  This is a documented instrument boundary, not something I reached behind the instrument to
  fake, and it matches the "enumberated set of oracles" wording in the claims' kill rule. I am
  NOT asserting it is a fresh falsification — it is an instrument *limit*, recorded.

**NOT FALSIFIED** overall on the frozen-claim surface: the predicate reproduces, the three
attack sides refused. The oracle-table finding (§4) is the only actionable C1 limit this seat
found and is newly measured this round.

## Residual risk / gaps

- `--reemit-only` and fresh-case generation are NOT exercised here (I used `--fresh 2 --runs 1`
  in the legitimate run; `--reemit-only` and generative fresh-case sweeps would belong to an
  executor seat, not a reviewer seat).
- I did not try to defeat the *witness* freshness route (draw_fresh, line 388, and its random
  `_fresh()` names). That is a critic/labout seat's surface, not a C1 scope.
- Python runtime: 3.14.8 (probe surface for `LOADER_MATRIX_CHILD_TIMEOUT` numerical parsing
  taken at face value; no string-formatted shell injection exercised).
- No tool installs: none needed this seat; all work ran under the existing `python3`/`git`/`sha256sum`
  toolchain on the host (dictating no pacman/uv installs; no tool record required).
