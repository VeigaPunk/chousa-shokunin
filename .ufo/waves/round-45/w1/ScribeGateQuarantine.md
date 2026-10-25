# ScribeGateQuarantine — round 45 wave 1: Gates-row draft for `tools/quarantine-check.py` (round 42)

Seat: `L1Chousa45.ScribeGateQuarantine` (scribe; leaf — no subagents, no dispatch).
Item: draft the SKILL.md Gates row for the round-42 quarantine gate (`tools/quarantine-check.py`,
subcommands slice/examine/verdict/digests, plus its two frozen counters), one 8-cell line,
verdict map from observed counter runs, control in self-test, commit/receipt in pinned values.
Report only; no lane edits (SKILL.md untouched — this seat writes only this file).

## What was read (all on-disk, read-only)

- `tools/quarantine-check.py` (docstring 2–30, argparse/main 392–417): contract —
  slice = re-derive from the read-only register; examine = examine every quarantined quote;
  verdict = apply the frozen decision rule; digests = sha256 of register and consulted captures.
  Exit codes: `0` ok · `1` findings (a row could not be examined, or the slice is empty) ·
  `2` usage/env (register not readable / cache not a dir). No receipt-writing options.
- `corpus/evidence/round42/claims.md` (frozen at `dd63b6cfec5e1eafddb6662fc343e2ff6ab6aedc`,
  base `872bf3a3507875b382313f955d15960f9638256f`): C1 target `SLICE_REDERIVE_MATCH=24/24`,
  `QUOTES_EXAMINED=43/43`, `REPRODUCIBLE=1/1`, `POSITIVE_CONTROL=1/1`,
  `NEGATIVE_CONTROL=1/1`, `MUTANT_DETECTED=1/1`, exit 0; C2 target `VERDICTED=24/24`,
  `CLASS_CONSISTENT=24/24`, `REASON_NONEMPTY=24/24`, `FLIP_NONEMPTY=24/24`,
  `VOCAB_OK=24/24`, `DUPLICATE_ROWS=0`, `ROWS_OUTSIDE_SLICE=0`, exit 0.
  Do-nothing controls: C1 = tree without the tool (counter exits non-zero, receipt
  `controls/c1-control-before.txt`); C2 = one row's verdict flipped (S093 absent→present,
  `CLASS_CONSISTENT=23/24`, exit 1, receipt `controls/c2-control-before.txt`).
- `corpus/evidence/round42/c1-count.py` / `c2-count.py`: docstrings — exit `0` all counts
  hold · `1` a count failed · `2` usage/env (C1); no argv options, no `--receipt`; both
  resolve lane root via `parents[3]`, so they run from any tree and never write into the lane
  (C1 uses an internal `tempfile.TemporaryDirectory` scratch for its controls).
- `SCORECARD.md` §Round 42 verdict (lines 2302–2332): C1/C2 measured values exactly as above,
  controls named, all axes no-harm, verdict **improved**; freeze commit `dd63b6cf…`.
- `corpus/lessons/round-42.md`: adjudication summary (24 rows: 15 `absent`, 9 `unverifiable`,
  0 `present`/`mixed`); round-42 gate section (lines 86–131).

## Commands run (lane root `/home/vgpnk/Projects/shokunin/chousa-shokunin`; verbatim output, exit codes)

### 1) `python3 tools/quarantine-check.py slice | wc -l`
```
24
```
`PIPESTATUS=0 0` (tool exit 0; wc exit 0) → 24 slice rows (id, round, class, url, nquotes).

### 2) `python3 tools/quarantine-check.py verdict | cut -f1,2 | sort | uniq -c | head`
```
      1 S077	unverifiable
      1 S080	absent
      1 S082	absent
      1 S084	absent
      1 S086	absent
      1 S088	absent
      1 S093	absent
      1 S094	absent
      1 S095	unverifiable
      1 S096	unverifiable
```
`PIPESTATUS=0 0 0 0 0` (tool exit 0). Full verdict run = 24 rows, one verdict per row
(15 `absent` + 9 `unverifiable`; receipt `receipts/verdict.txt`).

### 3) `python3 corpus/evidence/round42/c1-count.py` (read-only run)
```
SLICE_REDERIVE_MATCH PASS  tool=24 independent=24
EXAMINE_RUNS         PASS  exit=0
QUOTES_EXAMINED      PASS  examined=43 expected=43
NO_SKIPPED_QUOTE     PASS  every examined quote carries a status
REPRODUCIBLE         PASS  two runs identical=True
POSITIVE_CONTROL     PASS  fold=exact strict=True
NEGATIVE_CONTROL     PASS  fold=None strict=False
MUTANT_DETECTED      PASS  mutant=23 base=24
SLICE_REDERIVE_MATCH=24/24
QUOTES_EXAMINED=43/43
REPRODUCIBLE=1/1
POSITIVE_CONTROL=1/1
NEGATIVE_CONTROL=1/1
MUTANT_DETECTED=1/1
exit=0
```
Matches committed receipt `receipts/c1-after-freeze.txt` exactly on every decisive line.

### 4) `python3 corpus/evidence/round42/c2-count.py` (read-only run)
```
VERDICTED=24/24
CLASS_CONSISTENT=24/24
REASON_NONEMPTY=24/24
FLIP_NONEMPTY=24/24
VOCAB_OK=24/24
DUPLICATE_ROWS=0
ROWS_OUTSIDE_SLICE=0
C2=PASS
exit=0
```
Matches committed receipt `receipts/c2-after.txt` exactly.

## Drafted SKILL.md Gates row (verbatim; single line, exactly 8 cells)

```
| `quarantine-check` round-42 gates | gate | `python3 tools/quarantine-check.py {slice,examine,verdict,digests}` · `python3 corpus/evidence/round42/c1-count.py` · `python3 corpus/evidence/round42/c2-count.py` (lane root; no options; read-only) | tool: exit `0` ok (`slice` 24 rows, `examine` 43 quotes, `verdict` 24 rows, `digests` register+cache sha256) · `1` findings (a row could not be examined, or the slice is empty) · `2` usage/env (register/cache missing); C1: `SLICE_REDERIVE_MATCH=24/24` `QUOTES_EXAMINED=43/43` `REPRODUCIBLE=1/1` `POSITIVE_CONTROL=1/1` `NEGATIVE_CONTROL=1/1` `MUTANT_DETECTED=1/1` exit `0` iff all hold, `1` any count failed, `2` usage/env; C2: `VERDICTED=24/24` `CLASS_CONSISTENT=24/24` `REASON_NONEMPTY=24/24` `FLIP_NONEMPTY=24/24` `VOCAB_OK=24/24` `DUPLICATE_ROWS=0` `ROWS_OUTSIDE_SLICE=0` exit `0` iff all hold, `1` otherwise, `2` usage/env; none superseded (current versions) | C1 do-nothing control (tree without the tool): `c1-count` exits 1 (`corpus/evidence/round42/controls/c1-control-before.txt`); mutant register (one lane data row dropped): 23 vs 24 rows; C2 do-nothing control (S093 flipped absent→present): `CLASS_CONSISTENT=23/24`, exit 1 (`corpus/evidence/round42/controls/c2-control-before.txt`); tool slice on an empty register exits 1 | contract `corpus/evidence/round42/claims.md` (freeze commit `dd63b6cfec5e1eafddb6662fc343e2ff6ab6aedc`, base `872bf3a3507875b382313f955d15960f9638256f`); measured receipts `corpus/evidence/round42/receipts/{c1-after-freeze,c2-after,verdict,examine,digests}.txt` | read-only (tool and counters write nothing; C1's scratch controls live in its own temp dir) | chousa |
```

## Verdict

- Row drafted per the existing Gates-table conventions (compare `research-gate round-37 counters`,
  `research-gate round-38 counters`): name | gate | full entry commands | verdict map with each
  exit code and exact PASS print values | failing control | contract/receipt pins | write scope |
  `chousa`. 8 cells, starts `| `, ends ` |`.
- All entry points named by full repo-relative path: `tools/quarantine-check.py`,
  `corpus/evidence/round42/c1-count.py`, `corpus/evidence/round42/c2-count.py`.
- Both counters are current versions — none superseded (no `-v2`/`-v3` successors exist), so no
  successor note is required in the verdict map.
- Verdict-map values are observed, not remembered: my read-only runs reproduce the committed
  receipts (`c1-after-freeze.txt`, `c2-after.txt`) line-for-line, exit 0 each.

## Pointers

- Claims/targets: `corpus/evidence/round42/claims.md:67-99` (C1/C2 targets and controls).
- Scorecard: `SCORECARD.md:2302-2332` (round-42 verdict, controls, freeze commit).
- Lesson: `corpus/lessons/round-42.md:17-32` (measured run summary), `:86-131` (gate section).
- Receipts: `corpus/evidence/round42/receipts/c1-after-freeze.txt`, `c2-after.txt`,
  `verdict.txt`, `examine.txt`, `digests.txt`; controls: `corpus/evidence/round42/controls/c1-control-before.txt`, `c2-control-before.txt`.

## Limits / notes

- Lane HEAD at measurement: `d82cec904bf0fb8736886b9f17be913c7807427a` (round-45 freeze commit);
  the round-42 tool and counters were measured on the working tree at that HEAD.
- No fetch, no network egress, no tool installs, no scratch directory created (nothing to clean);
  the only file written this seat is this report.
