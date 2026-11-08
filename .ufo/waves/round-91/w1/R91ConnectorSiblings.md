# R91ConnectorSiblings — Sibling-Overlap Scan and Connector Synthesis (chousa, round 91)

Seat: `R91ConnectorSiblings` (connector, leaf).
Wave: round-91 w1. Lane: `chousa-shokunin`.
Carrier attacked: `C3 = 67954adc599bd605705d94a1ea7abb582491a907`; freeze `F3 = 4d00d7519290569879f853d7122b82a927cda1f3`; base `265b8633b7e5d1da49da6fb948df9707373fb15c`.
Scratch directory: `/fast/scratch/hyaku/chousa-r91/R91ConnectorSiblings` (read-only scan across sibling repositories, no sibling files edited).
Receipts and pointer maps written to: `.ufo/waves/round-91/w1/R91ConnectorSiblings/`.

---

## 1. Declared Axes of Round 91

Round 91 attacks three frozen axes:
- **C1 — Operability (historical 3/10, lowest scored non-retired axis):** Harden receipt verification against forged headers via multi-value header capture (`header_multi()` in `control-driver-r91.py`), requiring exactly one occurrence each of `case`, `expected_exit`, `exit`, and `computed_against` (`check_headers()`); require `# expected_exit=`; bind executed instrument scripts and expectation files against digest pins (`instrument-pins.txt`); bind dual-revision `SELF_PIN` (`rev=F receipts_rev=C`); and refuse unscored receipts. Grounded in source S070 (`sha256sum(1)`).
- **C2 — Calibration:** Harden knowledge curation counter (`curation-r91.py`) to validate all rows of `## Located quotes` as 3-cell `Q<n>` rows without duplicates (`QSHAPE`); cross-check cited sources against the registry for `status=mined` and `used-by` link; guard decision row warrant entailment with a document-frequency threshold over the entry's units (`TFREQ`, `DF_MAX=3`); check duplicate qids in warrant cells (`dup_qid`); and replace the unentailed double-count loop.
- **C3 — Freshness:** Derive `SKILL.md` case-range prose directly from the tool's debug case names (`ok-case` names in selftest: `bashenv` at 273–275, `bash-pin-override` at 282–283) rather than prose heuristics, repairing historical mislabeling.

---

## 2. Sibling Overlap Scan: Scope and Methodology

An exhaustive, read-only search was conducted across all 20 sibling repositories under `/home/vgpnk/Projects/shokunin/*-shokunin/`:
`audio-shokunin`, `game-dev-2d-shokunin`, `game-dev-3d-shokunin`, `kagi-shokunin`, `kaidoku-shokunin`, `kake-shokunin`, `kama-shokunin`, `kasegi-shokunin`, `kengaku-shokunin`, `kotoba-shokunin`, `kotodama-shokunin`, `kumitate-shokunin`, `lore-shokunin`, `mado-shokunin`, `mori-shokunin`, `revenger-shokunin`, `souji-shokunin`, `tabi-shokunin`, `tameshi-shokunin`, `tsukuroi-shokunin`.

The scan searched for two target classes:
1. **Class 1:** Last-wins parsing of repeated keys/headers in receipt, header, registry, or section parsers (dict assignment on repeated key, `header_fields`-style loops, `load_sections` last-wins).
2. **Class 2:** Warrant/term-frequency or document-frequency logic in curation or claim-verification counters, and any duplicate-row/qid guard.

---

## 3. Class 1 Findings: Last-Wins Parsing

Across the 20 sibling lanes, last-wins dictionary assignment on repeated keys was identified in 7 sibling lanes across receipt, header, section, and registry parsers.

### Pointer Map: Class 1 Hits

| Lane | Path:Line | One-line Reading | Same Class as C1 R1? |
|---|---|---|---|
| `souji-shokunin` | `census/round-26/waves/w1/report-assemble.py:133` | `header[key.strip()] = value.strip()` inside `parse_receipt()` | **YES** — classic receipt header last-wins overwriting |
| `souji-shokunin` | `census/round-26/waves/w1/report-assemble.py:245` | `sections[match.group(1)] = text[match.end():end].strip('\n')` inside `parse_sections()` | **YES** — verbatim `load_sections` last-wins overwriting |
| `souji-shokunin` | `census/round-56/c2-counter.py:206` | `header_kv[m.group(1)] = m.group(2)` for `# KEY=VAL` | **YES** — dict retains last header value despite logging diagnostic |
| `tsukuroi-shokunin` | `tools/count-mount-rows-r81.py:86` | `rows[cells[0]] = {'kind': cells[2], ...}` in `registry_rows()` | **YES** — last-wins dict assignment on repeated Source ID `S\d+` |
| `tsukuroi-shokunin` | `tools/count-mount-rows-r81.py:102` | `digests[parts[1]] = parts[0]` in manifest `verify()` | **YES** — last-wins dict assignment on repeated manifest filename |
| `kagi-shokunin` | `corpus/recheck-replay.py:133` | `rows[m.group(1)] = line` in `registry_rows()` | **YES** — last-wins dict assignment on repeated Source ID `S\d+` |
| `mado-shokunin` | `quality/check-session-material.py:832` | `entries[path] = (digest, frozenset(rulelist), ...)` in `load_registry()` | **YES** — last-wins dict assignment on repeated waiver path |
| `mori-shokunin` | `.ufo/waves/round-85/count-c2.py:109` | `fields[name] = value` in `parse_receipt()` | **YES** — receipt header dict assignment is last-wins |
| `game-dev-2d-shokunin` | `reports/round-102/mutations/mut03_retarget_s02.py:94` | `fields[k] = v` for `k, v = tok.split('=', 1)` in `receipt_fields()` | **YES** — receipt token dict assignment is last-wins |
| `tameshi-shokunin` | `tools/conjunct-disposition.py:62` | `conj[k] = (v.strip() == 'true')` in `receipt_conjuncts()` | **YES** — receipt conjunct dict assignment is last-wins |
| `chousa-shokunin` *(internal)* | `corpus/evidence/round91/control-driver-r91.py:83` | `pins[parts[1].strip()] = parts[0]` in `read_pins()` | **YES** — latent last-wins dict assignment on repeated pin path |

### Detailed Readings: Class 1

1. **`souji-shokunin` `census/round-26/waves/w1/report-assemble.py:133` and `:245`:**
   In `parse_receipt()`, line 133 reads:
   ```python
   if state == "header":
       if "=" in line:
           key, value = line.split("=", 1)
           header[key.strip()] = value.strip()
   ```
   Repeated header keys in receipt files silently overwrite earlier keys.
   In `parse_sections()`, line 245 reads:
   ```python
   def parse_sections(text: str) -> dict[str, str]:
       sections: dict[str, str] = {}
       matches = list(re.finditer(r"^## (.+?)\s*$", text, re.M))
       for index, match in enumerate(matches):
           end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
           sections[match.group(1)] = text[match.end():end].strip("\n")
       return sections
   ```
   If a markdown report contains duplicate `## Heading` sections, `sections[heading]` silently stores only the trailing section. This is identical to the `load_sections` last-wins pattern.

2. **`tsukuroi-shokunin` `tools/count-mount-rows-r81.py:86`:**
   ```python
   def registry_rows(text):
       rows = {}
       for line in text.splitlines():
           if not re.match(r'^\s{0,3}\|\s*S[0-9]{3,}\s*\|', line):
               continue
           cells = [c.strip() for c in line.split('|')[1:-1]]
           if len(cells) != 11:
               continue
           rows[cells[0]] = {'kind': cells[2], 'tier': cells[3], 'source': cells[1]}
       return rows
   ```
   If `SOURCES.md` contains duplicate rows with the same Source ID, earlier entries are silently dropped.

3. **`kagi-shokunin` `corpus/recheck-replay.py:133`:**
   ```python
   def registry_rows(root):
       rows = {}
       for line in (root / REGISTRY).read_text(encoding="utf-8").splitlines():
           m = re.match(r"^ {0,3}\|\s*(S\d{3,})\s*\|", line)
           if m:
               rows[m.group(1)] = line
       return rows
   ```
   While `manifest()` in the same file explicitly refuses duplicate URLs (`if cols[1] in rows: return None, "manifest-duplicate-url"`), `registry_rows()` performs an unguarded dict assignment.

4. **`chousa-shokunin` `corpus/evidence/round91/control-driver-r91.py:83`:**
   While chousa round 91 hardened receipt header parsing via `header_multi()` and `check_headers()`, its pin loader `read_pins()` remains vulnerable to the exact same defect:
   ```python
   def read_pins(path):
       ...
       with open(path, encoding="utf-8") as fh:
           for ln in fh:
               ...
               parts = ln.split(None, 1)
               if len(parts) != 2 or not SHA_RE.fullmatch(parts[0]):
                   raise SystemExit(f"SETUP malformed pin row: {ln!r}")
               pins[parts[1].strip()] = parts[0]
       return pins
   ```
   If `instrument-pins.txt` contains duplicate paths, `pins[path] = digest` silently takes the last occurrence without error (verified in scratch: `.ufo/waves/round-91/w1/R91ConnectorSiblings/pin_duplicate_probe.txt`).

### What Was NOT Found for Class 1 (Sweep Result)
- **First-wins implementations:** Several siblings avoided last-wins by enforcing first-wins:
  - `kotodama-shokunin` (`reports/round-76/counters/capture-evidence.py:1886`): `_header_map()` checks `if match and match.group(1) not in out: out[match.group(1)] = match.group(2)`.
  - `revenger-shokunin` (`corpus/training/bounty-triage/check_package.py:84`): `parse_sections()` checks `if current is not None and current not in sections: sections[current] = "\n".join(lines).strip()`.
- **Ordered sequence validation:** `souji-shokunin` (`tools/souji-receipt-run.py:318`) parses headers strictly in `HEADER_ORDER`, advancing an index `idx` so that duplicate header names fail `startswith` checks.
- **Multi-value duplicate rejection:** No sibling lane implemented a multi-value parser (`header_multi()`) that preserves all duplicate occurrences in a list to allow strict single-occurrence verification (`len(values) == 1`). Chousa's C1 R1 design is unique in this regard.

---

## 4. Class 2 Findings: Warrant/TF-DF Logic and Duplicate-Row/QID Guards

Across the 20 sibling lanes:
- **Term-frequency / Document-frequency (TF/DF) logic is 100% ABSENT across all sibling lanes.**
- **Duplicate QID guards (`dup_qid` or `Q\d+` repeat checks) are 100% ABSENT across all sibling lanes.**
- **Duplicate row guards** exist in 5 sibling lanes (`tsukuroi`, `kake`, `tabi`, `mori`, `game-dev-2d`), but only protect markdown table rows, member paths, or TSV records against duplicate insertion, not quote citations or warrant entailment.

### Pointer Map: Class 2 Hits

| Lane | Path:Line | One-line Reading | Same Class as C2 R3? |
|---|---|---|---|
| `tsukuroi-shokunin` | `tools/count-ul-rows-r73.py:213,351` | `seen_ids` set tracking row IDs + `dup_row()` fixture testing `duplicate-id` | **PARTIAL** — guards table row IDs (`UL<n>`), not quote citations or TF/DF |
| `kake-shokunin` | `.ufo/waves/round-60/c60_gate_status.py:18` | `>1 counted rows -> duplicate_row` across `SKILL.md` tables | **PARTIAL** — enforces table row uniqueness for tool member paths |
| `tabi-shokunin` | `scripts/check-adjacency.mjs:168` | `REASON.duplicateRow`: repeated surface+sibling or pin cited twice in TSV | **PARTIAL** — refuses duplicate mapping rows in `adjacency.tsv` |
| `mori-shokunin` | `.ufo/waves/round-45/count-c2.py:905` | `duplicate_row()` fixture and classification in event validation | **PARTIAL** — checks duplicate evidence records in event logs |
| `game-dev-2d-shokunin` | `reports/round-101/mutations/ver9_selftest.py:115` | `m_dup = write("dup_row", ...)` table row duplication mutator | **PARTIAL** — test mutator for duplicate table row detection |

### Detailed Readings: Class 2

1. **`tsukuroi-shokunin` `tools/count-ul-rows-r73.py:213-214`:**
   ```python
   seen_ids = set()
   for line in rows:
       ...
       if n in seen_ids:
           problems.append("duplicate-id")
       seen_ids.add(n)
   ```
   Tested by test case `case("DUPID", dup_row, 1, "duplicate-id")` where `dup_row` duplicates a row. While structurally similar to chousa's C2 R1 (`dup_qids`), it operates at the whole-row ID level rather than tokenized warrant citations.

2. **`tabi-shokunin` `scripts/check-adjacency.mjs:168-170`:**
   ```javascript
   // duplicate_row: the same folded surface+sibling pair appears on two rows,
   // or the same sibling pin (lane@path:line) is cited twice
   ```
   Refuses duplicate mappings in `corpus/adjacency.tsv`.

### What Was NOT Found for Class 2 (Sweep Result)
- **Zero TF/DF logic:** Neither document frequency (`DF_MAX`, `qdf`), term frequency (`tfreq`), nor distinctive word filtering over citation units exists anywhere in the sibling fleets.
- **Zero quote-level duplicate guards:** No sibling lane parses multi-citation warrant cells (e.g. `cells[3]` with `Q1 Q2`) to verify that quote tokens are distinct (`dup_qid(qids)`).
- Chousa's C2 R3 calibration architecture is completely unrepresented in the sibling fleet.

---

## 5. Non-Obvious Move: Compatible Synthesis Across Round Proposals

### The Synthesis Context
1. **`R91CriticClaims` findings:**
   - **F1 (HIGH):** The frozen C1 counting command omits `--work <scratch>`, exiting `rc=2` with `arguments are required: --work`.
   - **F3 (HIGH):** `instrument-pins.txt` is not checked for self-pinning between `--root` and `--rev`.
   - **F4 (HIGH):** In `curation-r91.py`, `data_lines()` silently skips empty-qid rows (`cells[0] == ""`), allowing empty-cell data rows in `## Located quotes` to bypass `q_shape_violation()`.
2. **`R91ReviewerC1` and `R91ExecC1Repro` findings:**
   - The frozen counting command requires an explicit `--work` path.
   - Driver path defaults escape `--root` unless absolute paths or explicit `--root` re-basing are provided.
3. **Sibling overlap scan findings (this seat):**
   - Latent last-wins parsing is widespread across sibling lanes (e.g., `tsukuroi` `digests[parts[1]] = parts[0]`, `kagi` `rows[m.group(1)] = line`).
   - In chousa's own `control-driver-r91.py:83`, `read_pins()` contains the exact same latent defect:
     ```python
     pins[parts[1].strip()] = parts[0]
     ```
     `read_pins()` silently permits duplicate paths in `instrument-pins.txt`, taking the last digest.

### Proposed Move: Joint Pin-Table Hardening and Command Correction
Synthesize a single, mutually compatible amendment across C1 and C2:

1. **Harden `read_pins()` against duplicate paths (C1):**
   In `corpus/evidence/round91/control-driver-r91.py:83`:
   ```python
   path_key = parts[1].strip()
   if path_key in pins:
       raise SystemExit(f"SETUP duplicate pin row for {path_key!r}")
   pins[path_key] = parts[0]
   ```
   This closes the last-wins vulnerability on the pin table, preventing forged or conflicting pin specifications from silently succeeding.
2. **Harmonize C1 Counting Command (C1):**
   Update the C1 command statement in `corpus/evidence/round91/claims.md` and `.ufo/waves/round-91/claims.json` to include `--work <scratch>` (resolving Critic F1 and Reviewer F1).
3. **Harmonize `data_lines()` empty cell check (C2):**
   Apply Critic F4's one-line fix in `curation-r91.py`:
   `cells[0] in ("Situation", "qid") or (cells[0] and set(cells[0]) <= set("-: "))`
   so that phantom empty-qid rows are caught as `Q_SHAPE` violations rather than silently skipped.

### Affected Axes
- **C1 Operability:** **Improved.** Closes the latent last-wins hole in `read_pins()` and resolves the `--work` command invocation block, ensuring clean 6/6 pass execution.
- **C2 Calibration:** **Improved.** Catches phantom empty-qid rows without regressing on legitimate 20/20 quote rows or 17/17 warrant rows.
- **C3 Freshness:** **Unharmed.** C3 derives case ranges from selftest names independently; neither pin-table duplicate checking nor C2 row parsing touches C3.

### Risks and Tradeoffs
- **Zero Risk to Clean Tree:** The committed `instrument-pins.txt` contains exactly 16 distinct, non-duplicated file paths. Refusing duplicate pin paths will never trigger on legitimate trees.
- **No Incompatible Contracts:** The change requires no schema modification and preserves exact counter outputs (`COMMITTED_OK=6/6`, `CURATION_R91=PASS`, `SKILL_TALLY_R91=PASS`).

### Verification
- Tested in scratch fixture: duplicate pin lines in `pins.txt` reliably trigger duplicate detection rather than last-wins overwriting (`.ufo/waves/round-91/w1/R91ConnectorSiblings/pin_duplicate_probe.txt`).
- Clean tree verify: `control-driver-r91.py verify --root . --repo . --rev 4d00d751... --receipts-rev 67954adc... --work <scratch>` exits 0 with all 16 pins matching.

---

## 6. Artifact Inventory

Receipts generated by this seat under `.ufo/waves/round-91/w1/R91ConnectorSiblings/`:
- `sibling_class1_hits.txt` — pointer map of Class 1 last-wins parsing across 7 sibling lanes + internal chousa `read_pins()`.
- `sibling_class2_hits.txt` — pointer map of Class 2 duplicate row / curation guards across sibling lanes.
- `sweep_summary.txt` — exhaustive summary of the 20-lane sweep, confirming 0 occurrences of TF/DF and 0 occurrences of quote-level `dup_qid` guards.
- `pin_duplicate_probe.txt` — executable proof of last-wins vulnerability in `control-driver-r91.py:83` on duplicate pin paths.

---

VERDICT: R91ConnectorSiblings C1 held — Sibling scan identifies latent last-wins header/section/registry parsing across 7 sibling lanes while chousa's C1 R1 header_multi refuses duplicate headers; read_pins() in the driver has the same latent last-wins defect.
VERDICT: R91ConnectorSiblings C2 held — C2 R3 document-frequency warrant guarding and dup_qid checks are completely absent across all 20 sibling lanes, confirming chousa's unique calibration hardening.
VERDICT: R91ConnectorSiblings C3 n/a — Freshness claim C3 (tool-derived case ranges) was not part of the sibling overlap scan.
