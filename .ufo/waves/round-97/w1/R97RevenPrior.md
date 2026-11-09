# R97RevenPrior — newness / routed-debt check (leaf, falsify only)

Seat: R97RevenPrior. Tree attacked: F = 9a0ce2015fa0254848f2f32f612b20caf7dc5478 (clone
`/fast/scratch/hyaku/chousa-r97/R97RevenPrior/repo`, checkout F; BASE = c8087ac529003e667505bcc624f9a7bde0cffbce
reached via `git show BASE:...`). No production edits; scratch only under
`/fast/scratch/hyaku/chousa-r97/R97RevenPrior/` (removed before yield). No tools installed
(pacman paused host-wide; none needed — stock python3/git/grep only).

Questions: (1) was the C1 debt really open at BASE? (2) does any BASE file hold the PRESS
checklist questions? (3) D1: does a correction row break the three TSV readers?

---

## Q1 — were the 20 base survivors already killed at BASE?

### The 20 base survivors (frozen counter)

Command (F tree, committed before-receipt):
`git -C $S/repo show 9a0ce2015fa0254848f2f32f612b20caf7dc5478:corpus/evidence/round97/before/c1-base.txt | grep SURVIVED`
→ `CASE external n02/n07/n09/n10/n11/n12/n13/n14/n15/n16/n17/n20/n22/n23/n26/n27/n28/n29/s1/s2 SURVIVED ...`
Observed tail: `CASE do-nothing-base BASE_KILLED=10/30 ...` and
`POSITIVE=0/1 EXTERNAL_KILLED=10/30 DO_NOTHING_REFUSED=1/1 R96_MUTANTS_KILLED=23/23 NO_WRITE=1/1 BASE_KILLED=10/30 CASES=47`
(line in `corpus/evidence/round97/before/c1-base.txt`). So the "20 survivors" = 30 − 10 killed.

**Important qualification the claim already states:** n11/n12/n13/n26 exit 1 with a traceback and no
FAIL line and "count as survivors" (claims.md C1 Before). The frozen kill rule is
`rc == 1 and "SEARCH_RERUN_SELFTEST: FAIL" in out and "Traceback" not in err` (r97 battery `killed()`),
i.e. a crash is NOT a kill. Any "already killed" finding must be judged against the frozen rule,
not against a looser battery-FAIL reading.

### Method (as assigned: `--tool <each base mutant>` for ≥8)

Built each mutant at BASE: `git show BASE:tools/search-rerun.py` → apply the one-site
`(old,new)` from the committed probe (`.ufo/waves/round-96/w1/R96MutantsC1-mutprobe.py.txt`, parsed
with the battery's `_lit`) plus the two Sentinel mutants transcribed in
`corpus/evidence/round97/selftest-controls-r97.py:SENTINEL`. All 8 sampled applied exactly once
(each `src.count(old)==1`, asserted in driver). Sampled 8 spanning all four families:
`n02-findings-per-row` (judgement), `n07-digest-uses-tree` (digest), `n11-header-order` (parse),
`n14-rev-regex-case` (parse), `n17-regex-search-to-match` (matches), `n20-utf8-strict` (matches),
`n26-cells-strip-order` (parse), `s2-partial-scrub` (git_env).
Receipts: `.ufo/waves/round-97/w1/R97RevenPrior-q1-r96-tallies.txt`,
`R97RevenPrior-q1-r95-tallies.txt`, per-mutant `R97RevenPrior-r96-<name>.txt` /
`R97RevenPrior-r95-<name>.txt`.

- r96 adapter: `python3 -B corpus/evidence/round96/selftest-controls-r96.py --root . --work <scratch/r96-<name>> --tool <base-mutant> --no-regression`
  (run at F; battery reads BASE tool/mutants via `git show bbf64970...`, ancestor of BASE).
- r95 adapter: `python3 -B corpus/evidence/round95/rerun-controls-r95.py --root . --work <scratch/r95-<name>> --tool <base-mutant>`
  (8-way parallel; each ~40–90 s).
- Direct: `python3 -B <base-mutant> --selftest` → `--selftest` is the BASE 32-case self-test.

### Results (exact tallies)

| mutant | direct selftest (BASE) | r96 `--tool` | r95 `--tool` |
|---|---|---|---|
| n02-findings-per-row | PASS 32/32 rc 0 | `POSITIVE=1/1 MUTANTS_KILLED=23/23` **PASS** rc 0 | `RERUN_CONTROLS=PASS` rc 0 |
| n07-digest-uses-tree | PASS 32/32 rc 0 | `POSITIVE=1/1 MUTANTS_KILLED=22/23` FAIL rc 1 (**setup artifact**, see below) | `POSITIVE=0/1 FORGERY_REFUSED=2/10` **FAIL** rc 1 |
| n11-header-order | crash rc 1, Traceback, **no FAIL line** | `POSITIVE=0/1 MUTANTS_KILLED=0/23` FAIL rc 1 (crash) | `POSITIVE=0/1 ... SETUP_REFUSED=4/12` **FAIL** rc 1 (crash) |
| n14-rev-regex-case | PASS 32/32 rc 0 | PASS 23/23 rc 0 | PASS rc 0 |
| n17-regex-search-to-match | PASS 32/32 rc 0 | PASS 23/23 rc 0 | `POSITIVE=0/1 FORGERY_REFUSED=0/10` **FAIL** rc 1 |
| n20-utf8-strict | PASS 32/32 rc 0 | PASS 23/23 rc 0 | PASS rc 0 |
| n26-cells-strip-order | crash rc 1, Traceback, **no FAIL line** | `POSITIVE=0/1 MUTANTS_KILLED=0/23` FAIL rc 1 (crash) | `POSITIVE=0/1 ... SETUP_REFUSED=4/12` **FAIL** rc 1 (crash) |
| s2-partial-scrub | PASS 32/32 rc 0 | `POSITIVE=1/1 MUTANTS_KILLED=22/23` FAIL rc 1 (**setup artifact**) | PASS rc 0 |

Observed lines (tallies in receipts):
- r96 n07: `CASE mutant m22-no-digest-compare SETUP applies 0 times FAIL` (in `R97RevenPrior-r96-n07-digest-uses-tree.txt`).
- r96 s2: `CASE mutant m20-no-env-scrub SETUP applies 0 times FAIL` (in `R97RevenPrior-r96-s2-partial-scrub.txt`).
- r96 n11: `CASE positive rc=1 expect=0 FAIL` + all 23 `SURVIVED` with `failed=-` because the tool
  crashes before any case (in `R97RevenPrior-r96-n11-header-order.txt`).
- r95 n07 positive: `CASE positive rc=1 expect=0 FAIL`; direct `verify` on the mutant prints
  `SEARCH_RERUN Q1 rev=DRIFT ... SET_DRIFT,TREE_CHANGED` and `SEARCH_RERUN: DRIFT` (false drift on
  the good record), vs the clean `rev_match=8/8` on the base tool.
- r95 n17 positive: `CASE positive rc=1 expect=0 FAIL`.
- Direct n11/n26: stdout 0 bytes, stderr `Traceback ... raise Setup("HEADER", ...)`, rc 1, no
  `SEARCH_RERUN_SELFTEST: FAIL` line (in `R97RevenPrior-n11-selftest.txt` / `R97RevenPrior-n26-selftest.txt`).

### Reading — three definitions of "killed", only one is the frozen rule

1. **Frozen C1 kill** (exit 1 + FAIL line + no Traceback): **0 of 8 killed**. n02/n07/n14/n17/n20/s2
   print `PASS 32/32`; n11/n26 print a traceback and no FAIL line. This confirms the before-receipt's
   10/30: the BASE self-test alone did not detect any of the sampled survivors. The C1 "new debt"
   premise for the *self-test* is intact on this sample.
2. **mutants-r95 kill** (`rerun-controls-r95.py` prints `RERUN_CONTROLS=FAIL`): **4 of 8**
   (n07, n11, n17, n26). Of these, only **n07 and n17** are genuine detections — the mutant's
   `verify` deviates from expected verdicts (`POSITIVE=0/1`, `FORGERY_REFUSED` collapses) on the
   committed r95 record, which is exactly the evidence mutants-r95.py scores (`KILLED when battery
   prints RERUN_CONTROLS=FAIL`). n11/n26 "fail" the battery only because `verify` exits 2
   (`Setup: HEADER`) on every row — a crash, counted as killed by that definition but, per the
   frozen rule, not a detection.
3. **r96 battery as `--tool`**: three FAILs are **not kills at all** and must not be counted:
   n07 and s2 fail with `SETUP applies 0 times` (the external mutant already replaced the very
   string an r96 mutant needs — m22 for n07, m20 for s2 — so the battery fails to *set up* one of
   its own mutants, not to detect the external one). n11/n26 fail with `MUTANTS_KILLED=0/23` because
   the tool crashes in POSITIVE, so all 23 r96 mutants "survive" as crashes. Counting any of these
   as "already killed" would be a category error.

**Conclusion for (1).** The debt was **half-open** on this 8-sample, and the C1 sentence's "20 base
survivors" framing silently inherits that: under the frozen definition the self-test was blind to
all 8, so C1 closes a real self-test gap — but **2 of the 8 (n07 digest-uses-tree, n17
regex-search-to-match) were already killed at BASE by the lane's other instrument (r95 `verify`
evidence)**, i.e. the *lane* (r95+r96 together) already detected them; only **4 of 8
(n02, n14, n20, s2)** were fully open across all instruments. [INFERENCE extrapolating 4/8 to the
full 20: ~10 fully open, ~5 r95-killed, ~5 crash-killed — inference only, sample is 8/20.]
This does not make the C1 sentence false as stated (it says "makes it [the self-test] exit 1..." and
names the self-test as the instrument), but it bounds newness: roughly a quarter of the sampled
"survivors" were not lane-wide blind spots; the remaining three quarters were. A claim that these
sites were uncovered *by the lane* would be false for n07/n17; the claim as written is about the
self-test and holds. No tracker/kill-rule violation is asserted from Q1 alone; Q1 is reported as
held with the above scoping.

---

## Q2 — did any BASE file already hold the PRESS checklist questions?

Command (checked out at BASE c808 in scratch clone; same result via `git grep <rev>`):
`git -C $S/repo grep -n -F -- "<string>" c8087ac529003e667505bcc624f9a7bde0cffbce`
for five strings, receipt `.ufo/waves/round-97/w1/R97RevenPrior-q2-base-grep.txt`
(observed lines quoted below; exit codes are git-grep's).

| string | exit | observed |
|---|---|---|
| `Are there any spelling errors` | 1 (no line) | no line |
| `orphan lines` | 1 | no line |
| `Does the search strategy match the research question` | 1 | no line |
| `Boolean and proximity operators` | 0 | 14 hits — **all element-list phrases, none is a checklist question**: e.g. `corpus/knowledge/search-peer-review-dedup-r96.md:59,79,152` (the semicolon element list from the S223 abstract) and `corpus/captures/e94691f583d644da14661ec1.txt:161`, `c52a1f15884a...:1754` (unrelated prose). No hit contains the question form `Are Boolean or proximity operators used correctly?` (`git grep -n "Are Boolean"` → `exit:1`, no line). |
| `subject headings and terms in free text` | 1 | no line |

Narrower checks: `spelling errors` → exit 1; `Translation of the research question` → exit 1;
`Are there any` in the whole BASE tree → hits only an unrelated Garner 2016 line
(`.ufo/waves/round-26/build/SrcGarner2016.md:11`). `corpus/knowledge/` at BASE lists no
`press-checklist-questions-r97.md` (absent); "checklist" hits in knowledge are PRISMA-2020 Japanese/
Chinese checklists and generic prose, none PRESS-2015 question wording.

Also: the two new captures are genuinely new —
`git cat-file -e c8087ac...:corpus/captures/347c55ba9be9d63afe17986e.txt` → `fatal: ... not in 'c808...'`
exit 128; same for `80a844fe287a1a26d4280251.txt` (S226). S225/S226 registry rows absent at BASE.

**Conclusion for (2).** No BASE lane file held the PRESS 2015 checklist *questions*. The one
five-string hit (the Boolean element phrase) is the six-element list already named in the round-96
entry's first named limit as *not* the checklist's own wording — it is not a question and does not
anticipate C2. The claims' Before ("no base capture holds a line with ...") is confirmed for the two
named strings (both exit 1). **C2's newness holds** on the question wording; the element *names*
overlap by design (the round-96 debt this claim closes).

---

## Q3 — D1: does a correction row break the three TSV readers?

D1 (round-96 spot-check §5): `refetch.tsv:195` carries the J Clin Epidemiol 403 attempt
(`2026-11-09T00:36:09Z`, key `1de3fee329fc8a80be50edc6`) under id `S224`, which the registry gives
to the PRISMA-S re-open (`corpus/SOURCES.md:236`). The spot-check asks for "a correction row
(append-only) so the id names one document". plans/round-97.md records the lane's refusal:
"a correction row of a new shape has not been shown safe for all three [readers]".

### The three readers (read at F, exact behaviour)

- `tools/gate-records.py:load_refetch` — `rows = [9-col lines only]`; REFETCH check is an `any(...)`
  match. A 9-col append cannot *break* any existing record (monotone `any`); a non-9-col append is
  silently dropped.
- `tools/store-record-audit.py` — `dict(zip(HEADER, ln.split("\t")))` for every non-empty line
  (no length check), grouped by `key` (URL hash, not id). Failure rows only matter for their key.
- `tools/capture-fetch.py:read_records` — `dict(zip(HEADER, ...))`, counts per `(id,url)` against
  `MAX_ATTEMPTS = 3`. Also confirmed other readers exist beyond the three named:
  `corpus/evidence/round57/c2-count.py` (same `len==9` filter + header check),
  `tools/capture-fetch.py` itself, `corpus/evidence/round81/depth-r81.py:parse_refetch` —
  none asserts id uniqueness. **So "safe for all three" understates the reader set, but the
  shape analysis below covers the strictest of them.**

### Proposed exact shape (testable, append-only)

The J Clin Epidemiol statement has **no registry row at any revision** (S225–S227 are taken at F by
Cochrane/Karolinska/CADTH; S228 is free — `grep -c "^| S228" corpus/SOURCES.md` → 0, exit 1).
A non-colliding append-only correction must therefore be a plain 9-field row under the next free id:

```
S228<TAB>https://www.jclinepi.com/article/S0895-4356(16)00058-5/pdf<TAB>1de3fee329fc8a80be50edc6<TAB>1<TAB>2026-11-09T00:36:09Z<TAB>22<TAB>403<TAB>-<TAB>-
```

(verbatim copy of line 195 with `S224`→`S228`; key is `sha256(url)[:24]`, deterministic, so it
cannot differ). This is **not** a "new shape" — it is the existing shape, which is exactly why it
is testable. The alternative "new shape" (a 10th column, e.g. `...<TAB>CORRECTION-of-S224`) was also
tested.

### Tests (scratch COPY only; lane TSV untouched)

Baseline (lane F, unmodified):
- `python3 -B tools/gate-records.py verify --root . corpus/knowledge/search-peer-review-dedup-r96.md`
  → `GATE_RECORDS files=1 records=33 ok=33 fail=0`, exit 0
  (receipt `R97RevenPrior-d1-baseline-gate.txt`).
- `python3 -B tools/store-record-audit.py` → exit 1, `ORPHAN=3 ... STORE_BUT_RECORD_DENIES=2 ... rows=198 keys=127`
  (pre-existing FAIL; receipt `R97RevenPrior-d1-baseline-audit.txt`).

With the S228 row appended to a scratch copy (`refetch-S228.tsv`, 199 lines; scratch store copy
of `corpus/captures/`):
- audit: `python3 -B tools/store-record-audit.py --record <copy> --store <scratch-store>`
  → exit 1, `ORPHAN=3 RECORD_ONLY=0 BYTES_STALE=0 STORE_BUT_RECORD_DENIES=2 rows=199 keys=127`
  (only `rows` moves 198→199; keys 127 unchanged; all class counts identical —
  receipt `R97RevenPrior-d1-audit-S228.txt`; `diff` to baseline shows only the rows count).
- gate: fake root (`/fast/scratch/.../d1/fakeroot`, SOURCES + captures + corrected TSV):
  `python3 -B tools/gate-records.py verify --root <fakeroot> corpus/knowledge/search-peer-review-dedup-r96.md`
  → `records=33 ok=33 fail=0`, exit 0, **byte-identical** to the orig-TSV run
  (`diff` exit 0; receipts `R97RevenPrior-d1-gate-orig.txt` / `R97RevenPrior-d1-gate-S228.txt`).
- capture-fetch logic (simulated `read_records` + counts on the copy): header exact, 199 rows all
  9-col, `(S224,JCE)=1, (S224,JMLA)=1, (S228,JCE)=1` — all under the 3-attempt cap; no exception.

With the 10-col shape (`refetch-10col.tsv`):
- audit: rows=199 keys=127, classes unchanged (zip drops the 10th field;
  receipt `R97RevenPrior-d1-audit-10col.txt`).
- gate: 33/33 exit 0 (the row is dropped by the `len==9` filter;
  receipt `R97RevenPrior-d1-gate-10col.txt`). c2-count likewise sees 198 9-col rows of 199.

### The correction repairs nothing (the actual hazard)

A forged unreachable record under the *wrong* id still verifies before **and** after the append,
because REFETCH is an `any()` match over the unwithdrawn original row:
```
GATE-RECORD S224 url=https://www.jclinepi.com/article/S0895-4356(16)00058-5/pdf fetched=2026-11-09T00:36:09Z tier=A decision=reject capture=none curl_rc=22 http=403 words=0 quote=none
```
- on orig TSV: `GATE_RECORD ... S224 OK` / `records=1 ok=1 fail=0` exit 0 (`R97RevenPrior-d1-forge-orig.txt`)
- on S228 TSV: identical OK (receipt `R97RevenPrior-d1-forge-S228.txt`).
So `S224` continues to name *two* documents for REFETCH purposes — the `any()` disjunction means an
append can never subtract the wrong disjunct; and the registry still has no S228 row, so the
correction's provenance claim is itself unverifiable through gate-records (REGISTRY would fail any
S228 entry record). A 10-col "new shape" is worse: two of the readers truncate it, one drops it,
so it is *invisible* — safe only because it does nothing.

### Conclusion for (3)

The lane's stated reason — "not shown safe for all three" — is **narrowly inaccurate as a breakage
claim**: both the plain 9-field S228 row and the 10-col row were shown on scratch copies to leave
gate-records (33/33), store-record-audit (class counts) and capture-fetch counts unchanged; no tool
breaks on append. But the refusal was **necessary in effect**, for the opposite reason: neither
shape repairs the collision (the forged S224/JCE record still passes), and the 10-col shape is
silently ignored by gate-records/c2-count and truncated by the two `zip` readers, so writing it
would certify a fix that no instrument checks. Defensibly: refusing was right; the justification
should be "no append-only row withdraws the wrong `any()` disjunct and no new id is registered",
not "breaks a reader". This bears on the routed debt being *closed*, not on C1/C2 wording (D1 is
explicitly carried, not claimed).

---

## Verdicts

VERDICT: R97RevenPrior C1 held — the BASE self-test detected none of 8 sampled survivors under the frozen rule (the gap was real); 2 were already killed lane-wide by r95 verify (n07, n17) so the debt was half-open, bounding newness without falsifying the sentence as stated.
VERDICT: R97RevenPrior C2 held — no BASE file holds the PRESS 2015 checklist questions; the sole five-string hit is the element-name phrase already disclosed as not checklist wording, and both new captures are absent at BASE.
VERDICT: R97RevenPrior C1 n/a — Q3(D1) refusal was necessary in effect (neither correction shape withdraws the wrong any-match disjunct; the new shape is invisible) though not for the stated breakage reason (no reader breaks).
