# R57W1ReviewFrozen — frozen-input integrity review (chousa round 57, W1)

Seat: R57W1ReviewFrozen (reviewer, leaf). Target: verify the frozen inputs
(claims.md, c2-count.py, c3-count.py, controls/) are untouched since their
freeze commits; classify every commit since the claim base. No counter,
predicate, target, control, or recipe is proposed changed — findings are
reported, not patched. Only write: this report. Scratch
(/fast/scratch/hyaku/chousa-r57/R57W1ReviewFrozen) deleted before yield.

## 1. Spec-literal checks (as assigned)

`git -C /home/vgpnk/Projects/shokunin/chousa-shokunin diff c2f914c53201a8f8ee4fef823b82681051d55592 f9736a39a0344a0aed63a65dfaddf7db624303d9 -- corpus/evidence/round57/claims.md corpus/evidence/round57/c2-count.py corpus/evidence/round57/c3-count.py corpus/evidence/round57/controls` (also re-run to current HEAD e0e73e0f76163b014033e80c6ba53ed92c14113d — identical output):

```
 corpus/evidence/round57/c3-count.py                | 290 ++++++++++++++++++++++
 corpus/evidence/round57/claims.md                  |  59 ++++++
 .../evidence/round57/controls/build-c3-controls.py |  96 ++++++++
 .../evidence/round57/controls/c3-before.txt        |   8 +
 .../evidence/round57/controls/c3-controls.txt      |  16 ++
 5 files changed, 469 insertions(+), 0 deletions(-)
```

Not empty as the seat text anticipated, and cannot be: c3-count.py, the C3
section of claims.md and the c3 controls came into existence only at the
LATER C3 freeze (fd95724d), after the C2 freeze (c2f914c). Every change shown
is that legitimate C3-freeze addition. c2-count.py does not appear in the
change list at all. This is a seat-spec expectation defect, not a lane defect
(see Findings).

Spec's second check used hash `fd95724d56a33a150cd2638fadd2ce1f3425e6c`:
`fatal: bad revision 'fd95724d56a33a150cd2638fadd2ce1f3425e6c'` (exit 128) —
that object does not exist. The repo's actual R57-C3 freeze commit (from
`git log`, author chousa@shokunin.local) is `fd95724d56a33ad150cd263f8add2ce1f3425e6c`.
Re-run with the real hash, to the dispatch tip and to HEAD:

```
$ git diff fd95724d..f9736a39 -- corpus/evidence/round57/c3-count.py   → (empty)
$ git diff fd95724d..HEAD       -- corpus/evidence/round57/c3-count.py → (empty)
```

## 2. Per-freeze integrity (the checks that must be empty — all are)

```
$ git diff c2f914c..HEAD -- corpus/evidence/round57/c2-count.py → (empty)
$ git diff c2f914c..HEAD -- controls/c2-before.txt controls/c2-controls.txt controls/build-c2-controls.py → (empty)
$ git diff fd95724d..HEAD -- c3-count.py controls/{build-c3-controls.py,c3-before.txt,c3-controls.txt} claims.md → (empty)
$ git diff c2f914c..fd95724d -- claims.md → single hunk @@ -66,3 +66,62 @@, 59 additions / 0 deletions (pure C3-section append; C2 section untouched)
blob ids: c2-count.py b1895cd90ed1340a9a31c1f3c92bf6ffc8f3532b (freeze == tip == HEAD)
          c3-count.py bff9de0399015e660f18f3e6a5fe8b0b15db4ed8 (freeze == tip == HEAD)
$ git merge-base --is-ancestor c2f914c HEAD / fd95724d HEAD / 6656f077 c2f914c → all ancestors
```

Working tree: `git status --porcelain -- corpus/evidence/round57/ corpus/captures/` shows only
` M refetch.tsv` (in-flight C3-candidate rows S133-S136) and 4 untracked capture pairs
(6f545e6c/S133, 9695437c/S134, ad3010d2/S135, c71776bc/S133). No frozen path modified.

## 3. Commit classification — `git log --format='%H %s' 6656f077..f9736a39` (+2 newer, to HEAD)

```
f9736a39 round-57: L1 re-fetch pass 1 — 47 attempted, 43 stored (38 R/5 D/4 pending); capture-fetch.py; refetch.tsv   [L1 fetch build]
b022b135 hyaku run9 wrap-up: remaining round-57 captures (14 .raw binaries)                                          [L1 capture ingest]
fd95724d round-57: freeze R57-C3 (counter, before receipt, controls)                                                 [L1 freeze]
c2f914c round-57: freeze R57-C2 (counter, before receipt, controls, egress table, census start)                      [L1 freeze]
```
Newer than the dispatch tip, same classification basis (both author chousa@shokunin.local):
`a03824d` — L1 W1 spec+dispatch + dry-run receipts (.ufo only, 6 files); `e0e73e0` — L1 C2
after-receipt (retries +54 refetch rows, S105 record-less bytes removed, 6 capture pairs).
All commits in range are round-57 L1 work. `git show --stat` confirms none of a03824d/e0e73e0
touches claims.md, either counter, or controls/.

## 4. Frozen counters execute against live state (read-only runs, lane root)

```
$ python3 corpus/evidence/round57/c2-count.py
SET=47 VERDICTS=47/47 REPRODUCED=41 DRIFTED=5 UNREACHABLE=1 BYTE_BACKED=46 CONSISTENT=46/46 FLAGGED=0/0 C2=PASS   (exit 0)
$ python3 corpus/evidence/round57/c3-count.py → ENTRY=no … BOUND=0/7 … C3=FAIL                                      (exit 1)
```
Before receipts on disk match the frozen claims (c2-before: VERDICTS=0/47 … C2=FAIL exit=1;
c3-before: ENTRY=no BOUND=0/7 C3=FAIL exit=1). Verbose check: S111 still REPRODUCED after its
attempt-2 byte refresh; S113/S114 DRIFTED absent=0/6 and 0/9; S105 UNREACHABLE (3 failed
attempts, a1→a2 1439 s apart, all curl_rc=28); no orphan e3ca8f4f.txt (count 0).

## 5. Findings (severity order)

1. (none) **No defect against the frozen claims.** Both frozen counters, all six control
   files, and both claims sections are byte-identical to their freeze commits at the
   dispatch tip and at current HEAD. The two FROZEN claims survive this review intact.
2. (info, seat-spec) The assigned C3 freeze hash `fd95724d56a33a150cd2638fadd2ce1f3425e6c`
   is not a repo object (`fatal: bad revision`); actual is
   `fd95724d56a33ad150cd263f8add2ce1f3425e6c`. Verified with the real hash.
3. (info, seat-spec) The assigned "must be EMPTY" diff c2f914c→tip over {claims.md,
   c2-count.py, c3-count.py, controls} is unsatisfiable as written: c3-count.py, the C3
   claims section and c3 controls legitimately originate at the later C3 freeze. The
   correct per-freeze diffs (§2) are all empty; c2-count.py and the c2 controls never
   appear in any diff.
4. (info, bookkeeping) f9736a39's message says the misroot sweep was "recorded in the
   round lesson", but `git log --all -- corpus/lessons/round-57.md` is empty and the file
   does not exist in the tree or working copy — the record is apparently deferred to the
   wave scribes (R57W1ScribeLesson.md has landed). Commit message overstates the tree.
5. (info, frontier conformance) The L1's after-receipt (e0e73e0) also re-fetched 20
   already-verdicted URLs (attempt-2 rows for S111–S130) beyond the 4 named pending.
   Observed byte deltas are volatile tokens only (S111 jsessionid; S113/S114 hit counters
   1313→1314/1306→1307). Verdicts unchanged (R 38→41 = the three pending resolutions;
   D stays 5; U=1), all within the frozen recipe (≤3 attempts, verdict binds the last
   successful attempt), and CONSISTENT=46/46, FLAGGED=0/0 re-verified at HEAD. S105's
   record-less wrap-up .raw was removed, as UNREACHABLE's "no capture" requires.

## 6. Residual risk / gaps

- Frozen-input checks are git-content checks; they cannot detect a working-tree edit that
  is also staged to match — but `git status` shows no staged or unstaged change on any
  frozen path, and blob equality at HEAD closes the loop.
- C3 is mid-build (ENTRY=no; candidate fetches S133–S136 in flight, uncommitted); its
  freeze-integrity is unaffected, but its verdict is a later-wave matter.

Scratch directory removed before yield: confirmed (`scratch-exists=no`).

VERDICT: Attacked the frozen inputs of R57-C2/R57-C3 (claims.md, c2-count.py, c3-count.py,
controls/) and the commit history since base 6656f077 — SURVIVED: every frozen byte is
identical to its freeze commit at the dispatch tip and at current HEAD e0e73e0f; all six
commits are round-57 L1 work; counters execute (C2=PASS, C3=FAIL as expected at build start);
only findings are two seat-spec transcription defects and two informational bookkeeping notes.
