# MutC1Junk — mutation test of C1's gate (R46-C1, operability)

seat: L1Chousa46.MutC1Junk (mutation-tester, leaf)
date: 2026-10-25
target: `tools/inference-ground.py` + `corpus/evidence/round46/c1-count.py`
fixture under mutation: `corpus/fixtures/inference-ground-r46/positive-a.md`
scratch: `/tmp/chousa-r46-MutC1Junk/` (deleted at end)
No fetch, no network. No production file written. No install needed.

Bytes tested (working tree; `tools/inference-ground.py` is untracked in this wave):
- `tools/inference-ground.py` sha256 `61c09d7248c5b1cdb12cad3e980aa644a18433f63ca7f020e7363eabbe6aeac5`
- `corpus/evidence/round46/c1-count.py` sha256 `e7686236c811df493ead441f474b7d57fa9671934762a0a4ca673b12ff6c5d7a`

Pristine bytes before and after (unchanged):
`1378296857c6193d80ce9649f5778216003f10ffdd645c0461fa43c2c46b8a21`
(`corpus/fixtures/inference-ground-r46/positive-a.md`; identical sha256 in the
scratch copy). Baseline run of the tool on the pristine fixture:
`GROUND entry=positive-a.md section=1 bullets=1 tokens=1 grounded=1 / GROUND: PASS` EXIT=0.

## Grounding token map (why each mutant is falsifiable)

positive-a: `#### Inference` = one bullet, citation `(S901)`, one backticked
5-word token `the release ships a frozen pool`, **zero numerals**, span
`spans/S901-1.txt` = `the release ships a frozen pool of pages; no revision is recorded per sentence`.
So the numeral mutant (3) is *degenerate on this fixture* — handled by a
two-step probe (below), recorded as a fixture-coverage finding, not faked.

## The six assigned mutants (verbatim tool output)

Command form: `python3 tools/inference-ground.py --entry <m> --spans spans.tsv --counts counts.json --root .`

| # | mutant | tool output | exit | verdict |
|---|--------|-------------|------|---------|
| 1 | m1-drop-citation — `(`S901`)` removed from the bullet | `bullets=1 tokens=1 grounded=0 / FINDING INF_UNCITED bullet=1 / FINDING INF_TOKEN_NOT_IN_SPAN bullet=1 token='the release ships a frozen pool' / GROUND: FAIL` | 1 | **killed** |
| 2 | m2-word-swap — `frozen pool` → `frozen cache` inside the backticks | `FINDING INF_TOKEN_NOT_IN_SPAN bullet=1 token='the release ships a frozen cache' / GROUND: FAIL` | 1 | **killed** |
| 3 | m3b-numeral-4137 — grounded figure 5,959 replaced by 4,137 | `tokens=2 grounded=1 / FINDING INF_TOKEN_NOT_IN_SPAN bullet=1 token='4,137' / GROUND: FAIL` | 1 | **killed** (see numeral note) |
| 4 | m4-token-in-observation — token moved to `#### Observation` only | `tokens=0 grounded=0 / FINDING INF_UNGROUNDED bullet=1 / GROUND: FAIL` | 1 | **killed** |
| 5 | m5-fence-shadow — fenced `#### Inference` appended inside the section | `section=1 bullets=1 tokens=1 grounded=1 / GROUND: PASS` | 0 | **accepted — equivalent mutant** (correct: fenced headings are declared literal; the only bullet is still grounded, so the shadow changes no verdict) |
| 6 | m6-h2-inference — `#### Inference` → `## Inference` | `section=0 bullets=0 / FINDING INF_SECTION_ABSENT bullet=0 / GROUND: FAIL` | 1 | **killed** |

Mutant 3 note (probe pair, because positive-a carries no numeral):
- `m3a-grounded-numeral` (insert `5,959`, a value in `counts.json`): `tokens=2 grounded=2 / PASS` EXIT=0 — numeral leg works.
- `m3b` (same position, `4,137`): killed as above. 4,137 is the `junk-borrowed` figure and is absent from `counts.json` {7572, 5959, 78.7}.
- Finding N3: the tool accepts a counts value **regardless of which source the bullet cites** (`counts.json` is global, `--spans` binding is per-id). Declared by rule 4 (counts alternative), but it means "grounded numeral" ≠ "numeral bound to the cited source".

## Accepted mutants that ARE defects (coverage findings)

| probe | content | tool output | exit | finding |
|-------|---------|-------------|------|---------|
| P1 | `p1-fence-hides-bullet` — ungrounded bullet `- Therefore every claim is `independently re-verified against a live source` (`S901`).` inside a fenced block appended after the real bullet | `bullets=1 tokens=1 grounded=1 / GROUND: PASS` | 0 | **survives** |
| P4 | `p4-mid-fence-hides-bullet2` — two-bullet section, bullet 1 grounded, bullet 2 (ungrounded) inside a mid-section fence | `bullets=1 tokens=1 grounded=1 / GROUND: PASS` | 0 | **survives** |
| P2 | `p2-fence-block` — fenced block containing `#### Not An Inference` + an ungrounded bullet | `bullets=1 / PASS` | 0 | survives (same class) |
| P3 | `p3-unclosed-fence-before-heading` — ` ``` ` before the real heading | `section=0 / INF_SECTION_ABSENT` | 1 | killed (malformed entry) |

Cause (F-C1-a): `inference_bullets()` treats a line starting with ```` ``` ````
as a fence and, while the fence is open, skips `- ` lines instead of recording
them (`tools/inference-ground.py:81-88`: `if not fence:` gates the only `- `
branch, so a fenced bullet is never appended). Rule 2/3 say *every bullet of that
section*; a bullet inside a fence is in the section but is not enumerated, so it
escapes citation and grounding checks. This is the round-45 D7 class
(prose that asserts something else) entering through markdown structure rather
than through token mismatch. It is not named in the tool docstring's "Named
limit" (which speaks of semantics only) and not in claims.md.

Suggested one-line close (for the executor, not applied here): when a fence
opens inside the Inference section, either fail with `INF_FENCED_BULLET` on any
`- ` line held inside it, or strip empty fences before enumerating.

## Counter behaviour with mutants as the fixture set (`--root` on a copied tree)

Copied tree `/tmp/chousa-r46-MutC1Junk/tree/` = `tools/inference-ground.py` +
`corpus/fixtures/inference-ground-r46/`; one mutant substituted per row.

| row | substitution | counter output | exit |
|-----|--------------|----------------|------|
| A | pristine | `TOOL=present POSITIVE_PASS=3/3 JUNK_KILLED=3/3 C1=PASS` | 0 |
| B | m1 as `positive-a.md` | `POSITIVE_PASS=2/3 JUNK_KILLED=3/3 C1=FAIL` | 1 |
| B2 | m2 / m3b / m4 as `positive-a.md` | `POSITIVE_PASS=2/3 JUNK_KILLED=3/3 C1=FAIL` (each) | 1 |
| C | m5 as `positive-a.md` | `3/3 3/3 C1=PASS` | 0 |
| C2 | p1 as `positive-a.md` | `3/3 3/3 C1=PASS` | 0 |
| D | p1 added as `junk-fencehide.md` (extra file) | `3/3 3/3 C1=PASS` — file never read | 0 |
| E | p1 replaces `junk-borrowed.md` (a declared slot) | `3/3 JUNK_KILLED=2/3 C1=FAIL` | 1 |
| F | stub tool: exit 0 on `positive-*`, exit **2 (crash)** on `junk-*` | `3/3 3/3 C1=PASS` | 0 |

Declared controls reproduced exactly (`--tool`):
- always-exit-0 → `POSITIVE_PASS=3/3 JUNK_KILLED=0/3 C1=FAIL` EXIT=1 (matches claims.md).
- citation-presence-only → `POSITIVE_PASS=3/3 JUNK_KILLED=1/3 C1=FAIL` EXIT=1 (matches claims.md).

### Would the declared 3/3+3/3 catch the mutants?

- Killed mutants 1,2,3,4 **are** caught — but only *because* the counter reads
  exit codes: substituted into a positive slot they drop `POSITIVE_PASS` to 2/3.
  They are never exercised as junk, so the counter proves "tool rejects this
  body", not "tool rejects this junk class".
- Mutant 5 is accepted, correctly (equivalent).
- p1/p4 — the real survivors — are **not caught by the declared legs**: as an
  extra file the counter never opens it (row D), and the gate stays `C1=PASS`.
  They are caught only if a seat manually drops them into one of the three
  hard-coded junk filenames (row E). The fixture set is a frozen tuple
  (`POSITIVES`/`JUNKS` at `corpus/evidence/round46/c1-count.py:31-32`), so the
  directory is not a set the counter enumerates despite the predicate's wording
  "every `positive-*.md` / `junk-*.md` fixture of the directory".
- Row F: `JUNK_KILLED` counts any non-zero exit, so exit 2 (usage/crash) scores
  as a kill although claims.md declares junk must exit **1**. A tool that
  crashes on all junk would score full marks. Kill rule wording ("below 1/3 on
  either leg") does not exclude this.

## Verdict

- Gate behaves as declared for the four falsifiers it was built for
  (uncited · ungrounded · wrong word · moved token) and refuses a missing or
  re-levelled section. Those kills are real (finding classes named per bullet).
- One surviving defect class: **fenced bullets escape enumeration** (P1/P4,
  exit 0 on an inference that asserts `independently re-verified against a live
  source`), which is exactly the D7 class C1 exists to close. C1 as declared
  still verifies (its counters pass), but the operability claim "makes inference
  grounding executable" is one markdown fence short of the D7 class; recommend
  the executor add the fenced-bullet finding and a `junk-fenced.md` fixture in
  the same wave, before the claims freeze is cited as closed.
- Counter calibration limits to name in the verdict: fixed filename tuples,
  and `!=0` counting a crash as a kill.

## Restoration evidence

- `corpus/fixtures/inference-ground-r46/positive-a.md` sha256 after all runs:
  `1378296857c6193d80ce9649f5778216003f10ffdd645c0461fa43c2c46b8a21` (unchanged;
  all mutation done on copies under `/tmp/chousa-r46-MutC1Junk/`).
- No lane file written except this report; `/tmp/chousa-r46-MutC1Junk/` removed.
