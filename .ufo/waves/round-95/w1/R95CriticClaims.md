# R95CriticClaims — clause-by-clause falsification of C1/C2

Seat: R95CriticClaims (critic). Attack tree C=d27e989..., freeze F=d6429e02...
Count counter binds here: every finding names the exact command, the receipt path (below) and the
observed line plus exit code. Unrun checks have not passed; deviations are findings.

Scope: for every clause of each frozen sentence in `.ufo/waves/round-95/claims.md`, name the
instrument line that enforces it or state that nothing does. Reported as enforced / partly /
unenforced, with the narrowed wording for each unenforced or partly clause.

Receipts I covered into `.ufo/waves/round-95/w1/` before yielding (all under `<seat>-*.txt`):
- `R95CriticClaims-a-dup-cases.txt`
- `R95CriticClaims-b-prior-vacuous.txt`
- `R95CriticClaims-c-warrant-gaps.txt`
- `R95CriticClaims-d-lane-and-fragments.txt`
- `R95CriticClaims-e-c2-oracle-asymmetry.txt`
- `R95CriticClaims-f-engine-divergence.txt`

Commands were run in the cloned attacked tree
`/fast/scratch/hyaku/chousa-r95/R95CriticClaims/repo` (checked out at C, `git rev-parse HEAD`
=d27e9891ba6d2bae8b1f6060f7c01bf13a1a6ea1) and in a `--shared` clone
`/fast/scratch/hyaku/chousa-r95/R95CriticClaims/stubrepo` with an asserted toplevel.
Per-lane host rules used `/usr/bin/grep` (GNU grep 3.12) wherever grep semantics mattered
(the b7 `grep` builtin shim was not used). No network, no production edits, no lane/git
mutation; the only writes are under `.ufo/waves/round-95/w1/` and scratch, both torn down
before yield.

Tooling authorization note: no installs were needed; nothing was installed via pacman/uv/npx.

## C1 `C1-RERUN-R95` (operability, capability acquisition)

Frozen sentence (claims.md §C1):

> The lane can re-run a recorded local search expression at the revision the record names and
> refuse a record whose filed count or hit set differs from what the expression finds there
> (`COUNT_DRIFT`, `SET_DRIFT`, exit 1), while reporting separately whether the current tree
> moved since that revision (`TREE_CHANGED`, exit 0 unless `--strict`). On the committed
> 8-search record every search matches at its revision; the nearest prior instrument,
> `research-gate verify-sweeps`, accepts all 8 one-cell forgeries the new tool refuses.

### C1 clause 1 — re-run at the named revision; refuse count/set drift (exit 1)

**ENFORCED** (with two narrow edges, below).

- Rev re-run: `tools/search-rerun.py:214` `run_at_rev` walks `files_at_rev` blobs via
  `git ls-tree -r -z --full-tree <rev>` (`:190`) and `git cat-file blob` (`:207`);
  rev must be a commit (`files_at_rev` `cat-file -e <rev>^{commit}`, `:187`).
- Count: `:291-292` `if len(at_rev) != r["n"]: codes.append("COUNT_DRIFT")`.
- Set (list form): `:296-297` `elif sorted(r["set"]) != at_rev: codes.append("SET_DRIFT")`;
  set comparison is a sorted-list equality against the **multiset of filed paths minus nothing**,
  i.e. `sorted(r["set"])` (with duplicates) against the distinct found list.
  Digest form: `:293-295` compares `digest(at_rev)` against the filed digest.
- Verdict/exit: `:313-314` prints `SEARCH_RERUN: CLEAN|DRIFT` and returns `0 if findings == 0
  else 1`. `findings` counts `bad = [c for c in codes if c != "TREE_CHANGED" or strict]` (`:301`).
- The battery (`rerun-controls-r95.py:99-123`) drives 8 one-cell forgeries (f1-count
  …f8-where); all refuse on their QD line (`rev=DRIFT`, expected code present) with rc=1.
- **Prompt's named probe — a `hit_set` listing a path twice IS refused.** I built a Q4
  variant whose `hit_set` lists `corpus/captures/62be15a474e866e4bef6c9d5.txt` twice while
  `hits` stays 1 (`receipt: R95CriticClaims-a-dup-cases.txt`). Observed line:
  `SEARCH_RERUN Q4 rev=DRIFT tree=SAME recorded=1 at_rev=1 at_tree=1 SET_DRIFT`, rc=1.
  The same variant with `hits` forged to 2 (matching `len(r["set"])` incl. the duplicate)
  is also refused: `COUNT_DRIFT,SET_DRIFT`, rc=1. `sorted(r["set"]) != at_rev` catches every
  duplicate because `at_rev` cannot contain duplicates (one entry per repo path). A `./`-prefixed
  path and a case-changed path are refused the same way (`SET_DRIFT`, rc=1). So the naive
  "count is right but set has a duplicate" hole does not exist: `COUNT_DRIFT` compares
  `len(at_rev)` against the **filed `hits`**, not against `len(set)`, while `SET_DRIFT`
  compares the filed multiset against the found set — a duplicate fails the latter regardless.

Edges where clause 1 says more than the instrument (partly):

**(E1) A duplicate-in-list is only a hole in the digest form's favor, by design.** For Q1 and
Q5 the `hit_set` is a digest over `sorted(paths)`; the digest form has no per-path content to
dupe. The claim's "hit set differs" is honored: a wrong digest compares unequal
(`SET_DRIFT`, covered by forgery f4). No defect, but the claim does not distinguish the two
filed forms; a reader could mistake the digest form for a stronger guarantee than it is
(a one-way hash proves set equality, not enumerability). No narrowing needed for a *falsification*
— the wording is true of both forms.

**(E2) Expression bytes are not verified — only their consequences.** A forged `expression`
whose count/set happen to coincide with the filed ones passes (`expr-space`: `` `exactly as
run ` `` with trailing space, rc=0, `rev=MATCH`). The sentence only promises to refuse
records whose count/set *differ*, so this is out of scope as written; but the C2 decision row
("the record's `expression` cell holds the bytes the engine ran") is **NOT** enforced by this
instrument at all (see C2). C1's sentence is faithful to the instrument here; the overclaim
lives in C2.

**(E3) PCRE/Python `re` divergence produces spurious COUNT_DRIFT, not a setup refusal.**
`tools/search-rerun.py:133-137` compiles regex rows with Python `re`; the record (per
`corpus/fixtures/search-rerun-r95.md:9-18`, `NAMED LIMIT (a)`) was produced with GNU
grep 3.12 `-P`. On the 8 committed expressions the two engines agree (Q6/Q8 verified identical
under both; receipt `R95CriticClaims-f-engine-divergence.txt`). But on a PCRE-only expression
(e.g. `` `\QPRISMA-S\E` `` — valid for `grep -P`, `re.error: bad escape \Q` for Python) a
truthful record (filed counts from the actual `grep -P` run) is refused with
`COUNT_DRIFT,SET_DRIFT` rc=1 (`at_rev=0`). Inverted: `\p{Letter}…` is the same. Conversely
`(?>…)` atomic groups happen to compile in Python 3.11+ and agree on this fixture's hit sets,
so there is no setup error `EXPRESSION`. So the sentence's "what the expression finds" is
engine-relative; the claim names the divergence in `NAMED LIMIT (a)` ("agreement measured on
these 8 expressions only") but the **sentence** does not carry the engine qualifier, while the
predicate (fixed 8-expression record) does. Verdict: **partly** — narrow the sentence:
"refuse a record whose filed count or hit set differs, under the Python `re` engine, from what
the expression finds there".

### C1 clause 2 — separate `TREE_CHANGED` reporting, exit 0 unless `--strict`

**ENFORCED.** `run_on_tree` (`:260-271`) walks disk files under each glob's static dir via
`tree_files` (`:239-257`, symlink on the path refused as `WHERE_TYPE`), `changed =
at_tree != at_rev` (`:298`), `TREE_CHANGED` is excluded from `bad` unless `strict` (`:301`),
so exit is 0 on tree-movement alone and 1 under `--strict`. Live check at C: bare verify
prints 5× `TREE_CHANGED … tree=CHANGED` and exits 0; with `--strict` exits 1 with only
`TREE_CHANGED` codes (battery: `CASE strict-tree rc=1 … codes=['TREE_CHANGED'] ok`). Also
covered in a `--shared` clone with one edited capture (`clone-edit rc=0/1 … ok`).

Note: "the current tree" means **disk files (tracked or not)** under the globs' static
directories (named limit (c), invoked only offline). The sentence's "moved since that revision"
is accurate under that reading; a commit that only changes files outside every glob's static
dir yields `SAME` — leave as is.

### C1 clause 3 — every search on the committed 8-record matches at its revision

**ENFORCED.** `SEARCH_RERUN_SUMMARY searches=8 rev_match=8/8 tree_same=3/8 findings=0` +
`SEARCH_RERUN: CLEAN`, rc=0 (at C, receipt `corpus/evidence/round95/after/c1-verify.txt`;
and the positive case in the battery checks the substring `rev_match=8/8` plus rc=0 and the
CLEAN line). All 8 lines read `rev=MATCH`. Note that 5 of 8 also read `tree=CHANGED` — the
positive does not require tree sameness, matching the sentence.

### C1 clause 4 — "the nearest prior instrument, `research-gate verify-sweeps`, accepts all 8
one-cell forgeries the new tool refuses"

**PARTLY (true as a verdict, vacuous as "acceptance of a forgery").**

- `verify-sweeps` on the real record and on every forged copy returns
  `VERIFIED_SWEEPS=0/0 REJECTIONS_OK=0/0` / `RESEARCH_GATE: CLEAN`, rc=0 (`R95CriticClaims-b-prior-vacuous.txt`,
  first battery block `CASE prior-f1-count … rc=0 expect=0 ok`). So the battery's
  `PRIOR_ACCEPTED=8/8` is literal: the **verdict** for every forged record is CLEAN/exit 0.
- **But** the record contains no `## Sweeps` section, so the prior **examined nothing** —
  `sweeps=0 verified=0` in every verdict line. The mode's own contract is in
  `tools/research-gate.sh:133-134` / `:2683` "sweeps mode: kept rejections + negative sweeps
  (local re-runs only)" — it re-runs **negative-sweep globs for emptiness** and rejection
  rows, and only those. A record with a planted `## Sweeps` local glob that hits DOMINATES
  the same mode (the self-test `sweeps-fail-planted-hit`, `research-gate.sh:5469-5488`, yields
  `DRIFT`, rc=1). So `verify-sweeps` *would* refuse a forgery that spoke its language;
  the 8 one-cell `## Searches` forgeries never speak it.
- "Nearest" claim: I read every `tools/` header (19 Python tools + `research-gate.sh`).
  `gate-records.py` verifies GATE-RECORD quotes, not searches; `store-record-audit.py`
  verifies store/record bytes; `absent-split.py`/`quarantine-check.py` locate quotes;
  `inference-ground.py` checks citations; `build-spans.py` builds span manifests;
  `claims-audit{,-v2}.py` checks self-assessment statements; `lane-preflight.py` is a
  meta-runner. **None re-executes a recorded search expression and compares its count/set.**
  `verify-sweeps` is the only prior that **re-runs a recorded glob set** (for emptiness),
  hence nearest in *mechanism*. The claim does not claim verify-sweeps *had the opportunity*
  to see these forgeries — only that it "accepts" them. Under the battery's operational
  definition (rc=0 + CLEAN line) the sentence is **true**, so this is not a falsity.
  However the word "accepts" will be misread by a verifier as "examined and passed them".
  Recommended narrowing (not a kill): "…returns `CLEAN` (exit 0) on all 8 one-cell forgeries
  without examining the `## Searches` table (`sweeps=0/0`)". With that qualifier the clause
  is enforced by the battery; as frozen it is **partly** because the instrument enforces
  the verdict, not the interpretation.

### C1 kill rules K1–K4 vs the instrument

- K1 predicate unmet at landing — measured at C: both predicates print the frozen lines with
  rc=0 and `tree_equals_F_for_measured_paths=yes` (receipts F-vs-C diff clean, rc=0 diff).
- K2 forgery accepted / positive refused — every way a count can differ *is* refused by
  design-and-probe (above). One more divergence channel I probed: a `where` like
  `corpus/captures/**/*.txt` matches the same 1 file on this record and passes `rev=MATCH`
  (`star-star` probe, rc=0) — correct: the recorded count/set do not differ under the filed
  glob's *Python `full_match`* semantics, while the recorded `where` glob came from a shell
  glob where `**` behaves differently. This is the same engine-relative qualifier as (E3):
  the refusal promise is relative to the instrument's glob semantics, not the recorder's shell.
- K3 writes/socket/out-of-root read (incl. symlinks) — **UNENFORCED by the battery's cases**
  (no write/socket case; the clone-symlink case covers the symlink half only). The code
  itself is read-only (`git ls-tree`/`cat-file`, `open(..., "rb")`, no `write`, no `socket`
  import in `tools/search-rerun.py`), so the *property* holds but nothing in the recorded
  predicate would catch a regression that added a write. Enforcement is code-inspection-only.
- K4 source-blind stand-ins — `ORACLES_REJECTED=3/3` (constant-CLEAN fails 4/4 groups,
  count-only fails `FORGERY` 4/8, rev-blind fails `POSITIVE`/`STRICT_TREE`/`FORGERY` 0/8 and
  more). Re-ran to confirm (`RERUN_CONTROLS=PASS`). This is indeed how a constant passes
  the old counters but not this one.

### C1 do-nothing control on its own counter

The battery's do-nothing (tool absent at base → rc=2, no CLEAN line) proves the *predicate*
is not vacuous against an empty tree. A forcing stand-in control — a "count-only" oracle that
ignores sets — is present (K4 group) and fails `FORGERY` 4/8. And the prior tool on the same
counter scores `FORGERY_REFUSED=0/8` if swapped in (it accepts all 8). So the claim **beats a
do-nothing on its own counter**: no contract-satisfying stand-in passes `POSITIVE=1/1 +
FORGERY_REFUSED=8/8 + SETUP_REFUSED=12/12` simultaneously; I confirmed the cheap
constant-CLEAN/count-only/rev-blind controls all fail (receipts in `c1-controls.txt`).
The do-nothing group is honest, not a straw person.

VERDICT layout:
- C1 sentence = enforce**d** on clauses 2,3; **partly** on 1 (engine-relative qualifier missing);
  **partly** on 4 (vacuous acceptance — verdict true, examination false).
- No clause is false as measured: duplicate path refused; every counted difference refused;
  PRIOR_ACCEPTED is verdict-true. I do **not** fire C1's predicate numbers, but "nearest prior
  instrument … accepts" and "refuse … what the expression finds" both need the narrowings above.

## C2 `C2-ENTRY-R95` (depth)

Frozen sentence (claims.md §C2):

> The lane holds `corpus/knowledge/search-rerun-record-r95.md`, whose 7 decision rows are each
> warranted by located quotes of PRISMA-S (`S222`, opened this round): all 9 quotes are
> located (gate-records normalization) in the committed `.txt` capture of the publisher PDF,
> the Located-quotes table equals the 9 `GATE-RECORD` quotes one-to-one, and each row's
> `Lane` column is marked as the lane's reading, not a PRISMA-S requirement.

### C2 clause 1 — the lane holds the entry

**ENFORCED** (file committed at F and C; `git diff --quiet F C` over measured paths rc=0).
`verify-metadata` reads the header (`source: S222`, `verified-at: 2026-11-08`,
`recheck: on-release`) — `METADATA_COMPLETE=1/1`, `RESEARCH_GATE: CLEAN`, rc=0
(`c2-metadata.txt`).

### C2 clause 2 — 7 decision rows each "warranted" by located quotes

**UNENFORCED — the central overstatement.** What the instrument actually proves:

- `entry-controls-r95.py:56-63` `bindings()` reads the `## Decision table`, takes **only the
  `Warrant` cell** (`cells[3]`), extracts `re.findall(r"\bQ[0-9]+\b", cells[3])`, and counts a
  row OK iff it names ≥1 qid and every named qid is a Located-quote row. It never reads the
  `Do`/`Never`/`Situation`/`Lane` cells, never checks the quote text says what the `Do` says,
  never checks the named qid is the *right* quote. So `WARRANTS_OK=7/7` proves **"each row
  names an existing qid"**, not "each row is warranted by the quote that qid holds".
- **I demonstrated both directions** (`R95CriticClaims-c-warrant-gaps.txt`):
  (a) replacing the first row's `Do` ("file the strategy … exactly as run") with
  "DELETE EVERYTHING and burn the archive" keeps `WARRANTS_OK=7/7`, `LQ_BOUND=9/9`,
  `records=9/9`, **and** `gate-records.py verify` still `records=9 ok=9 fail=0` rc=0 —
  because gate-records only inspects the `GATE-RECORD` lines.
  (b) changing the first row's Warrant from `Q1` to `Q5` (a limits quote) for a row that is
  really about item-8 "exactly as run" keeps `WARRANTS_OK=7/7` — the instrument cannot tell
  the quote is the wrong one.
- **The claim's own named limit (b)** concedes this: "the instruments check that a warrant
  exists, not that the paraphrase is faithful — that is the wave's reviewer item." So the
  **freeze acknowledges the sentence is not fully instrumented**, but the **sentence** still
  says "each warranted by located quotes". Reviewer breaks the tie, not the counter. Kill
  rule K2's remedy ("the row is narrowed or withdrawn, and the count in the sentence changes
  with it") is likewise not mechanised by any of the three instruments in the predicate.
- Narrowed wording (required): "whose 7 decision rows **each name a located-quote qid** from
  the Located-quotes table (semantic warrant — whether the named quote actually supports the
  `Do`/`Never` wording — is a reviewer check, not an instrument check)".

### C2 clause 3 — all 9 quotes located (gate-records normalization) in the .txt capture

**ENFORCED.** `tools/gate-records.py:207-271` `check()`: word count == `words=`
(`WORDS`), 1≤n≤25 (`QUOTE_LEN`), tier vs registry (`TIER`), capture path/key/sha-256 and a
`refetch.tsv` row with matching `sid/url/key/fetched/curl_rc/http/capsha` (`REFETCH`),
and — the location proper — lines 241-245: `norm(quote) in norm(capture_text)`, where
`norm()` (`:92-94`) maps curly quotes → straight and collapses whitespace.
`records=9 ok=9 fail=0`, rc=0 (`c2-gate.txt`). I forked a copy with Q6's inner quotes
removed (`to view the same "slice"...` → `to view the same slice...`) and got
`FAIL QUOTE_ABSENT` for exactly that record (`records=9 ok=8 fail=1`, rc=1) — proving the
check is a real substring check against the capture bytes, not a count echo. The capture file
sha256 is `86f1aacd…` (the committed `capture_sha256` in each GATE-RECORD, verified by
`sha256_file`). The capture key is `sha256(url)[:24]` and matches the filename
(`1a8c36c4c24444967bd9c3ce`). A whitespace-collapse forgery (`copied  and  pasted…`) still
passes `records=9 ok=9` — inside the normalisation the claim **names** ("gate-records
normalization"), so this tolerance is disclosed, not hidden.

### C2 clause 4 — Located-quotes table equals the 9 GATE-RECORD quotes one-to-one

**ENFORCED as multiset equality; PARTLY as correspondence.** `bindings()` (`:49-55`) takes
the multiset of the 9 `quote="…"` strings from the GATE-RECORD lines and checks that each
of the 9 LQ-table strings appears in that multiset once (`bound=9`, `len(lq)==9`,
`len(recs)==9`, `not pool`). `LQ_BOUND=9/9`. Two under-determination points that are latent
here but *inactive on this entry* (all 9 quotes distinct strings):

- Because it is multiset equality, **swapping the LQ texts of Q1 and Q2** leaves
  `LQ_BOUND=9/9` and `WARRANTS_OK=7/7` intact (`R95CriticClaims-c-warrant-gaps.txt`) — the
  instrument cannot see a qid↔quote permutation. The claim's "one-to-one" is true at the
  string-multiset level but **not enforced per-qid**; if a future entry permuted two LQ
  rows, the rows' warrants would then name the *wrong* quotes and nothing would fire. On
  *this* committed entry the mapping is correct (spot-read all 9), so the *statement* is
  true today; the **instrument** does not prove the per-qid direction.
- Adding a 10th LQ row without a GATE-RECORD is refused (`bound == len(lq) == len(recs)`
  fails — verified probe C), so the table cannot silently outgrow the gate set. Symmetric
  deletion is caught by the same invariant plus `records=9`.
- Narrowed wording: "…the Located-quotes table's 9 quote strings are the same **multiset**
  as the 9 `GATE-RECORD` quotes (per-qid correspondence verified by reading, not by the
  binding counter)".

### C2 clause 5 — each row's `Lane` column marked as the lane's reading, not a PRISMA-S
requirement

**UNENFORCED by any instrument; enforced by the entry's prose only.** `bindings()` never
reads the `Lane` cell; `gate-records.py` never reads the entry at all except its GATE-RECORD
lines; `verify-metadata` reads only the Markdown header (`source`/`verified-at`/`recheck`).
I emptied a Lane cell — `gate-records` stays `records=9 ok=9 fail=0`, `bindings` still
`WARRANTS_OK=7/7`, `LQ_BOUND=9/9` (`R95CriticClaims-d-lane-and-fragments.txt`). The marking
rests solely on (i) the entry's own sentence (§"What this entry governs": "The column marked
*lane* is this lane's reading for a local, committed corpus; it is not a PRISMA-S
requirement." — note it is rendered as a *description of* the italicised word, not machine-checked),
and (ii) every row's Lane cell being non-empty and phrased as the lane's implementation.
The sentence "each row's `Lane` column is marked as the lane's reading" is a property of
the prose a reader approves, not of the counter. Narrowed wording or an additional counter is
needed: the predicate as frozen does not check any `Lane` content, so the clause is
**unenforced** — the strongest honest form is "the Lane column is described in the entry's
prose as the lane's reading (a reviewer checks each cell is so phrased; no instrument reads them)".

### C2 kill rules K1–K3 vs the instrument

- K1 predicate unmet — measured at C: `GATE_RECORDS … records=9 ok=9 fail=0`,
  `METADATA_COMPLETE=1/1`, `ENTRY_CONTROLS=PASS`, all rc=0 (receipts `c2-gate.txt`,
  `c2-metadata.txt`, `c2-controls.txt`).
- K2 Do/Never asserting more than its warranting quote — **UNENFORCED** (see clause 2):
  the counterexample above (nonsense `Do` passing `gate-records` + both bindings rc=0)
  is exactly the construct K2 is meant to catch, and it passes every instrument in the
  predicate. The claim's named limit (b) is the admission; the sentence omits the admission.
- K3 a quote located only by joining text across the two text-form columns —
  **PARTLY**. The material risk is the genuine two-column case (Q7–Q9 are three column-line
  fragments of one sentence, lines 22-24 and 59: "their joining is read from the layout").
  The battery's `g2-column-join` forges the natural wrong join
  (`"If a reader tries to duplicate a search from a systematic review"`) and refuses it with
  `QUOTE_ABSENT`, rc=1; I independently confirmed the joined string is ABSENT from the
  normalised capture text, so K3 has teeth on the committed case. But the enforcement is
  exactly one forgery shape ("cross-column join" = concatenate *this* sentence's neighbours);
  a different join (second column's line interleaved mid-phrase) is refused only insofar as
  it still fails substring search — which is the same `norm(quote) in norm(text)` test, so
  all joins are in fact refused (any join produces a string not present on one column-line).
  Verdict: partly because the battery names one instance while the underlying check is general;
  the sentence is fine as measured now, and K3's remedy in the entry (each fragment located
  "on its own" per the 22-24 note) is respected by every forge I tried.

### C2 do-nothing control on its own counter (and a gap in the battery)

The battery's DO_NOTHING (entry absent at base → `gate-records` rc=2) proves the predicate
is not vacuous against an empty tree, and g8 (`records=0`) proves a sourceless copy of the tables
fails. But the C2 battery, unlike C1, has **no `ORACLES` group**: a cheap
"constant-CLEAN" `gate-records` stand-in should fail `FORGERY_REFUSED`. I tested this on a
clone where `tools/gate-records.py` was replaced by a constant `records=9 ok=9` printer:
`POSITIVE=1/1 FORGERY_REFUSED=0/8 DO_NOTHING_REFUSED=0/1 GATE_RECORDS=9/9 LQ_BOUND=9/9
WARRANTS_OK=7/7 METADATA=clean, ENTRY_CONTROLS=FAIL` (`R95CriticClaims-e-c2-oracle-asymmetry.txt`).
So the counter **does** reject the stand-in — but **no case inside the frozen battery
demonstrates it** (C1's battery has three oracles, C2's has none; the constant-CLEAN outcome
above is from my out-of-battery probe). This is an asymmetry of *evidence*, not of outcome,
and worth a post-freeze addition to the battery rather than a kill. On its own counter the
claim still beats a do-nothing/cheap control (a lookup-table stub that always prints the
predicate lines scores `FORGERY_REFUSED=0/8`).

## Cross-claim notes (sward, not findings)

- The tree at C equals F on every measured path (`git diff --quiet F C -- <measured paths>`
  rc=0); the 5 after-receipts were emitted at F. Predicate lines match the in-repo receipts and
  my fresh runs (`RERUN_CONTROLS=PASS`, `ENTRY_CONTROLS=PASS`, rc=0 both).
- `corpus/lessons/round-95.md` (cited by the plan as the D3 Gate record carrier) does not exist
  at C (`git cat-file -e …:corpus/lessons/round-95.md` → fatal, rc=128) — but it is **not** in
  either predicate or either sentence, so it is not a finding against C1/C2. Noted for the
  round-close (plan §D3 debt), not for the two shapes.
- `tools/research-gate.sh` and `tools/gate-records.py` are byte-unchanged F→C (per above
  diff), as claimed.

## Bottom line

- **C1**: predicate numbers hold. Two clauses are **partly** rather than falsely stated:
  engine-relativity (E3) and vacuous prior acceptance. The duplicate-path probe the
  assignment asked for shows the feared hole does **not** exist — `SET_DRIFT` catches it.
- **C2**: three of five clauses **unenforced or materially stronger than the instrument**:
  (2) semantic "warranted" is a qid-existence check (faired by the claim's own named limit but
  stronger in the sentence); (4) one-to-one is multiset equality (qid-permutation blind);
  (5) `Lane`-marking is prose, unread by every instrument. Kill rule K2 is **unenforced** by
  the predicate: a nonsense-`Do`, wrong-qid entry passes `gate-records` and both bindings
  with rc=0.

VERDICT: R95CriticClaims C1 held — every counted difference is refused (duplicate set included), predicate numbers re-run clean, but the sentence should be narrowed to name the Python-re engine and the prior's vacuous acceptance.
VERDICT: R95CriticClaims C2 fired — "7 decision rows are each warranted" and the Lane-marking clause say more than any instrument checks (WARRANTS_OK is qid-existence; a nonsense-Do/wrong-qid entry passes all counters rc=0).
