#!/usr/bin/env python3
"""Build the round-88 wave-1 spec (12 seats, policy v1 band 8-16). Run from anywhere; writes w1-spec.json beside itself."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
SCRATCH = "/fast/scratch/hyaku/chousa-r88"
BASE = "f484d94f"
FREEZE = "4ea9d008abfd2e09cb51649a42678a78f52ac530"

GODSPEED = """/skill:godspeed

You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.
"""

CONTEXT = f"""Lane chousa round 88, L1 ChousaR88 holds the canonical planner seat, the freeze and the integration. Root {LANE}.
Revisions: base {BASE} (round-87 landing + its non-author spot-check); claim freeze {FREEZE}; landed bytes you
attack {FREEZE} (the freeze commit carries the counters themselves — there is no separate landing commit this round
beyond the freeze, so build your trees at {FREEZE}).
Frozen predicate set: {LANE}/corpus/evidence/round88/claims.md — read it FIRST, with every kill rule — and
{LANE}/plans/round-88.md for the pre-freeze repairs. The subject tool `tools/gate-records.py` is UNCHANGED this
round (the round-87 unreach repair stands). Two claims. C1 operability: the successor battery
(`corpus/evidence/round88/gate-records-r88.py`) binds the 203 class to `http == "203"` in both independent
derivations, pins the width against a third derivation plus `ROWS_203 = 3`, and accounts its verdict by re-reading
each leg's own receipt file and reconciling each detail string against its value, printing `D1_EXPECTED=3
D1_FORGES=3 D1_REFUSED=3/3 D2_FORGES=3 D2_REFUSED=3/3 MUT_ADMIT_KILLED=1 MUT_UNREACH_KILLED=1 DERIVE_NEG=1
LEG_REREAD=15/15 RECONCILED=15/15 LEGS_APPENDED=15`. C2 calibration: `curation-r88.py` adds an every-qid warrant
leg, a per-entry qid-set pin plus a per-row token floor (`MIN_TOKENS = 7`, the measured minimum over the 20 located
base quotes), and a `mined`-superseder disposal, printing `SUPERSEDED_LIVE=0 UNENTAILED_TERM=0 MODIFIED_DEF_CITED=1
QUOTES_LOCATED=20/20 WARRANT_OK=17/17 TEACHES_FLAGGED=1 TEACHES_UNRESOLVED=0 LEGS=7/7` and refusing all five
round-87 forgeries. The freeze commit also carries one entry repair: `corpus/knowledge/provenance-recording-r85.md`
row "Naming what a resource derives from" now names `Q1 (S215)` instead of `Q1, Q3 (S215)` (Q3's quote shares no
term with the row). Ground sources: S216 (RFC 9110 203) and S218 (own-work, QUALITY 178), both through the
round-87 claims file.

Every `Report:` trailer path is relative to {LANE} — write it at {LANE}/<that path>.

Leaf only: no task tool, no subagents, no agent://all, no production edits, no lane or fleet git/jj mutation, no commits
or pushes, no edits to /home/vgpnk/Projects/shokunin/scripts, /home/vgpnk/Projects/shokunin/.ufo/state, MANIFEST.json,
considerthese/ or any sibling repo. The only files you write are under your own output folder
{LANE}/.ufo/waves/round-88/w1/<seat>/ plus your scratch dir. Network: none this round — every check reads committed
bytes (a GET is a finding). Never mutate a host sysctl, never run sudo, never restart a host service.

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
    seat("R88ExecRepro", "executor", f"""
Reproduce both frozen claims from a clean tree. Build `S={SCRATCH}/R88ExecRepro` and `git -C {LANE} archive {FREEZE} | tar -x -C $S`.
(a) Run `python3 -B $S/corpus/evidence/round88/gate-records-r88.py --root $S --repo {LANE} --work $S` and record the whole
line plus exit. Re-derive every field from the tree independently where you can: the D1/D2 class width (count the rows in
`$S/corpus/evidence/round57/refetch.tsv` with `http_code == "203"`), `FORGED_REFUSED` against the generated total, the
leg receipts under `$S/legs/` and their reconciliation.
(b) Run `python3 -B $S/corpus/evidence/round88/curation-r88.py --root $S` and independently re-derive `QUOTES_LOCATED`,
the per-entry qid sets, the token floor minimum (count the words of each of the 20 located quotes and find the minimum),
`WARRANT_OK` (pick 5 of the 17 decision rows and re-check the qid→quote→term chain by hand) and the one `TEACHES_FLAGGED` row.
(c) Confirm the instrument bytes equal `$S/corpus/evidence/round88/instrument-pins.txt` for every pinned path, and that
`$S/tools/gate-records.py` is the landed blob.
(d) Run `python3 -B $S/corpus/evidence/round88/curation-r88-controls.py --root $S --work $S` and
`python3 -B $S/corpus/evidence/round88/mutate-r88.py --root $S --repo {LANE} --work $S`.
Report every deviation as a finding with its receipt. Write `R88ExecRepro.md` + `receipts/`."""),

    seat("R88ExecHarm", "executor", f"""
Harm sweep for C1's K3, wider than the round's own. Build `S={SCRATCH}/R88ExecHarm` with
`git -C {LANE} archive {FREEZE} | tar -x -C $S` and a second tree at the base `{BASE}`.
(a) Run `python3 -B $S/corpus/evidence/round88/harm-recheck.py --root $S --repo {LANE} --base-tool <base gate-records.py>`
and confirm `moved=0`.
(b) Go wider: run the base tool and the `tools/gate-records.py` at {FREEZE} over every committed `GATE-RECORD` line in
the whole lane tree (`git -C {LANE} grep -n '^GATE-RECORD'` and the same over `.ufo/waves/**` and `plans/`), file-per-line,
and list any record whose verdict differs.
(c) Positive control: confirm a *deliberately broken* unreach record is refused by both, so the sweep can fail.
(d) The provenance entry repair: `git -C {LANE} diff {BASE} {FREEZE} -- corpus/knowledge/provenance-recording-r85.md`
must be exactly the one-cell warrant change; confirm no other entry cell moved.
Write `R88ExecHarm.md` + `receipts/`."""),

    seat("R88ExecForge", "executor", f"""
Forge the C1 battery from a tree at `{FREEZE}` (`S={SCRATCH}/R88ExecForge`). Your job is to find an in-class forged
record the frozen predicate accepts. Attack, at minimum:
(a) the two 203 classes: a `D1` admit whose quote is the first quotable line of a 203 capture; a `D2` reject whose
`http` is 200 with `curl_rc` non-zero; a `D2` reject on a 203 row whose `fetched` is a *different* attempt;
(b) the width pin: a *new* committed refetch row with `http=203` for a different S-id — does the third derivation move;
(c) the escape hatches: BOM/zero-width prefix, indented record, record inside a fence, duplicate `GATE-RECORD` line;
(d) the `url/unreach` grammar: `curl_rc=0 http=299`, `curl_rc=0 http=300`, `curl_rc=1 http=203`.
For every forgery, name the code you expect and whether the landed tool refused it with exactly that code. A forgery
the tool ACCEPTS is a finding against C1's K2. Write `R88ExecForge.md` + `receipts/`."""),

    seat("R88ExecC2Forge", "executor", f"""
Forge the C2 curation counter from a tree at `{FREEZE}` (`S={SCRATCH}/R88ExecC2Forge`). Find a tree shape the frozen
predicate accepts that C2's sentence should refuse. Attack, at minimum:
(a) the qid-set pin: rename Q10→Q99 and add a new row Q10 carrying a different verbatim quote (set restored, content
changed); reorder the qid rows; delete Q10 and add Q14 duplicate (the restored caseG shape);
(b) the token floor: replace a real quote with a verbatim 7-word quote and one with a verbatim 8-word quote;
(c) the warrant leg: a row naming a qid whose quote shares a *stopword-length* word; a row naming the same qid twice;
(d) the teaches leg: a flagged row disposed by a superseder whose `status` is `queued`; a superseding row that carries
its own contrast+term absent from its capture.
Mirror the tree the way `curation-r88-controls.py` does; never write in the lane. A forgery ACCEPTED is a finding
against C2's K3/K4. Write `R88ExecC2Forge.md` + `receipts/`."""),

    seat("R88MutCounter", "mutation-tester", f"""
Mutation-probe both round-88 counters and the subject tool (`S={SCRATCH}/R88MutCounter`, trees at `{FREEZE}` and
`{BASE}`). Your assigned detector is each counter's own frozen predicate: a mutant is killed only when the predicate
stops reporting `PASS`.
(a) Extend `corpus/evidence/round88/mutate-r88.py`'s shapes with at least six NEW one-point mutations of each counter
beyond the six already in that file, including at least one that attacks the named limit in `claims.md` C1 (a counter
edit that jointly rewrites the leg writer, the receipts and the reconciliation — state plainly whether it survives).
(b) Mutate the subject tool beyond the two shapes already in the file: make the unreach branch use `http == "203"`;
make the admit branch accept `int(http) < 300`; make `git_blob` return `b""`.
(c) For every SURVIVOR, state the leg that should have killed it and whether that leg exists; if it exists, show it
failing on a probe tree.
Write `R88MutCounter.md` + `receipts/`. A survivor is a coverage finding, not a defect in the landed repair."""),

    seat("R88ReviewerC1", "reviewer", f"""
Attack C1's stated wording against what the instrument enforces, reading
`{LANE}/corpus/evidence/round88/claims.md` C1 as the claim and `corpus/evidence/round88/gate-records-r88.py` as the
instrument. For each clause of the sentence and predicate, say whether the instrument enforces it and show the line or
the run. Specifically test:
(a) "every committed refetch row with `http` exactly 203 in both derivations" — re-derive the width by hand from
`corpus/evidence/round57/refetch.tsv`; do the two derivations agree, and is `ROWS_203 = 3` the right constant?
(b) "re-reading each leg's own receipt and reconciling the detail": is `LEG_REREAD`/`RECONCILED` load-bearing? Build
the round-87 E4 shape (a leg that keeps its append and detaches its `ok`) and report the verdict with its receipt.
(c) the named limit: is it stated at its true width?
Write `R88ReviewerC1.md`. End with one `VERDICT:` line for C1."""),

    seat("R88ReviewerC2", "reviewer", f"""
Attack C2's stated wording against `corpus/evidence/round88/curation-r88.py`. Specifically:
(a) "every named qid shares a distinctive content word" — re-derive the 17/17 from the tree; find any row whose only
shared word is incidental, and decide whether the claim's sentence promises more.
(b) the provenance repair: does the row "Naming what a resource derives from" still state what `Q1` states, and does
dropping `Q3` narrow the entry's taught content in a way the counter cannot see? Read the entry's `## Limits` and
`## Inference` sections for the sentence the removed warrant carried.
(c) "a superseder disposes only when `mined`" — does the tree have a flagged row whose only superseder is `queued`?
show the run.
Write `R88ReviewerC2.md`. End with one `VERDICT:` line for C2."""),

    seat("R88CriticClaims", "critic", f"""
Falsify the claims the way round 87's critic did. Build trees at `{BASE}` and `{FREEZE}` in
`{SCRATCH}/R88CriticClaims`.
(a) The do-nothing test: for each claim, build the cheapest instrument that skips the claimed work and still prints the
frozen line — a wrapper that echoes the predicate line and exits 0; a counter that runs the *base* tool but hard-codes
the new fields; a counter whose legs all report ok from constants. State for each whether the frozen predicate would
accept it and what stops it.
(b) The reconciliation re-test: build the round-87 E7 shape (every list leg tautologised) and the E4 shape against the
round-88 battery and report each verdict with its receipt.
(c) The do-nothing C2 test: run the round-87 counter against the round-88 tree and confirm it prints `CURATION_R87=PASS`.
Write `R88CriticClaims.md`. End with `VERDICT:` lines for C1 and C2."""),

    seat("R88SentinelScope", "sentinel", f"""
Adversarial scope and safety review of the round's own artifacts; read-only outside your output folder.
(a) Egress: this round fetches nothing. Confirm it: list every `refetch.tsv` row with `fetched >= 2026-11-08T07:00:00Z`
and confirm none exists, and confirm no `corpus/captures/` file is newer than the freeze commit.
(b) Credential shape: grep the round's new files (`plans/round-88.md`, `corpus/evidence/round88/**`,
`corpus/knowledge/provenance-recording-r85.md` diff) for token-, cookie-, `op://`- and session-shaped material; report
only path:line shape, never a value.
(c) Scope: does any new file in this round write outside `{LANE}`? Check `git -C {LANE} show --stat {FREEZE}` and the
fleet root `git -C /home/vgpnk/Projects/shokunin status --porcelain` for a lane-written stray.
(d) Scratch and host: grep the round's committed tools (`corpus/evidence/round88/*.py`) for hardcoded `/tmp`; confirm
nothing touches a host sysctl, `sudo`, or a service.
(e) Attribution: confirm the freeze commit's author and committer are `chousa-shokunin <chousa@shokunin.local>`.
Write `R88SentinelScope.md` with one finding per item."""),

    seat("R88ScoutRegistry", "scout", f"""
Registry reconnaissance for C2's `teaches` leg (no edits; read committed bytes at `{FREEZE}`).
(a) Re-derive the supersession graph: print every `supersedes S0NN —` edge with both statuses; which edges have a
non-mined superseder, and is any of them the disposal edge for the one flagged row?
(b) Measure the superseding row's own read: which superseding rows carry a contrast phrase and a date term, and does
each term read in its own capture? Show the command and the counts.
(c) Check the qid-set pin against the registry: is the pinned set for each routed entry exactly the set of qids the
entry carries at {FREEZE}? Check the token floor against the 20 located quotes.
(d) Collision check against the campaign package: run the census extractor over the lane registry and, read-only, over
`/home/vgpnk/Projects/shokuknow/merge/chousa/SOURCES.append.md` if it exists; report the id sets and any collision.
Whether `merge/chousa/` was assimilated this round is the L1's call — report only the measured collision count.
Write `R88ScoutRegistry.md` with counts, commands and the row lists."""),

    seat("R88ConnectorSiblings", "connector", f"""
Sibling-overlap scan (read-only; do not absorb anything, report it). Root `/home/vgpnk/Projects/shokunin`.
(a) Does any sibling lane already own HTTP status-semantics or record-schema ground (the 203 class, the
success-vs-failure record form, a leg-receipt reconciliation)? Search `*/corpus/knowledge/*.md`, `*/PROVINCE.md` and
`*/corpus/SOURCES.md` for `203`, `Non-Authoritative`, `status code`, `unreach`, `REFETCH`, `leg receipt`, `reconcile`
and report every hit with its lane and whether it conflicts with chousa's claim.
(b) Does any sibling hold quote-floor / warrant-linkage / registry-supersession machinery? Report the lane, path and
one-line description; name any stricter than chousa's.
(c) The cross-lane defect round 86 routed (kotodama's `check-gate-captures.py` false-green): is it still open? Read-only
check, one command, report the observed state.
(d) Report contested scope per PROVINCE.md rules — an adjacency finding, nothing absorbed.
Write `R88ConnectorSiblings.md`."""),

    seat("R88ScribeLesson", "scribe", f"""
Draft the round-88 lesson's settlement sections from committed evidence — prose only, no code, no edits outside your
folder. Read `{LANE}/corpus/evidence/round88/claims.md`, `plans/round-88.md`, the existing
`corpus/lessons/round-88.md` if present (the L1's draft), `corpus/QUALITY.md` 182–189 and `.ufo/waves/round-88/w1/*.md`
as they land.
(a) Check whether the lesson must carry a `## Gate` block: what GATE-RECORD lines does this round owe (the rows it
opened or repaired), and does the provenance repair row's `Q1` quote re-open verbatim? Run
`python3 -B tools/quote-reopen.py verify --items <tsv>` if the lesson cites a web quote.
(b) Check `## Mistakes` items if present: each must have class · evidence pointer · captured-by · fix, and each fix
must name a check that can fail.
(c) Draft the settlement paragraph the L1 will paste after WAVE-DONE: which seats fired, which held, and one sentence
per fired claim with the seat and receipt path. Mark it clearly as a DRAFT with the seat names it read.
Write `R88ScribeLesson.md` (and `lesson-settlement-draft.md` for (c))."""),
]

SPEC = {
    "wave": "chousa-r88-w1",
    "reportDir": ".ufo/waves/round-88/w1",
    "context": CONTEXT,
    "items": ITEMS,
}

if __name__ == "__main__":
    out = os.path.join(HERE, "w1-spec.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(SPEC, fh, indent=1)
    print(f"wrote {out} seats={len(ITEMS)}")
