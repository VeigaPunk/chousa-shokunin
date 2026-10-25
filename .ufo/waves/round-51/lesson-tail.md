## Census

Command: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa`.

- **Round start** (`corpus/evidence/round51/census-start.txt`): exit 0, `ok`, five pre-existing W04 warnings (S051, S053, S073, S074, S075); 106 rows.
- **Round end:** @@CENSUS_END@@
- **Rows:** @@ROWS@@ (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`). Added by tier: A S107 S108 S109 S110 S112; B S111. Rows touched old → new: none.
- **Sourced claim:** C2 rests on S107–S112, all opened this round.
- **Mined mistakes:** eight, in `## Mistakes`; rows 1, 5, 6 and 8 each have a check shown able to fail (QUALITY 84, 86, the README correction check, QUALITY 85).

## Disclosed post-freeze changes

All outside the frozen predicates, counters and targets; the frozen counters are unchanged after the freeze commit except E1.

- **E1** (before any seat existed): the C3 tokenizer stopped stripping a leading dot; before-state 8 → 5 (`claims-erratum.md`).
- **E2** the frozen C1 counter can hang when its first two id draws collide (1/401 per run); not changed — `c1-supplement.py` draws distinct ids and runs the frozen counter only with a seed that does not collide.
- **E3** the frozen C1 counter inherits an ambient `ASSIMILATE_CITES`; not changed — the supplement removes the variable from the tool's environment; run the frozen counter as `env -u ASSIMILATE_CITES python3 …`.
- **E4** the round-50 echo and const controls delegated to the lane tool; the round-51 copies delegate to `controls/tool-before.py` (a control pins its base, QUALITY 85); the before receipts were produced at the base, where the two were the same tool.
- **Tool v2** (`tools/assimilate-rows.py` after the W1 `R51ReviewAdopterCode` review, commit `cf642c66`): per-entry substitution and citation (F1), the id right after `source:` on header lines only (F3), refusal of a `source:` id that is neither staged nor a Registry row (F4); `corpus/fixtures/assimilate-selftest/` extended (a no-space `source:` line, a cross-entry body mention, a tail id) — digest `3b7ad258…`, 27 findings. Not fixed, named: the twin-id `held` label and the refusal ordering (F5, F6).
- **E5** `controls/build-c3-controls.py` changed after the freeze: the three negative controls start from the BASE `SCORECARD.md`/`SHONEN.md` and a DOTPATH positive control was added (`controls/c3-controls-final.txt`; `c3-controls.txt` and `c3-controls-erratum.txt` stay as filed). Also post-freeze: `c1-supplement.py` (ten legs, random directory and entry names), `receipt-check.py` (at least one receipt; `--skill` reads the Gates table), tool v3 (the W2 `R51W2ReviewToolV2` N1–N5 fixes: own-work vs staged `source:` id by URL, stale outputs cleared on every entry run, header ends at `#### Observation|Inference|Unknown`, fenced examples skipped, a body token equal to a minted id flagged; the dead minted-id refusal removed), and the entries, registry row S107 and README blocks narrowed after W2 (Mistakes row 9).
- **Not done:** the W1 `R51ExecCaptureForm` zip-member form and the `MutAdopter` survivors MUT04 and MUT06 (no real behaviour differs: registry identity already uses the escaped-pipe splitter, and the outside-row check refuses a registry with no heading and rows).
