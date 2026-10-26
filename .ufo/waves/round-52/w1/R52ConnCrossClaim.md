# R52ConnCrossClaim — cross-claim / cross-fleet findings (round 52 w1)

Seat: R52ConnCrossClaim (leaf; no subagents). Lane: chousa-shokunin. Scope: the three
cross-claim questions over the frozen C1/C2 claims (claims.md at lane commit
37468eadd8d098e80289b2f31a22de3872d4a1f6). All paths absolute; repo read-only (no writes
other than this report). Tooling: read `~/.omp/agent/RULES.md`; no install performed or
needed (no pacman/uv/npx action — record none). Scratch `/fast/scratch/hyaku/chousa-r52/
R52ConnCrossClaim/` created and removed before finish. No counters run by this seat (not in
scope); every statement below is grounded in a command run or a file:line read.

---

## Q1 — does the lane already carry other capture-form rules the new tool should subsume or that contradict it?

Command (run on the live tree):
```
$ grep -rEc 'UTF-16LE|form_texts|DEINT|two-column' \
    chousa-shokunin/corpus/QUALITY.md chousa-shokunin/corpus/knowledge chousa-shokunin/tools \
    2>/dev/null | grep -v ':0$'
## UTF-16LE
.../QUALITY.md:1
.../knowledge/citation-count-semantics-r37.md:2
## form_texts
## DEINT
## two-column
.../knowledge/chinese-search-record-r39.md:1
.../knowledge/japanese-search-record-r38-amendment-2026-10-23.md:2
```
File:line of every match: `QUALITY.md:805` (criterion 76); `knowledge/citation-count-semantics-r37.md:4,5`; `knowledge/chinese-search-record-r39.md:17`; `knowledge/japanese-search-record-r38-amendment-2026-10-23.md:3,12`.

Findings:
1. The lane already operates THREE named capture forms, all in the form-vocabulary of QUALITY
   76 (`QUALITY.md:800-808`: "Every `char N` offset in a lesson names the capture form it
   indexes") and of its checker `corpus/evidence/round50/decode-form-check.py:19` (FORM_LINE
   recognizes only `utf-8-sig`, `UTF-16LE`, `.txt…UTF-8`): (a) `.txt` read as UTF-8 for PDF
   captures — applied in `japanese-search-record-r38-amendment-2026-10-23.md:3,12` (S112
   JAHBS, "two-column PDF text: a sentence can cross the gutter") and `chinese-search-record-r39.md:17`;
   (b) `.raw` decoded as UTF-16LE for OLE `.doc` captures — applied in
   `citation-count-semantics-r37.md:4,5` (S100/S101); (c) `.raw` decoded as UTF-16LE is the
   only raw form the checker knows.
2. The new C1 form — `.raw` (OOXML .docx) through `tools/capture-text.py` — is a FOURTH form.
   It does not contradict (b): UTF-16LE is valid only for OLE .doc payloads; a .docx `.raw`
   decoded as UTF-16LE is garbage. There is no overlap and no rule to subsume under the names
   `form_texts`/`DEINT` (zero matches anywhere in the three paths).
3. Gap (the real finding): `decode-form-check.py:19` does not recognize the capture-text form,
   so a round-52+ lesson that names it ("the `.raw` through `capture-text.py` form") will be
   judged `FORM_MISSING` (QUALITY 76 checker exits 1), and a lesson that misnames the docx form
   as UTF-16LE will pass — the exact failure class of round-49 defect 5 (offsets shifted between
   decodes, cited at `QUALITY.md:801-802`).

Recommendation: extend the form vocabulary — add the capture-text form to `FORM_LINE`
(`decode-form-check.py:19`) and to the wording of criterion 76 — and state there that UTF-16LE
applies to OLE `.doc` raw captures only. Without this, the new tool is not a legal named form
under QUALITY 76, harming the verification surface.

## Q2 — how do other lanes read binary captures?

Commands:
```
$ grep -rln 'zipfile' <lane>/tools <lane>/corpus/evidence 2>/dev/null
chousa…/tools/capture-text.py
chousa…/corpus/evidence/round52/controls/naive-tool.py
chousa…/corpus/evidence/round52/c1-count.py
chousa…/corpus/evidence/round52/build-spans.py
kaidoku…/corpus/evidence/round-41/c1/V4/oracle.tsv | nonregular.tsv | after.json   (data strings, not code)
tabi…/round-13/aria/node_modules/… (bundled playwright)
$ grep -rln 'pdftotext' <lane>/tools <lane>/corpus/evidence 2>/dev/null
chousa…/tools/quarantine-check.py   chousa…/evidence/round42/quarantine-verdicts.tsv
kengaku…/evidence/round12-fleet/r12-prior-art-*.md, round14-fleet/r14-review-priorart.md, round30/quote-mode-six-rows.txt
$ grep -rEn 'utf-16|UTF-16' <lane>/tools 2>/dev/null
kaidoku…/round-26/recompute-ids.py:11,92-93   kaidoku…/round-31/sqlite_oracle.py:27-28
kama…/tools/digest-ledger.py:39
```
Findings:
1. Only chousa's round-52 files read OOXML zips (`zipfile`): the new `capture-text.py`, its
   counter `c1-count.py`, its control `controls/naive-tool.py`, and the builder `build-spans.py`.
   A fleet-wide scan of the other lanes' tools/scripts/verifiers found no other zip reader.
2. PDF captures are produced UPSTREAM (the campaign) as `pdftotext -layout` text: round-42
   verdicts describe captures as "a pdftotext -layout rendering" (`evidence/round42/quarantine-verdicts.tsv:7-9`);
   `tools/quarantine-check.py:223` documents that capture class. Lanes consume the ready `.txt`
   sidecar from `.qcache` (consumers include `knowledge/search-log-method-r39.md`, `knowledge/
   japanese-search-record-r38.md`, `knowledge/citation-version-binding-r36.md`, …). No lane runs
   pdftotext itself (the only code hit is a comment).
3. The only true in-lane binary readers besides the new tool are kaidoku's
   `sqlite_oracle.py:27-28` (decodes SQLite payload encodings UTF-8/16le/16be via a table) and
   `recompute-ids.py:11,92-93` (JS UTF-16 unit ordering — a domain-id sort key, not a capture
   reader). kama's `digest-ledger.py:39` only notes UTF-16 documents are not seen.

Recommendation: `capture-text.py` should be the fleet's single OOXML reader — no sibling lane
should reimplement zipfile parsing; and sibling lanes consuming the docx form should use the tool
(like r37 used the UTF-16LE decode for OLE .doc), never the `.txt` sidecar (garbage for .docx,
per the round goal). This matches the existing split of labor (campaign produces sidecars; lanes
decode raw only when unavoidable).

## Q3 — is the C1 nonce-name design used elsewhere in the fleet?

C1 counter design (`corpus/evidence/round52/c1-count.py`): RNG is `random.SystemRandom()` unless
`--seed` (line 256); input files get random basenames `Gen.name()` (lowercase alnum, length
5-12, lines 77-78) and a random extension among `.raw/.docx/.bin/""` (lines 262-263) inside a
fresh `mkdtemp(prefix="c1r52-")` dir (line 258); zip MEMBER names are randomized in the
MAIN_PART leg (lines 201-204) and REFUSE leg (lines 302-308). Fixed names: none but the tempdir
prefix (unique via mkdtemp's own entropy suffix). This implements round-51 lesson section 6:
"make the next counter nonce-only with no fixed directory names" (`lessons/round-51-verifier-spotcheck.md:100`).

Fleet prior art (command: `grep -rEn 'mkstemp|mkdtemp|…|urandom|uuid4|token_hex' <lane>/tools <lane>/corpus/evidence`):
- `kaidoku…/round-33/measure_driver.py:365,386,388`: `secrets.token_hex(12/8/16)` random
  classifier-file, directory and fixture-file names inside a random `mkdtemp(prefix="r33m-")`
  priv dir — the same file+dir nonce shape as C1.
- `kaidoku…/round-34/version-needs-counter.py:119-120`: input basename is
  `"opaque-" + secrets.token_hex(12) + ".data"` with the comment "Neither basename, carrier id,
  source path nor expected JSON is given to the reader" — the same rationale as C1's fresh names.
- `chousa…/tools/mechanism-witness.py:234` and `argv-witness.py:298`: seed defaults to
  `int.from_bytes(os.urandom(8), "big")`; tempdir names embed that seed (`w35wit-%08x-`,
  `r36wit-%08x-`).
- `kama…/tools/append-only-audit.py:504,614,692`: `os.urandom(...).hex()` nonces in line
  content (content, not names).
- Contrast: kaidoku's `heldout-gen*.py` (rounds 39-42) explicitly forbid urandom (docstrings:
  "no ``os.urandom``") — a deterministic alternative; C1 follows the measure_driver /
  version-needs-counter precedent, not heldout-gen.

Findings: file/directory-level nonce naming is established fleet practice, and C1 extends it to
zip member names — that member level is new in round 52 (no other zip writer exists). The only
non-random residue is the fixed tempdir prefix, which is safe (mkdtemp entropy) and aids
readability.

Recommendation: keep the `SystemRandom` default and the fixed prefix; record
`version-needs-counter.py:119-120` and `measure_driver.py:365-388` as the precedent lines in the
SKILL note on one-shot counters, and note the member-name leg is the novel extension that the
frozen counter already covers (MAIN_PART/REFUSE).

---

## One bounded proposal

Move: extend `decode-form-check.py:19` (and QUALITY 76 wording) so the capture-text form is a
legal named form, scoped UTF-16LE to OLE .doc, and document `capture-text.py` as the fleet-wide
OOXML reader (with version-needs-counter/measure_driver as the nonce precedent). Axes: improves
operability (C1's form becomes quotable in lessons) and depth (C2's NIPH quotes stay checkable)
without touching the frozen predicates, targets, counters or controls. Risks: changing
decode-form-check is a verification-surface edit — keep its output contract (FORM_NAMED/FORM_MISSING)
unchanged; add only the new form to FORM_LINE. Verification: run `decode-form-check.py` on a
lesson naming the capture-text form (expect FORM_NAMED) and on round-50 lessons (expect
unchanged output).

VERDICT: cross-claimed C1/C2 against the lane's form rules, sibling binary-reading practice and
fleet nonce precedent — found no contradiction, one vocabulary gap (QUALITY 76 / decode-form-check
missing the capture-text form) and direct precedent for the nonce design; proposal bounded to the
form-vocabulary extension.
