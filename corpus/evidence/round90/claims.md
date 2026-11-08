# chousa — round 90 frozen claims

L1 `ChousaR90`. Base `f54a45ed197dd475af50d82e43a22df3d2e99782` (round-89 landing + its non-author spot-check
`corpus/lessons/round-89-verifier-spotcheck.md`). This file is the prose form; `.ufo/waves/round-90/claims.json` is the
machine form the pre-file gate reads. A `narrowing` cell in `.ufo/waves/round-90/claim-falsification.tsv` resolves to a
section of `plans/round-90.md`.

The round's input is round 89's spot-check `## Routed defects` 1–7 and Amendment 7's control-driver package, plus
Amendment 8 (the unprinted `VERDICT` token), Amendment 9 (the constant-substituted-detector survivors) and the
Gate-standard item 5 (stale `SKILL.md` tallies).

## C1 — `C1-DRIVER-R90` (operability; the lowest scored non-retired axis, historical 3/10)

**Claim type.** Repair (successor control-receipt driver; the r89 instrument stays in the tree as the prior).

**Sentence (frozen).** At the landing revision

```
python3 -B corpus/evidence/round90/control-driver-r90.py verify --root . --repo . \
    --rev <freeze-rev> --receipts-rev <receipts-carrier-rev>
```

prints `CONTROL_DRIVER_R90=PASS` (exit 0) with `COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6` over the six
committed receipts under `corpus/evidence/round90/controls/receipts/`. For every row the driver (a) reads the
committed receipt before any fresh run and writes nothing under the receipts directory, (b) requires the receipt's
`# exit=` to equal the row's expected exit, (c) requires every required `K=V` value to equal one whole
whitespace-delimited body token — a token that starts with the key and differs is `TOKEN_DETACHED`, never a pass,
(d) requires every `key>=N` predicate (the harm row's `records>=1`), (e) refuses a required key carried twice with
different values (`DUPLICATE_KEY`), (f) requires `# computed_against=` to equal `--rev` and the scoring bytes to be
byte-identical to their blobs at the named carrier revisions, and (g) requires the instrument re-run into `--work`
to agree with the committed receipt. And

```
python3 -B corpus/evidence/round90/control-forgeries-r90.py --root . --work <scratch> --rev <freeze-rev>
```

prints `FORGERY_REFUSED=6/6 PRIOR_ACCEPTED=6/6 POSITIVE=pass` — the six forgery classes (`B2-substring`,
`B1-committed`, `B3-no-pin`, `B3b-stale-pin`, `B4-harm-vacuity`, `C-duplicate-key`) are each refused by the round-90
driver and each accepted by the unchanged round-89 driver on the same fixture; the positive fixture is accepted by
both.

**Before.** The round-89 driver (`corpus/evidence/round89/controls/run-controls.sh`) prints `CONTROL_RECEIPTS=PASS`
over its own rows, and on the six forgery fixtures it prints `FORGERY_REFUSED=0/6` in effect (all six accepted):
`corpus/evidence/round90/controls/receipts/c1-prior-driver.txt` and the forgery battery's `prior rc=0` lines.
Spot-check evidence: `corpus/lessons/round-89-verifier-spotcheck.md` §Amendment 7 B1–B4.

**Counting command.** The two commands above; the driver's `emit` mode generated the committed receipts and is not
part of the scored path.

**Kill rules.** K1 the predicate is not met at the landing revision. K2 a forgery class is accepted by the round-90
driver, the positive fixture is refused, or the round-89 driver refuses a forgery (the fixture would then not prove
the prior state). K3 a genuine row is moved or silently rewritten by the verification path (any `RECEIPT … FINDING`
on the committed set, or a receipts-directory write). K4 the pass is reached without the work: a missing receipt
accepted (`MISSING_RECEIPT`), the committed receipt not read (verify is fresh-only), the token leg falling back to
substring matching, or the pin minted inside `verify` instead of carried by an emitted receipt.

**Named limits.** (1) The driver verifies a receipt/expectation pair: a coherent joint edit of the instrument, its
receipt and its expectation row survives — that edit is the harness. (2) Whole-token matching binds one field per
token, not its semantic role: a required token printed on an unrelated diagnostic line passes; only the C2 verdict
phrase uses the `line:` whole-line form. (3) The self-pin compares bytes at named revisions; it cannot detect a
rewritten history, only a moved byte inside the named commit.

**Sources.** S220 (GNU grep(1) `-x` whole-line match semantics, opened this round; the receipt driver's exact-token
rule is the same contract at the shell-token level).

## C2 — `C2-CURATION-R90` (calibration)

**Claim type.** Repair (successor curation counter; the round-89 counter stays in the tree as the prior).

**Sentence (frozen).** At the landing revision `python3 -B corpus/evidence/round90/curation-r90.py --root .` prints
`CURATION_R90=PASS` (exit 0) with `LEGS_MEASURED=10/10`, an output line containing `VERDICT fields_hold=1`, and
`DETECTOR_WITNESS=8/8`, plus the carried fields `DUP_QIDS=0 WARRANT_OK=17/17 QUOTES_LOCATED=20/20 TEACHES_FLAGGED=1
TEACHES_UNRESOLVED=0 SUP_CLAUSE_CHECKED=0 SUP_UNRESOLVED=0`. The verdict leg is appended before the summary line, so
the passing path prints the token pair round 89's Amendment 8 said was unprinted. The `VERDICT` leg is part of the
leg set the summary counts (`LEGS_MEASURED=10/10`) and `passed` requires every leg ok, so the printed line and the
verdict are the same measured value. `curation-r90-mutants.py --root . --work <scratch>` prints `MUTANTS_KILLED=10/10 COUNTER_DETECTED=9
BATTERY_DETECTED=1 PRIOR_R89_SURVIVORS=2/2`: the two constant-substituted detectors that survived round 89
(`locates` forced true; `unentailed_row` forced false) are SURVIVORS against the round-89 counter and die against the
round-90 counter on `LEG_FAIL WITNESS`. `curation-r90-controls.py --root . --work <scratch>` prints `CONTROLS=PASS
FORGERY_REFUSED=7/7 PRIOR_REGRESSION=7/7` (the seven tree-forgery classes stay refused).

**Before.** `corpus/evidence/round89/curation-r89.py` on the same tree prints `CURATION_R89=PASS` with
`LEGS_MEASURED=8/8` and no `VERDICT fields_hold=1` token on the passing path (`grep -c 'VERDICT fields_hold=1'` → 0),
and the two substitutions applied to its bytes print `CURATION_R89=PASS` (survivors): receipts
`controls/receipts/c2-prior-landing.txt`, `controls/receipts/c2-subst-before.txt`.

**Counting command.** The three commands above.

**Kill rules.** K1 the predicate is not met at the landing revision. K2 a listed mutant survives, the positive mirror
is refused, or a tree forgery is accepted. K3 harm: a curated entry's verdict moves, or the registry diff exceeds the
S220 row plus its `used-by` cell. K4 the verdict or witness is satisfied by constants rather than the detector bodies
(the mutant battery is the detector: any forced detector body must fail `WITNESS`, which it does for four of them and
for the two round-89 survivors).

**Named limits.** (1) `MIN_TOKENS=7` is a measured floor, not a content check. (2) The qid-set pin guards label
identity, not quote content. (3) The witness exercises each detector function on synthetic strings; a substitution in
a *caller* that bypasses the function is not witnessed. (4) The superseder-own-read clause is vacuous on the real
registry (`SUP_CLAUSE_CHECKED=0`); its non-vacuity is the battery's mirror case.

## C3 — `C3-TALLY-R90` (freshness)

**Claim type.** Repair (Gate-standard registry freshness, routed defect 5).

**Sentence (frozen).** At the landing revision `python3 -B corpus/evidence/round90/skill-tally-r90.py --root .` prints
`SKILL_TALLY_R90=PASS` (exit 0) with `TALLY_ROWS=9 STALE_TALLIES=0/9 EXPECTED_CASES=283 EXPECTED_SKIPPED=0
OTHER_OCCURRENCES=3`: every **current** `PASS (<n> cases, <m> skipped)` tally in `SKILL.md` — the eight Gates-table
rows whose first cell names `research-gate`, plus the `Selftest` statement at the skill's host note — re-derives to the
subject tool's own printed selftest verdict. The three historical occurrences (round-25/32/34/37 quotes) are counted
as `OTHER_OCCURRENCES` and are not bound.

**Before.** The same command prints `STALE_TALLIES=9/9` with `EXPECTED_CASES=283`, because all nine rows still read
`PASS (275 cases, 0 skipped)`; receipt `controls/receipts/c3-before.txt`.

**Counting command.** `python3 -B corpus/evidence/round90/skill-tally-r90.py --root .` (it runs
`bash tools/research-gate.sh --selftest` itself; a captured receipt can be passed with `--selftest`).

**Kill rules.** K1 the predicate is not met at the landing revision. K2 the check passes with no tally row, or it
matches the file against a stale number instead of the tool's own live verdict line. K3 harm: `SKILL.md` moves
outside the tally cells and the one case-range note (diff reviewed at landing).

**Named limits.** (1) The check binds the two numbers in each current cell; it does not verify that cases 276–283 are
the `bash-pin-override-*` cases the note names, nor any other prose in the Gates table. (2) Historical occurrences are
recognised by shallower structure than the binding rule (they are simply not in the Gates table and do not carry the
host note's `Selftest` phrase); a historical line rewritten to look current would be bound and must then also re-derive.
