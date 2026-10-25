# Round 45 wave 2 — Mutation probe: tools/parent-lifetime.sh launcher edges

Seat: L1Chousa45.MutLauncherEdges. Target: `tools/parent-lifetime.sh` at lane commit
5e8c7ad2f7b8254d83358820286e3d12ca4672d1 (measured over `git archive` bytes, not the live repo).
Measured bytes: parent-lifetime.sh sha256 `d2c77c860c9ab051f6e5bc0549931e54a08b3001ab8a7173f956139aae280ff8`;
c1-count.py sha256 `72382086953604c39548ca5d182dbbc2a9a8eb260450ab3c5d2cd1c8dfe92e70`.
Resolvable pointers are to the archived file `tree/tools/parent-lifetime.sh`.

Method: stub `kimi` (copy of c1-count.py STUB + a TERM-trapping mode) placed first on PATH,
in `/tmp/chousa-r45-MutLauncherEdges/bin/kimi`; each probe ran
`env PATH=<tmp>/bin:$PATH STUB_MODE=… bash tree/tools/parent-lifetime.sh --receipt $d/receipt …`
Two-seat dispatches built exactly as c1-count.py `dispatch()` does
(`{"taskCall":{"context":"c","tasks":[{"name":"A",…},{"name":"B",…}]}}`).

## Probes (verbatim decisive output)

### A. Dispatch file that is not JSON (`--timeout 1`) → exit 3
stderr (tail):
```
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
parent-lifetime: incomplete wave n_spawned=0 n_timeout=0
```
receipt:
```
start parent_pid=2710390 epoch=1792921763 timeout_s=1
end parent_pid=2710390 epoch=1792921763 n_spawned=0 n_reaped=0
```
Malformed JSON is silently treated as a zero-task dispatch; the JSON traceback leaks to the caller's
stderr. Exit 3 = header "zero tasks were spawned" clause; no header misstatement.

### B. Stub exiting 1 (failed seat, not timeout; `--timeout 5`) → exit 0
```
start parent_pid=2710398 epoch=1792921763 timeout_s=5
spawn name=A child_pid=2710405 epoch=1792921764
spawn name=B child_pid=2710408 epoch=1792921764
reap name=A child_pid=2710405 exit_code=1 epoch=1792921764
reap name=B child_pid=2710408 exit_code=1 epoch=1792921764
end parent_pid=2710398 epoch=1792921764 n_spawned=2 n_reaped=2
```
Exit 0 per header ("every child reaped, no seat timed out"); non-zero child exit ≠ timeout. OK.

### C. Seat killed by SIGKILL: `--timeout 1` + stub trapping TERM → exit 3
stderr: `Killed` job notes for both children; `parent-lifetime: incomplete wave n_spawned=2 n_timeout=2`.
```
start parent_pid=2710416 epoch=1792921764 timeout_s=1
spawn name=A child_pid=2710423 epoch=1792921764
spawn name=B child_pid=2710426 epoch=1792921764
reap name=A child_pid=2710423 exit_code=137 epoch=1792921785
reap name=B child_pid=2710426 exit_code=137 epoch=1792921785
end parent_pid=2710416 epoch=1792921785 n_spawned=2 n_reaped=2
```
Exit 3 per header ("a seat exited 124/137 (timeout)"), receipt complete. Took ~21 s (TERM at 1 s,
KILL at `--kill-after=20`); expected from the tool's own `--kill-after=20`.

### D. `--timeout 0` → exit 2, usage; no receipt file created. Regex `^[1-9][0-9]*$` (line 40) rejects.
### E. `--timeout abc` → exit 2, usage; no receipt file created.
### F. `--selftest` without `--timeout` → exit 0
```
start parent_pid=2787242 epoch=1792921785 timeout_s=0
spawn name=SelfA child_pid=2787258 epoch=1792921785
spawn name=SelfB child_pid=2787262 epoch=1792921785
reap name=SelfA child_pid=2787258 exit_code=0 epoch=1792921785
reap name=SelfB child_pid=2787262 exit_code=0 epoch=1792921785
end parent_pid=2787242 epoch=1792921785 n_spawned=2 n_reaped=2
```
Line 38 defaults TIMEOUT to 0; start line carries `timeout_s=0`.
### G. `--selftest --timeout 1` → exit 0, identical shape with `timeout_s=1`.
### H. Dispatch without `--timeout` → exit 2, usage; no receipt. Matches header's explicit "including a dispatch run without --timeout".

## Verdict

All eight probes behave exactly as the header contract states: exit 0 only when end line written,
n_spawned>0, all children reaped, no 124/137; exit 3 when zero tasks spawned or any 124/137, with a
complete receipt; exit 2 on usage (invalid/absent `--timeout`), before any receipt is created/truncated.
Start lines always carry `timeout_s=` with the value passed (0 in default selftest). **No header
misstatement found — all claims hold.**

Observations (not contract violations, no change proposed):
1. Malformed dispatch JSON is indistinguishable from a genuinely empty task list (both → exit 3,
   n_spawned=0); `JSONDecodeError` traceback leaks to stderr with no parent-lifetime diagnostic.
   Header is silent on malformed JSON, so not misstated. Resolvable: archived lines 62-70 (mapfile /
   `json.load`), exit path lines 119-121.
2. SIGKILL detection relies on GNU timeout's 137 propagation; a TERM-trapping seat costs ~21 s per
   wave (`--kill-after=20`), still exit 3 with complete receipt.

Evidence: outputs above are verbatim from the probes; receipt contents are the tool's own writes.
Scratch `/tmp/chousa-r45-MutLauncherEdges` deleted. No lane/fleet files touched; no fetch, no network.
