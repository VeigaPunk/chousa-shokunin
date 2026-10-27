# R59Scribe22 — round-59 Gate / Mistakes wording, grounded in measured bytes

Seat `R59Scribe22` (scribe, leaf; axes **depth**; instance `R59Scribe22-2`, the retry of the canonical seat
recorded in `.ufo/waves/round-59/w1.ready.partial` as `"R59Scribe22": "R59Scribe22-2"`). Lane
`/home/vgpnk/Projects/shokunin/chousa-shokunin`, HEAD `af8c0a460d087cbfb8245fb9326608783ccc510b`
(`git rev-parse HEAD`), `git status --porcelain` → only `?? .ufo/waves/round-59/` and
`?? corpus/evidence/round59/`. This report is my only lane write. Scratch
`/fast/scratch/hyaku/chousa-r59/R59Scribe22/` removed before yield (`ls` → `No such file or directory`,
twice). No fetch, no install, no git/jj/index write, no spawn, no edit to any claim, counter or receipt.

Tag convention: **[OBSERVED]** = bytes I read or a command I ran in this seat · **[DERIVED]** = a static
consequence of observed bytes, not an execution · **[REPORTED]** = a sibling's result I did not re-run ·
**[INFERENCE]** = explanation consistent with the bytes but not proven by them.

Assignment as dispatched (`.ufo/waves/round-59/w1-dispatch.json` `taskCall.tasks[R59Scribe22].task`):
"Read round58 lesson and spotcheck, draft evidence-backed round59 Gate/Mistakes or report wording. No
writes except your report; do not claim checks unrun." The wave context (same object) names
`corpus/evidence/round59/claims.md` as frozen and required before work.

---

## 0. Commands run (exact, with outcomes)

```
read corpus/evidence/round59/claims.md
   → Path not found (repeated; last check 2026-10-27T18:23:59Z)
find corpus/evidence/round59 -type f -printf '%p %s\n'
   → census-start.txt 535 · controls/c1-before.txt 958   (2 files; no claims, no counter, no builder)
sha256sum corpus/evidence/round59/controls/c1-before.txt corpus/evidence/round58/controls/c1-before.txt
   → 2c9bbe5446ae4f733bf17a2836cc1b32e823fc8bc287d3da42801b948cfaebfe (both)
diff <round59 c1-before> <round58 c1-before>        → IDENTICAL
cat -n corpus/evidence/round59/controls/c1-before.txt
   → 16 lines; line 1 EMPTY_OK=pass; line 14 SUMMARY OK=4/4 REFUSE=0/7 …; line 15 C1=FAIL; line 16 EXIT=1
sha256sum corpus/evidence/round59/census-start.txt
   → 09ce4a959ddba208da141bc97e872fd5eb36fd428390a1ecf8cf741853016207  (5×W04, chousa ok, exit=0)
sha256sum corpus/evidence/round58/c1-count.py corpus/evidence/round58/c2-count.py
   → 65da18bbcb03581ca98354d90049215ed3cab3bfd3e41d483908dc1e1c703d3f (406 lines)
   → dbb859612f9d018296b217baec76a5c6cb744609b7c95372dabae4d6691c8503 (165 lines)
sha256sum tools/build-spans.py corpus/evidence/round58/controls/build-spans-r55.py
   → 1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6 (both; tree builder IS the r55 pin)
sha256sum tools/capture-text.py → 2c0140bc04029c8faedc6c89a65bd657430d8b85f433406946567b70303e2573
               corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw
   → 6063a3aff7a4081e93a685f2721e2cd6b477ba84a841211e298bcddd6d9fddf3 (both match the frozen pins)
grep -n 'PASS\|pass' corpus/evidence/round58/c1-count.py
   → :51 PASS="pass" · :147/:160/:223/:234 emitters · :315 literal pass(refused) · :377 child probe C1=PASS
     · :391 ref_pass needs "=PASS" · :398-399 SUMMARY needles
sed -n '384,402p' c1-count.py  → :389 dead assignment; :390 ok_pass "=pass"; :391 ref_pass "=PASS";
                                   :393 denied_pass; :394 verdict; :402 exit
sed -n '24,50p'  c1-count.py    → :36 HERE · :37 LANE · :40 BEFORE_BUILDER = HERE/"controls"/"build-spans-r55.py"
                                   · :42 CONTEXT=80 · :43 SIZE_CAP=64 MiB · :44 QUOTES_CAP=100_000
grep -n 'SIZE_CAP\|QUOTES_CAP' c1-count.py → :43 (definition only) and :301 (range(QUOTES_CAP+1)) — SIZE_CAP unused
grep -n 'SIZE_CAP\|QUOTES_CAP\|64 \* 1024\|100_000\|100000' tools/build-spans.py controls/build-spans-r55.py
   → no match (exit 1): neither builder has any size or row cap
sed -n '224,236p' c1-count.py   → SYMLINK_OUT: annotation "(target-dir-written!)" appended, leg not failed
sed -n '319,360p' c1-count.py   → HELDOUT_OK derives the form and requires the builder's span-start offsets;
                                   BEFORE_FOREIGN runs the r55 pin at HERE/controls/
sed -n '130,160p;118,147p' (builder/expect_ok)
   → build-spans.py:139-149 off=text.find(quote); start=max(0,off-80) written as the offset cell
   → c1-count.py:133-137 start=form.find(quote)-80; offset!=start → FAIL
python3 -B tools/capture-text.py corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw | sha256 / len
   → 27,012 chars · sha256 a8e3e7ad213b6ec50479542cda23612e7ae7ae5fd4506fba53a91f2f7e79f867
   → S101 quote `并以[文献类型标识/载体类型标识]表示` at char 797, len 19 chars, 1 whitespace word (no whitespace)
   → 12-row arithmetic over `corpus/evidence/round58/c2/quotes.tsv` (§3.4 table)
ls corpus/knowledge/carrier-alphabet-china-r58.md
   → No such file or directory; `find corpus/evidence/round58/c2 -type f` → quotes.tsv only (no manifest)
git grep -l '載体类型标识' b13ca7b5c8bbb40d2d29a37fb443c64ca043f791 -- corpus/knowledge   → rc=1 (never present)
git grep -c '文献载体标识'  b13ca7b5… -- corpus/knowledge
   → source-type-taxonomy-r36.md:1 · source-type-taxonomy-r37.md:7  (ground pre-exists at BASE)
python3 -B corpus/evidence/round58/c1-count.py --builder tools/build-spans.py \
         --work /fast/scratch/hyaku/chousa-r59/R59Scribe22/c1work3 > c1.out
   → rc=1; 15 lines; `diff` of receipt lines 1–15 against c1.out → identical; receipt line 16 EXIT=1 is an
     annotation the counter never prints
python3 -B corpus/evidence/round58/c2-count.py --root . --work /fast/scratch/hyaku/chousa-r59/R59Scribe22/c2work3
   → rc=1; 14 lines equal the committed `c2-before-frozen.txt` lines 3–16; only that receipt's command
     header (1–2) and trailing EXIT=1 (17) differ
python3 (json) over .ufo/waves/round-59/w1-spec.json and w1-dispatch.json
   → spec: 66 items, roles exec16/rev14/scr12/scout12/crit7/mt5, axes operability16/depth24/calibration26;
     66/66 spec item texts identical ("review ready handoff requirements … claims.md"); 0 item texts name
     build/falsify/control
   → dispatch: counts {"spawn":66,"resume":0,"total":66}; 66 distinct task bodies, 0/66 name claims.md;
     taskCall.context names the claims path; each task footer carries the milestone line
date -u; ls .ufo/waves/round-59/; python3 len(w1.ready.partial)
   → 2026-10-27T18:23:59Z · no w1.ready.dispatched, no w1-results.json · partial = 47 keys · 59 w1/*.md
```

Not run: `scripts/sources-census.sh`, `corpus/evidence/round51/quote-substance-check.py`,
`tools/inference-ground.py` standalone, any builder directly, any install, any fetch, any edit. The two
counter runs above are **round-58 frozen bytes executed at HEAD**, not round-59 measurements.

---

## 1. Wave and evidence state at read (moving target)

| path | state at 18:23:59Z | evidence |
|---|---|---|
| `corpus/evidence/round59/claims.md` | **absent** | `read` → Path not found; `find` → 2 files |
| `corpus/evidence/round59/census-start.txt` | 535 B, sha `09ce4a95…` | 5 W04 duplicate-URL lines (S051/S053/S073/S074/S075), `chousa ok`, `exit=0` |
| `corpus/evidence/round59/controls/c1-before.txt` | 958 B, sha `2c9bbe54…`, **byte-identical to round 58's** | `sha256sum`, `diff` |
| round-59 counter / builder / after receipt | none exist | `find corpus/evidence/round59 -type f` |
| `.ufo/waves/round-59/w1.ready` | 154 B; names lane, round, wave, dispatch path, `l1: ChousaR59` | file read |
| `w1.ready.partial` | 47 seat mappings (grew 6 → 26 → 47 during the wave) | `json.load` |
| `w1.ready.dispatched` / `w1-results.json` | **both absent** | `ls` |
| `w1-dispatch.json` | 77,324 B; `counts {"spawn":66,"resume":0,"total":66}` | `json.load` |
| `w1-spec.json` | 30,346 B; 66 items, role/axis split in §0 | `json.load` |
| `w1/*.md` | 59 reports at 18:23:59Z | `ls | wc -l` |

Consequences the Gate must carry verbatim: the frozen input the dispatch's own context names is
**absent**; the only file labelled `before` is a copy of round 58's receipt; no round-59 predicate,
counter, control or after receipt exists; and per criterion 99 (`corpus/QUALITY.md:941`) the wave is
**not reported dispatched** while `.ready.dispatched` and the results file are absent.

---

## 2. Round-58 lesson and spot-check intake, re-derived against bytes

| round-58 statement | my re-check | status |
|---|---|---|
| "frozen C1 counter cannot represent its positive state" | `PASS="pass"` (:51); every refusal emitter interpolates it (:160,:223,:234) or the literal at :315; `ref_pass` (:391) and SUMMARY `REFUSE=` (:399) search `=PASS`. No path writes `=PASS` into a leg. | **[OBSERVED+DERIVED]** |
| a builder satisfying all 11 legs still prints `REFUSE=0/7 C1=FAIL` | mechanism confirmed statically; the concrete runs are siblings' (`R58ScribeMistakeMine.md:57-83`, `R58ExecC1CounterAudit.md`; round-59 `R59Executor01/05/08/16.md`). | **[REPORTED]**, mechanism observed |
| spot-check: "C1 counter expects uppercase `=PASS` while refusal output is lowercase `=pass`" | same bytes; the precise defect is narrower than round 58's lesson wording: safe legs are matched correctly at :390, only the seven refusal legs are case-mismatched (:391,:399). | **[OBSERVED]** |
| "C2 builder span-start offsets cannot satisfy occurrence-offset binding and byte-identical rebuild" | `c2-count.py:100-108` requires `occurrences[0]==int(offset)` and span `form[off-80:off+len+80]`; rebuild :119-129 byte-compares the builder's manifest; builder writes `start=max(0,off-80)` (:142-149). | **[OBSERVED+DERIVED]** |
| SCORECARD r58: C1 and C2 `unprovable`, operability scale 3/10 unchanged, no delta | read at `SCORECARD.md` round-58 verdict block; no round-59 section exists yet. | **[OBSERVED]** |
| spot-check: S101 quote "exactly 19 whitespace-delimited words" | the quote has **19 characters**, **1 whitespace-delimited word** (no whitespace in it); at char 797 of the pinned form. The spot-check's unit is wrong; the value still fits the ≤25-word/≤160-char Gate shape. Append-only: record, do not rewrite. | **[OBSERVED]** |
| spot-check supplies the outside admit/reject sample after round-58 filing | read in full; it routes "record the external admit/reject check … in the next lesson". Round-58's lesson sentence ("No non-author admit/reject sample was available before filing") is therefore stale but stays as filed. | **[OBSERVED]**, routed |

**Read-first conclusion.** The round-58 defects are real and reproducible *as defects of the predecessor
bytes*. They are **not** round-59 claim verdicts: round 59 has no frozen claim, so nothing round-59 can be
called unprovable. The Gate must keep the two apart.

---

## 3. Independent findings from this seat's runs

### 3.1 The copied baseline is not stale — it reproduces byte-for-byte [OBSERVED]
Running the frozen C1 counter at HEAD with the tree builder reproduces `c1-before.txt` lines 1–15 exactly
(`diff` empty); the receipt's 16th line `EXIT=1` is an annotation the counter does not print. So the
round-59 file is a **copy of a still-reproducible round-58 measurement**, not a stale or edited artifact.
The provenance defect stands (it is not a round-59 measurement); the content defect is round 58's.

### 3.2 Current C2 state reproduces the frozen before-state [OBSERVED]
The frozen C2 counter at HEAD emits the same 14 body lines as `c2-before-frozen.txt` (entry missing,
manifest missing, 0/12 bound, 0/3 anchors, `C2=FAIL`, exit 1). Nothing has changed in the C2 tree since
round 58: the entry was never landed.

### 3.3 The C1 claim's *target behaviors* are absent from every builder in the tree [OBSERVED+DERIVED]
Round-58 claims items (4) "raw reads are bounded at 64 MiB" and (5) "`quotes.tsv` is bounded at 100,000
rows" (`corpus/evidence/round58/claims.md`). Measured:

- `tools/build-spans.py` and `controls/build-spans-r55.py` contain no size or row cap
  (`grep 'SIZE_CAP|QUOTES_CAP|64 \* 1024|100_000|100000'` → exit 1), and are byte-identical
  (`1ed2650a…`).
- the counter's `SIZE_CAP` is a **dead constant**: defined at `c1-count.py:43`, never read; the FAT_RAW
  leg only asks the builder to refuse with a reason containing `SIZE`.
- the FAT_RAW fixture is refused by `capture-text` as `ole-malformed: sector shift 0, mini shift 0`
  before any size test, and MANY_QUOTES returns `rc=0` on 100,001 rows.

Consequence for the Gate: even a case-repaired counter cannot produce `C1=PASS` against the tree's
builder; the round-58 "after" builder never landed. The positive path is absent at two levels — the
predicate's token and the candidate's behavior.

### 3.4 C1 and C2 impose *opposite* offset semantics on the same pinned builder [OBSERVED+DERIVED]
- C1 `HELDOUT_OK` → `expect_ok` at `c1-count.py:133-137`: `start = max(0, form.find(quote) - CONTEXT)`;
  `if offset != start: FAIL`.
- C2 `CAPTURE_BIND` at `c2-count.py:100-103`: `occurrences[0] != off → CAPTURE_BIND`.
- Both counters pin the same builder (`1ed2650a…`); `tools/build-spans.py:139-149` writes `off-80`.

So a manifest emitted by the pinned builder satisfies C1's HELDOUT leg and fails C2's bind leg; any
manifest satisfying C2 fails C1's HELDOUT leg. The two frozen counters cannot both pass in one tree.
`R59Scribe18.md` reached the same contradiction independently; this seat agrees and adds the
`expect_ok:133-137` line reference.

### 3.5 The C2 `NEW_GROUND` leg cannot detect prior ground [OBSERVED]
`c2-count.py:153` greps the mixed-script needle `載体类型标识` at BASE. That string occurs in **no file**
at BASE (`git grep -l` → rc=1; `載` appears only in unrelated Japanese entries), so the base test is
always true and the leg reduces to "the entry text contains `载体类型标识`". The ground it is supposed to
be new against is already at BASE under a different term: `文献载体标识` occurs 1× in
`source-type-taxonomy-r36.md` and 7× in `source-type-taxonomy-r37.md`. The claim's "new ground" premise is
therefore false in substance, and any entry that uses the simplified phrase passes the leg regardless.

### 3.6 C2's positive state is absent in three independent ways [OBSERVED+DERIVED]
1. entry `corpus/knowledge/carrier-alphabet-china-r58.md` does not exist → `ENTRY_MISSING`,
   `PROVENANCE_TRIO`, `REF_ID_UNBOUND`, `ENTRY_QUOTES=0/12`;
2. manifest `corpus/evidence/round58/c2/spans.tsv` does not exist (`c2/` holds only `quotes.tsv`) →
   `CAPTURE_BOUND` unreachable, `REBUILD` unreachable;
3. `ENTRY_QUOTES` requires **all 12 exact quotes inside the entry**; an entry that passes must reproduce
   the source text verbatim, which is a content-copying requirement no previous chousa entry carried.

Arithmetic over the pinned form (12 quotes, 27,012 chars, sha `a8e3e7ad…`):
`start == off` for 0/12; anchors at quote offset 3/12 (315, 330, 993); anchors at span start **0/12**.
So the anchor floor (≥3) has **zero margin** and exists only in the hand-edited shape that the rebuild
leg then rejects.

### 3.7 A counter copy is not the counter [OBSERVED+DERIVED]
`c1-count.py:40` resolves its integrity fixture as `BEFORE_BUILDER = HERE/"controls"/"build-spans-r55.py"`.
A scratch copy of `c1-count.py` without that sibling prints `BEFORE_FOREIGN=absent` instead of
`deleted` — which is exactly what `R59MutationTester63.md` reports as its "pristine" run. That report's
pristine result is therefore a **copy artifact**, and its `HELDOUT_OK=fail` is not explained by the copy
alone (its copied builder's digest is not stated). Any seat's "re-run" must name the counter path **and**
the controls directory it resolved.

### 3.8 The spec's item texts are not the dispatched task texts [OBSERVED]
`w1-spec.json` items are 66 copies of "For round 59, review ready handoff requirements. Read
…/round59/claims.md; read before work…". `w1-dispatch.json` (the file `w1.ready` names) carries 66
**distinct, role-specific** bodies; **0/66** mention `claims.md`; the wave `taskCall.context` does name it;
each task footer carries the milestone. The milestone therefore reached seats through the context/footer,
not through the item bodies, and no item body assigns anyone to *build* a control. This resolves a sibling
dispute (§7.3) without adjudicating it.

---

## 4. Draft `## Gate`

### 4.1 Precondition (blocker, not a result)
Hold, in this order:

- The wave context and the dispatch payload name `corpus/evidence/round59/claims.md` as frozen and
  required. The path is absent at 18:23:59Z (`read` → Path not found; `find` → two files). `predata/` is
  empty.
- Round-58 `claims.md` is **predecessor evidence, not a substitute**: it declares C1/C2 against base
  `b13ca7b5…` and freeze `9e73a031…`, and round 59's milestone is different.
- Consequence: **no round-59 claim is admissible and no axis may move.** The sentence is "round 59 has no
  frozen claim; nothing was tested", never "the target was tested and failed".

### 4.2 Two admissible shapes (pick one after the round settles)
1. **Claims never land** → `INPUT_ABSENT`, the `find` listing, the copied baseline with its sha, the
   reproduced round-58 verdicts labelled *predecessor*, and operability/depth/calibration
   `unchanged`/`unprovable` with **no score delta**. Positive product of the round = the calibration
   defects in §3 and the conflicts in §7.
2. **Claims land later** → the Gate must carry the claim text, its freeze commit, the exact counter path
   and sha256, and a receipt whose **first line names the revision measured** (criterion 108). A claim
   without a receipt at that revision stays unprovable.

### 4.3 What may be said about the positive verdict path *today*
- The only `before` receipt in the round is round 58's, copied byte-for-byte (`2c9bbe54…`), and it
  reproduces at HEAD (§3.1). Say "copied, and reproducible at HEAD", never "measured this round".
- The frozen predecessor predicate is unsatisfiable in three independent ways: case-mismatched credit
  token on refusal legs (`c1-count.py:51,160,391,399`); a target behavior absent from every builder
  (§3.3); and an integrity leg that resolves a sibling path (§3.7).
- The C2 predicate's three binding legs are jointly unsatisfiable on the frozen bytes (§3.4, §3.6), and
  its `NEW_GROUND` leg cannot detect prior ground (§3.5).
- No round-59 positive-control receipt exists. A future one must (i) run the exact counter bytes that will
  judge the claim, (ii) satisfy every declared leg, (iii) reach the declared final token **and** its
  success exit, (iv) be paired with a one-leg mutation that flips it, and (v) name the revision and the
  controls directory in its header.

### 4.4 Round-58 outside spot-check (record; do not rewrite round 58)
| item | decision | re-opened source | agree | reason (spot-check, verbatim) |
|---|---|---|---|---|
| S101 document-type/carrier notation | admit as source evidence only | `corpus/evidence/round58/s101-open.txt:3-6`; quote `并以[文献类型标识/载体类型标识]表示` at char 797 | agree | "Reopened the located capture; it supports only what the document states. No claim about current validity or live authority was made." |
| Present status/legal force/current use of GB3469 | reject | round-58 Gate lines 10–12; open L0 | agree | "The lesson explicitly limits evidence to the captured document and gives a reasonable flip condition …; it does not overclaim absent evidence." |

State explicitly: this sample was committed at `af8c0a4` (hyaku closure), is **post-filing** round-58
closure evidence, and must not be attributed to a round-59 seat or used to claim round-58 discernment
improvement retroactively. The quote unit is characters (19), not words (1).

### 4.5 SOURCES / census
Record the round-start census as committed: 5 W04 duplicate-URL warnings (S051, S053, S073, S074, S075),
validator exit 0; row count 133 (`grep -cE '^\|\s*S[0-9]{3,}\s*\|' corpus/SOURCES.md` → 133 at my read).
No SOURCES change is attributable to round 59 while no claim exists. No live fetch: L0 `8d77e6c1` open
(`/home/vgpnk/Projects/shokunin/.ufo/l0-questions.md`, chousa rounds 41–42).

### 4.6 Axis table the Gate must use
| axis | round-59 verdict | evidence |
|---|---|---|
| operability | **no round-59 verdict** (predecessor C1 `unprovable`; no score delta) | §1, §3.1, §3.3 |
| depth | **no round-59 verdict** (predecessor C2 `unprovable`; no score delta) | §3.4–§3.6 |
| calibration | **no round-59 verdict**; the round's only product is the defect set in §3 and §7 | §3.5, §3.7, §3.8 |

### 4.7 Gate prose to reuse (both defensible at filing time)
- "Round 59's frozen claim artifact was absent at the path its own wave context named; the round produced
  no claim verdict, and the only committed `before` receipt is round 58's, copied byte-for-byte
  (`sha256 2c9bbe54…`) and reproduced at HEAD `af8c0a4`."
- "The positive verdict path is undemonstrated at three levels: the frozen predecessor counter credits
  `=PASS` on refusal legs whose emitters can only write `=pass` (`c1-count.py:51,160,391,399`); the
  builder those legs test has no 64 MiB read bound and no 100,000-row cap (`grep` → no match; FAT_RAW
  `ole-malformed`; MANY_QUOTES `rc=0`); and the same pinned builder's offset column must be `off-80` for
  C1 (`c1-count.py:133-137`) and `off` for C2 (`c2-count.py:100-103`)."

---

## 5. Draft `## Mistakes` rows (candidate; drop rows the settled receipts do not support)

1. **vacuous — a copied receipt entered the round's evidence tree as a baseline** · Evidence: round-59
   `controls/c1-before.txt` and round-58's are byte-identical (`sha256 2c9bbe54…`, `diff` IDENTICAL);
   nothing in the file names a round-59 revision, command or builder; my HEAD run reproduces its 15
   counter lines. Captured-by: criterion 108 (a measurement citation names its receipt's revision) and
   criterion 115 (the pass token must exist in a pre-data receipt). Fix: seed a round's evidence only by
   measurement; an inherited baseline must say `COPIED FROM <round>/<path> sha256 <digest>` in line 1.
2. **unprovable — the wave was dispatched on a frozen claims path that does not exist** · Evidence: the
   dispatch `taskCall.context` and the spec context name `corpus/evidence/round59/claims.md`; `read` →
   not found; `find` → 2 files; `predata/` empty. Captured-by: criterion 99's family and criterion 14's
   freeze-before-data discipline. Fix: write the claims file (freeze commit + counter sha256) **before**
   `w1.ready`, and make the ready file name the claims path plus digest.
3. **contradiction — `w1-spec.json` and `w1-dispatch.json` disagree about what seats were told** ·
   Evidence: 66/66 spec item texts are one identical string naming `claims.md`; the dispatch's 66 task
   bodies are role-specific and 0/66 name `claims.md`; `w1.ready` names the dispatch file only. Two seats
   reasoned from different files (`R59Reviewer49` from the spec, this seat's own prompt from the
   dispatch). Captured-by: criterion 99 (report the handoff you can show) and criterion 110's dry-run
   principle. Fix: generate the spec from the dispatch, or make `w1.ready` name both and the Gate cite
   both.
4. **vacuous — the credit token is case-mismatched on the refusal path only** · Evidence: `PASS="pass"`
   (:51); safe legs match `=pass` (:390) and pass 4/4; refusal legs emit `=pass(refused)` (:160,:223,:234)
   and a literal (:315) while `ref_pass` (:391) and `REFUSE=` (:399) search `=PASS`; the verdict (:394)
   and exit (:402) are therefore always FAIL/1. Captured-by: criterion 115. Fix: parse legs as fields,
   not substrings, and require the positive token in a pre-freeze receipt. (Prefer this wording over
   round 58's "vacuous" alone: the AND-mask is the consequence, not the cause.)
5. **absent target — the claim's candidate behavior was never landed** · Evidence: round-58 claims items
   (4)/(5) against `tools/build-spans.py` (`1ed2650a…` = the r55 pin): no size or row cap (grep exit 1),
   `SIZE_CAP` defined at `c1-count.py:43` and never read, FAT_RAW refused as `ole-malformed`, MANY_QUOTES
   `rc=0` on 100,001 rows. Captured-by: criteria 86/115 applied to the candidate, not only the counter.
   Fix: freeze the candidate artifact and its digest before the counter; a claim whose target does not
   exist in the tree is not a calibration target.
6. **contradiction — two frozen counters demand opposite offset semantics from one pinned builder** ·
   Evidence: `c1-count.py:133-137` (`offset == find-80`) vs `c2-count.py:100-103` (`offset == find`);
   builder `:139-149` writes `off-80`; both pin `1ed2650a…`. Captured-by: criterion 115's "the predicate
   must be reachable", applied across the round's claim set. Fix: one column for the quote offset and a
   separate column for the span start; never derive one from the other.
7. **vacuous — the `NEW_GROUND` leg cannot detect prior ground** · Evidence: `c2-count.py:153` greps the
   mixed-script `載体类型标识`, absent from every file at BASE (`git grep -l` → rc=1), so the leg reduces
   to a substring test on the entry; the ground already exists at BASE as `文献载体标识`
   (`source-type-taxonomy-r36.md:1`, `r37.md:7`). Captured-by: criterion 86's seeded-positive-control
   principle and criterion 101's re-derivation discipline. Fix: pin the needle as the *simplified* phrase
   and assert rc=1 over a named path set, with a positive fixture that makes the leg fail.
8. **vacuous — the do-nothing control clause is opt-in and self-gated** · Evidence: `c1-count.py:365`
   `if args.controls`; the round's baseline prints `DENIED=0/0` because `--controls` was not passed;
   `c1-controls.txt` shows `DENIED=2/2` but both children are denied by the probe at :377, which tests the
   unreachable `C1=PASS`. Captured-by: criterion 115 (a deny-only set cannot prove reachability). Fix:
   require `--controls` and a `DENIED=n/n, n>0` receipt header; score a child by its declared final token
   *and* a distinct observable.
9. **unproven — hazard fixtures are refused for reasons other than the one they name** · Evidence:
   `FIFO_TXT` and `DEVZERO_TXT` fixtures are non-regular `.txt` paths; `build-spans.py:85-90` resolves them
   as "no defined text form", so the expected classes (`NOT_REGULAR`/`FIFO`/`SIZE`/`SYMLINK`) never
   appear; `FAT_RAW` is refused as `ole-malformed` before any size test. Captured-by: criterion 86 (a
   control must exercise the class it claims). Fix: make each fixture reach the guard it names, or accept
   the builder's declared reason and test *that*.
10. **unproven — a containment violation is annotated, not failed** · Evidence: `c1-count.py:232-236`
    appends `"(target-dir-written!)"` to `SYMLINK_OUT` without setting FAIL; only safe legs run the
    outside-write snapshot (`:141-146`). Captured-by: criterion 115's falsifiability. Fix: make the
    annotation a failing condition, with a mutant that writes through the link.
11. **contradiction — a copied counter silently loses its integrity leg** · Evidence:
    `c1-count.py:40` resolves the pinned r55 builder relative to `HERE`; a scratch copy prints
    `BEFORE_FOREIGN=absent`, which is exactly `R59MutationTester63.md`'s "pristine" output. Captured-by:
    criterion 110 (dry-run the recipe) and criterion 108 (name the revision). Fix: resolve fixtures from
    an explicit `--controls` path and fail loudly when it is absent.

Rows 3, 11 and 9 are this seat's additions; rows 1–2, 4–8 restate and sharpen round-58/round-59 findings
with line-level pins. None may be filed as a round-59 claim verdict.

---

## 6. Report wording constraints and reject list

Must:
- say `INPUT_ABSENT` with the exact path and the two-file listing; never "claims were reviewed";
- say the C1 baseline is **copied** (sha `2c9bbe54…`, source round 58) **and reproducible at HEAD**;
- say `unprovable` for the predecessor C1/C2 with line citations, and `no score delta`;
- keep round-58 and round-59 verdicts separate (no claim exists for round 59);
- cite QUALITY criteria by number (86 · 99 · 101 · 108 · 110 · 115) and state that 86/115 are precedent
  plus prospective rule, not round-59 results;
- record the outside spot-check as post-filing closure at `af8c0a4`, with the quote at char 797 and the
  character/word unit;
- report the wave as **not dispatched** while `.ready.dispatched`/`w1-results.json` are absent, and give
  the `counts` object read from the dispatch.

Must refuse:
1. "C1 controls pass" from `DENIED=0/0`, or from any receipt copied between rounds.
2. "C2 is satisfied" from a hand-edited manifest, or from any receipt lacking `REBUILD=MATCH` — the three
   binding legs cannot all be green on the frozen bytes.
3. "Measured at `<rev>`" without a receipt whose first line names that rev.
4. "Wave dispatched" from `w1.ready`, the spec, the dispatch, or the roster.
5. Any external-freshness or "current GB3469 status" claim (L0 `8d77e6c1` open; no fetch authorized).
6. Any numeric axis delta, or a "3/10" restated as a new measurement rather than the historical
   observables at `SCORECARD.md:2808/2838/2870` and the round-58 `unprovable` at `:2908`-block.
7. Any attribution of a sibling's scratch result as a committed round-59 receipt (59 reports exist; the
   evidence tree has two unchanged files).
8. "The dispatched items were the spec items" (they were not, §3.8), in either direction.

---

## 7. Conflicts for the canonical judge (reported verbatim; not adjudicated)

1. `R59Critic57.md:8`: "*the former lists census source URLs, not frozen claim text, and the latter
   contains only an empty line.*" Observed at the named path: `controls/c1-before.txt` is 958 B, 16 lines,
   line 1 `EMPTY_OK=pass`, 12 leg lines + `SUMMARY`, `C1=FAIL`, `EXIT=1`. It is not empty.
2. `R59Reviewer54.md:19`: "*records four duplicate-URL-across-scopes warnings (S051, S053, S073, S074,
   S075)*". Observed: five W04 lines, then `chousa ok …/corpus/SOURCES.md`, then `exit=0`. Five ids under
   the word "four".
3. `R59Reviewer49.md:13`: "*The item strings for executor, scribe, scout, and reviewer members all instead
   say “review ready handoff requirements,” … Therefore the dispatched contract does not assign the work
   named by the milestone*". Observed: that is true of `w1-spec.json`'s 66 items; `w1-dispatch.json`'s 66
   task bodies are role-specific (executor: "*inspect and run exact round58 frozen counter/tool or
   controls …*"; scribe: this seat's own wording) and none names `claims.md`; the context and each
   footer do name the claims path and the milestone. Same report, line 13 also says "*The `w1.ready`
   marker confirms a dispatch*", which criterion 99 excludes.
4. `R59Scout40.md:10`: "*`corpus/evidence/round59/controls/c1-before.txt` is a direct before-capture for
   current calibration.*" Observed: it is byte-identical to round 58's committed receipt and reproduces
   at HEAD — a copy that is *reproducible*, not a round-59 capture. `R59Reviewer54.md:13` handles the
   provenance correctly ("*The filename and content mark this as `before`*").
5. `R59MutationTester63.md:5`: "*Pristine and restored output … `HELDOUT_OK=fail`; `BEFORE_FOREIGN=absent`*"
   versus the committed receipt and my HEAD run: `HELDOUT_OK=pass`, `BEFORE_FOREIGN=deleted`. The
   `BEFORE_FOREIGN=absent` half is explained by running a copied counter without `controls/`
   (`c1-count.py:40`); the `HELDOUT_OK=fail` half is not explained by the copy alone and the report gives
   no copied-builder digest. Also note its mutant (`verdict = "PASS" if True`) demonstrates a
   false-positive path, which is consistent with the uppercase-token defect rather than independent of it.
6. `R59Reviewer49.md:13` vs `R59Scribe20.md:168-171`: the former treats `w1.ready` as dispatch
   confirmation; the latter (and criterion 99) state no dispatch is reportable without
   `w1.ready.dispatched`/`w1-results.json`. Both are on disk; the marker files are absent.

---

## 8. Not run / limits

- No round-59 counter, builder, control or after receipt exists to run; the two runs I made execute
  **round-58 frozen bytes** at `af8c0a4` in scratch and are labelled as such.
- I did not run the census validator, `quote-substance-check.py`, `inference-ground.py`, or any builder
  directly; their behaviour is cited from source lines or committed receipts, tagged accordingly.
- The form arithmetic depends on `capture-text.py` (`2c0140bc…`) and the raw capture
  (`6063a3af…`); both digests were verified before the arithmetic.
- The wave was still moving: 59 reports and 47 `w1.ready.partial` keys at 18:23:59Z. If `claims.md` or
  round-59 counters appear, every § preceded by "absent" must be re-derived before filing.
- I received one cross-seat note that foreign bytes (`positive-path/…`) exist under
  `/fast/scratch/hyaku/chousa-r59/R59Executor07/`; they are not mine, I did not create or remove them.
- Incidental: `tools/build-spans.py` docstring line 16 states the offset column is "the span start", and
  `c2-count.py` expects the quote offset — the contradiction in §3.4 is documented in the builder's own
  contract, not merely implied.

## 9. Artifacts

- This report: `.ufo/waves/round-59/w1/R59Scribe22.md`
- Bytes read (digests in §0): `corpus/evidence/round59/{census-start.txt,controls/c1-before.txt}`;
  `corpus/evidence/round58/{claims.md,c1-count.py,c2-count.py,c2/quotes.tsv,controls/*}`;
  `corpus/lessons/round-58.md`; `corpus/lessons/round-58-verifier-spotcheck.md`;
  `corpus/QUALITY.md:915,941,959,963,974`; `SCORECARD.md` round-58 block; `corpus/SOURCES.md:111`;
  `tools/{build-spans.py,capture-text.py}`; `corpus/knowledge/source-type-taxonomy-r{36,37}.md`;
  `.ufo/waves/round-59/{w1.ready,w1.ready.partial,w1-spec.json,w1-dispatch.json}`;
  `.ufo/l0-questions.md:136,140`; sibling `w1/*.md` as cited.
- Scratch (removed): `/fast/scratch/hyaku/chousa-r59/R59Scribe22/`.

## Report trailer

Relative to lane root: `.ufo/waves/round-59/w1/R59Scribe22.md`
