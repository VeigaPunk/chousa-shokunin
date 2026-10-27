# R59Scribe19 — round-59 Gate / Mistakes wording, evidence-backed (report only)

Seat: scribe, axes `depth`. Lane root `/home/vgpnk/Projects/shokunin/chousa-shokunin`.
This file is my only lane write. Scratch `/fast/scratch/hyaku/chousa-r59/R59Scribe19/` was created for one
derivation and removed before yield (§7). No lane file, claim, counter, control, SOURCES row, SCORECARD,
LOG, QUALITY or considerthese byte was modified. No fetch, no install, no git/jj command (read or write) was
run by this seat.

Task as seated: read the round-58 lesson and the round-58 verifier spot-check, then draft evidence-backed
round-59 `## Gate` / `## Mistakes` (and report) wording. I did that, and I verified the round-58 numerals I
inherited instead of copying them.

## 0. Commands actually run (verbatim where short)

```
read corpus/evidence/round59/claims.md
    → Path not found (checked first; re-checked at 15:23:10-03:00 — still absent)
ls -la corpus/evidence/round59/ corpus/evidence/round59/controls/
    → round59/: census-start.txt (535 B), controls/
      round59/controls/: c1-before.txt (958 B) — nothing else
find corpus/evidence/round59 -type f -printf '%p %s\n'
    → the same two files, no .py, no counter, no control builder, no claim text
md5sum corpus/evidence/round58/controls/c1-before.txt corpus/evidence/round59/controls/c1-before.txt
    → 52026fede3340219efd39fca2f6fc3a6a  (both files)
diff  <round58 c1-before> <round59 c1-before>   → IDENTICAL; both 16 lines
stat -c '%n %y'  corpus/evidence/round59/{census-start.txt,controls/c1-before.txt}
    → census-start 2026-10-27 15:12:21 -0300; controls/c1-before.txt 2026-10-27 15:14:30 -0300
cat .ufo/waves/round-59/w1.ready            → {"lane":"chousa","round":59,"wave":"w1", ... "l1":"ChousaR59"}
cat .ufo/waves/round-59/w1.ready.partial    → 21 seats listed (mtime 15:19:31 -0300)
ls .ufo/waves/round-59/                     → predata/ (empty), w1/, w1-dispatch.json, w1-spec.json,
                                              w1.ready, w1.ready.partial
                                              (no w1.ready.dispatched, no w1-results.json)
python3 - <<'PY' (json read of w1-spec.json)
    → 66 items; 66/66 item texts name corpus/evidence/round59/claims.md; axes {depth, operability, calibration}
wc -l corpus/evidence/round58/{c1-count.py,c2-count.py}   → 406, 165
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md → 133
sed -n '51p;160p;223p;234p;391p;399p' corpus/evidence/round58/c1-count.py
    → PASS = "pass" · return f"{name}={PASS}(refused)" · FOREIGN={PASS}(refused) ·
      SYMLINK_OUT={PASS}(refused) · ref_pass = all(("=PASS" in l) ...) · REFUSE={sum('=PASS' ...)}
grep -n 'ref_legs = \[\|ok_legs = \[\|ok_pass = all\|verdict = "PASS"' corpus/evidence/round58/c1-count.py
    → 384, 386, 389+390, 391, 394
sed -n '300,360p' corpus/evidence/round58/c1-count.py   → MANY_QUOTES/FIFO/DEVZERO/FAT_RAW use expect_refuse
python3 -B tools/capture-text.py corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw > $S/form.txt
    → rc=0; 47,356 B; 27,012 chars; sha256 a8e3e7ad…f7e79f867
sha256sum tools/capture-text.py corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw
    → 2c0140bc…03e2573 and 6063a3af…6d9fddf3 (both equal to the round-58 frozen pins)
python3 offset recomputation over c2/quotes.tsv against form.txt (see §2.3)
```

Not run by this seat, and not claimed: `round58/c1-count.py`, `round58/c2-count.py`, any builder,
`scripts/sources-census.sh validate`, `git`/`jj`, any install. Where I need those results I say so and
attribute them (recorded receipt or peer report).

## 1. Round-58 lesson and spot-check, re-verified against bytes

| Claim in `corpus/lessons/round-58.md` / `round-58-verifier-spotcheck.md` | This seat's check | Result |
|---|---|---|
| `c1-count.py` 406 lines | `wc -l` | 406 — agree |
| `c2-count.py` 165 lines | `wc -l` | 165 — agree |
| SOURCES rows 133 at both ends | counting command in the spot-check | **133 today**; I did not re-run the row count at the round-58 revision (no git use), so only the current-tree figure is mine |
| C1 defect at lines 51, 160, 223, 234, 391, 399 | direct line read | exact match, including `PASS = "pass"` at :51 and the uppercase `=PASS` aggregate at :391/:399 |
| "a scratch builder reports all 11 safe/refusal legs as passing, yet … `REFUSE=0/7`, `C1=FAIL`" | `R58ScribeMistakeMine.md:57-83` re-read (132-line file exists) | the transcript shows `EMPTY_OK=pass` … `FOREIGN=pass(refused)` … `HELDOUT_OK=pass`; consistent |
| "independently re-derived by `R58ExecC1CounterAudit.md`" | file exists (95 lines); `R58ReviewFrozenClaims.md:25-37` re-read | both witnesses exist and state the same mechanism, including the dead assignment at :389 |
| S101 quote at char 797 | re-derived from committed raw (§2.3) | **797 — reproduced**, quote `并以[文献类型标识/载体类型标识]表示`, count 1 |
| census exit 0 with five W04 warnings | read `corpus/evidence/round59/census-start.txt` (recorded receipt) | five W04 lines (S051, S053, S073, S074, S075), `ok`, `exit=0`; **validator not re-run by me** |
| lesson `## Mistakes` item 1 is complete prose | `read :26-26:raw` | complete; ends "…still returns `C1=FAIL` under the frozen counter." |

Conclusion: the round-58 lesson and spot-check are faithful to the bytes on every numeral this seat could
re-check without executing a counter or a git command. I found no inflation to report.

One wording correction worth carrying: the spot-check says the C1 aggregate "expects uppercase `=PASS` while
refusal output is lowercase `=pass`". That is true, but it understates the defect — §2.1 shows the aggregate
is not a status comparison at all, and §2.2 shows the second half of the same predicate is reachable by the
wrong input.

## 2. Evidence this seat added

### 2.1 The frozen C1 predicate is a substring test, not a leg-status test

Refusal-leg lines can only be produced by four sites, and all of them emit the lowercase `PASS` constant:

| site | line | literal |
|---|---|---|
| `expect_refuse` (SYMLINK_CACHE, FIFO_TXT, DEVZERO_TXT, FAT_RAW, MANY_QUOTES) | :160 | `return f"{name}={PASS}(refused)"` |
| FOREIGN | :223 | `legs.append(f"FOREIGN={PASS}(refused)" …)` |
| SYMLINK_OUT override | :234 | `legs[-1] = f"SYMLINK_OUT={PASS}(refused)"` |
| constant | :51 | `PASS = "pass"` |

while the aggregate tests `ref_pass = all(("=PASS" in l) for l in ref_legs)` (:391) and counts
`REFUSE={sum('=PASS' in l …)}/…` (:399). `ref_legs` is selected by leg name (:386), not by status.

Consequence 1 (satisfying builder): for a builder that refuses all seven hazards, FOREIGN/SYMLINK_OUT lines
contain `=pass` and the other five `=pass(refused)`; no refusal line can contain `=PASS`, so
`ref_pass` is always `False` and `C1=PASS` (verdict at :394) is unreachable. This is unconditional and is a
static proof from the frozen source; the round-58 scratch probe is consistent with it.

Consequence 2 ([INFERENCE] — derived from source, **not executed**): the same substring test is reachable
by an *unsafe* builder. `expect_refuse`'s reason-absent branch embeds the builder's stderr —
`f"{name}={FAIL}(rc=…, reason {reason_classes!r} absent in {err[:160]!r})"` — so a builder that exits
non-zero and prints the literal `=PASS` (with none of the hazard words) turns each FAIL line into a line that
contains `=PASS`. For SYMLINK_OUT the correct-refusal branch is overwritten with lowercase `pass(refused)`
(:233-234), so the only quoting route for that leg is the *hazard* branch, `(target-dir-written!)`. A builder
that writes into the symlink target and prints `=PASS` would therefore be counted as 7/7 refusals and could
print `C1=PASS` with every refusal leg reading `fail`. The frozen predicate can thus certify a builder the
claim forbids — it is not sound, not merely unsatisfiable.

Unrun flip for either consequence (assigned to a counter-running seat, not this one): construct the two
builders in scratch and run `python3 corpus/evidence/round58/c1-count.py --builder <b> --work <fresh>`.
Prediction: correct builder → all legs `=pass`, `REFUSE=0/7`, `C1=FAIL`, exit 1; token-printing unsafe
builder → all seven refusal legs contain `fail`, `REFUSE=7/7`, `C1=PASS`, exit 0. If the second run does not
print `C1=PASS`, this inference is falsified and should be dropped.

Wording consequence for round 59: QUALITY 115's "positive control that reaches the declared final verdict"
is necessary but not sufficient. The control must reach the verdict **with every leg in its declared pass
state**, and the counter must read the leg's own status field rather than search the line for a token.
Otherwise a positive control can be satisfied by token collision, which is the exact defect class QUALITY 114
records for the C3 provenance counter.

### 2.2 The frozen C2 predicate cannot be satisfied by any artifact (recomputed, 12/12)

- `c2-count.py:101` requires the manifest `offset` column to equal the quote's **occurrence** offset:
  `if url!=URL or digest!=RAW_SHA or len(occurrences)!=1 or occurrences[0]!=off: CAPTURE_BIND`.
- `c2-count.py:105-107` builds the expected span from that same `off`: `start=max(0,off-80)`.
- the pinned builder (and current `tools/build-spans.py`) writes the **span start**:
  `start = max(0, off - CONTEXT)` (`:142`) and `lines.append(… str(start) …)` (`:149`).
- `c2-count.py:124-129` then requires the rebuilt `spans.tsv` to be **byte-identical** to the committed
  manifest, i.e. to contain the builder's span-start offsets.

So builder-produced manifest → `CAPTURE_BIND` fails on every row; occurrence-offset manifest →
`BUILDER_REBUILD_MISMATCH`. My arithmetic over the frozen quote set (§2.3) shows the conflict is present on
**12/12 rows**, not on an edge case: every quote occurs at an offset > 80, so `occurrence ≠ span_start` in
all twelve rows (offsets 315, 330, 590, 683, 734, 781, 797, 838, 965, 993, 1460, 11723 vs span starts
235, 250, 510, 603, 654, 701, 717, 758, 885, 913, 1380, 11643).

The rest of the frozen C2 legs would pass: all 12 quotes occur exactly once in the defined form, and
**3/12** are line-start bound, satisfying the `ANCHOR_BOUND=3/3` floor. The predicate is therefore blocked
only by the mutually exclusive offset convention — a counter-authoring defect, not a source problem.

### 2.3 Independent re-derivation of the S101 defined form (offline, no fetch)

From the committed lane capture only:

- raw sha256 `6063a3aff7a4081e93a685f2721e2cd6b477ba84a841211e298bcddd6d9fddf3` (matches the round-58 claim);
- `tools/capture-text.py` sha256 `2c0140bc04029c8faedc6c89a65bd657430d8b85f433406946567b70303e2573`
  (matches the round-58 pin);
- defined text form: 47,356 B / 27,012 chars, sha256 `a8e3e7ad213b6ec50479542cda23612e7ae7ae5fd4506fba53a91f2f7e79f867`;
- all twelve occurrences and offsets reproduce `corpus/evidence/round58/s101-open.txt` exactly, including
  `并以[文献类型标识/载体类型标识]表示` at character 797.

This is the only offline source evidence this seat verified. It confirms the round-58 *opening receipt*; it
does not admit the C2 knowledge entry and does not re-open S101 as a live source (fetch-scope L0 `8d77e6c1`
remains open).

### 2.4 Round-59 pre-data state — the Gate blocker

1. **The frozen artifact the round was dispatched on does not exist.** `corpus/evidence/round59/claims.md`
   is named as frozen and required "before work" by the wave context and by **66/66** seat items
   (`w1-spec.json`; same text in `w1-dispatch.json` `taskCall.context`). It is absent from the lane tree at
   every check, including the last at 15:23:10-03:00. `corpus/evidence/round59/` contains exactly
   `census-start.txt` and `controls/c1-before.txt`.
2. **The round-59 pre-data control is not a round-59 measurement.** `controls/c1-before.txt` is byte-identical
   (md5 `52026fede3340219efd39fca2f6fc3a6a`) to `corpus/evidence/round58/controls/c1-before.txt`, whose mtime
   is 14:06:59 on the same day. Its only new information is its own mtime (15:14:30). It carries no command
   line, no counter revision and no builder pin, so it cannot be tied to any round-59 candidate.
3. **No positive verdict-path control exists for round 59.** `controls/` has one file. There is no
   PASS-reaching receipt, no REFUSEALL control, no builder, and no counter — the exact gap QUALITY 115
   requires be closed *before* a freeze. The only round-59 "before" receipt shows `OK=4/4 REFUSE=0/7
   BEFORE_FOREIGN=deleted DENIED=0/0`, `C1=FAIL`, `EXIT=1`, i.e. the round-58 before-state.
4. **Sequencing is inverted relative to round 58.** `w1.ready` (dispatch marker) is at 15:12 and
   `w1.ready.partial` at 15:19:31, while the claims file has not appeared; round 58 froze claims at
   `9e73a031…` before dispatch. Whatever L1 intended, wave-1 seats were dispatched onto a missing freeze.
5. **Scope of the census receipt.** `corpus/evidence/round59/census-start.txt` differs from the round-58
   start receipt only in the final line (`EXIT=0` → `exit=0`) and, unlike `round58/census-end.txt`, carries
   no `Command:` line. I record it as a receipt of unknown provenance and did not re-run the validator.

## 3. Draft `## Gate` for `corpus/lessons/round-59.md`

> Use as-is if the claims never land; keep the bracketed branch if they land later.

```markdown
## Gate

### Frozen input — absent at dispatch (blocker, not a result)

- The wave context and all 66 W1 seat items name `corpus/evidence/round59/claims.md` as frozen and
  required "before work" (`.ufo/waves/round-59/w1-spec.json` context; `.ufo/waves/round-59/w1-dispatch.json`
  `taskCall.context`). The path is absent from the lane-visible tree at every check this round: the
  round-59 evidence directory contains exactly `census-start.txt` (535 B, 7 lines) and
  `controls/c1-before.txt` (958 B, 16 lines). No claim text, frozen counter, control builder or
  positive-verdict receipt exists for round 59.
- Sequencing: `w1.ready` is stamped 2026-10-27 15:12 and `w1.ready.partial` 15:19:31, both before any
  claims artifact; round 58 froze claims at `9e73a031ab1ac3bac343de008850d7d87f9e5634` before dispatch.
- [If claims land later: record the claims commit and sha256 here, re-check that the file the seats were
  told to read is the file that was frozen, and re-state this Gate against it. Do not bind wave data
  produced before the freeze to the later claims.]

### Pre-data controls

- `corpus/evidence/round59/controls/c1-before.txt` is byte-identical (md5
  `52026fede3340219efd39fca2f6fc3a6a`) to the round-58 before receipt, so it is a carried base-state
  receipt, not a measurement of a round-59 candidate; it carries no command line, counter revision or
  builder pin.
- No positive verdict-path control was filed. QUALITY criterion 115 requires one, reaching the declared
  final verdict with every leg in its declared pass state, before a counter binds round data. That
  requirement is unmet, so no round-59 verdict can be calibrated—positive or negative.

### Carried defects (not repaired in round 59 pre-data)

- C1/round58 counter: the aggregate is a substring test (`corpus/evidence/round58/c1-count.py:391,399`
  search `=PASS`; refusal emitters at :51,:160,:223,:234 write `=pass`). Unreachable for a satisfying
  builder; reachable only via token collision in an embedded error string (see the round-59 lesson's
  Mistakes row). No revised counter was frozen.
- C2/round58 counter: `CAPTURE_BIND` requires occurrence offsets (`c2-count.py:101`) while byte-identical
  rebuild requires the pinned builder's span-start offsets (`tools/build-spans.py:142,149`); conflict on
  12/12 frozen rows. No revised counter was frozen.

### Source opening

- No source was opened and no fetch was made; the fetch-scope L0 `8d77e6c1` remains open. The only
  source-adjacent check this round is a read-only re-derivation of the S101 defined form from the
  committed capture (§2.3 of the seat report), which reproduces the round-58 opening receipt and admits
  nothing new.
```

## 4. Draft `## Mistakes` for `corpus/lessons/round-59.md`

```markdown
## Mistakes

1. **vacuous — the round was dispatched without its frozen claim artifact.** Evidence: the wave context
   and 66/66 seat items require `corpus/evidence/round59/claims.md` "before work"; the path is absent and
   `corpus/evidence/round59/` holds only `census-start.txt` and `controls/c1-before.txt` (W1 `R59Scribe19.md`
   §2.4; independently recorded by `R59Scribe22.md`, `R59Critic55.md`, `R59Reviewer42.md`). Captured-by: the
   seat gate is prose, not a check — nothing asserted the file existed with a digest before `w1.ready`.
   Fix: freeze claims, then emit `w1.ready` only after a gate command fails closed when the file is absent
   or its sha256 differs from the recorded freeze. Do not back-fill claims after wave data and bind the
   wave's reports to them.

2. **vacuous — the round-59 pre-data control is a byte-for-byte copy of round 58's, so the
   positive-verdict requirement was again unmet.** Evidence: `md5sum` of round-58 and round-59
   `controls/c1-before.txt` is `52026fede3340219efd39fca2f6fc3a6a` for both; the round-59 controls
   directory contains that file and nothing else — no builder, no REFUSEALL, no PASS-reaching receipt.
   Captured-by: `corpus/QUALITY.md` criterion 115, which was added precisely to require a must-pass
   positive control before a freeze. Fix: file a positive-verdict receipt before dispatch and name the
   command, counter revision and builder pin in it; a negative before-state may be carried, but it cannot
   stand in for the positive leg.

3. **misleading — the frozen C1 predicate is a substring test, so it false-kills a correct builder and can
   be made to certify an unsafe one.** Evidence: `corpus/evidence/round58/c1-count.py:51,160,223,234` emit
   lowercase `=pass`; :391/:399 test uppercase `=PASS` over legs selected by name (:386); :394 is the only
   verdict line. Static consequence: a builder that correctly refuses all seven hazards can never print
   `C1=PASS`. [INFERENCE, not executed] the reason-absent branch embeds builder stderr, and SYMLINK_OUT's
   correct-refusal branch is overwritten with lowercase `pass(refused)` (:233-234), so the only quoting
   route for that leg is `(target-dir-written!)` — a builder that writes the symlink target and prints
   `=PASS` would be counted 7/7 refusals and could print `C1=PASS` with every refusal leg reading `fail`.
   Captured-by: criteria 114/115 (a counter must not accept a self-authored token) and 86 (positive
   control seeded with the mangle class). Fix: parse each leg's status field; never search free text for a
   verdict token; re-freeze the counter before any further C1 claim.

4. **blocking (carried, not repaired) — the C2 predicate's offset column is doubly specified.** Evidence:
   `c2-count.py:101` requires the quote occurrence in `offset`, :105-107 derives the expected span from it,
   while `tools/build-spans.py:142,149` writes the span start and :124-129 requires a byte-identical
   rebuild. Recomputed over the frozen rows: all 12 quotes occur past offset 80, so occurrence ≠ span start
   on 12/12 rows (occurrences 315…11723; span starts 235…11643); the 3/12 line-start anchors would
   otherwise satisfy the predicate. Fix: one documented meaning for `offset`, stated in the counter and the
   builder from the same constant, and a rebuild leg that compares spans rather than re-deriving the
   manifest's offset column.
```

Both rows 3 and 4 are carried defects: round 59 did not introduce or repair them, and the lesson must say so
rather than imply a repair. If any seat does produce a repaired counter this round, the lesson should cite
that counter's receipt and revise only the "carried, not repaired" clause — append-only, per criterion 3.

## 5. Draft report wording (round-59 fleet report)

If the wave settles with no claims artifact, these are the sentences that keep the report honest:

- Work performed: "Round 59 was dispatched onto a frozen-claims path that does not exist …
  No claim was bound, no after-state exists, and no axis is claimed to have moved. 66 W1 seats were
  dispatched; [N] reports exist; [state what the wave actually measured, e.g. counter falsification
  candidates], none of which can be promoted past `unprovable` without a freeze."
- Before → after table: both rows read **unprovable** with the reason "no frozen claim/predicate/receipt
  exists for round 59", and must not borrow round 58's numbers as if they were round-59 measurements.
- Sources & frontier: "Rows [n] → [n]; census end receipt at path; validator [re-run by the integration
  seat / not re-run — say which]. No source opened; no fetch; L0 `8d77e6c1` open."
- Trend verdicts: expansion/quality/discernment all **unchanged** unless a wave seat supplies
  non-author evidence that actually binds; the round-58 spot-check's `discernment improved` belongs to
  round 58 and must not be restated here.
- SHONEN: four `[~]` lines, each a lane assertion; do not mark any box `[x]` on the strength of this round.
- Closure conformance: record the routed self-defect ("claims freeze did not precede dispatch; positive
  control again absent; C1/C2 counters still unsatisfiable") and the exact commit that carries it.
- Forbidden claims, verbatim: "C1 is fixed", "the positive control passed", "the counter now reaches
  `C1=PASS`", "operability improved", "C2 depth admitted" — none is available from these bytes.

## 6. Limits and what I did not verify

- I did not execute either frozen counter, any builder, or any control. §§2.1-2.2 are static source reads
  plus arithmetic over the frozen quote set; §2.1's second consequence is labelled `[INFERENCE]` and has a
  stated falsifier.
- I did not re-run the census validator; the five W04 warnings and `exit=0` are quoted from the recorded
  receipt.
- I did not run `git`/`jj`; the lane HEAD `af8c0a460d087cbfb8245fb9326608783ccc510b` and the untracked-state
  observation in `R59Scribe22.md` are peer-reported, not mine.
- The wave was still in flight when I filed (21 of 66 seats dispatched per `w1.ready.partial` at 15:19:31).
  A claims file appearing after 15:23:10-03:00 would not falsify §2.4's sequencing finding but would change
  the Gate's first branch; the lesson must re-check the path and its digest at write time.
- Scope held: no lane modification, no counter/claim edit, no SOURCES/SCORECARD/LOG/QUALITY/considerthese
  write, no fetch, no install (so no `RULES.md` install path was exercised).

## 7. Scratch

`/fast/scratch/hyaku/chousa-r59/R59Scribe19/` held `form.txt` (the derived S101 form, 47,356 B) and nothing
else; it was removed before yield. No `/tmp` path was used for evidence.
