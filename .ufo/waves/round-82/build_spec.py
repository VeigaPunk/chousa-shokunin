#!/usr/bin/env python3
"""Build the round-82 v1 wave spec (13 seats, one batched spawn handoff)."""
import json
import pathlib

LANE = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
SCRATCH = "/fast/scratch/hyaku/chousa-r82"
BASE = "142b6f0c08e645ef9507f6d880be44e518c39043"
EGRESS = "5d792e1e953649e801d9bf1f64093b1f0d4dac8c"
CONTROLS = "38f5af8268b2807811dded3d7d7221ff3f509495"
FREEZE = "57c0d16795db97ed09b69034e335e725ce577285"
LANDING = "b4a41d251b488f06b4a6ab01a11bc12ce72edd20"
W = f"{LANE}/.ufo/waves/round-82/w1"
E = "corpus/evidence/round82"

CONTEXT = f"""Lane chousa round 82, L1 ChousaR82 holds the canonical planner seat and integration. Root {LANE}. Revisions: base {BASE} (round-81 tip, closed rejected-honest-stop); egress table committed before any fetch {EGRESS}; prefreeze instruments + fixtures + captures {CONTROLS}; claim freeze (claims + prefreeze control receipts) {FREEZE}; candidate landing {LANDING} (the bytes you attack).
Frozen predicate set: {LANE}/{E}/claims.md — read it FIRST, including its kill rules. Two claims: C1 operability — `tools/research-gate.sh` refuses the round-81 K2 forms and a declared closed placeholder class through the UNCHANGED SKILL.md checklist item-2 and item-4 Run lines, counted by `{E}/k2-gate-r82.py` over `{E}/c1-manifest.tsv` + `{E}/c1-records/`, plus the gate `--selftest` for no-harm; C2 depth — one new entry `corpus/knowledge/question-framing-frames-r82.md` on registry rows S008 (re-opened), S209, S210, S211, counted by `{E}/depth-r82.py`. Before receipts: `{E}/controls/`; after receipts: `{E}/after/`. The claims are frozen: you never amend them, their counters, manifests, fixtures or receipts; you measure, attack and report. A kill-rule firing is the most valuable finding you can return; report it plainly.
Every `Report:` trailer path is relative to {LANE} — write it at {LANE}/<that path>.

Leaf only: no task tool, no subagents, no agent://all, no production edits, no lane or fleet git/jj mutation, no commits or pushes, no edits to /home/vgpnk/Projects/shokunin/scripts, /home/vgpnk/Projects/shokunin/.ufo/state, MANIFEST.json, considerthese/ or any sibling repo. The only files you write are under your own output folder {W}/<seat>/ plus your scratch dir. Network: none, except a seat whose item names a re-open (one GET per URL that has a 2026-11-06T19:42Z row in `corpus/evidence/round57/refetch.tsv`, into your scratch; never write `corpus/captures/` or `refetch.tsv`) — `{E}/egress-approval.md` is the table.

Scratch: every clone, archive tree, work dir and fixture lives under {SCRATCH}/<your seat name>/; create it with mkdir -p, pass it explicitly (TMPDIR=... HYAKU_SCRATCH=...), delete it before you yield (`trap 'rm -rf -- "$S"' EXIT` in shell, `finally: shutil.rmtree` in Python), and copy every receipt you cite into your wave output folder first. Never write under /tmp (the reaper deletes it; a /tmp path is never citable evidence). Use `git -C {LANE} archive <rev> | tar -x -C <scratch dir>` for a tree at a revision; any fixture git repo is `D=$(mktemp -d -p {SCRATCH}/<seat>) && git -C "$D" init -q`, every later git call names `-C "$D"`. Never mutate host sysctls or services. The gate selftest takes ~90 s and is CPU-heavy: run it at most twice per seat.

Counter that binds you: every finding names the exact command, the receipt path you wrote and the observed line plus exit code. An unrun check has not passed; a deviation from an expected value is a finding, never something to hide. End your report with one line `VERDICT: <seat> <claim> fired|held|n/a — <one sentence>` per claim you touched (plain text, not JSON).

Tooling authorization (operator, 2026-10-19): you may install or upgrade tools that help the task; read /home/vgpnk/.omp/agent/RULES.md first (official channels only; record tool/version/channel/reason in your report). pacman guard (orchestrator ruling 2026-10-20): all pacman transactions are PAUSED host-wide — install via `uv tool`/`npx`/an official binary in ~/.local/bin, or not at all; never -Sy/-Syu/-U/-R/downgrade/restart a host service."""

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


add("R82ExecRepro", "executor", f"""
Reproduce both frozen claims from committed bytes, before and after (C1 K1/K4, C2 K1).
(a) Instrument identity: `git -C {LANE} show <rev>:<path> | sha256sum` for every path in `{E}/instrument-pins.txt` at {CONTROLS}, {FREEZE} and {LANDING} (tools/research-gate.sh and SKILL.md are EXPECTED to differ at {LANDING}; the counters, manifest, base list and c1-records must not). Also confirm the item-2 and item-4 Run lines in SKILL.md are byte-identical between {CONTROLS} and {LANDING} (extract the first backtick span after `- Run: ` under each item).
(b) BEFORE/AFTER: archive {CONTROLS} and {LANDING} into scratch; in each run `python3 -B <tree>/{E}/k2-gate-r82.py --root <tree>` and `python3 -B <tree>/{E}/depth-r82.py --root <tree>`. Expected before: `K2_REFUSED=0/11 … CLASS_REFUSED=2/24 POSITIVE=5/6` `K2_GATE=FAIL` rc 1 and `DEPTH_R82 entries=0` FAIL rc 1; after: the exact predicate lines in claims.md, rc 0.
(c) At {LANDING} run `bash tools/research-gate.sh --selftest` once in the archived tree; expected `RESEARCH_GATE_SELFTEST: PASS (280 cases, 0 skipped)`.
(d) Re-run the committed control driver from an archive of {FREEZE}: `HYAKU_SCRATCH={SCRATCH}/R82ExecRepro bash <tree>/{E}/run-controls-r82.sh {CONTROLS} {W}/R82ExecRepro/controls-rerun` (run it with cwd = the archived tree; the driver archives REV from the lane repo it is located in — say whether that resolves to the lane or the scratch tree and adapt by running it from {LANE} if needed, without writing into the lane) and diff each summary/verdict line against `{E}/controls/`.
Receipts in {W}/R82ExecRepro/.
""")

add("R82ExecForms", "executor", f"""
Fire-or-hold C1 kill rule K2 (generalization) — author NEW records the frozen manifest does not contain, inside the declared class of claims.md K2 (a)/(b)/(c), and run the frozen Run lines on them at {LANDING}.
Work in an archive of {LANDING} in scratch; put records under `<tree>/{E}/r82-forms/`; run from the tree root exactly the SKILL.md item-2 line (`f=<record>; ! bash tools/research-gate.sh verify "$f" --root . | grep -q '^FINDING NEGATIVE_WITHOUT_SWEEP' && bash tools/research-gate.sh verify-sweeps "$f" --root .`) or item-4 line (`bash tools/research-gate.sh verify-sweeps <record> --root .`).
Cover, at least: every vocabulary value of claims.md in each of the four cells (reason, flip, where, claim sweep) starting from `{E}/c1-records/item2-pass.md`, `item4-pass.md`, `sweeps-r5.md`; case, surrounding whitespace, backticks, double quotes, `**bold**`, trailing period variants; NBSP/tab inside or around the value; unicode look-alikes (fullwidth slash `n／a`, U+2012/U+2015 dashes); headings `## Rejected`, `## REJECTIONS`, `## Kept rejections (2)`, `### Rejected sources`, a rejection table inside a fenced block; a negative claim with sweep `W1` while `## Sweeps` declares `w1` (case), a sweep cell `W1,` / `W1;W9` / `[W1]` / `` `W1` ``, a claim kind `Negative` / `negative ` ; two `## Claims` sections; a negative claim whose sweep row exists but has status `not-applicable`.
For each record: K2 class membership per claims.md (yes/no and why), rc, decisive output line. Any in-class record with rc 0 FIRES K2 — say so. Out-of-class passes are residuals: list them separately. Receipts + records in {W}/R82ExecForms/.
""")

add("R82ExecHarm", "executor", f"""
Fire-or-hold C1 kill rule K3 (harm): find records the base gate passes and the landed gate refuses, that carry none of K2's forms.
(1) Archive {CONTROLS} (base gate) and {LANDING} (landed gate) into scratch. Collect every record-shaped Markdown file in the lane that has a `## Rejections`, `## Sweeps`, `## Negatives` or a `## Claims` table with a `negative` row: `git -C {LANE} grep -l -E '^## (Rejections|Sweeps|Negatives|Rejected)' {LANDING} -- corpus .ufo` and the fixtures under `corpus/fixtures/` (incl. `archives-r9/`, `full-r6*.md`, `integrity-r7*.md`, `sweeps-r5*.md`, `chain-r3*.md`).
(2) Run `bash tools/research-gate.sh verify-sweeps <file> --root .` (and `verify-all <file> --root .`) from each tree root on each file; tabulate base rc vs landed rc and the RESEARCH_GATE line.
(3) For every base 0 → landed non-0 transition, decide whether the file carries a K2 form (placeholder cell, reject-heading rejection incomplete, unresolved negative). A transition without a K2 form FIRES K3. A transition on a file that genuinely carries the defect is a correct new refusal — list it (these are the gate's real catches on lane history).
(4) Also diff the full `--selftest` case list output between the two trees (one run each) — every base case must still be `ok-case` with the same exit.
Receipts in {W}/R82ExecHarm/ (table.tsv + per-file outputs for transitions).
""")

add("R82ExecTrial", "executor", f"""
End-to-end trial of the lane's method on this round's real question, through the landed checklist at {LANDING}.
Question: "For a chousa research record whose question maps what exists (not a test of an effect), what question frame applies and what must the record keep separate?"
(1) In an archive of {LANDING} in scratch, write a research record in the lane's record v1 grammar (study `corpus/fixtures/sweeps-r5.md`, `corpus/fixtures/full-r6.md`) at `<tree>/{E}/trial/record.md`: `## Question`; `## Sources` pointing to the committed capture texts `corpus/captures/bcb4a695b2aa019305121cff.txt` (S210) and `corpus/captures/fd7eed5e0e6c64e22bc1470c.txt` (S008); `## Claims` with observation claims whose spans are verbatim in those captures; one negative claim (e.g. "no base knowledge entry before round 82 held a question-frame decision table") with a `## Sweeps` row naming the local glob(s) it looked at; a `## Rejections` row (e.g. S028 as a source for question framing: wrong scope) with reason and flip; a `## Chain` with resolved hops; `## Approval`.
(2) Run from the tree root every applicable SKILL.md checklist Run line (items 1, 2, 3 if an entry is checked, 4, 6) plus `bash tools/research-gate.sh verify-all <record> --root .`; record each rc and verdict line.
(3) Make three mutated twins: rejection flip `TBD`; negative claim sweep cell naming an undeclared id; sweep `where` = `N/A`. Record that items 2/4 exit 1 on each with the expected finding id.
(4) Say plainly which checklist lines were awkward, wrong, or too strict in practice (false refusals on a reasonable record are K3 evidence — report them).
Copy the record, twins and receipts to {W}/R82ExecTrial/.
""")

add("R82ExecReopen", "executor", f"""
Fire-or-hold C2 kill rule K2: every counted quote re-derived from committed bytes, and re-opened live.
(1) From `git -C {LANE} show {LANDING}:corpus/knowledge/question-framing-frames-r82.md` extract the 11 `## Located quotes` rows (qid, source, quote) and the S028 quote lines of `corpus/knowledge/correction-retraction-status-r81.md` (round-82 addendum).
(2) For each: find the registry row in `{LANDING}:corpus/SOURCES.md`, compute key = sha256(URL)[:24], check `corpus/captures/<key>.txt` sha256 equals the LAST successful `corpus/evidence/round57/refetch.tsv` row for that id/URL (fetched 2026-11-06T19:42Z), and test the quote's presence after whitespace collapse (and curly-quote folding) — report each; `wc -w` each quote (must be 8–25 for the 11 counted).
(3) Live: one GET per URL (S008, S209, S210, S211, S028) with `curl -fsSL --compressed --max-time 30 -A 'Mozilla/5.0 (X11; Linux x86_64)'` into scratch; strip tags, collapse whitespace; test each quote; compare live sha256 with the committed `.raw` (dynamic pages differ — record, do not fire). Also try `python3 {LANE}/tools/quote-reopen.py verify --items <tsv>` from {LANE} on the five URLs' quotes and record its verdicts.
K2 fires only on a capture/refetch mismatch or a quote absent from its committed capture. Receipts in {W}/R82ExecReopen/.
""")

add("R82ReviewerEntry", "reviewer", f"""
Fire-or-hold C2 kill rule K3 — the semantic check the counter cannot do (claims.md states the salad boundary).
For each of the 9 decision-table rows of `corpus/knowledge/question-framing-frames-r82.md` at {LANDING}: open each warranting quote IN CONTEXT in the committed capture text (`{LANE}/corpus/captures/<key>.txt`; keys in the entry header and SOURCES anchors; S008 = fd7eed5e…, S209 = 21323730…, S210 = bcb4a695…, S211 = 97223722…) — read at least the surrounding paragraph — and judge the row's Do and its Never separately: supported / overreach / contradicted, with a ≤25-word located passage for each judgment. A row whose Do or Never is contradicted by, or not supported by, its warranting quote in context FIRES K3 (one row suffices) — say so plainly.
Also review: the `## Inference` and `## Limits` sections (is the inference marked as the lane's own?); the four registry rows S008/S209/S210/S211 and the S028 row (tier, scope, anchor, teaches vs source); the round-82 Crossmark addendum in `corpus/knowledge/correction-retraction-status-r81.md` (is the "never" clause honest about being inference?); whether the entry transfers health-synthesis guidance beyond what the sources support.
Report at {W}/R82ReviewerEntry/review.md.
""")

add("R82ReviewerGate", "reviewer", f"""
Code review of the C1 gate change: `git -C {LANE} diff {FREEZE} {LANDING} -- tools/research-gate.sh SKILL.md`.
Check: `sweep_is_placeholder` normalization (locale: run under `LC_ALL=C` and `LC_ALL=C.UTF-8` — does `${{v,,}}` or the `—`/`–` match change?), the rejection-section loop (duplicate headings, a heading named `Rejections` appearing twice, SEC_ORDER contents, a `## Rejected claims` table with a different schema), the negative-resolution block (multiple Claims tables, empty SWEEP_ROWS, `local` declared inside a loop, `read -r -a` word splitting with globs disabled or not, ids differing in case), interaction with `verify-all` (does the composed verdict for the sweeps section change for any fixture under `corpus/fixtures/`? run `bash tools/research-gate.sh verify-all <fixture> --root .` at both {FREEZE} and {LANDING} trees for the fixtures that carry sweeps/rejections), `--json` output if any, the five new selftest cases (do they assert the new finding ids and would they fail if the patch were reverted? prove one by running that case's record against the {FREEZE} gate), and the accuracy of every new SKILL.md / header-comment sentence (one command each).
Report defects with severity at {W}/R82ReviewerGate/review.md. A defect that makes an in-class K2 record pass is a C1 K2 firing; a false refusal of a K2-free record is a C1 K3 firing — say which.
""")

add("R82CriticClaims", "critic", f"""
Falsify the round as declared. Read claims.md, the control receipts (`{E}/controls/`), the after receipts (`{E}/after/`), the round-79/80/81 spot-checks in `corpus/lessons/`, and the round's commit sequence (`git -C {LANE} log --format='%H %cI %s' {BASE}..{LANDING}`).
Attack: (1) ordering — egress commit time vs first round-82 refetch row; controls executed and committed before freeze; freeze before any gate/entry byte (diff {CONTROLS}..{FREEZE} must touch only claims/pins/receipts); (2) cheapest controls — build the cheapest tree you can that reaches either predicate WITHOUT the claimed work (e.g. a gate that special-cases the manifest's file names or note lines; an entry reusing the positive-control fixture `{E}/c2-controls/P1-positive/ctl-entry-r82.md`; S-rows faked with a committed capture you write yourself into scratch) and score it with the frozen counters — say what each cheap tree needed and whether it is the claimed work in disguise; (3) is C1 really operability (does the checklist become more executable for a user?) or calibration/quality; is C2 depth or coverage (§9 rule: name the axis by the surface changed); (4) causal separability — score C1 on a tree with knowledge/SOURCES at {CONTROLS} and C2 on a tree with the gate at {CONTROLS}; (5) does the declared closed vocabulary make C1 a narrow, list-memorizing fix — argue both sides with evidence; (6) any frozen rule changed after scoring.
Report at {W}/R82CriticClaims/critique.md, each attack with its command and receipt.
""")

add("R82MutationGate", "mutation-tester", f"""
Mutation-test the C1 gate patch and both frozen counters.
(A) Gate: in an archive of {LANDING}, make ≥12 single mutants of the round-82 hunks of `tools/research-gate.sh` (drop each placeholder value class, drop the `while … *.` period strip, drop backtick/quote folding, restrict the reject-heading match to `Rejections`, drop placeholder→junk in `sweep_token_class`, drop SW_CLAIMS / SW_IDS[cid] / token match in negative resolution, invert `nres`, emit the negative finding as `info`, …). For each run `python3 -B <tree>/{E}/k2-gate-r82.py --root <tree>` and record which manifest rows catch it; survivors that no manifest row catches are coverage gaps — say which K2 form a survivor would let through. Run the gate selftest on at most two mutants (CPU) and say whether the five new cases catch them.
(B) Counters: ≥8 mutants each of `{E}/k2-gate-r82.py` (drop FROZEN_RUNLINE check, accept rc 2 as refusal, drop the verify-mode finding union, PASS on `>=` partial, …) and `{E}/depth-r82.py` (drop E3 capture check, drop ROUND_START, drop E4/E5/E6/E7, lower row floor, …); score each against the committed control set by running the committed driver on a mutated copy (`HYAKU_SCRATCH=<your scratch> bash <tree>/{E}/run-controls-r82.sh {CONTROLS} <out>` from a tree whose counters are mutated — read the driver to see which copy of the counters it runs) and say which control kills it. Round-81 survivors (12/18, 9/17) are the bar to beat.
Report at {W}/R82MutationGate/mutants.md with a table mutant → killed/survived → killer.
""")

add("R82ScoutNovelty", "scout", f"""
Per-surface reconnaissance for C2 K4 (ground already held) and the frontier. Read-only.
(1) At base {BASE}: does any `corpus/knowledge/*.md`, `corpus/README.md` or `SKILL.md` already hold a decision table or decision list on choosing or aligning a review question frame (PICO levels, PCC, PECO/SPIDER, objective–question–eligibility alignment, protocol deviations)? `git -C {LANE} grep -n -i -E 'PICO|PCC|PECO|SPIDER|question fram|answerable question|eligibility criteri|protocol deviation|review question' {BASE} -- corpus/knowledge corpus/README.md SKILL.md PROVINCE.md`. For every hit quote the line and judge: same ground (fires K4), adjacent, or unrelated. claims.md names two near neighbours; judge them too.
(2) Registry at {LANDING}: duplicate URLs for S209–S211/S008/S028 (census W04), rows still `queued` that the new entry could have cited, and whether S008's re-open changed anything the row says.
(3) `corpus/README.md` coverage map: which coverage row the entry belongs under; is the round-82 README section accurate?
Report at {W}/R82ScoutNovelty/recon.md with a command per finding.
""")

add("R82ConnectorSiblings", "connector", f"""
Sibling-overlap scan, read-only: does another lane hold knowledge on research question framing (PICO/PCC/PECO, eligibility from the question) or a gate that refuses placeholder cells (`n/a`, `TBD`, `-`) in records?
Search `/home/vgpnk/Projects/shokunin/*-shokunin/` (excluding chousa) with `grep -rn -i -E 'PICO|PCC|PECO|question fram|eligibility criteri|placeholder|n/a|TBD' --include=*.md --include=*.py --include=*.sh` (limit output sensibly). For each relevant hit: file:line, quote, and whether it is contested scope with chousa's province (`{LANE}/PROVINCE.md`), a stronger sibling mechanism worth noting, or unrelated. Pin each sibling's revision (`git -C <repo> rev-parse HEAD`). Absorb nothing. Report at {W}/R82ConnectorSiblings/scan.md.
""")

add("R82ScribeLesson", "scribe", f"""
Draft (do not land) `corpus/lessons/round-82.md` sections in the lane's lesson format (study `{LANE}/corpus/lessons/round-81.md`).
(1) `## Gate`: one record per registry row touched this round — S008 (re-opened; status queued→mined, anchor and used-by changed), S209, S210, S211 (new), S028 (queued→mined, anchor and used-by changed) — with URL, access time (the 2026-11-06T19:42Z refetch rows in `corpus/evidence/round57/refetch.tsv`), tier, decision, a ≤25-word quote located in the committed capture text (`{LANE}/corpus/captures/<key>.txt`) with its `wc -w` count and the command that locates it; log every status/anchor/recheck/used-by change old→new (`git -C {LANE} diff {BASE} {LANDING} -- corpus/SOURCES.md`). Include ≥1 reject from the round's material: e.g. S209's page title changed (slug vs title) — admit or reject with reason; any candidate the L1 did not take (SPIDER, PRISMA-ScR) as a reject-for-now with flip.
(2) `## Mistakes`: mine ONE mistake: R81ReviewerC2 described its record `r4-07-alt-section.md` as "reason present, flip empty" while its bytes carry a complete rejection (diff against `corpus/evidence/round81/checklist-fixtures/item4-pass.md`), and the round-81 closure counted it among eleven K2 records. Class · evidence pointer · captured-by · fix, with a fix shown able to fail (a command whose failing output you paste, e.g. a check that a seat-described defect form is present in the record's bytes).
(3) `## considerthese`: read `{LANE}/considerthese/` newest files (never edit); name at most ONE still-unimplemented proposal and whether this round implements it (with evidence) or not (with reason).
(4) `## Assimilation`: `none` with the reason (round-78 package collision file `{LANE}/.ufo/waves/round-78/assimilation/collisions`; re-count its lines).
Deliver at {W}/R82ScribeLesson/lesson-draft.md.
""")

add("R82SentinelScope", "sentinel", f"""
Boundary and safety sentinel for round 82. Read-only.
(1) Egress: `{E}/egress-approval.md` was committed at {EGRESS} — compare `git -C {LANE} log -1 --format=%cI {EGRESS}` (convert to UTC) with every refetch.tsv row dated 2026-11-06 after 19:00Z; every fetch a GET of a URL in the table's intended-targets list, no credentials (read `tools/capture-fetch.py` argv). Report whether round-81 routed defect 3 (table written after fetches) is closed.
(2) Province: does the new entry or the gate change absorb sibling province (kengaku model quality, kasegi bounty scope, kumitate orchestration, kagi secrets)? Quote `PROVINCE.md` and the entry lines.
(3) Secrets: scan `git -C {LANE} diff {BASE} {LANDING}` and the five new captures for credential-shaped strings (tokens, keys, cookies, session ids — the Confluence pages carry `requestCorrelationId`; judge it) — shape only, never print a value.
(4) Misroot: `git -C /home/vgpnk/Projects/shokunin status --porcelain` — list any untracked fleet-root file whose content names chousa round 82 (do not move or delete anything; report paths).
(5) Scratch: `du -sh {SCRATCH} 2>/dev/null; ls /tmp | grep -i r82` — report leftovers.
Report at {W}/R82SentinelScope/sentinel.md.
""")

spec = {"wave": "chousa-r82-w1", "reportDir": ".ufo/waves/round-82/w1", "context": CONTEXT, "items": items}
out = pathlib.Path(f"{LANE}/.ufo/waves/round-82/w1-spec.json")
out.write_text(json.dumps(spec, indent=2) + "\n")
print(f"wrote {out} with {len(items)} items; roles={sorted(i['role'] for i in items)}")
