# ExecChainCollision — C1 falsification probe: simultaneous-substitution property of assimilate-rows.py

Seat: ExecChainCollision (leaf; no subagents, no background jobs). Wave: round 49 / w1 (build + first falsifiers). Tooling: no installs (no tool was needed; system `python3` stdlib only — RULES.md channel list not exercised; record: n/a).

## Subject

- Candidate: `tools/assimilate-rows.py` at commit `65940928cc9332b386bcbca92571451cc4374cbe` (verified `git -C <lane> log -1 --format=%H -- tools/assimilate-rows.py`), sha256 `3b8a6e7daa45dca66c1d2f84cbb7903d999091a75a4b92ac2cda2c71997b06a6`.
- Property probed: staged-id → lane-id substitution is **simultaneous** (one pass over the original text), so chained maps (staged S100→lane S101, staged S101→lane S102, both cited) must not double-shift.

## Fixture (scratch, /tmp/chousa-r49-ExecChainCollision/)

- `registry.md`: `## Registry` with one row `| S100 | prior row — https://registry.example/prior |` ⇒ next free id = S101.
- `staged.md`: two 11-cell staged rows `S100` (https://example.org/probe-a) and `S101` (https://example.org/probe-b); neither URL held by the registry.
- `knowledge/corpus/knowledge/chain-probe.md` (entry): cites both staged ids — "Staged document S100 backs the claim stated at S100; staged document S101 backs the claim stated at S101. Both are cited here: S100, S101."

## Probe run (tool)

```
$ python3 <lane>/tools/assimilate-rows.py --staged /tmp/chousa-r49-ExecChainCollision/staged.md \
    --registry /tmp/chousa-r49-ExecChainCollision/registry.md \
    --knowledge /tmp/chousa-r49-ExecChainCollision/knowledge --opened 2026-10-25 \
    --out /tmp/chousa-r49-ExecChainCollision/out --entry corpus/knowledge/chain-probe.md
COLLISIONS=1
CITED=2 APPEND=2 HELD=0
```

(`COLLISIONS=1` is the informational diagnostic at `assimilate-rows.py:135-136` — staged S100 intersects registry S100; it is not a refusal, run continued.)

`out/renumber.tsv`:

```
staged_id	lane_id	action	url
S100	S101	append	example.org/probe-a
S101	S102	append	example.org/probe-b
```

Tool output entry `out/corpus/knowledge/chain-probe.md`:

```
# Chain probe

Staged document S101 backs the claim stated at S101; staged document S102 backs the claim stated at S102. Both are cited here: S101, S102.
```

Tool `out/append.md` rows (each row keeps its own document's URL, id renumbered):

```
| S101 | Chain probe A — https://example.org/probe-a | docs | B | probe | §1 | chained citation text | mined | 2026-10-25 | 180d | corpus/knowledge/chain-probe.md |
| S102 | Chain probe B — https://example.org/probe-b | docs | B | probe | §1 | chained citation text | mined | 2026-10-25 | 180d | corpus/knowledge/chain-probe.md |
```

⇒ Tool output cites each document's correct id: original S100 mentions → S101, original S101 mentions → S102. No chaining.

## Naive sequential control (10-ish lines: `control.py`, same renumber.tsv mapping, word-boundary `\bS\d{3,}\b`)

```
import re
import sys
TOKEN = re.compile(r"\bS\d{3,}\b")
MAPPING = {}
with open(sys.argv[1], encoding="utf-8") as fh:
    for line in fh:
        parts = line.rstrip("\n").split("\t")
        if len(parts) == 4 and parts[2] != "action":
            MAPPING[parts[0]] = parts[1]
text = open(sys.argv[2], encoding="utf-8").read()
for src, dst in MAPPING.items():
    text = TOKEN.sub(dst, text)
print(text, end="")
```

```
$ python3 control.py out/renumber.tsv knowledge/corpus/knowledge/chain-probe.md
# Chain probe

Staged document S102 backs the claim stated at S102; staged document S102 backs the claim stated at S102. Both are cited here: S102, S102.
```

⇒ control double-shifts: original S100 mentions became S101 then got re-replaced to S102; every citation collapses to S102. `diff` tool-output vs control: `3c3` — control line differs exactly in the S101 mentions being S102.

## Mechanism (why the tool holds)

`assimilate-rows.py` builds `sub` from the whole mapping, then applies one regex pass: `TOKEN_RE.sub(lambda m: sub.get(m.group(0), m.group(0)), s)` (`:182-183`; token regex `:54`), i.e. every match is resolved from the **original** string via the dict — replacements never re-enter the scan. `cited` is computed from entry text (`:150`); row id cell is overwritten to the lane id (`:196`), so append rows are consistent too.

## Result

- Falsification attempt **failed** — the simultaneous-substitution property holds for chained mappings (staged S100→S101, S101→S102, both cited).
- The naive sequential control double-shifts; the candidate does not. No bug found in this property; no change made to the tool or any production file.

VERDICT: Built chained-map fixture (registry max S100; staged S100/S101 both cited) and ran the frozen C1 adopter vs a naive sequential re.sub control — tool substitutes simultaneously (each doc keeps its correct lane id), control double-shifts; property stands, no falsification.
