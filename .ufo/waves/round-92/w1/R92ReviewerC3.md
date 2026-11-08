# R92ReviewerC3 — C3 stated-wording attacks (frozen instruments at carrier C5 16ccf769)

Axes (godspeed): C1 operability / C2 calibration / C3 freshness — this seat attacks C3 wording only.
Tree: `git clone --shared` → scratch `/fast/scratch/hyaku/chousa-r92/R92ReviewerC3/repo`, checkout
`16ccf7693c61b8ffe392fc757352304f239bfcad` (asserted `rev-parse --show-toplevel` = that dir).
Instrument read first: `corpus/evidence/round92/skill-tally-r92.py` (scope lines 72-80, others 94-101,
case-range 108-135) and `corpus/evidence/round92/claims.md` §C3 + `plans/round-92.md`.
All runs: `python3 -B corpus/evidence/round92/skill-tally-r92.py --root <scratch-tree> --selftest <receipt>`
from the scratch repo. Baseline reproduces the frozen predicate (receipt `r-baseline.txt`).

## A1 — heading after `## Gates` not `## `-prefixed: scope bleeds (NOT neutral — narrowing fires)

**Claim sentence attacked:** "the tally search and the two case-range searches run over the `## Gates`
section only (up to the next `## `)"; "the 215 tail tally sits after `## Round26` and is unbound by design."

**Construction (three variants, same handling):** scratch SKILL.md = landing SKILL.md except the single
heading at line 576 is renamed: (1) `# Round26 …` (level-1), (2) `##X Round26 …`, (3) `  ## Round26 …`
with two leading spaces. No other byte changes.

**Commands & observed:**
- `python3 -B corpus/evidence/round92/skill-tally-r92.py --root …/a1-h1 --selftest …/selftest-r92.txt`
  → `TALLY_ROWS=9 STALE_TALLIES=0/9 … OTHER_OCCURRENCES=3 … OTHERS_OK=0 LEGS=2/3`,
  `LEG_FAIL OTHERS expected={('161','0'):1, ('256','0'):1} observed={('256','0'):1, ('161','0'):1, ('215','0'):1}`,
  `SKILL_TALLY_R92=FAIL`, exit 1 (`r-a1-h1.txt`). Identical for a1-h2, a1-indented (`r-a1-h2.txt`, `r-a1-indented.txt`).
- Scope autopsy (code path, lines 73-77): `gates_start = text.find("## Gates")`, `nxt = text.find("\n## ", …)` —
  none of the three renamed headings contains the literal `\n## `, so `gates_text` runs to EOF and swallows
  the Round26 tail. Two bleed effects observed in the same run: (a) the 215 tally joins the others multiset
  (`OTHER_OCCURRENCES=3`, `OTHERS_OK=0`); (b) the 9th CURRENT row appears (line 781
  `userns exists). Selftest \`PASS (283 cases, 0 skipped)\`` which in the clean tree sits after `## Round26`
  and is excluded) — `TALLY_ROWS=9` vs baseline 8.

**Verdict: FALSIFIES-WORDING (firing).** The instrument obeys the literal sentence ("up to the next `## `"),
but the sentence's premise — "the 215 tail tally is deliberately out of scope under the section scoping" —
holds only while the next heading keeps the exact `## ` at column 0. A heading-level change 1-2 chars away
converts the deliberately-unbound 215 into a bound failure with **no boundary diagnostic**: the verdict
blames `OTHERS` while the actual cause is scope bleed. K3's protection ("historical tally outside
`## Gates` moves") is silently reversed: moving the boundary marker, not the tally, changes the verdict.
**Narrowing to record** (`plans/round-92.md` Amendments): the section boundary is the next line matching
`^## ` at column 0; a heading rewrite to `# `, `##X`, or indented `## ` is not a boundary, and the 215
tally's out-of-scope status is contingent on the literal `## Round26` heading remaining — a bleed diagnostic
(e.g. `SCOPE_BLEED` when the slice contains a `# ` heading or a tally beyond the pinned pair) is required
before the 215 can be called "unbound by design" rather than "unbound contingent on heading form".

## A2 — `## Gates` deleted / clauses deleted: refused, SETUP or FAIL (NEUTRAL re K4 wording — reading strengthened)

**Claim sentence attacked:** K4 "an absent clause is tolerated" as a finding class.

**Construction:** (a) scratch SKILL.md with the `## Gates` heading line deleted, table kept;
(b) scratch SKILL.md with only the two range clauses (`r39 bash-pin cases 273–275 …` / `bash-pin-override
cases 282–283`) in the Gates row replaced by `[clauses deleted]`, section present.

**Commands & observed:**
- (a) `… --root …/a2-nogates …` → `SKILL_TALLY_R92=SETUP no ## Gates section in SKILL.md`, exit 2 (`r-a2-nogates.txt`).
- (b) `… --root …/a2b-clause-absent …` → `CASE_RANGE_FINDING CLAUSE_MISSING:r39-bash-pin`,
  `CLAUSE_MISSING:bash-pin-override`, `CASE_RANGE_OK=0/2`, `LEG_FAIL CASE-RANGE`, `SKILL_TALLY_R92=FAIL`, exit 1 (`r-a2b-clause-absent.txt`).

**Verdict: NEUTRAL (wording holds).** An absent section is a refusal (exit 2), not a tolerated pass; absent
clauses are `CLAUSE_MISSING`+FAIL. The K4 phrase "an absent clause is tolerated" is therefore a true
kill class: the instrument does *not* tolerate it. No narrowing needed; the wording is, if anything,
understated (section-absence is even louder — SETUP exit 2, distinct from FAIL exit 1).

## A3 — duplicated `ok-case 5` with a different name: counted nowhere (FALSIFIES-WORDING quotient — narrowing fires on "verdict counts")

**Claim sentence attacked:** "every current tally row equals the tool's verdict counts" (and T1/leg-1 design
"every current tally row equals the tool's verdict counts").

**Construction:** scratch selftest receipt = committed `selftest-r92.txt` plus one inserted line
`ok-case  5  dup-case-5-different-name exit=1` after case 5 (284 `ok-case` lines; verdict line unchanged:
`RESEARCH_GATE_SELFTEST: PASS (283 cases, 0 skipped)`). SKILL.md = landing tree. Diff: `diff-a3-dup.txt`.

**Command & observed:** `python3 -B …/skill-tally-r92.py --root …/a3-dupcase --selftest …/selftest-dup.txt`
→ `EXPECTED_CASES=283 EXPECTED_SKIPPED=0 … LEGS=3/3`, `SKILL_TALLY_R92=PASS`, exit 0 (`r-a3-dupcase.txt`).
The dup changes nothing: `cases`/`skipped` come from `VERDICT_RE` on the verdict line (lines 61-65);
`names = CASE_RE.findall(out)` (line 66) is used *only* for the two family derivations
(`bashenv` substring, `bash-pin-override` prefix, lines 109-110) — there is no `len(names)==cases` leg,
no duplicate-number leg, and no name-identity leg. Control: renaming every ok-case name (receipt
`selftest-rename.txt`, 283 lines, verdict kept) changes the derived bash-pin range to `none` → FAIL, proving
names matter only as family membership, never as counts (`r-a3-rename.txt`).

**Verdict: FALSIFIES-WORDING (firing) — narrowed.** A receipt with 284 case lines (one number twice, two
names) and `EXPECTED_CASES=283` passes. The sentence "tallies equals the tool's verdict counts" is true
only of the verdict *line* (283), not of the enumerated `ok-case` lines, which are never counted. A
duplicated, dropped, or extra `ok-case` line is invisible unless it perturbs one of two family min/max
ranges. **Narrowing to record** (Amendments): pin the enumeration — `len(names)==cases` and
duplicate case numbers refused — or restate the bound as "the verdict line's two figures and the two
family ranges only"; as frozen, "verdict counts" does not bind the case enumeration.

## A4 — r39 clause moved below `## Round26`: scoped out, CLAUSE_MISSING (NEUTRAL — wording holds)

**Claim sentence attacked:** Named limit (1) "a clause moved outside `## Gates` leaves the leg and the
counter prints `CLAUSE_MISSING`."

**Construction:** scratch SKILL.md with the r39/override clause stripped from the Gates table row
(replaced by `[r39/override clause moved prose]`) and re-inserted verbatim as a line immediately after
`## Round26 metadata options and resource qualification` (line 578-580), i.e. inside another section.

**Command & observed:** `python3 -B …/skill-tally-r92.py --root …/a4-moved --selftest …/selftest-r92.txt`
→ `CASE_RANGE_FINDING CLAUSE_MISSING:r39-bash-pin`, `CLAUSE_MISSING:bash-pin-override`,
`CASE_RANGE_OK=0/2`, `LEG_FAIL CASE-RANGE`, `SKILL_TALLY_R92=FAIL`, exit 1 (`r-a4-moved.txt`).

**Verdict: NEUTRAL (wording holds exactly).** The clause outside `## Gates` is not found; both legs print
`CLAUSE_MISSING` as the sentence promises. Not silently found.

## Committed battery (context, not an attack)

`python3 -B corpus/evidence/round92/skill-tally-r92-controls.py --root <repo> --work <scratch>` →
`CONTROLS=PASS OLDPROSE_REFUSED=1/1 PRIOR_ACCEPTED=1/1 STALE_REFUSED_BOTH=1/1`, exit 0 (`r-controls.txt`).
Matches the frozen C3 battery figures.

## Residual risk / verification gaps

- A1: the bleed also *adds* a current row (line 781). A bleed that adds an *agreeing* 283 row changes no
  verdict except TALLY_ROWS — the count change is the only trace. No scoped run distinguishes
  "clean scope, moved heading" from "dirty scope" in the diagnostic vocabulary.
- A3: family derivation is itself crash-fragile — renaming all names makes `derived_ovr=None` and the
  `CASE_RANGE_BASH_PIN=none` path returns FAIL without MISLABELED counts; not a wording question here.
- All fixtures are single-edit scratch-tree copies at C5; instrument bytes are the committed r92 ones
  (pinned? — C1's pins file was not re-verified by this seat; tally runs use the on-disk instrument at C5).

`VERDICT: R92ReviewerC3 C3 fired — A1 scope bleed and A3 uncounted case enumeration falsify the C3 wording as stated; A2 and A4 hold.`
