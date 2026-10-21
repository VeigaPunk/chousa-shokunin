# FC1 falsification: control `nonrecord-mention-is-not-verdict`

- Item: `corpus/evidence/round27-regressions.py:85` (C1), lane `/home/vgpnk/Projects/shokunin/chousa-shokunin`, commit `dd72641e574679c4f7882dd43de072b4c8892d6f`.
- Gate sha256 at pinned commit: `ca39d14db907ec3fcf41ff0593658b4d6831fa82452944fe1f58463364992f84` (matches assignment).
- Sandbox: `/tmp/chousa-r27-falsify-FC1NonrecordMentionIsNotV05` (`git archive` of dd72641e). Base `64eec5d` gate extracted read-only for reference only.
- Author-lane advice, not outside admission.

## Verdict: FALSIFIED (scoped)

The control's expectation and its sensitivity to the targeted fault both hold. Its title and coverage do not: the name promises "nonrecord mention" in general, but the control only exercises mid-line text. Three adjacent C1 mutants pass all six C1 controls.

| # | Question | Result |
|---|---|---|
| 1 | Expectation derived from the contract, independent of gate code? | HOLDS for the tested input. The expected value is a literal, and mid-line text is not anchored, so usage passes. The title overreaches (CE1). |
| 2 | Reverting the targeted fix makes the control fail for the intended reason? | HOLDS. Substring revert (M1) and unanchored count (M2) both exit 1 with the helper running (`FAIL-case ... rc=2`), not a setup error (harness rc 2). Not unique: correct-usage-with-help fails identically. Unique catch: synopsis-exemption hack M4. |
| 3 | Nearby counterexample or vacuity | FALSIFIED: CE1 (title), CE2 (leading-whitespace anchor, M5 survives), CE3 (column-0 shape, M3 survives), CE4 (dead `_accepts`, Mdead survives), CE5 (non-anchored verdict tokens accepted; contract-consistent, intent gap). |

No contract-level false accept or false reject was found in the landed predicate. It equals `grep -c '^RESEARCH_GATE: '`, and it behaved as the contract requires on every tested input (see "No false negative found" under CE5).

## 1. Expectation provenance

- Harness line 85: `('nonrecord-mention-is-not-verdict', 2, usage + 'note RESEARCH_GATE: not a record\n', 0)`. Stub rc 2, expected helper exit 0 (accept). The `0` is a literal; no gate predicate computes it.
- Contract: `corpus/evidence/round27-claims.md:7` says "Count verdict records by anchored `^RESEARCH_GATE: `, not help-text substrings ... correct usage passes." A mid-line `RESEARCH_GATE:` is not anchored, so accept follows. The claims never list a nonrecord case; it is implied.
- Caveats:
  - `usage` copies the shipped synopsis (`Verdict: RESEARCH_GATE: CLEAN|DRIFT`, gate line 385). The input derives from gate text; the expectation does not.
  - The title over-generalizes. The contract excludes only non-anchored text. Column-0 non-verdict prose is a record under the contract (CE1).
  - Harness lines 73-78 extract both `metadata_asof_usage_accepts` and `metadata_asof_usage_case`. Line 89 invokes only `_case`. Line 69 claims "exact shipped usage helper ... not a duplicated predicate". Production `_accepts` (gate 6036-6040) has zero callers. `.ufo/waves/round-27/build/ExecUsage.md:19` says it is kept only so the extractor finds that name.

## 2. Mutation evidence

Single-line predicate edits in sandbox copies (`mut/`). Harness: `c1only.py`, which is regression lines 1-93 plus 225-237 (C1 block and summary only; C2/C3 not run). Command: `python3 c1only.py --gate <mutant> --output <json>`.

```
gate       edit (sandbox line)                                          rc  C1 mismatches (of 6)
LANDED     none                                                         0   0
M0copy     none (sha256 identical to landed)                            0   0
M1subst    6048 predicate back to base substring rule                   1   2: correct-usage, nonrecord
M2unanch   6047 count with unanchored grep                              1   2: correct-usage, nonrecord
M4synop    6047 count after removing the synopsis text
           nverdict=$(grep -c 'RESEARCH_GATE: ' <<<"${out//Verdict: RESEARCH_GATE: CLEAN|DRIFT/}" || true)
                                                                        1   1: nonrecord only
M6nochk    6048 drops the verdict count                                 1   2: reject-clean, reject-drift
M3shape    6047 count only ^RESEARCH_GATE: (CLEAN|DRIFT)                0   0 (survives)
M5indent   6047 count with leading-whitespace tolerance                 0   0 (survives)
Mdead      6039 (_accepts, never invoked) reverted to substring         0   0 (survives)
```

Intended-reason evidence for M1 and M2: the helper executed and printed `FAIL-case fixture rc=2 expected=expected diagnostic verdicts=N`. Harness rc 1 means mismatch, not setup error. In M1 the display shows `verdicts=0` because the mutant keeps the anchored count line for display; the decision used the substring rule.

## 3. Probe matrix

Helper `metadata_asof_usage_case` extracted verbatim from each gate. Stub prints the given bytes with rc 2 unless noted. ACC = helper accepts (exit 0), REJ = helper rejects.

```
probe                          LANDED M1subst M2unanch M3shape M4synop M5indent M6nochk Mdead
regr-correct-usage-with-help   ACC    REJ     REJ      ACC     ACC     ACC     ACC     ACC
regr-nonrecord-mid-line        ACC    REJ     REJ      ACC     REJ     ACC     ACC     ACC
regr-reject-clean-line         REJ    REJ     REJ      REJ     REJ     REJ     ACC     REJ
ingate-help-control            ACC    REJ     REJ      ACC     ACC     ACC     ACC     ACC
ingate-clean-control           REJ    REJ     REJ      REJ     REJ     REJ     ACC     REJ
ingate-drift-control           REJ    REJ     REJ      REJ     REJ     REJ     ACC     REJ
P-col0-prose-line              REJ    REJ     REJ      ACC     REJ     REJ     ACC     REJ
P-indented-DRIFT               ACC    REJ     REJ      ACC     REJ     REJ     ACC     ACC
P-CR-glued-CLEAN               ACC    REJ     REJ      ACC     REJ     ACC     ACC     ACC
P-unterminated-glued-DRIFT     ACC    REJ     REJ      ACC     REJ     ACC     ACC     ACC
P-NUL-glued-CLEAN              ACC    REJ     REJ      ACC     REJ     ACC     ACC     ACC
P-BOM-prefixed-CLEAN           ACC    REJ     REJ      ACC     REJ     ACC     ACC     ACC
P-tab-after-colon-CLEAN        ACC    ACC     ACC      ACC     ACC     ACC     ACC     ACC
P-invalid-utf8-CLEAN (C.UTF-8) REJ    REJ     REJ      REJ     REJ     REJ     ACC     REJ
P-crlf-verdict-CLEAN           REJ    REJ     REJ      REJ     REJ     REJ     ACC     REJ
P-two-anchored-verdicts        REJ    REJ     REJ      REJ     REJ     REJ     ACC     REJ
```

Real usage outputs fed through the shipped helper (`cat` stub): `asof-invalid`, `asof-missing`, `wrong-mode` all give LANDED=ACC, M3=ACC, M4=ACC, M5=ACC. Column-0 forms: `RESEARCH_GATE:CLEAN` (no space) and `RESEARCH_GATE_SELFTEST: ...` are ACC everywhere; `RESEARCH_GATE: CLEAN|DRIFT` at column 0 is REJ everywhere.

## 4. Counterexamples and vacuity

- **CE1 (title counterexample; gate correct by contract).** Input: `expected diagnostic` / `usage: fixture` / `RESEARCH_GATE: explains the verdict format` (rc 2). LANDED rejects. The title predicts accept. The contract says an anchored line is a record, so reject is right. The control name is only accurate for mid-line text.
- **CE2 (leading-whitespace anchor is unpinned).** Input: `expected diagnostic` / `usage: fixture` / `  RESEARCH_GATE: DRIFT` (rc 2). LANDED accepts (contract-consistent). M5 rejects. All six C1 controls pass under M5, so an anchor-loosening regression is invisible to the C1 set.
- **CE3 (column-0 shape is unpinned).** Input: `RESEARCH_GATE: explains the verdict format` at column 0. LANDED rejects; M3 accepts. All six C1 controls pass under M3.
- **CE4 (dead predicate is unexercised).** `_accepts` has no production callers and no harness invocation. Reverting its predicate (Mdead) leaves all six controls green, and the in-gate selftest does not call it either. The harness's "exact shipped helper" claim covers `_case` only.
- **CE5 (non-anchored verdict tokens accepted; intent gap, not a contract violation).** LANDED accepts these rc-2 outputs that contain the diagnostic:
  - `usage: fixture` + CR + `RESEARCH_GATE: CLEAN` (CR-glued)
  - `usage: fixture` + `RESEARCH_GATE: DRIFT` with no newline (unterminated, glued)
  - `usage: fixture` + NUL + `RESEARCH_GATE: CLEAN` (bash `$()` drops NUL with a warning, so the result is glued)
  - BOM-prefixed, two-space-indented, tab-after-colon, and mid-line `note RESEARCH_GATE: DRIFT`
  - The review oracle (`ReviewUsageVerdict.md:18`) says "no usage error may be accepted when it emits an actual verdict." Under the anchored contract these are not records, and the gate's own verdict parser (landed line 2863, `grep -m1 '^RESEARCH_GATE: '`) would not see them either. The control's own mid-line expectation (accept) encodes this policy without stating it.
  - Structural reason: any token-level rule counts the synopsis, because `Verdict: RESEARCH_GATE: CLEAN|DRIFT` contains `RESEARCH_GATE: CLEAN` (M2 shows correct usage failing). Keeping the synopsis without special-casing (M4) forces anchoring, and anchoring accepts glued tokens. The alternative is to change the synopsis so the token never appears.
  - No false negative found: invalid UTF-8 before an anchored verdict is REJ under C, C.utf8, en_US.utf8 and C.UTF-8. CRLF, verdict-first and two-verdict inputs are REJ.

## 5. Reachability in shipped output

- `usage()` heredoc (gate 303-387): no line begins `RESEARCH_GATE:`. The only mention is the synopsis at 385, mid-line.
- `die_usage` (390) writes `research-gate: ...` and usage, both newline-terminated.
- All seven verdict format strings (1050, 1473, 1760, 2112, 2301, 2802, 3059) start `RESEARCH_GATE: ` at output column 0 and end in `\n`.
- Real usage runs on the landed gate: `verify-metadata corpus/README.md --root . --as-of 2026-02-30` rc 2, 0 anchored lines, diagnostic present. `verify-metadata ... --as-of` (missing) rc 2, 0 anchored lines. `verify corpus/README.md --as-of 2026-10-21` rc 2, 0 anchored lines. All three contain the mid-line synopsis.
- Residual negative substring predicate on `RESEARCH_GATE` in the landed gate: none. Only positive token checks remain (6352, 6355). The base gate had one (6016), so the fault class is removed.

So CE2 through CE5 are latent, not reachable from current shipped output.

## 6. Advice to the author lane

1. Rename the control to what it tests (`midline-mention-is-not-verdict`), or add column-0 counterparts: anchored prose must REJECT (kills M3) and an indented verdict must ACCEPT (kills M5).
2. State the policy for non-anchored verdict tokens as an explicit control (glued, mid-line DRIFT, BOM, NUL), citing the anchored rule beside it.
3. Use one predicate: have `metadata_asof_usage_case` call `metadata_asof_usage_accepts`, or delete `_accepts` and retarget the extractor. Then the harness exercises what production runs, and Mdead is caught.
4. M4 passes every in-gate usage control and the three real usage cases (helper-level replay). Only the independent nonrecord control catches it. Consider mirroring that control in the in-gate selftest.
5. Keep `usage()` free of column-0 `RESEARCH_GATE:` lines. A grep guard in selftest would make that structural.

## 7. Limits

- Only the C1 block ran, through a derived `c1only.py`. Full `--selftest` and the full regression script were not run, per assignment.
- The in-gate selftest usage block was not executed. M4 passing it is inferred from helper-level replay of the five in-gate control strings and the three real outputs.
- Probes used printf-escape stubs and `cat` of real outputs. Locale checks covered invalid UTF-8 and mid-line text under C, C.utf8, en_US.utf8 and C.UTF-8 only, not the full battery under each locale.
- Reverts were done by editing one predicate line in sandbox copies. The base gate was not run, because it has no `_accepts` extractor target, so the harness cannot run on base.
- Git was used read-only (`archive`, `show`, `cat-file`). No lane file was edited; this report is the only lane write. Sibling reports in `falsify/` were not read.

## 8. Commands and exit codes (key)

- `git -C <lane> archive dd72641e... | tar -x -C <sandbox>` -> exit 0
- `git -C <lane> show dd72641e...:tools/research-gate.sh | sha256sum` -> `ca39d14d...92f84`, matches assignment
- `git -C <lane> show 64eec5d...:tools/research-gate.sh > base-research-gate.sh` -> 6351 lines (reference)
- `python3 c1only.py --gate tools/research-gate.sh` -> exit 0, C1 6/6, 0 mismatches
- Mutants (see table in section 2): exit 1 for M1, M2, M4, M6; exit 0 for M0copy, M3, M5, Mdead
- Real usage commands (section 5): exit 2 each
- `grep -c '^RESEARCH_GATE: '` on raw bytes, LC_ALL=C and C.UTF-8: invalid UTF-8 + CLEAN -> 1; CR-glued -> 0; BOM -> 0; indented -> 0; tab -> 0; NUL-then-verdict on its own line -> 1; unterminated-glued -> 0

## 9. Tools

None installed or updated. Used: host bash, python3 standard library, GNU grep, git (read-only).

## 10. Erratum (appended after write; no other text changed)

- Section 5, residual-predicate bullet: the search matched only line 6352 (positive token check). Line 6355 was grep context, not a match, so "(6352, 6355)" should read "(6352)".
- Verdict table, row 2: "(harness rc 2)" denotes the setup-error exit code. The observed harness exit for M1 and M2 was 1 (mismatch), as stated in section 2.
