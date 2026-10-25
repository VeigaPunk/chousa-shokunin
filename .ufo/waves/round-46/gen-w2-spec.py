#!/usr/bin/env python3
"""gen-w2-spec.py — round-46 chousa wave 2 (falsify), v1 band 32-64.

Every item attacks one landed artifact of round 46 at commit d09fc8e7 and names
what it attacks. Seats are read-only toward production files.
"""
import json
import pathlib

LANE = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
OUT = pathlib.Path(LANE) / ".ufo/waves/round-46/w2-spec.json"
EV = f"{LANE}/corpus/evidence/round46"
QC = "/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache"
LAND = "d09fc8e7e2972e30e5e0aaa6e404c97aa0b9f95a"
BASE = "corpus/knowledge/evidence-pool-versioning-r39.md"
AMEND = "corpus/knowledge/evidence-pool-versioning-r39-amendment-2026-10-23.md"

DIRECTIVE = """You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls."""

CONTEXT = f"""# Goal
chousa lane (deep-research method), round 46, **wave 2 — falsify**. Everything attacks what landed at lane commit `{LAND}` (the round-46 landing; the frozen claims are at `c2f0e9d1`, `{EV}/claims.md`). Read the frozen claims first; a predicate, counter target or kill rule is NOT yours to change — report a disagreement, do not re-scale a target.

Three frozen claims: C1 operability (`tools/inference-ground.py` exits 0 on every positive-*.md and 1 on every junk-*.md fixture of `{LANE}/corpus/fixtures/inference-ground-r46/`; counter `{EV}/c1-count.py`; fixtures are byte-pinned in the counter). C2 calibration (every committed gate entry point — tools/*, the round-45 counter pattern, and every existing *.py/*.sh named in SCORECARD.md or a claims file — named in a `## Gates` row of SKILL.md; counter `{EV}/c2-count.py --list`; after: `ENTRY_POINTS=72 REGISTERED=72/72 UNREGISTERED=0`). C3 depth (two adopted entries `{BASE}` and `{AMEND}`, rows S085–S089, eleven spans in `{EV}/spans.tsv` each an exact capture slice with 80 chars of context either side; counter `{EV}/c3-count.py` and `--lane-only`).

Known and already reported by wave 1 (do not re-report as new): the tool checks citation and token PRESENCE, not that the inference follows (`CritC1Attack`); the C2 set is mention-based, not dependence-based (`CritC2Framing`); `junk-borrowed.md` dies on invented tokens rather than on a wrong inference. Attack the CURRENT bytes and find what wave 1 did not.

# Sources (read-only, no fetch)
On-disk captures: S085 `{QC}/5a631adb18988a1a2421ce75.txt`, S086 `{QC}/1c15b611118dee97e4105fcf.txt`, S087 `{QC}/7800e2e1e2df3bc124b6b83e.txt`, S088 `{QC}/b73f7e8dd5b0ace740e48046.txt`, S089 `{QC}/78761b633aee2289e5874ce9.txt`. Lane: `{LANE}/corpus/SOURCES.md`, `{LANE}/SKILL.md` (`## Gates`), `{LANE}/corpus/README.md`, `{LANE}/corpus/evidence/round46/` (claims, counters, controls, spans, measure-after.txt), `{LANE}/.ufo/waves/round-46/w1/` (32 wave-1 reports), `{LANE}/corpus/lessons/round-46.md`, `{LANE}/SCORECARD.md`, `{LANE}/LOG.md`.

# Seat contract
- Leaf seat: no spawning, no background work. An executor may spawn one read-only `labrat` probe.
- Write ONLY your own report. Every `Report:` trailer path is relative to {LANE} — write it at {LANE}/<that path>. Never write anywhere else: no lane production file, no lane git index or jj state (no git add/commit/stash/checkout/reset, no mutating jj), no fleet repo /home/vgpnk/Projects/shokunin (including .ufo/state and .scratch), no sibling lane, nothing under /home/vgpnk/Projects/shokuknow (read-only; never run its tools).
- Scratch under /tmp/chousa-r46w2-<YourName>/; delete it before you finish. Where an item needs a mutation of lane bytes, copy the tree to /tmp with `git -C {LANE} archive {LAND} | tar -x -C /tmp/...` or `cp -r`, and mutate the COPY.
- Absolute paths only; your tools start at the fleet root.
- NO network egress of any kind (fetch-scope L0 8d77e6c1 open). A dispatch item is not an operator approval.
- Tooling: reading /home/vgpnk/.omp/agent/RULES.md is required before an INSTALL only; pacman is PAUSED host-wide (never -S/-Sy/-Syu/-U/-R). Use uv tool / npx / ~/.local/bin, or report the need.
- Routing is the host role table (operator-owned, read-only). Never pass a model.
- Never message agent://all. Report: the item, every command with its verbatim decisive output, your verdict, resolvable pointers (path:line, char offset, sha256). Never assert an unrun result. Keep it under 130 lines."""


def it(name, role, text):
    return (name, role, text)


ITEMS = [
    # C1 attacks (8)
    it("RevRerunC1", "reviewer", f"Re-run C1 over a `git archive` of `{LAND}` extracted to /tmp: `python3 corpus/evidence/round46/c1-count.py --root <tree>`. Paste output and exit code, plus the sha256 of the counter and of all six fixtures and the tool; confirm each fixture hash equals the PINNED value in the counter (read `PINNED` and compare by script). Verdict: re-derived / diverged."),
    it("RevC1Pin", "reviewer", f"Attack the fixture pinning: in a /tmp copy of the archive, change ONE byte of `corpus/fixtures/inference-ground-r46/positive-a.md` and run the counter; then delete one junk fixture and run again; then restore. Report `FIXTURES_CHANGED=` lines and exit codes, and whether the kill rule's 'fixture set changed after the freeze' clause is now enforced. Also check whether the PINNED dict can be bypassed by passing `--root` at a tree whose fixtures hash-collide (impossible in practice — say why)."),
    it("MutC1More", "mutation-tester", f"Four new mutants on /tmp copies: (1) a fenced `- ` bullet after the real bullet (was a survivor in wave 1 — is it killed now?); (2) `#### Inference` with only prose and no bullets (`INF_NO_BULLETS`); (3) a bullet whose only numeral is a 2-digit figure inside a 3-digit span; (4) an entry with TWO Inference sections (does the first or the last win?). Paste exit codes and findings; name any survivor."),
    it("MutC1Tool", "mutation-tester", f"Mutate `{LANE}/tools/inference-ground.py` in /tmp: (a) drop the `--registry` leg; (b) drop the section-end break; (c) accept any non-empty cited set without checking spans; (d) skip the counts leg. Run `python3 {EV}/c1-count.py --root <tree> --tool <mutant>` for each. Report which fixture/mutation pair kills each mutant; any mutant that still scores 3/3+3/3 is a hole in C1's fixture coverage — name it precisely."),
    it("CritC1D7", "critic", f"Characterise the residual exactly. Build the strongest class-(c) body you can that the tool accepts: correct spans, correct figures, wrong inference (the round-45 D7 class). Report the body, its exit code, and the narrowest true sentence for what the tool enforces. Then state whether C1's SCORECARD row and Gates row describe that sentence or overclaim, quoting them from `{LANE}/SCORECARD.md` and `{LANE}/SKILL.md`."),
    it("RevC1Line", "reviewer", f"Compare three texts for the same rule: the docstring of `{LANE}/tools/inference-ground.py` (its numbered rule), the frozen sentence in `{EV}/claims.md` R46-C1, and the `inference-ground` Gates row in `{LANE}/SKILL.md`. List every place they disagree (the registry leg, numeral extraction, fences, bullets=0, exit codes). Verdict per disagreement: docstring wins / claims wins / row must be corrected — propose the corrected cell text only."),
    it("SentC1Path", "sentinel", f"Re-test the span-path boundary in `{LANE}/tools/inference-ground.py`: on a /tmp manifest, try (a) an absolute span_file, (b) `../` , (c) a symlink inside the spans dir pointing outside, (d) a span_file that is a directory. Report exit codes and whether any reads outside the manifest directory. Also probe `--json /etc/...` (write scope) and state whether the declared read-only scope in the Gates row is accurate."),
    it("RevC1Controls", "reviewer", f"Re-run both control receipts verbatim from `{EV}/controls/c1-controls.txt` and `c1-before.txt` (always-exit-0 forge and citation-presence-only forge against the before tree `git archive 6e2630a6` + this round's counters/fixtures). Paste actual vs recorded lines; report any drift, including the counter revision you used."),
    # C2 attacks (6)
    it("RevRerunC2", "reviewer", f"Re-run C2 over a `git archive` of `{LAND}`: `python3 corpus/evidence/round46/c2-count.py --root <tree> --list`. Paste output/exit. Then re-enumerate the entry-point set with your own script (do not import the counter) and compare set-for-set; report every difference with its cause."),
    it("RevC2Rows", "reviewer", f"Judge five of the new Gates rows for truth, not membership: run the `entry` command of `round24–27 counting instruments`, `round33–34 census instruments`, `qr-harness`, `inference-ground` and `chousa round-46 counters` once each (read-only; omit options that write) and compare the real output with the row's verdict-map cell. Report each row: true / wrong cell (quote both) / unverifiable."),
    it("MutC2More", "mutation-tester", f"Attack the hardened C2 with four new forges on /tmp SKILL.md copies: (a) a valid 8-cell row inside a `<!-- -->` comment that also has a `|` inside it; (b) a row naming a path with a trailing `;` and a row with the path inside a Markdown link `[x](path)`; (c) an indented (4-space) row; (d) a row inside a fence that is opened before `## Gates` and never closed. Report REGISTERED/UNREGISTERED and whether each forge is refused."),
    it("CritC2Scope", "critic", f"Attack what `UNREGISTERED=0` means. Enumerate every executable under `corpus/evidence/`, `tools/` and `.ufo/waves/` that a round's receipt depends on but that the frozen set does not contain (start from `{LANE}/.ufo/waves/round-46/w1/CritC2Framing.md` residual list and verify each yourself). State the count, give the paths, and judge whether the SCORECARD row's wording (read it) overstates the property. Propose the one-sentence limit the row should carry."),
    it("RevC2TagCount", "reviewer", f"Verify the invisible-gate finding: (1) confirm `corpus/evidence/round45/tag-count.py` has a Gates row; (2) in a /tmp copy delete that row and run C2 — does `UNREGISTERED` stay 0 while a real gate becomes unregistered? (3) run `python3 corpus/evidence/round45/tag-count.py` and report `TAGGED=k/n` for the default range. State the consequence for C2's claim in one sentence."),
    it("RevC2Before", "reviewer", f"Re-derive C2's before-state on three trees: (A) bare `git archive 6e2630a6` + only `corpus/evidence/round46/*count.py` copied in; (B) bare archive + the whole `round46` dir; (C) bare archive alone. Paste `ENTRY_POINTS/REGISTERED/UNREGISTERED` for each and check which tree `{EV}/controls/c2-before.txt` actually labels 'tree A' and 'tree B'. Report any mislabel as a defect with the corrected lines."),
    # C3 attacks (8)
    it("RevRerunC3", "reviewer", f"Re-run both C3 modes over a `git archive` of `{LAND}`: default and `--lane-only`. Paste outputs and exit codes, plus `python3 corpus/evidence/round46/build-spans.py --check`. Report any leg that differs from `{EV}/measure-after.txt`."),
    it("RevC3Spans", "reviewer", f"Re-derive all 11 spans yourself from the captures: for each row of `{EV}/spans.tsv`, check capture sha256, that the span file is exactly capture[offset:offset+len], that the quote sits inside the span, and that the span carries context on both sides (report the context chars before and after each quote). Report per-row and any row where the span is byte-identical to the quote (the wave-1 M1 class)."),
    it("RevC3Rows", "reviewer", f"Judge the five new Registry rows S085–S089 for truth: for each, re-open the capture, confirm the `anchor` cell's quote is contiguous and <=25 words at the stated offset, that `source` names the right document, `kind`/`tier` are defensible under `{LANE}/corpus/QUALITY.md` and CORPUS.md, and `used-by` names an entry that really cites it. Report per-row verdict and any cell you would change."),
    it("RevC3Entries", "reviewer", f"Read both landed entries (`{BASE}`, `{AMEND}`) against their captures: locate every quoted token and every figure they state (including the char-pointer figures) and report any that you cannot find verbatim, any sentence that states more than the capture supports, and any staged-id remnant. Verdict per entry: clean / findings listed."),
    it("CritC3Inference", "critic", f"Attack the two entries' Inference sections one bullet at a time as a hostile reader: does each inference follow from the spans it cites, or does it substitute the lane's framing for the source's? Pay attention to (a) 'durability comes from freezing the pool, not from stamping each citation', (b) the amendment's 'same instrument the lane already holds', (c) the unknown that the corpus does not address revision history. Verdict per bullet: holds / holds narrowed (give the sentence) / fails."),
    it("RevC3Quotes", "reviewer", f"Verify the eleven committed quotes are verbatim in their captures at the recorded offsets, and that each quote also appears in the citing entry (that is the QUOTES_IN_ENTRY leg). Report any quote whose entry copy differs in whitespace, punctuation or apostrophe form — including the S089 curly apostrophe and any `%` spacing."),
    it("RevC3RefBind", "reviewer", f"Verify the two cross-reference bindings and the id whitelist: find the sentence in each entry that names S079 and the one that names S081, confirm each names the right document (RFC 7089; WARP/NDL), and confirm no staged id (S120–S122, S127, S128, S071, S095, S082-as-PRISMA-S) survives anywhere in either entry. Then check the counter's ALLOWED_IDS is not wider than the entries need — name any id the whitelist would let in that no entry should cite."),
    it("RevC3Census", "reviewer", f"Run the census both ways: `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` and `--file {LANE}/corpus/SOURCES.md`. Paste exit codes and the E-code lines (must be none). Then check the row count (89 rows) and that no row cell contains a pipe. Report any E/W code beyond the five known W04."),
    it("RevC3QuoteReopen", "reviewer", f"Run the lane's quote-reopen tool over the eleven round-46 quotes as an independent second check: build a TSV (`id`, `source_id`, `quote`) from `{EV}/spans.tsv` in /tmp and run `python3 {LANE}/tools/quote-reopen.py verify --items <tsv> --registry {LANE}/corpus/SOURCES.md`. NOTE the tool fetches http(s) — network egress is FORBIDDEN this round, so do NOT run it; instead read its code and state exactly what it would do, why it cannot be used offline, and substitute a local byte-compare of each quote against its capture at the recorded offset. Report the local verdict per quote."),
    # records and hygiene (10)
    it("RevCensus", "scout", f"Independent census: count rows and statuses in `{LANE}/corpus/SOURCES.md` with the frozen manual commands from /home/vgpnk/Projects/shokunin/CORPUS.md (row count, malformed rows, tier histogram, status histogram, duplicate ids, enum violations, mined used-by paths that do not exist). Paste each command and output; report any non-empty check."),
    it("RevShonen", "reviewer", f"Read `{LANE}/SHONEN.md` and check each box's claim against the repo state now (files exist, commands run, evidence pointers resolve). Report per box: holds / does not hold (with the command). Do not edit SHONEN.md."),
    it("RevClaimTags", "reviewer", f"Run `python3 {LANE}/corpus/evidence/round45/tag-count.py --scorecard {LANE}/SCORECARD.md --from 46 --to 46`; it must print `TAGGED=n/n` with exit 0 for the round-46 verdict table, and each claim row must carry `ground` or `plumbing` consistent with what it changed (C1 plumbing, C2 plumbing, C3 ground). Report the output and any untagged or mistagged row."),
    it("SentScope2", "sentinel", f"Scope and egress audit of the landed state: run `git -C {LANE} status --porcelain`, confirm no round-46 file names the fleet repo or shokuknow for writing, grep the round's new code for egress and write paths (`urllib requests socket http.client curl wget os.system subprocess open(.*w`), and check that `{LANE}/corpus/evidence/round46/controls/` and `spans/` contain only what the counters read. Report every hit and whether it can write outside the lane."),
    it("RevMisroot", "scout", f"Misroot sweep: `git -C /home/vgpnk/Projects/shokunin status --porcelain` (no pathspec) and for every untracked file at the fleet root or under its `.ufo/waves/`, check whether its content names chousa or round-46. Report each hit with path and the matching line; report zero if none. Never delete or move anything."),
    it("RevLesson", "reviewer", f"Read `{LANE}/corpus/lessons/round-46.md` `## Mistakes` and check every row: class present, evidence pointer resolves, captured-by names a criterion or `none`, and the fix is shown able to fail (a command or receipt exists). Report each row: complete / missing element. Also check `## Gate` records URL, access date and a <=25-word quote for each of the five new rows."),
    it("RevGatesRows", "reviewer", f"Check the five new Gates rows for structural conformance with the table's own header (8 cells, 9 pipes, one line) and with the frozen row rule; then verify two rows' `pinned values` digests against the files (sha256 prefixes) and report any stale digest. Report each row."),
    it("CritRoundHonesty", "critic", f"Audit the round for overclaim. Read `{LANE}/SCORECARD.md`'s round-46 section, `{LANE}/corpus/lessons/round-46.md` and `{LANE}/corpus/evidence/round46/measure-after.txt`. For each of the three claims, state whether the recorded verdict is supported by the counter output at `{LAND}` and whether any per-axis verdict (including 'unchanged' ones) is unsupported. Name any sentence that would not survive a hostile closure review."),
    it("RevInherited", "scout", f"Confirm the inherited state is untouched: the three modified JSON paths (`.ufo/waves/round-40/w1/swarm-registry.json`, `.ufo/waves/round-41/w1/swarm-registry.json`, `corpus/evidence/round41/receipts/cells/cells.json`) still have their pre-round hashes (cells.json `1f5c0afae802…` per round 45); list every uncommitted path in the lane and attribute it (wave evidence vs inherited vs new work); confirm the lane tip and `jj-lane.sh state` output."),
]


def main():
    items = [{"name": n, "role": r, "item": DIRECTIVE + "\n\n" + t} for n, r, t in ITEMS]
    spec = {
        "wave": "chousa-r46-w2",
        "milestone": "Round 46 wave 2 (falsify): re-run each counting command, re-derive each span and row, mutation-test the new gate and registry, audit the round records at d09fc8e7",
        "reportDir": ".ufo/waves/round-46/w2",
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
