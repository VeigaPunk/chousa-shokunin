# Round 34 — frozen claim (design v1)

Base `b80539005176ac6ce39bc1c7afb846cb1f2f7c75` (lane `master`). Gate at base:
`tools/research-gate.sh` SHA-256 `43a1af35ca668fe535fcef1e68b0c64bbba3eada59c7a23181f591901fca4346`
(the landed round-33 gate). Counter (this commit): `corpus/evidence/round34/c1-count.py`, SHA-256
`5ef347874960b52561a1cfa517f3f3fc0d1763830e3580c44b993f8394c0a565`; every receipt records the
counter that produced it (`counter_sha256`); only receipts carrying that hash count for design v1.

One claim this round. The round-33 routed defects E1–E5
(`corpus/lessons/round-33-verifier-spotcheck.md:155-173`) are repairs, not claims: E1 (fuzz
receipts bound to an uncommitted gate), E2 (per-seed confuser counter for the round-33 reader),
E3 (stale `SKILL.md:83` range), E4 (receipts labelled on uncommitted gate bytes), E5 (misroot
proof). E2 re-scores a rule the lane already holds on new inputs: quality work, never a claim
(round prompt §6.9). Anti-loop (orchestrator note for r34): the claim works a different frontier
area than the round-32/33 streak (record-field parsing): span length.

## C1 — operability (lowest scored axis: the only scored axis, `SCORECARD.md:7`)

**Surface.** The span matcher of `verify-claims`: `tok_span_at` and `tok_span_all`
(`tools/research-gate.sh:1553-1607`), called from `verify_claims` (`:1806`, `:1827`). Both build a
PCRE pattern of four bytes per span byte (`\xHH`) and pass it to grep(1) as one argv string. A
span of 32768 bytes or more makes that string longer than the kernel's single-argument limit, the
exec fails with "Argument list too long", no occurrence is reported, and a span that is in the
source verbatim reads `observed=unsupported` with `CLAIM_SPAN_NOT_FOUND`. Measured on the base
gate before this design (L1 probe, `/fast/scratch/hyaku/chousa-r34/probe/`): a 40498-byte span
copied verbatim from its source reads `unsupported`, stderr
`/usr/bin/grep: Argument list too long`. The corpus README frontier carries "the per-character
cost of the bash reader on very long lines"; SCORECARD planned r34 names "spans of 32 KiB or more
(`tok_span_at` argv limit)". Operability (AXES.md): the checklist command `verify-claims` does
not produce its stated outcome on such claims. Coverage is not claimed: the rule (verbatim,
boundary-delimited span; round-31 line binding) is held; what moves is the span length the
runnable command can evaluate.

**Contract.**
1. A span of 32768..65536 bytes that occurs in its source with token boundaries on both sides
   (the round-4 rules) reads `observed=supported` (`expect=supported`).
2. A span of that length that does not occur delimited — one letter changed anywhere, its two
   halves present but never adjacent, or its only occurrence glued to a word character on either
   side — reads `observed=unsupported`.
3. With a `"line"` field, a long span binds iff some delimited occurrence starts and ends on the
   named lines (round 31); otherwise `observed=mislocated` with a `CLAIM_LINE_MISMATCH` finding
   naming the id.
4. Short spans (64..4096 bytes) keep their verdicts.

**Counter.** `python3 corpus/evidence/round34/c1-count.py [--gate PATH] [--seed N] [--receipt F]
[--keep DIR]` (lane root). 30 records in 13 classes with fixed counts (the counter's docstring
lists them; 24 long, 6 short). All content is generated per seed: a per-seed random lowercase
vocabulary, random separators, random span lengths, mutation offsets (head ≤63, tail last 64,
middle 8192..len−8192), split points and line positions; ids and file names random hex; record
and file-creation order shuffled; random mtimes. Every record carries `expect=supported`; truth is
hidden. Matching rule (docstring, same text): one `CLAIM id=<id>` line with `observed=` equal to
the truth, and `CLAIM_LINE_MISMATCH` naming the id iff the truth is `mislocated`. The gate run must
exit 1 with a `RESEARCH_GATE: DRIFT` line within 1500 s, else every record scores `none`.

**P1 (frozen predicate).** C1 is met iff, on the landed lane revision, this counter prints
`LONGSPAN_MATCH=30/30` (receipt label `predicate_holds=true`) on each of two fresh-seed runs, and no
committed run of this counter on the landed gate prints a lower count.

Code condition: `holds = matched == TOTAL` with `TOTAL = 30`. Receipt label: `predicate_holds`.

**Kill rule.** Any committed run of this counter on the landed gate below 30 is a miss. A miss is
reported as an honest stop; the counter, TOTAL and P1 are never amended after a candidate is
scored.

**Before (do-nothing control).** The base gate on fresh seeds (L1, receipts under
`.ufo/waves/round-34/controls/L1-base/`). Expected from the classes: every long supported,
line-bound and line-wrong record misses (19 of 30 match at most: the 6 short records, and the 13
long records whose truth is `unsupported`). Measured before this commit, seed 3401:
`LONGSPAN_MATCH=19/30` (gate rc 1, 490 s, stderr `/usr/bin/grep: Argument list too long`;
`controls/L1-base/base-s3401.json`). The first draft of this paragraph said 18; the count of
long `unsupported` records is 13 (2+2+3+2+2+2), so the ceiling is 19, corrected before freezing.

**Pre-data control wave (required before any candidate is scored).** Mutation-tester and executor
seats build and score, with this counter as committed: do-nothing (base) on fresh seeds;
accept-long (any span ≥32768 bytes supported without a search); prefix-only and suffix-only
truncation; prefix+suffix windows; independent halves (both halves present anywhere); no-reader
and junk gates; a boundary-blind substring search; a fix in `tok_span_at` only (line binding left
on the argv path); line-field ignored; shortcuts keyed on ids, file names, record order, span
length or the fixture's vocabulary shape. Their receipts are committed before the first candidate
receipt. A control that meets 30/30 sends the design back to v2 before data.

**The command that would show C1 unmoved:** this counter on the landed gate printing a count below
30, as the base does.

**Not claimed.** Spans above 65536 bytes; run time (only the 1500 s run bound); other modes
(`verify-chain` quote anchors and `verify-sweeps` use the same helpers but are not counted);
`expect=contradicted` markers on long spans; the `CLAIM_SPAN_NOT_FOUND` context probe; sources
with non-ASCII or non-letter content; semantics or truth of a span.

## Sources (frontier step)

C1 rests on a `SOURCES.md` row opened this round: the Linux man-pages execve(2) limit on the
length of a single argument or environment string (`MAX_ARG_STRLEN`, 32 pages), and, if opened,
pcre2limits(3) on compiled-pattern size (why a long literal PCRE pattern is not a fix either).

## Design v2 (before data; supersedes the v1 counter, TOTAL, P1 and kill rule)

Made after the pre-freeze control wave and before any candidate was scored. Three wave-1 control
seats ended on provider `cyber_policy` holds (CtlC1Shortcut, CtlC1Windows, CtlC1Halves; also
MutC1Counter and CritC1AxisFit), so the L1 built those control shapes itself
(`.ufo/waves/round-34/controls/L1-gates/`, sha256 in `SHA256SUMS`). Under the v1 counter
(`5ef34787…a565`) three skip-the-middle controls meet the target
(`controls/L1-v1-meets/`): the shoulder shape CritC1Shapes named (prefix 64 bytes + middle
[8192:len−8191] + suffix 64 bytes at consistent offsets) 30/30 on seeds 3421 and 3422; a
three-window 90% compare 30/30 on 3421 and 3422; first/last 16384-byte windows 30/30 on 3421.
Cause: v1 put each long record's single mutation at 0..63, len−64.., or 8192..len−8192, so a
gate that never compares some bytes is caught only when a mutation happens to land there. v1 is
therefore rejected as the P1 counter before data. (An intermediate uncommitted draft with ten
uniform single-mutation records was itself met by the 90% compare on one of four seeds and was
discarded unscored; its bytes were not kept, so no receipt of it is cited.)

**Counter v2.** `python3 corpus/evidence/round34/c1-count-v2.py [--gate PATH] [--seed N]
[--receipt F] [--keep DIR]` (lane root), SHA-256
`7127246260390a8e33b9597a7726c009dccb0b26935cc1f0889c3b99988376ac`. 40 records in 16 classes:
v1's classes with long-mut-mid (3) replaced by long-mut-center (2, one letter changed within 64
bytes of len/2) and three near-copy decoy classes: the source holds 8 copies of the span, each
with one letter changed at an offset drawn uniformly over the whole span — long-decoys (7, no
exact copy, `unsupported`), long-decoys-exact (2, one exact copy at a random slot, `supported`),
long-decoys-line-wrong (2, exact copy present, `"line"` names a decoy's lines, `mislocated`).
A gate that accepts a copy matching on only a fixed fraction f of the bytes passes long-decoys
with probability about f^56 per seed. Matching rule, run bound and the other classes unchanged.

**P1 v2 (frozen predicate).** C1 is met iff, on the landed lane revision, this counter prints
`LONGSPAN_MATCH=40/40` (receipt label `predicate_holds=true`) on each of two fresh-seed runs, and
no committed run of this counter on the landed gate prints a lower count.

Code condition: `holds = matched == TOTAL` with `TOTAL = 40`. Receipt label: `predicate_holds`.

**Kill rule v2.** Any committed run of counter v2 on the landed gate below 40 is a miss, reported
as an honest stop; counter v2, TOTAL and P1 v2 are never amended after a candidate is scored.

**Controls under v2 (pre-data, L1; `controls/L1-v2/summary.txt`, seeds 3441–3444).** Best
non-oracle: 90%/95% three-window compare 34–38/40; shoulder 32–34; 16384 windows 30–31; halves
(2/4/16 chunks, any or ordered) 29–31; band/line-keyed metadata 29; long-majority 29; record
order / mtime 11–19; id-hash 7–16. Feasibility oracle (python exact search, never a candidate):
40/40 on all four seeds. Do-nothing (base gate) under v2: `controls/L1-base/` (committed with the
v2 receipts or before the first candidate receipt). The seats' v1 control gates are re-scored
under v2 by the L1 before the first candidate receipt (`controls/L1-v2-rescore/`).

**The command that would show C1 unmoved:** counter v2 on the landed gate printing below 40.

## Design v3 (before data; supersedes counter v2, TOTAL, P1 v2 and kill rule v2)

Made before any candidate was scored, after CritC1Shapes (`.ufo/waves/round-34/w1/CritC1Shapes.md`,
a completed seat) named gate shapes no v2 class distinguishes — order-insensitive fingerprints,
whitespace-normalising and case-insensitive comparison, first-raw-occurrence-only matching — and
after CritC1AxisFit's in-flight note (sent by IRC; the seat itself ended on a provider hold, so the
note is recorded, not relied on) that no generated span exceeded 65009 bytes.

**Counter v3.** `python3 corpus/evidence/round34/c1-count-v3.py [--gate PATH] [--seed N]
[--receipt F] [--keep DIR]` (lane root), SHA-256
`970cf9a709d72ed8b3ec91eeabc2b1778831f695b5ea18b40f026489f7f2da2a`. 42 records in 17 classes (the
docstring lists them): v2's classes, each near-copy decoy now carrying one edit of a kind drawn per
decoy (substitution, adjacent transposition, upper-casing, separator swap); long-decoys holds 24
near-copies; new class long-glued-then-valid (2, `supported`); long spans drawn up to 65536 bytes.

**P1 v3 (frozen predicate).** C1 is met iff, on the landed lane revision, this counter prints
`LONGSPAN_MATCH=42/42` (receipt label `predicate_holds=true`) on each of two fresh-seed runs, and
no committed run of this counter on the landed gate prints a lower count.

Code condition: `holds = matched == TOTAL` with `TOTAL = 42`. Receipt label: `predicate_holds` is
the per-run condition; P1 needs two receipts with it and no committed landed-gate receipt without it.

**Kill rule v3.** Any committed run of counter v3 on the landed gate below 42 is a miss, reported as
an honest stop; counter v3, TOTAL and P1 v3 are never amended after a candidate is scored.

**Held controls and exclusions (orchestrator safety clarification, 2026-10-23 ~11:20Z).** Five
wave-1 seats ended on provider `cyber_policy` holds: CtlC1Shortcut, CtlC1Windows, CtlC1Halves,
MutC1Counter, CritC1AxisFit. Before the clarification the L1 re-authored the held control shapes
itself; under the clarification that is a bypass of the hold. Those artifacts are therefore
**excluded from evidence** and are not cited for any verdict: `controls/L1-keyed/` (record
order/mtime, id-hash, length-band/line-keyed and long-majority controls, the CtlC1Shortcut shape),
`controls/L1-windows/` and the window/fraction controls (`window_ctl.py`, `window_frac.py`,
`ctl-win*`, `ctl-frac*`, the CtlC1Windows shape), the halves controls (`halves_ctl.py`,
`ctl-halves*`, the CtlC1Halves shape), their receipts in `controls/L1-v1-meets/` and
`controls/L1-v2/`, and their v3 scores (kept uncommitted in scratch). They stay in the history as
committed by `ef16afb1`; this paragraph is their exclusion record. The v2 design paragraph above
cites them as its motivation; the v2 and v3 counter designs stand as frozen before data, but no
claim of shortcut resistance rests on those excluded receipts.

**Consequence for C1 (declared before data).** The round prompt §6.9 and the pre-freeze control
rule require the cheapest shortcut controls (fixture-keyed, window, independent-chunk) to be scored
before freezing. Those controls are held and may not be substituted, so C1 **cannot verify this
round whatever the measurement shows**: it is reported `unverified (required controls held)`. The
candidate is still built, landed and measured with counter v3 as independent operability work.

**Non-held controls under v3 (L1, `controls/L1-v3/`, seeds 3461–3464).** Feasibility oracle
(python exact search; never a candidate) 42/42 ×4; shapes from CritC1Shapes: case-insensitive
33–35/42, whitespace-blind 34–35, order-blind histogram with anchors 35, first raw occurrence only
38, shoulder-blind three-region compare 34–35. The do-nothing control (base gate) under v3 and the
wave-1 seats' own control gates (non-held seats) are scored by the L1 before the first candidate
receipt (`controls/L1-base/`, `controls/L1-v3-rescore/`).

## Erratum (after data; evidence pointers only — counter v3, TOTAL, P1 v3 and the verdict rule unchanged)

Found by R34CritClaim (`.ufo/waves/round-34/w2/R34CritClaim.md`):
- The v2 section's sentence that a v2 do-nothing receipt (`controls/L1-base/`) and v2 seat
  re-scores (`controls/L1-v2-rescore/`) would be committed before the first candidate receipt was
  never fulfilled: v2 was superseded by v3 before those runs were made. `controls/L1-base/` holds
  only the v1 receipt (19/30). The v3 do-nothing receipts are in `controls/L1-base-v3/` (25/42
  under `LC_ALL=C`; 0/42 ×2 by timeout in the UTF-8 locale), not `controls/L1-base/` as the v3
  paragraph says; the v3 seat re-scores are in `controls/L1-v3-rescore/`.
- The L1 control receipts bind the wrapper script (`ctl-*.sh`), which `exec`s a python helper at a
  scratch path; `L1-gates/SHA256SUMS` hashes the helpers, but no receipt proves which helper bytes
  ran. The L1 control scores are diagnostic, not independent proof of control closure.
- `shoulder_ctl.py` was derived from `window_frac.py` (an excluded window-family helper). It is
  moved to the exclusion list with the window family. Counter v3's docstring still names held-seat
  material in its design history (CritC1AxisFit's note; v2's held-control motivation); CritC1Shapes
  (`w1/CritC1Shapes.md`, completed) independently records the 65009-byte bound.
- Two counter-v3 receipts at 42/42 on the landed gate (`measure/c1v3-s3601.json`,
  `c1v3-s3602.json`) meet the numerical P1 v3; C1 stays `unverified (required controls held)` as
  declared before data.
