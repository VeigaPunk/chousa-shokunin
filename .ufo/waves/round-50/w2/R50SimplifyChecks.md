# R50SimplifyChecks — YAGNI review of the round-50 additions

Seat: simplifier, round 50 wave 2. Scope: the six checks, `controls/build-c2-controls.py`,
`.ufo/waves/round-50/assemble-quotes.py`, `build-lesson.py`. Lane files untouched: `git -C . diff --stat`
over those nine paths prints nothing; every mutation below ran on a copy under
`/dev/shm/chousa-r50-R50SimplifyChecks/` (deleted at the end). No tool installed (pacman paused; none needed).

## Method and measurement window

Baseline (19:1x, before a sibling write; commands run from the lane root, `TMPDIR` in scratch):

```
c1-count.py                 LEGS=5/5 C1=PASS rc=0
c2-count.py                 ENTRIES=3/3 BOUND=3/4 REFUSED=1 QUOTE_ROWS=55 ... C2=PASS rc=0
stale-count-check.py        STALE_HITS=8 UNRESOLVED=2 STALE_COUNT=FAIL rc=1
wave-complete … --rev 5275c892 --lane .   8 MISSING, OK 27/35, rc=1
wave-complete … w1-spec w1               13 MISSING, OK 29/42, rc=1
name-collision … w1-spec.json             NAME_COLLISIONS=13 ITEMS=42 rc=1
cited-id … renumber.tsv <3 lane entries>  CITED_IDS=FAIL rows=5 rc=1
cited-id … renumber.tsv <3 package entries> CITED_IDS=PASS rows=5 rc=0
decode-form round-47.md / round-50.md     FORM_MISSING rc=1 / FORM_NAMED rc=0
cjk-ground --old old-ig.py                A/B/C PASS, CJK_GROUND=PASS rc=0
controls/build-c2-controls.py             STAGED C2=FAIL · TOOLED C2=FAIL rc=0
assemble-quotes --out scratch             ROWS 55 {S104:18,S105:34,S106:3} + `SHORT S107 0`; bytes == quotes.tsv
build-lesson (L pinned to scratch)        rows 55; 27360 bytes == committed lesson
```

`old-ig.py` = `git show 3c51da77…:tools/inference-ground.py` (sha256 `fa2b4eb5…`; lane tool `33d4a37f…`).
Each deletion below: copy script to scratch, delete the named lines, re-run that check's documented command,
compare full stdout+rc with the unmutated copy.

## Deletions proven no-op (recommended)

| # | file:line | deleted | command re-run | observed |
|---|---|---|---|---|
| 1 | `stale-count-check.py:55,58` | `--receipt` flag and its only use | `stale-count-check.py --root <lane>` | IDENTICAL (8 hits, FAIL, rc 1) |
| 2 | `wave-complete-check.py:29` | `isinstance(it, str)` item branch | both legs above | IDENTICAL |
| 3 | `wave-complete-check.py:32-33` | name dedupe `if n not in out` | both legs | IDENTICAL |
| 4 | `name-collision-check.py:23,32` | `--round` flag + `a.round` | `name-collision-check.py <w1-spec>` | IDENTICAL (13 collisions, rc 1) |
| 5 | `build-c2-controls.py:32,33` | `corpus/evidence` and `corpus/lessons` mkdirs | `build-c2-controls.py` | IDENTICAL (both C2=FAIL) |
| 6 | `build-c2-controls.py:34` | `ignore=ignore_patterns("controls","c1-fixtures")` | same | IDENTICAL |
| 7 | `assemble-quotes.py:23,54-55` | `--min` flag + SHORT loop | `assemble-quotes.py --out <scratch>` | quotes.tsv bytes SAME; stdout loses only `SHORT S107 0` |
| 8 | `stale-count-check.py:20` | `CAPTURE_BOUND=(\d+)/\1` pattern | `stale-count-check.py --root <lane>` | IDENTICAL |

Notes on 1, 2, 4, 7, 8. No caller passes `--receipt`, `--min` or `--round` (`grep -rn -- '--receipt|--min|--round'`
over `corpus/`, `.ufo/waves/round-50/`, `SKILL.md` hits only each script's own docstring). Every spec item in
`.ufo/waves/**` is a dict, so the str branch is unreachable. `SHORT S107 0` is printed on every run and reports
the deliberately refused 教师 manual as short; no receipt records assemble-quotes' stdout (quotes.tsv is the
artifact and it is byte-identical). 8 is a genuine no-op *at tip*: the only prose hit of the form is
`LOG.md:1803` `CAPTURE_BOUND=28/28`, which duplicates that same line's `28 located quotes`, and `said()` dedupes
it — but QUALITY 74 names the pattern, so deleting it narrows a written criterion; I name it, I do not recommend it.

## Unexercised, kept (a deletion would weaken a stated rule — do not re-litigate)

- `stale-count-check.py:74` value-quote guard `set(nums[j-1]) <= quoted[j]`: IDENTICAL at tip (all three landed
  corrections quote the value they supersede); it is the docstring rule "may quote the value it supersedes".
- `stale-count-check.py:70-71` branch for a count ON a correction line: DIFFERS (`:786` prints RESOLVED) — live.
  `:19` dedupe: DIFFERS (hit count) — live.
- `wave-complete-check.py:49` `os.getcwd()`, `:51` `rel == "."`, `:52` empty-items die, `:55-56` outside-lane die:
  IDENTICAL only because the receipted invocations always pass `--lane` and a report dir inside the lane.
- `cited-id-check.py:20-22` NO_ROWS (vacuity guard; an empty table would otherwise print PASS rows=0), `:26` `\b`
  (without it `source: S1180` satisfies `S118`), `:24` blank-row filter (dead at tip, 1 clause).
- `decode-form-check.py:18`: **any one** alternative can be dropped and both documented runs stay IDENTICAL
  (round-50 matches `backtick-txt`, `txt-40-UTF8` and `decode form`; `utf-8-sig`/`UTF-16LE` match only round-49
  lessons). QUALITY 76 names all three forms, so keep — but the overlap is three-way, not one form each.
- `cjk-ground-check.py:22` `--tool`: IDENTICAL only together with its call site; it is the sole way to point the
  check at a mutant tool, i.e. the mutation-test entry point. Keep.
- `cjk-ground-check.py` fixture values: garbling spans.tsv cells 3,4,6,7 (`capture_sha256`, `offset`, `quote`,
  `entry`) and reg.md cells 3-11 leaves `CJK_GROUND=PASS` IDENTICAL — `inference-ground.span_texts` reads
  cells[0] and cells[4] only, `registry_source` cells[0..1]. The 7-cell / 11-cell COUNT is load-bearing
  (`len(cells) != 7` → skip; `len(cells) == 11`). Fixture must keep the shape, not the values.
- `assemble-quotes.py:36` limit filter: bytes SAME when deleted at tip (no candidate trips 25 words/160 chars).
  It is the located-quote rule, and `c2-count.py` enforces the same limits again (`QUOTE_SHORT`). Exercised
  elsewhere: the `any(t.count(q) > 1 …)` clause at `:33` was inert at 19:1x and is live at 19:29 (deleting it
  adds one S107 row), and the `QUOTE` machine-line branch is live (13 of 62 rows come from it).

## Duplication (second authorities; no deletion proposed)

1. `build-spans.py` (207 ln) and `quote-substance-check.py` (68 ln) are the round-49 files: `diff` after
   normalising `round 49→50` leaves 8 and 10 changed lines. 275 lines duplicated (claims-erratum item 3).
2. Capture key + cache dir, four copies: `assemble-quotes.py:12,25`, `build-lesson.py:8,12`,
   `build-spans.py:43,52`, `c2-count.py:52,108` — `sha256(url)[:24]+".txt"` and the `.qcache` literal.
3. Document set: `assemble-quotes.py:13-18` DOC (4 URL→lane id) vs `c2-count.py:57-60` constants + DOCS
   (5 staged pairs). A fifth document means editing both.
4. Registry-row regex: `c2-count.py:79` `^ {0,3}\|[ \t]*(S\d{3,})[ \t]*\|` vs `build-c2-controls.py:57` the same
   shape without the capture group.
5. Spec-item names: `wave-complete-check.names_of` accepts str items and dedupes; `name-collision-check.py:30`
   `[i["name"] for i in spec["items"]]` accepts dicts only, no dedupe — one spec is usable by one check and
   exit 2 by the other.
6. `source:` line: `cited-id-check.py:31` `^source: {staged}\b` (no URL) vs `c2-count.py:170`
   `^source:\s*<id>\s+—\s+<url>` — two strictness levels for one convention.
7. `char N` token parsed twice: `decode-form-check.py:19` `\bchar\s+\d+` vs `c2-count.py:81` `\bchar\s+(\d+)`.
8. The form fact is stated twice in the lesson: the head sentence (`lesson-head.md`, "Decode form: …") and the
   per-row `form` cell built at `build-lesson.py:15`. Proven: replacing the cell with `txt` still prints
   FORM_NAMED, and QUALITY 76's own limit is "one naming per file, not one per offset" — the 55/62-row column is
   a second statement the criterion never reads.

## Defects found while replaying the documented commands

1. **QUALITY 74 is false at tip.** `python3 corpus/evidence/round50/stale-count-check.py` prints
   `STALE_HITS=8 UNRESOLVED=2 … STALE_COUNT=FAIL` rc 1, while `QUALITY.md:783` claims `STALE_COUNT=PASS`,
   exit 0, and names `corpus/evidence/round50/stale-count-after.txt` — `ls` says No such file. Two unresolved
   hits: `LOG.md:1803` `28 located quotes` (no later correction names it; the three landed corrections name
   QUALITY:746, README:1074, lessons/round-49.md:20) and `README.md:1080` `55-row manifest` — a **false hit**:
   that sentence describes round 50's own 55-row manifest, and the check's single receipt is round 49's 31 rows
   (its own named limit, "one receipt per scan"). The check cannot pass while the README describes round 50.
2. **The C2 control's receipt does not replay.** `controls/build-c2-controls.py` at tip: STAGED
   `REF_ID_UNBOUND=15 BOUND=0/4 C2=FAIL`; TOOLED `BOUND=4/4 REFUSED=0 REF_ID_UNBOUND=3 QUOTE_ROWS=55
   ON_BOUND=0/55 C2=FAIL`. `controls/c2-before.txt` records TOOLED `BOUND=3/4 BOUND_IDS=S106,S108,S109
   REF_ID_UNBOUND=8 QUOTE_ROWS=0`. Cause: `scratch()` copies the **live** `corpus/evidence/round50` (quotes.tsv
   and spans.tsv landed after the receipt) and reads the live package. The verdict reproduces; the numbers do not.
3. `cjk-ground-check.py:23` leaks one `tempfile.mkdtemp` dir per run and never removes it (5 dirs after 5 runs).

Live-tree note (not mine): at 19:28:36 another seat rewrote `quotes.tsv` (+7 rows) and `spans.tsv` (now 62 rows); `c2-count.py` at 19:29 prints `QUOTE_ROWS=62 … QUOTES_IN_LESSON=60/62 … C2=FAIL` rc 1 (lesson not regenerated). The nine files I reviewed are byte-identical to HEAD.

VERDICT: attacked the nine round-50 additions for dead weight and duplication — 8 deletion sets (20 lines) proven
output-identical and 8 duplications named (275 lines of copied round-49 code the largest); defect found:
QUALITY 74's `STALE_COUNT=PASS` and its `stale-count-after.txt` receipt are false at tip (exit 1, receipt absent,
one hit a false positive on round 50's own manifest), plus the C2 control receipt is unreplayable.
