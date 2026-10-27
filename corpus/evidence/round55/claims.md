# Round 55 — frozen claims (chousa)

author: chousa L1 (hyaku run 9, agent `ChousaR55`)
date: 2026-10-27
freeze: before any round-55 wave seat exists or scores; the C1 candidate (`tools/build-spans.py`)
is committed after this file
base: `dba605deb5cd5ed4874e0e3c39ba24737409cd80` (`BASE_REV`; the lane tip at round start: the
round-54 tip `25abbe82`, the closure spot-check `714cf555`, the orchestrator's W2 salvage `78ebc257`
and its round-53 `w2.ready` abandonment `dba605de`)

No external fetch or network egress: L0 `8d77e6c1` remains open; every source opened this round is
an on-disk capture under the read-only `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache`.

Three claims, three distinct axes, causally separable:

- C1's counter generates its own documents, reads four pinned OLE captures and round 54's committed
  manifest at BASE_REV, and runs the builder; it never reads the lane's registry, entries, lesson or
  round-55 spans.
- C2's counter judges the round-55 manifest against text forms it derives itself (the BASE_REV
  `tools/capture-text.py`, imported from a scratch copy); it never runs `tools/build-spans.py`, so a
  manifest built by any means is judged the same and C2 can land without C1.
- C3's counter reads only the SCORECARD errata block, the eleven target files, BASE_REV bytes, three
  captures and probes it runs itself; it reads no C1 or C2 output.

The L1 ran a reference builder once under the C1 counter before this freeze (a feasibility check of the
counter, not a measurement: `--seed 7` and one unseeded run, both 4/4); no seat has scored.

Routed items this round meets (round-54 closure, `corpus/lessons/round-54-verifier-spotcheck.md`
section 6): (1) the uncommitted W2 output — committed by the orchestrator's salvage `78ebc257` below
BASE_REV; recorded, not re-committed; (2) the W2 findings — C3's eleven items are the W2 falsifications
of lane statements, the rest are routed through wave 1 (integration register); (3) RW-1, the sixth
round — C1's counter is built against the mechanisms W2 demonstrated: no expected value is on disk
while the tool runs (the oracle-echo of `R54W2SentFinal` F1/F2), generated documents are copied alone
and their generation tree deleted (the sibling-HTML forge of round 54), file opens, listings and scans
outside the run's own directories end the run (the `/proc` and oracle reads), ctypes library loads end
the run (`R54W2CritC1Verdict`'s ctypes delegate), REGRESS runs under the hook (the round-54 unhooked
REGRESS, `R54W2CritMistakes`), and a span is judged against the exact defined form, so a LibreOffice
delegate fails on content even past the hook; (4) the r36 wording — C3 E01/E03 (E02/E04 are further
W2 `R54W2CritEntailSta` findings); (5) QUALITY 97 F1 — C3 E05 (and E06/E07, W2 F2); (6) lesson
Mistakes row 2 — C3 E08; (7) the five W04 warnings — carried to wave 1 for adjudication.
The SCORECARD round-55 plan items: "a span builder that reads an OLE `.doc` through
`tools/capture-text.py`" is C1; "the refused S130 grey-literature entry, now that its form blocker is
gone" is C2; "a frozen C1-style counter whose generated inputs never sit beside the tool's input and
whose REAL leg cannot be canned by digest (RW-1)" is C1's counter; the HIT carrier-alphabet leg (S101)
waits for a round whose counter covers it.

## R55-C1 — operability (lowest scored axis, 3/10; capability acquisition)

**Frozen predicate (one sentence, = the `c1-count.py` docstring):**
`tools/build-spans.py --quotes Q --out DIR --cache C`, run as an ordinary
command under an audit hook that ends the run (exit 97) on any process spawn,
exec, fork, socket connect or bind, or ctypes library load, and on any file
open, directory listing or scan outside the run's work directory, the hook's
own file, the tool's own directory, the lane's `tools/` directory and the
Python installation,
writes `DIR/spans.tsv` (header
`id url capture_sha256 offset span_file quote entry`, one row per quote row of
Q, in order) and `DIR/spans/<id>-<n>.txt`, where for every row the span file
is the exact slice `form[offset:offset+len(span)]` of the document's DEFINED
text form, longer than its quote, holding the quote at char N = offset + the
quote's position in the span, with `capture_sha256` the digest of the file
read — the defined form being, for a capture whose `.raw` is an OLE compound
file or a zip, the stdout of `tools/capture-text.py` on that `.raw` (its
`.txt` sidecar is never used), and otherwise the `.txt` capture read with
universal newlines — and prints `QUOTE <id> char <N> <span_file>` per row and
exits 0; this is checked on held-out quotes the counter picks at counting time
from OLE `.doc` files it generates from fresh random text (each copied alone
into the run's cache under the key of a random URL, with no sibling file, the
generation tree deleted before the run) and from the four distinct pinned OLE
captures of the read-only campaign cache (copied with their `.txt` sidecars
under the keys of random URLs), the expected offsets held only in the
counter's memory; while a run whose rows include one with no defined form (a
`.raw` that is neither an OLE file nor a zip, and no `.txt`, though the quote
sits once in the raw's UTF-16LE decode), one whose quote is absent from the
defined form though it occurs exactly once in the capture's `.txt` sidecar or
in the raw's UTF-16LE decode, or one on an OLE file `tools/capture-text.py`
refuses (a spreadsheet) exits 1, prints a stderr line starting
`build-spans: refused <that id>`, and writes no `spans.tsv` and no span file;
and run on round 54's `quotes.tsv` (as committed at BASE_REV) against copies of
its captures it re-derives round 54's committed `spans.tsv` and span files
byte for byte — counted as legs GENOLE, OLEPIN, REFUSE, REGRESS.

- Counting command: `python3 corpus/evidence/round55/c1-count.py` (`--per-leg K`, default 3, minimum 2;
  `--seed N`; `--work DIR`, empty or absent, default a `$TMPDIR` mkdtemp removed on exit; `--tool PATH`,
  default `tools/build-spans.py`). Oracle `tools/capture-text.py` pinned at sha256
  `2c0140bc04029c8faedc6c89a65bd657430d8b85f433406946567b70303e2573`; pinned captures by sha256 prefix;
  either mismatch is `ENV_CHANGED` exit 2.
- Before (`controls/c1-before.txt`): `tools/build-spans.py` is absent at BASE_REV (`git cat-file -e` →
  fatal); the counter prints `LEGS=0/4`, `C1=FAIL` exit 1 on `--seed 7` and three unseeded runs.
- Controls (`controls/build-c1-controls.py`, scored `--seed 55`, `controls/c1-controls.txt`): R54SHIM
  (the round-54 builder behind the round-55 CLI — the do-nothing control: `.txt` first, else the raw's
  UTF-16LE decode) `LEGS=1/4` (REGRESS only); TXTONLY 1/4 (REGRESS only); DELEGATE (LibreOffice through
  ctypes `system()`) 0/4, `AUDIT_FORBIDDEN ctypes.dlopen`.
- Target: `LEGS=4/4`, `C1=PASS` exit 0, on three independent unseeded runs and once with `--seed 7`.
- Kill rule: any leg failing in any of those runs, or an `ENV_CHANGED` exit 2, means C1 fails.
- Tag: plumbing (QUALITY 64). Capability row only if the after-measurement passes in this round.

## R55-C2 — depth (sourced; the NMPA grey-literature search-record field, by document)

**Frozen predicate (one sentence, = the `c2-count.py` docstring):**
the NMPA grey-literature search-record field enters the lane BY DOCUMENT as
the lane entry `corpus/knowledge/grey-literature-and-chinese-search-record-r40.md`,
which exists; of the three new documents it may rest on (the NMPA guideline
`.doc` hosted by gcpunion.org, the 中国食品药品网 issuance report, the NMPA
English issuance notice) at least two are BOUND — exactly one lane Registry
row whose FIRST source-cell URL is the document's URL, that row new since
BASE_REV, `mined`, opened 2026-10-27, its `used-by` naming exactly the
existing entries citing it (at least one), and every citing entry carrying a
`source: <that id> — <url>` line — the guideline `.doc` among them, and every
other one is REFUSED (no lane row, no `source:` line naming its URL in the
entry, and a `refused-doc` line naming its URL in the round-55 lesson); the
梅斯医学 PRISMA-S item is cited, if at all, only as `source: S113 — <its url>`
with S113's `used-by` naming the entry; no `S###` token appears in the entry
except a bound id or S113 so cited; at BASE_REV no `corpus/knowledge` file
held `是否检索灰色文献`, and the entry holds it; `corpus/evidence/round55/spans.tsv`
carries at least three quote rows per bound id, each quote at most 25
whitespace words and 160 characters, inside its span file, inside the entry
and inside the round-55 lesson, each span file the exact slice, at the
recorded offset, of the document's DEFINED text form whose file digest is the
recorded one — for a capture whose `.raw` is an OLE compound file or a zip,
the stdout of `tools/capture-text.py` as committed at BASE_REV run on the
`.raw` (its `.txt` sidecar is not a defined form), otherwise the `.txt`
capture read with universal newlines — and longer than its quote; the
round-51 `quote-substance-check.py` exits 0 on the manifest; every `char N`
in a bound row's `anchor` cell (at least one) is the offset of a quote of that
id in that form; the entry exits 0 under `tools/inference-ground.py` with
this manifest; and the lesson carries a re-check verdict line for each
absent-defect-register row on a theme URL (the sweep prints how many: 1 at
the freeze, register S125 round6 on the guideline `.doc`), with no bound
document whose verdict is `fabricated` or `unverifiable`.

- Counting command: `python3 corpus/evidence/round55/c2-count.py` (`--lane-only` never passes).
- Before (`controls/c2-before.txt`): `ENTRIES=0/1 BOUND=0/3 QUOTE_ROWS=0 SUBSTANCE=FAIL
  QUARANTINE_VERDICTS=0/1 (S125) C2=FAIL` exit 1.
- Controls (`controls/build-c2-controls.py`, `controls/c2-controls.txt`): STAGED (the package entry
  copied unchanged, its staged rows appended as staged) `ENTRIES=1/1 BOUND=0/3 REF_ID_UNBOUND=12
  QUOTE_ROWS=0 C2=FAIL`; REWRITE (ids renumbered by document, rows mechanically normalized, S113's
  `used-by` extended — binding with no quote, span or lesson) `BOUND=2/3 GUIDELINE_BOUND=yes
  REF_ID_UNBOUND=2 QUOTE_ROWS=0 ANCHOR_BOUND=0/2 C2=FAIL`.
- Target: `C2=PASS` exit 0.
- Kill rule: `C2=FAIL` or exit 2 means C2 fails. Expansion credit is per document bound, not per row
  or entry.
- Tag: ground.

## R55-C3 — calibration (W2-falsified lane statements, corrected by anchored errata)

**Frozen predicate (one sentence, = the `c3-count.py` docstring):**
each of the eleven lane self-statements E01-E11 below — committed at BASE_REV
and contradicted by an observation the round-54 W2 seats reported — carries,
in `SCORECARD.md` under the heading `## Round 55 statement errata`, an
appended line `erratum: <Exx> <target> anchor: "<A>" observed: "<O>"` whose
target is the item's target file, whose anchor A contains the item's key
phrase and occurs exactly once in that target at the counted tree (the
statement is corrected by an appended erratum, never rewritten away), and
whose observed text O equals, byte for byte, the observation this counter
computes from committed bytes at BASE_REV, the read-only capture cache and
probe runs it makes itself; the last `erratum:` line naming an item governs.

Items (target · key phrase · observation; the counter's docstring):

  E01 r36 entry · "belongs to no line here" · the S122 capture's latent
      no-full-text string: count and char offset
  E02 r36 entry · "主管部门为 国家标准委 (char 575)" · the phrase's offset in S121
  E03 r36 entry · "the document-type taxonomy the standard prescribes" ·
      counts of 附录 and 文献类型 in the S121 and S122 forms
  E04 r36 entry · "count 1 each, on one line" · count of 国家标准委 in both forms
  E05 QUALITY.md · "12,963 / 12,795" · the six S101 phrases located in the
      defined OLE form (BASE tool) and their drift from the stated anchors
  E06 QUALITY.md · "18,242 control characters" · C0 counts of the UTF-16LE
      decode under three exclusion sets
  E07 QUALITY.md · "0 U+FFFD, 0 control characters" · C0 and LF counts of the
      defined OLE form
  E08 lessons/round-54.md · "prints `BAD=6`" · pointer-anchor-check (BASE) on a
      BASE mirror without the two round-54 text-form dumps
  E09 QUALITY.md · "and refuses a tool that delegates to that reader" · a
      ctypes libc system() call run under the round-54 hook
  E10 QUALITY.md · "the SHELL control's receipt says the same" · the SHELL
      block's LEGS line in controls/c1-controls.txt
  E11 round54/c1-supplement.py · "outside the generation tree (no HTML, no" ·
      SUPPLEMENT_LEGS of an oracle-echo tool that never opens the `.doc`

- Counting command: `python3 corpus/evidence/round55/c3-count.py` (`--work DIR`, empty or absent;
  `--skip-slow` skips E11 and cannot pass).
- Before (`controls/c3-before.txt`): `ERRATA=0/11 MISSING=11`, `C3=FAIL` exit 1.
- Controls (`controls/build-c3-controls.py`, `controls/c3-controls.txt`): RESTATE (exact anchors, the
  lane's own committed claim as the observation) `ERRATA=0/11 WRONG=11`; PARAPHRASE (the W2 reports'
  observations under paraphrased anchors) `ERRATA=0/11 ANCHOR=11`.
- Target: `ERRATA=11/11`, `C3=PASS` exit 0.
- Kill rule: fewer than 11, or exit 2, means C3 fails. An erratum that removes or rewrites its target
  statement fails its own item (the anchor must still occur exactly once).
- Tag: calibration (a count of self-statement/observation mismatches resolved, not an assertion).

## Frontier step (inside the claim cap)

- Sourced claim: C2 (rows opened 2026-10-27, cited by the entry as `source: S###`).
- Mistake to mine: candidate — the round-54 report was filed before W2's WAVE-DONE while the prompt
  forbids filing before every launched wave settles (`/home/vgpnk/Projects/shokunin/.ufo/reports/round-54/chousa.md`;
  W2 results recovered only by the orchestrator's salvage `78ebc257`).
- Census: `corpus/evidence/round55/census-start.txt` (exit 0, five pre-existing W04).
- Assimilation (section 10): theme — the NMPA grey-literature search-record field; one staged entry
  (`grey-literature-and-chinese-search-record-r40.md`), re-grounded by document; scratch
  `.ufo/waves/round-55/assimilation/` (`reg-ids` 123, `staged-ids` 114, `collisions` 42,
  `quarantine-slice` 24, `guard/` proof: a two-space-indented `  | S002 |` row collides under the
  0–3-space pattern and not under the column-zero one).
