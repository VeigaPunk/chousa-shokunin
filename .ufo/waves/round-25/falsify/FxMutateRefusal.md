# FxMutateRefusal — round-25 refusal mutation probes

Axes: operability (detector sensitivity); constraints: branch specificity, independent mutations, byte-exact restoration.
Private clone: `/tmp/chousa-r25-FxMutateRefusal`; no delegation or production-code edits.
Observed original base (`git rev-parse HEAD`): `0fc037e6b07f3820ead8c9207a8034ac854197a1`.
Observed corrected measured base (`git rev-parse HEAD`): `d8c8cff3923f10481ac9ced66d0af7c41d38130c`.
L1 subsequently named full pin `e93ac711f885a10d44fdd80a1734997419595b5a`; gate unchanged from d8c8cff per L1, so these gate-only probes were not rerun there.
Read limitations: `corpus/lessons/round-25.md:40-47`; `corpus/knowledge/metadata-screen-r25.md:41-46,69-83`. No semantic-screen limitation is claimed as a new regression.

## Packaging evidence retained
- At 0fc037e, `tools/research-gate.sh:5198-5203,5206-5239` has only the old selftest/dispatch; gate SHA-256 `752e4e382ed77c06ac5030ce2179c7ca524934f86fd2a6b25ef946ab027ac553`.
- Command `bash /tmp/chousa-r25-FxMutateRefusal/tools/research-gate.sh --selftest` at 0fc037e: exit 0, `RESEARCH_GATE_SELFTEST: PASS (136 cases, 0 skipped)`; receipt `FxMutateRefusal-pristine.log:137`. Cases 151/152 absent, so no mutant was attempted against that old gate.
- Command `bash /tmp/chousa-r25-FxMutateRefusal/tools/research-gate.sh verify-metadata /tmp/chousa-r25-FxMutateRefusal/corpus/knowledge --root /tmp/chousa-r25-FxMutateRefusal`: exit 2, `research-gate: multiple record paths` at 0fc037e.
- L1's CHECKPOINT CORRECTION attributed this to omitted `tools/research-gate.sh`; its FULL-CHECKPOINT CORRECTION also disclosed omitted `corpus/evidence/README.md` (d8c8cff fixed gate only; e93ac711 restores the evidence index). Second omission is L1-reported, not independently tested by this gate-only seat.

## Same bounded detector, five corrected-gate runs
Detector in every row: `bash /tmp/chousa-r25-FxMutateRefusal/tools/research-gate.sh --selftest` (180-second bound, private-clone cwd; stdout retained in the named receipt).
Both mutant commands first ran `bash -n` with `&&`; syntax checks succeeded and the detector executed all 154 cases, not a parse-error failure.
| State / receipt | Exit | Actual detector output |
|---|---:|---|
| pristine / `FxMutateRefusal-corrected-pristine.log:151-155` | 0 | cases 151/152 ok; `RESEARCH_GATE_SELFTEST: PASS (154 cases, 0 skipped)` |
| canonical mutant / `FxMutateRefusal-canonical-mutated.log:151-160` | 1 | only `FAIL-case metadata-denylist-alias rc=1/1`; `RESEARCH_GATE_SELFTEST: FAIL (1/154 cases)` |
| canonical restored / `FxMutateRefusal-canonical-restored.log:151-155` | 0 | cases 151/152 ok; `RESEARCH_GATE_SELFTEST: PASS (154 cases, 0 skipped)` |
| NUL mutant / `FxMutateRefusal-nul-mutated.log:151-159` | 1 | only `FAIL-case metadata-nul-refused rc=0/1`; `RESEARCH_GATE_SELFTEST: FAIL (1/154 cases)` |
| NUL restored / `FxMutateRefusal-nul-restored.log:151-155` | 0 | cases 151/152 ok; `RESEARCH_GATE_SELFTEST: PASS (154 cases, 0 skipped)` |

- M1, `tools/research-gate.sh:2331`: removed only `|| is_denylist_path "$canon"`, retaining the raw-path check. Expected detector: case 152 `metadata-denylist-alias` (`:5549-5555`). KILLED: expected `reason=denylist unparsed` disappeared; actual finding was `META_ENTRY_REFUSED ... entry=alias.md reason=nul unparsed`, `METADATA_COMPLETE=0/1`, DRIFT (`canonical-mutated.log:152-157`). This is a diagnostic/branch-specific kill, not evidence that the alias became accepted; case 151 still passed.
- M2, `tools/research-gate.sh:2335`: replaced the NUL-probe condition with `elif false; then`; canonical/raw denylist and size checks retained. Expected detector: case 151 `metadata-nul-refused` (`:5543-5548`). KILLED: actual `META entry=meta-nul.md source=present verified_at=dated recheck=scheduled verdict=clean`, `METADATA_COMPLETE=1/1`, `RESEARCH_GATE: CLEAN (entries=1 complete=1 findings=0 drift=0)` (`nul-mutated.log:151-155`); case 152 still passed.
- Exact restoration after EACH mutation: `cmp -s /tmp/chousa-r25-FxMutateRefusal/tools/research-gate.sh /tmp/chousa-r25-FxMutateRefusal/FxMutateRefusal-gate.pristine.sh && sha256sum /tmp/chousa-r25-FxMutateRefusal/tools/research-gate.sh` exited 0 and printed P below, then the restored detector passed. Mutations never overlapped.

## Before / mutant / restored hashes and written files
All paths below are relative to the private clone; P/C/N are full SHA-256 values.
P = `63a39282a15f19f5b0443212e66ad2dfc8ce0315e65697e479a7206879a598b2`.
C = `919cf227d24b0871becc4b3ce5103c220603f5a093bfae64d83dd9338c5e79df`.
N = `d6267b9825efc23e2c98ff9612cbe95b3eb10c2ba257f74cbcf6e88ae031d783`.
M1: P → C → P. M2: P → N → P. Final `tools/research-gate.sh` = P.
Written/modified clone files (selftest temporary fixtures removed by the detector):
- `tools/research-gate.sh` = P; `FxMutateRefusal-gate.pristine.sh` = P.
- `FxMutateRefusal-canonical-mutant.sh` = C; `FxMutateRefusal-nul-mutant.sh` = N.
- `FxMutateRefusal-pristine.log` = `b53891717e8d00fcc47f6e69439063c07e97193bc4be7c6934f13c121979c19f`.
- `FxMutateRefusal-corrected-pristine.log` = `a053be283f9e8d8554325245c37219ab449c37125f186be88b56a7109e8d3665`.
- `FxMutateRefusal-canonical-mutated.log` = `401e858e429f529dc8974d8425c5e35074d11b440bd2680dd4d4c9d0d465a3d3`.
- `FxMutateRefusal-canonical-restored.log` = `a053be283f9e8d8554325245c37219ab449c37125f186be88b56a7109e8d3665`.
- `FxMutateRefusal-nul-mutated.log` = `6f7c0ebe52e94adc424da4fc762bec1149658230f7caba3d2778daa6152dbf76`.
- `FxMutateRefusal-nul-restored.log` = `a053be283f9e8d8554325245c37219ab449c37125f186be88b56a7109e8d3665`.
Live-lane write: this report only; retained mutant snapshots/logs remain private. No claim-admission judgment or integration performed.
VERDICT: Both assigned mutants KILLED at measured d8c8cff (case 152 then case 151); both exact-byte restores and restored 154-case detectors passed. Installs/updates: none.
