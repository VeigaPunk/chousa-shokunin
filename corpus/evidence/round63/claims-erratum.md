# Erratum — round 63 frozen claims (proposed, for L1 to file under corpus/evidence/round63/)

Target: `corpus/evidence/round63/claims.md`, sha256 prefix `6c46b2cc193e1a44`, freeze commit `62876ef90154714bfa806fbbec7890a9ff11b179`.
The claims file is not edited; each entry below is a recorded correction, per the freeze rule.
Found by seat CritCalibration (wave w1). Every observed value is from the command shown in the seat report.

## E1 — line 81, "committed before the freeze" (C1 Controls)

- Statement: `Controls (all committed before the freeze; ...)`.
- Observed: `git -C <lane> log --oneline --diff-filter=A -- corpus/evidence/round63/controls corpus/evidence/round63/claims.md corpus/evidence/round63/c1-battery.py corpus/evidence/round63/c2-count.py` prints one commit, `62876ef round-63: freeze claims, battery, counter, controls and receipts`. The controls were first added in the freeze commit itself, not in an earlier one.
- Correction: "Controls (committed in the freeze commit `62876ef`, the same commit as this file; not in an earlier commit; ...)".

## E2 — line 144, "wrong header file" (C2 controls list)

- Statement: lists `wrong header file` among the 19 single-defect variants.
- Observed: the variant named `s143-wrong-file` in `corpus/evidence/round63/controls/run-c2-controls.py` (line 113) replaces the S143 row's man-page path `/usr/share/man/man7/gitrevisions.7.gz` with `/usr/share/man/man1/git-log.1.gz`. It is a wrong source file, not a header. The variant count (19) is unaffected; `c2-controls.txt` prints the line `s143-wrong-file rc=1 ... C2=FAIL OK`.
- Correction: replace `wrong header file` with `S143 row cites a wrong man-page file (s143-wrong-file)`.

## E3 — line 14, quoted heading `Planned — round 63 (amended before the freeze)`

- Statement: the SCORECARD row is "amended by `Planned — round 63 (amended before the freeze)`".
- Observed: `grep -cF 'Planned — round 63 (amended before the freeze)' SCORECARD.md` prints `0`. The heading in `SCORECARD.md` line 2991 is `## Planned — round 63 (amended before the freeze, 2026-10-28)`. The meaning matches; the quoted string does not occur.
- Correction: quote the heading as it stands: `Planned — round 63 (amended before the freeze, 2026-10-28)`.

## E4 — line 115, "the lane holds nothing on what a git revision name ... names" (overbroad)

- Statement: the lane holds nothing on what a git revision name names.
- Scoped evidence (true): `git -C <lane> grep -c rev-parse a847a37cc263c80417ee1cdf650de33e2f91a839 -- corpus/knowledge` prints nothing (exit 1). The claim's own command, `grep -rl 'rev-parse' corpus/knowledge`, prints nothing at the base and in the worktree.
- Contradicting evidence for the unscoped sentence: `git -C <lane> grep -c rev-parse a847a37cc263c80417ee1cdf650de33e2f91a839 -- corpus tools` lists 12 files with a nonzero count, including `corpus/lessons/round-31-verifier-spotcheck.md` (`git rev-parse --verify <h>^{commit}`), `corpus/evidence/round57/sidecar-audits.md` (`git rev-parse master:corpus/evidence/round45/spans.tsv`), `corpus/evidence/round51/receipt-check.py` (`rev:path` blob resolution) and `tools/capture-fetch.py`. These are uses, not knowledge about what a revision name names, but the sentence as written is universal over the lane.
- Correction: "the knowledge layer (`corpus/knowledge/`) holds nothing on what a git revision name ... names; the lane's lessons and scripts use `git rev-parse` but do not state what its spellings name".

## Not errata

- Digest prefixes (9 of 9) match `sha256sum FILE | cut -c1-16`.
- The C1 and C2 `Before` lines and exit codes match `controls/c1-before.txt` and `controls/c2-before.txt` exactly.
- Control counts (22 C1 legs/tools, 16 mutants with 15 FAIL and M11 SURVIVED, 25 C2 receipt lines with 21 FAIL) match the receipts.
