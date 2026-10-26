# R52W2MutSupplement — mutation test of the post-freeze C1 supplement

Seat: R52W2MutSupplement · role: mutation tester (godspeed) · lane: chousa r52 w2 (falsify).
Attacked: `corpus/evidence/round52/c1-supplement.py` (post-freeze, erratum E1–E4), the
4-leg C1 supplement that re-spells OOXML packages and re-checks the pinned NIPH text form.

## Setup (all scratch, bounded)
The supplement `import`s `c1-count.py` from its own directory (`HERE / "c1-count.py"`),
so each mutant clone got its own copy of both files. Scratch root
`/fast/scratch/hyaku/chousa-r52/R52W2MutSupplement/`; `TMPDIR` exported there; `--work`
passed to the supplement; no lane file was ever written. Controls run by absolute path
from the lane (`controls/forge-shape.py`, `controls/naive-tool.py`), real tool
`tools/capture-text.py`.

Baseline hashes (lane originals, unchanged after all runs — restoration evidence):
```
86711a5f…c0109b0  c1-supplement.py
4ec29333…e101cbaa  c1-count.py
03fd0d3c…253f743  controls/forge-shape.py
51b11350…b811230  controls/naive-tool.py
```

## Mutants (one per leg; each = one behavioral-point change in the scratch clone)
| tag | change | base lines |
|---|---|---|
| M1 | PREFIX: `respell_prefixes` renames nothing (returns xml) | 67–84 |
| M2 | RELS_FORM: drop `g.r.shuffle(attrs)` — attribute order kept | 121 |
| M3 | SYNTAX: no `<!-- … -->` comment, no CDATA branch (decimal refs kept) | 91–93,95 |
| M4 | REAL_TEXT: drop sha256, keep only `len(txt)==TEXT_CHARS` | 165 |
| M5 | default-namespace branch never taken (`default_w = False`) | 69 |
| M6 | `respell_package` skips the decoy part (respells only the `_rels/.rels` officeDocument target) | 103–114 |

M1–M6 verified by `diff -u base mutant` showing exactly those hunks.

## Matrix (each run: `c1-supplement.py --tool <tool> --seed 52 --work $S/work`; seed fixed)
```
variant     real (must PASS)  forge (must FAIL)  naive (must FAIL)
base        4/4 rc=0          0/4 rc=1          0/4 rc=1
M1 PREFIX  4/4 rc=0          1/4 rc=1          0/4 rc=1
M2 RELS    4/4 rc=0          0/4 rc=1          0/4 rc=1
M3 SYNTAX  4/4 rc=0          0/4 rc=1          0/4 rc=1
M4 REAL    4/4 rc=0          0/4 rc=1          0/4 rc=1
M5 defNS   4/4 rc=0          0/4 rc=1          0/4 rc=1
M6 decoy   4/4 rc=0          0/4 rc=1          0/4 rc=1
```
All six mutants: real tool still 4/4 PASS (no mutant broke the generator's contract);
forge and naive still fail (detection intact). Full per-leg lines:

base vs forge: `PREFIX=FAIL g_paras: text differs at 10 (got 96, want 101)` ·
`RELS_FORM=FAIL g_paras: rc=2` · `SYNTAX=FAIL g_paras: rc=2` ·
`REAL_TEXT=FAIL rc=0 chars=21`.
base vs naive: `PREFIX=FAIL g_paras: text differs at 10 (got 96, want 101)` ·
`RELS_FORM=FAIL g_revisions: text differs at 14 (got 130, want 57)` ·
`SYNTAX=FAIL g_paras: text differs at 26 (got 26, want 129)` ·
`REAL_TEXT=FAIL rc=0 chars=21910`.
M1 vs forge: `PREFIX=PASS ok` — the ONLY leg that flips to PASS when neutered; the rest
still fail (`RELS_FORM=FAIL rc=2`, `SYNTAX=FAIL rc=2`, `REAL_TEXT=FAIL chars=21`) ⇒
overall still FAIL.
M1 vs naive: still `PREFIX=FAIL g_revisions: text differs at 14 (got 176, want 87)` —
naive fails even unrespelled revisions (delText/instrText/tabs leaks), so PREFIX stays
killed against naive through content, not prefix.
M2 vs forge: `RELS_FORM=FAIL rc=2` — attribute-order shuffle is NOT the killer; the
element-prefix rename (`<p:Relationship>`) and whitespace variants are. Naive was and
remains unaffected by rels (it reads fixed `word/document.xml`).
M3 vs forge: `SYNTAX=FAIL rc=2` — the leg also respells `_rels/.rels` (rels=True), so
forge dies at the rels regex, not at comments/CDATA; paired `<w:tab></w:tab>` and typed
`<w:br w:type="page" />` still kill naive (M3 naive `SYNTAX=FAIL g_paras: text differs
at 26 (got 124, want 129)`).
M4: char-count alone catches forge (chars=21) and naive (chars=21910); the sha256
component is not exercised by either control (both fail on length).
M5: plain prefix rename already breaks forge/naive; default-ns variant never needed. It
was live in baseline: probe over 200 seeds fired `xmlns="…wordprocessingml/2006/main"`
94×, so M5 really removes a taken branch; the real tool passes with or without it
(capability test, not a killer).
M6: confirmed by content probe — `main_respelled=True, decoy_respelled=False` for M6
vs `True,True` for base (seeds 52/7/1234). No detector reads the decoy as authoritative
(real & forge follow rels target; naive reads `word/document.xml`, which is just the
wrong-text decoy), so verdicts unchanged.

## Leg verdicts (load-bearing vs decorative)
- PREFIX (M1): **load-bearing for its own leg** — neutering it is the only change that
  lets the forge PASS a leg; redundant overall because RELS_FORM/SYNTAX/REAL_TEXT still
  kill forge, and naive is killed here via revision content regardless.
- RELS_FORM (M2): the **attribute-order shuffle is decorative** vs forge (prefix rename
  kills it); the leg itself is what catches forge on rels shape.
- SYNTAX (M3): **comment/CDATA insertion is decorative**; paired tab/br, typed br and the
  rels respell carry the detection.
- REAL_TEXT (M4): **sha256 is decorative** against both controls (char count alone fails
  them); it is the only guard vs a stub padded to exactly 19682 chars.
- default-ns branch (M5): **decorative** vs controls; it only extends the real tool's
  namespace coverage (was exercised 94/200 seeds).
- decoy respell (M6): **decorative** — no detector reads the decoy; respelling the main
  part alone suffices.

VERDICT: attacked c1-supplement.py's PREFIX/RELS_FORM/SYNTAX/REAL_TEXT/default-ns/decoy
features with six single-point mutants — all six survive the real tool (4/4 PASS) and
stay killed by forge & naive, proving the four legs are mutually redundant; only PREFIX
is leg-load-bearing vs forge, and attr-order, comments/CDATA, sha256, default-ns and
decoy respell are decorative against these two controls.
