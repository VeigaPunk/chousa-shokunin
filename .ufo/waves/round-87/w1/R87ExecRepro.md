# R87ExecRepro — clean-tree reproduction of both frozen claims

Seat `R87ExecRepro`. Tree: `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin archive e6e920a4e6988287c31e89b3e920a118b569ae52 | tar -x -C $S` with `S=/fast/scratch/hyaku/chousa-r87/R87ExecRepro/S`. No network. No host mutation. python3 3.14.8 (system `python3`, no installs).

## Commands run (exact) and observed lines

### (a) C1 battery

```
cd $S && python3 -B corpus/evidence/round87/gate-records-r87.py --root $S --repo /home/vgpnk/Projects/shokunin/chousa-shokunin --work $S
```
- exit `0`. Receipt `receipts/01-gate-records-r87.txt`.
- Observed (verbatim):
```
TOOL=present POSITIVE=15/15 FRESH_POSITIVE=5/5 FORGED_REFUSED=362/362 EXPECTED_CODE=362/362 EMPTY_REFUSED=1/1 RC=4/4 SETUP=1/1 D1_EXPECTED=3 D1_FORGES=3 D1_REFUSED=3/3 D2_FORGES=3 D2_REFUSED=3/3 MUT_ADMIT_DERIVED=1 MUT_ADMIT_KILLED=1 MUT_UNREACH_DERIVED=1 MUT_UNREACH_KILLED=1 DERIVE_NEG=1 LEGS=15/15
GATE_RECORDS_R87=PASS
```
- Matches the frozen predicate in `corpus/evidence/round87/claims.md` (C1) field-for-field: `D1_EXPECTED=3 D1_FORGES=3 D1_REFUSED=3/3 D2_FORGES=3 D2_REFUSED=3/3 MUT_ADMIT_KILLED=1 MUT_UNREACH_KILLED=1 DERIVE_NEG=1 LEGS=15/15`, plus `POSITIVE=15/15 FRESH_POSITIVE=5/5 FORGED_REFUSED=EXPECTED_CODE=362` (frozen number in claims.md §C1: `FORGED_REFUSED=EXPECTED_CODE=362`).

Independent re-derivation:
- D1 class width: I parsed `corpus/evidence/round57/refetch.tsv` (185 lines incl. header; 184 data rows), kept rows with `curl_rc=0`, non-200 status, existing capture, and `sha256(capture) == txt_sha256`. Result: exactly 3 rows — `S021` (pubmed 17638714), `S032` (pubmed 17638714), `S022` (pubmed 28912002), all `http=203`. The 4th `S022` row is `curl_rc=22 http=404` (excluded). So `D1_EXPECTED=3` is re-derived, not just echoed. The battery's own independent counter `count_203_rows` (gate-records-r87.py:294-316) re-counts on a separate code path (adds an 8–25-word-line gate on the capture; I confirmed `S022`'s capture has 1 such line, so all 3 survive both gates).
- `FORGED_REFUSED` against generated total: the battery generates `total_forged = len(forged)` at runtime (gate-records-r87.py:418) and prints `FORGED_REFUSED=362/362`; my run's receipt confirms refused == total == 362. D1/D2 contribute 3+3 of the 362; the rest are built from the 15 pinned positives (`c1-positives.tsv`, 15 rows, pin-verified OK).
- `LEGS=15/15`: source audit — 1 `TOOL` leg append (line 375) + 14 entries in the `legs += [...]` list (lines 538-553) = 15, matching frozen `EXPECTED_LEGS=15` (line 41). `passed = len(legs)==EXPECTED_LEGS and all(ok)` (line 566). Derived mutants: `build_mutant` reads the subject tool's bytes (`ADMIT_LITERAL = 'r[6] == "200"'`, `UNREACH_LITERAL = '200 <= int(kv["http"]) < 300'`); `DERIVE_NEG=1` exercises the no-derivation path on a literal-rewritten copy.

### (b) C2 battery

```
cd $S && python3 -B corpus/evidence/round87/curation-r87.py --root $S
```
- exit `0`. Receipt `receipts/02-curation-r87.txt`.
- Observed (verbatim):
```
SUPERSEDED_LIVE=0 UNENTAILED_TERM=0 MODIFIED_DEF_CITED=1 QUOTES_LOCATED=20/20 Q_FLOORS=search-transparency-reporting-r84.md=13/13 floor13,provenance-recording-r85.md=7/7 floor7 WARRANT_OK=17/17 TEACHES_CHECKED=1 TEACHES_FLAGGED=1 TEACHES_UNRESOLVED=0 LEGS=7/7
TEACHES_FLAGGED S024 terms=publication,modification disposition=superseded by S031
CURATION_R87=PASS
```
- Matches frozen C2 sentence/predicate field-for-field plus the in-sentence `Q_FLOORS=13/13 floor13, 7/7 floor7`.

Independent re-derivation:
- `QUOTES_LOCATED=20/20` and floors: I recounted quote tables with my own parser — `search-transparency-reporting-r84.md` has Q1–Q13 (13 rows), `provenance-recording-r85.md` has Q1–Q7 (7 rows); 13+7=20. Floors `13` and `7` equal the measured per-entry totals (they are not smaller round-sum minima). Battery source: `FLOORS = {r84: 13, r85: 7}` (curation-r87.py:42-45); floor leg requires `located >= floor AND located == total` per entry (line 199).
- `WARRANT_OK=17/17`: 11 decision rows (r84) + 6 (r85) = 17, recounted independently. I hand-checked 5 rows (r84 rows 0, 5, 8; r85 rows 1, 5) qid→quote→term chain: e.g. r84 row 0 warrant `Q1 (S214)` → Q1 quote (PRISMA list of sources, captured verbatim) shares distinctive words `consulted/other/reference/sources` with the Do/Never cells; r84 row 8 warrant `Q13 (S023)` → `Date on which the resource was changed.` shares `changed`; r85 row 5 warrant `Q7 (S031)` → lastReviewed definition shares `accuracy/completeness/reviewed`. All 5 resolve all qids, all located verbatim in the qid's own capture, all share a distinctive word. Battery leg: `qids and len(resolved)==len(qids) and shares` (curation-r87.py:180-184).
- `TEACHES_FLAGGED=1`: the flagged row is `S024` (terms `publication,modification`, disposition superseded by `S031`). Independent check: `S024`'s teaches cell says "separate from publication or modification dates" (contrast phrase + date terms present); its capture (key `11d6cc56bb24adfc61eea2b4`, URL `https://schema.org/lastReviewed`) contains `publication` 0, `published` 0, `modified` 0, `modification` 0, `created` 0, `issued` 0. `S031`'s row states `supersedes S024 —`, so `S024` is in the superseded set → disposition superseded, `TEACHES_UNRESOLVED=0`. I also scanned the whole registry for the contrast+date detector shape: `S024` is the ONLY row the detector fires on at this tree (consistent with `TEACHES_CHECKED=1`, not a dead detector per K4 — it has a live instance).

### (c) Instrument pins / landed tool bytes

- All 14 pins in `$S/corpus/evidence/round87/instrument-pins.txt` verified OK against the `$S` tree (sha256): both counters, `mutate-r87.py`, `curation-r87-controls.py`, `harm-recheck.py`, `c1-positives.tsv`, `controls/expected.tsv`, `tools/gate-records.py` (`905f9da2fdf2…`), and all 6 control receipts. `PINS_ALL_OK`.
- `$S/tools/gate-records.py` diffed against the base blob `git show 6495ef88:tools/gate-records.py` (copied to `receipts/06-base-tool-6495ef88.py`): the ONLY change is the unreach repair —
  `success = kv["curl_rc"] == "0" and kv["http"] == "200"` →
  `success = kv["curl_rc"] == "0" and 200 <= int(kv["http"]) < 300`
  (3-line comment citing round-86 F1 and S216 §15.3.4). Any 2xx is a successful response, never a failed transfer.
- S216 grounding: registry row `S216` (RFC 9110, capture key `b1b13a12aee75c6ecc20fb91`) points at §15.3.4; the committed capture's §15.3.4 body (offset ~321126) reads: "The 203 (Non-Authoritative Information) status code indicates that the request was successful but the enclosed content has been modified from that of the origin server's 200 (OK) response by a transforming proxy…" — verbatim the basis for both 203 classes.
- S218 grounding: registry row `S218` (own-work) cites `corpus/QUALITY.md` criterion 178 + `CORPUS.md` rule 2; criterion 178 is present at `corpus/QUALITY.md:1120` and states exactly the `S024`/`S031` contract the TEACHES leg enforces.

### (d) Controls + mutation batteries

```
cd $S && python3 -B corpus/evidence/round87/curation-r87-controls.py --root $S --work $S
```
- exit `0`. Receipt `receipts/03-curation-r87-controls.txt`. Observed: `FORGERY_REFUSED=4/4 R86_ACCEPTED_FORGERY=4/4`, `CONTROLS=PASS`. Each forgery refused with a named `LEG_FAIL`: E5b (FLOOR r85=6/6 floor7), E5c2 (FLOOR 1/1 floor13 + 1/1 floor7), E6 (WARRANT 16/17), T (TEACHES checked=2 flagged=2 unresolved=1); all 4 accepted by frozen `curation-r86.py` (rc=0). Matches claims.md C2 `controls/receipts/c2-controls.txt` description and K3 (`FORGERY_REFUSED=4/4`).

```
cd $S && python3 -B corpus/evidence/round87/mutate-r87.py --root $S --repo /home/vgpnk/Projects/shokunin/chousa-shokunin --work $S
```
- exit `0`. Receipt `receipts/04-mutate-r87.txt`. Observed: `MUTANTS_KILLED=4/4 TOOL_MUTANTS_CAUGHT=2/2 EQUIVALENT_ON_TREE=1/1 TOTAL=6/6` — T4-record-keyed, T4-truncate, M2-credit-mutant, M5-drop-setup all KILLED (rc=1, PASS never printed; e.g. truncate fails `D1_WIDTH 1/3`/`D2_WIDTH 1/3`, M2 fails both MUT legs at derived=0). Tool mutants (`T4-record-keyed-tool`, `admit-2xx-tool`) CAUGHT with `MUT_ADMIT derived=1 killed=0` / `MUT_UNREACH derived=0` patterns as expected. `N-deny-width` is `EQUIVALENT_ON_TREE` (rc=0, PASS) — I did not inspect whether this is a genuine equivalent mutant or a calibration miss; it is inside the battery's own accounting (`EQUIVALENT_ON_TREE=1/1`, `TOTAL=6/6`, exit 0), so it does not fire any C1 kill rule. Noted as a residual question for the mutation seat, not a deviation from the frozen predicate.

### Harm (K3 ground truth)

Because `harm-recheck.py` needs the *base* tool as `--base-tool` (its `--help` shows required `--repo REPO --base-tool BASE_TOOL`; the seat spec's command omits it), I ran:
```
git -C /home/vgpnk/Projects/shokunin/chousa-shokunin show 6495ef88:tools/gate-records.py > $S/base-tool.py
cd $S && python3 -B corpus/evidence/round87/harm-recheck.py --root $S --repo /home/vgpnk/Projects/shokunin/chousa-shokunin --base-tool $S/base-tool.py
```
- exit `0`. Receipt `receipts/05-harm-recheck.txt`. Observed: `HARM_RECHECK files=11 records=28 moved=0 base_rc=0 r87_rc=0`. No committed record moves. (The frozen claims.md cites 27 records across 10 lessons at the freeze; at the landing revision the tree has 11 files / 28 records — the extra record is the new round-87 lesson file `corpus/lessons/round-87.md:13`, a `GATE-RECORD S216 … decision=admit …` line that verifies under both tools. `moved=0` in both counts; no deviation from the K3 substance, only the file census grew by the round's own lesson.)

The one genuine committed unreach record `corpus/lessons/round-81.md:28` (`S208 … decision=reject capture=none curl_rc=22 http=403`) is untouched by the repair and still verifies OK (403 is non-2xx, `curl_rc=22` ≠ 0 → `success=False` → OK). Confirmed in the receipt (`moved=0`).

## Findings

No deviations from the frozen predicates at the landing revision. Both `*_R87=PASS` (exit 0), all printed fields match claims.md, all 14 instrument pins verify, the tool repair is exactly the one-line semantic change claimed, K3 harm holds (`moved=0`), and K3/K4 control shapes (4/4 forgeries refused+accepted-both, 4/4 counter mutants killed, 2/2 tool mutants caught) all reproduce. Two notes, neither a kill:

1. `harm-recheck.py` requires `--base-tool` which the seat spec's (d) command doesn't pass; running it without that flag fails loudly (exit 1, `ABSENT() -> OK()` ×28). With the real base tool it reports `moved=0`. Tooling/usage note, not a claim deviation.
2. The landing tree has 28 committed GATE-RECORDs vs the frozen 27 (the round-87 lesson adds `S216`). Harm result unchanged (`moved=0`).
3. `N-deny-width` is scored `EQUIVALENT_ON_TREE` by the battery; its true-equivalence status is the mutation seat's call. It does not affect either frozen predicate.

Tooling: no installs (python3 3.14.8 system; RULES.md read — no pacman, no uv/npx needed). Scratch `$S` under `/fast/scratch/hyaku/chousa-r87/R87ExecRepro/` is to be deleted by the seat cleanup below; all cited receipts are already copied into `receipts/` (note above).

VERDICT: R87ExecRepro C1 held — battery prints the exact frozen PASS line (LEGS=15/15, D1/D2=3/3) at the landing revision from a clean archive, pins verify, and harm recheck moves 0 records.
VERDICT: R87ExecRepro C2 held — curation prints the exact frozen PASS line (QUOTES 20/20 with floors 13/7, WARRANT 17/17, TEACHES 1 flagged/0 unresolved, LEGS=7/7) and independently re-derived quote/warrant/teaches values agree.

Report: .ufo/waves/round-87/w1/R87ExecRepro.md
