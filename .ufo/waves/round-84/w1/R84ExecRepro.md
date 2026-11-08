# R84ExecRepro — frozen-claim reproduction (C1 K1, C2 K1/K4)

Seat: R84ExecRepro. Lane root: `/home/vgpnk/Projects/shokunin/chousa-shokunin`.
Freeze rev: `3b616420b2dcc1f8a24a1cb9db4198c7adc8929b`; scored landing + tip: `03bbb4580b39b442be69f998fae2db48d64b8c93`.
Receipts: `.ufo/waves/round-84/w1/R84ExecRepro/` (`pins.txt`, `depth-r84-*.txt`, `gate-records-r84-*.txt`, `controls-rerun/`, `controls-diff.txt`).
Tooling installs: none. Network: none.

## (a) Instrument identity

Command: `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin show <rev>:<path> | sha256sum` for every row of `corpus/evidence/round84/instrument-pins.txt` at both revs.
Receipt: `.ufo/waves/round-84/w1/R84ExecRepro/pins.txt`.

- Landing `03bbb458`: all 6/6 MATCH (depth-r84.py, gate-records-r84.py, run-controls-r84.sh, c2-positives.tsv, base-knowledge.txt, claims.md).
- Freeze `3b616420`: 3/6 MATCH — `depth-r84.py`, `gate-records-r84.py`, `c2-positives.tsv` MATCH; `run-controls-r84.sh` (freeze `3a8dcbf2…` vs pin `2a20115c…`), `base-knowledge.txt` (`b457155b…` vs `67bd6378…`), `claims.md` (`f6f032a6…` vs `19d68274…`) MISMATCH.

Explanation (verified, not assumed): `instrument-pins.txt` does not exist at freeze (`git show 3b616420:…/instrument-pins.txt` → `fatal: path … exists on disk, but not in '3b616420…'`); it was added in `03bbb458` pinning landing bytes. The freeze→landing diff for the 3 mismatched files is substantive round-84 landing work: `run-controls-r84.sh` gained `BASE_REV`/`mkbase` + pre-repair `81b81173` tool swap for `c2-k0`; `base-knowledge.txt` gained `appraisal-judgment-records-r83.md`; `claims.md` changed S017→S214/S018/S023 and FRESH 6→5 / RC 3→4. The two counters and `c2-positives.tsv` — the counting instruments — are byte-identical at both revs, so the counting commands bind identically. This is a pin-timing artifact, not counter drift.

## (b) Before/after counters

Trees: `git -C … archive <rev> | tar -x -C <scratch>` under `/fast/scratch/hyaku/chousa-r84/R84ExecRepro/` (`tree-freeze`, `tree-landing`), `--repo` = lane checkout, `--work` = scratch seat dir.

Before (freeze `3b616420`), receipt `depth-r84-freeze.txt`:
- `python3 -B <tree-freeze>/corpus/evidence/round84/depth-r84.py --root <tree-freeze>` → `ENTRY appraisal-judgment-records-r83.md ok=no rows=10 quotes=0/16 fails=E3,E6` / `DEPTH_R84 entries=1 ok_entries=0 rows=10 located_quotes=0 fresh_sources=0` / `DEPTH_R84=FAIL`, rc=1. DEVIATION from seat brief's expected `entries=0`: observed `entries=1` — the r83 appraisal entry is present at freeze but fails the depth predicate (0 located quotes). Matches the committed `controls/receipts/c1-d0-donothing.txt` exactly (same lines), so the counter's before-behaviour is as committed; the brief's `entries=0` shorthand is wrong, the FAIL outcome is as claimed.
- `python3 -B <tree-freeze>/corpus/evidence/round84/gate-records-r84.py --root <tree-freeze> --repo … --work …` → `TOOL=present POSITIVE=15/15 FRESH_POSITIVE=5/5 FORGED_REFUSED=288/288 EXPECTED_CODE=288/288 EMPTY_REFUSED=1/1 RC=4/4 SETUP=unscored` / `GATE_RECORDS_R84=PASS`, rc=0. Matches expected predicate at freeze (tool already repaired at freeze).

After (landing `03bbb458`, run twice), receipts `depth-r84-landing.txt`, `gate-records-r84-landing.txt`:
- Depth → `ENTRY search-transparency-reporting-r84.md ok=yes rows=11 quotes=12/12 fails=-` / `DEPTH_R84 entries=1 ok_entries=1 rows=11 located_quotes=12 fresh_sources=3` / `DEPTH_R84=PASS`, rc=0. Meets predicate (`entries=1 ok_entries=1`, `rows=11≥7`, `located_quotes=12≥8`, `fresh_sources=3≥1`).
- Gate-records → `TOOL=present POSITIVE=15/15 FRESH_POSITIVE=5/5 FORGED_REFUSED=288/288 EXPECTED_CODE=288/288 EMPTY_REFUSED=1/1 RC=4/4 SETUP=unscored` / `GATE_RECORDS_R84=PASS`, rc=0. Byte-identical predicate line on both runs.

## (c) Committed control driver re-run

Command: `HYAKU_SCRATCH=/fast/scratch/hyaku/chousa-r84/R84ExecRepro bash corpus/evidence/round84/run-controls-r84.sh 03bbb4580b39b442be69f998fae2db48d64b8c93 …/R84ExecRepro/controls-rerun`.
Result rc=0, `CONTROLS_AS_EXPECTED=9/9`; `diff` of rerun `summary.tsv` vs committed `corpus/evidence/round84/controls/receipts/summary.tsv` → identical (receipt `controls-diff.txt`). All 9 controls as expected (c1-d0/d1/d3 FAIL, c1-b1 PASS, c2-k0/f1/f2/f3/f4 FAIL).

## (d) C1 predicate (b) — lesson verify at landing

Command (from archived tree-landing): `python3 tools/gate-records.py verify --root . --repo /home/vgpnk/Projects/shokunin/chousa-shokunin corpus/lessons/round-84.md` → 3 OK (`S214`, `S018`, `S023`), `GATE_RECORDS files=1 records=3 ok=3 fail=0`, rc=0. As expected.

## (e) C1 K4 legs at landing (all from tree-landing)

- No-record file: `GATE_RECORDS files=1 records=0 ok=0 fail=0`, rc=1. Expected 1 — PASS.
- One OK rev record + one FAIL record: `…:1 S199 OK`, `…:2 ? FAIL PARSE`, `records=2 ok=1 fail=1`, rc=1. Expected 1 — PASS.
- Missing FILE argument: `error: the following arguments are required: files`, rc=2. Expected 2 — PASS.

## FINDING (C1 K2 setup leg) — FIRED

Command: `python3 tools/gate-records.py verify --root . --repo /fast/scratch/hyaku/chousa-r84/R84ExecRepro/nogit <revonly.md>` where `revonly.md` holds one genuine rev record (`S199 rev=b7803829922770b890e9f4efdd30d12c3695439a path=corpus/lessons/round-79-verifier-spotcheck.md line=222 …`) and `nogit` is a scratch dir with no git history.
Observed: stdout `GATE_RECORD … S199 FAIL LINE,REV`, `GATE_RECORDS files=1 records=1 ok=0 fail=1`, stderr empty, rc=1.
Frozen expectation (claims.md §C1 class 4 + counter docstring): exit 2 with `GATE_RECORDS_ERROR` on stderr — not `FAIL REV,LINE` with exit 1.
Root cause in landing bytes: `tools/gate-records.py` uses subprocess `git -C <repo> cat-file` and on non-zero returncode degrades to a record-level FAIL (`LINE,REV`); `GATE_RECORDS_ERROR` is only emitted for missing files (lines 277/281), never for a non-git `--repo`. The counter prints `SETUP=unscored` and explicitly delegates this leg to the executor seat, so the counter's PASS does not cover it. Under K2 (setup leg counts as K2 if the tool misreports), this is a misreport at the landing revision. This is the sole kill-rule hit in this reproduction.

## Verdicts

VERDICT: R84ExecRepro C1 fired — counter predicate passes (288/288) but the K2 setup leg misreports: non-git --repo gives FAIL LINE,REV rc 1 instead of GATE_RECORDS_ERROR rc 2.
VERDICT: R84ExecRepro C2 held — before FAIL rc 1, after PASS rc 0 (rows=11, located_quotes=12, fresh_sources=3), controls 9/9.
