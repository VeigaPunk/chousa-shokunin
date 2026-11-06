# R82ScoutNovelty — scoped findings (round 82, wave 1, lane chousa)

Seat: `R82ScoutNovelty`. Scope: per-surface reconnaissance for C2 K4 (ground already held), the registry at
the landing revision, and the README coverage map. Leaf seat: read-only — no lane or fleet git/jj mutation,
no commits or pushes, no production edits, no subagent dispatch, no network fetch (no item in this seat names
a re-open).

Full detail and every command: `.ufo/waves/round-82/w1/R82ScoutNovelty/recon.md`.
Receipts (recorded outputs): `.ufo/waves/round-82/w1/R82ScoutNovelty/receipts/*.out` (each `.out` is the
output of the `.txt` command file beside it).
Revisions: base `142b6f0c08e645ef9507f6d880be44e518c39043`, landing `b4a41d251b488f06b4a6ab01a11bc12ce72edd20`
(the bytes attacked), tip `46dd1dc31e55c5a9133a0da47e22f8b598946cf1`.

---

## C2 K4 — ground already held? **No. K4 does not fire.**

- Frozen grep at base over `corpus/knowledge corpus/README.md SKILL.md PROVINCE.md` for
  `PICO|PCC|PECO|SPIDER|question fram|answerable question|eligibility criteri|protocol deviation|review question`
  → 7 hits, **all adjacent**, none a decision table or decision list on choosing/aligning a review question
  frame: `PROVINCE.md:5` (ownership), `SKILL.md:3` (trigger description), `SKILL.md:17` (the lane's own
  intent-table row naming "question framing" as a method step), `archived-export-intake.md:89` (the near
  neighbour claims.md names — an archive claim label), `quality-control-guideline-issued-text-r48.md:15`
  and `:26` (the other near neighbour — one Chinese instrument's PICOS-optional inclusion rule),
  `japanese-search-record-r38-amendment-2026-10-23.md:11` (a protocol-content paragraph).
- Structural sweep at base: only **three** base knowledge entries carry a `## Decision` heading
  (`citation-searching-tarcis-r81.md:29`, `correction-retraction-status-r81.md:36`,
  `recheck-due-r26.md:21`) — none on question framing. Exactly **one** base knowledge file contains
  `PICO` at all (the r48 near neighbour). `PCC`/`PECO`/`SPIDER`: **zero** in base `corpus/knowledge`,
  base `corpus/README.md`, base lessons. Base `corpus/README.md` has no `Decision` heading. Base
  `corpus/QUALITY.md` and `corpus/MINT.md`: **no** frame hits. Every base heading that could carry a
  frame-choice list (`## The rule*`, `## Disposition table/rule`, `## The sweep rule`, `## The token rule`,
  `## The seven rule classes`, `## Reading rule`) was read: all are about metadata screens, gate findings,
  aliasing or token boundaries.
- Closest base surface (reported, not a fire): base `corpus/SOURCES.md` row S008's `teaches` cell already
  said "Frame an answerable question first and keep review PICO, synthesis PICO, and included-study PICO
  distinct", and base `## Paths` said "scope the question before searching (PICO levels)". K4 targets a
  *base-list entry* holding a decision table/list; the base entry list holds none. But a K3 reviewer should
  know the new entry's PICO-level rows ground a **pre-existing base registry proposal**.

## C2 counter at the landing — measured here, PASS

`python3 -B corpus/evidence/round82/depth-r82.py --root <archive of b4a41d25>` →
`ENTRY question-framing-frames-r82.md ok=yes rows=9 quotes=11/11 fails=-` /
`DEPTH_R82 entries=1 ok_entries=1 rows=9 located_quotes=11 fresh_sources=4` / `DEPTH_R82=PASS`, exit 0.
Target met (rows ≥5 → 9; located_quotes ≥5 → 11; fresh_sources ≥3 → 4). All 11 declared quotes located in
their committed capture texts; all five capture sha256s equal their `refetch.tsv` `txt_sha256` cells.
C2's K2 (quote absent / sha mismatch) is not fired by anything measurable.

## Registry at the landing

- **No duplicate URL introduced.** Fleet census `validate` at base and at landing print the **identical** five
  W04 warnings (`S051 S053 S073 S074 S075`) and then `ok`, exit 0; **no W04 names S008, S028, S209, S210 or
  S211**. The three JBI rows share a host and wiki space but have three distinct page paths, so the census'
  whole-URL normalisation keeps them apart. S008's row already existed at base with the same URL.
  (Census E11 lines appear only when the registry file is copied outside the tree — an artefact of the
  invocation, not a lane defect; the in-tree form is `ok`.)
- Census counts: base `rows=208 queued=19 mined=166 rejected=23`; landing `rows=211 queued=17 mined=171
  rejected=23`.
- **Queued rows the new entry could have cited: none.** All 17 rows still queued at the landing
  (S009–S012, S017–S024, S026, S027, S030–S032) have **no capture in the tree** (`sha256(url)[:24]` key
  absent for every one), and `refetch.tsv` rows dated on/after the round start exist for exactly the round's
  own five ids (S008, S028, S209, S210, S211). The two topically-nearest queued rows are S009 (MECIR
  risk-of-bias) and S017 (PRISMA 2020) — neither is a framing source and neither has bytes; S019 is the same
  URL as mined S029, whose row supersedes it ("S029 supersedes S019", `metadata-screen-r25.md:89`).
- **The S008 re-open changed no taught content.** Cell-by-cell diff base vs landing: `teaches` **byte-identical**
  ("Frame an answerable question first and keep review PICO, synthesis PICO, and included-study PICO
  distinct"); `id`/`source`/`kind`/`tier`/`scope`/`opened`/`recheck` unchanged. Changed: `anchor`
  (now names the three PICO stages + capture key + serve date), `status` `queued`→`mined`, `usedby` `—`→
  the new entry. S028's row changed in the same three cells with `teaches` byte-identical.

## README coverage map

- **Placement is right.** The README's top `## Coverage map` table (lines 3–96) names only 43 of the 93 base
  `corpus/knowledge/*.md` files and omits both round-81 entries; the lane's convention is a per-round section
  at the end (`## Round81 coverage and frontier` at base 1367, `## Round82 coverage and frontier` at landing
  1377). The landing puts the new entry in a per-round table row, matching that precedent, and G02 passes
  (`G02 knowledge-index PASS 94 entries indexed`).
- **DEFECT — the Round82 section names `lessons/round-82.md`, which does not exist** in the landing revision
  or at the tip (`git ls-tree … -- corpus/lessons/round-82.md` → empty at both). The round-81 section names
  `lessons/round-81.md`, which does exist at base — so the round-82 bullet breaks the precedent it copies.
  No gate catches it (G02 indexes only `corpus/knowledge/*.md`; census E11 checks only `used-by` cells).
  Scope note: while this seat was finishing, another seat created `corpus/lessons/round-82.md` as an
  **untracked** worktree file; it is in neither the landing revision nor the tip, so the finding as stated
  (the *committed* tree holds no such note) stands.
- **RESIDUAL — the base Frontier sentence at README line 859 is stale**: it still lists S008 among "the queued
  SOURCES rows S008–S012, S017, S018 waiting for an entry that mines them", while S008 is `mined` at the
  landing.
- **The Round82 coverage table row itself is accurate** — its "Holds" text matches the entry's rows 1–5 and 9
  (PCC mapping, PICO/PECO precursor, three PICO stages, eligibility per frame element, protocol deviations
  with justification) and its Sources cell `S008, S209, S210, S211` matches the entry's `source:` line and the
  registry `usedby` cells. The other two bullets (Crossmark addendum; S009/S017/S019 stay queued) are true of
  the tree.
- **r81 routed defect 4 is still open at the tip**: no committed G02/`PREFLIGHT=1/1` receipt exists under
  `corpus/evidence/round82` (only `after/c1-after.txt`, `after/c1-selftest-after.txt`,
  `after/c2-after.txt`).

## Other measured surfaces (frontier)

- C1 counter at the landing: `RUNLINES=2/2 K2_REFUSED=11/11 HOLD_REFUSED=9/9 CLASS_REFUSED=24/24
  POSITIVE=6/6` / `K2_GATE=PASS`, exit 0. Gate selftest (run once here): `RESEARCH_GATE_SELFTEST: PASS
  (280 cases, 0 skipped)`, exit 0 → C1's K4 not fired (PASS, 0 skipped, 280 ≥ 275).
- Preflight G01–G07 at the landing tree: all PASS, `PREFLIGHT=7/7`, exit 0 (G08 skipped there; selftest run
  separately as above).
- **K3 candidate at the landing bytes (evidence only; the verdict belongs to a non-author reviewer seat):**
  row 1's Never clause at the landing reads "force an intervention, comparator and outcome onto a mapping
  question", warranted by Q6 ("JBI suggests utilising the PCC … approach") and Q7 ("…can be seen as
  hypothesis-generating, whereas a systematic review is hypothesis-testing"). Neither quote states a
  prohibition, and the same page's next paragraph (Q8) reads "there may be a compelling argument to use a
  different question format (such as PICO or Population, Exposure, Comparator, Outcome [PECO]), such as when
  performing a structured analysis of existing research or research gaps, or as a precursor to a systematic
  review" — which contradicts the Never as written. The uncommitted worktree copy of the entry already
  repairs row 1 and row 7 and appends a `## Correction (round 82, after scoring)` section; per claims.md, a
  repair after scoring does not rescue the landing revision.
- **C1 wording observation:** the landing reworded the surrounding prose of both SKILL.md Run lines while
  leaving the backticked commands verbatim, so "Run lines stay byte-identical to base" holds only in the
  frozen counter's sense (command text), not for the whole line. The counter's `RUNLINES=2/2 found=yes`
  check is unaffected.
- The Round82 section's Crossmark addendum (`correction-retraction-status-r81.md`) contains the round's one
  "Never" clause not traceable to a quote ("treat an absent Crossmark button as 'no correction or
  retraction'"). The addendum labels it as the lane's reading and the source does not state it; it sits
  outside the C2 counter's scored entry, so the counter's PASS says nothing about it.

Tooling: none installed or upgraded by this seat (`uv`/`npm`/`pacman` untouched). Binaries used, all
pre-installed: `git`, `python3`, `bash`, `grep`, `awk`, `sha256sum`, `sed`, `sort`, `diff`. The fleet census
`scripts/sources-census.sh` was used unmodified and read-only. Scratch
`/fast/scratch/hyaku/chousa-r82/R82ScoutNovelty/` was deleted before this report was written; every receipt
cited above was copied into `.ufo/waves/round-82/w1/R82ScoutNovelty/receipts/` first.

VERDICT: R82ScoutNovelty C2 K4 held — no base entry, README, SKILL.md, PROVINCE.md, QUALITY.md, MINT.md or lesson holds a decision table/list on choosing or aligning a review question frame, so the ground was not already held and K4 does not fire; the landed bytes themselves carry the defects listed above (README names a nonexistent `lessons/round-82.md`, stale line 859, S008's anchor omits §2.5.2 where quote Q5 sits, and row 1's Never clause is contradicted by Q8 in the same source page).
