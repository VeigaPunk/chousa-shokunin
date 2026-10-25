# ReviewR3Counts — R3 knowledge-count re-derivation (round 40, w1)

Seat: leaf L2 reviewer. Lane: chousa. Lane tip read: `6bc90e0`
(`round-40 verifier spot-check (integrator, hyaku)`). Fleet repo (`/home/vgpnk/Projects/shokunin`)
read-only. Tool installs/updates: **none** (coreutils/git/python3 already present; no pacman
transaction, no uv/cargo/npm install).

## Assigned attack

Re-derive the r39 report's knowledge-file count at the two cited commits using only
`corpus/knowledge/*.md`; compare the observed 50-to-52 with the report's 29-to-31 and the
appended correction.

Axes: **operability** (does the committed reproduction recipe run as written), **calibration**
(does the claim's object equal the counted population), **depth** (root cause and recurrence).

## Verdict

**The appended correction is numerically right; the r39 report is wrong by a constant level
shift of 21 at both endpoints; and the correction's committed reproduction recipe is fail-open.**
Three independent commit-pinned populations (extracted-tree `ls corpus/knowledge/*.md`,
`git ls-tree --name-only <rev>:corpus/knowledge`, `git ls-tree -r`) all give **50 → 52** at
`8c7c867b66e103712ae33e1d076786f50dd3239e` (r39 base = parent of the first r39 commit `6d914e9`)
and `6ac1007e6a5d699d0742801026554fac1d900b5d` (r39 tip). The +2 delta is exactly the two files
the report names: `A corpus/knowledge/capture-bash-pin-r39.md`,
`A corpus/knowledge/receipt-verifier-subject-r39.md`, with 0 deletions and 0 renames.

- `29` is a **real** historical count, but only on 2026-10-21 round-25 commits (`0fc037e`,
  `c2a6e33`). It is the number in `corpus/README.md:82-85`, the newest in-tree count statement.
- `31` **never existed** as a count at any commit reachable from any ref in this clone
  (`git rev-list --all -- corpus/knowledge`: 129 knowledge-touching commits out of 713): the values
  jump 29 → 32. So the report did not measure; it took README's stale `before` and added the round's
  +2 (`29 + 2 = 31`).
- The 21-file offset is explained exactly: 21 knowledge files were added
  (`git diff --diff-filter=A c2a6e33 8c7c867 -- corpus/knowledge` = 21; D = 0, R = 0), i.e.
  29 + 21 = 50 and 31 + 21 = 52. The report's *delta* and *filenames* are right; only the levels
  are stale. The correction preserves the correct delta.

So the correction's arithmetic, commit pair, and population are confirmed. What is **not**
confirmed is that a reader can execute the correction: the only committed recipe prints
`0` for both revisions and exits `0` (finding F1), and the C2 counter does not detect that
(finding F2).

## Evidence (exact commands and outputs)

### E1 — the report's own command, run at the two commits (extracted commit bytes, no worktree mutation)

```
$ mkdir -p /tmp/r39count/{base,tip}
$ git archive 8c7c867b66e103712ae33e1d076786f50dd3239e corpus/knowledge | tar -x -C /tmp/r39count/base
$ git archive 6ac1007e6a5d699d0742801026554fac1d900b5d corpus/knowledge | tar -x -C /tmp/r39count/tip
$ for d in base tip; do (cd /tmp/r39count/$d && ls corpus/knowledge/*.md | wc -l); done
50
52
```

The command the report cites (`corpus/README` style `ls corpus/knowledge/*.md | wc -l`, report
line 132) therefore **self-refutes** the numbers printed beside it (`29 → 31`) by 21 at both ends.

### E2 — filesystem vs git-object population agreement

```
$ for r in 8c7c867b66e103712ae33e1d076786f50dd3239e 6ac1007e6a5d699d0742801026554fac1d900b5d; do
    printf '%s direct_md=%s all_entries=%s dirs=%s\n' "${r:0:7}" \
      "$(git ls-tree --name-only "$r":corpus/knowledge | grep -c '\.md$')" \
      "$(git ls-tree -r --name-only "$r" -- corpus/knowledge | wc -l)" \
      "$(git ls-tree -d "$r":corpus/knowledge | wc -l)"; done
8c7c867 direct_md=50 all_entries=51 dirs=0
6ac1007 direct_md=52 all_entries=53 dirs=0

$ git ls-tree -r 8c7c867 -- corpus/knowledge | awk '{print $1}' | sort | uniq -c
     51 100644          # regular blobs only; no symlinks/submodules
$ git ls-tree 8c7c867:corpus/knowledge | grep gitkeep
100644 blob e69de29bb2d1d6434b8b29ae775ad8c2e48c5391	.gitkeep
```

`all_entries` is 51/53 because of `.gitkeep`; `direct_md` is the `corpus/knowledge/*.md`
population and equals the recursive count because there are **no subdirectories** at either
commit or at HEAD (`git ls-tree -d HEAD:corpus/knowledge | wc -l` → `0`).

### E3 — what the round added

```
$ git diff --name-status 8c7c867 6ac1007 -- corpus/knowledge
A	corpus/knowledge/capture-bash-pin-r39.md
A	corpus/knowledge/receipt-verifier-subject-r39.md
$ git rev-parse 6d914e9^
8c7c867b66e103712ae33e1d076786f50dd3239e        # base is exactly the pre-r39 tip
```

### E4 — 29 exists only in round 25; 31 never exists

```
$ for c in $(git rev-list HEAD -- corpus/knowledge); do n=$(git ls-tree --name-only "$c":corpus/knowledge | grep -c '\.md$'); [ "$n" = 29 ] && git log -1 --format='%h %ci %s' "$c"; done
c2a6e33 2026-10-21 05:52:11 -0300 round-25: land falsifier corrections and recovery evidence
0fc037e 2026-10-21 04:35:31 -0300 round-25: metadata screen, index freshness, ledger calibration; 68-seat build evidence

$ for c in $(git rev-list --all -- corpus/knowledge); do n=$(git ls-tree --name-only "$c":corpus/knowledge | grep -c '\.md$'); [ "$n" = 31 ] && echo "$c"; done
(no output — 31 never occurs on any ref)
$ git log -1 --format='%h %ci %s' -S'→ 29' -- corpus/README.md
0fc037e 2026-10-21 04:35:31 -0300 round-25: metadata screen, index freshness, ledger calibration; ...
```

Distinct-count histogram over all refs (count of knowledge `.md` per knowledge-touching commit):
`... 24(3) 28(6) 29(8) 32(8) 33(6) ...` — no 30/31 bucket exists; the round-26 transition is
`29 → 32`, so `31` cannot have been measured anywhere.

### E5 — the erratum's recipe, copied literally from `corpus/evidence/round39/claims.md:198`

```
$ for r in 8c7c867b66e103712ae33e1d076786f50dd3239e 6ac1007e6a5d699d0742801026554fac1d900b5d; do printf '%s ' \"$r\"; git ls-tree -r --name-only \"$r\" -- corpus/knowledge | awk '/\\.md$/ {n++} END {print n+0}'; done
"8c7c867b66e103712ae33e1d076786f50dd3239e" fatal: Not a valid object name "8c7c867b66e103712ae33e1d076786f50dd3239e"
0
"6ac1007e6a5d699d0742801026554fac1d900b5d" fatal: Not a valid object name "6ac1007e6a5d699d0742801026554fac1d900b5d"
0
exit=0
```

The committed line contains literal `\"$r\"` and `\\.md$` (single backtick code span, so
Markdown does not unescape them; `grep -rn '\\"\$' corpus/` finds exactly this one occurrence):

- `\"` reaches `git` as part of the revision name → `fatal: Not a valid object name`;
- `\\.md$` reaches `awk` as an escaped-backslash-then-any-char regex → matches no path
  (`printf 'a.md\n' | awk '/\\.md$/ {n++} END {print n+0}'` → `0`;
  with `\.md$` → `1`);
- the pipeline's status is `awk`'s, so git's fatal is masked and the loop **exits 0**.

### E6 — the same recipe with plain quoting and a single backslash

```
$ for r in 8c7c867b66e103712ae33e1d076786f50dd3239e 6ac1007e6a5d699d0742801026554fac1d900b5d; do printf '%s ' "$r"; git ls-tree -r --name-only "$r" -- corpus/knowledge | awk '/\.md$/ {n++} END {print n+0}'; done
8c7c867b66e103712ae33e1d076786f50dd3239e 50
6ac1007e6a5d699d0742801026554fac1d900b5d 52
exit=0
```

The erratum's *intent* is reproducible and matches the observed 50 → 52. Only its committed
text is not.

### E7 — the frozen C2 counter and its R3 condition

```
$ python3 corpus/evidence/round40/c2-count.py
R2_DISPOSITION=ok
R3_DISPOSITION=ok
R4_DISPOSITION=ok
R5_DISPOSITION=ok
R39_CALIBRATION_DISPOSITIONS=4/4
exit=0
```

`corpus/evidence/round40/c2-count.py:66-70` derives `md_count(BASE39)`/`md_count(TIP39)`
(hardcoded `8c7c867…`/`6ac1007…`) and requires `(50, 52)`, the string `29 → 31` in the r39
report, and the strings `29 → 31` + `50 → 52` + `R3` in the claims. Those counts are the true
committed counts (E2), so the numeric half of R3 is genuinely re-derived, not a prose label.

## Findings

### F1 — High (operability): the only committed R3 reproduction recipe is fail-open

`corpus/evidence/round39/claims.md:198` is the sole artifact a reader is told to run to
re-derive 50 → 52. Copied as committed it prints `0` and `0` and exits `0` (E5). The recipe can
never fail: git's `fatal` goes to stderr, `awk` prints `0` and returns success, and the shell
loop's status is the last successful `awk`. A future seat that trusts the exit code records a
verified correction over an empty population; one that trusts the stdout records 0 knowledge
files. Blast radius is zero until copy-pasted, which is exactly what a reproduction recipe is
for. This is the same fail-open class the lane's operability axis is scored on (C1 lowest at
3/10), now present in C2's own evidence.

Recommended replacement (verified: E2/E6, prints `8c7c867… 50` / `6ac1007… 52`, exits 0):

```
set -o pipefail
for r in 8c7c867b66e103712ae33e1d076786f50dd3239e 6ac1007e6a5d699d0742801026554fac1d900b5d; do
  printf '%s %s\n' "$r" "$(git ls-tree --name-only "$r":corpus/knowledge | grep -c '\.md$')"
done
```

Append-only handling: leave the frozen body and the existing erratum bytes untouched; add a
round-41 erratum child line (or an erratum-2 bullet) carrying the corrected command, exactly as
R1–R5 were appended.

### F2 — Medium (calibration): the counter does not bind the prose commit citation

`c2-count.py` hardcodes `BASE39`/`TIP39` but never asserts that those SHAs appear in the claims
text; the R3 conjunction only looks for `"29 → 31"`, `"50 → 52"`, and `"R3"`. Read-only
demonstration over the committed strings:

```
$ python3 - <<'PY'
import pathlib
claims = pathlib.Path("corpus/evidence/round39/claims.md").read_text()
report = pathlib.Path("/home/vgpnk/Projects/shokunin/.ufo/reports/round-39/chousa.md").read_text()
def r3(claims_text, report_text, counts=(50, 52)):          # c2-count.py:67-70, verbatim condition
    return ("29 → 31" in report_text and counts == (50, 52)
            and "R3" in claims_text and "29 → 31" in claims_text
            and "50 → 52" in claims_text)
print("as-committed      :", r3(claims, report))
doctored = claims.replace("8c7c867b66e103712ae33e1d076786f50dd3239e", "0"*40).replace(
                     "6ac1007e6a5d699d0742801026554fac1d900b5d", "1"*40)
print("wrong SHAs in prose:", r3(doctored, report))
nosh = claims.replace("8c7c867b66e103712ae33e1d076786f50dd3239e", "").replace(
                "6ac1007e6a5d699d0742801026554fac1d900b5d", "")
print("SHAs deleted       :", r3(nosh, report))
PY
as-committed      : True
wrong SHAs in prose: True
SHAs deleted       : True
```

Replacing both SHAs with 40 zero/one characters, or deleting them entirely, leaves R3 `True`.
So the property that distinguishes the correction from the report — a *commit-pinned* count —
is unenforced; a later edit that drops the pins passes 4/4 while re-creating the
unreproducible-tally defect criterion 37 forbids. Cheap fix: add
`BASE39 in claims and TIP39 in claims` to the `r3` conjunction, and assert the two counts occur
after the SHA mention in the erratum line.

### F3 — Medium (depth): the stale `29` source is still live, so the defect recurs

`corpus/README.md:82-85` remains the newest count statement in the lane and is byte-identical at
r39 tip (`git show 6ac1007:corpus/README.md`, lines 82-85) and at round-40 HEAD:

```
Round-25 correction (appended 2026-10-21; supersedes the round-24 count
as current at this landing): 43 entries — 29 knowledge notes and 14 lessons
(`ls corpus/knowledge/*.md | wc -l` → 29; ...
```

Round 40's README append (`d164f88`) added the round-40 note and the
`receipt-expectation-digests-r40.md` coverage row but no corrected count statement. Actual counts
are 53 knowledge / 43 lessons at HEAD (knowledge 52 → 53 after `d164f88`; lessons were already 40
at `6ac1007`, so the README's `14` is 29 lessons stale at HEAD). The report's
`29` is exactly this line, so the correction fixes the report but not the source the next report
will read. Two concrete consequences: (a) a future report that copies the newest count
statement reproduces `29` again; (b) the README count command carries no revision, which is the
criterion-37 failure that produced the drift in the first place. Recommended: append a dated
count correction to that block with a commit-pinned command (same shape as F1), or drop bare
count prose from the index header in favour of a pinned command.

Completeness of the lane-side sweep: `grep -rn '29 → 31' --include=*.md .` returns only
correction or audit records — the r39 spot-check (`round-39-verifier-spotcheck.md:65,73`), the
round-40 lesson row (`round-40.md:19`), the erratum (`claims.md:198`), the SCORECARD/LOG round-40
corrections, and this round's own wave reports. No live tally assertion survives lane-side, so
`corpus/README.md:82-85` — which states only the bare `29` — is the single stale source; the fleet
r39 report is the other, frozen by design.

### F4 — Low (calibration): correction population is recursive, the cited defect is not

The r39 report's population is the direct-children glob `corpus/knowledge/*.md`; the erratum's
recipe is `git ls-tree -r` (recursive). They coincide today only because
`git ls-tree -d <rev>:corpus/knowledge` is `0` at both commits and at HEAD (E2). If a
subdirectory (e.g. an archive bucket) is ever added under `corpus/knowledge`, the recipe and the
counter silently count a superset while the claim text still reads `corpus/knowledge/*.md`.
Verified equal-at-present; recommend switching both the erratum and `md_count()` to
`git ls-tree --name-only <rev>:corpus/knowledge` (direct children), which gives the same 50/52
today.

### F5 — Low (informational, calibration): the report's evidence preamble is also false

Report line 132 reads "Evidence: README coverage rows; `ls corpus/knowledge/*.md | wc -l` 29 → 31".
The README coverage-row population at the same commits is `47 → 49`
(`git show <rev>:corpus/README.md | grep -c '^| \`knowledge/'`), not `29 → 31`. Among the four
things asserted on that line — population preamble, before, after, delta — only the delta (+2)
and the two filenames reproduce. That is consistent with F3's diagnosis: nothing on the line was
executed at the cited revisions.

## Confirmed, for calibration honesty

- 50 → 52 at the r39 before/tip commits: **confirmed** by three populations (E1, E2, E6).
- r39 base commit identity and tip identity: `8c7c867` is the direct parent of the first r39
  commit `6d914e9`; `6ac1007` is the r39 knowledge/close commit; both reachable from HEAD (E3).
- +2 delta and the two named entries: **confirmed**; 0 deletions, 0 renames (E3).
- Correction's `29 → 31` characterization of the report: **confirmed**; report line 132 is
  exactly `29 → 31` (citation resolves at `.ufo/reports/round-39/chousa.md:132-133`, fleet commit
  `f713ee1`).
- Round-40 spot-check's independent `50 → 52` and `53`-at-HEAD figures: **agree** with mine.
- C2 counter 4/4 with `R3_DISPOSITION=ok`: **reproduced** (E7).
- Peer mutation evidence (`.ufo/waves/round-40/w1/ExecC2Count.md`, rows M3/M8) fails R3 when the
  literal `29 → 31` in the report or `50 → 52` in the claims is corrupted. The *strings* are
  load-bearing (R-2); this does not contradict F2, which is about the unreferenced *SHAs*.
- Independent agreement: `RevengerR2R5History.md:82` reaches the same 50/52 by `git ls-tree`.

## Residual risk

- **R-1 (cross-repo unpinned read).** `c2-count.py:15` reads
  `ROOT.parent/.ufo/reports/round-39/chousa.md` from the fleet working tree, not a pinned fleet
  revision. Today the file is tracked and byte-identical to its committed blob
  (`sha256(worktree) = sha256(git show HEAD:…) = 01bbed5fcd74c358895c2d0a7b2b5981abb3de875a4abe654b7217fdfebd1ca2`,
  `git status --porcelain` empty — including after this wave's mutation tests, which restore it).
  Any later append to the filed report still flips `R3_DISPOSITION` without a lane change. Pin a
  fleet SHA or copy the exact line into the disposition record.
- **R-2 (string coupling).** R3 matches the literal `29 → 31` / `50 → 52` (U+2192). A `->`
  rewrite or a line re-wrap breaks the counter without changing truth or falsehood.
- **R-3 (recipe independence).** Because F2's check is textual, C2 can be met with F1 unfixed
  indefinitely; "re-derived from committed evidence" currently means "the counter re-derived the
  numbers", not "the documented recipe runs".
- **R-4 (history scope).** "31 never existed" is established over `git rev-list --all` in this
  clone (713 commits, 129 knowledge-touching, jj/keep refs included). Untracked scratch trees and
  other clones are outside the claim.

## Verification gaps

- The r39 report lives in the fleet repo and is read-only for this seat; I could not (and must
  not) modify it, so F1/F3/F4/F2 fixes are recommendations only. No production file was edited.
- I did not run the C2 before-control in a detached worktree (C2 owner scope; the round-40
  spot-check and `control-before.txt` cover it). `c2-count.py` was run once at lane tip,
  read-only, and produced the committed 4/4 state.
- No LSP server applies to this item: the audit target is Markdown prose plus git-object counts,
  and the only code inspected is `c2-count.py`'s predicate, which I read and exercised through
  string-level evaluation rather than LSP references/definitions. The `lsp` device is not exposed
  in this seat's toolset; text/git-object reads here are the canonical evidence for a count, and I
  do not present them as semantic proof of code behavior.
- No live network fetch was made (not needed; no external source is part of R3).

## Out-of-scope observation (not an R3 finding)

At audit time the lane worktree carries changes I did not make and did not touch:
`M tools/research-gate.sh` (+85 lines, self-described "capture-tool pins (round-41 C1)"),
`M .ufo/waves/round-40/w1/swarm-registry.json`, and untracked `.ufo/waves/round-41/` plus
`corpus/evidence/round41/`. They are concurrent work, not part of round 40's R3 evidence. They do
not affect anything above: every count here is commit-pinned (`git ls-tree` / `git archive`), and
the knowledge tree is clean (`git status --porcelain corpus/knowledge` empty; worktree = HEAD = 53
`.md`). Flagged only because an uncommitted gate edit in the same worktree can silently change
what later worktree-run verifiers see, which matters to the round's "no production edits"
milestone.

## Artifact pointers

| Pointer | What it holds |
|---|---|
| `.ufo/waves/round-40/w1/ReviewR3Counts.md` | this report |
| `corpus/evidence/round39/claims.md:198` | the correction under audit (commit pair + broken recipe) |
| `corpus/evidence/round40/c2-count.py:19-20,66-70` | hardcoded revisions and the R3 conjunction |
| `/home/vgpnk/Projects/shokunin/.ufo/reports/round-39/chousa.md:132-133` | the `29 → 31` claim (fleet commit `f713ee1`) |
| `corpus/README.md:82-85` | the live stale `29` source (F3) |
| `corpus/evidence/round40/routed-defect-dispositions.json` (`R3`) | disposition record: `corrected`, 3 evidence pointers |
| `corpus/lessons/round-40.md:19,28` | number-drift mistake row and correction intake row |
| `/tmp/r39count/{base,tip}` | extracted commit trees used for E1 (transient, outside all repos) |
