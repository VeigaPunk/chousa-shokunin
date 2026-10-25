# CritC2Framing — is "a path named in SCORECARD.md or a claims file" a gate-registry surface?

seat: critic (leaf). no fetch, no production write. 2026-10-25.
Item: attack C2's framing as calibration; list verifiers that stay outside the frozen set after
the extension; one-sentence judgement tree-vs-prose.

## Verdict

**C2's predicate is measurable and its counter is honest — but the measured property is "the
registry agrees with the prose that names paths", not "the registry covers the gate table".**
The extension samples on *mention*, not on *dependence*: 13 past-round instruments with no
declared verdict map enter, the one gate-shaped executable with a real verdict map stays out, and
a byte-identical tree gains or loses an entry point by editing one sentence. C2 can reach
`UNREGISTERED=0` and leave the residual below. That is a named limit, not a counter defect — but
the claim's sentence "makes the registry agree with the tree the verdicts rest on" is not what the
counter shows and must not be scored as if it were.

## Counterexample (strongest available)

`corpus/evidence/round34/self-audit.py` — the claim's own motivating case (round-45 D8) — says of
itself, line 12: `The tool COUNTS, it does not gate: exit is 0 whenever the set was readable,`.
`round26-measure.sh:6`: `# A probe, not an admission gate: exit 0 only means`. The flagship entry
the extension adds has no verdict map, so its `verdict map` cell can only be invented.

Inversion, same experiment: `corpus/evidence/round45/tag-count.py` **is** a gate — declared
verdict map (`corpus/QUALITY.md:588-589`: `TAGGED=k/n`, `exit 0 only when every claim row is
tagged`), a control (`round45/controls/tag-control-r35-r44.txt`), a real row (`SKILL.md:111`) —
and it is **outside** C2's set, because it is named in QUALITY.md/SKILL.md, never SCORECARD.md or
a claims file. The counter can neither reward its registration nor detect the row's deletion.

Prose-only membership, tree held byte-identical (three historical SCORECARD lines naming
`corpus/evidence/round24-measure.sh` deleted in a `/tmp` symlink root):

    # SCORECARD mentions removed; tree symlinked, unchanged
    GATES_ROWS=30  REGISTERED=55/71  UNREGISTERED=16  C2=FAIL
    # same root, SCORECARD restored
    GATES_ROWS=30  REGISTERED=55/72  UNREGISTERED=17  C2=FAIL

`ENTRY_POINTS` moved 72→71 with zero tree change, so `ENTRY_POINTS≥71` is not a tree property: the
claim's "Before" 71 is reproducible either by the base tree or by deleting a past-tense sentence
today, and the live tree already reads 72 because C1's executor created
`tools/inference-ground.py` — C2's denominator is coupled to C1's landing.

## Evidence (decisive lines verbatim)

1. `python3 corpus/evidence/round46/c2-count.py --list` (real exit 1):
   `ENTRY_POINTS=72 (tools=8 counters=50 named=70)` / `GATES_ROWS=30` / `REGISTERED=55/72` /
   `UNREGISTERED=17` / `C2=FAIL`, with 17 `UNREGISTERED_PATH` lines.
2. Lane census (`.py`/`.sh`, `.git`/`.jj`/`.ufo` excluded) against the counter's own
   `entry_points()`: `CENSUS=82  IN_C2_SET=72  OUTSIDE_SET=10`.
3. Invoked-path scan (`(python3|bash) (tools|corpus|scripts)/…py|sh`) of the other two prose
   surfaces:
   `corpus/QUALITY.md: invoked=12 existing=12 outside_C2_set=4` (`round29/prose-check.py`,
   `round30/rerun-check.py`, `round32/q33-check.py`, `round45/tag-count.py`);
   `SKILL.md: invoked=57 existing=57 outside_C2_set=1` (`round45/tag-count.py`).
   SKILL.md's own `entry` column is the tightest surface (56/57 already in set) and its blind
   spot is inverted: the table names a gate the census cannot see.
4. Verdict-map census over the 13 historical entries' headers (`|| exit 1` guards excluded):
   **0 declare a verdict map; 2 explicitly disclaim gating** (`round26-measure.sh:6`,
   `self-audit.py:12`).
5. Exit-contract presence in the *naming* prose of the 17: **0/17**
   (`round25-meta-differential.sh` cited as `→54/54 (27 fixtures)`; `d2-census.py` as `prints … 21`).
   `SKILL.md:77` requires a `verdict map` cell per row; the naming prose supplies none, so 17
   verdict maps must be authored — and C2's kill rule does not measure row truth. The "named
   limit" is 100% of this claim's delta.
6. No consumer executes Gates rows: `tools/research-gate.sh` parses `## Claims`/`## Sources`
   (`table_rows()` :869) and never SKILL.md; `c2-count.py` is the only reader of `## Gates`.
   "Registered" means "a line exists".

## Residual list — executable verifiers OUTSIDE the frozen set after the extension

Tier A — gate-shaped (verdict map and/or control), outside because its naming lives in
QUALITY.md / SKILL.md:

- `corpus/evidence/round45/tag-count.py` — QUALITY 64 check, `SKILL.md:111` row, exit contract, control.

Tier B — receipt-dependent instruments, outside for the same reason (leg B's name pattern does not
reach them; leg C never reads receipts, lessons, READMEs):

- `corpus/evidence/round45/build-spans.py` — "a committed builder" a round-45 verdict rests a
  figure repair on (`corpus/lessons/round-45.md:42`); produces `round45/spans.tsv`, consumed at
  `corpus/evidence/round45/c3-count.py:114`.
- `corpus/evidence/round46/build-spans.py` — produces the `spans.tsv` C3 hashes this round; named
  in no SCORECARD row and no claims file (claims names only `spans.tsv`).
- `corpus/evidence/round25-meta-oracle.py` — invoked at
  `round25-meta-differential.sh:40`; decides the SCORECARD-cited 54/54.
- `corpus/evidence/round26-registry-oracle.py` — `ORACLE=$SCRIPT_DIR/…` (`round26-registry-differential.sh:9`).
- `corpus/evidence/round30/rerun-check.py` — QUALITY 27 (`QUALITY.md:191`, `lessons/round-30.md:17`),
  prints `RERUN_RECEIPTS=5/6`, exit 1.
- `corpus/evidence/round32/q33-check.py` — QUALITY 33, "Shown able to fail" (`QUALITY.md:255`).
- `corpus/evidence/round29/prose-check.py` — `QUALITY.md:155`.
- `corpus/evidence/round25-holds/battery.sh` — named by `lessons/round-26.md`, `lessons/round-33.md`,
  `corpus/evidence/README.md`, `round25-final-pin.json`; leg B never looks in `round25-holds/`.
- `corpus/evidence/round25-sources-census.sh` — named in `corpus/README.md` only.

`.ufo/waves/`: `gen-w1-spec.py` (r32,33,35,36,38,45,46), `round-44/make-settle-tables.py`,
`round-45/assimilation/map-staged.py`, `assimilation/validate/` copies. A grep of `corpus/evidence`
and `.ufo/reports` found **no** receipt depending on them; they are wave instrumentation and belong
in no gate registry. C2 excludes them by path prefix, not by kind — the same accident that admits
`self-audit.py`.

## Impacted axes

- **calibration:** `REGISTERED=n/n` would license a statement about the tree; it is a statement
  about three documents, one of which (QUALITY.md) the counter never reads.
- **operability:** 17 rows no runner executes and no self-test backs — the table grows, the
  certified executable surface does not.
- **depth:** C3's `CAPTURE_BOUND` rests on `round46/build-spans.py`, itself unregistered.
- **authority:** one executable now carries two statements (SCORECARD evidence cell + Gates row)
  with no precedence rule; `round24-measure.sh` already sits in SCORECARD:1256-1258 as a
  past-tense cell and is now also owed a forward-looking row.

## Smallest safe correction

Keep A and B; repair leg C's *selector*, as a route (the predicate is frozen — never edit C2 mid-round):

1. **Derive from invocations, not mentions.** Scan the receipt corpus
   (`corpus/evidence/**/*.{txt,json,md}`) plus QUALITY.md/SKILL.md for *executed* paths and each
   claims row's `Counting command:`. This picks up the Tier-B entries a verdict actually ran with
   no threshold change.
2. **Two kinds, two obligations.** A derived path holds either a `kind=gate` row (verdict map +
   self-test + control) or one `kind=instrument` allowance (inputs, outputs, provenance digest, no
   verdict). The five `*-measure*` scripts and `self-audit.py` become instruments by their own
   header text; `tag-count.py` becomes a gate; invented verdict maps disappear.
3. **Guard the prose-deletion hole:** print `CENSUS−SET` (82−72 today) so a prose edit that drops
   an entry point shows as delta growth, not as a lower denominator.

Cheapest catch-all needing no new tooling: assert
`set(SKILL.md entry-column paths) ⊆ ENTRY_POINTS` — it fails today on exactly `tag-count.py`.

## Judgement (one sentence)

The extension makes the registry agree with the **prose**, not the tree — membership follows
whether a document names a path, so 10 lane executables (one a real gate, two the span builders
C3's receipts rest on) stay outside while 13 historical instruments, two of which declare they do
not gate, come in.

## Pointers

- `corpus/evidence/round46/c2-count.py:44-59` (leg C selector), `:77` (row rule), `:97-101`.
- `corpus/evidence/round34/self-audit.py:12`; `corpus/evidence/round26-measure.sh:6`.
- `corpus/QUALITY.md:588-589`; `SKILL.md:111`; `SKILL.md:77` (row schema).
- `corpus/lessons/round-45.md:42`; `corpus/evidence/round45/c3-count.py:114`.
- `corpus/evidence/round25-meta-differential.sh:40`; `corpus/evidence/round26-registry-differential.sh:9`.
- `corpus/evidence/round46/claims.md` (frozen C2 legs, `ENTRY_POINTS ≥ 71`, `UNREGISTERED=0`).

Tooling: none installed or upgraded. Scratch `/tmp/chousa-r46-CritC2Framing` + temp files removed.
