# R87CriticClaims — round-87 claim critic (L1 review seat)

Lane `chousa`, round 87, seat `R87CriticClaims`. Leaf only: no subagent, no lane/fleet git mutation, no production edit, no
network. Only files written: this report and `.ufo/waves/round-87/w1/R87CriticClaims/` (receipts, fixtures, diffs).
Every tree and fixture lived under `/fast/scratch/hyaku/chousa-r87/R87CriticClaims/` and is deleted before yield. No tool
was installed or upgraded.

Paths used below:

```
S=/fast/scratch/hyaku/chousa-r87/R87CriticClaims
L=$S/landed   # git archive e6e920a4… | tar -x
B=$S/base     # git archive 6495ef88… | tar -x
REPO=/home/vgpnk/Projects/shokunin/chousa-shokunin
W=$REPO/.ufo/waves/round-87/w1/R87CriticClaims
```

Trees were built with `git -C $REPO archive <rev> | tar -x -C <dir>`; no network. Frozen contract read first:
`corpus/evidence/round87/claims.md` (all four kill rules), then `plans/round-87.md` — the pre-freeze repairs *and* the
five post-freeze amendments (Amendments 1–5), because those amendments already narrow the clauses my counterexamples
touch and the verdicts below are stated against both texts.

## Provenance — pinned bytes first

Computed on the extracted landing tree before any measurement; every hash equals `corpus/evidence/round87/instrument-pins.txt`:

```
07336fcad89db137…  corpus/evidence/round87/gate-records-r87.py   (pin; freeze blob c033577b and landing blob both match)
a17a02b86b3d07d2…  corpus/evidence/round87/curation-r87.py       (pin; freeze and landing match)
87a88ceb0f79fa73…  corpus/evidence/round87/curation-r87-controls.py
9625c8cda07901fb…  corpus/evidence/round87/mutate-r87.py
8c089828981bb0c8…  corpus/evidence/round87/c1-positives.tsv
905f9da2fdf233b3…  tools/gate-records.py                         (pin; landing only)
fe204539b9b549ef…  tools/gate-records.py at 6495ef88             (pre-repair; the table below shows the repair is load-bearing)
```

The two `git show c033577b:corpus/evidence/round87/… | sha256sum` runs give the two pins exactly, so
the freeze bytes are the scoring bytes. `git diff e6e920a4..abf7ea58 -- corpus/lessons` is empty (HEAD `abf7ea58` adds only
`.ufo/waves/round-87/`), so the live-lane `git grep` used by `build_fresh_positives` reads the landing lesson bytes today.

## Baselines reproduce exactly

| run | command (abridged) | observed | exit |
|---|---|---|---|
| C1 landing | `python3 -B $L/corpus/evidence/round87/gate-records-r87.py --root $L --repo $REPO --work $S/w-land` | `TOOL=present … D1_EXPECTED=3 D1_FORGES=3 D1_REFUSED=3/3 D2_FORGES=3 D2_REFUSED=3/3 MUT_ADMIT_DERIVED=1 MUT_ADMIT_KILLED=1 MUT_UNREACH_DERIVED=1 MUT_UNREACH_KILLED=1 DERIVE_NEG=1 LEGS=15/15` / `GATE_RECORDS_R87=PASS` | 0 |
| C2 landing | `python3 -B $L/corpus/evidence/round87/curation-r87.py --root $L` | `SUPERSEDED_LIVE=0 UNENTAILED_TERM=0 MODIFIED_DEF_CITED=1 QUOTES_LOCATED=20/20 Q_FLOORS=…r84=13/13 floor13,…r85=7/7 floor7 WARRANT_OK=17/17 TEACHES_CHECKED=1 TEACHES_FLAGGED=1 TEACHES_UNRESOLVED=0 LEGS=7/7` / `CURATION_R87=PASS` | 0 |
| C2 controls | `python3 -B $L/corpus/evidence/round87/curation-r87-controls.py --root $L --work $S/w-cur` | `FORGERY_REFUSED=4/4 R86_ACCEPTED_FORGERY=4/4` / `CONTROLS=PASS` | 0 |
| C1 k0 (pre-round tool) | `… gate-records-r87.py --root $L --repo $REPO --tool $B/tools/gate-records.py` | `FORGED_REFUSED=359/362 … D2_REFUSED=0/3 … MUT_UNREACH_DERIVED=0 MUT_UNREACH_KILLED=0 … LEGS=11/15` / `FAIL` | 1 |
| C1 frozen r86 instrument | `… round86/gate-records-r86.py --root $L --repo $REPO` | `D1_FORGES=1 D1_REFUSED=1/1 MUT17_KILLED=1/1`, no `D2_` field / `PASS` | 0 |
| C2 frozen r86 counter | `… round86/curation-r86.py --root $L` | `QUOTES_LOCATED=20/20` / `CURATION_R86=PASS` | 0 |

Receipts: `c1-landed.txt`, `c2-landed.txt`, `c2-controls.txt`, `c1-k0-repro.txt`, `c1-r86-instrument.txt`,
`c2-r86-on-r87.txt`. The k0 line is byte-for-byte the committed `controls/receipts/c1-k0-donothing.txt`.

Other landing facts measured, not assumed:

- `b-d1-class.txt`: the qualifying class is exactly three rows — `('S021','203'), ('S032','203'), ('S022','203')`; S021 and
  S032 share capture key `58725f5e0ac436166546a5ec`, S022 uses `ff9013bd7d9387e45cd6e000`.
- C1 harm, landing tree + pre-repair tool: `HARM_RECHECK files=11 records=28 moved=0 base_rc=0 r87_rc=0`, exit 0
  (`c1-harm.txt`). Freeze tree reproduces the committed receipt exactly: `files=10 records=27 moved=0`, exit 0
  (`c1-harm-freeze.txt`). The 27/10 figure in `claims.md` is the pre-landing tree; landing adds the round-87 lesson
  (28/11) and moves no verdict.
- All 28 committed `GATE-RECORD` lines are `OK` under both the base and the landed tool (`c1-base-tool-verdicts.txt`,
  `c1-landed-tool-verdicts.txt`: 28 ` OK`, 0 ` FAIL` each).

## (a) Do-nothing instruments

All fixtures are in `W/fixtures/`; the copied scripts run from the wave folder. The gate copies must sit next to
`c1-positives.tsv` (`POS_TSV` resolves from the script's own directory), so the counter fixtures were copied into
`$L/corpus/evidence/round87/` for the run only and removed after.

| # | instrument | receipt / exit | frozen predicate | what stops it |
|---|---|---|---|---|
| A1 | `cc-donothing-gate.py`: parses args, prints the frozen C1 line, exits 0 — no leg executed | `a-donothing-gate.txt`, exit 0 | **accepted**: the line is byte-identical | nothing inside the predicate; the freeze/landing blob pins (07336fca…) are the only control, plus a reader who notices no leg output precedes the line |
| A2 | `cc-donothing-curation.py`: echoes the C2 line, exits 0 | `a-donothing-curation.txt`, exit 0 | **accepted** | same: pin a17a02b8… |
| A3 | `fixtures/base-hardcode.py`: runs the **pre-repair** tool by default, then hard-codes `refused/exp/d1_refused/d2_refused/mut_unreach_*` | `base-hardcode.txt`, exit 0 | **accepted** — the frozen line prints `FORGED_REFUSED=362/362 … D2_REFUSED=3/3 … LEGS=15/15` / `PASS`, while its own stdout above the line carries `NOT_REFUSED g0359.md D2-203-reject S021` (also g0360 S032, g0361 S022) | the predicate cannot see it; a reviewer reads the `NOT_REFUSED` lines, and the counter-sha pin catches the substituted instrument. The same base tool **without** the hard-code fails `D2_REFUSED=0/3`, `MUT_UNREACH=0/0`, `LEGS=11/15` (k0 above), so the hard-code is exactly load-bearing |
| A4 | `fixtures/m5-setup-tautology.py`: one leg's `ok` tautologised, detail kept | `m5-setup-tautology.txt`, exit 0 | **accepted**: `SETUP=1/1 … LEGS=15/15` / `PASS` | nothing structural; this is Amendment 4's `E4` class |

The claim's frozen named limit (claims.md:46–48) states this: "the predicate binds the field the leg prints". A3 is the
sharp one — it does not even run the repaired tool, and the battery still prints `PASS`. The stop is provenance
(`instrument-pins.txt` + the freeze blob), not the predicate.

## (b) T4 family re-test

Tool-side T4 is a **tool** rule; counter-side narrowing is a **builder** change. The two are killed by different legs,
and that distinction matters:

| candidate | fixture | observed | exit |
|---|---|---|---|
| T4 tool, one-record exception `r[6] == "200" if sid == "S021" else 2xx` | `fixtures/tool-t4-onerow.py` | `D1_FORGES=3 D1_REFUSED=1/3 D2_REFUSED=3/3 FORGED_REFUSED=336/362 EXPECTED_CODE=336/362`; `LEG_FAIL FORGED`, `LEG_FAIL CODES`, `LEG_FAIL D1_REFUSED`; `D1_WIDTH 3/3` unchanged; `LEGS=12/15` | 1 |
| two-row narrowing `sid in ("S021","S032")` | `fixtures/tool-t4-tworow.py` | `D1_REFUSED=2/3`, `FORGED_REFUSED=337/362`, `LEGS=12/15` | 1 |
| counter class narrowed to `{S021,S032}` in `_qualifying_203` | `fixtures/counter-narrow-tworow.py` | `D1_EXPECTED=3 D1_FORGES=2 D1_REFUSED=2/2`; `LEG_FAIL D1_WIDTH 2/3 floor3`, `LEG_FAIL D2_WIDTH 2/3 floor3`; `LEGS=13/15` | 1 |
| zero-record class (`_qualifying_203` returns `[]`) | `fixtures/zero-record.py` | `D1_FORGES=0 D2_FORGES=0 D1_REFUSED=0/0`; width `0/3`; `MUT_ADMIT_KILLED=0 MUT_UNREACH_KILLED=0`; `LEGS=9/15` | 1 |

So the assignment's expectation is half right, and the half that is wrong is informative:

- `D1_WIDTH`/`D2_WIDTH` kill the **builder** narrowing (2/3 and 0/3); they do **not** move against a T4 **tool** (3/3 in
  both tool rows). The tool rule is killed by `D1_REFUSED` (1/3, 2/3) and by `FORGED`/`CODES`.
- The committed `T4-record-keyed` **counter** mutant in `mutate-r87.py` is not a T4 shape at all. Its anchor
  `'        if cells is None:\n            continue\n'` is applied with `src.replace(old, new, 1)` (`mutate-r87.py:103`),
  and the first occurrence is line 234 — the **fresh unreach builder** inside `build_fresh_positives` — not line 270
  (`_qualifying_203`). Reproduced on clean landing bytes (`c1-mutate-r87-repro.txt`): its only failure lines are
  `LEG_FAIL FRESH 0/5 FRESH_BUILD=FAILED admits=2 revs=2 unreach=0` and `LEG_FAIL RC 3/4`; `D1_WIDTH` is untouched.
  It is killed for a collateral reason. `T4-truncate` (`return out[:1]`) is the clean one-row builder narrowing and does
  print `LEG_FAIL D1_WIDTH 1/3 floor3` / `LEG_FAIL D2_WIDTH 1/3 floor3`.
- Therefore `plans/round-87.md:189` ("the width leg refuses a class narrowed on one side (`T4-truncate`,
  `T4-record-keyed`, both `KILLED`)") is false as to `T4-record-keyed`. The capability is still witnessed (by
  `T4-truncate` and by the two-row/zero-row fixtures above); the *named control* is not the control it claims to be.

## (c) `M2` / `M5` against the landed accounting, and the two-point variant

The two-point variant — stub the printed fields **and** the derived flags, with no mutant built and none run — is
`fixtures/m2-two-point.py`: the block from `positives = files + …` through the `DERIVE_NEG` probe (the whole mutant half) is
replaced by

```
            mut_admit_derived = mut_admit_killed = 1
            mut_unreach_derived = mut_unreach_killed = 1
            derive_neg = 1
```

and the `legs += [...]` registrations are left untouched.

| candidate | receipt / exit | observed |
|---|---|---|
| **M2 two-point** (credit both mutants, build/run none, skip `DERIVE_NEG`) | `m2-two-point.txt`, exit **0** | full frozen line, `MUT_ADMIT_DERIVED=1 MUT_ADMIT_KILLED=1 MUT_UNREACH_DERIVED=1 MUT_UNREACH_KILLED=1 DERIVE_NEG=1 LEGS=15/15`, `GATE_RECORDS_R87=PASS` |
| **M5** delete the `SETUP` leg registration | `m5-drop-setup.txt`, exit 1 | `LEGS=14/15`, `FAIL` — killed by the append count |
| M5 literal round-86 edit (`drop and setup_ok == 1 from passed`) | n/a | no such term in `passed` (line 566 is `len(legs) == EXPECTED_LEGS and all(...)`); the edit is vacuous |
| M5 tautologise the `SETUP` `ok` expression | `m5-setup-tautology.txt`, exit 0 | `SETUP=1/1 … LEGS=15/15` / `PASS` |

The two-point M2 **survives**, and it is stronger than the committed `M2-credit-mutant`. `mutate-r87.py:43–47` replaces the
block with `mut_admit_derived = mut_admit_killed = 0` / `mut_unreach_derived = mut_unreach_killed = 0` — it reports the
mutants as **not derived**, so `LEG_FAIL MUT_ADMIT derived=0 killed=0` kills it. That is a *denial*, not a credit: it never
tests "a mutant credited without being built". My two-point fixture is the first instance of the credit shape, and it
passes. Consequence: `plans/round-87.md:187–188` ("against the round-86 instrument this changes the verdict for the `M2`
shape (a mutant credited without being built) … both measured `KILLED`") is not witnessed by the frozen control battery,
and Amendment 5's "mutation evidence" scope inherits the same hole.

**Named-limit width.** The frozen limit (`claims.md:46`) names "a counter edit that *executes* a leg and misreports its
printed value". The two-point stub executes neither mutant leg nor `DERIVE_NEG` (it removes the block that prints the
`NOT_DERIVED` warnings and runs the mutants), so the frozen wording does **not** cover it: the survivor class is wider than
"executes and misreports". Amendment 4 restates the limit at the true width (`plans/round-87.md:195`): "Any counter edit
that keeps every append and the printed detail strings while detaching an `ok` expression from its measurement survives …
`LEGS` is an append count, never an execution count." Under that restatement the two-point stub **is** covered, and C1's
amended claim is not falsified by it. The remaining defect is evidential: the committed control and the amendment's
sentence both claim the credit shape was measured `KILLED`, and it was not.

## (d) C2 — four routed forgeries, the `2/2` junk-row shape, and two floor counterexamples

The four routed forgeries reproduce `FORGERY_REFUSED=4/4 R86_ACCEPTED_FORGERY=4/4` (`c2-controls.txt`, exit 0): E5b, E5c2 and
T are refused on the `FLOOR`/`TEACHES` legs, E6 on `WARRANT 16/17`. K2 is independently verified: all 20 located quotes are
verbatim (whitespace-normalised, curly quotes folded) in the capture of the registry row's own URL — `K2 quotes=20
not_located=0` (`c2-k2-verify.txt`). K4 is not a dead detector: `TEACHES_FLAGGED S024 terms=publication,modification
disposition=superseded by S031`; S024's own capture is the schema.org/lastReviewed page (key `11d6cc56bb24adfc61eea2b4`,
shared with S031) and contains `modified`/`modification`/`publication` 0 times, so the flag is a real miss, not a
missing-capture artifact.

Fixtures are mirrors of `corpus/SOURCES.md` + the two entries with `corpus/captures` and `corpus/evidence/round57`
symlinked; every diff from the landed tree is in `W/fixtures/case*-r8*.diff`. One example command:

```
python3 W/fixtures/build-caseG.py $L $S $W
python3 -B $L/corpus/evidence/round87/curation-r87.py --root $S/caseG
```

| case | edit | observed | exit |
|---|---|---|---|
| **E5b+E5c2 junk rows** (`caseJ`) | keep only Q13 (r84) / Q7 (r85), add 20 junk rows that split into 5 cells (dropped from both numerator and denominator) | `QUOTES_LOCATED=2/2`, `Q_FLOORS=…r84=1/1 floor13,…r85=1/1 floor7`, `WARRANT_OK=2/17`; `LEG_FAIL FLOOR`, `LEG_FAIL WARRANT` | 1 |
| delete Q10 only (`caseF`) | remove the uncited Schema.org subproperty row | `QUOTES_LOCATED=19/19`, `Q_FLOORS=…r84=12/12 floor13`; `LEG_FAIL FLOOR` | 1 |
| **delete Q10 + duplicate Q13** (`caseE`) | restore the row count with a second copy of Q13 | `QUOTES_LOCATED=20/20 Q_FLOORS=…r84=13/13 floor13,…r85=7/7 floor7 WARRANT_OK=17/17 LEGS=7/7` / **`CURATION_R87=PASS`** | **0** |
| **delete Q10 + relabel a duplicate of Q13 as Q14** (`caseG`) | restore the count *and* the distinct-qid count | identical frozen line / **`PASS`** | **0** |
| E6-family re-point row 9 `Q13→Q11` (`caseW`) | a resolving, verbatim quote of the wrong property | `WARRANT_OK=16/17`; `LEG_FAIL WARRANT` | 1 |

`caseE`/`caseG` are the finding. Q10 is the only quote row in either entry that no decision-table row cites (computed on
the landed entries: 13 rows r84, 12 cited, `Q10` uncited; 7/7 cited in r85). Deleting it removes a genuine evidence row
and `FLOOR` still passes at `13/13` because the leg counts rows (`loc >= fl and loc == tot`, lines 198–200), and `quotes`
is a qid-keyed dict (line 175) that a duplicate simply overwrites or a new qid extends. `caseG` keeps every qid distinct
and every quote verbatim, so neither K2 nor the distinct-qid idea alone catches the relabel; a one-line
`len(quotes) == total` catches `caseE` but not `caseG`.

Amendment 2 already narrows this clause to "counts of located quote rows", and its A1c/A1d mirrors show substituted
one-word quotes passing. `caseG` is a new instance of the amended class, and it defeats the amendment's proposed round-88
remedy: a per-row **token/length floor** does not close it, because the relabelled Q14 carries Q13's full 9-token quote,
and the deleted Q10 was never cited. The identity of the removed row disappears; only a pinned qid set (or a pinned
qid→quote map) notices. Amendment 1's `any` narrowing is confirmed independently at landing: the r85 row "Naming what a
resource derives from" names `Q1, Q3`, `Q1` shares `{entities, property, provenance}`, `Q3` shares `{}`, and the row is
still counted.

## Other measured — tradeoff and provenance notes

- **T3-analog on the unreach literal (tradeoff, not a defect at this landing).** `fixtures/tool-rephrased.py` replaces
  `200 <= int(kv["http"]) < 300` with the semantically identical `kv["http"][0] == "2"`. The battery prints
  `POSITIVE=15/15 FRESH_POSITIVE=5/5 FORGED_REFUSED=362/362 D1_REFUSED=3/3 D2_REFUSED=3/3` but
  `MUT_UNREACH_DERIVED=0 MUT_UNREACH_KILLED=0`, `LEG_FAIL MUT_UNREACH derived=0 killed=0`, `LEGS=14/15`, exit 1
  (`tool-rephrased.txt`). The mutant leg scores the literal text, not the capability: the next revision that rephrases
  the rule will fail a correct tool. This is the same tradeoff round-86 recorded for the admit literal (T3); the subject
  tool is pinned with the exact literal, so nothing here falsifies C1.
- **`--tool` / `--repo` provenance (unchanged from round 86).** `--tool` takes any path (`gate-records-r87.py:359`) and
  the counter never asserts the pinned subject sha; the frozen counting command omits `--tool`, so the scored subject is
  `$L/tools/gate-records.py` (sha 905f9da2…). Passing the base tool without a counter edit fails loudly (k0), so the path
  is bound by outcome, not by identity. `--repo` names the live lane; today `git diff e6e920a4..abf7ea58 -- corpus/lessons`
  is empty, so the `rev=` fresh positives are byte-identical to the landing revision, but the run is not a function of the
  landing bytes alone.
- **Class is "non-200", not "203" (Amendment 4 confirms).** `_qualifying_203` accepts any digit status `!= "200"` (line
  264); `count_203_rows` additionally requires three digits (line 303). Both sides are exactly the three 203 rows on this
  tree (`b-d1-class.txt`), and a future 201/204 row with a stored body would join both sides. Amendment 4 records this and
  routes `http == "203"`; no landing falsification.

## Impacted axes

- **operability (C1).** The predicate is met at landing: three-row D1 class, reject-form D2 class, both mutants derived
  from the landing tool bytes and run, `DERIVE_NEG=1`, `LEGS=15/15`; the T4 tool rule and builder narrowings are killed;
  no committed record moves. Defects: the frozen named limit's "executes" wording is narrower than the measured survivor
  class (the two-point stub), and the frozen mutation battery does not instantiate either the M2 credit shape or the
  T4-record-keyed builder narrowing it claims. Amendment 4 already restates the limit correctly; the controls are not fixed.
- **calibration (C2).** The predicate is met and the four routed forgeries are refused; K2 and K4 hold. The floor is a row
  count, so a deleted uncited row plus a relabelled duplicate of another row passes `13/13`; the amended sentence admits
  this, but the amendment's per-row token-floor remedy does not close it and the qid set is not pinned.

## Smallest safe corrections

1. **C2 FLOOR (one line + one frozen list).** Require the per-entry qid set exactly, e.g.
   `set(quotes) == FROZEN_QIDS[rel]` with `FROZEN_QIDS` = `Q1..Q13` (r84) and `Q1..Q7` (r85), in addition to
   `loc >= fl and loc == tot`. That closes `caseE`/`caseG` and the Amendment 2 A1c/A1d relabelling class; a per-row token
   floor does not. Do not edit the frozen `curation-r87.py` — this is the round-88 instrument duty.
2. **C1 mutation battery (control bytes, not the counter).** Change `mutate-r87.py`'s `M2-credit-mutant` to the two-point
   shape (`= 1` constants, no build/run, `DERIVE_NEG` removed) and re-anchor `T4-record-keyed` inside
   `_qualifying_203` (line 270 block) with an assertion that the failing legs are `D1_WIDTH`/`D2_WIDTH`. That makes
   Amendment 4's and Amendment 5's evidence sentences true.
3. **C1 named limit.** Keep Amendment 4's restatement; add the two-point fixture as the canonical `M2` control so the
   survivor is measured rather than argued.
4. No post-freeze edits to either frozen counter; no amendment is needed for the landing predicate, which is met. If the
   judge prefers the frozen sentence over the amendments, the two sentence clauses to narrow are: C1 "credits a mutant it
   never built fails the predicate" (the two-point stub passes) and C2 "a deleted or truncated quote table fails"
   (`caseG` passes). Both are already narrowed by Amendments 4 and 2 respectively.

## Verdicts

VERDICT: R87CriticClaims C1 held — the landing predicate prints the frozen line exactly (`D1_EXPECTED=3 D1_FORGES=3 D1_REFUSED=3/3 D2_FORGES=3 D2_REFUSED=3/3`, both mutants derived and run, `LEGS=15/15`, exit 0), the T4 tool rule and the counter narrowings are killed and no committed record moves, but the committed `M2` mutant is a denial (`derived=0`) and the two-point credit-without-run variant passes, so the "M2 … measured KILLED" evidence sentence is not witnessed; Amendment 4's restated limit already covers the survivor.
VERDICT: R87CriticClaims C2 held — the landing predicate prints exactly, the four routed forgeries are refused 4/4 with named legs, K2 is 20/20 verbatim and K4 flags S024 with a named disposition, but the floor counts rows, so deleting the uncited Q10 and relabelling a duplicate of Q13 as Q14 passes `13/13 20/20 17/17` (caseG); Amendment 2 narrows the sentence but its proposed per-row token floor does not close that class — pin the per-entry qid set.
