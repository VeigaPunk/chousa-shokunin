# FxMetaStrict — round-25 `verify-metadata` falsification

Axes: operability/spec conformance; honesty and consistency of summary counters.

## Findings
- **No actionable defect found** in the corrected full integration pin for this assignment.

## Checkpoint identity and packaging corrections
- Private clone `/tmp/chousa-r25-FxMetaStrict`; tested full checkpoint `e93ac711f885a10d44fdd80a1734997419595b5a` (observed `git log -1`). Its gate SHA-256 is `63a39282a15f19f5b0443212e66ad2dfc8ce0315e65697e479a7206879a598b2`.
- L1 corrected the initially assigned `0fc037e6b07f3820ead8c9207a8034ac854197a1`: its gate SHA-256 is `752e4e382ed77c06ac5030ce2179c7ca524934f86fd2a6b25ef946ab027ac553` (old gate). The intermediate `d8c8cff3923f10481ac9ced66d0af7c41d38130c` has the new gate, but missed the updated evidence-index integration; `d8..e93` changes `corpus/evidence/README.md` by 154 insertions/43 deletions. Gate is unchanged between d8/e93 (`git diff --quiet ... -- tools/research-gate.sh`, rc=0). I ran checks only on e93.

## Exact checks and results
- In the private clone: `set -o pipefail; bash corpus/evidence/round25-meta-differential.sh | tee /tmp/chousa-r25-FxMetaStrict-differential.log` → `AGREE=54/54 (fixtures=27, modes normal+strict)`; log SHA-256 `9e956e0891dc1a7c56de4885f25e117782fcd2ed642bd8188eef99cd7cd9389e`.
- One-at-a-time command: `python3 /tmp/chousa-r25-FxMetaStrict-audit.py | tee /tmp/chousa-r25-FxMetaStrict-audit.log`. It ran each of the 27 fixture files separately with `CHOUSA_STRICT` unset and `=1`; all 54 META lines, finding-ID sets, and return codes matched the hand table. Full exact commands/stdout/stderr/rc for every invocation are in `/tmp/chousa-r25-FxMetaStrict-one-at-time.raw.log` (SHA-256 `fcb77e3515822973bdc0d681f99a59326ee54875ca9a35bfde893ce29bba74c5`). Concise output: `/tmp/chousa-r25-FxMetaStrict-audit.log` (SHA-256 `94c4933e41b89e49d92ca8f612c70e2080e05e4325d47d834fcf36f0787e34b3`).
- Fixture-directory reconciliation: normal and strict each report 27 META entries, 13/27 complete, and 19 findings; drift is 14 normal / 19 strict; both rc=1. The 5 info-only fixtures (`command-only-recheck`, `control-citation-fidelity`, `empty-recheck`, `root-parent-recheck`, `unrecognized-recheck`) retain complete=1/1 and their findings in both modes; strict changes verdict/rc to drift/1. Other fixtures match the README cells. This agrees with completeness defined as source present + verified-at dated + recheck present, independent of info drift (spec `round25-claims.md:36-40`; gate `research-gate.sh:2396-2457`).
- Counter attack (three scratch entries, only under `/tmp`): a complete entry with both info findings, a three-warning missing-key entry, and a NUL-refused entry. Normal summary `DRIFT (entries=3 complete=1 findings=6 drift=4)`, strict `DRIFT (entries=3 complete=1 findings=6 drift=6)`, `METADATA_COMPLETE=1/3`, rc=1. Thus META-line count, entry count, actual FINDING-line count, complete count, severity/strict drift count, and rc all reconcile; complete remains counted for the info-only entry even when strict marks it drift. Audit output lines 28–33 contain aggregate and counter results.

## Spec assessment, residual risk, verification gaps
- **Spec match:** yes for all 27 registered fixtures × both modes, plus the summary-counter attack; no divergence or ambiguity observed. The gate emits findings for each fixture as expected, and its counters reconcile against independently parsed META/finding lines.
- LSP status/references/definition/diagnostics were unavailable: `read xd://lsp` returned “No such tool.” Grep was used only to locate the mode; implementation was then read directly and exercised.
- Scope is the specified fixture set and the described scratch counter attack; no full selftest or broader fuzzing was run (not assigned). No installs.

VERDICT: No actionable `verify-metadata` operability defect found on full pin e93ac711f885a10d44fdd80a1734997419595b5a; tested fixture behavior and summary counters match spec v1.