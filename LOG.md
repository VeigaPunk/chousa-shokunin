# chousa-shokunin — Iteration Log

- 2026-10-14 — round 0: minted as shonen (sibling mint; rationale in MINT.md).

## 2026-10-15 — boundary parity fix (round 1 integration prep)

`ScopeBoundary` found a contradiction in the mint artifacts: `MINT.md` and the
roster scan (`mint-roster-scan.json`) explicitly rejected **kumitate** as a
complementary province, but the `PROVINCE.md` and `SKILL.md` refusal clauses this
lane wrote omitted it. Closed here — both files now name orchestration,
multi-agent dispatch and agent lifecycle as refused (→ kumitate). Recorded rather
than silently patched, because the omission had already propagated into peer
proposals (`QualityBar` Q-BOUND, `ApprovalTable`), and the proposed gate vocabulary
classified `SCOPE_ORCHESTRATION_ABSORBED` as `info` where the other two absorbed-
scope ids are `warn` — a severity asymmetry that would let an absorbed orchestration
record pass as CLEAN. **Landing requirement:** that id must be elevated to `warn`
so all three refused provinces have identical gate teeth, with one symmetric
selftest fixture per province asserting exit 1.

## 2026-10-15 — research gate landed (not field-ready)

`tools/research-gate.sh` landed from the round-1 design (994 lines). Two design bugs
were found and fixed while landing:

1. `local sec=$1 line body=${SEC_BODY[$sec]-}` — `local` expands every right-hand
   side before assigning, so `$sec` was unset and `set -u` aborted; **13 of 17**
   selftest cases died on `line 165: sec: unbound variable`. Split the declaration.
2. `ROOT` was captured once at load from the ambient `CHOUSA_ROOT`, but the hermetic
   suite exports it per case and calls `verify_record` as a function — so every
   `lib/…:N` pointer read "missing under CHOUSA_ROOT" and both PASS controls failed.
   `verify_record` now re-reads the env.

After both: `bash tools/research-gate.sh --selftest` → **`RESEARCH_GATE_SELFTEST:
PASS (17 cases)`** exit 0, and the suite's own secrecy case confirms a planted
`sk-` value is not echoed.

**Carried defect, named:** on a real chat-export input the gate exits 1 with **no
verdict line** — an unchecked `grep` under `set -e` ends the script before the
summary. Not field-ready; unblock is to `|| true` every non-fatal `grep` and re-run
the suite plus the real artifact.

### Citation-shift notice (appended 2026-10-15)

The boundary-parity fix inserted **3 lines** into `SKILL.md` at 39–41 (the kumitate
refusal). Every line number below that point moved by +3: the checklist heading is
now `SKILL.md:44` and the four rules are `:46`–`:49` (sweep rule at `:47`), where
the wave's seats cite the pre-edit numbers. **Round-1 citations to `SKILL.md:44` or
later are pre-edit** and must be re-derived before being trusted — the rules
themselves are unchanged. This notice also fixed the lane's own guard, which cited
`SKILL.md:45` for the observation/inference/unknown split; the live line is `:48`.

Also recorded from the same audit: `RuleOrProposal` found several wave-internal
citations that resolve to the wrong lines (QUALITY item numbers used as line numbers;
`claim-ledger.sh:45-48` cited for stamp status where the live lines are `:15-16`;
export chips treated as URLs; `README.md:6-8` credited with a four-tier hierarchy it
does not state). Those are wave-report defects, not lane defects, and they are the
reason the corpus landing must re-derive every citation rather than copy one.

### Skill honesty note (appended 2026-10-15)

`HonestyAudit` measured the peer set at 96 admitted / 34 proposal label instances
and found this skill's own operative rows largely unmarked: **0 `proposal` tokens**
and **0 independently cited admissions** at mint. The four-tier source hierarchy is
this lane's construction — no other lane states it and the survey exports do not —
so it is now marked as a working standard rather than an inherited rule, and any row
warranted only by it is a `proposal` until a real `path:line` backs it. The audit's
citation findings match the shift notice above (18 cites do not say what they claim;
the +3 `SKILL.md` shift moved the checklist).

## 2026-10-15 — round-1 operability: baseline and selected move

At lane commit `34774a1777d4058ca8c2b4456ce2e6ccee9e24c5`, the real
`bash tools/research-gate.sh verify <export> --root ..` CLI was executed over
the three `research/deep-research-2026-09-28/` inputs A/B/C named in `MINT.md:8-13`.
Each returned exit 1, zero stdout bytes, zero stderr bytes, and zero verdict
lines: `VERDICT_BEARING_EXPORTS=0/3`. `SCORECARD.md` now declares the narrow
counting command and initializes the previously absent scorecard; operability is
the sole measured axis, score 0, not an invented overall expertise rating.

The earlier "unchecked grep" diagnosis above is not the demonstrated cause:
`tools/research-gate.sh:68-76` ends `emit_finding` with a conditional strict-mode
branch. A non-strict `info` finding returns 1; `verify_record` invokes that
helper directly for export chrome (`:339-341`) under `set -e` (`:25`).
The selected single improvement is a verdict-preserving informational emitter,
with real-CLI regression coverage and a locally sourced intake example.
No external targets, browser/session state, or domain source writes are required.

### Round-1 dispatch and publication preconditions

The single native OMP `task` batch returned the role seats
`OperabilityPlanner` (planner), `SiblingConnector` (connector),
`ProductionGate`, `CliRegression`, `IntakeExample` (executors),
`EvidenceScribe` (scribe), `LocalSurfaceScout` (scout),
`ContractReviewer` (reviewer), and `ClaimCritic` (critic).
This is the mission-specific heterogeneous batch under the shokunin host
mapping, not a validated generic UFO swarm-wave. Role names, not model aliases,
were passed to the unchanged host router. L2s remain part of the author lane;
their reviews cannot grant promotion marks or an outside discernment check.

Source inputs were pinned by `git -C .. log -1 --format='%H %aI' -- research`
to fleet commit `0863746e9da95457f71b9e00a40361b88ab0df15`.
`sha256sum ../research/deep-research-2026-09-28/{A-shokunin-tradition,B-multiagent-knowledge,C-rank-taxonomy}.md`
returned, in that order:

```text
9033857d4625555c7b778dfad6df80e3e1b24ed8bffa3fee2fd445b9c5540b85
6d8dbddd3e2d2f47dcb153c5a3347cc6321db4afc72cf07da40f0f7fe5022006
e48fe70ff92055c217ac6ca6ce68e403aa5689fee8717f3bd0ccf5badc92321b
```

`git remote -v` in this lane returned no rows; fleet origin is configured as
`https://github.com/VeigaPunk/shokunin.git`. No lane URL was guessed or created.
The operator question is appended to `.ufo/l0-questions.md`, keyed
`chousa | round-1 | Which operator-selected remote URL should chousa-shokunin use?`;
the integrator owns committing that queue. Reachable local work continues.

### Round-1 continuation — observed batch and retained baseline

This execution inherited the uncommitted scorecard and the baseline/precondition
entries above at lane HEAD `34774a1777d4058ca8c2b4456ce2e6ccee9e24c5`.
The scorecard's exact counting command was executed again before any gate edit:
`VERDICT_BEARING_EXPORTS=0/3`. Input hashes and the source commit above were
re-derived with the recorded `sha256sum` and `git -C .. log` commands and matched.

One native OMP `task` call returned nine seats: `RoundOnePlanner` (planner),
`RoundOneConnector` (connector), `GateRuntime`, `SourceIntake`, `CorpusLearning`
(three executors), `RoundOneScribe` (scribe), `RoundOneScout` (scout),
`RoundOneReviewer` (reviewer), and `RoundOneCritic` (critic).
These are the observed seats for this continuation; the earlier seat-name
paragraph is inherited prep, not evidence of these seats' results.
The host binding maps a shokunin batch to `task`; this heterogeneous round
is not represented as a validated generic UFO wave. No model parameter or
routing mutation was used. `~/.omp/agent/config.yml:318-330` is the read host
role-override authority; its current buckets differ from the mission prose.
No model aliases were copied into lane configuration.

The retained cause is the false return from the non-strict `info` branch of
`emit_finding`, not a demonstrated unchecked-`grep` failure. The existing
`tcase` invokes `verify_record` under `set +e` (`tools/research-gate.sh:562-568`
at the baseline), so it does not exercise the CLI's errexit behavior. The
single move couples explicit finding-emitter success to fresh-process CLI
coverage and a local archive-intake specimen. Post-edit results are recorded
only after integration and execution below.

## 2026-10-15 — interactive round-1 reconciliation and integration

Starting HEAD was `34774a1777d4058ca8c2b4456ce2e6ccee9e24c5`.
Inherited modified gate/index/log and untracked scorecard/intake/lesson/input
pins were preserved. The driver's launch counter is not a verified-round count.
The plan is `.ufo/plans/round-1-interactive-20261015T050057Z.md`.

**Dispatch correction to the preceding nine-seat accounts:** the required
round-1 batch already exists as `Shokunin12hP5ChousaR1`. Read-only preserved
fleet artifacts at `.ufo/waves/shokunin12h-20261014-p5-chousa-r1/` show
32 rendered tasks and `task-response.json` saying “Spawned 32”; its safe
progress metadata records content `m_composer`, audits `m_grok`, connectors
`m_antigravity`. The registry under
`.ufo/scopes/Shokunin12hP5ChousaR1/swarm-registry.json` has 32 assignments;
all 32 named reports exist. `ufo-swarm-wave.mjs plan --spec <preserved spec>`
returned exit 0 with spawn=32, resume=0, width=32. Distinct rendered names,
prompts and leading `/skill:godspeed` prefixes each count 32. Full per-member
source hashes/dispositions are in `.ufo/evidence/round-1/wave-reconciliation.json`;
the revalidated plan is `wave-plan.json` beside it. No new task call was made.
Later nine-seat calls are advisory, not replacement or completion evidence.
The old registry drops actual `-2` suffixes for CorpusMap, FindingIds and
GateRegistryRow; local reconciliation records the response IDs without
mutating the shared registry. Spawn-time `pending` is not a current liveness
claim; member report files, not a re-probe of native sessions, are observed.

The current global role defaults would misroute a **new** wave; this does not
invalidate the existing dispatch-time bindings. The initial interactive plan's
round-1 route-blocker classification is superseded by its reconciliation
correction. No route overlays, global settings, source trees, session bodies
or shared reports were changed. The already reported Phase 0 failures were
not rerun and no native judgment is claimed.

The one improvement preserves the inherited explicit-success finding emitter
and real-CLI fixture harness. Integration review found a fixture name mismatch:
`pass-export-chrome.md` was created but `pass-export-chrome-lenient.md` was
requested. The invocation now uses the created file. Comments were shortened
to the invariant; broad grep suppression was not introduced. Acceptance and
real CLI outcomes are not pre-claimed; they are recorded after execution.

**Named existing debt:** the scope-finding IDs required by the boundary-parity
entry at the top of this log never landed in the script. A read-tool grep
`SCOPE_|scope|absorbed` over `tools/research-gate.sh` found only a fixture table
header, no scope finding emitter. The documented province refusals are retained,
but gate enforcement is not claimed. A future single axis move can implement
the three refused-province findings and symmetric exit/finding fixtures.

## 2026-10-15 — round-1 local acceptance, corpus integration and receipt boundary

Measured committed gate: `31b46832e56a7f095092a4a6d62b74bfaf6933e8`.
Script SHA-256:
`08843552378071929c8b6abcd50be6613365691cfae4bf0d74fb03d86eb5b46e`.
The L1 ran the public CLI with inherited CHOUSA overrides unset, recording
exact argv/stdout/stderr/exits in `.ufo/evidence/round-1/acceptance.json`
and `acceptance.txt`:

- `--selftest` → `RESEARCH_GATE_SELFTEST: PASS (20 cases)`, exit 0.
  Normal info remains CLEAN; strict info DRIFT; malformed-after-info
  continues to later findings; secrecy and session refusal pass; setup cases
  retain exit 2 with no stdout verdict.
- A/B/C archive inputs each matched the committed expected SHA-256 before
  invocation; each exits 1 with exactly one full DRIFT verdict
  (`findings=6 drift=5 questions=0 sources=0 chains=0 claims=0 negatives=0
  rejections=0 approvals=0`). `VERDICT_BEARING_EXPORTS=3/3`; baseline 0/3
  is the retained prior measurement, not a failure rerun here.
- The inherited intake draft exits 0 with one CLEAN verdict. After adding
  opening metadata and append-only errata, its actual CLI recheck also exits
  0 with `findings=0 drift=0 questions=1 sources=8 chains=8 claims=9
  negatives=2 rejections=10 approvals=3`. Final input SHA-256:
  `33deaf93cec381509604db84e1b9c44d8ab3020998bf103eea7b720203fb62ec`;
  exact output is `.ufo/evidence/round-1/final-intake.json`.

`SKILL.md` now has one gate registry with the observed selftest and limited
structural guarantee, not the false “unchecked grep” cause or a field-ready
claim. `corpus/README.md` indexes the actual lesson and knowledge specimen;
`functions.glob` over `corpus/knowledge/*.md;corpus/lessons/*.md` returns those
two entries. Opening source/verified-at/recheck fields and append-only
integration errata preserve the inherited note/lesson rather than erasing
draft observations.

The L1 remeasured bounded source-form sweeps, saved in `source-sweeps.json`:
numbered-section regex `^([0-9]+[.]|[(][0-9]+[)])` matches A:74 and B:77;
HTTP(S)-locator regex has no matches across A/B/C plus README; visible
search-label regex matches A:42, B:42, C:42 and C:55. The old Markdown-table
command escaped alternation incorrectly; its executable correction is
appended to the intake. Numbered-section absence is not proof of every
answer's absence in prose. Visible labels cannot verify or contradict a
live search total; the stronger provenance assertion remains unknown.
No external source was fetched and no native transcript body was read.

**Citation-shift correction to the earlier LOG notice:** the current checklist
is `SKILL.md:54`, rules `:56-59`; the old `:44` / `:46-49` notice and
baseline script references are historical. The named superseded-claim grep
across touched skill/scorecard/log/index/intake/lesson/script found only
historical statements and explicit corrections, not a live unchecked-grep
diagnosis. No QUALITY criterion or non-author agree/disagree was invented.

**Verdicts:** operability improved, 0/3 → 3/3; depth, coverage, freshness,
calibration and adjacency unchanged (no broader measurements claimed).
Learning: expansion improved by the newly held intake form; quality and
discernment unchanged. No axis harmed, no scalar substitute, no promotion.
The old scope-finding requirement remains explicit debt, not a claimed
preserved executable boundary.

**Receipt prerequisite, not a local-code failure.** Launch metadata and the
exact Sighting mission entry provide run/session/mission IDs but no taskKey
or stored expected receipt bag. The configured canonical queue path
(`ufo-fsd-alpha/config/ufo.json:77`, `.ufo/pending-work.json`) is absent in
glob and directory read. The receipt API requires an authentic
`task_[24 lowercase hex]` key and dispatch-owned prompt/config bindings
(`scripts/ufo-mission-result.mjs:68-73,637-645,698-710,2707-2717`).
The applicable receipt cannot be truthfully minted by guessing those fields.
`.ufo/evidence/round-1/receipt-blocker.json` records the exact missing
authority and integrator unblock. No receipt or Sighting completion is
fabricated; receipt-backed completed rounds remain 0 pending acceptance.
The operator target remains at least 100, with no in-session second round.

The current launch overlay contains no role overrides (targeted grep of
`config/mission-nightcall.yml` found only maxConcurrency); global defaults
therefore still need operator-owned bindings before a new wave. This is
next-dispatch debt only; inherited round-1 routes are evidenced separately.
Reports/continuation remain lane-local. Native sessions, fleet ledgers and
shared reports are excluded from commits. Nothing is pushed.

### Round-1 publication — lane-local report and continuation

After work HEAD `cfb803a20ba6bf29ba977248bab41b939c7f2ea9` existed,
the lane wrote `.ufo/reports/round-1/chousa.md`, citing that HEAD and the
measured gate commit. Report SHA-256:
`ada72514590414e5daea12c0481c53927498eb0d37740f550969158f3e1aa2b6`.
`.ufo/continuations/round-1.json` binds the same work/report/evidence and
records all axes, learning trends, debt owners and concrete unblocks.
The report lands with this publication entry under the lane identity;
no shared report or ledger is updated.

Publication does not turn the receipt prerequisite into a pass: no genuine
receipt could be minted without the authentic queue identity/expected bag,
and no mint, shape-only validation, Sighting completion or successor launch
is invented. The integrator must resolve round-1 receipt acceptance first,
then release one fresh session for round 2. No second actual round was run
here; the 100-verified-round target remains unchanged.

## Round 2 — claim-vs-source verification (goal wave)

**Round 2 — goal-wave admission (2026-10-15).** Motivating evidence: the
round-1 registration (pre-register the local-only claim-verification fixture)
with routing now supplied by the operator's in-session direct dispatch.
Landed (evidence commit `c3df458`): gate `03a33244…` with `verify-claims`
(selftest 30 = +10; corpus-boundary canonicalization; verbatim spans;
line-aware misses; contradicted marker; exact counting); fixture
`corpus/fixtures/claims-r2.jsonl` (17 claims, provenance README);
`corpus/knowledge/claim-verification-r2.md`; lesson; four receipts.
**Receipt identity remains OPEN** — these receipts are lane-local evidence
logs, not queue taskKey/expected-receipt bags; proven receipt-backed
completed rounds remain 0 pending integrator binding (operator surface).

**Parent acceptance (2026-10-15T23:45Z).** selftest 30/30 exit 0;
`verify-claims corpus/fixtures/claims-r2.jsonl --root ..` →
`VERDICT_BEARING_CLAIMS=17/17`, `RESEARCH_GATE: CLEAN` exit 0 (13 supported /
2 contradicted / 2 unsupported); round-1 observable intact (VERDICT_BEARING_
EXPORTS=3/3). Acceptance note: the fixture sources are fleet-root-relative,
so the documented run requires `--root ..` — an acceptance run without it
refuses all sources correctly (boundary working as designed), and the parent
caught its own omission by reading the refusal lines.

**Verdicts.** ADMIT: coverage/depth/operability **improved**; freshness/
calibration/adjacency **unchanged**; none harmed. Named residuals: hardlink
canonicalization bypass; no claim-source size cap; r1 banner string. Round 3
registered: chain-hop resolution mode.

**Boundaries held.** Zero network (strace-confirmed); research corpus
read-only; no secrecy reads; seats committed nothing; parent integrated
under the chousa lane identity.

Round report: `.ufo/round-2/chousa-goalwave.md` (debts section carries the
receipt-identity note per the mission contract).

## Round 3 — verify-chain (goal wave)

**Round 3 — goal-wave admission (2026-10-15).** Motivating evidence: round 2's
named continuation (chain hops verified structurally only). Landed (evidence
commit `cc9fe8f`): gate `67daf85e…` with `verify-chain` (selftest 40 = +10;
source-id resolution through the Sources table; heading/quote/line anchors with
line reporting; exempt-but-counted unresolved hops; refused-unknown-ids);
fixture `corpus/fixtures/chain-r3.md` + broken control + README;
`corpus/knowledge/chain-resolution-r3.md`; receipts. Environmental: host /tmp
per-user quota exhausted by accumulated wave scratch mid-acceptance; parent
freed 727 MB of declared-ephemeral scratch; battery re-run clean.

**Parent acceptance (2026-10-16T00:15Z).** selftest 40/40 x2;
`verify-chain corpus/fixtures/chain-r3.md --root ..` -> `RESOLVED_HOPS=17/22`
CLEAN exit 0 (17 verified / 5 exempt); broken control DRIFT exit 1
(anchor-missing named); verify-claims 17/17 held byte-identical; r1 observable
3/3 intact.

**Verdicts.** ADMIT: coverage/depth/operability **improved**; freshness/
calibration/adjacency **unchanged**; none harmed. Named limit: substring
anchor semantics (truncated quotes resolve) — round 4 registered for
token-boundary hardening. Receipt identity remains OPEN (operator side).

**Boundaries held.** Zero network; corpus read-only; seats committed nothing;
parent integrated under the chousa lane identity.

Round report: `.ufo/round-3/chousa-goalwave.md`.

## Round 4 — anchor token boundaries (goal wave)

**Round 4 — goal-wave admission (2026-10-16).** Motivating evidence: round 3's
named limit (substring semantics; truncated quotes resolve). Landed (evidence
commit `a6f3118`): gate `6b83705b…` — one shared token-boundary matcher for
claims spans + chain quote anchors (char class in the header; `-`/`'`/
`_`/non-ASCII rules; fail-closed); selftest 44 = +4 with same-bytes-both-modes
cases; fixtures held (claims 17/17, chain 17/22 CLEAN; broken control DRIFT);
r1 observable 3/3. Wave: 32-seat flash call, 25/25. Environment: /tmp quota
held (quota-sentinel, ~700M headroom); seats cleaned scratch.

**Verdicts.** ADMIT: calibration/depth/operability **improved**; coverage/
freshness/adjacency **unchanged**; none harmed. Round 5 registered:
verify-sweeps — rejections + negative sweeps verdict-bearing (the last r1
structural axis). Receipt identity remains OPEN (operator side).

**Boundaries held.** Zero network; corpus read-only; seats committed nothing;
parent integrated under the chousa lane identity.

Round report: `.ufo/round-4/chousa-goalwave.md`.

## Round 5 — verify-sweeps (goal wave)

**Round 5 — goal-wave admission (2026-10-16).** Motivating evidence: the last
unmeasured r1 structural axis (rejections + sweeps structural only). Landed
(evidence commit `e7ab39a`): gate `55adb92d…` with `verify-sweeps` (selftest 54
= +10, 1-44 byte-identical) — rejections need reason + flip-condition; local
sweeps re-run for emptiness with planted hits named by path; exempt-but-counted
non-local class; fixture CLEAN (1/2 verified, 3/3 rejections), broken control
DRIFT naming both classes. claims 17/17 and chain 17/22 held. Wave: 32-seat
flash call, 27/27.

**Verdicts.** ADMIT: coverage/depth/operability **improved**; freshness/
calibration/adjacency **unchanged**; none harmed. Named limits (critic seats):
vacuous flip-conditions, narrow-sweep triviality — documented in the note.
Round 6 registered: `verify-all` composition (one record, one deep verdict
across all four modes) + the record's verification state lands in the lane's
manifest. Receipt identity remains OPEN (operator side).

**Boundaries held.** Zero network; corpus read-only; seats committed nothing;
parent integrated under the chousa lane identity.

Round report: `.ufo/round-5/chousa-goalwave.md`.

## Round 6 — verify-all composition (goal wave)

**Round 6 — goal-wave admission (2026-10-16).** Motivating evidence: no
composed verdict; no manifest. Landed (evidence commit `74c533d`): gate
`0c3d51ed…` with `verify-all` (selftest 64 = +10, 1-54 byte-identical) —
sections run as fresh solo invocations (tally-equal by construction),
composed CLEAN|DRIFT, absent!=drift, `--json` append-only manifest at
`corpus/evidence/verify-all-manifest.jsonl`. Full fixture CLEAN (4/4);
broken DRIFT with drift-sections=2; zero network (strace). Wave: 32-seat
flash call, 26/26.

**Verdicts.** ADMIT: operability/depth/freshness **improved**; coverage/
calibration/adjacency **unchanged**; none harmed. Named limit: absent!=drift
omission hole — r7 = binding integrity (cross-section references resolve,
fail-closed). Receipt identity remains OPEN (operator side).

**Boundaries held.** Zero network; corpus read-only; seats committed nothing;
parent integrated under the chousa lane identity.

Round report: `.ufo/round-6/chousa-goalwave.md`.

## Round 7 — verify-integrity (goal wave)

**Round 7 — goal-wave admission (2026-10-16).** Motivating evidence: round 6's
demonstrated dangling-reference hole. Landed (evidence commit `a1948c3`):
gate `3ba718bf…` with `verify-integrity` (selftest 74 = +10) — reference cells
across chain/claims/negatives/sweeps/rejections resolve against declared ids
fail-closed; exempt classes counted; fifth verify-all section. Fixture 16 refs
/ 15 resolved / 0 unresolved CLEAN; broken control DRIFT naming S9 + C9.
Wave: 32-seat flash call, 24/24.

**Verdicts.** ADMIT: coverage/depth/operability **improved**; freshness/
calibration/adjacency **unchanged**; none harmed. Round 8 registered: gate
behavioral baseline (--pin/--drift). Receipt identity remains OPEN (operator).

**Boundaries held.** Zero network; corpus read-only; seats committed nothing;
parent integrated under the chousa lane identity.

Round report: `.ufo/round-7/chousa-goalwave.md`.

## Round 8 — gate behavioral baseline (goal wave)

**Round 8 — goal-wave admission (2026-10-16).** Motivating evidence: no gate
baseline; regressions catchable only post-hoc. Landed (evidence commit
`LOGPEND8`): gate `46f5ddb3…` with `--pin`/`--drift` (selftest 85 = +11) —
canonical self-built fixture invocation, declared volatile contract
(ts/gate_sha256 shape-masked), GATE_DRIFT none/named-tokens/missing-malformed
under 0/1/2; catches measured: field mutant, silently-skipped mode
(-SECTION:sweeps), volatile-list rewrite. Lane baseline committed
(`corpus/evidence/gate-baseline-r8-20261016T033757Z.json`); parent drift
re-run `none` exit 0. Mori lineage declared. Wave: 32-seat flash call, 23/23.

**Verdicts.** ADMIT: freshness/operability/depth **improved**; coverage/
calibration/adjacency **unchanged**; none harmed. Round 9 registered: the
archived inputs through verify-all end-to-end + expanded fixtures. Receipt
identity remains OPEN (operator).

**Boundaries held.** Zero network; corpus read-only; seats committed nothing;
parent integrated under the chousa lane identity.

Round report: `.ufo/round-8/chousa-goalwave.md`.

## Round 9 — archives verified end-to-end (goal wave)

**Round 9 — goal-wave admission (2026-10-16).** Motivating evidence: no archive
had passed verify-all; claim coverage ~17. Landed (evidence commit
`LOGPEND9`): `corpus/fixtures/archives-r9/{A,B,C}-r9.md` + README + claims-r9
(10 new claims) — verify-all CLEAN on all three (zero findings: A 6/7 hops,
13 refs/0 unresolved; B 6/7, 14/0; C 7/8, 15/0; rejections 4/4, 3/3, 4/4;
sweeps 1/1 each). Honest premise correction: archives do not literally
cross-cite; hops authored intra-archive/conceptual. Gate unchanged (fixture-
led as designed). Wave: 32-seat flash call, 24/24.

**Verdicts.** ADMIT: coverage/depth/calibration **improved**; operability/
freshness/adjacency **unchanged**; none harmed. Round 10 registered: residual
hardening (archive-scale negative controls + exempt-hop audit + r2-r9 limit
disposition). Receipt identity remains OPEN (operator).

**Boundaries held.** Archives read-only; zero network; seats committed
nothing; parent integrated under the chousa lane identity.

Round report: `.ufo/round-9/chousa-goalwave.md`.

## Round 10 — negative controls + limit ledger (goal wave)

**Round 10 — goal-wave admission (2026-10-16).** Motivating evidence: no
archive-scale controls; no limit ledger. Landed (evidence commit
`LOGPEND10`): six controls under corpus/fixtures/archives-r9/controls/, each
DRIFTing verify-all with exactly one class-named finding (parent re-ran all
six); exempt audit clean; `corpus/knowledge/hardening-r10.md` = the r2-r9
limit-disposition ledger. Gate byte-unchanged. Wave: 32-seat flash call, 23/23.

**Verdicts.** ADMIT: calibration/coverage/depth **improved**; operability/
freshness/adjacency **unchanged**; none harmed. Named non-coverage:
RECORD_SCHEMA_INVALID fires with companions (documented). Round 11 registered:
the chousa capstone audit. Receipt identity remains OPEN (operator).

**Boundaries held.** Zero network; corpus read-only; no gate change; seats
committed nothing; parent integrated under the chousa lane identity.

Round report: `.ufo/round-10/chousa-goalwave.md`.

## Round 11 — capstone audit (goal wave)

**Round 11 — goal-wave admission (2026-10-16).** Motivating evidence: operator
goal — ten rounds each on mori and chousa; this closes chousa. Landed
(evidence commit `2e414ec`): `corpus/knowledge/audit-r11.md` — the
consolidated capstone audit: round 2's chain re-executed 15/15 supported at
frozen bytes; rounds 2-10 chains verified; the today's-bytes battery green
(selftest 85, drift none, fixtures/records/controls reproducing); the gate
byte-unchanged. Corrections folded: wave-seat-count claims unverifiable
without rosters (recorded; future rounds should log rosters); audit §5/§7
record-text defects carry [PARENT] markers; SHONEN 0/4 hold (no
self-attestation). chousa rounds 2-11: ten admitted rounds.

**Verdicts.** ADMIT-with-correction: calibration/depth **improved**; all else
**unchanged**; none harmed. Discernment trend: **improved**. Carried to the
operator: receipt identity (open since round 1), named-non-author SHONEN
verification, the promotion decision, and push (no lane remote exists for
either lane).

Round report: `.ufo/round-11/chousa-goalwave.md`.

## 2026-10-16 — protocol conformance: SCORECARD contract fields

**Operator rollout (2026-10-16 protocol amendment, fleet-root `84bade0`) — not a craft round.** Already present as recordable sections: axes (`## Axes`), planned (`## Planned`), retired (`## Retired`). Added by this rollout additively at file end: `## Capabilities` (repertoire-table scaffold, `— none yet —` row) and `## Saturation` (line + stagnation window N deferred to the lane's next round per `AXES.md` §The stagnation nudge).

No axis claim was made, no score moved, no verdict changed, no number invented; existing `SCORECARD.md` bytes unchanged (original 30128-byte prefix byte-identical, `sha256 2e802345c72f31197f83d400958816544d9cc0df7c365d2658687685d519c373`).

## 2026-10-19 — round-12 opening: environment unblock, before-receipts, claim registration

- **Battery unblock.** `--selftest` failed with `cat: write error: Disk quota exceeded` — the host per-user /tmp quota (same class as round 3's mid-acceptance exhaustion; the tmpfs itself had 3.1G free). Freed 6.4G of stale declared-ephemeral wave scratch under /tmp: 14 dirs (`d23` 2.2G, `P1` 484M, `p6` 443M, `c1` 348M, `m1h24` 294M, `f2` 268M, `m5-probe` 258M, `h24-H8` 251M, `f4` 230M, `f2f-scout` 211M, `h6` 200M, `h11` 177M, `s6` 147M, `s2-opencode` 147M), each verified zero open handles (`lsof +D`) and untouched >60 min before deletion. After: tmpfs 6.6G/16G used; `RESEARCH_GATE_SELFTEST: PASS (85 cases)` exit 0; `GATE_DRIFT: none` exit 0 vs `corpus/evidence/gate-baseline-r8-20261016T033757Z.json`; r1 counting command `VERDICT_BEARING_EXPORTS=3/3`.
- **Before-observables re-measured.** `grep -c SCOPE_ tools/research-gate.sh` → 0 (the r1 scope-teeth landing requirement is still open); `VERSION=research-gate-r1` at `tools/research-gate.sh:227` (r2-carried cosmetic residual); no size cap on claim/chain source reads; the r11 audit's one open finding reproduced — `corpus/fixtures/archives-r9/A-r9.md` row C3 cites `A-shokunin-tradition.md:76`, the quoted span verified at `:86` (line 76 carries the finishing/competence/independence distinction; line 86 carries the quoted sentence).
- **Claims declared** (full text: SCORECARD.md §Planned — round 12): coverage = scope-refusal teeth; operability = banner + source size-cap residuals; calibration = close the A-r9 C3 finding. Wave: 64 seats, one batched AgentSwarm call, opencode-go key 1 / deepseek-v4.1-flash (curriculum loop 1 round 1; opencode-go keys rotate between rounds).

### Round-12 dispatch deviation (2026-10-19, operator directive)

The first round-12 wave (opencode-go key 1, 64 seats) was interrupted before any seat reported. Operator directive: move to another opencode-go key and stay on it until it fails. Round 12's wave re-dispatches on **opencode-go-2 / deepseek-v4.1-flash**, and subsequent rounds stay on opencode-go-2 (deviation from the between-round key rotation recorded here and in the round-12 report; the directive supersedes the rotation).

### Round-12 dispatch deviation 2 (2026-10-19, operator directive)

The key-2 wave (opencode-go-2, 64 seats) was also interrupted before any seat reported. Operator directive: move to the next opencode-go key and stay on it. Round 12's wave now re-dispatches on **opencode-go-3 / deepseek-v4.1-flash**, and per the standing directive subsequent rounds stay on opencode-go-3 until it fails. Two aborted 64-seat dispatches (keys 1 and 2) produced zero seat reports; the roster in the round-12 report records this honestly.

### Round-12 dispatch deviation 3 (2026-10-19, measured failure)

The key-3 wave (opencode-go-3, 64 seats) failed instantly and completely: every seat returned `402 Upstream request failed: Insufficient account funds` (64/64, no seat started). Key 3 is out of funds — a measured provider failure, not an interruption. Per the standing operator directive (move to the next opencode-go key, stick with it), round 12 re-dispatches on **opencode-go-4 / deepseek-v4.1-flash**.

### Round-12 dispatch deviation 4 (2026-10-19, measured failure)

The key-4 wave (opencode-go-4, 64 seats) failed instantly and completely: every seat returned `402 Upstream request failed: Insufficient account funds` (64/64). Keys 3 and 4 are both out of funds. Per the standing directive the lane probes the remaining opencode-go keys with a single cheap liveness agent before spending another 64-seat wave; the wave re-dispatches on the first key that answers and stays there.

### Round-12 key selection (2026-10-19, measured)

Liveness probes (single agent, reply "alive"): opencode-go-5 → `402 Insufficient account funds`; **opencode-go-6 → alive**. Keys 3, 4, 5 are out of funds; keys 1 and 2 were abandoned on operator interruption before any seat reported (unmeasured). Per the standing operator directive, the lane sticks with **opencode-go-6 / deepseek-v4.1-flash** for round 12's wave and subsequent rounds until it fails.

## Round 12 — goal wave (2026-10-19)

**Admission.** Landed (evidence commit `5691bf531086dd435006cd9d6157df00933973a3`; wave: one 64-seat AgentSwarm call on opencode-go-6 / deepseek-v4.1-flash, 64/64 seat reports; key selection history in the deviation entries above):

- **Claim 1 (coverage) — scope-refusal teeth** (the r1 landing requirement): `scope_decl_screen` reads only `## Meta` rows keyed `domain`/`scope` (table + `key: value` forms; prose never scanned); refused-province declarations emit `SCOPE_BOUNTY_ABSORBED` / `SCOPE_MODEL_QUALITY_ABSORBED` / `SCOPE_ORCHESTRATION_ABSORBED` at warn (drift, exit 1), one finding per matched province per declaration row; 7 selftest cases (86–92); canary `verify B-r9` → 0 `SCOPE_` findings. Observable: emitting assignments `grep -c 'id=SCOPE_'` → 3 (amended from the bare `SCOPE_` count, conformance reviewer D3 — docs/fixture mentions would over-count).
- **Claim 2 (operability) — r2-carried residuals**: (a) `VERSION=v2` (banner contract; six sites; cases 93–94 incl. the `GATE_DRIFT: GATE` mutant arm); (b) 8 MiB source-read cap at the shared `claim_source_path` chokepoint (`CLAIM_SOURCE_READ_TOO_LARGE` / `CHAIN_SOURCE_READ_TOO_LARGE`, warn, refused before any read; cases 95–98 straddle 8388608/8388609, over-cap span on line 1 proving never-partially-read). Namespacing the pre-registered bare `SOURCE_READ_TOO_LARGE` to the mode idiom is a recorded amendment (seats 18/36). **Companion deviation (recorded)**: `count_nl` was quadratic (>60 s at 8 MiB, measured by the seat) — replaced with the linear `tr -dc '\n' | wc -c` (~3 ms); behavior-identical, without it the cap would be operability theatre.
- **Claim 3 (calibration) — closed as debt-closure, axis unchanged** (per the wave reviewers; claiming "improved" would double-count the r11 audit): A-r9.md C3 `:76` → `:86` (new sha `dfd2ae1a…` exactly as predicted); post-fix verify-all CLEAN; parent re-sweep 19/19; controls stay byte-copies of the pre-fix base (desync note); append-only errata to `audit-r11.md` and `hardening-r10.md` §6 (rows 9/10/56/70 dispositioned; 71 rows → 38·23·7·0·3, queue 26); pin cascade (archives-r9 README, claims-r9 README, archives-verified-r9, corpus/README, evidence README, SKILL.md, 5 knowledge-note dispositions). The class (pointer-line vs span-line) stays a named non-coverage.
- **Forced + recorded re-pin**: `--drift` vs the r8 baseline reads `GATE_DRIFT: GATE record_sha256` exit 1 (VERSION v2 + the pin fixture's clean domain row, both unmasked contract words); one re-pin at final bytes: `corpus/evidence/gate-baseline-r12-20261019T115519Z.json` (`GATE_PIN: ok`, immediate `GATE_DRIFT: none`); reason in `corpus/knowledge/gate-baseline-r12.md`.
- **Battery** (receipts `corpus/evidence/scope-r12-20261019T115519Z-*.log`): selftest `PASS (98 cases)`, cases 1–85 `cmp` byte-identical vs the r8 receipt; r1 `3/3`; fixture battery (A/B/C-r9, r6 trio, r7 pair, claims-r2, chain-r3, sweeps-r5, six controls) byte-identical vs the pre-round gate modulo masked banner/ts; zero network; gate `46f5ddb3…` → `91a01695…`.

**Verdicts** (full table: SCORECARD.md §Round 12 verdict): coverage/operability/freshness(narrow)/depth **improved**; calibration **unchanged** (debt closure); adjacency **unchanged**; none harmed. **ADMIT.** Learning trends: expansion/quality improved; discernment unchanged. Capabilities table gained three rows (screening, cap, banner contract).

**Corrections to prior entries (append-only, per the r11 audit D3):** the round-8/9/10 goal-wave entries above carry the placeholders `LOGPEND8`/`LOGPEND9`/`LOGPEND10`; the evidence commits they name at those rounds' admission were `27b55c3` (r8), `ebd04d2` (r9), `5f99fa3` (r10) as recorded in each round's SCORECARD verdict block — the placeholders were never resolved to hashes in this file; resolved here.

**Boundaries held.** Zero network; research corpus read-only; seats committed nothing (read-only wave); parent integrated under the lane identity; no pushes (goal boundary; the origin remote exists and master is ahead 7 — push is an operator/integrator call, noted for the record). Receipt identity remains OPEN (re-filed to the fleet L0 queue this round — see the round-12 report). Round 13 registered in SCORECARD §Planned.

## 2026-10-19 — round-13 opening: claims, before-receipts, dispatch

- **Before-observables** (at HEAD 91aebd3, after the round-12 battery): selftest `RESEARCH_GATE_SELFTEST: PASS (98 cases)`; drift vs the r12 baseline `GATE_DRIFT: none`; r1 counting command `VERDICT_BEARING_EXPORTS=3/3`; inode/hardlink logic in the gate: `grep -c samefile tools/research-gate.sh` → 0; multi-linked files across corpus/tools/research: 0 (so the fix cannot perturb any existing fixture by construction — to be re-measured by the wave).
- **Claims** (pre-registered SCORECARD.md §Planned — round 13; curriculum loop 1 round 2): coverage = close the last r2 residual — in-root hardlink canonicalization (ledger row 8): a claims/chain source cited through an in-root hardlink alias of an out-of-corpus file is read today; after: refused (named finding) or canonicalized to the inode-true path with the boundary re-checked, plus symmetric selftest fixtures and the hold battery green. depth = the alias-semantics knowledge note (what readlink -f does and does not prove about inodes; refusal semantics; named limits) + SKILL.md registry sweep. The stagnation nudge stays dormant (operability 3 is the only score; claim 1 lands on coverage, claim 2 on depth — the round works the registered row-8 class).
- **Wave**: one batched AgentSwarm call, 64 seats, opencode-go-6 / deepseek-v4.1-flash (standing directive: stick with key 6). Seat roster lands in the round-13 report.

## Round 13 — goal wave (2026-10-19)

**Admission.** Landed (evidence commit this entry; wave: one 64-seat AgentSwarm call on opencode-go-6 / deepseek-v4.1-flash, 64/64 seat reports):

- **Claim 1 (coverage) — hardlink-alias boundary** (the last r2 residual, ledger row 8): the wave's enumeration designs were BLOCKed as unsound (order dependence, nested/bind-mounted roots); the landing is a one-probe `stat -c '%s %h'` check at the shared `claim_source_path` chokepoint (one probe now serves the r12 size cap and the r13 alias check): `nlink != 1` → refused unread, `CLAIM_SOURCE_MULTILINKED` / `CHAIN_SOURCE_MULTILINKED`, crit, per-item `observed=refused`. Claim re-scoped per the reviewers: the HARDLINK class closes; bind mounts (nlink=1, stat-invisible), TOCTOU, unmeasurable-stat fallback, and legit in-root multi-link families refusing are named limits (`corpus/knowledge/hardlink-alias-r13.md`), case 101 pins the family trade. The bypass is proven live: `corpus/evidence/alias-r13-20261019T123621Z-bypass-before.log` reads `observed=supported` CLEAN at the pre-round gate; `-after.log` refuses crit at the landed gate.
- **Claim 2 (depth)**: `corpus/knowledge/hardlink-alias-r13.md` + lesson `2026-10-19-hardlink-alias-boundary.md` + SKILL.md paragraph/table sweep.
- **Battery**: selftest `PASS (102 cases)` (98+4), cases 1–98 `cmp` byte-identical; r1 `3/3`; drift `none` vs the r12 baseline (no re-pin — canonical invocation unchanged); masked battery vs the pre-round gate with LANE_ROOT intact (temp copy inside `tools/`; the /tmp-copy form breaks lane-root-relative pointer resolution — sweeps-r5 S4 — a recorded method artifact) ALL IDENTICAL; zero network. Gate `91a01695…` → `6b17e50c…`.
- **Errata/records**: hardening-r10 round-13 addendum (row 8 closed(r13, hardlink class); carried limits inside the closure; 71 rows → **by-design 38 · carried 22 · closed 8 · finding 0 · operator 3**, queue 26 → 25); corpus/README carried-residuals line + knowledge-index row; evidence/README receipt rows; SKILL.md registry sweep.
- **Verdicts** (SCORECARD §Round 13 verdict): coverage/operability/depth/freshness(narrow) **improved**; calibration/adjacency **unchanged**; none harmed. **ADMIT.** Capabilities +1 (hardlink-alias refusal). Learning: expansion/quality improved, discernment unchanged. Round 14 registered (curriculum round 3: zai glm-5.3-flash; fallback key 6 if zai is out; claim from the named-limit queue, pre-registered at opening).

**Boundaries held.** Zero network; research corpus read-only; seats read-only; lane-identity pathspec-limited commits; no pushes (8 → 11 local commits; push remains operator/integrator-owned). Receipt identity still OPEN (L0 row filed at round 12, unanswered — routed around).

### Round-14 provider deviation (2026-10-19, operator directive)

Operator directive: **use the token-plan lanes for the deepseek-v4.1-flash swarms** instead of opencode-go. Standing assignment from round 14: deepseek-v4.1-flash waves run on **alibaba-token-plan** (keys -2/-3 are the overflow ladder; stick with the first working key per the standing doctrine, probing liveness before each wave). Round 13 and earlier ran on opencode-go-6 (recorded history, unchanged).

## 2026-10-19 — round-14 opening: claims, before-receipts, dispatch

- **Claims** (curriculum loop 1 round 3): coverage/operability = the mount-alias (bind) boundary — refuse claim/chain sources whose `st_dev` differs from the resolving root's device (`CLAIM_SOURCE_CROSS_DEVICE` / `CHAIN_SOURCE_CROSS_DEVICE`), closing the named residual the r13 reviewers carved out (same-device binds remain a named limit — stat cannot see them); the wave validates the unprivileged fixture strategy (user-namespace bind if available on this host; otherwise an absolute-path cross-device fixture) and BLOCKs to a documented named-limit if no sound check exists. depth = the mount/alias note (device semantics, why %d, the same-device-bind honesty) + registry sweep. Before: `grep -c CROSS_DEVICE tools/research-gate.sh` → 0; device logic absent.
- **Before-receipts**: selftest `PASS (102 cases)`; drift `none` vs the r12 baseline; r1 `3/3`; st_dev probes absent (to be re-measured by the wave).
- **Wave**: one batched AgentSwarm call, 64 seats, **alibaba-token-plan / deepseek-v4.1-flash** (operator directive above). Seat roster lands in the round-14 report.

## Round 14 — goal wave (2026-10-19)

**Admission.** Landed (evidence commit this entry; wave: one 64-seat AgentSwarm call on **alibaba-token-plan / deepseek-v4.1-flash** per the operator's token-plan directive, 63/64 reports — seat 54 failed on a provider content-filter 400; deficit recorded, not backfilled):

- **Claim 1 (coverage/operability) — mount-alias boundary**: the chokepoint now tracks the RESOLVING root (longest-prefix rule — the wave proved a ROOT-only compare false-refuses the live sweeps-r5 S4 lane-fallback case and the selftest itself) and one `stat -c '%s %h %d'` probe serves nlink (r13) → size (r12) → device (r14); `CLAIM_SOURCE_CROSS_DEVICE` / `CHAIN_SOURCE_CROSS_DEVICE` (crit) refuse cross-device sources unread. The mount-free "absolute-path" fixture was BLOCKed as unsound (two seats, measured); the fixture is a user+mount-namespace tmpfs forge (unprivileged on this host; a repo bind inside the ns is refused, rc=2). Live before/after receipts `corpus/evidence/mount-r14-20261019T125621Z-bypass-{before,after}.log`.
- **Claim 2 (depth)**: `corpus/knowledge/mount-alias-r14.md` + SKILL paragraph/table sweep; named limits: same-device binds (stat-invisible), overlay roots (file-vs-root-dir comparison breaks), TOCTOU, unmeasurable-stat fallback, legit cross-device subtrees refusing; **discovered and queued: the `--root /` boundary dead-arm** (`case "$canon" in "$root_r"/*` → `//*`, every source refuses; fix `"${root_r%/}"/*` named, not landed — outside the r14 claim).
- **Battery**: selftest `PASS (106 cases, 0 skipped)`, cases 1–102 `cmp` byte-identical; r1 `3/3`; drift `none` vs the r12 baseline (no re-pin); masked battery vs the pre-round gate (LANE_ROOT intact, r13 method) ALL IDENTICAL; zero network. Gate `6b17e50c…` → `d8bbd0bf…`.
- **Errata/records**: hardening-r10 round-14 addendum (E3: the E2-carried bind item closes; 71 rows → **by-design 38 · carried 21 · closed 9 · finding 0 · operator 3**; queue 25 → 25, the `--root /` item in, bind item out); corpus/README + evidence/README + SKILL sweeps.
- **Verdicts** (SCORECARD §Round 14): coverage/operability/depth/calibration(narrow) **improved**; freshness/adjacency **unchanged**; none harmed. **ADMIT.** Capabilities +1. Round 15 registered (curriculum round 4: zai glm-5.3-flash, 32–64 seats; fallback ladder token-plan → devin → opencode-go-6).

**Boundaries held.** Zero network; research corpus read-only; seats read-only; lane-identity pathspec-limited commits; no pushes. Receipt identity still OPEN (L0 row from round 12 unanswered — routed around).

## 2026-10-19 — round-15 opening: claims, before-receipts, dispatch

- **Claims** (curriculum loop 1 round 4): coverage/operability = fix the `--root /` boundary dead-arm discovered by the round-14 wave: `case "$canon" in "$root_r"/*` renders as `//*` when `root_r=/`, matching nothing, so every source refuses OUT_OF_CORPUS (live demo this opening: a claim citing `/etc/hostname` with `--root /` refuses `CLAIM_SOURCE_OUT_OF_CORPUS` crit; `/etc/hostname` is dev 31 = root dev, nlink 1, 17 B — a legitimate read blocked purely by the pattern bug). After: `"${root_r%/}"`-normalized prefix matching (src_root still stat'ed as `/`), symmetric treatment of the lane-root pattern, selftest case(s) incl. the absolute-path reads + the before-behavior pinned; sweeps' separate resolver audited for the same class. depth = the root-normalization note (glob mechanics of `//*`, why only absolute paths bite, the normalized-match contract) + registry sweep.
- **Before-receipts**: selftest `PASS (106 cases, 0 skipped)`; drift `none` vs the r12 baseline; r1 `3/3`; the dead-arm demo above (recorded in the round-15 receipts).
- **Wave**: one batched AgentSwarm call, 48 seats (curriculum 32–64), **zai glm-5.3-flash** (liveness-probed alive this opening; fallback ladder per the standing record: devin deepseek → token-plan deepseek → opencode-go-6). Seat roster lands in the round-15 report.

## Round 15 — goal wave (2026-10-19)

**Admission.** Landed (evidence commit this entry; wave: one 48-seat AgentSwarm call on **zai glm-5.3-flash** per the round-15 opening, 48/48 seat reports):

- **Pre-registration correction (measured, keeps the wave off a green-but-unfixed landing):** the opening's one-token fix `"${root_r%/}"/*` is a **no-op at `root_r=/`** in `case` patterns on bash 5.3.15 — a quoted operator expansion whose result is empty leaves the adjacent glob non-special: `case /etc/hostname in "${root_r%/}"/*)` → no match (reproduced ×3; the two-step form `rr="${root_r%/}"; case … in "$rr"/*)` matches). At normal roots the inline form matches, so all 106 existing selftest cases would stay green with the dead-arm unrepaired — the trap is invisible to the suite. Landed shape: the `in_root()` helper (`tools/research-gate.sh` ~:612) materializes `r=${2%/}` then tests `[[ $c == "$r" || $c == "$r"/* ]]` — version-independent by construction, and the `== "$r"` arm keeps the root-directory edge hitting the boundary then failing `-f` → `MISSING`.
- **Claim 1 (coverage/operability) — the `--root /` boundary dead-arm**: absolute in-`/` sources read after the fix; before-behavior pinned. Three same-class sites converted: `claim_source_path` (:1044-1075), `ptr_resolves_meta` (:546-551 — the third site, found by this round's registry sweep, not named in the opening), `sweep_path_guarded` (:1750-1756). `src_root` keeps the un-normalized root so the r14 device probe still stats the declared root. Live before/after receipts `corpus/evidence/root-r15-20261019T152000Z-demo.log` (a `/etc/hostname` claim: dev 31 = root dev, nlink 1, 9 B — legitimate read blocked purely by the pattern → `CLEAN` `1/1`). Selftest cases 107–110 (ghost-missing, `/etc/hostname` read, tmpfs cross-device, sweeps absolute glob); cases 1–106 `cmp` byte-identical. The `CHOUSA_ROOT=` override rides a new harness channel — six runners gained a `^CHOUSA_[A-Z_]+=` env-override classifier; `tcase`'s override placement corrected to last-wins.
- **Claim 2 (depth)**: `corpus/knowledge/root-slash-boundary-r15.md` — the `//*` glob mechanics (measured), the four-outcome pre-fix table (absolute-existing → OUT_OF_CORPUS; root-relative-existing → same; absolute-absent → OUT_OF_CORPUS mislabeled; relative-absent → MISSING via the `//`-canon artifact), the `in_root` contract, the 3-site registry, the inline-strip quirk, named limits.
- **Battery**: selftest `PASS (110 cases, 0 skipped)`; r1 `3/3`; drift `none` vs the r12 baseline (no re-pin); masked battery vs the pre-round gate (LANE_ROOT intact, r13 method) ALL IDENTICAL; zero network. Gate `d8bbd0bf…` → `dd0951d7…`.
- **Errata/records**: hardening-r10 round-15 addendum (E4: the E3-queued `--root /` item closes; 71 rows → **by-design 38 · carried 21 · closed 10 · finding 0 · operator 3**; queue 25 → 24; the dead-arm closure is a queue-item closure, not a row closure — the E3 phantom-count explained); **append-only LOG correction: the round-14 admission entry (`LOG.md:596`) cites bypass receipts `…125621Z-…`; the on-disk files are `mount-r14-20261019T132025Z-bypass-{before,after}.log` (typo already corrected at `hardening-r10.md:516-518`; LOG itself was never)**; corpus/README + evidence/README + SKILL sweeps.
- **Verdicts** (SCORECARD §Round 15): coverage/operability/depth/calibration(narrow) **improved**; freshness/adjacency **unchanged**; none harmed. **ADMIT.** Capabilities +1. Round 16 registered (curriculum round 5: gpt-6-luna-max, 64 seats — verification wave re-auditing loop-1 rounds 1–4).

**Boundaries held.** Zero network; research corpus read-only; seats read-only; lane-identity pathspec-limited commits; no pushes. Receipt identity still OPEN (L0 row from round 12 unanswered — routed around). Round report: `.ufo/reports/round-15/chousa.md` (seat roster lands there, per the r11 correction).

## 2026-10-19 — round-16 opening: claims, before-receipts, dispatch

- **Claims** (curriculum loop 1 round 5 — verification wave): coverage/calibration = adversarially re-audit the current loop's rounds 1–4 (lane rounds 12–15) for correctness defects and missed coverage; every finding lands as a dispositioned item (fix, absorb, or named debt). The audit surface: the boundary stack (scope refusal cases 86–92, size cap 95–98, hardlink 99–102, cross-device 103–106, root-slash 107–110), the gate's refusal/finding registry, the knowledge notes' measured claims, and the selftest harness itself. operability = the audit's own receipts.
- **Before-receipts**: selftest `PASS (110 cases, 0 skipped)`; drift `none` vs the r12 baseline; r1 `3/3`; gate `dd0951d7…`; HEAD `58cf0b9`.
- **Wave**: one batched AgentSwarm call, 64 seats (curriculum 64), **openai-codex gpt-6-luna-max** (liveness-probed alive this opening; fallback ladder per the standing record: devin → token-plan → opencode-go-6). Seat roster lands in the round-16 report.

## Round 16 — goal wave (2026-10-19)

**Admission.** Landed (evidence commit this entry; wave: one 64-seat AgentSwarm call on **openai-codex gpt-6-luna-max** per the round-16 opening, 64/64 seat reports — zero deficit):

- **Verification verdict**: the boundary stack (rounds 12–15) is sound — no out-of-corpus read found, no refusal class broken. The wave's findings are ~2 fixes, ~15 absorbs, ~12 named debts.
- **Fix 1 — `--root //` still refused** (seats 09, 10, 52): `in_root` stripped only one `/`, leaving `/` which still rendered `//*`. The loop now strips all trailing slashes; case 111 pins it. `cd // && pwd -P` → `//` measured.
- **Fix 2 — r15 battery receipt wrong fixture paths** (seats 32, 62): A/B/C-r9 under `corpus/fixtures/` not `archives-r9/`; `--root .` vs `--root ..`. Re-run with correct paths, masked diff IDENTICAL; receipt replaced.
- **Absorbs** (~15): `wc -c` fallback reads to measure (not to search) — named limit corrected in mount-alias-r14; scope-refusal coverage overstatement corrected; full-r6 README sweeps-absent corrected; mount-alias "queued" item closed; stale hardlink status in older notes absorbed; hardening-r10 count phantom explained; `ptr_resolves_meta` coverage gap named; empty-claims vacuous-pass documented; FAIL-summary skip asymmetry absorbed; chain kind-blindness already carried; r15 roster internally complete (wave file in session log); conformance exploratory-claim rule scoped; `--` delimiter edge absorbed; URI-like citation classification named; manifest outside-root documented.
- **Named debts** (~12, round-17 queue): scope-screen fenced-heading shadow, `LLM benchmarks` phrase gap, sweeps symlink-escape guard, `--drift` truncated-baseline ambiguity, `--json` delimiter edge, manifest timestamp mask breadth, secret-scan source coverage, bash-3 portability, 8 unasserted finding IDs, TOCTOU readability, relative-root missing-path severity, `--` delimiter handling.
- **Battery**: selftest `PASS (111 cases, 0 skipped)`, cases 1–110 `cmp` byte-identical vs the r15 receipt; r1 `3/3`; drift `none` vs the r12 baseline (no re-pin); corrected masked battery vs the pre-round gate ALL IDENTICAL; zero network. Gate `dd0951d7…` → `<FILL>`.
- **Errata/records**: `corpus/knowledge/verification-r16.md` (the full disposition table); `corpus/knowledge/mount-alias-r14.md` (unmeasurable-stat corrected, queued item closed); `corpus/knowledge/scope-refusal-r12.md` (coverage overstatement corrected); `corpus/fixtures/full-r6.README.md` (sweeps-absent corrected); `corpus/README.md` (verification-r16 row); `SKILL.md` (110→111, r15 paragraph updated for `//`); SCORECARD verdict + round-17 registration.
- **Verdicts** (SCORECARD §Round 16): operability/depth/calibration **improved**; coverage/freshness/adjacency **unchanged**; none harmed. **ADMIT.** Capabilities +0 (verification round — no new capability, the existing stack verified). Round 17 registered (curriculum round 6: xai-oauth grok-4.7-fast, 32–64 seats).

**Boundaries held.** Zero network; research corpus read-only; seats read-only; lane-identity pathspec-limited commits; no pushes. Receipt identity still OPEN (L0 row from round 12 unanswered — routed around). Round report: `.ufo/reports/round-16/chousa.md` (seat roster lands there).

## 2026-10-19 — round-17 opening: claims, before-receipts, dispatch

- **Claims** (curriculum loop 1 round 6): coverage/operability = fix the scope-screen fenced-heading shadow (round-16 named debt): `load_sections` resets on every `## ` line without recognizing fenced code blocks, so a `## Meta` inside a fence shadows the real declaration — the scope screen then checks the wrong body. Fix: recognize fenced blocks and skip headings inside them. depth = the fenced-heading mechanics note + the `LLM benchmarks` phrase gap disposition.
- **Before-receipts**: selftest `PASS (111 cases, 0 skipped)`; drift `none` vs the r12 baseline; r1 `3/3`; gate `2b64a1c8…`; HEAD `0a2d7ce`.
- **Wave**: one batched AgentSwarm call, 32–64 seats (curriculum 32–64), **xai-oauth grok-4.7-fast** (liveness-probed alive this opening; fallback ladder per the standing record: devin → token-plan → opencode-go-6). Seat roster lands in the round-17 report.

## Round 17 — goal wave (2026-10-19)

**Admission.** Landed (evidence commit this entry; wave: one 32-seat AgentSwarm call on **opencode-go / deepseek-v4.1-flash** — xai-oauth grok-4.7-fast failed on 403 quota for all 48 seats, then zai glm-5.3-flash was interrupted at 14/48 before the re-dispatch landed on opencode-go; 27/32 seat reports — 5 failed on provider 400 `reasoning_content` errors; deficit recorded, not backfilled):

- **Claim 1 (coverage/operability) — the fenced-heading shadow**: `load_sections` splits on every `## ` line with no fence state — a `## Meta` inside a fenced code block resets the real Meta body, so the scope screen checks the wrong declaration. A record with `domain: bounty program scope` in its real Meta plus a fenced `## Meta` declaring `deep-research method` passed CLEAN (live demo: pre-round gate → CLEAN; landed → `SCOPE_BOUNTY_ABSORBED` warn + DRIFT; receipt `fence-r17-20261019T171200Z-demo.log`). The fix pairs fences in two passes — same char must close, closing length >= opening, 0–3 literal-space indent; an unclosed opener IS a fence (fail closed — everything after it is literal). The naive `^``` ` toggle fixes only the simple shadow (the wave's seat-30 verifier measured it still opens on nested 4-backtick, indented closers, and unclosed fences — all five variants now refuse).
- **Claim 2 (depth)**: `corpus/knowledge/fenced-heading-r17.md` — the shadow mechanics, the naive-vs-two-pass measured shape matrix, the call-site audit (load_sections serves every mode; no caller depends on fenced headings), and named limits (fenced data rows inside a real section are still scanned; the gate is not a Markdown renderer).
- **Battery**: selftest `PASS (116 cases, 0 skipped)`, cases 1–109 `cmp` byte-identical vs the r15 receipt (r16 inserted case 110 — the cmp boundary is 109, not 111); r1 `3/3`; drift `none` vs the r12 baseline (no re-pin); masked battery vs the pre-round gate (LANE_ROOT intact, r13 method) ALL IDENTICAL; zero network. Gate `2b64a1c8…` → `c2915f24…`.
- **Errata/records**: the `LLM benchmarks` phrase gap stays named debt (not silently absorbed); the provider deviation is recorded (xai 403 → zai interrupted → opencode-go); `corpus/README` + `evidence/README` + SKILL sweeps; SCORECARD verdict + round-18 registration.
- **Verdicts** (SCORECARD §Round 17): coverage/operability/depth/calibration(narrow) **improved**; freshness/adjacency **unchanged**; none harmed. **ADMIT.** Capabilities +1. Round 18 registered (curriculum round 7: zai glm-5.3-flash, 16–32 seats; fallback ladder per the standing record).

**Boundaries held.** Zero network; research corpus read-only; seats read-only; lane-identity pathspec-limited commits; no pushes. Receipt identity still OPEN (L0 row from round 12 unanswered — routed around). Round report: `.ufo/reports/round-17/chousa.md` (seat roster lands there).

## 2026-10-19 — round-18 opening: claims, before-receipts, dispatch

- **Claims** (curriculum loop 1 round 7): coverage = close the `LLM benchmarks` phrase gap (round-16 named debt): `SCOPE_KENGAKU` has `model benchmark(s)` but not `llm benchmark(s)`/`llm scoring`/`ai benchmark(s)` — a record declaring `domain: LLM benchmarks` passes CLEAN despite the model-quality boundary. The fix adds the missing phrases to `SCOPE_KENGAKU`; the wave audits the other two province lists for the same class. operability = the phrase-gap selftest cases.
- **Before-receipts**: selftest `PASS (116 cases, 0 skipped)`; drift `none` vs the r12 baseline; r1 `3/3`; gate `c2915f24…`; HEAD `02b70c0`.
- **Wave**: one batched AgentSwarm call, 16 seats (curriculum 16–32), **openai-codex gpt-6-luna-max** — zai glm-5.3-flash quota exhausted; operator directed codex luna max for all zai-assigned rounds until tomorrow. Deepseek waves use opencode-go key 6. Seat roster lands in the round-18 report.

## Round 18 — goal wave (2026-10-19)

**Admission.** Landed (evidence commit this entry; wave: one 16-seat AgentSwarm call on **openai-codex gpt-6-luna-max** per the round-18 opening — zai glm-5.3-flash quota exhausted, operator directed codex luna max for all zai-assigned rounds until tomorrow; 16/16 seat reports — zero deficit):

- **Claim 1 (coverage/operability) — the SCOPE_KENGAKU phrase gap**: `SCOPE_KENGAKU` covered `model benchmark(s)` and `model scoring` but not `llm benchmark(s)`/`llm scoring` — a record declaring `domain: LLM benchmarks` passed CLEAN despite the model-quality boundary (live demo: pre-round gate → CLEAN; landed → `SCOPE_MODEL_QUALITY_ABSORBED` warn + DRIFT; receipt `scope-r18-20261019T173000Z-demo.log`). `scope_hit` matches literal phrases after `scope_norm` lowercases and folds punctuation; it never stems, so `llm benchmarks` needs its own entry — `model benchmarks` does not cover it. The conservative 3-phrase set landed (`llm benchmark|llm benchmarks|llm scoring`); `ai benchmark(s)` stays named debt — the wave's adversary seats measured it too broad for AI-methodology research. Cases 117–119 pin the new phrases + the prose-only control.
- **Claim 2 (depth)**: `corpus/knowledge/scope-phrase-gap-r18.md` — the gap mechanics, the conservative-vs-broad fix boundary, the audit's other inflection findings dispositioned (`bug bounties`, `dispatch mechanisms`, `llm evaluations`, `llmbenchmark` camel-case, `language model benchmark(s)` all named debt).
- **Battery**: selftest `PASS (119 cases, 0 skipped)`, cases 1–116 `cmp` byte-identical vs the r17 receipt; r1 `3/3`; drift `none` vs the r12 baseline (no re-pin); masked battery vs the pre-round gate (LANE_ROOT intact, r13 method) ALL IDENTICAL; zero network. Gate `c2915f24…` → `6e694881…`.
- **Errata/records**: the provider deviation is recorded (zai exhausted → luna); `corpus/README` + `evidence/README` + SKILL sweeps; SCORECARD verdict + round-19 registration.
- **Verdicts** (SCORECARD §Round 18): coverage/operability/depth/calibration(narrow) **improved**; freshness/adjacency **unchanged**; none harmed. **ADMIT.** Capabilities +1. Round 19 registered (curriculum round 8: openai-codex gpt-6-luna-max, 16–32 seats — zai exhaustion directive).

**Boundaries held.** Zero network; research corpus read-only; seats read-only; lane-identity pathspec-limited commits; no pushes. Receipt identity still OPEN (L0 row from round 12 unanswered — routed around). Round report: `.ufo/reports/round-18/chousa.md` (seat roster lands there).

## 2026-10-19 — round-19 opening: claims, before-receipts, dispatch

- **Claims** (curriculum loop 1 round 8): coverage/operability = the sweeps symlink-escape guard (round-16 named debt): `sweep_path_guarded` canonicalizes the glob's BASE directory but a wildcard inside a symlinked dir can match files outside the allowed roots — the guard sees the symlink's target (inside root) while the glob expands to the target's children (which may be outside). The fix must canonicalize each glob MATCH, not just the base. depth = the symlink-escape mechanics note + the remaining named-debt dispositions.
- **Before-receipts**: selftest `PASS (119 cases, 0 skipped)`; drift `none` vs the r12 baseline; r1 `3/3`; gate `6e694881…`; HEAD `71b0b5f`.
- **Wave**: one batched AgentSwarm call, 16 seats (curriculum 16–32), **openai-codex gpt-6-luna-max** (zai exhaustion directive). Seat roster lands in the round-19 report.

## Round 19 — goal wave (2026-10-19)

**Admission.** Landed (evidence commit this entry; wave: one 16-seat AgentSwarm call on **openai-codex gpt-6-luna-max** per the zai-exhaustion directive, 16/16 seat reports — zero deficit):

- **Claim 1 (coverage/operability) — the sweeps symlink escape**: `sweep_path_guarded` canonicalizes the glob's literal BASE but not each match — a wildcard inside an in-root dir can match a symlink whose target is outside both roots (live demo: pre-round gate → `SWEEP_CLAIM_FALSE` hit on an outside symlink; landed → `SWEEP_LOCATION_OUT_OF_CORPUS` crit + refused; receipt `symlink-r19-20261019T174500Z-demo.log`). Two escape shapes closed: leaf symlink (`dir/*.md`) and directory symlink (`dir/*/*.md`). The fix canonicalizes every expanded match against `in_root` for both roots; any escape refuses the whole sweep.
- **Claim 2 (depth)**: `corpus/knowledge/sweep-symlink-r19.md` — the escape mechanics, the fix contract, the named limits (post-expansion check — bash already traversed the symlinked dir during glob expansion; TOCTOU; `--root /` vacuous by declaration).
- **Battery**: selftest `PASS (122 cases, 0 skipped)`, cases 1–119 `cmp` byte-identical vs the r18 receipt; r1 `3/3`; drift `none` vs the r12 baseline (no re-pin); masked battery vs the pre-round gate (LANE_ROOT intact, r13 method) ALL IDENTICAL; zero network. Gate `6e694881…` → `9f163807…`.
- **Errata/records**: `corpus/README` + `evidence/README` + SKILL sweeps; SCORECARD verdict + round-20 registration.
- **Verdicts** (SCORECARD §Round 19): coverage/operability/depth/calibration(narrow) **improved**; freshness/adjacency **unchanged**; none harmed. **ADMIT.** Capabilities +1. Round 20 registered (curriculum round 9: openai-codex gpt-6-luna-max, 64–128 seats — zai exhaustion directive).

**Boundaries held.** Zero network; research corpus read-only; seats read-only; lane-identity pathspec-limited commits; no pushes. Receipt identity still OPEN (L0 row from round 12 unanswered — routed around). Round report: `.ufo/reports/round-19/chousa.md` (seat roster lands there).

## 2026-10-19 — round-20 opening: claims, before-receipts, dispatch

- **Claims** (curriculum loop 1 round 9 — the second verification-scale wave): coverage/calibration = adversarially re-audit the expanded boundary stack (rounds 15–19's fixes: in_root, fence-aware load_sections, SCOPE_KENGAKU phrase expansion, per-match sweeps canonicalization) for correctness defects, missed coverage, and interactions the earlier rounds didn't test. The audit surface: the 122 selftest cases' assertion quality, the named limits' honesty, the dispositioned findings' actual status, and the interaction matrix between the four boundary mechanisms. operability = the audit's own receipts + any fixes that land.
- **Before-receipts**: selftest `PASS (122 cases, 0 skipped)`; drift `none` vs the r12 baseline; r1 `3/3`; gate `9f163807…`; HEAD `2bb556b`.
- **Wave**: one batched AgentSwarm call, 64 seats (curriculum 64–128), **openai-codex gpt-6-luna-max** (zai exhaustion directive). Seat roster lands in the round-20 report.
