# Attack15 — C2 duplicate versus unknown-rule parsing

Axes: calibration (mutation discrimination), correctness (invalid-rule refusal), provenance (frozen versus supplemental evidence).

## Counterexample

The frozen A10 patch changes `len(cols) != 6 or cols[1] not in RULES` to `len(cols) != 6 and cols[1] not in RULES`. It does **not** change duplicate-id detection. Consequently C7, described as the A10 discriminator, rejects the same duplicate fixture identically before and after A10. A single six-column unknown-rule row distinguishes them:

```text
R1<TAB>not-a-rule<TAB>anchor line one<TAB>S.md<TAB>## R|x<TAB>unknown
```

Claims contain `anchor line one`; S.md contains `## R`, `x`, `y`. Frozen checker: exit 1, empty stdout, stderr `claims-audit: bad rule row unknown.tsv:1`. A10 checker: exit 0, stdout `FLAGGED=0/1 AUDIT=PASS`, empty stderr. Both reject duplicate ids, including ids equal after stripping surrounding whitespace, with exit 1 and stderr `claims-audit-v2: duplicate rule id`. Both accept the valid section-contains control with exit 0 and `FLAGGED=0/1 AUDIT=PASS`.

## Evidence and frozen comparison

Executed bounded command (exit 0):

```sh
python3 -B /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-64/w1/Attack15/probe.py
```

`Attack15/evidence.json` records all eight exact commands, exits, stdout/stderr, Python version and SHA256 comparisons against `git show bf40d99bda9eefdad3ed6276da077cfb24ba82f1:<path>`. Current checker, generator and runner exactly equal frozen bytes; prefixes match claims: `db0e28dd4c033259`, `6e1055b28d315e32`, `0045787ee9de3974`. Reproducer and TSV inputs are retained under `Attack15/`. Scratch was removed in `finally`; no clone or git mutation was used.

Source evidence:
- `tools/claims-audit-v2.py:99–112`: unknown-rule check and independent duplicate-id check.
- Same file `351–360`: C7 exercises duplicates only; no unknown-rule fixture.
- `gen-audit-mutants.py:64–66`: exact A10 patch.
- `c2-mutrun.py:148–163`: R1 selftest, R2–R4 receipt audits, R5 old probe, R6 fault, R7 first-commit fixture; no direct malformed-rule leg.
- `round63/audit-probe.py:66–120`: valid named rules, not unknown-rule rejection.

**[INFERENCE]** A10 survives the frozen v2 matrix whenever its unmutated baseline legs meet their expectations: its only changed behavior concerns malformed/unknown rows, absent from those fixtures, and C7 remains unchanged. This is a defect in the frozen C2 discriminator, not merely a new beyond-twelve mutant or supplemental weakness. The unconditional observed claim here is narrower: the exact C7 fixture fails to discriminate the exact frozen A10 patch. I did not execute the full matrix/selftest because those drivers create git repositories and commits, forbidden by this seat assignment. No full `AUDIT_MUTANTS_KILLED` result is fabricated. The named after-receipt `controls/c2-mutrun-v2.txt` was absent when read.

The production checker itself correctly rejected all assigned duplicate/unknown forms tested. Separately, its docstring calls usage/IO errors exit 2, while malformed rows currently exit 1 via string-valued SystemExit; the observed behavior is recorded, not silently repaired.

## Smallest safe correction

Keep all frozen rules and bytes unchanged. L1 should record the C7/A10 discriminator failure honestly; a separately named post-freeze supplement or next-round instrument can add the six-column unknown-rule leg, expecting nonzero and `bad rule row` on stderr. Preserve C7 as independent duplicate-id coverage. A supplemental success must not be relabeled as the frozen C2 12/12 receipt. Canonical closure remains outside this advisory review.

C1's frozen E12/E13 independently generated filename/link mismatch remains an honest frozen failure, as disclosed in `claims-erratum.md:5`. `c1-battery-supplement.py` is a distinct post-freeze repair and cannot admit frozen C1. This seat neither reran nor repaired C1.

Tools: installed Python 3.14.8 and existing git (read-only `show`); no installation/update, network access, service action, production edit or frozen edit.

Self-evaluation: accuracy 4/5 (full-matrix survival explicitly inferred, not observed); completeness 4/5 (bounded parsing scope complete; prohibited commit-producing drivers omitted); clarity 4/5 (fixture and exact outputs separated from inference); actionability 4/5 (specific independent unknown-rule supplement); conciseness 4/5 (provenance detail retained for replay). Mean 4.0. Highest-impact improvement for an authorized integrator: obtain the frozen full-matrix receipt without changing its inputs. Would the user agree? Evidence supports the narrow counterexample, not an invented closure verdict.
