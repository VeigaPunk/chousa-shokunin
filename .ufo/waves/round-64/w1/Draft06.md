# Draft06 — round64 attempt2 claim erratum (advisory)

## Behavior and provenance

Static, read-only enumeration; no repair, battery execution, runtime invocation, or closure judgment. Lane: `/home/vgpnk/Projects/shokunin/chousa-shokunin`. Assignment identifies freeze commit `bf40d99bda9eefdad3ed6276da077cfb24ba82f1`; that commit association was supplied, not independently verified. Evidence below is the local source/receipt text read in this seat, not a new execution at frozen or landing bytes. `ref-preflight-v3.py` remains a candidate, not production evidence.

Axes: factual accuracy, preservation of frozen predicates, provenance clarity, and zero product/peer interference. Only documentary moves were retained. No tools installed or updated.

## Enumerated errata

1. **Contradictory arithmetic in the frozen C1 instrument's prose.** `corpus/evidence/round64/c1-battery-v3.py:56-58` says, verbatim, `CLEAN=1/1 DEFECTS=29/29 BENIGN=11/11 ZERO=3/3 BATTERY=PASS`, “forty-four legs”, and absent-tool `DEFECTS=0/29`. Its actual table at lines 403–447 contains one CLEAN, seventeen D defects, eleven E defects, eight B benign, three E benign, and three ZERO legs: **1 + 28 + 11 + 3 = 43**. Its summary construction at lines 615–617 and absent-tool branch at 597 use denominator 28. Claims lines 38–44 correctly say 28 defects and forty-three total; those numbers should not be reported as erroneous. If lines 56–58 instead describe only the seventeen-defect/eight-benign base described immediately above, that base totals **1 + 17 + 8 + 3 = 29**, not forty-four. Enumerate this prose contradiction without changing either instrument or claim.

2. **E12 is not a reliably benign same-token fixture.** Claims lines 42–43 and 73 call E12 a benign valid shape / false positive. Frozen battery lines 386–389 create `escaped_q{tag()}.md` but independently draw another `tag()` for `knowledge/escaped\\_q{tag()}.md`. Line 202 defines each call as a fresh `rnd.getrandbits(32)` draw. Unescaping an underscore does not reconcile two different generated suffixes. [INFERENCE] When those draws differ, the created file is unindexed and the README has a phantom token; rejecting it is conforming, not evidence of the promised escape false positive. Independent draws can collide, so this is not a claim that every possible seed must differ.

3. **E13 has the same false benign-token premise.** Frozen battery lines 391–394 create `gate notes q{tag()}.md`, then independently draw the suffix in `knowledge/gate%20notes%20q{tag()}.md`. Percent decoding fixes spaces, not the independently generated suffix. [INFERENCE] For differing suffixes, rejection is correct. The inherited `c1-battery-supplement.py:386-396` draws once into `t` for each fixture and reuses it; this is a distinct post-freeze supplement, never a frozen C1 pass or a repair performed by this seat. The pre-existing `claims-erratum.md:5` independently discloses the mismatch.

4. **“Whole-token” exceeds the literal right boundary.** Claims lines 55–56 freeze `(?<![\\w.-])(?:knowledge/)?NAME(?![\\w-])`, where NAME includes `.md`. The right boundary excludes word characters and hyphen, but **not dot**. [INFERENCE from the specified expression] With NAME `entry.md`, `entry.md.extra` contains a forward match, just as sentence-final `entry.md.` does. The limit at lines 97–99 discloses the latter punctuation case, but does not distinguish a dotted extension from sentence punctuation. This is a contract-description limit, not authority to tighten the frozen regex.

5. **D3's class description must not be promoted into URL/code-span rejection.** Claims lines 29–31 identify a name counted from “a URL/code-span/strike mention” as D3, but the literal normalization at lines 53–55 removes strike spans only; it does not strip URLs or code spans. Lines 95–97 explicitly admit E05 is strike-only. [INFERENCE] An exact `entry.md` inside backticks or after a URL slash can satisfy the specified regex. Therefore a strike-row fixture does not demonstrate rejection of all three named mention contexts. This is a mismatch between class-level rhetoric and literal predicate/coverage, not a newly observed candidate execution failure.

6. **Boundary-class transcription is visibly malformed.** Claims lines 97–98 literally say `[coeff]w.-` and `[coeff]w-`, whereas the operative expression at lines 55–56 uses `[\\w.-]` and `[\\w-]`. Preserve the operative regex and record the transcription defect; the corrupted descriptive tokens are not a new rule.

7. **C2's “one per surviving mutant class” is not one-to-one arithmetic.** Claims lines 148–151 list six survivors (A05, A06, A07, A08, A10, A11). Lines 158–160 enumerate seven added selftest cases C4–C10 and append “one per surviving mutant class”. Seven cases cannot be a one-to-one allocation over six classes. The same claims separately assign A07's first-add scenario to a scratch-repo matrix leg (136–137), and A11 to a fault arm (160–161). This identifies an overcompressed explanatory assertion, not a falsification of the twelve-mutant result; no C2 runner or selftest was executed here.

8. **The legs-only receipt is not identical in expectations to the full-before receipt.** Claims lines 73–74 call the second run “the same fourteen failures”. Both receipts do list fourteen failing leg IDs, but `.ufo/waves/round-64/before-e.txt:2-4` expects `[G01,G02]`, `[G01,G02]`, and `[G02]`; the full receipt lines 28–30 and frozen leg table lines 431–433 expect `[G01,G02,G04,G05]` for all three. Thus “same” is supportable for failing IDs, not identical frozen expected gate sets. Neither receipt is a new run by this seat.

## Gates and observed outcomes

- Existing full-before receipt `.ufo/waves/round-64/c1v3-before-full.txt:44`: `CLEAN=1/1 DEFECTS=17/28 BENIGN=8/11 ZERO=3/3 BATTERY=FAIL`. Claims lines 67–68 attribute exit **1** to it; the plain receipt itself does not independently encode the process exit.
- Existing E12/E13 receipt lines 38–39: `LEG E12 benign FAIL rc=1 want 0` and `LEG E13 benign FAIL rc=1 want 0`. These are observed receipt contents, not newly reproduced executions, and do not isolate normalization behavior from the fixture-token defect.
- Frozen C1 kill rule (claims 89–93) still requires the **unmodified** battery to pass three times at landing bytes, null FAILs, and twice-passing v2 cross-check. No such pass is established here. Report the frozen failure honestly; a supplemental result cannot replace it.
- C2/C3 closure, numeric axis scoring, mutation acceptance, and non-author closure remain outside this seat. No canonical Rust judgment is claimed.

## Exact operations and limits

No shell commands were run; command/output/exit records for new probes are **not applicable**. This assignment requires enumeration, not execution; no bounded probe was necessary or performed. `read`/`grep`/`glob` returned source listings and receipt text successfully; those file-tool responses have no subprocess exit status.

Read operations: `/home/vgpnk/.omp/agent/RULES.md`; `skill://godspeed`; `skill://agent-self-evaluation`; lane-relative `corpus/evidence/round64/claims.md` (all displayed lines); `claims-erratum.md:1-180`; `c1-battery-v3.py:23-61`, `:270-294,380-400,401-450`; `.ufo/waves/round-64/c1v3-before-full.txt:1-100`; `before-e.txt:1-20`. Targeted grep located fixture construction, tag generation, summary arithmetic, and supplemental single-token reuse in the two battery files. A glob listed round64 evidence and wave-root artifacts. No source digest or commit identity was newly measured.

Touched surface: this report only. No operator input, frozen claim, counter, instrument, production code, sibling artifact, git/jj state, PATH directory, or service changed. No network access, package transaction, clone, or scratch tree was created; there is no seat scratch to remove.

Output-path conflict preserved verbatim: “Write only your own report and evidence beneath /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-64/w1/Draft06/ (report.md)” versus “Report: write your scoped findings to .ufo/waves/round-64/w1/Draft06.md”. This seat uses the later explicit Report trailer, without creating an alternate folder report or modifying another seat's output. This is reported for canonical resolution, not silently treated as authorization to alter the contract.

## Self-evaluation

Accuracy 4/5: every finding cites visible source, but supplied freeze identity was not independently authenticated. Completeness 4/5: requested arithmetic/token enumeration is delivered; no dynamic token demonstration is asserted. Clarity 4/5: literal predicate, inference, and existing receipts are separated; report is necessarily longer to preserve conflicts. Actionability 4/5: numbered errata are available for L1 without editing frozen instruments; no closure decision is supplied. Conciseness 4/5: operation provenance and exact conflicts add length. Overall **4.0/5**. Highest-impact improvements belong to the integration owner: authenticate frozen bytes and preserve the distinction between frozen failure and post-freeze supplement; neither is falsely claimed here. Would the user agree? The report is deliberately bounded to advisory enumeration.

Artifact: `.ufo/waves/round-64/w1/Draft06.md`.
