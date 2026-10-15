# chousa — round 2: claim-vs-source verification (coverage move)

<!-- SCRIBE DRAFT for parent integration. Measured values are from the frozen
     gate revision sha256 03a3324455852ea0025115cb0e3ba9c8cdea10da5edc051c4738854a27c14be0
     and the receipts under corpus/evidence/claims-r2-20261015T233027Z-*.log.
     [PARENT] marks fields only the integrating parent may bind (commit hashes,
     acceptance, final scorecard call). Lane HEAD at draft time: 6344569. -->

## Work performed

- Round 2 ran as the operator's **in-session direct dispatch** of a 32-seat
  flash wave. This satisfies round 1's "new-wave role bindings" debt **for this
  wave**: no fleet-rendered wave, no role-alias overlay, and **no Sighting step**
  is claimed. Starting lane HEAD `6344569a68ca9a198df04c7febae58444d821e1f`;
  round-2 artifacts were uncommitted at draft time ([PARENT] commit).
- Landed the coverage move in `tools/research-gate.sh`: new mode
  `verify-claims <claims-file>`, each claim's verbatim span byte-matched against
  its cited **local** source inside the corpus boundary, with per-claim
  disposition plus an exact counting summary under the unchanged exit contract
  (`tools/research-gate.sh:27-45,84,710-859`; boundary helper `:655-708`;
  dispatch `:1465`).
- Pre-registered fixture **`corpus/fixtures/claims-r2.jsonl`** — 17 real claims
  copied from the three archived inputs (13 supported / 2 contradicted /
  2 unsupported), sha256 `23d078cb…`, contract in
  `corpus/fixtures/claims-r2.README.md` (sha256 `44d8a890…`). Authored before the
  mode existed (gate sha `088435…`, zero `verify-claims` tokens), so it is a
  genuine pre-registration, not a post-hoc test.
- Selftest grew 20 → **30 cases** (cases 21-30: `claims-pass`,
  `claims-fail-tampered`, `claims-fail-out-of-corpus`, `claims-fail-external`,
  `claims-fail-session`, `claims-fail-contradicted-unmarked`,
  `claims-fail-stray-marker`, `claims-fail-counting`, `setup-claims-no-path`,
  `setup-claims-missing-file`).
- Evidence receipts (corrected set carries the selftest PASS):
  `corpus/evidence/claims-r2-20261015T233027Z-{fixture,gate,live,selftest}.log`
  (fixture cross-check, r1 regression, live run + four negative controls,
  selftest under `TMPDIR`); the earlier `…-20261015T232752Z-selftest.log` is the
  superseded quota-blocked false negative (see the defect note below). Knowledge
  note: `corpus/knowledge/claim-verification-r2.md`. Lesson:
  `corpus/lessons/2026-10-15-claims-span-fidelity.md`. Receipt index:
  `corpus/evidence/README.md`. Coverage row: `corpus/README.md` (landed with
  rows for the note, fixture and lesson). Skill rows: `SKILL.md` gate table +
  claims-mode section.

## Landed changes

[PARENT] Work HEAD when this report is integrated: `[PARENT: commit hash]`.
Lane commits integrate under identity `chousa-shokunin <chousa@shokunin.local>`.

| Commit | Landed work | LOG connection |
|---|---|---|
| `[PARENT: commit hash]` | `verify-claims` mode + boundary findings + 10 selftest cases; pre-registered fixture; receipts; note; skill rows | `LOG.md:[PARENT]` |

## Before → after measurements

**One axis move: coverage — claim-vs-source verification.** Falsifiable claim:
before, the gate validates record STRUCTURE only and no claim is ever checked
against its cited source; after, `verify-claims` resolves each claim's verbatim
span in its cited local source and reports per-claim verdicts with an exact
counting summary under the existing exit contract (0 CLEAN / 1 DRIFT / 2 setup).

**Before** (shipped round-1 gate, sha256 `08843552…`, lane HEAD `6344569`;
captured by the scribe at 2026-10-15T23:15:27Z, and independently by the
receipts writer):

```text
$ grep -c 'verify-claims' tools/research-gate.sh
0
$ bash tools/research-gate.sh verify corpus/fixtures/claims-r2.jsonl --root ..
RESEARCH_GATE: DRIFT (findings=5 drift=5 questions=0 sources=0 chains=0 claims=0 …)
exit=1
```

The r1 gate has no claim-vs-source mode at all and reports **`claims=0`** on the
real 17-claim fixture — zero claims checked. (`corpus/evidence/claims-r2-20261015T233027Z-live.log:9-18`;
scribe capture `/tmp/chousa-scribe-before.txt`.)

**After** (frozen gate sha256 `03a3324455852ea0025115cb0e3ba9c8cdea10da5edc051c4738854a27c14be0`,
identical across repeated samples after the wave's last edit):

```text
$ bash tools/research-gate.sh verify-claims corpus/fixtures/claims-r2.jsonl --root ..
CLAIM id=A01 expected=supported observed=supported … at=line:52 verdict=match
… (17 lines, all verdict=match; gate at= 52,80,81,88,64,-,47,64,79,69,-,89,92,97,102,130,53)
VERDICT_BEARING_CLAIMS=17/17
RESEARCH_GATE: CLEAN (claims=17 supported=13 contradicted=2 unsupported=2 mismatched=0 unproven=0 refused=0 invalid=0 findings=0 drift=0)
exit=0
```

17/17 match the fixture's pre-registered ground truth
(`claims=17 supported=13 contradicted=2 unsupported=2 mismatched=0`).

**Negative controls** (receipts `corpus/evidence/claims-r2-20261015T233027Z-live.log`, all exit 1):

| Control | Observed | Summary |
|---|---|---|
| Tampered span (A03 `nine`→`ten`) | A03 `observed=unsupported verdict=mismatch`; `CLAIM_SPAN_NOT_FOUND` | `VERDICT_BEARING_CLAIMS=16/17`, DRIFT |
| External URL source (X01) | `observed=refused`; `CLAIM_SOURCE_EXTERNAL` crit ("url source refused (no external fetch)") | 17/18, DRIFT |
| Out-of-corpus source (`/etc/hostname`) | `observed=refused`; `CLAIM_SOURCE_OUT_OF_CORPUS` crit | 17/18, DRIFT |
| Contradicted without marker (A05 marker removed) | `observed=unproven`; `CONTRADICTION_MARKER_ABSENT` | 16/17, DRIFT |

**Selftest:** `bash tools/research-gate.sh --selftest` → `RESEARCH_GATE_SELFTEST:
PASS (30 cases)`, exit 0; the 20 round-1 case lines are byte-identical to the r1
baseline. Setup boundary: `verify-claims` with no path or a missing file → exit
2, stdout empty.

**Existing behavior byte-stable:** at `CHOUSA_NOW_EPOCH=1760000000`, A/B/C each
exit 1 with stdout byte-identical to the r1 baseline, intake exits 0
byte-identical (ts-normalized), `VERDICT_BEARING_EXPORTS=3/3`
(`corpus/evidence/claims-r2-…-gate.log`).

**No-external-fetch bound is absolute:** no fetch primitive exists in the gate
(`grep -E '\b(curl|wget|nc|ssh|scp|ftp|dig|nslookup)\b'` → none); sources are
canonicalized with `readlink -f` and must resolve under `CHOUSA_ROOT` or the lane
root; URLs → `CLAIM_SOURCE_EXTERNAL` crit, session/denylist → `CLAIM_SOURCE_SESSION`
crit, outside both roots → `CLAIM_SOURCE_OUT_OF_CORPUS` crit, all **refused
before any read** (`tools/research-gate.sh:655-708`). The expect vocabulary has
no `refused`, so a fixture cannot pre-register its way past a refusal.

**Environment defect (named, resolved in-wave; not a gate defect):** the first
receipts pass ran while the host `/tmp` tmpfs hit its shared user quota
(`usrquota`), so its selftest capture failed —
`corpus/evidence/claims-r2-20261015T232752Z-selftest.log` records `exit: 1` with
`tools/research-gate.sh: line 873: printf: write error: Disk quota exceeded` —
and its case-line diff is a false negative from the same exhaustion, not a gate
regression. The frozen revision honors `TMPDIR` (`:863-872`); the corrected
receipts set `…-20261015T233027Z-selftest.log` re-ran under
`TMPDIR=/home/vgpnk/.cache/chousa-r2/tmp` and gives `RESEARCH_GATE_SELFTEST: PASS
(30 cases)`, exit 0, with round-1 case lines 1-20 byte-identical. The scribe
independently reproduced that PASS under the same quota pressure. The
`232752Z` selftest line is the superseded environment-blocked capture; the fleet
`/tmp` quota remains an environment-owned item (see debt).

## SHONEN

Author assertions only; a `[x]` requires a named non-author verifier, which this
round did not have. No promotion is implied.

- [~] SKILL.md carries real decision tables/error patterns/checklists: gate table
  now has a `verify-claims` row plus a claims-mode section with the measured
  revision and limits (`SKILL.md` Gates). Hierarchy rows remain `proposal` where
  independently unsupported.
- [~] At least one end-to-end domain task executed and logged: 17-claim
  claim-vs-source verification over the three pinned archives, receipts
  `corpus/evidence/claims-r2-20261015T233027Z-*.log`; no external semantic
  verification is claimed.
- [~] Instructions executable without oral context: `verify-claims <claims-file>
  [--root PATH]` runs from the lane cwd; re-run commands are in the note and the
  fixture README. No independent agent-without-oral-context review is claimed.
- [~] No cross-domain bleed: PROVINCE.md unchanged; the fixture keeps
  foreign-province material (B03 numerals, rank/governance text) as byte controls
  and near-misses, never adopted.

## Per-axis and learning verdicts

Verdict vocabulary only; no scalar. The declared round move is **coverage**;
other axes are judged separately with their own evidence boundaries.

| Axis | Verdict | Evidence boundary |
|---|---|---|
| coverage | improved | Before: no claim checked (`claims=0`, structure only). After: 17/17 pre-registered claims across A/B/C checked with per-claim verdicts; 2 structural contradictions and 2 unsupported near-misses observed; refusals for external/session/out-of-corpus. Boundary: span byte identity inside the corpus roots, not semantics — the `claim` label is never compared with its span, so a claim may assert the opposite of its span and still close CLEAN |
| operability | improved | New public mode runs under the preserved exit contract; selftest 20 → 30 all PASS; r1 verify paths byte-identical. Boundary: the round-1 narrow count (3/3 archives) is unchanged; [PARENT: this row reads `improved` on the new runnable mode — keep, or set `unchanged` if only the capped 3/3 count is read] |
| depth | unchanged | No independently verified domain fact; fixture spans are byte controls, not adopted knowledge |
| freshness | unchanged | Archive pins re-checked at fixed revisions only; no new cross-revision drift detector |
| calibration | unchanged | Structural limits stated (CLEAN = every observed status equals its expectation; no semantics); no non-author discernment |
| adjacency | unchanged | Foreign-province content kept as rejections/near-misses, not absorbed |

Learning trends: **expansion improved** — a net-new admitted entry
(`corpus/knowledge/claim-verification-r2.md`) on ground the coverage map did not
hold, plus a new gate edge class; the `corpus/README.md` coverage rows landed.
**quality unchanged** — the new CLEAN is structural; no older admitted entry was
reverified or superseded.
**discernment unchanged** — no non-author admit/reject spot-check.

## Debt, cross-domain handoff and admission

| Debt | Owner / concrete unblock |
|---|---|
| **Receipt identity (round 1) — STILL OPEN** | The direct interactive launch supplies no authentic queue taskKey or stored expected receipt bag (`.ufo/evidence/round-1/receipt-blocker.json`). Mission acceptance remains integrator-owned: bind this mission/identity to an authentic dispatcher task and validate the six expected fields before any Sighting completion. No `task_…` value was invented; proven receipt-backed completed rounds remain **0**; operator target remains at least 100. |
| New-wave role bindings | **Satisfied for this wave** by the operator's in-session direct dispatch. No fleet-rendered wave or role-alias overlay was created by the lane; **no Sighting was invoked**. |
| Scope-refusal finding IDs (round-1 debt) | Still open — documentary refusals only; a future single move implements the three catalogue scope findings with symmetric exit-1 fixtures. |
| Non-author spot-check (discernment) | Integrator/operator samples ≥1 admit and ≥1 reject and records agree/disagree; until then no discernment gain or promotion. |
| Frozen replay gate conformance | `corpus/evidence/round-1/expected.json` pins inputs but is not a rerunnable comparator; still open. |
| Fleet `/tmp` quota exhaustion | Integrator/environment-owned: the `/tmp` tmpfs hit its quota mid-wave, breaking one receipt (selftest) and silently truncating small writes across seats. The gate honors `TMPDIR`; other lane tooling and receipts should too. |

Cross-domain: no host/source/sibling/shared-ledger mutation; the archived
research corpus was read-only; native session material excluded from commits.

## Fresh-session continuation

[PARENT] Bind `.ufo/continuations/round-2.json` (or the round-1 successor file)
to this report and the integrated work HEAD. Acceptance stays separate from
local craft results: this report claims local evidence only, no receipt and no
Sighting.
