# Round 80 — the scored set stops being a committed table, and a Gate record becomes a line a counter re-opens

Lane `chousa`. Base revision `b7803829922770b890e9f4efdd30d12c3695439a` (round-79 tip, closed
`ok` / `rejected-honest-stop` by the non-author spot-check `corpus/lessons/round-79-verifier-spotcheck.md`).
Claims frozen in `corpus/evidence/round80/claims.md`; the freeze evidence is the wave-spec commit
`0d253c95732c0ed19a9fa414e5d17769ddefa48d`, whose parent `0f59b985933b2fe9b0b6a754d908ac6ae47399e6`
carries the instruments, the claims text and the two do-nothing controls (see `## Mistakes`, row 1:
the preservation commit landed all three together, so this round's controls-before-freeze ordering is
shown by commit order only, not by separate commits).

Two claims, two axes, causally separable. C1 operability (lowest scored non-retired axis, the
historical 3/10 held) changes the battery: the scored subject set is drawn per run. C2 calibration
changes the gate record: a `GATE-RECORD` line is re-opened by a counter that reads committed bytes
at a named revision.

## Gate

```
GATE-RECORD S199 rev=b7803829922770b890e9f4efdd30d12c3695439a path=corpus/lessons/round-79-verifier-spotcheck.md line=222 words=12 quote=the battery is recording forgeable through the payload channel on **both** batteries
GATE-RECORD S200 rev=b7803829922770b890e9f4efdd30d12c3695439a path=corpus/QUALITY.md line=1056 words=20 quote=A subject-identity salt is defeated by any normalizer that knows its marker family, so the closure is a per-channel measurement
GATE-RECORD S201 rev=b7803829922770b890e9f4efdd30d12c3695439a path=corpus/QUALITY.md line=1054 words=25 quote=A self-assessment counter validates each resolution line against the bytes it claims to repair, and its audit window covers every block rather than the newest.
GATE-RECORD S202 rev=3eb4a3cad8febf75698a017cb6c4441f763b3454 path=.ufo/waves/round-78/w1/R78ReviewB/atkB2-new-block-window.txt line=11 words=2 quote=SELFCHECK=PASS unresolved=0/3
```

- Admit S199, own-work B, scoped to whether an outer battery's PASS line is reachable without
  scoring a subject. `corpus/lessons/round-79-verifier-spotcheck.md` at
  `b7803829922770b890e9f4efdd30d12c3695439a`, line 222, quote inside its operability row. Opened
  2026-11-04. Located quote: "the battery is fully forgeable through the payload channel on
  **both** batteries" (12 words, `wc -w`). Grounds C1's target: the scored set must be drawn fresh
  per run, because a committed subject set is a table any decoder can read.
- Admit S200, own-work B, `supersedes S196 —`. `corpus/QUALITY.md` at
  `b7803829922770b890e9f4efdd30d12c3695439a`, criterion 147 at line 1056. Opened 2026-11-04.
  Located quote: "A subject-identity salt is defeated by any normalizer that knows its marker
  family, so the closure is a per-channel measurement" (20 words). The round-79 lesson quoted 25
  words of this sentence while `wc -w` prints 27 (the spot-check's finding); the superseding row
  states 20 words, measured.
- Admit S201, own-work B, `supersedes S197 —`. `corpus/QUALITY.md` at
  `b7803829922770b890e9f4efdd30d12c3695439a`, criterion 146 at line 1054. Opened 2026-11-04.
  Located quote: "A self-assessment counter validates each resolution line against the bytes it
  claims to repair, and its audit window covers every block rather than the newest." (25 words,
  measured); the round-79 lesson stated 24, off by one.
- Reject S202, own-work C, `supersedes S198 —`. `.ufo/waves/round-78/w1/R78ReviewB/atkB2-new-block-window.txt`
  at `3eb4a3cad8febf75698a017cb6c4441f763b3454`, lines 1–11 (the file is eleven lines; the round-79
  row said "lines 1-20"), quote on line 11. Opened 2026-11-04. Located quote:
  `SELFCHECK=PASS unresolved=0/3` (2 words). REJECTED, reason unchanged from S198: a receipt that
  prints one counter's false green is that counter's own evidence, not a source about how
  self-assessment should be audited (the S195 class one layer out). Flip: admit scoped to what a
  control receipt must carry if an admitted entry ever rests on receipt format.
- Record correction, old→new: S196 (`25 words` stated, 27 measured) → S200 (`20 words` measured);
  S197 (`24 words` stated, 25 measured) → S201 (`25 words` measured); S198 (`lines 1-20`, quote
  absent from the file) → S202 (`lines 1-11`, quote located on line 11). The superseded rows stay in
  the registry with their bytes untouched (append-only, `CORPUS.md` rule 2); no `status`, `recheck`
  or `used-by` cell of an existing row changed this round.
- No URL was opened or fetched: all four rows are revision-pinned committed paths, opened by
  `git show <rev>:<path>`.
- Non-author spot-check requested: three admits and one reject above. Dispatched wave seats are
  author-lane evidence, not independent admission or promotion reviewers.
- Assimilation: none. The `merge/chousa/` package stays closed (round 78 measured 111 of 114 staged
  ids colliding with the live registry; the id drift is not renumbered in scratch). No package
  bytes read into the lane, no campaign tool run, no shokuknow write.
- `considerthese/2026-10-26.md` (2026-10-26, the newest) was opened; **proposal 4 — one independent
  CJK quote spot-check per review — is adopted** as QUALITY 158, because `wc -w` prints 2 for a
  68-character CJK span line, so the ≤25-word bound cannot measure such a row. Proposals 1 (stable
  ids) and 2 (recurring-weakness streaks, already running as `corpus/evidence/round53|55|62/recurring.tsv`)
  and 3 (lane-vs-verifier disagreement list, partly covered by QUALITY 14) were not picked, one
  proposal per round.

## Claim outcomes (measured on committed bytes)

| claim / axis | before → after | counting command / evidence | verdict |
|---|---|---|---|
| C1 operability (lowest scored non-retired axis; the historical 3/10 held) | a committed subject table that a structure-identity matrix passes without scoring (before: `BATTERY_EXIT=0 BATTERY_VERDICT=PASS RECEIPT_LINES=113`, `ORACLE=ACCEPTED`, exit 1) → a per-run drawn set with the fresh positive/forger legs and the five enumerated oracles scored (after: `BATTERY=PASS forgers_rejected=11/11 positive=2/2 fresh_positive=2/2 fresh_forgers=2/2 oracles_rejected=5/5`, exit 0, 97.3 s) | `python3 -B corpus/evidence/round80/matrix-battery-v7.py --matrix corpus/evidence/round76/loader-matrix-v3.py --work DIR --runs 1 --fresh 2 --rev b7803829922770b890e9f4efdd30d12c3695439a`; `controls/{oracle-before-r80,v7-legit-matrix-r80}.txt` | **falsified by its own kill rule — honest stop**: the legitimate matrix is refused on some draws (`BATTERY=FAIL … fresh_positive=1/2 fresh_forgers=1/2`, `… fresh_positive=0/3 fresh_forgers=0/3`), and two HIGH defects hollow the clause (below) |
| C2 calibration (sourced on S199) | three prose Gate records nothing re-opened (`GATE_GROUNDING=FAIL unresolved=3 superseded_resolved=0 audited=S196,S197,S198`, exit 1) → four machine-checkable records re-opened on committed bytes, the three superseded rows resolving through their replacements (`GATE_GROUNDING=PASS unresolved=0 superseded_resolved=3 audited=S199,S200,S201,S202`, exit 0) | `python3 -B corpus/evidence/round80/gate-grounding-check.py --rev 44d09edfc20dba26ee8d58a93d365989916a2692`; `controls/{grounding-before-r80,grounding-after}.txt` | **improved**, with three instrument limits recorded (below) |

Do-nothing controls: at the base the v6 battery accepts the structure-identity oracle
(`controls/oracle-before-r80.txt`) and the C2 counter prints `unresolved=3` with `record=none` on all
three rows (`controls/grounding-before-r80.txt`). A round that does nothing cannot reach either
after-state.

## Instrument limits (measured by the wave, recorded, not repaired after scoring)

1. **The fresh leg's ground truth is the subject under test.** `matrix-battery-v7.py:125` sets
   `WITNESS = LANE/corpus/evidence/round76/loader-matrix-v3.py`, and the frozen counting command
   passes that same path as `--matrix`; `MATRIX_SHA256=b79d6441…913f` in
   `controls/v7-legit-matrix-r80.txt` equals `sha256sum corpus/evidence/round76/loader-matrix-v3.py`.
   `draw_fresh` labels its re-emitted copies from the witness's own rc/marks/cells, so
   `fresh_positive=2/2 fresh_forgers=2/2` assert self-consistency for that subject (a
   wrong-but-self-consistent matrix satisfies them); a constant-verdict matrix is still caught (no
   FORGER can be drawn). Receipt: `.ufo/waves/round-80/w1/R80SentinelA/receipts/06-fresh-leg-ground-truth.txt`.
2. **One of the five counted oracle rejections never produced a verdict.** All 17
   `ORACLE:structure-identity RUN` lines in `controls/v7-legit-matrix-r80.txt` read
   `matrix_exit=1 marks=none content=bad`, and line 180 counts the oracle `REJECTED`:
   `_rename` (`matrix-battery-v7.py:231-282`) renames class-body `Name` stores but not
   `ast.Attribute.attr`, so the re-emitted oracle raises `AttributeError: '_7ff523aa' object has no
   attribute 'canon'` and exits 1 with no stdout. `oracle_ok += not full` cannot tell "missed" from
   "never ran", so `oracles_rejected=5/5` overstates the anchor and the strongest known adversary is
   destroyed before it can be measured. Reproduced independently by the seat
   (`R80SentinelA/receipts/09-rename-defect-repro.txt`: the oracle alone prints
   `LOADER_MATRIX=12/12 MATRIX=PASS` exit 0).
3. **The record grammar's four rules are discriminating only within their own scope.** R3 tests a
   substring of one named line, so an enormous line can host an unrelated quote that passes; R4
   bounds the count, not the substance; a superseded parent is counted resolved through its
   replacement's passing record, which is a re-filing and not a proof that the parent's defect is
   gone; and the audit window is `--since-round`, so a row whose only `- Admit`/`- Reject` bullet sits
   in an older lesson is never audited — measured: `--since-round 79` audits 3 rows
   (`S196,S197,S198`) while `--since-round 70` (or 1) audits 17 and reports
   `unresolved=17` (`S182`–`S198`), so 14 records that a lesson names are outside the frozen window. Measured by `R80ReviewerB` and `R80CriticA` (receipts under
   `.ufo/waves/round-80/w1/`).
4. **Revision labels.** `matrix-battery-v7.py:657` prints `git rev-parse master` as `LANE_REV`, and
   the instrument first exists at `0f59b985`, not at the `b7803829` it prints
   (`git cat-file -e b7803829:corpus/evidence/round80/matrix-battery-v7.py` → `fatal: … exists on
   disk, but not in 'b7803829…'`). The bytes measured are the worktree bytes whose sha256 is pinned in
   `claims.md`; the label is a token, not a binding. `R80SentinelA` F5.
5. **A frozen claims-file count the landed record contradicts.** `claims.md:90` calls S200's quote
   "15-word"; the landed record measures 20 (`wc -w` on `corpus/QUALITY.md:1056@b7803829`) and the
   counter confirms `quote_words=20`. No counter reads `claims.md`, so the frozen 15 is re-opened by
   nothing; the file is not amended (freeze is freeze) and the landed record is the measured one.
   `R80ScribeB` F6.
6. **A frozen claims-file description the landed row does not match.** `claims.md` describes S199 as
   "own-work A: the round-79 structure-identity receipts"; the landed row S199 is tier B and cites the
   spot-check's §4 payload line (222), which grounds the same requirement one channel out. The frozen
   file is not amended; the row that landed is the one the counter audits. `R80ScribeA` F5.

7. **A second `GATE-RECORD` for one id is a silent overwrite, and the verdict follows tree order.**
   `records_at()` overwrites `out[id]` per id, so the last record in `git ls-tree` order wins: a
   defective S200 record in `round-79.md` is invisible next to the good one in `round-80.md`
   (`R80ReviewerB/60-f5-last-wins-hides-defect.txt`) and surfaces when it sorts later
   (`60b-f5b-sort-order-escape.txt`). QUALITY 160 carries the successor rule.
8. **The oracle enumeration is a fixed five-tuple.** `ORACLES` in `matrix-battery-v7.py` is a
   literal five-entry table, `--fresh` draws subjects only and the instrument takes no `--oracle`
   argument, so a sixth oracle written today is rejected only if it happens to fall inside the
   table's coverage — the predicate's `oracles_rejected=5/5` says nothing about an oracle the round
   did not name. `R80CriticA` finding F4.

## Mistakes

| class | evidence | captured-by | fix |
|---|---|---|---|
| a round-80 attempt died mid-work and the orchestrator preserved its instruments, controls and claims text in one commit, so the round's controls-before-freeze ordering is shown by commit order only | `git show --stat 0f59b985933b2fe9b0b6a754d908ac6ae47399e6` lists `claims.md`, both control receipts and the four instruments in a single commit; the freeze evidence for this attempt is `0d253c95732c0ed19a9fa414e5d17769ddefa48d` | nothing: no criterion bound the preservation commit's shape, and the round-close sweep is the orchestrator's, not the lane's | recorded here and in the report; the next round writes `claims.md` only in its own freeze commit, and QUALITY 153 makes every receipt name the revision it measured so a preserved attempt's receipts stay re-derivable |
| the inherited attempt left about 2.1 GB of clones under `/tmp` (`r80-base`, `r80-decl`, `r80-tip`), outside `$HYAKU_SCRATCH` | `scripts/hyaku/disk-guard.sh status` lists `/tmp/r80-tip 698.7M`, `/tmp/r80-decl 688.0M`, `/tmp/r80-base 687.3M` at 2026-11-04T23:55 | the §7 scratch rule names `$HYAKU_SCRATCH` but nothing fails when a seat ignores it; the reaper only deletes idle entries, so these survived the attempt | this attempt kept every clone, work dir and receipt under `/fast/scratch/hyaku/chousa-r80/` and removed the tree at landing; the receipts name the scratch root they were produced in |
| a QUALITY criterion cited a receipt that was not yet committed, and the round-79 counter caught it | `python3 -B corpus/evidence/round79/selfcheck-v2.py --lane .` printed `CHECK S2-quality-pointers FAIL criteria=55 missing=[116, 152, 153] unresolved=['152:controls/grounding-after.txt', '153:corpus/evidence/round80/controls/grounding-after.txt']` until the receipt landed in `5ba30d87172e94dd76a49e1a94294561e90f6cbd`, after which it prints `S2-quality-pointers ok … unresolved=[]` | the round-79 counter's S2 leg (a prior round's gate caught this round's slip) | land the receipt before the criterion that cites it, and re-run S2 at the integration revision before the report |
| the C2 predicate is satisfied by rows this round added, so it measures that the record became machine-checkable and not that the three old defects were discovered | `claims.md` C2 predicate: `superseded_resolved=3 audited=S199,S200,S201,S202`, and all four audited ids are new at `44d09edf`; the base bytes carried the defects, not the counter | `R80CriticA`'s do-nothing mirror (base bytes + four rows that say `supersedes` + four records) | recorded, not repaired after scoring: the next counter must re-derive each old defect from the old bytes (the 27-word quote, the eleven-line span) instead of counting the new rows' existence |

## Kill-rule outcomes (frozen before data; reported, never repaired)

- **C2 fires its own kill rule (third clause).** The frozen rule says the claim does not verify "if
  the counter reports `unresolved=0` while a `GATE-RECORD` line names bytes it never opened".
  `R80CriticA/receipts/c2-unopened-superseded-record.txt` shows exactly that: a `GATE-RECORD S195
  rev=b7803829… path=corpus/lessons/does-not-exist.md line=9999 words=1 quote=x` line sits in the
  tree at `18ffcf29`, `git cat-file -e b7803829:corpus/lessons/does-not-exist.md` returns 128, and
  the counter prints `GATE_GROUNDING=PASS unresolved=0 superseded_resolved=4`. Cause, read from the
  source: `records_at()` collects every record, but the audit loops only over `audited` tips and
  `parents`, so a record attached to a non-tip row is parsed and never opened. **C2 as written does
  not verify**; the mechanism still lands and the three defects are genuinely closed, and QUALITY 155
  carries the successor rule.
- **A hollow record passes the counter.** `R80CriticA/receipts/c2-donothing-control.txt`: base bytes
  plus four rows whose `teaches` says `supersedes` plus four records quoting the single word `S` on
  `corpus/SOURCES.md:1` reach `GATE_GROUNDING=PASS unresolved=0 superseded_resolved=3`. R1–R4 check
  that a quote exists on a named line, not that it grounds `teaches`: the predicate measures that the
  record became machine-checkable, never entailment. The landed records are grounded because this
  lane measured each quote against its line, not because the counter can tell.
- **C1 fires its own kill rule ("or if the legitimate matrix is refused").** The frozen counting
  command is draw-dependent: the same bytes print `BATTERY=PASS … fresh_positive=2/2 fresh_forgers=2/2`
  on one run and `BATTERY=FAIL … fresh_positive=1/2 fresh_forgers=1/2` on the next
  (`R80ExecA/r80a-after-v7-run1.txt`, `r80d-v7-run2.txt`), and `--fresh 3` prints `BATTERY=FAIL …
  fresh_positive=0/3 fresh_forgers=0/3` (`r80d-v7-run3-fresh3.txt`). Cause, measured:
  `f"{base_name}#{i}"` names a fresh positive and a fresh forger identically when they share a base,
  and `score()` is keyed by name, so both score `MISS` (`R80CriticA/receipts/c1-name-collision-probe.txt`:
  `fresh_positive=0/1 fresh_forger=0/1`). **C1 as written does not verify**; QUALITY 159 carries the
  successor rule (a drawn name carries its label; the command is run k>=5 times and every run must
  print the same line).
- **C1's remaining content stands.** The structure-identity and payload-decode matrices do **not**
  reach the PASS line on the drawn set (`a10-as-matrix-fresh2`: `BATTERY=FAIL … fresh_forgers=0/2`),
  where round 79's v6 accepted both, so the drawn leg discriminates the two known forged matrices
  even while its own naming is unstable.
- **C1: the predicate line holds; two clauses are hollowed.** The literal kill rule (any enumerated
  forger/positive/fresh case/oracle `is a MISS`, or the legitimate matrix refused) did not fire: all
  eleven forgers, both positives, both drawn legs and all five oracle slots are counted as the
  predicate says. But the wave measured that one of those five counted oracle rejections
  (`ORACLE structure-identity REJECTED positive=0/2 forger=0/11`) is a `_rename` crash that produced
  no verdict at all, and that the drawn legs' witness is the subject under test — so the predicate's
  `oracles_rejected=5/5` clause is not substantiated for that oracle. **Reported as a narrowed
  improvement, not as a clean pass**; the two repairs are QUALITY 156–157 and the round-81 plan.
- **A fresh-leg name collision fails closed.** `R80CriticA/receipts/c1-name-collision-probe.txt`:
  when a fresh positive and a fresh forger share one drawn name (`X#0`), `score()` keyed by name
  reports both `MISS` and prints `fresh_positive=0/1 fresh_forger=0/1` — a false negative, not a
  false green, so the collision costs a re-run rather than a bad admission.
