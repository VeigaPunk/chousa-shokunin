# R78SentinelA — boundary and evidence audit of the round-78 instruments (read-only)

Seat: R78SentinelA, lane chousa round 78, wave 1. Leaf, read-only, no dispatch, no network,
no lane/fleet git mutation. Frozen predicate set read first:
`corpus/evidence/round78/claims.md` (frozen 2026-11-04; base `53dbd512`, controls
`93e0432e`). QUALITY 141–145 read. Instruments audited at the controls bytes:

| instrument | sha256 (recomputed here) | matches claims table |
|---|---|---|
| `corpus/evidence/round78/matrix-battery-v5.py` | `5545a471…032b5af0` | yes |
| `corpus/evidence/round78/forge-battery.py` | `ba98db41…f1c5143` | yes |
| `corpus/evidence/round78/work-contract.py` | `e51d8917…d87ffa8a0` | yes |
| `corpus/evidence/round78/selfcheck.py` | `f5acdd82…c22837bf9af` | yes |

Method: every instrument was run from a **scratch mirror** of the lane (copy of
`corpus/evidence/round{74,75,76,77,78}` under `/fast/scratch/hyaku/chousa-r78/R78SentinelA/lane`,
plus a `git clone --shared` of the lane at `93e0432e` for `selfcheck --lane`), so a stray write
could not reach the lane tree. The mirror was verified unmodified after the runs
(`find <mirror> -newermt '2026-11-04 20:04' -type f` → empty). `LANE = HERE.parents[2]` and
`HERE` are the only path roots the instruments use (grep verified; no `parents[3]`), so the
mirror is behaviourally equivalent.

Trace set (explicit): `strace -f -y -s 4096 -e trace=openat,open,unlink,unlinkat,rmdir,mkdir,mkdirat,rename,renameat,renameat2,chdir`.
`-y` resolves `AT_FDCWD`/dirfd to a real directory, so relative paths are resolved per pid
(no unresolved paths remained). Every file creation necessarily passes `openat`/`mkdir`/
`rename`; `write`/`truncate`/`chmod`/`utimensat`/`link`/`symlink` were not traced (limitation,
not a gap in creation coverage).

---

## (a) Write scope — PASS, with one out-of-tree exception in the compiler

Commands, exit codes, and predicates (all four reproduced the frozen after-state on the
mirror):

| # | command | exit | predicate line |
|---|---|---|---|
| A1 | `strace … python3 -B <mirror>/corpus/evidence/round78/matrix-battery-v5.py --matrix <mirror>/corpus/evidence/round76/loader-matrix-v3.py --work <S>/work/battery --runs 1 --matrix-timeout 60` | 0 | `BATTERY=PASS forgers_rejected=11/11 positive=2/2 oracle=REJECTED` |
| A2 | `strace … python3 -B <mirror>/corpus/evidence/round78/work-contract.py --battery <mirror>/…/matrix-battery-v5.py --work <S>/work/wc` | 0 | `WORK_CONTRACT=PASS survived=yes unwritable_exit=2 file_exit=2` |
| A3 | `strace … python3 -B <mirror>/corpus/evidence/round78/selfcheck.py --lane <S>/selflane --verbose` | 0 | `SELFCHECK=PASS unresolved=0/3` |
| A4 | `strace … python3 -B <mirror>/corpus/evidence/round78/forge-battery.py --battery <mirror>/…/matrix-battery-v5.py --work <S>/work/forge --runs 1 --settle 0` | 0 | `FORGE_BATTERY=PASS forgers_handled=4/4 positive=1/1` |

Write-capable syscalls, successful ones, split by destination (receipt:
`R78SentinelA/write-scope.json`, `R78SentinelA/outside-writes.txt`):

| instrument | seen | failed/no-effect | inside `--work`/`--lane` | outside |
|---|---|---|---|---|
| matrix-battery-v5 | 12461 | 1797 | 9306 | **1358 × `openat /dev/null`** |
| work-contract | 479 | 6 | 379 | **94 × `openat /dev/null`** |
| selfcheck | 1 | 0 | **0** | 1 × `openat /dev/null` |
| forge-battery | 14476 | 1829 | 10895 | 1740 × `openat /dev/null` + **12 gcc temporary operations under `/tmp`** |

**No successful write landed beside any instrument, in the mirror lane tree, in the caller's
cwd, in `$HOME`, or in any other path.** The only destinations outside `--work` are:

1. `/dev/null` (`O_RDWR`), opened by `subprocess`/`git`/`cc` children — a device, not state.
2. `forge-battery` only: `cc -O2 -fopenmp -o <work>/perm <…>/perm.c -lcrypto` writes its
   compiler temporaries (`/tmp/ccEpG9VT.s`, `/tmp/ccyYb1QV.o`, `/tmp/cchoRxQB.res`,
   `/tmp/ccmi3nrF.cdtor.c`, `/tmp/ccfyyynx.cdtor.o`), and `cc` unlinks them itself (matching
   `unlink` lines present). They honour `TMPDIR`; they are transient, not state files. This is
   the **only** write outside `--work` attributable to a round-78 instrument, and it is
   `cc`'s, not the instrument's (severity: informational).

Per-instrument detail:

- **matrix-battery-v5** creates `--work/r78-<16 hex>` and per-subject dirs `<run>/<16 hex>/`
  with `<…>/subject.py` and `<…>/w`; `finally: shutil.rmtree(run)` removes only that run dir.
  After A1 the `--work` directory was **empty** — it deleted exactly what it created and left
  the caller's directory in place. `--work` as a regular file and an unwritable `--work` both
  exit 2 with a one-line diagnostic and no traceback (A2 CASE B/C, reproduced).
- **work-contract** writes only under `--work` (`a/`, `b/`, `c` and the battery's nested runs);
  it `rmtree`s a pre-existing `--work` at startup — that is the control's own documented
  contract, and it is the *control*, not the battery, that does the deleting.
- **selfcheck** performed **zero** successful writes. It reads `SKILL.md`,
  `corpus/QUALITY.md`, `corpus/lessons/round-77.md` and lane-local git metadata
  (`git -C <lane> ls-files|show|cat-file`), and creates no cache or state file beside itself
  or in `--lane`.
- **forge-battery** writes only under `--work` (receipts, `*.w`, `perm`, `a7-cache`,
  `forger-calls.log`).

---

## (b) Receipt self-containment — three defects (none changes a predicate)

`corpus/evidence/round78/controls/` holds six files, all `.txt`. Full table:
`R78SentinelA/receipt-audit.txt`.

1. **No receipt ends with an `# exit:` line.** All six place the exit line before the
   provenance trailer (`# exit:` → `# lane rev:` → `# <instrument> sha256:`), so the last
   line is a digest or a rev. A verifier that reads the final line for the exit code reads a
   hash. The `# exit:` lines themselves are present and agree with each file's predicate line
   (`0`/`PASS`, `1`/`FAIL`) in all six cases. Severity: **Low** (ordering, not content).
2. **`selfcheck-before.txt` carries no instrument digest** (no `# selfcheck sha256:` line).
   Every other receipt carries one, and all five present digests match the recomputed bytes.
   Severity: **Low** (the before-state cannot be tied to a specific counter build).
3. **`work-contract-before-v4.txt` carries no `# lane rev:` line.** Severity: **Low**.
4. **Two "after" receipts record a lane revision at which the instrument does not exist.**
   `forge-battery-after-v5.txt` and `work-contract-after-v5.txt` end with
   `# lane rev: 53dbd512d0ab70055338cb44898a6db70049537f (controls)`, but
   `git cat-file -e 53dbd512:corpus/evidence/round78/{forge-battery,work-contract}.py` returns
   **absent** (all four round-78 instruments are absent at `53dbd512`; they first appear at
   `93e0432e`). `claims.md` states the after state was "measured at controls `93e0432e`", and
   `selfcheck-after.txt` correctly records `93e0432e`. Severity: **Medium** — provenance
   contradiction with the frozen claims: a verifier that re-derives the after receipt at the
   recorded rev gets nothing, and the `(controls)` annotation points at a commit that is not
   the controls commit. Smallest remediation (post-freeze, therefore report-only): re-measure
   and record `93e0432e`, or drop the `(controls)` label from the two trailers.

Positive: the body of the two forge/work-contract receipts carries `BATTERY_PATH=` and
`BATTERY_SHA256=5545a471…`, so the battery under test is identified even though it has no
trailer of its own; and every digest that *is* present matches the bytes.

---

## (c) `cc` at run time — compile failure is handled, a missing compiler is not

`forge-battery.py:110` runs `subprocess.run(["cc", "-O2", "-fopenmp", "-o", <work>/perm,
<…>/perm.c, "-lcrypto"])` inside `main()`, guarded only by `if not perm.is_file():`.

| case | command | exit | stderr |
|---|---|---|---|
| compile fails (fake `cc` exiting 1) | `env -i PATH=<S>/bin-failcc /usr/bin/python3 -B <mirror>/…/forge-battery.py --battery <mirror>/…/matrix-battery-v5.py --work <S>/work/c2` | **2** | `forge-battery: cannot build the permutation enumerator: cc: fatal error: simulated toolchain failure` |
| `cc` absent from `PATH` | `env -i PATH=<S>/bin-nocc /usr/bin/python3 -B <mirror>/…/forge-battery.py --battery <mirror>/…/matrix-battery-v5.py --work <S>/work/c1` | **1** | 23-line `Traceback (most recent call last)` ending `FileNotFoundError: [Errno 2] No such file or directory: 'cc'`; stdout empty |

So: **a failing compile is correct** (exit 2, one-line diagnostic, no traceback). **A missing
`cc` is not**: `FileNotFoundError` is not caught, the process dies with a traceback and exit
**1**, which is the code the docstring reserves for `FORGE_BATTERY=FAIL`, and which the
frozen predicate reserves for a genuine verdict failure. An environment problem is thereby
indistinguishable, by exit code, from a scored failure — the round's C1 predicate would be
reported as failed on a host without a C toolchain, with an empty receipt (no `RECEIPT_LINES`
trailer, so `read_receipt` returns `integrity=None`). Severity: **Medium**.
Smallest remediation (report-only; the instrument is frozen): wrap the `subprocess.run` in
`try/except OSError` and return 2 with the existing diagnostic shape
(`forge-battery: cannot build the permutation enumerator: <exc>`).

---

## (d) Network / fleet repo / `.ufo/state/` / sibling lane — clean

Grep over the four instruments, the eight files under `forgers/`, and `claims.md`
(`urllib|requests|socket|http|urlopen|sftp|ssh|fleet|\.ufo|state/|sibling|/home/|projects`)
finds only:

- `selfcheck.py:42` — the string `"http"` inside `NOT_A_PATH`, a **filter** that discards
  URL-like tokens; it never fetches.
- `forgers/a2,a5d,a7` docstrings — provenance prose naming `.ufo/waves/round-77/…`; no read
  of that path.
- `claims.md:94` — the boundary sentence itself.

External commands spawned, exhaustively (`grep subprocess`):

| instrument | commands |
|---|---|
| matrix-battery-v5 | `sys.executable -B <matrix> --counter <subject> --work <…>` |
| forge-battery | `sys.executable -B <battery> …`; `cc …` |
| work-contract | `sys.executable -B <battery> …` |
| selfcheck | `git -C <lane> show|ls-files|ls-tree|cat-file` — always `-C` the `--lane` argument |

Reads stay inside the instrument's own lane: `LANE = HERE.parents[2]` →
`corpus/evidence/round7{4,5,6}` (battery positives/forgers, forge positive) and
`corpus/evidence/round78/forgers` (oracles). `selfcheck` reads `SKILL.md`,
`corpus/QUALITY.md`, `corpus/lessons/round-77.md` and lane git metadata. **No network socket,
no fleet-repo path, no `.ufo/state/`, no sibling lane, no package manager, no host question.**
PASS.

---

## Additional boundary observations (beyond the four asked questions)

**O1 — matrix children inherit the caller's cwd and the caller's full environment (Medium,
design limit, not a predicate).** `run_matrix` builds `env = dict(os.environ,
LOADER_MATRIX_CHILD_TIMEOUT="3")` and passes no `cwd=`, so every matrix under test runs in
whatever directory the verifier invoked the battery from, with every ambient variable. Under
`forge-battery` that includes `R78_PERM`, `R78_FORGE_CACHE` and **`R78_FORGE_LOG`, whose
parent directory is the directory holding the receipts**. Demonstrated with a probe matrix run
through the battery under the same three variables `forge-battery` sets
(`<S>/work/envprobe/envprobe.txt`, copied as `R78SentinelA/envprobe.txt`):

```
{'R78_PERM': '<work>/perm', 'R78_FORGE_CACHE': '<work>/a7-cache',
 'R78_FORGE_LOG': '<work>/forger-calls.log', 'LOADER_MATRIX_CHILD_TIMEOUT': '3'}
cwd=/home/vgpnk/Projects/shokunin
```

The probe wrote that file **into the battery's `--work` from a path derived only from the
environment**, which is the exploit path: a hostile matrix can address the receipt directory
and the caller's cwd with relative paths, i.e. it can write outside the `--work` it is given.
This is the same channel `a5d` already uses via `/proc/<ppid>/fd/1`; the `RECEIPT_LINES`
trailer detects the append, so the claim stands, but the *reach* is wider than the docstring's
"writes only under `--work`" framing. Smallest remediation (successor, not this freeze):
pass `cwd=<run dir>` and a scrubbed `env` (only the `R78_*`/timeout variables a given matrix
needs) to `subprocess.run`.

**O2 — `forge-battery` trusts a pre-existing `<work>/perm` (Low).** `if not perm.is_file():`
skips compilation, so an executable planted at that path by anything that wrote the caller's
`--work` earlier is used without checking. The caller owns `--work`, so this is a
self-inflicted surface, but the path is not derived from the `perm.c` digest.

**O3 — the battery does not kill the child's process group (Low, recorded timing limit).**
`subprocess.run(..., timeout=…)` reaps only the direct child. The `a5d` forger forks a
`setsid()` grandchild that sleeps 20 s and appends. In the A4 run (`--settle 0`) the receipt
read at exit had 113 lines and was scored `REFUSED`; the same file has **139 lines now**, i.e.
the append landed after the battery exited. Detection therefore depends on `forge-battery`'s
`--settle` exceeding the forger's delay (default 26 > 20). A forger that sleeps longer than
`settle` is not detected — consistent with the docstring's stated limits, but the limit is
timing-based, not only truncation-based. No stray processes remained afterwards
(`pgrep -af 'a5d-detached|a7-order-from-digest'` → none).

---

## Severity summary

| id | finding | severity | touches a predicate? |
|---|---|---|---|
| F1 | missing `cc` → traceback + exit 1 instead of exit 2 + diagnostic (c) | Medium | no (contract violation) |
| F2 | two "after" receipts record lane rev `53dbd512 (controls)`, where the instrument is absent (b) | Medium | no (provenance) |
| O1 | children inherit caller cwd + full env, incl. `R78_FORGE_LOG` → receipt dir (a-adjacent) | Medium | no (limit) |
| F3 | no receipt ends with `# exit:`; `selfcheck-before.txt` lacks a digest; `work-contract-before-v4.txt` lacks a lane rev (b) | Low | no |
| O2 | pre-existing `<work>/perm` is trusted without recompiling | Low | no |
| O3 | detached grandchild survives the battery; detection is settle-dependent | Low | no (recorded limit) |
| — | write scope of all four instruments (a) | **PASS** | — |
| — | network / fleet / `.ufo/state/` / sibling lane (d) | **PASS** | — |

No frozen instrument or receipt was edited. No claim is falsified: C1 and C2's predicate
lines reproduced unchanged on the mirror (A1–A4).

## Reproducibility

Scratch root `/fast/scratch/hyaku/chousa-r78/R78SentinelA/` held the mirror, the clone, the
work dirs and the raw strace logs (~53 MB, kept out of `/tmp`); receipts were copied to this
folder first and the scratch tree was deleted on yield. Artifacts in
`.ufo/waves/round-78/w1/R78SentinelA/`: `write-scope.json`, `outside-writes.txt`,
`strace-excerpt.txt`, `receipt-audit.txt`, `envprobe.txt`, and the stdout/stderr of A1–A4 and
of the two `cc` cases (`battery.*`, `work-contract.*`, `selfcheck.*`, `forge.*`, `c1.*`,
`c2.*`).

Tooling: none installed or upgraded (used host `strace`, `cc`, `python3 3.14.8`, `git 2.56.0`).
