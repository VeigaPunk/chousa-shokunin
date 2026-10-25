# Round 50 — frozen claims (chousa)

author: chousa L1 (hyaku run 7, agent `ChousaR50`)
date: 2026-10-25
freeze: before any round-50 candidate change lands and before any wave seat scores
base: `3c51da77b3696ed884c943548ec4b4006e3ca528` (`BASE_REV` in the C2 counter; the round-49 closure tip)

No external fetch or network egress: L0 `8d77e6c1` remains open; every source
opened this round is an on-disk capture under the read-only
`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache`.
Two claims, distinct axes, causally separable: C1's counter runs the tool
`--selftest` on counter-owned pinned fixtures (`c1-fixtures/`) and never reads
the lane's entries or registry rows; C2's counter reads lane bytes and the
capture cache and never runs the tool. Both counters embed what round 49's
closure routed: a perturbed-input leg for a capability counter, and the span
substance floor for a quote counter (QUALITY 72; verifier spot-check defect 3).

## R50-C1 — operability (lowest scored axis, 3/10; capability extension)

**Frozen predicate (one sentence, = the `c1-count.py` docstring):**
`tools/assimilate-rows.py --selftest [--fixtures DIR] [--expected FILE]` runs
the adopter on an isolated fixture package and compares the observed finding
lines with the `findings` list of an expected file, so that on the counter's
own pinned fixture package (`corpus/evidence/round50/c1-fixtures/`, digest
pinned) it exits 0 with `SELFTEST=PASS` and 26 findings, and on each of six
perturbed copies it exits 1 and names the perturbed finding in a `DIFF` line
(P1 indented registry row removed, P2 a held URL changed, P3 the escaped pipe
removed, P4 a recheck made unparseable, P5 one expected finding dropped, P6 a
cited id removed from an entry), and an unparseable expected file exits 2 with
`SELFTEST=ERROR`; and the lane default (`python3 tools/assimilate-rows.py
--selftest`, no flags) also exits 0 PASS; and the round-49 counter
`corpus/evidence/round49/c1-count.py --tool <tool>` still prints `C1=PASS`.

- Counting command: `python3 corpus/evidence/round50/c1-count.py`
  (finding grammar and fixture layout frozen in its docstring).
- Before (`controls/c1-before.txt`, the base tool copied to
  `controls/tool-before.py`): `BASELINE=FAIL rc=2`, `PERTURB_PASS=0/6`,
  `LEGS=2/5`, `C1=FAIL` exit 1.
- Do-nothing controls with the same interface: `controls/echo-tool.py`
  (prints the expected findings back and the real fixture digest, exit 0) —
  passes the baseline, `PERTURB_PASS=0/6`, `C1=FAIL`; `controls/const-tool.py`
  (`SELFTEST=PASS`, exit 0 whatever it is given) — `BASELINE=FAIL`,
  `PERTURB_PASS=0/6`, `C1=FAIL`.
- Target: `LEGS=5/5`, `PERTURB_PASS=6/6`, `C1=PASS` exit 0.
- Kill rule: any leg failing, the fixtures digest differing from the pin
  (exit 2), or a perturbation that exits other than 1 means C1 fails.
- Tag: plumbing (QUALITY 64). Capability-row update only if the
  after-measurement passes in this round.

## R50-C2 — depth (sourced; the assimilation theme)

**Frozen predicate (one sentence, = the `c2-count.py` docstring):** the theme
"what a Chinese citation-checking feature compares, and which of CNKI's
manuals document it" is adopted BY DOCUMENT as the three lane entries
`corpus/knowledge/cnki-citation-check-r40.md`,
`corpus/knowledge/citation-matching-semantics-r41.md` and
`corpus/knowledge/istic-citation-verification-r39.md`; of the four staged
documents they rest on, at least three are BOUND — exactly one lane Registry
row carries the document's URL, that row is new since BASE_REV, `mined`,
opened 2026-10-25, its `used-by` names exactly the entries citing it, and
every citing entry carries a `source: <that id> — <url>` line — and the other
one is REFUSED (no lane row, no `source:` line, and a `refused-doc` line naming
its URL in `corpus/lessons/round-50.md`); no `S###` token appears in the
entries except a bound id; at BASE_REV no `corpus/knowledge` file held 引文核对
or 引证检索, and each entry holds its own term; `spans.tsv` (derived by
`build-spans.py`) carries at least three quote rows per bound id, each quote
at most 25 whitespace words and 160 characters, inside its span file, inside
the citing entry and inside the round-50 lesson, each span file the exact slice
of the capture text form at the recorded offset whose file digest is the
recorded one, and longer than its quote; `quote-substance-check.py` exits 0 on
the manifest; every `char N` in a bound row's `anchor` cell (at least one) is
the offset of a quote of that id; all three entries exit 0 under
`tools/inference-ground.py`; and the lesson carries a re-check verdict line for
each absent-defect-register row on a theme URL (the sweep prints how many
there are), with no bound document whose verdict is `fabricated` or
`unverifiable`.

- Counting command: `python3 corpus/evidence/round50/c2-count.py` (and
  `--lane-only`).
- Before (`controls/c2-before.txt`): `ENTRIES=0/3 BOUND=0/4 NEW_GROUND=0/3
  INFERENCE_GROUNDED=0/3 C2=FAIL` exit 1.
- Controls (`controls/build-c2-controls.py`): the three staged entries copied
  unchanged — `REF_ID_UNBOUND=15`, `BOUND=0/4`, `C2=FAIL`; the same entries
  rewritten by the adopter with its append block inserted but no quote, span or
  lesson — `BOUND=3/4`, `REF_ID_UNBOUND=8`, `QUOTE_ROWS=0`, `C2=FAIL`.
- Target: `C2=PASS` exit 0 (`BOUND>=3`, `BOUND+REFUSED=4`).
- Kill rule: fewer than three bound documents, any unbound S-token, any quote
  leg short of n/n, `SUBSTANCE=FAIL`, an anchor not at a located quote offset,
  any entry failing `inference-ground`, a missing register verdict, or a bound
  document with a `fabricated`/`unverifiable` verdict means C2 fails.
- Tag: ground (QUALITY 64). Province, QUALITY bar and coverage-map credit are
  judged per entry in the lesson Gate; the counter measures binding and
  presence, not entailment.
- Known counter limit, declared before data: the counter cannot tell a
  re-grounded quote that supports its bullet from one that merely occurs in
  the capture; the Gate reader and the closure judge that.

## Admission rule

Each claim is admitted only if its frozen counter meets the target on the
landed commit and no owned axis is harmed. Neither counter's pass overrules
the external closure's spot-check of the Gate verdicts.
