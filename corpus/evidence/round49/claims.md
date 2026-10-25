# Round 49 — frozen claims (chousa)

author: chousa L1 (hyaku run 7, agent `ChousaR49`)
date: 2026-10-25
freeze: before any round-49 candidate change and before any wave seat scores
base: `414a2ec6cde05a921dbdd9e02e7ae56b0db647ef` (`BASE_REV` in both counters)

No external fetch or network egress: L0 `8d77e6c1` remains open; every source
opened this round is an on-disk capture under the read-only
`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache`.
Round 48 completed the wave-4 quarantine-first duty (24/24 verdicts; closure
admitted), so round 49 is this lane's first package-adoption round under
addendum section 10. Two claims, distinct axes, causally separable: C1's
counter runs the tool on scratch mirrors of the BASE_REV registry and never
reads the lane's adopted entries; C2's counter reads lane bytes and never runs
the tool.

## R49-C1 — operability (lowest scored axis, 3/10; capability acquisition)

**Frozen predicate (one sentence, = the `c1-count.py` docstring):**
`tools/assimilate-rows.py` turns a frozen set of staged campaign entries into
an append block and rewritten entries that pass the fleet census on a scratch
mirror of the lane registry at BASE_REV, renumbering every cited staged id BY
DOCUMENT (held URL -> the lane's existing id; new URL -> the next lane id, in
ascending staged-id order, contiguous from the base maximum) with one
simultaneous substitution, appending exactly the rows the entries cite, each
with status `mined`, the given opened date, a census-valid recheck and a
`used-by` naming exactly the citing entries; it reports the section-10 id
collisions with the 0-3-space pattern (an indented registry row collides);
and it rewrites an escaped-pipe staged cell so the appended row parses as 11
cells. Three package sets (A: this round's theme, B: a collision-chain entry,
C: an entry with held rows) plus the GUARD and PIPE fixtures must all pass.

- Counting command: `python3 corpus/evidence/round49/c1-count.py` (tool
  interface frozen in its docstring; package inputs sha256-pinned; a changed
  package exits 2).
- Before (`controls/c1-before.txt`): `TOOL=absent C1=FAIL` exit 1.
- Do-nothing control (`controls/copy-tool.py`, same interface: byte-exact
  append, unchanged entries, identity map, column-zero collision grep):
  `SETS_PASS=0/3`, `GUARD ... COLLISIONS=[] FAIL`, `PIPE ... CELLS=13 FAIL`,
  census E01/E03/E04/E09 on every set, `C1=FAIL` exit 1.
- Target: `SETS_PASS=3/3`, `GUARD -> PASS`, `PIPE -> PASS`, `C1=PASS` exit 0.
- Kill rule: any set, GUARD or PIPE leg failing, a census E-code on any
  mirror, or a harness/env exit 2 on the measured commit means C1 fails.
- Tag: plumbing (QUALITY 64). Capability row only if the after-measurement
  passes in this round.

## R49-C2 — depth (sourced; the assimilation theme)

**Frozen predicate (one sentence, = the `c2-count.py` docstring):**
the theme "a citation index's data is a derived artefact" is adopted BY
DOCUMENT as the two lane entries `corpus/knowledge/aggregator-vs-source-r36.md`
and `corpus/knowledge/citation-count-semantics-r37.md`; of the nine staged
documents they rest on, at least seven are BOUND — exactly one lane Registry
row carries the document's URL, that row is new since BASE_REV, `mined`,
opened 2026-10-25, its `used-by` names the citing entry, and the entry carries
a `source: <that id> — <url>` line — and every other one is REFUSED (no lane
row, no `source:` line, and a `refused-doc` line naming its URL in
`corpus/lessons/round-49.md`); every `S###` token in either entry is a bound
id or the held S003; `corpus/evidence/round49/spans.tsv` (derived by
`build-spans.py`) carries at least two quote rows per bound id, each quote at
most 25 whitespace words and 160 characters, inside its span file, inside the
citing entry and inside the round-49 lesson, each span file the exact slice of
the capture text form at the recorded offset whose file digest is the recorded
one, and longer than its quote; every `char N` in a bound row's `anchor` cell
(at least one) is the offset of a quote of that id; both entries exit 0 under
`tools/inference-ground.py` with this round's spans; and the lesson carries a
re-check verdict line for each absent-defect-register row on a theme URL,
with no bound document whose verdict is `fabricated` or `unverifiable`.

- Counting command: `python3 corpus/evidence/round49/c2-count.py` (and
  `--lane-only`).
- Before (`controls/c2-before.txt`): `ENTRIES=0/2 BOUND=0/9
  INFERENCE_GROUNDED=0/2 QUARANTINE_VERDICTS=0/5 C2=FAIL` exit 1.
- Control: the two staged entries copied unchanged into a scratch root with
  the lane registry: `ENTRIES=2/2 BOUND=0/9 REF_ID_UNBOUND=11 C2=FAIL` — the
  staged ids S087–S103 name lane rows of OTHER documents.
- Target: `C2=PASS` exit 0 (`BOUND>=7` with `BOUND+REFUSED=9`).
- Kill rule: fewer than seven bound documents, any unbound token, any quote
  leg short of n/n, an anchor not at a located quote offset, either entry
  failing `inference-ground`, a missing register verdict, or a bound document
  with a `fabricated`/`unverifiable` verdict means C2 fails.
- Tag: ground (QUALITY 64). Province, QUALITY bar and coverage-map credit are
  judged per entry in the lesson Gate; the counter measures binding and
  presence, not entailment.

## Admission rule

Each claim is admitted only if its frozen counter meets the target on the
landed commit and no owned axis is harmed. Neither counter's pass overrules
the external closure's spot-check of the Gate verdicts.
