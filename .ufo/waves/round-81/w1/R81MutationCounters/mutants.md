# R81MutationCounters — mutant table (round 81, L1 chousa)

Attacked bytes: `7e2da96a0541946e796384d42fea18e09ede9e9f` (candidate landing), counters
`corpus/evidence/round81/depth-r81.py` (sha256 `10c989c0…da1e9`) and
`corpus/evidence/round81/checklist-run.py` (`66ca8c97…5bbc2`), driver
`run-controls.sh` (`c1942bb9…7ea65c`) — all three matching the instrument hashes in
`corpus/evidence/round81/claims.md`.

Detector: the committed control driver, unchanged, run from the mutated tree
(`bash <tree>/corpus/evidence/round81/run-controls.sh 378fda82dc2cbcc555a0565052cc408121813cef <out>`);
the driver resolves the counter from its own tree, so the mutation is what executes.
Verdict rule: KILLED iff any of the 16 controls deviates from its pristine exit code
(baseline rc, in driver order: 1,1,0,1,1,1,1,1,1,1,0,1,1,1,2,1, all matching `expect_rc`), else SURVIVED.

35 mutants: 18 in `depth-r81.py`, 17 in `checklist-run.py`. Evidence:
`receipts/mutant-runs.tsv`, `receipts/summary-all.json`, per-control receipts in
`receipts/baseline-controls/` (pristine) and `receipts/killing/` (killing control).

| # | mutant (clause) | verdict | killing control (expect→got) |
|---|---|---|---|
| d01 | P1 `len(fids) < 2` → `< 1` | SURVIVED (equivalent) | none — see N1 |
| d02 | P1 drop `opened == --date` | KILLED | c1-f3-stale-opened-date (1→0) |
| d03 | P1 drop `used_by` names-entry | SURVIVED | none — witness W3 (1→0) |
| d04 | P1 drop `status == mined` | SURVIVED | none — witness W4 (1→0) |
| d05 | P2 quote lines `< 3` → `< 1` | SURVIVED | none — witness W5 (1→0) |
| d06 | P2 word cap `> 25` → `> 9999` | SURVIVED | none — witness W6 (1→0) |
| d07 | P2 drop `sid not in fids` | SURVIVED (rc coincidence: KeyError) | c1-f1 sees a traceback, rc still 1 = expected |
| d07b | P2 weaken to `sid in ids` | SURVIVED | none — witness W7b (1→0) |
| d08 | P2 distinct rows `< 2` → `< 1` | SURVIVED | none — witness W8 (1→0) |
| d09 | P2 drop whole refetch.tsv binding | KILLED | c1-f5-capture-not-recorded (1→0) |
| d10 | P2 drop refetch `fetched_utc == date` | SURVIVED | none — witness W10 (1→0) |
| d11 | P2 drop refetch `txt_sha256 == sha` | KILLED | c1-f5-capture-not-recorded (1→0) |
| d12 | P2 drop the capture needle check | KILLED | c1-f2-altered-quote (1→0) |
| d13 | P3 drop the table requirement | KILLED | c1-f6-no-table (1→0) |
| d14 | P4 drop duplicate-bytes branch | SURVIVED (equivalent) | none — see N2 |
| d15 | P4 drop shared-quote branch | SURVIVED | none — witness W15 (1→0); confirms the pre-data note |
| d16 | threshold `k >= 2` → `>= 1` | KILLED | c1-f1, f2, f3, f4, f6, f7 (1→0 each) |
| d17 | P2 drop `curl_rc==0` and `http 2xx` | SURVIVED | none — witness W17 (1→0) |
| c01 | denominator `!= 6` → `!= 0` | KILLED (malformed flip) | every control, rc 2 ("denominator 6 != 6") |
| c01b | denominator accepts any count ≥ 1 | KILLED | c2-g4-item-deleted (2→1) |
| c02 | legs ignore the exit code (`good = True`) | KILLED | c2-g2-or-true, c2-g5-wrong-mode (1→0) |
| c03 | item2 pass/fail rc swapped | KILLED | c2-pos-candidate (0→1) |
| c04 | item4 pass/fail rc swapped | KILLED | c2-pos-candidate (0→1) |
| c05 | item5 `no_source=1` needle removed | SURVIVED | none — witness C5 (1→0) |
| c06 | needle branch never evaluated | SURVIVED | none — same clause as c05 |
| c07 | `r = bool(runs)` → `r = True` | SURVIVED (rc coincidence: IndexError) | c2-k0 sees a traceback, rc still 1 = expected |
| c08 | drop all discrimination legs | KILLED | c2-pos-candidate (0→1) |
| c09 | verdict drops `runnable == 6` | SURVIVED | none — witness C9: prints `CHECKLIST_RUN=5/6 … CHECKLIST=PASS` rc 0 |
| c10 | drop the no-placeholder refusal | SURVIVED (equivalent) | none — see N3 |
| c11 | every placeholder → first fixture (drop `count=1`) | SURVIVED | none — witness C11 (1→0) |
| c12 | invert the rc comparison | KILLED | c2-pos-candidate (0→1) |
| c13 | item numbering 1-based → 0-based | KILLED | c2-pos-candidate (0→1) |
| c14 | drop the missing-fixture guard | SURVIVED | none — witness C14 (rc 2→1) |
| c15 | first Run command → last Run command | SURVIVED | none — witness C15 (0→1) |
| c16 | item5 `needle in x` → `True` | SURVIVED | none — same clause as c05 |

Killed 14 / survived 21 (18 live-clause coverage gaps, 3 equivalent mutants).

## Survivor detail — clause no control exercises

All witnesses are hand-built trees with the shape of the driver's `snap`/`addrows`/`entry`
trees, run twice: pristine counter vs the single mutant. Receipts are the raw stdout of each
run under `receipts/witness/<tree>.<mutant>.{pristine,mutant}.txt`.

- **W3 d03** — `w-used-by`: rows mined, opened 2026-11-06, `used_by` naming another entry.
  pristine `ENTRY ctl-a-r81.md counted=no reason=P1-fresh-rows=0` rc 1;
  mutant `counted=yes`, `DEPTH_R81 entries=2 …=PASS` rc 0.
- **W4 d04** — `w-status`: rows opened today with status `rejected`.
  pristine `P1-fresh-rows=0` rc 1; mutant `entries=2 … PASS` rc 0.
- **W5 d05** — `w-two-quotes`: entry with two located quote lines.
  pristine `P2-quote-lines=2` rc 1; mutant `counted=yes … PASS` rc 0.
- **W6 d06** — `w-word-cap`: entry with a located 28-word quote.
  pristine `P2-quote-words=28` rc 1; mutant `counted=yes … PASS` rc 0.
  (Control f7 does not isolate the cap: its doubled quote is also absent from the capture.)
- **W7b d07b** — `w-stale-listed-row`: quote cites S906, listed on the source line, opened
  2026-10-21. pristine `P2-quote-cites-non-fresh-S906` rc 1; mutant `counted=yes … PASS` rc 0.
- **W8 d08** — `w-one-row`: three located quotes all from S901.
  pristine `P2-distinct-rows<2` rc 1; mutant `counted=yes … PASS` rc 0.
- **W10 d10** — `w-refetch-date`: refetch rows dated 2026-10-21, registry opened 2026-11-06.
  pristine `P2-no-fetch-record-S901` rc 1; mutant `counted=yes … PASS` rc 0.
- **W15 d15** — `w-shared-quote`: two byte-distinct, individually valid entries sharing one
  located quote (S905, `used_by` naming both).
  pristine `ENTRY ctl-b-r81.md counted=no reason=P4-shared-quote` rc 1;
  mutant `counted=yes`, `entries=2 fresh_rows=4 located_quotes=6`, `DEPTH_R81=PASS` rc 0.
- **W17 d17** — `w-curl-rc`: refetch row with `curl_rc=22`, sha still matching.
  pristine `P2-no-fetch-record-S901` rc 1; mutant `counted=yes … PASS` rc 0.
- **C5 c05** — `w-needle`: item 5's Run line prints `QUOTE_REOPEN_SUMMARY no_source=0` and
  exits 1. pristine `ITEM 5 … leg=fail`, `DISCRIMINATE=2/3`, rc 1; mutant `leg=pass`,
  `CHECKLIST_RUN=6/6 DISCRIMINATE=3/3`, `CHECKLIST=PASS` rc 0. (c06, c16 are the same clause.)
- **C9 c07 / C7** — `w-item1-no-run`: item 1 (non-leg) carries no Run line.
  pristine `CHECKLIST_RUN=5/6 DISCRIMINATE=3/3` rc 1; c07 mutant `CHECKLIST_RUN=6/6 … PASS` rc 0;
  c09 mutant `CHECKLIST_RUN=5/6 DISCRIMINATE=3/3 / CHECKLIST=PASS` rc 0 — PASS printed beside a
  5/6 counter, i.e. the predicate text is not what the battery checks.
- **C11 c11** — `w-placeholders`: item 2's Run line carries two `<record.md>` placeholders and
  only the second decides the exit code. pristine `DISCRIMINATE=2/3` rc 1; mutant `3/3 … PASS` rc 0.
- **C14 c14** — `w-missing-fixture` with `--fixtures` lacking `item4-fail.md`:
  pristine `CHECKLIST error: missing fixture item4-fail.md` rc 2; mutant rc 1.
- **C15 c15** — `w-last-run`: item 2 carries the real Run line plus a trailing `true <record.md>`.
  pristine `CHECKLIST=PASS` rc 0; mutant `DISCRIMINATE=2/3 … FAIL` rc 1.

## Surviving mutants that are equivalent (not coverage gaps)

- **N1 d01** — with one fresh row the entry fails P2's `distinct fresh rows >= 2` anyway.
  `eq-d01.d01.pristine` → `P1-fresh-rows=1` rc 1; `eq-d01.d01.mutant` → `P2-distinct-rows<2`
  rc 1. Same counted set and rc; only the printed reason shifts. Unobservable in the predicate.
- **N2 d14** — identical bytes imply identical quote lines, and P2 guarantees ≥ 3 quote lines, so
  `P4-shared-quote` always fires when `P4-duplicate-bytes` would. d14's own f4 run:
  `receipts/killing/d14--c1-f4-duplicate-entry.txt` → `counted=no reason=P4-shared-quote` rc 1.
  The two branches mask each other; only one of them is behaviourally observable.
- **N3 c10** — a placeholder-free Run command receives no per-leg argument, so it must exit the
  same way on the pass and the fail fixture; the leg fails with or without the early refusal.
  No leg verdict can change.

## Restoration

Every mutant run restored the mutated file with `git -C <worktree> checkout -- <file>` and
re-hashed it: `restored_sha == pristine_sha` for all 35 entries in `receipts/mutant-runs.tsv`
(columns `mutant_sha16`, `pristine_sha16`, `restored_sha16`). The three instrument files in the
unmutated tree still hash to the frozen values (`10c989c0…`, `66ca8c97…`, `c1942bb9…`).
