# ScribeC1Rows — round 47 wave 1, C1 description rows (scribe)

Item: draft (a) the replacement `## Gates` row for `inference-ground`, (b) QUALITY criterion 67,
(c) a SCORECARD capabilities row "polarity probe in the inference check"; run tool and counter once.
Axes: operability, calibration, depth. Tree: lane HEAD `a15610a59aaeaf43b79ccc650acee4bd4da00341`
(the C1 landing); `tools/inference-ground.py` and the fixtures are unmodified in the working tree
(`git status --short` lists only round-40/41 registries, `round41/receipts/cells/cells.json`, round-47 wave files).
No lane file written except this report. No install. Scratch `/tmp/chousa-r47-ScribeC1Rows/` removed (`ls` → No such file).

## Observed (commands from the lane root)

```
$ sha256sum tools/inference-ground.py ; git rev-parse HEAD:tools/inference-ground.py
8899e7868ffb66fd0d58162342a20a2ab6f3a0e1aee7d0d5b36aa1b7fd7a0a40  tools/inference-ground.py   (git blob 1685016b…)
$ git show a15610a5:tools/inference-ground.py | sha256sum   → 8899e786…7a0a40  (= working tree)
$ git show 45ede9c:… | sha256sum ; git show 9a9f94db:… | sha256sum   → c3ea067e…bbb3 both
$ grep -n inference-ground corpus/evidence/round46/measure-after.txt  → :7 `### sha256 tools/inference-ground.py c3ea067e…bbb3`
$ python3 corpus/evidence/round47/c1-count.py      (sha256 6d39dce5…0cc7, frozen at 22a44b8)
TOOL=present  POSITIVE_PASS=3/3  JUNK_KILLED=3/3  CANARY=pass  R46_COUNTER=pass  R46_ENTRIES=2/2  C1=PASS   exit=0
$ python3 corpus/evidence/round47/c1-count.py --tool corpus/evidence/round47/controls/base-tool-r46.py   (sha256 c3ea067e…)
TOOL=present  POSITIVE_PASS=3/3  JUNK_KILLED=0/3  CANARY=fail  R46_COUNTER=pass  R46_ENTRIES=2/2  C1=FAIL   exit=1
$ python3 tools/inference-ground.py --entry $D/<f>.md --spans $D/spans.tsv --counts $D/counts.json --root $D   (D=corpus/fixtures/inference-ground-r47)
positive-negation-kept / positive-affirmed / positive-figure-negated: `GROUND … bullets=1 tokens=1 grounded=1` `GROUND: PASS` exit=0 each
junk-flip-asserted  FINDING INF_POLARITY_FLIP bullet=1 token='no revision is recorded / revised'            exit=1
junk-flip-denied    FINDING INF_POLARITY_FLIP bullet=1 token='the release ships a frozen pool / frozen'     exit=1
junk-flip-figure    FINDING INF_POLARITY_FLIP bullet=1 token='7,572 / counts key answers_named_source'     exit=1
$ python3 tools/inference-ground.py --entry corpus/knowledge/evidence-pool-versioning-r39{,-amendment-2026-10-23}.md --spans corpus/evidence/round46/spans.tsv --counts /dev/null --registry corpus/SOURCES.md --root . | tail -2
… bullets=4 tokens=7 grounded=7 / GROUND: PASS ;  … bullets=4 tokens=5 grounded=5 / GROUND: PASS
```
(The `exit=0` printed after `| tail -2` is tail's; the entries' exit 0 is evidenced by the counter's `R46_ENTRIES=2/2`.)

Named-limit probe (/tmp copy of `junk-flip-asserted.md`, `revised` → `edited`, same fixture spans/counts):
`GROUND entry=limit-synonym.md section=1 bullets=1 tokens=1 grounded=1` · `GROUND: PASS` · exit=0 — a different-stem flip passes, as declared.

## (a) Replacement `## Gates` row (SKILL.md:117; entry cell unchanged)

```
| `inference-ground` (r46; polarity probe r47) | tool | `python3 tools/inference-ground.py --entry PATH --spans TSV --counts JSON --registry corpus/SOURCES.md [--root DIR] [--json OUT]` | exit `0` grounded, no findings (`GROUND entry=… section=N bullets=N tokens=N grounded=N`, `GROUND: PASS`) · exit `1` findings, one or more `FINDING` lines naming the bullet, `bullet=0` for section-level findings (`INF_SECTION_ABSENT`/`INF_NO_BULLETS`/`INF_UNCITED`/`INF_UNGROUNDED`/`INF_TOKEN_NOT_IN_SPAN`/`INF_POLARITY_FLIP`; an uncited bullet emits `INF_UNCITED` and its token finding; `INF_POLARITY_FLIP` names `<phrase> / <bullet word>` or `<figure> / counts key <key>`) · exit `2` usage or a missing/unreadable entry (an unreadable `--spans`/`--counts`/`--registry` reads as empty and fails closed at exit `1`) | `python3 corpus/evidence/round47/c1-count.py` → `TOOL=present POSITIVE_PASS=3/3 JUNK_KILLED=3/3 CANARY=pass R46_COUNTER=pass R46_ENTRIES=2/2 C1=PASS` exit 0 over `corpus/fixtures/inference-ground-r47/` (fixture bytes pinned; `R46_COUNTER` re-runs `corpus/evidence/round46/c1-count.py` on this tool); controls `corpus/evidence/round47/controls/c1-controls.txt`: round-46 tool `JUNK_KILLED=0/3`, always-exit-1 `POSITIVE_PASS=0/3`, negator-word refuser `POSITIVE_PASS=1/3 R46_ENTRIES=0/2`, all exit 1; limits: lexical — citation and token presence plus a stem-sharing polarity probe, NOT entailment: a flip through a synonym or a different-stem antonym (`revised` vs `edited`), or beyond the word windows (3 before / 2 after a scope word; 4 after a counts figure), still passes; a phrase's polarity is read from the first cited span carrying it; the figure leg covers only figures grounded by the counts manifest; 1–2 digit figures are never tokens; a cited document's designator (`RFC 7089`) grounds its own numeral only | sha256 `8899e7868ffb66fd0d58162342a20a2ab6f3a0e1aee7d0d5b36aa1b7fd7a0a40` at commit `a15610a5` (round-46 blob `c3ea067e…`, `corpus/evidence/round46/measure-after.txt:7`, is history); span files named in the manifest must stay inside the manifest's directory | read-only (no network); `--json OUT` writes exactly the named path | chousa |
```

## (b) QUALITY.md criterion 67 (append after :639)

```
## Round-47 addition (appended 2026-10-25; criteria 1–66 unchanged)

67. **An inference must not assert the opposite of a phrase it quotes.** A
    bullet under `#### Inference` (a column-0 `- ` or `* ` item of any such
    section) that quotes a phrase its cited span negates must not use that
    phrase's words un-negated in its own text, one that quotes a phrase the
    span affirms must not negate those words, and a figure taken from a counts
    key must keep the key's polarity (`answers_without_archive_key` is followed
    by a negator, `answers_named_source` is not). Check: `python3
    tools/inference-ground.py --entry <entry> --spans <spans.tsv> --counts
    <counts.json> --registry corpus/SOURCES.md --root .` — exit 1 with a
    `FINDING INF_POLARITY_FLIP` line names the phrase or figure and the
    bullet's word; the gate is `python3 corpus/evidence/round47/c1-count.py`
    (`C1=PASS`, exit 0). Shown able to fail: `junk-flip-asserted.md` (span
    "no revision is recorded", bullet "is revised"), `junk-flip-denied.md`
    (span "the release ships a frozen pool", bullet "not frozen") and
    `junk-flip-figure.md` (`7,572` from `answers_named_source`, bullet "name
    no source") of `corpus/fixtures/inference-ground-r47/` each exit 1 with
    that finding, and the round-46 tool scores them `JUNK_KILLED=0/3`, exit 1
    (`corpus/evidence/round47/controls/c1-controls.txt`). Named limit: the
    probe only sees a flip that shares a five-letter stem with the quoted
    phrase inside its word window — `edited` for `revised` passes — so meaning
    stays a reader's check. — `lessons/round-47.md`.

    Note on 66 (round 47): its named limit ("correct tokens strung into an
    assertion of the opposite still pass") now holds only for flips criterion
    67's probe cannot see; the round-46 demonstration stays as history.
```

## (c) SCORECARD capabilities row (new `## Capabilities (round-47 addition)` table, header as :2476)

```
| polarity probe in the inference check | refuses (`INF_POLARITY_FLIP`, exit 1) an `#### Inference` bullet whose own words assert the opposite polarity of a phrase its cited span carries, or re-denominate a counts figure against its key's polarity — stem-sharing flips only; a synonym or different-stem antonym still passes | `tools/inference-ground.py` (rule 5, sha256 `8899e786…`, `a15610a5`); `corpus/evidence/round47/c1-count.py`; `corpus/fixtures/inference-ground-r47/`; `corpus/evidence/round47/controls/c1-controls.txt` | 47 |
```

## Findings

1. **`INF_NO_BULLETS` is already in the live row** (SKILL.md:117, `…/INF_SECTION_ABSENT`/`INF_NO_BULLETS`/…); CritC1D7 §5 routed it and `45ede9c` landed it. The draft keeps it; the only new code is `INF_POLARITY_FLIP` (`tools/inference-ground.py:418,425`; `INF_NO_BULLETS` at `:440`).
2. **Stale pin, confirmed.** The row points to `measure-after.txt`, which names `c3ea067e…` (the blob at `9a9f94db` and `45ede9c`); the tool at HEAD `a15610a5` is `8899e786…`. The draft pins it directly.
3. **Verdict-map wording corrected to observed output.** The tool prints `section=N` (every run above), which the live row leaves out. The draft also takes the docstring's exit-2 and fail-closed wording (`tools/inference-ground.py:41-42`).
4. **Bullet subject narrowed so it doesn't overclaim (CritC1D7 §5).** At HEAD, `inference_bullets` (`:78-128`) reads every `#### Inference` section and only column-0 `- `/`* ` items. Criterion 67 says exactly that. `+ `, `1. ` and indented items ahead of the first bullet were not probed here [INFERENCE: whether they escape is unverified this round].
5. **Out of scope, routed:** SKILL.md:70 (`Run:` bullet) still says the tool "does NOT enforce that the inference follows (round 46, QUALITY 66)" and doesn't mention rule 5. It needs a one-clause update when (a) lands. `corpus/lessons/round-47.md` doesn't exist yet. The `— lessons/round-47.md` pointer in (b) only resolves once it is written.
6. **Over-refusal not measured.** The five-letter prefix (`stem = w[:5]`, `:242-243`) could refuse a correct bullet that shares a prefix with a scope word. Only the three positives and the two round-46 entries show no false positives [INFERENCE: other collisions are untested].

## Verdict

All three drafts are grounded in observed runs. C1 reads `C1=PASS` exit 0 at `a15610a5`, and the round-46 tool reads `JUNK_KILLED=0/3` exit 1. The named limit reproduces: a different-stem synonym flip passes with exit 0. No predicate, counter, fixture, floor or target was touched.
Axes: operability, the gate row now names the code and pin it enforces; calibration, the stale pin and the overclaim of bullet scope are both removed; depth, untouched.
Checks for the main agent after landing (a)–(c): `python3 corpus/evidence/round47/c1-count.py`, `python3 corpus/evidence/round47/c2-count.py --list` (the row's entry cell is unchanged, so no new DANGLING is expected), and `grep -c 8899e786 SKILL.md SCORECARD.md`.
