# R57W1ConnSiblings — Sibling-Overlap Scan & UFO-FSD Connector (Round 57 Wave 1)

Seat: R57W1ConnSiblings (connector). Claim base: `6656f077`. Round 57 axes: freshness, depth, calibration.
Target: Sibling-overlap scan across all 20 sibling lanes for:
(a) Chinese drug-evaluation regulatory standards,
(b) normative-reference/citation-chain binding of standards,
(c) capture re-fetch/freshness pinning.
Deliverable: overlap verdicts (none / report-don't-absorb / contested) grounded in PROVINCE/SKILL headers; one bounded proposal for the C3 entry's Province section.
Tooling: zero tools installed or upgraded; standard host Python 3.12 / coreutils.
Scratch dir: `/fast/scratch/hyaku/chousa-r57/R57W1ConnSiblings` (purged on completion).

## 1. Evidence: Sibling-Overlap Scan across 20 Lanes

Scanned all 20 sibling lane repos under `/home/vgpnk/Projects/shokunin/*-shokunin/` (`audio`, `game-dev-2d`, `game-dev-3d`, `kagi`, `kaidoku`, `kake`, `kama`, `kasegi`, `kengaku`, `kotoba`, `kotodama`, `kumitate`, `lore`, `mado`, `mori`, `revenger`, `souji`, `tabi`, `tameshi`, `tsukuroi`).

### (a) Chinese Drug-Evaluation Regulatory Standards
- **Evidence:** Zero sibling lanes claim clinical, pharmaceutical, or drug evaluation regulatory standards in `PROVINCE.md:3` or `SKILL.md`. Sibling domains are strictly bounded: kasegi (bounties), kake (web properties), mori (host observability), kengaku (eval), kotoba (prompts), kumitate (orchestration), kama (model serving), kagi (vault), tabi (browser/CDP), souji (hygiene), kaidoku/revenger (reverse engineering), tsukuroi (OS repair), tameshi (fixture craft), mado (compositor), kotodama (conlangs), lore (world bible), audio (game audio), game-dev-2d/3d (games).
- **chousa grounding:** `chousa-shokunin/PROVINCE.md:3-8` owns deep-research method only; `PROVINCE.md:17` commands "Out of province → report, never absorb." Prior knowledge entries ground this distinction: `corpus/knowledge/grey-literature-and-chinese-search-record-r40.md:33` ("drug-safety evaluation practice itself ... is adjacent ground this entry reports and does not hold") and `grey-literature-field-china-r42.md:35` ("what a drug clinical comprehensive evaluation must assess ... are adjacent ground this entry reports and does not hold").
- **Verdict:** `none` across siblings; chousa posture is `report-don't-absorb`.

### (b) Normative-Reference / Citation-Chain Binding of Standards
- **Evidence:** `chousa-shokunin/PROVINCE.md:5-6` explicitly and exclusively owns "source hierarchy (primary / secondary / aggregator / unsourced); citation chaining and hop resolution; claim-vs-source verification". Sibling lanes explicitly route research method to chousa:
  - `kumitate-shokunin/PROVINCE.md:29`: "Research method → chousa."
  - `kengaku-shokunin/PROVINCE.md:137`: "| chousa | research method — ... question → source-hierarchy → citation-chain → claim-vs-source method stays chousa's ... this lane holds neither method nor duplicates it |"; lines 262, 307, 403, 454, 515: "capture and citation method stay chousa's".
  - `kotodama-shokunin/PROVINCE.md:19`: refuses "general source-research method (chousa)".
  - `lore-shokunin/PROVINCE.md:27`: "chousa — research method, not lore canon: chousa-shokunin/SKILL.md ... lore consumes its evidence".
  Sibling citation instruments (`kagi-shokunin/SKILL.md:242` `claim-ledger.sh`, `kake-shokunin/SKILL.md:1199` `citation_lint.py`, `kaidoku-shokunin/SKILL.md:672` `citation-drift-probe.py`, `kama-shokunin/SKILL.md:654` `citation-provenance.py`, `tsukuroi-shokunin/SKILL.md:1857` `check-section-citations.py`) only lint internal markdown/repo commit hashes, never external literature citation chaining.
- **Verdict:** `none` (chousa sole fleet owner; uncontested).

### (c) Capture Re-Fetch / Freshness Pinning
- **Evidence:** Freshness and capture verification are domain-scoped per lane; no sibling holds fleet-wide capture custody:
  - `kake-shokunin/PROVINCE.md:14,17`, `SKILL.md:212,579`: owns `scripts/freshness-sweep.mjs` for web properties / Pages deploys.
  - `tabi-shokunin/PROVINCE.md:5-13`: owns dynamic browser CDP evidence capture and `check-release-pins.mjs`.
  - `mori-shokunin/PROVINCE.md:3-10`: owns watchdog liveness and wave settlement freshness.
  - `tsukuroi-shokunin/PROVINCE.md:5-7`: owns OS package and initramfs boot freshness (`boot-writers` gate).
  - `kama-shokunin/PROVINCE.md:14`: owns endpoint drift and baseURL history.
  - `kagi-shokunin/SKILL.md:48,177`: owns secret vault drift pins.
  - `tameshi-shokunin/PROVINCE.md:14-17`: owns reusable verification craft; refuses product domains ("every lane's gate remains its own").
  - `kotoba-shokunin/verifiers/`: runs `--fetch` checking live vendor doc text for prompt/skill features.
  Historical consensus (`chousa-shokunin/.ufo/waves/round-25/build/ConnectorMetaSiblings.md:14`): "These are domain-scoped owners, not a fleet-wide owner of knowledge-entry freshness. Report the domain-scoped checks; do not absorb another lane's freshness gate into chousa."
  chousa owns "this lane's own corpus and gates" (`chousa-shokunin/PROVINCE.md:8`), which includes its pinned span captures (`corpus/captures/<key>.raw/.txt`) and re-fetch verification (`tools/capture-fetch.py`, `refetch.tsv`) executed under egress approval tables (`corpus/evidence/round57/egress-approval.md`, `claims.md:11-15`, `PROVINCE.md:7,13-14`).
- **Verdict:** `none` (no fleet-wide overlap or contest; domain-scoped per lane).

## 2. Affected Axes
- **calibration (improved):** Rigorously bounds chousa's deep-research method from adjacent regulatory content and prevents cross-lane scope absorption or false drift claims.
- **depth (improved):** Provides the authoritative, scan-grounded Province formulation for the C3 entry `normative-reference-chain-china-r57.md`.
- **freshness (unharmed):** Preserves all frozen R57-C2/C3 counters, targets, and recipes without modification.

## 3. Proposed Move: Synthesized C3 Entry `#### Province` Section
The draft entry in `.ufo/waves/round-57/w1/R57W1ScribeEntry.md:104-106` only addresses drug-evaluation subject matter. We propose synthesizing the scan verdicts into the entry's `#### Province` block, citing `R57W1ConnSiblings`:

```markdown
#### Province

- **Research method vs domain content (scan: `R57W1ConnSiblings`).** Sibling-overlap scan across all 20 fleet lanes confirms:
  1. Chinese drug-evaluation regulatory standards: zero sibling ownership (`none`); adjacent external ground that chousa reports and does not hold (`report-don't-absorb`, `chousa-shokunin/PROVINCE.md:17`).
  2. Normative-reference and citation-chain binding of standards: zero sibling overlap (`none`); chousa is the sole owner of citation chaining and hop resolution (`PROVINCE.md:5-6`), explicitly routed from kumitate (:29), kengaku (:137), kotodama (:19), and lore (:27).
  3. Capture re-fetch and freshness pinning: zero fleet-wide overlap (`none`); freshness ownership is domain-scoped per lane (kake web properties, tabi CDP sessions, mori watchdog logs, tsukuroi OS boot, kama endpoints), while chousa owns its own research corpus and digest-checked capture store (`PROVINCE.md:8`) under approved egress.
```

## 4. Risks & Second-Order Verification
- **Second-order contract check (`c3-count.py`):** `c3-count.py:85,248` enforces that any `\bS\d{3,}\b` token in the entry must be `S127` or a bound row. The proposed text contains zero `S###` tokens (verified by regex test `re.findall(r'\bS\d{3,}\b', text) == []`), preventing counter failure.
- **Safety & Mutation:** Zero mutation to frozen files (`claims.md`, `c2-count.py`, `c3-count.py`). Scratch directory `/fast/scratch/hyaku/chousa-r57/R57W1ConnSiblings` was cleaned before completion.

VERDICT: Sibling-overlap scan on (a) Chinese drug evaluation standards (verdict: none / report-don't-absorb), (b) normative-reference binding (verdict: none / chousa-owned), and (c) capture re-fetch/freshness pinning (verdict: none / domain-scoped) completed; synthesized C3 Province proposal survives.
