# FxMetaDuplicate — round 25 falsification

Checkpoint: private clone `HEAD=e93ac711f885a10d44fdd80a1734997419595b5a`; gate blob `90e43b0293fe04a89f056970a54669c1948c0161` (same at d8c8cff and e93ac7).
Packaging corrections preserved: at 0fc037e, gate blob was `896a13ebc544c03c64985f5a1a21c6f407f86452`; `git grep -c verify_metadata 0fc037e -- tools/research-gate.sh` found none. d8c8cff also omitted the `corpus/evidence/README.md` integration (`git diff --stat d8c8cff e93ac711 -- corpus/evidence/README.md` → `197` lines changed); full pin is e93ac7.

Finding (MEDIUM, operability) — repeated keys are underspecified; gate and oracle diverge:
- Spec v1 says a value ends at “another key line” but does not select which repeated value determines state (`corpus/evidence/round25-claims.md:26-40`). The hardening note repeats that rule without a duplicate policy (`corpus/knowledge/metadata-screen-r25.md:31-49`).
- Gate overwrites `verified_value` / `recheck_value` on each occurrence (`tools/research-gate.sh:2382-2385`); this is observed last-key-wins. The independent oracle explicitly says “v1 does not define duplicates; use the first occurrence” (`corpus/evidence/round25-meta-oracle.py:66-68`).
- Direct disagreement, dated then undated:
  `cd /tmp/chousa-r25-FxMetaDuplicate && bash tools/research-gate.sh verify-metadata scratch-fx/fx-dup-oracle.md` → `META entry=fx-dup-oracle.md source=present verified_at=undated recheck=scheduled verdict=drift`; `FINDING META_VERIFIED_AT_UNDATED ...`; `METADATA_COMPLETE=0/1`; `RESEARCH_GATE: DRIFT (entries=1 complete=0 findings=1 drift=1)`; rc 1.
  `cd /tmp/chousa-r25-FxMetaDuplicate && python3 corpus/evidence/round25-meta-oracle.py scratch-fx/fx-dup-oracle.md` → `META entry=fx-dup-oracle.md source=present verified_at=dated recheck=scheduled verdict=clean`; `METADATA_COMPLETE=1/1`; `RESEARCH_GATE: CLEAN`; rc 0.
- Gate order probes: `fx-verified-dated-undated.md` → `verified_at=undated`, `META_VERIFIED_AT_UNDATED`, `METADATA_COMPLETE=0/1`, rc 1; reversed `fx-verified-undated-dated.md` → `verified_at=dated`, `METADATA_COMPLETE=1/1`, rc 0.
- Recheck order probes: gate scheduled→command (`fx-recheck-sched-cmd.md`) → `recheck=unscheduled`, `META_RECHECK_UNSCHEDULED`, CLEAN/rc 0; command→scheduled (`fx-recheck-cmd-sched.md`) → `recheck=scheduled`, CLEAN/rc 0. Oracle picks the first: respectively `recheck=scheduled` with no finding, then `recheck=unscheduled` with `META_RECHECK_UNSCHEDULED` (both CLEAN/rc 0). Thus its 54/54 claim (`metadata-screen-r25.md:60-65`) does not cover differing duplicate values: the committed 27-fixture set has no file with repeated `source:`, `verified-at:` or `recheck:` lines (per-file count scan returned no rows); selftest metadata cases 137–154 likewise contain no duplicate-key case (`research-gate.sh:5423-5565`).

Counting / masking checks:
- `fx-source-twice.md` gate output has one `META` line (`source=present`) and no duplicate-key finding; ordinary missing verified-at/recheck findings are once each.
- `fx-all-dup.md` contains `recheck: 90d --root ..` then `recheck: bash --selftest`. Output: `META entry=fx-all-dup.md source=present verified_at=undated recheck=unscheduled verdict=drift`; only `META_VERIFIED_AT_UNDATED` and `META_RECHECK_UNSCHEDULED`; `METADATA_COMPLETE=0/1`; `RESEARCH_GATE: DRIFT (entries=1 complete=0 findings=2 drift=1)`. No `META_RECHECK_ROOT_PARENT`: the later value masks the earlier placement debt (`tools/research-gate.sh:2432`).
- Directory command `bash tools/research-gate.sh verify-metadata scratch-fx/dir` → two distinct `META` rows, `METADATA_COMPLETE=0/2`, `RESEARCH_GATE: DRIFT (entries=2 complete=0 findings=4 drift=3)`, rc 1. `grep -c '^META entry='` → `2`; duplicate entry-name count → `0`. Duplicate key occurrences do not double-count entries or findings per occurrence.

Assessment: SPEC AMBIGUITY, not violation of a defined v1 duplicate rule; implementation chooses last-key-wins while the oracle chooses first-key-wins. Undefined duplicate input therefore breaks gate/oracle agreement and can mask `META_RECHECK_ROOT_PARENT`. Residual risk: no duplicate policy/finding is pinned by fixtures or selftest. Verification gap: selftest not rerun (not assigned); no LSP device/server exposed in the available tool inventory, so checks were direct execution plus cited source lines.

Private-clone probe files written/copied (SHA-256):
- `scratch-fx/fx-all-dup.md` 7925ba387cfd15f4d63a628fe2056745a51a781d702b3503495b4adbbad766ab; `scratch-fx/dir/fx-all-dup.md` 7925ba387cfd15f4d63a628fe2056745a51a781d702b3503495b4adbbad766ab.
- `scratch-fx/fx-body-dup.md` 3abca8841600fcd3d9634169f8396c7a6ba120544d11ef758d123310732ef05a; `scratch-fx/fx-dup-oracle.md` c80e3c3f6ba01472a97f58ec1ba4f5518f2701b395cb162b3cca7333850f4cf8.
- `scratch-fx/fx-fence-dup.md` 0cf9661a15aeab4f4dbf63b138159bdcb9b5857815f63a2b941fa3218bf5c76d; `scratch-fx/fx-recheck-cmd-sched.md` 7433349367ca28e0439f883251c41a5acf7cbe895ab9c8a62c486ef5a1e79272.
- `scratch-fx/fx-recheck-sched-cmd.md` c5247a48fd1200b273921623134b75b36daaf8636f1cf3ec46ed9a3f4df56da5; `scratch-fx/fx-source-empty.md` d725477d0d757bddb787dcd9c8b454e87fe4933e721dc0dbbfdce1904d98dffd.
- `scratch-fx/fx-source-twice.md` af2fd071e497f75fde27f9a057d8f23cfa34c6cc6a51dbc7e2b5623f2bfa71e8; `scratch-fx/dir/fx-source-twice.md` af2fd071e497f75fde27f9a057d8f23cfa34c6cc6a51dbc7e2b5623f2bfa71e8.
- `scratch-fx/fx-verified-dated-undated.md` 84ffe0b88c2d9a73d160194f43eab006e14dedd4a2fa5aef23bb573eb142c600; `scratch-fx/fx-verified-undated-dated.md` 31a3a6f00666c2ce0434cd14fb6f70820bd3bada20469fd1647c4fcc665ddcfe.

VERDICT: SPEC AMBIGUITY; last-key-wins in gate conflicts with first-key-wins in oracle on duplicates; entry counts did not double-count.
Installs: none.