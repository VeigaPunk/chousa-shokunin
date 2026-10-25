# W2 MutateNested — leaf-only mutant vs frozen R48 cases-only counter

member: L1Chousa48.MutateNested (mutation-tester, leaf; no subagents, no background jobs)
date: 2026-10-25
claim under test: R48-C1 in `corpus/evidence/round48/claims.md` @ `4bbd2348578bb6288c0700dabf37cea04225bfb6` (HEAD; predicate and controls unchanged by this probe)
scope: `nested-count-key` handling only. Scratch: `/tmp/chousa-r48-MutateNested` (created, used, deleted; disposable per tasking). No lane writes besides this report; `git status` unchanged after probe (4 pre-existing `M`, wave dir `??` only).

## Basis (all local, verified byte-identical to HEAD blobs)

- `tools/inference-ground.py` sha256 `9d789b34562cc0ce35be7e4d7ea67a9fa57eabf8794bbf096c8a8d190925149b` (22018 B) — working tree == `git show HEAD:` blob.
- `corpus/evidence/round48/c1-count.py` sha256 `b2a69185213674a8f3bea126e820e2a3ea2c2ad02540f9c6a055f5af007f271e` — frozen cases counter.
- `corpus/evidence/round48/mutation-check.py` sha256 `aee54b9f199d1d6df81f83e74c3e4ca9249e1fccd6b458d16f929dd1957df2ca` — frozen transform source.

## Mutant (reconstructed exact-byte transform from mutation-check.py:24-25)

Delete, once (anchor count asserted ==1), from `key_negated` (tool lines 395-396):
```
    if leaf.lower() in GENERIC_KEYS and len(parts) > 1:
        leaf = parts[-2]
```
Effect: a generic leaf (`count`, `counts`, `value`, …) no longer defers to its parent key, so `without_archive/count` is read as bare `count` — polarity flips True→False. Defect point verified post-edit: `key_negated` body is `leaf = parts[-1]` then return.

- before sha256 `9d789b34…5149b` (22018 B); after `cd79acf8ea06df284086305a972937f93b99cbbfab862210b6bf75b6d750faa6` (21937 B, −81 B); `python3 -m py_compile` OK.

## Detector runs — `python3 corpus/evidence/round48/c1-count.py --root $PWD --tool <FILE> --cases-only`

BASELINE (scratch pristine copy):
```
implicit-neg=PASS rc=0 · un-neg=PASS rc=0 · un-prefix-flip=PASS rc=1 INF_POLARITY_FLIP
repeated-figure=PASS rc=1 INF_POLARITY_FLIP '1,582 / counts key figures/answers_without_archive_key'
nested-count-key=PASS rc=0 → REFINEMENT_CASES=5/5, C1_CASES=PASS, exit=0
```
MUTANT:
```
implicit-neg=PASS · un-neg=PASS · un-prefix-flip=PASS · repeated-figure=PASS (same finding strings)
nested-count-key=FAIL wanted_rc=0 observed_rc=1
  FINDING INF_POLARITY_FLIP bullet=1 token='1,582 / counts key without_archive/count'
→ REFINEMENT_CASES=4/5, C1_CASES=FAIL, exit=1
```
RESTORED (`cp pristine.py` back over mutant; sha256 again `9d789b34…5149b`):
```
nested-count-key=PASS → REFINEMENT_CASES=5/5, C1_CASES=PASS, exit=0  (full output rerun, last lines shown)
```
Instrument check at the defect point: `key_negated('without_archive/count')` = True pristine, True restored. (Mutant value was False by inspection: leaf `count` ∈ GENERIC_KEYS, deferral removed, `count` carries no NEG_KEY_PART.)

Frozen full probe re-run (read-only; mutates only its own tempfile): `python3 corpus/evidence/round48/mutation-check.py` → `PRISTINE_CASES=PASS`, all five `KILLED` incl. `nested-count-key=KILLED expected-cell=nested-count-key rc=1`, `MUTANTS_KILLED=5/5`, exit 0 — matches `controls/before.txt:85-96`.

## Why the mutant dies in exactly one cell

`count_keys` maps `1582`/`1,582` → `{"without_archive/count"}`. Mutant `key_negated` keeps leaf `count` → pols={False} → `figure_flip` requires NO negator in the 4 words after `1,582`; the bullet's next word is `no` (`is_neg("no")`→True) → flip → `INF_POLARITY_FLIP`, rc=1 vs expected 0. `c1-count.py:47` startswith-matches `nested-count-key=FAIL` → targeted kill.

## Fixture/predicate mismatch — none found

1. Expected-cell match: the only failing cell is the named one (`nested-count-key`); the other four cells still PASS under the mutant, so `c1-count.py`'s exit 1 is caused solely by the target cell — no collateral-failure ambiguity.
2. Discriminating fixture pair: `repeated-figure` uses leaf-negated `answers_without_archive_key`; `nested-count-key` uses parent-negated `without_archive/count`. The pair separates "leaf-only naming" from "generic-leaf→parent deferral" — the mutant distinguishes them exactly as designed (former PASS, latter FAIL).
3. Basis match: pristine/mutant scored against bytes identical to the frozen commit's blobs; the basis is also the "landed control tool" of `before.txt` (nested-count-key PASS there too), so scratch result and frozen receipt agree — no fixture drift.
4. Predicate scope: the probe covers only `--cases-only` (the refinement leg). The full C1 predicate's other legs (precision ≥11/12, LEGACY_R47) are untouched by this single-point defect class at this granularity; not exercised here, per tasking.
5. Cosmetic note (not a mismatch): `c1-count.py:30-33` `if/else` builds identical strings both branches — dead branch, no behavioral effect.

## Verdict

KILLED — the frozen cases-only counter fails the leaf-only mutant at exactly `nested-count-key` while pristine and restored bytes pass 5/5. No coverage finding; the C1 cases leg is load-bearing for this defect class. C1 predicate survives this mutation probe.

## Hygiene

Scratch `/tmp/chousa-r48-MutateNested` removed (verified absent). Zero lane-file modifications; no installs (pacman paused; none needed — python3 stdlib only).

Report: `.ufo/waves/round-48/w2/MutateNested.md`
