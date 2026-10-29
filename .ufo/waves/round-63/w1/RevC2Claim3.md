# RevC2Claim3 — entailment review of Claim 3, `corpus/knowledge/…` candidate (`controls/c2-positive-entry.md`)

Seat: RevC2Claim3 (reviewer, leaf). Item: entailment of Claim 3 against the quotes it cites (Q4, Q3) plus the entry's Limits.
Axes judged: operability, coverage, calibration. No instrument, control, candidate or frozen file was edited. Scratch removed before yield.

## Claim 3 as written (candidate entry, line 23)

> Claim 3. A revision spelled as a commit and a path names a blob, which is the file's bytes at that point rather than a commit, so a citation holding the blob name pins content but says nothing about which commit it was read from. [Q4, Q3]

## Findings

1. **Q3 does not bear on the claim (misattribution).** Q3 (S143 gitrevisions(7), rendered line 115) is the `^{commit}` peel rule: "if <rev> is a commit-ish, <rev>^{commit} describes the corresponding commit object." It says nothing about `<rev>:<path>`, blobs, file bytes or what a blob name pins. The claim cites it as if it supported the blob sentence. Nothing in Claim 3 is carried by Q3.

2. **Q4 supports only the first clause, and not verbatim.** Q4 (S143, rendered line 131): "A suffix : followed by a path names the blob or tree at the given path in the tree-ish object named by the part before the colon." Supported: a `<rev>:<path>` spelling names a blob (for a file path). Dropped: "or tree" (a directory path names a tree, so "names a blob" is narrower than the page). "a revision spelled as a commit" is a substitution: the page's rule is written for a "tree-ish object"; its example `HEAD:README` uses a commit name, so the substitution is tolerable but should be marked.

3. **"which is the file's bytes at that point rather than a commit" overreaches.** No cited quote says "bytes" or "content": `grep -c -i 'bytes\|content'` on both rendered pages returns 0 for each. "at that point" (a commit-relative reading) is not stated. The contrast "rather than a commit" is supported by a sentence the entry does not cite: gitrevisions(7) rendered line 12, "some Git commands (such as git-show(1) and git-push(1)) can also take revision parameters which denote other objects than commits, e.g. blobs ("files") or trees ("directories of files")." That sentence would support the claim if cited; it is absent from Q-list.

4. **"pins content" overreaches.** Neither page says a blob name pins, identifies or fixes content. The only observation in the entry is probe P07 (`unchanged-file-blob-id-same-across-commits observed=True expected=True`), which shows equal blob names for one unchanged file across two commits in one fixture on git 2.56.0. That is an observation of name equality, not of content identity. P07 is not in Claim 3's Q list (only Q4, Q3), so the claim does not carry its own evidence.

5. **"says nothing about which commit it was read from" overreaches.** Silence in the pages is not an assertion that a blob name is commit-independent. The only support is P07 (equal names across two commits, one file, one host), which is an INFERENCE-grade generalisation. The Limits do not mark it: the Limits list `[INFERENCE]` only for P02, P05, P06, and the probe docstring (candidate-git-revision-probe.py lines 14-15) lists INFERENCE only for P02, P05, P06, P13.

6. **Calibration defect in the probe that Claim 3 leans on (not in the entry text, but it decides Finding 4-5).** The probe's `# cite P07` (candidate-git-revision-probe.py line 109) quotes S143 "A suffix : followed by a path names the blob or tree at the given path in the tree-ish object named by the part before the colon." That sentence does not predict blob-name equality across commits, so `expected=True` for P07 is typed, not sourced, and it is not labelled INFERENCE as P02/P05/P06/P13 are. `PROBE_FACTS=14/14` therefore counts P07 as sourced agreement when it is the author's expectation. This is a limit to disclose, not a frozen-byte fix to make here.

7. **Q-number hygiene.** The entry's Q8 and Q9 point at probe output lines; Claim 3 uses neither. Any rewrite that relies on P07 must cite it by a new Q number (proposed Q11 below) with the exact output line.

## Verification run (what was actually executed)

- Rendered pages: `MANWIDTH=1000 man -l /usr/share/man/man1/git-rev-parse.1.gz | col -bx` and the same for `/usr/share/man/man7/gitrevisions.7.gz` (outputs 537 and 258 lines; scratch copies deleted). `git --version` = `git version 2.56.0`, matching the entry's Limits.
- Quotes re-opened verbatim: gitrevisions rendered lines 12, 115, 131; rev-parse rendered line 201-202 (Q1 text, same in both pages).
- Probe run: `TMPDIR=/fast/scratch/hyaku/chousa-r63/RevC2Claim3 python3 -B corpus/evidence/round63/controls/candidate-git-revision-probe.py --work /fast/scratch/hyaku/chousa-r63/RevC2Claim3/p` → exit 0; output lines `HEADER git=git version 2.56.0`, `HEADER python=3.14.8`, P01–P14 all `ok`, `PROBE_FACTS=14/14`. Diff against committed `candidate-git-revision-probe.txt` (excluding the python HEADER line, which matches as well): identical.
- Not run: the counter `c2-count.py` (not in this item's scope).

## Rewritten Claim 3 (for the landing entry; a stranger can check each sentence)

Proposed new quote rows (to be added to the Q-list by the integrating seat; text is verbatim from the rendered pages or the probe output):
- Q4 | S143 | A suffix : followed by a path names the blob or tree at the given path in the tree-ish object named by the part before the colon. | <rev>:<path>  (unchanged, rendered line 131)
- Q10 | S143 | ... can also take revision parameters which denote other objects than commits, e.g. blobs ("files") or trees ("directories of files"). | (rendered line 12; quote shortened with ellipsis, the words kept are verbatim)
- Q11 | S144 | PROBE P07 unchanged-file-blob-id-same-across-commits observed=True expected=True ok | P07 (candidate-git-revision-probe.txt line 9)

> Claim 3. A `<rev>:<path>` spelling names the blob or tree at that path in the tree-ish named before the colon, so for a file path it names a blob [Q4]. The pages describe blobs as objects other than commits, such as files [Q10]. On this host (git 2.56.0, one fixture), a file unchanged between two commits had the same blob name in both [Q11]. So a citation holding only a blob name does not by itself say which commit the file was read from [INFERENCE: no page states this; it follows from Q4 naming no commit and from Q11 on one file in one fixture]. Whether a blob name fixes the file's content is not stated by either page and is not checked by the probe [INFERENCE: the probe compares names, not bytes].

Removed from the candidate: "pins content", "the file's bytes at that point", "rather than a commit" (replaced by Q10's "objects other than commits", which is the page's words), and the Q3 citation.

## Limits to add (so the claim is not read past the evidence)

- The blob-name equality in Q11 is one unchanged file in one fixture on git 2.56.0; the probe's expectation for P07 is the author's typed value, cited to Q4 which does not predict it (see Finding 6).
- Whether a blob name "pins content" is not established by the pages or the probe.

## Verdict on the candidate Claim 3

The claim overreaches. The first clause follows from Q4 (with "or tree" dropped), the blob-versus-commit contrast follows from an uncited sentence of the same page (line 12), and the remaining clauses ("the file's bytes at that point", "pins content", "says nothing about which commit") go beyond every cited quote and the Limits; the one cited quote that is not about paths (Q3) is a misattribution.

VERDICT: CLAIM3=overreach rewrite_needed=yes
