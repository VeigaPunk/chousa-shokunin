# Round 61 · wave w1 · ScribeLogDraft (scribe)

## Findings

1. **Delivered.** Draft text for the three lane files is at `.ufo/waves/round-61/w1/ScribeLogDraft/draft.md`: §1 LOG.md round-61 entry, §2 SCORECARD.md round-61 verdict block, §3a corpus/README.md coverage-map row, §3b corpus/README.md "Round61 coverage and frontier" section with its Frontier paragraph. No lane file was written (`git status --short` shows no modified tracked files from this seat).
2. **Markers.** Every measured value is `<AFTER>`; no after value was taken from a seat report, fixture or positive control. Count: 71 `<AFTER` tokens across the four drafted sections (72 in the file including one literal mention in the scope note).
3. **Operability stays 3/10.** The SCORECARD draft keeps the numeric operability observable at 3/10 and says the C1 result is a 20-leg count, not a score. Depth, coverage and calibration carry no invented number.
4. **Verdicts are conditional.** Each verdict line restates the frozen kill rule (C1: 20/20 at three fresh seeds and `REAL_REBUILD=3/3`; C2: `C2=PASS` exit 0 on the landed commit) and leaves the verdict as `<AFTER>`. An unmet rule is an honest stop; the draft has no path to "verified" without the measurement.

## Calibration items for the L1 (checked, not fixed in the lane)

- **C2 CENSUS depends on a fleet-root script.** Predicate R61-C2 says the entry is checked "in the lane tree", but the CENSUS clause runs `scripts/sources-census.sh`, which the counter resolves through `--fleet`, defaulting to the fleet root (`c2-count.py:111,114`). That script exists at `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` (mode -rwxr-xr-x, Oct 19) and not in the lane (`ls chousa-shokunin/scripts` → no such directory). The draft discloses this in the LOG limits and the Frontier "Left open" list. Reproduction from a lane clone alone needs the fleet root.
- **Overreach predicate not frozen.** SCORECARD `## Planned — round 61` (line 2937) asked that C2 "requires a new entry and a measured no-overreach predicate or should be dropped". The frozen C2 has no overreach predicate (`c2-count.py` docstring: "structural … does not judge that a claim follows from its quotes"). The draft says so explicitly in §2 (candidate c, "not met") rather than claiming the planned row was satisfied.
- **Cap wording.** The claims file's C1 limit (ii) says "the 64 MiB caps". The counter has a 64 MiB text-form cap (docstring: "over 64 MiB chars") and a separate 96 MiB RSS limit (`c1-count.py:76` `RSS_LIMIT_KIB = 96 << 10`; leg H14 "limit=98304"). The draft states both numbers so the LOG does not conflate them.
- **Control fixtures differ from base on ROWS.** `controls/c2-before.txt` (base) reads `ROWS=0/3` with S134–S136 absent; the `absent` control in `c2-controls.txt` reads `ROWS=3/3` because the control fixture carries rows while lacking the entry. Both are correct for their fixtures; the draft quotes only the base line as "before".
- **Stale planned heading.** After landing, `## Planned — round 61 (not started)` in SCORECARD.md becomes history. The draft inserts the verdict block directly above it and does not rename it; the L1 decides whether to replace it with a round-62 planned heading (the file's convention is one planned section per next round).
- **Entry not yet on disk.** `corpus/knowledge/derived-output-safety-r61.md` is absent at this seat's read time (`ls corpus/knowledge | wc -l` → 82; no `*r61*` file). The coverage row's "Holds" text is therefore limited to the counter's required sections; the topic summary is `<AFTER>`.

## Frozen facts used (all read-only)

- Claims digest: `sha256sum corpus/evidence/round61/claims.md` → `9afec8d493f0ba511a256f38cd5098ff508f9ed311c6c49ff5383add9ce0acec`; `git show 2b0e17b:corpus/evidence/round61/claims.md | sha256sum` → same digest; `git diff --stat 2b0e17b -- corpus/evidence/round61` → empty.
- Digest also in the wave records: `grep -rl "9afec8d4" .ufo/waves/round-61/` lists `w1-spec.json` and `w1-dispatch.json`.
- C1 base receipt: `controls/c1-before.txt` → `LEGS=7/20 C1=FAIL`, exit=1, seeds 61001 and 61002 (both printed); failing legs P03, H07–H17, H20.
- C1 controls: `controls/c1-controls.txt` → base 7/20, noop0 1/20, always2 14/20, forge-token 7/20, naive-guard 10/20, reference 20/20, M01–M14 each KILLED, `CONTROLS_UNEXPECTED=0`.
- C1 reference: `controls/c1-reference.txt` → `LEGS=20/20 C1=PASS` exit=0 at seeds 61001–61003.
- C1 no-harm: `controls/regress-base.txt` → `REAL_REBUILD=3/3`, exit=0; `controls/regress-reference.txt` → `REAL_REBUILD=3/3`.
- C2 base receipt: `controls/c2-before.txt` → `ENTRY=0/1 TRIO=0/1 ROWS=0/3 QUOTES=0/0 COVERAGE=0/1 CLAIMS=0/1 LIMITS=0/1 CENSUS=1/1 C2=FAIL`, exit=1; rows S134–S136 absent.
- C2 controls: `controls/c2-controls.txt` → 12 negative cases all rc=1 (`C2=FAIL`), positive rc=0 `C2=PASS` with `QUOTES=8/8`, `echo-claims` rc=0 `C2=PASS`, `C2_CONTROLS_UNEXPECTED=0`.
- Positive entry quote count: `grep -c '^- Q' controls/c2-positive-entry.md` → 8 (Q1–Q8).
- Sources: `/usr/share/man/man2/open.2.gz` (16114 bytes) and `rename.2.gz` (5042 bytes) present; `corpus/SOURCES.md` table rows counted by `grep -cE '^\s*\|\s*S[0-9]{3,}\s*\|'` → 133 (matches the round-60 base count).
- Insertion anchors: LOG.md 1936–1942 is the round-60 entry (last); SCORECARD.md 2924–2937 holds the round-60 verdict then `## Planned — round 61`; corpus/README.md top table begins with `lessons/round-59.md` (row 7); the Round57 section is the file's last section (line 1234 onward).

## Method and boundaries

- No counter was run and no fixture was made: the assignment asks for a draft from frozen facts, and a measurement would have been a second source of after values. No scratch directory was created at `/fast/scratch/hyaku/chousa-r61/ScribeLogDraft/`, so nothing needed deletion.
- No tool installed or updated; no pacman; no git mutation; no network; no seat spawned.
- Writes: only `.ufo/waves/round-61/w1/ScribeLogDraft.md` (this report) and `.ufo/waves/round-61/w1/ScribeLogDraft/draft.md`.
- INFERENCE (marked): the statement that the L1 can reproduce C2 from a lane clone alone needs the fleet root — inferred from the `--fleet` default, not run from a clone.

## Verdict

Four drafted sections (LOG entry, SCORECARD block, coverage-map row, Round61 section with Frontier); every measured value left as `<AFTER>`; operability numeric 3/10 kept unchanged in the draft.

VERDICT: DRAFT_SECTIONS=4 after_markers=71
