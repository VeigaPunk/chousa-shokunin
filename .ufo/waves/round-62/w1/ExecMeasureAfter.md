# ExecMeasureAfter — round 62 w1 cross-measurement

Findings: every measured line matches the committed receipts. No difference found.

Context checked: claims.md sha256 a3193ebd…66bc (matches wave context). Lane HEAD at run time `d173d144bbf55403d091115b5a6ec73a721dd95c`
(not the freeze commit 388d1535…; read-only `git rev-parse HEAD`). Counter/builder digests (`sha256sum | cut -c1-16`):
c1v2-count.py `b7016fba91b03460`, c2v2-count.py `817d5fc0b94e9fc8`, tools/build-spans.py `c366492005ce304a` — all equal the claims.
Scratch: /fast/scratch/hyaku/chousa-r62/ExecMeasureAfter (removed before yield). No tools installed. Tests ran concurrently on a loaded host.
Note: item (1) as written carries `--counter` twice; both set to c1v2-count.py (argparse takes the last), so it is the same counter.

## (1) Battery, exit 0, 2m22s wall
`python3 -B .../c1v2-battery.py --counter .../c1v2-count.py --work $S/b --counter .../c1v2-count.py`
Subjects: landed-1..3 LEGS=20/20 exit 0; pos-indep1/2/3, pos-ref 20/20 exit 0; F01–F06,F08–F11 11/20, F07 12/20, F12 19/20, all exit 1;
stub-exit0 1/20, stub-exit2 14/20, stub-base 11/20, stub-base-token 11/20, all exit 1. Final:
`LANDED=3/3 POSITIVES=4/4 FORGERS_REJECTED=12/12 STUBS_REJECTED=4/4 BATTERY=PASS`  exit 0

## (2) Landing builder, C1V2_SEED unset (checked `env | grep -c C1V2_SEED` = 0; ran with `env -u`)
Builder sha256 c366492005ce304a… in each run's BUILDER line.
- seed run 1 (SEED=4010189337): `LEGS=20/20 C1V2=PASS` exit 0
- seed run 2 (SEED=1684615360): `LEGS=20/20 C1V2=PASS` exit 0
- seed run 3 (SEED=2274661470): `LEGS=20/20 C1V2=PASS` exit 0
(H14/H15 rss ~21 MiB of limit 98304 KiB; H20 rss 167 vs 231 MiB neutral/plain — as designed, no leg flagged.)

## (3) c2v2-count.py (expected FAIL, not landed)
`ENTRY=0/1 TRIO=0/1 ROWS=0/3 QUOTES=0/0 COVERAGE=0/1 CLAIMS=0/1 ECHO=0/1 LIMITS=0/1 PROBE=0/1 MAP=0/1 CENSUS=1/1 C2=FAIL`
(+ `ROW S138/S139/S140 absent`, `PROBE script or committed output absent`), exit 1.
Identical to controls/c2v2-before.txt line 1 and detail lines.

## (4) run-c2v2-controls.py --work $S/c2, exit 0
24 variant lines + `C2V2_CONTROLS_UNEXPECTED=0`. `diff` against controls/c2v2-controls.txt (minus its `exit=0` line): IDENTICAL.
positive rc=0 C2=PASS (QUOTES=9/9); non-sequitur rc=0 C2=PASS (named limit); all 22 others rc=1 OK.

## (5) run-c1v2-controls.py --only X00 X01 X02, exit 0
- X00-intact exit=0 SURVIVED: `LANDED=3/3 POSITIVES=4/4 FORGERS_REJECTED=12/12 STUBS_REJECTED=4/4 BATTERY=PASS`
- X01-no-neutral exit=1 KILLED forgers_accepted=F01,F02,F03,F04,F05,F07,F08,F09,F11: `FORGERS_REJECTED=3/12 ... BATTERY=FAIL`
- X02-no-sandbox exit=1 KILLED forgers_accepted=F06,F10,F12: `FORGERS_REJECTED=9/12 ... BATTERY=FAIL`
- `CONTROLS_UNEXPECTED=0`, runner exit 0.
diff against first 3 lines of controls/c1v2-controls.txt + `CONTROLS_UNEXPECTED=0`: IDENTICAL.

## Limits
Per-leg detail for forgers (leg counts) was not compared with a receipt (c1v2-before.txt covers round-61 counter only); only summary lines are receipted.
Timing/load flakiness was not observed. X03–X12 mutants were not part of this item and were not run.

VERDICT: MEASURE_AFTER_MATCHES_RECEIPTS=yes differing=none
