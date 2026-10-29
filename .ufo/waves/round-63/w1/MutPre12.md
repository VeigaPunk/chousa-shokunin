# MutPre12 — mutation probe of the R63-C1 reference preflight (G01 census, G02 knowledge-index)

Seat: MutPre12 (mutation-tester, leaf). Item: mutate `corpus/evidence/round63/controls/pos-ref-preflight.py` (sha256 prefix `07683086fd6c6b41`, unchanged at the end of the seat), target G01 and G02, run the frozen `corpus/evidence/round63/c1-battery.py` as the only detector.

## Findings

- 24 NEW single-defect mutants (N01–N16, N17–N23, N05b), none of them M01–M16. Each was run through the frozen battery with `--only <named legs>,CLEAN` (`--jobs 2`, `BATTERY=PARTIAL`). Each of the 9 survivors was then run through the full unmodified battery (22 legs, `--skip G08`).
- Result: 15 killed, 9 survived. All 9 survivors also read `BATTERY=PASS` on the full battery.
- Survivors split into 6 control gaps (the battery has no leg that exercises the defect) and 3 equivalents under the battery's predicate (the battery checks ids, statuses and counts, not detail text).
- The battery's D05 leg does catch stem-tolerant index matching (N07, N10). It has no leg for: a case-only README mismatch (N09), a missing README (N11), a missing or unreadable registry (N01, N05), SHOKUNIN_ROOT precedence (N03), or a broken census script in the lane parent (N18).
- Two of my own mutants were broken on first run (N07, N10: `str.stem` applied to names, so the gate crashed and the kill was an artefact). Both were corrected and re-run; the corrected versions are the ones reported. The table below uses the corrected results.
- Each survivor needs a registry or README removed, unreadable or differently cased, or an env/parent-directory condition the battery never sets. How often a real lane hits these is [INFERENCE]; I observed only the mutants and the scratch probes.

## Method and commands (all run; outputs are in `logs/`)
- Mutant generator: `.ufo/waves/round-63/w1/MutPre12/run-mutants.py` (batch 1: N01–N16) and `run-mutants2.py` (batch 2: N05b, N17–N23). Each asserts the anchor occurs exactly once, writes the mutant into scratch, and runs
  `python3 -B corpus/evidence/round63/c1-battery.py --tool <mutant> --fleet /home/vgpnk/Projects/shokunin --work <scratch>/w --jobs 2 --only <legs>`.
- Pristine baseline (`--only CLEAN,D01,...`): `LEG CLEAN clean ok ok`, every named leg `ok`, no failing legs (`logs/run1.log`, `REF_UNCHANGED=True`).
- Survivor full runs (command: `python3 -B <battery> --tool <mutant> --fleet /home/vgpnk/Projects/shokunin --work <w> --jobs 2`), each printed `CLEAN=1/1 DEFECTS=15/15 BENIGN=6/6 BATTERY=PASS`: N01, N02, N03, N05, N09, N11, N12, N18, N22.
- Direct probes (`logs/gapprobe.py`, `logs/gapprobe.log`): each survivor's named defect applied to a scratch copy of `corpus/` (and SHONEN/SCORECARD), reference and mutant run with `--only G01,G02`. Example, G2 (`chmod 000 corpus/SOURCES.md`):
  `ref rc=1 | GATE G01 census FAIL exit=2 gawk: ... Permission denied` ; `N05 rc=0 | GATE G01 census PASS exit=0`.
- Scratch was deleted before yield; mutant bytes are kept in `mutants/` (24 files), logs in `logs/`.
- Tools installed: none. Lane writes: this report and `.ufo/waves/round-63/w1/MutPre12/` only. Frozen paths untouched (`git status --porcelain -- corpus tools SKILL.md` empty).

## Killed mutants (15)

| Mutant | Defect | Killed by (battery legs that fail) |
|---|---|---|
| N04 `script-existence-ignored` | `cands[0]` used without an is_file check | D12 |
| N06 `env-no-exit-2` | ENV collapses to exit 0 | D12 |
| N13 `no-script-is-fail-not-env` | missing census script reported FAIL not ENV | D12 |
| N14 `fleet-flag-ignored` | `--fleet` never consulted | CLEAN, D01 (CLEAN: census not found, ENV) |
| N15 `census-mode-typo` | census run as `census` mode, not `validate` (exit 0 on findings) | D01, D02, D03, D11 |
| N05b `census-exit1-is-pass` | census findings (exit 1) reported PASS | D01, D02, D03, D11 |
| N07 `stem-not-name` (fixed) | G02 matches stem, not file name | D05 |
| N10 `near-miss-stem-accepted` (fixed) | G02 accepts stem as an index mention | D05 |
| N08 `first-missing-dropped` | `[1:]` drops the first unindexed entry | D04, D05, D11 |
| N16 `index-whole-corpus` | README replaced by all of corpus/*.md | D05 |
| N17 `skips-zz-entries` | entries starting `zz` not checked | D04, D11 |
| N19 `only-first-entry` | only the first sorted entry checked | D04, D05, D11 |
| N20 `tautological-index` | `f not in r and f in r` (always empty) | D04, D05, D11 |
| N21 `census-timeout-1s` | census run with a 1 s timeout (census takes ~1.1 s here) | CLEAN (timeout artefact; see limits) |
| N23 `readme-from-fleet-root` | README read from the lane's parent | CLEAN |

Note on N21: the timeout turns every G01 run into `FAIL timeout after 1s`. The defect legs D01–D03 and D11 still pass, because the battery reads only the FAILED set; a timeout is indistinguishable from a census finding. This is a battery limit (it reads ids and statuses, not details), not a kill of the defect.

## Survivors (9)

| Mutant | Defect | Full battery | Class | Battery leg that would kill it (leg not in the frozen battery) |
|---|---|---|---|---|
| N01 `registry-absent-env` | missing SOURCES.md reported ENV, not FAIL | PASS | control gap | a leg that removes `corpus/SOURCES.md`, expects G01 FAIL, rc 1 (probe G1: ref FAIL, N01 ENV rc 2) |
| N02 `registry-absent-check-dropped` | missing-file check removed; census exits 2 and G01 still FAILs | PASS | equivalent (status identical; detail text differs) | none under the predicate (detail not checked; probe G1: both FAIL) |
| N03 `shokunin-root-beats-fleet` | SHOKUNIN_ROOT precedence over `--fleet` | PASS | control gap | a leg that sets SHOKUNIN_ROOT (the battery's minimal env never does) to a script-less dir with a valid `--fleet`, expects G01 PASS (probe G6: ref PASS, N03 ENV rc 2) |
| N05 `census-exit2-treated-pass` | census exit 2 (unreadable registry) reported PASS | PASS | control gap | a leg with `corpus/SOURCES.md` chmod 000, expects G01 FAIL, rc 1 (probe G2: ref FAIL "exit=2 ... Permission denied", N05 PASS) |
| N09 `case-insensitive-index` | README match ignores case | PASS | control gap | a leg that changes one README mention to upper case only, expects G02 FAIL (probe G4: ref FAIL, N09 PASS) |
| N11 `readme-absent-pass` | missing corpus/README.md reported PASS | PASS | control gap | a leg that removes `corpus/README.md`, expects G02 FAIL (probe G3: ref FAIL "corpus/README.md absent", N11 PASS) |
| N12 `count-not-membership` | index check by count, not membership | PASS | equivalent (same pass/fail; detail string differs) | none under the predicate |
| N18 `parent-scripts-beat-fleet` | a census script in the lane's parent beats `--fleet` | PASS | control gap | a benign leg that plants a broken `scripts/sources-census.sh` in the lane parent with a valid `--fleet`, expects G01 PASS (probe G7: ref PASS, N18 FAIL) |
| N22 `census-errors-not-parsed` | census E-lines not read (detail only) | PASS | equivalent (detail text only) | none under the predicate |

N10 and N07 are not survivors: the corrected stem-based mutants are killed by D05. D05 renames the entry and keeps its stem, so a stem-tolerant check passes it while the reference fails it. The leg therefore does cover this class.

## Calibration notes

- My first pass at N07/N10 misjudged the D05 direction ("stem kept, so D05 survives"); the run disproved it. A mutant is killed when a named leg reports FAIL, which includes a leg whose defect the mutant misses.
- N05 was named "census-exit-1-treated-pass" in batch 1, but its bytes are `!= 1` (exit 2 treated as PASS). Batch 2's N05b is the exit-1 case. The table uses the bytes.
- N19 is killed by D05 in 83 of 84 random picks (the miss is caught only when the missing entry is the alphabetically first one). This is stochastic, not deterministic.
- The battery runs G08 never; mutants of G08 were out of scope.

## Limits

- Equivalents are equivalents only under the frozen predicate (ids, statuses, counts). If the battery later checks the detail text, N02, N12 and N22 become killable.
- Each survivor's "would-kill" leg is a proposal. The battery is frozen and I did not add legs; the probes (`logs/gapprobe.log`) show the reference and the mutant disagree on the same defect, so a leg with that defect would separate them.
- One host, one git, no network; no fleet, sibling-lane or shokuknow writes.

VERDICT: KILLED=15/24 survivors_that_are_gaps=6
