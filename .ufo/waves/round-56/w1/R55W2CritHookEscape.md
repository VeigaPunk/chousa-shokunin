# R55W2CritHookEscape — counter hook escape attempt

Axes: operability (R55 C1 hook boundary), depth (whether a capability escape yields an expected offset/seed or a leg pass); calibration unchanged.

## Evidence

Inspected `corpus/evidence/round55/c1-count.py:81-108`: the hook checks events `open`, `os.listdir`, `os.scandir`, and denies a fixed spawn/exec/socket/ctypes list. `allowed()` treats integer paths as allowed (`:91-100`), and does not inspect `dir_fd` arguments. It does not match `os.chdir`, `os.symlink`, or `os.kill`.

Inspected counter `Ctx.build` (`:188-196`): builder is a child process, receives its generated run's `TMPDIR`, `R55_ALLOW`, tool path and CLI arguments. The per-run directory is the subprocess cwd and contains `quotes.tsv` and `cache`. Counter derives expected forms/offsets before the build (`:299-315`); judge checks exact forms and offset afterward (`:238-279`). Seed is printed by counter (`:443-453`), and supplied seed is also a counter argv value.

Attempted the counter against the archived round-55 revision and actual landed builder:

```text
python3 "$S/corpus/evidence/round55/c1-count.py" --seed 7 --per-leg 2 --tool /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/build-spans.py --work "$S/work"
tool=/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/build-spans.py sha256=1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6 seed=7 per-leg=2
GENOLE=PASS 2 docs, 4 quotes
OLEPIN=PASS 4 captures, 8 quotes
REFUSE=PASS 4 cases
ENV_CHANGED git show corpus/evidence/round54/quotes.tsv
```

This was an environment/checkout mismatch at REGRESS, not a hook exploit or complete C1 measurement. A custom probe run was attempted, but the counter requires `--work` empty; the work directory was nonempty, so it exited `usage: --work must be empty` before launching a builder. Thus no probe result establishes access to `/proc/<ppid>/mem`, `/proc/<ppid>/environ`, counter argv, campaign cache, or lane corpus. No passing-leg exploit was observed.

## Assessment

The audit-hook boundary defect is supported by source: unchecked `os.chdir` can change the base used by `realpath`; unchecked `os.symlink` and `os.kill` expose additional unpoliced operations; `allowed(int)` accepts descriptor arguments. This alone does not prove a useful escape: ordinary `os.open` with `dir_fd` still checks its relative path against the current cwd, and an outside dirfd must first be acquired. The proposed deep-cwd/dirfd technique needs an executed probe before it can be called exploitable. `/proc` and campaign-cache reachability are likewise unproven. The seeded argv disclosure is plausible from the process interface but has not been observed from a builder in this attempt.

Smallest safe correction for the frozen claim's adjudication: classify this as an incomplete hook capability boundary, not as a demonstrated offset/seed leg-pass exploit; test dirfd-relative access, process metadata, and kill/symlink behavior in an empty-work scratch run. Do not change the frozen predicate or counter.

VERDICT: Round-55 hook boundary defect survives source inspection; no leg-pass exploit demonstrated, and proc/cache/dirfd access remains unverified.