# R51W2CritForgeC3Final — C3 after the repair: content, deletion, and eleven PASS cheats

seat: critic, r51 w2 · axis: calibration · claim R51-C3 (frozen `d603f6f`) · lane read, never written; no install
scratch `/dev/shm/chousa-r51-R51W2CritForgeC3Final/`, deleted before yield.

## 0. Tip I read

```
$ git log --oneline -1      → 72566c8 (one commit past the named 4436e279)
$ git diff --stat 4436e279b91d8d68fd439c9095695035fbeeab74 HEAD -- SCORECARD.md SHONEN.md corpus/evidence/round51/c3-count.py | wc -l
0
```

HEAD carries byte-identical `SCORECARD.md`, `SHONEN.md` and counter, so every result below is also the 4436e27 result.

## 1. The repair, checked by content

```
$ env -u ASSIMILATE_CITES python3 corpus/evidence/round51/c3-count.py; echo exit=$?
CAP_ROWS=36 (base 36) · POINTERS=74 (base 74) · RESOLVED_BY_CORRECTION=4 · DANGLING=0 · C3=PASS · exit=0
```

Four lines at `SCORECARD.md:2626-2629`; the rows still print the bare tokens (`:1843` `measure/final/`, `:2073`
`measure-l1/c1-s36361.json`, `:2074` `measure-l1/c2-s36371.json`, `:2616` `c1-supplement.py`).

| row | row prints | target | what the target shows |
|---|---|---|---|
| 1843 | `→ 24/24` | `.ufo/waves/round-32/measure/final/` | `battery.out:5` `APPEND_SERIALIZED=24/24` |
| 2073 | `→ 14/14` | `.ufo/waves/round-36/measure-l1/c1-s36361.json` | `:5` `"label": "ENGINE_SWAP_CANARY=14/14"`, `:6` `"matched": 14` |
| 2074 | `→ 5/5 + renamed pass` | `.ufo/waves/round-36/measure-l1/c2-s36371.json` | `:5` `"label": "WITNESS_PER_RECORD=5/5"`, `:30` `"renamed": "pass"` |
| 2616 | adopter self-test | `corpus/evidence/round50/c1-supplement.py` | `:11-12` `SELFTEST=ERROR` legs, `:34` runs the tool `--selftest`; round-50 C1 (`round50/claims.md:18-24`) *is* the adopter self-test |

All four targets tracked and non-empty (`git ls-files --error-unmatch` → TRACKED; 12403 / 7039 / 4069 / 4175 B).
Ambiguity: `find . -name c1-supplement.py` → round50 and round51; the line names round-50's, matching the row's
`## Capabilities (round-50 addition)` and milestone 50 — the counter would accept round-51's as readily (`:105-108`
is existence only). `SHONEN.md:10` has no correction channel (`:107` reads them only for `SCORECARD.md`), so it was
rewritten in place (`round25-meta-differential.log`: `AGREE=54/54`), 3 pointers held. Nothing deleted: `git diff
--numstat 9ec1751a… 4436e279…` → `9 0` / `1 1`; row and pointer counts equal base (36/74).

## 2. Cheat matrix at the repaired tip (real-tree copy, never a symlink to the lane)

`tar --exclude=.git -cf - . | tar -C $S/root -xf -` (257 MB; `test ! -L $S/root` → real dir); pristine copies in
`$S/pristine`; `$S/cheats.py` rewrites only the two files per run, clears what a prior run planted, and calls
`c3-count.py --root $S/root` (base counts still from the lane; HONEST — the unchanged lane — is the §1 run).

```
PASS V1 in-row retarget, corrections dropped; V2 same, -> README.md×3/PROVINCE.md     corr=0 D=0
PASS F  corrections -> README.md×3/PROVINCE.md; I  correction -> tools (a directory)  corr=4 D=0
PASS N2b honest + a later duplicate line -> README.md; J2 SHONEN:10 -> README.md×3     corr=4 D=0
PASS J  four capability rows -> decoys (36/36 74/74); L base text, five <…> wraps +
     five pads, no repair; K five 1-byte files; O five dirs with one 0-byte file      corr=0 D=0
PASS N3 one correction at line 1840, three lines above row 1843                       corr=4 D=0
FAIL A unwrap SHONEN pointer 73/74 · B rename largest heading 28/66 · N2a dup -> absent path, DANGLING 1843 ·
     DURA one blank line at the top, corr=0 DANGLING=4 · U demote `## Round 37`, 46/80 + DANGLING 2103
```

## 3. Decisive: the honest repair and four cheats print byte-identical stdout

```
084b7a69  HONEST = F (-> README×3/PROVINCE) = I (-> tools) = N2b (later dup -> README) = J2 (SHONEN:10 -> README×3)
3c5ced1e  V1 = V2 (in-row -> README×3/PROVINCE) = J (four rows -> decoys) = L (no repair: wraps + pads)
```

Both families print `DANGLING=0 C3=PASS`. Only `RESOLVED_BY_CORRECTION=` separates them, and it is not in the pass
expression: `c3-count.py:118 ok = not dangling and len(rows) >= len(brows) and n_ptr >= b_ptr`. F/I/N2b/J2 differ from
the honest repair only in bytes the counter never reads; V1/V2/J/L differ from one another only in content — **the
honest repair is separated from every PASS cheat by content alone**, exactly what C3 cannot grade. N2a proves
last-wins (`:100` dict assignment): one appended line disarms `:2626` while stdout stays `corr=4 D=0 PASS`.

## 4. Divergences and defects, in the frozen counter's terms

1. **An earlier correction line passes** (N3): `:2626`'s line at 1840, three lines above row 1843 with row numbers
   preserved → `corr=4 DANGLING=0 C3=PASS`; the sentence's word "**later**" is unimplemented. Implementing it is not
   a predicate change (same class as E1) and the repair already satisfies it — L1's call whether it deserves an E5.
2. **Last-wins duplicates** (N2a/N2b) are named nowhere: not in `claims.md` R51-C3's limits, not in QUALITY 83's.
3. **Totals, not sets**: J keeps 36 rows/74 pointers while deleting four capability identities; J2 keeps three
   pointers on `SHONEN.md:10` while replacing promotion evidence with `README.md` (identical stdout).
4. **The target need not be the document the row meant** (F, I): `:108` is `real()` — a non-empty file, or any file
   inside a directory — so K (1-byte) and O (0-byte inner) pass.
5. **Stale observation in a landed criterion**: `corpus/QUALITY.md:888` says "Shown able to fail (ran at the tip)"
   and prints `DANGLING=5 C3=FAIL` — the pre-repair tree; at `4436e27` it prints PASS (criterion 83 entered there).

What holds: the four corrections are truthful by content and each target shows its row's number; all targets are
tracked and non-empty; no capability row and no pointer was removed; the counter never over-refuses (honest repair,
true in-row retarget V1, a correction to a real path all pass); five cheats still fail (A, B, N2a, DURA, U).

## 5. What a reader must not conclude from `C3=PASS`

Not that (i) the four pointers were repaired rather than repointed — F/I/N2b pass with identical stdout; (ii) a
`correction:` line names the document its row meant, only that the path is non-empty; (iii) the correction set is the
visible one — last-wins replaces silently and a correction may sit before its row; (iv) capability identities survive
— J replaces four rows with decoys, J2 swaps `SHONEN.md`'s evidence; (v) the cited evidence shows the claimed
behaviour; (vi) a repair on `SHONEN.md` is distinguishable from an in-place rewrite. What it buys: row or pointer
deletion, an unwrapped or moved pointer, a missing or empty correction target, and the whole pre-repair tree.

## 6. Smallest safe correction

No code change makes a correction truthful without a new predicate (round-52); this round the correction is text,
appendable without touching a row. Intended for `corpus/QUALITY.md` criterion 83's limits sentence:

```
Shown able to fail on the base tree (a `--root` copy of `9ec1751`, not the tip): … `DANGLING=5 C3=FAIL` rc 1.
Named limits: existence, not truth; a `correction:` line is keyed by row line number and is last-wins, so a later
duplicate silently replaces its target and an edit that shifts the row invalidates it; corrections are accepted
before their row; `SHONEN.md` has no correction channel, so its line was rewritten in place; the row- and
pointer-count gates are totals, so a rewritten row or cell with the same number of resolving tokens passes.
# intended: wherever the round-51 C3 result is reported — C3 resolves by four `correction:` lines at
`SCORECARD.md:2626-2629` plus one in-place edit at `SHONEN.md:10`; the counter verifies each target is a non-empty
committed path, not that it is the document the row meant.
```

## 7. Lane and scratch

`git status --porcelain` shows only siblings' wave-2 files (`M …/w1/R51DraftSkillGates.md`, `?? …/w2/`,
`?? …/w2.ready*`); `sha256sum` of both files equals `git show HEAD:` (`352e31f4…`, `84e679f6…`); scratch removed.

VERDICT: attacked C3 after the repair — the four corrections are truthful by content (24/24, 14/14, 5/5 + renamed
pass, the adopter self-test) and nothing was deleted, but eleven cheat routes print `C3=PASS`, four of them
byte-identically to the honest repair (F, I, N2b, J2), and the correction channel is last-wins and position-blind: `C3=PASS` certifies a census of resolving tokens, not repaired evidence.
