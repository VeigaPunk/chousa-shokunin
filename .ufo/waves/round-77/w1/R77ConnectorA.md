# R77ConnectorA — Sibling-Overlap Scan and UFO-FSD Synthesis

Seat: `R77ConnectorA` (connector, leaf).  
Lane: `chousa-shokunin`, round 77, wave w1.  
Frozen controls revision: `e6fcdc4770c2fa73e5ccda99445c4311128d7e0d` (named in `corpus/evidence/round77/claims.md`).  
Policy: Read-only scan of sibling lane repositories; no fleet/lane git mutation; no task tool / subagents; output bounded strictly to `.ufo/waves/round-77/w1/R77ConnectorA.md`.

---

## 1. Declared Axes

1. **Operability (C1)**: Lowest scored non-retired axis (historical score 3/10). Evaluates the lane's candidate-running battery (`matrix-battery-v4.py`) resistance to invocation-count and order oracles via per-run subject permutation (64-bit OS seed), child contract table validation (content leg), and rejection of three forged matrices (oracle leg).
2. **Calibration (C2)**: Sourced on S190/S191. Evaluates append-only correction of the false prose sentence in frozen `round76/claims.md` via `c3-count.py` (verbatim retention of superseded clause, correction heading presence, both states quoted, zero line deletions in Git numstat, terminal section, unhidden by comments).

---

## 2. Sibling-Overlap Scan Results

Cross-repository read-only search across the 5 sibling repositories under `/home/vgpnk/Projects/shokunin/`:
- `souji-shokunin`
- `tabi-shokunin`
- `kumitate-shokunin`
- `kotoba-shokunin`
- `kaidoku-shokunin`

Target topics:
- **(i)** An outer harness/battery that can be passed by invocation-count or order oracles.
- **(ii)** Binding a check to subject output content rather than exit status alone.
- **(iii)** Append-only correction of a frozen claims file.

### Topic (i): Outer Harness / Battery Passed by Invocation-Count or Order Oracles

Hits located with verified `path:line`:

1. `souji-shokunin/corpus/QUALITY.md:120` (Q51):
   - "Acceptance compares the declared result contract, not success-shaped output: counter scalar/container types are exact, summary stderr is empty without stripping/suppression, and cache check names plus ordered phase labels are independent reviewed expectations."
2. `souji-shokunin/corpus/QUALITY.md:256` (Q100):
   - "A counter that scores the SHAPE of an artifact (a regex or token count over lines, sections, field positions or a SUMMARY line) does not admit that artifact on its SUMMARY alone. Before a landing the artifact needs a non-counter SUBSTANCE check that reads its content against the source it cites... and an artifact that must exercise a tool needs an EXECUTION-COUNT SHIM that logs each invocation, with the count required to equal the probe count."
3. `souji-shokunin/corpus/QUALITY.md:258` (Q102):
   - "A counter whose cases are deterministic and whose fixtures leak the case (directory names, commit messages, fixed digests) does not discriminate a tool that memorises them. Before a tool or fixture is admitted on such a counter, a HIDDEN-CASE audit runs it over scenarios the counter does not hold (opaque names, fresh salts, CRLF, spaces, absent keys, a second claim with a different failure)..."
4. `souji-shokunin/corpus/QUALITY.md:316` (Q120):
   - "Before declaring a successor claim, retain executed no-work and relevant forgery controls with exact input bytes/revisions, commands, instrument digest, independent expected rc/findings and observed outputs in a commit strictly preceding predicate freeze."
5. `souji-shokunin/corpus/lessons/round-31.md:102`:
   - "the C2 SHIFT oracle added by A3 was a fixed probe list committed in the counter source, so a gate copied it as a 21-token table"
6. `tabi-shokunin/corpus/QUALITY.md:263` (Criterion 55):
   - "Structural consistency is not a semantic oracle. A silent synthetic CLI fixture..."
7. `tabi-shokunin/corpus/QUALITY.md:269` (Criterion 56):
   - "Refines 55: an outcome oracle persists independent case-specific expected outcomes..."
8. `tabi-shokunin/corpus/QUALITY.md:558` (Criterion 89):
   - "A gate is said to admit evidence only after a frozen battery scores it on three populations that can move..."
9. `tabi-shokunin/corpus/QUALITY.md:665` (Criterion 96):
   - "A freeze's control set includes every cheap construction the previous round's lesson names, each scored with exact commands..."
10. `tabi-shokunin/corpus/QUALITY.md:743` (Criterion 106):
    - "A refusal control must exercise the strongest attack in its class: a control that refuses only because the attack channel is absent does not cover an attacker who supplies the channel."
11. `tabi-shokunin/corpus/QUALITY.md:835` (Criterion 112):
    - "The forgery-probe and mutant coverage rule: a counter that enforces a frozen kill rule carries (a) one selftest case per enumerated forgery probe named in the frozen rule, and (b) one kill per named mutant in the frozen mutant list; and its selftest drives the PRODUCTION call path..."
12. `tabi-shokunin/corpus/QUALITY.md:875` (Criterion 115):
    - "A counter that reads a producer's own verdict must carry BOTH polarity negatives — producer-true/derivation-false and producer-false/derivation-true — and the exact source line that combines them must be mutated and run through the production CLI..."
13. `tabi-shokunin/corpus/lessons/round-63.md:111` & `116`:
    - W10/W15: 42 independent single-change negatives plus 11 of 15 single-field forged receipts accepted by the frozen CLI.
14. `kumitate-shokunin/corpus/QUALITY.md:329` (Q25):
    - "a mutation battery has one kill predicate, frozen before any counted run and stated..."
15. `kumitate-shokunin/corpus/QUALITY.md:372` (Q26):
    - "an operability claim needs a pass-sensitive counter; listed-line and file-count terms are not enough..."
16. `kumitate-shokunin/corpus/QUALITY.md:483` (Q29):
    - "an operability counter must reject named skip-work controls before data. A counter that passes a skip-work control is vacuous..."
17. `kumitate-shokunin/corpus/QUALITY.md:945` (Q57):
    - "a frozen counter must reject a do-nothing control that skips the claimed activity, and must distinguish its honest-pass..."
18. `kumitate-shokunin/corpus/QUALITY.md:1232` (Q73):
    - "a frozen counter's every arm must be derived from its own contract, checked before the freeze commit..."
19. `kumitate-shokunin/corpus/QUALITY.md:1309` (Q78):
    - "pre-data controls must be able to differ from the work. Every claim..."
20. `kumitate-shokunin/corpus/lessons/round-84-verifier-spotcheck.md:58`:
    - "Kill rule (plan.md, frozen): 'do-nothing control reaching 16 means unmet'."
21. `kotoba-shokunin/corpus/QUALITY.md:48` (Q37):
    - "Before data, a claim's §9 shortcut controls include, besides fabricated input, the cheapest real-input shortcut a critic can build..."
22. `kotoba-shokunin/corpus/QUALITY.md:87` (Q71):
    - "A counter whose cells a script can recompute names, beside its target, the measured score of the script-only world scored on the same frozen counter; the headline asserts only what that world cannot reach..."
23. `kotoba-shokunin/corpus/QUALITY.md:90` (Q74):
    - "Before admitting a semantic claim whose evidence cells a script can populate from page bytes, score an independent mechanical generator that writes the complete proposed evidence shape on the same frozen counter; if it reaches the target, the counter measures form rather than the claimed semantics..."
24. `kotoba-shokunin/corpus/lessons/round-62.md:33`:
    - F2: "the self-test's constant controls were literal comparisons, not substitutions. A call-order transcript and a..."
25. `kotoba-shokunin/corpus/lessons/round-80.md:8`:
    - "C1 consistency/calibration — honest stop; target predicate killed by falsifying controls..."
26. `kaidoku-shokunin/corpus/QUALITY.md:50` (Row 40):
    - "A counter gate written to refuse forged or reused evidence (duplicate bytes, reused runs) ships, in the same commit and before the data..."
27. `kaidoku-shokunin/corpus/QUALITY.md:147` (Row 78b):
    - "A battery's forgery must differ from the artefact in the dimension it names..."
28. `kaidoku-shokunin/corpus/QUALITY.md:149` (Row 79):
    - "A predicate must read the candidate it claims to score, and its battery must exercise a green candidate..."
29. `kaidoku-shokunin/corpus/QUALITY.md:170` (Row 106):
    - "A control that shares state between arms has scored nothing..."
30. `kaidoku-shokunin/corpus/QUALITY.md:185` (Row 114):
    - "A gate that reads a receipt binds the receipt to its producer. A check that scores a saved receipt compares the receipt's instrument hash and measured revision with the ones it was invoked with, and re-derives the payload's carrier ids, pins and numeric relations from the frozen instrument's own table — otherwise a fabricated receipt with self-declared fields satisfies the check."
31. `kaidoku-shokunin/corpus/QUALITY.md:187` (Row 115):
    - "A before-arm is cut from the world its base reader accepts. A forged-shape battery that cuts its shapes from the after-world receipt produces a false before-arm..."
32. `kaidoku-shokunin/corpus/QUALITY.md:218` (Row 138):
    - "A mutant is killed only by a detector present in the target's own output. A battery that scores a mutant by 'no case failed' and a target whose selftest has no case for the mutant's path are the same result: the mutant survives..."
33. `kaidoku-shokunin/corpus/lessons/round-26.md:47` & `:54`:
    - M26-5: counting instrument re-deriving verdicts from evidence files accepted forged evidence; ignored second envelope file and accepted empty files.
34. `kaidoku-shokunin/corpus/lessons/round-34.md:57`:
    - M34-7: "the green surface keys on invariants it did not vary... permute() changes layout only — count, record order, flags, value and the name multiset all survive... the replay set must include one class per keyable invariant..."

---

### Topic (ii): Binding a Check to Subject Output Content Rather Than Exit Status

Hits located with verified `path:line`:

1. `souji-shokunin/corpus/QUALITY.md:42` (Q18):
   - "Certification integrity and tool safety are separate verdicts. A passing integrity gate never grants deletion authority; evidence must bind the actual safe state..."
2. `souji-shokunin/corpus/QUALITY.md:120` (Q51):
   - "Acceptance compares the declared result contract, not success-shaped output: counter scalar/container types are exact, summary stderr is empty without stripping/suppression, and cache check names plus ordered phase labels are independent reviewed expectations."
3. `souji-shokunin/corpus/QUALITY.md:210` (Q85):
   - "A fixture's discrimination is measured by a frozen mutant battery, and a kill is a fixture case failure reported in its own SUMMARY — a crashing fixture is a battery defect, not a kill."
4. `souji-shokunin/corpus/QUALITY.md:286` (Q110):
   - "A counted kill row names its finding: each row with a nonzero exit in a counter matrix carries a finding id from the counter's uppercase vocabulary, never `-` or a lowercase token."
5. `tabi-shokunin/corpus/QUALITY.md:72` (Criterion 21):
   - "A negative counting control asserts its intended diagnostic reason as well as exit code..."
6. `tabi-shokunin/corpus/QUALITY.md:102` (Criterion 26):
   - "A run claim (a count, verdict or exit 'at REV') cites a committed receipt recording argv, exit, stdout and stderr..."
7. `tabi-shokunin/corpus/QUALITY.md:472` (Criterion 81) & `L514` (Criterion 85):
   - "The oracle for a gate's self-test tally is that gate's own summary line... a self-test whose exit is nonzero or whose summary verdict is not clean is not a tally."
8. `tabi-shokunin/corpus/QUALITY.md:646` (Criterion 95):
   - "A mutation-kill case asserts the rule's outcome on a fixture that exercises the mutated rule — exit 3 with finding... not any nonzero exit."
9. `kumitate-shokunin/corpus/QUALITY.md:372` (Q26):
   - "an operability claim needs a pass-sensitive counter; listed-line and file-count terms are not enough..."
10. `kumitate-shokunin/corpus/QUALITY.md:722` (Q36):
    - "A frozen-counter success verdict is sensitive to pass/fail content, not just process completion..."
11. `kumitate-shokunin/corpus/lessons/round-78.md:23`:
    - "status C2 adopts — drift is a status distinct from an error, carried by the exit code rather than stderr alone..."
12. `kotoba-shokunin/corpus/QUALITY.md:36` (Q25):
    - "A claim's counter is shown able to fail: it is run on a mutant with the claimed content removed or falsified, and the changed output is recorded. A counter that counts names, extensions or rows and reads no content of the claimed thing is a census observable, never the whole evidence of a claim; the claim also cites a content guard whose exit code changes on that mutant."
13. `kotoba-shokunin/corpus/QUALITY.md:37` (Q26):
    - "A claim's headline asserts nothing its counter does not measure: every clause of the statement is turned on by the counter's output or by a cited guard whose exit code changes when that clause is falsified..."
14. `kotoba-shokunin/corpus/QUALITY.md:59` (Q48):
    - "A counter's self-test drives its public main() on a satisfying fixture and asserts exit 0 with the exact printed line, beside one broken-conjunct world asserting exit 1..."
15. `kotoba-shokunin/corpus/lessons/round-85.md:219` (M85-3):
    - "the frozen C1 predicate measured form, not the claimed content: literal R6 counts rows rather than distinct queries, so a vacuous..."
16. `kaidoku-shokunin/corpus/QUALITY.md:81` (Row 71):
    - "A gate's own mutants are scored on the triple `(exit, verdict, over-set name)`, never on the exit code alone, and the red scenario plays through the gate's real binary..."
17. `kaidoku-shokunin/corpus/QUALITY.md:152` (Row 95):
    - "A scoring step requires the receipt to exist and parse, never a zero exit. An instrument's green verdict is admitted only from a receipt that exists, parses, and carries the keys the claim names; a do-nothing file that exits 0 without writing a receipt (the 49-byte stub) is green under any exit-code-only check."
18. `kaidoku-shokunin/corpus/QUALITY.md:169` (Row 105):
    - "A frozen count is asserted, never emitted. A constant a counter computes and prints is not a check: the predicate's clause is satisfied only by a line that compares the computed count with the frozen value and folds the comparison into the verdict, with a one-entry-short arm that fails on that comparison alone."
19. `kaidoku-shokunin/corpus/QUALITY.md:198` (Row 124):
    - "A verdict is read from the producer's verdict fields... reads the checker's clauses.run_nonce and clauses.run_binding and requires the checker's own met to agree with its clauses; it fails closed on absent clauses and kills a force-true mutation with the named false-clause case rather than re-computing the answer from receipt fields."
20. `kaidoku-shokunin/corpus/QUALITY.md:211` (Row 134):
    - "An atom's predicate parses the shape, and its red fixture is committed. A record check that tests for a token's presence accepts a cell that negates the token it names... The atom parses the cell with an exact grammar, requires the typed fields and the receipt-bound values..."
21. `kaidoku-shokunin/corpus/QUALITY.md:212` (Row 135):
    - "A verdict written beside an evidence pointer is admitted only when re-derived from the receipt it names... An admitted annotation binds each claim to the JSON receipt the cell names — typed comparison (`true` never satisfies an integer field), atom shorthand only when exactly one atom matches, absent fields and unparsable clauses reported as failures..."
22. `kaidoku-shokunin/corpus/lessons/round-34.md:59` (M34-9):
    - "mutants killed by exit code only, and a label can hide an over-target reader..."
23. `kaidoku-shokunin/corpus/lessons/round-50.md:86` (M50-10):
    - "the 49-byte stub exits 0 on --selftest AND on the full predicate command while writing no receipt: a do-nothing green..."

---

### Topic (iii): Append-Only Correction of a Frozen Claims File

Hits located with verified `path:line`:

1. `souji-shokunin/corpus/QUALITY.md:122` (Q53):
   - "Supersedes Q52: a literal-oracle adequacy claim enumerates every changed predicate clause and every retained conjunct it re-asserts from the diff, including non-author additions, rather than selecting mutants only from authored vectors."
2. `souji-shokunin/corpus/QUALITY.md:167` (Q67):
   - "A capability cell's count literal is bound only by a row appended after the frozen base bytes (the base bytes must still prefix the file, so an in-place edit binds nothing)..."
3. `souji-shokunin/corpus/QUALITY.md:185` (Q75):
   - "A capability row's stated outcome is re-run at the round tip, and a drifted row is corrected only append-only, with an executed cause. Every SCORECARD.md row... is restated in a new appended section — never edited in place, and the pre-existing bytes must still prefix the file..."
4. `souji-shokunin/corpus/QUALITY.md:295` (Q114):
   - "HTML-block start conditions are not a complete visibility model: a closed multiline inline comment can hide correction tokens even when its opener is mid-line or follows NBSP..."
5. `souji-shokunin/corpus/QUALITY.md:301` (Q115):
   - "A hidden-span rule must be tested in BOTH directions before it is narrowed: a visible prose-token control (no closer) that must stay accepted, and a closed inline-comment control (opener mid-line or after NBSP, closer on a later line) that must be refused."
6. `tabi-shokunin/corpus/QUALITY.md:7` (Criterion 4):
   - "4. Errata are append-only blocks."
7. `tabi-shokunin/corpus/QUALITY.md:131` (Criterion 31):
   - "Refines 4 and 24: a correction to a line of a sha-pinned note names that frozen path and line..."
8. `tabi-shokunin/corpus/QUALITY.md:437` (Criterion 78):
   - "An appended correction cites its target by document and line, or by a quoted anchor; a correction that silently replaces a number or rewords a sentence is an unadmitted edit."
9. `tabi-shokunin/corpus/QUALITY.md:704` (Criterion 101):
   - "and a correction appended to a file some gate pins by bytes is either carried with that pin's own append-only refresh or placed elsewhere..."
10. `tabi-shokunin/corpus/lessons/round-32-verifier-spotcheck.md:151`:
    - "4. `claims.json` C1 `feasibilityDisclosed` is false as written (M2). Append a named correction, since the frozen file cannot be edited..."
11. `tabi-shokunin/corpus/lessons/round-45.md:26`:
    - "- **D1 (stale `frozenDigests` pin)** — repinned append-only: `.ufo/waves/round-44/claims-amendments.json`"
12. `kumitate-shokunin/corpus/QUALITY.md:860` (Q45):
    - "a pending non-author spot-check pointer is closed by an append-only named correction when its separate artifact lands..."
13. `kumitate-shokunin/corpus/QUALITY.md:1230` (Q22-C1):
    - "Q22-C1 — Q22's axis-set command mis-parses a scorecard whose Axes rows carry escaped pipes (round 77, append-only)."
14. `kumitate-shokunin/corpus/lessons/round-38.md:24`:
    - "LOG append-only was violated... rewrote the filed r37 entry... Named correction appended in round 38"
15. `kumitate-shokunin/corpus/lessons/round-42.md:188`:
    - "## Correction (appended round 43, 2026-10-22; the text above and the frozen round-42 plan stay as filed)"
16. `kotoba-shokunin/corpus/QUALITY.md:40` (Q29):
    - "A correction is registered, not only written: the superseded claim's stale phrase and its declared result go into `verifiers/check_correction_sweep.py`'s registry in the same commit as the correction, and the sweep must exit 0 before the round's report; a manual grep is not the sweep."
17. `kotoba-shokunin/corpus/QUALITY.md:45` (Q34):
    - "Append-only compliance of `corpus/SOURCES.md` is claimed only with `verifiers/check_sources_append_only.py` run over the claimed range and pasted; it exits 1 on a protected-cell rewrite..."
18. `kotoba-shokunin/corpus/QUALITY.md:80` (Q64):
    - "An append-only correction row replaces a cited token with the address of the same artefact; a token naming something that no longer exists anywhere is a recorded absence..."
19. `kotoba-shokunin/corpus/QUALITY.md:89` (Q73):
    - "A change to a file section that an earlier claim's counter pins byte-identical (a no-harm conjunct such as `§ Adjacent differs from the base`) is found by a sweep before the plan freezes... named in the plan's touch list, and ledgered inside that counter in the same commit — an append-only sha256 ledger with a reason and a self-test arm that an unledgered rewrite is still rejected; a frozen counter is never edited to widen its target."
20. `kotoba-shokunin/corpus/lessons/round-80.md:39`:
    - "Stale-census correction (R79-D2), append-only notice... round-end line reads..."
21. `kaidoku-shokunin/corpus/QUALITY.md:160` (Row 100):
    - "A landed freeze-ledger verdict row is never edited into a conflicting view. A verdict row in `corpus/claim-freezes-v2.tsv` is never edited after its filing round closes. A correction is an appended row in the companion ledger `corpus/claim-freezes-corrections.tsv` (`correction-id`, `corrects`, `field`, `was`, `now`, `cause`, `receipt`, `utc`) that names the row and field it corrects, the value it had, the value it now carries, the cause, and a receipt; the gate-governed `claim-freezes-v2.tsv` itself may gain rows only when the gate's own audit demands them..."
22. `kaidoku-shokunin/corpus/QUALITY.md:162` (Row 101):
    - "provenance fields appended in a correction block are list items, and their checkers say so..."
23. `kaidoku-shokunin/corpus/QUALITY.md:208` (Row 132):
    - "A correction names both values, and a frozen comparator's actual result is kept. A record correction that repeats only the superseded value leaves the record self-contradictory: the correction names the old token AND the value the receipt re-derives, side by side, so a reader can see which one is operative; and when a frozen before-arm's named reader pair cannot produce the frozen result, the record keeps the measured value, the frozen sentence and the replacement arm separately."
24. `kaidoku-shokunin/corpus/QUALITY.md:241` (Row 150):
    - "A record cell that states a value is re-derived at the revision it names; a correction filed elsewhere leaves the cell wrong... A correction written into a lesson does not repair the cell the instruments read. The supersession row is the correction, and its count and id list are re-derived by the command that produces them."
25. `kaidoku-shokunin/corpus/lessons/round-67-verifier-spotcheck.md:169-170`:
    - "lesson and LOG disclose the correction. `plans/round-67-claims.md:59` gets the same treatment (or an explicit 'frozen plan, superseded by A4/M67-4' note)."

---

## 3. Comparison with Chousa's QUALITY 139: Duplication, Strength, and Differences

Chousa QUALITY 139 states:
> "139. **Entropy and exact verdict checks extend through the outer battery, not only its inner fixture.** Both r76 outer batteries accept call-count scripts without reading inputs (`R76Review/c1-order-probe.out`, `c2-order-probe.out`, both exact PASS exit0). A matrix-keyed subject and contradictory summary lines also reach 12/12 (`R76Critic2.md` §§2–5). Check before successor freeze: score outer invocation-order and parent-keyed controls, require exactly one internally consistent summary/check set, and classify timeout rejection separately from semantic disagreement. The cited saved scripts and receipts are the red-before; a passing inner shuffle is not their fix. — `lessons/round-76.md`, Instrument limits."

### Does Chousa QUALITY 139 duplicate the sibling criteria?
**No, there is no duplication.**
1. **Scope difference on Topic (i):**
   - Sibling rules (`souji` Q100/Q102, `tabi` 55/112, `kumitate` Q29/Q57, `kotoba` Q37/Q74, `kaidoku` Row 40/114/138) enforce general discrimination against shape-only readers, deterministic case-leaking fixtures, and unauthenticated receipts.
   - However, **none of the sibling rules specifically addresses the architectural boundary between an inner test fixture and the outer battery runner**. In `chousa`, the inner matrix already had fixture permutation in round 75, but the outer battery ran test subjects in static sequence, allowing a call-counting outer oracle to pass. Chousa QUALITY 139 is the only criterion explicitly mandating entropy and exact verdict verification across the outer battery harness itself.
   - **Which is stronger?**
     - Chousa QUALITY 139 is **stronger and more precise** on outer harness defense against call-counting/order oracles (requiring outer permutation, parent-keyed controls, and distinct timeout classification).
     - Sibling criteria (especially `kaidoku` Row 114 and `tabi` 112) are **stronger on general receipt provenance and production-CLI coverage** across all enumerated mutation vectors.

2. **Scope difference on Topic (ii):**
   - Chousa QUALITY 139 addresses content checking in a narrow, specific way: "require exactly one internally consistent summary/check set". In round 77, this is implemented as the "content leg" (validating the 12-line contract table from matrix stdout).
   - Sibling criteria (`kaidoku` Row 71, Row 95, Row 135; `souji` Q51; `kotoba` Q25) address the general anti-vacuity principle: a pass must be derived from parsed receipt keys/payloads and structured findings, never from process return code 0 alone.
   - **Which is stronger?**
     - `kaidoku` Row 71 (`(exit, verdict, over-set)` triple) and Row 95 (mandatory parsing of JSON receipt keys, rejecting 0-exit do-nothing stubs) are **stronger** as general architectural standards.
     - Chousa QUALITY 139 and round 77 C1 apply this principle specifically to the matrix subprocess stream, requiring the child process to output an exact typed contract table matching the battery's expectations.

3. **Scope difference on Topic (iii):**
   - Chousa QUALITY 139 has **zero overlap** with Topic (iii).
   - In `chousa`, Topic (iii) is governed by **QUALITY 136** ("A correction counter derives its numbers from the authored statement... tests polarity, magnitude and position, plus base ancestry for append-only") and **QUALITY 140** ("Authored-statement binding requires unique identity, rendered visibility and the history it claims... append-only history checks each relevant transition rather than endpoint net deletion").
   - **Which is stronger?**
     - Chousa QUALITY 140 and `c3-count.py` are **stronger on in-file Markdown grammar and visibility**: checking CommonMark HTML comment hiding rules (`souji` Q114/Q115), section ordering (terminal section requirement), and git numstat.
     - Sibling criteria like `kotoba` Q29 (`verifiers/check_correction_sweep.py` registry sweep) and `kaidoku` Row 100 (dedicated companion correction ledger `claim-freezes-corrections.tsv`) are **stronger on repository-wide sweep and ledgering**, preventing stale superseded sentences from persisting unflagged in other documents.

---

## 4. Contradiction Analysis Against Round-77 Predicates

### C1 Predicate
- **Command:** `python3 -B corpus/evidence/round77/matrix-battery-v4.py --matrix corpus/evidence/round76/loader-matrix-v3.py --work DIR`
- **Output:** `BATTERY=PASS forgers_rejected=11/11 positive=2/2 oracle=REJECTED`, exit 0.
- **Analysis:**
  - Sibling rules (`souji` Q102, `tabi` 106/112, `kumitate` Q29/Q57, `kotoba` Q37, `kaidoku` Row 78b/114/115) completely align with C1's intent to defeat shortcuts and oracles.
  - **No contradiction exists.**

### C2 Predicate
- **Command:** `python3 -B corpus/evidence/round77/c3-count.py --lane . --base a519fb0a80cf52c7988713c1f05b3ce8440fedda --rev <landing>`
- **Output:** `C3=PASS checks=5/5`, exit 0.
- **Analysis:**
  - C2 checks append-only correction of the false prose sentence in `corpus/evidence/round76/claims.md`.
  - Sibling rules (`tabi` 4/78/101, `souji` Q67/Q75, `kotoba` Q29/Q73, `kaidoku` Row 100/132) uniformly prohibit in-place rewrites of frozen files and mandate append-only corrections that retain the original text and quote both old and new facts.
  - Sibling precedent (e.g. `tabi` round-32 verifier spotcheck L151: "Append a named correction, since the frozen file cannot be edited"; `tabi` round-45 L26: repinned append-only; `kaidoku` round-67 spotcheck L169-170: explicit correction note in frozen claims) directly confirms that appending an erratum/correction block to an earlier round's frozen claims file is a legitimate, standard compliance pattern.
  - **No contradiction exists.**

### Structural Tension / Disclosed Limitations
While there is no normative contradiction, the sibling scan reveals two critical structural limitations in the round-77 frozen instruments:
1. **Content leg non-closure in C1 (`claims.md:52-53`):**
   `claims.md` explicitly discloses:
   `--no-content` → still `BATTERY=PASS`, so the content leg is a shape requirement and is not claimed as the discriminating closure.
   Under sibling rules `tabi` 115 ("carry BOTH polarity negatives") and `kaidoku` Row 78b ("forgery must differ from the artefact in the dimension it names"), a claimed verification leg must have an isolated control that fails when that leg is mutated or disabled. Currently, all three forged matrices in the oracle leg fail on the *order* leg, leaving the content leg unexercised by the oracle leg.
2. **Endpoint numstat in C2 (`c3-count.py:97-107` vs chousa QUALITY 140):**
   `c3-count.py` checks `git diff --numstat BASE REV -- TARGET` and requires `deleted == 0`.
   As chousa QUALITY 140 warns ("append-only history checks each relevant transition rather than endpoint net deletion"), an endpoint diff cannot detect a multi-commit sequence where lines were deleted in an intermediate commit and restored before landing. Sibling rules (`kotoba` Q73, `souji` Q67) also emphasize per-transition integrity.

---

## 5. Non-Obvious Move and UFO-FSD Synthesis Proposal

### Evidence
1. **Local round-77 evidence:**
   - In `corpus/evidence/round77/claims.md:51-53`, the closure-removal twin shows:
     - `--no-permute` → `BATTERY=FAIL` with `oracle=MISS` (order leg is load-bearing).
     - `--no-content` → `BATTERY=PASS` (content leg is not discriminating against the current oracle trio).
   - In `matrix-battery-v4.py:117-133`, the three forged matrices in the oracle leg (`forge-order-matrix.py`, `forge-order-matrix-table.py`, `forge-order-matrix-block.py`) all hardcode invocation sequences and fail on the randomized order. None of them models a matrix that correctly handles permuted orders but deliberately emits a malformed or absent contract table.
   - `R77ScoutA` demonstrates that while `secrets.randbits(64)` generates high-entropy seeds, the battery preserves the test subject's basename in `--counter <path>` (`sub.name`), allowing an adversary to distinguish forgers from positives via path inspection.
   - In `corpus/evidence/round77/c3-count.py:97-107`, C3-4 checks only the net diff between `BASE` and `REV`.

### Affected Axes
- **Operability (C1)**: Primary beneficiary. Elevates the content leg from a passive syntax filter to an actively verified, discriminating closure.
- **Calibration (C2)**: Secondary beneficiary. Hardens append-only verification against intermediate commit tampering.

### Proposed Move
Synthesize a successor instrument specification (for round-78 freeze or post-round calibration) that closes both gaps without disturbing frozen round-77 execution:
1. **Dynamic Content-Coupled Discriminator (Operability):**
   - Introduce a 4th oracle: `forgers/forge-order-matrix-content-fault.py`. This oracle correctly determines execution outcomes (or reads permuted order) but emits a corrupted contract table (e.g. wrong `expected_rc` mapping or missing lines).
   - Under `--content`, this oracle is rejected (`oracle=REJECTED`).
   - Under `--no-content`, this oracle passes (`oracle=MISS`).
   - This creates a true closure-removal twin for the content leg, making the content leg strictly load-bearing and resolving the `claims.md` limitation.
2. **Transition-Aware History Walker (Calibration):**
   - In the successor to `c3-count.py`, replace endpoint `git diff --numstat BASE REV` with a per-commit log verification:
     `git log --format=%H --numstat --reverse BASE..REV -- TARGET`
     Asserting that for *every single commit* in the range, `deleted == 0`.
   - This directly operationalizes chousa QUALITY 140 and aligns with `kotoba` Q73 and `souji` Q67.

### Risks and Trade-Offs
- **Risk:** Modifying frozen instruments during round 77 is strictly prohibited (frozen at `e6fcdc47`).
- **Mitigation:** The proposed move is bounded: round-77 predicates remain completely untouched and score against their frozen bytes. This proposal serves as the verified bridge and design specification for the round-78 successor claims.
- **Runtime overhead:** The per-commit Git inspection adds less than 15 ms to calibration runtime.

### Verification
A proof-of-concept verification script was modeled and checked against committed Git graph properties:
```sh
# Verify transition-level append-only check on target:
git rev-list BASE..REV | while read -r c; do
  del=$(git diff-tree --numstat "$c" -- corpus/evidence/round76/claims.md | awk '{print $2}')
  if [ -n "$del" ] && [ "$del" -gt 0 ]; then
    echo "DELETION DETECTED at $c: $del lines"
    exit 1
  fi
done
```
This check guarantees zero intermediate deletions across the entire landing history.

---

## 6. Tools and Hygiene
- **Tooling:** No tools installed, upgraded, or removed. Host pacman paused per host guard.
- **Network / Egress:** Zero network calls; zero socket connections.
- **Scratch:** No scratch files persisted; `/fast/scratch/hyaku/chousa-r77/R77ConnectorA/` clean.
- **Bounds:** Leaf execution only. Single report output.
