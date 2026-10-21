# FrontierR12R13 — drafted `## Frontier` paragraphs (rounds 12, 13)

Target: `corpus/README.md` `## Frontier` (house style of Round 2–10 and Round 24; README:319–505). Placement: after the Round 10 paragraph (README:473–485) and before the "Still open" paragraph (README:487–490). Not written to README: this seat is read-only.

## Draft — Round 12

Round 12 ran the scope-refusal, operability and calibration move its opening registered, on one 64-seat AgentSwarm wave (opencode-go-6 / deepseek-v4.1-flash, 64/64 seat reports). At `46f5ddb3…` the gate had no scope machinery (`grep -c SCOPE_` → 0), `VERSION=research-gate-r1`, no source-read cap, and selftest `PASS (85 cases)`; at `91a01695…` the declared-scope screen emits three `SCOPE_*` warn findings (`grep -c 'id=SCOPE_'` → 3), the banner reads `VERSION=v2`, claim and chain sources over 8 MiB are refused before any read, and selftest reads `PASS (98 cases)` with cases 1–85 identical to the round-8 receipt's case lines. The baseline was re-pinned once at final bytes with the reason recorded: before the re-pin `--drift` read `GATE_DRIFT: GATE record_sha256` exit 1 by design, and after it reads `GATE_DRIFT: none` exit 0. The pinned observables hold: r1 `3/3`, the fixture battery byte-identical modulo banner and ts, and the A-r9 post-fix `verify-all` CLEAN with `sections=5`. That observable is not saturated either: the scope screen reads only declared `## Meta` rows, so undeclared absorbed scope passes and the solo modes carry no scope teeth; the size cap is bypassed when the stat itself fails; and the pointer-line versus span-line class stays a named non-coverage. Receipt identity remains OPEN.

Numbers (path:line):
- `46f5ddb3…` before, `grep -c SCOPE_` → 0, `VERSION=research-gate-r1`, no cap, selftest 85, r1 `3/3`: SCORECARD.md:520–525.
- `91a01695…` after, `grep -c 'id=SCOPE_'` → 3, `VERSION=v2`, 8 MiB cap, selftest 98, cases 1–85: SCORECARD.md:527–546; receipt corpus/evidence/scope-r12-20261019T115519Z-selftest.log:99 (`PASS (98 cases)`); cases 1–85 identical to the pin-r8 case lines (method in finding 4).
- 64-seat wave, opencode-go-6 / deepseek-v4.1-flash, 64/64: SCORECARD.md:512–513; LOG.md:557.
- Re-pin, `GATE_DRIFT: GATE record_sha256` exit 1 pre-re-pin: corpus/evidence/scope-r12-20261019T115519Z-drift-r8.log:1; `GATE_DRIFT: none` exit 0 after: corpus/evidence/README.md:606; corpus/knowledge/gate-baseline-r12.md:4; SCORECARD.md:541–545.
- Battery byte-identical modulo banner/ts: corpus/evidence/scope-r12-20261019T115519Z-battery.log:2; A-r9 `VERIFY_ALL sections=5 … findings=0`: corpus/evidence/scope-r12-20261019T115519Z-A-fix.log:8.
- Limits: SCORECARD.md:578–585 (solo modes, declaration-only, stat-failure bypass, canonical-invocation-only pin); SCORECARD.md:563, 575 (pointer-line class).
- Receipt identity OPEN: LOG.md:569.

## Draft — Round 13

Round 13 ran the coverage and depth move its opening registered — closure of the last round-2 residual, the in-root hardlink-alias bypass (ledger row 8) — on one 64-seat AgentSwarm wave (opencode-go-6 / deepseek-v4.1-flash, 64/64 seat reports). Two seats BLOCKed partner enumeration as unsound, so the claim was re-scoped to a one-probe `nlink != 1` refusal. Before (`91a01695…`, `grep -c samefile tools/research-gate.sh` → 0), a claim through an in-root hardlink alias of an out-of-root file read `observed=supported` CLEAN with rc=0; after (`6b17e50c…`) the same fixture refuses with `CLAIM_SOURCE_MULTILINKED` severity=crit, `observed=refused`, rc=1. Selftest moved 98 → 102 with cases 1–98 byte-identical to the round-12 receipt, the masked fixture battery was ALL IDENTICAL against the pre-round gate, drift against the round-12 baseline stayed `GATE_DRIFT: none` without a re-pin, and r1 held `3/3`. That observable is not saturated either: the check refuses on link count, so a legitimate in-root multi-link family refuses too (pinned by case 101 as a named trade); bind mounts present nlink=1 and stay invisible to stat; TOCTOU and an unmeasurable stat (alias check skipped) remain named limits. Receipt identity remains OPEN.

Numbers (path:line):
- Opening before-state `91a01695…`, `grep -c samefile` → 0, drift none, r1 `3/3`: SCORECARD.md:629–634; LOG.md:573.
- Bypass before, `observed=supported`, rc=0: corpus/evidence/alias-r13-20261019T123621Z-bypass-before.log:2 and :5.
- Bypass after, `CLAIM_SOURCE_MULTILINKED severity=crit`, `observed=refused`, rc=1: corpus/evidence/alias-r13-20261019T123621Z-bypass-after.log:3–7.
- `6b17e50c…` after; selftest `PASS (102 cases)`: SCORECARD.md:636–637; corpus/evidence/alias-r13-20261019T123621Z-selftest.log:103.
- Battery ALL IDENTICAL: corpus/evidence/alias-r13-20261019T123621Z-battery.log:3; drift `none` no re-pin: SCORECARD.md:645, LOG.md:583.
- Case 101 trade, 64-seat roster, BLOCK: SCORECARD.md:623–627; knowledge/hardlink-alias-r13.md:29–38.
- Limits: corpus/knowledge/hardlink-alias-r13.md:42–52.
- Receipt identity OPEN: LOG.md:587.

## Findings (freshness)

1. Round-13 evidence commit hash never recorded. LOG.md:579 ("evidence commit this entry") and SCORECARD.md:617 ("evidence commit this landing") carry no hash — the same placeholder class LOG.md:567 corrected for r8–r10. git: `5993dc4` = "round 13: hardlink-alias refusal …" (`git log --grep`); `5691bf5` is the round-12 evidence commit (LOG.md:557 correct). Draft cites no hash for r13 for this reason.
2. Conflicting round-13 "before" anchor: SCORECARD.md:629 says re-measured at opening `0b0a133`; LOG.md:573 says "at HEAD 91aebd3". git: `0b0a133` = round-13 opening; `91aebd3` = round-12 report commit. The records disagree on which commit was measured.
3. No standalone receipt for two recorded holds: r1 `3/3` (rounds 12 and 13) and drift `none` vs the r12 baseline at r13. `grep -ril VERDICT_BEARING_EXPORTS corpus/evidence` with 20261019T1[12] names → no match; no `alias-r13-*drift*` file exists. Both holds rest on SCORECARD/LOG prose only. Draft attributes them to SCORECARD/LOG accordingly.
4. "cmp byte-identical" phrasing (scope-r12 selftest receipt, corpus/evidence/README.md:629; alias-r13 README row:632) is method-dependent: raw `cmp` of `pin-r8-…-selftest.log` vs the r12 selftest fails at byte 1 (pin-r8 has a 9-line header, lines 1–9). Extracting `ok-case` lines, cases 1–85 match exactly; the r13 raw head-98 `cmp` matches. Draft says "identical to the round-8 receipt's case lines". The pin-r8 file also carries 96 `ok-case` lines against `PASS (85 cases)` at :103 — not investigated.
5. Current live gate sha256 is `752e4e38…` (`sha256sum tools/research-gate.sh`), not `6b17e50c…`: later rounds changed the gate. Not a round-12/13 defect; draft cites round-time shas only.
6. README gaps outside this item: no Round 11 paragraph and no Round 14–23 paragraphs in `## Frontier` (README:473–491 goes Round 10 → "Still open" → Round 24). README:488 already states the round-12 scope landing inside "Still open"; the drafted paragraphs should precede it.
7. Verified by git: `46f5ddb3…` = `5691bf5^`, `91a01695…` = `5691bf5` and `5993dc4^`, `6b17e50c…` = `5993dc4` (`git show <rev>:tools/research-gate.sh | sha256sum`). Full-hash forms in notes are 16-hex prefixes.

## Method and installs

- Read-only: README:319–505; SCORECARD.md:497–672; LOG.md:529–610; knowledge notes (scope-refusal-r12, gate-baseline-r12, hardlink-alias-r13); corpus/evidence receipts and README:598–671; git log/show (no mutation); sha256sum; cmp/grep.
- Gate not run (selftest and drift were not assigned). Holds quoted from receipts and records only.
- Writes: this file only. No live-lane, git-index or jj mutation.
- Installs: none.

VERDICT: two freshness-grounded paragraphs drafted for r12/r13 with cited numbers; three record defects (missing r13 commit hash, conflicting r13 before-anchor, two holds without receipts) flagged for the integrator to correct before admission.
