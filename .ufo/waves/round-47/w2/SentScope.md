ATTACKS: scope/misroot + no-network/write + shokuknow untouched for round 47 wave 2
VERDICT: holds
(Defect notes below are informational observations, not claim verdicts; per seat contract this report only reports.)

## 1. Fleet-root misroots (untracked files mentioning chousa round 47)
`git -C /home/vgpnk/Projects/shokunin status --porcelain` untracked:
- `.omp/mcp.json` — no chousa/round47 mentions
- `.scratch/goal-20261025-hyaku-12h.md` — mentions `chousa` twice, both in hyaku-orchestrator run-queue prose ("Next block: chousa (0 this run)…", chousa r46 re-dispatch note). Not a chousa-r47/round47 artifact; no r47/r47 mentions. NOT a misroot.
- `.ufo/state/kotoba.report-baseline`, `kotodama.report-baseline`, `revenger.report-baseline` — empty files (0 bytes)
- `.ufo/waves/round-24/w2/RevUnlandedResolution.md` — 0 chousa, 0 round47 hits
- `.ufo/waves/round-69/w1/ScoutAmp.md` — 0 chousa, 0 round47 hits
Result: NO untracked fleet-root file mentions chousa round 47.

## 2. Lane untracked paths outside `.ufo/waves/round-47/w2/`
`git -C /home/vgpnk/Projects/shokunin/chousa-shokunin status --porcelain` untracked:
- `.ufo/waves/round-47/gen-w2-spec.py`
- `.ufo/waves/round-47/w2-dispatch.json`
- `.ufo/waves/round-47/w2-run.err`
- `.ufo/waves/round-47/w2-spec.json`
- `.ufo/waves/round-47/w2/` (currently only `swarm-registry.json`)
- `corpus/evidence/round47/measure-after.txt`

Assessment: the four `w2-*`/`gen-w2-spec.py` files are the wave-2 orchestrator artifacts, matching the (tracked) w1 convention exactly (w1-spec.json, w1-dispatch.json, w1-run.err, gen-w1-spec.py are all committed). Expected, not a misroot.

Anomaly: `corpus/evidence/round47/measure-after.txt` is uncommitted. Every prior round's measure file is committed and tracked (round40/measure-after.txt, round41/measure-after-*.txt, round45/measure-*.txt, round46/measure-after.txt — all in `git ls-files`). `git log -- corpus/evidence/round47/measure-after.txt` shows no commits. It is cited as round-record evidence (SCORECARD "Round 47 verdict" measure) but is absent from lane commit `1fc5ed193ad48a482402c862f4e4cc47e46d5b2d`; a fresh archive of the lane tip cannot reproduce it. Severity: low (untracked file, no mutant effect on counters; but the round record is incomplete until committed). Content itself is consistent with claimed results (counters run under a git archive of 1fc5ed193; C1/C2/C3 all PASS; freeze-time counter shows MISMATCHES=0).

## 3. Network / write calls in counters + inference-ground.py
Files: corpus/evidence/round47/{c1-count,c2-count,c3-count,build-spans}.py, tools/inference-ground.py.
Imports: argparse, hashlib, pathlib, json, re, sys, tempfile, shutil, subprocess, types; itertools/collections in build-spans. No `requests`/`urllib`/`httpx`/`aiohttp`/`socket`/`subprocess`-shell/`os.system`/`Popen` (subprocess.run used only to invoke `sys.executable` on local tool scripts).
Network: NONE. No fetch/curl/wget/http.
Write side-effects:
- c1-count.py: `shutil.copyfile` into a `tempfile.TemporaryDirectory` (canary fixtures) — local tmp only; and invokes round-46 c1-count + inference-ground via subprocess.
- c3-count.py: subprocess invocations of inference-ground with `--counts /dev/null`, `--registry`; reads corpus/lessons/round-47.md; no writes.
- inference-ground.py:501: `pathlib.Path(a.json).write_text(...)` — opt-in `--json` output path; `--counts /dev/null` is used by counters, `--json` is not passed by any counter. No other writes.
- No `open(..., 'w'/'a')` writes anywhere in the five files.
Result: no network egress; no writes outside explicit opt-in `--json` sink (unused by counters) and tmpdir canaries.

## 4. shokuknow unchanged by this wave
`git -C /home/vgpnk/Projects/shokuknow status --porcelain` exit=0; repo shows many pre-existing modified/untracked files (merge/) — pre-dating round 47.
Source captures used by r47/ C3 (file = sha256(url)[:24].txt, S085–S094) mtimes: 2026-10-23 20:36–20:39 -03; absent-defect-register.md: 2026-10-24 08:37 -03. All BEFORE round 47. None modified by wave 2.
Only file modified today (find -newermt 2026-10-25 08:00): `lanes/tabi/round8/.work/ratelimit-series.tsv` at 09:06:31 -03 (git diff: +1323 lines; last commit for the file: 8b94c5c1 2026-10-24). This is the tabi lane's cpu-metering tsv (unrelated to chousa; not touched by any r47 wave-2 tool). No chousa-r47 activity wrote into shokuknow. Source captures and absent-defect register untouched.

## 5. Informational defects in touched git state (not wave-2 misroots; no production edits made)
- `corpus/evidence/round41/receipts/cells/cells.json` (modified this morning 06:36 -03, pre-wave-2): diff shows shape-blind counter re-runs — `"k": 12 → 1`, gate path swapped to `.ufo/waves/round-41/controls/base-gate-r41.sh`, and 11 cells flipped `predicate_holds: true → false` with 1454 trap marks. Owned by the r41 wave, outside r47 scope; flagged as a defect.
- `swarm-registry.json` r40 (04:18, 10-24) and r41 (04:42, 10-24) diffs are wave/shepherd bookkeeping (agentId fills), not r47.

## 6. Commands run (verbatim decisive)
- `git -C /home/vgpnk/Projects/shokunin status --porcelain` → listed in §1.
- `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin status --porcelain` → listed in §2.
- `grep -nE 'requests\.|urllib|urlopen|httpx|aiohttp|socket\.|subprocess|os\.system|Popen|urlretrieve|fetch|curl|wget|open\([^)]*["'][wa]|\.write\(|Path\([^)]*\)\.write|shutil\.(copy|move)|os\.(remove|rename|makedirs|mkdir)|os\.environ\[.*\]\s*=' corpus/evidence/round47/*.py tools/inference-ground.py` → hits: subprocess.run (c1:68,113,119; c3:173), shutil.copyfile (c1:107–108), `pathlib.Path(a.json).write_text(` (inference-ground.py:501). No network hits.
- `git -C /home/vgpnk/Projects/shokuknow status --porcelain; echo EXIT=$?` → EXIT=0.
- `find /home/vgpnk/Projects/shokuknow -type f -newermt "2026-10-25 08:00" ! -path "*/.git/*" -printf ...` → only `lanes/tabi/round8/.work/ratelimit-series.tsv` (09:06:31).
- `stat` on S085–S094 captures + absent-defect-register → 2026-10-23 20:36–20:39 / 2026-10-24 08:37 -03.
- `git log --oneline -3 -- corpus/evidence/round47/measure-after.txt` → no output (never committed); `git ls-files 'corpus/evidence/' | grep -i measure` → prior rounds' measure files tracked.
- `cat /home/vgpnk/Projects/shokunin/.ufo/state/kotoba.report-baseline` etc. → empty (0 bytes, sha256 of empty).
