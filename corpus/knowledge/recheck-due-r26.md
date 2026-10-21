source: S035 — tools/research-gate.sh verify-metadata --as-of; corpus/evidence/round26-claims.md Claim2. S037 — https://resources.cochrane.org/sites/resources.cochrane.org/files/uploads/inline-files/Transform/201912_LSR_Revised_Guidance.pdf, Version December2019, section4.3.4 p19, fixed-interval updates. S038 — https://docs.python.org/3/library/datetime.html, Python3.15.0 date.toordinal and date arithmetic note1, proleptic Gregorian calendar-day arithmetic. S029 — https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-iv, Handbook v6.5, IV.1 periodic currency assessment (reopened this round).
verified-at: 2026-10-21 — checked the declared due-date model against the spec, the frozen29 header oracle and six planted controls; measured revision and results are owned by SCORECARD.md Round26.
recheck: 90d — cwd=lane root; `bash corpus/evidence/round26-measure.sh "$PWD" c2`; for current notes, `bash tools/research-gate.sh verify-metadata corpus/knowledge --root . --as-of YYYY-MM-DD` with an explicit calendar date (never execute a recorded recheck command from entry text).

# A due date schedules assessment, not truth

## Source-grounded distinction

Cochrane says its reviews should be assessed periodically to decide whether
an update is needed (S029, IV.1). Its LSR guidance distinguishes searching
from publishing updates and allows a fixed-interval update schedule in the
specified setting (S037, §4.3.4). Neither source prescribes generic research
note fields or a universal90-day cadence.

The following is **this lane's policy**, not a Cochrane rule [INFERENCE]:
use an entry's declared schedule to compute when an assessment is due.
Python's `date`/`timedelta` arithmetic represents the proleptic Gregorian
calendar and addition of calendar days (S038); the independent oracle uses
those semantics. Adopting them for the Bash checker is a lane design choice.

## Decision table

| recheck first token | verified-at | due | freshness at explicit as-of |
|---|---|---|---|
| calendar-validYYYY-MM-DD | any | explicit recheck date | overdue iff as-of>due, otherwise current |
| Nd (decimal calendar days) | valid leading ISO date | verified-at+N days | same strict comparison; equality is current |
| on-release | any | on-release | event; no inferred calendar deadline |
| command-only, absent, invalid, or out-of-range result | any | unknown | unknown, never silently current |

`--as-of` is opt-in. Without it the metadata screen retains its old output.
The new warning `META_RECHECK_OVERDUE` means the **declared schedule** passed;
it is not a finding that the entry is false. `freshness=current` means only
that the recorded deadline has not passed, not that sources were reopened.
`event` does not certify that releases were monitored. Unknown is honest
missing scheduling information; command-only legacy rechecks stay unknown.

## Recheck method

At a real due point, open the source and named anchor again, compare the
claim with what the source states, and record what was checked. A date alone
is not the re-verification (QUALITY6/8). Do not change a cadence solely to
turn an overdue report green. The frozen29 distribution and controls are
owned by the final measurement receipt; no row-count increase is asserted
as expanded domain understanding by itself.

## Withdrawal of implementation admission — 2026-10-21 (append-only)

The source-grounded distinction and declared policy above remain proposals
with explicit scope, but **the Round26 implementation is not admitted**.
Its measured target is `0e9784bd52eca456b24d0bc40921480a47f91a2b`.
The inherited frozen run matches29/29 oracle cases and6/6 controls
(`evidence/round26-inherited-after.log`); these do not cover the independent
input-domain counterexamples in `.ufo/waves/round-26/falsify/`:
`FDateHugeCadence.md` records process termination rather than unknown;
`FDateAsOfUsage.md` records locale-dependent invalid-argument exit1 instead
of setup/usage exit2. Repeated-option behavior is separately observed in
`FDateExplicitDate.md`, not silently adopted as a new specification.

The shared selftest also fails3/187 (`FNoTrade.md`). No failed check was
rerun merely to confirm it during recovery. Do not use this candidate mode's
absence of findings as a reliable freshness verdict. SCORECARD records C2
harmed/falsified and the round not admitted; source-row mining is not
implementation validation or truth certification.
