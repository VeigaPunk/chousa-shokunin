# ExecNoSandbox (ExecNoSandbox-2) — v2 counter without a real sandbox

Counter `corpus/evidence/round62/c1v2-count.py` (unmodified, sha256 prefix per claims; BUILDER line shows
landing builder sha c366492005ce304a). Seed `C1V2_SEED=7`, `TMPDIR`/`--work` under
`/fast/scratch/hyaku/chousa-r62/ExecNoSandbox-2/`. Fakes are scripts in scratch dirs put first on `PATH`
(a dir holding only a `python3` symlink for the "absent" case). Nothing under PATH hosts or the lane was written.

## Findings

1. **Absent `unshare`** → fail closed. exit 2, `c1v2-count: sandbox unavailable ([Errno 2] No such file or directory: 'unshare')`
   (landing builder and an `exit 0` stub: identical).
2. **`unshare` = `exit 1`** → fail closed. exit 2, `sandbox unavailable (unshare exit 1); fail closed`.
3. **Fake sandbox = `exit 0` without running its argument** (a) the preflight `unshare -Ufp --kill-child --mount-proc true`
   does NOT catch it (exit 0 == "fine"); (b) the counter runs all 40 leg-runs with nothing executing, and returns a
   *verdict*, not a usage error: landing builder `LEGS=1/20 C1V2=FAIL` exit 1 (only P03 NOPYC "passes": an unchanged tools/ listing is
   true when nothing ran); `exit 0` stub: same `LEGS=1/20 C1V2=FAIL` exit 1. P04 even logs
   `counter exception FileNotFoundError ... spans`. **Defect:** a missing/broken sandbox is reported as "builder fails C1" (exit 1),
   indistinguishable from a real FAIL; the honest builder is judged failing. Battery on this counter+fake: `LANDED=0/3
   POSITIVES=0/4 FORGERS_REJECTED=12/12 STUBS_REJECTED=4/4 BATTERY=FAIL` exit 1 — i.e. the 12/12 comes from rejecting
   everything (a do-nothing counter), the battery does flag it (LANDED 0/3) but only as a failure of the
   landed builder, not as "sandbox missing".
4. **Fake that exits 0 *and* execs its argument with no namespace** (pass-through; `unshare` shifts its flags then
   `exec "$@"`; needed `/usr/bin` after it in PATH because the preflight arg `true` is resolved through PATH):
   counter on landing builder → `LEGS=20/20 C1V2=PASS` exit 0 (counter says PASS with no PID/user namespace at all);
   on the `exit 0` stub `LEGS=1/20 C1V2=FAIL` exit 1. Battery, fake first on PATH, real counter name:
   `LANDED=3/3 POSITIVES=4/4 FORGERS_REJECTED=12/12 STUBS_REJECTED=4/4 BATTERY=PASS` exit 0; renamed copy of the counter
   (`renamed-k.py`): same line, `BATTERY=PASS` exit 0. So the sandbox is neither verified at run time nor required by the
   battery's 12 forgers in this configuration. **Discrepancy, unexplained:** `controls/c1v2-controls.txt` X02 (`SANDBOX = []`)
   reads `forgers_accepted=F06,F10,F12`; my pass-through fake rejected all 12. INFERENCE only: the control's mutant runs
   differently (different cmdline / process tree). I did not run X02 and make no claim about it.
5. `unshare` is resolved via `PATH` by the counter (`SANDBOX[0]="unshare"`); an earlier PATH entry silently replaces
   it (cases 3–4 prove it). Python's `Popen` also searches the *child* env's PATH, which the neutral profile shuffles.

**Answer to the item:** a fake sandbox gets a verdict (exit 1 for `exit 0` fake, exit 0 for pass-through fake on the
landing builder). Preflight `... true` catches only non-zero fakes. Defect confirmed.

## Smallest fix (prototype tested in scratch copy; frozen counter not edited)

Two edits in `c1v2-count.py`: resolve `/usr/bin/unshare` absolutely, and replace the `... true` preflight with a probe
that runs a Python program inside the sandbox and checks its own output (pid 1 in a one-entry `/proc`, nonce echo).

```diff
-SANDBOX = ["unshare", "-Ufp", "--kill-child", "--mount-proc"]
+SANDBOX = ["/usr/bin/unshare", "-Ufp", "--kill-child", "--mount-proc"]  # absolute: no PATH lookup
+PROBE = ("import os,sys;n=open('/proc/self/status').read().split('NSpid:')[1].split(chr(10))[0].split()[-1];"
+         "print('C1V2PROBE',sys.argv[1],os.getpid(),n,sorted(int(x) for x in os.listdir('/proc') if x.isdigit()))")
@@ main()
+    nonce = secrets.token_hex(8)
     try:
-        pre = subprocess.run(SANDBOX + ["true"], stdin=subprocess.DEVNULL, capture_output=True, timeout=30)
+        pre = subprocess.run(SANDBOX + [sys.executable, "-c", PROBE, nonce], stdin=subprocess.DEVNULL,
+                             capture_output=True, timeout=30)
 ...
-    if pre.returncode != 0:
-        print(f"c1v2-count: sandbox unavailable (unshare exit {pre.returncode}); fail closed", file=sys.stderr)
+    want = f"C1V2PROBE {nonce} 1 1 [1]\n".encode()
+    if pre.returncode != 0 or pre.stdout != want:
+        print(f"c1v2-count: sandbox unavailable (unshare exit {pre.returncode}, probe output {pre.stdout[:80]!r}); fail closed", file=sys.stderr)
         return 2
```
Tested on scratch copy `.../ExecNoSandbox-2/lane/corpus/evidence/round62/c1v2-count.py` (seed 7):
- real sandbox: `LEGS=20/20 C1V2=PASS` exit 0 (same result as the frozen counter);
- `PATH=zero-fake:` first: ignored by the absolute path, `LEGS=20/20 C1V2=PASS` exit 0;
- fake exit-0 at the absolute path: `sandbox unavailable (unshare exit 0, probe output b''); fail closed` exit 2;
- pass-through fake at the absolute path: `... probe output b'C1V2PROBE 8afb... 1145937 1145937 [1, 2, 3, ...'); fail closed` exit 2;
- exit-1 fake: `sandbox unavailable (unshare exit 1, probe output b''); fail closed` exit 2.
Residual: a fake that forges the probe line (knows the nonce) is out of scope; a file at `/usr/bin/unshare` is trusted.
Cost: ~1 extra process at start. The fix must land in a later round (frozen bytes); route as a counter limit.
The battery also never feeds a missing/fake sandbox to the counter, so 'exit 2 on fake sandbox' is untested by it.

## Cleanup / environment
No tool installed. Scratch `/fast/scratch/hyaku/chousa-r62/ExecNoSandbox-2/` deleted at yield. No git/jj mutation.

VERDICT: FAKE_SANDBOX_GIVES_VERDICT=yes fail_closed=no
