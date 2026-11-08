# Round 93 — the pins table is the population, the whitespace quote has a name, and the historical tallies are derived (2026-11-08)

Base `206226dc9d9baef620e7d3d30bdac5f9194a459f` (round-92 landing + its non-author spot-check, admitted). Frozen
claims in `.ufo/waves/round-93/claims.md` and `.ufo/waves/round-93/claims.json`.
Freeze F6 `3789608dc8c0eded67f1e5d3840caf0a27522a88` (instruments, expectations, leg table, claims, pins);
carrier C7 `9d03318527f8fe734e67d24f64ac5dce192d43fc` (the six committed scored receipts plus the 23-row pins
table). Three earlier pairs — F `84998563` (never carried), F2 `b7241252`/C2 `754b62fb` (the pair the wave
attacked) and F3 `d5c19c54`/C4 `94fbf892`, F4 `596eabc9`/C5 `881a541f`, F5 `1362f4b2`/C6 `c1ebb1d9` — were cut
or superseded as the wave's findings landed; each defect is a row below. `corpus/evidence/round93/amendments.md`
records every amendment.
One v1 wave, 12 seats: see §Wave settlement.

## Gate

No registry row was written and no new source was opened this round; the sourced-claim duty is satisfied by the
S070 re-open and the S001 rev-form record below. No `status`, `recheck` or `used-by` cell changed (the registry is
byte-identical to round 92's: `git diff 206226dc b7241252 -- corpus/SOURCES.md` empty), which is why the earlier
plan sentence "move S001's `recheck` cell round 92 → round 93" was withdrawn: S001's recheck cell is a cadence
(`on-release`), not a round counter. Census exit 0 before and after
(`corpus/evidence/round93/census-start.txt`, `census-end.txt`), 219 rows, same five `W04` warnings.

GATE-RECORD S001 rev=b7241252c2358613d3b22b7d0454d98c56dab373 path=tools/research-gate.sh line=9010 words=4 quote=RESEARCH_GATE_SELFTEST: PASS (%d cases%s)

- **S073 correction noted** (`corpus/SOURCES.md:83`): S070's `SYNOPSIS` anchor label is the one S073 exists to
  correct (the `-c, --check` entry is a DESCRIPTION `.TP` item, not a SYNOPSIS line); the re-open below cites
  the digest text at line 11, which S070's own `teaches` cell states correctly, and quotes the literal roff
  form (`256\-bit`).
- **S070 re-opened** (`sha256sum(1)`, tier A, the installed page): `/usr/share/man/man1/sha256sum.1.gz`, sha256
  `93c17dffe9f25d56291113d566a7de3ff65c29f8cc32c381801c49cf27e8403f` — identical to the row's recorded sha;
  re-opened locally 2026-11-08. Decompressed line 11 is `Print or check SHA256 (256\-bit) checksums.` (rendered:
  "Print or check SHA256 (256-bit) checksums.", 7 words). It grounds C1's digest rule and its minus-self
  self-pin: the page says the tool prints or checks a digest, which is what the pin walk does with committed
  bytes. The S070 row's own cells are unchanged.
- **S001 re-opened** (`tools/research-gate.sh`, own-work, tier A): line 9010 PRINTS the one selftest-verdict line
  the C3 case-count leg depends on; the record above verifies at F2, and the tool is byte-identical at base,
  F2 and the landing (`git diff --quiet 206226dc <landing> -- tools/`).

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| a before-state asserted instead of measured | claims C2's first draft said the r92 counter "verifies `CURATION_R92=PASS`" on the whitespace-quote tree; the first actual run printed `CURATION_R92=FAIL` (downstream `LEG_FAIL FLOOR/WARRANT/TFREQ`, `Q_SHAPE_FAIL=0`) — `corpus/evidence/round93/evidence-before/c2-prior-accepts.txt` | the L1's own pre-freeze measurement, before any scoring | the claim was re-frozen as a CLASSIFICATION claim (r92 cannot name the class; r93 refuses it at the shape leg as `quote=<whitespace>` with `Q_WSQUOT=1`), and the controls battery re-derives the distinction every run via `WS_SHAPE_GREEN_R92=1/1` — a value that fails if r92's shape test ever names the class |
| the pins table's self row and row containment were unguarded | `R93ReviewerC1` H2/M1: deleting the self row (21/21) or adding a row for `/etc/hostname` still printed `CONTROL_DRIVER_R93=PASS`; the denominator moved with the deletion | the wave's own reviewer, replicating the frozen command | `PIN_SELF_ROW_ABSENT` and `PIN_ROW_OUTSIDE` wired (F5); both classes re-measured as `REGRESSION_REFUSED=2/2` in `after/c1-forgeries.txt` |
| a leg vocabulary that lived in the counter | `R93ExecMutations` M8: deleting the WSQUOTE leg **and** lowering `EXPECTED_LEGS` to 14 still printed PASS, and M7's stubbed population printed the same `CONTROLS=PASS` line | the wave's mutation seat, then `R93CriticClaims` C2 | the vocabulary is `controls/legs.txt`, a committed and pinned side table (`LEG_FAIL LEGSET`), and the controls bind `Q_WSQUOT=1` + `LEG_FAIL WSQUOTE` on both whitespace trees (F6); stub probe `after/c2-m7-stub.txt` |
| a scope claim wider than the code | `R93ReviewerC3` F2/F3: "tallies outside the scope are enumerated" held only for the tail, and the case-range leg checked endpoints of one family only — a head tally and an interior hole both stayed green | the wave's own reviewer | `HEAD_DECLARED={}` + `HIST_SCOPE_BLEED head`, index-set equality for both families over every `ok-case` line, and the `HEAD_REFUSED`/`INTERIOR_REFUSED` controls (F4) |
| a harness pair cut before its own legs could run | F/`84998563`: `self_pin` took the pin dict where the pins path belonged (TypeError at runtime), and the first forgery battery extracted `git archive` trees, where the fresh legs that call `git -C @ROOT@ show` cannot run (`FRESH_OK=4/6`, `CONTROL_DRIVER_R93=FAIL`) | the L1's own verify and battery run before the wave (`bg_22332` output in the round report) | F2 re-cut before any settled scoring with the signature fixed; the battery switched to `git clone --shared` trees per forgery; the defect pair is named in the report as Amendment 1 |
