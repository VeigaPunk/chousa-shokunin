# RevC2Claim1 — entailment review of Claim 1, `controls/c2-positive-entry.md`

Scope: Claim 1 only (annotated tag, object name, peeling). Frozen inputs read, not edited: `corpus/evidence/round63/claims.md`, `controls/c2-positive-entry.md`, `controls/candidate-git-revision-probe.py` and `.txt`. No writes outside this report and my scratch, which is deleted.

## Claim 1 as written

> Claim 1. An annotated tag has an object name of its own, so a citation that records the tag's name instead of the commit's names a different object, and a reader must peel the tag to the commit before comparing. [Q3, Q7, Q8]

Cited quotes: Q3 (S143), Q7 (S142), Q8 (S144 probe row P03).

## Re-opened evidence (what I ran and saw)

1. `MANWIDTH=1000 man -l /usr/share/man/man1/git-rev-parse.1.gz | col -bx` (git 2.56.0 page, 537 lines rendered) and the same for `gitrevisions.7.gz` (258 lines). Verbatim checks with `grep -c -F`, each returned 1:
   - Q3 `if <rev> is a commit-ish, <rev>^{commit} describes the corresponding commit object.` — gitrevisions(7), `<rev>^{<type>}` entry. Matches.
   - Q7 `git rev-parse "$VAR^{commit}" will make sure $VAR names an existing object that is a commit-ish` — rev-parse(1), `--verify` text. Matches, but the entry cuts the sentence before its parenthetical `(i.e. a commit, or an annotated tag that points at a commit)`, which is the only sentence on that page that mentions tags.
2. `python3 -B .../controls/candidate-git-revision-probe.py --work <scratch>/p` — exit 0. Output (minus `Wall time`) is byte-identical to the committed `candidate-git-revision-probe.txt` (`diff` printed nothing beyond the wall-time line). Relevant row: `PROBE P03 annotated-tag-id-differs-from-commit-id observed=True expected=True ok`; the probe script also runs `P04 peeled-annotated-tag-equals-commit-id observed=True expected=True ok`.
3. Probe source, lines 94–99: `tag_id = rev-parse v1`; `peeled = rev-parse v1^{commit}`; P03 is `tag_id != c1`; P04 is `peeled == c1`.
4. Limits of the entry: git 2.56.0 pages and probe only; probe expectations are the author's.

## Findings

**F1 — Overreach: the word "must".** The claim says "a reader **must** peel the tag to the commit before comparing." Nothing quoted says that. Q3 defines what `<rev>^{commit}` denotes; it is a tool, not a requirement. The same page offers `<rev>^{object}` ("make sure <rev> names an object that exists, without requiring <rev> to be a tag, and without dereferencing <rev>") and `<rev>^{tag}`, so a reader can compare tag object names with tag object names and never peel. The probe shows that peeling yields the commit id (P04), not that peeling is needed to compare. Verdict on this clause: the page supports "peeling gives the commit"; "must ... before comparing" goes beyond it. [INFERENCE on what a careful reader does; not stated anywhere quoted.]

**F2 — Overreach / unsourced fact: "An annotated tag has an object name of its own."** Stated as a plain general fact. Its only support in the entry is Q8, the own-work probe row P03 (one tag, one repository, git 2.56.0, one host). The Q3 and Q7 quotes do not say a tag has its own object name. The probe's `expected=True` is cited (`# cite P03`) to Q3, but Q3 does not say that the tag id differs from the commit id; the observed column is the only evidence. The page does have a sentence that would support it and the entry does not cite: gitrevisions(7) line 117, "because a tag is already an object, it does not have to be dereferenced even once to get to an object." It is not in the entry's Located quotes, so it cannot be used without adding it. Verdict on this clause: supported by an observation, not by the cited pages; it needs the version qualifier the Limits already give, or an [INFERENCE] tag.

**F3 — Ambiguity: "the tag's name".** In git, "name" of a tag can mean the refname (`v1`, which names no object by itself) or the tag object's object name (the id `git rev-parse v1` prints). The probe compares the second. A stranger checking the sentence cannot tell which is meant. Fix: say "the tag object's object name (the id `git rev-parse v1` prints)".

**F4 — Calibration, minor.** The claim is not in the entry's own Limits' scope cross-reference: it says nothing about the git version, though the Limits say the probe ran on 2.56.0 only. A rewrite should carry that.

**What holds.** The core observation — on this host, `rev-parse v1` (annotated tag) differs from `rev-parse v1^{commit}`, and the latter equals the commit id — is reproduced by my run of the committed probe and matches the committed output. The quotes Q3 and Q7 are verbatim in the rendered pages. The entry's Limits disclose the one-version, one-host scope. So the factual core is right; the overreach is in the modal "must", the untagged general statement, and the vague "name".

## Rewritten Claim 1 (checkable by a stranger)

New quotes, verbatim in the rendered pages and to be added to the entry's Located quotes if adopted:
- Q10 | S143 | As a special rule, <rev>^0 means the commit itself and is used when <rev> is the object name of a tag object that refers to a commit object. (gitrevisions(7), `<rev>^{<type>}` section; `grep -c -F` = 1)
- Q11 | S144 | PROBE P04 peeled-annotated-tag-equals-commit-id observed=True expected=True ok (probe output row; the observed column is the evidence)

> Claim 1. On git 2.56.0 on this host, an annotated tag is a tag object with its own object name: `git rev-parse v1` prints an id different from the id of the commit the tag points at [Q8, P03 observed=True; this is an observation, the pages cited do not state it]. A citation that records the tag object's id therefore names a different object from one that records the commit's id. To get the commit's id from the tag, peel with `<rev>^{commit}`, which "describes the corresponding commit object" [Q3], or with `<rev>^0`, which "is used when <rev> is the object name of a tag object that refers to a commit object" [Q10]; the probe observes that the peeled id equals the commit id [Q11, P04 observed=True]. Which of the two ids a citation should record is not settled by the pages quoted. [INFERENCE] A citation meant to pin the commit's content should record the peeled id.

Check of the rewrite: every word is either in Q3, Q10, the Q8/Q11 probe observations (with "observed" qualifier), the "On git 2.56.0 on this host" scope (Limits), or marked [INFERENCE]. "must" is removed. "tag's name" is replaced by "tag object's id".

## Probe note (outside Claim 1, recorded for the L1)

The probe's `expected` column for P03 is cited to Q3, which does not state the result. The probe's own Limits already say expectations are author-typed; the observed column is the evidence. No change to the frozen probe is proposed here.

## Commands and outputs

- `MANWIDTH=1000 man -l /usr/share/man/man1/git-rev-parse.1.gz | col -bx` — 537 lines.
- `MANWIDTH=1000 man -l /usr/share/man/man7/gitrevisions.7.gz | col -bx` — 258 lines.
- `grep -c -F` on Q3, Q7, Q10, Q11-page sentences, and the Q7 parenthetical: each `1`.
- `python3 -B controls/candidate-git-revision-probe.py --work <scratch>/p` — `EXIT=0`; `HEADER git=git version 2.56.0`; `PROBE_FACTS=14/14`; P03 and P04 `observed=True expected=True ok`.
- `diff` of my run vs committed `candidate-git-revision-probe.txt` (wall-time line removed) — identical.

Not run: the frozen counter `c2-count.py` (not my item); no network use.

Scratch `/fast/scratch/hyaku/chousa-r63/RevC2Claim1` removed after the probe run.

VERDICT: CLAIM1=overreach rewrite_needed=yes
