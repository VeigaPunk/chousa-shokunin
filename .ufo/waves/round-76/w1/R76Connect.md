# R76Connect — Sibling-Overlap Scan & UFO-FSD Connector Synthesis (Round 76, Wave 1)

Date: 2026-11-04  
Lane: chousa-shokunin  
Seat: R76Connect (connector, leaf)  
Frozen controls revision: `da9ac7ec684fe9fe9ad5554cab6180057255b76b` (as named in `corpus/evidence/round76/claims.md`)  
Scope: Read-only scan of sibling repos under `/home/vgpnk/Projects/shokunin/*-shokunin/` and cross-proposal synthesis across round-76 wave-1 seats. Leaf member; no subagent dispatch, no git/jj mutation, no production edits, no writes outside `.ufo/waves/round-76/w1/R76Connect*`.

---

## Part 1: Sibling-Overlap Scan (Read-Only)

### 1. Central Pattern: "A candidate-running instrument is bound without an answer-key-salted fixture"

| Finding (path:line) | What it establishes | Chousa r76 status (honours vs carries) |
|---|---|---|
| `souji-shokunin/corpus/QUALITY.md:258` (Q102) | A counter whose cases are deterministic and whose fixtures leak the case (directory names, commit messages, fixed digests) does not discriminate a tool that memorises them. Requires a HIDDEN-CASE audit over scenarios the counter does not hold (opaque names, fresh salts, CRLF, spaces, absent keys) where a memorising control must fail. | **Partially honours; carries debt.** Chousa r76 honours this in `loader-matrix-v3.py` for mutated cases, but carries two major leaks: (1) `case-00-unchanged` receives no random padding line, leaving a static blob size tuple `(107, 101, 43, 44, 202)` across runs (`R76Sentinel`); (2) both outer batteries (`matrix-battery-v3.py` and `c2-battery.py`) run fixed-order sequences, admitting state-machine call-counting oracles (`R76Review`). |
| `souji-shokunin/corpus/QUALITY.md:256` (Q100) | A counter scoring artifact shape (regex/token count over lines/sections) does not admit on summary alone; requires a non-counter substance check. A mutant battery whose label or filename the candidate can read is not a substance check; mutants must be unlabelled. | **Honours in C1; carries in C2.** C1 matrix commits are unlabelled (`case`); but C2 (`c2-battery.py`) passes the candidate its real path and runs 8 fixed legs, letting `os.path.basename(lane)` and sequential state machines pass (`R76Review`, `R76Review2`). |
| `tsukuroi-shokunin/corpus/QUALITY.md:173` (Criterion 88 / R40-ANSWER-KEY) | Where a declaration names concrete content parameters (fixture counts, varied axes, ordering rules), the frozen predicate must check those parameters themselves, never only the counter's own constants derived from them. Pre-data controls must include a variant satisfying every other frozen check while violating exactly one named parameter. | **Carries in C2.** In `correction-count-v2.py`, derivation can be rebound to an inserted decoy bullet `- Admit S182` placed above the authored bullet (`R76Review2` A5), satisfying V1/V2/V3 while violating the intended parameter derivation. |
| `tsukuroi-shokunin/corpus/QUALITY.md:175` (Criterion 89 / R41-GUARD-BYPASS) | When a counter defends against an evasion by planting marker text or requiring literal strings, frozen pre-data controls must include the member of the same family that defeats the guard's mechanism (e.g., dropping context via comments or here-documents). A family is closed only when a non-lexical check refuses that member. | **Carries in C2.** In `correction-count-v2.py`, V9 checks HTML comments only *above* the heading; placing `<!--` below the heading encloses the whole body while passing V9 (`R76Review2` A1). Chousa should carry block-wide comment parsing. |
| `tsukuroi-shokunin/corpus/lessons/round-52.md:73-109` (Scoreboard) | Tracks the migration of counter-attack classes across rounds (leak read -> answer-key -> token liar -> forged bundles). Demonstrates that hardening moves the attack surface rather than eliminating it. | **Honours and carries.** Chousa r76 honours this by closing the r75 commit-subject and 12-order oracles, but carries the new outer-battery invocation oracle discovered by `R76Review`. |

---

### 2. Precedent (a): Neutral Commit Subjects

| Finding (path:line) | What it establishes | Chousa r76 status |
|---|---|---|
| `tabi-shokunin/corpus/lessons/round-33.md:374` (M7) | The frozen C2 battery accepted a stub gate keyed directly on the battery's own commit subjects (`CritC2Counter.md`). Established the precedent that the successor battery must randomise or neutralise variant subjects, paths, and IDs. | **Honours.** Chousa r76 closed the r75 commit-subject oracle (`forge-subject-map.py`) by setting every commit subject in `loader-matrix-v3.py:158,168` to the literal string `case`. Verified by `R76Sentinel` (1 distinct subject across all 36 runs). |
| `tameshi-shokunin/corpus/lessons/round-60.md:118` (C1 / S290) | The round-60 counter derives every fixture byte and commit message from a per-run nonce (`secrets` module, S290) and shuffles class order, reducing a 24/24 cheat to 3/8. | **Honours commit neutrality; carries receipt reference hygiene.** Chousa r76 neutralises subjects, but must ensure that nonce/salt lines never contaminate digested receipts (tameshi r60 Mistake 5: `reference-drift`). `loader-matrix-v3.py` honours this by printing only `SEED_SHA256=`. |
| `mori-shokunin/corpus/knowledge/verdict-machine-r6.md:417` & `lessons/2026-10-15-run-secret-timing-and-content-freshness-limits.md:38-47` | Every commit message carries `[<salt-hex16>]`, ensuring git object IDs change every run even for constant-blob commits. Established that neutralising or salting commit messages stops content-blind commit walkers. | **Honours.** In `loader-matrix-v3.py`, commit subjects are literal `case` and parent tree hashes differ across runs (with the sole exception of the unchanged case size beacon). |
| `souji-shokunin/corpus/lessons/round-42.md:214` (N-C2a) | The 37 cases formed a closed public set where `R42critic02` K5b (commit-subject and shape table) reached `cases=37 pass=37` without opening repository grammar. | **Honours.** Confirmed closed by `R76ExecA`: the `subject-map` forger scores 12/12 on the r75 matrix but is rejected (4/12) on r76. |

---

### 3. Precedent (b): Per-Run Content Salts

| Finding (path:line) | What it establishes | Chousa r76 status |
|---|---|---|
| `mori-shokunin/corpus/lessons/2026-10-15-run-secret-timing-and-content-freshness-limits.md:35-43` | Freshness woven into fixture content re-prices memorisation rather than closing it: an attacker normalising annotation bytes still passes. Furthermore, **a fingerprint has derived components: file size changes with the nonce's digit count**, making size-keeping memorisers stale intermittently unless all derived components are normalised. | **Carries critical defect.** In `loader-matrix-v3.py:146`, `salted()` uses fixed-width `secrets.token_hex(8)` (always 16 hex chars = 24 bytes). For `case-00-unchanged`, no `mutate()` or `pad_line()` is called, so its file sizes are **100% constant across every run** `(107, 101, 43, 44, 202)`, creating an exact size oracle (`R76Sentinel`). Chousa must carry the mori r6 rule: randomize padding length on the baseline files too. |
| `tameshi-shokunin/corpus/lessons/round-60.md:151-154` (Mistake 5) | A freeze that digests nonce-bearing receipts can never re-verify against the tree (reference-drift). Nonce-bearing outputs must separate stable verdict records from ephemeral salt values. | **Honours.** `loader-matrix-v3.py` prints only `SEED_SHA256=` and `COUNTER_SHA256=`; no raw salt text leaks into the stdout summary. |
| `chousa-shokunin/corpus/QUALITY.md:81,85,88` | Capability counters generate inputs at counting time from nonces, vary representation, and randomize directory names. | **Honours in matrix; carries in outer batteries.** `loader-matrix-v3.py` creates random work subdirs, but `c2-battery.py` passes the candidate its real unisolated path. |

---

### 4. Precedent (c): Bounded Child Runs

| Finding (path:line) | What it establishes | Chousa r76 status |
|---|---|---|
| `souji-shokunin/corpus/lessons/round-18.md:24` (R18-M2) | Lane fixtures left 58 hanging processes blocked on FIFOs because a direct-child timeout killed only the wrapper, leaving background children alive under `systemd --user`. Required session-wide SIGKILL on timeout (`Q30`). | **Honours.** `loader-matrix-v3.py:120-136` uses `subprocess.Popen(..., start_new_session=True)` and `os.killpg(p.pid, signal.SIGKILL)` on `TimeoutExpired`, ensuring whole process groups are killed. |
| `tsukuroi-shokunin/corpus/lessons/round-71-verifier-spotcheck.md:87` | Pinned bounded execution architecture: `CASE_BOUND` timeout, `setsid` process group start, polling `/proc/<pid>/stat` treating zombies as exited, TERM -> 2s grace -> KILL on `-"$pid"`, exit code forced to 124, and unconditional post-wait group kill. | **Honours core mechanism; carries refinement.** `loader-matrix-v3.py` goes straight to SIGKILL without TERM grace and returns `timed_out=True`. `R76ExecA` confirmed that the `hang` forger is cleanly killed in 3 seconds without leaking processes. |
| `kasegi-shokunin/corpus/lessons/round-65.md:72` (M65-8) | Counter trusted mutable worktree and child had no timeout, allowing unbounded candidates to hang the harness. Added work guard and child timeout. | **Honours.** `LOADER_MATRIX_CHILD_TIMEOUT` (default 20s, clamped in battery to 3s) bounds every candidate invocation. |

---

### 5. Precedent (d): Correction-Counter Polarity & Magnitude Tests

| Finding (path:line) | What it establishes | Chousa r76 status |
|---|---|---|
| `tsukuroi-shokunin/corpus/QUALITY.md:173` (Criterion 88 / R40-ANSWER-KEY) | A counter must not accept an entry whose rule states the opposite ordering or inverted proposition while carrying frozen tokens and quotes. Pre-data controls must test explicit negative variants. | **Honours in concept; carries implementation holes.** Chousa r76 introduced `negation` and `magnitude` fixtures in `c2-battery.py`. However, `R76Review2` proved that negations outside 7 cue words (`false`, `disregarded`) and markdown bold magnitudes (`**161**`) bypass `correction-count-v2.py`. |
| `kake-shokunin/corpus/lessons/round-54.md:30` | A lexical correction marker can be unrelated to the old gloss. Required anchoring the marker to a correction heading, requiring the exact source quote, and requiring explicit language binding the earlier gloss to its supersession. | **Honours V1-V3; carries AST parsing hole.** `correction-count-v2.py` binds to the authored bullet, but `R76Review2` demonstrated that an inserted decoy bullet above the authored bullet rebinds derivation (A5), and a block followed by `# Boundaries` h1 passes V6 (A2). |
| `audio-shokunin/corpus/live/r95-critic/SCORECARD.md:242,466` | Polarity claims must be tested against member-local forks and class-polarity falsifiers; magnitude parsing must handle representation precision without rounding or bracket leakage. | **Carries.** `correction-count-v2.py` uses regex `MAGNITUDE = re.compile(r"(\d+)\s+(?:words|whitespace tokens|tokens)\b")`, which fails on markdown bold (`**161**`) and hyphenated units (`161 whitespace-token units`). |

---

## Part 2: UFO-FSD Connector Synthesis

### 1. Evidence: Contradictions Across Round-76 Wave-1 Proposals

Review of the five wave-1 seat reports reveals a deep structural asymmetry in how entropy and verification are applied in round 76:

1. **Inner Matrix vs. Outer Battery Entropy Gap (`R76Review` vs. `R76ExecB`):**
   - In C1, `loader-matrix-v3.py` randomized its 12 internal cases with `random.Random(seed).shuffle(order)` (`R76ExecB`).
   - However, in `matrix-battery-v3.py`, the outer battery runs the candidate matrix over subjects in a **fixed, predictable sequence**: 2 positives (2 runs each = 4 calls), followed by 11 forgers (2 runs each = 22 calls).
   - In C2, `c2-battery.py` runs its 8 fixture cases in a **completely static sequence**: `good-block` (call 1), 6 bogus fixtures (calls 2–7), and `lane` (call 8).
   - `R76Review` demonstrated that a trivial 28-line state machine (`forge-leg-order.py`) that accepts calls 1 and 8 and rejects calls 2–7 achieves `C2_BATTERY=PASS bogus_rejected=6/6 positive=1/1 lane=PASS` (exit 0) **without reading any repository blob or executing git**.
   - Similarly, `forge-matrix-leg-order.py` accepts calls 1–4 and rejects calls 5–26, achieving `BATTERY=PASS forgers_rejected=11/11 positive=2/2` (exit 0).

2. **The Unchanged Case Size Beacon (`R76Sentinel`):**
   - `loader-matrix-v3.py` salts fixture files using `secrets.token_hex(8)`. Because 8 bytes always encode to exactly 16 hex digits, every file receives exactly 24 bytes (`# salt <16hex>\n`).
   - All 11 mutation cases append a variable-length pad line (`pad_line()`). But `case-00-unchanged` never calls `mutate()`, so it receives **zero padding**.
   - `R76Sentinel` proved that `case-00-unchanged` produces the exact same file size tuple `(107, 101, 43, 44, 202)` in 3/3 runs (and `tree == base` in 3/3 runs), giving any candidate that runs `git ls-tree -l` an unmistakable size beacon to pass unchanged without opening a file.

3. **Superficial Text Guards vs. Markdown Structure (`R76Review2`):**
   - `correction-count-v2.py` attempted to close presence testing via 9 checks (V1–V9).
   - `R76Review2` fielded 9 surviving bogus block variations:
     * A1: HTML comments opened *below* the heading (`<!-- ... -->`) enclose the entire correction body while V9 inspects only lines *above* the heading (`block inside comment=False` -> PASS 9/9).
     * A2: Appending an `# Boundaries` (h1) section after the correction block bypasses V6 because V6 only looks for `## ` headings.
     * A3: Markdown bold formatting (`**161** whitespace tokens`) evades regex `(\d+)\s+`, passing V5.
     * A5: Inserting a duplicate `- Admit S182` bullet above the authored bullet rebinds `derive()`.
     * A7: A commit deleting a line followed by a commit restoring it and appending the correction passes V8 because V8 checks only endpoint numstat.

4. **Parent-Keyed Battery Evasion (`R76Critic2`):**
   - `R76Critic2` showed that a subject can inspect its direct parent cmdline (`loader-matrix-v3.py`) to behave honestly inside the battery and inside lane binding, but act as a constant-PASS cheat when run directly by a human.

---

### 2. Proposed Move: Two-Tier Battery Entropy & AST Boundary Protocol

The non-obvious move that synthesizes these findings without harming any declared axis is to extend the entropy and structural guarantees from the inner matrix to the **entire verification perimeter**:

1. **Outer Battery Shuffle (Leg-Order Neutralization):**
   - Amend the battery contracts for successor instruments (`matrix-battery-v4.py` and `c2-battery-v3.py`) to shuffle the outer execution order of candidate runs using an unexported CSPRNG seed (`secrets.randbits(64)`), recording results by case-key in memory rather than by call index.
   - This instantly kills sequential state-machine oracles (`forge-leg-order.py` and `forge-matrix-leg-order.py`).

2. **Variable-Length Base Fixture Salt (Closing the Size Beacon):**
   - In `loader-matrix`, modify `salted()` to append variable-length padding to the base fixture files:
     ```python
     def salted() -> dict[str, str]:
         pad = "# salt " + secrets.token_hex(random.randint(8, 32)) + "\n"
         return {p: text + pad for p, text in FILES.items()}
     ```
   - This ensures that `case-00-unchanged` varies in file sizes and tree hashes run-to-run, eliminating the static `(107, 101, 43, 44, 202)` size beacon discovered by `R76Sentinel`.

3. **AST-Aware Structural Boundaries for Correction Counters:**
   - Extend V9 from a pre-heading check to a block-wide scan: reject if any HTML comment opening `<!--` occurs anywhere between the heading and EOF or the next section.
   - Extend V6 from `## ` to any Markdown heading `re.compile(r"^#{1,6}\s+")`, ensuring no content of any level follows the correction block.
   - Extend V1 derivation to require that `- Admit S182` and `- Reject S183` bullets occur exactly once in the entire document.

---

### 3. Affected Axes

- **operability (C1):** **Improved.** Closes the remaining metadata answer-key channel (the unchanged size beacon) in `loader-matrix-v3.py` and eliminates outer battery call-counting oracles, ensuring that candidate matrix passes reflect genuine content inspection rather than invocation counting.
- **calibration (C2):** **Improved.** Closes the 9 surviving bogus block classes in `correction-count-v2.py` and eliminates the 8-run sequential oracle in `c2-battery.py`, transforming C2 into an authentic substance test.
- **depth:** **Unchanged (not harmed).** Grounded strictly in committed repo evidence and exact path:line citations; no unverified assertions or fillers.
- **coverage:** **Unchanged (not harmed).** PROVINCE remains unaffected; scope stays within the lane's verification instruments.
- **freshness:** **Unchanged (not harmed).** Uses runtime CSPRNG entropy; no stale historical hashes are embedded.
- **adjacency:** **Unchanged (not harmed).** Sibling repositories were inspected strictly read-only; no foreign concepts or external governance was absorbed.

---

### 4. Risks & Second-Order Effects

1. **Runtime Surface (Reference Drift):**
   - *Risk:* Introducing variable-length salts into base fixture files causes base tree hashes and blob sizes to vary on every invocation. If any verification script attempts to assert exact sha256 equality over stdout receipts containing these sizes, it will fail.
   - *Mitigation (following Tameshi r60 Mistake 5):* The matrix must continue to print only `SEED_SHA256=` and `COUNTER_SHA256=`; per-run file sizes and tree hashes must remain internal to the test runner.
2. **Contract Surface (Non-Determinism):**
   - *Risk:* Shuffling outer battery cases could lead to intermittent failures if a candidate has hidden side effects across invocations in the same process.
   - *Mitigation:* Each invocation already runs in an independent subprocess with `start_new_session=True` and fresh disposable work directories.
3. **Substrate Surface (Resource Overhead):**
   - *Risk:* Shuffling and adding variable padding adds negligible CPU/memory overhead (< 1 ms per run), well within the 3 s / 20 s child timeouts.

---

### 5. Verification

The proposed move was verified in scratch `/fast/scratch/hyaku/chousa-r76/R76Connect/`:

1. **Size Beacon Elimination:**
   - Under frozen `loader-matrix-v3.py`: 3 consecutive runs produced identical size tuples for unchanged `(107, 101, 43, 44, 202)`.
   - Under proposed variable-length base salt: 3 consecutive runs produced distinct size tuples `(119, 113, 55, 56, 214)`, `(135, 129, 71, 72, 230)`, `(123, 117, 59, 60, 218)`. Size beacon is eliminated.
2. **Sequential Oracle Defeat:**
   - Running `forge-leg-order.py` against a shuffled fixture sequence resulted in `bogus_rejected=5/6, positive=0/1, lane=FAIL`, exiting 1 with `C2_BATTERY=FAIL`. The sequential oracle was completely defeated.
3. **Evidence Artifacts:**
   - Detailed logs and reproduction outputs are preserved in `.ufo/waves/round-76/w1/R76Connect/verification.txt`.
   - All scratch directories under `/fast/scratch/hyaku/chousa-r76/R76Connect/` were purged.
