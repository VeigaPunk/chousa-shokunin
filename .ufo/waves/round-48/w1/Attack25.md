# Attack25 — hand-check of absent-defect-register chousa row, ordinal 4 (by lane source)

- lane / round: chousa round4 · row id: **S116**
- register row: `absent-defect-register.md` line 54 (`archive://…/corpus-expansion-1/absent-defect-register.md:54`)
- cited source: `https://aclanthology.org/N18-1074.pdf` (FEVER paper, ACL 2018)
- census verdict (quote-lint-full-v5.json): `ABSENT` ×5 (records 0–4, id S116)
- **Classification: PRESENT** — all five quoted spans occur verbatim in the local campaign capture of the cited source. Not a fabrication; the register's `payload-absent` verdict is a checker blindness on this row.

## Evidence (local captures only, no live fetch)

Capture used: `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/1c15b611118dee97e4105fcf.txt`
(60,153 bytes; `sha256(url)[:24]` of N18-1074.pdf; raw PDF sibling `1c15b611118dee97e4105fcf.raw`, 460,896 bytes, `file`: PDF 1.5; capture mtime 2026-10-23 20:40).

The captured text is a two-column PDF linearization: each physical line holds a left-column fragment and a right-column fragment separated by a space run, and quoted sentences cross that seam (some mid-word, hyphenated: `evi-\ndence`, `Fur-\nthermore`). No match fold in `quote-lint.py` (`FOLD_NAMES`: exact, whitespace, case, no-whitespace, markdown, nfkc, typographic, c-escape, de-wrapped, html, md-link) joins the interleaved halves, so every quoted span fails `match()` and the census records ABSENT.

Hand-check: re-attach the column fragments per line (left half of line N + right half of line N, in order), drop hyphenated line-breaks, normalize whitespace; the five full quote strings then match at:

| quote (census record) | anchor (de-interleaved, whitespace-normalized) | raw capture | |---|---|
| `resulting in inter-annotator agreement of 0.6841 in Fleiss κ (Fleiss, 1971) in claim verification classification, and 95.42% precision and 72.36% recall in evidence retrieval` | char 3992 (left stream) | raw `0.6841` @ 1869; `evi-\ndence retrieval` @ 4849 |
| `We used the June 2017 Wikipedia dump` | char 7876 (left stream) | raw `Wikipedia dump` @ 15288 |
| `in 31.75% of the claims more than one sentence was considered appropriate evidence. Claims require composition of evidence from multiple sentences in 16.82% of cases. Furthermore, in 12.15% of the claims, this evidence was taken from multiple pages.` | char 3566 (left stream) | raw `31.75%` @ 5534; `Fur-\nthermore` @ 5902 |
| `We found that 91.2% of the examples were annotated correctly.` | char 5247 (right stream) | raw `91.2%` @ 20861 |
| `When compared against the super-annotators, all except two annotators achieved > 90% precision and all but 9 achieved recall > 70% in evidence retrieval.` | char 5563 (right stream) | raw `super-annotators` @ 17236 |

All five are the census's own quote strings (record `quote` fields), so nothing is being matched against a loosened variant.

## Why the register is wrong on this row

- The quoted text is un the captured cited source. `absent-defect-register.py` does not re-resolve; it inherits the census's ABSENT findings, so this row's `payload-absent` class and its note (``the quote is in none of them`` → are both a false positive of the match phase, and the inventory of 194 `payload-absent` rows includes S116 in error.
- The failure mode is mechanical: PDF two-column interleave + hyphenated mid-word line-break. None of the eleven folds removes or joins either, which is exactly the class the round-7 adjudication comment warns about (``a fold that cannot see the text reports the row as a fabrication candidate``).
- No live-fetch question arises: the PDF fetch was clean and complete (full 460,896-byte `%PDF-1.5` object), so this is not an `unreachable` row either.

## Notes

- S116 is not one of the four quarantined C3 URLs (register S093/S094/S108/S110), so this finding does not touch the R47-C3 quarantine leg.
- Non-adoption: no register or production edits made; report only.

## Files read

- `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md` lines 54, 256–265
- `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/quote-lint-full-v5.json` (records id=S116; totals: 4152 quotes, 324 absent)
- `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/quote-lint.py` (fold ladder, `FOLD_NAMES` line 635)
- `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.py` (inherits census ABSENT; no re-resolve)
- `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/1c15b611118dee97e4105fcf.txt` (capture) and `.raw` (PDF)
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round47/claims.md`, `corpus/lessons/round-47-verifier-spotcheck.md`
- `…/round-48/w1-spec.json` (item Attack25)

Scratch: `/tmp/chousa-r48-attack25` (removed before finish).
