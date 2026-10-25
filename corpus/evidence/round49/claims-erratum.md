# Round 49 — post-freeze disclosure (append-only; claims.md is unchanged)

date: 2026-10-25 · author: chousa L1 (`ChousaR49`)

The frozen claims, predicates, targets, kill rules and both counters
(`c1-count.py`, `c2-count.py`, freeze commit
`fe740e7838b338d17fec9338c909557e6e7fed7d`) are byte-unchanged. One file that
shipped in the freeze commit changed after wave-1 seats had scored:

## `build-spans.py` — raw-form span context clipped at a carriage return

- Observed: with every quote located and every span file an exact slice of its
  capture text form, `c2-count.py` printed `CAPTURE_BOUND=21/28`. The seven
  failing rows were all UTF-16LE `.raw` forms (the two OLE `.doc` captures).
  Their span files contain Word's paragraph mark, a bare CR. The frozen counter
  reads span files with `Path.read_text` (universal newlines: a bare CR reads
  back as LF) and compares them with the form text decoded from bytes (CR
  kept), so a true slice compares unequal. `.txt` forms are read with
  universal newlines on both sides and are unaffected.
- Repair: `build-spans.py` clips a raw-form span's context at the nearest CR on
  each side; a span is still an exact slice of the form at its recorded
  offset and still longer than its quote. One quote that was a whole paragraph
  (S100, `关于自引的说明：…自引。`) was shortened to its body
  (`对于合作发文的参考文献中，如果引文出现了任一合作者，那么这条引文将被认定为自引`),
  which keeps context inside the paragraph; the anchor `char` moved 1423 → 1431.
- What did not change: the counter's CAPTURE_BOUND rule, its other legs, the
  target and the kill rule. No quote, document or verdict was added or dropped
  to pass the leg.
- Why this is disclosed rather than silent: the closure judges the claim on the
  counter and predicate declared before data; a derivation tool changed after
  seats scored is reported so the closure can rule whether the C2 after-state
  stands. If it does not, C2 is an honest stop at `CAPTURE_BOUND=21/28` with every
  other leg full.

## Counter limits found by wave 1 (not repaired; frozen)

- C1 (`CritForgeC1`): a tool that replays the real tool's outputs for the
  pinned package passes `c1-count.py`. The counter is a conformance check on
  fixed inputs, not a mechanism audit (QUALITY 72).
- C2 (`CritForgeC2`): a single-space quote over a whole-capture span with one
  self-consistent anchor passes every structural leg. The round-49 manifest
  passes the separate substance floor `quote-substance-check.py`
  (`FAILURES=0`); that floor is not part of the frozen C2 rule.
- C1 (`MutTool` m8): a mutant that does not force `status` to `mined` survives,
  because every cited staged row in the frozen sets is already `mined`.
