# Attack22 — R39/R40 active-receipt drift (item #5)

Role: critic (leaf). Verdict: **expected revision drift, not corrupt evidence**; a safe
byte-preserving repair exists and requires no receipt rewrite and no fetch.

## What was inspected (all local, read-only)

- Committed receipts: `corpus/evidence/round40/receipts/{c1-base-s39001,c1-after-s39011,c1-mutenv-s39013}-regenerated.json`, `corpus/evidence/round39/receipts/{c1-after-s39111,c2-after-s39101,c2-after-s39121}.json` (the 6-row active manifest `active-r39-receipts.tsv`), plus the four non-active r39 originals.
- Adding commits: `6d914e9` (r39; gate `4253c187…`), `d164f88` (r40 regenerations; gate unchanged).
- Tip-gate change: `1bd9001` (r41) moved `tools/research-gate.sh` `4253c187…` → `2cb04bdd…` (parent `1bd9001^` still `4253c187…`; tip `d4e6ef0` still `2cb04bdd…`).
- Leading records: `corpus/lessons/round-41.md` (post-landing addendum) and `corpus/lessons/round-47.md` mistake 9 (unclosed routed fix; QUALITY 68 pinned/tip legs; "receipts themselves are not repaired this round (named, routed to round 48)").

## Measured facts (commands + observed output)

1. Commit-identity of receipts: `git diff --stat d164f88 -- corpus/evidence/round40/` and `git diff --stat 6d914e9 -- corpus/evidence/round39/receipts/{c1-after-s39111,c2-after-s39101,c2-after-s39121}.json` → **empty**. Receipts are byte-identical since their adding commits; no post-hoc rewrite.
2. Receipt bindings vs committed bytes at tip (sha256sum):
   - counter `91618e91…` = `corpus/evidence/round39/c1-count.py`; counter `43849e9a…` = `corpus/evidence/round39/c2-count.py`; verifier `1b6e0de…` = `corpus/evidence/round39/verify-receipts.py`; expectations `01cbdc3a…` = `corpus/evidence/round39/expectations.jsonl`; base gate `0447ad14…` = `.ufo/waves/round-39/controls/base-gate-r39.sh`; mutant gate `e1251030…` = `.ufo/waves/round-39/controls/mut-gate-path-env.sh`.
   - Landed r39 gate `4253c187…` = `git show 6d914e9:tools/research-gate.sh` (and `d164f88:…`); live tip gate `2cb04bdd…` = `git show HEAD:tools/research-gate.sh`.
3. Verifier re-run per active receipt against its **bound** gate bytes (`verify-receipts.py` r39, `--expectations` committed): **6/6 `VERIFY: ok` rc 0** (base→base-gate-r39.sh; mutenv→mut-gate-path-env.sh; the four landed-gate rows→byte-extracted `4253c187…`).
4. r40 counter at its scoped revision: `git archive 6bc90e0` → `python3 corpus/evidence/round40/c1-count.py` → `R39_ACTIVE_RECEIPTS=6/6` exit 0 (matches the r41 addendum's replay claim).
5. r40 counter at tip: `python3 corpus/evidence/round40/c1-count.py` → `R39_ACTIVE_RECEIPTS=2/6` exit 1; the four rows routed to `tools/research-gate.sh` print `VERIFY-FAIL: gate-sha256-mismatch`; the two control-gate rows still `ok`.
6. Non-active r39 originals (excluded by design, not repair targets): `c1-after-s39011/c1-base-s39001/c1-mutenv-s39013` → `expect-sha256-mismatch` (R1 stale `3abd2dcb…`), `c1-mutenv-s39003` → `counter-sha256-mismatch` (superseded draft, uncommitted counter digest).

## Analysis

- The refusal is the receipt binding working: each receipt records the exact gate bytes measured
  (`pre==post==4253c187…`), and the verifier re-derives the live path's digest. The r41 gate
  edit is an intentional, committed change of the measured subject; old bindings are then
  *supposed* to refuse. Round-41's addendum already names this "correct receipt semantics, not a
  regression" and scopes the r40 predicate to revision `6bc90e0` + gate `4253c187…`, where the
  counter replays 6/6 — reproduced in fact 4.
- Not corruption: receipts byte-identical since commit (fact 1); all six verify against bound
  bytes (fact 3); counter/verifier/expectations digests still match committed files at tip
  (fact 2); the only drifted object is the gate path the four rows point at. No verifier defect,
  no recipient tamper, no receipt rewrite after commit.

## Safe byte-preserving repair (exists; no receipt rewrite, no fetch)

- **Option A — verify against recorded revision (zero new files):** run the r40 counter/verifier
  against the bound gate bytes, e.g. `git show 6d914e9:tools/research-gate.sh > gate-r39-landed.sh`
  and verify each row with `--gate gate-r39-landed.sh` (proven 6/6). This is the r41 successor
  design's option (b) applied without any file change.
- **Option B — durable pin (recommended):** commit a byte-exact copy of the r39 landed gate under
  `.ufo/waves/round-39/controls/landed-gate-r39.sh` (extract from the local object; no network)
  and repoint the four manifest rows at it (manifest/tab edit only — receipts and their digests
  stay untouched). Tip verification then permanently replays 6/6 and satisfies the round-47
  QUALITY 68 "pinned and tip legs" fix with a stable pinned leg.
- **Do not** re-stamp or rewrite any receipt (destroys the historical binding evidence the r40
  C1 claim rests on) and do not change `tools/research-gate.sh` (would break r41+ claims). L0
  `8d77e6c1` fetch-scope question is orthogonal and stays open under no-fetch; it does not affect
  this verdict.

## Commands run (decisive)

`git log --oneline --follow -- corpus/evidence/round{39,40}/receipts/`; `git log --oneline -- tools/research-gate.sh`; `git show <rev>:tools/research-gate.sh | sha256sum`; `sha256sum` of counter/verifier/expectations/control gates; `git diff --stat d164f88/6d914e9 -- <paths>`; `git archive 6bc90e0 | tar -x -C /tmp/chousa-r48-A22` then `python3 corpus/evidence/round40/c1-count.py`; tip `python3 corpus/evidence/round40/c1-count.py`; per-receipt `python3 corpus/evidence/round39/verify-receipts.py --receipt <f> --gate <bound> --counter <c{1,2}-count.py> --expectations …/expectations.jsonl` for all 6 active + 4 legacy rows. Scratch `/tmp/chousa-r48-A22` removed. No installs. No lane files modified.
