# R81ScribeLesson — round-81 lesson draft (C1 depth, C2 operability)

Seat: leaf scribe, no subagents, no agent://all. Lane root `/home/vgpnk/Projects/shokunin/chousa-shokunin`.
Measured revision: landing `7e2da96a0541946e796384d42fea18e09ede9e9f`; base `378fda82dc2cbcc555a0565052cc408121813cef`;
freeze `bb54e7f89da9ba4213aec9d976c13f3f4ba548fb`; prefreeze controls
`f7929f877e6fd54f4dc5ce7f993da46bc7df43f9`. Claims read from `corpus/evidence/round81/claims.md`
(frozen; not amended).

## Behavior

Drafted, **not landed**, the round-81 lesson sections the seat item names:

1. `## Gate` — one record per new registry row S203–S208, each with URL, fetch time (the 2026-11-06
   `refetch.tsv` time), tier, decision, and — for the five admitted rows — a ≤25-word quote located in the
   committed capture text with its `wc -w` count and the locating `python3 -c` substring test; S208 is
   recorded as rejected-unreachable (HTTP 403) with its flip condition. Also logged every
   status/recheck/used-by cell change old→new (all six rows are new, so every value is `— → …`).
2. `## Mistakes` — one mistake mined from the rejected rounds (r80 draw-label vs receipt-name mismatch),
   with class, evidence pointer, captured-by, and a fix demonstrated **failing** on the prose labels and
   passing on the receipt-true labels.
3. `## considerthese` — read `considerthese/2026-11-05.md` and `2026-11-06.md` (neither edited); named one
   still-unimplemented proposal (2026-11-06 "one open Gate-record S-id per daily review") and measured that
   this round does not implement it.
4. `## Assimilation` — `none`, with the round-78 collision re-count (111 of 114 staged ids) and the absence
   of any `merge` directory under the fleet root.

Both frozen counters were executed at the landing revision (not merely quoted): C1 `DEPTH_R81=PASS`,
C2 `CHECKLIST=PASS`. No production file was edited; no git/jj mutation, no commit, no push; no network was
used (this seat's item names no re-open). Scratch `/fast/scratch/hyaku/chousa-r81/R81ScribeLesson/` was
created with `mkdir -p`, the archive tree lived there, and it was removed before this report was yielded.

## Gates (exact command → receipt → observed line → exit code)

| # | check | command | receipt | observed | rc |
|---|---|---|---|---|---|
| 1 | C1 depth counter at landing | `git archive 7e2da96a \| tar -x -C $D` then `python3 -B corpus/evidence/round81/depth-r81.py --root "$D"` | `.ufo/waves/round-81/w1/R81ScribeLesson/receipts/02-c1-depth-landing.txt` lines 6–8 | `DEPTH_R81 entries=2 fresh_rows=5 located_quotes=14` / `DEPTH_R81=PASS` / `RC=0` | 0 |
| 2 | C2 checklist counter at landing | `python3 -B corpus/evidence/round81/checklist-run.py --root "$D"` (same tree) | `.../receipts/03-c2-checklist-landing.txt` lines 9–11 | `CHECKLIST_RUN=6/6 DISCRIMINATE=3/3` / `CHECKLIST=PASS` / `RC=0` | 0 |
| 3 | Gate quote location, 5 admitted rows | `LOC='import sys;t=" ".join(open(sys.argv[1],encoding="utf-8",errors="replace").read().split());print("FOUND" if " ".join(sys.argv[2].split()) in t else "ABSENT")'; python3 -c "$LOC" corpus/captures/<key>.txt '<quote>'` | `.../receipts/01-gate-quote-locate.txt` lines 3–4 (S203), 7–8 (S204), 11–12 (S205), 15–16 (S206), 19–20 (S207) | `located=FOUND words=13/15/13/10/25 rc=0` on all five | 0 |
| 4 | capture bytes == fetch record | `sha256sum corpus/captures/<key>.txt` vs `refetch.tsv` `txt_sha256` | `.../receipts/08-capture-sha.txt` lines 3–7 | five `MATCH`, `RC=0` (full digests in receipt) | 0 |
| 5 | S208 unreachable state | `sed -n '151p' corpus/evidence/round57/refetch.tsv`; `ls corpus/captures/5802b641e7092ed5c07e36e4.*` | `.../receipts/04-s208-unreachable.txt` line 3 (refetch row), line 10 (flip cell), lines 16–17 (`ls` error) | `curl_rc=22 http=403`; `ls: cannot access …` / `RC=2` (the rc is the `ls`, not the row) | 2 (`ls`) |
| 6 | registry cell changes | `git show 378fda82:corpus/SOURCES.md \| grep -cE '^\| S20[3-8] '`; `git diff --stat 378fda82 7e2da96a -- corpus/SOURCES.md`; per-row cell dump | `.../receipts/05-registry-cells.txt` lines 3–7 and 9–14 | `0` / `RC=1` (no rows at base); `6 ++++++`, `6 insertions(+)`; cells as tabled in the draft | 0 (except the deliberate `grep -c` 1) |
| 7 | draw-label fix, able to fail | `python3 -B .ufo/waves/round-81/w1/R81ScribeLesson/check-draw-labels.py .ufo/waves/round-81/w1/R81ScribeLesson/labels-bad.tsv` and `…/labels-good.tsv` | `.../receipts/07-draw-label-fix.txt` lines 3–6 (bad) and 9–12 (good) | `DRAW-LABEL MISMATCH … stated=PASS actual=FAIL` ×2 / `DRAW_LABELS bad=2` / `RC=1`; then `DRAW-LABEL OK …` ×2 / `bad=0` / `RC=0` | 1 then 0 |
| 8 | round-78 collision re-count | `wc -l .ufo/waves/round-78/assimilation/{collisions,staged-ids,reg-ids}` | `.../receipts/06-collisions.txt` lines 3–5 | `111`, `114`, `192`; `RC=0` | 0 |
| 9 | considerthese: twelve ids re-opened? | `grep -rn 'S170\|S171\|S173\|S174\|S175\|S176\|S178\|S179\|S182\|S183\|S191\|S193' corpus/evidence/round81/ .ufo/waves/round-81/` then `--exclude-dir=R81ScribeLesson \| wc -l`; `ls corpus/lessons/round-81.md`; `find … -maxdepth 4 -type d -name merge \| wc -l` | `.../receipts/09-considerthese-check.txt` lines 50–54 (3 self-hits), 55–57 (`0`), 60–62 (`No such file or directory`, rc 2), 63–64 (`0`) | no round-81 artifact re-opens the backlog; no lesson; no `merge` dir | 0 / 2 / 0 |
| 10 | locating query + knowledge delta | L1 transcript `history://ChousaR81` line 134; `git ls-tree -r <rev> corpus/knowledge \| wc -l` | `.../receipts/10-search-query-and-knowledge-delta.txt` lines 2–3, 5–7, 9–10 | `web_search(TARCiS statement citation searching Hirt BMJ 2024 PMC full text)`; knowledge 92 → 94; the two new entry paths | 0 |
| 11 | draft self-check (records ↔ registry/fetch/captures) | `python3 - <<'PY'` parser over the draft's `GATE-RECORD` lines (full body in receipt) | `.../receipts/11-draft-gate-selfcheck.txt` lines 3–8 | `RECORD S203…S208 admit/reject ok=True`; `GATE_RECORDS=6 bad=0`; `RC=0` | 0 |

The command in row 3 is reproduced with its two arguments filled, per row, in receipt 01 at the cited
lines; the `wc -w` values were produced by `printf '%s\n' '<quote>' | wc -w`. Row 5's `RC=2` is the `ls`
exit (no capture exists), not a failure of the rejected row.

## Findings

**F1 — both frozen predicates hold at the landing revision, as measured here.** C1 prints
`DEPTH_R81 entries=2 fresh_rows=5 located_quotes=14` / `DEPTH_R81=PASS` rc 0; C2 prints
`CHECKLIST_RUN=6/6 DISCRIMINATE=3/3` / `CHECKLIST=PASS` rc 0 (`receipts/02…:6-8`, `receipts/03…:9-11`).
This is the counter's exit-0 condition, nothing wider: K2 (live re-open) and K3 (decision-table
contradiction) were **not** exercised by this seat — K2 is another seat's item and needs network, which
this seat did not use.

**F2 — S207's counted quote sits exactly on the frozen 25-word bound.** `words=25`, `located=FOUND`
(`receipts/01-gate-quote-locate.txt:20`). The depth counter accepts 1–25 inclusive and counted it
(`located_quotes=14`), so the claim holds as frozen; any edit that adds one word to that sentence drops the
row from P2. Recorded in the draft as a boundary observation, not a defect.

**F3 — the egress table's record cell is not yet satisfied by any committed byte.** `egress-approval.md:21`
requires "query and chosen URL in the lesson `## Gate`". The query exists only in the L1 session transcript
(`history://ChousaR81:134`: `web_search(TARCiS statement citation searching Hirt BMJ 2024 PMC full text)`);
`receipts/10-search-query-and-knowledge-delta.txt:2-3` records it and states that no committed file holds
it. The draft carries the query with that provenance; if the lesson lands without it, the egress record
cell stays unmet.

**F4 — the r80 draw-label mismatch is evidenced by the closure's record plus the receipts, not by the
mislabelled prose itself.** At `7e2da96a` the string `run1 PASS` appears only in
`corpus/lessons/round-80-verifier-spotcheck.md:27,73` and `considerthese/2026-11-05.md:30`; the round-80
report sentence that carried the wrong labels is not a committed path in this lane. Ground truth is the two
committed receipts (`r80a-after-v7-run1.txt:216` = `BATTERY=FAIL … fresh_positive=1/2 fresh_forgers=1/2`;
`r80d-v7-run2.txt:216` = `BATTERY=PASS … fresh_positive=2/2 fresh_forgers=2/2`). The drafted fix
(`check-draw-labels.py`, receipt 07) fails closed on the prose labels (rc 1) and passes on the receipt-true
labels (rc 0), so it is shown able to fail rather than merely asserted.

**F5 — the "one open Gate-record S-id" proposal is not implemented by this round.** With this seat's own
folder excluded, the twelve ids (S170, S171, S173–S176, S178, S179, S182, S183, S191, S193) occur zero
times in `corpus/evidence/round81/` and `.ufo/waves/round-81/` (`receipts/09…:55-57`), and
`corpus/lessons/round-81.md` does not exist. The first, unfiltered grep printed 3 hits — all inside this
draft and its own receipt — and is shown at `receipts/09…:50-54` rather than hidden.

**F6 — instrument trust boundary.** The five captures are committed bytes whose sha256 equals their
2026-11-06 `refetch.tsv` `txt_sha256` (5/5 MATCH, `receipts/08…:3-7`), but whether the hosts still serve
those bytes was not tested (no network). S208's "a correction exists" rests on the search-result snippet
the entry records, never on a read page (403).

**F7 — process note (self-caught, no artifact).** A first version of receipt 09 printed a `CMD:` label that
did not match the grep actually executed (`^| S2` vs `^| S20[3-8] `; output `6`). It was caught before any
citation, the receipt was regenerated so its `CMD:` line states the executed pattern
(`receipts/09-considerthese-check.txt:58-59`). Same class as F4 — a label is a claim about a command — and
worth naming because the label, not the command, is what a reader tends to trust.

## Touched surfaces

- Wrote only under `.ufo/waves/round-81/w1/R81ScribeLesson/`: `lesson-draft.md`, `check-draw-labels.py`,
  `labels-bad.tsv`, `labels-good.tsv`, `receipts/01…11`.
- Read-only: lane tree at `7e2da96a`, `corpus/SOURCES.md`, `corpus/captures/*`, `corpus/evidence/round57/refetch.tsv`,
  `corpus/evidence/round81/*`, `corpus/knowledge/*-r81.md`, `corpus/lessons/round-8{0}-verifier-spotcheck.md`,
  `considerthese/2026-11-05.md`, `2026-11-06.md`, `.ufo/waves/round-80/w1/R80ExecA/*`,
  `.ufo/waves/round-78/assimilation/*`, and `history://ChousaR81` (read-only).
- Not touched: `corpus/lessons/round-81.md` (draft only), any production file, `scripts/`, `.ufo/state`,
  `MANIFEST.json`, `considerthese/`, sibling repos. No git/jj mutation, no commit, no push.

## Out of scope / not done

- K1/K2/K3 adjudication of either claim (reviewer/closure seats); this report measures the predicates and
  records limits.
- `corpus/evidence/round81/run-controls.sh` was not re-run: it writes under
  `corpus/evidence/round81/controls/`, outside this seat's write scope. The frozen before-state is quoted
  from `claims.md`, not observed.
- No domain judgment that a located quote grounds the decision-table row citing it (K3), and no judgment
  on the entries' wisdom.
- No re-open/GET of any URL (seat item names none; network forbidden otherwise).
- No tool install or upgrade was needed or performed.

## Artifact paths (all relative to the lane root)

- `.ufo/waves/round-81/w1/R81ScribeLesson/lesson-draft.md` — the drafted `corpus/lessons/round-81.md` sections.
- `.ufo/waves/round-81/w1/R81ScribeLesson/check-draw-labels.py` — the `## Mistakes` fix.
- `.ufo/waves/round-81/w1/R81ScribeLesson/labels-bad.tsv`, `labels-good.tsv` — its two inputs.
- `.ufo/waves/round-81/w1/R81ScribeLesson/receipts/01-gate-quote-locate.txt`
- `…/receipts/02-c1-depth-landing.txt`
- `…/receipts/03-c2-checklist-landing.txt`
- `…/receipts/04-s208-unreachable.txt`
- `…/receipts/05-registry-cells.txt`
- `…/receipts/06-collisions.txt`
- `…/receipts/07-draw-label-fix.txt`
- `…/receipts/08-capture-sha.txt`
- `…/receipts/09-considerthese-check.txt`
- `…/receipts/10-search-query-and-knowledge-delta.txt`
- `…/receipts/11-draft-gate-selfcheck.txt`

VERDICT: R81ScribeLesson C1 depth held — at 7e2da96a the frozen counting command prints `DEPTH_R81=PASS` with `entries=2 fresh_rows=5 located_quotes=14` and exits 0; K2/K3 were not exercised by this seat.
VERDICT: R81ScribeLesson C2 operability held — at 7e2da96a the frozen counting command prints `CHECKLIST_RUN=6/6 DISCRIMINATE=3/3` and `CHECKLIST=PASS` and exits 0; the counter's own forgery legs were not re-run by this seat.
