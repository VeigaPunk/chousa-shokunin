# R87ReviewerC2 — C2 (`C2-CURATION-R87`) wording attack

Seat `R87ReviewerC2`. Leaf. No network, no production edits, no git/jj mutation. Landed bytes attacked:
`e6e920a4e6988287c31e89b3e920a118b569ae52`. Base for the floor re-derivation: `6495ef88`. Frozen claims read first:
`corpus/evidence/round87/claims.md`; pre-freeze repairs: `plans/round-87.md`.
Instrument under attack: `corpus/evidence/round87/curation-r87.py`.

Scratch: `/fast/scratch/hyaku/chousa-r87/R87ReviewerC2/` (two `git archive` trees: landed `tmp.q7hDgLZ2SR`,
base `tmp.FlQkcsYpAH`; every mirror is `shutil.copytree(..., symlinks=True)` of the landed tree).
Receipts: `.ufo/waves/round-87/w1/R87ReviewerC2/receipts/`.

No tool was installed or upgraded this round.

---

## Baseline: the predicate does hold

**Command** (`claims.md` §C2 counting command, tree from `git archive e6e920a4`);
**receipt** `receipts/r01-landed-run.txt`; **exit 0**.

```
SUPERSEDED_LIVE=0 UNENTAILED_TERM=0 MODIFIED_DEF_CITED=1 QUOTES_LOCATED=20/20 Q_FLOORS=search-transparency-reporting-r84.md=13/13 floor13,provenance-recording-r85.md=7/7 floor7 WARRANT_OK=17/17 TEACHES_CHECKED=1 TEACHES_FLAGGED=1 TEACHES_UNRESOLVED=0 LEGS=7/7
TEACHES_FLAGGED S024 terms=publication,modification disposition=superseded by S031
CURATION_R87=PASS
```

The seven legs are each appended exactly once (`FLOOR, SUPERSEDED, UNENTAILED, DEF_CITED, WARRANT, TEACHES, SETUP`)
and `passed = len(legs) == EXPECTED_LEGS and all(ok)` (`curation-r87.py:247`), so K1 is met and the leg-account
repair holds. K3 holds independently: `receipts/r09-controls-at-landing.txt`, exit 0,
`FORGERY_REFUSED=4/4 R86_ACCEPTED_FORGERY=4/4`, `CONTROLS=PASS`.
K2 holds independently of the counter's own claim: `receipts/r03-independent-verbatim-location.txt`, exit 0,
`INDEPENDENT_QUOTES_LOCATED=20/20 misses=[]` (own `norm()` + `sha256(url)[:24]` capture lookup, no import of the
counter).

---

## F1 — the warrant clause is false as written at landing (no mutation needed)

**Claim sentence.** "a warrant-linkage leg requiring each decision-table row's named qid to resolve to a located
quote that shares a distinctive content word with the row's own cells".

**Code.** `curation-r87.py:185-193`: `resolved` is per-qid (`len(resolved) == len(qids)`), but `shares` is a single
row-level disjunction over all resolved quotes (`shares = any(... for q in resolved)`). So resolution is demanded of
every named qid; **word-sharing is demanded of only one of them**.

**Native counterexample at `e6e920a4`** — `receipts/r05-native-warrant-multi-qid.txt`, exit 0:

```
provenance-recording-r85.md row='Naming what a resource derives from' qids=['Q1', 'Q3'] shared={'Q1': ['entities', 'property', 'provenance'], 'Q3': []} qids_with_no_shared_word=['Q3']
```

Q3 ("then we can say that the bar chart prov:wasDerivedFrom the dataset.") shares no 5+ letter non-stopword with
the row's Do/Never cells, yet the row is one of `WARRANT_OK=17/17` (`receipts/r01-landed-run.txt`). Under the
sentence's per-qid reading the leg is already unsatisfied at landing; under a row-level reading the sentence is
merely under-specified.

**And the row-level reading is cheaply satisfiable by an incidental word** —
`receipts/r04-warrant-cheap-row.txt`, exit 0, `WARRANT_OK=17/17`, `CURATION_R87=PASS`. The forged row keeps the
shared token `validity` and replaces the entailed Never cell with a proposition Q11 does not state:

```
| Recording when a resource is valid | state the date or range of validity of the resource | ignore the validity of any resource that is a database, and prefer a machine-readable schema over prose | Q11 (S023) |
```

So "shares a distinctive content word" does not mean "is entailed by": one 5-letter token that survives
`STOPWORDS` (`curation-r87.py:50-54,114-120`) buys the leg. The sentence's word *distinctive* promises more
discrimination than one incidental token.

**Second scope gap in the same clause:** "the row's own cells" is `cells[1], cells[2]` only (`:188`) — the
`Situation` cell (`cells[0]`) is never read for sharing.

No kill rule covers this: K2 is about verbatim location, K3 about the four controls, K4 about the TEACHES
detector. The defect is in what the sentence says the leg verifies.

---

## F2 — TEACHES disposition accepts a `rejected` superseder

**Claim sentence.** "requires every flagged row to be disposed as superseded".

**Code.** `curation-r87.py:136-145,206-219`: `superseded_by` is populated from any row whose `teaches` matches
`supersedes (S\d{3,}) —`, with **no status predicate**; `:218` disposes a flagged row whenever `sid in superseded_by`.
`status` is `cells[7]`, already parsed and used at `:144` for the SUPERSEDED leg — it is simply not consulted here.

**Live registry fact (landing):** `S202` has `status=rejected` and `teaches` `supersedes S198 — REJECTED: …`;
`S198` itself is `status=rejected`.

**Run**, `receipts/r06-teaches-rejected-superseder.txt`, exit 0 (`S198`'s `teaches` gains "separate from
modification dates"; its URL is a repo-relative path, so `capture_text` returns `None` and every date term misses):

```
TEACHES_FLAGGED S198 terms=modification disposition=superseded by S202
SUPERSEDED_LIVE=0 … TEACHES_CHECKED=2 TEACHES_FLAGGED=2 TEACHES_UNRESOLVED=0 LEGS=7/7
CURATION_R87=PASS
```

**Does "disposed as superseded" hold?** Mechanically yes — the counter prints a named disposition and
`TEACHES_UNRESOLVED=0`. Substantively no: the contract the leg cites (S218 → `corpus/QUALITY.md` 178 /
`CORPUS.md` rule 2: "the superseding row's `teaches` is the evidence") is unmet when the superseder is itself
`rejected`, because a rejected row's `teaches` is not evidence either. The leg therefore disposes a flagged row on
a superseder that carries no evidentiary weight. The same hole exists for `queued` superseders (`S030→S022`,
`S032→S021` are `queued`). At landing no flagged row is S198, so the hole is latent, but it is reachable and the
corpus already contains the shape. K4 ("at least one flagged row and a named disposition") is satisfied by exactly
this path, so K4 does not catch it.

---

## (a) The 13/7 floors — claim accurate; the counts are rows, and rows == distinct at base

**Command** (section/table re-derivation over both trees); **receipt** `receipts/r02-base-floors.txt`, exit 0:

```
base-6495ef88     search-transparency-reporting-r84.md quote_rows=13 distinct_quote_texts=13 decision_rows=11
base-6495ef88     provenance-recording-r85.md          quote_rows=7  distinct_quote_texts=7  decision_rows=6
landing-e6e920a4  search-transparency-reporting-r84.md quote_rows=13 distinct_quote_texts=13 decision_rows=11
landing-e6e920a4  provenance-recording-r85.md          quote_rows=7  distinct_quote_texts=7  decision_rows=6
```

The counter counts **rows**: `total += 1` and `located += 1` per accepted row (`:171-175`), and `FLOOR` is
`loc >= fl and loc == tot` (`:199`). At the base revision rows and distinct quote texts coincide (13/13, 7/7), so
"the measured base counts" is true under either reading — the parenthetical does not misstate what the floor is.
Decision-row totals re-derive to **17** (11 + 6), matching `WARRANT_OK=17/17`.

**Residual, not an overstatement:** because the floor is a row count, a *duplicated* quote row inflates it instead
of failing — `receipts/r08-floor-counts-rows.txt`, exit 0, `Q_FLOORS=… provenance-recording-r85.md=8/8 floor7`,
`CURATION_R87=PASS` (Q7's text re-added as Q8). The claim promises only that "a deleted or truncated quote table
fails", which it does (`E5b` 6/6 floor7, `E5c2` 1/1 floor13, `receipts/r09-controls-at-landing.txt`), so this is a
documented-direction limit, not a falsification.

---

## (d) `UNENTAILED_TERM` — the claim does not overstate it; the printed line invites over-reading

The C2 sentence never mentions `UNENTAILED_TERM`; it is a carried leg whose value appears in the predicate line. So
the *claim* is silent, not overstated. Its width is nonetheless exactly two words over two entries:
`DEFECT_TERMS = ("modification", "modified")` (`:46`), aggregated **per entry** (`joined` over all of an entry's
located quotes, `:179-183`), and read only from `cells[1], cells[2]`.

**Run** — `receipts/r07-unentailed-width.txt`, exit 0 per probe:

```
A-other-vocabulary: rc=0 UNENTAILED_TERM=0 verdict=CURATION_R87=PASS
B2-entry-join:      rc=0 UNENTAILED_TERM=0 WARRANT=WARRANT_OK=17/17 verdict=CURATION_R87=PASS
D-situation-cell:   rc=0 UNENTAILED_TERM=0 WARRANT=WARRANT_OK=17/17 verdict=CURATION_R87=PASS
```

- **A**: the same defect asserted in other vocabulary ("record a deletion or removal of a resource without saying
  when it happened") does not fire — the term set is two literal words.
- **B2**: a row whose Never cell says "without a modified date" and whose own warrant is `Q11` passes, because a
  *different* quote of the same entry (`Q14`, "modified Property") puts the token in `joined`. Aggregation is
  entry-wide, so a row's own warrant need carry nothing.
- **D**: the `Situation` cell is unscanned.

This is a scope note against the PASS line, not a claim falsification. It becomes a claim defect only if the frozen
sentence is read as covering the carried leg.

---

## Residual risk and verification gaps

1. **Warrant, non-entailment:** the leg certifies vocabulary overlap, not entailment (F1, r04). Any future claim
   that the warrant leg "checks the row is supported" would be false. A per-qid sharing requirement plus the
   `Situation` cell would close the gap the sentence already implies.
2. **TEACHES superseder status (F2):** the fix is a status predicate on the superseder (`cells[7] in
   ("mined", …)`) — the field is already parsed one leg up.
3. **`teaches_checked` is 1 at landing.** The TEACHES leg's liveness rests on a single live row (`S024`). Not a
   defect, but the detector has one positive instance corpus-wide; a change to `S024`'s teaching text would take the
   leg to `teaches_checked=0` and FAIL — correct, but brittle in the sense that the detector's coverage is n=1.
4. **Not checked here** (out of seat scope, left to the other seats): whether `QUOTES_LOCATED` per-entry floors were
   chosen from the base revision rather than the landing revision in a way that hides a landing-time quote loss —
   they coincide at both revisions (r02), so no gap observed.
5. **Gap:** no run measures whether a quote located in capture *A* may warrant a row whose cited source is *B*. The
   code keys quotes per entry, not per source, so a row citing `Q1 (S214)` passes on any located quote. Not
   demonstrated with a run; recorded as an unexercised question, not a finding.

---

VERDICT: R87ReviewerC2 C2 fired — the predicate prints PASS honestly (r01, r09, r03), but the frozen sentence
overstates the warrant leg (Q3 shares no distinctive word yet counts OK at landing, F1) and reads "disposed as
superseded" over a `rejected` superseder (F2).
