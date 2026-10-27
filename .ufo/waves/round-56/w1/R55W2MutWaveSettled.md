# R55W2MutWaveSettled — wave-settled-check attack

Checker: `corpus/evidence/round55/wave-settled-check.py` at round-55 commit `29cfb12abd70f688b48c0d17f31e636f2d81104a`; `git diff 29cfb12a HEAD -- <checker>` was empty. Scratch checker SHA-256 pristine/restored: `ea82616faa6e63eaf4d8025923f27c7e015f053ccc49f15a9ad792237f002eec`. Fixture harness: `/fast/scratch/hyaku/chousa-r56/R55W2MutWaveSettled/driver.py`; separate timezone fixture `tz.py`. Each fixture used fresh lane/fleet Git repos in scratch and asserted fixture `--show-toplevel` before commits. No production file modified.

## Case results

- Baseline (two committed dispatched markers; w1 results before filing; w2 absent): `exit=1`; `SETTLED w1`, `UNSETTLED w2 no committed w2-results.json`, `WAVES=2 SETTLED=1`.
- Results added after report: `exit=1`; w2 `UNSETTLED ... after report=...` (expected).
- Results renamed away after commit, before filing: `HEAD` lacks `w1-results.json` (`git cat-file -e HEAD:<path>` failed), yet checker says `SETTLED w1` from historical add time. The round still exits 1 because w2 is absent. History-only receipt; not a false claim that results had once been committed.
- Results file present only uncommitted: `exit=1`, w2 `UNSETTLED no committed ...` (expected).
- Dispatched w3 marker untracked, while w1/w2 are both settled: `exit=0`, `WAVES=2 SETTLED=2`; w3 is invisible because marker enumeration uses `git ls-files`. False pass for a worktree dispatch absent from the committed index.
- Tracked dispatched marker changed only in worktree to an ABANDONED first line: `exit=0`, `ABANDONED w2`, `WAVES=2 SETTLED=2`. False pass: body comes from worktree if the path exists, so uncommitted text is trusted over HEAD. Reverse edit (HEAD ABANDONED, worktree dispatched) yields `exit=1`, confirming worktree preference.
- First line `TBD ABANDONED: maybe never` (no timestamp form): `exit=0`, `ABANDONED w2`; detector only tests substring `" ABANDONED:"`. A tab before `ABANDONED:` or the phrase on line 2 yields `exit=1` / `UNSETTLED`.
- Report add/delete/re-add, with w2 results between the adds: `exit=1`, `UNSETTLED w2 ... after report=23:50:07-03:00`; oldest report add governs, not the re-add.
- Results placeholder added before report, then real results content modified/committed after report: `exit=0`; checker reports `SETTLED w2 results=23:40:00-03:00`. `--diff-filter=A` sees only the early add, not the later update. False pass: an empty/stale placeholder can stand in for later results.
- Timezone comparison: independent lane result `2026-10-27T00:22:58+09:00` (15:22:58Z) vs fleet report `2026-10-26T23:50:07-03:00` (2026-10-27 02:50:07Z) yields `SETTLED`, `exit=0`; aware datetime comparison correctly treats result as earlier, despite wall-clock strings looking reversed. Equal instant across `-03:00` and `+02:00` also yields `SETTLED`, `exit=0` (inclusive boundary).
- `--before-filing`: uncommitted results remain `UNSETTLED` (`exit=1`); once committed, late result is `SETTLED` (`exit=0`), as documented. No report without flag and no committed markers each return usage `exit=2`.

## Mutation probe

Bounded detector: report-add/delete/re-add fixture (C6), expected oldest add to govern, hence `UNSETTLED` and `exit=1`. Pristine output: `UNSETTLED w2 results=2026-10-26T23:56:00-03:00 after report=2026-10-26T23:50:07-03:00`; mutant changed only `out[-1]` to `out[0]`, producing `SETTLED w2 results=2026-10-26T23:56:00-03:00`, `WAVES=2 SETTLED=2`, `exit=0` — killed by detector. Hashes: pristine `ea82616faa6e63eaf4d8025923f27c7e015f053ccc49f15a9ad792237f002eec`; mutant `d5629b0a40c672000a645aed8bdc029bc4ea829ea903ee8ca648441e0276f896`; restored `ea82616faa6e63eaf4d8025923f27c7e015f053ccc49f15a9ad792237f002eec`. Same C6 detector after restoration again returned `exit=1` / `UNSETTLED`. No baseline failure.

## Real-repository reproduction

Command, from lane root: `python3 corpus/evidence/round55/wave-settled-check.py --round N`; outputs match `corpus/evidence/round55/wave-settled-check.txt`:

```text
round 54: SETTLED w1 results=2026-10-26T23:41:46-03:00
UNSETTLED w2 results=2026-10-27T00:22:58-03:00 after report=2026-10-26T23:50:07-03:00
WAVES=2 SETTLED=1; exit=1
round 53: SETTLED w1 results=2026-10-26T21:22:31-03:00
ABANDONED w2 never taken by the dispatcher (marker: 2026-10-27T00:22:58 ABANDONED: round 53 closed (rounds[792]))
WAVES=2 SETTLED=2; exit=0
round 52: SETTLED w1 results=2026-10-26T20:23:18-03:00
SETTLED w2 results=2026-10-26T20:38:07-03:00
WAVES=2 SETTLED=2; exit=0
```

Live worktree check: `git ls-files -- .ufo/waves/round-56/w1.ready.dispatched` returned empty; checker `--round 56` returned `usage: no committed <wave>.ready.dispatched under .ufo/waves/round-56`, `exit=2` (the current dispatched marker is uncommitted and therefore invisible).

VERDICT: **FALSIFIED as a reliable wave-settled receipt** — uncommitted markers/worktree edits and stale early results placeholders can produce false `exit=0`; real round-54/53/52 receipt reproduced exactly. No invariant or target was changed.