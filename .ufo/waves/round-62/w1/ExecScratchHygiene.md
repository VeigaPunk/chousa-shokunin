# ExecScratchHygiene — round 62 w1 — scratch and /tmp hygiene (C1 counter, C1 battery, C2 probe)

Scratch: /fast/scratch/hyaku/chousa-r62/ExecScratchHygiene (TMPDIR=.../t). Tooling: strace and lsof were already installed (/usr/bin); nothing installed or upgraded.
Frozen files untouched; counter sha256 prefix b7016fba91b03460 (matches claims.md); battery prefix 9afe00b917fb95e2.

## Findings
1. Hardcoded temp paths: none. The requested grep over round62/*.py and controls/*.py hits only 4 lines:
   - c2v2-count.py:49 `import tempfile`
   - c2v2-count.py:219 `tmp = Path(a.work) if a.work else Path(tempfile.mkdtemp(prefix="c2v2-"))`
   - controls/pos-indep3.py:46 `import tempfile`
   - controls/pos-indep3.py:236 `tempfile.mkstemp(dir=path.parent, prefix=".bs-")` (builder atomic-write beside its target)
   No literal `/tmp`, `/var/tmp` or `/dev/shm` string is in any of the files. c1v2-count.py and c1v2-battery.py contain no mkdtemp/tempfile at all. hardcoded_tmp=0.
   - The one TMPDIR-dependent path is c2v2-count.py:219: with no `--work` it uses `tempfile.mkdtemp`, which resolves to `/tmp` when TMPDIR is unset. It is removed in the `finally` (line 232). With `--work` the probe's work dir is the caller's. The probe removes its own `--work` (probe line 142).
2. C1 counter, seed 62099 (strace -f, 10702 trace lines, 187 pids): `LEGS=20/20 C1V2=PASS`, exit 0. Second run, seed 62098 under `strace -f -y`: same verdict, exit 0.
3. Paths created outside --work (counter, seed 62098, 538 successful create/write/mkdir/link/rename calls, dirfd paths resolved with -y): the only non-work target is `/dev/null` (24 opens O_RDWR, an existing device, not a creation). PATHS_OUTSIDE_WORK = 0 created.
   - Mutating-call tally for the same run: builder atomic writes `.S###-n.txt.<hex>.tmp` (O_CREAT|O_EXCL|O_NOFOLLOW) and `mkdirat(..,"spans")` all resolve inside --work.
4. C1 battery (strace -f -y, 233869 trace lines, 12429 successful mutating calls, 5m37s): `LANDED=3/3 POSITIVES=4/4 FORGERS_REJECTED=12/12 STUBS_REJECTED=4/4 BATTERY=PASS`, exit 0. The only non-`--work` mutating target is `/dev/null` (573 opens). No `/tmp`, `/var/tmp` or `/dev/shm` create; no relative-path create outside work.
5. Work-dir removal: after the counter (both runs) and the battery, `ls` of the work dir reports "No such file or directory". The counter's `finally` (c1v2-count.py:720-728) chmods everything to 0700 (symlinks not followed) and `shutil.rmtree`s the work dir itself, so H17 mode-000 and H18 FIFO leftovers are gone (`find -type p` empty). TMPDIR (t) empty after counter, battery and probe.
6. Leftover processes: `pgrep -af ExecScratchHygiene` exits 1 (no match) after every run. The requested `pgrep -af 'build-spans|builder.py'` is NOT usable as a global check this wave: at start it listed ~50 processes, all sibling seats' (RevC1V2LegsH1/H3, CritC1Timing, MutC1V2Main, ...) under their own scratch dirs. The check is only meaningful when scoped to the seat's own path.
7. Host /tmp /var/tmp /dev/shm diff (`find -newer marker`, maxdepth 1): `/tmp/playwright_firefoxdev_profile-*` and 16 `/dev/shm/critc1timing-*` entries. Attributable to siblings (the `critc1timing-` prefix is seat CritC1Timing's; playwright is a browser). The strace shows none created by this seat. The diff is noisy with 60+ concurrent seats, so the strace is the evidence and the find diff is not.
8. Abnormal exit (extra probe, not requested): `timeout -s TERM 3` on the counter exits 124 and leaves its work dir (plain/, neutral/ with leg-* dirs) — there is no signal handler or atexit, only try/finally, so SIGTERM/SIGKILL skip cleanup. No process outlived it (`pgrep -af` on the work path: none, `unshare --kill-child`). Residue stayed inside --work and `rm -rf` removed it (no mode-000 dir needed chmod). Limit, not a defect against the claim: an interrupted run leaves its `--work`; seats must delete it.
9. Candidate probe (`controls/candidate-openat2-probe.py --work $N/pw`): exit 0, `PROBE_FACTS=14/14`, work dir removed afterwards, no tempfile use.

## Evidence pointers (command -> observed)
- `grep -n '/tmp\|mkdtemp\|tempfile' round62/*.py round62/controls/*.py` -> 4 lines above.
- `C1V2_SEED=62098 TMPDIR=$N/t strace -f -y -e trace=openat,mkdir,mkdirat,mknod,mknodat,symlink,symlinkat,link,linkat,rename,renameat,renameat2,creat -o trace-c1.txt python3 -B c1v2-count.py --builder tools/build-spans.py --work $N/w` -> LEGS=20/20 C1V2=PASS; non-work targets: `/dev/null` x24.
- same strace flags on `c1v2-battery.py --counter c1v2-count.py --work $N/bw` -> BATTERY=PASS; non-work targets: `/dev/null` x573.
- `ls $N/w`, `ls $N/bw`, `ls $N/pw` -> No such file or directory; `find $N/t $N/t2` -> only the dirs themselves.
- `pgrep -af ExecScratchHygiene` -> exit 1.

## Risks / notes
- Strace followed the unshare sandbox children (187 pids; builder `.tmp` writes visible), so the builders' writes are covered. Read-only opens outside work were not enumerated (not a creation).
- The seed was supplied via C1V2_SEED as instructed (62098/62099); fresh-random-seed behaviour not separately traced.
- Scratch is deleted before yield.

VERDICT: PATHS_OUTSIDE_WORK=0 residue=none hardcoded_tmp=0
