# Round 52 — frozen claims (chousa)

author: chousa L1 (hyaku run 9, agent `ChousaR52`)
date: 2026-10-26
freeze: before any round-52 wave seat exists or scores; the C1 candidate
`tools/capture-text.py` is committed after this file
base: `00f8c7f5272a1d98b6d34913985fa4537e00aaf9` (`BASE_REV` in the C2 counter; the round-51 closure tip)

No external fetch or network egress: L0 `8d77e6c1` remains open; every source
opened this round is an on-disk capture under the read-only
`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache`.
Two claims, two distinct axes, causally separable: C1's counter generates its
own `.docx` packages and reads one pinned capture, never a lane entry or row;
C2's counter reads lane bytes and the capture cache through the round-52 span
builder, which carries its OWN `.docx` reader (`build-spans.py` `docx_text`),
and never runs `tools/capture-text.py`. Both readers implement the one rule
written in the C1 predicate; on the NIPH capture they print the same 19682
characters (checked before the freeze; not a predicate).

What the round-51 closure routed (`corpus/lessons/round-51-verifier-spotcheck.md`
section 6) and how this round meets it: (1) a capability counter with no fixed
directory or file names — C1 draws every package, member and file name from
fresh randomness and honours `TMPDIR`/`--work`; (3) the NIPH `.docx` refusal
was a capture-form refusal — C1 builds the zip-member form as a lane tool and
C2 re-grounds the document in it; (2), (4), (5) are ordinary routed work
outside the claims, disclosed in the report.

## R52-C1 — operability (lowest scored axis, 3/10; capability acquisition)

**Frozen predicate (one sentence, = the `c1-count.py` docstring):**
`tools/capture-text.py RAW` prints, as UTF-8 on stdout with exit 0, the TEXT
FORM of an OOXML WordprocessingML capture — the main document part is the
target of the `_rels/.rels` relationship whose Type ends in `/officeDocument`
(a leading `/` stripped), never a fixed member name; in that part, in document
order, a `w:t` element emits its text (XML entities decoded), a `w:tab`,
`w:br` or `w:cr` whose parent is a `w:r` emits a tab, a newline, a newline,
the end of every `w:p` (nested ones included) emits a newline, everything
inside an `mc:Fallback` emits nothing, and nothing else emits text (so
`w:delText`, `w:instrText` and the `w:tab` stops of `w:pPr/w:tabs` are
dropped); `capture-text.py RAW --locate QUOTE` prints one line
`LOCATED count=<n> offset=<first offset in that text form or -1>` and exits 0
only when n == 1, else 1; and a RAW that is not a zip, or a zip with no
officeDocument relationship or whose target is missing, is refused with exit
2, a stderr line starting `REFUSED` and nothing on stdout — counted as nine
legs over packages generated at counting time from fresh random text, member
names and file names, plus the pinned NIPH capture (`REAL`: its text form holds
`SRにおける文献検索期間について明記する` exactly once and `--locate` agrees).

- Counting command: `python3 corpus/evidence/round52/c1-count.py` (legs PARAS,
  RUNS_ENTITIES, REVISIONS, LAYOUT, ALTCONTENT, MAIN_PART, LOCATE, REFUSE,
  REAL; `--per-leg K` packages per leg, default 3; `--seed N`; `--work DIR`).
- Before (`controls/c1-before.txt`, the lane at `BASE_REV`, exported by
  `git archive`): `tools/capture-text.py` absent, `LEGS=0/9 C1=FAIL` exit 1.
- Do-nothing and cheap controls with the same interface (same receipt):
  `controls/naive-tool.py` (fixed member `word/document.xml`, newline at
  `</w:p>`, tab at every `<w:tab…/>`, tag strip, `html.unescape`) `LEGS=4/9`
  (PARAS, RUNS_ENTITIES, LOCATE, REAL); `controls/cache-txt-tool.py` (the raw
  bytes decoded as UTF-8 with replacement, what the cache `.txt` sidecar is)
  `LEGS=0/9`; `controls/const-tool.py` (prints nothing, exit 0) `LEGS=0/9`.
- Target: `LEGS=9/9`, `C1=PASS` exit 0, on three independent runs (fresh
  nonces) and once with `--seed` fixed.
- Kill rule: any leg failing in any of those runs, or the pinned capture's
  digest differing (REAL fails), means C1 fails.
- Tag: plumbing (QUALITY 64). Capability row only if the after-measurement
  passes in this round.

## R52-C2 — depth (sourced; the section-10 search-record theme, continued)

**Frozen predicate (one sentence, = the `c2-count.py` docstring):** the
search-record theme continues BY DOCUMENT as the three lane entries
`corpus/knowledge/japanese-search-record-niph-form-r52.md` (the 国立保健医療科学院
submission form, a `.docx` refused in round 51 for its capture form),
`corpus/knowledge/japanese-prisma-item-wording-r40.md` (the Japanese PRISMA
2020 checklist translation, read at its web-archive copy) and
`corpus/knowledge/chinese-prisma-s-reception-r52.md` (the 梅斯医学 PRISMA-S
interpretation page and the 中国全科医学 PRISMA 2020 checklist page); of the
four documents they rest on, at least three are BOUND — exactly one lane
Registry row whose FIRST source-cell URL is the document's URL, that row new
since BASE_REV, `mined`, opened 2026-10-26, its `used-by` naming exactly the
entries citing it, and every citing entry carrying a `source: <that id> —
<url>` line — and every other one is REFUSED (no lane row, no `source:` line,
and a `refused-doc` line naming its URL in `corpus/lessons/round-52.md`); no
`S###` token appears in the entries except a bound id; at BASE_REV no
`corpus/knowledge` file held 文献検索期間, 完全な検索戦略 or 检索报告清单, and each
entry holds its own term (in that order); `corpus/evidence/round52/spans.tsv`
(derived by `build-spans.py`, whose zip raws read as the round-52 `.docx`
text form) carries at least three quote rows per bound id, each quote at most
25 whitespace words and 160 characters, inside its span file, inside the citing
entry and inside the round-52 lesson, each span file the exact slice of the
capture text form at the recorded offset whose file digest is the recorded
one, and longer than its quote; the round-51 `quote-substance-check.py` exits
0 on the manifest; every `char N` in a bound row's `anchor` cell (at least
one) is the offset of a quote of that id; all three entries exit 0 under
`tools/inference-ground.py` with this round's spans; and the lesson carries a
re-check verdict line for each absent-defect-register row on a theme URL (1
at the freeze, S120), with no bound document whose verdict is `fabricated` or
`unverifiable`.

- Counting command: `python3 corpus/evidence/round52/c2-count.py` (and
  `--lane-only`).
- Before (`controls/c2-before.txt`): `ENTRIES=0/3 BOUND=0/4 NEW_GROUND=0/3
  INFERENCE_GROUNDED=0/3 QUARANTINE_VERDICTS=0/1 C2=FAIL` exit 1.
- Controls (`controls/build-c2-controls.py`, output `controls/c2-controls.txt`):
  the three staged entries copied unchanged to the lane paths —
  `REF_ID_UNBOUND=31 BOUND=0/4 C2=FAIL`; the same entries rewritten by the
  lane adopter with its append block inserted, no quote, span or lesson —
  `BOUND=0/4 C2=FAIL`.
- Target: `C2=PASS` exit 0 (`BOUND>=3`, `BOUND+REFUSED=4`).
- Kill rule: fewer than three bound documents, any unbound S-token, any quote
  leg short of n/n, `SUBSTANCE=FAIL`, an anchor not at a located quote offset,
  any entry failing `inference-ground`, a missing register verdict, or a bound
  document with a `fabricated`/`unverifiable` verdict means C2 fails.
- Tag: ground (QUALITY 64). Province, QUALITY bar and coverage-map credit are
  judged per entry in the lesson Gate; the counter measures binding and
  presence, not entailment (the round-50/51 limit, restated before data).
  Expansion credit is per document, not per entry.

## Admission rule

Each claim is admitted only if its frozen counter meets the target on the
landed commit and no owned axis is harmed. Neither counter's pass overrules the
external closure's spot-check of the Gate verdicts. A rule changed after any
seat has scored is not the claim's rule; any post-freeze change is disclosed in
`claims-erratum.md`.
