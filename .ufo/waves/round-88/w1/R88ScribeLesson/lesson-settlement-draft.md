# Round 88 — settlement paragraph the L1 pastes after WAVE-DONE (DRAFT)

> **DRAFT — do not paste until the integration commit lands and the wave's results file exists.**
> Author: seat `R88ScribeLesson` (scribe; leaf member — no subagent dispatch, no production edit, no lane/fleet
> git mutation, no network). Sources read: the eleven wave seat reports present in
> `.ufo/waves/round-88/w1/` at the time of writing — `R88ExecRepro.md`, `R88ExecHarm.md`, `R88ExecForge.md`,
> `R88ExecC2Forge.md`, `R88MutCounter/R88MutCounter.md`, `R88ReviewerC1.md`, `R88ReviewerC2.md`,
> `R88CriticClaims/R88CriticClaims.md`, `R88SentinelScope.md`, `R88ScoutRegistry/R88ScoutRegistry.md`,
> `R88ConnectorSiblings.md` — plus the frozen predicate set `corpus/evidence/round88/claims.md`,
> `plans/round-88.md`, the freeze revision `4ea9d008abfd2e09cb51649a42678a78f52ac530`, and this seat's receipts
> under `.ufo/waves/round-88/w1/R88ScribeLesson/receipts/`.
>
> **No L1 draft lesson exists yet.** `corpus/lessons/round-88.md` is absent from the tree at `4ea9d008` and
> `git status --porcelain` shows only the untracked `.ufo/waves/round-88/` wave folder — so everything below is
> drafted against committed bytes and the wave's own reports, and every sentence naming a lesson line, a
> `## Mistakes` row or a `## Corrections` row must be re-checked against the L1's draft before it is pasted.

## Seat tally

**Fired (3 seats, 5 verdict lines):**

| seat | claim | what fired |
|---|---|---|
| `R88ReviewerC1` | C1 | K4 — the `RECONCILED` conjunct is tautological for the three non-`n/m` legs, so a detached `MUT_ADMIT` `ok` and a credited-but-unbuilt mutant both print `GATE_RECORDS_R88=PASS` (exit 0) |
| `R88CriticClaims` | C1 | K4 — the width, mutant and `TOOL` legs detached from their measurements survive together with `GATE_RECORDS_R88=PASS` (exit 0) |
| `R88CriticClaims` | C2 | K4 — `curation-r88.py` has no verdict-vs-field reconciliation, so a dead `TEACHES` detector and a detached `ok` both print `CURATION_R88=PASS` (exit 0) |
| `R88ExecC2Forge` | C2 | five in-class forgeries accepted green (duplicate-qid cite, quote-content swap under pinned qids, row reorder, ≥7-token verbatim substitutions) |
| `R88ScoutRegistry` | C2 | the claim's "superseding row's own `teaches` reads in its own capture" clause is dead code (`curation-r88.py:250`, case-mismatched regex over a lowercased cell) |

**Held (8 seats, 16 verdict lines):** `R88ExecRepro` (C1, C2), `R88ExecHarm` (C1), `R88ExecForge` (C1),
`R88MutCounter` (C1, C2), `R88ReviewerC2` (C2), `R88SentinelScope` (C1, C2), `R88ConnectorSiblings` (C1, C2),
and `R88ScoutRegistry`'s second line (C2 `n/a`, the campaign-package collision reported without a verdict).

**No verdict line at all:** `R88ExecForge.md` (the seat report names no `VERDICT:` line; its content — 28 probes,
zero accepted forgeries, the single acceptance being a correct acceptance of a genuine committed row — reads as
C1 held). The tally above counts it as held on content and records the missing trailer as a finding.

Evidence: every `VERDICT` line verbatim is in `.ufo/waves/round-88/w1/R88ScribeLesson/receipts/r17-verdicts-read.txt`.

## The paragraph to paste

> Round 88's wave fired both claims and held their printed predicates. C1 fired on two seats: `R88ReviewerC1` showed
> that the verdict's `RECONCILED` conjunct is tautological for the three legs whose detail carries no `n/m` ratio, so a
> `MUT_ADMIT` leg whose `ok` is detached from its measurement — and a mutant credited without being built — both
> print `GATE_RECORDS_R88=PASS` at exit 0
> (`.ufo/waves/round-88/w1/R88ReviewerC1-receipts/e4-m2-mutadmit-detached.txt`,
> `…/e4-m3-mutadmit-neverbuilt.txt`, with the contradicting leg receipts `…/e4-m2-leg-MUT_ADMIT.txt` =
> `MUT_ADMIT=ok detail=derived=1 killed=0` and `…/e4-m3-leg-MUT_ADMIT.txt` = `MUT_ADMIT=ok detail=derived=0 killed=0`),
> and `R88CriticClaims` showed the same class surviving with the width and `TOOL` legs detached as well
> (`.ufo/waves/round-88/w1/R88CriticClaims/receipts/e7c-width-detached.log`, `…/e7b-mutant-detached.log`,
> `…/combined-width-mutant-detached.log`, whose own leg receipts read `D1_WIDTH=ok detail=3/3/1 pin3` and
> `MUT_ADMIT=ok detail=derived=0 killed=0`); the frozen predicate itself still prints
> `TOOL=present POSITIVE=15/15 … D1_EXPECTED=3 D1_FORGES=3 D1_REFUSED=3/3 D2_FORGES=3 D2_REFUSED=3/3
> MUT_ADMIT_KILLED=1 MUT_UNREACH_KILLED=1 DERIVE_NEG=1 LEGS=15/15` and `LEG_REREAD=15/15 RECONCILED=15/15
> LEGS_APPENDED=15` / `GATE_RECORDS_R88=PASS` at exit 0, so the firing is against the sentence's wording that a
> detached `ok` "fails the predicate instead of passing on printed fields" and is discharged by a per-format
> reconciliation, not by a narrowing. C2 fired on three seats: `R88ExecC2Forge` showed five in-class forgeries
> accepted green — a duplicate qid cite (`Q1, Q1 (S215)`), a quote-content swap under pinned qids, a reordered quote
> table, and two ≥7-token verbatim substitutions
> (`.ufo/waves/round-88/w1/R88ExecC2Forge/receipts/run1.log`, `…/run2b.log`); `R88CriticClaims` showed the counter
> printing `CURATION_R88=PASS` over its own honestly-printed failures — a dead `TEACHES` detector prints
> `TEACHES_FLAGGED=0 … LEGS=7/7 CURATION_R88=PASS` and a detached `ok` prints `TEACHES_UNRESOLVED=1 … LEGS=7/7
> CURATION_R88=PASS`
> (`.ufo/waves/round-88/w1/R88CriticClaims/receipts/c2-dead-teaches.log`, `…/c2-detached-teaches.log`,
> `…/c2-constants-on-broken.log`); and `R88ScoutRegistry` showed the claim's stated "superseding row's own `teaches`
> reads in its own capture" requirement is dead code at `curation-r88.py:250` — the regex
> `supersedes (S\d{3,}) —` is matched against a lowercased cell and therefore never matches (10 raw-cell matches,
> 0 lowercased matches over 218 rows; a one-character-fixed counter refuses a tree the shipped one accepts)
> (`.ufo/waves/round-88/w1/R88ScoutRegistry/receipt-supclause-dead.txt`, `…/receipt-probe-run.txt`); the frozen
> predicate itself still prints `SUPERSEDED_LIVE=0 UNENTAILED_TERM=0 MODIFIED_DEF_CITED=1 QUOTES_LOCATED=20/20
> … WARRANT_OK=17/17 TEACHES_CHECKED=1 TEACHES_FLAGGED=1 TEACHES_UNRESOLVED=0 LEGS=7/7` / `CURATION_R88=PASS` at
> exit 0 and refuses all five round-87 forgeries (`FORGERY_REFUSED=5/5 R87_ACCEPTED_FORGERY=5/5`), so the firing is
> against the sentence's wording and against the counter's dead clause, and is discharged by a per-format
> reconciliation plus a live superseder-own-read check.

## Per-fired-claim line (one sentence each, seat + receipt path)

- **C1 — `R88ReviewerC1`** — the verdict's reconciliation is tautological for the three non-`n/m` legs, so a detached
  `MUT_ADMIT` `ok` (`MUT_ADMIT_KILLED=0`) and a credited-but-unbuilt mutant (`MUT_ADMIT_DERIVED=0 MUT_ADMIT_KILLED=0`)
  both print `GATE_RECORDS_R88=PASS` at exit 0 — `.ufo/waves/round-88/w1/R88ReviewerC1-receipts/e4-m2-mutadmit-detached.txt`,
  `.ufo/waves/round-88/w1/R88ReviewerC1-receipts/e4-m3-mutadmit-neverbuilt.txt`.
- **C1 — `R88CriticClaims`** — the width, mutant and `TOOL` legs detached from their measurements survive together
  (`D1_WIDTH=ok detail=3/3/1 pin3`, `MUT_ADMIT=ok detail=derived=0 killed=0`) with the full frozen line and
  `GATE_RECORDS_R88=PASS` at exit 0 — `.ufo/waves/round-88/w1/R88CriticClaims/receipts/combined-width-mutant-detached.log`,
  `.ufo/waves/round-88/w1/R88CriticClaims/receipts/e7c-width-detached.log`,
  `.ufo/waves/round-88/w1/R88CriticClaims/receipts/e7b-mutant-detached.log`.
- **C2 — `R88ExecC2Forge`** — five in-class forgeries pass the counter green: a duplicate qid cite (`Q1, Q1 (S215)`),
  a reordered quote table, an 8-token verbatim substitution on `Q1` and on `Q2`, and a quote-content swap under pinned
  qids — `.ufo/waves/round-88/w1/R88ExecC2Forge/receipts/run1.log`,
  `.ufo/waves/round-88/w1/R88ExecC2Forge/receipts/run2b.log`.
- **C2 — `R88CriticClaims`** — `curation-r88.py` has no verdict-vs-field reconciliation: a dead `TEACHES` detector
  prints `TEACHES_FLAGGED=0 … CURATION_R88=PASS` and a detached `ok` prints `TEACHES_UNRESOLVED=1 LEGS=7/7
  CURATION_R88=PASS`, both at exit 0 — `.ufo/waves/round-88/w1/R88CriticClaims/receipts/c2-dead-teaches.log`,
  `.ufo/waves/round-88/w1/R88CriticClaims/receipts/c2-detached-teaches.log`,
  `.ufo/waves/round-88/w1/R88CriticClaims/receipts/c2-constants-on-broken.log`.
- **C2 — `R88ScoutRegistry`** — the claim's "superseding row's own `teaches` reads in its own capture" clause is
  unreachable (`curation-r88.py:250` matches `supersedes (S\d{3,}) —` against a lowercased cell: 10 raw-cell matches,
  0 lowercased over 218 rows) — `.ufo/waves/round-88/w1/R88ScoutRegistry/receipt-supclause-dead.txt`,
  `.ufo/waves/round-88/w1/R88ScoutRegistry/receipt-probe-run.txt`.

## Pre-conditions before this paragraph may be pasted

Each is a finding in `.ufo/waves/round-88/w1/R88ScribeLesson.md`; each must be discharged by the integration commit,
or the paragraph above must be rewritten to drop the referent.

1. Land the plan's amendments for the three fired claims (the `RECONCILED` per-format reconciliation, the C2
   verdict-vs-field reconciliation, the live superseder-own-read clause) or state the honest stop — this seat's
   recommendation is that all three are *repairs*, not narrowings: each restores the property the frozen sentence
   already claims.
2. Land a `## Corrections` row in the round-88 lesson carrying the **real** mined-criteria split. The round-87
   spot-check's own sentence says "three/four/three" (summing to 10) while the criteria count is 8
   (`grep -cE '^18[2-9]\. ' corpus/QUALITY.md` → 8); the plan's "three / two / three" is the sum that matches.
   Receipt `r15-criteria-split-arithmetic.txt`.
3. Correct the SCORECARD's round-87 header seat count (13 → 12) and the two stale "five criteria mined
   (QUALITY 182–186)" sentences in `corpus/lessons/round-87.md:172` and `SCORECARD.md:3941` and `:3949`.
   Receipt `r12-routed-defects-and-plan-mismatch.txt`.
4. Land the lesson's `## Gate` block. Round 88 owes **one** `GATE-RECORD` line — `S218` in the `rev` form — and no
   `url` line (round 88 fetched nothing and opened no registry row). The verified candidate, its
   `tools/gate-records.py verify` result, the grounding-counter result and the harm count at that lesson are in
   receipts `r09`, `r10`, `r11`; the round-88 lessons count moves from 65 to 66 (receipt `r16`).
5. Amend `plans/round-88.md`'s two freeze sentences: it says the freeze commits `claims.json` and "the egress table",
   and neither file exists at `4ea9d008` (`git ls-tree 4ea9d008 corpus/evidence/round88/` lists 10 entries, no
   `claims.json`; no `egress-approval.md`). This is the sentinel's F4, and it is the plan's own text, not the claim's.
   Receipt `r12`.
6. Record in the lesson that `controls/expected.tsv`'s `c1-do-nothing` row expects exit 1 while its own committed
   receipt `controls/receipts/c1-k0-donothing.txt` prints `GATE_RECORDS_R88=PASS` — re-run here at exit 0, because
   the subject tool is byte-identical at base and freeze (sha256 `905f9da2…` both sides). The expectation row is
   unsatisfiable as written; the substance (the round-87 battery cannot bind 203) is carried by
   `c1-k0b-frozen-instrument.txt`. Receipts `r07`, `r12`.
7. Ensure `R88ExecForge`'s missing `VERDICT:` trailer is either supplied or named in the lesson's settlement
   sentence — this seat's tally counts it as C1 held on content (28 probes, zero accepted forgeries).

VERDICT: R88ScribeLesson C1 fired — the frozen battery prints the exact frozen line at `4ea9d008` with `LEG_REREAD=15/15 RECONCILED=15/15 LEGS_APPENDED=15` and `GATE_RECORDS_R88=PASS` exit 0, but two seats showed that the `RECONCILED` conjunct is tautological for the three non-`n/m` legs, so a detached `ok` and a credited-but-unbuilt mutant survive with PASS — the firing is against the sentence's "fails the predicate instead of passing on printed fields" clause and is discharged by a per-format reconciliation, not by a narrowing.
VERDICT: R88ScribeLesson C2 fired — the frozen counter prints the exact frozen line at `4ea9d008` with `CURATION_R88=PASS` exit 0 and refuses all five round-87 forgeries (`FORGERY_REFUSED=5/5`), but three seats showed five in-class forgeries accepted green, a verdict printed over honestly-printed failures, and the claim's superseder-own-read clause unreachable at `curation-r88.py:250` — the firing is against the sentence's wording and the counter's dead clause, and is discharged by a per-format reconciliation plus a live superseder-own-read check.
