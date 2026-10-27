# R59Scribe25 — round-59 Gate/Mistakes draft from the round-58 lesson and spot-check

Seat `R59Scribe25`, role scribe, axis depth, leaf (no dispatch, no fetch, no installs).
Lane root `/home/vgpnk/Projects/shokunin/chousa-shokunin`; HEAD `af8c0a460d087cbfb8245fb9326608783ccc510b`
(`round-58 verifier spot-check (integrator, hyaku): non-author admit/reject`).
Read first, as assigned: `corpus/evidence/round59/claims.md` — **absent** (see §1.1); then the round-58
lesson `corpus/lessons/round-58.md` and the round-58 verifier spot-check
`corpus/lessons/round-58-verifier-spotcheck.md`. My only write is this report. Nothing frozen was
touched; no claim, counter, control or source row was altered.

Scratch `/fast/scratch/hyaku/chousa-r59/R59Scribe25/`, removed at the end of this seat (§6).

## 1. What I ran (exact, observed)

### 1.1 Freeze precondition

```
ls corpus/evidence/round59/            → census-start.txt, controls/          (no claims.md)
ls .ufo/waves/round-59/                → w1.ready, w1.ready.partial, w1-dispatch.json,
                                         w1-spec.json, w1/, predata/ (empty)
find corpus/evidence/round59 .ufo/waves/round-59 -name '*claim*' -o -name '*count*' -o -name '*.py'
                                       → no matches
git ls-files corpus/evidence/round59 .ufo/waves/round-59   → empty
git status --porcelain --untracked-files=all corpus/evidence/round59
                                       → ?? corpus/evidence/round59/census-start.txt
                                         ?? corpus/evidence/round59/controls/c1-before.txt
git rev-parse HEAD                     → af8c0a460d087cbfb8245fb9326608783ccc510b
git ls-tree -r --name-only HEAD corpus/evidence/round59 .ufo/waves/round-59   → (no output)
```

There is no round-59 claims file, no round-59 counter (`c1-count.py`/`c2-count.py`), no round-59
quote manifest, and no freeze commit id. Round 58 had all of these before its wave
(`corpus/evidence/round58/claims.md`, `c1-count.py`, `c2-count.py`, `c2/quotes.tsv`, freeze
`9e73a031ab1ac3bac343de008850d7d87f9e5634`).

### 1.2 Plan record vs dispatch record

```
jq '.items|length' .ufo/waves/round-59/w1-spec.json                       → 66
jq -r '.items[].item' … | sed report-path→REPORT | sort -u | wc -l        → 1     (one body for all 66)
jq -r '[.items[]|select(.item|test("round59/claims\\.md"))]|length'       → 66    (all name the absent file)
jq '.taskCall.tasks|length' .ufo/waves/round-59/w1-dispatch.json          → 66
jq -r '.taskCall.tasks[].task' … | sed scratch/report-path→TOKEN | sort -u | wc -l  → 16
jq -r '[.taskCall.tasks[]|select(.task|test("round59/claims\\.md"))]|length' → 0
jq -r '[.taskCall.tasks[]|select(.task|test("claim"))]|length'            → 50
jq -r '[.taskCall.tasks[]|select(.task|test("round58"))]|length'          → 33
jq -r '[.taskCall.tasks[]|select(.task|test("round59"))]|length'          → 45
jq -r '[.taskCall.tasks[]|select(.task|test("author|create|write the|draft the|add a";"i"))]|length' → 0
jq '.counts'                                                              → {"spawn":66,"resume":0,"total":66}
```

Dispatched seat census (16 distinct bodies, by role): 16 executor ("inspect and run exact round58
frozen counter/tool or controls"), 14 reviewer ("Adversarially assess round59 claim design…"),
12 scribe ("Read round58 lesson and spotcheck, draft…"), 12 scout ("Read lane artifacts/captures
offline…"), 7 critic ("Try to falsify a proposed round59 claim/control/counter"), 5 mutation-tester
("Mutation-test exact round58/59 counter or claimed rule"). Zero dispatched tasks author a round-59
claims file, counter, control or quote manifest; every non-scribe body says "No edits"/"Never edit
lane files".

```
stat -c '%y %n' …
  w1-dispatch.json      2026-10-27 15:12:11.20
  w1.ready              2026-10-27 15:12:15.13
  census-start.txt      2026-10-27 15:12:21.54
  controls/c1-before.txt 2026-10-27 15:14:30.64
  w1-spec.json          2026-10-27 15:14:46.65
  w1.ready.partial      2026-10-27 15:17:14.44   (contains 6 executor names only)
cat .ufo/waves/round-59/w1.ready
  {"lane":"chousa","round":59,"wave":"w1","dispatch":"…/w1-dispatch.json","l1":"ChousaR59"}
```

`w1.ready` names no claims path and no digest; it was written before `w1-spec.json` existed.

### 1.3 The only round-59 control artifact

```
sha256sum corpus/evidence/round58/controls/c1-before.txt corpus/evidence/round59/controls/c1-before.txt
  → 2c9bbe5446ae4f733bf17a2836cc1b32e823fc8bc287d3da42801b948cfaebfe  (round58)
    2c9bbe5446ae4f733bf17a2836cc1b32e823fc8bc287d3da42801b948cfaebfe  (round59)
diff … → identical; size 958 B
```

Round-59 `controls/c1-before.txt` in full: `EMPTY_OK=pass`, `REBUILD_OK=pass`,
`FOREIGN=fail(rc=0, orphans deleted: foreign gone=True)`, `SYMLINK_OUT=fail(rc=0, expected
refusal)(target-dir-written!)`, `SYMLINK_CACHE=fail(rc=0, expected refusal)`, three refusal legs
failing on an absent diagnostic (`FIFO_TXT`, `DEVZERO_TXT`, `FAT_RAW`), `MANY_QUOTES=fail(rc=0,
expected refusal)`, `ESCAPE_ENTRY=pass(refused)`, `HELDOUT_OK=pass`, `BEFORE_FOREIGN=deleted`,
`DENIED=0/0`, `SUMMARY OK=4/4 REFUSE=0/7 …`, `C1=FAIL`, `EXIT=1`. No command line, no counter path,
no pin, no `--controls` set.

By contrast `corpus/evidence/round58/controls/c1-controls.txt` line 1 is, verbatim:
``Command: `python3 corpus/evidence/round58/c1-count.py --builder tools/build-spans.py --work
/fast/scratch/hyaku/chousa-r58/c1-controls-final --controls corpus/evidence/round58/controls` (exit 1
expected: base candidate fails)``
and its tail closes `DENIED=2/2` with `CONTROL_REFUSEALL=denied`,
`CONTROL_build-spans-r55=denied`. So the round-59 receipt is the **no-controls** variant: the two
do-nothing controls were not run in round 59, and no invocation is recorded.

### 1.4 Pins I re-measured (read-only)

```
sha256sum corpus/evidence/round58/c1-count.py → 65da18bbcb03581ca98354d90049215ed3cab3bfd3e41d483908dc1e1c703d3f
sha256sum corpus/evidence/round58/c2-count.py → dbb859612f9d018296b217baec76a5c6cb744609b7c95372dabae4d6691c8503
sha256sum tools/build-spans.py                → 1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6
sha256sum tools/capture-text.py               → 2c0140bc04029c8faedc6c89a65bd657430d8b85f433406946567b70303e2573
sha256sum corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw
                                              → 6063a3aff7a4081e93a685f2721e2cd6b477ba84a841211e298bcddd6d9fddf3 (129,024 B)
grep -n 'PASS' corpus/evidence/round58/c1-count.py
  51:  PASS = "pass"
  160: return f"{name}={PASS}(refused)"
  391: ref_pass = all(("=PASS" in l) for l in ref_legs)
  394: verdict = "PASS" if (ok_pass and ref_pass and integrity and denied_pass) else "FAIL"
  399: f"REFUSE={sum('=PASS' in l for l in ref_legs)}/{len(ref_legs)} "
```

The builder and both tool pins are unchanged from round 58. The frozen counter still mixes a
lowercase leg vocabulary (`PASS = "pass"`) with an uppercase aggregate search (`"=PASS" in l`), so
`ref_pass` cannot be true for refusal legs printed as `=pass(refused)` — the positive verdict path
is unreachable in the frozen bytes at the round-59 tip, by inspection of lines 51/391/394/399 alone.

### 1.5 Offline source re-derivation at the round-59 tip (no fetch)

```
python3 -B tools/capture-text.py corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw  (twice)
  → 27,012 chars both runs; cmp clean; form sha256
    a8e3e7ad213b6ec50479542cda23612e7ae7ae5fd4506fba53a91f2f7e79f867 (both runs)
12 rows of corpus/evidence/round58/c2/quotes.tsv located in that form:
  count 1 each (12/12 unique); offsets
  315, 330, 590, 683, 734, 781, 797, 838, 965, 993, 1460, 11723
  line-start: 315, 330, 993  (3/3 = the frozen floor, no margin)
```

All twelve offsets are identical to those filed in the round-58 opening
`corpus/evidence/round58/s101-open.txt` (eleven listed there as `char N`, the twelfth as
"character 797"), including the spot-check's quote `并以[文献类型标识/载体类型标识]表示`
at offset 797, count 1.

### 1.6 Census

```
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa
  → W04 S051, S053, S073, S074, S075; chousa  ok  …/corpus/SOURCES.md; rc=0
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md → 133
sha256sum corpus/evidence/round5{7,8,9}/census-start.txt
  round57 09ce4a959ddba208da141bc97e872fd5eb36fd428390a1ecf8cf741853016207
  round58 6e5373d0c51de51653a625134d8e3bc08fab0ce7ce2234630a0c983a011fcf20
  round59 09ce4a959ddba208da141bc97e872fd5eb36fd428390a1ecf8cf741853016207
diff round58/census-start.txt round59/census-start.txt → one line: `EXIT=0` (r58) vs `exit=0` (r59)
```

My validator run reproduces the receipt's six data lines exactly and exits 0; the receipt is
byte-identical to round 57's, so identity here does **not** discriminate a fresh run from a carried
copy (expected output over unchanged state is the same bytes).

### 1.7 S101 row state at the tip

```
awk -F'|' 'NR==111{…}' corpus/SOURCES.md
  [2] S101  [5] tier B  [9] mined  [10] 2026-10-25  [11] 180d
  [7] anchor cell: "section 11 (文献标志码), section 14.1 and 14.4 (参考文献) and the 15.7 parameter
      table (UTF-16LE text of the raw .doc capture); located quotes char 11170, char 11205,
      char 11993, char 12161, char 13247, char 34374"
  [12] used-by: "corpus/knowledge/citation-count-semantics-r37.md, corpus/lessons/round-58.md"
ls corpus/knowledge/carrier-alphabet-china-r58.md → No such file or directory
```

The round-58 carrier entry was never landed, so the used-by cell correctly does not name it; the
anchor cell still names only §§11/14.1/14.4/15.7 and the old UTF-16LE offsets (the round-58 scribe's
F4 stands unresolved).

### 1.8 Wave reports at the time this was written (41 landed, live count)

Snapshot taken while the wave was still settling: 41 `w1/*.md` reports existed, 40 name
`round59/claims.md`, and 13 contain a `C1=PASS`/`C2=PASS` token (twelve siblings and this report).
In the ones I read, the token is the *unreachable target* or a condition a receipt must satisfy, not
a round-59 result: `R59Critic55.md` and `R59Critic59.md` quote the round-58 audit,
`R59Scribe18.md` explicitly refrains from claiming either counter reached it, and
`R59MutationTester63.md` states a useful counter must not print `C1=PASS` while its own legs show
failed refusals. I did not read all 41, so "no landed report claims a reachable round-59 verdict" is
an observation over the reports I sampled, not a count. All seats are same-lane, not independent
witnesses.

## 2. Draft `## Gate` for `corpus/lessons/round-59.md`

### 2.1 Freeze state — what round 59 can score from W1

- **No round-59 freeze exists at W1.** `corpus/evidence/round59/` holds `census-start.txt` and
  `controls/c1-before.txt` only; `claims.md`, a round-59 counter and a quote manifest are absent
  (HEAD `af8c0a4` lists neither path; both files are untracked in the working tree). No W1 seat is
  dispatched to author them: the 16 distinct dispatched bodies (enumerated in §1.2) contain only
  run/assess/draft-wording/read/falsify/mutation-test instructions, every non-scribe body says
  "No edits"/"Never edit lane files", and a keyword count over all 66 tasks for authoring verbs
  (`author|create|write the|draft the|add a`) returns 0. Consequence for the Gate: **no round-59
  candidate can be admitted or refused this wave on a frozen predicate**; the Gate records state
  and schedules the build.
- **What the round-59 plan record says and what was dispatched disagree.** All 66 `w1-spec.json`
  `item` bodies are one boilerplate sentence that orders the seat to read the absent
  `round59/claims.md`; 0 of the 66 *dispatched* task bodies mention that path, 50 mention a
  round-59 claim, 45 mention round 59 and 33 mention round 58. A closure reader auditing
  `w1-spec.json` alone would conclude the wave ran against a freeze it never had; a reader auditing
  `w1-dispatch.json` would see a round-58-defect falsification wave. Both files must be reconciled
  in the lesson, and the Gate must cite the dispatch record for what seats were told.
- **`w1.ready` is not a precondition gate.** It carries lane/round/wave/dispatch/l1 only, was
  written at 15:12:15 before `w1-spec.json` (15:14:46), and names no claims path or digest. A
  missing freeze therefore cannot mark the wave not-ready — which is exactly what happened.

### 2.2 Offline source row (measured this seat, no fetch)

S101 — `corpus/SOURCES.md:111`, tier B, `mined`, opened 2026-10-25, recheck 180d. Re-derived this
round from the lane-owned capture with the pinned tool: raw `6dc68fd6b32ce9c8dfcebce8.raw`, 129,024 B,
sha256 `6063a3aff7a4…ddf3`; `tools/capture-text.py` pin `2c0140bc…2573`; defined form 27,012 chars,
sha256 `a8e3e7ad…f867`, byte-identical across two runs. All 12 frozen round-58 quotes (the only
manifest that exists) locate exactly once at offsets
315, 330, 590, 683, 734, 781, 797, 838, 965, 993, 1460, 11723; three are line-start-bound
(315, 330, 993).

Wording for the lesson: *S101 re-opened offline at the round-59 tip; the round-58 quote set still
binds 12/12 uniquely, so the capture and the pin are unchanged. Nothing about present-day validity,
issuer or edition is claimed: the located text carries none, and no fetch was made (L0 `8d77e6c1`
open).*

### 2.3 Outside spot-check record (round-58 closure) — the record the closure asked for

The round-58 verifier spot-check (`corpus/lessons/round-58-verifier-spotcheck.md`, committed by
`af8c0a4`, which touches only that file) recorded two discernment verdicts. The lesson must carry
them, with their quote, because that artifact is non-author evidence and round-58's lesson was not
rewritten:

- **Admit — S101 document-type/carrier notation, as source evidence only, not as knowledge and not
  as a claim.** Re-opened this round: `corpus/evidence/round58/s101-open.txt` lines 3–6 name the
  capture and the quote `并以[文献类型标识/载体类型标识]表示`, which re-locates at character 797,
  count 1, in the form I re-derived (§1.5). Agreement: agree.
- **Reject — present status, legal force or current use of GB3469.** Ground: no live source; the
  fetch-scope L0 `8d77e6c1` is open. Flip: an operator-approved research window plus a located
  current authority.
- Trend verdicts carried: expansion unchanged (133 source rows, no new knowledge entry), quality
  unchanged (no admitted entry re-verified), discernment improved (both outside verdicts agree with
  a re-open I could reproduce offline).

### 2.4 SOURCES and census

- Rows 133 → 133. Validator run at the tip: `rc=0`, five `W04` duplicate-URL warnings (S051, S053,
  S073, S074, S075) — unchanged from rounds 57 and 58. `census-start.txt` matches those six lines
  and is byte-identical to round 57's receipt, so the lesson should cite the receipt as *state*, not
  as proof of when it was produced.
- No row added this round (no fetch, no newly opened document). S101's used-by cell still reads
  `corpus/knowledge/citation-count-semantics-r37.md, corpus/lessons/round-58.md` and its anchor cell
  still names §§11/14.1/14.4/15.7 with the undefined UTF-16LE offsets. Any round-59 candidate
  citing S101 §1.2 must carry its own section-1.2 anchor in its own `source:` line rather than
  pointing at the row's anchor cell (round-58 scribe F4, unresolved).

### 2.5 Candidate decisions admissible from W1

| surface | decision | evidence | flip |
|---|---|---|---|
| any round-59 claim (C1/C2/other) | **not decidable** — no freeze, no counter | `corpus/evidence/round59/` holds 2 files; 0/66 dispatched tasks author a counter; `w1-spec.json` names an absent claims path 66/66 | an authored, digest-pinned round-59 claims file plus a counter whose positive control prints its exact target token, both committed before data seats |
| round-58 C1 as a positive-verdict-path claim | **refuse / unprovable** | `c1-count.py` (`65da18bb…`) lines 51, 391, 394, 399: lowercase legs vs `"=PASS"` aggregation makes the target unreachable; round-59 carries no patched counter | a builder plus counter that prints `C1=PASS` and exits 0 in bounded scratch, recorded, with the frozen bytes untouched |
| round-58 C2 entry `carrier-alphabet-china-r58.md` | **absent; not admitted** | `ls` → no such file; S101 used-by does not name it; the round-58 closure records the frozen C2 predicate as unsatisfiable (span-start offsets cannot satisfy occurrence-offset binding and byte-identical rebuild at once) | a re-freeze whose C2 counter passes, then the entry lands |
| S101 offline re-opening | **admit as source evidence only** | §1.5 measurements: 12/12 unique, 3 line-start, form and tool pins unchanged | capture digest or tool pin change |
| a new `SOURCES.md` row | **refuse** | 133 → 133; validator `rc=0`; no document opened this round | an operator-approved window plus a located document |
| round-58 positive-control obligation (QUALITY 115) | **not met in W1** | `predata/` empty; the only receipt is deny-only (`DENIED=0/0`, `REFUSE=0/7`); no positive builder receipt anywhere in round 59 | a committed receipt in which a conforming builder reaches the declared final token |

### 2.6 Spot-check intake from round 58 (the closure's routed defects)

1. *Freeze must-pass positive controls that exercise the exact final counter predicate before wave
   data.* **Not done in W1**: `predata/` is empty and no positive-control receipt exists; the only
   control artifact is round 58's before-receipt, copied (§1.3). Carried to whatever wave builds
   the round-59 counter; QUALITY 115 is the check.
2. *Record the external admit/reject check and its source quote in the next lesson.* **Discharged by
   §2.3 wording**, with the quote re-located independently at 797.
3. *Operator: review dispatch prompt / wave handoff clarity.* **Recurred, measured**: the plan
   record names a nonexistent freeze (66/66 `item`s), the dispatch record never mentions it (0/66),
   and the ready gate checks neither. See M1.

## 3. Draft `## Mistakes` rows for `corpus/lessons/round-59.md`

**1. handoff — the recorded plan names a freeze that does not exist and that no seat was told to
read.** · Evidence: `corpus/evidence/round59/claims.md` absent; `corpus/evidence/round59/` holds
only `census-start.txt` and `controls/c1-before.txt`; 66/66 `w1-spec.json` `item` bodies order the
seat to read it, while 0/66 `w1-dispatch.json` task bodies mention it (50 mention "claim", 45
"round59", 33 "round58"); `w1.ready` carries no claims path or digest and was written at 15:12:15,
before `w1-spec.json` at 15:14:46; 0 dispatched tasks author a claims file or counter, and every
non-scribe body forbids lane edits. · Fix: do not rewrite either wave file after the wave; the
lesson records both readings and cites the dispatch record as what seats were told. Prospectively,
`w1.ready` must carry the digest of every path the plan names and must not publish ready when one is
missing (QUALITY 24: controls and predicate before data).

**2. calibration — the round's only control receipt is a copy of the previous round's and carries
no provenance.** · Evidence: `corpus/evidence/round58/controls/c1-before.txt` and
`corpus/evidence/round59/controls/c1-before.txt` are byte-identical, sha256
`2c9bbe54…ebfe`, 958 B; the round-59 file has no command line, counter path, pin or `--controls`
set, while the round-58 `c1-controls.txt` carries all of those and `DENIED=2/2`; the round-59
receipt shows `DENIED=0/0`, so the two do-nothing controls were not run; the round-58 audit states
the base run reproduces that receipt byte-for-byte, so identity is expected and cannot date the
file. · Fix: report it as a carried receipt, never as a round-59 measurement; require every
before/after receipt to carry the command, counter digest, builder digest and `--work` path, as
`c1-controls.txt` does.

**3. calibration — the milestone's "build" half has no seat and the positive verdict path is still
unreachable.** · Evidence: `jq
'[.taskCall.tasks[]|select(.task|test("author|create|write the|draft the|add a";"i"))]|length'`
→ 0 across 66 seats (§1.2); the 16 executor seats only "inspect and run exact round58" artifacts; the
frozen counter's `PASS = "pass"` (line 51) versus `"=PASS"` in `ref_pass` (391) and SUMMARY (399)
with `verdict` (394) requiring `ref_pass`; `C1=FAIL` in the only receipt; QUALITY 115 landed at HEAD
but nothing in round 59 exercises its check. · Fix: the lesson states that no round-59 claim can be
scored from W1 and names the build wave's deliverables (claims file with digest, counter with a
positive fixture that reaches the declared token, deny-only controls, quote manifest), each with a
reachable receipt path.

**4. operability — the before-state is asserted from an undated copy while the destructive
behaviours it names are unadjudicated for this round.** · Evidence: the receipt's
`FOREIGN=fail(rc=0, orphans deleted: foreign gone=True)`, `SYMLINK_OUT=fail(rc=0, expected
refusal)(target-dir-written!)`, `SYMLINK_CACHE=fail(rc=0, expected refusal)` and
`MANY_QUOTES=fail(rc=0, expected refusal)`; the round-58 audit reports the same base-builder
behaviours on its own run, and the builder pin `1ed2650a…0bf6` is unchanged at the tip. · Fix: no C1
verdict this round; if a later wave re-measures, run the frozen counter on the pinned builder with a
fresh `--work` and commit the command line with the receipt, so the before-state is dated to that
wave rather than inherited.

**5. calibration — twelve depth seats received one identical instruction, so the wave produces
twelve re-derivations instead of twelve slices.** · Evidence: the 12 scribe task bodies are
identical after normalizing the scratch and report paths
(`.ufo/waves/round-59/w1-dispatch.json`), against round 58's nine differentiated scribe reports
(`R58ScribeEntryDraft`, `R58ScribeEntryInference`, `R58ScribeC2Limits`, `R58ScribeGateLesson`,
`R58ScribeMistakeMine`, `R58ScribeCounterReceipt`, `R58ScribeS101SourceRow`,
`R58ScribeConsiderThese`, `R58ScribeC1PatchNotes`). · Fix: assign each depth seat a named slice (Gate
row, Mistakes row, quote table, source row, receipt audit) and record the slice in the dispatch
record; the lesson counts distinct slices delivered, not seats run.

## 4. Findings reported, not filed as Mistakes

- **F1 (conflict, sibling report vs. tree).** `R59Critic59.md` states that
  `git ls-tree -r --name-only HEAD corpus/evidence/round59 corpus/evidence/round58 …` "lists only
  round59 `census-start.txt` and `controls/c1-before.txt` under round59". Run verbatim at HEAD
  `af8c0a4`, that command prints **nothing** for both round-59 paths; both files are untracked
  (`??`). The sibling's own conclusion (no round-59 claims file) is correct; the tree claim is not.
  Reported verbatim for the canonical judge; not edited in place.
- **F2 (calibration, unreachable positive path).** By inspection of the frozen bytes alone — no
  rerun needed — `c1-count.py:51` defines `PASS = "pass"`, `:391` requires `"=PASS"` in every
  refusal leg, `:394` requires `ref_pass`, and `:399` counts `"=PASS"`. The target cannot be reached
  by any builder. Round 59 did not patch or replace the counter, so the defect is inherited intact.
- **F3 (calibration, no margin).** Line-start anchors are 3/3 at the tip (315, 330, 993) against a
  frozen floor of 3: any offset shift in a future rebuild drops the anchor leg below the floor.
  The 12 offsets are otherwise unchanged from the round-58 opening `s101-open.txt` (§1.5).
- **F4 (calibration, receipt provenance).** Round-59's receipt is 958 B and 16 lines; the round-58
  control receipt with the same legs is prefaced by a `Command:` line and pinned digests. A receipt
  without an invocation record is indistinguishable from a carried copy, as here.
- **F5 (calibration, census).** `census-start.txt` is byte-identical to round 57's and differs from
  round 58's only in the case of `EXIT=`/`exit=`, i.e. the caller's line, not the validator's. My
  tip run reproduces the six data lines and `rc=0`; the lesson should cite state, not timing.
- **F6 (source narrowing, carried).** S101's row anchor cell names §§11/14.1/14.4/15.7 with UTF-16LE
  offsets, while the only re-derived quotes are in the defined capture-text form (§1.5). A round-59
  candidate citing §1.2 must carry its own anchor; extending the row's anchor cell would be a
  second edit beyond the round-58 used-by-only change and must be declared, not slipped in.

- **F7 (provenance, scratch only, reported at 15:24).** An unowned `positive-path/` tree exists under
  another seat's scratch namespace, `/fast/scratch/hyaku/chousa-r59/R59Executor07/positive-path/`:
  `c1-positive-builder.py` (7,544 B), `run-c1.sh`, `poison-base.py`, `c2-poison-zh.stdout`,
  `ctrl-vacuous/`, `keep/`, `run-ctrl/`, all mtime 15:23–15:24. It is **not mine** — my namespace was
  `/fast/scratch/hyaku/chousa-r59/R59Scribe25/`, now removed — and I neither moved nor deleted it;
  seat `R59Executor07-2` reported it as foreign and the author is unidentified. It changes nothing in
  §2.5: a positive C1 builder exists only as uncommitted scratch bytes, with no counter pin, command
  line or verdict, so it is not a receipt. Recorded here so a closure reader who finds the tree knows
  it was seen, unattributed, and not adopted.

## 5. Not run / limits

- `corpus/evidence/round58/c1-count.py` was **not** run by this seat; its committed receipts
  (`controls/c1-before.txt`, `controls/c1-controls.txt`) are cited as committed and its mechanism is
  cited from lines 51/391/394/399 read directly. The `REFUSEALL`-crash and case-fix reproductions
  are cited from `R58ExecC1CounterAudit.md` as sibling-report evidence, not re-run.
- `corpus/evidence/round58/c2-count.py` was **not** run; no round-59 C2 claim exists to test.
- `tools/quote-reopen.py` was **not** run (live fetch; L0 `8d77e6c1` open). Only the offline
  `capture-text.py` form was re-derived.
- No live fetch, no install or update, no `pacman`, no git/jj write, no write outside this report.
  Git was used read-only (`rev-parse`, `ls-files`, `ls-tree`, `status`, `show --stat`).
- The census validator **was** run once (rc 0) — the only validator invoked.
- Round-59 readings are a snapshot and the wave was still settling: 41 of 66 reports existed when I
  took the §1.8 count, and later seats may change it, not the structural facts of §1.1–§1.3.
- I did not author anything under `corpus/`; the Gate and Mistakes text above is draft wording for
  the L1 to place in `corpus/lessons/round-59.md`.

## 6. Scratch and artifact paths

- Scratch `/fast/scratch/hyaku/chousa-r59/R59Scribe25/` (`form1.txt`, `form2.txt`) was removed at the
  end of this seat (`ls /fast/scratch/hyaku/chousa-r59/` no longer lists it); nothing of mine remains
  outside this report.
- Report: `.ufo/waves/round-59/w1/R59Scribe25.md`
- Inputs: `corpus/evidence/round59/{census-start.txt,controls/c1-before.txt}`;
  `.ufo/waves/round-59/{w1.ready,w1.ready.partial,w1-spec.json,w1-dispatch.json}`;
  `corpus/lessons/{round-58.md,round-58-verifier-spotcheck.md}`;
  `corpus/evidence/round58/{claims.md,c1-count.py,c2-count.py,c2/quotes.tsv,controls/*,s101-open.txt}`;
  `corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw`; `corpus/SOURCES.md:111`; `corpus/QUALITY.md` 24, 115;
  `.ufo/waves/round-58/w1/{R58ExecC1CounterAudit.md,R58ScribeGateLesson.md}`;
  `.ufo/waves/round-59/w1/{R59Critic55.md,R59Critic59.md,R59Scout29.md}`

VERDICT: The Gate draft is admissible only as a state-and-schedule record: round 59 has no freeze,
no counter and no author seat for either, so **no round-59 claim can be decided from W1**; the rows
that survive are the offline S101 re-derivation (12/12 unique, 3/3 line-start, pins unchanged), the
round-58 closure's admit/reject record with its quote at char 797, and the unchanged 133-row census
with five W04 warnings. The round-58 C1 claim is falsified as a positive-verdict-path claim by
inspection of the frozen counter (`PASS = "pass"` vs `"=PASS"` at lines 51/391/394/399), and the
only round-59 control receipt is falsified as round-59 evidence by being byte-identical to round
58's (sha256 `2c9bbe54…ebfe`, `DENIED=0/0`, no command or pin). Reported conflicts: `R59Critic59.md`
claims HEAD lists the round-59 evidence files; `git ls-tree` at `af8c0a4` lists neither.

---

## 7. Second-pass verification (append-only; same seat, re-run)

Appended by a re-run of seat `R59Scribe25` at 2026-10-27T15:2x-03:00, lane HEAD still
`af8c0a460d087cbfb8245fb9326608783ccc510b`. Nothing above is rewritten; where this pass disagrees
with it, the correction is stated in §7.4 for the canonical judge.

### 7.1 Executed in this pass, and not

Ran, read-only, no lane writes:

- `python3 tools/capture-text.py corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw` and the same with
  `--locate '<quote>'` for the frozen S101 quotes.
- The frozen counter loaded as a module in an in-process kernel
  (`importlib.util.spec_from_file_location` on `corpus/evidence/round58/c1-count.py`; `main()` not
  called, no `subprocess`, nothing written) solely to evaluate its own aggregation expressions over
  leg strings the file itself emits.

Not run by this pass: the counter battery end-to-end (`c1-count.py --builder …`), `c2-count.py`,
`tools/quote-reopen.py`, the census validator, any fetch, any install. The `R59Executor*` receipts
cited below are read, not re-run.

### 7.2 S101 re-derivation — 12/12 confirmed; the offset convention is 0-based

```
python3 tools/capture-text.py <raw>                       → 47,356 bytes / 27,012 characters / 470 lines
python3 tools/capture-text.py <raw> --locate '并以[文献类型标识/载体类型标识]表示'
                                                          → LOCATED count=1 offset=797
python3 tools/capture-text.py <raw> --locate '[DB/OL]—联机网上数据库(database online)；'
                                                          → LOCATED count=1 offset=993
python3 tools/capture-text.py <raw> --locate 'not present at all zzz'
                                                          → LOCATED count=0 offset=-1   (rc=1)
```

27,012 characters matches `s101-open.txt`'s stated output length. Re-located all 12 frozen quotes
(`corpus/evidence/round58/c2/quotes.tsv`, 12 data rows, 12 distinct strings): each `count=1`; each
0-based index equals the char recorded in `s101-open.txt` (315, 330, 590, 683, 734, 781, 797, 838,
965, 993, 1460, 11723). A 1-based reading matches 0/12, so the lesson must state that the number is
the **0-based** `--locate` offset — criterion 89 binds an entry's `char N` to that tool's output.
Line-start anchors: 3/3 (315, 330, 993). Raw sha256 `6063a3af…d9fddf3` unchanged; no live fetch.

### 7.3 The positive verdict path, executed in both directions

Against the frozen module in memory (`PASS = 'pass'`, `FAIL = 'fail'`, both confirmed by import):

| leg set (exactly what the counter would emit) | `ref_pass` (:391) | `REFUSE` (:399) | verdict (:394) |
|---|---|---|---|
| every safe leg `pass`, every refusal leg `pass(refused)` — an honest builder | **False** | **0/7** | **FAIL** |
| every refusal leg `fail(rc=0, expected refusal)` — the round-58/59 receipt | False | **0/7** | FAIL |
| every refusal leg `fail(… reason … absent in '… token =PASS\n')` — builder prints the token | **True** | **7/7** | **PASS** |

- The tally is **invariant**: the best case and the worst case both print `REFUSE=0/7`, because
  `sum('=PASS' in l …)` never sees the uppercase token (`:399`). `REFUSE=` therefore was never a
  measurement of refusals, in either receipt.
- The forge is reachable because `ref_pass` is a substring test over the **whole leg line**, and the
  line embeds untrusted builder output: `err[:160]` at `:156`, `reason-unnamed:{err!r}` at `:224`.
  Executed: seven `FAIL` legs whose embedded stderr carries `=PASS` yield `ref_pass=True`,
  `verdict=PASS`, `REFUSE=7/7` — no leg passes on merit.
- `(target-dir-written!)` is appended to the same string (`:236`) and is never tested by `:391` or
  `:399`. Executed: an annotated `FAIL` leg bearing the token inside its stderr scores as passing.
- The deny leg cannot discriminate: `denied_pass = (denied == total) if total else True` (`:393`).
  `DENIED=0/0` is the skip branch (no `--controls`), and when controls are supplied each sub-run
  prints `C1=FAIL` for the same structural reason, so `denied` always reaches `total`. Both the
  round-59 receipt and the executor runs show `DENIED=0/0`; `R59Executor01` reports the same builder
  leaving `DENIED=2/2` when controls are attached.

End-to-end corroboration, cited not re-run: `R59Executor03` §4 runs the frozen bytes on a builder that
refuses nothing correctly, writes `spans.tsv` through the symlinked `--out`, embeds `=PASS` in its
stderr, and receives `SUMMARY … REFUSE=7/7 …` / `C1=PASS` / `EXIT=0`; `R59Executor16` R2 shows the same
eleven leg strings with only the two case literals changed reach `REFUSE=7/7 C1=PASS exit=0`;
`R59Executor08` shows an honest positive builder printing `=pass` 11 times, `=PASS` 0 times, `C1=FAIL`
on two byte-identical runs.

### 7.4 Corrections to the text above (append-only)

- **C1 (material).** Two places above state the target is unreachable tout court: §4 F2 ("cannot be
  reached by any builder") and §3 row 3 ("the positive verdict path is still unreachable"). Correct
  statement: it cannot be reached by any builder that refuses as declared; it **is** reached by a
  builder that prints the token into a failing leg's stderr (`R59Executor03` §4, executed; §7.3
  reproduces the predicate at string level). The frozen predicate is therefore a false negative for
  an honest builder **and** a false positive for a violating one — wider than the round-58 lesson's
  wording, which records only the false negative.
- **C5 (consequence for the flip condition).** §2.5's flip for round-58 C1 reads "a builder plus
  counter that prints `C1=PASS` and exits 0 in bounded scratch". That condition is already satisfied
  today by a builder that refuses nothing correctly (`R59Executor03` §4: `C1=PASS`, `EXIT=0`, and a
  file written through the symlinked `--out`). The flip must add "…and no refusal leg passed only
  because its line contained the token, and no forbidden write occurred", i.e. it must name the
  predicate, not the token.
- **C2 (minor).** §3 row 4 / §4 F4 say the receipt is "958 B and 13 lines". Size is right; the file is
  **16 lines** (15 program-emitted lines + the caller's `EXIT=1` annotation), confirmed by
  `awk 'END{print NR}'`.
- **C3 (minor).** §3 row 4's citation "lines 51/391/394/399" should add `:156`/`:224` (stderr
  embedding) and `:236` (unscored write-through annotation); note also `:389` is a dead reassignment —
  `:390` overwrites `ok_pass`, so the `(pass)`-suffix test at `:389` never runs.
- **C4 (state).** §1.8's "41 of 66" was an earlier snapshot. At this pass: 51 of 66 reports landed
  (executor 8/16, reviewer 10/14, scribe 11/12, scout 12/12, critic 7/7, mutation-tester 3/5), plus
  `swarm-registry.json`.

### 7.5 Draft Gate addendum (paste-ready, conditional on the missing freeze)

- **Freeze.** Round 59 has no `corpus/evidence/round59/claims.md`, no round-59 counter, no quote
  manifest and no freeze commit id at `af8c0a4`; the only round-59 evidence bytes are the untracked
  `census-start.txt` (byte-identical to round 57's) and `controls/c1-before.txt` (byte-identical to
  round 58's, sha256 `2c9bbe54…ebfe`, `DENIED=0/0`, no command, no pin). `w1.ready` was written
  15:12:15, before `w1-spec.json` at 15:14:46, and names no claims path or digest. Of 66 dispatched
  seats, none is an author seat for a claim, counter or control; the 12 scribe bodies are identical
  after normalizing scratch and report paths.
- **Positive verdict path (this round's milestone).** Measured, both directions: an honest builder
  satisfying all eleven declared legs still cannot reach `C1=PASS` (§7.3, executor receipts), while a
  builder that refuses nothing correctly and prints `=PASS` into its stderr does reach it and is even
  annotated `(target-dir-written!)` while passing. No positive control exists; the round-58 C1 claim
  stays unadmitted, and criterion 115 must be read as requiring **both** reachability by a conforming
  builder **and** non-reachability by a token-printing one.
- **Source opening (offline).** S101 re-derived from the committed capture: 12/12 quotes unique at
  their recorded 0-based offsets, 3/3 line-start anchors, 27,012 characters, raw pin unchanged; no
  live fetch while the chousa round-29 fetch-scope entry in the fleet L0 file (commit `8d77e6c1`)
  remains unanswered, and `tools/quote-reopen.py` was not run.

### 7.6 Draft Mistakes rows for `corpus/lessons/round-59.md`

1. **vacuous — a verdict predicate is a substring test over a line that embeds untrusted subprocess
   output** · Evidence: `corpus/evidence/round58/c1-count.py:156`, `:224` embed `err[:160]`/`{err!r}`
   in the leg line; `:391` and `:399` test `"=PASS" in l`. Executed: seven `FAIL` legs carrying the
   token reach `ref_pass=True`, `C1=PASS`, `exit 0` (`R59Executor03` §4, same run also writes through
   a symlinked `--out`). · Fix: compare a structured field per leg (name, exit code, named reason
   class) rather than a substring of the rendered line, and score the `(target-dir-written!)`
   annotation as a failure.
2. **vacuous — the receipt's headline tally is invariant** · Evidence: `:399` counts `"=PASS"` over
   legs that never render it, so `REFUSE=0/7` prints for the best and the worst builder alike
   (§7.3, executed). · Fix: a frozen receipt must print a statistic that changes when the measured
   behaviour changes; require the best case and the pinned-base case to print different tallies.
3. **vacuous — the deny-only control leg cannot discriminate** · Evidence: `:393`
   `denied_pass = (denied == total) if total else True`; `DENIED=0/0` in the round-59 receipt is the
   skip branch, and a supplied control is denied because `C1=PASS` is unreachable for it too
   (`R59Executor01` `DENIED=2/2`). · Fix: pair every deny control with a positive control that must
   reach the declared token and a token-forge control that must not, and require the three to print
   different verdicts before a freeze binds data.
4. **process — a carried byte-identical receipt is filed as the round's control** · Evidence:
   `corpus/evidence/round59/controls/c1-before.txt` = round-58 `controls/c1-before.txt` (sha256
   `2c9bbe54…ebfe`, 958 B, 16 lines, no `Command:` line, no pins, `DENIED=0/0`). · Fix: a round's
   before-receipt names its own invocation, builder pin and date, or the round records that it has no
   dated before-state instead of inheriting one.

### 7.7 Limits of this pass

- The counter battery was not run here; the two-direction result in §7.3 is derived from the frozen
  module's own expressions in memory, with end-to-end confirmation taken from the executor reports.
- No census validator, no `c2-count.py`, no `quote-reopen.py`, no fetch, no install, no `pacman`, no
  git/jj write, no write outside this report. Git was read-only (`rev-parse`, `ls-tree`, `status`).
- Scratch `/fast/scratch/hyaku/chousa-r59/R59Scribe25/` was removed during this pass by the concurrent
  run of the same seat before anything could be filed there; nothing of this pass persists on disk
  except this section.

SECOND-PASS TRAILER (relative to lane root): `.ufo/waves/round-59/w1/R59Scribe25.md`

### 7.8 Provenance of this file (appended by the first pass, after §7 landed)

- **Two writers, one seat id.** §1–§6 are this process's text; §7 was appended by a *concurrent run of
  the same seat* while this process was still working. Nothing in §1–§6 was rewritten to match §7, per
  the lane's errata-append practice; §7.4 is the authoritative correction block.
- **§7.4 C1 verified independently here, and it stands.** From the frozen bytes: `:156` embeds
  `err[:160]` inside a `FAIL` line, `:224` embeds `reason-unnamed:{err!r}`, `:391` is
  `all("=PASS" in l …)` over the whole leg line and `:399` counts the same substring. A builder that
  prints `=PASS` into a failing leg's stderr therefore scores `ref_pass=True` → `C1=PASS`; a builder
  that refuses as declared never renders the token and scores `C1=FAIL`. Executed corroboration is
  sibling evidence, not mine: `R59Executor03` §C (`C1=PASS`, `EXIT=0`, all seven refusals failing,
  a write through the symlinked `--out`) and `R59Executor01` §4 (all eleven legs passing on merit
  still prints `C1=FAIL` / `REFUSE=0/7`, the "strongest reachable positive state", with
  `DENIED=2/2` intact when controls are attached). C5 also stands: my §2.5 flip for round-58 C1 is
  satisfied by a non-refusing builder today, so the flip must name the predicate, not the token.
- **§7.4 C2's quoted target is stale, its conclusion is right.** Before §7 existed this process had
  already corrected the line count in place from 13 to **16** (`wc -l` = 16; 15 program lines plus the
  caller's `EXIT=1`). C2's conclusion (16 lines) is correct; the words it quotes no longer appear.
  §7.4 C3's added citations (`:156`, `:224`, `:236`) are accepted; `:236` appends
  `(target-dir-written!)` to the same unscored string.
- **§7.7's scratch attribution needs one correction.** The scratch directory was removed by *this*
  process at the end of its own run, not by §7's pass; §7's pass found it already absent. Either way
  nothing of either pass persists on disk.
- §7.4 C4's later snapshot (51 of 66 reports) supersedes my §1.8/§5 snapshot (41 of 66) without
  contradicting it; both are dated counts, and neither affects §1.1–§1.3.

PROVENANCE TRAILER (relative to lane root): `.ufo/waves/round-59/w1/R59Scribe25.md`
