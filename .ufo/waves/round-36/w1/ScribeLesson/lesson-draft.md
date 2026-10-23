# Round 36 lesson skeleton — wave 1

Axes: operability and calibration (`.ufo/waves/round-36/w1-spec.json:4-8`). Draft only; source-row teachings below are pending the local-manual citations from the S069/S070 source seats.

## Mistakes

| Class | Evidence pointer (opened 2026-10-23) | Captured by | Fix / lesson |
|---|---|---|---|
| Counter docstring number drift and survivor attribution | `corpus/evidence/round36/c2-count.py:36-39` says “separates only 3/5 (V3 and V5 pass it).” The committed legacy receipt `.ufo/waves/round-36/measure/c2-before-legacy-s36001.json:16-20` has `matched: 2`, `total: 5`, `predicate_holds: false`, `landed_attrib: absent`. Its variant fields show V2 `exit: 0`/`witness: pass` (`:37-48`), V3 pass (`:50-61`), and V5 pass (`:76-87`); all three also have `output_full: true`. | Compared the docstring to the receipt's top-level `matched` count and per-variant `witness` fields; this is not a new counter run. | Correct the docstring to say 2/5 are separated, distinguish separation from variants that survive the legacy witness, and list V2/V3/V5 as pass. |
| Attempt-1 landing-debris allegation (`corpus/evidence/round36/__pycache__`) is unverified by the available snapshot | The status command below returned current status on 2026-10-23 and contains no `corpus/evidence/round36/__pycache__` entry; a direct `glob` for that directory returned “Path not found.” The status was run after wave start, so it cannot establish what existed at wave start. The opened `.ufo/waves/round-36/w1-run.err:1` and `w1-plan.err:1` are empty, not start-time status records. | Ran `timeout 900s git -C /home/vgpnk/Projects/shokunin/chousa-shokunin status --short --untracked-files=all` (exit 0); checked the target path and the two wave stderr files. | Do not attribute residue to a crash or assert it existed at wave start without a contemporaneous status snapshot. Save the complete start-state status before running work. The cause and historical presence are not established here. |
| Attempt-label metadata mismatch (intent unknown) | Frozen design `corpus/evidence/round36/claims.md:3` says “Attempt: 1.” Wave spec `.ufo/waves/round-36/w1-spec.json:3` calls this “round-36 attempt 2 wave 1”. | Compared the frozen-design header with the wave's own milestone field. | Make the reuse explicit in the wave wrapper/report (e.g. attempt-1 frozen claims carried into attempt 2); do not silently edit the frozen claims. Whether this label difference is intentional is unknown. |

Current `git status` output (this is not a wave-start snapshot):

```text
 M .gitignore
?? .ufo/waves/round-36/gen-w1-spec.py
?? .ufo/waves/round-36/w1-briefs/CONTEXT.md
?? .ufo/waves/round-36/w1-briefs/ConnOverlap.md
?? .ufo/waves/round-36/w1-briefs/CritC1Swap.md
?? .ufo/waves/round-36/w1-briefs/CritC2CallForShow.md
?? .ufo/waves/round-36/w1-briefs/ExecC1BaseCtl.md
?? .ufo/waves/round-36/w1-briefs/ExecC1FreshA.md
?? .ufo/waves/round-36/w1-briefs/ExecC1FreshB.md
?? .ufo/waves/round-36/w1-briefs/ExecC1ScenarioMap.md
?? .ufo/waves/round-36/w1-briefs/ExecC2FreshA.md
?? .ufo/waves/round-36/w1-briefs/ExecC2FreshB.md
?? .ufo/waves/round-36/w1-briefs/ExecC2LegacyCtl.md
?? .ufo/waves/round-36/w1-briefs/ExecHashShim.md
?? .ufo/waves/round-36/w1-briefs/ExecLocaleDecode.md
?? .ufo/waves/round-36/w1-briefs/ExecModeCoverage.md
?? .ufo/waves/round-36/w1-briefs/ExecNewCases.md
?? .ufo/waves/round-36/w1-briefs/ExecPinEchoDrift.md
?? .ufo/waves/round-36/w1-briefs/ExecSelftest.md
?? .ufo/waves/round-36/w1-briefs/ExecWitnessDirect.md
?? .ufo/waves/round-36/w1-briefs/LabScenarioIsolation.md
?? .ufo/waves/round-36/w1-briefs/MutC1Arm.md
?? .ufo/waves/round-36/w1-briefs/MutC2AttrKey.md
?? .ufo/waves/round-36/w1-briefs/RevClaimPredicate.md
?? .ufo/waves/round-36/w1-briefs/RevCounterHonesty.md
?? .ufo/waves/round-36/w1-briefs/RevLocaleSeam.md
?? .ufo/waves/round-36/w1-briefs/RevPinContract.md
?? .ufo/waves/round-36/w1-briefs/ScoutC1Counter.md
?? .ufo/waves/round-36/w1-briefs/ScoutC2Counter.md
?? .ufo/waves/round-36/w1-briefs/ScoutGateDiff.md
?? .ufo/waves/round-36/w1-briefs/ScoutInherited.md
?? .ufo/waves/round-36/w1-briefs/ScoutReceipts.md
?? .ufo/waves/round-36/w1-briefs/ScribeKnowC1.md
?? .ufo/waves/round-36/w1-briefs/ScribeKnowC2.md
?? .ufo/waves/round-36/w1-briefs/ScribeLesson.md
?? .ufo/waves/round-36/w1-briefs/ScribeSrcGrep.md
?? .ufo/waves/round-36/w1-briefs/ScribeSrcSha.md
?? .ufo/waves/round-36/w1-briefs/SentNoHarm.md
?? .ufo/waves/round-36/w1-briefs/SimpDiff.md
?? .ufo/waves/round-36/w1-dispatch.json
?? .ufo/waves/round-36/w1-plan.err
?? .ufo/waves/round-36/w1-run.err
?? .ufo/waves/round-36/w1-spec.json
?? .ufo/waves/round-36/w1/ExecC1BaseCtl/c1-before-s36321.json
?? .ufo/waves/round-36/w1/swarm-registry.json
```

## Gate

SOURCES rows proposed for addition (teachings are provisional; ground them with the respective source row drafts and located manual quotes before merging):

| Row | One-line teach |
|---|---|
| S069 — GNU grep(1), `/usr/share/man/man1/grep.1.gz` | `-b` with `-o` reports the byte offset of the matching part; `-a` treats binary input as text. (Scope requested in `w1-briefs/ScribeSrcGrep.md:12-23`; manual quote still pending.) |
| S070 — GNU coreutils `sha256sum(1)`, `/usr/share/man/man1/sha256sum.1.gz` | A SHA-256 digest is 256 bits/64 hexadecimal characters; `--check` verifies checksum records. (Scope requested in `w1-briefs/ScribeSrcSha.md:12-23`; manual quote still pending.) |

Rejects to record:

- Reject citing only a local manual copy without its file SHA: the exact source bytes would not be pinned; require path, access date, hash, and a located short quote.
- Reject a network grep result or unopened POSIX page as evidence: neither was opened for this draft, and the wave contract forbids network access.

Spot-check placeholder — after results arrive, cross-check this draft with the wave seats listed in `.ufo/waves/round-36/w1-spec.json:12-35,107-165`: ScoutGateDiff, ScoutC1Counter, ScoutC2Counter, ScoutReceipts, ScoutInherited; RevLocaleSeam, RevPinContract, RevCounterHonesty, RevClaimPredicate; CritC1Swap, CritC2CallForShow; MutC2AttrKey, MutC1Arm; SentNoHarm, SimpDiff, ConnOverlap, and LabScenarioIsolation. No spot-check result is claimed yet.
