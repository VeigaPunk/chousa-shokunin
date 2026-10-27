# R59Scribe20 — round-59 Gate/Mistakes wording, evidence-backed

- Seat: `R59Scribe20` (second dispatch, `R59Scribe20-2`; `w1.ready.partial` maps `R59Scribe20 → R59Scribe20-2`).
- Role: scribe. Axes: `depth`. Item: read the round-58 lesson and verifier spot-check, draft evidence-backed
  round-59 Gate/Mistakes (or report) wording. Deliverable: this file only.
- Every line marked **measured** was produced by a command in §6. Lines marked **static** are read off cited
  lines. Lines marked **peer-reported** are another seat's claim, quoted with its report path and not adopted
  as my observation.

This file supersedes the first attempt's text at the same path. I re-derived its results rather than copying
them; §2.F1, F2, F5, F6, F7 reproduce them, and F6 **corrects** one of its statements (see the correction
note under F6).

## 1. Observed state

Read-only; all times `-03:00`, 2026-10-27.

| observation | result |
|---|---|
| `date -Is` at last check | `2026-10-27T15:22:15-03:00` |
| `ls corpus/evidence/round59 corpus/evidence/round59/controls` | `census-start.txt` (535 B) and `controls/c1-before.txt` (958 B); **no `claims.md`**, no counter, no after-receipt |
| `git rev-parse HEAD` | `af8c0a460d087cbfb8245fb9326608783ccc510b` |
| `git status --porcelain` | `?? .ufo/waves/round-59/` and `?? corpus/evidence/round59/` — both round-59 trees are untracked |
| `git ls-tree -r --name-only HEAD corpus/evidence/round59` | empty output |
| `sha256sum corpus/evidence/round59/controls/c1-before.txt corpus/evidence/round58/controls/c1-before.txt` | both `2c9bbe5446ae4f733bf17a2836cc1b32e823fc8bc287d3da42801b948cfaebfe` |
| `stat -c '%y %s' corpus/evidence/round59/controls/c1-before.txt` | `2026-10-27 15:14:30.645`, 958 B |
| `stat` mtimes | `w1-dispatch.json` 15:12:11.20, `w1.ready` 15:12:15.13, `w1-spec.json` 15:14:46.65, `w1.ready.partial` 15:19:33.81 (858 B) |
| `ls .ufo/waves/round-59/` | `predata/` (empty), `w1/` (54 `*.md`), `w1-dispatch.json`, `w1-spec.json`, `w1.ready`, `w1.ready.partial`; **no `w1.ready.dispatched`, no `w1-results.json`** |
| `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | `133` |
| `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` | exit `0`; W04 warnings S051, S053, S073, S074, S075 then `ok …/corpus/SOURCES.md` — the same five warnings and ok line that `corpus/evidence/round59/census-start.txt` records |

## 2. Findings

### F1 — the frozen C1 counter is wrong in **both** directions: an honest candidate can never pass, a token-printing candidate passes without refusing anything

This is the round's central calibration fact, and it is stronger than "the positive path is unreachable".

**Static — the honest side.** `corpus/evidence/round58/c1-count.py`:

- `:51 PASS = "pass"`, `:52 FAIL = "fail"`.
- Refusal emitters write that lowercase constant: `:160 return f"{name}={PASS}(refused)"`,
  `:223 legs.append(f"FOREIGN={PASS}(refused)" …)`, `:234 legs[-1] = f"SYMLINK_OUT={PASS}(refused)"`.
- The verdict searches uppercase: `:391 ref_pass = all(("=PASS" in l) for l in ref_legs)`, and `:399`
  prints `REFUSE={sum('=PASS' in l …)}/7` with the same test.
- `:394 verdict = "PASS" if (ok_pass and ref_pass and integrity and denied_pass) else "FAIL"`.

Every *pass* branch of a refusal leg goes through `PASS="pass"` (`:160`, `:223`, `:234`); the only way `=PASS`
can appear in a refusal line is as the candidate's own text echoed into a `fail(...)` message (`:156`, `:222`).
So for a candidate that does not print the token, `ref_pass` is `False` and `C1=PASS`/exit 0 is unreachable.
`:389` is dead code, overwritten on the next line by `:390`.

**Measured — honest side, end to end.** Frozen counter on the lane's own builder:

```
python3 -B corpus/evidence/round58/c1-count.py --builder tools/build-spans.py \
        --work /fast/scratch/hyaku/chousa-r59/R59Scribe20-2/c1run
```

All four safe legs pass (`EMPTY_OK`, `REBUILD_OK`, `HELDOUT_OK`, `ESCAPE_ENTRY`), all seven refusal legs fail,
`SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=0/0`, `C1=FAIL`, exit 1, 5.4 s wall.
`diff` of my stdout against `corpus/evidence/round59/controls/c1-before.txt` reports exactly one difference,
`15a16 > EXIT=1`: the carried receipt is the same run plus the shell's `echo EXIT=$?`. So the round-59 "before"
receipt is **reproducible** on the current tree — and it evidences the *base* builder, not any round-59 candidate.

**Measured — the forged side.** The same substring test reads refusal lines that embed the candidate's own
output: `:152 err = (proc.stderr or "") + (proc.stdout or "")`, `:156 … absent in {err[:160]!r}` (`:222/:224`
do the same for `FOREIGN` at 200 chars). Driving the frozen `expect_refuse` with a child that exits nonzero and
prints `=PASS` yields seven leg lines that are all labelled `fail`, on which the frozen predicate evaluates:

```
FOREIGN=fail(reason-unnamed:'refusing: nothing to do =PASS')
SYMLINK_OUT=fail(rc=1, reason [...] absent in 'refusing: nothing to do =PASS\n')
… (SYMLINK_CACHE, FIFO_TXT, DEVZERO_TXT, FAT_RAW, MANY_QUOTES identical shape)
legs labelled fail: 7 of 7
ref_pass on these lines: True
REFUSE display: REFUSE=7/7
```

The four safe legs still have to be genuinely earned, so this is not "any file passes"; but a candidate that
builds correct spans and prints one token while refusing hazards is scored `REFUSE=7/7` **without naming a
single reason class**. Three peers measured the same surface end to end (**peer-reported**, not my runs):
`R59Executor03.md:53-54` (`.ufo/waves/round-59/w1/`), `R59Executor02.md:86,100-101,199` (token-repaired copy
credits a "47-line name-keyed forge" with `C1=PASS`), `R59Executor01.md:72,153,162` (symlink containment
annotated `target-dir-written!` but not failed, so `C1=PASS` is containment-unsound even after a token repair).

**Consequence for this round.** The pair "honest candidate fails / forger passes" means the counter cannot
discriminate, which is precisely what QUALITY 115 (`corpus/QUALITY.md:974`) was written to prevent before a
freeze. No round-59 claim may rest on this counter in either direction.

### F2 — the control conjunct is vacuous under the predicate the claim declares

`corpus/evidence/round58/claims.md:9` freezes the predicate as
`python3 corpus/evidence/round58/c1-count.py --builder <builder> --work <fresh-absolute-dir>` — no `--controls`.
In the counter, the control block only runs when `--controls` is truthy (`:365`), else `:382` prints
`DENIED=0/0`, and `:393 denied_pass = (denied == total) if total else True` makes a zero denominator a pass.
The claim's prose ("Do-nothing controls must not reach `C1=PASS`") is therefore not exercised by its own
predicate. The separate committed controls run (`corpus/evidence/round58/controls/c1-controls.txt`) does print
`DENIED=2/2`, but its two `CONTROL_* = denied` lines are nested invocations (`:372-381`) whose only test is
"stdout has no `C1=PASS`" — which F1 guarantees for any honest control. The control battery has zero
discriminating power independent of the builder.

### F3 — two further vacuous checks in the same counter, both static and both cheap to see

1. `:389 ok_pass = all(l.endswith("(pass)") or l.endswith(")") and f"{FAIL}" not in l and "=pass" in l …)`
   is immediately overwritten by `:390`. Dead predicate; the live one is the plain substring test.
2. `HELDOUT_OK` passes `snapshot(work)` as its "before" snapshot at `:345`, evaluated **after** `run_builder`
   has returned, so `outside_before` and `outside_after` (`:143-145`) are two post-run snapshots and can never
   differ. `EMPTY_OK` takes its snapshot before the run (`:195`); `HELDOUT_OK`, the leg that uses the real
   pinned OLE capture, does not. Its containment check is vacuous.

### F4 — frozen C2 counter on the current tree (measured, end to end)

```
python3 -B corpus/evidence/round58/c2-count.py --root /home/vgpnk/Projects/shokunin/chousa-shokunin \
        --work /fast/scratch/hyaku/chousa-r59/R59Scribe20-2/c2run
```

prints `ENTRIES=0/1 BOUND=0/1 … QUOTE_ROWS=0/12 CAPTURE_BOUND=0/12 ENTRY_QUOTES=0/12`,
`ERROR ENTRY_MISSING`, `ERROR PROVENANCE_TRIO`, `ERROR S101_NOT_IN_SOURCE`, `ERROR REF_ID_UNBOUND`,
`ERROR MANIFEST_MISSING`, `ERROR BUILDER_REBUILD_MISMATCH`, `ERROR CAPTURE_BOUND=0/12`,
`ERROR ANCHOR_BOUND=0/3`, `ERROR ENTRY_QUOTES=0/12`, `ERROR NEW_GROUND_FAIL`, `C2=FAIL`, exit 1.

Two readings matter for calibration:

- `ENTRY_MISSING` is literal: `corpus/knowledge/carrier-alphabet-china-r58.md` does not exist (`ls` → no such
  file). C2's target artefact was never landed, consistent with the round-58 lesson.
- `S101_NOT_IN_SOURCE` is **derived, not independent**: `:55 if 'S101' not in (trio[0] if trio else '')` reads
  the *entry's* first line, and with no entry `trio` is empty. The SOURCES row itself is present and healthy —
  `corpus/SOURCES.md:111` carries `| S101 |`, status `mined`, `used-by` naming
  `corpus/knowledge/citation-count-semantics-r37.md, corpus/lessons/round-58.md`. `REF_ID_UNBOUND` (`:62`) is
  likewise expected: the entry path is not (and cannot be) in the `used-by` cell. An operator counting the
  `ERROR` lines would overstate provenance damage; the counter has no short-circuit between "artefact absent"
  and "source binding broken". This seat does not call the SOURCES row defective.

### F5 — C2's two frozen legs still demand mutually exclusive `offset` semantics (measured arithmetic)

- Builder writes span-start: `tools/build-spans.py:43 CONTEXT = 80`, `:142 start = max(0, off - CONTEXT)`,
  `:143 span = text[start:off + len(quote) + CONTEXT]`, `:149 "\t".join([..., str(start), ...])`.
- Counter requires occurrence binding: `c2-count.py` `occurrences=[m.start() for m in re.finditer(...)]`,
  `… or occurrences[0]!=off` → `CAPTURE_BIND`, then `start=max(0,off-80)` / `expected=form[start:end]`.
- Rebuild leg byte-compares the regenerated `spans.tsv` with the committed manifest.

Measured derivation from committed bytes (`tools/capture-text.py` on
`corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw`, exit 0, **27,012 characters / 47,356 bytes**) against the 12
frozen quotes in `corpus/evidence/round58/c2/quotes.tsv`:

| quote n | occurrence | start (=occ−80) | occurrences | len |
|---|---|---|---|---|
| 1 | 315 | 235 | 1 | 14 |
| 2 | 330 | 250 | 1 | 36 |
| 3 | 590 | 510 | 1 | 13 |
| 4 | 683 | 603 | 1 | 29 |
| 5 | 734 | 654 | 1 | 20 |
| 6 | 781 | 701 | 1 | 15 |
| 7 | 797 | 717 | 1 | 19 |
| 8 | 838 | 758 | 1 | 33 |
| 9 | 965 | 885 | 1 | 27 |
| 10 | 993 | 913 | 1 | 33 |
| 11 | 1460 | 1380 | 1 | 27 |
| 12 | 11723 | 11643 | 1 | 21 |

All 12 unique, all `occurrence − start = 80` exactly. A manifest offset must equal the occurrence (binding)
and the start (byte-equal rebuild); no value does both. Independently reproduces the round-58 lesson's
`char 797` anchor (row 7).

Scoped side observation, offered because C2 will be re-frozen from this row: the S101 anchor cell
(`corpus/SOURCES.md:111`, cell 7) cites `char 11170, 11205, 11993, 12161, 13247, 34374`. Against the pinned
form, `34374` exceeds the form length (27,012), and the other positions do not coincide with any frozen quote
start in the table above. This seat did **not** reconstruct the text-form version in use when the row was
written (2026-10-25), so this is recorded as an anchor that is not reproducible under the current pin — not as
a finding that the row is false.

### F6 — the wave's frozen-claims precondition is unmet, and the round-59 tree is not committed at all

`corpus/evidence/round59/claims.md` — the path named by the wave context, by `w1-dispatch.json`'s
`taskCall.context`, and by all 66 seat bodies — does not exist (§1). No round-59 claim is frozen. The review
performed in this report is therefore a reading of **round-58** frozen bytes, not of a round-59 claim.

**Correction to the first attempt.** That text said the absence "is in the committed tree, not a worktree
accident" and reported `git ls-tree … HEAD corpus/evidence/round59` as showing "the same two files". My
measurement is different and important: `git status --porcelain` shows `?? corpus/evidence/round59/` and
`?? .ufo/waves/round-59/`, and `git ls-tree -r --name-only HEAD corpus/evidence/round59` prints **nothing**.
Nothing from round 59 — not the census, not the carried control receipt, not the wave directory — is committed.
The precondition is unmet in the worktree *and* nothing has been frozen into HEAD. Whether that is L1's pending
freeze or an orchestrator omission is not established here; either way, no seat in this wave had a round-59
claim to read.

### F7 — wave shape contradicts the milestone: 66 report-only seats, no seat that may build a control

- `w1-spec.json`: 66 items, 66 distinct raw bodies, **1** distinct body after substituting the seat name
  (`sha256 8a9535ad…` before, `beef4ebeeed0…` after normalising `<name>.md`); body text is "For round 59,
  review ready handoff requirements… Report exact evidence; do not write lane files."
- `w1-dispatch.json`: 66 members, six role templates — 16 executor, 14 reviewer, 12 scribe, 12 scout, 7
  critic, 5 mutation-tester; `taskCall.tasks` length 66. The role text lives only here: my scribe item is
  "Read round58 lesson and spotcheck, draft evidence-backed round59 Gate/Mistakes or report wording. **No writes
  except your report**"; a reviewer item is "Adversarially assess… **No edits**"; an executor item is "In
  isolated scratch only, inspect and run… **Never edit lane files**".
- The milestone says "build and falsify controls for positive verdict-path calibration". No seat body says
  build, repair, freeze or land a control, and every worker is forbidden lane writes. The only actor that could
  have built one is L1; `predata/` is empty and `corpus/evidence/round59/` holds only `census-start.txt` and the
  byte-identical round-58 receipt. **Measured: no round-59 control exists.**
- `w1-spec.json` (15:14:46) post-dates `w1-dispatch.json` (15:12:11) and replaced the six role bodies with one
  generic body; the per-role text survives only in the dispatch file.

### F8 — dispatch preceded its own pre-data control, and seats report reading a file that did not yet exist

`w1.ready` is 15:12:15; the carried control receipt's mtime is 15:14:30. Two peer reports describe the receipt
as empty at their read time — `R59Scout39.md:5` ("`controls/c1-before.txt` (0 bytes)"), `R59Critic57.md:8`
("the latter contains only an empty line") — while the file is 958 B now and byte-identical to round 58's. I did
not observe those seats' reads and cannot date them, so this is **peer-reported shape** plus my own mtime
evidence: the wave was dispatched before its only pre-data receipt was in place. QUALITY 115's ordering
("before it binds round data") was therefore inverted in time, whatever the file's eventual content.

### F9 — dispatch marker state

At 15:22:15 there is no `w1.ready.dispatched` and no `w1-results.json`; `w1/` holds 54 seat reports and
`w1.ready.partial` is 858 B with 30 `R59…` tokens. Per `corpus/QUALITY.md:941` (criterion 99) the wave is
**not** reported dispatched; the sealed carriage of the round's own evidence is still open.

### F10 — SOURCES and census: unchanged by this seat

133 rows; validator exit 0 with the five pre-existing W04 duplicate-URL warnings (S051, S053, S073, S074, S075);
output matches `census-start.txt`'s warning set and ok line. No row was added, edited or re-statused.

## 3. Draft round-59 Gate wording (for L1 adoption; not a filed Gate)

> ### Gate
>
> **No round-59 claim was frozen.** `corpus/evidence/round59/claims.md` — named by the wave context and by all
> 66 seat bodies — is absent, and the whole round-59 tree is untracked (`git status` → `?? corpus/evidence/round59/`,
> `?? .ufo/waves/round-59/`; `git ls-tree HEAD corpus/evidence/round59` empty). This round files no claim
> verdict; what follows is a reading of round-58 frozen bytes plus the round-59 control state.
>
> **Inherited C1 counter — two-sided calibration failure, re-derived and re-measured.** Frozen
> `corpus/evidence/round58/c1-count.py`: refusal emitters print lowercase `pass` (`:51,160,223,234`) while the
> aggregate requires uppercase `=PASS` (`:391,399`), so `C1=PASS` is unreachable for an honest candidate; a
> rerun on the lane builder reproduces the carried receipt exactly (`OK=4/4 REFUSE=0/7 C1=FAIL`, exit 1; `diff`
> vs `controls/c1-before.txt` differs only by the receipt's `EXIT=1` line). The same substring test reads
> refusal lines that embed the candidate's stderr (`:152,156,222`) — a candidate that prints `=PASS` while
> naming no reason class scores `REFUSE=7/7` with seven legs labelled `fail` (leg-level, frozen functions;
> end-to-end forgery measured by peer seats, `R59Executor02/03`). `:389` is dead code; `HELDOUT_OK`'s
> outside-write snapshot (`:345` vs `:143-145`) is taken after the run and is vacuous.
>
> **Control battery is vacuous under its own predicate.** `claims.md:9` invokes no `--controls`; `:365,382,393`
> then yield `DENIED=0/0` and `denied_pass=True`. The committed `c1-controls.txt` (`DENIED=2/2`) tests only
> "nested stdout has no `C1=PASS`", which the token defect guarantees. No receipt in this round separates a
> conforming builder from a do-nothing builder.
>
> **Inherited C2 counter — unsatisfiable for two independent reasons.** (a) `tools/build-spans.py:142-149`
> writes span-start while `c2-count.py` binds occurrence and byte-compares a rebuild; measured over the 12
> frozen quotes on the 27,012-character S101 form, `occurrence − start = 80` for 12/12, so no manifest satisfies
> both. (b) The target entry `corpus/knowledge/carrier-alphabet-china-r58.md` does not exist; a frozen-counter run
> on this tree prints `C2=FAIL` with `ENTRY_MISSING` and `MANIFEST_MISSING`. Its `S101_NOT_IN_SOURCE` line is a
> cascade of the missing entry (`:55` reads the entry's first line), not a defect in row S101
> (`corpus/SOURCES.md:111`, `mined`).
>
> **Wave shape.** 66 report-only seats (one normalised spec body; six dispatch role templates; 16/14/12/12/7/5).
> No seat may write lane bytes, so the milestone's "build and falsify controls" had no owner below L1 and none
> exists (`predata/` empty; `corpus/evidence/round59/` = census + a byte-identical round-58 receipt).
> `w1-spec.json` (15:14:46) post-dates the dispatch (15:12:11).
>
> **Dispatch and SOURCES.** No `w1.ready.dispatched`, no `w1-results.json` at 15:22:15 → not dispatched
> (QUALITY 99). SOURCES 133 rows, validator exit 0, five pre-existing W04 warnings; no row changed.
> No live fetch (L0 `8d77e6c1` open, fleet `.ufo/l0-questions.md:136,140`).

## 4. Draft round-59 Mistakes wording

> 1. **vacuous — the round froze no claim and its evidence tree is uncommitted.** `corpus/evidence/round59/claims.md`
>    is absent while the dispatch context and all 66 seat bodies instruct seats to read it; `git status` shows
>    `?? corpus/evidence/round59/` and `?? .ufo/waves/round-59/`, and HEAD contains no round-59 path. Captured-by:
>    QUALITY 115 (freeze must precede round data) and 99 (marker discipline). Fix: commit `claims.md` with each
>    counter pinned by sha256 and a must-pass control per claim before `w1.ready`; otherwise file the round as
>    claim-free and do not let seats imply a frozen predicate exists.
>
> 2. **vacuous — the inherited C1 counter cannot discriminate in either direction.** Lowercase refusal emitters
>    (`:51,160,223,234`) against an uppercase aggregate (`:391,399`) make `C1=PASS` unreachable for an honest
>    candidate; the embedded-stderr substring test (`:152,156,222`) makes it reachable for a candidate that
>    prints the token without refusing. Measured here at leg level (`REFUSE=7/7` over seven `fail` lines); peers
>    measured it end to end. Captured-by: QUALITY 115 and 86's positive-control principle. Fix: compare parsed
>    fields, not substrings of a line that embeds child output; freeze one must-pass candidate control and one
>    must-fail forge control inside the predicate command.
>
> 3. **vacuous — the control conjunct never runs under the frozen predicate.** `claims.md:9` passes no
>    `--controls`; `:382/:393` print `DENIED=0/0` and treat a zero denominator as a pass; the committed
>    `DENIED=2/2` run tests only absence of `C1=PASS` from a nested invocation, which the token defect
>    guarantees. Captured-by: QUALITY 103 ("zero rows … is a failure"). Fix: put the control battery in the
>    frozen predicate, and make `total == 0` a failure.
>
> 4. **inherited (depth) — C2 defines `offset` twice, incompatibly, and its entry never landed.** Builder writes
>    span-start (`build-spans.py:142-149`); counter binds occurrence and byte-compares a rebuild; measured
>    `occurrence − start = 80` for 12/12 quotes. `corpus/knowledge/carrier-alphabet-china-r58.md` is absent, so a
>    frozen-counter run yields `ENTRY_MISSING` + `MANIFEST_MISSING` and never reaches the offset question.
>    Captured-by: QUALITY 115's general form. Fix: name one `offset` semantics in builder, counter and span
>    docstring, land the entry, and pin the pair with a must-pass control before re-freezing.
>
> 5. **counting — a derived error is displayed as an independent one.** With no entry, `c2-count.py:55` emits
>    `S101_NOT_IN_SOURCE` even though row S101 exists and is `mined`; `REF_ID_UNBOUND` (`:62`) follows from the
>    same absence. Captured-by: QUALITY 103's "a missing input tree is a failure, never a vacuous pass" — and
>    its converse, that a cascade must not read as N independent defects. Fix: short-circuit downstream checks
>    when an input artefact is missing, and print cascade markers as `SKIPPED(dependency)`.

## 5. Flips (what would settle each finding)

- F1: a counter whose refusal predicate parses `reason`/`rc` fields and rejects child-embedded tokens, shown by
  two controls in one receipt — a conforming builder reaching `C1=PASS` and a token-printing non-refusing builder
  reaching `C1=FAIL` — from the exact predicate command.
- F2: the frozen predicate invokes the control directory, `DENIED` uses a non-zero denominator, and a zero
  denominator is a failure.
- F3: `HELDOUT_OK`'s snapshot taken before its `run_builder`, and the dead `:389` line removed by an append-only
  erratum (frozen bytes not rewritten).
- F4/F5: an entry and a manifest that satisfy one named `offset` semantics, with a must-pass control; plus a
  re-anchoring of the S101 row's char positions against the pinned text form.
- F6: a commit adding `corpus/evidence/round59/claims.md` (counters pinned by sha256) and the round-59 tree.
- F7/F8: seat bodies that own control construction, and a control receipt whose mtime precedes `w1.ready`.
- F9: `w1.ready.dispatched` or `w1-results.json`.

## 6. Checks run (and what was not run)

**Run by this seat, read-only on lane bytes, scratch under `/fast/scratch/hyaku/chousa-r59/R59Scribe20-2/`:**

- `ls`, `stat -c '%y %s %n'`, `wc`, `sha256sum` on the round-59 evidence tree, round-58 control receipts and
  wave files; `diff` of the two `c1-before.txt`.
- `git rev-parse HEAD`, `git status --porcelain`, `git ls-tree -r --name-only HEAD corpus/evidence/round59`
  (read-only; no git/jj write, no index change).
- JSON introspection of `w1-spec.json` (item count, distinct bodies before/after normalising the seat name,
  item keys, `items[19]`) and `w1-dispatch.json` (member count, role histogram, `taskCall.tasks`, role bodies
  for `R59Scribe20`/`R59Reviewer42`).
- Frozen C1 counter end to end on `tools/build-spans.py` (5.4 s), stdout compared by `diff` to
  `controls/c1-before.txt`.
- Frozen C2 counter end to end with `--root` = lane, `--work` = scratch.
- `tools/capture-text.py` on the S101 raw (exit 0; 27,012 characters) and the 12-quote offset derivation.
- Leg-level forgery demonstration: imported the frozen module, called its `expect_refuse` with a child result
  carrying `=PASS` in stderr, and evaluated the frozen `ref_pass` expression on those lines.
- `grep`/`awk` reads of `c1-count.py`, `c2-count.py`, `tools/build-spans.py`, `corpus/QUALITY.md`,
  `corpus/SOURCES.md`, `corpus/evidence/round58/claims.md`, fleet `.ufo/l0-questions.md` (lines 136, 140).
- `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` (exit 0).

**Not run:** no conforming builder was written, so I did **not** produce an end-to-end `C1=PASS` from the
frozen counter — the token-forgery evidence here is leg-level over frozen functions, and the end-to-end forgery
is attributed to peers. No purpose-built token-printing builder either. No `--controls` invocation of the C1
counter (I read the committed receipt instead). No C2 repair attempt. No live fetch (L0 `8d77e6c1` remains
open). No install, no pacman, no registry/fleet/lane write, no write outside this report and scratch.

## 7. Non-claims and limits

- This report asserts **no round-59 claim verdict**, no axis score change, and no dispatch of the wave.
- F6's finding is about artefact presence, not about intent: I do not claim who failed to freeze the claims.
- F8 relies on peers' quoted descriptions of an earlier file state; I could not date their reads.
- F5's S101 anchor note is scoped to the current text-form pin; I did not reconstruct the 2026-10-25 form.
- The `w1.ready.partial` roster and the 54-report count are a snapshot at 15:22:15; the wave was still running.
- Peer findings are labelled as such throughout; none is adopted as this seat's measurement.

## 8. Touched surfaces

- Written: `.ufo/waves/round-59/w1/R59Scribe20.md` (this file), and nothing else in the lane.
- Scratch: `/fast/scratch/hyaku/chousa-r59/R59Scribe20-2/` (receipts `c1-now.txt`, `c1-now.err`,
  `c2-now.txt`, `s101.txt`, `forge-demo.txt`, work dirs `c1run/`, `c2run/`), removed before yield. Never `/tmp`.

Relative to lane root: `.ufo/waves/round-59/w1/R59Scribe20.md`
