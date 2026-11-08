# chousa — round 87 frozen claims

L1 `ChousaR87`. Base `6495ef88` (round-86 landing + its non-author spot-check, whose five routed defects are this
round's input). Frozen before any scored run of the round-87 candidates; the pre-freeze controls are committed beside
this file (`controls/receipts/`), their independent expectations in `controls/expected.tsv`, and the instrument bytes
are pinned in `instrument-pins.txt`.

Round shape: two claims, two distinct axes, one of them the lowest scored non-retired axis (operability, historical
3/10). No claim is exploratory.

## C1 `C1-BATTERY-R87` — operability (capability acquisition + repair)

**Sentence (what verifies).** The round-87 successor battery makes the 203 class *every* qualifying committed refetch
row instead of one, adds the reject-form 203 class, and accounts its verdict by counting executed legs: at the landing
revision it prints `D1_EXPECTED=3 D1_FORGES=3 D1_REFUSED=3/3 D2_FORGES=3 D2_REFUSED=3/3`, derives both mutant tools
from the subject tool's own bytes and kills each (`MUT_ADMIT_KILLED=1 MUT_UNREACH_KILLED=1`), refuses every generated
forgery with its expected code (`FORGED_REFUSED=EXPECTED_CODE=362`), and reports `LEGS=15/15`. So a counter that
narrows the class to one record, deletes a leg, or credits a mutant it never built fails the predicate instead of
passing on printed fields.

**Predicate.** `GATE_RECORDS_R87=PASS` (exit 0) printed by
`corpus/evidence/round87/gate-records-r87.py --root DIR --repo GITDIR [--tool PATH] --work DIR`, with all of
`TOOL=present`, `POSITIVE=15/15`, `FRESH_POSITIVE=5/5`, `FORGED_REFUSED` equals `EXPECTED_CODE` equals the generated
total, `EMPTY_REFUSED=1/1`, `RC=4/4`, `SETUP=1/1`, `D1_EXPECTED=3`, `D1_FORGES=3`, `D1_REFUSED=3/3`, `D2_FORGES=3`,
`D2_REFUSED=3/3`, `MUT_ADMIT_DERIVED=1`, `MUT_ADMIT_KILLED=1`, `MUT_UNREACH_DERIVED=1`, `MUT_UNREACH_KILLED=1`,
`DERIVE_NEG=1`, `LEGS=15/15`.

**Counting command.**

```sh
S=$(mktemp -d -p /fast/scratch/hyaku) && git -C /home/vgpnk/Projects/shokunin/chousa-shokunin archive <rev> | tar -x -C "$S" \
  && python3 -B "$S/corpus/evidence/round87/gate-records-r87.py" --root "$S" --repo /home/vgpnk/Projects/shokunin/chousa-shokunin --work "$S"
```

**Kill rules.**

- **K1** the predicate is not met at the landing revision.
- **K2** any in-class forged record is accepted, or is refused with a code outside its frozen expected set — the two 203
  classes (`D1-203-admit`, `D2-203-reject`) expect `REFETCH`.
- **K3** harm: a genuine committed record that the pre-round-87 tool accepts is refused at landing; the 15 frozen and 5
  fresh positives stay OK and the 27 committed `GATE-RECORD` lines across 10 lessons move no verdict
  (`controls/receipts/c1-harm-unreach.txt`).
- **K4** a mutant is not derived from the subject tool's bytes, or is credited without being run (a counter edit for
  which the frozen predicate still prints `PASS`); and a repair made after scoring does not rescue.

**Named limit (reported, not claimed away).** A counter edit that *executes* a leg and misreports its printed value
survives — the predicate binds the field the leg prints. `DERIVE_NEG`, the do-nothing control and the wave's mutation
seat are the cover; a wave finding on this class is reported, not argued away.

**Source.** `S216` (RFC 9110 §15.3.4, re-opened this round): "the request was successful but the enclosed content has
been modified from that of the origin server's 200 (OK) response by a transforming proxy" — the body is not the
origin's (D1) and the response is not a failed transfer (D2).

**Before (committed controls).** `controls/receipts/c1-k0-donothing.txt`: the round-87 battery pointed at the
pre-round-87 tool prints `D2_REFUSED=0/3 … MUT_UNREACH_DERIVED=0 LEGS=11/15` / `GATE_RECORDS_R87=FAIL`, exit 1.
`controls/receipts/c1-k0b-frozen-instrument.txt`: the round-86 battery prints `D1_FORGES=1` and no `D2_` field at all —
the prior instrument cannot express the target.

## C2 `C2-CURATION-R87` — calibration

**Sentence (what verifies).** The round-87 curation counter implements the two routed instrument duties: a per-entry
located-quote floor (13 and 7, the measured base counts) so a deleted or truncated quote table fails, and a
warrant-linkage leg requiring each decision-table row's named qid to resolve to a located quote that shares a
distinctive content word with the row's own cells — plus a registry-`teaches` leg that flags a row whose `teaches`
states a contrast against a date-property term its own capture never contains, and requires every flagged row to be
disposed as superseded. At the landing revision it prints
`SUPERSEDED_LIVE=0 UNENTAILED_TERM=0 MODIFIED_DEF_CITED=1 QUOTES_LOCATED=20/20 WARRANT_OK=17/17
TEACHES_FLAGGED=1 TEACHES_UNRESOLVED=0 LEGS=7/7`, and it refuses all four round-86 forgeries the round-86 counter
accepted.

**Predicate.** `CURATION_R87=PASS` (exit 0) printed by `corpus/evidence/round87/curation-r87.py --root DIR`, with the
fields above and `LEGS=7/7`.

**Counting command.**

```sh
python3 -B corpus/evidence/round87/curation-r87.py --root /home/vgpnk/Projects/shokunin/chousa-shokunin
python3 -B corpus/evidence/round87/curation-r87-controls.py --root /home/vgpnk/Projects/shokunin/chousa-shokunin --work DIR
```

**Kill rules.**

- **K1** the predicate is not met at the landing revision.
- **K2** a quote counted as located is not verbatim (whitespace-normalized, curly quotes folded) in the committed
  capture of the registry row's own URL.
- **K3** a control forgery the round-86 counter accepted is still accepted (E5b delete-one-row, E5c2 keep-two-rows, E6
  warrant-unlinked, T teaches-contrast) — `FORGERY_REFUSED=4/4` is part of the claim, not evidence beside it.
- **K4** the `TEACHES` leg is satisfied by flagging nothing (a dead detector): the leg requires at least one flagged
  row and a named disposition for it.

**Sources.** `S216` (re-opened above, grounding the two 203 classes) and `S218` (own-work, new this round: the lane's
own `corpus/QUALITY.md` criterion 178 + `CORPUS.md` rule 2, which is the contract the `TEACHES` leg enforces — a
superseded row's frozen `teaches` is not evidence).

**Before (committed controls).** `controls/receipts/c2-controls.txt`: `FORGERY_REFUSED=4/4 R86_ACCEPTED_FORGERY=4/4` —
each forgery is refused by `curation-r87.py` with a named `LEG_FAIL` and accepted by the frozen `curation-r86.py`.
`controls/receipts/c2-d0-donothing.txt`: the round-86 counter on the round-87 tree prints `CURATION_R86=PASS` — the
prior instrument has no leg of the three new classes.

## Frozen floors and non-negotiable bytes

- Instrument bytes: the two counters, the three control batteries and `c1-positives.tsv` are pinned in
  `instrument-pins.txt`; they are committed in the same commit as this file and are not edited after the first scored
  run. The subject tool `tools/gate-records.py` is modified by this round (the unreach repair) and its landing bytes are
  pinned in the same file.
- `FORGED_REFUSED`/`EXPECTED_CODE` and all leg tallies are derived at run time, not pinned, so a repair cannot be scored
  against a number chosen after the fact; the estate's composition is pinned by `c1-positives.tsv` and the builders.
- Neither claim is narrowed after landing: a miss is an honest stop.
