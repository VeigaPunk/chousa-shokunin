#!/usr/bin/env python3
"""Build the round-85 v1 wave spec (12 seats, one batched spawn handoff)."""
import json
import pathlib

LANE = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
SCRATCH = "/fast/scratch/hyaku/chousa-r85"
BASE = "43c3f7284eee4889cdcc6ac1626573f6579cd533"
FREEZE = "5d0b94139ae8baf60d6f630715bc495f0a93b448"
AMEND = "02df67db4f9ad39f8ebc73984ce50ea1fbea315f"
LANDING = "64803d33362f50cf9094e91fc3a4a07216c563ca"
TIP = LANDING
W = f"{LANE}/.ufo/waves/round-85/w1"
E = "corpus/evidence/round85"
ENTRY = "corpus/knowledge/provenance-recording-r85.md"
TOOL = "tools/gate-records.py"

CONTEXT = f"""Lane chousa round 85, L1 ChousaR85 holds the canonical planner seat and integration. Root {LANE}. Revisions: base {BASE} (round-84 tip + verifier spot-check); egress table and claim freeze {FREEZE} (committed before any fetch); claims amendment {AMEND} (C2 ground re-pointed to S215/S026/S024, depth counter parser repaired, C1 setup leg moved into the counter); scored landing {LANDING} (the bytes you attack); current tip {TIP} (same as landing).
Frozen predicate set: {LANE}/{E}/claims.md — read it FIRST, including every kill rule, and {LANE}/plans/round-85.md for the three amendments. Two claims: C1 operability — the round-85 repair of `{TOOL}` (`verify --root LANE [--repo GITDIR] FILE...`: non-git `--repo` is a setup error exit 2; REFETCH success is http exactly 200, not 2xx; `fetched` must be a real calendar instant) passes a successor battery, counted by `{E}/gate-records-r85.py` (15 frozen positives, 5 fresh positives built in-counter, 354 forgeries incl. the differentiated classes, whitelist and empty legs, and a counter-scored setup leg); C2 depth — one new entry `{ENTRY}` on registry rows S215 (W3C alternate PROV-O URL), S026 (GO FAIR R1.2) and S024 (Schema.org lastReviewed), counted by `{E}/depth-r85.py`. Before receipts: `{E}/controls/receipts/`; after receipts: `{E}/after/`. The claims are frozen: you never amend them; you attack the landing bytes and report fire-or-hold per kill rule.
Every `Report:` trailer path is relative to {LANE} — write it at {LANE}/<that path>.

Leaf only: no task tool, no subagents, no agent://all, no production edits, no lane or fleet git/jj mutation, no commits or pushes, no edits to /home/vgpnk/Projects/shokunin/scripts, /home/vgpnk/Projects/shokunin/.ufo/state, MANIFEST.json, considerthese/ or any sibling repo. The only files you write are under your own output folder {W}/<seat>/ plus your scratch dir. Network: none, except a seat whose item names a re-open (one GET per URL that has a 2026-11-08 round-85 row in `corpus/evidence/round57/refetch.tsv`, into your scratch; never write `corpus/captures/` or `refetch.tsv`) — `{E}/egress-approval.md` is the table.

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


add("R85ExecRepro", "executor", f"""
Reproduce both frozen claims from committed bytes, before and after (C1 K1, C2 K1, C2 K4).
(a) Instrument identity: `git -C {LANE} show <rev>:<path> | sha256sum` for every path in `{E}/instrument-pins.txt` at {LANDING}; all must equal the pins (the pins are re-derived from the landing commit, so a mismatch is a finding).
(b) BEFORE/AFTER: archive {BASE} and {LANDING} into scratch; in each, run
`python3 -B <tree>/{E}/depth-r85.py --root <tree>` and
`python3 -B <tree>/{E}/gate-records-r85.py --root <tree> --repo {LANE} --work {SCRATCH}/R85ExecRepro`.
Expected before (base tree, whose counters must be copied in from {LANDING} — say so and do it byte-exactly): `DEPTH_R85 entries=0` FAIL rc 1 and `TOOL=present ... SETUP=0/1` FAIL rc 1; after (landing): the predicate lines in claims.md, rc 0.
(c) Re-run the three committed control legs: `c1-k0-donothing`, `c2-d0-donothing`, `c1-accept-stub` from `{E}/controls/receipts/`, and confirm each observed value matches its receipt.
(d) C1 predicate at the landing tree through the public CLI: `python3 tools/gate-records.py verify --root <tree> --repo {LANE} corpus/lessons/round-85.md` → 3 OK, exit 0.
(e) Exit contract: a file with no record (expect 1), a file with one OK plus one FAIL record (expect 1), a missing FILE argument (expect 2), a non-git `--repo` (expect 2 with `GATE_RECORDS_ERROR` on stderr).
Receipts in {W}/R85ExecRepro/.
""")

add("R85ExecForge", "executor", f"""
Fire-or-hold C1 kill rule K2 (spec generalization): author NEW in-class forged `GATE-RECORD` lines the frozen battery does not contain, each violating one check of the docstring of `{TOOL}` at {LANDING}, and run the landed tool on them.
Work in an archive of {LANDING} in scratch; put each forged line in its own file under `<tree>/forge/`; run `python3 tools/gate-records.py verify --root <tree> --repo {LANE} <files>` from the tree root.
Start from the 15 frozen positives (`{E}/c2-positives.tsv`) and the three round-85 records (`corpus/lessons/round-85.md` at {TIP}). Cover at least: `fetched` with month 13 / day 32 / hour 24 / minute 60 / second 60 / Feb 29 in a non-leap year (PARSE expected after the repair — this is the round-85 calendar check); a refetch row of a 203 or 206 attempt for the same url/time (REFETCH expected after the 200-only narrowing); a refetch row whose http is 201/299; upper-case or mixed-case sha prefix; `…` vs `...` vs no suffix; sha of the `.raw` file instead of the `.txt`; a refetch row with matching url but a different id; url with trailing slash / fragment / http vs https; tier lower-case; decision values other than admit|reject; words with leading zero, plus sign or unicode digits; quote with NBSP, tab, zero-width space, curly vs straight quotes, HTML entities, a quote spanning a line break in the capture; quote located only in a DIFFERENT capture; rev form with 39-hex rev, tag name, `HEAD`, `rev^{{commit}}` text, a 26-word quote, `line=0`, `line` of 7 digits.
For each forged line: which docstring check it violates (or `none` — then it is not a forgery), in-class per claims.md K2 (yes/no and why), tool output line and rc. Any in-class line printing `OK` FIRES K2 — say so. Also list any line meeting every check that is refused (K3 harm candidate).
Receipts + forged files in {W}/R85ExecForge/.
""")

add("R85ExecHarm", "executor", f"""
Fire-or-hold C1 kill rule K3 (harm) and K4 on real lane history, plus a side-effect audit.
(1) In an archive of {TIP}, run `python3 tools/gate-records.py verify --root <tree> --repo {LANE} <file>` on every file under `corpus/lessons/` and on every other committed file containing a line whose first text is `GATE-RECORD` (`git -C {LANE} grep -n -E '^[[:space:]]*GATE-RECORD' {TIP}`). Tabulate records, OK, FAIL per file.
(2) For every FAIL, decide by hand from bytes whether the record really violates the docstring check named (show the bytes: registry row, capture sha256, refetch row with its http cell, calendar validity of `fetched`, `git -C {LANE} show <rev>:<path> | sed -n '<line>p'`). A FAIL on a record that meets every check FIRES K3. Two specific regressions to test explicitly: (a) any historical record whose refetch row has http 203/204/206 — it passed under r84's 2xx rule and must now FAIL, which is the intended narrowing, not harm, if and only if the body was unquotable; say which records change and whether each change closes a genuine in-class form; (b) any historical record with a calendar-invalid `fetched` (grep the refetch log).
(3) Side effects: run the tool once under `strace -f -e trace=network,openat,unlink,rename,write -o <file>` if strace exists (else say so and use a before/after `find <tree> -newer` listing): report any socket call, any file opened for writing, any git subcommand other than `cat-file`, and any `git -C` on a repo other than the one named.
Receipts in {W}/R85ExecHarm/.
""")

add("R85ExecReopen", "executor", f"""
Fire-or-hold C2 kill rule K2 (located). Network allowed for exactly three GETs (one per URL), the S215/S026/S024 URLs with 2026-11-08T03:5x–04:1xZ rows in `corpus/evidence/round57/refetch.tsv`.
(1) For each of the 7 quotes in `{ENTRY}` at {LANDING} (`## Located quotes`), check it in the committed capture of its S-id (`corpus/captures/<sha256(url)[:24]>.txt`) after whitespace collapse with curly quotes folded to ASCII; record FOUND/ABSENT and the capture line number.
(2) Re-open each URL once: `curl -fsSL --compressed --max-time 20 -A 'Mozilla/5.0' <url> -o {SCRATCH}/R85ExecReopen/<id>.html` (the campaign UA is the one in `tools/capture-fetch.py`; use the plain one if the campaign UA answers 403 and say so); tag-strip (drop script/style), unescape HTML entities, collapse whitespace, fold curly quotes; check every quote. Record HTTP status, byte count, FOUND/ABSENT per quote. An ABSENT quote on a 200 page FIRES K2; an unreachable page is recorded, not a kill.
(3) Count words of each quote (Python split); flag any outside 8..25.
Receipts (not the HTML bodies) in {W}/R85ExecReopen/.
""")

add("R85RevCalendar", "revenger", f"""
One falsifiable hypothesis, one probe: **the round-85 calendar check (`_valid_ts`) and the `TS_RE` shape check together accept exactly the real UTC instants and reject every shape-valid impossible date, and the check cannot be bypassed by a value that `strptime` accepts while a reader would call it invalid.**
Build an independent boundary set (do not copy the counter's list): leap day 2024-02-29 (accept), 2025-02-29 (reject), 2026-04-31 (reject), 2026-12-31T23:59:59Z (accept), 2026-01-01T00:00:00Z (accept), hour 24 (reject), second 60 / leap second (record what `strptime` does and whether the tool rejects), year 0000, month 00, negative-free forms with `+00:00` offset text (reject, shape), a lowercase `t`/`z` (reject), a value with a trailing `Z ` (record), and a unicode digit month. For each, run the landed `tools/gate-records.py verify` on one rev-form and one admit-form forged line (from a frozen positive), and report the tool's verdict + code.
Then state whether the check matches the hypothesis; if any input differs between the two forms (rev vs admit), that is a finding (one value grammar, two readings — QUALITY 164's class).
Also verify the tool imports `datetime` and that a missing import would be caught by the counter (mutate the copy in scratch to drop the import and show what happens).
Report at {W}/R85RevCalendar.md with receipts under {W}/R85RevCalendar/.
""")

add("R85ReviewerTool", "reviewer", f"""
Code review of `{TOOL}` at {LANDING} against its own docstring (the C1 spec) and claims.md C1 K2/K3/K4.
(1) For each documented check (PARSE, REGISTRY, TIER, CAPTURE_PATH, CAPTURE_KEY, CAPTURE_SHA, REFETCH, WORDS, QUOTE_LEN, QUOTE_ABSENT, REV, LINE, and the setup error), read the implementing code and state whether it enforces exactly what the docstring says. The three round-85 repairs get a line each: the non-git `--repo` probe (does it catch a bare directory, a file, a worktree root, `--repo ''`, a subdirectory of a repo?), the exactly-200 REFETCH rule, and the calendar `fetched` rule.
(2) Find any input on which the code prints OK while the docstring check is violated (build it, run it in an archive of {LANDING} in scratch with `--repo {LANE}`, record output — that FIRES K2 if in class) and any input meeting every check that is refused (K3).
(3) Parsing: key order, duplicate keys, empty values, `quote=` placement, trailing whitespace, CRLF, unicode, record-line detection (`lead_strip`, REC_RE), and whether the docstring's `1–25 word` bound is the same sentence in code (`1 <= n <= 25` vs `QUOTE_LEN` text).
(4) Exit contract (K4), error handling (unreadable capture, invalid UTF-8, missing refetch log, non-git `--repo` → exit 2), and any code path that writes, fetches or mutates git.
(5) Note every docstring/claims.md inconsistency, including the docstring's claim about `capture-fetch.py`'s own store rule.
Report at {W}/R85ReviewerTool.md with receipts under {W}/R85ReviewerTool/.
""")

add("R85ReviewerEntry", "reviewer", f"""
Fire-or-hold C2 kill rule K3 (warrant) on `{ENTRY}` at {LANDING}. Read claims.md K3 exactly.
For EACH of the 6 decision-table rows: (a) does the Do follow from the cited quotes (state what the quote says and what the Do adds); (b) does the Never follow (the Never must be the negation of something the quotes require, within their hedges); (c) read the FULL paragraph and section around each cited quote in the committed captures (`corpus/captures/6e48bcc4a04d13b7b3ebb68e.txt` S215 PROV-O, `67983a3dbbd1d690aa648744.txt` S026 R1.2, `11d6cc56bb24adfc61eea2b4.txt` S024 Schema.org) and quote, with capture line number, any sentence of the same source that contradicts the row's Do or Never. Also judge the entry's `## Inference` and `## Limits` sections for overreach (not K3 rows; report as residuals), and check whether S215's page is the same document as S020's canonical URL (the round claims the alternate URL carries the material — verify by content, not by title).
Be strict but exact: a finding must name the row, the word(s) in the row, and the located sentence or the missing support. A row that is merely narrower than the source is not a K3 firing.
Report at {W}/R85ReviewerEntry.md (and receipts under {W}/R85ReviewerEntry/).
""")

add("R85CriticClaims", "critic", f"""
Adversarial critic of both frozen claims (claims.md at {FREEZE} + the amendment at {AMEND}) as claims, not code.
(1) Controls adequacy: is there a control cheaper than the claimed work that meets either predicate? Build and score it with the frozen counters (in an archive of {LANDING} in scratch): for C1 a tool that keys on the forgery construction (file names, the `Zyzzyva` string, the `g0001.md` numbering, the `fresh%02d.md` name), a tool that checks registry+refetch only, a tool that accepts only lines containing `capture_sha256=`, and a wrapper that shells out to the pristine tool plus a hard-coded answer for the setup leg; for C2 a content-free-rows entry (the declared B1 boundary), a re-landed round-84 entry with a fresh `source:` line, an entry whose quotes come from captures but whose rows cite the wrong source. Report each control's counter lines and rc. A cheap control that PASSes either counter shows the battery is gameable: say whether the claim text then still verifies.
(2) Claim–predicate alignment: does the C1 predicate measure the claim sentence (all docstring checks + setup leg + the three repairs)? Which docstring check has no forgery in the 354? Does the C2 predicate measure "teaches provenance recording", and is `fresh_sources=3`/`rows>=6`/`located_quotes>=7` a target the do-nothing control can reach?
(3) Thinness: is C1 a real capability (compare with what the lessons' hand Location command and `tools/quote-reopen.py` already did; is any check redundant with an existing lane tool or gate)? Is C2 new ground (K4; compare with `corpus/knowledge/search-transparency-reporting-r84.md`, `metadata-screen-r25.md`, `recheck-due-r26.md`, `correction-retraction-status-r81.md`)?
(4) Freeze discipline: compare commit times and contents of {FREEZE}, {AMEND}, {LANDING}; judge whether any predicate, counter byte or control receipt changed after the first scored entry (the amendment before scoring is disclosed; a change after scoring is a defect).
Report at {W}/R85CriticClaims.md with receipts under {W}/R85CriticClaims/.
""")

add("R85MutationTool", "mutation-tester", f"""
Mutation test `{TOOL}` against the frozen counter `{E}/gate-records-r85.py` (C1). In an archive of {LANDING} in scratch, generate at least 22 single-point mutants of the tool (remove or invert each check, relax `{{16,64}}` to `{{1,64}}`, drop the key check, drop `r[8] == capsha`, drop `r[4] == fetched`, accept curl_rc != 0, accept non-200 (2xx), drop the calendar check, accept a calendar-invalid date, skip `lead_strip`, skip indented lines, REV accepting short revs, LINE checking the whole blob instead of the line, exit 0 on zero records, exit 0 with FAIL lines, ASCII digit class relaxed to Unicode `\\d`, quote boundary `"` guard removed, the setup probe removed, the setup probe inverted (exit 2 on a valid repo), `TS_RE` relaxed to `\\d{{4}}` any month). For each mutant run `python3 -B <tree>/{E}/gate-records-r85.py --root <tree> --repo {LANE} --tool <mutant> --work {SCRATCH}/R85MutationTool/<m>` and record PASS/FAIL plus the printed predicate line.
Report: the full mutant × verdict table, every survivor (mutant the counter PASSes — a survivor is the important finding: it names a check the counter does not load-bear), and the mapping from each survivor to the class a round-86 battery must add. Also re-run the round-84 counter (`{E}/../round84/gate-records-r84.py`) on the landing tool to record cross-round compatibility.
Report at {W}/R85MutationTool.md with mutants and receipts under {W}/R85MutationTool/.
""")

add("R85ScoutGround", "scout", f"""
Read-only reconnaissance, three surfaces.
(1) C2 K4 (ground): at {BASE} and at {LANDING}, does any file in `corpus/evidence/round85/base-knowledge.txt`'s list (under `corpus/knowledge/`) cite S215, S026 or S024 on a `source:` line, or contain any of the three URLs (`git -C {LANE} grep -n -F '<url>' <rev> -- corpus/knowledge`)? Quote what you find with file:line.
(2) Novelty vs held ground: does any held entry already teach provenance recording (`prov:wasDerivedFrom`, generatedAtTime, FAIR R1.2, lastReviewed)? Check `metadata-screen-r25.md`, `recheck-due-r26.md`, `search-transparency-reporting-r84.md`, `correction-retraction-status-r81.md`. Name the nearest neighbour and the exact sentences that differ.
(3) S020 disposition data: collect every refetch row for both PROV-O URLs (`fc127d142427c83cc805fe67` and `6e48bcc4a04d13b7b3ebb68e`) with ids, dates, http codes; state how many attempts each URL has and whether the alternate URL is the same document (compare a distinctive sentence found in both the canonical row's capture if any and the new capture). Also check whether `S033` (the S020 superseding row) is queued or mined and what its URL is — the round's claims file says S020 stays queued.
Report at {W}/R85ScoutGround.md.
""")

add("R85ConnectorSiblings", "connector", f"""
Sibling-overlap scan (read-only). Sibling lanes live at /home/vgpnk/Projects/shokunin/<lane>-shokunin (e.g. kengaku, kasegi, kumitate, kagi, tameshi, kaidoku, mori, tabi, souji, kotoba, kotodama, revenger, tsukuroi, kama, kake, mado). (1) Does any sibling hold a knowledge entry on provenance recording (PROV-O, `wasDerivedFrom`, FAIR R1.2, DCMI `modified`, `lastReviewed`, generation/invalidation times)? `grep -rl` over each `corpus/knowledge/` and `corpus/SOURCES.md`, and quote the closest sentence. (2) Does any sibling hold a tool that verifies lesson Gate records / located quotes against committed captures (grep tools/ and scripts/ for `GATE-RECORD`, `capture_sha256`, `refetch.tsv`), and does any of them already check a calendar-valid timestamp or a 200-only success rule? (3) Does the new entry or the tool repair touch sibling province (`{LANE}/PROVINCE.md`)?
Report at {W}/R85ConnectorSiblings.md.
""")

add("R85ScribeLesson", "scribe", f"""
Draft (do not land) sections for `corpus/lessons/round-85.md` (current Gate block at {TIP}; study `{LANE}/corpus/lessons/round-84.md` for format).
(1) `## Mistakes`: assess the two rows already drafted (prefreeze C2 named an instrument that could never pass; the predicted quote/row counts were unreachable under E4/E7) and either confirm each with the exact failing receipt lines, or replace them with a better-evidenced mistake. The fix must be shown able to fail: run the counter before/after and paste both outputs.
(2) `## consoliderthese`: read `{LANE}/considerthese/` newest files (never edit); name at most ONE still-unimplemented proposal and whether this round implements it (with evidence) or not (with reason).
(3) `## Assimilation`: `none` with the reason (re-count `{LANE}/.ufo/waves/round-78/assimilation/collisions` lines if the file exists).
(4) A `## Gate` addendum: one admit and one reject (or a planned reject) for the non-author spot-check, drawn from the existing Gate block at {TIP} (verify each with `python3 tools/gate-records.py verify` and the hand location command). Note that this round has no new reject row and say whether that is honest.
Deliver at {W}/R85ScribeLesson/lesson-draft.md.
""")

spec = {"wave": "chousa-r85-w1", "reportDir": ".ufo/waves/round-85/w1", "context": CONTEXT, "items": items}
out = pathlib.Path(f"{LANE}/.ufo/waves/round-85/w1-spec.json")
out.write_text(json.dumps(spec, indent=2) + "\n")
print(f"wrote {out} with {len(items)} items; roles={sorted(i['role'] for i in items)}")
