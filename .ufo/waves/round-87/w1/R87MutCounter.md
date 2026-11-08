# R87MutCounter — mutation probe of the two round-87 counters and the repaired subject tool

Seat `R87MutCounter`, leaf (no subagents, no task tool, no commits). Lane `/home/vgpnk/Projects/shokunin/chousa-shokunin`.
Inputs read first: `corpus/evidence/round87/claims.md` (frozen predicate set and every kill rule) and `plans/round-87.md`.
Scratch root `/fast/scratch/hyaku/chousa-r87/R87MutCounter` (deleted before yield). No network was used; no tool was
installed or upgraded (python3 stdlib only). No production byte, claim, plan, counter or tool was edited; every mutant
was written into the scratch tree only.

## Revisions and bytes attacked

| role | revision | extraction |
|---|---|---|
| landing (attacked) | `e6e920a4e6988287c31e89b3e920a118b569ae52` | `git -C $LANE archive e6e920a4… \| tar -x -C $S/land` |
| base (before control) | `6495ef88` | `git -C $LANE archive 6495ef88 \| tar -x -C $S/base` |

Pristine instrument bytes equal the freeze pins `corpus/evidence/round87/instrument-pins.txt`:

```
07336fcad89db1370ffc2cb563961bec2aa7b261a9fd99d17d31b148c31b61e1  corpus/evidence/round87/gate-records-r87.py
a17a02b86b3d07d2a25d5b2f9273098ed83b7fa7962588d8bda050066bb30d23  corpus/evidence/round87/curation-r87.py
9625c8cda07901fb88a60148f57163cf1e3eca4658fd9d8abb4d56f5a8edf235  corpus/evidence/round87/mutate-r87.py
8c089828981bb0c8b5a0ab253bb4ec5f1537825cb84cea8964497310bb01f3c6  corpus/evidence/round87/c1-positives.tsv
905f9da2fdf233b3a599f079a4c40ace730e3acf5464a2b80e1f93a616242d60  tools/gate-records.py
```

The pinned `mutate-r87.py` is a frozen instrument and this seat may not edit production bytes, so the new shapes were
**not** appended to that file. They live in the two drivers copied beside this report
(`receipts/mutation-driver.py`, `receipts/probe-driver.py`) and are re-applied verbatim by one-point replacement to the
landing bytes; `receipts/mutant-sha256.txt` pins every mutant source. The file's existing seven (4 counter, 1
equivalent, 2 tool shapes) are untouched and not re-scored here.

## Detector (identical for pristine and every mutant)

The assigned detector is each counter's own frozen predicate, evaluated on the landing revision: exit 0, verdict
`GATE_RECORDS_R87=PASS` / `CURATION_R87=PASS`, and every field the claim pins equal to its frozen value.
A mutant is **killed** when any of the three stops matching (including "no verdict" / non-zero exit); it is a
**SURVIVOR** when the full frozen line and exit 0 still print.

```sh
# C1 counter (the mutant file sits beside a copy of c1-positives.tsv: POS_TSV is HERE-relative)
python3 -B $M/gate-records-r87.py --root $S/land --repo /home/vgpnk/Projects/shokunin/chousa-shokunin --work $W
# C2 counter
python3 -B $N/curation-r87.py --root $S/land
# subject tool: mutate a copy of tools/gate-records.py, point the PRISTINE counter at it
python3 -B $S/land/corpus/evidence/round87/gate-records-r87.py --root $S/land \
  --repo /home/vgpnk/Projects/shokunin/chousa-shokunin --tool $T --work $W
```

C1 field set compared: `TOOL, POSITIVE, FRESH_POSITIVE, FORGED_REFUSED, EXPECTED_CODE, EMPTY_REFUSED, RC, SETUP,
D1_EXPECTED, D1_FORGES, D1_REFUSED, D2_FORGES, D2_REFUSED, MUT_ADMIT_DERIVED, MUT_ADMIT_KILLED,
MUT_UNREACH_DERIVED, MUT_UNREACH_KILLED, DERIVE_NEG, LEGS`. C2 field set: `SUPERSEDED_LIVE, UNENTAILED_TERM,
MODIFIED_DEF_CITED, QUOTES_LOCATED, WARRANT_OK, TEACHES_FLAGGED, TEACHES_UNRESOLVED, LEGS`.

## Baselines (pristine, before any mutation)

| leg | observed line | exit |
|---|---|---|
| C1 land | `TOOL=present POSITIVE=15/15 FRESH_POSITIVE=5/5 FORGED_REFUSED=362/362 EXPECTED_CODE=362/362 EMPTY_REFUSED=1/1 RC=4/4 SETUP=1/1 D1_EXPECTED=3 D1_FORGES=3 D1_REFUSED=3/3 D2_FORGES=3 D2_REFUSED=3/3 MUT_ADMIT_DERIVED=1 MUT_ADMIT_KILLED=1 MUT_UNREACH_DERIVED=1 MUT_UNREACH_KILLED=1 DERIVE_NEG=1 LEGS=15/15` / `GATE_RECORDS_R87=PASS` | 0 |
| C2 land | `SUPERSEDED_LIVE=0 UNENTAILED_TERM=0 MODIFIED_DEF_CITED=1 QUOTES_LOCATED=20/20 Q_FLOORS=…r84.md=13/13 floor13,…r85.md=7/7 floor7 WARRANT_OK=17/17 TEACHES_CHECKED=1 TEACHES_FLAGGED=1 TEACHES_UNRESOLVED=0 LEGS=7/7` / `CURATION_R87=PASS` | 0 |
| C1 base | `… D2_REFUSED=0/3 … MUT_UNREACH_DERIVED=0 MUT_UNREACH_KILLED=0 … LEGS=11/15` / `GATE_RECORDS_R87=FAIL` | 1 |
| C2 base | the same frozen C2 line and `CURATION_R87=PASS` | 0 |

The C1 base run reproduces the field line of the committed before control `controls/receipts/c1-k0-donothing.txt`
byte-for-byte (`FORGED_REFUSED=359/362 … D2_REFUSED=0/3 … MUT_UNREACH_DERIVED=0 … LEGS=11/15`, exit 1), so the
harness is calibrated against a live committed baseline. Receipts: `receipts/c1-pristine-landing.txt`,
`receipts/c2-pristine-landing.txt`, `receipts/base-tree-c1-counter.txt`, `receipts/base-tree-c2-counter.txt`.

Note: `curation-r87.py` also passes on the base tree — the base tree already carries the repaired quote/warrant
tables (20/20 located), so the round-87 C2 legs are exercised by the defects the C2 control battery injects, not by
the base tree. That is reported, not used as a baseline substitution: every mutant below is scored on the landing
revision.

## C1 counter — 8 new one-point mutants of `gate-records-r87.py`

| id | one-point mutation | observed landing output | verdict |
|---|---|---|---|
| **A1-d2-class-emptied** | `d2 = build_d2_203_rejects(root)` → `d2 = []` | `LEG_FAIL D2_WIDTH 0/3 floor3`, `LEG_FAIL D2_REFUSED 0/0`, `LEG_FAIL MUT_UNREACH derived=1 killed=0`, `D2_FORGES=0`, `LEGS=12/15` / `FAIL`, rc 1 | **KILLED** (leg) |
| **A2-code-credit-blind** | `if code in v[1]:` → `if True:` (a refusal with *any* code is credited as the expected code) | frozen line unchanged, `LEGS=15/15` / `PASS`, rc 0 | **SURVIVOR** (named-limit class) |
| **A3-expected-legs-14** | `EXPECTED_LEGS = 15` → `14` | `LEGS=15/14` / `FAIL`, rc 1 | **KILLED** (accounting identity, no `LEG_FAIL`) |
| **A4-freshok-hardcode** | insert `fresh_ok = 5` after the fresh-positive loop | frozen line unchanged / `PASS`, rc 0 | **SURVIVOR** (named limit: leg runs, value misreported) |
| **A5-unreach-mutant-wrong-shape** | the derived unreach mutant's replacement `kv["http"] == "200"` → `kv["http"] != "200"` | `LEG_FAIL MUT_UNREACH derived=1 killed=0`, `MUT_UNREACH_KILLED=0`, `LEGS=14/15` / `FAIL`, rc 1 | **KILLED** (mutant leg) |
| **A6-pok-hardcode** | insert `p_ok = len(pos)` after the positive loop | frozen line unchanged / `PASS`, rc 0 | **SURVIVOR** (named limit) |
| **A7-admit-mutant-noop** | the derived admit mutant's replacement `'r[6].startswith("2")'` → `'r[6] == "200"'` (no change ⇒ no mutant built) | `LEG_FAIL MUT_ADMIT derived=0 killed=0`, `MUT_ADMIT_KILLED=0`, `LEGS=14/15` / `FAIL`, rc 1 | **KILLED** (K4 derivation leg) |
| **A8-setupok-hardcode** | `setup_ok = 1 if (p.returncode == 2 and "GATE_RECORDS_ERROR" in p.stderr) else 0` → `setup_ok = 1` | frozen line unchanged / `PASS`, rc 0 | **SURVIVOR** (named limit) |

Mutant shas: A1 `9c5b858233dc…`, A2 `751c20e8a1ff…`, A3 `7288f0b12afc…`, A4 `b8ff8ee5cca8…`,
A5 `a544832d98dd…`, A6 `04462c15b118…`, A7 `c9429f68c039…`, A8 `5879dfd07ad1…` (full values in
`receipts/mutant-sha256.txt`; per-mutant stdout/exit in `receipts/c1-mut-<id>.txt`).

## C2 counter — 8 new one-point mutants of `curation-r87.py`

| id | one-point mutation | observed landing output | verdict |
|---|---|---|---|
| **B1-floor-drop** | `floors_ok = all(loc >= fl and loc == tot …)` → `all(loc == tot …)` (drops the per-entry floors) | frozen line unchanged `QUOTES_LOCATED=20/20 … LEGS=7/7` / `PASS`, rc 0 | **SURVIVOR** |
| **B2-total-only-located** | move `total += 1` inside the `located` branch (denominator counts only located quotes) | frozen line unchanged / `PASS`, rc 0 | **SURVIVOR** |
| **B3-warrant-drop-shares** | `if qids and len(resolved) == len(qids) and shares:` → drop `and shares` (any resolving qid passes) | frozen line unchanged / `PASS`, rc 0 | **SURVIVOR** |
| **B4-teaches-dead-detector** | `miss = [t for t in named if cap is None or t not in cap.lower()]` → `miss = []` | `TEACHES_FLAGGED=0`, `LEG_FAIL TEACHES checked=1 flagged=0 unresolved=0`, `LEGS=6/7` / `FAIL`, rc 1 | **KILLED** (leg + field) |
| **B5-def-cited-leg-dropped** | delete `legs.append(("DEF_CITED", …))` | `LEGS=6/7` / `FAIL`, rc 1 | **KILLED** (accounting identity) |
| **B6-entries-narrowed** | delete the second `ENTRIES` line | verdict still `CURATION_R87=PASS`, rc 0, but `QUOTES_LOCATED=13/13`, `WARRANT_OK=11/11` | **KILLED** (field set only — no leg fires) |
| **B7-floor-raised** | entry-1 floor `13` → `20` | `LEG_FAIL FLOOR …r84.md=13/13 floor20`, `LEGS=6/7` / `FAIL`, rc 1 | **KILLED** (leg) |
| **B8-warrant-dead-detector** | `if qids and len(resolved) == len(qids) and shares:` → `if True:` (every row credited) | frozen line unchanged / `PASS`, rc 0 | **SURVIVOR** |

Mutant shas: B1 `d8136bfa7b66…`, B2 `b3a96f6f9202…`, B3 `3d345130a1c4…`, B4 `bd3db5b0ab52…`,
B5 `ab0c34f84950…`, B6 `cd91c2458538…`, B7 `94bb94ac7044…`, B8 `53211f408658…`
(`receipts/mutant-sha256.txt`; per-mutant stdout/exit in `receipts/c2-mut-<id>.txt`).

## Subject tool — 4 new one-point mutants of `tools/gate-records.py`, caught by the PRISTINE C1 counter

| id | one-point mutation | observed output (pristine counter) | verdict |
|---|---|---|---|
| **T3-unreach-203** | `success = kv["curl_rc"] == "0" and 200 <= int(kv["http"]) < 300` → `… and kv["http"] == "203"` | `LEG_FAIL MUT_UNREACH derived=0 killed=0`, `MUT_UNREACH_DERIVED=0`, `LEGS=14/15` / `FAIL`, rc 1; **every other leg passes** (`D2_REFUSED=3/3`, `POSITIVE=15/15`, `FORGED_REFUSED=362/362`) | **CAUGHT** (K4 derivation only) |
| **T4-admit-lt-300** | the admit refetch match `r[6] == "200"` → `int(r[6]) < 300` | `FORGED_REFUSED=359/362`, `EXPECTED_CODE=359/362`, `D1_REFUSED=0/3`, `MUT_ADMIT_DERIVED=0 killed=0`, `LEGS=11/15` / `FAIL`, rc 1 | **CAUGHT** (behavioral legs + derivation) |
| **T5-calendar-check-deleted** | drop `or not _valid_ts(kv["fetched"])` from `parse` | 12 × `WRONG_CODE … D4-non-timestamp-fetched … expected=PARSE got=REFETCH`, `EXPECTED_CODE=350/362`, `LEG_FAIL CODES 350/362`, `LEGS=14/15` / `FAIL`, rc 1 | **CAUGHT** (CODES leg) |
| **T6-git-blob-empty** | `return b.stdout if b.returncode == 0 else None` → `return b""` | `POSITIVE=11/15`, `FRESH_POSITIVE=3/5`, `RC=2/4`, `MUT_ADMIT_KILLED=0`, `MUT_UNREACH_KILLED=0`, `LEGS=10/15` / `FAIL`, rc 1 | **CAUGHT** (positive/RC legs) |

Mutant shas: T3 `9c774224b4fa…`, T4 `93e962b26261…`, T5 `39599ee7a47a…`, T6 `b9e6499d4be9…`
(`receipts/mutant-sha256.txt`; per-mutant stdout/exit in `receipts/tool-mut-<id>.txt`).

### The T3 finding, stated exactly

The round-87 repair's *semantics* (`any 2xx is a successful response`) is exercised by the estate on **203 only**.
`T3` narrows the rule to exactly 203 and every behavioral leg still passes: the D2 class is 203 by construction, and
the other forged unreach forms (U01 `http=200`, U03 `404/410`) are refused because no committed refetch row matches
their claimed status — not because of the success test. The only thing that catches T3 is `MUT_UNREACH_DERIVED`, the
K4 requirement that the mutant be derived from the subject tool's own bytes. A tool whose bytes keep the literal but
whose logic is narrowed differently would not be caught behaviorally by this estate.

## Survivors — the leg that should have killed each, and the probe that shows it

Same probes: the **pristine** counter runs first on the injected defect (proving the leg exists and fires), then the
mutant counter runs on the identical input. Probe trees are scratch copies of the landing tree with one committed
predicate input changed; probe tools are landing tool copies passed with `--tool`. Receipts:
`receipts/probe-<id>-{pristine,mutant}.txt`.

| survivor | leg that should have killed it | exists? | pristine on the probe | mutant on the probe |
|---|---|---|---|---|
| **A2** (any code credited) | `CODES` (`EXPECTED_CODE` must equal the generated total) | yes | probe tool refuses in-class admits with `WRONGCODE`: `EXPECTED_CODE=335/362`, `D1_REFUSED=0/3`, 27 `WRONG_CODE` lines, `LEG_FAIL CODES 335/362` / `FAIL`, rc 1 | `EXPECTED_CODE=362/362`, `D1_REFUSED=3/3`, **no `WRONG_CODE` line printed at all**, `PASS`, rc 0 |
| **A4** (`fresh_ok` hardcoded) | `FRESH` (`fresh_ok == 5`) | yes | probe tool fails every `fresh*.md` record: `LEG_FAIL FRESH 0/5`, `LEG_FAIL RC 3/4`, `LEG_FAIL MUT_ADMIT/MUT_UNREACH killed=0` / `FAIL`, rc 1 | `LEG_FAIL RC 3/4`, `MUT_ADMIT/MUT_UNREACH killed=0` / **`FAIL`, rc 1** — killed on the probe by `RC`, so no fresh failure can be hidden by this edit; the residual exposure is the landing tree only |
| **A6** (`p_ok` hardcoded) | `POSITIVE` (`p_ok == 15`) | yes | probe tree drifts `corpus/lessons/round-80.md:19` one trailing space from `c1-positives.tsv` while the record still verifies: `LEG_FAIL POSITIVE 14/15` / `FAIL`, rc 1 | `POSITIVE=15/15`, **`PASS`, rc 0** — the leg never fires and `RC` stays 0 |
| **A8** (`setup_ok` hardcoded) | `SETUP` (tool must exit 2 + `GATE_RECORDS_ERROR` on a non-git `--repo`) | yes | probe tool with the `--repo` validation deleted: `LEG_FAIL SETUP 0/1` / `FAIL`, rc 1 | `SETUP=1/1`, **`PASS`, rc 0** |
| **B1** (per-entry floors dropped) | `FLOOR` (`loc >= fl and loc == tot` per entry) | yes | probe tree drops unreferenced located `Q10`: `LEG_FAIL FLOOR …r84.md=12/12 floor13` / `FAIL`, rc 1 | `LEGS=7/7`, **`PASS`, rc 0** |
| **B2** (denominator counts located only) | `FLOOR` (`loc == tot`) | yes | probe tree adds an unlocated `Q14` row: `LEG_FAIL FLOOR …r84.md=13/14 floor13` / `FAIL`, rc 1 | `QUOTES_LOCATED=20/20` (the unlocated row drops out of both sides), `LEGS=7/7`, **`PASS`, rc 0** |
| **B3** (warrant distinct-word share dropped) | `WARRANT` (named qid must resolve *and* share a distinctive content word) | yes | probe tree re-points the "derivation's direction" row warrant `Q2 (S215)` → `Q7 (S031)` (resolves, shares no ≥5-letter content word): `LEG_FAIL WARRANT 16/17` / `FAIL`, rc 1 | `WARRANT_OK=17/17`, **`PASS`, rc 0** |
| **B8** (warrant credits every row) | `WARRANT` | yes | probe tree adds a decision row warranted to unresolved `Q99`: `LEG_FAIL WARRANT 17/18` / `FAIL`, rc 1 | `WARRANT_OK=18/18`, **`PASS`, rc 0** |

`B6-entries-narrowed` is killed by the field set, not by a leg: on the landing tree the pristine counter prints
`QUOTES_LOCATED=20/20` and the mutant `13/13` (and `WARRANT_OK` 17/17 → 11/11), so the frozen field comparison
distinguishes them even though every leg passes and the verdict is still `PASS`.

## What the survivors mean

A surviving mutant is a coverage finding against the **counters**, not a defect in the landed repair or the subject
tool: the landing counters print the full frozen C1/C2 lines (baselines above), every in-class forgery is refused, and
all four new subject-tool mutants are caught. No kill rule was tripped:

- **C1.** A2, A4, A6 and A8 are counter edits for which the frozen predicate still prints `PASS` with the full field
  set — the class the claim's named limit already reports ("a counter edit that *executes* a leg and misreports its
  printed value survives — the predicate binds the field the leg prints"). A6 (POSITIVE) and A8 (SETUP) and A2
  (CODES) are shown to be genuine holes, not equivalences: a probe tree/tool that makes the leg fire passes the
  mutant counter. A4 has no independent hole because every fresh failure also breaks `RC` (the counter's own
  `rc_ok == 4` accounting), so hardcoding `fresh_ok` cannot hide a fresh failure — it is a redundant leg on this
  estate, not an exposed one. The derived-mutant legs are load-bearing in the other direction: A1, A5 and A7 (and
  tool T3) are killed by the D2 class, the `MUT_UNREACH` run, and the K4 derivation check respectively.
- **C2.** B1, B2, B3 and B8 are counter edits that keep the full frozen line and verdict. Each corresponding
  **pristine** leg fires on a one-input probe and the mutant does not, so the four legs exist and are load-bearing in
  the landed counter; they are not self-protecting. B4, B5 and B7 are killed by `TEACHES`, the leg-count identity and
  `FLOOR`; B6 only by the printed field set.

## Restoration evidence

Every mutant was written under `$S/mut|drive-*/`, never over a pristine file. Before/after hashes of the three attacked
landing files are identical and equal the freeze pins:

```
07336fcad89db1370ffc2cb563961bec2aa7b261a9fd99d17d31b148c31b61e1  before == after  corpus/evidence/round87/gate-records-r87.py
a17a02b86b3d07d2a25d5b2f9273098ed83b7fa7962588d8bda050066bb30d23  before == after  corpus/evidence/round87/curation-r87.py
905f9da2fdf233b3a599f079a4c40ace730e3acf5464a2b80e1f93a616242d60  before == after  tools/gate-records.py
```

(`receipts/restoration.txt`: `"identical": true`.) The lane checkout was only read (`git archive`,
`git cat-file` via `--repo`); scratch `/fast/scratch/hyaku/chousa-r87/R87MutCounter` was removed after the receipts
were copied here.

## Counter compliance

Each row names the exact command template and the receipt it wrote; every observed line and exit code above is copied
from those receipts. 20 one-point mutants were executed (8 C1 counter, 8 C2 counter, 4 subject tool — beyond the seven
already in `mutate-r87.py`), plus 8 survivor probes × 2 runs and 4 baselines. Nothing is inferred: no "no
verdict" case occurs in the delivered set (the one draft A1 variant that crashed with an uncaught `ValueError` was
replaced by the clean A1-d2-class-emptied and is not counted). Mutant sources and the two drivers are reproduced in
`receipts/`, so every shape is re-runnable from the pinned landing bytes.

VERDICT: R87MutCounter C1 held — the landed counter prints the full frozen C1 line (legs 15/15, `D1/D2` 3/3, both derived mutants killed) and all four new tool mutants are caught, while A2/A4/A6/A8 survive as the claim's named printed-field class (A2, A6, A8 shown to be genuine holes; A4 is covered by the RC leg).
VERDICT: R87MutCounter C2 held — the landed counter prints the full frozen C2 line and the pristine C1/C2 legs fire on every injected probe, while B1/B2/B3/B8 survive as counter coverage gaps and B6 is killed only by the printed field set.
