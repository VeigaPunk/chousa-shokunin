# ExecProbeStability — round 62 w1 — probe stability and C2 verdict stability

Probe = corpus/evidence/round62/controls/candidate-openat2-probe.py; expected = candidate-openat2-probe.txt
(18 lines: KERNEL, PYTHON, HEADER, P01–P14, PROBE_FACTS). "Identical" = whole stdout byte-equal to the .txt
(a superset of the PROBE/HEADER lines). Driver and scratch were in /fast/scratch/hyaku/chousa-r62/ExecProbeStability
(removed). Every run used `python3 -B`, a fresh `--work` (`w-<8 hex>`), and left no work dir behind. No labrat used.

## Findings
1. **10/10 identical.** Ten runs rotated through cwd {lane root, `/`, scratch}, umask {077, 022}, `nice -n 19`,
   TMPDIR=scratch, `--work` on /fast (xfs) for 7 runs and on /dev/shm (tmpfs; no sudo needed) for 3. Each was rc=0, stdout
   equal to the .txt, work dir removed.
2. **Extra matrix, 27/27 identical** (rc=0; 15 cwd×umask + 12 work-parent runs; the 5 umask-277 runs excluded, see 4): cwd {lane, `/`, scratch, empty subdir, /proc} × umask {077, 022, 000};
   `--work` parent {/dev/shm, /tmp, /var/tmp, scratch} × 3 with nice and TMPDIR. (/tmp and /var/tmp are root-owned 1777,
   so those cover the "sticky world-writable parent" case under my own uid.)
3. **Non-owner: no difference.** As uid `nobody` (`sudo -n -u nobody`, probe copied to a 755 dir because /home/vgpnk is
   0700; copy deleted) with `--work` under /tmp, /dev/shm and /var/tmp, 2 runs each: 6/6 rc=0, identical. As root: identical.
4. **One real instability, outside the asked matrix: a umask that strips the owner's w or x bit.** `umask 277` and
   `umask 177` give rc=1 and no stdout; traceback is `PermissionError` at `(root / "real").mkdir(parents=True)` (line 73),
   because `Path.mkdir` creates the parent `root` with mode 0777&~umask, which is not owner-writable/searchable.
   umask 277 failed on all 5 cwds tried; 177 was run once (scratch cwd). The other 15 cwd×umask grid combos
   (umask 077/022/000) passed. The failure is loud (non-zero rc, empty stdout, no `PROBE_FACTS` line); it is not a silent
   wrong-PASS. In C2, such a run would read as `PROBE=0/1`. [INFERENCE: not run through the counter under umask 277.]
   Any harness that sets umask 177/277 around the counter would turn PROBE to FAIL; the normal 022/077/000 are safe.
5. Nothing in the output varies with cwd, nice, TMPDIR, filesystem type or uid; KERNEL/PYTHON/HEADER lines are host-bound
   (named limit in claims.md: one kernel, x86_64 only).

## C2 verdict stability
Mirror prepared as `controls/run-c2v2-controls.py` does for the `positive` variant (corpus copy minus
captures/evidence/fixtures, README + map line, probe .py/.txt into mirror evidence/round62, positive rows into
SOURCES.md, positive entry), a fresh mirror each time, run with `python3 -B corpus/evidence/round62/c2v2-count.py --root <mirror>`
(cwd varied: lane, `/`, scratch, lane, `/`; TMPDIR=scratch). All 5 runs: rc=0, byte-identical stdout (1 distinct sha256):
`ENTRY=1/1 TRIO=1/1 ROWS=3/3 QUOTES=9/9 COVERAGE=1/1 CLAIMS=1/1 ECHO=1/1 LIMITS=1/1 PROBE=1/1 MAP=1/1 CENSUS=1/1 C2=PASS`
Context runs: the real `run-c2v2-controls.py --work <scratch>` once → `C2V2_CONTROLS_UNEXPECTED=0`, rc=0 (non-sequitur
PASS as recorded). The counter on the unmodified lane root (entry not landed) prints the frozen before line
`ENTRY=0/1 ... CENSUS=1/1 C2=FAIL` as expected.

## Limits
Only one host/kernel/fs; the probe was not run under a different kernel or a read-only /tmp; no concurrent-load
stress beyond nice 19; sticky-dir case covered with my uid, nobody and root but not a foreign-owned `--work` parent
with restrictive mode.

VERDICT: PROBE_RUNS_IDENTICAL=10/10 c2_verdict_stable=yes
