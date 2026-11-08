# Round 93 — amendments published before filing

The frozen predicate set (`.ufo/waves/round-93/claims.md`, `.ufo/waves/round-93/claims.json`) is the file the
wave attacked at `F2/C2`. It is **not** rewritten after scoring: its pinned bytes stay at F4
(`596eabc9`). This file records every sentence that the wave or the L1's own re-measurement falsified, with
the correction now carried by the landing instruments. Read it with the claims.

## Amendment 1 — the F/`84998563` pair was cut before its own legs ran (harness defect, no scoring)

`self_pin` took the pin dict where the pins path belonged (runtime TypeError), so `verify` could never pass
at F. The first forgery battery also extracted `git archive` trees, where the fresh legs that call
`git -C @ROOT@ show` cannot run (`FRESH_OK=4/6`). Both fixed before any settled scoring; F2/C2 replaced F.
Receipt: `bg_22332`/`bg_22446` output, quoted in the round report §Work performed.

## Amendment 2 — C1 Before: "pins no receipt" holds in the tree-only form

`R93RevPrior` found that the r92 driver's `self_pin` *does* bind a receipt's bytes when `--repo` and
`--receipts-rev` are supplied — but only to a revision, never to the pins table, and the default `verify`
form has no `--repo`. The frozen Before sentence stays as written; the battery measures the tree-only form and
the claim's named limit (5) now says exactly that.

## Amendment 3 — C1: the driver resolves its own bytes against `--repo`

`R93ExecC1Repro`/`bg_22624` measured that `rel_for(root, __file__)` calls the dispatch form
`--root <clone>` a setup escape on correct bytes. The driver now resolves `__file__` against `--repo`; the
`DERIVE_OK` class in the battery measures the remaining difference (r92 refuses, r93 does not).

## Amendment 4 — C2: `Q_WSQUOT` is a pre-resolution count, and the leg is a second witness

`R93ReviewerC2` F3/F4: the named limit said an unresolvable-source whitespace quote is "reported by FLOOR
instead"; the code counts it before resolution (so it is counted *and* FLOOR fails), and the leg's expression
is the same one the shape branch uses, so its own verdict force is the `EXPECTED_LEGS` arity check. Both
sentences are now as the code behaves; `LEG_FAIL ARITY` was added so that cause is named (its F5).

## Amendment 5 — C2: `DETECTOR_WITNESS` 11 → 13

`R93ReviewerC2` F6: `witness()` did not cover the new class. It now has two WSQUOTE rows, so the landing
counter prints `DETECTOR_WITNESS=13/13`. The frozen After sentence said 11/11 at C2; the landing number is a
strengthening, measured after the fix, not a narrowed target.

## Amendment 6 — C2: `claims.json`'s C2 controls predicate named tokens no instrument prints

`R93ReviewerC2` F1/F2: the machine form asked for `FORGERY_REFUSED=4/4`/`PRIOR_ACCEPTED=4/4` and a K2 that
r92's own refusals trigger. The machine form is corrected at F4: it now names the printed
`CARRIED_REFUSED_BOTH`/`WS_NAMED`/`WS_SHAPE_GREEN_R92`/`PRIOR_REGRESSION` tokens and a K2 that says what the
classification claim can actually discriminate.

## Amendment 7 — C3: tallies above `## Gates` were invisible; the claim said otherwise

`R93ReviewerC3` F2: only the tail was scanned. The counter now declares the head empty (`HEAD_DECLARED = {}`)
and fires `HIST_SCOPE_BLEED head …`, with a control case (`HEAD_REFUSED=1/1`) that r92 accepts.

## Amendment 8 — C3: the case-range leg was endpoint-only and blind to the no-`exit=` names

`R93ReviewerC3` F3: an interior hole and a renamed `accepted=` case both stayed green. The leg now requires the
claimed range to be exactly the family's index set for both families, over every `ok-case` line; the control
case `INTERIOR_REFUSED=1/1` fails r92 and passes r93.

## Amendment 9 — C3: the machine form asked for `TAIL_REFUSED=1/1`

`R93ReviewerC3` F1: the instrument prints `TAIL_REFUSED=2/2`. The machine form is corrected at F4 and the
printed token set is the one the counter emits.

## Amendment 10 — citation precision on the source rows (report-level, frozen file unchanged)

`R93ScoutSources` F1: S070's anchor label lives in a row (S073) that exists to correct it, and the quote is the
rendered rather than the literal roff form. The report's Sources & frontier section cites both rows and the
literal form (`Print or check SHA256 (256\-bit) checksums.`); the S070/S001 re-open artifacts land in
`corpus/lessons/round-93.md` `## Gate` (untracked at C2, committed at the landing). The scout's note that
S001 states no leg-vocabulary rule is accepted: C2 rests on the lane's own contract, and S001 grounds only the
one verdict line the tally counter reads.

## Amendment 11 — the plan's `recheck` sentence is withdrawn

`R93ScoutSources` C3: S001's recheck cell has read `on-release` in every commit that touched the registry; it
never held a round number. No registry cell changes this round (registry byte-identical to base).

## Amendment 12 — the pin population is 23 rows, not 22

Killing `R93ExecMutations` M8 (delete the WSQUOTE leg **and** lower `EXPECTED_LEGS`) needed the leg
vocabulary to live outside the counter: `corpus/evidence/round93/controls/legs.txt`, one name per line, is now
a pinned instrument (F6). The pins table therefore holds 23 rows, and the landing verify prints
`PINNED_FILES=23/23`. The frozen C1 sentence names `22/22`, which was true between F5 and F6 only; the landing
number is re-measured in `after/c1-verify.txt`. `DETECTOR_WITNESS` moved 11 → 13 the same way (Amendment 5).
