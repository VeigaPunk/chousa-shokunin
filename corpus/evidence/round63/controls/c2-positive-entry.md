# What pins a citation to a git revision (round 63, positive control for the C2 counter)

source: S142 git-rev-parse(1) Git 2.56.0 (rendered man page, git 2.56.0-1); S143 gitrevisions(7) Git 2.56.0 (rendered man page); S144 corpus/evidence/round63/git-revision-probe.txt (own-work probe, git 2.56.0)
verified-at: 2026-10-28 (git 2.56.0-1 pages rendered `MANWIDTH=1000 man -l FILE | col -bx`; probe run on the same day)
recheck: on-release (from the lane root: `python3 corpus/evidence/round63/c2-count.py`)

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

## Claims

Claim 1. An annotated tag has an object name of its own, so a citation that records the tag's name instead of the commit's names a different object, and a reader must peel the tag to the commit before comparing. [Q3, Q7, Q8]
Claim 2. A leading substring names an object only while no other object in the repository shares that prefix, so a four-digit abbreviation cited today can stop resolving after later objects arrive; a citation that must keep resolving records the full name. [Q1, Q2, Q9]
Claim 3. A revision spelled as a commit and a path names a blob, which is the file's bytes at that point rather than a commit, so a citation holding the blob name pins content but says nothing about which commit it was read from. [Q4, Q3]
Claim 4. The shortest abbreviation the tool will print is four digits and its default comes from configuration, so an abbreviation printed on another machine may be longer or shorter than the one a citation shows. [Q5, Q1]
Claim 5. A reader who wants every object that could be meant by a short prefix can ask for them all, which turns a failed lookup into a list of candidates instead of a silent guess. [Q6, Q2, Q9]

## Limits

- This entry rests on the pages installed with git 2.56.0 and the probe run with git version 2.56.0; other versions may differ, and a hosting service's own revision display is not covered.
- [INFERENCE] A lightweight tag, a branch and a sha256 repository behave as the probe shows (P02, P05, P06), but no sentence of either page states those three results; they are observations of this host.
- The probe's expected values are typed by its author, so `PROBE_FACTS=14/14` counts agreement with them, not an independent measurement.
