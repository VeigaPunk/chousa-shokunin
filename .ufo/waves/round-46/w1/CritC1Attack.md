# CritC1Attack — C1's fixture set as an oracle (R46-C1, operability)

seat: L1Chousa46.CritC1Attack (critic, leaf) · 2026-10-25
item: attack `corpus/fixtures/inference-ground-r46/` as an oracle — are the three
junk fixtures strawmen, and does a fourth junk body that reuses correct spans and
figures (every token grounded, assertion wrong) survive? bounds: read-only; no
fetch, no network, no install; only this file written; scratch
`/tmp/chousa-r46-CritC1Attack/` deleted. Pairs with `MutC1Junk.md` (same wave:
fence hole F-C1-a, counts-vs-citation independence N3); not repeated.

## 0. Baseline — the claim as declared verifies

```
$ git rev-parse HEAD
c2f0e9d100c0d46633a6277b2fd51d2ac99678eb              # = freeze commit
$ git diff --stat c2f0e9d1… -- corpus/fixtures/inference-ground-r46 tools/ corpus/evidence/round46/   # empty
$ python3 corpus/evidence/round46/c1-count.py
TOOL=present  POSITIVE_PASS=3/3  JUNK_KILLED=3/3  C1=PASS      EXIT=0
```

Controls reproduce the claim's numbers exactly: always-exit-0 → `POSITIVE_PASS=3/3
JUNK_KILLED=0/3` exit 1; citation-only → `POSITIVE_PASS=3/3 JUNK_KILLED=1/3` exit 1.
Per-fixture runs (`--entry … --spans …/spans.tsv --counts …/counts.json`):

| fixture | tool line | findings | exit |
|---|---|---|---|
| positive-a / -b / -c | `tokens=1 grounded=1` / `=1/1` / `=2/2` | — | 0 |
| junk-uncited | `tokens=1 grounded=0` | `INF_UNCITED`; `INF_TOKEN_NOT_IN_SPAN token='the release ships a frozen pool'` | 1 |
| junk-ungrounded | `tokens=1 grounded=0` | `INF_TOKEN_NOT_IN_SPAN token='reverse index of every citation'` | 1 |
| junk-borrowed | `tokens=3 grounded=1` | `INF_TOKEN_NOT_IN_SPAN 'independently re-verified against a live source'`, `… '4,137'` | 1 |

## 1. `junk-borrowed.md` is a strawman for the class it names

Class (c) is declared as "a body that reuses the correct spans and figures while
its inference asserts something else (the D7 class)". The fixture does not do
that; of its **three** tokens, two are fabricated:

```
- Therefore every claim is `independently re-verified against a live source` before release,
  and 4,137 claims carry `no revision is recorded` (`S901`).
```

Both fabricated tokens are absent from `spans/S901-1.txt` and `counts.json`
(`{7572, 5959, 78.7}`), so the fixture is killed by the same check as
`junk-ungrounded.md`: class (c) has **zero** fixtures and `JUNK_KILLED=3/3` buys
two checks, not three. `junk-uncited.md` is fair for the citation leg but
misdiagnosed: its token `the release ships a frozen pool` **is** in
`spans/S901-1.txt` (`grep -c` → `1`), so `INF_TOKEN_NOT_IN_SPAN` there is false —
emitted only because `span_texts()` returns `[]` for an empty cited set
(`tools/inference-ground.py:149-152`).

## 2. The fourth mutant — grounded tokens, wrong assertion → SURVIVES

`junk-negated.md` (sha256 `d82add4d06f496ea2831a636b23a6cf4c28756fc62fd937fb2c890c60f3d5260`):
two source lines, every token verbatim in a span or the counts manifest, two
assertions inverted against their spans. The single `#### Inference` bullet:

```
- Every sentence carries a recorded revision and a placeholder value is an archive link, so the pool
  does not ship `the release ships a frozen pool` and all 5,959 answers are bound citations (`S901`, `S902`).
```

S901-1 says `… no revision is recorded per sentence`; S902-1 says `a placeholder
value is not an archive link`. Wrong quantifier, wrong negation, negated quote —
accepted: `GROUND entry=junk-negated.md section=1 bullets=1 tokens=2 grounded=2 /
GROUND: PASS`, exit 0.

Four further mutants, one `#### Inference` bullet each; **all four exit 0 with
`tokens=2 grounded=2 / PASS`** (`junk-nospan` `tokens=1 grounded=1`):

| mutant (sha256) | inference bullet |
|---|---|
| `junk-figureflip` `e66aa19f…` | `78.7% of answers name no source at all, which is why the archived copy is `the archived copy is dated at build` (`S902`).` — 78.7 is the *archive* share |
| `junk-figureid` `8406acbb…` | `All 7,572 answers carry an archive link, and the archived copy is `the archived copy is dated at build` (`S902`).` — 7,572 name a source; 5,959 archived |
| `junk-crossattrib` `54167bee…` | `S902 says `the release ships a frozen pool` while S901 says `the archived copy is dated at build` (`S901`, `S902`).` — each quote belongs to the other |
| `junk-nospan` `38dd5a95…` | `5,959 answers carry an archive link, so a filled field is a bound citation (`S999`).` — S999 has no span row |

`junk-nospan` shows the numeral leg is neither citation- nor span-scoped:
`count_values()` flattens the whole JSON into one set, so any listed figure
grounds any bullet, even one whose cited source has no evidence at all.

**The round-45 D7 forge still passes.** Rebuilt as `CritC3Axis.md:77-79` describes
(two `source:` lines plus the four quotes pasted verbatim; the other, the source
line plus the seven figures) and run on the real round-45 tree, both print
`GROUND: PASS` exit 0 — `d7-field.md` `tokens=4 grounded=4`, `d7-snap.md`
`tokens=6 grounded=6`. The second also shows a blind spot: seven figures pasted,
six tokenised — `1 evidence empty` is invisible, the numeral pattern needs three
digits or a percent (`tools/inference-ground.py:26`).

## 3. Oracle drift — the kill rule's second clause is unmeasured

`c1-count.py` names its six fixtures in two tuples and reads nothing else, so
"a fixture set changed after this freeze" cannot fail. Tree copy with two
surviving mutants added beside the six — `ls drift2/corpus/fixtures/inference-ground-r46/*.md
| wc -l` → `8`, then `python3 corpus/evidence/round46/c1-count.py --root
/tmp/chousa-r46-CritC1Attack/drift2` → `TOOL=present POSITIVE_PASS=3/3
JUNK_KILLED=3/3 C1=PASS` exit 0: eight fixtures, two failing, still green.

## 4. Verdict

**Holds-narrowed — predicate true, capability claim false.** R46-C1 verifies as
declared and both cheap controls are correctly refused, but the fixture set does
not instantiate junk class (c): `junk-borrowed` is a second class-(b) case wearing
a fabricated figure, so the third kill leg is untested and the D7 forgery the claim
exists to close passes the new tool unchanged. `junk-uncited` also makes the tool
print a false `INF_TOKEN_NOT_IN_SPAN`.

**Narrowest true sentence** — what the tool enforces: *every `#### Inference` bullet
outside a fence names at least one `S`-id; every bullet carries at least one
backticked or quoted phrase of two or more words or a number of three or more
digits; every such phrase appears verbatim in a span file listed for one of the ids
that bullet itself cites; and every such number appears somewhere in the counts
manifest.*

**What it still cannot do:** refuse a bullet whose phrases and figures are all
genuine but whose sentence asserts the opposite (`not`, `no`, `never` around a
grounded phrase), the wrong quantifier (`every` for `some`/`no`), the wrong label
for a real figure, the wrong source among jointly cited ones, or a source with no
span at all; nor see a bullet hidden in a fence (`MutC1Junk.md` F-C1-a) or a 1–2
digit figure.

## 5. Smallest safe correction

1. **Re-label, do not re-engineer** (`claims.md` R46-C1): drop "(the D7 class)"
   from `junk-borrowed.md` — it is class (b) with a second fabricated token — and
   record class (c) in the claim's named limit beside the tool docstring's lexical
   limit. `JUNK_KILLED=3/3` then means what it measures; no predicate, counter,
   fixture or target changes, so the kill rule stays intact.
2. **Make the freeze clause measured** (2 lines in `c1-count.py`): assert the
   directory holds exactly the six names, else print `FIXTURE_DRIFT` and exit 1.
3. **Fix the false finding**: for a bullet citing nothing emit `INF_UNCITED` only,
   or rename that code `INF_NO_CITED_SPAN`; optionally require a numeral's *key*
   (e.g. `answers_archived`) in the bullet, killing `junk-figureid` and
   `junk-nospan` lexically. Do not attempt the negation/quantifier class lexically
   — declare it unenforced.

## 6. Impacted axes

**operability (C1's axis):** increment real but one third narrower than recorded;
the D7 forgery still passes. **calibration:** the counter's fixture-freeze kill
clause is prose — an oracle can grow failing members and still print PASS.
**depth (C3):** untouched directly; the risk is C3 verdicts inheriting "grounded"
whose known meaning is lexical only.

No lane file modified beyond this report. No install. Scratch deleted.
