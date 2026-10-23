# RevReportCounts — round-36 wave/report/receipt/source counts

Seat: `L1chousa36.RevReportCounts-2` (residual reviewer/critic, read-only).
All paths relative to lane root `/home/vgpnk/Projects/shokunin/chousa-shokunin`.
Measured ~2026-10-23T21:35–21:40Z. **The wave is still landing** (reports went 32 → 34
during measurement); every number below is a snapshot at the stated time.

## 1. Wave seats vs reports on disk

| Metric | Command | Observed |
|---|---|---|
| Dispatched seats | `python3 -c "import json;print(len(json.load(open('.ufo/waves/round-36/w1-dispatch.json'))['registry']['members']))"` | **36** (`counts.total` also 36, `spawn` 36, `resume` 0) |
| Reports on disk | `ls .ufo/waves/round-36/w1/*.md \| wc -l` | **34** @21:40Z (33 @21:34, 32 @21:30 — live arrivals; will read 35 after this report file lands) |
| Dispatched seats with NO report | `comm -23 <(dispatch members) <(ls w1/*.md \| sed 's\|.*/\|\|;s\|\.md$||' \| sort)` | **ConnOverlap, CritC1Swap** |
| Report files with no dispatch entry | same `comm`, reversed | none |
| Seats with no `w1/<Seat>/` dir | `ls` + `find w1 -mindepth 1 -type d` | **CritC1Swap has no dir at all** — consistent with SCORECARD's "dead seat (`CritC1Swap`, provider `cyber_policy` refusal)". `ConnOverlap/` exists but is empty @21:40 (seat still in flight or dead-with-empty-dir; no registry field records a cause — `agentId` is `null` for all 36 members in `w1-dispatch.json` and `w1/swarm-registry.json`). `CritC2CallForShow/` had receipts + `CritC2CallForShow.md` by 21:39. |

Role histogram (dispatch `members[].role`): scout 5, executor 15, reviewer 4, critic 2,
mutation-tester 2, sentinel 1, simplifier 1, connector 1, scribe 5.
rev+crit+mut+sent+simp = **10/36 = 27.8%** — matches SCORECARD "attack roles 10 = 28%".

## 2. Receipts

| Metric | Command | Observed |
|---|---|---|
| Committed construction receipts | `ls .ufo/waves/round-36/measure/*.json \| wc -l` | **8** — c1-after-s36001/36011, c1-before-s36001, c2-after-s36001/36011, c2-before-legacy-s36001, c2-stubfail-s36001, c2-stubpass-s36001 |
| L1 re-derivation receipts | `ls .ufo/waves/round-36/measure-l1/*.json \| wc -l` | **2** — c1-s36361 (14/14, holds), c2-s36371 (5/5, holds) |
| Seat receipts | `ls .ufo/waves/round-36/w1/*/*.json \| wc -l` | **42** @21:40Z (41 @21:34; CritC2CallForShow wrote `c2-s36321-committed.json` during measurement — rising) |
| — of which counter-shaped (label/matched/total/holds) | same glob filtered to `w1/*/c?-*.json` | 24 files; one (`CritC2CallForShow/c2-s36331-variants.json`) is a variants table, not a receipt |
| — with `predicate_holds=false` | python json scan of `w1/*/c?-*.json` | `RevCounterHonesty/c1-forshow-s36341` (`ENGINE_SWAP_CANARY=error`), `c1-forshow2-s36361` (`error`), `c1-pinnaming-s36351` (12/14); `ExecC1BaseCtl/c1-before-s36321` (10/14, expected — before-state); `ExecC2LegacyCtl/c2-before-legacy-s36321` (2/5, expected) |
| — with `predicate_holds=true` 14/14 or 5/5 | same scan | C1 14/14 on seeds 36301, 36311, 36321 (comment-patched gate), 36331, 36361 (L1), 36371 (call-for-show gate, by design per erratum 9); C2 5/5 on 36301, 36311, 36321, 36331, 36371 (L1) |

Per-seat receipt counts (`for d in w1/*/; do ls "$d"*.json | wc -l; done`):
MutC1Arm 12, RevCounterHonesty 7, SimpDiff 3, RevLocaleSeam 2, RevClaimPredicate 2,
LabScenarioIsolation 2, ExecWitnessDirect 2, CritC2CallForShow 2→3 (live); 1 each for
ScoutReceipts, ScoutC1Counter, ExecC1BaseCtl, ExecC1FreshA/B, ExecC1ScenarioMap,
ExecC2FreshA/B, ExecC2LegacyCtl; 0 for all scribe/sentinel/reviewer-remaining/scout-remaining seats.

## 3. SOURCES census

| Metric | Command | Observed |
|---|---|---|
| S-rows | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | **70** (first S001, last S070; S069 and S070 present, both `docs`/`A`/`mined`) |
| Frozen contract-v1 census | `bash corpus/evidence/round25-sources-census.sh` (read-only, exit 0) | `rows=70 malformed=0 tiers=A=64 B=1 C=5 status=mined=47 queued=19 rejected=4 duplicates=[] enum=[] missing-used-by=[]` |
| Canonical validator | `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` | exit **0**, `chousa ok`, exactly two W04 warnings: **S051** (w3.org html52 duplicate URL) and **S053** (docs.python.org socket.html duplicate URL) |
| Type histogram (col 3) | python parse | docs 28, spec 20, paper 11, own-work 9, community 2 |
| Recheck histogram (col 10) | python parse | on-release 33, 365d 30, 90d 4, 180d 3 |

## 4. Agreement check vs `corpus/lessons/round-36.md` §Gate and `SCORECARD.md` §Round 36

Matches:
- §Gate "S069, S070 (68 → 70 rows)" — 70 measured, delta consistent. ✔
- §Gate "census `validate` exit 0 with the two standing W04 warnings for S051/S053" — reproduced verbatim, exit 0. ✔
- §Gate "Status / recheck / used-by changes: none in place… enter `mined`" — S069/S070 rows are `mined`; histogram shape consistent (tier-inflation check clean, enum clean). ✔
- §Mistakes row "the wave-1 brief said the measure directory holds 11 committed receipts; w1/ScoutReceipts.md counts 8" — **8 measured**; the lesson's self-correction is accurate. ✔
- Lesson "wave 1 (36 seats)", "L1 re-derived C1 14/14 on seed 36361 and C2 5/5 on seed 36371" — dispatch 36; `measure-l1/c1-s36361.json` (14/14, holds) and `c2-s36371.json` (5/5, holds) measured. ✔
- Lesson "no-harm battery held (claims 17/17, chain 17/22, broken control 1/2, archives 3/3)" and "selftest passed 261 cases" — `SentNoHarm.md`/`ExecSelftest.md` contain those numbers. ✔
- SCORECARD "one v1 wave, 36 seats (attack roles 10 = 28%)" — 36 dispatched; 10/36 = 27.8%. ✔
- SCORECARD "one dead seat (`CritC1Swap`, provider `cyber_policy` refusal, not retried)" — CritC1Swap is the only dispatched seat with neither report nor seat directory. ✔
- SCORECARD "Sources 68 → 70 rows", "QUALITY 50-52 added" — 70 rows measured; QUALITY rows 50/51/52 exist at `corpus/QUALITY.md:399,410,420`. ✔
- SCORECARD C1 "before `ENGINE_SWAP_CANARY=10/14` (base gate… re-derived seed 36321 by `w1/ExecC1BaseCtl`)" and C2 "`2/5` before… re-derived seed 36321 by `w1/ExecC2LegacyCtl`" — `w1/ExecC1BaseCtl/c1-before-s36321.json` 10/14 holds=false; `w1/ExecC2LegacyCtl/c2-before-legacy-s36321.json` 2/5 holds=false. ✔

Mismatches / inaccuracies:
- **M1 — SCORECARD "§Erratum appended after the data, 6 entries"** vs `corpus/evidence/round36/claims.md` §Erratum numbered **1–13** (verified lines 157–228; entries referenced by other seats: 7 BASH_ENV, 8 prefix-64, 9 call-for-show, 13 locale seam). Count disagreement: written 6, actual 13. Likely a stale count drafted before the erratum grew [INFERENCE]; the text says "appended", not a frozen count.
- **M2 — SCORECARD/lesson C1 seed enumerations are not receipt-accurate.** SCORECARD "after 14/14 on seeds … 36301/36311/36331/36341/36351/36361 (wave + L1)": `c1-forshow-s36341.json` is `ENGINE_SWAP_CANARY=error` (holds=false), `c1-pinnaming-s36351.json` is 12/14 (holds=false), and the s36361 wave receipt is `c1-forshow2-s36361.json` = `error`; the only 14/14 on 36361 is the L1's `measure-l1/c1-s36361.json`. Lesson "after 14/14 on seeds 36001/36011 (construction) and 36301/36311/36361 (wave + L1)" is accurate but omits 36331 (wave 14/14) and 36371 (wave call-for-show gate 14/14, by design). As exhaustive lists both statements are wrong; read as "(examples incl.)" the lesson is fine and SCORECARD still lists 36341/36351/36361 which are not 14/14 wave receipts.
- **M3 — report-count framing.** SCORECARD "one dead seat" is accurate for *dead* seats, but at measurement time **two** dispatched seats had no report on disk (ConnOverlap, CritC1Swap); a "36 seats → 36 reports" citation needs the live-wave caveat. ConnOverlap left an empty dir; if it never lands, dead seats = 2.
- **M4 (minor)** — dispatch/lesson "wave-1 brief said 11 committed receipts" vs measured **8**: already self-reported in the lesson's §Mistakes; no residual error, recorded for completeness.

## Residual risk / verification gaps

- Counts drift during the wave (32→34 reports, 41→42 receipts within minutes). Any round-level
  sentence citing report/receipt counts must either name its snapshot time or re-measure at
  closure. `w1/*.md | wc -l` after this file lands will read 35 by construction.
- `swarm-registry.json`/`w1-dispatch.json` carry no per-seat status (`agentId: null` for all 36),
  so "dead" vs "still in flight" for ConnOverlap cannot be decided from lane files alone.
- `w1/*/c?-*.json` glob misses receipts not named `c1-*`/`c2-*` (e.g. MutC2AttrKey's
  `rec-prefix-s*.json` cited in erratum 8 live under `w1/MutC2AttrKey/art/`), so the 42-file
  seat-receipt count is a superset (includes non-receipt JSON like the variants table) AND the
  c?-subset an undercount of witness receipts.
- No tool installs this run; all commands above were read-only; nothing under tools/, corpus/,
  SCORECARD.md, LOG.md, SKILL.md, claims.md was modified.
