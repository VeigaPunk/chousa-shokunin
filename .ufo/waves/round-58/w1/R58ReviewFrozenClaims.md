# R58ReviewFrozenClaims — freeze coherence of round-58 claims, counters, before receipts

Reviewed: corpus/evidence/round58/claims.md, c1-count.py, c2-count.py, c2/quotes.tsv,
controls/* receipts at freeze 9e73a031ab1ac3bac343de008850d7d87f9e5634; claim base
b13ca7b5c8bbb40d2d29a37fb443c64ca043f791. Read-only review; no lane file edited; no installs.
All runnable probes used unmodified copies under /fast/scratch/hyaku/chousa-r58/R58ReviewFrozenClaims/.

## Freeze identity — PASS
- `git rev-parse HEAD` → `9e73a031ab1ac3bac343de008850d7d87f9e5634` ("round-58: freeze claims and
  before controls"); `git cat-file -t` confirms both freeze and base are commits. 9e73a03 adds the
  round-58 evidence (10 files, +678) directly on base; no round-57 claim rows rewritten.
- Working tree: all tracked round58 files clean; 3 untracked under controls/
  (REFUSEALL.py, build-spans-r55.py, c1-controls.txt) — generated pre-dispatch by the frozen
  controls/build-c1-controls.py, as claims.md:25 declares. All other receipts are committed.
- Pins re-hashed this session (`sha256sum`): tools/build-spans.py
  `1ed2650a…59c80bf6` == claims.md:9 pin == `git show b13ca7b…:tools/build-spans.py` blob;
  tools/capture-text.py `2c0140bc…03e2573` == claims.md:17; captures/6dc68fd6b32ce9c8dfcebce8.raw
  `6063a3af…fddf3` == claims.md:17; controls/build-spans-r55.py `1ed2650a…` == R55 pin; receipt
  c1-control-build.txt `BASELINE_SHA256_PINNED_BYTES=` matches. Both counters bind these same bytes.

## C1 — claims.md:7-11 vs c1-count.py
- Leg inventory (claims.md:9) — PASS. Safe legs EMPTY_OK/REBUILD_OK/ESCAPE_ENTRY/HELDOUT_OK and
  refusal legs FOREIGN/SYMLINK_OUT/SYMLINK_CACHE/FIFO_TXT/DEVZERO_TXT/FAT_RAW/MANY_QUOTES appear
  exactly once each (c1-count.py:196-322) and match the claim list verbatim.
- Predicate "must print `C1=PASS` and exit 0" (claims.md:9) — **FAIL: unsatisfiable as frozen.**
  Refusal-leg pass lines are lowercase: c1-count.py:51 `PASS = "pass"`; :160 `return
  f"{name}={PASS}(refused)"`; :223 FOREIGN, :234 SYMLINK_OUT same template. But the verdict gate
  :391 is `ref_pass = all(("=PASS" in l) for l in ref_legs)` (uppercase), and the SUMMARY count
  :399 uses the same uppercase needle. Probe (verbatim frozen lines :388-394 executed from an
  unmodified copy, fed a perfect battery — 4/4 safe `=pass`, 7/7 refusal `=pass(refused)`,
  BEFORE_FOREIGN=deleted, controls 2/2 denied):
  `perfect_battery -> ok_pass: True ref_pass: False integrity: True denied_pass: True => verdict: FAIL`
  `SUMMARY REFUSE line on perfect battery: REFUSE=0/7`
  `expect_refuse` on a correctly-refusing proc returns `'SYMLINK_CACHE=pass(refused)'` etc. No
  refusal-leg line can ever contain `=PASS`, so C1=PASS is unreachable for ANY builder — the gate
  false-kills. Symptom that the verdict block was never self-tested: :389 is a dead assignment
  (overwritten at :390). A counter amendment + re-freeze is required before dispatch.
- Claim (1) foreign preserved, refusal before orphan deletion (claims.md:7) — PARTIAL. FOREIGN leg
  (:209-224) checks S777-1.txt survival, rc!=0, reason "777"/"foreign", but never checks the true
  orphan S503-1.txt created by `rows_few = rows[:2]` (:213): a builder that deletes the orphan and
  then refuses would pass. Discrimination is proven: BEFORE_BUILDER block :347-359;
  BEFORE_FOREIGN=deleted in controls/c1-before.txt:12 and c1-controls.txt:15.
- Claim (2) symlinks refused — PASS. SYMLINK_OUT :226-241 (refusal + `not any(real.iterdir())`
  target-untouched check), SYMLINK_CACHE :243-254 (SYMLINK|REGTYPE|NOT_REGULAR).
- Claim (3) FIFO/device without blocking — PASS. :255-268/:270-280 wrap runs in 20s timeouts;
  TimeoutExpired → leg FAIL, so a hang cannot yield C1=PASS.
- Claim (4) "raw reads bounded at 64 MiB" — PARTIAL. FAT_RAW (:282-295) only proves refusal of an
  80 MiB OLE-headed raw with reason SIZE. `SIZE_CAP = 64*1024*1024` (:43) is never exercised at the
  boundary and nothing measures acceptance ≤64 MiB; a builder capping at e.g. 16 MiB would pass the
  leg while contradicting the prose. Mitigated by claims.md:9 ("exact fixture and reason checks are
  frozen in the counter").
- Claim (5) "quotes.tsv bounded at 100,000 rows" — PARTIAL. MANY_QUOTES (:297-306) proves only
  refusal of 100,001 rows with SIZE|ROWS|CAP; acceptance at ≤100,000 rows is unmeasured, and reason
  "SIZE" alone satisfies the leg, so a byte cap could stand in for the row cap.
- Claim (6) containment under --out + `..` refusal — PASS. expect_ok (:114-147) snapshots files
  under the work root and fails on any change outside the out dir; ESCAPE_ENTRY (:308-320) requires
  rc!=0 and no spans.tsv. Blind spot (INFO): HELDOUT_OK runs `--cache LANE/corpus/captures`
  (:339-341), outside the snapshot root — a candidate writing into the lane store is caught only
  later by C2's RAW_PIN, not by this leg.
- Before sentence (claims.md:11) — PASS on measured parts: c1-before.txt:4 `FOREIGN=fail(rc=0,
  orphans deleted: foreign gone=True)`, :5 SYMLINK_OUT target written, :10 `MANY_QUOTES=fail(rc=0)`
  (no row cap). The prose "reads filesystem objects through Path.read_bytes() without type/size
  bounds" is characterization: the same receipt shows the base refusing FIFO/DEVZERO (wrong reason,
  rc=1) and the 80 MiB raw (`ole-malformed`) — accidental partial bounds exist. Predicate unaffected.
- Controls (claims.md:9,25) — PASS. c1-controls.txt: DENIED=2/2, CONTROL_REFUSEALL=denied,
  CONTROL_build-spans-r55=denied, C1=FAIL; REFUSEALL.py also fails all safe legs structurally.

## C2 — claims.md:13-21 vs c2-count.py / c2/quotes.tsv
- Quote set (claims.md:17) — PASS. Probe on frozen bytes: `frozen_n: 12 tsv_data_rows: 12
  malformed: 0 / quote_set_equal: True / frozen_unique: True tsv_unique: True /
  tabs_in_any_quote: False / max_quote_len: 36 all_le_36: True / urls_all_match_counter: True
  entry_all_match: True ids: ['S101']`. QUOTES list (c2-count.py:20-34) == quotes.tsv col 3, row
  order included; tsv header == counter HEADER; all 12 ≤36 chars.
- Offset binding (claims.md:17,19) — PASS as logic: :100-101 requires exactly one occurrence of the
  quote in the defined form at the declared offset, with URL+digest equal to the frozen URL/RAW_SHA;
  :85 enforces the exact set; :134 `anchors<3` implements "at least 3 line-start anchors";
  manifest header/row-count :91-95. (Runtime values unrun — no entry exists yet.)
- Entry provenance (claims.md:19) — logic PASS: trio check :55-57; registry binding :62
  (`cells[7]=='mined'`, ENTRY_REL in `cells[10]`) matches real SOURCES.md: header
  `| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |`;
  S101 row has 11 cells, status `mined`, used-by currently only
  `corpus/knowledge/citation-count-semantics-r37.md` — unbound at freeze, exactly the before-state
  receipted in c2-before.txt (`REF_ID_UNBOUND`, `ENTRY_MISSING`, `QUOTES_MISSING`,
  `MANIFEST_MISSING`, `C2=FAIL`, `EXIT=1`), matching claims.md:21.
- Stray-id (:60-61), rebuild byte-compare against the R55 pin (:115-131), substance/inference
  runners (:137-160; deps round51/quote-substance-check.py and tools/inference-ground.py exist) —
  PASS as frozen logic; consistent with claims.md:19.
- New ground (:153-154) — PASS at this base, LATENT DRIFT. :153 greps
  `載体类型标识` (traditional `載` U+8F09) at BASE `-- corpus/knowledge`, while claims.md:19
  names simplified `载体类型标识` (`载` U+8F7D). Measured: `git grep -c` at base for both variants
  → rc=1 (absent) for BOTH, and no `carrier-alphabet*` file in `git ls-tree b13ca7b --
  corpus/knowledge/` — outcome identical today. Latent: a base containing only the simplified
  token would pass "absent" while the named ground existed. Counter measures a different byte
  string than the predicate sentence.
- Controls (claims.md:19 "Controls are built in `controls/` and must fail binding"; :25 receipts
  preserved under this directory) — **FAIL (prose/receipt)**. Frozen controls/build-c2-controls.py
  builds STAGED/REWRITE control roots under caller `--work` scratch (docstring "in caller-provided
  scratch"; code copies SOURCES.md and writes entry shells there), never into controls/; and no C2
  control receipt exists under controls/ at freeze (only c1-controls.txt, c1-control-build.txt,
  c1-before.txt, c2-before.txt). The "C2 controls must fail binding" clause is UNRUN as of freeze.
  C1/C2 asymmetry: C1 controls land in controls/, C2's cannot by construction — stale claim prose.

## Findings by severity
1. HIGH — c1-count.py:391 (+ :399) uppercase `=PASS` needle vs lowercase leg strings (:51,:160,
   :223,:234): frozen C1 predicate is unsatisfiable; every hardened builder is false-killed and
   receipts would read `REFUSE=0/7 ... C1=FAIL` on a perfect run. Counter amendment + re-freeze
   needed before the C1 target can be claimed (finding, not fix — nothing edited here).
2. MEDIUM — claims.md:19 "Controls are built in `controls/`" contradicts frozen
   build-c2-controls.py (--work scratch roots); no C2 control receipt at freeze; run and receipt
   STAGED/REWRITE failures (expected C2=FAIL) before dispatch.
3. LOW — FOREIGN leg never checks true-orphan survival (c1-count.py:209-224): "refusal before orphan
   deletion" (claims.md:7) is only partially measured.
4. LOW — FAT_RAW / MANY_QUOTES measure only the over-cap side; 64 MiB and 100,000-row boundary
   acceptance unmeasured; SIZE reason alone satisfies MANY_QUOTES (claims.md:7 (4)(5) prose vs
   battery).
5. LOW — c2-count.py:153 traditional-variant grep differs from the claims.md:19 token; latent
   drift, outcome-equivalent at b13ca7b (both variants absent, verified above).
6. INFO — HELDOUT_OK cache writes sit outside the expect_ok snapshot (:339-341); dead code
   expect_ok :125-126 (`got/want`) and :389; c1-count rmtree's a pre-existing --work (:175-177).

## Residual risk / unrun (marked unrun, not failed)
- Unrun: full c1-count battery against a candidate hardened builder (none exists at freeze);
  c2-count against a completed entry; C2 STAGED/REWRITE control runs. My verdict-logic probe ran
  the frozen verdict lines verbatim but not the fixture battery end-to-end.
- C2 runtime risks outside freeze scope: anchors≥3 and byte-identical rebuild depend on the entry
  and manifest the executors produce; quotes.tsv malformed rows are silently dropped before the
  QUOTE_SET compare (c2-count.py:84), so a corrupted extra row could hide — kill rule still applies
  at integration.
- Post-fix note for L1: with :391 corrected, REFUSEALL/r55 control denial receipts remain valid
  (both fail safe legs and refusal legs regardless of case).

VERDICT: attack = freeze-time verdict-logic defect, c1-count.py:391 cannot accept the counter's own
lowercase `=pass(refused)` refusal lines, so "must print C1=PASS" (claims.md:9) is falsified as
unsatisfiable for every builder; C2 quote-set/pin/registry coherence survives review (12/12 exact,
unique, offset-bound logic, all pins re-hashed), with C2 control prose/receipt drift unfixed —
overall: C1 falsified (predicate unreachable), C2 coherent-but-incomplete (control clause unrun).
