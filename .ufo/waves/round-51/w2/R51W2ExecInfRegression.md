# R51W2ExecInfRegression — inference-ground regression, the three entries, a polarity probe

Lane `/home/vgpnk/Projects/shokunin/chousa-shokunin`, HEAD `72566c84e4184846ff9cbc4c92bc33b8291bc53b`. The brief's tip `4436e279…`
is an ancestor and `git diff --stat 4436e27..72566c8` is four `.ufo/waves/round-51/` files only (`gen-w2-spec.py`,
`w2-dispatch.json`, `w2-run.err`, `w2-spec.json`): no tested byte moved. No network, no install; only this file written; scratch
`/dev/shm/chousa-r51-R51W2ExecInfRegression/` removed.

## 1. The tool is byte-identical to the pre-round state

```
$ sha256sum tools/inference-ground.py                                    33d4a37f3f7a5ce87862d0a354b3058ed5c579c5491b9e5d3ec6610a8e962b6d
$ git show 9ec1751a24231e899ceea4688e21c8edf6046d35:tools/inference-ground.py | sha256sum   (identical digest)
```
Confirmed premise: every counter below measures the round-50 tool against round-51 bytes.

## 2. Round-46/47/48 counters, replayed from committed bytes (`git archive 72566c8` into scratch)

```
round46/c1-count.py        rc=0 C1=PASS      round47/c1-count.py        rc=0 C1=PASS
round46/c2-count.py        rc=1 C2=FAIL <--  round47/c2-count.py        rc=0 C2=PASS
round46/c3-count.py        rc=0 C3=PASS      round47/c3-count.py        rc=0 C3=PASS
round48/c1-count.py        rc=0 C1=PASS      round48/precision-count.py rc=0 PRECISION_GATE=PASS
round48/mutation-check.py  rc=0 MUTANTS_KILLED=5/5
```
`precision-count.py` also prints `CORRECT_BULLETS_PASS=12/12 MIN_CORRECT_PASS=11/12` (round-47/48 polarity intact on its own fixtures).

## 3. BREAK: R46-C2 regressed PASS (base) → FAIL (freeze) → still FAIL (tip)

```
base   9ec1751  ENTRY_POINTS=93 (tools=9 counters=58 named=91) GATES_ROWS=50 REGISTERED=93/93 UNREGISTERED=0 C2=PASS rc=0
freeze d603f6f  ENTRY_POINTS=97 (tools=9 counters=61 named=95) GATES_ROWS=50 REGISTERED=94/97 UNREGISTERED=3 C2=FAIL rc=1
tip    72566c8  ENTRY_POINTS=98 …                             GATES_ROWS=50 REGISTERED=96/98 UNREGISTERED=2 C2=FAIL rc=1
$ python3 corpus/evidence/round46/c2-count.py --list          # tip
UNREGISTERED_PATH corpus/evidence/round51/c2-count.py
UNREGISTERED_PATH corpus/evidence/round51/c3-count.py
```
`corpus/evidence/round46/claims.md` kill rule: `UNREGISTERED>0 … fails the claim as declared`; nothing retires R46-C2
(`grep -n "R46-C2\|retire" corpus/evidence/round4[78]/claims.md corpus/evidence/round50/claims.md` → prose about axes only): a frozen prior claim is false at the tip.

Cause, measured: `gates_rows()` (round46/c2-count.py:74) reads a row only if the **raw** line starts with `|`, carries
`>= 9` pipes **and contains the literal word `exit`**. The wave-1 row at `SKILL.md:133`
(`| \`chousa round-51 counters and checks\` | gate | …`) has 9 pipes, starts with `|`, and names all three counters in its
entry cell — but no `exit` token (`row.count('|')=9`, `'exit' in row` → `False`); its verdict cell reads
``C1 `0` only with `LEGS=5/5` … `2` `PIN_CHANGED``. `c1-count.py` still registers via round-51 `claims.md:40` (leg C);
`c2-count.py`/`c3-count.py` are named nowhere else. Round-47/c2 does not flag them because its rule accepts a backticked
code (`EXIT_CODE`, round47/c2-count.py:91 matches `` `0` ``): the two frozen counters disagree and only the older is red.

Draft repair for the L1 — one insert into the verdict-map cell of `SKILL.md:133`, no predicate/target/control touched:

```
find:    | C1 `0` only with `LEGS=5/5`
replace: | exit 0 only when every counter prints its PASS line; C1 `0` only with `LEGS=5/5`
```
Witnessed in a scratch copy of the committed tip tree, not the lane: `round46/c2-count.py` → `REGISTERED=98/98 UNREGISTERED=0
C2=PASS rc=0`; `round47/c2-count.py` → `MISMATCHES=0 C2=PASS rc=0`. The inserted map is true: all three round-51 counters are
`return 0 if ok else 1` (c1-count.py:215, c2-count.py:273, c3-count.py:120).

## 4. The three entries ground, with the brief's exact command

```
python3 tools/inference-ground.py --entry <e> --spans corpus/evidence/round51/spans.tsv --counts /dev/null \
        --registry corpus/SOURCES.md --root .
r38        section=1 bullets=4 tokens=10 grounded=10  GROUND: PASS rc=0
r39        section=1 bullets=6 tokens=9  grounded=9   GROUND: PASS rc=0
amendment  section=1 bullets=5 tokens=8  grounded=8   GROUND: PASS rc=0
python3 corpus/evidence/round51/quote-substance-check.py …/spans.tsv → IDS=6 QUOTES=61 FAILURES=0 rc=0
```

## 5. HAND-MADE POLARITY PROBE — three CJK flips pass; four Latin controls fire

**Missed (the deliverable).** Each entry copied to scratch, one `#### Inference` bullet minimally negated, all tokens byte-exact,
tool rerun with the §4 flags (`spans.tsv` = header + 61 rows) — all three PASS:

| entry | edit | observed |
|---|---|---|
| r38 | `the expression is not restated in the checklist body` → `the expression is restated in the checklist body` | `tokens=10 grounded=10 GROUND: PASS` |
| r39 | `§2.4.1 asks for \`至少提供一个主要数据库的完整检索策略\`` → `§2.4.1 does not ask for …` | `tokens=9 grounded=9 GROUND: PASS` |
| amendment | `is reported as a PRISMA-P protocol element` → `is not reported as a PRISMA-P protocol element` | `tokens=8 grounded=8 GROUND: PASS` |

**Caught** (the gate is alive, not dead):
- pinned fixture `corpus/fixtures/inference-ground-r47/junk-flip-denied.md` → `FINDING INF_POLARITY_FLIP bullet=1 token='the release ships a frozen pool / frozen'` rc=1.
- r38 bullet 1 citation swap `(S108)` → `(S112)`, tokens untouched → 4 × `INF_TOKEN_NOT_IN_SPAN`, `grounded=6` rc=1.
- a quote from S112 appended to that same S108 bullet (`評価がしやすくなる`) → `INF_TOKEN_NOT_IN_SPAN` rc=1.
- the same negation restated in Latin in r39 bullet 5 (`+ " The module row does not name MeSH."`) → `FINDING INF_POLARITY_FLIP bullet=5 token='检索词及逻辑关系（结合 MeSH/Emtree 主题词与自由词） / mesh'` rc=1.

**The blind spot, exactly.** P1/P2 are Latin-lexical: `WORDS_RE` matches `[a-z]` only (tools/inference-ground.py:253), `content()`
keeps len≥4 ASCII words (:283), `polarity_flips()` returns `[]` when a phrase yields no stems (:340) — a CJK quoted phrase yields
an empty scope, so neither span-side negation nor bullet-side negator can fire. Measured across the
three entries: **27 grounding tokens, 1 with a non-empty scope** — only `检索词及逻辑关系（结合 MeSH/Emtree 主题词与自由词）`
(scope `mesh`, `emtree`). Round 47 named the limit as "token presence, not entailment"; round 51 sharpens it: for this theme
the polarity machinery addresses 1 of 27 quoted claims, and the one flip it caught was one I wrote in English. Named limit,
not a wiring bug — do not widen `WORDS_RE` inside a frozen round's tool. Draft text the L1 may land beside §3's repair
(additive, predicate-free):
```
correction: SKILL.md:133 — `tools/inference-ground.py` P1/P2 polarity reads Latin content words only
(tools/inference-ground.py:253, :283, :340); 26 of the round-51 entries' 27 quoted claims carry no Latin scope word and
are outside the polarity check, so a negated CJK claim still grounds. Claim truth for S107-S112 rests on the C2 quote and
lesson gates, not on this tool.
```
## 6. What holds

- `round51/c1-count.py` `C1=PASS`, `c2-count.py` `C2=PASS`, `c3-count.py` `C3=PASS`, `c1-supplement.py` `C1_SUPPLEMENT=PASS`,
  each rc=0 with `env -u ASSIMILATE_CITES`: the round-51 claims are green; only inherited R46-C2 is not.
- Tool unchanged since base (digest above); round-47/48 fixtures still 12/12 correct bullets passing, `MUTANTS_KILLED=5/5`.
- Entries: `#### Inference` present, every bullet cited, every token grounded (10/10, 9/9, 8/8); citation identity enforced
  (swap and foreign-quote probes); `--counts /dev/null` per the brief, so the figure path was not exercised. Both red paths
  sit in the SKILL row's entry cell — the failure is the missing literal `exit`, not a missing registry entry.

## 7. Risks / blockers

- An unrepaired tip ships a frozen claim printing `C2=FAIL rc=1`; one word in one cell makes it green (§3, witnessed).
- Reading `GROUND: PASS` here as a fidelity verdict would be wrong for 26 of 27 quoted claims; the entries may still be faithful
  — this tool does not measure that. No blocker; repair and correction line are drafts for the L1, not edits by me.

VERDICT: attacked the round-46/47/48 replay of `tools/inference-ground.py` and its Inference grounding on all three
round-51 entries — tool byte-identical and entries ground (10/9/8 tokens), but **R46-C2 prints FAIL at the tip**
(`round51/c2-count.py`, `round51/c3-count.py` unregistered; base PASS → freeze FAIL → tip FAIL; one-word row repair
witnessed green), and **all three hand-negated CJK Inference bullets pass** while four Latin controls fire — polarity is
Latin-only, 27 tokens, 1 scope-bearing.
