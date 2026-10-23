# Round 36 wave 1 — ExecSelftest

Date: 2026-10-23. Scope: the validated brief's three `research-gate.sh --selftest` runs only. The gate was pinned before running: SHA-256 `a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8` (the expected landed gate); `master` tip was `700bd5fcbf9abc118a6a0f078d51a2e7460c2878`.

## Runs and deciding evidence

All three test commands exited 0. Each produced the same last eight lines below, ending in `RESEARCH_GATE_SELFTEST: PASS (261 cases, 0 skipped)`; case count was 261 with 0 skipped.

| Environment | Exact test invocation | Exit | Decisive line |
|---|---|---:|---|
| Default locale | `timeout 1800 bash tools/research-gate.sh --selftest` | 0 | `RESEARCH_GATE_SELFTEST: PASS (261 cases, 0 skipped)` |
| C locale | `LC_ALL=C timeout 1800 bash tools/research-gate.sh --selftest` | 0 | `RESEARCH_GATE_SELFTEST: PASS (261 cases, 0 skipped)` |
| Scratch `TMPDIR` | `TMPDIR=/tmp/hyaku/chousa-r36/w1/ExecSelftest/tmp timeout 1800 bash tools/research-gate.sh --selftest` | 0 | `RESEARCH_GATE_SELFTEST: PASS (261 cases, 0 skipped)` |

Last eight lines, identical in all three runs:

```text
ok-case  255 claims-deadzone-line         exit=1
ok-case  256 claims-deadzone-edge         exit=1
ok-case  257 claims-locale-c              exit=0
ok-case  258 claims-locale-boundary       exit=0
ok-case  259 all-manifest-hash-shim       exit=0
ok-case  260 pin-echo-isolation           exit=0
ok-case  261 pin-drift-grep-token         exit=1
RESEARCH_GATE_SELFTEST: PASS (261 cases, 0 skipped)
```

## Commands issued and exit evidence

The following shell command strings were issued. The selftest child exit codes are recorded above and in their result artifacts; each capture wrapper completed successfully (exit 0).

```text
mkdir -p /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecSelftest /tmp/hyaku/chousa-r36/w1/ExecSelftest/tmp
```

```text
sha256sum /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh && git -C /home/vgpnk/Projects/shokunin/chousa-shokunin rev-parse master
```
Output: expected gate hash and `master` tip listed above; exit 0.

```text
set +e; timeout 1800 bash tools/research-gate.sh --selftest > /tmp/hyaku/chousa-r36/w1/ExecSelftest/normal.log 2>&1; rc=$?; { printf '%s\n' 'COMMAND: timeout 1800 bash tools/research-gate.sh --selftest'; printf 'EXIT_CODE: %s\n' "$rc"; printf '%s\n' 'LAST_8_LINES:'; tail -n 8 /tmp/hyaku/chousa-r36/w1/ExecSelftest/normal.log; } > .ufo/waves/round-36/w1/ExecSelftest/normal.result.txt; cat .ufo/waves/round-36/w1/ExecSelftest/normal.result.txt
```

```text
set +e; LC_ALL=C timeout 1800 bash tools/research-gate.sh --selftest > /tmp/hyaku/chousa-r36/w1/ExecSelftest/clocale.log 2>&1; rc=$?; { printf '%s\n' 'COMMAND: LC_ALL=C timeout 1800 bash tools/research-gate.sh --selftest'; printf 'EXIT_CODE: %s\n' "$rc"; printf '%s\n' 'LAST_8_LINES:'; tail -n 8 /tmp/hyaku/chousa-r36/w1/ExecSelftest/clocale.log; } > .ufo/waves/round-36/w1/ExecSelftest/clocale.result.txt; cat .ufo/waves/round-36/w1/ExecSelftest/clocale.result.txt
```

```text
set +e; TMPDIR=/tmp/hyaku/chousa-r36/w1/ExecSelftest/tmp timeout 1800 bash tools/research-gate.sh --selftest > /tmp/hyaku/chousa-r36/w1/ExecSelftest/tmpdir.log 2>&1; rc=$?; { printf '%s\n' 'COMMAND: TMPDIR=/tmp/hyaku/chousa-r36/w1/ExecSelftest/tmp timeout 1800 bash tools/research-gate.sh --selftest'; printf 'EXIT_CODE: %s\n' "$rc"; printf '%s\n' 'LAST_8_LINES:'; tail -n 8 /tmp/hyaku/chousa-r36/w1/ExecSelftest/tmpdir.log; } > .ufo/waves/round-36/w1/ExecSelftest/tmpdir.result.txt; cat .ufo/waves/round-36/w1/ExecSelftest/tmpdir.result.txt
```

```text
sha256sum /tmp/hyaku/chousa-r36/w1/ExecSelftest/normal.log /tmp/hyaku/chousa-r36/w1/ExecSelftest/clocale.log /tmp/hyaku/chousa-r36/w1/ExecSelftest/tmpdir.log .ufo/waves/round-36/w1/ExecSelftest/normal.result.txt .ufo/waves/round-36/w1/ExecSelftest/clocale.result.txt .ufo/waves/round-36/w1/ExecSelftest/tmpdir.result.txt && wc -c .ufo/waves/round-36/w1/ExecSelftest/normal.result.txt .ufo/waves/round-36/w1/ExecSelftest/clocale.result.txt .ufo/waves/round-36/w1/ExecSelftest/tmpdir.result.txt
```

This hash/size command exited 0. The three receipt sizes were 483, 492, and 532 bytes (all below 1 MiB). The initial `mkdir`, gate-pin/revision command, and artifact hash/size command were not wrapped in `timeout`; the three requested selftests were each bounded by `timeout 1800`.

## Retained artifacts and hashes

Receipts under the assigned artifact directory:

- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecSelftest/normal.result.txt` — SHA-256 `53b09cec243d13e1166d56b2db47325d8fe044e30aa180d8979ac4f7bdabe39d`.
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecSelftest/clocale.result.txt` — SHA-256 `966f1044b96ccc63a4565411f66ae61841c0ed5c881bd24ef80ccfd8e9649010`.
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecSelftest/tmpdir.result.txt` — SHA-256 `ff1df9d284f1b3860375e54a1bd307f9ac2f764ac7f014f35cd00c5b08315154`.

Full logs retained in scratch as allowed:

- `/tmp/hyaku/chousa-r36/w1/ExecSelftest/normal.log` — SHA-256 `d8b4a3e8cf4481e7a30acdba088d033fe78932ec1170e226649b43a09b47705e`.
- `/tmp/hyaku/chousa-r36/w1/ExecSelftest/clocale.log` — SHA-256 `d8b4a3e8cf4481e7a30acdba088d033fe78932ec1170e226649b43a09b47705e`.
- `/tmp/hyaku/chousa-r36/w1/ExecSelftest/tmpdir.log` — SHA-256 `d8b4a3e8cf4481e7a30acdba088d033fe78932ec1170e226649b43a09b47705e`.

## Files opened (access date: 2026-10-23)

- `/home/vgpnk/.agents/skills/godspeed/SKILL.md`
- `/home/vgpnk/.omp/agent/RULES.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1-briefs/ExecSelftest.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round36/claims.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round36/c1-count.py`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round36/c2-count.py`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/argv-witness.py`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/mechanism-witness.py`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh` (searched for selftest/TMPDIR code, hash-pinned, and executed read-only).
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecSelftest.md` was checked and did not exist before this report was written.

No tools were installed or updated. No production file was written; C1/C2 were not measured in this selftest-only move.

**VERDICT: no-harm holds for the assigned selftest scope — all three runs passed 261/261 with 0 skipped; no non-PASS finding or blocker.**