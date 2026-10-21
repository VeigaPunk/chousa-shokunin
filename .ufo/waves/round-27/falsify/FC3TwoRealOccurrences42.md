# FC3 falsification — C3 control `two-real-occurrences` (round 27, attempt 1)

Target: dd72641e574679c4f7882dd43de072b4c8892d6f (gate sha256 ca39d14d…f84, verified on extraction).
Sandbox: /tmp/chousa-r27-falsify-FC3TwoRealOccurrences42 (git archive extraction; mutants + fixtures only there).

## Verdict: HOLDS

## 1. Derivation independence — HOLDS
Control body: `corpus/evidence/round27-regressions.py:151-159` — `('two-real-occurrences', 'S002,S002', 1, 2)` is a literal expectation in an independent script; it reads no gate code. Counting regexes `^FINDING META_SOURCE_NOT_MINED\b[^\n]* source_id=S002(?: |$)` and total `^FINDING META_SOURCE_` re-derive the frozen finding-line contract (same fixed text as the r26 receipts/selftest), not gate internals. The per-occurrence (no-dedupe) semantics comes from the declared r27 contract: round27-claims.md C3 "standalone ASCII S-ids without invented or duplicate occurrences" (duplicate = rescan-invented), corroborated by build evidence `.ufo/waves/round-27/build/CriticRegistryTokens.md:31` ("The contract counts per occurrence… the r27 harness would reject this"). rc=1 derives from the declared CLI contract (exit 1 = unresolved findings). The only gate-text parsing in the control script is the C1 usage-helper extraction; C3 has none.
Disclosure (not disqualifying): the gate's own selftest contains a semantically identical case `metadata-registry-duplicate-occurrences` (tools/research-gate.sh:6456-6460, `source: S002,S002` → 2 NOT_MINED), so the control is independent code but not fully independent case design.

## 2. Mutation sensitivity — HOLDS (with precision caveat)
Driver: sandbox `occ-driver.py` (mirror of the control's fixture: registry S001 mined/used-by entry + S002 queued; control's exact count regexes; 7 declared cases + 7 same-class probes).

- Mutant A — dedupe (`| LC_ALL=C sort -u` appended to the landed grep pipeline), `mutant-dedupe.sh`: `two-real-occurrences` FAILS for the intended reason — `NOT_MINED@S002 1 != 2`, `META_SOURCE_* 1 != 2`, rc 1 with a real finding emitted (no parse/setup error). Also fails probe-three-occurrences (1≠3), probe-rowmissing-duplicate (1≠2), probe-mixed-three (2≠3), probe-nonascii-boundary, probe-hyphen-boundary. `adjacent-real-ids` still passes (set semantics invisible at 1 id).
- Mutant B — exact revert of the scanner rewrite to parent 8b65c72 (`source_id_re='(^|[^[:alnum:]_])(S[0-9]{3,})([^[:alnum:]_]|$)'` + `source_scan=${source_scan#*"$source_match"}` rescan loop; parent had no `local LC_ALL=C`), `mutant-rescan-revert.sh`: `two-real-occurrences` itself still PASSES (2=2). The revert is caught by four sibling controls, all semantically: glued-before-terminal (invents S002, NOT_MINED 1≠0, rc 1≠0), glued-missing-before-terminal (invented finding 1≠0), nonstandalone-duplicate (2≠1), glued-repeat-duplicate (3≠1). `underscore-glued` passes under revert too (the parent regex already rejects `_`/`x` adjacency). Zero setup errors in every mutant run.

Conclusion: the named control guards the no-dedupe/per-occurrence half of the fix; occurrence identity as a whole is guarded by the 7-case table acting as a set. Reverting the whole rewrite does not make this one control fail — that is a coverage fact, not a defect.

## 3. Counterexample search — none found (landed gate correct in class)
All against the unmutated landed gate; expectations derived from the declared per-occurrence contract and the r26 oracle boundary class:
- `S002,S002,S002` → 3 findings (rc 1). `S003,S003` → 2 ROW_MISSING. `S003,S002,S003` → 3. `S002,S002` vs mined+used-by registry → 0, rc 0.
- `S002é S002` → 2 occurrences: matches the r26 oracle class `(?<![A-Za-z0-9_])S[0-9]{3,}(?![A-Za-z0-9_])` (é is not a blocking char there). It diverges from the gate's claims-span word-char convention (non-ASCII = word char, research-gate.sh:241), but the registry S-id class is separately declared by the oracle, so this is not a defect.
- `S002-S002` → 2 (hyphen boundary in both contracts). Folded continuation (`source: S002\nprose names S003 here`) → 2 ids, matching oracle `metadata_values` folding.
- 1000 occurrences → 1000 findings (no cap/dedupe). `S0020,S002` → ROW_MISSING S0020 + NOT_MINED S002 (no invented prefix occurrence); `S0020` solo → 1; `S0000002` → ROW_MISSING S0000002.
- 20,000-trial fuzz differential (seed 2707; alphabet incl. `_ .,;:- é — 。 combining mark ２ tab glued `S002`/`S00`): landed extraction (C-locale `[[:alnum:]_]+` run-split + `^S[0-9]{3,}$`) vs oracle regex — `mismatches= 0`, exact order+multiset equality.

## Commands / exits
- `python3 occ-driver.py tools/research-gate.sh` → EXIT=0 (14/14 pass)
- `python3 occ-driver.py mutant-dedupe.sh` → EXIT=0 driver; control case fails as intended (count mismatch)
- `python3 occ-driver.py mutant-rescan-revert.sh` → EXIT=0 driver; 4 sibling controls fail semantically, target case passes
- occurrence-cap/width probes → EXIT=0, all OK; fuzz differential → `mismatches= 0`
- Full regression script and `--selftest` intentionally NOT run (L1 owns them, per bounds).

## Limits
- Invalid-UTF-8 source values untested (unwritable via text fixtures; oracle decodes strict UTF-8, so out of declared contract).
- Boundary equivalence is proven over the fuzz alphabet, not all of Unicode.
- Dedupe mutant uses `sort -u`; any set-semantics implementation is behaviorally identical for these cases.
- No installs or updates performed; no network, host files, /proc, strace, mount, or debugger use; lane production files untouched except this report.
