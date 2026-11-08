#!/usr/bin/env python3
"""Build the round-87 wave-1 spec (13 seats, policy v1 band 8-16). Run from anywhere; writes w1-spec.json beside itself."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
SCRATCH = "/fast/scratch/hyaku/chousa-r87"
BASE = "6495ef88"
EGRESS = "b7db07140791ab071de49743687e6d330edabc2e"
FREEZE = "c033577b4fb840553f3e10e40aa77c724abe0bca"
LANDING = "e6e920a4e6988287c31e89b3e920a118b569ae52"

GODSPEED = """/skill:godspeed

You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.
"""

CONTEXT = f"""Lane chousa round 87, L1 ChousaR87 holds the canonical planner seat, the freeze and the integration. Root {LANE}.
Revisions: base {BASE} (round-86 landing + its non-author spot-check); egress table {EGRESS} (committed before the first
fetch); claim freeze {FREEZE}; landed bytes you attack {LANDING}.
Frozen predicate set: {LANE}/corpus/evidence/round87/claims.md — read it FIRST, with every kill rule — and
{LANE}/plans/round-87.md for the pre-freeze repairs. Two claims. C1 operability: the successor battery
(`corpus/evidence/round87/gate-records-r87.py`) makes the 203 class every qualifying committed refetch row (3), adds the
reject-form 203 class, and accounts its verdict by counting executed legs, printing `D1_EXPECTED=3 D1_FORGES=3
D1_REFUSED=3/3 D2_FORGES=3 D2_REFUSED=3/3 MUT_ADMIT_KILLED=1 MUT_UNREACH_KILLED=1 DERIVE_NEG=1 LEGS=15/15`; the subject
tool `tools/gate-records.py` gains the unreach repair (any 2xx is a successful response, never a failed transfer).
C2 calibration: `curation-r87.py` adds per-entry located-quote floors (13 and 7), a warrant-linkage leg over 17 decision
rows, and a registry-`teaches`-against-own-capture leg, printing `SUPERSEDED_LIVE=0 UNENTAILED_TERM=0
MODIFIED_DEF_CITED=1 QUOTES_LOCATED=20/20 WARRANT_OK=17/17 TEACHES_FLAGGED=1 TEACHES_UNRESOLVED=0 LEGS=7/7`.
Ground source this round: S216 (RFC 9110 203, re-opened) and S218 (own-work, new).

Every `Report:` trailer path is relative to {LANE} — write it at {LANE}/<that path>.

Leaf only: no task tool, no subagents, no agent://all, no production edits, no lane or fleet git/jj mutation, no commits
or pushes, no edits to /home/vgpnk/Projects/shokunin/scripts, /home/vgpnk/Projects/shokunin/.ufo/state, MANIFEST.json,
considerthese/ or any sibling repo. The only files you write are under your own output folder
{LANE}/.ufo/waves/round-87/w1/<seat>/ plus your scratch dir. Network: none this round — every check reads committed
bytes (a GET is a finding; the round's one fetch is already committed under corpus/captures/). Never mutate a host
sysctl, never run sudo, never restart a host service.

Scratch: every clone, archive tree, work dir and fixture lives under {SCRATCH}/<your seat name>/; create it with
`mkdir -p`, pass it explicitly (`--work`, `TMPDIR=`), delete it before you yield (`trap 'rm -rf -- "$S"' EXIT` in shell,
`finally: shutil.rmtree` in Python), and copy every receipt you cite into your wave output folder first. Never write
under /tmp. Build a tree at a revision with `git -C {LANE} archive <rev> | tar -x -C <scratch dir>`; any fixture git
repo is `D=$(mktemp -d -p {SCRATCH}/<seat>) && test -n "$D" && git -C "$D" init -q`, every later git call names `-C
"$D"`, and you assert `git -C "$D" rev-parse --show-toplevel` equals `$D` before any mutating git command.

Counter that binds you: every finding names the exact command, the receipt path you wrote and the observed line plus
exit code. An unrun check has not passed; a deviation from an expected value is a finding, never something to hide.
End your report with one line `VERDICT: <seat> <C1|C2> fired|held|n/a — <one sentence>` per claim you touched (plain
text, not JSON).

Tooling authorization (operator, 2026-10-19): you may install or upgrade tools that help the task; read
/home/vgpnk/.omp/agent/RULES.md first (official channels only; record tool/version/channel/reason in your report).
pacman guard (orchestrator ruling 2026-10-20): all pacman transactions are PAUSED host-wide — install via `uv tool`/
`npx`/an official binary in ~/.local/bin, or not at all; never `pacman -Sy`, `-Syu`, `-U`, `-R`, never downgrade.
"""


def seat(name, role, body):
    return {"name": name, "role": role, "prompt": GODSPEED + "\n" + body.strip() + "\n"}


ITEMS = [
    seat("R87ExecRepro", "executor", f"""
Reproduce both frozen claims from a clean tree. Build `S={SCRATCH}/R87ExecRepro` and `git -C {LANE} archive {LANDING} | tar -x -C $S`.
(a) Run `python3 -B $S/corpus/evidence/round87/gate-records-r87.py --root $S --repo {LANE} --work $S` and record the whole
line plus exit. Re-derive every field from the tree independently where you can: the D1/D2 class width (count the rows in
`$S/corpus/evidence/round57/refetch.tsv` that qualify), `FORGED_REFUSED` against the generated total, and `LEGS`.
(b) Run `python3 -B $S/corpus/evidence/round87/curation-r87.py --root $S` and independently re-derive `QUOTES_LOCATED`,
the two per-entry floors, `WARRANT_OK` (pick 5 of the 17 decision rows and re-check the qid→quote→term chain by hand) and
the one `TEACHES_FLAGGED` row.
(c) Confirm the instrument bytes equal `$S/corpus/evidence/round87/instrument-pins.txt` for every pinned path, and that
`$S/tools/gate-records.py` is the landed blob.
(d) Run `python3 -B $S/corpus/evidence/round87/curation-r87-controls.py --root $S --work $S` and
`python3 -B $S/corpus/evidence/round87/mutate-r87.py --root $S --repo {LANE} --work $S`.
Report every deviation as a finding with its receipt. Write `R87ExecRepro.md` + `receipts/`."""),

    seat("R87ExecHarm", "executor", f"""
Harm sweep for C1's K3, wider than the round's own. Build `S={SCRATCH}/R87ExecHarm` with
`git -C {LANE} archive {LANDING} | tar -x -C $S` and a second tree at the base `{BASE}`.
(a) Run `python3 -B $S/corpus/evidence/round87/harm-recheck.py --root $S --repo {LANE} --base-tool <base gate-records.py>`
and confirm `moved=0`.
(b) Go wider than the lessons: sweep every committed `GATE-RECORD` line in the whole lane tree (`git -C {LANE} grep -n
'^GATE-RECORD'` and the same over `.ufo/waves/**` committed evidence and `plans/`), run the base tool and the landed tool
over a file per line, and list any record whose verdict differs.
(c) Positive control: confirm a *deliberately broken* unreach record (`decision=reject capture=none curl_rc=0 http=404`
with a refetch row that says 200) is refused by both, so the sweep can fail.
(d) Check the unreach repair cannot be satisfied by a 3xx/4xx being called success: probe `http=301` and `http=418`
records against a matching committed row, or state that no such row exists and show the sweep.
Write `R87ExecHarm.md` + `receipts/`."""),

    seat("R87ExecForge", "executor", f"""
Forge the C1 battery from a tree at `{LANDING}` (`S={SCRATCH}/R87ExecForge`). Your job is to find an in-class forged
record the frozen predicate accepts. Attack, at minimum:
(a) the two 203 classes: a `D1` admit whose quote is one long line of the 203 capture; a `D2` reject whose `http` is 200
with `curl_rc` non-zero; a `D2` reject on a 203 row whose `fetched` is a *different* attempt of the same row;
(b) the tier/tier-flip, the `capture_sha256` prefix and the `rev`/`path` forms on the 203 rows;
(c) the escape hatches: a record with a BOM or zero-width prefix, an indented record, a record inside a fence, a duplicate
`GATE-RECORD` line for one S-id;
(d) the `url/unreach` grammar: `curl_rc=0 http=299`, `curl_rc=0 http=300`, `curl_rc=1 http=203` and the same with the
matching refetch row.
For every forgery you build, name the code you expect and whether the landed tool refused it with exactly that code.
A forgery the tool ACCEPTS is a finding against C1's K2. Write `R87ExecForge.md` + `receipts/`."""),

    seat("R87ExecC2Forge", "executor", f"""
Forge the C2 curation counter from a tree at `{LANDING}` (`S={SCRATCH}/R87ExecC2Forge`). Find a tree shape the frozen
predicate accepts that C2's sentence should refuse. Attack, at minimum:
(a) the floors: add a junk quote row (a 1-word quote that IS verbatim in its capture) to each entry to restore the count
after deleting a real row; and truncate a real row's quote to a verbatim prefix;
(b) the warrant leg: name the same qid twice; name a qid whose quote shares a *stopword*-length word with the row;
repoint a warrant to a quote from a different S-id but the same entry;
(c) the teaches leg: a row whose `teaches` carries a contrast phrase and a date term that IS in its capture (the leg
should pass — confirm it does not over-fire); and a NOT-yet-superseded row with a contrast+term absent from its capture
(the leg should fire — confirm);
(d) the supersession leg: a supersession edge whose superseding row is `rejected`.
Mirror the tree the way `curation-r87-controls.py` does (real copies of `SOURCES.md` and the two entries, symlinks for
`captures` and `evidence/round57`); never write in the lane. A forgery ACCEPTED is a finding against C2's K3/K4.
Write `R87ExecC2Forge.md` + `receipts/`."""),

    seat("R87MutCounter", "mutation-tester", f"""
Mutation-probe both round-87 counters and the repaired subject tool (`S={SCRATCH}/R87MutCounter`, trees at `{LANDING}`
and `{BASE}`). Your assigned detector is each counter's own frozen predicate: a mutant is killed only when the predicate
stops reporting `PASS` or the field set deviates.
(a) Extend `corpus/evidence/round87/mutate-r87.py`'s shapes with at least six NEW one-point mutations of each counter
beyond the seven already in that file, including at least one that attacks the named limit in `claims.md` C1 (a leg that
keeps its append but misreports its value — e.g. `setup_ok = 1`, `d1_refused = len(d1)`, `f_pok = len(pos)`).
(b) Mutate the subject tool beyond the two shapes already in the file: make the unreach branch use `http == "203"`; make
the admit branch accept `int(http) < 300`; delete the calendar check; make `git_blob` return `b""`.
(c) For every SURVIVOR, state the leg that should have killed it and whether that leg exists; if it exists, show it
failing on a probe tree.
Write `R87MutCounter.md` + `receipts/`. A survivor is a coverage finding, not a defect in the landed repair."""),

    seat("R87ReviewerC1", "reviewer", f"""
Attack C1's stated wording against what the instrument enforces, reading
`{LANE}/corpus/evidence/round87/claims.md` C1 as the claim and `corpus/evidence/round87/gate-records-r87.py` as the
instrument. For each clause of the sentence and predicate, say whether the instrument enforces it and show the line or the
run. Specifically test:
(a) "every qualifying committed refetch row" — what is "qualifying"? Is the builder's predicate the same as
`count_203_rows`'? Construct a committed-bytes case where they would disagree (or prove they cannot).
(b) "accounts its verdict by counting executed legs" — is `LEGS=15/15` load-bearing or decorative? Try a counter edit
that keeps all 15 appends and still passes with a broken duty.
(c) the named limit: is it stated at its true width?
(d) the `MEASURED but not enforced` class: list every printed field that is NOT in `passed`/legs.
Write `R87ReviewerC1.md`. End with one `VERDICT:` line for C1."""),

    seat("R87ReviewerC2", "reviewer", f"""
Attack C2's stated wording against `corpus/evidence/round87/curation-r87.py`. Specifically:
(a) "a per-entry located-quote floor (13 and 7, the measured base counts)" — re-derive both counts from `{LANDING}` and
check they are counts of *rows* and not of distinct quotes.
(b) "a warrant-linkage leg requiring each decision-table row's named qid to resolve to a located quote that shares a
distinctive content word" — build the cheapest row that satisfies the leg while its Do/Never is unentailed by the quote
(e.g. a row whose only shared word is incidental), and decide whether the claim's sentence promises more than that.
(c) the `TEACHES` leg: does "requires every flagged row to be disposed as superseded" hold when a flagged row is
superseded by a `rejected` row? Show the run.
(d) `UNENTAILED_TERM` is still a two-word substring test over two entries — does the claim overstate its width?
Write `R87ReviewerC2.md`. End with one `VERDICT:` line for C2."""),

    seat("R87CriticClaims", "critic", f"""
Falsify the claims the way round 86's critic did. Build trees at `{BASE}` and `{LANDING}` in
`{SCRATCH}/R87CriticClaims`.
(a) The do-nothing test: for each claim, build the cheapest instrument that skips the claimed work and still prints the
frozen line — a wrapper that echoes the predicate line and exits 0; a counter that runs the *base* tool but hard-codes the
new fields; a counter whose legs all report ok from constants. State for each whether the frozen predicate would accept it
and what stops it.
(b) The T4-family re-test: re-run the round-86 critic's `T4` (`r[6] == "200" if sid == "S021" else 2xx`) against the
landed battery and confirm `D1_WIDTH`/`D2_WIDTH` kill it; then build the two-row narrowing (`sid in ("S021","S032")`) and
the zero-record class (`_qualifying_203` returns []) and report each verdict.
(c) The `M2`/`M5` re-test against the landed accounting, including the two-point variant (stub the fields AND the
derived flags) — that one is expected to survive; say so plainly and check whether C1's named limit covers it at its true
width.
(d) C2: re-run the four routed forgeries and add the `2/2`-with-junk-rows shape from the round-86 E5c2 finding.
Write `R87CriticClaims.md`. End with `VERDICT:` lines for C1 and C2."""),

    seat("R87SentinelScope", "sentinel", f"""
Adversarial scope and safety review of the round's own artifacts; read-only outside your output folder.
(a) Egress: the approval table is `corpus/evidence/round87/egress-approval.md` (commit `{EGRESS}`). Compare its
intended-targets URL set with every `refetch.tsv` row whose `fetched` is `>= 2026-11-08T06:40:00Z`, and with every
`corpus/captures/` file whose mtime is after the egress commit. Name any URL fetched outside the table.
(b) Credential shape: grep the round's new files (`plans/round-87.md`, `corpus/evidence/round87/**`,
`corpus/lessons/round-87.md`, the LOG/SCORECARD/QUALITY/README additions) for token-, cookie-, `op://`- and
session-shaped material; report only path:line shape, never a value.
(c) Scope: does any new file in this round write outside `{LANE}`? Check `git -C {LANE} show --stat {LANDING}` and the
fleet root `git -C /home/vgpnk/Projects/shokunin status --porcelain` for a lane-written stray.
(d) Scratch and host: grep the round's committed tools (`corpus/evidence/round87/*.py`) for hardcoded `/tmp`; confirm
nothing touches a host sysctl, `sudo`, or a service.
(e) Attribution: confirm the landing commit's author and committer are `chousa-shokunin <chousa@shokunin.local>`.
Write `R87SentinelScope.md` with one finding per item."""),

    seat("R87ScoutRegistry", "scout", f"""
Registry reconnaissance for C2's `teaches` leg (no edits; read committed bytes at `{LANDING}`).
(a) Re-derive the teaches-rule population over all 218 rows: how many rows carry a contrast phrase; how many carry a
contrast phrase AND a date term; which are flagged; which are superseded. Show the command and the counts.
(b) Measure over-fire and under-fire for a wider vocabulary: add `rather than`, `not the same as`, `other date
properties` and re-count; report every row that newly flags and whether its capture supports the flag.
(c) Check the supersession graph for chains and cycles: print every `supersedes S0NN —` edge, find chains of length > 1,
and any edge whose target row does not exist. Does the leg's disposition rule handle a chain correctly?
(d) Collision check against the campaign package: run the census extractor over the lane registry and, read-only, over
`/home/vgpnk/Projects/shokuknow/merge/chousa/SOURCES.append.md` if it exists; report the id sets and any collision. Never
write in the shokuknow tree.
Write `R87ScoutRegistry.md` with counts, commands and the row lists."""),

    seat("R87ConnectorSiblings", "connector", f"""
Sibling-overlap scan (read-only; do not absorb anything, report it). Root `/home/vgpnk/Projects/shokunin`.
(a) Does any sibling lane already own HTTP status-semantics or record-schema ground (the 203 class, the
success-vs-failure record form)? Search `*/corpus/knowledge/*.md`, `*/PROVINCE.md` and `*/corpus/SOURCES.md` for
`203`, `Non-Authoritative`, `status code`, `unreach`, `REFETCH` and report every hit with its lane and whether it is a
conflict with chousa's claim.
(b) Does any sibling hold quote-floor / warrant-linkage / registry-supersession machinery (a counter with a denominator
floor, a warrant leg)? Report the lane, path and one-line description; name any that is stricter than chousa's.
(c) The cross-lane defect round 86 routed (kotodama's `check-gate-captures.py` false-green): is it still open? Read-only
check, one command, report the observed state.
(d) Report contested scope per PROVINCE.md rules — an adjacency finding, nothing absorbed.
Write `R87ConnectorSiblings.md`."""),

    seat("R87ScribeLesson", "scribe", f"""
Draft the round-87 lesson's settlement sections from committed evidence — prose only, no code, no edits outside your
folder. Read `{LANE}/corpus/evidence/round87/claims.md`, `plans/round-87.md`, the existing
`corpus/lessons/round-87.md` (the L1's draft), `corpus/QUALITY.md` 182–186 and `.ufo/waves/round-87/w1/*.md` as they
land.
(a) Check the `## Gate` block against `python3 tools/gate-records.py verify --root . --repo . corpus/lessons/round-87.md`
and against the registry rows (S216 `used-by`, S218 row) — every claim in the block must match the committed bytes.
(b) Check `## Mistakes` items 1–4: each must have class · evidence pointer · captured-by · fix, and each fix must name a
check that can fail (QUALITY's rule). Name any item whose fix is asserted rather than shown.
(c) Check `## Spot-check intake` covers all eight items of round 86's routed-defect and conformance list, one row each.
(d) Draft the settlement paragraph the L1 will paste after WAVE-DONE: which seats fired, which held, and one sentence per
fired claim with the seat and receipt path. Mark it clearly as a DRAFT with the seat names it read.
Write `R87ScribeLesson.md` (and `lesson-settlement-draft.md` for (d))."""),
]

SPEC = {
    "wave": "chousa-r87-w1",
    "reportDir": ".ufo/waves/round-87/w1",
    "context": CONTEXT,
    "items": ITEMS,
}

if __name__ == "__main__":
    out = os.path.join(HERE, "w1-spec.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(SPEC, fh, indent=1)
    print(f"wrote {out} seats={len(ITEMS)}")
