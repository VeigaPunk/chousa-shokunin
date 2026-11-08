# chousa round-85 verifier spot-check — non-author closure review

author: hyaku closure (non-author integrator, @m_zfl)

## Step-1 conformance

- **Report committed in the fleet repo by the lane identity.** `git log --format='%an %ae %H' -- .ufo/reports/round-85/chousa.md` → `chousa-shokunin chousa@shokunin.local 1581877a819da1d55a52c8a9a5cd2d87034d5d21` (and a 43-second-earlier filing `c35326da`, which cited `a8041fcd`). Observed: not a marker — it carries work performed, eight evidence pointers, a `Landed changes` table with per-row `LOG.md` bullets and hashes, two before→after measurements with their counting commands, `## Sources & frontier`, trend verdicts and the `SHONEN` heading. Two filings, one correction of the cited hash: `git diff c35326da 1581877a` = +3/−2 (cited lane HEAD `a8041fcd` → `da97aaa2`, one new `Landed changes` row for the erratum), committed 18 s after the erratum commit and 47 s before the driver's `complete` line, so the final bytes land last. Noted, not a defect.
- **`SHONEN` heading.** Present, one line per box, 4 boxes, all `[~]` with pointers; no `[x]`, no added/removed box. Lane rank unchanged (`SHONEN.md` still at HEAD; no promotion claim).
- **Cited lane commits exist and are ancestors of the branch.** `git cat-file -e <h>^{commit}` + `git merge-base --is-ancestor <h> master` for `5d0b9413`, `02df67db`, `64803d33`, `863d624e`, `a8041fcd`, `da97aaa2`, `43c3f728` → all `exists ancestor=YES`. Tested against `master`, never `@{u}` (git HEAD is detached: `rev-parse --abbrev-ref HEAD` → `HEAD`).
- **No uncommitted round work; pushed.** `scripts/hyaku/jj-lane.sh state chousa-shokunin` → `branch=master local=da97aaa2… remote=da97aaa2… ahead=0 behind=0 head=detached tracked=0 untracked=0`; `git -C chousa-shokunin status --porcelain` → empty; `git ls-remote origin refs/heads/master` → `da97aaa2d8c676deec659d6fcde893e1bfda9e74`.
- **Prompt fidelity.** `.ufo/prompts/chousa-round-85.md` (985 lines, committed by the lane as `87fe3d42`) is `templates/round-prompt.md` rendered with substitutions only: `diff <(sed -n '1,140p' prompt) <(sed -n '1,140p' template)` shows only `{{LANE}}`/`{{ROUND}}`/`{{FLEET_ROOT}}`/`{{AXES}}` replacements. Round-level items (i)–(v) present (§1 MISSION/AXES binding, §3 L2 floor = one batched swarm ≥8, §5 commit-then-push, §5 push scope, §5 L0), plus all five child-lane items (§4 report path `.ufo/reports/round-85/chousa.md`, commit-before-report, `SHONEN` heading, commit-hash citation rule, write scope); §2b frontier step and §8 pre-file ledger carried. The L2 floor quoted matches `MISSION.md` §L2 concurrency ("at least 8 … in one batched AgentSwarm call"); no role→model pin appears in the prompt (routing is deferred to the host route table, as `MISSION.md` requires).
- **Dispatch digest (copied from the closure prompt; `.ufo/watchdog.log` is mutable):**
  `2026-11-08T00:46:50-03:00 launch chousa round=85 pgid=1292517 driver=hyaku-inline attempt=1` /
  `2026-11-08T02:49:07-03:00 complete chousa round=85; hyaku-inline attempt=1`.
- **Wave shape (evidence-verified from committed artifacts).** `chousa-shokunin/.ufo/waves/round-85/w1-results.json` → 12 results (4 executor, 2 reviewer, 1 critic, 1 mutation-tester, 1 revenger, 1 scout, 1 connector, 1 scribe), 12 `.md` seat artifacts present, `w1.ready` + `w1-dispatch.json` + `w1-spec.json` committed. Attack seats by the ledger's role set (it counts `connector`) = 6/12 = 50%; by the round's narrower set (reviewer/critic/mutation/revenger) = 5/12. Both above the 25 % floor.

## Claims — re-derived by the non-author (nothing here is quoted from the report)

Instruments verified byte-identical to `corpus/evidence/round85/instrument-pins.txt`:
`sha256sum` → `gate-records-r85.py 62496d36…1d22`, `depth-r85.py 8ff164eb…3724`, `c2-positives.tsv 8c089828…f3c6`;
and the pinned subject bytes re-derive: `git show 64803d33:corpus/evidence/round85/claims.md | sha256sum` → `080ded8f…b7a5`,
`git show 64803d33:tools/gate-records.py | sha256sum` → `2de79722…3beb`.

### C1 operability (capability acquisition)

Trees: `git archive 64803d33 | tar -x -C landing`, `git archive 43c3f728 | tar -x -C base` (scratch
`/fast/scratch/hyaku/cl85`, removed after the run).

| run | command | observed |
|---|---|---|
| after @ landing | `python3 -B corpus/evidence/round85/gate-records-r85.py --root <landing> --repo <lane> --work <w1>` | `TOOL=present POSITIVE=15/15 FRESH_POSITIVE=5/5 FORGED_REFUSED=354/354 EXPECTED_CODE=354/354 EMPTY_REFUSED=1/1 RC=4/4 SETUP=1/1` / `GATE_RECORDS_R85=PASS` / exit 0 |
| after @ lane HEAD | same, `--root <head da97aaa2>` | identical line, `GATE_RECORDS_R85=PASS`, exit 0 |
| before @ base | counter + `c2-positives.tsv` copied byte-exactly into the base tree (base predates the counter) | `… FORGED_REFUSED=354/354 EXPECTED_CODE=342/354 EMPTY_REFUSED=1/1 RC=4/4 SETUP=0/1` / `GATE_RECORDS_R85=FAIL`, 12 × `WRONG_CODE … D4-non-timestamp-fetched expected=PARSE got=REFETCH`, exit 1 |
| 200-only witness | `python3 -B corpus/evidence/round85/forge-203.py --base-tree <base> --new-tree <head> --repo <lane> --work <w4>` | `OLD(base): rc=0 … S021 OK` / `NEW(head): rc=1 … S021 FAIL REFETCH` / `FORGE203=PASS`, exit 0 |

Both predicates reproduce exactly as reported; the base/landing delta is real (`SETUP=0/1`→`1/1`,
`EXPECTED_CODE=342/354`→`354/354`) and the 200-only repair is independently witnessed.
Cross-round compatibility (evidence-verified, not re-executed): `R85MutationTool` §2 runs the frozen r84 counter on
the landing tool → `GATE_RECORDS_R84=PASS`; `R85ExecHarm` reports base-OK→landing-FAIL = 0 over committed bytes; my
own census of that surface reproduces its denominators — `git grep -c -E '^[[:space:]]*GATE-RECORD' 64803d33` →
**355 lines in 274 files**, and `… -- corpus/lessons` → **24 lines**.

**Defect found in the before-row's committed receipt (status-neutral, named):** the report's before row and my
re-run both print `/354`, but the committed control `corpus/evidence/round85/controls/receipts/c1-k0-donothing.txt`
prints `FORGED_REFUSED=354/378 EXPECTED_CODE=342/378`. The receipt was produced by the **freeze**-pinned counter
(`931b5ed7…`, no `kv_set` absent-key guard: 24 of the 378 "forgeries" were byte-identical to their positive), not by
the landing-pinned counter. The lane discloses the instrument change (amendments 4/7b, QUALITY 170) but the receipts
were never re-run with the pinned counter, so the committed control tally belongs to a different instrument than the
post value it is compared with. Same class, second instance: `corpus/evidence/round85/claims.md:96` cites
`controls/receipts/c1-d0-donothing.txt`, which does not exist (the file is `c2-d0-donothing.txt`) — disclosed in the
lesson's `## Corrections` item 6, unrepaired because the freeze is not edited.

### C2 depth

| run | command | observed |
|---|---|---|
| after @ landing | `python3 -B corpus/evidence/round85/depth-r85.py --root <landing>` | `ENTRY provenance-recording-r85.md ok=yes rows=6 quotes=7/7 fails=-` / `DEPTH_R85 entries=1 ok_entries=1 rows=6 located_quotes=7 fresh_sources=3` / `DEPTH_R85=PASS`, exit 0 |
| after @ lane HEAD | same, `--root <head da97aaa2>` | identical, `DEPTH_R85=PASS`, exit 0 |
| before @ base | counter + `base-knowledge.txt` copied into the base tree | `DEPTH_R85 entries=0 ok_entries=0 rows=0 located_quotes=0 fresh_sources=0` / `DEPTH_R85=FAIL`, exit 1 |

Plain counts (no instrument): `git ls-tree -r --name-only <rev> corpus/knowledge | grep -c '\.md$'` →
`43c3f728`=**96**, `64803d33`=**97**, `da97aaa2`=**97**; `git show <rev>:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'`
→ `43c3f728`=**214**, `64803d33`=**215**, `da97aaa2`=**215**. Both reported counts re-derive.

**Additional finding the round did not record — S024 was re-mined while the lane's own registry marks it superseded.**
`corpus/SOURCES.md:41` (present at base `43c3f728`, unchanged at HEAD) is row **S031** — *"Schema.org property
lastReviewed — https://schema.org/lastReviewed … supersedes S024 — lastReviewed records the date a web page was last
reviewed for accuracy and/or completeness; **no comparison to other date properties claimed**"*, status `queued`,
`used-by —`. Round 85 flipped **S024** (same URL, same scope string, `awk -F'|'` on both rows) `queued`→`mined` with
`teaches` = *"A last-reviewed date for accuracy is a property separate from publication or modification dates"* and
`used-by` = the new entry, leaving the superseding row queued and unused. So (a) the registry now holds two rows on
one URL and one scope with contradictory `teaches`, and the **superseded** row carries the citation, inverting the
`CORPUS.md` §Rules-2 supersession convention; (b) the new row asserts exactly the publication/modification-date
comparison the lane's own earlier curation refused to claim; (c) the entry's row 6 `Never` ("pass a record off as
reviewed when only its modification date is known") rests on that same unclaimed comparison — `R85ReviewerEntry`
flagged the import and graded row 6 "held (weakly … see residuals)", so this is a wave residual, not a wave catch.
The census cannot flag it by construction: `scripts/sources-census.sh` exempts a same-scope duplicate whose `teaches`
matches `supersedes S[0-9]{3}` (`sources-census.sh:646-649`), and the duplicate is on the *superseding* row.
`E7` in `depth-r85.py` is entry-scoped ("its URL appears in no base-list entry"), so a registry-level duplicate
cannot fail it. Census run: `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` →
`ok`, exit 0, five pre-existing W04 rows (S051/S053/S073/S074/S075) only.

## Claim verdicts

- **C1 — does not verify as stated (honest stop).** The predicate's headline reproduces (base FAIL → landing PASS,
  `SETUP` leg load-bearing), but the sentence enumerates "per-class load-bearing forgeries for every enumerated
  class": class **D1** (stale-refetch / 200-only) generated **zero** forgeries (`D1_forges_at_landing 0`,
  `R85CriticClaims` §, `R85MutationTool` §4 S2/S4), and `M17-refetch-http-2xx-accepted` — the tool with `r[6] == "200"`
  relaxed back to `2xx` — **survives** all 354 legs. The claim's pre-repair failure signature (amendments/F2: "setup
  leg and the HTTP-203 class") does not reproduce either: at base the counter fails on `SETUP` plus 12 `D4` calendar
  wrong-codes, and no 203 class is exercised. The 200-only witness (`forge-203.py`) landed in `a8041fcd`, **after**
  the scored landing `64803d33`, so it cannot rescue a claim scored at `64803d33` (K2: "repairs after scoring do not
  rescue"). Narrowed property (amendment 7b) does hold and I re-ran both its load-bearing legs (M28/M29-class setup
  via `SETUP=0/1`→`1/1`; calendar via the 12 `D4` wrong-codes; 200-only via `forge-203.py`).
- **C2 — does not verify as stated (honest stop).** K3 fires on rows 1 and 5 on the scored bytes
  (`R85ReviewerEntry`: "primary" imported into row 1's `Never`; "tool/version/step" absent from S026 and from Q6).
  Under the frozen K3 ("one such row falsifies C2") that alone closes it. Independently: the ground sentence is
  narrower than stated — S215 is the same W3C Recommendation as **S033**, already taught by
  `corpus/knowledge/metadata-screen-r25.md` (`R85ScoutGround`), and **S024 is the same URL as S031, which the
  registry itself marks as superseding it** (finding above). And the C2 floors were lowered `rows≥7`→`≥6`,
  `located_quotes≥8`→`≥7` in the same commit that changed the ground although the prefreeze floors were reachable
  (`R85ScribeLesson` receipt 04: `rows=7 quotes=8/8 … PASS`) — a predicate relaxed onto its own artifact, mined as
  QUALITY 172. K2/K4 held (`7/7` quotes located in captures — I re-located all three Gate quotes at their capture
  byte offsets and matched each `capture_sha256` prefix — and no base-list entry cites S215/S026/S024).

**Re-measured by me:** both predicates (landing and HEAD), the base-side failure of each, the `forge-203` pair, the
knowledge/registry counts, the capture quotes, the census.
**Evidence-verified only (not executed — PROTOCOL §Gate standard):** `research-gate.sh --selftest`
(`measure/gate-selftest-r85.log` → `RESEARCH_GATE_SELFTEST: PASS (283 cases, 0 skipped)`), the preflight logs
(`PREFLIGHT=5/5 FAILED=none SKIPPED=G06,G07,G08`; `PREFLIGHT=2/2 FAILED=none`), the r84 counter's cross-round PASS,
and the harm ledger's alignment receipts.

## Per-axis verdicts (agree with the lane, with the additions above)

| axis | verdict | basis |
|---|---|---|
| operability | **improved narrowly, claim not admitted as written** | base→landing delta re-derived (`SETUP=0/1`→`1/1`, `342/354`→`354/354`); 200-only repair witnessed by `forge-203.py` reproduced by me; harm held over 354 committed records (0 base-OK→landing-FAIL); claim falsified on the D1 class and the stale control receipt |
| depth | **improved narrowly, claim falsified** | 96→97 `.md`; entry's S026 (FAIR R1.2 facets) ground is genuinely new; S024 re-mines an S031-superseded row, so the ground half is narrower than "S026 and S024 mined on provenance ground no base entry held" |
| calibration | **improved** | QUALITY 169–172 each carry evidence pointers and a Check; every attack seat reconciled by the ledger; the lane published its own freeze/egress/floor/receipt defects and its lesson carries two correction blocks that retract its own filed sentences |
| coverage | unchanged | `PROVINCE.md` untouched; the entry stays inside research-method scope |
| freshness | unchanged | no drift surface measured; S023 re-opened (anchor note + refetch row), S020 canonical URL still dead (403) and routed |
| adjacency | unchanged | `R85ConnectorSiblings`: no sibling holds FAIR R1.2 / `lastReviewed` ground; kotodama's PROV-O entry reported read-only, nothing absorbed |

SCORECARD harm sweep: `git diff 43c3f728 da97aaa2 -- SCORECARD.md` is append-only (one new `## Round 85 verdict`
section + `## Planned — round 86`; no score row rewritten). `corpus/lessons/round-85.md` `## Claim outcomes` still
prints **"verified"** for both claims — a superseded statement left standing beside the report's honest-stop verdict
(no correction item retracts it, though item 5 retracts the floors). Evidence-standard "corrections sweep every
mention" defect, routed below.

## Pre-file falsification ledger (addendum §8, Amendment 59)

`python3 /home/vgpnk/Projects/shokunin/scripts/hyaku/prefile-falsification.py --lane chousa --round 85` →
`PREFILE-FALSIFICATION: pass claims=2 rows=13 attack_seats=6 findings=0`, exit **0**. Present and passing; not a
conformance defect. I adjudicated every `falsifies-wording` row by re-opening the artifact it names:

| row | artifact | narrowing named | adjudication |
|---|---|---|---|
| C1 | `R85CriticClaims.md` | amendment 7 | **real and reconciled** — the 200-only class has 0 forgeries; amendment 7 names it, amendment 7b states the narrower claim that may verify, and the class is routed to round 86 |
| C1 | `R85MutationTool.md` | amendment 7 | **real and reconciled** — 6 survivors; S4/M17 is the 2xx→200 one; amendments 7/7b cite it as the reason for the honest stop |
| C2 | `R85ReviewerEntry.md` | amendment 8 | **real and reconciled** — rows 1 and 5 fired K3 on the scored bytes; amendment 8 writes the narrowed `Never` cells (which are the bytes now in the entry) and scores the verdict honest stop |
| C2 | `R85ScoutGround.md` | amendment 9 | **real and reconciled** — S215 = S033 document; amendment 9 narrows the expansion reading to FAIR R1.2 + `lastReviewed` |
| C2 | `R85ScribeLesson.md` | amendment 10 | **real and reconciled** — floors relaxed beside their ground; amendment 10 records both floors and the receipt proving the prefreeze floors reachable |

No spurious row; no unreconciled row. Ledger not edited. Gap the ledger's shape cannot express (reported, not a
ledger edit): the S024/S031 registry contradiction and the stale `c1-k0-donothing` tally are **falsifies-number/wording
facts with no attack seat that measured them**, so no row could carry them.

## Discernment spot-check (LEARNING.md) — `corpus/lessons/round-85.md` `## Gate`

The `## Gate` block records three admits and **no rejects** ("Rejected this round … none new", itself corrected by
`## Corrections` item 4 as a narration error: three refusals of one URL, none with a capture to register). The reject
sample below is therefore taken from the round's refusal/non-admission decisions, re-opened at their own evidence.

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S215 PROV-O alternate URL (tier A, admit) | admit | `corpus/captures/6e48bcc4a04d13b7b3ebb68e.txt` + `refetch.tsv` row 177 + `SOURCES.md:228` | agree | quote *"Provenance chains comprising only Entities can be formed using the prov:wasDerivedFrom property."* (12 words) located verbatim after whitespace collapse; `capture_sha256=8c9aeabb…` equals `sha256(capture)` and the row's refetch `txt_sha256`; tier A correct (W3C Recommendation for its own scope). Document identity with S033 is real and disclosed (amendment 9) |
| S026 GO FAIR R1.2 (tier A, admit) | admit | `corpus/captures/67983a3dbbd1d690aa648744.txt` + `refetch.tsv` row (2026-11-08T04:14:51Z, 200) | agree | 20-word quote located verbatim; sha prefix `27ee7573…` matches; new ground — no base entry cites R1.2 facets. Tier A arguable A/B for a foundation *interpretation*, but the row scopes its tier to that interpretation, which is honest |
| S024 Schema.org `lastReviewed` (tier A, admit → `mined`) | admit | `corpus/captures/11d6cc56bb24adfc61eea2b4.txt`, `SOURCES.md:34` **and `:41` (S031)** | **disagree** | the quote locates (16 words, sha prefix `97fe1a6a…` matches), but the round mined the row its own registry marks *superseded by S031* on the same URL and scope, and the new `teaches` claims a "separate from publication or modification dates" distinction that S031's `teaches` explicitly refuses ("no comparison to other date properties claimed"). The gate compared source-id freshness, not document novelty |
| row 6 of the entry (`lastReviewed` Do/Never) | admit (held "weakly") | S024 capture + `SOURCES.md:41` | **disagree (residual accepted by the seat)** | the seat itself records that "modification date" is imported and not entailed; the lane's own S031 row is decisive evidence the comparison was never claimed. Under frozen K3(a) the import is a firing form; two other rows already fired, so the score is unchanged, but the row should not have been left standing |
| S020 canonical PROV-O URL (not admitted; stays `queued`) | reject | `refetch.tsv` rows 175/176 (`http=403`, `curl_rc=22`) + `SOURCES.md:` S020 row | agree | correct refusal: 403 on both attempts, no capture, no quote; the material is carried by S215 under the alternate URL and the disposition is routed, not asserted |
| round-85 refusals not registered as rejected rows | reject (retained) | `refetch.tsv` rows 175, 176, 179 (all `403`, no `txt_sha256`) | agree | no refused URL carried a capture or a quote, so `CORPUS.md` gives nothing to write as a rejected row; the narration error ("none new" vs three refusals) is retracted in `## Corrections` 4. Side defect already disclosed: row 179 files the alternate URL under id `S033` (an id/url mismatch in an append-only log) |

Newly written SOURCES row quote check: all three new/touched rows carry ≤25-word located quotes — S215 12,
S026 20, S024 16 words, each located in its committed capture and each anchor naming a capture key that equals
`sha256(capture)[:24]` (`6e48bcc4a04d13b7b3ebb68e`, `67983a3dbbd1d690aa648744`, `11d6cc56bb24adfc61eea2b4`). The
lesson's three `GATE-RECORD` lines carry the same three quotes at the same word counts (`words=12/20/16`), so the
gate record and the registry agree.

## Trends

- **expansion: improved (narrowly).** 96→97 `knowledge/*.md`, registry 214→215, re-derived above. Narrowed further
  than the lane's own narrowed reading: of the three "fresh sources", **S215 re-emits S033's document** (amendment 9)
  and **S024 re-mines S031's URL** (this check), so the genuinely new ground is **S026's FAIR R1.2 facets** alone.
  An entry on that ground still counts — improved, not unchanged — but not on three fronts.
- **quality: improved (narrowly).** Three tool repairs with a re-run witness each, a self-inflicted instrument defect
  (`kv_set`) closed, four criteria mined with pointers, and no existing entry found false and left unmarked. Offset
  by: the D1 class still unwitnessed in the battery, the stale control receipts, the entry's row-6 residual, and the
  S024 → S031 inversion. Both claims honest-stop as stated.
- **discernment: improved.** The wave falsified both claims with receipts from five attack seats and the lane filed
  the falsification instead of widening the wording; the ledger reconciles all six attack seats; the lesson retracts
  its own false sentences in two correction blocks; four criteria carry the round's own defects. The one disagreeing
  admit (S024) is recorded here and routed — **if it is left unlearned next round this trend becomes `harmed`**.

## Routed defects — the lane must fix next round

1. **(curation, lane) `S024` vs `S031`.** Repository now holds two rows on `https://schema.org/lastReviewed`, one
   scope, contradictory `teaches`, with the *superseded* row carrying `mined` + `used-by` and the superseding row
   `queued` + `—`. Resolve by a new row whose `teaches` opens `supersedes S024 —` (or by retiring S024's citation and
   moving `used-by` to S031), and drop from `provenance-recording-r85.md` row 6 the "modification date" `Never` or
   cite a source that states it. Add the QUALITY criterion the census and `E7` structurally cannot cover: *a
   "fresh source" is a document new to the registry, not a row id the counter has not seen* (counter `E7` is
   entry-scoped; `sources-census.sh:646-649` exempts the superseding row).
2. **(instrument, lane) Re-run the four C1 control receipts with the pinned counter.** `c1-k0-donothing.txt` prints
   `/378` from the freeze counter; the report and a re-run of the pinned counter print `/354`. Either re-run at the
   pinned bytes and repin, or annotate the receipt with the instrument hash it was taken under. Also retire the
   frozen `claims.md:96` pointer to `controls/receipts/c1-d0-donothing.txt` (file is `c2-d0-donothing.txt`) via a
   superseding claims file — the freeze itself is not edited.
3. **(claim, lane) Add the 200-only forge to the battery** (a 203-row admit built from the committed S021 capture,
   expecting `REFETCH`) so `M17-refetch-http-2xx-accepted` dies inside the frozen predicate rather than beside it;
   the lane already routes this (planned r86 item 1, amendment 7b).
4. **(evidence standard, lane) `corpus/lessons/round-85.md` `## Claim outcomes` still says "verified" for C1 and C2.**
   File a correction entry retracting that column to the honest-stop verdict; a superseded claim must not stand in
   the lesson that the gate reads. (Found by this check; no attack seat measured it.)
5. **(cross-lane, route — aggregator/owner) kotodama `check-gate-captures.py` false-green.** Carried unchanged from
   `round-84-verifier-spotcheck.md`; `R85ConnectorSiblings` reconfirms it. Closure records routing; this lane must not
   edit the sibling.
6. **(operator, not a lane defect) SHONEN boxes.** All four are `[~]` lane-asserted; no non-author `[x]` exists, so
   the promotion gate is unmet. Reading the repo, all four now *look* checkable by a non-author — `SKILL.md` carries
   `## Decision table`, `## Error patterns`, `## Checklist (executable)`, `## Gates`; `LOG.md` Round 85 is an
   end-to-end domain task with pointers; box 3's command is runnable; `PROVINCE.md` is untouched and accurate.
   Promotion is operator-owned; flagged only.
