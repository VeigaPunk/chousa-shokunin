# SCORECARD.md — round-10 draft sections (parent-owned file; [PARENT] binds)

<!-- SCRIBE DRAFT — MEASURED through the before-state battery, controls,
     exempt audit and ledger reconciliation (one ledger-completeness finding);
     receipts/SKILL/README integrate as landed. Gate sha256
     46f5ddb39d5fafa220fb584121dba2f4a15e071a91fa42728849f3c7567c6ccd on both
     sides (== HEAD `d5c99c2` blob; working-tree sha identical before and after
     the runs, re-derived 05:49Z; `git diff --numstat tools/research-gate.sh`
     EMPTY — fixture-led round, no gate change; a gate change without a
     reported defect would be a finding — measured none). Lane HEAD `d5c99c2`;
     no commits by any seat. Verdict vocabulary only: improved / unchanged /
     harmed / unprovable-but-better. No scalar scores. [PARENT] marks
     parent-only bindings. The admission section keeps the receipt-identity
     debt OPEN, per the mission contract. -->

<!-- Artifact status markers:
     [[CONTROLS]] LANDED 05:41Z, MEASURED — corpus/fixtures/archives-r9/controls/ (controls-author)
     [[LEDGER]]   LANDED 05:45:38Z (`f5dc8889…`), RECONCILED — one finding:
                  three carried residuals unmapped vs §3.9's completeness claim
     [[LESSON]]   LANDED (`92656ca2…`)
     [[RECEIPTS]] corpus/evidence/ (receipts-writer) — pending at last check (~05:52Z)
     [PARENT: SKILL.md rows (skill-row-updater), corpus/README.md row
      (corpus-readme-updater) — integrate as landed] -->

Rounds 1–9 sections stay as written. These are the round-10 sections to
append, plus the admission/`Planned` refresh. **This round executes the move
round 9 registered** (residual hardening — negative controls at archive scale,
the exempt-hop audit, and disposition of every r2–r9 named limit). The
falsifiable claim, in the round's own words: before, no negative controls
exist at archive scale (defect classes are only covered by small fixtures),
the exempt items in the archive records are unaudited, and the limits named
across rounds 2–9 have no single disposition ledger. After, one broken archive
record per defect class (span-not-found, anchor-missing, dangling-ref,
rejection-missing-flip, false-sweep, structure-break) each DRIFTs verify-all
naming exactly its class; every exempt item in the archive records is
justified by source bytes (or is a finding); `corpus/knowledge/hardening-r10.md`
carries the complete disposition ledger.

**Before** (gate `46f5ddb3…`, lane HEAD `d5c99c2`): MEASURED —
`ls corpus/fixtures/archives-r9/controls/` → No such file or directory (no
archive-scale negative control exists); selftest `PASS (85 cases)` exit 0;
`--drift` vs the r8 baseline `GATE_DRIFT: none` exit 0; the three archive
records compose CLEAN as at r9 (A `RESOLVED_HOPS=6/7` · `VERIFIED_SWEEPS=1/1
REJECTIONS_OK=4/4` · `INTEGRITY refs=13 resolved=12 unresolved=0`; B 6/7 ·
3/3 · 14/13/0; C 7/8 · 4/4 · 15/14/0; claims 10/10 each; all
`sections=5 run=5 absent=0 drift-sections=0 findings=0 drift=0` exit 0);
regressions claims-r2 17/17 · claims-r9 10/10 · chain-r3 17/22 · r1
`VERDICT_BEARING_EXPORTS=3/3`. The three-part hole: no archive-scale negative
control; the records' 6 exempt items unaudited; the r2–r9 limits scattered
across nine notes with no single disposition ledger.

**After** (gate `46f5ddb3…`, unchanged — fixture-led): MEASURED —
exempt audit 6/6 justified; [[CONTROLS]] six controls, all six naming exactly
their class; [[LEDGER]] 68-row ledger reconciled with one finding (three
carried residual classes unmapped while §3.9 claims completeness). Details
below and in the report's part 1–3.

- **Exempt-item audit (measured, this seat):** the records' exempt items are
  exactly 6 — three `blocked-no-fetch` chain hops (A `コトバンク`, B
  `arxiv.org`, C `jstage.jst.go.jp`) and the three integrity tokens on those
  rows (A `C1`, B `C3`, C `C8`, each a DECLARED claim id, so nothing dangling
  hides behind the exemption). Each chip name is byte-present in its archive
  at the lines the record's note names (A:68; B:51+B:72; C:103 — bare chips
  alone on their lines, not URLs, not local paths), so no local resolution is
  possible and `blocked-no-fetch` is the truthful status; **6/6 justified by
  source bytes, 0 findings.** Sweep globs re-run empty (`saved-*`,
  `*-snapshot-*` → both absent), matching `VERIFIED_SWEEPS=1/1` on all three.
- **[[CONTROLS]]:** MEASURED — six controls landed (05:41Z; single-cell/section
  mutations, base diffs independently re-derived), all six compose DRIFT exit 1
  with `drift-sections=1 findings=1` naming exactly their class
  (`CLAIM_SPAN_NOT_FOUND` id=A07 / `CHAIN_ANCHOR_NOT_FOUND` hop=2 /
  `SWEEP_REJECTION_INCOMPLETE` id=R2 / `SWEEP_CLAIM_FALSE` id=SW1 hits=3 /
  `REF_UNRESOLVED` C9 chain row 1 / `NO_QUESTION` crit), every other section
  CLEAN, clean bases still CLEAN in the same window; the controls README's own
  runs (05:40–05:42Z) reproduce every line modulo `ts=`. See the report's
  part-1 table for tallies and shas.
- **[[LEDGER]]:** MEASURED, one finding — `corpus/knowledge/hardening-r10.md`
  landed (sha `f5dc8889…`, 30317 B; 68 rows: by-design 38 · carried 22 ·
  closed 3 · finding 1 · operator 4; 27-item round-11 audit queue). Reported,
  not fixed: the reconciliation against this seat's enumeration maps every
  class except THREE carried residuals named in the r2–r8 notes (and listed in
  the lesson's own §5) — in-root hardlink bypass, no source size cap, cosmetic
  banner `research-gate-r1` — which have no row in §3.1–§3.9 while §3.9
  (`hardening-r10.md:306-313`) claims item-by-item completeness; a finding,
  ledger-side (note-writer's file: three rows + the counts/queue arithmetic).
  Everything the ledger does carry re-checks clean (row/queue counts re-derived;
  row 53 matches the live `A-r9.md:50` state).

| Axis | Verdict | Evidence boundary |
|---|---|---|
| calibration | **improved** | The round's selected axis, MEASURED: the gate's detection boundaries are now demonstrated at the archive scale, not only on small fixtures — six broken archive records, one per defect class, each composing `DRIFT … drift-sections=1 findings=1` naming exactly its class's finding id (`CLAIM_SPAN_NOT_FOUND` A07; `CHAIN_ANCHOR_NOT_FOUND` hop=2; `SWEEP_REJECTION_INCOMPLETE` R2; `SWEEP_CLAIM_FALSE` SW1 hits=3; `REF_UNRESOLVED` C9 chain row 1; `NO_QUESTION` crit), exit 1, every other section CLEAN; each control independently re-derived as a single-cell/section mutation of its clean base; bases still CLEAN in the same window. And the records' exemptions are audited rather than counted-and-ignored: 6/6 justified by source bytes against the read-only archives, with the general "exemption is a declaration" limit kept named. |
| coverage | **improved** (one finding) | New measured surface: 6 archive-scale negative controls, the first negative controls against the archive corpus — each measured to DRIFT naming exactly its class with the other four sections CLEAN; plus the 68-row r2–r9 disposition ledger (one reconciliation finding: three carried residuals unmapped, ledger-side). Before: zero archive-scale controls and no ledger. |
| depth | **improved** (one finding) | The ledger note (`corpus/knowledge/hardening-r10.md`, sha `f5dc8889…`, 30317 B) carries the semantics this round owed: 68 dispositioned rows with evidence (38 by-design · 22 carried · 3 closed · 1 finding · 4 operator), the controls class map, the exempt audit, and a 27-item round-11 queue; this seat's reconciliation found three carried residuals (in-root hardlink bypass, no source size cap, cosmetic banner) with no row while §3.9 claims item-by-item completeness → named finding, ledger-side (note-writer's file). [PARENT: same precedent as r2–r9 note-per-round.] |
| operability | **unchanged** | By design: no gate file changed (sha `46f5ddb3…` before the battery; diff vs HEAD blob EMPTY). The controls battery exercises all five composed sections on broken archive records — but no new mode/flag/branch lands, so the tool's operability boundary is unmoved; regressions held (claims-r2 17/17, claims-r9 10/10, chain-r3 17/22, r1 3/3, selftest 85, `GATE_DRIFT: none`). |
| freshness | **unchanged** | No new drift detector or pinned artifact; [[RECEIPTS]] pending — when they land they are receipts at the unchanged SHA. |
| adjacency | **unchanged** | Corpus boundaries held: archives quoted read-only, never written; controls live under the lane's own `corpus/fixtures/`; zero network (no fetch paths; blocked chips stay unopened); seats write only in owned paths; no commits. |

## Round-10 learning trends

| Trend | Verdict | Evidence |
|---|---|---|
| expansion | **improved** | New specimens: [[CONTROLS]] `corpus/fixtures/archives-r9/controls/` (6 controls + claims copy + README; shas pinned; all six measured to name exactly their class); the exempt audit (6/6 justified by source bytes) is part of the round's evidence; [[LEDGER]] `corpus/knowledge/hardening-r10.md`, [[LESSON]], [[RECEIPTS]] integrate as landed. |
| quality | **improved** (one finding) | The falsifiable claim measured on both sides: zero archive-scale controls → six, each naming exactly its class with every other section CLEAN; unaudited exemptions → 6/6 justified against source bytes; scattered limits → one 68-row ledger + 27-item queue. One reconciliation finding: three carried residuals lack rows while §3.9 claims completeness (ledger-side; report part 3). |
| discernment | **unchanged** | No non-author admit/reject spot-check exists; no criterion added. |

## Admission and continuation (round-10 replacement text)

[PARENT: refresh the round-9 admission paragraphs after integration.]

Local axis result: calibration improved (all six archive-scale controls
measured, each DRIFTing with exactly its class and every other section CLEAN);
coverage improved; depth improved with one finding (the ledger's three
unmapped carried residuals — ledger-side, named); operability unchanged
(fixture-led — the gate sha held, exactly as the round declared); freshness
unchanged; adjacency unchanged. Named limits carried into the record: the
general "exempt ≠ verified" limit (r3) survives the audit — the audit
justifies exactly the archive records' 6 instances, it cannot check a
different exemption; the `A-r9.md:50` pointer-line defect persists (re-verified
at `338918fc…`: pointer :76, span at A:86, invisible to every gate mode; the
ledger's single `finding` row 53); and the three ledger-completeness misses
above are this round's integration-relevant finding. [PARENT: adjust the axis
cells if integration finds a landed artifact disagreeing with a measured
value.]

Mission acceptance is separate and remains blocked on the round-1 receipt
identity: the interactive launch has no authentic queue taskKey/expected
receipt bag, so no `task_…` value may be manufactured, no shape-only receipt
counted, and no Sighting marked complete. Receipt-backed verified rounds
remain **0**; the operator target remains at least 100. Routing for this wave
was satisfied by the operator's in-session direct dispatch; no Sighting was
invoked. The round-10 artifacts are lane evidence, not a mission receipt.

Debt after round 10: receipt identity (integrator) — **STILL OPEN**; no
controls gap (landed 05:41Z, measured); new — ledger completeness (three
carried residual classes unmapped in `hardening-r10.md` §3 while §3.9 claims
completeness; ledger-side, note-writer's file: three rows + the counts/queue
arithmetic); the carried list holds — omitted!=absent limit (r6),
non-vacuous flip screening (r5), id-shape boundary (r7), manifest schema
growth, nested execution cost, non-author spot-check (integrator/operator),
usage/outside-path pin blind spot (r8), masked-set blind spots (r8), re-pin
policy (r8), carried residuals (in-root hardlinks, no source size cap,
token-aligned shortening, non-ASCII-adjacent fail-closed edges, scope-refusal
finding IDs, frozen-replay comparator); r9 carries (record claims-table `span`
outside every gate check; `path#quote:text` structure quirk; reframing
residual; `A-r9.md:50` pointer-line defect). [PARENT: artifact ledger with
shas at integration time.] See `.ufo/round-10/goal-wave/report-draft.md` for
owners.

## Planned (round-10 refresh)

[PARENT: replace the round-9 `Planned` paragraph.] Round 10's registered move
(residual hardening — archive-scale negative controls, the exempt-hop audit,
the r2–r9 limit-disposition ledger) ran in the operator's in-session wave.
**Round 11 (next) is the capstone audit — this round produces its starting
map:** the controls (what each defect class looks like when it fires at
archive scale), the audited exemption set (the 6 items and their source-byte
justifications), and the disposition ledger (every carried limit, marked).
Round 11 should audit the lane against that map rather than re-deriving it;
any next round must again declare its own falsifiable single move and genuine
scope before dispatch; do not rerun this round's wave. Standing lane
candidates: the residuals named under Debt.