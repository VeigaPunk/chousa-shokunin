# Round 81 — critic (claims) — R81CriticClaims

Leaf critic seat. Lane root `/home/vgpnk/Projects/shokunin/chousa-shokunin`.
Attacked bytes: landing `7e2da96a0541946e796384d42fea18e09ede9e9f`; claim freeze
`bb54e7f89da9ba4213aec9d976c13f3f4ba548fb`; prefreeze controls
`f7929f877e6fd54f4dc5ce7f993da46bc7df43f9`; base `378fda82dc2cbcc555a0565052cc408121813cef`.
Scratch: `/fast/scratch/hyaku/chousa-r81/R81CriticClaims` (deleted before yield). Every tree was made
with `git -C <lane> archive <rev> | tar -x -C <scratch dir>`; every counter run used the frozen script
from the landing revision; no network (my item names no re-open); no tool installs; no production edits.
Receipts cited below are copied to `.ufo/waves/round-81/w1/R81CriticClaims/receipts/`; counterexample
records and the two cheapest trees are in `.ufo/waves/round-81/w1/R81CriticClaims/artifacts/`.

I never amended a claim, counter, fixture or receipt. I measure, attack, report.

## 0. The two predicates reproduce at the landing revision

| claim | command (cwd = extracted landing tree) | observed | rc | receipt |
|---|---|---|---:|---|
| C1 | `python3 -B corpus/evidence/round81/depth-r81.py --root <landing>` | `DEPTH_R81 entries=2 fresh_rows=5 located_quotes=14` / `DEPTH_R81=PASS` | 0 | `receipts/r01-depth-landing.txt` |
| C1 | same counter, `--root <base>` | `DEPTH_R81 entries=0 fresh_rows=0 located_quotes=0` / `DEPTH_R81=FAIL` | 1 | `receipts/r02-depth-base.txt` |
| C2 | `python3 -B corpus/evidence/round81/checklist-run.py --root <landing>` | `CHECKLIST_RUN=6/6 DISCRIMINATE=3/3` / `CHECKLIST=PASS` | 0 | `receipts/r03-checklist-landing.txt` |
| C2 | same counter, `--root <base>` | `CHECKLIST_RUN=3/6 DISCRIMINATE=0/3` / `CHECKLIST=FAIL` | 1 | `receipts/r04-checklist-base.txt` |

Both declared before→after moves are real on the counters. The attacks below are about what the
counters mean, and two of them find a kill-rule firing.

## 1. Attack 1 — does C1 name the right axis (depth), or is it coverage/quality?

**What the claim says** (`claims.md:22-27`): "Surface moved: `corpus/knowledge/` … Topics: citation
searching per the TARCiS statement (S203, S204), and correction/retraction status …". Predicate: two
`*-r81.md` entries, each citing ≥2 fresh rows, ≥3 located quotes from ≥2 distinct rows, a Markdown
table with ≥3 body rows, disjoint.

**The axis naming is defensible by the lane's own convention.** Every historical depth row in
`SCORECARD.md` is a knowledge entry carrying semantics/limits (`SCORECARD.md:107,151,189,227,263,299,
339,376,414,452,574`), and the changed surface here is exactly that entry set (91 `.md` entries at base
→ 93 at landing). On a read of the landed bytes the entries are genuinely substantive, not filler:
9 and 5 located quote lines, quote lengths 8–25 words, decision tables whose Warrant cells name
recommendations 2/6/7/8/9/10 and S205–S207 (extracted table rows in `receipts/r26-c1-decision-tables.txt`).

**But the predicate is not a depth measure.** The cheapest 10-line entry that satisfies P1–P4 — three
one-word quotes (`the`, `of`, `a`) and a 3×2 dummy table — passes:

```
# cmd: cd <landing> && python3 -B corpus/evidence/round81/depth-r81.py --root <c1min>
ENTRY citation-searching-tarcis-r81.md counted=yes reason=all-pass
ENTRY correction-retraction-status-r81.md counted=yes reason=all-pass
DEPTH_R81 entries=2 fresh_rows=4 located_quotes=6
DEPTH_R81=PASS
rc=0
```
(`receipts/r09-c1-filler-entries.txt`; the two entries are
`artifacts/c1min/citation-searching-tarcis-r81.md` and
`artifacts/c1min/correction-retraction-status-r81.md`.)

The counter cannot distinguish a TARCiS recommendation from a dummy cell. It is a necessary-condition
floor (grounded quotes, a table, disjointness), not the claim's after-state. Two consequences:

1. **§9's same-sentence rule is broken.** The dispatch (§9) requires "one predicate that is the same
   sentence in the plan, the same condition in the counter's code and the same label in the receipt".
   The label is **depth**; the code counts **grounded form**.
2. **The claim's "ground the lane does not hold" is a coverage property, and nothing measures it.**
   The counter never compares the new entries against the base set; two entries on ground the lane
   already holds would pass the same way, provided the registry's `used-by` names them.

Both sides: the axis is not misnamed (knowledge entry = depth in this lane), and the landed entries
are real depth work; the **measurement** is insufficient. That is a fixable defect, not proof the
entries are shallow.

## 2. Attack 2 — the cheapest tree that skips the claimed work reaches both predicates

**C1.** Two filler entries (above) reach `DEPTH_R81=PASS`. The claimed work — two research-method
entries with a decision table a reader can act on — is entirely optional under the counter.

**C2.** A base tree plus three fixture-keyed `Run:` lines reaches the whole C2 predicate:

```
# inserted into the base SKILL.md at items 2, 4, 5:
- Run: `grep -q 'item 2 pass' <record.md>`
- Run: `grep -q 'item 4 pass' <record.md>`
- Run: `printf 'QUOTE_REOPEN_SUMMARY no_source=1\n' <items.tsv>; false`
```
```
# cmd: cd <landing> && python3 -B corpus/evidence/round81/checklist-run.py --root <c2min>
CHECKLIST_RUN=6/6 DISCRIMINATE=3/3
CHECKLIST=PASS
rc=0
```
(`receipts/r10-c2-fixture-keyed-runlines.txt`; `artifacts/c2min/SKILL.md`.) The two `grep` lines
discriminate only because the frozen fixtures' Meta notes literally contain `item 2 pass` / `item 4
pass`; the item-5 line prints the summary and exits 1 without opening anything. Neither implements the
item's semantics.

**Why this matters beyond "the counter is weak".** Dispatch §9: "A target must be one a do-nothing
control cannot reach … Before freezing, build the cheapest control that skips the claimed work, score
it with the frozen counter … if it meets the target, the counter or target is wrong — fix it before
data." The committed controls are literal no-work controls (C1: empty tree
`controls/c1-k0-donothing.txt`; C2: base tree `controls/c2-k0-donothing.txt`, `controls/c2-g1` `true`,
`g2` `|| true`, `g3` no placeholder). They do not include the cheapest **work-skipping** forger that
passes. This is the same class as the two root failures the fresh-start read named: r78 "the battery's
answer key was reachable by a normalizer that scores nothing" and r80 C2 "a one-word hollow record
reaching PASS" (`corpus/lessons/round-80-verifier-spotcheck.md` §2). The round repeated the class it
was told to leave.

## 3. Attack 3 — C2: is the wiring real? (and the K2 firing)

**Case for real operability.** Base 3/6 → landing 6/6; 0/3 → 3/3 (`r03`/`r04`). AXES operability is
exactly "A checklist item can be run and produces the stated outcome" (`AXES.md:13`), and the three
new lines delegate to pre-existing gate modes — no new tool code was required (`tools/` diff empty;
`receipts/r22-tools-unchanged.txt`). The item-2 line does catch the two frozen defects (empty sweep;
sweep row with no location): `rc=1` on `item2-fail.md` and on `negA-probe.md`, `rc=0` on
`item2-pass.md` (`receipts/r16-item2-discrimination-baseline.txt`). Item 4 catches the empty flip cell:
`rc=1`, `FINDING SWEEP_REJECTION_INCOMPLETE` (`receipts/r17-item4-discrimination-baseline.txt`).

**Case against, and the kill: K2 fires on both items.**

Item 2 text: "A negative claim carries its search sweep, naming where it looked."

- Well-formed record, negative `N1` with `sweep W1`, Sweeps table carrying only `W2` (diff in the
  receipt): the landed Run line exits **0** and prints `RESEARCH_GATE: CLEAN`, `VERIFIED_SWEEPS=1/1`
  over the unrelated `W2`. Nothing in the record names where `N1` looked.
  `receipts/r11-k2-item2-dangling-sweep-id.txt`, observed line `RESEARCH_GATE: CLEAN … rc=0`.
- Same with the Sweeps section removed entirely: `rc=0`
  (`receipts/r12-k2-item2-no-sweeps-section.txt`).

Item 4 text: "A rejected source is kept with its rejection reason and flip-condition."

- `## Rejections` row whose `flip_condition` cell is `-`: landed Run line exits **0**,
  `REJECTION id=R1 … flip=present … REJECTIONS_OK=1/1`
  (`receipts/r13-k2-item4-dash-flip.txt`).
- Same with `none` (also `rc=0`, `receipts/r14-k2-item4-none-flip.txt`).
- A kept rejection recorded as a bullet with no flip condition: `rc=0`, `REJECTIONS_OK=0/0`
  (`receipts/r15-k2-item4-bullet-rejection.txt`).
- The item's actual surface is the registry, not a research record. The landed line run against
  `corpus/SOURCES.md` (which holds this round's rejected row S208) prints
  `REJECTIONS_OK=0/0` / `RESEARCH_GATE: CLEAN`, `rc=0`; a minimal registry with a `rejected` row and
  no flip condition also exits 0 (`receipts/r24-item4-registry-surface-unguarded.txt`). SKILL.md's own
  Run-line text concedes it: "It reads research records only: a rejected `corpus/SOURCES.md` row is
  not checked by it".

So the landed Run lines do **not** produce the stated outcome on records carrying the named defect.
This is C2 kill rule K2, fired twice, independently. The item-4 surface mismatch also means the
operability gain for that item is nominal even before K2: the item's subject is unguarded.

The counter cannot see any of this because its fixtures are exactly the two forms the tools do catch
(empty cell / empty location) plus an unregistered id; the *dangling reference* and *placeholder value*
forms are not frozen fixtures, and a fixture-keyed thesaurus passes the whole set (§2).

## 4. Attack 4 — causal separability — held

Built and scored two mixed trees:

| tree | construction | C1 | C2 | receipts |
|---|---|---|---|---|
| `m1-c1only` | landing tree with `SKILL.md` from base | `DEPTH_R81=PASS` rc0 | `CHECKLIST=FAIL` rc1 | `r05`, `r06` |
| `m2-c2only` | landing tree with `corpus/knowledge/` from base | `DEPTH_R81=FAIL` rc1 | `CHECKLIST=PASS` rc0 | `r07`, `r08` |

Each claim is verifiable with the other's surface at base. Held. No cross-claim interaction was found;
neither claim's bytes touch the other's counter inputs.

## 5. Attack 5 — egress-ordering disclosure — protocol defect

`SKILL.md` Boundaries: "A window without an approval table is loopback-only. The approval table is
itself a chousa deliverable." (`receipts/r20-egress-ordering.txt`.)

Facts:
- The six GETs ran `2026-11-06T18:44:29Z`–`18:44:31Z` (`refetch.tsv` lines 146–151).
- The egress table landed in `f7929f87`, committer date `2026-11-06 15:47:58 -0300` =
  `18:47:58Z` — **3m27s after the last GET**.
- The table itself says: "the six fetches below ran at … before this file was written. The table
  states the terms they ran under; it was not on disk first."

Under the rule as written, the window was loopback-only when the six GETs ran. The disclosure is
honest and is itself a deliverable, but it is not authorization; a post-hoc table does not make the
window approved. The table's cited authority (dispatch §2b) is also misdirected: §2b requires
`SOURCES.md` rows **after** a source is opened; it does not grant an external-fetch window. The only
operative rule on the window is the SKILL.md boundary, and it was violated at fetch time.

**Judgment:** a protocol defect that should block admission of C1's counted evidence under the rule
as written. C1's entire sourced leg (S203–S207) is the bytes fetched in that window; the predicate
trusts those captures by design (`depth-r81.py` docstring: "bytes … are trusted as committed"). The
smallest safe correction is an L0/operator ruling that either regularizes the window (accepts the
table's terms retroactively) or excludes the five captures from counted evidence; without it, C1's
evidence was obtained in a window the lane's own rule declared loopback-only.

Secondary: the table says the ordering is "recorded as a `## Mistakes` row in
`corpus/lessons/round-81.md`"; that file does not exist at the landing revision
(`receipts/r23-round81-lesson-absent.txt`). If the closure writes it, the pointer is prospective; if
not, the disclosure is not recorded where it says it is.

## 6. Attack 6 — did the L1 change a frozen rule after scoring? — held

`receipts/r19-frozen-instruments.txt`:

```
depth-r81.py      f7929f87 10c989c0…2fdaa1e9   ==  7e2da96a 10c989c0…2fdaa1e9
checklist-run.py  f7929f87 66ca8c97…f295bbc2   ==  7e2da96a 66ca8c97…f295bbc2
run-controls.sh   f7929f87 c1942bb9…27ea65c    ==  7e2da96a c1942bb9…27ea65c
git diff --name-status bb54e7f8 7e2da96a -- corpus/evidence/round81/
A  corpus/evidence/round81/negA-probe.md
```

The five fixture hashes match the truncated pins in `claims.md` (full hashes in
`receipts/r27-fixture-pins.txt`). `claims.md` is unchanged after its own commit. Only `negA-probe.md`
was added under `corpus/evidence/round81/` at the landing commit — a probe record, not a rule. Held:
no frozen rule, counter, fixture or claim sentence changed after the freeze.

Minor calibration defect in that added file: `negA-probe.md` labels itself "item 2 pass" in its Meta
note, but its `N1` negative claim has an empty sweep cell; `research-gate.sh verify` emits
`FINDING NEGATIVE_WITHOUT_SWEEP` and the item-2 Run line exits 1 on it
(`receipts/r18-negA-probe-mislabel.txt`). The probe is a fail-shaped record with a pass label.

## 7. Checks that found no defect (so the closure does not chase them)

- **"92 files at base"** (`claims.md:22`) is `92` under the lane's file-count convention: 91 `.md`
  entries plus `corpus/knowledge/.gitkeep` = 92 files; landing = 94 files (93 `.md` + `.gitkeep`).
  The round-80 closure used the same convention ("knowledge set 92 → 92"). Not a false number
  (`receipts/r21-knowledge-count.txt`).
- **Item 5's fail leg is offline and refuses before any fetch:** `NO_SOURCE`, exit 1
  (`receipts/r25-item5-nosource.txt`). The claim's stated limit (a printing command can pass the leg)
  stands and is demonstrated in `r10`; it is disclosed, not hidden.
- **C1 K2 (live re-open of a counted quote)** was **not run** by this seat: my item names no re-open
  and the campaign allows no other network. It is unrun here, not passed. The capture bytes are
  internally consistent with `refetch.tsv` (the counter's `located()` passed for all 14 quotes,
  `r01`), but that is not a live check.

## 8. Kill-rule ledger

| claim | rule | result | evidence |
|---|---|---|---|
| C1 | K1 counting command at landing = PASS rc0 | pass | `r01` |
| C1 | K2 live re-open of a counted quote ABSENT | not run (no network for this seat) | — |
| C1 | K3 a counted entry's table row contradicts its located quote | no contradiction found on a read of both tables against the 14 located quotes | `r26` |
| C2 | K1 counting command at landing = predicate line rc0 | pass | `r03` |
| C2 | K2 a defect-bearing record where the landed Run command exits 0 | **FIRED** (item 2: dangling sweep id; item 4: `-`/`none`/bullet flip; registry surface) | `r11`–`r15`, `r24` |

## 9. Impacted axes and smallest safe corrections

- **operability (C2) — harmed as declared.** K2 fired. The smallest fix is not a re-scope: make the
  item-4 Run line read the registry's rejected rows (the item's subject) or narrow the item text to
  research records and accept that the registry surface is unguarded; add the dangling-sweep-id and
  placeholder-flip records to the frozen fixtures; add the fixture-keyed junk control (`r10`) to the
  control set. Until then the predicate's `DISCRIMINATE=3/3` is not evidence of operability.
- **depth (C1) — predicate insufficient.** Add the filler-entry control (`r09`) to the frozen control
  set. If a 10-line filler entry prints PASS, the predicate needs a depth condition: each table body
  row cites a quote-line id, each counted entry has ≥2 quotes of ≥8 words, and every quote's S-id
  appears in the row's Warrant. The landed entries pass the stronger form (`r26`), so this is a
  measurement fix, not a demand for new work.
- **calibration.** The control sets omitted the cheapest passing forger (both claims); the egress
  table's authority is misdirected and its lesson pointer is not yet on disk; `negA-probe.md` is
  mislabeled. These are the discrepancy class the lane's calibration axis exists for.
- **freshness / coverage / adjacency:** no claim touched them; no harm observed.
- **admission-level:** the egress-ordering defect (§5) blocks C1's sourced evidence under the rule as
  written unless the operator regularizes the window.

VERDICT: R81CriticClaims C1 held — K1 passes at the landing revision and no K3 contradiction was found, but the depth predicate is not a depth measure: a two-entry filler tree with six one-word quotes and 3×2 dummy tables prints `DEPTH_R81=PASS` (§9 cheapest-control defect), and the five counted captures were fetched before the egress table existed, in a window `SKILL.md` calls loopback-only.
VERDICT: R81CriticClaims C2 fired — kill rule K2 fires on both items: a well-formed record whose negative claim names sweep W1 with no W1 row exits 0, and a `## Rejections` row whose flip condition is `-`, `none`, or absent-as-a-bullet exits 0 under the landed Run lines, while the item-4 line returns CLEAN on `corpus/SOURCES.md` itself; a base tree with three fixture-keyed junk Run lines scores `CHECKLIST=PASS`.
