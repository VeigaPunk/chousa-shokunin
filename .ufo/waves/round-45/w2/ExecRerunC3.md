# Wave 2 — ExecRerunC3 (falsify C3 targets)

Seat: leaf executor. Item attacked: round-45 C3 depth counter's two counting targets
(default and `--lane-only`) and the committed do-nothing control, as landed at lane
commit `5e8c7ad2f7b8254d83358820286e3d12ca4672d1`.

Method: measured over committed bytes only. Extracted `git archive 5e8c7ad…` →
`/tmp/chousa-r45-ExecRerunC3/tree` and `git archive d29bf47d…` →
`/tmp/chousa-r45-ExecRerunC3/base`. Ran every command inside the tree; the frozen
reading of the real (read-only) capture cache `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache`
was used only for the default mode. No fetches, no lane writes, no tool installs.

## 1. Default mode — runs in tip archive tree

Command: `python3 corpus/evidence/round45/c3-count.py` (cwd = tree root)

```
ENTRIES=2/2
CITES_BOUND=3/3
QUOTES_IN_SPAN=4/4
QUOTES_IN_ENTRY=4/4
COUNTS_IN_ENTRY=7/7
CAPTURE_BOUND=4/4
COUNTS_REDERIVED=7/7
C3=PASS
exit=0
```

Matches the frozen target line-for-line (claims.md `## C3` target block). **Target holds.**

## 2. `--lane-only --cache /nonexistent` — in tip archive tree

Command: `python3 corpus/evidence/round45/c3-count.py --lane-only --cache /nonexistent`

```
ENTRIES=2/2
CITES_BOUND=3/3
QUOTES_IN_SPAN=4/4
QUOTES_IN_ENTRY=4/4
COUNTS_IN_ENTRY=7/7
CAPTURE_BOUND=skipped
COUNTS_REDERIVED=skipped
C3=PASS
exit=0
```

Lane-only never touches the cache (c3-count.py only uses `cache` inside
`if not a.lane_only`, lines 126-131/142-146); a nonexistent cache path is accepted
and ignored. Matches the frozen `--lane-only` target. **Target holds.**

## 3. Do-nothing control (scored at freeze)

Command: `python3 corpus/evidence/round45/c3-count.py --root /tmp/chousa-r45-ExecRerunC3/base`
(tip counter vs base-tree archive d29bf47d…) → diff vs committed control:

```
$ ( … ; echo "exit=$?") > do-nothing.out
$ diff do-nothing.out corpus/evidence/round45/controls/c3-control-do-nothing.txt
CONTROL_DIFF_IDENTICAL
```

Byte-identical, including `exit=1`. Grounds: base tree has no `corpus/evidence/round45/`
directory, no `corpus/knowledge/evidence-archive-field-policy-r41.md` /
`evidence-snapshot-coverage-r40.md` (grep: no match), and its SOURCES.md carries no
S082/S083/S084 Registry rows (only the narrative "Rejected staged S082" on the round-44
line 255). So ENTRIES=0/2 … C3=FAIL is a genuine no-work baseline, not an artifact.
**Control holds.**

## 4. Independent corroboration (not counted in targets)

- Capture shas: re-derived `sha256(url)[:24]` filenames and hashed the qcache files:
  README `ce16d57277fedfd4f0e7750e.txt` → `8e1f5bff…d91989fe5` ✓; paper
  `412b146a2720ce6557268d05.txt` → `a3ff65e0…a8a7cf8f` ✓; train
  `974299ae4b5f3bdb808b36a9.txt` → `ae5eda7c…afe00f9c` ✓ — all equal the recorded
  `capture_sha256`/`cap_sha256` values (counts.json, spans.tsv).
- Non-vacuous gate: mutation copy of the tip tree with one span offset 1809→999999
  gave `CAPTURE_BOUND=3/4`, `C3=FAIL`, exit 1 — the default mode really binds spans to
  capture bytes (the committed forged-span control `c3-control-forged-span.txt` documents
  the complementary lane-only blind spot; consistent with the predicate's D1 closure).
- Side-effect check: `diff -r` of the tree after all runs vs a fresh re-extraction is
  empty — the counter wrote nothing in the tree it ran in.

## Verdict

**Holds.** Both C3 targets (default `C3=PASS` exit 0; `--lane-only` `C3=PASS` exit 0,
cache-independent) reproduce exactly as frozen at `5e8c7ad…`, and the do-nothing control
output is byte-identical to `controls/c3-control-do-nothing.txt`. No defect found in the
counter or its executed inputs; the only documented limitation is lane-only mode's
inability to see a forged span (named in the counter docstring and the forged-span
control, not a regression of this wave).

Resolvable pointers: `corpus/evidence/round45/claims.md` (`## C3` target/kill-rule
block); `corpus/evidence/round45/c3-count.py` (binding check 104-110, span capture bound
118-131, counts re-derivation 142-146, ok-thresholds 157-164); `corpus/evidence/round45/counts.json`
(capture `974299ae4b5f3bdb808b36a9.txt`, sha `ae5eda7c…`); `corpus/evidence/round45/spans.tsv`;
`corpus/SOURCES.md` lines 92-94 (S082/S083/S084 rows); `corpus/evidence/round45/controls/c3-control-do-nothing.txt`;
qcache captures `ce16d57277fedfd4f0e7750e.txt`, `412b146a2720ce6557268d05.txt`,
`974299ae4b5f3bdb808b36a9.txt`.
