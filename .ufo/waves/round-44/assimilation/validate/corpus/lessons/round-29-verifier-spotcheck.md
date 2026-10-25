# Round 29 — non-author verifier spot-check

author: hyaku closure (non-author integrator, @m_opus)

Date: 2026-10-23 UTC (host clock 2026-10-22, UTC-3). Runtime model string exposed to this closure
session: `anthropic/claude-opus-5-5` (reached through the configured `task` route; no model
parameter was passed). Three read-only seats re-checked parts of the evidence: ChronoV3Freeze
(critic), LivenessEvidence (reviewer) and ReceiptsMutants (reviewer). They are named where their
findings are used. Driver digest, copied from `.ufo/watchdog.log`:

```
2026-10-22T22:03:00-03:00 launch chousa round=29 pgid=3655527 driver=hyaku-inline attempt=1
2026-10-22T23:27:23-03:00 complete chousa round=29; hyaku-inline attempt=1
```

## Decision

**Status `ok`, admitted.** The one declared claim, C1 (operability, capability acquisition:
`tools/quote-reopen.py verify`), verifies on its frozen design-v3 predicate. No axis is harmed. The
operator asked for three rulings. Each is decided below with its reasons:

1. **Was v3 frozen before any data was scored under it? Yes.** The only v3-counter execution before
   `aa5e1a31` (01:28:23Z) is the do-nothing before-receipt that the freeze commit itself contains.
   Before v3, the mutation seat MutateCounter scored only controls: always-ABSENT, id-keyed,
   position-keyed, silent and similar, on the v2 counter and on mutated counters
   (`.ufo/waves/round-29/build/MutateCounter.md:21-27,43`). The first scoring of a primary candidate
   is ExecTool at 01:34:02Z, on v3. One contract-following reference implementation was scored
   before a redesign: the CtlCasefoldNoBoundary baseline, 82/82 under v1. It is disclosed at
   `corpus/evidence/round29/claims.md:30-35` and was committed with v2 at `12244431`. It is not the
   claim's command. Both redesigns were triggered by controls, not by a candidate result, and each
   only made the target harder. §9 of the addendum prescribes exactly this sequence: "if it meets
   the target, the counter or target is wrong — fix it before data". It is not a rule changed to fit
   data.
2. **Does the frozen predicate claim liveness? No.** The predicate sentence
   (`claims.md:49-53`) is "every one of the … 130 items gets a verdict equal to its label". The
   counter condition is `n == t == 130` (`c1-count.py`), and the receipt label is
   `QUOTE_REOPEN_MATCH`. None of the three requires that the answering process fetch. The word
   "live" appears in the prose that describes the surface (`claims.md:41-42`) and in the
   capabilities row (`SCORECARD.md`, round-29 capabilities). It does not appear in the predicate.
   The cache-only verifier is not a do-nothing control either. It needed page text that an
   independent extractor had fetched and normalized 27 minutes earlier, plus a matcher that follows
   the contract (`falsify/CriticClaimDesign.md:55-57,86`). The best committed v3 control without
   page text reached 115/130 (`controls/CtlLabelKeyed/receipt-v3-contrast-run2.json`). The rule that
   "any control that meets the counter voids the design" is scoped to the pre-data control wave
   (`claims.md:27-28,167-169`). So §9 does not fail C1 on this finding. The counter cannot prove a
   live fetch; the predicate never asked it to. The "live" wording is backed separately by committed
   runtime evidence: `falsify/DiffToolB/landed-fixture.network.json` records the registry GETs and
   eight 200 responses, bound to the landed tool hash by `differential-receipt.json`. The tool code
   uses only a per-invocation cache (`tools/quote-reopen.py:379-398`).
3. **Do the three surviving mutants falsify C1? No.** Verdict order (`MutOrder`), script and head
   text kept (`MutSkipScript`) and case-insensitive matching (`MutCasefold`) each score
   130→130→130. Each breaks the frozen tool contract (`claims.md:90-98`, `:103-105`, `:114-117`).
   The predicate's wording is item-level equality on the 130 items, not conformance to the full
   contract. The landed tool is none of these mutants: the second implementation agrees with it on
   all 73 items (`falsify/DiffToolB.md`). The survivors show a fixture coverage gap, routed below.

Admission rests only on committed evidence. The lane's earlier rejection streak was not weighed.

## Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| report landed by the lane | `git log --format='%an %H' -- .ufo/reports/round-29/chousa.md` | `chousa-shokunin f314a4f492b6dbfb78db75b52ba01f33bc68ad79` | pass |
| SHONEN heading, one line per box | report `## SHONEN`; `git show 7692bf13:SHONEN.md \| grep -cE '^\s*- \[[ x~]\]'` | 4 report lines `[~]`, 4 boxes | pass |
| cited hashes exist and are ancestors of `master` | `git merge-base --is-ancestor <h> master` for 6c5eb146, f9fd6d6c, 12244431, 8026fe60, aa5e1a31, 66bf1b93, 30c9d24d, b18b3ec9, 7692bf13 | all ok | pass |
| fleet L0 commit | `git cat-file -t 8d77e6c1`; ancestor of fleet HEAD | commit by `chousa-shokunin`, ancestor | pass |
| lane pushed, clean | `jj-lane.sh state …` ; `git status --porcelain` | `ahead=0 behind=0 local=remote=7692bf13…`; porcelain empty | pass |
| remote | `git ls-remote origin refs/heads/master` | `7692bf13a3e4bc4a75e23793e268a3288356ec50` | pass |
| prompt carries template contract | every literal line of `templates/round-prompt.md` (140 lines; lines with placeholders excluded) found in `.ufo/prompts/chousa-round-29.md` | 0 missing | pass |
| census at closure | `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` | `chousa ok`, exit 0 | pass |
| diff shape | `git diff --numstat 6c5eb146 7692bf13` | 517 files, 233974 insertions, 0 deletions | additive only |

Conformance defects (status-neutral): the report's re-run count, recorded under D2 below;
`build/ExecTool.md:5` prints a nonexistent revision, which the lesson corrects with an erratum
(`lessons/round-29.md:110-112`); the snapshot-control code and data stayed in scratch, so only
their receipts are committed (`falsify/CriticClaimDesign/snapshot-provenance-summary.json`).

## Claims — re-check against `7692bf13`

C1 is **evidence-verified, not re-executed**. The counter fetches external pages, the lane's
fetch-scope L0 question (fleet `8d77e6c1`) is still open, and the counter is lane-owned
measurement machinery. These were plain reads of committed bytes:

| Check | Command | Observed |
|---|---|---|
| tool identity | `git show 7692bf13:tools/quote-reopen.py \| sha256sum` | `72a3ad47…18754fea`, equal to the reported value and to `30c9d24d` |
| counter identity and freeze | `git show 7692bf13:corpus/evidence/round29/c1-count.py \| sha256sum`; `git diff --stat aa5e1a31 7692bf13 -- c1-count.py fixtures/quote-reopen-r29/ claims.md` | `cd509650…a6993b5c175d`; empty diff, so nothing changed after the freeze |
| before | jq over `controls/before-do-nothing-v3.json` | 0/130, counter exit 1, hash v3 |
| after | jq over `measure/after-run1.json`, `after-run2.json` | 130/130 twice, seeds 1858171162794361068 and 11266274748383853032, cmd `python3 tools/quote-reopen.py verify`, hash v3 |
| independent reruns | jq over `falsify/RerunCounterA/receipt.json`, `RerunCounterB/receipt-{1,2}.json`, `ScoutFreshnessH/rederive-receipt.json` | 4 JSON receipts at 130/130, plus `rederive3.out` at 130/130; the reported sixth run has no committed output (D2) |
| v3 controls | ReceiptsMutants tally of every receipt under `controls/` that carries the v3 hash | 28 receipts, maximum 126/130 (casefold without a boundary), none at 130 |
| v1/v2 voids | jq over `controls/CtlLabelKeyed/receipt.json` and `receipt-v2-warmed*.json` | v1 82/82 `predicate_holds: true`; v2 warmed 130/130 on seeds 2901 and 2902; v2 fresh seed 106/130 |
| no-harm | `git diff --quiet 6c5eb146 7692bf13 -- tools/research-gate.sh` | identical, so the round-1 operability score of 3 stands; the LOG, SKILL and QUALITY diffs are insertions only |
| D1/D2 repair | `prose-check.py` run on committed copies in scratch | `lessons/round-28.md`: 14 hits, exit 1; `lessons/round-29.md` and `knowledge/quote-reopen-r29.md`: 0 hits, exit 0 |

## Per-axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| operability | improved | C1 capability acquisition: before 0/130, after 130/130 on the landed tool under the frozen v3 predicate; capabilities row added; the round-1 scale is unchanged at 3 → 3, as reported |
| depth | unchanged | not claimed; a new knowledge entry and SKILL rows were added, and the existing entries are untouched (insertions only) |
| coverage | unchanged | not claimed; SOURCES grew 45 → 49 with no existing row changed |
| freshness | unchanged | not claimed; 33 earlier Gate quotes were re-opened as a by-product, with no `recheck` or `status` change |
| calibration | unchanged | the claim's limits are disclosed (liveness, mutants, chronology qualified in `lessons/round-29.md:94-109`); the re-run count overstates committed evidence by one run (D2), which is a defect, not a contradiction of repo state |
| adjacency | unchanged | the fetch scope is filed as L0 (fleet `8d77e6c1`) and routed around; no boundary text was rewritten (`falsify/CriticNoHarm.md`) |

## Discernment spot-check

Source: `corpus/lessons/round-29.md` `## Gate`. I re-opened each page on 2026-10-23 with curl and
extracted it with Python `html.parser`, NFKC and whitespace folding.

| Item | Gate decision | Re-opened source | Agree? | Reason |
|---|---|---|---|---|
| S048 | admit | https://unicode.org/reports/tr15/ (200, 141588 B) | agree | quote found at §1.2, 17 words, verbatim |
| S046 | admit | https://www.w3.org/TR/annotation-model/ (200) | agree | quote found under "4.2.4 Text Quote Selector", 25 words, verbatim |
| S047 | admit | https://wicg.github.io/scroll-to-text-fragment/ (200) | agree | quote found in §3.6.1 body text, 13 words; the tool's `ABSENT` is the disclosed missing-`</head>` limit, so the gate correctly read the body rather than trusting the tool |
| S049 | admit | https://docs.python.org/3/library/html.parser.html (200) | agree | quote present in the HTMLParser constructor text, 20 words; my extractor adds spaces around inline `code`, which the frozen contract does not |
| "a `VERBATIM` verdict shows support or truth" | reject | S046 page | agree | the Text Quote Selector "describes a range of text by copying it"; the page has no verification or support semantics |
| design v1 / design v2 | reject (void before data) | `controls/CtlLabelKeyed/receipt.json`, `receipt-v2-warmed*.json` | agree | receipts show 82/82 and 130/130 without fetching, so each design was rightly voided |

SOURCES row check: the S048 row (`corpus/SOURCES.md:58`) names §1.1 and §1.2, and its teaches cell
matches the page. Its ≤25-word quote is the Gate quote above, verified. The census before → after,
which I re-ran on git blobs with the CORPUS.md commands, matches the report: rows 45 → 49,
malformed 0 → 0, tiers A 39 B 1 C 5 → A 43 B 1 C 5, status mined 22 queued 19 rejected 4 →
mined 26 queued 19 rejected 4, no duplicates.

## Trend verdicts

- **expansion: improved.** One admitted capability on uncovered ground. The new entry
  `knowledge/quote-reopen-r29.md` cites four mined tier-A rows, S046 to S049.
- **quality: unprovable-but-better.** D1 to D3 are repaired. QUALITY criteria 23 to 25 each have a
  lesson behind them, and `prose-check.py` is shown able to fail (I re-ran it). 27 of 33 earlier
  Gate quotes re-verified. One admitted Gate quote failed its re-check, though:
  h20, `lessons/round-25.md:70`. It is sentence-cased "A signal" and drops "However,"
  (`falsify/ScoutFreshnessH.md:89`). The round-29 lesson marks it, so quality is not harmed, but no
  correction was appended where the quote lives. The `improved` condition ("no admitted entry
  failing its re-check") is therefore not met.
- **discernment: improved.** The outside spot-check agrees with the gate on four admits and two
  rejects.

## Routed defects (lane fixes next round)

1. D1: Liveness wording. The capabilities row and `claims.md:41-42` say "live". The counter cannot
   show that (cache-only verifier at 130/130, `falsify/CriticClaimDesign.md`). Next round, either
   add a candidate network observation to a new counter version, declared before data, or cite
   `falsify/DiffToolB/landed-fixture.network.json` beside the row as the liveness evidence. Never
   edit the frozen v3 files.
2. D2: Re-run count. The report (`:36`) and SCORECARD say 6 further runs; committed evidence holds
   5. ScoutFreshnessH run 2 (seed 12970099299958901445) cites `rederive3.out`, which records run 3
   (seed 3497534629407128034). Append a dated correction.
3. D3: Mutant survivors. Add fixture classes before data: an unreachable over-long item, a
   head-only or script-only quote, and a case-only edit. These kill MutOrder, MutSkipScript and
   MutCasefold.
4. D4: h20. Append a dated correction to `lessons/round-25.md` for the sentence-cased quote and its
   dropped "However,". Do not rewrite the original.
5. D5: Chronology wording. "Before any data seat had run the counter" (`claims.md:13-14`) should
   read "before either primary executor scored its candidate". Disclose the v1 reference
   implementation (82/82) and the MutateCounter replays beside it. Next round's control-wave context
   should forbid baselines that implement the full contract on the fixture.
6. D6: Uncommitted scratch. Commit the snapshot-control code and its data (or their hashes and
   paths) next to the CriticClaimDesign receipts, so the zero-socket-event assertion can be audited.
7. D7: Carried and operator-owned: the L0 fetch-scope question (fleet `8d77e6c1`), sentinel T1
   (DNS rebinding) and T4 (slow-drip read), and the missing-`</head>` and 2xx-challenge limits.

SHONEN: all 4 boxes are `[~]` with pointers. Box 3 (the counting command runs without oral
context) is checkable by a non-author. The other three need a reviewer's reading of SKILL.md and
PROVINCE.md. Promotion is operator-owned and this closure does not grant it.
