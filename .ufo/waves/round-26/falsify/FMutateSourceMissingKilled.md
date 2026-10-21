# FMutateSourceMissingKilled — missing registry-row mutation

## Scope, axis, and result

- **Axis: calibration (C3), specifically independent failing-control sensitivity.** Production isolation and exact-byte restoration are held constraints, not additional improvement claims.
- **Mutation verdict: KILLED** for the final single-token S999 fixture. The pristine detector exited 0; disabling only the missing-row warning made the gate incorrectly return CLEAN/0 and the independent detector exit 1; exact restoration returned the detector to exit 0.
- This is author-lane advisory evidence for round26 attempt1 only, not an outside judgment, overall C3 admission, citation support/truth assessment, or field-readiness claim.
- The detector used here is the scoped one-entry wrapper `detect-source-missing.py` plus the immutable independent registry oracle. The shipped multi-suite `round26-registry-differential.sh` was inspected but **not run**; no sensitivity result is claimed for that script.

## Immutable identity and isolation

Read the assigned claims, QUALITY, measured-revision manifest, operator rules, and relevant skills before changing anything. Contract anchors: `corpus/evidence/round26-claims.md:84-116,132-165` and `corpus/QUALITY.md:93-100` at the target below.

| Identity | Observed value |
|---|---|
| Target from measured-revision manifest | `0e9784bd52eca456b24d0bc40921480a47f91a2b` |
| Manifest phase | immutable production target; integrated final run not yet performed |
| Manifest observation time | `2026-10-21T12:48:50.583128+00:00` |
| Lane HEAD observed before extraction | `0e9784bd52eca456b24d0bc40921480a47f91a2b` |
| Claim base resolved as a commit | `ba3333254dd337658a4f25e7a9471f9cf4e4567e` |
| Private archive sandbox | `/tmp/chousa-r26-falsify-FMutateSourceMissingKilled-ZqrJA8t7` |

The tested gate came from `git archive` of the target, not from the moving lane working tree. Only the assigned report was written inside the lane. All fixtures, detector files, mutations and raw captures are in the private sandbox. No production gate, Git index, jj state, sibling tree, runtime, routing, fleet ledger, or source registry was edited. No delegation or background jobs were started.

### Identity commands and exits

The following shell commands completed with exit 0. Unless a cwd is stated otherwise, cwd was `/home/vgpnk/Projects/shokunin`.

```sh
git -C /home/vgpnk/Projects/shokunin/chousa-shokunin rev-parse HEAD 0e9784bd52eca456b24d0bc40921480a47f91a2b^{commit} ba3333254dd337658a4f25e7a9471f9cf4e4567e^{commit}
mktemp -d /tmp/chousa-r26-falsify-FMutateSourceMissingKilled-XXXXXXXX
git -C /home/vgpnk/Projects/shokunin/chousa-shokunin archive --format=tar 0e9784bd52eca456b24d0bc40921480a47f91a2b | tar -x -C /tmp/chousa-r26-falsify-FMutateSourceMissingKilled-ZqrJA8t7
git -C /home/vgpnk/Projects/shokunin/chousa-shokunin show 0e9784bd52eca456b24d0bc40921480a47f91a2b:tools/research-gate.sh | sha256sum
```

The rev-parse output, in order, was target, target, claim base as shown in the identity table. `mktemp` returned the sandbox shown above. Extraction printed nothing. The `git show` checksum was `c2c813f1b425bc4e74625a2607eaca1b97addf9898f834e88af8f1fe2143abc6`.

From cwd `/tmp/chousa-r26-falsify-FMutateSourceMissingKilled-ZqrJA8t7`, exit 0:

```sh
sha256sum tools/research-gate.sh corpus/evidence/round26-measure.sh corpus/evidence/round26-claims.md corpus/evidence/round26-date-differential.sh corpus/evidence/round26-registry-oracle.py corpus/evidence/round26-registry-differential.sh corpus/SOURCES.md corpus/QUALITY.md SKILL.md corpus/README.md corpus/knowledge/reader-allocation-r26.md corpus/knowledge/recheck-due-r26.md corpus/knowledge/registry-link-r26.md
```

Every extracted input below matched its manifest SHA-256:

| Path | SHA-256 |
|---|---|
| `tools/research-gate.sh` | `c2c813f1b425bc4e74625a2607eaca1b97addf9898f834e88af8f1fe2143abc6` |
| `corpus/evidence/round26-measure.sh` | `b51c96f63a36bfe0bce96f90be26c931d9f6d2d85169c237cd1dcb23fc6dfb53` |
| `corpus/evidence/round26-claims.md` | `dcbe2b5f12415b7d3828d149e2295bdeb492b712a0f896a9907d56e01f507f1c` |
| `corpus/evidence/round26-date-differential.sh` | `bb8f7f44871b1ac52d3da1f85d6d314aee77490315b566b382788d94ada1f5e7` |
| `corpus/evidence/round26-registry-oracle.py` | `6b2d135c01a8f41b914fb248af35567828336a1a69190560c5df4a07b40f1d78` |
| `corpus/evidence/round26-registry-differential.sh` | `852a764870f71e7247005f2b91d6864cbe0ba6527098f2c35536466117e676e9` |
| `corpus/SOURCES.md` | `8308e6291bdd0c1896bb5d72095696ff491f7f3d748c1b28ed13e9c2c78a5aa9` |
| `corpus/QUALITY.md` | `2428baaf8ddc8fe3b8f08eff0865563dc4c1c08489b86bb4a8d6ba860327dce6` |
| `SKILL.md` | `ee2179753af34d9777537f9ce8cbbd9ddf19cd28e59c544590a5f8b5e1e9958f` |
| `corpus/README.md` | `9def6469ad4078446db03e76641ddab7be353de4f10848665824cf89daf7cc8b` |
| `corpus/knowledge/reader-allocation-r26.md` | `cc653b0fe48f1d5a0f3efa2d61d1e1134d87a36fd67d799f70e07ab963bf5325` |
| `corpus/knowledge/recheck-due-r26.md` | `a0995b7814ddae2a2edf8e25f785de065af674efbb8a337a655feac4c82c7d5e` |
| `corpus/knowledge/registry-link-r26.md` | `248224a270481c49a7fc8a2aaf4b4edf36e061fbea8cc35d3fd715e8f0886d29` |

## Mutant: disable the missing-row warning only

Target: `metadata_registry_check_source`, original `tools/research-gate.sh:2482-2483` in the private archive. The body of the existing missing-row branch alone was replaced with Bash's valid no-op command; the conditional, scan progression, found-ID handling, not-mined branch and used-by branch were left unchanged.

Exact mutation delta (also retained as sandbox `source-missing.patch`):

```diff
--- a/tools/research-gate.sh
+++ b/tools/research-gate.sh
@@ -2482,2 +2482 @@
-      emit_finding META_SOURCE_ROW_MISSING warn metadata \
-        "entry=$entry_base source_id=$source_id registry row missing"
+      :
```

After the mutated run, the exact two original lines were restored in place using the inverse surgical edit, before the restored run.

| Stage | Gate SHA-256 |
|---|---|
| Pristine, also committed target | `c2c813f1b425bc4e74625a2607eaca1b97addf9898f834e88af8f1fe2143abc6` |
| Mutated | `3678d45f9ee3c53185ab688e455bc817bed54ba3be9ad1fd8d6cc8386e50f65c` |
| Restored | `c2c813f1b425bc4e74625a2607eaca1b97addf9898f834e88af8f1fe2143abc6` |

## Expected detector and bounded fixture

The independent expectation is derived from the declared missing-row contract, not from the production branch: S999 is a valid standalone source ID, and the registry has no S999 row. Consequently the gate must emit `META_SOURCE_ROW_MISSING` at warn severity, an entry drift verdict, and final DRIFT/exit 1. The immutable independent oracle must return exactly `{"missing-S999.md":["META_SOURCE_ROW_MISSING"]}` with exit 0.

Final entry, `fixture-root/corpus/knowledge/missing-S999.md`:

```markdown
source: S999 corpus/SOURCES.md#Registry
verified-at: 2026-10-21 checked fixture registry membership
recheck: 90d

## Claim
Fixture for the required missing registry-row warning only.
```

Registry, `fixture-root/corpus/SOURCES.md`:

```markdown
# Isolated registry fixture

| id | status | used-by |
|---|---|---|
| S001 | mined | corpus/knowledge/other.md |
```

The 183-byte final entry and 114-byte registry were unchanged throughout the final pristine/mutated/restored sequence. Their SHA-256 values were respectively `d92e6b0efb89f483088a2b6c15bc67ad14b5d0fc5f8afe612d337c605e328c56` and `a3cfab0ce0ba9a7ee677202a799897755451f5ea01a9c8d5cf85268d7d17fb11`.

The wrapper's SHA-256 was `926c4ba09cf57715dc877ff7ad05bb1565be43d1f61db57b54bbd322f5d0da78` in every run. It invokes the pinned Python oracle and then the gate, with a 15-second timeout each and explicit `LC_ALL=C CHOUSA_STRICT=0`. It checks the oracle's exact expected JSON, the observed finding-ID set, the full S999 warn text, gate exit 1, entry `verdict=drift`, and the exact final one-warning DRIFT summary. Setup/oracle failure or an abnormal gate run (including non-0/1 gate exit, stderr, missing/duplicate entry or summary, or missing completion marker) is INCONCLUSIVE/exit 2, never killed. A completed but behaviorally mismatching gate is detector FAIL/exit 1. Agreement is detector PASS/exit 0.

The same exact detector command, cwd and environment were used for all stages; all child commands, stdout, stderr and exits are retained below. The outer capture used Python `subprocess.run(..., cwd=sandbox, capture_output=True, text=True, timeout=40)`; each capture returned normally. No build, selftest, lint, formatter, large-input amplification probe or other runtime was invoked.

### Initial fixture correction — inconclusive, not a kill

Before any mutation, the first draft of the entry said `source: S999 corpus/SOURCES.md row S999`. That contains **two** S999 tokens. The unmodified gate produced two missing-row warnings and DRIFT/exit 1, while the wrapper required the single-warning summary. The detector therefore exited 1 on pristine bytes. This setup run is **INCONCLUSIVE**, not a killed mutant and not evidence of a production defect. Its raw output is retained below.

Only the fixture source line was then corrected to the single-token form shown above; the detector and production gate remained unchanged. The clean baseline used for the mutation verdict was established after that correction. The initial fixture SHA-256 was `eee728df06336cebcd663ec1c53ce415efc41723dd0dc22d670c6d15798d8380`.

## Results

| Run | Oracle exit | Gate exit | Independent detector exit | Interpretation |
|---|---:|---:|---:|---|
| Initial duplicated-token fixture, pristine gate | 0 | 1 | 1 | Inconclusive fixture/count mismatch; not a kill |
| Final fixture, pristine gate | 0 | 1 | 0 | Valid negative detected; baseline agreement |
| Final fixture, warning disabled | 0 | 0 | 1 | S999 negative missed; independent behavioral mismatch kills mutant |
| Final fixture, restored gate | 0 | 1 | 0 | Negative detected again; exact restoration |

The mutated execution completed normally: one META line, `METADATA_COMPLETE=1/1`, one CLEAN summary and empty stderr. Its detector failure was exactly:

```text
DISAGREE missing-S999 expected=['META_SOURCE_ROW_MISSING'] gate=[] expected_rc=1 gate_rc=0
SOURCE_MISSING_DETECTOR=FAIL
```

This is a behavioral kill, not a syntax-error relabeling. The pristine/restored gate's exit 1 is the expected negative-control outcome, not a regression. The detector's mutated exit 1 is the expected sensitivity failure. No production behavior was falsified by the final S999 fixture; the result demonstrates this narrow independently checked warning is mutation-sensitive.

## Raw captures

The following are unedited detector stdout and stderr captures, including the exact child commands and gate output. The initial setup failure is preserved as well as all three final stages.

### initial-fixture-inconclusive

Cwd: `/tmp/chousa-r26-falsify-FMutateSourceMissingKilled-ZqrJA8t7`

Command: `python3 /tmp/chousa-r26-falsify-FMutateSourceMissingKilled-ZqrJA8t7/detect-source-missing.py`

Detector exit: **1**

```text
ENV LC_ALL=C CHOUSA_STRICT=0
SHA256 926c4ba09cf57715dc877ff7ad05bb1565be43d1f61db57b54bbd322f5d0da78 detect-source-missing.py
SHA256 c2c813f1b425bc4e74625a2607eaca1b97addf9898f834e88af8f1fe2143abc6 tools/research-gate.sh
SHA256 6b2d135c01a8f41b914fb248af35567828336a1a69190560c5df4a07b40f1d78 corpus/evidence/round26-registry-oracle.py
SHA256 eee728df06336cebcd663ec1c53ce415efc41723dd0dc22d670c6d15798d8380 fixture-root/corpus/knowledge/missing-S999.md
SHA256 a3cfab0ce0ba9a7ee677202a799897755451f5ea01a9c8d5cf85268d7d17fb11 fixture-root/corpus/SOURCES.md
COMMAND python3 /tmp/chousa-r26-falsify-FMutateSourceMissingKilled-ZqrJA8t7/corpus/evidence/round26-registry-oracle.py /tmp/chousa-r26-falsify-FMutateSourceMissingKilled-ZqrJA8t7/fixture-root/corpus/knowledge/missing-S999.md --root /tmp/chousa-r26-falsify-FMutateSourceMissingKilled-ZqrJA8t7/fixture-root --registry /tmp/chousa-r26-falsify-FMutateSourceMissingKilled-ZqrJA8t7/fixture-root/corpus/SOURCES.md
ORACLE_EXIT=0
ORACLE_STDOUT_BEGIN
{"missing-S999.md":["META_SOURCE_ROW_MISSING"]}
ORACLE_STDOUT_END
ORACLE_STDERR_BEGIN
ORACLE_STDERR_END
COMMAND bash /tmp/chousa-r26-falsify-FMutateSourceMissingKilled-ZqrJA8t7/tools/research-gate.sh verify-metadata /tmp/chousa-r26-falsify-FMutateSourceMissingKilled-ZqrJA8t7/fixture-root/corpus/knowledge/missing-S999.md --root /tmp/chousa-r26-falsify-FMutateSourceMissingKilled-ZqrJA8t7/fixture-root --registry /tmp/chousa-r26-falsify-FMutateSourceMissingKilled-ZqrJA8t7/fixture-root/corpus/SOURCES.md
GATE_EXIT=1
GATE_STDOUT_BEGIN
research-gate v2 — ts=2026-10-21T12:58:25Z — mode=verify-metadata — path=/tmp/chousa-r26-falsify-FMutateSourceMissingKilled-ZqrJA8t7/fixture-root/corpus/knowledge/missing-S999.md — root=/tmp/chousa-r26-falsify-FMutateSourceMissingKilled-ZqrJA8t7/fixture-root
META entry=missing-S999.md source=present verified_at=dated recheck=scheduled verdict=drift
FINDING META_SOURCE_ROW_MISSING severity=warn surface=metadata obs=entry=missing-S999.md source_id=S999 registry row missing
FINDING META_SOURCE_ROW_MISSING severity=warn surface=metadata obs=entry=missing-S999.md source_id=S999 registry row missing
METADATA_COMPLETE=1/1
RESEARCH_GATE: DRIFT (entries=1 complete=1 findings=2 drift=2)
GATE_STDOUT_END
GATE_STDERR_BEGIN
GATE_STDERR_END
DISAGREE missing-S999 expected=['META_SOURCE_ROW_MISSING'] gate=['META_SOURCE_ROW_MISSING'] expected_rc=1 gate_rc=1
SOURCE_MISSING_DETECTOR=FAIL
```

Detector stderr: `''`

### pristine

Cwd: `/tmp/chousa-r26-falsify-FMutateSourceMissingKilled-ZqrJA8t7`

Command: `python3 /tmp/chousa-r26-falsify-FMutateSourceMissingKilled-ZqrJA8t7/detect-source-missing.py`

Detector exit: **0**

```text
ENV LC_ALL=C CHOUSA_STRICT=0
SHA256 926c4ba09cf57715dc877ff7ad05bb1565be43d1f61db57b54bbd322f5d0da78 detect-source-missing.py
SHA256 c2c813f1b425bc4e74625a2607eaca1b97addf9898f834e88af8f1fe2143abc6 tools/research-gate.sh
SHA256 6b2d135c01a8f41b914fb248af35567828336a1a69190560c5df4a07b40f1d78 corpus/evidence/round26-registry-oracle.py
SHA256 d92e6b0efb89f483088a2b6c15bc67ad14b5d0fc5f8afe612d337c605e328c56 fixture-root/corpus/knowledge/missing-S999.md
SHA256 a3cfab0ce0ba9a7ee677202a799897755451f5ea01a9c8d5cf85268d7d17fb11 fixture-root/corpus/SOURCES.md
COMMAND python3 /tmp/chousa-r26-falsify-FMutateSourceMissingKilled-ZqrJA8t7/corpus/evidence/round26-registry-oracle.py /tmp/chousa-r26-falsify-FMutateSourceMissingKilled-ZqrJA8t7/fixture-root/corpus/knowledge/missing-S999.md --root /tmp/chousa-r26-falsify-FMutateSourceMissingKilled-ZqrJA8t7/fixture-root --registry /tmp/chousa-r26-falsify-FMutateSourceMissingKilled-ZqrJA8t7/fixture-root/corpus/SOURCES.md
ORACLE_EXIT=0
ORACLE_STDOUT_BEGIN
{"missing-S999.md":["META_SOURCE_ROW_MISSING"]}
ORACLE_STDOUT_END
ORACLE_STDERR_BEGIN
ORACLE_STDERR_END
COMMAND bash /tmp/chousa-r26-falsify-FMutateSourceMissingKilled-ZqrJA8t7/tools/research-gate.sh verify-metadata /tmp/chousa-r26-falsify-FMutateSourceMissingKilled-ZqrJA8t7/fixture-root/corpus/knowledge/missing-S999.md --root /tmp/chousa-r26-falsify-FMutateSourceMissingKilled-ZqrJA8t7/fixture-root --registry /tmp/chousa-r26-falsify-FMutateSourceMissingKilled-ZqrJA8t7/fixture-root/corpus/SOURCES.md
GATE_EXIT=1
GATE_STDOUT_BEGIN
research-gate v2 — ts=2026-10-21T12:58:50Z — mode=verify-metadata — path=/tmp/chousa-r26-falsify-FMutateSourceMissingKilled-ZqrJA8t7/fixture-root/corpus/knowledge/missing-S999.md — root=/tmp/chousa-r26-falsify-FMutateSourceMissingKilled-ZqrJA8t7/fixture-root
META entry=missing-S999.md source=present verified_at=dated recheck=scheduled verdict=drift
FINDING META_SOURCE_ROW_MISSING severity=warn surface=metadata obs=entry=missing-S999.md source_id=S999 registry row missing
METADATA_COMPLETE=1/1
RESEARCH_GATE: DRIFT (entries=1 complete=1 findings=1 drift=1)
GATE_STDOUT_END
GATE_STDERR_BEGIN
GATE_STDERR_END
SOURCE_MISSING_DETECTOR=PASS
```

Detector stderr: `''`

### mutated

Cwd: `/tmp/chousa-r26-falsify-FMutateSourceMissingKilled-ZqrJA8t7`

Command: `python3 /tmp/chousa-r26-falsify-FMutateSourceMissingKilled-ZqrJA8t7/detect-source-missing.py`

Detector exit: **1**

```text
ENV LC_ALL=C CHOUSA_STRICT=0
SHA256 926c4ba09cf57715dc877ff7ad05bb1565be43d1f61db57b54bbd322f5d0da78 detect-source-missing.py
SHA256 3678d45f9ee3c53185ab688e455bc817bed54ba3be9ad1fd8d6cc8386e50f65c tools/research-gate.sh
SHA256 6b2d135c01a8f41b914fb248af35567828336a1a69190560c5df4a07b40f1d78 corpus/evidence/round26-registry-oracle.py
SHA256 d92e6b0efb89f483088a2b6c15bc67ad14b5d0fc5f8afe612d337c605e328c56 fixture-root/corpus/knowledge/missing-S999.md
SHA256 a3cfab0ce0ba9a7ee677202a799897755451f5ea01a9c8d5cf85268d7d17fb11 fixture-root/corpus/SOURCES.md
COMMAND python3 /tmp/chousa-r26-falsify-FMutateSourceMissingKilled-ZqrJA8t7/corpus/evidence/round26-registry-oracle.py /tmp/chousa-r26-falsify-FMutateSourceMissingKilled-ZqrJA8t7/fixture-root/corpus/knowledge/missing-S999.md --root /tmp/chousa-r26-falsify-FMutateSourceMissingKilled-ZqrJA8t7/fixture-root --registry /tmp/chousa-r26-falsify-FMutateSourceMissingKilled-ZqrJA8t7/fixture-root/corpus/SOURCES.md
ORACLE_EXIT=0
ORACLE_STDOUT_BEGIN
{"missing-S999.md":["META_SOURCE_ROW_MISSING"]}
ORACLE_STDOUT_END
ORACLE_STDERR_BEGIN
ORACLE_STDERR_END
COMMAND bash /tmp/chousa-r26-falsify-FMutateSourceMissingKilled-ZqrJA8t7/tools/research-gate.sh verify-metadata /tmp/chousa-r26-falsify-FMutateSourceMissingKilled-ZqrJA8t7/fixture-root/corpus/knowledge/missing-S999.md --root /tmp/chousa-r26-falsify-FMutateSourceMissingKilled-ZqrJA8t7/fixture-root --registry /tmp/chousa-r26-falsify-FMutateSourceMissingKilled-ZqrJA8t7/fixture-root/corpus/SOURCES.md
GATE_EXIT=0
GATE_STDOUT_BEGIN
research-gate v2 — ts=2026-10-21T12:59:01Z — mode=verify-metadata — path=/tmp/chousa-r26-falsify-FMutateSourceMissingKilled-ZqrJA8t7/fixture-root/corpus/knowledge/missing-S999.md — root=/tmp/chousa-r26-falsify-FMutateSourceMissingKilled-ZqrJA8t7/fixture-root
META entry=missing-S999.md source=present verified_at=dated recheck=scheduled verdict=clean
METADATA_COMPLETE=1/1
RESEARCH_GATE: CLEAN (entries=1 complete=1 findings=0 drift=0)
GATE_STDOUT_END
GATE_STDERR_BEGIN
GATE_STDERR_END
DISAGREE missing-S999 expected=['META_SOURCE_ROW_MISSING'] gate=[] expected_rc=1 gate_rc=0
SOURCE_MISSING_DETECTOR=FAIL
```

Detector stderr: `''`

### restored

Cwd: `/tmp/chousa-r26-falsify-FMutateSourceMissingKilled-ZqrJA8t7`

Command: `python3 /tmp/chousa-r26-falsify-FMutateSourceMissingKilled-ZqrJA8t7/detect-source-missing.py`

Detector exit: **0**

```text
ENV LC_ALL=C CHOUSA_STRICT=0
SHA256 926c4ba09cf57715dc877ff7ad05bb1565be43d1f61db57b54bbd322f5d0da78 detect-source-missing.py
SHA256 c2c813f1b425bc4e74625a2607eaca1b97addf9898f834e88af8f1fe2143abc6 tools/research-gate.sh
SHA256 6b2d135c01a8f41b914fb248af35567828336a1a69190560c5df4a07b40f1d78 corpus/evidence/round26-registry-oracle.py
SHA256 d92e6b0efb89f483088a2b6c15bc67ad14b5d0fc5f8afe612d337c605e328c56 fixture-root/corpus/knowledge/missing-S999.md
SHA256 a3cfab0ce0ba9a7ee677202a799897755451f5ea01a9c8d5cf85268d7d17fb11 fixture-root/corpus/SOURCES.md
COMMAND python3 /tmp/chousa-r26-falsify-FMutateSourceMissingKilled-ZqrJA8t7/corpus/evidence/round26-registry-oracle.py /tmp/chousa-r26-falsify-FMutateSourceMissingKilled-ZqrJA8t7/fixture-root/corpus/knowledge/missing-S999.md --root /tmp/chousa-r26-falsify-FMutateSourceMissingKilled-ZqrJA8t7/fixture-root --registry /tmp/chousa-r26-falsify-FMutateSourceMissingKilled-ZqrJA8t7/fixture-root/corpus/SOURCES.md
ORACLE_EXIT=0
ORACLE_STDOUT_BEGIN
{"missing-S999.md":["META_SOURCE_ROW_MISSING"]}
ORACLE_STDOUT_END
ORACLE_STDERR_BEGIN
ORACLE_STDERR_END
COMMAND bash /tmp/chousa-r26-falsify-FMutateSourceMissingKilled-ZqrJA8t7/tools/research-gate.sh verify-metadata /tmp/chousa-r26-falsify-FMutateSourceMissingKilled-ZqrJA8t7/fixture-root/corpus/knowledge/missing-S999.md --root /tmp/chousa-r26-falsify-FMutateSourceMissingKilled-ZqrJA8t7/fixture-root --registry /tmp/chousa-r26-falsify-FMutateSourceMissingKilled-ZqrJA8t7/fixture-root/corpus/SOURCES.md
GATE_EXIT=1
GATE_STDOUT_BEGIN
research-gate v2 — ts=2026-10-21T12:59:10Z — mode=verify-metadata — path=/tmp/chousa-r26-falsify-FMutateSourceMissingKilled-ZqrJA8t7/fixture-root/corpus/knowledge/missing-S999.md — root=/tmp/chousa-r26-falsify-FMutateSourceMissingKilled-ZqrJA8t7/fixture-root
META entry=missing-S999.md source=present verified_at=dated recheck=scheduled verdict=drift
FINDING META_SOURCE_ROW_MISSING severity=warn surface=metadata obs=entry=missing-S999.md source_id=S999 registry row missing
METADATA_COMPLETE=1/1
RESEARCH_GATE: DRIFT (entries=1 complete=1 findings=1 drift=1)
GATE_STDOUT_END
GATE_STDERR_BEGIN
GATE_STDERR_END
SOURCE_MISSING_DETECTOR=PASS
```

Detector stderr: `''`

## Restoration and limits

Restoration is evidenced by the restored detector's gate SHA-256 equaling both the pristine archive checksum and the independently obtained `git show` checksum. The restored run also reproduced the required missing-row warning and DRIFT/1. The detector, oracle and final fixture hashes remained identical across the final three stages. No second mutant was attempted.

Raw detector captures are additionally retained as `initial-fixture-inconclusive.stdout.txt`, `pristine.stdout.txt`, `mutated.stdout.txt`, `restored.stdout.txt` and corresponding `.stderr.txt` files in the sandbox, alongside `probe-runs.json`, the detector and exact mutation patch. The report embeds the relevant raw evidence so the /tmp path is not the sole evidence record.

Only the specified bounded source-missing mutation was exercised. Other C3 checks, C1 allocation, C2 arithmetic, composed flags, the frozen populations, full suites and integrated admission were not verified here. This seat neither integrates nor ships. Tools installed/updated: **none**; no package transaction or service operation was performed.
