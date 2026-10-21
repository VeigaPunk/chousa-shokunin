# FMutateC2Killed — C2 overdue comparison sensitivity

## Scope, axes and verdict

- Seat: `ChousaR26R.FMutateC2Killed`; round26 attempt1, fresh falsification wave. Author-lane advice only; no outside-judge, promotion, SHONEN or round-admission conclusion.
- Primary axis: **calibration** — demonstrate that an independent expected-result assertion actually fails when the targeted freshness check is disabled. Target behavior: **freshness**, claim C2. Isolation/restoration protects production operability; no general operability result is claimed.
- **Mutant verdict: KILLED.** The same one-fixture detector exited **0 → 1 → 0** on pristine → mutated → restored gate bytes. The mutant executed successfully, misclassified the overdue entry as current, omitted `META_RECHECK_OVERDUE`, and returned CLEAN. The detector then failed four independent persisted expectations. This was a behavioral mismatch, not a syntax error, timeout or baseline failure.
- No production defect was demonstrated on this fixture: pristine and restored runs produced the required overdue warning and DRIFT exit. This is sensitivity evidence for the detector below, not proof that the entire C2 suite or C1/C3 is correct.

## Immutable identity and isolation

Read first: `corpus/evidence/round26-claims.md` and `corpus/QUALITY.md`, followed by `corpus/evidence/round26-measured-revision.json` and workstation rules. C2's contract is claims lines 59–74: an explicit calendar-valid recheck date is the due date; as-of strictly after due requires overdue plus a warning. QUALITY criterion 17 requires a real independent failing control, not a printed tally.

- Claim base resolved: `ba3333254dd337658a4f25e7a9471f9cf4e4567e`.
- Target in the measured-revision record: `0e9784bd52eca456b24d0bc40921480a47f91a2b`.
- Lane HEAD observed at isolation: `0e9784bd52eca456b24d0bc40921480a47f91a2b` (same target). The moving tree was not graded.
- Measured-revision record phase: `immutable production target; integrated final run not yet performed`. This report does not substitute for that integrated run.
- Unique private archive: `/tmp/chousa-r26-falsify-FMutateC2Killed-YXmN1Cv2`.
- The only lane write by this seat is this report. All fixture, detector, mutation and capture files are in that private archive. No lane production gate, index, jj state, fleet state, sibling files, configuration or routing was modified. No delegation, background job, other agent/runtime invocation or external research was performed.

## Exact mutation

One operand at `tools/research-gate.sh:2756`, changing the overdue comparison into a self-comparison. A plausible wrong-operand/copy-paste defect makes the predicate always false while keeping valid Bash and the normal execution path.

```diff
--- a/tools/research-gate.sh
+++ b/tools/research-gate.sh
@@ -2756 +2756 @@
-        if ((asof_days > due_days)); then freshness=overdue; fi
+        if ((asof_days > asof_days)); then freshness=overdue; fi
```

The exact delta is also retained at sandbox `mutation-evidence/disable-overdue.patch`. No other gate line was edited. Restoration replaced that same line with its exact original bytes before the restored run.

## Independent expected result and bounded detector

Exactly one small fixture, sandbox `mutation-evidence/overdue.md` (189 bytes):

```markdown
source: S001 isolated local calibration fixture
verified-at: 2026-10-01 checked isolated overdue fixture
recheck: 2026-10-20

## Body
A dated recheck strictly before 2026-10-21 is overdue.
```

The explicit due date is independently chosen from the registered contract, not inferred from gate output. At as-of `2026-10-21`, the required due is `2026-10-20`, freshness is `overdue`, the warning is required, and gate exit is 1. The detector imports no gate helper and uses no gate-derived oracle. It asserts the gate exit and exact metadata/finding/summary lines rather than accepting `METADATA_COMPLETE=1/1` alone.

Identical detector bytes were used for all three states, sandbox `mutation-evidence/detect-overdue.sh`:

```bash
#!/usr/bin/env bash
set -uo pipefail
sandbox=$1
fixture="$sandbox/mutation-evidence/overdue.md"
expected_meta='META entry=overdue.md source=present verified_at=dated recheck=scheduled due=2026-10-20 freshness=overdue verdict=drift'
expected_finding='FINDING META_RECHECK_OVERDUE severity=warn surface=metadata obs=entry=overdue.md due=2026-10-20 as_of=2026-10-21'
expected_complete='METADATA_COMPLETE=1/1'
expected_summary='RESEARCH_GATE: DRIFT (entries=1 complete=1 findings=1 drift=1)'
output=$(timeout 15s env CHOUSA_ROOT="$sandbox" CHOUSA_STRICT=0 CHOUSA_NOW_EPOCH=1792540800 bash "$sandbox/tools/research-gate.sh" verify-metadata "$fixture" --root "$sandbox" --as-of 2026-10-21 2>&1)
gate_rc=$?
printf '%s\n' '--- raw gate output ---' "$output" '--- end raw gate output ---'
printf 'GATE_EXIT=%s\n' "$gate_rc"
mismatches=0
if [[ $gate_rc != 1 ]]; then
  printf 'ASSERT_FAIL gate_exit expected=1 actual=%s\n' "$gate_rc"
  mismatches=$((mismatches + 1))
fi
for expected in "$expected_meta" "$expected_finding" "$expected_complete" "$expected_summary"; do
  if [[ $'\n'"$output"$'\n' != *$'\n'"$expected"$'\n'* ]]; then
    printf 'ASSERT_FAIL missing_exact_line=%s\n' "$expected"
    mismatches=$((mismatches + 1))
  fi
done
if ((mismatches)); then
  printf 'DETECTOR: FAIL mismatches=%s\n' "$mismatches"
  exit 1
fi
printf '%s\n' 'DETECTOR: PASS mismatches=0'
```

Each gate invocation is bounded by `timeout 15s`. Each detector subprocess was additionally captured with a 20-second deadline using Python's standard-library `subprocess.run(..., capture_output=True, timeout=20)` in the tool session; all completed normally. The frozen epoch yields the same banner timestamp in every run. Gate stdout/stderr is combined by the detector; detector process stderr was empty in all three runs.

Exact detector command, run once in each state with cwd equal to the sandbox:

```sh
bash /tmp/chousa-r26-falsify-FMutateC2Killed-YXmN1Cv2/mutation-evidence/detect-overdue.sh /tmp/chousa-r26-falsify-FMutateC2Killed-YXmN1Cv2
```

## Actual outputs and exits

### Pristine — detector exit 0, gate exit 1 (expected negative fixture)

```text
--- raw gate output ---
research-gate v2 — ts=2026-10-21T00:00:00Z — mode=verify-metadata — path=/tmp/chousa-r26-falsify-FMutateC2Killed-YXmN1Cv2/mutation-evidence/overdue.md — root=/tmp/chousa-r26-falsify-FMutateC2Killed-YXmN1Cv2
META entry=overdue.md source=present verified_at=dated recheck=scheduled due=2026-10-20 freshness=overdue verdict=drift
FINDING META_RECHECK_OVERDUE severity=warn surface=metadata obs=entry=overdue.md due=2026-10-20 as_of=2026-10-21
METADATA_COMPLETE=1/1
RESEARCH_GATE: DRIFT (entries=1 complete=1 findings=1 drift=1)
--- end raw gate output ---
GATE_EXIT=1
DETECTOR: PASS mismatches=0
```

### Mutated — detector exit 1, gate exit 0 (expected detector failure)

```text
--- raw gate output ---
research-gate v2 — ts=2026-10-21T00:00:00Z — mode=verify-metadata — path=/tmp/chousa-r26-falsify-FMutateC2Killed-YXmN1Cv2/mutation-evidence/overdue.md — root=/tmp/chousa-r26-falsify-FMutateC2Killed-YXmN1Cv2
META entry=overdue.md source=present verified_at=dated recheck=scheduled due=2026-10-20 freshness=current verdict=clean
METADATA_COMPLETE=1/1
RESEARCH_GATE: CLEAN (entries=1 complete=1 findings=0 drift=0)
--- end raw gate output ---
GATE_EXIT=0
ASSERT_FAIL gate_exit expected=1 actual=0
ASSERT_FAIL missing_exact_line=META entry=overdue.md source=present verified_at=dated recheck=scheduled due=2026-10-20 freshness=overdue verdict=drift
ASSERT_FAIL missing_exact_line=FINDING META_RECHECK_OVERDUE severity=warn surface=metadata obs=entry=overdue.md due=2026-10-20 as_of=2026-10-21
ASSERT_FAIL missing_exact_line=RESEARCH_GATE: DRIFT (entries=1 complete=1 findings=1 drift=1)
DETECTOR: FAIL mismatches=4
```

The mutant's valid META and CLEAN summary, gate exit 0, and lack of error text establish execution reached the behavioral path; no syntax-error kill is claimed. The completion tally stayed `1/1`, illustrating why an assertion on that tally alone would be insufficient.

### Restored — detector exit 0, gate exit 1 (same expected negative fixture)

```text
--- raw gate output ---
research-gate v2 — ts=2026-10-21T00:00:00Z — mode=verify-metadata — path=/tmp/chousa-r26-falsify-FMutateC2Killed-YXmN1Cv2/mutation-evidence/overdue.md — root=/tmp/chousa-r26-falsify-FMutateC2Killed-YXmN1Cv2
META entry=overdue.md source=present verified_at=dated recheck=scheduled due=2026-10-20 freshness=overdue verdict=drift
FINDING META_RECHECK_OVERDUE severity=warn surface=metadata obs=entry=overdue.md due=2026-10-20 as_of=2026-10-21
METADATA_COMPLETE=1/1
RESEARCH_GATE: DRIFT (entries=1 complete=1 findings=1 drift=1)
--- end raw gate output ---
GATE_EXIT=1
DETECTOR: PASS mismatches=0
```

The capture comparison actually reported:

```text
RESTORED_STDOUT_EQUALS_PRISTINE=True
RESTORED_STDERR_EQUALS_PRISTINE=True
```

Raw captures remain in sandbox `mutation-evidence/{pristine,mutated,restored}.{stdout,stderr}`. The complete outputs, fixture, detector and delta are embedded here so the evidence does not depend on `/tmp` survival.

## Hashes and exact-byte restoration

Gate SHA-256, recorded with `sha256sum` at each state:

| State | SHA-256 |
|---|---|
| Target commit via `git show` | `c2c813f1b425bc4e74625a2607eaca1b97addf9898f834e88af8f1fe2143abc6` |
| Pristine archive | `c2c813f1b425bc4e74625a2607eaca1b97addf9898f834e88af8f1fe2143abc6` |
| Mutated archive | `5b696c8d21fab1c9003499eac3d14041fb7342be8904f95cdb2c06d369fda62c` |
| Restored archive | `c2c813f1b425bc4e74625a2607eaca1b97addf9898f834e88af8f1fe2143abc6` |

Detector SHA-256 was identical before mutation, during mutation and after restoration: `af5d7ce2c311a81d3a07289bb09cf98a697108031b338805bcf95ad1368e7efd`.

Fixture SHA-256 was identical in those same three states: `7ee7f58c521803ccd9222a048918660531f3cf1daaa6a09c7eb8c6f3b760005d`.

All 13 target-record input hashes were observed in the pristine archive and again after restoration, matching the measured-revision record in both observations:

```text
c2c813f1b425bc4e74625a2607eaca1b97addf9898f834e88af8f1fe2143abc6  tools/research-gate.sh
b51c96f63a36bfe0bce96f90be26c931d9f6d2d85169c237cd1dcb23fc6dfb53  corpus/evidence/round26-measure.sh
dcbe2b5f12415b7d3828d149e2295bdeb492b712a0f896a9907d56e01f507f1c  corpus/evidence/round26-claims.md
bb8f7f44871b1ac52d3da1f85d6d314aee77490315b566b382788d94ada1f5e7  corpus/evidence/round26-date-differential.sh
6b2d135c01a8f41b914fb248af35567828336a1a69190560c5df4a07b40f1d78  corpus/evidence/round26-registry-oracle.py
852a764870f71e7247005f2b91d6864cbe0ba6527098f2c35536466117e676e9  corpus/evidence/round26-registry-differential.sh
8308e6291bdd0c1896bb5d72095696ff491f7f3d748c1b28ed13e9c2c78a5aa9  corpus/SOURCES.md
2428baaf8ddc8fe3b8f08eff0865563dc4c1c08489b86bb4a8d6ba860327dce6  corpus/QUALITY.md
ee2179753af34d9777537f9ce8cbbd9ddf19cd28e59c544590a5f8b5e1e9958f  SKILL.md
9def6469ad4078446db03e76641ddab7be353de4f10848665824cf89daf7cc8b  corpus/README.md
cc653b0fe48f1d5a0f3efa2d61d1e1134d87a36fd67d799f70e07ab963bf5325  corpus/knowledge/reader-allocation-r26.md
a0995b7814ddae2a2edf8e25f785de065af674efbb8a337a655feac4c82c7d5e  corpus/knowledge/recheck-due-r26.md
248224a270481c49a7fc8a2aaf4b4edf36e061fbea8cc35d3fd715e8f0886d29  corpus/knowledge/registry-link-r26.md
```

## Command / exit ledger

Repository identity command (exit 0):

```sh
git -C /home/vgpnk/Projects/shokunin/chousa-shokunin rev-parse HEAD 0e9784bd52eca456b24d0bc40921480a47f91a2b^{commit} ba3333254dd337658a4f25e7a9471f9cf4e4567e^{commit}
```

Actual output, in argument order:

```text
0e9784bd52eca456b24d0bc40921480a47f91a2b
0e9784bd52eca456b24d0bc40921480a47f91a2b
ba3333254dd337658a4f25e7a9471f9cf4e4567e
```

Sandbox setup (each command exit 0; archive pipeline overall exit recorded, individual stage exits not separately captured):

```sh
mktemp -d /tmp/chousa-r26-falsify-FMutateC2Killed-XXXXXXXX
git -C /home/vgpnk/Projects/shokunin/chousa-shokunin archive --format=tar 0e9784bd52eca456b24d0bc40921480a47f91a2b | tar -x -C /tmp/chousa-r26-falsify-FMutateC2Killed-YXmN1Cv2
git -C /home/vgpnk/Projects/shokunin/chousa-shokunin show 0e9784bd52eca456b24d0bc40921480a47f91a2b:tools/research-gate.sh | sha256sum
```

The archive command ran with cwd `/tmp`; the `git show` checksum pipeline ran with cwd `/tmp` and overall exit 0. All checksum commands below ran with cwd `/tmp/chousa-r26-falsify-FMutateC2Killed-YXmN1Cv2`, each exit 0:

```sh
# Pristine target-record inputs:
sha256sum tools/research-gate.sh corpus/evidence/round26-measure.sh corpus/evidence/round26-claims.md corpus/evidence/round26-date-differential.sh corpus/evidence/round26-registry-oracle.py corpus/evidence/round26-registry-differential.sh corpus/SOURCES.md corpus/QUALITY.md SKILL.md corpus/README.md corpus/knowledge/reader-allocation-r26.md corpus/knowledge/recheck-due-r26.md corpus/knowledge/registry-link-r26.md
# Run once pristine and once mutated:
sha256sum tools/research-gate.sh mutation-evidence/detect-overdue.sh mutation-evidence/overdue.md
# Restored target-record inputs plus unchanged detector and fixture:
sha256sum tools/research-gate.sh corpus/evidence/round26-measure.sh corpus/evidence/round26-claims.md corpus/evidence/round26-date-differential.sh corpus/evidence/round26-registry-oracle.py corpus/evidence/round26-registry-differential.sh corpus/SOURCES.md corpus/QUALITY.md SKILL.md corpus/README.md corpus/knowledge/reader-allocation-r26.md corpus/knowledge/recheck-due-r26.md corpus/knowledge/registry-link-r26.md mutation-evidence/detect-overdue.sh mutation-evidence/overdue.md
```

The mutation and restoration used the surgical edit tool, each changing only displayed line 2756 in the sandbox. There was no patch shell command or lane edit. The detector command above ran exactly three times: pristine exit 0, mutated exit 1, restored exit 0; its inner gate exits were 1, 0, 1 respectively. No other behavioral checks were run.

## Limits and disposition

- The mutant is killed by this bounded independent detector. The expected detector failure is an intentional negative control, not a production regression.
- The pristine observation covers one explicit-date overdue fixture only. It does not establish cadence arithmetic, all date boundaries, refusal handling, registry behavior, citation support/truth, field readiness, legacy holds or integrated round admission.
- No full selftest, build, lint, formatter, differential suite, measurement suite or 8 MiB amplification probe was run. L1 retains integrated verification and production ownership.
- No tools were installed or updated; the paused package-manager boundary was respected.
- Exact gate bytes restored; independent fixture and detector unchanged; no further mutation probe performed.
