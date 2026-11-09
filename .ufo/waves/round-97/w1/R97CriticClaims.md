# R97CriticClaims — adversarial reading of C1 and C2 at F 9a0ce2015fa0254848f2f32f612b20caf7dc5478

Attacked tree: shared clone of the lane at F, checked out at 9a0ce201 (`git -C $S/repo log -1` → `9a0ce201`). Scratch
`/fast/scratch/hyaku/chousa-r97/R97CriticClaims` removed before yield. Clone edits were made only in that scratch clone
and reverted (`git status --porcelain` clean after each run). No lane, fleet or sibling file was written.

Tools: no install; `git`, GNU `grep` (`/usr/bin/grep`), Python 3 stdlib only. Nothing installed or upgraded.

## C2 — entry depth: FIRED (two defects the instruments do not enforce)

### F1. The Citing row states a count the recount refutes (K5)

Entry line 72 (Lane cell of "Citing the checklist") says: `12 of the 26 S225 quotes are not found verbatim in S226`.
Recount (python, over `corpus/captures/80a844fe287a1a26d4280251.txt` with the entry's own `norm`):

- verbatim matches: 10/26 (agrees with the entry's `## Two reprints compared` and `ENTRY_CONTROLS` VERBATIM=10/26)
- NOT verbatim: **16** (L1 L2 L3 L4 L8 L11 L12 L13 L14 L15 L16 L18 L20 L21 L23 L26)
- NOT under letters: 12 (L1 L2 L3 L8 L11 L12 L13 L14 L15 L18 L20 L23) — the number 12 is the *letters* miss count,
  placed in a *verbatim* sentence.

Nothing checks a number inside a Lane cell. `entry-controls-r97.py` parses the Lane cell only for non-emptiness
(`lane_ok`, `cells[4]` truthy). The round-97 claim's own K5 ("stated corroboration counts differ from a recount")
is violated by this row. Receipt: `.ufo/waves/round-97/w1/R97CriticClaims-after-c2-all.txt` (the lane's ENTRY_CONTROLS
line is intact; the defect sits in the row, which the tallies do not read).

### F2. The breakdown of the 12 letter-misses is wrong (K5 by another route)

Entry `## Two reprints compared`: "Of the 12 not found under *letters*, 5 are element headings …, one is S225's own
pointer (L1), one the PRESS checklist title (L2), and five are questions where the wording itself differs … (L12, L20),
… (L15), … (L13 against L29)."

Recount of the 12 letter-misses: element headings are **6** (L3, L8, L11, L14, L18, L23 — "1. Translation…", "2. Boolean…",
"3. Subject…", "4. Text word…", "5. Spelling…", "6. Limits…"); wording differences are **4** (L12, L13, L15, L20). The
sentence's own named wording items total 4, not 5. The stated split (5 + 1 + 1 + 5) is not the split of the 12 quotes.

### F3. The Do/Never check does not reach Never cells (K2 — the stand-in)

Stand-in: in a clone-scratch copy of the entry, the Never cell of "Checking limits and filters" was inverted from
`apply a filter without citing where it comes from` to `apply a filter and always cite where it comes from, citing every filter`
— the warrant (L23, L24, L25) is unchanged; the Do cell is unchanged; the row keeps all its warrant terms.

Commands run on the stand-in (all from the clone root, exit codes observed):

- `python3 -B tools/gate-records.py verify --root . <entry>` → `GATE_RECORDS files=1 records=30 ok=30 fail=0`, rc 0
- `bash tools/research-gate.sh verify-metadata <entry> --root .` → `METADATA_COMPLETE=1/1`, `RESEARCH_GATE: CLEAN`, rc 0
- `python3 -B tools/search-rerun.py verify <entry> --root .` → `SEARCH_RERUN_SUMMARY searches=7 rev_match=7/7`, `SEARCH_RERUN: CLEAN`, rc 0
- `python3 -B corpus/evidence/round97/entry-controls-r97.py --root . --work <scratch>` → `ENTRY_CONTROLS=PASS`, rc 0,
  with `WARRANT_TERMS=8/8 LANE_FILLED=8/8 SOLE_SUPPORT=8/8 VERBATIM=10/26 LETTERS=14/26`

So the stand-in meets every printed tally with a Never cell that asserts the opposite of its warrant. The claim's
sentence "each cell … shares a content word" is enforced only for Do; the K2 kill rule ("a Do **or** Never cell asserting
what its warranting quotes do not say") has no instrument leg for Never. Receipt:
`.ufo/waves/round-97/w1/R97CriticClaims-c2-neverflip-standin.txt`.

### What held (C2)

- `SOLE_SUPPORT` as written (a row needs at least one S225 quote; S226-only rows are dropped): the tier-C forgery
  `sole-support-tierC` drops the tally 8→7, so the "never as a row's only support" leg is enforced as a row check.
- Gate 30 records, metadata, 7/7 rev-match: all run clean on the unmodified entry (after/c2-all.txt).
- Named limit (c) (letters across a line break in S226): not probed; no evidence either way this round.
- Tier/scope cells (K4) not probed beyond the captures' stated tiers; not claimed either way.

## C1 — operability: FIRED (the predicate line is reachable without the claimed property)

### F4. A self-test that hashes its own body passes the whole frozen battery

Stand-in (`.ufo/waves/round-97/w1/R97CriticClaims-search-rerun-hashself-standin.py.txt`): the lane's
`tools/search-rerun.py` at F, with a new module-level `_self_hash_ok()` that sha256s its own source (minus one
`_EXPECTED = ` line) and, when `selftest()` starts, prints `SEARCH_RERUN_SELFTEST: FAIL cases=0/47` and returns 1 unless
the hash equals the constant embedded at build time; otherwise it prints `SEARCH_RERUN_SELFTEST: PASS cases=47/47`
and returns 0. No case is run. Unmodified, it passes; any one-site mutation of its body fails it, which is exactly
the mutant-detection behaviour the battery measures.

Installed as the default tool in the scratch clone (reverted after), then:

`python3 -B corpus/evidence/round97/selftest-controls-r97.py --root . --work <scratch>` → rc 0,
`POSITIVE=1/1 EXTERNAL_KILLED=30/30 DO_NOTHING_REFUSED=1/1 R96_MUTANTS_KILLED=23/23 ORACLES_REJECTED=3/3 NO_WRITE=1/1 REGRESSION_R95=2/2 BASE_KILLED=10/30 CASES=47`,
`SELFTEST_CONTROLS_R97=PASS`.

So the printed tallies of the frozen counter do not distinguish 47 real cases from a hash check. The battery's three
oracles (constant PASS, hollow self-test, always-FAIL) are the only stand-ins it tests; they fail for reasons unrelated
to hashing (the hollow stub and always-FAIL both fail NO_WRITE/POSITIVE and are rejected). Receipt:
`.ufo/waves/round-97/w1/R97CriticClaims-c1-hashself-standin-full.txt`.

Consequence for the sentence: "runs 47 in-memory cases" is printed, not enforced; the only enforcement of "cases" is the
literal line `PASS cases=47/47`, which the stand-in prints. The claim's own named limit (b) covers the guard, not this.

### F5. The battery's external set is not wholly "read from committed bytes" (docstring says "never retyped here")

Docstring line 8 of `corpus/evidence/round97/selftest-controls-r97.py`: "read from the committed round-96 bytes (never retyped
here)". The two `SENTINEL` entries (`s1-no-replace-objects`, `s2-partial-scrub`) are hard-coded strings in the battery.
`s2`'s new/old lines match `R96SentinelC1-partial-git-scrub.txt`; `s1`'s exact `env.update({"GIT_NO_REPLACE_OBJECTS": "1", ...})`
line is **not** in `R96SentinelC1-replace-refs-false-clean.txt` (`grep -c` of the literal fragment: 0, rc 1). The claim
sentence itself separates the two ("the 28 … read … plus two `git_env` mutants R96SentinelC1 reported"), so the claim is
not false; the docstring is. The sentinel's text is a transcription, and nothing checks it against the seat's bytes.

### F6. The battery's stand-in leg runs only with the default tool, and `--no-regression` drops two tallies

From the code: `ORACLES` and `REGRESSION_R95` are gated on `default_tool` (`--tool` unset) and `not a.no_regression`.
The `before/c1-base.txt` run used `--tool <base> --no-regression`, so its printed line omits `ORACLES_REJECTED` and
`REGRESSION_R95`; a `--tool` run that prints PASS therefore exercises none of the oracles and none of the r95 leg.
The predicate line in the claim lists those tallies; a `--no-regression` run is permitted by the claim's own
"(`--no-regression` skips the slow r95 leg)" but then the printed line is not the predicate line. Minor, stated for the record.

### What held (C1)

- `SEARCH_RERUN_SELFTEST: PASS cases=47/47` is what the tool at F prints (after/c1-all.txt, exit 0) — not attacked further.
- The do-nothing control: `before/c1-base.txt` shows `POSITIVE=0/1 EXTERNAL_KILLED=10/30 … BASE_KILLED=10/30` and
  `SELFTEST_CONTROLS_R97=FAIL`; the base tool's `--selftest` line `PASS cases=32/32` (before file header) matches. The base
  n11/n12/n13/n26 rows read `rc=1 SURVIVED failed=-` (traceback, no FAIL line), consistent with the battery's rule.
  Read as held: the base is scored by the frozen counter, not a patched copy.
- NO_WRITE: the stand-in ran with cwd/HOME/TMPDIR in an empty directory and returned `left=[] status_same=True diff_same=True`.
- Harm leg (K4): `c1-verify-harm-and-c2-separable.txt` shows `SAME` for the three `verify` entries against base; the
  round-95 leg passed in the default run of the stand-in too (`regression-rerun-controls-r95 rc=0`, `regression-mutants-r95 rc=0`).

## Named-limit checks

- C1 (a) "fresh mutant elsewhere may survive": not probed; not needed to fire F4.
- C1 (d) `verify` ↔ `evaluate` tie: not probed; stated as a limit.
- C2 (a) "rows' wording is a paraphrase": the Never-flip stand-in (F3) is the direct evidence that the instruments cannot
  distinguish a faithful Never cell from an inverted one; the claim's named limit (a) then reads as the whole Never leg.

## Commands and exit codes (observed)

- `git clone -q --shared …/chousa-shokunin $S/repo && git -C $S/repo checkout -q 9a0ce2015fa0254848f2f32f612b20caf7dc5478` → 0; `git log -1` → `9a0ce201`
- python recount of S225 vs S226 (verbatim/letters): 10/26 verbatim; 16 not verbatim; 12 not letters
- `tools/gate-records.py verify` on the Never-flip stand-in → rc 0, `records=30 ok=30 fail=0`
- `tools/research-gate.sh verify-metadata` on the stand-in → rc 0, `RESEARCH_GATE: CLEAN`
- `tools/search-rerun.py verify` on the stand-in → rc 0, `rev_match=7/7`, `SEARCH_RERUN: CLEAN`
- `corpus/evidence/round97/entry-controls-r97.py` on the stand-in → rc 0, `ENTRY_CONTROLS=PASS`
- `tools/search-rerun.py --selftest` with the hash-self stand-in → rc 0, `SEARCH_RERUN_SELFTEST: PASS cases=47/47`
- `corpus/evidence/round97/selftest-controls-r97.py --root . --work <scratch>` with the hash-self stand-in as default tool → rc 0, `SELFTEST_CONTROLS_R97=PASS`, tally as predicate
- `grep -c 'GIT_NO_REPLACE_OBJECTS": "1", "GIT_NO_LAZY_FETCH"' R96SentinelC1-replace-refs-false-clean.txt` → 0, rc 1

## Receipts (copied to .ufo/waves/round-97/w1/)

- `R97CriticClaims-c2-neverflip-standin.txt` — F3 counting-command outputs (rc 0 each)
- `R97CriticClaims-c1-hashself-standin-full.txt` — F4 battery output and rc
- `R97CriticClaims-search-rerun-hashself-standin.py.txt` — the stand-in tool source
- `R97CriticClaims-before-c1-base.txt`, `R97CriticClaims-before-c2-base.txt` — do-nothing controls read as held
- `R97CriticClaims-after-c2-all.txt` — the unmodified C2 counting output (ENTRY_CONTROLS line intact)

## Recommended smallest correction (for the canonical planner)

1. Lane cell of "Citing the checklist": replace "12 of the 26 … not found verbatim" with "16 of the 26 … not found verbatim
   (10 verbatim)" and the `## Two reprints compared` split with the recount (6 headings, 4 wording differences; L26 under letters).
2. Add a Never-cell check to `entry-controls-r97.py` (for example a per-row content-word check on the Never cell against the warrant, or a
   negation-polarity check), and a `CELLNUM` check that a number in a Lane cell equals its recount.
3. For C1: have the battery run the 47 cases by name (e.g. require every `SELFTEST pNN/rNN/...` line to be printed with its
   own ok) and reject a printed PASS whose case lines are absent; change the docstring's "never retyped" to name the two sentinel strings as transcribed.

VERDICT: R97CriticClaims C1 fired — the frozen battery passes a hash-of-self self-test (F4) with all printed tallies equal to the predicate, so "runs 47 in-memory cases" is printed, not enforced; the sentinel docstring claim is also overstated (F5).
VERDICT: R97CriticClaims C2 fired — the Lane cell's "12 of the 26 … not found verbatim" is refuted by the recount (16), the 12 breakdown is misstated (6 headings, 4 wording), and an inverted Never cell passes every counting command (F1–F3).
