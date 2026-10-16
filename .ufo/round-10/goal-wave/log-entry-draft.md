# LOG.md — round-10 entry draft (parent-owned file; integrate under [PARENT] markers)

<!-- SCRIBE DRAFT — MEASURED through the before-state battery, controls,
     exempt audit and ledger reconciliation (one ledger-completeness finding);
     receipts/SKILL/README integrate as landed. Gate sha256
     46f5ddb39d5fafa220fb584121dba2f4a15e071a91fa42728849f3c7567c6ccd on both
     sides (== HEAD `d5c99c2` blob; working-tree sha identical before and after
     the runs, re-derived 05:49Z; `git diff --numstat tools/research-gate.sh`
     EMPTY — fixture-led round, no gate change; a change without a reported
     defect would itself be a finding — measured none). Lane HEAD `d5c99c2`;
     no commits by any seat. Scribe scratch $HOME/.cache/chousa-tmp/
     (`scribe-r10-*.log`; declared ephemeral, cleaned at end of run). [PARENT]
     marks parent-only bindings. The debts section keeps the receipt-identity
     debt OPEN per the mission contract. -->

## 2026-10-16 — round-10 calibration (fixture-led): archive-scale negative controls + the limit-disposition ledger

Round 10 executes the move round 9 registered: **residual hardening** — (a)
negative controls at archive scale (one broken archive record per defect
class), (b) the exempt-hop audit, (c) disposition of every r2–r9 named limit.
The operator dispatched this wave directly in-session (same routing as rounds
2–9; **no Sighting step was invoked**); receipt identity from round 1 remains
open and untouched by this round. Fixture-led: **no `tools/research-gate.sh`
change** — measured, not assumed (working-tree sha == HEAD blob, diff empty
before the battery).

**Before (MEASURED at gate `46f5ddb3…`, lane HEAD `d5c99c2`):**

```text
$ git show HEAD:tools/research-gate.sh | sha256sum → 46f5ddb3… (== working tree; git diff EMPTY)
$ bash tools/research-gate.sh --selftest           → RESEARCH_GATE_SELFTEST: PASS (85 cases) exit=0
$ bash tools/research-gate.sh --drift corpus/evidence/gate-baseline-r8-20261016T033757Z.json
                                                   → GATE_DRIFT: none exit=0
$ ls corpus/fixtures/archives-r9/controls/         → No such file or directory

$ verify-all per archive record (claims bound via Meta) — A/B/C each:
  sections=5 run=5 absent=0 drift-sections=0 findings=0 drift=0, CLEAN exit=0
  A chain 6/7 · sweeps 1/1 4/4 · integrity refs=13 resolved=12 unresolved=0
  B chain 6/7 · sweeps 1/1 3/3 · integrity refs=14 resolved=13 unresolved=0
  C chain 7/8 · sweeps 1/1 4/4 · integrity refs=15 resolved=14 unresolved=0
  claims 10/10 on each
$ regressions: claims-r2 17/17 · claims-r9 10/10 · chain-r3 17/22 · r1 observable 3/3
```

**The move.** Part 1, **archive-scale negative controls** (landed 05:41Z,
measured 05:43Z by this seat; controls-author's README records its own runs
05:40–05:42Z and every line reproduces modulo `ts=`). Six controls under
`corpus/fixtures/archives-r9/controls/`, each a scripted single-cell/section
mutation of a clean archive record (bases `338918fc…` / `abfa5290…` /
`97be0e69…`; base diffs re-derived by this seat: A hop 2 quote
`rank`→`certification`; A claims copy A07 span `four`→`five`; B R2 flip
emptied; B SW1 where → `…/2026-09-28/*.md`; C hop 1 `from` `C1`→`C9`; C
`## Question` removed). All six:

```text
A-r9-span-not-found   → claims DRIFT   CLAIM_SPAN_NOT_FOUND id=A07   VERDICT_BEARING_CLAIMS=9/10      exit=1
A-r9-anchor-missing   → chain DRIFT    CHAIN_ANCHOR_NOT_FOUND hop=2  RESOLVED_HOPS=5/7                exit=1
B-r9-rejection-missing-flip → sweeps DRIFT  SWEEP_REJECTION_INCOMPLETE id=R2 missing=flip  REJECTIONS_OK=2/3  exit=1
B-r9-false-sweep      → sweeps DRIFT   SWEEP_CLAIM_FALSE id=SW1 hits=3  VERIFIED_SWEEPS=0/1          exit=1
C-r9-dangling-ref     → integrity DRIFT  REF_UNRESOLVED kind=claim id=C9 chain row=1 from  refs=15 resolved=13 unresolved=1  exit=1
C-r9-structure-break  → structure DRIFT  NO_QUESTION crit            findings=1                      exit=1
each: VERIFY_ALL sections=5 run=5 absent=0 drift-sections=1 findings=1 drift=1 · RESEARCH_GATE: DRIFT
each: the other four sections CLEAN; the clean bases still CLEAN exit=0 in the same window
companion direct run: verify-claims A-r9-span-not-found.claims.jsonl → 9/10 DRIFT exit=1
control shas: 5dedb73b… (span-not-found.md) · 0edb78ee… (its claims copy) · e3490cf4… (anchor-missing) ·
  b0d488aa… (rejection-missing-flip) · 69b7b08f… (false-sweep) · b24be0f0… (dangling-ref) · 21d77e6c… (structure-break)
```

Part 2, the **exempt-item audit** (MEASURED, this seat; solo runs at the
unchanged gate):

```text
A-r9.md: CHAIN hop=7 status=blocked-no-fetch observed=exempt source=コトバンク anchor=- at=- verdict=exempt
          REF kind=claim id=C1 section=chain row=7 cell=from observed=exempt verdict=exempt status=blocked-no-fetch
B-r9.md: CHAIN hop=7 status=blocked-no-fetch observed=exempt source=arxiv.org anchor=- at=- verdict=exempt
          REF kind=claim id=C3 section=chain row=7 cell=from observed=exempt verdict=exempt status=blocked-no-fetch
C-r9.md: CHAIN hop=8 status=blocked-no-fetch observed=exempt source=jstage.jst.go.jp anchor=- at=- verdict=exempt
          REF kind=claim id=C8 section=chain row=8 cell=from observed=exempt verdict=exempt status=blocked-no-fetch

audit: 6/6 exempt items justified by source bytes, 0 findings —
  A hop7 コトバンク: grep -n → A:68, A:72 (bare chips alone on their lines; record note names A:68)
  B hop7 arxiv.org: grep -n → B:51, B:72 (record note names both; bare chips)
  C hop8 jstage.jst.go.jp: grep -n → C:103 (record note names C:103; bare chip)
  the three integrity tokens are the from-cells of those exempt rows and are DECLARED claim
  ids (A C1 / B C3 / C C8) — no dangling id hides behind the exemption
  sweep globs re-run: ls ../research/deep-research-2026-09-28/saved-* *-snapshot-* → both absent
```

Part 3, the **disposition ledger** [[LEDGER]] (landed 05:45:38Z; note-writer):
`corpus/knowledge/hardening-r10.md` (sha `f5dc8889534a8527d5fd010c1f9e2493d4214f358566d0f1fea0e91ae1f3a2f0`,
30317 B) — 68 rows (by-design 38 · carried 22 · closed 3 · finding 1 ·
operator 4) + a 27-item round-11 audit queue. This seat's reconciliation
against the r2–r9 limit enumeration (report §Named limits): all classes map
except THREE carried residuals — in-root hardlink bypass, no source size cap,
cosmetic banner `research-gate-r1` (named in the r2–r8 notes; the lesson's §5
lists them too) — which have no row in §3.1–§3.9 while §3.9
(`corpus/knowledge/hardening-r10.md:306-313`) claims item-by-item
completeness. **FINDING (ledger-side, note-writer's file; reported, not
fixed):** the ledger is three rows short of its completeness claim. All other
ledger content re-checks clean: row count and disposition counts re-derive by
grep; the queue arithmetic closes for its own 68 rows; its single `finding`
row 53 matches this seat's re-verified `A-r9.md:50` state; §1/§2 reproduce
this seat's control runs and exempt audit.

**Measurements after the move** (gate `46f5ddb3…`; fresh processes; verbatim):

```text
Controls, all six (this seat 05:43Z; controls README's runs 05:40–05:42Z reproduce modulo ts=):
  A-r9-span-not-found        claims    DRIFT CLAIM_SPAN_NOT_FOUND id=A07        9/10    exit=1
  A-r9-anchor-missing        chain     DRIFT CHAIN_ANCHOR_NOT_FOUND hop=2      5/7     exit=1
  B-r9-rejection-missing-flip sweeps   DRIFT SWEEP_REJECTION_INCOMPLETE id=R2 missing=flip  2/3 exit=1
  B-r9-false-sweep           sweeps    DRIFT SWEEP_CLAIM_FALSE id=SW1 hits=3   0/1     exit=1
  C-r9-dangling-ref          integrity DRIFT REF_UNRESOLVED kind=claim id=C9 chain row=1 from  refs=15 resolved=13 unresolved=1 exit=1
  C-r9-structure-break       structure DRIFT NO_QUESTION crit                 findings=1 exit=1
  each: sections=5 run=5 absent=0 drift-sections=1 findings=1 drift=1 · other four sections CLEAN
  companion direct: verify-claims A-r9-span-not-found.claims.jsonl → 9/10 DRIFT exit=1
  controls shas: 5dedb73b… · 0edb78ee… · e3490cf4… · b0d488aa… · 69b7b08f… · b24be0f0… · 21d77e6c…

Exempt audit: 6/6 items justified by source bytes, 0 findings (verbatim above).
Holds re-run in this window: selftest PASS (85 cases) · GATE_DRIFT: none · claims-r2 17/17 ·
  claims-r9 10/10 · chain-r3 17/22 · r1 observable 3/3 · gate sha 46f5ddb3… unchanged.
[[LEDGER]] LANDED: corpus/knowledge/hardening-r10.md (`f5dc8889…`, 30317 B) — 68 rows
  (38 by-design · 22 carried · 3 closed · 1 finding · 4 operator) + 27-item queue; this
  seat's completeness check found 3 carried residual classes (in-root hardlink bypass,
  no source size cap, cosmetic banner) without rows while §3.9 claims completeness →
  finding, ledger-side (part 3 above).
```

**Named limits.** The audit's scope limit: it justifies exactly the archive
records' 6 exemptions; the r3 general limit stands (an exemption is the
author's declaration — the mode cannot check that a DIFFERENT exemption is
truthful). The `A-r9.md:50` (row C3) pointer-line defect persists at `338918fc…`
(pointer :76, span occurs at A:86 — re-verified; `claims-r9.jsonl` A11 pins
:86; invisible to every gate mode; a patch moves the record sha and requires
re-measuring); the ledger dispositions it as its single `finding` row 53.
**New this round — the ledger-completeness finding** (report part 3): three
carried residuals (in-root hardlink bypass, no source size cap, cosmetic
banner `research-gate-r1`), named in the r2–r8 notes and the lesson, have no
row in `hardening-r10.md` §3.1–§3.9 while §3.9 (`:306-313`) claims item-by-item
completeness; ledger-side, note-writer's file, reported not fixed. [PARENT: +
the ledger's ⊕ rows and queue as landed.]

**Admission.** [PARENT: ADMIT/REJECT line + commit hashes; no scalar; axis
verdicts live in SCORECARD.md's round-10 sections.]

**Debt.** Receipt identity (round 1) STILL OPEN — no authentic queue
taskKey/expected receipt bag exists; mission acceptance is integrator-owned,
no `task_…` value was invented, proven receipt-backed completed rounds remain
0, operator target unchanged (≥100). Controls landed 05:41Z and were measured
(part 1) — no controls gap. New: the ledger-completeness finding (three
carried residual rows missing from `hardening-r10.md` §3, reported above,
note-writer's file). Carried debts: absent!=drift omission limit (r6); non-vacuous flip
screening (r5); id-shape boundary (r7); manifest schema growth; nested
execution cost; non-author spot-check (integrator/operator); usage/outside-path
pin blind spot (r8); masked-set blind spots (r8); re-pin policy (r8); carried
residuals (in-root hardlinks, no source size cap, token-aligned shortening,
non-ASCII-adjacent fail-closed edges, scope-refusal finding IDs, frozen-replay
comparator); r9 carries (record claims-table `span` outside every gate check;
`path#quote:text` structure quirk; reframing residual; `A-r9.md:50`
pointer-line defect). Artifacts as landed (uncommitted, shas this seat
re-computed): controls `corpus/fixtures/archives-r9/controls/` — 5dedb73b…
(span-not-found.md), 0edb78ee… (its claims copy), e3490cf4… (anchor-missing),
b0d488aa… (rejection-missing-flip), 69b7b08f… (false-sweep), b24be0f0…
(dangling-ref), 21d77e6c… (structure-break), README `23f47722…`; note
`corpus/knowledge/hardening-r10.md` `f5dc8889…` (30317 B); lesson
`corpus/lessons/2026-10-16-archive-scale-controls-and-ledger.md` `92656ca2…`.
[PARENT: integrate only what lands — receipts (receipts-writer), `SKILL.md`
rows (skill-row-updater), `corpus/README.md` row (corpus-readme-updater) were
not observed landed at this seat's last check; record sha256 for each]. Lane
hygiene: no commits by seats.