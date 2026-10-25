# R50MutLandedC2 — mutation test: landed C2 bytes vs frozen counter (round 50, wave 2)

Attacked: the landed C2 bytes — `corpus/knowledge/` cnki-citation-check-r40 /
citation-matching-semantics-r41 / istic-citation-verification-r39, `corpus/SOURCES.md`
(rows S104/S105/S106, refused-教师 decision), `corpus/lessons/round-50.md` (55-quote
manifest, refused-doc line), `corpus/evidence/round50/` (spans.tsv, 55 span files,
quote-substance-check.py) and `tools/` — against the frozen counter
`corpus/evidence/round50/c2-count.py --root <root>`. Lane untouched (read-only opens; the
counter's BASE_REV `git show`/`git grep` are reads). All writes under
/dev/shm/chousa-r50-R50MutLandedC2/ (deleted at end). Tooling authorization noted: nothing
installed, none needed; pacman paused host-wide, no other channel used.

## Baseline (pristine) — required pass
Scratch: `cp -a` of the lane files above into `$S/root` (first attempt flattened
`evidence/` because the dir did not pre-exist; rebuilt with `evidence/` pre-created, 108
files, spans.tsv sha aadcbf91e2680bb9…).

```
$ python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round50/c2-count.py --root /dev/shm/chousa-r50-R50MutLandedC2/root
ENTRIES=3/3
BOUND=3/4 (min 3) REFUSED=1
BOUND_IDS=S104,S105,S106
REF_ID_UNBOUND=0
NEW_GROUND=3/3
QUOTE_ROWS=55 ON_BOUND=55/55
SPAN_IDS=3/3 (min 3 each)
QUOTES_IN_SPAN=55/55
QUOTES_IN_ENTRY=55/55
QUOTES_IN_LESSON=55/55
QUOTE_SHORT=55/55
SPAN_CONTEXT=55/55
CAPTURE_BOUND=55/55
SUBSTANCE=PASS
ANCHOR_BOUND=3/3
INFERENCE_GROUNDED=3/3
QUARANTINE_VERDICTS=0/0 ()
QUARANTINE_BLOCKED_ADOPTED=0
C2=PASS
exit=0
```
Baseline passes, so mutant verdicts are judgeable.

## Protocol
Per mutant: rebuild root from the pristine byte copy → sha256 target file → apply the one
prescribed edit → run the counter → restore exact pristine bytes → sha256 again (must be
equal) → re-run counter on restored bytes (must print C2=PASS). Pristine hashes: SOURCES.md
69d92f33b26119bf…, r41 256865509b115ef9…, lesson ee87ec18d079b631…, spans/S104-1.txt
9f7fc217f7d785fe…. Final proof: `diff -rq pristine root` → empty, exit 0.

## Mutants — counter stdout lines that changed vs baseline (all: `--root $S/root`)
- **M1 S105 used-by loses one entry** (drops `, corpus/knowledge/cnki-citation-check-r40.md`):
  `BOUND=2/4 (min 3) REFUSED=1 ; BOUND_IDS=S104,S106 ; REF_ID_UNBOUND=22 ; ON_BOUND=21/55 ;
  SPAN_IDS=2/2 ; ANCHOR_BOUND=2/2` → **C2=FAIL exit=1 — KILLED** (used-by ≠ citing entries
  unbinds the SXU doc, c2-count.py:162-165).
- **M2 S106 opened date changed** (2026-10-25→2026-10-24): `BOUND=2/4 REFUSED=1 ;
  BOUND_IDS=S104,S105 ; REF_ID_UNBOUND=7 ; ON_BOUND=52/55` → **C2=FAIL exit=1 — KILLED**
  (`r[8] == OPENED` gate, c2-count.py:165).
- **M3 `source:` line removed from r41** (whole `source: S105 — https://gs.sxu…` line):
  `BOUND=2/4 REFUSED=1 ; BOUND_IDS=S104,S106 ; REF_ID_UNBOUND=21 ; ON_BOUND=21/55` →
  **C2=FAIL exit=1 — KILLED** (`cites` requires the line in every citing entry, :163-164).
- **M4 quote edited by one character in the lesson only** (first listing of the first
  manifest quote, `論` for its leading `论`): no leg changed → **C2=PASS exit=0 — SURVIVOR.**
  The quote occurs twice in the lesson (count=2) and the leg is an existence check —
  `in_lesson += bool(quote and quote in lesson)` (c2-count.py:197) — so one intact duplicate
  masks the corrupted site. Diagnostic M4b (both sites corrupted): `QUOTES_IN_LESSON=53/55` →
  C2=FAIL (53 not 54: the adjacent row's quote embeds the corrupted prefix, so two rows fail).
  Coverage finding: the lesson leg tolerates any single-site corruption of a twice-listed quote.
- **M5 span file edited by one character** (spans/S104-1.txt first char swapped):
  `CAPTURE_BOUND=54/55` → **C2=FAIL exit=1 — KILLED.** QUOTES_IN_SPAN stayed 55/55: the edit
  sits in the 80-char context margin, quote substring intact; only the capture-digest leg
  binds margin bytes.
- **M6 `refused-doc` line removed** (lesson's only `refused-doc:` line, the BNU 教师 manual):
  `BOUND=3/4 (min 3) REFUSED=0` → **C2=FAIL exit=1 — KILLED** (nbound+refused=3 ≠ 4 docs;
  the fourth document vanishes from both sides of the ledger).
- **M7 extra S-token added to an entry** (` (staged S118)` appended inside r41's S105 source
  line — S118 is a lane row of another document, the exact copy-staged-bytes defect):
  `REF_ID_UNBOUND=1` → **C2=FAIL exit=1 — KILLED** (only this leg fired; inference-ground did
  not flag the dangling token).
- **M8 tier of S106 set to community** (`| docs | B |` → `| docs | community |`): no leg
  changed → **C2=PASS exit=0 — SURVIVOR.** The counter reads Registry cells r[0] (:144,165),
  r[1] (:159), r[5] (:215), r[7]=="mined" and r[8]==OPENED (:165), r[10] (:162); `r[3]`
  (tier) appears nowhere — grep of c2-count.py for `tier`/`r[3]`: no match. Coverage finding:
  C2 never asserts tier; tier lives in the QUALITY admission path, not this count.
- **M9 Registry row of S104 moved outside `## Registry`** (row re-inserted under `## Paths`):
  `BOUND=2/4 REFUSED=1 ; BOUND_IDS=S105,S106 ; REF_ID_UNBOUND=14 ; ON_BOUND=37/55` →
  **C2=FAIL exit=1 — KILLED** (`registry()` ignores rows outside the Registry section; ISTIC
  unbinds and its entry token turns unbound).

## Scoreboard
9 mutants: 7 killed, 2 survived (M4 single-site lesson-quote corruption; M8 Registry tier
cell). Both survivors are coverage findings about the frozen counter; per assignment the
contract (claims.md predicates) is unchanged and no lane byte was altered. Restoration:
every target sha before == after; restored detector re-run printed C2=PASS exit=0 for all 9;
whole-tree `diff -rq` pristine vs root empty at close. Scratch deleted.

VERDICT: attacked the landed C2 bytes with the 9 prescribed mutants against the frozen counter — 7 killed; 2 SURVIVED (coverage findings): a one-char corruption of a single listing of a twice-listed lesson quote passes the QUOTES_IN_LESSON existence check, and the Registry `tier` cell is read by no C2 leg (S106 tier→community passes).
