# chousa — round 86: plan and amendments

L1 `ChousaR86`. Base `3bfb6885958ad4a674ad1896f70d1e836be609e4`. The frozen claims are in
`corpus/evidence/round86/claims.json` (machine form) and `corpus/evidence/round86/claims.md` (prose); this file records
the pre-freeze repairs and any post-freeze amendment the round needs. A `narrowing` cell in
`.ufo/waves/round-86/claim-falsification.tsv` resolves to a section here.

## Claim selection

- **C1 — operability (the lowest scored non-retired axis, historical 3/10).** It closes round-85 routed defect 3 and
  the round-85 critic/mutation findings: the battery had no forgery for the 200-only class, so the repaired REFETCH rule
  was witnessed only by a fixture beside the predicate, and mutant `M17-refetch-http-2xx-accepted` survived every leg.
  Round 86 moves the class *inside* the predicate (a 203-body admit built from the committed `S021` refetch row) and
  computes the mutant from the subject tool's bytes.
- **C2 — calibration.** It closes round-85 routed defect 1 (the `S024`/`S031` supersession inversion, and the two
  warrant cells that state a distinction their cited quotes refuse) plus round-85 routed defect 4's retraction duty
  (lesson correction). The axis is calibration because the repaired defects are the lane's own self-assessment of what
  is mined and what a quote entails.
- Rejected as claims this round: a new knowledge entry (the one candidate source fetched for it, `S217` DCMI Namespace
  Policy, served a stub — recorded `rejected`), and the twelve r80 backlog Gate ids (no new instrument; carried debt).

## Pre-freeze repairs (before the first scored run, disclosed)

1. **`curation-r86.py` supersession predicate narrowed to the live-vs-unadopted form.** The first bytes counted every
   edge whose target row was `mined` (5 on this tree: `S024`, `S070`, `S171`, `S196`, `S197`), which would have failed
   legitimate legacy two-row histories (`S073`/`S176`/`S200`/`S201` are themselves `mined`). The routed defect is the
   inversion where the superseded row is the live citation and the correction is unadopted; the counter now counts that
   (1 at base). No scored run used the earlier bytes.
2. **`curation-r86.py` case bug in `MODIFIED_DEF_CITED`.** The first bytes compared the lowercase definition string
   against the quote's original case and printed 0 on a tree that carries the quote; found while building the candidate
   in scratch (`/fast/scratch/hyaku/chousa-r86/l1/cand`), before the freeze and before any scored run. Fixed to compare
   lowercased; the counter's sha is pinned in `instrument-pins.txt` at the freeze.
3. **`gate-records-r86.py` D1 builder derives its quote from the capture**, not from a quoted literal, so no forgery
   text is hard-coded in the counter. The mutant leg derives `M17` by replacing `r[6] == "200"` with
   `r[6].startswith("2")` in the subject tool's own bytes and refuses to score a mutant that the subject bytes did not
   yield.

## Freeze

`corpus/evidence/round86/claims.md`, `claims.json`, both counters, `c2-positives.tsv`, the three control receipts and
`instrument-pins.txt` are committed together as the freeze, before the landing commit and before any scored run. The
subject tool `tools/gate-records.py` is not modified this round.

## Amendments after the freeze

None yet. An amendment is written here only when a wave artifact falsifies a claim's stated wording (addendum §8,
Amendment 59), and it names the artifact, the narrower property that may verify, or the honest stop.

## Amendment 11 — C2 narrowed to the property the instrument enforces (wave artifacts `R86ReviewerEntry`, `R86CriticClaims`)

**Findings (post-freeze, from the round's own wave).**

1. `R86ReviewerEntry` §2.3 and `R86CriticClaims` control (2) V4: `claims.md` publishes the C2 predicate as
   "`QUOTES_LOCATED` equal to its total **with the total ≥ 19**", but the counter's `pred()` is
   `quotes_total > 0 and quotes_located == quotes_total` — no floor. A tree carrying 15 quote rows prints
   `QUOTES_LOCATED=15/15` and `PASS`. The published predicate therefore contained a conjunct the instrument never
   implemented.
2. `R86ReviewerEntry` §2.4 (E6): `MODIFIED_DEF_CITED` is a *presence* test ("some located quote of the entry contains
   the definition"), not the warrant linkage the sentence names ("the round-84 row 9 gains the `modified` Definition
   quote … as its warrant"). Re-pointing row 9's warrant to `Q10` while leaving `Q13` in place still prints `1`.
3. `R86ReviewerEntry` §2.1/§2.2 (E3, E4): the `UNENTAILED_TERM` check is a two-word substring test. It is satisfied by
   deleting the word (E3), and it scores the *round-85* defect bytes verbatim as a pass when the imported nouns are
   `primary`/`tool`/`version`/`step` (E4). The frozen sentence names only the two words, and on those two words it is
   literally true — but the parenthetical rationale ("the round-85 routed defect 1: an imported distinction the cited
   source refuses") names a class no byte of the instrument measures.

**Narrowed C2 (the claim that may verify).** `CURATION_R86=PASS` with `SUPERSEDED_LIVE=0`, `UNENTAILED_TERM=0` over the
frozen term set `{modification, modified}`, `MODIFIED_DEF_CITED=1` (presence of the `S023` `modified` Definition among
the entry's located quotes), and `QUOTES_LOCATED` equal to its total. The published floor `total ≥ 19` is **withdrawn
as a predicate conjunct** because the instrument never enforced it; the measured total at landing is 20/20, so the
withdrawn floor's intent holds on the bytes and is reported as a measured value, not as an enforced one.

**What the narrowing moves from counted to reviewed.** (a) The class-level closure of the imported-distinction defect
is **review-verified, not counted**: `R86ReviewerEntry` §1 re-read both repaired rows against their located quotes
(`Q13` at S023 capture line 8786, `Q7` at S031 capture line 211) and both hold; the entry-wide term counts at landing
are `primary`/`tool`/`version`/`step` = 0. (b) The warrant linkage of the r84 row 9 is review-verified by reading the
row, not by the counter. (c) The entry-deletion gaming path (delete the failing quote row and the denominator shrinks)
is named as routed debt for round 87: implement the floor (`quotes_total >= 19`, per-entry minima) and a
warrant-linkage leg (the repaired row's `Warrant` cell must name a `qid` whose quote carries the distinguishing term).

**Not narrowed:** (i) the S024/S031 inversion repair — `SUPERSEDED_LIVE=0` at landing, 1 at base, reproduced by three
seats; (ii) the two repaired cells' verified entailment. `R86CriticClaims` V1 (S024 re-mined *and* re-credited to the
same entry as S031) still passes `SUPERSEDED_LIVE=0`; that is the disclosed consequence of the pre-freeze narrowing
(plan §Pre-freeze repairs 1), not a new relaxation, and it is routed to round 87 as "the live citation is the
superseding row's `used-by`, not the superseded row's".

## Amendment 12 — C1's residuals routed, not narrowed (wave artifacts `R86CriticClaims`, `R86MutCounter`, `R86ExecForge`)

C1's sentence is about the landing subject tool and the derived mutant, and every clause of it held under attack
(`R86ReviewerClaims` clause table; `R86ExecRepro`, `R86ExecBase`, `R86ExecHarm`, `R86ExecForge` all held). Three
residuals are routed as next battery's work rather than treated as a narrowing:

1. **D1 is one record wide where the committed bytes support three.** `R86CriticClaims` T4 — a tool whose rule is
   `r[6] == "200" if sid == "S021" else 2xx` — prints `D1_FORGES=1 D1_REFUSED=1/1 MUT17_KILLED=1/1` and exits 0.
   `build_d1_203_admit` returns the first qualifying row; `S021`, `S032` and `S022` all have `curl_rc=0`, `http=203`
   and a matching stored sha. Round 87 builds D1 from every qualifying row and requires `D1_REFUSED=N/N`.
2. **Derivation and SETUP duties are fields, not verdict conjuncts.** `R86MutCounter` M2 (mutant credited without a
   run) and M5 (`SETUP` dropped from `passed`) survive `GATE_RECORDS_R86=PASS`; the landed line still prints
   `MUT17_KILLED=0/1`/`SETUP=0/1` on the probes, so the fields tell and the verdict does not. The predicate in
   `claims.md` enumerates every field, which is why the landing line is the predicate; the counter still needs a leg
   that fails when its own duty is dropped. Routed.
3. **A rejection-form 203 record is accepted** (`R86ExecForge` F1: `decision=reject capture=none curl_rc=0 http=203`
   → `OK`, 3/3 committed 203 rows). The frozen D1 class is an **admit** over a stored 203 body, and no in-class admit
   is accepted (F4), so K2 does not fire; the acceptance is the honest record of a rejected attempt and is reported as
   a boundary, not a breach.
