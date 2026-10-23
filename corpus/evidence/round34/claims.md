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
