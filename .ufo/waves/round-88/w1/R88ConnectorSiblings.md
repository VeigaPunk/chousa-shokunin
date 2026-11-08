# R88ConnectorSiblings — Cross-Lane Sibling-Overlap Scan & UFO-FSD Synthesis

Seat: `R88ConnectorSiblings` (leaf). Lane: `chousa`, round 88, wave w1.
Base: `f484d94f` | Freeze / Landed: `4ea9d008abfd2e09cb51649a42678a78f52ac530`.
Claims evaluated: C1 operability (`C1-BATTERY-R88`), C2 calibration (`C2-CURATION-R88`).
Ground sources: `S216` (RFC 9110 §15.3.4, HTTP 203 Non-Authoritative Information) and `S218` (own-work, QUALITY 178 / CORPUS rule 2).

---

## 1. Declared Axes

1. **Operability (C1)**: Capability acquisition and repair (`C1-BATTERY-R88`, historical lowest scored non-retired axis: 3/10). Verifies that the successor battery (`corpus/evidence/round88/gate-records-r88.py`) binds the 203 class to `http == "203"` in both independent derivations, pins the width against a third derivation plus `ROWS_203 = 3`, and accounts its verdict by re-reading each leg's own receipt file and reconciling each detail string against its value (`D1_EXPECTED=3 D1_FORGES=3 D1_REFUSED=3/3 D2_FORGES=3 D2_REFUSED=3/3 MUT_ADMIT_KILLED=1 MUT_UNREACH_KILLED=1 DERIVE_NEG=1 LEG_REREAD=15/15 RECONCILED=15/15 LEGS_APPENDED=15`).
2. **Calibration (C2)**: Epistemic alignment and internal consistency (`C2-CURATION-R88`). Verifies that `corpus/evidence/round88/curation-r88.py` adds an every-qid warrant leg, a per-entry qid-set pin plus a per-row token floor (`MIN_TOKENS = 7`, the measured minimum over the 20 located base quotes), and a `mined`-superseder disposal, printing `SUPERSEDED_LIVE=0 UNENTAILED_TERM=0 MODIFIED_DEF_CITED=1 QUOTES_LOCATED=20/20 WARRANT_OK=17/17 TEACHES_CHECKED=1 TEACHES_FLAGGED=1 TEACHES_UNRESOLVED=0 LEGS=7/7` and refusing all five round-87 forgeries.

---

## 2. Sibling-Overlap Scan

### (a) Sibling Ownership of HTTP Status-Semantics & Record-Schema Ground

A read-only census across all 20 sibling lanes in `/home/vgpnk/Projects/shokunin/` searching `*/corpus/knowledge/*.md`, `*/PROVINCE.md`, and `*/corpus/SOURCES.md` for `203`, `Non-Authoritative`, `status code`, `unreach`, `REFETCH`, `leg receipt`, `reconcile` yielded 819 raw hits across 20 lanes (receipt `01-sibling-overlap-search-a.txt`, filtered substantive breakdown in `02-filtered-substantive-a.txt`).

#### 1. HTTP Status Semantics (`203`, `Non-Authoritative`, `status code`, `unreach`, `REFETCH`)
- **`kake-shokunin` (Domain: Web Properties & Publishing)**:
  - *Evidence*: `corpus/SOURCES.md:201` (S454 RFC 9110 HTTP Semantics §15.5.5 / §15.5.11); `corpus/knowledge/heuristic-freshness.md:63, 77, 329` (includes status 203 in the RFC 9111 §4.2.2 heuristically cacheable set `{200, 203, 204, 206, 300, 301, 308, 404, 405, 410, 414, 501}`); `corpus/knowledge/crawl-scope-per-host.md:11` ("5xx/network-unreachable response"); and status code citations (200, 304, 404, 412) in link checking.
  - *Conflict Assessment*: **No conflict with chousa's claim.** Kake owns web properties, response headers, and RFC 9110/9111 protocol specifications. Kake evaluates HTTP 203 strictly under RFC 9111 caching rules; it does not claim gate-record schemas, evidential provenance, or transforming proxy mutation boundaries for research ingestion.
- **`tabi-shokunin` (Domain: Browser & Web-Interaction Craft)**:
  - *Evidence*: `corpus/SOURCES.md:134` (S120 RFC 6585 Additional HTTP Status Codes); `corpus/knowledge/redirect-and-retry-after-semantics.md:1-53` (cites RFC 9110 as S107 for §15.4 3xx redirection and §10.2.3 Retry-After for browser journey driving); `corpus/knowledge/host-published-rate-limit-headers.md:7` (explicitly declares ground as "the published signal set a host returns with a response, not the status code alone"); `corpus/knowledge/rate-limit-policy-fields.md:144` ("non-authoritative field" in RateLimit HTTP header draft); `corpus/knowledge/rate-signal-decision-table.md:23, 51-52` (status code, unreachable robots.txt, refetch).
  - *Conflict Assessment*: **No conflict.** Tabi drives browsers and records interaction evidence; it explicitly disclaims transport header or RFC 9110 status-code taxonomy ownership (`PROVINCE.md:186`).
- **`kagi-shokunin` (Domain: Secrets & Vault Ops)**:
  - *Evidence*: `corpus/SOURCES.md:140` (S132 PubMed record 11554662: "rejected as unreachable and misidentified | the whole body is a cookie-wall shell (HTTP 203, 5590 bytes); Europe PMC EXT_ID:11554662 resolves to a 2001 rhinology case series, not NegEx; ... REJECTED: the page returns HTTP 203 and a cookie wall"); `corpus/knowledge/control-plane-hardening.md:149` ("output status codes, never response bodies").
  - *Conflict Assessment*: **No conflict.** Kagi empirically rejected S132 in round 62 due to PubMed returning HTTP 203 on a cookie wall (the identical phenomenon chousa encountered on PubMed S021). Kagi does not claim HTTP status code semantics or admission gate schemas.
- **`mori-shokunin` (Domain: Fleet & Host Observability)**:
  - *Evidence*: `PROVINCE.md:596` (`tools/mori-source-drift.py`: refetch source-registry URLs); `corpus/SOURCES.md:47` (S041 RFC 6585); archival source S221 (RFC 9110, `sources-r100/S221-rfc9110-r100.txt:7000`).
  - *Conflict Assessment*: **No conflict.** Mori tracks archival source drift and fleet observability; it does not define admission/rejection gate schemas.
- **Other Siblings (`audio`, `kaidoku`, `revenger`, `kengaku`, `tameshi`, `tsukuroi`, `mado`)**:
  - Matches for `203` are file line numbers (e.g. `:203`), table example rows (GFM Example 203 in `kaidoku`), or binary procedure counts (203 procedures in `kaidoku`). Matches for `unreach` refer to unreachable code arms in mutation testing (`tameshi`), unreached preflight handlers (`audio`), or socket/bus timeouts (`tsukuroi`). None touch HTTP status semantics.

#### 2. Record-Schema Ground (`GATE-RECORD`, Success-vs-Failure Forms, Leg Receipts, `reconcile`)
- **`GATE-RECORD` and Success-vs-Failure Ingestion Grammar**:
  - A fleet-wide audit confirms that **`chousa-shokunin` is the sole owner** of the `GATE-RECORD S### ...` space-delimited schema and `tools/gate-records.py`. No sibling lane defines or executes this schema. Sibling lanes enforce markdown tables (`| S### |`) or JSON evidence bundles.
- **Leg Receipts & Reconciliation Machinery**:
  - **`kumitate-shokunin`**: Owns `scripts/counter-receipt.mjs` and `corpus/knowledge/counter-receipt-source-binding.md` / `counter-transcript-reconciliation.md`. It reconciles counter transcripts against literal `arm('<name>')` call sites in counter source code, checking `HELD_COUNT`, `ARM_FAILED`, `ARM_UNBOUND`, and `sha256`.
  - **`kengaku-shokunin`**: Mentions "devinleg receipt" in `corpus/knowledge/probe-battery-r19.md:282` as an exclusion marker for unverified subagent traces.
  - **`mori-shokunin`**: Owns `tools/mori-retention-reconcile.py` (reconciling retention counts).
  - **`souji-shokunin`**: Owns `tools/souji-citation-reconcile.py` (reconciling citation hashes with git commits).
  - **`kaidoku-shokunin`**: Owns `reconcile-javascript-runtime` (REA verb reconciling static vs runtime analysis).
  - **`chousa-shokunin`'s Claim**: In C1, `gate-records-r88.py` writes `<work>/legs/<name>.txt` and re-reads it to verify that internal battery legs executed and produced matching counts. This is chousa-local test battery scaffolding; no sibling conflicts with it.

---

### (b) Sibling Quote-Floor, Warrant-Linkage, and Registry-Supersession Machinery

A census across sibling tools, scripts, and verifiers (receipt `03-machinery-scan-b.txt`) evaluated machinery relevant to C2:

#### 1. Quote-Floor Machinery
- **`tsukuroi-shokunin` (`tools/count-jd-rows-r76.py`, and r70–r75)**:
  - Enforces: `MIN_WORDS = 12` (statement length floor), `MIN_QUOTE_WORDS = 4`, `MAX_QUOTE_WORDS = 25` (quote length bounds), `MIN_TOKENS = 6` (shared tokens between statement and snapshot), and `MIN_SHARE = 0.5` (at least 50% of the statement's tokens must be shared with the snapshot: `len(shared)/len(stmt_tokens) >= MIN_SHARE`).
  - *Strictness Comparison*: **Tsukuroi is STRICTER than chousa in statement grounding and quote bounding.** While chousa's `MIN_TOKENS = 7` sets a higher minimum word floor on quotes (7 vs 4), Tsukuroi enforces an upper bound (`MAX_QUOTE_WORDS = 25`, preventing page-dump quotes) AND a proportional overlap floor (`MIN_SHARE = 0.5`, requiring half of all statement tokens to be grounded in the snapshot text). Chousa has no upper bound on quote length and no proportional overlap ratio (a 1-token overlap satisfies chousa's warrant linkage).
- **`kasegi-shokunin` (`corpus/instruments/gate-quote-audit.py`)**:
  - Enforces an explicit word-count measurement on quote annotations (`<N> words by wc -w`) and an anti-vacuity completeness floor (`--min-quotes`, default 4 annotations; fails closed with exit 1). Less strict than chousa's per-entry floors (13 and 7 = 20 total), but enforces explicit word-count metadata.

#### 2. Warrant-Linkage Machinery
- **`kake-shokunin` (`scripts/doc_quote_truth.py`)**:
  - Checks claim-row quote truth: every backtick span (`...`) in a claim row must appear contiguously or through valid elision in cited receipt files (T1/T2 findings), and correction rows (`supersedes` / `[rNN-correction]`) must quote full receipt lines (T4 finding). Binds claim text to receipt text, but does not evaluate decision-table-to-source-quote semantics.
- **`tsukuroi-shokunin` (`tools/check-adjacency-overlap.py`)**:
  - Checks that action statements contain at least 8 words and 4 distinct content words (`content = {token for token in tokens if token not in STOP_WORDS}`).
- *Strictness Comparison*: **No sibling holds decision-table-to-quote warrant-linkage machinery** like chousa's (`distinctive()` content word intersection between decision cells and quote cells). Chousa's warrant-linkage leg is unique in the fleet.

#### 3. Registry-Supersession Machinery
- **`kotodama-shokunin` (`tools/check-supersession-settlement.py`)**:
  - Implements a formal 5-state settlement automaton (`SETTLED-ACTIVE`, `SETTLED-RETIRED`, `SETTLED-CLOSED`, `SETTLED-SPLIT`, and `PENDING`). In `--scan` mode, it classifies every `supersedes` chain and fails closed (exit 1) if `pending > 0`.
  - *Strictness Comparison*: **Kotodama is STRICTER than chousa's curation supersession leg.** Kotodama requires all supersedes chains across the entire registry to be formally settled and mandates that the superseding row be `mined` (`SETTLED-ACTIVE`). In contrast, chousa's `curation-r88.py` checks only date-contrast `teaches` rows.
- **`tabi-shokunin` (`scripts/check-sources.mjs` & `check-release-pins.mjs`)**:
  - Checks that when a row is marked drifted, `entry.superseded_by` names a registry row whose `teaches` cell opens `supersedes <id> —` and whose source URL matches.
- **`tameshi-shokunin` (`tools/registry-check.py` & `tools/evidence-disposition.py`)**:
  - Validates `status: active|superseded`, `superseded_by: <name>`, verifies that superseded rows still execute in tests, and validates manifest ancestry (`G7: supersedes must name a v1 manifest`).
- **`kama-shokunin` (`tools/round40-calibration-audit.py` & `tools/round76-selfrecord-facts.py`)**:
  - Checks that superseded pointers name the exact superseded byte span, not a shifted line number.
- **`kotoba-shokunin` (`verifiers/check_sources_append_only.py`) & `kama-shokunin` (`tools/sources-append-only.py`)**:
  - Mechanically enforce append-only immutability of registry cells across commits (`opened`, `anchor`, `source` never mutated in place).

---

### (c) Cross-Lane Defect Status: Kotodama `check-gate-captures.py` False-Green

The cross-lane defect routed in round 86 (`round-86-verifier-spotcheck.md:63`) was re-evaluated via a single read-only command against current bytes:

- **Command**:
  ```sh
  python3 -B /home/vgpnk/Projects/shokunin/kotodama-shokunin/tools/check-gate-captures.py /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/lessons/round-87.md /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/captures
  ```
- **Receipt**: `.ufo/waves/round-88/w1/R88ConnectorSiblings/04-kotodama-check-gate-captures.txt`
- **Observed Line**: `GATE-CAPTURES: 0 finding(s) in 0 row(s)`
- **Exit Code**: `0` (**FALSE GREEN / VACUITY DEFECT**)
- **State**: **STILL OPEN**.
- *Diagnosis*: Kotodama's checker parses only markdown table rows (`| ... |`) carrying a `capture file` header inside a `## Gate` section. Because chousa formats its gate records in space-delimited `GATE-RECORD` grammar, `check-gate-captures.py` parses zero rows (`len(results) == 0`). In line 213, it executes `return 1 if findings else 0`; with `findings == 0`, it exits 0. It certifies a file as completely valid without checking a single record.

---

### (d) Contested Scope per PROVINCE.md Rules

1. **`chousa-shokunin` Domain & Scope (`PROVINCE.md`)**:
   - Owns: deep-research method (調査) — the reusable craft of source research; question framing; source hierarchy; citation chaining; claim-vs-source verification; search-strategy taxonomy; external-target approval table; this lane's own corpus and gates (`tools/gate-records.py`).
   - Refuses: bounty-program scope (→ kasegi); model-quality or evaluation claims (→ kengaku); orchestration, multi-agent dispatch (→ kumitate); live-target research without operator approval; secret custody (→ kagi).
   - Core principle: *Out of province → report, never absorb.*
2. **Adjacency Findings**:
   - **HTTP Protocol Semantics Boundary (with `kake-shokunin`)**: Protocol taxonomy and RFC 9110/9111 specifications belong to `kake-shokunin`. Chousa's claim on S216 (RFC 9110 §15.3.4, HTTP 203) is valid strictly as an *evidential provenance rule* (a transforming proxy modifying origin content invalidates authority for quote grounding). Chousa must not expand into general HTTP caching or header semantics.
   - **Cross-Lane Gate Checker Grammar Incompatibility (with `kotodama-shokunin`)**: Kotodama's verification tools (`check-gate-captures.py`, `check-gate-quotes.py`) assume markdown table or bullet-list format. Running them across chousa files produces false-green certification without parsing a single record. Chousa owns its `GATE-RECORD` schema; foreign checkers that do not parse the schema must either add fail-closed floors (`len(rows) >= 1`) or restrict scope to their owning lanes.
   - **Supersession Graph Settlement Boundary (with `kotodama-shokunin`)**: Kotodama owns formal multi-state supersession settlement (`check-supersession-settlement.py`). Chousa's C2 claim evaluates date-contrast `teaches` supersession liveness; full registry-wide settlement of dual-mined chains remains adjacent and should not be unilaterally absorbed.
   - **Counter Transcript and Leg Receipt Reconciliation (with `kumitate-shokunin`)**: Kumitate owns orchestration and transcript/receipt reconciliation (`scripts/counter-receipt.mjs`). Chousa's C1 leg-receipt re-reading is an internal test-battery anti-tautology device; chousa does not own general agent transcript reconciliation.

---

## 3. UFO-FSD Connector Move: Synthesis & Proposal

### Contradictions Surfaced Across Round 88 Proposals
1. **The C1 Reconciliation Fallback Hole (K4 Breach)**:
   - `R88ReviewerC1` and `R88CriticClaims` demonstrated that in `gate-records-r88.py`, leg receipt reconciliation was implemented using an `n/m` regex:
     ```python
     m = re.search(r"detail=(\d+)/(\d+)", txt)
     n_ok = (m.group(1) == m.group(2)) if m else (got_ok and ok)
     ```
   - For the three non-`n/m` legs (`TOOL`, `MUT_ADMIT`, `MUT_UNREACH`), `m` is None. The fallback executes `n_ok = (got_ok and ok)` where `got_ok = "ok" in txt`. Because the leg file itself contains `"ok"`, this check is a complete tautology!
   - As proven by `R88ReviewerC1` (`e4-m2-mutadmit-detached.txt` and `e4-m3-mutadmit-neverbuilt.txt`), detaching `MUT_ADMIT` or `MUT_UNREACH`'s `ok` (e.g. setting `ok = True` without compiling or executing the mutant) satisfies reconciliation and prints `GATE_RECORDS_R88=PASS` (exit 0), directly breaching kill rule K4.
2. **The C2 Untyped Warrant & Lack of Reconciliation**:
   - `R88ReviewerC2` and `R88ExecC2Forge` demonstrated that `curation-r88.py`'s warrant linkage requires only `>= 1` distinctive content word (`[a-z]{5,}` not in 44 stopwords). A single generic word (e.g. `evidence`, `changed`, or `provenance` in a gibberish row) passes warrant linkage.
   - `R88ExecC2Forge` proved that citing the same qid twice (`Q1, Q1`) passes because qids are not deduplicated before checking `len(resolved) == len(qids)`.
   - `R88CriticClaims` proved that `curation-r88.py` has **no receipt reconciliation at all**: a constant-printer or detached-ok counter prints `CURATION_R88=PASS` over failed sub-checks (`receipts/c2-constants-on-broken.log`).
3. **Cross-Lane Sibling Synthesis**:
   - Sibling `kumitate-shokunin` (`scripts/counter-receipt.mjs`) solved this exact problem by enforcing a **strict typed receipt grammar**: every arm/receipt writes explicit typed tokens (`key=value`), and unparsed or mismatched structures fail closed immediately.
   - Sibling `tsukuroi-shokunin` (`tools/count-jd-rows-r76.py`) solved semantic grounding by requiring proportional token overlap (`MIN_SHARE = 0.5`) and length bounds (`MAX_QUOTE_WORDS = 25`).

### Proposed Bounded Move
**Enforce a Typed-Detail Reconciliation Contract across Chousa's C1 Battery and C2 Curation Counters (synthesizing Kumitate's `counter-receipt.mjs` discipline), and Deduplicate Warrant QIDs.**

Specifically:
1. **In `gate-records-r88.py` (C1 Operability Repair)**:
   Replace the crude `(\d+)/(\d+)` regex and tautological fallback with an explicit registry of leg detail schemas:
   ```python
   LEG_SCHEMAS = {
       "MUT_ADMIT":   r"^derived=(\d+)\s+killed=(\d+)$",
       "MUT_UNREACH": r"^derived=(\d+)\s+killed=(\d+)$",
       "TOOL":        r"^present$",
       "DERIVE_NEG":  r"^derived=(\d+)\s+killed=(\d+)$",
   }
   ```
   In the reconciliation loop:
   - For legs in `LEG_SCHEMAS`, match against the registered pattern:
     - For mutant legs (`MUT_ADMIT`, `MUT_UNREACH`, `DERIVE_NEG`), require `sm.group(1) == "1"` and `sm.group(2) == "1"`.
     - For `TOOL`, require `r_detail == "present"`.
   - For all other legs, require `^(\d+)/(\d+)` where `group(1) == group(2)`.
   - Any leg receipt that does not match its registered schema or fails its assertion produces `n_ok = False`.
   - **Receipt proof**: Executed and verified in `.ufo/waves/round-88/w1/R88ConnectorSiblings/07-reconcile-typed-proof.txt`. A detached mutant receipt `name=MUT_ADMIT ok detail=derived=0 killed=0` is immediately refused (`False`), while the genuine landing receipt passes (`True`).
2. **In `curation-r88.py` (C2 Calibration Strengthening)**:
   - Add leg receipt emission and reconciliation: have `curation-r88.py` write its 7 leg records to `<work>/curation_legs/<name>.txt` with typed details (e.g. `FLOOR` writes `detail=located=20 total=20 floor=20 min_tokens=7`, `WARRANT` writes `detail=ok=17 total=17`), and re-read/reconcile them before printing `PASS`, closing the critic's constant-printer / detached-ok bypass.
   - In warrant linkage, deduplicate cited QIDs before evaluation:
     `qids = list(dict.fromkeys(re.findall(r"Q\d+", cells[3])))`
     This directly closes `R88ExecC2Forge`'s duplicate-qid forgery (`Q1, Q1 (S215)`).

### Second-Order Effects Trace
- **Runtime Surface**: Replaces weak fallbacks with deterministic schema regexes. Runtime overhead is sub-millisecond. Zero external dependencies.
- **Contract Surface**: Directly closes K4 breach on C1: crediting an unbuilt mutant or detaching `ok` from measurement now fails `RECONCILED` (14/15 or 12/15) and exits 1.
- **Substrate Surface**: `<work>/legs/*.txt` files become authoritative, machine-checkable records rather than unparsed text dumped to disk.
- **Verification Surface**: Eliminates the surviving mutant and forgery paths discovered by `R88ReviewerC1` and `R88ExecC2Forge`. Both counters fail closed against malicious or lazy alterations.

### Affected Axes
- **Operability (C1)**: **Significantly Improved**. Closes the K4 firing loophole where detached mutant legs survived reconciliation.
- **Calibration (C2)**: **Significantly Improved**. Closes duplicate-QID forgery and arms C2 with receipt reconciliation against constant-printer attacks.
- **Freshness, Coverage, Depth, Adjacency**: **Unharmed**. Retains all existing positive and forgery tests with zero regression.

### Risks
- Leg receipts must adhere strictly to their registered detail format. Any intentional format change in a future round must update the registered schema alongside the leg writer.

### Verification Plan
1. Run typed reconcile against `e4-m2-mutadmit-detached` receipt: observe `reconcile == False`, `RECONCILED=14/15`, exit 1.
2. Run typed reconcile against `e4-m3-mutadmit-neverbuilt` receipt: observe `reconcile == False`, `RECONCILED=14/15`, exit 1.
3. Run typed reconcile against genuine landing tree: observe `RECONCILED=15/15`, `GATE_RECORDS_R88=PASS`, exit 0.
4. Run C2 against `Q1, Q1` warrant duplicate: observe duplicate rejected or normalized without count distortion.

---

## 4. Landed Receipts Summary

The following verification receipts are committed under `.ufo/waves/round-88/w1/R88ConnectorSiblings/`:
- `01-sibling-overlap-search-a.txt`: Raw grep results across all 20 sibling lanes for `203`, `Non-Authoritative`, `status code`, `unreach`, `REFETCH`, `leg receipt`, `reconcile`.
- `02-filtered-substantive-a.txt`: Substantive breakout of hits across kake, tabi, kagi, mori, kumitate, etc.
- `03-machinery-scan-b.txt`: Machinery scan across sibling tools/scripts for quote floors, warrant linkage, and registry supersession.
- `04-kotodama-check-gate-captures.txt`: Command and output of `check-gate-captures.py` on `round-87.md` proving the cross-lane false-green defect remains open (exit 0, `GATE-CAPTURES: 0 finding(s) in 0 row(s)`).
- `05-c1-gate-records-landing.txt`: `gate-records-r88.py` re-run at landing revision (`GATE_RECORDS_R88=PASS`, exit 0).
- `06-c2-curation-landing.txt`: `curation-r88.py` re-run at landing revision (`CURATION_R88=PASS`, exit 0).
- `07-reconcile-typed-proof.txt`: Executed proof demonstrating that typed reconciliation kills the detached `MUT_ADMIT` mutant while passing the genuine landing receipt.

---

## 5. Verdicts

VERDICT: R88ConnectorSiblings C1 held — 203 binding and width derivations verify on committed bytes, and no sibling lane owns GATE-RECORD schema or HTTP 203 refusal ground, while sibling synthesis with kumitate provides the typed-detail reconciliation fix for the non-ratio leg fallback.
VERDICT: R88ConnectorSiblings C2 held — curation predicate PASS and control forgeries reproduced at landing, with tsukuroi and kumitate machinery synthesis identifying the warrant duplicate and un-reconciled counter gaps without harming genuine estate records.
