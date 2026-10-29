# ExecProbeEnv — probe stability under hostile environments (round 63, w1)

Probe: `corpus/evidence/round63/controls/candidate-git-revision-probe.py` (not edited). Reference:
`controls/candidate-git-revision-probe.txt`. git `git version 2.56.0`, python 3.14.8, lane HEAD `c8bfcc65cb32…` when read.
Scratch `/fast/scratch/hyaku/chousa-r63/ExecProbeEnv/` (removed before yield). Driver `run.sh`: `cd` scratch,
`env TMPDIR=<scratch> <assignments> python3 -B <probe> --work <scratch>/p`, stdout diffed to the committed `.txt`
(`diff <(stdout) reference`), exit code and stderr size recorded.

## Findings

1. **No run differs.** 15 of 15 runs: stdout byte-identical to the committed `.txt` (empty diff), exit 0, stderr 0 bytes,
   `PROBE_FACTS=14/14`. No cause to report because no PROBE line differed.
2. Runs and results (all `IDENTICAL exit=0 err=0`):
   - `plain01`..`plain10`: ten clean-environment runs.
   - `home`: `HOME=<scratch>/home` holding `.gitconfig` with `core.abbrev=12`, `init.defaultBranch=other`, `user.name=x`.
   - `gitdir`: the same HOME plus `GIT_DIR=<lane>/.git` and `GIT_WORK_TREE=<lane>`.
   - `cfgcount`: `GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=core.abbrev GIT_CONFIG_VALUE_0=12`.
   - `lang`: `LANG=de_DE.UTF-8`. **The locale does not exist here** (`locale -a | grep -i de_` printed nothing), so this
     ran under a fallback and is not a German-locale test. A second leg `all` added `LC_ALL=de_DE.UTF-8` the same way, with
     HOME, GIT_DIR, GIT_WORK_TREE and GIT_CONFIG_* set together: identical. The probe pins `LC_ALL=C` for its fixture git
     calls anyway (`BASE_ENV`, line 30), so a missing locale would not have changed it (INFERENCE: not shown with a real de locale).
3. **Why the environment cannot reach the output** (read from the source, lines 26-43): `git()` deletes every `GIT_*`
   variable from the inherited environment, then applies `BASE_ENV` (`GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_SYSTEM=/dev/null`,
   `GIT_CONFIG_NOSYSTEM=1`, fixed identity and dates, `LC_ALL=C`). That covers GIT_DIR, GIT_WORK_TREE, GIT_CONFIG_COUNT/KEY/VALUE
   and the HOME `.gitconfig` (XDG config is also bypassed by `GIT_CONFIG_GLOBAL`).
4. **Lane untouched, by trace.** `strace -f -e trace=%file` of the `all`-style environment (HOME + GIT_DIR/GIT_WORK_TREE
   + GIT_CONFIG_*), 5116 `execve` lines: 76 lines mention the lane path, all of them the probe script's own path walked by
   Python (readlink/stat/openat on `.../round63/controls[/candidate-git-revision-probe.py]`); zero mention `<lane>/.git`;
   none of the lane-path lines is a write/create/unlink/rename/mkdir (grep for `O_WRONLY|O_RDWR|O_CREAT|unlink|rename|mkdir|\.git` empty).
5. **One environment leak, harmless to the output.** The header call `subprocess.run(["git","--version"])` (line 79) uses
   the raw inherited environment, not `git()`/`BASE_ENV`. The trace shows that process (pid 1432199) opened the fake
   `<scratch>/home/.gitconfig`. `git --version` prints only the version, so `HEADER git=` is unaffected in every run above;
   but a user `.gitconfig`/`GIT_*` is not isolated for that one call. Cosmetic isolation gap, not an output risk found here
   (INFERENCE: a wrapper `git` earlier on PATH that appends text to `--version` would alter the header; not tried).
6. **Lane `git status` before/after.** `git -C <lane> status --porcelain=v2 --branch --untracked-files=all` before (57 lines)
   and after differ in exactly: `.ufo/waves/round-63/w1.ready.partial` → `w1.ready.dispatched`, and a new untracked
   `.ufo/waves/round-63/w1/MutPre12.md`. Both are sibling-seat/L1 writes under `.ufo/waves/round-63/` (another seat's report
   and the dispatch marker), not the probe: item 4's trace shows no lane write by the probe. I did not write under the lane
   except this report, so the delta attributable to this seat is nil apart from `w1/ExecProbeEnv.md`. Tracked-file lines
   (`1 .M` / `1 M.` records) did not change. `.git/index` ctime moved during the session (23:31:05) — consistent with sibling
   `git status` refreshes (INFERENCE; the strace shows my probe never opened it).

## Not done / limits
- No real `de_DE` locale (not installed; no locale generation attempted — it would be a host mutation).
- Ten identical runs bound flakiness at 0/10 on this host for plain runs; the 4-digit collision search (P09) is
  content-deterministic (`filler N` text), so no run-to-run variance is expected.
- No tools installed or updated. No git mutation in the lane (read-only `git status`); no fixture repo outside the probe's own.

VERDICT: PROBE_RUNS_IDENTICAL=15/15 env_leaks=git-version-header-call-reads-unisolated-HOME-gitconfig(harmless,output-unchanged)
