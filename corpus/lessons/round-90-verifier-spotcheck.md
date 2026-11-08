# Round 90 — non-author verifier spot-check (hyaku closure)

author: hyaku closure (non-author integrator, @m_zfl)

Lane `chousa`, lane-round `90`. Base `f54a45ed197dd475af50d82e43a22df3d2e99782` (round-89 landing + its
non-author spot-check), lane HEAD at filing `64db6a83b8fd262076f80c8cb161fd659da0dac2`. I authored nothing in
this round. Per `PROTOCOL.md` §Gate standard (closure consequence) I did not execute a sibling's gate: the three
claims were re-derived from **committed bytes** (git/grep/awk/sha256 reads and source reads) and the instrument
runs were **evidence-verified** from the committed receipts and the wave artifacts. Every command and number
below was run by this closure against the committed tip tree unless explicitly marked "evidence-verified".

Dispatch/complete digest (copied from the closure brief; `.ufo/watchdog.log` is mutable, lines 3326 and 3339 at
read time):
`2026-11-08T06:39:55-03:00 launch chousa round=90 pgid=2956878 driver=hyaku-inline attempt=1`;
`2026-11-08T07:43:20-03:00 complete chousa round=90; hyaku-inline attempt=1`.

## Step-1 conformance

1. **Report identity and path.** `git log --format='%an %ae %H' -- .ufo/reports/round-90/chousa.md` →
   `chousa-shokunin chousa@shokunin.local 75c08f9620921d864b735ebcddeb3099e5c16502`. `git show --name-only
   75c08f96` lists exactly `.ufo/reports/round-90/chousa.md` (155 lines), no sibling sweep. Pass.
2. **Landed last.** Lane tip `64db6a83` is 2026-11-08T07:42:39-03:00; the report commit `75c08f96` is
   07:43:03-03:00 and cites `64db6a83`. The report lands after the work it cites. Pass.
3. **`SHONEN` heading.** `## SHONEN` at report line 118, four lines for the four `SHONEN.md` boxes
   (`grep -n '^- \[' SHONEN.md` → 4), all `[~]` with pointers, no `[x]`. All required sections present in
   order (Work performed, Landed changes, Before → after measurements, Sources & frontier, Trend verdicts,
   SHONEN, Process notes). Real report, not a marker. Pass.
4. **Cited commits exist and are ancestors of the branch ref** (`master`; the repo is jj-colocated and HEAD is
   detached): `8d9893b42eb22690ea5f920ab87fd7e1810b847a`, `9bad12011187d114ba2c4588c5df08a21ab28145`,
   `aa7d4223`, `a45cbff6e783b9d817c23c99716c5fc7135f8a44`, `64db6a83b8fd262076f80c8cb161fd659da0dac2`,
   `af71d0a1`, `6ccf22b9` → `git merge-base --is-ancestor <hash> master` → 0 for each. Pass.
5. **Pushed, no uncommitted round work.**
   `scripts/hyaku/jj-lane.sh state /home/vgpnk/Projects/shokunin/chousa-shokunin` →
   `state branch=master local=64db6a83b8fd262076f80c8cb161fd659da0dac2 remote=64db6a83b8fd262076f80c8cb161fd659da0dac2
   ahead=0 behind=0 head=detached tracked=0 untracked=0`; `git status --porcelain` prints nothing. Pass.
6. **Prompt carries the template contract.** `diff templates/round-prompt.md .ufo/prompts/chousa-round-90.md`
   (lines 1–140) shows only the substitutions `{{LANE}}`=chousa, `{{ROUND}}`=90, `{{FLEET_ROOT}}`, `{{AXES}}`;
   the hyaku addendum §6 begins at line 141. Present: mission/axes binding (§1), 1–3 falsifiable claims (§2),
   frontier step (§2b), L2 floor ≥8 in one batched swarm with role split (§3), report contract + marker rule
   (§4), commit-then-push + push scope + L0 (§5). All five child-lane items are carried: report path (§4),
   commit-before-report ordering (§5), `SHONEN` heading (§4), commit-hash citation (§4 "Landed changes"), lane
   write scope (§5). The prompt's §3 routes roles through `task.agentModelOverrides` and states
   "the route table, not this prompt, decides"; no bucket contradiction with `MISSION.md` §L2 concurrency.
   The planner seat is not dispatched: prompt lines 394–397 rule that `planner` is a frozen-topology validator
   rejection and the L1 holds the canonical §3 planner seat, and the report records that mapping. Pass.
7. **Wave / L2 floor.** `.ufo/waves/round-90/w1-dispatch.json` is one `taskCall` with 13 tasks (`spawn: 13,
   resume: 0`); `w1-results.json` records `seats: 13` and 13 seat reports exist under `w1/`:
   `Counter({'executor': 5, 'reviewer': 2, 'critic': 1, 'mutation-tester': 1, 'sentinel': 1, 'scout': 1,
   'connector': 1, 'scribe': 1})`, 0 dead. Above the ≥8 floor; attack seats 6/13 = 46 %. Pass.
8. **Marker test.** Real committed work, resolvable hashes, full section contract → status `ok`.

## Prefile falsification (addendum §8, Amendment 59)

Command re-run by this closure, unedited:
`python3 /home/vgpnk/Projects/shokunin/scripts/hyaku/prefile-falsification.py --lane chousa --round 90` →
`PREFILE-FALSIFICATION: pass claims=3 rows=18 attack_seats=6 findings=0`, exit **0**.

Coverage: `.ufo/waves/round-90/claim-falsification.tsv` carries 18 rows covering C1/C2/C3 and names all six
attack seats (`R90ReviewerC1`, `R90ReviewerC2`, `R90CriticClaims`, `R90MutBattery`, `R90SentinelScope`,
`R90ConnectorSiblings`) 3× each; every artifact path resolves under `.ufo/waves/round-90/`. Four rows are
`falsifies-wording`, each carrying a `narrowing` pointer to `plans/round-90.md`; no `falsifies-number` row; no
row is unreconciled. The C2 honest stop is carried by Amendment 8 (the kill rule, not a wording clause).

Adjudication of the load-bearing rows (re-opened by this closure):

| row | firing | real? | adjudication |
|---|---|---|---|
| C1 `R90ReviewerC1` → Amendment 4 | duplicate `# exit=`/`# computed_against=`/`# case=` headers resolve last-wins; `EXACT_OK` is not a term of `passed`; the instrument bytes a row executes are unpinned | yes — read in `control-driver-r90.py` (`header_fields()` keeps the last value; `instrument-pins.txt` is not read) | narrowed to what the driver enforces (limits 4–5); the six scored rows carry one header each, so no scored field moves. C1 verifies on the narrowed text. |
| C1 `R90MutBattery` → Amendments 7 + 9 | the frozen counting command omits the driver's required `--work`; one-point mutants (`fresh-no-compare`, `empty-body-ok`) survive the frozen fixture set | yes — `argparse` requires `--work`; the fixture set has no divergence/empty-body case | command corrected; the detector is the frozen fixture set (limit 6), round-91 repair routed. Not a claim failure. |
| C2 `R90ReviewerC2` → Amendments 5–6 | "die on `LEG_FAIL WITNESS`" is the committed run's death line, not a battery detector; the before-receipt is a derived survival marker | yes — `curation-r90-mutants.py` kills on exit/verdict, and `grep -c 'CURATION_R89=PASS' c2-subst-before.txt` → 0 | both narrowed. C2 still honest-stops on K2 (Amendment 8), so these are recorded, not load-bearing. |
| C3 `R90MutBattery` → Amendment 10 | `EXPECTED_CASES` read from the file instead of the tool survives the landing leg and dies only on the 275-case before leg | yes — the before/after pair is what binds the number | narrowed: the expected-number clause verifies over the before+landing pair. C3 verifies on that wording. |

Two ledger-precision defects (**status-neutral**, routed below): (a) every `narrowing` cell names
`plans/round-90.md` without the amendment number (the note carries it); (b) the C1/`R90SentinelScope` row is
graded `neutral` although its F2 — a forged committed body field still prints `CONTROL_DRIVER_R90=PASS` — is
exactly the un-narrowed (g) that Amendment 2/4(g) narrows; the row should read `falsifies-wording`. The
substantive narrowing exists, so C1 still verifies on the narrowed text; the ledger's coverage is what is off.

## Claims — re-measured vs evidence-verified

**C1 `C1-DRIVER-R90` (operability).** Evidence-verified on the narrowed wording (Amendments 2, 3, 4, 7, 9);
the pins and the receipt headers were re-measured from committed bytes by this closure.

```
$ while read -r want path; do got=$(git show 8d9893b4:"$path" | sha256sum | cut -d' ' -f1); ... done \
    < corpus/evidence/round90/instrument-pins.txt
PIN OK ×11   (driver, forgeries, harm-recheck, curation±controls/mutants, skill-tally, expected.tsv, claims.md,
              claims.json, plans/round-90.md)
$ for f in c1-gate-r89 c1-mutants-r89 c1-harm c1-harm-setup c2-prior-landing c2-prior-controls; do
    git show 9bad1201:corpus/evidence/round90/controls/receipts/$f.txt | grep -E '^#(exit|computed_against)'
# case=c1-harm-setup → # expected_exit=2 / # exit=2 ; every other row → # exit=0 ; all six →
# computed_against=8d9893b42eb22690ea5f920ab87fd7e1810b847a
$ grep -cE 'TOKEN_DETACHED|DUPLICATE_KEY|PIN_MISSING|PIN_MISMATCH|PREDICATE_SHORT' \
    corpus/evidence/round90/control-driver-r90.py            # 7
$ git show 9bad1201:corpus/evidence/round89/controls/run-controls.sh   # the prior driver
   line 25: ( cd "$ROOT" && eval "$instrument" ) >"$out" 2>&1   # overwrites the receipt before reading it
   line 30: grep -qF -- "$f" "$out"                            # substring match
   grep -c 'computed_against|DUPLICATE_KEY|TOKEN_DETACHED|records>=' → 0   # no pin, no duplicate-key, no predicate
$ grep -nE 'B1-committed|B2-substring|B3-no-pin|B3b-stale-pin|B4-harm-vacuity|C-duplicate-key|POSITIVE' \
    corpus/evidence/round90/control-forgeries-r90.py | wc -l    # 6 classes + the positive
```

After, evidence-verified from the committed landing receipts: `after/c1-verify-landing.txt` →
`RECEIPT … OK committed+exact+pin+fresh` ×6, `RECEIPT SELF_PIN OK all scoring bytes equal their blobs at --rev`,
`COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 CONTROL_DRIVER_R90=PASS`;
`after/c1-forgeries-landing.txt` → six `OK B…/C-duplicate-key: r90 refused (…), r89 accepted` lines with
`r90 rc=1 prior rc=0`, `OK POSITIVE … r90 rc=0 prior rc=0`,
`FORGERY_REFUSED=6/6 PRIOR_ACCEPTED=6/6 POSITIVE=pass`. Before, re-measured at source: the r89 driver cannot
refuse any of the six classes (it overwrites before reading, matches substrings, and carries no pin,
duplicate-key or predicate leg), so the `FORGERY_REFUSED=0/6`-equivalent prior state is true by construction
and is corroborated by `after/c1-forgeries-landing.txt` (`prior rc=0` on all six). **Verdict: verified,
narrowed** (the narrowed limits are Amendments 2/3/4 and 9; the un-narrowed header/pin/body-agreement readings
are false and are not claimed).

**C2 `C2-CURATION-R90` (calibration).** Does **not** verify; the lane honest-stopped it (Amendment 8). I
substantiated the kill rule firing from the counter's source rather than from the lane's summary:

```
$ sed -n '229,244p' corpus/evidence/round90/curation-r90.py
    for cells in table_rows(section_lines(text, "Located quotes"), 3):
        if not re.match(r"Q\d+$", cells[0]):
            continue                      # a row outside the Q/3-cell shape is dropped BEFORE counting
$ grep -n 'cells\[7\]' corpus/evidence/round90/curation-r90.py
205:        if cells[7] == "mined": ...       # status is read only by the supersession block
208:        if target is not None and target[7] == "mined" and cells[7] != "mined": ...
```

Both falsified trees are committed at exit 0 with the full frozen conjunction
(`w1/R90ExecC2Forge/t-nonq-row-r90.txt`, `t-status-rejected-r90.txt` → `QUOTES_LOCATED=20/20 … CURATION_R90=PASS`,
exit 0), and both mechanisms are visible in the source above. K2 ("a tree forgery is accepted") fires; a kill
rule cannot be rewritten after a seat has scored. Before/after numbers that do reproduce, evidence-verified:
`grep -c 'VERDICT fields_hold=1' controls/receipts/c2-prior-landing.txt` → 0, on
`after/c2-counter-landing.txt` → 2; `LEGS_MEASURED=8/8` → `10/10`; `MUTANTS_KILLED=10/10 …
PRIOR_R89_SURVIVORS=2/2`; `CONTROLS=PASS FORGERY_REFUSED=7/7 PRIOR_REGRESSION=7/7`. Reported, not admitted.
**Verdict: unverified (honest stop)** — calibration is not improved and nothing is harmed.

**C3 `C3-TALLY-R90` (freshness).** Re-measured from committed bytes (Amendments 1 and 10).

```
$ grep -c "283 cases, 0 skipped" SKILL.md                       # 9  (tip)
$ git show f54a45ed:SKILL.md | grep -c "275 cases, 0 skipped"   # 9  (base)
$ grep -n "PASS ([0-9]* cases," SKILL.md | grep -v "283 cases"  # 186 (256), 188 (161), 640 (215) — historical
$ grep -c "PASS ([0-9]* cases," SKILL.md                        # 12 = 9 current + 3 historical (OTHER_OCCURRENCES=3)
$ grep -c '^ok-case' corpus/evidence/round90/controls/selftest-r90.txt   # 283, indices 1..283 distinct, 0 FAIL-case
$ tail -1 corpus/evidence/round90/controls/selftest-r90.txt
RESEARCH_GATE_SELFTEST: PASS (283 cases, 0 skipped)
$ git diff --numstat f54a45ed 64db6a83 -- SKILL.md              # 9  9  (nine lines: eight Gates rows + host note)
$ git diff --stat f54a45ed 64db6a83 -- tools/                   # (empty — tools byte-identical at base and tip)
```

The subject tool is byte-identical at base and tip, so the 283-case verdict committed in the freeze receipt is
the tool's own verdict at both revisions; the nine base cells (275) were therefore stale against the tool and the
nine tip cells (283) match it. `after/c3-after.txt` → `TALLY_ROWS=9 STALE_TALLIES=0/9 EXPECTED_CASES=283
EXPECTED_SKIPPED=0 OTHER_OCCURRENCES=3 SKILL_TALLY_R90=PASS`; `controls/receipts/c3-before.txt` →
`STALE_TALLIES=9/9 … SKILL_TALLY_R90=FAIL` (exit 1). K3 holds (9 changed lines, only tally cells + the host
note). The expected number is not a literal: the before run already printed `!= tool 283/0` (it ran the tool),
and Amendment 10 binds the clause to the before+landing pair. **Verdict: verified, narrowed.**

## Harm / no-axis-moved

```
$ git diff --numstat f54a45ed 64db6a83 -- corpus/SOURCES.md SKILL.md LOG.md SCORECARD.md \
    corpus/QUALITY.md corpus/README.md corpus/evidence/round57/refetch.tsv
38 0 LOG.md | 42 0 SCORECARD.md | 9 9 SKILL.md | 48 0 corpus/QUALITY.md | 9 0 corpus/README.md
1 0 corpus/SOURCES.md | 3 0 corpus/evidence/round57/refetch.tsv
$ git diff --name-only f54a45ed 64db6a83 -- PROVINCE.md SHONEN.md AGENTS.md | wc -l      # 0
$ git ls-tree -r --name-only f54a45ed -- corpus/knowledge | wc -l                        # 98 (97 .md + .gitkeep)
$ git ls-tree -r --name-only 64db6a83 -- corpus/knowledge | wc -l                        # 98
$ git diff --stat f54a45ed 64db6a83 -- corpus/knowledge                                  # (empty)
```

The registry diff is one added row (`S220`) and no in-place cell change; `SKILL.md` moves only in its nine tally
cells; no curated entry's verdict moved; `PROVINCE.md`/`SHONEN.md`/`AGENTS.md` untouched; the subject tools
unchanged. C2's K3 harm test and C3's K3 harm test both hold.

## Gate evidence (Gate standard, closure consequence)

Evidence-verified, not executed: `after/preflight-landing.txt` →
`GATE G01 census PASS exit=0 … GATE G08 gate-selftest PASS exit=0 / PREFLIGHT=8/8 FAILED=none ENV=none
SKIPPED=none`; `controls/selftest-r90.txt` → `PASS (283 cases, 0 skipped)` with 283 distinct `ok-case` lines;
`corpus/lessons/round-90.md` `## Gate` carries the S220 `GATE-RECORD` with `capture_sha256=5a5e69c5…` and
`words=10`. I re-derived the substantive parts myself (quote presence, sha256, per-file pins, tally counts)
rather than relying on the tallies alone.

## Source census

`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa`
→ exit 0, `chousa ok …/corpus/SOURCES.md`, same five pre-existing `W04` duplicate-URL warnings (S051, S053,
S073, S074, S075). Rows 218 → 219 (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` at base / tip); 0
malformed rows (`awk … NF!=13`). Matches both committed census files.

## Per-axis verdicts

| axis | verdict | evidence |
|---|---|---|
| operability | **improved** | C1 verified on Amendments 2/3/4/7/9: committed receipt read before any fresh run and never written by `verify`, whole-token binding (`TOKEN_DETACHED`), `DUPLICATE_KEY`, exit/pin/predicate legs, six forgery classes refused where the r89 driver carries none of those legs, positive accepted. All 11 instrument pins re-derived at the freeze revision. Residues (duplicate headers, unpinned instrument bytes, `SELF_PIN` base) named as limits 4–5 and routed. |
| calibration | unchanged | C2 honest-stopped: frozen K2 fires on two tree forgeries the three-command kit accepts at exit 0; the counter's own parser shows both mechanisms. The printed verdict, 10/10 mutants and 2/2 prior survivors are reported, not admitted. Nothing regressed and `curation-r90.py`'s extra legs are additive over `curation-r89.py`. |
| freshness | **improved** | C3: nine current `SKILL.md` tallies re-derive to the tool's own 283-case verdict; 275→283 in nine cells, three historical quotes counted and untouched, `tools/` byte-identical. |
| depth | unchanged | no new `corpus/knowledge/` entry (97 `.md` at base and tip); S220 grounds an instrument rule, not a domain fact. |
| coverage | unchanged | registry 218 → 219 (one mined row); `PROVINCE.md` untouched; no frontier row advanced (disclosed). |
| adjacency | unchanged | `R90ConnectorSiblings` reports read-only sibling scan; nothing absorbed; no cross-domain claim made. |

## Discernment spot-check (LEARNING.md, from outside)

The round's `## Gate` records one admit and no new registry rejection; the reject half of the sample is the
round's own gate-level refusal (the reserved `S219` id and the byte-less gnu.org attempt) — both re-opened.

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S220 GNU grep(1) `-x` | admit (tier A) | `corpus/captures/e6ec761219e8044b0e9e067a.txt` — sha256 `5a5e69c56413ba682b1609cba2baacafb393ff6821d5b752938efc390fd12823` at `aa7d4223` and in the working tree; anchor `Matching Control`, lines 166–167 | agree | the quote is verbatim after whitespace normalisation ("Select only those matches that exactly match the whole / line."), 10 words ≤ 25, and it grounds the row's scope (whole-line selection for a receipt field checked as one token). Tier A is defensible on the row's deliberately narrow scope; the page is a man-page render, not the official GNU manual host — the flip is already covered by the 180-day recheck. |
| `S219` candidate row (reserved, not written) | reject | `corpus/evidence/round89/curation-r89-controls.py:41` (`S219_ROW = "\| S219 \| mirror row …"`), `.ufo/waves/round-90/w1/R90ScoutRegistry.md:115` (`FORGERY_REFUSED=7/7 PRIOR_ACCEPTED_FORGERY=6/7`) | agree | the id is free in the registry but is a live literal inside the r89 control battery's mirror table; a real row at that id displaces the mirror and one prior case stops being accepted. Renumbering to `S220` is the right disposition, and `grep -c "\| S219 \|" corpus/SOURCES.md` → 0 confirms the reservation held. |
| gnu.org grep manual (first attempt) | reject (no row) | `corpus/evidence/round57/refetch.tsv` row `S219 … 28 000 - -`; `.ufo/waves/round-90/egress.tsv` line 1 | agree | a fetch with rc 28 and no bytes cannot ground a quote, and the refetch row records the failure without a digest; writing a row from it would be an unsupported claim. (Re-open of the live URL was not attempted; the decision rests on the recorded absence of bytes, which is what the row claims.) |
| three historical tallies left untouched | not bound (correct refusal to "repair" history) | `SKILL.md:186`, `:188`, `:640` (256 / 161 / 215 cases) | agree | all three sit outside the Gates table and outside the host-note phrase; rewriting them to 283 would falsify quotations of earlier selftest states. `OTHER_OCCURRENCES=3` matches my own count (12 total occurrences − 9 bound). |

No disagreement. The Gate quote is 10 words (the wave's draft `words=11` was corrected before landing, Mistakes
row 5).

## Trend verdicts (for MANIFEST)

- **expansion: unchanged** — `corpus/knowledge/` is byte-identical at base and tip (97 `.md`, `git diff` empty);
  registry 218 → 219 with one `mined` row (`S220`) cited by `corpus/evidence/round90/claims.md`, not by a
  knowledge entry, so no admitted entry lands on uncovered ground.
- **quality: improved** — C1 and C3 verified with red-before witnesses re-derived here (the r89 driver's
  substring/overwrite/no-pin shape versus six refused forgery classes; nine 275-cells re-derived to the tool's
  283), the pins and the tally counts re-measured, and QUALITY 196–202 land each citing its own mistake.
  C2's instrument gains are reported and explicitly not admitted; nothing admitted was found false and left
  unmarked.
- **discernment: improved** — the wave fired wording or kill rules on all three claims and the lane narrowed two
  and honest-stopped the third before filing (`PREFILE-FALSIFICATION … findings=0`); six mistakes are mined with
  fixes shown able to fail; this outside spot-check agrees on all four sampled decisions.

## Routed defects (lane must fix next round)

1. **C2 reclaim (Amendment 8).** Count every row in `## Located quotes` (or refuse a non-`Q`/non-3-cell row
   explicitly), cross-check every cited source's `status`/`used-by`, and guard the warrant share with a
   term-frequency test; then a successor C2 claim that names those classes. Already in SCORECARD's round-91 plan.
2. **C1 residues (Amendments 4/9).** Refuse duplicate header keys; bind the instrument bytes a row executes to a
   pin (and have the driver read `instrument-pins.txt`); make `SELF_PIN` name both revisions; add fixtures for
   fresh-divergence and the empty body (M6/M8); repair the `--root`/`--repo` path base (QUALITY 202).
3. **Harm row is a self-comparison (`R90ExecC1Forge` F6).** `expected.tsv`'s `c1-harm` base tool is
   `git show master:tools/gate-records.py`, i.e. the tip tool, so base and head are the same bytes and `moved=0`
   cannot move. Give the sweep a base-versus-head delta that can fail (freeze tool vs landed tool) or register
   `harm-recheck` as a probe, not a harm guard.
4. **Ledger classification.** `.ufo/waves/round-90/claim-falsification.tsv` grades C1/`R90SentinelScope` as
   `neutral`; its F2 (a forged committed body field still prints `CONTROL_DRIVER_R90=PASS`) is the un-narrowed
   (g) and should be `falsifies-wording` → `plans/round-90.md` (Amendments 2/4). Also make the `narrowing` cell
   name the amendment number, not only the file.
5. **Freeze pin defect not recorded in the plan.** At `8d9893b4` all six receipts carried
   `# computed_against=f8fa55ec…`, a revision where the round-89 instruments do not exist
   (`git cat-file -e f8fa55ec:corpus/evidence/round89/curation-r89.py` fails); they were re-emitted at
   `9bad1201`. The re-pin is disclosed in the report, LOG and lesson, but `plans/round-90.md`'s
   pre-freeze list does not record it; the next round should append it as a plan entry so the amendment list is
   complete (report/lesson/LOG are append-only, so the correction goes in, never over, them).
6. **Citation precision in the C1 before-line.** The report's "Before" sentence attaches `FORGERY_REFUSED=0/6` to
   `controls/receipts/c1-prior-driver.txt`, which prints eight `RECEIPT_OK` lines and no `FORGERY_REFUSED` token;
   the value is real but lives in `after/c1-forgeries-landing.txt` (`prior rc=0` ×6). Cite the receipt that
   carries the string.
7. **Clause (a) is per row (`R90ReviewerC1` F5).** With `--repo` a cross-row rewrite is caught post hoc by
   `SELF_PIN`; without it the rewritten receipt is believed. Name this as a limit in the next claim that touches
   the driver rather than leaving it only in a wave report.

Nothing in this list changes the round status: every item is a next-round repair or a status-neutral
conformance/reporting defect.

## Closure verdict

No axis harmed; C1 and C3 verify on their narrowed wording, **C2 does not verify** (frozen K2 fires, honest
stop). Under "admitted only if every claim verifies and no axis is harmed" the lane-round is
`rejected-honest-stop`, lane status `ok`.
