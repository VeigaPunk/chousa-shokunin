#!/usr/bin/env python3
"""Build the round-95 wave-1 spec (12 seats, policy v1 band 8-16). Constants are the measured revisions."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
SCRATCH = "/fast/scratch/hyaku/chousa-r95"
BASE = "7b2373586fb70f0ead6446c671fcc8b546d3e687"
FREEZE = "d6429e02bb4807bdb4cc26cd35f62f3c5c5dc7d2"
CARRIER = "d27e9891ba6d2bae8b1f6060f7c01bf13a1a6ea1"
OUT = f"{LANE}/.ufo/waves/round-95/w1"

GODSPEED = """/skill:godspeed

You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.
"""

CONTEXT = f"""Lane chousa round 95, L1 ChousaR95a2 holds the canonical planner seat, the freeze and the integration. Root {LANE}.
Revisions: base {BASE} (round-94 landing + its non-author spot-check); claim freeze F {FREEZE}; the tree you
attack is carrier C {CARRIER} (F plus five scored receipts under corpus/evidence/round95/after/, emitted at F).
Frozen claims: {LANE}/.ufo/waves/round-95/claims.md — read it FIRST, with every kill rule and NAMED LIMIT. Machine
form: {LANE}/.ufo/waves/round-95/claims.json. Plan, pre-freeze fixes and routed defects: {LANE}/plans/round-95.md.
Two claims, two axes, both sourced on S222 (PRISMA-S, JMLA publisher PDF, capture corpus/captures/1a8c36c4c24444967bd9c3ce.txt):
C1 operability, capability acquisition: NEW tool `tools/search-rerun.py verify <record> --root <lane> [--strict]` re-runs each
recorded local search expression (`## Searches` table) at the revision the record names (COUNT_DRIFT/SET_DRIFT = the record is
wrong) and over the current tree (TREE_CHANGED = the corpus moved). Record: corpus/fixtures/search-rerun-r95.md (8 searches over
corpus/captures/*.txt at base, recorded with GNU grep 3.12 `/usr/bin/grep -l -F|-P`). Battery:
`python3 -B corpus/evidence/round95/rerun-controls-r95.py --root . --work <scratch>` → `POSITIVE=1/1 STRICT_TREE=1/1
FORGERY_REFUSED=8/8 PRIOR_ACCEPTED=8/8 SETUP_REFUSED=12/12 CLONE_TREE=2/2 DO_NOTHING_REFUSED=1/1 ORACLES_REJECTED=3/3`.
C2 depth: NEW entry corpus/knowledge/search-rerun-record-r95.md — 9 located PRISMA-S quotes (GATE-RECORD lines) warranting 7
decision rows; `python3 -B tools/gate-records.py verify --root . <entry>` → `records=9 ok=9 fail=0`; `bash tools/research-gate.sh
verify-metadata <entry> --root .` CLEAN; `python3 -B corpus/evidence/round95/entry-controls-r95.py --root . --work <scratch>` →
`POSITIVE=1/1 FORGERY_REFUSED=8/8 DO_NOTHING_REFUSED=1/1 LQ_BOUND=9/9 WARRANTS_OK=7/7`.
`tools/research-gate.sh` and `tools/gate-records.py` are UNCHANGED this round.

Your job is to FALSIFY: find where a claim's stated sentence says more than its instrument enforces, where a quote or a
decision row says more than the source, where the tool is wrong, unsafe or not new. A finding is worth more than a pass.

Every `Report:` trailer path is relative to {LANE} — write it at {LANE}/<that path>. Copy every receipt you cite
into {OUT}/ (name files `<YourSeatName>-*.txt`) before you yield.
Leaf only: no task tool, no subagents, no agent://all, no production edits, no lane or fleet git/jj mutation, no
commits or pushes, no edits to /home/vgpnk/Projects/shokunin/scripts, /home/vgpnk/Projects/shokunin/.ufo/state,
MANIFEST.json, considerthese/ or any sibling repo. The only files you write are under {OUT}/ plus your scratch dir.
Network: none, except the one scout item that names it (a read-only re-open of the S222 URL into its own scratch).
Never mutate a host sysctl, never run sudo, never restart a host service.
Scratch: every tree, work dir and fixture lives under {SCRATCH}/<your seat name>/; create it with `mkdir -p`, pass it
explicitly (`--work`, `TMPDIR=`), delete it before you yield (`trap 'rm -rf -- "$S"' EXIT` in shell, `finally:
shutil.rmtree` in Python). Never write under /tmp. To get the attacked tree: `git clone -q --shared {LANE} $S/repo` then
`git -C $S/repo checkout -q {CARRIER}` (never repack a shared clone). Any fixture git repo is `D=$(mktemp -d -p
{SCRATCH}/<seat>) && test -n "$D" && git -C "$D" init -q`, every later git call names `-C "$D"`, and you assert
`git -C "$D" rev-parse --show-toplevel` equals `$D` before any mutating git command; commit there only with
`-c user.name=fixture -c user.email=fixture@invalid`.
Note: in this host's interactive shell `grep` may be a builtin shim; use `/usr/bin/grep` (GNU grep 3.12) when grep semantics matter.
Counter that binds you: every finding names the exact command, the receipt path you wrote and the observed line plus exit
code. An unrun check has not passed; a deviation from an expected value is a finding, never something to hide.
End your report with one line per claim you touched: `VERDICT: <seat> <C1|C2> fired|held|n/a — <one sentence>` (plain text,
not JSON). `fired` means you found that the claim's wording or number is false as stated.

Tooling authorization (operator, 2026-10-19): you may install or upgrade tools that help the task; read
/home/vgpnk/.omp/agent/RULES.md first (official channels only; record tool/version/channel/reason in your report).
pacman guard (orchestrator ruling 2026-10-20): all pacman transactions are PAUSED host-wide — install via `uv tool`/
`npx`/an official binary in ~/.local/bin, or not at all; never `pacman -Sy`, `-Syu`, `-U`, `-R`, never downgrade."""


def item(name, role, task):
    return {"name": name, "role": role, "prompt": GODSPEED + task}


ITEMS = [
    item("R95ExecC1Repro", "executor", f"""Reproduce frozen C1 from a clean tree. `S={SCRATCH}/R95ExecC1Repro`; shared clone at C.
(a) From `$S/repo` run both C1 counting commands (claims.md C1 predicate) and diff their verdict lines against
`corpus/evidence/round95/after/c1-verify.txt` and `c1-controls.txt`. (b) INDEPENDENT re-derivation of the record: materialise
`corpus/captures` at base `{BASE}` with `git archive` into `$S/base`, and for each of the 8 rows of
`corpus/fixtures/search-rerun-r95.md` run GNU grep yourself (`/usr/bin/grep -l -F` for fixed, `-P` for regex) and
compute count, sorted list and `sha256sum` of the sorted list; report a table row-by-row, recorded vs yours. (c) Run the
tool against a record you write with 3 NEW searches of your own over `corpus/captures/*.txt` at base (one fixed, one regex
with `|`, one zero-hit), recorded with GNU grep; report whether the tool agrees. (d) Time one verify run. VERDICT trailer
required."""),

    item("R95ExecC2Repro", "executor", f"""Reproduce frozen C2 from a clean tree. `S={SCRATCH}/R95ExecC2Repro`; shared clone at C.
(a) From `$S/repo` run the three C2 counting commands and diff against `corpus/evidence/round95/after/c2-*.txt`.
(b) Independently, without `gate-records.py`: for each of the 9 GATE-RECORD quotes in
`corpus/knowledge/search-rerun-record-r95.md`, count occurrences in `corpus/captures/1a8c36c4c24444967bd9c3ce.txt` after your
OWN whitespace normalisation (write the 10-line script into your report), report count and line number of each.
(c) If `pdftotext` is installed, re-derive the text form from `corpus/captures/1a8c36c4c24444967bd9c3ce.raw` with
`pdftotext -layout <raw> -` and compare its sha256 with the committed `.txt` and with the `txt_sha256` of the S222 row in
`corpus/evidence/round57/refetch.tsv`; also run `pdftotext` WITHOUT `-layout` and report whether Q7+Q8+Q9's sentence
appears contiguous there (it supports or refutes the entry's named limit (a)). (d) Check that the S222 registry row is
11 columns and that `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa`
exits 0 (read-only). VERDICT trailer required."""),

    item("R95ExecEngine", "executor", f"""Engine-agreement probe (the validator has no labrat role; this executor item is that probe). Hypothesis to test (falsifiable): "for any fixed string or Python-re pattern that a record can file,
tools/search-rerun.py's per-line matcher and GNU grep `-l -F`/`-l -P` select the same files". `S={SCRATCH}/R95ExecEngine`.
Build a scratch fixture git repo (rules in context) with small files probing: CRLF line ends, a file with NUL bytes,
invalid UTF-8 bytes, a file with no trailing newline, a match on the last line, case differences, `\\s`, `$`, `^`, `\\w`
on non-ASCII (Japanese/Chinese), `\\b`, lookbehind, a pattern that only matches across a newline, a dotfile `.x.txt`
under a `*.txt` glob (bash glob skips dotfiles; does the tool?), a file in a subdirectory under `dir/*.txt`, an
empty file. For each probe record what GNU grep (`/usr/bin/grep`, invoked over a bash glob exactly as the record's
'As run' section does) selects and what `python3 -B {LANE}/tools/search-rerun.py verify <record> --root <fixture>`
reports (write records whose recorded values are GNU grep's). Report a table: probe | grep | tool | agree. Every
disagreement is a finding; say whether the frozen named limits (claims.md C1 (a)-(f)) already disclose it. VERDICT
trailer required."""),

    item("R95ReviewerC1", "reviewer", f"""Correctness review of `tools/search-rerun.py` at C (read it whole). `S={SCRATCH}/R95ReviewerC1`.
Attack: table parsing (escaped `\\|`, a cell containing a backtick, trailing spaces, a header with extra spaces, two
tables in the section, a row after a blank line), `hit_set` list parsing (spaces, duplicates in the list, an unsorted
list, a path outside the glob), the digest form (what exactly is hashed; is it what `| LC_ALL=C sort | sha256sum` prints
for non-ASCII paths?), the `where` validator (globs with `**`, `.`, empty segments, Windows separators), `static_dir`
for globs whose wildcard is in the first segment, exit-code contract (0/1/2) against the docstring, what happens when
the same glob matches a directory, and whether `TREE_CHANGED` can be raised by files the rev re-run cannot see (e.g.
untracked files). For each item: the command you ran, observed output, and whether it contradicts the docstring or a
claims.md sentence. VERDICT trailer required."""),

    item("R95SentinelScope", "sentinel", f"""Containment and side-effect review of `tools/search-rerun.py` and
`corpus/evidence/round95/rerun-controls-r95.py` at C. `S={SCRATCH}/R95SentinelScope`. Prove or refute claims.md C1 K3: the
tool writes nothing, opens no socket, and reads no path outside `--root`. Attacks: a symlink as a path component at the
REV side (a commit in a scratch fixture repo whose tree has a mode-120000 entry under the glob's static directory), a
symlinked directory on the tree side, a record path that is itself a symlink, `--root` pointing at a subdirectory of a
repo, a rev given as a branch name or `HEAD~1` (must be refused), environment variables that change git's behaviour
(`GIT_DIR`, `GIT_WORK_TREE`, `GIT_CONFIG_*`) set in the caller's environment. If `strace` is available, run the positive
verify under `strace -f -e trace=openat,connect,write` and list every opened path outside the lane and every write
fd other than 1/2. The battery: does it write only under `--work`, and does it clean up on failure? VERDICT trailer
required."""),

    item("R95MutantsC1", "mutation-tester", f"""Mutation test of C1. `S={SCRATCH}/R95MutantsC1`; shared clone at C. Write at least 12
mutants of `tools/search-rerun.py` into scratch copies (never edit the lane): e.g. drop COUNT_DRIFT, drop SET_DRIFT, compare
count only against the tree, swap `rev_ok` accounting, treat TREE_CHANGED as a finding without `--strict`, never raise
TREE_CHANGED, accept any engine, skip the `..` check, match whole-file instead of per-line, case-insensitive fixed,
digest over unsorted paths, `hits` parsed as `len(hit_set)`. For each mutant run
`python3 -B corpus/evidence/round95/rerun-controls-r95.py --root $S/repo --work $S/w --tool <mutant>` and record
`RERUN_CONTROLS=` and the failing groups. Report killed/total and list every surviving mutant with the reason it
survives and whether the frozen sentence of C1 is false because of it. VERDICT trailer required."""),

    item("R95ReviewerC2", "reviewer", f"""Fidelity review of `corpus/knowledge/search-rerun-record-r95.md` at C against its source. `S={SCRATCH}/R95ReviewerC2`.
Read the capture `corpus/captures/1a8c36c4c24444967bd9c3ce.txt` around each quote (Table 1 items 8, 9, 12, 13, 15; the
ITEM 13 and ITEM 15 explanations). For each of the 7 decision rows judge separately: does the `Do` cell say only what its
warranting quote says? does the `Never` cell follow from it, or is it the lane's addition presented as PRISMA-S? is every
non-PRISMA-S statement inside the `Lane` column? Pay special attention to: "per-source count" vs "total" in item 15, "for
each strategy" in item 13, "nearly the same" vs the lane's exactness, and whether Q6 ("slice") is about date limits rather
than revisions. Also check the entry's prose pointers (`corpus/README.md:398-399`, `corpus/lessons/round-47.md:251-253`,
the base-revision grep claim) by running them. Output a table row | verdict (faithful / overreach / lane-unmarked) | why,
and the minimal rewording for each non-faithful cell. VERDICT trailer required."""),

    item("R95ScoutSources", "scout", f"""Source re-open and reading-order check for S222. `S={SCRATCH}/R95ScoutSources`. (a) ONE read-only GET of
`https://jmla.pitt.edu/ojs/jmla/article/download/962/1274` into `$S/` (curl -fsSL --max-time 30), report http status, size
and sha256, and compare with the S222 row (`raw_sha256`) of `{LANE}/corpus/evidence/round57/refetch.tsv`. Do not write
`corpus/captures` or `refetch.tsv`. (b) Read the PDF in reading order (`pdftotext` without `-layout`, or any PDF reader you
install per the tooling rule) and quote, verbatim, the full ITEM 15 sentence that the entry's Q7-Q9 fragments come from and
the ITEM 13 sentence around "slice"; say whether the fragments are in that order in one sentence. (c) Does the JMLA PDF
itself state that the article is co-published in Systematic Reviews (the S222 row says "co-published in Systematic Reviews
10:39")? Quote the line or report that it does not. (d) Is there a newer PRISMA-S version or erratum (search the web) that
changes items 8, 9, 12, 13 or 15? Report URL and date. VERDICT trailer required."""),

    item("R95CriticClaims", "critic", f"""Falsify the frozen sentences of C1 and C2 against their instruments, at C. `S={SCRATCH}/R95CriticClaims`.
For every clause of each sentence in `.ufo/waves/round-95/claims.md`, name the instrument line that enforces it or state
that nothing does. Specific targets: C1 "refuse a record whose filed count or hit set differs" (is every way a count can
differ refused? e.g. a record whose `hit_set` lists a path twice); C1 "the nearest prior instrument" (is
`research-gate verify-sweeps` really the nearest? read tools/research-gate.sh sweeps code and the other tools/ files);
C1 "accepts all 8 one-cell forgeries" (does PRIOR_ACCEPTED prove acceptance or only exit 0 on a record with no sweeps?);
C2 "7 decision rows are each warranted" (WARRANTS_OK checks that a qid is named — is that "warranted"?); C2 "located ...
in the committed .txt capture" vs gate-records normalisation; whether each claim beats a do-nothing control on its OWN
counter (try the cheapest control that skips the claimed work and score it). Report each clause as enforced / partly /
unenforced, and propose the narrowed wording for each unenforced clause. VERDICT trailer required."""),

    item("R95RevenPrior", "revenger", f"""Is C1's capability new? Reverse-engineer the lane's existing search/sweep machinery at base
`{BASE}`. `S={SCRATCH}/R95RevenPrior`. Read `tools/research-gate.sh` (the `verify-sweeps` mode and anything else that runs a
recorded command or compares a count), `tools/*.py`, `corpus/fixtures/sweeps-r5*.md`, `corpus/knowledge/sweeps-rejections-r5.md`,
`corpus/knowledge/search-log-method-r39.md` and `corpus/README.md:385-400`. Answer: (1) does any lane instrument at base
re-execute a recorded search expression, or compare a recorded hit count or hit set? cite file:line either way. (2) What
was the original intent of the r5 sweep re-run, and does README:398-399 still describe the base state accurately? (3) Run
`bash tools/research-gate.sh verify-sweeps corpus/fixtures/search-rerun-r95.md --root ..` at C and explain WHY it is
CLEAN (which code path; does it even read a `## Searches` section?). VERDICT trailer required."""),

    item("R95ConnectorSiblings", "connector", f"""Cross-lane pattern scan, read-only. `S={SCRATCH}/R95ConnectorSiblings`. Search
`/home/vgpnk/Projects/shokunin/*-shokunin/` (excluding chousa) for: (1) any tool that re-runs a recorded search/grep
expression and compares counts (`/usr/bin/grep -rlE "rerun|re-run|recorded (count|hits)" --include='*.py' --include='*.sh'`),
(2) any knowledge entry or SOURCES row holding PRISMA-S (`grep -rl "PRISMA-S\\|jmla.2021.962"`), (3) any search-record
format with `hits`/`hit_set` columns. For each hit: path, what it does, and whether it is the same mechanism as C1/C2
(then chousa's novelty claim is a defect) or a different one. Report `OVERLAPS=n` with one line per pattern and any
cross-domain evidence chousa should route but not absorb. No writes to sibling repos. VERDICT trailer required."""),

    item("R95ScribeCorrections", "scribe", f"""Draft append-only corrections owed from the round-94 non-author spot-check
(`{LANE}/corpus/lessons/round-94-verifier-spotcheck.md`, section "Routed defects for next round", D2 and D4-D8). For each
defect, open the cited file and line YOURSELF (`LOG.md` round-94 block, `.ufo/waves/round-94/claim-falsification.tsv`, the
cited seat reports under `.ufo/waves/round-94/w1/`, `plans/round-94.md`), confirm the defect with the exact command and
observed text, and draft one correction bullet of the form `- Correction (r94 spot-check D<n>): <file>:<line> says "<old>";
the record is "<new>" (<evidence pointer>). The original text stays.` Write the draft to
`{OUT}/R95ScribeCorrections-log-draft.md`. If a defect does not reproduce, say so instead of drafting it. Also compute the
round-94 ledger class tally with `awk -F'\\t' 'NR>1{{c[$3]++}} END{{for(k in c) print k, c[k]}}'
{LANE}/.ufo/waves/round-94/claim-falsification.tsv` (check whether the file has a header first) and paste it. VERDICT
trailer: use `n/a` for C1/C2."""),
]

SPEC = {
    "wave": "chousa-r95-w1",
    "reportDir": ".ufo/waves/round-95/w1",
    "context": CONTEXT,
    "items": ITEMS,
}

if __name__ == "__main__":
    out = os.path.join(HERE, "w1-spec.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(SPEC, fh, indent=1)
    print(f"spec {out} items={len(ITEMS)} roles="
          + ",".join(f"{r}={sum(1 for i in ITEMS if i['role'] == r)}"
                     for r in sorted({i['role'] for i in ITEMS})))
