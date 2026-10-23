# CritC3Claim — C3 claim review, round 34 attempt 2

Access date: 2026-10-23. Axes: **calibration** (whether assessment matches observed state) and **operability** (whether the advertised audit command actually reproduces its count). This is critic evidence, not a canonical Rust judgment or admission decision.

## Finding

**The committed numerical result is reproducible, and I found no post-first-run audit-set edit. The weakness is the claimed calibration improvement, not fabricated arithmetic.** The audit-only overlay on the unchanged pre-C3 assessment produces exactly the same 0/0 output as the after-state. Moreover, changing the scorecard's own current audit population from 43 to 777, then breaking a SHONEN evidence pointer, still produces byte-identical 0/0 output. Those mutations do not falsify the explicitly bounded 43-check predicate: they expose the difference between that predicate and the broader assertion that round-34 self-description is machine-audited.

## Pins and scope

- Frozen lane revision: `707da8184a0fc4d10ab3f17271556cdf364f0af5`.
- `timeout 30s sha256sum /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh` exited 0 and printed `a6307edf687ac0fb1b0b08bf7f0518b3fbc310fa9924b970aa3654612562995b`.
- The review copied 30 required input files from that named commit, not an unpinned working tree. Every copied file equalled its source working-tree bytes when copied: `CritC3Claim/input-pins.json` records paths, sizes and full SHA-256 values. Audit-set SHA-256: `01f6c4b49febdd02a28d12d7ad1c623ce015219df53e4c01d0582a9369479f5c`; auditor: `22a6822ca79f7f5eac8d0e64ad7e6bc0fd0a46af0be8353d52884b75d246091f`.
- Scratch: `/fast/scratch/hyaku/chousa-r34-a2/w2/CritC3Claim/`. The scratch repositories are no-checkout, shared-object clones with only the auditor's required inputs materialized. No lane production files, Git index, jj state, fleet files or sibling files were changed.
- `timeout 30s df -h /fast` exited 0: 37G available. No network, installs, signals, C1 held-shape experiments, C2 counter runs, or other judging runtime were used. TMPDIR/C1_TMP/C2_TMP were set to this seat's scratch directory in both experiment runners.

All artifact references below are relative to `.ufo/waves/round-34/w2a2/`. Production citations are lane-relative, accessed 2026-10-23.

## Commands and observations

The principal command was `timeout 240s python3 /fast/scratch/hyaku/chousa-r34-a2/w2/CritC3Claim/review_probe.py` (exit 0). Its 66 bounded subprocess calls, PIDs, exact argv/cwd, exits, stdout or stdout hashes, and stderr are in `CritC3Claim/probe-commands.json`. Runner SHA-256: `24b10dde2861937b83e587959f23d7b475f0273a6a9c9e64f02d1f5f44de21ce`.

Every audit below ran the same auditor command, `timeout 60s python3 corpus/evidence/round34/self-audit.py`, from the named scratch root. Every run exited **0**, as the counting contract specifies.

| Experiment | Scratch root / change | Observed K / J | Evidence |
|---|---|---|---|
| Frozen after-state | `lane/`, all input bytes pinned to frozen tip | **0 / 0**, 43 AUDIT lines; stdout byte-identical to committed first receipt | `CritC3Claim/baseline-audit.txt`, `probe-commands.json` |
| Pre-C3 assessment + auditor only | `before-with-auditor/`: all pre-existing selected inputs from `fe0f22e0`; add only the frozen auditor, set and empty dispositions; do not add first-run receipt | **0 / 0**, stdout byte-identical to after-state | `CritC3Claim/pre-c3-with-auditor.txt`, `probe-commands.json` |
| False current scorecard population | Change scratch SCORECARD.md:1961 from 43 checks to **777 checks**; audit set unchanged | **0 / 0**, still 43 AUDIT lines; stdout byte-identical to baseline | `CritC3Claim/false-scorecard-count.txt`, `false-scorecard-count-receipt.json` |
| Also break promotion evidence | Additionally change scratch SHONEN.md:6 to cite missing `corpus/knowledge/crit-c3-missing-r34.md` | **0 / 0**, stdout byte-identical to baseline | `CritC3Claim/false-scorecard-and-shonen.txt`, `false-scorecard-and-shonen-receipt.json` |
| Re-derive committed negative control | Restore assessment files; change first commit prefix to `deadbeef` and expected gate digest to 64 zeros in scratch set; empty dispositions | **2 / 2** | `CritC3Claim/two-lies-no-disposition.txt`, matching `-receipt.json` and `-set.json` |
| Re-derive disposition subtraction | Same two lies; add `commit-b8053900 | accepted synthetic control only; not a lane disposition` to scratch dispositions | **2 / 1** | `CritC3Claim/two-lies-one-disposition.txt`, matching `-receipt.json` and `-set.json` |

Mutation runs used `timeout 90s python3 /fast/scratch/hyaku/chousa-r34-a2/w2/CritC3Claim/capture_audit.py <label>`, each exit 0. Labels are the experiment artifact basenames above; individual receipts retain child PID, exact audit command/cwd, output digest, input hashes, changed assessment lines and dispositions. Capture-runner SHA-256: `9f774f02d1c77b664d0bfb9ce3682a539452348dde7ca6e3873e9a9f219fc587`. `timeout 30s test ! -e /fast/scratch/hyaku/chousa-r34-a2/w2/CritC3Claim/lane/corpus/knowledge/crit-c3-missing-r34.md` exited 0.

Baseline and pre-C3-overlay stdout SHA-256 are both `b709781c949b5f63371783b93f3b99958f6b48b413a96899de1209646af06452`.

## Answers to the assigned attacks

### 1. Does it count mismatches rather than assert them?

**Yes, for the enumerated population.** `corpus/evidence/round34/self-audit.py:76-129` evaluates the five check kinds and appends failed check IDs; `:129-134` counts them and subtracts IDs present in dispositions. The two injected lies were actually detected, and the disposition-key experiment reproduces the committed negative-control description (`.ufo/waves/round-34/measure-a2/audit-negative-control.txt:1-5`). This is not a constant-zero printer.

The 43 checks are 12 commit resolutions, four digest comparisons, four receipt/gate bindings, 20 path-existence checks and three text assertions (`audit-set.json:4-234`). They do **not** count arbitrary statements in self-assessment documents. In particular, no check reads SCORECARD.md; SHONEN.md is merely an existence check at `audit-set.json:194-197`, while its three selected evidence paths are independent fixed strings at `:199-212`. The only text assertions are two SKILL tally patterns and a LOG lesson-path pattern (`:214-232`). This explains the two surviving false-assessment controls without blaming the arithmetic.

### 2. Is the after-state one concrete value re-derivable with one command?

**Yes, once the revision/input bytes are pinned.** The command in the scorecard, `python3 corpus/evidence/round34/self-audit.py`, prints K=0 and J=0 on the frozen input set; my bounded invocation reproduced the entire committed receipt byte-for-byte, not just its final two lines. The original receipt contains 43 check lines followed by 0/0 (`.ufo/waves/round-34/measure-a2/audit-first-run.txt:1-45`). The tool intentionally exits 0 even for mismatches (`self-audit.py:129-134`), so exit 0 alone is not evidence for P3.

### 3. Can the do-nothing control reach it?

**Literal absence of the auditor cannot produce an auditor receipt; unchanged assessment state can reach its numerical after-state once measured.** `timeout 30s git ls-tree -r fe0f22e0 -- corpus/evidence/round34/self-audit.py corpus/evidence/round34/audit-set.json corpus/evidence/round34/audit-dispositions.md .ufo/waves/round-34/measure-a2/audit-first-run.txt` exited 0 with no entries. Thus the claim's stated absence-of-receipt distinction is real.

But the pre-C3 overlay above preserves the existing gate, assessment documents, receipts and other selected inputs from `fe0f22e0`; only the three new measurement artifacts are added. It reaches **exactly the same 0/0 output** without any existing self-assessment repair. This is a counterfactual instrument-overlay control, not falsely labelled a literal no-tool run. [INFERENCE] It establishes acquisition of a reproducible structural audit, not a reduction in calibration mismatches. Treating receipt creation alone as proof that assessment quality improved is the claim-level weakness for the canonical judge to decide.

### 4. Was any audit check edited/deleted after the first committed counted run?

**No such violation exists in the pinned committed history I inspected.** Exact command: `timeout 30s git log --format=fuller -p 707da8184a0fc4d10ab3f17271556cdf364f0af5 -- corpus/evidence/round34/audit-set.json` (exit 0). It shows only addition of the entire set at `0af0844c156845c1e5f7feb59bdada9f642d6ae8`, the same commit that first adds the counted receipt. There are no later set edits, deletions or appends. Receipt/tool/set/dispositions history was also opened with `git log`; all first appear in that commit, while claims-a2.md first appears at `7c7eb3a6`.

`timeout 60s git -C <lane> diff --stat 0af0844c..707da8184a0fc4d10ab3f17271556cdf364f0af5 -- corpus/evidence/round34/audit-set.json corpus/evidence/round34/self-audit.py corpus/evidence/round34/audit-dispositions.md .ufo/waves/round-34/measure-a2/audit-first-run.txt` exited 0 with empty output. Evidence: `CritC3Claim/audit-set-history.txt` (SHA-256 `300080b1c883b5ea43d1242d8bbfb0725079d6200a1c731146c65a09918d0695`), `post-first-audit-changes.txt`, and `attempt2-timeline.txt`.

An important chronology limit, not an accusation of a kill-rule breach: the artifact set was not independently committed at the earlier claims-design commit; its first committed form arrives alongside the first receipt. This history cannot establish what uncommitted drafts existed before that run. Also, SCORECARD/LOG assessment updates land later at `fce3119c`; `timeout 30s git diff --stat 0af0844c..707da8184a0fc4d10ab3f17271556cdf364f0af5 -- SCORECARD.md LOG.md SKILL.md SHONEN.md` exited 0 and showed LOG +20 and SCORECARD +27/-5. The first count therefore is not evidence that later-added assessment wording was individually checked.

### 5. Is K=0 informative or vacuous?

**Informative as 43 bounded facts; not evidence that all assessment is correct or improved.** The negative control demonstrates sensitivity, so the count is not wholly vacuous. With K=0, however, the statement that every mismatch has a disposition is vacuously true: the committed dispositions file is empty, and no real disposition decision is exercised. The pre-C3 replay shows no observed before-to-after mismatch reduction. The surviving 777-check and missing-pointer mutations show that 0 is compatible with plainly false statements in the two documents named by the calibration axis.

The claim expressly excludes unenumerated checks (`claims-a2.md:164-165`), so those mutations are **coverage/wording counterexamples**, not a fabricated numerical P3 failure. The broader current scorecard statement at `SCORECARD.md:1959-1961` should not be read as comprehensive self-assessment validation. The canonical axis definition is self-assessment quality, not merely artifact existence (`/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/AXES.md:13-16`).

### 6. What would make C3 fail next round?

Under the unchanged frozen P3 and kill rule (`claims-a2.md:144-153`), [INFERENCE] any newly different K fails the reproduction requirement, even if its mismatches receive dispositions. A changed gate or counter digest, vanished selected path, unresolved selected commit, broken selected receipt binding, missing 256-case text, or an appended failing check would produce a mismatch; the observed two-lie controls demonstrate this class of failure. An undispositioned mismatch additionally makes J positive. Silently updating an existing pinned expectation or deleting a failing check would violate the no-edit/no-delete rule rather than rescue the old result.

Conversely, [INFERENCE] new false scorecard content or a changed SHONEN reference outside the fixed checks need not move K at all; the scratch controls already demonstrate this blindness. Reusing K=0 next round is not evidence of saturation or continued comprehensive calibration.

## Smallest safe correction

1. **For this record:** retain the honest 0/0 measurement and immutable checks, but describe the achievement narrowly as a newly reproducible 43-check structural audit. Do not infer repaired assessment errors or comprehensive calibration from the absence-of-receipt control. Whether that bounded acquisition earns a calibration-axis move is reserved for the canonical judge.
2. **For a stronger calibration claim:** freeze an assessment-derived population and apply the same instrument to before and after assessment bytes. Include controls that alter an existing scored assertion and an actual cited pointer, not just the audit set. Any extension of this set must be appended and logged under the existing rule; do not revise old expectations or retroactively change K to absorb a new failure.

## Limits

I reviewed the frozen claims, full C2 counter, self-audit implementation/set, first/negative audit receipts, relevant assessment/lesson sections and committed attempt-2 history. I re-derived the C3 first result and both negative-control counts only; I did not re-score C2 or C1, audit excluded held shapes, validate all claims made in assessment documents, or prove the authenticity of historical execution beyond the committed files. The pre-C3 replay contains the auditor's complete consulted input population, not a full repository checkout. It deliberately adds the instrument and is not presented as an untouched no-tool baseline. No production fix or canonical judgment was made. Artifacts are bounded below 1 MiB; the largest is the command ledger, approximately 161 KB.
