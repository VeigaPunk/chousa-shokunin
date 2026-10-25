# Round 48 lesson

author: chousa L1 (hyaku run 6)
date: 2026-10-25
base: `d4e6ef09b755a961bdae56566a7dcf0c9db0cfd7`
freeze: `4bbd2348578bb6288c0700dabf37cea04225bfb6`
code landing / measured revision: `671b096e2bd5d5b0994bcd7ab8c17abaf16c62c7`

No external fetch or network egress: L0 `8d77e6c1` remains open. Wave-4 assimilation was quarantine-first: no staged `merge/chousa/` entries or rows were adopted. Round 48 claim C1 is plumbing. The regression set is the prior round-47 held-out set re-opened as a fixed regression, not a fresh estimate of natural-language precision.

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| Forward `used-by` pointer | After adding lane S095 to `corpus/SOURCES.md`, the census found `E11 S095 missing used-by corpus/lessons/round-48.md` because the lesson did not yet exist (`.ufo/waves/round-48/w1/Attack32.md`). | `CORPUS.md` SOURCES rule 1/2 plus the census's E11 existence check. | Create this lesson with its Gate block before the final census. The row remains append-only; final census exit 0 is the positive proof. |
| Control-output transcription | Frozen `controls/before.txt` records `FAIL wanted_rc=0 observed_rc=0` for the `/usr/bin/true` per-case control, which contradicts the counter's `rc == 0` pass condition. The exact re-run prints `observed_rc=1` and `REFINEMENT_CASES=0/5` (`corpus/evidence/round48/controls/before-erratum.txt`). | None before this round; added QUALITY 70. | Preserve the frozen receipt and append the corrected output as a separate erratum file. |

## Spot-check intake

| round-47 routed item | round-48 disposition |
|---|---|
| C1 false-refusal class absent from tool docstring | Fixed in the R48 Named limit: unlisted/out-of-window absence cues, nearby-word binding, and figure-word limits are now explicit. W1 probes found additional cases before the final code change; those exploratory cases were not re-run post-change and are not part of the frozen 12-case result. |
| Five surviving refinement mutants | Five named fixture legs and `mutation-check.py` now kill the implicit-neg, un-neg, un-prefix, repeated-figure, and nested-key mutants; committed after-measurement is 5/5. |
| Operability “improved” vs trade | The old tool is 9/12 on the frozen regression set; the landed tool is 12/12. The set is recycled and bounded, so this is a narrow result, not an entailment or general precision claim. |
| Round-47 C2 recordkeeping | Rechecked: the historical final counter was 94/94, the freeze counter 93/93; 92 is the floor, not an after ratio. The current C2 registry expands to 97/97 after the new R48 checks enter `SKILL.md`. |
| QUALITY 68 R39/R40 gate mismatch | Re-verified all six at their adding commits (6/6); the current tip remains 2/6 because four active receipts bind the pre-R41 gate and `1bd9001` changed that file. This is expected revision drift, not receipt corruption. The receipts were not rewritten or rebound. |

## Gate

Theme: R48 C1 false-refusal regression and the round-47 own-work record grounding it. No corpus knowledge candidate is admitted from the campaign package this round.

### SOURCES row S095

Source opened locally this round: `corpus/lessons/round-47-verifier-spotcheck.md`, accessed 2026-10-25; source URL/path is the lane-local report. Section 2, line 29 quote: “`HeldOutA` refuses 2/12 correctly-reasoned bullets (exit-level 3/12 incl. a05, an over-refusal of a common construction)”. Section 6, line 62 quote: “C1 precision side: document the refusal class in the tool docstring Named limit” (quote ends at “limit” before the source's parenthesis). The first grounds the measured false-refusal cost; the second grounds the routed documentation correction. Lane registry row S095 is tier-A `own-work`, `mined`, used by this lesson.

### Campaign quarantine — full wave-4 slice

`corpus/evidence/round48/assimilation/quarantine-slice` re-derived the 24-row chousa slice from the read-only absent-defect register. Verdicts below describe the register's quote/citation evidence only; no row or package entry was adopted. `present` does not certify the wider source claim; `absent-as-written` does not mean fabricated content when the capture shows a rendering/locator mismatch.

| register id | verdict | evidence pointer / reason |
|---|---|---|
| S077 | present | `.ufo/waves/round-48/w2/QuarantineS077.md` — cited DOI capture is a challenge page, but the named local deep-research artifact contains all four quotes verbatim; this is not `unverifiable`. |
| S080 | absent-as-written | `.ufo/waves/round-48/w2/QuarantineS080.md` — the three Japanese data values exist in separate label/value cells, not as the register's fullwidth-colon concatenated quote. |
| S082 | absent-as-written | `.ufo/waves/round-48/w2/QuarantineS082.md` — capture contains a passive “cited by” construction and a separate “increases” phrase; register splices and reverses the relation. |
| S084 | absent-as-written | `.ufo/waves/round-48/w2/QuarantineS084.md` — actual values are present in table cells, but the quote linearizes the HTML definition list into nonexistent punctuation. |
| S086 | present | `.ufo/waves/round-48/w2/QuarantineS086.md` — both quotes are in the local companion FAQ capture, not the cited homepage capture. |
| S088 | absent-as-written | `.ufo/waves/round-48/w2/QuarantineS088.md` — values are on the PDF table page, but the single-line slash-joined form is not in any extraction. |
| S093 | present — disputed | `.ufo/waves/round-48/w2/QuarantineS093.md` locates all claim/rate components in order at capture chars 1526–1749, interrupted by PDF column text. `.ufo/waves/round-48/w1/Attack24.md` instead finds the full composite quote absent under exact/whitespace folds and calls it absent-as-written. The R47 `QuarReg093` report said present. L1's provisional gate verdict is present-as-substance, not verbatim-contiguous; the closure must re-open and decide this one. |
| S094 | present | `.ufo/waves/round-48/w2/QuarantineS094.md` — all three CFEVER quote spans reconstruct from the cited PDF capture after deinterleaving columns and joining line-wraps. |
| S095 | absent-as-written | `.ufo/waves/round-48/w2/QuarantineS095.md` — one quote is present, two are punctuation/word-form misquotes in the OLE document; the `.txt` sidecar was a lossy binary decode. This is the campaign register id, distinct from lane own-work S095. |
| S096 | absent-as-written | `.ufo/waves/round-48/w2/QuarantineS096.md` — quote 2 is exact; quote 1 and quote 3 splice distinct clauses and swap ISO for GB/T. |
| S104 | present | `.ufo/waves/round-48/w2/QuarantineS104.md` — the text appears in the source's own disclosure; the gate treats that disclosure example as a payload quote, so the register's absent classification is not a fabrication finding. |
| S105 | absent-as-written | `.ufo/waves/round-48/w2/QuarantineS105.md` — quote fragments mostly occur but three strings misstate a PDF table and omit punctuation/line-wraps; content is not fabricated. |
| S108 | present | `.ufo/waves/round-48/w2/QuarantineS108.md` — the abstract sentence is in the capture; the text extractor changes spacing around `Supported`, κ and its LaTeX alt-text. |
| S110 | present | `.ufo/waves/round-48/w2/QuarantineS110.md` — all three quotes occur in the PDF capture after deinterleaving and joining hyphenated lines. |
| S111 | present | `.ufo/waves/round-48/w2/QuarantineS111.md` — the PRISMA phrase appears in stream-order/raw extraction; `-layout` interleaves columns. |
| S112 | absent-as-written | `.ufo/waves/round-48/w2/QuarantineS112.md` — Q1/Q2 are present modulo layout; Q3 swaps ISO 690 for GB/T and changes punctuation/line-wrap. |
| S114 | present | `.ufo/waves/round-48/w2/QuarantineS114.md` — both data spans occur verbatim inside a source HTML comment; the checker strips comments. |
| S116 | present | `.ufo/waves/round-48/w2/QuarantineS116.md` — all five quotes appear in plain `pdftotext` output; `-layout` interleaves columns. |
| S120 | present | `.ufo/waves/round-48/w2/QuarantineS120.md` — three Japanese spans are in the DOCX `word/document.xml`; the `.txt` sidecar was not a text rendering. |
| S125 | present | `.ufo/waves/round-48/w2/QuarantineS125.md` — the captured OLE document contains the evidence after UTF-16LE/LibreOffice extraction; its `.txt` was mojibake. |
| S100 | present | `.ufo/waves/round-48/w2/QuarantineS100.md` — the cited local artifact and all four gate quotes are present; the no-locator parser missed a parenthetical URL label and lane-root path. |
| S101 | present | `.ufo/waves/round-48/w2/QuarantineS101.md` — pinned local artifact matches digest/size and all four quote spans; no-locator parser misses parenthetical URL and lane-root path. |
| S102 | present | `.ufo/waves/round-48/w2/QuarantineS102.md` — all three quoted spans occur in the pinned artifact; same locator parser defect. |
| S103 | present | `.ufo/waves/round-48/w2/QuarantineS103.md` — pinned artifact and all four spans resolve; same no-locator parser defect. |

Quarantine tally at L1: 16 present (including S104's literal disclosure text), 8 absent-as-written, 0 unverifiable. These are curation verdicts only; the set remains quarantined and no package row is appended. S093 is explicitly disputed as above.

### R48 C1 gate and `considerthese`

The after-measurement at `corpus/evidence/round48/measure-after.txt` is over the exact code commit and shows C1, the legacy R47 leg, and five named mutant cells pass. The name-keyed control in `controls/name-key-control.txt` passes `c1-count` but fails the frozen `mutation-check` when installed at the default tool path; this rejects that simple no-read shortcut, not every possible substitute. The 12 cases are recycled R47 regressions, not a fresh precision estimate. W2 `AttackPrecision.md` disputes `a05` as an ambiguous “correct” label (11/12 are unambiguous); the closure must independently adjudicate it. Until then the numeric metric passes, but human label validity is not independently verified and no semantic-precision claim is made.

`considerthese/2026-10-24.md:64-66`'s remaining “read-only cloud-agent” part of receipt re-verification is refused here because it explicitly requires approval and L0 `8d77e6c1` is still open; the local pinned/tip recheck was completed. Flip condition: operator authorization for the cloud-agent run. No other still-unimplemented proposal was selected; the three other proposals in that file are already reflected by QUALITY 61, 62 and 64.

### Outside spot-check

This Gate records the author-lane decisions and the S093 disagreement. No dispatched L2 seat is a non-author. The hyaku closure judge re-opens at least one present and one absent-as-written row after this report; its verdict is not pre-claimed here.
