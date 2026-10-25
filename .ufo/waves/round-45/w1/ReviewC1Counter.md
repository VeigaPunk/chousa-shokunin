# Review C1Counter — round 45, wave 1

Seat: L1Chousa45.ReviewC1Counter (leaf, review-only). No subagents, no writes
outside this report.

## Item
Review `corpus/evidence/round45/c1-count.py` against frozen predicate R45-C1
(`corpus/evidence/round45/claims.md` lines 23-29): case fidelity (exit codes,
end-line fields, both reap lines `exit_code=124`, start-line `timeout_s`),
stub honesty, and whether a tool that ignores `--timeout` can false-PASS. Run
the counter against the lane tool and paste output.

## Verdict
The counter is faithful to the predicate on all five cases; its 1/5 verdict
against the committed `tools/parent-lifetime.sh` is a true negative — the
committed launcher does not yet implement (a) exit-3-on-empty, (c)
exit-3-on-timeout, (d) exit-2-on-omitted-`--timeout`, or (e) `timeout_s` in
the start line. The stub is honest (`exec sleep 30` under `timeout 1` returns
124). No realistic false-PASS on a tool that ignores `--timeout`. Minor
imprecisions (substring checks) are theoretical-only; none fires on the current
tool.

## Commands run + verbatim output (decisive lines)

Counter against the lane tool:

```
$ cd /home/vgpnk/Projects/shokunin/chousa-shokunin && python3 corpus/evidence/round45/c1-count.py; echo "EXIT=$?"
CASE a_empty_exits_3=FAIL
CASE b_ok_exits_0=ok
CASE c_timeout_exits_3=FAIL
CASE d_no_timeout_exits_2=FAIL
CASE e_start_timeout_s=FAIL
CASES_MATCH=1/5
C1=FAIL
EXIT=1
```

Manual probes of the launcher (stub `kimi` first on PATH):

```
=== stub honesty: hang mode under timeout 1 ===
STUB_EC=124
=== stub ok mode exit ===
STUB_OK_EC=0
=== case a: empty dispatch, --timeout 5 ===
A_EC=0
--- receipt ---
start parent_pid=2323942 epoch=1792920928
end parent_pid=2323942 epoch=1792920928 n_spawned=0 n_reaped=0
=== case c: two hang seats, --timeout 1 ===
C_EC=0
--- receipt ---
start parent_pid=2324071 epoch=1792920928
spawn name=SeatA child_pid=2324223 epoch=1792920928
spawn name=SeatB child_pid=2324226 epoch=1792920928
reap name=SeatA child_pid=2324223 exit_code=124 epoch=1792920929
reap name=SeatB child_pid=2324226 exit_code=124 epoch=1792920929
end parent_pid=2324071 epoch=1792920929 n_spawned=2 n_reaped=2
=== case d: omit --timeout ===
D_EC=0
--- receipt ---
start parent_pid=2331071 epoch=1792920929
spawn name=SeatA child_pid=2331192 epoch=1792920929
reap name=SeatA child_pid=2331192 exit_code=0 epoch=1792920929
end parent_pid=2331071 epoch=1792920929 n_spawned=1 n_reaped=1
```

Simulated counter sub-checks (proving FAILs are exit-code/start-line
mismatches, not counter bugs):

```
sim a (ec=3): True
sim c (ec=3): True | reaps: 2
e edge: value 5 vs timeout_s=50 -> True
e edge: value 1 vs timeout_s=10 -> True
e ok:  value 5 vs timeout_s=5  -> True
b edge: 'n_spawned=2' in 'end n_spawned=20 n_reaped=20' -> True
```

## Findings

F1. Case fidelity — matches the sentence, case by case.
- (a) c1-count.py:94: `ec == 3` + regex `\bn_spawned=0\b` on the last
  `end`-prefixed line (end_line, lines 67-69). Exact; the `\b` rejects
  `n_spawned=00`. Sentence (claims.md 24-25) satisfied.
- (b) c1-count.py:98-99: `ec == 0` + both strings in end line. Matches the
  sentence (claims.md 25-26). Imprecision: substring containment
  (`"n_spawned=2" in …`) would false-PASS on `n_spawned=20`/`n_reaped=20`
  (sim edge above). Cosmetic; only 2 seats are ever dispatched, so no tool
  whose receipt is arithmetically consistent triggers it.
- (c) c1-count.py:103-105: `ec == 3`, exactly 2 `reap`-prefixed lines, each
  containing the token ` exit_code=124 ` (trailing-space guard rejects
  `exit_code=1240`). Matches (claims.md 26-27). Good.
- (d) c1-count.py:109: `ec == 2` only, with a one-seat dispatch. The sentence
  (claims.md 27-28) specifies only the exit code; sufficient.
- (e) c1-count.py:72-74, 95/100/106, 111: per-receipt check that line 1
  starts `start ` and carries ` timeout_s=<value passed>` (5 for a/b, 1 for
  c), conjoined. Matches (claims.md 28-29). Imprecision: value is
  substring-matched, so `timeout_s=50` passes for value 5 and
  `timeout_s=10/100` for value 1 (sim edges). It still cannot pass on a tool
  that omits `timeout_s` (which is what the committed tool does).

F2. Stub honesty — honest. STUB (c1-count.py:34-40) `hang` mode `exec sleep 30`
replaces the shell; `timeout --signal=TERM --kill-after=20` sends TERM to that
same pid; GNU timeout then reports 124; the parent's `wait` sees 124 (probe:
`STUB_EC=124`; reap lines `exit_code=124`). ok mode exits 0
(`STUB_OK_EC=0`).

F3. False-PASS on a `--timeout`-ignoring tool — no realistic path. (c)
requires both reap lines `exit_code=124`, which only an actual kill produces
(a 30 s `sleep` ignores TERM exits 0 and fails); (d) requires exit 2 when the
flag is omitted; (e) requires `timeout_s` recorded in the start line. A tool
ignoring `--timeout` fails three of five. The only passing route is a forged
receipt (hard-coded 1 s killer + fabricated start field), which is outside a
black-box counter's reach under this predicate.

F4. Counter verdict vs committed tool — true negative. The launcher
(`tools/parent-lifetime.sh`) at head: start line has no `timeout_s` (line 38);
zero tasks → `n_spawned=0` then `exit 0` (lines 87-108), never 3; timeout path
kills via `timeout` (line 73) so reaps ARE 124 but the parent still exits 0
(line 108), never 3; omitting `--timeout` defaults to 420 (line 20) and exits
0, never 2. So (a),(c),(d),(e) are genuinely unmet; (b) genuinely met. The
counter's output (1/5, exit 1) is the correct falsification. (The sibling
`ExecLauncherPatch.md` indicates the launcher patch is a separate in-flight
item.)

F5. Robustness notes.
- `subprocess.run(..., timeout=120)` (line 62): a hang past 120 s raises an
  uncaught `TimeoutExpired` → traceback + exit 1, no CASE summary printed. It
  fails loudly (kill rule preserved), but output is not machine-parseable in
  that path.
- Case (c) checks `len(reaps)==2`, so a launcher that writes extra reap lines
  fails — correct-by-contract.
- The `--tool` override (line 79) lets the same counter score the round-44
  control; the committed control `controls/c1-control-r44-tool.txt` (1/5,
  exit 1) matches the counter's output shape.

## Residual risk / verification gaps
- Substring edges from F1 (b)/(e) are untested against a contrived receipt; a
  mutation testing the counter would find them. None affects the current
  verdict.
- I did not inspect or run the sibling's launcher patch; this review covers
  the committed tool at the freeze tree, which is what the counter measures.

Scratch cleaned: `/tmp/chousa-r45-L1Chousa45ReviewC1Counter` removed.
