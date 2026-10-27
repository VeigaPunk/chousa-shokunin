# R55DraftMistakes — round-54 filing and mistake-table audit

Scope: mined the candidate round-54 premature report filing, the lesson's `BAD=6` assertion, and W2 reports for other round-54 record mistakes. Read frozen claims at `corpus/evidence/round55/claims.md:196-198` (candidate mistake) and round-54 lesson `corpus/lessons/round-54.md:14-17`.

## 1. Report filed before W2 settled — confirmed

Evidence:

- Prompt criterion, fleet `.ufo/prompts/chousa-round-54.md:89` (located by search): “Do not file the report before WAVE-DONE for every wave you launched.”
- `/home/vgpnk/Projects/shokunin/.ufo/reports/round-54/chousa.md:97-98` explicitly says W2 was dispatched and “The report was filed before W2 WAVE-DONE”.
- Fleet report commit: `git -C /home/vgpnk/Projects/shokunin log -1 --format='%H %cI' -- .ufo/reports/round-54/chousa.md` → `86023b972ef9c975e21ad6cb78c6c050aa25c625 2026-10-26T23:50:07-03:00`.
- Lane W2 dispatch commit: `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin show -s --format='%H %cI' 178667dc2c9d1656e864abfdc251c68757428613` → `178667dc2c9d1656e864abfdc251c68757428613 2026-10-26T23:41:46-03:00`.
- W2 results says `settled_by` orchestrator session exit, not WAVE-DONE: `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-54/w2-results.json:8-9`; note timestamps exit `2026-10-26T23:57:36-03:00`, after report commit. Result record: 38 spawned, 22 outputs recovered, with other outputs null/read reports (`:5-9`).

Criterion that should have caught it: the round prompt's report gate is WAVE-DONE for every launched wave, not merely dispatch; round-54's own report accurately disclosed the violation, but disclosure is not conformance. The results JSON documents an eventual session-exit settlement, not a WAVE-DONE receipt.

A practical gate must reject a report commit if any launched-wave completion receipt is missing or timestamped after the report commit. Example check (run against preserved round-54 evidence; exits nonzero because completion receipt is absent and report predates recorded settlement):

```sh
python3 -c 'import json,subprocess,sys; p="/home/vgpnk/Projects/shokunin/.ufo/reports/round-54/chousa.md"; t=subprocess.check_output(["git","-C","/home/vgpnk/Projects/shokunin","log","-1","--format=%cI","--",p],text=True).strip(); r=json.load(open("/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-54/w2-results.json")); settled=r["note"].split("exited at ",1)[1].split(" ",1)[0]; assert r.get("wave_done") is not None and settled <= t, ("NO WAVE-DONE before report",t,settled)'
```

Observed on round-54: `AssertionError: ('NO WAVE-DONE before report', '2026-10-26T23:50:07-03:00', '2026-10-26T23:57:36-03:00')`, exit 1. The absent `wave_done` field and later settlement are independently visible in results `:8-9`. On a corrected record, a timestamped WAVE-DONE receipt at or before report commit makes the same predicate pass. This is an example gate, not a claim that the round-54 system actually ran it.

## 2. Lesson row 2's unrun number — confirmed; captured-by gap

`corpus/lessons/round-54.md:15` claims the mirror without the two dumps gives `BAD=6`. W2 report `R54W2CritMistakes.md:17` reports the actual run: both dumps absent → `ANCHORED=7/16 UNANCHORED=9 BAD=9`, exit 1. `BAD=6` applied only when S101's dump alone is missing; S100 alone gives `BAD=3`. Thus row's failure direction is right, numeric evidence is not. This is specifically a **captured-by** failure: `captured-by: none` at lesson `:15` represents no executed observation/check for that exact two-dump condition; a named criterion elsewhere does not capture an unrun numeric outcome. The corresponding check is `python3 corpus/evidence/round53/pointer-anchor-check.py` on a mirror lacking both dumps, whose output must be retained verbatim; it fails against the incorrect recorded expectation (`BAD=6`) and yields the observed BAD=9.

## 3. Other committed-record mistake found in W2 reports

W2 `R54W2ExecCensus.md:117-120` reports a “pre-existing S077 tool used-by” surviving. This conflicts with the W2 C2 rerun at `R54W2ExecC2Rerun.md:168-169`, which states the S101 used-by premise holds and the cut is consistent, not S077; and report draft's detailed findings. This is a pointer/identity mix-up in the census report, not evidence of a defect in frozen C2. It should have been caught by verifying the cited row ID and used-by cell against `corpus/SOURCES.md` at the measured tip before calling it a finding. Suggested fail-on-bad-record check: extract each claimed `S077` used-by finding and assert the row is actually S077 and matches the stated inspected value; the W2 report's own pointer/findings do not supply that matching evidence. I did not run an independent row mutation or checker for this item, so it is a located discrepancy, not a shown-fail fix.

## Verification and limits

No checks were run beyond the command outputs transcribed above and the cited report/lesson reads. In particular, I did not rerun the pointer-anchor checker or independently inspect the S077 row. No installs, source fetches, or product edits. No scratch artifacts are cited.

VERDICT: attacked the round-54 W2-before-filing gate and lesson row-2 number; premature filing and BAD=6 are contradicted by recorded evidence, with an additional W2 census-report ID discrepancy noted but not mutation-tested.
