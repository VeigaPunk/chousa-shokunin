# R54 W2 — C1 after-state attacker (`R54W2ExecC1Target`)

Leaf executor, no dispatch (no spawn tool mounted; **no labrat dispatched**), no tool installs (python3 + the lane's
counters + system `soffice` sufficed; no pacman/uv/npx run). Scratch removed at exit; `PYTHONDONTWRITEBYTECODE=1` throughout.

## 1. Object under attack
```
$ sha256sum tools/capture-text.py
2c0140bc04029c8faedc6c89a65bd657430d8b85f433406946567b70303e2573  tools/capture-text.py
$ git show 447cf7ed4dc1a3708518b99e9a5e62e177c11ce9:tools/capture-text.py | sha256sum
2c0140bc04029c8faedc6c89a65bd657430d8b85f433406946567b70303e2573  -
$ git diff --stat 447cf7e 178667d -- tools/capture-text.py    # lane HEAD while I ran → (empty)
```
E2 comparison candidate: `git show 8a7d0f1:tools/capture-text.py` → sha256
`fd0ed3f58565b781ab8eedaad5d229976e150bdd8e391a2b0cacd0a0825fcd89`.

## 2. Frozen counter — 3 unseeded + `--seed 7`, every leg line pasted
Header on all four runs: `tool=/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/capture-text.py
sha256=2c0140bc04029c8faedc6c89a65bd657430d8b85f433406946567b70303e2573 seed=<n> per-leg=3`.
```
seed=589305729  GEN=PASS 3 docs                        NONWORD=PASS 3 sheets
ENCRYPTED=PASS 3 docs                                  MALFORMED=PASS 3 docs
REAL=PASS 5 captures                                   REGRESS=PASS r52 ['LEGS=9/9'] ['SUPPLEMENT_LEGS=4/4']
LEGS=6/6                                               C1=PASS   exit=0
seed=540763334  GEN=PASS 3 docs                        NONWORD=PASS 3 sheets
ENCRYPTED=PASS 3 docs                                  MALFORMED=PASS 3 docs
REAL=PASS 5 captures                                   REGRESS=PASS r52 ['LEGS=9/9'] ['SUPPLEMENT_LEGS=4/4']
LEGS=6/6                                               C1=PASS   exit=0
seed=280565567  GEN=PASS 3 docs                        NONWORD=PASS 3 sheets
ENCRYPTED=PASS 3 docs                                  MALFORMED=PASS 3 docs
REAL=PASS 5 captures                                   REGRESS=PASS r52 ['LEGS=9/9'] ['SUPPLEMENT_LEGS=4/4']
LEGS=6/6                                               C1=PASS   exit=0
seed=7  GEN=PASS 3 docs                                NONWORD=PASS 3 sheets
ENCRYPTED=PASS 3 docs                                  MALFORMED=PASS 3 docs
REAL=PASS 5 captures                                   REGRESS=PASS r52 ['LEGS=9/9'] ['SUPPLEMENT_LEGS=4/4']
LEGS=6/6                                               C1=PASS   exit=0
```
No leg failed, no `ENV_CHANGED`, stderr empty on all four; no non-6/6 run existed to reproduce.

## 3. Post-freeze supplement — 3 unseeded + `--seed 7` (same header)
```
seed=215224194  ISOLATED=PASS 3 docs  RESAVE=PASS 5 resaved captures  HELDOUT=PASS 3 lane files  SUPPLEMENT_LEGS=3/3  SUPPLEMENT=PASS  exit=0
seed=248277883  ISOLATED=PASS 3 docs  RESAVE=PASS 5 resaved captures  HELDOUT=PASS 3 lane files  SUPPLEMENT_LEGS=3/3  SUPPLEMENT=PASS  exit=0
seed=144033993  ISOLATED=PASS 3 docs  RESAVE=PASS 5 resaved captures  HELDOUT=PASS 3 lane files  SUPPLEMENT_LEGS=3/3  SUPPLEMENT=PASS  exit=0
seed=7          ISOLATED=PASS 3 docs  RESAVE=PASS 5 resaved captures  HELDOUT=PASS 3 lane files  SUPPLEMENT_LEGS=3/3  SUPPLEMENT=PASS  exit=0
```
The audit hook is provably live here: a scratch tool doing `subprocess.run(["true"])` gives `LEGS=0/6`,
`REGRESS=r52 ['LEGS=0/9'] ['SUPPLEMENT_LEGS=0/4']`, every leg `rc=97 b'AUDIT_FORBIDDEN subprocess.Popen\n'`.

## 4. E2 disclosure audit — `git diff 8a7d0f1 447cf7e -- tools/capture-text.py` (61+/3−)
| hunk | behaviour change | disclosed in E2? |
|---|---|---|
| docstring 34-37 | tracked deletion emits nothing; insertions + hidden emitted | yes ("drops runs carrying sprmCFRMarkDel"; "Hidden text stays emitted in both forms") |
| `import bisect`; `fc_bte,lcb_bte` at pos+12*8; `deleted_runs`; `marks_deleted` | reads PlcBteChpx CHPX FKP pages, sprm 0x0800 operand ∈ {1,0x81} | yes in substance ("reads the CHPX FKP pages of the PlcBteChpx") — **two new refusal strings unnamed** (F2) |
| Clx walk `cb_grpprl < 0 or i+3+cb > len(clx)` | malformed Prc refused instead of hang/Traceback | yes, message quoted verbatim in E2 |
| piece loop `live(off+x)` / `live(fcv+2*x)` | deleted FKP runs excluded from compressed and UTF-16 pieces | yes ("drops runs") |

**Answer: yes — every change is disclosed at the level of what changes**, with one gap: the CHPX walk adds two
`ole-malformed` refusal paths E2 never names, and they refuse documents the candidate printed (F2). The two
silent-degradation edges are unmentioned too (F4).

## 5. Mechanism claims re-derived, not trusted
- **Tracked deletion (E2: candidate FAIL, landed PASS).** Run myself: landed `TRACKED_DELETION=PASS` →
  `'alpha INSERTEDTEXT bravo charlie\nvisible HIDDENTEXT end 中文删除测试\n第二 保留\n'`; candidate
  `TRACKED_DELETION=FAIL` → `'… bravo DELETEDTEXT charlie\n… 第二 删除的中文保留\n'`. Insertion + hidden
  emitted, both deletions (ASCII and CJK) dropped, on `.doc` and `.docx`.
- **"Five pinned captures byte-identical before and after."** Both tools on each `.raw`: `cmp` identical YES ×5
  (sha256 prefixes `7dbf2a21…`, `7dbf2a21…`, `a8e3e7ad…`, `70ca0f0d…`, `f0b08997…`). E2 holds.
- **"No frozen leg reaches the Clx walk."** Parsed fcClx/lcbClx of every frozen OLE document: five pinned captures
  and the six generated GEN/ENCRYPTED docs all `prc_entries=0 next=0x02`; MALFORMED docs refuse at the sector
  check; round-52 legs are OOXML/raw only (no OLE magic in `round52/c1-*.py`). Verified — while the **CHPX** walk
  *is* reached by every GEN doc (`lcbBteChpx=12`), so the tracked half runs, never with a deletion.

## 6. Findings
**F1 (medium — evidence gap, disclosed for only half of E2).** The after-measurement cannot discriminate the landed
tool from the candidate: `c1-count --tool cand-tool.py --seed 7` → `LEGS=6/6 C1=PASS exit=0`; `c1-supplement --tool
cand-tool.py --seed 7` → `SUPPLEMENT_LEGS=3/3 SUPPLEMENT=PASS`. Both E2 changes are invisible to the claim rule
*and* the supplement: no frozen document carries a deletion (five pinned + six generated all `deleted_runs=0`) and
none carries a Prc (§5). E2 admits the blindness for the Clx fix only; the tracked-deletion fix is equally
unmeasured, and only the non-claim `tracked-deletion-check.py` (one fixture) sees it. So `C1=PASS` at the tip is
evidence about the candidate's capability, not the tip's E2 semantics.

**F2 (low — undisclosed narrowing).** `deleted_runs` adds `REFUSED ole-malformed: PlcBteChpx outside the table
stream` and `… CHPX FKP page outside WordDocument`. One-word FIB patch (lcbPlcfBteChpx := 0x7FFFFFFF): candidate
`rc=0` and printed the whole story; landed `rc=2`, stdout empty, `REFUSED ole-malformed: PlcBteChpx outside the
table stream`, no Traceback. Unreachable by any frozen leg (§5), so the claim is unharmed, but E2 should name the
widened refusal surface.

**F3 (low — E2's Clx half has no lane fixture).** Nothing in the lane exercises the Clx bound
(`corpus/fixtures/capture-text-ole/` holds only `tracked.doc`, `tracked.docx`). Rebuilt in scratch: `tracked.doc`'s
Clx (`0210…`, unique at file offset 2732), byte 0 → 0x01, `cbGrpprl` := −3 → candidate hangs (>10 s, killed),
landed `rc=2 REFUSED ole-malformed: Prc GrpPrl outside the Clx`; := −32768 → candidate `rc=1` + `Traceback`, landed
the same clean refusal; := 1000 → both refuse. E2's F1 account is accurate, just unverifiable from lane bytes.

**F4 (informational — silent degradation).** `lcbPlcfBteChpx=0` and a garbage BTE page (fc := len(table)−12,
lcb := 12) both give `rc=0` with `DELETEDTEXT` printed, no refusal. The docstring's unconditional "a tracked deletion
emits nothing", and the `.docx` form's `w:delText` drop, therefore diverge on such a file.

**F5 (note — predicate entailment; nothing to change).** With E2 landed, the frozen C1 predicate's "every paragraph,
table-cell and hyperlink-anchor text … appears exactly once" is literally false for a `.doc` carrying a tracked
deletion (its paragraph text is deliberately dropped). The measured after-state is untouched (no frozen document has
one), so `C1=PASS` stands; recorded as a claim-text entailment gap.

**E1's forgeability cap re-measured (confirmed).** Rebuilt the forge for real: `build-c1-forge.py` →
`sha256=f73ac5c33c233880e9e7a950bf14c14bf272e5bb80f84bc687f2bbbf2a45fa88` (byte-identical to the L1 receipt);
`c1-count --seed 7` → `LEGS=6/6 C1=PASS exit=0`; supplement `--seed 7` → `SUPPLEMENT_LEGS=0/3 exit=1`. Cap real.
**Robustness (mine, 200 mutants):** 200 one/two/three-byte mutants of `tracked.doc` over the WordDocument+table region
→ `{'ok': 197, 'REFUSED ole-not-word': 2, 'REFUSED ole-malformed': 1}`, no Traceback, no timeout, no exit outside {0,2}.

## 7. Not run / limits
- I did not re-run `build-c1-controls.py` (CONST/NAIVE/REFUSEALL/SHELL); scope was the after-state, the supplement and
  E2. The one control I did reproduce is the forge. No network or live fetch: every capture came from the read-only `.qcache`.
- Nothing in the lane touched: `git status --porcelain` shows no file of mine outside `.ufo/waves/round-54/w2/`;
  `tools/__pycache__/capture-text.cpython-314.pyc` is gitignored and predates this session (mtime `2026-10-26 23:15:44 -0300`).

VERDICT: attacked C1's after-state on tool sha256 `2c0140bc…` (= 447cf7e = HEAD) and it survived — 6/6 three times
unseeded and with `--seed 7`, supplement 3/3 on the same four, pinned-capture text forms byte-identical across the
E2 change, both E2 mechanisms independently reproduced (tracked-deletion drop; Prc bound turning a candidate
hang/Traceback into a clean refusal), E1's forgeability cap confirmed at `f73ac5c…` (6/6 counter, 0/3 supplement) —
with F1–F5 recorded: the after-measurement buys no evidence about either E2 change (candidate is also 6/6 and 3/3),
E2 leaves two new refusal strings and two silent-degradation edges unnamed, and the Clx half has no lane fixture.
