# Round 61 · w1 · RevC1LegsH1 — review of C1 legs H07 FOREIGN, H08 REPLACE, H09 ORPHAN

Scope: `corpus/evidence/round61/c1-count.py` (sha256 f1d8b6fd…cfff9ef, matches claims.md) against predicate R61-C1.
Counter and reference were read, not edited. All work in `/fast/scratch/hyaku/chousa-r61/RevC1LegsH1/` (deleted before yield).
Frozen inputs checked: claims.md sha256 9afec8d4…ceacec ✔; reference `controls/ref-build-spans.py` sha256 86d64c31…eccfd ✔;
freeze 2b0e17b is an ancestor of lane HEAD (`git merge-base --is-ancestor`, read-only). No installs. No network.

## Findings

**F-1 Counter defect, H07 FOREIGN: a builder that clobbers a foreign `spans.tsv` and restores it before exiting 2 passes.**
- The leg snapshots with `snap(fx.out)` (c1-count.py:364, 366, 371, 373). `snap` ignores mtime unless asked (line 94 default `mtime=False`; mtime added only at line 115 under `if mtime`).
- Incorrect builder `f-transient.py` (= reference + write golden manifest over the foreign one, then write the original bytes back, exit 2; edit at reference lines 274–278).
- Run: `TMPDIR=$S python3 -B c1-count.py --builder f-transient.py --work $S/w-f-transient --seed 61001` → `LEG H07 FOREIGN pass rc=2,2`, `LEGS=20/20 C1=PASS` (also 61002, 61003: 20/20).
- Hand demo (`demo.sh`): reference foreign `spans.tsv` ctime unchanged on refusal; `f-transient` ctime/mtime rewritten (`1793227054` vs `978314400`), content identical afterwards.
- Probe (scratch copy only, `c1-count-mtime.py`: lines 364/366/371/373/388/390 use `snap(..., True)`): `f-transient` → `LEG H07 FOREIGN fail` (19/20); reference 20/20; `c-guardorder` 20/20; `c-refuselinks` 20/20. So an mtime-aware snapshot discriminates this without false alarms on the three correct variants.

**F-2 Counter defect, H08 REPLACE: `--replace` that deletes non-`.txt` user files passes.**
- The only non-span file H08 places is `README.txt` (c1-count.py:369–370; expectation at 376). Its name ends in `.txt`.
- Incorrect builder `f-selective.py` (= reference + under `--replace`, unlink every regular root file whose suffix is not `.txt`/`.tsv`; edit after reference line 306).
- Run: `LEG H08 REPLACE pass rc=0`, `LEGS=20/20 C1=PASS` (61001–61003). Hand demo: `--replace` removed `notes.md`; `README.txt` kept.
- Probe (scratch copy `c1-count-probe2.py`: adds `notes.md` next to README at 370–372 and expects it at 379–380): `f-selective` → `LEG H08 REPLACE fail` (19/20); reference 20/20.

**F-3 Counter defect, H09 ORPHAN: a builder that writes its output to a sibling of DIR and refuses passes.**
- H09 snapshots and compares only `fx.out` (c1-count.py:388, 390). The fixture root `fx.dir` (holding `cache/`, `tools/`, `q.tsv`) is never compared, so writes beside DIR are invisible.
- Incorrect builder `f-staged.py` (= reference + on orphan refusal without `--replace`, write the full build into `out.staged` beside DIR, then exit 2; edit at reference 274–281).
- Run: `LEG H09 ORPHAN pass rc=2`, `LEGS=20/20 C1=PASS` (61001–61003). Hand demo: `out=spans.tsv` (unchanged), `sibling=spans spans.tsv`.
- Probe (scratch copy: H09 snapshots `fx.dir` at 391/393): `f-staged` → `LEG H09 ORPHAN fail` (19/20); reference 20/20.

**F-4 No false negative found on H07, H08, H09.** Three correct builders, each at seeds 61001, 61002, 61003, passed all three legs and the whole counter:
- `c-guardorder.py` — guard order changed: orphan and differs checks run before the link/type checks (reference 259–277 reordered).
- `c-heallinks.py` — symlinked `spans/` is unlinked and replaced without a flag (allowed by the counter's H10–H12 wording, "exit non-zero, or healed"); guard does not refuse links.
- `c-refuselinks.py` — links refused by default, replaced under `--replace` only.
- Run: `LEGS=20/20 C1=PASS` for all three at 61001, 61002, 61003 (`run-c-*-6100{1,2,3}.out`), with `H07 pass rc=2,2`, `H08 pass rc=0`, `H09 pass rc=2`.
- Exit codes: H07 and H09 admit only exit 2 (predicate: "exit 2 each time"), so no exit-code variant is admissible for these legs; none was built for them.

**F-5 Calibration consequence (for L1).** The three incorrect builders reach `C1=PASS` at all three fresh seeds (`f-transient`, `f-selective`, `f-staged`, each `LEGS=20/20`). The landed-builder kill rule ("C1 verified when 20/20 at three seeds") would therefore verify a builder that violates the docstring's "nothing written or removed" (line 34–40 of the builder), "--replace overwrites spans.tsv and orphan span files" only, and "refuse … unless --replace". These are failures inside the H07–H09 hazard classes, so they are counter defects, not the "hazard outside the 20 legs" routing the claim reserves.

**F-6 Outside my legs (observation).** The builder docstring says links are refused, exit 2, with no exception (`tools/build-spans.py`, "Output safety" paragraph). The counter's H10–H12 accept healing ("exit non-zero, or … healed"). `c-heallinks` passes C1 on that basis. Counter and docstring disagree on link policy; not verified against the landed builder (not run).

## Counter line references (c1-count.py, unmodified)
- 94 `snap(root, mtime=False)`; 115 mtime gate.
- 341–356 `prior_state` (`spans.tsv` + `spans/{sid}-1.txt` + `spans/S404-9.txt`).
- 359–378 H07/H08: 364, 366 (part a), 369–370 (README), 371, 373, 376 (want README), 377.
- 381–390 H09: 385 orphan write, 388 snapshot, 390 comparison.

## Commands and observed output
- `python3 -B c1-count.py --builder controls/ref-build-spans.py --work $S/w-ref --seed 61001` → `LEG H07 FOREIGN pass rc=2,2` · `LEG H08 REPLACE pass rc=0` · `LEG H09 ORPHAN pass rc=2` · `LEGS=20/20 C1=PASS` (calibration, matches controls/c1-reference.txt).
- `c-guardorder`, `c-heallinks`, `c-refuselinks`, `f-transient`, `f-selective`, `f-staged` at 61001 (`run-*-61001.out`): all `LEGS=20/20 C1=PASS`; 61002 and 61003 identical (`run-*-6100{2,3}.out`).
- `demo.sh`: the three incorrect behaviours shown by hand on a 1-URL fixture (F-1..F-3 above).
- Probes: `probe-ref-build-spans.out`, `probe-f-transient.out` (H07 fail), `probe-c-guardorder.out`, `probe-c-refuselinks.out` (20/20); `probe2b-{ref,sel,stg}.out` (H08 fail for sel; H09 fail for stg; ref 20/20).

## Not run / limits
- Landed `tools/build-spans.py` was not run (outside this seat's item).
- Probe copies are scratch-only; the counter in the lane is unchanged.
- Other legs (H10–H20, P01–P06) not reviewed beyond the reference calibration run.
- Probes change one thing each; a combined fix for F-1..F-3 is INFERENCE until run.
- Lane HEAD is 9f32ac0 (wave spec); freeze 2b0e17b is an ancestor; I did not inspect that commit's contents.

## Verdict
Three incorrect builders pass their legs; three correct builders pass all three. Counter defects are real and specific (mtime-blind snapshot, extension-selective guard test, fixture-root-blind snapshot), each shown to be closed by a scratch-only probe with no regression on the reference or the correct variants.

VERDICT: LEG_DEFECTS=3 false_negative=0 false_positive=3 legs=H07 FOREIGN, H08 REPLACE, H09 ORPHAN
