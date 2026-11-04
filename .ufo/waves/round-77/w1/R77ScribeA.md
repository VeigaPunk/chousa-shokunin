# R77ScribeA — round-77 Gate and Mistakes drafts

Seat: scribe (leaf). Scope: draft `## Gate` (S190 admit, S191 admit, S192 reject) and `## Mistakes`
(one row) for `corpus/lessons/round-77.md`, prose only, in this folder. The lane tree was not edited.

## Outputs (this folder)

- `gate-block.md` — `## Gate` draft with corrected quotes and resolved revisions.
- `mistakes-block.md` — `## Mistakes` draft, one row.
- `digest-sweep.txt` — receipt of the full-history blob digest sweep (exit 0).

## Corrections to the existing draft `corpus/lessons/round-77.md` (not applied; lane tree read-only)

1. **Placeholders.** The header still reads `CONTROLS_REV` and `FREEZE_REV`. Resolved:
   `CONTROLS_REV` = `e6fcdc4770c2fa73e5ccda99445c4311128d7e0d`; `FREEZE_REV` =
   `a9530782578723de1364e0a3a47effcde8c85c23` (`git show --stat a9530782` adds only `claims.md`).
2. **S191 quote is wrong.** The draft's quote "supersede it with an append-only correction entry
   naming the superseded text" is **11 words, not 12**, and spans lines 163–164 of
   `corpus/lessons/round-76-verifier-spotcheck.md` at `6defa58d` (`wc -w` = 11; `sed -n 150,164p`).
   Replacement drafted: "is honoured by naming the controls revision in every receipt" — 10 words,
   verbatim on line 161 (the false claim itself). The correcting clause is on lines 161–162.
3. **S190 is correct:** "Outer batteries score exit codes in a fixed subject order." — 10 words, line 150.
4. **S192 is correct:** claims.md line 1 heading, verbatim; reject and flip match the S189 precedent.
   Registry ends at S189, so S190–S192 are free.

## Mistakes block — the row and why this one

The draft's two rows are not both usable. Row 1 (the state file in the lane tree) has no receipt and
the file was removed before any commit, so it is prose-only. Row 2 (missing subject) is receipt-backed
(`controls/mutant-missing-subject.txt:5`), but that receipt reproduces the guard with a mutant path, not
the real slip path. The row drafted instead is a receipt-identity slip found by sweep:

- `controls/before-oracle-v3.txt:4` and `:7` claim the oracle sha256 `9bb74e2a…248b1`.
- The committed oracle `corpus/evidence/round77/forgers/forge-order-matrix.py` is blob `1540e364…`,
  sha256 `e7a12850…` (`controls/forge-as-matrix-summary.txt:6` agrees with that digest).
- Sweep: every blob in the lane's full object history. Positive control `e7a12850…` → 1 hit
  (blob `1540e364`, path `corpus/evidence/round77/forgers/forge-order-matrix.py`), so the sweep works.
  `9bb74e2a…` → 0 hits (`digest-sweep.txt`).
- Two single-edit variants of the committed oracle (guard call removed; guard function and call removed)
  did not reproduce `9bb74e…` either. The pre-guard bytes no longer exist to compare.
- Captured-by: none in round 77. QUALITY 125 covers claims files only; receipts are outside it.
- Limit: the frozen before-receipt cannot be amended. The gap is recorded as a limit, not repaired.

## Verification performed (exit codes observed)

- `sha256sum` of frozen instruments: `matrix-battery-v4.py` 155fafb1…, `c3-count.py` 32b76565…,
  `loader-matrix-v3.py` b79d6441… — all equal the digests pinned in `claims.md`. Exit 0.
- Quote/line checks: `git show 6defa58d:corpus/lessons/round-76-verifier-spotcheck.md | sed -n 150,164p`;
  word counts via `wc -w` on each quote.
- `git cat-file --batch-all-objects` sweep (`digest-sweep.txt`): `sweep rc=0`, `exit: 0` written in receipt.
- `git status --porcelain` and `git diff --numstat -- corpus/evidence/round76/claims.md`: exit 0.

## Observations for the main agent (not in the drafts)

1. **C2 landing is uncommitted.** `git diff --numstat -- corpus/evidence/round76/claims.md` prints
   `12 0` and `git status` shows `M corpus/evidence/round76/claims.md`. The `## Correction — round-76
   claims prose` block is in the working tree only. `c3-count.py --rev <landing>` cannot score an
   uncommitted edit; the landing must be committed before the C2 predicate is claimed.
2. **Battery deletes the caller's `--work` root.** `corpus/evidence/round77/matrix-battery-v4.py:220`
   resolves `--work`, and `:256–257` runs `shutil.rmtree(work, ignore_errors=True)` in a `finally`.
   Pointing `--work` at a directory that holds other data deletes that data. Not observed this round
   (every receipt uses `/fast/scratch/...`); a latent hazard, not a mistake row.
3. **Oracle guard is prose-only as evidence.** `forge-order-matrix.py:22–27` documents the `.state`
   write, and the state-file slip is not in any receipt. The lesson should cite it as a limit.

## Host / scratch / tooling

- Scratch: `/fast/scratch/hyaku/chousa-r77/R77ScribeA/` created; removed by `trap ... EXIT`.
- One earlier probe wrote `/tmp/r77probe` (a Python hash test of oracle variants, under 1 KB). It was
  removed with `rm -rf` in the next command; it was outside the `/fast/scratch` rule and is disclosed here.
- No installs or upgrades. No pacman, no network, no git/jj mutation, no commit, no push, no subagent.
  Lane tree, `corpus/`, `tools/`, `.ufo/` outside this folder: read-only.

## Checks for the main agent to run once (not run by this seat)

- `python3 -B corpus/evidence/round77/c3-count.py --lane . --base a519fb0a80cf52c7988713c1f05b3ce8440fedda --rev <landing>` after the C2 correction is committed.
- `python3 -B corpus/evidence/round77/matrix-battery-v4.py --matrix corpus/evidence/round76/loader-matrix-v3.py --work <fresh dir>` — expect `BATTERY=PASS forgers_rejected=11/11 positive=2/2 oracle=REJECTED`.
