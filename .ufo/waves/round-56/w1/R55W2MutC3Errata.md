# R55W2MutC3Errata — C3 mutation probe

Scope: `c3-count.py` against the round-55 lane revision `29cfb12abd70f688b48c0d17f31e636f2d81104a`; no production files changed. The counter docstring says E11 is necessarily WRONG with `--skip-slow`; its non-skipped observation requires `soffice`.

## Detector receipts

- Initial archive-only scratch copy lacked git objects. Counter output: `ENV_CHANGED git show dba605deb5cd:tools/capture-text.py` (exit 2); inconclusive, not a mutant result.
- Recreated scratch as a shared local clone at the specified revision (HEAD printed `29cfb12abd70f688b48c0d17f31e636f2d81104a`); the required BASE_REV object was then accessible.
- Pristine `--skip-slow` baseline: E01–E10 `OK`, E11 `WRONG (slow item skipped)`, `ERRATA=10/11 MISSING=0 ANCHOR=0 WRONG=1`, `C3=FAIL`, rc=1. Per the frozen claim, this is expected for `--skip-slow`, not a passing baseline for a full 11-item mutant comparison.
- E11 non-skipped invocation (performed once): E11 `OK`, but E01 `ANCHOR` because the scratch SCORECARD was in the shortened-anchor mutation state; `ERRATA=10/11 MISSING=0 ANCHOR=1 WRONG=0`, `C3=FAIL`, rc=1. Thus the E11 observation ran, but this is not a pristine full baseline.

## Mutations

| Perturbation | Item | Output/status | Verdict |
|---|---|---|---|
| Changed one character in E01 observation (`count=1` → `count=2`) | E01 | E01 `WRONG`; other E01–E10 items `OK`; skipped E11 `WRONG`; `ERRATA=9/11 … WRONG=2`, rc=1 | Killed: wrong observation detected. E11 skip is a known baseline failure. |
| Shortened E01 anchor, dropping key phrase “no line here” | E01 | E01 `ANCHOR`; other E01–E10 `OK`; skipped E11 `WRONG`; `ERRATA=9/11 … ANCHOR=1 WRONG=1`, rc=1 | Killed: anchor/key check detected. |

I did not complete the requested duplicate-anchor, target-path-typo, and section-heading mutations. Their statuses are unmeasured, not inferred. The observation mutation was subsequently restored before the anchor mutation; the latter was restored using `git -C <scratch clone> checkout -- SCORECARD.md`. The E11 run occurred before that restoration.

## Anchor duplication census at 29cfb12

Python `str.count(anchor)` over each erratum target at the specified revision returned exactly `1` for every anchor E01–E11. Relevant later-edit surfaces mentioned in the task are the r36 `#### Corrections (round 55)` section and QUALITY statement corrections; the census shows no duplicate at this revision. This count does not establish behavior for subsequent edits beyond this revision.

Commands exercised (paths abbreviated only for readability):

```text
python3 <scratch>/lane/corpus/evidence/round55/c3-count.py --root <scratch>/lane --work <empty-work> --skip-slow
python3 <scratch>/lane/corpus/evidence/round55/c3-count.py --root <scratch>/lane --work <empty-work>   # once, E11
```

VERDICT: The two executed E01 mutations were killed by C3; remaining three requested perturbations are unmeasured, and the first full-baseline attempt is inconclusive because the tested E11 run was not pristine.
