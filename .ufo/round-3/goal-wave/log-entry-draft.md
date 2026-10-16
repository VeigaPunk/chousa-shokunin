# LOG.md — round-3 entry draft (parent-owned file; integrate under [PARENT] markers)

<!-- SCRIBE DRAFT. Measured values from the frozen gate revision
     sha256 67daf85ecc49c4c7accbee9534c31b0734061b7f329e8de7a98254a57f9d6084
     (green + stable), lane HEAD 0aa794d, fixture shas
     chain-r3.md 06115f2f…, chain-r3-broken.md b66222a1…,
     chain-r3.README.md 72dbee4e… (revised in-wave), note
     corpus/knowledge/chain-resolution-r3.md 9f16c7e7…. Scribe captures in
     /home/vgpnk/.cache/chousa-r3/. The report draft's debts section keeps the
     receipt-identity debt named per the mission contract. -->

## 2026-10-15 — round-3 coverage: chain-hop resolution becomes verdict-bearing

Round 3 executes the move round 2 registered: chain-hop resolution — each hop's
citation must resolve to a real corpus location. The operator dispatched this
wave directly in-session (same routing as round 2; **no Sighting step was
invoked**); receipt identity from round 1 remains open and untouched by this
round.

**Before.** The shipped round-2 gate (sha256 `03a33244…`, lane HEAD `0aa794d`)
has no chain-citation mode — `grep -c 'verify-chain' tools/research-gate.sh`
is 0 — and its `verify` path checks hops STRUCTURALLY only. Measured on the
round's own control record: `verify corpus/fixtures/chain-r3-broken.md --root ..`
→ `RESEARCH_GATE: CLEAN (findings=0 … chains=2 …)`, exit 0, although hop 2
cites `人為 — jin’i-ryū` which exists nowhere in its target. Independently, a
synthetic hop `status=resolved to=lib/primary.md:999` (line 999 does not exist
in a 2-line target) passes CLEAN exit 0 at the r2 revision. Captures:
`/tmp/chousa-scribe-r3/before.txt`, `/home/vgpnk/.cache/chousa-r3/before-demo.txt`.

**The move.** New `verify-chain <record> [--root PATH]` mode
(`tools/research-gate.sh:106,890-1158,1917`). A resolved hop must carry a
citation: source (a `## Sources` id or a local path — same canonicalization and
corpus boundary as `verify-claims`) plus an anchor the source must contain —
`heading` (Markdown heading text, trimmed), `quote` (verbatim span, line-aware
miss with `nearest_line`/`context`), or `line` (one whole line, trailing
whitespace trimmed); anchors come from an `anchor_kind`+`anchor` column pair or
a `to` fragment `path#kind:text` (`chain_citation` `:910-950`; matcher
`chain_anchor_at` `:953-985`). Per hop: `CHAIN hop=… status=… observed=…
source=… anchor=… at=… verdict=…` (`observed`
verified|anchor-missing|refused|invalid|exempt; `verdict`
match|mismatch|refused|invalid|exempt), then `RESOLVED_HOPS=N/M` (N = verified
hops over M read) and the summary under the unchanged exit contract (0 CLEAN /
1 DRIFT / 2 setup). Unresolved/marked hops (`unresolved`, `blocked-no-fetch`,
`rejected`, `labelled-dead`, `not-applicable`) stay **exempt but counted**;
CLEAN iff N + exempt = M and no finding drifts. Refusals reuse the r2 boundary:
URL → `CHAIN_SOURCE_EXTERNAL` crit, session/denylist → `CHAIN_SOURCE_SESSION`
crit, outside both roots → `CHAIN_SOURCE_OUT_OF_CORPUS` crit, ephemeral/missing
→ warn, all refused before any read; anchor misses → `CHAIN_ANCHOR_NOT_FOUND`
warn; malformed citations → `CHAIN_CITATION_INVALID` warn.

**Fixture (pre-registered).** `corpus/fixtures/chain-r3.md` sha256 `06115f2f…`
— 22 real hops over the three archived inputs (pins A `9033857d…`, B
`6d8dbddd…`, C `e48fe70f…`): 17 resolved (line/quote anchors on these
non-Markdown exports — the `heading` kind is exercised by the gate's own
selftest; incl. cross-input co-anchors), 3 unresolved (real chain breaks marked, counted,
exempt), 2 `blocked-no-fetch` (the exports' own external chips コトバンク and
arxiv.org — exempt, never fetched). Ground truth: `RESOLVED_HOPS=17/22`,
CLEAN, exit 0. Broken-anchor control `corpus/fixtures/chain-r3-broken.md`
sha256 `b66222a1…`: hop 2 claims `resolved` on absent bytes → `anchor-missing`,
`RESOLVED_HOPS=1/2`, DRIFT, exit 1. Contract + provenance:
`chain-r3.README.md` (revised during the wave; current sha256 `72dbee4e…`, pins
the settled revision and both fixture shas). The dispatch named a JSONL pre-draft
(`chain-r3.jsonl`); the landed mode reads Markdown records, so its author
superseded and removed the JSONL rather than keep a second drifting copy. The
fixture README's own gate-free python check (run verbatim by the scribe):
`chain-r3.md: RESOLVED_HOPS=17/22 bad_hops=[]`;
`chain-r3-broken.md: RESOLVED_HOPS=1/2 bad_hops=['2']`.

**Measured at frozen gate sha256 `67daf85ecc49c4c7accbee9534c31b0734061b7f329e8de7a98254a57f9d6084`** (green; identical across 4+ samples):

```text
bash tools/research-gate.sh verify-chain corpus/fixtures/chain-r3.md --root ..
… 17 × CHAIN … verdict=match (at= 74,64,35,107,109,57,71,67,79,88,67,87,89,52,63,55,107)
… 5 × CHAIN observed=exempt (hops 18-22)
RESOLVED_HOPS=17/22
RESEARCH_GATE: CLEAN (hops=22 verified=17 exempt=5 anchor-missing=0 refused=0 invalid=0 findings=0 drift=0)
exit=0

bash tools/research-gate.sh verify-chain corpus/fixtures/chain-r3-broken.md --root ..
CHAIN hop=2 … observed=anchor-missing … verdict=mismatch
FINDING CHAIN_ANCHOR_NOT_FOUND severity=warn … nearest_line=53 context=The key distinction is between skill, teaching authority, and permission to act.
RESOLVED_HOPS=1/2
RESEARCH_GATE: DRIFT (hops=2 verified=1 exempt=0 anchor-missing=1 refused=0 invalid=0 findings=1 drift=1)
exit=1

bash tools/research-gate.sh --selftest
RESEARCH_GATE_SELFTEST: PASS (40 cases)
exit=0   # cases 1-30 byte-identical to the round-2 baseline; 31-40 chain cases

# regression at CHOUSA_NOW_EPOCH=1760000000
verify A/B/C → exit 1 each, stdout byte-identical to the r2 baseline; intake → exit 0 byte-identical; verify-claims claims-r2 → byte-identical, VERDICT_BEARING_CLAIMS=17/17; VERDICT_BEARING_EXPORTS=3/3
```

**Negative controls** (identical anchor miss):
`chain-fail-tampered` (anchor altered), `chain-fail-anchor-kinds` (invalid/
conflicting kinds), `chain-fail-out-of-corpus` (outside file refused unopened),
`chain-fail-external` (`CHAIN_SOURCE_EXTERNAL` crit), `chain-fail-invalid`
(missing anchor, unknown status), `chain-fail-counting` (`RESOLVED_HOPS=2/8`;
hops=8 verified=2 exempt=2 anchor-missing=1 refused=1 invalid=2),
`chain-fail-no-chain` (`CHAIN_ABSENT`); setup: no path / missing file → exit 2,
stdout empty.

**Honest boundaries.** A CLEAN `verify-chain` establishes anchor BYTES at a
reported first occurrence inside the allowed local roots — not semantics, not
line binding/uniqueness, not the exports' own truth. Exempt hops are counted
but prove nothing. Cross-input hops are co-anchors: they assert the bytes exist
in the target, never that the target input cites or endorses the source input
(`chain-r3.README.md`, "Honest boundaries"). Fixture anchors are byte controls,
not knowledge (the ACE numerals at hop 9 stay a round-2 boundary case, RJ-03).
No network primitive exists in the gate; URLs are refused before any read.
No older admitted entry was reverified; no non-author spot-check; no promotion.
Receipt identity remains open.

**Scribe defects (found during the wave; integration state):**
the earlier fixture-README sample (sha256 `25148a1b…`) pinned fixture sha
`6f73c8d0…` ≠ shipped `chain-r3.md` `06115f2f…` and settled revision
`7379b7ee…`; the author's revised README (sha256 `72dbee4e…`, the one the
receipts were cut against) pins `67daf85e…` and the correct fixture shas —
resolved in-wave. Two receipt nuances, found in the superseded
`235411Z` stamp and fixed by the receipts re-cut (integrated stamp `235623Z`):
control 1 now tampers to `…semanticsX` — a genuine miss, exit 1 — and the
adapter summary reads "2 fixtures re-derived; … hop 2 absent as expected".
Read the `235623Z` set.
Still flagged: `tools/research-gate.sh:75` banners `research-gate-r1`
(round-2 cosmetic residual); untracked `before.transcript` in the lane root is
another seat's scratch. The host `/tmp` quota defect recurred at round start
(scratch moved to `/home/vgpnk/.cache/chousa-r3/`); environment-owned.

**Not claimed.** `[PARENT: note/lesson/receipts/SKILL rows and the updated
`corpus/evidence/README.md` index landed in-wave — integrate what is in the
working tree at commit time; `corpus/README.md` coverage rows had not landed
at draft time — do not claim them unless they land.]`

### Evidence paths

`corpus/fixtures/chain-r3.md` · `corpus/fixtures/chain-r3-broken.md` ·
`corpus/fixtures/chain-r3.README.md` (revised, sha256 `72dbee4e…`) ·
`tools/research-gate.sh` (frozen revision `67daf85e…`) · scribe captures
`/home/vgpnk/.cache/chousa-r3/{before.txt, before-demo.txt, r2-baseline/,
now/, selftest-*.out, chain-run-*.txt}` · receipts
`corpus/evidence/chain-r3-20261015T235623Z-{fixture,gate,live,selftest}.log` ·
note `corpus/knowledge/chain-resolution-r3.md` (sha256 `9f16c7e7…`) · lesson
`corpus/lessons/2026-10-15-chain-hop-resolution.md` · `SKILL.md` gate rows ·
[PARENT] `corpus/README.md` coverage rows (if they land).