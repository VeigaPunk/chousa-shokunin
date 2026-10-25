# HeldOutA — round 47 wave 2: false-refusal rate of the C1 polarity probe

ATTACKS: C1 operandability claim; false-refusal rate of `tools/inference-ground.py` on a fresh held-out set (wave-1 `LabC1FalsePos` sentences not reused)
VERDICT: overclaim

## Method
12 one-bullet entries shaped like `corpus/fixtures/inference-ground-r47/positive-negation-kept.md`, each quoting a phrase verbatim from `spans/S901-1.txt` or `spans/S902-1.txt` (manifest `spans.tsv`: S901=`the release ships a frozen pool`, S901=`no revision is recorded`, S902=`the archived copy is dated at build`) and reasoning correctly in varied academic English: six about the negated phrase `no revision is recorded`, six about the affirmed phrases (three each). Run landed tool on each:
`python3 tools/inference-ground.py --entry /tmp/chousa-r47w2-HeldOutA/probes/<f>.md --spans corpus/fixtures/inference-ground-r47/spans.tsv --counts corpus/fixtures/inference-ground-r47/counts.json`

Tool: lane tip `1fc5ed193ad48a482402c862f4e4cc47e46d5b2d`, tool sha256 `244a1897feec49a5a08625a0ca8d0cb3c490675678badeb3ee23d97a4329667e`, clean working tree for the tool. Every run printed `GROUND … bullets=1 tokens=1 grounded=1` (token grounded) except the two runs noted below.

## Result — refusals **2/12** (p03, p04); every other bullet PASS (exit 0)
```
p01  no revision is recorded / no revision can be traced … impossible to verify -> PASS
p02  no revision is recorded / The frozen pool lacks revision markers -> PASS
p03  no revision is recorded / this release's revision history is nonexistent -> FINDING INF_POLARITY_FLIP token='no revision is recorded / revision'  exit=1
p04  no revision is recorded / the release cannot show that any sentence has been revised -> FINDING INF_POLARITY_FLIP token='no revision is recorded / revised'  exit=1
p05  no revision is recorded / a published page is distributed without revision records -> PASS
p06  no revision is recorded / the pool is unsuitable for revision-sensitive evaluation -> PASS
a01  the release ships a frozen pool / a later page cannot be an unrecorded update -> PASS
a02  the release ships a frozen pool / the pool is stable after its release -> PASS (see rerun note)
a03  the release ships a frozen pool / its contents are fixed -> PASS
a04  the archived copy is dated at build / snapshotted on the build date -> PASS
a05  the archived copy is dated at build / that date is not the copy's build date -> FINDING INF_POLARITY_FLIP token='the archived copy is dated at build / build'  exit=1
a06  the archived copy is dated at build / needs a separate timestamp -> PASS
```
Probe sha256 (files deleted with scratch): p01 `2efa029b…a2b2c`, p02 `5037e0ff…9157e`, p03 `0417be38…0dbf2`, p04 `e90591d9…5a87`, p05 `c66f8cf1…ab18d`, p06 `d568a4b5…bbd330`, a01 `7c4005ea…0d373`, a02 `b035c09d…dcbf59` (after rerun), a03 `2eb30f6a…7f97a`, a04 `b5a05e8f…fc3e2`, a05 `1314550d…5bbc7` (after rerun), a06 `a097f4e4…43c852`.

## Refused bullets: mechanism (both inf)
- **p03**: bullet restates the negated noun (`revision history`) with `nonexistent` as the absence word. `nonexistent` is not in the reference negation list or `IMPLICIT_NEG` (reference:254-255), and `UN_NEG_RE` (`^un(?!…)`) does not match it — it starts with `non-`, not `un-`. So no negator sits in the 3-before/2-after window of the `revis` stem. Same mechanism class as wave-1 p03 (`absent`), here with a different unlisted word.
- **p04**: the correct negator `cannot` is outside the 3-before/2-after window of the `revis` stem (`revised`): `The release cannot show that any sentence has been revised` — `cannot` is 5 words before `revised`; ref 3 before/2 after (reference:333-335). Same mechanism as wave-1 p05; this exact example is not in wave 1.

## The other nine bullets confirm the tool's documented behavior
- Affirmed half: 5/6 pass. `a05` refuses because the bullet's own negator (`not`) lands within 3 words before the affirmed scope stem `build` (`is not the copy's build date`), P2 (reference:336). The bullet's reasoning is correct — the negator's scope is its second date, not the established build date — so this is an over-refusal of a common natural construction. The `un`-prefixed P2 branch is not exercised (no `unfrozen`-style word needed in correct prose).
- Negated half: 4/6 pass. The 4 passers cover (i) avoiding the scope stem (p01: `no` is in-window for `revis`), (ii) a listed implicit negator adjacent to the stem (p02 `lacks`), (iii) a literal negator adjacent to the stem (p05 `without`), (iv) an implicit negator + no stem (p06).
- Named limit (reference:55-58) stays intact: no flip is accepted; every refusal flags a P1/P2 flip token, none is a silent pass.

## Counterexample (strongest)
p05: "a published page is distributed without revision records, as `no revision is recorded` per sentence." The body correctly describes absence (`without` = listed negator), yet P1's window (3 before/2 after the `recor` stem) does not reach `without` (4+ words before `records`). Two competing correct phrasings of the same fact straddle the pass/refuse line purely by word distance (p05 vs p02). This is the same distance sensitivity wave-1 documented (p09/p05), reproduced here.

## Impacted axes
- **Calibration**: measured false-refusal rate on this fresh held-out set is 2/12 (≈17%); on the negated half 2/6 (≈33%). The round-47 lesson's wave-1 figure (9/10) reflected a tuning set of near-minimal distance phrasings; the rate here is lower but non-zero, and remains concentrated in "absence expressed without a listed negator" and "negator beyond the window".
- **Operability**: the tool's docstring Named limit (reference:55-58) still lists only false negatives (synonym/antonym/scope); the false-positive refusal class (negated-phrase stem reused without an in-window listed negator, including `non-` words and distance) is not documented. This is the wave-1 repair suggestion 1, still unapplied — the round-47 lesson names it as mistake 3 (counter repairs), not a docstring repair.

## Smallest safe correction (no predicate/counter/fixture/floor/target change)
Document the cost side of the frozen predicate: add a false-positive sentence to the docstring's Named limit and to the round-47 lesson — a correct bullet that restates a negated phrase's stem with an unlisted absence word (`nonexistent`, `lacks` is listed), or with a listed negator beyond the 3-before/2-after window, is refused by rule 5 P1; measured here 2/12 on a fresh set. No tool, counter, fixture, predicate or target change is proposed or made. No installs; scratch `/tmp/chousa-r47w2-HeldOutA/` deleted at the end.
