# Entailment-review packet — the non-author bar for the r66 semantic counter (round 70)

Purpose. The r66 semantic counter (`corpus/evidence/round66/c2-semantic-count.py`, 9 arms) proves
that a knowledge entry's citations are registered, mined, tier-A/B, anchored, body-cited, and that
its Claims/Limits sections are non-trivial. It cannot prove that any claim is *entailed by* its
source — the filler-author residual disclosed at r66 (QUALITY-131) and carried verbatim through the
r68 and r69 verifier spot-checks: "a non-author entailment review remains the real bar". This
packet turns that bar from a phrase into a runnable protocol, so the operator can schedule the
review the way the r69 spot-check's SHONEN note schedules the promotion review. **The packet does
not close the residual.** The residual closes only when a completed, committed non-author review
record exists (Closure rule below). Until then the counter's filler-author class stays open and
every verdict that leans on the counter stays limited exactly as disclosed.

## Who reviews

A fresh non-author session — one that did not author the entries under review and is not
dispatched by this lane's round author — scheduled by the operator. Author-dispatched seats and
this packet's fixtures do not satisfy the bar (AXES.md: a dispatched subagent does not count).

## What is in scope

`claims-scope.tsv` enumerates the 12 numbered claims of the four entries the counter has passed
since r66 (`receipt-identity-r65`, `host-source-resolution-r66`, `receipt-digest-provenance-r67`,
`host-portable-gate-selftest-r68`). A reviewer may review a subset; each reviewed claim gets one
row. Rows outside the scope ids are a format FAIL (the checker names them).

## How to review one claim (per-claim procedure)

1. Read the claim in its entry (the `## Claims` item named by the claim id's `#n`).
2. Look up the cited S-row in `corpus/SOURCES.md`; open the row's source: for tier-A upstream rows
   the committed capture under `corpus/evidence/round*/captures/` is the bytes to read (no fetch —
   read the committed capture); for own-work rows read the named receipt/path at the pinned revision
   (`git show <rev>:<path>`).
3. Decide one verdict word per QUALITY criterion 8's support states: `supported` (the source states
   what the claim states, at the row's located anchor), `contradicted` (the source states the
   opposite), `unsupported` (neither — including "source exists and is on topic but does not state
   this"). Never promote an observation: "source opens" and "source is on topic" are not support.
4. Write one row in the record format below. The reason (>= 8 words) must name the anchor location
   you read (file and line, or capture + offset) — "looks right" is not a reason.

## Record format

Copy `review-record.template.md`, fill `reviewer:` and `reviewed-at:`, one row per reviewed claim:

    | <entry-slug>#<n> | <entry path> | <S###> | <verdict> | <reason naming the anchor you read> |

Check the format mechanically before handing the record back:

    python -I corpus/evidence/round70/entailment-review/record-format-check.py \
      --record <your-record.md> --scope corpus/evidence/round70/entailment-review/claims-scope.tsv --root .

Exit 0 = format PASS; 1 = format FAIL (each defect named); 2 = fail-closed ERROR. The checker
validates FORMAT ONLY — a passing format check says nothing about the verdicts' correctness.

## Closure rule

The residual closes when a completed record lands as a committed non-author document (suggested
home: `corpus/lessons/round-<N>-entailment-review.md`, authored by the reviewer, committed by the
integrator). Until that record exists, the lane's records must keep the disclosure: the counter
proves registration and form, entailment stays with the non-author reviewer.

## Limits of this packet

The packet operationalizes the review; it is not the review. The scope is the four counter-passed
entries, not every entry in `corpus/knowledge/`. The checker's format verdict is mechanical
(shape, presence, resolvability) and is forgeable in the way every form check is — a reviewer
could write well-formed nonsense; that is precisely why the bar is a non-author judgment and not
a checker. Nothing here fetches anything: tier-A ground is read from committed capture bytes.
