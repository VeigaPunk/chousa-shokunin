# Attack17 — R47 C1 counter coverage: leaf/ancestor key polarity (mut-f)

author: chousa L1 scout subagent (Attack17), round 48 w1
date: 2026-10-25
scope: read-only on the lane; scratch only under /tmp/chousa-r48-Attack17 (removed before finish)

## 1. Target and method

R47 C1 freeze (claims.md lines 24-65, frozen counter `corpus/evidence/round47/c1-count.py`)
was already known to have a dead defect: `MutC1Refined.md` (R47 w2) scored seven
refinement mutants of `tools/inference-ground.py` with the frozen counter and only
two died (c/d, via R46_ENTRIES); five survived, including **mut-f** (key_negated
leaf-key only, lines 28, 62-66 of that report). This attack re-derives mut-f
against the **current tip** (`02d95d3`, sha256 9d789b34…925149b — the wave-2 fix
that documents leaf-key polarity in the tool docstring lines 45-49) and re-tests
whether the frozen counter catches it.

Setup: mutation applied only to a scratch copy
`/tmp/chousa-r48-Attack17/mutant/inference-ground.py` (sha256
f02ecf27c060da65e9fc1b15d85922bcff09baa47a4e9e1b97e3b7b200595a56). The one
edit: `key_negated(path)` — `leaf = parts[-1]` + generic-leaf defers to parent
(`leaf = parts[-2]` when `leaf.lower() in GENERIC_KEYS` and `len(parts) > 1`) →
leaf-only, no parent deferral (`leaf = parts[-1]` unconditionally). No lane file
touched; no installs (tooling directive: nothing installed).

## 2. Minimal killer setup (exact leg shape)

`python3 <tool> --entry entry.md --spans spans.tsv --counts counts.json --root <k>`
under `/tmp/chousa-r48-Attack17/mutant/killers/f/`:

- `counts.json`: `{"without_archive": {"count": 1582}}` — negation only on the
  ancestor key; generic leaf `count` (no fixture in the pinned set has a nested
  counts key).
- `spans.tsv`: one row S902 → `spans/S902-1.txt` ("The archived copy is dated at
  build, and the manifest tracks which answers dropped out…"; no digits, so the
  figure grounds via the counts leg).
- `entry.md`: Inference bullet `1,582 records carry no archive bucket, so they
  are unbound (S902)` — figure kept negated (negator `no` within the next 4
  words), so it is genuinely positive.

## 3. Results

| run | output | verdict |
|---|---|---|
| pristine tip on killer | `GROUND: PASS` exit 0 | correct (affirmed) |
| mutant mut-f on killer | `FINDING INF_POLARITY_FLIP bullet=1 token='1,582 / counts key without_archive/count'` exit 1 | false refusal — mutant misreads ancestor-negated key as affirmative |
| frozen counter vs pristine tip | `TOOL=present POSITIVE_PASS=3/3 JUNK_KILLED=3/3 CANARY=pass R46_COUNTER=pass R46_ENTRIES=2/2 C1=PASS` exit 0 | baseline matches claims.md target |
| frozen counter vs mutant mut-f | **identical** `C1=PASS` exit 0 | **mutant survives** |
| frozen counter vs always-exit-1 tool (control) | `POSITIVE_PASS=0/3 JUNK_KILLED=0/3 CANARY=fail R46_COUNTER=fail R46_ENTRIES=0/2 C1=FAIL` exit 1 | counter is operational — the survival is a genuine blind spot, not a dead counter |

## 4. Why the frozen counter misses it

The counter's scoring legs read (1) six pinned fixtures of
`corpus/fixtures/inference-ground-r47/` and (2) the two R46 entries. The pinned
`counts.json` has only flat keys (`answers_named_source`, `answers_archived`,
`answers_without_archive_key`): the key polarity exercised is leaf-carried, never
ancestor-carried, so the ancestor-deferral branch of `key_negated` is never
reached. The R46 entry legs run with `--counts /dev/null` (c1-count.py lines
119-123), so no figure key is seen there either. Result: no leg can distinguish
leaf-only from parent-deferral key polarity, so a ref that breaks exactly that
refinement scores a perfect C1=PASS. The same is true for the other four
survivors (a/b/e/g — implicit negators, un- forms, repeated figure occurrences),
per `MutC1Refined.md` §5: the dead set contains no implicit negator, no un-
negator/flip, no repeated figure, no nested counts key.

## 5. Verdict

R47 C1's class-key-polarity coverage defect is **reproduced and confirmed at the
current tip**: a minimal scratch mutant of `key_negated` (parent-deferral →
leaf-only) survives the frozen counter with all legs PASS, while the same mutant
is killed by a minimal positive fixture documenting the refinement. This is a
pure frozen-counter coverage gap (as routed in round-47-verifier-spotcheck.md §6
item 2), not a tool defect — the pristine tool implements and passes the refined
predicate. Fix direction (not applied): add the nested-counts-key positive fixture
(above) to the pinned set; then mut-f yields `POSITIVE_PASS=2/3 C1=FAIL`.
