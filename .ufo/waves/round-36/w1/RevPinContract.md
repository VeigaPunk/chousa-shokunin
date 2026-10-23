# RevPinContract — round-36 wave-1 review (pin/drift contract, R1/R2, cases 260/261)

Access date for all file reads: 2026-10-23. Lane root: `/home/vgpnk/Projects/shokunin/chousa-shokunin`.
Gate pinned: `tools/research-gate.sh` sha256 `a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8`; base control `a47688518e509edbf43b433a5e16e1cf2481233f3acedb5824ba341f7f0c38ad`; `git rev-parse master` = `700bd5fcbf9abc118a6a0f078d51a2e7460c2878` (= wave base). No tool installs performed. No lane file modified.

## Verdict

- **P1 re-derived: MET.** `ENGINE_SWAP_CANARY=14/14`, `predicate_holds=true` on fresh seeds 36301 and 36311 against the landed gate (receipts `rec/c1-s3630{1,1}.json`, gate_sha256 = landed).
- **P2 re-derived: MET.** `WITNESS_PER_RECORD=5/5 OUTPUT_EQUIV=5/5 LANDED_ATTRIB=pass RENAMED=pass`, `predicate_holds=true` on the same two fresh seeds (receipts `rec/c2-s3630{1,1}.json`, witness sha256 `e6832e0b…`).
- **R1 verdict: hole found (reproduced).** The `--pin`/`--drift` capture scrub of `CHOUSA_GREP_PIN_ECHO` is defeated by a caller-exported `BASH_ENV` that re-exports the flag: the baseline embeds a `GATE_GREP:` line and the unchanged gate reports a false drift. Reproducing command below. Does not kill C1 (the counter never sets a `BASH_ENV` exporter; S13 passes), but the repair is incomplete against the variable class it names.

## Findings (by severity)

### F1 HIGH — R1 scrub hole: `BASH_ENV` re-export smuggles `CHOUSA_GREP_PIN_ECHO` into the canonical capture

The capture scrubs the flag before exec: `tools/research-gate.sh:3921-3922` runs
`env -u CHOUSA_RECORD … -u CHOUSA_AGGREGATOR_ERE -u CHOUSA_GREP_PIN_ECHO bash "$SELF" verify-all …`
but `BASH_ENV` is not on the `-u` list. The inner bash sources `BASH_ENV` at startup, i.e. **after** `env -u` runs, so an exported re-export wins. The inner run's `grep_pin_init` echo (`research-gate.sh:417-418`, stderr `>&2`) then lands in `capture.txt` (`>capture.txt 2>&1`, line 3923-3924) and inside the compared canonical block.

Reproducing commands (scratch `/tmp/hyaku/chousa-r36/w1/RevPinContract/attack`, gate = landed sha):

```
printf 'export CHOUSA_GREP_PIN_ECHO=1\n' > benv.sh
BASH_ENV=$PWD/benv.sh bash research-gate.sh --pin base.txt   # pin_rc=0, baseline GATE_GREP count=1
env -u BASH_ENV     bash research-gate.sh --drift base.txt   # drift_rc=1, "GATE_DRIFT: -GATE_GREP"
```

Directions measured:
- pin under `BASH_ENV`, drift clean → `GATE_DRIFT: -GATE_GREP` exit 1 — **false drift against an unchanged gate** (erratum 8a symptom, reintroduced). Baseline polluted at canonical-block line 2: `GATE_GREP: path=/usr/bin/grep source=default version="grep (GNU grep) 3.12-modified"` (artifact `attack/base.txt`, sha256 `7a904b11…`).
- pin clean, drift under `BASH_ENV` → `GATE_DRIFT: +GATE_GREP` exit 1; the `--drift` invocation's **own stdout** also gains the stray `GATE_GREP:` line before `GATE_DRIFT:` (`attack/drift2.out`), breaking the "flag off ⇒ byte-identical existing-mode output" header promise (lines 344-345) and any caller doing a full-string stdout match.
- `BASH_ENV` on **both** sides → `GATE_DRIFT: none` exit 0, but the baseline now permanently carries engine identity (`path`/`source`/`version`) inside the compared body: a later default→override swap or grep upgrade reports field drift under the same hostile env. The hostile env silently converts the declared "behavior, not revision" baseline into an identity baseline.

Fix direction (one line): add `-u BASH_ENV` to the capture `env` at 3921 (or scrub the flag inside the capture invocation after sourcing). Not a C1 kill: the counter's S13 sets no `BASH_ENV` exporter, and both fresh-seed runs score 14/14.

### F2 PASS — claim re-derivations on fresh seeds (independent)

Commands (all from lane root, `TMPDIR`/`C1_TMP`/`C2_TMP`/`WITNESS_TMP` pointed at `/tmp/hyaku/chousa-r36/w1/RevPinContract`):

```
timeout 1800 python3 corpus/evidence/round36/c1-count.py --seed 36301 --receipt <art>/rec/c1-s36301.json   # rc=0
timeout 1800 python3 corpus/evidence/round36/c1-count.py --seed 36311 --receipt <art>/rec/c1-s36311.json   # rc=0
timeout 1800 python3 corpus/evidence/round36/c2-count.py --seed 36301 --receipt <art>/rec/c2-s36301.json   # rc=0
timeout 1800 python3 corpus/evidence/round36/c2-count.py --seed 36311 --receipt <art>/rec/c2-s36311.json   # rc=0
```

Seeds 36301/36311 are fresh (not 36001/36011/36021). All four receipts carry `gate_sha256=a7d3922c…` (landed). Key per-scenario evidence: S13 `baseline_echo=false`, `drift_out="GATE_DRIFT: none"`, `stderr_tail` shows the echo printed to the pin's stderr; S14 `drift_out="GATE_DRIFT: -GATE_GREP"`, `drift_rc=1`; S11 `manifest_ok=true` with `true_gate_sha` = landed; S12 C-locale observation identical to UTF-8. C2 battery: V1-V5 `output=9/9 witness=fail` with per-record attrib <9, V6 renamed `witness=pass attrib=9` — separation without false kill. Kill-rule checks: no committed run is lower (base gate 10/14 and 2/5 are the committed "before"), scored gate sha equals receipt sha, fixtures not weakened (counters run unmodified; sha256 below).

### F3 MEETS-adjacent, by design — baseline records zero engine identity

Pin under a distinct-path output-equivalent override, drift under the default engine:

```
printf '#!/bin/bash\nexec /usr/bin/grep "$@"\n' > gwrap && chmod +x gwrap
RESEARCH_GATE_GREP=$PWD/gwrap bash research-gate.sh --pin base4.txt   # rc=0
env -u RESEARCH_GATE_GREP bash research-gate.sh --drift base4.txt     # rc=0, "GATE_DRIFT: none"
```

An engine swap between pin and drift is invisible to the baseline when the engines are output-equivalent. This is the declared contract — the baseline header states "behavior, not revision, is compared" (`research-gate.sh:4074`) — and identity is carried instead by the stderr echo (S6/S10) and the counter. Listed as a demonstrated limit, not a defect; it is the same call-for-show class C1's "Limits" already states.

### F4 LOW — selftest case 260 does not assert the echo prints

Case 260 (`research-gate.sh:8110-8125`) pins with `CHOUSA_GREP_PIN_ECHO=1`, drifts with `env -u`, and asserts `GATE_PIN: ok`, `GATE_DRIFT: none`, and `! grep -q '^GATE_GREP: ' base.txt` (line 8119). It never asserts the echo **was printed** during pin; deleting the echo block (lines 417-419) keeps case 260 green. The counter's S13 covers the prints-half via `stderr_tail`. Coverage gap only; no contract impact.

### F5 info — canonical capture itself rolls DRIFT, by contract

The pinned canonical run is `RESEARCH_GATE: DRIFT (sections=5 … findings=1 drift=1)` (fixture contains a by-design mismatch; observed in `attack/base.txt`). The header declares "pinning a run that itself rolls DRIFT is still a pin" (`research-gate.sh:227-229`), and the capture accepts rc 0 or 1 with exactly one `RESEARCH_GATE:` line (3928). Consistent; noted so no reader mistakes the baseline verdict for CLEAN.

## Contract answers (brief item 1)

- **Echo write fd: stderr.** `research-gate.sh:417-418`: `printf 'GATE_GREP: …' >&2`, gated on `CHOUSA_GREP_PIN_ECHO == 1`.
- **Receipt:** never written by the gate itself; receipts may capture the caller-merged stderr (counter S13's `stderr_tail` does exactly this).
- **stdout consumed by a caller:** echo never goes to stdout; `--pin` prints `GATE_PIN: ok path=… gate_sha256=…` to stdout (4082), `--drift` prints `GATE_DRIFT: …` to stdout (4140-4148 region); header promises neither mode prints a `RESEARCH_GATE:` line (546-553). Exception: under the F1 attack, `--drift` stdout gains the stray `GATE_GREP:` line.
- **JSON field: no.** The manifest writer (`research-gate.sh:3726`) emits `schema/ts/record/record_sha256/gate_sha256/sections…` only — no grep-identity field; the only `GATE_GREP` emitters in the file are the echo (418) and the drift pairing token (3952).

## R1 scrub table (brief item 2) — variables → scrubbed? → evidence

| Variable | Changes echo? | Changes drift/capture output? | Scrubbed at capture | Evidence |
|---|---|---|---|---|
| `CHOUSA_GREP_PIN_ECHO` | gates echo on/off | baseline content via inner echo | scrubbed **directly**, but re-exportable via `BASH_ENV` (F1 hole) | `research-gate.sh:3922` `-u CHOUSA_GREP_PIN_ECHO`; F1 repro |
| `BASH_ENV` | no (function import overridden by wrapper at 359; `command` avoided) | **yes — can export any var into the inner bash**, incl. the echo flag | **NOT scrubbed** | F1 repro; `env` list 3921-3922 has no `-u BASH_ENV` |
| `RESEARCH_GATE_GREP` | echo fields `path`/`source`/`version` (391-393, 418) | behavioral only (output-equivalence is the compared contract) | not scrubbed (by design; echo cannot fire in capture while the flag is scrubbed) | `research-gate.sh:391-401`; F3 demo |
| `CHOUSA_RECORD/CLAIMS/STRICT/ROOT/AGGREGATOR_ERE` | no | capture semantics | scrubbed | `research-gate.sh:3921-3922` |
| `PATH` | no — no PATH consultation for grep (398-411); probe avoids `head`/`command` (369-380) | `bash`/`sed`/`sort`/`env`/`mktemp` remain PATH-resolved (interpreter-level; residual risk, out of this contract's declared scope) | n/a (unscrubbable) | `research-gate.sh:398-411, 369-380, 3923, 3850, 3940` |
| `GREP_BIN` / `grep` made readonly by caller | refusal, not echo content | refusal exit 2 | n/a | `research-gate.sh:413-414, 359-360` |
| `TMPDIR` | no | capture fixture location only | n/a | `research-gate.sh:3900` |
| `ts`, `gate_sha256` (volatile fields) | no | masked to `<V>`; changing the declared list is itself drift | n/a (normalize) | `research-gate.sh:3846-3857, 4125, 5745-5747` |

**Named not-scrubbed variable: `BASH_ENV`** — the exact hole, with reproducing command in F1.

## Selftest cases 260/261 (brief item 3)

Landed gate, `bash tools/research-gate.sh --selftest` → rc=0, `RESEARCH_GATE_SELFTEST: PASS (261 cases, 0 skipped)`, log `logs/selftest-kept.log` (sha256 `d8b4a3e8…`):

```
ok-case  260 pin-echo-isolation           exit=0
ok-case  261 pin-drift-grep-token         exit=1
```

- Case 260 (`research-gate.sh:8112-8119`) exercises the scrub: pins with `CHOUSA_GREP_PIN_ECHO=1` (output merged `2>&1`), drifts with `env -u`, asserts `GATE_DRIFT: none` (full-string match, line 8116) and `! grep -q '^GATE_GREP: ' "$WORK/r36-pin.txt"` (line 8119) — the baseline stays echo-free even though the caller env carried the flag. Gap: does not assert the echo printed (F4).
- Case 261 (`research-gate.sh:8127-8134`) exercises the R2 token: injects a `GATE_GREP:` line after the canonical marker via `sed -i` (8129), drift must exit 1 with `GATE_DRIFT: -GATE_GREP` (8134) — pairing under its own token, not `LINE` (line-id at 3952).

## Residual risk and verification gaps

- F1's fix is not verified (read-only role; no patch applied). A patched-gate check would add `-u BASH_ENV` at 3921 and rerun the F1 matrix; I did not build that control.
- Other `BASH_ENV` re-exports (`CHOUSA_STRICT=1` etc.) reach the inner capture wholesale; they surface as honest behavioral drift, but the gate has no "capture ran under a foreign BASH_ENV" marker.
- `bash`/`sed`/`sort`/`env`/`mktemp` in the capture path are PATH-resolved; a caller-level interpreter shim is outside the pin contract's declared threat model (the caller already chose the interpreter).
- I re-derived both claims on two fresh seeds (36301, 36311); seeds 36321/36331/36341 were not consumed by this seat (other executors hold them).
- No reads of `mechanism-witness.py` internals beyond the C2 counter's use; witness honesty is RevCounterHonesty's slice.

## Artifacts (all under `.ufo/waves/round-36/w1/RevPinContract/`)

| Path | sha256 |
|---|---|
| `rec/c1-s36301.json` | `032f035d01e0be752f6dcf20b6b7714a35220147225f9305bf38d469c953fe8c` |
| `rec/c1-s36311.json` | `2ce0d51627a6bcf384275fc3ef6deee83b43b0e61751cea800d980fb8b16031c` |
| `rec/c2-s36301.json` | `eecb20e4719c98fd6797dde2dd452d64368247e7e72a8c60002fe9cb1ce93259` |
| `rec/c2-s36311.json` | `83c480fe37321d0f135f8ad3f0a9ffc8037bb17c9329adb0ad0a00515304f2c0` |
| `attack/base.txt` (F1 pin-under-BASH_ENV baseline) | `7a904b11e35934ebe0313c30d30a121f41cc3e840eab3f06ba5ae7aeeadda014` |
| `attack/base2.txt` (F1 clean pin) | `26c10a3265f60a39ca42e623f0043585b71e08e49c6563ddc42c5df234517e8a` |
| `attack/base3.txt` (BASH_ENV both sides) | `c976013d3b47d4511d2b28f94f929ce03dc391c88937f4f6a050dba1c9101233` |
| `attack/base4.txt` (F3 override pin) | `a4bcaf8fb9b3e2adb3172b61ce555f391df60600147245a2de9dc78212407502` |
| `attack/benv.sh` | `d129505340801b5ac16e77cac9585c306ba901057d72d44514331294446e5e58` |
| `attack/gwrap` | `5ba49e0f0cddc0327a521fe78d8505c8a672bc1f3667bb4289c2c0b5cd6e67ff` |
| `logs/selftest-kept.log` | `d8b4a3e8cf4481e7a30acdba088d033fe78932ec1170e226649b43a09b47705e` |
| `logs/c1-s36301.log` (full 14-scenario trace) | `1d89954f4c0c74c3580a9a53f3da35dc825f0bd3e2e8fc2be1a6a6f58d8d00f2` |
| `logs/c2-s36311.log` (full battery trace) | `7a4a21e90daac5c94b42446085f8b89ab423d2ed41af4239e1c9d3e997b5a85d` |
| `logs/c1-s36311.log`, `logs/c2-s36301.log`, `logs/pids.txt` | on disk (not enumerated; c1/c2 logs mirror the pairs above) |

Inputs hashed: `c1-count.py` `fee038d5…`, `c2-count.py` `67c33fe4…`, `argv-witness.py` `e6832e0b…` (matches receipts), `mechanism-witness.py` `9f537bfd…`. Large/unkept run debris stayed in `/tmp/hyaku/chousa-r36/w1/RevPinContract/` (same tree; kept logs cited above).

## Files opened (access date 2026-10-23)

`.ufo/waves/round-36/w1-briefs/RevPinContract.md`; `corpus/evidence/round36/claims.md`; `corpus/evidence/round36/c1-count.py` (partial, ranges); `corpus/evidence/round36/c2-count.py` (partial); `tools/research-gate.sh` ranges 222-420, 424-463, 265-301, 3836-3863, 3889-4163, 5464-5469(header cites), 8104-8143 + grep hits; receipts/logs/artifacts listed above. Quotes ≤25 words each, cited inline.
