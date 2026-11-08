# R88 CriticClaims — falsification of the round-88 frozen claims (C1, C2)

Seat: `R88CriticClaims`. Frozen claims read first: `corpus/evidence/round88/claims.md`
(all kill rules) and `plans/round-88.md` (pre-freeze repairs). Trees built with
`git archive` at `f484d94f` (base) and `4ea9d008abfd2e09cb51649a42678a78f52ac530` (freeze) into
`/fast/scratch/hyaku/chousa-r88/R88CriticClaims/`. Every finding below names the exact command,
the receipt written under `.ufo/waves/round-88/w1/R88CriticClaims/receipts/`, and the observed
output line + exit code. No network was used (every check read committed bytes; both counters
have no `urllib`/`socket`/`requests`/`http.client` imports — verified by grep, clean).
No tool was installed or upgraded (python 3.14.8 only; nothing to record under the tooling
directive). `tools/gate-records.py` blob is byte-identical at base and freeze
(`dc7a4176129a42dc711ae62ceb72ba281fc5595d` at both revisions — verified by
`git rev-parse f484d94f:tools/gate-records.py` / `4ea9d008…:tools/gate-records.py`; both
`dc7a417…`), confirming the round-87 unreach repair stands and C1 changes only the battery.

## Landing baselines (re-derived, not trusted from the committed controls)

- C1, exact counting command from claims.md (base → freeze trees under scratch):
  `python3 -B <freeze>/corpus/evidence/round88/gate-records-r88.py --root <freeze> --repo
  /home/vgpnk/Projects/shokunin/chousa-shokunin --work <scratch/real/c1work>`
  → prints `GATE_RECORDS_R88=PASS`, `LEG_REREAD=15/15 RECONCILED=15/15 LEGS_APPENDED=15`,
  exit 0. Receipt: `receipts/c1-landing.log`.
- C2: `python3 -B <freeze>/corpus/evidence/round88/curation-r88.py --root <freeze>`
  → `CURATION_R88=PASS`, `SUPERSEDED_LIVE=0 UNENTAILED_TERM=0 MODIFIED_DEF_CITED=1
  QUOTES_LOCATED=20/20 WARRANT_OK=17/17 TEACHES_FLAGGED=1 TEACHES_UNRESOLVED=0 LEGS=7/7`,
  exit 0. Receipt: `receipts/c2-landing.log`.
- Frozen mutation battery:
  `python3 -B <freeze>/corpus/evidence/round88/mutate-r88.py --root <freeze> --repo …
  --work <scratch/real/mutwork>` → `MUTANTS_KILLED=6/6 TOOL_MUTANTS_CAUGHT=2/2 TOTAL=8/8`,
  exit 0. Receipt: `receipts/mutate.log`.
- Curation controls: `python3 -B …/curation-r88-controls.py --root <freeze> --work …`
  → `FORGERY_REFUSED=5/5 R87_ACCEPTED_FORGERY=5/5 CONTROLS=PASS`, exit 0.
  Receipt: `receipts/c2-controls.log`.

## (a) The do-nothing test

### C1 — three do-nothing variants

**A1. Echo wrapper (skips all work, prints the frozen line).**
`fixtures/gate/do-nothing.py` prints the exact frozen predicate line plus
`LEG_REREAD=15/15 RECONCILED=15/15 LEGS_APPENDED=15` and `GATE_RECORDS_R88=PASS`, runs
nothing. Command: copied to `$S/dn/gate-records-r88.py` with the committed
`c1-positives.tsv` beside it, run as
`python3 -B $S/dn/gate-records-r88.py --root <freeze> --repo … --work $S/dn/work`
→ the frozen three lines, exit 0. Receipt: `receipts/do-nothing-c1.log`.
*Would the frozen predicate accept it?* A scorer that greps stdout for the frozen fields
accepts it. The frozen predicate binds the counter by path
(`corpus/evidence/round88/gate-records-r88.py`) and by sha256 in `instrument-pins.txt`
(`f5096b02…` for `gate-records-r88.py`, verified by `sha256sum` against the committed pin
file — both match). No code in the tree verifies the pin file (grep for
`instrument-pins` across the round-88 evidence finds only the pin file itself; neither
counter greps it), so the do-nothing instrument is stopped only by an independent
sha/path check — i.e. by this critic (and the wave's mutation seat), not by the predicate
mechanics. This is the same structural position as round 87's do-nothing control; the
claim's named limit covers only the joint-rewrite-of-writer class, not the echo wrapper.
Noted, not counted as a firing: K1–K4 do not cover "counter replaced by a printer", and
the freeze explicitly pins the instrument bytes so substitution is detectable.

**A2. Counter that runs the base tool but hard-codes the new 203 fields.**
`fixtures/gate/hardcoded-fields.py`: `_qualifying_203`, `count_203_rows` and
`registry_rows_203` replaced by constants (`return 3`). Command:
`python3 -B $S/hard/gate-records-r88.py --root <freeze> --repo … --work $S/hard/work`
→ `WRONG_CODE g0356.md D1-203-admit S021 expected=REFETCH got=PARSE` (×6 lines),
`EXPECTED_CODE=356/362`, `D1_REFUSED=0/3 D2_REFUSED=0/3`, `GATE_RECORDS_R88=FAIL`, exit 1.
Receipt: `receipts/hardcoded-fields-c1.log`.
*Stopped by:* the forged records built from the hard-coded (fake) qualifying rows do not
parse as the tool expects, so the forgery-code leg fails. Hard-coding the width without
building real records is caught. **Held.**

**A3. Counter whose legs all report `ok` from constants (details kept honest).**
`fixtures/gate/constants.py`: every leg of the `legs +=` block forced to `True` (measured
`p_ok`/`refused`/etc. still in the detail strings). Command:
`python3 -B $S/constants/gate-records-r88.py --root <freeze> --repo … --work $S/constants/work`
→ full PASS line, exit 0, on the honest tree (where measurements pass anyway, so
constants ≡ honest — this variant alone proves nothing, see (b) for the discriminating
form). Receipt: `receipts/constants-c1.log`.
*Would the frozen predicate accept it?* Yes, on this tree. What stops the harmful version
is the reconciliation on legs whose detail records a failure — which is (b).

### C2 — do-nothing variants

**A4. Echo wrapper.** `fixtures/curation/do-nothing.py` prints the frozen
`CURATION_R88=PASS` line, exit 0. Receipt: `receipts/do-nothing-c2.log`. Same verdict as
A1: stopped only by the path+sha pin (`f99ac9b7…` for `curation-r88.py`, verified by
`sha256sum`), no in-tree verifier. Noted.

**A5. Dead/disjoint legs** — see (b).

## (b) The reconciliation re-test: E7 and E4 against the round-88 battery

The round-88 battery writes each leg as `<work>/legs/<name>.txt` with
`<name>=ok|fail detail=<detail>` and reconciles the re-read value against the detail
string: it searches `detail=(\d+)/(\d+)`, and if found takes `n == m` as the reconciled
expectation. This covers legs with an `n/m` detail (POSITIVE, FRESH, FORGED, CODES,
EMPTY, RC, SETUP, D1_REFUSED, D2_REFUSED, DERIVE_NEG). It does **not** cover: the
`derived=x killed=y` detail of MUT_ADMIT/MUT_UNREACH (no `n/m` → falls back to
`got_ok and ok`), the `len/d1/div3 pinN` detail of D1_WIDTH/D2_WIDTH (regex matches only
the first `len/d1` pair — `3/3/1` reconciles as `3/3`), or TOOL's `tool present` (no
numbers at all). Two shapes were built to prove the boundary, plus the two frozen ones.

**E7-n/m (round-87 E7 shape: every list leg tautologised).** `fixtures/gate/e7-nm.py`:
`setup_ok = 0` forced, all eight `n/m` legs' `ok` forced `True`, details honest.
Command: `python3 -B $S/e7/gate-records-r88.py --root <freeze> --repo … --work $S/e7/work`
→ `SETUP=0/1`, `LEG_REREAD=15/15 RECONCILED=14/15 LEGS_APPENDED=15`,
`GATE_RECORDS_R88=FAIL`, exit 1. Receipt: `receipts/e7-nm-legs.log`. **Killed**, exactly
the `RECONCILED=14/15` the plan claims for the E4 shape.

**E4-setup-detached (round-87 E4 shape: one leg detached, detail honest).**
`fixtures/gate/e4-setup.py`: `setup_ok = 0`, SETUP `ok=True`.
Command: `python3 -B $S/e4/gate-records-r88.py --root <freeze> --repo … --work $S/e4/work`
→ `RECONCILED=14/15`, `GATE_RECORDS_R88=FAIL`, exit 1. Receipt: `receipts/e4-setup-detached.log`.
**Killed.** Matches the frozen `mutate-r88.py` E4 result (`LEG_FAIL SETUP 0/1`).

**E7c — the width legs detached with a narrowed derivation (NEW FINDING).**
`fixtures/gate/e7c-width.py`: `div3 = 1` (third derivation deliberately narrowed, so the
detail is `3/3/1 pin3`), D1_WIDTH and D2_WIDTH `ok` forced `True`, everything else honest.
Command: `python3 -B $S/e7c/gate-records-r88.py --root <freeze> --repo … --work $S/e7c/work`
→ the full frozen PASS line (all printed fields `3/3/3`-honest in the summary), exit 0.
Receipt: `receipts/e7c-width-detached.log`.
*What stops it?* Nothing in the predicate. The reconciliation regex
`detail=(\d+)/(\d+)` matches the first pair `3/3` of the detail `3/3/1 pin3`, so the
narrowed third component and the `pin3` never enter the reconciliation; the width leg's
own `ok` expression is the only real check, and detaching it is exactly the E4 shape
the claim says K4 fires on. The frozen battery's E1-joint-narrow mutant is *killed*
because its `ok` stays honest (`LEG_FAIL D1_WIDTH 1/3/3 pin3`) — but E1 and E7c differ
only in the detachment, and the detachment is the claim's own K4 case. **This is the
round-87 E7 written over the n/m legs only; over the width legs it survives.**

**E7b — the mutant legs detached (`derived/killed` detail).**
`fixtures/gate/e7b-mutant.py`: MUT_ADMIT/MUT_UNREACH `ok` forced `True` with detail
`derived=0 killed=0`. Command: `python3 -B $S/e7b/gate-records-r88.py … --work $S/e7b/work3`
→ full frozen PASS line, exit 0. Receipt: `receipts/e7b-mutant-detached.log`.
The `derived=0 killed=0` detail has no `n/m`, so `n_ok = (got_ok and ok)` and a detached
`ok=True` reconciles. The summary line still prints the real `MUT_ADMIT_KILLED=1`
(computed before the leg block), so the receipt contradicts the summary only inside the
leg file — which the re-read accepts. **Survives** for the same reason; same K4 class.

**Combined — E7c + E7b + TOOL detached (the strongest do-nothing).**
`fixtures/gate/combined.py`: D1/D2 width narrowed to `div3=1` with `ok=True`, mutant
legs `ok=True` with `derived=0 killed=0` details, TOOL `ok=True`. Command:
`python3 -B $S/combined/gate-records-r88.py … --work $S/combined/work`
→ `TOOL=present POSITIVE=15/15 … MUT_ADMIT_DERIVED=1 MUT_ADMIT_KILLED=1 …
DERIVE_NEG=1 LEGS=15/15`, `LEG_REREAD=15/15 RECONCILED=15/15 LEGS_APPENDED=15`,
`GATE_RECORDS_R88=PASS`, exit 0. Receipt: `receipts/combined-width-mutant-detached.log`;
the dishonest leg receipts are copied at `receipts/combined-legs/` (e.g.
`MUT_ADMIT.txt` contains `MUT_ADMIT=ok detail=derived=0 killed=0` and `D1_WIDTH.txt`
contains `D1_WIDTH=ok detail=3/3/1 pin3` — the re-read files themselves carry the
contradiction the predicate does not check). The frozen predicate **would accept this
counter**. It does not jointly rewrite the leg writer or the reconciliation: the writer
still writes each leg's measured detail, and the reconciliation still runs — only the
`ok` bindings of five legs are detached. That is the claimant's own K4 sentence ("a
leg's `ok` value is detached from its measured detail, while the frozen predicate still
prints `PASS`"), so it is inside the claim's cover, not inside the named limit (the
named limit is the joint rewrite). **Firing for C1.**

Smallest safe correction: make the reconciliation check each leg's own tally in its own
format — for the width legs require the full `len/d1/div3 == pin` (or at least that the
last number equals `pin` and `div3`), for the mutant legs require `derived`/`killed`
to match the ok, and for TOOL require the file present. Concretely, parse
`detail=(\d+)/(\d+)/(\d+) pin(\d+)` and demand all four equal for width legs, parse
`derived=(\d+) killed=(\d+)` for the mutant legs. That closes E7c/E7b without touching the
accounting shape.

**E7-over-everything (control).** `fullE7` (all 15 legs tautologised, SETUP
forced-failing, width narrowed) → `RECONCILED=14/15`, `GATE_RECORDS_R88=FAIL`, exit 1.
Receipt: `receipts/fullE7.log`. It fails through the SETUP canary, proving the
`n/m` reconciliation works where it reaches — and, by contrast, that the combined
five-leg detachment (which avoids the `n/m` legs) is the live shape.

### C2 — reconciliation re-test (C2 has no leg-receipt mechanism)

`curation-r88.py` has **no** receipt files, no re-read, no reconciliation:
`passed = len(legs) == EXPECTED_LEGS and all(ok for _, ok, _ in legs)`. Any detached `ok`
passes. Three instruments were built:

**Dead TEACHES detector.** `fixtures/curation/dead-teaches.py`: the detector never flags
(`if miss: pass`), TEACHES `ok` forced `True`.
Command: `python3 -B $S/deadteaches.py --root <freeze>`
→ `TEACHES_CHECKED=1 TEACHES_FLAGGED=0 TEACHES_UNRESOLVED=0 LEGS=7/7 CURATION_R88=PASS`,
exit 0. Receipt: `receipts/c2-dead-teaches.log`.
The printed fields contradict the verdict (`FLAGGED=0`), so a field-reading scorer
catches it against the frozen predicate (`TEACHES_FLAGGED=1` is part of the predicate),
but the counter's own PASS line is dishonest and K4's "a dead detector" is exactly this
shape. **Firing for C2 on K4.**

**Detached TEACHES with a live detector.** `fixtures/curation/detached-teaches.py`: one
row forced unresolved, TEACHES `ok` forced `True`.
Command: `python3 -B $S/detachedc2.py --root <freeze>`
→ `TEACHES_FLAGGED=1 TEACHES_UNRESOLVED=1 LEGS=7/7 CURATION_R88=PASS`, exit 0.
Receipt: `receipts/c2-detached-teaches.log`. The summary honestly prints
`TEACHES_UNRESOLVED=1` and the `TEACHES_FLAGGED S024 … disposition=superseded by S031`
line while the verdict claims 7/7 legs pass. **Firing for C2** (detached `ok`, the same
class C1's K4 names; C2's kill rules K1–K4 do not name a detached-`ok` leg for C2, and
there is no reconciliation leg to catch it).

**Constants on a genuinely broken tree (the discriminating C2 proof).** A broken tree was
built in scratch (`$S/broken`, a copy of the freeze tree with `S031`'s status flipped
`mined → queued` in `corpus/SOURCES.md`, so `S024` loses its `mined` disposal):
- pristine counter → `TEACHES_UNRESOLVED=1 LEGS=6/7 CURATION_R88=FAIL`, exit 1.
  Receipt: `receipts/c2-pristine-on-broken.log`.
- all seven legs' `ok` forced `True` (`fixtures/curation/constants.py`, details honest)
  → `TEACHES_UNRESOLVED=1 LEGS=7/7 CURATION_R88=PASS`, exit 0, still printing
  `disposition=UNRESOLVED` in the flagged line. Receipt: `receipts/c2-constants-on-broken.log`.
*Field check:* the frozen predicate includes `TEACHES_UNRESOLVED=0`, so a field-reading
scorer stops this one too — but the counter prints PASS over its own honest failure
fields, which is the E4 class. **Firing for C2** (the counter's verdict is unsound even
though the printed fields expose it; the counter never reconciles its own verdict with
its own fields).

Smallest safe correction for C2: add the same leg-receipt + reconciliation discipline
C1 has (or at minimum require `passed` to agree with the printed tallies:
`teaches_unresolved == 0`, `teaches_flagged >= 1`, `warrant_ok == warrant_total`,
`not short`, etc. — i.e. derive `passed` from the printed fields rather than a separate
`all(ok)`), so a detached `ok` cannot print PASS over printed failures.

## (c) The do-nothing C2 test (round-87 counter on the round-88 tree)

Command: `python3 -B <freeze>/corpus/evidence/round87/curation-r87.py --root <freeze>`
→ the full round-87 line ending `CURATION_R87=PASS`, exit 0.
Receipt: `receipts/c2-r87-on-r88-tree.log`. **Confirmed**: the prior instrument has no
leg of the four new classes (it prints the same `SUPERSEDED_LIVE=… LEGS=7/7` fields but
its WARRANT/FLOOR/TEACHES legs predate the every-qid, token-floor, pinned-qid-set and
mined-superseder rules — the committed control `c2-d0-donothing.txt` shows the same
line). The round-87 counter is therefore not a do-nothing *for the round-88 claims*: it
cannot express them, and the five-forgery battery is the discriminating evidence
(`FORGERY_REFUSED=5/5`, receipts above).

## What held (attempted falsifications that did not fire)

- **K2 (C1).** The 203 classes refuse with their frozen code: the landing run has
  `FORGED_REFUSED=362/362 EXPECTED_CODE=362/362` and `D1_REFUSED=3/3 D2_REFUSED=3/3`.
  No in-class forged record is accepted. Held.
- **K2 (C2).** `QUOTES_LOCATED=20/20` with whitespace-normalized, curly-quote-folded
  matching in the committed captures, and the five round-87 forgeries are refused
  (`FORGERY_REFUSED=5/5 R87_ACCEPTED_FORGERY=5/5`). Held.
- **K3 (C1 harm).** `controls/receipts/c1-harm.txt` (`HARM_RECHECK files=11 records=28
  moved=0 base_rc=0 r88_rc=0`) and the landing run's `POSITIVE=15/15 FRESH_POSITIVE=5/5`.
  Held (committed receipt, re-derived landing fields agree).
- **K4 (C1, `n/m` legs).** E7-n/m and E4-setup-detached are both killed by
  `RECONCILED=14/15` (above). Held for the ten `n/m` legs.
- **The entry repair (`Q1, Q3 → Q1`).** Not a counter change and not buried: the
  round-88 counter on the **base** tree fails
  `WARRANT_OK=16/17 … WARRANT_UNLINKED … row=Naming what a resource derives from
  warrant=Q1, Q3 (S215) resolved=2/2 … CURATION_R88=FAIL`, exit 1
  (receipt: `receipts/c2-on-base-tree.log`). So the repair is load-bearing for the
  landing PASS and is disclosed in `plans/round-88.md` repair 6. Q3's quote
  ("then we can say that the *bar chart* prov:wasDerivedFrom the *dataset*") shares no
  `[a-z]{5,}` non-stopword with the row's cells (`provenance, derivation, entities,
  known, property, resource, chain`); Q1's quote shares `provenance, entities,
  property`. The narrowed warrant is genuine. Also: the repair touches no counter
  (the entry is in `ENTRIES` only as a quote table source, which the repair does not
  alter — `Q1..Q7` all still present). Held.
- **Width composition.** The `http_code == "203"` rows in
  `corpus/evidence/round57/refetch.tsv` are exactly S021, S032 (one `(sid,url)` pair
  each sharing the PubMed URL `…/17638714/`) and S022 (`…/28912002/`) — three pairs,
  two URLs, matching `ROWS_203 = 3` and the claims. (A grep for `203` also hits
  `sha256` fragments and the `S203` id with `http_code 200` — verified by
  `awk -F'\t'` on the raw lines.) The capture-hash filter in `_qualifying_203` does
  not secretly narrow further: the committed captures hash to `txt_sha256` for all
  three rows (battery passes). Held.
- **S216 gloss.** "the request was successful but the enclosed content has been modified
  from that of the origin server's 200 (OK) response" (RFC 9110 §15.3.4, as cited
  through the round-87 claims file) supports both the D1 refusal (a 203 admit claiming
  OK content) and the D2 refusal (a 203 reject claiming a failed transfer). Held.
- **Docstring drift (minor, not a finding).** Line 15 of `gate-records-r88.py` says
  "the frozen `203_ONLY=2` constant" while the code uses `ROWS_203 = 3` (and
  `registry_rows_203`). The measured `D1_EXPECTED=3` agrees with the code, so this is a
  stale word in a comment, not a wrong pin. Noted; no axis impact.

## Axes and smallest safe corrections

- **C1 (operability).** The 203 binding itself is sound in both derivations plus the
  third pin (`ROWS_203 = 3`), and the `n/m` reconciliation is a real E4 killer. The
  defect is that the reconciliation only implements the `n/m` format, leaving five
  legs (TOOL, D1_WIDTH, D2_WIDTH, MUT_ADMIT, MUT_UNREACH) reconcilable by
  construction if their `ok` is detached. Smallest safe correction: per-format
  reconciliation — width legs must equal `n/n/n pin n` with all four equal and `pin ==
  ROWS_203`; mutant legs must satisfy `derived == killed == 1` for `ok`; TOOL must
  require the receipt to name the actual file. Plus add E7c/E7b-shaped mutants to
  `mutate-r88.py` so the battery kills the detachment it now claims to kill.
- **C2 (calibration).** The four new legs are substantively correct (every-qid
  term-sharing, `MIN_TOKENS = 7`, pinned qid sets, mined-superseder disposal) and are
  discriminated by the five-forgery battery. The defect is that the counter has no
  verdict-vs-field reconciliation at all, so a dead detector or a detached `ok` prints
  PASS over honestly-printed failures (K4's own examples). Smallest safe correction:
  derive `passed` from the printed tallies (flagged ≥ 1, unresolved = 0,
  `warrant_ok == warrant_total`, …) or adopt C1's leg-receipt discipline; add a
  dead-detector and a rejected-superseder control to the C2 battery.

Neither correction narrows a claim after landing: both restore the claimed property
(K4 / K4-shaped) rather than weakening it, so they are repairs, not amendments. No
host files were touched; no `pacman`/`sudo`/network was used; no lane git state was
mutated (all work in `/fast/scratch/hyaku/chousa-r88/R88CriticClaims/`, all fixtures
and receipts copied into this seat's wave folder and listed above).

VERDICT: R88CriticClaims C1 fired — the frozen predicate accepts a counter with the width, mutant and TOOL legs detached from their measurements (E7c/E7b/combined survive with PASS), contrary to kill rule K4.
VERDICT: R88CriticClaims C2 fired — curation-r88 prints CURATION_R88=PASS over honestly-printed failures (dead TEACHES detector and detached-ok variants both pass, kill rule K4 shape), because it has no verdict-vs-field reconciliation.
