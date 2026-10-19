# chousa — round 15 report (2026-10-19)

Goal-wave round (curriculum loop 1, round 4). Work commit `dd0951d7…` (HEAD when filed).

## Work performed

- Opening: claims + before-receipts (selftest PASS 106/0-skip; drift none vs r12 baseline; r1 3/3; dead-arm demo `/etc/hostname` refusing `CLAIM_SOURCE_OUT_OF_CORPUS` crit at `CHOUSA_ROOT=/`) — commit `aabf7f4`.
- Wave: one batched AgentSwarm call, 48 read-only seats, **zai glm-5.3-flash** (liveness-probed at opening; fallback ladder devin → token-plan → opencode-go-6 not needed). 48/48 seat reports — zero deficit.
- Parent integration: the `in_root()` helper (`tools/research-gate.sh` ~:612) + three same-class sites converted (`claim_source_path`, `ptr_resolves_meta`, `sweep_path_guarded`) + six-runner `CHOUSA_`-prefixed env-override channel + selftest cases 107–110 + receipts.

## Landed changes (each tied to LOG.md round-15 entry)

- `tools/research-gate.sh` (`d8bbd0bf…` → `dd0951d7…`): `in_root()` helper; `claim_source_path` :1044-1075 prefix tests via `in_root`; `ptr_resolves_meta` :546-551 via `in_root`; `sweep_path_guarded` :1750-1756 via `in_root`; `tcase` override reorder to last-wins; `tclaims`/`tchain`/`tsweeps`/`tintegrity`/`tall` gained `^CHOUSA_[A-Z_]+=` override classifier; cases 107–110 appended.
- New: `corpus/knowledge/root-slash-boundary-r15.md`; `corpus/evidence/root-r15-20261019T152000Z-{demo,selftest,battery,drift}.log`.
- Errata/records: `corpus/knowledge/hardening-r10.md` E4 addendum (the `--root /` queue item closes; queue 25→24); `corpus/README.md` + `corpus/evidence/README.md` + `SKILL.md` sweeps; `SCORECARD.md` verdict block + round-16 registration.

## Before → after measurements (counting commands in SCORECARD §Round 15)

- Dead-arm: absolute in-`/` claim `OUT_OF_CORPUS` crit (pre) → `CLEAN` `1/1` (landed); receipt `root-r15-20261019T152000Z-demo.log`.
- Selftest: 106 → 110 (0 skipped); cases 1–106 `cmp` byte-identical vs `mount-r14-20261019T132025Z-selftest.log`.
- Battery: r1 `3/3`; drift `none` vs the r12 baseline (no re-pin); masked battery vs the pre-round gate ALL IDENTICAL.
- Canary: `claims-r2` under `--root /` `0/17 MISSING` before AND after (byte-stable — the `//`-concat accident keeps the same observed class through a different mechanism).

## Cross-domain evidence

None. All work confined to the chousa province (deep-research method); nothing surfaced routes out per PROVINCE.md.

## SHONEN

- [ ] real decision tables / error patterns / checklists with cited sources — the lane's own assessment `[~]` (the knowledge notes + the gate's finding registry + the selftest fixture tables are the cited decision tables; a fresh lane review is not on file)
- [ ] end-to-end domain task executed and logged — `[~]` (36 rounds of gate development, each with receipts; a fresh lane review is not on file)
- [ ] instructions executable by an agent without oral context — `[~]` (SKILL.md + the gate's `--help` + the corpus README are self-contained; a fresh lane review is not on file)
- [ ] no cross-domain bleed with `PROVINCE.md` still accurate — `[~]` (PROVINCE.md unchanged this round; a fresh lane review is not on file)

## Seat roster (48; model zai glm-5.3-flash; one batched call)

| seat | role | deliverable (one line) | verdict |
|---|---|---|---|
| 01 | RoundPlanner | parent-side integration sequence; site registry (3 sites, 2 pattern forms); edit-order mandate | ADMIT |
| 02 | DeadArmAnalyst | `//*` glob mechanics proven; LANE_ROOT derivation (never `/`) | ADMIT |
| 03 | FixDesigner | `in_root()` helper patch (fenced, style-matched); selftest spec 107–110; harness override prerequisite named | ADMIT |
| 04 | SweepsResolverScout | `sweep_path_guarded` :1741-1743 same-class confirmed; no fourth site | ADMIT |
| 05 | FixtureDesigner | selftest case designs + harness change recommendation | ADMIT |
| 06 | SemanticsChecker | post-fix probe-arm walk verified; `src_root` contract confirmed | ADMIT |
| 07 | RegressionScout | behavior-identity proof for non-`/` roots | ADMIT |
| 08 | ReceiptScout | before-battery verbatim + live dead-arm demo | ADMIT |
| 09 | ByteIdentityAnalyst | head-106 cmp spec + append-only guarantee | ADMIT |
| 10 | PinInteractionAnalyst | canonical `--pin` capture unaffected; no re-pin | ADMIT |
| 11 | HarnessEditScout | six-runner override-channel patch (validated on scratch copy, byte-neutral on 106 cases) | ADMIT |
| 12 | Adversary (empty-normalization) | `//`-input concern real, healed by same fix; harness artifact corrected | ADMIT |
| 13 | Adversary (exact-root-edge) | canon==`/` edge resolves sanely; patch-shape correction surfaced | ADMIT |
| 14 | Adversary (lane-pattern) | lane-side prefix never sees `lane_r=/` | ADMIT |
| 15 | Adversary (device-stat-root) | `stat -c %d /` works; unreadable-root edge documented | ADMIT |
| 16 | Reviewer (claim 1) | acceptance criteria vs real code; verdicts + defects | ADMIT |
| 17 | Reviewer (claim 2) | depth criteria; verdicts + defects | ADMIT |
| 18 | Reviewer (cross-claim) | r15×r12/13/14 hazards; kill-checks | ADMIT |
| 19 | Reviewer (protocol-conformance) | PROTOCOL.md checks; defect list | ADMIT |
| 20 | Reviewer (evidence) | receipt set completeness; pre-registered fix form-sensitive | ADMIT |
| 21 | Critic (round-level) | steelman reject vs fix; recommendation | ADMIT |
| 22 | Critic (claim 1) | fix-form soundness; idiom recommendation | ADMIT |
| 23 | SkillRowDesigner | SKILL.md update spec | ADMIT |
| 24 | KnowledgeNoteDesigner | `root-slash-boundary-r15.md` draft (measured four-outcome table, inline-strip quirk) | ADMIT |
| 25 | LedgerScribe | hardening-r10 E4 addendum draft; phantom-count correction | ADMIT |
| 26 | ScorecardScribe | verdict-block skeleton + §Planned round-16 | ADMIT |
| 27 | LogScribe | LOG admission skeleton; stale receipt-stamp errata found | ADMIT |
| 28 | ReportScribe | this report's skeleton + roster | ADMIT |
| 29 | LessonScribe | lesson draft (recommend fold into r14 lesson) | ADMIT |
| 30 | DemoScout | before/after pair design; BEFORE half run live | ADMIT |
| 31 | ManifestScribe | MANIFEST.json round-15 entry JSON | ADMIT |
| 32 | SHONENScribe | SHONEN lines + seed check | ADMIT |
| 33 | CorpusReadmeScribe | README update draft | ADMIT |
| 34 | IdiomMatcher | style checklist from r13/r14 hunks | ADMIT |
| 35 | GitGuardScout | git-state audit; fleet queue state | ADMIT |
| 36 | HeaderRegistryScout | doc-anchor sweep (header :15-34, usage :314-320) | ADMIT |
| 37 | FallbackPlanner | provider ladder runbook | ADMIT |
| 38 | ScopeBoundaryScout | boundary scan of all 48 seat briefs | ADMIT |
| 39 | Verifier | consistency pass over seats 03/05/11; three defects found | ADMIT |
| 40 | Verifier | ROOT parsing re-derived; `//`-input concern closed | ADMIT |
| 41 | Verifier | boundary-case consumers re-derived; behavior-identity confirmed | ADMIT |
| 42 | Verifier | `/etc/hostname` fixture determinism measured | ADMIT |
| 43 | SaturationScribe | window/capability accounting | ADMIT |
| 44 | L0Scribe | L0 state check (r12 row still open; routed around) | ADMIT |
| 45 | ClosureScribe | closure checklist (ordered) | ADMIT |
| 46 | ReceiptScribe2 | r15 runbook + receipt inventory | ADMIT |
| 47 | WaveArchivist | wave-shape paragraph | ADMIT |
| 48 | BaselineGuardScout | committed-receipt perturbation audit; masked battery plan | ADMIT |

## Deviations and honesty notes

- The pre-registered fix text (`"${root_r%/}"/*`) is a **no-op at `root_r=/`** in `case` patterns on bash 5.3.15 — a quoted operator expansion whose result is empty leaves the adjacent glob non-special. The wave caught this before landing; the `in_root()` helper (materialized local, never inline) is the sound form. LOG.md opening text records the original formula; this report is the correction.
- The `ptr_resolves_meta` :548 site was **not** in the pre-registered claim — found by this round's registry sweep. Covered under the claim's "same class" language; the SCORECARD calibration verdict records it explicitly.
- `/etc/hostname` stat erratum: the opening recorded `17 B`; the live stat at landing is `9 B` (dev/nlink stable at 31/1). Receipts pin the measured value.
- LOG.md:596 carries a stale receipt stamp (`125621Z` vs on-disk `132025Z`) — append-only correction recorded in the LOG round-15 errata bullet.
- The selftest harness's `CHOUSA_ROOT` hardcode clobbered env overrides — a blocker for the `CHOUSA_ROOT=/` cases. Six runners gained a `^CHOUSA_[A-Z_]+=` classifier (the bare `^[A-Z_]+=` form would hijack `VERDICT_BEARING_CLAIMS=` want-tokens); `tcase`'s override placement corrected to last-wins.
