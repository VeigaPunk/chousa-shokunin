# ExecC1ScenarioMap — round 36, wave 1

Axes: **operability** (assigned C1 scenario evidence); calibration was not scored in this scoped move.

## Verdict

**VERDICT: The four assigned C1 arms S11–S14 reproduce as PASS on landed gate seed 36331; the full counter is 14/14 with `predicate_holds=true`.** This is one fresh seed, not by itself the frozen two-seed P1. The gate scored was `tools/research-gate.sh`, SHA-256 `a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8`; the base control was pinned at `a47688518e509edbf43b433a5e16e1cf2481233f3acedb5824ba341f7f0c38ad`.

The frozen rule says, “Any run of the counter against the landed gate below 14/14 kills C1” (`corpus/evidence/round36/claims.md`, accessed 2026-10-23). The command and receipt below give 14/14. No production file was changed.

## Four arms

### S11 — manifest hash shim

**Counter detail (receipt):** `pass=true`, `rc=0`, `manifest_ok=true`, `stderr_tail=""`; observed record SHA `721d2837dfeeba3a88405a42053c818ae7233ae5e8b1b452d27ac0f00b854fde`, gate SHA `a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8`.

**Hand reproduction:** with the hostile `sha256sum` first on PATH, landed `verify-all` exited 0 and emitted `RESEARCH_GATE: CLEAN`; its manifest held the same two true hashes above. Base-control `verify-all` also exited 0 and emitted CLEAN, but its manifest fields were both `HOSTILE-CUT-OUTPUT`. Thus the base failure is false manifest identity despite a successful gate exit.

**MEETS-ADJACENT (wording caveat):** no named refusal was emitted by the landed gate for the specified hostile-PATH fixture; it successfully ignored the PATH shim and produced real hashes, as S11 requires. The named failure branch exists in source as “sha256sum unavailable or returned a non-hex value; manifest not written” (`tools/research-gate.sh`, accessed 2026-10-23), but that condition was not induced by this fixture. I did not modify an absolute system utility or the gate to force it.

### S12 — C-locale decode

**Counter detail (receipt):** `pass=true`; UTF-8 and C locale both had `rc=0`, with `L1` parsed as `supported / match` in both.

**Hand reproduction:** using the `\u00e9` JSON span and UTF-8 source bytes under `LC_ALL=C`, landed emitted `CLAIM id=L1 expected=supported observed=supported source=src/cafe.md at=line:1 verdict=match`, `RESEARCH_GATE: CLEAN`, and exited 0. Base control emitted `CLAIM id=L1 expected=supported observed=unsupported source=src/cafe.md at=- verdict=mismatch`, `FINDING CLAIM_SPAN_NOT_FOUND`, and `RESEARCH_GATE: DRIFT`; it exited 1.

### S13 — pin echo isolation

**Counter detail (receipt):** `pass=true`; `pin_rc=0`, `drift_rc=0`, `drift_out="GATE_DRIFT: none"`, `baseline_echo=false`; pin command stderr captured `GATE_GREP: path=/usr/bin/grep source=default version="grep (GNU grep) 3.12-modified"`.

**Hand reproduction:** landed `--pin` exited 0, subsequent `--drift` emitted `GATE_DRIFT: none` and exited 0, and the pinned baseline had no `GATE_GREP:` line. Base-control `--pin` exited 0, but its baseline did contain that line; `--drift` emitted `GATE_DRIFT: -LINE` and exited 1.

### S14 — drift token

**Counter detail (receipt):** `pass=true`; `pin_rc=0`, `drift_rc=1`, `drift_out="GATE_DRIFT: -GATE_GREP"`.

**Hand reproduction:** inserted `GATE_GREP: path=/usr/bin/grep source=default version="x"` after the canonical-output marker. Landed `--pin` exited 0; `--drift` emitted `GATE_DRIFT: -GATE_GREP` and exited 1. Base-control `--pin` exited 0; the same injected token produced `GATE_DRIFT: -LINE` and exited 1.

## Commands run (verbatim)

Each command was time-bounded. Outputs named above are the deciding lines; the counter command explicitly printed its overall exit code.

1. Gate/base pin and lane tip — exit 0; output lines were the two expected gate hashes and `700bd5fcbf9abc118a6a0f078d51a2e7460c2878`:

```sh
timeout 900s bash -lc 'mkdir -p /tmp/hyaku/chousa-r36/w1/ExecC1ScenarioMap /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecC1ScenarioMap && sha256sum /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/controls/base-gate-r36.sh && git -C /home/vgpnk/Projects/shokunin/chousa-shokunin rev-parse master'
```

2. Fresh counter — exit 0; decisive line `ENGINE_SWAP_CANARY=14/14`, followed by all 14 scenario lines marked PASS and `EXIT=0`:

```sh
timeout 1800s env C1_TMP=/tmp/hyaku/chousa-r36/w1/ExecC1ScenarioMap C2_TMP=/tmp/hyaku/chousa-r36/w1/ExecC1ScenarioMap WITNESS_TMP=/tmp/hyaku/chousa-r36/w1/ExecC1ScenarioMap TMPDIR=/tmp/hyaku/chousa-r36/w1/ExecC1ScenarioMap python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round36/c1-count.py --gate /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh --seed 36331 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecC1ScenarioMap/c1-s36331.json; rc=$?; printf 'EXIT=%s\n' "$rc"; exit "$rc"
```

3. Scratch fixture directories — exit 0:

```sh
timeout 900s mkdir -p /tmp/hyaku/chousa-r36/w1/ExecC1ScenarioMap/hand/s11/lib /tmp/hyaku/chousa-r36/w1/ExecC1ScenarioMap/hand/s11/hostile-bin /tmp/hyaku/chousa-r36/w1/ExecC1ScenarioMap/hand/s12/src
```

The hand fixtures were written under `/tmp/hyaku/chousa-r36/w1/ExecC1ScenarioMap/hand/`: S11 reused the counter's `RECORD_D` and `CLAIMS_D` shape with the counter's hostile shim; S12 used `{"id":"L1","source":"src/cafe.md","span":"caf\\u00e9","expect":"supported"}` and UTF-8 `café` source bytes.

4. S11 landed/base reproduction — shell command exit 0; its printed decisive per-gate statuses were `LANDED_S11_EXIT=0`, `BASE_S11_EXIT=0`. Landed manifest hashes were real; base manifest hashes were poisoned:

```sh
timeout 900s bash -lc 'set +e
s=/tmp/hyaku/chousa-r36/w1/ExecC1ScenarioMap/hand/s11
gate=/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh
base=/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/controls/base-gate-r36.sh
path="$s/hostile-bin:/usr/local/bin:/usr/bin:/bin"
env -i PATH="$path" LC_ALL=C LANG=C /usr/bin/bash "$gate" verify-all "$s/record.md" --claims "$s/claims.jsonl" --json "$s/landed.jsonl" --root "$s"
rc=$?; printf "LANDED_S11_EXIT=%d\n" "$rc"; /usr/bin/cat "$s/landed.jsonl"
env -i PATH="$path" LC_ALL=C LANG=C /usr/bin/bash "$base" verify-all "$s/record.md" --claims "$s/claims.jsonl" --json "$s/base.jsonl" --root "$s"
rc=$?; printf "BASE_S11_EXIT=%d\n" "$rc"; /usr/bin/cat "$s/base.jsonl"'
```

5. S12 landed/base reproduction — shell command exit 0; deciding statuses were `LANDED_S12_EXIT=0` and `BASE_S12_EXIT=1`, with the match/mismatch lines recorded above:

```sh
timeout 900s bash -lc 'set +e
s=/tmp/hyaku/chousa-r36/w1/ExecC1ScenarioMap/hand/s12
gate=/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh
base=/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/controls/base-gate-r36.sh
path=/usr/local/bin:/usr/bin:/bin
env -i PATH="$path" LC_ALL=C LANG=C /usr/bin/bash "$gate" verify-claims "$s/claims.jsonl" --root "$s"
rc=$?; printf "LANDED_S12_EXIT=%d\n" "$rc"
env -i PATH="$path" LC_ALL=C LANG=C /usr/bin/bash "$base" verify-claims "$s/claims.jsonl" --root "$s"
rc=$?; printf "BASE_S12_EXIT=%d\n" "$rc"'
```

6. S13/S14 landed/base reproduction — shell command exit 0; deciding lines were the landed `GATE_DRIFT: none` / `GATE_DRIFT: -GATE_GREP` and base `GATE_DRIFT: -LINE` outputs, with statuses recorded above:

```sh
timeout 900s bash -lc 'set +e
path=/usr/local/bin:/usr/bin:/bin
s=/tmp/hyaku/chousa-r36/w1/ExecC1ScenarioMap/hand/s13
mkdir -p "$s"
gate=/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh
base=/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/controls/base-gate-r36.sh
env -i PATH="$path" LC_ALL=C LANG=C CHOUSA_GREP_PIN_ECHO=1 /usr/bin/bash "$gate" --pin "$s/landed-pin.txt"
rc=$?; printf "LANDED_S13_PIN_EXIT=%d\n" "$rc"
env -i PATH="$path" LC_ALL=C LANG=C /usr/bin/bash "$gate" --drift "$s/landed-pin.txt"
rc=$?; printf "LANDED_S13_DRIFT_EXIT=%d\n" "$rc"
echo_seen=0; while IFS= read -r line || [[ -n $line ]]; do [[ $line == GATE_GREP:* ]] && echo_seen=1; done < "$s/landed-pin.txt"; printf "LANDED_S13_BASELINE_ECHO=%d\n" "$echo_seen"
env -i PATH="$path" LC_ALL=C LANG=C CHOUSA_GREP_PIN_ECHO=1 /usr/bin/bash "$base" --pin "$s/base-pin.txt"
rc=$?; printf "BASE_S13_PIN_EXIT=%d\n" "$rc"
env -i PATH="$path" LC_ALL=C LANG=C /usr/bin/bash "$base" --drift "$s/base-pin.txt"
rc=$?; printf "BASE_S13_DRIFT_EXIT=%d\n" "$rc"
echo_seen=0; while IFS= read -r line || [[ -n $line ]]; do [[ $line == GATE_GREP:* ]] && echo_seen=1; done < "$s/base-pin.txt"; printf "BASE_S13_BASELINE_ECHO=%d\n" "$echo_seen"
env -i PATH="$path" LC_ALL=C LANG=C /usr/bin/bash "$gate" --pin "$s/landed-drift.txt"
rc=$?; printf "LANDED_S14_PIN_EXIT=%d\n" "$rc"
tmp="$s/landed-drift.tmp"; while IFS= read -r line || [[ -n $line ]]; do if [[ $line == "# --- canonical output follows ---" ]]; then printf "%s\n" "$line" "GATE_GREP: path=/usr/bin/grep source=default version=\"x\"" >>"$tmp"; else printf "%s\n" "$line" >>"$tmp"; fi; done < "$s/landed-drift.txt"; mv "$tmp" "$s/landed-drift.txt"
env -i PATH="$path" LC_ALL=C LANG=C /usr/bin/bash "$gate" --drift "$s/landed-drift.txt"
rc=$?; printf "LANDED_S14_DRIFT_EXIT=%d\n" "$rc"
env -i PATH="$path" LC_ALL=C LANG=C /usr/bin/bash "$base" --pin "$s/base-drift.txt"
rc=$?; printf "BASE_S14_PIN_EXIT=%d\n" "$rc"
tmp="$s/base-drift.tmp"; while IFS= read -r line || [[ -n $line ]]; do if [[ $line == "# --- canonical output follows ---" ]]; then printf "%s\n" "$line" "GATE_GREP: path=/usr/bin/grep source=default version=\"x\"" >>"$tmp"; else printf "%s\n" "$line" >>"$tmp"; fi; done < "$s/base-drift.txt"; mv "$tmp" "$s/base-drift.txt"
env -i PATH="$path" LC_ALL=C LANG=C /usr/bin/bash "$base" --drift "$s/base-drift.txt"
rc=$?; printf "BASE_S14_DRIFT_EXIT=%d\n" "$rc"'
```

7. Receipt hash — exit 0:

```sh
timeout 900s sha256sum /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecC1ScenarioMap/c1-s36331.json
```

## Retained artifact, files opened, and limits

Artifact under the assigned artifact directory:

- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecC1ScenarioMap/c1-s36331.json` — SHA-256 `ca6664fae87d51baa5d5557e76eaaaebbe377696837753b2c7e198910c859a05`.

Files/source locations opened on 2026-10-23: `/home/vgpnk/.agents/skills/godspeed/SKILL.md`; `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1-briefs/ExecC1ScenarioMap.md`; `corpus/evidence/round36/claims.md`; `corpus/evidence/round36/c1-count.py`; `corpus/evidence/round36/c2-count.py`; `tools/argv-witness.py`; `tools/mechanism-witness.py`; `tools/research-gate.sh`; `.ufo/waves/round-36/controls/base-gate-r36.sh`; and the retained receipt above. I also listed `.ufo/waves/round-36/measure/` and the assigned artifact directory. Scratch manifest files read for the hand run were `/tmp/hyaku/chousa-r36/w1/ExecC1ScenarioMap/hand/s11/landed.jsonl` and `base.jsonl`.

Risks/blockers: the scoped seed is only one of the two required for frozen P1. The exact S11 hostile-PATH setup did not emit a named refusal; it passed with true hashes, while the base control generated poisoned hashes. No build, lint, formatter, or unrelated test suite was run. No installation was made.
