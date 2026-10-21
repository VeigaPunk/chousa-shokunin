# FxMutateMissing — round-25 missing-metadata mutation probe
Axis: operability; safeguards: isolated writes, honest checkpoint attribution, byte-exact restoration. No admission/integration judgment.
Scratch: `/tmp/chousa-r25-FxMutateMissing` (all log/diff paths below are relative to this absolute directory). No production edit except this report; no delegation.
Scope: challenge missing-key detection, not the already-disclosed semantic limitations (`corpus/knowledge/metadata-screen-r25.md:69–83`; `corpus/lessons/round-25.md:46`).

## Checkpoints and packaging failures
- Observed original base: `git -C /tmp/chousa-r25-FxMutateMissing rev-parse HEAD` → `0fc037e6b07f3820ead8c9207a8034ac854197a1`. Gate lacked metadata dispatch (`tools/research-gate.sh:5198–5290` at that pin); assigned selftest → `RESEARCH_GATE_SELFTEST: PASS (136 cases, 0 skipped)` (`original-checkpoint.log:1–12`). Requested mutants were INCONCLUSIVE there, not killed/survived.
- Original gate sha256: `752e4e382ed77c06ac5030ce2179c7ca524934f86fd2a6b25ef946ab027ac553`. L1 acknowledged its omitted gate path and authorized correction, rather than treating the prose's 154-case claim as execution evidence.
- Fetched/switched private clone only; observed corrected HEAD `d8c8cff3923f10481ac9ced66d0af7c41d38130c`. All mutation measurements below are on its actual gate bytes.
- L1's subsequent correction also reports omitted `corpus/evidence/README.md`, repaired in full pin `e93ac711f885a10d44fdd80a1734997419595b5a`; L1 says gate bytes unchanged and gate-only reruns unnecessary. This second packaging finding is L1-reported, not independently remeasured by this gate-only seat.

## Same bounded detector, pristine → mutant → restored
Command every measured phase: `bash /tmp/chousa-r25-FxMutateMissing/tools/research-gate.sh --selftest`, cwd `/tmp/chousa-r25-FxMutateMissing`.
| phase | exit | actual summary | receipt |
|---|---:|---|---|
| corrected pristine | 0 | `PASS (154 cases, 0 skipped)` | `pristine-selftest.log:157–159` |
| M1 suppress missing-recheck finding | 1 | `FAIL (4/154 cases)` | `mutant-recheck-selftest.log:176–178` |
| restored M1 / pristine for M2 | 0 | `PASS (154 cases, 0 skipped)` | `restored-recheck-selftest.log:157–159` |
| M2 suppress missing-source finding | 1 | `FAIL (2/154 cases)` | `mutant-source-selftest.log:167–169` |
| restored M2 | 0 | `PASS (154 cases, 0 skipped)` | `restored-source-selftest.log:157–159` |
Pristine gate SHA256 P = `63a39282a15f19f5b0443212e66ad2dfc8ce0315e65697e479a7206879a598b2`; both restorations returned exactly P before/after their detector runs.
M1 gate SHA256 = `c4371dc208ceb8bd2e69c5a17825b6d4a1b8d68c4ea7593de16a4395de53944c` before/after detector; sequence P → M1 → P.
M2 gate SHA256 = `b1b6b00d4083291bafb2ebdc0a1cbedb5cb2677e771ba5404cce34f7d41e5032` before/after detector; sequence P → M2 → P.

## Separate one-line diffs and failing case lines
M1: delete only `tools/research-gate.sh:2438`; leave `recheck_state=absent; entry_complete=0` unchanged. Full actual diff: `mutant-recheck.diff:1–12`.
```diff
-      emit_finding META_RECHECK_ABSENT warn metadata "entry=$base key=recheck absent"
```
Expected detector: cases 140 (`:5455–5458`) and 148 (`:5531–5535`). Observed both, plus 145 and 146; actual failure headers (`mutant-recheck-selftest.log:142,151,158,164`):
`FAIL-case metadata-no-recheck          rc=0/1 missing:'FINDING META_RECHECK_ABSENT severity=warn surface=metadata obs=entry=meta-no-recheck.md' missing:'META entry=meta-no-recheck.md source=present verified_at=dated recheck=absent verdict=drift'`
`FAIL-case metadata-fenced              rc=1/1 missing:'FINDING META_RECHECK_ABSENT severity=warn surface=metadata obs=entry=meta-fenced.md'`
`FAIL-case metadata-after-heading       rc=0/1 missing:'FINDING META_RECHECK_ABSENT severity=warn surface=metadata obs=entry=meta-after-heading.md' missing:'recheck=absent verdict=drift'`
`FAIL-case metadata-directory           rc=0/1 missing:'META entry=z.md source=present verified_at=dated recheck=absent verdict=drift'`
M2: after M1 restoration/pass, delete only `tools/research-gate.sh:2402`; leave `source_state=absent; entry_complete=0` unchanged. Full actual diff: `mutant-source.diff:1–12`.
```diff
-      emit_finding META_SOURCE_ABSENT warn metadata "entry=$base key=source absent"
```
Expected detector: case 138 (`:5439–5442`). Observed it plus 145; actual headers (`mutant-source-selftest.log:140,151`):
`FAIL-case metadata-no-source           rc=0/1 missing:'FINDING META_SOURCE_ABSENT severity=warn surface=metadata obs=entry=meta-no-source.md' missing:'META entry=meta-no-source.md source=absent verified_at=dated recheck=scheduled verdict=drift'`
`FAIL-case metadata-fenced              rc=1/1 missing:'FINDING META_SOURCE_ABSENT severity=warn surface=metadata obs=entry=meta-fenced.md'`
Both missing-key fixtures incorrectly became `RESEARCH_GATE: CLEAN (entries=1 complete=0 findings=0 drift=0)` under their mutants (`mutant-recheck-selftest.log:146`; `mutant-source-selftest.log:144`). Fenced cases still exited 1 but failed stable finding-ID assertions: not exit-only detection. Both mutants KILLED; these are injected implementation divergences, not spec defects or surviving coverage gaps.

## Every authored private-clone file, final SHA256
Observed with `sha256sum` over these nine absolute scratch paths (gate restored; cloned checkout and Git bookkeeping excluded from this authored-file list):
```text
63a39282a15f19f5b0443212e66ad2dfc8ce0315e65697e479a7206879a598b2  tools/research-gate.sh
716a9a7d017487f5e976df16928c5043aacf9183d70ab0fceba775059f2c2f97  original-checkpoint.log
e2be5c51c41b5323a6b5774dcd5d71624373079411496d3f81d438fa340dd091  pristine-selftest.log
a989e1703e5b46b397de4b958bdf5657118dd1dc23761c244b7edd8fe94f5432  mutant-recheck.diff
0c3cca881864b3e70d5efbc2fe6bfdc3bfa371bdb4fa33b7d14171de276e5300  mutant-recheck-selftest.log
e2be5c51c41b5323a6b5774dcd5d71624373079411496d3f81d438fa340dd091  restored-recheck-selftest.log
d01d6eb0edd879c7ca7eda5fdfbb87c889b551dd42e64366e6afdb24d05ca7a4  mutant-source.diff
f08bf1f674b8246801abe7091a55e031ee1adee94912b3ec4030a11c57261a1c  mutant-source-selftest.log
e2be5c51c41b5323a6b5774dcd5d71624373079411496d3f81d438fa340dd091  restored-source-selftest.log
```
Installs/updates: none. No unassigned suites, production gate runs, or contract changes.
VERDICT: M1 KILLED (140/145/146/148); M2 KILLED (138/145); corrected pristine and both exact restorations PASS 154/154; original 0fc037e packaging failure preserved, later index omission attributed to L1.
