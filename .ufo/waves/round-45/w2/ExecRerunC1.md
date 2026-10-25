# ExecRerunC1 — wave 2 falsify report

Seat: L1Chousa45.ExecRerunC1 · lane commit measured: `5e8c7ad2f7b8254d83358820286e3d12ca4672d1`
Method: `git archive 5e8c7ad… | tar -x -C /tmp/chousa-r45-ExecRerunC1/tree`; every counter ran from inside that tree (cwd = tree). No lane writes; no fetch; r44 blob extracted locally via `git show 79ee8f2942802ee1d1771a7e5887a7a9a36cdb8b`.

## 1. C1 target `CASES_MATCH=5/5` — three runs (committed tree)

Command (x3, in tree): `python3 corpus/evidence/round45/c1-count.py`

Verbatim output, identical on all three runs (RUN1/2/3_EXIT=0 each):

```
CASE a_empty_exits_3=ok
CASE b_ok_exits_0=ok
CASE c_timeout_exits_3=ok
CASE d_no_timeout_exits_2=ok
CASE e_start_timeout_s=ok
CASES_MATCH=5/5
C1=PASS
```

Verdict: **C1 target HOLDS.** 5/5, C1=PASS, exit 0, deterministic across three runs (3.25 s total). The counter exercises the tree's `tools/parent-lifetime.sh` (TOOL = parents[3] of `__file__` = tree root), stub `kimi` prepended to PATH (`run()` sets `PATH={tmp/bin}:…`), receipts read from temp dirs; no receipts written into the tree.

## 2. r44-tool control reproduction — FAILS byte-for-byte (one trailer line)

Command (in tree): `python3 corpus/evidence/round45/c1-count.py --tool /tmp/chousa-r45-ExecRerunC1/r44.sh`

Verbatim output (TOOL_EXIT=1):

```
CASE a_empty_exits_3=FAIL
CASE b_ok_exits_0=ok
CASE c_timeout_exits_3=FAIL
CASE d_no_timeout_exits_2=FAIL
CASE e_start_timeout_s=FAIL
CASES_MATCH=1/5
C1=FAIL
```

`diff` vs committed `corpus/evidence/round45/controls/c1-control-r44-tool.txt` (tree copy; DIFF_EXIT=1):

```
7a8
> exit=1
```

sha256: run output `8bc137df4965d7f692a8dbdd21b6171c9861fc3eed779ae55406e96f3eb0d6ef`; control `08ba8735d3d4ed4c9214ad0c3afbcf34befb370a3fd132536c45f1db4790d333` (live repo copy identical: `cmp` exit 0; same bytes at freeze commit d82cec9 — verified via `git show d82cec9:…/c1-control-r44-tool.txt | sha256sum`).

Analysis: the committed control carries an 8th line `exit=1`; the committed c1-count.py never prints an exit line (grep over `c1-count.py` confirms no `print(.*exit`; exit is communicated via process status only, docstring line 18). So the naive pipeline does not reproduce the control byte-for-byte; it matches only if the harness appends the process exit code (`; echo "exit=$?"`). **Systemic**: every round-45 control ends with an `exit=1` trailer (c2-control-base.txt:33, c3-control-do-nothing.txt:9, c3-control-forged-span.txt:20, tag-control-r35-r44.txt:25) while no round-45 counter emits one. Both control and counter were authored in the same freeze commit d82cec9 and unchanged since; the mismatch is present in the frozen snapshot itself.

## 3. Verdict on C1 (claims.md:33 target)

- `CASES_MATCH=5/5` / `C1=PASS` / exit 0: **HOLDS** (3/3 runs).
- Do-nothing control semantic content (claims.md:35-37): score 1/5, case b only, C1=FAIL, exit 1 — **HOLDS** in content; its literal byte reproduction as committed **FAILS** by one appended trailer line (`exit=1`), so any byte-comparing gate must append the exit code to match the fixture. No fetch needed; no lane changes made.

## Resolvable pointers

- Counter: `corpus/evidence/round45/c1-count.py` (commit 5e8c7ad) — printing at lines 113-119, no exit trailer; exit via `return` (line 119).
- Control: `corpus/evidence/round45/controls/c1-control-r44-tool.txt` line 8 (`exit=1`) — not emitted by the counter.
- Claim: `corpus/evidence/round45/claims.md` lines 33, 35-37 (target + do-nothing control description).
- Freeze commit: d82cec904bf0fb8736886b9f17be913c7807427a (both files last touched there; sha256 of control unchanged from freeze to lane commit).
