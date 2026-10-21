# FSourceCochrane — round26 attempt1 falsification: S037 Cochrane LSR guidance

Seat: `ChousaR26R.FSourceCochrane` (scout, axis: freshness). Author-lane advice only;
not an outside judge or SHONEN verdict. Date 2026-10-21.

## Verdict

**S037 is not falsified.** The Gate quote is verbatim, 14 words, and sits on page 19 in §4.3.4. The
source does separate the search cadence from the update cadence, and the row's
"intervention" scope matches what the document says. Two low-severity residuals remain:
the row's `teaches` text leaves out the source's own condition on fixed-interval updating, and
the anchor text is not a literal substring of the PDF. One freshness gap is unresolved:
nobody checked whether a newer guidance version replaces this one.

## Target identity

- Measured revision: `0e9784bd52eca456b24d0bc40921480a47f91a2b`, read from
  `corpus/evidence/round26-measured-revision.json`. `git cat-file -t` returned `commit`.
  The lane `HEAD` observed at the time was the same commit.
- Sandbox: `/tmp/chousa-r26-falsify-FSourceCochrane/tree`, created with
  `git archive 0e9784bd… | tar -x` (rc 0).
- `sha256sum` in the sandbox matched the measured-revision manifest:
  - `corpus/SOURCES.md` `8308e629…5aa9`
  - `corpus/knowledge/recheck-due-r26.md` `a0995b78…7d5e`
  - `corpus/QUALITY.md` `2428baaf…abc6`
  - `corpus/evidence/round26-claims.md` `dcbe2b5f…f1c`
- Claim base (not graded directly): `ba3333254dd337658a4f25e7a9471f9cf4e4567e`.

## Source reopened (static public document named by the row; no other target probed)

- URL: the S037 row URL `…/Transform/201912_LSR_Revised_Guidance.pdf`.
- `curl -sSL` returned rc 0, HTTP 200, `application/pdf`, 1,457,761 bytes.
- PDF sha256: `42ef5ecdeb2770474fb33fdd0c37c4686d61e77d536d38ad87d1e80283b85a70`.
- `pdfinfo`: 60 A4 pages; author Anneliese Synnot; CreationDate 2019-12-19 21:50:26 -03,
  ModDate 2019-12-19 22:39:18 -03.
- HTTP `HEAD`: `last-modified: Thu, 16 Oct 2025 10:13:15 GMT`, etag `"163e61-64143dd825e8e"`.
  The server mtime is newer than the PDF's internal ModDate. The content still identifies
  itself as December 2019, so the newer mtime is not evidence that the content changed.
- Text was extracted with `pdftotext` (poppler, `/usr/bin`, already installed).

## Checks and observations

| # | Attack | Observed | Result |
|---|---|---|---|
| 1 | Is the Gate quote (`lessons/round-26.md:43`) exact? | After whitespace normalization, it is an exact substring of page 19: “updated on a fixed-interval schedule approved by the editorial team (e.g. every four months).” A Python string-equality check against the lessons quote returned True. | Holds. 14 words (limit 25). |
| 2 | Is the location right (§4.3.4, p19)? | The quote is on physical page 19, and the printed header and footer both read 19. It sits under heading “4.3.4 Once the review is in living mode”. The table of contents (p2) lists 4.3.4 at p19. | Holds. |
| 3 | Is the version right? | The title page reads “Version December 2019”. Page 4 identifies it as “Version 1.0 … released in December 2019”. | Holds. |
| 4 | Does the source separate searching from updating? | p19: “The ongoing searches are run and screened at their pre-specified frequency (i.e. monthly …)”, versus “The LSR is updated according to the decisions specified in the protocol.” §4.3.4.2 (p23) has teams decide in advance whether to proceed when “A scheduled update is due … but the ongoing searches have identified no new evidence”. That only makes sense if searching and updating run on separate cadences. | Supported. The word “separate” in the row is the lane's paraphrase, but a fair one. |
| 5 | Does the row's “intervention” scope hold? | p4: guidance is for “living systematic reviews of interventions published in the … CDSR”. p12 §4.1: “developed with a standard Cochrane intervention review in mind. The Cochrane LSR pilot only included intervention reviews.” | Supported. |
| 6 | Does the row keep the source's scope qualifiers? | The source makes the fixed interval conditional and second-best. p19: “For LSRs where a high volume of new evidence is anticipated, however, it may have been deemed more feasible…”, after “Ideally, updates will occur whenever new evidence likely to impact the review conclusions is identified”. Box 2 (p16) repeats both points and adds “author teams consult with the editorial team regarding which of the above two options to use.” The S037 `teaches` cell (`SOURCES.md:47`, “Review updates may follow a protocol-specified fixed interval approved by the editorial team; this is separate from ongoing evidence searches”) drops both the high-volume condition and the impact-driven default. The knowledge entry only says “in the specified setting” (`recheck-due-r26.md:11-12`), without naming the setting. The Gate admission boundary also omits them. | **Residual R1 (low).** Not a misquote; “may” keeps the permission accurate. But under QUALITY 7, the stated scope is wider than the source's. C2 is unaffected: the entry labels the generic `Nd` policy as `[INFERENCE]` and says neither source prescribes a universal 90-day cadence (`recheck-due-r26.md:12-15`). |
| 7 | Is the anchor literally findable? | The row anchor (`SOURCES.md:47`) is “section4.3.4 p19; Version December2019”. The entry header (`recheck-due-r26.md:1`) uses the same form. A byte check found no separator at all between `section` and `4.3.4`, or between `December` and `2019`: these are missing spaces, not NBSP. Neither `section4.3.4` nor `Version December2019` appears in the PDF text; `December 2019` and `4.3.4` do. | **Residual R2 (low, cosmetic).** The location can still be found. The same missing space before digits recurs elsewhere (for example “universal90-day”, “frozen29”, “Claim2”), so it looks like a systematic authoring artifact. |
| 8 | Freshness: is a newer guidance version in force? | The PDF has no notice that it has been replaced. Page 4 says “we expect this guidance will continue to evolve.” Neither the registry row nor the entry records a check for a later version. S037 recheck is `180d` from opened 2026-10-21, giving due 2027-04-19. The entry's `90d` from verified-at 2026-10-21 gives 2027-01-19 (computed with Python `datetime`). | **Unresolved (U1).** I did not probe pages outside the named PDF, as the bounds require. Whether a later Cochrane LSR guidance replaces Version 1.0 is unknown. |

## Where the procedure lives (not a defect)

The entry header labels the anchor “section4.3.4 p19, fixed-interval updates”. Page 19
holds the permission sentence. The fixed-interval procedure itself is in §4.3.4.2 (p23),
and the What's New handling is in §4.4.1.3 (p26). If the lane ever cites S037 for how
fixed-interval updates are run, as opposed to the fact that they are allowed, it should
use the p23 anchor.

## Suggested remedies (advice only; nothing in production was edited)

- **R1:** qualify the S037 `teaches` cell and the entry sentence. Suggested wording:
  “…a protocol-specified fixed interval approved by the editorial team, when a high volume of
  new evidence is anticipated; impact-driven updating is the stated ideal (p19; Box 2 p16).”
- **R2:** write the anchor as “section 4.3.4, p19; Version December 2019 (v1.0)”.
- **U1:** at the 2027-04-19 recheck, open Cochrane's LSR guidance landing page and record
  whether Version 1.0 has been replaced. Until then, keep presenting S037 as a December 2019
  version-pinned source.

## Commands run (exit codes)

1. `git cat-file -t 0e9784bd…`; `git archive 0e9784bd… | tar -x -C …/tree`; `sha256sum` (4
   files); `git rev-parse HEAD` — rc 0.
2. `curl -sSL -A "Mozilla/5.0" -o lsr.pdf <S037 URL>` — rc 0, HTTP 200. `file`, `sha256sum` — rc 0.
3. `pdfinfo lsr.pdf`; `pdftotext -layout lsr.pdf all.txt`; a per-page `grep` loop. The final
   `grep -n` for `4\.3\.4` returned rc 1 (no match) because `-layout` output separates `4.3.4`
   from the heading text with spaces. This was a pattern-anchoring problem in a probe, not a
   source finding; the per-page dumps located the text.
4. `pdftotext -f 19 -l 19` (also pages 1–2, 4–5, 23) — rc 0.
5. Python normalization and exact-substring checks; byte inspection of the anchor; `curl -sSI` — rc 0.
6. Python `date + timedelta` for the due dates — rc 0.

No build, selftest, lint, formatter, or amplification probe was run, as the assignment requires.

## Tools

No installs or updates. Used existing `/usr/bin/pdftotext`, `/usr/bin/pdfinfo`,
`/usr/bin/python3` and `curl`. No pacman transactions.
