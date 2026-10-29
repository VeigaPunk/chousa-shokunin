# ScribeEntryIndep — item scribe: independent C2 entry (what pins a citation to a git revision)

Entry: `.ufo/waves/round-63/w1/ScribeEntryIndep/entry.md` (5 claims, 15 located quotes: S142 x7, S143 x5, S144 x3).
Written before opening `controls/c2-positive-entry.md`; the candidate was opened only after the entry was final.

## Findings

1. **Entry passes the frozen counter on a mirror built with my entry.** Mirror built by importing the builder
   functions of `controls/run-c2-controls.py` (`rows_into`, `ENTRY`) and substituting my entry for the candidate;
   candidate rows, candidate probe and its output kept, as the builder does. Counter line:
   `ENTRY=1/1 TRIO=1/1 ROWS=3/3 QUOTES=15/15 COVERAGE=1/1 CLAIMS=1/1 ECHO=1/1 LIMITS=1/1 PROBE=1/1 MAP=1/1 CENSUS=1/1 C2=PASS` (exit 0).
2. **First counter run failed for a harness reason, not an entry defect.** With `--work <dir>` where `<dir>` did not
   exist, the counter's PROBE step ran the probe on `<dir>/probe`; the probe requires its `--work` parent to exist
   (`git-revision-probe.py --work must be absent or empty, with its parent present`). The counter printed only
   `PROBE exit=2 facts=None same_as_committed=False bound_to_live_git=True`; the probe's stderr is discarded, so the
   cause is not visible from the verdict. Fixed by `mkdir -p` and a rerun. Routed as a limit: a missing `--work`
   parent reads as a C2 defect. The run-c2-controls builder omits `--work`, so the frozen controls are unaffected (INFERENCE).
3. **Echo screen failed on my first draft of claims 2-4** (fresh words 5/18, 5/17, 1/10). I reworded them to carry
   their own terms. The echo screen is satisfied by vocabulary, not by entailment; I judged entailment by reading
   each claim against its quotes (below).
4. **Anchors.** The counter binds each quote's anchor to the registry row's anchor cell. To choose anchors I read
   the anchor, column and used-by cells of `controls/candidate-git-rows.txt` (not the candidate entry). Disclosed as
   the one shared input. Quotes came from the rendered pages and the probe output only.

## Independent entry (summary; full text in entry.md)

- C1 `--verify`: one name becomes a raw 20-byte SHA-1 object name; the output is checked to name an object; `^{type}` requires a given type. [Q1-Q3]
- C2 `--short` / `--disambiguate`: minimum length 4, default from `core.abbrev`; `--disambiguate` lists every object with the prefix, prefix at least four hex digits. [Q4-Q7]
- C3 names: full 40-byte hex or a unique leading substring; `master` typically means `refs/heads/master`; `heads/master` picks one when both branch and tag exist. [Q8-Q10]
- C4 `<rev>^{<type>}` dereferences until the type is found or nothing more can be dereferenced; `<rev>:<path>` picks the blob or tree at a path. [Q11-Q12]
- C5 (probe, this host, git 2.56.0): annotated tag id differs from commit id (P03); unchanged file keeps its blob id across commits (P07); a short prefix becomes ambiguous once a second object shares it (P09). [Q13-Q15]

## Diff against the candidate (`controls/c2-positive-entry.md`, Claims 1-5)

Claims made only by the candidate (no full counterpart in mine):
- K1 (cand C1): a citation of a tag's name names a different object from the commit's; a reader must peel the tag before comparing. Mine has the P03 fact (C5), not the citation consequence.
- K2 (cand C2): a short prefix can stop resolving as objects arrive; a citation that must keep resolving records the full name. Mine has P09 (C5), not the advice.
- K3 (cand C3): a blob name pins content but says nothing about the commit it was read from. Mine has the `<rev>:<path>` definition (C4) only.
- K4 (cand C4): an abbreviation printed on another machine may be longer or shorter. Mine has "default from `core.abbrev`" (C2), not the cross-machine consequence.
- K5 (cand C5): a failed prefix lookup can list candidates instead of a silent guess. Mine has the `--disambiguate` listing (C2), not the failed-lookup consequence.
- Candidate Limits only: K6 lightweight tag, branch and sha256 behave as P02, P05, P06 (marked [INFERENCE]); K7 probe expectations are author-typed, so `PROBE_FACTS` counts agreement with them.

Claims made only by mine (no full counterpart in candidate):
- M1 (C1): `--verify` takes exactly one name and returns a raw 20-byte SHA-1 object name; the candidate cites Q7 for `--verify` only for the peel point.
- M2 (C2): `--disambiguate` prefix must be at least four hex digits so the list does not cover the repository.
- M3 (C3): the full-name / unique-substring definition, the `master` to `refs/heads/master` rule and the `heads/` disambiguation; the candidate quotes Q1 but states no refname claim.
- M4 (C4): the recursive `<rev>^{<type>}` rule; the candidate quotes `^{commit}` only inside its peel advice.
- M5 (C5): P07 (unchanged file keeps its blob id); the candidate does not cite P07.

Shared facts: `--short` minimum 4 and `core.abbrev` default (cand C4 / mine C2); P03 (cand C1 / mine C5); P09 (cand C2, C5 / mine C5); `<rev>:<path>` (cand C3 / mine C4); `<sha1>` full-name rule (cand C2 / mine C3).

Count basis: whole claims. None of the candidate's five claims is made in full by my entry, so `claims_only_in_candidate=5`; by the same basis five of mine have no full counterpart (M1-M5).

## Calibration notes (reading, not machine-checked)

- Candidate C3 ("says nothing about which commit"), C4 ("another machine"), C5 ("turns a failed lookup into a list of candidates") and the "must peel" advice in C1 are not carried by their cited quotes and are not marked [INFERENCE]. The counter passes them because the echo screen only counts vocabulary.
- My C5 relies on probe test names plus `observed=` values; it states probe results, not page statements.
- My Limits mark the one inference ([INFERENCE]: entailment judged by reading) and name the git version (`git version 2.56.0`).

## Evidence pointers (commands run)

- `MANWIDTH=1000 man -l /usr/share/man/man1/git-rev-parse.1.gz | col -bx` (537 lines; quotes from lines 61-66 `--verify`, 74-75 `--short`, 118-119 `--disambiguate`, 201-202 `<sha1>`)
- `MANWIDTH=1000 man -l /usr/share/man/man7/gitrevisions.7.gz | col -bx` (258 lines; quotes from lines 21-22 `<sha1>`, 27-28 `<refname>`, 114-115 `<rev>^{<type>}`, 130-131 `<rev>:<path>`)
- `git --version` -> `git version 2.56.0`
- Probe output `controls/candidate-git-revision-probe.txt`: lines 1-2 `HEADER git=git version 2.56.0`, P03/P07/P09 lines, `PROBE_FACTS=14/14`
- `python3 -B corpus/evidence/round63/c2-count.py --root <mirror-indep> --fleet /home/vgpnk/Projects/shokunin --work <dir>` -> `C2=PASS`, exit 0 (line above)
- Earlier run, same command with `--work` parent missing -> `C2=FAIL`, `PROBE exit=2` (finding 2)
- Direct probe run `python3 -B <mirror>/corpus/evidence/round63/git-revision-probe.py --work <fresh>` -> `PROBE_FACTS=14/14`, exit 0

Not run: the full C2 controls (`run-c2-controls.py`), the candidate's own counter run, any probe other than the counter's PROBE step.

## Tools and cleanup

- No tools installed or upgraded. Read-only git not used. No fleet, sibling-lane or registry writes; the mirror was built in scratch only.
- Scratch `/fast/scratch/hyaku/chousa-r63/ScribeEntryIndep/` removed.
- Writes: `.ufo/waves/round-63/w1/ScribeEntryIndep/entry.md` and this report.

VERDICT: INDEPENDENT_ENTRY_C2=PASS claims_only_in_candidate=5
