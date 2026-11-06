# R81ReviewerC2 — C2 K2 attack log (lane chousa round 81)

Seat: R81ReviewerC2 (leaf; no subagents, no network used).
Attack target: the landed SKILL.md `## Checklist (executable)` Run lines of items 2, 4 (execution) and 5 (prose), at candidate landing `7e2da96a0541946e796384d42fea18e09ede9e9f`.
Kill rule attacked: C2/K2 — a record carrying exactly the item-2 or item-4 defect, in a form the item text names, on which the landed Run command exits 0.

## 0. Setup and byte identity

- Tree under attack: `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin archive 7e2da96a0541946e796384d42fea18e09ede9e9f | tar -x -C /fast/scratch/hyaku/chousa-r81/R81ReviewerC2/tree`.
- Byte identity of the attack target: `git show 7e2da96a…:SKILL.md | sha256sum` → `cf0f73b6de46fd33b06f56356b3addcf0aef908164ffcc66e8c534e9d5336101` = `sha256sum tree/SKILL.md`. Receipt: `receipts/` (inline in this log, §0 of `R81ReviewerC2.md` companion).
- Frozen instruments re-hashed, all equal to claims.md: `checklist-run.py 66ca8c97…`, `depth-r81.py 10c989c0…`, `run-controls.sh c1942bb9…`, `item2-pass d9f1aa51…`, `item2-fail 5f9b89d1…`, `item4-pass 64183e47…`, `item4-fail b7a45309…`, `item5-fail.tsv bf53d570…`.
- No tools installed (bash, python3, git, system grep only). No pacman/uv/npm traffic.

## 1. Baselines (K1 status)

`python3 -B corpus/evidence/round81/checklist-run.py --root .` in the landing tree →
`CHECKLIST_RUN=6/6 DISCRIMINATE=3/3`, `CHECKLIST=PASS`, rc=0. Receipt: `receipts/c2-counter-at-landing.txt`.
C2 K1 holds at the landing revision as measured by this seat; K2 is what follows.

Fixture legs reproduced explicitly with the landed lines (all as the counter claims):

| case | landed line | rc | receipt |
|---|---|---|---|
| item2-pass.md | item-2 compound line | 0 | `receipts/fix-item2-pass.txt` |
| item2-fail.md | item-2 compound line | 1 (`SWEEP_LOCATION_ABSENT`) | `receipts/fix-item2-fail.txt` |
| item4-pass.md | item-4 verify-sweeps | 0 (`REJECTIONS_OK=1/1`) | `receipts/fix-item4-pass.txt` |
| item4-fail.md | item-4 verify-sweeps | 1 (`SWEEP_REJECTION_INCOMPLETE missing=flip`) | `receipts/fix-item4-fail.txt` |
| item5-fail.tsv | item-5 quote-reopen verify | 1 (`QUOTE_REOPEN q1 NO_SOURCE`, `QUOTE_REOPEN_SUMMARY … no_source=1`) | `receipts/fix-item5-fail.txt` |

## 2. Landed Run lines, exactly as SKILL.md prints them (placeholder replaced)

- Item 2 (SKILL.md:72): `f=<record.md>; ! bash tools/research-gate.sh verify "$f" --root . | grep -q '^FINDING NEGATIVE_WITHOUT_SWEEP' && bash tools/research-gate.sh verify-sweeps "$f" --root .`
- Item 4 (SKILL.md:76): `bash tools/research-gate.sh verify-sweeps <record.md> --root .`
- Item 5 (SKILL.md:80): `python3 tools/quote-reopen.py verify --items <items.tsv>`

All runs: cwd = landing tree, `bash -c <line>`, record path absolute, `--root .` as printed.

## 3. K2 FIRES — item-2 defect, landed item-2 line exits 0

Records are in `records/` (sha256 given); receipts in `receipts/`. All records derive from frozen `item2-pass.md` by exactly the one stated mutation and are otherwise identical to the passing fixture.

| # | record (sha256) | defect (form the item text names) | rc | decisive observed line |
|---|---|---|---|---|
| F2-1 | `r2-01-undeclared-sweepid.md` `26b83b66…` | claim N1 names sweep `W1`; **no `## Sweeps` section and no sweep row declares it** — the negative names nowhere | **0** | `VERIFIED_SWEEPS=0/0 REJECTIONS_OK=1/1` + `RESEARCH_GATE: CLEAN` (`receipts/r2-01-undeclared-sweepid.txt`) |
| F2-2 | `r2-02-sweeps-header-only.md` `7631d1ef…` | `## Sweeps` present but **zero sweep rows** (header only); claim names W1 | **0** | `VERIFIED_SWEEPS=0/0 … CLEAN` (`receipts/r2-02-sweeps-header-only.txt`) |
| F2-3 | `r2-06-where-na.md` `fdc1ba40…` | sweep W1 `where` cell = `n/a` — **names nowhere**, but `n/a` contains `/`, classifies local (`sweep_looks_path`), globs to nothing → "verified" | **0** | `SWEEP id=W1 where=n/a looked=local hits=0 at=- observed=verified verdict=match` + `CLEAN` (`receipts/r2-06-where-na.txt`) |
| F2-4 | `r2-09-sweepcell-dash-nosec.md` `734c3195…` | claim N1 sweep cell = `-` (names nothing), no Sweeps section | **0** | `VERIFIED_SWEEPS=0/0 … CLEAN` (`receipts/r2-09-sweepcell-dash-nosec.txt`) |
| F2-5 | `r2-10-sweepcell-na-nosec.md` `e5c0fa51…` | claim N1 sweep cell = `n/a`, no Sweeps section | **0** | `VERIFIED_SWEEPS=0/0 … CLEAN` (`receipts/r2-10-sweepcell-na-nosec.txt`) |
| F2-6 | `r2-14-negsec-only-na.md` `9cea28eb…` | negative kept **only in a `## Negatives` section**, sweep cell `n/a`; no Sweeps section | **0** | `SWEEP id=N1 where=n/a looked=local hits=0 … verified` + `CLEAN` (`receipts/r2-14-negsec-only-na.txt`) |

Mechanism (code, tree `tools/research-gate.sh`): the verify-mode `NEGATIVE_WITHOUT_SWEEP` check fires **only when the claim's sweep cell is empty** (lines 1337–1345); a non-empty cell naming an undeclared id, `-` or `n/a` is never re-resolved. `verify-sweeps` only re-runs rows that exist in `## Sweeps` (or a `## Negatives` fallback via `sweep_raw_where`, which falls back to the `sweep` cell); with no declared rows it reports `VERIFIED_SWEEPS=0/0`, which satisfies its DRIFT condition vacuously → CLEAN, exit 0. `sweep_token_class` (line 2695) calls `sweep_looks_path` (line 2686), which accepts any token containing `/` — so `n/a` is a "local" location whose glob matches nothing and the sweep "verifies".

## 4. K2 FIRES — item-4 defect, landed item-4 line exits 0

Records derive from frozen `item4-pass.md` by exactly the one stated mutation.

| # | record (sha256) | defect (form the item text names) | rc | decisive observed line |
|---|---|---|---|---|
| F4-1 | `r4-02-flip-dash.md` `77c1c84b…` | kept rejection's flip-condition cell = `-` | **0** | `REJECTION id=R1 … flip=present observed=complete` + `REJECTIONS_OK=1/1 … CLEAN` (`receipts/r4-02-flip-dash.txt`) |
| F4-2 | `r4-03-flip-na.md` `a4752b70…` | flip cell = `n/a` | **0** | `flip=present … CLEAN` (`receipts/r4-03-flip-na.txt`) |
| F4-3 | `r4-04-flip-none.md` `2fe77180…` | flip cell = `none` | **0** | `flip=present … CLEAN` (`receipts/r4-04-flip-none.txt`) |
| F4-4 | `r4-06-reason-dash.md` `0903ea1b…` | reason cell = `-` | **0** | `reason=present … CLEAN` (`receipts/r4-06-reason-dash.txt`) |
| F4-5 | `r4-07-alt-section.md` `776dbb12…` | the kept rejection (reason present, flip empty) sits in a section named `## Rejected sources`, not `## Rejections` | **0** | `VERIFIED_SWEEPS=1/1 REJECTIONS_OK=0/0 … CLEAN` — the rejection is never seen (`receipts/r4-07-alt-section.txt`) |

Mechanism: `sweep_flip_cell`/`cell` (lines 2764, 906) treat any non-empty cell as present — `-`, `n/a`, `none` are flip-conditions for the gate (the r5 README's "Honest boundaries" already conceded "a placeholder string would pass"); and the sweeps mode reads only the section literally named `Rejections` (`SEC_BODY[Rejections]`), so a rejection kept under any other header is invisible and `REJECTIONS_OK=0/0` is CLEAN.

## 5. Forms that correctly HOLD (no fire) — completeness of the attack

| record | form | rc | observed |
|---|---|---|---|
| `r2-03-negsec-undeclared.md` | negative in Claims with empty sweep cell + duplicate in `## Negatives` | 1 | verify `NEGATIVE_WITHOUT_SWEEP` (claims-row leg) (`receipts/r2-03-negsec-undeclared.txt`) |
| `r2-04-where-spaces.md` | `where` = whitespace only | 1 | `SWEEP_LOCATION_ABSENT no location named` |
| `r2-05-where-dash.md` | `where` = `-` in a declared W1 row | 1 | `SWEEP_LOCATION_ABSENT unclassifiable location naming` |
| `r2-07-where-none.md` | `where` = `none` | 1 | `SWEEP_LOCATION_ABSENT unclassifiable` |
| `r2-08-where-undeclared-sid.md` | `where` = undeclared source id `S9` | 1 | `SWEEP_LOCATION_UNRESOLVED source_id=S9 not in ## Sources` |
| `r2-11-emptycell-nosec.md` | empty sweep cell, no Sweeps section (designed path) | 1 | verify `FINDING NEGATIVE_WITHOUT_SWEEP severity=warn … obs=claim=N1 negative without sweep` (`receipts/sent-verify-negwithoutswp.txt`) |
| `r2-12-hit.md` | local sweep whose glob really matches (`corpus/fixtures/sweeps-r5.md`) | 1 | `SWEEP_CLAIM_FALSE hits=1` |
| `r2-13-negsec-na.md` | Negatives duplicate + empty claims cell (confounded) | 1 | claims-row `NEGATIVE_WITHOUT_SWEEP` |
| `r4-01-noflip-column.md` | Rejections table with **no flip column at all** | 1 | `SWEEP_REJECTION_INCOMPLETE missing=flip` |
| `r4-05-reason-empty.md` | reason cell empty | 1 | `SWEEP_REJECTION_INCOMPLETE missing=reason` |
| `r4-08-no-rejections-section.md` | no Rejections section (vacuous — see §7 sentence check) | 0 | `REJECTIONS_OK=0/0 … CLEAN` (`receipts/r4-08-no-rejections-section.txt`) |

## 6. False-refusal test (item-2 line vs the well-formed round-5 fixture)

`f=<tree>/corpus/fixtures/sweeps-r5.md; ! … verify … | grep -q '^FINDING NEGATIVE_WITHOUT_SWEEP' && … verify-sweeps …` (cwd = tree, `--root .` as printed) → **rc 0**, `VERIFIED_SWEEPS=2/2 REJECTIONS_OK=3/3 … CLEAN`. The landed item-2 line does **not** refuse the well-formed passing record — no false refusal. Receipt: `receipts/falserefusal-sweeps-r5.txt`. (Root note: under `--root .` the fixture's fleet-relative W1 glob verifies vacuously — the README-documented root sensitivity; direction of this test is unaffected.)

## 7. Factual sentences of the three new Run lines — one verifying command each

Item 2 (SKILL.md:72):
1. "exit 0 with `RESEARCH_GATE: CLEAN` from the sweeps mode" — TRUE. Cmd: landed line on item2-pass.md → rc 0, `RESEARCH_GATE: CLEAN`. `receipts/fix-item2-pass.txt`.
2. "exit 1 when a negative claim has no sweep at all (the structure check's `NEGATIVE_WITHOUT_SWEEP` …)" — TRUE **only for an empty sweep cell**. Cmd: `bash tools/research-gate.sh verify <r2-11> --root .` → rc 1, `FINDING NEGATIVE_WITHOUT_SWEEP severity=warn surface=negatives obs=claim=N1 negative without sweep`. `receipts/sent-verify-negwithoutswp.txt`. FALSE as a general "no sweep at all" claim: r2-01/r2-09/r2-10 carry a negative with no sweep anywhere and the line exits 0 (§3).
3. "`verify-sweeps` alone passes that record, round 81" — TRUE. Cmd: `bash tools/research-gate.sh verify-sweeps <r2-11> --root .` → rc 0 `RESEARCH_GATE: CLEAN` (`VERIFIED_SWEEPS=0/0`). `receipts/sent-vsweeps-alone-r2-11.txt`.
4. "when a sweep names nowhere (`SWEEP_LOCATION_ABSENT`)" — TRUE for empty/whitespace/`-`/`none`; FALSE for `n/a` (r2-06 verifies, §3 F2-3).
5. "when a local sweep has a hit (`SWEEP_CLAIM_FALSE`)" — TRUE. Cmd: landed line on r2-12-hit.md → rc 1, `FINDING SWEEP_CLAIM_FALSE … hits=1 first=corpus/fixtures/sweeps-r5.md`. `receipts/sent-sweep-claim-false.txt`.

Item 4 (SKILL.md:76):
1. "exit 0 with `REJECTIONS_OK=K/K`" — TRUE, and also vacuously at 0/0 (r4-07/r4-08 receipts).
2. "a kept `## Rejections` row without a reason or a flip-condition is `SWEEP_REJECTION_INCOMPLETE`, exit 1" — TRUE for empty cells and a missing flip column; FALSE for placeholder cells `-`/`n/a`/`none` (F4-1…F4-4) and for rejections kept outside the `## Rejections` header (F4-5).
3. "It reads research records only: a rejected `corpus/SOURCES.md` row is not checked by it" — TRUE. Cmd: landed line on r4-08 (zero rejections) → rc 0 `REJECTIONS_OK=0/0 … CLEAN`, while `corpus/SOURCES.md` carries rejected rows S014/S015/S016/S025/S074 (grep receipt in `R81ReviewerC2.md`); sweeps-mode code (lines 2840–3020) reads only the record and root globs.
4. "the fleet census only warns on a thin `teaches` cell (`W02`), not on a missing flip" — TRUE by code: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh:672` `if (status=="rejected" && length(teaches)<8) printf … W02 … thin reject reason`; `grep -n -i flip` over the census → no matches. `receipts/sent-census-w02.txt`. (Census verified by code inspection only; not executed.)

Item 5 (SKILL.md:80):
1. header `id`,`source_id`,`quote` — TRUE; the landed line parsed the fixture TSV (`receipts/fix-item5-fail.txt`).
2. "exit 1 with one `QUOTE_REOPEN` line per other verdict and a `QUOTE_REOPEN_SUMMARY` tally" — TRUE: `QUOTE_REOPEN	q1	NO_SOURCE	no registry row S999999` + `QUOTE_REOPEN_SUMMARY verbatim=0 absent=0 too_long=0 no_source=1 unreachable=0`, rc 1.
3. "(an unregistered id is `NO_SOURCE` before any fetch)" — TRUE: run with `http.client.HTTP(S)Connection` replaced by a raising class (`receipts/sent-item5-nofetch.txt`) → identical output, rc 1, no connection attempt (`NOFETCH_RUN_RC 1`).
4. "It fetches the live page" — TRUE by code: `fetch_page` builds `http.client.HTTP(S)Connection` (`tools/quote-reopen.py:265,444`); live-fetch path NOT exercised (this seat has no egress approval).
5. "exit 0 when every quote is `VERBATIM`" — TRUE by code: `return 0 if counts["VERBATIM"] == len(items) else 1` (`receipts/sent-item5-fetch-pdf.txt`); live path not exercised (no egress); the registered loopback counters (round-30 `QUOTE_REOPEN_HEADLESS_MATCH=106/106`, `QUOTE_REOPEN_FETCH_BOUND_MATCH=27/27`) attest the verdict map without network.
6. "a PDF row is re-opened by `tools/capture-fetch.py` and a located quote in its text form instead" — supported: `quote-reopen.py` has no PDF branch (`grep -i pdf` → none) and `tools/capture-fetch.py:90-93` sniffs `%PDF-` and runs `pdftotext -layout` into text form. Same receipt.

## 8. Residual risk and verification gaps

- Item-5 live behavior (VERBATIM exit-0, UNREACHABLE, PDF row through quote-reopen) is code-attested, not executed — this seat holds no egress approval and took none.
- Census W02 sentence is code-attested only; the census was not run (it scans fleet registries and this seat's write scope excludes everything but its output folder).
- `r2-13` is confounded (its Claims row also carries an empty sweep cell); the clean Negatives-only form is `r2-14`, which fires.
- K2 adjudication is L1's: fires F2-1/F2-4/F2-5 (non-empty-but-undeclared sweep cell) turn on reading "no sweep at all" as "no resolvable sweep", which the item text ("carries its search sweep, naming where it looked") supports; F4-1…F4-4 (placeholder cells) turn on reading "flip-condition" as content, not any non-empty string — the r5 README itself concedes the gate cannot tell.

## 9. Tooling

Nothing installed or upgraded (bash, python3 3.14, git, GNU grep only). No pacman, no uv, no npm. Scratch `/fast/scratch/hyaku/chousa-r81/R81ReviewerC2/` deleted before yield; all receipts and record bytes cited here live in this folder.

VERDICT: R81ReviewerC2 C2 fired — the landed item-2 Run line exits 0 on six negative-without-named-location records (undeclared sweep id, header-only Sweeps, `-`/`n/a` sweep cells, `n/a` where, Negatives-section form) and the landed item-4 Run line exits 0 on five kept-rejection defects (`-`/`n/a`/`none` flip or reason cells, rejection kept under a renamed section), so K2 fires on both items.
