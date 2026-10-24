# Round 42 — wave-4 quarantine-first: the lane's 24-row quarantine slice, adjudicated

author: chousa L1 (Kimi fresh L1; wave dispatch: see the round report's wave section)
date: 2026-10-24
round: 42 (attempt 1)

## Claims and measurements

Frozen design: `corpus/evidence/round42/claims.md`, frozen at lane commit
`dd63b6cfec5e1eafddb6662fc343e2ff6ab6aedc` (base `872bf3a3507875b382313f955d15960f9638256f`).
The lane's own construction runs (the tool's first slice/examine/verdict run) preceded
that freeze and are disclosed, the round-39 pattern; the adjudication table did not
exist when the freeze was written. This round adopts **nothing** from the shokuknow
package (fleet lane-addendum item 10, wave-4 quarantine-first) and made **no external
fetch** (the fetch-scope L0 question `8d77e6c1` is still open).

- **C1 operability (the lane's lowest scored non-retired axis, 3/10):** the lane's
  quarantine scope became a runnable, re-derived surface. `python3
  corpus/evidence/round42/c1-count.py` → `SLICE_REDERIVE_MATCH=24/24`,
  `QUOTES_EXAMINED=43/43`, `REPRODUCIBLE=1/1`, `POSITIVE_CONTROL=1/1`,
  `NEGATIVE_CONTROL=1/1`, `MUTANT_DETECTED=1/1`, exit 0
  (`corpus/evidence/round42/receipts/c1-after-freeze.txt`). The do-nothing control — a
  tree without `tools/quarantine-check.py` — exits 1
  (`corpus/evidence/round42/controls/c1-control-before.txt`).
- **C2 calibration:** every slice row carries exactly one verdict from the frozen
  vocabulary, agreeing with an independent re-examination, with a non-empty reason and
  a non-empty flip condition. `python3 corpus/evidence/round42/c2-count.py` →
  `VERDICTED=24/24`, `CLASS_CONSISTENT=24/24`, `REASON_NONEMPTY=24/24`,
  `FLIP_NONEMPTY=24/24`, `VOCAB_OK=24/24`, `DUPLICATE_ROWS=0`,
  `ROWS_OUTSIDE_SLICE=0`, exit 0. The do-nothing control — the landed table with one
  row's verdict flipped away from the evidence — prints `CLASS_CONSISTENT=23/24` and
  exits 1 (`corpus/evidence/round42/controls/c2-control-before.txt`).

The round-1 operability scale is unchanged: score 3 → 3 (delta 0). Its counting command
still prints `VERDICT_BEARING_EXPORTS=3/3`, and `tools/research-gate.sh` is not touched by
this round. The C1/C2 observables sit beside that score, as in rounds 25, 29 and 31–41.

## The slice (re-derived, not taken from the register's summary)

The extraction is the operator's own recipe, run against the read-only register:

```sh
awk -F'|' -v l='chousa' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' \
  /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md
```

→ **24 data rows**: 20 of the register's `## Rows` table (`payload-absent`) and 4 of its
`## Rows whose quotes were NEVER CHECKED` table (S100–S103, whose class cell is prose).
The register's own `## By lane` summary says `chousa 20` and its header says 194 rows /
324 quotes: both are stale, as item 10 warns. The M12 census's figure (25) is not
reproduced by this extraction; the lane reports the 24 it derives.

## Adjudication (24 verdicts, one per row)

`corpus/evidence/round42/quarantine-verdicts.tsv` — id, verdict, reason, flip. One row
per slice row, no row omitted.

| class | rows | what it means here |
|---|---:|---|
| `present` | 0 | no quarantined quote was located in the local capture |
| `absent` | 15 | the quoted span is not in the capture that was actually read (the fabrication class) |
| `mixed` | 0 | part of a row's quoted span is present and part is not |
| `unverifiable` | 9 | the source was never really read locally (1 bot wall, 4 binary documents, 4 rows naming no locator) |

The 15 `absent` rows are not all the same defect, and the reason cell says which: the
measured longest contiguous common run between the quote and the capture's text
separates "the document is on disk and the quote is a defective transcription of it"
(S093 79/120 chars, S094 63/86, S108 69/108, S116 34/36) from "the capture carries no
material part of the quote" (S086 4/46 and 2/29, S114 7/32 and 2/30). Both are refused;
the flip condition differs — correct the quote, or drop the row as fabricated.

The 9 `unverifiable` rows are **never** called fabrications: S077's capture of the DOI
is a 265-character bot-challenge page, S095/S096/S120/S125 are binary office documents
whose bytes were never rendered to text, and S100–S103 are the register's own unchecked
family whose class cell names no locator.

## Mistakes

| Class | Evidence | Captured-by | Fix |
|---|---|---|---|
| provenance-class — a register class that licenses a fabrication verdict is only as good as the capture behind it; "fetched cleanly" can mean "a bot wall was saved" | S077: the campaign's class cell reads `payload-absent` ("every relevant source fetched cleanly") while the local capture of that DOI is a 265-char `Client Challenge` page (`tools/quarantine-check.py` `capture_kind`, cache file `01f657b3d0ab045c494b3f92.txt`) | none — no criterion tied a capture's FORM to the class it licenses | the frozen decision rule's step 2 refuses a bot wall, a binary document and a too-short capture as `unverifiable`; the lane's QUALITY criterion 59 and this lesson are the record |
| evidence-label — a status field that always carries the same value is not evidence, and a counter that asserts only a field's domain cannot see that | the first `examine` implementation labelled every quote `no-capture` because the status test still compared the pre-form capture kind; `c1-count.py`'s `NO_SKIPPED_QUOTE` check passed anyway, because it asserted only that the status was one of four legal words | none — QUALITY 52 asks a cell to assert its mechanism, but nothing asks whether the field VARIES | the tool's status test was corrected (`kind.startswith("page")`); the counter now sees 15 `no-capture` and 28 `absent` instead of 43 `no-capture`. Disclosed: the corrected label changes no counted value of the frozen predicate (the counts are line counts), and the wave attacked the tool as frozen at `dd63b6c` |
| register-shape — a register with two row shapes loses rows when the parser assumes one | the register's `## Rows` table has seven columns and `## Rows whose quotes were NEVER CHECKED` has five; a parser that requires seven columns keeps 20 rows and drops S100–S103 | none — the lane had never read this register | `parse_register` reads both shapes; the slice is 24 and the four dropped rows are the unchecked family, which is where a fabrication verdict would have been most tempting |
| stale-summary — a summary table is a claim about the data, not the data | the register's `## By lane` summary says `chousa 20`; the derived slice is 24 | item 10 of the fleet lane-addendum ("its header AND `## By lane` summary totals are stale — derive your slice yourself") | the slice is derived from the data rows by the operator's own recipe; the stale totals are named here, and the register is never edited (read-only) |

## Gate

### Candidate and admitted

**Admitted** (lane-side, this round): the runnable quarantine surface
`tools/quarantine-check.py` and its two counters, the adjudication table
`corpus/evidence/round42/quarantine-verdicts.tsv`, this lesson, and one `corpus/SOURCES.md`
row for the installed manual this round opened (below). **No knowledge entry is
admitted** and **no package row is appended**: this is the lane's first round under item
10 and it adopts nothing from the shokuknow package. The 24 rows are adjudicated, not
imported; a later round may adopt a row whose quote is present and re-grounded.

**Rejected** (kept as evidence of taste): the whole staged package, this round, on the
rule of item 10 — wave-4 lanes make their first round quarantine-first. Flip: a later
round, once the slice's verdicts are closed and an entry is re-grounded in-round under
CORPUS rule 1.

### Sources opened and registry changes (installed copies only; no egress)

- **S077 opened** — Poppler `pdftotext(1)` manual, installed `/usr/share/man/man1/pdftotext.1.gz`
  (file SHA-256 `50dd56df96821e172abfcfdef75995c076ca3cb4602c99c6cb58f0d25abf4a27`),
  accessed 2026-10-24. Located quote (11 words): "Pdftotext converts Portable Document Format (PDF) files to plain text."
  (DESCRIPTION, decompressed lines 12–13 of the roff source). Tier A: the documented
  contract of the exact tool whose output the campaign's PDF captures are. The installed
  binary is `pdftotext version 26.08.0` (Poppler Developers, `http://poppler.freedesktop.org`,
  printed by `pdftotext -v`). It grounds the frozen rule's step 2 — a PDF capture in the
  cache IS a text rendering (`pdftotext -layout`), so a quote's absence in it is a
  statement about the rendering, and a non-PDF binary document that was never rendered
  cannot refute a quote at all.
- **Bounded search log entry added** to `corpus/SOURCES.md` (`## Search log`, round 42):
  question — what contract do the cached captures carry, and which of them can refute a
  quote? Where: the campaign's committed capture cache and the installed man pages only;
  the campaign's own checker (`quote-lint.py`) was READ, never run (it writes into the
  campaign tree). Identified 24 quarantined quotes over 24 rows, screened 24, included 24,
  excluded 0. Stop rationale: the slice is closed by the register's own data rows; every
  quote of every slice row was examined once against the local capture material.
- **Rejected this round**: fetching the canonical URL of the man page, and fetching any
  of the 20 cited sources. Flip: the operator answers the fetch-scope L0 question
  `8d77e6c1`, or an approved fetch is added to the approval table.

### Non-author spot-check

Pending an outside non-author review of at least one admit and one reject. The wave's
seats are author-lane (a seat this lane dispatched is still the lane), so no seat
verdict is counted as independent review, and discernment is not claimed externally
verified this round.

## Sources census

Round-start command: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa`; exit 0; output: five W04 warnings (S051, S053, S073, S074, S075) + `ok`.
Round-end command: the same; exit 0; the same five W04 warnings (S075's is dispositioned by
round 41's C2) and the new row S077 adds no warning; exit 0.
Manual census (frozen commands, lane root): rows 76 → 77; tier A 70 → 71; status mined
52 → 53; duplicate ids none; malformed rows 0; mined used-by paths resolve.

## Id-collision note (scratch, no append)

The lane's next free id is S077 and the staged package's first id is also S077
(`/home/vgpnk/Projects/shokuknow/merge/chousa/SOURCES.append.md`). The operator's
collision recipe was run in scratch with the 0–3 leading-space pattern the census
parser accepts; the collision is recorded in the round report and in the L0 note. This
round appends no staged row, so the collision is a future adoption-time renumbering
matter (the package's ids shift by one and every adopted citation is re-pointed BY
DOCUMENT, never by arithmetic).
