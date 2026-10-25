# Attack30 — QUALITY 68 pinned/tip values and round-39/40 receipt attribution

Seat: L1Chousa48.Attack30 (critic) · date: 2026-10-25 · lane: chousa-shokunin
Item (w1-spec): audit QUALITY 68 pinned/tip values (6/6, 2/6) and round39/40 attribution
against committed round artifacts. Read-only; scratch `/tmp/chousa-r48-attack30*` removed.

## Verdict

QUALITY 68's stated values reproduce exactly from committed bytes: pinned leg **6/6**
(b173b094, d164f88), tip leg **2/6** (a15610a5, current tip), all four refusals
`gate-sha256-mismatch` and drift, not receipt corruption. The round-39/40 receipt
attribution is correct. One defect found: **SCORECARD.md:2531 calls round 41
"QUALITY 68's first run" — the criterion was added in round 47; the round-41 run
predates it.** No scorecard edits made (report only).

## Measured facts

Re-runs (git archive → /tmp; `python3 corpus/evidence/round40/c1-count.py`):

- `d164f88` archive (r40 work commit, adds the three regenerated receipts):
  `R39_ACTIVE_RECEIPTS=6/6`, exit 0.
- `b173b094` archive (parent of the r41 gate edit `1bd9001`): 6/6, exit 0.
  Gate `tools/research-gate.sh` at `b173b094` = `4253c18738f84df9…` (matches receipt bindings).
- `a15610a5` archive (r47 C1 landing, named in the criterion's Check line): 2/6, exit 1;
  refusals `c1-after-s39011-regenerated.json`, `c1-after-s39111.json`, `c2-after-s39101.json`,
  `c2-after-s39121.json` — all `VERIFY-FAIL: gate-sha256-mismatch`.
- Current tip `d4e6ef0` archive: 2/6, exit 1, same four refusals.

Pinned vs tip: 6/6 at b173b094/d164f88; 2/6 at a15610a5 and tip. The four failing rows bind
`tools/research-gate.sh` sha `4253c187…`; commit `1bd9001` (round 41) moved the file to
`2cb04bdd…` (+92 −2). The two passing rows bind control gates that were never changed:
`base-gate-r39.sh` (`0447ad14…`) and `mut-gate-path-env.sh` (`e1251030…`); current shas match.

## Integrity of the four failing receipts (not corruption)

- Self-digest (`receipt_sha256` vs canonical `json.dumps(body, indent=2, sort_keys=True) + "\n"`):
  all six active receipts OK.
- Every receipt's last-touched commit equals its adding commit (`d164f88` r40 ×3; `6d914e9`
  r39 ×3): receipts are byte-unchanged since commit; no receipt was edited after the drift began.
- The gate commit `1bd9001` is after all four adding commits → refusals are expected revision
  drift under QUALITY 68's tip-leg disposition rule, not defect. Confirmed by r41 lesson
  (post-landing addendum) and r47 round `ExecReceiptSpot` (Run 2/3).
- R1/R2 attribution: manifest `active-r39-receipts.tsv` (added `6c01a41`) = 3 r40 regenerated
  + 3 preserved r39 originals; r39 erratum R1/R2 (claims.md:196-197) names exactly the three
  regenerated files and the superseded `c1-mutenv-s39003.json` (excluded, preserved). Consistent.
- `measure-after.txt` (r40) records the same 6/6 six-row population; verifier binding
  (`verifier_sha256=1b6e0de…`) matches the committed `round39/verify-receipts.py`.

## Disputed-value resolution

Round-47 wave-2 `RevLesson` claimed the criterion's tip value false ("6/6 at `a15610a5`").
Independent re-run (this seat) gives 2/6 at `a15610a5`, matching both the committed criterion
and `RevQ68`'s identical reproduction. The dispute resolved to a mistaken observation; the
criterion's stated values stand.

## Defect: scorecard misattributes QUALITY 68's first run

`SCORECARD.md:2530-2531`: "repair or supersede the four round-39/40 receipts that fail
`gate-sha256-mismatch` since round 41 (QUALITY 68's first run; routed in round 41, never closed)".
- Criterion 68 was added in **round 47** (`git log -S "A committed receipt is re-verified every round"`
  → `3d2a063`; QUALITY.md "Round-47 additions", appended 2026-10-25; criteria 1–66 unchanged).
- The round-41 lesson records the drift and routes a successor-counter design to round 42; it
  never mentions QUALITY 68. The scorecard's parenthetical is a false provenance.
- Smallest correction: "since round 41 (routed in round 41; QUALITY 68, added round 47, has
  carried it through rounds 47–48 as its only unresolved receipt issue)" — wording only; no
  numeric change.

## Named limits (still open, unchanged by this audit)

- c2 receipts bind `subject_counter` as an absolute live-lane path (`/home/vgpnk/Projects/shokunin/
  chousa-shokunin/corpus/evidence/round39/c1-count.py`); archive runs read the live file. Live
  bytes match the bound digest and the `6d914e9` blob, so pinned results are not distorted.
- Pinned leg anchors on the adding commit (receipts carry no revision field); a pass proves
  integrity against committed bytes, not authorship.

Commands run: `git log --format='%h %P %s' -1 1bd9001` (parent b173b094); `git merge-base
--is-ancestor d164f88 b173b094` (YES); `git archive/receipt | tar -x -C /tmp/…` then
`c1-count.py` at d164f88/b173b094/a15610a5/HEAD; `git show <rev>:tools/research-gate.sh |
sha256sum`; `git log -1 --diff-filter=A -- <receipt>` ×6; receipt field/digest checks.
No installs; no fetch; no lane production file modified.
