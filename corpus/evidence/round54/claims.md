# Round 54 — frozen claims (chousa)

author: chousa L1 (hyaku run 9, agent `ChousaR54`)
date: 2026-10-26
freeze: before any round-54 wave seat exists or scores; the C1 candidate
(`tools/capture-text.py` with the OLE `.doc` text form) is committed after this file
base: `c49ffc6ce1c3de87c1dfa96856239ed7274bf07b` (`BASE_REV`; the round-53 tip, `master` at round start)

No external fetch or network egress: L0 `8d77e6c1` remains open; every source
opened this round is an on-disk capture under the read-only
`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache`.
Two claims, two distinct axes, causally separable: C1's counter generates its
own documents, reads five pinned OLE captures and runs the tool; it never
reads the lane's registry, entries or spans. C2's counter reads lane bytes and
the capture cache and never runs `tools/capture-text.py`: its three new
documents are an HTML record, an HTML notice and a PDF whose `.txt` sidecars
are their text forms, and the HIT `.doc` it may cite is held (S101) and needs
no new span. C2 can land with the base tool.

The L1 ran the candidate once under the counter before this freeze (a
feasibility check, not a measurement: `--seed 7` and one `--per-leg 8` run,
both 6/6; no seat has scored).

Routed items this round meets (round-53 closure, `corpus/lessons/round-53-verifier-spotcheck.md`
section 6): (3) receipt discipline — the before, control and after receipts
are standalone files under `corpus/evidence/round54/`; (6) the forgeable
frozen-counter streak (RW-1) — C1's counter has a non-vacuous sample-size
guard (`--per-leg` >= 2, else usage exit 2), generates its GEN/ENCRYPTED/
MALFORMED documents from fresh random text at counting time, judges REAL
against an oracle (the LibreOffice export) made at counting time rather than
canned strings, and runs every tool invocation under an audit hook so a tool
that shells to LibreOffice is refused; (1)/(2) the inherited round-53 W2
registry and the W2 that was never dispatched are disclosed in the report.
The SCORECARD round-54 plan item "a defined OLE `.doc` text form or a narrower
refusal" is C1; "continue theme C (GB/T 7714 source-type)" is C2.

## R54-C1 — operability (lowest scored axis, 3/10; capability acquisition)

**Frozen predicate (one sentence, = the `c1-count.py` docstring):**
`tools/capture-text.py`, run as an ordinary command under an audit hook that
fails the run on any process spawn, exec, fork or socket connect, prints for
an OLE Word 97+ `.doc` the text form of its main document story — every
paragraph, table-cell and hyperlink-anchor text of a document generated at
counting time from fresh random text (CJK, Latin-1 and ASCII mixed) appears
exactly once and in document order in the whitespace-free text form, the
hyperlink's random URL (a field code) does not appear, there is no U+FFFD
and no code point below 0x20 other than tab and newline, and `--locate` on a
generated paragraph prints `LOCATED count=1 offset=<o>` with the stdout text
form holding that paragraph at `<o>` — and for each OLE Word capture of the
read-only campaign cache (five pinned `.raw` files, four distinct documents)
exits 0 with no U+FFFD, holds every line (>= 8 non-space characters) of the
LibreOffice plain-text export of the same bytes, made at counting time, in its
whitespace-free text form (directly, or after dropping one leading list label
of at most 12 non-space characters), has a whitespace-free length within
0.90-1.10 of that export's, and locates the two pinned quotes exactly once;
while it refuses (exit 2, nothing on stdout, a stderr line starting
`REFUSED ole-not-word`, `REFUSED ole-encrypted` or `REFUSED ole-malformed`
respectively, no `Traceback`) a generated OLE spreadsheet, a generated `.doc`
whose FIB has fEncrypted or fObfuscated set, and a generated `.doc` cut short
before its WordDocument stream or carrying a sector shift of 7 — and the
round-52 frozen counter prints `LEGS=9/9` and the round-52 supplement
`SUPPLEMENT_LEGS=4/4` for the same tool — counted as legs GEN, NONWORD,
ENCRYPTED, MALFORMED, REAL, REGRESS.

- Counting command: `python3 corpus/evidence/round54/c1-count.py` (`--per-leg K`
  generated documents per generated leg, default 3, minimum 2; `--seed N`;
  `--work DIR`, default a `TMPDIR` mkdtemp removed on exit; `--tool PATH`).
  Pinned captures: sha256 prefixes in `REAL`, else `ENV_CHANGED` exit 2.
- Before (`controls/c1-before.txt`, the lane tool at `BASE_REV`): `LEGS=1/6`
  (REGRESS only), `C1=FAIL` exit 1 on three unseeded runs and `--seed 7` —
  the base refuses every OLE file as `not a zip`.
- Controls (`controls/build-c1-controls.py`, scored `--seed 54`,
  `controls/c1-controls.txt`): CONST (prints nothing, exit 0) 0/6; NAIVE (the
  round-49 reading: whole file as UTF-16LE, control characters dropped) 0/6;
  REFUSEALL (`REFUSED ole-not-word` for everything) 1/6 (NONWORD); SHELL (a
  forge that hands the file to LibreOffice and keys refusals on byte checks)
  1/6 (NONWORD) — the audit hook stops its spawn.
- Target: `LEGS=6/6`, `C1=PASS` exit 0, on three independent unseeded runs and
  once with `--seed 7`.
- Kill rule: any leg failing in any of those runs, or an `ENV_CHANGED` exit 2,
  means C1 fails.
- Tag: plumbing (QUALITY 64). Capability row only if the after-measurement
  passes in this round.

## R54-C2 — depth (sourced; theme C, the PRC citation standard GB/T 7714-2025)

**Frozen predicate (one sentence, = the `c2-count.py` docstring):**
the citation-standard theme (GB/T 7714-2025, the PRC rules for bibliographic
references) enters the lane BY DOCUMENT as the lane entries
`corpus/knowledge/source-type-taxonomy-r36.md` (the SAMR standard record and
the openstd full-text notice) and `corpus/knowledge/source-type-taxonomy-r37.md`
(the editorial office's copy of the standard's text, and optionally the HIT
data specification the lane already holds as S101), both of which exist; of
the three new documents they rest on, at least two are BOUND — exactly one lane
Registry row whose FIRST source-cell URL is the document's URL, that row new
since BASE_REV, `mined`, opened 2026-10-26, its `used-by` naming exactly the
existing entries citing it (at least one), and every existing citing entry
carrying a `source: <that id> — <url>` line — and every other one is REFUSED
(no lane row, no `source:` line naming its URL in any existing entry, and a
`refused-doc` line naming its URL in the round-54 lesson); an entry citing the
HIT specification does so only as `source: S101 — <its url>` and S101's
`used-by` names it; no `S###` token appears in the existing entries except a
bound id or S101 so cited; at BASE_REV no `corpus/knowledge` file held
`ISO 690:2021` or `文献载体标识`, and each existing entry holds its own term (in
that order); `corpus/evidence/round54/spans.tsv` (derived by `build-spans.py`)
carries at least three quote rows per bound id, each quote at most 25
whitespace words and 160 characters, inside its span file, inside the citing
entry and inside the round-54 lesson, each span file the exact slice of the
capture text form at the recorded offset whose file digest is the recorded
one, and longer than its quote; the round-51 `quote-substance-check.py` exits
0 on the manifest; every `char N` in a bound row's `anchor` cell (at least
one) is the offset of a quote of that id; every existing entry exits 0 under
`tools/inference-ground.py` with this round's spans; and the lesson carries a
re-check verdict line for each absent-defect-register row on a theme URL (the
three documents and the HIT specification; the sweep prints how many: 3 at
the freeze), with no bound document whose verdict is `fabricated` or
`unverifiable`.

- Counting command: `python3 corpus/evidence/round54/c2-count.py` (and
  `--lane-only`).
- Before (`controls/c2-before.txt`): `ENTRIES=0/2 BOUND=0/3 SUBSTANCE=FAIL
  QUARANTINE_VERDICTS=0/3 C2=FAIL` exit 1.
- Controls (`controls/build-c2-controls.py`, output `controls/c2-controls.txt`):
  the two staged entries copied unchanged — `REF_ID_UNBOUND=6 HELD_BAD=1
  BOUND=0/3 C2=FAIL`; the same entries rewritten by the base adopter with its
  append block inserted, no quote, span or lesson — `BOUND=3/3
  REF_ID_UNBOUND=3 HELD_BAD=1 ANCHOR_BOUND=0/3 C2=FAIL`. Binding alone is
  mechanical; the claim's substance is the located quotes, their spans,
  anchors, the held-row `used-by` update and the inference ground.
- Quarantine slice at the freeze: 24 chousa data rows; three on theme URLs —
  register `S080` (SAMR record), `S088` (JMU copy), `S096` (HIT specification).
- Target: `C2=PASS` exit 0 (`ENTRIES=2`, `BOUND>=2`, `BOUND+REFUSED=3`).
- Kill rule: an entry missing, fewer than two bound documents, any unbound
  S-token or bad held citation, any quote leg short of n/n, `SUBSTANCE=FAIL`,
  an anchor not at a located quote offset, any existing entry failing
  `inference-ground`, a missing quarantine verdict, or a bound document with a
  `fabricated`/`unverifiable` verdict means C2 fails.
- Tag: ground (QUALITY 64). Province, QUALITY bar and coverage-map credit are
  judged per entry in the lesson Gate; the counter measures binding and
  presence, not entailment (restated before data). Expansion credit is per
  document, not per entry; S101 (held) earns none.

## Admission rule

Each claim is admitted only if its frozen counter meets the target on the
landed commit and no owned axis is harmed. Neither counter's pass overrules the
external closure's spot-check of the Gate verdicts. A rule changed after any
seat has scored is not the claim's rule; any post-freeze change is disclosed in
`claims-erratum.md`.
