# R57W2SentFinal — final scope sweep at HEAD (sentinel, leaf)
lane `chousa-shokunin` · HEAD `3010e7537d163d9a76264a166d491214ecdaf45e` · claimed tip `1c9626ef…` · snapshot
`2026-10-27T06:26:22-03:00` · scratch `/fast/scratch/hyaku/chousa-r57/R57W2SentFinal` (removed) · only lane write: this file.
No counter, claim, control or recipe touched; nothing patched — every finding is reported.
Axes: A tip integrity · B tree cleanliness · C artifact tree · D fleet root · E scratch · F frozen inputs · G round-45 · H claims
## A. Claimed tip vs actual HEAD — SURVIVES
```
$ git cat-file -t 1c9626efba2455d513b6b18df9b3df291e66556f   → commit
$ git merge-base --is-ancestor 1c9626ef… HEAD                → YES-ANCESTOR
$ git log --oneline 1c9626e..HEAD   → 3010e75 round-57: W2 residual falsify call (8 reviewer/critic/mutation seats …)
$ git diff-tree --no-commit-id --name-only -r 3010e75 | grep -vc '^\.ufo/'   → NON-UFO-COUNT: 0
```
The one commit above the claimed tip adds 6 files, all under `.ufo/waves/round-57/` (420 insertions, 0 deletions), so the
claim state at HEAD equals the claim state at the claimed tip; the brief's tip sentence holds.
## B. `git status --porcelain` — DEVIATION (F2, low)
```
$ git status --porcelain
?? .ufo/waves/round-57/w2.ready.dispatched
?? .ufo/waves/round-57/w2/chousa-report-draft.md
$ git status --porcelain -- corpus/ tools/ | wc -l   → 0
```
Neither path is a seat report; zero corpus/tools dirt. `w2.ready.dispatched` (365 B, 06:23:41) is the driver's seat→seat
release marker — its w1 twin `w1.ready.dispatched` is **TRACKED**, this one is `UNTRACKED`, and `git check-ignore -v`
→ `NOT-IGNORED`. `w2/chousa-report-draft.md` (9577 B, 06:23) is the L1 draft. No seat report existed under `w2/` at
snapshot, so no seat owns this dirt. Blast radius: any downstream "`status --porcelain` empty at receipt" check fails on
two files no seat may delete. **Remediation:** commit both with the wave, or ignore the marker and move the draft out.
This is `R57W1SimpRound.md` §6b's class (`w1.ready.partial` vs `w1.ready.dispatched` — two names, mismatched tracking,
one map) recurring in w2.
## C. Artifact tree — SURVIVES (brief's "four root files" is wrong: 13)
```
$ find .ufo/waves/round-57 -type f | wc -l   → 81     [w1 66 (65 *.md + swarm-registry.json) · w2 2 · root 13]
$ find … -maxdepth 1 -type f -printf '%f\n' | sort
gen-w1-spec.py gen-w2-spec.py w1-dispatch.json w1.ready w1.ready.dispatched w1-results.json w1-run.err
w1-spec.json w2-dispatch.json w2.ready w2.ready.dispatched w2-run.err w2-spec.json
```
Every path outside `w1/`/`w2/` is wave-driver infrastructure (specs, dispatches, results, run logs, ready markers). No
corpus, tool, lesson or knowledge byte sits in the wave tree; no stray experiment file.
## D. Fleet root — NO CHOUSA WRITE; the brief's predicate cannot pass (F3)
```
$ find /home/vgpnk/Projects/shokunin -maxdepth 1 -newer …/round57/claims.md
/home/vgpnk/Projects/shokunin   /home/vgpnk/Projects/shokunin/.scratch
/home/vgpnk/Projects/shokunin/.git   /home/vgpnk/Projects/shokunin/MANIFEST.json
```
"must show only lane-internal paths" is unsatisfiable: `-maxdepth 1` on the fleet root can only print fleet-root paths.
On substance all four hits are non-chousa — `MANIFEST.json` tracked and clean (`git diff --stat HEAD -- MANIFEST.json`
empty), last touched by `945f2f3d rounds ledger: kake r60 closure … hyaku, non-author`, `1 file changed, 43 insertions(+)`,
with **zero chousa round-57 refs** (its round-57 entries are kotodama/kotoba/kumitate/kake), so no premature fleet-root
filing; `.scratch` tracked (18 files), clean, newest members the orchestrator goal docs (04:51/04:54); `.` and `.git` are
mtimes. Fleet-root untracked inventory belongs to other lanes (`.ufo/reports/round-50/mado.md` 06:24:55,
`.ufo/reports/round-61/kake.md` 06:14:55) — the fleet `status` shows only those two. **Remediation:** replace the check
with `git -C chousa-shokunin status --porcelain` plus an attributable-commit test on each fleet-root hit.
## E. Scratch audit — THREE LEFTOVERS
```
$ ls /fast/scratch/hyaku/chousa-r57/   → R57W1ReviewAxes/  dryrun/  fetch/
```
- `R57W1ReviewAxes/` — empty leftover (dir kept, contents cleaned) from a w1 seat; names neither live work nor a defect.
- `dryrun/` — not a seat dir: `lane-copy/` (a full `git clone --shared` incl. `.git`) + `lane-archive/`, 05:12.
- `fetch/` — not a seat dir: `pinned-pairs.tsv`, empty `recipe/`, `refetch.append` (06:15). The append is a **pure
  subset** of the committed record (`append_rows 144`, `committed_rows 145`, `append_not_in_committed 0`) — nothing stranded.
My own dir was removed; no seat dir was found holding stray writes.
## F. Frozen inputs — SURVIVE
```
$ git diff --stat c2f914c… HEAD -- …/c2-count.py                        → (empty)
$ git diff --stat fd95724d… HEAD -- …/c3-count.py                       → (empty)
$ git log --oneline fd95724d… HEAD -- …/claims.md                       → (empty)
$ git ls-tree --name-only fd95724d… …/controls/                         → all 6 controls present IN the freeze commit
$ git diff --stat fd95724d… HEAD -- …/controls/                         → (empty)
$ git log --oneline --diff-filter=M -- 'corpus/evidence/round57/c3/**'  → (empty: no post-add manifest rewrite)
```
Counters byte-identical to their freezes; `claims.md` frozen since C3; all six controls committed *at* the freeze and
never edited after; C3 manifests added once (`f31a91b`, `a8d4e7d`) and never rewritten. Since the C2 freeze the corpus
shows 150 additions + 16 modifications + 1 deletion, all inside this round's disclosed work and none on a frozen path.
## G. Round-45 incident (§6a) — CLOSED
```
$ git hash-object corpus/evidence/round45/spans.tsv   → a21a0365bce096f3678d4becdba8028b37a2a374
$ git rev-parse 6656f07…:…/round45/spans.tsv          → a21a0365…      (identical)
$ git rev-parse HEAD:…/round45/spans.tsv              → a21a0365…      (identical)
$ grep S083 corpus/evidence/round45/spans.tsv → pin a3ff65e0db9cc4f2178932ce53965e4cba60c6aab0ba3b1d4ce40020a8a7cf8f ×2
$ git diff --name-only HEAD -- corpus/evidence/round45/   → (empty)    [status: empty]
```
Worktree == HEAD == round base byte for byte, and S083's pin is the **original** `a3ff65e0…`, not §6a's substituted drift
digest `d37b64ed…`. Nothing remains to commit; the hazard is fully restored.
## H. Both claims re-derived at HEAD — SURVIVE
```
$ TMPDIR=$PWD PYTHONDONTWRITEBYTECODE=1 python3 …/c2-count.py   (exit 0)
SET=47 VERDICTS=47/47 REPRODUCED=41 DRIFTED=5 UNREACHABLE=1 BYTE_BACKED=46 CONSISTENT=46/46 FLAGGED=0/0 C2=PASS
$ TMPDIR=$PWD PYTHONDONTWRITEBYTECODE=1 python3 …/c3-count.py   (exit 0)
ENTRY=yes S127_CITED=yes NEW_GROUND=yes CLAUSE=yes
BOUND=4/7 (min 4) R1:S131 R2:S132 R3:S133 R7:S118   SWEPT=3/3 R4 R5 R6
QUOTE_ROWS=10 IN_SPAN=10 IN_ENTRY=10 IN_LESSON=10 SHORT=10 CONTEXT=10 CAPTURE_BOUND=10
SUBSTANCE=PASS ANCHOR_BOUND=3/3 INFERENCE_GROUNDED=yes STRAY_IDS=-     C3=PASS
```
Both lines are verbatim the after-receipts recorded at `SCORECARD.md:2863` — no predicate, target or threshold moved
since the freezes. Counter side effects audited: `c3-count.py:132` `shutil.rmtree` acts only on
`pathlib.Path(tempfile.mkdtemp(prefix="r57c3-"))`; c2 has no `rmtree`; neither writes into the lane.
## I. Provenance defect introduced by W1 integration — F1 (low, committed record)
`SCORECARD.md:2863` prints C3's freeze as the brief's transcription slip:
```
$ git cat-file -e fd95724d56a33a150cd2638fadd2ce1f3425e6c   → fatal: Not a valid object name   (exit 128)
$ git cat-file -e fd95724                                    → (exit 0)  = fd95724d56a33ad150cd263f8add2ce1f3425e6c
$ git log -S 'fd95724d56a33a150cd2638fadd2ce1f3425e6c' -- SCORECARD.md              → 1c9626e (W1 integration)
$ git log -S 'fd95724d56a33a150cd2638fadd2ce1f3425e6c' -- LOG.md corpus/lessons/round-57.md → (empty)
```
`LOG.md` and the committed lesson use 7-hex `fd95724`, which resolves — they are correct. Exactly one committed lane
record is unresolvable as written, and the L1 introduced it at `1c9626e` by copying the brief; three w1 reports
(`R57W1CritC3Stray.md:3`, `R57W1LabHeading.md:4`, `R57W1LabRecipe.md:4`) reproduce the wrong id as given. Frozen bytes are
unaffected — `claims.md` never held the hash (`git log -S … -- claims.md` empty). **Remediation:** fix that one 40-hex
string to `fd95724d56a33ad150cd263f8add2ce1f3425e6c` (or `fd95724`) when the wave is committed.
## J. Disclosed, not falsifying — record-less S105 bytes
`b022b13 "hyaku run9 wrap-up: remaining round-57 captures"` lands captures after the C3 freeze with no fetch record.
`corpus/captures/e3ca8f4fdd15420b80096a75.raw` was **absent at c2f914c** (`git ls-tree c2f914c corpus/captures/ | grep -c
e3ca8f4f` → 0), landed in `b022b13`, deleted in `e0e73e0` — so C2's `UNREACHABLE=1` partly rests on "no capture" reached
by deletion. Disclosed in the `e0e73e0` subject and `corpus/lessons/round-57.md:34`. Not forge-friendly: keeping those
bytes yields REPRODUCED/`BYTE_BACKED=47`, above the 46 measured, so the deletion lowered the lane's own number.
VERDICT: attacked the wave's final state — claimed-tip drift, tree dirt, fleet-root writes, scratch leftovers, frozen
counter/claims/control/round-45 bytes and both counters — and the claim state SURVIVES at HEAD (`C2=PASS`, `C3=PASS`,
frozen inputs byte-identical, `round45/spans.tsv` restored to `a21a0365`); falsified only the wave's self-hygiene: two
untracked non-seat files at the tip (F2), a committed `SCORECARD` freeze id no object resolves (F1), three scratch
leftovers, and a fleet-root check written so it can never pass (F3).
