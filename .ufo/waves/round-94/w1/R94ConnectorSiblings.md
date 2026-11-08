# R94ConnectorSiblings — cross-lane pattern scan (chousa round 94)

Seat: `R94ConnectorSiblings` (connector, leaf, read-only). Lane root `/home/vgpnk/Projects/shokunin/chousa-shokunin`,
tip read at carrier `352924bbea624caf3771ef291be98fd4ec679dda`.

Read first: `.ufo/waves/round-94/claims.md` + `claims.json` (every kill rule and named limit), `plans/round-94.md`,
`corpus/lessons/round-94.md`, `corpus/evidence/round94/instrument-pins.txt` (34 rows), `controls/expected.tsv`,
`control-driver-r94.py`. Then the fleet: every `/home/vgpnk/Projects/shokunin/*-shokunin` tree, 1393 files whose
name matches `*pin*.txt|*pins*.txt|*pin*.tsv|*pins*.tsv` outside chousa, plus every lane driver/gate named below
and the recent `SCORECARD.md` blocks. Everything was read with committed bytes; nothing was written in a sibling
repo; nothing was absorbed. Scratch `/fast/scratch/hyaku/chousa-r94/R94ConnectorSiblings` was created and removed.

Receipts (all under `.ufo/waves/round-94/w1/R94ConnectorSiblings/`, each holds the command, its output and
`[exit=N]`):

* `overlap-role-pins.txt` — the role-table greps and the 1393-file population count.
* `closest-c1-role-pin.txt` — kake r60 gate-status classes, kasegi r69 labels, kama r80 role column, kagi pins.
* `closest-c2-punct-quote.txt` — tsukuroi alnum rule, kengaku word floor, kotodama/kagi counting conventions, kama V13.
* `closest-c3-heading-owner.txt` — kake r60 C5 owner check, kake/kotodama section scoping, tsukuroi anchor pointers.
* `scorecard-and-citations.txt` — fleet SCORECARD scan, chousa r94 cross-lane citation check, driver parse lines.

## Answer (1) — does a sibling lane already carry each pattern?

| pattern | carried by a sibling? | decisive evidence (receipt) |
|---|---|---|
| role-bearing pin table (`<sha256>  <role>  <path>`, closed role enum, role sets checked both directions) | **No.** 0 of 1393 sibling pin files has the shape. Two label-first lists exist; neither is machine-read as a role set. | `grep -rl 'instrument\|expectation' --include='*pins*.txt' .` → `NO MATCH` (exit 0 wrapper); shape grep `^[0-9a-f]{64}  [a-z_]+  ` matched only chousa’s own table and one in-lane wave seat file; `grep -rn 'pins-r69' kasegi-shokunin --include='*.py'` → `NO MACHINE CONSUMER` (`overlap-role-pins.txt`, `closest-c1-role-pin.txt`) |
| punctuation-only quote class | **Yes as a rule, no as a class.** tsukuroi’s landed gate refuses a quote cell with no alphanumeric character and names it in the diagnostic, but folds it into a generic `quote_bad` bucket; no sibling counts the class or gives it a leg. | `tsukuroi-shokunin/tools/lint-grounding-r51.py:303-311` (`not re.search(r'[A-Za-z0-9]', want)` → `quote {sid} {base}:{n}: empty, blank or no alphanumeric content`); registered `tsukuroi-shokunin/SKILL.md:4556`; bound by `check-scrub-admission-r51.py:80,378` (`lint_ok == 3`). `grep -rn 'PUNCTQUOT' --include='*.py' .` outside chousa → `NO SIBLING PUNCTQUOT` (`closest-c2-punct-quote.txt`) |
| heading-bound tally check | **No for tallies.** The same *primitive* is landed in a sibling for quotes: an item’s nearest preceding heading must equal the row’s declared anchor heading, and a moved item is refused. | `kake-shokunin/.ufo/waves/round-60/c60_quote_truth.py:516-525` (`if got != anchors[sid]`), `:1012-1016` (`Gate spans share one preceding heading`), selftest `:1198 fail_gate_quote_in_other_section`, `:1303 fail_anchor_heading_inside_code_sample`. `grep -rn 'TAIL_OWNED\|TAIL_OWNER' --include='*.py' .` outside chousa → `NO SIBLING TAIL-OWNER` (`closest-c3-heading-owner.txt`) |

```
OVERLAPS=3
C1 role-bearing pin table — closest kake .ufo/waves/round-60/c60_gate_status.py (docstring :8-38, CLASS_ORDER :99-101) — DIFFERENT mechanism: bidirectional declared-vs-observed population equality over SKILL.md registry rows (member_missing / member_changed / extra_member / unregistered / duplicate_row / row_incomplete / label_invalid), no role column, no pins table.
C2 punctuation-only quote — closest tsukuroi tools/lint-grounding-r51.py:303-311 (docstring :17-18) — SAME rule (`[A-Za-z0-9]` required in the quote cell, named diagnostic), DIFFERENT apparatus: one `quote_bad` bucket, no class counter, no leg.
C3 heading-bound tally — closest kake .ufo/waves/round-60/c60_quote_truth.py:516-525,:1198 — SAME primitive (declared owner heading vs nearest preceding heading, moved item refused), DIFFERENT object and declaration form (HTML article headings for Gate quotes vs ATX headings for SKILL.md tail tallies).
```

## 2. Closest sibling mechanism per pattern, and whether it is the same

### C1 `C1-DRIVER-R94` — the role column is not a sibling mechanism; the both-direction invariant is a sibling mechanism class

* **kake r60 `c60_gate_status.py`** is the closest *invariant*: a frozen member population, one rendered SKILL.md
  table row per member, a closed label enum (`historical` / `never-met` / `live`, else `label_invalid`), and codes
  for **both** directions — `member_missing` (declared, absent), `extra_member` (present, undeclared),
  `unregistered` (not registered), `duplicate_row`, `pin_not_ancestor`, plus `live_not_green` (label vs observed
  exit). Receipt `closest-c1-role-pin.txt`, observed `:99-101`. **Different mechanism**: the population is
  SKILL.md registry rows, not a pins table, and there is no role column or role set. The r94 relation
  (`role=instrument` == the expected rows’ executed set) has no sibling counterpart.
* **kasegi r69 `controls/pins-r69.txt`** is the closest *shape*: `<label> <sha256> <path>` with labels
  `counter / base_gate / forgery_gate / candidate_trial_gate / s103_capture / s103_manifest`, one row with a
  prose cell instead of a digest (`(working copy, not committed before this freeze)`). No script reads it
  (`NO MACHINE CONSUMER`), and r70/r71 pins are plain `sha  path` again — labels without an invariant did not
  survive. **Different mechanism** (annotations, not membership claims).
* **kama r80 `registry/engine-pin-relations.tsv`** has a literal `role` column (`engine ref kind role relation
  newer newest receipt dated`); the role is a provenance source (`engine-pins.tsv`, `source-row S553`,
  `cross-lane kengaku S178`) and the only check is `empty-role` (`round80-engine-pin-relations.py:155-156`).
  **Different mechanism** (non-empty provenance label, no closed enum, no set relation).
* **kagi `corpus/anchor-pins.sh`** is the pin-gate tradition: id-keyed `anchor-pins.tsv` (`id`, `anchor_sha256`),
  `DRIFT <id> dup|shape|schema`, `--selftest`, and a named ceiling. One-directional (pin → registry cell), no
  roles. **Different mechanism.**
* In-lane context, not an overlap: chousa’s own `SKILL.md:85` Gates table already has a `kind` column
  (`gate` / `tool` / `probe`). The label is not new; the machine set relation over the pins table is.

### C2 `C2-CURATION-R94` — the rule is prior art; the class apparatus is not

* **tsukuroi `tools/lint-grounding-r51.py`** (landed, registered `grounding-lint-r51`, exit 0/1/2) requires a
  Quote row’s text to be “non-empty with an alphanumeric character” (docstring `:17-18`) and refuses
  `not re.search(r'[A-Za-z0-9]', want)` as `quote <sid> <file>:<line>: empty, blank or no alphanumeric content`
  (`:303-311`). `check-scrub-admission-r51.py:80,378` makes `lint_ok == 3` part of its predicate. This is the
  **same rule** as `q_shape_violation` on a different table. It is **not the same apparatus**: the case is
  counted inside `quote_bad`, there is no `Q_PUNCTQUOT`-style population count, no `quote=<punctuation>` token and
  no leg.
* **kengaku `pkg_gate.py`** refuses a quote outside `quote_words = [3, 25]` (`:155-161`, rules `:308-310`), so a
  one-token punctuation quote cannot pass that gate — the *outcome* is already refused in a sibling by length,
  not by character class.
* **kotodama `tools/check-gate-quotes.py:34-38`** and **kagi `corpus/lessons/round-49.md:51` (E49-1)** both count
  punctuation-only tokens as words, so a punctuation-only quote is one word and passes a 25-word cap. The fleet’s
  shared counting convention leaves exactly the hole C2 names.
* **kama `KamaR27CtlContentFree/REPORT.md:57`** (V13) records a punctuation-variant prose cell **accepted** by its
  counter; kama’s own boundary (“does not judge … prose”) is explicit — an adjacent class with a different
  decision, not the same rule.
* **Non-routes** (do not cite as prior art): `kengaku-shokunin/plans/battery37/p4.py:84`
  (`the first quote has no alphanumeric character`) is a fixture-builder precondition, not a quote rule;
  `kasegi-shokunin/.ufo/waves/round-100/w1/SentinelCookie.md:179` is cookie-separator prose.

**Explicit contradiction, not smoothed:** if C2’s novelty were read as “this lane now refuses the class”, it is a
duplicate — tsukuroi r51 already refuses it, by name, and binds it into an admission counter. The frozen sentence
is narrower and stays true: r93 fails the tree downstream with `Q_SHAPE_FAIL=0` and cannot *name* the class; no
sibling counts the class, gives it a shape code, or makes a leg arity tripwire fire on its deletion.

### C3 `C3-TALLY-R94` — same primitive, different object

* **kake r60 `c60_quote_truth.py` C5_quote_truth** declares a row anchor heading and requires each page-unique
  Gate quote’s nearest preceding article heading to equal it; a quote whose nearest heading is another one is
  refused (`:516-525`), two quotes under one heading are refused (`:1015`), and the selftest names the moved case
  `fail_gate_quote_in_other_section` (`:1198`) plus `fail_anchor_heading_inside_code_sample` (`:1303`).
  **Same primitive and same refusal semantics**, different object (HTML article headings and Gate quotes vs ATX
  headings and SKILL.md tail tallies) and different declaration form (anchor derived from the article’s own
  heading vs an owner substring declared in the counter).
* Section **scoping** precedents — the weaker form chousa’s r92 used and r93/r94 repaired: kake
  `scripts/doc_quote_truth.py:318-320` (`sections()`: a claim row outside its `^Round[- ]?<N>` level-two body is
  simply not population) and kotodama `tools/check-gate-quotes.py:15` (`## Gate` up to the next `## `). These
  **drop** a moved item instead of refusing it; kake C5 and chousa r94 **refuse** it.
* **tsukuroi `SCORECARD.md:593`** anchors ownership pointers by exact heading (with quote and digest) — a heading
  anchor, not an owner match on counts.
* In-lane context: chousa `SCORECARD.md:4119` (r92) already scoped tallies to an ATX boundary; the r94 addition is
  the per-occurrence owner match. No sibling binds a **tally** to a heading
  (`TAIL_OWNED|TAIL_OWNER` outside chousa → none).

## 3. Cross-domain evidence to route (report, not absorb)

1. **tsukuroi `tools/lint-grounding-r51.py` (r51, landed gate `grounding-lint-r51`)** — prior art for C2’s rule;
   route as a citation in the next calibration plan or the lesson’s Gate, not as a chousa instrument (tsukuroi
   province: knowledge-entry grounding; the rule there is welded to whole-line equality against pinned snapshots).
2. **kake `.ufo/waves/round-60/c60_quote_truth.py` C5_quote_truth** — prior art for C3’s owner primitive; route
   likewise (kake province: quote truth against retained article bodies).
3. **kake `.ufo/waves/round-60/c60_gate_status.py`** — prior art for the both-direction population invariant
   behind C1, and an enumerated parse-hazard list for deriving an executed-set from an entry command (A2/A3,
   `:27-38`: env words, `[...]` segments, revision placeholders, metacharacters → `command_unparsable`). Route to
   C1’s next tightening.
4. **kasegi r69 → r70/r71 label drop** — evidence that a label column without a membership invariant does not
   survive the next round (receipt `closest-c1-role-pin.txt`, `pins-r69.txt:2-7` vs `pins-r70.txt:1-10`). Route as
   design evidence for C1, not as an instrument.
5. **kengaku 3–25 word quote floor + kotodama/kagi punctuation-token counting + kama V13** — three lanes meet the
   same content-free class with three different boundaries; route to C2’s named limits so a future rule does not
   silently claim a wider class than `[A-Za-z0-9]` absence.

## 4. Verification exercised (exact commands, receipts, observed lines, exit codes)

All receipts are in `.ufo/waves/round-94/w1/R94ConnectorSiblings/`; every entry below is a line that receipt holds.

| # | command | receipt | observed line | exit |
|---|---|---|---|---|
| 1 | `grep -rl 'instrument\|expectation' --include='*pins*.txt' .` | `overlap-role-pins.txt` | `NO MATCH` | 0 (wrapper) |
| 2 | `find . -type f \( -name '*pin*.txt' -o -name '*pins*.txt' -o -name '*pin*.tsv' -o -name '*pins*.tsv' \) -not -path './chousa-shokunin/*' \| wc -l` | `overlap-role-pins.txt` | `1393` | 0 |
| 3 | `find … -print0 \| xargs -0 grep -lE '^[0-9a-f]{64}  [a-z_]+  '` (whole fleet) | `overlap-role-pins.txt` | only `chousa-shokunin/corpus/evidence/round94/instrument-pins.txt` and one in-lane seat file; **0 sibling-lane files** | 0 |
| 4 | `find … -print0 \| xargs -0 grep -lE '^[a-z_]+ +[0-9a-f]{64}  '` | `overlap-role-pins.txt` | `kasegi-shokunin/.ufo/waves/round-69/controls/pins-r69.txt`, `audio-shokunin/corpus/live/r84-scribe/commit-pin.txt` (one `worktree` row, :36) | 0 |
| 5 | `grep -nE 'extra_member\|unregistered\|member_missing\|member_changed\|label_invalid\|duplicate_row\|row_incomplete' kake-shokunin/.ufo/waves/round-60/c60_gate_status.py` | `closest-c1-role-pin.txt` | `:99-101` `CLASS_ORDER = ["member_missing", "member_changed", "extra_member", "unregistered", "duplicate_row", "row_incomplete", "label_invalid", …]` | 0 |
| 6 | `sed -n '1,8p' kasegi-shokunin/.ufo/waves/round-69/controls/pins-r69.txt` | `closest-c1-role-pin.txt` | `candidate_trial_gate … (working copy, not committed before this freeze)` | 0 |
| 7 | `grep -rn 'pins-r69' kasegi-shokunin --include='*.py'` | `closest-c1-role-pin.txt` | `NO MACHINE CONSUMER` | 0 (wrapper) |
| 8 | `sed -n '25,32p;150,158p' kama…/round80-engine-pin-relations.py` | `closest-c1-role-pin.txt` | `:155-156` `if not role: findings.append(f"PIN_RELATIONS_FINDING empty-role …")` | 0 |
| 9 | `cut -f4 kama-shokunin/registry/engine-pin-relations.tsv \| sort \| uniq -c` | `closest-c1-role-pin.txt` | `1 cross-lane kengaku S178 / 3 engine-pins.tsv / 1 role / 1 source-row S553` | 0 |
| 10 | `sed -n '150,175p;305,312p' kengaku…/R36GateD/pkg_gate.py` | `closest-c2-punct-quote.txt` | `:155-161` `if not lo <= words <= hi: return False, f"quote has {words} words (want {lo}..{hi})"`; `:308-310` `"quote_words": [3, 25]` | 0 |
| 11 | `sed -n '303,311p' tsukuroi-shokunin/tools/lint-grounding-r51.py` (via grep receipt) | `closest-c2-punct-quote.txt` | `:311` `quote {sid} {base}:{n}: empty, blank or no alphanumeric content` | 0 |
| 12 | `grep -rn 'PUNCTQUOT' --include='*.py' .` (chousa excluded) | `closest-c2-punct-quote.txt` | `NO SIBLING PUNCTQUOT` | 0 (wrapper) |
| 13 | `grep -n 'V13-next-action-punctuation-only' kama…/KamaR27CtlContentFree/REPORT.md` | `closest-c2-punct-quote.txt` | `:57` V13 row, registered 2 / counted 2 | 0 |
| 14 | `sed -n '514,527p;1012,1016p' kake…/c60_quote_truth.py` + `grep -n 'fail_gate_quote_in_other_section…'` | `closest-c3-heading-owner.txt` | `:525` `has nearest preceding heading {got!r}, not row anchor {anchors[sid]!r}`; `:1198` `fail_gate_quote_in_other_section` | 0 |
| 15 | `sed -n '318,321p' kake-shokunin/scripts/doc_quote_truth.py` | `closest-c3-heading-owner.txt` | `:318-320` `def sections(...) "Bodies of level-two headings …"` | 0 |
| 16 | `grep -rc 'TAIL_OWNED\|TAIL_OWNER' chousa…/skill-tally-r94.py` + fleet-wide grep | `closest-c3-heading-owner.txt` | `8` in-lane; `NO SIBLING TAIL-OWNER` fleet-wide | 0 |
| 17 | `grep -rn 'role column\|role-bearing\|role=instrument' --include='SCORECARD.md' .` | `scorecard-and-citations.txt` | only `chousa-shokunin/SCORECARD.md:4177,4199` | 0 |
| 18 | `grep -rn 'punctuation-only quote\|punctuation quote\|Q_PUNCT' --include='SCORECARD.md' .` | `scorecard-and-citations.txt` | only `chousa-shokunin/SCORECARD.md:4187,4200,4206` | 0 |
| 19 | `grep -rn 'heading.*tally\|tally.*heading\|owner.*heading' --include='SCORECARD.md' .` | `scorecard-and-citations.txt` | only chousa r92/r94 bullets (`:4119,4183`); tsukuroi `:593` is pointer anchoring | 0 |
| 20 | `grep -rn '<sibling lanes>' chousa-shokunin/{corpus/lessons/round-94.md,plans/round-94.md,.ufo/waves/round-94/claims.md,claims.json}` | `scorecard-and-citations.txt` | `NO CROSS-LANE CITATION IN R94` | 0 (wrapper; grep itself 1) |
| 21 | `sed -n '137,152p' chousa…/control-driver-r94.py` | `scorecard-and-citations.txt` | `instrument_rels`: `if (t.endswith(".py") or t.endswith(".sh")) and os.path.isabs(t)` after only `@ROOT@` substitution | 0 |
| 22 | `cut -d' ' -f3 chousa…/instrument-pins.txt \| sort \| uniq -c` | `scorecard-and-citations.txt` | `2 claims / 20 driver / 1 expectation / 5 instrument / 6 receipt` (34 rows) | 0 |

## 5. Risks and second-order effects (evidence, not judgment)

* **C1’s executed set is the parser’s set.** `instrument_rels()` (`control-driver-r94.py:141-150`) maps only
  absolute `.py`/`.sh` tokens after `@ROOT@` substitution. In `expected.tsv` the `c1-harm` row also executes
  `git show 265b8633…:tools/gate-records.py` (a git-object path, not absolute) and writes/reads
  `@WORK@/harm/base-tool.py` (scratch, `@WORK@` never substituted); both are skipped, and
  `tools/gate-records.py` has no pin row (`grep -c` → 0). The five *tree* instruments the rows execute are exactly
  the five `instrument` rows, so the relation holds as stated; but a future expected row that executes a relative
  path, a `bash -c` string, or an interpreter fed by an env var would sit silently outside the role relation.
  kake’s A2/A3 (`c60_gate_status.py:27-38`) is the enumerated edge list and *refuses* unparsable commands
  (`command_unparsable`); chousa’s parser ignores what it cannot classify.
* **C2 is a duplicate rule across lanes.** tsukuroi r51 and chousa r94 now both require an alphanumeric character
  in a quote cell. They are lane-local so nothing is double-counted today; if either tightens, the other is
  unbound. Report only.
* **C3’s primitive is implemented twice** (kake C5 and chousa r94) with different declaration sources; a future
  fleet-level owner check would have two precedents to reconcile. Report only.
* **Adjacency axis.** The round declares adjacency “unchanged: the connector seat’s sibling scan is read-only;
  nothing absorbed”. This scan does not change that — it produces six routable citations (§3) with paths and line
  numbers. Recording them is the L1’s call; absorbing them would need a separate round and its own freeze.

## 6. Limits of this scan

* “No sibling carries it” is bounded by the searched vocabulary and shapes: literal tokens
  (`instrument|expectation`, `PUNCTQUOT`, `TAIL_OWNED|TAIL_OWNER`), the two pin-row shapes over 1393 files, and
  the SCORECARD greps. C2’s rule surfaced only by reading quote-checker bodies (`tsukuroi`’s alnum test) — a
  differently-worded equivalent for C1 could exist and would not have been found by shape alone.
* The scan is fleet-wide but shallow: each candidate was read to the point that decides same/different; no sibling
  instrument was run, and no sibling claim was re-measured (not this lane’s province).
* No chousa predicate was executed by this seat (connector, not exec/attack); the C1/C2/C3 numbers quoted above
  are the L1’s committed ones, read from the scorecard and pins table, not re-derived here.

VERDICT: R94ConnectorSiblings C1 n/a — read-only overlap scan; no sibling carries the role-set relation, so this seat produces no kill ground and no verdict on the claim.
VERDICT: R94ConnectorSiblings C2 n/a — the alnum rule is prior art in tsukuroi r51 but the counted class apparatus is absent fleet-wide; the claim's own wording, not this seat, will decide whether that is a citation or a defect.
VERDICT: R94ConnectorSiblings C3 n/a — the owner primitive is prior art in kake r60 C5; the tally population is not, so this seat reports and does not judge.
