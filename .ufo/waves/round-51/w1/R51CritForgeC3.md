# R51CritForgeC3 — the C3 counter attacked (cheat matrix)

seat: critic, round 51 wave 1 · axis: calibration · claim: R51-C3 frozen at `d603f6f`
scope: `corpus/evidence/round51/c3-count.py` + the C3 sentence in `corpus/evidence/round51/claims.md`; lane read-only
tooling: nothing installed (no network, no pacman); scratch `/dev/shm/chousa-r51-R51CritForgeC3`, deleted

## Method

Tip `cfe6c9f`, lane untouched:

```
$ cd /home/vgpnk/Projects/shokunin/chousa-shokunin && python3 corpus/evidence/round51/c3-count.py; echo "exit=$?"
CAP_ROWS=36 (base 36)
POINTERS=74 (base 74)
RESOLVED_BY_CORRECTION=0
DANGLING SCORECARD.md:1843 measure/final/
DANGLING SCORECARD.md:2073 measure-l1/c1-s36361.json
DANGLING SCORECARD.md:2074 measure-l1/c2-s36371.json
DANGLING SCORECARD.md:2616 c1-supplement.py
DANGLING SHONEN.md:10 round25-meta-differential.log
DANGLING=5
C3=FAIL
exit=1
```

Five, not eight — the erratum's leading-dot fix (E1) is in the tip counter (`claims.md`'s Before bullet still says 8;
`controls/c3-before-erratum.txt` shows the 8 was the artefact). Each cheat ran in a fresh scratch root — every lane
entry symlinked **except** `SCORECARD.md`/`SHONEN.md` (copied) — via `c3-count.py --root <scratch>`; base counts come
from the lane repo, not `--root` (`:85-86`), so a cheat moves only the tip. 24 roots, all observed (W in the pair below):

```
cols: id rows/base ptrs/base corr dangling verdict | cheat
A  36/36 73/74 c0 d4 FAIL | unwrap-backtick (SHONEN.md:10)    B  28/36 66/74 c0 d5 FAIL | rename biggest Capabilities heading
C  36/36 73/74 c0 d4 FAIL | angle-span <measure/final/>       D  36/36 73/74 c0 d4 FAIL | bracket-span [c1-supplement.py]
E  36/36 74/74 c0 d5 FAIL | cell-move attempt (token stayed)   E2 36/36 73/74 c0 d4 FAIL | cell-move into cell 2
F  36/36 74/74 c4 d0 PASS | 4 corrections -> README.md         G  36/36 74/74 c4 d0 PASS | 4 corrections -> PROVINCE.md
H  36/36 74/74 c0 d4 FAIL | corrections at line 1              I  36/36 74/74 c4 d0 PASS | correction target is a dir (tools)
J  36/36 75/74 c0 d0 PASS | delete 5 dangling lines + 4 decoys  K  36/36 74/74 c0 d0 PASS | 1-byte files planted
L  36/36 74/74 c0 d0 PASS | wrap 5 tokens + 5 pad pointers      M  36/36 98/74 c0 d5 FAIL | rename heading + 8 decoy rows
N  36/36 74/74 c4 d0 PASS | corrections ABOVE the rows          O  36/36 74/74 c0 d4 FAIL | dir + zero-byte inner file
P  36/36 74/74 c0 d2 FAIL | symlinks to README.md               Q  32/36 82/74 c0 d5 FAIL | decoy rows in a fenced block
R  36/36 74/74 c0 d5 FAIL | demote Round-33 heading             S  46/36 80/74 c0 d6 FAIL | demote Round-37 (10 rows absorbed)
T  46/36 75/74 c0 d1 FAIL | S + 5 wraps                         U  46/36 74/74 c0 d0 PASS | 1 heading demotion + 6 wraps
V  36/36 74/74 c0 d0 PASS | rewrite 5 pointer strings, no correction line
```

## Decisive pair — the cheapest PASS prints exactly what the true repair prints

`V` replaces the five dangling strings with `PROVINCE.md`, `README.md`, `README.md`, `SKILL.md`, `PROVINCE.md` — five
substitutions, nothing repaired, no file created, no `correction:` line. `W` points the same five at the true on-disk
targets, which all exist (`.ufo/waves/round-32/measure/final`, `.ufo/waves/round-36/measure-l1/c1-s36361.json`,
`.../c2-s36371.json`, `corpus/evidence/round50/c1-supplement.py`, `corpus/evidence/round25-meta-differential.log`).
Byte-identical stdout:

```
V false retarget : CAP_ROWS=36 (base 36) POINTERS=74 (base 74) RESOLVED_BY_CORRECTION=0 DANGLING=0 C3=PASS exit=0
W true repair    : CAP_ROWS=36 (base 36) POINTERS=74 (base 74) RESOLVED_BY_CORRECTION=0 DANGLING=0 C3=PASS exit=0
```

So the `correction:` channel is a dead letter: a retarget need not be declared, and the counter cannot tell repair
from repoint. `RESOLVED_BY_CORRECTION` is printed (`:110`) but is not in the pass expression (`:118`,
`ok = not dangling and len(rows) >= len(brows) and n_ptr >= b_ptr`).

## Cheats that pass, and what each launders

1. **Corrections to unrelated documents (F, G, I).** `corr[(row line, pointer)] = target` (`:100`) plus `real(root/tgt)`
   (`:107`, `:44-48`) accept *any* existing non-empty path: `-> README.md` (F), `-> PROVINCE.md` for a `measure/` pointer
   (G: right row number, path exists, not the document the row meant), a directory `-> tools` (I) — all PASS, `corr=4`.
2. **Corrections are position-independent (N).** The frozen sentence says "a **later** `correction:` line"; `:100` stores
   any position, so four lines placed above their rows (with shifted numbers) PASS. H fails only because the inserted
   lines move the row numbers — the guard is incidental, not the rule.
3. **The count gate is a total, not a set (`:118`).** L wraps the five dangling tokens as `` `<measure/final/>` `` (the
   `<>` in `BAD`, `:39`, drops them from the census) and pads five resolving pointers into one cell → PASS. U demotes one
   heading, `## Round 37 — …` → `### Round 37 — …`; since the preceding section is `## Capabilities (round-36 change)` and
   only `## ` resets `inside` (`:60-63`), ten verdict-table rows are absorbed as capability rows (`rows=46/36 ptrs=80/74`,
   **no text added**, S) → with six wraps, PASS. J deletes the five dangling-holding lines and adds four decoy rows → PASS
   with four real rows gone. Q: fenced blocks are not skipped, so decoys can be parked in a fence (`ptrs=82/74`).
4. **Suppression is invisible; it fails only by one pointer (A, C, D, E2, B).** Unwrapping backticks (A), `<…>` (C), `[…]`
   (D) or moving the token to cell 2 (E2) each drops exactly one pointer: `ptrs=73/74` → FAIL by arithmetic, not
   detection; one pad pointer restores it (L). Renaming the largest heading (`## Capabilities (round-25 reconciliation of
   earlier LOG claims)` → `## Capability reconciliation…`) drops `rows=28/36 ptrs=66/74` — 8 rows, 8 pointers, FAIL; the
   demotion direction (S) is the one that pays.
5. **`real()` is existence-only (`:44-48`).** A directory holding a zero-byte file resolves `measure/final/` (O); a symlink
   to `README.md` resolves three more (P); a 1-byte file resolves all five (K). The EMPTY control fails only because it
   writes zero bytes at the file path itself, never a directory.

## Classification

- **Fixable divergence from the frozen text** — the "later line" clause (N) is in the predicate sentence, so enforcing it
  implements the claim rather than changing it (same class as erratum E1); I edit nothing, the L1 chooses between that
  erratum and a disclosure that corrections are position-independent.
- **Predicate-level holes, frozen, not fixable this round** — corrections to unrelated paths (F/G/I), the totals-not-sets
  gate (J/L/S/U/Q), suppression invisibility (A/C/D/E2), the undeclared retarget (V). C3's kill rule ("any dangling pointer,
  a lower row or pointer count") is exactly the two-sided gate L and U defeat. Disclose now, do not inherit: strengthening
  (base pointer set ⊆ tip pointer set, capability names compared, correction target bound to the pointer's directory, a
  suppressed-token census) is a new predicate — a round-52 decision.
- **Already-named limit** — "existence, not truth" (`claims.md` C3, docstring) covers K, O, P, W.
- **No false negative** — W passes with unchanged counts; the counter is under-discriminating, not over-strict.

## Calibration or bookkeeping

Bookkeeping. C3=PASS asserts only that the extractor found no unresolved token in the cells it chose to read and that two
totals did not fall. A reader must **not** conclude from C3=PASS that (i) the five pointers were repaired rather than
deleted, wrapped, demoted or repointed; (ii) any `correction:` line is truthful (any existing path counts; `corr=4` is
compatible with zero repair); (iii) the census is complete (backticks only, cells 2 and 4 unread, `<…>`/`[…]` skipped);
(iv) the capability set is unchanged (rows keyed by line number and heading text, names unchecked); (v) the cited evidence
shows the claimed behaviour — the declared existence limit, which V/W show is undetectable. What C3 buys is narrow and
real: wholesale deletion of the capabilities table or a mass move of pointers would be caught, the round-50 defect it was
written for.

Lane untouched: `git status --porcelain` lists only the pre-existing untracked `.ufo/waves/round-51/*` (plus a sibling
seat's `corpus/evidence/round51/zero.txt`, not mine); `sha256sum SCORECARD.md SHONEN.md` equals `git show HEAD:`
(`9c7b59cb…`, `6cebe10f…`). The one bytecode cache my `importlib` load created (`…/round51/__pycache__/c3-count
.cpython-314.pyc`) was removed; a sibling's `build-spans` pyc left.

VERDICT: attacked C3 — eight repair-free routes reach `C3=PASS` (V, F, G, I, N, J, L, U), the cheapest being five pointer-
string substitutions whose stdout is byte-identical to a true repair's; C3 as declared is bookkeeping of its own census,
not calibration, and its PASS must not be read as repaired evidence.
