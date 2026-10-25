#!/usr/bin/env python3
"""gen-w2-spec.py — build the round-45 chousa wave-2 spec (falsify, v1 band 32-64).

Every item attacks one thing wave 1 produced, measured over the committed
landing 5e8c7ad2f7b8254d83358820286e3d12ca4672d1. Seats are read-only toward
the lane; counters run inside a `git archive` extraction under /tmp.
"""
import json
import pathlib

LANE = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
TIP = "5e8c7ad2f7b8254d83358820286e3d12ca4672d1"
OUT = pathlib.Path(LANE) / ".ufo/waves/round-45/w2-spec.json"
EV = f"{LANE}/corpus/evidence/round45"
QC = "/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache"
PKG = "/home/vgpnk/Projects/shokuknow/merge/chousa"
W1 = f"{LANE}/.ufo/waves/round-45/w1"

DIRECTIVE = """You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls."""

TREE = (f"Measure over committed bytes: `mkdir -p /tmp/chousa-r45-<YourName>/tree && git -C {LANE} archive {TIP} | tar -x -C /tmp/chousa-r45-<YourName>/tree` "
        f"and run every counter from inside that tree (cd into it), never inside {LANE} — some older counters rewrite receipts in the tree they run in.")

CONTEXT = f"""# Goal
chousa lane (deep-research method: claim-vs-source verification, source hierarchy, citation chaining), round 45, wave 2 — FALSIFY. Wave 1 built; the L1 landed the work at lane commit {TIP}. Your job is to attack exactly one item that wave 1 or the L1 produced and report whether it holds. Frozen claims: {EV}/claims.md (frozen at d82cec904bf0fb8736886b9f17be913c7807427a) — never propose changing a predicate, a counter or a target; a defect you find is reported, not fixed.
- C1 operability: tools/parent-lifetime.sh exit contract; counter corpus/evidence/round45/c1-count.py (target CASES_MATCH=5/5).
- C2 calibration: every committed gate entry point named in a SKILL.md Gates row; counter corpus/evidence/round45/c2-count.py --list (target UNREGISTERED=0). Twelve rows were added in `## Gates` of SKILL.md this round (rounds 31-34 v1/v2/v3, 40, 41, quarantine-check r42, absent-split r43, 44, 45, parent-lifetime, tag-count).
- C3 depth: corpus/knowledge/evidence-archive-field-policy-r41.md and corpus/knowledge/evidence-snapshot-coverage-r40.md adopted as rows S082 (AVeriTeC README), S083 (arXiv 2305.13117v3), S084 (AVeriTeC train.json) in corpus/SOURCES.md; spans in corpus/evidence/round45/spans/ + spans.tsv; counts in corpus/evidence/round45/counts.json; counter corpus/evidence/round45/c3-count.py (default and --lane-only).
- Also landed: QUALITY 64 (round tag; check corpus/evidence/round45/tag-count.py) and 65 (archive coverage counted by value) in corpus/QUALITY.md; lesson corpus/lessons/round-45.md; coverage-map rows at the end of corpus/README.md.
Wave-1 reports: {W1}/. Captures (on disk, read-only; file = sha256(url)[:24] + '.txt'): {QC}. Staged package (read-only): {PKG}.

# How to measure
{TREE}

# Seat contract
- Every seat is a leaf: do not spawn, dispatch or create background work. The only exception: an executor may spawn one read-only `labrat` probe for one falsifiable hypothesis.
- Write ONLY your own report file. Every `Report:` trailer path is relative to {LANE} — write it at {LANE}/<that path>. Your tools start at the fleet root /home/vgpnk/Projects/shokunin, so a relative path lands in the WRONG repo: always write the absolute path {LANE}/.ufo/waves/round-45/w2/<YourName>.md.
- Never modify lane files, the lane git index or jj state (no git add/commit/stash/checkout/reset, no mutating jj), the fleet repo /home/vgpnk/Projects/shokunin (including .ufo/state and .scratch), any sibling lane, or anything under /home/vgpnk/Projects/shokuknow (read-only; never run its tools renumber-staged.py, merge-plan.py, quote-lint.py, absent-defect-register.py).
- Scratch only under /tmp/chousa-r45-<YourName>/; delete it before you finish.
- NO external live-target fetches and no network egress (fetch-scope L0 8d77e6c1 is open). A dispatch item is NOT an operator approval; report a needed live read as a finding.
- Tooling authorization (operator, 2026-10-19): you may install or upgrade tools that help the task — read /home/vgpnk/.omp/agent/RULES.md first, official channels only, record tool/version/channel/reason. pacman guard: all pacman transactions are PAUSED host-wide — never run pacman -S, -Sy, -Syu, -U or -R; use uv tool / npx / an official binary in ~/.local/bin, or report the need.
- Routing is the host role table (~/.omp/agent/config.yml, operator-owned, read-only). Never pass or hardcode a model. The planner seat is the L1.
- Never message agent://all. Report: the item, every command with verbatim decisive output, a verdict (holds / fails / holds-narrowed, with the exact defect), and resolvable pointers (path:line, char offset, sha256). Never assert a result you did not run. Under 120 lines."""


def row(name, label, extra=""):
    return (name, "reviewer",
            f"Attack the SKILL.md Gates row whose name cell is {label} (in `## Gates` of {LANE}/SKILL.md at {TIP}). Re-run every command its entry cell names, inside the archive tree, and compare each value in its verdict map and self-test cell with what you observe; open every path its pinned-values cell cites and confirm it exists at {TIP}. {extra} Report per cell: holds / wrong (quote the row text and the observation). Also confirm the row has exactly 8 cells.")


ITEMS = [
    row("RevRowR31", "`research-gate round-31 counters`"),
    row("RevRowR32", "`research-gate round-32 v1 counters`", "Confirm the supersession sentence names real successor files."),
    row("RevRowR33", "`research-gate round-33 C1 v1/v3 counters`", "Confirm the supersession sentence names real successor files."),
    row("RevRowR34", "`research-gate round-34 v1/v2 counters`", "These counters can take ~30 s each; run with LC_ALL=C."),
    row("RevRowR40", "`research-gate round-40 counters`", "The row says C1 currently prints 2/6 in a worktree because of gate-sha drift (R40-W2); check what it prints inside the archive tree of the tip, and whether the row states that honestly."),
    row("RevRowR41", "`research-gate round-41 counters`", "Its C1 rewrites corpus/evidence/round41/receipts/cells/ in the tree it runs in — run it ONLY inside the archive tree and confirm that write scope is what the row's write-scope cell says."),
    row("RevRowQuarantine", "`` `quarantine-check` round-42 gates ``"),
    row("RevRowAbsentSplit", "`` `absent-split` (round 43) ``"),
    row("RevRowR44", "`` `research-gate round-44 counters` ``", "Check the D1 sentence (c3 reads an untracked campaign capture path)."),
    row("RevRowR45", "`` `chousa round-45 counters` ``"),
    row("RevRowLauncher", "`` `parent-lifetime` (r44; exit contract r45) ``", "Read tools/parent-lifetime.sh at the tip and check every exit code the row states against the code paths."),
    row("RevRowTagCount", "`` `tag-count` (QUALITY 64, r45) ``"),
    ("ExecRerunC1", "executor", f"Re-run the C1 counting command `python3 corpus/evidence/round45/c1-count.py` inside the archive tree three times and paste each output; then run it with `--tool` pointing at the round-44 blob (`git -C {LANE} show 79ee8f2942802ee1d1771a7e5887a7a9a36cdb8b > /tmp/chousa-r45-ExecRerunC1/r44.sh`) and confirm the committed control {EV}/controls/c1-control-r44-tool.txt is reproduced byte-for-byte (diff). Verdict on C1's target CASES_MATCH=5/5."),
    ("ExecRerunC2", "executor", f"Re-run `python3 corpus/evidence/round45/c2-count.py --list` inside the archive tree and paste it; then rebuild the base tree (`git -C {LANE} archive d29bf47d94149a1b71581eeb0f36d9ff22d41da3`) and run the tip's c2-count.py with `--root <base tree>` and diff against {EV}/controls/c2-control-base.txt. Independently enumerate the entry-point set with your own find/ls command and compare with ENTRY_POINTS=54. Verdict on C2's target UNREGISTERED=0."),
    ("ExecRerunC3", "executor", f"Re-run `python3 corpus/evidence/round45/c3-count.py` and `python3 corpus/evidence/round45/c3-count.py --lane-only --cache /nonexistent` inside the archive tree; then the do-nothing control: run the tip's c3-count.py with `--root` pointed at a base-tree archive (d29bf47d…) and compare with {EV}/controls/c3-control-do-nothing.txt. Verdict on C3's two targets."),
    ("MutLauncherPatched", "mutation-tester", f"Wave 1's launcher mutants were built from the PRE-fix tool and were inconclusive. Build four mutants of the LANDED tools/parent-lifetime.sh (from the archive tree), each breaking one C1 case: exit 0 on zero tasks; no timeout_s in the start line; --timeout optional with a default; exit 0 on a timed-out seat. Run `python3 corpus/evidence/round45/c1-count.py --tool <mutant>` on each; every mutant must score <5/5 and exit 1. Also run the pristine landed tool (must be 5/5). Report survivors."),
    ("MutLauncherEdges", "mutation-tester", f"Probe the LANDED tools/parent-lifetime.sh (archive tree) with a stub `kimi` first on PATH (copy the stub from corpus/evidence/round45/c1-count.py): dispatch file that is not JSON; stub exiting 1 (a failed seat, not a timeout); a seat killed by SIGKILL (exit 137, e.g. --timeout 1 with a stub that traps TERM); --timeout 0 and --timeout abc; --selftest with and without --timeout. For each: exit code and receipt lines. Compare with the header contract at the top of the tool; report any behaviour the header misstates."),
    ("MutC2RowRemoval", "mutation-tester", f"In a scratch copy of the archive tree, delete each of the twelve rows added this round to `## Gates` in SKILL.md one at a time (they are the rows from `research-gate round-31 counters` through `tag-count`, placed after the `mechanism-witness` row) and run `python3 corpus/evidence/round45/c2-count.py --root <copy> --list`. Report, per row, which paths become unregistered; flag any row whose removal changes nothing (duplicate authority) and any path registered by two new rows."),
    ("MutC3Entries", "mutation-tester", f"In scratch copies of the archive tree, mutate the ADOPTED entries and run `c3-count.py --root <copy>` (default mode, cache = the real {QC}): remove one of the four quotes from evidence-archive-field-policy-r41.md; change `1,386` to `1,387` everywhere in evidence-snapshot-coverage-r40.md; swap the URLs of the two `source:` lines in the field-policy entry; change S084's row status to `queued`. Each must fail; report survivors and which count catches each."),
    ("RevSourceS082", "reviewer", f"Attack lane row S082 in corpus/SOURCES.md at {TIP}: confirm 11 cells and no pipe inside a cell; locate its anchor quote in the README capture {QC}/ce16d57277fedfd4f0e7750e.txt (char offset by Python str.find, word count <= 25); judge whether its teaches cell is supported by the capture and does NOT claim more than the README says (e.g. any cause for an empty claim archive). Verdict per cell."),
    ("RevSourceS083", "reviewer", f"Attack lane row S083 in corpus/SOURCES.md at {TIP}: confirm 11 cells; locate its anchor quote in the paper capture {QC}/412b146a2720ce6557268d05.txt (str.find offset, <= 25 words); check every factual clause of its teaches cell (evidence pages cached; claim URLs 'not said to be'; annotation guideline 8 and the 404) against the capture. Search the capture for any sentence saying claim URLs ARE archived (archive.org, cached, Wayback near 'claim'); if one exists the row over-claims."),
    ("RevSourceS084", "reviewer", f"Attack lane row S084 in corpus/SOURCES.md at {TIP}: recount from {QC}/974299ae4b5f3bdb808b36a9.txt with your own code every figure in its anchor and teaches cells (3,068; 7,572 answers naming a real source = source_url non-empty and not 'Metadata'; 5,959 web.archive.org; 1,491 real-source answers with no cached_source_url key; 1,145 of 2,531) and confirm the capture sha256. Verdict per figure."),
    ("CritEntryFieldPolicy", "critic", f"Attack every Observation and Inference bullet of {LANE}/corpus/knowledge/evidence-archive-field-policy-r41.md (at {TIP}) against the README capture {QC}/ce16d57277fedfd4f0e7750e.txt and the paper capture {QC}/412b146a2720ce6557268d05.txt. For each bullet: supported / over-reads / wrong, with the capture text. Specifically test: 'It says nothing of caching claim URLs'; 'its one Where possible is the annotator guideline on extractive answers'; the guideline-8 location (Appendix J.4.1); and whether 'a filled archive field is a link, not proof that the archived capture resolves' is grounded or rhetoric."),
    ("CritEntrySnapshot", "critic", f"Attack every figure and inference of {LANE}/corpus/knowledge/evidence-snapshot-coverage-r40.md (at {TIP}). Recount each figure yourself from {QC}/974299ae4b5f3bdb808b36a9.txt with your own code (state your rules: what counts as empty, as a web.archive.org link, as 'real source'). Test the inference 'the missing snapshots sit in answers that lack the field and among filled values that are not archive links' and the arithmetic sentences (99.98%, 45.2%, 78.7%, factor about 2, more than three orders of magnitude). Verdict per sentence."),
    ("ExecExtraCounts", "executor", f"Independently recount, with your own code (do not import corpus/evidence/round45/build-spans.py), every key of `extra_not_frozen` and `counts` in {EV}/counts.json at {TIP} from {QC}/974299ae4b5f3bdb808b36a9.txt; diff your values against the file. Then re-run `python3 corpus/evidence/round45/build-spans.py <scratch-root>` (it takes the lane root as argv[1]; give it a scratch root containing an empty corpus/evidence/round45/ directory) and diff its outputs against the committed spans.tsv, spans/ and counts.json."),
    ("RevSpans", "reviewer", f"For each row of {EV}/spans.tsv at {TIP}: compute sha256 of the capture named sha256(url)[:24].txt in {QC} and compare with the row; read the span file and check capture_text[offset:offset+len(span)] == span (Python, utf-8 text, char offsets); check the quote is inside the span and appears exactly once in the capture; check the quote appears verbatim in the citing entry. Verdict per row."),
    ("ScoutRenumberMap", "scout", f"Re-check the by-document binding at {TIP}: for each line of {LANE}/.ufo/waves/round-45/assimilation/renumber-map.tsv, confirm the staged row's URL in {PKG}/SOURCES.append.md equals the map URL and equals the URL in the lane row; re-run the 0-3-space id-collision extraction on the lane registry at the tip and the staged append (the collision set must now be exactly the adopted lane ids S082-S084, which is expected and is NOT a defect because they bind by URL — say so explicitly) and confirm the committed pre-append `collisions` file is empty."),
    ("RevCensusMirror", "reviewer", f"Re-run `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file {LANE}/.ufo/waves/round-45/assimilation/validate/corpus/SOURCES.md` and `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa`; paste both with exit codes. Diff the three S082-S084 lines between the mirror and the live registry {LANE}/corpus/SOURCES.md. Confirm no E03/E04 and that the registry has 84 rows (count with the 0-3-space pattern)."),
    ("CritRejectDecision", "critic", f"Attack the round's one reject (lesson {LANE}/corpus/lessons/round-45.md `## Gate`): the staged evidence-pool-versioning-r39-amendment-2026-10-23.md. Was it refused for a sound reason, or could its AVeriTeC dataset-page and AVerImaTeC quotes have been adopted as a third entry on the same theme? Locate its quotes in {QC} (cache names = sha256 of https://fever.ai/dataset/averitec.html and https://arxiv.org/html/2505.17978v2, first 24 hex) and report located/absent. Verdict: reject sound / reject over-cautious (give the reason) / reject wrong."),
    ("CritCoverageGround", "critic", f"Attack the claim that the two adopted entries are ground the lane did not hold: grep {LANE}/corpus/knowledge/ and {LANE}/corpus/README.md at {TIP} for prior coverage of archive links in verification corpora, AVeriTeC, FEVER evidence binding, Memento, cached copies (citation-version-binding-r36/r37, revision-binding-r31, claim-verification-r2). State what is new and what duplicates held ground, and whether the two new coverage-map rows overstate."),
    ("CritLessonMistakes", "critic", f"Attack each of the six `## Mistakes` items in {LANE}/corpus/lessons/round-45.md at {TIP}: does its evidence pointer resolve (open it), is captured-by honest, is the fix real and is it shown able to fail as stated? Also check the D1-D6 disposition table against {LANE}/corpus/lessons/round-44-verifier-spotcheck.md. Verdict per item."),
    ("RevQuality64", "reviewer", f"Attack QUALITY 64 in {LANE}/corpus/QUALITY.md and its check corpus/evidence/round45/tag-count.py at {TIP}: reproduce the control `--from 35 --to 44` (TAGGED=0/22, exit 1) and diff with {EV}/controls/tag-control-r35-r44.txt; independently count claim rows in SCORECARD.md round sections 35-44 by your own method; build two forges in scratch (a `ground` word inside a longer cell; a tag on a non-claim row) and report whether the check is fooled."),
    ("RevQuality65", "reviewer", f"Attack QUALITY 65 in {LANE}/corpus/QUALITY.md at {TIP}: verify each figure in its 'shown able to fail' sentence (5,959 of 6,510; 429 Metadata; 1,582 sourced answers without a key) against {EV}/counts.json and a recount from {QC}/974299ae4b5f3bdb808b36a9.txt; confirm the staged sentence it quotes exists verbatim in {PKG}/knowledge/corpus/knowledge/evidence-snapshot-coverage-r40.md. Judge whether 65 is a checkable criterion or a slogan."),
    ("CritC1Admission", "critic", f"Judge C1 for admission: improved with no harm? Read the landed tools/parent-lifetime.sh and corpus/evidence/round45/parent-lifetime.diff at {TIP}. Attack: (1) selftest mode now records timeout_s=0 — is that honest or misleading; (2) removing the `set +e`/`set -e` toggles around `wait` — does any later command now behave differently; (3) does any committed lane doc still say 'Exit 0 when the end line is written' or default 420 (grep the lane at the tip); (4) do the round-44 receipts still verify (run corpus/evidence/round44/c1-count.py in the archive tree)."),
    ("CritC2Admission", "critic", f"Judge C2 for admission: did it land by row padding? Sample five of the twelve new Gates rows and check each verdict map's PASS labels against the counter's actual print strings (grep the counter source for each label). Check that no new row registers a path while describing a different gate. State whether C2's calibration verdict should be improved, unchanged or harmed, and why."),
    ("CritC3Axis", "critic", f"Judge C3 for admission and axis naming (round-prompt rule: name the axis by the surface the round changes; a coverage/depth claim names the surface it moves and the command that would show it unmoved). Is 'depth' right, or is this coverage? Could a junk-row commit pass the default mode (try to describe the cheapest forge that would)? Is the do-nothing control truly a control the claimed work skips?"),
    ("SentScopeAudit", "sentinel", f"Scope audit: `git -C {LANE} diff --name-status d29bf47d94149a1b71581eeb0f36d9ff22d41da3 {TIP}` — every path must sit inside the lane; flag any deletion or any change outside corpus/, tools/, SKILL.md, .ufo/waves/round-45/. Then `git -C /home/vgpnk/Projects/shokunin status --porcelain` and `ls /home/vgpnk/Projects/shokunin/.ufo/waves/ 2>/dev/null` — report any file naming chousa or round-45 outside the lane (misroot) without touching it. Also confirm `git -C /home/vgpnk/Projects/shokuknow status --porcelain` shows no change caused by this round."),
    ("ScoutWave1Ledger", "scout", f"Account wave 1: read {LANE}/.ufo/waves/round-45/w1/swarm-registry.json and list the 46 members; confirm each has a report file under {W1}/ at {TIP} (`git -C {LANE} ls-tree -r --name-only {TIP} .ufo/waves/round-45/w1/`); count dead seats (no report); identify any seat whose report says it wrote outside its report (e.g. restored a lane file) and quote it. Produce the seat-role mix table."),
]


def main():
    items = [{"name": n, "role": r, "item": DIRECTIVE + "\n\n" + t} for n, r, t in ITEMS]
    spec = {
        "wave": "chousa-r45-w2",
        "milestone": f"Round 45 wave 2 (falsify): attack every Gates row, counter, source row, span, entry, criterion and the reject that wave 1 and the L1 landed at {TIP}; no fetch, no lane writes",
        "reportDir": ".ufo/waves/round-45/w2",
        "axes": ["operability", "calibration", "depth"],
        "context": CONTEXT,
        "items": items,
    }
    OUT.write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding="utf-8")
    roles = {}
    for i in items:
        roles[i["role"]] = roles.get(i["role"], 0) + 1
    print("wrote", OUT, len(items), "items", roles)


if __name__ == "__main__":
    main()
