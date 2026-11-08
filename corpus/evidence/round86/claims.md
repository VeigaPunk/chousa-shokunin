# chousa — round 86 frozen claims

L1 `ChousaR86`. Base `3bfb6885958ad4a674ad1896f70d1e836be609e4` (lane tip at round start). Frozen before any scored
run of the round-86 candidates; the pre-freeze controls are committed beside this file
(`controls/receipts/`), and the instrument bytes are pinned in `instrument-pins.txt`.

Round shape: two claims, two distinct axes, one of them the lowest scored non-retired axis (operability, historical
3/10). No claim is exploratory.

## C1 `C1-BATTERY-R86` — operability (capability acquisition + repair)

**Sentence (what verifies).** The round-86 successor battery generates the round-85 `D1` class (an admit record whose
stored body arrived under HTTP 203, built from the committed `S021` PubMed refetch row and its capture) *inside* the
frozen predicate, and computes the round-85 `M17` mutant from the subject tool's own bytes: the subject tool refuses
the `D1` record with `REFETCH`, and the derived mutant — REFETCH success relaxed back to `2xx` — accepts every positive
and the `D1` record, so the battery kills it instead of surviving it. The round-85 estate (15 frozen positives, 5 fresh
positives, the forged battery, the empty-file leg, the non-git setup leg) is unchanged.

**Predicate.** `GATE_RECORDS_R86=PASS` (exit 0) printed by
`corpus/evidence/round86/gate-records-r86.py --root DIR --repo GITDIR [--tool PATH] --work DIR`, with all of:
`TOOL=present`, `POSITIVE=15/15`, `FRESH_POSITIVE=5/5`, `FORGED_REFUSED` equals `EXPECTED_CODE` equals the generated
total, `EMPTY_REFUSED=1/1`, `RC=4/4`, `SETUP=1/1`, `D1_FORGES=1`, `D1_REFUSED=1/1`, `MUT17_KILLED=1/1`.

**Counting command.**

```sh
S=$(mktemp -d -p /fast/scratch/hyaku) && git -C /home/vgpnk/Projects/shokunin/chousa-shokunin archive <rev> | tar -x -C "$S" \
  && python3 -B "$S/corpus/evidence/round86/gate-records-r86.py" --root "$S" --repo /home/vgpnk/Projects/shokunin/chousa-shokunin --work "$S"
```

**Kill rules.**

- **K1** the predicate is not met at the landing revision.
- **K2** any in-class forged record is accepted, or is refused with a code outside its frozen expected set — including
  the `D1` 203-body admit, whose expected code is `REFETCH`.
- **K3** harm: a genuine committed record that the pre-round tool accepts is refused at landing (the 15 frozen and 5
  fresh positive legs).
- **K4** the mutant leg is not derived from the subject tool's bytes (a counter that hard-codes a mutant, or that cannot
  derive one, prints `MUT17_KILLED=0/1`); and a repair made after scoring does not rescue.

**Source.** `S216` (RFC 9110 §15.3.4, opened this round): 203 means a transforming proxy modified the enclosed content
from the origin's 200 response, so a 203 body is not the origin's representation and cannot ground a registered quote.

**Before (committed controls).** `controls/receipts/c1-k0b-frozen-instrument.txt`: the round-85 counter prints
`FORGED_REFUSED=354/354 … SETUP=1/1` / `GATE_RECORDS_R85=PASS` with **zero** `D1-203-admit` or mutant lines in its
bytes (grep count 0) — the prior instrument cannot express the target. `controls/receipts/c1-k0-donothing.txt`: the
round-86 battery on the pre-round-85 tool (`2xx`) prints `D1_REFUSED=0/1 MUT17_KILLED=0/1 … GATE_RECORDS_R86=FAIL`,
exit 1.

## C2 `C2-CURATION-R86` — calibration

**Sentence (what verifies).** The two curation defects the round-85 non-author check routed are closed on committed
bytes: (a) no row that a later row supersedes is `mined` while the superseding row is not (the round-85 inversion
`S024` mined / `S031` queued is resolved by restoring `S024` to `queued` and mining `S031` as the r85 entry's cited
row); and (b) neither routed entry's decision-table cells carry the frozen defect terms (`modification`, `modified`)
without a located quote of that entry carrying them — the round-84 row 9 gains the `modified` Definition quote
("Date on which the resource was changed.", `S023` capture line 8786) as its warrant, and the round-85 row 6 drops the
comparison its source refuses.

**Predicate.** `CURATION_R86=PASS` (exit 0) printed by `corpus/evidence/round86/curation-r86.py --root DIR`, with
`SUPERSEDED_LIVE=0`, `UNENTAILED_TERM=0`, `MODIFIED_DEF_CITED=1`, and `QUOTES_LOCATED` equal to its total with the total
≥ 19 (the base count; the repair adds one).

**Counting command.**

```sh
python3 -B corpus/evidence/round86/curation-r86.py --root /home/vgpnk/Projects/shokunin/chousa-shokunin
```

**Kill rules.**

- **K1** the predicate is not met at the landing revision.
- **K2** a quote counted as located is not verbatim (whitespace-normalized, curly quotes folded) in the committed
  capture of the registry row's own URL.
- **K3** a repaired decision-table row's Do or Never states something its warrant quote neither states nor entails, or a
  sentence in the same source contradicts it (a non-author reviewer's finding).
- **K4** the round-84 repair's added quote is not from `S023`, or the round-85 entry cites the superseded `S024`
  instead of `S031`.

**Sources.** `S023` (DCMI Metadata Terms, re-opened this round, HTTP 200 at `2026-11-08T06:00:11Z`, capture
`f5545a194c06ab421875b047`, definition at line 8786) and `S031` (Schema.org `lastReviewed`, re-opened this round, HTTP
200 at `2026-11-08T06:00:10Z`, capture `11d6cc56bb24adfc61eea2b4`).

**Before (committed control).** `controls/receipts/c2-d0-donothing.txt`: on the base tree the counter prints
`SUPERSEDED_LIVE=1 UNENTAILED_TERM=2 MODIFIED_DEF_CITED=0 QUOTES_LOCATED=19/19` / `CURATION_R86=FAIL`, exit 1.

## Frozen floors and non-negotiable bytes

- Instrument bytes: the two counters and `c2-positives.tsv` are pinned in `instrument-pins.txt`; they are committed in
  the same commit as this file and are not edited after the first scored run. The subject tool
  `tools/gate-records.py` is unchanged this round (`sha256 fe204539…`), pinned for the record.
- `FORGED_REFUSED`/`EXPECTED_CODE` totals are derived (not pinned) so that a repair cannot be scored against a number
  chosen after the fact; the composition of the estate is pinned by `c2-positives.tsv` and the counter's own builder.
- Neither claim is narrowed after landing: a miss is an honest stop.
