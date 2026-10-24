# Round 39 — wave handoff (host mapping)

This seat (L1 chousa r39) holds NO live L2 dispatch tool — the accepted host
mapping (verified across seats 2026-10-24): the hyaku orchestrator dispatches
prepared waves itself between rounds. This directory carries the PREPARED,
VALIDATED wave for round 39:

- `w1-spec.json` — v1 wave, 32 seats, policy v1
  (`scripts/hyaku/ufo-wave-policy.json`, band 32–64). Validator:
  `node ~/Projects/ufo-fsd-alpha/scripts/ufo-swarm-wave.mjs plan --spec
  .ufo/waves/round-39/w1-spec.json` → `counts {spawn:32, resume:0, total:32}`,
  dispatch `{calls:1, kind:task}` (recorded in `w1-plan.json`, rc 0).
- Role mix (32): executor 6, reviewer 6, critic 5, scout 3, scribe 3,
  mutation-tester 3, sentinel 2, revenger 2, connector 1, simplifier 1.
  §3 floor inside the wave: connector (sibling-overlap scan) = ConnectorSiblings;
  executors (write/run code) = Exec{ C1Rederive, C2Rederive, MutantReprobe,
  NoHarm, DoNothingCtl, ReceiptAudit }; scribe 3 (prose surfaces); scout 3
  (per-surface reconnaissance); reviewer 6 + critic 5 (falsify what the
  builders assert); sentinel 2 (scope/environment); revenger 2; mutation-tester
  3; simplifier 1. The planner seat is held by the L1 (validator rejects
  `planner` as a swarm role; the planning data-walk rides ScoutSurfaces /
  ConnectorSiblings).
- The dispatch envelope is exactly ONE `task` call carrying the validator's
  `taskCall` (`context` + `tasks`) unchanged, with
  `UFO_CONFIG_PATH=/home/vgpnk/Projects/shokunin/scripts/hyaku/ufo-wave-policy.json`
  and `UFO_PROJECT_ROOT=/home/vgpnk/Projects/shokunin/chousa-shokunin`.
- Every seat prompt leads with `/skill:godspeed` + the verbatim directive
  bytes (renderer/hook idempotent). Every seat is a leaf (no spawns);
  reportDir `.ufo/waves/round-39/w1` (lane-relative; seats resolve the
  `Report:` trailer under the lane root per the context).

Status at round landing: prepared + validated, NOT dispatched by this seat;
0 dispatched, 0 dead, 0 reports. The L1's own construction runs (disclosed in
`corpus/evidence/round39/claims.md`) supply the committed measurement
evidence; the wave re-derives on fresh seeds when the orchestrator dispatches
it, and wave 2 (falsify, 32 seats) follows under the same policy when wave 1
returns ≥32 distinct attack items.
