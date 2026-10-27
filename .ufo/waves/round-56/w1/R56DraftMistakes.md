# R56DraftMistakes — mistakes mined for `corpus/lessons/round-56.md` `## Mistakes`

Seat R56DraftMistakes (leaf; no dispatch). Lane `chousa-shokunin`, HEAD `99eff0e`; claims frozen at `41c58925`;
candidate `46e1758`. Scratch `/fast/scratch/hyaku/chousa-r56/R56DraftMistakes`, removed at exit. No production
file written, no network, no pacman. Every command below ran; scratch paths are shown as `$S`.

**Adjudication up front:** (1) is a genuine round-56 mistake (two defects in one draft); (2) is round-55's D3, whose
class is captured by QUALITY 9 in letter but by no check; (3) is round-55's D1, captured by QUALITY 104 and already
homed in `corpus/lessons/round-55.md:17` — re-entering it verbatim in round 56's table would break QUALITY 9's one
home. Rows for the round-56 table are drafted in §4 with that home stated.

## 1. Candidate (1) — first driver draft: equivalent mutant M9 + gyppable kill rule — VERIFIED

Committed facts: `corpus/evidence/round56/claims.md:21-31` discloses both pre-freeze defects; the gate's window filter
carries two newline guards (`corpus/evidence/round56/c1-gate.py:168-169`: `any(c in w for c in "\t\n\r\ufffd")` and
`or any(ord(c) < 0x20 for c in w)`); the landed mutant set adds the second edit only for M9
(`corpus/evidence/round56/c1-count.py:97-98`, `EXTRA = {"M9": […]}`).

(a) **M9 equivalence, reproduced.** Scratch clone at `46e1758` with `EXTRA = {}` and `SEEDS = (7,)` (one seed is
enough: an equivalent mutant's vector never differs from G's):

    $ cd $S/lane && python3 corpus/evidence/round56/c1-count.py --work $S/work-m9
    CANDIDATE=1/1 seed7=(0, 'PASS', 'PASS', 'PASS', 'PASS')
    MUTANT M9 WIN_NL SURVIVED
    RUNS=65
    CANDIDATE=1/1 KILLED=8/9 DENIED=2/2
    C1=FAIL

    (exit 1; M1-M8 killed with their own reasons, probes DENIED 2/2)

(b) **Kill-rule forgery, mechanism reproduced.** The committed JUNK builder's FLIP tool corrupts the first
`capture_sha256` cell on odd calls (`corpus/evidence/round56/controls/build-c1-junk.py:27-43`). Driving it
alternately through the landed gate and an M3 (NO_SHA) gate copy, with FLIP call parity aligned to the roles:

    --- call1 G   GENOLE=FAIL S901 capture_sha256 | LEGS=2/4 C1=FAIL   (rc=1)
    --- call2 M3  LEGS=4/4 C1=PASS
    --- call3 G   GENOLE=FAIL S901 capture_sha256 | LEGS=2/4 C1=FAIL
    --- call4 M3  LEGS=4/4 C1=PASS

`S901 capture_sha256` is exactly M3's marker (`c1-count.py:89`). A rule that takes one seed's "G fails with the
clause's reason / mutant passes" therefore reports a kill for M3 from a tool that never writes a bad digest.

**The L1's own FLIP-kill line has no committed receipt — say so explicitly.** `grep -rn FLIP` over the lane finds
only `claims.md:28-29` (the `mGmG`/seed-56 kill), `build-c1-junk.py:4` and `controls/c1-controls.txt:25` (the header
naming the FLIP entry). The committed controls show the FLIP battery entry *not* killing: JUNK block
`controls/c1-controls.txt:47` `MUTANT M9 WIN_NL KILLED by CANDIDATE` and `:51` `KILLED=1/9`. The original forgery is
disclosed text, not a record. A criterion-33-style check extended to claim files (scratch `checks/kill-sentence-check.py`)
confirms it: on `claims.md` it prints `UNRECEIPTED line 28 mutants=['FLIP', 'FLIP', 'M3']` and
`UNRECEIPTED line 37 mutants=['M9']` (exit 1 — the M9 sentence is true but names no receipt), and on a copy that
names `controls/c1-before.txt` and marks the FLIP observation as not receipted it prints `UNRECEIPTED=0` (exit 0).

**Criterion.** QUALITY 28 ("a surviving mutant becomes a fixture class before data") is the nearest for (a) but its
letter is "a mutant of a landed tool" and its shown-able-to-fail case is round-30 tool mutants, so a gate-mutant set
is outside it; QUALITY 33 ("a detector-kill sentence is receipt-backed") is the nearest for the FLIP line but binds
"a lesson sentence" while the line sits in a frozen claim file. Neither ran. For this class the answer is **none**;
drafts 106 and 107 below. Checks that fail on it: the `EXTRA = {}` run in (a) (survivor) and the parity-aligned
sequence in (b) (a kill pattern with no violation).

## 2. Candidate (2) — round-55 report cited revisions its receipts do not name (D3) — VERIFIED

    $ git show 53f1ce6b:corpus/evidence/round55/c2-measure-after.txt | head -1
    # R55-C2 after-measurement (L1) at lane master 5a35ebd6cff2f165b4785baa592c269fb04179f0
    $ git show 53f1ce6b:corpus/evidence/round55/c3-measure-after.txt | head -1
    # R55-C3 after-measurement (L1) at lane master 5a35ebd6cff2f165b4785baa592c269fb04179f0

`.ufo/reports/round-55/chousa.md:31-32` says C2 and C3 were "measured at `29cfb12a`" and a C2 "re-run at `53f1ce6b`";
`grep -rl 53f1ce6b corpus/evidence/round55 corpus/evidence/round56` → only `round56/claims.md` (the tip name). Closure
`corpus/lessons/round-55-verifier-spotcheck.md:31` (D3) and the correction at `corpus/lessons/round-55.md:32` agree.

Check (scratch, `checks/rev-citation-check.py`: every `measured|re-run at \`<rev>\`` must appear in a receipt header):

    $ python3 $S/checks/rev-citation-check.py .ufo/reports/round-55/chousa.md chousa-shokunin/corpus/evidence/round55
    CITES=4 UNNAMED=3 29cfb12a 53f1ce6b          (exit 1)
    $ python3 $S/checks/rev-citation-check.py $S/checks/r55-fixed.md …   # copy with both citations → 5a35ebd6
    CITES=4 UNNAMED=0                            (exit 0)

**Criterion.** QUALITY 9 ("one home per number and finding … names its owning file + revision") should have caught it;
12 (kept score re-derived/frozen) and 27 (stated re-run count = receipts) do not reach a *revision label* on a report
sentence, and no check reads report citations. Partially captured → draft 108 gives it a runnable check.

## 3. Candidate (3) — round 55 filed before W1 settled, never dispatched W2 (D1) — VERIFIED, already captured

    $ git cat-file -e 53f1ce6b:corpus/evidence/round55/w1-results.json      → fatal … does not exist (128)
    $ git ls-tree -r --name-only 53f1ce6b .ufo/waves/round-55/w1/ | grep -c '\.md$'   → 36
    $ python3 -c '…len(w2-spec["items"])'                                   → 36 items; 0 `w2.ready` at TIP
    $ cat corpus/evidence/round55/wave-settled-r55.txt                      → UNSETTLED w1 no committed w1-results.json

Re-run now, post-salvage (`e5a3795`, committer 01:26:01):

    $ python3 corpus/evidence/round55/wave-settled-check.py --round 55
    UNSETTLED w1 results=2026-10-27T01:26:01-03:00 after report=2026-10-27T01:11:40-03:00   (exit 1)

**Live hazard for this round:** the round-56 dispatch marker is untracked (`?? .ufo/waves/round-56/w1.ready.dispatched`),
and the check only sees committed markers:

    $ python3 corpus/evidence/round55/wave-settled-check.py --round 56 --before-filing
    usage: no committed <wave>.ready.dispatched under .ufo/waves/round-56               (exit 2)

So QUALITY 104's guard cannot rule round 56 until `w1.ready.dispatched` is committed; an L1 who files with the marker
uncommitted gets a usage error, not a verdict. **Criterion: 104** (exists; it ran red at round 55 and the report was
filed anyway under the wrap notice, `corpus/lessons/round-55.md:17`). No new criterion; the row's home is round 55.

## 4. Draft rows for `corpus/lessons/round-56.md` `## Mistakes`

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| 1. a gate counter's first draft scored an equivalent mutant and a kill rule an alternating tool forges: M9 dropped one of the window filter's two newline guards, and any verdict-vector difference counted as a kill — both found by the L1's own control runs before the freeze | `corpus/evidence/round56/claims.md:21-31`; `c1-count.py:97-98` vs `c1-gate.py:168-169`; scratch `EXTRA={}` run → `MUTANT M9 WIN_NL SURVIVED … KILLED=8/9`; the FLIP kill line (`claims.md:28-29`) is in **no committed receipt** — the committed JUNK receipt prints `KILLED=1/9` | `none` — QUALITY 28 binds a landed tool's mutants, QUALITY 33 binds lesson sentences; neither reaches a gate-mutant set or a claim file | mutant drops both guards and the rule demands the clause's own reason in 3 G runs + 3 mutant passes at both seeds (1-in-400 for a call-counting forge); check ran: `EXTRA={}` → M9 SURVIVED (scratch, 65 runs); JUNK control → `KILLED=1/9` (`controls/c1-controls.txt:47,51`) |
| 2. a report cited measurement revisions its receipts do not name (round-55 D3, corrected this round): "measured at `29cfb12a`", "re-run at `53f1ce6b`" against receipts whose headers say `5a35ebd6` | `.ufo/reports/round-55/chousa.md:31-32`; `git show 53f1ce6b:corpus/evidence/round55/{c2,c3}-measure-after.txt \| head -1`; `corpus/lessons/round-55.md:32`; closure §1 D3 | QUALITY 9 (letter) — no check reads a report's citations | cite only the revision a receipt header names; check ran: `rev-citation-check.py` → `CITES=4 UNNAMED=3 29cfb12a 53f1ce6b` exit 1, corrected copy → `UNNAMED=0` exit 0 (draft 108) |
| 3. round 55 filed with W1 unsettled and W2 never dispatched (closure D1) — **already homed**: `corpus/lessons/round-55.md:17`; enter here only if round 56 repeats it | `corpus/evidence/round55/wave-settled-r55.txt`; no `w1-results.json` at `53f1ce6b`; `.ufo/waves/round-55/w2-spec.json` 36 items, no `w2.ready` | QUALITY 104 — it existed and ran red at round 55; the L1 filed under the wrap notice | run 104's check before filing; re-ran now: round 55 → `UNSETTLED … after report`, exit 1. Hazard: round-56's `w1.ready.dispatched` is untracked, so `--round 56` exits 2 until it is committed |

## 5. Draft QUALITY criteria 106–108 (file's shape; append after 105)

    ## Round-56 additions (appended 2026-10-27; criteria 1–105 unchanged)

    106. **A counter's kill rule cannot be satisfied by a tool that alternates its behaviour or reads its run
        number.** Round 56's first rule took any verdict-vector difference as a kill; the committed JUNK battery's
        FLIP tool corrupts the first `capture_sha256` cell on odd calls, so a single-seed rule sees G fail with
        `S901 capture_sha256` — M3's own marker — while the M3 gate passes on the next call (scratch, clone at
        `46e1758`: odd call → `GENOLE=FAIL S901 capture_sha256`, `LEGS=2/4`; even call under the M3 gate →
        `LEGS=4/4 C1=PASS`). The killed-clause pattern is produced without the violation, and the L1's `mGmG`
        seed-56 instance is in no committed receipt. Check: `python3 corpus/evidence/round56/c1-count.py` prints
        `KILLED=9/9` only with the clause's own reason in three G runs and three mutant passes at **both** seeds
        (a call-counting forge matches one order in 400), and
        `python3 corpus/evidence/round56/controls/build-c1-junk.py OUT && python3 corpus/evidence/round56/c1-count.py
        --battery OUT` prints `KILLED=1/9`. Shown able to fail (ran): the scratch parity-aligned sequence above
        yields the M3 kill pattern from a tool that never writes a bad digest. — `corpus/evidence/round56/claims.md:25-31`;
        `.ufo/waves/round-56/w1/R56DraftMistakes.md` §1(b).
    107. **A frozen mutant set contains no equivalent mutant, and a survivor is classified before the target is
        fixed.** Round 56's first pass let M9 drop one of the window filter's two newline guards, so M9 could not be
        distinguished from the gate: the counter with `EXTRA = {}` prints `MUTANT M9 WIN_NL SURVIVED`,
        `KILLED=8/9`, `C1=FAIL` (scratch, seed 7, 65 runs); the landed set drops both guards
        (`c1-count.py:97-98`) and the landed builder kills M9 at both seeds. Check: rebuild the mutant set with the
        first edit and run the counter — a survivor is a mutant-set defect, never a data result; CANDIDATE must kill
        it (`controls/c1-before.txt:17`). Shown able to fail (ran): the `EXTRA = {}` run above. —
        `corpus/evidence/round56/claims.md:21-24`; `.ufo/waves/round-56/w1/R56DraftMistakes.md` §1(a).
    108. **A report's measurement citation names the revision its committed receipt header names, and a cited re-run
        has a receipt.** Round 55's report said C2/C3 were "measured at `29cfb12a`" and a C2 "re-run at `53f1ce6b`";
        the receipts' first lines say lane master `5a35ebd6` (`corpus/evidence/round55/c2-measure-after.txt:1`,
        `c3-measure-after.txt:1`) and no receipt names `53f1ce6b`. Check: for every `measured at` / `re-run at`
        citation in a report, require a file under the round's evidence whose first line carries that revision —
        scratch `checks/rev-citation-check.py` prints `CITES=4 UNNAMED=3 29cfb12a 53f1ce6b`, exit 1, on the
        round-55 report and `CITES=4 UNNAMED=0`, exit 0, on a copy citing `5a35ebd6`. Shown able to fail (ran):
        both runs. — `corpus/lessons/round-55-verifier-spotcheck.md:31`; `corpus/lessons/round-55.md:32`.

## 6. Findings, limits, touched surfaces

- **Untracked after-receipt.** At HEAD `99eff0e`, `corpus/evidence/round56/c1-measure-after.txt` is `??` (untracked);
  the `KILLED=9/9 C1=PASS` line cited by the frozen claim has no committed receipt yet. The committed receipts
  (`c1-before.txt`, `c1-controls.txt` at `46e1758`) both print `KILLED=1/9`. Candidate 1's fix is therefore shown
  against the mutant set (M9) but not yet against the target.
- **Archive copies cannot run the gate.** `git archive 46e1758 | tar -x` gives a tree without history; the gate's
  REGRESS leg runs `git show dba605de:corpus/evidence/round54/quotes.tsv` and the run dies `ENV_CHANGED git show
  corpus/evidence/round54/quotes.tsv`, exit 2. A test copy of this gate must be a `git clone --shared` + checkout
  (what §1 used), not the archive recipe in the seat spec.
- **Criterion numbering has no round-56 home yet:** `QUALITY.md:849` still heads the block that runs to 105 with
  "criteria 1–80 unchanged"; 106+ needs its own heading (drafted in §5).
- **QUALITY 33's scope gap:** it binds "a lesson sentence"; the FLIP kill line is in a frozen claim file, so the
  criterion as written could not fire on it. Named, not edited.
- Limits: the M9 reproduction ran one seed (`SEEDS=(7,)`) for time — equivalence is seed-independent; the FLIP
  reproduction is my scratch parity sequence, not the L1's `mGmG` observation (unreceipted, §1). I did not run the
  frozen counter on the committed battery; that is the after-measurement seat's work.
- Touched surfaces: this report only (lane write). Scratch removed at exit. Out of scope: `QUALITY.md`, the lesson,
  claims, gate, counter, battery, probes, any git/jj state.

VERDICT: attacked all three candidates — (1) the equivalent-mutant + forged-kill-rule class is real (M9 SURVIVED with `EXTRA={}`, and a parity-aligned FLIP forges M3's kill pattern with no violation; the L1's own FLIP-kill line has no committed receipt), (2) D3 reproduces under a citation check that fails on the report and passes on a corrected copy, (3) D1 reproduces under QUALITY 104's own check and that check is currently unusable on round 56's uncommitted marker — all survived as findings; none of the frozen predicates was touched.
