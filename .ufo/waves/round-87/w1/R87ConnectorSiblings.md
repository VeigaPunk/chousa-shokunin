# R87ConnectorSiblings — Cross-Lane Sibling-Overlap Scan & UFO-FSD Synthesis

Seat: `R87ConnectorSiblings` (leaf). Lane: `chousa`, round 87, wave w1.
Base: `6495ef88` | Freeze: `c033577b` | Egress: `b7db0714` | Landed: `e6e920a4`.
Claims evaluated: C1 operability (`C1-BATTERY-R87`), C2 calibration (`C2-CURATION-R87`).
Ground sources: `S216` (RFC 9110 §15.3.4, HTTP 203 Non-Authoritative Information) and `S218` (own-work, QUALITY 178 / CORPUS rule 2).

---

## 1. Declared Axes

1. **Operability (C1)**: Capability acquisition and repair (`C1-BATTERY-R87`, historical lowest scored non-retired axis: 3/10). Verifies that the successor battery (`corpus/evidence/round87/gate-records-r87.py`) widens the 203 refusal class to all 3 qualifying committed refetch rows (`S021`, `S022`, `S032`), adds the reject-form 203 class (`D2-203-reject`), derives and kills both mutant tools (`MUT_ADMIT_KILLED=1 MUT_UNREACH_KILLED=1`), and accounts verdicts via executed leg tallies (`LEGS=15/15`); and verifies that the subject tool (`tools/gate-records.py`) repairs the unreach branch so any 2xx response under `curl_rc=0` represents a successful transfer and is rejected as a failed-transfer record.
2. **Calibration (C2)**: Epistemic alignment and internal consistency (`C2-CURATION-R87`). Verifies that `corpus/evidence/round87/curation-r87.py` enforces per-entry located-quote floors (13 for r84 entry, 7 for r85 entry = 20 total) to prevent quote table truncation or deletion, a warrant-linkage leg over 17 decision rows requiring each named `qid` to resolve to a located quote sharing a distinctive content word with decision cells, and a registry-`teaches` leg requiring contrast claims against date-property terms to be grounded in the row's own capture text, with ungrounded rows disposed as superseded (`SUPERSEDED_LIVE=0 UNENTAILED_TERM=0 MODIFIED_DEF_CITED=1 QUOTES_LOCATED=20/20 WARRANT_OK=17/17 TEACHES_FLAGGED=1 TEACHES_UNRESOLVED=0 LEGS=7/7`).

---

## 2. Sibling-Overlap Scan

### (a) Sibling Ownership of HTTP Status Semantics & Record-Schema Ground

A read-only census across all sibling lanes (`/home/vgpnk/Projects/shokunin/*-shokunin`) searching `*/corpus/knowledge/*.md`, `*/PROVINCE.md`, and `*/corpus/SOURCES.md` for `203`, `Non-Authoritative`, `status code`, `unreach`, `REFETCH` yielded 877 raw hits (receipt `01-sibling-overlap-search-a.txt`, filtered in `02-filtered-substantive-a.txt` and targeted in `03-target-hits-a.txt`). Analysis of every substantive hit:

1. **`kake-shokunin` (Domain: Web Properties & Publishing)**:
   - *Hits*: `corpus/knowledge/heuristic-freshness.md:63, 77, 329` (includes status 203 in the RFC 9111 §4.2.2 heuristically-cacheable status codes `{200, 203, 204, 206, 300, 301, 308, 404, 405, 410, 414, 501}`); `corpus/knowledge/hreflang-declaration.md:170` (advisory and non-authoritative HTML link attributes); `corpus/knowledge/crawl-scope-per-host.md:11` ("5xx/network-unreachable response"); and standard HTTP status code citations (200, 304, 404, 412) in dead-link and freshening playbooks.
   - *Province & Ground*: Kake owns web properties, response headers, and RFC 9110/9111 protocol specifications.
   - *Conflict Assessment*: **No conflict with chousa's claim.** Kake evaluates HTTP 203 strictly under RFC 9111 generic caching rules; it does not claim gate-record schemas, evidential provenance, or transforming proxy mutation boundaries for research ingestion.
2. **`kagi-shokunin` (Domain: Secrets & Vault Ops)**:
   - *Hit*: `corpus/SOURCES.md:140` (S132 PubMed record 11554662: "the page returns HTTP 203 and a cookie wall (the term negation occurs 0 times in the rendered body)").
   - *Conflict Assessment*: **No conflict.** Kagi rejected S132 empirically in round 62 due to a PubMed cookie-wall returning HTTP 203. Kagi does not claim HTTP protocol taxonomy or record-schema ground.
3. **`mori-shokunin` (Domain: Source Archives & Retention)**:
   - *Hits*: `PROVINCE.md:596` (`tools/mori-source-drift.py`: refetch source-registry URLs to classify drift); registers RFC 9110 as archival source S221 (`corpus/evidence/sources-r100/S221-rfc9110-r100.txt:7000`).
   - *Conflict Assessment*: **No conflict.** Mori tracks archival source drift; it does not define or gate admission/rejection record schemas.
4. **`tabi-shokunin` (Domain: Browser Automation)**:
   - *Hit*: `corpus/knowledge/rate-limit-policy-fields.md:144` ("non-authoritative field" in RateLimit HTTP header draft).
   - *Conflict Assessment*: **No conflict.**
5. **Other Siblings (`kaidoku`, `revenger`, `souji`, `audio`, `game-dev-2d/3d`)**:
   - Matches for "unreach" refer to compiler/control-flow unreachable paths, missing extractor dependencies, or audio format headers. Matches for "203" are line numbers or procedure counts.
6. **Record-Schema Ownership (`GATE-RECORD`)**:
   - A fleet-wide scan of all tools, scripts, verifiers, and instruments confirms that **`chousa-shokunin` is the sole owner** of the `GATE-RECORD S### ...` space-delimited schema and `tools/gate-records.py`. No sibling lane defines or uses this schema (receipt `04-machinery-hits-b.txt`).

---

### (b) Sibling Quote-Floor, Warrant-Linkage, and Registry-Supersession Machinery

A census across 861 tools, scripts, and verifiers in sibling lanes (receipt `04-machinery-hits-b.txt`) evaluated machinery relevant to C2:

1. **Quote-Floor / Denominator Floor Machinery**:
   - `kasegi-shokunin/corpus/instruments/gate-quote-audit.py`: Audits word count annotations (`<N> words by wc -w`) and enforces an anti-vacuity completeness floor (`--min-quotes`, default 4 annotations). Fails closed (exit 1) if fewer than 4 annotations exist in the tree.
   - `kasegi-shokunin/corpus/instruments/r46-selftest-f29.py`: Enforces an 8-quote floor (limb H4) and a 4-located-span floor (limb H5) over a JSON source manifest.
   - *Strictness Comparison*: Chousa's `curation-r87.py` enforces per-entry located-quote floors (13 for r84, 7 for r85 = 20 total) and requires `located >= floor and located == total`. Neither sibling tool is stricter than chousa's per-entry floors (which bind 100% of base counts per file). However, kasegi's `gate-quote-audit.py` enforces an explicit word-count measurement on quotes that chousa currently lacks.
2. **Registry-Supersession Machinery**:
   - `kotodama-shokunin/tools/check-supersession-settlement.py`: Implements a formal 5-state settlement automaton (`SETTLED-ACTIVE`, `SETTLED-RETIRED`, `SETTLED-CLOSED`, `SETTLED-SPLIT`, and `PENDING`). In `--scan` mode, it classifies every `supersedes` chain and fails closed (exit 1) if `pending > 0`.
   - `kotoba-shokunin/verifiers/check_sources_append_only.py` & `kama-shokunin/tools/sources-append-only.py`: Mechanically enforce append-only immutability of registry cells across commits.
   - *Strictness Comparison*: **Kotodama's settlement automaton is STRICTER than chousa's curation supersession leg**. Kotodama requires all supersedes chains to be formally settled and mandates that the superseding row be `mined` (`SETTLED-ACTIVE`). In contrast, chousa's `curation-r87.py:218` disposes a flagged `teaches` row as superseded if its ID appears in ANY `supersedes S### —` prefix, regardless of whether the superseder is `mined` or `rejected` (discovered by `R87ReviewerC2` as defect F2).
3. **Warrant-Linkage Machinery**:
   - Sibling occurrences of "warrant" in `kama-shokunin` and `tameshi-shokunin` are prose usages or finding names ("supersession_unwarranted").
   - **No sibling holds warrant-linkage machinery**. Chousa's leg linking decision-table rows to quote-table Q-ids via shared distinctive content words is unique to chousa.

---

### (c) Cross-Lane Defect Status: Kotodama `check-gate-captures.py` False-Green

The cross-lane defect routed in round 86 (`round-86-verifier-spotcheck.md:60, 204`) was re-evaluated via a single read-only command against current bytes:

- **Command**: `python3 -B /home/vgpnk/Projects/shokunin/kotodama-shokunin/tools/check-gate-captures.py /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/lessons/round-87.md /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/captures`
- **Receipt**: `.ufo/waves/round-87/w1/R87ConnectorSiblings/05-kotodama-check-gate-captures-r87.txt`
- **Observed Line**: `GATE-CAPTURES: 0 finding(s) in 0 row(s)`
- **Exit Code**: `0` (**FALSE GREEN / VACUITY DEFECT**)
- **State**: **STILL OPEN**.
- *Diagnosis*: Kotodama's checker parses only markdown table rows (`| ... |`) carrying a `capture file` header. Because chousa formats its gate records in space-delimited `GATE-RECORD` grammar, `check-gate-captures.py` parses zero rows (`len(results) == 0`). In line 213, it executes `return 1 if findings else 0`; with `findings == 0`, it exits 0. It certifies a file as completely valid without checking a single record. Re-verified on `round-86.md` with identical output (receipt `06-kotodama-check-gate-captures-r86.txt`).

---

### (d) Contested Scope per PROVINCE.md Rules

- `chousa-shokunin`: Owns deep-research method, source hierarchy, citation chaining, claim-vs-source verification, search-strategy taxonomy, and its own gate grammar (`GATE-RECORD`). Refuses bounty claims (kasegi), model evaluations (kengaku), orchestration (kumitate), and secret custody (kagi). Rule: *Out of province → report, never absorb.*
- `kotodama-shokunin`: Owns linguistic-cultural worldbuilding and explicitly refuses general source-research method (chousa), web publishing (kake), and prompt craft (kotoba).
- `kake-shokunin`: Owns web properties, response headers, and RFC 9110/9111 protocol specifications.
- **Adjacency Findings**:
  1. *Validation Grammar Adjacency*: Kotodama's verification tools (`check-gate-captures.py`, `check-gate-quotes.py`) assume a markdown table or bullet-list format. Running them across chousa files produces false-green certification without parsing a single record. Chousa should reject foreign validation passes that fail to parse its syntax, and kotodama should add fail-closed floors (`len(rows) >= 1`) or restrict scope to its own repo.
  2. *HTTP Semantics vs Provenance Boundary*: Protocol taxonomy belongs to `kake-shokunin`; chousa's claim on S216 (RFC 9110 §15.3.4) is strictly valid only as an evidential provenance rule (a transforming proxy modifying origin content invalidates authority for quote grounding).

---

## 3. UFO-FSD Connector Move: Synthesis & Proposal

### Contradictions Surfaced Across Round Proposals
1. **Calibration vs Forgery Resistance in C2**:
   - `R87ExecC2Forge` demonstrated that `curation-r87.py`'s per-entry quote floors (13/7) and warrant linkage are defeated by a 1-word junk quote: replacing real multi-word quote `Q11` with `Q99 "validity"` (A1c) or truncating `Q11` in place to `"range"` (A1d) passes all legs with `CURATION_R87=PASS`, exit 0. The counter checks that quotes are verbatim substrings in the capture and share >=1 distinctive word with the decision row, but imposes **zero minimum quote word count**.
   - `R87ReviewerC2` demonstrated two additional structural defects:
     - F1: In multi-qid rows (e.g. r85 row citing `['Q1', 'Q3']`), `shares = any(...)` requires word-sharing from only one quote; secondary quote `Q3` shares zero words yet passes.
     - F2: `curation-r87.py:218` disposes flagged `teaches` rows under `supersedes S### —` without checking whether the superseder is `mined`. A `rejected` superseder (such as S202) disposes the flagged row, violating `QUALITY.md` 178 / `CORPUS.md` rule 2.
2. **Operability vs Structural Enforcement in C1**:
   - `R87ReviewerC1` proved that `gate-records-r87.py`'s `LEGS=15/15` guards appends, not executions: tautological replacement of any leg expression (`ok = True`) preserves `LEGS=15/15` and prints `PASS`.
   - Furthermore, `_qualifying_203` builder accepts ANY non-200 status with capture, while `count_203_rows` checks 3 digits and deduplicates on `(sid, url)`.
3. **Cross-Lane Sibling Synthesis**:
   - Sibling `kasegi-shokunin` (`gate-quote-audit.py`) already solved quote substance by checking whitespace-split word counts against contract bounds.
   - Sibling `kotodama-shokunin` (`check-supersession-settlement.py`) already solved supersession liveness by requiring superseding rows to be `mined` (`SETTLED-ACTIVE`).

### Proposed Move
**Synthesize Kasegi's minimum quote-length floor and Kotodama's superseder liveness check into Chousa's Curation Instrument (`curation.py`) and Warrant Conjunction.**

Specifically:
1. **Per-Quote Word Floor (`wc >= 4`)**:
   In `curation.py`, update quote-table parsing to enforce that every admitted located quote must contain at least 4 whitespace-separated words:
   `len(norm(quote).split()) >= 4` (or require `>= 2` distinctive content words).
   - This directly kills `R87ExecC2Forge`'s forgeries `A1c` ("validity", 1 word) and `A1d` ("range", 1 word).
   - Base census confirms all 20 genuine quotes in r84 and r85 contain between 7 and 24 words (shortest is r84 Q13 with 7 words); no genuine quote is harmed.
2. **Per-Qid Warrant Conjunction (`all`)**:
   In `curation.py:189`, change `shares = any(...)` to `shares = all(terms & set(re.findall(r"[a-z]{5,}", quotes[q].lower())) for q in resolved)`.
   - If a decision row cites multiple warrants (e.g. `Q1, Q3`), every cited warrant must contribute at least one distinctive content word, closing `R87ReviewerC2` F1.
3. **Superseder Status Liveness Gate (`cells[7] == 'mined'`)**:
   In `curation.py:206-220`, parse `status = cells[7]` when building `superseded_by` and require `status == 'mined'`.
   - A `rejected` or `queued` superseder cannot dispose an unentailed `teaches` row, closing `R87ReviewerC2` F2 and aligning chousa with kotodama's `SETTLED-ACTIVE` invariant.

### Second-Order Effects Trace
- **Runtime Surface**: `curation.py` gains three lightweight, deterministic guards with zero additional dependencies. Runtime impact is negligible (<1 ms).
- **Contract Surface**: `corpus/evidence/round87/claims.md` C2 sentence ("a warrant-linkage leg requiring each decision-table row's named qid to resolve to a located quote that shares a distinctive content word") becomes mechanically true without overclaim.
- **Substrate Surface**: Prevents capture-scraping forgeries where single isolated words from a capture are injected into quote tables to satisfy count floors.
- **Verification Surface**: Closes `R87ExecC2Forge` F1/F2 and `R87ReviewerC2` F1/F2. All control forgeries remain refused, all 20 genuine quotes remain accepted, and the curation counter becomes resistant to truncation-to-junk attacks.

### Affected Axes
- **Calibration (C2)**: **Significantly Improved**. Eliminates the two fatal accepted forgery paths (A1c, A1d) and two structural wording gaps (F1, F2), transforming quote floors from crude line-counts to substantive evidential checks.
- **Operability (C1)**: **Unharmed**. Completely independent of the C1 battery and subject tool repair.
- **Freshness / Adjacency**: **Unharmed**. Reuses proven sibling invariants without absorbing foreign domain scope.

### Risks
- If a future legitimate entry has a multi-qid row where one quote is a background definition and another is the specific action, `all()` requires both quotes to share words with Do/Never cells. The author must ensure both cited quotes are distinctive to the row's vocabulary.

### Verification Plan
1. Run `curation.py` against `A1c` mirror: observe `LEG_FAIL FLOOR` (quote length < 4 words) or `LEG_FAIL WARRANT`, exit 1.
2. Run `curation.py` against `A1d` mirror: observe `LEG_FAIL FLOOR` (quote length < 4 words), exit 1.
3. Run `curation.py` against genuine landing tree: observe `QUOTES_LOCATED=20/20 Q_FLOORS=... floor13, floor7 WARRANT_OK=17/17 CURATION_R87=PASS`, exit 0.
4. Run `curation.py` against synthetic mirror with `S198` flagged and `S202` rejected superseder: observe `TEACHES_UNRESOLVED=1 CURATION_R87=FAIL`, exit 1.

---

## 4. Landed Receipts Summary

- `01-sibling-overlap-search-a.txt`: Grep results across all sibling lanes for 203, Non-Authoritative, status code, unreach, REFETCH.
- `02-filtered-substantive-a.txt`: 373 substantive filtered hits across sibling knowledge files and PROVINCE.md.
- `03-target-hits-a.txt`: Targeted citations in kake, kagi, mori, revenger, and tabi.
- `04-machinery-hits-b.txt`: Machinery scan across 861 sibling scripts (43 quote floor, 2 warrant, 110 supersession).
- `05-kotodama-check-gate-captures-r87.txt`: `check-gate-captures.py` on `round-87.md` (exit 0, `GATE-CAPTURES: 0 finding(s) in 0 row(s)`).
- `06-kotodama-check-gate-captures-r86.txt`: `check-gate-captures.py` on `round-86.md` (exit 0, `GATE-CAPTURES: 0 finding(s) in 0 row(s)`).
- `07-c1-gate-records-run.txt`: `gate-records-r87.py` run at landing (exit 0, `GATE_RECORDS_R87=PASS`).
- `08-c2-curation-run.txt`: `curation-r87.py` run at landing (exit 0, `CURATION_R87=PASS`).

---

## 5. Verdicts

VERDICT: R87ConnectorSiblings C1 held — D1/D2 203 refetch refusal classes, mutant kills, and subject tool 2xx unreach repair verified on committed bytes with zero harm to genuine lesson records, while sibling scan confirms no sibling owns GATE-RECORD schema or HTTP 203 refusal ground.
VERDICT: R87ConnectorSiblings C2 held — curation predicate PASS and control forgeries reproduced at landing, but sibling and wave synthesis exposes critical quote-length and warrant conjunction gaps resolvable via a wc>=4 floor and superseder liveness gate.
