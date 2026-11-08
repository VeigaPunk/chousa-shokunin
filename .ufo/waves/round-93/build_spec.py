#!/usr/bin/env python3
"""Build the round-93 wave-1 spec (12 seats, policy v1 band 8-16). Constants are the measured revisions."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
SCRATCH = "/fast/scratch/hyaku/chousa-r93"
BASE = "206226dc9d9baef620e7d3d30bdac5f9194a459f"
FREEZE = "b7241252c2358613d3b22b7d0454d98c56dab373"
CARRIER = "754b62fb6adc60e44e12375af5461a0ebe302994"
SUPERSEDED = "84998563 / (emitted at 84998563, never carried)"

GODSPEED = """/skill:godspeed

You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.
"""

CONTEXT = f"""Lane chousa round 93, L1 ChousaR93 holds the canonical planner seat, the freeze and the integration. Root {LANE}.
Revisions: base {BASE} (round-92 landing + its non-author spot-check, admitted); claim freeze F2 {FREEZE}; the
tree you attack is carrier C2 {CARRIER} (the freeze plus the six committed control receipts; the receipts pin
{FREEZE}). One earlier freeze/carrier pair ({SUPERSEDED}) was superseded before any scored run and before this
wave (its defect: self_pin took the pin dict for the pins path); treat F2/C2 as the freeze. The pins table has
22 rows: the 15 instrument/expectation/claims rows, six receipt rows, and the self row (minus-self digest).
Frozen predicate set: {LANE}/.ufo/waves/round-93/claims.md — read it FIRST, with every kill rule and every
NAMED LIMIT. Machine form: {LANE}/.ufo/waves/round-93/claims.json.
Three claims, three axes:
C1 operability (lowest scored, historical 3/10): `python3 -B corpus/evidence/round93/control-driver-r93.py verify
--root . --repo . --rev {FREEZE} --receipts-rev {CARRIER} --work <scratch>` prints `CONTROL_DRIVER_R93=PASS`
with `COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 PINNED_FILES=22/22 RECEIPT_PINS=6/6`; the battery
`forgeries-r93.py --root . --repo . --rev {FREEZE} --receipts-rev {CARRIER} --work <scratch>` prints
`FORGERY_REFUSED=2/2 PRIOR_ACCEPTED=2/2 DERIVE_OK=1/1 POSITIVE=pass`. Source S070 (installed sha256sum(1),
re-opened this round, quote "Print or check SHA256 (256-bit) checksums.") grounds the digest-pin rule including
the minus-self self-pin.
C2 calibration: `python3 -B corpus/evidence/round93/curation-r93.py --root .` prints `CURATION_R93=PASS` with
`LEGS_MEASURED=15/15 Q_SHAPE_FAIL=0 Q_WSQUOT=0 Q_ROWS=20 WARRANT_OK=17/17 TFREQ_OK=17/17 DUP_QIDS=0`
and `curation-controls-r93.py --root . --work <scratch>` prints `CONTROLS=PASS CARRIED_REFUSED_BOTH=4/4
WS_NAMED=2/2 WS_SHAPE_GREEN_R92=1/1 DUPCOUNT_1=1/1 PRIOR_REGRESSION=7/7`. This claim is CLASSIFICATION, not a
refusal r92 lacks: r92 fails the whitespace trees downstream with `Q_SHAPE_FAIL=0`.
C3 freshness: `python3 -B corpus/evidence/round93/skill-tally-r93.py --root . --selftest
corpus/evidence/round93/controls/selftest-r93.txt` prints `SKILL_TALLY_R93=PASS` with `LEGS=4/4
HIST_DERIVED=2/2 HIST_PRESENT=2/2 TAIL_OK=1 TALLY_ROWS=8 STALE_TALLIES=0/8 CASE_RANGE_OK=2/2 MISLABELED=0`;
`skill-tally-r93-controls.py --root . --work <scratch>` prints `CONTROLS=PASS OLDPROSE_REFUSED=1/1
PRIOR_ACCEPTED=1/1 STALE_REFUSED_BOTH=1/1 HIST_REFUSED_BOTH=1/1 TAIL_REFUSED=2/2 TAIL_PRIOR_ACCEPTED=1/1
TAIL_ADDED_REFUSED=1/1 HIST_UNGROUNDED_REFUSED=1/1`.
`tools/research-gate.sh` and `tools/gate-records.py` are UNCHANGED this round; SKILL.md is unchanged.

Every `Report:` trailer path is relative to {LANE} — write it at {LANE}/<that path>. Copy every receipt you cite
into your wave output folder before you yield.
Leaf only: no task tool, no subagents, no agent://all, no production edits, no lane or fleet git/jj mutation, no
commits or pushes, no edits to /home/vgpnk/Projects/shokunin/scripts, /home/vgpnk/Projects/shokunin/.ufo/state,
MANIFEST.json, considerthese/ or any sibling repo. The only files you write are under
{LANE}/.ufo/waves/round-93/w1/ plus your scratch dir. Network: none this round except a re-open an item names;
every other check reads committed bytes (an unrequested GET is a finding). Never mutate a host sysctl, never run
sudo, never restart a host service.
Scratch: every tree, work dir and fixture lives under {SCRATCH}/<your seat name>/; create it with `mkdir -p`,
pass it explicitly (`--work`, `TMPDIR=`), delete it before you yield (`trap 'rm -rf -- "$S"' EXIT` in shell,
`finally: shutil.rmtree` in Python). Never write under /tmp. For pin/self-pin checks you need history, so
`git clone --shared {LANE} <scratch>/repo` and `git -C <scratch>/repo checkout {CARRIER}`. Any fixture git repo
is `D=$(mktemp -d -p {SCRATCH}/<seat>) && test -n "$D" && git -C "$D" init -q`, every later git call names
`-C "$D"`, and you assert `git -C "$D" rev-parse --show-toplevel` equals `$D` before any mutating git command.
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
    item("R93ExecC1Repro", "executor", f"""Reproduce frozen C1 from a clean tree. `S={SCRATCH}/R93ExecC1Repro`; `git clone --shared {LANE} $S/repo`
then `git -C $S/repo checkout {CARRIER}`. Run, from `$S/repo`:
(a) `python3 -B corpus/evidence/round93/control-driver-r93.py verify --root . --repo . --rev {FREEZE} --receipts-rev {CARRIER} --work $S/verify`
→ record full stdout, the `CONTROL_DRIVER_R93=` line and the exit code; expected `COMMITTED_OK=6/6 EXACT_OK=6/6
PIN_OK=6/6 FRESH_OK=6/6 PINNED_FILES=22/22 RECEIPT_PINS=6/6` and `RECEIPT SELF_PIN OK rev={FREEZE} receipts_rev={CARRIER}`.
(b) `python3 -B corpus/evidence/round93/forgeries-r93.py --root . --repo . --rev {FREEZE} --receipts-rev {CARRIER} --work $S/forge`
→ expected `FORGERY_REFUSED=2/2 PRIOR_ACCEPTED=2/2 DERIVE_OK=1/1 POSITIVE=pass`; record each forgery line.
(c) prove the pin walk is not self-satisfying: take a byte-appended copy of an UNEXECUTED pinned instrument
(`corpus/evidence/round93/curation-controls-r93.py`) inside a scratch clone and show `PIN_DISK_MISMATCH path=...`
plus exit 1, while the same tamper is invisible to `corpus/evidence/round92/control-driver-r92.py --expected ...
--receipts ... --pins ...` on the same tree (rc 0). Then show a tampered receipt body fires `RECEIPT_MISMATCH`.
(d) prove `verify` writes nothing: `sha256sum corpus/evidence/round93/controls/receipts/*.txt` before and after (a).
Copy each receipt into your report folder. VERDICT trailer required."""),

    item("R93ExecC2Repro", "executor", f"""Reproduce frozen C2 from a clean tree. `S={SCRATCH}/R93ExecC2Repro`; clone at `{CARRIER}`.
Run, from `$S/repo`:
(a) `python3 -B corpus/evidence/round93/curation-r93.py --root .` → record stdout + exit; expected `CURATION_R93=PASS`
with `LEGS_MEASURED=15/15 Q_ROWS=20 Q_SHAPE_FAIL=0 Q_WSQUOT=0 SOURCE_STATUS_OK=20/20 USED_BY_OK=20/20
TFREQ_OK=17/17 UNENTAILED_TERM=0 WARRANT_OK=17/17 DUP_QIDS=0`.
(b) `python3 -B corpus/evidence/round93/curation-controls-r93.py --root . --work $S/ctl` → expected `CONTROLS=PASS
CARRIED_REFUSED_BOTH=4/4 WS_NAMED=2/2 WS_SHAPE_GREEN_R92=1/1 DUPCOUNT_1=1/1 PRIOR_REGRESSION=7/7`.
(c) independently measure the WSQUOTE class claim: build your OWN whitespace-quote tree (do not reuse the
controls' helper) by copying the two routed entries plus `corpus/SOURCES.md` and symlinking `corpus/captures`,
replace one Located-quotes quote cell with a single space, then run the R92 counter and the R93 counter on it.
Report: r92 `Q_SHAPE_FAIL=` value and its `LEG_FAIL` lines; r93 `Q_SHAPE_FAIL=`, `Q_WSQUOT=`, the named
`quote=<whitespace>` shape line and its `LEG_FAIL` lines. The claim is classification, so also say which legs
refused the tree in each counter.
(d) count the two routed entries' Located-quote rows (13 and 7, width 3) and Decision-table rows (11 and 6, width 4)
by hand, independent of the counter; report the tables.
Copy receipts into your report folder. VERDICT trailer required."""),

    item("R93ExecC3Repro", "executor", f"""Reproduce frozen C3 from a clean tree. `S={SCRATCH}/R93ExecC3Repro`; clone at `{CARRIER}`.
Run, from `$S/repo`:
(a) `python3 -B corpus/evidence/round93/skill-tally-r93.py --root . --selftest corpus/evidence/round93/controls/selftest-r93.txt`
→ expected `SKILL_TALLY_R93=PASS` with `TALLY_ROWS=8 STALE_TALLIES=0/8 CASE_RANGE_OK=2/2 MISLABELED=0
HIST_DERIVED=2/2 HIST_PRESENT=2/2 TAIL_TALLIES=2 OTHERS_OK=1 TAIL_OK=1 LEGS=4/4`.
(b) `python3 -B corpus/evidence/round93/skill-tally-r93-controls.py --root . --work $S/ctl` → expected `CONTROLS=PASS
OLDPROSE_REFUSED=1/1 PRIOR_ACCEPTED=1/1 STALE_REFUSED_BOTH=1/1 HIST_REFUSED_BOTH=1/1 TAIL_REFUSED=2/2
TAIL_PRIOR_ACCEPTED=1/1 TAIL_ADDED_REFUSED=1/1 HIST_UNGROUNDED_REFUSED=1/1`.
(c) prove the derivation is not decorative, independently of the controls battery: copy `SKILL.md` plus the two
grounding receipts into scratch, (i) change the `161` tally's grounding line in
`corpus/evidence/round25-final-measure.log` → expect `HIST_DERIVED=1/2` and exit 1; (ii) delete the `215` tail
tally from the copy → expect `TAIL_OK=0` and exit 1 while the r92 counter still exits 0; (iii) append an
undeclared tail tally → expect `HIST_SCOPE_BLEED` and exit 1 while r92 exits 0.
(d) re-derive the multiset by hand from `SKILL.md` alone (`## Gates` to the next depth<=2 heading; non-current
`PASS (N cases, M skipped)` cells) and list every tally inside and outside the scope with its line number.
Copy receipts into your report folder. VERDICT trailer required."""),

    item("R93ExecMutations", "mutation-tester", f"""Mutation battery on the three r93 instruments. `S={SCRATCH}/R93ExecMutations`; `git clone --shared {LANE} $S/repo`;
checkout `{CARRIER}`. Mutate COPIES under `$S` only; never edit the lane.
For each mutant, copy the instrument into `$S/mut/<id>/`, apply one textual change, run the matching counter on
`$S/repo` (with `--selftest` for C3, and `--root . --repo . --rev {FREEZE} --receipts-rev {CARRIER}` for C1),
and record the verdict line + exit code.
C1 mutants: M1 `pin_report` skips rows whose path it cannot resolve (silent `continue`); M2 `receipt_pins` counts a
receipt without comparing its bytes; M3 `self_pin` compares receipt rows at `rev` instead of `receipts_rev`;
M4 the `--root` derivation is reverted to `HERE`-based defaults.
C2 mutants: M5 `q_shape_violation` restores the r92 ordering (strip whitespace before quotes only);
M6 the WSQUOTE leg is deleted while `EXPECTED_LEGS` stays 15; M7 `Q_WSQUOT` counts only rows that passed shape;
M8 `EXPECTED_LEGS` is lowered to 14 with the leg deleted (the r92 hole).
C3 mutants: M9 the historical multiset is a frozen literal again (`{("161","0")}` / `{("256","0")}`); M10 the
receipt grounding check is deleted (`HIST_DERIVED` always 2/2); M11 the tail scan is deleted (`TAIL_OK` always 1).
Also one control: M12 a mutant that only renames a local variable (must SURVIVE and be reported as a survivor,
proving the battery is not a blanket refusal). Report `MUTANTS_KILLED=n/12 SURVIVORS=m/12` with the exact command,
observed verdict and exit per mutant. VERDICT trailer required."""),

    item("R93RevPrior", "revenger", f"""Independently reproduce the BEFORE state the three claims rest on, from committed bytes only.
`S={SCRATCH}/R93RevPrior`; `git clone --shared {LANE} $S/repo` and `git -C $S/repo checkout {CARRIER}`.
(a) C1 before, by executing the r92 driver's own functions on the r93 pins table: show (i) `pin_report`'s wanted
set covers only the six executed instruments plus expectations and pins (cite the lines, print `PINNED_FILES=7`),
(ii) `receipt_pins` does not exist in r92 and receipts are read but unpinned (show a tampered receipt accepted,
rc 0, on a scratch copy), (iii) the r92 `--expected/--receipts/--pins` defaults are `HERE`-relative
(`DEFAULT_*` lines) and a `--root <archive>` run without explicit paths exits non-zero with `escapes base`.
(b) C2 before: on a whitespace-quote tree you build yourself, show r92 prints `Q_SHAPE_FAIL=0` and refuses only
downstream; state which legs fired. Also show r92 has no `Q_WSQUOT` field anywhere in its source (`grep -c`).
(c) C3 before: show r92's `EXPECTED_OTHERS` is a frozen literal (cite the line) and that a tail-tally change
(`215` → `214`) leaves r92 at rc 0.
(d) Compare your findings with `corpus/evidence/round93/claims.md`'s Before paragraphs and report any disagreement
with the exact line. VERDICT trailer required."""),

    item("R93ReviewerC1", "reviewer", f"""Attack C1's frozen sentence against the committed code and receipts. `S={SCRATCH}/R93ReviewerC1`;
clone at `{CARRIER}`, read `corpus/evidence/round93/control-driver-r93.py`, `forgeries-r93.py`,
`corpus/evidence/round93/instrument-pins.txt` and `{LANE}/.ufo/waves/round-93/claims.md` C1.
Findings must be concrete: (1) does `PINNED_FILES=22/22` really cover all 22 rows, or does some row escape the
walk (e.g. a row whose file is the pins file, a path outside `--root`, a directory)? (2) Is the self row's
minus-self digest actually load-bearing (can a rewrite of another row keep it green)? (3) Can a receipt be
counted as pinned while its row is stale? (4) Does `passed` really require `checked == len(pins)` and
`rchecked == rtotal`? (5) Is the `--root` derivation genuinely `--root`-relative in every branch (emit and
verify), or does any branch still read `HERE`? (6) Are the two forgeries in the battery the *cheapest*
interesting ones, or does an easier class survive (e.g. an expected row deleted, a pin row for an absent file)?
For each: name the line, the command you ran, the observed output and whether it FIRES or HOLDS. Do not edit the
lane. VERDICT trailer required."""),

    item("R93ReviewerC2", "reviewer", f"""Attack C2's frozen sentence against the committed code and receipts. `S={SCRATCH}/R93ReviewerC2`;
clone at `{CARRIER}`, read `curation-r93.py`, `curation-controls-r93.py` and claims C2.
Findings must be concrete: (1) is `Q_WSQUOT` counting the intended population (three-cell rows whose quote
strips to empty) and can it be made to fire on a CLEAN registry-shaped row? (2) Does the WSQUOTE leg fail for the
right reason on each of the two whitespace trees, and would a four-cell whitespace row be counted? (3) Is
`EXPECTED_LEGS=15` actually load-bearing (delete the leg from a copy and show the verdict changes)? (4) Does the
`DECISION_WIDTH` print line fire for a wrong-width row, and is it only observability (i.e. does the verdict
already fail without it)? (5) Does the controls battery's `WS_SHAPE_GREEN_R92` assertion hold if r92's shape test
changes? (6) Is the "classification not refusal" framing honest — i.e. does any part of the claim still imply
r92 accepts those trees? Quote the claim line and say so.
For each: name the line, the command, the observed output and FIRES or HOLDS. Do not edit the lane. VERDICT
trailer required."""),

    item("R93ReviewerC3", "reviewer", f"""Attack C3's frozen sentence against the committed code and receipts. `S={SCRATCH}/R93ReviewerC3`;
clone at `{CARRIER}`, read `skill-tally-r93.py`, `skill-tally-r93-controls.py` and claims C3.
Findings must be concrete: (1) do the two grounding quotes really appear in the named receipts at the named
lines, and does the counter require the *quote* (not just the file)? (2) Can `HIST_DERIVED` be 2/2 while a
grounding receipt is absent (path resolution, symlink, `--root` escape)? (3) Does `HIST_PRESENT` really require
the tally inside the Gates scope, and is `declared` the derived multiset (not a literal)? (4) Does the tail scan
start exactly at the scope end offset (no off-by-one, no duplicate-line blindness)? (5) Would a tally moved from
inside the scope to outside it be refused (i.e. is `TAIL_DECLARED` not a loophole)? (6) Does `case-range` still
bind at the landing bytes, and does the enumeration pin still hold at 283 cases?
For each: name the line, the command, the observed output and FIRES or HOLDS. Do not edit the lane. VERDICT
trailer required."""),

    item("R93CriticClaims", "critic", f"""Falsify the three claims as *claims*: freeze integrity, control discipline, sizing. `S={SCRATCH}/R93CriticClaims`;
clone at `{CARRIER}`.
(1) Freeze integrity: recompute every sha256 in `corpus/evidence/round93/instrument-pins.txt` against the blobs at
`{FREEZE}` and `{CARRIER}` (which rows belong to which revision, per the driver's own rule), and the minus-self
digest from the committed file. Report any row whose base is wrong or whose digest cannot be re-derived.
(2) Does any claim assert a value its counter does not print? Check each numeric token in claims C1/C2/C3 against
the counter source's printed fields (quote the print statement). 
(3) Is any claim reachable by a do-nothing control? For each claim, describe the cheapest control that does no
work and say whether it meets the after-state; C2 is explicitly a classification claim, so say whether its
after-state (`Q_SHAPE_FAIL=1 Q_WSQUOT=1` named) is reachable without the landed code.
(4) Are the claims causally separable — is each verifiable with the others' instruments absent or reverted?
(5) Any universal clause ("all", "every", "no ... anywhere") that the counting command does not enumerate?
(6) Does the round's own §9 discipline hold: predicate frozen before scoring, no target narrowed after landing?
Quote the claim line for every finding. VERDICT trailer required."""),

    item("R93SentinelScope", "sentinel", f"""Perimeter and harm review of the round's committed surface. `S={SCRATCH}/R93SentinelScope`; clone at `{CARRIER}`.
(1) Scope: list every path in `git diff --name-only {BASE}..{CARRIER}` and say whether each is inside the lane's
write scope (lane repo files only); flag anything touching `tools/`, `corpus/SOURCES.md`,
`corpus/knowledge/`, `SKILL.md`, `MANIFEST.json`, sibling repos, the fleet root, `.scratch/`, `.ufo/state/`.
(2) Harm: run the subject tools unchanged — `bash tools/research-gate.sh --selftest` tail (expect
`PASS (283 cases, 0 skipped)`) and `python3 -B tools/gate-records.py verify` if it has a read-only mode over the
round's lesson; report exit codes. Confirm `git diff {BASE}..{CARRIER} -- tools/` is empty.
(3) Credential/secret shape: scan the new files for material that looks like a live credential, private key,
token or absolute home path outside the lane (report file:line; do not print any suspect value in full).
(4) Confinement: does the driver's `verify` path ever write outside `--work`? Does `emit` refuse without
`--receipts`? Does any new tool write under `/tmp` regardless of TMPDIR/`--work`?
(5) Host safety: confirm no new file mutates sysctls, runs sudo, or restarts a service.
Report findings with file:line and observed command output; FIRES/HOLDS per item. VERDICT trailer required."""),

    item("R93ConnectorSiblings", "connector", f"""Sibling-overlap scan, read-only. `S={SCRATCH}/R93ConnectorSiblings`; no writes outside your scratch dir and
`{LANE}/.ufo/waves/round-93/w1/`.
(1) Scan the sibling lane repos under `/home/vgpnk/Projects/shokunin/*-shokunin/corpus/evidence/` for a
pins-table walk, a receipt-pin mechanism, a whitespace-quote shape rule, or a historical-tally derivation that
this round re-invents. Report the closest match per pattern with path:line, and say whether chousa's version is
distinct or a duplicate of a sibling's (a duplicate is a finding).
(2) Cross-lane checkpoint ledger convention: does any sibling record an evidence-directory-wide pin table with a
minus-self row? Quote it.
(3) Report any sibling rule that chousa's new instruments violate (e.g. a shared QUALITY criterion about
`--root`-relative defaults or about evidence naming). Read-only: change nothing in a sibling repo.
VERDICT trailer required."""),

    item("R93ScoutSources", "scout", f"""Per-surface reconnaissance of the registry and the sources the claims cite. `S={SCRATCH}/R93ScoutSources`;
clone at `{CARRIER}`.
1. Re-open S070's premise from committed bytes and the installed page: `/usr/share/man/man1/sha256sum.1.gz`
   sha256 (expect `93c17dffe9f25d56291113d566a7de3ff65c29f8cc32c381801c49cf27e8403f`), the exact line carrying
   "Print or check SHA256 (256-bit) checksums.", and the registry row's anchor and `teaches` cells. Report match or
   drift with the exact cell text.
2. Re-open S001 (own-work chain row): find the tool line its Gate names, quote it, and report whether the row's
   `recheck` cell names round 92 or round 93 (the round plans to move it 92 → 93; report the current value).
3. Verify every source cited by the two routed entries' Located-quotes rows: S214, S018, S023, S215, S026, S031 —
   `status=mined` and `used-by` token-naming the citing entry; report any drift with the exact cell.
4. Census: `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root
   /home/vgpnk/Projects/shokunin chousa` → exit code; row count via
   `grep -cE '^ {0,3}\\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md`; list the W04 warnings.
Report commands, lines, exits; no edits. VERDICT trailer required."""),
]

SPEC = {
    "wave": "chousa-r93-w1",
    "reportDir": ".ufo/waves/round-93/w1",
    "context": CONTEXT,
    "items": ITEMS,
}

if __name__ == "__main__":
    out = os.path.join(HERE, "w1-spec.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(SPEC, fh, indent=1, ensure_ascii=False)
    print(f"wrote {out} items={len(ITEMS)}")
