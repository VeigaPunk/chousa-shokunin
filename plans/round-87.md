# chousa — round 87: plan and amendments

L1 `ChousaR87`. Base `6495ef88` (round-86 landing + the non-author spot-check at `6495ef88`, whose five routed
defects are this round's input). The frozen claims are in `corpus/evidence/round87/claims.json` (machine form) and
`corpus/evidence/round87/claims.md` (prose); this file records the pre-freeze repairs and any post-freeze amendment.
A `narrowing` cell in `.ufo/waves/round-87/claim-falsification.tsv` resolves to a section here.

## Inputs — the five defects round 86's non-author check routed

`corpus/lessons/round-86-verifier-spotcheck.md` `## Routed defects` (all five endorsed there, none re-routed):

1. **D1 is one record wide.** `build_d1_203_admit` returns the first qualifying 203 row it finds (`S021`), and the
   predicate requires `D1_REFUSED=1/1`. The critic's `T4` mutant — `r[6] == "200" if sid == "S021" else
   r[6].startswith("2")`, a general-2xx rule with a single record-keyed exception — prints the full frozen line and
   `PASS` (`.ufo/waves/round-86/w1/R86CriticClaims.md` §T4). The class the claim names is every 203 row; the class the
   instrument enforces is one row.
2. **The mutant-derivation and SETUP duties are printed fields, not verdict conjuncts.** `M2` (replace the whole
   mutant leg with `mut17 = 1`) and `M5` (drop `and setup_ok == 1` from `passed`) both print the frozen line and `PASS`
   (`.ufo/waves/round-86/w1/R86MutCounter.md` §C1).
3. **A `decision=reject` 203 record is accepted.** The `url/unreach` form's success test is
   `curl_rc == "0" and http == "200"`, so a record claiming a failed fetch while reporting `curl_rc=0 http=203` is
   accepted on every 203 row (`R86ExecForge` F1, candidates 3/6/8). A 203 is a *successful* response
   (S216: "the request was successful but the enclosed content has been modified"), so it cannot record a failed
   transfer.
4. **C2's `QUOTES_LOCATED` has no denominator floor and no warrant linkage.** `E5b` (delete the failing quote row) →
   `19/19 PASS`; `E5c2` (keep only `Q13` and `Q7`) → `2/2 PASS`; `E6` (re-point the r84 row-9 warrant at `Q10` while
   leaving `Q13` in place) → `MODIFIED_DEF_CITED=1 PASS` (`R86ReviewerEntry` §2.3/§2.4).
5. **A registry `teaches` cell is never read against its capture.** `S024`'s frozen `teaches` asserts a comparison to
   modification dates that its superseder's capture refuses (`S031` capture contains `modified`/`modification` 0 times),
   and no instrument in the lane reads registry `teaches` against captures at all (QUALITY 178).

## Claim selection

- **C1 — operability (the lowest scored non-retired axis, historical 3/10).** It closes routed defects 1–3 on the
  battery. Capability: the round-87 battery widens the 203 class to every qualifying committed row, adds the reject-form
  203 class, and accounts its verdict by counting executed legs so a dropped leg or a credited-but-unrun mutant changes
  the verdict instead of the printed fields only. The subject tool gains the unreach-form repair (a 2xx is not a failed
  transfer).
- **C2 — calibration.** It closes routed defects 4–5 on the curation instrument: an implemented per-entry quote floor, a
  warrant-linkage leg, and a registry-`teaches`-against-capture leg over every live (non-superseded) row. The axis is
  calibration because each leg is the lane's own check on whether its self-assessment of what is mined, warranted and
  located matches the bytes.
- Rejected as claims this round: a new knowledge entry (no candidate source was opened for one; the round's one new
  registry row is `own-work`, S218, which grounds C2's contract leg), and the twelve r80 backlog Gate ids (carried debt,
  no new instrument).

## Pre-freeze repairs (before the first scored run, disclosed)

1. **`build_d1_203_admits` returns every qualifying row, and the predicate pins the expected width.** The builder walks
   the committed `refetch.tsv` for every row with `curl_rc=0`, a non-200 status, a matching capture key and a capture
   whose sha equals the row's `txt_sha256` (3 at this base: `S021`, `S032`, `S022`), and `passed` requires
   `D1_FORGES == D1_EXPECTED` and `D1_REFUSED == D1_FORGES`. A counter that rebuilds the one-row class prints
   `D1_FORGES=1` and fails on the expected-width leg (this is the `T4` kill).
2. **The verdict is leg-accounted.** Every leg appends exactly one `(name, ok, detail)` record; `passed` is
   `all(ok) and len(legs) == EXPECTED_LEGS` with `EXPECTED_LEGS` a frozen constant. A leg whose body is deleted (the
   `M5` shape) or whose mutant is credited without a build (the `M2` shape) changes the leg count and fails, so the
   predicate cannot be met by a counter that stopped executing the duty.
3. **The mutant leg carries its own derivability probe.** `MUT17_DERIVED` is true only when `build_mutant` produced
   different bytes *and* the derived copy ran; a second probe feeds `build_mutant` a copy whose literal is rewritten
   (`r[6] == "2" + "00"`) and requires it to report "not derived", so the derivation duty is exercised both ways.
4. **The reject-form 203 class (D2) is built from the same committed rows** in the `url/unreach` shape
   (`decision=reject capture=none curl_rc=0 http=203`) and its expected code is `REFETCH`.
5. **`tools/gate-records.py` unreach branch: a 2xx status is not a failed transfer.** `success = curl_rc == "0" and
   http == "200"` becomes `curl_rc == "0" and 200 <= int(http) < 300`. Harm control: the only genuine committed unreach
   record in the tree is `corpus/lessons/round-81.md:28` (S208, `curl_rc=22 http=403`), and it still verifies OK
   (`controls/receipts/c1-harm-unreach.txt`); no committed record of either url form moves.
6. **`curation-r87.py` per-entry floors are the measured base counts** (r84 entry 13 located quotes, r85 entry 7), not a
   round-sum minimum: `E5c2` keeps 2 across both entries and fails both floors, where a round-sum floor of 2 would pass.
7. **The `teaches` leg skips superseded rows by contract, not by name.** A row whose id appears as the target of
   another row's `teaches` `supersedes S0NN —` prefix is not live (CORPUS rule 2 / QUALITY 178: the superseding row's
   `teaches` is the evidence), so the leg reads only live rows and requires 0 rows whose `teaches` names a
   date-property term their own capture does not contain. `S024` is therefore neither edited nor counted.

## Freeze

`corpus/evidence/round87/claims.md`, `claims.json`, both counters, the control batteries, their receipts, the egress
table and `instrument-pins.txt` are committed together as the freeze, before the landing commit and before any scored
run of the candidate bytes.

## Amendments after the freeze

None yet. An amendment is written here only when a wave artifact falsifies a claim's stated wording (addendum §8,
Amendment 59) and names the artifact plus the narrower property that may verify, or the honest stop.

## Amendment 1 — C2's warrant clause narrowed to the property the leg enforces

**Finding — first read by the L1 from the instrument's own bytes, then confirmed by the wave on landing bytes.**
`R87ReviewerC2` §F1 (`.ufo/waves/round-87/w1/R87ReviewerC2.md`, receipt `receipts/` r02-class run) shows the accepted
instance at the landing revision with no mutation at all: the r85 row "Naming what a resource derives from" names
`Q1, Q3 (S215)`, `Q3` shares no distinctive word with the row's cells, and `WARRANT_OK` still counts the row. That is
this amendment's narrow. `claims.md` C2 says the warrant leg requires "each named qid to resolve to a located quote that
shares a distinctive content word with the row's own cells". `curation-r87.py` implements two separate conjuncts:

- `len(resolved) == len(qids)` — *every* named qid resolves to a located quote of that entry;
- `shares = any(terms & … for q in resolved)` — *at least one* of them shares a distinctive content word.

A row naming `Q1, Q3` where only `Q1` shares a term passes. The frozen sentence therefore reads wider than the
instrument on the sharing conjunct.

**Narrowed sentence (the one that verifies).** For every decision-table row of the two routed entries, every qid named
in the `Warrant` cell resolves to a located quote of that entry, and at least one named qid's quote shares a
distinctive content word with the row's `Do`/`Never` cells. Measured at landing: `WARRANT_OK=17/17`.

**What the narrowing moves from counted to reviewed.** The stronger reading — every named qid's quote must share a term
— is review-verified for the routed rows: `Q13` carries row 48's term `changed`, and the r85 row 6's `Q7` carries
`review`/`accuracy`/`completeness`. It is not enforced for rows naming several qids, and this amendment says so. The
`E6` forgery (re-pointing to `Q10`) is refused under either reading, so C2's K3 is unaffected.

**Routed to round 88.** Require the sharing conjunct on every named qid, then re-measure `WARRANT_OK` (expected 17/17
still, but the class must be counted, not reviewed).

## Amendment 2 — C2's floor clause narrowed to a row count, not a quote-content check (wave artifact `R87ExecC2Forge`)

**Finding.** `claims.md` C2 says the per-entry floor exists "so a deleted or truncated quote table fails".
`R87ExecC2Forge` falsifies the clause as written on two accepted forgeries, each a one-cell edit of a mirrored tree:

- **A1c** (`.ufo/waves/round-87/w1/R87ExecC2Forge/receipts/receipt-A1c-strong-junk.txt`): delete the real `Q11` row
  (`"Date (often a range) of validity of a resource."`) and add `| Q99 | S023 | "validity" |` — a one-word quote that
  *is* verbatim in the S023 capture — then repoint the decision row's warrant `Q11 → Q99`. Observed
  `QUOTES_LOCATED=20/20 Q_FLOORS=…r84=13/13 floor13 WARRANT_OK=17/17 LEGS=7/7 PASS`, exit 0. The real quote's content is
  lost and no leg detects it: the count is restored, the qid resolves, the distinctive word `validity` is shared, and
  the quote is verbatim (K2's wording is met).
- **A1d** (`.ufo/waves/round-87/w1/R87ExecC2Forge/receipts/receipt-A1d-truncate-to-junkword.txt`): replace `Q11`'s quote
  with the bare verbatim word `"range"`. Observed `QUOTES_LOCATED=20/20 … WARRANT_OK=17/17 LEGS=7/7 PASS`, exit 0.

The instrument enforces a **count of located rows**, and nothing about a quote's length or content; the frozen sentence
reads wider.

**Narrowed sentence (the one that verifies).** The per-entry floors are *counts* of located quote rows (13 and 7, the
measured base counts): a table with a deleted row fails (E5b, `19/19`→ floor 7 breached at `6/6`), a table cut down to
two rows fails both floors (E5c2), and each entry's located count must equal its total. The floor does **not** check a
quote's length or content, so a substituted table whose row count is restored by a verbatim one-word quote passes
(A1c/A1d). Measured at landing: `Q_FLOORS=…r84=13/13 floor13,…r85=7/7 floor7`, `FORGERY_REFUSED=4/4` on the four routed
forgeries.

**What the narrowing moves from counted to reviewed.** The floor's composition is review-verified for the routed rows:
the A1b and A3 deletions are caught by the **warrant** leg's dangling-qid check, not by the floor, which shows the two
legs compose rather than one carrying the class.

**Routed to round 88.** Add a per-row quote floor (a minimum token count per located quote row, or a per-row
`norm(quote)` length bound), then re-measure; the phrase "truncated quote table" may not return to the claim until that
leg is counted.

**Also recorded (no widening):** the warrant sharing conjunct is per row (`any`), so a padding qid alongside a good one
is not detected (`B1b-second-qid-unshared`, `PASS`) — this is Amendment 1's narrowing, confirmed by the same seat.


## Amendment 3 — C2's `TEACHES` disposition is structural, not status-checked (wave artifact `R87ReviewerC2` §F2)

**Finding.** `claims.md` C2 says the leg "requires every flagged row to be disposed as superseded". `curation-r87.py`
builds its supersession set from every row whose `teaches` opens `supersedes S0NN —`, **regardless of that row's
status**. `R87ReviewerC2` §F2 (`.ufo/waves/round-87/w1/R87ReviewerC2.md`) constructs the case: S031 set to `rejected`
while still naming `supersedes S024 —`; the flagged `S024` is then disposed by a superseder that is not itself evidence,
and the leg passes. Observed at landing: `TEACHES_FLAGGED=1 TEACHES_UNRESOLVED=0`, exit 0.

**Narrowed sentence (the one that verifies).** A flagged row is disposed when another registry row's `teaches` opens
`supersedes S0NN —` naming it — a **structural** edge. Whether the superseding row is `mined`, `queued` or `rejected`
is not consulted. Measured at landing: `TEACHES_CHECKED=1 TEACHES_FLAGGED=1 TEACHES_UNRESOLVED=0`, with the one flagged
row (`S024`) reported and disposed by `S031`.

**What the narrowing moves from counted to reviewed.** The disposition's adequacy — that `S031` is `mined` and its own
`teaches` refuses the comparison — is review-verified at landing (`corpus/SOURCES.md:41`) and is not enforced.

**Routed to round 88.** Require the superseding row's status to be `mined` before it disposes a flagged row, then
re-measure with a `rejected`-superseder mirror as a control (the shape `R87ReviewerC2` §F2 already builds).

## Amendment 4 — C1's class width, verdict-accounting clause and named limit narrowed to what the legs enforce (wave artifact `R87ReviewerC1`)

**Findings** (`.ufo/waves/round-87/w1/R87ReviewerC1.md` §(a)–(c), receipts `E1_*` … `E8_*`, `probe-count.txt`). Three
clauses of the frozen sentence read wider than the instrument. Landing bytes are not falsified: the predicate prints the
frozen line, `D1_EXPECTED=3 D1_FORGES=3`, and the two builders agree on this tree.

1. **Width (§a).** `_qualifying_203` accepts **any** non-200 status with a matching capture (`http.isdigit() and
   http != "200"`), not 203; `count_203_rows` additionally requires a 3-digit `http` and deduplicates on `(sid, url)`.
   On this tree both yield exactly `[(S021,203),(S032,203),(S022,203)]`, so the claim's "3" holds, but a future `201`
   or `204` row with a stored body would widen the class and both width sides would widen together.
2. **Verdict accounting (§b).** `LEGS` counts *appends*, not executions. `E4` (SETUP `ok` expression tautologised) and
   `E7` (all 14 list legs tautologised) print `LEGS=15/15 PASS` with exit 0, and `E1` (both width sides narrowed to one,
   floors lowered to 1) also passes the instrument's own verdict. Only a deleted append (`E8`) or a one-sided narrowing
   fails.
3. **Named limit (§c).** The frozen limit names only "a leg that executes and misreports its printed value". The measured
   survivable family is wider: an `ok` expression detached from its measurement while the detail string stays accurate
   (`E2`–`E4`, `E6`, `E7`), and a kill expression hardcoded after a real mutant run (`E5`).

**Narrowed sentence (the one that verifies).** The round-87 battery's verdict is the conjunction of 15 legs appended
exactly once each plus a frozen expected-append count (`EXPECTED_LEGS = 15`), and its two width derivations are
independent code paths. Against the round-86 instrument this changes the verdict for the **`M2` denial shape** (a mutant leg that reports it
derived nothing — `derived=0`, measured `KILLED`) and the **`M5` shape** (a deleted leg append — measured `KILLED`), and
the width leg refuses a class narrowed on one side (`T4-truncate`, `T4-record-keyed`, both `KILLED`). It does **not**
change the verdict for the **`M2` credit shape** (fields hardcoded to 1 with no mutant built): the two-point variant
`R87CriticClaims` §(c) builds (`fixtures/m2-two-point.py`) prints the full frozen line and `PASS`, and is covered only by
the restated limit below, not by a leg. The earlier draft of this amendment called the credit shape "measured `KILLED`";
that sentence was not witnessed and is withdrawn here. The class is *every committed
refetch row that qualifies* — a successful non-200 attempt whose stored capture hashes to the row's `txt_sha256` and
carries a quotable line — three at this base, all `203`. Measured at landing: `D1_EXPECTED=3 D1_FORGES=3 D1_REFUSED=3/3
D2_FORGES=3 D2_REFUSED=3/3 MUT_ADMIT_KILLED=1 MUT_UNREACH_KILLED=1 DERIVE_NEG=1 LEGS=15/15`, `MUTANTS_KILLED=4/4
TOOL_MUTANTS_CAUGHT=2/2`.

**Restated named limit (the true width).** Any counter edit that **keeps every append and the printed detail strings**
while detaching an `ok` expression from its measurement survives: a tautologised leg expression (`E2`–`E4`, `E6`, `E7`),
a kill expression hardcoded after a real run (`E5`), or a joint narrowing of both width derivations (`E1`). `LEGS` is an
append count, never an execution count.

**Routed to round 88.** (i) Bind the class to `http == "203"` (and keep the length check in both derivations), so the
claimed width is the enforced one; (ii) have each leg write its own one-line receipt under `--work` and re-read the leg
count, names and values from that file, so a tautologised `ok` expression changes the re-read; (iii) make the width legs
compare against a 203-only count rather than against each other.

**What the narrowing moves from counted to reviewed.** That the three qualifying rows *are* 203 is review-verified
(`R87ExecRepro` re-derived the row list by hand); the instrument does not enforce it after this amendment.

## Amendment 5 — C2's leg load-bearingness is witnessed on the control mirrors, not on the landing tree (wave artifact `R87MutCounter`)

**Finding.** `R87MutCounter` mutated `curation-r87.py` eight times; four mutants keep the full frozen line and verdict on
the **landing** tree: `B1-floor-drop` (per-entry floors removed), `B2-total-only-located` (denominator counts only located
quotes), `B3-warrant-drop-shares` (the sharing conjunct removed) and `B8-warrant-dead-detector` (every row credited).
Each removes a leg this round claims. They survive because no instance of their class fails on the landing tree — the
floors are exactly met, every quote is located, and every warrant row passes — so a leg and its tautology are
indistinguishable there.

**What this does and does not change.** The legs are load-bearing on the trees where their class has a failing
instance, and that is measured: `curation-r87-controls.py` refuses `E5b` and `E5c2` on the `FLOOR` leg, `E6` on the
`WARRANT` leg and `T-teaches-contrast` on the `TEACHES` leg (`FORGERY_REFUSED=4/4`, part of C2's K3). The frozen
sentence is not widened or narrowed by this finding; what it adds is the *scope of the mutation evidence*: a
counter-mutation battery scored only against the landing tree cannot certify a leg whose class is unrepresented there.

**Routed to round 88.** Score the counter mutants against the control mirrors as well as the landing tree, and require
`B1`/`B2`/`B3`/`B8`-shaped mutants to be killed on the mirror that instantiates their class. (`mutate-r87.py`'s
`N-deny-width` is already labelled `EQUIVALENT_ON_TREE` for the same reason.)


## Amendment 6 — C2's floor can be restored by an *uncited* quote row and a relabelled duplicate (wave artifact `R87CriticClaims` §(d), caseG)

**Finding.** `R87CriticClaims` caseG (`.ufo/waves/round-87/w1/R87CriticClaims/fixtures/caseG-r84.diff`,
`caseG.txt`): delete the uncited quote row `Q10` (no decision row names it) and re-label a duplicate copy of `Q13` as
`Q14`. Observed `QUOTES_LOCATED=20/20 Q_FLOORS=…r84=13/13 floor13 WARRANT_OK=17/17 LEGS=7/7 PASS`, exit 0. The count is
restored without adding any evidence, because the floor counts *rows* and the warrant leg only reads the qids a
decision row names — an uncited row is invisible to it.

**What Amendment 2 already said, and what it missed.** Amendment 2 narrowed the floor to a count of located rows and
named the one-word-substitution class (`A1c`, `A1d`). It did not name this class: the substitution happens on a row no
decision row cites, so even a per-row token floor on *cited* rows would not close it (the critic's own sentence: "its
proposed per-row token floor does not close that class — pin the per-entry qid set").

**Narrowed sentence (unchanged from Amendment 2, now with the class named).** The per-entry floors are counts of located
quote rows; a table with a deleted row fails, a table cut to two rows fails, and a restored count is not evidence of
restored content (`A1c`, `A1d`, `caseG`). Measured at landing: `Q_FLOORS=…r84=13/13 floor13,…r85=7/7 floor7`,
`FORGERY_REFUSED=4/4` on the four routed forgeries.

**Routed to round 88 (replaces Amendment 2's remedy).** Pin the per-entry *qid set* (a committed list of the qids the
entry is allowed to carry) and require `set(qids) == pinned_set` as well as the count; a per-row token floor is not
sufficient. Then re-measure with `caseG` as a control.
