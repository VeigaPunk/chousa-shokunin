# ExecBareExport — round 63 w1: bare `git archive` export vs the frozen instruments

Setup: `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin archive HEAD | tar -x -C /fast/scratch/hyaku/chousa-r63/ExecBareExport/exp`.
HEAD at archive time = `c8bfcc65cb327b1a7da27fa39ef9a482a5b33cfb` (not the freeze commit 62876ef; later lane commits). Export has
no `.git`, no parent fleet (its parent is `/fast/scratch/hyaku/chousa-r63/ExecBareExport`, no `scripts/`).
All runs `cd exp`, `python3 -B`, `TMPDIR=/fast/scratch/hyaku/chousa-r63/ExecBareExport`, `SHOKUNIN_ROOT` unset in the environment.
No labrat, no network, no write outside scratch and this report. Scratch deleted at the end.

## Findings (the four requested invocations)

| # | invocation | rc | observed |
|---|---|---|---|
| 1 | `c2-count.py --fleet /home/vgpnk/Projects/shokunin` | 1 | `ENTRY=0/1 ... CENSUS=1/1 C2=FAIL` + `ROW S142/S143/S144 absent`, `LIMITS do not name the live git version 2.56.0`, `PROBE script or committed output absent`. A real verdict (the entry has not landed at this HEAD), not an error; the counter ran from a bare export. |
| 2 | `c2-count.py` (no `--fleet`) | 2 | stderr: `c2-count: no scripts/sources-census.sh — pass --fleet DIR (the fleet root, or set SHOKUNIN_ROOT); a bare git archive of the lane has no fleet parent`. Names the flag, the env var and the cause: the round-62 exit-2 defect is now a self-explaining usage error. |
| 3 | `c1-battery.py --tool .../pos-ref-preflight.py --lane exp --fleet F --work W --only CLEAN,B01` | 0 | `LEG CLEAN clean ok ok`, `LEG B01 benign ok ok`, `CLEAN=1/1 DEFECTS=0/15 BENIGN=1/6 BATTERY=PARTIAL` (3.8 s). Exit 0 with PARTIAL is the documented `--only` behaviour (docstring line 41). |
| 4a | preflight `--root exp --fleet F --skip G08` | 0 | G01–G07 PASS, `PREFLIGHT=7/7 FAILED=none ENV=none SKIPPED=G08`. |
| 4b | preflight `--root exp --skip G08`, no fleet | 2 | `GATE G01 census ENV no sources-census.sh (pass --fleet DIR, or set SHOKUNIN_ROOT, or run inside a fleet layout)`; `PREFLIGHT=6/7 FAILED=none ENV=G01 SKIPPED=G08`. ENV is not counted as pass, flag named. |

Extra probes (same export, same environment):
- c1-battery without `--fleet` (rc 2): `c1-battery: no census script under /fast/scratch/hyaku/chousa-r63/ExecBareExport/scripts (pass --fleet DIR)` — clear. With `SHOKUNIN_ROOT` exported instead (rc 2) the same message: the battery ignores `$SHOKUNIN_ROOT`, unlike c2-count and the preflight (its usage line does not claim it; asymmetry, not a defect).
- c1-battery without `--work` (rc 2): argparse `the following arguments are required: --work`. Nonexistent `--work` dir: accepted (rc 0).
- c1-battery `--only ZZ` (unknown leg), rc 0: `CLEAN=0/1 DEFECTS=0/15 BENIGN=0/6 BATTERY=PARTIAL` — no leg ran and nothing says the name matched no leg. UNCLEAR (1).
- c2-count `--fleet /nonexistent`, rc 2: same message as invocation 2, including `a bare git archive of the lane has no fleet parent` although a fleet WAS passed and is wrong. Slightly misleading (2).
- c2-count `--fleet F --config openat2`: `ENTRY=1/1 ... C2=PASS`, rc 0 (round 62's entry passes in the export).
- preflight `--only G99`: rc 2, `lane-preflight: unknown gate id for --only: G99`, no summary line (matches contract).
- preflight with `SHOKUNIN_ROOT=F`, `--only G01`: rc 0, G01 PASS — env fallback works.

## What a reader with no oral context can complete from the usage text alone

- Usage text lives in the module docstrings (c2-count lines 41–46, c1-battery line 39–41 and 28–30, preflight lines 1–20). `-h` prints only bare option names (no help strings) and none of that text, so `-h` alone teaches nothing about `--fleet`.
- From the docstrings: (1) yes — "pass `--fleet`" is explicit; (2) yes, and the error message itself finishes the job; (3) yes — usage line gives `--tool --work [--lane] [--fleet] [--only]`, lines 28–29 give the exit-2 case and the `--only` PARTIAL rule; (4) yes — preflight docstring gives the flags and the ENV/exit-2 rule.
- From `-h` plus the error messages only: 2 (message), 4b (message), 1 and 3 after one rc-2 round trip (message says `--fleet`). All four are completable; none needs oral knowledge once the docstring or the first error is read.

## Risks / limits
- Run at HEAD c8bfcc6, not the freeze commit; C2=FAIL is expected here (entry/probe/rows land later in the round).
- Preflight default `--root` (no `--root`) ran against cwd = export in 4c (G02 PASS 84 entries); not examined further.
- Only `--only CLEAN,B01` was run for the battery (as assigned), not the 22 legs.
- INFERENCE: n counts messages I found confusing; the count is mine.

VERDICT: BARE_EXPORT_OK=4/4 unclear_messages=2
