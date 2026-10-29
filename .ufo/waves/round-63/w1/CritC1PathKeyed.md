# CritC1PathKeyed — R63-C1 path forgers (critic)

Scope: attack `corpus/evidence/round63/c1-battery.py` by recognising the battery and printing expected lines per leg, without running any gate. Scratch-only forgers; no lane, fleet or frozen file was written (the battery was copied to scratch and edited there).

## Findings

1. **One of four recognition levels passes the unmodified battery in full.** The `token` forger reads `CLEAN=1/1 DEFECTS=15/15 BENIGN=6/6 BATTERY=PASS` (exit 0) and runs no gate code. It is accepted.
2. **What it recognises** (all must hold, else it falls back to the reference tool; the trace shows no fallback on any leg):
   - root matches `/v-[0-9a-f]{8}/lane$` and the sibling `../../golden` exists (the battery's scratch golden; no real lane has it);
   - environment keys are the battery's five (PATH, LC_ALL, HOME, TMPDIR, HYAKU_SCRATCH), HOME equals cwd, cwd matches `/c-[0-9a-f]{8}$`, own path matches `/t-[0-9a-f]{8}/x[0-9a-f]{8}\.py$`.
   - Then per leg: argv `--skip G99` → D13 (exit 2, no PREFLIGHT line); `--only G03` → D14; a `--fleet` without `scripts/sources-census.sh` → D12 (ENV G01, exit 2).
   - Content: bytes diff against the sibling golden (difflib line opcodes: new file / append / insert / replace). An inserted SOURCES line identical to a golden line → D01, else B01. Replaced-in-place SOURCES row → G01 (D02, D03 expect the same set, so they are one class). Knowledge file new with README untouched → D04; plus README append → B02; plus an in-place SOURCES dup → D11. Lesson new → B03; lesson edited in place → D06. README in place → D05; README+LOG+quote-reopen appended → B06. SCORECARD append → B05, in place → D08. SHONEN in place → D07. freeze-check / assimilate-rows in place → D09 / D10.
   - **The one token:** an appended SHONEN line containing the literal `missing` → D15 (otherwise B04). This is the only leg pair that differs only in whether a pointer resolves (G04).
3. **Recognition ladder (same battery, four forgers).** Only the last one is accepted.

| forger (recognition used) | CLEAN | DEFECTS | BENIGN | battery | legs it cannot fake |
|---|---|---|---|---|---|
| `argv` (battery path + argv only; every other `--skip G08` run prints clean) | 1/1 | 3/15 | 6/6 | FAIL | D01–D11, D15 |
| `mtime` (battery path + mtime fresher than `v-*` dir + names, new-vs-golden; no content) | 1/1 | 15/15 | 3/6 | FAIL | B01, B04, B05 (an append and an edit of the same file look alike) |
| `shape` (battery path + diff vs golden opcodes + exact-duplicate test; no tokens) | 1/1 | 14/15 | 6/6 | FAIL | D15 (B04's append has the same shape) |
| `token` (shape + literal `missing` in appended SHONEN line) | 1/1 | 15/15 | 6/6 | **PASS** | none |

   - `mtime` confirms the task's mtime recognition works: the apply step's files are the only ones newer than the variant directory. The forger still cannot split append from edit without content.

4. **Battery change that rejects the accepted forger.** Its only tell is the planted stem of D15, the literal word `missing`. In a scratch copy (`patched/c1-battery-p1.py`, `--lane` pointed at the real lane) the stem `zz-%s-missing.md` became `zz-%s-lost.md`, and nothing else changed. `LEG D15 defect FAIL rc=0 want 1` then `CLEAN=1/1 DEFECTS=14/15 BENIGN=6/6 BATTERY=FAIL` (exit 1). The token forger is rejected; the other 21 legs still pass.
   - [INFERENCE, not run] A list-based forger could hard-code `lost|gone|missing`, because the battery source is public. The durable form is to drop the word: `zz-%s.md` with only the random tag, so no planted word exists in D15's text. D15 then separates from B04 only by a path-existence read, which is G04's job.

5. **Calibration of the battery (no forger involved).**
   - The 15 defect legs have 10 distinct expected outcomes: {G01}: D01, D02, D03; {G02}: D04, D05; {G03}: D06 and D14 (argv); {G04}: D07, D15; {G05}: D08; {G06}: D09; {G07}: D10; {G01,G02}: D11; ENV G01: D12; usage: D13.
   - Only D15 (vs B04) needs a read of a pointer's existence. Every other defect is a shape or argv fact, which is why the shape forger reaches 14/15.
   - Six benign legs all expect PASS, so an always-PASS shape-matched forger is only caught by the defect legs that share a shape with a benign leg (B01/D01, B04/D15, B05/D08, B03/D06).

## Evidence (commands and observed output)

- `python3 -B .../c1-battery.py --tool forge_token.py --fleet /home/vgpnk/Projects/shokunin --work <scratch>/b-token --jobs 2`
  → 22 `LEG ... ok` lines, then `CLEAN=1/1 DEFECTS=15/15 BENIGN=6/6 BATTERY=PASS`, exit 0.
- Same command with `forge_shape.py`: `LEG D15 defect FAIL rc=0 want 1`; `CLEAN=1/1 DEFECTS=14/15 BENIGN=6/6 BATTERY=FAIL`, exit 1.
- `forge_mtime.py`: `LEG B01 ... FAIL rc=1 want 0`, `LEG B04 ... FAIL rc=1 want 0`, `LEG B05 ... FAIL rc=1 want 0`; `CLEAN=1/1 DEFECTS=15/15 BENIGN=3/6 BATTERY=FAIL`, exit 1.
- `forge_argv.py`: `CLEAN=1/1 DEFECTS=3/15 BENIGN=6/6 BATTERY=FAIL`, exit 1.
- Partial run `--only CLEAN,D01,D15,B04,B01,D12,D13,D14` on the token forger: 8 legs ok, `BATTERY=PARTIAL`, exit 0 (17.8 s).
- Per-level trace (the forger's own log of identified legs): 22 entries per level, zero `leg=None`, zero `NOT-BATTERY`. Trace confirms no reference fallback. Token-level trace notes D02 and D03 both as `D03` (same expected set).
- Patched battery run: `CLEAN=1/1 DEFECTS=14/15 BENIGN=6/6 BATTERY=FAIL`, exit 1, 91 s.
- Four full runs took 308 s at `--jobs 2`; host load average 72 on 32 cores (22:29).
- Scratch forger sha256 prefixes: `forge_token.py` e47f5b9ab03b97e3; `forge_shape.py` 1c2f78b85795e865; `forge_mtime.py` 6f857e3793d93d23; `forge_argv.py` 7bd353db3be6fe4b; `patched/c1-battery-p1.py` 56224a9319ea1c47. The sources are deleted with the scratch directory.

## Limits and disclosures

- I did not run the reference tool on any leg; its only role in the forgers is off-battery fallback, which never triggered.
- The `mtime` identification assumes no other seat rewrites lane files during a battery run; it did not happen in these runs, but nothing enforces it.
- The `token` forger's `golden` sibling is a battery-only artifact; the claim is "battery passable by recognition", not "a lane tool can be fooled in use". A real tool run outside the battery would see no `golden` sibling and fall back (INFERENCE).
- Every run used the frozen battery at sha256 prefix `0073fba73c89aaf8` (matches claims; committed at `62876ef`, and `git status` on `corpus/evidence/round63/` was clean when checked). No battery or lane file was changed.
- No tool installed or upgraded; no pacman, git or network use; no lane, fleet or sibling write. Scratch `/fast/scratch/hyaku/chousa-r63/CritC1PathKeyed/` removed before yield.

VERDICT: PATH_FORGERS_ACCEPTED=1 best=15/15+6/6
