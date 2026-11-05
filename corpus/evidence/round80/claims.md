# Round-80 frozen claims — chousa

Frozen before any seat scored, at the claims-freeze commit named in the round report. Base
revision: `b7803829922770b890e9f4efdd30d12c3695439a` (round-79 lane tip, closed `ok` /
`rejected-honest-stop` by the non-author spot-check at `corpus/lessons/round-79-verifier-spotcheck.md`).
Two claims, two axes, causally separable: C1 changes the battery (operability), C2 changes the
gate-record audit (calibration). Each is verifiable without the other having landed.

## Instruments (sha256 of the committed bytes at the freeze commit)

| instrument | sha256 |
|---|---|
| `corpus/evidence/round80/matrix-battery-v7.py` | `35351b2328bb6a284da13e61240a6ec598f39a148b8d8948d4e3d60dd78d914d` |
| `corpus/evidence/round80/oracle-check.py` | `580233adaa1cf23b3a24012d05d7e5a2e313f7f4628d382f245433117c5e0289` |
| `corpus/evidence/round80/gate-grounding-check.py` | `d9e426216665a098cd90adf8fbf5e5dd62e02dc7b5b707c322b404b3eb55c553` |
| `corpus/evidence/round80/forgers/a10-payload-decode.py` | `3cb234be36a3d0d5d5523f16e5b7bb6926bbd0be8d0701d6229f0d8690ca9f64` |
| subject battery (predecessor, unchanged) `corpus/evidence/round79/matrix-battery-v6.py` | `bb91406e9130d9a1960d99226c69380435fc933385db79e0e6ea6b5542a61e1d` |
| matrix under test `corpus/evidence/round76/loader-matrix-v3.py` | `b79d6441057a01b27eb465c6b0625cd46502114f8b622b370c2cd2805c81913f` |

## C1 — operability (lowest scored non-retired axis; the historical 3/10 is held)

**Claim.** The round-79 battery accepted a matrix that identifies subjects without scoring them:
the committed structure-identity matrix reaches `BATTERY=PASS` on v6. v7 draws its subject set per
run — `--fresh N` semantics-preserving rewrites (fresh positives) and semantics-altering mutations
(fresh forgers) of the two committed positives, ground-truthed by the committed witness matrix — and
scores that drawn set with the matrix under test **and** with every enumerated oracle, so an oracle
whose table was built from committed bytes cannot reach the PASS line.

**Before (do-nothing control, committed).**
`corpus/evidence/round80/controls/oracle-structure-v6-accepted.txt`:
`python3 -B corpus/evidence/round80/oracle-check.py --battery corpus/evidence/round79/matrix-battery-v6.py
--oracle .ufo/waves/round-79/w1/R79ExecC/matrix-structure-identity.py --work DIR --runs 1`
→ `BATTERY_EXIT=0 BATTERY_VERDICT=PASS RECEIPT_LINES=113`, `ORACLE=ACCEPTED`, exit 1.

**Counting command (after).**

```
python3 -B corpus/evidence/round80/matrix-battery-v7.py \
  --matrix corpus/evidence/round76/loader-matrix-v3.py --work DIR --runs 1 --fresh 2 --rev REV
```

**Predicate (one sentence, same in the report, the SCORECARD row and the receipt label).** The
command exits 0 and prints exactly
`BATTERY=PASS forgers_rejected=11/11 positive=2/2 fresh_positive=2/2 fresh_forgers=2/2 oracles_rejected=5/5`.

**Kill rule (enumerates exactly the set the predicate counts).** The claim does not verify if the
predicate line claims PASS while any of the eleven named committed forgers, the two named committed
positives, the two drawn fresh positives, the two drawn fresh forgers or the five enumerated oracles
(the three committed forged matrices, the round-79 structure-identity matrix, the round-79
payload-decode forger) is a MISS, or if the legitimate matrix is refused (blanket refusal is not a
gain).

**Limits recorded, not claimed closed.** The fresh leg's ground truth is the committed witness
matrix, so a witness wrong about a case makes both legs wrong together; the eleven committed
forgers and the five oracles are the independent anchor. A classifier that knows this generator's
rewrite operators can still separate fresh positives from fresh forgers statically — measured by the
wave's critic and labrat seats, recorded in the lesson, never certified closed.

## C2 — calibration (sourced on S200)

**Claim.** Round 79's Gate records are prose that nothing re-opens: the non-author spot-check found
a 27-word quote stated as 25 (S196), a stated count off by one (S197) and a "located quote" absent
from the file it cites (S198). A machine-checkable `GATE-RECORD` line, re-opened by a counter that
reads only committed bytes at a named revision, resolves all three by append-only supersession.

**Before (do-nothing control, committed).**
`corpus/evidence/round80/controls/grounding-before.txt`:
`python3 -B corpus/evidence/round80/gate-grounding-check.py --rev b7803829922770b890e9f4efdd30d12c3695439a`
→ `GATE_GROUNDING=FAIL unresolved=3 superseded_resolved=0 audited=S196,S197,S198`, exit 1.

**Counting command (after).**

```
python3 -B corpus/evidence/round80/gate-grounding-check.py --rev REV
```

**Predicate.** The command exits 0 and prints `GATE_GROUNDING=PASS unresolved=0
superseded_resolved=3` with `audited=` listing `S199,S200,S201,S202`.

**Kill rule (enumerates exactly the checks the counter runs).** The claim does not verify if any
audited tip or superseded row resolves while R1 (the named revision does not resolve), R2 (the named
path is absent at that revision), R3 (the named line does not contain the quote) or R4 (the quote's
word count disagrees with the record, or exceeds 25) fails; or if the counter reports `unresolved=0`
while a `GATE-RECORD` line names bytes it never opened.

## Sourced claims

C1's evidence cites **S199** (own-work A: the round-79 structure-identity receipts, opened this
round). C2's landing cites **S200** (own-work B: QUALITY criterion 147's opening sentence at
`b7803829`, the corrected 15-word located quote that supersedes S196). Both rows carry a
`GATE-RECORD` line in `corpus/lessons/round-80.md`.
