# R97ConnectorSiblings — cross-lane pattern scan (read-only) + three falsifications

Seat: cross-lane connector, round 97. Attacked tree: `F 9a0ce2015fa0254848f2f32f612b20caf7dc5478` (clone
`git clone -q --shared … $S/repo && git -C $S/repo checkout -q 9a0ce2…`), base `c8087ac5…`. Scratch
`/fast/scratch/hyaku/chousa-r97/R97ConnectorSiblings`, deleted at exit. No sibling repo, no production file,
no lane/fleet git was written; every sibling read is `git -C <repo> grep` / `git -C <repo> rev-parse`.

Mission was the scan in my dispatch plus the standing falsification duty. The scan produced no PRESS 2015
hold anywhere in the fleet (§3) and two sibling entries that bear directly on C1's own method (§4); the
falsification duty produced one fired claim (§1), two held claims with routed defects (§2, §5) and one
duplicate of another seat's finding (§6).

---

## 1. F1 — C1's external set is described as "the 28 non-equivalent mutants"; the 29th is not equivalent
   (novel; C1 **fired** on wording, predicates still met)

**What the claim says** (`claims.md`, C1 sentence and named limit f): the 30 named external mutants are
"the 28 **non-equivalent** mutants that `R96MutantsC1` wrote and applied in round 96 … plus the two
`git_env` mutants", and "`n30` is excluded as equivalent (the seat's own verdict, `R96MutantsC1.md:154-159`)".
The battery encodes the same ground: `EXCLUDED = {"n30-sep-row-lenient": "equivalent (R96MutantsC1.md:154-159)"}`
(`corpus/evidence/round97/selftest-controls-r97.py:49-50`), and the only guard on the set is a count
(`if len(external) != 28: … return 2`, `:151-153`). **No instrument in the lane tests the equivalence
verdict**; it is a prose verdict, copied forward.

**What the round-96 verdict reasons** (`R96MutantsC1.md:154-159`): "`cells` on a separator row always yields
8 cells whenever the header checked. Recorded as equivalent, not a coverage hole."

**That premise is false.** `cells()` is a splitter — `SPLIT_RE.split(s[1:-1])` on the line it is given
(`tools/search-rerun.py:124-126`) — so a 7-cell separator row yields 7 cells. The `len(sep) != len(HEADER)`
test the mutant deletes is the *only* thing that rejects it.

**Witness (the check tameshi's lane requires for an equivalence claim, §4a).** Command (receipt
`R97ConnectorSiblings-n30-witness.txt`; probe imports the F tool and the n30 mutant and parses one record):

```
SEP-BEFORE: '|---|---|---|---|---|---|---|---|'
ORIGINAL: ('REFUSED', 'TABLE')
N30-MUTANT: ('OK', 1)
NON_EQUIVALENT_WITNESS: True
SEP-CELLS: 7 HEADER-CELLS: 8
```

The original refuses the record `TABLE`; the mutant returns one parsed row. The mutant is **observably
non-equivalent**, so the exclusion's stated ground is false.

**And the mutant survives the landed self-test** — `python3 -B $S/n30.py --selftest` → `EXIT=0`,
`SEARCH_RERUN_SELFTEST: PASS cases=47/47` (same receipt). Note the direction: this is not a harm to the
47 cases; it is a hole in the *population* the claim says is covered, plus a false description in its
sentence.

**Falsified as stated:** "the 28 non-equivalent mutants that `R96MutantsC1` wrote and applied" is false —
29 of the 29 applying mutants are non-equivalent: the 28 are provably non-equivalent by their own kills at
F (a kill is a witness — the failing case is an input on which mutant and original differ), and n30 is
provably non-equivalent by the witness above, which is why its exclusion cannot stand. The battery's 30 sit
on a set that under-reports the non-equivalent population by one, and the missing one is a *named round-96
site* which the claim's own named limit (a) defines as the thing being covered ("these named sites are now
covered").

**Predicates unaffected:** predicate 1 re-run at F, `EXIT=0`, last line `SEARCH_RERUN_SELFTEST: PASS
cases=47/47` (receipt `R97ConnectorSiblings-selftest-baseline.txt`); predicate 2's tallies reproduce at `after/c1-all.txt:144-145` (`POSITIVE=1/1 EXTERNAL_KILLED=30/30 … BASE_KILLED=10/30
CASES=47`, `SELFTEST_CONTROLS_R97=PASS`), with the base's n11 survivor at `:93` (`rc=1 SURVIVED failed=-`), the
shape the claim's Before paragraph describes — but see §6 for the receipt-provenance problem. So this is a wording/number
fault, not a predicate failure: K1 does not fire, K2 does not fire (n30 is not named as external), and the
claim's *counts* still hold over the population it actually uses.

**Bounded move proposed (one):** replace the prose equivalence verdict with the witness. Restore
`n30-sep-row-lenient` to the scored set and add one in-memory case (`r16-sep-width`) asserting
`parse_text` raises `Setup("TABLE", …)` on the 7-cell-separator record above. Second-order edits that move
forces, all mechanical: `EXCLUDED` loses its second entry (`:60`), the set-size guard becomes 29
(`:145`), `N_CASES` 47→48, and every restated number in `claims.md` and in the battery docstring
(`EXTERNAL_KILLED=30/30`→`31/31`, `BASE_KILLED=10/30`→re-measured, `CASES=47`→`48`). Risks: the base kill
count for the added mutant is unmeasured by me, so the do-nothing control's expected value must be
re-measured, not guessed; and the claim text is frozen, so the honest alternatives are (i) the move above
plus a re-frozen claim, or (ii) withdrawing the word "non-equivalent" from the sentence and re-stating
limit (f) as "n30 excluded on an unverified verdict". Verification of the move:
`python3 -B tools/search-rerun.py --selftest` → `PASS cases=48/48`; `python3 -B corpus/evidence/round97/
selftest-controls-r97.py --root . --work <scratch>` → `EXTERNAL_KILLED=31/31 … CASES=48`; and the witness
probe above must print `NON_EQUIVALENT_WITNESS: True` before the mutant is admitted to the set.

---

## 2. F2 — the self-test covers the guard *function*, not its launch-site carriers; the round-95 battery does
   (novel probe; C1 **held** — named limit (c) is accurate)

mado's round-74 entry is the exact statement of this class (§4c): "A carrier it does not count is a real
check script that looks guarded and is not." chousa's guard is `git_env()` (`tools/search-rerun.py:109-117`)
and it is handed to git at two sites (`:120`, `:280`).

Probe M-A drops the carrier at the launch site only — `subprocess.run(["git", …], capture_output=True,
env=git_env())` → `capture_output=True` (1 application; receipt `R97ConnectorSiblings-mutA-launchenv.txt`):

- `python3 -B $S/mutA.py --selftest` → `EXIT=0`, `SEARCH_RERUN_SELFTEST: PASS cases=47/47` — **survives
  the self-test**, exactly as named limit (c) declares ("the self-test still does not exercise the git and
  disk readers").
- `TMPDIR=… python3 -B corpus/evidence/round95/rerun-controls-r95.py --root . --work … --tool $S/mutA.py`
  → `EXIT=1`, `CASE containment-git-dir rc=2 expect=0 FAIL`, `CONTAINMENT=1/2`, `RERUN_CONTROLS=FAIL`.

So the lane *does* hold a carrier instrument for this site — the round-95 battery's `containment-git-dir`
case — and the claim's statement that the round-95 battery covers what the self-test cannot (K4's harm
instrument) is **confirmed by an independent mutant the battery's author did not write**. This is
mado-R74's lesson, resolved one level down; it duplicates mado's method and does not contradict C1.
Residual, worth the reviewer's eye only: the two sentinel mutants among C1's 30 (F1
`GIT_NO_REPLACE_OBJECTS` dropped, F7 only `GIT_DIR` scrubbed) are mutants of the *function*;
the *carrier at each call site* is covered by `containment-git-dir` at one site. Whether the second site
(`:280`) is covered is not measured by me.

---

## 3. Does any sibling hold a reachable copy of the PRESS 2015 checklist primary? **No.**

Five sweeps, all read-only (receipt `R97ConnectorSiblings-sibling-scan.txt`):

| sweep | result |
|---|---|
| `git -C <repo> grep -nIE 'PRESS 2015\|PRESS checklist\|Preferred Reporting Items for Peer' -- corpus/ tools/ plans/ reports/ docs/` over 21 siblings | no match anywhere (exit 1 each) |
| `git -C <repo> grep -oE '\bPRESS\b' -- 'corpus/knowledge/*'` | 0 occurrences, all 21 siblings |
| `git -C <repo> grep -nIE 'McGowan\|work\.cochrane\.org\|kib\.ki\.se'` | only unrelated hits: souji `census/round-90/srcs/tr14.html:4578` (Unicode names, Rick McGowan) and tsukuroi `.ufo/waves/round-88/w1/ConnectorOverlap/…:18` (a Cochrane Information Retrieval Methods Group author list in an unrelated capture) |
| `git -C <repo> grep -nIE 'spelling errors\|orphan lines'` | unrelated senses only (wave-line counters, MDN spellcheck page) |
| `ls /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache \| wc -l` | `0` — the shared campaign cache is empty, so the one cross-lane cache a chousa row can reach holds nothing |

Consequence for C2's tier/scope cells: S225/S226/S227 stand or fall on chousa's own captures; there is no
second lane to corroborate against, and the primary (McGowan 2016 / the guideline statement) is not held
anywhere in the fleet. This is consistent with C2's own named limit (b).

---

## 4. Cross-lane match table

Revisions as at scan (`git -C <repo> rev-parse --short HEAD`); kagi moved `ba8c730`→`17a8964` mid-scan.

| # | path | rev | one-line relevance | vs chousa C1 / C2 |
|---|---|---|---|---|
| a | `tameshi-shokunin/corpus/knowledge/witness-scoped-kill-verdict.md:13,23,27` | `ab60e134` | four verdicts (`killed` / `accidental` / `unapplied` / `baseline`); a kill counts as killed-on-witness only if the pre-registered failing label is among the captured ones | **Duplicates C1's shape, contradicts its kill rule's precision.** chousa's `killed()` (`selftest-controls-r97.py:92-97`) accepts *any* `SEARCH_RERUN_SELFTEST: FAIL` + `rc=1` + no traceback; it never requires the failed case to be the mutated site — tameshi's `accidental` class is not excluded. Low risk here (each mutant has a case aimed at it), but the rule as written cannot distinguish them. |
| b | `tameshi-shokunin/corpus/knowledge/llm-mutant-equivalence-cost.md:7,24,52` | `ab60e134` | equivalence is undecidable (S287); "a witness is per-mutant evidence (an input where the mutant and the original differ), never a general decision procedure"; a survivor is not yet a test hole | **Contradicts C1's exclusion method** (F1). chousa excludes n30 on a seat verdict, not a witness; my witness shows the verdict was wrong. This is the fleet's own standard for exactly this judgement. |
| c | `mado-shokunin/corpus/knowledge/guard-carrier-twohop-environ-alias-r74.md:12` | `f77ed5e9` | a guard census must count carriers — aliases of `os.environ`, dotted-path aliases — because "a carrier it does not count is a real check script that looks guarded and is not" | **Duplicates C1's guard concern, one level down** (F2). chousa's `git_env()` is behavioural (planted env, r13), stronger than a static classifier on the function; the *call-site* carrier is caught by the r95 `containment-git-dir` case, not by the self-test. No contradiction. |
| d | `mado-shokunin/corpus/knowledge/control-set-mutant-kill-r73.md:4,15-20` | `f77ed5e9` | "a frozen control set has its own measurable property: how many named mutations of the rule it certifies it can separate"; `killed=4 base_killed=2 verdict=TARGET_MET` — a control set plus a **base/do-nothing** control | **Direct structural twin of chousa's battery** (`POSITIVE` / `EXTERNAL_KILLED` / `DO_NOTHING_REFUSED` / `BASE_KILLED`). Duplicates the method; supports reading C1 as the same pattern at a larger N (30 vs 4). |
| e | `tabi-shokunin/corpus/knowledge/bidi-gate-selftest-round-34.md:9-10` | `360d7cc9` | 20 single-point mutants of the rule lines, self-test killed 8; "a rule whose mutant survives the self-test is an unverified checklist item"; one isolated case added per survivor, plus neutral/decoy/**twin** probes | **Duplicates C1's r01-r15 move** exactly. One gap it names that chousa does not fill: a **twin/equivalent probe** — chousa scores only killable mutants and *excludes* the one mutant it believes equivalent, so the battery never demonstrates that its kill rule declines to "kill" an equivalent mutant. §1's move supplies the missing twin. |
| f | `kagi-shokunin/corpus/knowledge/claim-instrument-heldout.md:6,10,44` | `ba8c730` (read) / `17a8964` (scan) | "a checker's own fixture table is not evidence for that checker"; a held-out set must be **sealed before the hardening** | **C1 satisfies the first clause and fails the second.** Its 47 cases are its own fixtures, which the 30 external mutants (written by a non-author seat in round 96) convert into evidence — good. But they were not sealed before round 97's 15 cases were written (named limit a says so). kagi's standard is one notch stricter; route, do not absorb. |
| g | `kagi-shokunin/corpus/knowledge/claim-instrument-falsifiability.md:6,132` | `17a8964` | a gate's `--selftest` "must execute its own aggregation"; a token-presence-only item is a declared ceiling | **C1 satisfies both.** The summary line is computed from `k`/`n` (`tools/search-rerun.py:568-570`), and the constant-PASS stand-in is caught (`after/c1-all.txt:138`: `POSITIVE=1/1 EXTERNAL_KILLED=0/30 … ` → battery FAIL). No contradiction. |
| h | `kotodama-shokunin/corpus/knowledge/verification/verification-independence-anti-circularity.md:40` | `5fa04a9b` | quotes the fleet rule: "several URLs or witnesses copying one account are one evidential lineage, not independent corroboration — *count witnesses, not websites*" | **Contradicts the word "independent" in S226's scope cell** (§5). Does not touch C2's numbers. |
| i | `kasegi-shokunin/corpus/instruments/r46-selftest-f29.py:1-30`, `corpus/instruments/anchorcheck.py:98-108` | `a887f61` | per-case fixture isolation restored per case; a registry that asserts every declared limb is covered, prints the failing case **and that case's** stdout/stderr, exits 1 on an uncovered limb | **Duplicates C1's per-case guard and improves on it in one respect:** kasegi asserts *coverage of the declared case list*, so a silently dropped case is a failure. chousa's `case()` prints one line per case and the tally is `k/n`, so a dropped `case()` call would surface as `cases=46/47` — same effect, reached differently. No contradiction. |
| j | `tameshi-shokunin/corpus/knowledge/fleet-kill-rate-ledger.md:1-20` | `ab60e134` | one row per gate: suite size, kill-rate, survivor classes, hardened-or-not, sweep pin; "a rate is never implied to hold at a later revision" | **Duplicates C1's purpose** (operability = kill-rate of a suite). C1's numbers are revision-bound as that entry requires. No contradiction. |

Not matched, for the record: no sibling holds a self-test that *scores against externally-written mutants
for a research-lane gate other than the above*; the closest code-level instruments are mado's
`quality/counters/c1-r73-summary-mutants.py` and `c2-r74-shapes.py` (control set + base control, measured
`controls=36/36 base_controls=32/36`), tabi's `.ufo/waves/round-34/counters/c2-gate-mutants.mjs`, and
kasegi's two instrument self-tests above.

---

## 5. F4 — C2 **held**, two defects routed (not fired)

**F4a — the verdict word `CLEAN` tolerates total set drift.** Command (receipt
`R97ConnectorSiblings-c2-verify-both-tools.txt`, cwd = F clone):

```
python3 -B tools/search-rerun.py verify corpus/knowledge/press-checklist-questions-r97.md --root .   EXIT=0
SEARCH_RERUN Q1 rev=MATCH tree=CHANGED recorded=0 at_rev=0 at_tree=2 TREE_CHANGED        (Q1..Q7 all +2)
SEARCH_RERUN_SUMMARY searches=7 rev_match=7/7 tree_same=0/7 findings=0
SEARCH_RERUN: CLEAN
```

Every one of the 7 recorded sets fails against the landing tree (`tree_same=0/7`) — because the entry
itself now sits in the searched corpus and each expression gains 2 hits — and the tool still prints
`CLEAN`, exit 0. C2's predicate 3 quotes only `rev_match=7/7` + `CLEAN`, and both are observed, so the
predicate holds. But the sentence's prose — "the entry's 7 searches … re-run at that revision with the
recorded count and set" — reads as reproduction of count *and* set, which the instrument does not enforce
and the tree does not satisfy. Two bounded consequences, both second-order and neither in any claim:
(i) if the words "count and set" are meant, the sentence says more than the verdict enforces and the
landed entry cannot satisfy it, because its own bytes are in the corpus; (ii) every future re-run of these
7 searches must record counts that include this entry, or `tree_same` stays 0. The same summary line at
base (`c8087ac5` tool, same tree) is identical, which is what makes the separability claim true — see §6.

**F4b — "independent" in S226's scope cell claims more than the bytes support.** `corpus/SOURCES.md:238`
calls S226 "a second, **independent** reprint of the PRESS 2015 checklist questions". Both S225 (Cochrane
reprinting the checklist, "Derived from" McGowan 2016) and S226 (Karolinska's reprint) reproduce the *same*
McGowan-2016 account; kotodama's entry (§4h) states the fleet rule that copies of one account are one
evidential lineage, not independent corroboration. S226's own limit cell already records that the two
"differ in wording", i.e. each is a re-type. Read evidentially, "independent" overstates; read as "a
separate institution's reprint", it is exact. C2's frozen sentence is careful ("a second reprint … used for
corroboration and never as a row's only support") and does not use the word — the exposure is K4's, on the
SOURCES cell, and it is a narrowing, not a false number. The corroboration counts (10/26, 14/26) measure
carrier agreement and are not affected.

---

## 6. F3 — the `after/` receipts are not at F (independently confirmed; already reported by `R97ExecC2Repro`)

Receipt `R97ConnectorSiblings-receipts-at-F.txt`:

```
git ls-tree -r --name-only F -- corpus/evidence/round97   → 6 files: before/c1-base.txt, before/c2-base.txt,
    census-start.txt, egress-approval.md, entry-controls-r97.py, selftest-controls-r97.py      EXIT=0
git status --porcelain corpus/evidence/round97            → ?? corpus/evidence/round97/after/  EXIT=0
ls corpus/evidence/round97/after/                         → c1-all.txt, c1-verify-harm-and-c2-separable.txt,
                                                            c2-all.txt                          EXIT=0
ls corpus/evidence/round97/after/c2-separable-base-tool.txt → No such file or directory           EXIT=2
```

Two distinct facts: (i) the whole `after/` directory is untracked, so nothing in it is at F — the C1 and C2
"after" tallies cannot be read from the frozen tree; (ii) the file C2's separability paragraph *names*,
`after/c2-separable-base-tool.txt`, **does not exist even in the worktree**, and the receipt that does
exist (`c1-verify-harm-and-c2-separable.txt`) holds three `SAME … rc=0` verdict-equality lines and no
`rev_match=7/7` line. The substantive statement is nonetheless true and I reproduced it: the base tool
prints `rev_match=7/7`, `tree_same=0/7`, `SEARCH_RERUN: CLEAN`, `EXIT=0` on the same entry
(`R97ConnectorSiblings-c2-verify-both-tools.txt`, first block). So: fact true, cited receipt path false,
freeze incomplete on evidence. `R97ExecC2Repro.md:17,71,78` reported (i)+(ii) first; I confirm it from the
frozen clone rather than the worktree, which is the stronger form.

---

## 7. Axes touched, and what I did not do

- **C1 operability:** fired on wording only (§1). Predicate 1 re-run independently (`47/47`); the r95
  battery / r96 rebuild legs were not re-run by me (the executor seat holds them) — I ran only the single
  M-A probe through `rerun-controls-r95.py`, 44 s, `EXIT=1`.
- **C2 depth:** held. Predicate 3 reproduced on both tools; predicates 1, 2, 4 were not re-run by me (the
  entry-controls battery is `R97ExecC2Repro`/`R97MutantsC2`'s seat) — I read their published receipt
  `after/c2-all.txt` for the tallies, which is exactly why §6 matters.
- **No production edit, no lane or fleet git mutation, no commit, no sibling write, no `sudo`, no pacman,
  no tool install (nothing was needed).** Scratch removed before yield.

## VERDICT

VERDICT: R97ConnectorSiblings C1 fired — C1's sentence calls its 30 mutants "the 28 non-equivalent mutants … plus two", but `n30-sep-row-lenient` is observably non-equivalent (7-cell separator: original refuses `TABLE`, mutant parses one row) and survives the landed self-test at `cases=47/47`, so the exclusion's stated ground and the population's stated size are both false.
VERDICT: R97ConnectorSiblings C2 held — `rev_match=7/7` and `SEARCH_RERUN: CLEAN` reproduce on the base and F tools, but the frozen tree carries no `after/` receipt, the named `after/c2-separable-base-tool.txt` exists nowhere, `tree_same=0/7` rides along with `CLEAN`, and S226's "independent" claims more than one McGowan-2016 lineage supports.
