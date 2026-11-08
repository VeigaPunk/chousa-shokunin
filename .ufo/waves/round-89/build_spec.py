#!/usr/bin/env python3
"""Build the round-89 wave-1 spec (12 seats, policy v1 band 8-16). Run from anywhere; writes w1-spec.json beside itself."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
SCRATCH = "/fast/scratch/hyaku/chousa-r89"
BASE = "f8fa55ec94cb34e7b572a9d87d7f62d88bc80bf8"
FREEZE = "ac0a0892c15de11fb28d3208f2b287687c00477e"

GODSPEED = """/skill:godspeed

You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.
"""

CONTEXT = f"""Lane chousa round 89, L1 ChousaR89 holds the canonical planner seat, the freeze and the integration. Root {LANE}.
Revisions: base {BASE} (round-88 landing + its non-author spot-check); claim freeze {FREEZE}; the bytes you attack are
{FREEZE} (the freeze commit carries both counters, their control batteries, the receipt driver and the pins — there is
no separate landing commit, so build your trees at {FREEZE}).
Frozen predicate set: {LANE}/corpus/evidence/round89/claims.md — read it FIRST, with every kill rule and every NAMED
LIMIT — and {LANE}/plans/round-89.md for the seven pre-freeze repairs. Machine form: {LANE}/.ufo/waves/round-89/claims.json.
Two claims, both successors of round-88 bytes; the subject tool `tools/gate-records.py` is UNCHANGED (sha256 905f9da2…).

C1 operability: `corpus/evidence/round89/gate-records-r89.py` must print `GATE_RECORDS_R89=PASS` with
`LEG_REREAD=16/16 RECONCILED=16/16 CROSSCHECK=15/15 LEGS_APPENDED=16` — each leg's receipt detail is re-derived in its
OWN grammar (`n/m`; `len/d1/div3 pinN` with all four equal and pin == ROWS_203; `derived=x killed=y` with both 1;
`tool present`), and each leg's re-derived numbers must equal the summary fields printed for it (`DIV3` is printed for
that reason). `mutate-r89.py` must print `MUTANTS_KILLED=11/11 TOOL_MUTANTS_CAUGHT=2/2`; the four shapes round 88's
wave left alive are `E7c` (detached width ok over a narrowed third derivation), `E7b` (detached mutant ok over zeroed
measurements), `E7d` (forged width detail), `E7f` (printed field detached from its measurement).
C2 calibration: `corpus/evidence/round89/curation-r89.py` must print `CURATION_R89=PASS` with nine legs,
`DUP_QIDS=0 WARRANT_OK=17/17 QUOTES_LOCATED=20/20 TEACHES_FLAGGED=1 TEACHES_UNRESOLVED=0 SUP_CLAUSE_CHECKED=0
SUP_UNRESOLVED=0` and a verdict derived from the printed fields (`VERDICT fields_hold=1`);
`curation-r89-controls.py` must print `CONTROLS=PASS FORGERY_REFUSED=7/7 PRIOR_ACCEPTED_FORGERY=7/7`;
`curation-r89-mutants.py` must print `MUTANTS_KILLED=6/6 COUNTER_DETECTED=5 BATTERY_DETECTED=1`.
Ground sources: S216 (RFC 9110 §15.3.4, committed capture `corpus/captures/b1b13a12aee75c6ecc20fb91.txt`) and S218
(own-work: QUALITY 178 + CORPUS rule 2). Both rows' `used-by` gained `corpus/evidence/round89/claims.md` this round and
that is the ONLY registry change (two cells).

Every `Report:` trailer path is relative to {LANE} — write it at {LANE}/<that path>.

Leaf only: no task tool, no subagents, no agent://all, no production edits, no lane or fleet git/jj mutation, no commits
or pushes, no edits to /home/vgpnk/Projects/shokunin/scripts, /home/vgpnk/Projects/shokunin/.ufo/state, MANIFEST.json,
considerthese/ or any sibling repo. The only files you write are under {LANE}/.ufo/waves/round-89/w1/<seat>/ plus your
scratch dir. Network: none this round — every check reads committed bytes (a GET is a finding). Never mutate a host
sysctl, never run sudo, never restart a host service.

Scratch: every tree, work dir and fixture lives under {SCRATCH}/<your seat name>/; create it with `mkdir -p`, pass it
explicitly (`--work`, `TMPDIR=`), delete it before you yield (`trap 'rm -rf -- "$S"' EXIT` in shell, `finally:
shutil.rmtree` in Python), and copy every receipt you cite into your wave output folder first. Never write under /tmp.
Build a tree at a revision with `git -C {LANE} archive <rev> | tar -x -C <scratch dir>`; any fixture git repo is
`D=$(mktemp -d -p {SCRATCH}/<seat>) && test -n "$D" && git -C "$D" init -q`, every later git call names `-C "$D"`, and
you assert `git -C "$D" rev-parse --show-toplevel` equals `$D` before any mutating git command.

Counter that binds you: every finding names the exact command, the receipt path you wrote and the observed line plus
exit code. An unrun check has not passed; a deviation from an expected value is a finding, never something to hide.
End your report with one line `VERDICT: <seat> <C1|C2> fired|held|n/a — <one sentence>` per claim you touched (plain
text, not JSON). A seat that ships no `VERDICT:` trailer is tallied as a seat-discipline finding.

Tooling authorization (operator, 2026-10-19): you may install or upgrade tools that help the task; read
/home/vgpnk/.omp/agent/RULES.md first (official channels only; record tool/version/channel/reason in your report).
pacman guard (orchestrator ruling 2026-10-20): all pacman transactions are PAUSED host-wide — install via `uv tool`/
`npx`/an official binary in ~/.local/bin, or not at all; never `pacman -Sy`, `-Syu`, `-U`, `-R`, never downgrade.
"""


def seat(name, role, body):
    return {"name": name, "role": role, "prompt": GODSPEED + "\n" + body.strip() + "\n"}


ITEMS = [
    seat("R89ExecRepro", "executor", f"""
Reproduce both frozen claims from a clean tree. `S={SCRATCH}/R89ExecRepro`; `git -C {LANE} archive {FREEZE} | tar -x -C $S`.
(a) `python3 -B $S/corpus/evidence/round89/gate-records-r89.py --root $S --repo {LANE} --work $S` — record the two lines
and the exit. Then re-derive independently: the 203 width from `$S/corpus/evidence/round57/refetch.tsv`; the leg receipts
under `$S/legs/` and their own reconciliation, including `SUMMARY.txt`; `CROSSCHECK` by hand for three legs.
(b) `python3 -B $S/corpus/evidence/round89/curation-r89.py --root $S` — re-derive `QUOTES_LOCATED`, the per-entry qid
sets, the token-floor minimum over the 20 located quotes, `WARRANT_OK` (hand-check 5 of 17 rows), the one flagged row and
its disposition, and confirm `SUP_CLAUSE_CHECKED=0` is the true population.
(c) Confirm every path in `$S/corpus/evidence/round89/instrument-pins.txt` hashes as pinned, and that
`$S/tools/gate-records.py` is the landed blob (`905f9da2…`).
(d) `python3 -B $S/corpus/evidence/round89/mutate-r89.py --root $S --repo {LANE} --work $S` and
`python3 -B $S/corpus/evidence/round89/curation-r89-mutants.py --root $S --work $S`.
Every deviation is a finding with its receipt. Write `R89ExecRepro.md` + `receipts/`."""),

    seat("R89ExecHarm", "executor", f"""
Harm sweep, wider than the round's own. `S={SCRATCH}/R89ExecHarm`; trees at `{FREEZE}` and `{BASE}`.
(a) `python3 -B $S/corpus/evidence/round89/harm-recheck.py --root $S --repo {LANE} --base-tool <base blob>` → `moved=0`.
(b) Wider: run `tools/gate-records.py` (the same blob at both revisions) over EVERY `GATE-RECORD` line in the whole lane
tree — `git -C {LANE} grep -n '^GATE-RECORD'` plus the same over `.ufo/waves/**`, `plans/` and `corpus/evidence/**` — and
list any record whose verdict differs from the `c1-positives.tsv` expectation.
(c) The two curated entries: `git -C {LANE} diff {BASE} {FREEZE} -- corpus/knowledge/` must be EMPTY; run
`curation-r89.py` on both revisions and confirm the two entries' leg verdicts are identical.
(d) Registry: `git -C {LANE} diff {BASE} {FREEZE} -- corpus/SOURCES.md` must be exactly two `used-by` cells; show the two
lines and confirm no other cell moved (`awk` cell-by-cell diff).
(e) Positive control: a deliberately broken record must still be refused, so the sweep can fail.
Write `R89ExecHarm.md` + `receipts/`."""),

    seat("R89ExecC1Forge", "executor", f"""
Forge C1 from a tree at `{FREEZE}` (`S={SCRATCH}/R89ExecC1Forge`). Find a counter state the frozen predicate ACCEPTS while
C1's sentence is false. Attack, at minimum:
(a) the cross-check: detach a printed field from its measurement in a way `DIV3` does not carry (e.g. forge
`FORGED_REFUSED` or `MUT_ADMIT_DERIVED` in the summary only); forge a leg detail *and* its `ok` coherently for a width
leg while leaving `DIV3` honest; forge `SUMMARY`'s own receipt.
(b) the per-format re-derivation: a detail that re-derives True but is not the measurement (e.g. `4/4/4 pin4` with the
pin constant moved); a leg whose detail is grammatically valid but names a different leg's numbers.
(c) `DERIVE_NEG`: make it pass while the subject tool DOES carry a usable literal (string concatenation that the mutant
builder still finds).
(d) the `TOOL` leg: make `ok` true while the tool path is a directory or a symlink to the base blob.
For every forgery state the expected refusal and whether the landed counter refused it. An accepted forgery is a finding
against C1's K2/K4. Write `R89ExecC1Forge.md` + `receipts/`."""),

    seat("R89ExecC2Forge", "executor", f"""
Forge C2 from a tree at `{FREEZE}` (`S={SCRATCH}/R89ExecC2Forge`), mirroring the tree the way
`curation-r89-controls.py` does. Find a tree shape the counter ACCEPTS where C2's sentence should refuse it. Attack:
(a) the duplicate guard: `Q1, Q1` with a second distinct qid (`Q1, Q1, Q3`); a duplicate expressed with different
whitespace or a trailing comma; a qid cited twice across two different decision rows.
(b) the field-derived verdict: make `fields_hold` true on a tree the *legs* refuse (or the reverse) — find any printed
field the verdict does not read.
(c) the superseder clause: a superseder whose date term reads in its capture but whose contrast phrase does not; two
superseders, one mined and one queued, where the queued one carries the bad cell.
(d) the token floor's boundary: the shortest verbatim quote that passes; a quote assembled from two non-adjacent
fragments; a curly-quote variant.
(e) the qid-set pin: restore the pinned set with a duplicate content row (the round-88 `caseG` restored shape) — does
the DUPQID leg see it?
An accepted forgery is a finding against C2's K2/K3. Write `R89ExecC2Forge.md` + `receipts/`."""),

    seat("R89MutBattery", "mutation-tester", f"""
Mutation-probe both round-89 counters (`S={SCRATCH}/R89MutBattery`, trees at `{FREEZE}` and `{BASE}`). Detector = each
counter's own frozen predicate.
(a) Add at least SIX new one-point mutations per counter beyond the committed 11 + 6. At least two must attack the
NAMED LIMITS in `claims.md` (the joint rewrite of writer+receipts+reconciliation; the coherent detail+ok forgery; the
`TOOL` non-numeric witness; the ≥7-token substitution; the quote-content swap) and say plainly whether each survives.
(b) Mutate the subject tool beyond the committed two: unreach using `http == "203"`; admit using `int(http) < 300`;
`git_blob` returning `b""`.
(c) For every SURVIVOR state the leg that should have killed it, whether that leg exists, and — if it exists — show it
failing on a probe tree.
A survivor is a coverage finding, not automatically a defect in the landed repair. Write `R89MutBattery.md` + `receipts/`."""),

    seat("R89ReviewerC1", "reviewer", f"""
Attack C1's stated wording against what the instrument enforces: `{LANE}/corpus/evidence/round89/claims.md` C1 against
`corpus/evidence/round89/gate-records-r89.py`. For each clause of the sentence and predicate say whether the instrument
enforces it, with the line or the run.
(a) `RECONCILED=16/16` — is the sixteenth leg (`SUMMARY`) load-bearing, or does the count recompute itself? Try removing
one receipt and one leg's `ok` separately.
(b) `CROSSCHECK=15/15` — which summary fields are compared, and which printed fields are NOT compared? Is any leg's
cross-check vacuous (compares a value to itself)?
(c) The three named limits: for each, build the counterexample the limit describes and confirm the limit's wording is
exactly right — no narrower, no wider.
(d) Confirm the round-88 field set is unchanged (the claim asserts it): diff the two counters' printed field names.
Write `R89ReviewerC1.md`. End with one `VERDICT:` line for C1."""),

    seat("R89ReviewerC2", "reviewer", f"""
Attack C2's wording against `corpus/evidence/round89/curation-r89.py`.
(a) "the verdict is computed from the printed fields" — list every leg and say whether `fields_hold` reads a value that
leg prints, a value it recomputes, or nothing. Find any leg whose failure `fields_hold` cannot see.
(b) The `DUPQID` guard — does it catch a duplicate on one row only, and does it catch `Q1, Q1, Q3`? Show the runs.
(c) The superseder clause — with `SUP_CLAUSE_CHECKED=0` on the real registry, what does the claim's sentence actually
guarantee, and is the sentence's phrasing exactly that? Compare against `plans/round-89.md` repair 4.
(d) The four named limits: build each counterexample and confirm the limit's wording.
Write `R89ReviewerC2.md`. End with one `VERDICT:` line for C2."""),

    seat("R89CriticClaims", "critic", f"""
Falsify both claims the way round 88's critic did (`S={SCRATCH}/R89CriticClaims`, trees at `{BASE}` and `{FREEZE}`).
(a) The do-nothing test: for each claim build the cheapest artifact that skips the claimed work and still prints the
frozen lines — an echo wrapper; a counter that runs the prior instrument and reprints its fields; a counter whose legs
are all constants with honest details. For each: would a scorer that reads stdout accept it, and what stops it?
(b) The claim-vs-instrument gap: for each claim clause, name the artefact that proves the clause is enforced; if a
clause has none, mark it `falsifies-wording` and name the narrow property the instrument does enforce.
(c) The prior-round survivors: confirm the four round-88 shapes (`E7b`, `E7c`, `E7d`, `E7f`) are now killed, and that
the pre-round-89 counter accepts each of them (the do-nothing evidence).
Write `R89CriticClaims.md`. End with `VERDICT:` lines for C1 and C2, and a per-clause table the falsification ledger can
read."""),

    seat("R89SentinelScope", "sentinel", f"""
Adversarial scope and safety review of the round's own artifacts; read-only outside your output folder.
(a) Egress: confirm zero fetches — every `refetch.tsv` row's `fetched_utc` (name the column as the file spells it) is
older than this round's freeze, and no `corpus/captures/` file is newer than `{FREEZE}`. Run the `awk` over the real
column and print a non-zero row count for the bound you chose.
(b) Control-receipt discipline (the round-88 F7 defect): read `corpus/evidence/round89/controls/expected.tsv` and every
receipt under `controls/receipts/`; report any row where the receipt's exit code or a `required_fields` token disagrees.
Re-run `bash corpus/evidence/round89/controls/run-controls.sh {LANE} <scratch>` and compare.
(c) Credential shape: grep the round's new files for token-, cookie-, `op://`- and session-shaped material; report
path:line shape only, never a value.
(d) Scope: `git -C {LANE} show --stat {FREEZE}` — does any path fall outside the lane or outside this round's declared
write scope? Check the fleet root `git -C /home/vgpnk/Projects/shokunin status --porcelain` for a lane-written stray.
(e) Attribution: the freeze commit's author and committer must be `chousa-shokunin <chousa@shokunin.local>`.
Write `R89SentinelScope.md` with one finding per item."""),

    seat("R89ScoutRegistry", "scout", f"""
Registry reconnaissance, read-only, at `{FREEZE}`.
(a) Re-derive the supersession graph: every `supersedes S0NN —` edge with both statuses; which have a non-mined
superseder; is any of them the disposal edge for the flagged row?
(b) Superseder-own-read population: how many superseding rows carry a contrast phrase AND a date term, and does each term
read in its own capture? Confirm or refute `SUP_CLAUSE_CHECKED=0` with your own script.
(c) The two `used-by` edits: show the exact old→new cells and confirm no other registry cell moved this round
(`git -C {LANE} diff {BASE} {FREEZE} -- corpus/SOURCES.md`).
(d) Campaign collision, read-only: if `/home/vgpnk/Projects/shokuknow/merge/chousa/SOURCES.append.md` exists, extract its
id set with the 0–3-space-tolerant pattern and compare to the lane registry; report the collision count and the id lists.
Emptiness is a result. Do not adopt, do not edit the campaign repo.
(e) Census: run `sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` and record the exit plus the
row count; confirm 218 → 218 with the same five pre-existing W04 warnings.
Write `R89ScoutRegistry.md` with counts, commands and the row lists."""),

    seat("R89ConnectorSiblings", "connector", f"""
Sibling-overlap scan (read-only; do not absorb anything, report it). Root `/home/vgpnk/Projects/shokunin`.
(a) Does any sibling lane already own leg-receipt reconciliation, field-derived verdicts, duplicate-qid guards, or a
supersession-clause check? Search `*/corpus/knowledge/*.md`, `*/corpus/lessons/*.md` and `*/tools/*.py` for the class
names (`reconcil`, `fields_hold`, `dup.*qid`, `supersed`), and report each hit with lane, path and line.
(b) Is the round's own instrument overlap a PROVINCE violation? Read `{LANE}/PROVINCE.md` and say whether the work is
inside "this lane's own corpus and gates" or drifts into another lane's ground.
(c) Name any contested scope the integrator should arbitrate, and any sibling whose next round should be told.
Write `R89ConnectorSiblings.md`. Nothing absorbed, nothing edited outside your folder."""),

    seat("R89ScribeLesson", "scribe", f"""
Draft the round-89 lesson from the committed receipts — you draft, the L1 integrates. Read
`corpus/evidence/round89/claims.md`, `plans/round-89.md`, the eight receipts under `corpus/evidence/round89/controls/`
and round 88's lesson for the shape.
Write `lesson-settlement-draft.md` in your folder with:
(a) `## Gate` — the sourced-claim records for S216 and S218: URL or repo path, access date, and a ≤25-word located quote
for each, formatted so `python3 -B tools/gate-records.py verify --root {LANE} --repo {LANE} <file>` can section it.
(b) `## Claim outcomes` — the two predicates with the fields the receipts print.
(c) `## Mistakes` — four rows in the class/evidence-pointer/captured-by/fix shape for THIS round's own errors: the
single-point healthy-tree mutant that proves nothing; the mirror id that collided with a real registry row (S099);
the summary field that reported 15/16 before the SUMMARY leg existed; the battery diagnostic that named a summary key
that does not exist. Each fix must be shown able to fail.
(d) `## Spot-check intake` — a table with one row per routed defect 1–8 of
`corpus/lessons/round-88-verifier-spotcheck.md`.
(e) `## Trends` — three rows (expansion, quality, discernment) with the evidence pointers you can verify from receipts.
Cite only paths and commands you personally ran or read. Write `lesson-settlement-draft.md` + `receipts/`."""),
]

if __name__ == "__main__":
    spec = {"wave": "chousa-r89-w1", "reportDir": ".ufo/waves/round-89/w1", "context": CONTEXT, "items": ITEMS}
    out = os.path.join(HERE, "w1-spec.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(spec, fh, indent=1)
    print(f"wrote {out} items={len(ITEMS)} roles={sorted({i['role'] for i in ITEMS})}")
