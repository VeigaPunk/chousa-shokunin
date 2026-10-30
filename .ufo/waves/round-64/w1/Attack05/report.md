# Attack05 — C1 symlink recursion

## Axes and counterexample

Axes: operability (G02 completeness), calibration (frozen versus supplemental evidence), provenance (which bytes were measured). Advisory review only; no admission, integration, or canonical judgment.

Minimal counterexample: a knowledge directory containing indexed `ok.md` plus `loop -> .`. Frozen C1 text requires a non-file symlink to FAIL (claims.md:47–52, 99–101). The inherited reference candidate instead returns PASS because `os.walk(..., followlinks=False)` puts the symlink in `ds`, and the reference checks only `fs`. A directory symlink `alias -> ../outside`, with an unindexed file inside outside, produces the same false pass. Following directory links recursively is NOT the correction: the explicit contract rejects these links and a cycle must terminate.

## Byte identities

Read-only `git show bf40d99bda9eefdad3ed6276da077cfb24ba82f1:tools/lane-preflight.py` exited 0. Probe snapshot SHA-256:

- freeze-commit tool: `7e9427785db117e2996fe23134ab5c9357ea793d25efabb5cb5159e4ca79d460`
- inherited `corpus/evidence/round64/controls/ref-preflight-v3.py`: `0b4da0d2128e23b4feeb82bb179ec6a89277a1f0a0aa1c7115e3ae38966f185e`
- current working-tree `tools/lane-preflight.py`: `3d792f0961434ccd76ef87ccb0b2dcccc022f6f84d958dbc4e35e6f4c260a89d`
- frozen battery: `4b3f0b658bcd3bb640cd2e6e56a28a91a72d5352f2610887db01e636fc039fe2` (matches frozen prefix)
- post-freeze supplement: `a7057ae33ac958f060a25ea325537bec7bed728e7ea2dad3f3a961e715fc33f1`
- claims: `bab186919f4518f3662c31661d1e2060b4f9f3d186b33d184c365a3f82d7cfc0`

Current working-tree tool already contains a `ds` symlink rejection (lines 109–113 in initial read). It is not identical to either inherited reference or freeze-commit production bytes. Its bounded results below close this particular defect at the measured working-tree bytes; this is not a landing-commit or full-battery certificate.

## Bounded executed evidence

Driver retained at `.ufo/waves/round-64/w1/Attack05/probe.py`. Command (exit 0):

```
python3 -B /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-64/w1/Attack05/probe.py
```

Driver snapshots tools, constructs five tiny fixtures, and concurrently runs each tool with this exact argument form (each command has a ten-second timeout):

```
/usr/bin/python3 -B /fast/scratch/hyaku/chousa-r64/Attack05/TOOL.py --root /fast/scratch/hyaku/chousa-r64/Attack05/CASE --only G02 --work /fast/scratch/hyaku/chousa-r64/Attack05/work-TOOL-CASE
```

| Fixture | Frozen tool | Reference candidate | Current tool |
|---|---|---|---|
| clean: indexed ok.md | PASS, exit 0 | PASS, exit 0 | PASS, exit 0 |
| directory-link: alias -> outside directory | PASS, exit 0 | PASS, exit 0 | FAIL, exit 1 |
| directory-cycle: loop -> . | PASS, exit 0 | PASS, exit 0 | FAIL, exit 1 |
| regular-link: indexed alias.md -> ok.md | PASS, exit 0 | PASS, exit 0 | PASS, exit 0 |
| dangling-link: indexed alias.md -> absent.md | PASS, exit 0 | FAIL, exit 1 | FAIL, exit 1 |

Every subprocess stderr was empty. Exact decisive current-tool lines:

```
GATE G02 knowledge-index FAIL 1 invalid under corpus/knowledge: alias (not a regular file)
GATE G02 knowledge-index FAIL 1 invalid under corpus/knowledge: loop (not a regular file)
GATE G02 knowledge-index PASS 2 entries indexed
GATE G02 knowledge-index FAIL 1 invalid under corpus/knowledge: alias.md (unresolvable symlink)
```

False-pass reference lines for both directory cases:

```
GATE G02 knowledge-index PASS 1 entries indexed
PREFLIGHT=1/1 FAILED=none ENV=none SKIPPED=G01,G03,G04,G05,G06,G07,G08
```

Failing cases printed `PREFLIGHT=0/1 FAILED=G02 ENV=none SKIPPED=G01,G03,G04,G05,G06,G07,G08`; every other gate was SKIP. Clean yielded PASS 1 entry; regular-link yielded PASS 2 entries. These are narrow G02 probes, not frozen battery runs.

## Frozen failure versus supplemental weakness

The supplied known E12/E13 frozen failure was not rerun or repaired. Source inspection confirms frozen battery lines 386–394 independently call `tag()` for the created filename and index mention in BOTH legs; expected rc is nevertheless 0 (lines 442–443). This invalidates their intended benign premise. Honest correction cannot generally make those mismatched fixtures pass without weakening the rule. The frozen C1 kill condition still requires the unmodified battery to PASS three times (claims.md:89–93); supplemental success cannot substitute for that requirement. C1's frozen failure must remain explicit.

The distinct supplement reuses one generated tag per E12/E13 fixture (lines 386 onward). However, its only symlink plant is E08's dangling link; no directory-symlink or cycle leg exists in the inspected leg table. Thus the supplement lacks a verdict-bearing check for the demonstrated reference-candidate defect. This is supplemental coverage weakness, distinct from the frozen E12/E13 claim failure. Per frozen routing, fresh falsifier classes go to a subsequent instrument, not into rewritten frozen rules.

## Smallest safe correction

For any still-used reference candidate: keep `followlinks=False`, reject symlinks present in each `ds` list before examining `fs`, retain stat-based regular-file symlink acceptance, and add separately named future coverage for `loop -> .`, an external-directory link, and a benign regular-file link. The measured current tool already implements the source-side rejection and passes these bounded probes. Do not integrate the older reference over that correction; only L1 integrates. Do not rename supplemental evidence as frozen C1 success. No production edit was made.

## Hygiene and self-assessment

Python 3.14.8 and existing git were used; no tools installed/updated, network accesses, clones, commits, pushes, or operator-input changes. Driver reported `SCRATCH_REMOVED True` after removing its entire scratch directory.

Self-evaluation (not canonical judgment): accuracy 4/5 (all results pinned to snapshots, not landing bytes); completeness 4/5 (assigned symlink shapes covered, full battery deliberately not rerun); clarity 4/5 (matrix separates three authorities, lengthy identities retained for provenance); actionability 5/5 (small correction and frozen/supplement routing explicit); conciseness 4/5 (reproducibility adds detail). Mean 4.2/5. Highest-value improvement outside this seat is future independently named symlink coverage, not changing the frozen counter. User-agreement self-check: findings directly distinguish inherited failure, current correction, and frozen closure failure.
