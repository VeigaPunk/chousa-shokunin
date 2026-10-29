# RevFreezeCheck — round 62 w1 freeze check (reviewer)

Lane: /home/vgpnk/Projects/shokunin/chousa-shokunin. Lane HEAD d173d144bbf55403d091115b5a6ec73a721dd95c.
Read-only. No writes outside this report and scratch (/fast/scratch/hyaku/chousa-r62/RevFreezeCheck, deleted before yield).

## 1. Findings

**F1. Freeze check PASS.** Command:
`python3 -B tools/freeze-check.py --claims corpus/evidence/round62/claims.md --dispatch .ufo/waves/round-62/w1-dispatch.json --spec .ufo/waves/round-62/w1-spec.json --ready .ufo/waves/round-62/w1.ready` (exit 0). Output, verbatim:
```
CHECK CLAIMS_NONEMPTY PASS 10594 bytes sha256=a3193ebd328919e2af017011278e423c5940fd9447f0730bd400da9d15c866bc
CHECK CONTEXT_DIGEST PASS context carries a3193ebd328919e2af017011278e423c5940fd9447f0730bd400da9d15c866bc
CHECK CONTEXT_SPEC_EQ PASS identical (3613 chars)
CHECK DIGEST_STRAY PASS no 64-hex token other than the claims digest
CHECK NAMES PASS 66 names match in order, roles match agents
CHECK BODY_RENDER PASS 66/66 dispatch tasks equal the rendered spec items
CHECK READY_DISPATCH PASS ready -> .../w1-dispatch.json
CHECK READY_IDENT PASS lane=chousa round=62 wave=w1 agree with dispatch, spec and location
FAILED_CHECKS=none
FREEZE_CHECK=PASS
```
The claims digest `sha256sum corpus/evidence/round62/claims.md` = a3193ebd…866bc matches.

**F2. Statement false at read time: seat count 64, actual 66.** Frozen claims line 128 says "One v2 wave `w1`, 64 seats". Evidence: `w1-dispatch.json` `counts.total` = 66 and `taskCall.tasks` length = 66; `w1-spec.json` `items` length = 66; roster names match in order (CHECK NAMES). Seat prompt `SentRoundScratch` also says "the 64-seat wave". The freeze check does not test prose counts, so it passes. The claims file is frozen and I did not edit it; routing to L1: correct the count in the report or note it as a known error.

**F3. Identifier cited in claims is absent from SOURCES.** Frozen claims line 85 says "S138 is the lead recorded in `corpus/SOURCES.md` `## Leads` by round 61". Evidence: `grep -n S138 corpus/SOURCES.md` prints nothing. The Leads heading is `## Leads (unopened)` (line 324), and the openat2(2) bullet has no id; it says "named by wave seat RevC2Claim1 (round 61)". The counter reports `ROW S138 absent`. INFERENCE: the id S138 is a landing assignment, not an existing one; the claim text should not be read as proof that the row already exists.

**F4. Landing-only files named by the frozen claims are absent (expected pre-landing).** `corpus/evidence/round62/openat2-probe.py` and `corpus/evidence/round62/openat2-probe.txt` do not exist (`ls` error). The counter needs both (`c2v2-count.py` lines 58, 217, 234: `PROBE script or committed output absent`). Only the candidates exist, in `controls/` (`candidate-openat2-probe.py`, `.txt`). `controls/run-c2v2-controls.py` line 53 copies the candidate to `corpus/evidence/round62/openat2-probe.py` in a mirror, which is the landing step. Until that copy and the S140 row land, C2 PROBE stays 0/1. No seat cites these two paths as inputs (checked: zero matches for `evidence/round62/openat2-probe` in spec items).

**F5. Seat items: no missing inputs.** 66 items; each dispatch task equals its spec prompt (BODY_RENDER; my check: 0 mismatches). I extracted 72 distinct path tokens from all prompts and resolved each against the lane. The 18 that did not resolve on first pass were classified by context:

| Token | Seats | Classification |
|---|---|---|
| `/corpus/evidence/round62/c1v2-count.py` | MutC1V2*, RevC1V2Legs*, ExecReproBattery, ExecReproC1V2A, ExecScratchHygiene, ExecForgeVariants, CritC1Content | regex truncation; full path `…/chousa-shokunin/corpus/evidence/round62/c1v2-count.py` exists |
| `pos-indep2.py` / `pos-indep3.py` / `pos-indep1.py..pos-indep3.py` | RevC1V2Legs*, ExecReproC1V2A | exist at `corpus/evidence/round62/controls/` |
| `null-pass.py`, `null-fail.py`, `null-hashlist.py` | ExecReproBattery | exist at `controls/` |
| `run-c2v2-controls.py` | RevQualityB | exists at `controls/` |
| `candidate-openat2-probe.txt` | CritC2Probe, RevC2V2Claim1–5 | exists at `controls/` |
| `capture-text.py` | CritC1Content, ExecForgeVariants, MutC1V2* | exists at `tools/capture-text.py` |
| `QUALITY.md` | RevQuality A–C, ScoutMistakesPrior | exists at `corpus/QUALITY.md` |
| `SOURCES.md` | ScoutC2RowsCensus | exists at `corpus/SOURCES.md` |
| `round-61-verifier-spotcheck.md` | RevQualityC | exists at `corpus/lessons/` |
| `corpus/knowledge/x.md` | CritC1Content | illustrative example cell in the prompt, not an input |
| `builder.py` | ExecScratchHygiene | generic name in a `pgrep` pattern, not a file |
| `ScribeStreak/streak.md` | ScribeStreak | output the seat creates under `.ufo/waves/round-62/w1/` |
| `corpus/lessons/round-62.md` | ScribeGate | output the seat drafts |
| `corpus/knowledge/openat2-resolve-r62.md` | ScribeC2V2Entry1–3 | output the seat drafts |

**Missing input files cited by seats: 0.** Expected-absent outputs (to be created by the seats named): ScribeC2V2Entry1–3 (one entry file), ScribeGate, ScribeStreak. The two landing-only claim files (F4) are not seat inputs.

**F6. Digests and commit references in claims match.** Commands and outputs (`sha256sum … | cut -c1-16`):
- `tools/build-spans.py` → c366492005ce304a (claim: c366492005ce304a) ✓
- `corpus/evidence/round62/c1v2-count.py` → b7016fba91b03460 (claim: b7016fba91b03460) ✓
- `corpus/evidence/round62/c2v2-count.py` → 817d5fc0b94e9fc8 (claim: 817d5fc0b94e9fc8) ✓
- `corpus/evidence/round61/c1-count.py` → f1d8b6fde8dedd88 (exists; claims cite it as the round-61 counter)
- `git cat-file -t 388d1535…` and `8607de84…` → commit. `git merge-base --is-ancestor 388d1535… HEAD` → ancestor ✓. Its subject: "round-62: claims freeze, v2 counter, forger battery, C2 counter, probe candidate, controls and receipts".
- Host: `/usr/include/linux/openat2.h` present; `pacman -Q man-pages linux-api-headers` → `man-pages 6.19-1`, `linux-api-headers 7.2-1` (match claims); `/usr/share/man/man2/openat2.2.gz` present.
- `grep -rl openat2 corpus/knowledge` → no output, exit 1 (matches claim "prints nothing (exit 1) at the base").
- `corpus/lessons/round-61-verifier-spotcheck.md`, `corpus/knowledge/derived-output-safety-r61.md`, `controls/c1v2-before.txt`, `controls/c2v2-before.txt`: present.

**F7. Before-receipts reproduce.** Counter run, `python3 -B corpus/evidence/round62/c2v2-count.py` (TMPDIR in scratch):
`ENTRY=0/1 TRIO=0/1 ROWS=0/3 QUOTES=0/0 COVERAGE=0/1 CLAIMS=0/1 ECHO=0/1 LIMITS=0/1 PROBE=0/1 MAP=0/1 CENSUS=1/1 C2=FAIL`, exit 1; detail lines `ROW S138/S139/S140 absent`, `PROBE script or committed output absent`. This equals the claims' "Before" line and `controls/c2v2-before.txt`. C1 before, `controls/c1v2-before.txt` tail: `LANDED=3/3 POSITIVES=4/4 FORGERS_REJECTED=0/12 STUBS_REJECTED=4/4 BATTERY=FAIL`, exit 1 (matches claims). I did not run the C1 battery (not in my item). `c1v2-battery.py --help` runs (exit 0) and shows the documented `--counter/--work` flags.

**F8. CENSUS=1/1 with no lane-local script.** The lane has no `scripts/sources-census.sh`; the fleet root has one (`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`, present). The counter's CENSUS passed, so the claim is consistent. Seats `ScoutC2RowsCensus` and `ScoutCensusCounts` use the fleet path. Not a false statement, but a seat that copies the lane-root path would fail.

**F9. Calibration gap in the freeze check.** It verifies digests, names, render and ready-file identity. It does not verify prose facts. F2 (66 vs 64) and F3 (S138 absent) pass it. For w1, the freeze check is not a sufficient gate on claim wording; L1 should read the claims prose for counts and ids.

**F10. Working-tree state.** `git -C … status --short` shows only `?? .ufo/waves/round-62/w1.ready.dispatched` and `?? .ufo/waves/round-62/w1/`, which are orchestrator/seat artifacts, not mine. I wrote nothing in the lane except this report. No installs. No pacman. No network.

## 2. Residual risk and verification gaps
- The counter run I made (C2) used `--root` default and TMPDIR scratch; I did not inspect every byte it wrote. Status shows no tracked-file change.
- I did not verify entailment or any seat's claim content (out of my item).
- Did not run the C1 battery; its freeze-check is the same file digest (b7016fba…), already checked.

## 3. Summary of the freeze check for the orchestrator
- Freeze check: PASS (8/8 CHECK lines, FAILED_CHECKS=none).
- Seats with a cited input missing: none.
- Frozen-prose errors to route to L1 (not edited by me): "64 seats" (should read 66); "S138 ... ## Leads" (no such id in SOURCES.md).
- Landing-only: corpus/evidence/round62/openat2-probe.py and .txt must be copied from controls/candidate-openat2-probe.* at landing for C2 PROBE.

VERDICT: FREEZE_CHECK=PASS missing_files_cited=0
