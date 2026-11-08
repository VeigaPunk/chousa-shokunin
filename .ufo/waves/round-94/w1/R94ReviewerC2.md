# R94ReviewerC2 — C2 (`C2-CURATION-R94`) attack report

Seat R94ReviewerC2, leaf. Attacked tree: carrier **C `352924bbea624caf3771ef291be98fd4ec679dda`**
("round-94: carrier C — six control receipts emitted at F and the 34-row pins table"), cloned
`--shared` to `$S=/fast/scratch/hyaku/chousa-r94/R94ReviewerC2/repo` and checked out; HEAD and a clean
work tree are in `receipts-R94ReviewerC2/tree-identity.txt` (`git rev-parse HEAD` → C, `status --porcelain`
→ 0 lines). The lane root's copies of the two counters, both entries, `SOURCES.md`, the leg table, the pins
table and `claims.md` `cmp`-match the clone byte for byte. Every fixture is a scratch copytree of the
committed bytes; the clone and the lane were never written. No tool installs (host `python3`/`git` only).
No `lsp` device is mounted (`read xd://lsp` → "No such tool"), so no server answered these Python files;
semantic checks were done by importing the counters and executing `punct_quote_cell`,
`q_shape_violation`, `locates` directly (`D-detector-cases.txt`, `locates-r93-vs-r94.txt`), not by grep.

## Predicate at C

Command (clone root): `python3 -B corpus/evidence/round94/curation-r94.py --root .`
Receipt `receipts-R94ReviewerC2/c2-counter-clean.txt`, **exit 0**:

```
... Q_ROWS=20 Q_SHAPE_FAIL=0 Q_WSQUOT=0 Q_PUNCTQUOT=0 ... WARRANT_OK=17/17 TFREQ_OK=17/17 ... DUP_QIDS=0 ... LEGS_MEASURED=16/16
VERDICT fields_hold=1 legs_ok=16/16 DETECTOR_WITNESS=17/17
CURATION_R94=PASS
```

All eight named fields and the three VERDICT sub-fields hold; field-by-field check in
`predicate-fields.txt` (all `OK`).

Command: `python3 -B corpus/evidence/round94/curation-controls-r94.py --root . --work $S/work-final`
Receipt `c2-controls-clean.txt`, **exit 0**:

```
CONTROLS=PASS CARRIED_REFUSED_BOTH=4/4 WS_NAMED=2/2 PUNCT_NAMED=2/2 PUNCT_SHAPE_GREEN_R93=1/1 DUPCOUNT_1=1/1 PRIOR_REGRESSION=7/7
```

All six named fields hold. The leg table holds exactly the 16 emitted names (`legset.txt`: sorted diff
empty, `EXPECTED_LEGS = 16` at `curation-r94.py:109`).

## Findings (severity order)

### F1 — LOW: `Q_PUNCTQUOT` is not the "located-quote population" the claim names

`claims.md:81-82` says the class is "counted on the located-quote population before the shape filter";
the counter docstring (line 8) and the leg comment (line 542) repeat it. The implementation
(`curation-r94.py:373-381`) counts every **three-cell line** of `## Located quotes` after only the
header/separator skip, before the qid test, the source test and `locates()` — the code's own comment on
line 378 says "every three-cell quote row", and named limit 1 (`claims.md:109-110`) discloses only source
resolution.

- Command/fixture: pristine mirror + `| note | S999 | "—" |` inserted after Q13; run
  `python3 -B .../curation-r94.py --root <tree>`. Receipt `C1-nonq-punct-r94.txt`, **exit 1**:
  `Q_ROWS=20 ... Q_PUNCTQUOT=1`, `Q_SHAPE ... qid=note row=| note | S999 | "—" |`,
  `LEG_FAIL PUNCTQUOT search-transparency-reporting-r84.md note`. A non-`Q` row that is not a located
  quote is counted and named by the leg.
- On the battery's `x1-punct-dash` tree the count is not a subset of located rows either:
  `Q_ROWS=19 Q_SHAPE_FAIL=1 ... Q_PUNCTQUOT=1` (`c2-controls-x1-r94.txt`, exit 1).
- Clean tree: `Q_PUNCTQUOT=0`, PASS — no clean-tree false positive from the population.
- The "punctuation-heavy longer quote" false positive is structurally excluded: `punct_quote_cell` fires
  only when the whole content has no `[A-Za-z0-9]`. Direct calls (`D-detector-cases.txt`) give
  `punct_quote_cell=False` for `"— date when each source was last searched or consulted."`, for an em
  dash inside a longer quote, and for the clean Q10 quote (commas/slash/hyphens); the clean tree's 20
  located quotes all carry an ASCII alphanumeric.

**FIRES (low, claim wording): the counted population is pre-qid/pre-source/pre-location, not the
located-quote population. No clean-tree effect.**

### F2 — LOW: the class is ASCII-only while the claim says "no alphanumeric character"

`PUNCT_RE = re.compile(r"[A-Za-z0-9]")` (`curation-r94.py:110`); `claims.md:81` and the docstring line 4
say "no alphanumeric character".

- Real single-symbol quote: Q9 (source S023) replaced by `"©"`. `©` is a genuine substring of the cited
  S023 capture (`A-copyright-capture-check.txt`: `contains_copyright=True`, one occurrence at line 22689
  `'©'`, capture `f5545a194c06ab421875b047.txt`), so this is a real quote of a real manual, not a
  synthetic string. Receipt `A-copyright-r94.txt`, **exit 1**:
  `Q_SHAPE ... quote=<punctuation> row=| Q9 | S023 | "©" |`, `Q_PUNCTQUOT=1`,
  `LEG_FAIL PUNCTQUOT ... Q9`. r93 on the same bytes (`A-copyright-r93.txt`, **exit 1**) reports
  `Q_SHAPE_FAIL=0`, `QUOTES_LOCATED=20/20` and refuses at `LEG_FAIL FLOOR`, `LEG_FAIL WARRANT`,
  `LEG_FAIL TFREQ` — so the over-refusal is verdict-neutral here: classification, not a new refusal.
- Bare `"—"`, `"..."`, `"©"`, `"§"` are refused; `"§ 4.2"` passes (digit). This is the PUNCTQUOT class;
  named limit 3 (`claims.md:111-113`) discloses the punctuation-only rule, and the routed captures make
  it harmless for r93 discrimination: the largest whitespace-separated punctuation-only run in any cited
  capture is 3 tokens (`S023`, `punct-run-scan.txt`), below `MIN_TOKENS = 7`, so r93's FLOOR refuses
  every punctuation-only quote that can locate in these captures.
- The undisclosed part: `"数据库"` and `"Ω"` are `.isalnum() == True` in Python (letters, not
  punctuation) yet are refused and labelled `quote=<punctuation>` (`B-cjk-r94.txt` exit 1;
  `D-detector-cases.txt`: `cjk_letters ascii_alnum=False isalnum=True punct_quote_cell=True`, same for
  `Ω`). A future entry citing a non-Latin source would have a lexical quote refused and mislabelled, and
  the claim's sentence is false for that input. No committed instance: the routed entries cite only
  S214/S018/S023 (English captures).

**FIRES (low, class definition / named-limit gap): the class it refuses is PUNCTQUOT
`quote=<punctuation>`. Harm is bounded to diagnostics and the future-entry rule — on the routed entries
it is verdict-neutral; for non-Latin alphanumerics it is an undisclosed over-refusal and a wrong label.**

### F3 — LOW: frozen predicate text is not a verbatim line (values hold)

`claims.md:96-98` and the seat spec quote `CONTROLS=PASS … PUNCT_SHAPE_GREEN_R93=1/1
PRIOR_REGRESSION=7/7`. The observed line inserts `DUPCOUNT_1=1/1`
(`curation-controls-r94.py:200-203`, key built from `fl_old.get('UNENTAILED_TERM')`) between the last two
named fields. Receipt `controls-predicate-contiguous.txt`: command
`grep -cF -- 'PUNCT_SHAPE_GREEN_R93=1/1 PRIOR_REGRESSION=7/7' c2-controls-clean.txt` → `0`, **exit 1**;
the second check `grep -cF -- 'LEGS_MEASURED=16/16 Q_SHAPE_FAIL=0 Q_WSQUOT=0 Q_PUNCTQUOT=0 Q_ROWS=20'`
→ `0`, **exit 1** (the counter prints `Q_ROWS` before `Q_SHAPE_FAIL` and `LEGS_MEASURED` last). Every
named field is present with the expected value (`predicate-fields.txt`, all `OK`).

**FIRES (low, predicate-text fidelity). K1 is not fired on values; a checker doing verbatim line
matching would fail.**

### F4 — LOW (framing): the new `locates()` guard has no pipeline force

`locates()` (`curation-r94.py:219-222`) adds `bool(PUNCT_RE.search(quote))`. `q_shape_violation`
(252-266) already refuses `quote=<punctuation>` on the same content, and the main loop calls `locates`
only after the shape branch (382, 391); the two strings differ only by whitespace stripping, which cannot
change the presence of `[A-Za-z0-9]`.

- Instrumented copy (`counter-guard.py`, appended `BLOCKED` list) run on the clean tree, x1 and the `©`
  tree: `GUARD_BLOCKS=1 BLOCKED=['—']` in all three (`E-guard-clean.txt`, `E-guard-x1.txt`,
  `E-guard-copyright.txt`) — the single block is the witness's synthetic
  `locates("—", "before — after")`, never a routed quote.
- Removing the guard **and** its witness row leaves the clean-tree field line identical except
  `DETECTOR_WITNESS=16/16` vs `17/17`, both `CURATION_R94=PASS` (`E2-noguard-clean.txt`,
  `E2-orig-clean.txt`, exit 0). Removing the guard with the witness row kept fails
  `LEG_FAIL WITNESS 16/17 bad=1` (`m5-noguard-witness.txt`, exit 1).

So answer Q3 is **no verdict change on the two routed entries**. Claim line 82 "`locates()` returns False
for a punctuation-only quote" is true at function level (`locates-r93-vs-r94.txt`: r93 True, r94 False on
`"—"` / `"before — after"`); named limit 2 (`claims.md:110-112`) covers the leg as a second witness, not
this guard, so the After narrative slightly overstates the guard's role. Not a predicate failure.

## Per-question answers

1. **Population.** `Q_PUNCTQUOT` counts pre-shape three-cell lines, including non-`Q` rows
   (`| note | S999 | "—" |` → 1), not the located-quote population the claim names — **FIRES (low)**.
   It cannot fire on a clean entry's punctuation-heavy longer quote: any ASCII alphanumeric anywhere in
   the cell suppresses it; committed clean tree `Q_PUNCTQUOT=0` — **HOLDS** on that direction.
2. **Over-refusal of a single symbol.** A real `"©"` from the cited S023 capture is refused as
   `quote=<punctuation>` / PUNCTQUOT; `§`, `→`, `—`, `...` likewise. On the routed captures this is
   verdict-neutral (r93 also fails the same trees; max punctuation run 3 < `MIN_TOKENS=7`), and limit 3
   discloses the punctuation-only rule. `"数据库"`/`"Ω"` are alphanumeric but refused and mislabelled —
   undisclosed — **FIRES (low)**.
3. **`locates()` guard on the two routed entries.** No existing verdict changes; instrumented pipeline
   blocks: 0 (only the witness blocks); guard removal + witness-row removal gives the same PASS field
   line; guard removal with the witness kept fails WITNESS — **HOLDS**.
4. **`EXPECTED_LEGS=16` load-bearing.** Yes. Delete the PUNCTQUOT leg only: `m1-delete-leg.txt`,
   **exit 1** — `LEG_FAIL ARITY expected=16 measured=15`, `LEG_FAIL LEGSET missing=PUNCTQUOT extra=none`,
   `CURATION_R94=FAIL`. Lower arity alone: `m2-delete-leg-arity15.txt`, **exit 2** —
   `CURATION_R94=SETUP leg table holds 16 names, EXPECTED_LEGS=15`. Vacuous leg (`True`) on the clean
   tree still PASSes (`m4-vacuous-leg.txt`), consistent with the leg being a second witness. Coherent
   joint edit of counter + `legs.txt` PASSes C2 (`m3b-coherent-joint.txt`, exit 0) — **HOLDS as written**;
   that edit is caught only by C1's pin row (`instrument-pins.txt:22 … driver
   corpus/evidence/round94/controls/legs.txt`, `pins-legs-row.txt`).
5. **`PUNCT_SHAPE_GREEN_R93` re-derivation.** Real. `curation-controls-r94.py:156-163` runs the OLD
   counter as a fresh subprocess on the x1/x2 trees each invocation; the trees carry the mutations
   (`| Q2 | S214 | "—" |` / `"..."` at line 23). Forcing a fake OLD to print `Q_SHAPE_FAIL=1` flips the
   field to `PUNCT_SHAPE_GREEN_R93=0/1`, `FAIL punct-classification`, `CONTROLS=FAIL`, exit 1
   (`sensitivity-battery-full.txt`), while the real run is `1/1` PASS — **HOLDS**.
6. **Classification framing.** Honest. Quote: "This is a classification claim: r93 fails those trees too,
   but it cannot name the cause." (`claims.md:100-101`). Same bytes, r93: `Q_SHAPE_FAIL=0`,
   `Q_PUNCTQUOT_count=0`, `punct_reason_count=0`, `CURATION_R93=FAIL` on both trees
   (`c2-controls-x1-r93.txt`, `c2-controls-x2-r93.txt`, `r93-no-punct-class.txt`, exit 1 each); the `©`
   tree is likewise refused by r93. No new refusal — **HOLDS**. F3 is a text-fidelity issue, not a
   framing issue.

## Residual risk / verification gaps

- **Coherent joint edit.** Deleting the leg, lowering `EXPECTED_LEGS` and deleting the name from
  `controls/legs.txt` PASSes C2 (`m3b`). C2's arity tripwire is defeated; the defense is C1's pin row
  (driver role) byte-checking the table. K4 as written ("deleting it must change the verdict through the
  named `LEG_FAIL ARITY` line") is met only by the leg-only deletion.
- **Non-Latin sources.** The capture store contains CJK/other-script captures, but none is cited by the
  two routed entries; a future entry quoting one would hit the ASCII-only class (F2).
- **`Q_PUNCTQUOT` is pre-shape.** `Q_PUNCTQUOT <= Q_ROWS` does not hold on forged trees (x1: 1 vs 19;
  C1: 1 extra row with `Q_ROWS=20`); a consumer treating it as a subset of located quotes is wrong.
- **No test for a 4-cell punctuation row**: `punct_quote_cell` returns False (`len != 3`); QSHAPE reports
  `cells=4`, so the tree still fails, but the class count stays 0.
- C1 and C3 were not attacked by this seat; only C1's pins row was read for the `legs.txt` pin cited above.

VERDICT: R94ReviewerC2 C2 held — predicate and all four kill rules survive at C (all named fields, exit 0; r93 fails both trees without naming the class; Q_PUNCTQUOT is 1 on both forged trees and 0 on the clean tree; deleting the leg trips ARITY/LEGSET), with three low findings (population wording, ASCII-only "alphanumeric" and its undisclosed non-Latin over-refusal, non-verbatim predicate text) and one framing note (the `locates()` guard is unreachable in the pipeline and only forced by its witness row).
VERDICT: R94ReviewerC2 C1 n/a — not attacked by this seat.
VERDICT: R94ReviewerC2 C3 n/a — not attacked by this seat.
