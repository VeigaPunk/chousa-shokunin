# W3ExecSelftest — falsifying the landed round-44 launcher selftest

Seat: round-44 wave 3, leaf. Date: 2026-10-24.
Target: `tools/parent-lifetime.sh` (108 lines, bash 5.3.20(1)-release host).
Method: run the mandated selftest, then probe the edges it does not reach.
All probe artifacts live in `/tmp/w3-*` and `/tmp/seat-logs/` — no lane-tree writes.

## 1. The mandated run

```
bash tools/parent-lifetime.sh --selftest --receipt /tmp/w3-selftest-exec.receipt
```

Exit code: **0** (wall time 0.244 s).

Receipt content, verbatim (`/tmp/w3-selftest-exec.receipt`):

```
start parent_pid=3637585 epoch=1792891714
spawn name=SelfA child_pid=3637589 epoch=1792891714
spawn name=SelfB child_pid=3637591 epoch=1792891714
reap name=SelfA child_pid=3637589 exit_code=0 epoch=1792891714
reap name=SelfB child_pid=3637591 exit_code=0 epoch=1792891714
end parent_pid=3637585 epoch=1792891714 n_spawned=2 n_reaped=2
```

The core round-43 closure claim holds *for this path*: one pid (3637585) opened,
spawned 2 children, reaped both itself, and closed. n_spawned == n_reaped == 2.

## 2. What the selftest covers

- Parent-lifetime contract for the trivial case: two `sleep 0.2` children,
  backgrounded and `wait`ed by the same shell, receipt lines written per event.
- Usage/exit-2 path: `bash parent-lifetime.sh` with no args → usage text, exit 2 (measured).
- Receipt creation via `mkdir -p` + truncate at the `--receipt` path.
- That's all. 6 of 108 lines (43–50) are the selftest branch; everything else is
  the dispatch branch the selftest never enters.

## 3. Falsifications — what it does not cover (all empirically probed)

### F1. The dispatch branch is entirely untested, and its failure mode is a green exit
Malformed dispatch JSON (`/tmp/w3-bad-dispatch.json` containing `{not json`):
python3 emits a `JSONDecodeError` traceback, `mapfile` ingests zero rows, zero
children spawn, the end line is written, and the script **exits 0**.

```
BAD_DISPATCH_EXIT=0
start parent_pid=3666484 epoch=1792891876
end parent_pid=3666484 epoch=1792891876 n_spawned=0 n_reaped=0
```

The script honors its stated contract ("Exit 0 when the end line is written")
— the contract itself is miscalibrated. A round driver keying on exit status
believes the wave launched. `n_spawned=0` is the only tell, and it sits in the
receipt text, not the exit code. Same outcome for valid JSON with an empty
`tasks` array.

### F2. Child failure never propagates to the launcher's exit code
Dispatch probe with a real child (`kimi 2.3.1` is installed on this host; it
ran and rejected my synthetic agent file: `Invalid agent file ... Missing
frontmatter`):

```
reap name=ProbeFail child_pid=3666503 exit_code=1 epoch=1792891876
end ... n_spawned=1 n_reaped=1     FAILING_CHILD_EXIT=0
```

Launcher exit 0 despite a failed child — twice confirmed (also the duplicate
probe below). Per-child status exists only as receipt text. This is by design
per the header comment, but the selftest cannot show it because `sleep 0.2`
cannot fail.

### F3. The end-of-run pid guard (line 102) is dead code
`parent_pid=$$` then `[[ "$$" -ne "$parent_pid" ]]` compares `$$` to itself.
Measured on this host:

```
PID_CHECK_DEAD_ALWAYS_FALSE   (bash 5.3.20(1)-release)
```

`$$` is constant for the life of a bash process; the "pid changed" exit-1
branch is unreachable. The receipt's matching `end parent_pid=` line is an
echo of a bash guarantee, not a check that anything was verified.

### F4. Exit-code 1 is overloaded by an accidental `set -e` state machine
`set -e` is off for the whole run, then switched ON at line 96 after the first
`wait`. Selftest with an unwritable receipt path (`--receipt /proc/w3-no-such-dir/r.receipt`):

```
mkdir: cannot create directory '/proc/w3-no-such-dir': No such file or directory
.../parent-lifetime.sh: line 37/38/49/49/97: ... No such file or directory
UNWRITABLE_EXIT=1
```

Only ONE line-97 error for two reaps: the first failed append under the now-on
`set -e` aborts the script. No end line, no diagnostics beyond bash redirection
spam. The documented meaning of exit 1 is "a child pid was not captured"; here
it means "receipt unwritable, aborted mid-loop". Documented contract ≠ behavior.

### F5. Duplicate task names silently overwrite prompt and log files
Dispatch with two tasks both named `Dup`: receipt records both spawns/reaps
(distinct pids, colliding names), but `seat-logs/Dup.prompt` contains only
`second body` — `first body` is destroyed before its child even reads it
(`printf '%s\n' "$body" > "$prompt_file"` truncates). `Dup.log` likewise holds
only the second child's output. No name-uniqueness check anywhere.

### F6. The receipt is self-attesting and destroyable
- Header admits: "The receipt is not proof against a later hand-edit."
- `: > "$RECEIPT"` truncates on every run — rerunning the selftest (or a wave)
  against the same path erases the prior run's evidence.
- The selftest child names (`SelfA`/`SelfB`) are labels the script prints
  itself; the spawn lines carry no independent corroboration.

### F7. Untested surfaces the selftest never touches
- JSON parsing success path, unit-separator task encoding (`\x1f`/`\x1e`),
  prompt-file writing, `seat-logs` creation.
- The real `kimi` invocation and its recorded constraint ("--auto and --yolo
  cannot combine with --prompt, kimi 2.3.1") — an untested assumption in a comment.
- `--timeout` / `timeout --kill-after=20` kill path (0.2 s sleeps never time out).
- The exit-1 "no pid captured" branch — with `$!` after a background spawn this
  is near-unreachable; untestable via selftest.
- Concurrent runs sharing a receipt path (last writer wins, interleaved lines).

## 4. Calibration summary for round drivers

| Signal | Trust level | Notes |
|---|---|---|
| launcher exit 0 | weak | true even for 0 spawned children or all-children-failed |
| launcher exit 2 | strong | usage/arg validation only |
| launcher exit 1 | ambiguous | documented "no pid"; observed "receipt unwritable, set -e abort" |
| receipt `end` line + `n_spawned` | moderate | hand-editable; but `n_spawned>0` is the minimum dispatch sanity gate |
| per-child `reap ... exit_code=` | moderate | the only child-status channel; parse it line-wise |

Minimum downstream gate the exit code does not give you: parse the receipt,
require `n_spawned == expected task count > 0`, require `n_reaped == n_spawned`,
and inspect each `reap exit_code`.

## 5. Cheap hardening suggestions (NOT applied — leaf bounds)

1. After the python parse: abort nonzero-exit if `${#TASKS[@]} -eq 0` (fixes F1).
2. Fail fast if the receipt path is not writable up front, with a named error
   and a distinct exit code (fixes F4's overloaded 1).
3. Uniqueness-check task names before spawning (fixes F5), or key log files by pid.
4. Delete or replace the `$$` guard (F3) — if pid continuity matters, re-exec
   a check or compare `/proc/$parent_pid/stat` fields honestly.
5. Append a `--append` mode or rotate receipts instead of `: >` truncation (F6).
6. Give the selftest one failing child and one `--timeout`-killed child so the
   reap `exit_code` and timeout paths are exercised, not just happy sleeps.

## 6. Verdict

The landed selftest passes and genuinely demonstrates the narrow round-43
closure property (same-pid spawn/reap of two trivial children) — but as a
launcher signal it is weak: it exercises 8 lines of 108, its exit code lies
green over empty dispatches and failed children (F1, F2), one of its two
documented failure codes is unreachable dead code (F3), the other is
overloaded by an accidental `set -e` abort (F4), and the receipt it produces
is truncated on rerun and self-attesting (F6). The wave-level landed state is
operable but not yet falsifiable by this selftest alone; §4's parsing gate is
the minimum discipline until §5 lands.
