# RevC1LegsH3 — review of C1 legs H13 OUTSIDE, H14 BIGTXT, H15 BIGRAW

Scope: `corpus/evidence/round61/c1-count.py` (read-only; not edited), legs H13/H14/H15 only, against
predicate R61-C1 in `corpus/evidence/round61/claims.md`. Reference builder
`controls/ref-build-spans.py` sha256 `86d64c31…eccfd` (re-checked with sha256sum). Counter output
lines below were captured in scratch (deleted before yield) and are quoted verbatim.

## Findings (severity order)

### F1 — H13 OUTSIDE passes a builder that writes outside bytes into output (counter defect, high)
- Builder `f1`: reference with the containment check removed (ref lines 97–98), so a cache `.txt`
  symlink is read through; writes its spans, then exits 1 (ref line 336 `return 0` -> `return 1`).
  The builder's own contract is "any refusal writes nothing and exits 1" (builder docstring, lines 27–28).
- Counter: `LEG H13 OUTSIDE pass rc=1 leaked=False` at seeds 61001, 61002, 61003.
- Kept fixture (`--keep`, seed 61001): span `S236-1.txt` is 189 bytes, `marker_in_span False`,
  `outside-text-in-span True`; the span is an exact substring of `outside.txt` (the leaked content).
- Cause: the marker is written at byte 0 (c1-count.py:458 `marker + " " + raw`). Spans are
  `form[off-80 : off+len+80]` (CONTEXT, line 74; golden spans lines 224–225), and the quote sits well
  past byte 80 (paragraphs of 14–24 words, lines 163–171), so the marker never reaches an output file.
  The leak test (lines 463–467) searches only for the marker in `out/`; line 468 accepts any non-zero exit.
- Direction for L1 (not applied): place the marker inside the quote's ±80-char window, or test for a
  distinctive run of the outside file's own bytes in every output file.

### F2 — H14 and H15 pass a builder that buffers 64 MiB+1 before deciding (counter calibration defect, both legs)
- Builder `f2`: reference with the size check moved after `f.read(MAX_CAPTURE + 1)` (ref lines 140–145
  replaced). Violates the builder contract "decided before any byte is read" (builder docstring, lines 16–18).
  Under the literal predicate ("peak RSS under 96 MiB") it passes.
- Counter: `H14 BIGTXT pass rc=1 rss_kib=86452` (61001), `85828` (61002), `86364` (61003);
  `H15 BIGRAW pass rc=1 rss_kib=85260 / 86184 / 86008`. Limit `98304` KiB.
- Cause: `RSS_LIMIT_KIB = 96 << 10` (line 76) leaves 32 MiB over the builder's 64 MiB cap. The
  reference measures ~19–21 MiB (`rss_kib` 19360–20792 across all runs), so a limit nearer that
  baseline would separate read-ahead from refuse-first. `big_leg` (line 482) checks only `rc != 0`,
  no timeout, clean output, and the RSS ceiling.
- INFERENCE (untested; counter not edited): a limit of about 48 MiB would still admit the reference
  and reject `f2`.

### F3 — H15 passes a builder whose 192 MiB read runs in a session-detached helper (counter limit, medium)
- Builder `f3`: reference line 123 replaced by `subprocess.Popen([python, helper-that-reads-the-file],
  start_new_session=True)`; the builder then refuses with exit 1. It also fails P02 by construction,
  which does not affect the H15 verdict.
- Counter: `H15 BIGRAW pass rc=1 rss_kib=21720` (61001), `21092` (61002), `21668` (61003); the helper
  performs `f.read()` on the full 192 MiB sparse OLE file.
- Cause: the measure is the `os.wait4` rusage of the direct child (lines 258, 271). With
  `start_new_session=True` (line 254) and the `killpg` cleanup (lines 255–264), a detached helper is
  outside both the rusage and the kill.
- Control `f4` (same helper, waited with `subprocess.run`): `H15 BIGRAW fail rc=1 rss_kib=206456`
  (61001), `205692` (61002), `205384` (61003). Waited descendants are counted; only detached ones escape.
- Standalone probe (scratch): a waited reader of the same 192 MiB sparse file gave `ru_maxrss_kib = 206700`.
  The helper's RSS inside the counter was not measured separately (INFERENCE: about the same).
- Adversarial: a real builder would not detach. The measurement gap is still real: the big-read hazard
  is not measured across the process tree.

## Discrimination controls (counter sanity; all ran)
- Reference `controls/ref-build-spans.py`, seed 61001: `LEGS=20/20 C1=PASS`; H13 `rc=1 leaked=False`,
  H14 `rc=1 rss_kib=20292`, H15 `rc=1 rss_kib=20784`.
- `f0` (reference with the 64 MiB size guard removed, ref lines 140–141), seed 61001:
  `H14 BIGTXT fail rc=1 rss_kib=413424`, `H15 BIGRAW fail rc=1 rss_kib=415768`, `LEGS=18/20 C1=FAIL`.
  The legs catch a builder with no cap.

## Correct builders (false-negative search): none found
- `c1`: a cache link is treated as absent, so the row is refused with exit 1 (edit at ref line 96).
  H13/H14/H15 pass at 61001, 61002, 61003.
- `c2`: a link out of the cache prints a message and exits 2 before any write (ref line 98).
  H13 `pass rc=2` at all three seeds; H14/H15 pass.
  Note: the builder docstring maps a refused row to exit 1 (line 44); exit 2 is the stated class for
  usage/output refusals. The H13 predicate accepts any non-zero (line 468), so this looseness is a leg
  limit, not a false negative.
- `c3`: the size check runs before `realpath` (ref line 96 area). H13/H14/H15 pass at all three seeds.
- Total: 3 correct builders × 3 seeds × 3 legs = 27 leg-runs, 0 failures.

## Counter line references
CONTEXT line 74 · BIG line 75 · RSS_LIMIT_KIB line 76 · golden spans 218–226 · process group, session,
killpg 254–264 · `os.wait4` line 258 · `ru_maxrss` line 271 · H13 450–468 (marker line 458, leak scan
463–467, predicate 468) · `big_leg` 471–483 (sparse file with quote at start 476–479, predicate 482) ·
H14/H15 wrappers 486–491 · plan entries 588–589.

## Commands run (all with `python3 -B`, fresh `--work` per run, TMPDIR in scratch)
- `python3 -B corpus/evidence/round61/c1-count.py --builder <B> --work <scratch>/w/<name>-<seed> --seed <seed>`
  for B in {reference, c1, c2, c3, f0, f1, f2, f3, f4} at seed 61001, and for c1, c2, c3, f1, f2, f3, f4
  at seeds 61002 and 61003.
- The same with `--keep` for f1 at seed 61001, then a Python check of the kept `out/spans/*.txt` against `outside.txt`.
- Standalone 192 MiB waited-reader probe (`ru_maxrss` via `os.wait4`).
- `git -C <lane> status --short` (read-only); no lane file written by this seat.

## Limits of this review
- Only H13, H14 and H15 were reviewed; the other 17 legs appear in the run output but were not assessed.
- Helper RSS in f3 was not measured in situ (see INFERENCE above).
- Nothing installed; no network; scratch `/fast/scratch/hyaku/chousa-r61/RevC1LegsH3/` deleted before yield.

VERDICT: LEG_DEFECTS=3 false_negative=0 false_positive=3 legs=H13 OUTSIDE, H14 BIGTXT, H15 BIGRAW
