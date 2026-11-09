#!/usr/bin/env python3
"""Build the round-96 wave-1 spec (12 seats, policy v1 band 8-16). FREEZE is passed on the command line."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
SCRATCH = "/fast/scratch/hyaku/chousa-r96"
BASE = "bbf64970b6c73ca64bcc5f6de2f33b0550459813"
FREEZE = sys.argv[1] if len(sys.argv) > 1 else "<freeze>"
OUT = f"{LANE}/.ufo/waves/round-96/w1"

GODSPEED = """/skill:godspeed

You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.
"""

CONTEXT = f"""Lane chousa round 96, L1 ChousaR96 holds the canonical planner seat, the freeze and the integration. Root {LANE}.
Revisions: base {BASE} (round-95 landing + its non-author spot-check); claim freeze F {FREEZE} — the tree you attack.
Frozen claims: {LANE}/.ufo/waves/round-96/claims.md — read it FIRST, with every kill rule and NAMED LIMIT. Machine form:
{LANE}/.ufo/waves/round-96/claims.json. Plan and pre-freeze fixes P0-P3: {LANE}/plans/round-96.md.
C1 operability: `tools/search-rerun.py --selftest` (NEW; 32 in-memory cases; judgement cases go through the same `evaluate`
function `verify` runs) → `SEARCH_RERUN_SELFTEST: PASS cases=32/32`; battery
`python3 -B corpus/evidence/round96/selftest-controls-r96.py --root . --work <scratch>` → `POSITIVE=1/1 DO_NOTHING_REFUSED=1/1
MUTANTS_KILLED=23/23 ORACLES_REJECTED=3/3 NO_WRITE=1/1 REGRESSION_R95=2/2 CASES=32`, `SELFTEST_CONTROLS=PASS` (takes ~10 min:
its REGRESSION leg re-runs the round-95 battery and mutant rebuild; pass `--no-regression` when you only need the other groups).
SKILL.md gains a Gates row `search-rerun` (r96 re-registration, kind gate).
C2 depth: NEW entry corpus/knowledge/search-peer-review-dedup-r96.md — 8 decision rows warranted by 30 located quotes of
PRISMA-S items 14/16 + Box 1 (S224, the PRISMA-S publisher PDF capture corpus/captures/1a8c36c4c24444967bd9c3ce.txt, re-opened
this round under a second scope) and of the PRESS 2015 authors' JCHLA abstract (S223, capture
corpus/captures/e94691f583d644da14661ec1.txt, tier B); plus a `## Searches` record of 8 real searches run with GNU grep at base.
Counting: `python3 -B tools/gate-records.py verify --root . <entry>` → `records=31 ok=31 fail=0`; `bash tools/research-gate.sh
verify-metadata <entry> --root .` CLEAN; `python3 -B tools/search-rerun.py verify <entry> --root .` → `rev_match=8/8` CLEAN;
`python3 -B corpus/evidence/round96/entry-controls-r96.py --root . --work <scratch>` → `ENTRY_CONTROLS=PASS`.

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
    item("R96ExecC1Repro", "executor", f"""Reproduce frozen C1 from a clean tree. `S={SCRATCH}/R96ExecC1Repro`; shared clone at F.
(a) In `$S/repo` run C1 predicate 1 and 2 (claims.md) and predicate 3; paste the tally lines and exit codes.
(b) Behaviour preservation: materialise the base tool (`git -C $S/repo show {BASE}:tools/search-rerun.py > $S/base.py`) and
run BOTH the base tool and the F tool `verify` on `corpus/fixtures/search-rerun-r95.md` and on
`corpus/knowledge/search-peer-review-dedup-r96.md`, plus `--strict`; diff stdout and exit codes line by line. Any difference is a
finding against K5. (c) Write 6 one-cell forged records of your own (count, path, digest, rev, glob, engine) and run both tools;
report any verdict that differs. VERDICT trailer required."""),

    item("R96ExecC2Repro", "executor", f"""Reproduce frozen C2 from a clean tree. `S={SCRATCH}/R96ExecC2Repro`; shared clone at F.
(a) Run the four C2 counting commands and paste tallies + exit codes. (b) INDEPENDENT re-derivation of the entry's `## Searches`
record: `git archive {BASE} corpus/captures | tar -x -C $S/base` and run each of the 8 rows yourself with GNU grep
(`/usr/bin/grep -l -F` or `-P`, reading every `\\|` as `|`), compute count, sorted list and sha256 of the sorted list; table
recorded vs yours. (c) Without gate-records.py: for each of the 30 quoted GATE-RECORD lines count occurrences in its capture
after your own whitespace/curly-quote normalisation (put your ≤15-line script in the report) and give the line number(s).
(d) `pdftotext` (if installed) WITHOUT `-layout` on `corpus/captures/e94691f583d644da14661ec1.raw`: do L19-L23, L24-L25 and
L26-L29 each read as one contiguous sentence in reading order? Paste the reading-order sentences. VERDICT trailer required."""),

    item("R96ExecWrap", "executor", f"""Probe (falsifiable hypothesis): "the entry's per-line searches under-count statements that a layout text form wraps
across lines". `S={SCRATCH}/R96ExecWrap`; shared clone at F. For the two captures S223 (`corpus/captures/e94691f583d644da14661ec1.raw`)
and S224/S222 (`corpus/captures/1a8c36c4c24444967bd9c3ce.raw`) build a reading-order text with `pdftotext` (no `-layout`) and a
whitespace-joined single-line form into `$S`. Run the 8 expressions of the entry's `## Searches` table (GNU grep, `-F`/`-P`) over
(i) the committed layout `.txt`, (ii) reading-order, (iii) joined. Table: query | layout | reading-order | joined. State whether
the entry's named limit (c) and its Q6 note describe the result exactly, under-state it or over-state it. Also: does any decision
row's Do cell rely on a sentence that exists only across a column line break? VERDICT trailer required."""),

    item("R96MutantsC1", "mutation-tester", f"""Mutation test of C1 beyond its frozen 23 sites. `S={SCRATCH}/R96MutantsC1`; shared clone at F. Write at
least 12 NEW one-site mutants of `tools/search-rerun.py` (not among the 23 in `corpus/evidence/round96/selftest-controls-r96.py`
MUTANTS), aimed at `evaluate`, `parse_text`, `cells`, `matches`, `seg_match`, `hit`, `digest`, `static_dir`, `git_env` — e.g. swap
`at_rev`/`at_tree` roles, `tree_same` accounting, `findings` counted per row not per code, `hits` regex accepting a sign, date
regex loosened, `HEADER` order, `SPLIT_RE` lookbehind dropped, `lines_of` on `\\r\\n`, regex `search`→`match`, utf-8 decode
strict. Run each mutant's `--selftest` (copy into scratch; never edit the lane) and record exit and failed cases. Report
killed/total, every SURVIVOR with why it survives, and whether any survivor makes a sentence of claims.md C1 false as stated
(vs. falling under named limit (b)). VERDICT trailer required."""),

    item("R96ReviewerC1", "reviewer", f"""Correctness review of the C1 change at F: `git -C $S/repo diff {BASE} {FREEZE} -- tools/search-rerun.py`
(`S={SCRATCH}/R96ReviewerC1`). Check: (1) is `verify` behaviourally identical to base (the `evaluate` extraction, the
`at_rev_of` closure, argparse changes: `verify` without args, `--selftest verify x`, `-h`)? (2) Is every selftest case's
expectation correct by an independent derivation (recompute ST_AB_DIGEST yourself; check each p/m/j case)? (3) Does the
docstring's case count and description match the code (14 parse, 8 matching, 10 judgement)? (4) Does the self-test exercise
`verify`'s actual decision code, as the claim says, or a copy? (5) Is the new SKILL.md Gates row (search `r96 re-registration`)
accurate in every cell, and does the `## Gates` vocabulary (`gate|probe`) fit? Each item: command, observed output, and whether it
contradicts a claims.md sentence. VERDICT trailer required."""),

    item("R96SentinelC1", "sentinel", f"""Side-effect audit of `tools/search-rerun.py --selftest` at F (claims.md C1 K4). `S={SCRATCH}/R96SentinelC1`.
Run it under `strace -f -e trace=openat,open,creat,connect,execve,clone,clone3,write,unlink,rename` (if strace is available) from an
empty cwd with HOME and TMPDIR in scratch; list every opened path that is not the interpreter/stdlib, every execve, every connect,
every write to a fd other than 1/2. Does the `m08-env-scrub` case leave `os.environ` exactly as it was (also when GIT_DIR was set
by the caller before)? Does `--selftest` behave the same with `GIT_DIR`/`PYTHONPATH` pointed at hostile paths? Also audit the
battery `selftest-controls-r96.py`: does it write only under `--work` and clean up on a failing run (kill it mid-run with a short
timeout and look)? VERDICT trailer required."""),

    item("R96ReviewerC2", "reviewer", f"""Fidelity review of `corpus/knowledge/search-peer-review-dedup-r96.md` at F against its sources.
`S={SCRATCH}/R96ReviewerC2`. Read the S224 capture `corpus/captures/1a8c36c4c24444967bd9c3ce.txt` around Table 1 items 14/16
(~lines 296-316), the ITEM 14 explanation (~840-885), ITEM 16 (~888-925) and Box 1 "Peer review" (~1044-1046); and the S223 capture
`corpus/captures/e94691f583d644da14661ec1.txt` lines 142-177. For each of the 8 decision rows judge separately: does Do say only what
its warrant quotes say? does Never follow from them, or is it the lane's addition presented as the source's? is every non-source
statement inside the Lane column? Pay special attention to: "should strongly consider" vs any mandatory reading; PRESS timing
("after the MEDLINE search has been developed") vs the row's generalisation; whether six elements are really the abstract's
grouping; "describe" vs "do"; whether the S223 row's tier B, scope and anchor (pages 98-99) are accurate; whether S224's scope cell
overclaims. Output: table row | verdict (faithful / overreach / lane-unmarked) | why | minimal rewording. VERDICT trailer required."""),

    item("R96CriticClaims", "critic", f"""Adversarial reading of claims.md (both claims) against the instruments at F. `S={SCRATCH}/R96CriticClaims`.
For every clause of each claim sentence, name the instrument line that enforces it or say "unenforced". Specific suspects: C1
"scored by the same `evaluate` function `verify` runs" (is that checked anywhere?); "writes nothing" vs NO_WRITE's actual scope;
"registers the tool as a gate" vs the predicate-3 grep; whether DO_NOTHING could pass for a reason other than "no self-test";
whether a source-blind stand-in (e.g. a self-test that only checks the 23 mutated lines by text) could pass the battery — build it
if cheap and score it. C2: "warranted" vs WARRANT_TERMS' lexical floor; "real searches" vs what the record proves; "opened this
round" for S224 (same bytes as S222); separability of C1/C2 (does C2 need anything C1 adds?). Propose the narrowed wording for
each unenforced clause. VERDICT trailer required."""),

    item("R96ScoutSources", "scout", f"""Source re-open and frontier scout. `S={SCRATCH}/R96ScoutSources`. (1) Re-open into your own scratch, one
`curl -sSL` GET each: `https://journals.library.ualberta.ca/jchla/index.php/jchla/article/download/28195/20695/73210` (S223) and
`https://jmla.pitt.edu/ojs/jmla/article/download/962/1274` (S224); compare raw sha256 with `corpus/evidence/round57/refetch.tsv`
(rows S223 / S224, round 96) and `pdftotext -layout` sha256 with the committed `.txt`. (2) Verify S223's bibliographic cells from the
bytes: authors, title, JCHLA volume 37, pages 96-100, doi 10.5596/c16-019, and that the PRESS abstract is on pages 98-99. (3) With
web search only (no further GETs), find whether an open full-text route to the PRESS 2015 Guideline Statement or the CADTH E&E exists
that a plain GET could reach (e.g. PMC, Europe PMC, institutional repository); report URLs as leads, not fetched. (4) Is there an
erratum or a newer PRESS/PRISMA-S version? VERDICT trailer required."""),

    item("R96RevenPrior", "revenger", f"""Is C1 new, and was D1 really open? `S={SCRATCH}/R96RevenPrior`. At base `{BASE}`: read
`corpus/lessons/round-95-verifier-spotcheck.md` (D1), the SKILL.md `## Gates` header and the §Gate standard wording (search SKILL.md and
`/home/vgpnk/Projects/shokunin/PROTOCOL.md` for "self-test"/"gate|probe"), and `tools/search-rerun.py`. Answer: (1) did any lane
mechanism at base self-test search-rerun (cite file:line either way)? (2) what does the §Gate standard require of a gate row and does
the r96 row satisfy each requirement? (3) other tools in `tools/` that have no `--selftest` but are registered as gates — list them
(they are routing candidates, not this round's claim). VERDICT trailer required."""),

    item("R96ConnectorSiblings", "connector", f"""Cross-lane pattern scan, read-only. `S={SCRATCH}/R96ConnectorSiblings`. Search
`/home/vgpnk/Projects/shokunin/*-shokunin/` (excluding chousa) for (1) knowledge entries or SOURCES rows on search peer review / PRESS
/ deduplication (`/usr/bin/grep -rlE "PRESS|Peer Review of Electronic Search|deduplicat" --include='*.md'`), (2) tools with an
in-memory `--selftest` over their own decision function and a mutant battery that scores it (`grep -rlE "selftest|self-test"
--include='*.py'`). For each hit: path, what it does, same mechanism as C1/C2 or different. Report `OVERLAPS=n`, one line per
pattern, and anything chousa should route but not absorb. No writes to sibling repos. VERDICT trailer required."""),

    item("R96ScribeCorrections", "scribe", f"""Draft append-only corrections owed from the round-95 non-author spot-check
(`{LANE}/corpus/lessons/round-95-verifier-spotcheck.md`, section 6 "Routed defects", D2, D3, D5, and section 7's revised D4). For each,
open the cited file and line YOURSELF (`corpus/lessons/round-95.md`, `.ufo/reports/round-95/chousa.md` in
/home/vgpnk/Projects/shokunin, `SCORECARD.md`, `corpus/README.md`, `corpus/evidence/round95/`), confirm the defect with the exact
command and observed text, and draft one correction bullet of the form `- Correction (r95 spot-check D<n>): <file>:<line> says
"<old>"; the record is "<new>" (<evidence pointer>). The original text stays.` Write the draft to
`{OUT}/R96ScribeCorrections-log-draft.md`. If a defect does not reproduce, say so instead of drafting it. VERDICT trailer: use `n/a`
for C1/C2."""),
]

SPEC = {
    "wave": "chousa-r96-w1",
    "reportDir": ".ufo/waves/round-96/w1",
    "context": CONTEXT,
    "items": ITEMS,
}

if __name__ == "__main__":
    out = os.path.join(HERE, "w1-spec.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(SPEC, fh, indent=1)
    print(f"spec {out} items={len(ITEMS)} roles="
          + ",".join(f"{r}={sum(1 for i in ITEMS if i['role'] == r)}" for r in sorted({i['role'] for i in ITEMS})))
