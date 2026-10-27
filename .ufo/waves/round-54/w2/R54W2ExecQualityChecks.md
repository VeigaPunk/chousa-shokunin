# R54W2ExecQualityChecks — the check command of each new QUALITY criterion 97–100, re-run on the tip
Seat `R54W2ExecQualityChecks` (executor, leaf). Lane `/home/vgpnk/Projects/shokunin/chousa-shokunin`, tip
`178667dc2c9d1656e864abfdc251c68757428613` (`git -C lane rev-parse HEAD`), L1 integration `447cf7e`. Scratch
`/fast/scratch/hyaku/chousa-r54/R54W2ExecQualityChecks` (removed at exit), `TMPDIR` and
`PYTHONDONTWRITEBYTECODE=1` exported; no network, no tool install, `shokuknow` read-only. Every line below is a
command I ran or a file:line I opened; outputs are pasted here (these receipts are retained in this file).
## Table

| # | check command (as the criterion states it) | ran output | red-before reproduced? | matches the criterion's text? |
|---|---|---|---|---|
| 97 | per-anchor: `python3 tools/capture-text.py <raw> --locate '<quote>'` prints `LOCATED count=1 offset=N`, N = stated `char N` (manual, not a counter) | 9/9 anchors `count=1`; stated `char`s match **0/9**; S101 form 27,012 chars / 0 U+FFFD / 0 ctrl | **yes** (0/6 S101, 0/3 S100; decode 64,512 / 263 U+FFFD; `.txt` −1 ×9; `build-spans.py:107-113` still decodes) | **no** — 3 numeric/text defects (F1–F3) |
| 98 | `python3 corpus/evidence/round54/c1-count.py --tool <candidate> --seed N --per-leg 2` | forge: 5/5 hooked legs `rc=97 AUDIT_FORBIDDEN`, `LEGS=0/6 C1=FAIL` exit 1; landed tool: `REAL=PASS 5 captures`, `LEGS=6/6 C1=PASS` exit 0 | **yes** (both arms) | **no** — 2 citation defects (F4–F5); refs `:70-76/:114/:244-256/:259-278`, `round52/c1-count.py:215` verified |
| 99 | `python3 corpus/evidence/round50/wave-complete-check.py .ufo/waves/round-53/w2-spec.json .ufo/waves/round-53/w2 --rev d21eb285 --lane .` + print marker/results | `OK 0/43 reports present …` **exit 1**; r53 W1 marker 2 lines / 49 ids / `2026-10-26T21:03:41` + `w1-results` seats=49 results=49; r53 W2 marker+results **absent**; report "W2: 43 seats dispatched" | **yes** | **yes** |
| 100 | `python3 corpus/evidence/round54/c2-count.py [--lane-only]` prints `HELD_CITED=<id> HELD_BAD=0` only when cited+`used-by` agree | lane: `C2=PASS` exit 0 with `HELD_CITED=- HELD_BAD=0`; scratch A/B/C = `-/1/2`, `S101/0/0`, `-/1/2`; TOOLED `BOUND=3/3 … HELD_BAD=1 … REF_ID_UNBOUND=3` | **yes** (A/B/C and TOOLED exact) | **no** — check vacuous at the tip (F6) |
## 97 — ran

```
$ python3 -c  raw decode 6dc68fd6…raw: chars 64512  U+FFFD 263  C0 18451 (excl tab/LF 18431; excl tab/LF/CR 18242); 0x0B=243, CR=189
$ python3 tools/capture-text.py 6dc68fd6b32ce9c8dfcebce8.raw → 27012 chars, U+FFFD 0, ctrl 0 (all <0x20 = 469 newlines)
$ python3 tools/capture-text.py <raw> --locate '<q>'        (the SCORECARD "Round 54 pointer corrections" anchors)
  S101 11170→11972  11205→12007  11993→12795  12161→12963  13247→14049  34374→25123   (count=1 ×6; .txt find=-1 ×6)
  S100 1296→16      1431→151    2843→492                                             (count=1 ×3; .txt find=-1 ×3)
$ per quote: raw.decode("utf-16-le").find(q) == stated char → True ×9, count 1 ×9 (the anchors index the decode)
$ import build-spans: bs.raw_form(raw) == utf-16le decode → True; == tool form → False; def at :107-113
$ (cd lane && python3 corpus/evidence/round53/pointer-anchor-check.py) → ANCHORED=16/16 UNANCHORED=0 BAD=0 exit 0
```

Red-before: the Registry rows still state the decode offsets — S101 "located quotes char 11170, 11205, 11993,
12161, 13247, 34374" in the form "(UTF-16LE text of the raw .doc capture)" (`corpus/SOURCES.md:111`), S100
1296/1431/2843 (`:110`); `--locate` gives 0/6 and 0/3. The `.txt` sidecar holds none of the nine.

- **F1 (97, the check still fails on its own subject).** Applied literally to "a Registry row", S101 is 0/6 and
  S100 0/3 at the tip: the re-point landed only as append-only text (nine `correction:` lines,
  `SCORECARD.md:2740-2748`, 16/16 anchored; the lesson's `## Mistakes` row 2 values also match 9/9). The
  criterion's limit ("the six S101 anchors stay wrong until the correction rows land") is met outside the row,
  but the row itself still names the undefined form and the old numbers.
- **F2 (97, number differs).** "18,242 control characters" (`corpus/QUALITY.md:937`) is not reproducible under
  the vocabulary the same criterion uses for the defined form (tab/newline allowed → 0): the decode has **18,451**
  C0 code points, **18,431** excluding tab/LF, and 18,242 only if CR is excluded too (189). No CR survives in the
  defined form, so the exclusion is unstated and form-specific.
- **F3 (97, listing/drift differs).** The criterion lists located `11,972 / 12,007 / 12,963 / 12,795 / 14,049 /
  25,123` positionally against stated `11,170 / 11,205 / 11,993 / 12,161 / 13,247 / 34,374` with "drift +802,
  +802, +970, +634, +802, −9,251". Ran: `11993→12795`, `12161→12963` — all five drifts are **+802**, and the
  third/fourth offsets are transposed in the criterion's prose. SCORECARD and the tool agree; the conclusion
  "no constant repairs an old anchor" still holds.
## 98 — ran

```
$ python3 corpus/evidence/round54/c1-count.py --tool delegate.py --seed 97 --per-leg 2 --work $PWD/w-forge
tool=…/delegate.py sha256=55ffaca64492f4e513c4b25695b5854c03c320148b925a788b34fcd3475af845 seed=97 per-leg=2
GEN=FAIL ggen0.doc rc=97 b'AUDIT_FORBIDDEN subprocess.Popen\n'  NONWORD=FAIL x0.xls rc=97 …  ENCRYPTED=FAIL genc0.doc rc=97 …
MALFORMED=FAIL gmal0.doc rc=97 …  REAL=FAIL 54fe0734c01f699e735b4b0a rc=97 …  REGRESS=FAIL r52 ['LEGS=1/9'] ['SUPPLEMENT_LEGS=0/4']
LEGS=0/6  C1=FAIL  exit=1   (4.5 s)
$ python3 corpus/evidence/round54/c1-count.py --seed 97 --per-leg 2 --work $PWD/w-honest
tool=…/tools/capture-text.py sha256=2c0140bc04029c8faedc6c89a65bd657430d8b85f433406946567b70303e2573
GEN=PASS 2 docs  NONWORD=PASS 2 sheets  ENCRYPTED=PASS 2 docs  MALFORMED=PASS 2 docs  REAL=PASS 5 captures
REGRESS=PASS r52 ['LEGS=9/9'] ['SUPPLEMENT_LEGS=4/4']  LEGS=6/6  C1=PASS  exit=0
$ python3 corpus/evidence/round54/c1-count.py --per-leg 1 → exit 2 "usage: --per-leg must be at least 2 (sample-size guard)"
```

- **F4 (98, text mismatch).** "the SHELL control's receipt says the same" (`QUALITY.md:939`) is false: the
  committed `controls/c1-controls.txt` SHELL block prints `NONWORD=PASS 3 sheets` and `MALFORMED=FAIL gmal0.doc
  rc=2 err=b'REFUSED ole-not-word: no WordDocument name\n'` — it keys refusals on a byte check before rendering,
  so it does not fail "every hooked leg". My unconditional delegator does (5/5 `rc=97`), which is what the Check
  sentence describes.
- **F5 (98, uncommitted receipt).** The "Shown able to fail" forge digest `9c8def9b…` appears only in the W1
  working record (`.ufo/waves/round-54/w1/R54DraftQuality.md:14,49,54` and its `w1-results.json:76`; `grep -rn
  9c8def9b` → those plus `QUALITY.md:939`) and in **no** `corpus/evidence/` receipt; the committed control digests
  are `e53423bd…` (SHELL) and `f73ac5c3…` (rebuilt forge). The class reproduces (mine `55ffaca6…`); the named
  receipt does not exist.
## 99 — ran

```
$ python3 corpus/evidence/round50/wave-complete-check.py .ufo/waves/round-53/w2-spec.json .ufo/waves/round-53/w2 --rev d21eb285 --lane .
MISSING R53W2ExecC1Target … MISSING R53W2ExecAdopterBoundary
OK 0/43 reports present in …/.ufo/waves/round-53/w2@d21eb285        exit=1
$ markers: r53 w1.ready.dispatched 1983 B, 2 lines, 49 ids, 2026-10-26T21:03:41; w1-results.json seats=49 results=49
           r53 w2.ready 154 B; w2.ready.dispatched ABSENT; w2-results.json ABSENT
           r54 w1.ready.dispatched 49 ids 22:40:28 + w1-results 49/49; r54 w2.ready.dispatched 38 ids 23:43:50; w2-results.json ABSENT
$ .ufo/reports/round-53/chousa.md:14 → "W2: 43 seats dispatched"
$ .scratch/goal-20261026-hyaku-run9.md:126 → "w2.ready orphaned - L1 exited before dispatcher marked wave"
```

All four values match the criterion's text. Its draft-time note is superseded: round-54 W1 now has the marker
(49 ids) and `w1-results.json` (49/49), `w1.ready.partial` is gone, and W2 has its 38-id marker with no results
yet (in flight).
## 100 — ran

```
$ python3 corpus/evidence/round54/c2-count.py     → C2=PASS exit 0: ENTRIES=2/2, HELD_CITED=- HELD_BAD=0,
   BOUND=3/3, REF_ID_UNBOUND=0, QUOTE_ROWS=33 ON_BOUND=33/33, SPAN_IDS=3/3, 33/33 in span/entry/lesson,
   QUOTE_SHORT=33/33, SPAN_CONTEXT=33/33, CAPTURE_BOUND=33/33, SUBSTANCE=PASS, ANCHOR_BOUND=3/3,
   INFERENCE_GROUNDED=2/2, QUARANTINE_VERDICTS=3/3 (S080,S088,S096)
$ … --lane-only                                   → C2=PASS exit 0 (CAPTURE_BOUND=skipped)
$ scratch root = lane SOURCES.md copy + corpus/knowledge/source-type-taxonomy-r37.md = "source: <id> — <HIT url>", --lane-only
  A used-by unchanged, source: S101 → HELD_CITED=- HELD_BAD=1    REF_ID_UNBOUND=2  C2=FAIL  exit=1
  B used-by cell += the entry      → HELD_CITED=S101 HELD_BAD=0  REF_ID_UNBOUND=0  C2=FAIL
  C B + "source: S090 — <url>"     → HELD_CITED=- HELD_BAD=1    REF_ID_UNBOUND=2  C2=FAIL
$ python3 corpus/evidence/round54/controls/build-c2-controls.py
  STAGED  HELD_CITED=- HELD_BAD=1 BOUND=0/3 REF_ID_UNBOUND=6 C2=FAIL
  TOOLED  BOUND=3/3 (min 2) HELD_CITED=- HELD_BAD=1 REF_ID_UNBOUND=3 C2=FAIL   (adopter exit=0, COLLISIONS=39)
$ corpus/SOURCES.md:111 cell 10 = " corpus/knowledge/citation-count-semantics-r37.md "
```

**F6 (100, check vacuous at the tip).** Erratum E3 cut the r37 entry's S101 leg, so no entry carries `source:
S101 — <HIT url>`; the counter's held loop sees no citing entry and prints `HELD_CITED=- HELD_BAD=0`, not
`HELD_CITED=<id> HELD_BAD=0`, and the lesson records the cell **unchanged** (`corpus/lessons/round-54.md:45`
"S101's `used-by` is therefore unchanged"; `:111` "no existing row touched (S101 `used-by` unchanged)"). The
clause "the lesson records the cell's change old→new" is unsatisfiable on the landed round, and `HELD_BAD=0`
is vacuous rather than earned; only a scratch root (A/B/C above) exercises the check, exactly as the
criterion's red-before states.
## Risks / notes
- 97's `build-spans.py:107-113` state is still live (a span from an OLE `.doc` would index the decode); no
  round-54 span touches S101, so C2 is unaffected — the criterion names this as a limit.
- 98's oracle is one LibreOffice 26.8.1.1; REAL's pass is version-bound (`ENV_CHANGED` otherwise).
- No tool installed or upgraded (pacman paused; none needed). Files written: this report only. Lane,
  `shokuknow` and fleet writes: none. Scratch removed; these runs left no `__pycache__` in the lane
  (`find -newermt -90 minutes` → none), and the live `soffice` processes are `R54W2MutSupplement`'s.

VERDICT: attacked all four new criteria by re-running their checks on tip `178667dc` — 99 matched its text and
all four red-befores reproduced (97: 0/6+0/3 anchors, 64,512/263 decode vs 27,012/0/0 form; 98: forge `LEGS=0/6`
rc=97 vs landed `LEGS=6/6`; 99: `OK 0/43` exit 1, W1 49/49 marker+results, W2 neither; 100 A/B/C `HELD_CITED
-/S101/-`), but 97's control count (18,242 vs 18,431), its offset order/drifts (`+970/+634` vs `+802/+802`) and
its Registry-row subject (still 0/9), 98's SHELL-receipt and forge-digest-receipt sentences, and 100's vacuity
under E3 do not match the criteria's own text.
