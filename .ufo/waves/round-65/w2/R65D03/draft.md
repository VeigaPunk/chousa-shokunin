# R65D03 — draft "Trend verdicts" section (round-65 report)

Seat R65D03 (scribe, wave-2 falsify). Draft only; no lane file was edited.
All citations below are read from the committed lane tree at tip `62b0af1538e067f014ed96d6973e9a711b9d2487`
(measurement receipts re-pinned at `1df2af73a79d038edf0b62ebc5691cb579ca3445`, receipts committed at
`36281d6989275c83bd20628c9df1a25bdd70e951`). Every git call was read-only with an explicit `-C`.
No tool was installed; pacman was not run.

Vocabulary used (the four values the seat spec allows): **improved | harmed | unchanged |
unprovable-but-better**. No numeric axis score is asserted here; the historical operability
observable is untouched (`SCORECARD.md:7` still reads `3`, unchanged since round 1).

---

## Trend verdicts

- **expansion: improved.** A new capability entered the lane's repertoire and its
  evidence is a committed, non-vacuous measurement rather than a prose claim.
  Evidence pointer: `corpus/evidence/round65/controls/c1-after.txt:25` —
  `CASES=20/20 C1=PASS`, `EXIT=0` (`c1-after.txt:1-2`, `REVISION=1df2af73…`), against the
  frozen before receipt `corpus/evidence/round65/controls/c1-before.txt:5` —
  `CASES=0/20 C1=FAIL missing-target`, `EXIT=1`. The target is not reachable by a do-nothing
  control: `corpus/evidence/round65/controls/c1-stubs-after.txt:5-6` records `always-pass:
  CASES=3/20 C1=FAIL (counter exit 1)` and `always-fail: CASES=17/20 C1=FAIL (counter exit 1)`,
  both `EXIT=1` (`c1-stubs-after.txt:2`). The capability is registered as a lane gate at
  `SKILL.md:159` (`receipt-pin`) and `SKILL.md:160` (`round65 claim counters`), and the
  capability row landed in the scorecard's capabilities table at `SCORECARD.md:3105`
  (`receipt-header consistency checking`, first-working round 65). The corpus surface grew
  correspondingly: `corpus/SOURCES.md:164-167` (rows S154-S157, three admitted and one
  rejected), `corpus/knowledge/receipt-identity-r65.md` (new entry, indexed at
  `corpus/README.md:1342`), `corpus/QUALITY.md:1014` (criterion 130) and `corpus/QUALITY.md:1016`
  (criterion 131), and `corpus/lessons/round-65.md` (Gate at `:6`, five Mistakes rows, routed
  items, wave-2 findings at `:64`). The summary of record is
  `corpus/evidence/round65/measurement-summary.json:22` and `:24`.

- **quality: improved (narrowly).** The corpus gained a sourced interpretation entry and a
  registered gate, and this round's own falsify wave found and fixed a real defect class rather
  than leaving it latent. Evidence pointer: `corpus/evidence/round65/measurement-summary.json:26`
  — `controls/l1-boundary-probes.txt` records `bad-revision-arg -> exit=2`, `absent-receipt ->
  exit=2 out=RECEIPT_PIN=ERROR receipt file unreadable`, `non-git-root -> exit=2
  out=RECEIPT_PIN=ERROR --root is not a git repository` and `git-missing -> exit=2
  out=RECEIPT_PIN=ERROR git is unavailable`, while receipt-content defects still exit 1
  (`zeropad`, `dotpath`, `blankbody`) — the exit taxonomy the frozen contract asked for
  (`corpus/evidence/round65/claims.md`, C1: "0 consistent,1 invalid,2 usage/environment") now
  holds; the defect that broke it was found by a wave seat (`corpus/lessons/round-65.md` Mistakes
  row, `corpus/lessons/round-65.md:26`, "The validator answered every environment fault with a
  receipt verdict (exit 1)") and the fix is recorded at `corpus/lessons/round-65.md:26` and
  registered in the gate row `SKILL.md:159`.
  Criterion 130 landed this round with a red-before and a named limit (`corpus/QUALITY.md:1014`),
  and criterion 131 landed as a new red-before covering the shape-only counter
  (`corpus/QUALITY.md:1016`). The narrowness is stated, not hidden, and bounds the credit:
  the C2 counter attests the entry's shape and not its substance — `corpus/evidence/round65/controls/c2-after.txt:5`
  reads `ENTRY_CHECKS=10/10 C2=PASS` (EXIT 0), but a boilerplate control also scores
  `ENTRY_CHECKS=10/10 C2=PASS` exit 0 (`corpus/evidence/round65/measurement-summary.json:29`), so
  that counter is not admitted as evidence of depth and the depth axis move rests on the
  re-opened sources and the source review instead. A fabricated body still passes the validator
  (`corpus/knowledge/receipt-identity-r65.md`, `## Limits`; `corpus/QUALITY.md:1014`).

- **discernment: unchanged.** The lane's own discrimination worked — the falsify wave caught
  the exit-taxonomy deviation and the shape-only counter, and the L1 re-opened every source
  rather than trusting the inherited bytes — but no outside non-author spot-check exists for
  this round, so no discernment upgrade is claimed. Evidence pointer: the round's own gate
  records the debt at `corpus/lessons/round-65.md:8` — "Outside non-author spot-check remains
  required; wave seats dispatched by this lane are still lane-authored evidence. Suggested
  sample: admit S155 and reject S157" — and the absence is confirmed in the tree: no
  `corpus/lessons/round-65-verifier-spotcheck.md` exists (the newest spot-check lesson in the
  lane is `corpus/lessons/round-64-verifier-spotcheck.md`, which covers round 64, not round 65).
  A fleet-root `.ufo/reports/round-65/chousa.md` does exist, but it is this lane's own report of
  its own round — author evidence, not an outside review, and it is not a spot-check lesson.
  Wave-1 (64 seats) and wave-2 (32 dispatched) are lane-dispatched, so every seat finding in
  this round is author evidence, including this one. An outside reviewer taking the suggested
  sample (admit S155, reject S157) is what would move this verdict.

---

## Notes for the integrator (not part of the section text)

1. **The section above is consistent with the scorecard's own committed trend line**
   (`SCORECARD.md:3095-3098`: "Trends: expansion improved (new capability row below); quality
   improved narrowly (sourced entry + registered gate, with the counter's shape-only limit
   stated); discernment unchanged (outside non-author spot-check still owed; wave seats are
   lane-authored evidence)"). The draft adds the committed-receipt pointers the scorecard
   line compresses, and keeps the shape-only bound visible.

2. **Two unfixed provenance defects sit in the committed corpus and bear on the "quality"
   verdict's evidence base.** They are recorded here rather than folded into the verdict, because
   neither changes the direction of the three trends; both are offered to L1 for repair. (Both are
   also raised independently by wave seat `R65C02`, findings D1 and D2.)

   a. **`corpus/lessons/round-65.md:33` claims a blob digest the receipts do not carry.** The
      line reads "New validator and revision/exit-bearing prefreeze controls; **final receipts
      also carry blob digest**." No receipt under `corpus/evidence/round65/controls/` carries a
      `SHA256=` header — `grep -c "SHA256="` returns `0` for `c1-after.txt`, `c2-after.txt`,
      `c1-stubs-after.txt`, `c1-before.txt` and `c2-before.txt` alike — and the lane's own
      validator refuses all of them:
      `python3 -B tools/receipt-pin.py --receipt corpus/evidence/round65/controls/c1-after.txt --root . --revision 1df2af73a79d038edf0b62ebc5691cb579ca3445`
      → `RECEIPT_PIN=FAIL SHA256 header must be 64 lowercase hex plus a relative path` (exit 1),
      the same output for `c2-after.txt` and `c1-stubs-after.txt`. (Wave seat `R65C02` finding D1
      raises the same defect independently.) Smallest correction: restate the clause as "final
      receipts carry revision and exit only".

   b. **`corpus/evidence/round65/measurement-summary.json:17` points at a digest that is recorded
      nowhere.** It reads `"tools/receipt-pin.py": "blob at 1df2af73 (see the commit; sha256
      recorded in the wave-2 seat reports)"`. Searching the wave-2 evidence for that digest
      returns nothing: `grep -rl "22b967ad\|7ac5aac" .ufo/waves/round-65/w2/` is empty. The
      actual digest is `git cat-file blob HEAD:tools/receipt-pin.py | sha256sum` →
      `22b967ad212a887959bb0d2d6bf4d63b617f8a45797f10042995033674723ce2` (blob
      `7ac5aac341e4a6b625341aeb5e5a1024c2330b00`). Smallest correction: record that digest in the
      summary's own `digests` block. (Wave seat `R65C02` finding D2 raises the earlier wording of
      the same line; the reworded line still points at an absent record.)

3. **One stale pointer in the scorecard's round-65 section, not in the trends.** `SCORECARD.md:3081`
   says "(`git diff f99de3b 0a851898` over `corpus/evidence/round65` instruments is empty)". The
   literal command `git diff --stat f99de3b 0a851898 -- corpus/evidence/round65` is **not** empty —
   it adds `corpus/evidence/round65/source-openings.json` (34 insertions). The instruments
   themselves are byte-unchanged: the same diff scoped to
   `corpus/evidence/round65/{c1-count.py,c2-count.py,claims.md,controls/}` prints nothing, and the
   blob ids match the freeze exactly (`c1-count.py` `f43bf9f582c99b89dd0632a73310e638ff8b9a83`,
   `c2-count.py` `2d642e72f05b96b0fad3dfef184bf0f9eecc8b3c`, `claims.md`
   `1ed2bda480a02de15209469b8bac483434089472` at both `f99de3b` and `HEAD`). Smallest correction:
   scope the parenthetical to the instruments, as `measurement-summary.json:15` already does
   ("c1-count.py, c2-count.py and claims.md are byte-identical to the freeze").

4. **Scope note on the falsify wave's reach.** Wave-2 dispatched 32 seats (`w2-dispatch.json`
   `counts.spawn = 32`); 29 have a committed top-level seat report, and the lesson records
   "32 seats dispatched, 29 reported, 3 released un-settled" (`corpus/lessons/round-65.md:64`).
   The three un-settled are `R65D01` (a partial draft only, committed at `62b0af1`), `R65S07`
   (no output at all) and this seat, `R65D03`, which had not settled when the lesson was
   written. This seat's draft is lane-authored evidence and is not an independent check on the
   lane; the discernment verdict above is written accordingly and claims nothing an outside
   reviewer would have to confirm.

5. **No scalar.** This section states no numeric axis score and moves none. `SCORECARD.md:7`
   (`| operability | 3 | …`) is unchanged, and the round-65 verdict's own claim row keeps the
   frozen "numeric score unchanged at the declared historical 3/10 per the frozen claim" wording.
