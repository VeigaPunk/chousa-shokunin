source: S034 — corpus/evidence/round26-measure-before.log, C1 four-shape RSS table; tools/research-gate.sh verify_metadata snapshot/header loop (round26 measured revision named in SCORECARD.md).
verified-at: 2026-10-21 — exercised the four frozen 8,388,000-byte shapes against the base reader; checked that the read cap and the downstream line-array allocation are different bounds.
recheck: 90d — cwd=lane root; `bash corpus/evidence/round26-measure.sh "$PWD" c1` (frozen inputs read from the lane's pinned base objects; run heavy probes in an isolated clone).

# A byte cap is not an allocation bound

## Observation

The round25 metadata reader capped a single fd-bound snapshot at8MiB, then
copied **every line** into a Bash array before parsing the header. At base
`ba333325`, an8,388,000-byte newline-only file peaked at2,238,736KiB RSS,
versus11,644KiB for a small control. The header-body, CRLF and no-heading
shapes also amplified. Exact measurements and command live in
`corpus/evidence/round26-measure-before.log` and `round26-measure.sh`; do not
convert these shape-specific observations into a universal resource bound.

## Method

1. Name the unit bounded: bytes read, objects allocated, peak RSS, or elapsed
   time. A bound in one unit does not prove a bound in another.
2. Hold input bytes fixed while varying shape (newline density, long lines,
   real header followed by body, no terminator). A small valid control alone
   cannot expose representation amplification.
3. Parse the bounded snapshot directly; do not first materialize a line array.
   The first literal unfenced `## ` ends header parsing, but **not** the
   whole-file NUL/size check. Snapshot acquisition and header cutoff are
   distinct operations.
4. Compare both resources and output: frozen corpus digest, exit code,
   refusals and legacy selftest names/exits. A fast reader that silently
   skips a key is not an improvement.

## Limits

The four-shape RSS acceptance is a test, not a general memory/time budget.
The snapshot is still held as a Bash string; headerless files still require
line traversal, and large continuation values can cost time. Other gate
readers are not repaired by this change. Source identity, fd races, and
semantic claim support remain separate boundaries (see the metadata-screen
round25 note and the hardening ledger). Final C1 measurements are owned by
`SCORECARD.md`'s Round26 row, not restated here before they exist.

## Recovery qualification — 2026-10-21 (append-only)

The final Round26 SCORECARD section now exists. At measured production
revision `0e9784bd52eca456b24d0bc40921480a47f91a2b`, the inherited
`round26-measure.sh TREE all` run records `C1_AMPLIFIED=0/4` with the frozen
plain-output hash/rc unchanged (`evidence/round26-inherited-after.log`).
`falsify/FMutateC1Killed.md` independently demonstrates an RSS detector's
0→1→0 response to restoring the old array representation in a private copy.

This is a narrow measured improvement, **not admission**: the cumulative
gate's selftest fails3/187, and31 falsifier seats returned no report.
`falsify/FNoTrade.md` also finds allocation amplification in the new
registry parser, which C1's plain metadata-entry shapes do not exercise.
All falsifier paths here are under `.ufo/waves/round-26/`.
This note remains a qualified candidate; no universal resource-bound claim
or new admitted capability is supported.
