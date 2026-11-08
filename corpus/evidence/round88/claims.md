# chousa — round 88 frozen claims

L1 `ChousaR88`. Base `f484d94f` (round-87 landing + its non-author spot-check, whose four routed defects are this
round's input). Frozen before any scored run of the round-88 candidates; the pre-freeze controls are committed beside
this file (`controls/receipts/`), their independent expectations in `controls/expected.tsv`, and the instrument bytes
are pinned in `instrument-pins.txt`.

Round shape: two claims, two distinct axes, one of them the lowest scored non-retired axis (operability, historical
3/10). No claim is exploratory.

## C1 `C1-BATTERY-R88` — operability (capability acquisition + repair)

**Sentence (what verifies).** The round-88 successor battery makes the 203 class *every* committed refetch row with
`http` exactly `203` in both independent derivations, and accounts its verdict by re-reading each leg's own receipt
file and reconciling it: at the landing revision it prints `D1_EXPECTED=3 D1_FORGES=3 D1_REFUSED=3/3 D2_FORGES=3
D2_REFUSED=3/3`, derives both mutant tools from the subject tool's own bytes and kills each
(`MUT_ADMIT_KILLED=1 MUT_UNREACH_KILLED=1`), refuses every generated forgery with its expected code
(`FORGED_REFUSED=EXPECTED_CODE=362`), and reports `LEG_REREAD=15/15 RECONCILED=15/15 LEGS_APPENDED=15`. So a counter
that narrows the class to one record, deletes a leg, credits a mutant it never built, detaches a leg's `ok`
expression from its measurement, or narrows both width derivations together fails the predicate instead of passing
on printed fields.

**Predicate.** `GATE_RECORDS_R88=PASS` (exit 0) printed by
`corpus/evidence/round88/gate-records-r88.py --root DIR --repo GITDIR [--tool PATH] --work DIR`, with all of
`TOOL=present`, `POSITIVE=15/15`, `FRESH_POSITIVE=5/5`, `FORGED_REFUSED` equals `EXPECTED_CODE` equals the generated
total, `EMPTY_REFUSED=1/1`, `RC=4/4`, `SETUP=1/1`, `D1_EXPECTED=3`, `D1_FORGES=3`, `D1_REFUSED=3/3`, `D2_FORGES=3`,
`D2_REFUSED=3/3`, `MUT_ADMIT_DERIVED=1`, `MUT_ADMIT_KILLED=1`, `MUT_UNREACH_DERIVED=1`, `MUT_UNREACH_KILLED=1`,
`DERIVE_NEG=1`, `LEG_REREAD=15/15`, `RECONCILED=15/15`, `LEGS_APPENDED=15`.

**Counting command.**

```sh
S=$(mktemp -d -p /fast/scratch/hyaku) && git -C /home/vgpnk/Projects/shokunin/chousa-shokunin archive <rev> | tar -x -C "$S" \
  && python3 -B "$S/corpus/evidence/round88/gate-records-r88.py" --root "$S" --repo /home/vgpnk/Projects/shokunin/chousa-shokunin --work "$S"
```

**Kill rules.**

- **K1** the predicate is not met at the landing revision.
- **K2** any in-class forged record is accepted, or is refused with a code outside its frozen expected set — the two 203
  classes (`D1-203-admit`, `D2-203-reject`) expect `REFETCH`.
- **K3** harm: a genuine committed record that the pre-round-88 tool accepts is refused at landing; the 15 frozen and 5
  fresh positives stay OK and the committed `GATE-RECORD` lines move no verdict (`controls/receipts/c1-harm.txt`).
- **K4** a mutant is not derived from the subject tool's bytes, or is credited without being run, or a leg's `ok`
  value is detached from its measured detail, while the frozen predicate still prints `PASS`; and a repair made after
  scoring does not rescue.

**Named limit (reported, not claimed away).** A counter edit that jointly rewrites the leg writer, the receipt files
and the reconciliation survives — that edit *is* the counter, not a leg misreport. `DERIVE_NEG`, the do-nothing
control and the wave's mutation seat are the cover; a wave finding on this class is reported, not argued away.

**Source.** `S216` (RFC 9110 §15.3.4, re-opened round 87 and cited here through the round-87 claims file):
"the request was successful but the enclosed content has been modified from that of the origin server's 200 (OK)
response" — the body is not the origin's (D1) and the response is not a failed transfer (D2).

**Before (committed controls).** `controls/receipts/c1-k0-donothing.txt`: the round-88 battery pointed at the
pre-round-88 tool … plus the round-87 battery, which cannot bind the class to 203 (its derivations accept non-200).
Measured at the freeze below.

## C2 `C2-CURATION-R88` — calibration

**Sentence (what verifies).** The round-88 curation counter closes the four round-87 routed instrument defects: the
warrant leg requires *every* named qid to resolve to a located quote that shares a distinctive content word with the
row's own cells (a padding qid fails); the floor leg requires per entry the pinned qid set and a per-row token
floor at the measured minimum (a one-word junk substitution and a count restored by a relabelled duplicate fail);
the `TEACHES` leg requires every flagged row to be disposed by a `mined` superseding row whose own `teaches` reads
in its own capture (a rejected superseder fails). At the landing revision it prints
`SUPERSEDED_LIVE=0 UNENTAILED_TERM=0 MODIFIED_DEF_CITED=1 QUOTES_LOCATED=20/20 WARRANT_OK=17/17 TEACHES_CHECKED=1
TEACHES_FLAGGED=1 TEACHES_UNRESOLVED=0 LEGS=7/7`, and it refuses all five round-87 forgeries the round-87 counter
accepted.

**Predicate.** `CURATION_R88=PASS` (exit 0) printed by `corpus/evidence/round88/curation-r88.py --root DIR`, with the
fields above and `LEGS=7/7`.

**Counting command.**

```sh
python3 -B corpus/evidence/round88/curation-r88.py --root /home/vgpnk/Projects/shokunin/chousa-shokunin
python3 -B corpus/evidence/round88/curation-r88-controls.py --root /home/vgpnk/Projects/shokunin/chousa-shokunin --work DIR
```

**Kill rules.**

- **K1** the predicate is not met at the landing revision.
- **K2** a quote counted as located is not verbatim (whitespace-normalized, curly quotes folded) in the committed
  capture of the registry row's own URL.
- **K3** a control forgery the round-87 counter accepted is still accepted (A1c junk-substitute, A1d truncate,
  caseG relabel, F2 rejected-superseder, B1b padding-qid) — `FORGERY_REFUSED=5/5` is part of the claim, not
  evidence beside it.
- **K4** the `TEACHES` leg is satisfied by flagging nothing (a dead detector): the leg requires at least one flagged
  row and a named disposition for it, and the disposition's superseder is `mined`.

**Sources.** `S216` and `S218` (own-work: `corpus/QUALITY.md` criterion 178 + `CORPUS.md` rule 2, the contract the
`TEACHES` leg enforces — a superseded row's frozen `teaches` is not evidence), both through the round-87 claims
file; `S215` (the PROV-O document) for the repaired warrant row, whose `Q3` quote is dropped because it shares no
term with the row.

**Before (committed controls).** `controls/receipts/c2-controls.txt`: `FORGERY_REFUSED=5/5 R87_ACCEPTED_FORGERY=5/5` —
each forgery is refused by `curation-r88.py` with a named `LEG_FAIL` and accepted by the frozen `curation-r87.py`.
`controls/receipts/c2-d0-donothing.txt`: the round-87 counter on the round-88 tree prints `CURATION_R87=PASS` — the
prior instrument has no leg of the four new classes.

## Frozen floors and non-negotiable bytes

- Instrument bytes: the two counters, the three control batteries and `c1-positives.tsv` are pinned in
  `instrument-pins.txt`; they are committed in the same commit as this file and are not edited after the first scored
  run. The subject tool `tools/gate-records.py` is unchanged this round (the round-87 unreach repair stands).
- `FORGED_REFUSED`/`EXPECTED_CODE` and all leg tallies are derived at run time, not pinned, so a repair cannot be
  scored against a number chosen after the fact; the estate's composition is pinned by `c1-positives.tsv` and the
  builders.
- `ROWS_203 = 3`, `MIN_TOKENS = 7` and the per-entry qid sets are the measured base counts, frozen in the counters
  themselves; a revision that moves them is a new claim, not an amendment.
- Neither claim is narrowed after landing: a miss is an honest stop.
