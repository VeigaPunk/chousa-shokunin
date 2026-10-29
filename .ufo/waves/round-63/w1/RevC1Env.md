# RevC1Env — environment review of the C1 reference preflight and battery (round 63, w1)

Scope: `corpus/evidence/round63/controls/pos-ref-preflight.py` (sha256 prefix `07683086fd6c6b41`, matches the claims file)
and `corpus/evidence/round63/c1-battery.py` (prefix `0073fba73c89aaf8`, matches). Lane export: `git -C <lane> archive
62876ef90154714bfa806fbbec7890a9ff11b179` into scratch (no git metadata). The tool was copied to scratch as
`lane-preflight.py` (bytes unchanged). `tools/lane-preflight.py` does not exist in the lane at this revision, so the
reference candidate is the object under test. No network, no installs, no lane or fleet writes. Scratch deleted at the end.

## Findings (environment matrix, `--skip G08` unless noted)

| # | Condition | Outcome | Message tells reader what to pass? |
|---|---|---|---|
| 1 | export, no `--fleet` (parent has no `scripts/`) | ENV G01, exit 2 | Yes: "(pass --fleet DIR, or set SHOKUNIN_ROOT, or run inside a fleet layout)" |
| 1b | same, G08 not skipped | ENV G01, G08 PASS (exit 0), exit 2 | as above; the only G08 receipt in the export env |
| 2 | `--fleet /home/vgpnk/Projects/shokunin` | PASS 7/7, exit 0 | n/a |
| 3 | `--fleet <dir with no scripts/>` | ENV G01, exit 2 | MISLEADING: says "pass --fleet DIR" though `--fleet` was passed; does not name the path searched |
| 4 | `SHOKUNIN_ROOT=<missing dir>`, no `--fleet` | ENV G01, exit 2 | MISLEADING: says "set SHOKUNIN_ROOT" though it is set; does not name the path searched |
| 5 | cwd `/`, absolute `--root` and `--fleet` | PASS 7/7, exit 0 | n/a |
| 6 | cwd = export, `--root .` | PASS 7/7, exit 0 | n/a |
| 7 | `env -u HOME` | PASS 7/7, exit 0 | n/a |
| 8 | Python 3.9.25, 3.10, 3.11, 3.12, 3.13, 3.15 (uv-installed; 3.14 is system) | PASS 7/7 each, exit 0 | n/a |
| 8b | Python 3.8 | not run (not installed; not installed here) | — |
| 9 | PyPy 3.11.16 | FAIL G06 "exit=1", exit 1 | NO: detail is only `exit=1`; reader must rerun the selftest by hand |
| 10 | `PATH=<empty dir>`, skip G08 | FAIL G01 "cannot run: [Errno 2] ... 'bash'", exit 1 | Names `bash`, not PATH; classified FAIL, not ENV (see Contract note) |
| 10b | `PATH=<empty dir>`, full run | FAIL G01 and FAIL G08 (same message), exit 1; G02-G07 PASS | as 10 |
| 11 | `PATH` = a dir holding only a `bash` symlink (no coreutils, no gawk) | FAIL G01 "exit=2 .../sources-census.sh: line 88: dirname: comma", exit 1 | NO: detail is cut at 80 chars mid-word; no hint about coreutils or PATH |
| 12 | `--only G99` | exit 2, "unknown gate id for --only: G99" | Yes |
| 13 | `--only G03` | PASS 1/1, others SKIP, exit 0 | n/a |
| 14 | Battery env exactly (`env -i`, PATH kept, LC_ALL, HOME=cwd, TMPDIR, HYAKU_SCRATCH) | PASS 7/7, exit 0 | n/a |

No traceback was observed in any run (all stderr captured; only rows 3/4/12 and the battery's own usage lines wrote to stderr).

## Frozen battery, run against the export

- `c1-battery.py --tool <copy of ref> --lane <export> --fleet /home/vgpnk/Projects/shokunin --work <scratch>` under system
  Python 3.14: `CLEAN=1/1 DEFECTS=15/15 BENIGN=6/6 BATTERY=PASS`, exit 0. (Receipt only; the closure is the lane's, not mine.)
- Same battery under Python 3.9 with `--only CLEAN,B01`: CLEAN ok, B01 ok (`PARTIAL`, exit 0).
- Same battery under PyPy 3.11 with `--only CLEAN`: `CLEAN=0/1 ... BATTERY=PARTIAL`, the CLEAN leg FAILs (tool exit 1). The
  battery does not pin an interpreter; it runs the tool with its own `sys.executable`, so the verdict depends on it.
- Battery without `--fleet`: exit 2, "c1-battery: no census script under .../RevC1Env/scripts (pass --fleet DIR)". Clear.
- Battery with a missing tool path: `CLEAN=0/1 DEFECTS=0/15 BENIGN=0/6 BATTERY=FAIL`, exit 1 (matches the claim's before-line).

## Root causes

1. PyPy G06 FAIL (row 9). Not a tool bug; a fixture bug in the frozen selftest. `tools/freeze-check.py:450`:
   `json.dump(j, open(rp, 'w'))` leaves the handle unclosed. CPython closes it by refcount at once; PyPy does not flush
   before the next read, so the M19 fixture's `ready` file is read as truncated JSON (`JSONDecodeError`) and READY_DISPATCH
   and READY_IDENT fail (33/34). Reproduced three times (first run plus two reruns: `SELFTEST 33/34 pass` each time). The
   same selftest under CPython: `SELFTEST 34/34 pass`. The preflight reports this honestly as FAIL; the message does not say why.
   INFERENCE: the cause is the unclosed write, from the traceback-free failure pattern and the CPython/PyPy difference; I did
   not patch and re-run the frozen file (out of scope).
2. Missing `bash` (row 10) and missing coreutils (row 11) are both reported as FAIL. Row 11's cause is `sources-census.sh`
   running `dirname` with nothing on PATH.
3. ENV messages name neither the path searched nor the environment variable's value (rows 3, 4).

## Silent passes

- S1 (one exit-0 run). A root holding only `corpus/README.md` (empty `corpus/knowledge/`, no `corpus/lessons/`), with
  `--fleet F --only G02,G03`: `GATE G02 knowledge-index PASS 0 entries indexed`, `GATE G03 lesson-gate PASS 0 lessons carry
  ## Gate`, `PREFLIGHT=2/2 FAILED=none ENV=none SKIPPED=G01,G04,...`, exit 0. Two gates pass over zero items. `g02` and `g03`
  use `files = [] if not dir` and then pass on an empty list; an absent directory is not a failure.
- S2 (gate-level, run fails overall). Empty root (`--root <empty dir> --fleet F --skip G08`): G03 PASS "0 lessons carry
  ## Gate" while G01, G02, G04-G07 FAIL correctly. Same cause as S1.
- S3 (false detail, not a pass verdict). `g01` prints the literal `census_findings=0` on every PASS. On the export the
  census validate exits 0 and prints 5 `W04` lines (duplicate URLs across scopes; `grep -c` gives 5 W, 0 E). The detail is
  false text; the PASS verdict itself is consistent with the census contract ("0 clean or warnings").

Count used for the verdict: `silent_passes` = runs that exit 0 while a gate passed over zero items = 1 (S1).

## Contract note

The tool doc says a gate that "could not run" should yield ENV (exit 2 when no gate failed). A missing `bash` is "could not run",
but the code classes an OSError as FAIL (`run()` returns None and the gate returns FAIL). The claim text names ENV only for the
census script. Either reading is defensible; the code and the contract disagree and the claim does not settle it.

## Battery coverage gaps (env-class)

The battery's CLEAN and benign legs keep PATH from the host, so no leg removes `bash`, coreutils or gawk, runs under a second
interpreter, points `--root` at an empty or partial tree, or checks ENV message text. Rows 3, 4, 9, 10, 11 and S1-S3 would not
move `BATTERY=`. This is consistent with the claim's named limit ("does not check the gate names or messages"), but the
interpreter and PATH cases are not in the named limits. Recommend the integrator either names them as limits or adds legs.

## Recommendations for the integrator (not applied; the reference is frozen)

- G02/G03: fail when the directory they scan is absent (or when the scanned set is empty and the root has no `corpus/`).
- G01: parse the census W/E counts for the detail; drop the literal `census_findings=0`.
- ENV/FAIL details: name the path searched and the env var value; for G06/G07/G08 carry the last FAIL line of the selftest
  output, not only `exit=N`; for a missing binary, say "put <name> on PATH".
- Cut the stderr detail at a word boundary, not at 80 characters.
- Freeze-check: close the `open(rp, 'w')` handle (`tools/freeze-check.py:450`) in a next-round fix, not in this wave.

## Commands and their observed outcome (abbreviated)

- `python3 -B lane-preflight.py --root <export> --fleet /home/vgpnk/Projects/shokunin --skip G08` -> `PREFLIGHT=7/7 ... exit 0`
- `... --root <export>` (no fleet) -> `GATE G01 census ENV no sources-census.sh (pass --fleet DIR, ...)`, `PREFLIGHT=7/8 FAILED=none ENV=G01`, exit 2
- `env PATH=<emptybin> /usr/bin/python3 -B ... --skip G08` -> `GATE G01 census FAIL cannot run: [Errno 2] ... 'bash'`, exit 1
- `pypy3.11 -B lane-preflight.py ...` -> `GATE G06 freeze-selftest FAIL exit=1`, `PREFLIGHT=6/7 FAILED=G06`, exit 1
- direct `pypy3.11 -B tools/freeze-check.py --selftest --lane-root <export> --work <dir>` -> `SELFTEST 33/34 pass`, rc 1 (x3); CPython -> `34/34`, rc 0
- `python3 -B c1-battery.py --tool <copy> --lane <export> --fleet ... --work ...` -> `CLEAN=1/1 DEFECTS=15/15 BENIGN=6/6 BATTERY=PASS`, exit 0
- `pypy3.11 -B c1-battery.py ... --only CLEAN` -> `CLEAN=0/1 DEFECTS=0/15 BENIGN=0/6 BATTERY=PARTIAL`, exit 0 (CLEAN leg FAIL)
- `python3 -B lane-preflight.py --root <fixture with README only> --fleet ... --only G02,G03` -> both PASS "0 entries/0 lessons", exit 0
- Live lane `--root <lane> --fleet ... --only G01` (read only, TMPDIR scratch) -> `GATE G01 census PASS exit=0 census_findings=0`, exit 0

Not run: Python 3.8; PyPy with G08; a PATH holding coreutils but not gawk; the full battery under PyPy; any check that needs the
network (none used). Installs: none. Scratch `/fast/scratch/hyaku/chousa-r63/RevC1Env/` removed before yield.

Counts: ENV_FAILURES = 7 tool runs that did not pass because of the environment (rows 1, 3, 4 ENV; 9, 10, 10b, 11 FAIL).
Row 1 is the designed ENV for a non-fleet root; it is counted because the run did not pass.

VERDICT: ENV_FAILURES=7 silent_passes=1
