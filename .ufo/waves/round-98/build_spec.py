#!/usr/bin/env python3
"""Build the round-98 wave-1 spec (12 seats, policy v1 band 8-16). FREEZE is passed on the command line."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
SCRATCH = "/fast/scratch/hyaku/chousa-r98"
BASE = "98b8177c1e8b39cdf1167928e4f5d609f6fa81b6"
FREEZE = sys.argv[1] if len(sys.argv) > 1 else "<freeze>"
OUT = f"{LANE}/.ufo/waves/round-98/w1"
ENTRY = "corpus/knowledge/press-2015-statement-questions-r98.md"

GODSPEED = """/skill:godspeed

You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.
"""

CONTEXT = f"""Lane chousa round 98, L1 ChousaR98 holds the canonical planner seat, the freeze and the integration. Root {LANE}.
Revisions: base {BASE} (round-97 landing); claim freeze F {FREEZE} — the tree you attack.
Frozen claims: {LANE}/.ufo/waves/round-98/claims.md — read it FIRST, with every kill rule and NAMED LIMIT. Machine form:
{LANE}/.ufo/waves/round-98/claims.json. Plan, routes tried and pre-freeze fix P0: {LANE}/plans/round-98.md.
C1 operability: `tools/search-rerun.py --selftest` now runs a guard canary g00 (`_guard_canary` runs `_collect` and `_summary`
on two fixed case sets and compares every printed line and the exit code) plus 66 guarded cases (r17-r34 new) →
`SEARCH_RERUN_SELFTEST: PASS cases=67/67`; battery `python3 -B corpus/evidence/round98/selftest-controls-r98.py --root . --work <scratch>`
scores it against the 37 mutants of round-97 seat R97MutantsC1, read from the committed probe
`.ufo/waves/round-97/w1/R97MutantsC1-mutprobe.py.txt` at BASE (35 required killed; named survivors u01, u05), the round-97
battery's 34 and the round-96 battery's 23 mutants, three EQUIVALENT mutants that must survive, and five oracles (constant-pass,
hollow, always-fail, guard-blind, hash-of-self) → `... KILL_REQUIRED=35/35 ... EQUIVALENT_SURVIVED=3/3 ORACLES_REJECTED=5/5 ...
EXTERNAL_R97_KILLED=35/37 BASE_KILLED=12/37 CASES=67`, `SELFTEST_CONTROLS_R98=PASS` (~9 min; `--no-regression` skips the slow r95 leg,
~30 s with the oracles).
C2 depth: NEW entry {ENTRY} — the PRESS 2015 Guideline Statement's own abstract via Europe PMC's REST record of PMID 27005575
(S231, tier A for the abstract scope, capture corpus/captures/4ec85a1e83553aa272caeb69.txt = the JSON as served) in 15 quotes
M1-M15, an element-names comparison (S231 vs S225 headings vs S223 pointers), and 22 quotes K1-K22 holding the 20 S225 question
lines (capture corpus/captures/347c55ba9be9d63afe17986e.txt) the round-97 entry corpus/knowledge/press-checklist-questions-r97.md
did not. S228 (CADTH report 477 appendices, 403), S229 (PubMed, 203 cookie challenge), S230 (NCBI Bookshelf, reCAPTCHA page)
rejected. Counting: `python3 -B tools/gate-records.py verify --root . {ENTRY}` → `records=38 ok=38 fail=0`; `bash tools/research-gate.sh
verify-metadata {ENTRY} --root .` CLEAN; `python3 -B tools/search-rerun.py verify {ENTRY} --root .` → `rev_match=5/5` CLEAN;
`python3 -B corpus/evidence/round98/entry-controls-r98.py --root .` → `ENTRY_CONTROLS_R98=PASS` (QUESTION_LINES_HELD=36/36 BASE_HELD=16/36).
Receipts: {LANE}/corpus/evidence/round98/before/ (do-nothing controls, harm leg) and after/ (at F). Approval table for external
GETs: {LANE}/corpus/evidence/round98/egress-approval.md.

Your job is to FALSIFY: find where a claim's stated sentence says more than its instrument enforces, where a quote or a decision
row says more than its source, where the tool or a battery is wrong, unsafe or not new. A finding is worth more than a pass.
Every `Report:` trailer path is relative to {LANE} — write it at {LANE}/<that path>. Copy every receipt you cite into {OUT}/
(name files `<YourSeatName>-*.txt`) before you yield.
Leaf only: no task tool, no subagents, no agent://all, no production edits, no lane or fleet git/jj mutation, no commits or
pushes, no edits to /home/vgpnk/Projects/shokunin/scripts, /home/vgpnk/Projects/shokunin/.ufo/state, MANIFEST.json,
considerthese/ or any sibling repo. The only files you write are under {OUT}/ plus your scratch dir.
Network: none, except an item that names a URL (read-only re-open into your own scratch; never write corpus/captures or refetch.tsv).
Never mutate a host sysctl, never run sudo, never restart a host service, never spawn CPU burners.
Scratch: every tree, work dir and fixture lives under {SCRATCH}/<your seat name>/; create it with `mkdir -p`, pass it explicitly
(`--work`, `TMPDIR=`), delete it before you yield (`trap 'rm -rf -- "$S"' EXIT` in shell, `finally: shutil.rmtree` in Python).
Never write under /tmp. To get the attacked tree: `git clone -q --shared {LANE} $S/repo` then `git -C $S/repo checkout -q {FREEZE}`
(never repack a shared clone); run batteries against $S/repo, never against the live lane (its status changes while the L1 works).
Any fixture git repo is `D=$(mktemp -d -p {SCRATCH}/<seat> fx.XXXXXX) && test -n "$D" && git -C "$D" init -q`, every later git call
names `-C "$D"`, and you assert `git -C "$D" rev-parse --show-toplevel` equals `$D` before any mutating git command; commit there only
with `-c user.name=fixture -c user.email=fixture@invalid`. Never pass an empty or unchecked variable to `git -C`.
Note: in this host's interactive shell `grep` may be a builtin shim; use `/usr/bin/grep` (GNU grep 3.12) when grep semantics matter.
Counter that binds you: every finding names the exact command, the receipt path you wrote and the observed line plus exit code.
An unrun check has not passed; a deviation from an expected value is a finding, never something to hide.
End your report with one line per claim you touched: `VERDICT: <seat> <C1|C2> fired|held|n/a — <one sentence>` (plain text, not
JSON). `fired` means you found that the claim's wording or number is false as stated.

Tooling authorization (operator, 2026-10-19): you may install or upgrade tools that help the task; read
/home/vgpnk/.omp/agent/RULES.md first (official channels only; record tool/version/channel/reason in your report).
pacman guard (orchestrator ruling 2026-10-20): all pacman transactions are PAUSED host-wide — install via `uv tool`/`npx`/an
official binary in ~/.local/bin, or not at all; never `pacman -Sy`, `-Syu`, `-U`, `-R`, never downgrade."""


def item(name, role, task):
    return {"name": name, "role": role, "prompt": GODSPEED + task}


ITEMS = [
    item("R98ExecC1Repro", "executor", f"""Reproduce frozen C1 from a clean tree. `S={SCRATCH}/R98ExecC1Repro`; shared clone at F.
(a) In `$S/repo` run C1 predicates 1 and 2 (claims.md, full battery including regression); paste the tally lines and exit codes.
(b) K3 harm: materialise the base tool (`git -C $S/repo show {BASE}:tools/search-rerun.py > $S/base.py`) and run BOTH tools'
`verify` (plain and `--strict`) on `corpus/fixtures/search-rerun-r95.md`, the r96, r97 and r98 knowledge entries named in K3;
diff stdout+stderr and exit codes. (c) Write 6 one-cell forged records of your own (count, path, digest, rev, glob, engine) and run
both tools; any verdict difference is a finding. (d) `git -C $S/repo diff {BASE} {FREEZE} -- tools/search-rerun.py`: list every
changed line outside the self-test (`ST_*`, `st_row`, `_selftest_cases`, `_collect`, `_summary`, `_guard_canary`, `CANARY_*`,
`selftest`, the module docstring and the imports). VERDICT trailer required."""),

    item("R98ExecC2Repro", "executor", f"""Reproduce frozen C2 from a clean tree. `S={SCRATCH}/R98ExecC2Repro`; shared clone at F.
(a) Run the four C2 counting commands; paste tallies + exit codes. (b) INDEPENDENT re-derivation of the entry's `## Searches` record:
`git archive {BASE} corpus/captures | tar -x -C $S/base` and run each of the 5 rows yourself with `/usr/bin/grep -l -F`; table recorded
vs yours. (c) WITHOUT the lane's scripts, write your own ≤30-line script that: lists S225's capture lines between
`PRESS 2015 Guideline Evidence-Based Checklist` and `Derived from:` containing `?`; for each, decides whether the round-97 entry
and/or the round-98 entry quote it whole (one quote, or consecutive quotes joined by one space); prints held-by-both, held-at-BASE
(round-97 entry at {BASE} only) and held-after. Any difference from 36/36 and 16/36 is a K1 finding. (d) Parse S231's capture as JSON
and check every M1-M15 quote is a substring of `resultList.result[0].abstractText` with no `<h4>` inside the quote. VERDICT trailer required."""),

    item("R98MutantsC1", "mutation-tester", f"""Mutation test of C1 BEYOND its scored sets. `S={SCRATCH}/R98MutantsC1`; shared clone at F.
Write at least 20 NEW one-site mutants of `tools/search-rerun.py` at F that are not among the 37 (`.ufo/waves/round-97/w1/R97MutantsC1-mutprobe.py.txt`),
the round-97 battery's 34 or the round-96 battery's 23 — weight them on the NEW code: `_guard_canary` (compare loosened, one case set
dropped, `want_rc` ignored, `seen` all→any), `CANARY_FAIL`/`CANARY_PASS` text, `_collect`, `_summary`, the direct FAIL path in
`selftest`, and cases r17-r34. Each must apply exactly once. For each run `--selftest`; KILLED = exit 1 + `SEARCH_RERUN_SELFTEST: FAIL`
+ a case id or `setup` in `failed=` + no `Traceback` on stderr. Classify survivors (equivalent — prove it / uncovered). Separately
mutate the BATTERY `corpus/evidence/round98/selftest-controls-r98.py` (≥6 one-site mutants: kill rule loosened, EQUIVALENT leg
inverted, NAMED_SURVIVORS widened, DO_NOTHING condition flipped, an oracle dropped, `required` computed from survivors) and run each
with `--no-regression --work $S/w`; a battery mutant SURVIVES if it still prints `SELFTEST_CONTROLS_R98=PASS`. State whether any
survivor makes a C1 SENTENCE false as worded. Put probe scripts and full outputs in your receipts. VERDICT trailer required."""),

    item("R98MutantsC2", "mutation-tester", f"""Mutation test of the C2 instrument. `S={SCRATCH}/R98MutantsC2`; shared clone at F.
Target `corpus/evidence/round98/entry-controls-r98.py`: write at least 12 one-site mutants (e.g. `norm`→identity, run length cap 4→1,
`held` across entries instead of within one, `question_lines` without the `?` filter or with the footer anchor moved, ELEMENTS
substring instead of whole-line for S225, WARRANTS ignoring the source parenthesis, a forgery replacement that no longer applies,
DO_NOTHING condition flipped) and run each with `--root $S/repo`; KILLED if it prints `ENTRY_CONTROLS_R98=FAIL` or a SETUP line.
Then forge the ENTRY in 6 ways the controls or `tools/gate-records.py` should refuse but might not (e.g. a K quote that is a whole
line of the PRISMA-S part of S225 rather than the checklist; an S231 quote spanning the `<h4>` markup; a Do cell inverting its quote;
a duplicated K quote filling a run). Report survivors and whether any falsifies a C2 sentence. VERDICT trailer required."""),

    item("R98ReviewerC1", "reviewer", f"""Correctness review of the C1 change at F. `S={SCRATCH}/R98ReviewerC1`; shared clone at F.
Read `git -C $S/repo diff {BASE} {FREEZE} -- tools/search-rerun.py` and `corpus/evidence/round98/selftest-controls-r98.py`. Check:
(1) each of r17-r34 asserts what the real tool does (run the real function on each input yourself); (2) the canary: can it pass while
`_collect` or `_summary` is broken in a way a real run would expose? can the direct FAIL path be reached when the canary passes?
(3) r28 really runs no git (prove with an audit hook or strace), r29/r34 `git -C /dev/null` cannot touch any repository on any host
(what if /dev/null were replaced?); (4) are e1-e3 truly equivalent on every input (e3: is `not lines[-1]` == `lines[-1] == b""` for
every element `lines_of` can produce)? (5) is the hash-of-self oracle a faithful stand-in for round-97 routed limit (g)? (6) does the
battery read the 37 mutants, the r97 battery literals and the r96 set from committed BASE bytes faithfully? Every defect: file:line,
command, observed output. VERDICT trailer required."""),

    item("R98ReviewerC2", "reviewer", f"""Fidelity review of `{ENTRY}` at F against its sources. `S={SCRATCH}/R98ReviewerC2`; shared clone at F.
For EACH of the 10 decision rows: do the Do and Never cells say only what the warranting quotes say (K3: quote overreaching words;
a Never cell must be the negation of its own Do clause or "(none stated by the sources)")? Mark faithful / overreach / misattributed.
Check the `## Element names compared` table and paragraph against both captures (K4); S231's identity against S225's "Derived from"
citation (K5: title, authors, journal, volume, pages, DOI, PMID in the JSON); the Lane cells' statements about the lane's tools and
searches against the tree at F; the SOURCES.md rows S228-S231 (tier, scope, anchor, teaches, status, dates) against refetch.tsv and
the capture bytes; whether S231's tier A "for the abstract scope" is defensible for an index record. VERDICT trailer required."""),

    item("R98CriticClaims", "critic", f"""Adversarial reading of claims.md (both claims) against the instruments at F.
`S={SCRATCH}/R98CriticClaims`; shared clone at F. For every clause of each claim sentence, name the instrument leg that enforces it,
or show it is unenforced. Build at least two cheap stand-ins per claim that meet the printed tallies without the claimed property and
run them — for C1 at least one CONTENT-RECOGNITION self-test (passes POSITIVE and EQUIVALENT but detects the 37+34+23 scored mutants by
matching their `new` strings in its own source) to test named limit (c); for C2 an entry whose K rows quote every question line but
whose decision rows say the opposite of their quotes. Do the do-nothing controls in `corpus/evidence/round98/before/` really score the
base with the FROZEN counters? Is "kills 35 of the 37" what KILL_REQUIRED and EXTERNAL_R97_KILLED print? VERDICT trailer required."""),

    item("R98SentinelC1", "sentinel", f"""Side-effect audit at F. `S={SCRATCH}/R98SentinelC1`; shared clone at F.
(1) `strace -f -e trace=file,network,process` (install via an official channel only if absent; else python audit hooks)
`python3 -B tools/search-rerun.py --selftest`: list every file opened for write, every exec, every socket; is the claims.md named
limit (e) ("reads /dev/null and runs `git -C /dev/null` twice") exact? (2) Does r26's `os.environ` mutation of GITFOO leak (run the
self-test in-process with GITFOO preset and unset)? (3) Run the C1 battery with `--no-regression` under strace: does it write outside
`--work`, run any mutating git command, or touch the clone's index (`.git/index` mtime before/after)? Is its docstring's description
of what it does on the lane exact? (4) Same for `entry-controls-r98.py`. VERDICT trailer required."""),

    item("R98ScoutSources", "scout", f"""Source re-open and frontier scout. `S={SCRATCH}/R98ScoutSources`. Network allowed ONLY for the URLs named here,
read-only, into $S (never corpus/captures or refetch.tsv), at most 2 attempts each:
S231 https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:27005575%20AND%20SRC:MED&resultType=core&format=json ,
S225 https://work.cochrane.org/sites/work.cochrane.org/files/uploads/checklist_searches_for_editors_cochrane_work.pdf .
(1) sha256 of each body vs `corpus/evidence/round57/refetch.tsv` rows S231/S225; if S231 differs, diff the JSON `abstractText` only.
(2) Locate 6 M quotes and 4 K quotes of your choice in your own copies. (3) Is S231's record the guideline statement (title, authors,
DOI, PMID, journal, pages)? (4) Use web search only (no fetch) to list any reachable route to the statement's FULL TEXT or the CADTH
E&E other than the routes in plans/round-98.md (author manuscript, institutional repository, PMC) as leads with URLs. VERDICT trailer required."""),

    item("R98RevenPrior", "revenger", f"""Is each claim new, and was the routed debt really open? `S={SCRATCH}/R98RevenPrior`; shared clone at F.
(1) At BASE, did any lane instrument already kill the 23 R97MutantsC1 mutants the base self-test misses (run
`corpus/evidence/round97/selftest-controls-r97.py` and `corpus/evidence/round95/rerun-controls-r95.py` with `--tool <mutant>` for
at least 8 of them, including g01-g05)? (2) At BASE, does any lane file hold S231's abstract sentences or the 20 newly quoted
question lines as quotes in a knowledge entry (`git -C $S/repo grep -n -F` over corpus/knowledge at BASE for 6 of them)?
(3) Was round-97 routed limit (g) (hash-of-self) refused by any instrument at BASE? (4) D1 (round-96/97 spot-checks): propose the
exact reader rule `tools/gate-records.py` would need so a wrong `S224` refetch row cannot be matched, and test it on a scratch COPY of
the tool and `corpus/evidence/round57/refetch.tsv` — do not edit the lane. VERDICT trailer required (n/a allowed)."""),

    item("R98ConnectorSiblings", "connector", f"""Cross-lane pattern scan, read-only. `S={SCRATCH}/R98ConnectorSiblings`.
Scan sibling lane repos under /home/vgpnk/Projects/shokunin/*-shokunin (read-only: `git -C <repo> grep`, no writes) for (a) self-tests
that check their own harness (canaries, known-fail sets) or batteries with equivalent-mutant legs, (b) knowledge on PRESS, search
peer review, or reading a paper through an index record (Europe PMC/PubMed) instead of the publisher. For each match: path, revision,
one-line relevance, and whether chousa's C1/C2 contradicts or duplicates it. Route, do not absorb. VERDICT trailer: n/a allowed."""),

    item("R98ScribeLesson", "scribe", f"""Draft the round-98 lesson's `## Mistakes` section and a LOG.md entry draft. Read
`{LANE}/corpus/lessons/round-97.md`, `{LANE}/corpus/lessons/round-97-verifier-spotcheck.md`, `{LANE}/plans/round-98.md` (pre-freeze
fix P0 and the routes table) and `{LANE}/.ufo/waves/round-97/w1/R97MutantsC1.md`. Mine ONE mistake class with: class · evidence
pointer (path:line) · captured-by (the criterion or rule that should have caught it, or `none`) · fix — and say how the fix was shown
able to fail (point to the receipt line that shows the base failing). Candidates: round 97's claim that each case runs "inside a guard"
with no instrument observing the guard (R97MutantsC1 g01-g05); or P0, a new case whose text contained a scored mutant's site. Also
draft the lesson's `## Gate` lines for S228-S231 (URL, access date, ≤25-word located quote or the refusal reason) from refetch.tsv and
the captures — open every file you cite yourself. Write `{OUT}/R98ScribeLesson-mistakes-draft.md` and
`{OUT}/R98ScribeLesson-log-draft.md`. VERDICT trailer: n/a for C1/C2."""),
]

SPEC = {
    "wave": "chousa-r98-w1",
    "reportDir": ".ufo/waves/round-98/w1",
    "context": CONTEXT,
    "items": ITEMS,
}

if __name__ == "__main__":
    out = os.path.join(HERE, "w1-spec.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(SPEC, fh, indent=1)
    print(f"spec {out} items={len(ITEMS)} roles="
          + ",".join(f"{r}={sum(1 for i in ITEMS if i['role'] == r)}" for r in sorted({i['role'] for i in ITEMS})))
