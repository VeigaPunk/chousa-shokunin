# RegistryQuarantine — prior quarantine verdict boundary

## Scope and identity

Read-only analysis of the assigned frozen claims text, relevant committed round-42 quarantine evidence, and current round-60 counter/source evidence. No live fetch or source-tree mutation. No LSP device/server was exposed in the available tools; the findings below are grounded in direct file inspection, not semantic reference resolution.

The assignment pins claims SHA-256 `09d8053f5f09a26c07f41286a7a885a2c21bff31b30f71963cceaa35d971a440`; `sha256sum corpus/evidence/round60-claims.md` returned `65721569fc1336b159c7637acf476cda6f583bbd4b3a84aaadd239f7d02018d`. These differ. I left the claims file untouched; whether this is the intended snapshot is unresolved. Findings about round-60 claims refer to the observed file content, not a certified match to the assigned digest.

## Observed prior quarantine evidence

- Round 42 explicitly derived a 24-row chousa slice from two register table shapes: 20 payload-absent rows plus four unchecked-family S100–S103. It warned that the register's `chousa 20` summary and 194-row header were stale (`corpus/evidence/round42/claims.md:20-33`; `corpus/lessons/round-42.md:47-50`).
- The frozen per-row decision rule makes unchecked-family rows `unverifiable`, never fabrication; no capture, bot wall, unrendered binary office document, or too-short capture likewise prevents a negative/fabrication conclusion (`corpus/evidence/round42/claims.md:35-52`).
- The committed adjudication receipt follows that rule for S100–S103: each is `unverifiable`, with reason that the register's unchecked family named no locator and no quote was checked (`corpus/evidence/round42/receipts/verdict.txt:24-27`). This is a boundary against treating lack of evidence as evidence of fabrication, not a judgment that the underlying quotes are present or absent.
- The round-42 lesson records concrete process failures: a bot-challenge page had been misrepresented by an overbroad source class, an examination status was constant while its counter checked only membership in a legal vocabulary, a parser assumed one table shape and dropped S100–S103, and a stale summary was mistaken for underlying data (`corpus/lessons/round-42.md:81-84`). These support keeping source-form, actual inspection, field variation, and data-row parsing distinct. They do not establish that the current round-60 counters have those same defects.

## Relation to round-60 claims and current evidence

The observed C1 claim is specifically a round-58 counter measurement-integrity correction and disclaims whole-builder/hazard-matrix security (`corpus/evidence/round60-claims.md:5-11`). The round-42 quarantine receipts concern a distinct source-quote adjudication task; they do not validate the round-60 candidate safe-path, pinned control, or output-injection states. Prior C1 false-positive evidence is separately documented in `.ufo/waves/round-59/w1/R59Executor09.md:215-260` and should not be conflated with the S100–S103 source-quote verdicts.

Current counter/source inspection reports elsewhere in this wave identify C1/C2 predicate or admission gaps; this quarantine history adds no counter-execution evidence and no present-day external-source verification. In particular, an `unverifiable` historical source-row verdict cannot be upgraded by reuse of the frozen receipt, and it cannot substitute for the round-60 C2 claim's required in-round offline S101 reopen, located quote and Gate metadata, or non-author QUALITY disposition (`round60-claims.md:13-15`).

## Conclusion and gaps

Observed: the earlier quarantine process explicitly preserved four unchecked-family entries as unverifiable rather than calling them fabrication, and recorded mistakes about source form, status evidence, row-shape parsing, and stale summaries. Inference: this is a relevant caution against collapsing missing/weak provenance into a positive or negative source verdict, but it neither proves nor falsifies either current round-60 claim. The assigned immutable SHA mismatch remains unresolved; no resolution source beyond the supplied assignment and present file was available. No claim/counter/source file was edited. Assigned scratch `/fast/scratch/hyaku/chousa-r60/RegistryQuarantine` was removed before report completion.