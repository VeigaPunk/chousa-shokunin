# R92ConnectorSiblings — Sibling-Overlap Scan and Connector Synthesis (chousa, round 92)

Seat: `R92ConnectorSiblings` (connector, leaf).
Wave: round-92 w1. Lane: `chousa-shokunin`.
Carrier attacked: `C5 = 16ccf7693c61b8ffe392fc757352304f239bfcad`; freeze `F5 = 42e0337822a508208800f98faa3a63c6af9f8c27`; base `d7780feff6e39ae74a2fd77fc9773c671b33da95`.
Scratch directory: `/fast/scratch/hyaku/chousa-r92/R92ConnectorSiblings` (read-only scan across sibling repositories, no sibling files edited; cleaned prior to yield).
Receipts cited and copied to: `.ufo/waves/round-92/w1/R92ConnectorSiblings/`.

---

## 1. Declared Axes of Round 92

Round 92 hardens three frozen axes in `chousa-shokunin`:
- **C1 — Operability (historical 3/10, lowest scored non-retired axis):** Harden receipt verification against header whitespace and duplicate pins; require every executed script, expectation file, and the pins file itself to be pinned on disk and at `--rev`; enforce self-pinning of `instrument-pins.txt` via minus-self digest (`pins_file_sha_minus_self`); eliminate last-wins pin parsing by refusing duplicate pin paths (`SETUP PIN_DUPLICATE`); and verify dual-revision `SELF_PIN` (`rev=F receipts_rev=C`). Grounded in source S070 (`sha256sum(1)`).
- **C2 — Calibration:** Harden knowledge curation counter (`curation-r92.py`) to validate all rows of `## Located quotes` as 3-cell `Q<n>` rows without silent skips (`QSHAPE`); enforce exact tokenized `used-by` links from both entry and registry sides (`SOURCE_STATUS_OK=20/20`, `USED_BY_OK=20/20`); pin decision-row width (4 cells) and count (17); and require document frequency `<= 3` for quote-warrant content terms (`TFREQ`).
- **C3 — Freshness:** Derive `SKILL.md` case-range prose directly from the tool's debug case names (`bashenv` at 273–275, `bash-pin-override` at 282–283); scope tally and case-range searches strictly to the `## Gates` section (up to the next `## ` heading); and pin the multiset of historical non-current tallies (`{(161,0):1, (256,0):1}`) so deleting or altering historical quotes changes the verdict.

---

## 2. Sibling Overlap Scan: Scope and Methodology

An exhaustive, read-only search was conducted across all 20 sibling repositories under `/home/vgpnk/Projects/shokunin/*-shokunin/`:
`audio-shokunin`, `game-dev-2d-shokunin`, `game-dev-3d-shokunin`, `kagi-shokunin`, `kaidoku-shokunin`, `kake-shokunin`, `kama-shokunin`, `kasegi-shokunin`, `kengaku-shokunin`, `kotoba-shokunin`, `kotodama-shokunin`, `kumitate-shokunin`, `lore-shokunin`, `mado-shokunin`, `mori-shokunin`, `revenger-shokunin`, `souji-shokunin`, `tabi-shokunin`, `tameshi-shokunin`, `tsukuroi-shokunin`.

The scan searched for two target classes hardened in round 92:
1. **Target Class 1: Self-referential pin tables & Last-wins table parsers** — a pins/sums file whose own digest is listed in itself, sidecar self-pins, or a table read last-wins on repeated paths (`dict[path] = digest` without duplicate checking).
2. **Target Class 2: Section-scoped search vs Document-wide search & Unpinned counts** — counters that search a document font-wide/document-wide where a section-scoped contract exists (heading-anchored extraction), arbitrary byte/character slice windows, or unpinned counts over historical quotations/tallies.

---

## 3. Target Class 1 Findings: Self-Referential Pin Tables & Last-Wins Table Parsing

### Pointer Map: Target Class 1 Hits

| Lane | Path:Line | One-line Reading | Same Class as chousa C1 S5 / self-pin? |
|---|---|---|---|
| `tameshi-shokunin` | `.ufo/evidence/round-92/c1/measure-v92.py:51` | `def self_pin_ok()`: strips `SELF_PIN_RE` (`SELF_SHA256 = "..."`) to compute own minus-self digest | **YES** — direct script-embedded minus-self self-pin, grounded in `sha256sum(1)` |
| `tameshi-shokunin` | `.ufo/evidence/round-95/c1/measure-v95.py:97` | `def self_pin_state()`: checks `len(re.findall(SELF_PIN_RE, b)) == 1` before minus-self digest check | **YES** — minus-self self-pin plus explicit duplicate pin line refusal |
| `kake-shokunin` | `.ufo/waves/round-42/c42_count.py:396` | `sums[path.strip().lstrip("*")] = digest` in `for line in open("SHA256SUMS")` | **YES** — last-wins dictionary assignment on repeated path in checksum table |
| `kake-shokunin` | `.ufo/waves/round-92/c92_defects.py:399` | `pin = show(root, rev, SELF_PIN)`: script verified against external `.sha256` sidecar file | **RELATED** — self-pin via external sidecar file rather than unified minus-self table |
| `kagi-shokunin` | `plans/round-58-c1-check.py:278` | `pins[m.group(2)] = m.group(1)` in `for ln in txt.splitlines()` | **YES** — last-wins dictionary assignment on repeated instrument path |
| `kaidoku-shokunin` | `.ufo/waves/round-80/w1/ScoutRecord/probe.py:87` | `pins[name] = (pin, pointer)  # last-wins, mirrors round 79` | **YES** — explicit last-wins dictionary assignment on pin table extraction |
| `tsukuroi-shokunin` | `tools/count-mount-rows-r81.py:102` | `digests[parts[1]] = parts[0]` in `verify()` manifest parser | **YES** — last-wins dictionary assignment on repeated manifest path |
| `tsukuroi-shokunin` | `.ufo/waves/round-42/w2/C2CritSC1/check-sc1.py:20` | `sums[name.lstrip("*")] = digest` in `for line in open(sums_path)` | **YES** — last-wins dictionary assignment on repeated checksum path |
| `chousa-shokunin` *(prior)* | `corpus/evidence/round91/control-driver-r91.py:83` | `pins[parts[1].strip()] = parts[0]` in `read_pins()` | **YES** — prior r91 last-wins defect repaired in r92 by `SETUP PIN_DUPLICATE` |
| `chousa-shokunin` *(current)* | `corpus/evidence/round92/control-driver-r92.py:179` | `pins_file_sha_minus_self(pins_path, self_rel)` removes self row to compute pin table digest | **YES** — chousa's C1 S5 unified self-pin implementation |

### Detailed Readings: Class 1

1. **`tameshi-shokunin` `.ufo/evidence/round-92/c1/measure-v92.py:51–60` (and `c1/measure-v95.py:97–115`):**
   In `measure-v92.py`, line 37 declares `SELF_SHA256 = "723562ed5b20e1a914d9addbce9007b8edf1c962c8237592dbac3b39e5509c2c"`.
   Lines 51–60 implement the self-pin:
   ```python
   def self_pin_ok():
       """QUALITY 144: the check runs before any other action, on the file's own bytes."""
       try:
           with open(os.path.abspath(__file__), "rb") as f:
               b = f.read()
       except OSError:
           return False
       norm = re.sub(SELF_PIN_RE, b"", b, flags=re.M)
       return hashlib.sha256(norm).hexdigest() == SELF_SHA256
   ```
   Furthermore, line 45 cites `SOURCE_URL = "https://man.archlinux.org/man/sha256sum.1.en"` (Source S320 in tameshi, corresponding to S070 in chousa).
   In round 95 (`measure-v95.py:109`), tameshi hardened this further by verifying that `len(re.findall(SELF_PIN_RE, b, flags=re.M)) == 1`, refusing multiple embedded self-pin lines.
   *Comparison with chousa C1 S5:* Tameshi applies the minus-self digest principle directly to Python script source by regex-stripping the literal `SELF_SHA256` assignment. Chousa C1 S5 applies minus-self to the structured pin table (`instrument-pins.txt`), stripping the row that names `corpus/evidence/round92/instrument-pins.txt` (`pins_file_sha_minus_self()`). Both solve the fundamental circular dependency problem (`sha(file_with_digest) != digest`) using minus-self content hashing.

2. **`kake-shokunin` `.ufo/waves/round-42/c42_count.py:393–397`:**
   ```python
       src = os.path.join(root, REALRUN_DIR)
       sums = {}
       for line in open(os.path.join(src, "SHA256SUMS"), encoding="utf-8"):
           digest, path = line.split(None, 1)
           sums[path.strip().lstrip("*")] = digest
   ```
   Repeated entries for the same path in `SHA256SUMS` silently overwrite previous entries (last-wins). Furthermore, `SHA256SUMS` itself is unpinned in the sums table.
   In round 92 (`.ufo/waves/round-92/c92_defects.py:58, 399`), kake avoided self-referential table parsing by maintaining a separate external sidecar file `.ufo/waves/round-92/frozen/c1-self.sha256` that pins `c92_defects.py`.

3. **`kagi-shokunin` `plans/round-58-c1-check.py:274–278`:**
   ```python
       pins: dict[str, str] = {}
       for ln in txt.splitlines():
           m = INSTRUMENT_RE.match(ln)
           if m:
               pins[m.group(2)] = m.group(1)
   ```
   In `item2()`, instrument pins from `controls-prefreeze-epochC*.txt` receipts are extracted into a dictionary without duplicate detection. If the receipt repeats a path with conflicting digests, `pins[path]` retains the final match.

4. **`kaidoku-shokunin` `.ufo/waves/round-80/w1/ScoutRecord/probe.py:86–87`:**
   ```python
       pins = {}
       for name, pin, pointer in RE_PIN.findall(text):
           pins[name] = (pin, pointer)  # last-wins, mirrors round 79
   ```
   The author explicitly documents that pin extraction is `last-wins`, intentionally mirroring prior round behaviour rather than refusing duplicates.

5. **`tsukuroi-shokunin` `tools/count-mount-rows-r81.py:102`:**
   In manifest `verify()`, lines from the manifest are split into `digests[parts[1]] = parts[0]` without checking `if parts[1] in digests`. Duplicate filenames silently overwrite earlier hashes.

### What Was NOT Found for Class 1 (Sweep Result)

- **Unified Table Self-Pinning:** No sibling lane maintains a unified tabular pin file (`instrument-pins.txt`) that simultaneously pins all runtime instruments, expectations, and its own self-digest within the same table. Sibling implementations either use external sidecar `.sha256` files (`kake-shokunin`), embed the digest in script source (`tameshi-shokunin`), or leave the pin table unpinned (`kagi-shokunin`, `kake-shokunin` round 42). Chousa's C1 S5 minus-self row exclusion (`pins_file_sha_minus_self()`) is unique across the fleet.
- **Pre-scoring Duplicate Exit-2 Refusal:** Outside chousa, no sibling driver checks the pin table for duplicates prior to scoring and terminates execution with an explicit setup exit code.

---

## 4. Target Class 2 Findings: Section-Scoped Search vs Document-Wide Search & Unpinned Counts

### Pointer Map: Target Class 2 Hits

| Lane | Path:Line | One-line Reading | Same Class as chousa C3 scoping? |
|---|---|---|---|
| `kotodama-shokunin` | `reports/round-100/predispatch.py:329` | `open(sk).read().count('check-table-support.py')` unpinned font-wide search on `SKILL.md` | **YES** — font-wide document search where `SCORECARD.md` was section-scoped |
| `kengaku-shokunin` | `plans/round77_c2_defect_discharge.py:213` | `tail = tail[: tail.index("...") + 4000]`: arbitrary 4000-char window without heading anchor | **YES** — arbitrary character slice lacking heading-anchored boundary contract |
| `mori-shokunin` | `tools/mori-claim-sweep.py:175–178` | `for line in text.splitlines(): for literal in literals: line.count(literal)` | **YES** — font-wide search for stale literals across all sections of carriers |
| `kagi-shokunin` | `corpus/current-claims.py:124` | `m = re.search(r"PASS \(([0-9]+) cases\)", ln)` in whole-stdout loop | **YES** — document-wide tally regex search without section isolation |
| `kagi-shokunin` | `plans/round-58-c1-check.py:869` | `m = re.search(r"--selftest` (\d+) cases", txt)` on entire lesson text | **YES** — font-wide regex extraction over full markdown lesson text |
| `lore-shokunin` | `corpus/tools/boundary_doc_check.py:332` | `matches = list(ANCHOR.finditer(doc_text))` across full document text | **YES** — font-wide regex search for code citations without section boundaries |
| `tsukuroi-shokunin` *(defense)* | `tools/check-registry-content.py:105` | `if match and len(match.group(1)) <= 2: break` in `operative_rows()` | **DEFENDED** — ATX heading depth `<= 2` boundary stops scope bleed |
| `mado-shokunin` *(defense)* | `quality/counters/c2-r86-clause-observations.py:321` | `if inside and stripped.startswith("### "): break` in `section_rows()` | **DEFENDED** — heading-anchored section extraction up to next `### ` |
| `chousa-shokunin` *(prior)* | `corpus/evidence/round91/skill-tally-r91.py:75` | `for ln in text.splitlines(): for mm in TALLY_RE.finditer(ln):` | **YES** — font-wide tally counting across full `SKILL.md` |
| `chousa-shokunin` *(current)* | `corpus/evidence/round92/skill-tally-r92.py:73` | `gates_start = text.find("## Gates")`, `nxt = text.find("\n## ", ...)` | **YES** — scoped to `## Gates`, but vulnerable to level-1 `# ` bleed |

### Detailed Readings: Class 2

1. **`kotodama-shokunin` `reports/round-100/predispatch.py:320–332`:**
   In leg `O5` (capability registration):
   ```python
       sc = os.path.join(root, 'SCORECARD.md')
       sk = os.path.join(root, 'SKILL.md')
       if os.path.isfile(sc) and os.path.isfile(sk):
           in_cap, rows = False, 0
           for l in open(sc, encoding='utf-8', errors='replace'):
               if l.startswith('## '):
                   in_cap = l.startswith('## Capabilities')
               elif in_cap and l.lstrip().startswith('|') and 'check-table-support.py' in l:
                   rows += 1
           skn = open(sk, encoding='utf-8', errors='replace').read().count('check-table-support.py')
           ok = rows >= 1 and skn >= 1
   ```
   Notice the sharp contrast in contract enforcement: `SCORECARD.md` is strictly section-scoped (`in_cap = l.startswith('## Capabilities')`), but `SKILL.md` is searched font-wide via `read().count('check-table-support.py')`. Any mention of `check-table-support.py` anywhere in `SKILL.md` (e.g., in a historical lesson quotation, an archived gate row, or an HTML comment) satisfies `skn >= 1`. This is the exact defect pattern of chousa's r91 `skill-tally-r91.py`.

2. **`kengaku-shokunin` `plans/round77_c2_defect_discharge.py:208–217`:**
   In `leg_v2()`:
   ```python
       skill = visible(reader.get(SKILL))
       if "round76-c1-surface-resolver" not in skill:
           return "pending", "round-76 SKILL rows absent"
       tail = skill[skill.index("round76-c1-surface-resolver"):]
       tail = tail[: tail.index("round76-c2-defect-discharge") + 4000] if "round76-c2-defect-discharge" in tail else tail[:4000]
       need = ["cases=12 red=11", "9/9", "cases=14 red=13", "12/12"]
       missing = [n for n in need if n not in tail]
   ```
   Instead of anchoring to section headers (e.g. `## Gate registry` or `### Round-76`), the code uses substring slicing followed by an arbitrary window of `+ 4000` characters. This creates an unprincipled boundary contract where edits elsewhere in the file or changes in row length can arbitrarily push target tallies outside or pull extraneous tallies inside the 4000-character window.

3. **`mori-shokunin` `tools/mori-claim-sweep.py:175–178`:**
   ```python
       for number, line in enumerate(text.splitlines(), 1):
           for literal in literals:
               for _ in range(line.count(literal)):
                   mismatches.append(('stale', carrier, number, repr(literal)))
   ```
   In `sweep()`, stale literals are searched document-wide across all lines of carriers (`SCORECARD.md`, `SHONEN.md`). If a historical section (such as an append-only round log or an archived audit note) legitimately quotes an older literal for historical documentation, the counter fails font-wide.

4. **Sibling Defenses Against Scope Defects:**
   - **`tsukuroi-shokunin` `tools/check-registry-content.py:101–108`:** In `operative_rows()`, the section extraction identifies the start line of `## Gate and probe registry — round<N>`, and scans forward until encountering an ATX heading with depth `<= 2`:
     ```python
     for index in range(start + 1, len(lines)):
         match = ATX_HEADING.match(lines[index])
         if match and len(match.group(1)) <= 2:
             end = index
             break
     ```
     This cleanly prevents scope bleeds if a level-1 `# ` heading or another `## ` heading follows.
   - **`mado-shokunin` `quality/counters/c2-r86-clause-observations.py:314–323`:** `section_rows()` isolates from `stripped == section` up to the next `### ` heading, preventing runbook row extraction from bleeding into subsequent sections.

### What Was NOT Found for Class 2 (Sweep Result)

- **Pinned Historical Multiset Verification:** Across all 20 sibling repositories, no sibling counter pins the exact multiset of historical non-current tallies. Siblings either count document-wide without distinguishing current vs historical, or ignore non-current lines entirely. Chousa's C3 design — combining section scoping to `## Gates` with an exact dictionary equality check on the historical multiset (`EXPECTED_OTHERS = {("161", "0"): 1, ("256", "0"): 1}`) — is unique across the fleet.

---

## 5. Connector Synthesis: Proposed Move

### 5.1 Evidence

1. **Class 1 (Operability):** Chousa round 92 successfully hardens `control-driver-r92.py` against duplicate pins (`SETUP PIN_DUPLICATE`) and introduces unified minus-self self-pinning (`pins_file_sha_minus_self`). Sibling scanning reveals that `tameshi-shokunin` independently implements minus-self digest calculation on script bytes (`measure-v92.py:51`) and enforces single-line occurrence (`measure-v95.py:109`), grounded in the same `sha256sum(1)` source. However, as noted by peer `R92ReviewerC1` (finding F4), `read_pins` raises `SystemExit(f"SETUP PIN_DUPLICATE path={path}")`, which Python translates to exit code 1 instead of exit 2 as promised in `claims.md` clause 6 ("a repeated pin path is `SETUP PIN_DUPLICATE` exit 2").
2. **Class 2 (Freshness):** Chousa round 92 scopes tally and case-range searches to `## Gates` using `nxt = text.find("\n## ", gates_start + 1)`. As demonstrated by peer `R92ReviewerC3` (attack A1), this literal string search bleeds across the entire document to EOF if the subsequent heading is renamed to level-1 `# ` or has leading whitespace, inadvertently swallowing historical tallies (such as the 215 tally) without a boundary diagnostic. Sibling scanning reveals that `tsukuroi-shokunin` (`check-registry-content.py:105`) defends against this exact bleed by terminating section scans on any ATX heading with depth `<= 2` (`re.match(r"^(#{1,2})\s")`).

### 5.2 Affected Axes

- **C1 (Operability):** Alignment of setup exit codes for duplicate pin detection with clause 6 and fleet-wide setup refusal conventions.
- **C3 (Freshness):** Prevention of heading-level scope bleed from `## Gates` into historical sections, ensuring that the 215 tail tally remains unbound by design rather than contingent on fragile literal string matching.

### 5.3 Proposed Move

**Implement an ATX-heading boundary extractor and align setup exit codes:**
1. **For C1:** Update `read_pins()` to explicitly exit 2 on duplicate pin detection (e.g. `sys.stderr.write(f"SETUP PIN_DUPLICATE path={path}\n"); sys.exit(2)`), reconciling code behaviour with `claims.md` clause 6 without modifying verification semantics.
2. **For C3:** Replace the literal string search `text.find("\n## ", ...)` in `skill-tally-r92.py` with an ATX heading regex that terminates on any column-0 heading of depth `<= 2` (`re.search(r"\n#{1,2}\s", ...)`). If the slice reaches EOF without encountering an expected terminal heading or if unexpected non-table content is encountered, emit an explicit `SCOPE_BLEED` setup diagnostic rather than misattributing the failure to `LEG_FAIL OTHERS`.

### 5.4 Risks & Second-Order Effects

- **Runtime Surface:** No additional dependencies or external processes; pure standard library (`sys`, `re`).
- **Contract Surface:** Resolves the F4 contradiction identified by `R92ReviewerC1` where the spec claimed exit 2 but code returned exit 1. Strengthens C3's claim that historical tallies outside `## Gates` are unbound by design.
- **Substrate Surface:** Read-only against `SKILL.md` and `instrument-pins.txt`; does not alter the committed bytes of either file.
- **Verification Surface:** Zero negative impact on existing passing baseline receipts; baseline C1 `verify` and C3 `skill-tally-r92.py` will continue to print PASS with identical tallies.

### 5.5 Verification Plan

1. Verify `read_pins()` on a duplicate pin row fixture: confirm exit code is 2 and stdout/stderr contains `SETUP PIN_DUPLICATE`.
2. Verify `skill-tally-r92.py` against a fixture where `## Round26` is replaced by `# Round26`: confirm the parser terminates the `## Gates` section cleanly at the `# ` boundary instead of bleeding to EOF and inflating `TALLY_ROWS` to 9.

---

## 6. Receipts Summary Table

All verification probes were executed on committed repository bytes and recorded in `.ufo/waves/round-92/w1/R92ConnectorSiblings/`:

| Receipt File | Target Lane & Script | Command Executed | Exit Code | Key Observed Output Line |
|---|---|---|---|---|
| `tameshi_self_pin_probe.txt` | `tameshi-shokunin` `measure-v92.py:51` | `python3 -c '<tameshi_self_pin>'` | 0 | `MATCH=True` (`STORED_SHA == ACTUAL_SHA`) |
| `kake_last_wins_probe.txt` | `kake-shokunin` `c42_count.py:396` | `python3 -c '<kake_last_wins>'` | 0 | `HAS_LAST_WINS_DICT=True`, `HAS_DUP_CHECK=False` |
| `kagi_last_wins_probe.txt` | `kagi-shokunin` `plans/round-58-c1-check.py:278` | `python3 -c '<kagi_last_wins>'` | 0 | `HAS_LAST_WINS_DICT=True`, `HAS_DUP_CHECK=False` |
| `kaidoku_last_wins_probe.txt` | `kaidoku-shokunin` `probe.py:87` | `python3 -c '<kaidoku_last_wins>'` | 0 | `EXPLICIT_LAST_WINS_COMMENT=True` |
| `tsukuroi_last_wins_probe.txt` | `tsukuroi-shokunin` `count-mount-rows-r81.py:102` | `python3 -c '<tsukuroi_last_wins>'` | 0 | `HAS_LAST_WINS_DIGESTS=True` |
| `kotodama_unscoped_skill_probe.txt` | `kotodama-shokunin` `predispatch.py:329` | `python3 -c '<kotodama_unscoped>'` | 0 | `HAS_FONT_WIDE_SKILL_COUNT=True` |
| `kengaku_byte_window_probe.txt` | `kengaku-shokunin` `round77_c2_defect_discharge.py:213` | `python3 -c '<kengaku_byte_window>'` | 0 | `HAS_ARBITRARY_BYTE_WINDOW=True` |
| `mori_unscoped_literal_probe.txt` | `mori-shokunin` `mori-claim-sweep.py:175` | `python3 -c '<mori_unscoped_literal>'` | 0 | `HAS_DOC_WIDE_LITERAL_COUNT=True` |
| `chousa_minus_self_probe.txt` | `chousa-shokunin` `instrument-pins.txt` | `python3 -c '<chousa_minus_self>'` | 0 | `MATCH=True` (`STORED_SELF_PIN == COMPUTED_MINUS_SELF`) |
| `chousa_gates_scoping_probe.txt` | `chousa-shokunin` `skill-tally-r92.py:73` | `python3 -c '<chousa_gates_scoping>'` | 0 | `SCOPED_TO_GATES=True` |

---

VERDICT: R92ConnectorSiblings C1 held — Sibling scan confirmed chousa's C1 minus-self pin table is uniquely unified across the fleet, while validating the need to align PIN_DUPLICATE exit code.
VERDICT: R92ConnectorSiblings C2 held — C2 located-quote and registry token joins are distinct from sibling table schemas.
VERDICT: R92ConnectorSiblings C3 held — Sibling scan confirmed chousa's C3 multiset pinning is unique, while exposing the hazard of literal string boundary slicing.
