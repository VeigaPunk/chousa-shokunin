#!/usr/bin/env python3
"""Build the round-97 wave-1 spec (12 seats, policy v1 band 8-16). FREEZE is passed on the command line."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
SCRATCH = "/fast/scratch/hyaku/chousa-r97"
BASE = "c8087ac529003e667505bcc624f9a7bde0cffbce"
FREEZE = sys.argv[1] if len(sys.argv) > 1 else "<freeze>"
OUT = f"{LANE}/.ufo/waves/round-97/w1"

GODSPEED = """/skill:godspeed

You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.
"""

CONTEXT = f"""Lane chousa round 97, L1 ChousaR97 holds the canonical planner seat, the freeze and the integration. Root {LANE}.
Revisions: base {BASE} (round-96 landing); claim freeze F {FREEZE} — the tree you attack.
Frozen claims: {LANE}/.ufo/waves/round-97/claims.md — read it FIRST, with every kill rule and NAMED LIMIT. Machine form:
{LANE}/.ufo/waves/round-97/claims.json. Plan and pre-freeze fixes P0-P2: {LANE}/plans/round-97.md.
C1 operability: `tools/search-rerun.py --selftest` now runs 47 guarded in-memory cases (r01-r15 added; an exception inside a case
is that case's FAIL) → `SEARCH_RERUN_SELFTEST: PASS cases=47/47`; battery
`python3 -B corpus/evidence/round97/selftest-controls-r97.py --root . --work <scratch>` scores it against 30 EXTERNAL mutants read
from the committed round-96 seat probe `.ufo/waves/round-96/w1/R96MutantsC1-mutprobe.py.txt` (28) plus two R96SentinelC1 git_env
mutants → `POSITIVE=1/1 EXTERNAL_KILLED=30/30 DO_NOTHING_REFUSED=1/1 R96_MUTANTS_KILLED=23/23 ORACLES_REJECTED=3/3 NO_WRITE=1/1
REGRESSION_R95=2/2 BASE_KILLED=10/30 CASES=47`, `SELFTEST_CONTROLS_R97=PASS` (~8 min; `--no-regression` skips the slow r95 leg).
C2 depth: NEW entry corpus/knowledge/press-checklist-questions-r97.md — 8 decision rows on the PRESS 2015 checklist questions as
Cochrane reprints them (S225, tier B, capture corpus/captures/347c55ba9be9d63afe17986e.txt), corroborated against a Karolinska
library reprint (S226, tier C, capture corpus/captures/80a844fe287a1a26d4280251.txt); S227 = CADTH Table 9, rejected (http 403).
Counting: `python3 -B tools/gate-records.py verify --root . <entry>` → `records=30 ok=30 fail=0`; `bash tools/research-gate.sh
verify-metadata <entry> --root .` CLEAN; `python3 -B tools/search-rerun.py verify <entry> --root .` → `rev_match=7/7` CLEAN;
`python3 -B corpus/evidence/round97/entry-controls-r97.py --root . --work <scratch>` → `ENTRY_CONTROLS=PASS` (VERBATIM=10/26 LETTERS=14/26).
Receipts at F: {LANE}/corpus/evidence/round97/after/ and before/.

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
(never repack a shared clone). Any fixture git repo is `D=$(mktemp -d -p {SCRATCH}/<seat>) && test -n "$D" && git -C "$D" init -q`,
every later git call names `-C "$D"`, and you assert `git -C "$D" rev-parse --show-toplevel` equals `$D` before any mutating
git command; commit there only with `-c user.name=fixture -c user.email=fixture@invalid`.
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
    item("R97ExecC1Repro", "executor", f"""Reproduce frozen C1 from a clean tree. `S={SCRATCH}/R97ExecC1Repro`; shared clone at F.
(a) In `$S/repo` run C1 predicates 1 and 2 (claims.md); paste the tally lines and exit codes.
(b) K4 harm: materialise the base tool (`git -C $S/repo show {BASE}:tools/search-rerun.py > $S/base.py`) and run BOTH tools'
`verify` (plain and `--strict`) on `corpus/fixtures/search-rerun-r95.md`, `corpus/knowledge/search-peer-review-dedup-r96.md` and
`corpus/knowledge/press-checklist-questions-r97.md`; diff stdout and exit codes. (c) Write 6 one-cell forged records of your own
(count, path, digest, rev, glob, engine) and run both tools; any verdict difference is a finding. (d) `git -C $S/repo diff {BASE}
{FREEZE} -- tools/search-rerun.py`: list every changed line outside `ST_*`, `st_row` and `selftest`. VERDICT trailer required."""),

    item("R97ExecC2Repro", "executor", f"""Reproduce frozen C2 from a clean tree. `S={SCRATCH}/R97ExecC2Repro`; shared clone at F.
(a) Run the four C2 counting commands; paste tallies + exit codes. (b) INDEPENDENT re-derivation of the entry's `## Searches`
record: `git archive {BASE} corpus/captures | tar -x -C $S/base` and run each of the 7 rows yourself with `/usr/bin/grep -l -F`
or `-P`; count, sorted list and sha256 of the sorted list; table recorded vs yours. (c) WITHOUT the lane's scripts, write your own
≤25-line script: for every Located-quotes row find the capture line number(s) containing it in its own source's capture; then
recount the corroboration (S225 quotes found in S226 verbatim after whitespace collapse, and after lowercasing and deleting
non-alphanumerics). Paste the script and both counts; any difference from 10/26 and 14/26 is a K5 finding. VERDICT trailer required."""),

    item("R97MutantsC1", "mutation-tester", f"""Mutation test of C1 BEYOND its 30 named sites. `S={SCRATCH}/R97MutantsC1`; shared clone at F.
Write at least 20 NEW one-site mutants of `tools/search-rerun.py` at F that are not among the 30 (read them from the battery and
from `.ufo/waves/round-96/w1/R96MutantsC1-mutprobe.py.txt`) — include the parse checks, `matches`/`seg_match`, `hit`, `lines_of`,
`digest`, `evaluate`, `git_env`, and the NEW guard machinery (`case`, `refusal`, the summary line). Each must apply exactly once.
For each: run `--selftest` (KILLED = exit 1 + `SEARCH_RERUN_SELFTEST: FAIL` + no traceback). For every survivor also run the r95
battery `python3 -B corpus/evidence/round95/rerun-controls-r95.py --root $S/repo --work $S/w --tool <mutant>`. Classify survivors
(equivalent / covered by r95 battery / uncovered). State whether any survivor makes a SENTENCE of C1 false as worded (named
limits (a)(b) are part of the claim). Put the probe script and its full output in your receipts. VERDICT trailer required."""),

    item("R97MutantsC2", "mutation-tester", f"""Mutation test of the C2 instrument. `S={SCRATCH}/R97MutantsC2`; shared clone at F.
Target `corpus/evidence/round97/entry-controls-r97.py`: write at least 12 one-site mutants (e.g. drop the S225 test in SOLE_SUPPORT,
`norm`→identity, `letters` keeping punctuation, ONE_LINE using whole text, `stated` regex loosened, CORROBORATION forgery no-op,
a forgery's expected code swapped) and run each with `--root $S/repo --work $S/w`; a mutant is KILLED if the battery prints
`ENTRY_CONTROLS=FAIL` or a SETUP line. Then forge the ENTRY itself in 6 ways the battery should refuse but might not (e.g. a Do cell
that inverts its quote while sharing a word; a row citing only S226 and one irrelevant S225 quote; a stated count with a different
denominator). Report survivors and whether any falsifies a C2 sentence. VERDICT trailer required."""),

    item("R97ReviewerC1", "reviewer", f"""Correctness review of the C1 change at F. `S={SCRATCH}/R97ReviewerC1`; shared clone at F.
Read `git -C $S/repo diff {BASE} {FREEZE} -- tools/search-rerun.py corpus/evidence/round97/selftest-controls-r97.py`. Check:
(1) each of r01-r15 asserts what the real tool does (run the real parser/matcher on each input yourself); (2) the guard: can a case
pass while its body raised? can the summary print PASS with a failed case? (3) the battery reads the 28 mutants from committed BASE
bytes faithfully (compare to the probe file) and its exclusions match the seat's own verdicts; (4) does the KILLED rule (exit 1 +
FAIL line + no 'Traceback' in stderr) let a crash count as a kill in any path; (5) is `os.environ` restored after r13 on every path.
Every defect: file:line, command, observed output. VERDICT trailer required."""),

    item("R97ReviewerC2", "reviewer", f"""Fidelity review of `corpus/knowledge/press-checklist-questions-r97.md` at F against its sources.
`S={SCRATCH}/R97ReviewerC2`; shared clone at F. For EACH of the 8 decision rows: do the Do and Never cells say only what the
warranting quotes (and their capture context: `corpus/captures/347c55ba9be9d63afe17986e.txt`, `80a844fe287a1a26d4280251.txt`) say?
Mark each row faithful / overreach (quote the overreaching words) / misattributed. Check the `## Two reprints compared` paragraph's
classification of the 12 non-matching quotes against the captures, the Lane cells' statements about `tools/search-rerun.py` against
the tool at F, and the SOURCES.md rows S225-S227 (tier, scope, anchor, teaches) against the bytes. VERDICT trailer required."""),

    item("R97CriticClaims", "critic", f"""Adversarial reading of claims.md (both claims) against the instruments at F.
`S={SCRATCH}/R97CriticClaims`; shared clone at F. For every clause of each claim sentence, name the instrument leg that enforces it,
or show it is unenforced. Build at least two cheap stand-ins per claim that meet the counting commands' printed tallies without the
claimed property (e.g. a self-test that detects mutants by hashing its own source; an entry whose rows are lexically warranted but
say the opposite; a battery run where EXTERNAL counts but a mutant was skipped) and run them. Does the do-nothing control in
`corpus/evidence/round97/before/` really score the base with the FROZEN counter? Is C2's "used for corroboration and never as a
row's only support" what SOLE_SUPPORT checks? VERDICT trailer required."""),

    item("R97SentinelC1", "sentinel", f"""Side-effect audit at F. `S={SCRATCH}/R97SentinelC1`; shared clone at F.
(1) `strace -f -e trace=file,network,process` (install via official channel only if absent; else use python audit hooks)
`python3 -B tools/search-rerun.py --selftest`: any file write, any exec of git, any socket? (2) Does r13's `os.environ` mutation
leak (run the self-test in-process after setting your own GIT_DIR and check it is restored)? (3) Run the C1 battery with
`--no-regression` under strace or inotify: does it write anywhere outside `--work`, run any mutating git command, or touch the lane
index (`git -C $S/repo status --porcelain` and `.git/index` mtime before/after)? (4) Same for `entry-controls-r97.py`.
VERDICT trailer required."""),

    item("R97ScoutSources", "scout", f"""Source re-open and frontier scout. `S={SCRATCH}/R97ScoutSources`. Network allowed ONLY for the URLs
named here, read-only, into $S (never corpus/captures or refetch.tsv), at most 2 attempts each:
S225 https://work.cochrane.org/sites/work.cochrane.org/files/uploads/checklist_searches_for_editors_cochrane_work.pdf ,
S226 https://kib.ki.se/en/search-evaluate/systematic-reviews/press-2015-checklist-search-strategies ,
S227 https://www.cda-amc.ca/sites/default/files/PRESS_Peer_Review_Electronic_Search_Strate/Table_9-PRESS.pdf .
(1) sha256 of each body vs `corpus/evidence/round57/refetch.tsv` rows; `pdftotext -layout` S225 and diff against the capture.
(2) Locate 6 quotes of your choice from the entry in your own copies. (3) Is S226 an independent transcription or a copy of S225
(compare wording differences; any shared errors)? (4) Use web search only (no fetch) to list any OTHER reachable reprint or primary
route of the PRESS 2015 checklist (publisher, PMC, institutional repository) as leads with URLs — do not fetch them. VERDICT trailer required."""),

    item("R97RevenPrior", "revenger", f"""Is each claim new, and was the routed debt really open? `S={SCRATCH}/R97RevenPrior`; shared clone at F.
(1) At BASE, did any lane instrument already kill the 20 base survivors (run `corpus/evidence/round95/rerun-controls-r95.py` and
`corpus/evidence/round96/selftest-controls-r96.py --no-regression` with `--tool <each base mutant>` for at least 8 of them)?
(2) At BASE, does any lane file already hold the PRESS checklist questions (`git -C $S/repo grep -n -F` for 5 question strings over
the whole tree at BASE)? (3) D1 (round-96 spot-check): read `tools/gate-records.py`, `tools/capture-fetch.py`,
`tools/store-record-audit.py` and determine, on a scratch COPY of `corpus/evidence/round57/refetch.tsv`, whether appending a
correction row (propose its exact shape) breaks any of the three; this decides whether the lane's refusal to write it this round
(plans/round-97.md) was necessary. VERDICT trailer required (n/a allowed)."""),

    item("R97ConnectorSiblings", "connector", f"""Cross-lane pattern scan, read-only. `S={SCRATCH}/R97ConnectorSiblings`.
Scan sibling lane repos under /home/vgpnk/Projects/shokunin/*-shokunin (read-only: `git -C <repo> grep`, no writes) for (a) self-tests
that guard each case against exceptions or score against externally-written mutants, (b) knowledge on search peer review / PRESS /
reprint-vs-primary corroboration. For each match: path, revision, one-line relevance, and whether chousa's C1/C2 contradicts or
duplicates it. Route, do not absorb. Also: does any sibling hold a reachable copy of the PRESS 2015 checklist primary? VERDICT
trailer: n/a allowed."""),

    item("R97ScribeLesson", "scribe", f"""Draft the round-97 lesson's `## Mistakes` section and a LOG.md entry draft. Read
`{LANE}/corpus/lessons/round-96.md`, `{LANE}/corpus/lessons/round-96-verifier-spotcheck.md`, `{LANE}/plans/round-97.md` (pre-freeze
fixes P0-P2) and `{LANE}/.ufo/waves/round-96/w1/R96MutantsC1.md`. Mine ONE mistake class with: class · evidence pointer (path:line) ·
captured-by (the criterion or rule that should have caught it, or `none`) · fix — and say how the fix was shown able to fail (point
to the receipt line that shows the base failing). Candidate: round-96's self-test reported `PASS cases=32/32` while 19 seat-written
mutants survived, 4 of them by crashing (traceback, no summary). Open every file you cite yourself. Write
`{OUT}/R97ScribeLesson-mistakes-draft.md` and `{OUT}/R97ScribeLesson-log-draft.md`. VERDICT trailer: n/a for C1/C2."""),
]

SPEC = {
    "wave": "chousa-r97-w1",
    "reportDir": ".ufo/waves/round-97/w1",
    "context": CONTEXT,
    "items": ITEMS,
}

if __name__ == "__main__":
    out = os.path.join(HERE, "w1-spec.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(SPEC, fh, indent=1)
    print(f"spec {out} items={len(ITEMS)} roles="
          + ",".join(f"{r}={sum(1 for i in ITEMS if i['role'] == r)}" for r in sorted({i['role'] for i in ITEMS})))
