# Wave 2 review: absent-split Gates row (round 43)

Seat: RevRowAbsentSplit. Item: the SKILL.md `## Gates` row whose name cell is
`` `absent-split` (round 43) `` at commit
`5e8c7ad2f7b8254d83358820286e3d12ca4672d1`.

Measured inside the archive tree
`/tmp/chousa-r45-RevRowAbsentSplit/tree` (git archive of 5e8c7ad…, extracted
`2026-10-25`). No lane, fleet or shokuknow writes; no network.

## Row shape

Raw row has exactly **8 cells** (name, kind, entry, verdict map, self-test,
pinned values, write scope, owner), matching the header `| name | kind |
entry | verdict map | self-test | pinned values | write scope | owner |`:
starts with `|`, carries 8 `|` separators, contains `exit`. **Holds.**

## Cell-by-cell

### name — `` `absent-split` (round 43) `` — holds
Row exists at SKILL.md line 107 of the committed tree; name matches the
assignment.

### kind — `tool` — holds
Entry names one tool plus three counters; consistent with kind `tool`.

### entry — holds
Commands named:
- `python3 tools/absent-split.py`
- `python3 corpus/evidence/round43/c1-count.py`
- `python3 corpus/evidence/round43/c2-count.py`
- `python3 corpus/evidence/round43/c3-count.py`

All four exist at 5e8c7ad… (`tools/absent-split.py`, all three counters).
**Holds.**

### verdict map — holds
Row text: `tool exit `0` with both classes nonempty and all absent rows
classified; `1` missing row/empty class/uncomputable ratio; `2` usage/env. C1
exit `0`: `ABSENT_ENUMERATED=15/15 CLASSED=15/15 BOTH_NONEMPTY=1/1
REPRODUCIBLE=1/1 MUTANT_DETECTED=1/1 C1=PASS`; exit `1` any count miss; `2`
usage/env. C2 exit `0`: `SPLIT_AGREES=15/15 VOCAB_OK=15/15 C2=PASS`; exit `1`
miss; `2` usage/env. C3 exit `0`: `ENTRY_CITES=1/1 QUOTE_LOCATED=1/1
URL_MATCH=1/1 C3=PASS`; exit `1` miss; `2` usage/env`.

Observed (verbatim, inside archive tree):

`python3 tools/absent-split.py`:
```
S080	not-carried	19	50	0.380000	1
S082	not-carried	18	43	0.418605	1
S084	misquote	48	90	0.533333	2
S086	not-carried	4	46	0.086957	2
S088	not-carried	26	94	0.276596	1
S093	misquote	79	120	0.658333	1
S094	misquote	63	86	0.732558	3
S104	not-carried	25	88	0.284091	1
S105	misquote	17	24	0.708333	3
S108	misquote	69	108	0.638889	1
S110	misquote	72	119	0.605042	3
S111	misquote	10	19	0.526316	1
S112	misquote	40	71	0.563380	3
S114	not-carried	7	32	0.218750	2
S116	misquote	34	36	0.944444	3
EXIT=0
```
15 rows; both classes nonempty (misquote 9, not-carried 6); exit 0.

`python3 corpus/evidence/round43/c1-count.py`:
```
TABLE_ABSENT PASS 15/15
TOOL_EXIT PASS exit=0
ABSENT_ENUMERATED PASS 15/15
CLASSED PASS 15/15
BOTH_NONEMPTY PASS misquote=9 not-carried=6
REPRODUCIBLE PASS identical=True
MUTANT_DETECTED PASS short=14 expected=15
ABSENT_ENUMERATED=15/15
CLASSED=15/15
BOTH_NONEMPTY=1/1
REPRODUCIBLE=1/1
MUTANT_DETECTED=1/1
C1=PASS
EXIT=0
```

`python3 corpus/evidence/round43/c2-count.py`:
```
SPLIT_AGREES=15/15
VOCAB_OK=15/15
MISMATCHES=0
C2=PASS
EXIT=0
```

`python3 corpus/evidence/round43/c3-count.py`:
```
ENTRY_CITES=1/1
QUOTE_LOCATED=1/1
URL_MATCH=1/1
C3=PASS
EXIT=0
```

All exit codes and all counts match the verdict map exactly. **Holds.**

### self-test — holds
Row text: `flipped-row C2 control `--flip S086` → `SPLIT_AGREES=14/15`,
exit 1; C1 missing-tool control and C3 missing-entry control also exit 1
(`corpus/evidence/round43/controls/c1-control-before.txt`,
`c3-control-before.txt`)`.

Observed:
- `python3 corpus/evidence/round43/c2-count.py --flip S086`:
  ```
  SPLIT_AGREES=14/15
  VOCAB_OK=15/15
  MISMATCHES=1
  MISMATCH S086 table=misquote independent=not-carried
  C2=FAIL
  EXIT=1
  ```
  Matches `SPLIT_AGREES=14/15`, exit 1.
- `python3 corpus/evidence/round43/c1-count.py --tool /tmp/no-such-absent-split.py`:
  ```
  TABLE_ABSENT PASS 15/15
  TOOL_PRESENT FAIL missing /tmp/no-such-absent-split.py
  C1=FAIL
  EXIT=1
  ```
  Exit 1; identical to committed `controls/c1-control-before.txt`.
- `python3 corpus/evidence/round43/c3-count.py --entry /tmp/no-such-entry.md`:
  ```
  ENTRY_CITES=0/1
  QUOTE_LOCATED=0/1
  URL_MATCH=0/1
  C3=FAIL entry-missing
  EXIT=1
  ```
  Exit 1; identical to committed `controls/c3-control-before.txt`.

Both cited control paths exist at 5e8c7ad…; `c2-control-before.txt` also
exists and matches the `--flip S086` output. **Holds.**

### pinned values — holds
Row text: `measured lane HEAD `d82cec904bf0fb8736886b9f17be913c7807427a`;
claims frozen base `15f9f3fbd3c17b2155f718c67cbef0624034cf6d``.

Both objects exist in the lane repo: `git cat-file -t` → `commit` for each;
`git merge-base --is-ancestor d82cec904… 5e8c7ad…` exits 0 (pinned HEAD is an
ancestor of the measured commit). `corpus/evidence/round43/claims.md` line 6
declares `base: 15f9f3fbd3c17b2155f718c67cbef0624034cf6d`, matching the row.
**Holds.**

### write scope — `read-only` — holds
Counters read committed inputs plus the read-only on-disk capture cache under
`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/` (absent-defect-
register.md, .qcache); source inspection shows no writes by any of the four
commands. **Holds.**

### owner — `chousa` — holds.

## Verdict

**Holds.** No defect found in any of the 8 cells; every entry command, every
self-test control, and the pinned values reproduce exactly as the row states
at 5e8c7ad2f7b8254d83358820286e3d12ca4672d1. Residual note: c2/c3 rely on the
host-local read-only shokuknow cache (matching the claims' disclosed capture
design); not counted as a defect since the row and claims declare it.
