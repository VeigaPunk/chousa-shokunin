# MutC1More — round 46 wave 2, mutation probe on R46-C1

seat: L1Chousa46.MutC1More (mutation-tester, leaf) · target: `d09fc8e7e2972e30e5e0aaa6e404c97aa0b9f95a`, `tools/inference-ground.py` · landed tool sha256 `819f83ebdc6c6b47d83216f5403824c152ba1f12f09c88b16e2e1184275326bc`
detector `corpus/evidence/round46/c1-count.py` (`819287e2075c3f5b57c4ceb26fb6b3d7594af48e03ad7cfcd61690727c9e0a65`) · scratch `/tmp/chousa-r46w2-MutC1More` (`git archive d09fc8e7 | tar -x`), deleted after. Line pointers below are landed-file lines.

## Baseline — pristine copy of the landing

`python3 corpus/evidence/round46/c1-count.py --root /tmp/.../base` → rc **0**
```
TOOL=present / POSITIVE_PASS=3/3 / JUNK_KILLED=3/3 / C1=PASS
```
Live lane: rc **0**, identical. All 8 `PINNED` digests re-derived independently: `mismatches: none | pins: 8` — the byte-pin leg wave 1 (`CritC1Attack`) named is enforced, and C1 holds as declared before any mutation.

## M1 — fenced `- ` bullet after the real bullet (wave-1 survivor)

Body: bullet 1 grounded, then fenced `- Therefore every claim is \`independently re-verified against a live source\` (\`S901\`).`
Landed tool rc **1**
```
GROUND entry=bodies/m1-fenced.md section=1 bullets=2 tokens=2 grounded=1
FINDING INF_TOKEN_NOT_IN_SPAN bullet=2 token='independently re-verified against a live source'
```
**KILLED at the tool level**: the landed `if line.startswith("- ")` (`:92`) is not guarded by `fence`, so fenced bullets count.
As a mutant it **SURVIVES the detector** — insert `if fence: continue` before `:92`
(`mut/t1-fence-skip.py`, sha `59f58e7d75e931ed833fb9aa1ae4e55c2384c767a9d483d31e39d3f819cffe5a`):
```
counter rc=0 :: TOOL=present | POSITIVE_PASS=3/3 | JUNK_KILLED=3/3 | C1=PASS
mutant on m1-fenced.md rc=0 :: bullets=1 tokens=1 grounded=1 | GROUND: PASS
```
`fence lines in fixtures: 0`. The one-line behavior that fixed the wave-1 survivor is unpinned — a revert is invisible.

## M2 — `#### Inference` with prose only (no bullets)

Landed tool on one prose sentence carrying a cited token and no `- ` line: rc **0**
```
GROUND entry=bodies/m2-prose.md section=1 bullets=0 tokens=0 grounded=0
GROUND: PASS
```
**SURVIVOR — live escape on the landed bytes.** `INF_NO_BULLETS reachable in landed source: False`
(the last findings append is inside the per-bullet loop at `:260`; `:261` prints with no bullet-less guard).
The docstring rule "every bullet of that section cites …" is vacuously true when there are none, and the
counter scores the same rc=0 (`landed :: (0, 'TOOL=present … C1=PASS')`). The wave-2 correction commit `3807537`
(child of the target; HEAD while probing) already patches it — `tools/inference-ground.py` differs from the landing by
+26/−4, sha `3018b1d25d76205496ae002600003f5ddb4294328be4741b9fa58c8ddc223f07` (= `git show 3807537:tools/…`):
```
WT tool on m2-prose rc=1 | FINDING INF_NO_BULLETS bullet=0 | GROUND: FAIL
```
The repair is not in the target, and `git diff --stat d09fc8e7 3807537 -- corpus/fixtures/ corpus/evidence/round46/c1-count.py`
is empty, so no fixture pins it either. Round-honesty seat: C1's PASS at `d09fc8e7` rests on bytes that accept a
bullet-less Inference section, and that repair landed during the falsification wave rather than in the landing.

## M3 — bullet whose only numeral is a 2-digit figure inside a 3-digit span figure

Span `spans/S901-3.txt`: `the corpus records 421 answers per release; 5,959 answers carry…`; bullet `…records 42 answers…`.
Landed tool rc **1**
```
GROUND entry=bodies/m3-two-digit.md section=1 bullets=1 tokens=0 grounded=0
FINDING INF_UNGROUNDED bullet=1 token=''
```
**KILLED, but incidentally and at a precision cost**: the kill is the `NUM_RE` floor at `:50` (`\d[\d,]{2,}` = 3+ digits),
not a value compare. The honest mirror (`42 answers` verbatim in its own span) is refused identically —
`rc=1 :: FINDING INF_UNGROUNDED` — so a true 2-digit figure can never be a grounding token. A mutant lowering the floor
(`mut/t3-numeral-2digit.py`, sha `ed1b7e88d9e74059896882370516cc22240f629c8b940ac846a224d8388db9f4`) **SURVIVES** and
then grounds both bodies by substring (`"42" in "421 answers"`):
```
counter rc=0 :: POSITIVE_PASS=3/3 | JUNK_KILLED=3/3 | C1=PASS
mutant on m3-two-digit.md rc=0 :: bullets=1 tokens=1 grounded=1 | GROUND: PASS
```
No bullet in the six fixtures carries a sub-3-digit numeral (`45` in `junk-borrowed.md` is in its `# … round-45 D7 class` title).

### M3b — same seam on the current bytes, no mutant needed (**new**; not in wave 1's list)

Bullet `- Only 959 answers carry an archive link (\`S901\`).` against a span holding `5,959`. `ok = any(tok in s for s in grounded)`
at `:251` is a substring test, so the wrong figure grounds: rc **0**
```
GROUND entry=bodies/m3b-three-digit-in-four.md section=1 bullets=1 tokens=1 grounded=1
GROUND: PASS
```
`959 ≠ 5,959`. Live false positive on the landing (the `values` leg uses exact membership; the span leg does not).

## M4 — two `#### Inference` sections: first or last wins?

Landed tool, grounded section then junk section: rc **0**
```
GROUND entry=bodies/m4-twice-good-first.md section=1 bullets=1 tokens=1 grounded=1
```
Reversed body → rc **1**, so **the first section wins and the second is never read** (pre-scan `start = i + 1; break`, `:75-76`).
**SURVIVOR — an entry may carry a second, unexamined Inference section.** Mutant `mut/t4-last-wins.py` (drop `break`,
sha `33ce6acddd20b3d2e232cc5921211924d1f2ef1824ecb8a84b65c89e1dce43fb`) **SURVIVES** the counter (`rc=0 :: C1=PASS`)
while my body kills it (`rc=1 :: FINDING INF_TOKEN_NOT_IN_SPAN`). The section policy is unpinned both ways, and the landed
direction is the permissive one. `two-inference-entries=[]`.

## Coverage census — why all four survive

```
fence lines in fixtures: 0 ; two-inference-entries=[] ; sub-3-digit numerals in any bullet: none
```
and `c1-count.py`'s `run()` passes only `--entry/--spans/--counts/--root`, never `--registry`, so the landed registry path
(`:184-186` stores the whole title cell; `:255-256` grounds a numeral by substring of that cell — no `designators` yet) is
unexercised too. Six bodies, three defect classes, eight pinned bytes.

## Claim verdict

R46-C1 **PASSES as declared** at `d09fc8e7`: rc=0, pins 8/8, both legs 3/3, and the tool also passes both adopted
knowledge entries (`section=1 bullets=4 tokens=7 grounded=7`; `bullets=4 tokens=5 grounded=5`, rc=0). No kill rule
violated, no target re-scaled.

Reported disagreement (scope, not target): the predicate is fixture-only, so three escapes *inside the tool's own stated
rule* are invisible to it — (a) "every bullet of that section cites …" is vacuously true for a bullet-less section (M2, rc 0);
(b) an unread second `#### Inference` section (M4, rc 0); (c) substring numeral grounding `959 ⊂ 5,959` (M3b, rc 0), plus the
mirror precision loss (a verbatim 2-digit figure refused, M3, rc 1). The docstring's named limit covers (c)'s semantic cousin
only; (a) and (b) are structural, and (c) counts a wrong figure as the right one.

## Restoration evidence (scratch only; lane bytes never written)

Each mutant staged in a scratch slot, scored, restored from the pristine copy and re-hashed:
```
RESTORE t1-fence-skip.py:     before=819f83ebdc6c mutated=59f58e7d75e9 after=819f83ebdc6c equal=True counter_rc=0
RESTORE t3-numeral-2digit.py: before=819f83ebdc6c mutated=ed1b7e88d9e7 after=819f83ebdc6c equal=True counter_rc=0
RESTORE t4-last-wins.py:      before=819f83ebdc6c mutated=33ce6acddd20 after=819f83ebdc6c equal=True counter_rc=0
```
`mut/landed.py` and `base/tools/inference-ground.py` both `819f83eb…5326bc` (`== git show d09fc8e7:tools/inference-ground.py`).
Lane bytes untouched by this seat (lane tool `3018b1d2…f07` = `git show 3807537:tools/…`). All baseline and mutant
scores used the landed detector `corpus/evidence/round46/c1-count.py` `819287e2…` (identical at `d09fc8e7` and `3807537`);
the live counter now reads `8473abf6c4437beda5e8ba53e3045e5e47d994c87294707c745fc6493c69e03a` — a concurrent seat's edit, not this one's.
Scratch tree deleted.

survivors named: M2 (prose-only section), M4 (second section unread), M3b (substring numeral), plus mutant-level T1, T3, T4 — all five accept a body the counter scores PASS.
tooling: nothing installed or upgraded (no pacman, no uv, no network); counters ran on the host `python3` 3.14.
