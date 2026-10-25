# CritC1Harm — C1 exit-contract change, harm attack

Seat: L1Chousa45.CritC1Harm (critic, leaf; no subagents, no fetch, no lane writes except this report).
Axes: operability (C1), calibration (C2), depth (C3). Verdict: **no harm to committed counters/receipts/scripts**; two caveats (external driver invocation pattern; stale in-file docs) — both fixable, neither blocks the frozen predicate.

## Item

Attack R45-C1 for harm: `tools/parent-lifetime.sh` gaining a required `--timeout` (exit 2 when omitted in dispatch mode) and exit 3 on zero tasks / any seat timeout, plus a `timeout_s=` start-line field. Does anything commit call the tool without `--timeout`, or depend on exit 0? Do round-44's counter and committed receipts still verify? Is a `timeout_s` start line still parsed by `rootpus/evidence/round44/c1-count.py`?

## Evidence — what is in the tree

1. Lane HEAD `d82cec9` ("round-45: freeze three claims … score their controls"); `tools/parent-lifetime.sh` is **clean** at HEAD and unchanged since round 44 (sha256 `f3b0baac457710d6a210ad4e1f27e8d398f6b51c58290d8c90fea8bdca3e33cb`, 3352 bytes, mtime 2026-10-24 21:49:24). The round-44 tool is still the old contract: `[--timeout SECS]` optional, default `TIMEOUT=420` (line 20), start line `start parent_pid=… epoch=…` with no `timeout_s`, `exit 0` after the end line. The new contract exists only as the sibling probe copy `/tmp/chousa-r45-ExecLauncherPatch/parent-lifetime.sh` (sha256 `4a5a2a48…`), which passes `c1-count.py --tool …`: `CASES_MATCH=5/5`, `C1=PASS`, exit 0; selftest still `-- 0` without `--timeout` (`usage` guard is `SELFTEST -eq 0 && TIMEOUT_SET -eq 0`).
2. **No committed script, counter, or wrapper calls the tool.** `grep parent-lifetime\.sh` over the lane (and fleet root) finds only: prompt strings inside `.ufo/waves/round-44/{w1,w2,w3}-spec.json`, `w1/w2-dispatch.json`, `w1/w2-plan.json`, `make-w3-spec.py:223-226`, `seat-logs/*.prompt`; text mentions in `QUALITY.md:573-579`, round-44 reports/lessons, `l0-questions.md:148`; and the tool's own header. Every embedded invocation is `--selftest --receipt …` (no `--timeout`), which the probe patch keeps valid (exit 0, start line now carries `timeout_s=420`). No dispatch-mode invocation exists anywhere in committed code.
3. Committed receipt `corpus/evidence/round44/parent-lifetime.receipt` (130 lines, start `parent_pid=3226659`, end `n_spawned=64 n_reaped=64`) is a historical artifact; the tool change does not touch it.

## Evidence — round-44 counter still verifies (run, verbatim)

```
$ python3 corpus/evidence/round44/c1-count.py
N_SPAWNED=64/64
N_REAPED=64/64
PARENT_PID_MATCH=1/1
ZERO_PIDS=0
NAMES_MATCH=64/64
C1=PASS
EXIT=0
```

Round-44 `c1-count.py` reads the receipt file, not the tool; `parse()` (lines 27-46) tokenizes each line on whitespace and keeps `key=value` fields generically, so a start-line extension is inert.

## Evidence — `timeout_s` start line still parsed (run against a copy with ` timeout_s=5` appended to the start line, /tmp)

```
$ (first line of copy) start parent_pid=3226659 epoch=1792889279 timeout_s=5
$ python3 corpus/evidence/round44/c1-count.py --receipt /tmp/…/receipt-timeout_s.txt --names …/seat-names.txt
N_SPAWNED=64/64
N_REAPED=64/64
PARENT_PID_MATCH=1/1
ZERO_PIDS=0
NAMES_MATCH=64/64
C1=PASS
EXIT=0
```

Backward compatible: receipts written under the new contract (start line with `timeout_s=`) verify unchanged under the round-44 counter.

## Findings

1. **No committed caller breaks.** Nothing in the lane invokes dispatch mode; the only embedded invocations are selftest prompts, which the probe patch explicitly keeps working without `--timeout`. No dependence on exit-0-on-malformed in committed code (that behavior is precisely the defect QUALITY 63 and lesson mistake 4 name).
2. **External driver caveat (real, out-of-lane).** The round-44 wave driver invoked the launcher **without** `--timeout`: the round-44 report states "the launcher's default 420 s timeout (`tools/parent-lifetime.sh:20`) killed 27 of wave 3's 32 seats", and outer logs record `launcher_exit=0` for w1/w3 (`.ufo/waves/round-44/launcher-outer.log:4`, `w3-launcher-outer.log:4`). Under the new contract that exact invocation pattern exits 2 (usage) and writes no receipt. This is not a committed lane artifact, but any driver not updated to pass `--timeout` will fail to launch. Smallest safe correction: the wave driver must pass `--timeout` explicitly; the round-45 counter already does (its `run()` passes `--timeout` except in case d).
3. **Stale in-file docs (minor).** The tool's own header (lines 2-8) still documents "Exit 0 when the end line is written. Exit 1 … Exit 2 on usage" — the probe patch does not update it, so after landing the header omits exit 3 and the mandatory `--timeout`. `QUALITY.md:573-579` documents the old exit-0-on-malformed demonstration as current. Both should be updated atomically with the patch (header: add exit 3 and "dispatch mode requires --timeout"; QUALITY 63: mark the demonstration historical/round-44). Neither affects the frozen predicate.
4. **Round-44 counter and committed receipts: unaffected** (demonstrated above). `c1-control-r44-tool.txt` remains a valid frozen do-nothing control (it quotes the round-44 blob, still retrievable from git).

## Verdict

**No harm** to any committed lane script, doc (except stale wording noted), counter, or receipt under the probed change. Round-44 `c1-count.py` still passes on the committed receipt and on a `timeout_s`-augmented start line. The only real break is the external wave driver's recorded no-`--timeout` invocation pattern (exit 0 → exit 2), which the change is designed to force; it must be updated to pass `--timeout`. No predicate, counter, or target modification proposed.

Commands run (verbatim, decisive lines above): `python3 corpus/evidence/round44/c1-count.py`; `sed -e '1s/$/ timeout_s=5/' …parent-lifetime.receipt > /tmp/chousa-r45-CritC1Harm/receipt-timeout_s.txt` + `c1-count.py --receipt` on it; `git log -1 --oneline` (d82cec9), `git status --porcelain -- tools/parent-lifetime.sh` (empty), `sha256sum tools/parent-lifetime.sh` (f3b0baac…); `grep parent-lifetime\.sh` lane + fleet. Nothing installed.
