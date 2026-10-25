# Round 42 — frozen claims (chousa)

Frozen at the round-42 freeze commit (the commit that carries this file, the tool and
the two counters). Base: lane tip `872bf3a3507875b382313f955d15960f9638256f`.

**Round shape.** Wave-4 quarantine-first under fleet lane-addendum item 10: this lane's
first round under the assimilation directive adopts **nothing** from its shokuknow
package. It hand-checks the lane's full absent-defect-register quarantine slice and
lands a verdict per row. No new knowledge entry is admitted from the package; no
`corpus/SOURCES.md` row is appended from it. The only source this round opens is an
installed man page on the host (see §Sources).

**Disclosure.** The lane's own construction runs — the tool's first slice/examine run
and the per-row class computation it produced — happened **before** this freeze, in the
same pattern as round 39 (`SCORECARD.md` r39: "two seeds, both L1 construction runs").
The adjudication table (`corpus/evidence/round42/quarantine-verdicts.tsv`) did not exist
when this freeze was written. The counters, the decision rule and the kill rules below
are the frozen text; nothing in them was widened after any seat scored anything.

## The slice (derived, not asserted)

Extraction is the one the operator's item 10 names, re-derived here with the
space-tolerant pattern the census parser accepts:

```sh
R=/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md
awk -F'|' -v l='chousa' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' "$R"
```

→ **24 data rows**: 20 `payload-absent` (rows 37–56 of the register) + 4 of the
register's unchecked family (S100–S103, whose fourth cell is prose, not a class).
The register's own `## By lane` summary says `chousa 20` and its header says 194 rows:
both are stale, as item 10 warns — the summary counts only the `## Rows` table.

## The frozen decision rule (per slice row)

Let `Q` be the row's quarantined quotes (the register's quote cell, `<br>`-separated),
`C` the local capture of the row's cited URL (cache key `sha256(url)[:24]`), and
`located` the number of quotes of `Q` that the STRICT test (NFKC + whitespace
collapse, case-sensitive) finds in `C`.

1. If the register's row is of the unchecked family (a prose class cell: "could not be
   fetched" / "named no locator"), the verdict is `unverifiable`. **Never a
   fabrication.**
2. Else if there is no local capture of the cited URL, or the capture is a bot wall
   (interstitial) or a binary office document (`.doc`/`.docx`/RTF) whose bytes were
   never rendered to text, or the capture is shorter than the longest quote of the row,
   the verdict is `unverifiable`. **Never a fabrication.**
3. Else if `located == |Q|`, the verdict is `present`.
4. Else if `located == 0`, the verdict is `absent` — the fabrication class: the row's
   quoted span is not in the source that was actually read.
5. Else the verdict is `mixed` — part of the row's quoted span is present, part is not.

Actions this round: `present` → **adoptable later, adoption stays closed this round**
(the row is re-grounded and its citation re-pointed by document at adoption time);
`absent` → **refuse the row** with reason + flip; `mixed` → **refuse with correction**
(the absent quote's text must be corrected to the located source text);
`unverifiable` → **mark unverifiable**, never a fabrication.

## C1 — operability (the lane's lowest scored non-retired axis, 3/10)

**Predicate.** The lane's quarantine scope becomes a runnable, re-derived surface: one
committed command re-derives the lane's slice from the read-only register and examines
every quarantined quote against the capture material already on disk, and the
derivation is complete, reproducible and control-discriminating.

**Counting command.** `python3 corpus/evidence/round42/c1-count.py` (lane root).

**Target.** `SLICE_REDERIVE_MATCH=24/24`, `QUOTES_EXAMINED=Q/Q` (every independently
counted quarantined quote examined, none skipped), `REPRODUCIBLE=1/1`, `POSITIVE_CONTROL=1/1`,
`NEGATIVE_CONTROL=1/1`, `MUTANT_DETECTED=1/1`; exit 0.

**Do-nothing control.** A tree without `tools/quarantine-check.py`: the counter cannot
run and exits non-zero. Committed receipt: `corpus/evidence/round42/controls/c1-control-before.txt`.

**Kill rule.** If the do-nothing control meets the target, the counter or the target is
wrong and is fixed **before** the scored run. If any of the six counts fails on the
landed tree, C1 is reported as a miss — the count is not re-scaled and the target is
not narrowed after the fact.

**Limits.** The counter grades the derivation and the examination's completeness and
discrimination; it does not assert that any row's verdict is *true* about the live
web, and it never touches the network.

## C2 — calibration (discernment)

**Predicate.** Every row of the lane's quarantine slice carries exactly one verdict
from the frozen vocabulary (`present`, `absent`, `mixed`, `unverifiable`), that verdict
agrees with an **independent** re-examination of the row, and it carries a non-empty
reason and a non-empty flip condition.

**Counting command.** `python3 corpus/evidence/round42/c2-count.py` (lane root).

**Target.** `VERDICTED=24/24`, `CLASS_CONSISTENT=24/24`, `REASON_NONEMPTY=24/24`,
`FLIP_NONEMPTY=24/24`, `VOCAB_OK=24/24`, `DUPLICATE_ROWS=0`, `ROWS_OUTSIDE_SLICE=0`; exit 0.

**Do-nothing control.** A table with the same 24 rows in which one row's verdict is
flipped away from the evidence: `CLASS_CONSISTENT=23/24`, exit 1. Committed receipt:
`corpus/evidence/round42/controls/c2-control-before.txt`.

**Kill rule.** The independence is the point: `c2-count.py` re-parses the register,
re-resolves the captures, re-matches the quotes with its own NFKC + whitespace-collapse
test and re-classifies every row from its own magic-byte and interstitial checks. It
never reads the gate tool's output. Where the two implementations disagree the
conservative union decides and the disagreement is counted and reported. If the
counter's own class computation is wrong, the table is corrected to the evidence and
the disagreement is named — the table is never edited to fit the counter.

**Limits.** The counter grades rule-consistency and completeness of the adjudication,
not the truth of the underlying "absent" judgement about the live web. Under this
round's fetch boundary (no new external fetch; the L0 fetch-scope question `8d77e6c1`
is still open) a row whose source cannot be read locally is `unverifiable`, never a
fabrication — so `absent` here means "not in the source that was actually read".

## Frontier step

- `corpus/SOURCES.md`: **no row is appended from the shokuknow package.** The one source
  opened this round is an installed man page on this host; it grounds the
  capture-rendering ground the decision rule's step 2 rests on. Its row is appended
  with the next unused id, and its `used-by` names the tool and the round lesson.
- Census before → after: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa`.
- Mistake mined in `corpus/lessons/round-42.md` `## Mistakes`.
- The sourced claim: **C1** — its rule's step 2 (a capture that was never rendered to
  text cannot refute a quote) cites the opened row.
- `considerthese/2026-10-23.md` proposal mined: "for every frozen counter, name the
  cheapest gate that can score full marks without doing the work" — it lands as a
  `corpus/QUALITY.md` criterion and is honoured above: each counter names its
  do-nothing control, and the C1 counter's controls are positive, negative and mutant.

## Ruled out of scope

Adoption of any package knowledge entry or staged row; any new external fetch; any
edit to `/home/vgpnk/Projects/shokuknow` (read-only); any run of the campaign's own
checking tools (they write into the campaign tree); any bulk import.
