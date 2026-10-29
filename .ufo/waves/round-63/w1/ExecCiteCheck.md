# ExecCiteCheck — round 63 w1 — generalised probe-cite-check

Deliverable: `.ufo/waves/round-63/w1/ExecCiteCheck/probe-cite-check.py` (sha256 prefix `9d707407317c85d0`, 119 lines,
executable). Candidate probe bytes unchanged: `sha256sum controls/candidate-git-revision-probe.py | cut -c1-16` = `ccd702f4e9a2f7c4`
(matches claims.md). Nothing under the frozen paths was touched.

## What it does (generalised from round62/probe-cite-check.py)
- `--source S<id>=man:PATH` (rendered `MANWIDTH=1000 man -l PATH | col -bx`, LC_ALL=C.UTF-8, same as c2-count.py's
  `render_man`) or `--source S<id>=file:PATH` (plain text); repeatable; whitespace-normalised both sides.
- Per `probe(ID, label, observed, expected)` call (found via `ast.walk`, so indented/nested defs count): needs a
  `# cite P<n>: S<id> "<quote>"` (S<id> registered, quote >= 4 words, quote a substring of that source) or
  `# cite P<n>: INFERENCE ...`. First passing cite wins; refusals are printed per cite.
- Prints `CITES=<k>/<n> SOURCED=<s> INFERENCE=<i>` and `CITE=PASS|FAIL`.
- Exit 0 = at least one probe call and all cited; 1 = FAIL; 2 = usage/source error (bad spec, missing page,
  unreadable file, unparseable probe, no `--source`).
- Dropped from round 62: the errno-name-in-quote rule (the git probe has no errno expectations).
- Added: unregistered-source refusal, explicit under-4-words message, `orphan cite` lines (cite with no probe call;
  informational, does not change the verdict — INFERENCE: could be made a FAIL, not asked for).

## Receipts (all with TMPDIR=/fast/scratch/hyaku/chousa-r63/ExecCiteCheck, `python3 -B`)
Sources used: `--source S142=man:/usr/share/man/man1/git-rev-parse.1.gz --source S143=man:/usr/share/man/man7/gitrevisions.7.gz`

1. Candidate probe (`controls/candidate-git-revision-probe.py`):
   `CITES=14/14 SOURCED=9 INFERENCE=5` / `CITE=PASS`, exit 0. Earlier `grep -n '# cite P'` listing: 14 cite lines
   (P01-P14); my count of the INFERENCE ones is P02, P05, P06, P10, P13 = 5 (`grep -c '# cite P[0-9]*: INFERENCE'` printed 5);
   sourced = 9. No difference from the expectation.
2. Mutants (copies in scratch; each edited with the edit tool at line 138, the cite of P11):
   - m1, cite line deleted: `P11 uncited`, `CITES=13/14 SOURCED=8 INFERENCE=5`, `CITE=FAIL`, exit 1.
   - m2, quote ends "...given suffix." (page says "prefix"): `P11 quote not in S142: Show every object whose name begins with the given suffix.`,
     `P11 uncited`, `CITES=13/14`, `CITE=FAIL`, exit 1.
   - m3, quote "Show every object" (3 words; the text does occur in the page): `P11 quote under 4 words: Show every object`,
     `CITES=13/14`, `CITE=FAIL`, exit 1.
3. Extra edge checks (not asked; all observed):
   - `--source S142=nope`: message, exit 2. `--source S142=man:/nonexistent.1.gz`: `rendered nothing (exit 16)`, exit 2.
   - Only S142 registered on the candidate probe: five S143 cites each print `cite names unregistered source S143`,
     `CITES=9/14`, exit 1.
   - S142 given as a `file:` of a 3-line wrapped fragment (`Show every object whose / name begins with the given prefix.`):
     P11 passes (no P11 line), proving `file:` loading and whitespace normalisation; other S142 cites fail there as expected.
   - Cross-source quote swap (a quote of S143 filed under S142) is refused by the same substring rule — shown by the
     `file:` run above, where S142 quotes absent from that source were refused.

## Limits
- Checks quote presence in the registered page, not entailment (`expected` value vs quote) — the same limit as round 62
  minus its errno rule. A quote from S142 filed under S143 that happens to occur in both pages would pass (substring-only).
- `man` render depends on the host's man-db/groff (git 2.56.0-1 pages here); a different render could shift a quote.
- Mutants were single-point on P11 only; each of the three rule branches (uncited, absent, short) was hit once.

Scratch /fast/scratch/hyaku/chousa-r63/ExecCiteCheck removed before yield.

VERDICT: CITES=14/14 mutants_rejected=3/3
