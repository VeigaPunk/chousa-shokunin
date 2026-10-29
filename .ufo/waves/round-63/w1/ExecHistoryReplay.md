# ExecHistoryReplay — round 63 w1 — history replay through the reference preflight

Reference tool: `corpus/evidence/round63/controls/pos-ref-preflight.py` (unmodified), `--fleet /home/vgpnk/Projects/shokunin --skip G08`,
cwd and TMPDIR in my scratch, `--work` per run. G08 never run (instruction). Nothing written outside my report and scratch (scratch deleted at the end).

## Findings (first)
1. 12/12 commits exported and run; every run exit 1 (never crashed, never ENV): no gate returned ENV and the tool produced a well-formed `PREFLIGHT=` line each time.
2. On the export exactly as specified (`SHONEN.md SCORECARD.md corpus tools` + `.ufo` rounds) **G04 FAILs in 12/12**, every time on `SKILL.md,LOG.md,PROVINCE.md`
   (round-62 commit: only these three, so nothing else is wrong there). Cause: the specified export omits root files SHONEN.md points at. That is
   an **export-scope artifact**, not a historical state (12 FAIL lines, classified neither legacy nor real).
3. To judge the history I re-ran each commit with a second export that adds `SKILL.md LOG.md PROVINCE.md QUALITY.md` (those that exist at the commit); this is the "full-root" basis below.
   On it the round-62 commit reads `PREFLIGHT=7/7 FAILED=none` (exit 0): the tool is clean on the newest state.
4. Full-root basis: 11/12 commits FAIL at least one gate; 32 gate-FAIL lines in all: **27 legacy, 5 real**. Legacy false-alarm rate = 27/32 = 84 % of FAIL lines;
   6 of the 11 failing commits (k3,4,7,9,11,12) fail only on legacy grounds (55 %), 5 (k2,5,6,8,10) carry a real G02 defect.
5. Gate/gate-rule history: G03 (lesson gate heading) and G01 (census, current script run on the old SOURCES.md) and G05 passed at all 12 commits; only G02, G04, G06, G07 ever failed.

## Commit sample (chosen before running: indexes 0,5,10,15,20,25,29,34,39,44,49,54 of the 55 commits in rounds 25-62 of `git log -- corpus/SOURCES.md`; 56 total, index 55 is round 24, excluded)
| k | idx | commit | round | `.ufo` rounds present | specified-export FAILED | full-root FAILED | classification |
|---|---|---|---|---|---|---|---|
| 1 | 0 | c4c11e9 | 62 | (as at golden) | G04 | none | clean; G04 = export artifact |
| 2 | 5 | 1c9626e | 57 | 59-61 absent (r57 predates them) | G02,G04,G06 | G02,G06 | G02 real; G06 legacy |
| 3 | 10 | 6af11e9 | 54 | — | G04,G06 | G06 | G06 legacy |
| 4 | 15 | 4436e27 | 51 | — | G04,G06 | G06 | G06 legacy |
| 5 | 20 | 73ea811 | 48 | — | G02,G04,G06,G07 | G02,G04,G06,G07 | G02 real; G04,G06,G07 legacy |
| 6 | 25 | 5e8c7ad | 45 | — | G02,G04,G06,G07 | G02,G04,G06,G07 | G02 real; rest legacy |
| 7 | 29 | 1bd9001 | 41 | — | G04,G06,G07 | G04,G06,G07 | all legacy |
| 8 | 34 | 7659748 | 36 | — | G02,G04,G06,G07 | G02,G04,G06,G07 | G02 real; rest legacy |
| 9 | 39 | 4c076a0 | 33 | — | G04,G06,G07 | G04,G06,G07 | all legacy |
| 10 | 44 | ee1024f | 31 | — | G02,G04,G06,G07 | G02,G04,G06,G07 | G02 real; rest legacy |
| 11 | 49 | 7c87b97 | 28 | — | G04,G06,G07 | G04,G06,G07 | all legacy |
| 12 | 54 | 0fc037e | 25 | r25 only | G04,G06,G07 | G04,G06,G07 | all legacy |
(The `.ufo` column: I did not tabulate per-commit presence beyond the export ls-tree filter; rounds 59-61 cannot exist before round 59, which is why G06 reads "absent" before r61 regardless.)

## Per-gate adjudication (rule broken then, or rule did not exist yet)
- **G06 freeze-selftest, 11 FAILs, all legacy.** Message `tools/freeze-check.py absent`; the tool was first added by 2edacaf (round 61, 2026-10-28): `git log --diff-filter=A -- tools/freeze-check.py`. No earlier state could have broken a rule about a tool that did not exist.
- **G07 assimilate-selftest, 8 FAILs, all legacy.** `tools/assimilate-rows.py absent`; first added by 6594092 (round 49, 2026-10-25). Commits k5-k12 (rounds 25-48) precede it.
- **G04 shonen-pointers, 8 residual FAILs (k5-k12), all legacy.** The one unresolved word is `round25-meta-differential.log`: SHONEN.md then wrote it as a bare basename shorthand beside a full-path sibling; the file lived at `corpus/evidence/round25-meta-differential.log`. SHONEN.md was changed to the full path by cf642c6 (round 51). No pointer-resolution gate existed at the time; the shorthand is a lexical false alarm of the rule, not a broken file.
- **G02 knowledge-index, 5 FAILs, real.** corpus/README.md has been a "Coverage map" table of `knowledge/…` notes since round 2 (header at 73ea811 and at every sampled commit); the failing commits each carry a knowledge file the map did not yet name (r57 `normative-reference-chain-china-r57.md`, r45/r48 `search-log-method-r39.md`, r36 `engine-swap-canary-r36.md`+`per-record-argv-attribution-r36.md`, r31 `line-binding-r31.md`+`revision-binding-r31.md`). Caveat: this was a convention, not an enforced rule, and the drift was transient, repaired later by the lane itself (r57: README repaired 43 min later in 5dc1860; r31: 2353659 the next commit; r36 in e85ea21; r39 note in 4436e27, i.e. 3-6 commits/rounds later). I class them as real defects of an existing convention (index lag), flagged INFERENCE on severity: the lane's own later repair is the evidence it saw them as defects.

## Evidence pointers
- Driver (python in my scratch, run with `python3 -B` for the tool): `git -C <lane> archive <commit> -- <paths that exist at the commit per ls-tree>` extracted to scratch `h<k>` (specified) and `s<k>` (full-root); per-commit stdout kept in the driver only, summaries above are the printed GATE/PREFLIGHT lines.
- Observed lines (specified basis): k1 `PREFLIGHT=6/7 FAILED=G04 ENV=none SKIPPED=G08`; k2 `4/7 FAILED=G02,G04,G06`; k5 `3/7 FAILED=G02,G04,G06,G07`; k12 `4/7 FAILED=G04,G06,G07`. Full-root k1: `PREFLIGHT=7/7 FAILED=none ENV=none SKIPPED=G08`, exit 0; k2 `5/7 FAILED=G02,G06`; k3,k4 `6/7 FAILED=G06`.
- `git -C lane log --diff-filter=A -- tools/freeze-check.py` -> 2edacaf; `.../assimilate-rows.py` -> 6594092; `log -S'corpus/evidence/round25-meta-differential.log' -- SHONEN.md` -> cf642c6.
- Round-25 log sits at `corpus/evidence/round25-meta-differential.log` in 5e8c7ad and 73ea811 (ls-tree) — the gate's "unresolved" is the bare name only.

## Calibration notes / risks
- Operability: the tool is deterministic and quick on all 12 states; failures name a gate and a precise detail (names the missing README entry, the absent tool, the unresolved word), which made classification mechanical.
- Calibration weakness: run on historical trees, G06/G07 "absent" are FAIL not ENV/SKIP; a gate whose tool the lane does not yet have is a legacy alarm by construction. A lane preflight run on an older export (or a state before r61/r49) will report these. Suggest the L1 note it as a named limit (INFERENCE: an "absent tool" status distinct from FAIL would remove 19 of 27 legacy alarms, but that would change the frozen contract; routed as a supplement, not a change).
- G04's rule counts every backticked basename: SHONEN.md shorthand (no dir) falls out as FAIL; also the lane preflight is root-relative, so an export that omits root files (as the specified export does) fails G04 on those — the export recipe in the item (`SHONEN.md SCORECARD.md corpus tools`) is insufficient for a G04-clean run; `SKILL.md LOG.md PROVINCE.md` are needed.
- G01 ran the *current* census script over old registries and passed everywhere (0 findings); I did not check old censuses against their own era's script, so it is no evidence about G01 historical correctness.
- No labrat used. G08 not run.

VERDICT: COMMITS_RUN=12/12 legacy_alarms=27 real_defects=5
