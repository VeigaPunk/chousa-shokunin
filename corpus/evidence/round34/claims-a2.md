# Round 34 attempt 2 — frozen claims (design v4)

Attempt 1 of round 34 (lane commits `f20aeaa7`…`bf7c931a`) declared ONE claim, C1
(long spans ≥32768 bytes, operability), built the candidate gate `772a1d8e…3e58`
(commit `3026a4e5`) and measured counter v3 at 42/42, but five wave-1 control seats
ended on provider `cyber_policy` holds; under the orchestrator safety clarification
(2026-10-23 ~11:20Z) the L1's re-authored held-shape controls were excluded and C1
was declared before data as **unverified (required controls held)**. Attempt 1 died
with the phase-4 orchestrator before writing the round report; the watchdog logged
`lane-dead-no-report chousa round=34`.

Attempt 2 (this file) inherits that state and does NOT re-open C1: the exclusion
record and the pre-data `unverified` declaration are frozen (`claims.md` v1–v3 +
erratum). C1's landed capability (spans ≥32768 bytes verify) stands as committed
operability work with verdict `unverified (required controls held)`.

Attempt 2 declares TWO new claims, each on a distinct axis, sized per the r33
rejection lessons (after-states re-derivable with one command; a calibration claim
counts mismatches, never asserts):

- **C2 — operability** (the lane's only scored, therefore lowest-scoring non-retired
  axis): the span-length surface immediately below C1's window.
- **C3 — calibration**: self-assessment text vs observed repo state, counted.

Base for C2/C3: lane tip `bf7c931a…` (gate `772a1d8e…3e58`, unchanged by attempt 1
after the candidate landed).

## C2 — operability: spans of 32765..32767 bytes (the PCRE dead zone)

**Surface.** `tok_span_offsets` (`tools/research-gate.sh`) routes a span to the
one-pattern grep matcher when its length is ≤ `TOK_DIRECT_SPAN_MAX` (32767) and to
the round-34 chunk matcher above it. The one-pattern matcher passes the span to
grep(1) as one `\xHH` PCRE pattern of 4 bytes per span byte. Two ceilings bound the
direct path: execve(2)'s per-string limit (span ≥32768 → E2BIG, C1's surface) and
PCRE2's compiled-pattern ceiling ("approximately 64 thousand code units",
pcre2limits(3), row S065). The second ceiling binds FIRST on this host: the
measured boundary is a span of **32764 bytes compiles; 32765 fails** with
`grep: regular expression is too large`, so spans of **32765, 32766 and 32767**
bytes — a 3-byte window just under the argv limit — read `observed=unsupported`
even when the source holds the span verbatim. Spans ≥32768 already verify via the
C1 chunk matcher. Measured on the base gate this attempt (L1 probe, all content
classes: space-joined words, newline-dense, punctuation-dense, single-byte,
escape-dense — the failure is length-only):
`/fast/scratch/hyaku/chousa-r34-a2/probe/`, runs of 2026-10-23 ~15:35-03: len
32764 supported; len 32765/32766/32767 `observed=unsupported`,
stderr `grep: regular expression is too large`. S065's host note records the same
32765 boundary. The planned-r35 entry hypothesised the window "about 28000–32767";
the measured window is exactly three lengths — planned entries are hypotheses, and
this correction is mined into `corpus/lessons/round-34.md`.

**Contract.**
1. A span of 32765..32767 bytes occurring in its source with token boundaries on
   both sides (round-4 rules) reads `observed=supported`.
2. A span of that length that does not occur delimited (one byte changed anywhere,
   halves present but never adjacent, glued to a word character on either side)
   reads `observed=unsupported`.
3. With a `"line"` field, such a span binds iff a delimited occurrence starts and
   ends on the named lines; otherwise `observed=mislocated` with
   `CLAIM_LINE_MISMATCH` naming the id.
4. Spans outside the window keep their verdicts (≤32764 direct path, ≥32768 chunk
   path, both unchanged except the routing constant).

**Fix.** Lower `TOK_DIRECT_SPAN_MAX` from 32767 to 32764 so the three dead-zone
lengths route to the existing chunk matcher (probe chunk + whole-span
confirmation); no other matcher change. Add selftest cases pinning the window
(verbatim/mutated/glued/line at lengths 32765 and 32767).

**Counter.** `python3 corpus/evidence/round34/c2-count.py [--gate PATH] [--seed N]
[--receipt F] [--keep DIR]` (lane root). 37 records, 17 classes, all content
generated per seed (vocabulary, separators, span lengths in 32765..32767, mutation
offsets, decoy edit kinds, split points, line positions, ids, file names, record
and file-creation order, mtimes): dz-verbatim-ml 3 supported; dz-verbatim-1l 2
supported; dz-edge 2 supported (lengths exactly 32765 and 32767); dz-mut-head 2,
dz-mut-tail 2, dz-mut-center 2 (mutations at ≤63, last-64, within-64-of-len/2) all
unsupported; dz-decoys 5 unsupported (12 near-copies each with one edit of a kind
drawn per decoy — substitution, adjacent transposition, upper-casing, separator
swap — no exact copy); dz-decoys-exact 2 supported; dz-decoys-line-wrong 2
mislocated; dz-split 2 unsupported; dz-glued-left 2, dz-glued-right 2 unsupported;
dz-glued-then-valid 1 supported; dz-line-bound 2 supported; dz-line-wrong 2
mislocated; short-verbatim 2 supported; short-mut 2 unsupported. Every record
carries `expect=supported` (label carries no truth). Matching rule: one
`CLAIM id=<id>` line with `observed=` equal to the truth and `CLAIM_LINE_MISMATCH`
naming the id iff truth is `mislocated`; the gate run must exit 1 with a
`RESEARCH_GATE: DRIFT` line within 1500 s, else every record scores `none`.
Counter SHA-256 is recorded in every receipt (`counter_sha256`).

**P2 (frozen predicate).** C2 is met iff, on the landed lane revision, this counter
prints `DEADZONE_MATCH=37/37` (receipt label `predicate_holds=true`) on each of two
fresh-seed runs, and no committed run of this counter on the landed gate prints a
lower count.

Code condition: `holds = matched == TOTAL` with `TOTAL = 37`. Receipt label:
`predicate_holds`.

**Kill rule.** Any committed run of this counter on the landed gate below 37 is a
miss, reported as an honest stop; the counter, TOTAL and P2 are never amended after
a candidate is scored.

**Before (do-nothing control).** The gate before the fix (`TOK_DIRECT_SPAN_MAX=32767`,
tip `bf7c931a`) on fresh seeds. The 17 long-supported records (3+2+2+2+2+1... the
classes whose truth is supported and whose span is in the dead zone) must miss:
every record with a 32765..32767-byte span fails with "regular expression is too
large", short records (4) pass. Expected ceiling 4/37. Measured before the
candidate (receipt `measure-a2/c2-before-s<seed>.json`): if the do-nothing control
meets 37/37 the counter or target is wrong and C2 is sent back to design before any
candidate receipt.

**The command that would show C2 unmoved:** this counter on the landed gate
printing a count below 37, as the base does.

**Not claimed.** Spans ≥32768 (C1's surface) and ≤32764 (already work); run time
(only the 1500 s bound); other modes; semantics.

**Pre-freeze note.** C2's shortcut controls (window/chunk/keyed shapes) are NOT
L1-built: the orchestrator safety clarification forbids the L1 re-authoring the
held-seat shapes. They are dispatched as wave-2 attack seats scoring the frozen
counter against their own scratch gates; C2's verdict cites only what is committed
at freeze.

## C3 — calibration: counted self-audit of the round's self-assessment

**Surface.** The calibration axis: "SHONEN.md/SCORECARD entries match observed repo
state" (AXES.md). The r33 verifier spotcheck routed E4 (receipts labelled on
uncommitted gate bytes) and E5 (misroot proof without committed hashes); attempt 1
repaired them as point fixes (`w1/ExecE4Census/receipt-binding.py`, QUALITY 42-43).
What remains unmeasured: whether the lane's round-34 self-description (SCORECARD
rows, LOG entry, SKILL.md tallies, SHONEN evidence pointers) matches committed
bytes as of the landed revision — counted, not asserted.

**Tool.** `python3 corpus/evidence/round34/self-audit.py [--set PATH] [--lane PATH]`
(lane root) with the audit set `corpus/evidence/round34/audit-set.json` (declared,
frozen with the tool). Check kinds: `git_commit` (prefix resolves in lane history);
`path` (exists at lane root); `sha256` (file bytes equal the pinned digest);
`receipt_binding` (a committed receipt's `gate_sha256` equals
`git show <commit>:tools/research-gate.sh | sha256sum` for the commit the receipt
claims); `grep_assert` (a named text assertion holds in a named file). The tool
prints one `AUDIT id=<id> ok` or `AUDIT id=<id> MISMATCH <detail>` line per check,
then `SELF_AUDIT_MISMATCHES=K`, then `SELF_AUDIT_UNDISPOSITIONED=J` where J counts
mismatches with no line in the committed
`corpus/evidence/round34/audit-dispositions.md` (format: `<id> | <disposition>`;
disposition = `fixed <commit>` / `routed <where>` / `accepted <reason>`). Exit 0
always — the tool counts, it does not gate.

**P3 (frozen predicate).** C3 is met iff, on the landed lane revision, the tool with
the committed audit set prints `SELF_AUDIT_UNDISPOSITIONED=0`, and the printed
`SELF_AUDIT_MISMATCHES=K` is reproduced verbatim by a re-run (the count is the
claim's number; every counted mismatch carries a committed disposition).

**Kill rule.** A re-run printing a different K, or any mismatch line lacking a
committed disposition, is a miss, reported as an honest stop; the audit set is
frozen with the claim and amended only before the first counted run... the set MAY
grow by appended checks (each appended check is itself logged), but no check is
edited or deleted after the first counted run.

**Do-nothing control.** No audit → no committed receipt naming K and J; the
after-state is unreachable without the tool, the set and the dispositions. A
junk tool that prints 0/0 without running the checks is excluded because the
re-derivation command re-runs each enumerated check and any seat can inject a
broken pointer into a scratch copy of the set and watch the count move.

**The command that would show C3 unmoved:** `SELF_AUDIT_UNDISPOSITIONED>0` or a
re-run disagreeing with the committed K.

**Not claimed.** Fleet-repo or sibling-lane state; checks not enumerated in the
audit set; automatic repair (dispositions are logged or fixed by hand).

## Frontier step (attempt 2)

C2 rests on row S065 (pcre2limits(3), opened round 34 attempt 1): the compiled
pattern ceiling that bounds the direct path below the argv limit. Attempt 2
re-opens S065 and logs the recheck in `corpus/lessons/round-34.md` (access date,
quote, pins). No new rows are planned; any the wave finds are added per contract.

Mistake mined this attempt: the planned-r35 "PCRE dead zone about 28000–32767"
hypothesis vs the measured 3-byte window (C2 surface paragraph) — planned entries
are hypotheses until measured; and C1 selftest cases 252-253 use a 29999-byte span,
which exercises the DIRECT path, so the chunk matcher shipped r34 with no selftest
case (found while designing C2; the new cases pin both boundaries).

## Erratum (post-data; evidence pointers only — counter, TOTAL, P2 and the kill rule unchanged)

- "Before (do-nothing control)" predicted a 4/37 ceiling (only the 4 short records pass).
  Both committed before receipts measure 21/37: the 17 long records whose truth is
  unsupported (mutations, decoys, split, glued) coincidentally pass on the broken gate; the
  16-record miss set is the 12 supported and 4 mislocated records (every long span reads
  observed=unsupported when grep refuses the pattern, which matches their truth). The
  do-nothing control still cannot reach 37/37; P2 is unaffected. Found independently by
  wave seats RevC2Receipts (MEDIUM) and ExecC2Rerun (D1).
