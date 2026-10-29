# CritC2Quotes — critic report (round 63, wave w1, item C2 quotes)

Scope: the nine quotes Q1–Q9 of `corpus/evidence/round63/controls/c2-positive-entry.md`, read in their page context
against the rows in `controls/candidate-git-rows.txt` (`teaches` = column 7) and the entry's five claims. No file under
the frozen tree, `tools/`, `corpus/` or `SKILL.md` was written. Scratch used and removed:
`/fast/scratch/hyaku/chousa-r63/CritC2Quotes/`.

## Method and what was run

1. Rendered both pages as the counter does (`MANWIDTH=1000 man -l FILE | col -bx`, whitespace collapsed):
   `man -l /usr/share/man/man1/git-rev-parse.1.gz` (537 lines) and `.../man7/gitrevisions.7.gz` (258 lines); `git --version`
   printed `git version 2.56.0`, matching the installed page.
2. Ran a substring/anchor check (`python3 -B check.py`, scratch) over the normalised render: each quote in the entry's
   `## Located quotes` section, against S142/S143 renders and S144 = `controls/candidate-git-revision-probe.txt`.
   Output (summary): all nine `FOUND count= 1`; word counts Q1 18, Q2 22, Q3 11, Q4 20, Q5 16, Q6 10, Q7 15, Q8 6, Q9 8
   (all inside the counter's 4–25); each anchor string occurs in the rendered text (`anchor_in_text= True` ×9).
   Anchors name the entry the quote sits under: `<sha1>` (Q1, Q2), `<rev>^{<type>}` (Q3), `<rev>:<path>` (Q4), `--short` (Q5),
   `--disambiguate` (Q6), `--verify` (Q7), `P03` (Q8), `P09` (Q9). All verified against the render headings.
3. Grepped the page renders and the entry for hedges (`typically`, `for example`, `e.g.`, `may`, `can`, `usually`).
   The entry itself carries none of them. The pages carry `For example,` before Q3 and Q7, `E.g.` before Q2, and
   `typically, but not necessarily, names a commit object` (gitrevisions, `<rev>` paragraph; not quoted anywhere).
4. Read the probe's `# cite` comments (`controls/candidate-git-revision-probe.py` lines 85–147) to see what P03, P08,
   P09 and P10 were built to test.

Caveat on Q8/Q9: the entry's S144 path `corpus/evidence/round63/git-revision-probe.txt` does not exist yet; the quotes
were checked against the candidate output, which is the same content by the controls' design (INFERENCE until landed).

## Per-quote reading

Labels: **supports** = the quote in its page context entails what its row teaches and the claim citing it;
**supports-with-unstated-limit** = it supports the core, but the citing claim or the reading needs a scope, condition or
inference that neither the quote nor the entry states; **misleading** = a reading of the quote in context contradicts
the claim. No quote is misleading.

- **Q1** (S143 `<sha1>`, "The full SHA-1 object name (40-byte hexadecimal string), or a leading substring that is unique
  within the repository."). **supports-with-unstated-limit.** The uniqueness clause supports claim 2. The parenthetical
  is SHA-1-only (40 bytes) and the page says nothing about SHA-256 names. Claim 2 does not repeat the 40, but the entry
  never states that the page's full-name wording does not cover sha256 repositories; that is only in Limits line 30 as
  INFERENCE about P02/P05/P06, and P02's own cite comment says "the pages describe SHA-1 names". Citation fit: claim 4 cites
  Q1 for "an abbreviation printed on another machine may be longer or shorter"; Q1 says nothing about length or machines
  (claim 4's support is Q5 alone). Not counted as a misreading; recorded as a citation-fit defect.

- **Q2** (S143 `<sha1>` e.g. sentence: "dae86e both name the same commit object if there is no other object in your
  repository whose object name starts with dae86e."). **supports.** The quote drops the page's `E.g. dae86e1950…
  and`, which is only the example's data; the conditional that carries the rule is in the quote. Claim 2 uses it correctly.

- **Q3** (S143 `<rev>^{<type>}`: "if <rev> is a commit-ish, <rev>^{commit} describes the corresponding commit object.").
  **supports.** The page's sentence opens `For example,`, which the quote drops. The quoted sentence is one instance of the
  general dereference rule in the same paragraph ("dereference the object at <rev> recursively until an object of type
  <type> is found"), and that rule is what claim 1 uses (peel tag → commit). Citation fit: claim 3 cites Q3 for "a
  revision spelled as a commit and a path names a blob"; Q3 is about peeling, not blobs. Q4 carries claim 3; Q3 is extra.

- **Q4** (S143 `<rev>:<path>`: "A suffix : followed by a path names the blob or tree at the given path in the tree-ish
  object named by the part before the colon."). **supports-with-unstated-limit.** The blob-at-path mapping supports
  claim 3's first half. Claim 3's second half, "so a citation holding the blob name pins content but says nothing about
  which commit it was read from", is not in Q4, not in Q3, and not in any quote; the probe that would show it, P07
  (`unchanged-file-blob-id-same-across-commits`), is named in the S144 row but not cited by claim 3 and not quoted. The
  clause is a content-addressing inference and is not marked [INFERENCE]. Also: the page says "blob or tree" and
  "tree-ish" (not only commits); the claim narrows to commits without saying so.

- **Q5** (S142 `--short`: "The minimum length is 4, the default is the effective value of the core.abbrev configuration
  variable"). **supports.** Claim 4's minimum and config-dependent default are both in the quote. The claim's word "the
  tool" is unnamed in the entry; the row's scope (rev-parse `--short`) is the only reading the quote supports. Minor scope
  gap, not counted.

- **Q6** (S142 `--disambiguate`: "Show every object whose name begins with the given prefix."). **supports-with-unstated-limit.**
  This supports "can ask for them all". Claim 5 adds "which turns a failed lookup into a list of candidates instead of a
  silent guess". Nothing in Q6 describes a failed lookup, and nothing in the entry quotes git's plain-lookup behaviour (P10
  would show an ambiguity error, but P10 is not quoted and its cite is INFERENCE). Git does not guess silently on a
  plain lookup in any quoted sentence, so the "silent guess" contrast is an unquoted contrast. The quote also drops the
  next sentence of the same entry, "The <prefix> must be at least 4 hexadecimal digits long", which is the bound on
  claim 5's "a short prefix".

- **Q7** (S142 `--verify`: "git rev-parse "$VAR^{commit}" will make sure $VAR names an existing object that is a
  commit-ish"). **supports.** The page's sentence opens `For example,` (dropped). The parenthetical that defines commit-ish
  to include "an annotated tag that points at a commit" is outside the quote; it supports claim 1 more strongly than the
  quote shows. Nothing contradicts the claim.

- **Q8** (S144 P03 line: "PROBE P03 annotated-tag-id-differs-from-commit-id observed=True expected=True ok"). **supports.**
  One observation on one host, git 2.56.0; the probe's `expected` is typed by its author (cite comment: `S143 "<rev>^{commit}
  describes the corresponding commit object."`, which does not say tag ids differ). The entry's Limits line 29 states the
  version, and Limits line 31 states the typed expectation; that is a stated limit. The `ok` token is a self-agreement
  check, not a measurement, and Limits says so.

- **Q9** (S144 P09 line: "PROBE P09 prefix-resolves-then-ambiguous-after-second-object observed=(True, True) expected=(True,
  True) ok"). **supports-with-unstated-limit.** The prefix is not a cited abbreviation: the probe searches for a 4-hex
  collision among `filler n` blobs (cap 6000) and then adds the second blob. Claim 2 says "a four-digit abbreviation cited
  today can stop resolving after later objects arrive" as a general possibility; the one case shown is a collision built
  by search. The tuple `(True, True)` is unlabelled in the quote (its meaning is "resolves before", "ambiguous after",
  readable only from the probe source). Entry Limits discloses typed expectations, not the constructed collision.

## Coverage of the row `teaches` cells (checked against the quotes)

- S142 `teaches` ("verify a name names an object of the needed type; how short a name may be made; how to list every
  object sharing a prefix") is covered by Q7, Q5, Q6. Complete.
- S143 `teaches` ("which spellings name a commit; which name a **tag object**; which name only a file's bytes; when an
  abbreviation stops being unique") is covered for commit (Q3), file bytes (Q4) and uniqueness (Q1, Q2). **No S143 quote
  says that a tag name names a tag object.** That is carried by S142 Q7 and S144 Q8. The row overstates what S143 itself
  teaches on that point. Not a quote misreading; a row-level gap.
- S144 `teaches` ("tag-versus-commit id, the unchanged-blob id, the prefix that stops resolving") is covered for tag (Q8)
  and prefix (Q9). **The unchanged-blob id (P07) is not quoted anywhere**, although the row names it and claim 3 needs it.

## Findings, ranked

1. Claim 3's commit-blindness clause has no source in the quotes and no citation to P07 (`controls/candidate-git-revision-probe.py`
   cites S143 Q4 for P07, so the probe has the sentence, the entry does not). Fix: cite P07 in claim 3 or mark the clause [INFERENCE].
2. Claim 5's "instead of a silent guess" contrast is unquoted; Q6 drops the ≥4-hex bound. Fix: quote the next sentence and
   either quote git's ambiguity error (P10, with its INFERENCE marking) or drop the contrast.
3. Q1 is the only quote carrying SHA-1-only wording; the entry's claims are generic, but Limits does not say the page is
   silent on sha256. Fix: one Limits sentence: "S143 defines full names as SHA-1 (40 hex); sha256 full length is P02, an observation."
4. Claim 4 cites Q1 for machine-dependence; Q1 does not support it. Claim 3 cites Q3 for blobs; Q3 does not support it. Fix the citation lists.
5. Q9's collision is constructed; the entry should say so next to claim 2's "four-digit" wording.
6. Q3, Q7: the dropped `For example,` markers do not change scope here (each is a single instance of a general rule the same
   paragraph states), but the quotes should carry the general sentence when they are used as the rule.

Not counted as defects: every quote is a contiguous substring of its normalised render; every anchor names the heading its
quote sits under; no quote is misleading.

## Counts

Labels: supports ×5 (Q2, Q3, Q5, Q7, Q8); supports-with-unstated-limit ×4 (Q1, Q4, Q6, Q9); misleading ×0.

VERDICT: QUOTES_WITH_UNSTATED_LIMIT=4 of 9
