# SCORECARD.md — round-8 draft sections (parent-owned file; [PARENT] binds)

<!-- SCRIBE DRAFT — MEASURED FINAL. Before: gate sha256
     3ba718bf9207eed70c66b8c849ac43b44c76890785e1576eeb5e795a604166b2
     (== lane HEAD `848738c`; `git diff tools/research-gate.sh` EMPTY).
     After: gate sha256
     46f5ddb39d5fafa220fb584121dba2f4a15e071a91fa42728849f3c7567c6ccd
     (+523/−6; stable ≥2 min before this seat's battery, sha identical before
     and after it). Lane HEAD still `848738c`; no commits by any seat.
     Verdict vocabulary only: improved / unchanged / harmed /
     unprovable-but-better. No scalar scores. [PARENT] marks parent-only
     bindings. The admission section keeps the receipt-identity debt OPEN,
     per the mission contract. -->

Rounds 1–7 sections stay as written. These are the round-8 sections to
append, plus the admission/`Planned` refresh.

## Round-8 per-axis verdicts

Measurements: both sides measured fresh-process by the scribe seat; the
before side at the checked-out gate (`3ba718bf…`, `git diff` empty), the
after side at the settled revision `46f5ddb3…` with the sha identical before
and after the whole battery. Falsifiable claim: before, the gate's own
behavior had no baseline — a regression (a mode silently skipped, an output
field changed) was only catchable by reading a previous round's receipts and
comparing by hand; after, `--pin` captures a normalized baseline of a
hermetic canonical invocation with a declared volatile contract, `--drift`
reports `GATE_DRIFT: none` exit 0 / names changed tokens exit 1 /
missing-malformed exit 2, a baseline is committed under `corpus/evidence/`
with a re-run recipe, and all 74 prior selftest cases are byte-stable.

**Before** (gate `3ba718bf…`, lane HEAD `848738c`): `--pin`/`--drift` are
unknown flags (exit 2, no file written); zero `GATE_PIN`/`GATE_DRIFT` strings
in the gate; no baseline under `corpus/evidence/`; selftest PASS (74 cases)
with case lines byte-identical to the r7 receipt.

**After** (gate `46f5ddb3…`, selftest 85): `--pin` → `GATE_PIN: ok
path=… gate_sha256=46f5ddb3…` exit 0; the committed baseline
`corpus/evidence/gate-baseline-r8-20261016T033757Z.json` (2988 B, sha256
`1c81a6cb…`, header `volatile_fields=ts gate_sha256`) drifts `none` exit 0;
two independent pins at this revision have byte-identical canonical bodies;
drift holds `none` across 65 s of live churn and a +2.6-day clock shift; the
silently-skipped-chain mutant is named (`GATE_DRIFT: -SECTION:chain …`), the
field mutant is named (`drift severity`), the banner-word mutant — which the
selftest tolerates (PASS 85/85) — is named (`GATE`), a comment-only different-
sha copy reads `none` (behavioral, not revision-bound); the malformed/missing
battery all exit 2 (seven distinct messages), a rewritten volatile list reads
`volatile_fields` exit 1; all solo regressions held (claims 17/17 · chain
17/22 + broken 1/2 · sweeps · integrity · full-r6 trio · r1 archives 3/3);
selftest 74 → 85 with cases 1–74 byte-identical; strace zero network on both
legs (0 of 3754 / 0 of 3759).

| Axis | Verdict | Evidence boundary |
|---|---|---|
| freshness | **improved** | The round's selected axis: the gate's own drift is now detectable against a committed baseline with a declared volatile contract — `none` across churn and clock shifts (measured), named tokens on three mutant classes, `volatile_fields` when the contract itself is edited. This is the lane's second durable append-only ledger-like artifact (baseline text file) and its first cross-revision behavioral comparison. |
| operability | **improved** | Two new modes (`--pin`/`--drift`) with the exit contract 0/1/2 held across the missing/unreadable/malformed battery (seven distinct messages), the flag guards and mutual exclusion; selftest 74→85 with cases 1–74 byte-identical; all five solo modes and the composed verify-all byte-stable on their fixtures; the r1 observable intact (3/3); zero network. |
| depth | **improved** [PARENT: r2–r7 precedent — each admitted scorecard credited the landed knowledge note under depth; `corpus/knowledge/gate-baseline-r8.md` (18454 B, `d7370ecf…`) and the lesson `corpus/lessons/2026-10-16-gate-behavioral-baseline.md` (19512 B, `9c906ad8…`) both landed before this seat's last check] | This seat independently re-derived the load-bearing observables (canonical body shape, hermetic pin equality, the churn/clock holds, the three mutant reports, the malformed messages, the regressions) and they agree with the note; the semantics (canonical invocation, volatile contract, exit grammar, blind spots) are documented in the gate header `:153` ff. and the note. |
| coverage | **unchanged** | No new measured surface of the province or of a record's content; the round makes the gate's own behavior comparable over time. All five existing modes' fixture contracts held (measured battery). |
| calibration | **improved** [PARENT: if integration reads the volatile contract + named blind spots as r7-style boundary-naming rather than a calibration gain, mark unchanged] | The tool now declares exactly what its `none` means: the masked set (`ts` shape-scoped, `gate_sha256`) travels in every baseline header, the contract is itself compared (`volatile_fields`), consultation honesty measured — the banner mutant the selftest tolerates is named by the pin, while the usage-text edit outside the demonstrated path reads `none` (a measured, named blind spot, not a hidden one). |
| adjacency | **unchanged** | Zero network (strace on both pin and drift legs: 0 network lines of 3754 / 3759); corpus read-only; `--pin` writes only the path given, `--drift` zero writes; seats wrote only in-lane. |

Scribe-found limits (measured; candidates for `Planned`/future rounds):

- **Outside-path edits are invisible.** A usage-text edit reads
  `GATE_DRIFT: none` exit 0 (line 316 measured) — the canonical invocation
  never prints the usage. Any edit outside the demonstrated path (usage/help,
  dead branches) is unseen by both the selftest (this class) and the pin.
- **The pin's added power over the selftest is partial, and measured as
  such.** The two round-named regression classes are also caught by the
  selftest (chain-skip FAIL 8/85; severity field FAIL 6/85); the pin's extra
  reach measured: the selftest-tolerated banner class (`GATE` exit 1), the
  named-field reports, and the durable committed contract.
- **Masked-set blind spots.** Every masked field is where a real regression
  reads `none`; `ts` is shape-scoped so malformed timestamps surface
  (measured by the note: `ts=epoch-…` → `GATE_DRIFT: ts`).
- **Baseline aging/re-pin policy.** The canonical capture is hermetic, so
  aging is small; re-pinning must remain a recorded act with a reason.
- **Nested execution cost (carried).** Each pin/drift leg runs one full
  composed verify-all (5 sections as fresh solo calls); ~2–3 s wall per leg
  measured at wave load.
- **Cosmetic (carried, now visible).** The banner still reads
  `research-gate-r1` — and with the pin it is no longer invisible: the
  banner-word mutant reads `GATE_DRIFT: GATE`.

## Round-8 learning trends

| Trend | Verdict | Evidence |
|---|---|---|
| expansion | improved | New admitted specimens: committed lane baseline `corpus/evidence/gate-baseline-r8-20261016T033757Z.json` (`1c81a6cb…`); receipts `pin-r8-20261016T033757Z-{pin,drift,live,selftest}.log` (`40abd23d…`, `051695ee…`, `9829ed10…`, `6334240b…`); note + lesson (shas above); `corpus/evidence/README.md` (`685efae8…`: rounds 2-8 + the round-8 receipts section); selftest +11 cases (75–85); `SKILL.md` r8 rows (`a358cdd2…`); [PARENT: `corpus/README.md` row — not landed by this seat's last check]. |
| quality | improved | The round's falsifiable claim is measured on both sides: the before-state has no mechanism (unknown flags, no baseline), the after-state names the silently-skipped mode, the changed field, and the selftest-tolerated cosmetic word — while the comment-only control reads `none` and the committed baseline holds `none` across churn. |
| discernment | unchanged | No non-author admit/reject spot-check exists; no criterion added. |

## Admission and continuation (round-8 replacement text)

[PARENT: refresh the round-7 admission paragraphs after integration.]

Local axis result: freshness improved (the gate's own drift is now detectable
against a committed baseline — `none` across churn and clock shifts, named
tokens on mutant classes, `volatile_fields` on contract edits),
operability improved (selftest 74→85 with 1–74 byte-identical; two fail-closed
modes; exit contract 0/1/2 held across the malformed battery; zero network),
calibration improved [PARENT: or unchanged, see the cell],
depth improved under the r2–r7 note precedent [PARENT]; coverage/adjacency
unchanged; none harmed. Accepted limits, named rather than hidden: the
usage/outside-path blind spot (measured); the masked-set blind spots (the
contract travels in every header); the selftest-overlap nuance (complement,
not replacement); baseline aging/re-pin policy; nested execution cost. No
scalar substitute, no promotion. [PARENT: adjust the axis cells if integration
finds a landed artifact disagreeing with a measured value, or if the gate
moves past `46f5ddb3…`.]

Mission acceptance is separate and remains blocked on the round-1 receipt
identity: the interactive launch has no authentic queue taskKey/expected
receipt bag, so no `task_…` value may be manufactured, no shape-only receipt
counted, and no Sighting marked complete. Receipt-backed verified rounds
remain **0**; the operator target remains at least 100. Routing for this wave
was satisfied by the operator's in-session direct dispatch; no Sighting was
invoked. The round-8 artifacts are lane evidence, not a mission receipt.

Debt after round 8: receipt identity (integrator) — **STILL OPEN**; the new
usage/outside-path blind spot; the masked-set blind spots; the re-pin policy
as a standing ritual [PARENT]; nested execution cost; the absent!=drift
omission limit (r6, still open); non-vacuous flip screening (r5); the id-shape
boundary (r7); manifest schema growth; non-author spot-check
(integrator/operator); carried residuals (in-root hardlinks, no source size
cap, token-aligned shortening, non-ASCII-adjacent fail-closed edges,
scope-refusal finding IDs, frozen-replay comparator). Artifact ledger at draft
time (uncommitted, at the settled gate): gate `46f5ddb3…` (+523/−6), baseline
`1c81a6cb…`, receipts shas above, note `d7370ecf…`, lesson `9c906ad8…`,
`SKILL.md` `a358cdd2…` [PARENT: `corpus/README.md` row when it lands].
Integrate only what lands. See `.ufo/round-8/goal-wave/report-draft.md` for
owners.

## Planned (round-8 refresh)

[PARENT: replace the round-7 `Planned` paragraph.] Round 8's registered move
(the gate's own behavioral baseline — `--pin`/`--drift` adapted from the
sibling lane's proven pattern) ran in the operator's in-session wave and is
measured (the two-side contract above). Round 9 registered: [PARENT: proposed
candidates — (a) the measured usage/outside-path blind spot (the demonstration
path could be widened, e.g. a second canonical leg exercising the usage or a
representative record); (b) the absent!=drift omission limit (r6, carried);
(c) non-vacuous flip screening (r5, carried); (d) manifest schema versioning.
Choose one falsifiable move.] Any next round must again declare its own
falsifiable single move and genuine scope before dispatch; do not rerun this
round's wave. Standing lane candidates: the residuals named under Debt.