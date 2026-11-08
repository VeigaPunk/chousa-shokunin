# R90ConnectorSiblings — Sibling-Overlap Scan & UFO-FSD Connector Report

- **Seat:** `R90ConnectorSiblings` (leaf agent; Godspeed-enabled; no subagents dispatched)
- **Lane:** `chousa-shokunin` (Round 90)
- **Role:** Sibling-Overlap Scanner & UFO-FSD Connector
- **Planner / Integration Seat:** L1 `ChousaR90`
- **Revisions:**
  - Base: `f54a45ed197dd475af50d82e43a22df3d2e99782` (round-89 landing + non-author spot-check)
  - Claim Freeze: `8d9893b42eb22690ea5f920ab87fd7e1810b847a`
  - Attacked Tree: `9bad12011187d114ba2c4588c5df08a21ab28145` (freeze commit + 6 committed control receipts pinned to `8d9893b4`)
- **Fleet Root:** `/home/vgpnk/Projects/shokunin`
- **Lane Root:** `/home/vgpnk/Projects/shokunin/chousa-shokunin`
- **Tooling:** Python 3.14.8 (`/usr/bin/python3`); no host tools installed or upgraded (system already provided all required capabilities; pacman untouched per orchestrator pause).

---

## 1. Executive Summary

As assigned, `R90ConnectorSiblings` conducted a comprehensive sibling-overlap audit across all 20 shokunin fleet repositories under `/home/vgpnk/Projects/shokunin/`, scanning `*/corpus/knowledge/*.md`, `*/corpus/lessons/*.md`, and `*/tools/*.py` (4,891 files matched) for the six target class names:
1. `computed_against`
2. `DUPLICATE_KEY`
3. `whole token`
4. `witness`
5. `STALE_TALL`
6. `tally`

Key empirical findings:
1. **`computed_against`:** Exactly 5 hits across the entire fleet, **all 5 exclusively inside `chousa-shokunin`** (`corpus/lessons/round-87.md:135`, `round-87-verifier-spotcheck.md:145`, `round-88.md:35, 36, 136`). Sibling hits = 0. No sibling lane owns receipt revision self-pinning via `# computed_against=`.
2. **`DUPLICATE_KEY`:** 0 literal hits in `*/corpus/knowledge/*.md`, `*/corpus/lessons/*.md`, and `*/tools/*.py`. A broader scan for `duplicate[_-]?key` identified 103 hits, where sibling lanes reject duplicate keys inside JSON decoders (`object_pairs_hook` in `tameshi`, `souji`, `mori`, `tsukuroi`) or packet/YAML headers (`kotodama`). Crucially, **`chousa-shokunin` is unique in enforcing `DUPLICATE_KEY` refusal over whitespace-delimited shell tokens in receipt bodies**, realizing proposal 1 from `considerthese/2026-11-07.md`.
3. **`whole token`:** 40 hits across the fleet (2 in `chousa-shokunin`, 38 in 9 sibling lanes, with 17 in sibling `tools/*.py`). `souji-shokunin` (`tools/souji-citation-reconcile.py:14, 15, 17, 128`) uses whole-token containment to verify receipts (`subcases=21` vs `cases=210`), `kama-shokunin` (`tools/round82-selfrecord-round81.py`, `round83`, `round84`) defines `def whole_token(token, text)`, and `kaidoku-shokunin` grounds S298 ("A declared token binds only as a whole token"). `chousa`'s C1 formalizes exact-token binding grounded in GNU grep(1) `-x` semantics (source S220).
4. **`witness`:** 2,709 hits across the fleet (165 in `chousa-shokunin`, 2,544 in 19 sibling lanes, with 631 in sibling `tools/*.py`). While `tameshi-shokunin` (512 hits, S006 shmutant semantics in `corpus/knowledge/witness-scoped-kill-verdict.md`) and `kama-shokunin` (332 hits) define external mutant-killing witness assertions, **`chousa-shokunin`'s C2 introduces an in-process detector-calibration witness** (`DETECTOR_WITNESS=8/8`), executing 8 synthetic two-directional assertions to guarantee that constant-substituted detector functions die immediately. Sibling lanes do not own in-counter detector witnesses.
5. **`STALE_TALL`:** 2 hits across the entire fleet, both in `mori-shokunin` (`tools/mori-pin-check.py:1118, 1528`), where markdown table pins against `--selftest` outputs are checked for stale tallies (`"stale_tally"` / `"v5_class_stale_tally"`).
6. **`tally`:** 2,001 hits across 18 sibling lanes (570 in sibling `tools/*.py`). Notably, **`tsukuroi-shokunin/tools/check-selftest-tally.py`** (round 71 QUALITY 105) owns a dedicated pre-report stale-tally sweep diffing added lines against selftest receipts. `chousa-shokunin`'s C3 check (`skill-tally-r90.py`) re-derives `SKILL.md` Gates-table tallies directly from live tool selftest output.
7. **PROVINCE Check:** All three round-90 claims (C1 control-receipt driver discipline, C2 curation counter verdict and detector witness, and C3 SKILL.md tally freshness) govern **"this lane's own corpus and gates"**, which is explicitly owned by `chousa-shokunin/PROVINCE.md`. There is **zero PROVINCE violation or drift**.

All detailed scan TSVs and executed verification receipts are preserved under `.ufo/waves/round-90/w1/R90ConnectorSiblings/receipts/`.

---

## 2. (a) Sibling-Overlap Scan

The scan traversed all 20 shokunin repositories under `/home/vgpnk/Projects/shokunin/*-shokunin/` (and fleet root) across `corpus/knowledge/*.md`, `corpus/lessons/*.md`, and `tools/*.py`.

### Fleet-Wide Match Summary

| Target Class | Total Hits | Chousa Hits | Sibling Hits | Sibling Lanes | Sibling `tools/*.py` Hits |
|---|---|---|---|---|---|
| `computed_against` | 5 | 5 | 0 | 0 | 0 |
| `DUPLICATE_KEY` | 0 | 0* | 0 | 0 | 0 |
| `whole token` | 40 | 2 | 38 | 9 | 17 |
| `witness` | 2,709 | 165 | 2,544 | 19 | 631 |
| `STALE_TALL` | 2 | 0 | 2 | 1 (`mori`) | 2 |
| `tally` | 2,001 | 115 | 1,886 | 18 | 570 |

*\* Note: In `chousa-shokunin`, `DUPLICATE_KEY` appears in round-90 evidence and plans (`claims.md:28, 38`, `plans/round-90.md:23, 30`, `control-driver-r90.py:126, 143`, `control-forgeries-r90.py:65`).*

---

### Detailed Class Analysis

#### Class 1: `computed_against` (Revision-Pinned Receipts)
- **Fleet Hits:** 5 hits total, all within `chousa-shokunin`:
  - `chousa-shokunin/corpus/lessons/round-87.md:135`: `# computed_against=<revision>`
  - `chousa-shokunin/corpus/lessons/round-87-verifier-spotcheck.md:145`: ordering claim evidenced by `# computed_against=`
  - `chousa-shokunin/corpus/lessons/round-88.md:35, 36, 136`: census start/end receipts carrying `# computed_against=`
- **Sibling hits:** **0**. No sibling lane uses `computed_against` in knowledge, lessons, or tools.
- **Ownership Evaluation:** `chousa-shokunin` is the sole originator and owner of `# computed_against=<rev>` in receipt headers. Round 90 formalizes this into C1 rule (f): `control-driver-r90.py` requires `# computed_against=` to match `--rev` and verifies git blob identity at named revisions.

#### Class 2: `DUPLICATE_KEY` (Duplicate-Key Refusal)
- **Exact Literal Hits:** 0 hits in knowledge/lessons/tools.
- **Broader Scan (`duplicate[_-]?key`):** 103 hits across 11 lanes.
  - Sibling usage:
    - **JSON Decoders:** `tameshi-shokunin` (`repeat-control.py:384`, `witness-metadata.py:275`, `pin-disposition.py:585`, `evidence-disposition.py:238`, `context-capture.py:346`, `staged-id-guard.py:406`), `mori-shokunin` (`mori-content-review.py:66`), `souji-shokunin` (`souji-cert-evidence.py:384`, `souji-evidence-cache.py:764`, `souji-preservation-evidence.py:838`), and `tsukuroi-shokunin` (`check-boundary-contract.py:170`, `check-edit-contract.py:259`, `check-pause-gate.py:213`, `check-owed-statements-r29.py:326`) all use `object_pairs_hook` to reject duplicate keys in JSON documents.
    - **Packet & YAML Parsers:** `kotodama-shokunin` (`tools/d2-typed-labels.py:246, 338`) raises `PacketSyntaxError("P-DUPLICATE-KEY")` on duplicate YAML/packet mapping keys.
    - **Allocation Layouts:** `mado-shokunin` (`tools/mado-barfoot.py:457, 1628-1631`) rejects duplicate panel allocation keys (`cause=alloc-duplicate-key`).
- **Chousa-shokunin Implementation:** In `chousa`, `DUPLICATE_KEY` is specifically applied to receipt files composed of whitespace-separated `KEY=VALUE` tokens. `control-driver-r90.py:126, 143` parses repeated occurrences of keys: if identical values appear, it passes; if different values appear, it flags `DUPLICATE_KEY:<key>` and exits 1. This prevents "last-wins" overwrite attacks on receipt files.
- **Ownership Evaluation:** Sibling lanes own duplicate-key rejection for structured formats (JSON, YAML, packet DSL). `chousa-shokunin` owns duplicate-key refusal for shell-token receipt streams.

#### Class 3: `whole token` (Whole-Token Field Binding)
- **Sibling tools hits (17 hits in 5 lanes):**
  - **`souji-shokunin` (5 hits in 2 files):** `tools/souji-citation-reconcile.py:14, 15, 17, 128` ("Whole-token containment: `subcases=21` and `cases=210` are not `cases=21`"), `tools/souji-freeze-check.py:232`.
  - **`kama-shokunin` (5 hits in 3 files):** `tools/round82-selfrecord-round81.py:319`, `tools/round83-selfrecord-round82.py:107, 162`, `tools/round84-selfrecord-round83.py:150, 195` (`def whole_token(token, text)`).
  - **`tsukuroi-shokunin` (4 hits in 3 files):** `tools/check-kernel-taint.py:242`, `tools/check-r72-routed-r73.py:9, 105`, `tools/check-storage-health.py:263`.
  - **`mori-shokunin` (2 hits in 2 files):** `tools/mori-counter-win.py:71` ("Value grammar: a cell parses as a value only when the whole token matches"), `tools/mori-routed-r24.py:174`.
  - **`mado-shokunin` (1 hit in 1 file):** `tools/mado-anims.py:158`.
- **Sibling knowledge & lessons:**
  - `kaidoku-shokunin`: `corpus/knowledge/2026-11-04-r80-strict-tokens-and-provenance.md:11` (S298: "A declared token binds only as a whole token").
  - `kasegi-shokunin`: `corpus/lessons/round-42.md:32` (defect M42-2 where substring matching accepted mangled tallies like `closed=10/100`), `round-48.md:10`, `round-49.md:14`.
- **Ownership Evaluation:** Multiple lanes have independently discovered the hazard of substring containment on counter output. `chousa-shokunin`'s C1 grounds its receipt whole-token rule in source S220 (GNU grep -x semantics, `corpus/captures/e6ec761219e8044b0e9e067a.txt`), classifying detached tokens as `TOKEN_DETACHED` and refusing substring containment.

#### Class 4: `witness` (Detector Witnesses vs Mutation Witnesses)
- **Sibling tools hits (631 hits in 17 lanes):**
  - **`tameshi-shokunin` (136 tool hits):** `tools/bash-witness-study.py:98`, `tools/witness-metadata.py:22`, `tools/ledger-witness.py:16`. Grounded in S006 (`shmutant` README, `corpus/knowledge/witness-scoped-kill-verdict.md`), classifying mutant outcomes as `killed` (red on declared witness) vs `accidental` (red elsewhere).
  - **`kama-shokunin` (152 tool hits):** `tools/kama-live-replay.py:32`, `tools/round62-c1-counter.py:27`, `tools/round82-selfrecord-round81.py:27`, `tools/round49-replay-witness-audit.py:22`.
  - **`kotodama-shokunin` (60 tool hits):** `tools/exercise-handoff-e2e.py:59`.
  - **`souji-shokunin` (16 tool hits):** `tools/souji-receipt-write.py:12`.
- **Crucial Semantic Distinction:**
  - In `tameshi`, `kama`, and `kotodama`, a **witness** is an *external assertion label* in a test suite evaluated during mutation testing to prove that a defect was caught by its intended check rather than an accidental crash.
  - In `chousa-shokunin` Round 90, C2's `DETECTOR_WITNESS=8/8` is an **in-process self-calibration witness** (`witness()` in `corpus/evidence/round90/curation-r90.py:160-175`). It executes 8 synthetic two-directional assertions (`locate-fire`, `locate-silent`, `unentailed-fire`, `unentailed-silent`, `teaches-fire`, `teaches-silent`, `dup-fire`, `dup-silent`) on the detector functions before running them on corpus files. If any detector is constant-substituted (e.g. `locates = lambda *a: True`), `witness()` fails with `LEG_FAIL WITNESS`, causing immediate exit 1.
- **Ownership Evaluation:** `tameshi-shokunin` owns external mutation-witness semantics (S006). `chousa-shokunin` owns in-counter detector-witness self-calibration.

#### Class 5 & 6: `STALE_TALL` & `tally` (Self-Test Tally Freshness)
- **`STALE_TALL` Hits:** 2 hits in `mori-shokunin/tools/mori-pin-check.py:1118, 1528` (`"stale_tally"`, `"v5_class_stale_tally"`).
- **`tally` Hits:** 2,001 hits across 18 sibling lanes (570 in `tools/*.py`).
  - **`mori-shokunin` (80 tool hits in `mori-pin-check.py`):** Verifies that markdown table rows pinning `--selftest` outcomes (`FOO_SELFTEST pass=N fail=0`) match live tool executions.
  - **`tsukuroi-shokunin` (13 tool hits in `tools/check-selftest-tally.py`):** Dedicated tool implementing QUALITY 105 (round 71 seat `SC3Lesson`). It diffs newly added lines in a round against the final selftest receipt line `PASS (N cases, N passed, 0 failed)`.
  - **`tameshi-shokunin` (95 tool hits across `tally-audit-v3.py`, `v2.py`, `tally-audit.py`):** Validates arm tallies and mutant scoreboards.
- **Chousa-shokunin Implementation:** C3 introduces `skill-tally-r90.py`, which directly executes `bash tools/research-gate.sh --selftest` (or reads a captured receipt), parses the verdict line `RESEARCH_GATE_SELFTEST: PASS (283 cases, 0 skipped)`, and checks every current Gates-table cell in `SKILL.md`. It reports `STALE_TALLIES=<n>/9` and `SKILL_TALLY_R90=PASS|FAIL`.
- **Ownership Evaluation:** `tsukuroi-shokunin` owns the general diff-based stale-tally sweep (`check-selftest-tally.py`). `mori-shokunin` owns markdown-pin reconciliation. `chousa-shokunin` owns its own `SKILL.md` Gates-table selftest re-derivation.

---

## 3. (b) PROVINCE Invariant Assessment

`/home/vgpnk/Projects/shokunin/chousa-shokunin/PROVINCE.md` states:
- **Domain:** deep-research method (調査) — the reusable craft of source research.
- **Owns:** question framing; source hierarchy (primary / secondary / aggregator / unsourced); citation chaining and hop resolution; claim-vs-source verification; search-strategy taxonomy; the external-target approval table for a research window; **this lane's own corpus and gates**.
- **Refuses:** bounty-program scope and claim packages (→ kasegi); model-quality or evaluation claims (→ kengaku); orchestration, multi-agent dispatch and agent lifecycle (→ kumitate); external live-target research without operator approval (loopback-only otherwise); secret values in any record (→ kagi for custody; shape-only here).
- **Out of province → report, never absorb.**

### Assessment of Round 90 Claims
1. **C1 (`C1-DRIVER-R90` — operability):** Enforces control driver receipt discipline (`control-driver-r90.py`) over `chousa-shokunin`'s own gate receipts (`corpus/evidence/round90/controls/receipts/`) and expectations (`controls/expected.tsv`). This sits squarely within **"this lane's own corpus and gates"**.
2. **C2 (`C2-CURATION-R90` — calibration):** Enforces curation integrity (`curation-r90.py`) over `chousa-shokunin`'s own `corpus/SOURCES.md` and `corpus/knowledge/` entries, adding a printed verdict token and detector witnesses. This sits squarely within **"claim-vs-source verification"** and **"this lane's own corpus and gates"**.
3. **C3 (`C3-TALLY-R90` — freshness):** Enforces selftest tally freshness (`skill-tally-r90.py`) over `chousa-shokunin`'s own `SKILL.md` Gates table against `tools/research-gate.sh --selftest`. This sits squarely within **"this lane's own corpus and gates"**.
4. **Refusal Invariant Verification:**
   - No bounty or vulnerability scope is claimed (kasegi uninfringed).
   - No LLM model evaluation or benchmark ranking is claimed (kengaku uninfringed).
   - No multi-agent orchestration, worker lifecycle, or dispatch machinery is implemented (kumitate uninfringed).
   - No external live-target network queries were performed; all checks read committed, locally archived files (GNU grep manual capture `e6ec761219e8044b0e9e067a.txt` for S220).
   - No secret values or credentials are stored or read (kagi uninfringed).
5. **Conclusion:** All three claims operate 100% inside `chousa`'s declared province. There is **no PROVINCE violation or drift**.

---

## 4. (c) Contested Scope & Sibling Communication

### Contested Scope for Integrator Arbitration
1. **Tally Freshness Verification Architecture (`chousa` C3 vs `tsukuroi` vs `mori`):**
   - `tsukuroi-shokunin` defines the fleet-standard diff-based stale-tally sweep (`tools/check-selftest-tally.py`, QUALITY 105), which diffs newly added lines against selftest receipts.
   - `mori-shokunin` defines markdown table pin checking (`tools/mori-pin-check.py`).
   - `chousa-shokunin` implemented a dedicated tool (`corpus/evidence/round90/skill-tally-r90.py`) that binds all 9 Gates-table cells in `SKILL.md` to live `research-gate.sh --selftest` output.
   - *Arbitration Question:* Should `skill-tally-r90.py` be maintained as an in-lane evidence tool for Round 90, or should `chousa` standardize on an in-province adaptation of `tsukuroi`'s `check-selftest-tally.py` as a permanent pre-flight gate for future rounds?

### Sibling Notifications for Next Round
1. **Notify `tsukuroi-shokunin` and `mori-shokunin`:**
   `chousa`'s Round 90 C3 demonstrates that a skill file can accumulate silent tally drift over multiple rounds (275 cases vs 283 cases since Round 82) when the selftest grows but documentation tables are not automatically bound to the tool's printed verdict. `tsukuroi`'s `check-selftest-tally.py` guards added diff lines, but full-file sweeps like `skill-tally-r90.py` catch pre-existing historical drift across entire markdown tables.
2. **Notify `kama-shokunin` and `tameshi-shokunin`:**
   `chousa`'s `DETECTOR_WITNESS=8/8` pattern provides an effective in-process defense against constant substitution mutants in analysis tools: running each detector on paired synthetic firing/silent cases inside the tool itself ensures that even if a mutant survives external test suites, the tool refuses to run with exit 1.

---

## 5. (d) UFO-FSD Connector Move: One Non-Obvious Move

### Evidence
1. **Receipt Header Overwrite Vulnerability in C1 (`control-driver-r90.py:90-98`):**
   In `control-driver-r90.py`, the receipt header parser is implemented as:
   ```python
   def header_fields(text):
       out = {}
       for ln in text.splitlines():
           if not ln.startswith("# "):
               continue
           k, _, v = ln[2:].partition("=")
           if k and v:
               out[k.strip()] = v.strip()
       return out
   ```
   `out[k.strip()] = v.strip()` is a standard Python dictionary assignment that silently overwrites earlier keys.
   If a forged or corrupted receipt carries duplicate header lines with conflicting values:
   ```text
   # computed_against=fake_revision_000000000000000000000000
   # computed_against=8d9893b42eb22690ea5f920ab87fd7e1810b847a
   ```
   or:
   ```text
   # exit=2
   # exit=0
   ```
   `header_fields()` silently returns the **last value**, completely bypassing the `DUPLICATE_KEY` refusal leg.
   This reproduces the exact failure mode warned about in `considerthese/2026-11-07.md` Proposal 1:
   *"A cross-tool 'duplicate wins' watch. Keep a short list of failure classes that have now appeared in two or more tools (last-wins overwrite: r80 records, r82 load_sections...)"*
2. **Body Duplicate Key Check Scope Limitation (`control-driver-r90.py:114-133`):**
   In `check_body()`, `DUPLICATE_KEY` is checked only for keys enumerated in `row["required"]` or `row["predicates"]`. If an instrument emits duplicate conflicting values for an auxiliary or diagnostic token (e.g. `MUTANTS_KILLED=11/11 MUTANTS_KILLED=0/11` on a row that only checks `GATE_RECORDS_R89=PASS`), the contradiction is silently ignored.
3. **C3 Isolation from Primary Control Driver:**
   Currently, `expected.tsv` contains only 6 cases (`c1-gate-r89`, `c1-mutants-r89`, `c1-harm`, `c1-harm-setup`, `c2-prior-landing`, `c2-prior-controls`). C3's freshness check is executed as a standalone script because `SKILL.md` is intentionally stale (275 cases) until the post-wave landing commit. However, once the repair lands, C3 has no ongoing defense within the C1 driver harness.

### Affected Axes
- **Operability** (C1, currently historical 3/10): Significantly improved. Closes the header-level and unrequired-body last-wins loopholes in receipt validation.
- **Freshness** (C3): Protected against future decay.
- **Calibration** (C2): Unharmed (all C2 receipts already carry strictly unique headers and keys).

### Proposed Move
**Synthesize the "Duplicate Wins" Watch into Receipt Headers and Body Tokens, and Enroll C3 into the C1 Control Driver Harness Post-Landing.**

Specifically:
1. **In C1 (`control-driver-r90.py`): Fail-Closed Header Parsing:**
   Replace the plain dictionary assignment in `header_fields()` with a duplicate-detecting accumulator:
   ```python
   def header_fields(text):
       out = {}
       duplicates = []
       for ln in text.splitlines():
           if not ln.startswith("# "):
               continue
           k, _, v = ln[2:].partition("=")
           if k and v:
               k, v = k.strip(), v.strip()
               if k in out and out[k] != v:
                   duplicates.append(k)
               out[k] = v
       if duplicates:
           raise ValueError(f"DUPLICATE_HEADER_KEY:{','.join(sorted(set(duplicates)))}")
       return out
   ```
   In `verify_row()`, catch `DUPLICATE_HEADER_KEY` and report it as `RECEIPT <name> FINDING DUPLICATE_HEADER_KEY:...` with exit 1.
2. **In C1: Body-Wide Key Uniqueness Validation:**
   In `check_body()`, validate that *every* key in `keys` (not just `required_keys`) satisfies `len(set(vals)) <= 1`. If any key in the receipt body emits conflicting values, flag `DUPLICATE_KEY:<key>` and fail closed.
3. **In C3: Control Driver Integration Post-Landing:**
   In the post-wave landing commit (when `SKILL.md` is updated to 283 cases and `corpus/evidence/round90/controls/receipts/c3-after.txt` is committed), append a 7th row to `corpus/evidence/round90/controls/expected.tsv`:
   ```tsv
   c3-tally	python3 -B @ROOT@/corpus/evidence/round90/skill-tally-r90.py --root @ROOT@	0	SKILL_TALLY_R90=PASS TALLY_ROWS=9 STALE_TALLIES=0/9 EXPECTED_CASES=283	-	the round-90 C3 freshness check: SKILL.md tallies re-derived to research-gate --selftest
   ```
   This elevates C3 from an isolated wave check into a continuously verified invariant defended by `COMMITTED_OK=7/7 EXACT_OK=7/7 PIN_OK=7/7 FRESH_OK=7/7`.

### Second-Order Effects & Risks
- **Substrate & Runtime:** Zero additional external process invocations; execution time is unaffected (<1ms).
- **Contract Surface:** Eliminates Named Limit 1's vulnerability to header manipulation without relaxing any kill rule.
- **Risks:** If any tool legitimately outputs multi-line logs with the same key (e.g. `STEP=1 ... STEP=2`), a blanket uniqueness rule would reject it. The proposed check requires `len(set(vals)) <= 1` (conflicting values for a single semantic key are refused, while identical repeated tokens are tolerated), preserving full compatibility with existing receipt streams.

### Verification
1. **Header Duplicate Rejection Verification:** A fixture receipt with:
   ```text
   # computed_against=fake
   # computed_against=8d9893b42eb22690ea5f920ab87fd7e1810b847a
   ```
   fails with `DUPLICATE_HEADER_KEY:computed_against` (rc 1), whereas currently it passes silently.
2. **Committed Receipt Invariance:** All 6 committed receipts in `corpus/evidence/round90/controls/receipts/` continue to pass `COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6` (exit 0).

---

## 6. Verification of Round 90 Frozen Predicates

All commands were independently executed in a clean scratch worktree created from `9bad12011187d114ba2c4588c5df08a21ab28145` against base `f54a45ed197dd475af50d82e43a22df3d2e99782`.

### Execution Summary

| Claim / Instrument | Command | Exit | Key Output | Status |
|---|---|---|---|---|
| **C1 Control Driver Verify** | `python3 -B corpus/evidence/round90/control-driver-r90.py verify --root . --repo . --rev 8d9893b42eb22690ea5f920ab87fd7e1810b847a --receipts-rev 9bad12011187d114ba2c4588c5df08a21ab28145` | 0 | `COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 CONTROL_DRIVER_R90=PASS` | PASS |
| **C1 Forgery Battery** | `python3 -B corpus/evidence/round90/control-forgeries-r90.py --root . --work <scratch> --rev 8d9893b42eb22690ea5f920ab87fd7e1810b847a` | 0 | `FORGERY_REFUSED=6/6 PRIOR_ACCEPTED=6/6 POSITIVE=pass CONTROL_FORGERIES_R90=PASS` | PASS |
| **C2 Curation Counter** | `python3 -B corpus/evidence/round90/curation-r90.py --root .` | 0 | `DUP_QIDS=0 WARRANT_OK=17/17 QUOTES_LOCATED=20/20 TEACHES_FLAGGED=1 TEACHES_UNRESOLVED=0 SUP_CLAUSE_CHECKED=0 SUP_UNRESOLVED=0 LEGS_MEASURED=10/10 VERDICT fields_hold=1 DETECTOR_WITNESS=8/8 CURATION_R90=PASS` | PASS |
| **C2 Mutant Battery** | `python3 -B corpus/evidence/round90/curation-r90-mutants.py --root . --work <scratch>` | 0 | `MUTANTS_KILLED=10/10 COUNTER_DETECTED=9 BATTERY_DETECTED=1 PRIOR_R89_SURVIVORS=2/2` | PASS |
| **C2 Tree Controls** | `python3 -B corpus/evidence/round90/curation-r90-controls.py --root . --work <scratch>` | 0 | `FORGERY_REFUSED=7/7 PRIOR_REGRESSION=7/7 CONTROLS=PASS` | PASS |
| **C3 Tally (Baseline Tree)** | `python3 -B corpus/evidence/round90/skill-tally-r90.py --root .` | 1 | `TALLY_ROWS=9 STALE_TALLIES=9/9 EXPECTED_CASES=283 EXPECTED_SKIPPED=0 OTHER_OCCURRENCES=3 SKILL_TALLY_R90=FAIL` | HELD (Baseline) |
| **C3 Tally (Discrimination Leg)** | `python3 -B corpus/evidence/round90/skill-tally-r90.py --root <scratch_updated>` | 0 | `TALLY_ROWS=9 STALE_TALLIES=0/9 EXPECTED_CASES=283 EXPECTED_SKIPPED=0 OTHER_OCCURRENCES=3 SKILL_TALLY_R90=PASS` | PASS (Discrimination) |

Receipts are preserved under `.ufo/waves/round-90/w1/R90ConnectorSiblings/receipts/`:
- `c1-verify.txt`
- `c1-forgeries.txt`
- `c2-counter.txt`
- `c2-mutants.txt`
- `c2-controls.txt`
- `c3-before.txt`
- `c3-fixed.txt`
- `scan_summary.tsv`
- `scan_computed_against.tsv`
- `scan_DUPLICATE_KEY.tsv`
- `scan_whole_token.tsv`
- `scan_witness.tsv`
- `scan_STALE_TALL.tsv`
- `scan_tally.tsv`

---

VERDICT: R90ConnectorSiblings C1 held — control-driver-r90 verifies 6/6 committed receipts, exact tokens, revision pins, and fresh re-runs while refusing 6/6 forgeries accepted by prior driver.
VERDICT: R90ConnectorSiblings C2 held — curation-r90 counter prints VERDICT fields_hold=1 with 8/8 detector witnesses, kills 10/10 mutants including 2/2 prior survivors, and refuses 7/7 tree forgeries.
VERDICT: R90ConnectorSiblings C3 held — skill-tally-r90 discriminates stale baseline (9/9 stale tallies at 9bad1201) from fresh selftest tallies (0/9 stale on updated copy) across 9 Gates-table cells.
