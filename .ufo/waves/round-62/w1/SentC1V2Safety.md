# SentC1V2Safety — hostile-builder safety under the v2 counter (round 62, w1)

Scope: `corpus/evidence/round62/c1v2-count.py` (sha256 prefix `b7016fba91b03460`, run only, never edited) and
the frozen battery's sandbox contract. Read-only on the lane except this report. No secret content was opened
(permission checks only, `os.access`/`lstat`/`listdir` on names); no socket was connected; no network use.
Tools: none installed or upgraded. Versions read: `bwrap --version` = 0.13.1; `pacman -Q bubblewrap util-linux` =
0.13.1-1 / 2.42.4-1 (query only, no transaction); `unshare --version` = util-linux 2.42.4.
Scratch `/fast/scratch/hyaku/chousa-r62/SentC1V2Safety/` deleted before yield; my markers removed (verified).

## Findings

1. **The v2 sandbox is not a filesystem boundary.** `SANDBOX = ["unshare","-Ufp","--kill-child","--mount-proc"]`
   creates user, pid and mount namespaces only. Verified (`readlink /proc/self/ns/*`): host net, ipc and uts
   namespace inodes are shared with the sandbox (`net=net:[4026531833]` on both). The builder keeps kuid 1000
   (`vgpnk`); the user-namespace mapping changes only what the process displays, not owner checks. Files it
   creates are owned by `1000 1000` on the host (`ls -ln` after the probe).
2. **Outside writes succeed.** Probe `probe.py` under the counter's prefix (driver `drive.py`, variant V0):
   `W1` scratch outside fixture = WROTE, `W2` lane sentinel dir = WROTE, `W3` `$HOME/.cache` = WROTE, `W4`
   `$HOME` root = WROTE. Frozen counter with the harmless hostile builder `hostile-builder.py` (writes 3 markers
   per invocation, exits 2): after the run, 44 markers each in scratch, `~/.cache` and the lane sentinel dir.
3. **Reads and reach (access checks only, `os.access` R_OK/W_OK, V0 = counter sandbox):**
   `~/.ssh/id_ed25519` R_OK; `~/.gnupg/private-keys-v1.d` R_OK; `~/.claude.json` R_OK;
   `~/.1password/agent.sock` W_OK; `/run/user/1000/bus` (srw-rw-rw-) W_OK; `/run/user/1000` lists `gnupg`,
   `keyring`, `pipewire-0`, `1Password-BrowserSupport.sock`; another seat's scratch (`CritC1Timing`) W_OK;
   `tools/` in the lane W_OK; frozen `c1v2-count.py` W_OK. Network: host interfaces (`br-*`, `docker0`, `enp7s0`,
   `lo`) visible, so anything read can leave the host.
   INFERENCE (not run, no connection made): the session D-Bus and 1Password agent sockets are reachable by the
   builder and could be used to request secrets; `~/.ssh/authorized_keys` and `~/.bashrc` are owner-writable.
4. **Lane poisoning path.** The counter copies `tools/capture-text.py` from the lane into every fixture and checks
   only the fixture's tool names (`tools_unchanged`). It never re-hashes lane bytes. A builder that rewrites lane
   `tools/` affects every later leg. INFERENCE: the write path is shown by W_OK plus owner match; I did not alter
   any lane bytes.
5. **What the counter relies on, each measured:**
   - `RLIMIT_FSIZE` 512 MiB: `ftruncate` to 600 MiB → `errno=27 File too large` (V0, V1, V2). Per file only; no
     total quota. INFERENCE: total disk fill is bounded only by the filesystem (`/fast` 543 G free).
   - `RLIMIT_AS` 200 MiB: `bytearray(300 MiB)` → `MemoryError` (V0, V1, V2). Per process.
   - 60 s timeout and `killpg`: a `setsid` child that writes a heartbeat every 0.5 s stops after the driver's
     `killpg` (V0, V1, V2: `heartbeat_exists=True`, `heartbeat_written_after_kill=False`) and after the builder
     exits normally (`escape-exit`, V0, V1, V2: same). The kill of detached children comes from pid-namespace
     teardown, not from `killpg`.
   - pid namespace hides host processes: `/proc` shows one entry in V0 (`proc_entries=1`), `/proc/<host pid>`
     absent (`host_pid_visible=false`).
   - Fail-closed: `SANDBOX + ["true"]` pre-check exits 2 when the sandbox is missing (observed with the bwrap copy
     and a missing bind source: `sandbox unavailable (unshare exit 1); fail closed`, exit 2). The message says
     `unshare` even under bwrap; cosmetic.
   - No `RLIMIT_NPROC`, no `RLIMIT_NOFILE`, no CPU limit beyond the 60 s timeout. `ulimit -u` = 122865, `pid_max`
     = 4194304, vgpnk had 426 processes. INFERENCE (not run): a fork bomb consumes the user's process budget.

## Hardening that keeps the legs working (tested)

Cheapest options checked:
- `unshare -Ufrp` (map root) and `--map-user`: **no effect on files.** V1 (map root) wrote every marker
  (`uid 0` inside, `1000` on host). Not hardening.
- `bwrap` (bubblewrap 0.13.1): empty tmpfs root, read-only `/usr` and `/etc`, `/proc`, `/dev`, `/tmp` tmpfs, only
  the fixture bound read-write, and `--unshare-user --unshare-pid --unshare-ipc --unshare-uts --unshare-net
  --die-with-parent`. Verified (V2): `/home`, `/run/user`, `/fast/.../probe-out`, lane `Projects/` and `.ssh`
  absent; `echo x > /home/vgpnk/...` fails; net, ipc, uts, pid, mnt, user namespaces differ from host; probe
  `W1–W4` all land inside the sandbox and none on the host (checked `ls`); escape and fsize/as limits unchanged.

Copy of the counter with only the SANDBOX line and the LANE line changed (frozen file untouched):
```
SANDBOX = ["bwrap","--unshare-user","--unshare-pid","--unshare-ipc","--unshare-uts","--unshare-net",
           "--die-with-parent","--ro-bind","/usr","/usr","--symlink","usr/bin","/bin","--symlink","usr/lib","/lib",
           "--symlink","usr/lib","/lib64","--ro-bind","/etc","/etc","--proc","/proc","--dev","/dev",
           "--tmpfs","/tmp","--bind",WORKROOT,WORKROOT]
LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/chousa-shokunin")
```
`WORKROOT` must exist before the run (the pre-check fails closed otherwise).

Legs with the copy (`--builder tools/build-spans.py`, `--work` under WORKROOT, fresh per run):
| run | counter | seed | result |
|---|---|---|---|
| base | frozen | `C1V2_SEED=62001` | `LEGS=20/20 C1V2=PASS` exit 0 |
| base | frozen | random ×3 | `LEGS=20/20 C1V2=PASS` exit 0 ×3 |
| bwrap copy | copy | `C1V2_SEED=62001` | `LEGS=20/20 C1V2=PASS` exit 0 |
| bwrap copy | copy | random ×3 | `LEGS=20/20 C1V2=PASS` exit 0 ×3 |

Hostile builder (`hostile-builder.py`, exit 2): base run `LEGS=14/20 C1V2=FAIL` (expected) and 44 markers each in
three locations; bwrap run `LEGS=14/20 C1V2=FAIL` (expected) and **0 new markers** (census 44/44/44 before and
after).

Named gaps of the copy (not closed here): the bind is read-write on the whole `--work` root (sibling legs are
visible and writable); no `RLIMIT_NPROC` or disk quota; the copy is not in the frozen tree; the battery
(23 counter runs) was **not run** by this seat, so the copy's battery verdict is unknown.

## Verdict inputs for L1

- Frozen counter: sandbox does not contain writes or reads; any builder can reach the lane, other seats and the
  user's home, and the network. Its own legs cannot detect this (they check the fixture only).
- Routed (limit, not rewrite, per the claims freeze): bwrap read-only system binds with a fixture-only read-write
  bind, `--unshare-net`, plus `RLIMIT_NPROC` in `preexec_fn`; re-run the battery on the copy before any claim.
- Operability of the hardened copy: legs 20/20 at 4 seeds; hostile builder 0 outside writes.

VERDICT: OUTSIDE_WRITES_POSSIBLE=yes hardening=bwrap with fixture-only read-write bind and read-only system mounts
