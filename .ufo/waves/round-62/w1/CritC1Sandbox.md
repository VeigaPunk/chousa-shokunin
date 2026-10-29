# CritC1Sandbox — sandbox attack on c1v2-count.py (`unshare -Ufp --kill-child --mount-proc`)

Scope: attack the sandbox only. Counter, battery, controls and claims were read, not edited. Scratch
`/fast/scratch/hyaku/chousa-r62/CritC1Sandbox/` removed. No git mutation. No pacman, no installs.

## Findings

1. **The sandbox is a PID/proc namespace, not a filesystem sandbox.** The docstring's "the builder cannot see the
   counter" is false for files. Inside the namespace the builder sees the whole host filesystem with the caller's
   own permissions (kuid 1000 is kept; only the displayed uid becomes 65534).
   - `unshare -Ufp --kill-child --mount-proc /usr/bin/python3 -B probe.py` printed
     `uid_map:` (empty), `getuid 65534`, `proc pids visible: [1]`, then
     `READ lane counter OK bytes 32661`, `READ lane claims.md OK`, `READ host RULES.md OK`,
     `READ home dir OK dir entries 140`; `READ etc shadow FAIL [Errno 13]`.
   - Writes succeed: `WRITE OK` to the fixture scratch, to the lane `.ufo/...` path and to `/tmp`
     (files removed by the probe).
   - **Frozen counter and its source are writable from the builder:**
     `OPEN_WRONLY lane counter: OK (no bytes written)`; `ACCESS_W lane capture-text True`. I did not write
     to them. The open probe was a no-op open-for-append.

2. **Cross-run contamination is real (scratch copy, not the frozen file).** A scratch copy of the counter, with
   `CAPTURE_TEXT` pointed at a scratch copy of `capture-text.py`, was run three times:
   - A: a poisoner builder appends `raise SystemExit(1)` to that source → `LEGS=1/20 C1V2=FAIL`, rc=1.
   - B: landed builder afterwards → `LEGS=19/20 C1V2=FAIL`, **rc=1** (correct builder rejected).
   - C: pristine copy restored → `LEGS=20/20 C1V2=PASS`, rc=0.
   The lane's `c1v2-count.py` sha prefix stayed `b7016fba91b03460` (the frozen value).

3. **The sandbox load-bearing claim holds only when unshare really isolates.** Under a no-isolation
   pass-through `unshare` (shim: strips the flags, execs the rest; exits 0), the counter's pre-check
   (`unshare … true` rc 0) passes and the full counter reads `LEGS=20/20 C1V2=PASS`. Battery subset
   (`c1v2-battery.py --only F06 F10 F11 F12`):

   | subject | real unshare (`bat-base`) | pass-through shim (`bat-shim`) |
   |---|---|---|
   | F06 parent cmdline | exit 1, ok (LEGS 11/20) | **exit 0, MISS** (LEGS 20/20) |
   | F10 any process cmdline | exit 1, ok (LEGS 11/20) | **exit 0, MISS** (LEGS 20/20) |
   | F11 stdout is a file | exit 1, ok | exit 1, ok |
   | F12 detached cleaner | exit 1, ok (LEGS 19/20) | **exit 0, MISS** (LEGS 20/20) |

   Mechanism, confirmed: in the real sandbox `getppid()` is 0 and `/proc` lists only pid 1, so F06 and F10
   never fire. Their rejection comes from the base builder failing legs, not from detection. F12's helper is
   killed when PID 1 exits (`ORPHAN marker after 2s (sandboxed): ABSENT`; unsandboxed: present). Without the
   namespace the parent's cmdline names `c1v2-count.py`, matching F06/F10 detection, so the forgers are accepted.
   Consequence: 2 of the 12 forger rejections are not detection-based in the real sandbox, and the sandbox is
   the only thing standing between those forgers and an accept.

4. **Root (euid 0) gives a false reject, not exit 2.** `leg_h17` raises `SystemExit` when `geteuid()==0`.
   That is not caught and the counter exits 1 for every builder. Observed: `sudo -n` requires a password (not
   run); `unshare -r env … c1v2-count.py --work …` → `c1v2-count: H17 needs a non-root user (mode 000 is readable
   by root)`, rc=1, landed builder included. Docker default containers run as root, so this is the same path
   there (INFERENCE, no python in the images).

5. **Fail-closed (exit 2) cases, run:**
   - PATH without unshare (`env -i PATH=<empty dir> /usr/bin/python3 -B c1v2-count.py --work …`) →
     `c1v2-count: sandbox unavailable ([Errno 2] No such file or directory: 'unshare')`, rc=2.
   - `unshare` stub exits 1 → `sandbox unavailable (unshare exit 1); fail closed`, rc=2.
   - Docker `debian:bookworm`, default seccomp: `unshare -Ufp … true` → `unshare failed: Operation not
     permitted`, pre-check rc=1 → counter exit 2 (INFERENCE from the same pre-check path; the counter itself
     cannot run in these images because no image has python3).
   - Docker `--security-opt seccomp=unconfined`: `unshare: mount /proc failed: Operation not permitted`,
     pre-check rc=1 → exit 2. Plain `unshare -U` works here (rc 0), so only `--mount-proc` fails.
   - `alpine:3.20` (busybox unshare): `unshare: unrecognized option: kill-child`, rc=1 → exit 2 (INFERENCE from
     the same path).
   - `max_user_namespaces=0` or `unprivileged_userns_clone=0`: not testable without root; INFERENCE: `unshare -U`
     fails with EPERM → exit 2.

6. **/proc nosuid.** Host `/proc` is `rw,nosuid,nodev,noexec`. The fresh `--mount-proc` mount inside the
   namespace shows the same flags and the `--mount-proc` pre-check passes. So nosuid does not change the verdict
   here. Where `--mount-proc` cannot mount (finding 5), the counter fails closed.

7. **uid mapping (H17, H18).** The namespace has no uid map: `getuid` displays 65534, `CapEff` is 0, the kernel
   still uses kuid 1000. A mode-000 file is `READ FAIL [Errno 13]` both inside and outside the namespace
   (`m0probe`). Baseline `base-counter.txt` shows `LEG H17 UNREADABLE pass` and `LEG H18 FIFO pass` in both
   profiles. So the uid mapping does not change H17 or H18 on this host.

8. **Minor, INFERENCE from code.** The neutral profile shuffles `PATH` (line ~281) and Popen resolves `unshare`
   via the child env, while the pre-check uses the parent `PATH`. With two `unshare` binaries on `PATH` the
   pre-check and the legs could use different binaries. Not tested.

## Commands and result lines (exit codes)

- Baseline full counter (real sandbox): `LEGS=20/20 C1V2=PASS`, rc=0 (`base-counter.txt`).
- Shim battery: `LANDED=0/0 POSITIVES=0/0 FORGERS_REJECTED=1/4 STUBS_REJECTED=0/0 BATTERY=FAIL`, rc=1 (subset run).
- Not run by me: the full battery and the full `c1v2-count.py` at three seeds. Those belong to the other seats.
- Network: not tested. The namespace does not unshare the network (`-n` is absent), so inference is that the
  builder has network access. Untested.

## Verdict inputs

- Wrong verdicts: pass-through unshare → F06, F10, F12 exit 0 (3). euid 0 → landed builder exit 1 (1). Poisoned
  shared source → landed builder exit 1 (1). Total k=5.
- Fail-closed: pre-check failures (no unshare, unshare exit 1, docker default seccomp, `--mount-proc` failure,
  busybox option) exit 2. But present-and-not-isolating unshare (finding 3) and euid 0 (finding 4) do not. So the
  counter is not fail-closed as a whole.

Recommended limit for the counter owner (not a rewrite of the frozen counter; for L1 routing): assert
isolation, e.g. a pre-check that the child sees only pid 1 and `getppid()==0`, and that a sibling file the
parent wrote is unreadable; treat `geteuid()==0` as a refusal with exit 2, not an exit 1 verdict; and run the
builder against a read-only copy of the lane tools and a separate scratch mount.

VERDICT: SANDBOX_WRONG_VERDICTS=5 fail_closed=no
