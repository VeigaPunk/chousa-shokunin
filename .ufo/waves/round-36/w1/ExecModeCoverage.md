# R6 pin-coverage ledger measurement

Access date: 2026-10-23. Scope: the validated ExecModeCoverage brief, measuring `verify-integrity` and `verify-sweeps` only. No production file was modified.

## Axes

- **Correctness:** whether the gate accepts the fixtures and reports the expected clean tallies.
- **Pin coverage:** whether either mode sends a matcher invocation through the configured `RESEARCH_GATE_GREP` recorder.
- **Evidence quality:** gate identity, exact invocations, exits, and retained logs.

## Verdict

**TRUE for both measured landed-gate invocations:** `verify-integrity` and `verify-sweeps` each made **one total recorder call**, solely `['--version']` for the pin's GNU-provenance probe; each made **zero matcher grep calls**. Both gate invocations exited 0 and reported CLEAN on their fixture. Thus the one recorder call is not matcher coverage.

The tested gate was lane `master` tip `700bd5fcbf9abc118a6a0f078d51a2e7460c2878`; `tools/research-gate.sh` SHA-256 was `a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8` (the expected landed hash).

## Ledger and source evidence

- Frozen R6 text: `corpus/evidence/round36/claims.md:146-147` says: “R6 pin-coverage ledger: verify-integrity and verify-sweeps run no matcher grep and are not pin coverage (erratum 12); named in SKILL.md.” (21 words; accessed 2026-10-23.)
- The corresponding SKILL ledger rows are `SKILL.md:82` (`verify-sweeps`) and `SKILL.md:83` (`verify-integrity`). Their stated scopes are “opens the local path/glob sets sweeps name only” and “reads the record's own cells only”; neither row explicitly says “no matcher grep” or “not pin coverage.” (Accessed 2026-10-23.)
- The gate comment at `tools/research-gate.sh:332-347` says the matcher uses grep and that “every grep call in this shell runs that absolute path through the wrapper below.” `grep_pin_verify` invokes the candidate with `--version` (`:369-385`), and `grep_pin_init` is called before mode dispatch (`:8208`). This explains the one recorder call per run.
- Mode bodies: `tools/research-gate.sh:2619-2799` (`verify_sweeps`) and `:2877-2988` (`verify_integrity`). The executed clean-fixture outputs decide that both modes ran successfully; the recorder logs decide whether pinned matcher calls occurred.
- The C1 counter defines a matcher-shaped argv as including `-a -z -b -o -P` (`corpus/evidence/round36/c1-count.py:291-304`). The only recorded argv in either run was `--version`, so it cannot be a matcher invocation.

## Required per-mode measurements

### `verify-integrity`

Command (the complete shell command used to preserve output and report the gate status):

```sh
set +e; timeout 900 env RESEARCH_GATE_GREP=/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecModeCoverage/grep-recorder-integrity bash tools/research-gate.sh verify-integrity corpus/fixtures/integrity-r7.md --root . > /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecModeCoverage/verify-integrity.log 2>&1; rc=$?; printf 'COMMAND_EXIT=%s\n' "$rc"; timeout 10 cat /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecModeCoverage/verify-integrity.log; exit "$rc"
```

- Exit: **0** (`COMMAND_EXIT=0`; gate exit 0).
- Recorder: **1 total**, argv `['--version']`; **0 matcher calls**. The recorder log is `.../ExecModeCoverage/grep-recorder-integrity.calls`.
- Decisive output: `verify-integrity.log:18-19` — `INTEGRITY refs=16 resolved=15 unresolved=0`; `RESEARCH_GATE: CLEAN (refs=16 resolved=15 unresolved=0 exempt=1 findings=0 drift=0)`.
- Verdict: **TRUE — no matcher grep; the only call is the version probe.**

### `verify-sweeps`

Command (the complete shell command used to preserve output and report the gate status):

```sh
set +e; timeout 900 env RESEARCH_GATE_GREP=/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecModeCoverage/grep-recorder-sweeps bash tools/research-gate.sh verify-sweeps corpus/fixtures/sweeps-r5.md --root . > /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecModeCoverage/verify-sweeps.log 2>&1; rc=$?; printf 'COMMAND_EXIT=%s\n' "$rc"; timeout 10 cat /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecModeCoverage/verify-sweeps.log; exit "$rc"
```

- Exit: **0** (`COMMAND_EXIT=0`; gate exit 0).
- Recorder: **1 total**, argv `['--version']`; **0 matcher calls**. The recorder log is `.../ExecModeCoverage/grep-recorder-sweeps.calls`.
- Decisive output: `verify-sweeps.log:7-8` — `VERIFIED_SWEEPS=1/2 REJECTIONS_OK=3/3`; `RESEARCH_GATE: CLEAN (sweeps=2 verified=1 exempt=1 hit=0 refused=0 invalid=0 rejections=3 rejections-ok=3 findings=0 drift=0)`.
- Verdict: **TRUE — no matcher grep; the only call is the version probe.**

The recorder route was available; both overrides were accepted and the modes reached normal CLEAN output. `CHOUSA_GREP_PIN_ECHO=1` was not needed. The counts cover invocations routed through `RESEARCH_GATE_GREP`, not unrelated host processes.

## Commands and exit codes

All shell commands below were run with the shown timeouts; each returned exit 0 unless noted. The deciding mode-output lines and recorder counts are cited above.

1. `timeout 10 git -C /home/vgpnk/Projects/shokunin/chousa-shokunin rev-parse master && timeout 10 sha256sum /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh` — exit **0**; output was the tip and landed gate hash recorded above.
2. `timeout 10 mkdir -p /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecModeCoverage` — exit **0**; created only the exclusive evidence directory.
3. The two full mode commands above — exit **0** each; `COMMAND_EXIT=0` and the cited CLEAN summary lines decide the gate results.
4. `timeout 10 python3 -c 'import sys; d=open(sys.argv[1],"rb").read(); calls=[[x.decode("utf-8","replace") for x in p.split(b"\n",1)[0].split(b"\0") if x] for p in d.split(b"CALL\n")[1:]]; req={"-a","-z","-b","-o","-P"}; m=[a for a in calls if req.issubset(set(a)) and any(not x.startswith("-") for x in a)]; print("RECORDER_CALLS=%d"%len(calls)); [print("CALL%d=%r"%(i+1,a)) for i,a in enumerate(calls)]; print("MATCHER_CALLS=%d"%len(m))' /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecModeCoverage/grep-recorder-integrity.calls` — exit **0**; `RECORDER_CALLS=1`, `CALL1=['--version']`, `MATCHER_CALLS=0`.
5. The same count command with `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecModeCoverage/grep-recorder-sweeps.calls` as its final argument — exit **0**; identical counts and argv.
6. `timeout 10 sha256sum /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecModeCoverage/grep-recorder-integrity /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecModeCoverage/grep-recorder-integrity.calls /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecModeCoverage/verify-integrity.log /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecModeCoverage/grep-recorder-sweeps /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecModeCoverage/grep-recorder-sweeps.calls /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecModeCoverage/verify-sweeps.log && timeout 10 stat -c '%n %s bytes' /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecModeCoverage/*` — exit **0**; hashes and sizes are below (all under 1 MiB).

Repository source searches used the specialized search tool (not shell processes, so no process exit code applies): `verify-integrity|verify-sweeps|RESEARCH_GATE_GREP|pin coverage` in `tools/research-gate.sh`; `verify-integrity|verify-sweeps|pin coverage|matcher grep` and `pin.*coverage|coverage.*pin|matcher|matcher.*grep|no.*grep` in `SKILL.md`; `grep_pin_init|grep_pin_define|MODE=|verify_sweeps|verify_integrity` in `tools/research-gate.sh`.

## Artifacts and SHA-256

All files are under `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecModeCoverage/`; sizes observed were 16–1,625 bytes.

- `grep-recorder-integrity` — `5f66d5f714b0244371a34805a0d0481e568e502c132140542fdab871ebff503a`
- `grep-recorder-integrity.calls` — `075d11ce0cc52888782533058791f3c523682463fea456c9a46ed7c0a1f441c2`
- `verify-integrity.log` — `b6fbae10f7d93bd73c0827527d4bf2150035086652b4dc3e9c356150b09b5c41`
- `grep-recorder-sweeps` — `5f66d5f714b0244371a34805a0d0481e568e502c132140542fdab871ebff503a`
- `grep-recorder-sweeps.calls` — `075d11ce0cc52888782533058791f3c523682463fea456c9a46ed7c0a1f441c2`
- `verify-sweeps.log` — `4b4c484331a859cc5c745a6cba11b1076af1c649a7b296782b9c87682a402160`

## Files accessed (2026-10-23)

- `/home/vgpnk/.agents/skills/godspeed/SKILL.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1-briefs/ExecModeCoverage.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round36/claims.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round36/c1-count.py`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round36/c2-count.py`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/argv-witness.py`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/mechanism-witness.py`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/SKILL.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/fixtures/integrity-r7.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/fixtures/sweeps-r5.md`
- The six evidence artifacts listed above (the two output logs and the integrity recorder were also read directly; both call logs were parsed).

## Risks and blockers

No blocker. The SKILL mode rows identify these verifiers but do not themselves make the no-matcher assertion explicit; the frozen R6 claim and the recorder measurement supply it. Counts are specifically for these two landed-gate invocations on the named small fixtures; the total of one includes the provenance probe, so reporting “zero total calls” would be incorrect. No builds, tests, linters, or formatters were run.
