# ScribeIndexRows — round 25 (seat ChousaR25Recovery.ScribeIndexRows-3)

Lane `/home/vgpnk/Projects/shokunin/chousa-shokunin`, claim base d730ae4. Read-only: no lane file written, no gate run, no clone. Observations are marked (obs); drafts are marked (draft).

## 1. Re-derived counts (obs)

- `ls corpus/knowledge/*.md | wc -l` → **28** (matches the round-24 correction).
- `ls corpus/lessons/*.md | wc -l` → **13** (round-24 correction says 12). The 13th is `lessons/round-24-verifier-spotcheck.md` (mtime 2026-10-19 19:17; `git ls-files` lists it as tracked). It is in neither the coverage map (0 backtick-row hits in `corpus/README.md`) nor the frozen base list in `evidence/round25-measure.sh` POP2.
- Total entries: **41** (28 + 13). Round-24 correction said 40.
- Coverage-map rows present: knowledge **27/28** (unindexed: `knowledge/audit-r11.md`); lessons **11/13** (unindexed: `lessons/2026-10-19-hardlink-alias-boundary.md`, `lessons/round-24-verifier-spotcheck.md`). The "1 hit" for audit-r11 and the hardlink lesson comes only from the round-24 correction text, not from a row.
- Freshness gap for the claim-2 prediction: the measure script's base list has 12 lessons, so `STALE_INDEX_ITEMS=0` at landing holds only if the spot-check row below also lands. Otherwise the landing run reads 0 while one entry stays unindexed. Owner: measure/landing (ChousaR25Recovery.FrontierR11-3 / integration).

## 2. Draft coverage-map rows (draft; house style of `corpus/README.md` `## Coverage map`; insert before the `SOURCES.md` row)

```
| `knowledge/audit-r11.md` | Round-11 capstone audit, a dated snapshot (2026-10-16, HEAD `44cbad6`): findings A1–A28 with verdicts and pins, defects D1–D5 with dispositions, the final debt register, SHONEN readiness ("NOT promotion-eligible"). Pins are as-of that date: gate `46f5ddb3…` is superseded (`752e4e38…` at base); ledger `3845709b…` is superseded by the `hardening-r10.md` §6 revisions (latest 71 / 38·21·10·0·3 / queue 24); F1 closed by the errata at `:312-344` | `knowledge/audit-r11.md` `:299-344` (pins, errata); `knowledge/hardening-r10.md` §6 `:411-600`; `corpus/evidence/round25-measure-before.log` (claim 3 ledger tuple) |
| `lessons/2026-10-19-hardlink-alias-boundary.md` | Round-13 lesson: the hardlink-alias boundary — one `stat -c '%s %h'` probe serves the r12 size cap and the r13 alias check; refuse-on-count chosen over partner enumeration (both enumeration designs BLOCKed as unsound); carry-forwards named (TOCTOU, same-device bind mounts, unmeasurable stat, battery copies must run from inside `tools/`). Gate `6b17e50c…` is the r13 gate, superseded at r14 by `d8bbd0bf…` (hardening-r10 `:514`) | `evidence/alias-r13-20261019T123621Z-{selftest,bypass-before,bypass-after,battery}.log` (selftest `PASS (102 cases)`); `knowledge/hardlink-alias-r13.md`; `knowledge/hardening-r10.md` §6 Round-13 addendum `:470-490` |
| `lessons/round-24-verifier-spotcheck.md` | Outside check on round 24, written by the integrator (not lane-owned): spot-check of admits and rejects (reviewer sampled 4 admits, 4/4 agree; 3 rejects, 3/3 agree), ADMITTED with erratum `095b90c`; named debts: concurrent-append blank-line residual, citation-chain recheck needs the fleet root as `--root`, lesson template should carry a spot-check slot | `lessons/round-24.md`; `knowledge/citation-chain-fidelity-r24.md` (erratum `095b90c`); fleet `.ufo/waves/kaika-w3/chousa-review.md`, `chousa-critic.md` (cited by the file) |
```

Round-25 new files (templates; fill every field with an observed value at landing, never with the prediction):

```
| `knowledge/metadata-screen-r25.md` | Round-25 note: the `verify-metadata` mode (spec v1 as landed: header region, `source:`/`verified-at:`/`recheck:` key grammar, the `META_*` finding set, `METADATA_COMPLETE=N/M`); observed frozen-population result [fill]; named limits (not composed into `verify-all`; `--root ..` root-dependency info) | `evidence/round25-claims.md` claim 1; `evidence/round25-measure.sh` POP1; `evidence/round25-measure-after.log`; selftest cases 137+ [fill]; source row `S001` (used-by must name this entry) |
| `lessons/round-25.md` | Round-25 lesson: the lane's own mistakes (IDs continue the round-24 `M-1..M-14` numbering [INFERENCE, unchecked]), criteria 9–12 as binding; before/after counts for claims 1–3 [fill] | `evidence/round25-measure-before.log`, `evidence/round25-measure-after.log`; `corpus/QUALITY.md` criteria 9–12; `lessons/round-24-verifier-spotcheck.md` |
| `evidence/round25-claims.md` | Round-25 pre-registration: claims 1–3, frozen populations, `verify-metadata` spec v1, predictions, registered at base d730ae4 | `SCORECARD.md` `## Planned — round 25` (base `:1282-1303`) |
| `evidence/round25-measure.sh` + `round25-measure-before.log` | Read-only counting script (`bash corpus/evidence/round25-measure.sh <tree-root>`) and its base-tree output: gate `752e4e38`; `STALE_INDEX_ITEMS=66`; `STALE_RESTATEMENTS=15`; selftest `PASS (136 cases)`; `GATE_DRIFT: none`; `VERDICT_BEARING_EXPORTS=3/3` | `evidence/round25-claims.md`; the script itself |
| `evidence/round25-measure-after.log` | Landing-tree output of the same script [fill at landing]; predictions (not results): `STALE_INDEX_ITEMS=0`, `STALE_RESTATEMENTS=0`, `METADATA_COMPLETE=25/28`, exit 1 | `evidence/round25-claims.md` |
```

Note for the template rows: the placeholder markers above are deliberate draft slots, not record text. No `TODO`/`TBD`/`${…}` may survive into the committed record (criterion 10).

## 3. Draft appended correction (draft; for `corpus/README.md` after the Round-24 correction block; criteria 4 and 9)

```
Round-25 correction (appended; the 2026-10-16 count and the round-24 count above are dated snapshots): 41 entries — 28 knowledge notes and 13 lessons (`ls corpus/knowledge/*.md | wc -l` → 28; `ls corpus/lessons/*.md | wc -l` → 13, 2026-10-21). The round-24 count of 12 lessons was one short: `lessons/round-24-verifier-spotcheck.md` is the 13th. Rows for `knowledge/audit-r11.md`, `lessons/2026-10-19-hardlink-alias-boundary.md` and `lessons/round-24-verifier-spotcheck.md` are indexed by the round-25 coverage rows; the count is re-derived by the two commands named here.
```

## 4. Per-file freshness findings (obs unless marked)

- `knowledge/audit-r11.md`: `source:` and `verified-at:` present (`verified-at: 2026-10-16T06:50–07:15Z`, ISO-dated). No `recheck:` key: the file's recheck section is a bash block titled "recheck (from the lane cwd…)" (`:22`), so the key is absent → `META_RECHECK_ABSENT`, as predicted. Do not add `recheck:` in this landing without re-registering claim 1 — the file is a frozen population member and the prediction names it.
- audit-r11 pins superseded in-file: gate `46f5ddb3…` (`:304`) → `752e4e38…` (base header, `round25-measure-before.log:1`; `sha256sum tools/research-gate.sh` = `752e4e38…`, 5290 lines). Ledger `3845709b…` (`:307`) → latest revision 71 / 38·21·10·0·3 / queue 24 (`hardening-r10.md:549-559`, the measure's `led[-1]`).
- audit-r11 D-status re-checked by grep: D3 closed by append (`LOG.md:567`). D5 closed by reference (`hardening-r10.md:461-468` supersedes; `corpus/lessons/2026-10-16-archive-scale-controls-and-ledger.md:8` still cites `f5dc8889…`, dated history). D2 OPEN: `SCORECARD.md:328` and `LOG.md:441` still read `-SECTION:sweeps`; no correction line found. D4 OPEN: `SKILL.md:341`, `:367` still carry `46f5ddbf…` (calibration seat). D1 not re-checked (out of scope).
- `lessons/2026-10-19-hardlink-alias-boundary.md`: not `knowledge/`, so criterion 6 header does not apply. It is dated r13 history; its gate sha `6b17e50c…` is the r13 gate (matches `hardening-r10.md:514`, `knowledge/hardlink-alias-r13.md`). All four named receipts exist in `corpus/evidence/`.

## 5. Left to other seats (not edited)

- `LOG.md:437/459/480` keep `LOGPEND8/9/10` inside backticks; the resolution is the append at `LOG.md:567` (D3 closed). Within criterion 10's backtick rule.
- `corpus/evidence/README.md` misfiled rows: EvidenceIdx seat. `SKILL.md` and `hardening-r10.md` addenda r16–r23: calibration seat.

## 6. Tooling and writes

- Installs/updates: none.
- Git: one `git status` (read-only; may refresh the `.git/index` stat cache) and one `git ls-files` for four paths (read-only). No `jj`/git mutation.
- Writes: this report only (`.ufo/waves/round-25/build/ScribeIndexRows.md`, lane root). No corpus file touched.

VERDICT: 41 entries (28 knowledge, 13 lessons); the index has three unindexed entries (audit-r11, hardlink lesson, round-24 spot-check), and the claim-2 prediction holds only if the spot-check row lands with the other two; drafts above are ready to insert, not inserted.
