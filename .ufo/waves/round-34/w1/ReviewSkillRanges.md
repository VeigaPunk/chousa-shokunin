# E3 — SKILL.md selftest case-range calibration (round 34, W1, ReviewSkillRanges)

Date: 2026-10-23. Seat: ChousaR34.ReviewSkillRanges (leaf, read-only on lane).
Routed defect: `corpus/lessons/round-33-verifier-spotcheck.md:167` — "`SKILL.md:83` "metadata cases 137–154" is stale (CalibrationSkill33)." (also spotcheck:78: the round-33 SKILL.md diff "+18/−12: selftest tally 241 → 251 … `SKILL.md:83` still says metadata cases 137–154 … the report says not fixed").

## Method
1. Ground truth bound to landed gate bytes, not taken on faith:
   - `git clone -q /home/vgpnk/Projects/shokunin/chousa-shokunin /fast/scratch/hyaku/chousa-r34/w1/ReviewSkillRanges/clone && git -C <clone> checkout -q 70feb5eacc959eb98071461fe89f0b892c0810d8` (GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE unset first), exit 0.
   - `sha256sum clone/tools/research-gate.sh` = `43a1af35ca668fe535fcef1e68b0c64bbba3eada59c7a23181f591901fca4346` — byte-identical to lane `tools/research-gate.sh` and equal to the landed round-33 gate prefix `43a1af35ca668fe5`.
   - `timeout 1800 bash tools/research-gate.sh --selftest` in the clone → `EXIT=0`, tail `RESEARCH_GATE_SELFTEST: PASS (251 cases, 0 skipped)`, 165.92 s wall, host UTF-8 locale. Log: `.ufo/waves/round-34/w1/ReviewSkillRanges/selftest-r34.log`.
   - `diff /fast/scratch/hyaku/chousa-r34/probe/selftest-base.log selftest-r34.log` → identical; both sha256 `acf0564af458e7a28cae8f66c1a5e87b2647d29b4b6edcc1722747d21a3bf16f` (receipt `.ufo/waves/round-34/w1/ReviewSkillRanges/selftest-sha256.txt`). So L1's probe log IS the landed gate's case list.
2. Case numbering is sequential at run time (helpers `metadata_case`/`tclaims`/`t` print `ok-case %d` from a `$cases` counter; static comment `tools/research-gate.sh:7096` "round-31 C1 selftest cases (after the r27 matcher-fault case)" confirms the 215→216 boundary), so log order = case numbers.
3. Citation inventory: grep `cases? [0-9]` over SKILL.md (whole file) + manual read of lines 76–115 and 400–589 + a reversed-form grep (`[0-9][–—-]+[0-9]+ (cases?|slots?)`, `slots? [0-9]`) → no additional hits. Inventory below is complete for SKILL.md @ 70feb5ea.

## Verdict per citation
Registry rows (current claims; OK/STALE against the bound 251-case list):

| SKILL.md | Citation | Verdict | Evidence (case names in the bound run) |
|---|---|---|---|
| :77 | `PASS (251 cases)` | OK | log tail `PASS (251 cases, 0 skipped)` |
| :78 | claims cases 21–30 and 41–42 | OK | 21 `claims-pass` … 30 `setup-claims-missing-file`; 41 `claims-boundary-pass`, 42 `claims-boundary-fail` |
| :78 | r31 line-binding cases 216–219 | OK | 216 `c1-pass-bound`, 217 `c1-fail-mislocated`, 218 `c1-fail-invalid-line`, 219 `c1-pass-no-line` |
| :78 | revision-pin cases 220–228 | OK | 220 `claims-sha-absent` … 228 `claims-sha-crlf` |
| :78 | r32 round-31-gap cases 235–241 | OK | 235 `claims-r2-sha-nonstring` … 241 `claims-r2-nested-string` (240 `r2-hash-fault-shim`) |
| :78 | r33 top-level reader cases 242–248; post-falsify fail-closed 249–251 | OK | 242 `r33-top-nested-line` … 248 `r33-top-dup-id`; 249 `r33-post-literals`, 250 `r33-post-nul-dup`, 251 `r33-post-escapes` |
| :79 | chain cases 31–40 and 43–44; r32 exempt-hop 229–232 | OK | 31 `chain-pass` … 40 `setup-chain-missing-file`; 43/44 `chain-{pass,fail}-boundary`; 229–232 `chain-exempt-{resolvable,unresolvable,judgment,mixed}` |
| :80 | sweeps cases 45–54 | OK | 45 `sweeps-pass` … 54 `setup-sweeps-missing-file` |
| :81 | integrity cases 65–73 | OK | 65 `integrity-pass` … 73 `setup-integrity-missing-file` |
| :82 | verify-all cases 55–64 and 74; integrity 65–73; `--json` delimiter 134–136; r32 manifest lock 233–234 | OK | 55–64 `all-*`/`claims-pass.jsonl`/`no-such-record`; 74 `all-dangling`; 134–136 `json-{unterminated,nul-terminated,unreadable}-manifest`; 233/234 `c1lk-{holder-blocks-append,second-append}` |
| :83 | **metadata cases 137–154** | **STALE** | actual metadata-named coverage is **137–208 and 210–215** (78 cases). 155 `metadata-hardlink-refused`, 156 `metadata-stat-unavailable`, 157 `metadata-invalid-calendar`, 158 `metadata-literal-heading`, 159 `metadata-no-content-echo`, 160 `metadata-stable-object`, 161 `metadata-usage`, 162–164 no-final-newline/fenced-heading/heading-boundary, 165–179 `metadata-asof-*` (overdue/current/date-past/event/unknown/boundary/invalid/missing/wrong-mode/leap-2028/leap-2027/large-cadence/date-overflow/invalid-verified-date/refused), 180–187 `metadata-registry-*`, 188–192 `metadata-asof-usage-*` controls, 193–196 unicode-date/128k-zero-prefix, 197–208 registry width/colon-denylist family, 210 `metadata-asof-all-zero-cadence`, 211–214 escaped-pipe/mixed-outer-pipes/delimiter-after-blank, 215 `metadata-asof-usage-matcher-fault`. Case **209 `claims-registry-colon-deny`** sits inside the block but exercises the registry denylist through `verify-claims` — the corrected row should read "metadata cases 137–208 and 210–215" (or "137–215" with 209 named as the claims-surface control). |
| :84 | pin/drift cases 75–85 | OK | 75 `pin-clean` … 85 `setup-pin-drift-exclusive` |

Prose (current-behavior claims):
- :105 `cases 86-92` OK (86–88 `scope-fail-*`, 89–92 `scope-pass-*`). :107 `cases 95-98` OK (claims/chain cap-at/over). :109 case 93 `banner-pin`, case 94 `drift-banner-version` OK. :111 case 101 `claims-hardlink-family`, cases 99-102 OK. :113 cases 103-106, "case 106 is the lane-fallback control" OK (`claims-lane-fallback`). :115 `cases 107–111` OK (`claims-root-slash-{absent,read,xdev}`, `claims-root-dslash`, `sweeps-root-slash`).

Historical, self-labeled tallies (numbering checked; byte-identity is pinned by committed round logs and NOT re-verified here):
- :92 "PASS (161 cases, 0 skipped) (metadata cases 137–161)" — round-25-final frame; consistent: current 137–161 are all `metadata-*`, 161 `metadata-usage`. OK as historical.
- :101-102 "case 154 was revised and seven further case slots added" — matches `corpus/knowledge/metadata-screen-r25.md:103-106` (safe symlink154, multilink155, stat156, calendar157, literal heading158, non-disclosure159, held object160, usage→161) and current names. OK as historical (inside the paragraph :89 explicitly labels "the round-25 tally, not the current one").
- Round tallies :177-178 (r4 44 = 1–40 + 41–44), :213 (r3 40 = 1–30), :251 (r5 45–54), :297-298 (r6 1–54 + 55–64), :342 (r7 1–64 + 65–74), :393-396 (r8 1–74 + 75–85) — all numbering consistent with the current list's family layout. OK as historical.

## Findings
1. **STALE (the routed E3, confirmed):** `SKILL.md:83` "metadata cases 137–154" understates `verify-metadata` selftest coverage by 61 case numbers. Correct range: **137–208 and 210–215** (case 209 `claims-registry-colon-deny` is the claims-surface control inside the block). Note the row contradicts SKILL.md's own :92 (r25 final already 137–161) and the Round27 section's checkpoint total (215 cases, whose tail is exactly this family), so the staleness predates round 33; the round-33 diff (spotcheck:78) merely left it unfixed.
2. **Adjacent (informational, outside SKILL.md, not repaired here):** `corpus/knowledge/metadata-screen-r25.md:5` recheck instruction still says "cases 137–154 pin the arms"; :129-130 correctly scopes "Final selftest coverage is cases 137–161" to r25. Quote (accessed 2026-10-23): "Final selftest coverage is cases 137–161; the header's 137–154".
3. No other citation in SKILL.md is stale. Repair for E3 = one-line edit of SKILL.md:83 (executor/L1 scope; this seat is read-only on lane production files).

## Limits
- Historical "byte-identical to round-N run" prose claims verified by numbering/names only; their byte-identity is owned by committed round logs, not re-run here.
- Family attribution (which cases "are metadata") is by selftest case names + the gate's static case table order; I did not run `verify-metadata` per fixture.
- No installs (none needed). Background processes: selftest job bg_7591 completed (EXIT=0); nothing left running; the failed first launch started no process (empty PID, no log). Scratch clone left at `/fast/scratch/hyaku/chousa-r34/w1/ReviewSkillRanges/clone` (evidence; gate sha pinned above).
- Artifacts: `.ufo/waves/round-34/w1/ReviewSkillRanges/selftest-r34.log` (12.5 KB) and `selftest-sha256.txt`; nothing else written outside my dirs.
