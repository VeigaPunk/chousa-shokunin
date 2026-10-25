# ExecLauncherEdge — round 45 wave 1

## Assignment
Probe round-44 `tools/parent-lifetime.sh` with four `kimi` stub/dispatch edge cases; record tool exit codes and receipt lines; compare against frozen C1. Axes: operability, calibration, depth.

## Evidence and commands
Read frozen predicate: `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round45/claims.md:19-39` (snapshot `CD6B`). It requires zero-task exit 3 and end receipt, two successful seats exit 0 and `n_spawned=2 n_reaped=2`, timed-out seats exit 3 with both reaps 124, omitted timeout exit 2, and `timeout_s` start lines for cases a-c.

Read launcher: `/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/parent-lifetime.sh:22-38,51-85,87-108` (snapshot `A546`). Read stub recipe/counter logic: `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round45/c1-count.py:34-64,93-111` (snapshot `CC96`). Existing counter stub supports `ok` and `hang`; for these probes I extended the recipe in `/tmp/chousa-r45-ExecLauncherEdge/bin/kimi` with `exit1` and `kill9` modes. Scratch was removed after use. No tools installed.

Command executed:
```sh
set +e
SCRATCH=/tmp/chousa-r45-ExecLauncherEdge
TOOL=/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/parent-lifetime.sh
mkdir -p "$SCRATCH/agent"
printf 'stub\\n' > "$SCRATCH/agent/agent.yaml"
run_case() {
  tag=$1; mode=$2; kind=$3
  d="$SCRATCH/$tag"; mkdir -p "$d"
  if [ "$kind" = invalid ]; then printf 'not json\\n' > "$d/dispatch.json"; else python3 -c 'import json,sys; names=sys.argv[1:]; print(json.dumps({"taskCall":{"context":"c","tasks":[{"name":n,"task":"stub"} for n in names]}}))' ${kind#names:} > "$d/dispatch.json"; fi
  STUB_MODE="$mode" PATH="$SCRATCH/bin:$PATH" bash "$TOOL" --dispatch "$d/dispatch.json" --receipt "$d/receipt" --agent "$SCRATCH/agent/agent.yaml" --timeout 1
  ec=$?
  printf '\\nCASE %s TOOL_EXIT=%s\\n' "$tag" "$ec"
  if [ -f "$d/receipt" ]; then cat "$d/receipt"; else echo '(no receipt)'; fi
}
run_case sigkill kill9 names:SeatA
run_case exit1 exit1 names:SeatA
run_case invalid ok invalid
run_case spaced ok 'names:Seat One'
rm -rf "$SCRATCH"
exit 0
```

Verbatim decisive output (epoch values retained):
```text
/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/parent-lifetime.sh: line 93: 2398307 Killed                     timeout --signal=TERM --kill-after=20 "$TIMEOUT" kimi --agent-file "$AGENT" --prompt "$(cat "$prompt_file")" --output-format text > "$logdir/$name.log" 2>&1

CASE sigkill TOOL_EXIT=0
start parent_pid=2398233 epoch=1792920955
spawn name=SeatA child_pid=2398307 epoch=1792920955
reap name=SeatA child_pid=2398307 exit_code=137 epoch=1792920955
end parent_pid=2398233 epoch=1792920955 n_spawned=1 n_reaped=1

CASE exit1 TOOL_EXIT=0
start parent_pid=2398514 epoch=1792920955
spawn name=SeatA child_pid=2398585 epoch=1792920955
reap name=SeatA child_pid=2398585 exit_code=1 epoch=1792920955
end parent_pid=2398514 epoch=1792920955 n_spawned=1 n_reaped=1
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
  File "/usr/lib/python3.14/json/__init__.py", line 298, in load
    return loads(fp.read(),
        object_hook=object_hook, parse_float=parse_float, parse_int=parse_int,
        parse_constant=parse_constant, object_pairs_hook=object_pairs_hook, **kw)
  File "/usr/lib/python3.14/json/__init__.py", line 352, in raw_decode
    raise JSONDecodeError("Expecting value", s, err.value) from None
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)

CASE invalid TOOL_EXIT=0
start parent_pid=2398601 epoch=1792920955
end parent_pid=2398601 epoch=1792920955 n_spawned=0 n_reaped=0

CASE spaced TOOL_EXIT=0
start parent_pid=2398796 epoch=1792920955
spawn name=Seat child_pid=2398879 epoch=1792920955
spawn name=One child_pid=2398883 epoch=1792920955
reap name=Seat child_pid=2398879 exit_code=0 epoch=1792920955
reap name=One child_pid=2398883 exit_code=0 epoch=1792920955
end parent_pid=2398796 epoch=1792920955 n_spawned=2 n_reaped=2
```

## Results / frozen-predicate coverage
- **SIGKILL after `--kill-after`** (`trapkill`-like condition): tool exit **0**; receipt has `reap ... exit_code=137` and a normal end line. C1 does **not** cover exit 137: its timeout case explicitly expects 124 for both seats; it only tests a hanging process terminated by the configured timeout, not an uncatchable kill after the grace window. Residual limit: no contract for post-grace SIGKILL exit status.
- **Stub exits 1**: tool exit **0**; receipt records `exit_code=1`, followed by normal end. C1 does **not** cover generic seat failure (it exercises success and timeout only). Residual limit: seat nonzero exit codes are logged but do not make launcher fail.
- **Non-JSON dispatch**: tool exit **0**; receipt contains start and `end ... n_spawned=0 n_reaped=0`; Python JSON decoder traceback appears on stderr. C1 does **not** cover malformed dispatch input. Residual limit: parse failure is treated as empty work by the launcher and still receives successful exit/end receipt.
- **Task name containing a space**: input `Seat One` yields separate `Seat` and `One` spawn/reap entries; tool exit **0**; end says `n_spawned=2 n_reaped=2`. C1 does **not** cover whitespace-containing task names; its names are `SeatA`/`SeatB`. Residual limit: row parsing via shell whitespace splitting fragments task names containing spaces.

C1's scope is exactly its frozen cases (claims.md:23-29), not a general failure/dispatch/name-sanitization contract. No predicate changes proposed.

## Verdict
All four probes expose behaviors outside the frozen C1 predicate. They are recorded as residual limits, not grounds to retune the frozen claim. No production or lane files modified.