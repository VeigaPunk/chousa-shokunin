# R77SentinelA — boundary audit of the round-77 instruments

Seat: sentinel, wave w1, round 77. Leaf member: no subagent dispatch, no network, no production
edits, no lane/fleet git mutation. Every clone, fixture and work dir lived under
`/fast/scratch/hyaku/chousa-r77/R77SentinelA/` and was deleted before this report (the battery's own
`finally` removed its work dirs; the remaining scratch tree was `rm -rf`'d at the end).
Nothing under the lane was created, modified or deleted by this seat: the only lane writes are this
report and `receipts/` beside it.

Lane read at: `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin rev-parse HEAD` =
`9fcfb70ba6f202506dfd55f71917dc2d31b3f825` (the tree also carried sibling seats' uncommitted edits;
the audited instruments are the frozen bytes, hashes below).

Audited bytes (all match `corpus/evidence/round77/claims.md`):

| file | sha256 |
|---|---|
| `corpus/evidence/round77/matrix-battery-v4.py` | `155fafb1…f106a3d` (full in `receipts/00-static-scan.txt`) |
| `corpus/evidence/round77/c3-count.py` | `32b76565…062335d` |
| `corpus/evidence/round77/forgers/forge-order-matrix.py` | `e7a12850…767801c6` |
| `corpus/evidence/round77/forgers/forge-order-matrix-table.py` | `3182dcfb…ae232b43` |
| `corpus/evidence/round77/forgers/forge-order-matrix-block.py` | `02e54d85…d876709f` |
| `corpus/evidence/round76/loader-matrix-v3.py` | `b79d6441…5c81913f` |

Note on scope wording: the assignment names "the two oracle files"; `matrix-battery-v4.py:ORACLES`
registers **three** (`summary-only`, `contract-table`, `block-position`). All three were audited.

Predicate re-run twice for the trace (both exact, both exit 0):

```
$ cd /fast/scratch/hyaku/chousa-r77/R77SentinelA
$ strace -f  -e trace=network,openat -o trace-predicate.txt \
    python3 -B <lane>/corpus/evidence/round77/matrix-battery-v4.py \
    --matrix <lane>/corpus/evidence/round76/loader-matrix-v3.py --work $PWD/work
BATTERY=PASS forgers_rejected=11/11 positive=2/2 oracle=REJECTED     rc=0
$ strace -fy -e trace=network,openat -o trace-predicate-y.txt … --work $PWD/work2
BATTERY=PASS forgers_rejected=11/11 positive=2/2 oracle=REJECTED     rc=0
```
Receipts: `receipts/01-predicate-under-strace.out`, `receipts/01-predicate-fd-annotated.out`.
The `-y` run is the authoritative one: it annotates every dirfd, so each relative `openat` resolves to
an absolute path instead of being guessed.

---

## Verdicts

| # | Item | Verdict |
|---|---|---|
| B1a | no network socket in battery, c3-count or the three oracles (static + `strace`) | **PASS** |
| B1b | no credential read by the instruments | **PASS** |
| B1c | no write outside `--work` during the predicate | **PASS** (0 of 9313 write opens) |
| B2a | oracle `.state` can only land in the battery's work dir | **PASS** (with the S4 limit) |
| B2b | `--work` omitted → usage error, exit 2, nothing written | **PASS** |
| B2c | `--work` unwritable → "usage error, exit 2" | **FAIL** — exit **1** with a traceback (S2) |
| B2d | nothing written into the lane by any failing `--work` case | **PASS** |
| B3a | `c3-count.py` never writes to the lane | **PASS** (zero write syscalls) |
| B3b | `--lane` outside the lane resolves "relative to a lane-root guard" | **NO GUARD EXISTS** (S3) |

S1 (a destructive `--work` delete) is a boundary defect found inside item B2 and is reported below.

---

## B1 — sockets, credentials, writes

**Static.** `grep -nE 'socket|urllib|http|requests|netrc|ssh|credential|keyring|expanduser|environ'`
over the battery, `c3-count.py` and all three oracles returns exactly one line,
`matrix-battery-v4.py:148: env = dict(os.environ, LOADER_MATRIX_CHILD_TIMEOUT=CHILD_TIMEOUT)`
(`receipts/00-static-scan.txt`). No `socket`, `urllib`, `http`, `requests`, `netrc`, `keyring`,
`expanduser`, `/proc` constant or `$HOME` join exists in the instruments.

**Dynamic.** `strace -fy -e trace=network,openat` over the full predicate (154 747 trace lines):

- `socket(`/`connect(`/`bind(`/`sendto(`/`recvfrom(`: **0** occurrences.
- `openat` with `O_WRONLY|O_RDWR|O_CREAT`: 9 313 opens over 3 734 distinct targets, **all 9 313 under
  the `--work` directory**; `targets_outside_work=0`, `unresolved=0`
  (`receipts/01a-write-target-resolution.txt`). The only non-`--work` write-flagged opens are
  `2716` opens of `/dev/null` (`subprocess.DEVNULL` for child stdin), which cannot carry data.
- Reads: 137 357 opens over 4 302 targets — `/usr` 70 822 (CPython stdlib), `<work>` 54 529,
  `/home` 7 281, `/etc` 4 259, `/proc` 465. Lane read targets: 21 (237 opens), lane write targets: 0.
- Credential-name matches (`id_rsa|.netrc|.ssh/|.aws|.git-credentials|.password|keyring|shadow`): **0**.
  `/home` reads outside the lane are only `~/.local/lib/python3.14/site-packages`,
  `~/.config/git/config`, `~/.config/git/attributes` (the child `git` calls in the loader matrix).
- `/proc` targets: two `/proc/<pid>/cmdline` (the `seed-leak` forger's designed probe), two
  `/proc/<pid>/fd/1`, one `/proc/self/maps`. No `/proc` write.

Command and exit code for the traced run: the two `strace … --work $PWD/work{,2}` invocations above,
`rc=0`, stdout ending in the exact predicate line.

Limits (recorded): the battery cannot sandbox the *matrix under test* — that is arbitrary code the
caller supplies and it inherits the caller's privileges; the `--work` argument is the only containment
it is handed. B1c proves the battery's own and the frozen subjects' writes, not a candidate's.

## B2 — the oracle state file and the `--work` argument

**B2a — state file containment: PASS.** `salted_copy()` writes every subject and every oracle copy to
`work/<16-hex>/subject.py`, and each oracle computes its state path as
`Path(__file__).resolve().with_suffix(".state")`, i.e. `work/<16-hex>/subject.state`. In the traced run
the only `.state` write targets are three paths of that shape, **0 outside `work`**
(`receipts/01b-state-containment.txt`). Belt: each oracle calls `refuse_inside_worktree()` first and
exits 2 before creating the state file when `git -C <dir> rev-parse --show-toplevel` succeeds:

```
$ cd /fast/scratch/.../probe2f/repo && git init -q . && cp <lane>/…/forge-order-matrix.py ./oracle.py
$ python3 -B ./oracle.py --counter x --work y
oracle.py: refusing to run inside the git worktree /fast/scratch/.../probe2f/repo; copy the probe outside it first
rc=2      # no oracle.state created (receipts/02f-oracle-worktree-guard.txt)
```

**B2b — `--work` omitted: PASS.**

```
$ python3 -B <lane>/corpus/evidence/round77/matrix-battery-v4.py \
    --matrix <lane>/corpus/evidence/round76/loader-matrix-v3.py
matrix-battery-v4.py: error: the following arguments are required: --work      rc=2
```
Under `strace -f -e trace=network,openat,mkdirat,unlinkat`: zero write-flagged `openat`, zero
`mkdirat`, zero `unlinkat`, zero sockets — nothing was written anywhere, so nothing into the lane
(`receipts/02a-work-omitted.stderr`, and the lane fingerprint below).

**B2c — `--work` unwritable: FAIL against the instrument's own exit contract.** The module docstring
says `Exit: 0 BATTERY=PASS · 1 BATTERY=FAIL · 2 usage/env`, and `main()` returns 2 for a missing
matrix or bad `--runs`/`--matrix-timeout`, but the `work.mkdir()` is unguarded:

```
$ mkdir ro && chmod 500 ro
$ python3 -B <lane>/…/matrix-battery-v4.py --matrix <lane>/…/loader-matrix-v3.py --work $PWD/ro/w
PermissionError: [Errno 13] Permission denied: '…/probe2b/ro/w'                    rc=1
$ : > afile; … --work $PWD/afile
FileExistsError: [Errno 17] File exists: '…/probe2b/afile'                          rc=1
$ mkdir exists-ro && chmod 500 exists-ro; … --work $PWD/exists-ro
MATRIX_PATH=… / MATRIX_SHA256=… / RUNS=2 … / MATRIX ORDER 0 …      (stdout already emitted)
PermissionError: [Errno 13] Permission denied: '…/probe2j/exists-ro/bc939ae1c2887788'   rc=1
```
Receipts: `receipts/02b-…`, `02c-…`, `02j-…`. Consequences: (i) an environment failure is
indistinguishable from `BATTERY=FAIL` to any caller that checks the exit status alone (both are 1);
(ii) in the third case the header lines are already on stdout, so a `BATTERY=` grep finds nothing but
the run looks started; (iii) in the third case the caller's directory `exists-ro` was **deleted**
(see S1). No lane file was touched in any of the three cases.

**B2d — nothing into the lane: PASS.** Lane fingerprint before/after the traced predicate
(`git status --porcelain` + `ls -la --time-style=full-iso corpus/evidence/round77/forgers/`) differs
only by a sibling seat's report file, and the forgers directory keeps its three files and their
mtimes; `find <lane> -name '*.state'` is empty. All my failing-`--work` probes ran with `cwd` inside
scratch and absolute lane paths, and the trace shows 0 lane writes.

## B3 — `c3-count.py`

**B3a — never writes: PASS.**

```
$ strace -f -e trace=network,openat,unlinkat,mkdirat,rename -o trace-c3.txt \
    python3 -B <lane>/corpus/evidence/round77/c3-count.py --lane <lane> \
    --base a519fb0a80cf52c7988713c1f05b3ce8440fedda --rev HEAD
C3-1 PASS … C3-4 FAIL numstat added=0 deleted=0 … C3=FAIL checks=4/5      rc=1
```
(`C3-4` fails only because the C2 landing was still uncommitted in the working tree at audit time;
that is a state fact, not a finding.) The trace has **zero** write-flag `openat`, zero `unlinkat`,
zero `mkdirat`, zero `rename`, zero sockets (`receipts/03a-c3-lane-run.out`, `.stderr` empty).
Its only effects are `read_text()` on the target and `git -C <lane> diff --numstat`, both read-only.

**B3b — no lane-root guard exists.** `--lane` is taken literally and joined with the relative
`corpus/evidence/round76/claims.md`; the only containment is that join plus `is_file()`. Measured:

```
$ … --lane <scratch>/emptydir            c3-count: missing …/emptydir/corpus/evidence/round76/claims.md   rc=2
$ … --lane <lane>/corpus                 c3-count: missing …/chousa-shokunin/corpus/corpus/evidence/round76/claims.md   rc=2
$ … --lane /home/vgpnk/Projects/shokunin c3-count: missing /home/vgpnk/Projects/shokunin/corpus/evidence/round76/claims.md   rc=2
$ … --lane <scratch>/nongit  (copy of the target, no repo)
    c3-count: git: warning: Limiting comparison with pathspecs is only supported if both paths are directories. …   rc=2
$ … --lane <scratch>/fakerepo (fresh git repo outside the lane, same relative path, appended block)
    C3-1..C3-5 PASS → C3=PASS checks=5/5      rc=0
```
Receipts: `receipts/03b-c3-lane-resolution.txt`, `receipts/03c-c3-fake-lane-scores.out`. So the
counter is a general checker over any directory, not a lane-bound one: it fails closed (exit 2) when
the relative target is absent or the directory is not a repository, but a same-shaped tree anywhere
scores `C3=PASS`. For C2 that is acceptable only because the predicate command pins `--lane .` from
the lane root and the receipt records it; the verdict itself carries no lane identity.

---

## Findings

### S1 — HIGH — `--work` is unvalidated and unconditionally deleted (`shutil.rmtree`)

`matrix-battery-v4.py:main()` resolves `--work` and, in `finally:`, runs
`shutil.rmtree(work, ignore_errors=True)` on it. There is no check that `--work` is outside `LANE`,
that it is empty, that the battery created it, or that it is not `/` or `$HOME`.

Exploit path (measured, scratch fixture only): point `--work` at any existing directory.
`--work <lane root>` — or `--work .` run from the lane root, the natural mistake when adapting the
predicate command — recursively deletes the lane tree (`corpus/`, `tools/`, `.ufo/`). The delete also
runs on every failure path, so a crashed or misconfigured run still destroys the caller's directory.

Evidence:
```
$ mkdir -p fakelane/corpus/evidence/round76 fakelane/keepdir; echo sentinel > fakelane/SENTINEL.md
$ python3 -B <lane>/…/matrix-battery-v4.py --matrix trivial-matrix.py --work $PWD/fakelane
BATTERY=FAIL forgers_rejected=0/11 positive=0/2 oracle=REJECTED          rc=1
$ test -e fakelane || echo GONE      →  GONE: fakelane, SENTINEL.md and keepdir/inner.txt removed
```
(`receipts/02d-after-tree.txt`, `02d-work-preexisting-dir-deleted.out`). Second witness: the
`exists-ro` directory of B2c was deleted by the failed run (`receipts/02j-…`). Third witness: after
each successful predicate run `--work` no longer exists, so the receipt cannot show what the run
wrote — the reason this audit had to trace it.

Impact: data loss in the lane or in `$HOME` on a single mistyped argument; no guard, no confirmation,
no dry-run. The frozen predicate itself is unaffected (it still prints the exact line, exit 0), so
this is a boundary defect to route, not a claim failure — and the frozen instrument must not be edited
by a seat.

Smallest remediation: refuse `--work` when `work == LANE or LANE in work.parents`, and delete only a
private child the battery itself created (`work / f"battery-{secrets.token_hex(8)}"`), leaving a
caller-supplied directory in place.

### S2 — MEDIUM — environment failures exit 1, not the documented 2

`work.mkdir()` and `salted_copy()` raise uncaught `PermissionError`/`FileExistsError`; the process
exits 1 with a traceback, the same status as `BATTERY=FAIL`. In the existing-but-unwritable case the
`MATRIX_*`/`RUNS=`/`ORDER` header lines have already been printed. Impact: a caller that keys on exit
status alone reads an environment failure as a scored battery failure; a caller that greps `BATTERY=`
sees a truncated run. The frozen predicate (exact line, exit 0) is unaffected.
Evidence: `receipts/02b-…`, `02c-…`, `02j-…`. Smallest remediation: wrap the work-dir setup and the
`score()` call in `try/except OSError` → `print(..., file=sys.stderr); return 2`.

### S3 — LOW — `c3-count.py` has no lane-root binding

Stated in B3b: `--lane` is used verbatim, any directory with the relative target is scored, and a
foreign repository reaches `C3=PASS checks=5/5` (`receipts/03c-…`). Read-only, so no containment
impact; the impact is evidential — a `C3=PASS` receipt does not by itself identify which tree was
scored. Smallest remediation: after resolving, require
`git -C lane rev-parse --show-toplevel` to equal `LANE` (the script's `HERE.parents[2]`), exit 2
otherwise, and print the resolved target path.

### S4 — LOW — oracle containment is a git-worktree check, not a lane check

`refuse_inside_worktree()` refuses only when `git rev-parse` succeeds for the containing directory.
Measured: in a plain directory the oracle runs and writes `<name>.state` beside itself
(`receipts/02g-oracle-nongit.txt`, `oracle.state` = `1`); with `git` absent from `PATH` it raises
`FileNotFoundError` and exits 1 (`receipts/02h-…`) — still before the state write, so writes stay
fail-closed. Impact: a lane copy without `.git` (exported tree, `git archive` extraction, a `GIT_DIR`
redirect) that is run in place writes a state file into the lane, and the guard adds a `git`
dependency to every oracle invocation. In the committed lane the guard holds (B2a). Smallest
remediation: replace the subprocess with a path test against the script's own lane root
(`HERE.parents[2]`) and require an explicit state directory inside a temp/work tree.

### S5 — INFO — inherited environment and inherited git config reach the child runs

`run_matrix()` passes `dict(os.environ, LOADER_MATRIX_CHILD_TIMEOUT=CHILD_TIMEOUT)` to every matrix
and subject, so the candidate sees the operator's whole environment (QUALITY 137 lists `env` as a
channel; the battery adds no class/label there, but it also scrubs nothing). The loader matrix's
fixture `git` calls inherit the operator's global config: the trace reads
`~/.config/git/config` and `~/.config/git/attributes`. A global `commit.gpgsign` or `core.hooksPath`
would change fixture behaviour on another host, i.e. the predicate is not host-independent.
Smallest remediation: pass a minimal env to children (`PATH`, `LOADER_MATRIX_CHILD_TIMEOUT`, and
`HOME`/`GIT_CONFIG_GLOBAL`/`GIT_CONFIG_SYSTEM` pointed at scratch) — but note this changes the
instrument's child contract, so it belongs to a successor freeze, not to a post-data edit.

---

## What this audit does not establish

- It does not re-score C1 or C2. The predicate line reproduced exactly twice at the audited bytes,
  which is consistency, not promotion.
- It does not prove arbitrary-candidate containment: the matrix under test is unconstrained code
  (B1 limits).
- It does not prove the absence of other lanes' or tools' behaviour; only these five instrument
  files and the predicate's own process tree.
- The two control twins (`--no-permute`, `--no-content`) were not re-run; the assignment's surface
  was boundary behaviour.

## Tooling

No tool was installed or upgraded: `strace`, `python3` (3.14.8), `git` (2.56.0) were already present
and sufficient; no pacman transaction was attempted (host guard in force).

## Receipts (this directory)

`receipts/00-static-scan.txt`, `01-predicate-under-strace.out`, `01-predicate-fd-annotated.out`,
`01a-write-target-resolution.txt`, `01b-state-containment.txt`, `02a-work-omitted.stderr`,
`02b-work-unwritable.stderr`, `02c-work-is-file.stderr`, `02d-work-preexisting-dir-deleted.out`,
`02d-after-tree.txt`, `02e-nested-work-leftovers.txt`, `02f-oracle-worktree-guard.txt`,
`02g-oracle-nongit.txt`, `02h-oracle-git-absent.stderr`, `02j-work-existing-unwritable.txt`,
`03a-c3-lane-run.out`, `03a-c3-lane-run.stderr`, `03b-c3-lane-resolution.txt`,
`03c-c3-fake-lane-scores.out`.

One further measured wart, for completeness: `--work` with nonexistent parents is created with
`parents=True` and the ancestors are left behind after the run (`a/`, `a/b/` in
`receipts/02e-nested-work-leftovers.txt`) — a write outside `--work` that is bounded to the path
prefix; `parents=False` or removing the created ancestors would close it.
