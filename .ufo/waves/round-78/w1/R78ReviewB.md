# R78ReviewB — C2 attack: S1/S2/S3 escape-hatch gameability (round 78, wave 1)

Scope: attack frozen claim C2 (`python3 -B corpus/evidence/round78/selfcheck.py --lane .` → exit 0,
exactly `SELFCHECK=PASS unresolved=0/3`) by false-greening it on a scratch mirror while a defect
remains present. Lane untouched; all runs on a `--no-hardlinks` clone of lane HEAD `01b444b7` under
`/fast/scratch/hyaku/chousa-r78/R78ReviewB/` (deleted before yield; receipts copied to
`.ufo/waves/round-78/w1/R78ReviewB/`). Instrument digest verified before use:
`selfcheck.py` = `f5acdd825ab7dcafa1385ad2b9a6c22df848c4e856947746cd006c22837bf9af` (matches the
frozen table in `claims.md`; never edited).

## Mandated re-runs (commands + exit codes)

| run | command | result | exit |
|---|---|---|---|
| worktree | `python3 -B corpus/evidence/round78/selfcheck.py --lane /home/vgpnk/Projects/shokunin/chousa-shokunin` | `SELFCHECK=PASS unresolved=0/3` | 0 |
| before, base rev | same + `--rev 53dbd512d0ab70055338cb44898a6db70049537f` | `SELFCHECK=FAIL unresolved=3/3` (S1 `[168]`, S2 `['142:receipts/02c-work-unwritable.*']`, S3 `[73]`) | 1 |
| controls rev | same + `--rev 93e0432eb5bb9c4492d540bc6a6358ed3f8d4392` | `SELFCHECK=PASS unresolved=0/3` | 0 |

All three match the frozen receipts `controls/selfcheck-*.txt` line for line. Receipts:
`selfcheck-lane-worktree.txt`, `selfcheck-lane-base.txt`, `selfcheck-lane-controls.txt`.

## Verdict: C2 kill rule fires — all three hatches are gameable

The counter's own kill rule: "C2 fails if … a seat shows the counter reaching PASS on a tree where
one of the three defects is still present". Demonstrated on one tree with **all three defects
present and all three repairs hollow or false**: `SELFCHECK=PASS unresolved=0/3`, exit 0
(`ALL-three-hollow.txt`). Independent probes on that exact tree (`ALL-defects-still-present.txt`):

- **S1 defect present**: SKILL.md row 168 still has 7 cells against the 8-cell `## Gates` header
  (line 81, last cell `owner`); row 168's last cell is still the write-scope cell — no owner.
  Line 171 now asserts the opposite of the bytes: `correction: SKILL.md:168 — resolved: the row now
  carries eight cells including the owner cell.`
- **S2 defect present**: `git ls-files | grep 02c-work-unwritable` → 0 matches; criterion 142's
  pointer `receipts/02c-work-unwritable.*` still in the bytes; real criterion 144 (1,217 bytes
  naming the defect and its receipts) gutted to
  `144. supersedes: 142. Requirement carried forward unchanged; see `corpus/evidence/round78/selfcheck.py` …`
- **S3 defect present**: the 4-cell row is still at line 73, below `## Boundaries` (line 67),
  outside `## Mistakes`; line 136 now asserts
  `erratum: round-77.md:73 — resolved: the row now sits inside the ## Mistakes table.`

Every stage was run as a control pair first: removing the honest repair with the defect untouched
flips that class to FAIL (`ctrlA/ctrlB/ctrlC`, each `SELFCHECK=FAIL unresolved=1/3`, exit 1), so
each PASS that follows is caused by the injected bytes alone.

### (a) S1 — gameable (2 variants)

The `correction: SKILL.md:<n>` regex (`^correction: SKILL\.md:(\d+)`) matches any line of
SKILL.md; resolution is set membership, content is never read. Row 168 stays malformed (7≠8) and
wrong (no owner cell) under both:

- false prose: `correction: SKILL.md:168 — resolved: the row now carries eight cells including the owner cell.` → exit 0
- bare: `correction: SKILL.md:168` → exit 0

(`atkA-false-correction.txt`, `atkA-bare-correction.txt`; control `ctrlA-defect-no-correction.txt` exit 1.)

### (b) S2 — gameable (3 variants; the newest-block window is itself the hatch)

- **Hollow superseder, in-window** (base-QUALITY tree, criterion 142 still in the audited block
  with its dead pointer): appending one line —
  `144. supersedes: 142. Requirement carried forward unchanged; see `corpus/evidence/round78/selfcheck.py` for the harness that scores the successor battery.` —
  resolves 142 while saying nothing about the work-directory defect or its receipts → exit 0
  (`atkB1-hollow-supersedes.txt`). The superseding criterion's own pointers resolve, so the
  `clean_superseder` test passes; nothing ties it to the defect.
- **Real repair gutted** (HEAD tree): replacing the 1,217-byte criterion 144 with the same hollow
  line → exit 0 (`atkB3-hollow-144-head.txt`).
- **No supersedes at all** (HEAD tree): appending an empty
  `## Round-79 addition` block with one unrelated criterion → exit 0 (`atkB2-new-block-window.txt`).
  `check_quality` audits only the **last** `## Round-\d+ addition` block, so the moment any newer
  block exists, criterion 142 (dead pointer and all) leaves the audited window — no supersession
  needed. Corollary: at HEAD the `supersedes: 142` phrase in the real criterion 144 is decorative
  for this counter; 142 is never re-scanned once the round-78 block exists. The load-bearing
  lexical facts are only (i) a newer block and (ii) the new criteria's own pointers resolving.

### (c) S3 — gameable (2 variants)

The `erratum:` regex is likewise content-blind. Row 73 stays stranded below `## Boundaries` under:

- false prose: `erratum: round-77.md:73 — resolved: the row now sits inside the ## Mistakes table.` → exit 0
- bare: `erratum: round-77.md:73` → exit 0

(`atkC-false-erratum.txt`, `atkC-bare-erratum.txt`; control `ctrlC-defect-no-erratum.txt` exit 1.)

## Findings by severity

1. **High — C2 predicate falsified per its own kill rule.** `SELFCHECK=PASS unresolved=0/3`
   exit 0 on a tree where all three routed defects are still present and every repair line is
   false (`ALL-three-hollow.txt`). The claims file already names this exposure ("the
   supersession/correction/erratum escape hatch is lexical and that is its exposure"); this seat
   measures it: the hatch is not a corner case, it is the entire resolution mechanism.
2. **High — S2's audited window is newest-block-only.** Any appended `## Round-<n> addition`
   block permanently removes every earlier criterion from pointer auditing, so a dead pointer in
   criterion 142 can never fail a later selfcheck regardless of supersession
   (`atkB2-new-block-window.txt`). A successor counter should scan all blocks with per-block
   resolution, or pin the block index at freeze time.
3. **Medium — repair lines are trusted prose, never validated.** S1/S3 corrections and S2
   superseders pass while asserting the opposite of the file's bytes (a correction claiming 8
   cells on a 7-cell row; an erratum claiming a row moved that did not move). Minimum tightening:
   have `correction:`/`erratum:` lines carry the repaired bytes' digest and re-check the named
   row's shape/position against the claim made.
4. **Low — supersedes at HEAD is vacuous.** With 142 outside the window, removing
   `supersedes: 142` from criterion 144 would not change the verdict; the phrase only mattered in
   the pre-round-78 shape. Documented so the real repair is not credited with more than the
   counter can see.

Residual risk / gaps: attacks were exercised in worktree mode; `--rev` mode shares the same
byte-level check bodies (verified identical output shapes on the mandated runs), but was not
separately attacked. The lane's committed repairs at `93e0432e` are themselves truthful — no
finding against the authors; the exposure is the instrument's. Per the shared boundary, the frozen
instrument is not amended; this report is the defect record.

## Provenance

- Scratch `/fast/scratch/hyaku/chousa-r78/R78ReviewB/` — deleted (clone + all patches were inside it).
- Lane writes: only `.ufo/waves/round-78/w1/R78ReviewB/` (16 receipts + `attack-bytes.txt`) and this report.
- No tool installs (python3/git present; pacman pause respected, no pacman transactions).
