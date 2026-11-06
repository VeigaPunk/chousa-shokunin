# R82ExecRepro — independent reproduction of round-82's frozen claims (C1 operability, C2 depth)

Seat: `R82ExecRepro`, wave w1 round 82. Leaf: no dispatch, no lane mutation, no network (this seat's item names no
re-open, so zero GETs were made). Everything below is measured from committed bytes, in trees made with
`git -C /home/vgpnk/Projects/shokunin/chousa-shokunin archive <rev> | tar -x -C <scratch>`; scratch was
`/fast/scratch/hyaku/chousa-r82/R82ExecRepro/` (removed before yield; every receipt was copied to this folder first).
Receipts live beside this file in `.ufo/waves/round-82/w1/R82ExecRepro/`.

Revisions: base `38f5af82…` (prefreeze tree), freeze `57c0d167…` (claims + controls + pins), landing `b4a41d25…`
(the bytes under attack). All three trees extracted; landing and freeze trees 349 MB each.

## 0. Headline

- **(a)(b)(c)(d) all reproduce exactly.** Instrument pins, before/after predicates, the 280-case selftest, the
  committed control driver's 14/14 and all 14 receipt bodies match; the Run lines are byte-identical to base.
- **C1 K2 (generalization) fires.** A record that is `item2-pass.md` with exactly one cell changed — the claim's
  `sweep` cell — to a declared-vocabulary value, while the `## Sweeps` row still carries that claim, exits **0** on
  the frozen item-2 Run line. 30/30 declared-vocabulary values pass, including the empty cell. Evidence in §5.1;
  the counter-argument (the gate resolves the sweep by `claim_id`) is stated there too, so the L0 can weigh the
  letter of K2(a) against the gate's own comment.
- **C2 K2 holds** on independent re-derivation (11/11 quotes located, 4/4 capture sha256 = refetch row). C2 K1 and K4
  hold. C2 K3 (row follows from its quote) is a non-author reviewer's call, not mine.

## 1. (a) Instrument identity — `git show <rev>:<path> | sha256sum` for every path in `instrument-pins.txt`

Command (loop over the seven pins plus the `c1-records` aggregate; the aggregate is `sha256sum * | sha256sum` inside
`corpus/evidence/round82/c1-records/`, reproducing the pin file's own formula):

```
git -C <lane> show <rev>:<path> | sha256sum
```

| path | 38f5af82 | 57c0d167 | b4a41d25 | pin |
|---|---|---|---|---|
| `corpus/evidence/round82/k2-gate-r82.py` | 4d6ba055…ab3af | 4d6ba055…ab3af | 4d6ba055…ab3af | match |
| `corpus/evidence/round82/depth-r82.py` | 726d3ed9…eb6de | 726d3ed9…eb6de | 726d3ed9…eb6de | match |
| `corpus/evidence/round82/run-controls-r82.sh` | 74940be2…babc8 | 74940be2…babc8 | 74940be2…babc8 | match |
| `corpus/evidence/round82/c1-manifest.tsv` | 16ab5682…8a799 | 16ab5682…8a799 | 16ab5682…8a799 | match |
| `corpus/evidence/round82/base-knowledge.txt` | 9d5dcc0d…2dcc2 | 9d5dcc0d…2dcc2 | 9d5dcc0d…2dcc2 | match |
| `tools/research-gate.sh` | d5d48128…24d41e2 | d5d48128…24d41e2 | **0d8ac50f…570d92a** | diff at landing (expected) |
| `SKILL.md` | f34e8b33…b6f709 | f34e8b33…b6f709 | **43e9b5ed…47268676** | diff at landing (expected) |
| `corpus/evidence/round82/c1-records/*` (49 files) | f3e5dca7…74aea7a5 | f3e5dca7…74aea7a5 | f3e5dca7…74aea7a5 | match |

Receipt: `pins.txt` (command output verbatim). The only two landing diffs are the two paths the claim expects to move
(the gate and SKILL.md prose); the counters, manifest, base list and all 49 fixture records hold their prefreeze bytes
into the landing commit.

**Run-line byte identity.** Extracting the first backtick span after `  - Run: ` under checklist items 2 and 4:

- item 2 (168 bytes, sha256 `7a02d696…67d7b`): `f=<record.md>; ! bash tools/research-gate.sh verify "$f" --root . | grep -q '^FINDING NEGATIVE_WITHOUT_SWEEP' && bash tools/research-gate.sh verify-sweeps "$f" --root .`
- item 4 (62 bytes, sha256 `788fb8c5…22ce7`): `bash tools/research-gate.sh verify-sweeps <record.md> --root .`

Both identical at `38f5af82` and `b4a41d25`; `RUNLINES_IDENTICAL= 2 /2`. The SKILL.md change is entirely in the prose
**after** each Run span's closing backtick (suffix 648→904 bytes on item 2, 453→645 on item 4, a "Round 82: …" note):
`prefix_through_closing_backtick_identical=True`, `suffix_identical=False`. Receipts: `runlines.txt`,
`skill-runline-split.txt`, `diff-SKILL-base-landing.txt`.

## 2. (b) BEFORE and AFTER predicates

```
python3 -B <tree>/corpus/evidence/round82/k2-gate-r82.py --root <tree>
python3 -B <tree>/corpus/evidence/round82/depth-r82.py --root <tree>
```

**Before** (`38f5af82`, receipt `before-c1-k2-gate.txt` / `before-c2-depth.txt`):

```
MANIFEST_SHA256=16ab568268947a738354f894b59a6b46cb7687792bb388842accf9c044c8a799 RECORDS_DIGEST=7dc17486ed99c0e0a0410cb5970cf8595c235c18c9c7cf05ea12ca608f8e1bf7 rows=50
RUNLINES=2/2 K2_REFUSED=0/11 HOLD_REFUSED=9/9 CLASS_REFUSED=2/24 POSITIVE=5/6
K2_GATE=FAIL
rc=1
```
```
DEPTH_R82 entries=0 ok_entries=0 rows=0 located_quotes=0 fresh_sources=0
DEPTH_R82=FAIL
rc=1
```

**After** (`b4a41d25`, receipt `after-c1-k2-gate.txt` / `after-c2-depth.txt`):

```
RUNLINES=2/2 K2_REFUSED=11/11 HOLD_REFUSED=9/9 CLASS_REFUSED=24/24 POSITIVE=6/6
K2_GATE=PASS
rc=0
```
```
ENTRY question-framing-frames-r82.md ok=yes rows=9 quotes=11/11 fails=-
DEPTH_R82 entries=1 ok_entries=1 rows=9 located_quotes=11 fresh_sources=4
DEPTH_R82=PASS
rc=0
```

Both are the exact predicate lines in `claims.md` (C1 target: the exact fractions plus `K2_GATE=PASS`, rc 0;
C2 target: `entries=1 ok_entries=1`, `rows` ≥ 5, `located_quotes` ≥ 5, `fresh_sources` ≥ 3 — observed 9, 11, 4).

**Cross-check against committed receipts** (bodies, `#` header lines excluded because they carry the archive path):
`diff` of committed `corpus/evidence/round82/controls/c1-k0-donothing.txt` vs my before run → identical;
`controls/c2-d0-donothing.txt` → identical; `after/c1-after.txt` → identical (all 50 `K2CASE` rows, incl. every
`rc=`/`findings=` value); `after/c2-after.txt` → identical.

## 3. (c) Gate selftest at landing, once

```
cd <tree>/tools/.. && bash tools/research-gate.sh --selftest
```
Observed: `RESEARCH_GATE_SELFTEST: PASS (280 cases, 0 skipped)`, `rc=0`, wall 247 s (receipt
`after-c1-selftest.txt`, all 280 `ok-case` lines retained; cases 276–280 are the five the round adds:
`env-pin-override-missing`, `env-pin-override-fake`, `pin-bash-path-shim`, `bash-pin-override-missing`,
`bash-pin-override-fake`). K4's three conditions (PASS, no skip, ≥ 275) all hold; 280 = 275 + 5.
Committed `after/c1-selftest-after.txt` carries the same summary line.

## 4. (d) Committed control driver, re-run from `57c0d167`

**LANE resolution.** The driver computes `LANE=$(cd "$(dirname "$0")/../../.." && pwd)`. Run from the plain archive
(`cwd = <archive of 57c0d167>`), `dirname` is `<tree>/corpus/evidence/round82` and `../../..` is the **scratch tree**,
which is not a git repository: `git -C <tree> archive REV` printed `fatal: not a git repository` and `tar: This does not
look like a tar archive` for every control. Receipt: `controls-rerun-archived.txt` (all rows `ERROR`). It does **not**
resolve to the lane.

**Adapted run.** The driver's bytes are pinned (`74940be2…` at 57c0d167 and identical at the lane HEAD copy), so I
re-ran the same committed script from a `git clone --shared` of the lane checked out at `57c0d167` (clone top-level
asserted: `git rev-parse --show-toplevel` → the clone), `cwd = <clone>`, `HYAKU_SCRATCH=/fast/scratch/hyaku/chousa-r82/R82ExecRepro`,
`OUTDIR` = this folder's `controls-rerun/`. Then `git -C <clone> archive 38f5af82…` archives from the lane's own
objects, and the `c2-controls` overlays come from the clone's checkout of the freeze revision.

```
HYAKU_SCRATCH=<scratch> bash <clone>/corpus/evidence/round82/run-controls-r82.sh 38f5af82… <out>/controls-rerun
```
```
c1-k0-donothing FAIL FAIL   c1-f1-blanket-refuse FAIL FAIL   c1-f2-wrong-finding-keyed FAIL FAIL
c1-f3-keyed-runline FAIL FAIL   c2-d0-donothing FAIL FAIL   c2-d1-r81-filler FAIL FAIL
c2-d2-fabricated-quotes FAIL FAIL   c2-d3-stale-r81-sources FAIL FAIL   c2-d4-duplicate-cells FAIL FAIL
c2-d5-four-rows FAIL FAIL   c2-d6-placeholder-cells FAIL FAIL   c2-d7-unregistered FAIL FAIL
c2-p1-positive PASS PASS   c2-b1-salad-boundary PASS PASS
CONTROLS_AS_EXPECTED=14/14
rc=0
```

`diff corpus/evidence/round82/controls/summary.tsv <out>/controls-rerun/summary.tsv` → identical;
per-receipt body diff over all 14 `*.txt` (lines not starting `#`) → `RECEIPTS_IDENTICAL=14/14`
(`controls-rerun-diff.txt`). The only difference anywhere is the `# cmd:` header's scratch path, which the driver
builds from `HYAKU_SCRATCH` (mine nested `chousa-r82/R82ExecRepro/chousa-r82/controls` vs the committed
`chousa-r82/controls`) — cosmetic, not a verdict line.

## 5. Attacks (beyond the required reproduction)

### 5.1 C1 K2(a) — FIRES: a declared-vocabulary claim-`sweep` cell passes when a `## Sweeps` row carries the claim

Frozen K2(a) verbatim: *"any record, authored by anyone, that (a) differs from `item2-pass.md`, `item4-pass.md` or
`sweeps-r5.md` in one reason, flip-condition, `where` or claim-`sweep` cell set to a declared-vocabulary value … on
which the frozen item-2 or item-4 Run line exits 0 at the landing revision → C1 falsified."*

Deciding record: `item2-pass.md` with exactly one cell changed (`diff`, one line):

```
-| N1 | negative | … | corpus/fixtures/sweeps-r5.md | observed-in-dump | W1 |
+| N1 | negative | … | corpus/fixtures/sweeps-r5.md | observed-in-dump | n.a |
```
(the `## Sweeps` row `| W1 | N1 | … | zero matches |` is untouched.)

Command (frozen item-2 line, record inside the landing tree, relative path, cwd = tree root — counter semantics):

```
cd <landing tree>; f=corpus/evidence/round82/probe-k2a-sweepcell.md
{ ! bash tools/research-gate.sh verify "$f" --root . | grep -q '^FINDING NEGATIVE_WITHOUT_SWEEP' \
  && bash tools/research-gate.sh verify-sweeps "$f" --root .; }; echo $?
```
Observed `0`, and the sweeps mode prints:
`VERIFIED_SWEEPS=1/1 REJECTIONS_OK=1/1` / `RESEARCH_GATE: CLEAN (… findings=0 drift=0)`.
Receipts: `c1-k2-deciding-record.txt`, `c1-k2-claim-sweepcell.txt`.

Scale of the hole — every declared-vocabulary value in the `## Claims` `sweep` cell, with the row intact, exits 0:

```
DECLARED_VALUE_CLAIM_SWEEP_PASSES=30/30 values=['', '-', '--', '---', '—', '–', 'n/a', 'N/A', 'na', 'n.a',
 'none', 'nil', 'null', 'tbd', 'tba', 'todo', '?', '??', '...', '…', 'x', 'unknown', 'not applicable',
 'same', 'ditto', 'see above', 'idem', 'n/a.', '`n/a`', '_none_']
```

Why it is uncovered: every claim-sweep class fixture in `c1-records` also removes or breaks the row
(`v2-sweepcell-*-nosec` deletes `## Sweeps`; `v2-sweepcell-w9-withsec` repoints `W1`'s `claim_id` to `N7`), so the
counter's 24/24 never exercises "placeholder cell **with** an intact carrying row". The gate's own code comment
(`tools/research-gate.sh`, sweeps-mode block) documents the resolution rule as *"its sweep cell names a declared
sweep id, **or** a sweep row's claim_id … is the claim's id"* — i.e. the implementation deliberately accepts my
record, while the landing `SKILL.md` item-2 prose says *"a negative claim whose sweep cell names no sweep row the mode
re-ran (an undeclared id, a header-only `## Sweeps`, a placeholder) is `SWEEP_NEGATIVE_UNRESOLVED`"*. Reported plainly:
**under K2(a)'s letter, C1 is falsified by this record**; the defensible counter-reading is that the sweep *was*
re-run via `claim_id`, so the placeholder cell is inert. Both readings are on the record above; the L0 decides.

### 5.2 C1 K2(b) — no gap found

Empty or declared-vocabulary `reason`/`flip` under `## Rejects`, `## Rejection log`, `## REJECTIONS — round 82`,
`## Rejected and dropped`, `## Rejected sources` → all `rc=1` with `SWEEP_REJECTION_INCOMPLETE` naming the row and
section (receipt `c1-k2b-heading-probe.txt`). Renaming a heading while keeping reason+flip complete still passes
(correct: nothing to refuse). `where` placeholders (`same`, `idem`, `n.a`, `x`, `see above`, `--`) → all
`SWEEP_LOCATION_ABSENT`, rc 1 (receipt `c1-k2-probe.txt`).

### 5.3 C1 K3 — 112-record sweep, no schema-valid record regressed

Same record bytes, same corpus, base gate (`5d792e1e`, swapped into a hardlink copy of the landing tree — only the
gate file differs) vs landed gate, both frozen Run lines, over every `corpus/**/*.md` carrying
`## Sweeps|Rejections|Rejected|Claims`:

```
K3_DELTAS=70 records=112          (116 record/item pairs both gates pass)
```
67 of the 70 deltas are the round-82 `c1-records` fixtures themselves (intended refusals). The three outside that
directory:

| file | item | base | landed | finding | carries a K2 form? |
|---|---|---|---|---|---|
| `corpus/evidence/round81/negA-probe.md` | 4 | 0 | 1 | `SWEEP_NEGATIVE_UNRESOLVED` | **yes** — empty claim-sweep cell, no `## Sweeps` row → K2(a)/(c); not harm |
| `corpus/fixtures/sweeps-r5.README.md` | 2,4 | 0 | 1 | `SWEEP_REJECTION_INCOMPLETE` ×3 | no |

Receipts: `k3-probe.txt`, `k3-readme.txt`, `k3-readme-base.txt`, `k3-header-probe.txt`. A separate pass over the 13
`corpus/**/*.md` that carry `## Negatives` but none of the four headings found no delta (`k3-negatives-sweep.txt`).

The README is a **K3 candidate, not a firing**: it is fixture documentation, not a research record — no
`<!-- chousa-record: v1 -->`, no Meta/Question/Claims sections, and base `verify` mode already calls it
`RECORD_SCHEMA_INVALID`. The mechanism is still worth recording: the new read of "any `##` heading containing reject"
now applies the (pre-existing, exact-column) rejection rule to prose tables, and this README's column is
`reason (from the method)`, so all three rows read `reason=absent`. Header sensitivity itself is unchanged between
gates (`Reason` and `Flip Condition` capitals pass on both; `reason (from the method)`, `reason_text`, `notes` fail on
both — `k3-header-probe.txt`), so the delta is the heading scan, not a header rule change. A real record whose
rejection table qualifies its `reason` column under a non-exact `## Rejections` heading would be refused by the landed
gate and passed by base; that is the residual this candidate names.

### 5.4 C2 K2 — holds on independent re-derivation

Own script (`c2-k2-recheck.py`, not the counter): for S008/S209/S210/S211 — registry row `mined`, `used-by` names the
entry, `key = sha256(url)[:24]`, capture exists, and `txt_sha256` of the *last* matching refetch row equals the
capture's sha256; then every `## Located quotes` row searched (after curly-quote/whitespace folding) in its capture:

```
SOURCE S008 capture 598abc09…2ac433a  sha_matches_last_row=True  fetched_utc=2026-11-06T19:42:03Z
SOURCE S209 capture 8581ca18…5d273ad7 sha_matches_last_row=True  fetched_utc=2026-11-06T19:42:05Z
SOURCE S210 capture fc857da3…cf889875 sha_matches_last_row=True  fetched_utc=2026-11-06T19:42:08Z
SOURCE S211 capture b8b542d9…0e6ca7de sha_matches_last_row=True  fetched_utc=2026-11-06T19:42:10Z
QUOTE Q1..Q11 present_in_capture=True (11/11, 11–23 words each)
C2_K2_INSTRUMENT_CHECKS bad=0
```
Receipt: `c2-k2-recheck.txt`. The four refetch rows post-date the egress-table commit
(`5d792e1e`, 2026-11-06T19:41:56Z), so round-81 routed defect 3's ordering holds on these bytes.

### 5.5 C2 K4 — spot-check, holds

`corpus/evidence/round82/base-knowledge.txt` is the base set. No base entry carries a decision table or list on
choosing/aligning a question frame: three base entries own a `## Decision table` (citation-searching TARCiS,
correction/retraction status, recheck-due) and none is on question framing; the only base mentions are
`quality-control-guideline-issued-text-r48.md` (PICOS optional in one instrument's inclusion rule, 2 lines, no table)
and `archived-export-intake.md` ("question framing before search" as claim CL-02, no decision rows). Receipt:
`c2-k4-basecheck.txt`. (K3 — whether a row's Do/Never follows from its quote — needs a non-author reviewer; not
claimed here.)

### 5.6 Positive controls that must not be harm

`pending` and `no flip` in a flip cell (outside the declared vocabulary) pass the landed gate (`rc=0`) — no
over-refusal. The 6 positive controls still pass at landing (`POSITIVE=6/6`), and 116/112 sweep pairs pass under both
gates.

## 6. Residuals and risks

1. **The K2(a) hole is a predicate-counter gap, not a gate crash**: the counter's class fixtures all break the
   carrying row, so a placeholder cell beside a valid `## Sweeps` row is never scored. If the L0 reads K2(a) as
   written, C1 is falsified; if it reads the gate's `claim_id` cross-reference as the intended contract, then the
   landing `SKILL.md` item-2 prose sentence overstates what the gate does and should be corrected (a documentation
   defect, not a kill).
2. Rejection-table `reason` column matching is exact-name on both gates; a qualified column (`reason (from the
   method)`) is invisible. Pre-existing, but the round-82 heading scan widens its reach to prose tables.
3. Driver portability: `run-controls-r82.sh` cannot be run from a `git archive` tree (its `LANE` is the archived
   tree, not a repo). Reproduction requires a real clone/checkout at the freeze revision — worth a line in the
   driver header.
4. `n.a` / `--` / `null` / empty in a claim's `sweep` cell are accepted whenever a `## Sweeps` row claims the row id;
   every other placeholder location (reason, flip, `where`) is refused.

## 7. Tooling and hygiene

- No installs, no upgrades, no pacman transactions (host-wide pause respected). No network: this seat's item named no
  re-open, so zero HTTP requests were made and no capture or `refetch.tsv` row was written.
- Only reads outside scratch: `git -C <lane> show/archive/ls-tree/log`, `git -C <lane> diff`. No writes to the lane,
  `scripts/`, `.ufo/state`, `MANIFEST.json`, `considerthese/` or any sibling repo; no commits, no `jj`.
- Scratch `/fast/scratch/hyaku/chousa-r82/R82ExecRepro/` (trees at three revisions, clone, probes) removed before
  yield; nothing written under `/tmp`; every cited receipt copied into this folder first.
- Selftest executed **once** (limit two).

## 8. Receipts in this folder

`pins.txt`, `runlines.txt`, `skill-runline-split.txt`, `diff-SKILL-base-landing.txt`,
`before-c1-k2-gate.txt`, `before-c2-depth.txt`, `after-c1-k2-gate.txt`, `after-c2-depth.txt`,
`after-c1-selftest.txt`, `controls-rerun.txt`, `controls-rerun-archived.txt`, `controls-rerun-diff.txt`,
`controls-rerun/` (14 receipts + summary), `c2-k2-recheck.txt`, `c2-k4-basecheck.txt`,
`c1-k2-probe.txt`, `c1-k2-claim-sweepcell.txt`, `c1-k2-deciding-record.txt`, `c1-k2b-heading-probe.txt`,
`k3-probe.txt`, `k3-readme.txt`, `k3-readme-base.txt`, `k3-header-probe.txt`, `k3-negatives-sweep.txt`.

VERDICT: R82ExecRepro C1 fired — K1 predicate (11/11, 9/9, 24/24, 6/6), K4 (selftest 280/0 skipped) and both Run
lines hold, but K2(a) fires: `item2-pass.md` with only the claim-`sweep` cell set to a declared-vocabulary value
(`n.a`, 30/30 values incl. empty) and the `## Sweeps` row `W1|N1` intact exits 0 on the frozen item-2 Run line.
VERDICT: R82ExecRepro C2 held — before DEPTH_R82=FAIL/rc 1 and after entries=1 ok_entries=1 rows=9 located_quotes=11
fresh_sources=4/PASS/rc 0 reproduce exactly, 11/11 quotes are in their captures, 4/4 capture sha256 equal their
refetch rows, and no base entry holds a question-framing decision table.
