# Sibling-Overlap Scan — R75Connect

## Scope & Method
Read-only scan of sibling lane repositories under `/home/vgpnk/Projects/shokunin/*-shokunin/` for the pattern:
> *"a candidate-running counter or matrix binds a claim without a committed prefreeze detection-forger battery"*

Searched terms across QUALITY criteria, lessons, verifier spot-checks, and wave reports:
- `detection-forger`
- `forger battery`
- `order oracle`
- `source-blind`

All searches respected leaf read-only boundaries: no lane mutations, no git/jj alterations, no subagents, and no host configuration changes.

---

## Detailed Hit Census

### 1. `tsukuroi` — Round 38 (Hook Order Verification) & Round 35 (Line Shuffling)
- **File:Line:** `tsukuroi-shokunin/corpus/lessons/round-38-verifier-spotcheck.md:76` (and `SCORECARD.md:2105`)
- **One-Line Quote:**
  > `| Kill rule: pacman.log run-order oracle | my own parser over /var/log/pacman.log: per transaction and phase, the running '<hook>' sequence must be increasing in the table's positions | 60 transactions with hooks, 109 phases, 0 violations, 0 names absent from the table.`
- **Related Hit:** `tsukuroi-shokunin/.ufo/waves/round-35/w1/K08FixtureKeyed.md:19`
  > `Lines are shuffled once, written with LF separators and a final LF, so there is no stable line-position or chronological-order oracle.`
- **Defect Class vs C1:** **Partially Related Mechanism, Distinct Defect Class.** Tsukuroi used an order oracle to verify that pacman log entries strictly reflected chronological hook execution order against its reference table. In chousa C1, the order oracle is an adversarial forge that cheats the test matrix by guessing the static execution sequence of test cases without reading repository content.
- **Prior Art to Cite:** Tsukuroi's technique of shuffling event/fixture lines (`K08FixtureKeyed`) to prevent chronological or position-based oracles from succeeding.
- **PROVINCE Boundary (Do NOT Absorb):** Tsukuroi owns host operability and repair (Pacman, ALPM hooks, pacman.log parsing, btrfs error counters, systemd). Chousa must NOT absorb pacman hook transaction logs, system package management, or host filesystem error structures.

---

### 2. `kama` — Round 28 (Source-Blind Hard-Limit Controls)
- **File:Line:** `kama-shokunin/corpus/lessons/round-28.md:34` (and `round-28-verifier-spotcheck.md:185`, `CtlSourceBlind/REPORT.md:11`)
- **One-Line Quote:**
  > `Evidential: do-nothing 0, junk 0/30, label-keyed 12/41, source-blind 14/38, duplicate-field 0/26.`
- **Related Hit:** `kama-shokunin/.ufo/waves/round-28/controls/CtlSourceBlind/REPORT.md:11`
  > `The behavior-bearing mutation was to add one registry row per selected field... while fabricating the outcome from a fixed heuristic. The expected frozen detector must keep this shortcut below counted >= 18. This fixed mutant was killed at that threshold: 14 < 18.`
- **Defect Class vs C1:** **SAME Defect Class.** In kama r28, a counter scoring registry rows against server behaviors was vulnerable to "source-blind" shortcuts (guessing hardcoded HTTP 400 bounds like 0..INT32_MAX without executing the server or reading semantics). Kama constructed explicit pre-freeze controls (`CtlSourceBlind`) to measure the ceiling of source-blind forgeries (scored 14 under A0, 9 under A1, staying below the 18 threshold). This is the exact defect class as chousa's C1 where a counter/matrix can be satisfied by a source-blind generator that guesses answers without inspecting the actual underlying source content.
- **Prior Art to Cite:** Kama's methodology of pre-registering explicit pre-freeze source-blind forgery controls (`CtlSourceBlind`) with a bounded score ceiling to demonstrate that shortcut guessing cannot achieve the required threshold to pass.
- **PROVINCE Boundary (Do NOT Absorb):** Kama owns local model serving and endpoint health (`llama-server`, server-schema.cpp, GBNF grammars, request field validation). Chousa must NOT absorb HTTP endpoint verification, server parameters, or sampling semantics.

---

### 3. `kumitate` — Rounds 48, 51, 52, 68 (Summary Forgery, Zero-Spawn Forgers, Leaked Answer Keys)
- **File:Line:**
  - `kumitate-shokunin/corpus/lessons/round-48.md:9` (and `.ufo/waves/round-48/r48/MutSummaryForge.md:1`)
  - `kumitate-shokunin/corpus/lessons/round-51.md:91-92, 98-99`
  - `kumitate-shokunin/corpus/lessons/round-68.md:23`
  - `kumitate-shokunin/corpus/QUALITY.md:806-808` (Q43)
- **One-Line Quotes:**
  - Round 48: `kills one case, suppresses the FAIL line, prints 62/62 + VERDICT: PASS exit 0, read ROUTED_HELD 3/3 under F48. captured-by: the pre-data control wave (MutSummaryForge)... fix: A48 — per-case line corroboration...`
  - Round 51: `seat ExecForgerControl (wave 1, delivered late during wave 2 — 53 min, after two return-now nudges) built a zero-spawn forger with faithful receipt format (canonical digest, GNU sidecar, distinct nonces, ledger semantics) and read ATTEST_HELD held=9/9`
  - Round 51 (Q43): `Fix: at freeze time the L1 runs the counter at base and commits the receipt (base/attest-base-v3r6.txt, held=0/9); every freeze repair re-runs it; every declared do-nothing control is executed by a seat before data, not asserted. From round 51 on, a freeze means frozen AND executed.`
  - Round 68: `counter-forgery — C1 L4 reveals mutant names through fixture paths, allowing a pathname-dispatch stub to report HELD without ledger semantics. Captured by K68CriticForgeryC1; next freeze must hide the answer key and score an implementation-level falsifier.`
- **Defect Class vs C1:** **SAME Defect Class.** Kumitate repeatedly encountered forgers that passed without executing the underlying tool contract:
  - In round 48, `MutSummaryForge` defeated aggregate summary checks (equivalent to diff-only/summary-level checks).
  - In round 51, `ExecForgerControl` created a zero-spawn forger that read 9/9 because the probe's challenge was predictable/leaked (analogous to order oracle predicting outputs).
  - In round 68, `K68CriticForgeryC1` showed that leaking test case identities via pathname allowed a stub to achieve full marks without ledger semantics (exact parallel to chousa r74 matrix where case ordering / diff-only inspection leaked sufficient signal for a stub to score 9/9 without reading file contents).
- **Prior Art to Cite:**
  1. Kumitate Q43 freeze discipline ("a freeze means frozen AND executed; every declared do-nothing control is executed before data, not asserted").
  2. Kumitate r48 A48 per-case expected-line corroboration (checking both aggregate summary and per-case exit codes / failed check sets, exactly as `loader-matrix-v2.py` does with `expected_rc` and `expected_failed`).
  3. Kumitate r68 lesson on preventing answer-key leakage through test harness parameters.
- **PROVINCE Boundary (Do NOT Absorb):** Kumitate owns orchestration and tooling (OMP harness, bubblewrap isolation, Rust runtime, gate dispatch, attestation ledger). Chousa must NOT absorb container orchestration, bwrap namespace sandboxing as host isolation, or OMP session lifecycle machinery.

---

### 4. `souji` — Round 59 (Prefreeze Admission Prerequisites) & Round 40 (Oracle Forgeries)
- **File:Line:** `souji-shokunin/corpus/QUALITY.md:316` (Q120) and `:241` (Q93)
- **One-Line Quotes:**
  - Q120: `Q120 | Before declaring a successor claim, retain executed no-work and relevant forgery controls with exact input bytes/revisions, commands, instrument digest, independent expected rc/findings and observed outputs in a commit strictly preceding predicate freeze. A later replay never repairs the chronology of the rejected claim.`
  - Q93: `...commit the pair list and probe inputs before dispatch; run the frozen counter under the declared unprivileged runner; include a negative class/trigger control and a filename/row-name oracle-forgery variant that must fail`
- **Defect Class vs C1:** **EXACT SAME Procedural Defect Class.** Chousa round 74 was rejected under QUALITY 126 because prefreeze detection-forger controls were not committed prior to candidate scoring. Souji Q120 codifies the fleet rule that prefreeze controls must precede predicate freeze in commit history.
- **Prior Art to Cite:** Souji Q120 prefreeze control commitment rule, requiring exact inputs, commands, instrument digests, and expected vs observed outputs committed prior to freeze.
- **PROVINCE Boundary (Do NOT Absorb):** Souji owns workspace hygiene (stale artifacts, duplicate files, census quarantine). Chousa must NOT absorb file cleanup, quarantine, or workspace hygiene policies.

---

### 5. `tabi` — Rounds 32, 33, 62 (Empirical Forgery Batteries & Whitelist Rejection)
- **File:Line:** `tabi-shokunin/corpus/QUALITY.md:561-568` (Criteria 89, 90) and `112` (`:835-836`)
- **One-Line Quotes:**
  - Q90: `90. A feasibility sentence — 'not reachable without …', 'the counter cannot judge …', 'the battery cannot catch …' — is written only after the cheapest forgery against that instrument has been run, and it names the attack and cites its control...`
  - Q112: `112. The forgery-probe and mutant coverage rule: a counter that enforces a frozen kill rule carries (a) one selftest case per enumerated forgery probe named in the frozen rule, and (b) one kill per named mutant in the frozen mutant list; and its selftest drives the PRODUCTION call path...`
- **Defect Class vs C1:** **SAME Defect Class.** Prohibiting ungrounded prose claims of unforgeability and requiring empirical execution of cheapest forgeries against candidate-running instruments before declaring them robust.
- **Prior Art to Cite:** Tabi Q90/Q112 empirical forgery test standards, executing forgeries through production entrypoints.
- **PROVINCE Boundary (Do NOT Absorb):** Tabi owns browser and web-interaction craft (CDP, Playwright, browser automation). Chousa must NOT absorb browser protocols.

---

### 6. `kaidoku` — Round 48 (Clause-Specific Forgery Discrimination)
- **File:Line:** `kaidoku-shokunin/corpus/QUALITY.md:147-149` (Row 78)
- **One-Line Quote:**
  > `Row 78: ...A battery's forgery must differ where it claims to... Before freezing, run the proposed instrument against one complete green candidate and each forgery, and inspect the exact field each clause reads.`
- **Defect Class vs C1:** **SAME Defect Class.** Ensuring that a forger battery tests the actual discriminating logic of the checker rather than failing for extraneous or incidental reasons (e.g. case count starvation).
- **Prior Art to Cite:** Kaidoku Row 78 requiring that each forgery differ specifically where it claims to, and inspecting the exact fields each clause reads.
- **PROVINCE Boundary (Do NOT Absorb):** Kaidoku owns binary reverse engineering with REA on host (Ghidra, ELF decompilation). Chousa must NOT absorb binary forensics.

---

### 7. `mori` — Round 18 (Key-Order Oracle in Fixtures)
- **File:Line:** `mori-shokunin/.ufo/waves/round-18/falsify/MutDispatchLedger.md:96`
- **One-Line Quote:**
  > `2. Independent recursive key-order oracle — demonstrated survivor M2. The task object has only one key (:447), and fixture files are themselves serialized with sorted keys (:379-385). There is no noncanonical nested insertion-order fixture checked against an independent canonical digest. The current suite does not protect sort_keys=True.`
- **Defect Class vs C1:** **Related Mechanism, Distinct Defect Class.** Fixture sorting masking the lack of key-order verification, analogous to fixed test ordering masking invocation-order oracles.
- **Prior Art to Cite:** Mori M2 demonstration that deterministic ordering in fixtures masks candidate inability to enforce canonical ordering.
- **PROVINCE Boundary (Do NOT Absorb):** Mori owns fleet and host observability (森). Chousa must NOT absorb host telemetry or wave settlement tracking.

---

### 8. `mado` — Round 46 (Committed Forgery Suite)
- **File:Line:** `mado-shokunin/corpus/QUALITY.md:432-436` (Criterion 88)
- **One-Line Quote:**
  > `88. A counter that reads tree shape carries a committed forgery suite — revisions a reader rejects — and a tightening candidate is admitted only when the positive control passes every candidate and each undeclared admitted forgery fails the intended one...`
- **Defect Class vs C1:** **Related Defect Class.** Requiring a committed forgery suite where each forgery tests a specific rejection path.
- **Prior Art to Cite:** Mado criterion 88 on committed forgery suites verifying tightening candidates.
- **PROVINCE Boundary (Do NOT Absorb):** Mado owns desktop and compositor craft (Hyprland, waybar). Chousa must NOT absorb desktop compositor state.

---

### 9. `kotoba` — Round 37 (Source-Blind Comparator)
- **File:Line:** `MANIFEST.json:4527`
- **One-Line Quote:**
  > `kotoba r37... REJECTED on C1 (depth): the source-blind harness re-derivation fails as declared — comparator exit 1, 23/28 headline (strict 17/28), 5 open rows (3 catalogue UNLANDED = a real blindness boundary; 2 disagreements with raw-substrate evidence favoring the harness)...`
- **Defect Class vs C1:** **Distinct Defect Class.** Kotoba intentionally constructed a source-blind harness comparator to establish the empirical boundary of what could be inferred without router inspection, whereas chousa C1 addresses a surviving false-green forge.
- **Prior Art to Cite:** Kotoba r37/r38 discipline of strict comparators between independent implementations to isolate blindness boundaries.
- **PROVINCE Boundary (Do NOT Absorb):** Kotoba owns prompt and skill craft. Chousa must NOT absorb prompt routing or skill catalog schemas.

---

## Synthesis & Citation Guidance for Chousa

| Sibling Precedent | What Chousa Must Cite | What Must NOT Be Absorbed (Province Boundary) |
|---|---|---|
| **Souji Q120** | Prefreeze commitment of executed no-work and forgery controls preceding predicate freeze in Git history | Workspace hygiene, stale artifact sweeping, quarantine before delete |
| **Kumitate Q43, A48, R68** | Frozen-and-executed rule (Q43); per-case line corroboration comparing `expected_rc` and `expected_failed` sets (A48); masking answer keys from harness parameters (R68) | Tooling runtime, container/bubblewrap orchestration, process attestation ledgers |
| **Kama r28 CtlSourceBlind** | Pre-registering explicit source-blind controls to measure empirical shortcut score ceilings | HTTP server option schemas, GBNF grammars, sampling parameters |
| **Tsukuroi r35 K08** | Shuffling test case presentation order to eliminate stable position / invocation-order oracles | Pacman ALPM hooks, pacman.log parsing, btrfs error counters |
| **Tabi Q90, Q112** | Empirical cheapest-forgery execution across production call paths rather than prose assertions | Browser automation, CDP protocol, Playwright scripts |
| **Kaidoku Row 78** | Verifying that forgeries fail on the exact discriminating clauses under test | Binary reverse engineering, REA, Ghidra decompilation |
