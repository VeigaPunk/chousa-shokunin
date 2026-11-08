#!/usr/bin/env python3
"""Build the round-84 v1 wave spec (12 seats, one batched spawn handoff)."""
import json
import pathlib

LANE = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
SCRATCH = "/fast/scratch/hyaku/chousa-r84"
BASE = "408ae68f9e445fc911f713d5bbb3a64dda1ab9fe"
FREEZE = "3b616420b2dcc1f8a24a1cb9db4198c7adc8929b"
LANDING = "03bbb4580b39b442be69f998fae2db48d64b8c93"
TIP = "03bbb4580b39b442be69f998fae2db48d64b8c93"
W = f"{LANE}/.ufo/waves/round-84/w1"
E = "corpus/evidence/round84"
ENTRY = "corpus/knowledge/search-transparency-reporting-r84.md"
TOOL = "tools/gate-records.py"

CONTEXT = f"""Lane chousa round 84, L1 ChousaR84 holds the canonical planner seat and integration. Root {LANE}. Revisions: base {BASE} (round-83 tip, closed rejected-honest-stop); egress table committed before any fetch (in freeze {FREEZE}); claim freeze (claims + counters + controls script) {FREEZE}; scored landing {LANDING} (the bytes you attack); current tip {TIP} (same as landing — no post-scoring changes).
Frozen predicate set: {LANE}/{E}/claims.md — read it FIRST, including every kill rule. Two claims: C1 operability — the repaired tool `{TOOL}` (`verify --root LANE [--repo GITDIR] FILE...`) passes a successor battery it could not pass before the r83 repair, counted by `{E}/gate-records-r84.py` (15 frozen positives, 5 fresh positives built in-counter, 288 forgeries across all mutation classes incl. 9 r83 survivors, non-ASCII numerals, whitelist-forger control, empty-file leg, setup leg); C2 depth — one new entry `{ENTRY}` on registry rows S214 (PRISMA 2020 checklist PDF), S018 (ACL 2026 survey), S023 (DCMI terms), counted by `{E}/depth-r84.py`. Before receipts: `{E}/controls/receipts/`; after receipts: `{E}/after/`. The claims are frozen: you never amend them, their counters, fixtures or receipts; you measure, attack and report.
Every `Report:` trailer path is relative to {LANE} — write it at {LANE}/<that path>.

Leaf only: no task tool, no subagents, no agent://all, no production edits, no lane or fleet git/jj mutation, no commits or pushes, no edits to /home/vgpnk/Projects/shokunin/scripts, /home/vgpnk/Projects/shokunin/.ufo/state, MANIFEST.json, considerthese/ or any sibling repo. The only files you write are under your own output folder {W}/<seat>/ plus your scratch dir. Network: none, except a seat whose item names a re-open (one GET per URL that has a 2026-11-08T02:1x-02:2xZ row in `corpus/evidence/round57/refetch.tsv`, into your scratch; never write `corpus/captures/` or `refetch.tsv`) — `{E}/egress-approval.md` is the table.

Scratch: every clone, archive tree, work dir and fixture lives under {SCRATCH}/<your seat name>/; create it with mkdir -p, pass it explicitly (TMPDIR=... HYAKU_SCRATCH=... --work ...), delete it before you yield (`trap 'rm -rf -- "$S"' EXIT` in shell, `finally: shutil.rmtree` in Python), and copy every receipt you cite into your wave output folder first. Never write under /tmp (the reaper deletes it; a /tmp path is never citable evidence). Use `git -C {LANE} archive <rev> | tar -x -C <scratch dir>` for a tree at a revision; any fixture git repo is `D=$(mktemp -d -p {SCRATCH}/<seat>) && test -n "$D" && git -C "$D" init -q`, every later git call names `-C "$D"` and you assert `git -C "$D" rev-parse --show-toplevel` equals "$D" before any mutating git command.

Counter that binds you: every finding names the exact command, the receipt path you wrote and the observed line plus exit code. An unrun check has not passed; a deviation from an expected value is a finding, never something to hide. End your report with one line `VERDICT: <seat> <claim> fired|held|n/a — <one sentence>` per claim you touched (plain text, not JSON).

Tooling authorization (operator, 2026-10-19): you may install or upgrade tools that help the task; read /home/vgpnk/.omp/agent/RULES.md first (official channels only; record tool/version/channel/reason in your report). pacman guard (orchestrator ruling 2026-10-20): all pacman transactions are PAUSED host-wide — install via `uv tool`/`npx`/an official binary in ~/.local/bin, or not at all; never `pacman -Sy`, `-Syu`, `-U`, `-R`, never downgrade, never restart a host service.
"""

GODSPEED = """/skill:godspeed

You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.
"""

items = []


def add(name, role, body):
    items.append({"name": name, "role": role, "prompt": GODSPEED + "\n" + body.strip() + "\n"})


add("R84ExecRepro", "executor", f"""
Reproduce both frozen claims from committed bytes, before and after (C1 K1, C2 K1, C2 K4).
(a) Instrument identity: `git -C {LANE} show <rev>:<path> | sha256sum` for every path in `{E}/instrument-pins.txt` at {FREEZE} and {LANDING}; all must equal the pins.
(b) BEFORE/AFTER: archive {FREEZE} and {LANDING} into scratch; in each run `python3 -B <tree>/{E}/depth-r84.py --root <tree>` and `python3 -B <tree>/{E}/gate-records-r84.py --root <tree> --repo {LANE} --work {SCRATCH}/R84ExecRepro`. Expected before (freeze rev): `DEPTH_R84 entries=0` FAIL rc 1 and `TOOL=present ... GATE_RECORDS_R84=PASS` rc 0 (the tool was already repaired at freeze — the counter proves it); after (landing): the exact predicate lines in claims.md, rc 0. Repeat the after runs at {TIP}.
(c) Re-run the committed control driver: from {LANE} run `HYAKU_SCRATCH={SCRATCH}/R84ExecRepro bash {E}/run-controls-r84.sh {LANDING} {W}/R84ExecRepro/controls-rerun` and compare its summary.tsv with `{E}/controls/receipts/summary.tsv` (expect `CONTROLS_AS_EXPECTED=9/9`).
(d) C1 predicate (b): at {TIP} run `python3 tools/gate-records.py verify --root . corpus/lessons/round-84.md` from an archived tree (with `--repo {LANE}`); expect 3 OK, exit 0.
(e) C1 K4: run the tool on a file with no record, on a file with one OK record plus one FAIL record, and with a missing FILE argument; report each rc (expected 1, 1, 2).
Receipts in {W}/R84ExecRepro/.
""")

add("R84ExecForge", "executor", f"""
Fire-or-hold C1 kill rule K2 (spec generalization): author NEW in-class forged `GATE-RECORD` lines the frozen battery does not contain, each violating one check of the docstring of `{TOOL}` at {LANDING}, and run the landed tool on them.
Work in an archive of {LANDING} in scratch; put each forged line in its own file under `<tree>/forge/`; run `python3 tools/gate-records.py verify --root <tree> --repo {LANE} <files>` from the tree root.
Start from the 15 frozen positives (`{E}/c2-positives.tsv`) and the 3 round-84 records (`corpus/lessons/round-84.md` at {TIP}). Cover at least: upper-case or mixed-case sha prefix; `…` vs `...` vs no suffix; sha of the .raw file instead of the .txt; a refetch row of a FAILED attempt for the same url; a refetch row with matching url but a different id; url with trailing slash / fragment / http vs https; tier lower-case; decision values other than admit|reject; words with leading zero, plus sign or unicode digits (beyond the 9 r83 survivors); quote with NBSP, tab, zero-width space, curly vs straight quotes, HTML entities, a quote spanning a line break in the capture; quote that is located only in a DIFFERENT capture; rev form with short rev, tag name, `HEAD`, a tree hash, path with spaces or non-ASCII; admit form with `capture=none`; unreach form claiming success; line number off by one; record-line detection edge cases (leading whitespace, indented lines, fenced code blocks).
For each forged line: which docstring check it violates (or `none` — then it is not a forgery), in-class per claims.md K2 (yes/no and why), tool output line and rc. Any in-class line violating a check on which the tool prints `OK` FIRES K2 — say so. Also list any line that meets every check but is refused (K3 harm candidate).
Receipts + forged files in {W}/R84ExecForge/.
""")

add("R84ExecHarm", "executor", f"""
Fire-or-hold C1 kill rule K3 (harm) and K4 on real lane history, plus a side-effect audit.
(1) In an archive of {TIP}, run `python3 tools/gate-records.py verify --root <tree> --repo {LANE} <file>` on every file under `corpus/lessons/` and on every other committed file containing a line whose first text is `GATE-RECORD` (`git -C {LANE} grep -n -E '^[[:space:]]*GATE-RECORD' {TIP}`). Tabulate records, OK, FAIL per file.
(2) For every FAIL, decide by hand from bytes whether the record really violates the docstring check named (show the bytes: registry row, capture sha256, refetch row, quote location command `python3 -c 'import sys;t=" ".join(open(sys.argv[1],encoding="utf-8",errors="replace").read().split());print(" ".join(sys.argv[2].split()) in t)' <capture> '<quote>'`, or `git -C {LANE} show <rev>:<path> | sed -n '<line>p'`). A FAIL on a record that meets every check FIRES K3. A genuine defect in an old record is a real catch — list it.
(3) Side effects: run the tool once under `strace -f -e trace=network,openat,unlink,rename,write -o <file>` if strace exists (else say so and use `ltrace`/`inotifywait` or a before/after `find <tree> -newer` listing): report any socket call, any file opened for writing, any git subcommand other than `cat-file` (also grep the source for subprocess calls). Any write, network or mutating git FIRES K3.
Receipts in {W}/R84ExecHarm/.
""")

add("R84ExecReopen", "executor", f"""
Fire-or-hold C2 kill rule K2 (located). Network allowed for exactly three GETs (one per URL), the S214/S018/S023 URLs with 2026-11-08T02:1x-02:2xZ rows in `corpus/evidence/round57/refetch.tsv`.
(1) For each of the 12 quotes in `{ENTRY}` at {LANDING} (`## Located quotes`), check it in the committed capture of its S-id (`corpus/captures/<sha256(url)[:24]>.txt`) after whitespace collapse with curly quotes folded to ASCII; record FOUND/ABSENT and the capture line number.
(2) Re-open each URL once: `curl -fsSL --compressed --max-time 20 -A 'Mozilla/5.0 (chousa r84 reopen)' <url> -o {SCRATCH}/R84ExecReopen/<id>.html`; tag-strip (drop script/style), unescape HTML entities, collapse whitespace, fold curly quotes; check every quote. Record HTTP status, byte count, FOUND/ABSENT per quote. An ABSENT quote on a 200 page FIRES K2; an unreachable page is recorded, not a kill.
(3) Count words of each quote (`wc -w` and Python split); flag any outside 8..25.
Receipts (not the HTML bodies) in {W}/R84ExecReopen/.
""")

add("R84ReviewerEntry", "reviewer", f"""
Fire-or-hold C2 kill rule K3 (warrant) on `{ENTRY}` at {LANDING}. Read claims.md K3 exactly.
For EACH of the 11 decision-table rows: (a) does the Do follow from the cited quotes (state what the quote says and what the Do adds); (b) does the Never follow (the Never must be the negation of something the quotes require, within their hedges); (c) read the FULL paragraph and section around each cited quote in the committed capture (`corpus/captures/a640b15abf781e5c583d7088.txt` S214, `248b43277f376e437a356909.txt` S018, `f5545a194c06ab421875b047.txt` S023) and quote, with capture line number, any sentence of the same source that contradicts the row's Do or Never. Also judge the entry's `## Inference` and `## Limits` sections for overreach (these are not K3 rows; report as residuals).
Be strict but exact: a finding must name the row, the word(s) in the row, and the located sentence or the missing support. A row that is merely narrower than the source is not a K3 firing. Verdict per row: held / fired (a) / fired (b) and why.
Report at {W}/R84ReviewerEntry.md (and receipts under {W}/R84ReviewerEntry/).
""")

add("R84ReviewerTool", "reviewer", f"""
Code review of `{TOOL}` at {LANDING} against its own docstring (the C1 spec) and claims.md C1 K2/K3/K4.
(1) For each documented check (PARSE, REGISTRY, TIER, CAPTURE_PATH, CAPTURE_KEY, CAPTURE_SHA, REFETCH, WORDS, QUOTE_LEN, QUOTE_ABSENT, REV, LINE, SETUP) read the implementing code and state whether it enforces exactly what the docstring says; find any input on which the code prints OK while the docstring check is violated (build it, run it in an archive of {LANDING} in scratch with `--repo {LANE}`, record output — that FIRES K2 if in class) and any input meeting every check that is refused (K3).
(2) Parsing: key order, duplicate keys, empty values, `quote=` placement, trailing whitespace, CRLF, unicode, record-line detection (`lead_strip`, REC_RE) vs the declared record class in claims.md.
(3) Exit contract (K4), error handling (unreadable capture, invalid UTF-8, missing refetch log, non-git `--repo` → exit 2), and any code path that writes, fetches or mutates git.
(4) Note every docstring/claims.md inconsistency.
Report at {W}/R84ReviewerTool.md with receipts under {W}/R84ReviewerTool/.
""")

add("R84CriticClaims", "critic", f"""
Adversarial critic of both frozen claims (claims.md at {FREEZE}) as claims, not code.
(1) Controls adequacy: is there a control cheaper than the claimed work that meets either predicate? Build and score it with the frozen counters (in an archive of {LANDING} in scratch: for C1 a tool that is not the landed one, e.g. one that keys on the forgery construction, on the file name pattern `f\\d{{3}}.md`, on the presence of `Zyzzyva`, or that only checks registry+refetch; for C2 an entry with content-free rows — the declared B1 boundary — or a re-landed old entry with fresh rows). Report each control's counter lines and rc. A cheap control that PASSes C1's counter shows the battery is gameable: say whether the claim text then still verifies.
(2) Claim–predicate alignment: does the C1 predicate measure the claim sentence (all docstring checks + setup leg)? Which forgery classes have no mutation in the 288 (coverage gap)? Does the C2 predicate measure "teaches search-transparency reporting"?
(3) Thinness: is C1 a real capability (compare with what the lessons' hand Location command and `tools/quote-reopen.py` already did; is any check redundant with an existing lane tool or gate)? Is C2 new ground (K4; compare with `corpus/knowledge/search-log-method-r39.md`, `search-tracking-record-r40.md`, `citation-searching-tarcis-r81.md`)?
(4) Freeze discipline: compare commit times and contents of {FREEZE}, {LANDING}; claims.md discloses the counters were frozen before the entry was drafted — judge whether any predicate or counter byte changed after scoring.
Report at {W}/R84CriticClaims.md with receipts under {W}/R84CriticClaims/.
""")

add("R84MutationTool", "mutation-tester", f"""
Mutation test `{TOOL}` against the frozen counter `{E}/gate-records-r84.py` (C1). In an archive of {LANDING} in scratch, generate at least 20 single-point mutants of the tool (remove or invert each check, relax `{{16,64}}` to `{{1,64}}`, drop the key check, drop `r[8] == capsha`, drop `r[4] == fetched`, accept curl_rc != 0, accept non-2xx, words off-by-one, QUOTE_LEN bounds 0..26, skip lead_strip, skip indented lines, REV accepting short revs, LINE checking the whole blob instead of the line, exit 0 on zero records, exit 0 with FAIL lines, ASCII digit class relaxed to Unicode `\\d`, quote boundary `"` guard removed, etc.). For each mutant run `python3 -B <tree>/{E}/gate-records-r84.py --root <tree> --repo {LANE} --tool <mutant> --work {SCRATCH}/R84MutationTool` and record the counter lines and rc. A mutant the counter still scores PASS is a battery gap — list it.
Report at {W}/R84MutationTool.md with mutants and receipts under {W}/R84MutationTool/.
""")

add("R84ScoutNovelty", "scout", f"""
Read-only reconnaissance, two surfaces.
(1) C2 K4 (ground): at {BASE} and at {LANDING}, does any file in `corpus/evidence/round84/base-knowledge.txt`'s list (under `corpus/knowledge/`) cite S214, S018 or S023 on a `source:` line, or contain any of the three URLs (`git -C {LANE} grep -n -F '<url>' <rev> -- corpus/knowledge`)? Does any held entry already teach search-transparency reporting (PRISMA checklist items, search strategy reporting, DCMI source/modified/valid)? Quote what you find with file:line and say whether it is the same ground.
(2) S017 disposition: S017 was fetched (landing page, checklist page, checklist PDF) but reverted to `queued` because the landing page has no quotable checklist text. Verify: does `corpus/captures/259c96bf7088a12bc7ce65c4.txt` (landing) contain any 8-25 word quote about search reporting? Does `corpus/captures/a640b15abf781e5c583d7088.txt` (PDF, now S214) contain the items? Is the S017→S214 split correct?
Report at {W}/R84ScoutNovelty.md.
""")

add("R84ConnectorSiblings", "connector", f"""
Sibling-overlap scan (read-only). Sibling lanes live at /home/vgpnk/Projects/shokunin/<lane>-shokunin (e.g. kengaku, kasegi, kumitate, kagi, tameshi, kaidoku, mori, tabi, souji, kotoba, kotodama, revenger, tsukuroi, kama, kake, mado). (1) Does any sibling hold a knowledge entry on search-transparency reporting (PRISMA checklist, search strategy reporting, DCMI source/valid, systematic-review search audit)? `grep -rl` over each `corpus/knowledge/` and `corpus/SOURCES.md`. (2) Does any sibling hold a tool that verifies lesson Gate records / located quotes against committed captures (grep tools/ and scripts/ for `GATE-RECORD`, `capture_sha256`, `refetch.tsv`)? (3) Does the new entry or tool touch sibling province (`{LANE}/PROVINCE.md`)?
Report at {W}/R84ConnectorSiblings.md.
""")

add("R84ScribeLesson", "scribe", f"""
Draft (do not land) sections for `corpus/lessons/round-84.md` (current Gate block at {TIP}; study `{LANE}/corpus/lessons/round-83.md` for format).
(1) `## Mistakes`: mine ONE mistake from an earlier round in the form `class · evidence pointer · captured-by · fix`. Candidates: (a) round-84's own S017→S214 split (landing page vs PDF capture mismatch — the depth counter's `fresh()` resolves by registry URL, so a source whose quotable content is in a linked PDF needs its own row); (b) round-83's `c1-b1` overlay breaking the real entry's `used-by` (comma-separated list fix); (c) round-83's Unicode `\\d` in `INT_RE` (already QUALITY 164). Show the fix can fail: run the counter before/after and paste outputs. If you find a better-evidenced mistake, use it and say why.
(2) `## considerthese`: read `{LANE}/considerthese/` newest files (never edit); name at most ONE still-unimplemented proposal and whether this round implements it (with evidence) or not (with reason).
(3) `## Assimilation`: `none` with the reason (re-count `{LANE}/.ufo/waves/round-78/assimilation/collisions` lines).
(4) A `## Gate` addendum: one admit and one reject for the non-author spot-check, drawn from the existing Gate block at {TIP} (verify each with `python3 tools/gate-records.py verify` and the hand location command).
Deliver at {W}/R84ScribeLesson/lesson-draft.md.
""")

add("R84SentinelScope", "sentinel", f"""
Boundary and safety sentinel for round 84. Read-only.
(1) Egress: `{E}/egress-approval.md` was committed before any fetch — compare `git -C {LANE} log -1 --format=%cI <egress-commit>` (convert to UTC) with every refetch.tsv row dated 2026-11-08 after 02:00Z; every fetch a GET of a URL in the table's intended-targets list, no credentials (read `tools/capture-fetch.py`).
(2) Province: does the new entry or tool absorb sibling province (kengaku model quality, kasegi bounty scope, kumitative orchestration, kagi secrets)? Quote `PROVINCE.md` and the entry lines.
(3) Secrets: scan `git -C {LANE} diff {BASE} {TIP}` and the three new captures for credential-shaped strings (tokens, keys, cookies, session ids) — shape only, never print a value.
(4) Misroot: `git -C /home/vgpnk/Projects/shokunin status --porcelain` — list any untracked fleet-root file whose content names chousa round 84 (do not move or delete anything; report paths).
(5) Scratch: `du -sh {SCRATCH} 2>/dev/null; ls /tmp | grep -i r84` — report leftovers.
Report at {W}/R84SentinelScope/sentinel.md.
""")

spec = {"wave": "chousa-r84-w1", "reportDir": ".ufo/waves/round-84/w1", "context": CONTEXT, "items": items}
out = pathlib.Path(f"{LANE}/.ufo/waves/round-84/w1-spec.json")
out.write_text(json.dumps(spec, indent=2) + "\n")
print(f"wrote {out} with {len(items)} items; roles={sorted(i['role'] for i in items)}")
