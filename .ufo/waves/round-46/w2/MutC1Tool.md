# MutC1Tool — mutation test of C1's gate (R46-C1, operability)

seat: L1Chousa46.MutC1Tool (mutation-tester, leaf)
date: 2026-10-25
target (frozen): `tools/inference-ground.py` at `d09fc8e7`, sha256
`819f83ebdc6c6b47d83216f5403824c152ba1f12f09c88b16e2e1184275326bc` (276 lines),
extracted with `git archive d09fc8e7 | tar -x -C /tmp/chousa-r46w2-MutC1Tool`.
counter bytes scored: `corpus/evidence/round46/c1-count.py` sha256
`8473abf6c4437beda5e8ba53e3045e5e47d994c87294707c745fc6493c69e03a` (snapshot in
scratch; includes the `CANARY=` leg). The counter changed mid-wave
(`e7686236` → `8473abf6`), so every score below was re-derived on the snapshot.
scratch: `/tmp/chousa-r46w2-MutC1Tool/` (deleted at end). No fetch. No lane file
written except this report. No install needed.

Command form (all rows):
`python3 snap/x/y/counter.py --root /tmp/chousa-r46w2-MutC1Tool --tool <mutant>`
fixtures are the pinned ones inside that tree (baseline `C1=PASS` exit 0 before
and after the probes, so no fixture byte moved).

## The four assigned mutants

| id | mutation (applied to a copy only) | sha256 |
|----|-----------------------------------|--------|
| A | dropped the whole `--registry` leg: `--registry` arg (frozen `:217`), `titles = registry_source(...)` (`:239`), designator block (`:254-256`), and `registry_source` (`:166-181`) | `bbd65c289451d429…ac3342` |
| B | dropped the section-end break `if not fence: … break` (frozen `:88-91`) | `2485f371ca41aa81…08dbd2` |
| C | `grounded = span_texts(spans, cited)` → `grounded = [bullet] if cited else []` (frozen `:248`) — any non-empty cited set accepted, spans never read | `e54a20ea09d617d0…275cc2` |
| D | dropped the counts leg `ok = any(v in values for v in numeral_variants(tok))` (frozen `:252-253`) | `6967fd5f7a9856cb…30a988` |

All four compile (`py_compile`) and run without traceback.

## Verdicts (counter output is verbatim; per-fixture exit codes from the mutant itself)

| id | expected detector | per-fixture outcome | counter | verdict |
|----|-------------------|---------------------|---------|---------|
| A | a fixture whose only figure is grounded by a cited Registry title, run with `--registry` | all 6 fixtures unchanged: positives 0,0,0; junks 1,1,1 | `POSITIVE_PASS=3/3 JUNK_KILLED=3/3 CANARY=pass C1=PASS` exit 0 | **survived** |
| B | a fixture with any bullet after the `#### Inference` section | all 6 fixtures unchanged: positives 0,0,0; junks 1,1,1 | `POSITIVE_PASS=3/3 JUNK_KILLED=3/3 CANARY=pass C1=PASS` exit 0 | **survived** |
| C | `junk-ungrounded` and/or `junk-borrowed` | `junk-ungrounded.md` exit **0** `GROUND: PASS`; `junk-borrowed.md` exit **0** `tokens=3 grounded=3 PASS`; `junk-uncited.md` still exit 1 | `POSITIVE_PASS=3/3 JUNK_KILLED=1/3 CANARY=pass C1=FAIL` exit 1 | **killed** (pair: mutant C × `junk-ungrounded`, mutant C × `junk-borrowed`) |
| D | `positive-b` (its only grounding is the counts manifest) | `positive-b.md` exit **1** `FINDING INF_TOKEN_NOT_IN_SPAN bullet=1 token='5,959'`; other five unchanged | `POSITIVE_PASS=2/3 JUNK_KILLED=3/3 CANARY=pass C1=FAIL` exit 1 | **killed** (pair: mutant D × `positive-b` only) |

Kill-reading: C dies on the **junk leg** (1/3) because both span-checked junk
classes collapse once the span lookup is skipped; `junk-uncited` survives C
because the citation leg is untouched. D dies on the **positive leg** (2/3)
because `5,959` is absent from `spans/S902-1.txt` (capture text is
`the archived copy is dated at build time; a placeholder value is not an archive link`)
and the counts manifest was its only credential. No positive fixture is killed
by C, no junk fixture by D — the two legs are genuinely independent.

## Hole A — the registry leg is never invoked, by the harness or by any fixture

`corpus/evidence/round46/c1-count.py:65-68` passes exactly `--entry --spans
--counts --root`; `grep -c registry` on the counter is **0**. So
`registry_source()` and the designator block are dead on every scored run, and
no frozen fixture needs them:

- `positive-a` / `positive-c` ground by span substring; `positive-b` by
  `counts.json` (`:252-253`); `junk-*` are refused by absence.
- Proof the leg exists and is behaviourally live (probe `probeA.md`, bare
  numeral `RFC 7089` with `(S079)`):
  pristine **with** `--registry corpus/SOURCES.md` → `tokens=1 grounded=1 GROUND: PASS` exit 0;
  pristine **without** → `FINDING INF_TOKEN_NOT_IN_SPAN token='7089'` exit 1;
  mutant A with `--registry` → `error: unrecognized arguments: --registry` exit 2;
  mutant A without → exit 1, identical to pristine.
- Consequence: mutant A is *equivalent to pristine for every invocation the
  counter makes*, which is why it scores 3/3+3/3. The fixture set pins neither
  the leg nor its narrowing (`tools/inference-ground.py:180` stores `cells[1]`
  whole in the frozen bytes, so a URL run inside the cell would ground a
  figure — wave-1 `ReviewerC1Tool` fixed that only in the working tree).

Named hole: **no `--registry`-dependent fixture; the counter never passes
`--registry`, so the registry / document-designator credential is unscored.**
`SKILL.md:116` registers the invocation *with* `--registry corpus/SOURCES.md`,
so the documented command exercises a path the counting command cannot see.

## Hole B — nothing after the Inference section is scored

Every fixture ends at its inference bullet, so removing the section-end break
(`:88-91`) changes no scored byte. The mutant is **not equivalent** — probe
`probeB.md` = `positive-c.md` + `## Unknown` bullet `- … `an unrecorded
revision ledger` … (`S902`).` :
pristine → `bullets=1 GROUND: PASS` exit 0; mutant B → `bullets=2 / FINDING
INF_TOKEN_NOT_IN_SPAN bullet=2 token='an unrecorded revision ledger'` exit 1.
Direction matters: without the break the tool is **stricter**, so B cannot let
junk through; the uncovered damage is the positive leg (a well-formed entry
carrying any bullet after its Inference section is wrongly refused). No frozen
fixture is such an entry, so B survives.
(Code-read, not run: `:74` matches `#### Inference*` by prefix, so
`#### Inference Notes` also opens the section; no fixture exercises the prefix.)

Named hole: **no fixture has a heading or bullet after `#### Inference`.**

## Extra finding — the working tree's tool crashes on a leading fence (not one of the four)

The lane working tree no longer holds the frozen bytes: `tools/inference-ground.py`
is now sha256 `3018b1d25d76205496ae002600003f5ddb4294328be4741b9fa58c8ddc223f07`
(uncommitted wave-1 edits, `diff` vs `d09fc8e7` shown in scratch). Line 71 adds
`if cur is not None: bullets.append(cur)` **inside the first scan loop**, before
`bullets, cur, fence = [], None, False` (`:79`) binds them. Run on a positive
entry with a fenced block above `#### Inference`:
`UnboundLocalError: cannot access local variable 'cur' where it is not
associated with a value`, exit **1** — indistinguishable from "findings", not
the declared exit 2. The frozen bytes handle the same probe: `GROUND: PASS`
exit 0. The lane's counting command resolves the tool from the working tree, so
a rerun scores these bytes; C1 still reads `C1=PASS` only because no frozen
fixture has a leading fence. This is a live operability defect in the tool the
Gates row registers, uncovered by the fixture set.

## Restoration evidence

- `tools/inference-ground.py` in the scratch tree: `819f83eb…09532bc` before and
  after every run (unmodified; all four mutations live in `mut/{a,b,c,d}.py`).
- No fixture byte written; the counter's `PINNED` gate still passes
  (`TOOL=present POSITIVE_PASS=3/3 JUNK_KILLED=3/3 C1=PASS` exit 0 after the probes).
- Working-tree tool re-read after the probes: `3018b1d2…c223f07` (unchanged by me).
- `/tmp/chousa-r46w2-MutC1Tool/` removed. Nothing written in the lane except this report.

## Verdict

C1 as declared still verifies: its counter passes on the frozen tool, and two
of the four attacks (C, D) are killed on different legs with a named decider.
The two survivors are coverage holes in the fixture set, not in the claim's
arithmetic: (A) the `--registry` / document-designator credential is unscored
because the counter never passes `--registry`, and (B) post-section text is
unscored because every fixture ends inside its Inference section. Both are
fixable by fixtures alone — a junk entry whose only figure is a Registry-title
designator scored under `--registry`, and a positive entry with a trailing
`## Unknown` bullet. Separately, the working-tree tool has regressed into an
`UnboundLocalError` on any entry with a leading code fence (exit 1), which the
current fixture set cannot see; that byte-level defect should be fixed before
the Gates row's registered command is cited as operable.
