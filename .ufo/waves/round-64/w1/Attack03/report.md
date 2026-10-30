# Attack03 — C1 fixture-path detector forgery

## Axes and counterexample

Impacted axes: operability (G02 rejects actual defects), calibration (battery PASS does not establish ordinary-path behavior), and provenance (supplemental evidence must not replace the frozen authority).

**Confirmed supplemental weakness:** a three-line branch added at the start of the inherited candidate's `g02` delegates to its existing implementation only when the root basename matches `lane-x[0-9a-f]{4}` and its parent matches `r-[0-9a-f]{8}`. Everywhere else it returns PASS without reading the index. This deliberately broken tool passed all 43 inherited supplemental legs, including E09, yet passed an ordinary-path fixture containing `knowledge/gone.md` with no corresponding file. The unmodified candidate rejected that same ordinary fixture.

This attacks the frozen battery's recognition-hardening assertion at `c1-battery-v3.py:71–77`: random suffixes do not eliminate its fixed path grammar. Both instruments expose that grammar at frozen lines 525–529 / supplement lines 527–531. The attacker needs neither the seed nor access to another leg. It uses only `--root`.

## Evidence and commands

All paths below are relative to `/home/vgpnk/Projects/shokunin/chousa-shokunin` unless absolute. Reproduction driver: `.ufo/waves/round-64/w1/Attack03/probe.py`. Three-line insertion retained in `forgery-insertion.txt`; full command arrays, stdout, stderr and child exits are retained alongside this report.

Executed command:

`python3 -B /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-64/w1/Attack03/probe.py`

The driver launched these independent bounded battery probes with `C1_SEED=Attack03-path-forgery`, `--fleet /home/vgpnk/Projects/shokunin`, and `--jobs 2`:

- Frozen battery against inherited candidate, `--only E12,E13`: exit **0**, but both legs print `FAIL rc=1 want 0`, followed by `BATTERY=PARTIAL`. This exit is explicitly the partial-run exit, not a passing full battery. Receipt: `frozen-benign.txt`.
- Distinct `c1-battery-supplement.py` against forged candidate: exit **0**, `CLEAN=1/1 DEFECTS=28/28 BENIGN=11/11 ZERO=3/3 BATTERY=PASS`. Receipt: `supplement-forged.txt`.
- Ordinary minimal fixture with `ok.md` indexed and a phantom `knowledge/gone.md` row, `--only G02`: inherited candidate exit **1**, `FAILED=G02`; forged candidate exit **0**, `PREFLIGHT=1/1 FAILED=none`, `GATE G02 knowledge-index PASS forged outside fixture path`. Receipts: `candidate-ordinary.txt`, `forged-ordinary.txt`.

Read-only `git show bf40d99bda9eefdad3ed6276da077cfb24ba82f1:corpus/evidence/round64/c1-battery-v3.py` exited 0. Its bytes equal the on-disk frozen instrument; SHA-256 `4b3f0b658bcd3bb640cd2e6e56a28a91a72d5352f2610887db01e636fc039fe2` (`provenance.txt`). No frozen bytes changed.

## Frozen failure versus supplemental weakness

Frozen E12 independently calls `tag()` for the file and its escaped README name (386–389); E13 independently calls it for the file and encoded README target (391–394). The supplement reuses a single tag per leg (386–396). These are different instruments. The observed frozen leg failures agree with the known mismatch; they must not be repaired, hidden, or reclassified as a successful C1 measurement. No full frozen BATTERY=PASS is claimed here. The frozen kill rule still requires three full frozen passes on landing production bytes; the supplement cannot discharge it, and the inherited reference is not production.

The new attack demonstrates supplemental false confidence separately: the complete supplemental PASS admits a tool that intentionally ignores every ordinary-path G02 defect. It does not establish that this forged tool passes the frozen full battery. The frozen rule itself routes fresh wave falsifier classes to the next battery rather than retroactively changing the claim.

## Smallest safe correction

Keep the frozen claim/counter and its failure record untouched. Route this path-recognition mutant into a separately named successor instrument. Its first additional metamorphic check should run identical defective content under both the current fixture grammar and an ordinary root name and require equal failing G02 verdicts. This kills the demonstrated mutant; merely renaming the current fixed prefixes only moves the recognizable signature. Do not claim that this single added check defeats arbitrary adaptive forgery. Do not promote a supplemental PASS to frozen claim closure; admission remains the canonical authority's decision.

## Execution limits and cleanup

One seed, one complete supplemental run, two frozen selected legs, two direct G02 probes. No production edits, clones, network, package installs, git/jj mutations, or sibling writes. Existing Python 3.14.8 was used (system installation; no update).

The overall driver exited **1 after all probe receipts were written**, because mode-000 E02c knowledge-directory residue defeated its initial `shutil.rmtree`. This cleanup failure is not a battery failure. A separate `chmod -R u+rwX /fast/scratch/hyaku/chousa-r64/Attack03 && rm -r /fast/scratch/hyaku/chousa-r64/Attack03` exited **0**. The retained reproduction driver now restores traversal permissions before cleanup; that cleanup amendment was not rerun. Scratch removed; no live clone created.

## Self-evaluation

Accuracy 4/5: raw child exits and the driver cleanup failure are distinguished; only one seed exercised. Completeness 4/5: the requested forgery and frozen/supplement split are covered; no full frozen run performed. Clarity 4/5: receipts are explicit, although reproduction is longer than the three-line attack. Actionability 4/5: a precise successor check is proposed, not implemented by this leaf reviewer. Conciseness 4/5: some cleanup detail is necessary for honest provenance. Overall 4.0/5. Improvement priority: successor-author validation of the metamorphic check with independent ordinary-name distributions. Would the user agree? Likely, provided these remain advisory findings rather than closure.
