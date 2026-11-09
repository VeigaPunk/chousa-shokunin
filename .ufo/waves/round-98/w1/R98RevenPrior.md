# R98RevenPrior — prior-coverage / novelty falsification (C1, C2, D1)

Seat: R98RevenPrior. Freeze F=aac826848dda5029ba459568b29d9a92176dc2b6, base=98b8177c1e8b39cdf1167928e4f5d609f6fa81b6. Clone: /fast/scratch/hyaku/chousa-r98/R98RevenPrior/repo at F; base tool extracted to /fast/scratch/hyaku/chousa-r98/R98RevenPrior/base-tool/search-rerun.py via `git show` from base.

Tool installs: none.

## Q1 — did any lane instrument at BASE already kill the R97MutantsC1 survivors the base self-test misses?

Method: built 8 one-site mutants of the BASE tool (g01–g05, e02-count-lt, m01-matches-any, v01-env-git-prefix) by exact-string replace (each applies exactly once), then ran `corpus/evidence/round95/rerun-controls-r95.py --root $S/repo --work <scratch> --tool <mutant>` and `corpus/evidence/round97/selftest-controls-r97.py --root $S/repo --work <scratch> --tool <mutant> --no-regression`. Battery PASS with a mutant tool = mutant NOT detected by that battery (survives); battery FAIL = mutant refused (killed). Full log: .ufo/waves/round-98/w1/R98RevenPrior-q1-batteries.txt (g01–g04 complete on both batteries; g05/e02/m01/v01 legs void — scratch deleted before they ran).

Observed:
- g01-case-always-true: r95 RERUN_CONTROLS=PASS (survives r95), r97 SELFTEST_CONTROLS_R97=FAIL (killed by r97 battery). Receipt: R98RevenPrior-q1-batteries.txt `=== g01 r95 === ... RERUN_CONTROLS=PASS`; `=== g01 r97 === ... SELFTEST_CONTROLS_R97=FAIL`.
- g02-case-setup-only: r95 RERUN_CONTROLS=PASS, r97 SELFTEST_CONTROLS_R97=PASS (survives BOTH; neither instrument kills it).
- g03-case-count-all: r95 RERUN_CONTROLS=PASS, r97 SELFTEST_CONTROLS_R97=FAIL (killed by r97).
- g04-summary-always-pass: r95 RERUN_CONTROLS=PASS (survives r95), r97 SELFTEST_CONTROLS_R97=FAIL (killed by r97). Receipt: R98RevenPrior-q1-batteries.txt `=== g04 r95 === ... RERUN_CONTROLS=PASS`; `=== g04 r97 === ... SELFTEST_CONTROLS_R97=FAIL`.
- g05/e02/m01/v01 legs: VOID — the background loop reached them only after the seat's scratch tree had been deleted on yield (`SETUP clone fatal: repository .../repo does not exist`, `can't open file .../selftest-controls-r97.py`). Those four mutants are unscored here; no verdict claimed.

Interpretation (bounded by completed legs): the claim's "23 missed by the base self-test" set was NOT wholly open at BASE for the guard mutants — the r97 battery already refused g01, g03 and g04 via its EXTERNAL/POSITIVE legs, but g02 survived both r95 and r97. Whether the remaining 19 (incl. g05/e02/m01/v01) survived at BASE is unscored here; a non-author seat must complete the loop before C1's novelty number is treated as covered.
- `consensus development forum were undertaken`, `structured PRESS could identify search errors`, `skilled translation of the search strategy`, `Are acronyms or abbreviations used appropriately`, `Are there any other fields to be included`, `Can any limits or filters be added`, `Are the search concepts clear`, `Are the subject headings relevant` → all `none` (no hit in corpus/knowledge/ at BASE). The only `Demonstrated` hit was an unrelated file. Receipt: R98RevenPrior-q2-grep.txt.

So S231's abstract sentences and the 20 newly quoted S225 lines were genuinely new at BASE.

## Q3 — was round-97 routed limit (g) (hash-of-self) refused by any instrument at BASE?

Inspected at BASE: corpus/evidence/round97/selftest-controls-r97.py oracle set = exactly {constant-pass, hollow-selftest, always-fail} (lines ~255–262); no hash-of-self body. Its comment at line 57–58 names the critic's hash-of-self stand-in as refused only via the case-lines requirement, with named limit (g) explicitly stating a forger of case lines is NOT distinguished. Base tools/search-rerun.py has no hash-of-self check (grep `hash|oracle` shows only hashlib for digest computation). plans/round-97.md line 71 confirms limit (g) was the forged-case-lines case. Conclusion: at BASE no lane instrument refused a hash-of-self self-test; the r98 battery's hash-of-self oracle is new.

## D1 — exact reader rule for gate-records.py (round-96/97 spot-checks)

Evidence: corpus/evidence/round57/refetch.tsv holds two S224 rows — a 403 row (jclinepi URL, key 1de3fee3…, curl_rc 22, http 403, `- -`) and a 200 row (jmla URL, key 1a8c36c4…, 0/200, real shas). tools/gate-records.py:238 (admit) binds sid+url+key+fetched+rc+http+txt_sha, but :253 (unreach) binds only sid+url+fetched+curl_rc+http and never checks r[2] (key). Demonstrated on a scratch COPY (lane never edited): with the S224 403 row's key field corrupted to `000000000000000000000000`, the unreach record `GATE-RECORD S224 url=https://www.jclinepi.com/... fetched=2026-11-09T00:36:09Z ... curl_rc=22 http=403` still prints `GATE_RECORD S224 OK`, `GATE_RECORDS ... ok=1 fail=0`, exit 0 (receipt R98RevenPrior-d1-key.txt). The correct unreach (real key) also OK; wrong-admit (jclinepi URL + jmla capture) correctly fails CAPTURE_KEY,REFETCH.

Proposed reader rule (one line, both branches): in the `unreach` branch, add `and r[2] == key` (where `key = sha256(url.encode()).hexdigest()[:24]` is already computed at line ~221) to the `any(...)` predicate; equivalently, require the refetch row's key column to be the content-addressed key of the record's URL before matching on id/url/fetched/status. This rejects a key-mutated/wrong-url S224 row without changing any correct row's verdict (verified direction: real-key row stays OK).

## Counter lines (each command run against the scratch clone, never the live lane)

- `python3 -B $S/base-tool/search-rerun.py --selftest` → last line `SEARCH_RERUN_SELFTEST: PASS cases=48/48`, exit 0 (baseline sanity).
- `python3 -B corpus/evidence/round95/rerun-controls-r95.py --root $S/repo --work $S/w1/r95-g01 --tool $S/base-tool/mut-g01.py` → `RERUN_CONTROLS=PASS`, exit 0.
- `python3 -B corpus/evidence/round97/selftest-controls-r97.py --root $S/repo --work $S/w1/r97-g01 --tool $S/base-tool/mut-g01.py --no-regression` → `SELFTEST_CONTROLS_R97=FAIL`.
- g02: r95 `RERUN_CONTROLS=PASS`; r97 `SELFTEST_CONTROLS_R97=PASS` (survives both). g03: r95 `RERUN_CONTROLS=PASS`; r97 `SELFTEST_CONTROLS_R97=FAIL`. g04: r95 `RERUN_CONTROLS=PASS`; r97 `SELFTEST_CONTROLS_R97=FAIL`.
- `git grep` Q2 lines above (grep exit 1/`none` for all but the S225 citation).
- D1: `python3 -B $S/d1-lane2/gate-records-copy.py verify --root $S/d1-lane2 $S/d1-lane2/unreach-right.md` → `GATE_RECORD ... S224 OK`, exit 0 (key corrupted to zeros).

VERDICT: R98RevenPrior C1 fired — at BASE the r97 battery already killed g01, g03 and g04, so the round-98 kill count is not wholly new coverage, though g02 still survived both prior batteries.
VERDICT: R98RevenPrior C2 held — S231's abstract sentences and the 20 new S225 question lines appear in no knowledge entry at BASE.
VERDICT: R98RevenPrior D1 — the unreach branch of gate-records.py binds everything except the content-addressed key, and a key-corrupted S224 row still passes; require r[2]==key in both branches.
