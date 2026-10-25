# CriticC2Calibration — attack on the C2 disposition claim (round 40, w1)

**Assigned attack.** Test whether the four C2 statuses in `corpus/evidence/round40/c2-count.py`
measure source-to-self-assessment mismatches, or merely count prose labels; supply a
falsifying case if possible.

**Verdict: FALSIFIED.** The counter passes `R39_CALIBRATION_DISPOSITIONS=4/4`, exit 0, on
planted prose labels alone. The frozen claim (`corpus/evidence/round40/claims.md:23`) states
"the counter must re-derive these states from the committed evidence, not count prose labels
alone." It counts prose labels alone for R2 and R5 outright, and for R3/R4 it conjoins a real
artifact check with substring presence whose required strings were authored in the same commit
(`d164f88`) as the disposition record — so no status compares a self-assessment against a
source the assessee did not control.

## Exact commands and observed output

Real lane repo (clean worktree, verified `git status --porcelain` empty on the C2 inputs):

```
$ python3 corpus/evidence/round40/c2-count.py
R2_DISPOSITION=ok
R3_DISPOSITION=ok
R4_DISPOSITION=ok
R5_DISPOSITION=ok
R39_CALIBRATION_DISPOSITIONS=4/4   (exit 0)
```

Falsifying simulation — scratch clone `/tmp/c2fleet/chousa-shokunin` (fleet layout replicated,
real repo untouched). Three mutations, all in **uncommitted worktree bytes**:

1. `corpus/evidence/round39/claims.md` erratum replaced by a decoy paragraph that states it
   "resolves nothing," carrying only the literals `29 → 31`, `50 → 52`,
   `c1-mutenv-s39003.json`, `superseded`, `R2`, `R3`.
2. `SCORECARD.md` round-40 correction section deleted — the live wrong phrase
   "two independent runners" (line 2234) retained — plus an unrelated line "the garden held
   two seeds."
3. `routed-defect-dispositions.json` reduced to bare `status` labels with `evidence` pointing
   at `nonexistent-file-xyz`.

```
$ python3 corpus/evidence/round40/c2-count.py
R2_DISPOSITION=ok
R3_DISPOSITION=ok
R4_DISPOSITION=ok
R5_DISPOSITION=ok
R39_CALIBRATION_DISPOSITIONS=4/4   (exit 0)
```

Every disposition "ok" while its decision asserts nothing, its evidence resolves to nothing,
and — for R5 — the defect is still live in the scorecard. Labels plus plantable literals are
both necessary and sufficient; the status fields are the only thing in `dispositions.json`
the counter reads (the `evidence` and `decision` keys are never opened).

## Per-status breakdown: what each check actually measures

- **R2** (`c2-count.py:60-64`): genuine conjuncts = `git ls-files` tracking + `is_file()` of
  the receipt. Everything else is substring co-occurrence: `"not committed" in lesson`,
  `"R2"`, receipt path, `"superseded"` anywhere in claims39. `"not committed"` is frozen r39
  text (`lessons/round-39.md:27`); the claims-side strings exist only because commit
  `d164f88` (which also created the dispositions file) appended them — self-assessment
  compared to self-authored prose.
- **R3** (`66-70`): `md_count(BASE39)/md_count(TIP39)` genuinely re-derives `(50, 52)` from
  pinned git revisions — the strongest check in the file. But the "mismatch" pairing is
  substring presence of `"29 → 31"` in report and claims39, and `"50 → 52"` in claims39;
  co-occurrence, not linkage. The decoy paragraph satisfies all of it.
- **R4** (`72-79`): real cross-source measurement — spec `items[].role` and plan
  `tasks[].agent` histograms recomputed and equated (verified independently: both are
  executor 6 / reviewer 6 / critic 5 / scout 3 / scribe 3 / mutation-tester 3 / sentinel 2 /
  revenger 2 / connector 1 / simplifier 1 = 32 rows, 0 missing keys), report substring, and
  the spot-check's contrary `"reviewer 8 / revenger 0"` (spotcheck line 74) still cited. This
  is the only status where the artifact evidence is independent of the disposition author.
  Residual weakness: substring `"revenger 2"` also matches "revenger 20"; histogram equality
  is not per-seat agreement (a seat-permuting spec/plan pair still passes); and the check
  still ANDs the artifact truth with a hand-written `"not-reproduced"` label rather than
  deriving the status.
- **R5** (`81-84`): pure label counting. `"two independent runners" in scorecard` *requires
  the uncorrected defect phrase to remain present*; `"two seeds" in scorecard` is satisfied by
  any co-located string (my garden sentence). `"R5" in scorecard` is satisfied by a
  pre-existing unrelated line (`R5 selftest cases`, r39-era line 2054). Only
  `"L1's construction runs" in claims` is genuine frozen r39 text (claims39:5, added in
  r39 commit `6d914e9`). No correction is verified — non-resolution passes.

## Secondary defect: "committed evidence" is not committed

Claim P2 says states are re-derived "from the committed evidence." Only `md_count` reads
pinned revisions (`git ls-tree BASE39/TIP39`). Every other input — claims39, lesson39,
scorecard, spotcheck, spec, plan, and the fleet `REPORT39` — is a working-tree `read_text`.
The counter validated uncommitted dirty bytes in the sim: `git ls-files --error-unmatch`
passes on tracked-but-modified files, so a dirty-tree rerun of P2 reports `4/4` on states
that were never committed. The real repo happens to be clean today; nothing enforces it.

## Impacted axes

- **Calibration (primary):** the axis measured by C2 is hollow for R2/R5 and label-bound for
  R3/R4. `4/4` is attainable, and was attained in simulation, with zero dispositions
  performed — direct falsification of the claim's "not count prose labels alone" clause.
- **Operability (secondary):** the counter runs cleanly and prints `4/4` exit 0 — fully
  operable while semantically empty, which hides the calibration defect behind a green count.
- **Depth (mixed):** R4's histogram recomputation and R3's pinned-revision counts are real
  re-derivation; the rest is grep-depth. The claim's own wording promises more than the
  counter delivers.

## Smallest safe correction

1. Pin all textual inputs to committed revisions (`git show <rev>:<path>`) or a frozen
   content hash; error on dirty tracked inputs.
2. Resolve each `evidence` pointer in `routed-defect-dispositions.json` to a tracked file and
   verify the cited line/range contains the claimed value (fail R2's evidence
   `nonexistent-file-xyz`, fail `SCORECARD.md:## Round 40 …` if the section is absent).
3. For R5, bind proximity: require "two seeds" within the round-40 correction block (or after
   the R5 marker), not anywhere in the file — and drop the requirement that the wrong phrase
   persist.
4. For R3/R2, require the literals to occur in a line/block also containing the defect marker
   (`R2`/`R3`), defeating co-occurrence planting.
5. For R4, use exact token comparison (`== "revenger 2"` on a parsed field, or regex
   `\brevenger 2\b`) and compare per-seat assignments if seat-level agreement is what the
   claim means.

Each fix is independent; (1)+(2) alone would have failed the decoy at R2/R5 immediately.

## Notes

- No production files modified. Simulation lived at `/tmp/c2fleet/` (outside the lane repo,
  scratch only; may be discarded).
- No tools installed or updated; `python3`/`git`/`grep` suffice (pacman paused per contract).
- Fleet report `.ufo/reports/round-39/chousa.md` read at committed r39-era content; the
  counter reads its live worktree path — flagged above.

Report: .ufo/waves/round-40/w1/CriticC2Calibration.md
