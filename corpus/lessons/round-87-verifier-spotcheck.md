# chousa round-87 verifier spot-check — non-author closure review

author: hyaku closure (non-author integrator, @m_zfl)

## Step-1 conformance

- **Report committed in the fleet repo by the lane identity.**
  `git -C /home/vgpnk/Projects/shokunin log --format='%an %H' -- .ufo/reports/round-87/chousa.md` →
  `chousa-shokunin 3dc2e41ef309e074a7db46f9a673bcdff7a5dc36`. Not a marker: work performed with evidence pointers, a
  Landed-changes table (7 rows, each with a LOG bullet and a hash), per-claim before→after with counting commands,
  Sources & frontier, trend verdicts, `SHONEN`, wave settlement and process notes.
- **`SHONEN` heading.** Present (report line 164), one line per box, 4 boxes, all `[~]` with evidence pointers; no `[x]`,
  no non-author verifier named (lane assertion only). `git diff 6495ef88 1f29e67b -- SHONEN.md` is empty — no promotion
  claimed.
- **Cited lane commits exist and are ancestors of `master`.** `git -C chousa-shokunin merge-base --is-ancestor <h> master`
  for `b7db0714`, `c033577b`, `e6e920a4`, `abf7ea58`, `1f29e67b` → all ancestor-OK. Tested against the `master` ref, never
  `@{u}` (head is detached: `head=detached`).
- **Base and after.** Base `6495ef881bb9062eaaf5029e20170992c00113f5` exists and is an ancestor; after `1f29e67b403c52386fac3a3c7a2fabcc64e1109c` is the lane tip and equals the remote tip.
- **No uncommitted round work; pushed.** `scripts/hyaku/jj-lane.sh state chousa-shokunin` →
  `branch=master local=1f29e67b403c52386fac3a3c7a2fabcc64e1109c remote=1f29e67b403c52386fac3a3c7a2fabcc64e1109c ahead=0 behind=0 head=detached tracked=0 untracked=0`;
  `git -C chousa-shokunin status --porcelain` → empty (before and after my own read-only re-runs).
- **Commit chain.** `6495ef88 → b7db0714 → c033577b → e6e920a4 → abf7ea58 → 1f29e67b`, linear, nothing stranded.
- **Prompt fidelity.** `.ufo/prompts/chousa-round-87.md` is 989 lines and diffs against `.ufo/prompts/chousa-round-86.md`
  only on round-number substitutions and the previous round's spot-check path
  (`diff <(sed 's/chousa/{{LANE}}/g; s/round-87/round-{{ROUND}}/g' …87) <(…86)`) — i.e. a byte-faithful template
  rendering. It carries §1 MISSION/AXES binding, §2 the 1–3 falsifiable claims with the lowest-axis rule, §2b the frontier
  step, §3 the L2 floor of ≥8 in one batched swarm with the role split, §4 the report contract (SHONEN one line per box,
  marker rule, commit-then-push ordering), §5 push scope and L0 side channel, and §6 the hyaku addendum with the run-15
  directive and §8 pre-file falsification duty. The L2 floor quoted (≥8, band 8–16) matches `MISSION.md` §L2 concurrency
  and run 15's size line.
- **Dispatch digest (copied from the closure prompt; `.ufo/watchdog.log` is mutable):**
  `2026-11-08T03:43:06-03:00 launch chousa round=87 pgid=3360448 driver=hyaku-inline attempt=1` /
  `2026-11-08T04:25:40-03:00 complete chousa round=87; hyaku-inline attempt=1`.
- **Pre-file falsification ledger.** `python3 scripts/hyaku/prefile-falsification.py --lane chousa --round 87` →
  `PREFILE-FALSIFICATION: pass claims=2 rows=15 attack_seats=6 findings=0`, exit 0. Coverage checked by reading the
  committed ledger `chousa-shokunin/.ufo/waves/round-87/claim-falsification.tsv` (15 rows): every row names a claim
  (`C1`/`C2`), every one of the six attack seats (`R87ExecC2Forge`, `R87MutCounter`, `R87ReviewerC1`, `R87ReviewerC2`,
  `R87CriticClaims`, `R87SentinelScope`) appears, and each `falsifies-wording` row names a narrowing. Six such rows:
  `R87ReviewerC1` → plan Amendment 4; `R87MutCounter/…/c1-mut-A8-setupok-hardcode.txt` → Amendment 4;
  `R87CriticClaims.md` → Amendment 4; `R87ExecC2Forge` → Amendment 2; `R87ReviewerC2` → Amendment 1 (its second finding,
  F2, is Amendment 3, also present); `R87CriticClaims/caseG.txt` → Amendment 6. `plans/round-87.md` carries Amendments
  1–6, each naming its artifact and the narrower property — I read all six and each is a real narrowing, not a restatement.
- **Wave evidence.** `.ufo/waves/round-87/{w1-spec.json,w1-dispatch.json,w1.ready,w1.ready.dispatched,w1-results.json,claim-falsification.tsv,w1/}`
  committed at `1f29e67b`; `w1-spec.json` items = 12, `w1-dispatch.json` `counts.spawn=12`, `w1-results.json` results = 12,
  0 dead. Roles: 4 executor, 2 reviewer, 1 mutation-tester, 1 critic, 1 sentinel, 1 scout, 1 connector, 1 scribe.

## Claims — re-derived by the non-author

Both instruments were re-executed over a **fresh `git archive` of the landing tree in scratch** (read-only over the lane;
no live-tree write, no network), and the results reproduce the committed `after/` receipts byte-for-byte. Everything else
(control batteries, mutation drivers, harm sweep) is **evidence-verified** from committed receipts, per PROTOCOL §Gate
standard — I did not run those.

### C1 `C1-BATTERY-R87` — operability — VERIFIED (re-measured)

- Command: `git -C chousa-shokunin archive 1f29e67b | tar -x -C $S && python3 -B $S/corpus/evidence/round87/gate-records-r87.py --root $S --repo /home/vgpnk/Projects/shokunin/chousa-shokunin --work $S`
- Observed (mine): `TOOL=present POSITIVE=15/15 FRESH_POSITIVE=5/5 FORGED_REFUSED=362/362 EXPECTED_CODE=362/362 EMPTY_REFUSED=1/1 RC=4/4 SETUP=1/1 D1_EXPECTED=3 D1_FORGES=3 D1_REFUSED=3/3 D2_FORGES=3 D2_REFUSED=3/3 MUT_ADMIT_DERIVED=1 MUT_ADMIT_KILLED=1 MUT_UNREACH_DERIVED=1 MUT_UNREACH_KILLED=1 DERIVE_NEG=1 LEGS=15/15` / `GATE_RECORDS_R87=PASS`, exit 0. Byte-identical to `after/c1-after.txt`.
- Before state, evidence-verified: `controls/receipts/c1-k0-donothing.txt` (`D2_REFUSED=0/3 … LEGS=11/15`, FAIL, exit 1) and `c1-k0b-frozen-instrument.txt` (round-86 instrument, `D1_FORGES=1`, no `D2_` field). Both are committed, both name their tool and tree.
- Instrument bytes pinned: `sha256sum` of `gate-records-r87.py` at the landing tree = `07336fca…b61e1`, equal to `instrument-pins.txt` row 1. The pin file records `base=6495ef88` and the freeze time.
- K1 holds (predicate met at landing, re-derived). K2 holds (362/362 refused with their frozen expected codes — all `REFETCH` per `controls/expected.tsv`). K3 holds (harm evidence-verified: `c1-harm-unreach.txt` `moved=0` at the freeze, `moved=0` over `files=11 records=28` at landing; correction 2 in the lesson scopes the two counts honestly). K4 holds (mutants derived from the subject tool's own bytes; `MUT_ADMIT_KILLED=1 MUT_UNREACH_KILLED=1` in the frozen run, `MUTANTS_KILLED=4/4 TOOL_MUTANTS_CAUGHT=2/2` in `after/c1-mutants-landing.txt`; the freeze predates the landing).
- **Named limit, respected.** The claim, the lesson and QUALITY 187 all state the same width: `LEGS` counts *appends*, so a leg expression detached from its measurement (`E4`, `E7`) or a joint narrowing of both width derivations (`E1`) survives while printing `PASS`. I confirmed this is the *stated* width rather than a discovered gap: `claims.md` C1 carries it as `namedLimit`, and Amendment 4 records the measured survivors (`A2/A4/A6/A8`, `T4` behaviour, `caseG` is C2). The round does not claim more than it measures.

### C2 `C2-CURATION-R87` — calibration — VERIFIED on the narrowed property

- Command: `python3 -B $S/corpus/evidence/round87/curation-r87.py --root /home/vgpnk/Projects/shokunin/chousa-shokunin`
- Observed (mine): `SUPERSEDED_LIVE=0 UNENTAILED_TERM=0 MODIFIED_DEF_CITED=1 QUOTES_LOCATED=20/20 Q_FLOORS=search-transparency-reporting-r84.md=13/13 floor13,provenance-recording-r85.md=7/7 floor7 WARRANT_OK=17/17 TEACHES_CHECKED=1 TEACHES_FLAGGED=1 TEACHES_UNRESOLVED=0 LEGS=7/7` / `TEACHES_FLAGGED S024 terms=publication,modification disposition=superseded by S031` / `CURATION_R87=PASS`, exit 0. Identical to `after/c2-after.txt`.
- Before, evidence-verified: the frozen round-86 counter accepts all four routed forgeries (`FORGERY_REFUSED=4/4 R86_ACCEPTED_FORGERY=4/4`, `controls/receipts/c2-controls.txt`) and has no leg for the three new classes (`c2-d0-donothing.txt` → `CURATION_R86=PASS`).
- Controls, evidence-verified: `after/c2-controls-landing.txt` `FORGERY_REFUSED=4/4`. I read the four forgery receipts (`receipt-A1c-strong-junk`, `receipt-A1d-truncate-to-junkword`, `receipt-B2-repoint-Q13-to-Q10`, `receipt-C2-teaches-term-absent-live`) — each is refused with its own reason.
- **Amendment adjudication (1, 2, 3, 6).** The published C2 sentence promised more than the legs enforce, and the wave proved it: a one-word verbatim quote restores a floor (`A1c`), a truncated quote passes (`A1d`), the warrant sharing test is per row not per qid (`F1`), the `TEACHES` disposition ignores a rejected superseder (`F2`), and deleting an uncited row plus relabelling a duplicate of a cited one restores `13/13` (`caseG`). Each amendment names its artifact and narrows to the enforced property; the narrowed claim is what verifies. I find the narrowing legitimate — it is a *withdrawal of stated wording*, not a downgrade of the measured values, and the count semantics are routed to round 88 in Amendment 6's remedy.
- Live check of the narrower property: `S024`'s `teaches` reads "a property separate from publication or modification dates"; `grep -ci 'modification\|publication' corpus/captures/11d6cc56bb24adfc61eea2b4.txt` → `0`,`0`; `S031` (same URL, `mined`, `used-by → corpus/knowledge/provenance-recording-r85.md`) supersedes it. The leg fires once on the tree and the disposition is structural, as declared.
- K1 holds; K2 holds on the counted property (20/20 quotes located in the capture of their row's URL — spot-verified for Q1/Q13 in r84 and Q7 in r85 below); K3 holds on the control mirrors; K4 holds (`TEACHES_FLAGGED=1`, not zero — a dead detector would print 0).

## Spot-check table (Discernment, LEARNING.md)

This round's `## Gate` records one new registry row (`S218`, `own-work`) and one admitted re-open (`S216`), and disposes
`S024`'s frozen `teaches` cell as superseded rather than reading it. There is no new `decision=reject` row this round, so
for the reject half I re-opened the standing reject the round's `TEACHES` machinery is built around (`S024`) and the
registry's most recent explicit rejection (`S217`), labelled as such.

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| `S216` admit (re-open) | admit | `corpus/captures/b1b13a12aee75c6ecc20fb91.txt` line 12267, §15.3.4 | agree | The 22-word quote in the Gate record is verbatim at the cited line and continues "…200 (OK) response by a transforming proxy (Section 7.7)"; §15.3.4 is the right anchor for 203. `sha256sum` of the capture = `ec14fa3499c2dfbc…`, and `grep -P '^S216\t' corpus/evidence/round57/refetch.tsv` returns attempts 1 and 2 with **identical** `raw_sha256=d4317606…` and `txt_sha256=ec14fa34…`. The "no capture byte moved" claim is true column-to-column. |
| `S218` admit (new, `own-work`) | admit | `corpus/QUALITY.md` criterion 178; `CORPUS.md` §"SOURCES.md — where a shokunin learns" rule 2 | agree | Both locations exist and say what the row says: criterion 178 (line 1120) states a frozen `teaches` is not evidence and the superseding row's is; registry rule 2 restricts in-place cell changes to `status`/`recheck`/`used-by`. Tier A is correct for `own-work` re-runnable lane rules. See conformance defect 2 — the row carries no ≤25-word quote in the Gate record. |
| `S024` `teaches` rejected as evidence | reject (as evidence) | `corpus/SOURCES.md` S024/S031 rows; `corpus/captures/11d6cc56bb24adfc61eea2b4.txt` | agree | `S024` asserts "separate from publication or modification dates"; the capture contains `modification`/`publication` **zero** times and `S031`'s `teaches` opens `supersedes S024 —` and refuses that comparison. Disposing the cell rather than editing it is the only move rule 2 permits, and the `TEACHES` leg enforces the disposition. |
| `S217` reject (standing, round 86) | reject | `corpus/captures/52db06f9e0e2eaf35bbdb321.txt` | agree | The capture is 9 lines: blank lines plus the redirect-target URL, no policy prose. No ≤25-word quote can ground the row; the rejection carries its reason and flip condition. |

Census validation: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` → `chousa ok
/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md`, **exit 0**, five pre-existing `W04` duplicate-URL
warnings (`S051`, `S053`, `S073`, `S074`, `S075`) — the same five the report names, none introduced this round.
Registry rows 217 → 218 verified on the bytes (`git show 6495ef88:corpus/SOURCES.md` vs the landing file), and
`git diff 6495ef88 1f29e67b -- corpus/SOURCES.md` shows exactly one appended row (`S218`) and one in-place `used-by`
extension on `S216` — no immutable cell touched.

## Per-axis verdicts

| Axis | Verdict | Evidence |
|---|---|---|
| operability | **improved** | C1 re-measured at the landing revision: the 203 class is every qualifying committed row (3) with an independent width derivation, the reject form refuses every 2xx, and the verdict is leg-accounted (`LEGS=15/15` against a frozen `EXPECTED_LEGS`) so a deleted append or a denial-shape mutant changes it. 362/362 forgeries refused with their expected codes; `moved=0` over 28 committed records. The historical 3/10 is held rather than re-scored, as the SCORECARD row states. |
| calibration | **improved** | C2 re-measured on the narrowed property: per-entry located-row floors (13/7) refuse the delete-row and truncate-table forms the round-86 counter passed; 17/17 decision rows carry a term-linked warrant; the `TEACHES` leg fires once and requires a supersession disposition. Eight criteria mined (QUALITY 182–189). Two of this round's own first instruments were falsified by its own pre-freeze probes and published as `## Mistakes` 1–2 instead of being quietly repaired. |
| depth | **unchanged** | `git ls-tree -r --name-only … corpus/knowledge \| grep -c '\.md$'` → 97 at both revisions. The one new registry row is `own-work` (a contract, not a domain fact), and the report says so. |
| coverage | **unchanged** | `PROVINCE.md` untouched (`git diff 6495ef88 1f29e67b -- PROVINCE.md` empty); registry 217 → 218; census exit 0 at both ends. |
| freshness | **unchanged** | One URL re-opened (`S216`, HTTP 200 at `2026-11-08T06:50:40Z`), captures byte-identical to round 86; no drift detector added. The egress table is committed at `b7db0714`, `2026-11-08T03:50:27-03:00` = `06:50:27Z`, 13 s before the fetch — verified from the commit's own timestamp. |
| adjacency | **unchanged** | `R87ConnectorSiblings` scanned every sibling for HTTP-status, record-schema and quote-floor ground, found no conflict and nothing stricter; nothing absorbed. Read-only, as declared. |

No axis is harmed. `git diff 6495ef88 1f29e67b -- SCORECARD.md` is +40/−0 — an appended round-87 verdict and round-88
plan, consistent with the SCORECARD contract (append, never rewrite). `SKILL.md` is untouched this round.

## Trends

| trend | verdict | evidence |
|---|---|---|
| expansion | **unchanged** | 97 → 97 knowledge entries; registry +1 `own-work` row. The round's gain is in the instruments and the report declines to convert a registry row into "ground" — an honest `unchanged`. |
| quality | **improved** | Six routed repairs across two instruments, each with a receipt: the 203 class widened to every committed qualifying row, the unreach form refusing all 2xx, leg accounting, per-entry floors, warrant linkage, and the `TEACHES` leg. Four round-86 forgeries now refused with named legs; 362 forgeries refused with expected codes; no genuine committed record moves. |
| discernment | **improved** | Every one of the six attack seats produced a finding that became a numbered amendment or a named limit; none was argued away. The round withdrew its own sentence about the `M2` credit shape (`R87CriticClaims` §c), restated its named limit at the measured width (Amendment 4), and published three defects in its own artifacts (the egress closure predicate, the census ordering, the README miscount) as Mistakes 6–7 rather than leaving them to the closure. My own spot-check agrees with every sampled gate decision. |

## Routed defects (lane to fix next round)

1. **`SCORECARD.md` round-87 header says the wave was 13 seats.** The committed evidence says 12 everywhere else:
   `w1-spec.json` items = 12, `w1-dispatch.json` `counts.spawn=12`, `w1-results.json` results = 12, the report and the
   lesson both say 12. Fix the count (or name the thirteenth seat and its receipt); the SCORECARD is lane-authored and
   this is its own heading, so it is a lane fix, not a closure edit.
2. **The mined-criteria count in the lane's own files is stale.** `corpus/QUALITY.md` carries criteria 182–189 (eight:
   `grep -cE '^18[2-9]\.' corpus/QUALITY.md` → 8; base carried 180–181), while the lesson's `## Trends` row and the
   SCORECARD's calibration row both say "five criteria mined (QUALITY 182–186)". The report says eight. The count was
   true at `e6e920a4`; criteria 187–189 landed in the integration commit and the two sentences were not corrected with
   them. Append the correction (the lesson is append-only — a `## Corrections` row, not an in-place rewrite). The
   attribution split is also looser than the receipt set: 182–184 come from pre-freeze probes (Mistakes 1, 2, 4), 185–186
   from round-86's routed defects, and 187–189 from the wave's findings (Mistakes 5–7), which is three/four/three, not the
   report's "four and four".
3. **`S218`'s Gate record carries no ≤25-word located quote.** CORPUS rule 1 asks for the URL (here: a path), the access
   date and a ≤25-word quote with its location for **every** new row. The record gives both locations and the paraphrase,
   but no quoted sentence. For an `own-work` row this is the weakest form of the requirement, not an exemption; quote
   criterion 178's operative clause (≤25 words) in the next round's lesson.
4. **Carried template defect, correctly attributed but mis-quoted.** Report conformance note 1 says
   `.ufo/prompts/chousa-round-87.md:143` "ends `…shokunin style bu…`". Line 143 is indeed where the addendum's run-15
   quote is corrupted, and it is byte-identical to the round-86 prompt, but the line does not end there (1043 characters,
   ending `…reaches round 100".`) and the corrupted fragment reads `on the hyaku style but using these models and conc
   i've assigned` — the cut is mid-word at `conc`/`remembe`/`re each`, not "shokunin style bu". The substance (the
   operator-owned template carries a corrupted run-15 quote) stands; the description should cite the real fragment.

## Conformance defects (status-neutral, named)

1. Census receipt ordering (self-disclosed): `census-start.txt` recomputes the base registry from the `6495ef88` archive
   but was written after the landing commit, so the file order is end-then-start. Substance holds by construction; the
   ordering claim is evidenced only by both receipts carrying `# computed_against=`. Recorded as Mistakes 7 and QUALITY
   189 by the lane — a good self-catch, named here only for the record.
2. `corpus/README.md` frontier prose still ends at round 6 (carried, reported, not claimed fixed).
3. `merge/chousa/` / `considerthese/` not assimilated; the report says so plainly ("Assimilation: none").

None of these bars admission: the report names real committed work, both claims verify, and no axis is harmed.
