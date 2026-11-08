#!/usr/bin/env python3
"""Build the round-90 wave-1 spec (13 seats, policy v1 band 8-16). Reads FREEZE and CARRIER from the environment."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
SCRATCH = "/fast/scratch/hyaku/chousa-r90"
BASE = "f54a45ed197dd475af50d82e43a22df3d2e99782"
FREEZE = os.environ["FREEZE"]
CARRIER = os.environ["CARRIER"]

GODSPEED = """/skill:godspeed

You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.
"""

CONTEXT = f"""Lane chousa round 90, L1 ChousaR90 holds the canonical planner seat, the freeze and the integration. Root {LANE}.
Revisions: base {BASE} (round-89 landing + its non-author spot-check); claim freeze {FREEZE}; the tree you attack is
{CARRIER} (the freeze commit plus the committed control receipts; the receipts pin {FREEZE}).
Frozen predicate set: {LANE}/corpus/evidence/round90/claims.md — read it FIRST, with every kill rule and every NAMED
LIMIT — and {LANE}/plans/round-90.md. Machine form: {LANE}/.ufo/waves/round-90/claims.json.
Three claims, three axes, all successors of round-89 bytes; `tools/research-gate.sh` and `tools/gate-records.py` are
UNCHANGED this round.

C1 operability (lowest scored, historical 3/10): `corpus/evidence/round90/control-driver-r90.py verify --root <lane>
--repo <clone at {CARRIER}> --rev {FREEZE} --receipts-rev {CARRIER}` must print `CONTROL_DRIVER_R90=PASS` with
`COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6`; the six committed receipts under
`corpus/evidence/round90/controls/receipts/` are read before any fresh run, their `# exit=`/`# computed_against=`
headers are checked, required values match whole body tokens, the harm row requires `records>=1`, a repeated key
with different values is `DUPLICATE_KEY`, and the fresh re-run agrees. `control-forgeries-r90.py` must print
`FORGERY_REFUSED=6/6 PRIOR_ACCEPTED=6/6 POSITIVE=pass` (six classes refused by r90 and accepted by the unchanged r89
driver).
C2 calibration: `corpus/evidence/round90/curation-r90.py --root .` must print `CURATION_R90=PASS`, `LEGS_MEASURED=10/10`,
an output line containing `VERDICT fields_hold=1`, `DETECTOR_WITNESS=8/8`, and the carried fields
`DUP_QIDS=0 WARRANT_OK=17/17 QUOTES_LOCATED=20/20 TEACHES_FLAGGED=1 TEACHES_UNRESOLVED=0 SUP_CLAUSE_CHECKED=0
SUP_UNRESOLVED=0`; `curation-r90-mutants.py` must print `MUTANTS_KILLED=10/10 COUNTER_DETECTED=9 BATTERY_DETECTED=1
PRIOR_R89_SURVIVORS=2/2`; `curation-r90-controls.py` must print `CONTROLS=PASS FORGERY_REFUSED=7/7
PRIOR_REGRESSION=7/7`.
C3 freshness: `corpus/evidence/round90/skill-tally-r90.py --root .` must print `SKILL_TALLY_R90=PASS` with
`TALLY_ROWS=9 STALE_TALLIES=0/9 EXPECTED_CASES=283 EXPECTED_SKIPPED=0 OTHER_OCCURRENCES=3` at the landing revision; at
{CARRIER} it is expected to print `STALE_TALLIES=9/9` because `SKILL.md` still says 275 (the repair lands after the
wave). Its discrimination leg is a scratch copy with the nine current cells changed to 283.
Ground source: S220 (GNU grep(1) `-x`, committed capture `corpus/captures/e6ec761219e8044b0e9e067a.txt`) grounds C1's
whole-token rule; the registry went 218 -> 219 rows with that one mined row and its `used-by` cell.

Every `Report:` trailer path is relative to {LANE} — write it at {LANE}/<that path>.

Leaf only: no task tool, no subagents, no agent://all, no production edits, no lane or fleet git/jj mutation, no commits
or pushes, no edits to /home/vgpnk/Projects/shokunin/scripts, /home/vgpnk/Projects/shokunin/.ufo/state, MANIFEST.json,
considerthese/ or any sibling repo. The only files you write are under {LANE}/.ufo/waves/round-90/w1/<seat>/ plus your
scratch dir. Network: none this round except C3's own selftest; every other check reads committed bytes (a GET is a
finding). Never mutate a host sysctl, never run sudo, never restart a host service.

Scratch: every tree, work dir and fixture lives under {SCRATCH}/<your seat name>/; create it with `mkdir -p`, pass it
explicitly (`--work`, `TMPDIR=`), delete it before you yield (`trap 'rm -rf -- "$S"' EXIT` in shell, `finally:
shutil.rmtree` in Python), and copy every receipt you cite into your wave output folder first. Never write under /tmp.
Build a tree at a revision with `git -C {LANE} archive <rev> | tar -x -C <scratch dir>`; for the C1 self-pin you need
history, so `git clone --shared {LANE} <scratch>/repo` and `git -C <scratch>/repo checkout {CARRIER}` instead. Any
fixture git repo is `D=$(mktemp -d -p {SCRATCH}/<seat>) && test -n "$D" && git -C "$D" init -q`, every later git call
names `-C "$D"`, and you assert `git -C "$D" rev-parse --show-toplevel` equals `$D` before any mutating git command.

Counter that binds you: every finding names the exact command, the receipt path you wrote and the observed line plus
exit code. An unrun check has not passed; a deviation from an expected value is a finding, never something to hide.
End your report with one line per claim you touched: `VERDICT: <seat> <C1|C2|C3> fired|held|n/a — <one sentence>`
(plain text, not JSON). A seat that ships no `VERDICT:` trailer is tallied as a seat-discipline finding.

Tooling authorization (operator, 2026-10-19): you may install or upgrade tools that help the task; read
/home/vgpnk/.omp/agent/RULES.md first (official channels only; record tool/version/channel/reason in your report).
pacman guard (orchestrator ruling 2026-10-20): all pacman transactions are PAUSED host-wide — install via `uv tool`/
`npx`/an official binary in ~/.local/bin, or not at all; never `pacman -Sy`, `-Syu`, `-U`, `-R`, never downgrade.
"""


def seat(name, role, body):
    return {"name": name, "role": role, "prompt": GODSPEED + "\n" + body.strip() + "\n"}


ITEMS = [
    seat("R90ExecC1Repro", "executor", f"""
Reproduce frozen C1 from a clean tree. `S={SCRATCH}/R90ExecC1Repro`; `git clone --shared {LANE} $S/repo` then
`git -C $S/repo checkout {CARRIER}`. Run, from `$S/repo`:
(a) `python3 -B corpus/evidence/round90/control-driver-r90.py verify --root $S/repo --repo $S/repo --rev {FREEZE}
    --receipts-rev {CARRIER} --work $S/work` — record every `RECEIPT … OK/FINDING` line, the four counts and the exit.
(b) `python3 -B corpus/evidence/round90/control-forgeries-r90.py --root $S/repo --work $S/forge --rev {FREEZE}` —
    record every `OK/CASE_DEVIATION` line, `FORGERY_REFUSED`, `PRIOR_ACCEPTED`, `POSITIVE` and the exit.
(c) Prove the receipt is read before any fresh run: note `receipts/*.txt` mtimes before and after (b)/(a), and show
    `git -C $S/repo status --porcelain` is empty after both. A write under `controls/receipts/` is a finding.
Copy the transcript to your wave folder. Write `R90ExecC1Repro.md` with commands, paths, observed lines and exits."""),

    seat("R90ExecC2Repro", "executor", f"""
Reproduce frozen C2 from a clean tree. `S={SCRATCH}/R90ExecC2Repro`; `git -C {LANE} archive {CARRIER} | tar -x -C $S`.
Run, from `$S`:
(a) `python3 -B corpus/evidence/round90/curation-r90.py --root .` — record the full summary, the `VERDICT …` line,
    `DETECTOR_WITNESS`, and the exit; also `grep -c 'VERDICT fields_hold=1'` over a saved transcript.
(b) `python3 -B corpus/evidence/round90/curation-r90-mutants.py --root . --work $S/mut` — every `KILLED/SURVIVOR` and
    `SURVIVOR_PRIOR` line, the summary and the exit.
(c) `python3 -B corpus/evidence/round90/curation-r90-controls.py --root . --work $S/ctl` — every case line, the
    summary and the exit.
(d) Before-state re-derivation: run the round-89 counter `corpus/evidence/round89/curation-r89.py --root .` and record
    whether a `VERDICT fields_hold=1` token exists on its passing path (`grep -c`), and re-derive that the two
    round-89 substitution edits survive (the mutant battery's `SURVIVOR_PRIOR` lines are the reproduction).
Write `R90ExecC2Repro.md` with commands, observed lines, exits."""),

    seat("R90ExecC3Tally", "executor", f"""
Reproduce frozen C3's before-state and its discrimination leg. `S={SCRATCH}/R90ExecC3Tally`; tree at `{CARRIER}`.
(a) Before: `python3 -B corpus/evidence/round90/skill-tally-r90.py --root .` on the tree (it runs the selftest itself,
    about 95 s) — record `TALLY_ROWS`, `STALE_TALLIES`, `EXPECTED_CASES`, `OTHER_OCCURRENCES`, the exit, and one full
    `STALE_TALLY` line. Expect `STALE_TALLIES=9/9`.
(b) Discrimination: copy the tree to `$S/after`, replace only the nine current `PASS (275 cases, 0 skipped)` cells with
    `PASS (283 cases, 0 skipped)` (the eight Gates-table `research-gate` rows and the `Selftest` host note), and run
    the same command with `--selftest` pointing at the selftest transcript you saved in (a); record
    `STALE_TALLIES=0/9` and the exit. Do not edit the three historical occurrences (round-25/32/34/37 quotes).
(c) Sweep the file for every `PASS (<n> cases` occurrence with line numbers and say which are current and which are
    historical; confirm the current set is exactly 9 and the historical set exactly 3.
Write `R90ExecC3Tally.md` with the counts and the line list."""),

    seat("R90ExecC1Forge", "executor", f"""
Forge frozen C1 from a tree at `{CARRIER}` (`S={SCRATCH}/R90ExecC1Forge`). Find a receipt/expectation state the frozen
predicate ACCEPTS while C1's sentence is false. Attack at least:
(a) the token leg — a required token on a diagnostic line, a token with a different value in a second line, a `line:`
    phrase that appears in a comment or a `#`-header line;
(b) the pin leg — a receipt that pins {FREEZE} while its bytes come from a different tree; a `--rev` passed as the
    wrong commit; the receipts-carrier revision confused with the instrument revision;
(c) the fresh leg — an instrument whose output depends on `--work` content or on time, so the committed receipt and the
    fresh run agree only sometimes;
(d) the harm predicate — a receipt with `records=1` and `moved=0` from an empty after-map; a `records` value glued to
    other text; a duplicate `records=` token.
Every accepted forgery is a finding with the receipt path, the line and the exit. Refuted attempts are recorded too.
Write `R90ExecC1Forge.md` with a `VERDICT:` line."""),

    seat("R90ExecC2Forge", "executor", f"""
Forge frozen C2 from a tree at `{CARRIER}` (`S={SCRATCH}/R90ExecC2Forge`, mirror the tree the way
`curation-r90-controls.py` does). Find a tree or counter state the counter ACCEPTS where C2's sentence is false.
Attack at least:
(a) the witness — a detector function replaced by a constant that still satisfies the two synthetic assertions (e.g.
    a substring-based `locates` that passes both witness strings but fails on a real capture);
(b) the verdict line — `VERDICT fields_hold=1` printed while `fields_hold` is computed from a different variable
    (constant substitution, stale snapshot before the legs run);
(c) the carried legs — a registry/tree edit that keeps `DETECTOR_WITNESS=8/8` while moving a real field;
(d) the control battery's regression frame — a tree forgery both counters accept.
Every accepted forgery is a finding. Write `R90ExecC2Forge.md` with a `VERDICT:` line."""),

    seat("R90ReviewerC1", "reviewer", f"""
Attack C1's stated wording clause by clause against `corpus/evidence/round90/control-driver-r90.py`,
`control-forgeries-r90.py`, `controls/expected.tsv` and the six committed receipts. For each clause of the C1 sentence
say whether the instrument ENFORCES it, merely prints it, or cannot see it — with the line number and one runnable
probe. Specifically: "reads the committed receipt before any fresh run", "writes nothing under the receipts
directory", "whole whitespace-delimited body token", "`TOKEN_DETACHED`", "`DUPLICATE_KEY`", "`records>=1`",
"byte-identical to their blobs at the named carrier revisions", "the instrument re-run … agrees". Also test the claim
that the six forgery classes are refused by r90 and accepted by r89 (read the battery, then run one case by hand).
Write `R90ReviewerC1.md` with a clause table and a `VERDICT:` line."""),

    seat("R90ReviewerC2", "reviewer", f"""
Attack C2's wording against `corpus/evidence/round90/curation-r90.py`, its controls and mutants. For each clause:
"prints an output line containing `VERDICT fields_hold=1`", "the verdict leg is appended before the summary and is one
of the ten legs `passed` requires", "`DETECTOR_WITNESS=8/8`", "each detector … fires and stays silent", "the two substitutions
survive r89 and die on `LEG_FAIL WITNESS`". Run the mutants and controls yourself and quote the lines. Report any
clause that the instrument does not enforce as `falsifies-wording` with the receipt path.
Write `R90ReviewerC2.md` with a `VERDICT:` line."""),

    seat("R90CriticClaims", "critic", f"""
Falsify all three claims the way round 89's critic did. For each claim build the cheapest artifact that skips the
claimed work and score it with the frozen counter:
(a) C1 — a driver that only re-runs instruments and never reads the committed receipt; a receipt set with the pin
    minted in `verify`; a token check that is substring again. Show which counter fields catch each.
(b) C2 — a counter whose `VERDICT` line is a constant print, a counter whose witness is not called by the detectors, a
    controls frame that passes with the seven forgeries accepted.
(c) C3 — a SKILL.md where the nine current cells say 283 but a tenth current row is stale; a check that binds only the
    file's text, not the tool's verdict.
Also run the do-nothing control: for each claim, what does the round leave unchanged if the instrument is not landed?
Write `R90CriticClaims.md` with one row per (claim, control), the observed line and a `VERDICT:` line."""),

    seat("R90MutBattery", "mutation-tester", f"""
Mutation-probe the round-90 instruments (`S={SCRATCH}/R90MutBattery`, tree at `{CARRIER}`). Detector = each
instrument's own frozen predicate.
(a) At least EIGHT one-point mutations of `control-driver-r90.py`: force the token check to a substring; skip the
    committed read; drop the pin check; drop the `records>=1` predicate; make `DUPLICATE_KEY` unreachable; make the
    fresh leg compare nothing; make `self_pin` return no drift; make `check_body` return ok for an empty body. Record
    which die and which survive, with the mutant file and the run line.
(b) At least FOUR mutations of `curation-r90.py` beyond M6–M9 in the committed battery (e.g. witness returns [] or
    all-true; verdict printed from a pre-leg snapshot; `fields_hold` ignoring `witness_bad`). Record survivors.
(c) Two mutations of `skill-tally-r90.py` (current-line rule widened to every occurrence; expected count read from the
    file instead of the tool). Record survivors; a survivor is a finding.
Write `R90MutBattery.md` with a mutant table and a `VERDICT:` line."""),

    seat("R90SentinelScope", "sentinel", f"""
Adversarial scope, control-discipline and safety review of the round's own artifacts; read-only outside your output
folder.
(a) Control discipline: for each of the six committed receipts under `corpus/evidence/round90/controls/receipts/`,
    verify the `# computed_against=` pin equals `{FREEZE}`, the `# exit=` equals the expected row, and the receipt is
    byte-identical to the blob at `{CARRIER}` (`git -C {LANE} show {CARRIER}:<path>`). Report any mismatch.
(b) Egress: list every refetch row added this round (`corpus/evidence/round57/refetch.tsv` rows whose `fetched_utc`
    starts with 2026-11-08T09:4 or 09:5), the id under which each landed, and say whether a registry row exists for
    it. The S219 failed attempt and the S220 success must be named; confirm no other fetch.
(c) Scope: `git -C {LANE} diff {BASE} {CARRIER} --stat` — does any path fall outside the lane or outside this round's
    declared surface? Check `SKILL.md` is unchanged at {CARRIER} (C3 lands after the wave).
(d) Attribution: the freeze commits' author and committer must be `chousa-shokunin <chousa@shokunin.local>`.
(e) Credential shape: no secret values in any new file (grep for `op://`, `ghp_`, `sk-`, `Bearer `).
Write `R90SentinelScope.md` with one finding per item and a `VERDICT:` line."""),

    seat("R90ScoutRegistry", "scout", f"""
Registry reconnaissance, read-only, at `{CARRIER}`.
(a) S220: read the row, then re-open its capture `corpus/captures/e6ec761219e8044b0e9e067a.txt` and confirm the quote
    `Select only those matches that exactly match the whole line.` is present after whitespace normalisation, that it is
    11 words, that the capture sha256 matches the row's refetch line, and that the refetch row's `http_code` is 200,
    `curl_rc` 0 and its `fetched_utc` is the access instant. Report the located capture line numbers.
(b) The id: why the row is S220 and not S219. Re-derive the collision by adding a real `S219` row to a scratch copy of
    the registry and running `corpus/evidence/round89/curation-r89-controls.py --root <copy> --work <scratch>`; record
    the case that stops being accepted by the prior counter, then revert the copy. This is the round's disclosed id
    reservation.
(c) C3 independent count: `grep -c` the `PASS (275 cases` and `PASS (283 cases` strings in SKILL.md and the historical
    occurrences; say how many are current (Gates-table rows naming `research-gate`, plus the host-note `Selftest`
    line) and how many are historical, without trusting the tool's own rule.
(d) Census: `sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` at `{CARRIER}` — record the exit
    and the row count (expect 219).
Write `R90ScoutRegistry.md` with counts, commands and the row list."""),

    seat("R90ConnectorSiblings", "connector", f"""
Sibling-overlap scan (read-only; absorb nothing, report it). Root `/home/vgpnk/Projects/shokunin`.
(a) Does any sibling lane already own receipt/commit-then-verify drivers, whole-token field binding, revision-pinned
    receipts, duplicate-key refusal, detector witnesses, or self-test tally freshness? Search
    `*/corpus/knowledge/*.md`, `*/corpus/lessons/*.md` and `*/tools/*.py` for the class names (`computed_against`,
    `DUPLICATE_KEY`, `whole token`, `witness`, `STALE_TALL`, `tally`), and report each hit with lane, path and line.
(b) Is this round's work inside `{LANE}/PROVINCE.md` ("this lane's own corpus and gates")? Say so or name the drift.
(c) Name any contested scope the integrator should arbitrate.
Write `R90ConnectorSiblings.md`."""),

    seat("R90ScribeLesson", "scribe", f"""
Draft the round-90 lesson from the committed receipts — you draft, the L1 integrates. Read
`corpus/evidence/round90/claims.md`, `plans/round-90.md`, the receipts under `corpus/evidence/round90/controls/` and
round 89's lesson for the shape.
Write `lesson-settlement-draft.md` in your folder with:
(a) `## Gate` — the GATE-RECORD line for S220 in the `url/admit` form (`url=`, `fetched=`, `tier=A`,
    `decision=admit`, `capture=corpus/captures/e6ec761219e8044b0e9e067a.txt`, `capture_sha256=`,
    `words=11`, `quote="Select only those matches that exactly match the whole line."`), using the exact refetch row
    values; plus the S219 reservation note.
(b) `## Claim outcomes` — one block per claim with the fields the receipts print.
(c) `## Mistakes` — at least three rows in the class/evidence-pointer/captured-by/fix shape for this round's own
    errors: the S219/S220 id collision discovered before the row was written; the tally rule that bound historical
    occurrences; one more you can ground in the round's files. Each fix must be shown able to fail.
(d) `## Spot-check intake` — one row per routed defect 1–7 of `corpus/lessons/round-89-verifier-spotcheck.md`.
(e) `## Trends` — three rows (expansion, quality, discernment) with evidence pointers you personally verified.
Cite only paths and commands you read or ran. Write `lesson-settlement-draft.md`.""")
]

if __name__ == "__main__":
    spec = {"wave": "chousa-r90-w1", "reportDir": ".ufo/waves/round-90/w1", "context": CONTEXT, "items": ITEMS}
    out = os.path.join(HERE, "w1-spec.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(spec, fh, indent=1)
    print(f"wrote {out} items={len(ITEMS)} roles={sorted({i['role'] for i in ITEMS})}")
