# R59Scout37 — bounded offline data walk

## Observed

- The specified frozen round-59 claims artifact `corpus/evidence/round59/claims.md` was not found. The round-59 evidence listing contains only `census-start.txt` and `controls/c1-before.txt`; no alternate frozen claim body is established here. Therefore exact current predicates cannot be compared to the receipts below.
- `corpus/evidence/round59/census-start.txt` records five W04 duplicate-URL warnings (S051, S053, S073, S074, S075), a successful SOURCES validator line, and `exit=0`. This is a start census, not a proof that scopes or source contents are valid and not an end-state comparison.
- The round-59 C1 before receipt (`corpus/evidence/round59/controls/c1-before.txt`) records `OK=4/4`, `REFUSE=0/7`, `BEFORE_FOREIGN=deleted`, `DENIED=0/0`, `C1=FAIL`, `EXIT=1`. In detail, FOREIGN deletes a foreign file; SYMLINK_OUT writes to its target; SYMLINK_CACHE and MANY_QUOTES return success where refusal was expected. FIFO_TXT, DEVZERO_TXT, and FAT_RAW return failure but lack expected diagnostic tokens. ESCAPE_ENTRY is refused; EMPTY, REBUILD, HELDOUT pass. This is direct captured before-state evidence, not a current after-state or causal diagnosis.
- The round-58 verifier spot-check (`corpus/lessons/round-58-verifier-spotcheck.md`, §§11–17, 34–38) records C1 unprovable because the counter expects uppercase `=PASS` while refusal tokens are lowercase; C2 unprovable because builder span-start offsets cannot meet occurrence-offset binding and byte-identical rebuild simultaneously. Its routed correction is to freeze exact-predicate positive controls, repair/re-freeze those counter defects, and retain reachable after receipts. This makes the round-59 before receipt a relevant baseline but does not show whether repairs landed.
- The frozen round-57 C3 claim (`corpus/evidence/round57/claims.md`, lines 70–127) is a useful offline source-chain example: it ties a normative-reference entry to captured S127 and other documents using digest-backed capture, defined text forms, quote/offset and heading requirements. The manifest has captured span texts for S131–S133 and S118/S127. This shows an existing lane pattern for bounded documentary chaining, not validation of those bytes or the round-59 claim.
- The same round-57 frozen claim makes its evidence boundary explicit (lines 11–15): live fetch scope was an approval table, while L0 `8d77e6c1` remained open. Round-58 closure likewise rejected current legal/status assertions absent approved fetch scope and current authority (spot-check §24). No live fetch or authority upgrade is supported by this walk.

## Bounded interpretation

**Observed:** the baseline C1 receipt has both false-success outcomes and harmful side effects, alongside a zero refusal denominator. **Inference:** any later pass claim would need to be checked against its exact frozen aggregate predicate and positive-path control, with side effects and refusal diagnostics kept distinct; the receipt alone does not identify which code or fixture caused each outcome. The prior closure explicitly warns that passing component legs did not establish a reachable aggregate C1 verdict.

The duplicate URL warnings establish reuse across recorded scopes only. S074's registry description (see `corpus/SOURCES.md`, S074) identifies a rejected duplicate of S059's hashlib scope; that one example cautions against treating every census warning as a duplicate claim or invalid source. Registry descriptions are lane records, not independent source verification.

## Unknowns / confidence

High confidence in the literal contents of the cited lane artifacts. The frozen round-59 claim body, any after receipt/final control output, and end census were not established; claim-to-predicate alignment, repair status, and final verdict remain unresolved. S131–S133 capture text was not reopened here, and no causal attribution is made. No external fetch, source modification, or tool installation was performed. LSP was not used: this is an artifact reconnaissance report, not a source-code semantic-contract finding.

## Report trailer

Lane-root-relative report: `.ufo/waves/round-59/w1/R59Scout37.md`.
