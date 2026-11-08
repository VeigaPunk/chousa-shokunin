#!/usr/bin/env python3
"""Build the round-94 wave-1 spec (12 seats, policy v1 band 8-16). Constants are the measured revisions."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
SCRATCH = "/fast/scratch/hyaku/chousa-r94"
BASE = "0f3f84dab3a094ec0a2fe8ae9ae59d3326e1a9b6"
FREEZE = "41038ed7c40cffc4cf86d649a6ba433c4b9eec1a"
CARRIER = "352924bbea624caf3771ef291be98fd4ec679dda"

GODSPEED = """/skill:godspeed

You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.
"""

CONTEXT = f"""Lane chousa round 94, L1 ChousaR94 holds the canonical planner seat, the freeze and the integration. Root {LANE}.
Revisions: base {BASE} (round-93 landing + its non-author spot-check, admitted); claim freeze F {FREEZE}; the tree
you attack is carrier C {CARRIER} (F plus the six control receipts emitted against F and the 34-row pins table).
Frozen predicate set: {LANE}/.ufo/waves/round-94/claims.md — read it FIRST, with every kill rule and every NAMED
LIMIT. Machine form: {LANE}/.ufo/waves/round-94/claims.json. Plan and pre-freeze measurements:
{LANE}/plans/round-94.md.
Three claims, three axes:
C1 operability (lowest scored, historical 3/10): `python3 -B corpus/evidence/round94/control-driver-r94.py verify
--root . --repo . --rev {FREEZE} --receipts-rev {CARRIER} --work <scratch>` prints `CONTROL_DRIVER_R94=PASS` with
`COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 PINNED_FILES=34/34 RECEIPT_PINS=6/6 PIN_ROLES_OK=14/14`;
the pins table carries a role column (`instrument|expectation|receipt|claims|driver`) checked in both directions;
`forgeries-r94.py --root . --repo . --rev {FREEZE} --receipts-rev {CARRIER} --work <scratch>` prints
`FORGERY_REFUSED=4/4 PRIOR_ACCEPTED=4/4 SCHEMA_REFUSED=1/1 SCHEMA_PRIOR_ACCEPTED=1/1 CARRIED_REFUSED=2/2
POSITIVE=pass`. Source S070 (installed sha256sum(1)) and S221 (installed git-clone(1): a --shared clone starts out
without any object of its own) ground it.
C2 calibration: `python3 -B corpus/evidence/round94/curation-r94.py --root .` prints `CURATION_R94=PASS` with
`LEGS_MEASURED=16/16 Q_SHAPE_FAIL=0 Q_WSQUOT=0 Q_PUNCTQUOT=0 Q_ROWS=20 WARRANT_OK=17/17 TFREQ_OK=17/17 DUP_QIDS=0`
and `curation-controls-r94.py --root . --work <scratch>` prints `CONTROLS=PASS CARRIED_REFUSED_BOTH=4/4
WS_NAMED=2/2 PUNCT_NAMED=2/2 PUNCT_SHAPE_GREEN_R93=1/1 PRIOR_REGRESSION=7/7`. CLASSIFICATION claim: r93 fails both
punctuation trees downstream with `Q_SHAPE_FAIL=0` and cannot name the class.
C3 freshness: `python3 -B corpus/evidence/round94/skill-tally-r94.py --root . --selftest
corpus/evidence/round94/controls/selftest-r94.txt` prints `SKILL_TALLY_R94=PASS` with `LEGS=4/4 TAIL_OK=1
TAIL_OWNED_OK=2/2 HIST_DERIVED=2/2 HIST_PRESENT=2/2 STALE_TALLIES=0/8 CASE_RANGE_OK=2/2 MISLABELED=0`;
`skill-tally-r94-controls.py --root . --work <scratch>` prints `CONTROLS=PASS CARRIED_REFUSED=6/6
MOVED_REFUSED=2/2 MOVED_PRIOR_ACCEPTED=2/2 DOUBLE_REFUSED=1/1 HEADING_ALIAS_ACCEPTED=1/1`. The tail set is bound
to the heading that owns each tally.
`tools/research-gate.sh` and `tools/gate-records.py` are UNCHANGED this round; SKILL.md is unchanged.

Every `Report:` trailer path is relative to {LANE} — write it at {LANE}/<that path>. Copy every receipt you cite
into your wave output folder before you yield.
Leaf only: no task tool, no subagents, no agent://all, no production edits, no lane or fleet git/jj mutation, no
commits or pushes, no edits to /home/vgpnk/Projects/shokunin/scripts, /home/vgpnk/Projects/shokunin/.ufo/state,
MANIFEST.json, considerthese/ or any sibling repo. The only files you write are under
{LANE}/.ufo/waves/round-94/w1/ plus your scratch dir. Network: none this round; every check reads committed bytes.
Never mutate a host sysctl, never run sudo, never restart a host service.
Scratch: every tree, work dir and fixture lives under {SCRATCH}/<your seat name>/; create it with `mkdir -p`,
pass it explicitly (`--work`, `TMPDIR=`), delete it before you yield (`trap 'rm -rf -- "$S"' EXIT` in shell,
`finally: shutil.rmtree` in Python). Never write under /tmp. For pin/self-pin checks you need history, so
`git clone --shared {LANE} <scratch>/repo` and `git -C <scratch>/repo checkout {CARRIER}` (S221: a shared clone
has no objects of its own, so never repack it). Any fixture git repo is `D=$(mktemp -d -p {SCRATCH}/<seat>) &&
test -n "$D" && git -C "$D" init -q`, every later git call names `-C "$D"`, and you assert
`git -C "$D" rev-parse --show-toplevel` equals `$D` before any mutating git command.
Counter that binds you: every finding names the exact command, the receipt path you wrote and the observed line
plus exit code. An unrun check has not passed; a deviation from an expected value is a finding, never something
to hide.
End your report with one line per claim you touched: `VERDICT: <seat> <C1|C2|C3> fired|held|n/a — <one sentence>`
(plain text, not JSON). A seat that ships no `VERDICT:` trailer is tallied as a seat-discipline finding.

Tooling authorization (operator, 2026-10-19): you may install or upgrade tools that help the task; read
/home/vgpnk/.omp/agent/RULES.md first (official channels only; record tool/version/channel/reason in your report).
pacman guard (orchestrator ruling 2026-10-20): all pacman transactions are PAUSED host-wide — install via `uv tool`/
`npx`/an official binary in ~/.local/bin, or not at all; never `pacman -Sy`, `-Syu`, `-U`, `-R`, never downgrade.
"""


def item(name, role, task):
    return {"name": name, "role": role, "prompt": GODSPEED + task}


ITEMS = [
    item("R94ExecC1Repro", "executor", f"""Reproduce frozen C1 from a clean tree. `S={SCRATCH}/R94ExecC1Repro`; `git clone --shared {LANE} $S/repo`
then `git -C $S/repo checkout {CARRIER}`. Run, from `$S/repo`:
(a) `python3 -B corpus/evidence/round94/control-driver-r94.py verify --root . --repo . --rev {FREEZE} --receipts-rev {CARRIER} --work $S/verify`
→ record full stdout, the `CONTROL_DRIVER_R94=` line and the exit code; expected `COMMITTED_OK=6/6 EXACT_OK=6/6
PIN_OK=6/6 FRESH_OK=6/6 PINNED_FILES=34/34 RECEIPT_PINS=6/6 PIN_ROLES_OK=14/14` and `RECEIPT SELF_PIN OK
rev={FREEZE} receipts_rev={CARRIER}`.
(b) `python3 -B corpus/evidence/round94/forgeries-r94.py --root . --repo . --rev {FREEZE} --receipts-rev {CARRIER} --work $S/forge`
→ expected `FORGERY_REFUSED=4/4 PRIOR_ACCEPTED=4/4 SCHEMA_REFUSED=1/1 SCHEMA_PRIOR_ACCEPTED=1/1
CARRIED_REFUSED=2/2 POSITIVE=pass`; record each of the seven case lines.
(c) independently measure the role relation by hand: parse `corpus/evidence/round94/instrument-pins.txt` and
`corpus/evidence/round94/controls/expected.tsv` with your own script (not the driver's functions) and report the
four sets (instrument/expectation/receipt/claims) with their member counts and whether each equals its
counterpart set. Then delete one claims row from a scratch copy of the table, re-digest the self row the way the
driver does, and show `PIN_ROLE_MISSING role=claims` + exit 1.
(d) prove `verify` writes nothing: `sha256sum corpus/evidence/round94/controls/receipts/*.txt
corpus/evidence/round94/instrument-pins.txt` before and after (a).
Copy each receipt into your report folder. VERDICT trailer required."""),

    item("R94ExecC2Repro", "executor", f"""Reproduce frozen C2 from a clean tree. `S={SCRATCH}/R94ExecC2Repro`; clone at `{CARRIER}`.
Run, from `$S/repo`:
(a) `python3 -B corpus/evidence/round94/curation-r94.py --root .` → record stdout + exit; expected `CURATION_R94=PASS`
with `LEGS_MEASURED=16/16 Q_ROWS=20 Q_SHAPE_FAIL=0 Q_WSQUOT=0 Q_PUNCTQUOT=0 WARRANT_OK=17/17 TFREQ_OK=17/17
DUP_QIDS=0 DETECTOR_WITNESS=17/17`.
(b) `python3 -B corpus/evidence/round94/curation-controls-r94.py --root . --work $S/ctl` → expected `CONTROLS=PASS
CARRIED_REFUSED_BOTH=4/4 WS_NAMED=2/2 PUNCT_NAMED=2/2 PUNCT_SHAPE_GREEN_R93=1/1 DUPCOUNT_1=1/1
PRIOR_REGRESSION=7/7`.
(c) independently measure the punctuation class: build YOUR OWN tree (copy the two routed entries plus
`corpus/SOURCES.md`, symlink `corpus/captures`, copy both leg tables) and replace the Q2 quote cell in
`search-transparency-reporting-r84.md` with `"—"`; then run the r93 counter and the r94 counter on it. Report
r93's `Q_SHAPE_FAIL=`/`LEG_FAIL` lines and r94's `Q_SHAPE_FAIL=`, `Q_PUNCTQUOT=`, the named `quote=<punctuation>`
shape line and `LEG_FAIL` lines. Then put the SAME punctuation cell in a row citing a source whose capture DOES
contain an em dash (find one) and say whether either counter now accepts the row as located.
(d) test the named limit: does a quote of only digits (`"2026"`) pass r94's shape leg? Report the verdict.
Copy receipts into your report folder. VERDICT trailer required."""),

    item("R94ExecC3Repro", "executor", f"""Reproduce frozen C3 from a clean tree. `S={SCRATCH}/R94ExecC3Repro`; clone at `{CARRIER}`.
Run, from `$S/repo`:
(a) `python3 -B corpus/evidence/round94/skill-tally-r94.py --root . --selftest corpus/evidence/round94/controls/selftest-r94.txt`
→ expected `SKILL_TALLY_R94=PASS` with `TALLY_ROWS=8 STALE_TALLIES=0/8 CASE_RANGE_OK=2/2 MISLABELED=0
HIST_DERIVED=2/2 HIST_PRESENT=2/2 TAIL_TALLIES=2 TAIL_OWNED_OK=2/2 OTHERS_OK=1 TAIL_OK=1 LEGS=4/4`.
(b) `python3 -B corpus/evidence/round94/skill-tally-r94-controls.py --root . --work $S/ctl` → expected `CONTROLS=PASS
CARRIED_REFUSED=6/6 MOVED_REFUSED=2/2 MOVED_PRIOR_ACCEPTED=2/2 DOUBLE_REFUSED=1/1 HEADING_ALIAS_ACCEPTED=1/1`.
(c) independently measure the owner binding: copy `SKILL.md` plus the two grounding receipts into scratch and
move BOTH tail tallies into ONE other section (so the multiset is unchanged) — report r93's and r94's verdicts and
the exact `TAIL_OWNER_*` lines. Then move a tail tally under a heading that only *contains* the declared owner
string and report whether r94 accepts it (named limit 1).
(d) state the exact heading each declared tally sits under, with line numbers, from `SKILL.md` alone.
Copy receipts into your report folder. VERDICT trailer required."""),

    item("R94ExecMutations", "mutation-tester", f"""Mutation battery on the three r94 instruments. `S={SCRATCH}/R94ExecMutations`; `git clone --shared {LANE} $S/repo`;
checkout `{CARRIER}`. Mutate COPIES under `$S` only; never edit the lane.
For each mutant, copy the instrument into `$S/mut/<id>/`, apply one textual change, run the matching counter on
`$S/repo` (with `--selftest` for C3; `--root . --repo . --rev {FREEZE} --receipts-rev {CARRIER}` for C1;
`--root .` for C2), and record the verdict line + exit code.
C1 mutants: M1 `role_report`'s instrument comparison becomes one-directional (dangling rows invisible);
M2 `CLAIM_PATHS` shrinks to one path; M3 `PIN_ROLE_UNKNOWN` becomes a warning instead of a setup exit;
M4 `PIN_ROLES_OK` counts `driver` rows as covered (so a deleted driver row looks fine).
C2 mutants: M5 `punct_quote_cell` returns False for three-cell rows (leg dead); M6 the PUNCTQUOT leg is deleted
while `EXPECTED_LEGS` stays 16; M7 `locates()` drops the punctuation guard; M8 `q_shape_violation` keeps the
punctuation test but `fields_hold` drops `not punct_quote_rows`.
C3 mutants: M9 `TAIL_OWNED` owners are read but the comparison is `owner in h or True`; M10 `TAIL_OWNED_OK` is
computed as `len(TAIL_OWNED)` (constant); M11 the nearest-heading tracker never updates (all tallies owned by
`<none>`).
Control: M12 a mutant that only renames a local variable must SURVIVE — reported as a survivor, proving the
battery is not a blanket refusal. Report `MUTANTS_KILLED=n/12 SURVIVORS=m/12` with the exact command, observed
verdict and exit per mutant. VERDICT trailer required."""),

    item("R94RevPrior", "revenger", f"""Independently reproduce the BEFORE states the three claims rest on, from committed bytes only.
`S={SCRATCH}/R94RevPrior`; `git clone --shared {LANE} $S/repo` and `git -C $S/repo checkout {CARRIER}`.
(a) C1 before: the r93 driver has no role notion. Show it (i) scores the landed r93-style table
`PINNED_FILES=34/34`-equivalent without ever reading a role, (ii) scores a table whose two claims rows are
deleted (`corpus/evidence/round94/evidence-before/c1-prior-accepts.txt` shows 21/21 PASS at the r93 freeze),
(iii) refuses a three-column row with `SETUP malformed pin row`. Say precisely which of these is a defect the
r94 claim covers and which is a schema difference.
(b) C2 before: on your own punctuation tree, show r93's `Q_SHAPE_FAIL=0`, the downstream legs that fired, and that
r93's `locates()` has no punctuation guard (`grep -n "def locates" -A3`).
(c) C3 before: show r93's `TAIL_DECLARED` literal and that a moved tally leaves `TAIL_OK=1`.
(d) Compare against `corpus/evidence/round94/evidence-before/*.txt` and report any disagreement with the exact
line. VERDICT trailer required."""),

    item("R94ReviewerC1", "reviewer", f"""Attack C1's frozen sentence against the committed code and receipts. `S={SCRATCH}/R94ReviewerC1`;
clone at `{CARRIER}`, read `corpus/evidence/round94/control-driver-r94.py`, `forgeries-r94.py`,
`make-pins-r94.py`, the pins table and claims C1.
Findings must be concrete: (1) Does `role_report` really compare the *executed* set, or a set derived from the
table itself? (2) Can a row be both `driver` and cover a real role gap (i.e. is `driver` a loophole for a
deleted instrument)? (3) Is `PIN_ROLES_OK` load-bearing (make it 13/14 on a scratch copy and show the verdict
changes)? (4) Does `make-pins-r94.py` reproduce the committed table byte-for-byte (`diff`), and does the self
row really bind the non-self rows? (5) Does the forgeries battery's `PRIOR_ACCEPTED` measure the *projection*
honestly, or does the projection differ from the fixture in a way that matters? (6) Is the claim's
"both directions" sentence true for all four covered roles, including `claims` (which is a fixed pair of paths,
not a derived set)? Quote the sentence and the line.
For each: name the line, the command, the observed output and FIRES or HOLDS. Do not edit the lane. VERDICT
trailer required."""),

    item("R94ReviewerC2", "reviewer", f"""Attack C2's frozen sentence against the committed code and receipts. `S={SCRATCH}/R94ReviewerC2`;
clone at `{CARRIER}`, read `curation-r94.py`, `curation-controls-r94.py`, the 16-name leg table and claims C2.
Findings must be concrete: (1) Is `Q_PUNCTQUOT` counting the intended population, and can it fire on a CLEAN
entry (a quote that is legitimately punctuation-heavy, e.g. `“—”` inside a longer quote)? (2) Does the class test
over-refuse a real quote that is a single symbol (e.g. a quote of `§` or `→` from a manual)? Name the class it
refuses and whether that is a harm. (3) Does `locates()`'s new guard change any existing verdict on the two routed
entries? (4) Is `EXPECTED_LEGS=16` load-bearing (delete the leg from a copy, show the verdict changes)? (5) Is
`PUNCT_SHAPE_GREEN_R93` a real re-derivation every run? (6) Does the claim's "classification, not refusal" framing
stay honest — quote the sentence.
For each: name the line, the command, the observed output and FIRES or HOLDS. Do not edit the lane. VERDICT
trailer required."""),

    item("R94ReviewerC3", "reviewer", f"""Attack C3's frozen sentence against the committed code and receipts. `S={SCRATCH}/R94ReviewerC3`;
clone at `{CARRIER}`, read `skill-tally-r94.py`, `skill-tally-r94-controls.py`, `SKILL.md` (Gates scope and the
two tail tallies) and claims C3.
Findings must be concrete: (1) Is the nearest-preceding-heading tracker correct at the scope boundary (the first
tail line after `## Gates`)? (2) Can a tally moved *inside* the Gates scope hide from the owner leg (it would be
caught by `others_ok` — verify)? (3) Is `TAIL_OWNED_OK` load-bearing (stub it to 2/2 on a copy and show the
verdict changes)? (4) Does `TAIL_OWNER_COUNT` fire for a duplicated tally and for a deleted one? (5) Does the
`moved-to-heading` control really prove the substring limit, or does it pass for another reason? (6) Is any
historical tally's owner claim wrong today (check the actual heading above each of the two)?
For each: name the line, the command, the observed output and FIRES or HOLDS. Do not edit the lane. VERDICT
trailer required."""),

    item("R94CriticClaims", "critic", f"""Wording attack: compare each frozen claim sentence with what the instruments enforce. `S={SCRATCH}/R94CriticClaims`;
clone at `{CARRIER}`; read `.ufo/waves/round-94/claims.md` (all three) and the three counters plus batteries.
For each claim, list every noun/quantifier the sentence asserts and the line of code that enforces it, or say
`unbound`. Specifically test: C1's "both directions" for `claims` and `expectation` (are they derived sets or
fixed paths?); C1's "a deleted or invented row moves the number rather than hiding"; C2's "r93 cannot name the
class" (is there ANY r93 output token that names punctuation?); C3's "TAIL_OK now requires both the multiset and
the owners" (is there a path where the multiset passes and owners fail without moving TAIL_OK?). Report
`WORDING_FIRES=n` with one line per unbound assertion and the exact sentence. Do not edit the lane. VERDICT
trailer required."""),

    item("R94SentinelScope", "sentinel", f"""Scope and safety review of the round's instruments. `S={SCRATCH}/R94SentinelScope`; clone at `{CARRIER}`.
Check, each with a command and an observed output: (1) Does any r94 instrument write outside `--work` (grep every
`open(..., "w")`, `makedirs`, `shutil` call; run each battery with `--work` on a read-only-mounted copy and report
the failure mode)? (2) Can `--root`/`--rev`/`--pins` be pointed at a path outside the tree and make the driver
read or write outside it (traversal, symlink, absolute path)? (3) Do the batteries clone with `--shared` and is
any tree left behind after a normal exit (measure `du -sh` before/after, and list what a failing exit leaves)?
(4) Does any instrument execute a network command or read `$HOME`? (5) Does `make-pins-r94.py` ever read a file it
does not pin, or pin a file it does not read? (6) Does the pins table or any receipt contain a credential shape or
an absolute host path that is not reproducible? Report `SCOPE_FINDINGS=n`. Do not edit the lane. VERDICT trailer
required."""),

    item("R94ConnectorSiblings", "connector", f"""Cross-lane pattern scan, read-only. `S={SCRATCH}/R94ConnectorSiblings`. Read
`/home/vgpnk/Projects/shokunin/*-shokunin/corpus/evidence/round*/` pin tables and drivers (and each lane's
`SCORECARD.md` recent blocks) and answer: (1) does any sibling lane already carry a role-bearing pin table
(`grep -rl "instrument|expectation" --include='*pins*.txt' /home/vgpnk/Projects/shokunin/*-shokunin/`), or a
punctuation-only quote class, or a heading-bound tally check? (2) For each pattern this round claims as new, name
the closest sibling mechanism with its path and say whether it is the same mechanism (then this round's novelty is
a defect) or a different one. (3) Report any cross-domain evidence this lane should route but not absorb.
Everything read-only; no writes to sibling repos. Report `OVERLAPS=n` with one line per pattern. VERDICT trailer
required."""),

    item("R94ScoutSources", "scout", f"""Source opening and a bounded planning data-walk. `S={SCRATCH}/R94ScoutSources`; clone at `{CARRIER}`.
(a) Open the two sources C1 cites and report, for each, the file/URL, the exact located quote and its line:
(i) `/usr/share/man/man1/sha256sum.1.gz` (S070) — print line 11 decompressed; (ii) `/usr/share/man/man1/git-clone.1.gz`
(S221) — print the `-s, --shared` body sentence "The resulting repository starts out without any object of its
own." with its decompressed line number and the page's sha256. Say whether each quote grounds the claim sentence
it is cited for.
(b) Data-walk for the planner seat (the L1 holds it; you supply the data): list every file the pins table pins,
grouped by role, with size and sha256; then state which pinned files are NOT read by any instrument at run time
(candidates for a role that does not exist yet). Give the exact command.
(c) Check the three r94 instruments for an unused import or a dead branch (`python3 -m pyflakes` if available, else
`python3 -m py_compile` plus a manual `grep`); report anything found with the line.
Copy receipts into your report folder. VERDICT trailer required."""),
]

SPEC = {
    "wave": "chousa-r94-w1",
    "reportDir": ".ufo/waves/round-94/w1",
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
