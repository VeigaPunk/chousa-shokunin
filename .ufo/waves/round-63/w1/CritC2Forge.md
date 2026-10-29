# CritC2Forge — attack on R63-C2 (critic, item CritC2Forge)

Scope: the frozen counter `corpus/evidence/round63/c2-count.py` (sha prefix 606207e224c0b7cf), read-only. Every forge was built in a
scratch mirror prepared the way `controls/run-c2-controls.py` prepares one (lane corpus minus captures/evidence/fixtures, candidate
rows inserted, candidate entry, candidate probe + committed output), then the frozen counter was run unmodified on it:
`python3 -B c2-count.py --root <mirror> --fleet <lane parent> --work <mirror>/../cw`. No lane, fleet or git writes.

## Findings

Eight forges reach `C2=PASS` in a mirror. Two of them are named in `claims.md` as limits. The other six are not
named there, and I found no counter rule that rejects two of them (F1b and F7); the rest have a rule that I tested offline.

| # | Forge (what the entry does) | Reaches PASS | Named in claims.md | One counter rule that rejects it | Rule tested? |
|---|---|---|---|---|---|
| F1 | Claim 5 is the quote restated plus hedges (`Generally, typically, usually, mostly, notably, ... clearly, probably, certainly, quite, rather, nearly`). Empty content, ECHO counts the hedges as fresh 5-letter words. | yes | no (echo screen is not named; only generic "entailment not machine-checked") | Count fresh words after removing a closed hedge list; reject if fewer than 3 or under 30 % remain | yes: R1 rejects F1, positive passes |
| F1b | Claim 5 is false: "a reader ... always gets exactly one object back ... the ambiguity error never appears" (contradicted by P09/P11 and by Q6 itself). | yes | yes ("non-sequitur" control, "entailment is not machine-checked") | none lexical: needs a closed quantifier screen (always/never/exactly/only) with no matching quote word; that screen is INFERENCE, not run | no; R1 does not reject it (correct: it is the named limit) |
| F2 | Probe check P11 rewritten to `len(dis) == 1`, expected changed `True`→`False`, committed output regenerated: `PROBE P11 ... observed=False expected=False ok`; PROBE=1/1, PROBE_FACTS=14/14. | yes | yes in part ("PROBE_FACTS=14/14 counts agreement with [typed expectations], not an independent measurement") | pin the probe script's sha256 to the frozen candidate digest `ccd702f4e9a2f7c4` (the counter compares only the live run with its own committed output, so both can be rewritten together) | yes: R4 rejects F2 (`466d7bca...`), positive passes |
| F3 | `git-revision-probe.py` is `sys.stdout.write(<committed .txt>)`: never runs git. PROBE passes (exit 0, PROBE_FACTS=14/14, lines equal, HEADER equals live git). | yes | no | the probe must call git: run it with a logging `git` first on PATH and require at least 14 invocations | yes: R5 finds `git_calls=0` for F3 (and the sha pin R4 also rejects it); candidate probe is not rejected |
| F4 | A `git` shim earlier on PATH: `--version` prints `git version 2.56.0`, else `exec /usr/bin/git`. LIMITS, PROBE and HEADER bind to the shim, C2=PASS. | yes (see caveat) | no | `git` must resolve to `/usr/bin/git` (the package file the S142 page names), not the first PATH entry | yes: R3 rejects F4 (`git resolves to .../forges/F4-git-shim-pinned/bin/git`), positive passes |
| F5 | Limits section is three bullets: `- [INFERENCE] git version 2.56.0`, `- git version 2.56.0`, `- git version 2.56.0`. LIMITS=1/1. | yes | no | each Limits bullet carries at least 6 words beyond the git version string and no two bullets are equal | yes: R2 rejects F5 (all three bullets); positive Limits (three real bullets) passes |
| F6 | Q6 (S142) replaced by a sentence from the `--all`/`--glob` option text that also occurs in git-log(1), git-rev-list(1), git-replay(1) and git-shortlog(1); Claim 5 rewritten to rest on it; anchor `OPTIONS`. Counter binds it to S142 by substring. | yes | no | a located quote must not occur in any installed git page other than the row's bound pages | yes (R6-fixed): rejects F6 (`Q6 also in ['git-log.1.gz', 'git-replay.1.gz', 'git-rev-list.1.gz']`), positive Q1–Q9 clean. Cost: rejects true shared boilerplate (4 such sentences in S142 alone) |
| F7 | Q5 anchor changed from `--short` to `git`; the anchor check is a substring test against the anchor cell and the page. | yes | no | none tested. A 300-character anchor-locality window does NOT reject it ("git" sits within 300 characters of Q5), and it wrongly rejects the positive's Q7 (anchor `--verify` is farther away): not adoptable as written | no usable rule |

Forges that do not reach PASS (controls behave as expected): F4b (shim reporting `git version 9.99.0`) → `C2=FAIL`, with
`LIMITS do not name the live \`git version 9.99.0\`` and `PROBE ... bound_to_live_git=False`. So the version binding
follows whichever `git` PATH resolves to, which is the F4 weakness.

Count: 8 forges reach PASS (F1, F1b, F2, F3, F4, F5, F6, F7). Named in claims.md: 2 (F1b, F2).

## Evidence (commands and observed output)

1. Frozen digests (`sha256sum | cut -c1-16`): c2-count.py `606207e224c0b7cf`, run-c2-controls.py `8b2b371340b01b58`,
   candidate probe `ccd702f4e9a2f7c4`, c2-positive-entry.md `93ad2c681783b6ce`, candidate-git-rows.txt `cfdf7b117c26a07f`. All five
   match the prefixes in claims.md. claims.md itself: `6c46b2cc193e1a44187777e6db98aec52278e37cc4f4b027efbe4365d24c70f5`, matches.
2. Positive control on my mirror (`forge.py pos`): `ENTRY=1/1 TRIO=1/1 ROWS=3/3 QUOTES=9/9 COVERAGE=1/1 CLAIMS=1/1 ECHO=1/1
   LIMITS=1/1 PROBE=1/1 MAP=1/1 CENSUS=1/1 C2=PASS`, rc 0.
3. Frozen controls runner reproduced from scratch (`run-c2-controls.py --work <scratch>/ctl`): every line is `OK`,
   `C2_CONTROLS_UNEXPECTED=0`, and the output equals the committed `controls/c2-controls.txt` except that the receipt has an
   extra trailing `exit=0` line (diff output: `26a27 > exit=0`). Also `non-sequitur rc=0 ... C2=PASS` (named limit) reproduced.
4. Forge run (`forge-run1.txt`): F1 hedge `rc=0 C2=PASS`; F1b `rc=0 C2=PASS`; F2 `rc=0 C2=PASS` with
   `PROBE P11 disambiguate-lists-both-objects observed=False expected=False ok`; F3 `rc=0 C2=PASS`; F4 `rc=0 C2=PASS`;
   F4b `rc=1 C2=FAIL`; F5 `rc=0 C2=PASS`; F7 `rc=0 C2=PASS`; F6 `rc=0 C2=PASS` (`forge.py` quote variant and `quote_forge.py`).
5. Shared sentences (`research.txt`): S143 shares 0 of 92 sentences with 221 other installed git pages; S142 shares 4 of 195:
   "The option core.warnAmbiguousRefs ..." (git-for-each-ref), "--exclude=<glob-pattern> ..." (log, replay, rev-list, shortlog),
   "If a trailing /* is intended ..." and "This option affects the next pseudo-ref option --all or --glob ..." (same four).
6. Offline rule simulations (`quote-rules.txt`, `rules-r6.txt`): R1 flags F1 only; R2 flags F5 only; R3 flags F4 only; R4 flags
   F2 and F3; R5 flags F3 only (`git_calls=0`); R6-fixed flags F6 only; R7 (300-character window) flags positive Q7 and F6's
   own Q6 but NOT F7. The positive mirror is rejected by none of R1–R6-fixed.
7. Why F4 is only partly shown: on this host the real `git` is also 2.56.0 (`which -a git` → `/usr/bin/git`; `git --version`
   → `git version 2.56.0`), so the shim's lie is not visible in facts. A host with a different real git would show whether
   the facts differ: INFERENCE, not run (no second git on this host).

## Limits of this check

- Each forge's "reaches PASS" is one run on this host; F4 is shown only as a PATH-binding weakness (see 7).
- The R1–R7 rules are offline simulations on the forged artifacts. None is wired into the frozen counter; none was run in the
  frozen counter's own process; they do not change any frozen file. Rule proposals are candidates for the next round's battery,
  per the frozen rule that post-wave findings are limits and supplements, not rewrites.
- R6-fixed rejects true shared boilerplate; it trades a false-positive risk for provenance. R7 false-rejects the positive; it is
  not a candidate as written.
- F1b's rejecting rule (a quantifier screen) is INFERENCE and not run.
- No fresh judgment of entailment was made; F1 and F1b are judged by the counter's own rules and by reading the claim against
  its quote (the closure's job).

## Routed to the lane (for L1; no edits made by this seat)

- Next battery (not this round's frozen instruments): add defect legs for F1 (hedge filler), F2 (probe sha pin), F3 (probe must
  invoke git), F4 (git must resolve absolutely), F5 (limits substance), F6 (no quote in another installed page). Each has an
  offline rule in hand except F7 and F1b.
- Claim wording: the claims file names "entailment is not machine-checked" and "PROBE_FACTS counts agreement with typed
  expectations". Both are accurate; neither names the PATH binding, the git shim, the cat probe or the empty Limits.

VERDICT: C2_FORGES_REACHING_PASS=8 named_in_claims=2
