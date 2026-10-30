# QualityDraft — scoped findings (round65 w1)

Criterion130 drafted from the round64 closure before-receipt self-containment item
(`corpus/lessons/round-65.md` Mistakes row 1). Full deliverable: `QualityDraft/report.md`.
Freeze f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd; QUALITY.md at freeze ends at 129; 130 is next.

## Behavior claimed by the draft

A self-contained receipt declares in-file REVISION (40 lowercase hex, = claimed revision), EXIT
(0..255 decimal, no leading zeros) and SHA256 (64 lowercase hex + canonical repo-relative POSIX path
of the instrument blob at that revision), empty separator, nonempty body. Matching header = receipt
consistency only, never execution authentication. Reference:
`corpus/evidence/round65/controls/ref-receipt-pin.py`; acceptance harness: `corpus/evidence/round65/c1-count.py`
(20 cases, claims R65-C1).

## Gates exercised (ran this wave; receipts in `QualityDraft/`)

| probe | subject | expected | observed |
|---|---|---|---|
| P1 red-before | round64 `controls/c1v3-before-full.txt` (headers absent) | FAIL exit1 | `RECEIPT_PIN=FAIL header/body` exit1 |
| P2 positive | exhibit's blob digest + `EXIT=1` | PASS exit0 | `RECEIPT_PIN=PASS` exit0 |
| P3 boundary | same header, fabricated body | PASS exit0 | `RECEIPT_PIN=PASS` exit0 |
| P4 negative | digest tampered 1 hex | FAIL exit1 | `RECEIPT_PIN=FAIL blob/digest` exit1 |
| P5 negative | header REVISION ≠ `--revision` | FAIL exit1 | `RECEIPT_PIN=FAIL header/body` exit1 |

P2 shows a consistent receipt may report a failed measured command (`EXIT=1`, validation exit0).
P3 shows the scope boundary: consistency is not authenticity. Red-before (P1) and positives are
required by the assignment and are satisfied; the criterion stays bound to receipt consistency,
not authenticity.

## Touched surfaces

Only this seat's outputs: `.ufo/waves/round-65/w1/QualityDraft/{report.md,
qualitydraft-c130-probe-results.txt, qualitydraft-c130-positive-fixture.txt,
qualitydraft-c130-fabricated-fixture.txt}` and this file. No production writes, no installs,
no network, no git/jj mutations (read-only `git -C` only). Scratch
`/fast/scratch/hyaku/chousa-r65/QualityDraft/` deleted after receipts were copied; no /tmp evidence.

## Out of scope / observations

- `tools/receipt-pin.py` (C1 target) absent at freeze; landing it is L1 integration, not this seat.
- Working tree holds uncommitted round65 planning/integration files (QUALITY.md 130 at line 939,
  round-65 lesson, receipt-identity entry, source-openings.json; SCORECARD/SKILL/README/SOURCES
  modified). Reported verbatim as data; no action taken by this seat.
- Historical receipts (S156) stay unmodified; the criterion is prospective for successors.

## Limits

This seat did not rerun the frozen 20-case C1 counter or the C2 counter, and did not check whether
the frozen counters were altered after the freeze; the L1 integration verifies that. The existence of
the before and positive control files in `controls/` was observed, not re-run. Probes cover the
reference validator, not a future target implementation. No claim is made that P3's pass proves
anything beyond the recorded boundary.
