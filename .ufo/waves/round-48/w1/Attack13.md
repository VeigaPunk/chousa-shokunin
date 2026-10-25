# Attack13 — R47 C1 frozen-counter coverage: implicit-negator class (mut-a, mut-b)

author: chousa R48 w1 seat Attack13 (critic/falsifier)
date: 2026-10-25
scope: read-only on the lane; scratch under /tmp/chousa-r48-Attack13/ (removed before finish); no lane file modified.

## 1. Target defect

R47 verifier spot-check routed defect 2: the frozen C1 counter
(`corpus/evidence/round47/c1-count.py`, HEAD d4e6ef0, sha256 6d39dce5…) misses
five refinement-mutant classes; `MutC1Refined.md` names the implicit-negator
class as mut-a (`IMPLICIT_NEG` emptied) and mut-b (`UN_NEG_RE` never matches).
This seat re-derives both mutants from the canonical pristine
(`git show 980fe43:tools/inference-ground.py`, sha256
244a1897feec49a5a08625a0ca8d0cb3c490675678badeb3ee23d97a4329667e) and tests
whether the frozen counter catches them, plus the minimal fixture perturbation
that would kill each.

## 2. Setup

- Pristine: `/tmp/chousa-r48-Attack13/tool-980fe43.py` = `git show 980fe43:tools/inference-ground.py` (sha256 244a1897…, equals the MutC1Refined pristine).
- Mutants (edit applied by hand on copies; hashes match MutC1Refined exactly):
  - mut-a `IMPLICIT_NEG = set()` — sha256 0b400d8f9a242e645733a946023eb1556db16b7e42a12cf5a10ab62e679a53c2 (matches 0b400d8f…a53c2).
  - mut-b `UN_NEG_RE = re.compile(r"(?!)")` — sha256 05315aa6af5b299565dffaad36dbafd7a4f1f19759822b9505e96cbaafb3a2c0 (matches 05315aa6…a2c0).
- Frozen counter: `python3 corpus/evidence/round47/c1-count.py --root <lane> --tool <tool>` (same command shape as MutC1Refined §1).

## 3. Frozen counter vs mutants

Baseline (pristine): `TOOL=present POSITIVE_PASS=3/3 JUNK_KILLED=3/3 CANARY=pass R46_COUNTER=pass R46_ENTRIES=2/2 C1=PASS exit=0`.

| tool | result | verdict |
|---|---|---|
| mut-a (IMPLICIT_NEG emptied) | identical all legs PASS, `C1=PASS exit=0` | **SURVIVED** |
| mut-b (UN_NEG_RE never matches) | identical all legs PASS, `C1=PASS exit=0` | **SURVIVED** |

The frozen counter does not distinguish either mutant: both score C1=PASS exactly as the pristine tool. The pinned six-fixture set (`corpus/fixtures/inference-ground-r47/`) contains no implicit negator (grep for `lack|lacks|absent|missing|fail|unable|devoid|untraceable|unfrozen|un…able/ed` over the fixture dir: zero matches, exit 1) and no un- span negator, so neither leg can observe the class.

## 4. Minimal fixture perturbation that WOULD kill each mutant

Counter leg shape reproduced verbatim (`python3 <tool> --entry entry.md --spans spans.tsv --counts counts.json --root <k>`):

killer a_implicit_neg (junk): span `the release lacks a frozen pool of cargo` (S901); bullet asserts `a frozen pool … is shipped… frozen at release`:
- pristine → `FINDING INF_POLARITY_FLIP 'a frozen pool / pool'` + `'/ frozen'`, exit 1;
- mut-a → `GROUND: PASS`, exit 0 (mutant misses "lacks").

killer b_un_neg_re (junk): span `untraceable, the archive link appears` (S901); bullet asserts `the manifest archives the archive link … keeps it`:
- pristine → `FINDING INF_POLARITY_FLIP 'the archive link / archives'`, exit 1;
- mut-b → `GROUND: PASS`, exit 0 (mutant misses "untraceable").

Each killer is one junk fixture: had it been in the pinned JUNKS set, the counter's `killed()` leg (rc 1 + `INF_POLARITY_FLIP`) would print `JUNK_KILLED=2/3` and `C1=FAIL` — i.e. the mutant would be caught. They are not in the set; the gap is pure fixture coverage, confirming MutC1Refined §4/§5.

## 5. Verdict

- Measured: frozen counter lets both implicit-negator mutants survive (`C1=PASS`, exit 0) — truth defect reproduced and confirmed on current HEAD counter.
- Measured: minimal scratch fixtures kill both on the counter's exact leg (pristine exit 1 / mutant exit 0), proving the fix is fixture coverage, not tool logic.
- No lane file touched; git status unchanged from pre-existing untracked round-48 files and inherited r40/r41 receipt JSONs. No installs.
- Follow-up (proposal only, not post-score change): add the two killer junk fixtures to the pinned set at next freeze.
