ATTACKS: QUALITY 68 (committed-receipt re-verify, pinned + tip legs, Shown-able-to-fail byte change); lesson mistake 9 (same claim)
VERDICT: holds

Runs (all on /tmp archives of the lane repo; no lane files touched):
1. `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin archive b173b094 | tar -x -C /tmp/chousa-r47w2-RevQ68/tree-b173b094 && (cd /tmp/chousa-r47w2-RevQ68/tree-b173b094 && python3 corpus/evidence/round40/c1-count.py)` → `R39_ACTIVE_RECEIPTS=6/6`, exit 0 (all six `VERIFY: ok`).
2. Same at lane tip `1fc5ed193ad48a482402c862f4e4cc47e46d5b2d` → `R39_ACTIVE_RECEIPTS=2/6`, exit 1; the four refusals are `VERIFY-FAIL: gate-sha256-mismatch` on `corpus/evidence/round40/receipts/c1-after-s39011-regenerated.json`, `corpus/evidence/round39/receipts/c1-after-s39111.json`, `corpus/evidence/round39/receipts/c2-after-s39101.json`, `corpus/evidence/round39/receipts/c2-after-s39121.json`.
3. Same at the criterion's named intermediate rev `a15610a5` → `R39_ACTIVE_RECEIPTS=2/6`, exit 1, same four refusals (matches criterion's stated value).
4. "Shown able to fail" byte change: in the `b173b094` copy, byte 676 (1-indexed) of `corpus/evidence/round40/receipts/c1-base-s39001-regenerated.json` is the `7` of `"matched": 7` (context `,\n  "matched": 7,\n  "predicate`); setting it to `6` → `VERIFY-FAIL: receipt-self-digest`, `R39_ACTIVE_RECEIPTS=5/6`, exit 1. Restoring `7` → 6/6, exit 0, file sha256 `e33199c1193ce6f0fb12cef788b41d79d2eb31181bbfdafe3d2f2eba97aa46af` == `b173b094` version (matches criterion's stated values).
5. Pinned leg (criterion: verify at each receipt's adding commit): round-40 receipts (adding commit `d164f88`): archive run → 6/6, exit 0. Round-39 receipts (adding commit `6d914e9`; round-40 counter does not exist there): ran `corpus/evidence/round39/verify-receipts.py` directly for `c1-after-s39111.json`, `c2-after-s39101.json`, `c2-after-s39121.json` → each `VERIFY: ok`, rc 0.
6. Tip-leg attribution: `git log -1 -- tools/research-gate.sh` → `1bd9001` (round-41), moving sha `4253c187…` → `2cb04bdd…`; `1bd9001` is after both adding commits (`d164f88`, `6d914e9`), so all four refusals are drift, and lesson round-47.md:99-106 lists `gate-sha256-mismatch` + `1bd9001` and routes to round 48 (receipts not repaired).

Named-limit audit (criterion lines 678-681): `subject_counter` in the c2 receipts is an absolute live-lane path (`/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round39/c1-count.py`); live file sha256 `91618e91640f748df76282244186088218d5f2b7a65364137fa6add29fea05d5` == receipt binding, and the file is unchanged since `6d914e9`. So archive copies read the same bound bytes; the named-limit note is accurate and did not distort the results above.

Minor observation (not a defect): the lesson lists the refusal class and the commit but not the four receipt paths individually; the claim's Check line and stated values are satisfied verbatim, and the same four receipts are named in the counter output (run 2). QUALITY 68's stated values (6/6 exit 0; 2/6 exit 1; 5/6 exit 1) reproduce exactly; lesson mistake 9's evidence (tip 2/6; b173b094 6/6; one changed byte → 5/6) reproduces exactly.

Tools installed: none (a standard `python3`/`git`/`tar` invocation; no installs required).
Scratch `/tmp/chousa-r47w2-RevQ68/` deleted before finish (tree archives + a15610a5 copy removed).
