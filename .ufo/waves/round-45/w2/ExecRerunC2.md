# ExecRerunC2 — C2 calibration falsification report (round 45, wave 2)

Item attacked: C2 calibration (claims.md R45-C2; frozen d82cec90) — every committed gate
entry point named in a SKILL.md Gates row; target `UNREGISTERED=0`. Measured over committed
bytes at lane tip `5e8c7ad2f7b8254d83358820286e3d12ca4672d1` (git archive), base
`d29bf47d94149a1b71581eeb0f36d9ff22d41da3`.

## 1. Tip run: `python3 corpus/evidence/round45/c2-count.py --list` (inside archive tree)
Verbatim decisive output:
```
ENTRY_POINTS=54
GATES_ROWS=30
REGISTERED=54/54
UNREGISTERED=0
C2=PASS
exit=0
```
No `UNREGISTERED_PATH` lines printed. Target `UNREGISTERED=0` holds at tip.

## 2. Reproducibility: tip counter vs base tree, diffed against c2-control-base.txt
`python3 corpus/evidence/round45/c2-count.py --root /tmp/chousa-r45-ExecRerunC2/base --list`
verbatim:
```
ENTRY_POINTS=51
GATES_ROWS=18
REGISTERED=25/51
UNREGISTERED=26
C2=FAIL
exit=1
```
`diff -u controls/c2-control-base.txt base-run-list.txt` → identical to the control except
(1) the control's provenance header line `## base d29bf47… (git archive), counter from the
freeze tree` — not script output, added by the control generator; (2) the trailing `exit=1`
line — appended by the runner, not printed by the script. All 26 `UNREGISTERED_PATH` lines,
`ENTRY_POINTS=51`, `GATES_ROWS=18`, `REGISTERED=25/51`, `UNREGISTERED=26`, `C2=FAIL` match
byte-for-byte. Counter blob identical at freeze and tip: `git rev-parse
<commit>:corpus/evidence/round45/c2-count.py` = `1506bdb855688bafc0d2b473a014446bf4d9d5b5`
for both d82cec90 and 5e8c7ad (missing at base d29bf47 — round 45 didn't exist yet). Base
control is reproducible from committed bytes.

## 3. Independent enumeration (own find, not the counter)
`find tools -maxdepth 1 -type f | sort` → 7 files: `absent-split.py`, `argv-witness.py`,
`mechanism-witness.py`, `parent-lifetime.sh`, `quarantine-check.py`, `quote-reopen.py`,
`research-gate.sh`.
`find corpus/evidence/round* -maxdepth 1 -type f \( -name 'c*-count*.py' -o -name
'verify-receipts.py' -o -name 'errata-count.py' \) | sort` → 47 files (rounds 29–45;
includes round-45's own c1/c2/c3-count.py, rounds 38/39 verify-receipts.py, round-44
errata-count.py).
Total 54 = `ENTRY_POINTS=54`; set equality vs counter's `entry_points()` verified
programmatically (`set(mine) ^ set(find_all) == set()`).

Independent reimplementation of the predicate (own parser: `## Gates` section, rows starting
`|` with ≥ 8 separators containing `exit`; registration = literal repo-relative path
substring in a row) yields the same numbers: tip GATES_ROWS=30, UNREGISTERED=0; base
ENTRY_POINTS=51, UNREGISTERED=26. No substring-collision can fake a registration: every path
ends in `.py`/`.sh` and round dirs are 2-digit, so no path is a proper substring of another
entry point (e.g. `round31/c1-count.py` is not a substring of `round31/c1-count-v3.py`).

## 4. The twelve added Gates rows (base 18 → tip 30, +12, none removed)
Diff of Gates rows base→tip names exactly: round-31 counters; round-32 v1 counters; round-33
C1 v1/v3; round-34 v1/v2; round-40; round-41; quarantine-check r42; absent-split r43;
round-44 counters; round-45 counters; parent-lifetime; tag-count — matching the claim's
enumeration (rounds 31–34 v1/v2/v3, 40, 41, r42, r43, 44, 45, parent-lifetime, tag-count).
Each added row names real committed entry points (all 54 registered overall).

## Verdict
**C2 HOLDs** at 5e8c7ad: `UNREGISTERED=0`, `C2=PASS`, exit 0, measured over committed bytes;
counter reproducible against the base control; independent enumeration agrees (54/54 both
counts and set); no defect found in the wave-1/L1 landing on this predicate as frozen. The
only differences from the control file are its provenance header and the shell-appended exit
trailer, which are not counter output.

Commands run (all in `/tmp/chousa-r45-ExecRerunC2/{tree,tree-list,tree-root}` clones):
`git archive 5e8c7ad… | tar -x`, `git archive d29bf47… | tar -x`, `c2-count.py --list`,
`c2-count.py --root <base> --list`, `diff -u controls/c2-control-base.txt <run>`, `find`
enumerations, `git rev-parse <commit>:…c2-count.py`, python reimplementation. No network, no
lane writes, no tools installed.
