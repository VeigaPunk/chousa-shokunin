# ScribeGateR45 — round 45 Gates row draft

Seat: `L1Chousa45.ScribeGateR45` (scribe, leaf). Item: draft the SKILL.md
`## Gates` row for round 45's three frozen counters (c1/c2/c3-count.py),
with each counter run once read-only.

## Behavior

- Read (read-only): `corpus/evidence/round45/claims.md`; the three counters'
  full docstrings/argparse (`c1-count.py`, `c2-count.py`, `c3-count.py`);
  all four committed controls in `corpus/evidence/round45/controls/`;
  SKILL.md `## Gates` section (existing rows, conventions copied from the
  `research-gate round-37/38/39 counters` rows); lane `SCORECARD.md`.
- Ran each counter exactly once from the lane root, read-only, passing no
  option that writes a receipt into the lane (c1's receipts go to its own
  `tempfile.TemporaryDirectory`; c2/c3 write nothing).
- Drafted ONE row (below), single line, exactly 8 cells, naming every listed
  file by full repo-relative path in the entry cell.
- No fetches, no network egress, no lane production edits, no git/jj
  mutations. Only file written: this report (no scratch dir was created;
  nothing to delete). No tools installed.

## Observed runs (verbatim decisive output; all read-only)

Run from `/home/vgpnk/Projects/shokunin/chousa-shokunin`:

```
$ python3 corpus/evidence/round45/c1-count.py
CASE a_empty_exits_3=FAIL
CASE b_ok_exits_0=ok
CASE c_timeout_exits_3=FAIL
CASE d_no_timeout_exits_2=FAIL
CASE e_start_timeout_s=FAIL
CASES_MATCH=1/5
C1=FAIL
$ echo $?   → 1
```

```
$ python3 corpus/evidence/round45/c2-count.py --list
UNREGISTERED_PATH corpus/evidence/round31/c1-count-v3.py
UNREGISTERED_PATH corpus/evidence/round31/c1-count.py
UNREGISTERED_PATH corpus/evidence/round31/c2-count-v3.py
UNREGISTERED_PATH corpus/evidence/round31/c2-count.py
UNREGISTERED_PATH corpus/evidence/round32/c1-count.py
UNREGISTERED_PATH corpus/evidence/round32/c2-count.py
UNREGISTERED_PATH corpus/evidence/round33/c1-count-v3.py
UNREGISTERED_PATH corpus/evidence/round33/c1-count.py
UNREGISTERED_PATH corpus/evidence/round34/c1-count-v2.py
UNREGISTERED_PATH corpus/evidence/round34/c1-count.py
UNREGISTERED_PATH corpus/evidence/round40/c1-count.py
UNREGISTERED_PATH corpus/evidence/round40/c2-count.py
UNREGISTERED_PATH corpus/evidence/round41/c1-count.py
UNREGISTERED_PATH corpus/evidence/round41/c2-count.py
UNREGISTERED_PATH corpus/evidence/round42/c1-count.py
UNREGISTERED_PATH corpus/evidence/round42/c2-count.py
UNREGISTERED_PATH corpus/evidence/round43/c1-count.py
UNREGISTERED_PATH corpus/evidence/round43/c2-count.py
UNREGISTERED_PATH corpus/evidence/round43/c3-count.py
UNREGISTERED_PATH corpus/evidence/round44/c1-count.py
UNREGISTERED_PATH corpus/evidence/round44/c2-count.py
UNREGISTERED_PATH corpus/evidence/round44/c3-count.py
UNREGISTERED_PATH corpus/evidence/round44/errata-count.py
UNREGISTERED_PATH corpus/evidence/round45/c1-count.py
UNREGISTERED_PATH corpus/evidence/round45/c2-count.py
UNREGISTERED_PATH corpus/evidence/round45/c3-count.py
UNREGISTERED_PATH tools/absent-split.py
UNREGISTERED_PATH tools/parent-lifetime.sh
UNREGISTERED_PATH tools/quarantine-check.py
ENTRY_POINTS=54
GATES_ROWS=18
REGISTERED=25/54
UNREGISTERED=29
C2=FAIL
$ echo $?   → 1
```

```
$ python3 corpus/evidence/round45/c3-count.py
ENTRIES=0/2
CITES_BOUND=0/3
QUOTES_IN_SPAN=0/4
QUOTES_IN_ENTRY=0/4
COUNTS_IN_ENTRY=0/7
CAPTURE_BOUND=0/4
COUNTS_REDERIVED=0/7
C3=FAIL
$ echo $?   → 1
```

```
$ python3 corpus/evidence/round45/c3-count.py --lane-only
ENTRIES=0/2
CITES_BOUND=0/3
QUOTES_IN_SPAN=0/4
QUOTES_IN_ENTRY=0/4
COUNTS_IN_ENTRY=0/7
CAPTURE_BOUND=skipped
COUNTS_REDERIVED=skipped
C3=FAIL
$ echo $?   → 1
```

All four runs FAIL with exit 1, exactly as expected before the work lands;
each output is byte-identical to its frozen do-nothing control. The row's
verdict map states the frozen targets (from claims.md), not these observed
pre-land values.

## The drafted row (verbatim; single line, 8 cells)

```
| `chousa round-45 counters` | gate | `python3 corpus/evidence/round45/c1-count.py` · `python3 corpus/evidence/round45/c2-count.py --list` · `python3 corpus/evidence/round45/c3-count.py` · `python3 corpus/evidence/round45/c3-count.py --lane-only` | C1 `CASES_MATCH=5/5` `C1=PASS` exit `0`; any case failed exit `1`; usage/env exit `2` · C2 `UNREGISTERED=0` `C2=PASS` exit `0`; any unregistered entry point exit `1`; no entry points exit `2` · C3 default `ENTRIES=2/2` `CITES_BOUND=3/3` `QUOTES_IN_SPAN=4/4` `QUOTES_IN_ENTRY=4/4` `COUNTS_IN_ENTRY=7/7` `CAPTURE_BOUND=4/4` `COUNTS_REDERIVED=7/7` `C3=PASS` exit `0`; `--lane-only` same first five, capture lines `skipped`, `C3=PASS` exit `0`; any count short of its target in either mode exit `1`; usage/env exit `2` | c1-control-r44-tool.txt (r44 launcher blob `79ee8f29`): `CASES_MATCH=1/5` exit 1 · c2-control-base.txt (base `d29bf47d`): `UNREGISTERED=26` exit 1; freeze tree adds this round's three counters → 29 · c3-control-do-nothing.txt: `ENTRIES=0/2` … `C3=FAIL` exit 1 · c3-control-forged-span.txt: lane-only passes (`C3=PASS` exit 0, the named blind spot); default refuses `CAPTURE_BOUND=0/4` `COUNTS_REDERIVED=0/7` exit 1 | lane commit `d82cec904bf0fb8736886b9f17be913c7807427a` (claims frozen at this commit) | read-only (c1 writes receipts to its own temp dir only) | chousa |
```

## Gates / touched surfaces

- The row above, verified: starts with `|`, count of `|` = 9 (8 cells),
  contains `exit` — satisfies C2's row rule for itself.
- Self-test cell quotes the four committed control files verbatim (their
  contents anchor the before-values above).
- No counter is superseded (no `-v2`/`-v3` variants exist in round45), so no
  successor note is needed in the verdict map.

## Findings

- C1 observed 1/5, exit 1 — byte-identical to `controls/c1-control-r44-tool.txt`:
  the committed `tools/parent-lifetime.sh` still exhibits the round-44
  launcher's behavior (the do-nothing control scored at freeze).
- C2 observed `ENTRY_POINTS=54` (base 51 + the three round45 counters),
  `UNREGISTERED=29` — exactly the freeze-tree before predicted by claims.md
  (26 at base `d29bf47d`, +3 counters).
- C3 observed `ENTRIES=0/2` in both modes — the two adopted entries are not
  yet present in the tree; matches `c3-control-do-nothing.txt`.
- Lane HEAD measured `d82cec904bf0fb8736886b9f17be913c7807427a` (the frozen
  claims commit) → pinned value.
- No claims beyond observed runs or verbatim quote from claims/controls.

## Out of scope

- This seat only drafts the row (delivered verbatim above); landing it in
  SKILL.md is the milestone's edit, not a scribe write. No production file
  was modified.

## Artifacts

- This report: `.ufo/waves/round-45/w1/ScribeGateR45.md` (lane-relative).
