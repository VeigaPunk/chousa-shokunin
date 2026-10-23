# CalibrationSkill33 — round 33 wave 2 calibration check

Attacked: every SKILL.md registry row touching research-gate (selftest count, case ranges,
counter rows) and every SHONEN.md box pointer, against repo state at lane tip `0fb300b5c27900ab8bb3abeb5f54776d71e04beb`.
Landed gate `tools/research-gate.sh` sha256 `94a7be5a54dd5cebd9532f2417c4eaedc401c9a0646029dcca8acc445378506e` (verified `sha256sum`).
Base clone `/fast/scratch/hyaku/chousa-r33/w2/CalibrationSkill33/lane` @ `2b9cc73aed30…` — base gate sha256 `f4731885ac0f83076210be364fd443a4378ac88c3b3ef94b5bf1c9e380f003f0` (verified). Round-31 gate extracted from `git show 7a7259f:tools/research-gate.sh` = `0bc318b3e74ac0ad45f4b34154e886d84aebf44673612afab6de5e0b0ff11258` (verified).

## Verified — no mismatch

**Selftest count (rows 77–84 all claim `PASS (248 cases)`).**
`TMPDIR=<scratch> timeout 1800 bash tools/research-gate.sh --selftest` → exit 0,
`RESEARCH_GATE_SELFTEST: PASS (248 cases, 0 skipped)`. Log: `<scratch>/selftest.log` (sha of dir cited; 250 lines).

**Stated case ranges** — all confirmed against the selftest log:
- `SKILL.md:78` claims cases 21–30 & 41–42 → `claims-*` (case names `claims-pass`…`claims-boundary-fail`); r31 216–219 (`c1-*` line-binding) & 220–228 (`claims-sha-*`); r32 235–241 (`claims-r2-*`/`r2-hash-fault-shim`); r33 242–248 (`r33-top-*`). All present at those numbers.
- `SKILL.md:79` chain cases 31–40 & 43–44; r32 exempt-hop 229–232 (`chain-exempt-*`). ✓
- `SKILL.md:80` sweeps cases 45–54. ✓
- `SKILL.md:81` integrity cases 65–73. ✓
- `SKILL.md:82` verify-all 55–64 & 74, `--json` delimiter 134–136 (`json-*-manifest`), r32 lock 233–234 (`c1lk-*`). ✓
- `SKILL.md:84` pin/drift 75–85. ✓

**Pinned values** — spot-checked all against fixture READMEs: `claims=17 supported=13 contradicted=2 unsupported=2 mismatched=0` (`corpus/fixtures/claims-r2.README.md:64-65`, `wc -l corpus/fixtures/claims-r2.jsonl` = 17); `RESOLVED_HOPS=17/22` & `1/2` (`chain-r3.README.md:12,14,88-93`); `VERIFIED_SWEEPS=1/2 REJECTIONS_OK=3/3` (`sweeps-r5.README.md:144`); `refs=16 resolved=15` / `resolved=13 unresolved=2` (`integrity-r7.README.md:136-147`); `metadata-r25` has 28 entries (`ls | wc -l` = 28, consistent with "27 files + README"); r12 baseline header carries `gate_sha256=91a01695…` and `volatile_fields=ts gate_sha256` verbatim (`corpus/evidence/gate-baseline-r12-20261019T115519Z.json:3,6`). Every cited path in rows 77–88 exists (loop `test -e`, all `OK`).

**Counter rows:**
- `SKILL.md:88` (r33 counters): `TOPLEVEL_FIELD_MATCH=156/156` on landed gate — reproduced:
  `C1_TMP=<scratch>/c1tmp1 python3 corpus/evidence/round33/c1-count-v2.py --gate tools/research-gate.sh --seed 3401 --receipt .ufo/waves/round-33/w2/CalibrationSkill33/c1v2-landed-3401.json` → exit 0, `156/156`. Second fresh-seed run seed 3404 → `156/156`, exit 0 (receipt `c1v2-landed-3404.json`). "Before" reproduced: same counter on base-gate copy, seed 3402 → `TOPLEVEL_FIELD_MATCH=60/156`, exit 1, `D1_duplicate_top_level 0/24` (receipt `c1v2-base-3402.json`) — matches row's `f4731885: 60/156`. `EXEMPT_AUDIT_MATCH=132/132`: `C2_TMP=<scratch>/c2tmp3 python3 corpus/evidence/round32/c2-count-v3.py --gate <scratch>/gatelayout/tools/research-gate.sh --seed 3403 --receipt .ufo/waves/round-33/w2/CalibrationSkill33/c2v3-landed-3403.json` → exit 0, `132/132`. Parenthetical "metadata-order control 132/132 under v2, 96/132 under v3" consistent with `SCORECARD.md:1818` (132/132 v2 receipts cited) and committed receipt `.ufo/waves/round-33/w1/ExecD1CounterV3/receipts/v3-metadata-s7331.json` (`label: EXEMPT_AUDIT_MATCH=96/132`).
- `SKILL.md:87` (r32 counters): `c1-count-v2.py` on r31-gate copy seed 3405 → `APPEND_SERIALIZED=0/24` exit 1; `c2-count-v2.py` on r31 gate seed 3406 → `EXEMPT_AUDIT_MATCH=0/132` exit 1 — "before `0bc318b3`: 0/24, 0/132" reproduced exactly. On landed gate copy: `APPEND_SERIALIZED=24/24` exit 0 (seed 3407, receipt `c1v2r32-landed-3407.json`, `gate_sha256=94a7be5a…`), `EXEMPT_AUDIT_MATCH=132/132` exit 0 (seed 3408).
- Kill-rule compliance: every `c1-count-v2.py` run used `--receipt` under `.ufo/waves/round-33/w2/CalibrationSkill33/`, fresh seeds 3401/3402/3404 (none 3301–3373), stdout redirected to file; no run below 156 on landed.

**claims.md citations** (`corpus/evidence/round33/claims.md:18-19`): `json_str`/`json_has_key` at base-gate lines 1109–1128 (`sed -n '1109,1128p' lane/tools/research-gate.sh` — both defs inside); `verify_claims` callers at 1448–1483 (`json_str "$line" id`, `marker_default`, `line`, `sha256` all inside). Correct for the frozen base revision. (On landed gate the same functions are at 1259/1267 and `verify_claims` at 1566 — the cite is a base pin, not a defect.)

**SHONEN.md box pointers** — all resolve:
- `SKILL.md` Gates table exists (`SKILL.md:76` header); `corpus/knowledge/metadata-screen-r25.md` exists with `## Limits` at :69.
- `LOG.md:455` `## Round 9 — archives verified end-to-end`; `corpus/fixtures/archives-r9/` exists.
- `bash tools/research-gate.sh --selftest` runs exit 0 (above); `corpus/evidence/round25-measure-after.log` and `round25-meta-differential.log` exist.
- `PROVINCE.md` exists; `.ufo/waves/round-25/build/ConnectorMetaSiblings.md` exists.
- `claims.md:16` "only scored axis, `SCORECARD.md:7`": `SCORECARD.md` axes table has exactly one row (operability, score 3) at line 7. ✓

## Mismatches (1)

1. **`SKILL.md:83` — stale metadata case range.** Row states "metadata cases 137–154" but the landed
   selftest runs 78 `metadata-*` cases occupying **137–215** contiguously (grep `'metadata-'` over
   `selftest.log` → 78; cases 155–215 include `metadata-hardlink-refused`, `metadata-asof-*`,
   `metadata-registry-*`, `metadata-entry-colon-denylist`, `metadata-unicode-date-*` …). Command:
   `bash tools/research-gate.sh --selftest`; `grep -E 'ok-case +N ' selftest.log`. The row's stated
   range is true as far as it goes but omits 61 of 79 metadata-family cases — a stale
   self-description (also note `claims-registry-colon-deny` at case 209 sits in this block and is
   claimed by no row's range).

## Verdict

**HOLDS with one stale range.** Every selftest count, stated case range (as far as stated), counter
value, "before" value, fixture tally, cited path and SHONEN pointer verified against the landed
revision; the only defect is `SKILL.md:83` naming metadata cases 137–154 when the selftest's
metadata block is 137–215.

## Limits / gaps

- Gate function line numbers cited in `claims.md` are base-revision pins; verified on the base
  gate, not re-anchored to landed (by design — claims.md names the base).
- `SKILL.md:85-86` (quote-reopen tool rows) intentionally out of scope (not research-gate rows);
  their cited files were existence-checked only.
- Fixture-count behavior claims beyond the README tallies (e.g. per-hop verdicts inside the
  fixtures) were trusted to the committed ground-truth docs, not re-executed record by record.
- `c1-count-v2.py` first invocation failed exit 2 (`temp dir` ENOENT) because `C1_TMP` did not
  exist — harness error, no count printed, no receipt written; retried after `mkdir -p`. Not a
  landed-gate run below 156.
- Artifacts: receipts in `.ufo/waves/round-33/w2/CalibrationSkill33/`; logs/clone/copies in
  `/fast/scratch/hyaku/chousa-r33/w2/CalibrationSkill33/` (`selftest.log`, `*.out`, `lane/`,
  `r31gate/`, `gatelayout/`).
- No installs performed; no lane files modified; no background jobs left running.

Report: .ufo/waves/round-33/w2/CalibrationSkill33.md
