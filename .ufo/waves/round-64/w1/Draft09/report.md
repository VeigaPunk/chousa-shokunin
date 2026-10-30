# Draft09 — index-rule-v3 knowledge draft

## Behavior, provenance and axes

Documentation-only seat; advisory to L1, not production integration or independent claim closure. Axes: fidelity to the frozen contract, separation of normative rules from observed behavior, and auditability. No numeric operability improvement is asserted.

Authority: `corpus/evidence/round64/claims.md`, read locally, especially lines 47–61 (contract), 89–104 (kill rule and limits), and 263–266 (frozen digests). Assignment identifies freeze commit `bf40d99bda9eefdad3ed6276da077cfb24ba82f1`; this seat did not independently resolve that commit. The document itself identifies census-start base `759c6cbef4cf9cdc81b68afc709f3b82ecd1a9d9`; those are different provenance roles, not interchangeable revisions.

The following is a proposed entry for L1 consideration at `corpus/knowledge/index-rule-v3-r64.md`. It has NOT been written there, admitted, or measured as implemented.

---

source: corpus/evidence/round64/claims.md lines 47–61, 89–104; corpus/evidence/round64/controls/c1v3-before-full.txt lines 27–44; corpus/evidence/round64/claims-erratum.md lines 3–6
reviewed-at: 2026-10-30; local contract/source/receipt reading only, not runtime verification
recheck: on G02 implementation or contract change; preserve the frozen instrument and distinguish any supplemental instrument

# G02 v3: index membership is a two-direction contract

## Question

What must the lane's knowledge-index gate establish, and what does a contract description not establish?

## Frozen rule, not an observed implementation

The round-64 contract requires all five clauses below. These are normative requirements for the proposed production amendment; they are not a claim that the currently landed tool or candidate satisfies them.

1. **Walk and admissible entries.** Recursively walk `corpus/knowledge/`. Every non-directory entry must be a regular file whose name ends in case-sensitive `.md`, except that `.gitkeep` is permitted. Judge symlinks by their targets: a symlink to a regular `.md` file passes the type condition; dangling and non-file symlinks fail. A missing knowledge path, a path that is not a directory, or one not readable and searchable by the running uid fails. Zero `.md` entries also fails; an empty walk is not success.
2. **Normalize before matching.** Remove `~~…~~` strike spans from `corpus/README.md`. Unescape the five specified Markdown escapes: backslash-underscore, backslash-asterisk, backslash-left-bracket, backslash-right-bracket, and backslash-backtick. Unquote percent-encoding in link targets. NFC-normalize both the README side and file-name side. This is the frozen normalization list, not a general Markdown-parser specification or authorization to decode every percent sign in prose.
3. **Forward membership.** A file counts as indexed exactly when the normalized README matches `(?<![\w.-])(?:knowledge/)?NAME(?![\w-])`, with NAME being the file's complete name INCLUDING `.md`. NAME denotes the literal filename, not regex syntax supplied by that filename. The `knowledge/` prefix is optional. Matching only `p.stem` implements a different rule.
4. **Reverse membership.** Every whole-token `knowledge/…/<NAME>.md` occurrence in the normalized README must name an existing regular `.md` file under `corpus/knowledge/`. A phantom path fails even when all real files have their own forward matches. The forward test is name-based; the reverse test binds a knowledge-shaped occurrence to a real path. Neither direction replaces the other.
5. **Invocation and output.** An existing non-directory supplied as `--work` requires usage exit 2, no GATE or summary line on stdout, and the offending path on stderr. A reported filename containing invalid UTF-8 must be printed backslash-replaced, preserving strictly UTF-8-decodable stdout. Sanitizing its display does not make an otherwise invalid or unindexed entry pass.

## Boundary consequences and limits

The following are deductions from the frozen wording, NOT executed probes:

- A basename-only mention may satisfy the forward check: the prefix is optional. This does not make bare phantom names subject to the reverse check, which only covers `knowledge/…`-shaped occurrences.
- A sentence-final `NAME.md.` may match because the right boundary excludes word characters and hyphen, not dot. A preceding word character, dot, or hyphen blocks the left boundary. The two boundaries are intentionally asymmetric.
- File extensions remain case-sensitive; NFC normalization does not promise case folding.
- The contract removes strike spans but does not specify removing all code spans or URLs before matching. Do not advertise URL-only or code-span-only exclusion as an implemented or frozen rule. The claims' D3 coverage limit explicitly says those variants are represented only by E05's struck-row class fixture.
- E14 pins an NFC filename with NFD index spelling, not the reverse direction; the frozen suite is not exhaustive Unicode coverage.
- Recursive scope does not establish path-unique forward coverage for colliding basenames; forward matching is expressed in terms of a file's name. Do not silently replace it with a stricter path-only rule.
- The frozen prose does not spell out every parsing, recursion-cycle, or containment edge case. This entry does not settle such ambiguities by inventing new gates.

## Observations and rejected inferences

**Observed by reading an existing receipt, not by rerunning:** `corpus/evidence/round64/controls/c1v3-before-full.txt` ends with `CLEAN=1/1 DEFECTS=17/28 BENIGN=8/11 ZERO=3/3 BATTERY=FAIL`. The frozen claims attribute exit 1 to this before run. E12 and E13 each read `benign FAIL rc=1 want 0`; E14 also fails in this before receipt. This is historical before-tool evidence, not a new candidate measurement.

**Observed source defect:** frozen `c1-battery-v3.py` lines 386–394 call `tag()` independently for each E12/E13 created filename and its README link. The fixture therefore does not ensure those names agree. `claims-erratum.md` explicitly records the conflict: “C1's statement that E12/E13 are benign fixtures is false for the frozen bytes: each invokes tag() independently for the created filename and README link.” The same erratum states: “The restored frozen battery is still the measurement authority, so no supplemental pass admits C1.” A conforming checker should reject a mismatched fixture's unindexed file and phantom link; do not weaken membership checks to make that fixture pass.

The inherited `corpus/evidence/round64/controls/ref-preflight-v3.py` is a candidate, NOT production. The distinct `corpus/evidence/round64/c1-battery-supplement.py` is post-freeze supplemental work, NOT the frozen counter. A candidate docstring, a supplemental PASS, or this entry cannot establish the frozen C1 full-pass predicate. No candidate or supplemental execution is claimed here.

## Gate — documentary admission only

| Evidence | Access | Admit/reject | Scope |
| --- | --- | --- | --- |
| Frozen claims lines 47–61 | 2026-10-30, local read | Admit | Authority for the normative five-clause contract only. |
| Frozen before receipt lines 27–44, paired with claims lines 67–76 | 2026-10-30, local read | Admit | Existing recorded before failure; no new execution. |
| Frozen battery lines 386–394 and attempt2 erratum lines 3–6 | 2026-10-30, local read | Admit | Fixture-name mismatch and explicit separation of frozen versus supplemental instruments. |
| Candidate documentation or proposed entry as proof of implementation | 2026-10-30, contract-only reasoning | Reject | Requirements and descriptions are not execution receipts. |
| Supplemental result as satisfaction of frozen C1 kill rule | 2026-10-30, claims lines 89–93 and erratum line 5 | Reject | Different instrument cannot replace the unmodified frozen battery. |

This Gate is a proposed documentary evidence table, not an external non-author closure verdict or a new source-registry admission.

---

## Gates, commands and outcomes for this seat

No shell commands, bounded probes, test runs, builds, candidate invocations, counter runs, or other runtimes were executed. Command/output/exit: **not applicable** to this documentation-only assignment. All evidence above came from successful `read`, `glob`, and `grep` tool operations; those operations do not expose process exit codes. No output has been promoted into a fresh execution receipt.

Read sequence began with `/home/vgpnk/.omp/agent/RULES.md`, then frozen claims and `skill://godspeed` in an independent batch. Additional local reads covered the existing lane-root knowledge-entry convention, frozen before receipt, supplement header, frozen E12/E13 source, erratum, and `skill://agent-self-evaluation`. Searches located the candidate/supplement and existing fixture-mismatch references. No external sources were fetched.

Tools installed or updated: none; version/channel/reason not applicable. No service action, package transaction, PATH write, git/jj command, clone, scratch directory, or temporary fixture was needed. Scratch cleanup is not applicable: this seat created no scratch artifacts or live clone.

## Touched surfaces and path conflict

Only own-seat report artifacts are written. Production, frozen claims, counters, operator inputs, and sibling output remain untouched.

Assignment paths conflict verbatim:

- “Write only your own report and evidence beneath /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-64/w1/Draft09/ (report.md)”
- “Report: write your scoped findings to .ufo/waves/round-64/w1/Draft09.md”

The full report is at the scoped folder path; the explicitly named trailer path contains a pointer and scoped summary. Both are unique Draft09 output surfaces. No judgment of this conflict is asserted; the canonical Rust judge retains authority.

## Out of scope and limits

No integration, source-registry change, production correctness verdict, C1 admission, implementation repair, fresh measurement, or score change. The historical before-run exit is attributed to the frozen claims rather than independently witnessed by this seat. L1 alone integrates the proposed entry. Entry/source admission and frozen claim closure intentionally remain unchanged.

## Self-evaluation

Accuracy 4/5: line-linked contract/source/receipt evidence; freeze commit identity was supplied rather than independently resolved. Completeness 4/5: all five clauses, limits, observations and proposed Gate included; intentionally no runtime evidence. Clarity 4/5: draft and seat report are separated, but the artifact is longer than an integrated entry should be. Actionability 4/5: L1 can extract the delimited entry without adopting its normative prose as a PASS. Conciseness 4/5: exact conflict and evidence-status repetition are retained for auditability. Mean 4.0/5. Highest-impact editorial improvement at integration: preserve status labels while removing duplicated seat-only provenance. Would the user agree? Expected yes for a documentation-only draft; no execution or closure is claimed.

Report: .ufo/waves/round-64/w1/Draft09.md
