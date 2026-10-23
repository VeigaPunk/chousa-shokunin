# Round 36 wave 1 — ExecWitnessDirect

**Axes:** operability (pinned-gate execution) and calibration (per-record attribution evidence).

## Verdict

**PASS for the assigned direct witness run, seed 36341:** `WITNESS=pass OUTPUT=9/9 ATTRIB=9/9 MATCHER_CALLS=11`; receipt gate SHA-256 is the landed `a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8`. No bypass is established by this run. This is one direct witness result, **not** the C2 counter's multi-seed P2 verdict; I did not run C1 or C2 counters.

## Commands and retained evidence

All commands below completed with exit 0. For the witness commands, the deciding line is the quoted summary; the direct receipt additionally records `witness=pass`, `output_full=true`, `output_match=9`, `output_total=9`, `unattributed=[]`, and the pinned gate hash. `argv-witness.py:372-373` returns 0 exactly when the witness passes and output is full.

1. Exact setup/pin command:
   ```sh
   timeout 900 bash -c 'mkdir -p /tmp/hyaku/chousa-r36/w1/ExecWitnessDirect /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecWitnessDirect && cd /home/vgpnk/Projects/shokunin/chousa-shokunin && printf "master=" && git rev-parse master && sha256sum tools/research-gate.sh'
   ```
   Deciding output: `master=700bd5fcbf9abc118a6a0f078d51a2e7460c2878`; `a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8  tools/research-gate.sh`.

2. Exact assigned direct witness command:
   ```sh
   cd /home/vgpnk/Projects/shokunin/chousa-shokunin && WITNESS_TMP=/tmp/hyaku/chousa-r36/w1/ExecWitnessDirect timeout 1800 python3 tools/argv-witness.py --gate tools/research-gate.sh --seed 36341 --json /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecWitnessDirect/witness-s36341.json
   ```
   Deciding stdout: `WITNESS=pass OUTPUT=9/9 ATTRIB=9/9 MATCHER_CALLS=11`. Receipt: gate rc 1, drift true, 12 recorder calls, 11 matcher calls, 8 long records, no misses, 9/9 attributed. The gate rc/drift are expected by the witness's `output_full` condition.

3. Capture-only preparation (copy of the witness; no production file changed):
   ```sh
   timeout 900 cp /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/argv-witness.py /tmp/hyaku/chousa-r36/w1/ExecWitnessDirect/argv-witness-capture.py
   ```
   In that scratch copy only, line 371's `shutil.rmtree(root, ignore_errors=True)` was replaced by a comment so the recorder log survived for inspection. All other logic was retained. This capture-only rerun is not counted as an independent measurement.

4. Capture-only rerun command:
   ```sh
   cd /home/vgpnk/Projects/shokunin/chousa-shokunin && WITNESS_TMP=/tmp/hyaku/chousa-r36/w1/ExecWitnessDirect timeout 1800 python3 /tmp/hyaku/chousa-r36/w1/ExecWitnessDirect/argv-witness-capture.py --gate tools/research-gate.sh --seed 36341 --json /tmp/hyaku/chousa-r36/w1/ExecWitnessDirect/witness-capture-s36341.json
   ```
   Deciding stdout: `WITNESS=pass OUTPUT=9/9 ATTRIB=9/9 MATCHER_CALLS=11`.

5. Exact NUL-to-line conversion command used to expose the recorder format:
   ```sh
   timeout 900 bash -c 'tr "\\0" "\\n" < /tmp/hyaku/chousa-r36/w1/ExecWitnessDirect/r36wit-00008df5-g1ed63aw/_witness/rec/gussghceseyf.log > /tmp/hyaku/chousa-r36/w1/ExecWitnessDirect/argv-log-tr.txt && wc -lc /tmp/hyaku/chousa-r36/w1/ExecWitnessDirect/argv-log-tr.txt && sha256sum /tmp/hyaku/chousa-r36/w1/ExecWitnessDirect/argv-log-tr.txt'
   ```
   Deciding output: `102 164476 .../argv-log-tr.txt`; converted-log SHA-256 `4ee3a68f55c0b8b8a23ee2399c59e0c9da202d09b6fdce18fc0d02e1af9bdb50`. Its structure is one marker line followed by that invocation's NUL-separated arguments, with the next marker delimiting the next call. The opening excerpt is:
   ```text
   W36CALL-6a21b127606a5f8f3dd9421b
   --version

   W36CALL-6a21b127606a5f8f3dd9421b
   -a
   -z
   -b
   -o
   -P
   --
   x

   W36CALL-6a21b127606a5f8f3dd9421b
   -a
   -z
   -b
   -o
   -P
   --
   \\x77(?=\\x6e\\x20\\x69\\x76\\x70\\x7a\\x67\\x71\\x70\\x20...)
   ```

6. Exact command used to establish the selected record's length and chunk hash:
   ```sh
   cd /home/vgpnk/Projects/shokunin/chousa-shokunin && jq -r 'select(.id=="h2d4adaa48") | (.span|length)' /tmp/hyaku/chousa-r36/w1/ExecWitnessDirect/r36wit-00008df5-g1ed63aw/claims.jsonl && jq -jr 'select(.id=="h2d4adaa48") | .span[:4096]' /tmp/hyaku/chousa-r36/w1/ExecWitnessDirect/r36wit-00008df5-g1ed63aw/claims.jsonl | sha256sum
   ```
   Deciding output: full span length `32765`; first-4096-byte SHA-256 `2694acdc410f1762b30b2ed8e6ce98c80dfe3b2cefb310b9d02edba4739de044`. The captured matcher argv for record `h2d4adaa48` is `[-a, -z, -b, -o, -P, --, "\\x77(?=<record span prefix>)"]`; the abbreviated pattern represents the first 4096 bytes of that record's 32765-byte span (SHA-256 above). The actual logged pattern begins `\\x77(?=\\x6e\\x20\\x69\\x76\\x70\\x7a\\x67\\x71\\x70...)`. The direct receipt attributes this ID as `chunk`; witness source lines 275-287 defines chunk attribution as exact equality with `span[:4096]`.

7. Exact artifact archival/hash command:
   ```sh
   timeout 900 bash -c 'd=/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecWitnessDirect; s=/tmp/hyaku/chousa-r36/w1/ExecWitnessDirect; cp "$s/r36wit-00008df5-g1ed63aw/_witness/rec/gussghceseyf.log" "$d/argv-recorder-s36341.bin" && cp "$s/argv-log-tr.txt" "$d/argv-recorder-s36341.tr.txt" && cp "$s/witness-capture-s36341.json" "$d/witness-capture-s36341.json" && cp "$s/argv-witness-capture.py" "$d/argv-witness-capture.py" && sha256sum "$d/witness-s36341.json" "$d/argv-recorder-s36341.bin" "$d/argv-recorder-s36341.tr.txt" "$d/witness-capture-s36341.json" "$d/argv-witness-capture.py"'
   ```

## Channel independence

`tools/argv-witness.py:199-213` draws the marker and log name from its own RNG and embeds them in the recorder script; it does not export either value. In `:316-326`, the witness builds the recorder before the gate environment, removes inherited `CHOUSA_*`/`RESEARCH_GATE_*`, then adds only the recorder as `RESEARCH_GATE_GREP` and the declared `CHOUSA_WITNESS_KEY`. At `:328-332`, gate stderr goes to `_stderr.log`, while attribution reads `read_calls(rlog, rmark)` from the recorder log. Thus the observed marker/log channel is outside the gate's environment and not gate stderr.

## Files opened (access date 2026-10-23)

- `/home/vgpnk/.agents/skills/godspeed/SKILL.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1-briefs/ExecWitnessDirect.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round36/claims.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round36/c1-count.py`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round36/c2-count.py`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/argv-witness.py`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/mechanism-witness.py`
- `/home/vgpnk/.omp/agent/RULES.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/measure/c2-after-s36001.json`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/measure/c2-after-s36011.json`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh` (SHA-256 checked; not modified)
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecWitnessDirect/witness-s36341.json`
- `/tmp/hyaku/chousa-r36/w1/ExecWitnessDirect/argv-witness-capture.py` (scratch-only capture copy)
- `/tmp/hyaku/chousa-r36/w1/ExecWitnessDirect/r36wit-00008df5-g1ed63aw/_witness/rec/gussghceseyf.log` (binary; read as raw, then converted with `tr`)
- `/tmp/hyaku/chousa-r36/w1/ExecWitnessDirect/argv-log-tr.txt`
- `/tmp/hyaku/chousa-r36/w1/ExecWitnessDirect/r36wit-00008df5-g1ed63aw/claims.jsonl` (queried for the attributed record)
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecWitnessDirect/witness-capture-s36341.json`

## Artifacts and SHA-256

All saved artifacts are under the assigned directory and below 1 MiB:

- `.ufo/waves/round-36/w1/ExecWitnessDirect/witness-s36341.json` — `f13b974b0db63c7b5dd334a3cdb1dea923b3cd52a38419e415b4b063e1d38081`
- `.ufo/waves/round-36/w1/ExecWitnessDirect/argv-recorder-s36341.bin` — `fd0f476a4e7cfd808b2b90091ea30daf4758a36b4947db5900efebc8c3336b6b`
- `.ufo/waves/round-36/w1/ExecWitnessDirect/argv-recorder-s36341.tr.txt` — `4ee3a68f55c0b8b8a23ee2399c59e0c9da202d09b6fdce18fc0d02e1af9bdb50`
- `.ufo/waves/round-36/w1/ExecWitnessDirect/witness-capture-s36341.json` — `5a8e150344230c60d511565cd1330eb95666d8623073cbdcee40e9e92aaf50a6`
- `.ufo/waves/round-36/w1/ExecWitnessDirect/argv-witness-capture.py` — `2e1304a94a364ea4530b3d326c47f97fd2d3c3a8e119b4265ae0d506e17b52da`

No tools were installed or updated. No lane production files were changed. No blockers.

## Risks / limits

The known call-for-show limit remains: a gate may query the pinned matcher and ignore its answer. The witness demonstrates that each record's bytes were queried; the output-match check is separate. Active anti-instrumentation by a gate that reads the recorder script is outside the claim's stated scope.
