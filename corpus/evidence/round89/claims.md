# chousa — round 89 frozen claims

L1 `ChousaR89`. Base `f8fa55ec` (round-88 landing + its non-author spot-check
`corpus/lessons/round-88-verifier-spotcheck.md`, whose routed defects 1–8 are this round's input; 2, 3, 4, 5 and 6
are the instrument repairs below, 1 is the `claims.json` layout, 7 is a seat-discipline note and 8 is
operator-owned). Frozen before any scored run of the round-89 candidates; the pre-freeze receipts are committed beside
this file (`controls/receipts/`), their expectations in `controls/expected.tsv`, the receipt-vs-expectation driver in
`controls/run-controls.sh`, and the instrument bytes are pinned in `instrument-pins.txt`.

Round shape: two claims, two distinct axes, one of them the lowest scored non-retired axis (operability, historical
3/10). No claim is exploratory. No new instrument ground is claimed: both counters are successors of the round-88
bytes and the claim is what they now enforce.

## C1 `C1-BATTERY-R89` — operability (the lowest scored non-retired axis)

**Sentence (what verifies).** `corpus/evidence/round89/gate-records-r89.py` prints `GATE_RECORDS_R89=PASS` (exit 0)
at the landing revision with `RECONCILED=16/16 CROSSCHECK=15/15 LEGS_APPENDED=16` and every round-88 field unchanged
(`POSITIVE=15/15 FRESH_POSITIVE=5/5 FORGED_REFUSED=EXPECTED_CODE=362/362`, `D1_REFUSED=3/3`, `D2_REFUSED=3/3`,
`MUT_ADMIT_KILLED=1`, `MUT_UNREACH_KILLED=1`, `DERIVE_NEG=1`). Each leg's own receipt detail is re-derived **in its
own grammar** — an `n/m` detail requires `n == m`; a `len/d1/div3 pinN` width detail requires all four numbers equal
and `pin == ROWS_203`; a `derived=x killed=y` mutant detail requires both `x` and `y` to be 1; `tool present`
requires the subject tool to be a file — and each leg's re-derived numbers must equal the fields the summary line
printed for it (`DIV3` is printed for exactly this reason). `mutate-r89.py` then prints
`MUTANTS_KILLED=11/11 TOOL_MUTANTS_CAUGHT=2/2`: the four shapes the round-88 wave left alive — a detached `ok` over a
narrowed third width derivation, over zeroed mutant measurements, over a forged width detail, and a printed field
detached from its measurement — each die with a named `UNRECONCILED` or `UNCROSSCHECKED` line, and both subject-tool
mutants are caught.

**Predicate.** `GATE_RECORDS_R89=PASS` (exit 0) printed by
`corpus/evidence/round89/gate-records-r89.py --root DIR --repo GITDIR [--tool PATH] --work DIR`, with
`LEG_REREAD=16/16 RECONCILED=16/16 CROSSCHECK=15/15 LEGS_APPENDED=16` and the round-88 field set above; plus
`MUTANTS_KILLED=11/11 TOOL_MUTANTS_CAUGHT=2/2 TOTAL=13/13` from
`corpus/evidence/round89/mutate-r89.py --root DIR --repo GITDIR --work DIR`.

**Counting command.**

```sh
L=/home/vgpnk/Projects/shokunin/chousa-shokunin; W=/fast/scratch/hyaku/chousa-r89/c1
mkdir -p "$W" && python3 -B "$L/corpus/evidence/round89/gate-records-r89.py" --root "$L" --repo "$L" --work "$W"
python3 -B "$L/corpus/evidence/round89/mutate-r89.py" --root "$L" --repo "$L" --work "$W"
python3 -B "$L/corpus/evidence/round89/harm-recheck.py" --root "$L" --repo "$L" --base-tool "$W/base-tool.py"   # moved=0
```

**Kill rules.**

- **K1** the predicate is not met at the landing revision.
- **K2** any listed mutant survives, or any subject-tool mutant is not caught, or a generated forgery is accepted or
  refused with a code outside its frozen expected set.
- **K3** harm: a genuine committed `GATE-RECORD` line moves verdict (`moved` > 0), or a frozen/fresh positive is
  refused.
- **K4** the predicate is met by an instrument that skips the claimed work: an echo/printer replacement (the
  instrument sha256 pins in `instrument-pins.txt` are the check), a leg whose `ok` is detached while its receipt
  detail still records the measurement, or a summary field that disagrees with the leg it summarises.

**Named limits (reported, not claimed away).**

1. A counter edit that jointly rewrites the leg writer, the receipt files and the reconciliation survives — that
   edit *is* the counter. `mutate-r89.py`'s `E7d` shows the boundary from the outside: forging both the detail and
   the `ok` coherently is caught only because the summary still carries the measured `DIV3`; forging that too is a
   joint rewrite.
2. `TOOL` has no numeric witness: its re-derivation is the filesystem (`os.path.isfile(tool)`), not a number. A
   tree where the tool is absent skips the whole measurement block and fails on `LEG_REREAD`, which is the
   structural guard the round-88 reviewer measured.
3. The reconciliation guards *agreement between a receipt and its own detail*, not the truth of the measurement
   expression that produced both. A leg computed from a wrong constant and printed honestly passes — that is a
   different class (the round-87 `E5` family), and the report says so.

**Source.** `S216` (RFC 9110 §15.3.4), re-opened this round from the committed capture
`corpus/captures/b1b13a12aee75c6ecc20fb91.txt`: "indicates that the request was successful but the enclosed content
has been modified from that of the origin server's 200 (OK) response" (22 words). A 203 is a success, which is why
the two 203 classes must be bound to `203` and refused in both the admit and the unreach direction.

**Before (committed controls).** `controls/receipts/c1-prior-instrument.txt`: the round-88 battery passes on this
tree (`GATE_RECORDS_R88=PASS`) and prints no `CROSSCHECK` field, so it cannot express the guard — the do-nothing
control. Non-vacuity is carried by `controls/receipts/c1-mutants.txt`, which contains the four round-88 survivor
shapes dying on the new lines.

## C2 `C2-CURATION-R89` — calibration

**Sentence (what verifies).** `corpus/evidence/round89/curation-r89.py` prints `CURATION_R89=PASS` (exit 0) at the
landing revision with nine legs, `DUP_QIDS=0`, `WARRANT_OK=17/17`, `QUOTES_LOCATED=20/20`,
`TEACHES_FLAGGED=1 TEACHES_UNRESOLVED=0`, `SUP_CLAUSE_CHECKED=0 SUP_UNRESOLVED=0`, and its verdict computed from the
fields the summary printed (`VERDICT fields_hold=1`) rather than from a separate `all(ok)`; the control battery
prints `CONTROLS=PASS FORGERY_REFUSED=7/7 PRIOR_ACCEPTED_FORGERY=7/7` — the five round-87 classes still refused (prior
counter r87) plus two classes the round-88 counter accepts: a warrant cell citing `Q1, Q1` (one qid counted twice) and
a superseder carrying a contrast phrase and a date term absent from its own capture; and `curation-r89-mutants.py`
prints `MUTANTS_KILLED=6/6`, five through the counter's field-derived verdict and the clause-death mutant through the
battery's mirror.

**Predicate.** `CURATION_R89=PASS` (exit 0) with the fields above; `CONTROLS=PASS FORGERY_REFUSED=7/7
PRIOR_ACCEPTED_FORGERY=7/7`; `MUTANTS_KILLED=6/6`.

**Counting command.**

```sh
L=/home/vgpnk/Projects/shokunin/chousa-shokunin; W=/fast/scratch/hyaku/chousa-r89/c2
mkdir -p "$W"
python3 -B "$L/corpus/evidence/round89/curation-r89.py" --root "$L"
python3 -B "$L/corpus/evidence/round89/curation-r89-controls.py" --root "$L" --work "$W"
python3 -B "$L/corpus/evidence/round89/curation-r89-mutants.py" --root "$L" --work "$W"
```

**Kill rules.**

- **K1** the predicate is not met at the landing revision.
- **K2** any of the seven battery forgeries is accepted at landing, or a quote counted as located is not verbatim
  (whitespace-normalised, curly quotes folded) in the committed capture of its row's own URL.
- **K3** harm: the two admitted entries' verdicts move, the registry diff is anything but the two `used-by` cell
  changes logged old→new in the round lesson, or a designed control mirror that should pass is refused (blanket
  refusal is not a gain).
- **K4** the counter prints PASS over its own honestly-printed failure fields: a dead detector
  (`TEACHES_FLAGGED=0`), a detached leg (`TEACHES_UNRESOLVED=1` beside `PASS`), or a verdict that no longer follows
  from the printed tallies.

**Named limits (reported, not claimed away).**

1. `MIN_TOKENS = 7` is a measured floor, not a content check: a ≥7-token verbatim substitution that shares a
   distinctive term still passes (`R88ExecC2Forge` findings 1–2, unchanged by this round and so disclosed).
2. The qid-set pin guards label identity, not content: swapping the quote texts under two pinned qids passes
   (`R88ExecC2Forge` finding 4). A content oracle would need a second copy of the entry, which is the entry itself.
3. Row reorder passes (`finding 5`) — benign, reported, not claimed.
4. The superseder-own-read clause is **vacuous on the real registry** (`SUP_CLAUSE_CHECKED=0`: no superseding row
   names a date term). Its non-vacuity is the battery's `SUP-clause-mirror`, which the round-88 counter accepts and
   this one refuses with `sup_unresolved=1 unresolved=0`. A vacuous leg plus a measured mirror is the honest shape;
   claiming the clause fires on real rows would be false.

**Sources.** `S218` (own-work: `corpus/QUALITY.md` criterion 178 + `CORPUS.md` rule 2 — the contract the `TEACHES`
and superseder legs enforce), re-opened this round at `corpus/QUALITY.md:1120`; `S216` as above for the record-form
discipline shared with C1.

**Before (committed controls).** `controls/receipts/c2-prior-instrument.txt` (`CURATION_R88=PASS` on this tree, no
`DUPQID` leg, no field-derived verdict) and `controls/receipts/c2-controls.txt`
(`PRIOR_ACCEPTED_FORGERY=7/7`).

## Frozen floors and non-negotiable bytes

- Instrument bytes: `gate-records-r89.py`, `curation-r89.py`, `mutate-r89.py`, `curation-r89-controls.py`,
  `curation-r89-mutants.py`, `harm-recheck.py`, `controls/expected.tsv`, `controls/run-controls.sh` and
  `c1-positives.tsv` are pinned in `instrument-pins.txt`; they are committed in the same commit as this file and are
  not edited after the first scored run.
- The subject tool `tools/gate-records.py` is unchanged this round (sha256 `905f9da2…` at base and landing), so the
  203 binding and the unreach repair stand unmodified; C1 changes only the battery that measures them.
- `ROWS_203 = 3`, `MIN_TOKENS = 7`, the per-entry qid sets and the pinned `FLOORS` are the measured base values,
  frozen in the counters themselves; a revision that moves them is a new claim, not an amendment.
- Neither claim is narrowed after landing: a miss is an honest stop.
