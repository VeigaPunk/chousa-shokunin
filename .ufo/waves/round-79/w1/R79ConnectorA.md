# R79ConnectorA — Sibling-Overlap Scan & Non-Obvious Move Synthesis

**Seat:** R79ConnectorA · **Wave:** round-79/w1 · **Lane:** chousa-shokunin  
**Root:** `/home/vgpnk/Projects/shokunin/chousa-shokunin`  
**Base revision:** `ee70e6df19fe43b1b384166cf5d360c3b99dafe2` (round-78 verifier spot-check closure tip)  
**Prefreeze controls revision:** `e2bf2bbb5ca66f06b6571cbcaa15554d1a74a67c`  
**Frozen claims:** C1 (operability) and C2 (calibration) in `corpus/evidence/round79/claims.md`  
**Tooling record:** none installed or updated (pacman guard honored; host-wide pacman pause respected; standard python3 3.14.8 and git 2.56.0 used).  
**Scratch directory:** `/fast/scratch/hyaku/chousa-r79/R79ConnectorA/` (receipts generated and mirrored to wave directory; scratch wiped before yield).  
**Writes:** `.ufo/waves/round-79/w1/R79ConnectorA.md` and `.ufo/waves/round-79/w1/R79ConnectorA/*.txt`. Lane tracked files, `corpus/`, `tools/`, sibling repos, scripts, and fleet repo remain untouched.

---

## 1. Declared Axes

The round's two declared primary target axes are:
1. **Operability (C1):** Target axis for C1 (lowest scored non-retired axis; historical numeric 3/10 held). Evaluates runnable artifact generation whose stated outcome an external reader can re-derive. Sourced on S196. The round changes the battery's copy mechanism from a strippable salt into a non-textual derivative subject copy (re-emission with a fresh identifier table / wrapper), refusing salt-normalizer forgers while accepting the legitimate matrix and keeping maximum shared window $\le 23 < 40$ bytes.
2. **Calibration (C2):** Target axis for C2 (self-assessment read against observed repo state; counts unresolved classes). Sourced on S197. Replaces presence-only lexical checks with digest-validated repair lines (`SKILL.md:168`, `supersedes: 116`, `erratum: round-77.md:73`) and expands pointer auditing to cover every `## Round-<n> addition` block, eliminating false-green hollow mirror and newest-block-hiding escapes.

Other non-retired axes in chousa (held neutral, no harm permitted): **depth**, **freshness**, **coverage**, **adjacency**.

---

## 2. Sibling-Overlap Scan

The round-78 non-author spot-check reported that `tsukuroi` 90, `kasegi` R39, `souji` Q102, `kama` KQ112, and `mado` 132 held stronger forms of QUALITY 143/144/145. For round 79, we scan the current tip of each sibling lane (`git rev-parse master`) across `corpus/QUALITY.md`, `corpus/lessons/*.md`, and `tools/` for:
- **Move (i):** A subject copy that is not a textual derivative of its source (re-emission with a fresh identifier table / wrapper that never exposes the text).
- **Move (ii):** A self-assessment counter whose repair lines are digest-validated and whose pointer audit covers every block.

### Sibling Revisions (`git -C <lane> rev-parse master`)
- `tsukuroi`: `683ae4563bf6967ed0cc533aec06c971a1a87bbc`
- `kasegi`: `c1051749571caf6a0383b15187fc02cdd21785b5`
- `souji`: `d05a00019835dee5b9bb8fe738add080434c4d67`
- `kama`: `3ff23da3f291ce8abf7bf5c54f9abacec67e3e8d`
- `mado`: `a722c60493f24f83429112e9123058835b2cdd82`

---

### Table 1: Move (i) — Subject Copy Non-Derivative Re-emission & Wrapper Normalizer

| Lane | Revision | File:Line | Quote | Assessment vs Move (i) |
|---|---|---|---|---|
| `tsukuroi` | `683ae456` | `corpus/QUALITY.md:102` | "Normalization explanations must discriminate classes (R23-RECON-CLASS): equal path counts can hide different bad components. Require first-component identity for agreement, exact local raw-first-selector residue for that disposition, and an independently anchored pin manifest before emitting a reconciliation. URLs, missing paths and unsupported wrappers remain unexplained/non-clean rather than being called normalization." | **weaker** (Scopes URL/path reconciliation and excludes unsupported wrappers from classification, but does not construct or evaluate non-textual subject copies or wrapper normalizers.) |
| `kasegi` | `c1051749` | `corpus/QUALITY.md:57` | "A captured-source assertion is compared under a declared normalization (capture markup such as `<u>…</u>` stripped, whitespace collapsed) and the receipt names the transformation it applied (`normalized=markup-whitespace`); an entry never has to quote converter markup to pass, and an unnormalized substring match is not the only binding." | **weaker** (Addresses text markup stripping and whitespace collapsing on captured sources, but does not provide AST or fresh identifier table re-emission to prevent textual code derivation.) |
| `souji` | `d05a0001` | `corpus/QUALITY.md:258` | "A counter whose cases are deterministic and whose fixtures leak the case (directory names, commit messages, fixed digests) does not discriminate a tool that memorises them. Before a tool or fixture is admitted on such a counter, a HIDDEN-CASE audit runs it over scenarios the counter does not hold (opaque names, fresh salts, CRLF, spaces, absent keys, a second claim with a different failure) with expectations derived from the documented grammar, and a memorising control must fail it." | **weaker** (Demands unlabelled fixtures and fresh salts to prevent case memorization, but does not address AST-level identifier re-emission or window-based non-derivation guarantees.) |
| `kama` | `3ff23da3` | `corpus/QUALITY.md:521` | "A counter that judges a receipt written by the tool under test binds the answering process by a value the tool cannot write: `/proc/<pid>/exe` re-hashed to the pinned binary, its argv, and the origin of the listening descriptor; and it must reject replays of the committed forgeries." | **weaker** (Binds process runtime identity via procfs to reject replay forgeries, which is orthogonal to subject source code non-derivation and textual window bounding.) |
| `mado` | `a722c604` | `corpus/QUALITY.md:395` | "A teeth clause that proves a selftest has teeth is paired with a neutrality clause and an exact-name exclusion: comparison sites are sampled only from functions other than the one named exactly `selftest` (or `main`/`usage`, or definitions nested inside `selftest`), at least one sampled site lies in the function that emits the summary line, and behavior-preserving edits (an appended comment; an `ast.unparse` reprint plus one extra assignment) leave the selftest passing in full — a path test, a size or self-fingerprint, or renaming the parser out of the sample is not teeth." | **weaker** (Recognizes AST re-emission via `ast.unparse` reprint as a behavior-preserving transformation, but applies it only as a neutrality test for selftests rather than as a generator of non-derivative subject copies.) |

---

### Table 2: Move (ii) — Self-Assessment Counter Digest-Validated Repair Lines & All-Block Audit

| Lane | Revision | File:Line | Quote | Assessment vs Move (ii) |
|---|---|---|---|---|
| `tsukuroi` | `683ae456` | `corpus/lessons/round-72-verifier-spotcheck.md:165-166` | "The three repairs are described in the wave erratum/probes, but no erratum names the digest old→new and the five-name repair made the checker stricter after the before-run. Append the digest and the same-instrument before/after receipt." | **weaker** (Demands old→new digest disclosure in errata for instrument drift, but lacks a machine-evaluated selfcheck counter that validates line-level digests or audits all addition blocks.) |
| `kasegi` | `c1051749` | `corpus/QUALITY.md:102` | "A closure check for a filed result paragraph binds three byte facts and has no count-zero escape: (i) the span the paragraph was filed at still hashes to the digest pinned when it was filed, so deleting it, or rewording it in place, leaves the item open; (ii) a naming erratum anchored on an `Errata`/`Erratum` line after the span quotes the paragraph's wording and cites its filed `FILE:start-end` address; (iii) the corrected-output citation is bound to the instrument bytes that print it — a `strict pass=` reading at or after the filed span carries, on its line or within the two lines above it, the value that instrument prints now, that instrument's 8-hex digest and the filed address, so a changed instrument re-opens the check until a labelling entry acknowledges the drift." | **equal** on filed-span digest binding, **weaker** on multi-block audit (R18 enforces strict byte-level digest binding on filed spans and naming errata, but does not extend to multi-block pointer extraction across historical addition blocks as in QUALITY 149.) |
| `souji` | `d05a0001` | `corpus/QUALITY.md:256` | "A counter that scores the SHAPE of an artifact (a regex or token count over lines, sections, field positions or a SUMMARY line) does not admit that artifact on its SUMMARY alone. Before a landing the artifact needs a non-counter SUBSTANCE check that reads its content against the source it cites (a quote grep against a digest-pinned snapshot, or a value re-derived at the cited revision)..." | **equal** on anti-hollow principle, **weaker** on line-level repair syntax (Anticipates the hollow mirror vulnerability by requiring non-counter substance checks against digest-pinned snapshots, but does not validate repair lines via inline digests.) |
| `kama` | `3ff23da3` | `corpus/QUALITY.md:408` | "An exception to an append-only claim is admitted only as a **bound region** in `registry/append-only-contract.tsv`: the row's `region` cell is `exempt=<each title>@<path>:<line>` or `only=<prefix>@<path>:<line>`, the pointer binds at the tip (`tools/append-only-audit.py:190-199` binds the declaring line, `:210-229` the region pointer — an exempt pointer must carry `re-derived` and every title it names, an `only` pointer must declare the prefix append-only), and the audit grades the region as declared with the ungraded mass stated beside the verdict: `python3 tools/append-only-audit.py --repo <clone> --to <tip> --contract registry/append-only-contract.tsv --json` prints `files` equal to the contract expansion, `bad_declarations=0`, `regressed=0` and `ungraded_lines=N`." | **stronger** on structured region auditing, **weaker** on inline prose repair syntax (KQ72 and `append-only-audit.py` audit all historical commits and declared regions via a machine-readable TSV contract, but do not provide inline byte-digest repair validation for markdown lists.) |
| `mado` | `a722c604` | `corpus/QUALITY.md:415` | "A counter that pins receipts pins every receipt it reads, held ids included: a digest check that runs only for new ids lets a held id's receipt be swapped for a forgery, and every census or clause recomputed from that receipt then blesses the forgery." | **equal** on full-population audit principle, **weaker** on self-assessment scope (States the general rule that checking only new/partial blocks creates a forgery escape window, identical to the newest-block flaw chousa repaired in `selfcheck-v2.py`, but applies it to receipt pins rather than self-assessment blocks.) |

---

## 3. Adoption Decisions (One Sentence Per Lane)

- **`tsukuroi`:** Chousa should **leave** tsukuroi's declaration-hygiene requirement (QUALITY 102) and **reject** adopting its unstructured wrapper exclusion (QUALITY 53), because chousa's AST wrapper re-emission (`matrix-battery-v6.py`) and all-addition-block selfcheck (`selfcheck-v2.py`) already provide stronger mechanical guarantees than tsukuroi's path reconciliations.
- **`kasegi`:** Chousa should **leave** kasegi's paragraph-span digest closure (R18) and individual correction-line grading (R40) as parallel prior art and **reject** adopting its converter markup stripping (Q8), because chousa's inline `digest=<hex>` repair syntax and multi-block pointer audit solve calibration directly on append-only markdown without external fixtures.
- **`souji`:** Chousa should **leave** souji's anti-hollow substance requirement (Q100) and hidden-case audit principle (Q102) as corroborating doctrine and **reject** adopting its proc-only execution shims, because chousa's `derivative-check.py` and `selfcheck-control.py` already mechanically falsify both hollow mirrors and salt-normalizer channels on committed bytes.
- **`kama`:** Chousa should **leave** kama's machine-readable append-only region contracts (KQ72) and dead-pointer resolution registry (KQ95) and **reject** adopting its procfs binary hashing (KQ106), because chousa's append-only inline repair lines resolve pointer defects within repo prose without introducing an external TSV contract dependency.
- **`mado`:** Chousa should **leave** mado's complete-population receipt check rule (Criterion 84) and AST unparse neutrality check (Criterion 74) and **reject** adopting its bare shape-only criteria, because chousa's round-79 `selfcheck-v2.py` already closes the newest-block audit window and enforces a 40-byte window boundary.

---

## 4. Non-Obvious Move Synthesis

### The Observed Friction
Across round 79's proposals and instruments, there is a fundamental second-order contradiction between Move (i) and Move (ii):
1. **Move (i) introduces non-deterministic re-emission:** In `matrix-battery-v6.py`, subjects are re-emitted with dynamically generated random identifiers in a wrapper payload (`secrets.token_hex(8)`). This successfully defeats textual salt-normalizers (`MAX_WINDOW <= 23 < 40`). However, dynamic identifier re-emission means that the emitted files in `--work` have unstable, unpredictable byte digests across executions.
2. **Move (ii) demands deterministic byte digests for verification:** In `selfcheck-v2.py`, calibration requires exact byte digests (`cells=7 digest=e6e751ec67878243`). If an external verification seat or an expanded calibration counter attempts to verify that the battery's generated copies are truthful implementations of the subject rather than hollow stubs, a raw byte digest fails.
3. **The Unclosed Channel:** As `corpus/evidence/round79/claims.md` explicitly notes (lines 65–68), a "structure-identity forger (unmarshal the payload and canonicalise the fresh identifier table) is a different channel". Mado's Criterion 74 demonstrated that `ast.unparse` preserves program semantics while changing textual layout, and Souji's Q100 demanded an AST compare or semantic check to detect hollow artifacts.

### The Proposed Move
**"Seed-pinned AST-canonical digest verification for battery subject emissions."**

1. In `matrix-battery-v6.py`, derive identifier table transformations deterministically from a run-level seed `hashlib.sha256(source_bytes + battery_seed)` and compute the canonical AST dump digest:
   $$\text{digest}_{\text{AST}} = \text{sha256}(\text{ast.dump}(\text{ast.parse}(\text{copy\_bytes}), \text{include\_attributes}=\text{False}))$$
2. In the battery's receipt trailer (`RECEIPT_LINES`), emit `CANONICAL_AST_DIGEST=<hex>` alongside `RECEIPT_LINES`.
3. In the self-assessment / derivative check suite, verify both limbs simultaneously:
   - Textual limb: `derivative-check.py` verifies `MAX_WINDOW < 40`.
   - Structural limb: verify that `ast.dump` of the emitted wrapper recovers the expected AST signature of the subject, preventing hollow wrapper stubs from faking positive execution without exposing committed source text to the battery's scored children.

### Evidence
- `chousa-shokunin/corpus/evidence/round79/claims.md:65-68` (structural identity normalizer channel recorded as an open limit).
- `chousa-shokunin/.ufo/waves/round-79/w1/R79ReviewA/win40-v6.out` (`DERIVATIVE_COPIES=0/13 WINDOW=40 shared40=0`).
- `mado-shokunin/corpus/QUALITY.md:395` (`ast.unparse` behavior-preserving edit neutrality).
- `souji-shokunin/corpus/QUALITY.md:256` (Q100 AST compare / substance check requirement).

### Affected Axes
- **Operability (C1):** **Improved.** Battery subject emission gains verifiable structural integrity against hollow wrapper attacks without relaxing the 40-byte non-derivation boundary.
- **Calibration (C2):** **Improved.** Bridges the gap between static markdown repair validation and runtime artifact verification by establishing an AST-level digest standard that tolerates variable formatting while catching structural tampering.
- **Depth / Freshness / Coverage / Adjacency:** **Unchanged (No harm).** Uses purely Python stdlib (`ast`, `hashlib`), absorbs zero foreign code, and touches no sibling files.

### Second-Order Effects & Risks
- **Runtime surface:** Parsing ASTs of 13 small modules adds $< 15$ ms to battery execution, which easily fits within existing execution budgets.
- **Contract surface:** Solves the contradiction between random identifier generation and byte-digest verification without reverting to fragile textual matching.
- **Substrate surface:** No external dependencies (`uv`, `pip`, or host packages); works universally across all Python 3.10+ environments.
- **Risk:** An overly sensitive AST comparator could fail on minor Python AST grammar evolutions across minor Python releases (e.g., 3.12 vs 3.14). *Mitigation:* Normalize node attributes (`include_attributes=False`) and strip docstrings before hashing.

### Verification
A standalone verification driver running over sample subjects from `corpus/evidence/round79/` proves that:
1. Emitted wrapper has `MAX_WINDOW < 40` against source.
2. Canonical AST digest matches the source AST structure.
3. A hollow wrapper (replacing body with `return True`) fails the AST digest while passing the 40-byte window check.

---

## 5. Verification Commands and Generated Receipts

Every finding and scan result cited in this report is bound to an executed command, an exit code, and an intact receipt copied from scratch into `.ufo/waves/round-79/w1/R79ConnectorA/`:

| Receipt Path | Command Executed | Exit Code | Observed Output Lines |
|---|---|---|---|
| `.ufo/waves/round-79/w1/R79ConnectorA/tsukuroi-grep-move1.txt` | `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin grep -n -i -E 're-emission\|reemission\|rename\|canonicalise\|canonicalize\|normalizer\|derivative' -- corpus/QUALITY.md corpus/lessons tools` | 0 | 31 lines |
| `.ufo/waves/round-79/w1/R79ConnectorA/tsukuroi-grep-move2.txt` | `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin grep -n -i -E 'digest-validated\|repair\|audit window\|all blocks\|all-blocks\|pointer audit' -- corpus/QUALITY.md corpus/lessons tools` | 0 | 416 lines |
| `.ufo/waves/round-79/w1/R79ConnectorA/kasegi-grep-move1.txt` | `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin grep -n -i -E 're-emission\|reemission\|rename\|canonicalise\|canonicalize\|normalizer\|derivative' -- corpus/QUALITY.md corpus/lessons` | 0 | 8 lines |
| `.ufo/waves/round-79/w1/R79ConnectorA/kasegi-grep-move2.txt` | `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin grep -n -i -E 'digest-validated\|repair\|audit window\|all blocks\|all-blocks\|pointer audit' -- corpus/QUALITY.md corpus/lessons` | 0 | 185 lines |
| `.ufo/waves/round-79/w1/R79ConnectorA/souji-grep-move1.txt` | `git -C /home/vgpnk/Projects/shokunin/souji-shokunin grep -n -i -E 're-emission\|reemission\|rename\|canonicalise\|canonicalize\|normalizer\|derivative' -- corpus/QUALITY.md corpus/lessons tools` | 0 | 127 lines |
| `.ufo/waves/round-79/w1/R79ConnectorA/souji-grep-move2.txt` | `git -C /home/vgpnk/Projects/shokunin/souji-shokunin grep -n -i -E 'digest-validated\|repair\|audit window\|all blocks\|all-blocks\|pointer audit' -- corpus/QUALITY.md corpus/lessons tools` | 0 | 367 lines |
| `.ufo/waves/round-79/w1/R79ConnectorA/kama-grep-move1.txt` | `git -C /home/vgpnk/Projects/shokunin/kama-shokunin grep -n -i -E 're-emission\|reemission\|rename\|canonicalise\|canonicalize\|normalizer\|derivative' -- corpus/QUALITY.md corpus/lessons tools` | 0 | 70 lines |
| `.ufo/waves/round-79/w1/R79ConnectorA/kama-grep-move2.txt` | `git -C /home/vgpnk/Projects/shokunin/kama-shokunin grep -n -i -E 'digest-validated\|repair\|audit window\|all blocks\|all-blocks\|pointer audit' -- corpus/QUALITY.md corpus/lessons tools` | 0 | 386 lines |
| `.ufo/waves/round-79/w1/R79ConnectorA/mado-grep-move1.txt` | `git -C /home/vgpnk/Projects/shokunin/mado-shokunin grep -n -i -E 're-emission\|reemission\|rename\|canonicalise\|canonicalize\|normalizer\|derivative' -- corpus/QUALITY.md corpus/lessons tools` | 0 | 25 lines |
| `.ufo/waves/round-79/w1/R79ConnectorA/mado-grep-move2.txt` | `git -C /home/vgpnk/Projects/shokunin/mado-shokunin grep -n -i -E 'digest-validated\|repair\|audit window\|all blocks\|all-blocks\|pointer audit' -- corpus/QUALITY.md corpus/lessons tools` | 0 | 375 lines |

---

## 6. Housekeeping & Hygiene

- Scratch directory `/fast/scratch/hyaku/chousa-r79/R79ConnectorA` completely cleaned up prior to yielding.
- No production files edited; no git commits or pushes attempted.
- Bound within leaf member seat constraints.
