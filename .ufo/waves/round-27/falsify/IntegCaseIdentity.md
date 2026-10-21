# Round 27 falsify — IntegCaseIdentity

Item: Integration invariant CaseIdentity at dd72641e574679c4f7882dd43de072b4c8892d6f
(gate sha256 ca39d14d…92f84 confirmed) versus base 64eec5d41c7cf7f17f5ce1e968e28b3769952596.
Invariant: the original 187 selftest calls keep their exact order, names, expected exits and
required diagnostics. New calls come only after case 187. Only the exact old failing predicate
may change, and no existing assertion obligation is removed.

Verdict: **HOLDS**, with one disclosed residual (a narrower predicate) and one dead helper.
Judged axes: operability (C1 harness) and calibration (control strength). No freshness impact.

## Method (static plus bounded sandbox; full selftest NOT run)

Sandbox: `/tmp/chousa-r27-falsify-IntegCaseIdentity/{base,target}` (via `git archive`).

1. `diff -u base/.../research-gate.sh target/.../research-gate.sh` gives 19 hunks. `run_selftest`
   spans base 3366–6247 and target 3391–6525. Three hunks touch it:
   - `local` declarations (new variables only)
   - helper definitions near base line 6007
   - an append block after base's final call `metadata-registry-refused-nul`, and before the
     PASS/FAIL summary.
2. Static case-call extractor (`extract.py`):
   - It finds helpers that increment `cases`: 15 in base, 17 in target. There are no loops
     around case calls.
   - It also counts inline `cases=$((cases + 1))` blocks, and treats `SKIPPED` branches as
     alternatives rather than extra cases.
   - Static totals are base **187** and target **210**, matching the runtime counts.
3. Cross-check against committed runtime logs:
   - The static target order equals all 210 names in `corpus/evidence/round27-selftest-after.log`.
     The only differences are the runtime `setup-` prefix added by `tsetup`.
   - The first 161 static base names equal `round25-retained-final-selftest.log`.
   - `grep '^ok-case' round27-selftest-after.log | head -161 | sha256sum` gives `5eac4a7e…01cb`,
     which equals the r26 `LEGACY_CASES_SHA`.

## Evidence

- **Identity:** the joined text of each base call statement (runner + name + every
  argument, which carries the expected exit and required diagnostics) has sha256
  `ccc06a48…9d80`. Target calls 1–187 have the same hash, and `diff` reports
  exit 0. Calls 188–210 are all new: 5 usage controls, 2 Unicode-date cases, the 128 KiB
  zero-prefix case and its plain variant, 8 registry header/width/S-id cases, 4 colon-denylist
  cases, and the all-zero-cadence case.
- **Changed runner body:** only `metadata_asof_usage_case`. Its third conjunct changed from
  `$out != *'RESEARCH_GATE: '*` to `grep -c '^RESEARCH_GATE: '` == 0, and its FAIL message gained
  a verdict count. Its only original callers are cases **171–173**
  (`metadata-asof-invalid`, `-missing`, `-wrong-mode`). Those are exactly the r26 FAIL3/187 cases.
  They lie outside legacy161, so the claim text "outside those161" is accurate. No passing
  original case uses the changed predicate.
- **Probe of the failing predicate** (`usage_probe.sh`, single gate commands, both gates):
  all three runs give `rc=2 expected_present=1 anchored_verdicts=0 substring_present=1 old_pred=0 new_pred=1`
  on both base and target. The cases failed only because the help line 385
  `Verdict: RESEARCH_GATE: CLEAN|DRIFT` matches the substring. The gate's behaviour on these
  inputs is unchanged; the repair is harness-only.
- **Mutation** (`control_mutant.sh`, a standalone copy of the landed helper plus the 5 controls):
  - `PRED=new`: 0/5 failures.
  - `PRED=old` (base predicate restored): `FAIL-case help-control accepted=0 want=1`, giving
    1/5 failures and rc=1.
  - So reverting the fix makes a control fail.

## Residual (tradeoff, not a CaseIdentity defect)

The anchored count accepts real-looking verdicts that do not start a line. In the
relaxation probes, `PRED=new` accepted 3/3 and `PRED=old` accepted 0/3:

- indented `  RESEARCH_GATE: CLEAN (...)`
- a CR-glued `\r\rRESEARCH_GATE: CLEAN (...)`
- a mid-line `... RESEARCH_GATE: DRIFT (...)`

Today every gate emitter prints the verdict at the start of a line: `printf 'RESEARCH_GATE: …'` at
lines 1050/1473/1760/2112/2301/2802/3059. The anchored form also matches the existing
`tcase`/`tclaims` convention and the C1 claim. So no current output exploits this, and the
invariant permits changing the exact failing predicate. A strict reading of "no obligation
removed" could flag it.

Smallest safe correction (optional): keep the anchored count, and also reject the counted-verdict
shape anywhere in the output. For example, add
`! grep -Eq 'RESEARCH_GATE: (CLEAN|DRIFT) \(' <<<"$out"`. The help line has no ` (`, so it still
passes. Then add one control with an indented verdict.

## Simplifier

- **Dead:** `metadata_asof_usage_accepts()` (target line 6036) is defined but has 0 call sites.
  It duplicates, verbatim, the predicate inlined in `metadata_asof_usage_case`, which risks the two
  copies drifting apart. Delete it, or have `metadata_asof_usage_case` call it.
- All other new helpers and variables are referenced: `is_denylist_{path_value,fs_path,path}`,
  `metadata_asof_usage_control_case`, `metadata_registry_finding_count_case`, `zero_prefix`,
  `unicode_locale`, `candidate_locale`, and `plain_*`.

## Limits

- The full selftest was not run (owned by L1). The pass state comes from the committed after-log.
- The extractor is specific to this file: it requires helpers defined at two-space indent and
  no loops around case calls. It was validated against runtime logs at both 187 and 210.
- Scope is CaseIdentity only. IntegSourceGate and IntegTokenCost belong to other named agents.
- No tools were installed.
