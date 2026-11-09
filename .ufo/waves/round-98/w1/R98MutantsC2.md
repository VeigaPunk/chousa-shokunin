# R98MutantsC2 — mutation probe of the C2 instrument (`corpus/evidence/round98/entry-controls-r98.py`)

Freeze attacked: `aac826848dda5029ba459568b29d9a92176dc2b6`, shared clone at `/fast/scratch/hyaku/chousa-r98/R98MutantsC2/repo` (never the live lane). Axes probed: (1) normalization/held/element/warrant scoping of the battery, (2) forgery refusal, (3) gate-records as independent backup. No network, no production edits, no prior lane mutation, no new tools installed. Every command below was run with `--root $S/repo` (pristine) or a full copied tree in scratch with only the battery or the ENTRY replaced (forgeries). Scratch deleted at the end; spaced receipts copied to this wave dir.

## Pristine baseline (unmutated battery on unmutated entry)

Command: `python3 -B corpus/evidence/round98/entry-controls-r98.py --root $S/repo`

Observed (receipt `.ufo/waves/round-98/w1/R98MutantsC2-pristine-controls.txt`): `CASE positive held=36/36 ... ok`, `CASE new-only prior=16 own=20 overlap=- ok`, all 7 forgeries `refused ok`, `POSITIVE=1/1 DO_NOTHING_REFUSED=1/1 NEW_ONLY=1/1 FORGERY_REFUSED=7/7 QUESTION_LINES_HELD=36/36 BASE_HELD=16/36 ELEMENTS=7+6/7+6 WARRANTS_OK=10/10 LANE_FILLED=10/10`, `ENTRY_CONTROLS_R98=PASS`, exit 0. Matches the frozen C2 predicate exactly. `tools/gate-records.py verify --root . corpus/knowledge/press-2015-statement-questions-r98.md` → `GATE_RECORDS files=1 records=38 ok=38 fail=0`, exit 0. Battery file SHA-256 `58f58a01fac94b67947566934248e07def965996c6db9f73ce495cbb78d587b8`, entry `4d85bafd7fa637f86f93d18392d0316419af7669427241fc2bcb4ede97a87d6d` (receipts `R98MutantsC2-hashes-{before,after}.txt`); `git status --porcelain` in the clone empty before and after — the attacked tree was never modified except via throwaway copies in scratch.

## Battery mutants (16, one-site each)

Each mutant was written as a full copy of the battery with one site replaced, run with `--root $S/repo` (same frozen bytes). KILLED = prints `ENTRY_CONTROLS_R98=FAIL` or a `SETUP` line (assignment rule); SURVIVED = prints `ENTRY_CONTROLS_R98=PASS` exit 0. Per-mutant receipts `R98MutantsC2-m*.out` in this directory.

| mutant | site | verdict | observed |
|---|---|---|---|
| m01 `norm`→identity (`return s`) | `norm` | KILLED | `QUESTION_LINES_HELD=0/36 BASE_HELD=0/36` FAIL exit 1 |
| m02 `norm` no whitespace-collapse (`return s.strip()`) | `norm` | KILLED | `POSITIVE=0/1` FAIL exit 1 (held still 36/36 but quote/element checks bite) |
| m03 run length cap 4→1 (`i+4`→`i+1`) | `held` | KILLED | `QUESTION_LINES_HELD=33/36 BASE_HELD=15/36` FAIL |
| m04 run length cap 4→2 (`i+4`→`i+2`) | `held` | SURVIVED | PASS exit 0 (`held=36/36` both caps) |
| m05 `held` across entries (runs built from the concatenated quote list, not per entry) | `held` | SURVIVED | PASS exit 0 |
| m06 drop the `?` filter (`if "?" in lines[i]`→`if True`) | `question_lines` | KILLED | `QUESTION_LINES_HELD=43/49 BASE_HELD=23/49` FAIL |
| m07 footer anchor moved +1 (`range(a,b)`→`range(a,b+1)`) | `question_lines` | SURVIVED | PASS exit 0 |
| m08 ELEMENTS S225 substring (`norm(r[2]) in s225_lines`→`norm(r[2]) in norm(cap)`) | `check_elements` | SURVIVED | PASS exit 0 |
| m09 WARRANTS ignore the source parenthesis (regex replaced by a flat S225-only parse) | `check_warrants` | KILLED | `WARRANTS_OK=0/10` FAIL |
| m10 forgery tally forced (`refused += 0 if fp else 1`→`refused += 1`, i.e. deletions refused) | `main` forgery loop | SURVIVED | PASS exit 0 |
| m11 NEW_ONLY overlap dropped (`not overlap and …`→`…` only) | `main` | SURVIVED | PASS exit 0 |
| m12 word cap 25→26 (`<=25`→`<=26`) | `check_quotes` | SURVIVED | PASS exit 0 |
| m13 S225 single-line rule removed (`elif src=="S225" and not any(...)`→`elif False:`) | `check_quotes` | SURVIVED | PASS exit 0 |
| m14 S231 element check pointed at the wrong capture (`norm(caps["S231"])`→`norm(caps["S225"])`) | `check_elements` | KILLED | `ELEMENTS=3+6/7+6` FAIL |
| m15 run join over two spaces (`" "`→`"  "`) | `held` | KILLED | `QUESTION_LINES_HELD=33/36 BASE_HELD=15/36` FAIL |
| m16 do-nothing condition flipped (`erc != 0`→`erc == 0`) | `main` | KILLED | `DO_NOTHING_REFUSED=0/1` FAIL |

Score: 8 KILLED, 8 SURVIVED.

Classification of the 8 survivors (verified with discriminating runs in full copied trees, not score-only):

- **Genuinely weaker, not equivalent (3): m08, m12, m13.** Hand-edited entries that the pristine battery rejects are accepted by the mutant: (a) S225 element cell `"Translation of the research"` (a substring of a whole heading line, not a whole line) → pristine `elements=7/5` FAIL vs m08 `ENTRY_CONTROLS_R98=PASS` exit 0; (b) 26-word single-line K17 quote (26-word prefix of capture line 66) → pristine `bad_quotes=['K17']` FAIL vs m12 `bad_quotes=-` ACCEPTED-then-FAIL only via held (the word-cap itself does not fire); (c) K18 quote joining the line-66 tail with the line-67 question (`"…fields to be included or excluded (database specific)?"` — present in the normalized whole capture but in no single capture line) → pristine `bad_quotes=['K18']` vs m13 `bad_quotes=-` (battery still FAILs overall on `held=35/36`, but the quote check no longer fires). These are coverage holes of a *mutated* battery, not of the frozen battery: the frozen battery kills all three. No C2 sentence is falsified by them.
- **Equivalent on every possible input over these bytes, or weaker-but-unreachable on the frozen entry (4): m04, m05, m07, m11.** m04: no S225 question line equals a run of 3+ consecutive quotes in either entry (cap2/cap3/cap4 all give `held=36/36`); the cap matters only for a future entry needing a 3- or 4-quote join. m05: no cross-boundary run (last-k of prior + first-j of new, k,j≤4) equals any of the 36 question-line texts (`cross matches: 0`); held identical. m07: the line at `Derived from:` contains no `?`, so `range(a,b+1)` selects the same 36 lines. m11: on the pristine entry there is no overlap, so the check is vacuous; a forged entry that adds a prior-held line (K23 duplicating line 34) prints `CASE new-only … overlap=[34]` **still tagged `ok`** under m11 and overall `ENTRY_CONTROLS_R98=PASS` — weaker in principle, but not exercised by any frozen forgery, and the pristine battery *does* refuse that K23 entry (`NEW_ONLY=0/1` FAIL on the same bytes — see E4 below).
- **Tautological mutant (1): m10.** Forcing the forgery tally to always count a refusal cannot fail when every battery forgery is already refused; it only conceals a *new* forgery that the set does not contain. It exists as a warning, not an equivalent: any future forgery added to the set would be miscounted. The frozen battery does not have this defect.

No surviving battery mutant falsifies a C2 sentence: each survivor needs a forgery the frozen battery already rejects (E4 pattern), or cannot change the frozen entry's held counts at all. **However:** the probe does show that the battery's own 7-forgery set is the only thing standing between an `m10`-style tally and silent acceptance, and that NEW_ONLY (m11) is the sole guard against an entry re-holding a line the round-97 entry already holds.

## Entry forgeries (6, judged by the PRISTINE instruments)

Each is a one-edit forgery of the frozen entry, run through pristine `entry-controls-r98.py` and `tools/gate-records.py` in a full copied tree. Receipts summarized per forgery.

| forgery | verdict | entry-controls | gate-records |
|---|---|---|---|
| E1r K1 replaced by `"PRISMA-S checklist"` (a whole non-checklist line of the S225 capture) | REFUSED | FAIL exit 1: `positive held=35/36`, `new-only … FAIL` | PASS exit 0 (reads only `GATE-RECORD` lines; unaffected by `## Located quotes`) |
| E2 S231 M3 quote spanning `<h4>` markup | REFUSED | FAIL exit 1: `bad_quotes=['M3']` | FAIL exit 1: `:158 S231 FAIL QUOTE_ABSENT,WORDS` |
| E3 Do cell inverted (checklist as the *entire* guideline) | **ACCEPTED — SURVIVOR** | PASS exit 0 (Do cells checked only for quoting existing qids) | PASS exit 0 |
| E4 K23 duplicating a prior-held line 34 (run-filling duplicate) | REFUSED | FAIL exit 1: `CASE new-only prior=16 own=21 overlap=[34] FAIL` | PASS exit 0 |
| E5 S231 M1 replaced by a title-field string | NOT A FORGERY | PASS exit 0 | FAIL exit 1: `:156 S231 FAIL WORDS` |
| E6 warrant naming K1 under `(S231)` | REFUSED | FAIL exit 1: `warrants=9/10` | PASS exit 0 |

Notes, per forgery:

- **E3 is the one true survivor**, and it is exactly the surface that Claims C2 Named limit (d) already concedes: "Do and Never cells are checked by the controls only for naming existing quotes of the right source; faithfulness is the reviewer's item (K3)." The instrument never inspects the *content* of a Decision `Do`/`Never` cell. My E3 sentence says the opposite of M1/M13/M14 (the checklist is the *whole* guideline, ignoring the other four documents) and both instruments PASS. This does **not** falsify a C2 sentence — the sentence and Named limit (d) both say the controls do not check this — but it is a kill-rule (K3) item for the reviewer, and the probe confirms it is real: a Do cell can invert its warrants with no instrument trip. Nothing in C2 claims the instrument enforces Do-cell faithfulness, so this is a coverage confirmation, not a falsification.
- E1r fine print: the battery refuses it via `held`/`NEW_ONLY`, not via `bad_quotes` — the PRISMA-S heading line *does* satisfy QUOTES (in capture, in one line), so the refusal is positional. A PRISMA-S question line inside the checklist range would be indistinguishable; the instrument could not tell "question held" from "wrong question held" except through the `held=36/36` count.
- E5 finding: `"Peer Review of Electronic Search Strategies (PRESS)"` **does** occur inside `abstractText`, so a title-field string is not distinguishable by the battery; `gate-records` refused the same edit only on the `words=` count, not on abstract scoping. Entry-controls has no *abstractText*-specific check — it checks the quote against the whole one-line JSON capture (`nq in norm(caps[src])`). A quote drawn from the JSON's non-abstract fields (title, keywordList, doi) that happens to fall inside the abstract string would pass both. Per C2 kill rule K2 ("an S231 quote is not inside the record's abstractText"), the *reviewer* must check that; the battery does not.

## What a survivor would falsify

- m08/m12/m13 survivors are mutants — the **frozen** battery kills all three. They falsify nothing about C2 but prove the checks are load-bearing (removing them changes verdicts).
- m04/m05/m07 are information-free on the frozen bytes; they falsify nothing and could only fire on a future entry/capture shape (3+-quote runs, cross-boundary joins, a `?` in the FOOT line).
- E3 and the abstract-scoping gap in E5 are reviewer-only coverage (pre-declared in C2 Named limits (a)/(d)); they falsify no sentence of C2 but mean K2/K3 remain uninstrumented.

## Restoration evidence

- Clone `git status --porcelain` empty after all runs; battery/entry/prior SHA-256 identical before and after (see hash receipts); no lane file written; scratch `/fast/scratch/hyaku/chousa-r98/R98MutantsC2` removed. Tools installed: none.

## Counter statements (exact commands, receipts, observed line + exit)

1. Command `python3 -B corpus/evidence/round98/entry-controls-r98.py --root $S/repo` → receipt `.ufo/waves/round-98/w1/R98MutantsC2-pristine-controls.txt`, observed `ENTRY_CONTROLS_R98=PASS`, exit 0 (matches C2 predicate line).
2. Command `python3 -B <mutant>.py --root $S/repo` per mutant → receipts `.ufo/waves/round-98/w1/R98MutantsC2-m*.out`, observed `8× ENTRY_CONTROLS_R98=FAIL` exit 1, `8× ENTRY_CONTROLS_R98=PASS` exit 0 (table above).
3. Command `python3 -B corpus/evidence/round98/entry-controls-r98.py --root <copied-tree-with-forged-entry>` → E1r/E2/E4/E6 `ENTRY_CONTROLS_R98=FAIL` exit 1; E3/E5 `ENTRY_CONTROLS_R98=PASS` exit 0 (E5 not a forgery of the battery — quote inside abstractText).
4. Command `python3 -B tools/gate-records.py verify --root . corpus/knowledge/press-2015-statement-questions-r98.md` in forged trees → E2/E5 `GATE_RECORDS files=1 records=38 ok=37 fail=1` exit 1; E1r/E3/E4/E6 `ok=38 fail=0` exit 0 (gate-records does not see `## Located quotes` / decision-table edits).

VERDICT: R98MutantsC2 C2 fired — entry controls are mute on an inverted Do cell (E3, kill rule K3) and blind to JSON-field scoping of S231 quotes (E5), both pre-conceded only for Do cells; no C2 sentence is numerically false.
