# R55ExecC3ObsProbe — C3 E08–E11 observations

Axes: calibration; independent observation; evidence traceability. No predicate, target, counter, or control was changed. All probe outputs below are from assigned BASE/round-54 files.

## Probe receipts

- E08 command: `python3 $S/mirror/corpus/evidence/round53/pointer-anchor-check.py --root $S/mirror` after `git archive dba605deb5cd5ed4874e0e3c39ba24737409cd80` into the mirror and deleting `corpus/evidence/round54/S100-text-form.txt` and `S101-text-form.txt`. Output last line: `ANCHORED=7/16 UNANCHORED=9 BAD=9`; the command also emitted nine `BAD_ANCHOR` lines, one per lost form anchor. The claim's `BAD=6` is falsified; counter-derived precise observation proposed as `ANCHORED=7/16 UNANCHORED=9 BAD=9`.
- E09 attempted requested ctypes probe under HOOK extracted from round-54 `c1-count.py`; the probe driver itself failed Python parsing before installing the hook: `SyntaxError: unexpected character after line continuation character`. No `rc` or marker observation was obtained. Do not claim this item observed; actionable blocker is to rerun with a valid driver.
- E10 direct receipt: `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round54/controls/c1-controls.txt`, SHELL block, exact line `LEGS=1/6`. Observation proposed `LEGS=1/6`.
- E11 inspected BASE `corpus/evidence/round54/c1-supplement.py`: docstring defines three legs `ISOLATED`, `RESAVE`, `HELDOUT`; the requested no-open oracle-echo execution was not run. Thus `SUPPLEMENT_LEGS=0/3` is not claimed as observed; blocker is execution of that exact tool under the BASE supplement/counter.

## Draft errata (only observations with direct evidence)

- E08 target `corpus/lessons/round-54.md`; unique anchor candidate: `anchor: "prints \`BAD=6\`"` (target file occurrence count must be checked; my quick shell probe mishandled backticks and returned the shortened string, so uniqueness remains unverified). `observed: "ANCHORED=7/16 UNANCHORED=9 BAD=9"`.
- E10 target `corpus/QUALITY.md`; anchor key phrase: `anchor: "the SHELL control's receipt says the same"` (occurs once in the file per `text.count` probe). `observed: "LEGS=1/6"`.

## Evidence limits

E08 was measured against the BASE mirror as specified. E10 was read from the committed receipt. E09 and E11 remain unmeasured; no erratum is supplied for either. No verification/build/test was run. Scratch was created at `/fast/scratch/hyaku/chousa-r55/R55ExecC3ObsProbe`; initial malformed-probe script did not create a marker or launch LibreOffice.

VERDICT: attacked E08–E11; E08 and E10 observations falsify their stated values, E09/E11 remain unmeasured.