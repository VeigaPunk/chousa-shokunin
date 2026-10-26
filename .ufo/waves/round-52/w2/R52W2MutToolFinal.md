# R52W2MutToolFinal — C1 tool mutation sweep (wave 2, falsify)

Seat: R52W2MutToolFinal. Attacked: the landed `tools/capture-text.py` (the C1
operand of the round-52 freeze) and the coverage of both detectors
(`c1-count.py` frozen counter, `c1-supplement.py` post-freeze supplement).
No tools installed (nothing needed; no pacman/uv/npx action). No git/jj used.

## System under test — two snapshots
The lane tool changed MID-RUN: at 20:34 (mtime) a revision landed replacing the
zip-directory size trust with an actual-inflation `Limited` stream
(`zlib` import, `Limit` class, bounded `_rels/.rels` read, `zlib.error/EOFError`
added to the unreadable mapping). I tested BOTH snapshots end-to-end; the
matrix and kill cases below are re-verified on the CURRENT bytes.
- snapshot A (`pristine.py`): sha256 `81ba0db0584c6069c4ae57c820fa0b4d5deb5af68c4751e5f89ee23cf2d05277` (the wave-1 landed tool)
- current B (`pristine2.py`): sha256 `6902db6acf3ae5a0ac579ff88ae4fe4a36877b7b960c438bf36a67007b26be17`

## Baselines (both must pass before mutation)
```
c1-count.py --tool pristine2.py --seed 5201  -> LEGS=9/9 C1=PASS rc=0
  REAL: rc=0 count=1 locate=(0,1,8996) chars=19682
c1-count.py (default rng)                    -> LEGS=9/9 C1=PASS rc=0
c1-supplement.py --tool pristine2.py --seed 5201 -> 4/4 PASS rc=0
c1-supplement.py (default rng)                -> 4/4 PASS rc=0
```
Snapshot A passed identically (same 19682 chars, same locate offset).

## Kill matrix (deterministic, `--seed 5201`, TMPDIR=scratch; per-leg defaults)
| # | mutant (one class each) | counter | supplement | verdict |
|----|----|----|----|----|
| 1 | root check removed | 9/9 PASS | 4/4 PASS | SURVIVES both |
| 2 | size bound removed (all 3 enforcement points) | 9/9 PASS | 4/4 PASS | SURVIVES both |
| 3 | MAX_PART = 1 KiB | 2/9 FAIL | 0/4 FAIL | KILLED both |
| 4 | `..` target check removed | 9/9 PASS | 4/4 PASS | SURVIVES both |
| 5 | MemoryError mapping removed | 9/9 PASS | 4/4 PASS | SURVIVES both |
| 6 | el.clear() moved to start events | 1/9 FAIL | 0/4 FAIL | KILLED both |
| 7 | RUN_BREAKS: any ancestor w:r | 9/9 PASS | 4/4 PASS | SURVIVES both |
| 8 | fallback depth never decremented | 8/9 FAIL | 0/4 FAIL | KILLED both |
| 9 | external rels not skipped | 9/9 PASS | 4/4 PASS | SURVIVES both |
|10 | refusal printed to stdout | 8/9 FAIL | 4/4 PASS | KILLED counter only |
|11 | --locate counts overlapping occurrences | 9/9 PASS | 4/4 PASS | SURVIVES both |
|12 | text joined with no final newline | 3/9 FAIL | 0/4 FAIL | KILLED both |
Kill details: m03 all legs rc=2 (every package >1 KiB); m06 all `w:t` text lost
(`text differs at 0, got 5 chars, want 147` — start-clear wipes text the C
parser later assigns); m08 `ALTCONTENT text differs at 35`; m10 `REFUSE bytes
not refused`; m12 PARAS text differs at final char. m03/m06/m08/m12 also fail
the supplement. m10 survives the supplement because it has no refusal leg.

## Survivors of BOTH detectors — generated killing cases (all run)
Mutants in `scratch/mutants2/`, fixtures in `scratch/k*.raw` (one source zip
each). Pristine = current tool; outputs observed:
- m01 (root check): k1 footnotes-root main part. Mutant prints `LEAK` rc=0;
  pristine `REFUSED main part 'word/footnotes.xml' is not WordprocessingML
  (root ...footnotes)` rc=2.
- m02 (size bound): k2 main part inflates to 283115734 B (>256 MiB cap).
  Mutant prints 283115520 chars rc=0; pristine `REFUSED 'word/document.xml'
  inflates to ... (limit 268435456)` rc=2.
- m04 (`..`): k4 member literally named `../escape.xml` as officeDocument
  target. Mutant prints `ESCAPED` rc=0; pristine `REFUSED officeDocument target
  '../escape.xml' leaves the package root` rc=2.
- m05 (MemoryError): k5 ~160 MiB main part under `ulimit -v 330000/270000`.
  Pristine rc=2 `REFUSED package too large to render in memory` (mapped);
  mutant rc=1 `MemoryError` traceback at text_form (unmapped).
- m07 (any-ancestor w:r): k7 tab stop of `w:pPr/w:tabs` inside a run-owned
  textbox (`v:textbox` in `w:pict`). Pristine `TABTEXT\nEND\n`; mutant
  `\tTABTEXT\nEND\n` (both rc=0, text differs).
- m09 (external rels): k9 first officeDocument rel is `TargetMode="External"`
  shadowing the real one. Pristine renders `DOCTEXT` rc=0; mutant refuses
  (root `{x}coreProperties`) rc=2.
- m11 (overlap): k11a `aaa` locate `aa` — pristine `LOCATED count=1 offset=0`
  rc=0; mutant `count=2` rc=1 (exit flip). k11b `aaaa` — count 2 vs 3, rc=1.
Each of the seven is a real behavior difference against the current tool; the
frozen counter and the supplement never see them: REFUSE legs only exercise
bytes/html/no-rel/dangling-target (claims.md:42-44 predicate names exactly
those); supplement legs are respelled copies of the same six text generators
plus the pinned REAL digest - no wrong-root, oversize, escaping target, OOM,
tab-stop-in-run, external-rel or self-overlapping-quote input exists in either
detector. The recorded-claim text (claims.md:31-47) likewise stops at
not-a-zip/no-rel/missing-target; the richer refusals live only in the tool's
own docstring, so m01/m02/m04/m05 are exactly the "post-candidate refusals"
that are expected frozen-counter survivors; the supplement sees none of the
seven either (verified 4/4 PASS on each).

## Restoration evidence
Lane sources untouched: `tools/capture-text.py` sha256 at run start
`81ba0db0...`; current tree `6902db6a...` (the L1/sibling landing at 20:34,
read-only observed); `c1-count.py` `4ec29333...`, `c1-supplement.py`
`86711a5f...` (recorded, never written). No writes outside scratch + this
report; no fleet-root files created. Scratch removed after this report.

## VERDICT
Mutated the landed capture-text.py: 5 killed by the frozen counter, 1 by the
counter only (m10), and 7 survived both detectors - every survivor killed by a
generated package (footnotes root, oversize, `..`-escape, ulimit MemoryError,
run-owned tab stop, external-rel shadow, self-overlapping quote); supplement
blind to all seven; claims text does not cover them either.
