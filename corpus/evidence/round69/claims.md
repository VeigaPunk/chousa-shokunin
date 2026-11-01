# Round 69 claims (frozen 2026-10-31 at commit A, against base `b51f4d879b95f42147a716eac1d05e7e01c981a0`)

Host: Windows/11, `python` 3.13.15 (`python -I` used throughout; no `python3` on this host), git 2.55.0.windows.3.
Fetches: none this round — both claims rest on own-work committed bytes opened this round (S166–S167), so nothing
beyond the lane repository is read; the standing r40/r65 fetch-scope and L2-floor template L0 questions stay open and
are routed around, never treated as answered. No wave: this host has no batched dispatch surface (the round-63
attempt-2 precedent, disclosed every round since); every verdict rests on committed counters, controls and receipts.
Trigger: the round-68 closure spot-check routed exactly two lane items to this round — (1) the round-68
after-battery receipt `corpus/evidence/round68/controls/after-freeze-battery.txt` carries a bare `EXIT=` for
invocation 1 (the very `receipt-exit-transcription` class the round mined), to be closed with a re-issued receipt
whose exit codes are captured explicitly, the r68 bytes kept as history; (2) the r68 SCORECARD correction note's G05
mechanism wording is imprecise (the truncated tail does name `tools/digest-in-tree.py`; G05 actually skips the row
because its parser requires >=4 cells), to be corrected append-only.

## C1 — operability (lowest-scored non-retired axis, 3/10)

Re-issue the r68 freeze-check battery receipt with explicit rc capture: re-run both invocations of the repaired
34-case battery at the round-69 landing tip (`python -I tools/freeze-check.py --selftest` and `--selftest
--lane-root .`), reading each exit code by immediate `rc=$?` after the redirected command (no pipeline — the r63/r68
receipt-exit-transcription class), into a new receipt `controls/after-freeze-battery-r69.txt` that names the
superseded bare `EXIT=` line. The r68 receipt bytes stay as committed history; `tools/freeze-check.py` itself is
byte-unchanged this round (sha256 `da9f6e16…b55c2`).

- Frozen before predicate (measured at the base `b51f4d879b95f42147a716eac1d05e7e01c981a0`):
  1. `grep -n '^EXIT=' corpus/evidence/round68/controls/after-freeze-battery.txt` shows `9:EXIT=` (bare) and
     `15:EXIT=0`; `grep -c '^EXIT=$' …` → 1, `grep -c '^EXIT=0$' …` → 1
     (`controls/before-r68-battery-receipt-defect.txt`).
  2. The old receipt's digest pins still re-derive at the base:
     `python -I tools/digest-in-tree.py --receipt corpus/evidence/round68/controls/after-freeze-battery.txt` →
     `DIGESTS_IN_TREE=1/1 DIGEST_IN_TREE=PASS` exit 0 — the defect is transcription-only, not pin rot
     (same before-receipt).
  3. `corpus/evidence/round69/controls/after-freeze-battery-r69.txt` does not exist at the freeze (the ls in the
     before-receipt exits 2: absence is the before state).
- Frozen after predicate (all must hold at the landing):
  1. `grep -c '^EXIT=0$' corpus/evidence/round69/controls/after-freeze-battery-r69.txt` → 2 and
     `grep -c '^EXIT=$'` (bare) → 0 in the same file.
  2. The receipt's transcript shows both invocations printing `SELFTEST 34/34 pass` and
     `VERDICT: FREEZE_CHECK=34/34 red_before_exit=1`, each `EXIT=` line captured immediately after its command;
     the receipt names the superseded r68 line and pins `TOOL_SHA256=da9f6e16…` (the tool bytes are unchanged
     since the r68 landing).
  3. `python -I tools/digest-in-tree.py --receipt corpus/evidence/round69/controls/after-freeze-battery-r69.txt`
     → `DIGESTS_IN_TREE=1/1 DIGEST_IN_TREE=PASS` exit 0 at HEAD (receipt `controls/after-r69-receipt-derivation.txt`).
  4. `git diff <base>..<landing> -- corpus/evidence/round68/ tools/freeze-check.py` is empty — no r68 bytes and no
     tool bytes change this round.
- Do-nothing control: the after-receipt is generated run output, not an edit — it cannot exist without re-running
  the battery; before-predicates 1 and 3 are red at the base by construction.
- No capability row: the repertoire (portable gate selftest execution) already entered in round 68; this round
  re-issues its evidence to the verifier-complete standard. Not scored as a capability acquisition.

## C2 — calibration (sourced on S166–S167, opened this round)

Correct the round-68 SCORECARD correction note's G05 mechanism wording, append-only: the r68 note says G05
"still passed because the truncated tail names no path", but the truncated tail does name `tools/digest-in-tree.py`
(in an unterminated backtick); G05 skips the row because its parser extracts pointers only from capability rows
with at least four cells (`tools/lane-preflight.py` g05, line 233: `len(cells) >= 4`), so the pointer is never read.
The correction lands as a new dated paragraph appended to SCORECARD.md (no r68 sentence bytes change) and is
demonstrated by a committed two-fixture control: a 3-cell capability row and a 4-cell capability row naming the
same missing path, run through `--only G05` — the 3-cell row is skipped (PASS, 0 pointers resolve), the 4-cell row
is parsed (FAIL, 1 unresolved).

- Frozen before predicate (measured at the base):
  1. `grep -c 'names no path' SCORECARD.md` → 1 (the r68 correction paragraph, line 3192); repo-wide
     (`grep -rn 'names no path' SCORECARD.md corpus/lessons/ LOG.md`) → 4: the SCORECARD note, the r68 lesson
     Mistakes row, and two quotations inside the round-68 closure spot-check (the non-author record quoting the
     wording it routed); all four stay as history (`controls/before-g05-note-greps.txt`).
  2. `grep -c 'len(cells) >= 4' SCORECARD.md` → 0 — the precise mechanism is recorded nowhere in SCORECARD.md;
     the parser ground is stable: `grep -n 'len(cells) >= 4' tools/lane-preflight.py` → line 233 (same receipt).
  3. The committed control fixtures demonstrate the mechanism at the base:
     `python -I tools/lane-preflight.py --only G05 --root corpus/evidence/round69/fixtures/g05-skip3` →
     `GATE G05 scorecard-paths PASS 0 capability pointers resolve` exit 0, and `…\g05-skip4` →
     `GATE G05 scorecard-paths FAIL 1 unresolved: corpus/no-such-entry-r69.md` exit 1 — the identical pointer,
     skipped in a 3-cell row, parsed in a 4-cell row (`controls/before-g05-skip-control.txt`).
- Frozen after predicate (all must hold at the landing):
  1. `grep -c 'len(cells) >= 4' SCORECARD.md` → 1 (the new note records the mechanism);
     `grep -c 'names no path' SCORECARD.md` → 2, the second hit being the new note's own quotation of the
     superseded wording (disclosed, the r67 correction-note precedent); the repo-wide count moves 4 → 5.
  2. The control re-run at the landing reads the same verdict pair
     (`controls/after-g05-skip-control.txt`); the parser line stays at 233 (`grep -n` unchanged).
  3. SOURCES.md gains rows S166 (the round-68 closure spot-check, the non-author routing record) and S167
     (the g05 parser bytes), both own-work tier B, opened this round; registry 165 → 167 (B 31 → 33, mined
     133 → 135); SOURCES.md diff additions-only, no held status/recheck/used-by cell changed.
- Do-nothing control: both after-greps are 0 at the base and the note cannot exist without being written; the
  fixtures exist at the base (mechanism ground, unchanged by the round), so the control alone cannot flip the
  greps.
- Do-nothing-unreachability of the mechanism claim: the control's verdict pair is fixed parser behavior — it
  neither proves nor depends on the note's existence; the note's after-greps are the claim state.

## Sizing (§9) and separability

Both targets are do-nothing-unreachable (C1's receipt is run output that does not exist at the base; C2's after-greps
are 0 at the base). C1 verifies from its own receipts alone (battery transcript, explicit rc lines, digest
re-derivation, empty round68/tool diff); C2 verifies from the greps, the parser line and the two fixture runs alone —
C2's evidence does not cite the re-issued receipt and C1's receipt does not cite the note. Claim axes are distinct
(operability, calibration); operability is the lowest-scored non-retired axis (SCORECARD `## Axes`: operability 3/10,
the only numerically scored axis, none retired) — the obligation is met by C1. One exploratory claim budget: unused
this round.

## Known limits, declared in advance

The re-issued receipt certifies the two invocations it transcribes at the named revision; it does not add a new
capability and does not move the frozen 3/10 observable. The G05 control demonstrates the >=4-cell parse boundary
only — it does not audit every G05 arm (header cells, separator cells, path prefixes, brace expansion stay covered
by the r63 batteries). G08 stays skipped in the preflight receipts (minutes-long full research-gate selftest; the
same skip r66–r68 disclosed). The registry grows by two own-work tier B rows: no external claim is made this round,
so no external fetch is taken (the r40/r65 L0 fetch-scope questions remain open; nothing beyond public read-only
was read, and nothing outside the lane repository was read at all).
