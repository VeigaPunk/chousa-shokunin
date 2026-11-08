# R93ReviewerC3 — C3 (`C3-TALLY-R93`, freshness) adversarial review

Lane: `chousa`, round 93, L1 `ChousaR93`. Seat: `R93ReviewerC3` (leaf; no subagents, no production edits).
Base `206226dc9d9baef620e7d3d30bdac5f9194a459f`; freeze F2 `b7241252c2358613d3b22b7d0454d98c56dab373`;
carrier C2 `754b62fb6adc60e44e12375af5461a0ebe302994` (checked out; lane repo HEAD during the review).
Scratch `/fast/scratch/hyaku/chousa-r93/R93ReviewerC3` (`repo` = `git clone --shared` at C2; every fixture under
`evidence-work/`, `probe*`, `case-extra*`); deleted before yield. No network, no sudo, no pacman, no installs;
`python3 -B` stdlib only, `TMPDIR` inside the scratch dir. No lane/agent/git mutation; the only lane files written
are this report and the receipts under `.ufo/waves/round-93/w1/`.

Raw evidence written this seat (all under `.ufo/waves/round-93/w1/`):

| receipt | content |
|---|---|
| `R93ReviewerC3-c3-tally-at-C2.txt` | the frozen tally command at C2, exit code |
| `R93ReviewerC3-c3-controls-at-C2.txt` | the frozen controls command at C2, exit code |
| `R93ReviewerC3-c3-probes.txt` | grounding, scope/tail, case-range, freeze-artifact probes (177 lines) |
| `R93ReviewerC3-c3-scope-extra.txt` | unterminated scope + non-ATX truncation probes |
| `R93ReviewerC3-c3-case-extra.txt` | `MISLABELED=1` + green verdict probe |
| `R93ReviewerC3-c3-grounding-extra.txt` | both grounding receipts deleted (`HIST_DERIVED=0/2`) |
| `R93ReviewerC3-cited-selftest-r93.txt` | copy of the committed 283-case selftest receipt |
| `R93ReviewerC3-cited-instrument-pins.txt` | copy of the committed 22-row pins table |
| `R93ReviewerC3-cited-round25-final-measure.log` | copy of the 161 grounding receipt |
| `R93ReviewerC3-cited-round34-audit-dispositions.md` | copy of the 256 grounding receipt |
| `R93ReviewerC3-cited-round-93-lesson.md` | copy of the untracked `corpus/lessons/round-93.md` (F5/F6) |

## 0. Landing bytes and canonical runtime

```
# command: git -C <clone> rev-parse HEAD
754b62fb6adc60e44e12375af5461a0ebe302994                       # exit 0
sha256 e3ad820471aaf274457fa67cc897b2a555893434cca04949426fca03e8854989  corpus/evidence/round93/skill-tally-r93.py
sha256 340541e65cfe39ad8babc0b96e14a4a22df3685bd00f4bcf39878f85be41953e  corpus/evidence/round93/skill-tally-r93-controls.py
sha256 9c29428160768524c77407eedd711200be53a1074e2a22fe9bab814ad3f5bb37  corpus/evidence/round93/controls/selftest-r93.txt
```

`corpus/evidence/round93/instrument-pins.txt` rows 5, 6 and 8 carry exactly those three digests, and rows 9/10 carry
the `claims.md`/`claims.json` digests (`bc2bc360…`, `db82f98c…`) that match the working tree: the bytes reviewed are the
frozen bytes. `git diff --stat F2 C2 -- skill-tally-r93.py skill-tally-r93-controls.py` is empty (instruments unchanged
between freeze and carrier); `git diff --stat base C2 -- tools/research-gate.sh tools/gate-records.py SKILL.md` is empty
(the gate tools and `SKILL.md` are untouched this round, as the assignment states); `git diff --stat F2 C2 --
.ufo/waves/round-93/` is empty (claims not re-frozen after F2). `/fast/scratch/.../repo` `git status --porcelain` was
empty when checked after the probe batch and after the controls run (the instruments write nothing and the controls
wrote only under `--work`).

No `lsp` device is mounted in this session (the tool inventory carries none), so the role's LSP status/references/
diagnostics step is recorded as unavailable rather than skipped silently; in its place both C3 instruments were read in
full (`skill-tally-r93.py` 217 lines, `skill-tally-r93-controls.py` 129 lines) and every cited definition/consumer is a
line of those files, so no grep sampling stands in for a definition lookup.

## 1. The frozen predicate at C2 — both commands

```
# command: python3 -B corpus/evidence/round93/skill-tally-r93.py --root . \
#            --selftest corpus/evidence/round93/controls/selftest-r93.txt
# (the summary is one output line, wrapped here for display)
TALLY_ROWS=8 STALE_TALLIES=0/8 EXPECTED_CASES=283 EXPECTED_SKIPPED=0 OTHER_OCCURRENCES=2 CASE_RANGE_BASHENV=273-275
CASE_RANGE_BASH_PIN=282-283 CASE_RANGE_OK=2/2 MISLABELED=0 HIST_DERIVED=2/2 HIST_PRESENT=2/2 TAIL_TALLIES=2
OTHERS_OK=1 TAIL_OK=1 LEGS=4/4
SKILL_TALLY_R93=PASS                                            # exit 0
```

```
# command: python3 -B corpus/evidence/round93/skill-tally-r93-controls.py --root . --work <scratch>/controls-work
CONTROLS=PASS OLDPROSE_REFUSED=1/1 PRIOR_ACCEPTED=1/1 STALE_REFUSED_BOTH=1/1 HIST_REFUSED_BOTH=1/1
TAIL_REFUSED=2/2 TAIL_PRIOR_ACCEPTED=1/1 TAIL_ADDED_REFUSED=1/1 HIST_UNGROUNDED_REFUSED=1/1
                                                                # exit 0
```

Every field the assignment and `claims.md:141-145` require is present verbatim; the r92 prior counter on the same
tree prints `SKILL_TALLY_R92=PASS` `LEGS=3/3` (its three-leg baseline), consistent with the claim's "Before".

## 2. The six asked questions

### (1) Are the two grounding quotes really at the named receipts/lines, and does the counter require the quote?

**HOLDS at the named lines.** `grep -n` (`probes.txt` §1):

```
corpus/evidence/round25-final-measure.log:53: RESEARCH_GATE_SELFTEST: PASS (161 cases, 0 skipped)
corpus/evidence/round34/audit-dispositions.md:5: skill-tally-256 | fixed at integration (SKILL.md rows 77-84 and :92
  cite the gate exact banner form PASS (256 cases, 0 skipped); found by wave seat ScoutSkillTally)
```

Exactly the line numbers named at `claims.md:126-127`; one occurrence each. The counter requires the **quote**, not the
file: `skill-tally-r93.py:130` is `if quote not in open(path).read()`. Blanking the 161 verdict line (file still
present) prints `HIST_FINDING HIST_UNGROUNDED 161 quote='PASS (161 cases, 0 skipped)' …`, `HIST_DERIVED=1/2`,
`SKILL_TALLY_R93=FAIL`, exit 1. Deleting the receipt and pointing it at a broken symlink behave the same
(`probes.txt` §1: three runs, exit 1 each).

But the counter does **not** bind the line: prepending 20 lines to the 161 receipt (quote now at line 73) still prints
`HIST_DERIVED=2/2 … SKILL_TALLY_R93=PASS`, exit 0 (`probes.txt` §1, `G-quote-relocated-20-lines`). The "at line 53/5"
detail is descriptive in `claims.md`, not enforced; it is true at C2.

### (2) Can `HIST_DERIVED` be 2/2 while a grounding receipt is absent?

**HOLDS against absence; a symlink substitution passes.** The path is `os.path.join(root, receipt)` with fixed
relative literals (`skill-tally-r93.py:126`), so there is no absolute-path or `..` escape; `--root` is an argument by
design (the controls build copy trees with it, `skill-tally-r93-controls.py:73-84`). Deleted receipt → `HIST_UNGROUNDED`,
`HIST_DERIVED=1/2`, exit 1; both deleted → `HIST_DERIVED=0/2`, exit 1 (`c3-grounding-extra.txt`);
symlink to a nonexistent target → `1/2`
(`probes.txt` §1). A symlink to an existing file *outside* the root that carries the quote passes:
`HIST_DERIVED=2/2 … SKILL_TALLY_R93=PASS`, exit 0 (`G-receipt-symlink-outside`). `os.path.isfile` follows links and
the check is substring content; that sits inside named limit (1) ("a rewritten receipt is caught by the quote test,
not by a digest") but a path substitution is not a rewrite — see residual R2.

### (3) Does `HIST_PRESENT` require the tally inside the Gates scope, and is `declared` derived?

**HOLDS.** `other_counts` is built only from `gates_text` (`skill-tally-r93.py:118-121`), and `hist_present` counts
those (`:134`); moving the in-scope `161` tally below the scope prints `HIST_PRESENT=1/2` and
`HIST_FINDING HIST_MISSING PASS (161 cases, 0 skipped)` (`probes.txt` §2, `S4`). `declared` is a dict comprehension
over `HIST_SOURCES` (`:122`), so the OTHERS leg compares against the same list that grounds the receipts — not a
separate frozen `EXPECTED_OTHERS` as in r92 (`round92/skill-tally-r92.py:108`). Nuance, not a defect: the `("161","0")`
/ `("256","0")` pairs are literals *inside* `HIST_SOURCES`; what is derived from the receipt is the verbatim evidence
string. This satisfies K4's four vacuity tests (receipt opened, quote required, presence required, tail by
`(cases, skipped)` pairs).

### (4) Does the tail scan start exactly at the scope end (off-by-one / duplicate-line blindness)?

**HOLDS.** `gates_end = gates_start + 1 + m_end.start()`, where the match is the `\n` before the next depth-≤2 heading
(`skill-tally-r93.py:86-89`); with C2's `SKILL.md` that is char 176266, i.e. the newline ending line 575, and the
boundary heading `## Round26 metadata options and resource qualification` is line 576. `gates_text` excludes that
newline; `text[gates_end:]` starts with it (first `splitlines()` element empty), so no line is lost or counted twice.
Probes (`probes.txt` §2), all with a synthetic `` `PASS (999 cases, 0 skipped)` ``:

* last in-scope line (`ZLAST`, inserted at gates_end): `OTHER_OCCURRENCES=3`, `TAIL_TALLIES=2`, `LEG_FAIL OTHERS`, exit 1
  — classified in-scope, and not double-counted in the tail;
* tally inside the boundary heading line: `HIST_SCOPE_BLEED line=999`, `TAIL_TALLIES=3`, `TAIL_OK=0`, exit 1;
* first body line after the boundary heading: same `HIST_SCOPE_BLEED`, `TAIL_OK=0`, exit 1.

Unterminated scope (truncate at the boundary newline) prints `SKILL_TALLY_R93=SETUP SCOPE_BLEED no next-## or #-level
heading after ## Gates`, exit 2 (`c3-scope-extra.txt`), so named limit (3)'s "terminates an unterminated scope" holds.

### (5) Would a tally moved from inside the scope to outside it be refused? Is `TAIL_DECLARED` a loophole?

**HOLDS; refused twice.** Rename/move the in-scope `161` tally below the scope: `HIST_SCOPE_BLEED line=161`,
`HIST_FINDING HIST_MISSING PASS (161 cases, 0 skipped)`, `HIST_PRESENT=1/2`, `OTHERS_OK=0`, `TAIL_OK=0`, `LEGS=2/4`,
exit 1 (`probes.txt` §2, `S4`). Even if the instrument's `TAIL_DECLARED` is patched to include `("161","0")` — the
strongest joint edit of the tail set — the OTHERS leg still fails (`LEG_FAIL OTHERS … codes=HIST_MISSING …`, `LEGS=3/4`,
`SKILL_TALLY_R93=FAIL`, exit 1; `S5`). `TAIL_DECLARED` is not a loophole for an in-scope historical tally.

### (6) Does case-range still bind at the landing bytes, and does the enumeration pin hold at 283?

**HOLDS at the landing bytes.** `CASE_RANGE_BASHENV=273-275`, `CASE_RANGE_BASH_PIN=282-283`, `CASE_RANGE_OK=2/2`,
`MISLABELED=0`; `EXPECTED_CASES=283` with 283 `^ok-case ` lines and 283 distinct numbers in the committed selftest
receipt (last line 285 is `RESEARCH_GATE_SELFTEST: PASS (283 cases, 0 skipped)`). Removing one `ok-case 283` line fires
`SKILL_TALLY_R93=FAIL case enumeration 282 lines, 282 distinct numbers, against verdict 283 cases`, exit 1
(`probes.txt` §3, `R5`). Renaming an endpoint (`273`) fires `CASE_RANGE_FINDING RANGE_MISMATCH:bashenv claimed=273-275
derived=274-275`, exit 1 (`R4`). The leg is nevertheless porous off-landing — see F3.

## 3. Findings by severity

### F1 — MEDIUM (freeze artifact): the machine-form C3 predicate can never be satisfied

`claims.json` is pinned at `db82f98cb7b7b089c7a569cf7ebc77540484c84c9eb399998e108bc9faf9f894` (`instrument-pins.txt`
row 10; `claims.md` at `bc2bc360…`, row 9) and freezes:

```
.ufo/waves/round-93/claims.json:97  … prints CONTROLS=PASS … TAIL_REFUSED=1/1 TAIL_PRIOR_ACCEPTED=1/1.
.ufo/waves/round-93/claims.json:108    "TAIL_REFUSED=1/1",
```

while the instrument prints `TAIL_REFUSED=2/2` (`skill-tally-r93-controls.py:121` is
`f"TAIL_REFUSED={…}/2"`; observed output above) and `claims.md:143` says `TAIL_REFUSED=2/2`. The literal
`TAIL_REFUSED=1/1` appears nowhere in the output of any run. A mechanical verifier that reads the machine form
would judge K1 unmet on a tree whose substance is green; conversely the prose and the instrument agree. Command:

```
$ grep -n 'TAIL_REFUSED=' .ufo/waves/round-93/claims.json .ufo/waves/round-93/claims.md \
      corpus/evidence/round93/skill-tally-r93-controls.py
claims.json:97  … TAIL_REFUSED=1/1 …        claims.json:108  "TAIL_REFUSED=1/1",
claims.md:143   … TAIL_REFUSED=2/2 …        skill-tally-r93-controls.py:121  …/2 "
                                                                # exit 0
```

(`probes.txt` §4.) Fix: regenerate `claims.json`'s C3 `sentence`/`predicate.controls` from the frozen prose and
re-pin row 10; until then C3's machine form and prose disagree. This is a freeze-coherence defect, not a behaviour
defect — the claims.md predicate (the authoritative one per the assignment) holds.

### F2 — MEDIUM (false accept): tallies *above* `## Gates` are invisible, contrary to the claim's wording

`claims.md:129-131` says "Tally occurrences outside the Gates scope are enumerated against a declared tail set …
an undeclared tail tally fires `HIST_SCOPE_BLEED`". The code only scans `text[gates_end:]`
(`skill-tally-r93.py:147`); nothing before `gates_start` (`:82`) is ever looked at. Insert
`` `PASS (777 cases, 0 skipped)` `` before `## Gates`:

```
# command: python3 -B …/skill-tally-r93.py --root <S6-declare-777-above-Gates> --selftest …/selftest-r93.txt
TALLY_ROWS=8 STALE_TALLIES=0/8 EXPECTED_CASES=283 EXPECTED_SKIPPED=0 OTHER_OCCURRENCES=2 CASE_RANGE_BASHENV=273-275
CASE_RANGE_BASH_PIN=282-283 CASE_RANGE_OK=2/2 MISLABELED=0 HIST_DERIVED=2/2 HIST_PRESENT=2/2 TAIL_TALLIES=2
OTHERS_OK=1 TAIL_OK=1 LEGS=4/4
SKILL_TALLY_R93=PASS                                            # exit 0
```

(`probes.txt` §2, `S6`: that is the unchanged green line — the 777 tally is simply not seen. A second head insertion
at the `## Error patterns` boundary is identical.) So the r92 defect class ("a tally outside the `## Gates` scope is
invisible") is closed for the **tail only**; a tally planted above the section — in the Decision table, Checklist, or
Boundaries — is still silently accepted. The sentence "Tally occurrences outside the Gates scope are enumerated" is
therefore true only of the tail; the tail-specific kill behaviour in K4 is intact. Fix: scan `text[:gates_start]`
against a declared head set (or require the head to contain zero tallies), or narrow the claim to the tail.

### F3 — MEDIUM (green verdict while printing a finding): case-range family is endpoint-only and `MISLABELED` does not bind

The family is derived from `names` (`skill-tally-r93.py:66`), which uses `CASE_RE` requiring `exit=` (`:36`), while the
enumeration pin uses *all* `ok-case` lines (`:69`). Three demonstrable holes (`probes.txt` §3, `c3-case-extra.txt`):

1. **Interior hole in the bashenv range.** Rename case `274 drift-bashenv-echo` → `drift-other-echo` (endpoints
   273/275 preserved): `CASE_RANGE_BASHENV=273-275 … CASE_RANGE_OK=2/2 MISLABELED=0 LEGS=4/4`,
   `SKILL_TALLY_R93=PASS`, exit 0. `derived_env` is `(min, max)` only (`:176`) and `MISLABELED` is computed only for
   the override range (`:186`), so a hole inside the bashenv range is invisible.
2. **No-exit case names are outside the family population.** The six `accepted=` case lines (196-200, 223) never match
   `CASE_RE`. Renaming case 223 to `pin-bashenv-evil` (count and distinct numbers unchanged) leaves
   `CASE_RANGE_OK=2/2 MISLABELED=0`, `SKILL_TALLY_R93=PASS`, exit 0.
3. **`MISLABELED` is printed but not part of the verdict.** Fixture: prose claims `bash-pin-override cases 281-283`,
   family is `{281,283}` (case 282 renamed out). Observed: `CASE_RANGE_FINDING MISLABELED=1 indices=282`,
   `CASE_RANGE_OK=2/2 MISLABELED=1 LEGS=4/4`, `SKILL_TALLY_R93=PASS`, **exit 0** — `ok_ranges`/`passed` (`:187`,
   `:203`) ignore `mislabeled` and only the endpoint comparisons bind.

Mitigation: the selftest receipt is pinned (`instrument-pins.txt` row 8), so these false accepts require a coherent
edit of a committed, pinned receipt; the enumeration pin (283 lines / 283 distinct numbers) still binds. At the landing
bytes all three are green for the right reasons. Fix: derive each family as a set and compare the claimed range
element-wise (and include `mislabeled` in `ok_ranges`).

### F4 — LOW (evidence provenance): the C3 "Before" receipt is not in the carrier

`claims.md:119-120` cites `corpus/evidence/round93/evidence-before/c3-prior-accepts.txt` for "deleting the `215` tail
line leaves `SKILL_TALLY_R92=PASS` (rc 0)". At C2:

```
$ git -C <clone> ls-tree --name-only 754b62fb corpus/evidence/round93/
corpus/evidence/round93/control-driver-r93.py
corpus/evidence/round93/controls
corpus/evidence/round93/curation-controls-r93.py
corpus/evidence/round93/curation-r93.py
corpus/evidence/round93/forgeries-r93.py
corpus/evidence/round93/instrument-pins.txt
corpus/evidence/round93/skill-tally-r93-controls.py
corpus/evidence/round93/skill-tally-r93.py
                                                                # exit 0 — no evidence-before/ entry
$ ls corpus/evidence/round93/evidence-before/ ; git status --porcelain corpus/evidence/round93/evidence-before/
c2-prior-accepts.txt  c3-prior-accepts.txt
?? corpus/evidence/round93/evidence-before/                     # exit 0
```

The file exists only as an untracked lane file (same for `c1-prior-accepts.txt` and the `after/` and `census-*.txt`
files), so a reader of C2 cannot verify the citation. Its content also measures a *changed* tail tally (214) and an
*added* tail tally (199), not the "deleting the `215` tail line" run the prose cites. I reproduced the deletion
independently: deleting line 640 gives r92 `SKILL_TALLY_R92=PASS` exit 0 and r93 `TAIL_TALLIES=1 TAIL_OK=0` exit 1
(`probes.txt` §2, `S7`), so the substance is true; the citation is not carried. (Cross-claim: C1/C2 cite their own
untracked `evidence-before/` receipts.)

### F5 — LOW (frozen doc vs carrier): the `S001` recheck sentence is unfulfilled

`claims.md:171-175` (Frontier step): "`S001` (the own-work chain row; its `recheck` cell moves round 92 → round 93,
logged old→new in the round-93 lesson)". `corpus/SOURCES.md` is byte-identical between base and C2
(`git diff --stat base C2 -- corpus/SOURCES.md` empty); `S001`'s recheck cell reads `on-release` (registry columns
`… | status | opened | recheck | used-by`), and the untracked `corpus/lessons/round-93.md` itself says the sentence was
withdrawn ("the earlier plan sentence … was withdrawn: S001's recheck cell is a cadence (`on-release`), not a round
counter"). The frozen `claims.md` still carries the withdrawn sentence. C3's frozen sentence only lists `S001` as its
source, and the source row is unchanged/accurate; this is a frozen-document inconsistency, not a counter defect.

### F6 — LOW/INFO (carrier naming): the untracked lesson names a different carrier

`corpus/lessons/round-93.md` (untracked) names "carrier C3 `d740760e5e2bdb2355435bd9c2fd132ad825df41` (… the forgery
battery fix)". `d740760e` exists as a commit, is a descendant of C2 (`git merge-base --is-ancestor` true), carries no
ref (`git for-each-ref --contains` empty), and differs from C2 in `forgeries-r93.py` and `instrument-pins.txt`
(`git diff --stat d740760e C2` shows those two files). Per the assignment C2 is the authoritative tree; the uncommitted
lesson must be corrected (or the carrier reconciled) before it is committed, otherwise the wave's own account points at
bytes that are not the scored carrier. It does not touch the two C3 instruments or the selftest receipt.

### F7 — INFO: the 256 grounding quote is a disposition sentence about SKILL.md, not a run capture

`audit-dispositions.md:5` reads "skill-tally-256 | fixed at integration (SKILL.md rows 77-84 and :92 cite the gate
exact banner form PASS (256 cases, 0 skipped); …)". It is the only occurrence and the counter's substring test passes,
but unlike `round25-final-measure.log:53` (an actual `RESEARCH_GATE_SELFTEST:` line) it is a round-34 note *about*
the citation, so it does not independently attest a 256-case run. Named limit (1) disclaims digest binding; the
observed counts still require the string to be present. Residual, not a kill.

### F8 — INFO: no line binding on the grounding quotes

Quote relocated 20 lines down in the 161 receipt → `HIST_DERIVED=2/2 … SKILL_TALLY_R93=PASS` exit 0
(`probes.txt` §1). `claims.md`'s "at line 53/5" is accurate at C2 but unenforced; no kill rule requires it.

### F9 — INFO: symlink substitution of a grounding receipt passes

Receipt path replaced by a symlink to an external file carrying the quote → `HIST_DERIVED=2/2`, `SKILL_TALLY_R93=PASS`,
exit 0 (`probes.txt` §1). Absent and broken-link targets are refused. Named limit (1) covers a rewritten receipt;
it does not name path substitution. Residual R2.

### F10 — INFO: the scope boundary matches any column-0 `#`/`##`, not ATX headings only

`re.search(r"\n#{1,2} ", …)` (`skill-tally-r93.py:86`) does not know about fences. A column-0 `# not a heading`
inserted inside `## Gates` truncates the scope; the result is loud — `HIST_SCOPE_BLEED` for 161 and 256,
`HIST_MISSING` for both, `HIST_PRESENT=0/2`, `LEGS=2/4`, exit 1 (`c3-scope-extra.txt`) — never a silent pass, because
the moved tallies land in the tail set. At C2 the heading scan finds `## Gates` at 82 and the next depth-≤2 heading
`## Round26` at 576; the `# cwd:` comment is line 581, after the boundary — no column-0 `#`/`##` sits between 82 and
576, so named limit (3)'s "ATX boundary" is accurate for the landing bytes only by document layout.

## 4. Residual risk and verification gaps

- **R1 (control coverage).** The controls battery has no case for a head-of-document tally (F2), an interior family
  hole (F3.1), a family name on a no-exit case (F3.2), or a `MISLABELED>0` tree (F3.3); its `deleted-tail` case
  mutates a digit (215→214) rather than deleting the line. The claim's K3/K4 are still met, but the battery does not
  protect the two holes it does not name.
- **R2 (grounding substrate).** HIST grounding is content-substring only: symlink substitution (F9), quote relocation
  (F8) and quote-in-another-context (F7) pass. The two historical receipts are not in `instrument-pins.txt`; only the
  selftest and the six control receipts are pinned.
- **R3 (named-limit accuracy).** `claims.md` says "Tally occurrences outside the Gates scope are enumerated" (F2) and
  "the `## Gates` scope is the r92 ATX boundary" (F10); the first overstates the head, the second is a regex that
  also matches fenced column-0 comments (loud failure, tested).
- **R4 (not exercised).** `--selftest` is read from the caller's CWD, not from `--root`; the frozen counting command
  happens to pass a path under the lane root. Not a defect under the frozen command, but a root/cwd mismatch would
  silently evaluate a different receipt than the tree.
- **No resume path** exists in this claim (`resume_continuity_v1` is n/a for C3).
- Verification gaps: I did not run `tools/research-gate.sh --selftest` itself (network-free but out of seat scope and
  slow); the committed selftest receipt at line 285 is the verdict the counter reads and it matches the 283-case
  enumeration. I did not audit C1/C2 instruments; F1/F4/F6 are cross-claim adjacent notes only.

## 5. Verdict

Kill rules at C2: K1 does not fire on the authoritative predicate (`claims.md:141-145`; both commands exit 0 — the
claims.json form would fire, F1); K2 does not fire (positive accepted, r92 accepts both tail trees while r93 refuses
both, `controls-at-C2`); K3 does not fire (the four tallies hold on the clean tree — `161` at `SKILL.md:188`, `256` at
`:186`, `215` at `:640`, `283` at `:781` — and the eight current `283` rows at `:86-93` are unchanged); K4 does not fire
(receipt opened at `skill-tally-r93.py:127-132`, quote required at `:130`, in-scope presence required at `:134-138`,
tail compared as `(cases, skipped)` pairs at `:145-150`).

VERDICT: R93ReviewerC3 C3 held — the frozen C3 predicate and all eight controls print exactly as claims.md freezes them at C2 (exit 0), with F1 (claims.json's unsatisfiable TAIL_REFUSED=1/1), F2 (head tallies invisible), F3 (case-range endpoint-only plus non-binding MISLABELED) and F4-F6 routed as findings rather than kills.
