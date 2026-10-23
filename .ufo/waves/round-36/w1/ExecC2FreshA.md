# C2 fresh-seed result — ExecC2FreshA

**Access date:** 2026-10-23  
**Verdict:** **PASS for fresh seed 36301; no MEETS counterexample in the assigned C2 battery.** This is one seed only; by itself it does not establish frozen P2's two-fresh-seed condition. C1 was outside this assignment.

## Measurement

Executed the counter against the landed gate and witness with seed 36301. The recorded command was:

```sh
mkdir -p /tmp/hyaku/chousa-r36/w1/ExecC2FreshA /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecC2FreshA && cd /home/vgpnk/Projects/shokunin/chousa-shokunin && export C1_TMP=/tmp/hyaku/chousa-r36/w1/ExecC2FreshA C2_TMP=/tmp/hyaku/chousa-r36/w1/ExecC2FreshA WITNESS_TMP=/tmp/hyaku/chousa-r36/w1/ExecC2FreshA TMPDIR=/tmp/hyaku/chousa-r36/w1/ExecC2FreshA && start=$(date +%s) && timeout 1800 python3 corpus/evidence/round36/c2-count.py --gate tools/research-gate.sh --witness tools/argv-witness.py --seed 36301 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecC2FreshA/c2-after-s36301.json > /tmp/hyaku/chousa-r36/w1/ExecC2FreshA/c2.stdout 2> /tmp/hyaku/chousa-r36/w1/ExecC2FreshA/c2.stderr; rc=$?; elapsed=$(( $(date +%s) - start )); printf 'COMMAND_EXIT=%s ELAPSED_SECONDS=%s\n' "$rc" "$elapsed"; exit 0
```

**Exit:** counter exit 0; wrapper reported `COMMAND_EXIT=0 ELAPSED_SECONDS=14`; receipt `elapsed_s=14.56`. **Stderr:** empty. Deciding stdout line: `WITNESS_PER_RECORD=5/5 OUTPUT_EQUIV=5/5 LANDED_ATTRIB=pass RENAMED=pass`.

Receipt fields: `seed=36301`, `predicate_holds=true`, `matched=5`, `output_equiv=5`, `landed_attrib=pass`, `renamed=pass`; landed witness `pass`, `output_full=true`, `output_match=9/9`, `unattributed=[]`, `matcher_calls=11`. Gate SHA-256 is `a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8`; witness SHA-256 is `e6832e0b9cbbdfae9da823528cc0a6218a6af7d8ed7e5864378713df2e19107e`.

| Variant | Witness | Output match / total | Attributed records |
|---|---|---:|---:|
| V1-python-exact | fail | 9/9 | 1 |
| V2-env-keyed | fail | 9/9 | 1 |
| V3-witness-forge | fail | 9/9 | 1 |
| V4-one-call-for-show | fail | 9/9 | 2 |
| V5-body-replaced | fail | 9/9 | 1 |
| V6-renamed-matcher | pass | 9/9 | 9 |

All five challenged variants remained output-equivalent and were separated; the renamed control remained output-equivalent and passed. No assigned-fixture bypass was observed.

## Source identity

`git rev-parse master` returned `700bd5fcbf9abc118a6a0f078d51a2e7460c2878`. Working-file and `master`-blob hashes matched for all three inputs: `tools/research-gate.sh` (`a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8`), `corpus/evidence/round36/c2-count.py` (`3c699aab0614fff78f88d1b8570166439014a360ee378c0a143bf204a96e4362`), and `tools/argv-witness.py` (`e6832e0b9cbbdfae9da823528cc0a6218a6af7d8ed7e5864378713df2e19107e`).

## Commands and evidence

The source identity check was run as:

```sh
timeout 900 bash -lc 'cd /home/vgpnk/Projects/shokunin/chousa-shokunin && printf "master=" && git rev-parse master && printf "working hashes:\n" && sha256sum tools/research-gate.sh corpus/evidence/round36/c2-count.py tools/argv-witness.py && printf "master hashes:\n" && for f in tools/research-gate.sh corpus/evidence/round36/c2-count.py tools/argv-witness.py; do git show "master:$f" | sha256sum; done'
```

It completed successfully (exit 0) and printed the revision and matching hashes above. Artifact hashing commands, each successful (exit 0), were:

```sh
timeout 900 sha256sum /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecC2FreshA/c2-after-s36301.json /tmp/hyaku/chousa-r36/w1/ExecC2FreshA/c2.stdout /tmp/hyaku/chousa-r36/w1/ExecC2FreshA/c2.stderr
timeout 900 sha256sum /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecC2FreshA/c2-after-s36301.json /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecC2FreshA/c2.stdout /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecC2FreshA/c2.stderr
timeout 900 rm -- /tmp/hyaku/chousa-r36/w1/ExecC2FreshA/c2.stdout /tmp/hyaku/chousa-r36/w1/ExecC2FreshA/c2.stderr
```

The receipt and retained stdout/stderr artifacts (all under this executor's assigned directory, each below 1 MiB):

- `.ufo/waves/round-36/w1/ExecC2FreshA/c2-after-s36301.json` — `14fcd717c777f123d1d59cde267ad98f7780ccac8fe07740a8382a8ef770cef9`
- `.ufo/waves/round-36/w1/ExecC2FreshA/c2.stdout` — `7a4a21e90daac5c94b42446085f8b89ab423d2ed41af4239e1c9d3e997b5a85d`
- `.ufo/waves/round-36/w1/ExecC2FreshA/c2.stderr` (empty) — `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`

## Opened files

All accessed on 2026-10-23: `skill://godspeed` (`/home/vgpnk/.agents/skills/godspeed/SKILL.md`); `/home/vgpnk/.omp/agent/RULES.md`; `.ufo/waves/round-36/w1-briefs/ExecC2FreshA.md`; `corpus/evidence/round36/claims.md`; `corpus/evidence/round36/c1-count.py`; `corpus/evidence/round36/c2-count.py`; `tools/argv-witness.py`; `tools/mechanism-witness.py`; `.ufo/waves/round-36/measure/c2-after-s36001.json`; `.ufo/waves/round-36/measure/c2-after-s36011.json`; and this run's `c2-after-s36301.json`, `c2.stdout`, and `c2.stderr`. The `.ufo/waves/round-36/measure/` directory was listed. Hashes were computed from the working files and corresponding `master` blobs for the gate, C2 counter, and argv witness as documented above.

## Risk / blocker

No blocker. Frozen-claim limit remains: attribution proves matcher calls were made for each record, not that results were used; an output-equivalent engine that makes the calls but ignores their answers can evade this witness. This run does not test that stated out-of-scope behavior.
