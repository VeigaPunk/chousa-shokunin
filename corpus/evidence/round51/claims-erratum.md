# Round 51 — claims erratum (chousa)

author: chousa L1 (`ChousaR51`) · date: 2026-10-25 · append-only; `claims.md` is not edited.

## E1 — C3 extractor stripped a leading dot (found before any wave seat existed)

Freeze: lane commit `d603f6f00f78d64f123d3aed2dd9f8701547a4ba` (`corpus/evidence/round51/claims.md`).
Found by the L1, reading the eight `DANGLING` lines while preparing the wave context, before the
wave-1 `.ready` file was taken (dispatcher log: `cap-defer …/round-51/w1.ready` at 20:05:10; no
`w1.ready.dispatched` marker, no seat registered, no seat had scored anything).

`c3-count.py` pointer extraction applied `str.strip(",;.:()")`, which removes a LEADING dot too, so
`.ufo/waves/round-34/measure/` (SCORECARD.md:1973), `.ufo/waves/round-34/measure-a2/` (:1974) and
`.ufo/waves/round-25/build/ConnectorMetaSiblings.md` (SHONEN.md:12) were read as `ufo/waves/...`
and printed `DANGLING`. Those three exist; they are false positives of the counter, not
self-assessment drift. The extraction now strips `,;:()` at both ends and only a trailing `.`
(`tok.strip(",;:()").rstrip(".")`). The predicate sentence in `claims.md` does not mention
extraction and is unchanged; the docstring's extraction clause is corrected. The target
(`DANGLING=0`, `CAP_ROWS>=36`, `POINTERS>=74`) is unchanged.

Effect on the before-state: `DANGLING=8` → `DANGLING=5` (SCORECARD.md:1843 2073 2074 2616;
SHONEN.md:10). `CAP_ROWS=36`, `POINTERS=74` unchanged. Receipts: `controls/c3-before-erratum.txt`,
`controls/c3-controls-erratum.txt` (all three controls still `C3=FAIL`: BLANKET `DANGLING=5`, DELETED
`CAP_ROWS=32`, EMPTY `DANGLING=5`); the originals `controls/c3-before.txt`, `c3-controls.txt` stay as
filed. The before-count the report quotes is 5; the 8 is the first run of a counter with this defect.

The class is a mined mistake (`vacuous`/counter-defect: a counter's own tokenizer made drift that was
not there; captured by none — C3's controls all fail by construction and none seeds a
dot-leading path) — see `corpus/lessons/round-51.md` `## Mistakes`.

## E2 — the frozen C1 counter can hang (found by wave 1, `R51ExecSeedRuns`)

`c1-count.py` redraws only the third id when the first two collide, so seeds 13, 182 and 324 never terminate (about 1/401 per run). Not changed (the freeze stands); `c1-supplement.py` draws distinct ids and runs the frozen counter only with a seed that does not collide (`safe_seed`, corrected in W2 after `R51W2ExecSeedSupplement` found it screened the wrong draw).

## E3 — the frozen C1 counter inherits an ambient `ASSIMILATE_CITES` (wave 1 `R51SentScope` H5)

`ASSIMILATE_CITES=all python3 corpus/evidence/round51/c1-count.py` → `LEGS=3/5 C1=FAIL`. Not changed; run it as `env -u ASSIMILATE_CITES python3 …`; the supplement scrubs the variable from the tool's environment.

## E4 — the round-50 echo and const controls delegated to the lane tool

At the base the lane tool was the base tool, so the before receipts are right; at the tip the echo control scored `LEGS=5/5`. The round-51 copies delegate to `controls/tool-before.py` (QUALITY 85).

## E5 — controls and supplements changed after the freeze

`controls/build-c3-controls.py` (BASE-derived negative controls, DOTPATH positive control; `controls/c3-controls-final.txt`), `controls/build-c2-controls.py` unchanged since the freeze; `c1-supplement.py`, `receipt-check.py`, `open-items-age.py` and the controls `forge-dirname.py`, `forge-dual.py`, `tool-candidate1.py`, `tool-v2.py` are post-freeze additions. The frozen predicates, counters (`c1-count.py`, `c2-count.py`; `c3-count.py` only by E1) and targets are unchanged: `git diff d603f6f00f78d64f123d3aed2dd9f8701547a4ba HEAD -- corpus/evidence/round51/c1-count.py corpus/evidence/round51/c2-count.py corpus/evidence/round51/claims.md` is empty.
