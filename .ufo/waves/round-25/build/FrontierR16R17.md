# FrontierR16R17 — drafted `## Frontier` paragraphs (corpus/README.md)

Scope: read-only draft. Nothing in corpus/README.md was edited. Insert point: between the Round 10 paragraph (README.md:485) and "Still open and integrator/operator-owned" (README.md:487). Round 11–15 and 18–23 paragraphs are also absent; outside this item.

## Draft — Round 16

Round 16 ran the verification move round 15 registered: one 64-seat audit call on openai-codex gpt-6-luna-max (64/64 seat reports, zero deficit) re-audited the boundary stack of rounds 12–15 for correctness defects and missed coverage, and every finding was dispositioned as fix, absorb, or named debt. The before→after observable is the gate at `dd0951d7…` with selftest 110 versus `2b64a1c8…` with `PASS (111 cases, 0 skipped)`: `in_root` now strips every trailing slash, so `--root //` no longer refuses in-corpus paths (case 111 pins it), and the r15 battery receipt was re-run with the correct fixture paths and `--root ..`. The disposition table holds the two fixes, the absorbed record corrections, and the named debts queued for round 17. The holds are drift `none` against the r12 baseline with no re-pin, and the r1 archive observable at three CLEAN verify lines. That observable is not saturated: the wave verified the refusal classes rather than extending them, so coverage is unchanged; the case-111 pin covers the `//` edge but not the `ptr_resolves_meta` root-slash site; the claimed cases 1–110 byte-identity holds only for 1–109 in the receipts; and the round left no r16-stamped selftest, drift, or pre-round battery receipt, so its holds rest on the LOG and SCORECARD statements.

Grounding (Round 16):
- gate `dd0951d7…` → `2b64a1c8…`: SCORECARD.md:805, :811; verification-r16.md:4; .ufo/reports/round-16/chousa.md:13. LOG.md:645 reads `→ <FILL>` (unresolved placeholder).
- selftest 110 → `PASS (111 cases, 0 skipped)`: SCORECARD.md:805, :811; verification-r16.md:4; LOG.md:645.
- 64/64 seat reports: LOG.md:638; .ufo/reports/round-16/chousa.md:8.
- two fixes: verification-r16.md:15–16; case 111 pin: verification-r16.md:77.
- "cases 1–110 cmp byte-identical" (claimed): SCORECARD.md:812; verification-r16.md:5; LOG.md:645. Receipts: root-r15-selftest.log:110 = `sweeps-root-slash`; fence-r17-selftest.log:110 = `claims-root-dslash` (differs); cases 1–109 identical (diff run, this item).
- drift `none`, r1 3/3: LOG.md:645, :654 (no r16 drift receipt exists; root-r15-drift.log:1 is the r15 receipt).
- battery "corrected": verification-r16.md:61–63.

## Draft — Round 17

Round 17 ran the round-16 named debt the verification wave had queued: `load_sections` reset a section on every `## ` line without fence state, so a fenced `## Meta` could shadow the real declaration and the scope screen checked the wrong body. The wave was one 32-seat call on opencode-go / deepseek-v4.1-flash, after xai-oauth failed on quota for all 48 seats and zai glm-5.3-flash was interrupted at 14/48; it landed 27/32 seat reports, with five provider-400 `reasoning_content` failures recorded and not backfilled. The before→after observable is the demo record with a real `domain: bounty program scope` and a fenced `## Meta` declaring `deep-research method`: at `2b64a1c8…` it verifies CLEAN, and at `c2915f24…` it raises `SCOPE_BOUNTY_ABSORBED` (warn) and DRIFT. The two-pass fence pairing (same character must close, closing length at least the opening, 0–3 spaces of indent, an unclosed opener fails closed) is pinned by cases 112–116; the selftest is `PASS (116 cases, 0 skipped)` with cases 1–109 byte-identical to the r15 receipt, drift `none` against the r12 baseline, and the r1 archive observable at three CLEAN verify lines. The `LLM benchmarks` phrase gap stays named debt. That observable is not saturated: the parser is not a Markdown renderer, fenced data rows inside a real section are still trusted, and the round's "masked battery ALL IDENTICAL" compares two runs that both carry DRIFT (claims `0/17`, chain `0/22`, verify-all `drift-sections=3 findings=13` under `root=.`), so the battery's pinned claims and chain observables do not hold in the receipts.

Grounding (Round 17):
- gate `2b64a1c8…` → `c2915f24…`: SCORECARD.md:863, :869; LOG.md:663; fenced-heading-r17.md:4; .ufo/reports/round-17/chousa.md:13.
- demo before CLEAN / after DRIFT + `SCOPE_BOUNTY_ABSORBED`: fence-r17 demo.log:3 and :7–:8.
- selftest `PASS (116 cases, 0 skipped)`: fence-r17 selftest.log:117; cases 112–116 at selftest.log:112–116; fenced-heading-r17.md:5.
- cases 1–109 identical to r15: diff run this item (IDENTICAL_FULL_LINES against root-r15-selftest.log:1–109).
- drift `none`: fence-r17 drift.log:1; SCORECARD.md:879.
- r1 observable: fence-r17 battery.log:2, :4, :6 (CLEAN ×3; the literal token `VERDICT_BEARING_EXPORTS` is not printed in this receipt).
- 27/32 seats, 5 failures: .ufo/reports/round-17/chousa.md:8, :76; LOG.md:659.
- battery: claims `0/17` battery.log:42; chain `0/22` :84; verify-all `root=.` :113, `DRIFT sections=5 run=5 absent=0 drift-sections=3 findings=13` :132–:133. Byte-identical to root-r15-battery.log (133 lines each; diff run).

## Findings (path:line or command+output)

F1 Battery is misrooted, and the r16/r17 "ALL IDENTICAL" and "research corpus resolves" claims do not match the receipts. The replaced battery (root-r15-battery.log) and the r17 battery (fence-r17 battery.log) are byte-identical; both show `RESEARCH_GATE: DRIFT` at :133 with claims `0/17` (:42), chain `0/22` (:84), and `CLAIM_SOURCE_OUT_OF_CORPUS` / `CHAIN_SOURCE_OUT_OF_CORPUS` on `research/deep-research-2026-09-28/*.md`. Observed: `ls research/deep-research-2026-09-28/A-shokunin-tradition.md` at the lane root fails; `../research/deep-research-2026-09-28/A-shokunin-tradition.md` exists. Inference: the battery ran with root `.` (banner :113), so the research pointers cannot resolve. verification-r16.md:61–63 says the research corpus resolves under `--root ..`; that is true only for the archives-r9 lines. Evidence README rows say "ALL IDENTICAL" (corpus/evidence/README.md:642, :646) with no DRIFT note. Not re-run here (no gate execution assigned).
F2 LOG.md:645 `Gate dd0951d7… → <FILL>` is an unresolved placeholder in the append-only round-16 entry; the value is recorded at SCORECARD.md:811 and verification-r16.md:4.
F3 "cases 1–110 cmp byte-identical" (SCORECARD.md:812, :830; verification-r16.md:5; LOG.md:645) is contradicted by receipts: root-r15-selftest.log:110 `sweeps-root-slash` vs fence-r17-selftest.log:110 `claims-root-dslash`. LOG.md:663 corrects the boundary to 109 in the r17 entry; the r16 text is not corrected.
F4 No r16-stamped receipts exist in corpus/evidence/ (listing: no `*r16*`; selftest files stop at root-r15 = 110 cases). "selftest 111", "drift none (r12 baseline)", and the battery-before half are asserted only in LOG.md:645/:654 and SCORECARD.md:805–833.
F5 Current gate file, read-only: `sha256sum tools/research-gate.sh` begins `752e4e38…`. The landed shas are the round-stamp values only; later rounds moved the gate (.ufo/reports/round-18/chousa.md:13 `c2915f24…` → `6e694881…`; LOG.md:681). The README paragraph must label `c2915f24…` as the round-17 landed sha, not current.
F6 Round 16 disposition labels do not partition cleanly: verification-r16.md:22 is labelled **absorb** but its text says "is a named debt"; `grep -c` gives 15 lines with `**absorb**` and 14 with `named debt**`; LOG.md:643–644 says "~15 absorbs, ~12 named debts". The table is the record; the LOG counts are approximate.
F7 Naming mix: fence-r17 demo.log:1 and .ufo/reports/round-17/chousa.md:7 cite the pre-round commit `eaa3bbd`, while LOG.md:663 uses gate sha `2b64a1c8…`. Both are correct for their role (commit vs file sha256 prefix); the README should say which one it cites.

## Files written
- /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-25/build/FrontierR16R17.md (this report; the only file written; no corpus/README.md edit).

## Installs
None. Read-only tools only (read, grep, glob, sha256sum, diff, ls).

VERDICT: Drafts for Round 16 and 17 are grounded in SCORECARD/LOG/knowledge/receipts, but the round-17 battery holds the README must not call green: claims 0/17 and chain 0/22 appear in the receipts under a misrooted `root=.`; the r16 receipts are absent and its 1–110 claim is 1–109.
