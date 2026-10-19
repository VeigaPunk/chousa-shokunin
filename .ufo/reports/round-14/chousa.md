# chousa — round 14 report (2026-10-19)

Goal-wave round (curriculum loop 1, round 3). Work commit
`e17742fa56cb587ecc335e41005507d09d0da787` + correction `0fa4fbf…` (HEAD
when filed; lane identity, local only, no push).

## Work performed

- Opening: claims + before-receipts + the token-plan provider deviation —
  commit `f472dbc`.
- Wave: one batched AgentSwarm call, 64 read-only seats, **alibaba-token-plan
  / deepseek-v4.1-flash** (operator directive), **63/64 completed — seat 54
  (OverflowScout) failed on a provider content-filter 400** (`data_inspection_
  failed`); the deficit is recorded here and in SCORECARD, not backfilled.
  The wave measured the bypass live, validated the unprivileged fixture
  (user+mount namespace tmpfs forge; repo binds inside the ns refused, rc=2),
  BLOCKed the mount-free "absolute-path" fallback as unsound (two seats),
  and pinned the resolving-root rule with the live sweeps-r5 S4 case.
- Parent integration: src_root tracking + one `stat -c '%s %h %d'` probe
  (nlink → size → device), both crit severity arms, chain id arm, docs,
  the ns runner + cases 103–106, receipts, errata.

## Landed changes (each tied to LOG.md round-14 entry)

- `tools/research-gate.sh` (`6b17e50c…` → `d8bbd0bf…`): resolving-root
  tracking, three-arm probe, `CLAIM_/CHAIN_SOURCE_CROSS_DEVICE` (crit),
  header/usage docs, cases 103–106 + ns runner + skip-aware summary.
- New: `corpus/knowledge/mount-alias-r14.md`, four
  `mount-r14-20261019T132025Z-*.log` receipts.
- Errata/records: `hardening-r10.md` round-14 addendum E3 (bind item
  closes; 71 rows → 38·21·9·0·3; queue 25 → 25 with the `--root /` dead-arm
  in) + same-round timestamp correction `0fa4fbf`; corpus/README +
  evidence/README + SKILL.md sweeps.
- `SCORECARD.md`: round-14 verdict block + capabilities row + round-15
  registration.

## Before → after measurements (counting commands in SCORECARD §Round 14)

- Bypass: mounted-alias claim `observed=supported` CLEAN rc=0 (pre-round)
  → `CLAIM_SOURCE_CROSS_DEVICE severity=crit` refused rc=1 (landed), both
  live in unprivileged namespaces.
- Selftest: 102 → 106 (0 skipped); cases 1–102 `cmp` byte-identical.
- Battery: r1 3/3; `GATE_DRIFT: none` vs the r12 baseline (no re-pin);
  masked battery vs the pre-round gate (LANE_ROOT intact) ALL IDENTICAL;
  zero network.

## Cross-domain evidence

None. The `--root /` dead-arm and the sweeps-glob surface are named as
limits/debt, not absorbed.

## SHONEN

- [~] SKILL.md decision tables/error patterns/checklists with cited sources — registry + r12/13/14 paragraphs; pointer: SKILL.md
- [~] End-to-end domain task executed and logged — rounds 2–14 logged; pointer: LOG.md
- [~] Instructions executable without oral context — `--selftest` reproduces; pointer: SCORECARD §Round 14 verdict
- [~] No cross-domain bleed — PROVINCE.md unchanged; pointer: PROVINCE.md

## Seat roster (63/64 completed; model alibaba-token-plan/deepseek-v4.1-flash; one batched call)

| seat | role | deliverable (one line) | verdict |
|---|---|---|---|
| 01 | RoundPlanner | P0–P2 integration sequence; measured the bypass live at HEAD | ADMIT |
| 02 | DeviceAnalyst | st_dev comparison design vs resolving root | ADMIT |
| 03 | FeasibilityScout | userns availability + device census (btrfs 30 / tmpfs 57 / shm 33) | ADMIT |
| 04 | BoundaryReviewScout | quoted r13 residual text with pointers | ADMIT |
| 05 | SemanticsDesigner | id/severity/obs decision table (17 cases) | ADMIT |
| 06 | CorpusDeviceAuditor | zero cross-device citations; validated both fixture recipes | ADMIT |
| 07 | ImplDesigner | validated patch (selftest byte-parity, drift none, live arms A–G) | ADMIT |
| 08 | SelftestDesigner | ns runner + cases 103–106, pre-fix-verified | ADMIT |
| 09 | BypassHunter | 14-route disposition table (same-device bind invisible, overlay root breaks naive rule) | ADMIT |
| 10 | SeverityAnalyst | crit arm placement | ADMIT |
| 11 | ReceiptScout | before-battery verbatim | ADMIT |
| 12 | ByteIdentityAnalyst | head-102 cmp spec | ADMIT |
| 13 | PinInteractionAnalyst | no-pin-perturbation verdict | ADMIT |
| 14 | LaneFallbackAnalyst | lane_r fallback reasoning verified | ADMIT |
| 15 | SkillRowDesigner | SKILL sweep list | ADMIT |
| 16 | LedgerScribe | E3 draft + counts re-derived | ADMIT |
| 17 | ScorecardScribe | verdict-block skeleton | ADMIT |
| 18 | LogScribe | admission skeleton | ADMIT |
| 19 | ReportScribe | this report's skeleton | ADMIT |
| 20 | KnowledgeNoteDesigner | mount-alias-r14.md draft | ADMIT |
| 21 | Adversary (same-device bind) | honest-limit proof | ADMIT |
| 22 | Adversary (toctou-mount) | swap-window confirmation | ADMIT |
| 23 | Adversary (root-device-flux) | fixture robustness analysis | ADMIT |
| 24 | Adversary (false-positive) | cross-device citation census | ADMIT |
| 25 | Adversary (absolute-path) | OUT_OF_CORPUS precedence receipt | ADMIT |
| 26 | Adversary (cap-nlink-order) | probe-order condition (device last) | ADMIT |
| 27 | Adversary (chain-mode) | chain arm verification | ADMIT |
| 28 | Adversary (proc-mounts) | mountinfo candidate assessment | ADMIT |
| 29 | Adversary (fixture-cleanup) | ns cleanup design | ADMIT |
| 30 | Adversary (userns-availability) | liveness probes | ADMIT |
| 31 | Reviewer (claim 1) | acceptance criteria vs real code | ADMIT |
| 32 | Reviewer (claim 2) | depth criteria | ADMIT |
| 33 | Reviewer (cross-claim) | r14×r12/13 hazard table | ADMIT |
| 34 | Reviewer (protocol) | conformance checks | ADMIT |
| 35 | Reviewer (evidence) | r14 receipt set | ADMIT |
| 36 | Reviewer (scope) | boundary scan | ADMIT |
| 37 | Critic (round-level) | false-positive-prone-device-check steelman | ADMIT |
| 38 | Critic (claim 1) | refuse-default defense | ADMIT |
| 39 | Critic (claim 2) | note-overlap management | ADMIT |
| 40 | Critic (minimal-edit) | untestable-check analysis (moot: userns present) | ADMIT |
| 41 | ReceiptScribe2 | r14 runbook | ADMIT |
| 42 | LessonScribe | lesson draft | ADMIT |
| 43 | ManifestScribe | integrator entry JSON | ADMIT |
| 44 | SaturationScribe | window computation | ADMIT |
| 45 | SHONENScribe | SHONEN lines + seed check | ADMIT |
| 46 | L0Scribe | L0 state check | ADMIT |
| 47 | CorpusReadmeScribe | README update draft | ADMIT |
| 48 | IdiomMatcher | style checklist | ADMIT |
| 49 | GitGuardScout | git-state audit | ADMIT |
| 50 | HeaderRegistryScout | registry anchor census | ADMIT |
| 51 | ChainSevScout | chain arms check | ADMIT |
| 52 | DemoScout | before/after demo design (ran the before half) | ADMIT |
| 53 | PerfScout | one-probe cost | ADMIT |
| 54 | OverflowScout | — | FAILED (provider 400 content filter) |
| 55 | FallbackPlanner | token-plan key ladder runbook | ADMIT |
| 56 | BaselineGuardScout | receipt-surface census | ADMIT |
| 57 | NoteDistiller | r13/r14 overlap map | ADMIT |
| 58 | FixtureAuditScout | independent device census | ADMIT |
| 59 | Verifier | drafts consistency pass | ADMIT |
| 60 | Verifier | resolving-root tracking re-derivation | ADMIT |
| 61 | Verifier | case feasibility re-check | ADMIT |
| 62 | Verifier | fallback-path parity proof | ADMIT |
| 63 | ClosureScribe | closure checklist | ADMIT |
| 64 | WaveArchivist | wave-shape paragraph | ADMIT |

## Deviations and honesty notes

- Provider: token-plan key 1 per the operator directive; key ladder and the
  devin/opencode fallbacks recorded in LOG.md.
- Seat 54 failed (provider content filter); 63/64 recorded.
- The mount-free absolute-path fixture was BLOCKed as unsound; the ns forge
  is the only landed fixture shape.
- No re-pin (canonical invocation unchanged; drift none confirms).
- MANIFEST rounds[] round-14 row appended at the fleet root, uncommitted by
  the lane (integrator-sweep precedent).
- Push state: 14 local commits unpushed (operator/integrator-owned).
