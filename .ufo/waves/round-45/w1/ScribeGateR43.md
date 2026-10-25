# ScribeGateR43 — draft SKILL.md Gates row for round 43 counters

Item: draft the missing Gates row for round 43's entry points
(`corpus/evidence/round43/c1-count.py`, `c2-count.py`, `c3-count.py`) in the
`## Gates` section of `SKILL.md`, copying the row conventions (e.g. the
`research-gate round-37 counters` row). Leaf seat; no dispatch; no lane
writes except this report. No tool installs needed (no install/update
record).

## Sources read

- `SKILL.md` `## Gates` section (lines 75–333; rows 79–99), including the
  `research-gate round-37 counters` row (line 95).
- `corpus/evidence/round43/claims.md` (frozen predicates, target print values,
  controls, base commit `15f9f3fbd3c17b2155f718c67cbef0624034cf6d`).
- `corpus/evidence/round43/c1-count.py` (docstring + main: exit 0/1/2, prints
  `ABSENT_ENUMERATED`/`CLASSED`/`BOTH_NONEMPTY`/`REPRODUCIBLE`/`MUTANT_DETECTED`,
  `--tool`, `--table`).
- `corpus/evidence/round43/c2-count.py` (docstring + main: `--table`,
  `--register`, `--cache`, `--flip`; prints `SPLIT_AGREES`/`VOCAB_OK`).
- `corpus/evidence/round43/c3-count.py` (full: `--entry`, `--sources`; prints
  `ENTRY_CITES`/`QUOTE_LOCATED`/`URL_MATCH`).
- `corpus/evidence/round43/receipts/{c1,c2,c3}-after.txt` and
  `corpus/evidence/round43/controls/{c1,c2,c3}-control-before.txt`.
- `corpus/lessons/round-43.md`; `SCORECARD.md` lines 2352–2363 (round-43
  verdict); `LOG.md` lines 1541–1554 (round-43 block).
- `tools/absent-split.py` (main 105–141: prints the split table to stdout,
  writes no file).

## Commands run (verbatim output, decisive lines)

All from `/home/vgpnk/Projects/shokunin/chousa-shokunin`, read-only, once.

`python3 corpus/evidence/round43/c1-count.py` → exit=0:
```
ABSENT_ENUMERATED=15/15
CLASSED=15/15
BOTH_NONEMPTY=1/1
REPRODUCIBLE=1/1
MUTANT_DETECTED=1/1
C1=PASS
```

`python3 corpus/evidence/round43/c2-count.py` → exit=0:
```
SPLIT_AGREES=15/15
VOCAB_OK=15/15
MISMATCHES=0
C2=PASS
```

`python3 corpus/evidence/round43/c3-count.py` → exit=0:
```
ENTRY_CITES=1/1
QUOTE_LOCATED=1/1
URL_MATCH=1/1
C3=PASS
```

Controls (self-test cell), all exit 1:

`python3 corpus/evidence/round43/c1-count.py --tool /tmp/no-such-absent-split.py`:
```
TOOL_PRESENT FAIL missing /tmp/no-such-absent-split.py
C1=FAIL
```

`python3 corpus/evidence/round43/c2-count.py --flip S086`:
```
SPLIT_AGREES=14/15
VOCAB_OK=15/15
MISMATCHES=1
MISMATCH S086 table=misquote independent=not-carried
C2=FAIL
```

`python3 corpus/evidence/round43/c3-count.py --entry /tmp/no-such-entry.md`:
```
ENTRY_CITES=0/1
QUOTE_LOCATED=0/1
URL_MATCH=0/1
C3=FAIL entry-missing
```

## Verdict

All three counters pass on the committed tree with exit 0; the three controls
exit 1 as claimed. All observed outputs match the frozen targets in
`corpus/evidence/round43/claims.md` and the round-43 scorecard/lesson. No
counter was superseded (no -v2/-v3 exists in the round-43 dir). Repo status
after my runs shows no round-43 file touched (only the pre-existing named
inherited modification/untracked round-45 wave files).

## Drafted Gates row (verbatim, one line, 8 cells)

```
| `research-gate round-43 counters` | gate | `python3 corpus/evidence/round43/c1-count.py` · `python3 corpus/evidence/round43/c2-count.py` · `python3 corpus/evidence/round43/c3-count.py` (lane root; c1 `--tool PATH`, `--table PATH`; c2 `--table PATH`, `--register PATH`, `--cache PATH`, `--flip ID`; c3 `--entry PATH`, `--sources PATH`) | `ABSENT_ENUMERATED=15/15 CLASSED=15/15 BOTH_NONEMPTY=1/1 REPRODUCIBLE=1/1 MUTANT_DETECTED=1/1` (C1) · `SPLIT_AGREES=15/15 VOCAB_OK=15/15` (C2) · `ENTRY_CITES=1/1 QUOTE_LOCATED=1/1 URL_MATCH=1/1` (C3), each prints `C*=PASS`; exit `0` all counts hold · `1` a count failed · `2` usage/env | C1 do-nothing (`--tool` a non-split path) → `TOOL_PRESENT FAIL` + `C1=FAIL`, exit 1; C2 flipped-row `--flip S086` → `SPLIT_AGREES=14/15 MISMATCH S086 table=misquote independent=not-carried`, exit 1; C3 missing `--entry` → `ENTRY_CITES=0/1 C3=FAIL entry-missing`, exit 1 | contract `corpus/evidence/round43/claims.md`; lane commit `737f40b` (landed), base `15f9f3f`; receipts `corpus/evidence/round43/receipts/`; controls `corpus/evidence/round43/controls/` | read-only: no counter and no executed `tools/absent-split.py` writes a file (the split table is printed to stdout); no network | chousa |
```

## Out-of-scope / findings

- Rows are also missing for the round-40/41/42 counter entry points (grep
  `round-4[012] counters|round4[012]` in `SKILL.md` → no matches). Those are
  not part of this item (round 43 only); they contribute to the round-45 C2
  29-unregistered count. No row drafted for them.
- The round-43 `receipts/c1-after.txt` etc. are the round's own after-images;
  the row's pinned-values cell cites them rather than a receipt path written by
  the counters (the counters expose no `--receipt`).
- No network egress, no production writes. Scratch: none created; nothing to
  delete.
