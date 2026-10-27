# Round 53 verifier spot-check — chousa

author: hyaku closure (non-author integrator, @m_opus)
date: 2026-10-26
scope: chousa round 53; BASE `5b550133d79bc09c82d8965cce2e48c2598b8c3e` → TIP `d21eb285ea2f7efa17e38d2df4f92588ab23122d` (== `master`, pushed, ahead=0); FREEZE `a6ff732c70011f11c9beb681d832cedc6e75f566`; report `.ufo/reports/round-53/chousa.md`.
Non-author: this file is written by the hyaku closure judge, not the lane. Six read-only reviewer seats re-derived the mechanical checks; the judge re-opened sources itself. No lane tool or frozen counter was executed (PROTOCOL §Gate standard, Closure consequence); gate claims were verified through committed evidence, plain counts were re-measured.

## 1. Step-1 conformance

- Report commit `3ffca1dd70ad72ea88795b98af22258b7edee1c7`, author+committer `chousa-shokunin <chousa@shokunin.local>`, on `origin/main`; `grep -c '^## SHONEN'` = 1 with one `[~]`+pointer line per box. CONFORM.
- Prompt `40da45b48eb1a6ad14a18c14df2f4e64ab5b0e45` committed under lane identity; carries the full round contract (MISSION/AXES binding, 1–3 claims + lowest-axis rule, frontier step, L2 floor, report contract incl. SHONEN heading and hash citation, commit-then-push, push scope, L0 channel). CONFORM.
- All six cited lane commits exist and are ancestors of `master` (`merge-base --is-ancestor` × 6). Lane pushed: `jj-lane.sh state` → `local=remote=d21eb28…, ahead=0`. All round commits authored+committed `chousa-shokunin <chousa@shokunin.local>`; no `.ufo/state/` or `.ufo/watchdog.log` in any commit.
- Working tree: `?? .ufo/waves/round-53/w2/swarm-registry.json` (49,957 B, `ufo-swarm-registry-v1`, wave `chousa-r53-w2`, 43 members) — uncommitted round artifact; its w1 counterpart was committed. Minor conformance defect, status-neutral. `w2.ready.dispatched`, `w2-results.json`, `w2/` seat reports absent from the tree — consistent with the report's disclosed "W2 WAVE-DONE/results had not arrived" limitation (dispatch evidence is committed; results unintegrated).
- Report is a real report, not a marker: work performed, landed-changes table with hashes, before→after with commands, Sources & frontier, trend verdicts, SHONEN.
- `git status --porcelain` on the fleet repo: clean; report and prompt both on `origin/main`.

## 2. Claim re-checks

### R53-C1 — operability (capability: section-10 adopter v4 twin/refusal) — improved (evidence-verified)

Lane-owned gate; per §Gate standard the committed evidence was verified, not executed.

- Frozen counter integrity: `git diff FREEZE..TIP -- corpus/evidence/round53/c1-count.py` empty; sha256 FREESE==TIP `e3aff6bf…`. `claims.md` predicate md5 == `c1-count.py` docstring md5 `1788d543…`. Post-freeze additions only (`c1-supplement.py` = disclosed erratum E1).
- Before: `controls/c1-before.txt` carries 3 unseeded + `SEED=7` blocks each `LEGS=1/8 C1=FAIL` (REGRESS only); controls `CONST 0/8, REFUSE 0/8, RELABEL 5/8 (RECHECK/ORDER/NOENTRY fail), ALLTWIN 2/8` — matches report.
- After: seat receipts `.ufo/waves/round-53/w1/R53ExecSeedRuns.md` record 45/45 runs `LEGS=8/8 C1=PASS` (20 unseeded + seeds incl. 7 + `--per-leg 10` + seeds 21–160 all pass; `/bin/true` → 0/8 non-vacuous), `R53ReviewAdopter.md`/`R53SimplifyAdopter.md` `LEGS=8/8 C1=PASS`, `SELFTEST=PASS findings=40 expected=40`, `FIXTURES_SHA256=9822ad59…` (recomputed equal). Report's "digest" = fixtures digest, not tool-file sha256 (`32628bbc…`) — labeled correctly in SCORECARD:2730, terse in the report.
- v4 diff verified: `held` only for Registry-carried URLs, same-run second row `twin`, `HELD=`/`TWIN=` counts, pre-pass recheck validation incl. held/twin, registry-refusals-before-entry-refusals, `--entry` refusal. `REAL` leg = `CITED=6 APPEND=5 HELD=0 TWIN=1`.
- Limits honestly disclosed: `R53CritForgeC1.md` — 189-line `forge-c1.py` passes 8/8 on six runs while canning REAL and string-stubbing `--selftest`; committed as `controls/forge-c1.py`. `SUPPLEMENT_LEGS=3/3`, forge `1/3` are assertion-only (no standalone receipt) but supplement is post-freeze, not the frozen rule. Frozen claim verifies as declared; forgeability disclosed, not claimed closed → **improved narrowly** stands.

### R53-C2 — depth (sourced: search-record instruments) — improved (re-measured + evidence-verified)

Re-measured over committed bytes at TIP:

- `ENTRIES=3/3`: three knowledge entries exist at TIP, all new since BASE; each carries `source: S### — <url>` only for bound ids; zero unbound `S###` tokens.
- `BOUND=4/5`: rows S117–S120 present exactly once each, 11 cells, `mined`, `opened 2026-10-26`, valid recheck (`365d`/`180d`), `used-by` paths all resolve; first-URL per row matches the renumbered staged document (S134→S117 JMLA, S185→S118 bjhea PDF, S186→S119 notice, S193→S120 Cochrane ch.4; S195 byte-identical URL → twin of S118, one row).
- `REFUSED=1`: `grep -c S190` on TIP registry = 0; `refused-doc` line in lesson names the pharmwyp URL; original NMPA capture is `.fail rc=22`.
- `QUOTE_ROWS=63`: `spans.tsv` 64 lines incl. header; 7 columns uniform; per-id S117=27/S118=22/S119=6/S120=8 (≥3 each); quote field max 17 words ≤25, max 119 chars ≤160, 0 violations; 63 unique span files all present → `CAPTURE_BOUND=63/63` consistent.
- `INFERENCE_GROUNDED=3/3` + `QUARANTINE_VERDICTS=0/0`: recorded in LOG.md:1848/SCORECARD.md:2713; quarantine independently re-derived — 24 chousa data rows, 0 theme-URL rows over all 325 register rows (grep jmla|cochrane|bjhea|nmpa|pharmwyp = 0). `ANCHOR_BOUND=4/4` consistent with 4 bound ids carrying `char N` anchors at located quote offsets.
- Controls fail as designed: `controls/c2-before.txt` `ENTRIES=0/3 BOUND=0/5 C2=FAIL`; `c2-controls.txt` STAGED `REF_ID_UNBOUND=12` and TOOLED `BOUND=5/5 REF_ID_UNBOUND=4 ANCHOR_BOUND=0/5 C2=FAIL`.
- Erratum E4 verified: CJK polarity patch to `inference-ground.py` post-freeze, disclosed, C2 passes on both base and landed tool ("only adds findings"); fixture red-before 2/6 → landed 6/6 recorded in QUALITY 95/erratum.
- Caveat: no dedicated `measure-after.txt` receipt file this round (after-values live in LOG.md/SCORECARD.md, identical text); several receipts embedded as quoted text rather than standalone files. Minor.

### Axis-harm check

`git diff BASE TIP -- SCORECARD.md` = 44 insertions, 0 deletions — pure append; no axis row decreased. `SHONEN.md` unchanged. `QUALITY.md` +12/−0 (rows 91–96 appended). `LOG.md` append-only, each round-53 entry cites a commit/evidence pointer. `considerthese/` untouched (operator input). `corpus/SOURCES.md` diff = exactly 4 appended rows, no existing row modified. **No axis harmed.**

## 3. Per-axis verdicts

| axis | verdict | evidence |
|---|---|---|
| operability | improved | C1 evidence above; capability row landed with selftest digest |
| depth | improved | C2 re-measured above |
| coverage | improved | corpus/README coverage-map rows for the three entries; new surface (search-record instruments) on ground not held at BASE |
| freshness | unchanged | no re-verification claim beyond this round's material |
| calibration | improved | 7 anchored append-only `correction:` lines (`ANCHORED=7/7`); forgeability/vacuous-leg disclosures; stale erratum ranges corrected by supersession pointers |
| adjacency | unchanged | sibling/shokuknow material handled read-only; contested scope correctly refused, not absorbed |

## 4. Discernment spot-check (non-author re-open; capture cache `shokuknow/.ufo/waves/corpus-expansion-1/.qcache`, no fetch)

| item | decision | re-opened source | verdict | reason |
|---|---|---|---|---|
| S117 admit (JMLA tracking-record paper) | lane admitted | `0ae65ac0….txt` len 27,659 chars; quote `reporting the number of records identified from each information source.` once @1320; joined staged sentence `should be reported in Column 2` count 0 | **agree** | located quote unique; staged interleaved string confirmed absent — the re-cut was warranted |
| western-instrument admit (S120 Cochrane + S118 guideline) | lane admitted, narrowed | `c9d1e74c….txt` len 210,708, quote once @13480; `16fe8487….txt` len 27,609, `PRISMA` count 0 | **agree** | both binding quotes verify; narrowing (PRISMA absent from guideline) is the conservative, correct call |
| S118 row quote | new SOURCES row | `16fe8487….txt` @10360 `数据库应包括多个中、英文专业数据库。` | **agree** | quote present verbatim at the recorded offset, ≤25 words |
| S119 row quote | new SOURCES row | `cfa080b4….txt` @517 `发布时间：2025年01月03日 来源：国家卫生健康委卫生发展研究中心` | **agree** | present verbatim at offset, ≤25 words |
| S190 reject (NMPA blog print) | lane refused document | cache key `b5c2c7c8…` = `.fail` containing `rc=22`, sole file for the key; `grep S190` on registry = 0; no entry cites it | **agree** | tier-C third-party print, original uncapturable; refusal with flip condition is calibrated |
| search-log-fields-r36 reject (3rd time) | lane refused | `01f657b3….txt` = 267-byte "Client Challenge" page | **agree** | source still unreadable; sustained refusal is discernment, not stubbornness — flip condition is checkable |

Census (run by judge): `sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` → exit 0, `ok`, five pre-existing W04 (S051, S053, S073, S074, S075 — duplicate-url warnings carried from before the round).

## 5. Trend verdicts

- **expansion — improved.** 116→120 rows; four unique documents absent at BASE (`git grep` = 0 per URL); all bound, `mined`, citing admitted entries; twin counted once; S190 refused without credit.
- **quality — improved.** Entries re-grounded to located spans (63 quotes ≤25 words), CJK polarity blind spot fixed red-before→green, QUALITY 91–96 lesson-backed, append-only corrections with anchors; no admitted entry found false.
- **discernment — improved.** Non-author re-open agrees on 2 admits + 2 rejects + 2 row quotes; rejections carry checkable flip conditions. The round-52 disagreement was folded into this round's corrected scope decision (grey-literature "out of province" reason withdrawn with evidence).

## 6. Routed defects / carried items for round 54

1. `.ufo/waves/round-53/w2/swarm-registry.json` uncommitted at lane HEAD — commit or record why runtime registries stay untracked (w1's counterpart was committed).
2. W2 (43 seats) dispatched but `WAVE-DONE`/results never arrived before the wrap directive — land `w2-results.json` + seat outcomes next round or record the seats dead with evidence; no falsification credit was taken, correctly.
3. Receipt discipline: commit standalone run receipts (a `measure-after.txt` for the frozen counters, the supplement and forge runs) rather than embedding output only in LOG/SCORECARD/lesson prose — `SUPPLEMENT_LEGS=3/3` and forge `1/3` are assertion-only this round.
4. Report label: the C1 "digest `9822ad59…`" is the selftest `FIXTURES_SHA256` (correctly labeled in SCORECARD:2730), not the tool-file sha256 (`32628bbc…`) — say which in the report.
5. Carried: five pre-existing W04 duplicate-url warnings (S051/S053/S073/S074/S075) remain un-adjudicated registry debt.
6. Frozen-counter forgeability streak (RW-1, 5 rounds): exposure recorded; a forged REAL leg still passes — schedule the supplement-leg promotion or a REAL-leg hardening in a future frozen predicate.

## 7. Note for the operator

The four SHONEN boxes carry `[~]` self-assertions with resolvable pointers and look fully checkable by a non-author (SKILL gate rows + QUALITY 91–96, logged end-to-end round, executable commands, PROVINCE fit with refused-document records). Promotion review is operator-owned; this round's evidence supports scheduling one.
