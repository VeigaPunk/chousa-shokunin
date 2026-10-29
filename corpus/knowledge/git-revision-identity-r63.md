# What a git revision name names, for a citation that pins a revision (round 63)

source: S142 git-rev-parse(1) Git 2.56.0 (installed man page, git 2.56.0-1, rendered `MANWIDTH=1000 man -l FILE | col -bx`); S143 gitrevisions(7) Git 2.56.0 (installed man page, same package); S144 corpus/evidence/round63/git-revision-probe.txt (own-work probe output, git 2.56.0, one host)
verified-at: 2026-10-28 (pages rendered and probe run on git 2.56.0-1; located quotes in `corpus/lessons/round-63.md` `## Gate`)
recheck: on-release (from the lane root: `python3 corpus/evidence/round63/c2-count.py`)

`SKILL.md` asks that a reused finding carry "the artifact and the revision read". When the artifact is a file in a git repository, the revision can be spelled several ways, and the installed pages say which spellings name which objects. This entry records only what those pages and the probe support; each claim below is tied to the quotes it cites, and what neither supports is in `## Limits`.

## Located quotes

- Q1 | S143 | The full SHA-1 object name (40-byte hexadecimal string), or a leading substring that is unique within the repository. | <sha1>
- Q2 | S143 | dae86e both name the same commit object if there is no other object in your repository whose object name starts with dae86e | <sha1>
- Q3 | S143 | if <rev> is a commit-ish, <rev>^{commit} describes the corresponding commit object. | <rev>^{<type>}
- Q4 | S143 | A suffix : followed by a path names the blob or tree at the given path in the tree-ish object | <rev>:<path>
- Q5 | S142 | The minimum length is 4, the default is the effective value of the core.abbrev configuration variable | --short
- Q6 | S142 | Show every object whose name begins with the given prefix. | --disambiguate
- Q7 | S142 | git rev-parse "$VAR^{commit}" will make sure $VAR names an existing object that is a commit-ish | --verify
- Q8 | S144 | PROBE P03 annotated-tag-id-differs-from-commit-id observed=True expected=True ok | P03
- Q9 | S144 | PROBE P09 prefix-resolves-then-ambiguous-after-second-object observed=(True, True) expected=(True, True) ok | P09
- Q10 | S144 | PROBE P07 unchanged-file-blob-id-same-across-commits observed=True expected=True ok | P07

## Claims

Claim 1. On git 2.56.0 an annotated tag is an object with an identifier of its own, because the probe observed a tag identifier different from its commit's identifier, so a citation that records a tag object's identifier names a different object from one recording the commit's identifier; the manual describes peeling with the commit suffix as the way to reach the corresponding commit. [Q3, Q7, Q8]
Claim 2. A leading substring names an object only while the repository holds no other object with that prefix, and the probe saw a four-digit prefix resolve and then stop resolving once a second object shared it, so an abbreviation cited today carries a risk that the full identifier does not; how often such a collision arises is not stated by the pages. [Q1, Q2, Q9]
Claim 3. A revision spelled as a commit, a colon and a path names the blob or tree stored at that path, and in the probe a file unchanged across two commits kept one blob identifier, so a blob identifier alone leaves open which of the two commits it was read from. [Q4, Q10]
Claim 4. The manual states a minimum of four digits for a shortened name and says the default comes from configuration, so an abbreviation printed under one configuration may differ in length from one printed under another. [Q5, Q1]
Claim 5. The manual offers an option that lists every object sharing a prefix, so a lookup that fails on an ambiguous prefix can be turned into a list of candidates rather than guessed. [Q6, Q2, Q9]

## Limits

- This entry rests on the pages installed with git version 2.56.0 and on one probe run with that git on one host; other versions, hosting services and repository formats may differ, and the pages describe SHA-1 names only.
- [INFERENCE] The probe's observations for a sha256 repository (P02, a 64-digit name), a lightweight tag (P05), a branch (P06), the wording of git's ambiguity message (P10) and the default abbreviation length of seven (P13) have no sentence in either page; they are observations of this host, and the pages' own text on them is not what is cited above.
- The probe's expected values are typed by its author, so `PROBE_FACTS=14/14` counts agreement with them and is not an independent measurement; the observed fields are the evidence, and five of the fourteen expectations are marked INFERENCE in the probe's `# cite` comments.
- Not checked: whether a full object name keeps resolving after garbage collection or in another clone; whether a blob identifier fixes the file's bytes beyond what one fixture shows; how often an abbreviation collides in a real repository. The three wave reviews that read the first draft of Claims 1 to 5 found each overreaching (a modal "must", an unsourced general fact, "pins content"); the claims above are the narrowed forms.
