# Round 40 — frozen claim design

Lane: chousa (deep-research method). Round: 40. Attempt: 1.

Frozen before round-40 correction work and receipt regeneration. A later change to this file is an appended erratum; the body and predicates below stay unchanged.

## C1 — operability (lowest scored axis: 3/10)

**Claim.** The six selected active round-39 evidence receipts verify against the committed gate, counter, verifier, and expectation bytes. This repairs the R1 stale `expect_sha256` receipts without rewriting their committed originals: three replacement receipts are issued under `corpus/evidence/round40/receipts/`; the old files remain preserved. The active population is frozen in `active-r39-receipts.tsv`.

**P1 (frozen predicate).** C1 is met iff `python3 corpus/evidence/round40/c1-count.py` prints `R39_ACTIVE_RECEIPTS=6/6` and exits 0. Code condition: every row in the six-row active manifest returns a line beginning `VERIFY: ok`; a missing receipt or any verifier refusal is a miss.

**Cheapest do-nothing control.** Run the frozen counter against the committed r39 tree before issuing the three replacement receipts. The six-row manifest names the three intended replacements, which are absent in the control; the three existing verified receipts are the c1-after-s39111 and two c2 receipts. The control is expected below 6/6 and must be recorded before data.

**Before (observed control).** At lane tip `691d26476ac39b8ec8b65155b41199e6f6d1f299`, `python3 corpus/evidence/round40/c1-count.py` produced `R39_ACTIVE_RECEIPTS=3/6`, exit 1; three frozen replacement paths were absent. Exact output is committed at `.ufo/waves/round-40/controls/control-before.txt`.

**After.** Pending re-derivation after all three replacements are committed.

**Kill rule.** Any active receipt fails the committed verifier, any active manifest row is missing/duplicated, or the counter's population differs from six; the claim does not pass. The four superseded originals remain outside the active population and are dispositioned under C2.

## C2 — calibration (R2–R5 closure alignment)

**Claim.** The four round-39 closure findings R2–R5 each receive an evidence-backed disposition in `routed-defect-dispositions.json`: R2/R3/R5 are corrected; R4 is explicitly marked not reproduced if the committed round-39 spec, validator plan, and report agree against the spot-check's contrary role counts. The counter must re-derive these states from the committed evidence, not count prose labels alone.

**P2 (frozen predicate).** C2 is met iff `python3 corpus/evidence/round40/c2-count.py` prints `R39_CALIBRATION_DISPOSITIONS=4/4` and exits 0. The R4 code condition requires exact role-count agreement among the committed spec, validator plan, and report, while the spot-check's contrary statement remains cited.

**Cheapest do-nothing control.** Run the frozen counter before adding the disposition record and round-40 corrections; it must return below 4/4. If it does not, redesign before accepting any correction.

**Before (observed control).** At lane tip `691d26476ac39b8ec8b65155b41199e6f6d1f299`, `python3 corpus/evidence/round40/c2-count.py` produced `R39_CALIBRATION_DISPOSITIONS=0/4`, exit 1; exact output is committed at `.ufo/waves/round-40/controls/control-before.txt`.

**After.** Pending re-derivation after the disposition record, append-only corrections, and scorecard text are committed.

**Kill rule.** Any defect disposition is absent, contradicts its cited committed source, or is unsupported by the counter's checks. R4 must not be changed to a positive “fixed” label while its cited spec/plan/report agree.

## Separability

C1 changes only the receipt evidence set and its active-manifest verification; its counter never reads the R2–R5 disposition record. C2 reconciles the four self-assessment/closure assertions against their source artifacts; its counter never depends on regenerated receipts. Either claim can meet independently.

## Sourced-claim binding

C1's supporting knowledge entry will cite a source row opened this round (planned row `S074`, official Python `hashlib` documentation) and the committed r39 verifier behavior. The source row and its located quote are recorded in `corpus/lessons/round-40.md` `## Gate`.
