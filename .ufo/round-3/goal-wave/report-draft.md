# chousa — round 3: chain-hop resolution (coverage move)

<!-- SCRIBE DRAFT for parent integration. Measured values are from the frozen
     gate revision sha256 67daf85ecc49c4c7accbee9534c31b0734061b7f329e8de7a98254a57f9d6084
     (green — selftest PASS 40 — and stable across 4+ samples), lane HEAD
     0aa794d, and the scribe captures under /home/vgpnk/.cache/chousa-r3/.
     [PARENT] marks fields only the integrating parent may bind (commit hashes,
     acceptance, wave report count, final scorecard call). Lane HEAD at draft
     time: 0aa794db58c2aafae0a50b25b8ae9822f4007900. -->

## Work performed

- Round 3 ran as the operator's **in-session direct dispatch** of a 32-seat
  flash wave (same routing as round 2: no fleet-rendered wave, no role-alias
  overlay, **no Sighting step**; receipt identity untouched — see Debts).
  Starting lane HEAD `0aa794d`; round-3 artifacts were uncommitted at draft
  time ([PARENT] commit). Wave seat reports: `[PARENT: N/N reports]`.
- Landed the coverage move in `tools/research-gate.sh`: new mode
  `verify-chain <record> [--root PATH]` (`tools/research-gate.sh:106,890-1158,1917`).
  A **resolved** hop must carry a citation — source (a `## Sources` id or a local
  path, same canonicalization/boundary as `verify-claims`) plus an anchor the
  source must contain: `heading` (Markdown heading text, trimmed), `quote`
  (verbatim span, line-aware miss report) or `line` (one whole line, trailing
  whitespace trimmed); anchors come from an `anchor_kind`+`anchor` column pair or
  from a `to` fragment `path#kind:text`. Per hop it prints
  `CHAIN hop=… status=… observed=… source=… anchor=… at=… verdict=…`
  (`observed` verified|anchor-missing|refused|invalid|exempt) and closes with
  `RESOLVED_HOPS=N/M` plus the summary under the unchanged CLEAN|DRIFT 0/1/2
  contract. Unresolved/marked hops (`unresolved`, `blocked-no-fetch`, `rejected`,
  `labelled-dead`, `not-applicable`) stay **exempt but counted**.
- Pre-registered fixture **`corpus/fixtures/chain-r3.md`** (sha256 `06115f2f…`)
  — 22 real hops over the three archived inputs (17 resolved, 3 unresolved,
  2 blocked-no-fetch), with contract `chain-r3.README.md` (revised during the
  wave; current sha256 `72dbee4e…`); its broken-anchor control
  **`chain-r3-broken.md`** (sha256 `b66222a1…`). The
  dispatch named a JSONL pre-draft (`chain-r3.jsonl`); the landed mode reads
  Markdown records, so the author superseded and removed the JSONL rather than
  keep two copies of the same hops (`chain-r3.README.md`, "Authoring state").
- Selftest grew 30 → **40 cases** (cases 31-40: `chain-pass`,
  `chain-fail-tampered`, `chain-fail-anchor-kinds`, `chain-fail-out-of-corpus`,
  `chain-fail-external`, `chain-fail-invalid`, `chain-fail-counting`,
  `chain-fail-no-chain`, `setup-chain-no-path`, `setup-chain-missing-file`);
  the round-1/round-2 case lines are byte-identical.
- This scribe independently re-derived the fixture's ground truth: the record
  README's own gate-free python check run verbatim → `chain-r3.md:
  RESOLVED_HOPS=17/22 bad_hops=[]` and `chain-r3-broken.md: RESOLVED_HOPS=1/2
  bad_hops=['2']`; and an earlier independent sweep of the JSONL pre-draft
  (`rows=22 bad=0`). The "before" premise was measured directly on the round's
  own record (below).
- Other seats' artifacts: note `corpus/knowledge/chain-resolution-r3.md`
  (sha256 `9f16c7e7…`; mode design, anchor semantics, honest limits, its own
  receipts including a strace-confirmed zero-network run), lesson
  `corpus/lessons/2026-10-15-chain-hop-resolution.md`, four receipts
  `corpus/evidence/chain-r3-20261015T235623Z-{fixture,gate,live,selftest}.log`
  (re-cut at `67daf85e…` and the revised README `72dbee4e…`; indexed in the
  updated `corpus/evidence/README.md`), and `SKILL.md` rows (gate table now
  carries `verify <record>` / `verify-claims` / `verify-chain` and a "Chain
  mode (round 3)" section). **Still not landed at draft time:** `corpus/README.md`
  coverage rows ([PARENT] gap — integrate only what actually landed; see
  "Integration gaps").

## Landed changes

[PARENT] Work HEAD when this report is integrated: `[PARENT: commit hash]`.
Lane commits integrate under identity `chousa-shokunin <chousa@shokunin.local>`.

| Commit | Landed work | LOG connection |
|---|---|---|
| `[PARENT: commit hash]` | `verify-chain` mode + chain helpers + 10 selftest cases; fixture records `chain-r3.md` / `chain-r3-broken.md` + README | `LOG.md:[PARENT]` |

## Before → after measurements

**One axis move: coverage — chain-hop resolution becomes verdict-bearing.**
Falsifiable claim: before, chain hops are checked STRUCTURALLY only — a hop
marked `resolved` whose `to` resolves as a pointer passes even when the anchor
it cites does not exist in the target; after, `verify-chain` resolves each
resolved hop's citation (source under the corpus boundary + anchor bytes present
in the target) and reports per-hop verdicts with an exact `RESOLVED_HOPS=N/M`
under the existing contract.

**Before** (round-2 revision, sha256 `03a33244…`, lane HEAD `0aa794d`; capture
`/tmp/chousa-scribe-r3/before.txt` and `/home/vgpnk/.cache/chousa-r3/`):

```text
$ grep -c 'verify-chain' tools/research-gate.sh
0
$ bash tools/research-gate.sh verify /tmp/…/hop-phantom-line.md --root <root>
  # a hop: status=resolved, to=lib/primary.md:999 — line 999 does not exist
  # (target has 2 lines)
RESEARCH_GATE: CLEAN (findings=0 drift=0 questions=1 sources=1 chains=1 claims=1 negatives=0 rejections=1 approvals=0)
exit=0
```

The r1/r2 `verify` path counts the hop and passes it CLEAN. On the round's own
control record, the same hole is measurable: `verify
corpus/fixtures/chain-r3-broken.md --root ..` → `RESEARCH_GATE: CLEAN
(findings=0 … chains=2 …)`, exit 0 — a hop whose anchor bytes exist nowhere in
its target passes the structural check (fixture README "Execution record" item
4; re-measured by this scribe at `67daf85e…`).

**After** (gate sha256 `67daf85ecc49c4c7accbee9534c31b0734061b7f329e8de7a98254a57f9d6084`,
identical across 4+ samples, selftest PASS):

```text
$ bash tools/research-gate.sh verify-chain corpus/fixtures/chain-r3.md --root ..
  # 17 × CHAIN … verdict=match; gate at= 74,64,35,107,109,57,71,67,79,88,67,87,89,52,63,55,107
  # 5 × CHAIN status∈{blocked-no-fetch,unresolved} observed=exempt
RESOLVED_HOPS=17/22
RESEARCH_GATE: CLEAN (hops=22 verified=17 exempt=5 anchor-missing=0 refused=0 invalid=0 findings=0 drift=0)
exit=0

$ bash tools/research-gate.sh verify-chain corpus/fixtures/chain-r3-broken.md --root ..
CHAIN hop=1 status=resolved observed=verified source=research/deep-research-2026-09-28/A-shokunin-tradition.md anchor=quote:"I could not substantiate this spelling as an established art" at=line:64 verdict=match
CHAIN hop=2 status=resolved observed=anchor-missing source=research/deep-research-2026-09-28/C-rank-taxonomy.md anchor=quote:"人為 — jin’i-ryū" at=- verdict=mismatch
FINDING CHAIN_ANCHOR_NOT_FOUND severity=warn surface=chain obs=hop=2 source=research/deep-research-2026-09-28/C-rank-taxonomy.md anchor=quote:"人為 — jin’i-ryū" nearest_line=53 context=The key distinction is between skill, teaching authority, and permission to act.
RESOLVED_HOPS=1/2
RESEARCH_GATE: DRIFT (hops=2 verified=1 exempt=0 anchor-missing=1 refused=0 invalid=0 findings=1 drift=1)
exit=1
```

22/17/5 and 2/1/1 are the fixtures' pre-registered ground truth
(`chain-r3.README.md`, "Hops" and "Execution record"); the gate agrees.

**Negative controls** (broken record above, plus in-selftest cases 31-40, all
exit 1 where drift is expected): tampered anchor (`chain-fail-tampered`),
invalid/conflicting anchor kinds (`chain-fail-anchor-kinds`), out-of-corpus
source refused unopened (`chain-fail-out-of-corpus`), URL source
`CHAIN_SOURCE_EXTERNAL` crit (`chain-fail-external`), missing anchor/unknown
status invalid (`chain-fail-invalid`), exact counting
`RESOLVED_HOPS=2/8 hops=8 verified=2 exempt=2 anchor-missing=1 refused=1
invalid=2` (`chain-fail-counting`), no chain table (`chain-fail-no-chain`);
setup: `verify-chain` with no path / missing record → exit 2, stdout empty.
The live receipt additionally records four record-level controls
(`corpus/evidence/chain-r3-20261015T235623Z-live.log`): a tampered quote anchor
(`…semanticsX`) → exit 1 `anchor-missing`; out-of-corpus absolute
source → exit 1 refused; external URL source → exit 1
`CHAIN_SOURCE_EXTERNAL`; a resolved hop marked `unresolved` → exempt, counted,
CLEAN `RESOLVED_HOPS=16/22` (exemption is the record author's declaration, not
a resolution — the honest limit the note names).

**Selftest:** `bash tools/research-gate.sh --selftest` → `RESEARCH_GATE_SELFTEST:
PASS (40 cases)`, exit 0; **first 30 case lines byte-identical** to the round-2
baseline capture (cmp-verified by this scribe).

**Existing behavior byte-stable:** at `CHOUSA_NOW_EPOCH=1760000000`, A/B/C each
exit 1 with stdout **byte-identical** to the round-2 baseline (itself identical
to the r1 baseline); intake exits 0 byte-identical (8 chains); `verify-claims`
on the round-2 fixture byte-identical, `VERDICT_BEARING_CLAIMS=17/17`;
`VERDICT_BEARING_EXPORTS=3/3`; fixture gate-free byte-check `counts {'supported':
13, 'contradicted': 2, 'unsupported': 2} bad []`. All scribe-measured
(`/home/vgpnk/.cache/chousa-r3/now/` vs `…/r2-baseline/`).

**Exempt is not verified.** Hops 18-22 of `chain-r3.md` count but prove nothing
about their citations: the two `blocked-no-fetch` hops cite the exports' own
external chips (コトバンク, arxiv.org) and are never fetched; hops 20-22 are real
chain breaks the record MARKS (e.g. `人為 — jin’i-ryū` absent; the same bytes
appear as the tampered hop of the broken control). A CLEAN run therefore means
N = M − exempt resolved, not that every hop was verified
(`chain-r3.README.md`, "Why the negative control is the round's falsification").

**No-external-fetch bound:** no network primitive exists in the gate
(`grep -E '\b(curl|wget|nc|ssh|scp|ftp|dig|nslookup|telnet)\b'` → none); chain
sources are canonicalized and confined to `CHOUSA_ROOT`/lane root, URLs →
`CHAIN_SOURCE_EXTERNAL` crit, session/denylist → `CHAIN_SOURCE_SESSION` crit,
outside → `CHAIN_SOURCE_OUT_OF_CORPUS` crit — refused before any read. The
fixture's two external hops are pre-marked exempt, never opened.

**Independent ground-truth checks (scribe):** the fixture README's own gate-free
python check, run verbatim by this seat → `chain-r3.md: RESOLVED_HOPS=17/22
bad_hops=[]` and `chain-r3-broken.md: RESOLVED_HOPS=1/2 bad_hops=['2']`; an
earlier sweep of the (since-removed) JSONL pre-draft against the pinned export
sha256s → `rows=22 bad=0`. The three export pins were re-derived from disk and
match the fixture README.

**Environment defect (recurring, named; not a gate defect):** the host `/tmp`
tmpfs (user quota) returned `Disk quota exceeded` to scribe writes twice within
minutes at round start (same defect round 2 recorded); this seat moved all
scratch and the gate's `TMPDIR` to `/home/vgpnk/.cache/chousa-r3/`. The gate
honors `TMPDIR` (round-2 fix) and its own runs were unaffected. The fleet `/tmp`
quota remains environment-owned (see Debts).

## Defects found by the scribe seat

1. Fixture README pins — **found and fixed in-wave**. At the earlier README
   sample (sha256 `25148a1b…`) the "Execution record" pinned revision
   `7379b7ee…` and a fixture sha `6f73c8d0…` that did not match the shipped
   `chain-r3.md` (`06115f2f…`). The author's revised README (current sha256
   `72dbee4e…`) pins the settled revision `67daf85e…` and the correct fixture
   shas, and the receipt set was cut against the revised README. [PARENT:
   ensure the `72dbee4e…` revision is the one integrated.]
2. Receipt nuances — **found in-wave and fixed by the receipts re-cut**. In the
   superseded `235411Z` stamp, "negative control 1" tampered `kiwami
   semantics` → `kiwami semantic` (a substring of the real bytes, so it still
   resolved, exit 0) and the fixture receipt's scratch adapter printed
   `CHAINCHECK_SUMMARY: FAIL (1 fixture(s) inconsistent)` for the broken
   control's pre-registered `bad_hops=['2']`. The integrated `235623Z` stamp
   tampers to `…semanticsX` (a genuine miss, exit 1) and its adapter summary
   reads "2 fixtures re-derived; chain-r3.md all 17 resolved anchors present;
   chain-r3-broken.md hop 2 absent as expected". Read the `235623Z` set.
3. Cosmetic residual carried from round 2: `tools/research-gate.sh:75`
   `VERSION=research-gate-r1` — every mode still banners `research-gate-r1`.
4. Lane hygiene (not part of the deliverable): untracked `before.transcript`
   sits in the lane root (another seat's scratch); parent decides keep/remove.
5. Carried structural residuals (named in the note): in-root hardlinks still
   bypass path canonicalization and there is no size cap on source reads.

## SHONEN

Author assertions only; a `[x]` requires a named non-author verifier, which this
round did not have. No promotion is implied.

- [~] SKILL.md carries real decision tables/error patterns/checklists: landed —
  the gate table now carries the `verify-chain` row (verdict map, shared
  selftest `PASS (40 cases)` with chain cases 31–40, pinned fixture ground
  truth) and a "Chain mode (round 3)" section; the decision table's "Follow a
  citation chain" row now reads "resolve its anchor there". No independent
  review is implied.
- [~] At least one end-to-end domain task executed and logged: 22-hop
  citation-chain resolution over the three pinned archives, plus the
  broken-anchor control; receipts
  `corpus/evidence/chain-r3-20261015T235623Z-{fixture,gate,live,selftest}.log`
  and the note's own runs (`corpus/knowledge/chain-resolution-r3.md`, incl. the
  strace zero-network check).
- [~] Instructions executable without oral context: `verify-chain <record>
  [--root ..]` runs from the lane cwd; the fixture README carries the re-run
  commands and the gate-free checker. No independent agent-without-oral-context
  review is claimed.
- [~] No cross-domain bleed: PROVINCE.md unchanged; fixture material stays
  byte controls (hop 9's ACE numerals reproduced only as the round-2 boundary
  case), never adopted.

## Per-axis and learning verdicts

Verdict vocabulary only; no scalar. The declared round move is **coverage**;
other axes are judged separately with their own evidence boundaries.

| Axis | Verdict | Evidence boundary |
|---|---|---|
| coverage | improved | Before: hops structural only — a resolved hop citing a non-existent anchor passes (`verify` on the broken record: CLEAN, exit 0; phantom-line demo at `03a33244…`). After: every resolved hop's citation resolved with per-hop verdicts and exact `RESOLVED_HOPS=N/M` over 22 real hops of the three archived inputs (17/22 + 5 exempt; broken control caught as anchor-missing). Boundary: anchor byte existence + local boundary only — not semantics, not authorship (cross-input hops are co-anchors: they assert the bytes exist in the target, never that the target cites the source input) |
| operability | improved | New public mode under the preserved exit contract (setup stdout empty); selftest 30 → 40 all PASS with the first 30 case lines byte-identical; `verify`/`verify-claims` outputs byte-stable; capped observables unchanged (`VERDICT_BEARING_EXPORTS=3/3`, `VERDICT_BEARING_CLAIMS=17/17`). Boundary: the r1 capped count is unchanged; [PARENT: keep `improved` (new runnable mode) or set `unchanged` if only the capped 3/3 count is read — either is supported] |
| depth | unchanged | No independently verified domain fact; fixture anchors are byte controls, not knowledge |
| freshness | unchanged | Archive pins re-checked at fixed revisions only; no new cross-revision drift detector |
| calibration | unchanged | Limits explicit (existence not semantics; exempt ≠ verified; exemption is the record's own marking); no non-author discernment |
| adjacency | unchanged | Foreign-province material kept as exemptions/near-misses; zero network; research corpus read-only |

Learning trends: **expansion improved** — net-new fixtures + contract README on
ground the coverage map did not hold (chain-hop resolution), plus new gate edge
classes (`CHAIN_SOURCE_*`, `CHAIN_ANCHOR_NOT_FOUND`, `CHAIN_CITATION_INVALID`);
`corpus/README.md` coverage rows `[PARENT: verify landed]`.
**quality unchanged** — the new CLEAN is structural; no older admitted entry was
reverified or superseded.
**discernment unchanged** — no non-author admit/reject spot-check.

## Debt, cross-domain handoff and admission

| Debt | Owner / concrete unblock |
|---|---|
| **Receipt identity (round 1) — STILL OPEN** | The direct interactive launch supplies no authentic queue taskKey or stored expected receipt bag (`.ufo/evidence/round-1/receipt-blocker.json`). Mission acceptance remains integrator-owned: bind this mission/identity to an authentic dispatcher task and validate the six expected fields before any Sighting completion. No `task_…` value was invented; proven receipt-backed completed rounds remain **0**; operator target remains at least 100. |
| Round-3 artifact gaps | Landed: note (`corpus/knowledge/chain-resolution-r3.md` sha256 `9f16c7e7…`; it cites the revised README `72dbee4e…`), lesson (`corpus/lessons/2026-10-15-chain-hop-resolution.md`), four receipts (`corpus/evidence/chain-r3-20261015T235623Z-*.log`, indexed in `corpus/evidence/README.md`), `SKILL.md` rows. Not landed at draft time: `corpus/README.md` coverage rows — integrate them only if they land; otherwise record the gap. Fixture README pins were corrected in-wave (defect 1); the receipt nuances were fixed by the `235623Z` re-cut (defect 2). |
| Fleet `/tmp` quota exhaustion | Environment-owned (recurred at round-3 start); gate/scratch honor `TMPDIR`/home scratch; other lane tooling should too. |
| Scope-refusal finding IDs (round-1 debt) | Still open — documentary refusals only. |
| Non-author spot-check (discernment) | Integrator/operator samples ≥1 admit and ≥1 reject; until then no discernment gain or promotion. |
| Frozen replay gate conformance | `corpus/evidence/round-1/expected.json` pins inputs but is not a rerunnable comparator; still open. |

Cross-domain: no host/source/sibling/shared-ledger mutation; the archived
research corpus was read-only; native session material excluded from commits.

## Fresh-session continuation

[PARENT] Bind `.ufo/continuations/round-2.json` (or a round-3 successor file) to
this report and the integrated work HEAD. Acceptance stays separate from local
craft results: this report claims local evidence only, no receipt and no
Sighting.