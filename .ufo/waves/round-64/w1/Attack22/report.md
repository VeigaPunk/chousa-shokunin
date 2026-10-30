# Attack22 — round64 attempt2 — G04/G05 no-harm review

Axes: preserve G04/G05 defect detection; preserve benign acceptance; distinguish frozen claim evidence from supplements.

## Findings, by severity

### Medium, inherited limit: G04 silently drops a missing top-level path

`corpus/evidence/round64/controls/ref-preflight-v3.py:191-192` and `tools/lane-preflight.py:196-197` discard slash-bearing words whenever their first path segment does not exist. Minimal SHONEN content: `` `absent-dir/missing.md` ``. With no `absent-dir`, all three tested versions print `GATE G04 shonen-pointers PASS 0 pointers resolve`, and selected-gates summary `PREFLIGHT=2/2 FAILED=none ENV=none SKIPPED=G01,G02,G03,G06,G07,G08`, exit 0. Thus removal of a whole first directory makes its SHONEN references disappear from detection. This is an inherited lexical classification limitation, **not a round64 regression**: the frozen implementation has exactly the same behavior. Do not treat it as evidence that the G02 amendment harmed G04, nor silently broaden the frozen rule to fix it.

### No newly introduced G04/G05 harm found

Read-only comparison against freeze `bf40d99bda9eefdad3ed6276da077cfb24ba82f1` shows identical ASTs for `read`, `path_words`, `g04`, `cap_pointers`, `brace_expand`, and `g05` in both inherited candidate and current working tool. Caller inspection: candidate `FUNCS` line 262 dispatches these same gates, `main` lines 297-317 preserves selection, exception-to-FAIL, summaries and exit precedence; working tool equivalents are lines 267 and 302-322. The diff changes G02/imports and the non-directory `--work` usage check, not the pointer gates. Candidate remains a candidate; a modified working file is not proof of admission or production integration.

## Frozen C1 versus supplement

Frozen `claims.md:78-91` requires three full unmodified-battery PASS runs plus null/v2 checks. Frozen `c1-battery-v3.py:386-394` draws independent random names for each E12/E13 file and its README reference. Those are mismatched fixtures, not valid benign inputs. The known frozen C1 failure is retained honestly: the stated frozen PASS requirement is not repaired by a supplement. I did not rerun the user-reported failure.

`c1-battery-supplement.py:386-396` instead binds one `t = tag()` per leg and reuses it for both names. That is a distinct post-freeze supplemental instrument, not the frozen counter. Neither instrument changes G04/G05 behavior. The probe confirmed frozen claims and frozen v3 battery are byte-identical to the specified freeze. No full battery PASS is claimed here.

## Bounded probe evidence

Command (exit **0**):

`python3 -B /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-64/w1/Attack22/probe.py`

The retained driver records every child argv, stdout, stderr and exit to stdout. It extracts frozen bytes read-only using `git show`, creates only tiny seat-owned fixtures, executes 15 bounded CLI runs in a six-worker pool, and removes its scratch in `finally`. No clone or git mutation. All child stderr was empty.

| Fixture | Frozen / candidate / working exits | Identical relevant output in all three |
|---|---|---|
| Existing SHONEN line suffix and SCORECARD trailing-dot/brace paths | 0 / 0 / 0 | `G04 ... PASS 2 pointers resolve`; `G05 ... PASS 3 capability pointers resolve` |
| Second SHONEN path missing, first present | 1 / 1 / 1 | `GATE G04 shonen-pointers FAIL 1 unresolved: corpus/missing.md`; `FAILED=G04` |
| Missing second member in SCORECARD brace shorthand | 1 / 1 / 1 | `GATE G05 scorecard-paths FAIL 1 unresolved: tools/missing.py`; `FAILED=G05` |
| Missing top-level SHONEN path | 0 / 0 / 0 | `GATE G04 shonen-pointers PASS 0 pointers resolve` |
| SHONEN and SCORECARD both absent | 1 / 1 / 1 | `G04 ... FAIL SHONEN.md absent`; `G05 ... FAIL SCORECARD.md absent`; `FAILED=G04,G05` |

Observed tool SHA256:

- Frozen tool: `7e9427785db117e2996fe23134ab5c9357ea793d25efabb5cb5159e4ca79d460`
- Inherited candidate: `0b4da0d2128e23b4feeb82bb179ec6a89277a1f0a0aa1c7115e3ae38966f185e`
- Working tool snapshot: `3d792f0961434ccd76ef87ccb0b2dcccc022f6f84d958dbc4e35e6f4c260a89d`

Final driver output: `BYTE_EQUAL_FREEZE corpus/evidence/round64/claims.md True`; `BYTE_EQUAL_FREEZE corpus/evidence/round64/c1-battery-v3.py True`; `SCRATCH_REMOVED True`.

## Residual risk and verification gaps

- `xd://lsp` discovery returned `No such tool`; no semantic server/status/references/definition/diagnostics device was available. Text fallback is not presented as semantic proof; AST comparison and actual CLI outputs are separate evidence.
- Review is scoped to G04/G05. No full battery, G08, sibling-corpus sweep, resume, runtime routing or saturation measurement was performed or inferred.
- Existing lexical boundaries (including the observed first-segment omission) are not comprehensive filesystem-reference validation. These five fixtures are not a saturation claim.
- No source, operator input, frozen claim/counter or sibling output was modified. No package installs/updates, network fetch, service restart, commit or push. Used installed Python 3.14.8, not an installed tool change.
- Scratch `/fast/scratch/hyaku/chousa-r64/Attack22/` was removed before reporting. Evidence and reports only remain in assigned seat output paths.

Advisory recommendation: no G04/G05 regression objection at these bytes; preserve frozen C1 failure and label supplemental evidence separately. Only L1 may decide integration/closure.

Self-evaluation: accuracy 4 (bounded CLI/AST evidence, not exhaustive); completeness 4 (scoped gates covered, full battery deliberately not repeated); clarity 4 (frozen failure separated from inherited limit); actionability 4 (precise branch and counterexample); conciseness 4 (full argv retained in driver instead of duplicating 15 logs). Mean 4.0. Improvement: L1 should attach its canonical full-battery receipts for closure; this report cannot substitute for them. User-agreement self-check: recommendation is explicitly advisory and makes no admission claim.
