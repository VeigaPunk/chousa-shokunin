# Round-25 residual final-measures review

Scope: working-tree diff for `round25-measure.sh`, `round25-meta-differential.sh`, and `round25-holds/battery.sh`, against the frozen claims and FxCritC2/FxCritC3. Static review only; no suites or runtimes were run.

## Findings by severity

### Medium — Claim 3's counter is stronger, but 3b remains deletion-sensitive

The follow-up at `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round25-measure.sh:71-98` closes several previously identified false-pass paths: 3a now requires the recount command if the old phrase is absent (`:71-74`); 3c requires exactly one raw token, the exact historical line, and the disposition marker after the appended preservation-correction heading (`:83-88`); 3d rejects missing/short addendum bodies and requires an `E<n>` and `case(s)` token (`:89-93`).

One substantive deletion path remains: 3b only compares tuple/queue strings that still occur in `SKILL.md` (`:77-82`). Deleting all those summaries leaves empty `sk_t`/`sk_q` sets and yields zero without requiring the promised current summaries to remain. The 3d content check is also lexical (length plus tokens), not evidence/pointer validation. The exact GSHA historical line is presently restored at `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/hardening-r10.md:488`, but the script's exact-line test does not require that text to remain in the Round-13 section; it protects the current representation, not byte-for-byte placement against a future relocation.

The prior live-stale-README finding is resolved: `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/README.md:284-288` now explicitly labels the old tuple/queue as a Round-10 handoff snapshot, points to the current hardening-r10 owner and recount command, and says the original snapshot is retained as history. The earlier paragraph's old values are no longer presented as current.

### Medium — Claim 2's 43-row counter is now deletion/duplicate sensitive, but its zero is not a complete index-validity check

The fixed `expected_receipts` map at `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round25-measure.sh:38-48` compares each expected filename's observed heading list to exactly `[round]`. Consequently a missing expected row, duplicate occurrence, or wrong/multiple heading is counted. This closes FxCritC2's specific deletion/duplicate blind spot for rows recognized by the parser.

Residual limitations: the parser recognizes only rows matching `^\| ` plus a backticked first cell (`:40-47`); it does not validate nonempty Shows/Key-result cells or that the indexed receipt file exists. The other C2 terms also remain weaker than the registered re-derivation claim: 2a uses path-substring membership rather than a unique parsed row (`:31-33`); 2b accepts only a `Round N` heading regex (`:34-36`); and 2d accepts any four-cell numeric-round row under a Capabilities heading (`:49-60`). The claimed round set is now frozen by the assertion at `:51`, but row identity/pointer content is not checked. Thus zero is stronger for 2c than before, but not proof that every C2 index entry is valid and re-derivable.

### Medium — `round25-measure.sh` exit 0 is completion, not an acceptance verdict

`set -euo pipefail` now propagates selftest-pipeline and drift failures (`/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round25-measure.sh:8,91-93`), and the metadata-mode status is captured and printed. However, the script does not fail when that captured status/output differs from the prediction, and the final exports probe prints `VERDICT_BEARING_EXPORTS=N/3` without returning nonzero when `N != 3` (`:94-95`). Therefore an exports result of 0/3 can coexist with script exit 0 (assuming the subprocess calls themselves do not raise). Treat this script's exit as successful measurement execution, not as proof the registered claims/holds pass.

By contrast, `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round25-meta-differential.sh:38-43` now exits nonzero for an observed disagreement, and `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round25-holds/battery.sh:47-69,91` records command status, compares it with the baseline, and returns failure for missing baselines or diffs. Those exit paths are honest for the populations they actually compare.

### Low — Commands are not uniformly placement-independent

The follow-up adds duplicate-row rejection and requires exactly 27 fixture rows with table names equal to the on-disk `.md` fixture names (`/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round25-meta-differential.sh:20,26-27`), closing the simple README-row deletion/duplicate shrink path. The script remains lane-root-relative as documented. The set is checked against the mutable on-disk inventory rather than an immutable expected-name/digest list, so coordinated replacement of both fixture and table remains outside this check.

`battery.sh` is cwd-independent once given usable tree/analysis roots: it derives baselines from `BASH_SOURCE` and changes to `TREE_ROOT` for commands (`/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round25-holds/battery.sh:8-14,37-46`). `round25-measure.sh` changes to its supplied tree root (`:9-10`), but its documented command uses a relative script path despite saying “from anywhere” (`:2-5`); from outside the lane, callers need to supply a reachable/absolute script path.

## Confirmed corrections

- **43-row identity counter:** yes, the new fixed expected-name/round comparison detects omitted and duplicated recognized rows, as well as misplaced rows.
- **GSHA history:** yes. `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/hardening-r10.md:488` has the original `${GSHA}` line restored, and lines 698-715 append an explicit preservation correction and `R25-GSHA-DISPOSITION` explaining that the old token is superseded data. The C3 counter now requires one raw token, that exact historical line, and the marker after the appended correction heading; it does not pin the exact line's Round-13 section location.
- **Other exit paths:** meta-differential and battery now return nonzero for measured disagreement/diff. The measurement script remains a reporting harness rather than an aggregate pass/fail gate, as described above.

## Residual risk and verification gaps

- No suite was rerun, per assignment; this review does not independently revalidate build68/falsify68 or assert current runtime outputs.
- `xd://lsp` was unavailable (`No such tool: xd://lsp`; absent from the mounted device list). I used targeted file reads for semantic review; text search was only used to locate references.
- The remaining C2/C3 weaknesses above are measurement false-pass risks; the inspected working tree does contain the explicit GSHA correction and the C3 addenda, but the counter does not prove their full acceptance criteria.

Installs: none.

## Follow-up integration disposition (static review)

- Accepted: the README snapshot qualification, strengthened GSHA/3a/3d guards, and the differential's duplicate/27-row/table-to-file guards address the corresponding specific false-pass findings above.
- Still open: C3's 3b deletion path; C2 2a/2b/2d syntax-only checks and 2c's lack of nonempty-cell/backing-file checks. Those counts require retained manual evidence review and must not be treated as self-authenticating acceptance.
- Exit and placement conclusions are unchanged: `round25-measure.sh` remains a counting probe whose rc 0 is not a verdict; the differential still requires lane-root cwd; the battery compares against its configured tree/analysis roots.
- I did not run suites or isolated negative controls, and do not claim their results. LSP remains unavailable as recorded above.
