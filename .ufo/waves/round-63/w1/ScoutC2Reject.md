# ScoutC2Reject — round 63, wave w1 (scout, item ScoutC2Reject)

Scope: find the rejection the round's Gate needs for C2 (what pins a citation to a git revision). Three further local sources opened on the same topic and judged against S142 (git-rev-parse(1)) and S143 (gitrevisions(7)). Read-only: no lane, fleet or git writes; scratch under /fast/scratch/hyaku/chousa-r63/ScoutC2Reject/, deleted before yield.

## Findings

| # | source (installed page) | judgment | teaches beyond S142/S143? |
|---|---|---|---|
| 1 | gitglossary(7) `object name` and `SHA-1` entries | **REJECT (recommended S145)** | No. Restates S143 Q1 with a hedge and conflates object name with SHA-1, which the lane probe refutes for sha256. |
| 2 | git-describe(1) | ADMIT as a further row (narrow; not counted) | One new fact: by default only annotated tags are candidates, so a describe name pins a commit through an abbreviation that drifts. Other content repeats S142 (`core.abbrev`) and S143 (abbreviation uniqueness). |
| 3 | git-cat-file(1) | ADMIT as a further row | Two new facts: `%(objectname)` expands an input name to the full hex object name, and batch mode prints a distinct `ambiguous` marker. S142 offers `--disambiguate` (a list) and `--verify` (a yes/no), not either of these. |

Calibration: the glossary reject rests on verbatim text with no other reading (confidence high). The describe admit rests on one new sentence (medium; the admit is narrow on purpose). Neither judgment touches the frozen counter, which fixes its row ids to S142, S143, S144 (`c2-count.py` line 64). I did not run the counter, so "not counted" is INFERENCE from that tuple, not an observed result.

## Quotes (rendered `MANWIDTH=1000 man -l FILE | col -bx`, git 2.56.0; footers read `Git 2.56.0`)

Glossary (`/usr/share/man/man7/gitglossary.7.gz`):
- L148: "The object name is usually represented by a 40 character hexadecimal string." (13 words)
- L148: "Also colloquially called SHA-1." (4 words)
- L329: "In the context of Git used as a synonym for object name." (11 words)

S143 cross-check (`/usr/share/man/man7/gitrevisions.7.gz`, rendered line 22): "The full SHA-1 object name (40-byte hexadecimal string), or a leading substring that is unique within the repository." (the S143 Q1 sentence; confirmed present, so the glossary's 40-character point is already covered).

Probe cross-check (`corpus/evidence/round63/controls/candidate-git-revision-probe.txt`, line 4): `PROBE P02 sha256-full-name-length observed=64 expected=64 ok`.

git-describe(1) (`/usr/share/man/man1/git-describe.1.gz`):
- L14: "By default (without --all or --tags) git describe only shows annotated tags." (14 words)
- L35: "(which will vary according to the number of objects in the repository with a default of 7)" (repeats S142 `--short` / `core.abbrev`)
- L89: `"-g975b" suffix alone may not be sufficient to disambiguate these commits.` (11 words; repeats S143 Q2 uniqueness, applied to a describe name)
- L92: "Annotated tags will always be preferred over lightweight tags" (9 words; a describe-only preference)

git-cat-file(1) (`/usr/share/man/man1/git-cat-file.1.gz`):
- L35: "Exit with zero status if <object> exists and is a valid object." (repeats S142 `--verify`)
- L169: "The full hex representation of the object name." (8 words; the `%(objectname)` atom, new)
- L212: "an ambiguous short sha), then cat-file will ignore any custom format and print:" (13 words; new)
- L214: "<object> SP ambiguous LF" (the marker line, new)
- L26: "see the "SPECIFYING REVISIONS" section in gitrevisions(7)" (pointer only; repeats S143)

## Reasons

1. **gitglossary(7): reject.** Its `object name` entry (L147-148) gives the 40-character length as "usually" (hedged) and so is weaker than S143 Q1, which states the 40-byte form plainly. Its `SHA-1` entry (L328-329) and "Also colloquially called SHA-1" (L148) make object name a synonym for SHA-1; the lane's own probe shows a sha256 full name is 64 hex digits (P02). The glossary teaches no spelling, peeling, uniqueness or tag/blob rule. It is a stray for the pinning question. Flip condition: admit it if an entry claim needs the term "object name" defined, cites the L148 sentence with its "usually" hedge kept, and cites P02 for the sha256 case, since the page never states that case.

2. **git-describe(1): admit (narrow).** The one new teaching is that a describe name carries an abbreviation and, by default (L14), only annotated tags are candidates. So a citation written as a describe name pins its commit only through an abbreviation S143 Q2 says can stop being unique (L89 is the same drift, given as an example). Not counted; it earns a row only if an entry claim cites describe output as a citation form.

3. **git-cat-file(1): admit.** `%(objectname)` (L169) turns a short citation into the full object name a pinned citation should record, and batch mode reports an ambiguous short name as a distinct line (L212-214). Neither appears in S142 or S143. Its `-e` and `<object>` entries repeat `--verify` and the SPECIFYING REVISIONS pointer.

## Recommended S145 (rejected) row — not inserted anywhere

Row shape copied from the live registry (`corpus/SOURCES.md`, rows S137 and S141 are the `rejected` precedents; 11 cells; `teaches` opens `REJECTED:` and ends `flip:`). Source cell names the page as the installed file and marks the package as INFERENCE (the footer says `Git 2.56.0`; the Arch package name was not confirmed with `pacman -Qo`, which the pacman guard blocks).

| S145 | gitglossary(7) — Git 2.56.0 manual page (footer `Git 2.56.0`), the installed /usr/share/man/man7/gitglossary.7.gz, of the Arch package git 2.56.0-1 [INFERENCE: package not confirmed], rendered with MANWIDTH=1000 man -l FILE then col -bx | docs | A | what git 2.56.0's glossary says the terms object name and SHA-1 mean; not the object database, not sha256 repositories, not what a revision spelling names | the `object name` entry (rendered lines 147-148) and the `SHA-1` entry (rendered lines 328-329), git 2.56.0 page | REJECTED: "object name" restates S143's 40-byte rule with a hedge ("usually", line 148) and calls object name "colloquially" SHA-1 (line 148), which probe P02 refutes for sha256 (observed 64); it pins nothing S142 or S143 do not already say; flip: admit if an entry claim needs "object name" defined, cites line 148 with its hedge kept, and cites P02 for the sha256 case | rejected | 2026-10-28 | 180d | — |

## Unknowns and limits

- The page dates are not in the rendered footers (`Git 2.56.0` only); S142's `2026-09-27` is not re-checked here.
- The rendered line numbers are from this host's `col -bx` output at `MANWIDTH=1000`; another render width moves them.
- The describe and cat-file admits are recommendations; neither is inserted, and their use in an entry is for the L1 to decide.
- Entailment is not checked: "pins nothing new" is my reading of the quotes, not a machine check.
- The lane's frozen `c2-count.py` was not run; the "not counted" statement is inference from its ids tuple.

## Commands run (read-only, cwd /home/vgpnk/Projects/shokunin)

- `MANWIDTH=1000 man -l <page> | col -bx` for gitglossary(7), git-describe(1), git-cat-file(1) and gitrevisions(7), written to scratch: 398, 104 and 260 lines for the first three (footers `Git 2.56.0`); the gitrevisions render was checked by grep only.
- `grep -n` over the renders for object-name, SHA-1, abbrev, annotated, batch-check, ambiguous; `sed -n` for the numbered lines above.
- `git --version` → `git version 2.56.0`.
- `grep` of `corpus/SOURCES.md` S139–S141 raw (registry shape) and of `corpus/evidence/round63/` (frozen C2 instruments, read-only).
- `grep -n 'P02'` on the candidate probe output → line 4; `grep -n` of the gitrevisions render → line 22.
- Scratch `/fast/scratch/hyaku/chousa-r63/ScoutC2Reject/` removed (`rm -rf`; a later `ls` returns no such directory).

VERDICT: SOURCES_OPENED=3 recommended_reject=gitglossary
