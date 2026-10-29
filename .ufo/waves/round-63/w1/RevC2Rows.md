# RevC2Rows — registry-fit review of candidate rows S142–S144 (round 63, w1)

Scope: `corpus/evidence/round63/controls/candidate-git-rows.txt` against `CORPUS.md` §SOURCES.md (rules, tier and column definitions) and `corpus/SOURCES.md`. No row, registry, tool or claim file was edited; the scratch copy and its outputs are deleted before yield.

## Findings

1. **S143 — needs-edit (teaches overclaims the page).** `teaches` says "which name only a file's bytes". The rendered page says `<rev>:<path>` "names the blob **or tree** at the given path" (gitrevisions.txt, SPECIFYING REVISIONS). The probe's own cite for P07 quotes the same sentence, so the row contradicts its own support.
   - Edit (replace the `teaches` cell):
     `which spellings name a commit (`<rev>^{commit}`), which check that a name identifies a tag object (`<rev>^{tag}`), which name a blob or tree at a path (`<rev>:<path>`), and that an abbreviation names an object only while it is unique within the repository`
   - Why the last clause changes: the page says a `<sha1>` abbreviation is "a leading substring that is unique within the repository" and does not state when uniqueness is lost; the row's "when ... stops being unique" promises a rule the page does not give. The replacement states only the page's condition.
   - "which name a tag object" is grounded only by `<rev>^{tag}` ("can be used to ensure that <rev> identifies an existing tag object"); the replacement says that exactly.
   - `scope` ("what git 2.56.0 states each way of spelling a revision names") is true of the page, which enumerates the spellings in SPECIFYING REVISIONS; no edit.

2. **S142 — fit.** Each `teaches` clause matches the rendered `git-rev-parse(1)` page:
   - "verify ... the type a citation needs": the `--verify` paragraph says `$VAR^{commit}` "will make sure $VAR names an existing object that is a commit-ish" and `^{object}` checks existence (rev-parse.txt lines 61-64).
   - "how short a name may be made": `--short` "The minimum length is 4, the default is the effective value of the core.abbrev" (line 75).
   - "how to list every object sharing a prefix": `--disambiguate=<prefix>` "Show every object whose name begins with the given prefix" (line 119); its 4-digit minimum is also stated, which the row does not contradict.
   - `scope` ("not other git versions", "not the object database format") is the page's own limit; `anchor` names the `--verify` paragraph, `--short` and `--disambiguate` entries, and the page date, all of which resolve.

3. **S144 — fit (own-work, tier B).** Tier B matches the lane precedent S140 (own-work probe, typed expectations, "PROBE_FACTS is self-consistency"). The registry gives tier A to "the lane's own re-runnable gate output"; a probe with author-typed expectations and no gate role is not that, so B is the honest tier.
   - `teaches` (tag-versus-commit id, unchanged-blob id, prefix that stops resolving) matches P03, P07, P09 of the output; P09's cite (S143, "unique within the repository") supports the last one.
   - Re-run reproduces the committed candidate byte-for-byte (see Evidence). The `anchor` ("lines P03, P07 and P09 ... git 2.56.0") is a locator a stranger can use: `grep PROBE` on the output.
   - Integration condition (not a row defect): `source` and `anchor` name `corpus/evidence/round63/git-revision-probe.{py,txt}`, which do not exist yet (only `controls/candidate-*` exists). The row is correct only if the candidate lands under exactly those names; otherwise `source` and `anchor` need the new names.

4. **Shared, for L1 decision (not a per-row edit by this seat).** `CORPUS.md` line 90 requires `source` to carry "canonical URL or DOI (a repo path or command for own-work)". S142 and S143 carry an installed man-page path instead, with no URL. The lane already uses this form (S134, S135, S138, S139). S142 and S143 are therefore fit under lane precedent. A strict reading makes both need a URL; I did not write one because no URL was opened this round (no fetch) and rule 1 forbids citing an unopened source. Decision for L1: accept the installed-page locator as the lane's form, or defer the URL to a round with a fetch.

5. **Near-duplicates: none.** `grep -n 'git\|rev-parse\|revision' corpus/SOURCES.md` shows no existing git-manual row (matches are "revision" in unrelated rows). Fleet grep for `git-scm|gitrevisions|git-rev-parse` in `*/corpus/SOURCES.md` hits only kaidoku S073–S074 (merge-base, cat-file, log) and S140–S142 (git-status, git-diff-tree, git-log), all different pages. Topical overlap with kaidoku S073 (cat-file object type/existence) is real, but the rows cite different pages, so this is not a duplicate.

6. **Pre-landing gap (expected).** S142–S144 are `mined` with used-by `corpus/knowledge/git-revision-identity-r63.md`, which does not exist yet. The census validator resolves used-by against the registry's directory and fails E11 until the knowledge entry lands. Not run without the placeholder; the E11 path follows from `usedby_findings` (sources-census.sh lines 538-567: `[ ! -e "$dir/$path" ]` prints E11).

## Evidence (commands run, output observed)

- Row shape and census (scratch copy of lane registry, candidate rows inserted after S141; knowledge dir symlinked; one placeholder file for the new used-by path; `--file` dir = dirname/..):
  `cd $S/with && bash scripts/sources-census.sh validate --file corpus/SOURCES.md --today 2026-10-28`
  Output: 15 lines, exit 1, identical to the base copy without the rows (`diff` empty). The exit-1 findings are E11/W04 on pre-existing rows (scratch copy lacks `corpus/lessons/`, an artifact of my copy, not a lane finding). Zero E-codes or W-codes name S142, S143 or S144. Columns: NF=13 for all three rows.
  `census`: S142, S143 and S144 counted under tier.A/B and status.mined; FLEET.tier.invalid=0, FLEET.status.invalid=0.
  `overdue` (today 2026-10-28): cadence lines only (`S142 recheck=on-release`, `S143 recheck=on-release`, `S144 recheck=180d`); none overdue.
- Man pages rendered as the rows describe: `MANWIDTH=1000 man -l /usr/share/man/man1/git-rev-parse.1.gz | col -bx`, same for `man7/gitrevisions.7.gz`. `zcat` `.TH` line: `"2026\-09\-27" "Git 2\&.56\&.0"` for both. `git --version`: `git version 2.56.0`. Package: `/var/lib/pacman/local/git-2.56.0-1/desc` shows `2.56.0-1` (read-only file read; no pacman run).
- Quotes checked against rendered text: rev-parse.txt lines 61-64, 74-75, 118-119, 294-299; gitrevisions.txt lines 21-22 ("unique within the repository"), 130-131 ("names the blob or tree at the given path"), SPECIFYING REVISIONS heading (line 14).
- Probe re-run (read-only of the candidate; output to scratch): `TMPDIR=$S python3 -B .../controls/candidate-git-revision-probe.py --work $S/probe-parent/run` → exit 0; `diff controls/candidate-git-revision-probe.txt <rerun>` empty; `PROBE_FACTS=14/14`.
- Cite check in the probe script (lines 96, 109, 113, 133, 138): P03 cites S143 "<rev>^{commit} describes the corresponding commit object" (supports the peel, not the tag-id difference, which is observed); P07 cites the S143 blob-or-tree sentence (this is what makes item 1 a contradiction); P09 cites the S143 unique-within-repository sentence.

## Not done
- No URL verification (no network; fetch scope not used).
- Did not run the knowledge-entry or counter (C2 counter is another seat's item).
- No installs; no tool or version changes.

## Edits summary
| row | verdict | edit |
|---|---|---|
| S142 | fit | none (see item 4 for the shared URL rule) |
| S143 | needs-edit | replace `teaches` cell as in item 1 |
| S144 | fit | none now; at landing, confirm `source`/`anchor` names match the landed files |

VERDICT: ROWS_NEEDING_EDIT=1/3
