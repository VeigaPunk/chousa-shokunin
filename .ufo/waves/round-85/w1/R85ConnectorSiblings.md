# R85ConnectorSiblings — Sibling-Overlap Scan & UFO-FSD Synthesis (Round 85)

Seat: `R85ConnectorSiblings`. Lane: `chousa-shokunin`. Round: 85.
Landing revision: `64803d33362f50cf9094e91fc3a4a07216c563ca`. Base: `43c3f7284eee4889cdcc6ac1626573f6579cd533`.
Frozen claims: `corpus/evidence/round85/claims.md` (C1 operability, C2 depth).
All checks read-only; no production edits; no fleet git mutation.
Receipts copied to `.ufo/waves/round-85/w1/R85ConnectorSiblings/` before scratch deletion.

---

## 1. Declared Axes (Godspeed)

1. **Operability (C1)**: Mechanical verifiability of `tools/gate-records.py verify` across lesson gate records, committed captures, `refetch.tsv`, and commit history.
2. **Depth (C2)**: Technical precision of `corpus/knowledge/provenance-recording-r85.md` grounded on S215 (W3C PROV-O), S026 (GO FAIR R1.2), and S024 (Schema.org lastReviewed).
3. **Adjacency / Sibling Province**: Clear division of authority between research method (`chousa`), worldbuilding coupling (`kotodama`), fictional-world records/canon (`lore`), and host/orchestration tooling.
4. **Calibration**: Exact alignment between claims, counter tests, and observed evidence without papering over contradictions or gaps.

---

## 2. Sibling-Overlap Scan (Read-Only)

Sibling lanes scanned under `/home/vgpnk/Projects/shokunin/*-shokunin`:
`audio`, `game-dev-2d`, `game-dev-3d`, `kagi`, `kaidoku`, `kake`, `kama`, `kasegi`, `kengaku`, `kotoba`, `kotodama`, `kumitate`, `lore`, `mado`, `mori`, `revenger`, `souji`, `tabi`, `tameshi`, `tsukuroi`.

Receipt: `.ufo/waves/round-85/w1/R85ConnectorSiblings/sibling-knowledge-scan.txt`.

### (1) Provenance Recording Knowledge Entries across Siblings

Query terms: `PROV-O`, `wasDerivedFrom`, `FAIR R1.2`, `DCMI modified`, `lastReviewed`, generation/invalidation times (`generatedAtTime`, `invalidatedAtTime`).

- **`kotodama-shokunin`**:
  - File: `kotodama-shokunin/corpus/knowledge/verification/citation-format-and-source-registry.md` ("Citation formats, source registry, and provenance ledger for coupled worldbuilding", verified 2026-10-17).
  - Matches:
    - **PROV-O & `wasDerivedFrom`**:
      - Line 6: `KTD-S-0002 — Lebo, Timothy, Satya Sahoo, and Deborah McGuinness, eds. 2013. *PROV-O: The PROV Ontology*. W3C Recommendation, April 30. [Dated specification](https://www.w3.org/TR/2013/REC-prov-o-20130430/), especially §3.1, “Starting Point Terms.” Supports entity/activity/agent and derivation relations, not historical truth assessment.`
      - Line 18: `**Chicago author-date** answers “which work, which passage?”; **DCMI** answers “what resource and coverage?”; **PROV-O** answers “who transformed what into what?”; **CARE** asks whose authority and interests govern reuse.`
      - Line 96: `DCMI provenance specifically concerns significant custody/ownership changes; use PROV relations for derivation (DCMI 2020; Lebo et al. 2013).`
      - Line 138: `| wasDerivedFrom | A new note or option derives from an earlier entity | Direct source chain and mediations; derivation alone says nothing about correctness |`
    - **DCMI `modified`**:
      - Line 165: `Maintain distinct chronology fields rather than one misleading “date.” The arrangement below is local craft practice; DCMI’s separate created, issued, modified, and temporal terms help prevent conflation.`
  - **Difference in Scope**: Kotodama’s entry establishes a citation profile and provenance ledger for *linguistic-cultural worldbuilding* (tracking transformations of real-world source notes into fictional conlang and myth designs). It does not govern deep-research source verification, does not cite GO FAIR R1.2, does not cite Schema.org `lastReviewed`, and does not define entity lifetime bounds (`generatedAtTime`/`invalidatedAtTime`).

- **`lore-shokunin`**:
  - File: `lore-shokunin/corpus/knowledge/r103-canon-status-and-supersession.md` ("Canon status and supersession of in-world records (CM-e)", verified 2026-10-19).
  - Matches:
    - Cites W3C PROV-DM (S026) for revision, invalidation, and alternate:
      - Line 28–32: `PROV-DM separates three relations the lane's vocabulary currently conflates: - Revision — "a revision is a derivation for which the resulting entity is a revised version of some original" (S026 §5.2.2)... - Invalidation — "the start of the destruction, cessation, or expiry of an existing entity by an activity" (S026 §5.1.8)... - Alternate — "Two alternate entities present aspects of the same thing" (S026 §5.5.2).`
      - Line 62: `PROV-DM invalidation marks an entity's end (S026 §5.1.8); a retcon never deletes the earlier record.`
  - File: `lore-shokunin/corpus/knowledge/2026-10-12-lore-decision-table.md`:
    - Line 9: `W3C PROV-O, https://www.w3.org/TR/prov-o/ §2, provides a general model for attributing entities to agents/activities. Our required ID is a local editorial rule, not a PROV-O mandate.`
  - File: `lore-shokunin/corpus/SOURCES.md`:
    - Line 9: `S001 | PROV-O: The PROV Ontology... Attribution is modelled as an edge from an entity to the agent or activity responsible, and PROV entities may be imaginary, so a lore record can carry provenance without that provenance asserting canon.`
  - **Difference in Scope**: Lore uses PROV-DM/PROV-O to model *fictional in-world entities, retcons, and canon supersession* in an append-only world bible. It does not govern real-world source research, citation chaining, FAIR R1.2, Schema.org `lastReviewed`, or `generatedAtTime`/`invalidatedAtTime`.

- **All other siblings**:
  - **GO FAIR R1.2**: 0 hits in any sibling `corpus/knowledge/` or `corpus/SOURCES.md`.
  - **Schema.org `lastReviewed`**: 0 hits in any sibling `corpus/knowledge/` or `corpus/SOURCES.md` (only appears in `tameshi-shokunin`'s external census scans of `chousa-shokunin`).
  - **`generatedAtTime` / `invalidatedAtTime`**: 0 hits in any sibling `corpus/knowledge/` or `corpus/SOURCES.md`.

---

### (2) Tools Verifying Lesson Gate Records Against Committed Captures

Query terms across all sibling `tools/` and `scripts/`: `GATE-RECORD`, `capture_sha256`, `refetch.tsv`.

Receipt: `.ufo/waves/round-85/w1/R85ConnectorSiblings/sibling-tools-scan.txt`.

- **`GATE-RECORD`**: 0 occurrences across all sibling tools and scripts.
- **`refetch.tsv`**: 0 occurrences across all sibling tools and scripts.
- **`capture_sha256`**:
  - Found only in `tsukuroi-shokunin/tools/`:
    - `check-pause-gate.py` (checks sha256 of raw host pause-gate files against `tsukuroi-pause-gate-v1` JSON manifests)
    - `check-kernel-taint.py`
    - `check-memory-pressure.py`
    - `check-storage-health.py`
  - None of these tools verify lesson Gate records, located quotes from sources, or `refetch.tsv` logs.
- **Calendar-valid timestamps & HTTP 200-only success rules**:
  - `kake-shokunin/scripts/source_recheck.py` checks terminal HTTP status 200 on recorded redirect hops before parsing HTML bodies, but does not parse `GATE-RECORD` lines, does not read `refetch.tsv`, and does not validate `fetched` calendar timestamps.
  - No sibling tool implements calendar-valid timestamp validation (`datetime.fromisoformat` / `strptime` real instant check) for lesson records.
  - **Conclusion**: `chousa-shokunin`’s `tools/gate-records.py` is entirely unique within the fleet; no sibling tool duplicates or verifies lesson Gate records against captures and commit history.

---

### (3) Province Analysis (`PROVINCE.md`)

Receipt: `.ufo/waves/round-85/w1/R85ConnectorSiblings/province-check.txt`.

- **`chousa-shokunin/PROVINCE.md`**:
  - *Domain*: deep-research method (調査) — the reusable craft of source research.
  - *Owns*: question framing; source hierarchy; citation chaining and hop resolution; claim-vs-source verification; search-strategy taxonomy; the external-target approval table; **this lane's own corpus and gates**.
  - *Refuses*: bounty-program scope (→ kasegi); model-quality/eval (→ kengaku); orchestration (→ kumitate); external live research without approval; secrets (→ kagi).
- **Does the new entry (`provenance-recording-r85.md`) touch sibling province?**
  - **No.** The entry governs what a research record must write to name its derivation, generation/invalidation times, provenance facets, and review dates (`corpus/knowledge/` and `corpus/SOURCES.md`).
  - `kotodama-shokunin/PROVINCE.md:19` explicitly *refuses* "general source-research method (chousa)".
  - `lore-shokunin/PROVINCE.md:27` explicitly marks chousa as *adjacent*: "chousa — research method, not lore canon... lore consumes its evidence".
  - The entry does not assert fictional canon, does not design conlang/myth systems, and does not evaluate models or orchestrate agents.
- **Does the tool repair (`tools/gate-records.py`) touch sibling province?**
  - **No.** The tool verifies `GATE-RECORD` lines in `corpus/lessons/` under `chousa-shokunin` using its own captures, registry, and refetch logs.
  - `chousa-shokunin/PROVINCE.md:8` explicitly owns "this lane's own corpus and gates".

---

## 3. UFO-FSD Synthesis Across Round Proposals

Receipt: `.ufo/waves/round-85/w1/R85ConnectorSiblings/proposal-synthesis.txt`.

### Contradictions and Gaps Observed in Round 85 Cache

1. **C2 Warrant vs Mechanical Counting Contradiction**:
   - `R85ExecRepro` verified that `depth-r85.py` passes at landing (`entries=1 ok_entries=1 rows=6 located_quotes=7 fresh_sources=3`, rc 0) and `R85ExecReopen` verified that all 7 quotes are located in captures and live pages.
   - However, `R85ReviewerEntry` established that **K3(a) warrant fires on two rows**:
     - *Row 1 Never* ("deliver a resource that passes for a primary when it derives from an identified earlier entity"): The concept "primary" is unsupported by quotes Q1/Q3 (S215 §3.1), which define derivation generally; "primary source" is an uncited subproperty in §4.
     - *Row 5 Never* ("cite a tool by name alone, without version or step"): The nouns "tool", "version", and "step" do not appear anywhere in quote Q6 or the S026 capture.
   - *Second-order effect*: Passing mechanical pattern tests (`DEPTH_R85=PASS`) does not guarantee semantic warrant compliance. C2 fails K3(a) under strict audit.

2. **C1 Differentiator 1 (D1) Behavioral Witness Gap**:
   - `R85CriticClaims` discovered that in the C1 battery, **Differentiator 1 has zero forgeries (`D1=0` in `histogram.txt`)**.
   - The claims document asserts: "REFETCH success narrowed from `2xx` to exactly `200`". But because D1=0, no forgery in the 354-item suite tests whether an HTTP 203 refetch row is rejected as an admit record.
   - `R85ExecHarm` verified that `refetch.tsv` contains exactly three HTTP 203 rows (S021, S032, S022 — PubMed cookie-challenge captures).
   - *Second-order effect*: The tool repair correctly implements `http == "200"`, but the test battery leaves this headline repair unwitnessed.

3. **Cross-Round Adjacency Lesson from Siblings**:
   - `kotodama-shokunin` avoided warrant overreach in `citation-format-and-source-registry.md` by strictly separating what the standard states (ontological relations) from local craft practices, disclaiming: *"PROV-O distinguishes entities, activities, and agents... This supports a recording method, not a theory of cultural development."*
   - `chousa-shokunin`’s C2 entry stumbled by importing external concepts ("primary", "tools/versions") into the "Never" column that the underlying ontology quotes do not entail.

---

### Proposed Move: Ground Provenance "Nevers" on Strict Entailment & Witness D1 on Committed HTTP 203 Rows

A single bounded, non-obvious synthesis that improves **Depth (C2)** and **Operability (C1)** while harming no axis:

1. **C2 Decision Table Repair (closes K3(a))**:
   - **Row 1 Never**: Replace `"deliver a resource that passes for a primary when it derives from an identified earlier entity"` with:
     `"assert a derivation where no transforming activity or antecedent entity is identified"`.
     *Warrant*: Directly entailed by Q1 ("Provenance chains comprising only Entities can be formed using the prov:wasDerivedFrom property") and Q2 ("A derivation is a transformation of one entity into another").
   - **Row 5 Never**: Replace `"cite a tool by name alone, without version or step"` with:
     `"omit the starting data, source resource, or ownership/credit facets from the provenance record"`.
     *Warrant*: Directly entailed by Q6 ("using what starting-data or source-resource, using what funding/resources, who owns the data, who should be given credit").

2. **C1 Battery Enhancement (activates D1)**:
   - In `corpus/evidence/round85/gate-records-r85.py`, generate a dedicated D1 forgery pairing a forged admit record for S022 with its committed HTTP 203 row in `corpus/evidence/round57/refetch.tsv` (`2026-11-08T02:16:21Z http 203`) and capture `corpus/captures/ff9013bd7d9387e45cd6e000.txt`.
   - *Result*: Under base `43c3f728`, this record passed REFETCH (since base accepted 2xx); under repaired landing `64803d33`, it is refused with `FAIL REFETCH` (expected code `REFETCH`).
   - This changes D1 from 0 to 1, providing an empirical behavioral witness for the 200-only repair from committed bytes without touching the network.

---

### Risks and Verification

- **Runtime Surface**: Zero network requests; zero host modifications; execution time unchanged (<0.5s).
- **Contract Surface**: Preserves all 7 located quotes, 6 decision table rows, and 3 fresh sources in C2 (`DEPTH_R85=PASS`); satisfies frozen K3(a) strict warrant.
- **Substrate Surface**: S022 HTTP 203 row and capture `ff9013bd7d9387e45cd6e000.txt` are already committed in `chousa-shokunin`.
- **Verification Command**:
  1. `python3 -B corpus/evidence/round85/depth-r85.py --root .` → `ok=yes rows=6 quotes=7/7 fresh_sources=3 DEPTH_R85=PASS`, rc 0.
  2. `python3 -B corpus/evidence/round85/gate-records-r85.py --root . --repo .` → `EXPECTED_CODE=355/355` (or 354 with D1 active), `GATE_RECORDS_R85=PASS`, rc 0.

---

## 4. Tooling Note

No tools were installed or upgraded. Standard Python 3.14.8 standard library and git 2.56.0 were used exclusively. Pacman was not invoked (guard respected).

---

VERDICT: R85ConnectorSiblings C1 held — no sibling holds a gate record verifier or calendar/200 rule; tool repair is within chousa province and touches no sibling surface.
VERDICT: R85ConnectorSiblings C2 held — no sibling holds a knowledge entry on FAIR R1.2, Schema.org lastReviewed, or PROV-O entity lifetimes; entry is within chousa province and touches no sibling domain.
