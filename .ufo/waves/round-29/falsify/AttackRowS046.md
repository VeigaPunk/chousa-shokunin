# AttackRowS046 — scoped falsification review

## Verdict and axes

**HOLDS for S046 quote operability; WRONG access-date provenance.** This is not a judgment of the complete frozen C1 predicate. Axes examined: operability, source/quote fidelity, scope discipline, provenance, and no-harm.

Attacked `corpus/SOURCES.md:56` and every use of S046 in `corpus/knowledge/quote-reopen-r29.md`. Independently opened the registered URL, https://www.w3.org/TR/annotation-model/#text-quote-selector . The normal reader returned W3C metadata only; opening the same URL as raw HTML exposed the actual document and cited section. No other source URL was opened.

## Per-cell verdicts

| Cell | Verdict | Evidence / qualification |
|---|---|---|
| id | OK | S046 identifies the row cited by the entry. |
| source | OK | Page title is `Web Annotation Data Model`; visible heading says `W3C Recommendation 23 February 2017`. |
| kind | OK | `spec`: this is the Recommendation's own selector model. |
| tier | OK | A is justified for what this primary Recommendation specifies, not for the lane's implementation or claim truth. |
| scope | OK | Exact text plus context is its model. Its `exact` property is explicitly text **after normalization**; the row does not claim byte equality or endorse this tool's particular matching algorithm. |
| anchor | OK | `<section id="text-quote-selector">` exists, headed `4.2.4 Text Quote Selector`; its opening paragraph is the cited passage. |
| teaches | OK | The opening paragraph explicitly says copied text and immediately preceding/following text distinguish repeated sequences. |
| status | OK | `mined` is consistent with the actual source citation and teaching at entry lines 3 and 67–70. |
| opened | WRONG | `2026-10-23` is a future completed-access assertion under the supplied current date, 2026-10-22. Independently, `.ufo/waves/round-29/build/ScribeKnowledge.md:6` explicitly records actual source opening on 2026-10-22; its original draft `ScribeKnowledge/quote-reopen-r29.md:4` also says 2026-10-22, whereas the landed entry's `verified-at` is 2026-10-23. I cannot attest any historical builder access beyond those conflicting records. |
| recheck | OK | `365d` is a valid lane-selected cadence, not presented as a W3C requirement. The entry's separate 180d cadence does not make the source page say anything else. |
| used-by | OK | The named knowledge file exists and uses S046 explicitly. |

Normative nuance: the section requires exactly 1 `exact` property and says there **SHOULD** be exactly 1 `prefix` and 1 `suffix`, with no more than 1 each. Calling context optional does not contradict a mandatory requirement, but it must not be read as the Recommendation positively recommending omission. No conformance claim is made here.

## Quote and scope check

**Quote: OK.** Copied verbatim from the independently opened page, with only the entry's Markdown line wrapping removed (24 words):

> some of the text immediately before (a prefix) and after (a suffix) it to distinguish between multiple copies of the same sequence of characters.

The page's opening sentence begins `This Selector describes a range of text by copying it, and including` immediately before that quotation. See the recorded passage in `.ufo/waves/round-29/falsify/AttackRowS046/source-excerpt.txt`.

**Beyond-scope use: OK — none found in this entry.** Lines 67–70 contrast the selector's context with the tool's lack of prefix/suffix support and distinguish presence from selecting a particular copy. The entry does not attribute NFKC, its boundary rule, or claim validation to S046. Lines 53–59 expressly explain normalized rather than byte-identical equality.

## Landed-tool exercise

Created only the requested one-row input, `.ufo/waves/round-29/falsify/AttackRowS046/items.tsv`, containing the complete 24-word S046 quotation above.

From `/home/vgpnk/Projects/shokunin/chousa-shokunin`, ran:

```sh
timeout 120 python3 tools/quote-reopen.py verify --items /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/falsify/AttackRowS046/items.tsv
```

Exit **0**; output:

```text
QUOTE_REOPEN	s046-entry-quote	VERBATIM	matched in normalized page text
QUOTE_REOPEN_SUMMARY verbatim=1 absent=0 too_long=0 no_source=0 unreachable=0
```

**Tool verdict: OK.** The exact quotation is present on the independently opened page and is below the 25-word limit. Unlike the documented S047 case, S046's raw HTML explicitly closes `</head>` before `<body>`, so the reported S047 extraction failure does not apply to this source. Output is preserved in `.ufo/waves/round-29/falsify/AttackRowS046/verifier-run.txt`.

## Counterexample, impact, smallest correction, limits

- Counterexample found: the row's completed access date and the landed entry's verification date do not respect the supplied chronology; the original knowledge-author report and draft explicitly preserve a different actual opening date. This affects **provenance**, not the observed S046 matcher result.
- Smallest safe correction: preserve the actual evidenced source-open date, and distinguish it from a separately evidenced later re-location date rather than replacing it. Under this assignment's date, do not record 2026-10-23 as an already completed operation. No matcher change, frozen-claim change, counter change, fixture edit, or re-scaling is warranted by this result.
- Limits: 1 S046 quote, 1 landed-tool invocation; no complete 130-item counter run, S047 fetch, broader algorithm audit, or claim-truth judgment. A successful quote location does not prove W3C-selector conformance or C1 as a whole.
- No-harm: no production, frozen, Git-index, or jj-state edits; no subagents, background jobs, test servers, installs, or updates. The single foreground command completed; no process tree remains from this review. Only this report and its own evidence directory were written.
