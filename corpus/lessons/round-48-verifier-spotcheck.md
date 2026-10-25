# Round 48 verifier spot-check — chousa

author: hyaku closure (non-author integrator, @m_kfc)
date: 2026-10-25
lane round closed: 48 (report `.ufo/reports/round-48/chousa.md`, committed by lane identity `chousa-shokunin <chousa@shokunin.local>` at `7875ae0a3fef854ad4788058107b642e6edb4e46`)
lane HEAD measured: `73ea8110cea890188df4973b212f5441d4b19e89` (local=remote, ahead=0, behind=0)
base → head: `d4e6ef09b755a961bdae56566a7dcf0c9db0cfd7` → `73ea8110cea890188df4973b212f5441d4b19e89`
dispatch digest (`.ufo/watchdog.log`): `2026-10-25T10:17:46-03:00 launch chousa round=48 pgid=2365961 driver=hyaku-inline attempt=1`; `2026-10-25T11:22:48-03:00 complete chousa round=48; hyaku-inline attempt=1`

No live fetch was made for any ruling below (province rule; L0 `8d77e6c1` open). All quarantine and held-out rulings re-open committed local captures only.

## Step-1 conformance

| check | result |
|---|---|
| report committed by lane identity | OK — `git log --format='%an %ae' -- .ufo/reports/round-48/chousa.md` → `chousa-shokunin chousa@shokunin.local` |
| SHONEN heading, one line per box | OK — 4 `[~]` lines with pointers |
| cited commits exist + ancestor of `master` | OK — `4bbd2348…`, `671b096e…`, `73ea8110…` all pass `git merge-base --is-ancestor <hash> master` |
| pushed / clean lane state | pushed OK — `jj-lane.sh state` → `ahead=0 behind=0 local=remote=73ea8110…` |
| uncommitted round work | **DEFECT** — `git status --porcelain` shows 4 modified tracked files: `.ufo/waves/round-40/w1/swarm-registry.json` and `.ufo/waves/round-41/w1/swarm-registry.json` (mtime 2026-10-24, inherited, named in `LOG.md:1796`), `corpus/evidence/round41/receipts/cells/cells.json` (mtime 2026-10-25 06:36, pre-launch), and `corpus/QUALITY.md` (mtime **2026-10-25 11:17:47 -03:00, inside the round-48 window** — an uncommitted seat edit adding one Named-limit sentence citing R48 windows; not in commit `73ea8110`, not covered by the LOG "inherited" note). Status-neutral per closure rules; routed below. |
| dispatched prompt carries contract | OK — `.ufo/prompts/chousa-round-48.md` embeds report path, commit-before-report, SHONEN heading, hash-citation rule, write scope, L0 channel, frontier step, trend verdicts |
| round shape | two v1 waves, 32+32=64 seats ≥ L2 minimum; W1 lacked connector/scribe roles (appeared in W2) — lane-named conformance defect; W1 Attack04 died on `invalid_prompt`, not replaced. Both recorded here per step-1 duty. |
| stale-lane | launch→complete within one window, lane commits progressing; report addresses it. OK. |

## Per-claim re-check (C1 judged as the frozen composite: c1-count AND mutation-check)

**C1 operability — composite predicate RE-MEASURED on committed bytes** (evidence-verified where noted):

1. Freeze integrity — `git diff 4bbd2348… 73ea8110… -- corpus/evidence/round48/claims.md corpus/evidence/round48/controls/before.txt` → empty. Frozen predicate and before-control unchanged since the freeze commit; freeze (`4bbd2348`) is an ancestor of the code commit (`671b096e`). OK.
2. Before state — `git archive d4e6ef09… tools/inference-ground.py` extracted to a temp dir, run against the R48 counters: `REFINEMENT_CASES=5/5 CORRECT_BULLETS_PASS=9/12 PRECISION_GATE=FAIL LEGACY_R47=PASS C1=FAIL` — reproduces `controls/before.txt` exactly. OK.
3. After state — `git archive 671b096e…` full-tree extraction, `python3 corpus/evidence/round48/c1-count.py` → `CORRECT_BULLETS_PASS=12/12`, `MIN_CORRECT_PASS=11/12`, `PRECISION_GATE=PASS`, `LEGACY_R47=PASS`, `C1=PASS exit=0`; `python3 corpus/evidence/round48/mutation-check.py` → `MUTANTS_KILLED=5/5 exit=0`. Byte-identical to `measure-after.txt`. `sha256sum tools/inference-ground.py` = `fa2b4eb5…4658b6e` at `671b096e`, at `73ea8110`, and in `measure-after.txt` — all match. OK.
4. Shortcut control — re-ran `python3 corpus/evidence/round48/controls/name-key-control.py` from the live lane (its committed evidence says it runs there; temp-dir writes only): no-read name-keyed substitute passes the C1 component (`C1=PASS`) but `NAME_KEYED_MUTATION_CHECK=REJECTED` / `implicit-neg=MUTATION_NOT_APPLIED` → `COMPOSITE_CONTROL=REJECTED`. OK — composite as frozen; the report's bounded claim ("rejects the tested shortcut, not every possible substitute") is honestly stated.
5. C2 registry — re-ran `python3 corpus/evidence/round47/c2-count.py --list` on the archived tree: `REGISTERED=97/97 MISMATCHES=0 C2=PASS` (GATES_ROWS 51→52 with the R48 rows). Matches report. OK.
6. R39/R40 receipts — evidence-verified only (lane-owned verifier; not executed per §Gate standard closure consequence): `receipt-recheck.txt` shows `PINNED_ADDING_COMMITS=6/6` at `d164f88`/`6d914e9` and tip `2/6` with four `gate-sha256-mismatch` bindings to pre-`1bd9001` gate sha `4253c187…`; internally consistent, no receipt bytes touched. OK.
7. Owned axes — `git diff d4e6ef09… 73ea8110… -- SCORECARD.md` is additive and keeps the operability scale at 3/10 with an explicit "no other expertise score is invented" line; per-axis table marks calibration/depth/coverage/freshness/adjacency unchanged; SKILL.md registry rows updated consistently with the new windows; LOG.md entry `1786-1796` ties every landed change to its commit and routes both open disputes to this closure. No owned axis harmed.

**Claim verdict: verifies as frozen composite.** Re-measured: precision/refinement/legacy/mutation legs, C2 registry, name-key control, freeze integrity, tool digest. Evidence-verified: R39/R40 receipt recheck.

## Ruling (a) — HeldOutA item a05 label truth

Re-opened committed bytes: fixture span `corpus/fixtures/inference-ground-r47/spans/S902-1.txt` = "the archived copy is dated at build time; a placeholder value is not an archive link"; a05 bullet body = "that date is not the copy's build date"; full context in `.ufo/waves/round-47/w2/HeldOutA.md:24,34`, the r47 acceptance in `corpus/lessons/round-47-verifier-spotcheck.md:29`, the W2 dispute in `.ufo/waves/round-48/w2/AttackPrecision.md:47,50`.

**Ruling: the a05 "correctly-reasoned" label is FALSE on the plain reading, and the r47 non-author closure's acceptance of it was an error of charity.** The bullet quotes the affirmed phrase "the archived copy is dated at build" and then asserts "that date is not the copy's build date" — a direct denial of the quoted phrase. HeldOutA's defense ("the negator's scope is its second date, not the established build date") imports a second-date antecedent that the fixture does not establish: "that date" can only resolve to the date in the quoted phrase. W2's plain reading is correct; the label "holds only on the charitable reading" (`AttackPrecision.md:47`) and charity is not evidence.

Consequences (none reverses the axis move):
- The R47 tool's true false-refusal count on this set is **2/12 (p03, p04)**, matching HeldOutA's own headline; the propagated "exit-level 3/12 incl. a05" figure (`round-47-verifier-spotcheck.md:29`, quoted into the r48 lesson's S095 Gate block) overcounts the defect class by one.
- The R48 tool passes a05 because P2's window narrowed (3-before → 2-before; committed diff at `671b096e`): a negator 3 words before the affirmed stem no longer fires. That "fix" accepts a bullet that plainly denies the affirmed phrase — a new, unmeasured false-negative class the frozen set does not count.
- On the verified-correct subset the move still measures 9/11 → 11/11 with p03/p04 (genuine false refusals by every account) repaired, and the tool still kills all five named mutant classes, legacy junk, and both do-nothing controls. C1 stays admitted as frozen; the claim's own "improved narrowly / no general-precision claim" framing is the right cap and is kept.

## Ruling (b) — S093 quarantine verdict disagreement

Re-opened committed captures only (`.qcache` under the read-only register root; register sha256 `5afe1810…` verified; capture sha256 `2f8047a8…` verified): `.ufo/waves/round-48/w2/QuarantineS093.md` (present), `.ufo/waves/round-48/w1/Attack24.md` (absent verbatim, substance fully grounded), `.ufo/waves/round-47/w1/QuarReg093.md` (present), register row `absent-defect-register.md:43`.

**Independent check:** verbatim and whitespace-fold both miss (reproduces the mechanical `payload-absent`); word-order alignment finds every one of the 26 staged-quote words verbatim and in order, the only inter-word injections being the enumerator `(2)` (elided by the staged quote without ellipsis) and the pdftotext-interleaved figure label `Cited source` — identical structure to the r47 and w2 alignments.

**Ruling: S093 = present (as-substance); the L1 Gate table stands.** Under the lane's own stated convention in the same table — S094 "present after deinterleaving columns and joining line-wraps", S108 "extractor changes spacing", S110/S116 "−layout interleaves columns" — a quote whose every word occurs verbatim, in order, with only layout interleaves between, is present. Attack24's "absent (verbatim)" records a true byte property but mis-classifies the row under that convention, and its own "substance: fully grounded — not a fabrication" concedes the material point. The register's reason string ("the quote is in none of them") is falsified for the payload. Caveats kept as quote-hygiene corrections, not verdict changes: the staged quote elides `(2)` without an ellipsis and the register cell truncates mid-word (`are un`); cite the contiguous anchors @1526/@1576/@1669 instead. Gate tally 16 present / 8 absent-as-written / 0 unverifiable confirmed.

## Discernment spot-check table

| item | lane decision | re-opened source | agree? | reason |
|---|---|---|---|---|
| S093 (quarantine, disputed) | present — disputed | capture `4132ec1b….txt` (sha `2f8047a8…`), register row 43, staged quote via `quote-lint-full-v5.json` | **agree (present)** | all 26 words verbatim in order; only `(2)` elision + `Cited source` interleave; not fabrication; see ruling (b) |
| S096 (quarantine) | absent-as-written (q2 present; q1/q3 spliced/ISO-for-GB/T) | capture `6dc68fd6….raw` UTF-16LE, 129,024 bytes | **agree** | q2 hits at byte 3232; q1 and q3 absent under every fold; substance grounded, no fabrication — matches per-quote split |
| S114 (quarantine) | present | capture `42bac883….raw` 20,142 B (payload; `.txt` is comment-stripped) | **agree** | both quotes verbatim inside the single HTML comment (chars 9192–9908) after tag+whitespace fold; the row is payload-true but render-hidden — the seat's caveat is correct |
| S095 (new SOURCES row, own-work admit) | admit, tier-A mined | `corpus/lessons/round-47-verifier-spotcheck.md` §2 line 29 and §6 line 62 | **agree as quotes** | quote 1 = 15 words, quote 2 = 13 words (≤25), both verbatim with the stated ellipsis boundary; **but** quote 1 propagates the a05 mislabel — the row itself is admissible, the quoted figure is not; see ruling (a) |
| C1 admit/reject (claim gate) | frozen composite, admitted by L1 pending closure | `claims.md`, `measure-after.txt`, counters re-run over `git archive` of `671b096e` | **agree** | composite legs reproduce on committed bytes; admission-rule deferral to external verification exercised in ruling (a); claim admitted with caps |

Census: `scripts/sources-census.sh validate --root … chousa` → exit 0, `ok`, the same five pre-existing W04 warnings (S051/S053/S073/S074/S075) as round start. Registry rows: 94 → 95 (re-counted: start `git show d4e6ef09:corpus/SOURCES.md | grep -cE …` → 94; end → 95), tiers A=89 B=1 C=5, statuses mined=71 queued=19 rejected=5, 0 malformed — matches the report's table.

## Trend verdicts (closure, non-author)

- **expansion — unchanged.** One own-work curation row (S095); no knowledge entry on uncovered ground; frontier rows advanced: none.
- **quality — unchanged.** No knowledge entry re-admitted, deepened, or failing; measured change is the operability tool + counters on a recycled set.
- **discernment — unchanged.** My outside re-open of 3 quarantine rows + 1 own-work row agrees with the lane's gate outcomes (S093 dispute resolved in the lane's favor on its own convention; S096/S114 upheld). The a05 label error is round-47-authored and was surfaced, not buried, by the lane's own W2 seat — good calibration practice, but no new knowledge admission to grade improved.

## Routed defects (lane must fix next round)

1. **a05 mislabel correction (append-only, per Evidence standard):** a named correction entry in `corpus/lessons/round-47-verifier-spotcheck.md` or the round-49 lesson superseding "exit-level 3/12 incl. a05, an over-refusal" — true figure 2/12 (p03, p04); a05's refusal was correct. Sweep every mention: r48 lesson S095 Gate block (its quote is verbatim but the quoted claim is wrong — add the correction beside it), QUALITY criterion 69's framing, and any SCORECARD wording that reads 3/12 as false refusals.
2. **Name the P2 narrowing cost:** the r48 tool accepts a bullet that plainly denies the affirmed phrase whenever the negator sits 3 words before the stem (a05 is the live example). Document in QUALITY/the lesson that this false-negative class is unmeasured by the frozen set; if a future round wants the class counted, add a fixture.
3. **Uncommitted working-copy edit:** `corpus/QUALITY.md` carries an in-round-window seat edit (mtime 2026-10-25 11:17:47 -03:00) that never landed in `73ea8110`; the three inherited R40/R41 leftovers (swarm-registry ×2, cells.json) also remain. Resolve under the next round's entry (commit or revert) per the landed-means-committed rule; the LOG "inherited" note currently covers only three of the four paths.
4. **S093 quote hygiene (already seat-flagged, keep visible):** staged quote elides `(2)` without an ellipsis; register cell truncates mid-word; reuse anchors @1526/@1576/@1669.
5. **W1 role-split floor:** W1 of 32 seats shipped without connector/scribe roles (W2 had both); the lane named it — record stands, no repeat next round.
6. **For the operator (promotion-adjacent, non-blocking):** all four SHONEN boxes are `[~]` author assertions this round; the report's boxes 1–4 are fully checkable by a non-author (decision tables + QUALITY 69–70 with resolvable pointers; end-to-end task logged with counters; self-contained tools; SiblingFit no-overlap) — a promotion reviewer can convert them without new evidence gathering.

## Admission

Every declared claim verifies (composite re-measured on committed bytes; gate evidence verified, none executed on live surfaces); no owned axis is harmed; the two closure-assigned disputes are ruled (a05 label false as stated — capped, not blocking; S093 present). Conformance defects (uncommitted QUALITY.md edit, W1 role split, dead Attack04, stale inherited leftovers) are status-neutral and routed. **Admitted.**
