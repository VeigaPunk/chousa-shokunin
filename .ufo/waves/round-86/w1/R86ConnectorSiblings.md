# R86ConnectorSiblings — Cross-Lane Sibling-Overlap Scan & Synthesis

Seat: `R86ConnectorSiblings` (leaf). Lane: `chousa`, round 86, wave w1.
Base: `3bfb6885958ad4a674ad1896f70d1e836be609e4` | Landing: `667a5d091dc46168ed95eda0ae7f19a9bcf139a2`.
Claims evaluated: C1 operability (`D1` 203-refusal & `M17` mutant kill), C2 calibration (`S024`/`S031` supersession & `S023` warrant entailment).
Ground source: `S216` (RFC 9110 §15.3.4, 203 Non-Authoritative Information).

---

## 1. Declared Axes

1. **Operability (C1)**: Capability acquisition and repair. Verifies that the successor battery (`corpus/evidence/round86/gate-records-r86.py`) incorporates the 200-only `D1` refusal class (an admit whose stored body arrived under HTTP 203, built from committed `S021` refetch bytes) inside the predicate, and derives/kills the round-85 `M17` mutant (`D1_REFUSED=1/1`, `MUT17_KILLED=1/1`).
2. **Calibration (C2)**: Epistemic alignment and internal consistency. Verifies that committed curation defects are resolved: the `S024` (queued) / `S031` (mined) supersession inversion is closed, and decision-table cells carry only distinctions entailed by their located warrant quotes (`S023` definition quote at line 8786, `SUPERSEDED_LIVE=0`, `UNENTAILED_TERM=0`, `MODIFIED_DEF_CITED=1`, `QUOTES_LOCATED=20/20`).

---

## 2. Sibling-Overlap Scan

### (1) Sibling Ground Overlap (RFC 9110 / 203, Supersession, Gate Verifiers)

A read-only grep across `/home/vgpnk/Projects/shokunin/*-shokunin` (receipts in `.ufo/waves/round-86/w1/R86ConnectorSiblings/`) reveals specific cross-lane overlaps:

1. **RFC 9110 & HTTP 203 Semantics**:
   - `kake-shokunin` (Domain: Web Properties & Publishing): Holds the fleet's primary RFC 9110 ground across dozens of sources (S028, S088, S430, S433, S453, S454, S477, S478, S479, S487). Specifically, `kake-shokunin/corpus/lessons/round-81-gate/rfc9110.html:11184` (and `rfc9110.txt:7000`) carries the full verbatim text of §15.3.4 "203 Non-Authoritative Information". Furthermore, in `kake-shokunin/scripts/stored_reuse.py:50`, status 203 is explicitly included in `CACHEABLE_STATUS = (200, 203, 204, 206, 300, 301, 308, 404, 405, 410, 414, 501)` under RFC 9111 §4.2.2 generic caching rules.
   - `mori-shokunin` (Domain: Source Archives & Retention): Holds RFC 9110 as registered source `S221` (`corpus/evidence/sources-r100/S221-rfc9110-r100.txt:7000`, `corpus/evidence/sources-r37/S221.src:261`), including section 15.3.4.
   - `kagi-shokunin` (Domain: Secrets & Identity Custody): In round 62 (`corpus/SOURCES.md:140` and `corpus/lessons/round-62.md:32`), S132 (PubMed record 11554662) was evaluated and **rejected** because `the page returns HTTP 203 and a cookie wall (the term negation occurs 0 times in the rendered body)`. This is the exact live phenomenon that hit chousa's PubMed S021 refetch row in round 85.
   - *Receipt*: `.ufo/waves/round-86/w1/R86ConnectorSiblings/10-grep-rfc9110-http203.txt`.

2. **`supersedes` & Supersession Invariants**:
   - `kotodama-shokunin`: Holds a formal 5-state supersession settlement automaton in `tools/check-supersession-settlement.py:2-42` (`SETTLED-ACTIVE`, `SETTLED-RETIRED`, `SETTLED-CLOSED`, `SETTLED-SPLIT`, and `PENDING`).
   - `kotoba-shokunin`: Holds `verifiers/check_sources_append_only.py:1-23`, mechanically enforcing `CORPUS.md` rule 2 ("A correction is a new row whose teaches opens `supersedes S0NN —`").
   - `kama-shokunin`: Holds `tools/sources-append-only.py:2-27`, diffing immutable registry cells across revisions.
   - *Receipt*: `.ufo/waves/round-86/w1/R86ConnectorSiblings/11-grep-supersedes-settlement.txt`.

3. **`GATE-RECORD` Verifiers**:
   - `tsukuroi-shokunin`: Records `R26-GATE-RECORD-MISSING` in `corpus/QUALITY.md:125` and `corpus/lessons/round-26.md:87`.
   - `mado-shokunin`: References gate records in `LOG.md:4373` and `corpus/lessons/round-90.md:38`.
   - `kama-shokunin`: Cites `gate-record.out` in `corpus/lessons/round-73-verifier-spotcheck.md:47, 59`.
   - *Grammar Boundary*: Sibling lanes enforce markdown tables (`| S### |`) or bullet lists (`- S###`); `chousa` is the only lane using the `GATE-RECORD S<id> ...` space-delimited key=value grammar verified by `tools/gate-records.py`.
   - *Receipt*: `.ufo/waves/round-86/w1/R86ConnectorSiblings/12-grep-gate-record-verifiers.txt`.

---

### (2) Vacuity and False-Green Scan Against Sibling Checkers

We executed sibling verifiers against chousa's round-86 files to determine whether any sibling tool accepts chousa bytes and exits 0 while selecting 0 rows (the kotodama `check-gate-captures.py` vacuity class):

1. **`kotodama-shokunin/tools/check-gate-captures.py`**:
   - **Command**: `python3 -B /home/vgpnk/Projects/shokunin/kotodama-shokunin/tools/check-gate-captures.py /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/lessons/round-86.md /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/captures`
   - **Receipt**: `.ufo/waves/round-86/w1/R86ConnectorSiblings/01-check-gate-captures-on-r86.txt`
   - **Observed Line**: `GATE-CAPTURES: 0 finding(s) in 0 row(s)`
   - **Exit Code**: `0` (**FALSE GREEN / VACUITY DEFECT**)
   - **Diagnosis**: The tool parses only markdown table rows (`| ... |`) carrying a `capture file` header. Because chousa's `corpus/lessons/round-86.md` formats its records as `GATE-RECORD S216 ...`, zero rows are parsed (`len(results) == 0`). In line 213, the tool executes `return 1 if findings else 0`; with `findings == 0`, it exits 0. It certifies a file as completely valid without checking a single record.

2. **`kotodama-shokunin/tools/check-gate-quotes.py`**:
   - **Command**: `python3 -B /home/vgpnk/Projects/shokunin/kotodama-shokunin/tools/check-gate-quotes.py /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/lessons/round-86.md`
   - **Receipt**: `.ufo/waves/round-86/w1/R86ConnectorSiblings/02-check-gate-quotes-on-r86.txt`
   - **Observed Line**: `GATE_QUOTES: 0 findings`
   - **Exit Code**: `0` (**FALSE GREEN / VACUITY DEFECT**)
   - **Diagnosis**: The tool only recognizes rows starting with `r"^[-*]\s*(?:\*\s*)?S\d+"`. Chousa's records start with `GATE-RECORD S216`, so zero rows are selected and it exits 0.

3. **Comparison with Fail-Closed Sibling & Lane Tools**:
   - **`kasegi-shokunin/corpus/instruments/gate-quote-audit.py`**:
     - **Command**: `python3 -B /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/gate-quote-audit.py --root /home/vgpnk/Projects/shokunin/chousa-shokunin`
     - **Receipt**: `.ufo/waves/round-86/w1/R86ConnectorSiblings/03-kasegi-gate-quote-audit.txt`
     - **Observed Line**: `GATE-QUOTE-AUDIT annotated=0 ok=0 erratum-on-record=0 failures=2`
     - **Exit Code**: `1` (**FAILS CLOSED**)
     - **Diagnosis**: Kasegi enforces an anti-vacuity floor (`--min-quotes`, default 4). When 0 annotations match, it fails closed with exit 1.
   - **`chousa-shokunin/tools/gate-records.py`**:
     - **Command on round-86**: `python3 -B /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/gate-records.py verify --root /home/vgpnk/Projects/shokunin/chousa-shokunin /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/lessons/round-86.md`
     - **Receipt**: `.ufo/waves/round-86/w1/R86ConnectorSiblings/04-chousa-gate-records-r86.txt`
     - **Observed Line**: `GATE_RECORDS files=1 records=2 ok=2 fail=0`, Exit `0`.
     - **Command on vacuous file**: `python3 -B /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/gate-records.py verify --root /home/vgpnk/Projects/shokunin/chousa-shokunin /home/vgpnk/Projects/shokunin/chousa-shokunin/README.md`
     - **Receipt**: `.ufo/waves/round-86/w1/R86ConnectorSiblings/05-chousa-gate-records-vacuity.txt`
     - **Observed Line**: `GATE_RECORDS files=1 records=0 ok=0 fail=0`, Exit `1` (**FAILS CLOSED** on `records == 0`).

4. **Testing Sibling Supersession & Append-Only Checks on Chousa**:
   - **`kotodama-shokunin/tools/check-supersession-settlement.py --scan`**:
     - **Command**: `python3 -B /home/vgpnk/Projects/shokunin/kotodama-shokunin/tools/check-supersession-settlement.py --root /home/vgpnk/Projects/shokunin/chousa-shokunin --scan`
     - **Receipt**: `.ufo/waves/round-86/w1/R86ConnectorSiblings/06-kotodama-supersession-scan.txt`
     - **Observed Lines**:
       `SETTLED-ACTIVE S031>S024 s=mined t=queued same_url=True used_by=1`
       `PENDING S073>S070 s=mined t=mined same_url=False used_by=1`
       `PENDING S176>S171 s=mined t=mined same_url=True used_by=2`
       `PENDING S200>S196 s=mined t=mined same_url=True used_by=1`
       `PENDING S201>S197 s=mined t=mined same_url=True used_by=1`
       `SETTLEMENT: pending=6 chains=10 usedby_paths=198 missing_paths=0`
     - **Exit Code**: `1`
     - **Significance**: Kotodama's checker successfully recognizes chousa's round-86 repair as `SETTLED-ACTIVE S031>S024`. However, it flags 4 legacy pairs where both rows are `mined` as `PENDING` because chousa lacks kotodama's `SETTLED-SPLIT` qualifier syntax.
   - **`kotoba-shokunin/verifiers/check_sources_append_only.py`**:
     - **Command**: `python3 -B /home/vgpnk/Projects/shokunin/kotoba-shokunin/verifiers/check_sources_append_only.py --repo /home/vgpnk/Projects/shokunin/chousa-shokunin --base 3bfb6885958ad4a674ad1896f70d1e836be609e4 --rev 667a5d091dc46168ed95eda0ae7f19a9bcf139a2`
     - **Receipt**: `.ufo/waves/round-86/w1/R86ConnectorSiblings/07-kotoba-sources-append-only.txt`
     - **Observed Lines**:
       `breach 667a5d091 S024 anchor: lastReviewed property definition paragraph (… -> page heading lastReviewed, definition paragr…`
       `breach 667a5d091 S024 opened: 2026-11-08 -> 2026-10-21`
       `breach 667a5d091 S031 anchor: …on paragraph; Schema.org page served 2026-10… -> …on paragraph; page re-opened 2026-11-08 (cap…`
       `sources append-only breach 3 change(s) in 1 of 1 commits`
     - **Exit Code**: `1`
     - **Significance**: Kotoba's checker strictly fails on in-place changes to `opened` and `anchor`, even when made to restore a pre-defect value.
   - **`kama-shokunin/tools/sources-append-only.py`**:
     - **Command**: `python3 -B /home/vgpnk/Projects/shokunin/kama-shokunin/tools/sources-append-only.py --repo /home/vgpnk/Projects/shokunin/chousa-shokunin --from 3bfb6885958ad4a674ad1896f70d1e836be609e4 --to 667a5d091dc46168ed95eda0ae7f19a9bcf139a2`
     - **Receipt**: `.ufo/waves/round-86/w1/R86ConnectorSiblings/08-kama-sources-append-only.txt`
     - **Observed Line**: `2 append-only violation(s)`, Exit `1`.
   - **`kotodama-shokunin/tools/check-cited-records.py`**:
     - **Command**: `python3 -B /home/vgpnk/Projects/shokunin/kotodama-shokunin/tools/check-cited-records.py --root /home/vgpnk/Projects/shokunin/chousa-shokunin`
     - **Receipt**: `.ufo/waves/round-86/w1/R86ConnectorSiblings/09-kotodama-cited-records.txt`
     - **Observed Line**: `SCRATCH /fast/scratch/hyaku/chousa-r86/l1/cand corpus/lessons/round-86.md`, Exit `1`.
     - **Significance**: Flags scratch path cited in lesson prose (QUALITY 31).

---

### (3) Cross-Lane Boundary Ledger

1. **What Siblings Should Adopt From This Round**:
   - **Anti-vacuity floor**: Kotodama's `check-gate-captures.py` and `check-gate-quotes.py` must adopt chousa's fail-closed discipline (`records >= 1`, exit 1 on 0 records). Exiting 0 on 0 parsed rows allows files with alternative or malformed syntax to bypass gate checks completely.
   - **HTTP 203 Provenance Refusal**: `kake-shokunin` and crawler/archiver lanes should adopt chousa's rule that HTTP 203 responses represent transforming proxies and cannot serve as authoritative origin representations for ground quote extraction, distinguishing cacheability (RFC 9111) from evidential provenance (RFC 9110 §15.3.4).

2. **What Chousa Should Stop Claiming Because Siblings Hold It**:
   - **General HTTP Protocol Semantics**: `kake-shokunin` owns web properties, response headers, and RFC 9110/9111 protocol specifications. Chousa should not claim broad HTTP protocol taxonomy; `S216` is justified strictly under citation grounding and quote registration provenance.
   - **Supersession Taxonomy Re-Invention**: `kotodama-shokunin` already solved multi-row supersession settlement (`SETTLED-SPLIT`). Chousa should stop inventing ad-hoc supersession narrowing rules and align with kotodama's settlement model.
   - **PubMed HTTP 203 Cookie-Wall Discovery**: `kagi-shokunin` already discovered, analyzed, and rejected PubMed's HTTP 203 cookie-wall response in round 62 (`S132`). Chousa's round-85 encounter with PubMed 203 on `S021` was a recurrence of kagi's prior finding.

---

## 3. UFO-FSD Connector Move: Synthesis & Proposal

### Contradictions Identified
1. **Operability vs Schema Completeness**: `tools/gate-records.py` provides only two record shapes: `url/admit` (200 success + capture + quote) and `url/unreach` (failure + `capture=none`). When an HTTP 200 fetch is rejected due to content (e.g. `S217` DCMI Namespace Policy serving a 9-line stub), the tool has no schema form to record the content rejection over the committed capture. This forced chousa to omit `S217` from `round-86.md`'s `## Gate` block entirely (disclosed as Mistake 1).
2. **Calibration vs Cross-Lane Supersession Debt**: In round 86, `curation-r86.py` pre-freeze had to narrow its supersession predicate to measure only the live-vs-unadopted edge (`S024`/`S031`) because checking all mined targets produced false-reds on legitimate two-row histories (`S073/S070`, `S176/S171`, `S200/S196`, `S201/S197`). Meanwhile, kotodama's `check-supersession-settlement.py` flags all four of these pairs as `PENDING` debt (exit 1).
3. **Append-Only Invariant Conflict**: Chousa's in-place restoration of `S024` opened date (undoing round 85's defect) violates sibling mechanical gates (`kotoba` and `kama` append-only verifiers both exit 1).

### Proposed Move
**Synthesize Kotodama's `SETTLED-SPLIT` grammar into Chousa's registry and expand `tools/gate-records.py` with an explicit `url/reject` record form.**

1. In `corpus/SOURCES.md`, append the explicit scope limiter `for entry ... only` to the `teaches` column of the four dual-mined successor rows (`S073`, `S176`, `S200`, `S201`).
2. Add a `url/reject` record form to `tools/gate-records.py`:
   `GATE-RECORD S<id> url=<url> fetched=<ts> tier=<tier> decision=reject capture=corpus/captures/<hash>.txt capture_sha256=<sha> words=0 quote=none reason="<text>"`
   This allows HTTP 200 content rejections (such as `S217`) to carry verifiable capture hashes and gate records without triggering `REFETCH` failures.
3. Update `curation.py` to restore universal supersession scanning across all 10 chains by recognizing `SETTLED-SPLIT` rows, unifying chousa's calibration with kotodama's settlement standard.

### Second-Order Effects Trace
- **Runtime Surface**: `tools/gate-records.py` parses a third valid form (`url/reject`), maintaining strict verification while eliminating the schema blindspot for stub rejections.
- **Contract Surface**: `corpus/SOURCES.md` conforms to Kotodama's QUALITY supersession contract, resolving the 4 `PENDING` findings.
- **Substrate Surface**: Capture files for rejected sources (like `S217`) become mechanically verifiable artifacts rather than unreferenced files.
- **Verification Surface**: `curation.py` checks all 10 registry chains rather than a single hard-coded pair, lifting calibration verifiability to full coverage. Sibling settlement checkers exit 0 on chousa's registry.

### Affected Axes
- **Calibration (C2)**: Significantly improved — eliminates 4 latent `PENDING` supersession debts and provides full-estate supersession verification.
- **Operability (C1)**: Improved without harm — resolves schema defect Mistake 1 without altering the frozen D1/M17 successor battery.

### Risks
- Scope qualifiers in `teaches` must be added through an explicit erratum/round-lesson log to satisfy `CORPUS.md` rule 2.

### Verification Plan
Run `python3 -B /home/vgpnk/Projects/shokunin/kotodama-shokunin/tools/check-supersession-settlement.py --root /home/vgpnk/Projects/shokunin/chousa-shokunin --scan` and observe `pending=0 chains=10 exit=0`.

---

## 4. Verdicts

VERDICT: R86ConnectorSiblings C1 held — D1 HTTP 203 refusal and M17 mutant kill verified on committed bytes with zero regression, while sibling scan reveals kotodama check-gate-captures false-greens on chousa record grammar.
VERDICT: R86ConnectorSiblings C2 held — S024/S031 inversion and S023 warrant entailment verified at landing, though kotodama settlement scanner exposes 4 unresolved legacy dual-mined chains (S073, S176, S200, S201) resolvable via SETTLED-SPLIT synthesis.
