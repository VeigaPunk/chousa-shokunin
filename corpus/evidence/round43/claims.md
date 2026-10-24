# Round 43 claims — frozen before scoring

author: chousa L1 (Kimi fresh L1)
date: 2026-10-24
round: 43 (attempt 1)
base: `15f9f3fbd3c17b2155f718c67cbef0624034cf6d`

No seat has scored these predicates. The construction recompute that chose the
1/2 bound is disclosed below; it is not a seat score, and the bound is not
retuned after any seat scores.

## Rule R43-SPLIT

A row the committed round-42 table
(`corpus/evidence/round42/quarantine-verdicts.tsv`) labels `absent` is
`misquote` if and only if the maximum, over that row's quotes, of (longest
contiguous common run length after NFKC and whitespace collapse) / (quote
length after the same normalization) is greater than or equal to 1/2,
recomputed from the committed capture. Otherwise the row is `not-carried`.

The 1/2 bound is the lane's own construction. It is the threshold at which the
round-42 lesson's named examples already separate: S093 79/120, S094 63/86,
S108 69/108 and S116 34/36 sit at or above 1/2; S086 4/46 and S114 7/32 sit
below. A construction recompute on 2026-10-24, before this file was the
scoring rule, reproduced those published ratios exactly (S086 4/46 and 2/29;
S093 79/120). That recompute is construction, not the claim's measurement.

## C1 — operability (lowest scored non-retired axis, 3/10)

Predicate R43-C1: `python3 corpus/evidence/round43/c1-count.py` executes
`tools/absent-split.py`, that command enumerates exactly the 15 absent ids of
the committed round-42 table, each id is exactly one of {misquote, not-carried},
both classes are nonempty, and two runs are byte-identical.

Counting command: `python3 corpus/evidence/round43/c1-count.py`

Target, one value: `C1=PASS` with `ABSENT_ENUMERATED=15/15`, `CLASSED=15/15`,
`BOTH_NONEMPTY=1/1`, `REPRODUCIBLE=1/1`, `MUTANT_DETECTED=1/1`, exit 0.

Do-nothing control: the same command with `--tool` pointed at a path that is
not the split command. It must exit 1. A tree that never grew the command
cannot print `C1=PASS`.

Kill rule: any missing id, an empty class, or two runs that differ is a miss.
The 1/2 bound is not part of this predicate. A label swap that keeps both
classes nonempty does not fail C1; that swap is C2's kill.

Cheapest full-marks gate without the work: a script that prints the five
target lines. This counter does not accept that script: it executes the
command and requires the ids to equal an independent read of the round-42 table.

## C2 — calibration

Predicate R43-C2: every label in `corpus/evidence/round43/absent-split.tsv`
agrees with an independent recompute of rule R43-SPLIT, and flipping one row's
label makes the agreement fail.

Counting command: `python3 corpus/evidence/round43/c2-count.py`

Target: `C2=PASS` with `SPLIT_AGREES=15/15`, `VOCAB_OK=15/15`, exit 0.
The flipped-row control (`--flip S086`) must print `SPLIT_AGREES=14/15` and
exit 1.

Kill rule: any disagreement, a label outside the vocabulary, or a flipped row
that still scores 15/15 is a miss. The bound is not retuned to absorb a
disagreement.

Cheapest full-marks gate without the work: a table whose labels were copied
from a printout and never checked against the captures. The flipped-row
control is that gate.

C1 and C2 are separable. C1 does not read the split table's labels. C2 does
not require `tools/absent-split.py` to exist.

## C3 — depth (sourced)

Predicate R43-C3: the admitted entry
`corpus/knowledge/search-log-method-r39.md` cites lane id S078, that id's
registry row names the Europe PMC full-text URL opened this round, and the
located quote is a substring of that URL's committed capture.

Counting command: `python3 corpus/evidence/round43/c3-count.py`

Target: `C3=PASS` with `ENTRY_CITES=1/1`, `QUOTE_LOCATED=1/1`,
`URL_MATCH=1/1`, exit 0.

Do-nothing control: the same command with `--entry` pointed at a missing file.
It must exit 1.

Kill rule: a citation of staged S118, a quote absent from the capture, or a
row whose URL is not the opened capture's URL is a miss. No network re-open
is part of this predicate.

The source opened this round is S078 (renumbered by document from staged S118;
the URL is the evidence, the id follows the lane registry, never arithmetic).

## Not claimed

- Live-web truth of any quote. No external fetch (L0 `8d77e6c1` open).
- Adoption of `search-log-fields-r36.md`. Staged S077's capture is a bot wall.
- The round-1 operability scale. It stays 3/10. These observables sit beside it.
