# CritC2AxisFit — C2 claim and axis review

Access date: **2026-10-23**. Axes examined: **calibration, operability**; coverage is the competing classification. This is a critic's evidence report, not a canonical judgment, axis reassignment, or admission decision.

Paths below are lane-relative unless absolute. `A` means `.ufo/waves/round-35/w2/CritC2AxisFit/`; `T` means `/tmp/hyaku/chousa-r35/w2/CritC2AxisFit/`. Complete exercised commands, environments, exit codes and key stdout are in `A/commands-and-results.txt`.

## Principal counterexample: an identity-only battery meets the arithmetic

**Yes: a battery that fails every byte-nonidentical gate can pass P2.** The constant-fail control does not establish resistance to that strategy.

I built `A/identity-only-battery.py` (sha256 `3eb3e16c2acd820b17fc2c8af9821fc51ca5835b9097f1668c1a91d810e82e53`). It reuses the committed fixture generator, executes the candidate **without `bash -x`**, and genuinely checks its nine observed verdicts, drift marker and exit code. Its mechanism answer is solely equality with the landed gate's SHA: identical → pass; anything else → fail. It collects no mechanism trace and honestly reports zero stamps. See its lines 25–43.

With the unmodified committed counter and landed gate:

| Battery | Seed | Exit | Separation | Output-equiv | Landed witness | `predicate_holds` |
|---|---:|---:|---:|---:|---|---|
| identity-only | 3581 | 0 | 2/2 | 2/2 | pass | true |
| identity-only | 3583 | 0 | 2/2 | 2/2 | pass | true |
| committed constant-fail | 3581 | 1 | 2/2 | 2/2 | fail | false |
| committed constant-pass | 3581 | 1 | 0/2 | 2/2 | pass | false |
| committed real witness | 3581 | 0 | 2/2 | 2/2 | pass | true |

Receipts: `A/identity-s3581.json`, `identity-s3583.json`, `stub-fail-s3581.json`, `stub-pass-s3581.json`, `real-witness-s3581.json`. Both identity receipts bind the required landed gate SHA and record **zero chunk/direct stamps even for the passing landed run**. The counter accepts the battery's `witness` and `output_full` fields without independently requiring stamps (`corpus/evidence/round35/c2-count.py:115-127,183-186`).

The exact command family was `timeout 1800s env <recorded scratch environment> python3 <lane>/corpus/evidence/round35/c2-count.py --gate <lane>/tools/research-gate.sh --battery <T>/identity-only-battery.py --seed 3581 --receipt <A>/identity-s3581.json`; seed 3583 changed only the seed and receipt. Absolute paths and environment assignments are recorded in the command artifact.

**Specificity test:** I made named control `neutral-comment.sh` by adding only a comment after the shebang. Its SHA is `32f1a66ca78558696157f0c94d973f5e175174d8551a427a29c8a1e66170043b`. At seed 3581:

- Identity-only battery: exit 1, `WITNESS=fail OUTPUT=9/9` (`A/neutral-identity-s3581.json`).
- Real witness: exit 0, `WITNESS=pass OUTPUT=9/9 STAMPS chunk=9 direct=1`, eight long records (`A/neutral-real-s3581.json`).

Thus the counterfeit battery demonstrably cannot distinguish a harmless source change from the mechanism substitution, yet scores the frozen arithmetic on two fresh seeds. This skips the claimed mechanism work, not the output check.

**Boundary:** these are alternate-`--battery` control runs. They do **not** falsify the default invocation against the fixed committed witness, which I independently observed passing. The fixed witness's SHA differs from the counterfeit and is recorded in every receipt. The finding is that the two constant controls are insufficient evidence of mechanism-sensitive discrimination; it is not an engine bypass of the committed witness or an anti-instrumentation exploit. `claims.md:100-104` is correct in its narrow statement that neither *constant* stub meets P2.

**Smallest safe correction:** preserve the frozen predicate and record this limitation. A future discrimination battery needs byte-distinct, mechanism-preserving positive controls as well as bypass negatives; the comment-only control is the cheapest demonstrated one. Identity-only must fail that enlarged battery. Source review and pinning the intended battery remain necessary; passing finite controls is not a universal cheating-resistance proof.

## Axis fit: the recorded calibration requirement is not measured

`corpus/evidence/round35/claims.md:61-90` declares calibration but measures whether a new trace-observation tool separates two generated engine variants. Its before-state is battery absence (`:96-98`), not a count of discrepancies between assessment and reality.

The canonical axes definitions distinguish domain-surface coverage, runnable artifacts, and honest self-assessment (`/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/AXES.md:9-16`). Mechanism attribution can improve honest self-assessment in the broad sense. However, the lane's recorded round prompt imposes a more concrete calibration observable: mismatches between SCORECARD/SHONEN and observed state (`/home/vgpnk/Projects/shokunin/.ufo/prompts/chousa-round-35.md:355-356`), and names the changed surface rather than the resulting number (`:368-372`). I inspected that prompt as the lane's recorded specification, not as an instruction to change this review's contract or routes.

**P2 does not compute that mismatch count.** Its inputs and predicate are gate/battery files, generated fixtures, verdict matches and trace labels (`c2-count.py:130-190`; `tools/mechanism-witness.py:227-301`). A targeted source search for `SCORECARD|SHONEN|self.assessment` in those two files returned no matches. The source never compares either assessment document with observation.

Additional opened evidence, **not a run by me**: peer `CritClaimSizing`'s `c2-without-assessment-s353504.json` binds the same landed gate and witness hashes, reports P2 true, and uses its isolated three-file experiment. The receipt confirms its passing result; absence of assessment inputs is independently visible in the counter source.

**Axis-fit objection for the canonical judge:** the directly demonstrated delta is a new mechanism-observation capability/tool surface (coverage/capability, with runnable-artifact operability), not the specified calibration mismatch measurement. The declared calibration assignment therefore is not established by P2 under that recorded requirement. Calling the number “calibration” does not supply the missing comparison. Nor does this single two-negative battery establish calibration saturation.

**Smallest safe correction now:** append an explicit measurement/axis-fit limitation and present the successful P2 runs as exactly what they measured. Do not silently relabel the frozen claim to coverage or add a new calibration predicate after data; the round prompt explicitly preserves the pre-data predicate (`:358,364-367`). A future calibration claim could freeze persisted assessment assertions, map them to observations, and count their mismatches. The canonical judge owns whether the present claim receives axis credit. This is an axis-evidence defect, not an operability regression or an observed no-trade violation.

No final round-35 lane report was available at review time: glob `/home/vgpnk/Projects/shokunin/.ufo/reports/round-35/*chousa*` returned no files. The opened scorecard still labels round 35 planned/not started (`SCORECARD.md:1976-1981`). Consequently this review audits the frozen assignment, not an imagined final report's wording.

## Output mismatch: the measured-verdict guard works

I built named control `A/broken-boundary.sh`, SHA `18814c7325cea103592f44a3d8e4941c423d8ea0e0391ba4c5f6b775689df3c8`, by inserting `return 1` at entry to `tok_left_ok` (control line 1608). This intentionally makes real supported occurrences unsupported while leaving the matcher routing available.

The committed counter plus committed witness at seed 3581 exited **1**:

`WITNESS_SEPARATED=0/2 OUTPUT_EQUIV=0/2 LANDED_WITNESS=pass`

Both generated variants had `witness=fail`, zero chunk stamps, **3/9 output**, and `output_full=false`; neither counted as separated. The candidate itself had witness pass with eight chunk stamps but only 3/9 output. Evidence: `A/broken-output-s3581.json:9-24,27-54`. This re-derives the guard in `c2-count.py:183-186`: a failing mechanism label cannot earn separation when the checked verdicts are wrong. The committed baseline, in contrast, produced 9/9 for all three gates.

**Scope of “output-equivalent”:** the witness checks recognized IDs' `observed=` values plus exit 1 and DRIFT (`tools/mechanism-witness.py:66,281-299`), not byte-identical stdout, all finding fields, or the complete set of output counters. Round-34's counter additionally checked `CLAIM_LINE_MISMATCH` and duplicate records (`corpus/evidence/round34/c2-count.py:46-48,95-96,337-344`). Thus the demonstrated guard rejects *measured verdict mismatches*; its label is not proof of total output-contract equivalence. I did not demonstrate a wrong-location or duplicate-output exploit. The smallest wording correction is “full match on this nine-record verdict fixture,” not “every output counter passes.”

## K1/K2 versus ctl4/ctl6: fair mechanism surrogate, not the same regression set

Opened original evidence: `.ufo/waves/round-34/w2a2/MutC2Keyed.md:40-47,78-111`. It records ctl4/ctl6 at 37/37 on seeds 6101/6103, with instrumented evidence that their alternate search actually fired. I did not rerun those old controls.

The original source confirms:

- `ctl4-fixedkey.sh:1598-1615` keys on the **PWD basename** `chousa-r34-c2-*` and dead-zone length, then uses Python whole-byte search without either matcher.
- `ctl6-claimshape.sh:1598-1615,1786-1795` uses the same search, keyed on fixed ID/source/expect shapes.
- Their search still feeds the gate's boundary/location logic; the old report explicitly identifies them as correct alternate implementations, not contract violations (`MutC2Keyed.md:98-111`).

The new controls retain that load-bearing substitution: Python exact offsets instead of chunk offsets (`round35/c2-count.py:58-82,93-112`), while ordinary boundary/location consumers remain in the candidate (`tools/research-gate.sh:1719-1758`). My committed-witness run establishes correct measured verdicts and zero chunk stamps for both new controls.

But they are **adapted surrogates**, not a literal reproduction of the two original fingerprints:

1. K1 unconditionally substitutes the search for every long span; it has no harness-metadata fingerprint.
2. K2 substitutes only under `/tmp`, `/fast` or `/var/tmp`. That condition is necessarily active in these runs because the generated fixture root is under the assigned `/tmp` scratch tree.
3. On this fixture K1 and K2 therefore exercise the same negative mechanism path. “2/2” counts two source variants, not two independent trace-discrimination challenges.
4. The new generator uses `w35wit-*` roots and `corpus/...` source names (`mechanism-witness.py:183-224,243`). **[INFERENCE from those source conditions]** the unchanged old prefix and `src/...` keys would be inert on it. Merely observing those old gates pass this new witness would not show a witness bypass: the bypass branches would not have fired.

So K1/K2 are not a bogus semantic strawman: they do represent the exact-search/no-chunk causal class. They are nevertheless an easier, narrower discrimination task than evidence against arbitrary keyed or partial shortcuts, and they do not independently replace the original 37-record regression coverage. The claim should name these two active surrogates rather than generalize to all fingerprint-and-shortcut engines. The disclosed active-trace/sham-call limit remains important (`claims.md:106-110`).

## “Kills” overstates what fails

`claims.md:63-79` simultaneously says the witness kills the variants and that both implement the written contract. Those are compatible only if “kills” means *declines their attribution to the landed chunk mechanism*, not *finds their functional implementation wrong*. The actual witness result is a threshold over function-entry stamps (`mechanism-witness.py:294-299`), independently combined with an output check.

Smallest safe wording: **“withholds chunk-mechanism credit from K1/K2 on the measured fixture; their measured output remains correct.”** The C2 kill rule can still describe a falsified measurement claim (`claims.md:92-94`). It must not turn absence of chunk attribution into proof that an alternative correct engine is defective. This distinction directly affects calibration; conflating the two would manufacture overconfidence from a provenance test.

## Pins, exercised scope and limits

The required pre-score `timeout 30s sha256sum` returned exit 0:

- landed gate: `1f2fb4f522d9a670b49dd61ad1369f55ee012f3b0d38050654be45a71aaef617`;
- pre-round gate: `a6307edf687ac0fb1b0b08bf7f0518b3fbc310fa9924b970aa3654612562995b`;
- committed counter: `557fdbf0bd793a6589fcb28fbc0a589db9145be0ae3c92790041fe8ebd907171`;
- committed witness: `9f537bfde0dd53f2240af149e1b7a03fd0a0f372ee1fa1a32e94044115a252b3`.

The only non-landed candidate gates scored were the two named, pinned controls above; their preserved sources are in `A`. K1/K2 are the committed counter's named generated controls and their individual hashes are in each receipt. Every listed artifact is below 1 MiB (the two preserved gates are 371225 and 371233 bytes; bounded `du -b` command recorded by the tool).

I first read the required claim/counters/witness/slen probe in order; R1/R2 were not independently re-tested in this scoped assignment. No C1 scoring, selftest, no-harm battery, production modification, Git/JJ write, network access, installation, canonical judge invocation, or other runtime orchestration. Two identity seeds, one real-witness baseline seed, two constant controls, one neutral positive comparison and one broken-output guard run were exercised. No blanket no-regression or universal equivalence claim is made. Setup-only launch/copy failures and their successful bounded retries are disclosed in `A/commands-and-results.txt`.
