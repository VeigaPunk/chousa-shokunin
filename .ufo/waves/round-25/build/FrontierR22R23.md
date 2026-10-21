# FrontierR22R23 — drafted `## Frontier` paragraphs (rounds 22, 23)

Scope: draft only. `corpus/README.md` is NOT edited (leaf member; this report is the only file written). Insertion point: after the "Still open…" paragraph (`corpus/README.md:487-490`) and before the Round 24 paragraph (`:491`), keeping chronological order.

## Draft paragraph — Round 22

Round 22 (loop 1, round 11) ran the move registered at the round-21 landing: one 32-seat AgentSwarm call, which fell back from antigravity gemini-3.8-flash (24 seats on provider errors, 8 aborted) to openai-codex gpt-6-luna-max and returned 32/32 seat reports, on the claim that `is_denylist_path` misses path-start citations of `.config/`, `.omp/` and `.local/state/`. Before (gate `bfc291ef`, selftest 128), `.config/agent-token.txt` closed CLEAN; after (gate `dfb798b4`), the same citation refuses with `CLAIM_SOURCE_SESSION` crit, the bare-start alternatives sitting after the existing `*/X/*` forms. The observables hold: selftest 128 → 132 with cases 1–128 byte-identical to the r21 receipt, `GATE_DRIFT: none` against the r12 baseline (freshness unchanged, no re-pin), and the r1 archive observable at `VERDICT_BEARING_EXPORTS=3/3`. That observable is not saturated: the denylist remains a pattern list, the r21 canonical-target check covers symlink indirection but not the raw path-start form, and the fix closes only the bare-start class of these three directories; `.config-adjacent` stays a non-hit by design (case 132).

Grounding (Round 22):
- wave 32 seats, luna, 24 provider-error + 8 aborted, 32/32 reports: `SCORECARD.md:1137-1140`; `LOG.md:790`, `LOG.md:794`; `.ufo/reports/round-22/chousa.md:8`.
- before `bfc291ef` (= blob sha of commit `10083e1`, verified by `git show 10083e1:tools/research-gate.sh | sha256sum`): `SCORECARD.md:1142-1148`; demo `corpus/evidence/deny-r22-20261019T190000Z-demo.log:1-5` (CLEAN on `.config/agent-token.txt`).
- after `dfb798b4` (= blob sha of `a27128e`, verified by re-run of `git show a27128e:…`): `SCORECARD.md:1150-1156`; demo `deny-r22-…-demo.log:7-12` (`CLAIM_SOURCE_SESSION` crit, `VERDICT_BEARING_CLAIMS=0/1`, DRIFT).
- selftest `PASS (132 cases, 0 skipped)`: `deny-r22-…-selftest.log:133`; cases 1–128 identical to `ptr-r21-…-selftest.log` (checked: `cmp` of first 128 lines IDENTICAL; my re-run at `a27128e` in `/tmp/r25f` also PASS 132, cases 1–128 IDENTICAL to both receipts).
- cases 129–132 (path-start + `.config-adjacent` control): `deny-r22-…-selftest.log:129-132`.
- drift `none`: `deny-r22-…-drift.log:1`; my re-run of `--drift … gate-baseline-r12-20261019T115519Z.json` at `a27128e`: `GATE_DRIFT: none` exit 0.
- r1 `3/3`: NOT present in any r22 receipt (grep for `VERDICT_BEARING_EXPORTS` in `deny-r22-*`/`fanchor-r23-*` returns nothing); asserted at `SCORECARD.md:1156` and `.ufo/reports/round-22/chousa.md:22`. Re-run by me at `a27128e`: `VERDICT_BEARING_EXPORTS=3/3`.
- masked battery "ALL IDENTICAL vs pre-round gate": asserted `SCORECARD.md:1156`, `LOG.md:798`; receipt `deny-r22-…-battery.log` (133 lines) exists; the pre-round comparison itself is not in the receipt and I did not re-run it.
- named limits: `corpus/knowledge/denylist-r22.md:25-31`.
- evidence index rows: `corpus/evidence/README.md:664-667`.

## Draft paragraph — Round 23

Round 23 (loop 1, round 12) ran the fenced-heading anchor move directly, with no wave: the falsifiable before→after had already been measured by the round-20 reproduction. Before (gate `dfb798b4`), `chain_anchor_at` matched a `## Phantom Heading` inside a fenced block as a real anchor and verified the hop at line 4; after (gate `b5d0f93d`), the heading arm tracks fence state inline, and the same record refuses with `anchor-missing`, a `CHAIN_ANCHOR_NOT_FOUND` warn, `RESOLVED_HOPS=0/1`, and DRIFT. Selftest 132 → 133 with cases 1–128 byte-identical to the r22 receipt and case 129 pinning the fenced arm; the r22 path-start cases are renumbered to 130–133. Drift stays `GATE_DRIFT: none` against the r12 baseline, and the r23 masked battery receipt is byte-identical to the r22 one. That observable is not saturated: only the `heading` anchor kind is fence-aware (the `quote` and `line` kinds match literal text by design), fence state resets per call, and the selftest counts fixtures, not the defect space.

Grounding (Round 23):
- direct integration, no wave: `LOG.md:806`; `SCORECARD.md:1191-1194`; `.ufo/reports/round-23/chousa.md:3,7`.
- before `dfb798b4` (= blob sha of commit `fb70ddb`, verified by `git show fb70ddb:tools/research-gate.sh | sha256sum`): `SCORECARD.md:1196-1199`; demo `corpus/evidence/fanchor-r23-20261019T192000Z-demo.log:1-5` (`verified`, `RESOLVED_HOPS=1/1`, line 4). Note: the demo header labels the pre-round gate by commit (`fb70ddb`), SCORECARD by blob sha (`dfb798b4`); same file.
- after `b5d0f93d` (= blob sha of commit `f818652`, verified by `git show f818652:tools/research-gate.sh | sha256sum`): `SCORECARD.md:1201-1205`; demo `fanchor-r23-…-demo.log:7-12` (`anchor-missing`, `CHAIN_ANCHOR_NOT_FOUND` warn, `RESOLVED_HOPS=0/1`, DRIFT).
- selftest `PASS (133 cases, 0 skipped)`: `fanchor-r23-…-selftest.log:134`; cases 1–128 identical to `deny-r22-…-selftest.log` (checked by `cmp`); case 129 `chain-fence-anchor` at `fanchor-r23-…-selftest.log:129`; path-start cases now 130–133 (`:130-133`; r22 had them at 129–132). My re-run at `f818652` in `/tmp/r25f`: `PASS (133 cases)`, lines 1–133 IDENTICAL to the r23 receipt.
- drift `none`: `fanchor-r23-…-drift.log:1`; my re-run at `f818652`: `GATE_DRIFT: none` exit 0.
- r1 `3/3`: not in the r23 receipts (same grep: none); asserted `SCORECARD.md:1205`, `.ufo/reports/round-23/chousa.md:21`. Re-run by me at `f818652`: `VERDICT_BEARING_EXPORTS=3/3`.
- battery: `diff deny-r22-…-battery.log fanchor-r23-…-battery.log` → identical (133 lines each). "ALL IDENTICAL vs pre-round gate" asserted at `SCORECARD.md:1204`, `LOG.md:810`; not re-run.
- named limits: `corpus/knowledge/fenced-anchor-r23.md:23-28`.
- index rows: `corpus/evidence/README.md:668-671`.

## Holds, by the numbers

| item | value | where |
|---|---|---|
| selftest r22 | PASS 132, 0 skipped | `deny-r22-…-selftest.log:133` (re-run `a27128e` ✓) |
| selftest r23 | PASS 133, 0 skipped | `fanchor-r23-…-selftest.log:134` (re-run `f818652` ✓) |
| r1 `VERDICT_BEARING_EXPORTS` | 3/3 at both shas | re-run only (no receipt line) |
| drift vs r12 baseline | `GATE_DRIFT: none` both rounds | receipts `:1`; re-run both shas ✓ |
| live gate now | `752e4e38` (5290 lines), round-24 landing | `LOG.md:826`; `sha256sum tools/research-gate.sh` |

## Findings for the integrator (not edited here)

1. Stale restatement — path-start case numbers. `corpus/README.md:27` ("selftest cases 129–132") and `corpus/knowledge/denylist-r22.md:5` ("cases 129–132 pin the path-start class") are wrong since the round-23 renumbering: current cases are 130–133 (`fanchor-r23-…-selftest.log:130-133`). `SCORECARD.md:1153` and `LOG.md:796` are correct as r22-era history; append-only, leave them.
2. Receipt gap — r1 `3/3` is asserted in r22/r23 SCORECARD, LOG and reports but no r22/r23 receipt carries the `VERDICT_BEARING_EXPORTS` line. The re-runs above confirm it at `a27128e` and `f818652`; a receipt line would close it.
3. Index placement — `corpus/evidence/README.md:664-671` (r22/r23 rows) sit after the `## Round-8 gate-baseline receipts` heading (`:580`) with no round-22/23 heading of their own; the round-24 section has one (`:938`).
4. Missing paragraphs — `corpus/README.md` has no Round 22/23 `## Frontier` paragraphs (`grep '^Round 2[23]'` empty); the drafts above fill that.
5. Label mixing — r22 demo names the pre-round gate by commit `10083e1`, r23 demo by `fb70ddb`; SCORECARD/LOG use blob shas `bfc291ef`/`dfb798b4`. Both pairs verified equal via `git show … | sha256sum`; no error, but a reader comparing the demo header to SCORECARD must map them.
6. Current `corpus/knowledge/denylist-r22.md:3` and `fenced-anchor-r23.md:3` line citations (`:581-592`, `:1514-1560`) match the live gate `752e4e38` (`is_denylist_path()` `:581`, `chain_anchor_at()` `:1514`) — no drift.

## Method and installs

- Live lane not mutated: only `read`, `grep`, `sha256sum`, and `git show`/`git log`/`cat-file` object reads against the lane.
- Re-runs executed in private clone `/tmp/r25f/chousa-shokunin` (clone of the lane; gate blob overwritten there to `a27128e` then `f818652`; `research` symlinked to fleet research read-only). Scratch `TMPDIR=/tmp/r25f/tmp`. Commands: r1 recipe from `corpus/evidence/README.md` re-run snippet, `--selftest`, `--drift … gate-baseline-r12-20261019T115519Z.json`.
- Installs/updates: none.
- Files written: this report only, `.ufo/waves/round-25/build/FrontierR22R23.md`.
