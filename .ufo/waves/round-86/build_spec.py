#!/usr/bin/env python3
"""Build the round-86 wave-1 spec (12 seats, policy v1 band 8-16). Run from anywhere; writes w1-spec.json beside itself."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
SCRATCH = "/fast/scratch/hyaku/chousa-r86"
BASE = "3bfb6885958ad4a674ad1896f70d1e836be609e4"
EGRESS = "e446875260a11e3489a0d78344d71d7fbb006a42"
FREEZE = "d0b1bd06872cdf0eeb03eccd099ff69ae6704307"
LANDING = "667a5d091dc46168ed95eda0ae7f19a9bcf139a2"

GODSPEED = """/skill:godspeed

You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.
"""

CONTEXT = f"""Lane chousa round 86, L1 ChousaR86 holds the canonical planner seat, the freeze and the integration. Root {LANE}.
Revisions: base {BASE} (round-85 tip + non-author spot-check); egress table {EGRESS} (committed before any fetch);
claim freeze {FREEZE}; landed bytes you attack {LANDING}.
Frozen predicate set: {LANE}/corpus/evidence/round86/claims.md — read it FIRST, with every kill rule — and
{LANE}/plans/round-86.md for the pre-freeze repairs. Two claims: C1 operability — the round-86 successor battery
(`corpus/evidence/round86/gate-records-r86.py`) builds the 200-only D1 class (an admit whose stored body arrived under
HTTP 203, from the committed S021 refetch row) inside the predicate and derives the round-85 M17 mutant from the
subject tool's own bytes, so `D1_REFUSED=1/1` and `MUT17_KILLED=1/1`; C2 calibration — `curation-r86.py` prints
`SUPERSEDED_LIVE=0 UNENTAILED_TERM=0 MODIFIED_DEF_CITED=1 QUOTES_LOCATED=20/20`, closing the round-85 routed defects
(the S024/S031 inversion and the two imported warrant cells). Ground source this round: S216 (RFC 9110 203).

Every `Report:` trailer path is relative to {LANE} — write it at {LANE}/<that path>.

Leaf only: no task tool, no subagents, no agent://all, no production edits, no lane or fleet git/jj mutation, no commits
or pushes, no edits to /home/vgpnk/Projects/shokunin/scripts, /home/vgpnk/Projects/shokunin/.ufo/state, MANIFEST.json,
considerthese/ or any sibling repo. The only files you write are under your own output folder
{LANE}/.ufo/waves/round-86/w1/<seat>/ plus your scratch dir. Network: none this round — every check reads committed
bytes (a GET is a finding; the round's fetches are already committed under corpus/captures/).

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
`npx`/an official binary in ~/.local/bin, or not at all; never `pacman -Sy`, `-Syu`, `-U`, `-R`, never downgrade,
never restart a host service."""


def item(name, role, body):
    return {"name": name, "role": role, "prompt": GODSPEED + "\n" + body.strip() + "\n"}


ITEMS = [
    item("R86ExecRepro", "executor", f"""
Reproduce both frozen claims from a clean tree at {LANDING} (C1 K1, C2 K1, and the instrument-identity leg).
(a) For every path in `{LANE}/corpus/evidence/round86/instrument-pins.txt`, `git -C {LANE} show {LANDING}:<path> | sha256sum`
and compare with the pin; report each match/mismatch.
(b) `S=<scratch>; mkdir -p $S/tree && git -C {LANE} archive {LANDING} | tar -x -C $S/tree` then
`python3 -B $S/tree/corpus/evidence/round86/gate-records-r86.py --root $S/tree --repo {LANE} --work $S` and
`python3 -B $S/tree/corpus/evidence/round86/curation-r86.py --root $S/tree`; record the full field line and exit code.
(c) Compare each predicate line against claims.md's expected values field by field and name any difference.
Write `R86ExecRepro.md` with the two field lines, every pin verdict and the comparison.""")
    ,
    item("R86ExecBase", "executor", f"""
Reproduce the BEFORE side of both claims from committed bytes and show the committed controls are not stale (C1 K3/K4,
C2 K1).
(a) C1 before: `S=<scratch>; mkdir -p $S/base85 && git -C {LANE} archive 43c3f7284eee4889cdcc6ac1626573f6579cd533 | tar -x -C $S/base85`
then run the round-86 counter with `--root <tree at {LANDING}> --tool $S/base85/tools/gate-records.py`; the expected
before line is `D1_REFUSED=0/1 MUT17_KILLED=0/1` / `GATE_RECORDS_R86=FAIL`, exit 1.
(b) C2 before: `mkdir -p $S/base86 && git -C {LANE} archive {BASE} | tar -x -C $S/base86` then
`python3 -B <tree at {LANDING}>/corpus/evidence/round86/curation-r86.py --root $S/base86`; expected
`SUPERSEDED_LIVE=1 UNENTAILED_TERM=2 MODIFIED_DEF_CITED=0` / `FAIL`, exit 1.
(c) Byte-compare the predicate and field lines you observe against
`{LANE}/corpus/evidence/round86/controls/receipts/c1-k0-donothing.txt` and `.../c2-d0-donothing.txt`; report any drift
as a finding (the instrument bytes may differ from the receipt's because the receipt names a different tree — distinguish
that from a value drift).
Write `R86ExecBase.md`.""")
    ,
    item("R86ExecForge", "executor", f"""
Attack the C1 battery's coverage from committed bytes: hunt for a 203-class forgery the battery still accepts (C1 K2).
Build candidate records from the committed S021 refetch row and capture only (no network) and run them through
`--root <tree at {LANDING}> --repo {LANE}` with the landing tool. At minimum test: (1) the D1 record exactly as the
counter builds it; (2) the same record with its quote replaced by absent text (expect QUOTE_ABSENT, not REFETCH);
(3) the same record in the `decision=reject capture=none` form claiming success with `http=203` (expect REFETCH);
(4) a 203 record whose `curl_rc` is nonzero (expect REFETCH or PARSE — name which); (5) a 203 record with a word count
off by one (expect WORDS). Report, for each candidate, the verdict line and code and whether the code is the expected
one; any candidate the tool accepts is a `NOT_REFUSED` finding with its bytes.
Write `R86ExecForge.md` plus each candidate record under `R86ExecForge/records/`.""")
    ,
    item("R86ExecHarm", "executor", f"""
Harm leg (C1 K3): show the round's instrument does not refuse records the pre-round tool accepted, over ALL committed
records. (a) Count committed `GATE-RECORD` lines: `git -C {LANE} grep -c -E '^[[:space:]]*GATE-RECORD' {LANDING}` and
per file. (b) For every file carrying records, run the landing tool and the pre-round-85 tool
(`git -C {LANE} archive 43c3f7284eee4889cdcc6ac1626573f6579cd533`, `tools/gate-records.py`) over a scratch copy of the
tree and diff the per-record verdicts; report every record whose verdict moved OK→FAIL and every FAIL→OK. (c) Report the
denominators you used and whether they match the 355 the counter's forged-battery total is built from (explain any
difference — the counter's total counts forgeries, not committed records).
Write `R86ExecHarm.md` with the comparison table and the counts.""")
    ,
    item("R86ReviewerClaims", "reviewer", f"""
Attack C1's STATED WORDING against its instrument (C1 K1/K2/K4).
(1) Read claims.md C1's sentence and the counter's code. For each clause — "generates the D1 class inside the frozen
predicate", "built from the committed S021 refetch row and its capture", "computes the M17 mutant from the subject
tool's own bytes", "the battery kills it instead of surviving it" — name the code line that enforces it, or the clause
the code does not enforce. (2) Verify `build_mutant` really rewrites the subject tool (`sha256` before/after, the exact
substitution count) and that the mutant leg would report `0/1` if the substitution found nothing. (3) Verify the D1
record's fields against the committed refetch row and capture (key, fetched, txt sha, tier) yourself; a record the
counter builds that is not derived from those bytes is a finding. (4) State whether a tool that hard-codes the D1
record's expected code could pass the predicate.
Write `R86ReviewerClaims.md` with one finding per clause: `HELD` or `FALSIFIES-WORDING: <clause> — <why>`, and the
evidence (file:line, command, output).""")
    ,
    item("R86ReviewerEntry", "reviewer", f"""
K3 attack on the two repaired decision-table rows and on C2's term check (C2 K2/K3/K4).
(1) Open `corpus/knowledge/search-transparency-reporting-r84.md` row "Recording when a resource changed" and its new
Q13; locate the quote in `corpus/captures/f5545a194c06ab421875b047.txt` yourself and say whether the Do and Never
state only what that quote states. (2) Same for `corpus/knowledge/provenance-recording-r85.md` row "Recording when
content was last reviewed", Q7, S031's registry row, and the capture `11d6cc56bb24adfc61eea2b4.txt`. (3) Attack the
`UNENTAILED_TERM` check as an instrument: can it be satisfied by deleting the offending word without repairing the
claim? Does the frozen term set miss an import class that the round-85 spot-check named (`primary`, `tool`, `version`,
`step`)? Name the consequence for C2's wording. (4) Report any cell in either entry that still states more than its
warrant entails.
Write `R86ReviewerEntry.md` with a per-row verdict and the exact quotes you located.""")
    ,
    item("R86CriticClaims", "critic", f"""
Cheap controls that falsify both claims if they pass (C1 K1/K4, C2 K1).
(1) Do-nothing C1: does ANY tool pass the round-86 counter with `D1_REFUSED=1/1 MUT17_KILLED=1/1` without the 200-only
repair? Construct the cheapest such candidate you can from committed bytes (e.g. a wrapper that post-processes the base
tool's output) and report whether the counter refuses it; name the missing leg if it would pass. (2) Do-nothing C2: gut
the registry in a scratch copy (delete the S031 row, or flip S024 back to `mined`) and show the counter fails; then show
what minimal registry edit would let a lazy lane pass C2 without repairing the entries — if one exists, that is a
K1-class finding about the predicate. (3) Check the counter's floors: `QUOTES_LOCATED` requires total>=19 but nothing
pins WHICH quotes; is deleting one entry's quotes and adding two elsewhere a pass?
Write `R86CriticClaims.md` with a verdict per control and the commands you ran.""")
    ,
    item("R86MutCounter", "mutation-tester", f"""
Mutate the two COUNTERS (not the tool) and report which mutants survive their own expected verdicts.
Copy the landing tree to scratch. For `corpus/evidence/round86/gate-records-r86.py` build at least: (M1) delete the
`forged.append((d1_label, ...))` line; (M2) force `mut17 = 1` without the mutant run; (M3) accept `d1 is None` in the
`passed` conjunction; (M4) make `build_d1_203_admit` return a record with `decision=reject`; (M5) drop `SETUP` from
`passed`. For `corpus/evidence/round86/curation-r86.py`: (N1) skip the supersession loop; (N2) compare `MODIFIED_DEF`
against the raw quote case; (N3) treat a missing capture as located; (N4) drop `UNENTAILED_TERM` from `pred`. For each
mutant, run the counter on the landing tree and on the base tree and state whether the mutant still prints the frozen
expected verdicts (survivor) or is killed (fails on one of the two trees). Report survivors with the receipt.
Write `R86MutCounter.md` with a survivor table and, for each survivor, the leg that should have killed it.""")
    ,
    item("R86RevSupply", "revenger", f"""
Append-only forensics on the round's registry edit (C2 K1/K4, and the round-85 in-place edit it repairs).
(1) `git -C {LANE} diff {BASE} {LANDING} -- corpus/SOURCES.md` and classify EVERY changed cell: which row, which column,
old value, new value. Name any change outside `status`, `recheck`, `used-by` in a pre-existing row (the S024 `opened`
restoration is expected and must be identified as a restoration, not a new edit). (2) Prove the S024 row at {LANDING}
is byte-identical to its bytes at `43c3f7284eee4889cdcc6ac1626573f6579cd533` and at an earlier revision of your choice
(cite both). (3) Check the four new/changed rows parse as 11 columns and that S216/S217's `opened` dates and the refetch
rows' `fetched_utc` agree with the egress commit's order. (4) Report any other row whose bytes changed between {BASE}
and {LANDING}.
Write `R86RevSupply.md` with the cell-level diff table and the byte comparisons.""")
    ,
    item("R86ScoutRegistry", "scout", f"""
Per-surface reconnaissance over the registry: find defects the round's counter cannot see (C2 K1 scope).
(1) Enumerate every supersession edge in `corpus/SOURCES.md` (rows whose `teaches` opens `supersedes S0NN —`) and
report each edge's (target status, superseding status) pair. Name any edge where the superseded row is `mined` while the
superseding row is not, and any where the superseding row's `teaches` contradicts the target's. (2) Enumerate every
normalized-URL group with >=2 rows and report groups whose `teaches` cells contradict each other (not just duplicate
scope). (3) List every row with `status=mined` whose `used-by` path does not exist at {LANDING}. (4) Report rows whose
`opened` date is later than the first entry that cites them. Do not edit anything; report read-only with the exact awk
or python one-liners you used.
Write `R86ScoutRegistry.md` with four numbered sections and counts.""")
    ,
    item("R86ConnectorSiblings", "connector", f"""
Sibling-overlap scan: does any other lane hold this round's ground, and does any sibling tool false-green on it?
(1) Grep the sibling lanes under /home/vgpnk/Projects/shokunin/*-shokunin (read-only) for RFC 9110 / 203 semantics,
`supersedes`, supersession invariants and any `GATE-RECORD` verifier; report which sibling (if any) holds overlapping
ground, with file:line. (2) Test whether any sibling verifier accepts chousa's round-86 lesson or registry bytes and
exits 0 while selecting 0 rows (the kotodama `check-gate-captures.py` class); name the tool, the command and the exit
code. (3) Report anything a sibling should adopt from this round, and anything this lane should stop claiming because a
sibling already holds it. Never write outside your own folder.
Write `R86ConnectorSiblings.md`.""")
    ,
    item("R86ScribeLesson", "scribe", f"""
Verify the round-86 lesson and criteria against committed bytes (report-contract conformance leg).
(1) `python3 -B {LANE}/tools/gate-records.py verify --root <tree at {LANDING}> --repo {LANE} <tree>/corpus/lessons/round-86.md`
— report the summary line and exit code. (2) Check the lesson's claim that `tools/gate-records.py` has no record form for
a successful fetch refused on content: read the tool's docstring and `parse`/`check` code and name the forms it accepts
and why a 200-rejected row cannot be expressed. (3) Check the `## Corrections` block: does `corpus/lessons/round-85.md`
still print "verified" in its `## Claim outcomes`, and does the round-86 lesson retract it without editing the round-85
file (cite both files' bytes)? (4) Check QUALITY 173–176: each cites an artifact — verify each cited artifact exists and
says what the criterion claims. (5) Check the lesson's Gate section carries the access date, URL and a <=25-word located
quote for S216 and names the S217 rejection reason.
Write `R86ScribeLesson.md` with a per-item verdict.""")
    ,
]

spec = {
    "wave": "chousa-r86-w1",
    "reportDir": ".ufo/waves/round-86/w1",
    "context": CONTEXT,
    "items": ITEMS,
}

with open(os.path.join(HERE, "w1-spec.json"), "w", encoding="utf-8") as fh:
    json.dump(spec, fh, indent=1, ensure_ascii=False)
print(f"wrote w1-spec.json items={len(ITEMS)} roles={sorted({i['role'] for i in ITEMS})}")
