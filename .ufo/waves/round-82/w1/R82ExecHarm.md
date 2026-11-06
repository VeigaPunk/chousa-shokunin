# R82ExecHarm — C1 kill rule K3 (harm): fire-or-hold

Seat: leaf executor, round-82 wave w1. Question: does the landed gate refuse records the base gate passes,
where those records carry none of C1's K2 forms?

**Answer: K3 does not fire on the record-shaped set. 0 of 66 base-pass → landed-refuse transitions lacks a K2 form,
both surfaces, both trees; no relaxation, no usage error, no selftest case changed.** Two residuals are named
below, one of which (F1) is a 21-document class that fires K3 *only* if "record" is read as any tracked `.md`
rather than as a gate record; the reading and the bytes are given so L1 can settle it.

## Trees and bytes

| tree | revision | `tools/research-gate.sh` sha256 |
|---|---|---|
| base | `38f5af8268b2807811dded3d7d7221ff3f509495` | `d5d48128509f77edf161e4d8b10b833e6e00f822906460fa049f27d1244d41e2` |
| landed | `b4a41d251b488f06b4a6ab01a11bc12ce72edd20` | `0d8ac50f2695b8df9300905dd44ea70668dd047912633226f8bababe7570d92a` |

`for r in 142b6f0c… 5d792e1e… 38f5af82… b4a41d25…; do git cat-file -p "$r:tools/research-gate.sh" | sha256sum; done`
→ the base gate is byte-identical at `142b6f0c`, `5d792e1e` (the revision K3 names) and `38f5af82`; only `b4a41d25`
differs (`diff -u` = 180 changed lines, i.e. the three declared additions only: `sweep_is_placeholder`, the
"any heading containing reject" loop, the negative-claim resolution block, plus 5 selftest cases).

Third tree built for isolation: `baseL` = the base tree (byte-copy) with `tools/research-gate.sh` replaced by the
landed gate, so both gates read identical bytes (records were not edited between the two revisions: of the 23 paths
`git diff --name-only 38f5af82 b4a41d25` changed, none is in the record set).

## Method

```
D=…/R82ExecHarm; git -C <lane> archive 38f5af82… | tar -x -C "$D/base"   # same for b4a41d25 → "$D/landed"
# file set: the seat-specified greps at b4a41d25 plus every corpus/fixtures/**.md and the named families
git -C <lane> grep -l -E '^## (Rejections|Sweeps|Negatives|Rejected)' b4a41d25 -- corpus .ufo        # 506
git -C <lane> grep -l -E '^\|[^|]*\|[[:space:]]*negative[[:space:]]*\|' b4a41d25 -- corpus .ufo      # 426
+ corpus/fixtures/**.md (84) + full-r6*/integrity-r7*/sweeps-r5*/chain-r3*/archives-r9/  → union 571 files
# per file, from each tree root, fresh process, CHOUSA_* scrubbed:
( cd base   && bash tools/research-gate.sh verify-sweeps "$f" --root . ) ; rc
( cd base   && bash tools/research-gate.sh verify        "$f" --root . ) ; rc
( cd baseL  && … same two surfaces … )        # landed gate on base bytes
( cd base   && bash tools/research-gate.sh verify-all    "$f" --root . )  and the baseL twin
```
571 files × 3 surfaces × 2 gates = 3426 invocations, all rcs captured in `table.tsv`.
A second, wider set (258 files whose `##` heading merely *contains* reject/sweeps/negative, enumerated with
`^##+ .*([Rr]eject|[Ss]weeps|[Nn]egative)`, 767 hits minus the 571) was run the same way (`table-wide.tsv`).

## Result 1 — exit-code matrix, 571 record-shaped files

| surface | 0→0 | 0→1 | 1→1 | relaxations (n→0) | usage errors (→2) |
|---|---|---|---|---|---|
| `verify-sweeps` | 142 | **66** | 363 | 0 | 0 |
| `verify` | 7 | 0 | 564 | 0 | 0 |
| `verify-all` | 0 | 0 | 571 | 0 | 0 |

Receipt: `.ufo/waves/round-82/w1/R82ExecHarm/table.tsv` (columns `file base_sweeps landed_sweeps base_verify
landed_verify transition k2_forms`); every transition has its two raw outputs under `transitions/`
(`<basename>.<sha16>.base.txt` / `.landed.txt`).

`verify` and `verify-all` contribute **no** transition of any kind. The item-2 Run line's rc tail is
`bash tools/research-gate.sh verify-sweeps "$f" --root .` (the `verify | grep -q '^FINDING NEGATIVE_WITHOUT_SWEEP'`
prefix only gates it), so `verify-sweeps` is the whole harm surface and the table above covers both Run lines.

## Result 2 — every one of the 66 transitions carries a K2 form

Classified from the landed output of the same bytes (the classes agree with the independent static read of the
base bytes recorded in `table.tsv:k2_forms`):

| files | landed finding | K2 form |
|---|---|---|
| 30 | `SWEEP_REJECTION_INCOMPLETE` under `## Rejections` (no `section=` obs), every one with a `placeholder=` field — `reason:present,flip:placeholder` (24 findings) / `reason:placeholder,flip:present` (6) | K2(b) |
| 21 | `SWEEP_NEGATIVE_UNRESOLVED`, cells `W1`(7) `-`(6) `n/a`(2) `W9`(2) `SW1`(1) `—`(1) `N/A`(1) `TBD`(1) | K2(c) |
| 9 | `SWEEP_LOCATION_ABSENT … unclassifiable location naming`, `where` = `n/a` / `N/A` / `n/a.` | K2(a) |
| 3 | `SWEEP_REJECTION_INCOMPLETE … section=Rejected sources / Rejected / Kept rejections` (flip column absent) | K2(b), empty flip |
| 3 | `SWEEP_REJECTION_INCOMPLETE … section=Rejections — provenance and flip-conditions` (`sweeps-r5.README.md` ×3) — finding F2 | K2(b) by the column rule only |

Every `W1`/`W9`/`SW1` unresolved row was checked by hand: e.g. `corpus/evidence/round82/c1-records/r2-01-undeclared-sweepid.md`
has **no `## Sweeps` section at all** (`grep -n '^## '` → Meta, Question, Sources, Claims, Rejections, Approval) while
the N1 claim's sweep cell reads `W1`; `r2-02-sweeps-header-only.md` has a `## Sweeps` header with zero rows. Both are
exactly K2(c). No transition fired because the cell named a declared id the code failed to match.

Sample, one line per tree, `bash tools/research-gate.sh verify-sweeps corpus/evidence/round82/c1-records/r2-01-undeclared-sweepid.md --root .`:
- base → `RESEARCH_GATE: CLEAN (… rejections=1 rejections-ok=1 findings=0 drift=0)`, **rc 0**
- landed → `FINDING SWEEP_NEGATIVE_UNRESOLVED … obs=claim=N1 sweep=W1 names no sweep row this mode re-ran` … `RESEARCH_GATE: DRIFT (… findings=1 drift=1)`, **rc 1**

Positive controls (a blanket refusal would score FAIL) are unchanged, base 0 → landed 0:
`corpus/evidence/round82/c1-records/item2-pass.md`, `…/item4-pass.md`, `…/r4-07-alt-section.md` (the r81 seat-record
whose description did not match its bytes), `corpus/fixtures/sweeps-r5.md`, `corpus/fixtures/full-r6.md`,
`corpus/fixtures/archives-r9/A-r9.md`.

Also unchanged: no relaxation anywhere — not one file that base refused is now accepted, on any of the three surfaces.

## Result 3 — `--selftest` case list, one run per tree

```
cd base   && TMPDIR=… HYAKU_SCRATCH=… bash tools/research-gate.sh --selftest   # rc 0
cd landed && TMPDIR=… HYAKU_SCRATCH=… bash tools/research-gate.sh --selftest   # rc 0
```
- base: `RESEARCH_GATE_SELFTEST: PASS (275 cases, 0 skipped)`, rc 0 → `selftest-base.txt`
- landed: `RESEARCH_GATE_SELFTEST: PASS (280 cases, 0 skipped)`, rc 0 → `selftest-landed.txt`
- case-list diff (`selftest-case-diff.txt`): **0 base cases missing, 0 base cases with a changed verdict or detail,
  0 non-`ok-case` in either tree**, 5 added: `sweeps-fail-placeholder-cells`, `sweeps-fail-rejected-heading`,
  `sweeps-fail-where-placeholder`, `sweeps-fail-negative-unresolved`, `sweeps-pass-prose-with-placeholder-word`.
  Case numbers shift by 5 after insertion point (base case 55 `all-pass.md` is landed case 60 with the same details).

## Finding F1 — the "any heading containing `reject`" reach refuses 21 non-record lane documents

Enumeration: `git grep -l -E '^##+ .*([Rr]eject|[Ss]weeps|[Nn]egative)' b4a41d25 -- corpus .ufo` → 767 hits, 259 of
them outside the record set; 258 have bytes at the base revision (the 259th, `corpus/evidence/round82/claims.md`,
was added at the freeze commit, so no base run exists for it). On those 258: base 0→0 235, **0→1 21**, 1→1 2,
relaxations 0 (`table-wide.tsv`, raw outputs `wide-transitions/`).

Every one of the 21 has **no `# research-record v1` header** (checked mechanically over the first 400 bytes of each)
and no `## Rejections` / `## Sweeps` / `## Negatives` section; the heading that triggers the new code is a prose
heading that contains the word *reject*. Examples, exact lines:

| file | base | landed |
|---|---|---|
| `corpus/lessons/round-24-verifier-spotcheck.md` (§`Spot-check (LEARNING.md — at least one admit and one reject)`, table `decision\|sample\|verifier\|result`) | `RESEARCH_GATE: CLEAN (… rejections=0 findings=0 drift=0)` rc 0 | `REJECTIONS_OK=0/2 … RESEARCH_GATE: DRIFT (… rejections=2 findings=2 drift=2)` rc 1, `FINDING SWEEP_REJECTION_INCOMPLETE … obs=id=R1 missing=reason,flip section=Spot-check (LEARNING.md — at least one admit and one reject)` |
| `corpus/evidence/README.md` (§`Round-5 rejection/sweep receipts — stamp …`, table `Receipt (sha256)\|Shows\|Key result`) | CLEAN, rc 0 | `REJECTIONS_OK=0/12 … DRIFT`, 12 findings, rc 1 |
| `corpus/lessons/round-41-verifier-spotcheck.md` (§`Discernment spot-check (LEARNING.md — non-author, ≥1 admit + ≥1 reject …)`, table `item\|decision\|re-opened source\|agree/disagree\|reason`) | CLEAN, rc 0 | `REJECTIONS_OK=0/5 … DRIFT`, rc 1 (reason present, no flip column) |

Command: `( cd base{,L} && bash tools/research-gate.sh verify-sweeps corpus/lessons/round-24-verifier-spotcheck.md --root . )`.
The other members of the class are `corpus/lessons/round-{41,49,65,71,80,81}-verifier-spotcheck.md`,
`corpus/evidence/README.md`, `.ufo/waves/round-65/w1/Attack12.md` + `…/report.md`,
`.ufo/waves/round-73/w1/R73S01/frozen-SCORECARD.md`, `.ufo/waves/round-74/w1/R74ExecC/inputs/SCORECARD.md`,
`.ufo/waves/round-80/w1/R80ConnectorA/kama--corpus__QUALITY.md.blob`, and the two assimilation-tree copies of the
README and of the r24/r41 lessons (`wide-transitions/`, listed in `transition-classes.txt` is the narrow list only —
the 21 are in `table-wide.tsv` with `transition=sweeps`).

**Reading.** K3 asks for "a record that the base gate passes … which the landed gate refuses … [carrying] none of
K2's forms". Two readings:
- *Record = a file a Run line is meant for* (files carrying the record header/sections — the 571 set, and the set the
  C1 counter's manifest draws from): these 21 are out of domain, and **K3 is held**.
- *Record = any tracked `.md` a lane sweep would hand the gate*: then these 21 carry no K2 form at all — their tables
  are spot-check ledgers and a receipts index, not kept rejections — and **K3 fires on 21 documents**.

I do not get to settle that; the bytes and both counts are above. What is not arguable: a directory-wide
`verify-sweeps` over the lane corpus now DRIFTs on 21 clean, non-record documents, and the frozen K2(b) wording
("under a `##` heading whose text contains `reject`") is what asks for it. If L1 scores this as harm, the defect is
in the rule's heading reach, not in a mistaken line of the landed gate.

## Finding F2 — `sweeps-r5.README.md`: complete reason invisible under a parenthetical column name

`corpus/fixtures/sweeps-r5.README.md` (and its two assimilation-tree copies) keeps three real rejections whose reason
sits in a column named `reason (from the method)`; the landed gate reads `reason=absent` and drifts
(`FINDING SWEEP_REJECTION_INCOMPLETE … missing=reason section=Rejections — provenance and flip-conditions`, rc 1)
while base passed it vacuously (`## Rejections — provenance and flip-conditions` is not the section `Rejections`).

Two controls isolate the cause, both run from the base tree:
- heading renamed to `## Rejections` only → **rc 1**, same three `missing=reason` findings — the pre-existing column
  matcher, not the new code (`controls/ctl-base-canonical-heading.txt`);
- heading **and** column renamed to `reason` → **rc 0**, `VERIFIED_SWEEPS=0/0 REJECTIONS_OK=3/3`,
  `RESEARCH_GATE: CLEAN` (`controls/ctl-base-canonical-heading-and-column.txt`).

So the transition is the heading widening meeting a base-gate column-matching limit. Under K2(b) the reason cell (as
the gate reads cells) *is* empty, so this does not fire K3; it is a residual: heading-widening can turn a complete
rejection into `incomplete` whenever the reason column carries a parenthetical.

## Risks

- **F1 is the live one.** It is a scope decision, not a byte defect. Any future `verify-sweeps`-over-a-directory
  habit, or any lane document with `reject` in a `##` heading, now yields DRIFT.
- F2's class (parenthetical/renamed reason columns) is under-refused-at-base and over-refused-at-landing; a real
  record written that way drifts.
- The K2 form classifier in `table.tsv:k2_forms` is my static read of the base bytes, independent of the gate; it
  agreed with the landed findings on all 66. It is a reading, not the frozen counter, and is not a receipt the
  parent should cite in place of the gate outputs.
- Timing: the base selftest ran 168 s, the landed one 152 s on an idle box; both within the two-run budget (2 runs
  used, 0 more).

## Blockers

None. No tool installs were needed (nothing installed; no pacman transaction attempted). No network used.

## Files I wrote (all under my output folder; no production edit)

```
.ufo/waves/round-82/w1/R82ExecHarm/table.tsv                 571-file × 3-surface × 2-gate matrix
.ufo/waves/round-82/w1/R82ExecHarm/table-wide.tsv            258-file wide set matrix
.ufo/waves/round-82/w1/R82ExecHarm/transitions/              66 × (base, landed) raw gate outputs
.ufo/waves/round-82/w1/R82ExecHarm/wide-transitions/         21 × (base, landed) raw gate outputs
.ufo/waves/round-82/w1/R82ExecHarm/transition-classes.txt    narrow transitions grouped by finding
.ufo/waves/round-82/w1/R82ExecHarm/selftest-base.txt         PASS (275 cases, 0 skipped), rc 0
.ufo/waves/round-82/w1/R82ExecHarm/selftest-landed.txt       PASS (280 cases, 0 skipped), rc 0
.ufo/waves/round-82/w1/R82ExecHarm/selftest-case-diff.txt    per-case identity diff
.ufo/waves/round-82/w1/R82ExecHarm/controls/ctl-base-canonical-heading.txt              F2 control, rc 1
.ufo/waves/round-82/w1/R82ExecHarm/controls/ctl-base-canonical-heading-and-column.txt   F2 control, rc 0
.ufo/waves/round-82/w1/R82ExecHarm/summary.txt               raw numbers
.ufo/waves/round-82/w1/R82ExecHarm/record-file-list.txt      the 571 paths
.ufo/waves/round-82/w1/R82ExecHarm/wide-file-list.txt        the 258 paths
```

VERDICT: R82ExecHarm C1 held — of 66 base-pass→landed-refuse transitions across 571 record-shaped files and three surfaces (`verify-sweeps` 66, `verify` 0, `verify-all` 0; no relaxation, no new usage error), every one carries a K2(a)/(b)/(c) form, and the selftest keeps all 275 base cases `ok-case` with unchanged detail; K3 fires only on the 21 non-record lane documents in F1 if "record" is read as any tracked `.md`.

VERDICT: R82ExecHarm C2 n/a — not attacked by this seat; C2 is the depth claim, and no C2 bytes were touched.
