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

