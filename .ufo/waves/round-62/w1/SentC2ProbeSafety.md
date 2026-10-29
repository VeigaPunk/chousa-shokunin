# SentC2ProbeSafety — safety review of `controls/candidate-openat2-probe.py` (round 62, w1)

Scope: review only. The probe was not edited. Writes: this report and scratch
`/fast/scratch/hyaku/chousa-r62/SentC2ProbeSafety/` (deleted at end). No installs, no git, no network.
Host: `uname -m` = x86_64; kernel 7.2.11-arch1-1; Python 3.14.8; `/usr/include/linux/openat2.h` and
`/usr/include/asm/unistd_64.h` present (`__NR_openat2 437`, `RESOLVE_*` as in the committed output).

Method: 17 cases run by a scratch driver (`python3 -B driver.py`), each with a before/after snapshot of
the whole scratch tree (lstat, symlinks not followed). Fault injection used a harness that execs the
unmodified probe: a BPF seccomp filter via `prctl(PR_SET_SECCOMP)` for syscall 437 (ERRNO=ENOSYS,
ERRNO=EPERM, TRAP->SIGSYS), `platform.machine` patched to aarch64, `HDR` pointed at a missing path,
`os.open` raising after fixture files exist, `os.unlink`/`os.rmdir` raising PermissionError.

## Findings (safety) — three defects

**S1. Deletes a directory that is not the named path (symlink resolved, then removed).**
Line 47 `work = Path(a.work).resolve()`; line 142 `shutil.rmtree(work)`. A `--work` that is a symlink
to an empty directory deletes the target.
- Case C, `--work S/wl` with `wl -> empty_t`: rc=0, `removed: ['empty_t']`, `wl` left dangling.
- Case D, the same with a non-empty target: rc=2 `--work must be absent or empty`, nothing removed.
Severity low: needs the caller to pass a link to an empty directory. The docstring says "DIR absent or
empty; removed afterwards" and does not say that symlinks are resolved first.

**S2. Creates ancestors of `--work` that cleanup never removes.**
Line 51 `work.mkdir(parents=True, exist_ok=True)` creates missing parents; line 142 removes only the leaf.
- Case H, `--work S/x1/x2/w`: rc=0, `added: ['x1', 'x1/x2']`, only `w` removed.
- Same residue in every run whose `--work` has a fresh parent: L (`enosys/`), M (`eperm/`),
  O (`inj/`, after an injected exception), R (`none/`), N (`sigsys/`, see below).
- Dangling symlink (case E, `--work S/wl3 -> S/dang_t`): `mkdir(parents=True)` creates the link target
  at its exact path and rmtree removes it, so one level leaves nothing. A longer dangling chain
  (`-> S/deep/a/b`) would leave `S/deep/a`. INFERENCE from the code path; not run.

**S3. Cleanup failure is silent and exits 0.**
Line 142 `shutil.rmtree(work, ignore_errors=True)`.
- Case P (`os.unlink` and `os.rmdir` raise PermissionError): rc=0, `added: ['cf', 'cf/w', 'cf/w/outside.txt',
  'cf/w/root', ..., 'cf/w/root/real/f.txt']`. The whole fixture is left, with no message and no non-zero exit.

## Not defects (checked)

- **No escape by the probe's own writes.** The probe creates only: `root/real/f.txt`, `root/f.txt`,
  `outside.txt`, and symlinks `linkdir -> real`, `flink -> f.txt`, `abslink -> <work>/outside.txt`,
  `absroot -> /f.txt`. Every opener uses O_RDONLY, O_PATH|O_NOFOLLOW, or a read with no O_CREAT, so the
  syscall never creates files. `absroot` is read only under RESOLVE_IN_ROOT (P10 `rootfile`). Case R
  (canary `outside_canary/keep` outside the work tree) and every other case: the canary and all
  non-work paths are unchanged in the diff.
- **Symlinked parent (the requested check).** Case B: `--work S/lp/w` with `lp -> S/real2`: rc=0,
  `PROBE_FACTS=14/14`, `real2/w` created and removed, `lp` still a symlink, no diff outside `real2/w`.
- **Symlink to non-empty dir** (case D), **existing non-empty dir** (F): rc=2, nothing removed.
- **`--work` is a regular file** (G): rc=1, `NotADirectoryError` from `iterdir` at line 48; file intact.
- **`/usr/include` missing** (J, `HDR` set to a missing path): rc=2 with the "needs Linux x86_64" message,
  nothing created. The check runs before `mkdir`.
- **Non-x86_64** (K, `platform.machine` = aarch64): rc=2 before `mkdir`.
- **Header lacks a constant** (`#define RESOLVE_NO_XDEV` only): rc=1, `AttributeError` at `const()`
  (`'NoneType' object has no attribute 'group'`), `bad/` left empty. Raised before `mkdir`, so no residue.
- **Cleanup on exception** (O, `os.open` raising after the fixture exists): rc=1, traceback,
  `inj/w` removed (the only residue is S2's parent `inj/`).
- **Baseline** (A, unmodified host): rc=0, `PROBE_FACTS=14/14`, and the KERNEL/PYTHON/HEADER lines match
  the committed `controls/candidate-openat2-probe.txt`. Only those lines were compared, not the full
  output; no diff run.
- **Documented, not counted:** an existing empty `--work` is accepted and removed (Q); `--work .` in an
  empty cwd removes the cwd (I). Both follow the docstring's "removed afterwards". L1 should know that the
  probe removes a directory that already existed.
- **Not tested:** TOCTOU between the emptiness check (line 48) and `mkdir` (line 51). INFERENCE only.

## Seccomp / non-safety observations

**ENOSYS exit (asked):** a blocked openat2 returns ENOSYS. The probe does not special-case it. Case L
(ENOSYS on 437): **rc=1**, `PROBE_FACTS=4/14`, output lines `observed=ENOSYS expected=ELOOP DIFFERENT`
(P04), `observed=None expected=rootfile DIFFERENT` (P10), and so on. Only P01, P02, P03 and P11 (no
openat2 call) pass. EPERM (case M) also gives rc=1 with the same shape. So `exit_on_enosys=1`.

Operability defect (not counted in k): a blocked syscall looks like a kernel-behaviour mismatch. No
distinct exit code or "openat2 unavailable" line, so a seccomp-restricted host cannot be told apart from
a kernel that disagrees with the page. Suggested for L1 or the author, not applied: map ENOSYS/EPERM on
the first openat2 call to a separate exit code and message.

**SIGSYS kill** (case N, TRAP): rc=-31, `sigsys/w` left with its 10 files. The kernel kills the process,
so `finally` cannot run. This is the same class as SIGKILL: a limit, not a fixable code defect.

## Reproduction (scratch deleted)

Harness (`harness.py`) and driver (`driver.py`) were scratch files, removed at the end. The seccomp
filter is 7 classic BPF instructions: arch check, load nr, `nr == 437 -> RET ERRNO|val`, else ALLOW.
Each case: fresh `run/` fixture, `python3 -B <probe or harness> --work <path>`, snapshot diff.

VERDICT: PROBE_SAFETY_DEFECTS=3 exit_on_enosys=1
