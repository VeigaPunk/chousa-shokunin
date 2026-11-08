author: hyaku closure (non-author integrator, @m_zfl)

# Round 94 verifier spot-check — chousa (non-author, hyaku closure)

Date 2026-11-08. Judge: hyaku closure (non-author integrator), lane `chousa`. Base
`0f3f84dab3a094ec0a2fe8ae9ae59d3326e1a9b6`; lane HEAD after the round
`0e311d16e2880eeba72004826d8638bbae7dde4a`; freezes F `41038ed7`, F2 `4cbaed6c`, F3 `ebbcbe39`; carriers C
`352924bb`, C2 `f276d7fb`, C3 `d13c2ff2`. Report `.ufo/reports/round-94/chousa.md`.

## Conformance (step 1)

- Report identity: `git log --format='%an <%ae> %H' -- .ufo/reports/round-94/chousa.md` →
  `chousa-shokunin <chousa@shokunin.local> 1f883f43249bfd15ed7e4322241de6bbeb887ad1`. Lane identity OK.
- SHONEN: `grep -c '^## SHONEN'` → 1; `grep -c '^- \['` → 4, one `[~]` line per `SHONEN.md` box
  (`grep -c '^- \[' SHONEN.md` → 4); no `[x]`; `git diff --quiet 0f3f84da 0e311d16 -- SHONEN.md` exit 0.
- Cited lane commits: `41038ed7`, `352924bb`, `6ae736ea`, `4cbaed6c`, `f276d7fb`, `ebbcbe39`, `d13c2ff2`,
  `0e311d16`, and the base `0f3f84da` — each `git -C chousa-shokunin merge-base --is-ancestor <hash>
  refs/heads/master` exit 0 (HEAD is detached under jj, so ancestry is tested against the branch ref).
  `git log --oneline 0f3f84da..0e311d16` lists exactly the eight round commits in report order.
- Clean/pushed: `jj-lane.sh state chousa-shokunin` → `branch=master local=0e311d16 remote=0e311d16 ahead=0
  behind=0 head=detached tracked=0 untracked=0`; `git -C chousa-shokunin status --porcelain` empty.
- Report lands last: report commit `%ct` 1794154675 > lane HEAD `%ct` 1794154661.
- Prompt fidelity: `.ufo/prompts/chousa-round-94.md` (998 lines, committed by `ee12fc8e`) diffs against
  `templates/round-prompt.md` rendered for `chousa`/`94` in two intended places only — the working-dir line
  (`<chousa-repo>` → `chousa-shokunin`) and the lane-axes line — with `## 6` addendum appended. All
  round-level items (mission/axes binding, L2 floor ≥8 in one batched call, commit-then-push, push scope, L0
  side channel) and all five child-lane items (report path, report-lands-last, `## SHONEN` grep, cited-hash
  rule, write scope) are present verbatim.
- Route map: `MISSION.md` carries role-class buckets (heavy-reasoning / fast-execution / economy), never
  model aliases; the prompt's §6 run-15 alias map is a campaign snapshot and `MISSION.md` says routing
  resolves through the operator's host table. No route-map/MISSION conflict.
- Marker check: three real claims, eight cited commits, per-claim receipts, LOG tie → status **ok**, not a
  marker.
- Watchdog digest (copied): `2026-11-08T12:10:27-03:00 launch chousa round=94 pgid=368999
  driver=hyaku-inline attempt=1` (line 3374); `2026-11-08T13:20:10-03:00 complete chousa round=94;
  hyaku-inline attempt=1` (line 3382). No dead/wave-error line for round 94.
- Fleet-root hygiene: `git ls-files corpus` at the fleet root → 0, and no `corpus/` directory exists there,
  so the report's misroot sweep (six stray receipts written one level high, then deleted) is real. The
  fleet-root dirty entries (`.scratch/*`, `.ufo/l0-questions.md` appends from tsukuroi/souji) are not
  chousa round work.
- Wave: `w1-dispatch.json` one wave; `w1-results.json` 12 results, 12 distinct seats, 12 seat reports under
  `.ufo/waves/round-94/w1/`; attack seats by the closure enumeration = 3 reviewers + critic +
  mutation-tester + sentinel + revenger + connector = 8/12 (the report counts 7/12, excluding the
  connector under the few-connector rule — both internally consistent); one connector.

Status-neutral defects found here are D1–D8 below.

## Step 2b — pre-file falsification ledger

```
$ python3 /home/vgpnk/Projects/shokunin/scripts/hyaku/prefile-falsification.py --lane chousa --round 94
PREFILE-FALSIFICATION: pass claims=3 rows=19 attack_seats=8 findings=0
$ echo $?
0
```

Hand adjudication of the same surface. The ledger covers all three claims (C1 8 rows, C2 5, C3 6), and its
artifact column reads all eight attack seats (ReviewerC1/C2/C3, CriticClaims, ExecMutations, SentinelScope,
RevPrior, ConnectorSiblings) plus the three executors and the scout. All nine non-neutral rows name a
narrowing in `plans/round-94.md`, and every named narrowing exists (Amendments 1, 2(a)/(b)/(c), 3(a)/(b),
5, 6, 7, 8). Defects found by hand, none of which leaves a wording unreconciled:

- **D4** — the C2 row credits `R94CriticClaims` with a two-line-predicate finding that seat does not file: its
  C2 predicate row reads "reproduced verbatim | bound", and its seven fires contain no such item. The nearest
  measured finding is `R94ReviewerC2` F3 (predicate-text fidelity, `grep -cF` 0 on the contiguous string), and
  Amendment 2 is headed `(R94ReviewerC2 F1/F2/F3/F4)`. The narrowing is real; the attribution is wrong.
- **D5** — the C1 `R94SentinelScope` row claims "no containment guard for `--work`, `--pins`/`--expected`/
  `--receipts`, symlinked pin rows or `--receipts-rev`". The seat measured `--work` (F2), symlinked rows (F5),
  `--pins` (F6) and `--receipts-rev` (F7); it files nothing on `--expected`/`--receipts`. The guard is real
  (`control-driver-r94.py:486-494` contains all four), so the row's scope is wider than the seat's evidence.
- **D6** — the `R94ExecC3Repro` row says "both named limits measured"; the seat measured limits 1 and 4 and
  states that limits 2 and 3 were not independently measured.

None of the three is an unreconciled `falsifies-wording`: in each case the forced narrowing landed and the
shortfall is in the ledger's attribution, not in the claim.

## Per-claim re-check (step 2)

Method: plain measurements over committed bytes (`git show`, `sha256sum`, `awk`, `grep`, `wc`) plus
structural reading of the instruments. No sibling gate or battery was executed (§Gate standard, closure
consequence). Each claim was re-derived on its own population; the counter verdict lines are
**evidence-verified** from the committed `after/*.txt` receipts (all six carry `# computed_against
F=ebbcbe39 C=d13c2ff2`, stable from C3 to the landing apart from that header).

### C1 `C1-DRIVER-R94` — operability (lowest scored axis, 3/10)

**Re-measured**

- Pins population: `git show d13c2ff2:corpus/evidence/round94/instrument-pins.txt` → 35 rows;
  `awk '{print $2}' | sort | uniq -c` → `driver 21, receipt 6, instrument 5, claims 2, expectation 1`;
  non-driver rows = 14 = the receipt's `PIN_ROLES_OK=14/14`.
- Byte truth of every row, walked by hash: for each row `git show F:<path> | sha256sum` and `git show
  C:<path> | sha256sum` → **28 rows match at F, the 6 receipt rows match at C, 0 mismatches**; the self row
  equals `git show <rev>:instrument-pins.txt | head -n -1 | sha256sum` (minus-self digest) at both F and C.
- Role sets in both directions: `role_report` (lines 284-331) computes `instrument == executed`,
  `expectation == {expected.tsv}`, `receipt == the receipts directory`, `claims == CLAIM_PATHS`, each with
  `PIN_ROLE_MISSING`/`PIN_ROLE_DANGLING` in the difference directions; the executed set is the five
  instruments `expected.tsv` names (`gate-records-r89.py`, `mutate-r89.py`, `harm-recheck-r90.py`,
  `curation-r89.py`, `curation-r89-controls.py`) — exactly the five `instrument` rows.
- PASS is not a token: `roles_ok = not role_codes and role_ok == role_total and role_total > 0`, and
  `passed` requires `findings == 0`, all four `n/n` ratios full, `checked == len(pins)`,
  `rchecked == rtotal > 0` (lines 617-620).
- Prior state is genuine: `grep -c 'role' corpus/evidence/round93/control-driver-r93.py` → 0.

**Evidence-verified** — `after/c1-verify.txt` (rc 0): `COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6
FRESH_OK=6/6 PINNED_FILES=35/35 RECEIPT_PINS=6/6 PIN_ROLES_OK=14/14 CONTROL_DRIVER_R94=PASS`, `RECEIPT
SELF_PIN OK rev=ebbcbe39 receipts_rev=d13c2ff2`; `after/c1-forgeries.txt` (rc 0): four role classes refused
by r94 (`PIN_ROLE_DANGLING role=instrument`, `PIN_ROLE_MISSING role=claims`, `PIN_ROLE_MISMATCH
role=expectation`, `SETUP PIN_ROLE_UNKNOWN`), each accepted by r93, plus `SCHEMA_REFUSED=1/1`,
`CARRIED_REFUSED=2/2`, `POSITIVE=pass`; before receipt `evidence-before/c1-prior-accepts.txt` (r93: 23/23
and 21/21 with the claims rows deleted, 0 role columns).

Verdict: **verified as stated**.

### C2 `C2-CURATION-R94` — calibration

**Re-measured**

- `Q_ROWS`: `awk` over the `## Located quotes` blocks of `search-transparency-reporting-r84.md` and
  `provenance-recording-r85.md` → 13 + 7 = **20**, equal to the receipt's `Q_ROWS=20`.
- Leg table: `wc -l corpus/evidence/round94/controls/legs.txt` → 16 names, including the new `PUNCTQUOT`;
  `EXPECTED_LEGS = 16` in the counter with `LEG_FAIL ARITY expected=16 measured=<n>` as the tripwire.
- Witness rows: 18 in `witness()` (counted; includes `punct-fire`, `punct-silent`, `punct-shape`,
  `punct-locate-silent`, `punct-cjk-silent`) = `DETECTOR_WITNESS=18/18`.
- The class is real and Unicode-correct: `punct_quote_cell` returns true only for a non-empty three-cell
  quote with no `ch.isalnum()`; `q_shape_violation` returns `quote=<punctuation>` for it; `locates()`
  refuses it by rule. Prior counter has no such token (`grep -c PUNCT corpus/evidence/round93/curation-r93.py`
  → 0).

**Evidence-verified** — `after/c2-counter.txt` (rc 0): `CURATION_R94=PASS` with `LEGS_MEASURED=16/16
Q_ROWS=20 Q_SHAPE_FAIL=0 Q_WSQUOT=0 Q_PUNCTQUOT=0 WARRANT_OK=17/17 TFREQ_OK=17/17 DUP_QIDS=0` and `VERDICT
fields_hold=1 legs_ok=16/16 DETECTOR_WITNESS=18/18`; `after/c2-controls.txt` (rc 0): `CONTROLS=PASS
CARRIED_REFUSED_BOTH=4/4 WS_NAMED=2/2 PUNCT_NAMED=2/2 PUNCT_SHAPE_GREEN_R93=1/1 CJK_SILENT=1/1
DUPCOUNT_1=1/1 PRIOR_REGRESSION=7/7`, with `x1-punct-dash`/`x2-punct-dots` refused by r94 at the shape leg
and `shapes old=0` (r93 green) on both, and `x3-cjk-quote` never labelled as the class. Before receipt
`evidence-before/c2-prior-accepts.txt` (r93 on the em-dash tree: `Q_SHAPE_FAIL=0`, refusal only at
`LEG_FAIL FLOOR`/`WARRANT`/`VERDICT`).

Verdict: **verified as stated** (a classification claim, narrowed by Amendment 2).

### C3 `C3-TALLY-R94` — freshness

**Re-measured**

- `TALLY_ROWS=8`: the `## Gates` table rows (SKILL.md 86-93) that carry a tally (`^| \`research-gate` or
  `Selftest \`PASS (`) — 8 rows, every one at `283 cases, 0 skipped` (`STALE_TALLIES=0/8`). Total
  occurrences of `PASS (<n> cases` in SKILL.md = 21 (`grep -cE`).
- Tail owners are observed, not declared: line 640 sits under `### Round27 repair/status correction —
  2026-10-21` and line 781 under `### Round 37 — the claim-pin provenance … (2026-10-23)` — the two
  `TAIL_OWNED` declarations; `TAIL_OWNER_COUNT`/`TAIL_OWNER_MISMATCH`/`TAIL_OWNER_UNMAPPED` all feed
  `tail_ok`, and the head scan keeps `HEAD_DECLARED = {}` honest.
- Historical grounding: `PASS (161 cases, 0 skipped)` appears once in `corpus/evidence/round25-final-measure.log`
  and once in SKILL.md's Gates scope; `PASS (256 cases, 0 skipped)` once in
  `corpus/evidence/round34/audit-dispositions.md` and once in scope → `HIST_DERIVED=2/2 HIST_PRESENT=2/2`.
- Prior state is genuine: `grep -c TAIL_OWNER corpus/evidence/round93/skill-tally-r93.py` → 0.

**Evidence-verified** — `after/c3-counter.txt` (rc 0): `SKILL_TALLY_R94=PASS` with `LEGS=4/4 TAIL_OK=1
TAIL_OWNED_OK=2/2 TAIL_TALLIES=2 TALLY_ROWS=8 STALE_TALLIES=0/8 HIST_DERIVED=2/2 HIST_PRESENT=2/2
CASE_RANGE_OK=2/2 MISLABELED=0`; `after/c3-controls.txt` (rc 0): `CONTROLS=PASS CARRIED_REFUSED=6/6
MOVED_REFUSED=2/2 MOVED_PRIOR_ACCEPTED=2/2 DOUBLE_REFUSED=1/1 HEADING_ALIAS_ACCEPTED=1/1
STALE_REFUSED_BOTH=1/1 TAIL_ADDED_REFUSED=1/1 HIST_UNGROUNDED_REFUSED=1/1`, with both moved-tail trees
`r93 rc=0 / r94 rc=1 TAIL_OWNER_MISMATCH`. Before receipt `evidence-before/c3-prior-accepts.txt` (r93:
`TAIL_OK=1 … SKILL_TALLY_R93=PASS`).

Verdict: **verified as stated**.

### No axis harmed

- `git diff --quiet 0f3f84da 0e311d16 -- tools/ SKILL.md PROVINCE.md` → exit 0; `-- corpus/knowledge/` →
  exit 0.
- Full diff: 328 files, 15 997 insertions, **0 deletions**, 0 renames. `corpus/SOURCES.md` is one appended
  row (hunk `@@ -230,6 +230,7 @@`); `SCORECARD.md` is a single EOF hunk (`43 0`) that appends the round-94
  block and carries the round-93 `22/22` correction as an appended line naming the superseded sentence —
  the round-93 block is byte-intact and its own row already reads `PINNED_FILES=23/23`; `corpus/QUALITY.md`
  adds rows 217-219 only (`21 0`, single hunk after base row 216); `LOG.md` is append-only (`28 0`, no
  removed line).
- Registry 219 → 220 rows (`grep -cE '^\|…S[0-9]{3,}…\|'` at base and landing), the new row `S221` only.

## Per-axis verdicts

- operability: **improved** (C1 verified; 35-row role-typed population, digests byte-true at F/C, role sets
  both directions, four forgery classes refused where r93 accepts)
- calibration: **improved** (C2 verified; punctuation class named, counted, refused at the shape leg, and
  Unicode-correct)
- freshness: **improved** (C3 verified; tail tallies bound to their owning headings, both moved trees
  refused)
- depth: **unchanged** (no `corpus/knowledge/` entry; S221 is a tool-documentation row)
- coverage: **unchanged** (registry +1 row; `PROVINCE.md` untouched)
- adjacency: **unchanged** (connector scan read-only; OVERLAPS=3 kake/tsukuroi, nothing absorbed)

## Discernment spot-check (step 3)

The round's `## Gate` records one admit (`S221`) and two re-opens (`S001`, `S070`), and states that no new
candidate was refused. Reject-class items are therefore sampled from the round's own gate decisions: the
S221 `GATE-RECORD` form refused by the lane's unchanged validator, the ASCII-only class refused by the wave
before the landing, and the unsatisfiable C1 battery case dropped at F2.

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S221 — installed `git-clone(1)`, `--shared` | admit | `/usr/share/man/man1/git-clone.1.gz`: `sha256sum` → `b3fd695c…802a` (identical to the row's anchor); `zcat … \| grep -n 'The resulting repository'` → line 100 `The resulting repository starts out without any object of its own\&.` | agree | the located quote is verbatim at the cited location, 11 whitespace tokens in the Gate record (≤25); the digest and path in the anchor match the installed page; the row's scope ("what a `--shared` clone stores") is exactly what the sentence grounds. |
| S070 re-open — `sha256sum(1)` | admit (unchanged cells) | `/usr/share/man/man1/sha256sum.1.gz`: `sha256sum` → `93c17dff…403f` (identical to the row); line 11 → `Print or check SHA256 (256\-bit) checksums.` | agree | digest and the line-11 quote reproduce exactly; no `status`/`recheck`/`used-by` change was made, as the Gate record states. |
| S221's first `GATE-RECORD` (`path=`/`sha256=`/`words=` with no `rev`/`url`) | reject (refused by the lane's own validator) | `tools/gate-records.py:19-23` documents exactly three record forms (url/admit, url/unreach, rev) and `PARSE` fires on anything else; the lesson's remaining record is the S001 `rev` form at line 15, whose `rev`/`path`/`line`/`quote` I re-resolved: `git show 4cbaed6c:tools/research-gate.sh \| sed -n 9010p` → `printf 'RESEARCH_GATE_SELFTEST: PASS (%d cases%s)\n' …`, quote tokens = 4 | agree | the rejected form is not implementable by the validator, so the seat's refusal was correct; the replacement record parses under the rev form and its line/quote resolve. |
| C2's ASCII-only punctuation class (`[A-Za-z0-9]`) | reject (falsified before landing) | `curation-r94.py:229-236` now uses `not any(ch.isalnum() for ch in inner)`, `witness()` carries `punct-cjk-silent`, and `after/c2-controls.txt` measures `x3-cjk-quote` → `r94 rc=1`, `punct new=0`, no `quote=<punctuation>` | agree | the first draft refused a CJK quote as punctuation, a wrong label on a legitimate short quote; the landed test is Unicode-aware and the control forbids the class label for CJK. |
| C1 battery case `s1-schema-two-column` | reject (dropped at F2) | `grep -n 's1-schema\|s0-schema' forgeries-r94.py` → only `s0-schema-prior` remains (line 188); `after/c1-forgeries.txt` shows `s0-schema-prior: r93 rc=0 (two-column table scores) r94 rc=2 (PIN_SCHEMA)` | agree | a case that writes the valid three-column table and then demands `SETUP PIN_SCHEMA` from it can never pass on any tree the driver accepts; the do-nothing measurement survives as `s0`. |

New-row quote check: the only new row is `S221`; its Gate quote is 11 tokens (≤25) at line 100 of the cited
page, and the row's `teaches` cell embeds the located fragment plus its gloss (27 tokens — normal for this
registry: 106 of 220 rows carry a `teaches` cell longer than 25 tokens, so the limit binds the Gate quote,
not the cell).

Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin
chousa` → exit 0, `chousa ok`, 220 rows, the same five pre-existing `W04` duplicate-url warnings
(S051/S053/S073/S074/S075) present at base.

## Trend verdicts with evidence

- **expansion: unchanged** — `git diff 0f3f84da 0e311d16 --stat -- corpus/knowledge/` empty; registry 219 →
  220 with one tool-documentation row; no frontier ground entered; no capability row entered
  `SCORECARD.md`.
- **quality: improved** — three r93 instruments superseded by successors whose new properties are measured
  against the prior counter on the same bytes (`PRIOR_ACCEPTED=4/4`, `PUNCT_SHAPE_GREEN_R93=1/1`,
  `MOVED_PRIOR_ACCEPTED=2/2`), each with a red-before receipt committed before any scored run, and no
  admitted corpus entry found false or stale.
- **discernment: improved** — the wave fired the frozen sentences before filing and every firing was
  answered by a widening of the instrument or a narrowing of the sentence (Amendments 1-9); this outside
  re-check agrees with the gate on the admit (S221) and on each sampled rejection. The ledger's
  attribution defects (D4-D6) are routing items, not disagreements left unlearned.

## Routed defects for next round

1. **D1 — ledger class miscount in the report.** `.ufo/reports/round-94/chousa.md` §Pre-file falsification
   and §Trend verdicts say "9 `falsifies-wording`, 1 `falsifies-number`, 9 `neutral`"; the ledger
   (`awk -F'\t' '{c[$3]++}' claim-falsification.tsv`) is **8 / 1 / 10**. What is 9 is the number of rows
   naming a `plans/round-94.md` pointer. Fix the sentence in the next report (a filed report is a record).
2. **D2 — `LOG.md` round-94 "After" bullet is stale (append-only correction owed).** `LOG.md:2712-2714`
   names only F/C and `LOG.md:2724-2728` quotes `PINNED_FILES=34/34 … rev=41038ed7 receipts_rev=352924bb`
   and `DETECTOR_WITNESS=17/17`; the landing state is `35/35`, `18/18` at F3/C3 (SCORECARD and
   `after/*.txt` agree). The earlier pair is genuine for its own revision (C-era receipts), so this is
   staleness, not fabrication. Append a correction entry in round 95 naming the superseded text; do not
   rewrite the round-94 block.
3. **D3 — lesson `## Gate` omits the URL and access date for the new row.** `corpus/lessons/round-94.md`
   `## Gate` gives the location (`man1/git-clone.1` OPTIONS, `-s, --shared` body) and the quote, but the
   URL (`https://git-scm.com/docs/git-clone`) and the access date (`2026-11-08`) appear only in the
   `S221` row/anchor. `CORPUS.md` contract v1 rule 1 requires the lesson to record all three for every new
   row. Record all three for any row added in round 95.
4. **D4 — ledger artifact attribution (C2).** The `R94CriticClaims` row claims a two-line-predicate finding
   the seat does not file (its C2 predicate row reads "reproduced verbatim | bound"); the finding belongs to
   `R94ReviewerC2` F3. The narrowing (Amendment 2(c)) is real. Name the seat that actually filed it.
5. **D5 — ledger scope over-broad (C1/Sentinel).** The row claims no containment guard for
   `--expected`/`--receipts`; the seat measured `--work`, symlinked pin rows, `--pins`, `--receipts-rev`.
   The guard exists (`control-driver-r94.py:486-494`), so attribute it to Amendment 8, not to the seat.
6. **D6 — ledger scope (C3/ExecC3Repro).** "both named limits measured" should read "named limits 1 and 4
   measured; 2 and 3 declared unmeasured", which is what the seat says (`R94ExecC3Repro.md:176`).
7. **D7 — `plans/round-94.md` Amendment 4 is stale on its revision pair.** It calls the green run "at
   F2/C2"; `after/c1-forgeries.txt` first lands at F3 `ebbcbe39` / C3 `d13c2ff2`
   (`# computed_against F=ebbcbe39 C=d13c2ff2`) and no `after/` file exists at C2 `f276d7fb`.
8. **D8 — `plans/round-94.md:86` preamble is stale.** It says every amendment was applied before `C2`;
   Amendments 8-9 (sentinel findings) land at F3 `ebbcbe39`.
9. **Carried debt re-flagged.** Round-93 routed items D2/D5/D6 are closed in this round (the `22/22`
   correction, `computed_against` on every scored receipt, and the r82 clip range carried in the round-95
   planned block); D3's "eleven amendments vs 12" does not recur. The round-93 D1 ledger is now present and
   passes.

## Operator notes

All four `SHONEN` boxes carry resolvable, non-author-checkable evidence (SKILL.md `## Gates` table,
`LOG.md` round-94, `scripts/measure-all-r94.sh` + `after/*.txt`, `PROVINCE.md` untouched) and the lane wrote
no `[x]`. Box 2's end-to-end task is the three-counter re-measurement chain (meta-work on the lane's own
instruments), which the operator should weigh as domain work before any promotion. Promotion and any `[x]`
are operator-owned; none was written here.

No lane-authored file was edited by this closure; the only lane write is this file, and no other lane was
touched. No tool was installed or upgraded.
