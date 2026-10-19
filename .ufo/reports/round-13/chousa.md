# chousa — round 13 report (2026-10-19)

Goal-wave round (curriculum loop 1, round 2). Work+records commit
`5993dc407cb05f16eefe06aa54e94f9a3df82887` (HEAD when filed; lane identity,
local only, no push).

## Work performed

- Opening: before-receipts (no inode logic; 0 multi-linked files in
  corpus/tools/research; battery green) — commit `0b0a133`.
- Wave: one batched AgentSwarm call, 64 read-only seats, opencode-go-6 /
  deepseek-v4.1-flash (standing directive: stick with key 6), 64/64 reports.
  Wave consensus: partner enumeration BLOCKed as unsound (seats 33, 42);
  refuse-on-`nlink != 1` ADMITed as the landing; reviewers re-scoped the
  claim (hardlink class only; bind mounts/TOCTOU/families named).
- Parent integration: one `stat -c '%s %h'` probe at the shared
  `claim_source_path` chokepoint serving the r12 cap AND the new alias check;
  `CLAIM_/CHAIN_SOURCE_MULTILINKED` (crit) with severity arms in
  claim_source_sev and chain_source_sev; 4 selftest cases appended; docs,
  erratum, receipts.

## Landed changes (each tied to LOG.md round-13 entry)

- `tools/research-gate.sh` (`91a01695…` → `6b17e50c…`): combined probe,
  both severity arms, chain id arm, header/usage docs, cases 99–102.
- New: `corpus/knowledge/hardlink-alias-r13.md`,
  `corpus/lessons/2026-10-19-hardlink-alias-boundary.md`, four
  `alias-r13-20261019T123621Z-*.log` receipts.
- Errata/records: `hardening-r10.md` round-13 addendum (row 8 closed(r13,
  hardlink class); 71 rows → 38·22·8·0·3, queue 25); corpus/README
  (carried-residuals line now "all three landed" + knowledge-index row);
  evidence/README receipt rows; SKILL.md (7 table rows 98→102 + the
  round-13 paragraph).
- `SCORECARD.md`: round-13 verdict block + capabilities row + round-14
  registration.

## Before → after measurements (counting commands in SCORECARD §Round 13)

- Bypass: `observed=supported` CLEAN rc=0 (pre-round gate, live) →
  `CLAIM_SOURCE_MULTILINKED severity=crit` refused rc=1 (landed gate).
- Selftest: 98 → 102; cases 1–98 `cmp` byte-identical.
- Battery: r1 3/3; `GATE_DRIFT: none` vs the r12 baseline (no re-pin);
  masked battery vs the pre-round gate (LANE_ROOT intact) ALL IDENTICAL;
  zero network.

## Cross-domain evidence

None. (The fix names kasegi/kengaku/kumitate nowhere; scope refusals stand
orthogonal.)

## SHONEN

- [~] SKILL.md decision tables/error patterns/checklists with cited sources — registry + r12/r13 paragraphs; pointer: SKILL.md
- [~] End-to-end domain task executed and logged — rounds 2–13 logged; pointer: LOG.md
- [~] Instructions executable without oral context — `--selftest` reproduces; pointer: SCORECARD §Round 13 verdict
- [~] No cross-domain bleed — PROVINCE refusals intact; pointer: PROVINCE.md (unchanged this round)

## Seat roster (64/64 completed; model opencode-go-6/deepseek-v4.1-flash; one batched call)

| seat | role | deliverable (one line) | verdict |
|---|---|---|---|
| 01 | RoundPlanner | P0–P3 landing sequence + acceptance commands | ADMIT |
| 02 | HardlinkAnalyst | bypass trace + patch point | ADMIT |
| 03 | BoundaryReviewScout | quoted r2 requirement text | ADMIT |
| 04 | ThreatModelDesigner | refuse semantics + crit parity + MULTILINKED ids | ADMIT |
| 05 | CorpusAuditor | multi-link surface measured (0) | ADMIT |
| 06 | FixtureDesigner | alias/family/control fixture designs | ADMIT |
| 07 | ImplDesigner | combined-probe patch draft | ADMIT |
| 08 | SelftestDesigner | cases 99–102 + guard recipes | ADMIT |
| 09 | BypassHunter | alias-route census | ADMIT |
| 10 | SeverityAnalyst | crit arms design | ADMIT |
| 11 | ReceiptScout | before-battery verbatim | ADMIT |
| 12 | ByteIdentityAnalyst | head-98 cmp spec | ADMIT |
| 13 | PinInteractionAnalyst | no-pin-perturbation proof | ADMIT |
| 14 | QuotaScout | /tmp headroom + fixture costs | ADMIT |
| 15 | SkillRowDesigner | SKILL sweep list | ADMIT |
| 16 | LedgerScribe | row-8 closure draft + counts re-derived | ADMIT |
| 17 | ScorecardScribe | verdict-block skeleton | ADMIT |
| 18 | LogScribe | admission skeleton | ADMIT |
| 19 | ReportScribe | this report's skeleton | ADMIT |
| 20 | KnowledgeNoteDesigner | hardlink-alias-r13.md draft | ADMIT |
| 21 | Adversary (toctou) | stat-then-read attack; documented limit | ADMIT |
| 22 | Adversary (alias-chains) | chain games; order-independence | ADMIT |
| 23 | Adversary (dir-mount) | dir-hardlink EPERM + bind-mount residual | ADMIT |
| 24 | Adversary (partner-in) | in-root family must-pass analysis | ADMIT |
| 25 | Adversary (cap-interplay) | one-stat design condition | ADMIT |
| 26 | Adversary (fixture-traps) | ln/cleanup trap list | ADMIT |
| 27 | Adversary (procfs) | magic-link census | ADMIT |
| 28 | Adversary (false-positive) | family false-positive class | ADMIT |
| 29 | Adversary (chain-mode) | chokepoint coverage confirm | ADMIT |
| 30 | Adversary (sweeps-mode) | sweeps content-free attestation | ADMIT |
| 31 | Adversary (id-namespace) | MULTILINKED naming + surfaces | ADMIT |
| 32 | Adversary (usage-docs) | doc surface enumeration | ADMIT |
| 33 | Adversary (mount-root) | enumeration BLOCK + count-rule verification | BLOCK→folded |
| 34 | Adversary (r12-regression) | r12-survival check list | ADMIT |
| 35 | Reviewer (claim 1) | re-scoped claim + F-limits condition | BLOCK→folded |
| 36 | Reviewer (claim 2) | depth acceptance criteria | ADMIT |
| 37 | Reviewer (cross-claim) | r13×r12 hazard table | ADMIT |
| 38 | Reviewer (protocol) | conformance checks | ADMIT |
| 39 | Reviewer (evidence) | two-evidences receipt set | ADMIT |
| 40 | Reviewer (scope) | boundary-risk scan | ADMIT |
| 41 | Critic (round-level) | reject-steelman + kill-checks | ADMIT |
| 42 | Critic (claim 1) | refuse-vs-resolve; enumeration unsound | BLOCK→folded |
| 43 | Critic (claim 2) | depth-not-padding criteria | ADMIT |
| 44 | Critic (minimal-edit) | fix-vs-document analysis | ADMIT |
| 45 | ReceiptScribe2 | r13 receipt runbook | ADMIT |
| 46 | LessonScribe | lesson draft | ADMIT |
| 47 | ManifestScribe | integrator entry JSON | ADMIT |
| 48 | SaturationScribe | window-state computation | ADMIT |
| 49 | SHONENScribe | SHONEN lines + seed check | ADMIT |
| 50 | L0Scribe | L0 state check (r12 row unanswered) | ADMIT |
| 51 | FixtureReadmeScribe | no-committed-fixture justification | ADMIT |
| 52 | CorpusReadmeScribe | corpus/README update draft | ADMIT |
| 53 | BaselineGuardScout | mask-set proposal | ADMIT |
| 54 | BashPortabilityAnalyst | GNU stat portability check | ADMIT |
| 55 | PerfScout | one-stat cost measurement | ADMIT |
| 56 | IdiomMatcher | r12 style checklist | ADMIT |
| 57 | GitGuardScout | git-state audit | ADMIT |
| 58 | OverflowScout | quota headroom (independent) | ADMIT |
| 59 | HeaderRegistryScout | registry anchor census | ADMIT |
| 60 | ChainSevScout | chain severity arm check | ADMIT |
| 61 | DemoScout | live bypass reproduction design | ADMIT |
| 62 | SemanticsChecker | refusal obs-string candidates | ADMIT |
| 63 | FallbackPlanner | key-6 failure runbook | ADMIT |
| 64 | ClosureScribe | closure checklist | ADMIT |

## Deviations and honesty notes

- Claim re-scoped by the wave (hardlink class only); four limits named, case
  101 pins the family-refusal trade.
- Method artifact recorded: pre-round gate copies must run with LANE_ROOT
  intact (temp copy inside `tools/`); the /tmp-copy form breaks
  lane-root-relative pointer resolution (battery.log header).
- No re-pin: the canonical invocation is byte-unchanged by the probe
  (fixture files are nlink=1 fresh writes); `GATE_DRIFT: none` confirms.
- MANIFEST rounds[] round-13 row appended at the fleet root, uncommitted by
  the lane (integrator sweep requested in the r12 L0 row).
- Push state: 12 local commits unpushed (operator/integrator-owned).
