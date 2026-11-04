# R75Connect — Sibling-Overlap Scan & Synthesis (Chousa Round 75)

- **Seat:** `R75Connect` (leaf member, no subagents, no task tool, no lane/fleet git mutations).
- **Lane Root:** `/home/vgpnk/Projects/shokunin/chousa-shokunin`
- **Frozen Revision:** `43a7a0db52c8aabdf32735f58e09610e05200e79`
- **Tooling Directive Report:** No tools installed or upgraded; host pacman paused; existing python3 3.14.8 and git 2.56.0 used read-only.
- **Detailed Data Artifacts:** Saved to `.ufo/waves/round-75/w1/R75Connect/sibling-scan.json` and `.ufo/waves/round-75/w1/R75Connect/sibling-scan.md`.

---

## 1. Naming the Axes

1. **Chousa Round 75 Declared Axes:**
   - **C1 — Operability** (lowest scored non-retired axis, 3/10): The loader matrix binds only after a committed detection-forger battery passes it (QUALITY 126), and the successor matrix kills the r74 source-blind invocation-order oracle and diff-only oracle.
   - **C2 — Calibration** (sourced on S184): Correcting the r74 spot-check's routed defect append-only (located-quote token counts 18/13 superseded by derived 16/11 in lesson correction block).
2. **Lane Domain Scope:** Deep-research method (調査) — question framing, source hierarchy, citation chaining, claim-vs-source verification; no live target fetches without operator approval.
3. **Cross-Lane Evaluation Axes:** Discernment, quality, operability, coverage, calibration.

---

## 2. Sibling-Overlap Scan Results

Search across sibling lane repos (`/home/vgpnk/Projects/shokunin/*-shokunin/`) for the pattern:
> *"a candidate-running counter or matrix binds a claim without a committed prefreeze detection-forger battery"*

Target grep terms: `detection-forger`, `forger battery`, `order oracle`, `source-blind`.

### Summary Table of Hits

| Lane | Round | File:Line | One-Line Quote | Same Defect Class as C1? |
|---|---|---|---|---|
| **souji** | 59 | `corpus/QUALITY.md:316` | `Q120 \| Before declaring a successor claim, retain executed no-work and relevant forgery controls with exact input bytes/revisions, commands, instrument digest, independent expected rc/findings and observed outputs in a commit strictly preceding predicate freeze. A later replay never repairs the chronology of the rejected claim.` | **YES** (Identical procedural gate violation: missing prefreeze committed forgery battery prior to scoring) |
| **kama** | 28 | `corpus/lessons/round-28.md:34` | `Evidential: do-nothing 0, junk 0/30, label-keyed 12/41, source-blind 14/38, duplicate-field 0/26.` | **YES** (A candidate-scoring counter vulnerable to source-blind shortcut guessing without reading underlying source content) |
| **kumitate** | 48 | `corpus/lessons/round-48.md:9` | `kills one case, suppresses the FAIL line, prints 62/62 + VERDICT: PASS exit 0, read ROUTED_HELD 3/3 under F48. captured-by: the pre-data control wave (MutSummaryForge)... fix: A48 — per-case line corroboration...` | **YES** (A test runner accepting aggregate summary exit codes without independent case-by-case corroboration) |
| **kumitate** | 51 | `corpus/lessons/round-51.md:91-92` | `seat ExecForgerControl (wave 1, delivered late during wave 2 — 53 min, after two return-now nudges) built a zero-spawn forger with faithful receipt format (canonical digest, GNU sidecar, distinct nonces, ledger semantics) and read ATTEST_HELD held=9/9` | **YES** (Predictable/leaked harness challenge allowing a zero-execution stub to score full marks) |
| **kumitate** | 68 | `corpus/lessons/round-68.md:23` | `counter-forgery — C1 L4 reveals mutant names through fixture paths, allowing a pathname-dispatch stub to report HELD without ledger semantics. Captured by K68CriticForgeryC1; next freeze must hide the answer key and score an implementation-level falsifier.` | **YES** (Harness leaking case identity via fixture paths/arguments, allowing a stub to dispatch answers without verifying target content) |
| **tabi** | 33 | `corpus/QUALITY.md:571` | `90. A feasibility sentence — 'not reachable without …', 'the counter cannot judge …', 'the battery cannot catch …' — is written only after the cheapest forgery against that instrument has been run, and it names the attack and cites its control...` | **YES** (Requiring empirical execution of cheapest forgeries rather than prose assertions of unforgeability) |
| **kaidoku** | 48 | `corpus/QUALITY.md:147` | `Row 78: ...A battery's forgery must differ where it claims to... Before freezing, run the proposed instrument against one complete green candidate and each forgery, and inspect the exact field each clause reads.` | **YES** (Ensuring forgeries test the specific discriminating logic of the checker rather than failing on incidental differences) |
| **tsukuroi** | 38 | `corpus/lessons/round-38-verifier-spotcheck.md:76` | `\| Kill rule: pacman.log run-order oracle \| my own parser over /var/log/pacman.log: per transaction and phase, the running '<hook>' sequence must be increasing in the table's positions \| 60 transactions with hooks, 109 phases, 0 violations, 0 names absent from the table.` | **NO** (Related mechanism — order verification — but distinct domain: verifying chronological log ordering vs defeating test sequence guessing) |
| **tsukuroi** | 35 | `.ufo/waves/round-35/w1/K08FixtureKeyed.md:19` | `Lines are shuffled once, written with LF separators and a final LF, so there is no stable line-position or chronological-order oracle.` | **YES** (Technique: shuffling fixture order to kill position/chronological oracles) |
| **mori** | 18 | `.ufo/waves/round-18/falsify/MutDispatchLedger.md:96` | `2. Independent recursive key-order oracle — demonstrated survivor M2... There is no noncanonical nested insertion-order fixture checked against an independent canonical digest. The current suite does not protect sort_keys=True.` | **NO** (Related mechanism: deterministic fixture order masking candidate inability to enforce canonical ordering) |
| **kotoba** | 37 | `MANIFEST.json:4527` | `kotoba r37... REJECTED on C1 (depth): the source-blind harness re-derivation fails as declared — comparator exit 1, 23/28 headline (strict 17/28), 5 open rows...` | **NO** (Distinct class: intentional source-blind comparator used to measure router blindness boundaries vs false-green forge) |
| **mado** | 46 | `corpus/QUALITY.md:432-434` | `88. A counter that reads tree shape carries a committed forgery suite — revisions a reader rejects — and a tightening candidate is admitted only when the positive control passes every candidate and each undeclared admitted forgery fails the intended one...` | **NO** (Committed forgery suite for desktop tree shape readers) |

---

## 3. Prior Art & Province Boundaries

### Sibling Precedent Chousa Should Cite as Prior Art:
1. **Souji Q120:** The canonical fleet rule requiring that no-work and forgery controls be executed and committed *strictly preceding* predicate freeze. Directly addresses the procedural gap that blocked chousa r74 under QUALITY 126.
2. **Kumitate Q43, A48, and R68:**
   - **Q43:** "A freeze means frozen AND executed" — every declared do-nothing control must be executed before data.
   - **A48:** Per-case line corroboration (matching both rc and specific failed check IDs per case, as `loader-matrix-v2.py` implements via `expected_rc` and `expected_failed`).
   - **R68:** Masking test case identifiers from fixture paths/arguments to prevent parameter-based routing.
3. **Kama r28 `CtlSourceBlind`:** Empirical measurement of source-blind shortcut ceilings using explicit negative controls (`CtlSourceBlind`, `CtlA1Rescore`) before freezing candidate scoring.
4. **Tsukuroi r35 `K08FixtureKeyed`:** Shuffling test cases once to eliminate stable position or chronological order oracles.
5. **Tabi Q90 / Q112:** Mandatory empirical execution of cheapest forgeries against production entrypoints rather than relying on prose claims.
6. **Kaidoku Row 78:** Ensuring each forgery in a battery differs specifically in the clause it claims to test, avoiding incidental failures.

### Sibling Precedents That Must NOT Be Absorbed (PROVINCE Boundary):
1. **Souji (Workspace Hygiene):** Owns stale artifact sweeps, duplicate census receipts, and quarantine before delete. Chousa must NOT absorb file-sweeping or quarantine workflows into deep-research loader testing.
2. **Kumitate (Tooling & Orchestration):** Owns OMP session life-cycle, bubblewrap isolation, Rust runtime, and invocation attestation ledgers. Chousa must NOT absorb container orchestration or bubblewrap sandboxing as host isolation.
3. **Kama (Model Serving):** Owns local model endpoint health (`llama-server`, server-schema.cpp, GBNF grammars). Chousa must NOT absorb HTTP endpoint validation, request parameters, or sampling semantics.
4. **Tsukuroi (Host Repair):** Owns Pacman ALPM hooks, pacman.log parsing, btrfs error counters, and systemd services. Chousa must NOT absorb host package manager transaction logs or filesystem repair mechanics.
5. **Tabi (Web Interaction):** Owns browser automation, Playwright scripts, and CDP protocols. Chousa must NOT absorb web scrapers or browser drivers.
6. **Kaidoku (Binary Reverse Engineering):** Owns Ghidra/REA binary forensics and ELF patching.
7. **Kotoba (Prompt Craft):** Owns prompt templates and skill catalog taxonomies.
8. **Mori (Fleet Observability):** Owns host monitors, wave settlement tracking, and OOM event logging.

---

## 4. UFO-FSD Connector Synthesis & One Proposed Move

### Local Wave Evidence & Observed Contradiction
1. **R75ExecA:** Confirms that `loader-matrix-v2.py` passes `matrix-battery.py` (5/5 forgers rejected, 2/2 positive accepted) while r74 fails (2/5 rejected).
2. **R75ExecB:** Confirms all 12 cases in v2 matrix are derivable from the counter's contract; none are decided by diff alone.
3. **R75ExecC:** Demonstrates that content cases kill diff-only and naive-grep (variant B), while order randomisation kills the order oracle (variant A).
4. **R75Mutation (`battery-m2-no-shuffle.txt`):** Revealed a critical asymmetry:
   - When running `matrix-battery.py` against `m2-no-shuffle.py` (which removes `random.shuffle`), the battery **still exits 0 with `BATTERY=PASS forgers_rejected=5/5`**!
   - **Why?** The battery's `forge-order-oracle.py` is the *historical round-74* 9-case oracle. When faced with the 12-case `m2-no-shuffle.py` matrix, it only returns 9 responses, scoring 9/12. Because 9/12 < 12/12, the battery marks it "REJECTED".
   - **Contradiction:** The battery currently claims to prove that order randomisation is what kills the order oracle. In reality, on the committed battery, the order oracle is rejected on `m2-no-shuffle.py` due to **case-count starvation** (9 cases vs 12 cases), NOT due to order shuffling!

### Synthesis
Synthesizing **Kaidoku Row 78** ("a battery's forgery must differ where it claims to"), **Kumitate A48** (per-case expectation corroboration), and **Tabi Q112** (covering production call paths):

### The One Proposed Move: "Length-Matched Forger Battery Standard"
**Move:** In any candidate-running test matrix that expands its case count from $N$ to $N+k$ (here 9 to 12) to defeat diff-only oracles, the prefreeze detection-forger battery must include:
1. The historical $N$-case forger (verifying backward-compatibility rejection on expanded suites); AND
2. An explicitly **length-matched ($N+k$ case) sequential order-oracle** whose hardcoded sequence matches the unshuffled case order.

### Second-Order Effects
- **Runtime:** Adds negligible execution time (~0.2s for 2 runs of a lightweight Python script).
- **Contract:** Discloses the true causal boundary of the matrix: order shuffling is empirically tested against a full-length sequential oracle (which would achieve 12/12 on an unshuffled matrix but fails on a shuffled matrix), rather than relying on a truncated 9-case oracle that fails regardless of shuffling.
- **Verification:** Prevents false confidence where a matrix with a broken shuffle function could pass the battery.

### Affected Axes
- **Discernment (Primary, Improves):** Directly distinguishes whether an order oracle is defeated by random permutation or by case-count exhaustion.
- **Quality (Secondary, Improves):** Closes a latent testing gap in the prefreeze battery without altering the frozen predicate of the current round.
- **Operability (Held / Harms None):** Read-only finding for future round criteria; leaves round 75 frozen instruments intact.

### Verification
Run `matrix-battery.py` augmented with `forge-order-oracle-v2-12cases.py`:
1. Against `loader-matrix-v2.py` (shuffled): `order-oracle-12` scores <12/12 and is REJECTED.
2. Against `m2-no-shuffle.py` (unshuffled): `order-oracle-12` scores 12/12 and is ACCEPTED (`BATTERY=FAIL`), proving that the test battery discriminates between shuffled and unshuffled matrices.

---

## 5. Verification & Exact Commands Run

All commands executed from fleet root (`/home/vgpnk/Projects/shokunin`), read-only across all lane repos:

1. `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin rev-parse HEAD`
   - Exit: `0`
   - Output: `43a7a0db52c8aabdf32735f58e09610e05200e79` (frozen revision confirmed)
2. `grep` across `/home/vgpnk/Projects/shokunin/*-shokunin/corpus/QUALITY.md` with patterns `detection-forger`, `forger battery`, `order oracle`, `source-blind`
   - Exit: `0` (Hits in chousa, souji, tabi, kumitate, kama, kaidoku, mado, kasegi)
3. `grep` across `/home/vgpnk/Projects/shokunin/*-shokunin/corpus/lessons/*.md` with patterns `detection-forger`, `forger battery`, `order oracle`, `source-blind`
   - Exit: `0` (Hits in chousa, tsukuroi, kama, kumitate, kengaku)
4. `grep` across `/home/vgpnk/Projects/shokunin/.ufo/reports/**/*.md`
   - Exit: `0` (Hits in chousa r74, kama r28)
5. `write` `.ufo/waves/round-75/w1/R75Connect/sibling-scan.json`
   - Exit: `0` (11,813 bytes)
6. `write` `.ufo/waves/round-75/w1/R75Connect/sibling-scan.md`
   - Exit: `0` (14,934 bytes)
7. `write` `.ufo/waves/round-75/w1/R75Connect.md`
   - Exit: `0` (This report)
