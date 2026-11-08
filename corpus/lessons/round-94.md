# Round 94 — the pins table learns what each row is, the punctuation quote gets a name, the tail set gets an owner (2026-11-08)

Base `0f3f84dab3a094ec0a2fe8ae9ae59d3326e1a9b6` (round-93 landing + its non-author spot-check, admitted).
Frozen claims in `.ufo/waves/round-94/claims.md` and `.ufo/waves/round-94/claims.json`. Plan and amendments:
`plans/round-94.md`. Three claims, three axes, no exploratory claim.

## Gate

Registry: one row added, `S221` (installed `git-clone(1)`, tier A, `--shared`), status `mined`,
`used-by: corpus/lessons/round-94.md`. No existing row's `status`, `recheck` or `used-by` cell changed;
`S001` and `S070` were re-opened and their cells are untouched. Census exit 0 before
(`corpus/evidence/round94/census-start.txt`) and after (`corpus/evidence/round94/census-end.txt`), 219 → 220
rows, the same five `W04` duplicate-url warnings.

GATE-RECORD S221 path=/usr/share/man/man1/git-clone.1.gz sha256=b3fd695ca3aeb5b315c0f87071972bfbebacc3cfaeb9a920075953dbded3802a opened=2026-11-08 words=10 quote=The resulting repository starts out without any object of its own

- **S221 admitted.** Decompressed `man1/git-clone.1` OPTIONS, `-s, --shared` body: "The resulting repository
  starts out without any object of its own." (10 words). It grounds C1's battery design: every fixture is a
  `git clone --shared` of the lane, so a fixture tree is never a self-contained archive and the lane's
  objects must outlive the battery. Tier A (the installed upstream manual page), scope limited to what a
  shared clone stores — not to Git's general safety.
- **S070 re-opened** (`sha256sum(1)`, tier A): sha256 `93c17dffe9f25d56291113d566a7de3ff65c29f8cc32c381801c49cf27e8403f`,
  unchanged from the row; line 11 still reads `Print or check SHA256 (256\-bit) checksums.` It grounds
  C1's digest discipline. Cells unchanged.
- **S001 re-opened** (`tools/research-gate.sh`, own-work, tier A): line 9010 still prints the selftest-verdict
  line C2/C3 read; `git diff --quiet 0f3f84da <landing> -- tools/` is empty (the tool is not touched this
  round). Cells unchanged.
- **Rejected this round:** no new candidate was refused; the registry's rejections from earlier rounds stand.

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| before-state asserted on bytes the prior counter refuses for an unrelated reason | the C1 first draft ran the r93 driver on the r94 three-column table; it exits `SETUP malformed pin row`, so the "prior accepts this defect" sentence would have compared two different instruments, not one defect. `corpus/evidence/round94/evidence-before/c1-prior-accepts.txt` now measures the defect on the r93 **two-column projection** of the same rows | the L1's own pre-freeze battery run (the first `forgeries-r94.py` shape), before any scoring | `forgeries-r94.py` writes both forms: the r94 table for the new driver and the re-digested two-column projection for the old one; `SCHEMA_PRIOR_ACCEPTED` keeps the do-nothing form measured every run |
| a leg that lives in one file, exercised by a battery that mirrors another round's path | first `curation-controls-r94.py` regression: `CASE_DEVIATION D1-duplicate-qid: NOT refused by both counters`, `CURATION_R90=SETUP missing …/round94/controls/legs.txt` (the r90 battery mirrors only the r93 leg table) | the same pre-freeze run, before the freeze | the alias shim writes the r94 leg table into the mirrored tree before invoking the counter; the regression line now requires `CONTROLS=PASS` as well as `FORGERY_REFUSED=7/7` |
| a count-only comparison leaves the new leg silent | `double-tail-215` first ran: the duplicated tally failed the multiset comparison, so no owner code fired and the owner leg was decorative for that class | the tally battery's own case list, before the freeze | `TAIL_OWNER_COUNT` added and bound by the `double-tail-215` case (was: the case bound `TAIL_OWNER_MISMATCH`, which never printed) |
