# Round 53 — frozen claims (chousa)

author: chousa L1 (hyaku run 9, agent `ChousaR53`)
date: 2026-10-26
freeze: before any round-53 wave seat exists or scores; the C1 candidate
(`tools/assimilate-rows.py` v4 and its self-test cases) is committed after this file
base: `5b550133d79bc09c82d8965cce2e48c2598b8c3e` (`BASE_REV` in both counters; the round-52 closure tip)

No external fetch or network egress: L0 `8d77e6c1` remains open; every source
opened this round is an on-disk capture under the read-only
`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache`.
Two claims, two distinct axes, causally separable: C1's counter generates its
own packages and reads the read-only campaign package and the registry at
`BASE_REV` (never the lane's current registry, entries or spans); C2's counter
reads lane bytes and the capture cache and never runs the adopter. C2 can be
landed with the round-52 adopter: its control `TOOLED` shows the base adopter
binds all five documents mechanically (the twin label is a stdout/renumber
label, not a row), so C2 does not need C1.

The L1 checked, before this freeze, that the round-52 W1 scratch patch
(`.ufo/waves/round-52/w1/R52ExecAdopterTwin.md` section 3) applied to the base
tool reaches the C1 target once (a feasibility check, not a measurement; no
seat has scored).

What the round-52 closure routed (`corpus/lessons/round-52-verifier-spotcheck.md`
section 6) and how this round meets it: (4) adopter twin-id `held` label and
refusal ordering — this is C1; (3) representation variance belongs in the
FROZEN counter — C1's generator randomises registry-row indentation (0–3
spaces), the heading separator (space or tab), the URL scheme, a trailing `/`
and the host case, all inside the census URL identity; (1), (2), (5) and the
anchored `correction:` check are ordinary routed work outside the claims,
disclosed in the report.

## R53-C1 — operability (lowest scored axis, 3/10; capability extension)

**Frozen predicate (one sentence, = the `c1-count.py` docstring):**
`tools/assimilate-rows.py`, run as an ordinary command with `--entry`, labels a
cited staged row `held` in `renumber.tsv` only when a lane Registry row already
carries its URL and `twin` when an earlier-cited staged row of the same run was
minted a lane id for that URL (the same lane id, nothing appended), and its
count line carries `HELD=<held rows>` and `TWIN=<twin rows>`; it validates the
recheck of every cited staged row, held and twin rows included, and refuses
(exit 1, a stderr line starting `REFUSED <staged id>: recheck`, no
`renumber.tsv` and no `append.md`) when one has no leading calendar-valid date
or `NNd`; a registry it cannot continue from (no `## Registry` heading, or an
`S###` row outside the Registry section) is refused with exit 1 and every
registry `REFUSED` line printed before any entry `REFUSED` line, and is
refused also when no `--entry` is given, while a sound registry with no
`--entry` still exits 0 — counted as legs over packages generated at counting
time from fresh random ids, hosts, paths, entry names and recheck values with
randomised representation (0-3 leading spaces on registry rows, `##` followed
by a space or a tab, http or https, a trailing `/`, an upper-case host), plus
REAL (the three round-53 staged entries of the read-only campaign package
against the registry at BASE_REV: S134 S185 S186 S190 S193 append as S117
S118 S119 S120 S121, S195 is `twin` of S118, `HELD=0 TWIN=1`) and REGRESS (the
round-50 pinned self-test passes with its pinned digest and the round-51 frozen
counter prints `LEGS=5/5` for the same tool).

- Counting command: `python3 corpus/evidence/round53/c1-count.py` (legs TWIN,
  HELD, MIX, RECHECK, ORDER, NOENTRY, REAL, REGRESS; `--per-leg K` packages per
  generated leg, default 3; `--seed N`; `--work DIR`; `--tool PATH`). The REAL
  leg is pinned: `pin()` over the campaign `SOURCES.append.md` and the three
  staged entries must equal `8e6484ed…689b`, else exit 2.
- Before (`controls/c1-before.txt`, the lane tool at `BASE_REV`): `LEGS=1/8`
  (REGRESS only), `C1=FAIL` exit 1 on three unseeded runs and `--seed 7`. On
  the real package the base tool labels S195 `held` (`CITED=6 APPEND=5 HELD=1`)
  although no Registry row carries its URL.
- Controls (`controls/build-c1-controls.py --seed 53`, same receipt): BASE 1/8;
  CONST (prints nothing, exit 0) 0/8; REFUSE (always refuses on a registry
  line, exit 1) 0/8; RELABEL (base with only the same-run label and a `TWIN=`
  count, the cheapest partial patch) 5/8 — RECHECK, ORDER, NOENTRY fail;
  ALLTWIN (every non-append row labelled `twin`) 2/8.
- Target: `LEGS=8/8`, `C1=PASS` exit 0, on three independent unseeded runs and
  once with `--seed 7`.
- Kill rule: any leg failing in any of those runs, or an `ENV_CHANGED` exit 2,
  means C1 fails.
- Tag: plumbing (QUALITY 64). Capability row only if the after-measurement
  passes in this round.

## R53-C2 — depth (sourced; the section-10 search-record theme, continued into its instruments)

**Frozen predicate (one sentence, = the `c2-count.py` docstring):**
the search-record theme continues BY DOCUMENT into the search-record
instruments as the lane entries `corpus/knowledge/search-tracking-record-r40.md`
(the JMLA PRISMA 2020 / PRISMA-S common-questions paper),
`corpus/knowledge/western-instrument-alignment-r50.md` (Cochrane Handbook
chapter 4 and the national centre's issued quality-control guideline) and
`corpus/knowledge/quality-control-guideline-issued-text-r48.md` (the issued
guideline, its release notice and the 2019 NMPA guideline copy), of which at
least two exist and every one that does not is named by a `refused-entry
<path>` line in `corpus/lessons/round-53.md`; of the five documents they rest
on, at least three are BOUND — exactly one lane Registry row whose FIRST
source-cell URL is the document's URL, that row new since BASE_REV, `mined`,
opened 2026-10-26, its `used-by` naming exactly the existing entries citing it
(at least one), and every existing citing entry carrying a `source: <that id>
— <url>` line — and every other one is REFUSED (no lane row, no `source:` line
naming its URL in any existing entry, and a `refused-doc` line naming its URL
in the round-53 lesson); no `S###` token appears in the existing entries
except a bound id; at BASE_REV no `corpus/knowledge` file held `tracking
record`, `information specialist` or `质量控制指南`, and each existing entry
holds its own term (in that order); `corpus/evidence/round53/spans.tsv`
(derived by `build-spans.py`) carries at least three quote rows per bound id,
each quote at most 25 whitespace words and 160 characters, inside its span
file, inside the citing entry and inside the round-53 lesson, each span file
the exact slice of the capture text form at the recorded offset whose file
digest is the recorded one, and longer than its quote; the round-51
`quote-substance-check.py` exits 0 on the manifest; every `char N` in a bound
row's `anchor` cell (at least one) is the offset of a quote of that id; every
existing entry exits 0 under `tools/inference-ground.py` with this round's
spans; and the lesson carries a re-check verdict line for each
absent-defect-register row on a theme URL (the sweep prints how many: 0 at the
freeze), with no bound document whose verdict is `fabricated` or
`unverifiable`.

- Counting command: `python3 corpus/evidence/round53/c2-count.py` (and
  `--lane-only`).
- Before (`controls/c2-before.txt`): `ENTRIES=0/3 BOUND=0/5 SUBSTANCE=FAIL
  C2=FAIL` exit 1.
- Controls (`controls/build-c2-controls.py`, output `controls/c2-controls.txt`):
  the three staged entries copied unchanged — `REF_ID_UNBOUND=12 BOUND=0/5
  C2=FAIL`; the same entries rewritten by the base adopter with its append block
  inserted, no quote, span or lesson — `BOUND=5/5 REF_ID_UNBOUND=4
  ANCHOR_BOUND=0/5 C2=FAIL`. Binding alone is mechanical (the TOOLED control
  binds all five); the claim's substance is the located quotes, their spans,
  anchors and the inference ground.
- Target: `C2=PASS` exit 0 (`ENTRIES>=2`, `BOUND>=3`, `BOUND+REFUSED=5`).
- Kill rule: fewer than two existing entries, an entry neither existing nor
  `refused-entry`, fewer than three bound documents, any unbound S-token, any
  quote leg short of n/n, `SUBSTANCE=FAIL`, an anchor not at a located quote
  offset, any existing entry failing `inference-ground`, or a bound document
  with a `fabricated`/`unverifiable` verdict means C2 fails.
- Tag: ground (QUALITY 64). Province, QUALITY bar and coverage-map credit are
  judged per entry in the lesson Gate; the counter measures binding and
  presence, not entailment (the round-50/51/52 limit, restated before data).
  Expansion credit is per document, not per entry; a document a lane entry
  already holds earns none.

## Admission rule

Each claim is admitted only if its frozen counter meets the target on the
landed commit and no owned axis is harmed. Neither counter's pass overrules the
external closure's spot-check of the Gate verdicts. A rule changed after any
seat has scored is not the claim's rule; any post-freeze change is disclosed in
`claims-erratum.md`.
