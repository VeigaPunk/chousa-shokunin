# R88ExecRepro — round-88 frozen-claim reproduction

Tree: `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin archive 4ea9d008abfd2e09cb51649a42678a78f52ac530 | tar -x -C $S` with `S=/fast/scratch/hyaku/chousa-r88/R88ExecRepro`. No network. The bench above (receipt paths under `receipts/`) carries the exact commands, outputs and exit codes. Scratch is deleted before this report is finalized (see cleanup note).

## (a) C1 successor battery — held

Command `python3 -B $S/corpus/evidence/round88/gate-records-r88.py --root $S --repo /home/vgpnk/Projects/shokunin/chousa-shokunin --work $S` (exit 0, receipt `receipts/c1-gate-records-r88.txt`):

```
TOOL=present POSITIVE=15/15 FRESH_POSITIVE=5/5 FORGED_REFUSED=362/362 EXPECTED_CODE=362/362 EMPTY_REFUSED=1/1 RC=4/4 SETUP=1/1 D1_EXPECTED=3 D1_FORGES=3 D1_REFUSED=3/3 D2_FORGES=3 D2_REFUSED=3/3 MUT_ADMIT_DERIVED=1 MUT_ADMIT_KILLED=1 MUT_UNREACH_DERIVED=1 MUT_UNREACH_KILLED=1 DERIVE_NEG=1 LEGS=15/15
LEG_REREAD=15/15 RECONCILED=15/15 LEGS_APPENDED=15
GATE_RECORDS_R88=PASS
```

Independent re-derivation (receipt `receipts/independent-rederive.txt`):

- Width: `csv.DictReader` over `$S/corpus/evidence/round57/refetch.tsv` with `http_code == "203"` → exactly 3 rows: S021, S032 (shared URL 17638714), S022 (28912002), all `curl_rc=0`. Matches `D1_EXPECTED=3`, `D1_FORGES=3`, `D2_FORGES=3`, `ROWS_203=3`.
- Binding in code (read `$S/corpus/evidence/round88/gate-records-r88.py`): `_qualifying_203` (line 279) and `count_203_rows` (line 320) both require `len(http)==3 and http=="203"`; third derivation `registry_rows_203` (line 344) requires `row[6]=="203"` and shares no filter code; width legs (lines 584–587) pin `len(d1)==d1_expected==div3==ROWS_203`.
- Mutants derive from subject-tool bytes: `build_mutant` is called with `ADMIT_LITERAL='r[6] == "200"'` and `UNREACH_LITERAL='200 <= int(kv["http"]) < 300'` read from `$S/tools/gate-records.py` (lines 534, 550); `DERIVE_NEG=1` is the literal-rewritten negative control (lines 567–574). The battery prints this plainly — no "credit".
- Leg receipts: 15 files under `$S/legs/` (`CODES, D1_REFUSED, D1_WIDTH, D2_REFUSED, D2_WIDTH, DERIVE_NEG, EMPTY, FORGED, FRESH, MUT_ADMIT, MUT_UNREACH, POSITIVE, RC, SETUP, TOOL`), every one `ok` with a detail matching the printed tally (e.g. `D1_WIDTH=ok detail=3/3/3 pin3`, `FORGED=ok detail=362/362`). This is the `LEG_REREAD=15/15 RECONCILED=15/15 LEGS_APPENDED=15` line re-verified from the files, not from printed fields.
- `FORGED_REFUSED=362/362` equals `EXPECTED_CODE=362/362` equals the generated total — generated at run time, not a pinned constant.

## (b) C2 curation counter — held

Command `python3 -B $S/corpus/evidence/round88/curation-r88.py --root $S` (exit 0, receipt `receipts/c2-curation-r88.txt`):

```
SUPERSEDED_LIVE=0 UNENTAILED_TERM=0 MODIFIED_DEF_CITED=1 QUOTES_LOCATED=20/20 Q_FLOORS=search-transparency-reporting-r84.md=13/13 floor13,provenance-recording-r85.md=7/7 floor7 WARRANT_OK=17/17 TEACHES_CHECKED=1 TEACHES_FLAGGED=1 TEACHES_UNRESOLVED=0 LEGS=7/7
TEACHES_FLAGGED S024 terms=publication,modification disposition=superseded by S031
CURATION_R88=PASS
```

Independent re-derivation (receipt `receipts/independent-rederive.txt`):

- `QUOTES_LOCATED`: re-located every `Located quotes` row through the registry URL → capture hash and checked verbatim (whitespace-normalized, curly quotes folded) membership: 13/13 in r84, 7/7 in r85 → 20/20.
- Per-entry qid sets: r84 Q1–Q13 (13) and r85 Q1–Q7 (7) match the pinned `QID_SETS` exactly.
- Token floor: counted words of all 20 located quotes; minimum is r84 `Q13` "Date on which the resource was changed." at 7 words → `MIN_TOKENS = 7` is the measured minimum. Second-smallest is 9 (Q2, Q11, Q12). Every quote is ≥ 7.
- `WARRANT_OK 17/17`: 11 decision rows in r84 + 6 in r85 (counter's header/separator skip applied: `Situation` and `---` rows skipped, else the count is 21). Hand-checked five rows against the counter's rule (every named qid resolves; every qid's quote shares a distinctive ≥5-letter non-stopword with the row's cells): r84 "Linking a claim to its source" (Q6,Q7), r85 "Naming what a resource derives from" (Q1), r85 "Recording when content was last reviewed" (Q7), r84 "Reporting how studies were selected" (Q4), r85 "Recording a resource's provenance" (Q5) — all chain through. The repaired row shares `entities, property, provenance` via Q1.
- `TEACHES_FLAGGED=1`: the only flagged row is S024 ("...a property separate from publication or modification dates" — contrast `separate from` + date terms `publication, modification`; neither word occurs in S024's own capture). Its disposal is S031, `status=mined` (S024 is `queued`), and S031's own teaches reads in its own capture — the `mined`-superseder leg, not any superseder.

## (c) Instrument bytes — held

`sha256sum -c corpus/evidence/round88/instrument-pins.txt` from `$S`: all 14 entries `OK` (receipt `receipts/instrument-pins.txt`). `$S/tools/gate-records.py` hashes to `905f9da2…242d60`, identical to the landing blob at `4ea9d008…:tools/gate-records.py`; the freeze-base diff `f484d94f..4ea9d008` touches `tools/gate-records.py` in 0 lines (unchanged this round, as claimed). The one entry repair is the single line `Q1, Q3 (S215)` → `Q1 (S215)` in `corpus/knowledge/provenance-recording-r85.md`.

## (d) Controls and mutations — held

- `curation-r88-controls.py --root $S --work $S` (exit 0, `receipts/c2-controls.txt`): positive accepted by both; all five round-87 forgeries refused by r88 with a named `LEG_FAIL` (A1c FLOOR, A1d FLOOR, caseG FLOOR, F2 TEACHES, B1b WARRANT) and accepted by the frozen r87 counter → `FORGERY_REFUSED=5/5 R87_ACCEPTED_FORGERY=5/5 CONTROLS=PASS`.
- `mutate-r88.py --root $S --repo … --work $S` (exit 0, `receipts/mutate-r88.txt`): `MUTANTS_KILLED=6/6 TOOL_MUTANTS_CAUGHT=2/2 EQUIVALENT_ON_TREE=0/0 TOTAL=8/8` — T4-record-keyed, T4-truncate, M2-credit-mutant, M5-drop-setup, E1-joint-narrow, E4-setup-detached killed; T4-record-keyed-tool and admit-2xx-tool mutants caught.
- `harm-recheck.py --root $S --repo … --base-tool $S/tools/gate-records.py` (receipt `receipts/harm-recheck.txt`): `HARM_RECHECK files=11 records=28 moved=0 base_rc=0 r88_rc=0` — no genuine record's verdict moved, so kill rule K3 is not triggered.

## Findings, risks, blockers

No deviations from any frozen field in either claim. No kills triggered. Constraints observed: every check above was executed (none skipped); no `GET`/network; no host sysctl/sudo/service actions; no edits outside `.ufo/waves/round-88/w1/R88ExecRepro/` and the scratch dir; scratch removed by `rm -rf -- "$S"` before yield (plus `trap` discipline honored via explicit removal). Tooling used: system `python3` (stdlib only), `git`, `sha256sum`, `tar` — all pre-existing; no installs were needed or performed.

VERDICT: R88ExecRepro C1 held — the battery prints the exact frozen line and I re-derived the 203 width (3 rows), forgery total (362) and all 15 leg receipts from the tree.
VERDICT: R88ExecRepro C2 held — the counter prints the exact frozen line and I re-located all 20 quotes, measured the 7-word floor minimum, hand-checked warrant chains, and confirmed the one mined-superseder disposition.
