# Attack17 — C3 relocation arithmetic

Axes: depth (C3), calibration (counter fidelity), provenance (frozen versus supplemental evidence). Advisory review only; no admission or canonical judgment.

## Counterexample

The frozen relocation oracle rejects all three correct startup diagnostics. In `corpus/evidence/round64/c3-count.py:86`, `mirror` is `<work>/rel-N/lane-copy/corpus/evidence/round65`. The instrument derives `LANE = mirror.parents[2]`, namely `lane-copy`. Its diagnostic therefore correctly names `lane-copy/corpus/SOURCES.md`. The counter instead expects `mirror.parent / "corpus/SOURCES.md"` (line 91), namely `lane-copy/corpus/evidence/corpus/SOURCES.md`. These are different paths. Every frozen relocation comparison is false independently of smoke outcomes.

There is a separate fixture-shape defect: changing `round64` to `round65` preserves directory depth. It is not the promised one-directory-deeper relocation in claims.md:200–203. A real `round64/controls` placement derives `lane-copy/corpus` and correctly diagnoses `lane-copy/corpus/corpus/SOURCES.md`.

## Evidence and bounded execution

Command (exit 0):

```
python3 -B /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-64/w1/Attack17/probe.py
```

The retained probe performs six bounded subprocess executions (10 seconds each), copying only the three instruments; no clone, whole battery, or production edit. It reads frozen bytes with `git show bf40d99bda9eefdad3ed6276da077cfb24ba82f1:<instrument>` (all exit 0) and compares them to current bytes. All three are byte-identical to that freeze:

| Instrument | SHA256 |
|---|---|
| c1-battery-v3.py | 4b3f0b658bcd3bb640cd2e6e56a28a91a72d5352f2610887db01e636fc039fe2 |
| run-receipts-v3.py | 0f3cfae75f711f17251174a2e123321040c91394497bafe4a64c9148d7c3abd7 |
| c3-count.py | 465a8c5efbb870f73c7c6306c813c4fe35f4ccaf5a996a56ab71d4da5feec682 |

For each NAME in the table, commands were `/usr/bin/python3 -B TARGET`, with targets:

```
/fast/scratch/hyaku/chousa-r64/Attack17/NAME/frozen-counter/lane-copy/corpus/evidence/round65/NAME
/fast/scratch/hyaku/chousa-r64/Attack17/NAME/actual-one-deeper/lane-copy/corpus/evidence/round64/controls/NAME
```

All six returned exit 2, empty stdout, and exactly the appropriate instrument prefix plus `MISSING_LANE_FILE: <derived_missing_path>` on stderr. For example the frozen-counter c3 subprocess printed:

```
c3-count: MISSING_LANE_FILE: /fast/scratch/hyaku/chousa-r64/Attack17/c3-count.py/frozen-counter/lane-copy/corpus/SOURCES.md
```

Its frozen oracle expected:

```
/fast/scratch/hyaku/chousa-r64/Attack17/c3-count.py/frozen-counter/lane-copy/corpus/evidence/corpus/SOURCES.md
```

The corresponding actual-one-deeper subprocess printed:

```
c3-count: MISSING_LANE_FILE: /fast/scratch/hyaku/chousa-r64/Attack17/c3-count.py/actual-one-deeper/lane-copy/corpus/corpus/SOURCES.md
```

Probe output: all six `exact_guard_match=true`; all six `counter_match=false`; all three `frozen_equal=true`; `scratch_removed=true`. The original counter's three actual fixtures therefore produce `RELOCATION_MATCH=0/3` [INFERENCE from directly exercised predicates]. I did not execute the whole counting command or claim an observed full `C3=FAIL` receipt.

The existing `controls/c3-before.txt` records `LEG CLEAN clean FAIL rc=1 want 0`, `BATTERY=PARTIAL`, `raw-exit=0`, and shift-only `SHIFT_MUTANT_UNNAMED=1/1`, `shift-exit=0`. It is not a successful relocation receipt and does not resolve the mismatch.

## Claim failure versus supplemental weakness

This is a defect in the frozen instrument itself, not merely a fresh attack outside its fixture coverage. Its required unmodified `RELOCATION_MATCH=3/3` target cannot follow from these bytes and these fixtures. The startup guards themselves behaved correctly in all six probes. The sourced knowledge/Gate leg was outside this seat's assignment and was not assessed.

A distinct inherited or future supplement can demonstrate corrected arithmetic, but cannot stand in for the frozen counter under claims.md:231–233. No supplement was used in these measurements. The known C1 frozen E12/E13 independently drawn-name mismatch remains a separate frozen failure; it was neither rerun nor repaired here. A post-freeze `c1-battery-supplement.py` does not retroactively change that C1 result.

## Smallest safe correction

Preserve frozen files and report the frozen C3 counting target as unmet. For a distinctly named supplement only: construct a genuinely deeper path (`lane-copy/corpus/evidence/round64/controls`), then compute the expected missing path from the fixture's explicitly known root (`lane-copy/corpus/corpus/SOURCES.md` for this depth shift), and compare the exact diagnostic rather than a substring. Merely correcting line 91 would fix the immediate mismatch but leave the depth-shift promise untested. Only L1 may integrate any such supplement.

Tools: existing Python 3.14.8 (`/usr/bin/python3`), existing git read-only; no installs/updates, network, service actions, git mutations, or frozen edits. Scratch removed in the probe's finally block; no clone created.

Self-evaluation: accuracy 4 (full counter result explicitly marked inference); completeness 4 (bounded relocation scope, no source-admission audit); clarity 4 (path arithmetic shown concretely); actionability 4 (separate supplemental correction specified, not implemented by this critic); conciseness 4 (six outcomes condensed). Average 4.0. Highest-impact improvement for the integrating owner: preserve an independent full frozen-counter failure receipt without changing its bytes. User agreement: expected for this scoped arithmetic review.
