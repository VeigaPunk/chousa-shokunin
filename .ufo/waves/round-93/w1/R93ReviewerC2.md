# R93ReviewerC2 — C2 `C2-CURATION-R93` attack report

Seat: `R93ReviewerC2` (leaf). Lane: chousa round 93. L1 `ChousaR93` holds the planner seat, the freeze and the
integration.

Tree under attack: carrier **C2** `754b62fb6adc60e44e12375af5461a0ebe302994` (freeze **F2**
`b7241252c2358613d3b22b7d0454d98c56dab373` plus the six committed control receipts), cloned with
`git clone --shared /home/vgpnk/Projects/shokunin/chousa-shokunin /fast/scratch/hyaku/chousa-r93/R93ReviewerC2/repo`
and checked out at C2 (`git rev-parse HEAD` = `754b62fb…`, `rev-parse --show-toplevel` = the scratch clone).
No production edit, no lane/fleet git mutation, no commit, no network, no `sudo`, no host service touched.
Tooling: nothing installed or upgraded this round. Every run used `python3 -B`; the attacked tree stayed clean
(`git -C <clone> status --porcelain` empty after all runs — receipt
`R93ReviewerC2-c2-adjacent-carrier-and-writecheck.txt`).

Frozen prose: `.ufo/waves/round-93/claims.md` (C2 at lines 65–109). Machine form:
`.ufo/waves/round-93/claims.json` (C2 at lines 56–87, sha256 `db82f98c…`, matching the pins table).

Receipts written to this wave folder (all paths relative to
`/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-93/w1/`):

| receipt | what it holds |
|---|---|
| `R93ReviewerC2-c2-counter.txt` | canonical clean counter run, rc 0 |
| `R93ReviewerC2-c2-controls.txt` | canonical controls battery run, rc 0 |
| `R93ReviewerC2-c2-prior-r92-ws.txt` | r92 on the two whitespace trees (Before evidence, reproduced) |
| `R93ReviewerC2-c2-probes.txt` | E1–E11 population/clean-row/width probes |
| `R93ReviewerC2-c2-deletions-width.txt` | D1–D4: WSQUOTE leg deletion, DECISION_WIDTH print deletion, shape-fixed r92 |
| `R93ReviewerC2-c2-claims-json.txt` | machine form vs instrument stdout tokens |
| `R93ReviewerC2-c2-evidence-before-presence.txt` | the cited Before receipt at F, C and in the lane |
| `R93ReviewerC2-evidence-before-c2-prior-accepts-asfound.txt` | the untracked lane copy, verbatim |
| `R93ReviewerC2-frozen-c2-prior-controls.txt`, `…-c2-prior-landing.txt` | the two frozen C2 receipts, copied from C2 |
| `R93ReviewerC2-c2-probe-harness.py`, `…-c2-mutation-harness.py`, `…-c2-harness-commands.txt` | the exact generating code and command lines for the probe and mutation receipts |
| `R93ReviewerC2-c2-adjacent-carrier-and-writecheck.txt` | later carrier diff, write-isolation check |

## Claim as frozen

claims.md C2 predicate (lines 91–97): counter prints `CURATION_R93=PASS` with
`LEGS_MEASURED=15/15 Q_SHAPE_FAIL=0 Q_WSQUOT=0`, controls print
`CONTROLS=PASS CARRIED_REFUSED_BOTH=4/4 WS_NAMED=2/2 WS_SHAPE_GREEN_R92=1/1 DUPCOUNT_1=1/1
PRIOR_REGRESSION=7/7`, and (line 96–97) “this is classification, not a refusal r92 lacks: r92 fails those trees
downstream”.

**Both canonical runs reproduce the frozen predicate exactly.**

- `python3 -B corpus/evidence/round93/curation-r93.py --root .` → rc **0**:
  `… Q_ROWS=20 Q_SHAPE_FAIL=0 Q_WSQUOT=0 SOURCE_STATUS_OK=20/20 USED_BY_OK=20/20 … WARRANT_OK=17/17
  TFREQ_OK=17/17 … DUP_QIDS=0 … LEGS_MEASURED=15/15` / `VERDICT fields_hold=1 legs_ok=15/15
  DETECTOR_WITNESS=11/11` / `CURATION_R93=PASS`. Receipt `R93ReviewerC2-c2-counter.txt`.
- `python3 -B corpus/evidence/round93/curation-controls-r93.py --root . --work <scratch>` → rc **0**:
  `CONTROLS=PASS CARRIED_REFUSED_BOTH=4/4 WS_NAMED=2/2 WS_SHAPE_GREEN_R92=1/1 DUPCOUNT_1=1/1
  PRIOR_REGRESSION=7/7`. Receipt `R93ReviewerC2-c2-controls.txt`.

C2's **scored predicate holds**. The findings below are in the frozen text around it (named limit, kill-rule
machine form) and in the leg's construction; none of them changes the PASS line at C2.

## Direct answers to the six attack questions

**(1) Is `Q_WSQUOT` counting the intended population, and can it fire on a clean registry-shaped row?**
The population is exactly “three-cell rows in `## Located quotes` whose quote cell strips to empty”
(`curation-r93.py:325`, condition `len(cells) == 3 and not cells[2].strip().strip('"').strip()`), counted before
`q_shape_violation` (`:327`). It **cannot** fire on a registry-shaped row with real quote content: E1 clean tree
`Q_WSQUOT=0` over 20 rows; E10 (a clean row with the content padded by spaces *inside* the quotes,
`| Q2 | S214 | "  date when each source was last searched or consulted.  " |`) → `Q_WSQUOT=0`, rc 0,
`CURATION_R93=PASS`. **HOLDS** for the false-positive direction. Two real scope facts: the predicate is
quote-**emptiness**, not whitespace (E3 empty cell → `Q_WSQUOT=1` with `Q_SHAPE … quote=<empty>`; E4 bare `"` →
same), and it is not restricted to `Q<n>` rows or to located rows (E11 `| note | S214 |  |` → `Q_WSQUOT=1` with
`Q_SHAPE … qid=note`). Receipt `R93ReviewerC2-c2-probes.txt`, cases E1/E3/E4/E10/E11, rc 0/1/1/0/1.

**(2) Does the WSQUOTE leg fail for the right reason on each whitespace tree, and is a four-cell row counted?**
Yes on both trees, at the right qid and with the right reason:
- space: `Q_SHAPE search-transparency-reporting-r84.md quote=<whitespace> row=| Q2 | S214 | " " |` and
  `LEG_FAIL WSQUOTE search-transparency-reporting-r84.md Q2`, `Q_WSQUOT=1` (E2, rc 1);
- tab: same two lines with `row=| Q2 | S214 | "<TAB>" |` (built tree `e2b-ws-tab` / the battery's `ws-tab` case),
  `Q_WSQUOT=1` (`R93ReviewerC2-c2-probes.txt`, `R93ReviewerC2-c2-controls.txt`).
A **four-cell** whitespace row is **not** counted: E5 `| Q2 | S214 | " " | extra |` → `Q_WSQUOT=0`,
`Q_SHAPE … cells=4`, rc 1. The row is still refused, by QSHAPE; the count simply skips it (`:325` width guard).
Receipt `R93ReviewerC2-c2-probes.txt` E2/E5, rc 1/1.

**(3) Is `EXPECTED_LEGS=15` load-bearing?**
Yes against a naive deletion, and only through arity. D1 (scratch copy with the WSQUOTE `legs.append` removed,
`EXPECTED_LEGS` left 15) on the clean tree → rc **1**, `VERDICT fields_hold=1 legs_ok=14/14`,
`CURATION_R93=FAIL`, **zero `LEG_FAIL` lines** (the arity mismatch is the only signal). D2 (leg removed *and*
`EXPECTED_LEGS = 14`) → clean tree rc **0** `CURATION_R93=PASS`; whitespace tree rc **1** with the same
`LEG_FAIL FLOOR/QSHAPE/WARRANT` set as the full counter minus `LEG_FAIL WSQUOTE`. So the constant breaks a
deletion that does not adjust it; a deletion that adjusts it changes no verdict on any tree that discriminates
WSQUOTE, because `fields_hold` still carries `and not ws_quote_rows` (`:511`). Receipt
`R93ReviewerC2-c2-deletions-width.txt` D1/D2.

**(4) Does `DECISION_WIDTH` fire for a wrong-width row, and is it only observability?**
Yes and yes. E9 (one decision row extended to five cells) → exactly one
`DECISION_WIDTH search-transparency-reporting-r84.md row=| Recording when a resource changed | … | extra |
cells=5`, rc 1, `LEG_FAIL WARRANT 16/16 width_fail=1 count_bad=0`. D3 (same tree, print loop at
`curation-r93.py:492-493` deleted) → no `DECISION_WIDTH` line, **same** `LEG_FAIL WARRANT … width_fail=1`,
rc 1, `CURATION_R93=FAIL`. The refusal is the `not decision_width` conjunct (`:509`); the print is observability,
exactly as named limit (2) says. Receipt `R93ReviewerC2-c2-deletions-width.txt` D3.

**(5) Does `WS_SHAPE_GREEN_R92` hold if r92's shape test changes?**
No — it is a live re-execution of the r92 counter, not an assertion over pinned bytes. D4: a scratch copy of
`round92/curation-r92.py` whose shape test is the r93 logic (`inner = cells[2].strip().strip('"').strip()`),
driven through a scratch copy of the controls with `OLD` re-pointed, gives
`Q_SHAPE_FAIL=1` for r92 on both trees and `CONTROLS=FAIL … WS_SHAPE_GREEN_R92=0/1` (rc 1). The assertion is
*sensitive* (it will not silently pass), but it fails the whole battery, and its failure line still reads
`FAIL ws-classification: r92 Q_SHAPE_FAIL=0 on both whitespace trees` — the observed value is not printed on the
failure path. `round92/curation-r92.py` is **not** in the 22-row pins table (rows cover round89/round90 and
round93 instruments plus the six receipts), so r92's bytes can move without C1 noticing and this control is the
only detector of that move. Receipt `R93ReviewerC2-c2-deletions-width.txt` D4.

**(6) Is “classification, not refusal” honest?**
In the prose: yes, explicitly. claims.md C2 Before: “r92 reports `Q_SHAPE_FAIL=0` and **refuses the tree only
downstream** (`LEG_FAIL FLOOR`, `LEG_FAIL WARRANT`, `LEG_FAIL TFREQ`), so the cause is never named”
(measured identically on both trees, `R93ReviewerC2-c2-prior-r92-ws.txt`, r92 rc 1 with exactly those three
`LEG_FAIL`s); predicate line 96–97 quoted above; the battery docstring: “The discrimination here is
classification, not refusal: r92 already fails the whitespace trees”. In the **machine form it is not honest**:
`claims.json` C2 `predicate.controls` demands `PRIOR_ACCEPTED=4/4` (line 69) and `kill_rules.K2` reads
“a forgery accepted by r93, the positive refused, or **r92 refusing a forgery**” (line 80). Both say the prior
*could* or *should* accept the forgeries, and K2 fires when r92 refuses one — while C2's entire battery asserts
r92 rc=1 on all six trees. The machine form contradicts the prose and the measurement.

## Findings by severity

### F1 — HIGH — `claims.json` C2 controls predicate is unsatisfiable by the instrument
Command: `grep -c 'FORGERY_REFUSED=4/4' …/R93ReviewerC2-c2-controls.txt` → **0**;
`grep -c 'PRIOR_ACCEPTED=4/4' …` → **0**. The controls source prints neither token: the only `FORGERY_REFUSED`
it emits is the child's own 7/7 line re-printed by the `regression:` line (`curation-controls-r93.py:165-167`),
and it never prints `PRIOR_ACCEPTED`. Observed actual line: `CONTROLS=PASS CARRIED_REFUSED_BOTH=4/4 WS_NAMED=2/2
WS_SHAPE_GREEN_R92=1/1 DUPCOUNT_1=1/1 PRIOR_REGRESSION=7/7` (rc 0). The machine sentence (line 58) and
`predicate.controls` (lines 67–70) therefore cannot be satisfied by the committed instrument at any revision; a
machine scorer reading `claims.json` marks C2 unmet even though claims.md's predicate holds. The machine `predicate.fields` also omits
`Q_ROWS=20`, `WARRANT_OK=17/17`, `TFREQ_OK=17/17`, `DUP_QIDS=0` that the sentence names. Receipt
`R93ReviewerC2-c2-claims-json.txt`; frozen prose receipt `R93ReviewerC2-c2-controls.txt`.

### F2 — HIGH — `claims.json` C2 K2 is inverted and implies r92 accepted the trees
`kill_rules.K2` (line 80): “a forgery accepted by r93, the positive refused, or r92 refusing a forgery”.
Applying K2 literally fires on C2's own evidence: the battery's four carried cases and both whitespace trees all
show `r92 rc=1` (`R93ReviewerC2-c2-controls.txt`: `ws-space: r92 rc=1 (CURATION_R92=FAIL)`, `ws-tab: r92 rc=1
…`, `c1…c4: r92 rc=1 …`). `PRIOR_ACCEPTED=4/4` in `predicate.controls` is the matching false statement: the
prior accepted **0** of the six C2 trees. This is the one place where the frozen artifact implies r92 accepts the
trees, and it is directly contradicted by the frozen prose (“this is classification, not a refusal r92 lacks”).
Receipts `R93ReviewerC2-c2-claims-json.txt`, `R93ReviewerC2-c2-controls.txt`.

### F3 — MEDIUM — named limit (1) is false in both forms
claims.md line 106–107: “`Q_WSQUOT` reads the located-quote population, so a whitespace quote whose source does
not resolve is reported by FLOOR instead.” claims.json line 85 repeats it. E6 (`| Q2 | S999 | " " |`, S999 is no
registry row) → `Q_ROWS=19 Q_SHAPE_FAIL=1 Q_WSQUOT=1`, `Q_SHAPE … quote=<whitespace>`,
`LEG_FAIL WSQUOTE … Q2`, and FLOOR also fails (`12/12 floor13`), rc 1. The count happens at `:325`, before
`q_shape_violation` and before `locates()`/`capture_text`, so source resolution cannot suppress it; and the
population is raw three-cell rows, not “located” rows (E11: non-Q row counted). The leg is *stronger* than the
limit says, but a named limit that states the wrong substitution is a false freeze statement. Receipt
`R93ReviewerC2-c2-probes.txt` E6/E11, rc 1/1.

### F4 — MEDIUM — K4: WSQUOTE is a strict subset of the shape gate; its load-bearing force is arity only
`q_shape_violation` (`:229-231`) and the WSQUOTE count (`:325`) evaluate the same expression on the same `cells`:
`inner = cells[2].strip().strip('"').strip()` / `not cells[2].strip().strip('"').strip()`. Every row WSQUOTE
counts is a row QSHAPE drops, so no tree exists where WSQUOTE fires and `Q_SHAPE_FAIL=0`; measured E2/E3/E4/E6/E8
all show both at once, E7 (zero-width-space quote) shows both silent (`Q_WSQUOT=0`, `Q_SHAPE_FAIL=0`, refused
downstream by FLOOR `12/13`). Consequence: the leg cannot be the sole cause of any FAIL; its only verdict-bearing
effect is the arity check (F/§3): D1 fails the clean tree with **all-green printed fields** and no `LEG_FAIL`;
D2 (leg + arity removed) passes clean and leaves every discriminating tree FAILing for the old reasons. The
machine-form K4's first clause — “counts rows the shape test already dropped” (claims.json line 82) — is therefore
literally satisfied. claims.md's K4 parenthetical (“it must count the row on the forged tree and stay 0 on the
clean one”) is satisfied (E2/E8 = 1, E1/E10 = 0), so the prose reading holds. Also, the claim text and the code
comment (`:481-483`) say “counted … independently of the cell parser”: the count uses the same `table_cells`
parser and the same `cells` tuple; it is independent only of the shape *leg*. Receipt
`R93ReviewerC2-c2-deletions-width.txt` D1/D2, `R93ReviewerC2-c2-probes.txt` E2–E8.

### F5 — LOW — deleting the leg gives a FAIL with no named reason
D1 output, rc 1: `VERDICT fields_hold=1 legs_ok=14/14 DETECTOR_WITNESS=11/11` / `CURATION_R93=FAIL`, and no
`LEG_FAIL` line. `LEGS_MEASURED` prints `14/14`; `passed` (`:539`) is the only place the arity mismatch exists,
and the `LEG_FAIL` loop (`:540-542`) only walks appended legs. An operator sees an all-green field line and a
red token. The counter's purpose is naming causes; the arity tripwire is the one cause it cannot name. Receipt
`R93ReviewerC2-c2-deletions-width.txt` D1.

### F6 — LOW — the new leg is absent from the docstring inventory and from `witness()`
The module docstring lists legs 1–14 (`curation-r93.py:30-54`, ending `14 VERDICT`); WSQUOTE is leg 15
(`:481-485`) and `EXPECTED_LEGS=15` (`:98`). `witness()`'s docstring says “Two-directional assertions over every detector,
including the two new legs”, but its 11 rows (`:253-266`) cover `locates`, `unentailed_terms`, `teaches_miss`,
`dup_qid`, `q_shape_violation` only — no WSQUOTE row, no `used_by_tokens`/USED_BY row, no decision-width row.
`DETECTOR_WITNESS=11/11` in the claim's verdict therefore does not witness the new leg; WSQUOTE's two-directional
evidence is the controls battery (W1/W2 fire, positive silent), not the witness. Receipt
`R93ReviewerC2-c2-counter.txt` (verdict line) and source lines cited.

### F7 — LOW — `Q_WSQUOT` is a quote-emptiness count, not a whitespace count
E3 (empty cell) → `Q_WSQUOT=1`, `Q_SHAPE … quote=<empty>`; E4 (bare `"`) → same; E11 (non-Q row `| note | S214 |
|`) → `Q_WSQUOT=1`, `Q_SHAPE … qid=note`. claims.md's “normalises to the empty string” covers the first two; the
field name and the battery's `ws` labels suggest whitespace-only, and the count accepts any three-cell pipe row in
the section. The printed diagnostic distinguishes `quote=<empty>` from `quote=<whitespace>`, so nothing is
misreported as whitespace. Receipt `R93ReviewerC2-c2-probes.txt` E3/E4/E11, rc 1/1/1.

### F8 — LOW — the four-cell whitespace row falls outside the count
E5 → `Q_WSQUOT=0` while `Q_SHAPE … cells=4` refuses the row (rc 1). The width guard at `:325` means a
malformed-width whitespace row is counted by nobody; it is still refused, so there is no verdict hole, but the
claim's “located-quote population” wording does not disclose that the count is width-filtered. Receipt
`R93ReviewerC2-c2-probes.txt` E5.

### F9 — LOW — C2's cited “Before” receipt is not in F or C
claims.md C2 Before (lines 67–72; the path is on line 71) cites
`corpus/evidence/round93/evidence-before/c2-prior-accepts.txt`.
`git ls-tree -r F/C -- corpus/evidence/round93/` lists no `evidence-before/` (both revs), and
`git log --all -- 'corpus/evidence/round93/evidence-before/*'` is empty on every ref. The file exists only as an
**untracked** lane file (`git status --porcelain` → `?? corpus/evidence/round93/evidence-before/`; `git ls-files`
empty; mtime 11:11, after the C2 commit at 11:05:54 -0300; the later, unreachable C3 commit `d740760e…` at
11:12:06 has no `evidence-before/` either — `git ls-tree … | grep -c evidence-before` = 0). I reproduced its
content independently: r92 on both whitespace trees gives `Q_ROWS=20 Q_SHAPE_FAIL=0` and
`LEG_FAIL FLOOR/WARRANT/TFREQ`, rc 1 — the same field values as the as-found file, which is an excerpt (it omits
the `TEACHES_FLAGGED`, `WARRANT_UNLINKED` and standalone `VERDICT` lines the live run prints). The claim's Before
facts hold; the cited receipt is uncommitted, so at C2 the freeze cites evidence a reviewer cannot read from the
tree. Receipts `R93ReviewerC2-c2-evidence-before-presence.txt`,
`R93ReviewerC2-c2-prior-r92-ws.txt`, `R93ReviewerC2-evidence-before-c2-prior-accepts-asfound.txt`.

### F10 — LOW — `WS_SHAPE_GREEN_R92` is a live dependency on an unpinned artifact
Receipt `R93ReviewerC2-c2-deletions-width.txt` D4 (rc 1):
`CONTROLS=FAIL CARRIED_REFUSED_BOTH=4/4 WS_NAMED=2/2 WS_SHAPE_GREEN_R92=0/1 DUPCOUNT_1=1/1
PRIOR_REGRESSION=7/7` with a shape-fixed r92. Today it holds (`WS_SHAPE_GREEN_R92=1/1`, rc 0). The coupling is
not named in the claim's named limits, and `corpus/evidence/round92/curation-r92.py` has no row in
`instrument-pins.txt`, so a later r92 hardening would flip this battery to FAIL with no C1 pin to explain it. The
failure message on that path still asserts the opposite of the observation
(`FAIL ws-classification: r92 Q_SHAPE_FAIL=0 on both whitespace trees`).

## What holds (checked, not assumed)

- The two canonical commands reproduce the frozen claims.md C2 field list exactly, rc 0 each; identical output
  across two runs (deterministic, no writes, no network — `curation-r93.py` has no write/open-for-write path and
  no network import; inspected by grep for `open(...,"w")`, `subprocess`, `socket`, `urllib`, `requests`).
- `WS_NAMED=2/2` on space and tab with `quote=<whitespace>` plus `LEG_FAIL WSQUOTE … Q2`; `WS_SHAPE_GREEN_R92=1/1`
  today; `PRIOR_REGRESSION=7/7` re-runs the r90 battery through the verdict alias (rc 0).
- `DECISION_WIDTH` print fires once per wrong-width row and is not a gate (D3).
- The counter is byte-identical at the later carrier `d740760e…` (C2→C3 diff touches only `forgeries-r93.py` and
  `instrument-pins.txt`), so the C2 findings are not an artifact of the older carrier.

## Residual risk and verification gaps

- The most consequential defects are in the **machine form**, not the counter: F1 (unsatisfiable predicate) and
  F2 (inverted K2) live only in `claims.json`; prose and instrument agree. If the lane's scorer reads only
  claims.md, C2 scores as claimed; if it reads claims.json, C2 cannot score.
- F4 is a judgement call between two readings of K4. Under the machine-form first clause the leg is vacuous; under
  the prose parenthetical it is not. I report both rather than pick silently; the fix that satisfies both is to
  state WSQUOTE as a *count/naming* leg (or make its population independent of `q_shape_violation`).
- Not in scope and not judged here: C1's own Before receipt
  `corpus/evidence/round93/evidence-before/c1-prior-accepts.txt` is likewise absent from the carrier **and** from
  the lane working tree (C1 reviewer's remit); C3's machine sentence differs from its prose (`TAIL_REFUSED=1/1`
  vs `2/2`) (C3 reviewer's remit); the later carrier `d740760e…` exists and changes the forgery battery (C1
  reviewer's remit). The lane's untracked `corpus/lessons/round-93.md` (11:13) names C3, not C2, as the carried
  tree; I reviewed the tree my assignment names, C2.
- No oracle digest recomputation (TameshiR97's seat) and no cross-seat receipt verification attempted; I verified
  only C2's own two instruments and their two frozen receipts.

VERDICT: R93ReviewerC2 C2 fired — the printed predicate and both batteries hold exactly at C2, but C2's named limit (1) is false (E6 shows `Q_WSQUOT=1` on an unresolvable-source whitespace row, not FLOOR-only), the WSQUOTE leg is a strict subset of the QSHAPE quote-emptiness branch whose only verdict force is the arity tripwire, and the frozen machine form (`claims.json` C2) demands `FORGERY_REFUSED=4/4`/`PRIOR_ACCEPTED=4/4` that no instrument prints and a K2 that r92's own refusals trigger.
