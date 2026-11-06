# R81ReviewerC2 — scoped findings (round 81, C2 K2 attack)

Revision attacked: `7e2da96a0541946e796384d42fea18e09ede9e9f` (SKILL.md sha256 `cf0f73b6de46fd33b06f56356b3addcf0aef908164ffcc66e8c534e9d5336101`, identical to `git show 7e2da96a…:SKILL.md`). Frozen instruments re-hashed — all match `corpus/evidence/round81/claims.md`. Full log with every command, receipt path, record sha256 and observed line: `.ufo/waves/round-81/w1/R81ReviewerC2/attack.md` (records in `…/R81ReviewerC2/records/`, receipts in `…/R81ReviewerC2/receipts/`).

K1 status first: `python3 -B corpus/evidence/round81/checklist-run.py --root .` in the landing tree prints `CHECKLIST_RUN=6/6 DISCRIMINATE=3/3`, `CHECKLIST=PASS`, rc=0 (`receipts/c2-counter-at-landing.txt`). The counter's own predicate holds; the fires below are K2, on the landed Run lines the counter blesses.

## Findings by severity

**F1 — HIGH, C2/K2 FIRES (item 2).** The landed item-2 Run line (`f=<record.md>; ! bash tools/research-gate.sh verify "$f" --root . | grep -q '^FINDING NEGATIVE_WITHOUT_SWEEP' && bash tools/research-gate.sh verify-sweeps "$f" --root .`) exits **0** on records carrying the item's own defect — a negative claim with no named location. Six forms, each a one-mutation child of frozen `item2-pass.md`, run with the line exactly as SKILL.md prints it (cwd = tree, placeholder replaced):
- `records/r2-01-undeclared-sweepid.md` (`26b83b66…`): claim names sweep `W1`, no `## Sweeps` section, no sweep row declares it → `VERIFIED_SWEEPS=0/0 REJECTIONS_OK=1/1`, `RESEARCH_GATE: CLEAN`, rc 0 (`receipts/r2-01-undeclared-sweepid.txt`).
- `records/r2-02-sweeps-header-only.md` (`7631d1ef…`): Sweeps section with zero rows → same CLEAN rc 0 (`receipts/r2-02-sweeps-header-only.txt`).
- `records/r2-06-where-na.md` (`fdc1ba40…`): `where` = `n/a` → `SWEEP id=W1 where=n/a looked=local hits=0 … observed=verified`, CLEAN rc 0 (`receipts/r2-06-where-na.txt`). Mechanism: `sweep_looks_path` (`tools/research-gate.sh:2686`) accepts any token containing `/`, so `n/a` is a "local" glob matching nothing and the sweep verifies — the item text's "naming where it looked" is satisfied by a cell that names nowhere.
- `records/r2-09-sweepcell-dash-nosec.md` (`734c3195…`) and `records/r2-10-sweepcell-na-nosec.md` (`e5c0fa51…`): claim sweep cell `-` / `n/a`, no Sweeps section → CLEAN rc 0 (`receipts/r2-09…`, `r2-10…`).
- `records/r2-14-negsec-only-na.md` (`9cea28eb…`): negative kept only in `## Negatives`, sweep cell `n/a` → `SWEEP id=N1 where=n/a … verified`, CLEAN rc 0 (`receipts/r2-14-negsec-only-na.txt`).
Root cause: the verify mode's `NEGATIVE_WITHOUT_SWEEP` fires only on an **empty** sweep cell (lines 1337–1345); a non-empty cell naming an undeclared id is never re-resolved, and `verify-sweeps` scores an absent sweep population as `VERIFIED_SWEEPS=0/0` CLEAN. The grep leg `'^FINDING NEGATIVE_WITHOUT_SWEEP'` is exact-prefix, so only the empty-cell path can stop the line.

**F2 — HIGH, C2/K2 FIRES (item 4).** The landed item-4 Run line (`bash tools/research-gate.sh verify-sweeps <record.md> --root .`) exits **0** on kept rejections without a real reason/flip-condition, five one-mutation children of frozen `item4-pass.md`:
- flip cell `-` → `records/r4-02-flip-dash.md` (`77c1c84b…`), `flip=present … CLEAN` rc 0 (`receipts/r4-02-flip-dash.txt`); `n/a` → `r4-03-flip-na.md` (`a4752b70…`, `receipts/r4-03-flip-na.txt`); `none` → `r4-04-flip-none.md` (`2fe77180…`, `receipts/r4-04-flip-none.txt`).
- reason cell `-` → `records/r4-06-reason-dash.md` (`0903ea1b…`), `reason=present … CLEAN` rc 0 (`receipts/r4-06-reason-dash.txt`).
- the kept rejection (reason present, flip empty) under a section named `## Rejected sources` → `records/r4-07-alt-section.md` (`776dbb12…`), `VERIFIED_SWEEPS=1/1 REJECTIONS_OK=0/0 … CLEAN` rc 0 — the rejection is never seen (`receipts/r4-07-alt-section.txt`).
Root cause: `cell`/`sweep_flip_cell` (`tools/research-gate.sh:906,2764`) treat any non-empty cell as present, and the sweeps mode reads only the section literally named `Rejections`. The round-5 fixture README's Honest boundaries already conceded "a placeholder string would pass"; the landed Run line still states the outcome as unconditional ("a kept `## Rejections` row without a reason or a flip-condition is `SWEEP_REJECTION_INCOMPLETE`, exit 1").

**F3 — MEDIUM (prose partially false, same mechanism).** Two factual sentences in the item-2 Run line hold only for the empty-cell cases their fixtures exercise: "a sweep names nowhere (`SWEEP_LOCATION_ABSENT`)" is false for `n/a` (F1, r2-06), and "exit 1 when a negative claim has no sweep at all" is false whenever the sweep cell is non-empty but names nothing (r2-01/02/09/10/14). The sentence "`verify-sweeps` alone passes that record" is TRUE (`receipts/sent-vsweeps-alone-r2-11.txt`, rc 0 CLEAN on r2-11), as are CLEAN-on-pass, `SWEEP_LOCATION_ABSENT` for whitespace/`-`/`none`, and `SWEEP_CLAIM_FALSE` on a real hit (`receipts/sent-sweep-claim-false.txt`, rc 1, `hits=1`).

**F4 — LOW/CONFIRMATORY.** Item-4's remaining sentences verify TRUE: empty reason and a missing flip column are caught (`receipts/r4-05-reason-empty.txt`, `r4-01-noflip-column.txt`, both rc 1 `SWEEP_REJECTION_INCOMPLETE`); "reads research records only, a rejected `corpus/SOURCES.md` row is not checked" — a rejection-free record passes CLEAN `REJECTIONS_OK=0/0` rc 0 while the registry carries rejected rows S014/S015/S016/S025/S074 (`receipts/r4-08-no-rejections-section.txt`); the fleet census W02 is exactly `status=="rejected" && length(teaches)<8` with no flip logic anywhere (`receipts/sent-census-w02.txt`, `scripts/sources-census.sh:672`). Item-5's sentences verify TRUE within this seat's no-egress bounds: unregistered id is `NO_SOURCE` before any fetch (run with `HTTP(S)Connection` denied — identical output rc 1, `receipts/sent-item5-nofetch.txt`), one `QUOTE_REOPEN` line plus `QUOTE_REOPEN_SUMMARY … no_source=1` rc 1 (`receipts/fix-item5-fail.txt`), `exit 0 iff all VERBATIM` and the PDF deferral to `tools/capture-fetch.py` (`pdftotext -layout`, lines 90–93) are code-attested (`receipts/sent-item5-fetch-pdf.txt`).

**False refusal: none.** The item-2 line passes the well-formed round-5 fixture `corpus/fixtures/sweeps-r5.md` rc 0 `VERIFIED_SWEEPS=2/2 REJECTIONS_OK=3/3 CLEAN` (`receipts/falserefusal-sweeps-r5.txt`).

Held forms, for the record: whitespace-only `where`, `-`/`none` in a declared W1 row, undeclared source id `S9` in `where`, empty sweep cell without a Sweeps section (the designed `NEGATIVE_WITHOUT_SWEEP` path), a real local-sweep hit, missing flip column, empty reason — all correctly rc 1 (attack.md §5).

## Residual risk and verification gaps

- K2 adjudication is L1's: the fires turn on reading the item texts as written ("carries its search sweep, naming where it looked"; "kept with its rejection reason and flip-condition") against a gate whose contract is non-empty-cell and declared-section shape; the r5 README concedes the placeholder hole, but no SKILL.md sentence discloses it.
- Item-5 live-fetch sentences and the census W02 are code-attested, not executed (this seat has no egress approval and took none; the census was not run).
- `records/r2-13-negsec-na.md` is confounded (its Claims row also has an empty sweep cell); the clean Negatives-only form is `r2-14`.
- lsp device: not available in this environment; all behavior claims rest on executed-command receipts in `receipts/`, code citations are to the archived tree's `tools/research-gate.sh` line numbers.

## Tooling

Nothing installed or upgraded. Scratch `/fast/scratch/hyaku/chousa-r81/R81ReviewerC2/` (archive tree) deleted before yield; every cited receipt and record byte lives under `.ufo/waves/round-81/w1/R81ReviewerC2/`.

VERDICT: R81ReviewerC2 C2 fired — the landed item-2 Run line exits 0 on six records carrying a negative claim with no named location (undeclared sweep id, header-only Sweeps, `-`/`n/a` sweep cells, `n/a` where, `## Negatives` form) and the landed item-4 Run line exits 0 on five kept rejections lacking a real reason or flip-condition (`-`/`n/a`/`none` cells, rejection under a renamed section), so C2 kill rule K2 fires on both items.
