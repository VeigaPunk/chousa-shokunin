#!/usr/bin/env python3
"""Build the round-100 wave-1 spec (12 seats, policy v1 band 8-16). FREEZE is passed on the command line."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
SCRATCH = "/fast/scratch/hyaku/chousa-r100"
BASE = "929c784c63a1fd17961d21742101b2b109b7b8ff"
FREEZE = sys.argv[1] if len(sys.argv) > 1 else "<freeze>"
OUT = f"{LANE}/.ufo/waves/round-100/w1"
ENTRY = "corpus/knowledge/quotation-error-update-r100.md"
OLD = "corpus/knowledge/quotation-error-rates-r99.md"
BAT = "corpus/evidence/round100/challenge-controls-r100.py"
CTL = "corpus/evidence/round100/entry-controls-r100.py"

GODSPEED = """/skill:godspeed

You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.
"""

CONTEXT = f"""Lane chousa round 100, L1 ChousaR100 holds the canonical planner seat, the freeze and the integration. Root {LANE}.
Revisions: base {BASE} (round-99 landing); claim freeze F {FREEZE} — the tree you attack.
Frozen claims: {LANE}/.ufo/waves/round-100/claims.md — read it FIRST, with every kill rule and NAMED LIMIT. Machine form:
{LANE}/.ufo/waves/round-100/claims.json. Plan and pre-freeze change P0: {LANE}/plans/round-100.md. Pre-freeze controls (committed
before F): {LANE}/corpus/evidence/round100/before/.
C1 operability: `tools/gate-records.py verify` now judges a rev-form GATE-RECORD by capture IDENTITY — `rev_capture_text` resolves
`git rev-parse rev:path` and looks the object id up in `capture_oids` (every corpus/captures/<24 hex>.txt|.raw entry of that rev's
tree, via `git ls-tree`); a .raw entry is judged by its sibling .txt at that rev when present; then the unchanged round-99 rule
`is_challenge` (≤200 words after `norm`, one of 11 markers). Round 99 judged a rev record only when its path was spelled exactly
`corpus/captures/<24 hex>.txt` (`.ufo/waves/round-99/w1/R99SentinelC1.md` F-1). Battery `python3 -B {BAT} --root . --work <scratch>`
(~25 s) → `NEG=7/7 MARK=11/11 BOUND=3/3 NORM=2/2 POS=4/4 REV=11/11 REVPOS=3/3 PROD=6/6 HARM_SAME=27/27 BASE_REV_ADMITTED=8/11
ORACLES_REJECTED=12/12`, `CHALLENGE_CONTROLS_R100=PASS`; with `--tool <base tool> --no-oracles` → FAIL (`before/c1-base.txt`). The battery
builds one fixture git repo under --work and verifies rev records with `--repo <fixture>`.
C2 freshness: NEW entry {ENTRY} answers the round-99 entry's `recheck: on-release`: the authors' 2025 update (Baethge & Jergas, Res Integr
Peer Rev 2025, pmid 40696441) read through Europe PMC's core record (S238, tier B, capture corpus/captures/b5eec205612ee5f138cf065d.txt
= the JSON as served; U0 = `title`, U1-U13 in `abstractText`), plus J1/J2 from S236 (capture 405a0054e1f6dbd1854a3618); 8 decision rows;
and {OLD} gains a `## Update` section naming the new entry and S238. S237 (PMC4627914 full text) and S239 (PMC12285159 full text) answered
http 500 to three lane GETs each and are rejected. Counting: `python3 -B tools/gate-records.py verify --root . {ENTRY}` → `records=17 ok=17
fail=0`; `bash tools/research-gate.sh verify-metadata {ENTRY} --root .` CLEAN; `python3 -B tools/search-rerun.py verify {ENTRY} --root .`
→ `rev_match=3/3` CLEAN; `python3 -B {CTL} --root .` → `ENTRY_CONTROLS_R100=PASS` (NUMBERS token-equal incl. sign, NEVER, FRESH,
FORGERY_REFUSED=13/13). Approval table for external GETs: {LANE}/corpus/evidence/round100/egress-approval.md.

Your job is to FALSIFY: find where a claim's stated sentence says more than its instrument enforces, where a quote or a decision
row says more than its source, where the tool or a battery is wrong, unsafe or not new. A finding is worth more than a pass.
Every `Report:` trailer path is relative to {LANE} — write it at {LANE}/<that path>. Copy every receipt you cite into {OUT}/
(name files `<YourSeatName>-*.txt`, always with your seat-name prefix) before you yield.
Leaf only: no task tool, no subagents, no agent://all, no production edits, no lane or fleet git/jj mutation, no commits or
pushes, no edits to /home/vgpnk/Projects/shokunin/scripts, /home/vgpnk/Projects/shokunin/.ufo/state, MANIFEST.json,
considerthese/ or any sibling repo. The only files you write are under {OUT}/ plus your scratch dir.
Network: none, except an item that names a URL (read-only re-open into your own scratch; never write corpus/captures or refetch.tsv).
Never mutate a host sysctl, never run sudo, never restart a host service, never spawn CPU burners; host paths outside your scratch
(/boot, /etc, /usr, /var) are read-only inputs.
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
    item("R100ExecC1Repro", "executor", f"""Reproduce frozen C1 from a clean tree and probe the identity rule. `S={SCRATCH}/R100ExecC1Repro`;
shared clone at F. (a) In `$S/repo` run the C1 counting command and the before command (claims.md); paste tallies + exit codes; compare
with `corpus/evidence/round100/before/c1-base.txt` and `c1-candidate.txt`. (b) In your own fixture repo (see context for the git rules)
commit S230's committed capture text (`corpus/captures/b5b8d050eea0c638e95ba674.txt` from the lane) at its capture path, then write rev
records verified with `--root $S/repo --repo <fixture>` (registry id S230) for at least 10 spellings or routes of your own that git
resolves to that blob or to a copy of it: `rev:./…`, `rev^{{commit}}`-style rev spellings (abbreviated hash, a tag name — the tool's rev
regex may refuse them: record), a committed symlink pointing at the capture, a copy in a subdirectory, the blob reached through a second
commit where the capture path was renamed or deleted (is the capture set read from the record's rev or another?), a capture re-committed
with CRLF line endings or a trailing newline added (named limit (b)). Table refused/admitted and which named limit (a)-(e) covers each
admission — an admission outside every named limit is a finding against the C1 sentence. VERDICT trailer required."""),

    item("R100MutantsC1", "mutation-tester", f"""Mutation test of the C1 change. `S={SCRATCH}/R100MutantsC1`; shared clone at F.
Write at least 20 one-site mutants of `tools/gate-records.py` at F on the NEW code (`capture_oids`, `rev_capture_text`, the rev-branch call)
and the round-99 code the battery now claims to cover (each CHALLENGE_MARKERS entry dropped — 11, `<=`→`<`, 200→199/201, `norm` dropped in
is_challenge, `.lower()` dropped, `any`→`all`): e.g. `ls-tree` path `corpus/captures/` → `corpus/`, `.txt wins` condition inverted, the
`parts[1] == "blob"` test dropped, `-z` dropped, the sibling lookup using `name[:-4]+".raw"`, `rev-parse` without `--verify`, cache keyed by
repo only, the url/admit call removed. Each mutant must apply exactly once. Run the battery `--tool <mutant> --no-oracles --work $S/w/<id>`
and classify KILLED/SURVIVED; for each survivor say whether it is equivalent (prove it) or uncovered, and whether it falsifies a clause of the
C1 sentence. Then mutate the BATTERY (≥6 one-site loosenings: a REV verdict test loosened to `rc==1`, REVPOS dropped, BASE_REV_ADMITTED
not compared, an oracle whose site is missing counted as rejected, HARM compares stdout only, the `t[g][1] > 0` guard dropped) and report
which still print PASS for the F tool and FAIL for the base tool. Receipts with probe scripts and outputs. VERDICT trailer required."""),

    item("R100SentinelC1", "sentinel", f"""Bypass and side-effect audit of C1 at F. `S={SCRATCH}/R100SentinelC1`; shared clone at F.
(1) Bypass the identity rule with S230's or S234's own text in a fixture repo: a byte-different but textually identical capture (BOM,
CRLF, NBSP, a zero-width char inside a marker), a git-lfs-style pointer, a gitlink/submodule entry at the capture path, a capture path
that is a tree not a blob, a rev that is a tag object or a tree-ish (`rev^{{tree}}`), `rev:path` where path contains `:` or starts with
`/`, a .raw whose sibling .txt is NOT a challenge page while the .raw is (and the reverse). For each: admitted or refused at F, which named
limit covers it; an uncovered admission is a finding. (2) Performance/robustness: `capture_oids` runs `git ls-tree` once per (repo, rev);
time `gate-records.py verify` over every lane GATE-RECORD file at base vs F (`time`), and run it with `--repo` pointing at a non-git dir and
at a repo with no corpus/captures. (3) `strace -f -e trace=file,network,process` (or python audit hooks) the battery and
`gate-records.py verify`: any write outside `--work`, socket, or mutating git command? Is the battery docstring exact about what it reads
and writes (it creates and commits a fixture repo under --work)? VERDICT trailer required."""),

    item("R100ReviewerC1", "reviewer", f"""Correctness review of the C1 diff at F. `S={SCRATCH}/R100ReviewerC1`; shared clone at F.
Read `git -C $S/repo diff {BASE} {FREEZE} -- tools/gate-records.py` and `{BAT}`. Check: (1) the module docstring's CHALLENGE paragraph
matches the code exactly (identity source, .raw sibling rule, which tree, what happens when rev-parse fails); (2) `capture_oids` parsing of
`git ls-tree -z` output (mode/type/oid TAB path; what if a capture path holds a tab or newline; `.txt wins`); (3) every battery leg tests
what claims.md says (REV r1-r11 each resolve via a distinct route? r9 really quotes a non-marker line? q3 really a non-capture blob? PROD
really on the production path with `--root LANE` and no `--repo`?), and each of the 12 oracles fails for its stated reason — run each oracle
yourself and read which CASE lines fail; (4) the before receipt really ran the base tool with the frozen battery; (5) QUALITY 126
(corpus/QUALITY.md): does this battery meet it, and is named limit (e) the honest residue? (6) claims.md's Separability paragraph against
what the battery actually reads. Every defect: file:line, command, observed output. VERDICT trailer required."""),

    item("R100ExecC2Repro", "executor", f"""Reproduce frozen C2 from a clean tree and re-derive it independently. `S={SCRATCH}/R100ExecC2Repro`;
shared clone at F. (a) Run the six C2 counting commands; paste tallies + exit codes; compare with `before/c2-candidate.txt`. (b) Re-run each
`## Searches` row yourself at {BASE}: `git archive {BASE} corpus/captures | tar -x -C $S/base` then `/usr/bin/grep -l -F -e <expr>`; table
recorded vs yours. (c) WITHOUT the lane's scripts, write your own ≤40-line checker: every `## Located quotes` row is in its capture's JSON
field (U0 = S238 `title`, others in `abstractText`; normalize curly quotes and whitespace only), every numeral of each Do and Never cell is
printed (same sign, same form) in that row's warrant quotes; print your tallies and compare with the controls'. (d) Network allowed for this
URL only, read-only into $S, one attempt:
https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:40696441%20AND%20SRC:MED&resultType=core&format=json — report its sha256
vs refetch.tsv row S238 and locate U7, U9, U11 in your copy. VERDICT trailer required."""),

    item("R100ReviewerC2", "reviewer", f"""Fidelity review of `{ENTRY}` and the `## Update` section of `{OLD}` at F against their sources (kill
rule). `S={SCRATCH}/R100ReviewerC2`; shared clone at F. For EACH of the 8 decision rows: do the Do and Never cells say only what the
warranting quotes say? Mark faithful / overreach / misattributed with the exact words that overreach (e.g. row 2 "the gap between them is
not a measured trend"; row 4 "record the association only as printed … risk of bias and the number of references were not"; row 5 "about
half of incorrect quotations were classed major"; row 7's method list; row 8 "treat them as a standing problem"). Check the `## What this
entry governs`, `## Named limits` and the round-99 `## Update` sentences against the captures (does the update's abstract support "no
significant improvement over time by meta-regression"? does anything say how many studies the two syntheses share?); the tier choice
(S238 B, index record); SOURCES.md rows S237-S239 and the S236 used-by change against refetch.tsv and the capture bytes; the Lane cells'
statements about lane tools and rules. Any overreach is a C2 finding. VERDICT trailer required."""),

    item("R100MutantsC2", "mutation-tester", f"""Mutation test of the C2 instrument. `S={SCRATCH}/R100MutantsC2`; shared clone at F.
Target `{CTL}`: write at least 14 one-site mutants (e.g. `norm`→identity, NUM losing the leading `-?` or `%`, token membership `in wtoks`
→ substring of the warrant text, NUMBERS reading only Do cells, NEVER accepting any cell, FRESH not checking the `## Update` content or the
`updates:` path, FIELD `in` instead of `==` for U0, IDENTITY dropping pmcid or volume, TOPIC case-insensitive or one phrase only, BASE leg
inverted, a forgery whose replacement no longer applies counted as refused, ACCEPT inverted, `passes` accepting n==0) and run each with
`--root $S/repo`; KILLED if it prints `ENTRY_CONTROLS_R100=FAIL` or SETUP. Note forgeries whose `replace` silently changes nothing. Then
forge the ENTRY in 6 ways the controls or `tools/gate-records.py` should refuse but might not (a Do cell that reverses its warrant with no
number — e.g. "accuracy has improved"; a number in the right form but the wrong sense, e.g. "25" from U11's N used as a percent elsewhere;
a U quote that is in `abstractText` but cut so it reverses meaning; a `## Update` section that names the entry but says the opposite).
Report survivors and whether any falsifies a C2 sentence. VERDICT trailer required."""),

    item("R100CriticClaims", "critic", f"""Adversarial reading of claims.md (both claims) against the instruments at F. `S={SCRATCH}/R100CriticClaims`;
shared clone at F. For every clause of each claim sentence, name the instrument leg that enforces it, or show it is unenforced (e.g. C1
"has the object id of a … entry of that rev's tree": is any leg's capture set at a rev different from the working tree? C2 "every Do/Never
numeral is a token of that row's own warrant quotes": is a numeral in a Never cell ever present?). Build at least two cheap stand-ins per
claim that meet the printed tallies without the claimed property and RUN them through the frozen counters — for C1 e.g. a tool that refuses
every rev record whose blob is ≤200 words with a marker regardless of path (o4 is one; find another the oracles miss), or keys on the
battery's fixture keys/`fixture.invalid`; for C2 an entry whose numerals pass but whose Do cells state the opposite of their warrants, or a
`## Update` that names the entry and S238 but says nothing true. Is C2's axis "freshness" right by /home/vgpnk/Projects/shokunin/AXES.md
("skill claims re-verified against live surfaces; stale items flagged or fixed") or is it depth/coverage? Is each do-nothing control the
cheapest one that skips the work? VERDICT trailer required."""),

    item("R100ScoutSources", "scout", f"""Source re-open and frontier scout. `S={SCRATCH}/R100ScoutSources`. Network allowed ONLY for the URLs
named here, read-only, into $S (never corpus/captures or refetch.tsv), at most 2 attempts each:
https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12285159/fullTextXML ;
https://www.ebi.ac.uk/europepmc/webservices/rest/PMC4627914/fullTextXML ;
https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:40696441%20AND%20SRC:MED&resultType=core&format=json ;
https://europepmc.org/api/fulltextRepo?pprId=PMC12285159&type=FILE&fileName=main.pdf (record status only, do not parse a PDF body).
(1) For each: http status, bytes, user agent you sent, and whether the body is the document. If the lane's GETs got 500 and yours get 200,
compare request headers with `tools/capture-fetch.py`'s recipe (its UA, `--compressed`) — is the 500 recipe-specific? (2) If the 2025 full
text answers, report: how "major" is defined, how many of the 46 studies overlap the 2015 set, and any sentence that contradicts a decision
row of {ENTRY}, quoted ≤25 words each. (3) Web search only (no fetch) for one more synthesis or primary study of citation/quotation accuracy
outside medicine (leads with URLs, not opened). VERDICT trailer required (n/a allowed)."""),

    item("R100RevenPrior", "revenger", f"""Is each claim new, and why did round 99 miss F-1? `S={SCRATCH}/R100RevenPrior`; shared clone at F.
(1) At BASE, list every lane GATE-RECORD of rev form (`/usr/bin/grep -rn '^GATE-RECORD .* rev=' corpus/`) and its path spelling; would the
F tool change any of their verdicts (HARM says no — re-derive independently)? (2) At BASE, did any lane instrument other than
gate-records.py check rev records against captures by identity or path normalization (`git -C $S/repo grep -n -e 'ls-tree' -e normpath
{BASE} -- tools corpus/evidence`)? (3) Read `.ufo/waves/round-99/w1/R99MutantsC1.md` and run round 99's surviving tool mutants (rebuild them
from that file's table at F's tool — the code moved) against the round-100 battery: which survive now? (4) At BASE, does any knowledge entry
other than {OLD} hold a rate that a newer source has since updated, flagged by an `## Update` or `superseded` line? Count entries with
`recheck: on-release` and whether any has ever been answered. Propose the next-round rule. VERDICT trailer required (n/a allowed)."""),

    item("R100ConnectorSiblings", "connector", f"""Cross-lane pattern scan, read-only. `S={SCRATCH}/R100ConnectorSiblings`.
Scan sibling lane repos under /home/vgpnk/Projects/shokunin/*-shokunin (read-only: `git -C <repo> grep`, no writes) for (a) any rule or tool
that resolves a cited file by content identity (git object id, sha256) rather than path spelling, or that normalizes cited paths before a
guard; (b) knowledge on the 2025 quotation-inaccuracy update (pmid 40696441, "quotation inaccuracy", "16.9%"), on stale-knowledge flags
(`## Update`, `superseded`, `recheck: on-release` answered). For each match: path, revision, one-line relevance, and whether chousa's C1/C2
contradicts, duplicates or should adopt it. Route, do not absorb. VERDICT trailer: n/a allowed."""),

    item("R100ScribeLesson", "scribe", f"""Draft the round-100 lesson's `## Gate` and `## Mistakes` sections and a LOG.md entry draft. Read
`{LANE}/corpus/lessons/round-99.md`, `{LANE}/corpus/lessons/round-99-verifier-spotcheck.md`, `{LANE}/plans/round-100.md`,
`{LANE}/corpus/evidence/round100/egress-approval.md`, `{LANE}/corpus/evidence/round57/refetch.tsv` rows S237-S239 and the capture they
name. Gate: one bullet per S237-S239 (URL, access/fetch times, decision, ≤25-word located quote you locate yourself in the capture, or the
refusal reason and flip condition), the S236 used-by change old→new, and "no web search this round". Mistakes: mine ONE mistake class with
class · evidence pointer (path:line) · captured-by (the criterion or rule that should have caught it, or `none`) · fix — and point to the
receipt line that shows the fix able to fail. Candidate: round 99 keyed a guard to a path's spelling while git resolves it semantically
(R99SentinelC1 F-1) — its fix is C1; or round 99's battery crashed instead of reporting SETUP (`before/c1-setup.txt`). Write
`{OUT}/R100ScribeLesson-lesson-draft.md` and `{OUT}/R100ScribeLesson-log-draft.md`. VERDICT trailer: n/a for C1/C2."""),
]

SPEC = {
    "wave": "chousa-r100-w1",
    "reportDir": ".ufo/waves/round-100/w1",
    "context": CONTEXT,
    "items": ITEMS,
}

if __name__ == "__main__":
    out = os.path.join(HERE, "w1-spec.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(SPEC, fh, indent=1)
    print(f"spec {out} items={len(ITEMS)} roles="
          + ",".join(f"{r}={sum(1 for i in ITEMS if i['role'] == r)}" for r in sorted({i['role'] for i in ITEMS})))
