# round-82 wave 1 — R82ExecForms

**Seat.** R82ExecForms (leaf executor). **Move.** Fire-or-hold C1 kill rule **K2 (generalization)**: author NEW
records the frozen manifest does not contain, inside the declared class of `claims.md` K2 (a)/(b)/(c), and run the
frozen SKILL.md item-2 / item-4 Run lines on them at the landing revision.

**Tree under test.** `b4a41d251b488f06b4a6ab01a11bc12ce72edd20`, extracted with
`git -C /home/vgpnk/Projects/shokunin/chousa-shokunin archive b4a41d25… | tar -x -C /fast/scratch/hyaku/chousa-r82/R82ExecForms/tree`.
Instrument hashes at that revision (`receipts/instrument.txt`):
`0d8ac50f…` `tools/research-gate.sh`, `43e9b5ed…` `SKILL.md`, `4d6ba055…` `corpus/evidence/round82/k2-gate-r82.py`,
`16ab5682…` `corpus/evidence/round82/c1-manifest.tsv`.

**Baseline, cited not re-run** (my move is K2, not K1/K4): `corpus/evidence/round82/after/c1-after.txt` ends
`RUNLINES=2/2 K2_REFUSED=11/11 HOLD_REFUSED=9/9 CLASS_REFUSED=24/24 POSITIVE=6/6` / `K2_GATE=PASS` / `rc=0`;
`after/c1-selftest-after.txt` reads `RESEARCH_GATE_SELFTEST: PASS (280 cases, 0 skipped)` / `rc=0`. So the
predicate K1/K4 part holds at landing and everything below is a pure generalization probe against it.

## Result

**K2 fires. Three new, unambiguous in-class records make the frozen item-2/item-4 Run lines exit 0 at
`b4a41d25`.** Two independent mechanisms, both already present at base (so they are unfixed residuals, not
regressions): the section loader keys sections by *name* and **keeps only the last body of a repeated
`##` heading** (`load_sections`: `SEC_BODY[$sec]=""` on every re-open, `tools/research-gate.sh:870`).

Totals (`receipts/classification.tsv`, 233 records): in-class **185** (refused 182, **passed 3**), reading-dependent
"ambiguous" **16** (refused 4, passed 12), out-of-class **32** (refused 8, passed 24, of which 6 are positive
controls that must pass). No run exited 2, none timed out, none skipped.

---

## 1. Firing — K2(b), duplicate `## Rejections`

Record `receipts/records/E-two-sections-first-bad.md`. Bytes (record's own lines 26-36, in `receipts/byteview.txt`): two `## Rejections`
sections; the **first** keeps a rejection with an **empty flip cell** (`| R1 | corpus/fixtures/sweeps-r5.md | a
round-5 fixture is test data, … |  |`), the second carries the complete row. Class per `claims.md` K2(b): "keeps a
rejection with an empty … reason or flip under a `##` heading whose text contains `reject`". In-class: **yes**
(empty is a declared-vocabulary value; the heading is literally `## Rejections`). No interpretive work needed —
this form is not a duplicate-section technicality, it is the record keeping an incomplete rejection under a
reject heading.

Command, run from the tree root (item-4 line, byte-identical to SKILL.md):

```
bash tools/research-gate.sh verify-sweeps /fast/scratch/hyaku/chousa-r82/R82ExecForms/tree/corpus/evidence/round82/r82-forms/E-two-sections-first-bad.md --root .
```

Receipt `receipts/runs/E-two-sections-first-bad.out`, **exit 0**, decisive lines:

```
REJECTION id=R1 ref=corpus/fixtures/sweeps-r5.md reason=present flip=present observed=complete verdict=match
VERIFIED_SWEEPS=1/1 REJECTIONS_OK=1/1
RESEARCH_GATE: CLEAN (sweeps=1 verified=1 exempt=0 hit=0 refused=0 invalid=0 rejections=1 rejections-ok=1 findings=0 drift=0)
```

Contrast set proving the mechanism is exact-name shadowing, not "duplicates are ignored": the same record with the
bad section **last** refuses (`E-two-sections-last-bad.out`, rc 1, `SWEEP_REJECTION_INCOMPLETE`,
`REJECTIONS_OK=0/1`); with the second section renamed `## REJECTIONS` (a distinct section key) both bodies are read
and it refuses (`H-two-case-sections-first-bad.out`, rc 1, `REJECTIONS_OK=1/2`).

## 2. Firing — K2(c), duplicate `## Claims`

Records `receipts/records/F-two-claims-empty.md` and `F-two-claims-w9.md`. Bytes (record's own lines 20-42, in `receipts/byteview.txt`):
the **first** `## Claims` carries `| N1 | negative | … | observed-in-dump |  |` (empty sweep) resp. `… | W9 |`
(no such row); the second `## Claims` carries one observation row. The single `## Sweeps` row is
`| W1 |  | corpus/knowledge/*tarcis-r80* | zero matches |` — no row's `claim_id` names N1, and there is no
`## Negatives` row. Class per K2(c): in-class **yes** — the record *carries* a negative claim whose sweep cell
names no declared `## Sweeps` row id.

Command, tree root (item-2 line, byte-identical to SKILL.md):

```
f=/fast/scratch/hyaku/chousa-r82/R82ExecForms/tree/corpus/evidence/round82/r82-forms/F-two-claims-empty.md; ! bash tools/research-gate.sh verify "$f" --root . | grep -q '^FINDING NEGATIVE_WITHOUT_SWEEP' && bash tools/research-gate.sh verify-sweeps "$f" --root .
```

Receipts `receipts/runs/F-two-claims-empty.out` and `F-two-claims-w9.out`, **exit 0** both, decisive lines:

```
SWEEP id=W1 where=corpus/knowledge/*tarcis-r80* looked=local hits=0 at=- observed=verified verdict=match
VERIFIED_SWEEPS=1/1 REJECTIONS_OK=1/1
RESEARCH_GATE: CLEAN (sweeps=1 verified=1 exempt=0 hit=0 refused=0 invalid=0 rejections=1 rejections-ok=1 findings=0 drift=0)
```

Hard proof the first table is dropped wholesale, not merely unread by the sweeps mode: the structure check on the
same file reports one claim and zero negatives (`receipts/structure-verify.txt`:
`RESEARCH_GATE: DRIFT (findings=1 drift=1 … claims=1 negatives=0 …)`).

---

## 3. Reading-dependent in-class passes (reported, not counted as the firing)

These 12 records exit 0 and are in-class **only under a stated reading**. I list them so the L1 can adjudicate; I
do not lean on them, because §1 and §2 already fire K2 without any interpretive choice.

| record | item | rc | class question | receipt |
|---|---|---|---|---|
| `E-heading-h3-under-notes` | 4 | 0 | `claims.md` K2(b) says "a `##` heading"; `### Rejected sources` is level-3. SKILL.md item-4 documents "rows kept under **any heading containing 'reject'** … are read too" — the gate reads none (`REJECTIONS_OK=0/0`). In-class under SKILL.md's own wording; out under a strict `##`-level reading. | `runs/E-heading-h3-under-notes.out` |
| `E-flip-nbsponly`, `E-flip-nbspboth`, `E-reason-nbsponly`, `E-reason-nbspboth` | 4 | 0 | cell is `\xa0` / `\xa0n/a\xa0` / `\xa0none\xa0`. The declared normalization says "**collapsing whitespace**"; U+00A0 is Unicode whitespace (Zs) but not bash `IFS`. In-class under a Unicode-whitespace reading, out-of-class under an ASCII-only reading. | `runs/E-*.out` |
| `D-flip-nbsponly`, `D-flip-nbspboth`, `D-reason-nbsponly`, `D-reason-nbspboth` | 4 | 0 | same cells rebuilt on `item4-pass.md`; same fork. | `runs/D-*.out` |
| `D-where-nbspboth` | 2 | 0 | where cell `\xa0n/a\xa0` is **classified as a local path** and *verified*: `SWEEP id=W1 where=\xa0n/a\xa0 looked=local hits=0 at=- observed=verified verdict=match`. The only where-cell form in the whole matrix that passes with a placeholder in it — because `sweep_looks_path` sees the `/`. | `runs/D-where-nbspboth.out` |
| `F-status-notapp-where-na` | 2 | 0 | where cell `n/a` on a row with `status=not-applicable`: `SWEEP id=W1 where=n/a looked=exempt … observed=exempt`, `VERIFIED_SWEEPS=0/1`, rc 0. In-class under a loose K2(a) reading (a declared `where` value); out under the strict one-cell reading (the record also adds a status column). | `runs/F-status-notapp-where-na.out` |
| `G-two-sweeps-first-bad` | 2 | 0 | where cell `n/a` in a first, shadowed `## Sweeps` section; the kept section verifies clean. Same loose/strict fork as above. | `runs/G-two-sweeps-first-bad.out` |

## 4. Held — 182 in-class refusals

All 26 declared vocabulary values were planted in **each** of the four cells: reason 26, flip 26, `where` 26,
claim-`sweep` 26 (`A-*`, `B-*`, `C-*`) — **104/104 refused**. Decoration variants, declared by the claim's own
normalization — `N/A`, `n/a.`, `` `n/a` ``, `"n/a"`, `'n/a'`, `**n/a**`, `_n/a_`, `  n/a  `, `n/a\t`, `\tn/a`,
`—`, `–`, `…`, `...`, `` `N/A`. `` — planted in all four cells: **60/60 refused**. Also held:
`## Rejected`, `## REJECTIONS`, `## Kept rejections (2)`, `## Rejection log`, a rejection table inside a fenced
block, `### Rejected sources` nested in `## Rejections`, `W1` vs declared `w1`, kinds `Negative` and
`negative `, a tab-only flip cell, and all six sweeps-r5-based mutations (`H-s5-*`, `REJECTIONS_OK=2/3`,
`VERIFIED_SWEEPS=0/2`).

Notable *correct* permissiveness (out-of-class passes, not residuals): `W1,`, `W1;W9`, `` `W1` ``, `  W1  ` all
resolve to declared row `W1` (rc 0) — decorated references still name their row, which is what K2(c) asks for.

## 5. Residuals — out-of-class passes (24, controls included)

Reported separately, per `claims.md` ("values outside this set … are recorded as a residual, not a kill"):

- **Unicode look-alikes outside the closed set**: `‒` U+2012, `―` U+2015, `n／a` U+FF0F in reason and flip pass
  (`D-reason-figdash`, `D-reason-hbar`, `D-reason-fullslash`, `D-flip-*`, `E-flip-*`, rc 0). Also `n\xa0/a` in
  reason, flip and `where` (`D-*-nbspmid`, rc 0; the `where` form is *verified* as a local path).
- **`kind` cell not normalized**: `kind = negative.` passes the item-2 line (rc 0) though the structure check
  flags it (`FINDING OBS_INFERENCE_COLLAPSE … obs=claim=N1 kind=negative. invalid`). Residual because K2(c) says
  "carries a `negative` claim"; also a Run-line-strength observation: the item-2 line greps one finding id only,
  so an otherwise-drifting record still exits 0.
- **Prose / bulleted rejections**: a rejection kept as a bullet or as prose under `## Rejections` is invisible to
  item-4 (`I-bullet-rejection`, `I-prose-rejection`, rc 0, `REJECTIONS_OK=0/0`); K2(b) is about row cells, so out
  of class.
- **Exempt sweeps still certify a negative claim**: `F-status-notapp` (rc 0, `VERIFIED_SWEEPS=0/1`,
  `RESEARCH_GATE: CLEAN`) — the negative claim's sweep row exists but is never run, and the earlier round-81 hole
  (`VERIFIED_SWEEPS=0/0` was CLEAN) now also covers `0/N`. Out of class because a row's `claim_id` names the claim,
  but it is the strongest semantic hole in the set and the one I would attack next.
- Controls (must pass, passed): `E-control-complete`, `E-control-other-heading-complete`, `F-control-baseline`,
  `F-control-claimid-binds`.

## 6. K3 context (measured; not this seat's assigned rule)

Base `5d792e1e` passes **every** probe I ran (`receipts/base-gate.txt`, rc 0 on all 12), including the three
firing records — so **no K2 firing here is a regression**; the placeholder/generalization work simply never reached
the section loader, the NBSP splitter, or the exempt-sweep path. Two refusals that base passed are lenient-reading
K3 candidates, not K2: `F-sweepcell-bracket` (`[W1]` — byte-unequal to the id, but plainly a reference to W1;
landed rc 1 `SWEEP_NEGATIVE_UNRESOLVED`) and `F-sweepid-case` (`W1` against declared `w1`; landed rc 1). Under a
*naming* reading of K2(c) these carry none of K2's forms, so they would be harm; under a *token* reading they are
in-class and the refusal is correct. I record both, and neither is needed for the verdict.

## 7. Limits

- I did not re-run `k2-gate-r82.py` or `--selftest` (K1/K4 are not my rule; the committed after-receipts are cited).
- Two frozen instrument behaviours were taken as given, not re-derived: the gate's `load_sections` name-keyed
  section map and `sweep_is_placeholder`'s bash-`IFS` splitter (read at `tools/research-gate.sh:800-877`,
  `2695-2712`). Both are quoted by line number in `receipts/` and reproduced by the runs.
- The "ambiguous" rows are the honest cost of `claims.md`'s wording; I have not promoted any of them into the
  firing count.
- Scratch `/fast/scratch/hyaku/chousa-r82/R82ExecForms` (tree, base tree, generators, runs) is deleted after the
  receipts are copied; no receipt or evidence path ever lived under `/tmp` (one transient sha256 comparison
  buffer was written there and deleted in the same call, and is not cited), and no git/jj mutation occurred in any
  lane or fixture.

## Files written

- `chousa-shokunin/.ufo/waves/round-82/w1/R82ExecForms/records/` — 233 authored records (+ `records-sha256.txt`).
- `…/R82ExecForms/receipts/runs/` — 233 per-record outputs (command, rc, full gate output).
- `…/R82ExecForms/receipts/` — `classification.tsv` (record, item, class, why, rc, findings, counts),
  `results*.tsv`, `base-gate.txt`, `instrument.txt`, `byteview.txt`, `structure-verify.txt`, `harness.txt`.
- This report. No production file, manifest, counter, fixture, receipt or corpus path was modified.

VERDICT: R82ExecForms C1 fired — K2 fires at b4a41d25: two new in-class records (`E-two-sections-first-bad` item 4; `F-two-claims-empty`/`F-two-claims-w9` item 2) exit 0 because `load_sections` keeps only the last body of a repeated `##` heading, so a kept rejection with an empty flip and a negative claim with an empty/undeclared sweep cell are both certified CLEAN (receipts `runs/*.out`, rc 0, `RESEARCH_GATE: CLEAN`).
VERDICT: R82ExecForms C2 n/a — not touched by this seat.
