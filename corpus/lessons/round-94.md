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

GATE-RECORD S001 rev=4cbaed6cc15f4cd1008b6ab6294ffe6894f3dfec path=tools/research-gate.sh line=9010 words=4 quote=RESEARCH_GATE_SELFTEST: PASS (%d cases%s)

- **S221 admitted.** Decompressed `man1/git-clone.1` OPTIONS, `-s, --shared` body: "The resulting repository
  starts out without any object of its own." (11 whitespace tokens; re-counted by `R94ScoutSources`, whose
  finding F2 also established that this row cannot carry a `GATE-RECORD` — the lane's three documented forms are
  url/admit, url/unreach and rev, and an installed local page with no fetch and no repo blob fits none. The
  per-row Gate record below is prose, exactly as S070's was in round 92; the record line above grounds S001,
  and `tools/gate-records.py verify` on this file is the gate.) It grounds C1's battery design: every fixture is a
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
- **Post-wave note (Gate):** `R94ScoutSources` F2 measured that the first S221 record line was a form
  `tools/gate-records.py` does not implement (`path=`/`sha256=`/`words=` with no `rev`/`url`); the record now is
  the S001 rev-form at F3 `ebbcbe39`, `gate-records.py verify` prints `records=1 ok=1 fail=0` (rc 0), and the
  S221 row itself keeps a prose Gate record exactly as S070's does. Every claim's final measurement is at F3
  `ebbcbe39` / C3 `d13c2ff2`, receipts `corpus/evidence/round94/after/*.txt`.

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| before-state asserted on bytes the prior counter refuses for an unrelated reason | the C1 first draft ran the r93 driver on the r94 three-column table; it exits `SETUP malformed pin row`, so the "prior accepts this defect" sentence would have compared two different instruments, not one defect. `corpus/evidence/round94/evidence-before/c1-prior-accepts.txt` now measures the defect on the r93 **two-column projection** of the same rows | the L1's own pre-freeze battery run (the first `forgeries-r94.py` shape), before any scoring | `forgeries-r94.py` writes both forms: the r94 table for the new driver and the re-digested two-column projection for the old one; `SCHEMA_PRIOR_ACCEPTED` keeps the do-nothing form measured every run |
| a leg that lives in one file, exercised by a battery that mirrors another round's path | first `curation-controls-r94.py` regression: `CASE_DEVIATION D1-duplicate-qid: NOT refused by both counters`, `CURATION_R90=SETUP missing …/round94/controls/legs.txt` (the r90 battery mirrors only the r93 leg table) | the same pre-freeze run, before the freeze | the alias shim writes the r94 leg table into the mirrored tree before invoking the counter; the regression line now requires `CONTROLS=PASS` as well as `FORGERY_REFUSED=7/7` |
| a count-only comparison leaves the new leg silent | `double-tail-215` first ran: the duplicated tally failed the multiset comparison, so no owner code fired and the owner leg was decorative for that class | the tally battery's own case list, before the freeze | `TAIL_OWNER_COUNT` added and bound by the `double-tail-215` case (was: the case bound `TAIL_OWNER_MISMATCH`, which never printed) |
| a control case overwrote the input it then asserted on | `forgeries-r94.py`'s `s1-schema-two-column` wrote the valid three-column table and then demanded `SETUP PIN_SCHEMA` from it, so `FORGERIES=PASS` was unreachable on every tree the driver accepts; five independent seats at C reported it while every integer token stayed green | the wave's own executors/reviewers/scout/sentinel/mutation seats (the case's own summary counter read a different case, which is why it was invisible to the token list) | `s1` dropped at F2 and the do-nothing measurement kept in `s0-schema-prior`; the lesson's rule: a case must build its fixture from the pristine table and mutate one dimension, and the battery summary must be checked against the case list, not only against its counters |
| a class test narrower than the sentence it carries | the punctuation class was ASCII-only (`[A-Za-z0-9]`) while the sentence said "no alphanumeric character", so a CJK quote was refused as punctuation | `R94ReviewerC2` F2 before the landing | `any(ch.isalnum() for ch in inner)`, witness row `punct-cjk-silent`, control `x3-cjk-quote` (a CJK quote must be refused downstream, never as the class) |
| a convenience script resolved the lane root one level too high | `scripts/measure-all-r94.sh` first run (`LANE=$(cd "$(dirname "$0")/../.." && pwd)`) wrote the six scored receipts to `/home/vgpnk/Projects/shokunin/corpus/evidence/round94/after/` — the fleet root — and reported `rc=2` for every command; `git ls-files corpus` at the fleet root is empty, so nothing tracked was touched, and the six files were mine | the run's own output paths, read before trusting them | `LANE=$(cd "$(dirname "$0")/.." && pwd)`; the six stray files were deleted from the fleet root (the one fleet-root deletion this lane may make), and the re-run writes into the lane |
