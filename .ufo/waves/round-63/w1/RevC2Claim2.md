# RevC2Claim2 — entailment review of Claim 2 (c2-positive-entry.md)

Scope: Claim 2 of `corpus/evidence/round63/controls/c2-positive-entry.md` only, against its cited quotes Q1, Q2, Q9 and its Limits. Read-only; no lane file touched. Scratch removed.

## Findings

1. **Overreach (the one that matters).** The claim's last clause says: `a citation that must keep resolving records the full name.` No cited quote supports that a full name *keeps resolving*. Q1 (S143 gitrevisions(7), also rev-parse(1) line 202) only defines the full 40-byte SHA-1 name as one of two allowed object-name forms. Neither page says anything about the object staying present. The probe does not cover it either: P01 checks the length of a full name, and P14 checks only that an all-zero full name fails `--verify`. The entry's Limits do not mention object retention, gc or pruning. A full name stops resolving in the repository where the object is pruned, so the claim, as written, states a guarantee the sources do not give. The sentence also turns a definition into a normative "must".

2. **Supported: "names an object only while no other object … shares that prefix".** Q1 says a leading substring counts as an object name when it is "unique within the repository" (rev-parse.txt:202, gitrevisions.txt:22). P09 (probe line `PROBE P09 prefix-resolves-then-ambiguous-after-second-object observed=(True, True)`) shows the 4-digit prefix resolving before a second object with that prefix was written and failing (`rev-parse --verify` nonzero) after. The word "only" follows from Q1's definition. Q2 is a sufficient condition ("both name the same commit object **if** there is no other object…"), so it supports "while unique" but not "only while"; the "only" comes from Q1, not Q2. Acceptable, but a stranger should be pointed at Q1 for the "only" part.

3. **Supported: "a four-digit abbreviation … can stop resolving after later objects arrive".** The four-digit part is not in Q1 or Q2 (Q2's example is `dae86e`, six digits). It rests on Q9/P09, which uses a 4-hex prefix. P09 builds its collision on purpose (it hashes filler blobs until two share a 4-hex prefix). It shows that the event is possible; the pages and the probe say nothing about how often "later objects" produce it. "Can" is supported; any sense of likelihood is not, and none is claimed. Marking the frequency as [INFERENCE] would make the claim exact.

4. **Minor, not an overreach.** The claim does not say the full name is 40 digits; for a sha256 repository it is 64 (P02, marked INFERENCE in the probe's own comment and not in the entry's Limits). The entry's Limits say "the pages installed with git 2.56.0", which does not cover this, so a stranger could read "the full name" as 40 digits. The rewrite below says "40-hex (SHA-1)".

5. **Verified quotes (no misquote).** Rendered with `MANWIDTH=1000 man -l … | col -bx`:
   - Q1 text ("The full SHA-1 object name (40-byte hexadecimal string), or a leading substring that is unique within the repository.") — verbatim at rev-parse.txt:202 and gitrevisions.txt:22.
   - Q2 text ("dae86e both name the same commit object if there is no other object in your repository whose object name starts with dae86e") — verbatim, same lines.
   - Q9 ↔ probe line `PROBE P09 … observed=(True, True) expected=(True, True) ok` — matches the output of a fresh run (below).

## Commands and output (what I ran)

- `MANWIDTH=1000 man -l /usr/share/man/man1/git-rev-parse.1.gz | col -bx` → 537 lines; `…man7/gitrevisions.7.gz …` → 258 lines. Quotes located with `grep -n -F` (above).
- `grep -n -i "unique\|ambiguous" rev-parse.txt gitrevisions.txt` → only the Q1 lines and the `--short` / `core.abbrev` lines; no sentence on ambiguity errors or on object retention. `grep -n -i "gc\|prune\|garbage\|collision\|forever"` → no hits in either page.
- `python3 -B …/candidate-git-revision-probe.py --work /fast/scratch/hyaku/chousa-r63/RevC2Claim2/p` → exit 0, `HEADER git=git version 2.56.0`, `PROBE_FACTS=14/14`.
- Diff of `PROBE`/`HEADER` lines against the committed `candidate-git-revision-probe.txt` (second run into `p2`) → identical (`IDENTICAL_PROBE_LINES`). The probe removes its own `--work` directory; no leftover.
- `grep -n -i "gc\|prune\|keep\|retain" c2-positive-entry.md` → only line 22 (Claim 2 itself). No retention limit in the entry.

## Rewritten Claim 2 (checkable by a stranger)

> Claim 2. A leading substring is an object name only while it is unique within the repository, so a four-digit abbreviation cited today can stop resolving once another object with the same prefix exists in that repository [Q1, Q9]. The git 2.56.0 pages define a valid abbreviation as "a leading substring that is unique within the repository" (Q1); on this host a 4-hex prefix that resolved before a second object with that prefix was written did not resolve after it (Q9, P09 `observed=(True, True)`). How often a later object produces such a collision is [INFERENCE]: P09 builds its collision by hashing filler blobs and the pages give no rate. A citation that must name one object later can record the 40-hex SHA-1 name [Q1]; that name is the same length as every other full name, so no other object shares its prefix [INFERENCE], but whether the object is still present in the repository is not covered by Q1, Q2, the probe or the Limits [INFERENCE: object retention depends on gc/pruning, not checked here].

Checks a stranger can run: `MANWIDTH=1000 man -l /usr/share/man/man7/gitrevisions.7.gz | col -bx | grep -F "a leading substring that is unique"` (Q1); `python3 -B …/controls/candidate-git-revision-probe.py --work <empty dir> | grep P09` (Q9; the line must read `observed=(True, True) expected=(True, True) ok`).

Changes from the original, in one line each: "names an object only while" → "is an object name only while" (unchanged meaning, the source is Q1); "four-digit … can stop resolving after later objects arrive" kept, with the rate marked [INFERENCE]; "must keep resolving records the full name" replaced, because the guarantee it states is not in the quotes.

Limits to add to the entry (not frozen here; L1 integrates): one line on object retention (full names resolve only while the object is present; not checked), and one on sha256 full names (64 hex; P02, INFERENCE).

## Residual risk / verification gaps

- The probe's expectations are typed by its author (the entry says so); P09's `expected` is the author's, the `observed` is the run.
- The probe does not check object retention, gc, or cross-clone resolution. Nothing here tests them.
- I did not run the frozen `c2-count.py`; the entailment question is outside its scope (counter is structural plus echo screen, per the frozen claims).

VERDICT: CLAIM2=overreach rewrite_needed=yes
