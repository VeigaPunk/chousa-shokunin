#!/usr/bin/env python3
"""Build the round-80 v1 wave spec (12 seats, one batched spawn handoff)."""
import json
import pathlib

LANE = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
SCRATCH = "/fast/scratch/hyaku/chousa-r80"
BASE = "b7803829922770b890e9f4efdd30d12c3695439a"

CONTEXT = f"""Lane chousa round 80, L1 ChousaR80 holds the canonical planner seat and integration. Root {LANE}; base revision (round-79 lane tip, closed `ok` / `rejected-honest-stop`): {BASE}.
Frozen predicate set: {LANE}/corpus/evidence/round80/claims.md — read it FIRST; every item below attacks or reproduces one of its two frozen claims (C1 operability, C2 calibration). Read {LANE}/corpus/lessons/round-79-verifier-spotcheck.md (the non-author closure of the previous round) before you score anything.
Every `Report:` trailer path is relative to {LANE} — write it at {LANE}/<that path>.

Leaf only: no task tool, no subagents, no agent://all, no network, no production edits, no lane or fleet git/jj mutation, no commits or pushes, no edits to /home/vgpnk/Projects/shokunin/scripts, /home/vgpnk/Projects/shokunin/.ufo/state, MANIFEST.json or any sibling repo. The only files you write are under your own output folder {LANE}/.ufo/waves/round-80/w1/<seat>/ plus your scratch dir. Frozen artifacts are never amended: everything under {LANE}/corpus/evidence/round79/ and {LANE}/corpus/evidence/round80/ is read-only for you (copy to scratch to mutate).

Scratch: every clone, mirror, work dir and fixture lives under {SCRATCH}/<your seat name>/; create it with mkdir -p, pass it explicitly (TMPDIR=... --work ...), delete it before you yield (`trap 'rm -rf -- "$S"' EXIT` in shell, `finally: shutil.rmtree` in Python), and copy every receipt you cite into your wave output folder first. Never write under /tmp (the reaper deletes it and a /tmp path is never citable evidence). One live clone per seat: `git clone --shared` or `git archive`.

Counter that binds you: every finding names the exact command, the receipt path you wrote and the observed line plus exit code. An unrun check has not passed; a deviation from an expected value is a finding, never something to hide. Instrument bytes you cite are the committed bytes: quote the sha256 you measured.

Tooling authorization (operator, 2026-10-19): you may install or upgrade tools that help the task; read /home/vgpnk/.omp/agent/RULES.md first (official channels only; record tool/version/channel/reason in your report). pacman guard (orchestrator ruling 2026-10-20): all pacman transactions are PAUSED host-wide — install via `uv tool`/`npx`/an official binary in ~/.local/bin, or file nothing; never -Sy/-Syu/-U/-R/downgrade/restart a host service."""

GODSPEED = """You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.
"""

items = []

items.append({
    "name": "R80ExecA", "role": "executor",
    "prompt": GODSPEED + f"""
Reproduce frozen claim C1 (operability) in both directions and measure the fresh leg's contribution.

(a) BEFORE (the committed do-nothing control, re-run by you): `python3 -B {LANE}/corpus/evidence/round80/oracle-check.py --battery {LANE}/corpus/evidence/round79/matrix-battery-v6.py --oracle {LANE}/.ufo/waves/round-79/w1/R79ExecC/matrix-structure-identity.py --work {SCRATCH}/R80ExecA/oracle --runs 1` — expected `BATTERY_EXIT=0 BATTERY_VERDICT=PASS RECEIPT_LINES=113`, `ORACLE=ACCEPTED`, exit 1.
(b) AFTER: `python3 -B {LANE}/corpus/evidence/round80/matrix-battery-v7.py --matrix {LANE}/corpus/evidence/round76/loader-matrix-v3.py --work {SCRATCH}/R80ExecA/v7 --runs 1 --fresh 2` — expected exit 0 and the exact line `BATTERY=PASS forgers_rejected=11/11 positive=2/2 fresh_positive=2/2 fresh_forgers=2/2 oracles_rejected=5/5`.
(c) The fresh leg's contribution: the same command with `--no-fresh`. State exactly what line it prints and its exit code; that is the measurement of whether the drawn set is load-bearing or decoration.
(d) `--fresh 3` with a different draw seed (if the tool exposes one; otherwise two independent runs) — are the fresh legs stable, and do the drawn subjects differ between runs? Record the drawn subject ids/hashes each run prints.

Save each run's stdout+stderr and its exit code as a receipt in your folder (`.ufo/waves/round-80/w1/R80ExecA/`). Report every observed predicate line verbatim, any deviation (that is a finding, not a failure to hide), the wall clock of each run, and the free space `df -h /fast` showed before and after. Do not edit the instruments.
"""})

items.append({
    "name": "R80ExecB", "role": "executor",
    "prompt": GODSPEED + f"""
Reproduce frozen claim C2 (calibration) in both directions, including the after state the L1 intends to land — you validate the record grammar before it lands.

(a) BEFORE: `python3 -B {LANE}/corpus/evidence/round80/gate-grounding-check.py --rev {BASE}` — expected `GATE_GROUNDING=FAIL unresolved=3 superseded_resolved=0 audited=S196,S197,S198`, exit 1, with `record=none` on all three rows. Copy the tool into a scratch mirror at the same repo-relative path so its `LANE` (`parents[3]` of `__file__`) resolves to the mirror.
(b) AFTER, in a scratch `git init` mirror at {SCRATCH}/R80ExecB/mirror (assert `git -C <mirror> rev-parse --show-toplevel` equals the mirror before the first commit): copy `corpus/`, `LOG.md`, `SCORECARD.md`, and add four candidate rows S199/S200/S201/S202 plus four `GATE-RECORD` lines exactly in the grammar `{LANE}/corpus/evidence/round80/gate-grounding-check.py` parses (`GATE-RECORD S### rev=<40-hex> path=<repo-relative> line=<n> words=<w> quote=<verbatim substring of that line>`). Candidate content (verify every quote yourself against `git show <rev>:<path>`; correct any that does not occur verbatim or whose word count is wrong, and say so):
  - S199, rev {BASE}, path corpus/lessons/round-79-verifier-spotcheck.md, line 222, quote `the battery is fully forgeable through the payload channel on **both** batteries`
  - S200, rev {BASE}, path corpus/QUALITY.md, line 1056, quote `A subject-identity salt is defeated by any normalizer that knows its marker family, so the closure is a per-channel measurement`
  - S201, rev {BASE}, path corpus/QUALITY.md, line 1054, quote `A self-assessment counter validates each resolution line against the bytes it claims to repair, and its audit window covers every block rather than the newest.`
  - S202, rev 3eb4a3cad8febf75698a017cb6c4441f763b3454, path .ufo/waves/round-78/w1/R78ReviewB/atkB2-new-block-window.txt, line 11, quote `SELFCHECK=PASS unresolved=0/3`
  S200/S201/S202 must carry `teaches` opening `supersedes S196 —` / `supersedes S197 —` / `supersedes S198 —` so the counter treats the parents as superseded.
(c) Run the counter against the mirror commit: expected `GATE_GROUNDING=PASS unresolved=0 superseded_resolved=3 audited=S199,S200,S201,S202`, exit 0. Report the exact line. If any record fails R1-R4, report which rule and why — that is the finding that matters.
(d) One negative control in the mirror: change one `words=` cell to a value one off the real count and confirm the counter reports R4 and non-zero exit; revert.

Receipts in `.ufo/waves/round-80/w1/R80ExecB/`, including the mirror's `git log --format='%H %s'`. Never commit anywhere but the scratch mirror (identity `t <t@t>` is forbidden on the lane and fleet repos).
"""})

items.append({
    "name": "R80ExecC", "role": "executor",
    "prompt": GODSPEED + f"""
Measure the limit C1 records rather than claims closed: can a classifier that never scores a subject reach v7's PASS line?

Read `{LANE}/corpus/evidence/round80/matrix-battery-v7.py` (how it draws fresh positives and fresh forgers: the rewrite operators, the ground-truth witness matrix) and `{LANE}/corpus/evidence/round79/matrix-battery-v6.py`. Write, in your own folder, a classifier that sees only the drawn subject's bytes (never the ground-truth label, never a run) and tries to separate fresh positives from fresh forgers statically — e.g. by reversing the documented rewrite operators, by diffing against the committed positives it was derived from, or by any structural feature.
Measure: over N>=5 independent draws (`--fresh 3` each), how many drawn subjects your classifier labels correctly, and what a matrix built on that classifier scores in the battery (run v7 with `--matrix <your classifier wrapper>`; report the exact predicate line it prints and its exit). A classifier that reaches `BATTERY=PASS` is a falsification of C1's after-predicate — report it as such, with the receipt. A classifier that cannot is the measured limit.
Also state, with a command, whether the drawn subjects are recoverable by the committed a10 payload-decoder ({LANE}/corpus/evidence/round80/forgers/a10-payload-decode.py) when that decoder is used as the matrix.

Receipts in `.ufo/waves/round-80/w1/R80ExecC/`. Delete your scratch dir before you yield.
"""})

items.append({
    "name": "R80ScoutA", "role": "scout",
    "prompt": GODSPEED + f"""
Per-surface reconnaissance of the lane's Gate-record surface — the ground C2 moves on. Read-only.

1. Enumerate every lesson file under `{LANE}/corpus/lessons/` whose name matches `round-<n>.md` with n >= 70 (`git -C {LANE} show {BASE}:<path>` for the base bytes). Extract every located quote a lesson's `## Gate` block states (the quoted string plus any `wc -w` count the prose asserts). For each: re-open the cited path at the cited revision, `grep -c` the quote at the cited line, and compute the count yourself. Report a table of row id, lesson, cited location, quote, stated count, measured count, and `ok|mismatch|absent`.
2. Report every record that is defective in that sense beyond S196/S197/S198 (the three the round-79 closure named). Each entry names the command and its output.
3. Separately: enumerate which registry rows the counter `{LANE}/corpus/evidence/round80/gate-grounding-check.py` would audit at `--rev {BASE} --since-round 79` and which rows escape because their `- Admit|- Reject` line sits in an older lesson (`--since-round 60` and `--since-round 1` deltas). That window is the counter's own blind spot; name its size.
4. Report where `corpus/lessons/round-79.md`'s `## Gate` states a word count that its own quote does not have (S196 states 25, S197 states 24 — verify or refute each with `wc -w`).

Write the survey at `.ufo/waves/round-80/w1/R80ScoutA/survey.md` with a `command → output` block per claim. No production edits.
"""})

items.append({
    "name": "R80ScribeA", "role": "scribe",
    "prompt": GODSPEED + f"""
Draft the registry and Gate material for C2 (calibration) — draft only, in your own folder; the L1 lands it.

Produce `.ufo/waves/round-80/w1/R80ScribeA/draft-sources-rows.md`:
1. Four `corpus/SOURCES.md` registry rows, 11 cells, exact schema from `{LANE}/corpus/SOURCES.md` header (`| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |`), no `|` inside a cell:
   - S199 own-work B, source = the round-79 non-author spot-check's payload/structure finding, anchor = `{BASE}`, line 222, status mined, used-by `corpus/lessons/round-80.md`.
   - S200 `teaches` opens `supersedes S196 — ` and re-states QUALITY 147's requirement, anchor = `{BASE}`, criterion 147 at line 1056.
   - S201 `teaches` opens `supersedes S197 — ` and re-states QUALITY 146's requirement, anchor = `{BASE}`, criterion 146 at line 1054.
   - S202 `teaches` opens `supersedes S198 — ` and refiles the rejection with the corrected anchor (the cited receipt is 11 lines, not 20), status rejected, used-by `—`.
2. Four `GATE-RECORD` lines in the exact grammar `GATE-RECORD S### rev=<40-hex> path=<repo-relative> line=<n> words=<w> quote=<verbatim substring>`, one per new row. For each, verify with a command that the quote is a verbatim substring of that line at that revision and that `words=` equals `wc -w`; quote the command and its output beside each line. Every quote must be <=25 words.
3. The `## Gate` prose block for `corpus/lessons/round-80.md`: per row, URL-or-path + access date (2026-11-04) + located quote + what it grounds, plus the old->new record correction (S196/S197/S198 -> S200/S201/S202) with the measured old and new word counts, plus one explicit line that no URL was fetched (revision-pinned committed paths only), plus the non-author spot-check request line.

Do not edit `corpus/SOURCES.md` or any lesson yourself. Every count you state is measured by you, not copied from this prompt — correct any number here that the bytes contradict.
"""})

items.append({
    "name": "R80ScribeB", "role": "scribe",
    "prompt": GODSPEED + f"""
Draft the lesson's learning material and the append-only corrections the round-79 closure routed — draft only, in your own folder; the L1 lands it.

Read `{LANE}/corpus/lessons/round-79-verifier-spotcheck.md` section 5 (routed defects 1-8) and `{LANE}/corpus/lessons/round-79.md`. Produce `.ufo/waves/round-80/w1/R80ScribeB/draft-lesson.md`:
1. `## Mistakes` rows (class | evidence pointer | captured-by | fix) for THIS round: the provider-failure death of round-80 attempt 1 and what it left (a claims file and instruments committed without a wave, a tee'd control receipt, `/tmp/r80-base`-style scratch outside `$HYAKU_SCRATCH`), and at least one mistake the round's own instruments caught. A fix counts only if you name the check that can fail; if you find none, paste the sweep that found none.
2. The append-only correction text for routed defect 4 (the `LOG.md` §Round 79 sentence contradicting the receipt — draft the exact correction entry, naming `SELFCHECK2=PASS unresolved=0/3` and the duplicate-116 window), defect 3 (the report's `LANDING` placeholder — draft an erratum naming `acca24498b8259d179db144a8bb2d44c0935e2c1`), and defect 5 (QUALITY 150-151 under a `## Round-80 addition` heading although they are round-79 findings — draft the record sentence for the lesson).
3. A `QUALITY.md` criterion draft for routed defect 6: a control receipt names the lane revision it was measured at (`REV=<40-hex>`), and a located quote is re-opened, `grep -c`'d at the named location and `wc -w`'d before a row is written. State its check as a command an auditor can run.
4. One `considerthese/` proposal mined per the operator's rule: read `{LANE}/considerthese/2026-10-26.md` (the newest) and pick at most one still-unimplemented proposal that fits the round; ground it against the repo bytes it points at (open them) and draft the lesson/QUALITY line it would land as. If nothing there fits, say so with the list of proposals you read.

Every claim in your draft carries the command and output that produced it. No edits outside your folder.
"""})

items.append({
    "name": "R80ReviewerA", "role": "reviewer",
    "prompt": GODSPEED + f"""
Attack frozen claim C1 (operability). Your job is to make it fail, not to confirm it.

C1's predicate: `python3 -B {LANE}/corpus/evidence/round80/matrix-battery-v7.py --matrix {LANE}/corpus/evidence/round76/loader-matrix-v3.py --work DIR --runs 1 --fresh 2 --rev REV` exits 0 printing exactly `BATTERY=PASS forgers_rejected=11/11 positive=2/2 fresh_positive=2/2 fresh_forgers=2/2 oracles_rejected=5/5`; its kill rule fires if any enumerated forger/positive/fresh case/oracle is a MISS or the legitimate matrix is refused.

1. Re-run the predicate yourself at the base revision and record the exact line + exit.
2. Try to reach the PASS line with a matrix that does not score subjects: the round-79 structure-identity matrix `{LANE}/.ufo/waves/round-79/w1/R79ExecC/matrix-structure-identity.py`, the payload decoder `{LANE}/corpus/evidence/round80/forgers/a10-payload-decode.py`, and any variant of your own. Report the line each prints and its exit.
3. Try to make the legitimate matrix be refused (blanket refusal is not a gain): e.g. a `--work` path with a space, a read-only work dir, a slow matrix under `--matrix-timeout 1`, a copy of the legitimate matrix whose trailing bytes differ. Each attempt: command, line, exit.
4. Audit the enumerated oracle list: read v7's source and list the five oracles it counts. Is the count bound to a fixed table (so a sixth, newly written oracle escapes the predicate)? Name the file:line where the list is fixed.

Receipts in `.ufo/waves/round-80/w1/R80ReviewerA/`. A finding that falsifies the claim is the deliverable; say `NOT FALSIFIED` only with the commands that tried.
"""})

items.append({
    "name": "R80ReviewerB", "role": "reviewer",
    "prompt": GODSPEED + f"""
Attack frozen claim C2 (calibration). Read `{LANE}/corpus/evidence/round80/gate-grounding-check.py` in full first.

1. Forge `GATE-RECORD` lines that satisfy R1-R4 while grounding nothing: a real quote on a real line of a real path at a real revision that does not support the row's `teaches`; a quote that appears on the line only because the line is enormous (the round-79 spot-check's line 222 is 100+ words); a `words=` value that matches its own quote but a `quote=` that is 25 words of boilerplate. For each, run the counter on a scratch mirror and report the exact output line and exit — a PASS is a finding against R1-R4's discriminating power.
2. Test the supersession arithmetic: a parent row whose replacement record passes while the parent's own defect is untouched (a label-only repair), and a chain S196 -> S200 -> S203 where the counter only looks at the last record. Report what `superseded_resolved` counts and whether a re-filing can be scored as a resolution.
3. Test the `decided` window: a row named only by a `- Admit S###` line in a lesson older than `--since-round` is never audited. Build that case in a mirror and report the counter's line.
4. Measure whether `check()`'s R3 substring test accepts a quote that is a substring of a *different* line (off-by-one `line=`), and whether R4's bound is enforced at exactly 25 or at >=25.

Receipts in `.ufo/waves/round-80/w1/R80ReviewerB/`. Falsification is the deliverable.
"""})

items.append({
    "name": "R80CriticA", "role": "critic",
    "prompt": GODSPEED + f"""
Falsify the two frozen predicates themselves — their wording, their kill rules and their before-receipts — before the round is reported.

Read `{LANE}/corpus/evidence/round80/claims.md` and the committed before-receipts it names (`{LANE}/corpus/evidence/round80/controls/grounding-before.txt`, `oracle-structure-v6-accepted.txt`, `v7-legit-matrix-prefreeze.txt`, `v7-legit-matrix-after.txt`).

1. C1: does the predicate enumerate exactly the set its kill rule counts (the round-79 C1 failure shape: predicate counts six forgers, kill rule says "any forger")? Name every clause of the predicate and every clause of the kill rule, and any asymmetry. Then test the one clause most likely to be reachable without work: `oracles_rejected=5/5` — is a sixth oracle, written today, rejected by construction or only by the fixed list?
2. C2: does the predicate's `superseded_resolved=3` measure a resolution or a re-filing? Does `audited=S199,S200,S201,S202` name rows that exist only because this round added them (i.e. is the counter's after-state produced by the round's own new rows, so a do-nothing round with four hand-written rows and four records would also pass)? Build that do-nothing control in a scratch mirror: base bytes + four rows whose `teaches` says `supersedes` + four records, no corrections, no criterion, no fix. Run the counter. If it prints PASS, say plainly that C2's counter is satisfied by bookkeeping and name what the claim would have to count instead.
3. Check the claims file's own consistency: instrument sha256 values it lists versus the committed bytes (`sha256sum {LANE}/corpus/evidence/round80/*.py {LANE}/corpus/evidence/round80/forgers/*.py`), and whether the receipt `v7-legit-matrix-after.txt` names a revision or a worktree.

Receipts in `.ufo/waves/round-80/w1/R80CriticA/`. Report every asymmetry as a numbered finding with the command that shows it.
"""})

items.append({
    "name": "R80MutationA", "role": "mutation-tester",
    "prompt": GODSPEED + f"""
Mutation-test the two instruments of this round: a guard that no mutant can kill is decoration.

In a scratch copy (never the committed bytes):
1. `{LANE}/corpus/evidence/round80/gate-grounding-check.py` — produce at least six mutants, one per declared rule and one per arithmetic step: drop the R1 `cat-file -e` test; accept any rev whose 12-char prefix resolves; skip the R3 substring test; accept a line index off by one; drop the `words != int(record['words'])` equality; drop the `words > 25` bound; treat every row as superseded so `audited` is empty. For each mutant, run it against a scratch mirror in the AFTER state (four correct records) and an AFTER state with one defective record, and record which runs the mutant mis-scores. Mutants that survive are findings.
2. `{LANE}/corpus/evidence/round80/matrix-battery-v7.py` — at least four mutants: remove the fresh-draw leg; reuse one draw across runs; accept an oracle that reaches PASS; drop the passed-subject scoring (score only exit codes). Run each against the legitimate matrix and against the structure-identity oracle; record the exact predicate line and exit for each mutant. A mutant that keeps printing the PASS line on the oracle is a live hole.
3. Report a mutation score per instrument (`killed/n`) with the receipt path for each run.

Receipts in `.ufo/waves/round-80/w1/R80MutationA/`. Delete scratch before yielding.
"""})

items.append({
    "name": "R80SentinelA", "role": "sentinel",
    "prompt": GODSPEED + f"""
Audit the round's committed artifacts for scope, leak and provenance defects. Read-only on everything outside your folder.

1. Scan `{LANE}/corpus/evidence/round80/` (all files) and `{LANE}/.ufo/waves/round-80/census-start.txt` for: absolute `/tmp/` or `/var/tmp/` paths (a `/tmp` path is never citable evidence), writes outside `$HYAKU_SCRATCH`, network calls (`urllib|requests|curl|wget|socket`), `subprocess` calls that mutate a repo (`git commit|git push|jj `), references to sibling lanes or the fleet repo as write targets, and credential-shaped strings (`BEGIN .*PRIVATE KEY`, `ghp_`, `sk-`, `op://`, token literals). Report file:line for each hit.
2. Verify the receipts name a revision: for each control receipt in `{LANE}/corpus/evidence/round80/controls/`, does it carry a 40-hex `REV=`/`LANE_REV=` line, or only `REV=worktree`? Count them and name the ones that do not.
3. Verify the instruments' declared sha256 against the committed bytes: `sha256sum` every `.py` under `corpus/evidence/round80/` and compare with the table in `corpus/evidence/round80/claims.md`.
4. Check the declared instrument limits: does `matrix-battery-v7.py` hardcode any absolute path, use `mkdtemp()` without honoring `TMPDIR` or `--work`, or read a file outside the lane? Grep and report with file:line.
5. Check the wave's own scope: does any committed file under `.ufo/waves/round-80/` name a fleet-repo or sibling-lane path as a write target?

Report at `.ufo/waves/round-80/w1/R80SentinelA/audit.md`, one numbered finding per item with the command and its output, plus a `CLEAN` line per numbered item that found nothing.
"""})

items.append({
    "name": "R80ConnectorA", "role": "connector",
    "prompt": GODSPEED + f"""
Sibling-overlap scan: does another lane already hold a stronger form of either move this round makes? Read-only, and never write outside your own folder.

1. Read the two instruments (`{LANE}/corpus/evidence/round80/gate-grounding-check.py`, `matrix-battery-v7.py`). For each, state the general method it implements in one sentence (e.g. "a registry record is bound to the bytes it quotes by revision+path+line+verbatim-substring+word-count").
2. Search the sibling lane repos under `/home/vgpnk/Projects/shokunin/` (tsukuroi-shokunin, kasegi-shokunin, souji-shokunin, kama-shokunin, mado-shokunin, kotoba-shokunin, kumitate-shokunin) for the same method: `grep -rn` for quote-location verification, revision-bound receipts, drawn-per-run fixtures, oracle rejection. For every hit, name the file:line, quote the mechanism, and say whether it is stronger, equivalent or weaker than this lane's.
3. For each stronger sibling mechanism, state in one sentence what chousa should absorb next round and why its own version falls short — or state that none exists. Do not absorb anything this round; do not edit any sibling file.
4. Report the sibling revisions you read (`git -C <sibling> rev-parse master`) so the comparison is pinned.

Report at `.ufo/waves/round-80/w1/R80ConnectorA/scan.md` with a command per claim.
"""})

spec = {
    "wave": "chousa-r80-w1",
    "reportDir": ".ufo/waves/round-80/w1",
    "context": CONTEXT,
    "items": items,
}

out = pathlib.Path(f"{LANE}/.ufo/waves/round-80/w1-spec.json")
out.write_text(json.dumps(spec, indent=2) + "\n")
print(f"wrote {out} with {len(items)} items; roles={sorted({i['role'] for i in items})}")
