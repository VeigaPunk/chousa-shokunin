# ExecReceiptSpot — round 47 wave 1

Item: operator proposal `considerthese/2026-10-24.md:64-66` ("Spot re-verify one receipt a week").
Run the newest `verify-receipts.py` read-only over a `/tmp` `git archive master` copy, name every
receipt that no longer verifies, and draft QUALITY criterion 68 with a Check line and a "Shown able to fail".
Lane tip measured: `master` = HEAD = `a15610a59aaeaf43b79ccc650acee4bd4da00341`. No lane file was written
except this report. No fetch, no installs.

## Verdict

At tip, **4 of the 6 receipts that round 40 lists as active no longer verify** (`gate-sha256-mismatch`):
`corpus/evidence/round40/receipts/c1-after-s39011-regenerated.json`,
`corpus/evidence/round39/receipts/c1-after-s39111.json`, `.../c2-after-s39101.json`, `.../c2-after-s39121.json`.
All four verify at the commit that added them. The drift comes from `1bd9001` (round 41), which changed
`tools/research-gate.sh` from `4253c187…` to `2cb04bdd…`. Round 41 recorded this (`lessons/round-41.md:55-71`)
and routed a successor-counter design to round 42. A search of `corpus/lessons/round-4[2-6]*.md` and
`corpus/evidence/round4[2-7]` finds no closure, so the routed fix is **still open after 5 rounds**.
Round 40's own committed counter currently prints `R39_ACTIVE_RECEIPTS=2/6`, exit 1, at tip.

## Newest verifier

`ls -t $(find corpus/evidence -name 'verify-receipts*.py')` lists `round39/verify-receipts.py` first, then
`round38/`. There are only two. Last commits: r39 `6d914e9` (2026-10-24 03:15), r38 `870074e`. The r39 file
sha256 is `1b6e0de688deda7493db3af5397d1e5bbf1fcdf556d8e254acae3ac6a8496267`.
Usage (docstring lines 24-32): `--receipt F --gate G --counter C [--expectations E]`. It exits 0 with
`VERIFY: ok …`, or exits 1 with `VERIFY-FAIL: <first failed binding>`. It binds its own sha256
(`verifier_sha256`, line 196), so only round-39 and round-40 receipts can pass. Earlier rounds fail closed by design.

## Run 1 — every committed receipt, tip archive

Setup: `git archive master | tar -x -C /tmp/chousa-r47-ExecReceiptSpot/lane` printed
"archive of a15610a5…". The loop then ran
`python3 corpus/evidence/round39/verify-receipts.py --receipt R --gate G --counter C [--expectations E]` from the
archive root for each of the 31 committed `corpus/evidence/round*/receipts/**/*.json`, with each receipt's own
`counter`, `expectations` and `gate` (the live-lane prefix stripped). Output:
```
round37/* (10)                                   rc=1 VERIFY-FAIL: missing-field counter_sha256
round38/* (9)                                    rc=1 VERIFY-FAIL: predicate-mismatch
round39/receipts/c1-after-s39011.json            rc=1 VERIFY-FAIL: expect-sha256-mismatch
round39/receipts/c1-after-s39111.json            rc=1 VERIFY-FAIL: gate-sha256-mismatch
round39/receipts/c1-base-s39001.json             rc=1 VERIFY-FAIL: expect-sha256-mismatch
round39/receipts/c1-mutenv-s39003.json           rc=1 VERIFY-FAIL: counter-sha256-mismatch
round39/receipts/c1-mutenv-s39013.json           rc=1 VERIFY-FAIL: expect-sha256-mismatch
round39/receipts/c2-after-s39101.json            rc=1 VERIFY-FAIL: gate-sha256-mismatch
round39/receipts/c2-after-s39121.json            rc=1 VERIFY-FAIL: gate-sha256-mismatch
round40/receipts/c1-after-s39011-regenerated.json rc=1 VERIFY-FAIL: gate-sha256-mismatch
round40/receipts/c1-base-s39001-regenerated.json  rc=0 VERIFY: ok … gate=base-gate-r39.sh counter=c1-count.py
round40/receipts/c1-mutenv-s39013-regenerated.json rc=0 VERIFY: ok … gate=mut-gate-path-env.sh counter=c1-count.py
round41/receipts/cells-before.json, cells/cells.json rc=1 VERIFY-FAIL: missing-field counter_sha256
VERIFIED=2/31
```
How to read the refusals: the 21 receipts from rounds 37, 38 and 41 fail closed by design (docstring 30-32).
The three r39 c1 `expect-sha256-mismatch` receipts are the documented stale originals (claims.md:196, R1). `s39003` is
the documented superseded draft (claims.md:197, R2). The 4 `gate-sha256-mismatch` rows are the active set, and that is the finding.

## Run 2 — round 40's own counter (reads the active manifest), tip archive

`cd /tmp/…/lane && python3 corpus/evidence/round40/c1-count.py`
```
…c1-base-s39001-regenerated.json: ok   …c1-after-s39011-regenerated.json: fail VERIFY-FAIL: gate-sha256-mismatch
…c1-mutenv-s39013-regenerated.json: ok …c1-after-s39111.json / c2-after-s39101.json / c2-after-s39121.json: fail gate-sha256-mismatch
R39_ACTIVE_RECEIPTS=2/6
r40-c1 exit=1
```
On the pre-round-41 tree (`git archive b173b094` = `1bd9001^`), the gate sha is `4253c18738f84df9`. Same counter:
`R39_ACTIVE_RECEIPTS=6/6`, exit 0. The tip gate is `2cb04bddfd5601d7`. `git diff --stat b173b094 1bd9001 -- tools/research-gate.sh`
shows 94 lines changed (+92 −2).

## Run 3 — each r39/r40 receipt at the commit that added it

Receipts carry no revision field, so the adding commit (`git log -1 --diff-filter=A -- R`) is the
revision anchor. For each receipt: `git archive <c>`, then the same verifier invocation.
```
c1-after-s39011 @6d914e9 rc=1 expect-sha256-mismatch   c1-after-s39111 @6d914e9 rc=0 VERIFY: ok
c1-base-s39001  @6d914e9 rc=1 expect-sha256-mismatch   c1-mutenv-s39003 @6d914e9 rc=1 counter-sha256-mismatch
c1-mutenv-s39013 @6d914e9 rc=1 expect-sha256-mismatch  c2-after-s39101 @6d914e9 rc=0 VERIFY: ok
c2-after-s39121 @6d914e9 rc=0 VERIFY: ok
c1-after/base/mutenv-…-regenerated @d164f88 rc=0 VERIFY: ok (3/3)
VERIFIED_AT_ADDING_COMMIT=6/10
```
All 6 active receipts verify at their adding commit. The 4 that fail there are exactly R1 and R2, already on record.
So no receipt has silently broken; the open item is tip drift with no landed successor.

## Hermeticity gap (new; not in r39–r46 records I searched)

Both c2 receipts bind `subject_counter` as an absolute live-lane path
(`/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round39/c1-count.py`). A `/tmp` archive run
still reads that file from the live tree. Command:
`strace -f -e trace=openat -o …/strace.txt python3 corpus/evidence/round39/verify-receipts.py --receipt corpus/evidence/round39/receipts/c2-after-s39121.json --gate tools/research-gate.sh --counter corpus/evidence/round39/c2-count.py --expectations corpus/evidence/round39/expectations.jsonl`
The trace shows `openat(AT_FDCWD, "/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round39/c1-count.py", O_RDONLY|O_CLOEXEC) = 3`.
The subject check (lines 199-206) runs before the gate check, so it passed on live bytes.
The pinned leg for c2 receipts therefore depends on the live worktree: an uncommitted edit to that file would
flip it. Possible fixes are a lane decision: a relative subject path in successor receipts, or a chroot/bind-mount run. Neither is applied here.

## Falsifier — corrupt one receipt byte (in /tmp only)

On the tip archive, receipt `corpus/evidence/round40/receipts/c1-base-s39001-regenerated.json` (sha256 `e33199c1…`).
At 0-based offset 675, `"matched": 7` became `6` (`cmp -l`: `676 67 66`, new sha256 `9878c337…`).
Verifier result: `VERIFY-FAIL: receipt-self-digest`, rc=1. After restoring the byte: `VERIFY: ok`, rc=0.
The tip counter already exits 1, so I repeated the test on the pinned `b173b094` archive, where it discriminates:
`pinned clean exit=0` → corrupt: `…s39001-regenerated.json: fail VERIFY-FAIL: receipt-self-digest`,
`R39_ACTIVE_RECEIPTS=5/6`, `pinned corrupt exit=1` → restored: `R39_ACTIVE_RECEIPTS=6/6`, `pinned restored exit=0`.

## Draft — QUALITY.md criterion 68 (proposed; QUALITY.md not edited)

```
68. **A committed receipt is re-verified every round, at its measured revision and at the tip.**
    Each round, the newest committed `verify-receipts.py` is run read-only, in a `git archive`
    copy, over every receipt its active manifest names (today
    `corpus/evidence/round40/active-r39-receipts.tsv`: 6 receipts, rounds 39 and 40). Pinned leg:
    in an archive of the commit that added each receipt (`git log -1 --diff-filter=A -- <receipt>`),
    every active receipt prints `VERIFY: ok`; a refusal there means the receipt never verified as
    committed (the round-39 R1 class) and no claim may cite it. Tip leg: in an archive of `master`,
    every refusal is listed in the round lesson with its refusal name and the commit that last
    changed the bytes it binds (`git log -1 -- <path>`); a refusal with no such commit after the
    receipt's adding commit is a defect, not drift. Check: `git archive <rev> | tar -x -C <tmp> &&
    (cd <tmp> && python3 corpus/evidence/round40/c1-count.py)` — at `b173b094` (last tree before
    the round-41 gate edit) `R39_ACTIVE_RECEIPTS=6/6`, exit 0; at `a15610a5` `R39_ACTIVE_RECEIPTS=2/6`,
    exit 1, all four refusals `gate-sha256-mismatch` after `1bd9001` moved `tools/research-gate.sh`
    from `4253c187…` to `2cb04bdd…` (`lessons/round-41.md`, post-landing addendum). Shown able to
    fail: in the `b173b094` copy, change byte 676 of `c1-base-s39001-regenerated.json`
    (`"matched": 7` to `6`); the verifier refuses `receipt-self-digest` and the counter prints
    `R39_ACTIVE_RECEIPTS=5/6`, exit 1; restoring the byte returns 6/6, exit 0. Named limits: the
    pinned leg anchors on the adding commit because receipts carry no revision field; the c2
    receipts bind `subject_counter` as an absolute live-lane path, so an archive copy still reads
    that file from the live tree; a pass proves integrity against committed bytes, not authorship.
    Operator proposal mined from `considerthese/2026-10-24.md` (2026-10-24), "Spot re-verify one
    receipt a week"; the file was not edited. — `lessons/round-47.md`.
```
Drafting notes: numbered 68 as assigned; QUALITY.md currently ends at 66 (`corpus/QUALITY.md:627`).
The tip leg is a disposition rule rather than an exit-0 gate. As long as the round-42 successor stays
unbuilt, an exit-0 tip gate would fail every round on legitimate gate edits, which is bad operability.
The per-receipt pinned leg has no committed runner yet. Its runnable form is the Run 3 loop above.
Committing it, e.g. as `corpus/evidence/round47/receipt-spot.sh` with a `## Gates` row, is the L1's call;
this seat writes no lane files.

## Pointers

- verifier `round39/verify-receipts.py` `1b6e0de688deda74…` (refusals :128 :134 :139 :196 :206 :213); counter `round40/c1-count.py` `d9b38b57de412b44…`; manifest `e462315950321447…`
- gate `tools/research-gate.sh` tip `2cb04bddfd5601d7…`, bound in the active receipts as `4253c18738f84df9…`
- open routed item: `lessons/round-41.md:55-71`; `lessons/round-41-verifier-spotcheck.md:78` (D1 → round 42)
- R1/R2 records: `corpus/evidence/round39/claims.md:196-197`; `corpus/knowledge/receipt-expectation-digests-r40.md:15`

## Risks / blockers

No blocker. The tip leg stays red until a successor counter or a reissue lands (routed since round 41).
Python 3.14.8 and `/usr/bin/strace`; no tool installed. Scratch deleted. L1 should re-run Run 2 and the pinned falsifier.
