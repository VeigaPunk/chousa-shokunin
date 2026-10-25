# Round 44 claims — frozen before scoring

author: chousa L1 (Kimi fresh L1)
date: 2026-10-24
round: 44 (attempt 1)
base: `e6983f6e242c7b82bd9a9c5ee170257624e8f109`

No seat has scored these predicates. Construction checks that chose the
quotes and the heading rule are disclosed below. They are not seat scores,
and the predicates are not retuned after any seat scores.

Lowest scored non-retired axis: operability, 3/10. C1 works that axis.
Freshness is not a claim. A pre-round capture open is not a freshness
improvement (round-43 closure route 2).

## C1 — operability (lowest scored non-retired axis, 3/10)

Predicate R44-C1: `python3 corpus/evidence/round44/c1-count.py` reads the
launcher log `corpus/evidence/round44/parent-lifetime.receipt`, written by
`tools/parent-lifetime.sh` while that process waited. The log's start and
end `parent_pid` are the same positive integer, `n_spawned` equals
`n_reaped` equals 64, every seat name is the frozen name in
`corpus/evidence/round44/seat-names.txt`, every `child_pid` is a positive
integer, and every reap line was written before the end line.

Counting command: `python3 corpus/evidence/round44/c1-count.py`

Target, one value: `C1=PASS` with `N_SPAWNED=64/64`, `N_REAPED=64/64`,
`PARENT_PID_MATCH=1/1`, `ZERO_PIDS=0`, `NAMES_MATCH=64/64`, exit 0.

Do-nothing controls, both must exit 1: a missing log
(`C1=FAIL receipt-missing`); `controls/pids0.receipt` (n_spawned 0).
A prose sentence that the parent stayed up is not a log and must exit 1
(`controls/prose.receipt`).

Kill rule: a changed parent pid, a zero child pid, a name not in the frozen
list, or n_reaped not equal to n_spawned is a miss. Dead seats (nonzero
exit codes) are not a miss. This predicate does not grade seat success.

Cheapest full-marks gate without the work (QUALITY 60): a hand-written log
that copies the schema, the 64 names, and invented positive pids. This
counter does not stop that forge. It stops the routed failure: a prose
assertion, a `pids 0` waiter, and a log whose end pid is not the start pid.
The forge is named here so a later round does not treat a schema-valid file
as proof of a live wait.

## C2 — calibration

Predicate R44-C2: `corpus/evidence/round44/disposition.tsv` has one row for
each of the 39 paths frozen in `c2-count.py`. Each of the 36 untracked
round-40/round-41 seat reports is `reverified-commit`: the committed file
contains its basename stem, contains a round token matching its directory
(`40` or `41`), is longer than 80 bytes, and its sha256 equals the row.
Each of the three modified paths is `left-named` and its reason contains
`not hunk-verified`. No other class is allowed.

Counting command: `python3 corpus/evidence/round44/c2-count.py`

Target: `C2=PASS` with `CONSISTENT=39/39`, `REVERIFIED=36/36`,
`LEFT_NAMED=3/3`, exit 0.

Do-nothing control: `controls/all-left.tsv` marks all 39 `left-named`. It
must print `REVERIFIED=0/36` and exit 1. A missing table exits 1.

Kill rule: a missing path, a reverified row whose stem, round token, or
sha256 does not match, or a modified path marked `reverified-commit`, is a
miss. Committing a path without that match is a blind sweep and fails.

Cheapest full-marks gate without the work: copy the spot-check's 39 names
into 39 `left-named` rows. The all-left control is that gate.

C1 and C2 are separable. C1 does not read the disposition table. C2 does
not read the launcher log.

## C3 — depth (sourced)

Predicate R44-C3: `corpus/knowledge/citation-version-binding-r36.md` cites
lane id S079, that row's URL is
`https://www.rfc-editor.org/rfc/rfc7089.txt`, and the located quote
`constitutes a promise that the resource state` is a substring of that
URL's committed capture. The entry does not cite `source: S081`.

Counting command: `python3 corpus/evidence/round44/c3-count.py`

Target: `C3=PASS` with `ENTRY_CITES=1/1`, `QUOTE_LOCATED=1/1`,
`URL_MATCH=1/1`, exit 0.

Do-nothing control: the same command with `--entry` pointed at a path that
does not exist. It must print `C3=FAIL entry-missing` and exit 1.

Kill rule: a missing entry, a citation of staged S081 as the lane id, a
URL mismatch, or a quote absent from the capture is a miss. The quote is
not rewritten after a seat scores.

Cheapest full-marks gate without the work: an entry that repeats the quote
and names S079 while the quote is not in the capture. The counter reads
the capture by the row URL.

Construction, not a seat score (2026-10-24, before this file was the
scoring rule): the quote is a contiguous substring of capture
`d0c4a09a9de32cb91d5e3797.txt` (sha256 of the URL, first 24 hex digits).
The 36 report headings were checked against the stem-and-round-token rule;
0 of 36 failed that looser rule. Fourteen fail a first-line-only rule, so
the first-line rule was not frozen.
