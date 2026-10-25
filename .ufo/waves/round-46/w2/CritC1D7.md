# CritC1D7 — the class-(c) residual, exactly (R46-C1, operability)

seat: L1Chousa46.CritC1D7 (critic, leaf) · 2026-10-25 · item: build the strongest junk class (c) body (correct spans, correct figures, wrong inference — the round-45 D7 class) that `tools/inference-ground.py` **accepts**; characterise the residual exactly; test C1's SCORECARD row and Gates row against that sentence. bounds: leaf, read-only on lane production; only this file written; scratch `/tmp/chousa-r46w2-CritC1D7/` deleted; no fetch, no install. Not re-reported from wave 1: presence≠inference (`CritC1Attack`), mention≠dependence (`CritC2Framing`), `junk-borrowed` dying on invented tokens, fence-hidden bullets (`MutC1Junk` F-C1-a), the registry escape, added-fixture blindness (`CritC1Attack` §3).

## 0. Bytes attacked (HEAD moved mid-seat)

```
$ git rev-parse HEAD                      # 3807537 landed while this seat ran
3807537db7e731af508ad7f7d5462f4422ce04c8
$ git cat-file -p d09fc8e7:tools/inference-ground.py | sha256sum
819f83ebdc6c6b47d83216f5403824c152ba1f12f09c88b16e2e1184275326bc   # round-46 landing
$ git cat-file -p HEAD:tools/inference-ground.py | sha256sum       # == worktree
3018b1d25d76205496ae002600003f5ddb4294328be4741b9fa58c8ddc223f07
$ git cat-file -p HEAD:corpus/evidence/round46/c1-count.py | sha256sum
819287e2075c3f5b57c4ceb26fb6b3d7594af48e03ad7cfcd61690727c9e0a65   # == d09fc8e7
```
Fixtures byte-identical at both commits (`git ls-tree` blob ids equal, all 8 names + `spans/`). Baseline at both: `python3 corpus/evidence/round46/c1-count.py` → `TOOL=present / POSITIVE_PASS=3/3 / JUNK_KILLED=3/3 / C1=PASS` EXIT=0. Every escape below was run against **both** tool blobs, identical output. (A sibling later edited the worktree `c1-count.py` to `8473abf6…` adding a `CANARY` leg; out of scope — counter results here use the archived commits, tool `3018b1d2` unchanged.)

## 1. The strongest class-(c) body the tool accepts

`v7-strongest.md`, sha256 `1234254cdc3c086c9813010ce5ef5ebb6feb69b65194ab81267df88e5df295b0` — every token genuinely present, both assertions inverted, and a second wholly fabricated inference in a section the parser never enters:

```markdown
#### Inference
- `the release ships a frozen pool` and `no revision is recorded` (`S901`, `S902`) prove every sentence is revised after publication, that 7,572 answers name no source at all, and that 78.7% of answers without a source carry `the archived copy is dated at build`.

#### Inference (continued)
- Every claim is `independently re-verified against a live source` before release, and 4,137 claims carry `no revision is recorded`.
```
```
$ python3 tools/inference-ground.py --entry v7-strongest.md --spans …/spans.tsv --counts …/counts.json --root .
GROUND entry=v7-strongest.md section=1 bullets=1 tokens=5 grounded=5
GROUND: PASS
EXIT=0
```
Each token is real — the first two in `spans/S901-1.txt`, the third in `spans/S902-1.txt`, `7,572` and `78.7` in `counts.json` — and the sentence drawn from them is false three ways: S901 says `no revision is recorded per sentence` (the bullet says every sentence **is** revised); 7,572 is `answers_named_source` (the bullet says they name **no** source); 78.7 is the archived share **of named-source answers** (re-denominated to answers **without** a source).

## 2. The residual, exactly — narrowest true sentence

> It reads the **first** ATX heading of level 4 whose text begins `inference` (case-insensitive) and the text run up to the next ATX heading of level ≤ 4; from that run it collects only **column-0 `- ` items** plus continuation lines; and it refuses the entry iff the section is absent, yields no such item, or some collected item lacks an `S\d{3,}` id or a grounding token (2+ word backticked/quoted phrase, 3+ digit number, percentage), or carries a token that is not a substring of a span file listed for an id **that item cites**, not numerically present anywhere in `counts.json`, and not a designator of a cited Registry title.

Not enforced: whether the inference follows (declared), and — new here — whether a visible inference is an item the parser reads at all.

## 3. Enumeration escapes wave 1 did not report (each EXIT 0, both blobs)

Mechanism: `inference_bullets()` breaks at the first `#### Inference` and returns at the next heading (`tools/inference-ground.py:70-79`); its only bullet branch is `line.startswith("- ")` (`:99`); a pre-bullet line is dropped silently while `cur is None`.

| body (sha256) | what the reader sees | parser | tool |
|---|---|---|---|
| `v3-second.md` `d3ee9d90d96e476d` | second `#### Inference (continued)` section, uncited, fabricated (`independently re-verified against a live source`, `4,137`) | `bullets=1` (first section) | `tokens=1 grounded=1 / PASS` EXIT=0 |
| `v5-starfirst.md` `5624867503558aa4` | `* ` bullet **before** the first `- ` bullet, uncited, fabricated | `bullets=1` (the `- ` item) | `tokens=1 grounded=1 / PASS` EXIT=0 |
| `v6-afterheading.md` `40d6ddf2e75998ce` | same fabricated claim under `#### Unknown` after the section | `bullets=1` | `tokens=1 grounded=1 / PASS` EXIT=0 |

Bounds, tested so the defect is not overstated: a `* ` bullet **after** a `- ` bullet is merged into it and checked (`v1-star` → `INF_TOKEN_NOT_IN_SPAN`, exit 1), likewise indented `  - ` (`v4-indent`, exit 1); a section whose only item is `* ` gives `bullets=0` → `INF_NO_BULLETS` exit 1 (`v8-staronly`). The escape needs a non-`- ` item ahead of the first `- ` item, or an item in a later section/run.

## 4. Counter at HEAD: substitution pinned, addition not

```
$ cp v7-strongest.md head/corpus/fixtures/inference-ground-r46/junk-classc.md
$ python3 head/corpus/evidence/round46/c1-count.py --root head
TOOL=present / POSITIVE_PASS=3/3 / JUNK_KILLED=3/3 / C1=PASS          EXIT=0
$ sed -i 's/4,137/5,959/' head2/.../junk-borrowed.md
$ python3 head2/corpus/evidence/round46/c1-count.py --root head2
FIXTURES_CHANGED=junk-borrowed.md / C1=FAIL                          EXIT=1
```
The pin closes **substitution** (wave 1 §3 predates it) but not **addition**: `POSITIVES`/`JUNKS` are fixed tuples (`c1-count.py:31-32`), so the predicate's "every junk-`*.md` fixture of the directory" still names a set the counter never enumerates.

## 5. Do the rows describe that sentence, or overclaim?

`SCORECARD.md:2459`: "inference grounding becomes an executable check — `tools/inference-ground.py` refuses an Inference bullet that cites no source and every quoted phrase or figure in one that its cited spans do not carry" · verdict cell: "**improved** (frozen predicate met)… the check proves citation and token PRESENCE, not that the inference follows — the round-45 D7 class still passes (`CritC1Attack`, `CritC1D7`); reported, not hidden".

`SCORECARD.md:2478`: "refuses an `#### Inference` bullet that cites no source, and every quoted phrase or figure in one that its cited spans (or its cited document's designator) do not carry — presence, not entailment".

`SKILL.md:116`: "exit `1` findings, one `FINDING` line per bullet (`INF_SECTION_ABSENT`/`INF_UNCITED`/`INF_UNGROUNDED`/`INF_TOKEN_NOT_IN_SPAN`)" · "limits: it checks citation and token presence, NOT that the inference follows … and it never sees 1–2 digit figures" · "sha256 `819f83ebdc6c…` at the round-46 landing".

- **Entailment residual — described, not overclaimed.** Verdict cell and limits cell both say presence, not entailment; the verdict cell already cites this seat.
- **Bullet scope — overclaims.** "an Inference bullet that cites no source" is false as written: `v5`, `v3`, `v6` each carry such a bullet and exit 0. The true subject is "a column-0 `- ` item in the first Inference section"; neither row says it.
- **Figure carrier — overclaims.** "every … figure in one that its cited spans do not carry" omits that `counts.json` grounds any figure **regardless of the cited source** (wave 1 N3) and that a cited Registry title grounds its designator; §1's `7,572`/`78.7` carry no span and pass. The capability row adds the designator, never the counts leg.
- **Finding codes — incomplete.** `INF_NO_BULLETS` is emitted (`tools/inference-ground.py:282`, `v8-staronly` exit 1) and is missing from the Gates row's list.
- **Provenance — stale pin.** The row still reads `819f83eb…` while HEAD's blob is `3018b1d2…`; `3807537` rewrote the row's command cell and the tool but not the pin (`grep -c 3018b1d2 SKILL.md SCORECARD.md` → `0`/`0`). True at `d09fc8e7`, wrong for the gate the row describes now.

**Claim status: R46-C1 verifies as declared** (counter EXIT 0 over the pinned six at both commits; controls reproduce `0/3` and `1/3`). The class-(c) clause fails: no fixture (wave 1: `junk-borrowed` is class (b)) and no enforcement (§1, §3).

## 6. Smallest safe correction, and axes

1. Union every `####` heading beginning `inference` after the first, or emit `INF_SECTION_REPEATED` (≈4 lines, closes `v3`). 2. Refuse, not drop, a section line matching `^\s*([-*+]|\d+\.)\s` (≈4 lines, closes `v5`; `v1`/`v4` stay killed). 3. Add `INF_NO_BULLETS` to the Gates code list; pin `3018b1d2…` with the commit named. 4. `c1-count.py`: require every `junk-*.md` in the directory to exit 1 (or `FIXTURE_EXTRA` for names outside `PINNED`) — the predicate's wording. 5. Reword both SCORECARD cells to "a column-0 `- ` item in the first `#### Inference` section" and add the counts-manifest leg. No predicate, counter or target changes; kill rule intact.

**operability (C1):** the check is real but three fixtures wide; a reader-visible inference can still bypass it by list mark or section position, so the D7 class the claim exists to close stays open — as the verdict cell concedes. **calibration:** a stale byte pin and an undocumented finding code sit in a live `## Gates` row; the counter's set is tuples, not the directory the predicate names. **depth:** untouched directly; risk is a C3 entry reading "grounded" as "sound".

No lane file written except this report. No install. `/tmp/chousa-r46w2-CritC1D7/` removed.
