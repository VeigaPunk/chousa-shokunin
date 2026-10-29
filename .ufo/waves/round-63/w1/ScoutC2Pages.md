# ScoutC2Pages — round 63, w1 — C2 quote location (S142, S143)

Scope: re-open the sources of rows S142 (git-rev-parse(1)) and S143 (gitrevisions(7)) and locate Q1–Q7 of
`corpus/evidence/round63/controls/c2-positive-entry.md`. No edits to the lane, no git writes, no network.
Scratch `/fast/scratch/hyaku/chousa-r63/ScoutC2Pages/` created and removed before this report.

## Findings

1. All seven entry quotes are verbatim in the rendered pages and in the raw roff. Q1–Q4 are in gitrevisions(7),
   Q5–Q7 in git-rev-parse(1), matching the entry's S142/S143 attribution.
2. Rendering changes nothing in Q1–Q7. `col -bx` removes only bold/italic escapes (`\fB`, `\fI`, `\fR`). Q7's
   `$VAR` and `^{type}` are bold in roff and plain in the render. The quotes contain no apostrophes, no
   non-breaking spaces and no soft hyphens.
3. Whitespace change seen elsewhere (not in Q1–Q7): the refname entry renders `E.g.  master` with two spaces. The
   roff source has `E\&.g\&.` at a line end, so roff inserts sentence spacing. The text is not in the source.
4. Curly apostrophes: rendered U+2019 counts are 7 (gitrevisions) and 10 (git-rev-parse), equal to the raw
   `\(cq` escape counts (7 and 10). No non-ASCII bytes, no `\~`, `\ ` or `\%` escapes in either raw file.
   Bullets: 7 rendered U+2022 in git-rev-parse, 14 raw `\(bu` (the 14 includes the option-list bullets, not
   all rendered; INFERENCE on the mapping, not separately counted).
5. The string `target branch’s` does not occur in either rendered page or in either raw file (grep, case
   insensitive, for `target` and `branch\(cq`). The apostrophe example in the brief is not from these pages.

## Q1–Q7 location table

Line numbers: "rendered" = `MANWIDTH=1000 man -l FILE | col -bx`; "raw" = `zcat FILE` (roff source).

| Q | Page | Rendered line | Raw roff line(s) | Text changed by render? | Nearby sentence limiting scope |
|---|---|---|---|---|---|
| Q1 | gitrevisions(7) S143 | 22 | 62 | no | Same paragraph: "if there is no other object in your repository whose object name starts with dae86e" (inside Q2 quote) |
| Q2 | gitrevisions(7) S143 | 22 | 62 | no | Its own limit clause is the scope ("if there is no other object ..."); the 4-digit floor is on git-rev-parse rendered 119 |
| Q3 | gitrevisions(7) S143 | 115 | 405–409 | no (roff `\fI<rev>\fR` markup removed) | "...dereference the object at <rev> recursively ... (in which case, barf)" (same paragraph, before Q3) |
| Q4 | gitrevisions(7) S143 | 131 | 470–472 | no (`\fI:\fR` removed) | "A path starting with ./ or ../ is relative to the current working directory." (rendered 131, raw 472–476) |
| Q5 | git-rev-parse(1) S142 | 75 | 193–194 start; quote's last word ("variable") on the next roff line, not separately printed (INFERENCE on line 195) | no (`\fBcore\&.abbrev\fR` bold removed; `\&` zero-width) | Same entry opens "Same as --verify but shortens the object name to a unique prefix with at least length characters." (rendered 75) |
| Q6 | git-rev-parse(1) S142 | 119 | 325 | no | "The <prefix> must be at least 4 hexadecimal digits long to avoid listing each and every object in the repository by mistake." (rendered 119, same entry) |
| Q7 | git-rev-parse(1) S142 | 64 | 153–158 | no (`\fB^\fR`, `\fB$VAR\fR` bold removed; quote text intact) | Lead-in in the --verify paragraph (rendered 62–64): "If you want to make sure that the output actually names an object ..."; and rendered 64 continues "To make sure that $VAR names an existing object of any type, git rev-parse "$VAR^{object}" can be used." |

Located count: rendered 7/7 (verified by a whitespace-normalised substring search, one hit each for Q1–Q7);
raw 7/7 (Q1, Q2, Q4, Q5, Q6 by windowed search; Q3 and Q7 by reading the raw lines after the windowed search missed
them because of roff markup and line splits).

## Extra located quotes (short name and tag name resolution)

All in gitrevisions(7), rendered page, `<refname>` entry (S143). Each is contiguous and 4–25 words.

- E1 (21 words), rendered 28, raw 78–83: "If you happen to have both heads/master and tags/master, you can explicitly say heads/master to tell Git which one you mean."
  Scope: applies only when both names exist; the page then says to write `heads/master` explicitly.
- E2 (5 words), rendered 34, raw 131–133: "otherwise, refs/tags/<refname> if it exists"
  Scope: this is rule 3 of 6 and applies only after `$GIT_DIR/<refname>` and `refs/<refname>` fail to match; the
  rule list starts only when a name is ambiguous (E4).
- E3 (14 words), rendered 28, raw 75–78: "A symbolic ref name. E.g. master typically means the commit object referenced by refs/heads/master."
  Scope: states what a short `<refname>` such as `master` means; the page gives no tag example for this sentence.
- E4 (15 words), rendered 28, raw 83–85: "When ambiguous, a <refname> is disambiguated by taking the first match in the following rules"
  Scope: the rules apply only when the name is ambiguous; the rule list follows immediately (rendered 30–40).

## Caveats

- Git version is the one installed with the pages (2.56.0-1); the render and raw checks are on this host only.
- Raw line numbers for Q5 are a range (193–194 shown; the continuation line was not printed); flagged above.
- The bullet counts in finding 4 are counted, not mapped line by line; the mapping is INFERENCE.
- Quote-to-claim entailment is out of scope for this item.

VERDICT: Q1_Q7_LOCATED=7/7 extra_quotes=4
