# R51ScoutConsiderthese — considerthese assimilation (lane tip `cfe6c9f`, read-only)

Read: all seven `considerthese/2026-10-19.md … 2026-10-25.md` (417 lines; `wc -l`). Lane mining record: `corpus/QUALITY.md` criteria 60/61/62/64/68/71 cite considerthese; `corpus/lessons/round-50.md:159-161` (`## considerthese`) says "Nothing left to mine"; `grep -rn considerthese corpus/lessons LOG.md` hits round-24 (M-7), 44, 47, 48, 49, 50 and LOG.md:1526,1553,1623,1688,1781,1805. I ran nothing that writes; one read-only counter run (below).

## Proposal ledger (every item in `Self-improvement proposals`, `Waiting on you`, "things João may want to know")

Legend: IMPL = implemented at path:line; FMT = reflection-format only (names no lane artefact); OPEN.

| File | Proposal | Status | Evidence |
|---|---|---|---|
| 10-19 | Verify gate numbers independently (selftest/--drift) | IMPL | QUALITY 15 (`:77`), 42 (`:321`), 68 (`:664`); `corpus/evidence/round40/c1-count.py` |
| 10-19 | Track hardening-r10 ledger / audit queue / A-r9.md:50 | IMPL | QUALITY 16 (`:86`); `corpus/evidence/round25-ledger-recount.py` (exists) |
| 10-19 | Calibration nudges: saturation line, capabilities rows | IMPL | `SCORECARD.md:469-473` (line 8.0 declared), `SCORECARD.md:461` `## Capabilities` |
| 10-19 | Watch SKILL.md size (~420 lines), distil prose | OPEN, unactioned | `wc -l SKILL.md` = 733; no QUALITY criterion/check names size or distillation |
| 10-20 | Hold myself to QUALITY 9, 10 | FMT | reflection's own hygiene |
| 10-20 | Review from a cursor | FMT (done: `cursor:` lines) | 10-23 onward end with `cursor: <sha>` |
| 10-20 | Second verifier for SOURCES rows | IMPL | `tools/quote-reopen.py` (exists); QUALITY 25 (`:169`) |
| 10-20 | Track round-25 debt queue | IMPL | QUALITY 16, round25 ledger recount, LOG.md round-25 closure |
| 10-20 | Recheck calendar (`90d`/`365d`/`on-release`) | IMPL | `SKILL.md:544` `--as-of`; `corpus/knowledge/recheck-due-r26.md`; `corpus/evidence/round26-claims.md` Claim 2 |
| 10-20 | Ask: append erratum to old file | FMT | permission question to the operator, not a lane artefact |
| 10-21 | Score round 26 against pre-registration | IMPL | `corpus/evidence/round26-claims.md` exists; round-27 lesson; 10-22 notes outcome |
| 10-21 | Run QUALITY 15 myself | IMPL (dropped by 10-22) | round-27 verifier did it |
| 10-21 | Flag same-file restatements | IMPL | QUALITY 9 (`:33`), 74 (`:772`) |
| 10-21 | Use support states in summaries | IMPL | QUALITY 8 (`:~29`) four support states |
| 10-21 | Resource bounds as coverage axis | IMPL | QUALITY 18 (`:104`) "A bound names its unit" |
| 10-22 | "Waiting on João" line | FMT (lane-side OPEN, see pick) | |
| 10-22 | Admission streaks, seats, wall time, cost per gain | OPEN, out of province | seats/wall time/dispatch are kumitate's (`PROVINCE.md` Refuses: "orchestration, multi-agent dispatch and agent lifecycle (→ kumitate)"); no `grep -n -i -E 'cost per gain|wall time|admission streak' corpus/QUALITY.md SCORECARD.md` hit |
| 10-22 | Prose regex / stale-claim scan on new text | IMPL | QUALITY 23 (`:152`), 74 (`:772`) |
| 10-22 | Read the verifier first | FMT | QUALITY 14 (`:69`) intake already requires it |
| 10-23 | Ask "cheapest gate" per counter | IMPL | QUALITY 60 (`:526`) |
| 10-23 | Handle large windows (300-file page) | FMT | `grep -rn -i -E 'listed, not read|300-file' corpus/QUALITY.md corpus/lessons` → no output (not a lane artefact) |
| 10-23 | Flag self-built controls | IMPL (stricter) | QUALITY 44 (`:336`): held-seat controls are never re-authored |
| 10-23 | `cursor:` fixed line | FMT, done by author | |
| 10-24 | Tag round ground/plumbing | IMPL | QUALITY 64 (`:583`), `corpus/evidence/round45/tag-count.py` |
| 10-24 | Track undispatched waves | IMPL | QUALITY 61 (`:542`), 63 (`:568`), 75 (`:788`) |
| 10-24 | Count errata per round | IMPL | QUALITY 62 (`:556`), `corpus/evidence/round44/errata-count.py` |
| 10-24 | Spot re-verify one receipt weekly | IMPL (local leg); cloud-agent leg refused | QUALITY 68 (`:664`); `lessons/round-48.md:73` refuses the cloud leg pending operator approval + L0 `8d77e6c1` |
| 10-25 | Retire two earlier ideas (tags, undispatched) | FMT | already QUALITY 64, 61 |
| 10-25 | "Waiting on you" box with open-round age | FMT in the reflection; **OPEN as a lane artefact** | no `OPEN_ITEMS`/`open operator` hit: `grep -rn -E 'open operator items|OPEN_ITEMS' corpus tools SKILL.md` → no output; `ls corpus/evidence/round51 \| grep -i -E 'open\|age\|waiting'` → no output |
| 10-25 | Capture-age line | IMPL | QUALITY 71 (`:725`), `corpus/evidence/round49/capture-age-check.py` |
| 10-25 | Adjust to the pace (lead with spot-checks) | FMT | |

Waiting-on-you items (operator-owned, tracked here as open at tip):

| Item | State at tip `cfe6c9f` |
|---|---|
| Round-47 polarity ruling (2/12 false refusals: strictness or harm) | still open: `SCORECARD.md:2513` "improved, disputed as a trade"; no ruling recorded |
| Fetch-scope `8d77e6c1` | open; lesson files citing it span rounds 29,30,31,32,41-50 (`grep -l 8d77e6c1 corpus/lessons/round-*.md`) — rounds 33-40 are absent from that grep, so a lessons-grep age (22 rounds since 29) is NOT reliable; age needs the LOG/SCORECARD text too |
| Four round-39/40 receipts failing `gate-sha256-mismatch` | still failing at tip: `python3 corpus/evidence/round40/c1-count.py` printed `corpus/evidence/round39/receipts/c2-after-s39101.json: fail VERIFY-FAIL: gate-sha256-mismatch`, `…s39121.json …` and `R39_ACTIVE_RECEIPTS=2/6` (read-only run, last 3 lines kept). LOG.md:1781-1784 and QUALITY 68 classify it as routed, not a defect; round 48 listed it as a candidate |
| L0 `chousa | round-43` / `round-44` unanswered | `LOG.md:1784` |

## The one pick (still-open, in province)

**"Open each reflection with a short 'waiting on you' box … with how many rounds each has been open"** (`considerthese/2026-10-25.md`, Self-improvement proposals bullet 2; same shape as `2026-10-22.md` "Waiting on João" bullet), mapped to the lane's own round report, not to the reflection.

Why it fits: PROVINCE owns "this lane's own corpus and gates" and calibration is a judged axis. It is the only open proposal that names a checkable lane artefact and is not orchestration. Four operator items have been open for 7–22 rounds and the lane restates them as prose each round ("L0 `8d77e6c1` open") without a count; QUALITY 71 fixed the same disease for freshness (a repeated "unchanged" hiding a cost). Not picked: SKILL.md size (10-19; no agreed threshold), cost per gain (kumitate province), cloud-agent re-verify (needs operator approval).

Spec (lane artefact, for the L1 to author; I did not create it): a round report line

`Open operator items: <id> since round <N> (<k> rounds); …`

derived by a check, not typed. Pitfall found above: a `corpus/lessons` grep misses rounds 33–40 for `8d77e6c1`, so the checker must scan LOG.md/SCORECARD.md and take the first-citing round.

Check command that would show it implemented (does not exist today; analogue of `capture-age-check.py`):

```
python3 corpus/evidence/round51/open-items-age.py <round-51 report>
# exit 0 + OPEN_ITEMS_AGE=PASS when the report has one line naming 8d77e6c1 with a since-round integer matching LOG.md/SCORECARD.md first citation; exit 1 FAIL otherwise
# shown able to fail: run against round-50's report -> FAIL (no such line)
```

Absence now: `ls /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round51/` lists build-spans.py, c1/c2/c3-count.py, census-start.txt, claims*.md, controls, quote-substance-check.py — no open-items file.

Caveat: the flip-condition for the operator items themselves is operator action; the pick only makes the age visible, it closes none of them.

VERDICT: swept all seven considerthese files (31 proposals, counted by a script over the table: 19 implemented, 9 reflection-format only, 3 open = SKILL.md size, cost-per-gain [out of province], lane-side waiting-on-you age) plus 4 waiting items; picked one (open-operator-items age line in the round report) with an absent-today check; the four-receipt item still reads 2/6 at tip.
