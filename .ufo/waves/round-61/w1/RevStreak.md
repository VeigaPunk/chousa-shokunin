# RevStreak — round 61 w1 — verification of the recurring-weakness table

Seat: reviewer (leaf, no subagents). Scope: check the claim that a frozen counter was reachable, forgeable or unreachable in rounds 49, 50, 51, 52, 56, 57, 58, 59, 60 and pre-freeze controlled in round 61, against lane lessons, spot-checks, fleet reports and the lane's own receipts. Source proposal: `considerthese/2026-10-26.md` ("Track recurring weaknesses as streaks").
Writes: this report only, plus scratch `/fast/scratch/hyaku/chousa-r61/RevStreak/` (deleted before yield). Counters ran with `python3 -B`, `TMPDIR` on scratch, `--work` on scratch. No git mutation. No network.

## Findings

1. **8 of 10 rows hold as worded**: 49, 50, 51, 52, 57, 58, 60, 61.
2. **Row 56 is not a frozen-counter weakness.** The forgeable state (an alternating "FLIP" forge and an equivalent mutant M9) was in the round-56 *draft* and was fixed before the freeze (`corpus/evidence/round56/claims.md:21-30`). The frozen rule is not shown reachable by do-nothing or forgeable: its controls kill the junk/forge control (`KILLED=1/9 … C1=FAIL`) and the positive reached `C1=PASS` 2/2 before the cache deletion. The post-freeze forge attack (`R56CritC1Forge`) did not run (`('ENV', 2)`), so it is *unmeasured*, not survived. Corrected class: **none at freeze; forge attack unrun**.
3. **Row 59 is mislabelled "frozen".** Round 59 had no claims artifact (`corpus/lessons/round-59.md` header: "none validly frozen"; spot-check conformance). The token-injection weakness belongs to the round-58 `c1-count.py`, re-run as reconnaissance. Class holds (forgeable: stderr interpolation lets an injected `C1=PASS` through with all seven hazards failing, `.ufo/waves/round-59/w1/R59Executor09.md:93,218`). Corrected label: **reused round-58 counter, not a round-59 freeze**.
4. **Row 52 is now ENV-blocked on one leg.** The frozen C1's forge passes the other eight legs today; the ninth (`REAL`) reads a capture from the shokuknow `.qcache`, which is empty since the 2026-10-27 deletion (see row 56 incident). The cited 9/9 receipt predates the deletion. Row holds as "forgeable"; the qualifier is host state, not counter design.
5. **Row 61 holds, with a named forgeable leg.** Controls are committed in the freeze commit and reproduce. C2's `CLAIMS` leg is passed by a claim that echoes its quote (`echo-claims … C2=PASS`, `controls/c2-controls.txt`), which the claims file records as a limit. So "pre-freeze controlled" is true for C1 and for C2's other legs, not for the CLAIMS leg.
6. **Streak pattern (calibration).** Forgeable: 49, 50 (C1), 51, 52, 57, 59 (6 rows). Unreachable: 50 (C2 inference leg for CJK captures), 58. Do-nothing reachable: 60. None: 56, 61. The forgeable class recurs; the lane's own supplements were the only post-freeze discriminators in 49–52.

## Corrected recurring-weakness table

| Round | Class as worded | Verified class | Pointer(s) | Verified how | Status |
|---|---|---|---|---|---|
| 49 | forgeable | forgeable: replay of tool outputs passes C1; hollow quote passes C2 structure | `corpus/lessons/round-49.md` rows 20–21; `corpus/lessons/round-49-verifier-spotcheck.md:45`; `.ufo/waves/round-49/w1/CritForgeC1.md`, `CritForgeC2.md` | cited (seat + spot-check); not re-run | confirmed |
| 50 | forgeable | forgeable (C1, 42-line forge); plus C2 inference leg unreachable for pure-CJK captures | `corpus/lessons/round-50.md` row 18; `…/round-50-verifier-spotcheck.md:36-38`; `.ufo/waves/round-50/w2/R50CritForgeC1.md` | re-run (below): forge `LEGS=5/5 C1=PASS` with `ASSIMILATE_CITES=all` | confirmed |
| 51 | forgeable | forgeable (C1 dirname-keyed forge); C3 pointer check passes any existing file | `corpus/lessons/round-51.md` row 2; `…/round-51-verifier-spotcheck.md:100-104`; `corpus/evidence/round51/c3-count.py:46-48` | re-run: frozen C1 `LEGS=5/5 C1=PASS`; supplement `SUPPLEMENT_LEGS=1/10` | confirmed |
| 52 | forgeable (frozen C1) | forgeable on 8 of 9 legs today; 9/9 pre-deletion | `corpus/lessons/round-52.md` row 3; `…/round-52-verifier-spotcheck.md:34`; `corpus/evidence/round52/controls/forge-shape.py` | re-run: `LEGS=8/9 C1=FAIL`, `REAL=FAIL pinned capture missing` (qcache empty) | confirmed, qualified |
| 56 | reachable/forgeable/unreachable | none at freeze; draft forgeable, fixed pre-freeze; forge attack unrun | `corpus/evidence/round56/claims.md:21-30`; `corpus/lessons/round-56.md` row 1; `…/round-56-verifier-spotcheck.md:43-45` | cited; capture cache gone, not re-run | **corrected** |
| 57 | forgeable (C3 provenance) | forgeable: fabricated `refetch.tsv` success row + replayed bytes → `C3=PASS` | `corpus/lessons/round-57.md:36,72,97-103`; `…/round-57-verifier-spotcheck.md:62,98`; `.ufo/waves/round-57/w2/R57W2CritC3Forge.md` | cited; forge file not committed; not re-run | confirmed |
| 58 | unreachable | unreachable: refusal legs emit `=pass(refused)`, the aggregate tests `=PASS` | `git show c9b08e90:corpus/evidence/round58/c1-count.py` lines 160, 315, 391, 399; `corpus/lessons/round-58.md` Mistake 1 | source read (`ref_pass` requires `=PASS`, no leg emits it); not run | confirmed |
| 59 | frozen counter, token injection | forgeable (token injection) on the round-58 counter; **no round-59 freeze** | `corpus/lessons/round-59.md` header + Mistake 2; `.ufo/waves/round-59/w1/R59Executor09.md:93,218`; `…/round-59-verifier-spotcheck.md` conformance | cited; not re-run | class confirmed; label **corrected** |
| 60 | reachable by do-nothing | do-nothing reaches C1=PASS (`sys.exit(0)` builder); C2 passes on base with no entry | `.ufo/waves/round-60/w1/BuildCounter.md` §B, lines 83–87; `corpus/lessons/round-60.md` Mistake 1 | cited; not re-run | confirmed (plus a separate claim-digest mismatch, a binding defect, not a counter class) |
| 61 | pre-freeze controlled | controlled: controls committed at freeze `1661b85`; reproduce; no stub reaches 20/20 | `corpus/evidence/round61/controls/`; `git show --stat 1661b85`; `…/c2-controls.txt` (echo-claims PASS) | re-run (below) | confirmed; C2 CLAIMS leg known-forgeable |

## Commands run and observed output

Lane tree, read-only:
- `sha256sum corpus/evidence/round61/claims.md` → `9afec8d493f0ba511a256f38cd5098ff508f9ed311c6c49ff5383add9ce0acec` (matches the wave context).
- `git -C … show --stat --format='%h %s' 1661b85` → 17 files under `corpus/evidence/round61/` including `c1-count.py`, `c2-count.py`, `claims.md`, `controls/*` (freeze commit, 18:50:41 -03). `2b0e17b` (18:52:24) amends `c1-count.py`, `claims.md`, `controls/c1-before.txt`, `controls/c1-reference.txt`, adds `controls/sniff-sweep.txt`.
- `git -C … diff --stat 9eef15e HEAD -- tools/build-spans.py` → empty (builder still base; wave not landed).
- `git -C … status --porcelain` → only sibling seat files; nothing from this seat.

Round-61 counters, scratch `--work` (seed 61001, printed builder sha):
- `python3 -B corpus/evidence/round61/c1-count.py --builder tools/build-spans.py --work …/c1base --seed 61001` → `LEGS=7/20 C1=FAIL`, exit 1; failing P03, H07–H17, H20. Matches `controls/c1-before.txt`.
- Same counter, `--builder …/noop0.py` (`import sys; sys.exit(0)`) → `LEGS=1/20 C1=FAIL`, exit 1. Matches the `noop0 legs=1/20` row in `controls/c1-controls.txt`.
- `python3 -B corpus/evidence/round61/c2-count.py` → `ENTRY=0/1 … C2=FAIL`, exit 1; `ROW S134/S135/S136 absent`. Matches `controls/c2-before.txt`.
- Not re-run: `always2` 14/20 (the best do-nothing; no stub reaches 20/20), `forge-token` 7/20, `naive-guard` 10/20, mutants M01–M14, `regress.py`. Receipts only.
- Fact-check: a first attempt used `#!/bin/sh` + `exit 0` written as a `.sh` file and read as `rc=1` for every leg (the counter runs the builder under Python; `exit 0` is not valid Python). Not a finding about the counter; the `.py` stub reproduces 1/20.

Prior-round forge replays against frozen counters (lane tools, read-only, no lane writes):
- `ASSIMILATE_CITES=all python3 -B corpus/evidence/round50/c1-count.py --tool corpus/evidence/round50/controls/forge-tool.py` → `R49_REGRESSION=PASS rc=0`, `LEGS=5/5`, `C1=PASS`, exit 0. Without the variable: `R49_REGRESSION=FAIL rc=1`, `LEGS=4/5`, `C1=FAIL`, exit 1. (Lane's own note: one-shot counters need `ASSIMILATE_CITES=all`.)
- `env -u ASSIMILATE_CITES python3 -B corpus/evidence/round51/c1-count.py --tool corpus/evidence/round51/controls/forge-dirname.py` → `REGISTRY_STRUCTURE=PASS 4/4`, `LEGS=5/5`, `C1=PASS`, exit 0.
- `env -u ASSIMILATE_CITES python3 -B corpus/evidence/round51/c1-supplement.py --tool corpus/evidence/round51/controls/forge-dirname.py` → `ENV_DEFAULT=FAIL 0/3`, `SUPPLEMENT_LEGS=1/10`, `C1_SUPPLEMENT=FAIL`, exit 1 (matches the "forge 1/10" receipt).
- `env -u ASSIMILATE_CITES python3 -B corpus/evidence/round52/c1-count.py --tool corpus/evidence/round52/controls/forge-shape.py` → `REAL=FAIL pinned capture missing or digest differs`, `LEGS=8/9`, `C1=FAIL`, exit 1. The eight non-REAL legs pass for the forge. The REAL leg reads `…/.qcache/3a8b45977cd111e45e3980a5.raw` (`corpus/evidence/round52/c1-count.py:46`).
- `ls -la /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache` → `total 0`, directory mtime `Oct 27 05:41`. Consistent with the round-56 incident.

Source reads (no run):
- `git -C … show c9b08e90:corpus/evidence/round58/c1-count.py`: lines 160 and 315 emit `…=pass(refused)` (`PASS = "pass"`, line 51); line 391 `ref_pass = all(("=PASS" in l) for l in ref_legs)`; line 399 `REFUSE=… sum('=PASS' in l …)`. The verdict therefore cannot reach `PASS` when any refusal leg exists. Round-58 spot-check reached the same reading (`…/round-58-verifier-spotcheck.md`, Claim re-checks).
- `corpus/evidence/round51/c3-count.py:46-48`: a pointer resolves if the path is a file, or a directory with any file. Existence only.

## Verification gaps (not run, cited only)

- Rounds 49, 56, 57, 59, 60 counters and seat forge files: cited from lane lessons and fleet reports; I did not re-run them. R56's forge attack has never run.
- Round-58 counter not executed; the verdict-path reading is by source only.
- Round-52 9/9 receipt is pre-deletion; the current REAL leg cannot be exercised.
- Spot-check closures (`*-verifier-spotcheck.md`) are non-author evidence for the lane's claims; I did not sample their admit/reject decisions.

## Verdict

VERDICT: STREAK_ROWS_CONFIRMED=8/10 corrected=2
