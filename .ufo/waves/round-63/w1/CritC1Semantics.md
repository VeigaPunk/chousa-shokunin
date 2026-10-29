# CritC1Semantics — does each G01–G08 gate catch a defect this lane really had?

Seat: CritC1Semantics (critic, item CritC1Semantics). Read-only git and `git archive` into scratch; no lane, tool or control file was edited; no commit, index or fleet write. Scratch `/fast/scratch/hyaku/chousa-r63/CritC1Semantics/` removed before yield.

## Method

1. `git log --oneline -- corpus/SOURCES.md corpus/README.md corpus/lessons SHONEN.md SCORECARD.md` (lane HEAD `c8bfcc6`); `git log -S` on each named string to find the introducing and fixing commit.
2. For each defect: `git archive <commit> | tar -x -C <scratch>/a/<commit>`, then the reference tool, e.g.
   `python3 -B corpus/evidence/round63/controls/pos-ref-preflight.py --root <archive> --fleet /home/vgpnk/Projects/shokunin --work <scratch>/w/<commit> --only G02,G04`.
   Where the defect is a selftest gap I ran the gate's own selftest command at that commit (G07, G08) and, for G07, a mutant copy of the fixture.
3. Caveat on history: tools that did not yet exist at an old commit make G06/G07/G08 print `FAIL tools/... absent` (or `exit=2`). I read those as tool-history noise, not detection; they are listed as such.

## Verdicts by gate (what each one actually saw in this history)

| gate | fired on a real defect? | note |
|---|---|---|
| G01 census | no | PASS at all sampled commits; no sampled defect used it |
| G02 knowledge-index | **yes, twice** | unindexed `search-log-method-r39.md` (1254ab2–cf642c6), `long-span-argv-r34.md` (98af778) |
| G03 lesson-gate | no | checks the heading `## Gate` exists, not its content (row 13) |
| G04 shonen-pointers | **yes** | dangling `round25-meta-differential.log` in SHONEN.md, 0fc037e–2a3389d |
| G05 scorecard-paths | no | PASS at every sampled commit; prefix rule skips `measure/final/` (row 12) |
| G06 freeze-selftest | **yes, conditional** | 2a5029e: selftest reads an uncommitted wave file (row 4) |
| G07 assimilate-selftest | no (incidental only) | PASS on the vacuous selftest; FAIL exit=2 only because no selftest existed (rows 5–7) |
| G08 gate-selftest | no | PASS on the chunk-path gap; env pin hides the LC_ALL=C dependence (rows 8–9) |

## Table: defective commit, defect, gate that fires or NONE

Source column: where the defect is named. "lesson" = a `## Mistakes`/spot-check row or the lesson's own text; "unnamed" = a real defect by the gate's own rule, named nowhere.

| # | commit | defect | source | gate that fires, or NONE | evidence (command → observed) |
|---|---|---|---|---|---|
| 1 | 0fc037e (string introduced; d8c8cff rewrites SHONEN) | SHONEN.md:10 pointer `corpus/evidence/round25-meta-differential.log` does not exist | lesson round-51-verifier-spotcheck §4–5 | **G04 fires** | archive 0fc037e, d8c8cff, beb04ea, bf7c931: `GATE G04 shonen-pointers FAIL 1 unresolved: round25-meta-differential.log`; cf642c6: `PASS 10 pointers resolve` |
| 2 | 1254ab2 (file since r39; README row added 4436e27) | `corpus/knowledge/search-log-method-r39.md` not named in corpus/README.md | unnamed | **G02 fires** | 1254ab2, 671b096, ec52e63, 2573dc1, 4ce61fc, 1d7aba0, 2a3389d, cf642c6: `FAIL 1 not named in corpus/README.md: search-log-method-r39.md`; 2a5029e: `PASS 83 entries indexed` |
| 3 | 98af778 (README row added bf7c931) | `corpus/knowledge/long-span-argv-r34.md` not in README | unnamed | **G02 fires** | 98af778: `FAIL … long-span-argv-r34.md`; bf7c931: `PASS 40 entries indexed` |
| 4 | 2a5029e (round-61 landing; wave file tracked only from b6c1d0e) | freeze-check selftest reads `.ufo/waves/round-61/w1.ready`, absent from the committed tree | unnamed | **G06 fires on a clean tree only** | archive 2a5029e: `GATE G06 freeze-selftest FAIL exit=1`; traceback `FileNotFoundError … round-61/w1.ready`; `git log -- .ufo/waves/round-61/w1.ready` → first commit b6c1d0e. The live file exists (dated before 2a5029e) and is tracked now, so a live-tree run would have passed (INFERENCE) |
| 5 | ec52e63 (fixed 2573dc1) | `--selftest` compares findings as sets (`tools/assimilate-rows.py:220`); a duplicated expected line passes | lesson round-50 Mistakes ("vacuous") | **NONE** (G07 PASS) | mutant: expected.json with `ROWSTATUS S013 mined` duplicated. ec52e63: `SELFTEST=PASS findings=26 expected=27`, rc 0. 2573dc1, same mutant: `DIFF missing ROWSTATUS S013 mined`, `SELFTEST=FAIL`, rc 1. G07 at ec52e63: `PASS exit=0` |
| 6 | 4ce61fc (tab headings, calendar-invalid dates, non-UTF-8 refusal) | three tool defects with no test; no `--selftest` option exists yet | commit message (W1 ReviewToolCode) | G07 FAILs, **for absence only** | `python3 -B tools/assimilate-rows.py --selftest` at 4ce61fc → rc 2; `grep -c selftest` → 0. G07 would fail at any pre-ec52e63 commit whatever the defect |
| 7 | 1d7aba0 (round-50 tip; still accepted at 4436e27) | registry without `## Registry` heading accepted; ids restart at S001 over existing rows | round-51-verifier-spotcheck line 34 | **NONE** (G07 PASS) | fixture registry with heading renamed to `## Table`: 1d7aba0 `COLLISIONS=2`, rc 0; 2573dc1, cf642c6, 4436e27 identical; HEAD `REFUSED registry rows outside the Registry section …`, rc 1. 1d7aba0 selftest: 0 heading-related strings; G07 `PASS exit=0` |
| 8 | 3026a4e (chunk matcher shipped; cases 252–253 use the direct path only; fixed by fe0f22e cases 254–256) | chunk-path matcher has no selftest case | lesson round-34 Mistakes row 1 | **NONE** (G08 PASS) | `LC_ALL=C.UTF-8 bash tools/research-gate.sh --selftest` at 3026a4e → `RESEARCH_GATE_SELFTEST: PASS (253 cases, 0 skipped)`, rc 0 |
| 9 | 3026a4e (LC_ALL=C dependence: `\u2192` decoded only in a UTF-8 locale; fixed before HEAD) | the gate's selftest fails under the lane's own `LC_ALL=C` | lesson round-34 ("ONE byte") | **NONE — masked by the preflight env pin** (`pos-ref-preflight.py:200` sets `LC_ALL="C.UTF-8"`) | same tree, `LC_ALL=C`: `RESEARCH_GATE_SELFTEST: FAIL (10/253 cases)`, rc 1 (claims-pass, all-pass.md, json-unterminated-manifest, …). Preflight's env: PASS 253. HEAD under `LC_ALL=C`: `PASS (275 cases)`, rc 0 (the defect is fixed; G08 under the preflight env at HEAD not run, ~11 min) |
| 10 | 671b096 | `corpus/QUALITY.md` criterion 69 cites "`round-48.md` Mistake 4"; that table has no 4th numbered row | lesson round-49 Mistakes row 3 | **NONE** (by construction) | `grep -n 'QUALITY\|LOG.md\|SKILL\|evidence/README' controls/pos-ref-preflight.py` → no output; G01–G05 at 671b096 fail only G02/G04 |
| 11 | 1254ab2 (QUALITY.md:746, README:1074, LOG) | stale count `QUOTES=28` after the manifest grew to 31 | lesson round-50 Mistakes row 1 | **NONE** | no count gate; at 1254ab2 G01, G03, G05 PASS (`PASS 27 lessons`, `PASS 56 capability pointers`), G02/G04 fail on other rows |
| 12 | aa47206 (round-32 capability row cites `measure/final/`); dangling at 1d7aba0 | SCORECARD.md:1843 evidence cell `` `measure/final/` `` names a directory absent from the root | lesson round-51-verifier-spotcheck §4 | **NONE** | 1d7aba0: `GATE G05 scorecard-paths PASS 60 capability pointers resolve`; the token rule (line 137) accepts only `corpus/`, `tools/`, `.ufo/` prefixes, so `measure/final/` is never read. `ls <archive>/measure` absent |
| 13 | beb04ea (first commit of round-35 lesson) | lesson `## Gate` has no reject rows (the spot-check's "conformance defect") | round-35-verifier-spotcheck line 111 | **NONE** | beb04ea: `GATE G03 lesson-gate PASS 13 lessons carry ## Gate`; `grep -ci reject corpus/lessons/round-35.md` → 0. G03 tests a heading line only |
| 14 | 2a5029e (SKILL.md gates landed) | SKILL.md carries unresolved path pointers (the round-61 lesson counts 6) | lesson round-61 line 75 | **NONE** (no gate reads SKILL.md) | applying G04's own word rule to SKILL.md at 2a5029e (read-only import of the tool) → 1054 pointers, 551 unresolved, e.g. `Q.tsv`, `LEGS=20/20`, `RESOLVED_HOPS=17/22`: the rule does not transfer to SKILL.md as written |
| 15 | 0fc037e and d8c8cff (round-25) | `corpus/evidence/README.md` not carried in the commit (blob unchanged) | lesson round-25 (after R25-M5) | **NONE** | no gate reads `corpus/evidence/README.md` (grep, as row 10) |

Sampled commits with no defect: G01 census never failed; G05 never failed. The G06/G07/G08 PASSes at ec52e63, 1d7aba0 and 3026a4e are the selftests that rows 5, 7 and 8 show to be blind.

## What this means for the gate set

- **Calibration of G02 and G04 is good on the defects the lane had.** Both fire on real, unnamed or lesson-named index and pointer defects, and both went green when the defect was fixed (cf642c6 for G04; 4436e27 and bf7c931 for G02, by git log -S of the README row).
- **G07 and G08 test the selftest's existence, not its coverage.** Three real selftest defects (rows 5, 7, 8) pass both gates. A selftest-gate that says PASS is evidence that the tool's own cases pass, not that the cases are adequate; the lane's own lessons show that gap recurring (rounds 34, 50, 51).
- **G08's env pin is a calibration defect.** The preflight forces `LC_ALL=C.UTF-8`, so the one gate that runs the most fragile code is blind to the locale class the lane found in round 34 (row 9). INFERENCE: running the gate under the operator's own locale would have shown it; the preflight does not offer that.
- **Scope gaps are by construction.** No gate reads `corpus/QUALITY.md`, `LOG.md`, `SKILL.md`, `corpus/evidence/README.md`, numeric restatements, or lesson content (rows 10–15). Those were the defect classes most often named in the lesson Mistakes tables (rounds 49–51).
- **G06 depends on the tree, not on the commit.** Row 4 fires only on a clean archive. The live preflight reads the working tree, so an uncommitted wave file keeps G06 green. Named as a limit: the gate does not check that the lane's selftests run from the committed bytes.
- **G05's prefix rule is narrower than the lane's own pointer style.** `measure/final/` (row 12) is a lane-relative pointer the gate never sees.

## Limits of this seat's evidence

- About twenty commits were archived and run; the list is the set of defects the lane named or that `git log -S` located. It is not a census of all defects.
- G08 was run by hand at 3026a4e (both locales) and at HEAD under `LC_ALL=C` only (about 11 min). G08 at HEAD under the preflight env was not run.
- Row 2's "unnamed" status is by the gate's own rule; no lesson names that file. Row 4's "fires" is conditional on the clean tree (see above).
- The 551 SKILL.md hits (row 14) show the G04 token rule is noisy on non-path tokens; I did not tune a SKILL rule.
- Commit-level fix dates come from `git log -S` (the commit that added or removed the string); they are not a bisect.

## Commands and receipts (scratch removed afterwards)

- `git log --oneline -- corpus/SOURCES.md corpus/README.md corpus/lessons SHONEN.md SCORECARD.md` (lane HEAD `c8bfcc6`).
- `python3 -B corpus/evidence/round63/controls/pos-ref-preflight.py --root <archive> --fleet /home/vgpnk/Projects/shokunin --work <scratch> [--skip G08|--only …]` over the archives listed in the table; outputs quoted above.
- `research-gate.sh --selftest` at 3026a4e (`LC_ALL=C.UTF-8`: PASS 253; `LC_ALL=C`: FAIL 10/253) and at HEAD (`LC_ALL=C`: PASS 275).
- `assimilate-rows.py --selftest` at ec52e63 / 2573dc1 with the duplicate-line mutant; heading-less registry repro at 1d7aba0, 2573dc1, cf642c6, 4436e27, HEAD.
- Read-only lane gates at HEAD: `--only G01,G02,G03,G04,G05` → `PREFLIGHT=5/5 FAILED=none`. G06 and G07 at HEAD (archive): `PASS exit=0` each.

Tools installed or upgraded by this seat: none.

VERDICT: REAL_DEFECTS_CAUGHT=4/15 uncaught_classes=[vacuous-set-comparison-selftest, selftest-case-gaps-chunk-and-registry-heading, locale-env-pin-masks-LC_ALL=C, stale-numeric-restatements, QUALITY.md-criterion-pointers, SCORECARD-unprefixed-pointers, SKILL.md-and-evidence-README-unread, lesson-gate-section-content]
