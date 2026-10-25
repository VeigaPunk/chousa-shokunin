# Round 45 verifier spot-check

author: hyaku closure (non-author integrator, @m_flash)
date: 2026-10-25
lane report: `.ufo/reports/round-45/chousa.md`

## Conformance

- Report commit attribution: `git log --format='%an %ae %H' -- .ufo/reports/round-45/chousa.md` → `chousa-shokunin chousa@shokunin.local f7dedb57baa2c8003a1ad4e95d75d1da7cfc87e0` (report present and authored by lane identity).
- Cited lane commits `d82cec904bf0fb8736886b9f17be913c7807427a`, `5e8c7ad2f7b8254d83358820286e3d12ca4672d1`, `2738202b37f05808bce82caba32c03dafaec8a13`, and `25641fffb2c99e47200e48684ad31099d38d3ec4` all exist and are ancestors of `master`; `git merge-base --is-ancestor <hash> master` succeeded for each. The cited base `d29bf47d94149a1b71581eeb0f36d9ff22d41da3` is also an ancestor. The C1 before object `79ee8f29…` is a Git blob, as expected for a tool-blob reference, not a commit.
- `/home/vgpnk/Projects/shokunin/scripts/hyaku/jj-lane.sh state …` → `branch=master local=25641fffb2c99e47200e48684ad31099d38d3ec4 remote=25641fffb2c99e47200e48684ad31099d38d3ec4 ahead=0 behind=0 head=detached tracked=3 untracked=0`. `git status --porcelain` reports three modified inherited paths: `.ufo/waves/round-40/w1/swarm-registry.json`, `.ufo/waves/round-41/w1/swarm-registry.json`, and `corpus/evidence/round41/receipts/cells/cells.json`; the report identifies these as pre-existing left-named state from round 44 and says they remain uncommitted. No round-45 work is left uncommitted.
- Watchdog digest matches report/prompt: `2026-10-25T06:19:59-03:00 launch chousa round=45 pgid=1928892 driver=hyaku-inline attempt=1`; `2026-10-25T07:01:59-03:00 complete chousa round=45; hyaku-inline attempt=1`. No `lane-dead-no-report` line found.
- The dispatched prompt carries the mission/axes binding, 1–3 falsifiable claims and admission rule, L2 floor and route, full report contract including SHONEN, commit-before-report ordering, push scope, L0 side channel, and the five child-lane items (report path, commit-before-report, SHONEN heading, hash citation, write scope). Its wave routing context specifies the policy band; the report says v1 band 32–64, consistent with the prompt's `ufo-wave-policy.json`.
- Report has `SHONEN` heading and four lines, one per box. All are `[~]` author assertions with evidence pointers; none is treated as a non-author check. All four appear checkable from committed files and end-to-end evidence; this is an operator-owned promotion decision, not marked here.
- `git diff d29bf47d94149a1b71581eeb0f36d9ff22d41da3 25641fffb2c99e47200e48684ad31099d38d3ec4 -- SCORECARD.md` adds the round-45 claim/verdict records and trends, without removing or contradicting prior axis evidence. `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` → five W04 duplicate-URL warnings (S051, S053, S073, S074, S075), `chousa ok`, exit 0.

## Claim re-checks

Measurements were re-run over a temporary extraction of `git archive 2738202b37f05808bce82caba32c03dafaec8a13`, not the moving checkout.

| Claim / axis | Re-check and observed output | Verdict |
|---|---|---|
| C1 operability | `python3 corpus/evidence/round45/c1-count.py` → cases `a_empty_exits_3=ok`, `b_ok_exits_0=ok`, `c_timeout_exits_3=ok`, `d_no_timeout_exits_2=ok`, `e_start_timeout_s=ok`; `CASES_MATCH=5/5`, `C1=PASS`, exit 0. This exercises the committed launcher with isolated stub fixtures. Before state is evidence-verified from `controls/c1-control-r44-tool.txt` and frozen control, reported 1/5, exit 1. | improved |
| C2 calibration | `python3 corpus/evidence/round45/c2-count.py --list` → `ENTRY_POINTS=54`, `GATES_ROWS=30`, `REGISTERED=54/54`, `UNREGISTERED=0`, `C2=PASS`, exit 0. Before state is evidence-verified from committed base-tree control: 25/51 and 26 unregistered; freeze-tree control says 29 unregistered. | improved |
| C3 depth | `python3 corpus/evidence/round45/c3-count.py --cache /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache` → `ENTRIES=2/2 CITES_BOUND=3/3 QUOTES_IN_SPAN=4/4 QUOTES_IN_ENTRY=4/4 COUNTS_IN_ENTRY=7/7 CAPTURE_BOUND=4/4 COUNTS_REDERIVED=7/7 C3=PASS`, exit 0. Also `--lane-only --cache /nonexistent` passes with capture checks skipped. Captures were locally re-opened; no live fetch. Before state evidence-verified in `controls/c3-control-do-nothing.txt`: 0/2, exit 1. | improved |

The after measurements above were re-measured; reported before values were checked against committed controls rather than independently reconstructed. No owned axis was harmed. Axis verdicts from the round's SCORECARD: operability improved, calibration improved, depth improved, coverage improved narrowly, freshness unchanged, adjacency unchanged. The report's “improved” freshness/quality learning claims are distinct from the freshness axis: quality is supported by the counter controls, rechecks and fixed-before/after probes; freshness axis remains unchanged because captures predate launch.

## Discernment spot-check

| Item | Decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| Admit: `evidence-archive-field-policy-r41.md` (S082/S083) | admit | On-disk capture `ce16d57277fedfd4f0e7750e.txt` (SHA-256 `8e1f5bff76c14672de04987fcaa6a0fcecfbb493f4c2b6c8f1c3443d91989fe5`) at the located JSON field descriptions; capture `412b146a2720ce6557268d05.txt` (SHA-256 `a3ff65e0db9cc4f2178932ce53965e4cba60c6aab0ba3b1d4ce40020a8a7cf8f`) at the caching sentence and 404 warning. | agree | The README text says “Where possible” for claim archive links and describes evidence archive links without that qualifier; paper text supports evidence-page caching and explicitly warns of 404s. The entry separates source observations from lane inference and records what remains unknown. No external fetch was made. |
| Reject: `evidence-pool-versioning-r39-amendment-2026-10-23.md` | reject | Staged candidate at `/home/vgpnk/Projects/shokuknow/merge/chousa/knowledge/corpus/knowledge/evidence-pool-versioning-r39-amendment-2026-10-23.md`; its cited AVeriTeC dataset-page capture is `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/b73f7e8dd5b0ace740e48046.txt`. | agree | Candidate itself explicitly says it is a dated amendment to a base entry and uses lane-numbered S071/S082 references whose target documents differ under this lane's renumbering. The dataset-page quotes do exist in the capture, so rejection is not based on missing evidence; the actual blockers are the unheld amendment base and unresolved document-bound IDs. The lesson's flip condition (adopt the base in the same round, rebind IDs, locate quotes) is appropriate. |

New SOURCES row quote check: S082's `teaches` grounding quote “Where possible, an archive.org link to the original claim url” is located in the reopened README capture at char 1027 (12 words); it is ≤25 words and supports the scoped teaching claim. S083's cited phrase and S084's capture digest also resolve in committed/on-disk captures.

## Trend verdicts

- **expansion — improved.** Re-measured SOURCES census validation is exit 0; committed registry grows S081→S084 (81→84 rows), and the two listed knowledge entries cite the three new mined rows. The round's coverage map adds two ground areas; no unsupported claim of row quota is used.
- **quality — improved.** C1/C2/C3 committed counters pass on the archived tip; C3's four saved spans are capture-bound and seven values re-derived. The lesson records nine mistakes and correction probes; round-45's described fixes are evidenced by committed controls and after-state.
- **discernment — improved.** Independent spot-check agrees with both sampled decisions for grounded reasons. This is the required outside check; the lane's wave seats alone were not independent.

## Routed defects / next-round queue

- Route D7 to chousa: C3's count/presence counter can pass junk inference text that reuses correct spans and values (`corpus/lessons/round-45.md`, “Limits named, not fixed”); next-round gate should test inference grounding, not just presence.
- Route D8 to chousa: C2 verifies path membership, not row truth, and the frozen entry-point pattern misses executable evidence verifiers (`round-45.md`, “Limits named, not fixed”); extend detection without weakening existing controls.
- Existing inherited left-named modified files and unresolved L0s are explicitly reported as inherited state, not round-45 defects; continue to leave them for their owner/operator.
