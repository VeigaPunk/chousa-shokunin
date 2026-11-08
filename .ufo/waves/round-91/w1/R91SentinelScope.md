# R91SentinelScope — scope and safety review of round-91's instruments and dispatch text

Seat: `R91SentinelScope`. Lane: chousa. Wave: round-91 w1.
Attack target: carrier **C3** `67954adc599bd605705d94a1ea7abb582491a907` (freeze **F3** `4d00d7519290569879f853d7122b82a927cda1f3`).
Scratch: `/fast/scratch/hyaku/chousa-r91/R91SentinelScope` (removed on yield). Clone: `git clone --shared` at C3.
Receipts: `.ufo/waves/round-91/w1/R91SentinelScope-receipts/`.

Tool installs: **none**. No pacman / uv / npm transaction was run this round; every check used committed bytes plus
the tools already present (`git`, `python3`, `bash`, `sha256sum`, `zcat`, `awk`, `grep`). Nothing to record.

---

## 0. Summary

The six instruments run and print their frozen values on the correct bytes; the write scope of `verify` is clean; the
credential grep is clean; the SKILL.md repair is one clause. Five scope defects and one dispatch-text defect were
found. The two that matter most are **F-1** (the claim's own printed C1 command cannot run — `--work` is required and
absent from the printed form) and **F-2** (the pin leg covers 6 of 16 pinned paths on disk, and the 10 uncovered paths
include every round-91 instrument and the C3 selftest receipt, so a coherent on-disk edit to the C3 receipt flips C3's
verdict while C1 still prints `PINNED_FILES=6 ... PASS`).

Severity ladder: F-1 and F-2 = high (a reader following the frozen text gets a wrong answer or a false pass); F-3 =
medium (C3's residual `r82 pin-override cases 276–283` clause is not bound by either leg — the repair moved the
prose but left an unbound range assertion behind); F-4 = medium-low (`emit` writes the committed receipts directory in
place — the verify path is clean, the sibling mode is not); F-5 = low (`bash -lc` sources the user's login profile, so
profile output reaches the fresh-leg token matcher); F-6 = low (an archive tree without `.git` fails the fresh leg).

---

## 1. Every command form printed in the wave context, run verbatim on correct bytes

### 1a. C1 verify — the printed form **fails**

Command (verbatim from the wave context / `claims.md` C1 statement / `.ufo/waves/round-91/claims.json` `counting_command[0]`):

```
cd <clone at C3> && python3 -B corpus/evidence/round91/control-driver-r91.py verify --root . --repo . \
  --rev 4d00d7519290569879f853d7122b82a927cda1f3 --receipts-rev 67954adc599bd605705d94a1ea7abb582491a907
```

Observed (receipt `c1-verify-printed-form.out`):

```
usage: control-driver-r91.py [-h] --root ROOT --work WORK --rev REV
                             [--repo REPO] [--receipts-rev RECEIPTS_REV]
                             [--expected EXPECTED] [--receipts RECEIPTS]
                             [--pins PINS]
                             {emit,verify}
control-driver-r91.py: error: the following arguments are required: --work
```

**exit 2.** No `CONTROL_DRIVER_R91=` line is printed at all.

**F-1 (high) — the frozen C1 counting command is not runnable as printed.**
`control-driver-r91.py:278` declares `ap.add_argument("--work", required=True)` (present at F3 and unchanged at C3 —
`git show 4d00d751:corpus/evidence/round91/control-driver-r91.py | grep -n add_argument` shows `--root/--work/--rev`
all `required=True`). Every printed form of the C1 command — the wave-context line, `corpus/evidence/round91/claims.md`
C1 statement, and `.ufo/waves/round-91/claims.json` `counting_command[0]` — omits `--work`. A reader who copies the
frozen text verbatim gets an argparse usage error, not `CONTROL_DRIVER_R91=PASS`. The plan already records exactly
this failure mode as a pre-wave repair for a *row* (`plans/round-91.md` §Pre-wave freeze repair 1, defect 1: "argparse
exited 2 before the tool printed `HARM_RECHECK_ERROR`"); the same defect survives at the *command* level in all three
frozen places.
*Exploit path:* none needed — a reader trusts the frozen text and records "C1 not runnable" or, worse, a seat that
adds `--work` ad hoc records a PASS whose provenance differs from the frozen command.
*Impact:* the C1 predicate as printed is unverifiable; a scoring seat cannot distinguish "the driver passes" from
"the driver was called with arguments the frozen text never mentions".
*Smallest remediation:* add `--work <scratch>` to the printed command in `claims.md`, `claims.json` and the wave
dispatch, or make `--work` default to a temp dir for `verify` — but the receipt-freezing semantics of `verify` argue
for the former.

### 1b. C1 verify with `--work` supplied (the same form, completed)

`--root . --repo .` (clone at C3, work = scratch), receipt `c1-verify-clone-root-repo-root.out`:

```
BASES root=/fast/scratch/.../repo repo=/fast/scratch/.../repo
RECEIPT c1-gate-r89 OK committed+exact+pin+fresh
RECEIPT c1-mutants-r89 OK committed+exact+pin+fresh
RECEIPT c1-harm OK committed+exact+pin+fresh
RECEIPT c1-harm-setup OK committed+exact+pin+fresh
RECEIPT c2-prior-landing OK committed+exact+pin+fresh
RECEIPT c2-prior-controls OK committed+exact+pin+fresh
RECEIPT PINS OK 6/16 pinned files byte-identical
RECEIPT SELF_PIN OK rev=4d00d7519290569879f853d7122b82a927cda1f3 receipts_rev=67954adc599bd605705d94a1ea7abb582491a907
COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 PINNED_FILES=6 CONTROL_DRIVER_R91=PASS
```
**exit 0.** All frozen C1 fields present, `SELF_PIN` names both revisions.

`--root /home/vgpnk/Projects/shokunin/chousa-shokunin --repo <clone>` (lane root, clone as the blob source), receipt
`c1-verify-lane-root-clone-repo.out`: identical six `RECEIPT ... OK` lines, `RECEIPT PINS OK 6/16`,
`RECEIPT SELF_PIN OK rev=4d00d751... receipts_rev=67954adc...`, `COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6
FRESH_OK=6/6 PINNED_FILES=6 CONTROL_DRIVER_R91=PASS`. **exit 0.**

`--root . --repo .` run from the lane root itself (HEAD `0c85c9ac`, carrier is its ancestor): same PASS line, exit 0.

### 1c. C1 forgery battery

`python3 -B corpus/evidence/round91/control-forgeries-r91.py --work <scratch>` (receipt `c1-forgery-battery.out`):

```
OK dup-header-exit: r91 rc=1 (HEADER_DUPLICATE:exit), r90 rc=0
OK dup-header-computed: r91 rc=1 (HEADER_DUPLICATE:computed_against), r90 rc=0
OK instrument-stub: r91 rc=1 (INSTRUMENT_PIN_MISMATCH:fx-tool.sh), r90 rc=0
OK expected-swap: r91 rc=1 (INSTRUMENT_PIN_MISMATCH:expected.tsv), r90 rc=0
OK missing-expected_exit: r91 rc=1 (MISSING_HEADER:expected_exit), r90 rc=0
OK extra-receipt: r91 rc=1 (UNSCORED_RECEIPT), r90 rc=0
OK positive: r90 rc=0 r91 rc=0
FORGERY_REFUSED=6/6 PRIOR_ACCEPTED=6/6 POSITIVE=pass
```
**exit 0.** All six classes refused by r91, accepted by the unchanged r90 driver, positive accepted by both.

### 1d. C2 counter and controls

`python3 -B corpus/evidence/round91/curation-r91.py --root .` — receipt `c2-counter-clone.out` (clone at C3) and
`c2-counter-lane.out` (lane working tree). The two outputs are byte-identical (`diff` exit 0). Both:

```
SUPERSEDED_LIVE=0 UNENTAILED_TERM=0 MODIFIED_DEF_CITED=1 QUOTES_LOCATED=20/20 Q_ROWS=20 Q_SHAPE_FAIL=0
SOURCE_STATUS_OK=20/20 USED_BY_OK=20/20 Q_FLOORS=... WARRANT_OK=17/17 TFREQ_OK=17/17 TFREQ_MAX_DF=3 DUP_QIDS=0
TEACHES_CHECKED=1 TEACHES_FLAGGED=1 TEACHES_UNRESOLVED=0 SUP_CLAUSE_CHECKED=0 SUP_UNRESOLVED=0 LEGS_MEASURED=13/13
VERDICT fields_hold=1 legs_ok=13/13 DETECTOR_WITNESS=11/11
CURATION_R91=PASS
```
**exit 0.** Every frozen C2 field present, including `LEGS_MEASURED=13/13`, `UNENTAILED_TERM=0`,
`VERDICT fields_hold=1`, `DETECTOR_WITNESS=11/11`.

`python3 -B corpus/evidence/round91/curation-r91-controls.py --root . --work <scratch>` — receipts
`c2-controls-clone.out` / `c2-controls-lane.out` (identical):

```
OK positive: r90 CURATION_R90=PASS r91 CURATION_R91=PASS
OK nonq-row: r91 CURATION_R91=FAIL (LEG_FAIL QSHAPE), r90 CURATION_R90=PASS
OK status-rejected: r91 CURATION_R91=FAIL (LEG_FAIL SOURCE), r90 CURATION_R90=PASS
OK used-by-blank: r91 CURATION_R91=FAIL (LEG_FAIL SOURCE), r90 CURATION_R90=PASS
OK ubiquitous-warrant: r91 CURATION_R91=FAIL (LEG_FAIL TFREQ), r90 CURATION_R90=PASS
OK duplicate-count: r90 UNENTAILED_TERM=2 r91 UNENTAILED_TERM=1
OK regression: FORGERY_REFUSED=7/7 PRIOR_REGRESSION=7/7 rc=0
CONTROLS=PASS FORGERY_REFUSED=4/4 PRIOR_ACCEPTED=4/4 DUPCOUNT_R90=2 DUPCOUNT_R91=1 PRIOR_REGRESSION=7/7
```
**exit 0.**

### 1e. C3 counter and controls

**At the attacked carrier C3** (receipt `c3-counter-carrier.out`) the C3 counter does **not** print the claimed
values, and the controls refuse to run:

```
CASE_RANGE_FINDING RANGE_MISMATCH:bash-pin-override claimed=276-283 derived=282-283
CASE_RANGE_FINDING MISLABELED=6 indices=276,277,278,279,280,281
TALLY_ROWS=9 STALE_TALLIES=0/9 EXPECTED_CASES=283 EXPECTED_SKIPPED=0 OTHER_OCCURRENCES=3
CASE_RANGE_BASHENV=273-275 CASE_RANGE_BASH_PIN=282-283 CASE_RANGE_OK=1/2 MISLABELED=6 LEGS=1/2
LEG_FAIL CASE-RANGE
SKILL_TALLY_R91=FAIL
```
**exit 1.** And `skill-tally-r91-controls.py --root . --work <scratch>` at C3 prints
`SETUP repaired clause absent from SKILL.md — is this the landing tree?`, **exit 2**.

This is expected and disclosed: the wave context states the C3 repair is *not* in the committed tree and lands after
the wave. The C3 claim is therefore about the **landing** revision, not the carrier.

**At the lane working tree** (which carries the one-clause `SKILL.md` repair), receipt `c3-counter-landing-worktree.out`:

```
TALLY_ROWS=9 STALE_TALLIES=0/9 EXPECTED_CASES=283 EXPECTED_SKIPPED=0 OTHER_OCCURRENCES=3
CASE_RANGE_BASHENV=273-275 CASE_RANGE_BASH_PIN=282-283 CASE_RANGE_OK=2/2 MISLABELED=0 LEGS=2/2
SKILL_TALLY_R91=PASS
```
**exit 0** — every frozen C3 field present. Controls (receipt `c3-controls-landing-worktree.out`):

```
OK old-prose: r90 ... SKILL_TALLY_R90=PASS, r91 SKILL_TALLY_R91=FAIL
OK stale-tally: r90 ... STALE_TALLIES=1/9 ... SKILL_TALLY_R90=FAIL (rc=1), r91 SKILL_TALLY_R91=FAIL (rc=1)
CONTROLS=PASS OLDPROSE_REFUSED=1/1 PRIOR_ACCEPTED=1/1 STALE_REFUSED_BOTH=1/1
```
**exit 0.**

**F-3 (medium) — C3's repair left an unbound range clause behind.**
The repaired `SKILL.md` cell now reads (grep, landing working tree):

```
r39 bash-pin cases 273–275 (pin-bashenv, drift-bashenv) and r82 pin-override cases 276–283, of which bash-pin-override cases 282–283
```

`skill-tally-r91.py` binds exactly two clauses: `BASHENV_RE = r"r39 bash-pin cases (\d+)[–-](\d+)"` (line 37) and
`OVERRIDE_RE = r"bash-pin-override cases (\d+)[–-](\d+)"` (line 38). The middle phrase **`r82 pin-override cases
276–283`** matches neither regex, so it is asserted in the shipped prose and never checked. Proof (receipt
`probe-c3-residual-clause-unbound.txt`): a scratch `SKILL.md` with that phrase rewritten to `r82 pin-override cases
200–999` still prints `CASE_RANGE_OK=2/2 MISLABELED=0 LEGS=2/2` / `SKILL_TALLY_R91=PASS`, exit 0.
*Why it matters:* `276–283` is precisely the mislabeled span the round set out to fix. The derived families from the
committed receipt's own names are `bashenv` = {273,274,275} and `bash-pin-override*` = {282,283}; the indices
276–281 carry `pin-env-fn-*`, `env-pin-override-*` and `pin-bash-path-shim`. A reader of the landing `SKILL.md` sees
"276–283" attached to a "pin-override" family and cannot tell it is stale, because the counter will not object.
*Smallest remediation:* either delete the residual phrase from the `SKILL.md` cell, or extend the counter with a third
regex (`pin-override cases N–M`) whose derived family is `{279,280,282,283}` (span 279–283) so the cell's three claims
are all bound. The plan's own §9 already treats the "r82" attribution as out of scope for the binding ("the round that
added a case is not derived"), but the *range* 276–283 is a bound-looking number and should not sit unchecked.

---

## 2. `verify` write scope — receipts directory untouched, `--work` is the only write root

**Receipts directory unchanged.** `sha256sum` of all nine files under `corpus/evidence/round91/controls/receipts/`
before and after the verify runs is identical (`receipts-dir-hashes-before.txt` vs `receipts-dir-hashes-after.txt`,
`diff` exit 0). The verify path opens receipts read-only (`control-driver-r91.py:337` `open(path).read()`,
`:377`, `:398`).

**Whole-tree unchanged.** A full `sha256sum` of every file in the lane tree (36 430 files) before and after a
C1 verify run is identical; the diff file is empty (`lane-tree-diff-c2c3.txt`, 0 bytes, `diff` exit 0). The same holds
for the C2 counter and the C2 controls run against the lane tree.

**`--work` is the only write root.** The driver writes `fresh-<case>.out` into `--work`
(`control-driver-r91.py:356`) and creates `--work` itself (`:301`). Every instrument it shells out to writes under
`@WORK@` (e.g. `controls/expected.tsv` rows pass `--work @WORK@/c1gate`, `@WORK@/c1mut`, `@WORK@/c2ctl`).

**F-4 (medium-low) — the sibling `emit` mode writes the committed receipts directory in place.**
`control-driver-r91.py:304` `os.makedirs(a.receipts, exist_ok=True)` and `:311` write `row["case"] + ".txt"` into the
receipts directory; `DEFAULT_RECEIPTS` is `HERE/controls/receipts` — i.e. the *committed* directory inside the tree,
not the scratch. Proof (receipt `probe-emit-writes-committed-receipts.txt`): on a scratch copy of C3,
`control-driver-r91.py emit --root . --work <scratch> --rev 000...0` rewrote all six committed receipts in place;
`c1-harm.txt` changed from `4cb0ba34…` to `685a87e4…`, and `EMITTED=6 MISMATCH=0` (exit 0).
The *claim* only forbids the **verification** path from writing there, and the verify path is clean — this is a scope
hazard in the sibling mode, not a claim violation. It matters because `emit` is the mode L1 uses to mint the carrier,
and nothing in the instrument stops an `emit` against a tree whose receipts are already committed.
*Smallest remediation:* make `emit` require an explicit `--receipts` (no default into the tree), or refuse to write
into a receipts directory that already contains committed receipts without `--force`.

**F-5 (low) — `bash -lc` lets the user's login profile into the fresh-leg token matcher.**
`control-driver-r91.py:139` runs each row as `subprocess.run(["bash", "-lc", cmd], …)`. `-l` is a *login* shell, so
`/etc/profile` and `~/.bash_profile` are sourced and their stdout/stderr is concatenated into the body the token
matcher reads (`:140` `(p.stdout or "") + (p.stderr or "")`). Proof (receipt `probe-login-shell-profile-leak.txt`): with
`HOME` pointed at a scratch dir whose `.bash_profile` echoes `moved=0` and `records=1`, the c1-harm row becomes
`RECEIPT c1-harm FINDING FRESH_DUPLICATE_KEY:records` and the run ends `FRESH_OK=5/6 … CONTROL_DRIVER_R91=FAIL`,
exit 1 — profile output reached the matcher and created a duplicate key. This is a robustness/hermeticity defect
(fail-closed here, but a profile that emits a *wanted* token could satisfy a body check), not a claim violation.
*Smallest remediation:* use `bash -c` with `env -i` (or set `HOME`/`BASH_ENV` to a scratch dir) for the fresh leg.

**F-6 (low) — the fresh leg needs a git working tree, so an archive-extracted root fails.**
The `c1-harm` row runs `git -C @ROOT@ show 265b8633…:tools/gate-records.py`, so `--root` must be a git checkout.
On a `git archive` extraction (no `.git`) the row dies with `FRESH_EXIT:128` and the run ends
`FRESH_OK=4/6 … CONTROL_DRIVER_R91=FAIL` (receipt `probe-archive-root-fails.txt`, exit 1). This is consistent with the
wave's own instruction to clone for pin/self-pin checks, but it means the printed command's `--root .` is only valid in
a checkout, and the failure message (`FRESH_EXIT:128`) does not say why.

---

## 3. Path escapes and host mutations — grep of the three instruments

Grep of `corpus/evidence/round91/*.py` (the three claim instruments plus their three controls) and of the five
prior-round instruments the C1 rows execute:

| pattern | hits | file:line |
|---|---|---|
| `/tmp` | **none** | — |
| `urllib|socket|requests\.|http[s]?://` | 1 | `corpus/evidence/round91/curation-r91.py:106` — `re.findall(r"https?://[^\s|)>\]]+", cells[1])`: a *regex over cell text*, not a network call |
| `sysctl|sudo|systemctl` | **none** | — |
| `HOME` | 1 | `corpus/evidence/round91/controls/expected.tsv:4` — the `c1-harm` row: `HOME=/home/vgpnk git -C @ROOT@ show 265b8633…:tools/gate-records.py > @WORK@/harm/base-tool.py`. `HOME` is set to the operator's home so `git show` finds its config; the write target is `@WORK@`, an absolute path *outside* the tree but inside scratch |
| absolute path literals | 1 | `controls/expected.tsv:4` (`/home/vgpnk`) — same row |

No instrument writes to an absolute path outside `--work`; `control-driver-r91.py`'s writes are `--work`-relative
(`:301`, `:356`) and the receipts dir only in `emit` mode (F-4). `curation-r91.py` opens files read-only
(`:92`, `:110`, `:266`). `curation-r91-controls.py` writes only under `--work` (`:84-85`, `:148` alias) and symlinks
`corpus/captures` and `corpus/evidence/round57` into the scratch mirror (`:52`) — read-only use of the real tree.
`skill-tally-r91-controls.py` writes scratch `SKILL.md` copies under `--work` (`:59-65`). No `shell=True`, no
`os.system`, no `popen` anywhere; every subprocess call is an argv list.

**No host mutation** was attempted by any instrument: no `sudo`, no `sysctl`, no `systemctl`, no service restart, and
no write under `/tmp` (the round's own scratch rule is honoured: everything of mine lives under
`/fast/scratch/hyaku/chousa-r91/R91SentinelScope`).

---

## 4. `SELF_PIN` / `PINNED_FILES` — the report would overstate it

The printed line is `RECEIPT PINS OK 6/16 pinned files byte-identical` and the summary carries `PINNED_FILES=6`.
`instrument-pins.txt` has **16** rows; `control-driver-r91.py:238` increments `checked` only for the files the leg
actually looks at.

**F-2 (high) — the pin leg checks 6 of the 16 pinned paths on disk; the other 10 are never compared to their
on-disk bytes.**
`pin_report()` (`:212-240`) builds `wanted` from `instrument_rel(row, root)` — the first `.py`/`.sh` token of each
row's command — plus the expectations file. The six expected rows execute five distinct prior-round instruments
(`gate-records-r89.py`, `mutate-r89.py`, `harm-recheck-r90.py` ×2 rows, `curation-r89.py`,
`curation-r89-controls.py`) plus `controls/expected.tsv` = 6 paths. The remaining **10 pinned paths — every round-91
instrument, `controls/selftest-r91.txt`, `claims.md`, `claims.json`, `plans/round-91.md` — are never sha256'd on
disk**; they are only checked as *blobs at `--rev`* through `pin_at_rev()` (`:242-253`, called from `self_pin()` at
`:270`).
*Exploit path (measured, receipt `probe-pin-leg-coverage.txt`):* on a scratch copy of C3, append one line to
`corpus/evidence/round91/curation-r91.py` — the C2 instrument — so its on-disk bytes are `db58f80f…` while the pin
still says `c607c15c…`. `control-driver-r91.py verify --root . --repo . --rev F3 --receipts-rev C3` still prints
`RECEIPT PINS OK 6/16 pinned files byte-identical` and
`COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 PINNED_FILES=6 CONTROL_DRIVER_R91=PASS`, **exit 0**. The
tampered C2 instrument is then scored by the C2 leg with no pin evidence against it.
The same hole reaches C3's verdict. `skill-tally-r91.py` reads the case names from the **on-disk** selftest receipt
(`--selftest corpus/evidence/round91/controls/selftest-r91.txt`), which is one of the 10 uncovered pinned paths.
Measured (receipt `probe-c3-doctored-receipt-false-pass.txt`): on a scratch copy of C3, rename cases 276–281 in that
receipt to `bash-pin-override-fake`; the **old, unrepaired** prose now reads as self-consistent and the counter
prints `CASE_RANGE_BASH_PIN=276-283 CASE_RANGE_OK=2/2 MISLABELED=0 LEGS=2/2` / `SKILL_TALLY_R91=PASS`, **exit 0** —
the C3 claim's K2 discrimination is defeated by an edit to a file the pin file claims to protect, while the C1 verify
on the same doctored tree still prints `PINNED_FILES=6 … CONTROL_DRIVER_R91=PASS` (exit 0).
*Impact:* "16 pins" reads as "every instrument and receipt is digest-checked"; in fact 6 paths are digest-checked on
disk and 10 are only revision-checked. The C3 freshness claim's own input (the selftest receipt) is unguarded on
disk, so the claim's `MISLABELED=0` leg is only as strong as the receipt's integrity — and the receipt's integrity is
checked nowhere on disk.
*Smallest remediation:* make `pin_report()` iterate the **whole** pin file (all 16 paths) for the on-disk digest, and
have `self_pin()` compare each pinned path's disk bytes to its blob at `--rev` rather than only to its pin entry. Then
`PINNED_FILES=16` would be truthful and the C3 receipt would be covered.

**Reading the printed `SELF_PIN` line correctly.** `RECEIPT SELF_PIN OK rev=4d00d751… receipts_rev=67954adc…` names
both revisions, as C1 rule 7 requires. `self_pin()` (`:255-271`) compares, against blobs in `--repo`: the driver
script and the expectations file at `--rev`, every `*.txt` in the receipts directory at `--receipts-rev`, and every
pinned path's blob at `--rev` via `pin_at_rev`. Note the `rel_for(root, …)` base separation (QUALITY 202) is real and
load-bearing: running the *clone's* driver with `--root` pointed at the lane produced
`RECEIPT PINS FINDING INSTRUMENT_UNPINNED:../../../../../fast/scratch/…/repo/corpus/evidence/round91/controls/expected.tsv`
and `RECEIPT SELF_PIN FINDING SELF_DRIFT …` — the base mismatch is caught, not silently tolerated (exit 1). Good.

---

## 5. Credential / secret shapes at the carrier

```
git -C <clone> grep -nE 'sk-|ghp_|AKIA|BEGIN [A-Z ]*PRIVATE KEY' 67954adc599bd605705d94a1ea7abb582491a907 -- .
```
→ **1925** `sk-`, **348** `ghp_`, **341** `AKIA`, **0** `BEGIN [A-Z ]*PRIVATE KEY` matching lines. Every hit is
accounted for and none is a credential:

* `sk-` — 320 copies of the gate's own detector regex `sk-[A-Za-z0-9_]{10,}` and 320 of the planted self-test literal
  `sk-fxdemo_not_real_0000` (`tools/research-gate.sh:1085`, `:4633`, `:5130` and the ~320 archived copies under
  `.ufo/waves/**/`); the remaining ~864 are substrings of ordinary words — `risk-bias` (91), `mask-gate.sh` (82),
  `disk-guard.sh` (30), `task-list` (24) — where `sk-` spans "ri**sk-**bias"/"ma**sk-**gate".
* `ghp_` / `AKIA` — 320 each from the same detector regexes (`tools/research-gate.sh:1086`, `:1088`), the rest from
  documentation prose in `corpus/captures/` and `corpus/lessons/` describing what the detector looks for.
* A high-confidence pattern — `(^|[^A-Za-z0-9_-])(sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{30,}|AKIA[A-Z0-9]{16}|-----BEGIN
  [A-Z ]*PRIVATE KEY-----)` — returns **no matches at all** (exit 1).

**No live credential material is committed at the carrier.** The naive `sk-` pattern is dominated by word
substrings and by the gate's own detector; a length-and-anchor-constrained pattern finds nothing.

---

## 6. The SKILL.md repair is one clause; the working tree carries more than that

`git -C /home/vgpnk/Projects/shokunin/chousa-shokunin diff -- SKILL.md` → **one line changed, one line added**
(`1	1	SKILL.md`), inside the single `research-gate` registry row's self-test cell. The whole diff is the clause
rewrite quoted in F-3.

**But the working tree is not clean, and the item's "no other file is modified" premise does not hold:**

```
 M SKILL.md                              (1 line, the C3 clause)
 M corpus/QUALITY.md                     (43 lines added — criteria 203–210)
 M corpus/evidence/round57/refetch.tsv   (1 line added — the failed S221 fetch row, rc 28)
?? .ufo/waves/round-91/w1.ready
?? .ufo/waves/round-91/w1.ready.dispatched
?? corpus/evidence/round91/after/
?? corpus/evidence/round91/census-end.txt
?? corpus/evidence/round91/census-start.txt
?? corpus/lessons/round-91.md
```

The `SKILL.md` change itself is exactly the one clause C3 names, and nothing else in `SKILL.md` moved (the other
seven registry rows and all nine tally cells are byte-identical; `TALLY_ROWS=9 STALE_TALLIES=0/9 OTHER_OCCURRENCES=3`
on the working tree equals the carrier's `OTHER_OCCURRENCES=3`, so C3's K3 "a historical tally or quote moves" is
**held**). The `QUALITY.md` and `refetch.tsv` edits are the round's own bookkeeping (criteria 203–210 and the
disclosed failed S221 fetch) and are not part of the C3 repair, but they *are* uncommitted working-tree changes at the
time of the wave — so "SKILL.md is the only modified file" is not what the tree shows. (Listing taken at 08:21; two
further files, `SCORECARD.md` and `plans/round-91.md`, were modified by other seats later in the wave — see §8.)

The landed `SKILL.md` cell also carries a **third** range phrase that the counter does not bind (F-3), and the phrase
`r39 bash-pin cases 273–275` is still bound by `BASHENV_RE` while the new parenthetical `(pin-bashenv, drift-bashenv)`
names only two of the three `bashenv` cases (`pin-bashenv-root` at 275 is omitted). That parenthetical is prose the
counter ignores, so it is harmless to the predicate but incomplete as documentation.

---

## 7. Attribution of the case indices (context for F-3)

Derived from the committed receipt's own names (`controls/selftest-r91.txt`, 283 `ok-case` rows):

* `bashenv` family → {273 `pin-bashenv-echo`, 274 `drift-bashenv-echo`, 275 `pin-bashenv-root`} → span 273–275.
* `bash-pin-override*` (prefix) → {282 `bash-pin-override-missing`, 283 `bash-pin-override-fake`} → span 282–283.
* `pin-override*` (substring) → {279, 280, 282, 283} → span **279–283**, not 276–283.
* 276–281 carry `pin-env-fn-echo-scrub`, `pin-env-fn-suppress`, `pin-env-fn-root`, `env-pin-override-missing`,
  `env-pin-override-fake`, `pin-bash-path-shim` — none of them is a `bash-pin-override` case.

History (`git log -S <case name> -- tools/research-gate.sh`): `pin-bashenv-*` arrived in `b905217a` (r37);
`pin-env-fn-*` and `env-pin-override-*` in `504c1d2a` (r38); `pin-bash-path-shim` and `bash-pin-override-*` in
`6d914e95` (r39). The r82 landing `51a5dee8` added **no** `ok-case` print (its own diff adds
`sweeps-fail-duplicate-rejections`, `sweeps-fail-claim-cell-placeholder` and one more sweep case — and its
`selftest-repaired.txt` already carries the same 276–283 mapping). So the shipped phrase "r82 pin-override cases
276–283" attributes to r82 a family and a range that r82 did not introduce and that the tool's own names contradict.
The plan's §"Claim selection" already concedes "the round that added a case is not derived", so this is *not* a
predicate violation — but it is a shipped sentence in `SKILL.md` that is both historically wrong and unchecked, which
is why F-3 asks for it to be either deleted or bound.

---

## 8. What I did not run (and why)

* **No fresh `bash tools/research-gate.sh --selftest`.** The wave context states the fresh battery (~6 minutes) is
  required only where an item says so; my items do not. Every C3 number above comes from the committed
  `controls/selftest-r91.txt` receipt, which is what the claim's counting command names.
* **No network fetch.** The only source the round opened is S070, the *installed* `sha256sum(1)` man page. I
  re-opened it locally (no GET) to confirm the claim's quote: `/usr/share/man/man1/sha256sum.1.gz` sha256
  `93c17dffe9f25d56291113d566a7de3ff65c29f8cc32c381801c49cf27e8403f` — byte-identical to the digest recorded in
  `corpus/SOURCES.md:80` — and decompressed line 11 reads `Print or check SHA256 (256\-bit) checksums.`, the exact
  quote C1 cites. S070's scope is confirmed; note `corpus/SOURCES.md:83` records S073 as *superseding* S070
  ("`supersedes S070 —` the `-c, --check` entry is a DESCRIPTION `.TP` item, not a SYNOPSIS line"), and the round's
  source list still names S070. The quote is at decompressed line 11 either way (S073's own anchor), so the claim's
  citation is accurate on substance but points at a superseded row — a citation-hygiene nit for L1, not a scope defect.
* **No lane mutation by me.** The only bytes I wrote in the lane are this report and
  `.ufo/waves/round-91/w1/R91SentinelScope-receipts/`. At the start of my session (08:21) `git status` showed
  `M SKILL.md`, `M corpus/QUALITY.md`, `M corpus/evidence/round57/refetch.tsv` plus six untracked paths — all pre-existing
  lane work, none of them mine. Two further tracked files (`SCORECARD.md`, mtime 08:43; `plans/round-91.md`, mtime
  08:45) became modified *during* my session by other seats writing concurrently; I did not touch either, and
  `SKILL.md` is unchanged since 08:04 (before my session) with `git diff --numstat -- SKILL.md` still `1  1`. No
  commits, no pushes, no `git`/`jj` mutation of the lane or the fleet repo; all my trees were scratch clones.

---

## 9. Findings table

| id | severity | one-line | evidence |
|---|---|---|---|
| F-1 | high | The frozen C1 command omits the required `--work`; run verbatim it exits 2 with an argparse usage error and never prints `CONTROL_DRIVER_R91=PASS` | `c1-verify-printed-form.out` (exit 2); `control-driver-r91.py:278` |
| F-2 | high | The pin leg digest-checks 6 of 16 pinned paths on disk; the 10 uncovered include every round-91 instrument and the C3 selftest receipt, so an on-disk edit to that receipt flips C3 to a false `SKILL_TALLY_R91=PASS` while C1 still prints `PINNED_FILES=6 … PASS` | `probe-pin-leg-coverage.txt`, `probe-c3-doctored-receipt-false-pass.txt` (both exit 0) |
| F-3 | medium | The repaired `SKILL.md` cell keeps a third range phrase, `r82 pin-override cases 276–283`, that neither counter regex binds; rewriting it to `200–999` still passes | `probe-c3-residual-clause-unbound.txt` (exit 0) |
| F-4 | medium-low | `emit` (sibling mode of the C1 driver) writes the committed receipts directory in place; only `verify` is required to be clean, and it is | `probe-emit-writes-committed-receipts.txt` (exit 0, six receipts rewritten) |
| F-5 | low | `bash -lc` in the fresh leg sources the user's login profile; profile stdout reaches the token matcher | `probe-login-shell-profile-leak.txt` (exit 1, `FRESH_DUPLICATE_KEY:records`) |
| F-6 | low | The fresh leg needs a git checkout at `--root`; an archive extraction fails with an opaque `FRESH_EXIT:128` | `probe-archive-root-fails.txt` (exit 1) |

Clean results recorded for completeness: C1 forgery battery `FORGERY_REFUSED=6/6 PRIOR_ACCEPTED=6/6 POSITIVE=pass`
(exit 0); C2 counter `CURATION_R91=PASS` with every frozen field, byte-identical on clone and lane (exit 0); C2
controls `CONTROLS=PASS FORGERY_REFUSED=4/4 PRIOR_ACCEPTED=4/4 DUPCOUNT_R90=2 DUPCOUNT_R91=1 PRIOR_REGRESSION=7/7`
(exit 0); C3 on the landing working tree `SKILL_TALLY_R91=PASS` with every frozen field and
`CONTROLS=PASS OLDPROSE_REFUSED=1/1 PRIOR_ACCEPTED=1/1 STALE_REFUSED_BOTH=1/1` (exit 0); C3 on the carrier `FAIL` /
`CASE_RANGE_OK=1/2 MISLABELED=6` (exit 1) and controls `SETUP` (exit 2), both as the wave context discloses; the
receipts directory and the whole 36 430-file lane tree are byte-identical before and after every verify/counter run;
no `/tmp`, no network call, no `sysctl`/`sudo`/`systemctl`; no credential shapes at the carrier under an
anchor-and-length-constrained pattern; `SKILL.md` working-tree repair = exactly one clause.

---

VERDICT: R91SentinelScope C1 fired — the frozen C1 counting command omits the required `--work` and exits 2 when run verbatim, though every other C1 field (6/6 COMMITTED/EXACT/PIN/FRESH, `PINNED_FILES=6`, both SELF_PIN revisions, `FORGERY_REFUSED=6/6 PRIOR_ACCEPTED=6/6 POSITIVE=pass`) prints correctly on the carrier.
VERDICT: R91SentinelScope C2 held — the counter prints `CURATION_R91=PASS` with every frozen field (identical bytes on clone and lane) and the controls print `CONTROLS=PASS FORGERY_REFUSED=4/4 PRIOR_ACCEPTED=4/4 DUPCOUNT_R90=2 DUPCOUNT_R91=1 PRIOR_REGRESSION=7/7`, both exit 0; the only C2-scope defect found is the sibling C1 `emit` mode writing committed receipts (F-4).
VERDICT: R91SentinelScope C3 fired — on the landing working tree the counter prints every frozen field with `MISLABELED=0` and the controls pass, but the shipped clause still asserts an unbound `r82 pin-override cases 276–283` (F-3) and the C3 selftest receipt is outside the C1 on-disk pin coverage (F-2).
