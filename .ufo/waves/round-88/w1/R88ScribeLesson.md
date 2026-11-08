# R88ScribeLesson — round-88 lesson settlement sections: audit against committed bytes

Seat: `R88ScribeLesson` (scribe; leaf member — no subagent dispatch, no production edit, no lane/fleet git
mutation, no network). Lane root `/home/vgpnk/Projects/shokunin/chousa-shokunin`. Nothing outside this seat's
folder `.ufo/waves/round-88/w1/R88ScribeLesson/` was written; the lesson, plan, QUALITY, `corpus/SOURCES.md` and
every corpus file were read only. Scratch `/fast/scratch/hyaku/chousa-r88/R88ScribeLesson/` was deleted before this
report was written; every receipt cited below was copied into `receipts/` first.

Revisions read: base `f484d94f`, freeze/landing `4ea9d008abfd2e09cb51649a42678a78f52ac530`. The freeze commit
carries the counters, the control batteries, the pins and the one entry repair; there is no separate landing
commit. `git status --porcelain` at the lane shows only `?? .ufo/waves/round-88/` — **no L1 draft lesson exists
yet** (`corpus/lessons/round-88.md` is absent), so every statement below is drafted from committed bytes plus the
wave's own reports, and every sentence that would name a lesson line must be re-checked against the L1's draft.

Tooling: nothing installed. `python3` (3.14.8, system), `git`, `tar`, `sha256sum` — all pre-existing. The
pacman pause was respected (no package transaction of any kind); no `sudo`, no host sysctl, no service control.

---

## (a) The `## Gate` block: what round 88 owes, and does the Q1 quote re-open verbatim?

### (a1) The lesson must carry a `## Gate` block — this is a hard gate, not a convention

`tools/lane-preflight.py` gate **G03** ("every `corpus/lessons/round-<N>.md` has a heading line beginning
`## Gate`") fails without it. Receipt `r11` (clone **with** the heading) and receipt `r16` (the same clone with the
heading removed):

```
$ python3 -B tools/lane-preflight.py --root . --only G03      # lesson HAS "## Gate"
GATE G03 lesson-gate PASS 66 lessons carry ## Gate
PREFLIGHT=1/1 FAILED=none …
exit=0

$ python3 -B tools/lane-preflight.py --root . --only G03      # same lesson, heading removed
GATE G03 lesson-gate FAIL 1 without ## Gate: round-88.md
PREFLIGHT=0/1 FAILED=G03 …
exit=1
```

So the round-88 lesson **must** have a `## Gate` heading or the lane's own preflight fails. This is also the lane's
standing shape — every one of the 65 existing lessons carries one (`GATE G03 lesson-gate PASS 65 lessons carry
## Gate`, receipt `r19`).

### (a2) Round 88 owes exactly ONE `GATE-RECORD` line, in the `rev` form, for `S218`

What the round did **not** do, measured at the freeze (`git diff --stat f484d94f 4ea9d008 -- corpus/SOURCES.md
corpus/captures/` is empty; `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → 218 at both
revisions):

- **No registry row was opened, re-anchored or re-opened.** `corpus/SOURCES.md` is byte-identical between base and
  freeze, so QUALITY 173 ("every registry row the round opened, re-anchored or re-opened is recorded in a
  `GATE-RECORD` line at this round's `fetched` time") is satisfied by *zero* url-form records. The round's own
  sources (`S216`, `S218`) are cited through the round-87 claims file (`corpus/evidence/round88/claims.md`:
  "both through the round-87 claims file"), so no new `url=` line is owed for either.
- **No fetch happened.** `awk -F'\t' 'NR>1 && $5 >= "2026-11-08T07:00:00Z"' corpus/evidence/round57/refetch.tsv`
  → 0 rows (the newest row in the ledger is `2026-11-08T06:50:40Z`, round 87's). A `url/admit` or `url/unreach`
  line would be a record with no fetch behind it, and `tools/gate-records.py` would refuse it (`REFETCH`).

What the round **does** owe is the one line the round-87 non-author check routed (spot-check `## Routed defects` 3,
quoted verbatim in `plans/round-88.md` §Inputs 3): *"Quote criterion 178's operative clause (≤25 words) in this round's
lesson before any new row is admitted."* `S218` is an `own-work` row whose source cell names `corpus/QUALITY.md`,
so the only form that fits is `rev` (no URL, no fetch, a path + line in a commit).

**The candidate line, verified.** Receipts `r09` (grounding counter), `r10` (harm sweep), `r11` (preflight), `r14`
(the row and the line number):

```
GATE-RECORD S218 rev=4ea9d008abfd2e09cb51649a42678a78f52ac530 path=corpus/QUALITY.md line=1120 words=11 quote=A frozen `teaches` cell is not evidence; the superseding row's is.
```

| check | command | observed | exit |
|---|---|---|---|
| record form | `python3 -B tools/gate-records.py verify --root . --repo <lane> corpus/lessons/round-88.md` | `GATE_RECORD corpus/lessons/round-88.md:5 S218 OK` · `GATE_RECORDS files=1 records=1 ok=1 fail=0` | 0 |
| grounding counter | `python3 -B corpus/evidence/round80/gate-grounding-check.py --rev HEAD --since-round 79` (clone carrying this lesson) | `ROW S218 record=ok quote_words=11 location=corpus/QUALITY.md:1120@4ea9d008abfd words=11 verdict=OK` · `GATE_GROUNDING=PASS unresolved=0 superseded_resolved=3 audited=S199,S200,S201,S202,S218` | 0 |
| harm sweep | `python3 -B corpus/evidence/round88/harm-recheck.py --root . --repo <lane> --base-tool <f484d94f blob>` | `HARM_RECHECK files=12 records=29 moved=0 base_rc=0 r88_rc=0` | 0 |
| preflight G03 | `python3 -B tools/lane-preflight.py --root . --only G03` | `GATE G03 lesson-gate PASS 66 lessons carry ## Gate` | 0 |

Two things the L1 must know about that line:

1. **The rev pin is load-bearing and must be the freeze, not the landing.** `line=1120` is criterion 178's line
   number **at `4ea9d008`** (`git show 4ea9d008:corpus/QUALITY.md | grep -n '^178\. '` → `1120:`; the file has
   1195 lines). `tools/gate-records.py` resolves a `rev` record's line **inside the blob at that rev**, so a later
   QUALITY append does not move it — but if the L1 pins the landing commit instead, the line number must be
   re-measured at that commit after the new criteria are appended. Pinning `4ea9d008` makes the record immune.
2. **The record count in the harm receipt moves by exactly one.** The committed control
   `corpus/evidence/round88/controls/receipts/c1-harm.txt` reads `files=11 records=28 moved=0`; with the
   round-88 lesson present the sweep reads `files=12 records=29 moved=0` (receipt `r10`). The claim's K3 substance
   (`moved=0`) holds; the count is revision-scoped, exactly as round 87 recorded in its `## Corrections` row 2. The
   lesson should say so rather than quote 28.

### (a3) The provenance repair row's `Q1` quote re-opens verbatim — VERBATIM, exit 0

The freeze's entry repair narrowed the row *"Naming what a resource derives from"* from `Q1, Q3 (S215)` to
`Q1 (S215)`. `Q1`'s quote is `"Provenance chains comprising only Entities can be formed using the prov:wasDerivedFrom
property."` Receipt `r03`:

- `Q1 == S215_RECORD_QUOTE` → **True** after normalization — byte-identical to the quote already carried by
  `corpus/lessons/round-85.md:14`'s `GATE-RECORD S215` line (`words=12` on both sides).
- `Q1_IN_COMMITTED_CAPTURE` → **True**; the quote occurs at raw line **779** of
  `corpus/captures/6e48bcc4a04d13b7b3ebb68e.txt`, whose capture key equals `sha256("https://www.w3.org/TR/prov-o/")[:24]`
  (`capture_key_ok: True`) and whose `sha256` is `8c9aeabb466fb6d133c6a83cfc546a49336af782d0b7f2fccebcc55c2eb1f2a4`
  — the same prefix the round-85 record's `capture_sha256=8c9aeabb466fb6d1…` claims.

**The named command was run.** `python3 -B tools/quote-reopen.py verify --items <tsv>` against the live registry
URL is a network GET, and this round forbids network ("every check reads committed bytes (a GET is a finding)"), so
the tool was run **unmodified** through the lane's own committed loopback harness
(`corpus/evidence/round30/qr_harness.py`), which replaces the child's socket layer and serves the **committed
capture bytes**. Receipts `r05` (Q1) and `r13` (S216):

```
[positive] cmd=python3 -B tools/quote-reopen.py verify --items positive.tsv --registry registry.md
[positive] rc=0 verdicts={"Q1-S215": "VERBATIM"} net_events=2
[negative] rc=1 verdicts={"NEG-absent": "ABSENT"} net_events=2
[S216]    rc=0 verdicts={"S216-quote": "VERBATIM"} net_events=2
```

Two notes the L1 must carry rather than gloss:

- **The negative control matters.** The same run's absent-phrase item returns `ABSENT` at exit 1, so the
  `VERBATIM` is a discriminating result and not a blanket accept.
- **The loopback registry row used `http://`, not `https://`.** The harness serves plain HTTP; an `https://` URL
  against it is `UNREACHABLE` at exit 1 (receipt `r18`, run with the same registry row but `https://`). The tool's URL extraction,
  normalization and boundary matching are scheme-independent, and the served body is the committed capture — but
  the *live* page was not contacted, so this is a re-open against committed bytes, not against the live W3C
  document. The lane's own `found()`/`norm()` applied directly to the committed capture agree
  (`found(committed_capture_text, Q1): True`, `found(capture, absent_phrase): False`, receipt `r04`). The
  round-87 lesson's `S215` record already establishes the live-page location.

The lesson therefore owes **no web-quote re-open beyond this**, and its `## Gate` block carries one `rev` line
(S218) and no `url=` line. `tools/gate-records.py verify` over the whole committed lesson set still passes with
that addition (receipt `r08` is the S215/S026/S024 set of round-85: `GATE_RECORDS files=1 records=3 ok=3 fail=0`,
exit 0; the wide harm sweep at `r10` covers all 29 records).

---

## (b) `## Mistakes` items — none exist yet; here is the shape they must take

`corpus/lessons/round-88.md` does not exist at the freeze, so there is no `## Mistakes` section to audit. The
requirement is the lane's: every row carries **class · evidence pointer · captured-by · fix**, and every fix names
**a check that can fail**. The round-87 lesson is the shape to copy — 7 rows, each with all four labelled fields
(`**Class:**`, `**Evidence pointer:**`, `**Captured-by:**`, `**Fix:**`, `corpus/lessons/round-87.md:72-136`) — and
each of its fixes names a failable check (e.g. row 3's fix names `sha256sum corpus/captures/b1b13a12aee75c6ecc20fb91.txt`
at two revisions; row 4's names the `url/unreach` parse check that an admit-branch placement returns as `PARSE`).

### The `## Mistakes` rows round 88 owes, each with a failable check

These are the wave's own findings, which the lesson must carry as Mistakes rows (not as a narrative):

| # | class | evidence pointer | captured-by | fix, with a check that can fail |
|---|---|---|---|---|
| 1 | a verdict reconciled only against one detail format: `RECONCILED` is tautological for the three legs whose detail carries no `n/m` ratio | `.ufo/waves/round-88/w1/R88ReviewerC1-receipts/e4-m2-mutadmit-detached.txt` (`MUT_ADMIT_KILLED=0`, `RECONCILED=15/15`, `GATE_RECORDS_R88=PASS`, exit 0) and `…/e4-m3-mutadmit-neverbuilt.txt` (`MUT_ADMIT_DERIVED=0`, exit 0), with the contradicting leg receipts `…/e4-m2-leg-MUT_ADMIT.txt` and `…/e4-m3-leg-MUT_ADMIT.txt`; `R88CriticClaims/receipts/e7c-width-detached.log` and `…/e7b-mutant-detached.log` | `R88ReviewerC1` §(b) and `R88CriticClaims` §(b); no criterion covered a reconciliation that parses one detail format | parse each leg's detail in its own format (`n/n`, `n/n/n pin N`, `derived=… killed=…`, presence) and reconcile against that; **check**: `python3 -B corpus/evidence/round88/mutate-r88.py --root DIR --repo GITDIR --work DIR` must print `MUTANTS_KILLED=8/8` including the new detached-width and detached-mutant shapes, and each detached shape must print `GATE_RECORDS_R88=FAIL` exit 1 |
| 2 | a counter with no verdict-vs-field reconciliation: the verdict is a conjunction of booleans a correct run already makes true | `.ufo/waves/round-88/w1/R88CriticClaims/receipts/c2-dead-teaches.log` (`TEACHES_FLAGGED=0 … LEGS=7/7 CURATION_R88=PASS`, exit 0) and `…/c2-detached-teaches.log` (`TEACHES_UNRESOLVED=1 LEGS=7/7 CURATION_R88=PASS`, exit 0), `…/c2-constants-on-broken.log` (`TEACHES_UNRESOLVED=1 LEGS=7/7 CURATION_R88=PASS` over a broken tree) | `R88CriticClaims` §(b); QUALITY 185 is the class (round 86's `M2`/`M5`) but the round-88 counter has no receipt-file leg at all | derive `passed` from the printed tallies (or give C2 the leg-receipt discipline C1 has); **check**: a dead-`TEACHES` and a detached-`ok` fixture must both print `CURATION_R88=FAIL` exit 1 |
| 3 | a claim clause enforced by code that can never run: the superseder-own-read requirement matches a case-sensitive regex against a lowercased cell | `.ufo/waves/round-88/w1/R88ScoutRegistry/receipt-supclause-dead.txt` (raw-cell match yes, lowercased match `None`) and `…/receipt-probe-run.txt` (`rows=218 raw_cell_matches=10 lowercased_cell_matches=0 case_insensitive_matches=10`); the code is `corpus/evidence/round88/curation-r88.py:250` — the same regex at line 158 runs against the **raw** `cells[6]` and works, so the defect is the lowercasing at 249 | `R88ScoutRegistry` finding 1; no criterion covered a case-mismatched comparison | match the raw cell (or use `re.I`) and keep the clause live; **check**: the one-character-fixed counter must print `LEG_FAIL TEACHES … sup_unresolved=1` / `CURATION_R88=FAIL` exit 1 on the tree the shipped counter accepts |
| 4 | a named limit stated at its true width: the surviving edit class is wider than "a joint rewrite of the writer, the receipts and the reconciliation" | `R88ReviewerC1.md` §(c) — both surviving edits are local (one `ok` expression plus one measurement; one constant plus one `ok`) and touch none of the three named components | `R88ReviewerC1` §(c); QUALITY 187 requires a leg-accounting claim to state what its count guards | restate the limit to name the local `ok`-literal class; **check**: the limit sentence must name a shape the mutation battery actually kills — `mutate-r88.py`'s current 6/6 does not include any detached-`ok` shape, so the limit must not cite the 6/6 as its cover |
| 5 | a frozen control whose expectation and receipt contradict each other | `corpus/evidence/round88/controls/expected.tsv` row `c1-do-nothing` says `expected_exit=1`; `…/controls/receipts/c1-k0-donothing.txt` prints `GATE_RECORDS_R88=PASS`; re-run here: the base blob is byte-identical to the landing tool (sha256 `905f9da2…` both sides) and the case exits **0** (receipt `r07`) — the case is unsatisfiable as written | `R88ReviewerC1` secondary finding and `R88SentinelScope` F7; the round-87 instrument comparison the prose describes is in `c1-k0b-frozen-instrument.txt` | correct the expectation or the receipt, and say which; **check**: the case's exit code must equal its `expected_exit`, and the "Before" prose must name the receipt that carries the round-87 comparison |
| 6 | a plan that describes a freeze it does not contain | `plans/round-88.md:4` and `:74-75` say the freeze commits `claims.json` and "the egress table"; `git ls-tree 4ea9d008 corpus/evidence/round88/ --name-only` lists 10 entries, **no** `claims.json`, and there is no `egress-approval.md` for round 88 (rounds 81–87 each have one) — receipt `r12` | `R88SentinelScope` F4; no criterion covered a plan's description of its own freeze | amend the two sentences to name what the freeze carries (and record that round 88 was a loopback-only window, so no egress table was required); **check**: every file the plan's freeze sentence names must exist at the freeze commit |
| 7 | a routed-defect count that does not sum to the thing it counts | the round-87 spot-check's split reads "three/four/three" (summing to 10) while `grep -cE '^18[2-9]\. ' corpus/QUALITY.md` → **8** and `plans/round-88.md:18-19` reads "three / two / three" (3+2+3 = 8) — receipt `r15` | this seat's audit of the plan against the spot-check; the plan's split is the arithmetically correct one | land the lesson's `## Corrections` row with the **eight** criteria and the plan's split; **check**: the three parts must sum to 8 |

Each of rows 1–4 has a check this seat did **not** run (no lane or wave mutation is in this seat's scope, and the
row-3 and row-1 fixes are the L1's repairs to write); each is stated with the receipt that exhibits the defect.

**What the round-88 lesson must not do**: carry a `## Mistakes` row whose fix names a check that cannot fail. The
round-87 lesson's row 5 is the counter-example in this lane's own history — it asserted a guarantee the mechanism
does not give, and it was corrected only by a plan amendment.

---

## (c) The settlement paragraph

Drafted in full in `.ufo/waves/round-88/w1/R88ScribeLesson/lesson-settlement-draft.md`, marked DRAFT, with the seat
names it read. Its tally, from every `VERDICT` line in the wave (receipt `r17-verdicts-read.txt`):

- **Fired (3 seats, 5 lines):** `R88ReviewerC1` (C1), `R88CriticClaims` (C1 and C2), `R88ExecC2Forge` (C2),
  `R88ScoutRegistry` (C2).
- **Held (8 seats, 16 lines):** `R88ExecRepro` (C1, C2), `R88ExecHarm` (C1), `R88ExecForge` (C1 — see below),
  `R88MutCounter` (C1, C2), `R88ReviewerC2` (C2), `R88SentinelScope` (C1, C2), `R88ConnectorSiblings` (C1, C2),
  `R88ScoutRegistry`'s second line (C2 `n/a`, the campaign package).
- **No `VERDICT` line:** `R88ExecForge.md` — the report's own content reads as C1 held (28 probes, zero accepted
  forgeries; the one acceptance is a genuine committed row under the documented failure grammar). This seat's tally
  counts it as held on content and records the missing trailer as a finding.

---

## Findings, ranked

**F1 (medium) — the C1 `RECONCILED` conjunct is tautological for three of fifteen legs, and the claim's sentence
says the opposite.** `gate-records-r88.py:622-623` reconciles only a `detail=(\d+)/(\d+)` detail; otherwise
`n_ok = (got_ok and ok)`, which is true by construction. The three legs whose detail has no ratio — `TOOL`
(`tool present`), `MUT_ADMIT` and `MUT_UNREACH` (`derived=X killed=Y`) — are therefore reconcilable by
construction. Two seats fired on this and it is inside the claim's own K4 ("a leg's `ok` value is detached from its
measured detail, while the frozen predicate still prints `PASS`"). *Evidence:* receipts `e4-m2-mutadmit-detached.txt`,
`e4-m3-mutadmit-neverbuilt.txt`, `e4-m2-leg-MUT_ADMIT.txt`, `e4-m3-leg-MUT_ADMIT.txt`,
`combined-width-mutant-detached.log`, `e7c-width-detached.log`, `e7b-mutant-detached.log`,
`combined-legs/D1_WIDTH.txt` (`D1_WIDTH=ok detail=3/3/1 pin3`), `combined-legs/MUT_ADMIT.txt`
(`MUT_ADMIT=ok detail=derived=0 killed=0`). *Captured by:* `R88ReviewerC1` §(b), `R88CriticClaims` §(b). *Fix:*
per-format reconciliation; *failable check:* the mutation battery must print `MUTANTS_KILLED=8/8` with the detached
shapes included, and each must print `GATE_RECORDS_R88=FAIL` exit 1.

**F2 (medium) — `curation-r88.py` prints `CURATION_R88=PASS` over its own honestly-printed failures.** The counter
has no leg-receipt mechanism at all: `passed = len(legs) == EXPECTED_LEGS and all(ok for …)` (line 628 area). A dead
`TEACHES` detector prints `TEACHES_FLAGGED=0 … LEGS=7/7 CURATION_R88=PASS`; a detached `ok` prints
`TEACHES_UNRESOLVED=1 LEGS=7/7 CURATION_R88=PASS`. C2's K4 names the dead-detector shape explicitly. *Evidence:*
`c2-dead-teaches.log`, `c2-detached-teaches.log`, `c2-constants-on-broken.log`. *Captured by:* `R88CriticClaims` §(b).
*Fix:* derive `passed` from the printed tallies; *failable check:* both fixtures must print `CURATION_R88=FAIL`
exit 1.

**F3 (medium) — the C2 claim's superseder-own-read clause is dead code.** `curation-r88.py:250` matches
`supersedes (S\d{3,}) —` against `tl = cells[6].lower()`; the raw cell says `supersedes S024 —` and the lowercased
one says `supersedes s024 —`, so the regex never matches. Over 218 rows: 10 raw-cell matches, 0 lowercased, 10
case-insensitive. The identical regex at line 158 runs against the **raw** `cells[6]` and works — which is why the
*disposal* half of the clause behaves and the *own-read* half does not. This seat confirmed the mechanism
independently (receipt `r06`). *Evidence:* `receipt-supclause-dead.txt`, `receipt-probe-run.txt`. *Captured by:*
`R88ScoutRegistry` finding 1. *Fix:* match the raw cell; *failable check:* the fixed counter must print
`LEG_FAIL TEACHES … sup_unresolved=1` / `CURATION_R88=FAIL` exit 1 on the tree the shipped counter accepts.

**F4 (medium) — five in-class C2 forgeries are accepted green.** Duplicate qid cite (`Q1, Q1 (S215)`), reordered
quote rows, an 8-token verbatim substitution on `Q1` and on `Q2`, and a quote-content swap under pinned qids all
print `CURATION_R88=PASS` exit 0. *Evidence:* `R88ExecC2Forge/receipts/run1.log` (`c2-duplicate-qid` → PASS),
`…/run2b.log`. *Captured by:* `R88ExecC2Forge`. *Fix:* the per-entry qid-set pin must bind content, not labels, and
the warrant leg must reject a repeated qid; *failable check:* each of the five shapes must print
`CURATION_R88=FAIL` exit 1 with a named `LEG_FAIL`.

**F5 (medium) — a frozen control's expectation contradicts its own receipt.** `controls/expected.tsv` row
`c1-do-nothing` requires exit 1; `controls/receipts/c1-k0-donothing.txt` prints `GATE_RECORDS_R88=PASS`; re-run
here: **exit 0** (receipt `r07`), because the base and landing subject-tool blobs are byte-identical
(`905f9da2…` both sides). The case as written is unsatisfiable, and the "Before" prose in `claims.md` describes a
round-87 comparison that lives in a different receipt (`c1-k0b-frozen-instrument.txt`). *Captured by:*
`R88ReviewerC1` secondary finding, `R88SentinelScope` F7. *Fix:* correct the expectation or the receipt and name
which; *failable check:* the case's exit code must equal its `expected_exit`.

**F6 (medium) — `plans/round-88.md` describes a freeze it does not contain.** Lines 4 and 74-75 say the freeze
commits `claims.json` and "the egress table"; neither file exists at `4ea9d008` (receipt `r12`). No egress table
was required (round 88 fetched nothing), so the sentence is a documentation defect, not a missing artifact — but a
reader auditing the freeze for the promised machine-form claims finds nothing. *Captured by:* `R88SentinelScope` F4.
*Fix:* amend the two sentences; *failable check:* every file the plan's freeze sentence names must exist at the
freeze commit.

**F7 (low-medium) — the round-87 spot-check's own criteria-split arithmetic does not sum.**
`corpus/lessons/round-87-verifier-spotcheck.md:128-129` reads "three/four/three" (= 10) while the criteria count
is 8 and `plans/round-88.md:18-19` reads "three / two / three" (= 8) (receipt `r15`). The plan's split is correct;
the lesson's `## Corrections` row must carry eight, not the spot-check's phrase.

**F8 (low) — two stale "five criteria mined (QUALITY 182–186)" sentences survive in the lane's own files**, in
`corpus/lessons/round-87.md:172` and `SCORECARD.md:3941` and `:3949`, while eight criteria 182–189 are committed.
The plan routes this to a `## Corrections` row in this round's lesson plus a SCORECARD fix (receipt `r12`).

**F9 (low) — `SCORECARD.md`'s round-87 header says the wave was 13 seats** (line 3930) while the committed evidence
says 12 everywhere else (`w1-spec.json` items = 12, `w1-dispatch.json` `counts.spawn` = 12, `w1-results.json`
results = 12 — receipt `r12`). The plan routes the fix to this round's landing. Round 88's own wave is also 12
seats, so a stale "13" must not be copied forward.

**F10 (low) — `R88ExecForge.md` carries no `VERDICT:` line.** Every other seat report ends with one; this one
ends with a summary of 28 probes and zero accepted forgeries. The settlement tally must either obtain the trailer or
name the seat as held-on-content (receipt `r17`).

**F11 (low) — `R88MutCounter.md` exists twice**, at `.ufo/waves/round-88/w1/R88MutCounter.md` and
`.ufo/waves/round-88/w1/R88MutCounter/R88MutCounter.md`, with byte-identical `VERDICT` lines. A tally that globs
`**/*.md` will count that seat twice (receipt `r17`).

**F12 (informational) — the round-88 lesson's `## Gate` count moves the harm receipt from 28 records to 29**
(`files=11 records=28 moved=0` at the freeze → `files=12 records=29 moved=0` with the lesson present; receipts
`r10`, `r12`). `moved=0` holds; the count is revision-scoped, as round 87 recorded.

---

## Receipt index (this seat's own folder, `.ufo/waves/round-88/w1/R88ScribeLesson/receipts/`)

Every receipt below was written by this seat, under the folder above, before the scratch tree was deleted. The
report cites them by their short number.

| short | file | what it holds |
|---|---|---|
| `r01` | `r01-c1-landing.txt` | C1 battery at `4ea9d008`: the exact frozen line, `GATE_RECORDS_R88=PASS`, exit 0 |
| `r02` | `r02-c2-landing.txt` | C2 counter at `4ea9d008`: the exact frozen line, `CURATION_R88=PASS`, exit 0 |
| `r03` | `r03-q1-quote-identity.txt` | `Q1` is byte-identical to round-85's `S215` record quote; present in the committed capture; capture key and sha256 verified |
| `r04` | `r04-q1-quote-reopen-offline.txt` | the tool's own `norm`/`found` applied to the committed capture: `Q1` found, an absent phrase not found |
| `r05` | `r05-quote-reopen-loopback.txt` | `quote-reopen.py verify` over the lane's loopback harness: `VERBATIM` exit 0, negative control `ABSENT` exit 1 |
| `r06` | `r06-dead-superseder-clause.txt` | the case-mismatched regex over a lowercased cell never matches (the dead C2 clause) |
| `r07` | `r07-c1-do-nothing-control.txt` | the `c1-do-nothing` case re-run with the base tool: `GATE_RECORDS_R88=PASS`, exit 0 — contradicting `expected.tsv`'s `expected_exit=1` |
| `r08` | `r08-gate-verify-round85.txt` | `tools/gate-records.py verify` over round-85's three records: 3/3 OK, exit 0 |
| `r09` | `r09-grounding-with-s218-record.txt` | the round-80 grounding counter over a clone carrying the candidate `S218` line: `ROW S218 record=ok … verdict=OK`, `GATE_GROUNDING=PASS`, exit 0 |
| `r10` | `r10-harm-with-s218-record.txt` | the round-88 harm sweep over the same clone: `files=12 records=29 moved=0`, exit 0 |
| `r11` | `r11-preflight-g03-with-gate.txt` | preflight G03 with the `## Gate` heading present: PASS, exit 0 |
| `r12` | `r12-routed-defects-and-plan-mismatch.txt` | the routed defects 1 and 2 (seat count, criteria count), the plan's `claims.json`/egress-table mismatch, and the freeze's file list |
| `r13` | `r13-quote-reopen-s216-loopback.txt` | the same loopback re-open for `S216`'s 203 clause: `VERBATIM`, exit 0 |
| `r14` | `r14-s218-row-and-quality-line.txt` | the `S218` registry row and criterion 178's line number at the freeze |
| `r15` | `r15-criteria-split-arithmetic.txt` | the criteria-count arithmetic: 8 criteria, "three/four/three" vs "three / two / three" |
| `r16` | `r16-preflight-g03-without-gate-heading.txt` | the same clone with the heading removed: `GATE G03 lesson-gate FAIL 1 without ## Gate: round-88.md`, exit 1 |
| `r17` | `r17-verdicts-read.txt` | every `VERDICT` line in the wave, verbatim, and the seat reports that carry none |
| `r18` | `r18-quote-reopen-https-variant.txt` | the `https://` variant of the loopback re-open: `UNREACHABLE`, exit 1 (the harness serves plain HTTP) |
| `r19` | `r19-lane-preflight-at-freeze.txt` | preflight G01–G03 on the lane at `4ea9d008`: 3/3 PASS, 65 lessons carry `## Gate` |

---

## Limits of this seat

- No lane or fleet git mutation: the only git operations were `git archive` (read), `git clone --shared` into
  scratch (read-only source), and `git commit`/`git checkout` **inside the scratch clone only**. The lane's own
  `git status --porcelain` shows only the untracked `.ufo/waves/round-88/`.
- No network: the only HTTP was to `127.0.0.1` inside the lane's committed loopback harness, serving committed
  capture bytes; `net_events=2` per run, both to the routed global address, which the harness redirects to
  loopback. No external host was contacted.
- The scratch tree, clone, fixtures and receipts under `/fast/scratch/hyaku/chousa-r88/R88ScribeLesson/` were
  deleted before this report was written.
- This seat read the counters and the frozen claims but did **not** mutate either; rows 1–4 of the `## Mistakes`
  table name fixes whose failable checks were not run here, and each is stated with the receipt that exhibits the
  defect rather than with a passing check.
- The L1's draft lesson did not exist during this audit. Every sentence in the settlement draft that would name a
  lesson line, a `## Mistakes` row number or a `## Corrections` row is conditional on that draft.

VERDICT: R88ScribeLesson C1 fired — the frozen battery prints the exact frozen line at `4ea9d008` with `LEG_REREAD=15/15 RECONCILED=15/15 LEGS_APPENDED=15` and `GATE_RECORDS_R88=PASS` exit 0, but two seats showed the `RECONCILED` conjunct is tautological for the three non-`n/m` legs, so a detached `ok` and a credited-but-unbuilt mutant survive with PASS — the firing is against the sentence's "fails the predicate instead of passing on printed fields" clause and is discharged by a per-format reconciliation, not by a narrowing.
VERDICT: R88ScribeLesson C2 fired — the frozen counter prints the exact frozen line at `4ea9d008` with `CURATION_R88=PASS` exit 0 and refuses all five round-87 forgeries (`FORGERY_REFUSED=5/5`), but three seats showed five in-class forgeries accepted green, a verdict printed over honestly-printed failures, and the claim's superseder-own-read clause unreachable at `curation-r88.py:250` — the firing is against the sentence's wording and the counter's dead clause, and is discharged by a per-format reconciliation plus a live superseder-own-read check.
