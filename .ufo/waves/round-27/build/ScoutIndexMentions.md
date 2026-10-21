# ScoutIndexMentions — r26 withdrawal/safety status index for append-only r27 status

Assigned item: locate r26 candidate safety/withdrawal qualifications in
README/SKILL/knowledge that need an append-only r27 status. Static read-only;
no gate/selftest/probe run, no fixture execution, no network, no host-secret or
live-process inspection. Base observed in tree: `64eec5d4` (per round claims).
All line numbers are current working-tree lines; lines cited outside the r26
tail are stable text, not offsets computed from another file.

## A. Present-tense r26 qualifications needing an r27 append

Every entry below is an existing append-only section; the r27 action is a new
dated section after its last line, never an edit of the quoted text.

| id | location | observed qualification (quote <=25 words) | why r27 status is needed |
|---|---|---|---|
| A1 | `SKILL.md:500-516`, heading `### Round26 recovery safety/status correction — 2026-10-21` | "not a verified current capability" (502–503); "`FAIL (3/187 cases)`, exit1" (505); "**not admitted**" (512); "No new capability or SHONEN promotion is claimed." (515–516) | Present-tense capability statement pinned to revision `0e9784bd…`. r27 repairs C1/C2/C3 at a new revision, so this paragraph becomes stale about the current target while the r26 revision-bound failure stays historical. Append after 516. |
| A1a | `SKILL.md:70-77` (Gates table tallies "PASS (154 cases)") and `SKILL.md:79-90` (Round-25 correction, "`PASS (161 cases, 0 skipped)`") | "The shared `154 cases` tally in the rows above records checkpoint `d8c8cff`" (79–80); "final shared selftest is `PASS (161 cases, 0 skipped)`" (80–81) | Both are already superseded by A1's `FAIL (3/187 cases)`. The r27 append should name the measured r27 tally (or point to its receipt owner) rather than leave 161 as the last positive tally a reader finds. Do not rewrite the historical rows. |
| A2 | `corpus/knowledge/reader-allocation-r26.md:42-57`, heading `## Recovery qualification — 2026-10-21 (append-only)` | "narrow measured improvement, **not admission**: the cumulative gate's selftest fails3/187" (51–52); "This note remains a qualified candidate; no universal resource-bound claim" (56–57) | C1 is the r27 repair target. After repair the "fails3/187" clause is historical, but "not admission" and the no-universal-bound limit must persist. Append after 57. |
| A3 | `corpus/knowledge/recheck-due-r26.md:46-63`, heading `## Withdrawal of implementation admission — 2026-10-21 (append-only)` | "the Round26 implementation is not admitted" (48–49); "Do not use this candidate mode's absence of findings as a reliable freshness verdict." (60–61) | C2 repair changes implementation status, not the policy/source distinction. The freshness-not-truth limit must survive; r26 source-policy proposals stay proposals. Append after 63. |
| A4 | `corpus/knowledge/registry-link-r26.md:43-66`, heading `## Withdrawal of implementation admission — 2026-10-21 (append-only)` | "**The Round26 checker is not admitted.**" (45); "The 8MiB snapshot cap bounds input bytes only, not parser memory/time" (59–60); "No absence of these findings establishes correct metadata, source support, or safety." (63–64) | C3 repair changes implementation status; the cap-unit and no-absence limits remain true and must not be traded away by a green r27 run. Append after 66. |
| A5 | `corpus/README.md:859-866` (`## Round26 frontier disposition`) and `:879-889` (`### Round26 frontier admission correction — 2026-10-21`) | "qualified/withdrawn candidates, not admitted expansion" (881–883); "Each note now has a recovery qualification naming the unsafe implementation and reports." (886–887) | 859–866's "New held ground" is already superseded by 879–889. The sentence at 886–887 becomes stale ("now") once r27 appends current status. Append a new r27 subsection after 889; leave both earlier blocks intact. |
| A6 | `corpus/README.md:62-66` (coverage-map rows for the three r26 notes, lesson 26, and `evidence/round26-*`) | Rows describe method/scope, e.g. "scoped to the metadata reader" (62); no withdrawal pointer in any row | These rows read as neutral capability descriptions. Do not edit rows; the r27 append at A5 should state that rows 62–66 describe historical candidates whose live status is in the notes' withdrawal sections and the r27 status section. |
| A7 | `corpus/evidence/README.md:1094-1104` (`## Round26 recovery evidence — 2026-10-21`) | "not a PASS record" (1099); "Retained comparators, not proof of general correctness" (1102); "selftest FAIL3/187" (1100) | r27 needs its own evidence section (regressions, selftest, census receipts) appended after 1104; do not restate or alter the r26 rows. |
| A8 | `corpus/lessons/round-26.md:191-194` | "withdrawn implementation candidates, not capabilities or admitted expansion" (191); "Current safety/status addenda in their notes, SKILL, README and SCORECARD supersede earlier unqualified … language." (192–194) | This pointer names which addenda are "current". After r27, the current addenda are r27's; append the supersession pointer in the round-27 lesson (already exists, see below), not here. |

Observed fact relevant to A8: root `README.md` contains zero r26/r27 status
text; the only README addendum is `corpus/README.md:879-889`. So r27 status
targets `corpus/README.md`, not the root README — the lesson-26 sentence's
"README" referent is the corpus README.

## B. Safety limits that must survive r27 (preserve, do not overwrite)

- `SKILL.md:480-498` option tables and limits: "not a universal memory/time
  budget" (494–495); "other gate readers are not repaired" (496); "The
  operability scalar remains the original r1 construct, not a resource-safety
  or readiness score." (497–498).
- `SKILL.md:447`: "No non-author corpus spot-check or promotion is implied by
  a passing selftest." A green r27 selftest must not lift this.
- `corpus/QUALITY.md:104-113` (criterion 18): "The probe exit0 is completion
  only; compare its values." (111–113). Scope conclusions to measured shapes.
- Note limits sections: `reader-allocation-r26.md:36-40` (other readers,
  source identity, fd races remain separate); `recheck-due-r26.md:26-36`
  (`unknown, never silently current`; event is not monitoring);
  `registry-link-r26.md:36-41` ("not the whole criterion6 verifier").
- `corpus/SOURCES.md:44-46` rows S034–S036 own-work limits: "not a universal
  resource budget" (44), "not source truth" (45), "not full criterion6" (46).
  Do not re-point or flip them; r27 already has own-work rows S040–S042 at
  `corpus/SOURCES.md:50-52` citing `corpus/lessons/round-27.md` (observed;
  written by a concurrent seat at 11:39, not by this scout).
- `corpus/evidence/round26-claims.md` is frozen pre-registration evidence
  (states "Registered before any implementation", 1–7). Append status to
  notes/SKILL/README only; never add a status section to that file.

## C. Append-only r27 status contract (advice to L1/scribe)

1. New dated heading after the last line of each r26 qualification; no edit,
   reflow, or deletion inside the r26 text. Historical revision `0e9784bd…`
   statements stay true as historical statements.
2. Each append should name: the r27 measured revision and receipt paths
   (only after L1's single verification run), the repaired behavior, and an
   explicit sentence that the r26 NOT ADMITTED verdict and each note's
   withdrawal remain historical — r27 repair does not retroactively admit
   r26, its controls, or its public-source conclusions (claims: "Public-source
   conclusions from r26 stay withdrawn unless independently revalidated").
3. Keep the limits from section B verbatim in force: probe exit0 is
   completion; due/freshness is not truth; registry relationships are not
   criterion6; an input-byte cap is not a memory/time budget.
4. Cite r27 own-work rows S040–S042 (`corpus/SOURCES.md:50-52`). If L1 adds a
   new r27 knowledge note, add its `used-by` only as logged old→new
   bookkeeping; do not mutate S034–S036 or the r26 notes' source lines.
5. One status owner: `SCORECARD.md:1446-1490` (r26 verdict) and
   `LOG.md:1034-1060` (r26 disposition) are historical owners. r27 appends new
   dated verdict/log entries; neither r26 block is rewritten.

## D. Unrun checks / remaining unknowns

- Not run by this seat: `bash tools/research-gate.sh --selftest`,
  `round27-regressions.py`, `verify-metadata`, any probe. No r27 PASS, exit
  code, tally, or count is claimed here; L1 runs verification once after
  landing.
- Not measured: whether the r27 final selftest tally is exactly 187, greater
  (new independent controls), or how L1 words the appendix; the claims require
  the original 187 identities preserved and new controls passing, so the tally
  to quote must come from the final receipt, not this report.
- Not opened: `.ufo/waves/round-26/falsify/*` full bodies (only the quoted
  pointers already in the notes/lesson); `.ufo/waves/round-26` reconciliation
  JSON; any non-local source.
- Concurrent-tree caveat: `corpus/lessons/round-27.md` (74 lines, mtime 11:39)
  and `corpus/SOURCES.md:50-52` appeared after my first scan; r26 lines cited
  above were re-read after that observation and are unaffected.
- Tool installs/updates: none.

Confidence: high for locations and quotes (direct reads at the cited lines);
medium for the necessity ranking, which is inferred from the r27 claims
(repairs make the r26 present-tense clauses stale while its historical verdict
must stand).
