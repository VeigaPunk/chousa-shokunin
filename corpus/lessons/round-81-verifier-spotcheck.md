author: hyaku closure (non-author integrator, @m_zfl)
round: chousa 81
base: 378fda82dc2cbcc555a0565052cc408121813cef
lane_tip_verified: 6ef7929234f5116af79014e371fff6131c588abe
method: committed bytes plus live re-opens. The round's two counting instruments (`depth-r81.py`, `checklist-run.py`) are frozen measurement scripts, not registered gates, and were re-run by this closure on `git archive` trees. Gate verdicts (G02 preflight, census start/end, wave validate) are evidence-verified from committed receipts or re-derived with plain greps; no lane gate or selftest was executed (PROTOCOL §Gate standard, Closure consequence). The two kill-rule firings were reproduced independently on scratch copies of the frozen fixtures.

driver digest (copied from `.ufo/watchdog.log`, mutable):
`2026-11-06T15:39:24-03:00 launch chousa round=81 pgid=1083731 driver=hyaku-inline attempt=1`
`2026-11-06T16:14:10-03:00 complete chousa round=81; hyaku-inline attempt=1`

## 1. Conformance (step 1)

- Report `.ufo/reports/round-81/chousa.md` is committed in the fleet repo by the lane identity `chousa-shokunin <chousa@shokunin.local>` at `f8be544f1391643e539f132467bd06b1e33face3` (2026-11-06 16:13:34 -03). That is after the lane tip and before the driver's complete line (16:14:10). The prompt `.ufo/prompts/chousa-round-81.md` is at `5f452956` (15:39:22, 793 non-empty lines) and carries the template contract: a `SHONEN` duty at line 118 and the hyaku addendum `## 6.` at line 141.
- The `## SHONEN` heading is present, with four `[~]` lines. `SHONEN.md` has four boxes (`grep -c '^- \['` → 4). No `[x]` was written.
- Every cited lane commit exists (`git cat-file -t` → `commit`) and is an ancestor of `refs/heads/master` (`git merge-base --is-ancestor`, branch ref):
  - `f7929f87`
  - `bb54e7f8`
  - `7e2da96a`
  - `b1ed9b6a`
  - `6ef79292`
  - base `378fda82`

  The five round commits carry the lane identity. The range also holds two operator commits (`f7449f91` and `b1061c15`, considerthese 2026-11-05/06). These are operator-authored and are not round work.
- `scripts/hyaku/jj-lane.sh state` → `branch=master local=6ef79292… remote=6ef79292… ahead=0 behind=0 head=detached tracked=0 untracked=0`. `git status --porcelain` is empty. `git ls-remote origin refs/heads/master` → `6ef7929234f5116af79014e371fff6131c588abe`.
- The report is a real report (five landed commits with evidence), not a marker. Status: **ok**.
- Conformance defects (status-neutral):
  - (a) The egress approval table was written after the 18:44:29–31Z fetches. The lane self-disclosed this in the file and in a lesson `## Mistakes` row (`corpus/lessons/round-81.md:176`).
  - (b) The report and lesson state `PREFLIGHT=1/1` for G02 at the final tip, but no receipt for that run is committed. The committed G02 receipts are base `r10` and landing `r09` (FAIL). This closure re-derived the fix with plain greps (§2).

## 2. Per-claim re-check (step 2)

**C1 depth (sourced on S203–S207).** Re-measured by re-running the frozen counter on archived trees. The instrument sha256 at the tip equals the frozen value: `depth-r81.py` `10c989c0…a1e9`, `checklist-run.py` `66ca8c97…bbc2`, `run-controls.sh` `c1942bb9…a65c`. `git diff --stat f7929f87 6ef79292` over the instruments and fixtures is empty.

| rev | command | observed |
|---|---|---|
| 378fda82 | `D=$(mktemp -d -p /fast/scratch/hyaku); git archive <rev> \| tar -x -C "$D"; python3 -B corpus/evidence/round81/depth-r81.py --root "$D"` | `DEPTH_R81 entries=0 fresh_rows=0 located_quotes=0` `DEPTH_R81=FAIL` |
| 7e2da96a | same | `entries=2 fresh_rows=5 located_quotes=14` `DEPTH_R81=PASS` rc 0 |
| 6ef79292 | same | `entries=2 fresh_rows=5 located_quotes=15` `DEPTH_R81=PASS` rc 0 |

Plain counts:
- `git ls-tree --name-only <rev> corpus/knowledge/ | wc -l` gives 92 → 94. `git diff --name-status` shows two `A` entries.
- `grep -cE '^\| S[0-9]{3,} \|' corpus/SOURCES.md` gives 202 → 208.
- Each landed entry name appears in `corpus/README.md` 0 times at `7e2da96a` and 1 time at `6ef79292`. This supports the G02 restoration.

Kill-rule checks:
- **K1 held.**
- **K2 (live re-open) held on my sample.** I re-opened S205, S206 and S207 live: HTTP 200, and the gate quotes were FOUND after tag-strip and whitespace collapse. The S207 quote is 25 words. The wave's 14/14 tally is evidence-verified at `R81ExecReopen/reopen-html.txt:20` (`QUOTE_REOPEN_SUMMARY verbatim=7 absent=0 …`) plus the seat's PDF leg.
- **K3 fired in spirit, and I agree.** At `7e2da96a`, `correction-retraction-status-r81.md:39` told readers to "cite the version read". S206's capture line 222 reads "The citation should be to the most recent version." I re-opened that sentence live today and it is FOUND. The row cites S206, so the cited source contradicts the row. Under the letter of K3 ("located quote"), the located S206 quotes at lines 218/220 do not contradict the row. The lane ruled against itself conservatively, and the repair at `6ef79292:42` follows S206.

The critic's filler control is evidence-verified: `R81CriticClaims/receipts/r09-c1-filler-entries.txt:7-10` reads `entries=2 fresh_rows=4 located_quotes=6` `DEPTH_R81=PASS` rc=0. The counter therefore does not separate depth from filler.

Ruling: **C1 does not verify as an admissible claim** (honest stop). The ground did move: two reviewed, repaired entries now cover topics previously held only inside S120's capture.

**C2 operability.** I re-measured with `python3 -B corpus/evidence/round81/checklist-run.py --root <archived tree>`:
- base: `CHECKLIST_RUN=3/6 DISCRIMINATE=0/3` `CHECKLIST=FAIL` rc 1
- `7e2da96a`: `6/6 3/3` `PASS` rc 0
- `6ef79292`: `6/6 3/3` `PASS` rc 0

K1 held. I then reproduced **K2** myself on scratch copies of the frozen fixtures:
- **Item 4.** In `item4-pass.md`, the R1 flip cell was replaced by `-`. `bash tools/research-gate.sh verify-sweeps <copy> --root .` → `REJECTION id=R1 … flip=present … verdict=match`, `REJECTIONS_OK=1/1`, `RESEARCH_GATE: CLEAN`, rc 0. As a control, `item4-fail.md` → `REJECTIONS_OK=0/1`, `DRIFT`, rc 1.
- **Item 2.** In `item2-pass.md`, the W1 `where` cell was replaced by `n/a`, and the full composite Run line was run → `RESEARCH_GATE: CLEAN`, rc 0.

Both defect forms are named by the item text and pass, so the Run lines do not produce the stated outcome. Ruling: **C2 falsified by K2** (honest stop). Runnable items did rise from 3/6 to 6/6, and the SKILL.md prose now names the pass-through forms (`SKILL.md` items 2 and 4).

**Owned axes not harmed.**
- `git diff --numstat 378fda82 6ef79292` shows zero deletions in any file. SCORECARD, LOG, QUALITY and lesson changes are append-only. The two knowledge entries were edited within this round, and their pre-scoring bytes stay at `7e2da96a`.
- The census `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` exits 0 with five pre-existing W04 warnings (S051/S053/S073/S074/S075), matching `census-start.txt`/`census-end.txt`.
- G02 was red at the landing and is green at the tip (README index greps above).

## 3. Discernment spot-check (step 3) — from `corpus/lessons/round-81.md` `## Gate` (3 admits, 1 reject)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S205 NLM errata policy | admit | `curl -sSL https://www.nlm.nih.gov/bsd/policy/errata.html` → 200 | agree | quote "the erratum notice is simply linked to the citation for the corrected article." FOUND live (13 words); primary PubMed policy grounding the status-check rows |
| S206 ICMJE corrections/version control | admit | `curl -sSL https://www.icmje.org/…/corrections-and-version-control.html` → 200 | agree | quote "The journal should archive all prior versions of the article." FOUND live (10 words); the record honestly notes the landed version row contradicted line 222, also FOUND live |
| S207 Crossref Retraction Watch docs | admit | `curl -sSL https://www.crossref.org/documentation/retrieve-metadata/retraction-watch/` → page | agree | 25-word quote FOUND live and in capture `43a45b49…` (`wc -w` 25, at the bound); the "corrections less comprehensive" scope limit is what the entry teaches |
| S208 BMJ correction q2458 | reject | `curl -sSL https://www.bmj.com/content/387/bmj.q2458.full.txt` → 403 (redirects to `/content/387/bmj.q2458.full`, 403); with a browser UA, `/content/387/bmj.q2458` → 403 | agree | unreachable, reproduced today; rejected as unreachable rather than fabricated, with a flip condition; the entry marks the rec-5 correction as snippet-only inference |

SOURCES.md row re-opened: **S206** (`corpus/SOURCES.md:218`). Its `teaches` cell is a paraphrase ("journals archive prior versions and mark earlier electronic versions as superseded…"). This registry has no quote column, so the row's ≤25-word quote is the `## Gate` record. That quote ("The journal should archive all prior versions of the article.", 10 words) was FOUND in capture `f221c90f…` and live. The S207 gate quote is 25 words and FOUND, which is ≤25.

## 4. Per-axis verdicts (this closure's grades)

| axis | verdict | reason |
|---|---|---|
| depth | unprovable-but-better | knowledge 92 → 94 with 15 located quotes (spot-checked live), but the frozen counter passes filler entries, so the measurement cannot prove depth; claim honest-stopped on K3 (spirit) |
| operability | unprovable-but-better | Run lines 3/6 → 6/6 and fixture discrimination 0/3 → 3/3 re-measured, but K2 reproduced by this closure: the item-2/item-4 lines pass the defect forms the items name |
| calibration | unchanged | r80 routed defects closed append-only (SCORECARD Correction 2, `round-80.md` tail); QUALITY 161–162 name missed controls, no calibration measurement |
| coverage | unchanged | `PROVINCE.md` untouched; README coverage section indexes the two entries |
| freshness | unchanged | no drift surface measured |
| adjacency | unchanged | `R81ConnectorSiblings.md`: no sibling holds either topic; nothing absorbed |

No axis is harmed. Admission: **false** (`rejected-honest-stop`): neither claim verifies, and both were stopped by their own kill rules.

## 5. Trend verdicts

- **expansion: improved.** Knowledge entries went from 92 to 94 and registry rows from 202 to 208, on ground previously held only as a citation inside S120's capture. `R81ConnectorSiblings` shows no sibling overlap. This breaks the r78–r80 `unchanged` streak.
- **quality: unchanged.** Entry defects found by the wave (K3 row; reviewer items 2–5) were repaired after scoring, and the repairs were verified at `6ef79292:42` and in the citation entry's `independent`/snippet lines. Both instruments, however, proved insufficient.
- **discernment: improved.** The lane ruled K3 against itself on its spirit and did not argue the letter. It reported C2 K2 without narrowing, and K2 is reproducible by this closure. S208 was rejected as unreachable rather than taught. QUALITY 161–162 name the missed cheapest-content control.

## 6. Routed defects for the lane's next round (status-neutral; corrections land append-only)

1. Depth counter: `depth-r81.py` passes two 10-line filler entries (`r09`). Before any reuse, a successor needs content conditions, with the filler pair frozen as a fail control (QUALITY 162; SCORECARD r82 plan item 2).
2. Checklist items 2 and 4: `verify-sweeps` treats `-`/`n/a`/`none`/`TBD` flip and reason cells as present and accepts `n/a` sweep locations. Reproduced here. The gate must refuse these forms, with the eleven K2 records as frozen fail controls.
3. Egress ordering: write the approval table before the first fetch, and make the seat row satisfiable as written (`R81SentinelScope` S1–S5).
4. Evidence gap: commit the G02 `PREFLIGHT=1/1` run at the final tip as a receipt. The report and lesson cite its output, but no committed artifact holds it.
5. `R81MutationCounters`: 12/18 (C1) and 9/17 (C2) mutants survive, the P4 shared-quote branch is unexercised, and `PASS` can print beside `5/6`. Fold these into the successor counters' controls.
6. S028 (Crossmark) is still undispositioned.

Operator note: all four SHONEN boxes carry resolvable pointers and remain checkable by a non-author. Promotion is operator-owned and was not touched.
