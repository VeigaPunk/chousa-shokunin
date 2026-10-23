# ExecC2Oracle — C2 feasibility oracle (round 34, attempt 2, wave 2a2)

Seat: `chousa-r34-w2a2-ExecC2Oracle-9`. Scope: the **C2 feasibility oracle** — an
independent exact-search re-implementation of the landed gate's `verify-claims`
span matcher, scored with the frozen C2 counter on two fresh seeds, plus the
per-class margin comparison against the landed and pre-fix gates. Read-only on
all lane production files; every experiment ran in
`/fast/scratch/hyaku/chousa-r34-a2/w2/ExecC2Oracle/`.

**Verdict: the C2 target 37/37 is attainable and the landed gate a6307edf
attains it. The oracle scores 37/37 on both fresh seeds (9101, 9102) and on two
more (9103, 9104); the landed bash gate scores 37/37 on the same fresh seeds;
the pre-fix gate 772a1d8e scores 21/37. Per-class margin (landed − oracle) is
+0 in all 17 classes — the landed gate is at the oracle's ceiling everywhere,
so no class has hidden headroom or a hidden loss.**

---

## 1. Pins (all verified this run)

| object | sha256 (prefix) | how obtained |
|---|---|---|
| landed gate `tools/research-gate.sh` | `a6307edf687ac0fb` | `git show 707da818:tools/research-gate.sh \| sha256sum` = worktree `sha256sum tools/research-gate.sh` (identical) |
| pre-fix gate (attempt-1 tip `bf7c931a`) | `772a1d8e4d94dbf3` | `git show bf7c931a:tools/research-gate.sh` |
| C2 counter `corpus/evidence/round34/c2-count.py` | `8c0def4d377cdf1a` | worktree == `git show 707da818:…` |
| frozen design v4 | — | `corpus/evidence/round34/claims-a2.md` at `707da818` |
| my oracle `oracle.py` | `56beec0830d86dfe` | `sha256sum` in `.ufo/waves/round-34/w2a2/ExecC2Oracle/oracle.py` |

Frozen tip `707da8184a0fc4d10ab3f17271556cdf364f0af5` was used for every
committed-blob citation (the lane working tree later advanced to `6a3cc32` and
then `b8b0af7`;
the gate blob and the C2 counter blob are unchanged between those two commits —
`git diff 707da818 HEAD -- tools/research-gate.sh corpus/evidence/round34/c2-count.py`
is empty). The C3 files (`audit-set.json`, `self-audit.py`) *did* change after
the frozen tip, so C3 is treated separately in §6.

---

## 2. The oracle (exact-search feasibility gate)

`oracle.py` (artifact, copied to `.ufo/waves/round-34/w2a2/ExecC2Oracle/oracle.py`)
is a from-scratch re-implementation of the landed gate's `verify-claims` span
decision, written to the **contract semantics**, not to the landed code:

* **Boundary rules transcribed from the landed gate blob**, with path:line
  citations into `tools/research-gate.sh`:
  * `TOK_WS` / `TOK_PUNCT` — `tools/research-gate.sh:1526-1527`
  * `tok_word_char` — `tools/research-gate.sh:1529-1536`
  * `tok_left_ok` — `tools/research-gate.sh:1538-1550`
  * `tok_right_ok` — `tools/research-gate.sh:1552-1564`
* **LC_ALL=C byte semantics** throughout: the oracle reads the source as
  `bytes`, computes offsets as byte offsets, and treats the span as the UTF-8
  encoding of the JSON string. No character/locale semantics anywhere.
* **Every occurrence**: `all_offsets()` returns *all* byte offsets at which the
  span occurs, including overlapping ones (`hay.find(span, i+1)` stepping), not
  the leftmost non-overlapping set. Each occurrence is then tested against both
  boundary predicates; the first delimited occurrence gives `at=`, and the line
  binding enumerates **all** delimited occurrences (matching the landed gate's
  `tok_span_all` loop at `tools/research-gate.sh:1894-1904`).
* Output protocol exactly as the counter parses it: `CLAIM id=… expected=… observed=…`
  (`c2-count.py:95`), `FINDING CLAIM_LINE_MISMATCH … obs=id=…` (`c2-count.py:96`),
  `VERDICT_BEARING_CLAIMS=`, `RESEARCH_GATE: DRIFT`, exit 1.
* `oracle-gate.sh` is a bash wrapper (`exec python3 oracle.py "$@"`) so the
  counter's `bash <gate> verify-claims <claims> --root <root>` invocation works
  unchanged (`c2-count.py:329`).

The oracle is deliberately *independent of the landed implementation*: it never
calls grep, never uses a probe chunk, and has no PCRE/argv ceiling at all.

---

## 3. Headline measurement — two fresh seeds (plus two more)

```
cd /fast/scratch/hyaku/chousa-r34-a2/w2/ExecC2Oracle
export C2_TMP=$PWD/tmp
timeout 900 python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round34/c2-count.py \
  --gate $PWD/oracle-gate.sh --seed 9101 --receipt $PWD/oracle-s9101.json
```

| seed | gate | label | exit | receipt |
|---|---|---|---|---|
| **9101 (fresh)** | **oracle** | **DEADZONE_MATCH=37/37** | 0 | `oracle-s9101.json` |
| **9102 (fresh)** | **oracle** | **DEADZONE_MATCH=37/37** | 0 | `oracle-s9102.json` |
| 9103 (fresh) | oracle | DEADZONE_MATCH=37/37 | 0 | `oracle-s9103.json` |
| 9104 (fresh) | oracle | DEADZONE_MATCH=37/37 | 0 | `oracle-s9104.json` |
| 9101 (fresh) | landed bash `a6307edf` | DEADZONE_MATCH=37/37 | 0 | `landed-s9101.json` |
| 9102 (fresh) | landed bash `a6307edf` | DEADZONE_MATCH=37/37 | 0 | `landed-s9102.json` |
| 9101 (fresh) | pre-fix bash `772a1d8e` | DEADZONE_MATCH=21/37 | 1 | `prefix-s9101.json` |

All receipts carry `counter_sha256=8c0def4d377cdf1a…`, `gate_rc=1`,
`predicate_holds=true` for the 37/37 rows. The oracle's elapsed time is 0.22–0.43 s
per run vs 19.6–26.9 s for the bash gate on the same fixture (exact search in
C beats grep-P-with-lookahead on 32 KiB spans) — an independent corroboration
that the oracle is doing real matching, not short-circuiting.

**The oracle independently reproduces the four committed after-receipts' seeds
(5011, 5023, 5033, 5047) at 37/37** (`oracle-committed-s*.json`), so the
committed measurement is re-derivable by a completely different matcher.

---

## 4. Why the landed bash gate can never exceed the oracle — and where it can fall short

### 4.1 The oracle is the semantic ceiling, not an approximation of it

The oracle computes the C2 contract directly: a record is `supported` iff the
span occurs in the source **and** both token boundaries hold at that offset;
`mislocated` iff a delimited occurrence exists but none spans the named line
range; `unsupported` iff no delimited occurrence exists. That is exactly the
contract in `claims-a2.md` items 1–4. The counter's truth map is built from the
same generator, so the oracle's per-record verdict is the contract verdict, and
the maximum attainable score is `TOTAL = 37` (`c2-count.py:90-91`, `TOTAL = sum(...)`; `assert TOTAL == 37`).

Two structural facts make "can never exceed" precise rather than rhetorical.
I state them for a **NUL-free source** and then give the one measured
exception, because the exception is the honest boundary of the claim:

1. **Soundness direction (no false positives).** The bash gate reaches
   `observed=supported` only after a *whole-span byte comparison*:
   the chunk matcher confirms each candidate with `[[ ${hay:offset:slen} == "$span" ]]`
   (`tools/research-gate.sh:1638`), and the direct matcher searches a literal
   `\xHH`-per-byte pattern (`tok_hex_pattern`, `tools/research-gate.sh:1584-1591`).
   Both are exact byte equality on the entire span. Hence every `supported`
   verdict the bash gate emits corresponds to a real delimited occurrence — a
   verdict the oracle, which enumerates *every* occurrence, necessarily also
   finds. Bash can therefore never claim support for a span the oracle does not
   find: **bash-supported ⊆ oracle-supported** (on a NUL-free source — see the
   measured exception below).

2. **Completeness direction (the only way bash can lose on a NUL-free source).**
   The bash gate's
   *candidate generation* is what is lossy, and the loss is entirely on the
   "find an occurrence" side:
   * the direct path is bounded by the PCRE2 compiled-pattern ceiling — measured
     on this host at exactly span bytes 32764 (OK) / 32765, 32766, 32767
     (`grep: regular expression is too large`) / 32768 (argv `E2BIG`,
     `Argument list too long`); re-measured independently in
     `pcre-boundary.txt` (artifact) — that is the dead zone the landed fix routes
     around by lowering `TOK_DIRECT_SPAN_MAX` to 32764
     (`tools/research-gate.sh:1581`);
   * the chunk matcher probes only the first `TOK_CHUNK_BYTES=4096` bytes and
     confirms the rest (`tools/research-gate.sh:1621-1652`), so it can miss an
     occurrence whose 4096-byte prefix is absent — not possible for a genuine
     occurrence, but the *candidate* set is a strict subset of all offsets.
   Consequently the bash gate's `unsupported` verdict can be wrong (a real
     occurrence exists but was not probed), while its `supported` verdict
     cannot be wrong in that direction.

   Net on a NUL-free source: **bash's occurrence set ⊆ oracle's occurrence
   set**, so bash may under-report (say `unsupported` where the oracle says
   `supported`) but never over-report. The oracle is therefore an upper bound
   on the bash gate's score, and `37/37` is the ceiling both must respect.

**Measured exception to the soundness direction — NUL bytes (one case, and it
is not a C2 case).** The bash gate reads the source through
`hay=$(cat -- "$path"; printf x)` (`tools/research-gate.sh:1881-1882`), and bash
command substitution **drops NUL bytes** (the gate itself prints
`warning: command substitution: ignored null byte in input`). So on a source
containing a NUL the bash gate matches a *different byte stream* than the
file's bytes, and the relation above inverts: on source `ab\x00 cd\n` with span
`ab`, bash answers `supported` (the byte after `ab` is a space once the NUL is
stripped) while the oracle answers `unsupported` (raw bytes: the byte after
`ab` is a NUL, a word character). This is a *pre-existing* property of the
gate's hay assembly, independent of C2; the C2 fixture contains no NUL bytes
(all 37 files pure ASCII — measured), so C2's count is unaffected. It is
reported because it is the one place where the oracle is not an upper bound on
the bash gate, and it bounds how far the "never exceed" claim can be pushed.

### 4.2 Measured margin per class (oracle as the ceiling)

From `margin-table.txt` (artifact) — oracle = min over seeds 9101-9104, landed
= min over seeds 9101-9102, prefix = seed 9101:

```
class                    n   oracle  landed  m(land-oracle)  prefix  m(prefix-oracle)
dz-verbatim-ml          3    3/3    3/3    +0             0/3    -3
dz-verbatim-1l          2    2/2    2/2    +0             0/2    -2
dz-edge                  2    2/2    2/2    +0             0/2    -2
dz-mut-head              2    2/2    2/2    +0             2/2    +0
dz-mut-tail              2    2/2    2/2    +0             2/2    +0
dz-mut-center            2    2/2    2/2    +0             2/2    +0
dz-decoys                5    5/5    5/5    +0             5/5    +0
dz-decoys-exact         2    2/2    2/2    +0             0/2    -2
dz-decoys-line-wrong    2    2/2    2/2    +0             0/2    -2
dz-split                 2    2/2    2/2    +0             2/2    +0
dz-glued-left            2    2/2    2/2    +0             2/2    +0
dz-glued-right           2    2/2    2/2    +0             2/2    +0
dz-glued-then-valid      1    1/1    1/1    +0             0/1    -1
dz-line-bound            2    2/2    2/2    +0             0/2    -2
dz-line-wrong            2    2/2    2/2    +0             0/2    -2
short-verbatim           2    2/2    2/2    +0             2/2    +0
short-mut                2    2/2    2/2    +0             2/2    +0
TOTAL                  37   37/37  37/37   +0            21/37  -16
```

Reading: the landed gate is at the oracle's ceiling in **every** class — margin
+0 everywhere, so C2 has no per-class headroom it is hiding behind, and no
class where the landed gate is silently below the contract. The pre-fix gate's
−16 is exactly the 12 supported + 4 mislocated long records (`dz-verbatim-ml` 3,
`dz-verbatim-1l` 2, `dz-edge` 2, `dz-decoys-exact` 2, `dz-glued-then-valid` 1,
`dz-line-bound` 2, `dz-decoys-line-wrong` 2, `dz-line-wrong` 2); the 21 records
that still pass on the broken gate are the unsupported-truth ones, which read
`unsupported` there by accident. (This reproduces the committed before-receipt
`21/37` on a *fresh* seed 9101, and the erratum at `claims-a2.md:180-188`
records the same 12+4 split.)

---

## 5. Differential evidence that the oracle and the bash gate agree where they should

* **Per-record, byte-identical on the C2 fixture.** Keeping the seed-9101 and
  seed-9102 fixtures (`--keep`) and running both gates on the *same* fixture
  root: `diff` of the sorted `CLAIM id=…` lines is empty for both —
  `PER_RECORD_IDENTICAL`, 37 records each. So the two implementations do not
  merely reach the same count; they emit the same verdict for every record.
* **Differential fuzz, 8 seeds × 60 records** (seeds 7001-7008) (`diff-fuzz.py`, artifact
  `diff-fuzz.txt`): 60 random records per seed mixing verbatim / mutated /
  glued-left / glued-right / dash-joiner / quote-joiner / non-ASCII-joiner
  shapes and span lengths 1..40000 bytes, both gates run on the same root,
  per-record `observed=` compared. Result: `TOTAL_DIVERGENCES=0` over
  480 record-level comparisons (960 gate observations: 60 records x 2 gates x
  8 seeds; the harness prints `records=120` per seed, i.e. 60 per gate).
* **Boundary-predicate differential** (`boundary-diff.sh`, artifact
  `boundary-diff.txt`): the predicate block is extracted *verbatim* from the
  landed blob (`sed -n '/^TOK_WS=/,/^}/p'` plus the three function bodies, 44
  non-empty lines) and evaluated in bash against 4000 random byte contexts
  (ASCII letters, punctuation, whitespace, `-`/`'` joiners, and multi-byte
  UTF-8), compared to the oracle's transcription. Result:
  `BOUNDARY_CASES=4000 DIVERGENCES=0`. (An earlier run reported 28 divergences;
  those were a harness artifact — command substitution strips trailing newlines
  — and vanished after the harness decoded bytes with a sentinel. The gate's own
  `hay=$(cat -- "$path"; printf x)` pattern, `tools/research-gate.sh:1881-1882`,
  shows the lane already guards against that in production.)

### 5.1 Two deliberate divergences found (both outside the C2 fixture surface)

These are *not* C2 defects — the C2 fixture never contains them — but they bound
the oracle's fidelity claim and are recorded for the round:

1. **Overlapping occurrences — the bash gate enumerates only NON-OVERLAPPING
   occurrences, the oracle enumerates EVERY occurrence.** Two probes, one per
   matcher path (artifact `divergence-probes.txt`):

   * *Direct path* (span 3 bytes `x\nx` in `x\nx\nx\n`, claim `line=2-3`):
     bash answers `observed=mislocated at=lines:1-2`; the oracle answers
     `observed=supported at=lines:2-3` (the oracle finds the overlapping
     occurrence at offset 2, which binds the named line).
   * *Chunk path* (span 32766 bytes, period 3, a **delimited** overlapping
     occurrence at offset 3): bash answers `observed=unsupported`; the oracle
     answers `observed=supported at=line:1`.

   Mechanism, isolated directly from the two matchers: the direct path's
   `grep -a -z -b -o -P` reports only non-overlapping matches (measured:
   `grep -o -b -P '\x78\x0a\x78'` on `x\nx\nx\n` yields offset 0 only,
   while the lookahead form `'\x78(?=\x0a\x78)'` yields offsets 0 **and** 2),
   and the chunk matcher's `resume` cursor skips any candidate below the
   previous match's end (`tools/research-gate.sh:1637`, `1640`). The chunk
   matcher's own comment states the intent: it reports "the same left-to-right,
   non-overlapping order the one-pattern matcher reports"
   (`tools/research-gate.sh:1577-1580`). So the gate is non-overlapping **by
   design**, while the C2 contract's line-binding clause ("a delimited
   occurrence starts and ends on the named lines") and its `at=` reading read
   as *every* occurrence. This is a contract-vs-implementation gap in the
   line-binding clause, on inputs where the span self-overlaps.

   It does not touch C2's fixture: in the kept seed-9101 fixture, of 37
   records, 5 have two occurrences and **0 have an overlapping pair**
   (measured), so the C2 count cannot be affected. It is recorded because the
   C2 contract's clause 3 is stated over "a delimited occurrence" without
   qualifying non-overlap.
2. **NUL bytes in the source.** Source `ab\x00 cd\n`, span `ab`: the bash gate
   answers `supported` (its `$(cat …)` strips the NUL, so the byte after `ab`
   is a space — a boundary), the oracle answers `unsupported` (raw bytes: the
   byte after `ab` is NUL, which is a word character). The gate's own warning
   `ignored null byte in input` is visible at `tools/research-gate.sh:1881`. Again
   outside the C2 fixture (all 37 fixture files are pure ASCII, 0 NUL bytes).

**Neither divergence can move C2's count**, because the C2 fixture's sources are
ASCII-only and contain no overlapping occurrence pair — both measured on the
kept fixture (see §5 bullets). The overlap gap is the one worth a decision by
the L1: it is pre-existing (the chunk matcher's non-overlap is documented
intent), it is outside C2's frozen surface, and I did not re-open it.

---

## 6. C3 side (secondary, same wave) — the frozen-tip audit set is not the current one

At the frozen tip `707da818`, `audit-set.json` has **43 checks** and
`self-audit.py` prints `SELF_AUDIT_MISMATCHES=0 / SELF_AUDIT_UNDISPOSITIONED=0`
(twice, byte-identical) — re-derived from a clean clone of the frozen tip
(`git clone -q … && git -C … checkout -q 707da818`, `self-audit.py --lane
lane-707da818`), exit 0. At the *current* lane HEAD (`6a3cc32`) the audit set
has grown to **62 checks** and the current run prints
`SELF_AUDIT_MISMATCHES=1` (the `audit-tool-digest` pin, dispositioned as
`superseded by audit-tool-digest-v3`) with `SELF_AUDIT_UNDISPOSITIONED=0`.

C3's P3 is "the printed K is reproduced verbatim by a re-run" — satisfied at both
tips (K is stable across re-runs). But note for the record: **the audit set and
the tool changed after the frozen tip** (`git diff 707da818 HEAD --stat --
corpus/evidence/round34/audit-set.json corpus/evidence/round34/self-audit.py`
→ 159 insertions, 22 deletions across the two files), so a C3 verdict must name *which* set it scored. The
`43 checks` figure in the wave task and in `claims-a2.md` describes the frozen
set; the live set is 62.

---

## 7. Committed-receipt census (P2's "no committed lower run on the landed gate")

At the frozen tip, exactly 6 committed receipts bind the r34 C2 counter
(`counter_sha256=8c0def4d…`): 4 on the landed gate `a6307edf` (seeds 5011, 5023,
5033, 5047 — all 37/37, min 37) and 2 on the pre-fix gate `772a1d8e` (seeds
5011, 5023 — 21/37). **No committed run of this counter on the landed gate
prints a lower count**, so P2's second clause holds at the frozen tip.

Scanning the whole repo at HEAD (`git ls-tree -r HEAD` + JSON parse) finds 129
committed receipts binding this counter, 80 with `matched<total` — but every one
of those 80 is on a *different* gate blob (mutants, pre-fix gates, control
gates: `772a1d8e`, `b091cf2d`, `215e5b5e`, `5472501a`, …), and the 27 receipts
bound to the landed blob `a6307edf` all read 37/37 with min 37. The kill rule
("any committed run of this counter on the landed gate below 37 is a miss") is
**not triggered**.

---

## 8. Commands run (all bounded, all in scratch; lane never written)

```
sha256sum tools/research-gate.sh                                   # a6307edf687ac0fb…
git show 707da818:tools/research-gate.sh | sha256sum              # identical
git show bf7c931a:tools/research-gate.sh | sha256sum               # 772a1d8e4d94dbf3
git show 707da818:corpus/evidence/round34/c2-count.py | sha256sum # 8c0def4d377cdf1a

python3 corpus/evidence/round34/c2-count.py --gate <oracle|landed|pre-fix> --seed <s> --receipt <f>
bash pcre-boundary.sh          # PCRE/argv ceiling, 32760..32769
bash boundary-diff.sh          # 4000 random byte contexts, predicate vs predicate
python3 diff-fuzz.py 7001..7008 # 480 record comparisons, both gates, same root
git clone -q <lane> lane-707da818 && git -C lane-707da818 checkout -q 707da818
python3 lane-707da818/corpus/evidence/round34/self-audit.py --lane lane-707da818
```

No `git`/`jj` write command was run in the lane or the fleet; no production file
was modified; `git status --porcelain` in the lane shows only the wave directory.
No network access. No process was signalled by name or pattern. `df -h /fast`
checked before the writes (36 G free).

---

## 9. Limits of this seat's findings

1. **The oracle is a re-implementation, not a proof.** It is a second opinion on
   the contract, written independently of the landed bash code and validated
   against it three ways (per-record diff on the fixture, 480-record fuzz,
   4000-case predicate differential). It shares one thing with the landed gate
   by construction: the *boundary rules*, which I transcribed from the landed
   blob and then differentially verified. And the "never exceed" argument of
   §4.1 has one measured exception (NUL bytes in the source, §4.1) — outside
   the C2 fixture, but it is the honest edge of the claim. If the landed rules
   themselves are wrong relative to the intent, both would be wrong together —
   the two
   divergences in §5.1 are exactly the places where "the landed rules" and
   "every occurrence" pull apart, and I flag them rather than resolve them
   (resolution is a design decision for the L1, not this seat).
2. **Fixture coverage.** Two fresh seeds for the headline (9101, 9102) plus two
   extra (9103, 9104) plus the four committed seeds = 8 seeds × 37 records =
   296 counter-scored records, all 37/37 for the oracle. The C2 fixture's
   shapes are ASCII-only and non-overlapping (§5), so §5.1's divergences are
   unreachable by construction — but that also means this seat did **not**
   re-measure the C2 surface *with* NUL bytes or overlapping spans.
3. **Host specificity.** The dead-zone boundary (32764 OK / 32765–32767
   `regular expression is too large` / 32768 argv `E2BIG`) is a property of
   this host's GNU grep 3.12 + PCRE2 10.49 (confirmed: `/usr/bin/grep` →
   `libpcre2-8.so.0`, strings show `PCRE2_10.49`). The landed fix
   (`TOK_DIRECT_SPAN_MAX=32764`) is correct on this host; on a host with a
   different PCRE2 ceiling the constant would need re-derivation — the claim
   record already says so (`corpus/knowledge/dead-zone-pcre-r34.md:36-38`).
4. **C3 was not my primary seat.** §6 re-derives the frozen-tip audit count
   (43 checks, K=0, J=0) and notes the post-tip growth to 62 checks; I did not
   re-score C3's claim against the live set, and C1 was not re-opened (frozen
   exclusion, held controls).
5. **Round shape.** The lane advanced from the frozen tip `707da818` to
   `6a3cc32` and then to `b8b0af7` during this wave (later commits add the C3
   audit-set/tool revision, a SKILL.md pointer fix and a verifier spot-check).
   The gate blob and C2 counter blob are identical at every one of those
   commits (`git diff 707da818 HEAD -- tools/research-gate.sh
   corpus/evidence/round34/c2-count.py` is empty), so the C2 numbers above are
   tip-independent; the C3 numbers are not, and I have quoted both. Re-running
   the §7 census at the then-current HEAD `b8b0af7` gives the same figures
   (129 receipts binding the counter; 27 on the landed blob, min 37, none
   below; 80 below 37, none of them on the landed blob).
