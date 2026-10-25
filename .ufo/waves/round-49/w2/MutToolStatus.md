# MutToolStatus — close W1 survivor m8 (status-forcing probe), round 49 wave 2

2026-10-25 · lane `chousa-shokunin` · target `tools/assimilate-rows.py` (adopted tool-fix commit 4ce61fc5) · supplementary probe ordered by W2 seat: close W1 MutTool's surviving mutant m8 ("status not forced to `mined`") by direct behavioral probe on a scratch package whose cited row is `queued`; also probe opened-date and used-by forcing the same way. No frozen predicate, target or counter changed; this is evidence, not a counter edit.

## Note on tool bytes
W1 mutated the pre-fix tool (BASE_REV 414a2ec, pristine sha256 `3b8a6e7daa45dca6…`). The adopted tool at lane tip 4ce61fc5 (tab headings, calendar-valid dates, non-UTF-8 refusal) hashes `4b995dbc2e950613a632c83dba068e932396c1cf1d6a44dc1255f1c4f04abc32`; its forcing loop is `tools/assimilate-rows.py:228-231` — same mutant class present. All probes below ran against the adopted bytes.

## Setup (all under /dev/shm/chousa-r49-MutToolStatus/; /tmp full host-wide, TMPDIR exported per bounds)
- `$ cp tools/assimilate-rows.py $T/pristine.py` → sha256 `4b995dbc2e9506…` (identical to production before AND after the probe: restoration evidence, production never edited).
- Fixture `staged.md`: one 11-cell row `| S170 | https://example.org/queued-item | page | web | probe | para 1 | staged finding text | queued | 2020-01-01 | 90d | other-entry.md |` — all three forced columns differ from the forced values (`mined` / `--opened` / computed used-by).
- Fixture `registry.md`: `## Registry` with one row `S001` (URL `https://registry.example/old-row`, so S170 is `append`, lane id S002; `COLLISIONS=0`).
- `knowledge/a-entry.md`, `knowledge/b-entry.md`: both cite S170 → expected used-by `a-entry.md, b-entry.md`.
- Mutants: byte-identical copies of pristine.py with ONE tuple dropped from the `:228` loop:
  | mutant | single-point edit (line 228) | sha256 after |
  |---|---|---|
  | m8a (W1 m8 class) | drop `("status", 7, "mined"),` | `9db85396de533bac3796145462458f6bd5d97aa0e769b2e326392c7c4190e578` |
  | m8b (opened) | drop `("opened", 8, a.opened),` | `2f71d41d2197feffb3124f9ec4eeba736ed55e548a6cb8c75803b47dfbe74546` |
  | m8c (used-by) | drop `("used-by", 10, ", ".join(users))` | `69f4518d7b011dc9263c45b4f2d0e2c91648386fea1437940675c113f1ce84e8` |

## Runs (identical args for all four; `<V>` ∈ pristine, m8a, m8b, m8c)
```
$ TMPDIR=$T python3 $T/<V>.py --staged $T/staged.md --knowledge $T/knowledge \
    --registry $T/registry.md --opened 2026-10-25 --out $T/out-<V> \
    --entry a-entry.md --entry b-entry.md
COLLISIONS=0
CITED=1 APPEND=1 HELD=0
rc=0          # all four: exit 0, no REFUSED, no stderr
```

### pristine (real tool) — `$T/out-pristine/append.md`, `stripped.tsv`, `renumber.tsv` (verbatim)
```
| S002 | https://example.org/queued-item | page | web | probe | para 1 | staged finding text | mined | 2026-10-25 | 90d | a-entry.md, b-entry.md |
lane_id	column	stripped
S002	status	queued
S002	opened	2020-01-01
S002	used-by	other-entry.md
staged_id	lane_id	action	url
S170	S002	append	example.org/queued-item
```
Status forced `queued`→`mined`, opened forced `2020-01-01`→`2026-10-25`, used-by forced `other-entry.md`→`a-entry.md, b-entry.md` (sorted, both citing entries); all three old values logged in stripped.tsv. Matches doc contract `tools/assimilate-rows.py:28-35` and code `:228-231`.

### m8a — status force dropped (the W1 survivor class)
```
| S002 | … | staged finding text | queued | 2026-10-25 | 90d | a-entry.md, b-entry.md |
lane_id	column	stripped
S002	opened	2020-01-01
S002	used-by	other-entry.md
```
Appended row keeps staged `queued`; stripped.tsv has NO status line. The mutant is behaviorally distinguishable from the real tool on this package — W1's m8 is closable.

### m8b — opened force dropped
```
| S002 | … | mined | 2020-01-01 | 90d | a-entry.md, b-entry.md |
S002	status	queued
S002	used-by	other-entry.md
```
Keeps staged `2020-01-01` (not `--opened`); no opened strip line.

### m8c — used-by force dropped
```
| S002 | … | mined | 2026-10-25 | 90d | other-entry.md |
S002	status	queued
S002	opened	2020-01-01
```
Keeps the staged passthrough `other-entry.md` instead of the computed citing-entry list; no used-by strip line.

## Why W1's detector missed it (frozen counter, read-only)
`corpus/evidence/round49/c1-count.py:257` asserts `cells[7] == "mined"` (NORMALIZED leg; :256 checks used-by, :257 opened) — but its staged fixtures hard-code status `mined` (c1-count.py:299-300, :316-317), so a no-force tool passes by passthrough. W1's mechanism note stands: cited ids in every W1 fixture were already `mined` (none S170/S171-class). A counter fixture citing a non-`mined` staged row would kill m8 (normalization is observable); recording that as a coverage finding is the reviewers' call — I changed nothing frozen.

## Boundaries / restoration
- Production `tools/assimilate-rows.py` sha256 before == after == `4b995dbc2e950613a632c83dba068e932396c1cf1d6a44dc1255f1c4f04abc32` (never edited; `cp`-only into scratch).
- Writes: this report + `/dev/shm/chousa-r49-MutToolStatus/` only. Scratch deleted: `rm -rf $T` → `ABSENT` verified. No git index/jj/fleet/sibling/shokuknow writes; no network; no installs (pacman paused; none needed); no subagents/background jobs (leaf seat).
- Counters not re-run (probe is direct tool behavior; W1 counter legs already recorded).

VERDICT: W1 survivor m8 (status-not-forced) in tools/assimilate-rows.py — holds — the adopted tool genuinely forces status→mined (and opened, used-by) and logs the replaced values in stripped.tsv while the single-point no-force mutants demonstrably keep the staged values, so the tool contract is intact and m8's W1 survival was pure fixture coverage (every cited staged row already `mined`), now closed by a queued-status probe.
