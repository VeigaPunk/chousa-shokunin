# R89SentinelScope — round-89 adversarial scope and safety review

Seat: `R89SentinelScope` (leaf; no dispatch, no production edits, no git/jj mutation).
Lane root: `/home/vgpnk/Projects/shokunin/chousa-shokunin`.
Bytes attacked: `ac0a0892c15de11fb28d3208f2b287687c00477e` (the freeze; its parent is the base `f8fa55ec`).
Scratch (now deleted): `/fast/scratch/hyaku/chousa-r89/R89SentinelScope` — every tree, fixture and probe lived there; all
cited receipts were copied into `.ufo/waves/round-89/w1/R89SentinelScope/receipts/` before cleanup.
Network: none. No `sudo`, no sysctl, no service restart. No file was written outside
`.ufo/waves/round-89/w1/R89SentinelScope*` and the scratch tree. Tool installs: none (no tool was needed).

Evidence convention: every finding names the exact command, the receipt path under
`.ufo/waves/round-89/w1/R89SentinelScope/receipts/`, the observed line and the exit code.

---

## Summary

| # | Item | Result | Severity |
|---|------|--------|----------|
| (a) | Egress — zero fetches | **HELD** — no violation | — |
| (b) | Control-receipt discipline (round-88 F7) | **FIRES (5 findings)** | medium ×3, low-medium ×2 |
| (c) | Credential shape | **HELD** — no credential-shaped material | — |
| (d) | Scope | **FIRES (2 findings)** | low ×2 |
| (e) | Attribution | **HELD** — one observation | info |

The two claims' *printed predicates* hold on the frozen bytes (I re-ran the committed control battery in an isolated
tree: 7 of 8 committed receipts reproduce byte-identically; the eighth is explained in B3). What fires is the
**control discipline around them** — the driver never checks the committed receipt bytes it is meant to police, the
harm control can pass without measuring anything, and C2's expectation row does not require the observable C2's own
frozen claim names.

---

## (a) Egress — zero fetches — **HELD**

### The bound I chose, and the row count for it

The lane's only fetch ledger is `corpus/evidence/round57/refetch.tsv`. Its fifth column is spelled **`fetched_utc`**,
and every value carries a `Z` (UTC). The freeze instant is the commit's **committer** date,
`2026-11-08T05:45:24-03:00` = **`2026-11-08T08:45:24Z`** (the author date, `05:30:44-03:00` = `08:30:44Z`, is 14m40s
earlier and was also checked; the bound holds under both).

```sh
R=/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round57/refetch.tsv
awk -F'\t' -v f="2026-11-08T08:45:24Z" 'NR>1 && $5<f{c++} END{print "rows_older_than_freeze="c+0}' "$R"
# observed: rows_older_than_freeze=184     exit=0
awk -F'\t' -v f="2026-11-08T08:45:24Z" 'NR>1 && $5>=f{c++} END{print "rows_at_or_after_freeze="c+0}' "$R"
# observed: rows_at_or_after_freeze=0       exit=0
awk -F'\t' 'NR>1{if($5>m){m=$5;id=$1}} END{print id, m}' "$R"
# observed: S216 2026-11-08T06:50:40Z       exit=0
```

**Non-zero row count for the bound: 184 data rows are strictly older than the freeze; 0 rows are at-or-after it.**
(185 lines minus the header.)

Receipt: `receipts/a-egress-refetch-bound.txt` (also prints the column header spelled out by name, column 5 =
`fetched_utc`).

### No `corpus/captures/` file is newer than the freeze

```sh
L=/home/vgpnk/Projects/shokunin/chousa-shokunin
FZ=$(date -u -d "2026-11-08 05:45:24 -0300" +%s)     # 1794127524
find "$L/corpus/captures" -type f -newermt "@$FZ" -printf '%TY-%Tm-%TdT%TH:%TM:%TS %p\n' | sort
# observed: (no lines)                     count_newer_than_freeze=0   exit=0
git -C "$L" status --porcelain corpus/captures | wc -l
# observed: capture_worktree_diff_lines=0  exit=0
git -C "$L" log -1 --format='%H %cI %s' -- corpus/captures
# observed: 667a5d09… 2026-11-08T03:06:26-03:00 (round-86 landing)  exit=0
```

181 capture files in the tree, 181 in `HEAD`; the newest by mtime is
`corpus/captures/b1b13a12aee75c6ecc20fb91.txt` at `2026-11-08T03:50:40` local = `06:50:40Z` — 1h55m **before** the
freeze. That file is the S216 capture C1 cites, and its mtime matches the `S216 … 2026-11-08T06:50:40Z` row in the
ledger exactly, i.e. the capture was fetched in an earlier round and only read this round.

Receipt: `receipts/a-egress-captures-bound.txt`.

### Corroboration

* The round-89 instruments contain **no network call**: `grep -nE 'socket|urlopen|requests\.|urllib' corpus/evidence/round89/*.py`
  returns only string literals about `curl_rc=` fields; `subprocess` is used exclusively for `python3 -B <local script>`
  and `git -C <repo> grep`.
* The lane's fetch ledger has not been touched since round 87: `git log -1 -- corpus/evidence/round57/refetch.tsv` →
  `e6e920a4… 2026-11-08T03:52:30-03:00`. The round-89 freeze adds no new fetch row.
* The three other `refetch*` artefacts in the lane (`.ufo/waves/round-82/…`, `.ufo/waves/round-83/…`) are copies from
  rounds 82–83; their newest date token is `2026-11-06T20:53:08Z`.

**No finding.** Zero fetches this round.

---

## (b) Control-receipt discipline (the round-88 F7 defect) — **FIRES**

`expected.tsv` has 8 rows; `controls/receipts/` has 8 committed files. I read every row against every receipt, then
re-ran the committed driver in an isolated tree built at the freeze.

### The good part (state it, because it is real)

For all 8 rows, every `required_fields` token is present in the committed receipt, and the driver's live exit codes
match `expected_exit` (all 0):

```
c1-landing: expected_exit=0 ALL_REQUIRED_TOKENS_PRESENT
c1-prior-instrument: expected_exit=0 ALL_REQUIRED_TOKENS_PRESENT
c1-mutants: expected_exit=0 ALL_REQUIRED_TOKENS_PRESENT
c1-harm: expected_exit=0 ALL_REQUIRED_TOKENS_PRESENT
c2-landing: expected_exit=0 ALL_REQUIRED_TOKENS_PRESENT
c2-prior-instrument: expected_exit=0 ALL_REQUIRED_TOKENS_PRESENT
c2-controls: expected_exit=0 ALL_REQUIRED_TOKENS_PRESENT
c2-mutants: expected_exit=0 ALL_REQUIRED_TOKENS_PRESENT
```

Receipt: `receipts/b-receipt-vs-expectation.txt`. Driver re-run (`RECEIPT_OK` ×8, `CONTROL_RECEIPTS=PASS`, exit 0):
`receipts/b-driver-rerun.txt`. The driver is also non-vacuous — a synthetic failing row is refused with
`RECEIPT_MISMATCH zprobe-failing: exit=1 want=0 missing[PASS_TOKEN_NOT_PRESENT]`, `CONTROL_RECEIPTS=FAIL`, exit 1
(`receipts/b-probe-nonnull-vacuity-and-substring.txt`).

The five findings below are what is *not* covered by that check.

---

### B1 — medium — the driver checks a receipt it just wrote, never the committed receipt bytes

**Defect.** `controls/run-controls.sh:16,23` sets `REC="$HERE/receipts"` and `out="$REC/$case_id.txt"`, then line 25
runs `( cd "$ROOT" && eval "$instrument" ) >"$out" 2>&1` and greps **that file**. The committed receipt at
`$REC/$case_id.txt` is overwritten before it is ever read. The check therefore proves "a fresh run of this instrument
produces these tokens with this exit code" — it does not prove "the committed receipt agrees with its expectation row",
which is the exact round-88 F7 defect the plan says this driver repairs ("the receipts were never checked against their
expectations"; plan §Inputs defect 5).

**Exploit path.** A committed receipt that contradicts its expectation row is invisible: edit
`corpus/evidence/round89/controls/receipts/c1-landing.txt` so the last line reads `GATE_RECORDS_R89=FAIL`, then run
the driver. It regenerates the file and reports success. The committed bytes that a reader of the freeze sees can
disagree with `expected.tsv` forever, undetected by the lane's own control instrument.

**Evidence.**

```sh
T=/fast/scratch/hyaku/chousa-r89/R89SentinelScope/tree
sed -i 's/GATE_RECORDS_R89=PASS/GATE_RECORDS_R89=FAIL/' "$T/corpus/evidence/round89/controls/receipts/c1-landing.txt"
cd "$T" && bash corpus/evidence/round89/controls/run-controls.sh "$T" .../ctl
```

Observed:

```
#   RECEIPT_OK c1-landing exit=0
#   RECEIPT_OK c1-prior-instrument exit=0
#   …
#   CONTROL_RECEIPTS=PASS
#   driver exit code: 0
```

and after the run the receipt's last line is `GATE_RECORDS_R89=PASS` again (regenerated, tamper erased).
Receipt: `receipts/b-probe-committed-receipt-tamper.txt`.

Note that the *receipts themselves* are correct today — I verified all 8 committed receipts against their rows
independently and every token agrees. So the round's committed evidence is sound; the **instrument that polices it is
not**. That is the finding.

**Impact.** The round-88 F7 shape (expectation ↔ receipt disagreement filed beside an unread table) is closed by
*convention and by this seat's manual check*, not by the committed driver. A future round that trusts the driver as
the discipline inherits the hole.

**Smallest remediation.** Have the driver write to `$WORK/receipts/` and compare (`diff`) against
`$HERE/receipts/$case_id.txt`, failing with `RECEIPT_MISMATCH` on any byte difference; or, before overwriting, check
the committed file's tokens and exit non-zero if they disagree.

---

### B2 — low-medium — `required_fields` are matched as bare substrings, so a wrong value passes

**Defect.** `run-controls.sh:29` uses `grep -qF -- "$f" "$out"` — fixed-string substring, not field equality. The
expected values are ratios and counts (`D1_REFUSED=3/3`, `LEG_REREAD=16/16`, `MUT_ADMIT_KILLED=1`), so a receipt
printing a *different* value that merely starts with the expected text satisfies the row.

**Evidence.** Synthetic row requiring `D1_REFUSED=3/3 LEG_REREAD=16/16 MUT_ADMIT_KILLED=1` whose instrument prints
`D1_REFUSED=3/30 LEG_REREAD=16/160 MUT_ADMIT_KILLED=1x`:

```
RECEIPT_OK zprobe-substr exit=0
CONTROL_RECEIPTS=PASS
driver_exit=0
```

Receipt: `receipts/b-probe-nonnull-vacuity-and-substring.txt`.

**Impact.** The expectation table cannot distinguish `16/16` from `16/160`, `3/3` from `3/30`, `KILLED=1` from
`KILLED=1x`. A counter that printed a wrong denominator with a matching prefix would pass the control battery —
precisely the "printed field detached from its measurement" family C1 claims to close.

**Smallest remediation.** Compare fields, not substrings: parse the `key=value` tokens out of the receipt and require
exact `key → value` equality (e.g. `awk -F= '$1=="D1_REFUSED" && $2!="3/3"{bad=1} END{exit bad}'`), or anchor the grep
with a word-boundary/line-end pattern.

---

### B3 — medium — the driver is not reproducible against the frozen revision; the `c1-harm` receipt does not reproduce

**Defect.** `expected.tsv` hard-codes `--root`/`--repo` to the **live lane working tree**
(`/home/vgpnk/Projects/shokunin/chousa-shokunin`) for every row. The driver therefore measures whatever the working
tree holds *now*, not the bytes at `ac0a0892`. The lane's working tree has moved since the freeze (an untracked
`corpus/lessons/round-89.md` carrying 2 `GATE-RECORD` lines), so the committed `c1-harm` receipt no longer
reproduces:

```
committed : HARM_RECHECK files=13 records=29 moved=0 base_rc=0 r88_rc=0
regenerated: HARM_RECHECK files=14 records=31 moved=0 base_rc=0 r88_rc=0
```

All 8 rows still pass (`moved=0` is still present, exit still 0), so the drift is silent — the receipt states a
different measurement than a re-run produces, and nothing compares them.

**Evidence.** `cd $T && bash corpus/evidence/round89/controls/run-controls.sh "$T" .../ctl` → `CONTROL_RECEIPTS=PASS`,
exit 0; byte compare against the committed receipts → `c1-harm.txt: DIFFERS` (all seven others `IDENTICAL`).
Corroboration: `grep -l 'GATE-RECORD' corpus/lessons/*.md` → 14 files live vs 13 in the frozen tree; the extra is
`corpus/lessons/round-89.md` (untracked, `git status --porcelain` → `?? corpus/lessons/round-89.md`).
Receipt: `receipts/b-driver-rerun.txt`.

**Impact.** A "control receipt" that is a function of a mutable working tree is not evidence about the frozen
revision; the round-89 control battery cannot be replayed against the commit it certifies.

**Smallest remediation.** Point the rows at a tree materialised from the pinned revision (e.g. the same
`git archive ac0a0892 | tar -x -C "$WORK/tree"` used here) and record the revision the receipt was taken against in
the receipt header.

---

### B4 — medium — the harm control passes vacuously, and its `required_fields` cannot see a setup failure

**Defect, two parts.**

1. `expected.tsv`'s `c1-harm` row requires exactly one token: `moved=0`. It does not require `records>=1`, nor
   `base_rc=0`, nor `r88_rc=0` — even though `harm-recheck.py` prints all three.
2. `harm-recheck.py` returns `0 if moved == 0 else 1` and counts `moved` only over records the tool actually
   produced. If the tool cannot run at all, there are no records, so `moved=0` and the exit is 0.

**Exploit path.** A tree where the subject tool exits 2 on every invocation (usage/IO error) yields
`HARM_RECHECK files=13 records=0 moved=0 base_rc=2 r88_rc=2` and **exit 0** — the driver prints `RECEIPT_OK c1-harm
exit=0` and `CONTROL_RECEIPTS=PASS`. The harm control reports "nothing moved" when it measured nothing.

**Evidence.**

```sh
# fixture: a git repo (toplevel asserted) whose tools/gate-records.py always exits 2
python3 -B corpus/evidence/round89/harm-recheck.py --root "$D" --repo "$D" --base-tool broken-tool.py
# observed: HARM_RECHECK files=1 records=0 moved=0 base_rc=2 r88_rc=2
#           exit=0
# same shape on the frozen tree: HARM_RECHECK files=13 records=0 moved=0 base_rc=2 r88_rc=2   exit=0
```

Additionally, structurally: the row extracts the base tool as `git show master:tools/gate-records.py`, and `master` is
the freeze itself (`git rev-parse master` == `ac0a0892`), while the tool blob is identical at base and freeze
(`dc7a4176…` at `f8fa55ec`, `ac0a0892` and `master`; working tree clean). `harm-recheck.py` runs the tool twice — once
with that base blob, once with the working-tree `tools/gate-records.py` — and both invocations therefore execute **the
same bytes**; `moved=0` is guaranteed by construction, not measured. And the tool is what the round did *not* change:
round 89's edit is to the battery `gate-records-r89.py`, which `harm-recheck.py` never invokes (it calls
`tools/gate-records.py verify` only), so this control cannot observe a battery-induced movement even in principle.
Its own header compounds the confusion — the file is byte-identical to `corpus/evidence/round88/harm-recheck.py` and
still calls itself "the round-88 C1 harm control" and prints a "Usage:" line naming `round88/harm-recheck.py`.

**Impact.** C1's kill rule K3 ("harm: a genuine committed `GATE-RECORD` line moves verdict (`moved > 0`)") rests on this
control. As wired it can neither fire nor report that it did not measure.

**Smallest remediation.** Add `records>=1` and `base_rc=0 r88_rc=0` to the `c1-harm` `required_fields` (and make
`harm-recheck.py` exit non-zero when `records == 0` or either rc is non-zero); take the base tool from the pinned base
revision (`f8fa55ec:tools/gate-records.py`) rather than from `master`.

---

### B5 — low-medium — C2's expectation row does not require the observable C2's own frozen claim names

**Defect.** `corpus/evidence/round89/claims.md` (C2, Sentence) says the counter prints a verdict "computed from the
fields the summary printed (`VERDICT fields_hold=1`) rather than from a separate `all(ok)`". The counter does not print
that string on the passing path: `curation-r89.py:316` appends the `VERDICT` leg with the detail string
`fields_hold=1 legs_ok=8/8`, and the print loop emits a leg's detail **only when it fails**
(`if not ok: print(f"LEG_FAIL {name} {detail}")`). The committed receipt `controls/receipts/c2-landing.txt` therefore
contains no `VERDICT` token at all — `VERDICT fields_hold=0 …` appears only in the *failing* mutant receipts
(`c2-mutants.txt`).

Two further wording gaps in the same sentence: it says "nine legs" while the counter's printed summary is
`LEGS_MEASURED=8/8` (`EXPECTED_LEGS = 9`, but the `VERDICT` leg is appended after the summary string is built — the
same "summary counts only what existed when it was built" shape that round 89 minted criterion 192 for), and the
`c2-landing` expectation row requires neither `VERDICT fields_hold=1` nor a leg total.

**Exploit path.** A counter that dropped the field-derived verdict entirely and printed `CURATION_R89=PASS`
unconditionally — while still printing `DUP_QIDS=0 WARRANT_OK=17/17 QUOTES_LOCATED=20/20 TEACHES_FLAGGED=1
TEACHES_UNRESOLVED=0 SUP_UNRESOLVED=0` — satisfies the committed `c2-landing` expectation row exactly. The control
battery therefore cannot distinguish the repaired counter from the round-88 one on this row.

**Evidence.** `grep -n 'VERDICT' corpus/evidence/round89/curation-r89.py` → line 316 only (the append); the receipt
`controls/receipts/c2-landing.txt` contains `LEGS_MEASURED=8/8` and no `VERDICT` token; the `c2-mutants` receipt shows
`LEG_FAIL VERDICT fields_hold=0 legs_ok=7/8` — i.e. the string only ever appears on failure.
(The mutants do prove the field-derived verdict is load-bearing — `M1-dead-teaches` and `M2-detached-leg` die on
`LEG_FAIL VERDICT fields_hold=0` — so the *implementation* is sound; the *published observable* is what is missing.)

**Impact.** C2's own predicate names an output the counter does not produce, and the `c2-landing` expectation row does
not close the gap. (The mutant battery *does* discriminate — `M1`/`M2`/`M3` die on `LEG_FAIL VERDICT fields_hold=0` —
so the field-derived verdict is load-bearing in the implementation; it is the published observable and the expectation
row that are missing.) This is the round-89-minted criterion 192 shape ("a summary field never reports a total that
includes items appended after it") recurring in C2 while being fixed in C1.

**Smallest remediation.** Print the verdict as a summary cell (`FIELDS_HOLD=1`) or print the `VERDICT` leg detail
unconditionally, add `VERDICT fields_hold=1` (or `FIELDS_HOLD=1`) to the `c2-landing` `required_fields`, and state the
leg total the counter actually appends.

---

### B6 — info — the "after" receipts are byte-identical copies of the "before/control" receipts

`corpus/evidence/round89/after/c1-after.txt` == `controls/receipts/c1-landing.txt` and
`after/c2-after.txt` == `controls/receipts/c2-landing.txt` (byte-identical). Round 88 committed its `after/` receipts
in the *integration* commit (`f7cedcad`), not in the freeze; round 89's freeze carries them. They are therefore not an
independent post-landing measurement of the landing tree — they are copies of the pre-freeze control outputs. Low
severity, but the header "after" overstates what they witness. (No remediation required if the landing is the freeze,
as the brief states; if a separate landing lands, they should be re-taken there.)

---

## (c) Credential shape — **HELD**

No credential-shaped material in the round's new files. Three pattern sets over every path in the freeze commit plus
`.ufo/waves/round-89/` and `plans/round-89.md`:

* **broad** — `token|cookie|op://|session|bearer|authorization|api_key|secret|password|credential` + 8 chars.
  Hits: 3, all benign English/identifier usage of the word *token* — `MIN_TOKENS` / "token floor":
  * `corpus/evidence/round89/claims.md:117` — "``MIN_TOKENS = 7`` is a measured floor, not a content check: a ≥7-token verbatim substitution…"
  * `.ufo/waves/round-89/claims.json:101` — same sentence, machine form
  * `plans/round-89.md:14` — "the ≥7-token verbatim substitution … **named limits**"
* **tight** — `op://`, `ghp_…`, `glpat-…`, `xox[baprs]-`, `AKIA…`, `Bearer <token>`, `cookie=`, `Cookie:`,
  `set-cookie`, `authorization=`, `Authorization:`, `password=`, `passwd=`, `secret=`, `api_key=`, `SESSIONID`,
  `JSESSIONID`, `PHPSESSID`, `-----BEGIN … PRIVATE KEY`. **0 hits.**
* **entropy/session** — `PI_SESSION_ID`, session ids, 40+ char base64 runs, 48+ char hex runs. Hits are the
  15-line `c1-positives.tsv` fixture (captured `GATE-RECORD` lines carrying truncated `capture_sha256=…` digests) and
  the 10 sha256 lines of `instrument-pins.txt` — corpus digests and pins, not secrets.

The same tight set over **every other seat's** round-89 wave output (`.ufo/waves/round-89/**`) also returns 0 hits.
No value was printed anywhere in this report; only path:line shapes.

Receipt: `receipts/c-credential-shape-scan.txt`.

---

## (d) Scope — **FIRES (2 low findings)**

### What is clean

* `git -C $L show --stat ac0a0892` — 25 files, all lane-internal: `corpus/evidence/round89/**` (23),
  `corpus/SOURCES.md`, `plans/round-89.md`, `.ufo/waves/round-89/{claims.json,census-start.txt}`.
  **No path outside the lane**, no sibling-repo path, no path under the fleet root's `scripts/`, `considerthese/`,
  `.ufo/state/` or `MANIFEST.json` (those are all clean at the fleet root).
* The registry change is exactly the two `used-by` cells and nothing else:
  `git show ac0a0892 -- corpus/SOURCES.md` → S216 and S218 last-cell edits only;
  `corpus/SOURCES.md | 4 ++--` (2 insertions, 2 deletions); `git status --porcelain corpus/SOURCES.md` → 0 lines.
* The subject tool is unchanged: blob `dc7a4176…` at `f8fa55ec`, `ac0a0892` and `master`; working tree clean;
  sha256 `905f9da2…` matching the pin.
* The freeze's parent is the base: `git rev-parse ac0a0892^` == `f8fa55ec`.
* All ten `instrument-pins.txt` entries verify: `sha256sum -c corpus/evidence/round89/instrument-pins.txt` → 10 × `OK`.
* Fleet root: `git -C /home/vgpnk/Projects/shokunin status --porcelain` → three modified (`.scratch/goal-20261103-hyaku-run15.md`,
  `.scratch/run15-state.json`, `.ufo/l0-questions.md`) and two untracked (`.scratch/closure-tabi-r83-entry.json`,
  `.scratch/run15-wrapup/misroot-cff0b4cb/`). None is chousa-lane output: the lane directory is gitignored at the fleet
  root (`.gitignore:1` = `*-shokunin/`), `git ls-files chousa-shokunin` → 0 files, the `run15-state.json` diff only
  relabels the lane (`"label": "ChousaR81"` → `"ChousaR89"`, the dispatcher's own field), and the `l0-questions.md`
  additions are tsukuroi round-92 lines. **No chousa-lane stray at the fleet root.**

Receipt: `receipts/d-scope-freeze-commit.txt`, `receipts/d-fleet-root-stray.txt`.

### D1 — low — the frozen receipts directory is no longer a closed set in the working tree

`corpus/evidence/round89/controls/receipts/` holds the 8 committed control receipts **plus two untracked files** that
were written after the freeze and have **no `expected.tsv` row**:

* `gate-records-round89.txt` (mtime `2026-11-08T05:53:05`), content
  `GATE_RECORD corpus/lessons/round-89.md:17 S216 OK` / `…:19 S218 OK` / `GATE_RECORDS files=1 records=2 ok=2 fail=0`
* `registry-cells.txt` (mtime `2026-11-08T05:54:39`), content: the S218 last-cell dump base→freeze and
  `corpus/SOURCES.md | 4 ++--`

Neither is in the freeze commit (`git show --name-only ac0a0892 | grep -c 'gate-records-round89\|registry-cells'` → 0).
They are referenced from the *uncommitted* `plans/round-89.md:86` and from the untracked `corpus/lessons/round-89.md:32`.

**Why it matters.** This is exactly the round-88 **F7b** shape — "a receipt filed beside an expectation table that has
no row for it" — reappearing inside the very directory this round's driver is meant to police. The driver iterates
`expected.tsv` and never enumerates the receipts directory, so such a file is invisible to it; I verified this
directly: dropping a synthetic `zz-orphan.txt` into the scratch tree's receipts directory produced **no** mention and
still `CONTROL_RECEIPTS=PASS`.

**Exploit path.** Because the driver overwrites receipts in place (B1), any file in this directory that a later round
reads as evidence has no guarantee of being either checked or regenerated.

**Impact.** Low. The directory's committed contents are exactly the 8 rows; the two strays are uncommitted working-tree
artifacts of the post-freeze integration, and one of them (`registry-cells.txt`) is evidence for a *committed* fact
(the two-cell registry diff) that I independently verified as correct. The risk is directional: the round that
introduced a receipt-discipline repair has, in the same working tree, grown receipts the discipline cannot see.

**Smallest remediation.** Either give both files `expected.tsv` rows (they are receipts of real, checkable commands —
the `registry-cells.txt` one should be a check that the registry diff is exactly two `used-by` cells), or move them out
of `controls/receipts/` into the wave-output folder where non-control receipts belong.

### D2 — low — four tracked lane files are modified in the working tree, uncommitted, alongside the freeze

`git status --porcelain` in the lane: ` M LOG.md`, ` M SCORECARD.md`, ` M corpus/QUALITY.md`, ` M plans/round-89.md`,
plus untracked `corpus/lessons/round-89.md` and the two receipts above. None of the frozen instrument bytes is touched
(`git diff --name-only` lists only those four; `instrument-pins.txt` still verifies 10/10). These are the L1's
post-freeze integration edits — the expected shape of an in-flight round — and they are correctly **not** part of the
freeze commit. I record the state, not a defect: at the moment of review the freeze is the only commit, and the
landing work is uncommitted.

**Impact.** Low. Flagged because a reviewer diffing the lane against `ac0a0892` will see these four modified files and
the two strays; the frozen bytes themselves are clean.

---

## (e) Attribution — **HELD**

```sh
git -C $L show -s --format='author=%an <%ae>%ncommitter=%cn <%ce>%nauthor_date=%aI%ncommitter_date=%cI' ac0a0892
# author=chousa-shokunin <chousa@shokunin.local>     exit=0
# committer=chousa-shokunin <chousa@shokunin.local>  exit=0
# author_date=2026-11-08T05:30:44-03:00
# committer_date=2026-11-08T05:45:24-03:00
```

Author **and** committer are both `chousa-shokunin <chousa@shokunin.local>`, exactly as required. The signed
`Author:`/`Committer:` lines in the commit object agree with the format output — no other identity anywhere in the
commit. Receipt: `receipts/e-attribution.txt`.

**Observation (info, not a finding).** The commit's *author* date `2026-11-08T05:30:44-03:00` is byte-identical to the
**base commit's committer date** (`f8fa55ec`, same timestamp) while its committer date is 14m40s later — the usual
signature of an inherited/carried author date (jj or an explicit `GIT_AUTHOR_DATE`), not of when the content was
written. The identity is correct; only the author timestamp is inherited. Worth a scribe note, since "the freeze was
made at 05:30:44" would be the wrong reading — the content's own file mtimes run `05:38`–`05:45`, and the receipts
were written `05:45:09`–`05:45:19`, i.e. **after** that timestamp. The committer date (`05:45:24`) is the one that
matches the artefacts, and it is the bound I used in (a).

---

## Consolidated evidence

`receipts/z-consolidated-evidence.txt` — every bound with its exit code in one place:

```
BOUND rows_older_than_freeze=184        exit=0
BOUND rows_at_or_after_freeze=0         exit=0
BOUND max_fetched_utc S216 2026-11-08T06:50:40Z   exit=0
BOUND count_newer_than_freeze=0         exit=0
BOUND capture_worktree_diff_lines=0     exit=0
driver_exit=0  /  CONTROL_RECEIPTS=PASS
author=chousa-shokunin <chousa@shokunin.local> committer=chousa-shokunin <chousa@shokunin.local>   exit=0
```

---

## What this seat did not do

No production edits, no lane or fleet git/jj mutation, no commits or pushes, no dispatch, no network, no `sudo`, no
sysctl, no service restart. Every probe ran against a scratch copy of the frozen tree or a throwaway fixture whose
`git rev-parse --show-toplevel` was asserted before use; the live lane was read-only throughout, and
`git status --porcelain` in the lane is byte-identical before and after this review (the four modified files and the
two stray receipts in D1/D2 were written by other seats, not by this one). The scratch tree
`/fast/scratch/hyaku/chousa-r89/R89SentinelScope` was deleted after the receipts were copied into
`.ufo/waves/round-89/w1/R89SentinelScope/receipts/`.

---

VERDICT: R89SentinelScope C1 fired — the committed control battery cannot police itself (the driver overwrites each receipt before grepping it, so a committed receipt contradicting `expected.tsv` is silently erased; the harm control returns PASS with `records=0` when the subject tool cannot run at all; and the `c1-harm` receipt does not reproduce against the frozen revision), so C1's K3 harm assurance rests on a control that can neither fire nor report that it measured nothing.
VERDICT: R89SentinelScope C2 fired — C2's frozen sentence names the observable `VERDICT fields_hold=1` and "nine legs", but `curation-r89.py` prints no `VERDICT` token on the passing path (only `LEGS_MEASURED=8/8` for a 9-leg counter) and the `c2-landing` expectation row requires neither, so the committed battery cannot distinguish the field-derived verdict from the round-88 `all(ok)` verdict it replaced.
