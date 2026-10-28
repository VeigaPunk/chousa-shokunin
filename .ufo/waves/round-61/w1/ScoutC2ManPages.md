# ScoutC2ManPages — S134/S135 quote locations

Sources reopened on this host, no network. Package `man-pages 6.19-1`. Both pages' `.TH` lines are dated 2026-02-08, "Linux man-pages 6.19" (`/usr/share/man/man2/open.2.gz`, `rename.2.gz`). Render matches `c2-count.py`: `LC_ALL=C.UTF-8 MANWIDTH=1000 man -l FILE` then `col -bx`. Roff line numbers are from `zcat` of those same files. All six entry quotes occur as exact substrings of the rendered text.

## Q1–Q6

Every quote sits under **DESCRIPTION**. Q1–Q3 are also inside a flag tag. Q4–Q6 are in the `rename()` lead, before `.SS renameat()`.

- **Q1** (20 words). Rendered open line 147. Roff open lines 522–525 (`.I path` on 523, `.BR ELOOP .` on 525). Tag **O_NOFOLLOW** (roff 521, rendered 146). Section heading rendered line 32, roff `.SH DESCRIPTION` line 44.
- **Q2** (12 words). Rendered open line 147, the next sentence of that paragraph. Roff 526–527: the source breaks between "be" and "followed." with no hyphen. Same O_NOFOLLOW tag.
- **Q3** (21 words). Rendered open line 123. Roff 418–424; line 419 is a `.\"` comment and is not rendered. Tag **O_EXCL** (roff 407, rendered 120). Same DESCRIPTION.
- **Q4** (23 words). Rendered rename line 46. Roff 92–97. Heading DESCRIPTION (roff `.SH` line 45, rendered line 33). `.SS renameat()` starts at roff 98 / rendered 48, after this paragraph.
- **Q5** (23 words). Rendered rename line 38, beginning after "If newpath already exists, ". Roff 60–63 (the quote starts mid-line 60). DESCRIPTION, the existing-`newpath` paragraph.
- **Q6** (19 words). Rendered rename line 38, the next sentence. Roff 64–68. Same paragraph and heading.

The entry's anchor column matches these headings: O_NOFOLLOW, O_NOFOLLOW, O_EXCL, DESCRIPTION, DESCRIPTION, DESCRIPTION.

## What `col -bx` and normalisation did

`col -bx` changed nothing. Under `LC_ALL=C.UTF-8` and `MANWIDTH=1000`, `man -l` stdout and `col -bx` stdout were byte-identical: open 44181 bytes, rename 13286 bytes. Backspace 0, ESC 0, tab 0, CR 0, U+00AD 0. No rendered line ends with `-` (open 516 lines, rename 210). Bold and italic requests (`.B`, `.I`, `.BR`, `.IR`) are already plain text in `man` stdout, so there was no overstrike for `col -bx` to strip and no hyphenation on either page.

The counter's `norm` (`re.sub(r"\s+", " ", s).strip()`) does not alter Q1–Q6. Each quote is already single-spaced, and a search for the quote string hits the rendered line before normalisation. Spacing that is real, and outside the quote span:

- List indent. O_NOFOLLOW and O_EXCL bodies (Q1–Q3) have 12 leading spaces. The Q4–Q6 paragraphs have 5. The quotes are interior substrings.
- Sentence spacing. Rendered open line 147 has two spaces in `ELOOP.  Symbolic` (between Q1 and Q2). Rendered rename line 38 has two spaces in `missing.  However` (between Q5 and Q6).
- Formatter resolution of roff, already done before `col`. `.BR open ()`, `.BR ELOOP .`, and `.BR rename ()` use a space as font syntax; the rendered words are `open()`, `ELOOP.`, and `rename()`. Q3 uses that rendered `open()`. The comment on roff line 419 is dropped, so "followed:" and "if" join with one space. Source newlines inside Q2 and Q4–Q6 join as one space. No `\%` in either roff file's quote spans (open's `\-` hits are elsewhere: the NAME line, RETURN VALUE, NOTES).

## Further quotes

Four sentences, each at most 25 words by `str.split()`, that bear on the entry's claims.

1. **25 words. Qualifies Q1.** "If path is a symbolic link and the O_NOFOLLOW flag is also specified, then the call returns a file descriptor referring to the symbolic link." Rendered open line 189 (12-space indent outside the span). Roff 693–698. Heading DESCRIPTION, tag **O_PATH** (`.TP` roff 582, tag 583, rendered tag line 162). With `O_PATH`, `O_NOFOLLOW` returns an fd to the link instead of failing.
2. **20 words. Bears on claim 4.** "If newpath exists but the operation fails for some reason, rename() guarantees to leave an instance of newpath in place." Rendered rename line 42 (5-space indent). Roff 78–84. Heading DESCRIPTION. A failed rename leaves an existing `newpath` in place.
3. **11 words. Prefix counterpart of Q2, for rename.** "Too many symbolic links were encountered in resolving oldpath or newpath." Rendered rename line 122 (tag and body on one line: `ELOOP` then two spaces, then the sentence). Roff 335–337; `.IR oldpath " or " newpath .` renders as `oldpath or newpath.` Heading **ERRORS** (rendered line 104, roff `.SH` line 281), tag ELOOP. `rename` follows symbolic links while resolving the path.
4. **13 words. Bears on claim 3.** "Don't overwrite newpath of the rename. Return an error if newpath already exists." Rendered rename line 70, tag **RENAME_NOREPLACE** on line 69. Roff 171–176; `.B RENAME_NOREPLACE` on 170; `.SS renameat2()` at roff 145 / rendered 61. Heading DESCRIPTION. The rendered line has two spaces between the sentences (`rename.  Return`). Those spaces are already in `man` stdout. `norm` collapses them, so this single-space wording matches only after normalisation; the exact single-space string is not a substring of the raw rendered line. This flag refuses the default overwrite.

## Evidence

- `pacman -Q man-pages` → `man-pages 6.19-1`.
- `zcat` `.TH`: `.TH open 2 2026-02-08 "Linux man-pages 6.19"` and `.TH rename 2 2026-02-08 "Linux man-pages 6.19"`.
- Python over the `LC_ALL=C.UTF-8 MANWIDTH=1000` render: `identical=True` for both pages; `exact_lines` Q1=147, Q2=147, Q3=123, Q4=46, Q5=38, Q6=38; extras X1=189, X2=42, X3=122; X4 `exact_lines=[]` and `norm_lines=[70]`. `eol_hyphen_lines` count 0 on both pages. Raw window at "trailing component" is plain UTF-8, no backspace: `O_NOFOLLOW\n            If the trailing component...`.
- No tool was installed.

Scratch `/fast/scratch/hyaku/chousa-r61/ScoutC2ManPages` held the renders and the roff copies and was removed after this report.

VERDICT: Q1_Q6_LOCATED=6/6 extra_quotes=4
