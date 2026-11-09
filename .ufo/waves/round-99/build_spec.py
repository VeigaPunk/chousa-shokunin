#!/usr/bin/env python3
"""Build the round-99 wave-1 spec (12 seats, policy v1 band 8-16). FREEZE is passed on the command line."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
SCRATCH = "/fast/scratch/hyaku/chousa-r99"
BASE = "47ed34fa785288837f84cde9db15c41300854a78"
FREEZE = sys.argv[1] if len(sys.argv) > 1 else "<freeze>"
OUT = f"{LANE}/.ufo/waves/round-99/w1"
ENTRY = "corpus/knowledge/quotation-error-rates-r99.md"

GODSPEED = """/skill:godspeed

You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.
"""

CONTEXT = f"""Lane chousa round 99, L1 ChousaR99 holds the canonical planner seat, the freeze and the integration. Root {LANE}.
Revisions: base {BASE} (round-98 landing); claim freeze F {FREEZE} — the tree you attack.
Frozen claims: {LANE}/.ufo/waves/round-99/claims.md — read it FIRST, with every kill rule and NAMED LIMIT. Machine form:
{LANE}/.ufo/waves/round-99/claims.json. Plan, routes and pre-freeze change P0: {LANE}/plans/round-99.md.
C1 operability: `tools/gate-records.py verify` gains a CHALLENGE check (`is_challenge`, `CHALLENGE_MARKERS` 11 phrases,
`CHALLENGE_MAX_WORDS` 200) on url/admit records and on rev records whose path is `corpus/captures/<24 hex>.txt`. Battery
`python3 -B corpus/evidence/round99/challenge-controls-r99.py --root . --work <scratch>` (~5 s) → `NEG_REFUSED=7/7 POS_ADMITTED=4/4
PROD_REFUSED=4/4 HARM_SAME=25/25 BASE_NEG_ADMITTED=7/7 ORACLES_REJECTED=5/5`, `CHALLENGE_CONTROLS_R99=PASS`; with
`--tool <base tool> --no-oracles` it prints FAIL (receipt corpus/evidence/round99/before/c1-base.txt). Background: round 98 showed the
base gate admits a GATE-RECORD quoting S230's http-200 reCAPTCHA page (corpus/evidence/round98/gate-records-challenge-200.txt,
QUALITY 229); this round S234 (Research Integrity and Peer Review) answered http 200 with a "Client Challenge" page that QUALITY 229's
grep pattern does not match.
C2 coverage: NEW entry {ENTRY} — how often a cited source fails the citing sentence: Jergas & Baethge 2015 via Europe PMC's core
record of PMID 26528420 (S236, tier B, capture corpus/captures/405a0054e1f6dbd1854a3618.txt = the JSON as served; J0 title, J1-J8
abstractText) and Mogull 2017 PLoS One publisher page (S233, tier A, capture corpus/captures/4b70901ad80c513f0c2f750c.txt; G0-G13),
an 8-row decision table. S232 (PeerJ 403), S234 (challenge page), S235 (Europe PMC full text 500) rejected. Counting:
`python3 -B tools/gate-records.py verify --root . {ENTRY}` → `records=25 ok=25 fail=0`; `bash tools/research-gate.sh verify-metadata
{ENTRY} --root .` CLEAN; `python3 -B tools/search-rerun.py verify {ENTRY} --root .` → `rev_match=4/4` CLEAN;
`python3 -B corpus/evidence/round99/entry-controls-r99.py --root .` → `ENTRY_CONTROLS_R99=PASS` (NUMBERS_SOURCED=6/6, FORGERY_REFUSED=10/10).
Receipts: {LANE}/corpus/evidence/round99/before/ (do-nothing controls) and after/ (at F). Approval table for external GETs:
{LANE}/corpus/evidence/round99/egress-approval.md.

Your job is to FALSIFY: find where a claim's stated sentence says more than its instrument enforces, where a quote or a decision
row says more than its source, where the tool or a battery is wrong, unsafe or not new. A finding is worth more than a pass.
Every `Report:` trailer path is relative to {LANE} — write it at {LANE}/<that path>. Copy every receipt you cite into {OUT}/
(name files `<YourSeatName>-*.txt`) before you yield.
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
    item("R99ExecC1Repro", "executor", f"""Reproduce frozen C1 from a clean tree and probe its named limits. `S={SCRATCH}/R99ExecC1Repro`;
shared clone at F. (a) In `$S/repo` run the C1 counting command and the before command (claims.md); paste tallies + exit codes.
(b) Write at least 8 NEW challenge-page fixtures of your own in a scratch lane built like the battery's `Lab` (copy SOURCES.md +
refetch.tsv, add a registry row, a refetch row http 200 and a capture keyed sha256(url)[:24]): Akamai "Access Denied … Reference #",
PerimeterX "Press & Hold to confirm you are a human", DataDome, hCaptcha, Sucuri "Website Firewall", AWS WAF, a Cloudflare page with
200+ words of footer text, a challenge page in another language. Run the F tool on each; table refused/admitted and which named limit
(a)-(d) each admission falls under — an admission outside every named limit is a finding against the C1 sentence. (c) Write 4 real-looking
short documents (≤200 words) that legitimately contain a marker (e.g. a changelog line "fix: recaptcha widget") and show whether they
are refused (named limit (b)). VERDICT trailer required."""),

    item("R99MutantsC1", "mutation-tester", f"""Mutation test of the C1 change. `S={SCRATCH}/R99MutantsC1`; shared clone at F.
Write at least 20 one-site mutants of `tools/gate-records.py` at F on the NEW code: each CHALLENGE_MARKERS entry dropped (11), `<=`→`<`,
200→199/201/1000, `.lower()` dropped, `norm` dropped inside is_challenge, `any`→`all`, `and`→`or`, the admit-branch call removed, the
rev-branch call removed, `CAP_RE.fullmatch`→`True` in the rev branch, CHALLENGE appended only when QUOTE_ABSENT is not. Each mutant must
apply exactly once. Run the battery with `--tool <mutant> --work $S/w/<id>` (oracles are patches of the given tool — use `--no-oracles`
for mutants) and classify KILLED (battery FAIL) / SURVIVED; for each survivor say whether it is equivalent (prove it) or uncovered, and
whether it makes any clause of the C1 sentence false (e.g. "11 frozen markers": does the battery show every marker is live?). Then
mutate the BATTERY itself (≥6 one-site mutants: a NEG verdict test loosened to `rc==1`, POS dropped, HARM compare stdout only, an
oracle site that no longer applies counted as rejected, PROD count 4→2) and report which still print PASS for the F tool and FAIL for
the base tool. Receipts with probe scripts and full outputs. VERDICT trailer required."""),

    item("R99SentinelC1", "sentinel", f"""Bypass and side-effect audit of C1 at F. `S={SCRATCH}/R99SentinelC1`; shared clone at F.
(1) Bypass the CHALLENGE check with S230's or S234's own text: zero-width characters inside a marker, NFKC-variant letters, HTML
entities left in the .txt, padding the capture past 200 words with whitespace-only or punctuation tokens, a capture path written as
`./corpus/captures/…` or with upper-case hex in the rev form, a url/admit record whose capture is a symlink or hardlink. For each:
admitted or refused at F, and which named limit covers it; an uncovered admission is a finding. (2) False refusals in the real store:
run `is_challenge` (import the F tool) over every `corpus/captures/*.txt` at F; list each capture flagged, its words, its marker, and
whether any GATE-RECORD in corpus/knowledge or corpus/lessons cites it. (3) `strace -f -e trace=file,network,process` (or python audit
hooks) the battery and `gate-records.py verify`: any write outside `--work`, socket, or mutating git command? Is the battery's docstring
exact about what it reads and writes? VERDICT trailer required."""),

    item("R99ReviewerC1", "reviewer", f"""Correctness review of the C1 diff at F. `S={SCRATCH}/R99ReviewerC1`; shared clone at F.
Read `git -C $S/repo diff {BASE} {FREEZE} -- tools/gate-records.py` and `corpus/evidence/round99/challenge-controls-r99.py`. Check:
(1) the module docstring's CHALLENGE paragraph matches the code exactly (forms covered, normalization, threshold, marker count); (2) the
marker provenance comment: open the four committed challenge captures (b5b8d050eea0c638e95ba674, 0954149536aaad411000e1fb,
b90988847e704a08aabc8321, 58725f5e0ac436166546a5ec) and confirm which markers each carries; (3) the battery's legs test what claims.md
says (NEG verdict = CHALLENGE as the ONLY code? PROD really on the production path with the lane's own rows? HARM file set = every file
with a GATE-RECORD line?); (4) every oracle is the stated stand-in and fails for the stated reason (run each and read which CASE lines
fail); (5) the before receipt really ran the base tool with the frozen battery; (6) QUALITY 126 (corpus/QUALITY.md): does this
battery meet it, and is named limit (f) the honest residue? Every defect: file:line, command, observed output. VERDICT trailer required."""),

    item("R99ExecC2Repro", "executor", f"""Reproduce frozen C2 from a clean tree and re-derive it independently. `S={SCRATCH}/R99ExecC2Repro`;
shared clone at F. (a) Run the four C2 counting commands; paste tallies + exit codes. (b) Re-run each `## Searches` row yourself at
{BASE}: `git archive {BASE} corpus/captures | tar -x -C $S/base` then `/usr/bin/grep -l -F -e <expr>`; table recorded vs yours.
(c) WITHOUT the lane's scripts, write your own ≤40-line checker: every `## Located quotes` row is in its capture (normalize curly quotes
and whitespace only), J0 is the JSON `title`, J1-J8 lie in `abstractText`, and every number in each Do cell is printed in that row's
warrant quotes; print your tallies and compare with the controls'. (d) Network allowed for these two URLs only, read-only into $S, one
attempt each: {"https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0184727"} and
{"https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:26528420%20AND%20SRC:MED&resultType=core&format=json"} — locate
G4, G10, G11, J2, J3 in your own copies and report sha256 vs refetch.tsv. VERDICT trailer required."""),

    item("R99ReviewerC2", "reviewer", f"""Fidelity review of `{ENTRY}` at F against its sources (kill rule K5). `S={SCRATCH}/R99ReviewerC2`;
shared clone at F. For EACH of the 8 decision rows: do the Do and Never cells say only what the warranting quotes say? Mark faithful /
overreach / misattributed with the exact words that overreach (e.g. "treat an unchecked citation as unreliable" — is that what J5 or G10
says?). Check: the `## What this entry governs` and `## Named limits` sentences against the captures (read the full S233 capture
around each G quote — is any quote's meaning changed by its cut, e.g. G1 "Previous reviews estimated…" is Mogull reporting others, not
Mogull's own estimate?); the tier choices (S233 A publisher page, S236 B index record); the SOURCES.md rows S232-S236 (tier, scope,
anchor, teaches, status, dates, used-by) against refetch.tsv and the capture bytes; the Lane cells' statements about lane tools. Any
overreach is a C2 finding. VERDICT trailer required."""),

    item("R99MutantsC2", "mutation-tester", f"""Mutation test of the C2 instrument. `S={SCRATCH}/R99MutantsC2`; shared clone at F.
Target `corpus/evidence/round99/entry-controls-r99.py`: write at least 14 one-site mutants (e.g. `norm`→identity, the NUM regex losing
`%` or the `,` decimal, NUMBERS reading all warrant text of the table instead of the row's, FIELD `in` instead of `==` for J0,
IDENTITY dropping one field, WARRANTS ignoring the Lane cell, TOPIC case-sensitive, BASE leg inverted, a forgery whose replacement no
longer applies counted as refused, ACCEPT inverted, `passes` accepting n==0) and run each with `--root $S/repo`; KILLED if it prints
`ENTRY_CONTROLS_R99=FAIL` or SETUP. Note forgeries whose `replace` silently changes nothing (the script counts `changed`). Then forge the
ENTRY in 6 ways the controls or `tools/gate-records.py` should refuse but might not (a Do cell that reverses its quote with no number; a
number that appears in a warrant quote but in another sense, e.g. "15" from G9 used as a rate; a J quote that is in `abstractText` but
cut so it reverses meaning). Report survivors and whether any falsifies a C2 sentence. VERDICT trailer required."""),

    item("R99CriticClaims", "critic", f"""Adversarial reading of claims.md (both claims) against the instruments at F.
`S={SCRATCH}/R99CriticClaims`; shared clone at F. For every clause of each claim sentence, name the instrument leg that enforces it, or
show it is unenforced. Build at least two cheap stand-ins per claim that meet the printed tallies without the claimed property and RUN
them through the frozen counters — for C1 e.g. a tool that refuses on the battery's fixture host `fixture.invalid` or S-ids ≥ S900 plus
the two PROD captures' paths (QUALITY 126 detection forgers beyond o4/o5; named limit (f)); for C2 an entry whose quotes and numbers
pass but whose Do cells state the opposite of their warrants. Is C2's axis "coverage" right by AXES.md (a new province surface) or is it
depth? Is the C1 do-nothing control the cheapest one that skips the work? Are the claims causally separable as claims.md says (run C2's
gate with the BASE tool; run C1's battery without C2's files)? VERDICT trailer required."""),

    item("R99ScoutSources", "scout", f"""Source re-open and frontier scout. `S={SCRATCH}/R99ScoutSources`. Network allowed ONLY for the URLs named
here, read-only, into $S (never corpus/captures or refetch.tsv), at most 2 attempts each:
https://peerj.com/articles/1364/ ; https://www.ebi.ac.uk/europepmc/webservices/rest/PMC4627914/fullTextXML ;
https://researchintegrityjournal.biomedcentral.com/articles/10.1186/s41073-025-00173-z ;
https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:10.1186/s41073-025-00173-z&resultType=core&format=json .
(1) For each: http status, bytes, whether the body is the document or a challenge page (and which CHALLENGE_MARKERS it carries).
(2) If the 2025 update's Europe PMC record answers, report its pmid/pmcid, title and the abstract's pooled rates, quoted ≤25 words each,
and whether they contradict anything in {ENTRY}. (3) Web search only (no fetch) for other reachable routes to Jergas & Baethge 2015's
full text (author manuscript, institutional repository) — leads with URLs. VERDICT trailer required (n/a allowed)."""),

    item("R99RevenPrior", "revenger", f"""Is each claim new, and why did the prior rule miss S234? `S={SCRATCH}/R99RevenPrior`; shared clone at F.
(1) At BASE, run QUALITY 229's check (corpus/QUALITY.md criterion 229, its grep pattern) over every `corpus/captures/*.txt` at F: which
challenge captures does it list, and which does it miss (S234 `b90988847e704a08aabc8321`)? Classify every capture of ≤300 words at F as
document / challenge page by reading it. (2) At BASE, did any lane instrument (tools/*.py, tools/research-gate.sh, any battery under
corpus/evidence/) refuse a GATE-RECORD quoting a challenge capture? Show the command. (3) At BASE, does any lane file hold quotation-error
rates (`git -C $S/repo grep -n -i -E 'quotation (error|accura)|misquot|citation error' {BASE} -- corpus tools SKILL.md`)?
(4) Round-98 spot-check routed defect 2 (R98MutantsC1 survivor R32, verify-line whitespace): re-run R32 from
`.ufo/waves/round-98/w1/` against the F tool and the round-95 battery; is it caught anywhere? Propose the next-round rule. VERDICT trailer
required (n/a allowed)."""),

    item("R99ConnectorSiblings", "connector", f"""Cross-lane pattern scan, read-only. `S={SCRATCH}/R99ConnectorSiblings`.
Scan sibling lane repos under /home/vgpnk/Projects/shokunin/*-shokunin (read-only: `git -C <repo> grep`, no writes) for (a) any rule or
tool that refuses challenge/interstitial pages in captured sources (marker lists, size thresholds, raw-HTML checks such as
`<title>Just a moment`, `cf-chl`, `g-recaptcha`) and how it handles false refusals, (b) knowledge on citation/quotation accuracy,
claim-vs-source support checks, or reading a paper through an index record. For each match: path, revision, one-line relevance, and
whether chousa's C1/C2 contradicts, duplicates or should adopt it. Route, do not absorb. VERDICT trailer: n/a allowed."""),

    item("R99ScribeLesson", "scribe", f"""Draft the round-99 lesson's `## Gate` and `## Mistakes` sections and a LOG.md entry draft. Read
`{LANE}/corpus/lessons/round-98.md`, `{LANE}/corpus/lessons/round-98-verifier-spotcheck.md`, `{LANE}/plans/round-99.md`,
`{LANE}/corpus/evidence/round99/egress-approval.md`, `{LANE}/corpus/evidence/round57/refetch.tsv` rows S232-S236 and the captures they
name. Gate: one bullet per S232-S236 (URL, access/fetch time, decision, ≤25-word located quote you locate yourself in the capture, or
the refusal reason and flip condition), plus the web-search query. Mistakes: mine ONE mistake class with class · evidence pointer
(path:line) · captured-by (the criterion or rule that should have caught it, or `none`) · fix — and point to the receipt line that
shows the fix able to fail. Candidate: QUALITY 229's check lists only challenge wordings already seen, so S234's "Client Challenge"
page passes it (run its command yourself at F and paste the output). Write `{OUT}/R99ScribeLesson-lesson-draft.md` and
`{OUT}/R99ScribeLesson-log-draft.md`. VERDICT trailer: n/a for C1/C2."""),
]

SPEC = {
    "wave": "chousa-r99-w1",
    "reportDir": ".ufo/waves/round-99/w1",
    "context": CONTEXT,
    "items": ITEMS,
}

if __name__ == "__main__":
    out = os.path.join(HERE, "w1-spec.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(SPEC, fh, indent=1)
    print(f"spec {out} items={len(ITEMS)} roles="
          + ",".join(f"{r}={sum(1 for i in ITEMS if i['role'] == r)}" for r in sorted({i['role'] for i in ITEMS})))
