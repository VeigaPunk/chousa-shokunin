# Attack16 — C2 summary/stdout consistency

Axes: calibration (honest summary), operability (consumer-visible stdout), evidence fidelity (frozen versus supplemental).

## Findings, severity ordered

### Medium — supplemental weakness: contradictory extra summary is accepted

`corpus/evidence/round64/c2-mutrun.py:151–155` checks `needle in p.stdout`, plus existence of any FLAG line for v2 R2. It does not require exactly one summary, a full-line match, or consistency between the FLAG count and every summary. The frozen text calls these “exact output lines” (`corpus/evidence/round64/claims.md:180–181`), which overstates this implementation's validation strength.

Minimal fresh mutant: retain `tools/claims-audit-v2.py:208` unchanged and append `print("FLAGGED=999/999 AUDIT=PASS")` immediately afterward. On the actual frozen R2 receipt, the checker exits 1 and prints two real FLAG lines followed by:

```
FLAGGED=2/2 AUDIT=FAIL
FLAGGED=999/999 AUDIT=PASS
```

The runner's exact R2-v2 predicate evaluates **True**, despite two incompatible summaries. Original bytes print only the first summary; the frozen A09 mutation instead prints `FLAGGED=0/2 AUDIT=FAIL`, and that same predicate evaluates **False**. Thus the frozen A09 class is genuinely caught in this leg; the fresh duplicate-summary variant exposes a broader consistency gap, not failure of the frozen twelve-mutant criterion.

Recommendation to L1: route a new summary-uniqueness/count-consistency mutant and parser invariant to a separately named future supplement; do not edit this frozen runner or extend C2's frozen acceptance set retroactively.

### Informational — original stale-anchor stdout says PASS while exit is 2

A one-row TSV with an absent anchor produces, on unmodified committed v2 bytes:

```
AUDIT_STALE R anchor not in claims file
FLAGGED=0/1 AUDIT=PASS
```

Exit 2; stderr empty. This follows `tools/claims-audit-v2.py:199–209`: stale rows increment `stale`, not `fired`, and PASS depends only on `fired`. It is not a newly falsified frozen contract: the documented PASS condition is zero fired rules, and the stale exit remains 2. Consumers must not treat `AUDIT=PASS` alone as successful validation. A future distinct instrument could make error status explicit, but this report does not rewrite the contract.

## Executed evidence

Command (cwd `/fast/scratch/hyaku/chousa-r64/Attack16`):

```
python3 -B /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-64/w1/Attack16/probe.py
```

Driver exit **0**. Python **3.14.8**, existing system binary `/usr/bin/python3`; no tool installed or updated. Reproducer retained at `Attack16/probe.py`. Each child command is bounded at 30 seconds and prints command, stdout, stderr, exit and the R2 predicate result. Actual results:

| Case | Child exit | Relevant stdout | R2-v2 predicate |
|---|---:|---|---|
| Original R2 | 1 | two FLAG lines; `FLAGGED=2/2 AUDIT=FAIL` | True |
| Frozen A09 R2 | 1 | same two FLAG lines; `FLAGGED=0/2 AUDIT=FAIL` | False |
| Fresh duplicate-summary R2 | 1 | same FLAG lines; honest summary then `FLAGGED=999/999 AUDIT=PASS` | True |
| Original absent-anchor fixture | 2 | `AUDIT_STALE R anchor not in claims file`; `FLAGGED=0/1 AUDIT=PASS` | not evaluated |

All child stderr was empty. Receipt children use the exact absolute R2 claims/audit paths from `c2-mutrun.py:89–91` and absolute lane `--root`; the absent-anchor fixture uses only seat scratch. The probe makes no git mutations, clone, network request or production change.

Byte comparison commands (lane cwd), all exit **0**:

```
git show bf40d99bda9eefdad3ed6276da077cfb24ba82f1:tools/claims-audit-v2.py | sha256sum
sha256sum tools/claims-audit-v2.py corpus/evidence/round64/c2-mutrun.py corpus/evidence/round64/gen-audit-mutants.py
```

Frozen-commit and inherited checker hash are identical: `db0e28dd4c0332591b8898feb727f23a0e80b6e2ad29cbf0a6237d35a4d0b88d`. Inherited runner hash `0045787ee9de39749e1dd06739259cd5f0a494865c921edbed91cfd86249a8c9`; generator `6e1055b28d315e32a3d43ee0866f9c32b78470899826f1d29c8c3707610a4191`; both match the prefixes frozen in claims lines 264–266.

## Classification and verification gaps

No C2 frozen-claim failure demonstrated. No claim that the fresh mutant survived a complete matrix run: only the actual R2 predicate was exercised. Static reading finds the other matrix/selftest assertions use output-presence checks, but that is not a measured full-survival result. Full matrix/selftests were not invoked because they create git repositories/commits and are outside this bounded stdout item. No canonical runtime/rerouting/resume path exists in the inspected C2 checker/runner scope; no saturation inference is made from this probe.

LSP device unavailable: `read xd://lsp` returned “No such tool”; hence no answering server/status/references/definition/diagnostics were available. Text search and line reads were a literal fallback, not semantic-reference proof.

C1 remains separate: the assignment reports frozen E12/E13 independently drawn fixture-name mismatch, and `c1-battery-supplement.py` is post-freeze repair, not the frozen battery. This seat did not rerun or repair C1 and does not convert that failure into PASS. `ref-preflight-v3.py` was not treated as production.

Scratch removed before handoff; no clone created. Advisory only, not admission or closure.

Self-evaluation: accuracy 4/5 (actual R2 evidence, no whole-matrix survival claim); completeness 4/5 (bounded summary scope, whole-matrix run intentionally absent); clarity 4/5 (frozen versus supplemental separated); actionability 4/5 (specific future invariant, no frozen edits); conciseness 4/5 (command evidence retained inline). Overall 4.0. Highest-value improvement would be an authorized future full-matrix fresh-mutant run. User-agreement self-check: scope and limitations are explicit.
