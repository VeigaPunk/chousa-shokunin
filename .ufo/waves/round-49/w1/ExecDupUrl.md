# Round 49 W1 — duplicate staged URL probe

Scope: duplicate-URL edge for frozen C1 adopter. No production files changed; no tools installed or updated.

## Commands and observed output

Scratch fixture: `/tmp/chousa-r49-ExecDupUrl/fixture` (removed after probe). It contained two cited staged rows S003/S004 with the identical, registry-absent URL `https://dup.example.com/doc/paper.pdf`, one entry citing both, and a registry with S001/S002 under `## Registry`.

Command executed by the probe:

```sh
python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/assimilate-rows.py \
  --staged /tmp/chousa-r49-ExecDupUrl/fixture/staged.md \
  --knowledge /tmp/chousa-r49-ExecDupUrl/fixture/knowledge \
  --registry /tmp/chousa-r49-ExecDupUrl/fixture/registry.md \
  --opened 2026-10-25 --out /tmp/chousa-r49-ExecDupUrl/fixture/out \
  --entry corpus/knowledge/entry.md
```

Observed tool output:

```text
TOOL_RC 0 STDOUT COLLISIONS=0 | CITED=2 APPEND=1 HELD=1 STDERR
S003 S003 append dup.example.com/doc/paper.pdf
S004 S003 held dup.example.com/doc/paper.pdf
```

The rewritten entry cited S003 for both original S003 and S004 citations. `append.md` contained one row.

Frozen `c1-count.py` `check_set()` logic (opened lines 213–222) builds `base_urls` only from registry rows, then handles each cited staged id independently: if URL is absent from `base_urls`, assign next id and `append`; it does not add that URL to `base_urls` or deduplicate against another staged row. Reproduced expectation and comparison:

```text
COUNTER_WANT {'S003': ('S003', 'append'), 'S004': ('S004', 'append')}
TOOL_GOT {'S003': ('S003', 'append'), 'S004': ('S003', 'held')}
BY_DOC 1 of 2 -> FAIL
N_APPEND_WANT 2 APPEND_ROWS_TOOL 1 -> DIFFER
```

**Result:** frozen counter and adopter disagree on this duplicate-URL edge. Tool emits second staged id as held to the first appended lane id; counter expects a distinct appended lane id.

Package scan of `/home/vgpnk/Projects/shokuknow/merge/chousa/SOURCES.append.md` found 114 parsed staged rows and 10 duplicate-URL groups overall:

```text
['S097', 'S120']
['S124', 'S135', 'S180', 'S187']
['S163', 'S172']
['S144', 'S177', 'S190']
['S185', 'S195']
['S164', 'S182']
['S129', 'S138']
['S111', 'S133', 'S181']
['S119', 'S141']
['S156', 'S169']
```

Using frozen `SETS` from `c1-count.py` lines 61–65 and staged citations in each package entry:

```text
SET A CITED ['S087', 'S088', 'S089', 'S091', 'S092', 'S100', 'S101', 'S102', 'S103'] DUP_PAIRS []
SET B CITED ['S082', 'S083', 'S090'] DUP_PAIRS []
SET C CITED ['S097', 'S114', 'S130', 'S131', 'S133'] DUP_PAIRS []
```

No frozen set contains a cited duplicate-URL pair. Thus this measured edge fails the counter’s per-document expectation but is not exercised by any frozen A/B/C set.

Scratch cleanup observed: `SCRATCH_REMOVED True`. No checks beyond the stated probe and package scan were run.

VERDICT: Built and ran a duplicate-URL C1 edge fixture; adopter and frozen counter disagree, while none of frozen sets A/B/C contains such a pair.
