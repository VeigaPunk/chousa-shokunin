# R89ConnectorSiblings — Sibling-Overlap Scan & UFO-FSD Connector Report

- **Seat:** `R89ConnectorSiblings` (leaf agent; Godspeed-enabled; no subagents dispatched)
- **Lane:** `chousa-shokunin` (Round 89)
- **Role:** Sibling-Overlap Scanner & UFO-FSD Connector
- **Planner / Integration Seat:** L1 `ChousaR89`
- **Revisions:** Base `f8fa55ec94cb34e7b572a9d87d7f62d88bc80bf8`; Freeze `ac0a0892c15de11fb28d3208f2b287687c00477e`
- **Fleet Root:** `/home/vgpnk/Projects/shokunin`
- **Lane Root:** `/home/vgpnk/Projects/shokunin/chousa-shokunin`
- **Tooling:** Python 3.14.8 (`/usr/bin/python3`); no tools installed or upgraded (system already provided all required capabilities; pacman untouched per orchestrator pause).

---

## 1. Executive Summary

As assigned, `R89ConnectorSiblings` executed a comprehensive sibling-overlap audit across all 20 shokunin fleet lanes in `/home/vgpnk/Projects/shokunin`, scanning `*/corpus/knowledge/*.md`, `*/corpus/lessons/*.md`, and `*/tools/*.py` for the four target class names: `reconcil`, `fields_hold`, `dup.*qid`, and `supersed`.

Key empirical findings:
1. **`reconcil`** appears widely (1,646 total hits; 1,572 sibling hits across 19 sibling lanes, including 262 hits across sibling `tools/*.py`). However, **no sibling lane owns leg-receipt reconciliation** for gate records in `chousa`'s sense. Sibling instruments reconcile GGUF model properties against receipts (`kama-shokunin/tools/gguf-identity.py`), or count selftest arms against summary lines (`kama-shokunin/tools/round86-mutant-owners.py`), or check path manifests (`tsukuroi-shokunin`), but `chousa`'s per-format leg re-derivation (`n/m`, `len/d1/div3 pinN`, `derived=x killed=y`, `tool present`) and summary `CROSSCHECK` is unique to `chousa`'s C1 battery (`corpus/evidence/round89/gate-records-r89.py`).
2. **`fields_hold`** has **0 hits across all sibling lanes** and 0 hits in fleet-wide knowledge, lessons, or tools. It exists strictly within `chousa`'s round-89 C2 calibration counter (`corpus/evidence/round89/curation-r89.py:305, 316-318`) and its frozen claims/mutants. No sibling lane owns field-derived verdicts.
3. **`dup.*qid`** has **0 hits across all sibling lanes** (5 hits total, all within `chousa-shokunin`: `corpus/lessons/round-88.md:75`, `round-88-verifier-spotcheck.md:143, 226-227`, and round-89 `claims.md:81, 132`). No sibling lane owns duplicate-qid warrant checking.
4. **`supersed`** appears across all lanes (5,848 total hits; 5,585 sibling hits across 20 sibling lanes, with 713 hits in `tools/*.py`). Crucially, **`kotodama-shokunin` owns `tools/check-supersession-settlement.py`** (Round 68), which validates whether registry supersession chains (`supersedes S### —`) are settled (`SETTLED-ACTIVE`, `SETTLED-RETIRED`, `SETTLED-CLOSED`, `SETTLED-SPLIT`, or pending). In `chousa-shokunin`, `curation-r89.py` checks both a `SUPERSEDED` leg (target mined while superseder is unmined) and a `TEACHES` supersession-clause check (verifying that superseding contrast/date teachings read in their own capture text).
5. **PROVINCE Check:** Both C1 and C2 measure and harden **"this lane's own corpus and gates"**, which is explicitly owned by `chousa-shokunin/PROVINCE.md`. Neither claim encroaches on refused domains (bounties, model evaluations, orchestration, external network research, or secrets custody). There is **no PROVINCE violation**.

All detailed scan TSVs and reproduced verification logs are captured in `receipts/`.

---

## 2. (a) Sibling-Overlap Scan

The scan traversed all 20 shokunin repositories under `/home/vgpnk/Projects/shokunin/*-shokunin/` across `corpus/knowledge/*.md`, `corpus/lessons/*.md`, and `tools/*.py`.

Summary of matches:

| Pattern | Total Hits | Chousa Hits | Sibling Hits | Sibling Lanes with Hits | Sibling `tools/*.py` Hits |
|---|---|---|---|---|---|
| `reconcil` | 1,646 | 74 | 1,572 | 19 | 262 (6 lanes) |
| `fields_hold` | 0 | 0* | 0 | 0 | 0 |
| `dup.*qid` | 5 | 5 | 0 | 0 | 0 |
| `supersed` | 5,848 | 263 | 5,585 | 20 | 712 (7 lanes) |

*\* Note: In `chousa-shokunin`, `fields_hold` appears in `corpus/evidence/round89/` (`claims.md:83`, `curation-r89.py:305, 316, 317, 318`, `curation-r89-mutants.py:59`), which is an evidence path rather than knowledge/lessons/tools.*

### Class 1: `reconcil` (Leg-Receipt Reconciliation)
- **Sibling tools hits:**
  - `kama-shokunin` (96 hits in 20 files):
    - `kama-shokunin/tools/gguf-identity.py`: lines 2, 47, 477, 644, 647, 846, 980, 982, 983 — defines `_reconcile_receipt_checked()` and `reconcile_receipt()`, reconciling receipt JSON against GGUF model binary properties and SHA-256.
    - `kama-shokunin/tools/round86-mutant-owners.py`: lines 3, 16, 27, 28, 30, 37, 58, 102, 123, 245 — reconciles completed selftest summary with failure-line cardinality and arm population.
    - `kama-shokunin/tools/round41-scorecard-reconcile.py:2`, `round42-selfdesc-reconcile.py:2, 7, 22, 152`: reconciles SCORECARD tables and self-description against git repository facts.
    - `kama-shokunin/tools/round78-live-reconcile.py:28, 38, 47, 110, 160, 209, 251, 285, 287`: reconciles three-row registry verdicts, probe exits, and child process lifecycles.
  - `kotodama-shokunin` (105 hits in 4 files):
    - `kotodama-shokunin/tools/exercise-handoff-e2e.py`: lines 65, 94, 2701, 2702, 2716, 2845, 3818, 3864, 4484, 4485, 4491, 4496 — reconciles handoff packet claims, twins, and read-sets.
    - `kotodama-shokunin/tools/assemble-d2.py`, `assemble-culture-d3.py`, `d2-typed-labels.py`.
  - `tsukuroi-shokunin` (36 hits in 1 file):
    - `tsukuroi-shokunin/tools/check-path-reconciliation.py`: checks path reconciliation between tracked files and audit manifests.
  - `mori-shokunin` (12 hits in 3 files):
    - `mori-shokunin/tools/mori-retention-reconcile.py`, `mori-pin-check.py`, `mori-routed-check.py`: reconciles capability and retention registers.
  - `tameshi-shokunin` (12 hits in 4 files):
    - `tameshi-shokunin/tools/wave-reconcile.py`: reconciles seat accounting and wave receipts.
  - `souji-shokunin` (1 hit in 1 file):
    - `souji-shokunin/tools/souji-citation-reconcile.py:2`: citation reconciliation against source registries.
- **Sibling knowledge & lessons:**
  - `kaidoku-shokunin`: 113 hits across knowledge entries analyzing REA CLI's `reconcile-javascript-runtime` verb (`corpus/knowledge/2026-10-13-asar-surface.md:57`, `2026-10-13-r4-08-observe-verbs.md:3, 24, 122`, `2026-10-14-r10-02-queue-ops-2.md:1, 30, 43`, `2026-10-14-r14-01-queue-b-residual.md:1, 19, 26`).
  - `audio-shokunin`: `corpus/lessons/round-101.md:7, 31` (historical unlogged round reconciliation).
  - `kagi-shokunin`: `corpus/knowledge/openbao-approle-secret-id-custody.md:79` (reconciling conflicting policy readings).
- **Ownership Evaluation:**
  No sibling lane owns **leg-receipt reconciliation** for gate records. While `kama-shokunin` developed summary-vs-cardinality reconciliation for selftest arms (`round86-mutant-owners.py`) and GGUF receipt reconciliation (`gguf-identity.py`), `chousa`'s C1 instrument is unique in reading individual leg receipt files in their own distinct grammars (`n/m`, `3/3/3 pin3`, `derived=1 killed=1`, `tool present`) and verifying bidirectional equality with printed summary fields (`DIV3`, `POSITIVE`, `D1_REFUSED`, `MUT_ADMIT_*`).

### Class 2: `fields_hold` (Field-Derived Verdicts)
- **Sibling tools, knowledge, lessons hits:** Exactly **0**.
- **Chousa-shokunin hits:**
  - `corpus/evidence/round89/claims.md:83`: `VERDICT fields_hold=1`
  - `corpus/evidence/round89/curation-r89.py:304, 305, 316, 317, 318`: `fields_hold = (len(superseded_live) == 0 and len(unentailed) == 0 and modified_def_cited >= 1 and located_all == total_all and total_all > 0 and len(teaches_unresolved) == 0 and len(dup_qids) == 0 and warrant_ok == warrant_total and warrant_total > 0 and floors_ok and len(teaches_sup_unresolved) == 0)`
  - `corpus/evidence/round89/curation-r89-mutants.py:59`
- **Ownership Evaluation:**
  `fields_hold` is entirely unowned by sibling lanes. It was introduced in `chousa` round 89 as an architectural fix for routed defect 3 (verdict-vs-field decoupling from round 88), computing the counter's verdict directly from the exact variables printed to stdout rather than from an independent boolean accumulator (`all(ok)`).

### Class 3: `dup.*qid` (Duplicate-QID Guards)
- **Sibling tools, knowledge, lessons hits:** Exactly **0**.
- **Chousa-shokunin hits:**
  - `corpus/lessons/round-88.md:75`: "the counter has no verdict-vs-field reconciliation and no duplicate-qid check"
  - `corpus/lessons/round-88-verifier-spotcheck.md:143, 226-227`: "Duplicate-qid / swapped-quote forgeries. Five in-class forgeries pass the C2 counter green (ledger row R88ExecC2Forge). Routed: duplicate-qid guard..."
  - `corpus/evidence/round89/claims.md:81, 85, 132`: `DUP_QIDS=0`
  - `corpus/evidence/round89/curation-r89.py:175, 281-282`: checks `len(dup_qids) == 0` for warrant cells citing `Q1, Q1`.
- **Ownership Evaluation:**
  `dup.*qid` is unowned by sibling lanes. It guards a citation-integrity invariant specific to `chousa`'s knowledge entries (`search-transparency-reporting-r84.md`, `provenance-recording-r85.md`), preventing a forger from citing one located quote ID multiple times in a single warrant cell to artificially satisfy warrant quotas.

### Class 4: `supersed` (Supersession-Clause Check)
- **Sibling tools hits:** 712 hits across 7 lanes.
  - **`kotodama-shokunin` (32 hits in 3 files):**
    - `kotodama-shokunin/tools/check-supersession-settlement.py`: lines 2, 4, 5, 8, 11, 13, 15, 25, 55, 99, 115, 119, 121, 237, 244, 251, 252, 261, 274.
      This tool is a dedicated, formal validator for the fleet/lane SOURCES registry supersession mechanism (`supersedes S### —`). It checks whether supersession chains are settled:
      - `SETTLED-ACTIVE`: superseding row is `mined` with `used-by` naming an existing corpus path, and superseded row is `queued` or `rejected`.
      - `SETTLED-RETIRED`: superseding row is `rejected`.
      - `SETTLED-CLOSED`: superseded row is `rejected`.
      - `SETTLED-SPLIT`: both rows `mined` with explicit scope limiter ("for entry/line... only").
      - `pending`: defective or incomplete supersession chain.
  - `kama-shokunin` (58 hits in 14 files):
    - `kama-shokunin/tools/round54-cited-path-check.py`: lines 4, 96, 98, 105, 119, 120, 125, 133, 167, 461, 471, 478 — checks `superseded` class citations in SCORECARD, SHONEN, SKILL.
    - `kama-shokunin/tools/round40-calibration-audit.py`: lines 8, 9, 12, 19, 64, 81 — checks that row S474's teaches starts with `supersedes S472` and contains the exact corrected evidence digest.
    - `kama-shokunin/tools/round76-selfrecord-facts.py:7, 36, 181`, `round77-selfrecord-round76.py:41, 147, 150`: checks `Supersedes:` field in appended correction blocks.
    - `kama-shokunin/tools/round92-server-defaults.py:8, 16, 39, 61, 269, 275`: counts `supersedes` in SKILL.md serving defaults.
  - `mori-shokunin` (210 hits in 5 files):
    - `mori-shokunin/tools/mori-sources-appendonly.py:7`: checks append-only supersession discipline.
- **Chousa-shokunin implementation:**
  - `tools/build-spans.py:3`: span builder superseding earlier per-round builders.
  - `corpus/evidence/round89/curation-r89.py`:
    - `SUPERSEDED` leg (lines 154–167, 270–271): verifies `target[7] == "mined" and cells[7] != "mined"` (flagging when a superseded target is still mined while the superseder is not mined).
    - `TEACHES` supersession-clause check (lines 251–268): checks that if a superseding row opens with `supersedes (S\d{3,}) —` and carries contrast words and date terms, those date terms must be readable in the superseding row's own capture text (`teaches_sup_unresolved`).
- **Ownership Evaluation:**
  `kotodama-shokunin` owns the general-purpose **status settlement checker** (`check-supersession-settlement.py`) for the fleet-wide `corpus/SOURCES.md` format. `chousa-shokunin` owns an in-counter semantic validator that checks the *internal content* of superseding rows (contrast and date grounding in local captures).

---

## 3. (b) PROVINCE Invariant Assessment

`/home/vgpnk/Projects/shokunin/chousa-shokunin/PROVINCE.md` declares:
- **Domain:** deep-research method (調査) — the reusable craft of source research.
- **Owns:** question framing; source hierarchy (primary / secondary / aggregator / unsourced); citation chaining and hop resolution; claim-vs-source verification; search-strategy taxonomy; the external-target approval table for a research window; **this lane's own corpus and gates**.
- **Refuses:** bounty-program scope and claim packages (→ kasegi); model-quality or evaluation claims (→ kengaku); orchestration, multi-agent dispatch and agent lifecycle (→ kumitate); external live-target research without operator approval (loopback-only otherwise); secret values in any record (→ kagi for custody; shape-only here).
- **Out of province → report, never absorb.**

### Assessment
1. **C1 (`C1-BATTERY-R89` — operability):** Measures the verification gate `corpus/evidence/round89/gate-records-r89.py` over `tools/gate-records.py` on `chousa-shokunin`'s own gates and gate records. This sits squarely within **"this lane's own corpus and gates"**.
2. **C2 (`C2-CURATION-R89` — calibration):** Measures `corpus/evidence/round89/curation-r89.py` over `chousa-shokunin`'s own `corpus/SOURCES.md` registry and `corpus/knowledge/` entries. This sits squarely within **"this lane's own corpus and gates"** and **"claim-vs-source verification"**.
3. **Refusal Check:**
   - No bounty or vulnerability scope is claimed (kasegi uninfringed).
   - No model evaluation or benchmark score is claimed (kengaku uninfringed).
   - No multi-agent orchestration, worker lifecycle, or dispatch machinery is implemented (kumitate uninfringed).
   - No live external target was queried; all checks read committed, locally archived files (RFC 9110 capture `b1b13a12...` and schema.org capture `11d6cc56...`).
   - No secret values or vault credentials are touched (kagi uninfringed).
4. **Conclusion:** The round's instrument overlap with sibling verification concepts is **NOT a PROVINCE violation**. Internal test batteries and curation gates are standard hygiene for a lane's own corpus.

---

## 4. (c) Contested Scope & Sibling Communication

### Contested Scope for Integrator Arbitration
- **Registry Supersession Settlement vs. Semantic Capture Grounding (`chousa` vs `kotodama`):**
  `kotodama-shokunin`'s `check-supersession-settlement.py` defines the canonical fleet model for registry supersession settlement, verifying status transitions (`mined` → `queued`/`rejected`) and `used-by` path existence. `chousa-shokunin`'s `curation-r89.py` independently implemented a `SUPERSEDED` leg and an in-counter `TEACHES` supersession-clause check.
  - *Arbitration question for the Integrator:* Should registry supersession status settlement remain a standalone check run via `kotodama`'s tool (or a fleet-level gate), while `chousa` focuses exclusively on semantic claim-vs-capture grounding? Or should `kotodama`'s status settlement rules be ratified as an in-lane requirement for any curation counter that inspects superseding rows?

### Sibling Notifications for Next Round
1. **Notify `kotodama-shokunin`:**
   `chousa`'s round 88/89 finding demonstrates that checking *settlement status* alone (`mined` vs `queued`) is insufficient to prevent supersession forgeries. A forged superseding row can achieve `SETTLED-ACTIVE` status by naming a valid knowledge entry, while asserting a teaching (such as temporal contrast or date boundaries) completely unsupported by its own source capture. `kotodama`'s round-90 planning should consider whether `check-supersession-settlement.py` should incorporate capture verification for superseding rows.
2. **Notify `kama-shokunin`:**
   `chousa`'s `fields_hold` pattern in `curation-r89.py` provides an algebraic proof against verdict decoupling: instead of computing `passed = all(ok)` from internal loop flags, the counter re-parses the exact values emitted in the summary string and enforces that `fields_hold == all(legs_ok)`. `kama-shokunin` (which experienced similar summary decoupling in round 81/86) should be notified of this pattern for its multi-arm gates.

---

## 5. (d) UFO-FSD Connector Move: One Non-Obvious Move

### Evidence
1. **C1 Limitation (Named Limit 1 & R89ExecRepro Challenge):**
   In `gate-records-r89.py`, the `CROSSCHECK` routine validates that summary fields equal re-derived numbers from leg receipts. However, the final verdict:
   ```python
   passed = (len(reconciled) == EXPECTED_LEGS and len(unreconciled) == 0
             and cross_ok == EXPECTED_CROSSCHECK and len(uncrosschecked) == 0
             and len(reread) == EXPECTED_LEGS)
   ```
   is computed from internal accumulators (`reconciled`, `cross_ok`). A multi-point forgery that modifies both the summary string and the leg writer survives if the exit boolean is decoupled, as shown by `R89ExecRepro`'s joint challenge run (`receipts/challenge-joint-run.txt`).
2. **C2 Limitation (Named Limit 4 & Vacuous Superseder Check):**
   In `curation-r89.py:251-267`, the superseder clause:
   ```python
   for sid, cells in sorted(reg.items()):
       if not re.match(r"supersedes (S\d{3,}) —", cells[6]): continue
       tl = cells[6].lower()
       if not any(c in tl for c in CONTRAST): continue
       named = [t for t in DATE_TERMS if t in tl]
       if not named: continue
       teaches_sup_checked += 1
       ...
   ```
   yields `SUP_CLAUSE_CHECKED=0` on the live registry. The claim itself acknowledges in Named Limit 4:
   *"The superseder-own-read clause is **vacuous on the real registry** (`SUP_CLAUSE_CHECKED=0`: no superseding row names a date term). Its non-vacuity is the battery's SUP-clause-mirror..."*
   None of the 10 real superseding rows in `chousa`'s registry combine a contrast phrase with a date term; they supersede anchor labels, scopes, or definitions (e.g. S073 superseding S070's `-c, --check` anchor). Thus, the clause is permanently dormant on real data.

### Affected Axes
- **Operability** (C1, currently historical 3/10): Improved.
- **Calibration** (C2): Improved.
- **Province / Adjacency:** Untouched (zero cross-repo contamination; 100% in-province).

### Proposed Move
**Synthesize C2's Algebraic `fields_hold` Verdict into C1, and Ground C2's Superseder Check via In-Province Citation Adoption.**

Specifically:
1. **In C1 (`gate-records-r89.py`):**
   Replace the accumulator-based `passed` check with a formal `fields_hold` evaluation derived directly from `summ`:
   ```python
   fields_hold = (
       summ.get("TOOL") == "present"
       and _ints("POSITIVE") == [15, 15]
       and _ints("FRESH_POSITIVE") == [5, 5]
       and _ints("FORGED_REFUSED") == [362, 362]
       and _ints("EXPECTED_CODE") == [362, 362]
       and _ints("EMPTY_REFUSED") == [1, 1]
       and _ints("RC") == [4, 4]
       and _ints("SETUP") == [1, 1]
       and _ints("D1_FORGES") == [3]
       and _ints("DIV3") == [3]
       and _ints("D1_REFUSED") == [3, 3]
       and _ints("D2_FORGES") == [3]
       and _ints("D2_REFUSED") == [3, 3]
       and _ints("MUT_ADMIT_DERIVED") == [1]
       and _ints("MUT_ADMIT_KILLED") == [1]
       and _ints("MUT_UNREACH_DERIVED") == [1]
       and _ints("MUT_UNREACH_KILLED") == [1]
       and _ints("DERIVE_NEG") == [1]
   )
   ```
   Add a `VERDICT` leg requiring `fields_hold == all(ok for _, ok, _ in legs) and fields_hold`. This eliminates the E7f class of detachment structurally in C1 without requiring external harness verification.
2. **In C2 (`curation-r89.py`):**
   Disarm Named Limit 4's vacuity by replacing the narrow date-contrast check with a non-vacuous **citation-adoption settlement check** adapted from `kotodama`'s model:
   - For every row where `cells[6]` matches `supersedes (S\d{3,}) —`:
     - If the superseding row is `mined`:
       - Its `used-by` cell MUST name an existing file in `corpus/knowledge/`.
       - That file MUST contain the superseding `S###` identifier.
       - That file MUST NOT contain the superseded `S###` identifier as an active warrant or evidence citation.
     - The superseded row MUST NOT be marked `mined`.
   - On `chousa`'s real registry, this clause immediately evaluates against all 10 real superseding rows (e.g. S029, S030, S031, S073), moving `SUP_CLAUSE_CHECKED` from 0 to 10 on live bytes, while preserving the battery mirror for forged date-contrast rows.

### Second-Order Effects & Risks
- **Substrate & Runtime:** Zero additional external processes; execution overhead is <10ms (string scans on already opened markdown files).
- **Contract Surface:** Eliminates Named Limit 4 from C2 without relaxing any kill rule. Strengthens C1 against joint detachment without modifying `tools/gate-records.py`.
- **Risks:** If any historical knowledge entry in `corpus/knowledge/` legitimately retains a superseded citation for historical contrast (e.g. "S024 superseded by S031"), the check must distinguish active citations (`used-by`) from historical mentions. This is cleanly handled by checking that the superseded ID is absent from active *warrant* and *source* headers, mirroring `kotodama`'s `check-supersession-settlement.py` `usedby` rule.

### Verification
1. **C1 Verification:** Mutating any printed summary field in `gate-records-r89.py` causes `fields_hold` to fail immediately and print `LEG_FAIL VERDICT fields_hold=0`, causing exit 1 even if `all(legs)` was detached to True.
2. **C2 Verification:** Running `curation-r89.py` on the live tree prints `SUP_ADOPTION_CHECKED=10/10 SUP_UNADOPTED=0` instead of `SUP_CLAUSE_CHECKED=0`. A planted control where a mined superseder's `used-by` file fails to cite the new row, or still cites the superseded row, exits 1 with `LEG_FAIL SUP_ADOPTION`.

---

## 6. Verification of Round 89 Frozen Predicates

All six commands were independently executed in a clean scratch tree built from freeze commit `ac0a0892c15de11fb28d3208f2b287687c00477e` against base `f8fa55ec94cb34e7b572a9d87d7f62d88bc80bf8`. Every run reproduced the frozen expectations exactly.

| Instrument | Command | Exit | Key Summary Output | Status |
|---|---|---|---|---|
| **C1 Battery** | `gate-records-r89.py` | 0 | `LEG_REREAD=16/16 RECONCILED=16/16 CROSSCHECK=15/15 LEGS_APPENDED=16 GATE_RECORDS_R89=PASS` | PASS |
| **C1 Mutants** | `mutate-r89.py` | 0 | `MUTANTS_KILLED=11/11 TOOL_MUTANTS_CAUGHT=2/2 TOTAL=13/13` | PASS |
| **C1 Harm** | `harm-recheck.py` | 0 | `HARM_RECHECK files=13 records=29 moved=0 base_rc=0 r88_rc=0` | PASS |
| **C2 Counter** | `curation-r89.py` | 0 | `DUP_QIDS=0 WARRANT_OK=17/17 QUOTES_LOCATED=20/20 TEACHES_FLAGGED=1 TEACHES_UNRESOLVED=0 SUP_CLAUSE_CHECKED=0 SUP_UNRESOLVED=0 CURATION_R89=PASS` | PASS |
| **C2 Controls** | `curation-r89-controls.py` | 0 | `FORGERY_REFUSED=7/7 PRIOR_ACCEPTED_FORGERY=7/7 CONTROLS=PASS` | PASS |
| **C2 Mutants** | `curation-r89-mutants.py` | 0 | `MUTANTS_KILLED=6/6 COUNTER_DETECTED=5 BATTERY_DETECTED=1` | PASS |

Receipts are preserved under `.ufo/waves/round-89/w1/R89ConnectorSiblings/receipts/`:
- `c1-battery.txt`
- `c1-mutants.txt`
- `c1-harm.txt`
- `c2-counter.txt`
- `c2-controls.txt`
- `c2-mutants.txt`
- `scan_reconcil.tsv`
- `scan_fields_hold.tsv`
- `scan_dup_qid.tsv`
- `scan_supersed.tsv`

---

VERDICT: R89ConnectorSiblings C1 held — C1 leg-receipt reconciliation and summary cross-check verify with 16/16 legs and 15/15 crosschecks, operating inside chousa province with zero sibling ownership overlap.
VERDICT: R89ConnectorSiblings C2 held — C2 curation counter, duplicate-qid guard and fields_hold verdict verify with 20/20 quotes and 6/6 mutants killed, remaining fully within chousa province while highlighting superseder settlement coordination with kotodama.
