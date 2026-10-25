# Round 51 — frozen claims (chousa)

author: chousa L1 (hyaku run 7, agent `ChousaR51`)
date: 2026-10-25
freeze: before any round-51 candidate change lands and before any wave seat scores
base: `9ec1751a24231e899ceea4688e21c8edf6046d35` (`BASE_REV` in the C2 and C3 counters; the round-50 closure tip)

No external fetch or network egress: L0 `8d77e6c1` remains open; every source
opened this round is an on-disk capture under the read-only
`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache`.
Three claims, three distinct axes, causally separable: C1's counter runs the
adopter on packages it generates itself and reads no lane entry or registry row;
C2's counter reads lane bytes and the capture cache and never runs the tool;
C3's counter reads `SCORECARD.md`, `SHONEN.md` and the file tree only. What the
round-50 closure routed is embedded: the nonce form for a capability counter
(spot-check routed defect 2), unique seat names (routed defect 3, checked by
`corpus/evidence/round50/name-collision-check.py` before every `.ready` file),
and the revision pin (routed defect 1) is closed outside the claims as ordinary
routed work, disclosed in the report.

## R51-C1 — operability (lowest scored axis, 3/10; capability extension)

**Frozen predicate (one sentence, = the `c1-count.py` docstring):**
`tools/assimilate-rows.py`, run as an ordinary command (not `--selftest`) on
packages the counter GENERATES at counting time from fresh random hosts and ids,
(S) cites only the ids on the entries' `source:` lines — an id an entry mentions
only in its body is neither renumbered nor appended, is left in the entry text
unchanged and is listed in `bodyonly.tsv` (`entry<TAB>staged id`) and as
`BODYONLY=<n>` on stdout — while `--cites all` keeps the round-50 behaviour;
(D1) takes a staged row's document identity from its source cell AFTER the
escaped-pipe rewrite; (D2) reads a registry row's source cell with the
escaped-pipe splitter; (D3) refuses (exit 1, a `REFUSED` stderr line, no
`renumber.tsv` and no `append.md`) a registry that has no `## Registry` heading
or that carries an `S###` row outside the Registry section, and on a well-formed
registry appends from the maximum id + 1; and the round-50 pinned fixture
package, run as `--selftest --fixtures <pinned> --expected <pinned> --cites all`,
still passes with 26 findings and its pinned digest, and the lane default
`--selftest` passes.

- Counting command: `python3 corpus/evidence/round51/c1-count.py` (five legs:
  SELFTEST_DEFAULT, LEGACY_ALL, SOURCE_ONLY, PIPE_IDENTITY, REGISTRY_STRUCTURE).
- Before (`controls/c1-lane-before.txt`, the lane tool at `BASE_REV`): `LEGS=1/5`,
  `LEGACY_ALL=FAIL rc=2` (no `--cites`), `SOURCE_ONLY=FAIL` (body-only id
  renumbered, 2 rows appended), `PIPE_IDENTITY=FAIL d1=no d2=no`,
  `REGISTRY_STRUCTURE=FAIL 1/4`, `C1=FAIL` exit 1.
- Do-nothing controls with the same interface (`controls/c1-before.txt`):
  `tool-before.py` (the base tool) `LEGS=1/5`; `echo-tool.py` (prints the
  round-50 expected findings back; passes LEGACY_ALL) `LEGS=2/5`;
  `const-tool.py` (`SELFTEST=PASS` for anything) `LEGS=1/5`; `flag-noop-tool.py`
  (the base tool that accepts `--cites` and ignores it) `LEGS=2/5`. With `--tool`
  the SELFTEST_DEFAULT leg is skipped and counted as passing, so every control
  starts with one free leg; none reaches 3/5.
- Target: `LEGS=5/5`, `C1=PASS` exit 0, on at least three independent runs of the
  counter (fresh nonces) and with `--seed` fixed in one of them.
- Kill rule: any leg failing, or the round-50 fixtures digest differing from the
  pin (exit 2), means C1 fails. Not part of the predicate (disclosed): the
  frozen round-49 and round-50 counters were written for the all-token behaviour
  and are one-shot (SKILL.md Gates); the report prints what they print at the
  landed tool, and `LEGACY_ALL` is what preserves their behaviour.
- Tag: plumbing (QUALITY 64). Capability-row update only if the after-measurement
  passes in this round.

## R51-C2 — depth (sourced; the assimilation theme)

**Frozen predicate (one sentence, = the `c2-count.py` docstring):** the theme
"what a Japanese or a Chinese systematic-review search record must carry" is
adopted BY DOCUMENT as the three lane entries
`corpus/knowledge/japanese-search-record-r38.md`,
`corpus/knowledge/chinese-search-record-r39.md` and
`corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md`; of the
seven staged documents they rest on, at least five are BOUND — exactly one lane
Registry row carries the document's URL, that row is new since BASE_REV,
`mined`, opened 2026-10-25, its `used-by` names exactly the entries citing it,
and every citing entry carries a `source: <that id> — <url>` line — and every
other one is REFUSED (no lane row, no `source:` line, and a `refused-doc` line
naming its URL in `corpus/lessons/round-51.md`); no `S###` token appears in the
entries except a bound id; at BASE_REV no `corpus/knowledge` file held 検索式,
検索期間 or 检索策略, and each entry holds its own term (検索式, 检索策略, 検索期間
respectively); `spans.tsv` (derived by `build-spans.py`) carries at least three
quote rows per bound id, each quote at most 25 whitespace words and 160
characters, inside its span file, inside the citing entry and inside the
round-51 lesson, each span file the exact slice of the capture text form at the
recorded offset whose file digest is the recorded one, and longer than its
quote; `quote-substance-check.py` exits 0 on the manifest; every `char N` in a
bound row's `anchor` cell (at least one) is the offset of a quote of that id;
all three entries exit 0 under `tools/inference-ground.py`; and the lesson
carries a re-check verdict line for each absent-defect-register row on a theme
URL (the counter prints how many there are: 6 at the freeze — S104 S105 S111
S112 S114 S120), with no bound document whose verdict is `fabricated` or
`unverifiable`.

- Counting command: `python3 corpus/evidence/round51/c2-count.py` (and
  `--lane-only`).
- Before (`controls/c2-before.txt`): `ENTRIES=0/3 BOUND=0/7 NEW_GROUND=0/3
  INFERENCE_GROUNDED=0/3 QUARANTINE_VERDICTS=0/6 C2=FAIL` exit 1.
- Controls (`controls/build-c2-controls.py`, output `controls/c2-controls.txt`):
  the three staged entries copied unchanged — `REF_ID_UNBOUND=30`, `BOUND=0/7`,
  `C2=FAIL`; the same entries with every non-`source:` id stripped and rewritten
  by the adopter with its append block inserted but no quote, span or lesson —
  `BOUND=7/7`, `REF_ID_UNBOUND=0`, `QUOTE_ROWS=0`, `C2=FAIL`.
- Target: `C2=PASS` exit 0 (`BOUND>=5`, `BOUND+REFUSED=7`).
- Kill rule: fewer than five bound documents, any unbound S-token, any quote leg
  short of n/n, `SUBSTANCE=FAIL`, an anchor not at a located quote offset, any
  entry failing `inference-ground`, a missing register verdict, or a bound
  document with a `fabricated`/`unverifiable` verdict means C2 fails.
- Tag: ground (QUALITY 64). Province, QUALITY bar and coverage-map credit are
  judged per entry in the lesson Gate; the counter measures binding and
  presence, not entailment (the round-50 limit, restated before data).

## R51-C3 — calibration

**Frozen predicate (one sentence, = the `c3-count.py` docstring):** every
repo-path pointer a self-assessment names resolves at the tip, where the
self-assessment is the evidence-pointer cell of every data row of every
`## Capabilities` table of `SCORECARD.md` plus every indented evidence line of
`SHONEN.md`, a pointer resolves when `<lane>/<pointer>` is a non-empty file or a
directory holding a file or a later `correction: SCORECARD.md:<row line>
<pointer> -> <path>` line names that row and an existing non-empty `<path>`, and
neither the capability-row count nor the pointer count is below its value at
BASE_REV.

- Counting command: `python3 corpus/evidence/round51/c3-count.py`.
- Before (`controls/c3-before.txt`): `CAP_ROWS=36 POINTERS=74 DANGLING=8 C3=FAIL`
  exit 1 (SCORECARD.md:1843 1973 1974 2073 2074 2616; SHONEN.md:10 12).
- Controls (`controls/build-c3-controls.py`, output `controls/c3-controls.txt`):
  one blanket `correction:` line — `DANGLING=8`; the dangling rows and lines
  deleted — `CAP_ROWS=30`, `POINTERS=50`; zero-byte files at the pointer names —
  `DANGLING=8`; all `C3=FAIL`.
- Target: `DANGLING=0`, `CAP_ROWS>=36`, `POINTERS>=74`, `C3=PASS` exit 0.
- Kill rule: any dangling pointer, a lower row or pointer count, means C3 fails.
- Tag: plumbing (calibration of the lane's own self-assessment against the tree).
  Named limit declared before data: existence, not truth — a pointer to a file
  that exists but does not show the claimed behaviour passes.

## Admission rule

Each claim is admitted only if its frozen counter meets the target on the
landed commit and no owned axis is harmed. Neither counter's pass overrules the
external closure's spot-check of the Gate verdicts.
