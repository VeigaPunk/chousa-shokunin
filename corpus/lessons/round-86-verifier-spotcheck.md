# chousa round-86 verifier spot-check — non-author closure review

author: hyaku closure (non-author integrator, @m_zfl)

## Step-1 conformance

- **Report committed in the fleet repo by the lane identity.** `git log --format='%an %H' -- .ufo/reports/round-86/chousa.md` → `chousa-shokunin 2614965dcbf308ac374a3a244171a7ad045e7589`. Not a marker: it carries work performed with evidence pointers, a Landed changes table (8 commits, each with LOG bullet and hash), per-claim before→after with counting commands, Sources & frontier, trend verdicts and the SHONEN heading.
- **SHONEN heading.** Present at report line 153, one line per box, 4 boxes, all `[~]` with evidence pointers; no `[x]`, no non-author verifier named (lane assertion only). No promotion claim; `SHONEN.md` untouched.
- **Cited lane commits exist and are ancestors of master.** `git merge-base --is-ancestor <h> master` for `e4468752`, `d0b1bd06`, `667a5d09`, `a9bed303`, `95f0fc44`, `c59391a1`, `16ba033b`, `0cbbeb66`, `43c3f728` → all ancestor-OK. Tested against `master`, never `@{u}` (HEAD detached).
- **Base and after hashes.** Base `3bfb6885958ad4a674ad1896f70d1e836be609e4` exists; after `0cbbeb665bac00c27274f9b3560b37c9783f3f73` is lane HEAD.
- **No uncommitted round work; pushed.** `scripts/hyaku/jj-lane.sh state chousa-shokunin` → `branch=master local=0cbbeb665bac00c27274f9b3560b37c9783f3f73 remote=0cbbeb665bac00c27274f9b3560b37c9783f3f73 ahead=0 behind=0 head=detached tracked=0 untracked=0`; `git -C chousa-shokunin status --porcelain` → empty (output showed an empty list). All 8 cited commits form a linear chain `e4468752 → d0b1bd06 → 667a5d09 → a9bed303 → 95f0fc44 → c59391a1 → 16ba033b → 0cbbeb66`; nothing stranded.
- **Prompt fidelity.** `.ufo/prompts/chousa-round-86.md` is the canonical template rendering (989 lines, hyaku addendum §6 included, run-15 through run-7 directives present). It carries MISSION/AXES binding (§1), 1–3 falsifiable claims with lowest-axis rule (§2), frontier step (§2b), L2 floor of ≥8 in one batched swarm with role split (§3), and the report contract with SHONEN one-line-per-box, marker rule, commit-then-push ordering, push scope and L0 side channel (§4), plus the campaign addendum (§6). §8 pre-file falsification ledger requirement present.
- **Dispatch digest (copied from the closure prompt; `.ufo/watchdog.log` is mutable):** `2026-11-08T02:57:28-03:00 launch chousa round=86 pgid=144445 driver=hyaku-inline attempt=1` / `2026-11-08T03:38:55-03:00 complete chousa round=86; hyaku-inline attempt=1`.
- **Prefile falsification.** `python3 scripts/hyaku/prefile-falsification.py --lane chousa --round 86` → `PREFILE-FALSIFICATION: pass claims=2 rows=12 attack_seats=6 findings=0`, exit 0. Rows cover both claims; zero `falsifies-wording` rows.
- **Wave evidence.** `chousa-shokunin/.ufo/waves/round-86/w1-results.json` and 12 seat directories (`R86ConnectorSiblings`, `R86CriticClaims`, `R86ExecBase`, `R86ExecForge`, `R86ExecHarm`, `R86ExecRepro`, `R86MutCounter`, `R86RevSupply`, …) are committed at `16ba033b`. Report states 12 seats (4 executor, 2 reviewer, 1 critic, 1 mutation-tester, 1 revenger, 1 scout, 1 connector, 1 scribe), 0 dead, attack share 7/12 by ledger role set (6/12 by the gate's ATTACK_ROLES), both above the 25% floor.

## Claims — re-derived by the non-author (nothing here is quoted from the report)

### C1 operability (capability acquisition + repair) — VERIFIED

I re-ran the frozen `gate-records-r86.py` on a fresh `git archive` of the landing tree at `0cbbeb66`:

- Command: `git archive 0cbbeb665bac00c27274f9b3560b37c9783f3f73 | tar -x -C $S && python3 -B $S/corpus/evidence/round86/gate-records-r86.py --root $S --repo <lane> --work $S`
- Observed: `TOOL=present POSITIVE=15/15 FRESH_POSITIVE=5/5 FORGED_REFUSED=355/355 EXPECTED_CODE=355/355 EMPTY_REFUSED=1/1 RC=4/4 SETUP=1/1 D1_FORGES=1 D1_REFUSED=1/1 MUT17_KILLED=1/1` / `GATE_RECORDS_R86=PASS`, exit 0. Matches the report's after-row byte-for-byte.

Committed controls (not re-executed — I verify their bytes, PROTOCOL §Gate standard):
- `c2-d0-donothing.txt` shows the C2 base: `SUPERSEDED_LIVE=1 UNENTAILED_TERM=2 MODIFIED_DEF_CITED=0 QUOTES_LOCATED=19/19` / `CURATION_R86=FAIL`, exit 1.
- `c1-k0-donothing.txt` header names the command, the base tree `3bfb6885`, and the pre-round-85 tool `43c3f728` with the `2xx` rule; body lines show `WRONG_CODE … expected=PARSE got=REFETCH` and the `D1_REFUSED=0/1 MUT17_KILLED=0/1` before-state. The routed defect 2 closure (receipt names command + tree + instrument bytes pinned in `instrument-pins.txt`) is confirmed by the receipt headers.
- Frozen instruments re-verified: `sha256sum` of `gate-records-r86.py`, `curation-r86.py`, `c2-positives.tsv` and `tools/gate-records.py` match `instrument-pins.txt`.
- Lane-owned gate evidence (not re-executed): the wave seats `R86ExecRepro`/`R86ExecBase` reproduce both sides, `R86ExecHarm` shows no genuine committed record moving across 449 records, `R86ExecForge` finds no in-class admit accepted. The `tools/research-gate.sh --selftest` PASS (283 cases, 0 skipped) and preflight `PREFLIGHT=8/8` are evidence-verified from `0cbbeb66`'s measurement logs, not re-run by me.

K1–K4: K1 holds (predicate met at landing); K2 holds (355/355 refused with expected codes); K3 holds (harm gate pass, evidence-verified); K4 holds (mutant derived from subject tool bytes, `MUT17_KILLED=1/1`, no post-scoring rescue — the freeze predates landing).

### C2 calibration — VERIFIED on the narrowed property (Amendment 11)

I re-ran the frozen `curation-r86.py` on a fresh `git archive` of the landing tree at `0cbbeb66`:

- Command: `git archive 0cbbeb665bac00c27274f9b3560b37c9783f3f73 | tar -x -C $S2 && python3 -B $S2/corpus/evidence/round86/curation-r86.py --root $S2`
- Observed: `SUPERSEDED_LIVE=0 UNENTAILED_TERM=0 MODIFIED_DEF_CITED=1 QUOTES_LOCATED=20/20` / `CURATION_R86=PASS`, exit 0. Matches the report's after-row.

Committed base control: `c2-d0-donothing.txt` prints the before-row exactly (`SUPERSEDED_LIVE=1 UNENTAILED_TERM=2 MODIFIED_DEF_CITED=0 QUOTES_LOCATED=19/19` / FAIL, exit 1) with command and tree named — evidence-verified, not re-executed.

**Amendment 11 adjudication.** The published predicate's `total ≥ 19` floor was never implemented in the counter (`R86ReviewerEntry` §2.3, `R86CriticClaims` V4), and `MODIFIED_DEF_CITED` is a presence test, not warrant linkage (`R86ReviewerEntry` §2.4). The lane withdrew the floor as a conjunct, kept the four enforced fields, and moved class closure of the imported-distinction defect to review. I find the narrowing legitimate: the wave falsified the stated wording, the amendment names both artifacts, the narrowed property is what the instrument enforces, and the measured total at landing is 20/20 (the floor's intent holds on the bytes though it is not an enforced conjunct). C2 therefore verifies on the narrowed property, not the originally published predicate.

**Review-verification of the moved items (my own reading):**
- The S024/S031 inversion is closed: `S031` is `mined`, `used-by` → `corpus/knowledge/provenance-recording-r85.md`, anchor restored to base bytes; `S024` is `queued`, `used-by —`, `opened 2026-10-21`, anchor restored. The `git diff 3bfb6885..0cbbeb66 -- corpus/SOURCES.md` shows exactly these two cell changes (plus S216/S217 additions).
- r84 row 9 now warrants `Q13` (S023) in its decision-table Warrant cell. Its Do says "state the date on which the resource was changed" and its Never "record that the resource changed without the date on which it changed" — both are entailed by Q13's located quote "Date on which the resource was changed." (S023 capture line 8786, verified below).
- r85 row 6 now warrants `Q7 (S031)`. Its Never states "record a review date for content that was not reviewed for accuracy or completeness" — entailed by Q7's quote "Date on which the content on this web page was last reviewed for accuracy and/or completeness." (S031 capture verbatim). The refused comparison to modification dates is gone from the cell.
- Entry-wide counts at landing: `modification`/`modified` in `search-transparency-reporting-r84.md` = 1 occurrence (the word `modified` in the Limits list, not in a decision-table cell); in `provenance-recording-r85.md` = 0. The moved class closure holds on reading.
- K2 holds: every counted quote is verbatim in the capture of its registry row's URL (I verified the three below). K3 holds on my reading (both repaired rows state only what their warrants state). K4 holds: the r84 repair cites S023, the r85 entry cites S031, not S024.

**Residuals already routed by the lane (not re-routed):** D1 is one record wide (three qualifying rows S021/S032/S022 instantiate the class; `R86CriticClaims` T4); the mutant-derivation and SETUP duties are fields, not verdict conjuncts (`R86MutCounter` M2/M5); a `decision=reject` 203 record is accepted (`R86ExecForge` F1); C2's floor and warrant linkage are unimplemented (`R86ReviewerEntry` E5/E6). All are in plan Amendment 12 / the SCORECARD round-87 plan. I do not re-route them.

## Per-axis verdicts

| Axis | Verdict | Evidence |
|---|---|---|
| operability | improved | C1 re-measured: battery generates the D1 (200-only) class from committed bytes inside the predicate, derives M17 from the subject tool's own bytes, kills it (`MUT17_KILLED=1/1`), 355/355 forgeries refused with expected codes, no harm over 449 records. The battery's coverage defect is now load-bearing, not beside the verdict. |
| calibration | improved | C2 re-measured on the narrowed property: S024/S031 inversion closed, both imported-distinction cells repaired to state only what their located warrants state, stale r85 "verified" column retracted (routed defect 4), control receipts name command + tree + pinned instrument bytes (routed defect 2). Five criteria mined (QUALITY 177–181), four from this round's own wave findings. |
| depth | unchanged | No new knowledge entry (97 → 97, verified by `git ls-tree` counts at both revisions); the one candidate source S217 was refused on content and recorded `rejected`. |
| coverage | unchanged | `PROVINCE.md` untouched; registry 215 → 217 rows (verified: base count from `git show 3bfb6885:corpus/SOURCES.md`, landing count from the current file; census exit 0). |
| freshness | unchanged | Four URLs re-opened 2026-11-08T06:00:10–11Z, all HTTP 200 per egress table and refetch rows; S023 capture bytes confirmed unchanged at base and landing (lesson correction 1 discloses the account error without disturbing the conclusion). |
| adjacency | unchanged | `R86ConnectorSiblings` reconfirms the kotodama `check-gate-captures.py` false-green read-only; no sibling holds RFC 9110 203 semantics; cross-lane defect 5 stays routed. |

No axis is harmed. `git -C chousa-shokunin diff 3bfb6885..0cbbeb66 -- SCORECARD.md` shows the round-86 verdict appended with the table above matching; the only changed existing file is SCORECARD.md appended in place, consistent with the SCORECARD contract.

## Spot-check table (Discernment, LEARNING.md)

The round's `## Gate` admits S216 (new, tier A, mined) and S031 (queued→mined), and rejects S217 (new, rejected). I sample one admit (S216) and the one reject (S217), plus S023's re-open record line and the S024 restoration.

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S216 admit | admit | `corpus/captures/b1b13a12aee75c6ecc20fb91.txt` §15.3.4, lines 12266–12272 | agree | The capture states: "The 203 (Non-Authoritative Information) status code indicates that the request was successful but the enclosed content has been modified from that of the origin server's 200 (OK) response by a transforming proxy." The 19-word quote in the lesson is verbatim in the capture; §15.3.4 is the correct anchor for 203 semantics; `teaches` is grounded. |
| S217 reject | reject | `corpus/captures/52db06f9e0e2eaf35bbdb321.txt` (9 lines) | agree | The capture is a 9-line stub (blank lines + the redirect-target URL) with no policy prose. No ≤25-word quote can ground a registry row; the rejection carries reason and flip condition per CORPUS.md. |
| S023 re-open record | admit (re-open) | `corpus/captures/f5545a194c06ab421875b047.txt` line 8786 | agree | Quote "Date on which the resource was changed." is verbatim at the cited line; the record line verifies against the committed capture. The lesson's own correction 1 discloses that the account of how the bytes got there (key vs content sha) was false while the substantive conclusion (Q13 at line 8786) stands — an honest disagreement record, which strengthens discernment. |
| S024 restoration | restore to queued | `corpus/SOURCES.md` diff at base vs landing | agree | The row returns to its pre-round-85 state (`queued`, `used-by —`, `opened 2026-10-21`, base anchor). The restoration touched two rule-2-immutable cells (`opened`, `anchor`) — disclosed old→new in the lesson and named as QUALITY 177 — but the row must return to `queued` for the inversion to close, and the disclosure makes the deviation checkable. |

Census validation: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` → exit 0, five pre-existing `W04` duplicate-URL warnings (S051, S053, S073, S074, S075) — the same five named in the report's frontier section, none introduced by this round.

## Trends

| trend | verdict | evidence |
|---|---|---|
| expansion | unchanged | `corpus/knowledge/*.md` 97 → 97 (verified by `git ls-tree -r --name-only` counts at base and landing); registry gained one mined tier-A standards row (S216) and one refused row (S217) — curation, not new held ground. Stated honestly in the report. |
| quality | improved | Battery's zero-forgery class is now a verdict conjunct with its mutant killed by computed bytes; two entry warrants repaired and located (Q13 at S023:8786, Q7 at S031 verbatim); five criteria mined (QUALITY 177–181), four from this round's own findings; three registry/lesson deviations (S031 anchor, S217 cell, S023 capture-identity account) reverted or corrected in the integration commits. |
| discernment | improved | The wave falsified the published C2 predicate on two clauses (floor never implemented, warrant linkage unimplemented) and the lane narrowed the claim instead of filing it; published its own three narrative/registry deviations; the one review that disagreed with the landed text (capture identity) is recorded as a correction, not defended. The non-author spot-check above agrees with the gate on all four sampled decisions. |

## Routed defects (for the lane to fix next round)

None new. The lane's own routed residuals I endorse and carry into the notes:
1. D1 one record wide — round 87 must build D1 from every qualifying committed 203 row (S021, S032, S022) and require `D1_REFUSED=N/N` (`R86CriticClaims` T4).
2. Mutant-derivation and SETUP duties are printed fields, not verdict conjuncts (`R86MutCounter` M2/M5) — add a leg that fails when its own duty is dropped.
3. A `decision=reject` 203 record is accepted (`R86ExecForge` F1) — the battery should cover the rejection form or name it out of class.
4. C2's `QUOTES_LOCATED` needs an implemented floor and a warrant-linkage leg (Amendment 11 routed items) so the class closure is counted, not review-verified.
5. `S024`'s frozen `teaches` still asserts the comparison its superseder refuses (QUALITY 178) — a future curation check should read registry `teaches` cells against captures, not only entry cells.

## Conformance defects (status-neutral, named)

1. The report's census "Start" run happened after the landing commit, not before it (disclosed in the report itself: "Process note: the first census run of this round happened after the landing commit, not before it; the base row count is derived from `git show 3bfb6885:corpus/SOURCES.md`"). The base count re-derives; the defect is procedural, not substantive.
2. The dispatched prompt (§6 addendum) contains an unbalanced truncation in the run-15 quote ("using the…" at line 143) — the template rendering is byte-faithful to the template, so this is a template defect, not a dispatch defect; named for the operator.
3. `corpus/README.md` frontier text still ends at round 6 (carried defect named in the report, not claimed fixed). `merge/chousa/` and `considerthese/` were not assimilated; the report says so plainly.

All three stay in notes; none bars admission.
