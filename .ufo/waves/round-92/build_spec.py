#!/usr/bin/env python3
"""Build the round-92 wave-1 spec (12 seats, policy v1 band 8-16). Constants are the measured revisions."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
SCRATCH = "/fast/scratch/hyaku/chousa-r92"
BASE = "d7780feff6e39ae74a2fd77fc9773c671b33da95"
FREEZE = "42e0337822a508208800f98faa3a63c6af9f8c27"
CARRIER = "16ccf7693c61b8ffe392fc757352304f239bfcad"
SUPERSEDED = "bf12c30e / ddb5fdf4, 85a2eeef / 9722365f, dc7056c4 / e40bce1a, 007d7ea7 / (007d7ea7-emitted, never carried)"

GODSPEED = """/skill:godspeed

You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.
"""

CONTEXT = f"""Lane chousa round 92, L1 ChousaR92 holds the canonical planner seat, the freeze and the integration. Root {LANE}.
Revisions: base {BASE} (round-91 landing + its non-author spot-check, admitted); claim freeze F5 {FREEZE}; the
tree you attack is carrier C5 {CARRIER} (the freeze plus the six committed control receipts; the receipts pin
{FREEZE}). Four earlier freeze/carrier pairs ({SUPERSEDED}) were superseded before any scored run and before
this wave — their defects are recorded in {LANE}/plans/round-92.md §§Pre-wave freeze repair 1-2; treat F5/C5 as
the freeze. The pins table has 16 rows (no plan row: plan prose is narrative, not scored bytes).
Frozen predicate set: {LANE}/corpus/evidence/round92/claims.md — read it FIRST, with every kill rule and every
NAMED LIMIT — and {LANE}/plans/round-92.md. Machine form: {LANE}/.ufo/waves/round-92/claims.json.
Three claims, three axes:
C1 operability (lowest scored, historical 3/10): `python3 -B corpus/evidence/round92/control-driver-r92.py verify
--root . --repo . --rev {FREEZE} --receipts-rev {CARRIER} --work <scratch>` prints
`CONTROL_DRIVER_R92=PASS` with `COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6`, and
`control-forgeries-r92.py --work <scratch>` prints `FORGERY_REFUSED=3/3 POSITIVE=pass`. Source S070 (installed
sha256sum(1), re-opened this round, quote "Print or check SHA256 (256-bit) checksums.") grounds the digest-pin
rule including the S5 self-pin (minus-self digest).
C2 calibration: `python3 -B corpus/evidence/round92/curation-r92.py --root .` prints `CURATION_R92=PASS` with
`LEGS_MEASURED=14/14 Q_ROWS=20 Q_SHAPE_FAIL=0 SOURCE_STATUS_OK=20/20 USED_BY_OK=20/20 TFREQ_OK=17/17 TFREQ_MAX_DF=3
UNENTAILED_TERM=0 WARRANT_OK=17/17 DUP_QIDS=0`, and `curation-r92-controls.py --root . --work <scratch>` prints
`CONTROLS=PASS FORGERY_REFUSED=4/4 PRIOR_ACCEPTED=4/4 DUPCOUNT_R91=1 DUPCOUNT_R92=1 PRIOR_REGRESSION=7/7`.
C3 freshness: `python3 -B corpus/evidence/round92/skill-tally-r92.py --root . --selftest
corpus/evidence/round92/controls/selftest-r92.txt` prints `SKILL_TALLY_R92=PASS` with `TALLY_ROWS=8
STALE_TALLIES=0/8 EXPECTED_CASES=283 EXPECTED_SKIPPED=0 OTHER_OCCURRENCES=2 CASE_RANGE_BASHENV=273-275
CASE_RANGE_BASH_PIN=282-283 CASE_RANGE_OK=2/2 MISLABELED=0 OTHERS_OK=1 LEGS=3/3`; `skill-tally-r92-controls.py
--root . --work <scratch>` prints `CONTROLS=PASS OLDPROSE_REFUSED=1/1 PRIOR_ACCEPTED=1/1 STALE_REFUSED_BOTH=1/1`.
The C3 repair (scope to `## Gates`, pinned others multiset) is IN the frozen instruments at C5, against the
committed `SKILL.md` (no SKILL.md change this round). `tools/research-gate.sh` and `tools/gate-records.py` are
UNCHANGED this round.

Every `Report:` trailer path is relative to {LANE} — write it at {LANE}/<that path>. Copy every receipt you cite
into your wave output folder before you yield.
Leaf only: no task tool, no subagents, no agent://all, no production edits, no lane or fleet git/jj mutation, no
commits or pushes, no edits to /home/vgpnk/Projects/shokunin/scripts, /home/vgpnk/Projects/shokunin/.ufo/state,
MANIFEST.json, considerthese/ or any sibling repo. The only files you write are under
{LANE}/.ufo/waves/round-92/w1/ plus your scratch dir. Network: none this round except a re-open an item names;
every other check reads committed bytes (an unrequested GET is a finding). Never mutate a host sysctl, never run
sudo, never restart a host service.
Scratch: every tree, work dir and fixture lives under {SCRATCH}/<your seat name>/; create it with `mkdir -p`,
pass it explicitly (`--work`, `TMPDIR=`), delete it before you yield (`trap 'rm -rf -- "$S"' EXIT` in shell,
`finally: shutil.rmtree` in Python). Never write under /tmp. Build a tree at a revision with
`git -C {LANE} archive <rev> | tar -x -C <scratch dir>`; for pin/self-pin checks you need history, so
`git clone --shared {LANE} <scratch>/repo` and `git -C <scratch>/repo checkout {CARRIER}` instead. Any fixture
git repo is `D=$(mktemp -d -p {SCRATCH}/<seat>) && test -n "$D" && git -C "$D" init -q`, every later git call
names `-C "$D"`, and you assert `git -C "$D" rev-parse --show-toplevel` equals `$D` before any mutating git
command.
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
    item("R92ExecC1Repro", "executor", f"""Reproduce frozen C1 from a clean tree. `S={SCRATCH}/R92ExecC1Repro`; `git clone --shared {LANE} $S/repo`
then `git -C $S/repo checkout {CARRIER}`. Run, from `$S/repo`:
(a) `python3 -B corpus/evidence/round92/control-driver-r92.py verify --root . --repo . --rev {FREEZE} --receipts-rev {CARRIER} --work $S/verify`
→ record the full stdout, the `CONTROL_DRIVER_R92=` line and the exit code; expected `COMMITTED_OK=6/6 EXACT_OK=6/6
PIN_OK=6/6 FRESH_OK=6/6` and `RECEIPT SELF_PIN OK rev={FREEZE} receipts_rev={CARRIER}`.
(b) `python3 -B corpus/evidence/round92/control-forgeries-r92.py --work $S/forge` → expected
`FORGERY_REFUSED=3/3 POSITIVE=pass`.
(c) the repairs the frozen text claims: (i) run `verify` with `--work` omitted and `TMPDIR=$S/td` → the work dir
is created under TMPDIR and the verdict is still PASS; (ii) `emit` without `--receipts` exits 2
(`emit requires an explicit --receipts`); (iii) a receipt with whitespace-indented `# case=` and `# exit=` lines
is read by the new `header_multi` (show with a tiny fixture: the header is found, not `MISSING_HEADER`).
(d) prove `verify` wrote nothing to the receipts dir: `sha256sum corpus/evidence/round92/controls/receipts/*.txt`
before and after (a), compare.
Copy each receipt into your report folder. Report every observed line and exit code. VERDICT trailer required."""),

    item("R92ExecC2Repro", "executor", f"""Reproduce frozen C2 from a clean tree. `S={SCRATCH}/R92ExecC2Repro`; clone at `{CARRIER}`.
Run, from `$S/repo`:
(a) `python3 -B corpus/evidence/round92/curation-r92.py --root .` → record stdout + exit; expected `CURATION_R92=PASS`
with `LEGS_MEASURED=14/14 Q_SHAPE_FAIL=0 SOURCE_STATUS_OK=20/20 USED_BY_OK=20/20 TFREQ_OK=17/17 TFREQ_MAX_DF=3
UNENTAILED_TERM=0`.
(b) `python3 -B corpus/evidence/round92/curation-r92-controls.py --root . --work $S/ctl` → expected
`CONTROLS=PASS FORGERY_REFUSED=4/4 PRIOR_ACCEPTED=4/4 DUPCOUNT_R91=1 DUPCOUNT_R92=1 PRIOR_REGRESSION=7/7`.
(c) independently measure the decision-count pin: count pipe-leading rows of `## Decision table` in the two routed
entries (expect 11 and 6, all width 4) independent of the counter, and print the table.
(d) derive the minus-self digest by hand: a small read-only probe that re-implements `pins_file_sha_minus_self`
on `instrument-pins.txt` and shows it equals the stored self row; and a two-directional used-by check: every
mined row naming either entry is cited by that entry (independent count, via grep).
Copy receipts into your report folder. VERDICT trailer required."""),

    item("R92ExecC3Repro", "executor", f"""Reproduce frozen C3 from a clean tree. `S={SCRATCH}/R92ExecC3Repro`; clone at `{CARRIER}`.
Run, from `$S/repo`:
(a) `python3 -B corpus/evidence/round92/skill-tally-r92.py --root . --selftest corpus/evidence/round92/controls/selftest-r92.txt`
→ expected `SKILL_TALLY_R92=PASS` with `TALLY_ROWS=8 STALE_TALLIES=0/8 OTHER_OCCURRENCES=2
CASE_RANGE_BASHENV=273-275 CASE_RANGE_BASH_PIN=282-283 CASE_RANGE_OK=2/2 MISLABELED=0 OTHERS_OK=1 LEGS=3/3`.
(b) `python3 -B corpus/evidence/round92/skill-tally-r92-controls.py --root . --work $S/ctl` → expected
`CONTROLS=PASS OLDPROSE_REFUSED=1/1 PRIOR_ACCEPTED=1/1 STALE_REFUSED_BOTH=1/1`.
(c) re-derive the scoped others multiset by hand: find `## Gates` to next `## ` in `SKILL.md`, count the
non-current `PASS (N cases, M skipped)` occurrences inside (expect exactly `(161,0)` and `(256,0)`), and show the
set/ordering.
(d) run the counter with `--root {LANE}` (the committed tree) — same verdict; show the section boundary line
numbers (`## Gates` at 82, next `## ` at 576) by grep.
Copy receipts into your report folder. VERDICT trailer required."""),

    item("R92ExecMutations", "mutation-tester", f"""Mutation battery on the three r92 instruments. `S={SCRATCH}/R92ExecMutations`; `git clone --shared {LANE} $S/repo`;
checkout `{CARRIER}`. Mutate COPIES under `$S` only; never edit the lane.
For each mutant, copy `$S/repo/corpus/evidence/round92/<instrument>` into `$S/mut/<id>/`, apply one textual
change, run the matching counter on `$S/repo` (with `--selftest` for C3), and record verdict + exit.
C1 mutants: M1 `read_pins` ignores a duplicate path (returns dict without the raise); M2 `instrument_rels`
returns only the first rel; M3 `pin_report` wanted set drops the pins-file entry.
C2 mutants: M4 `data_lines` filter restored to also skip `qid`-first cells (the old filter); M5 `table_rows`
silently drops wrong-width rows (restore the silent `continue`); M6 `source_link` uses the substring test
(`entry in used`); M8 USED_BY leg deleted (the summary still prints PASS).
C3 mutants: M9 the tally scope is document-wide again (search `text` instead of `gates_text`); M10 the others
multiset comparison is deleted (the summary still prints PASS).
Also one control: M11 a mutant that only renames a variable (must SURVIVE and be reported as a survivor, proving
the battery is not a blanket refusal). Expected `MUTANTS_KILLED=8/9 SURVIVORS=1/9` (M11). Report the exact
command per mutant, the observed verdict line and exit. VERDICT trailer required."""),

    item("R92RevPrior", "revenger", f"""Independently reproduce the BEFORE state the claims rest on, from committed bytes only. `S={SCRATCH}/R92RevPrior`;
`git clone --shared {LANE} $S/base` and `git -C $S/base checkout {BASE}`; a second clone at `{CARRIER}` for the r92
instruments.
(a) C1 before: with the round-91 driver `corpus/evidence/round91/control-driver-r91.py`, demonstrate the three
mechanisms on the r92 fixture classes, from source only: (i) cite `read_pins` last-wins lines and show by
executing the r91 function a duplicate pin path collapsing to one entry; (ii) cite `instrument_rel` first-only
and execute it on a two-script command, showing only one rel; (iii) cite `pin_report`'s wanted set lacking the
pins file. No r91 verify PASS is claimed (impossible against the real table).
(b) C2 before: on the four S forged trees `curation-r92-controls.py` builds, show `curation-r91.py` prints
`CURATION_R91=PASS` on each (the frozen battery already records this as `PRIOR_ACCEPTED=4/4` — re-derive it
independently from the controls' own trees if they persist, else rebuild).
(c) C3 before: `skill-tally-r91.py` on the deleted-161 tree prints `SKILL_TALLY_R91=PASS` (build the tree as the
controls do).
(d) compare (a)-(c) with the committed before receipts
`corpus/evidence/round92/controls/receipts/c{1,2,3}-before.txt` at the carrier; flag any line that does not
re-derive.
Report every command, line and exit. VERDICT trailer required."""),

    item("R92ReviewerC1", "reviewer", f"""Attack frozen C1's STATED WORDING against the code. `S={SCRATCH}/R92ReviewerC1`; clone at `{CARRIER}`.
Read `{LANE}/corpus/evidence/round92/claims.md` C1 (clauses 1-9 + named limits) and
`corpus/evidence/round92/control-driver-r92.py`. For each clause, build the smallest fixture that makes the code
accept a state the sentence reads as refused, or refuse a state the sentence reads as accepted. At minimum attempt:
1. a receipt whose headers are indented by TWO spaces (`  # exit=0`) and whose body contains the required token —
   accepted? the sentence says "after leading whitespace is stripped";
2. a row whose instrument is `bash @ROOT@/x.sh` where x.sh is pinned but whose script internally calls a second
   script via `bash` (the command has ONE .sh token) — does the sentence's "EVERY file a row's command names"
   read as covering it?
3. the pins file edited so that only its self row's digest changes (not the minus-self content) — accepted?
4. `passed` with `EXACT_OK` short while `COMMITTED_OK` is full: can it print PASS? (built fixture)
5. `emit` with `--receipts` pointing under the lane — writes are allowed there; and `verify` never writes the
   receipts dir — prove it, or find the write.
For each attempt: command, observed verdict token + exit, and whether it falsifies the wording. If it does, name
the narrowing the L1 must record (an amendment to `plans/round-92.md`). Do not edit the lane; your artifacts
live under your folder. VERDICT trailer required."""),

    item("R92ReviewerC2", "reviewer", f"""Attack frozen C2's STATED WORDING against the code. `S={SCRATCH}/R92ReviewerC2`; clone at `{CARRIER}`.
Read `{LANE}/corpus/evidence/round92/claims.md` C2 and `corpus/evidence/round92/curation-r92.py`. Attempt at minimum:
1. a Located-quotes section with a pipe-leading line BEFORE the header row (`| stray |` as the first line) —
   does `quote_lines` reach it? the sentence says "every pipe-leading data row" and "the only skips are the
   structural header row (first table line) and all-dash separator rows" — is a leading stray a data row?
2. a mined registry row whose used-by names the entry as a full path PLUS trailing words (`...-r84.md quoted`) —
   tokenised exact match?
3. a decision row with 4 cells whose warrant cell cites a qid NOT in the quote rows — WARRANT fires?
4. a Located-quotes row with 3 cells and a valid Qn and S-id but an EMPTY quote — QSHAPE fires?
5. the sentence's `LEGS_MEASURED=14/14` — does it survive a tree where `WARRANT` fails? (the VERDICT leg binds
   fields_hold==prior_ok: show a tree where legs pass but fields fail.)
Report each: command, observed line + exit, falsifies-wording or neutral, and the narrowing to record if it
fires. Do not edit the lane. VERDICT trailer required."""),

    item("R92ReviewerC3", "reviewer", f"""Attack frozen C3's STATED WORDING against the code. `S={SCRATCH}/R92ReviewerC3`; clone at `{CARRIER}`.
Read `{LANE}/corpus/evidence/round92/claims.md` C3 and `corpus/evidence/round92/skill-tally-r92.py`. Attempt:
1. a scratch SKILL.md where the `## Gates` table is followed by a section whose heading is NOT `## ` prefixed
   (e.g. `# Round26` level-1, or an indented `  ## Round26`) — does the scope end where the sentence says?
2. a scratch SKILL.md whose `## Gates` section is deleted entirely — `SETUP` or `FAIL`? The sentence's kill rule
   K4 says "an absent clause is tolerated" is a finding class — is it?
3. a scratch selftest receipt where a case number is DUPLICATED with two different names — are duplicates counted
   in `EXPECTED_CASES`? The sentence says tallies equals the tool's verdict counts.
4. a scratch SKILL.md whose only change moves the `r39` clause from the Gates table to a line AFTER `## Round26`
   (inside another section) — scoped out (CLAUSE_MISSING) or silently found?
Report each: command, observed line + exit, falsifies-wording or neutral, and the narrowing to record if it
fires. Do not edit the lane. VERDICT trailer required."""),

    item("R92CriticClaims", "critic", f"""Falsify the claims' shared assumptions and the freeze itself. `S={SCRATCH}/R92CriticClaims`; clone at `{CARRIER}`.
Read claims.md, plans/round-92.md (including §Pre-wave freeze repair 1-2) and claims.json. Attempt, with artifacts:
1. **Freeze integrity:** does `instrument-pins.txt` match the committed bytes at F5 for all 16 pins (minus-self
   for the self row)? Re-derive with `git show {FREEZE}:<path> | sha256sum`. Does the carrier `{CARRIER}` carry
   receipts that pin `{FREEZE}`? Is every pinned non-history file byte-identical between F5 and the carrier?
2. **No-work control:** for each claim, build the cheapest state that skips the claimed work and check the frozen
   predicate cannot reach it.
3. **Cross-claim coupling:** can C3's PASS be reached while `## Gates` is renamed (e.g. `## gates`)? The sentence
   names the heading — does the code treat it case-sensitively?
4. **The plan's claim that no scored run preceded F5** — verify from git history (`git log --oneline F5..C5`), and
   flag any commit that runs or scores a candidate before F5 (the four superseded pairs must be pre-wire).
5. **Ledger pre-shape:** propose the rows the `claim-falsification.tsv` must carry (per claim, per attack seat) and
   check every attack seat in this wave is named.
Report each attempt with command + observed line + verdict (falsifies-wording / neutral) and the exact narrowing
needed. VERDICT trailer required."""),

    item("R92SentinelScope", "sentinel", f"""Scope and safety review of the round's instruments and dispatch text. `S={SCRATCH}/R92SentinelScope`;
clone at `{CARRIER}`.
1. Run EVERY command form printed in the wave context verbatim on correct bytes (C1 verify with `--root . --repo .`;
   C1 verify with `--root {LANE} --repo <clone>`; the forgery battery; the C2 counter and controls; C3 with the
   committed receipt and controls). Any form that fails on correct bytes is a finding.
2. Check `verify` never writes under `corpus/evidence/round92/controls/receipts/` (sha256 before/after) and that
   `--work` is the only write root.
3. Check no path escapes: grep the three instruments for `/tmp`, absolute writes, `HOME`, network calls
   (`urllib|socket|http`) and host mutations (`sysctl|sudo|systemctl`); report each hit with file:line.
4. Check the claim's self-pin reading against the printed line (`PINNED_FILES=7`, 16 pins total) and flag if the
   report would overstate it.
5. Check credential/secret shapes: `git grep -nE 'sk-|ghp_|AKIA|BEGIN [A-Z ]*PRIVATE KEY'` at the carrier → expect
   none; report.
6. Confirm NO file changed between F5 and C5 except the six receipts (`git -C {LANE} diff --name-only {FREEZE} {CARRIER}`).
Report commands, lines, exits. VERDICT trailer required."""),

    item("R92ConnectorSiblings", "connector", f"""Read-only sibling-overlap scan. `S={SCRATCH}/R92ConnectorSiblings`; do not edit any sibling.
Search the sibling lane repos under `/home/vgpnk/Projects/shokunin/*-shokunin/` (and their `corpus/evidence/*/` tools)
for the two classes this round hardens, and report file:line for each hit:
1. **self-referential pin tables** — a pins/sums file whose own digest is listed in itself, or a table read
   last-wins on repeated paths;
2. **section-scoped search** — counters that search a document font-wide where a section-scoped contract exists
   (heading-anchored extraction), or unpinned counts over historical quotations.
For each hit: lane, path:line, one-line reading, and whether it is the same class as chousa's C1 S5/self-pin or
C3's scoping. Do not absorb, copy or edit anything; the report is a pointer map. Also state explicitly what you
did NOT find (the sweep).
VERDICT trailer required."""),

    item("R92ScoutRegistry", "scout", f"""Per-surface reconnaissance of the registry and the corpus surfaces the claims read. `S={SCRATCH}/R92ScoutRegistry`;
clone at `{CARRIER}`.
1. Re-open S070's premise from committed bytes (this round): `/usr/share/man/man1/sha256sum.1.gz` sha256, the decompressed line
   that carries "Print or check SHA256 (256-bit) checksums.", and the registry row's anchor/`teaches` cells; report
   whether the row's recorded sha (`93c17dff…`) still matches.
2. Verify every source cited by the two routed entries' Located-quotes rows: S214, S018, S023, S215, S026, S031 —
   `status=mined` and `used-by` token-naming the citing entry; report any drift with the exact cell.
3. Re-derive from raw bytes: the two entries' Located-quote rows (expect 13 and 7, all width 3), their
   Decision-table rows (expect 11 and 6, all width 4), and whether the decision-count pin matches.
4. Check the registry census: `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root
   /home/vgpnk/Projects/shokunin chousa` → exit code and the row count (`grep -cE '^ {0,3}\\|[[:space:]]*S[0-9]{3,}'
   corpus/SOURCES.md`); report both.
Report commands, lines, exits; no edits. VERDICT trailer required."""),
]

SPEC = {
    "wave": "chousa-r92-w1",
    "reportDir": ".ufo/waves/round-92/w1",
    "context": CONTEXT,
    "items": ITEMS,
}

if __name__ == "__main__":
    out = os.path.join(HERE, "w1-spec.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(SPEC, fh, indent=1, ensure_ascii=False)
    print(f"wrote {out} items={len(ITEMS)}")
