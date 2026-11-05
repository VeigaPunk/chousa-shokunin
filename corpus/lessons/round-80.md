# Round 80 — the scored set stops being a committed table, and a Gate record becomes a line a counter re-opens

Lane `chousa`. Base revision `b7803829922770b890e9f4efdd30d12c3695439a` (round-79 tip, closed
`ok` / `rejected-honest-stop` by the non-author spot-check `corpus/lessons/round-79-verifier-spotcheck.md`).
Claims frozen in `corpus/evidence/round80/claims.md`; the freeze evidence is the wave-spec commit
`0d253c95732c0ed19a9fa414e5d17769ddefa48d`, whose parent `0f59b985933b2fe9b0b6a754d908ac6ae47399e6`
carries the instruments, the claims text and the two do-nothing controls (see `## Mistakes`, row 1:
the preservation commit landed all three together, so this round's controls-before-freeze ordering is
shown by commit order only, not by separate commits).

Two claims, two axes, causally separable. C1 operability (lowest scored non-retired axis, the
historical 3/10 held) changes the battery: the scored subject set is drawn per run. C2 calibration
changes the gate record: a `GATE-RECORD` line is re-opened by a counter that reads committed bytes
at a named revision.

## Gate

```
GATE-RECORD S199 rev=b7803829922770b890e9f4efdd30d12c3695439a path=corpus/lessons/round-79-verifier-spotcheck.md line=222 words=12 quote=the battery is fully forgeable through the payload channel on **both** batteries
GATE-RECORD S200 rev=b7803829922770b890e9f4efdd30d12c3695439a path=corpus/QUALITY.md line=1056 words=20 quote=A subject-identity salt is defeated by any normalizer that knows its marker family, so the closure is a per-channel measurement
GATE-RECORD S201 rev=b7803829922770b890e9f4efdd30d12c3695439a path=corpus/QUALITY.md line=1054 words=25 quote=A self-assessment counter validates each resolution line against the bytes it claims to repair, and its audit window covers every block rather than the newest.
GATE-RECORD S202 rev=3eb4a3cad8febf75698a017cb6c4441f763b3454 path=.ufo/waves/round-78/w1/R78ReviewB/atkB2-new-block-window.txt line=11 words=2 quote=SELFCHECK=PASS unresolved=0/3
```

- Admit S199, own-work B, scoped to whether an outer battery's PASS line is reachable without
  scoring a subject. `corpus/lessons/round-79-verifier-spotcheck.md` at
  `b7803829922770b890e9f4efdd30d12c3695439a`, line 222, quote inside its operability row. Opened
  2026-11-04. Located quote: "the battery is fully forgeable through the payload channel on
  **both** batteries" (12 words, `wc -w`). Grounds C1's target: the scored set must be drawn fresh
  per run, because a committed subject set is a table any decoder can read.
- Admit S200, own-work B, `supersedes S196 —`. `corpus/QUALITY.md` at
  `b7803829922770b890e9f4efdd30d12c3695439a`, criterion 147 at line 1056. Opened 2026-11-04.
  Located quote: "A subject-identity salt is defeated by any normalizer that knows its marker
  family, so the closure is a per-channel measurement" (20 words). The round-79 lesson quoted 25
  words of this sentence while `wc -w` prints 27 (the spot-check's finding); the superseding row
  states 20 words, measured.
- Admit S201, own-work B, `supersedes S197 —`. `corpus/QUALITY.md` at
  `b7803829922770b890e9f4efdd30d12c3695439a`, criterion 146 at line 1054. Opened 2026-11-04.
  Located quote: "A self-assessment counter validates each resolution line against the bytes it
  claims to repair, and its audit window covers every block rather than the newest." (25 words,
  measured); the round-79 lesson stated 24, off by one.
- Reject S202, own-work C, `supersedes S198 —`. `.ufo/waves/round-78/w1/R78ReviewB/atkB2-new-block-window.txt`
  at `3eb4a3cad8febf75698a017cb6c4441f763b3454`, lines 1–11 (the file is eleven lines; the round-79
  row said "lines 1-20"), quote on line 11. Opened 2026-11-04. Located quote:
  `SELFCHECK=PASS unresolved=0/3` (2 words). REJECTED, reason unchanged from S198: a receipt that
  prints one counter's false green is that counter's own evidence, not a source about how
  self-assessment should be audited (the S195 class one layer out). Flip: admit scoped to what a
  control receipt must carry if an admitted entry ever rests on receipt format.
- Record correction, old→new: S196 (`25 words` stated, 27 measured) → S200 (`20 words` measured);
  S197 (`24 words` stated, 25 measured) → S201 (`25 words` measured); S198 (`lines 1-20`, quote
  absent from the file) → S202 (`lines 1-11`, quote located on line 11). The superseded rows stay in
  the registry with their bytes untouched (append-only, `CORPUS.md` rule 2); no `status`, `recheck`
  or `used-by` cell of an existing row changed this round.
- No URL was opened or fetched: all four rows are revision-pinned committed paths, opened by
  `git show <rev>:<path>`.
- Non-author spot-check requested: three admits and one reject above. Dispatched wave seats are
  author-lane evidence, not independent admission or promotion reviewers.
- Assimilation: none. The `merge/chousa/` package stays closed (round 78 measured 111 of 114 staged
  ids colliding with the live registry; the id drift is not renumbered in scratch). No package
  bytes read into the lane, no campaign tool run, no shokuknow write.
- `considerthese/` was opened (`2026-10-26.md` is the newest); nothing was implemented this round —
  the claim cap went to C1/C2 and the file's live proposals are recorded in the wave's scribe draft,
  not adopted.
