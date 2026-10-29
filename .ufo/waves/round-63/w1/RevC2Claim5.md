# RevC2Claim5: entailment review of Claim 5 (candidate c2-positive-entry.md)

Scope: Claim 5 only, against the Q quotes it cites and the Limits. Lane files read, none written. Scratch /fast/scratch/hyaku/chousa-r63/RevC2Claim5 (deleted before yield). Host git 2.56.0, python 3.14.8.

Claim 5 as written: "A reader who wants every object that could be meant by a short prefix can ask for them all, which turns a failed lookup into a list of candidates instead of a silent guess. [Q6, Q2, Q9]"

## Findings (by severity)

1. **overreach: "instead of a silent guess".** No cited page and no probe row says git guesses silently. Observed (my fixture, two blobs sharing 4-hex prefix `6a1c`): `git rev-parse 6a1c` writes `6a1c` to stdout and exits 128, with stderr `error: short object ID 6a1c is ambiguous` / `hint: The candidates are:` / `hint:   6a1cb63 blob` / `hint:   6a1cd0c blob` / `fatal: ambiguous argument '6a1c'`. `git rev-parse --verify --end-of-options 6a1c^{object}` gives the same ambiguity and exit 128. The failure is loud, so the "silent guess" foil is unsupported. Caveat: only git 2.56.0 checked, so [INFERENCE] for other versions.

2. **overreach: "turns a failed lookup into a list".** `--disambiguate` is a separate query. Q6 says "Show every object whose name begins with the given prefix." It is not described as a response to failure. The failed lookup already prints candidates, abbreviated to 7 hex, on stderr (finding 1). What `--disambiguate` adds is full 40-hex names and a query that works without a failure.

3. **overreach: "a short prefix".** Q6's paragraph continues in the rendered page (revparse.txt:119): "The <prefix> must be at least 4 hexadecimal digits long to avoid listing each and every object in the repository by mistake." The entry does not quote this, and the claim does not state the 4-digit bound. Observed on the same fixture: `git rev-parse --disambiguate=6a1` (3 digits) listed both objects, exit 0, so the stated minimum is not enforced here. `git rev-parse --disambiguate=ab` (2 digits) printed nothing and exited 0. That silent empty result is the failure the claim's wording says the option avoids. No probe row tests either case.

4. **citation mismatch: Q9.** Q9 is probe row P09 (`prefix-resolves-then-ambiguous-after-second-object`). It tests resolve-then-ambiguous, not listing. The listing result is P11 (`disambiguate-lists-both-objects`), which Claim 5 does not cite. The only quote supporting listing is Q6.

5. **checkability: the command is never named.** A stranger cannot check "ask for them all" without knowing the mechanism is `git rev-parse --disambiguate=<prefix>`.

6. **calibration: "every object".** P11 lists two blobs. The probe builds its collision with `hash-object` on blobs only. Commits, trees and tags are not tested, so they need [INFERENCE] or a separate probe.

What holds:
- Q1 to Q7 are verbatim in the rendered pages (grep, below).
- Q8 and Q9 match probe rows P03 and P09 in the probe output.
- The core statement, that `--disambiguate=<prefix>` lists every object with that prefix, is supported for the two-blob case by Q6 and P11.

## Evidence (commands and observed output)

- `MANWIDTH=1000 man -l /usr/share/man/man1/git-rev-parse.1.gz | col -bx` gives 537 lines. `MANWIDTH=1000 man -l /usr/share/man/man7/gitrevisions.7.gz | col -bx` gives 258 lines.
- Quote check by grep on the renders:
  - gitrevisions:22 has Q1 and Q2 (`dae86e ... if there is no other object in your repository whose object name starts with dae86e.`).
  - gitrevisions:115 has Q3 (`if <rev> is a commit-ish, <rev>^{commit} describes the corresponding commit object.`).
  - gitrevisions:131 has Q4 (`A suffix : followed by a path names the blob or tree ...`).
  - revparse:62-64 has Q7 (`git rev-parse "$VAR^{commit}" will make sure $VAR names an existing object that is a commit-ish`).
  - revparse:75 has Q5 (`The minimum length is 4, the default is the effective value of the core.abbrev configuration variable`).
  - revparse:119 has Q6 (`Show every object whose name begins with the given prefix.`).
- Probe: `python3 -B /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round63/controls/candidate-git-revision-probe.py --work /fast/scratch/hyaku/chousa-r63/RevC2Claim5/p` exits 0 with `HEADER git=git version 2.56.0`, `HEADER python=3.14.8`, and `PROBE_FACTS=14/14`. All 14 lines match `candidate-git-revision-probe.txt`. P11 is `observed=True expected=True ok`.
- Fixture (`python3 -B amb.py`, repo `git init -q -b main`, `rev-parse --show-toplevel` checked against the fixture dir before writes): two blobs `6a1cd0c8...` and `6a1cb632...` written with `hash-object -w`. Outputs as in findings 1 to 3.
- PROBE_FACTS=14/14 is self-consistency with the probe's typed expectations, as its Limits say. It is not an independent measurement.

## Rewritten Claim 5 (checkable; new quote marked Q6b)

Claim 5. `git rev-parse --disambiguate=<prefix>` prints every object whose full name begins with <prefix>, one full name per line. [Q6, "Show every object whose name begins with the given prefix."; P11, which lists both blobs that share a 4-digit prefix.] [INFERENCE: the same holds for commits, trees and tags, which P11 does not test.] The same paragraph requires the prefix to be at least 4 hexadecimal digits. [Q6b, S142 revparse:119, "The <prefix> must be at least 4 hexadecimal digits long to avoid listing each and every object in the repository by mistake."] Observed on git 2.56.0 but not in the probe: a 3-digit prefix still listed both objects, and a 2-digit prefix printed nothing and exited 0. A plain lookup of an ambiguous prefix does not resolve to a guess: `git rev-parse <prefix>` writes the prefix to stdout and exits 128, with the ambiguity and abbreviated candidates on stderr. [INFERENCE: other git versions behave alike.] Q9 (P09) shows that a prefix which resolves stops resolving once a second object shares it.

## Limits of this review

- One git version (2.56.0) and one host. Every behaviour beyond the two-blob case is [INFERENCE] or marked "observed, not in probe".
- The rewrite adds one new quote (Q6b). The frozen entry does not contain it, so the lane owner must add it if the rewrite is adopted. I have not edited the entry.

VERDICT: CLAIM5=overreach rewrite_needed=yes
