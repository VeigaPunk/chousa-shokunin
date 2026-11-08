# chousa — round 89: plan and amendments

L1 `ChousaR89`. Base `f8fa55ec` (round-88 landing + the non-author spot-check `corpus/lessons/round-88-verifier-spotcheck.md`). The frozen claims are in `corpus/evidence/round89/claims.md` (prose) and `.ufo/waves/round-89/claims.json` (machine form the pre-file gate reads — round 88 filed no `claims.json` and its gate run ended `SETUP findings=1`). A `narrowing` cell in `.ufo/waves/round-89/claim-falsification.tsv` resolves to a section here.

## Inputs — the round-88 spot-check's routed defects

`corpus/lessons/round-88-verifier-spotcheck.md` `## Routed defects` 1–8:

1. **Prefile ledger layout.** The prefile checker reads `.ufo/waves/round-<N>/claims.json`; round 88 filed only `corpus/evidence/round88/claims.md`. Fixed by writing both forms this round.
2. **Per-format reconciliation (C1).** The `RECONCILED` conjunct searched only `detail=(\d+)/(\d+)`, so a detached `ok` on `TOOL`, on the two width legs (`3/3/1 pin3` read as `3/3`) and on the two mutant legs (`derived=0 killed=0`) survived with `PASS` (`R88ReviewerC1` E4 receipts, `R88CriticClaims` `e7b`/`e7c`/`combined`). Fixed: `rederive()` per grammar.
3. **Verdict-vs-field reconciliation (C2).** `curation-r88.py`'s verdict was `all(ok)` over the legs, never reconciled with its printed fields, so a dead detector printed `TEACHES_FLAGGED=0 … PASS` (`R88CriticClaims` `c2-dead-teaches.log`) and a detached leg printed `TEACHES_UNRESOLVED=1 … PASS`. Fixed: `fields_hold` computed from the printed tallies, plus the `VERDICT` leg.
4. **Dead superseder-own-read clause (C2).** `curation-r88.py:250` matched a case-sensitive `supersedes (S\d{3,}) —` against a lowercased cell — 10 raw matches, 0 lowercased over 218 rows (`R88ScoutRegistry` `receipt-supclause-dead.txt`). Fixed: the raw cell is matched; non-vacuity is the battery's `SUP-clause-mirror`, because no real superseding row names a date term.
5. **Control-receipt discipline.** `expected.tsv`'s `c1-do-nothing` row expected exit 1 while its own receipt printed PASS, and `c2-d0-donothing.txt` had no expectation row (`R88SentinelScope` F7/F7b). Fixed by `controls/run-controls.sh`, which runs each control and refuses to pass unless the receipt's exit code **and** every `required_fields` token agree with the `expected.tsv` row.
6. **Duplicate-qid / swapped-quote forgeries (C2).** Five in-class forgeries passed the round-88 counter green; two are closed here — the duplicate-qid cite (`DUPQID`) and the superseder clause. The quote-content swap and the ≥7-token verbatim substitution are **named limits** in the claim, not silently kept: a content oracle would need a second copy of the entry, and the floor is a measured minimum.
7. **Seat discipline.** `R88ExecForge` shipped no `VERDICT:` trailer. The wave context requires the trailer; the scribe tallies an untrailered seat as a finding, not as a hold.
8. **Operator-owned prompt corruption.** Not the lane's to fix; carried.

## Claim selection

- **C1 — operability (the lowest scored non-retired axis, historical 3/10).** The successor battery closes routed defects 2 and 5, and adds the summary cross-check that makes a printed field and its leg agree. The subject tool is unchanged (`tools/gate-records.py` sha256 `905f9da2…` at base and landing), so no domain record can move; the harm sweep is the check.
- **C2 — calibration.** The successor curation counter closes routed defects 3 and 4 and half of 6.

Rejected as claims this round: a new knowledge entry (no candidate source was opened for one; the round is instrument repair plus the frontier step); the r80 backlog Gate ids and the `S217` successful-refused record form (carried debt, QUALITY 173, no new instrument this round); the round-74 routed "source-blind order oracle" debt (a different instrument, not touched by this round — named in the report as carried, never silently repaired backwards).

## Pre-freeze repairs (before the first scored run, disclosed)

1. **`rederive()` is per-format.** Four grammars, each re-derived from its own receipt text; the fallback `got_ok and ok` (a tautology) is gone.
2. **`CROSSCHECK` compares the printed summary to each leg.** `DIV3` is now printed so the third width derivation is checkable from the summary; `D1_EXPECTED`/`D1_FORGES`/`D2_FORGES`, the mutant `derived`/`killed` fields and every `n/m` field are compared to their leg's re-derived numbers.
3. **`SUMMARY` is a leg.** It is appended, receipted, re-read and reconciled like the rest (`EXPECTED_LEGS` 15 → 16), so a removed receipt changes the verdict.
4. **Mutants carry multi-point edits.** Round 88's survivor shapes need a broken measurement *plus* the detachment that hides it; a single-point healthy-tree mutant proves nothing (its `A3`/`E4` variant). `mutate-r89.py` applies a list of edits per mutant.
5. **C2's verdict is `fields_hold`, not `all(ok)`.** `fields_hold` is computed from the same values the summary prints; the `VERDICT` leg refuses a divergence between the two in either direction.
6. **C2's superseder clause matches the raw cell** and reports `SUP_CLAUSE_CHECKED` so its vacuity on the real registry is visible rather than implied.
7. **The control driver checks receipts against expectations** (routed defect 5) instead of filing receipts beside an unread `expected.tsv`.

## Freeze

`corpus/evidence/round89/claims.md`, `.ufo/waves/round-89/claims.json`, the six instruments, `controls/expected.tsv`, `controls/run-controls.sh`, the eight pre-freeze receipts under `controls/receipts/`, `instrument-pins.txt` and the registry `used-by` updates (S216, S218) are committed together as the freeze, before the landing commit and before any scored run of the round-89 candidates.

## Amendments after the freeze

None yet. An amendment is written here only when a wave artifact falsifies a claim's stated wording (addendum §8, Amendment 59) and names the artifact plus the narrower property that may verify, or the honest stop.

## Amendment 1 — C2's verdict sentence is narrowed: the verdict conjoins the printed-field derivation with the leg accounting

**Finding.** Two seats fired the *sentence* (not the predicate). `R89ReviewerC2` B1: the frozen C2 sentence says the
verdict is "computed from the fields the summary printed … **rather than** from a separate `all(ok)`", but the code is
`passed = … and all(ok for …) and fields_hold` and the `VERDICT` leg is `fields_hold == all(ok) and fields_hold` — the
repair is additive, so "rather than" overstates (receipt `u-A9b`: dropping `fields_hold` from `passed` still FAILs
through the `VERDICT` leg). `R89CriticClaims` recorded the same class from the other side: the verdict follows the
measurement tallies, not a parse-back of the rendered summary line.

**Narrowed property (what verifies).** `CURATION_R89=PASS` requires **both** the leg accounting (`all(ok)` over the
nine legs) **and** `fields_hold`, where `fields_hold` is computed from the same variables the summary line prints, not
by re-parsing the rendered text. The claim is: a dead detector or a detached leg cannot print PASS, because
`fields_hold` re-derives each tallied quantity from the measured variables and the `VERDICT` leg refuses any
divergence between the two in either direction. It is **not** the claim that the legs are redundant.

**What this amendment does not change.** No counter byte, no scored run, no predicate field. The frozen `claims.md`
sentence is not edited (CORPUS rule 2 discipline applied to a frozen claim); this amendment is the narrowing the
closure's `claim-falsification.tsv` cites.

## Amendment 2 — two further by-construction conjuncts are disclosed as seams

**Finding.** `R89ReviewerC2` B3/B4 measured two conjuncts of `fields_hold` that cannot fail on this registry or that
duplicate their own leg: (i) `len(superseded_live)==0` needs a superseded target that is `mined` while its superseder is
not, and every superseded target on this registry is `queued`, so the conjunct is satisfied by construction — the
`TEACHES` leg, not `SUPERSEDED`, is what catches the S031-queued shape; (ii) the `FLOOR` conjunct re-runs the leg's own
formula rather than reading the `Q_FLOORS` string, so a one-sided edit of the formula reopens the detach; and (iii) the
`SETUP` leg is the constant `True` (a missing registry or entry returns exit 2 before the leg block), so it is an
assertion, not a measured field.

**Disposition.** Reported as seams, not repaired beside a scored run: (i) and (iii) are the same family as the disclosed
superseder-clause vacuity (named limit 4), and (ii) is the residual duplication the reviewer names as B4. None falsifies
a stated predicate; the report's *What the instruments measure* section and the round-90 planned row carry them.

## Amendment 3 — the reviewer's registry-count finding is refuted against the committed bytes

**Finding claimed.** `R89ReviewerC2` B2 asserted that S218's `used-by` already contained
`corpus/evidence/round89/claims.md` at base `f8fa55ec`, so only one registry cell materially changed and C2's "two
cells" was one too strong.

**Measurement.** `git show f8fa55ec:corpus/SOURCES.md | grep '^| S218 '` ends `… , corpus/evidence/round87/claims.md |`
and `git show ac0a0892:corpus/SOURCES.md | grep '^| S218 '` ends `… round87/claims.md,
corpus/evidence/round89/claims.md |`. The S218 cell **did** change, and `git diff f8fa55ec ac0a0892 -- corpus/SOURCES.md`
carries one `-`/`+` pair for S216 and one for S218. The finding is refuted; the count stands at two cells. Recorded here
rather than argued in the report, and the receipt is `corpus/evidence/round89/controls/receipts/registry-cells.txt`.

## Amendment 4 — the cross-check is per leg, not per aggregate: `LEGS_MEASURED` is a printed cell bound to nothing

**Finding.** `R89ReviewerC1` F1 (`legs-measured-forge.txt`, `variants/lg-legs-measured-14of15.py`): the summary's
`LEGS_MEASURED={sum(ok)}/{len(legs)}` is not in the `crosscheck()` map, so a one-point edit rendering
`LEGS_MEASURED=0/15` still prints `GATE_RECORDS_R89=PASS` at exit 0 while the `SUMMARY` leg's own receipt reads
`15/15`. Of the 19 printed cells, 18 are cross-checked and `LEGS_MEASURED` is the one hole.

**Narrowed property.** The frozen C1 sentence's cross-check clause is **per leg**: "each leg's re-derived numbers must
equal the fields the summary line printed for it" — it covers the fifteen measurement legs' fields (`POSITIVE`,
`FRESH_POSITIVE`, `FORGED_REFUSED`, `EXPECTED_CODE`, `EMPTY_REFUSED`, `RC`, `SETUP`, `D1_EXPECTED`, `D1_FORGES`,
`DIV3`, `D1_REFUSED`, `D2_FORGES`, `D2_REFUSED`, the four mutant cells and `DERIVE_NEG`) and not the aggregate
`LEGS_MEASURED`, which summarises the leg list rather than any one leg's measurement. The claim does **not** assert
that every printed cell is bound; the aggregate cell is a reporting convenience, and forging it changes no predicate
input.

**What this amendment does not change.** No counter byte, no scored run. **Routed to round 90:** the aggregate becomes
checkable in one line — compare `LEGS_MEASURED` against the `SUMMARY` receipt's own `n/n` — and the same pass should
fold the `SUPERSEDED` and `FLOOR` seams Amendment 2 records. Receipt:
`.ufo/waves/round-89/w1/R89ReviewerC1/legs-measured-forge.txt`.

## Amendment 5 — two wording corrections: the field list is the enumerated one, and the frozen counting command is replaced by one that runs

**Finding (a).** `R89ReviewerC1` F3 (`field-diff.txt`): the sentence's universal "every round-88 field unchanged" is
literally false — `LEGS` was renamed to `LEGS_MEASURED` (a different expression, live leg count instead of
`EXPECTED_LEGS`), `DIV3` was added, and the tool-absent failure path still prints `LEGS=0/16`. **Narrowed:** the
sentence means the **enumerated measurement fields** it lists (`POSITIVE`, `FRESH_POSITIVE`,
`FORGED_REFUSED=EXPECTED_CODE`, `D1_REFUSED`, `D2_REFUSED`, `MUT_ADMIT_KILLED`, `MUT_UNREACH_KILLED`, `DERIVE_NEG`),
all of which are unchanged; renames and additions in the reporting tail are not claimed.

**Finding (b).** `R89ReviewerC1` F2 (`harm-counting-command-verbatim.txt`): the frozen C1 counting command omits the
step that materialises `$W/base-tool.py`, so run verbatim it yields `HARM_RECHECK … moved=31 base_rc=2` and exit 1 —
`moved=0` is unreachable from the frozen three lines. The runnable form is the `expected.tsv` `c1-harm` row, which the
driver executes. **Corrected literal command** (this is the form the report and the driver use):

```sh
L=/home/vgpnk/Projects/shokunin/chousa-shokunin; W=/fast/scratch/hyaku/chousa-r89/c1; mkdir -p "$W"
HOME=/home/vgpnk git -C "$L" show master:tools/gate-records.py > "$W/base-tool.py"
python3 -B "$L/corpus/evidence/round89/gate-records-r89.py" --root "$L" --repo "$L" --work "$W"
python3 -B "$L/corpus/evidence/round89/mutate-r89.py" --root "$L" --repo "$L" --work "$W"
python3 -B "$L/corpus/evidence/round89/harm-recheck.py" --root "$L" --repo "$L" --base-tool "$W/base-tool.py"
```

**What this amendment does not change.** No counter byte and no measured value: `moved=0` holds under the corrected
command (`controls/receipts/c1-harm.txt`, `archive-tree-harm.txt`). The frozen `claims.md` is not edited; this
amendment is the correction of record.

## Amendment 6 — named limit 1's edit surface is corrected; its boundary claim stands

**Finding.** `R89ReviewerC1` F4: the second half of named limit 1 reproduces exactly — forging `div3`, both width
`ok`s and both details dies on `UNCROSSCHECKED … DIV3=1` unless the summary's `DIV3` is forged too, and with it the
shape passes. But the first sentence names the wrong surface: the surviving edit never touches "the leg writer, the
receipt files [or] the reconciliation". Receipts are rendered from the leg tuples, so forging the tuple's `ok` **and**
its detail **and** the summary cell is the whole edit.

**Corrected wording of the limit.** A counter edit that forges a leg's `ok`, its printed detail **and** the summary
cell the cross-check compares against survives — that edit *is* the counter, because the reconciliation and the
cross-check both read the forged tuple. The boundary claim (a coherent joint forgery survives; a one-sided one does
not) stands as measured.

## Amendment 7 — the control-receipt driver's own discipline is defective; the claim's predicate is unaffected and the repairs are routed

**Finding.** `R89SentinelScope` B1–B4, each measured with a receipt:

- **B1 (medium)** `controls/run-controls.sh:25` writes `>"$out"` **before** grepping `"$out"`, so the committed receipt
  is overwritten before it is read. What the driver proves is "a *fresh* run of this instrument satisfies the row",
  not "the committed receipt satisfies the row". A committed receipt contradicting `expected.tsv` is silently erased.
- **B2 (low-medium)** `grep -qF -- "$f" "$out"` is fixed-string **substring**, not field equality, so a receipt
  printing a longer value that starts with the expected ratio (`LEG_REREAD=16/160`) satisfies the row.
- **B3 (medium)** every `expected.tsv` row hard-codes `--root/--repo` to the live working tree, so the driver measures
  whatever the tree holds **now** rather than the frozen revision; the receipt therefore carries no
  `# computed_against=` revision pin (QUALITY 189's class).
- **B4 (medium)** the `c1-harm` row requires only `moved=0`; `harm-recheck.py` reports `moved=0` when the subject tool
  cannot run at all (both verdict maps empty, `records=0`). The committed receipt is `records=29 moved=0`
  (`controls/receipts/c1-harm.txt`), so the value is measured over a non-empty set — but the *row* would also accept a
  vacuous run.

**Narrowed property (what the claim actually guarantees).** The frozen C1 sentence's harm clause is
`moved = 0` over the **non-empty** `GATE-RECORD` population the run reads (`records=29` in the committed receipt), and
the control rows are checked by a fresh run of each instrument against the expectations file — **not** by re-reading
the committed receipt bytes. The predicate fields themselves are unaffected: every one of the eight committed receipts
reproduces from its command, and the sentinel measured 7 of 8 byte-identical with the eighth explained by B3.

**Disposition.** Routed to round 90 as a single package: verify the **committed** receipt (read-then-write, or write to
a temp and compare), match `key=<value>` as a whole token, pin `# computed_against=<rev>` in every receipt, and require
`records>=1` plus a setup negative for the harm control. Not repaired after scoring, because a post-scoring repair
cannot rescue a claim.

## Amendment 8 — C2's `VERDICT fields_hold=1` is not a printed token; the observable is the failure side

**Finding.** `R89SentinelScope` B5: `curation-r89.py` appends the `VERDICT` leg with the detail
`fields_hold=1 legs_ok=…/…`, but the summary line prints only `LEGS_MEASURED=8/9` (measured before the leg is
appended), so the frozen C2 sentence's parenthetical "(`VERDICT fields_hold=1`)" names a string the counter never
prints. The `expected.tsv` `c2-landing` row did not require it either, so the battery could not distinguish the
field-derived verdict from round 88's `all(ok)`.

**Narrowed property.** The verdict's field derivation is observed on the **failure** side, which is where it matters:
`M1-dead-teaches` prints `LEG_FAIL TEACHES checked=1 flagged=0` and `LEG_FAIL VERDICT fields_hold=0`, `M2`/`M3` print
`LEG_FAIL VERDICT fields_hold=0 legs_ok=8/8`, and `M4a` prints `fields_hold=0` where the leg alone would have passed.
On the passing path the observable is `CURATION_R89=PASS` with the eight measured fields. The claim does **not** assert
a printed `VERDICT` token on the passing path.

**Routed to round 90:** print `VERDICT fields_hold=1` in the summary (or move the leg before the summary) and require
it in the expectation row, so the observable the sentence names exists on both paths.

## Amendment 9 — C2 carries the same measurement-substitution limit C1 names; the finding is disclosed, not closed

**Finding.** `R89MutBattery` §C2: two single-expression counter edits remove the verbatim-locate detector
(`norm(quote) in cap` forced true) and the `UNENTAILED` detector (the term scan forced empty) while every printed
field stays honest — `QUOTES_LOCATED=20/20`, `WARRANT_OK=17/17`, `UNENTAILED_TERM=0` — so `fields_hold` holds, the
`VERDICT` leg agrees, and none of the three detectors (`mutants`, `controls`, the field derivation) notices. §C1
reports the same family on the battery side: a tool-mutant ledger credited without running, and an unreach rule
narrowed to exactly `203` whose literal is kept (so `build_mutant` still finds it).

**Narrowed property.** C2's sentence claims the **verdict** follows the printed fields, and that is what it
guarantees: a dead *detector* that leaves a field visibly wrong (`TEACHES_FLAGGED=0`, `TEACHES_UNRESOLVED=1`) cannot
pass. It does **not** claim that every detector is exercised against a substituted measurement — a detector replaced by
a constant that prints honest values is invisible to any field-derived verdict, exactly as C1's named limit 3 says
for the battery (`moved=0` and a `PASS` line cannot distinguish a correct measurement expression from a substituted
one). This is C1 limit 3 restated for C2, and it belongs in C2's named-limit set rather than being argued away.

**Disposition.** Reported as the round's principal routed debt in the report, with the mutants' survivor class named:
round 90's counters add a per-detector positive control (a tree where the detector *must* fire and the field must move)
so a constant-substituted detector is caught by a witness rather than by a field.
