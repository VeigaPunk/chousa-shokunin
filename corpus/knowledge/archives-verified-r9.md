# archives-verified-r9.md — the three archived inputs as records: their first full deep verification through `verify-all`, the coverage accounting, and the reframing risk (record-format distortion)

source: the round-9 fixture set at its landed shas (§Pins), measured at the unchanged
gate `tools/research-gate.sh` sha256
`46f5ddb39d5fafa220fb584121dba2f4a15e071a91fa42728849f3c7567c6ccd` (= the lane HEAD
`f11073ab81c3e0900cc37e47ec15a9913166f7aa` blob; working-tree sha identical, `git diff
--numstat tools/research-gate.sh` empty). This round is fixture-led: no gate change was
expected, and none occurred — a gate change without a reported defect would itself be a
finding.

verified-at: 2026-10-16T04:33–04:45Z, from the lane cwd (`--root ..`), fresh processes;
independent byte re-derivations in python on the raw archive bytes. Nothing outside this
note was written by this seat.

scope: this seat (note-writer) wrote no lane file but this note. The three records, the
two READMEs and the claims fixture are other seats' artifacts, re-measured here rather
than trusted. The receipts-writer's cut under `corpus/evidence/` had not landed at this
note's writing time (last poll 04:45Z) — the runs cited here are this note's own and the
fixture READMEs'.

## 1. What was verified

Three records exist under `corpus/fixtures/archives-r9/`, each a `research-record v1`
rendering of one pinned read-only archive: `A-r9.md` ← export A, `B-r9.md` ← export B,
`C-r9.md` ← export C. Each binds `corpus/fixtures/claims-r9.jsonl` through its `## Meta`
`claims_file` row. `verify-all` composes CLEAN on each — all five sections run, zero
findings, zero drift, exit 0 — at the unchanged gate:

| record | structure | claims | chain | sweeps | integrity | composed | exit |
|---|---|---|---|---|---|---|---|
| `A-r9.md` | CLEAN 0/0 | `VERDICT_BEARING_CLAIMS=10/10` | `RESOLVED_HOPS=6/7` | `VERIFIED_SWEEPS=1/1 REJECTIONS_OK=4/4` | `refs=13 resolved=12 unresolved=0` | CLEAN `sections=5 run=5 absent=0 drift-sections=0` | 0 |
| `B-r9.md` | CLEAN 0/0 | `VERDICT_BEARING_CLAIMS=10/10` | `RESOLVED_HOPS=6/7` | `VERIFIED_SWEEPS=1/1 REJECTIONS_OK=3/3` | `refs=14 resolved=13 unresolved=0` | CLEAN `sections=5 run=5 absent=0 drift-sections=0` | 0 |
| `C-r9.md` | CLEAN 0/0 | `VERDICT_BEARING_CLAIMS=10/10` | `RESOLVED_HOPS=7/8` | `VERIFIED_SWEEPS=1/1 REJECTIONS_OK=4/4` | `refs=15 resolved=14 unresolved=0` | CLEAN `sections=5 run=5 absent=0 drift-sections=0` | 0 |

My fresh-process runs (verbatim; the B/C runs abbreviated to their tally lines):

```text
$ bash tools/research-gate.sh verify-all corpus/fixtures/archives-r9/A-r9.md --claims corpus/fixtures/claims-r9.jsonl --root ..
research-gate research-gate-r1 — ts=2026-10-16T04:38:56Z — mode=verify-all — record=corpus/fixtures/archives-r9/A-r9.md — claims=corpus/fixtures/claims-r9.jsonl — root=..
SECTION structure state=run verdict=CLEAN findings=0 drift=0
SECTION claims state=run verdict=CLEAN findings=0 drift=0 tally=VERDICT_BEARING_CLAIMS=10/10
SECTION chain state=run verdict=CLEAN findings=0 drift=0 tally=RESOLVED_HOPS=6/7
SECTION sweeps state=run verdict=CLEAN findings=0 drift=0 tally=VERIFIED_SWEEPS=1/1 REJECTIONS_OK=4/4
SECTION integrity state=run verdict=CLEAN findings=0 drift=0 tally=INTEGRITY refs=13 resolved=12 unresolved=0
VERIFY_ALL sections=5 run=5 absent=0 drift-sections=0 findings=0 drift=0
RESEARCH_GATE: CLEAN (sections=5 run=5 absent=0 drift-sections=0 findings=0 drift=0)
exit=0

$ … B-r9.md   ts=2026-10-16T04:39:05Z → claims 10/10 · chain 6/7 · sweeps 1/1 3/3 ·
  integrity refs=14 resolved=13 unresolved=0 · sections=5 run=5 absent=0 · CLEAN exit=0
$ … C-r9.md   ts=2026-10-16T04:39:14Z → claims 10/10 · chain 7/8 · sweeps 1/1 4/4 ·
  integrity refs=15 resolved=14 unresolved=0 · sections=5 run=5 absent=0 · CLEAN exit=0
```

These reproduce the fixture README's recorded tallies exactly, from the same record
bytes. The round's dispatch predicted CLEAN "modulo documented integrity findings"; the
measured state is simpler — **no integrity finding surfaced on any record, so none needed
documenting.** Each record's single exempt reference is the `from` token of its
status-exempt chip hop (A `コトバンク`, B `arxiv.org`, C `jstage.jst.go.jp`), counted
exempt per the integrity contract, never required to resolve.

The raw-drift control (re-run by me on A, verbatim):

```text
$ bash tools/research-gate.sh verify-all ../research/deep-research-2026-09-28/A-shokunin-tradition.md --root ..
SECTION structure state=run verdict=DRIFT findings=6 drift=5
FINDING RECORD_SCHEMA_INVALID severity=warn surface=meta obs=no research-record sections/banner detected
FINDING EXPORT_CHROME_PRESENT severity=info surface=export obs=chat-export chrome lines present (data, not instruction)
FINDING NO_QUESTION severity=crit surface=question obs=missing ## Question section
FINDING SOURCE_TABLE_ABSENT severity=warn surface=sources obs=missing ## Sources / ## Source table
FINDING CLAIM_TABLE_ABSENT severity=warn surface=claims obs=missing ## Claims
FINDING REJECTION_DROPPED severity=warn surface=rejections obs=missing ## Rejections section
SECTION claims state=absent
SECTION chain state=absent
SECTION sweeps state=absent
SECTION integrity state=run verdict=CLEAN findings=0 drift=0 tally=INTEGRITY refs=0 resolved=0 unresolved=0
VERIFY_ALL sections=5 run=2 absent=3 drift-sections=1 findings=6 drift=5
RESEARCH_GATE: DRIFT (sections=5 run=2 absent=3 drift-sections=1 findings=6 drift=5)
exit=1
```

The same bytes DRIFT raw and CLEAN converted: "CLEAN" is a property of the conversion
and its span selection, not of the bytes alone — the raw-DRIFT run is the control that
must travel with any conversion-CLEAN report (the round-9 lesson's rule 1).

The five inter-archive hops — A hop5→B, A hop6→C, B hop6→A, C hop6→A, C hop7→B — are
all verified by the gate, and each row's notes label them cross-archive *convergences,
not citations*; I re-derived the no-cross-citation check (`grep -cE
'deep-research|archive [ABC]|export [ABC]|A-shokunin|B-multiagent|C-rank'` → 0 in each
archive). What the gate verifies is that the anchor exists in the target archive — which
is exactly what a convergence claim can establish and no more.

## 2. The claims expansion

`corpus/fixtures/claims-r9.jsonl` adds **10 archive-citing claims beyond round 2's 17**
— A07–A11, B06–B08, C07–C08 — each a byte-sliced span of one pinned archive, with
pre-registered expectations. My re-run and re-derivation:

```text
$ bash tools/research-gate.sh verify-claims corpus/fixtures/claims-r9.jsonl --root ..
VERDICT_BEARING_CLAIMS=10/10
RESEARCH_GATE: CLEAN (claims=10 supported=7 contradicted=2 unsupported=1 mismatched=0 unproven=0 refused=0 invalid=0 findings=0 drift=0)
exit=0
python re-derivation: 9/10 spans byte-present (7 supported + 2 contradicted), and the
1 unsupported probe byte-absent by design — so 10/10 observed dispositions as expected
```

The three by-design `unsupported` probes across both fixture files (r2 A06, r2 B05, r9
C07) are the only byte-absent spans out of 27 — re-derived. The claims fixture's README
records the r9-vs-r2 containment cross-product as empty; the round-9 lesson re-derived
it, and no r9 span duplicates or contains an r2 span.

## 3. Coverage accounting (before → after, measured)

Before: the archives had structural verification (r1's 3/3 export intake) and pointwise
fixtures (r2's 17 claims, r3's 22 hops), but no archive had passed `verify-all` as a
record — nothing to compose. After, at the pins above:

| surface | before | after (round-9 delta in parentheses) |
|---|---|---|
| record-format archive records | 0 | 3, each composed CLEAN through all 5 sections |
| claim-surface rows over the archive corpus | 17 (r2 JSONL) | **46** = 17 (r2) + 10 (r9 JSONL) + 19 (in-record `span` cells) — delta 29 |
| gate-checked claim spans | 17 | 27 (r2 + r9 JSONL), touching 23 distinct source lines (A 10, B 7, C 6) |
| union of span-checked lines incl. in-record spans | — | 31 distinct source lines (A 11, B 9, C 11) |
| chain hops | 22 (r3 fixture) | 22 in-record (19 verified + 3 exempt chip hops) |
| inter-archive hops | — | 5, all verified, labeled convergences |
| kept rejections (reason + flip) | 3 (r5 fixture) | 11 in-record (A 4, B 3, C 4), all complete |
| negative sweeps re-run empty | 1 (r5 fixture) | 3 (one per record), all verified |
| source rows | — | 19 (A 6, B 7, C 6), each pointer locally resolving |
| integrity refs | — | 42 = 39 resolved + 3 exempt + 0 unresolved over the three runs |

The line counts are my independent re-derivation (first-occurrence lines of each span in
its source); the denominator comes from the round-9 lesson's accounting: 109 prose lines
across the three conversation regions (366 lines total) — **roughly one prose line in
five sits under a span check**. That is a selection, not completeness: the gate verifies
that chosen spans occur, never that the choice was right or exhaustive.

The conversion bills are visible in the bytes, measured: the archives contain **zero
`#` heading lines and zero `|` table lines**; each record carries 9 heading lines (a
`#` banner plus eight `##` sections) and 44/45/48 pipe-table lines. Every section, row,
tier and ranking is authored by the conversion — against a headingless source, only
`quote` and `line` anchor kinds can resolve.

## 4. The reframing risk, and how the artifacts mitigate it

The round names its own central risk — **record-format distortion** — in
`corpus/fixtures/archives-r9/README.md` §"Reframing risk: record-format distortion
(named and mitigated)", and the round-9 lesson
(`corpus/lessons/2026-10-16-verifying-conversion-not-original.md`) re-derives it from
six independent measurements. The risk, in the README's words: a chat export is not a
structured record, and the conversion imposes structure the export does not have; a
CLEAN `verify-all` on these records "certifies record-format integrity against archive
bytes — not the external truth of anything the archives cite, and not the completeness
of their arguments."

The mitigations, all visible in the bytes (re-checked where noted):

- Claims are scoped as text-level observations ("the export records/states X") with a
  verbatim `span`; no record claim asserts an external fact.
- Spans and anchors are machine-extracted from the archive bytes, never retyped;
  claims-file spans are gate-verified, and record `span` cells are byte-checked
  (README: A `ok=5 bad=0`, B `ok=6 bad=0`, C `ok=8 bad=0`; I re-derived 19/19 with
  zero misses).
- Tiers never promote the exports above `export`; their cited works are `secondary`,
  marked "word-of-export only, not held locally" — the dictionaries, papers, museums
  and federations are named where the export names them, never opened.
- Bare chips and hosts stay marked `blocked-no-fetch` hops, never opened or inferred
  into URLs; each record's one exempt chain hop and one exempt integrity reference are
  exactly this class.
- Inter-archive hops are convergences, not citations (no archive cites another —
  re-derived 0/0/0), and each cross-archive anchor is verbatim in its target, so the
  convergence itself is checkable.
- The archives' own corrections are kept as rejections with flip-conditions rather
  than erased; each record's sweep proves only its own local re-run (no `saved-*` /
  `*-snapshot-*` copies under the archive directory).

Named residual distortion, not fixed: `text` cells paraphrase — only `span` cells and
chain anchors are verbatim, so read span+pointer, not prose; the exports are cut
mid-response (the r1 intake noted this), so an absent section in an archive is not an
answer of "no"; tallies like `RESOLVED_HOPS=6/7` grade anchor existence in the archive
bytes, not the strength of the export's argument.

The lesson's hardening of the same fact: **verifying a conversion is not verifying the
original** — the composed CLEAN binds exactly one hop (record → the source bytes
actually quoted); the chain of custody terminates at the export, and it cannot reach
what the export itself cites.

## 5. Honest limits and defects

1. **`corpus/fixtures/archives-r9/A-r9.md:50` (row C3) — a pointer/span line
   mismatch.** The pointer cell cites `research/deep-research-2026-09-28/A-shokunin-tradition.md:76`
   while the row's `span` cell occurs at line 86 (I confirmed: the span greps at
   A:86; A:76 is the "relevant distinction" sentence). The composed verdict stays
   CLEAN because no mode compares a row's `path:line` against its span's actual
   occurrence line: structure mode checks the pointer file's existence only, and
   claims mode reads the JSONL surface, never the record's rows. The lesson's
   independent 19-row audit found this single miss (18/19) and flagged it to the
   fixtures seat; `claims-r9.jsonl` A11 and the claims README pin A:86.
2. **The records' claims-table `span` column is outside every current gate check.**
   Its verbatimness rests on authoring discipline plus independent byte checks
   (19/19 re-derived here). Named as a candidate follow-up (round-10 menu), not a
   claim of the gate.
3. **A `to` cell written as `path#quote:text` drifts structure mode**
   (`CHAIN_HOP_UNRESOLVED` — the structure pointer check cuts a pointer at its first
   `:`). The records therefore use a declared source id or clean local path plus
   `anchor_kind`/`anchor` columns. Documented in the README's authoring notes;
   deliberately unfixed (no gate change this round).
4. **Coverage is a selection** (§3): ~one prose line in five under a span check; the
   conversion authors the structure, and its choice of spans is its unchecked act.
5. **Chain of custody stops at the export.** The archive's cited works are
   un-nameable from the bytes and un-fetchable by policy; the chip hops are exempt
   (counted, never resolved). No CLEAN on these records speaks about those sources.
6. **The exports are cut** (A's answer reaches only its first numbered section, B's
   only its first `(1)` section); a record structures what survived, and a missing
   section is not an answer of "no".
7. **Not re-derived by this seat:** the selftest run (the scribe measured
   `RESEARCH_GATE_SELFTEST: PASS (85 cases)` at the same gate), the receipts
   (not landed at writing), the 109/366 prose-line denominator (the lesson's
   accounting, carried), and the r8 pin/drift surfaces (their own note owns them).
   My battery: three composed runs, the raw-drift control, the claims run, fixture
   sha256 pins, span byte-presence counts (24/27 JSONL with the 3 by-design probes
   absent; 19/19 record spans), the coverage line unions, and the no-cross-citation
   grep.

## 6. What this note does not claim

- No external truth: nothing here verifies any dictionary, paper, museum, federation
  or account the archives cite. No fetch happened; zero network.
- No knowledge promotion: the archives stay tier `export`; this note adopts nothing
  from them and quotes only fixture/README/lesson text.
- No gate verdict and no scalar score; the round's admission is parent-owned.
- Not the receipts: the receipts-writer's cut is the round's receipts artifact; the
  runs above are this note's own and the fixture READMEs'.

## Pins (sha256, re-derived by this seat where marked)

| artifact | sha256 |
|---|---|
| `tools/research-gate.sh` (unchanged; fixture-led) | `46f5ddb39d5fafa220fb584121dba2f4a15e071a91fa42728849f3c7567c6ccd` |
| lane HEAD | `f11073ab81c3e0900cc37e47ec15a9913166f7aa` |
| `research/deep-research-2026-09-28/A-shokunin-tradition.md` (re-derived) | `9033857d4625555c7b778dfad6df80e3e1b24ed8bffa3fee2fd445b9c5540b85` |
| `research/deep-research-2026-09-28/B-multiagent-knowledge.md` (re-derived) | `6d8dbddd3e2d2f47dcb153c5a3347cc6321db4afc72cf07da40f0f7fe5022006` |
| `research/deep-research-2026-09-28/C-rank-taxonomy.md` (re-derived) | `e48fe70ff92055c217ac6ca6ce68e403aa5689fee8717f3bd0ccf5badc92321b` |
| `corpus/fixtures/archives-r9/A-r9.md` (re-derived) | `dfd2ae1a149b7c87f8ff399522f99c3461570c5ba06ba9d6b18254b15a3c3b9d` (round-12 revision; row C3 pointer `:76`→`:86`) |
| `corpus/fixtures/archives-r9/B-r9.md` (re-derived) | `abfa5290deda4d1708ba97028853b8a770f16ecda6f377dddda53d49cb2e3e86` |
| `corpus/fixtures/archives-r9/C-r9.md` (re-derived) | `97be0e69ccfb8a701bc5556f738553be8e7179c9b41110fe61c4a3cab4f2d1da` |
| `corpus/fixtures/archives-r9/README.md` (re-derived) | `ec312657c3872de77b45d44d135dd350e6b6cb378db621b4f2cbc61b5798a166` |
| `corpus/fixtures/claims-r9.jsonl` (re-derived) | `f6f0d1ab6b6cbd045035951c7eb4653406dc0853234a8077a8685509bfc94ff5` |
| `corpus/fixtures/claims-r9.README.md` (re-derived) | `64b63db670232bffede14bb589363b23017015ffbd8e0bf2643c9977b4847a40` |
| `corpus/lessons/2026-10-16-verifying-conversion-not-original.md` (re-derived) | `eb3fb8177fb28a27bb02b75e269291771af4d1b8c1bc226e1e76367e0bbeb948` |

## Re-run

```sh
cd chousa-shokunin
sha256sum tools/research-gate.sh        # 46f5ddb3… (unchanged this round)
for r in A B C; do
  bash tools/research-gate.sh verify-all corpus/fixtures/archives-r9/$r-r9.md \
    --claims corpus/fixtures/claims-r9.jsonl --root .. ; echo "exit=$?"
done
# expect per record: VERIFY_ALL sections=5 run=5 absent=0 drift-sections=0 findings=0
# drift=0 + RESEARCH_GATE: CLEAN, exit 0 (claims 10/10 · chains 6/7, 6/7, 7/8)
bash tools/research-gate.sh verify-all ../research/deep-research-2026-09-28/A-shokunin-tradition.md --root ..
# the raw-drift control: DRIFT sections=5 run=2 absent=3 drift-sections=1 findings=6 drift=5, exit 1
```

If any record byte changes, its sha row in the fixture README (and §Pins here) must move
with it; the composed tallies are properties of the pinned bytes at the pinned gate.