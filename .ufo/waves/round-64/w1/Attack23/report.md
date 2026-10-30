# Attack23 — lowest-axis and score falsification review

Scope: round64 attempt2, read-only critic. Lane `/home/vgpnk/Projects/shokunin/chousa-shokunin`. Axes: operability, calibration, depth, coverage, freshness, adjacency. No judgment/admission, production edits, runtime invocation, network, installation, clone, or scratch tree. Findings are advisory only.

## 1. Frozen C1 cannot borrow a supplemental pass

Evidence: frozen claims.md:36–45 and 89–93 bind the unmodified v3 battery and three full passes on landing production bytes. Frozen battery:386–394 calls `tag()` twice independently in each E12/E13 leg; the filename and indexed target can differ. Expected exits at :442–443 are nevertheless zero. A checker enforcing both index completeness and phantom rejection must reject mismatched draws. Independent draws are not guaranteed unequal, so the exact defect is failure to guarantee a benign fixture—not mathematical impossibility of any coincidentally matching draw. The assignment's known frozen E12/E13 failure was not rerun.

The measured diff against `c1-battery-supplement.py` changes only these two legs to bind one `t = tag()` per filename/link pair. It is a different instrument, not restored frozen success. Frozen battery SHA256 is `4b3f0b658bcd3bb640cd2e6e56a28a91a72d5352f2610887db01e636fc039fe2`; supplement is `a7057ae33ac958f060a25ea325537bec7bed728e7ea2dad3f3a961e715fc33f1`.

Impacted axes: operability target evidence and calibration/provenance. Smallest safe correction: retain the frozen failure and separately label supplemental observations; never turn the supplement's eventual result into C1 closure. No frozen edits.

## 2. Candidate improvement is neither production identity nor complete contract coverage

Candidate SHA256: `0b4da0d2128e23b4feeb82bb179ec6a89277a1f0a0aa1c7115e3ae38966f185e`; production `tools/lane-preflight.py`: `3d792f0961434ccd76ef87ccb0b2dcccc022f6f84d958dbc4e35e6f4c260a89d`. These identities differ; no candidate pass proves the frozen production target.

Minimal static counterexample (not executed): knowledge contains regular `only.md`; README contains only `only`, without `.md`. Candidate :132–135 searches `p.stem`, so that entry is treated as indexed; frozen claims.md:54–56 requires NAME including `.md`. A valid README plus a directory-target symlink inside knowledge supplies a second static counterexample: candidate :107–124 only inspects `os.walk`'s `fs`, ignoring symlink-to-directory entries classified in `ds`; the frozen contract :49–51 requires non-file symlinks to fail. These are source-derived predictions, not recorded process verdicts. Neither is repaired by the E12/E13 supplement's two substitutions.

Impacted axes: operability and calibration. Smallest safe correction: L1 must implement complete-name matching and explicitly reject directory-target symlinks, retain candidate/production byte identities, and register additional tests under a distinct instrument. Existing frozen C1 failure remains separate from supplemental weakness.

## 3. Lowest recorded score is not independently established lowest expertise

SCORECARD.md:7–13 defines exactly one numeric axis: operability = count of three archived inputs with exit 1 and exactly one DRIFT summary, maximum 3/10. Claims.md:25–26 correctly calls it historical and explicitly refuses a new score. SCORECARD.md:484–495 qualifies lowest selection as being by the only recorded score. The other five axes are unscored—not zero, not higher, and not saturated.

Counterexample to an unqualified lowest-axis claim: an assignment of calibration = 1 is consistent with every recorded numeric score, since calibration is unmeasured; operability = 3 would then not be the actual minimum. This is an identifiability argument, not a fabricated calibration measurement. No unqualified ranking, numeric gain from G02, or numeric saturation is justified. I found no such numeric gain claim in the frozen round64 text.

The score's maximum 3 is also below the declared saturation threshold 8 (SCORECARD.md:471–489), so this fixed observable can never establish saturation even if every newer operability capability works. That is a disclosed conservative policy tradeoff, not evidence of a runtime defect or permission for this seat to revise the rubric. C1's targeted operational repair can remain meaningful while the historical scalar stays unchanged.

Impacted axes: calibration and operability selection. Smallest safe correction: preserve the wording “only/lowest numerically scored axis,” keep the historical score unchanged, and do not infer comparative expertise or saturation. A new rubric would require separately authorized registration, not post-hoc rescaling.

## 4. C3 evidence cannot rescue C1 or numeric claims

Static comparison agrees with the disclosed erratum: C3 counter :86 uses `lane-copy/corpus/evidence/round65` at the same relative depth as round64; :91 expects `mirror.parent / needs[0]`, whereas its own :34–38 derives `HERE.parents[2] / needs[0]`. The expected path thus differs from the instrument's path. This is a frozen counter defect, not a numerical depth increase. Its self-smoke :80–81 is a source-substring observation, explicitly disclosed by the counter docstring :13, not an executed intact self-run. No C3 runtime verdict was produced here.

Impacted axes: depth and calibration. Smallest safe correction: preserve the frozen miss/limits and separately name any corrected future counter. Do not claim that assertions or a sourced supplement make the frozen relocation target pass.

## Commands and observed outputs

1. `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin diff bf40d99bda9eefdad3ed6276da077cfb24ba82f1 -- corpus/evidence/round64/claims.md corpus/evidence/round64/c1-battery-v3.py corpus/evidence/round64/c3-count.py` — exit 0, empty output. These three inspected working files matched the specified freeze at observation time.
2. `sha256sum` on absolute lane paths `corpus/evidence/round64/{claims.md,c1-battery-v3.py,c1-battery-supplement.py,c3-count.py,controls/ref-preflight-v3.py}` and `tools/lane-preflight.py` — exit 0. Remaining hashes: claims `bab186919f4518f3662c31661d1e2060b4f9f3d186b33d184c365a3f82d7cfc0`; C3 `465a8c5efbb870f73c7c6306c813c4fe35f4ccaf5a996a56ab71d4da5feec682`. Battery/C3 prefixes equal the frozen claims.md:264–266 pins.
3. `diff -u /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round64/c1-battery-v3.py /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round64/c1-battery-supplement.py` — exit 1 (differences), exactly the two single-draw repairs described above.

No counting command, battery, judge, or runtime probe was executed; no historical or expected process output is presented as newly observed. Tools installed/updated: none. Scratch created: none; cleanup unnecessary.

## Review self-check

Accuracy 4/5: hashes/diff observed; counterexamples deliberately marked static, not runtime results. Completeness 4/5: numeric inference and frozen/supplemental authority covered; no independent current archive score measurement asserted. Clarity 4/5: separates identities, claim failure, and policy tradeoff. Actionability 4/5: corrections identify L1-owned matching/walk fixes without altering freeze. Conciseness 4/5: four findings retain necessary scope and provenance. Mean 4.0/5. Highest-impact improvement for an authorized executor is a uniquely named bounded test for the complete-name and directory-symlink examples; this critic does not invoke another runtime. User-agreement self-check: conclusions stay advisory and do not manufacture a verdict.
