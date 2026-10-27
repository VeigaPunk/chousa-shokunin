# DataWalk — round 60 frozen-claim evidence walk

Scope: offline, read-only walk of the frozen claim file, prior committed evidence and current round-60 source/counter receipts. No counter execution, external fetch, or edits outside this report. Scratch `/fast/scratch/hyaku/chousa-r60/DataWalk/` was created for this assignment and removed before yield (empty; no probes run). No tool installed. Textual file evidence only; no LSP server was available to establish semantic references.

## Frozen-input identity

- The assigned frozen path is `corpus/evidence/round60-claims.md`; it declares base `b379919a873e7080a31ef92c7002f55f5374e2c6`, C1 narrowly about counter measurement integrity rather than full builder safety, and C2 about one source-grounded correction note (`round60-claims.md:1-17`).
- **Integrity discrepancy:** the assignment states SHA-256 `09d8053f5f09a26c07f41286a7a885a2c21bff31b30f71963cceaa35d971a440`; current lane observations in `w1/ClaimPlanner.md:21` and `w1/C2CounterAudit.md:22` report the file's SHA-256 as `65721569fc1336b159c7637acf476cda6f583bbd4b3a84aaadd239f7d02018d1`. I have not written or altered the freeze. The exact assigned bytes therefore remain unverified; do not treat local textual agreement as proof of frozen-hash identity.

## C1 — operability / corrected verdict derivation

**Observed evidence.** The prior committed round-59 review records a concrete round-58 positive-verdict forgery: a builder emits `=PASS` on refusal paths and still yields `C1=PASS` despite seven failing hazards and a deleted foreign file (`round-59/w1/R59Reviewer46.md:13-39`, especially its captured output at 19-35). That is direct prior evidence motivating the frozen claim's counter-integrity scope, not evidence that the round-60 candidate builder is secure. Current pre-work receipt records `INJECTION_REJECTED=1/1`, `BASELINE_DISCRIMINATES=1/1`, but `CANDIDATE_REFUSAL=0/1`, `C1=FAIL`, exit 1 (`.ufo/waves/round-60/c1-before.txt:2-8`). Its note says candidate and pinned r55 both delete the foreign file. This is an adverse baseline and a meaningful do-nothing distinction, not a post-change pass.

**Inference / limits.** C1's frozen predicate is explicitly limited to safe path, destructive pinned control, and output-injection discriminator; it disclaims the full set of builder hazards (`round60-claims.md:7-11`). Thus even a passing result would not validate all hazards documented by the earlier review. Before receipt's injected output is rejected, but the candidate safe path fails, so it does not establish the complete conjunctive predicate. Treat C1 as unproven until the after-state demonstrates all frozen legs; never convert injection rejection alone into a claim pass.

## C2 — depth / S101 grounding

**Observed evidence.** The lane-owned committed capture was reopened offline; receipt records URL, access date, raw and rendered digests, and exact quote `c. 文献类型及载体类型标志；` at line 245 (`.ufo/waves/round-60/s101-receipt.txt:1-6`; rendered text `.ufo/waves/round-60/s101-open.txt:242-268`). The capture says the specification recommends GB/T 7714 formats (line 241), identifies bibliographic type/carrier fields (245), and describes electronic carrier notation and examples (260-268). It does not evidence current validity or CNKI implementation; receipt states that limit at lines 5-6. The prior knowledge entry already cites S101 and records unresolved current-validity / application limits (`corpus/knowledge/citation-count-semantics-r37.md`, as located by `w1/ClaimPlanner.md:16`). C2's before-receipt states no new round-60 entry existed at claim base and the claim was not admitted (`.ufo/waves/round-60/c2-before.txt:1`).

**Counterexample / inference.** Current source-level audit reports the visible C2 counter can return `C2=PASS` against the unchanged base by checking an existing entry rather than requiring a round-60 note; its cited run output is `w1/C2CounterAudit.md:5-14`. The same audit identifies `FORM` as sourced from script-global `ROOT` rather than CLI `--root`, mixing lane-copy inputs with another checkout (`:16-18`), and sees no check of declared scorecard disposition (`:14,25`). These defects, if still present in the effective counter, mean its PASS does not verify the frozen C2 requirements. The audit's counterexample is a reported execution by that seat, not one I independently reran. Consequently source-grounding is established for the narrow captured-text observation, but admission of a new note and the full counter predicate are not established by the receipts here.

## Source hierarchy, verdict boundaries, unresolved

The strongest evidence for S101 is the lane-held raw capture plus its reproducible-looking local rendering and located quote receipt, not live web authority. The strongest evidence for C1's historical defect is the prior reviewer transcript with actual counter output; the current C1 receipt establishes only the pre-change state. The frozen path's byte identity, the post-change C1 result, any actual new C2 note, and independent confirmation or repair of the C2 counter's base-pass/root-isolation issues remain unresolved in this bounded walk. No claim verdict is assigned by this seat.

## Report trailer

Relative to lane root: `.ufo/waves/round-60/w1/DataWalk.md`
