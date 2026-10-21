# IntegMeasurement — round 27 falsify (attempt 1)

**Seat:** `ChousaR27.IntegMeasurement-11`  
**Target revision:** `dd72641e574679c4f7882dd43de072b4c8892d6f`  
**Sandbox:** `/tmp/chousa-r27-falsify-IntegMeasurement` (base archive `64eec5d41c7cf7f17f5ce1e968e28b3769952596`)  
**Tooling:** no installs (system `python3`, `git`, `bash` only).

## Axes

| Axis | Item |
|---|---|
| Operability | C1 usage harness + mechanism count |
| Freshness | C2 date/locale/zero normalization |
| Calibration | C3 registry header / S-id / denylist |
| Measurement integrity | `round27-mechanisms.py` lexical probe vs behavioral receipts |
| Source gate | S040–S042 quotes vs r26 falsify reports |
| Case identity | Selftest cases 1–187 names/order vs base gate source |
| Token cost | 1–4 MiB `verify-metadata` wall time base vs target |
| Simplifier | Dead/duplicate helpers (read-only) |

---

## 1. Integration measurement (lexical probe)

**Verdict: FALSIFIED (as admission gate); HOLDS (as documented non-verdict counter).**

| Command | Exit | Key output |
|---|---|---|
| `python3 corpus/evidence/round27-mechanisms.py base/tools/research-gate.sh` | 0 | `claim_totals` C1=1, C2=2, C3=5; gate sha `c2c813f1…` |
| Same on `target/tools/research-gate.sh` | 0 | all mechanism counts 0; gate sha `ca39d14d…` (matches `git show dd72641:tools/research-gate.sh`) |
| Append decoy comment `# $out != *'RESEARCH_GATE: '*` to repaired gate, rerun probe | 0 | **C1=1** with all real predicates still fixed |

**Counterexample:** A trailing comment containing the C1 substring pattern makes the probe report C1=1 on an otherwise repaired gate (`mutant-gate.sh` in sandbox).

**Mutation (revert C1 predicate in sandbox copy):**

| Step | Exit | Note |
|---|---|---|
| Restore `$out != *'RESEARCH_GATE: '*` in `metadata_asof_usage_case` | — | patched `revert-c1/tools/research-gate.sh` |
| `round27-regressions.py --gate revert-c1/...` | **1** | `MISMATCH C1 correct-usage-with-help`, `MISMATCH C1 nonrecord-mention-is-not-verdict` |
| Mechanism probe on revert copy | 0 | C1=1 |

Behavioral controls fail when the lexical defect returns; the probe alone is **not** sufficient to certify repair (false positive via comment; false negative possible if patterns renamed — stated in script docstring).

**Phantom base-suite comparison:** No `round27-regressions.py` run was attempted on the base archive (script absent at `64eec5d4`; claims forbid implying a green base regression suite). Before-side mechanism count uses target’s probe script against base gate bytes only.

---

## 2. IntegSourceGate (S040–S042)

**Verdict: HOLDS (exact quoted text); scope rows remain lane inference.**

| Row | Cited file:lines | Lesson quote | Source text match |
|---|---|---|---|
| S040 | `.ufo/waves/round-26/falsify/FNoTrade.md:126–128` | “the predicate is unsatisfiable for any usage exit, and the failure is deterministic rather than flaky.” | **Exact** (lines 127–128) |
| S041 | `FDateHugeCadence.md:42–44` | “Bash's extglob `+(0)` longest-prefix match recurses in proportion to the run length.” | **Exact** (lines 42–43; line break between `` `+(0)` `` and “longest-prefix…”) |
| S042 | `FRegistryHeaderless.md:45` | “a non-pipe line sets `header_candidate=0; continue` but does not reset `id_col`/`status_col`/`usedby_col`.” | **Exact** (line 45) |

Scope cells (“code at `metadata_asof_usage_case` opened too”, ID/raw-path reports) are not verified as quotes here; they match the r26 report set named in the lesson table.

---

## 3. IntegCaseIdentity (cases 1–187, static)

**Verdict: HOLDS** for committed identity receipts; static invocation list alone does not equal runtime case numbers (inline/`tsetup` cases).

| Check | Result |
|---|---|
| `git show 64eec5d4:tools/research-gate.sh` vs `dd72641:…` — ordered runner invocations (`tcase`, `tclaims`, …, `metadata_*`) | **180 names identical**; target adds 20 new invocations after |
| `corpus/evidence/round27-selftest-after.log` case **187** | `metadata-registry-refused-nul` |
| `corpus/evidence/round26-inherited-after.log` tail | same case **187** name (FAIL 3/187 receipt) |
| `LEGACY_CASES_SHA` first 161 `ok-case` lines (r27 log) | `5eac4a7e2af964f6e81631f66990426e5c8ef58fb41ba6ec6d0054ef819e01cb` — **matches** r26 inherited log |

Runtime cases 181–187 (registry block) align with the last seven registry selftest names shared by base and target source order. Cases 188–210 are new r27 controls (expected).

**Limit:** Full 1–187 name list for base was not re-executed (`--selftest` forbidden); identity rests on legacy161 hash + matching case 187 + unchanged 180-invocation prefix.

---

## 4. IntegTokenCost (1–4 MiB synthetic source)

**Verdict: HOLDS (no material regression).**

`verify-metadata` on synthetic entry + registry under `/tmp/.../tokcost/fix` (rc=1 drift expected; timing only):

| MiB | Base ms | Target ms |
|---|---|---|
| 1 | 28 | 30 |
| 2 | 42 | 42 |
| 3 | 51 | 55 |
| 4 | 65 | 66 |

All runs &lt;120 s cap. Target not slower than base at these sizes.

---

## 5. Regression hash / receipt (target sandbox)

**Verdict: HOLDS on summary contract; full JSON file hash is run-dependent.**

```text
python3 corpus/evidence/round27-regressions.py \
  --gate target/tools/research-gate.sh \
  --output /tmp/.../regressions-after.json
exit 0
```

| Field | Sandbox | Committed `corpus/evidence/round27-regressions-after.json` |
|---|---|---|
| `gate_sha256` | `ca39d14d…` | match |
| `script_sha256` | `5afea786…` | match |
| `total` / `mismatches` | 58 / 0 | match |
| `claims` C1/C2/C3 | all mismatches 0 | match |
| Full file sha256 | `841e402c…` | `69b40668…` (**differs** — `ts=` timestamps in captured stdout) |

Use summary fields + gate/script hashes as the durable receipt; do not require byte-stable full JSON across reruns.

---

## 6. Simplifier (deletion candidates, no edits)

| Candidate | Evidence | Tradeoff |
|---|---|---|
| `metadata_asof_usage_accepts` inside `run_selftest` | Defined at ~6036; **no call sites** in gate; `round27-regressions.py` re-extracts this helper text for C1 synthetic runs | Removing it breaks regressions unless script inlines the same predicate; merge with `metadata_asof_usage_case` instead of duplicate helper |
| `is_denylist_path` vs `is_denylist_fs_path` | Both live; fs variant used on registry/metadata paths, pointer variant on citation paths | Not dead — dual authority is intentional post-C3; do not collapse without proof |

No other r27-added function (`is_denylist_path_value`, `is_denylist_fs_path`) is unused.

---

## Milestone falsify C1–C3 at dd72641

| Claim | Falsify outcome |
|---|---|
| C1 operability repair | **HOLDS** under revert test (regressions exit 1; mechanism C1→1) |
| C2 freshness repair | **INCONCLUSIVE** (no isolated revert run; static: no `##+(0)`, `LC_ALL=C` in `metadata_iso_date`) |
| C3 calibration repair | **INCONCLUSIVE** (no isolated revert; mechanism C3 counts 0 at target) |
| Measurement / no phantom base regression | **FALSIFIED** probe false-positive; **HOLDS** no phantom base suite claim |

Author-lane advice only.

Report-Trailer: `.ufo/waves/round-27/falsify/IntegMeasurement.md`
