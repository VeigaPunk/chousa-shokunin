# Round 70 — verifier spot-check (closure)

author: hyaku closure (non-author integrator, zcode subagent (fresh session, non-author))

Date: 2026-11-01. Lane HEAD at closure: `b2f88eccf603be88aa4c217adb5f49813cd82182` (= `origin/master`, pushed); base `1db6babf528692d871a2b97be0b3e519614fa300`. I did not author this round; every command below was run by me at closure time against committed bytes (`git show`/`git cat-file`/`git grep <rev>`) unless marked worktree. This file is written uncommitted by me; the orchestrator commits it.

## Closure ruling (one paragraph)

**rejected-honest-stop, admitted=false, no axis harmed, lane-round ok.** C1's verdict rule was frozen before measurement in `corpus/evidence/round70/claims.md`: battery completes with verdict line + preflight completes with `SKIPPED=none` → improved; if the repaired battery still dies before its verdict line or the preflight cannot complete → honest-stop, red receipts as the defect record. I re-derived both arms: arm 1 is NOT met (the battery transcript ends at case 257, the run was ended at case 258, and no verdict line is printed — `grep -c "^RESEARCH_GATE_SELFTEST:"` → 0); arm 2 IS met (`PREFLIGHT=7/8 FAILED=G08 ENV=none SKIPPED=none`, `EXIT=1`). Per the frozen rule the honest-stop is the rule's own outcome and the lane claimed no operability improvement — I concur, so the round does not admit (a round admits only if every claim verifies; C1 does not verify as an improvement). C2 verifies (re-derived; checker re-executed). Nothing is harmed. The report is a real report with real committed work, so the lane-round is `ok`, not a marker.

## 1. Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report committed by lane identity | `git -C <fleet> log --format='%an <%ae> %H' -1 -- .ufo/reports/round-70/chousa.md` | `chousa-shokunin <chousa@shokunin.local> 2728140c97c3612a83ecba4769a64fb83fb06100` | PASS |
| SHONEN heading | read report | `## SHONEN` present, four `[~]` lines each with a pointer | PASS |
| Cited lane commits exist + ancestry | `git merge-base --is-ancestor <h> refs/heads/master` for 098c23dd, f05eb5ba, b2043bf9, b2f88ecc | all four `ANCESTOR-OK` | PASS |
| Branch tip pushed | `git ls-remote origin refs/heads/master` vs local | both `b2f88eccf603be88aa4c217adb5f49813cd82182` | PASS |
| Round work in range | `git log 1db6babf..b2f88ecc --oneline` | exactly the four cited commits, in the reported order | PASS |
| Report minimum substance | read report + lane LOG | work/pointers, landed changes tied to LOG round-70 entry (LOG line 2097), measurements with commands, Sources & frontier, trend verdicts | PASS |
| Census validate (duty 3) | `bash scripts/sources-census.sh validate --root <fleet> chousa` | exit 0; same five pre-existing W04 duplicate-URL warnings as the committed census-start/end receipts | PASS |

Defects are listed in §5; all are status-neutral.

## 2. Claim re-checks

### C1 — operability, honest-stop per the frozen rule (evidence-verified + re-measured)

Re-measured over committed bytes (commands and observed output):

- Before, no full-run receipt anywhere: `git grep -l "GATE G08 gate-selftest PASS" 1db6babf528692d871a2b97be0b3e519614fa300 -- .ufo/waves/ | wc -l` → **0**. Skip chain: `controls/before-g08-skip-chain.txt` shows all four r67–r69 receipts carrying `SKIPPED=G08` (count 1 each) and r66's wave dir holding no preflight file; r69 summary verbatim `PREFLIGHT=7/7 FAILED=none ENV=none SKIPPED=G08` (re-opened at base, line 12). Matches the report.
- After, the full preflight receipt: `grep -c "SKIPPED=none" corpus/evidence/round70/controls/after-full-preflight-r70.txt` → **1**; lines 14–16 verbatim `GATE G08 gate-selftest FAIL timeout after 180s` / `PREFLIGHT=7/8 FAILED=G08 ENV=none SKIPPED=none` / `EXIT=1`. The wave copy `.ufo/waves/round-70/preflight-final.txt` is byte-identical (diff empty). The 180 s is the documented `G08_SELFTEST_BUDGET_S=180` override in the receipt header — the override mechanism demonstrated, consistent with the 7200 default landing. Matches the report.
- Battery did NOT reach its verdict line: `grep -c "^RESEARCH_GATE_SELFTEST:" after-battery-completes-r70.txt` → **0**; last numbered case line is `ok-case 257 claims-locale-c`; the RUN-END ADDENDUM discloses the run was ended at case 258 (`claims-locale-boundary` gate ran >70 min without emitting its line, D5). The honest-red fact holds. Worktree blob sha256 equals `git cat-file blob b2f88ecc:…` (`cca5426b…`), so the receipt I read is the committed bytes.
- Tool sha256 pins re-derive: `git show b2043bf9:tools/lane-preflight.py | sha256sum` → `c226ec3b…`; `git show b2043bf9:tools/research-gate.sh | sha256sum` → `af061ab2…` — both equal the receipt's pins and are unchanged at HEAD b2f88ecc. Matches `after-digest-derivations-r70.txt`.
- **Repair case-literal invariance (mechanical):** normalized case-invocation literals (`tall|tdrift|tsetup|r24_case|ns_case [^#]*`, whitespace-normalized, sorted) diff **empty** between base 1db6babf and landing b2043bf9 — no case input, expected rc, or expected token changed. All 15 research-gate hunks are at lines ≥ 4389 (inside `run_selftest`, matching the frozen "≥ 4378" scope); `lane-preflight.py` line 233 is byte-identical (sed 233p diff empty); the g08 hunk changes exactly the budget to `int(os.environ.get("G08_SELFTEST_BUDGET_S", "7200"))`. The six append-subject cases are wrapped in `HAVE_FLOCK` conditionals with their literals intact and `skip-case` else-branches reusing the c1lk pattern. Claim verified.
- Guard/skip/probe evidence in the transcript: five flock-reason skips print (`60 verify-all-manifest-append`, `61 verify-all-manifest-two-appends`, `134 json-unterminated-manifest`, `135 json-nul-terminated-manifest`, `234 c1lk-second-append`), plus the pre-existing `233 c1lk-holder-blocks-append`; the case-60 crash site is past (tall cases skip instead of dying); pin-zone failures print as named FAIL-cases. See defect D-70-3 on the "six skips" wording.
- Frozen-rule application: arm 1 (battery completes with verdict line) NOT met, arm 2 met → the frozen rule itself yields honest-stop; no predicate was edited after measurement (claims.md's rule text and the SCORECARD's verbatim quote agree byte-for-byte in substance). The lane claimed no operability improvement; the SCORECARD keeps operability at its historical 3/10. **C1 = honest-stop, concurred; no improvement graded.**

Verdict basis: evidence-verified (committed receipts, digests, frozen rule) plus my own re-measurements above. I did not execute the lane's gate battery (unbounded case 258; the gate standard's verify-committed-evidence rule).

### C2 — calibration, improved (re-measured, checker re-executed)

- Before: `git grep -l "entailment-review" 1db6babf -- corpus SCORECARD.md SKILL.md | wc -l` → **0**; control receipt `before-entailment-packet-greps.txt` agrees and shows the residual's carried wording at the base (r69 spotcheck line 92, r69 lesson lines 29/33).
- After: `git ls-tree --name-only b2f88ecc:corpus/evidence/round70/entailment-review | wc -l` → **6** (PROTOCOL.md, claims-scope.tsv, controls, fixtures, record-format-check.py, review-record.template.md).
- Checker sha pin: `git show b2f88ecc:…/record-format-check.py | sha256sum` → `7444fa3e29d4167c78e9b8e43e3cd8eefd70df2b6797f3aa8c41724feb09fbed` — matches the committed battery's `CHECKER_SHA256` and the digest-in-tree receipt.
- **Able-to-fail proof re-executed by me** (read-only `python -I`, after confirming all seven packet files' worktree sha256 equal HEAD blobs): valid fixture → `RECORD_FORMAT=2/2 REVIEW_FORMAT=PASS` rc=0; broken fixture → `RECORD_FORMAT=0/3 REVIEW_FORMAT=FAIL` rc=1 naming seven defects (verbatim identical to the committed battery output, all seven lines); absent record → `RECORD_FORMAT=ERROR REVIEW_FORMAT=ERROR record absent (fail-closed)` rc=2. All three arms reproduce exactly. This is the CORPUS "shown able to fail" red state, and it fails for the named reasons.
- Disclosure: `PROTOCOL.md` states verbatim "**The packet does not close the residual.**" and binds closure to a committed non-author review record; the reviewer is "a fresh non-author session … not dispatched by this lane's round author … scheduled by the operator". The review is requested on record (report, lesson `## Gate`). The claim's limits were frozen with the claim and the packet does not overstate itself. **C2 = improved, concurred** (the bar is now an executable protocol with a falsifiable checker where before there was carried prose); the residual itself stays open, as the round says everywhere it is relied on.

## 3. Axis table (closure verdicts — these grade the axes; the JSON verdicts map matches this table)

| axis | verdict | evidence |
|---|---|---|
| operability | **unchanged** (C1 honest-stop: the frozen completing-verdict-line predicate was not met; no improvement claimed or graded; the repair + red receipts land as the defect record and the routed residual) | §2 C1 |
| calibration | **improved** (C2: the residual's non-author bar is now a committed, runnable protocol with a checker shown able to fail; review requested on record; packet discloses it does not close the residual) | §2 C2 |
| depth | **unchanged** | all five SOURCES rows are own-work tier B records; no externally-grounded entry |
| freshness | **unchanged** | no drift surface measured; S168–S170 pinned to the base revision with `on-release` rechecks |
| coverage | **unchanged** | PROVINCE.md not in the round diff; repairs stay inside the lane's own gate/records ground |
| adjacency | **unchanged** | no sibling writes; the flock/python3/timeout findings are routed to the operator (L0), not absorbed as OS claims |

No axis is harmed: SCORECARD diff is additions-only (planned + verdict sections appended after line 3233; no prior row rewritten, no numeric change, no capability row), SOURCES.md is additions-only (+5), LOG.md append-only (+13), PROVINCE.md untouched.

## 4. Discernment spot-check (non-author)

The round's `## Gate` admits S168–S172 and records **0 post-open rejects** (search log: identified 5, screened 5, included 5, rejected 0 post-open, stop rationale given), so the contract's "≥1 reject" sample has no reject decision to sample; I sampled all five admits. Each quote re-opened at the named location:

| item | decision | re-opened source (command) | agree/disagree | reason |
|---|---|---|---|---|
| S168 admit (B, skip chain) | admit | `git show 1db6babf:.ufo/waves/round-69/preflight-final.txt` line 12 | **agree** | quote verbatim: `PREFLIGHT=7/7 FAILED=none ENV=none SKIPPED=G08`; the four-round skip chain is real (my own git grep agrees); narrow one-fact admission is the right scope |
| S169 admit (B, fail-closed contract) | admit | `git show 1db6babf:tools/research-gate.sh` lines 3970–3971 | **agree** | quote verbatim across the comment break (`…fails closed` / `# instead of appending unlocked.`); the designed fail-closed contract is exactly what constrains the repair to skip-wiring, and the landed repair conforms |
| S170 admit (B, skip pattern) | admit | `git show 1db6babf:tools/research-gate.sh` lines 7904–7905 | **agree** | quote verbatim; the repair's else-branches reuse this exact two-line pattern (seen in the diff) |
| S171 admit (B, recon failure shape) | admit, **quote location defect** (D-70-1) | `grep -n "line 5548" corpus/evidence/round70/controls/recon-run-r70.txt` and `before-g08-selftest-partial.txt` | **agree on the admission; disagree with the quote's attribution** | the quoted `dcCFup` crash line is NOT in the pinned `recon-run-r70.txt` (its crash lines carry tmpdir `K1Yhut` and the full scratch path, lines 66/74); the exact quoted bytes live in the sibling capture `before-g08-selftest-partial.txt`. Same crash site (`line 5548`, missing `r6-manifest.jsonl`), so the row's `teaches` (failure shape) is genuinely grounded and the admit stands; the location attribution is wrong |
| S172 admit (B, routed items) | admit | `grep -n "a full-run receipt remains owed" corpus/lessons/round-69-verifier-spotcheck.md` (line 91) | **agree** | quote verbatim, ≤25 words; this round closed exactly the two items it routes and routed the rest around, as the row claims |

New SOURCES.md row quote check: the S168/S169/S170/S172 quotes in `corpus/SOURCES.md` are verbatim at their named locations and ≤25 words; S171's row carries the same mis-attributed quote (D-70-1). SOURCES.md diff verified additions-only (exactly five rows; no held status/recheck/used-by cell changed). Census validate exit 0 (five pre-existing W04 warnings, identical to both committed census receipts).

No reject sample exists to check; nothing this round was admitted that I would reject. The S171 attribution slip is a precision defect, not a wrong gate call — the admitted record is real, correctly tiered, and correctly limited.

## 5. Routed defects (status-neutral; the lane must fix these next round)

- **D-70-1 (S171 quote attribution).** The S171 "verbatim" quote (lesson `## Gate` table + `corpus/SOURCES.md` S171 row) — `tools/research-gate.sh: line 5548: /tmp/chousa-research-gate-selftest.dcCFup/r6-manifest.jsonl: No such file or directory` — is present verbatim in `controls/before-g08-selftest-partial.txt`, not in the pinned `controls/recon-run-r70.txt`, whose crash lines (66/74) read `…scratch/chousa-r70/recon/research-gate.sh: line 5548: /tmp/chousa-research-gate-selftest.K1Yhut/…`. Same crash site, wrong capture named. Fix: a correction row (`supersedes S171 —`) or lesson erratum naming the right capture (or quoting the K1Yhut line verbatim).
- **D-70-2 (counting-command collision).** The report's and SCORECARD's no-verdict-line command, `grep -c "RESEARCH_GATE_SELFTEST:" after-battery-completes-r70.txt`, returns **1** over the committed bytes because the receipt's own header (line 4) quotes the frozen predicate string; claims.md's `grep -c "RESEARCH_GATE_SELFTEST: FAIL"` likewise returns 1. The honest-red fact is true — `grep -c "^RESEARCH_GATE_SELFTEST:"` → 0 and the transcript ends at case 257 with the RUN-END ADDENDUM — but the commands as written do not reproduce their stated values. Fix: anchor to `^` (or scope to the transcript section) in the correcting entry; never quote the predicate string inside a receipt whose counting command greps for it.
- **D-70-3 ("six skips" overstatement).** The report ("six skips by name"), SCORECARD verdict cell ("the six append-subject skips each print by name"), the battery receipt's RUN-END ADDENDUM, and the lesson's intake item 1 all say the six append-subject skips print — the committed transcript contains **five** of them (cases 60, 61, 134, 135, 234). The sixth (`all-manifest-hash-shim`) sits at case 259, after the ended-at case 258 (file order verified: locale cases at base 8289–8318, the hash-shim skip block inserted before the r36hashbin setup at 8328+), so it could not and did not print. The skip mechanism is proven by the five; the count is wrong. Fix: correcting entry stating five-of-six printed and why.
- **D-70-4 (the "/269" denominator).** "case 257/269" (report, lesson, ADDENDUM, commit subject) carries no counting command; the canonical committed total is 275 (SKILL registry row: `PASS (275 cases, 0 skipped)`). I could not re-derive 269 from committed bytes without executing the (unbounded) battery, so the denominator is unverifiable as written. Fix: state the denominator's derivation or replace with "case 257, run ended at case 258".
- **D-70-5 (SKILL registry row 83 contradicts its own cited receipt).** The row (landed b2043bf9, stands at HEAD b2f88ecc) says: on this host "the battery completes and prints `RESEARCH_GATE_SELFTEST: FAIL (k/N cases, 6 skipped)` rc=1", citing `after-battery-completes-r70.txt` — which shows the battery did NOT reach its verdict line. The row was written before the final measurement and the verdicts commit did not correct it; it is the one place the round's honest-stop outcome is not carried. Fix next round: correct the row to the measured state (runs truthfully through case 257, ended at case 258, no verdict line; honest-stop), per the corrections-sweep rule.
- **D-70-6 (no reject decision to sample).** The round's Gate rejected nothing post-open, so the admit+reject spot-check sampling is half-empty by the round's own record. Not charged as a defect — the search log's stop rationale is given and every opened row was honestly tiered — but a future round should let at least one rejection surface when one exists.

## 6. Trend verdicts (with evidence)

- **expansion: unchanged** — the round diff adds no `corpus/knowledge/` file, no PROVINCE.md change; the five SOURCES rows are own-work records inside ground the lane already holds (its own gates, receipts, and closure records). Matches the report.
- **quality: improved** — where four rounds of bare `SKIPPED=G08` receipts and a silent rc=2 death stood, there now stand: a full no-skip preflight receipt (red, honestly), a battery transcript truthful through case 257 with named skips and named FAIL-cases, and digest pins that re-derive (I recomputed all three). No admitted entry failed its re-check. The red is the improvement: the truth is measured and committed. Matches the report.
- **discernment: unchanged** — verdicts are receipt-and-control-derived; my spot-check agrees with all five sampled admits (one quote-attribution defect recorded, none of the admissions wrong); no reject decisions existed; the residual's judgment stays with the operator-scheduled non-author reviewer, and the entailment-review packet makes that review runnable when scheduled. Matches the report.

## 7. Notes for the operator

- All four SHONEN.md boxes still look checkable by a non-author promotion review (the r69 spot-check's note stands unchanged); that review and the entailment review (packet committed and runnable: `corpus/evidence/round70/entailment-review/PROTOCOL.md`) are both operator-schedulable now.
- Two L0 queue lines were filed this round (flock(1) install decision; the two historical bare `## Capabilities` headings) and are present at `.ufo/l0-questions.md` lines 241/244 in the fleet working tree — the integrator's commit of that file is the durability step (protocol-lane duty; not charged to this lane).
- The G08 residual is fully routed: operator flock decision (L0) + a bound for the unbounded locale-boundary case, both named for round 71 in the lesson's continuation section.
