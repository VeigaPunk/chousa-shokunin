# R98SentinelC1 — side-effect audit at F (aac826848dda5029ba459568b29d9a92176dc2b6)

Seat: R98SentinelC1 (leaf, sentinel). Scope: side effects of `tools/search-rerun.py --selftest`, the C1 battery
`corpus/evidence/round98/selftest-controls-r98.py` (with and without `--no-regression`), and
`corpus/evidence/round98/entry-controls-r98.py`. Attacked tree: a shared clone of the lane at F, `$S/repo`
(`S=/fast/scratch/hyaku/chousa-r98/R98SentinelC1`), HEAD verified = aac826848dda5029ba459568b29d9a92176dc2b6.
No batteries were run against the live lane. Lane state was only read (`git -C <lane> rev-parse HEAD`, `stat`).

Tools: `/usr/bin/strace` 7.2 (already present; not installed by this seat), Python 3.14.8, git 2.56.0. No package,
binary or sudo action by this seat. Scratch `$S` is deleted before yield; every receipt cited is copied to
`.ufo/waves/round-98/w1/` with prefix `R98SentinelC1-`.

## Summary

| # | axis | result | exit / predicate observed |
|---|------|--------|---------------------------|
| 1 | self-test I/O (`--selftest`) | no file write, no socket; 2 git children; no lane access | rc 0, `SEARCH_RERUN_SELFTEST: PASS cases=67/67` |
| 2 | `GITFOO` / `GIT_*` env leak (r26, in-process) | no leak in 4 variants | rc 0, `env_diff_after_selftest {}` ×4 |
| 3 | C1 battery `--no-regression` under strace | writes only under `--work` + lane `.git/index` (lock churn, one rewrite with identical bytes); no socket | rc 0, `SELFTEST_CONTROLS_R98=PASS` |
| 3b | C1 battery full (regression leg) under strace | writes under `--work` only (≈1.33 M file creates in 55 full-tree clone checkouts); lane `.git/index.lock` ×12, no rewrite | rc 0, predicate line equal to claim |
| 4 | `entry-controls-r98.py` under strace | no write, no socket, no index change; reads lane working tree (not committed bytes) | rc 0, `ENTRY_CONTROLS_R98=PASS` |

Findings (defects of wording or instrument), ranked:

### F1 — C1 named limit (e): "'no write, no socket' is observed (NO_WRITE leg for writes)" is false as stated
The NO_WRITE leg observes only (a) that the empty `HOME`/`TMPDIR`/cwd directory stays empty and (b) that the lane's
`git status --porcelain` and `git diff` digest are unchanged (`selftest-controls-r98.py`, `main()`, "no-write" block).
It cannot see a write to any other path. Demonstration (mutant = the F tool plus one line at the top of `selftest()`
writing `/fast/scratch/hyaku/chousa-r98/R98SentinelC1/leak/marker.txt`; `$S/mut/search-rerun.py`):

    python3 -B $S/repo/corpus/evidence/round98/selftest-controls-r98.py --root $S/repo --work $S/w-leak \
        --tool $S/mut/search-rerun.py --no-regression          → rc 0
    CASE no-write rc=0 left=[] status_same=True diff_same=True ok
    SELFTEST_CONTROLS_R98=PASS
    marker.txt present, content "outside work"

Receipts: `R98SentinelC1-nowrite-outside-write-battery-stdout.txt`, `R98SentinelC1-mutant-outside-write.py.txt`.
Consequence: K4 ("writes outside `--work` (self-test: anywhere)") is not enforced by any battery leg; at F only an
external trace (this audit) shows that the self-test writes nothing anywhere. The F tool itself does not write (F1
is an instrument gap, not a tool defect; the strace of check 1 below shows the tool itself writes nothing).

### F2 — C1 named limit (e) is incomplete: what the self-test's processes actually touch
Observed by `strace -f -qq -e trace=file,network,process` on `python3 -B tools/search-rerun.py --selftest`
(receipt `R98SentinelC1-strace-selftest-raw.txt`, summary `R98SentinelC1-strace-selftest-summary.txt`):

- two git children (pids 3084467 `cat-file blob 0000…`, 3084517 `rev-parse`), each `git -C /dev/null` — matches (e);
- each git child opens `/dev/null` **O_RDWR** (`openat(AT_FDCWD, "/dev/null", O_RDWR) = 3`), not read-only as (e) says;
  the python process opens it read-only (`O_RDONLY|O_CLOEXEC`, r30);
- each git child reads the host's global git config (`access("/etc/gitconfig")` ENOENT, `openat("/home/vgpnk/.config/git/config", O_RDONLY) = 3`,
  `access("/home/vgpnk/.gitconfig")` ENOENT) — `git_env()` strips `GIT_*` variables only, not user config files;
- `git` is resolved through `PATH`: twelve `execve` probes fail with ENOENT, `/usr/bin/git` succeeds.
- no write-capable open on any regular file; no `rename/unlink/mkdir/chmod/...`; no `socket`/`connect`: 0 lines each.

None of this changes r29/r34's expectations (the repository open fails with rc 128 both runs, observed), but (e)'s
inventory is not the whole inventory.

### F3 — r26 `GITFOO` mutation does not leak (held)
`envleak.py` loads the F tool, snapshots `os.environ`, calls `selftest()` and diffs the environment
(receipt `R98SentinelC1-envleak-results.txt`, scripts `R98SentinelC1-envleak.py.txt`, `…-envleak2.py.txt`):

    GITFOO=preset-val → rc 0 last SEARCH_RERUN_SELFTEST: PASS cases=67/67 ; env_diff_after_selftest {} ; GITFOO after 'preset-val'
    GITFOO unset      → rc 0 ; env_diff_after_selftest {} ; GITFOO after None
    GIT_DIR=/nonexistent GIT_NO_LAZY_FETCH=0 GIT_NO_REPLACE_OBJECTS=0 GITFOO=x → rc 0 ; env_diff {} ; GIT_DIR after '/nonexistent'
    GIT_TRACE=1 GIT_CONFIG_PARAMETERS=… GITFOO=x → rc 0 ; env_diff {}
    selftest() twice in one process → 0 0 ; env_same True

`r26`'s set/restore is inside `try/finally`; the planted `GIT_*` block is restored the same way.

### F4 — C1 battery under `--no-regression`, on the clone's `.git/index` (the docstring is exact; the index is touched)
Command: `strace -f -qq -e trace=file,network,process -o $S/strace-c1nr.txt python3 -B $S/repo/corpus/evidence/round98/selftest-controls-r98.py --root $S/repo --work $S/w-c1nr --no-regression`
→ rc 0, `CASE positive … ok`, `CASE external-r97 EXTERNAL_R97_KILLED=35/37 setup=0 survivors=u01-verify-return-0,u05-tree-files-jj`,
`SELFTEST_CONTROLS_R98=PASS`. Receipts: `R98SentinelC1-c1-no-regression-stdout.txt`, `R98SentinelC1-strace-c1-no-regression-summary.txt`.

- Git subcommands on the lane root: `show` 30, `status --porcelain` 12, `diff` 12 (the docstring's list, exact). The
  `cat-file blob`/`rev-parse` (194 each) are the self-test children.
- `.git/index`: mtime 00:06:02.590 → 00:07:42.104, sha256 `c2dc9db45995886d…` before and after (bytes identical). Strace:
  12× `openat(".git/index.lock", O_RDWR|O_CREAT|O_EXCL)`, 11× `unlink(index.lock)`, 1× `rename(index.lock → index)`.
  The docstring says "git may refresh the index stat cache while doing so" — that is accurate; it is a rewrite of the
  index file by git, which the sentence "it never writes a lane file itself" does not say (the battery code writes no lane file; git does).
- Opens for write outside `--work`: only the 12 `index.lock` creations (above). `/dev/null O_RDWR` ×440 (git children).
  Inside `--work`: 712 write-capable opens (mutant files, fixtures) — all removed at exit except the empty `w-c1nr` parent.
- No socket. `execve`: 717 python3 (self-test runs), 442 `/usr/bin/git`, plus the battery's own calls.
- The battery's `--no-regression` output has no `REGRESSION_R95` field, as the docstring says.

### F5 — C1 battery, full run (regression leg `round95/rerun-controls-r95.py`), side effects are inside `--work` but the docstring under-describes them
Command: `strace -f -qq -e trace=openat,open,rename,renameat2,unlink,unlinkat,mkdir,mkdirat,rmdir,execve,socket,connect,creat,chmod,fchmodat,truncate,link,linkat,symlink,symlinkat -o $S/strace-full.txt python3 -B $S/repo/corpus/evidence/round98/selftest-controls-r98.py --root $S/repo --work $S/w-full`
→ rc 0; `POSITIVE=1/1 KILL_REQUIRED=35/35 DO_NOTHING_REFUSED=1/1 PRIOR_R97_KILLED=34/34 R96_MUTANTS_KILLED=23/23 EQUIVALENT_SURVIVED=3/3 ORACLES_REJECTED=5/5 NO_WRITE=1/1 REGRESSION_R95=2/2 EXTERNAL_R97_KILLED=35/37 BASE_KILLED=12/37 CASES=67`, `SELFTEST_CONTROLS_R98=PASS`. Wall 1088.95 s under strace.
(The predicate line equals the claim's line field for field.)

- Under `--work`: the regression leg runs `git clone --shared --no-checkout` and then `git -C <clone> checkout -q --detach 7b2373…`
  (rerun-controls-r95.py line 172) **55 times** (`execve` of `/usr/bin/git` with that argv, 110 lines = 55 × unfinished/resumed).
  Each checkout writes the whole lane tree (~25 k files; 1,330,340 `O_WRONLY|O_CREAT|O_EXCL` relative-path opens) and
  `.git/logs/HEAD` appends (165 + 110) in the clone; `git init/add/commit` run on fixtures; 385 relative `symlink()` calls
  (tracked symlinks recreated by checkouts). The docstring's "Read-only on the lane: git archive, git clone --shared into --work"
  is correct for the lane but omits these mutating git commands in `--work`. Not a lane write.
- Attribution caveat [INFERENCE with evidence]: strace prints relative paths for these writes and truncates argv, and I did not trace `chdir`.
  The attribution to the `--work` clone rests on the writer's argv (`git -C …/R… checkout -q --detach 7b2373…`, the only
  checkout in the leg, line 172), on the lane's HEAD (`aac82684…` at the time of the run, `status --porcelain` empty,
  `reflog` 2 lines — unchanged) and on the lane index (below).
- Lane `.git/index.lock`: 12× create + unlink in this run; `rename` 0; index mtime 00:07:42 and sha `c2dc9db4…` unchanged (no rewrite in this run).
- `/dev/tty`: 1485 `openat("/dev/tty", O_RDWR|O_NONBLOCK) = -1 ENXIO` (git children; no file written).
- No socket. `execve` lines (unfinished+resumed counted separately): 52 703 `/usr/bin/git`, 9 350 `/usr/bin/timeout`, 2 563 python3, plus shell helpers
  (`bash tools/research-gate.sh verify-sweeps … --root ..` runs from the regression leg, `rerun-controls-r95.py` line 132).
- `--work` after exit: `w-full` is empty (`find` shows only the directory).
Receipts: `R98SentinelC1-c1-full-stdout.txt`, `R98SentinelC1-strace-c1-full-summary.txt`, `R98SentinelC1-index-and-tool-versions.txt`.

### F6 — C2 instrument docstring says "from committed lane bytes only"; it reads the working tree (wording false; C2 numbers held at F)
`entry-controls-r98.py` docstring: "Recomputes, from committed lane bytes only (no network, no lane write)". The code reads
`caps`, `text` and `prior` with `open(os.path.join(root, …))` (lines 140–142), i.e. working-tree bytes; only the BASE
reads use `git show`. At F the tree is clean so the counts hold. Demonstration on a second clone (`$S/repo2`) with an
uncommitted K1 wording edit (HEAD K1 row unchanged, `git show HEAD:…` line 52 `Are the search concepts clear?`):

    python3 -B $S/repo2/corpus/evidence/round98/entry-controls-r98.py --root $S/repo2
    CASE positive held=35/36 bad_quotes=['K1'] … FAIL
    ENTRY_CONTROLS_R98=FAIL          (exit 1)

Receipt: `R98SentinelC1-entry-controls-working-tree-demo.txt`. Predicate at F (unchanged tree): `POSITIVE=1/1 DO_NOTHING_REFUSED=1/1 NEW_ONLY=1/1 FORGERY_REFUSED=7/7 QUESTION_LINES_HELD=36/36 BASE_HELD=16/36 ELEMENTS=7+6/7+6 WARRANTS_OK=10/10 LANE_FILLED=10/10`, `ENTRY_CONTROLS_R98=PASS` (rc 0).

### F7 — C1 battery scores the working copy of the tool, not the committed F bytes, and does not refuse a dirty tree (not in the claim's named limits)
`selftest-controls-r98.py` line 179 `tool = os.path.join(root, TOOL)` and line 210 `src = open(tool, …)`; `lane_state` only compares
status before and after. Demonstration on `$S/repo2` (uncommitted edit to the tool's print format; `$S/repo2/tools/search-rerun.py` line 666):

    python3 -B $S/repo/corpus/evidence/round98/selftest-controls-r98.py --root $S/repo2 --work $S/w-dirty --no-regression → rc 1
    POSITIVE=0/1 KILL_REQUIRED=0/35 … EXTERNAL_R97_KILLED=36/37 … SELFTEST_CONTROLS_R98=FAIL

The battery fails the dirty tool here (it is not a pass-through), but it scores whatever bytes are on disk; a dirty
lane gives a verdict about uncommitted content. At F this is not observable (clean tree). Receipt: `R98SentinelC1-battery-dirty-tool-demo.txt`, `R98SentinelC1-battery-dirty-tool-stdout.txt`.

### F8 — observation outside the claims: a tracked absolute symlink into a sibling lane's scratch
`git ls-files -s` at F: `120000 46812490… .ufo/waves/round-84/w1/R84ExecForge/forge/linkcap.txt`; its blob content is
`/fast/scratch/hyaku/chousa-r84/R84ExecForge/tree/corpus/captures/f2489455cc311a4de981e926.txt`. Every checkout recreates a
dangling symlink on any host without that scratch tree (the regression leg recreates it 55 times inside `--work`). Hygiene
only; no claim depends on it.

## Verdict-relevant checks I ran (exact commands, observed lines, exit codes)

1. `strace -f -qq -e trace=file,network,process -o $S/strace-selftest.txt python3 -B $S/repo/tools/search-rerun.py --selftest` → rc 0; last line `SEARCH_RERUN_SELFTEST: PASS cases=67/67`; 0 socket/connect; 2 git execs; 2 `/dev/null O_RDWR`; 0 mutating fs calls.
2. `env [GITFOO=…|-u GITFOO|GIT_DIR=…] python3 -B $S/envleak.py $S/repo/tools/search-rerun.py` (and `envleak2.py`) → rc 0 each; `env_diff_after_selftest {}`.
3. `strace … selftest-controls-r98.py --root $S/repo --work $S/w-c1nr --no-regression` → rc 0; `SELFTEST_CONTROLS_R98=PASS`; index sha unchanged, mtime rewritten once.
4. `strace … selftest-controls-r98.py --root $S/repo --work $S/w-full` (full) → rc 0; predicate line as claimed; index unchanged.
5. `strace … entry-controls-r98.py --root $S/repo` → rc 0; `ENTRY_CONTROLS_R98=PASS`; 0 socket; 0 mutating fs; `git show` ×2 only.
6. Outside-write mutant through the NO_WRITE leg → rc 0, `SELFTEST_CONTROLS_R98=PASS` (F1).
7. Working-tree entry edit → rc 1, `ENTRY_CONTROLS_R98=FAIL` (F6); working-tree tool edit → rc 1, `SELFTEST_CONTROLS_R98=FAIL` (F7).

No network was used; no egress; `corpus/captures` and `refetch.tsv` untouched; lane not mutated.

## Named limit (e), exact form proposed

"The self-test reads `/dev/null` (r30) and runs `git -C /dev/null` twice (r29, r34); each git child opens `/dev/null`
O_RDWR, reads the host's global git config and is resolved through `PATH`; no write to any file and no socket was
observed by strace at F. The battery's NO_WRITE leg observes only an empty `HOME`/`TMPDIR`/cwd and the lane's
status/diff; it does not observe writes elsewhere."

## Not done (scope)

No verdict on the C1 mutant kill numbers beyond their predicate (other seats), no review of the entry's quotes against
captures (other seats). The sandbox run is single-host, single-run.

VERDICT: R98SentinelC1 C1 fired — limit (e) says "no write" is observed by the NO_WRITE leg, which passes a self-test writing outside --work (rc 0, SELFTEST_CONTROLS_R98=PASS on the outside-write mutant, F1); the predicate line and the self-test's own I/O at F held (67/67, 35/35, no write, no socket).
VERDICT: R98SentinelC1 C2 held — at F ENTRY_CONTROLS_R98=PASS (rc 0), the entry-controls run made no write, no socket, no index change; its docstring's "committed lane bytes only" is false (F6: it reads the working tree), but no claim sentence or number is contradicted at F.
