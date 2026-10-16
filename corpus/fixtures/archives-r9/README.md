# archives-r9 — the three archived research inputs as gate-format records (round 9)

Round 9 converts the three read-only archives under
`research/deep-research-2026-09-28/` into the research-gate's record format —
one record per archive — and runs each through `verify-all` end-to-end. This is
a fixture-led round: **no gate change accompanies this set**. Every number
below was measured at gate sha256
`46f5ddb39d5fafa220fb584121dba2f4a15e071a91fa42728849f3c7567c6ccd` (the
round-8 admitted gate), from the lane root with `--root ..`, on 2026-10-16.

## Files and pins

| record | source archive (read-only) | source sha256 | record sha256 |
|---|---|---|---|
| `A-r9.md` | `research/deep-research-2026-09-28/A-shokunin-tradition.md` | `9033857d4625555c7b778dfad6df80e3e1b24ed8bffa3fee2fd445b9c5540b85` | `338918fcb8ed5d6c5f15dc64e5eb8a3ae7a005d51b5c03e7e377c1dab9173c78` |
| `B-r9.md` | `research/deep-research-2026-09-28/B-multiagent-knowledge.md` | `6d8dbddd3e2d2f47dcb153c5a3347cc6321db4afc72cf07da40f0f7fe5022006` | `abfa5290deda4d1708ba97028853b8a770f16ecda6f377dddda53d49cb2e3e86` |
| `C-r9.md` | `research/deep-research-2026-09-28/C-rank-taxonomy.md` | `e48fe70ff92055c217ac6ca6ce68e403aa5689fee8717f3bd0ccf5badc92321b` | `97be0e69ccfb8a701bc5556f738553be8e7179c9b41110fe61c4a3cab4f2d1da` |

Record shas are of this revision; editing a record invalidates its row.

The shared claims surface the records bind (each via its `## Meta` row
`| claims_file | chousa-shokunin/corpus/fixtures/claims-r9.jsonl |`) is
`corpus/fixtures/claims-r9.jsonl`, sha256
`f6f0d1ab6b6cbd045035951c7eb4653406dc0853234a8077a8685509bfc94ff5` at the
time of these runs. It adds 10 claims beyond round 2's 17 (claims mode:
`VERDICT_BEARING_CLAIMS=10/10`, CLEAN, exit 0). If that file is extended,
re-run the commands below; the claims section re-verifies whatever the file
holds.

## How to read a record

Each record carries: `## Meta` (window loopback, fetch none, claims binding,
archive pin); `## Question`; `## Sources` (the archive's own named works as
declared ids — A's dictionaries and workshop accounts, B's paper work-table,
C's federations — each pointer being the archive line where the work is named,
because no cited external document is held locally); `## Chain` (self-quotes
anchored in the archive, cross-archive convergence hops, and one
`blocked-no-fetch` external chip); `## Claims` (pointed rows, each with a
verbatim `span` cell); `## Negatives` + `## Sweeps` (one re-runnable local
check); `## Rejections` (the archive's own corrections kept with reason and
flip-condition).

Every `span` and `anchor` was extracted from the archive bytes by a builder
keyed on (line, start-marker, end-marker) — never retyped — then checked
twice: the gate's token-boundary matcher for every chain anchor and claims-file
span, and an independent byte check for the record `span` cells. The byte
check, run from the lane root (result: A `ok=5 bad=0`, B `ok=6 bad=0`,
C `ok=8 bad=0`; the same invocation names each archive):

```sh
python3 - corpus/fixtures/archives-r9/A-r9.md ../research/deep-research-2026-09-28/A-shokunin-tradition.md <<'PY'
import sys
rec = open(sys.argv[1], encoding="utf-8").read()
arc = open(sys.argv[2], encoding="utf-8").read()
sec = rec.split("## Claims", 1)[1].split("\n## ", 1)[0]
ok = bad = 0
for row in sec.splitlines():
    if not row.startswith("|") or row.startswith("|---") or "| id |" in row:
        continue
    span = [c.strip() for c in row.strip("|").split("|")][3]
    ok, bad = (ok + 1, bad) if span in arc else (ok, bad + 1)
print(f"ok={ok} bad={bad}")
PY
```

## Verification (measured, gate `46f5ddb3…`)

`verify-all` on each record, claims bound. All three compose CLEAN with zero
findings and zero drift — no integrity findings surfaced, so none needed
documenting:

```text
A-r9.md
SECTION structure state=run verdict=CLEAN findings=0 drift=0
SECTION claims state=run verdict=CLEAN findings=0 drift=0 tally=VERDICT_BEARING_CLAIMS=10/10
SECTION chain state=run verdict=CLEAN findings=0 drift=0 tally=RESOLVED_HOPS=6/7
SECTION sweeps state=run verdict=CLEAN findings=0 drift=0 tally=VERIFIED_SWEEPS=1/1 REJECTIONS_OK=4/4
SECTION integrity state=run verdict=CLEAN findings=0 drift=0 tally=INTEGRITY refs=13 resolved=12 unresolved=0
VERIFY_ALL sections=5 run=5 absent=0 drift-sections=0 findings=0 drift=0
RESEARCH_GATE: CLEAN (sections=5 run=5 absent=0 drift-sections=0 findings=0 drift=0)
exit=0

B-r9.md
SECTION structure state=run verdict=CLEAN findings=0 drift=0
SECTION claims state=run verdict=CLEAN findings=0 drift=0 tally=VERDICT_BEARING_CLAIMS=10/10
SECTION chain state=run verdict=CLEAN findings=0 drift=0 tally=RESOLVED_HOPS=6/7
SECTION sweeps state=run verdict=CLEAN findings=0 drift=0 tally=VERIFIED_SWEEPS=1/1 REJECTIONS_OK=3/3
SECTION integrity state=run verdict=CLEAN findings=0 drift=0 tally=INTEGRITY refs=14 resolved=13 unresolved=0
VERIFY_ALL sections=5 run=5 absent=0 drift-sections=0 findings=0 drift=0
RESEARCH_GATE: CLEAN (sections=5 run=5 absent=0 drift-sections=0 findings=0 drift=0)
exit=0

C-r9.md
SECTION structure state=run verdict=CLEAN findings=0 drift=0
SECTION claims state=run verdict=CLEAN findings=0 drift=0 tally=VERDICT_BEARING_CLAIMS=10/10
SECTION chain state=run verdict=CLEAN findings=0 drift=0 tally=RESOLVED_HOPS=7/8
SECTION sweeps state=run verdict=CLEAN findings=0 drift=0 tally=VERIFIED_SWEEPS=1/1 REJECTIONS_OK=4/4
SECTION integrity state=run verdict=CLEAN findings=0 drift=0 tally=INTEGRITY refs=15 resolved=14 unresolved=0
VERIFY_ALL sections=5 run=5 absent=0 drift-sections=0 findings=0 drift=0
RESEARCH_GATE: CLEAN (sections=5 run=5 absent=0 drift-sections=0 findings=0 drift=0)
exit=0
```

Solo-mode spot checks agree with the composed tallies (each composed section
is the solo mode as a fresh subprocess, and was re-run solo for A): `verify`
(structure) CLEAN on all three (`sources=6/7/6`, `chains=7/7/8`,
`claims=5/6/8`, `rejections=4/3/4`); `verify-sweeps` CLEAN on all three
(`VERIFIED_SWEEPS=1/1 REJECTIONS_OK=4/4`, `3/3`, `4/4`); `verify-claims` on
the shared claims surface CLEAN `10/10`; `verify-chain A` CLEAN
`RESOLVED_HOPS=6/7` with the exempt hop `status=blocked-no-fetch`;
`verify-integrity A` CLEAN `refs=13 resolved=12 unresolved=0`. The one
`observed=exempt` reference in each integrity run is the `from` token of the
`blocked-no-fetch` chain row, counted exempt per the integrity contract (an
exempt-status row's reference tokens are counted, not required to resolve).

## Re-run recipe

```sh
cd chousa-shokunin
for r in A B C; do
  bash tools/research-gate.sh verify-all corpus/fixtures/archives-r9/$r-r9.md \
    --claims corpus/fixtures/claims-r9.jsonl --root .. ; echo "exit=$?"
done
```

Expected at the pins above: each run prints `VERIFY_ALL sections=5 run=5
absent=0 drift-sections=0 findings=0 drift=0` and `RESEARCH_GATE: CLEAN`,
exit 0.

## Coverage (before → after, measured)

Before: the archives had structural verification (r1's 3/3 export intake) and
pointwise claim/chain fixtures (r2's 17 claims, r3's 22 hops); no archive had
passed `verify-all` as a record. After: three records, each composed CLEAN
(`sections=5 run=5 absent=0`, 0 findings, 0 drift); 19 pointed record claims
(A 5, B 6, C 8), each with a byte-checked verbatim span; 22 chain hops
(19 verified, 3 exempt `blocked-no-fetch`); 11 kept rejections (4/3/4) with
reason and flip-condition; 3 re-runnable sweeps verified empty; 19 source rows
with locally resolving pointers; `INTEGRITY refs=42 resolved=39 unresolved=0`
(3 exempt). Claim surfaces over the archive corpus now total 17 (r2) + 10
(r9 JSONL) + 19 (in-record) = 46 rows; the round-9 delta is 29 new rows.

## Reframing risk: record-format distortion (named and mitigated)

A chat export is not a structured record, and this conversion imposes structure
the export does not have. Named risk: a CLEAN `verify-all` on these records
certifies record-format integrity against archive bytes — not the external
truth of anything the archives cite, and not the completeness of their
arguments.

Mitigations, all visible in the bytes:

- Claims are scoped as text-level observations ("the export records/states
  X") with a verbatim span; no record claim asserts an external fact.
- Spans/anchors are machine-extracted from the archive bytes, never retyped;
  claims-file spans are gate-verified and record spans byte-checked.
- Tiers never promote the exports above `export`; their cited works are
  `secondary` and marked "word-of-export only, not held locally"; bare chips
  and hosts stay marked `blocked-no-fetch` hops, never opened or inferred
  into URLs.
- Inter-archive hops are convergences, not citations: the three archives are
  independent chats and none cites another (measured: `grep -cE
  "deep-research|archive [ABC]|export [ABC]|A-shokunin|B-multiagent|C-rank"`
  returns 0 in each). Each cross-archive hop's notes say so, and its anchor
  is verbatim in the target archive, so the convergence itself is checkable.
- The archives' own corrections are kept as rejections with flip-conditions
  rather than erased.
- The sweep proves only its own local re-run (no `saved-*`/`*-snapshot-*`
  copies under the archive directory); it proves nothing external.

Residual distortion (named, not fixed): `text` cells paraphrase; only `span`
cells and chain anchors are verbatim, so read span+pointer, not prose. The
exports are also cut (the r1 intake noted answers truncated mid-response), so
a record structures what survived the cut — an absent section in an archive is
not an answer of "no". Tallies like `RESOLVED_HOPS=6/7` grade anchor existence
in the archive bytes, not the strength of the export's argument.

## Authoring notes for future fixture authors

- A `to` cell written as `path#quote:text` drifts structure mode
  (`CHAIN_HOP_UNRESOLVED`: the structure check cuts a pointer at its first
  `:`); use `to` = declared source id or clean local path plus
  `anchor_kind`/`anchor` columns, as these records do (measured in a probe
  before authoring).
- `## Rejections` rows need non-empty `reason` and `flip_condition` cells, or
  `verify-sweeps` drifts them (`SWEEP_REJECTION_INCOMPLETE`).
- Binding the claims surface via the `## Meta` `claims_file` row keeps
  `verify-all` self-contained; a command-line `--claims` overrides it.